"""End-to-end tests of a real mod lifecycle driven entirely through the CLI.

Unlike the unit-style tests (which use the tmp_project fixture), these build the
project via `init` itself and walk the full authoring flow:
init -> edit config -> new -> validate -> tune-ids -> build -> package ->
install -> pipeline/changelog, plus a non-interactive `wizard` scenario.
"""
import os
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI = REPO_ROOT / "s4chemist_cli.py"


def run_cli(args, cwd=REPO_ROOT, env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        stdin=subprocess.DEVNULL,  # force non-interactive
        env=env,
    )
    # Decode manually: text=True loses output on some Windows Pythons (3.11.9)
    # because the CLI reconfigures its stdout to UTF-8.
    return (
        result.stdout.decode("utf-8", errors="replace"),
        result.stderr.decode("utf-8", errors="replace"),
        result.returncode,
    )


def test_full_mod_lifecycle(tmp_path):
    proj = tmp_path / "NightShift"

    # 1. init — project skeleton exists.
    stdout, _, rc = run_cli(["init", str(proj)])
    assert rc == 0
    assert (proj / "s4modconfig.yaml").exists()
    assert (proj / "src" / "xml_snippets").is_dir()
    assert (proj / "src" / "ts4script").is_dir()
    assert (proj / "src" / "package").is_dir()

    # 2. Edit s4modconfig.yaml like a real user would.
    cfg = proj / "s4modconfig.yaml"
    text = cfg.read_text(encoding="utf-8")
    assert "mod_name: ReplaceMe" in text
    assert "creator: YourName" in text
    text = text.replace("mod_name: ReplaceMe", "mod_name: NightShift")
    text = text.replace("creator: YourName", "creator: NightOwl")
    cfg.write_text(text, encoding="utf-8")

    # 3. Scaffold career, buff, and interaction artifacts.
    artifacts = {
        "career": proj / "src" / "xml_snippets" / "NightShift_career" / "NightShift_career.xml",
        "buff": proj / "src" / "xml_snippets" / "NightFocus_buff" / "NightFocus_buff.xml",
        "interaction": proj / "src" / "xml_snippets" / "BrewCoffee_interaction" / "BrewCoffee_interaction.xml",
    }
    for kind, name in [("career", "NightShift"), ("buff", "NightFocus"), ("interaction", "BrewCoffee")]:
        _, _, rc = run_cli(["new", str(proj), kind, name])
        assert rc == 0, f"new {kind} {name} failed"
    for path in artifacts.values():
        assert path.exists(), f"missing artifact {path}"

    # 4. Non-strict validate is clean.
    stdout, _, rc = run_cli(["validate", str(proj)])
    assert rc == 0
    assert "0 issues" in stdout

    # 5. Strict validate flags the 0x00000000 placeholder tuning ids.
    stdout, _, rc = run_cli(["validate", str(proj), "--strict"])
    assert rc > 0
    assert "0x00000000" in stdout

    # 6. tune-ids assigns real ids; no 0x00000000 remains in any src XML.
    _, _, rc = run_cli(["tune-ids", str(proj)])
    assert rc == 0
    for xml in (proj / "src").rglob("*.xml"):
        assert "0x00000000" not in xml.read_text(encoding="utf-8"), f"placeholder id left in {xml}"

    # 7. Strict validate again: placeholder-id issues are gone (config was
    #    fixed in step 2). Flavor-text placeholders may still be flagged, so
    #    only assert the id placeholder no longer appears in the output.
    stdout, _, _ = run_cli(["validate", str(proj), "--strict"])
    assert "0x00000000" not in stdout

    # 8. build — exactly one valid zip, no dist/tmp entries, contains career XML.
    _, _, rc = run_cli(["build", str(proj)])
    assert rc == 0
    zips = list((proj / "dist").glob("*.zip"))
    assert len(zips) == 1
    assert zipfile.is_zipfile(zips[0])
    with zipfile.ZipFile(zips[0]) as zf:
        assert zf.testzip() is None
        names = zf.namelist()
    assert names, "archive must not be empty"
    assert not any(n.startswith(("dist/", "tmp/", "dist\\", "tmp\\")) for n in names)
    assert any(n.endswith("NightShift_career.xml") for n in names)

    # 9. package — a release-named archive appears.
    _, _, rc = run_cli(["package", str(proj)])
    assert rc == 0
    assert any(z for z in (proj / "dist").glob("*.zip") if "-release-" in z.name)

    # 10. install into a Sims Mods-style dir via S4_MODS_DIR.
    mods = tmp_path / "Mods"
    mods.mkdir()
    _, _, rc = run_cli(["install", str(proj)], env_extra={"S4_MODS_DIR": str(mods)})
    assert rc == 0
    installed = mods / proj.name
    assert installed.is_dir()
    assert not (installed / "dist").exists()
    assert not (installed / "tmp").exists()

    # 11. pipeline shows a Progress line; changelog creates CHANGELOG.md.
    stdout, _, rc = run_cli(["pipeline", str(proj)])
    assert rc == 0
    assert "Progress:" in stdout
    _, _, rc = run_cli(["changelog", str(proj)])
    assert rc == 0
    assert (proj / "CHANGELOG.md").exists()

    # 12. Sims-Mods-style directory check on the installed copy.
    assert (installed / "s4modconfig.yaml").exists()
    assert (installed / "src").is_dir()


def test_wizard_noninteractive_in_project(tmp_path):
    proj = tmp_path / "WizardMod"
    _, _, rc = run_cli(["init", str(proj)])
    assert rc == 0

    stdout, _, rc = run_cli(["wizard", "trait", "MoonMood", "--param", "label=Moon Mood"], cwd=proj)
    assert rc == 0
    xml = proj / "src" / "xml_snippets" / "MoonMood_trait" / "MoonMood_trait.xml"
    assert xml.exists()
    assert "Moon Mood" in xml.read_text(encoding="utf-8")
    assert (proj / "CHANGELOG.md").exists()
