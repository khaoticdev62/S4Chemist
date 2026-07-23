# Mod authoring workflow

The recommended path from idea to installed mod, entirely inside S4Chemist.

## The golden path

```bash
s4chemist_cli init MyMod
s4chemist_cli config MyMod mod_name=NightShift creator=YourName
s4chemist_cli new MyMod <kind> <Name>        # or: wizard <kind> <Name>
s4chemist_cli tune-ids MyMod --flavor        # real ids + stopgap flavor text
s4chemist_cli validate MyMod --strict        # must end at 0 issues
s4chemist_cli build MyMod                    # dev zip (dist/)
s4chemist_cli package MyMod                  # release zip + manifest + notes
s4chemist_cli install MyMod                  # copy into Mods
```

At every step `s4chemist_cli pipeline MyMod` shows which phase you are in and what artifact
comes next.

## What each kind looks like after generation

Every `new`/`wizard`/`generate` produces:

- `src/xml_snippets/<Name>_<kind>/<Name>_<kind>.xml` — tuning XML with placeholder id
  `0x00000000` and example tags for that kind (see `TUNING_TAG_RULES` in docs/validation.md)
- `README.txt` beside it — tuning notes and next steps
- Script mods (`ts4script`) additionally get `main.py` + `manifest.json`
- Packages (`package`) get a `.package.template` stub to compile in Sims4Studio/s4pe

## Post-generation workflow per artifact

1. **Edit the XML** — real display text, icons, and kind-specific tags.
2. **Run `tune-ids`** — rewrites `0x00000000` to stable generated ids and drops STBL maps
   into `src/localization/stbl_<stem>.txt` (key=value lines). Re-running is idempotent.
3. **Run `validate --strict`** — catches missing declarations/tags, placeholder ids and
   flavor text, template config values, config schema errors, broken manifests, and
   malformed localization files.
4. **Build/package** — `build` for iteration, `package` for release (adds
   `tmp/release_manifest.txt` with the full archive listing and
   `dist/<mod>-release-notes-<stamp>.txt` from your latest CHANGELOG section).
5. **Install + playtest** — then `uninstall` to clean up.

## tune-ids artifacts

- Rewritten XML in place (stable ids derived from the file name)
- `src/localization/stbl_<stem>.txt` — string-key maps for localization
- `tmp/tune_ids_report.txt` — what the pipeline tracker watches for
