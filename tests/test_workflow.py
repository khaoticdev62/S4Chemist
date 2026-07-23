"""Tests for the workflow trio: config, uninstall, tune-ids --flavor."""
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI = REPO_ROOT / "s4chemist_cli.py"


def run_cli(args, cwd, env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        stdin=subprocess.DEVNULL,
        env=env,
    )
    return (
        result.stdout.decode("utf-8", errors="replace"),
        result.stderr.decode("utf-8", errors="replace"),
        result.returncode,
    )


def test_config_sets_values(tmp_project):
    stdout, _, rc = run_cli(["config", str(tmp_project), "mod_name=NightShift", "creator=NightOwl"], REPO_ROOT)
    assert rc == 0
    cfg = (tmp_project / "s4modconfig.yaml").read_text(encoding="utf-8")
    assert "mod_name: NightShift" in cfg
    assert "creator: NightOwl" in cfg
    # and strict validate stops flagging the template config values
    stdout, _, _ = run_cli(["validate", str(tmp_project), "--strict"], REPO_ROOT)
    assert "ReplaceMe" not in stdout
    assert "YourName" not in stdout


def test_config_appends_new_key(tmp_project):
    _, _, rc = run_cli(["config", str(tmp_project), "custom_key=hello"], REPO_ROOT)
    assert rc == 0
    assert "custom_key: hello" in (tmp_project / "s4modconfig.yaml").read_text(encoding="utf-8")


def test_config_rejects_bad_token(tmp_project):
    _, _, rc = run_cli(["config", str(tmp_project), "noequalsign"], REPO_ROOT)
    assert rc == 2


def test_uninstall_removes_installed_copy(tmp_project, tmp_path):
    mods = tmp_path / "Mods"
    mods.mkdir()
    _, _, rc = run_cli(["install", str(tmp_project)], REPO_ROOT, env_extra={"S4_MODS_DIR": str(mods)})
    assert rc == 0
    assert (mods / tmp_project.name).exists()
    stdout, _, rc = run_cli(["uninstall", str(tmp_project)], REPO_ROOT, env_extra={"S4_MODS_DIR": str(mods)})
    assert rc == 0
    assert "Removed" in stdout
    assert not (mods / tmp_project.name).exists()


def test_uninstall_missing_target_errors(tmp_project, tmp_path):
    mods = tmp_path / "Mods"
    mods.mkdir()
    _, _, rc = run_cli(["uninstall", str(tmp_project)], REPO_ROOT, env_extra={"S4_MODS_DIR": str(mods)})
    assert rc == 2


def test_uninstall_refuses_foreign_directory(tmp_project, tmp_path):
    mods = tmp_path / "Mods"
    foreign = mods / tmp_project.name
    foreign.mkdir(parents=True)  # exists but no s4modconfig.yaml
    _, _, rc = run_cli(["uninstall", str(tmp_project)], REPO_ROOT, env_extra={"S4_MODS_DIR": str(mods)})
    assert rc == 2
    assert foreign.exists()  # untouched


def test_tune_ids_flavor_closes_strict_loop(tmp_project, repo_root):
    from tests.utils import cli_runner
    cli_runner(["new", str(tmp_project), "trait", "FlavorTrait"], repo_root)
    _, _, rc = run_cli(["tune-ids", str(tmp_project), "--flavor"], REPO_ROOT)
    assert rc == 0
    xml = next(tmp_project.rglob("*_trait.xml")).read_text(encoding="utf-8")
    assert "Replace with" not in xml
    assert "0x00000000" not in xml
    # config template values fixed too -> strict fully green
    run_cli(["config", str(tmp_project), "mod_name=FlavorMod", "creator=Tester"], REPO_ROOT)
    stdout, _, rc = run_cli(["validate", str(tmp_project), "--strict"], REPO_ROOT)
    assert rc == 0 and "0 issues" in stdout


def test_help_lists_trio():
    stdout, _, rc = run_cli(["--help"], REPO_ROOT)
    assert rc == 0
    for cmd in ("config", "uninstall"):
        assert cmd in stdout
