import os
import subprocess
import textwrap
import tempfile

SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'enforce_style_guide.sh'))


def run_cmd(cmd, env=None, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env, cwd=cwd)
    return r


def test_is_ignored_basic(tmp_path):
    # Prepare a minimal styleignore and test paths
    styleignore = tmp_path / '.styleignore'
    styleignore.write_text("""# ignore molecule configs\n*/molecule/*\nroles/ops\n""")

    # Source the script and call is_ignored for a molecule path
    cmd = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        STYLE_IGNORE="{styleignore}"
        is_ignored "roles/containers/media/molecule/negative/molecule.yml" && echo YES || echo NO
    """)

    r = run_cmd(cmd, cwd=tmp_path)
    assert r.returncode == 0
    assert 'YES' in r.stdout.strip()


def test_enforce_fqcn_respects_molecule_ignore(tmp_path):
    # Create a tiny project tree with a molecule file that would match the FQCN pattern
    proj = tmp_path
    mol = proj / 'roles' / 'containers' / 'caddy' / 'molecule' / 'negative'
    mol.mkdir(parents=True)

    mol_file = mol / 'molecule.yml'
    mol_file.write_text(textwrap.dedent("""
        ---
        - hosts: localhost
          tasks:
            - name: short copy
              copy:
                src: foo
                dest: /tmp
    """))

    # Without ignore, enforce_fqcn_standards should report the file
    cmd_no_ignore = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT="{proj}"
        enforce_fqcn_standards
    """)
    r_no = run_cmd(cmd_no_ignore, cwd=proj)
    # Should warn about at least one file
    assert 'Found' in r_no.stdout or 'Found' in r_no.stderr

    # With ignore pattern, it should not report that molecule file
    styleignore = proj / '.styleignore'
    styleignore.write_text("*/molecule/*\n")

    cmd_with_ignore = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT="{proj}"
        STYLE_IGNORE="{styleignore}"
        enforce_fqcn_standards
    """)
    r_yes = run_cmd(cmd_with_ignore, cwd=proj)

    out = r_yes.stdout + r_yes.stderr
    assert 'Found' not in out


def test_security_ignore_respects_styleignore(tmp_path):
    # Prepare a project with a file that contains a password-like literal
    proj = tmp_path
    sec_dir = proj / 'roles' / 'example' / 'molecule' / 'default'
    sec_dir.mkdir(parents=True)

    sec_file = sec_dir / 'converge.yml'
    sec_file.write_text(textwrap.dedent("""
        ---
        - hosts: localhost
          vars:
            some_password: "changeme"
          tasks:
            - name: noop
              debug:
                msg: "ok"
    """))

    # Run security check without ignore should report the file
    cmd_no_ignore = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT="{proj}"
        enforce_security_standards
    """)
    r_no = run_cmd(cmd_no_ignore, cwd=proj)
    assert 'Found' in (r_no.stdout + r_no.stderr)

    # Add an ignore entry and ensure the file is skipped
    styleignore = proj / '.styleignore'
    styleignore.write_text("*/molecule/*\n")

    cmd_with_ignore = textwrap.dedent(f"""
        source "{SCRIPT_PATH}" >/dev/null 2>&1 || true
        PROJECT_ROOT="{proj}"
        STYLE_IGNORE="{styleignore}"
        enforce_security_standards
    """)
    r_yes = run_cmd(cmd_with_ignore, cwd=proj)
    out = r_yes.stdout + r_yes.stderr
    assert 'Found' not in out
