import os
import subprocess
import textwrap

SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'enforce_style_guide.sh'))


def run_cmd(cmd, env=None, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env, cwd=cwd, executable='/bin/bash')
    return r


def test_is_ignored_basic(tmp_path):
    # Prepare a minimal styleignore and test paths
    styleignore = tmp_path / '.styleignore'
    styleignore.write_text("# ignore molecule configs\n*/molecule/*\nroles/ops\n")

    # Source the script and call is_ignored for a molecule path
    cmd = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        STYLE_IGNORE="{styleignore}"
        is_ignored "roles/containers/media/molecule/negative/molecule.yml" && echo YES || echo NO
    """)

    r = run_cmd(cmd, cwd=tmp_path)
    assert r.returncode == 0
    assert 'YES' in r.stdout.strip()


def test_enforce_fqcn_respects_styleignore(tmp_path):
    # Create a tiny project tree with a task file that would match the FQCN pattern
    proj = tmp_path
    mol = proj / 'roles' / 'containers' / 'caddy' / 'tasks'
    mol.mkdir(parents=True)

    mol_file = mol / 'main.yml'
    # No leading newline, minimal indentation
    mol_file.write_text(textwrap.dedent("""
        - name: simple task
          copy:
            src: foo
            dest: /tmp
    """).lstrip())

    # Without ignore, enforce_fqcn_standards should report the file
    cmd_no_ignore = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT=\"{proj}\" 
        STYLE_IGNORE="/nonexistent"
        enforce_fqcn_standards 2>&1
    """)
    r_no = run_cmd(cmd_no_ignore, cwd=proj)
    # Should warn about at least one file
    assert 'Found' in r_no.stdout or 'Found' in r_no.stderr

    # With ignore pattern, it should not report that file
    styleignore = proj / '.styleignore'
    styleignore.write_text("roles/containers/caddy/tasks/*\n")

    cmd_with_ignore = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT=\"{proj}\" 
        STYLE_IGNORE=\"{styleignore}\" 
        enforce_fqcn_standards 2>&1
    """)
    r_yes = run_cmd(cmd_with_ignore, cwd=proj)

    out = r_yes.stdout + r_yes.stderr
    assert 'Found' not in out


def test_security_ignore_respects_styleignore(tmp_path):
    # Prepare a project with a file that contains a password-like literal
    proj = tmp_path
    sec_dir = proj / 'roles' / 'example' / 'tasks'
    sec_dir.mkdir(parents=True)

    sec_file = sec_dir / 'main.yml'
    sec_file.write_text(textwrap.dedent("""
        - name: set password
          set_fact:
            my_password: \"changeme\"
    """).lstrip())

    # Run security check without ignore should report the file
    cmd_no_ignore = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT=\"{proj}\" 
        STYLE_IGNORE="/nonexistent"
        enforce_security_standards 2>&1
    """)
    r_no = run_cmd(cmd_no_ignore, cwd=proj)
    assert 'Found' in (r_no.stdout + r_no.stderr)

    # Add an ignore entry and ensure the file is skipped
    styleignore = proj / '.styleignore'
    styleignore.write_text("roles/example/tasks/main.yml\n")

    cmd_with_ignore = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT=\"{proj}\" 
        STYLE_IGNORE=\"{styleignore}\" 
        enforce_security_standards 2>&1
    """)
    r_yes = run_cmd(cmd_with_ignore, cwd=proj)
    out = r_yes.stdout + r_yes.stderr
    assert 'Found' not in out


def test_bulk_security_ignores(tmp_path):
    # Create multiple files that would be flagged by security checks
    proj = tmp_path
    candidates = [
        'roles/containers/media/defaults/main.yml',
        'roles/containers/caddy/defaults/main.yml',
        'roles/orchestration/k8s_node/defaults/main.yml',
        'roles/networking/vpn_mesh/defaults/main.yml',
        'roles/security/access/tasks/main.yml',
    ]

    for p in candidates:
        f = proj / p
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(textwrap.dedent("""
            ---
            some_secret: \"changeme_placeholder\"
        """).lstrip())

    # Run security check without ignore should report matches
    cmd_no = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT=\"{proj}\" 
        STYLE_IGNORE="/nonexistent"
        enforce_security_standards 2>&1
    """)
    r_no = run_cmd(cmd_no, cwd=proj)
    assert 'Found' in (r_no.stdout + r_no.stderr)

    # Add targeted ignore entries and verify they are skipped
    styleignore = proj / '.styleignore'
    styleignore.write_text('\n'.join(candidates) + '\n')

    cmd_yes = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT=\"{proj}\" 
        STYLE_IGNORE=\"{styleignore}\" 
        enforce_security_standards 2>&1
    """)
    r_yes = run_cmd(cmd_yes, cwd=proj)
    out = r_yes.stdout + r_yes.stderr
    assert 'Found' not in out


def test_is_ignored_negation_and_regex(tmp_path):
    # Prepare a styleignore with a broad glob, a negation, and a regex
    styleignore = tmp_path / '.styleignore'
    styleignore.write_text(textwrap.dedent("""
        */molecule/*
        !roles/containers/caddy/molecule/*
        re:^roles/special/molecule/negative/
    """))

    # Path that should be ignored by glob
    p1 = 'roles/containers/media/molecule/negative/molecule.yml'
    # Path that should be explicitly un-ignored by negation
    p2 = 'roles/containers/caddy/molecule/negative/molecule.yml'
    # Path that should be ignored by regex
    p3 = 'roles/special/molecule/negative/molecule.yml'

    cmd = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        STYLE_IGNORE=\"{styleignore}\" 
        is_ignored \"{p1}\" && echo P1_IGNORED || echo P1_NOT
        is_ignored \"{p2}\" && echo P2_IGNORED || echo P2_NOT
        is_ignored \"{p3}\" && echo P3_IGNORED || echo P3_NOT
    """)

    r = run_cmd(cmd, cwd=tmp_path)
    out = r.stdout.strip().splitlines()
    assert 'P1_IGNORED' in out
    assert 'P2_NOT' in out
    assert 'P3_IGNORED' in out


def test_ignores_workflows_and_artifacts(tmp_path):
    # Create a fake GH workflow and a CI artifact file that would otherwise match patterns
    proj = tmp_path
    wf = proj / '.github' / 'workflows'
    wf.mkdir(parents=True)
    wf_file = wf / 'ci-debug.yml'
    wf_file.write_text(textwrap.dedent("""
        ---
        name: Fake workflow
        on: [push]
        jobs:
          test:
            runs-on: ubuntu-latest
            steps:
              - name: Run something
                run: |
                  echo "hello"
    """))

    artifact_dir = proj / 'projects' / 'deploy-system-unified' / 'ci-artifacts'
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_file = artifact_dir / 'compliance_report.md'
    artifact_file.write_text('some report with commands: copy: something')

    # Create styleignore containing our new patterns
    styleignore = proj / '.styleignore'
    styleignore.write_text('.github/workflows/*.yml\nprojects/*/ci-artifacts/*\n')

    cmd = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT=\"{proj}\" 
        STYLE_IGNORE=\"{styleignore}\" 
        # Ensure workflows are not reported by FQCN check
        enforce_fqcn_standards
        # Ensure artifacts are not reported by security check
        enforce_security_standards
    """)
    r = run_cmd(cmd, cwd=proj)
    out = r.stdout + r.stderr
    # No 'Found' lines should be present
    assert 'Found' not in out


def test_fqcn_ignores_group_param(tmp_path):
    # Create a role file with a parameter named 'group' which should NOT be flagged as 'group' module
    proj = tmp_path
    role_dir = proj / 'roles' / 'test_role' / 'tasks'
    role_dir.mkdir(parents=True)
    task_file = role_dir / 'main.yml'
    
    # This content mimics a task where 'group' is a parameter key, not the module name
    task_file.write_text(textwrap.dedent("""
        - name: Create a user with a specific primary group
          user:
            name: testuser
            group: testgroup
            state: present
    """).lstrip())

    # We expect FQCN check to PASS (no output) because 'group:' is indented and clearly a param
    cmd = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT=\"{proj}\" 
        STYLE_IGNORE="/nonexistent"
        enforce_fqcn_standards
    """)
    r = run_cmd(cmd, cwd=proj)
    out = r.stdout + r.stderr
    assert 'Found' not in out
