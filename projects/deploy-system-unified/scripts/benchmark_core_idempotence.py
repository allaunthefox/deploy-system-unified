#!/usr/bin/env python3
"""Run a repeat-run idempotence benchmark for all roles/core/* roles.

The benchmark runs each role in an isolated container, applies the role twice,
and records whether the second run is idempotent (changed=0 and failed=0).

Artifacts are written to:
  projects/deploy-system-unified/ci-artifacts/idempotence/<timestamp>/
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import textwrap
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RECAP_RE = re.compile(
    r"ok=(?P<ok>\d+)\s+changed=(?P<changed>\d+)\s+unreachable=(?P<unreachable>\d+)\s+"
    r"failed=(?P<failed>\d+)\s+skipped=(?P<skipped>\d+)\s+rescued=(?P<rescued>\d+)\s+ignored=(?P<ignored>\d+)"
)


@dataclass
class RoleResult:
    role: str
    status: str
    duration_seconds: float
    changed_second_run: int | None
    failed_second_run: int | None
    unreachable_second_run: int | None
    recap_line_second_run: str | None
    failure_excerpt: str | None
    log_path: str
    playbook_path: str


def run_command(
    cmd: list[str],
    *,
    cwd: Path,
    timeout_seconds: int | None = None,
    stdin_text: str | None = None,
) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        input=stdin_text,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    return proc.returncode, proc.stdout + proc.stderr


def build_runner_image(repo_root: Path, image: str) -> None:
    dockerfile = textwrap.dedent(
        """\
        FROM ubuntu:22.04
        ENV DEBIAN_FRONTEND=noninteractive
        RUN echo 'APT::Sandbox::User "root";' > /etc/apt/apt.conf.d/99sandbox-root \\
            && apt-get update -y \\
            && apt-get install -y --no-install-recommends \\
               python3 \\
               python3-pip \\
               python3-apt \\
               sudo \\
               ca-certificates \\
            && pip3 install --no-cache-dir "ansible-core>=2.15,<2.16" \\
            && ansible-galaxy collection install ansible.posix community.general \\
            && rm -rf /var/lib/apt/lists/*
        """
    )
    inspect_rc, _ = run_command(
        ["docker", "image", "inspect", image],
        cwd=repo_root,
    )
    if inspect_rc == 0:
        return

    build_rc, build_out = run_command(
        ["docker", "build", "-t", image, "-f", "-", "."],
        cwd=repo_root,
        stdin_text=dockerfile,
    )
    if build_rc != 0:
        raise RuntimeError(f"Failed to build container image {image}\n{build_out}")


def parse_recap(run_text: str) -> tuple[dict[str, int] | None, str | None]:
    recap_line = None
    recap_data = None
    for line in run_text.splitlines():
        match = RECAP_RE.search(line)
        if match:
            recap_line = line.strip()
            recap_data = {k: int(v) for k, v in match.groupdict().items()}
    return recap_data, recap_line


def first_failure_excerpt(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if "fatal:" in stripped or "FAILED!" in stripped or stripped.startswith("ERROR!"):
            return stripped
    return None


def split_runs(log_text: str) -> tuple[str, str]:
    run1_start = "=== RUN1 BEGIN ==="
    run1_end = "=== RUN1 END ==="
    run2_start = "=== RUN2 BEGIN ==="
    run2_end = "=== RUN2 END ==="

    if run1_start not in log_text or run1_end not in log_text:
        return "", ""
    if run2_start not in log_text or run2_end not in log_text:
        return "", ""

    run1 = log_text.split(run1_start, 1)[1].split(run1_end, 1)[0]
    run2 = log_text.split(run2_start, 1)[1].split(run2_end, 1)[0]
    return run1.strip(), run2.strip()


def role_playbook(role: str) -> str:
    return textwrap.dedent(
        f"""\
        - name: Benchmark core/{role}
          hosts: localhost
          gather_facts: true
          become: true
          vars:
            virt_type: container
            is_virtualized: true
          roles:
            - role: core/{role}
        """
    )


def benchmark_role(
    *,
    repo_root: Path,
    image: str,
    role: str,
    role_timeout: int,
    run_dir: Path,
) -> RoleResult:
    playbooks_dir = run_dir / "playbooks"
    logs_dir = run_dir / "logs"
    playbooks_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    playbook_path = playbooks_dir / f"core_{role}.yml"
    playbook_path.write_text(role_playbook(role), encoding="utf-8")

    rel_playbook = playbook_path.relative_to(repo_root).as_posix()
    container_script = textwrap.dedent(
        f"""\
        set -euo pipefail
        export ANSIBLE_ROLES_PATH=/workspace/projects/deploy-system-unified/roles:/workspace/projects/deploy-system-unified
        echo 'benchmark-vault-pass' > /tmp/ansible-vault-pass
        chmod 0600 /tmp/ansible-vault-pass
        export ANSIBLE_VAULT_PASSWORD_FILE=/tmp/ansible-vault-pass
        if command -v apt-get >/dev/null 2>&1; then
          apt-get -o APT::Sandbox::User=root update -y >/dev/null 2>&1 || true
        fi
        ansible-playbook /workspace/{rel_playbook} -i "localhost," -c local > /tmp/run1.log 2>&1 || true
        ansible-playbook /workspace/{rel_playbook} -i "localhost," -c local > /tmp/run2.log 2>&1 || true
        echo "=== RUN1 BEGIN ==="
        cat /tmp/run1.log
        echo "=== RUN1 END ==="
        echo "=== RUN2 BEGIN ==="
        cat /tmp/run2.log
        echo "=== RUN2 END ==="
        """
    )

    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{repo_root.as_posix()}:/workspace",
        "-w",
        "/workspace",
        image,
        "bash",
        "-lc",
        container_script,
    ]

    start = time.time()
    status = "error"
    log_output = ""
    try:
        rc, log_output = run_command(cmd, cwd=repo_root, timeout_seconds=role_timeout)
        run1_text, run2_text = split_runs(log_output)

        recap, recap_line = parse_recap(run2_text)
        fail_excerpt = first_failure_excerpt(run2_text) or first_failure_excerpt(run1_text)

        changed = recap["changed"] if recap else None
        failed = recap["failed"] if recap else None
        unreachable = recap["unreachable"] if recap else None

        if rc != 0:
            status = "error_container"
        elif recap is None and (
            "ERROR!" in run2_text or "FAILED!" in run2_text or "fatal:" in run2_text
        ):
            status = "failed"
        elif recap is None:
            status = "error_no_recap"
        elif failed and failed > 0:
            status = "failed"
        elif unreachable and unreachable > 0:
            status = "failed"
        elif changed == 0:
            status = "idempotent"
        else:
            status = "non_idempotent"

    except subprocess.TimeoutExpired as exc:
        status = "error_timeout"
        log_output = (exc.stdout or "") + (exc.stderr or "")
        recap_line = None
        changed = None
        failed = None
        unreachable = None
        fail_excerpt = f"Timed out after {role_timeout}s"
    else:
        if "recap_line" not in locals():
            recap_line = None
        if "changed" not in locals():
            changed = None
        if "failed" not in locals():
            failed = None
        if "unreachable" not in locals():
            unreachable = None
        if "fail_excerpt" not in locals():
            fail_excerpt = None

    duration = time.time() - start
    log_path = logs_dir / f"core_{role}.log"
    log_path.write_text(log_output, encoding="utf-8")

    return RoleResult(
        role=role,
        status=status,
        duration_seconds=round(duration, 2),
        changed_second_run=changed,
        failed_second_run=failed,
        unreachable_second_run=unreachable,
        recap_line_second_run=recap_line,
        failure_excerpt=fail_excerpt,
        log_path=str(log_path.relative_to(repo_root)),
        playbook_path=str(playbook_path.relative_to(repo_root)),
    )


def collect_roles(roles_dir: Path, selected: list[str] | None) -> list[str]:
    available = sorted([p.name for p in roles_dir.iterdir() if p.is_dir()])
    if not selected:
        return available

    unknown = sorted(set(selected) - set(available))
    if unknown:
        raise ValueError(f"Unknown core roles: {', '.join(unknown)}")
    return [r for r in available if r in selected]


def summary_counts(results: list[RoleResult]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return counts


def write_markdown_summary(
    *,
    repo_root: Path,
    run_dir: Path,
    results: list[RoleResult],
    started_at: str,
    ended_at: str,
) -> Path:
    counts = summary_counts(results)
    rows = []
    for result in results:
        rows.append(
            "| core/{role} | {status} | {changed} | {failed} | {unreachable} | {duration}s | `{log}` |".format(
                role=result.role,
                status=result.status,
                changed=result.changed_second_run if result.changed_second_run is not None else "-",
                failed=result.failed_second_run if result.failed_second_run is not None else "-",
                unreachable=result.unreachable_second_run if result.unreachable_second_run is not None else "-",
                duration=result.duration_seconds,
                log=result.log_path,
            )
        )

    lines = [
        "# CORE_ROLE_IDEMPOTENCE_BASELINE",
        "",
        f"- Started (UTC): {started_at}",
        f"- Ended (UTC): {ended_at}",
        f"- Roles benchmarked: {len(results)}",
        f"- Idempotent: {counts.get('idempotent', 0)}",
        f"- Non-idempotent: {counts.get('non_idempotent', 0)}",
        f"- Failed: {counts.get('failed', 0)}",
        f"- Errors: {sum(v for k, v in counts.items() if k.startswith('error'))}",
        "",
        "## Per-Role Results",
        "",
        "| Role | Status | Changed (2nd run) | Failed (2nd run) | Unreachable (2nd run) | Duration | Log |",
        "| :--- | :--- | ---: | ---: | ---: | ---: | :--- |",
        *rows,
        "",
        "## First Failure Excerpts",
        "",
    ]
    for result in results:
        if result.failure_excerpt:
            lines.append(f"- `core/{result.role}`: {result.failure_excerpt}")

    summary_path = run_dir / "summary.md"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark idempotence across roles/core/*")
    parser.add_argument(
        "--roles",
        help="Comma-separated core role names (default: all core roles)",
        default="",
    )
    parser.add_argument(
        "--role-timeout",
        type=int,
        default=1200,
        help="Timeout in seconds per role benchmark run (default: 1200)",
    )
    parser.add_argument(
        "--image",
        default="dsu-idempotence-bench:ubuntu22.04-v2",
        help="Container image to use for benchmark runs",
    )
    parser.add_argument(
        "--no-build-image",
        action="store_true",
        help="Skip building benchmark image when missing",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    dsu_root = script_dir.parent
    repo_root = dsu_root.parent.parent
    roles_dir = dsu_root / "roles" / "core"

    selected_roles = [r.strip() for r in args.roles.split(",") if r.strip()] or None
    roles = collect_roles(roles_dir, selected_roles)
    if not roles:
        print("No core roles found to benchmark.", file=sys.stderr)
        return 1

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = dsu_root / "ci-artifacts" / "idempotence" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now(timezone.utc).isoformat()

    if not args.no_build_image:
        build_runner_image(repo_root, args.image)

    results: list[RoleResult] = []
    for role in roles:
        print(f"[benchmark] core/{role} ...", flush=True)
        result = benchmark_role(
            repo_root=repo_root,
            image=args.image,
            role=role,
            role_timeout=args.role_timeout,
            run_dir=run_dir,
        )
        results.append(result)
        print(
            f"[result] core/{role}: {result.status} (changed={result.changed_second_run}, failed={result.failed_second_run}, unreachable={result.unreachable_second_run})",
            flush=True,
        )

    ended_at = datetime.now(timezone.utc).isoformat()
    summary_path = write_markdown_summary(
        repo_root=repo_root,
        run_dir=run_dir,
        results=results,
        started_at=started_at,
        ended_at=ended_at,
    )

    payload: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": started_at,
        "ended_at_utc": ended_at,
        "roles_benchmarked": len(results),
        "summary_counts": summary_counts(results),
        "results": [r.__dict__ for r in results],
        "summary_markdown_path": str(summary_path.relative_to(repo_root)),
    }
    json_path = run_dir / "summary.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    latest_path = dsu_root / "ci-artifacts" / "idempotence" / "LATEST_RUN.txt"
    latest_path.write_text(f"{run_id}\n", encoding="utf-8")

    print(f"[done] summary: {json_path.relative_to(repo_root)}")
    print(f"[done] summary: {summary_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
