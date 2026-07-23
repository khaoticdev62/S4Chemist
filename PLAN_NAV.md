# S4Chemist Navigation Flow Refinement Plan

## Research Baseline

Current navigation surfaces:
- Bare TTY launch: questionary menu shell with arrow-key choices
- REPL entry: "Type a command..." from menu shell, prompt_toolkit history/completion
- Dashboard: Textual TUI with sidebar buttons, 4 tabs, command palette
- Direct CLI: s4chemist_cl.py <command> [args]
- Help: --help, help <cmd>

Observed pain points from code and docs:
- Three overlapping entry points with duplicated command discovery
- Menu shell asks for path and flags manually even for common workflows
- TUI sidebar is command-centric, not task-centric; project path is separate from actions
- No onboarding graph: new user must guess the sequence
- Pipeline status is inspect-only; next action is buried in command output
- Files tab is raw tree; preview is manual and not tied to validation/build actions
- generate and wizard overlap in both TUI and CLI help
- No single-source truth for command metadata and quick actions
- Windows console path/typing friction is not considered in interactive prompts

## Design Principles

1. One obvious entry point, not three competing ones
2. Task-first, not command-first: surface what to do next, not just raw commands
3. Command palette / menu / help all derive from one registry
4. Progressive disclosure: new users see guided flow, power users get fast CLI
5. State-aware UI: show pipeline-aware suggestions instead of ambient buttons
6. Minimal typing: project path should persist in session/navigation state
7. Platform-aware defaults: reduce interactive-friction on Windows

## Proposed Flow

### Top-Level Entry Model

Replace 3-surface sprawl with a single layered entry model:

Layer 1 - Quick Start / Guided Run:
  s4chemist_cli
    -> shows 4 task cards, not command table:
      1. Create / scaffold mod
      2. Validate & fix
      3. Build / package
      4. Pipeline status

Layer 2 - Contextual Quick Commands:
  Each card collects minimal required args:
    - project path persisted within the launcher session
    - kind/name collected via minimal select/text with smart defaults
    - optional params exposed through one expanded question

Layer 3 - Direct / Power:
  s4chemist_cli <command> [path] |
  s4chemist_cli tui [path] |
  /command palette in dashboard

### Command Model

Unify command metadata and action routing:

- Keep COMMANDS registry as single source of truth
- Add action categories per command:
  - create: init, new, generate, wizard
  - inspect: validate, pipeline, doctor
  - ship: build, package, install, changelog
  - repair: tune-ids
- Render menus, help, and TUI palette from category tags
- TUI action buttons should map to category workflows, not individual commands

### Bare Launch UX

Current: list of every command in table form
New: 4 task cards + 1 quick help footer

Card 1 - Create:
  Mod type: [Select]
  Name:      [Input]
  [Create]   [Advanced: --param form]
  Fallback:  command=new|wizard|generate

Card 2 - Validate:
  Path: [Input, default detected or last project]
  [Validate]  [Strict toggle]
  Fallback:   command=validate

Card 3 - Ship:
  Path: [Input]
  [Build]  [Package]  [Install]
  Fallback: command=build|package|install

Card 4 - Pipeline:
  [Status] [Next Actions] [Unlock] [Reset]
  Fallback: command=pipeline*

Footer:
  Type a command... -> drops into REPL
  Ctrl+P / /palette -> all commands
  tui -> dashboard

### TUI Redesign

Current layout issue: sidebar commands + 4 tabs is redundant.

Proposed tabs:
1. Workflow: phase-aware step wizard
   - Current phase from .s4modstate
   - One primary action for that phase
   - Secondary actions for adjacent phases
   - Example:
     Concept    -> Write notes, open editor placeholder
     Requirements -> Write requirements.md
     Proof      -> Scaffold snippet/script
     Tuning     -> tune-ids, param editor
     Impl       -> Validate, Build
     Validation -> Fix issues
     Local Test -> Install, launch helper notes
     Packaging  -> package release
     Distribution -> changelog, install notes

2. Create:
   - Replace separate generate and wizard with one unified form
   - Type select + name + dynamic params from WIZARD_PRESETS
   - One Create button that always uses wizard semantics
   - Remove redundant Generate section from sidebar

3. Files:
   - Keep tree + preview
   - Add file-level actions based on file kind:
     XML -> validate quick check
     ZIP -> archive stats
     Markdown/Text -> preview enhanced
   - Show dod/untracked badge if dist/tmp/.git exist

4. Log:
   - Keep current behavior
   - Add rerun / copy command line action per log entry

Sidebar replacement:
- Project path with quick init/open
- Workflow quick-jump to current phase
- Doctor / env check
- Command palette hint

Command palette additions:
- Navigate to next action
- Go to current phase in Workflow tab
- Run validate + auto-fix hints
- Toggle project path

### Menu Shell and REPL Simplification

Menu shell:
Current: everything in one long list
New: task groups with one recommended default each

Task groups:
- Create / scaffold
- Validate / test
- Build / package / install
- Pipeline / tune
- Environment / doctor
- TUI / dashboard
- Type command...

Interactive shell:
- Startup banner should recommend 1-2 next actions based on cwd/.s4modstate presence
- Tab completion should include:
  concrete commands
  project aliases if known
  quick actions: validate --strict, build --release, tune-ids, pipeline next

### Windows Simplifications

- Detect and default project path to common Mod authoring locations:
  Documents/Electronic Arts/The Sims 4/Mods
  current working directory if it looks like a project
- Use console-friendly default widths and avoid long menu lists
- TUI Linux-first behavior must not break on Windows; simplify keyboard hints

## Implementation Plan

### Phase 1 - Registry Simplification
Task:refactor command/menu metadata without behavior changes
- Add command categories to Command dataclass
- Render help/menu/palette from category metadata
- Preserve all existing argv dispatch paths

Task:TUI category-based sidebar replacement
- Replace per-command buttons with workflow-aware actions
- Unify creation into one Create tab form

Task:Remove duplicate generate/wizard UI divergence
- Wizard form drives both wizard and generate semantics
- Keep CLI generate command for backward compatibility

### Phase 2 - Guided Launch UX
Task:Replace bare launch with task cards
- Add _guided_launch() questionary flow
- Keep REPL fallback and --help behavior identical

Task:Add project-persistent session state in menu shell
- Remember last project path in menu session
- Prepopulate project input across card prompts

### Phase 3 - Pipeline-Aware Navigation
Task:Add next-action derivation to menu/TUI
- Menu shell shows recommended first action when cwd has no .s4modstate
- TUI Workflow tab drives actions from PIPELINE_META

Task:Expose one-click phase transitions
- Pipeline tab buttons match current phase, not all commands

### Phase 4 - Windows Onboarding Defaults
Task:Auto-detect project and Mods directories
- Menu shell and TUI project input default smarter
- Doctor summary becomes part of guided launch when missing

### Phase 5 - Verification and Rollout
Task:Add navigation regression tests
- menu_shell flow coverage via injectable select
- REPL banner recommendation tests
- TUI tab presence tests using Textual testing harness or launch smoke test
- Help and command palette coverage

Task:Smoke matrix
- python s4chemist_cli.py
- python s4chemist_cli.py tui
- python s4chemist_cli.py --help
- windows console questionary path

## Success Criteria

1. New user can scaffold a mod in 3 screen taps or fewer
2. Launch, validate, build, package sequence is visible from CLI/TUI without reading docs
3. Every action is reachable from command palette / REPL completion / REGISTRY
4. No surface duplicates more than one command map
5. Windows and POSIX launch paths both pass without environment tweaks
