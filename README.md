# The Evil Within — command console notes

Working notes for the retail Windows build
(`EvilWithin.exe`, build `May 10 2023`, id Tech 5 "Zwei"). All addresses are
module-relative or `0x140000000`-based VAs and hold across the retail installs
I compared (identical layout).

Layout: this top level holds the lookup/reference documents; the longer
task-specific notes live in [`notes/`](notes/), and runnable tools in
[`scripts/`](scripts/).

## Top level

| Doc | What it is | Read it when… |
|---|---|---|
| [`console_cmds.md`](console_cmds.md) | All 494 console commands — 188 functional, 10 no-op stubs, 296 removed-in-retail stubs — with handler addresses, syntax and the decl catalogue | you want to know whether a command exists, what its arguments are, or why it only prints a removal notice |
| [`cvar_flags_and_gates.md`](cvar_flags_and_gates.md) | CVar flag-bit decode, the runtime `set` gate (production/`0x10`), and the recipes for making a gated cvar settable | a `set` silently does nothing, you see unexplained flag hex, or you need the `com_fixedTic` / game-time scaling findings |

## notes/

| Doc | What it is | Read it when… |
|---|---|---|
| [`notes/cvars.md`](notes/cvars.md) | All 3,326 cvars with defaults, declared flags (raw hex) and per-cvar reference counts | you want a cvar's name, default value, or whether anything in the game actually reads it |
| [`notes/layer_logging.md`](notes/layer_logging.md) (+ [`scripts/ew_layer_log.py`](scripts/ew_layer_log.py)) | Runtime patch that links the engine's disabled file logger back in, capturing the layer stream to `base\qconsole.log` | you need to record which layers activate/deactivate as a map streams |
| [`notes/nextmap.md`](notes/nextmap.md) | `nextmap` guide: jump to any chapter/section, inventory carried over | you want to practise a specific section without replaying the lead-up |

## Start here for common tasks

- **"My `set` did nothing"** → [`cvar_flags_and_gates.md`](cvar_flags_and_gates.md)
- **"How do I get to chapter X, section Y"** → [`notes/nextmap.md`](notes/nextmap.md)
- **"What does cvar Z do"** → [`notes/cvars.md`](notes/cvars.md), then [`cvar_flags_and_gates.md`](cvar_flags_and_gates.md) if it's flagged/gated
- **"Where did the console output go"** → [`notes/layer_logging.md`](notes/layer_logging.md)
