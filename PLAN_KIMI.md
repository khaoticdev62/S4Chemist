# S4Chemist Kimi K3 Execution Plan

Focus: convert CLI scaffold into something actually usable for real mod authors.
This plan treats the existing `PLAN.md` as the canonical checklist and augments it with scoped execution items.

## Goal

Make `s4chemist_cli.py` a reliable local authoring surface for Sims 4 mods by fixing the biggest blockers first:
content fidelity, validation trust, packaging/release workflow, and fast feedback loops.

## Phase 0 — Test surface + regression confidence

Tasks:
- Add `tests/utils.py` if missing or fragmenting across test files.
- Add focused regression tests for:
  - init/new/validate/build/package end-to-end for all kinds
  - generate with --param rewrites
  - tune-ids stable-id rewrites and idempotency
  - packaging exclusions and integrity after build/package
  - install/uninstall with S4_MODS_DIR and --to-dir override
  - wizard interactive fallback and non-interactive name handling
- Verify coverage locally on Windows: `python -m pytest tests/ -v`.
- Commit message style: `test: add <area> regression coverage`.

Deliverable: failing tests tell you what’s broken before you ship.

## Phase 1 — Validation completeness and correctness

Tasks:
- Extend `validate_project_issues` to validate:
  - manifest.json for ts4script projects
  - s4modconfig.yaml schema: required fields, version format like x.y.z
  - localization files produced by tuning/generation/wizard
  - package files existence for CC-style release candidates
- Keep strict mode conservative; add new checks under strict first.
- Do not drop existing caller-visible behavior.

Deliverable: validation catches real-world scaffold problems and the output is actionable by file.

## Phase 2 — Content fidelity per mod kind

Tasks:
- For every supported kind:
  - expand XML param-aware rewrites beyond label/description where possible
  - generate meaningful README content with type-specific next steps
  - add at least one concrete tuning tag example per kind
- ts4script:
  - improve manifest.json defaults
  - add install/runtime guidance in README
- package:
  - convert template placeholder text into scoped packaging steps
  - reference tdesc and signing workflow in README

Deliverable: every `new` or `wizard` output is closer to runnable input for Sims 4 Studio/s4pe.

## Phase 3 — CLI documentation and content completeness

Tasks:
- Update docs to match actual command behavior.
- Add concise mod-authoring guidance:
  - what each kind should look like after generation
  - recommended post-generation workflow: tune-ids, validation, build, package, install, test
- Tune-ids docs should mention expected reports/artifacts.

Deliverable: end-user docs are accurate and minimize guesswork after scaffold generation.

## Phase 4 — Release/packaging workflow hardening

Tasks:
- Build release notes from CHANGELOG.md when packaging.
- Stopgap for release manifest: generate `tmp/release_manifest.txt` from built archive contents.
- Ensure build/package output paths are deterministic and documented.

Deliverable: release-like creation is repeatable and auditable.

## Phase 5 — TUI and shell polish

Tasks:
- Add one non-interactive smoke test for `tui` launch.
- Ensure command palette actions remain complete after refactors.
- Do not introduce heavy test flakiness.

Deliverable: the dashboard path is covered and not a mystery during tight edits.

## Verification contract

After every phase:
- run `python s4chemist_cli.py --help`
- run smoke: init → new kinds → validate --strict → build → package -> pipeline
- keep README/docs/help messages aligned with real behavior

## Success metrics

1. `validate` catches more than XML declaration/tag presence.
2. Every supported kind can be scaffolded and packaged in under 10 CLI commands.
3. Windows smoke test plus pytest both pass without secrets or network.
4. Docs can be followed literally without invented commands.
