from tests.utils import cli_runner


def test_help_shows_commands(repo_root):
    stdout, _, rc = cli_runner(["--help"], repo_root)
    assert rc == 0
    assert "init" in stdout
    assert "validate" in stdout
    assert "build" in stdout


def test_version_prints(repo_root):
    stdout, _, rc = cli_runner(["version"], repo_root)
    assert rc == 0
    assert f"s4chemist_cli v{_pyproject_version(repo_root)}" in stdout


def _pyproject_version(repo_root) -> str:
    for line in (repo_root / "pyproject.toml").read_text(encoding="utf-8").splitlines():
        if line.startswith("version"):
            return line.split("=", 1)[1].strip().strip('"')
    raise AssertionError("version not found in pyproject.toml")


def test_doctor_checks_environment(repo_root):
    stdout, _, rc = cli_runner(["doctor"], repo_root)
    assert rc in (0, 1)
    assert "Python" in stdout
