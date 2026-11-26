# Capturing the layer stream to a file

The game tells you which layers it activates and deactivates, but only through
`idLib::Printf`. In the retail build that text goes to the on-screen console and nowhere
else: there is no `con_logfile`, `conDump` is one of the 296 commands removed in shipping,
and the engine's own file logger is constructed but never plugged in. This page explains
why, and gives you a tool that turns the stream into a text file you can read afterwards.

---

## Quick start

```
:: 1. start the game and load the chapter/section you want to record
:: 2. from a normal command prompt, in the install folder:
::    (<repo> = wherever you cloned this notes repo)
python <repo>\scripts\ew_layer_log.py

:: 3. in the in-game console type anything, e.g.
g_debugLayers

:: 4. play through the part you want to record, then read
type base\qconsole.log
```

To check what the tool sees without changing anything:

```
python <repo>\scripts\ew_layer_log.py --check
```

To put everything back:

```
python <repo>\scripts\ew_layer_log.py --undo
```

---

## Why the built-in logger does nothing

`idCommonLocal` owns an `idLogFileWriter` at `EvilWithin.exe+0x2258C68` (it is the
sub-object at `idCommonLocal+8`, the singleton being `+0x2258C60`). Its constructor
(`0x140039CF0`) installs the vtable `0x141552188` and then **zeroes the enabled byte** at
`+0x10`.

The engine's print path walks a singly linked list of listeners whose head is
`+0x9C9D2A8`:

```
for (l = head; l; l = l->next)
    if (l->enabled && level >= l->threshold)
        l->Print(level, text);
```

`RegisterPrintListener` is `0x140D47F00`. A direct-call scan of `.text` finds **exactly
one caller**: `idConsoleLocal::Init` at `0x140065C6D`, which registers the console sink
(`idConsoleLocal+8`, vtable `0x14155B568`). Nothing ever registers the log writer, so:

- `logFile` (default `1`), `logFile_SystemRunning` (default `1`) and
  `logFileName` (default `qconsole.log`) are all set correctly and all useless.
- `qconsole.log` is never created, no matter what you type in the console.
- The writer's `Close` still runs at shutdown (`idCommonLocal::Shutdown`,
  `0x140041B89`) but there is no open file to archive.

The fix is not a cvar. It is to link the existing writer into the list at runtime.

## Dumping layer names

`--dump-layers` reads the live `idGameLocal` layer registry (`gameLocal+0x318`, entry
stride `0xA8`, name pointer at `+0x08`) and prints the names plus a quoted list:

```
python <repo>\scripts\ew_layer_log.py --dump-layers
python <repo>\scripts\ew_layer_log.py --dump-layers --prefix st12
```

The registry **accumulates** names as layers are activated; it is not a manifest of the
whole map. A live test at the chapter-6 start showed only the six start layers
(`mapcontrol/saveroom_control/...`, `mapcontrol/fort/...`). So after you have streamed a
section, `--dump-layers` lists every layer that section has touched — useful, but it is
not a way to learn a section you have never loaded. For a section you have not visited,
capture the transitions with the logger (or read a save made there).

Feed an accumulated list to `nextmap` if you want to re-load that state:

```
nextmap root/chapter/Losing_Grip_on_Ourselves player_start "<the quoted list>" 0
teleportCam <x> <y> <z> <yaw> <pitch>
```

## Dumping the entities that exist right now

```
python <repo>\scripts\ew_layer_log.py --dump-entities
python <repo>\scripts\ew_layer_log.py --dump-entities --prefix trigger
python <repo>\scripts\ew_layer_log.py --dump-entities --prefix sroom
```

This reads `idGameLocal`'s entity array (`gameLocal+0x68` → manager, pointers at
`+0x28`, name at `entity+0x08`) and prints the entities that currently exist. The list
grows as the map streams, so:

1. at the chapter start, find the trigger/event entity in the current section and
   `trigger <name>`;
2. dump again — the entities for the newly streamed section are now present;
3. find the checkpoint/save entity, then `teleport <name>` to it.

Note: `writeEntitiesFile` is in the command table but **cannot work in retail** — it
appends `.map` and runs the text-map lexer, and the shipped game has no `.map` source
(it prints `Could not load maps/root/chapter/...`).

## What the tool writes

| What | Address (RVA) | Value |
|---|---|---|
| list head | `0x09C9D2A8` | `writer` |
| writer `next` | `0x02258C70` | old head (the console sink) |
| writer `enabled` | `0x02258C78` | `1` |
| writer `threshold` | `0x02258C7C` | `1` |
| `logFile` | `0x0226BF78` | `2` (write **and flush** every line) |
| `logFile_SystemRunning` | `0x0226BFF8` | `1` |
| `g_debugLayers` | `0x09C5BD18` | `1` |

`next` is written before `head`, so a print racing the patch still sees a valid chain.

`g_debugLayers` is written directly because the console `set` path is gated in retail:
`Cvar_SetValue` returns silently when `production < 4` and the cvar does not carry flag
`0x10`; `g_debugLayers` carries `0x2`, and production is `3`. Typing `set g_debugLayers 1`
therefore looks like it worked (the `toggle` echo prints first) but changes nothing. The
layer code reads the integer at cvar `+0x28`, which is exactly `0x09C5BD18`.

The complete flag/gate decode — the registrar's flag normalization, the runtime
flag layout, and the alternative recipe that patches the flags dword so console
`set` works normally — is in `../cvar_flags_and_gates.md`.

## What it does to the log level

The layer prints are guarded by the cvar value, not by a build flag:

```
level = (g_debugLayers >= 1) ? 1 : 0;
idLib::Printf(level, "%d: layer '%s' activated\n", ...);
```

`idLib::Printf(level, ...)` at `0x140D47ED0` returns immediately when `level == 0`, so
with `g_debugLayers` at `0` nothing is printed at all. With it at `1` the writer's
threshold (`1`) is satisfied and the line reaches the file.

## The three messages

| Call site | Format string | Name register |
|---|---|---|
| `0x140974ADF` | `"%d: layer '%s' activated\n"` | `r9` (layer name) |
| `0x14097612C` | `"%d: layer '%s' deactivated\n"` | `r9` (layer name) |
| `0x140C7AEE5` | `"%d: '%s' changing layers:\n"` | `r9` (entity name) |

The `changing layers:` line is a header emitted by a layer-jump volume; the `%s` is the
volume's own name. The `activated` / `deactivated` lines after it are the layers that
volume switches on and off. That is the volume's list, not a dump of everything that is
currently active: layers it does not mention are left alone. So the trace tells you
**what changed and which volume changed it** — which is what you need to find a section
boundary.

The authoritative full active set for a point in the map is what a save made there records
in `inventory.zwei` (map, spawn, then every active layer), and that is exactly the list
`nextmap` takes. If you can save at the section, read it there. If you cannot, replay the
trace from the chapter-start set.

---

## Chapter 6 capture procedure

Chapter 6 is one map (`root/chapter/Losing_Grip_on_Ourselves`); its "sections" are layers
swapped by `dev/volume/layer_jump` entities. There are 18 of them in the package:

```
p03asrmst_dev_volume_layer_jump_1
st12_gd_dev_dev_volume_layer_jump_1 .. _7
st21_gd_dev_dev_volume_layer_jump_1 .. _10
```

1. Load `SLOT5` (the chapter-6 chapter start) or start it with
   `nextmap root/chapter/Losing_Grip_on_Ourselves player_start "" 0`.
2. Run `python <repo>\scripts\ew_layer_log.py`.
3. Type `g_debugLayers` in the console, or simply walk through the first layer-jump
   volume. The first level-1 print creates `base\qconsole.log` (its first line is the
   writer's own `log file '...' opened on ...` notice). If no file appears after a layer
   transition, stop and run `--check`.
4. Walk the route. Each layer-jump volume prints a `changing layers:` block naming the
   volume and the layers it turns on/off.
5. At the section you want, get the full active list in one of two ways:
   - **Save there** (manual save or quicksave) and read `inventory.zwei`; it stores the
     map, the spawn, then every active layer name as plain ASCII. This is the
     authoritative list.
   - **Use the trace**: take the chapter-start set and apply each `activated` /
     `deactivated` line in order. This works without saving but is easy to get wrong if
     you miss a line.
   
   Also run `where` there to record the position for `teleportCam`.
6. Build the jump:

   ```
   nextmap root/chapter/Losing_Grip_on_Ourselves player_start "<layer> <layer> ..." 0
   teleportCam <x> <y> <z> <yaw> <pitch>
   ```

`player_start` is the chapter-start spawn recorded by the game itself in
`SLOT5\inventory.zwei`. Do **not** use `lgo_pl_start`: that entity exists and `teleport`
will accept it, but it places you in the void. Checkpoint entities
(`phase00_checkpoint_2` .. `_6`, `phase01_checkpoint_7_joseph`,
`phase01_update_giant_village_checkpoint`) are save triggers, not spawn points, and are
layer-gated, so `teleport` reports "entity not found" for them until their layer is live.

### Using the result

For a post-event area there is usually no checkpoint to teleport to, so place yourself by
coordinate instead. `where` prints the current view position and angles; `teleportCam`
takes `x y z yaw pitch`:

```
nextmap root/chapter/Losing_Grip_on_Ourselves player_start "<layer> <layer> ..." 0
teleportCam <x> <y> <z> <yaw> <pitch>
```

A wrong layer list still loads the map but leaves you in the void (or at a position with
no geometry), so check the view after the jump.

If a checkpoint *does* exist in the section, `teleport phase00_checkpoint_N` is a useful
oracle: `entity not found` means its layer is not active, i.e. the list is wrong.

`nextmap` restores geometry and layers only. Enemies, script variables, one-time triggers
and puzzle flags are not restored, so treat a jumped-to section as a sandbox, not a valid
run.

---

## Caveats

- **The file lives at `base\qconsole.log` while the game runs.** On a clean exit the
  writer's `Close` renames it under `../logs/` (i.e. `<install>\logs\qconsole.log`).
  Copy it before quitting if you care about the tail.
- **ASLR is on.** Every address in the tool is an RVA and the module base is looked up
  fresh each run, so it survives restarts. Do not hard-code absolute addresses.
- **The tool needs to open the process.** If the game runs elevated, run the script from
  an elevated prompt. If more than one `EvilWithin.exe` exists, pass `--pid`.
- **Antivirus / AMSI.** The script calls `ReadProcessMemory` / `WriteProcessMemory`.
  Some endpoint tools flag that pattern. The writes are seven values in the game's own
  data section; there is no code injection and no executable memory is touched.
- **`--undo` is optional.** The patch disappears when the process exits. `--undo` exists
  for the case where you want the console-only behaviour back without restarting.
- **Do not raise the production global.** Writing `4` to `+0x9C9EE40` unlocks `set` for
  dev cvars but destabilises the game; the direct `+0x28` write used here avoids it.
- **There is no force-all-layers switch in this build.** The string
  `layer_forceAllMapLayersToLoad` is registered as a cvar, but it has exactly one
  reference in the whole binary — its own registration. Nothing reads it, so setting it
  (even by direct memory write) does nothing.

## Verifying the patch by hand (Cheat Engine)

If you prefer to do it manually, these are the same writes in CE terms. Attach to
`EvilWithin.exe`, then in the memory viewer (all addresses are `module base + RVA`):

```
[EvilWithin.exe+9C9D2A8]   -> pointer to the console listener (sanity check)
[EvilWithin.exe+2258C68]   -> 0x...1552188  (idLogFileWriter vtable, sanity check)

[EvilWithin.exe+226BF78]   -> 2            (logFile: on + flush)
[EvilWithin.exe+226BFF8]   -> 1            (logFile_SystemRunning)
[EvilWithin.exe+2258C78]   -> 1            (writer enabled byte)
[EvilWithin.exe+2258C7C]   -> 1            (writer threshold)
[EvilWithin.exe+2258C70]   -> old head     (writer.next)
[EvilWithin.exe+9C9D2A8]   -> writer addr  (list head)
[EvilWithin.exe+9C5BD18]   -> 1            (g_debugLayers)
```

Order matters only for the last three: set `next`, then `head`, then `g_debugLayers`.
