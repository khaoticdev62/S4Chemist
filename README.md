# ⚗ S4Chemist

**Portable Sims 4 Mod Construction CLI** — scaffold, validate, package, and install Sims 4
mods from one tool, with three interfaces: a polished terminal CLI, an arrow-key menu, and a
full Textual dashboard.

[![Tests](https://github.com/khaoticdev62/S4Chemist/actions/workflows/tests.yml/badge.svg)](https://github.com/khaoticdev62/S4Chemist/actions/workflows/tests.yml)

## Install

**Portable exe (Windows, no Python needed):** download `S4Chemist-portable-*.zip` from the
[latest release](https://github.com/khaoticdev62/S4Chemist/releases), extract anywhere, and
double-click `s4chemist_cli.exe` — it opens an arrow-key menu.

**From source** (Python 3.10+):

```bash
pip install rich questionary textual
python s4chemist_cli.py --help
```

**pip:**

```bash
pip install s4chemist
```

## Quickstart

```bash
s4chemist_cli init MyMod                 # create a mod project
s4chemist_cli new MyMod trait SunnyTrait # add an artifact (18 kinds supported)
s4chemist_cli validate MyMod             # hygiene check (add --strict for placeholders)
s4chemist_cli tune-ids MyMod             # replace 0x00000000 with stable tuning ids
s4chemist_cli build MyMod                # zip it up (reports size + file count)
s4chemist_cli install MyMod              # copy into your Mods folder
```

Or skip the typing: bare-launch opens the **arrow-key menu**, and

```bash
s4chemist_cli tui MyMod
```

opens the **dashboard**: live pipeline table, guided creation form (all 18 mod kinds),
file tree with syntax-highlighted preview, command log, and a Ctrl+P command palette —
all scaling to your desktop window.

## Commands

| Command | What it does |
|---|---|
| `init <name>` | Create a mod project skeleton |
| `new <proj> <kind> <name>` | Scaffold an artifact (xml_snippet, ts4script, package, career, trait, buff, interaction, event, achievement, aspiration, whim, club, holiday, loot_action, testset, relationship, skill, motive) |
| `generate <type> <name>` | Scaffold + tuning params (`--param k=v`) |
| `wizard <type> [name]` | Guided creation (interactive, or scripted via `--param`) |
| `validate [path]` | Actionable hygiene issues; `--strict` also flags placeholders ([rules](docs/validation.md)) |
| `tune-ids [path]` | Rewrite placeholder tuning ids to stable generated ids |
| `build` / `package` | Zip the project (release variant excludes owner docs) |
| `install [path]` | Copy to Mods (`--to-dir` or `S4_MODS_DIR` to override) |
| `pipeline [-next/-unlock/-reset]` | Phase-by-phase build tracker |
| `changelog [path]` | Prepend a dated CHANGELOG entry |
| `tui [path]` | Full Textual dashboard |
| `doctor` / `game-python` / `version` / `help` | Environment probes and info |

## UI highlights

- ⚗ brand banner, state-colored panel borders (red = fail, green = ok, yellow = local,
  blue = info)
- Color-off: `NO_COLOR`, `--no-color`, auto-plain when piped; `S4_ASCII=1` for legacy consoles
- Every panel is actionable: validation issues name the file and the fix

## Development

```bash
pip install -e ".[dev]"
python -m pytest        # 72 tests incl. real-mod E2E + headless TUI tests
ruff check s4chemist_cli.py tests
mypy s4chemist_cli.py
pyinstaller s4chemist_cli.spec   # build the portable exe
```

Single-file CLI (`s4chemist_cli.py`) — architecture notes in [CLAUDE.md](CLAUDE.md) and
[AGENTS.md](AGENTS.md). Changelog: [CHANGELOG.md](CHANGELOG.md).

## License

MIT
