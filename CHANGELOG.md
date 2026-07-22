# Changelog

## 0.2.0 — 2026-07-22

Implementation of PLAN.md phases 0–5.

### Added
- pytest suite (25 tests) with CI workflow (ruff + mypy + pytest on windows-latest)
- `COMMANDS` registry with data-driven help metadata; `main()` dispatches via `_cmd_<name>` handlers
- `validate` now prints one actionable line per issue; `--strict` also flags template config
  values (`ReplaceMe`/`YourName`), `0x00000000` tuning ids, and placeholder flavor text
- `docs/validation.md` documenting all validation checks and tag-matching rules
- `wizard --param k=v` overrides and non-interactive mode (defaults + overrides when not a TTY)
- `install` honors `S4_MODS_DIR` (priority: `--to-dir` > env var > auto-detect)
- Post-build archive integrity checks (`_verify_archive`)

### Fixed
- Windows: `_zip_project` exclusions used backslash paths, so `dist/`/`tmp/` were never excluded
  and archives embedded partial copies of themselves
- `testset` factory wrote `testset_name`; validation and `tune-ids` expect `test_set_name`
- Removed dead duplicate `pipeline` dispatch block, dead `_STBL_REPLACEMENTS` dict, and
  duplicated factory maps (now single `MOD_FACTORIES`)
- `build --release` semantics made explicit (delegates to `package_release`)

## 0.1.1 — 2026-07-21

- Version bump; added USAGE.md.
