# Packaging & Distribution

This release layout is designed for zip distribution and Mods-folder installs.

DISTRIBUTION FILES
- C:\Users\thecr\sims4-mod-cli\s4mod_cli.py
- C:\Users\thecr\sims4-mod-cli\OWNERS-GUIDE.txt
- C:\Users\thecr\sims4-mod-cli\docs\sims4-mod-types.md

RELEASE ZIP CONTENTS
- s4mod_cli.py
- OWNERS-GUIDE.txt
- docs/sims4-mod-types.md

CREATE RELEASE ZIP
1. Open terminal in C:\Users\thecr\sims4-mod-cli
2. Run: python "$SK" build
3. Zip the dist/ output or use package_release() for a release-named archive.

INSTALL FOR USERS
1. Python 3.10 or later
2. Extract release zip
3. Run: python s4mod_cli.py --help

MODS INSTALL
- python "$SK" install <project>
- This copies project files to Documents\Electronic Arts\The Sims 4\Mods\<project>
- dist/ and tmp/ are removed before copy

VERSIONING
- Use s4modconfig.yaml mod_name and version fields
- Build stamps use YYYYMMDD-HHMMSS
