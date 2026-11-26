# CVar flag bits, the production gate, and how to actually set a cvar

Companion to `notes/cvars.md` and `notes/layer_logging.md`. This documents the *flag system*
behind the "set does nothing" behaviour, decoded from the retail binary.

| | |
|---|---|
| Target | `EvilWithin.exe` in the game's install folder (verified identical layout across two local installs of the same build) |
| Binary | SHA-256 `6310988039db58fc27dca9c8e6ac00cb45c898da38bfccbb00898fa56dd414db`, build string `The Evil Within-Retail(NextGen-PC-D3D) May 10 2023 15:53:00`, PDB reference `Zweid3d64_NGShippingRetail.pdb` |
| Method | Ghidra via REA (static analysis; no PDB available, all names are reconstructed) |

## CVar object layout (idCVar, tech5)

Offsets below are from the cvar object base (the first argument of every
registration call, e.g. `FUN_141434f20` for `com_fixedTic`):

| Offset | Field |
|---|---|
| `+0x08` | current value (string) |
| `+0x28` | current value (int) — this is what code reads at runtime; see `notes/layer_logging.md` |
| `+0x30` | name string ptr |
| `+0x38` | default value string ptr |
| `+0x40` | description string ptr |
| `+0x48` | **flags dword** (what the `set` handler checks) |
| `+0x4c` | int init value |
| `+0x50` | float init value |

## How declared flags become runtime flags

The registrar `FUN_140d495c0` → `FUN_140d4aab0` normalizes the declared flag
number (the hex column in `notes/cvars.md`) before storing it at `+0x48`:

```c
if ((declaredFlags & 0x1C010) == 0)
    flags |= 0x8;                     // 0x1C010 = 0x10000 | 0x8000 | 0x4000 | 0x10
else
    flags = (flags & ~0x8) | 0x10;    // engine-native "console settable"
```

So a cvar declared `0x1`, `0x2` or `0x4` ends up with **bit 3 (`0x8`) set and bit
4 (`0x10`) clear** — not settable. A cvar whose declared flags already include
`0x10` (or the `0x4000`/`0x8000`/`0x10000` special bits) keeps `0x10` — settable.

Later, static registration (`idCVar::RegisterStaticVars`) adds **bit `0x20000`**.
Example: `com_fixedTic` declared `0x1` → runtime flags `1 | 0x8 | 0x20000`
= **`0x20009` = 131081** (read in memory, confirmed).

## The `set` gate (`set` handler `FUN_140d4d320`, cvar-command path `FUN_140d4a150`)

Checked in order against flags at `+0x48`:

1. bit `0x4000` set → prints `%s can only be set on the command line`, refuses
2. bit `0x8000` set → prints `%s is read only`, refuses
3. **`production < 4` (retail: production = 3) and flag `0x10` not set → returns silently, no message**

This is why `set com_fixedTic 1` looks like it worked and does nothing. It also
explains the repeated retries visible in `base/consoleHistory.txt` (`seta`,
`=`, quoting…) — those forms go through the same gated handler.

A bare cvar name (no arguments) is a **query** and is *not* gated: it prints
`"<name>" is:"<value>" default:"<default>"`. Use it to confirm whether a `set`
actually took.

## Recipe: make a gated cvar console-settable

Patch the flags dword (add `0x10`, drop `0x8`) so the cvar looks like the
engine-native settable shape. Module-relative, type 4-byte dword:

| CVar | Object RVA | Flags dword RVA | Runtime value | Write |
|---|---|---|---|---|
| `com_fixedTic` | `0x2258460` | `0x22584A8` | `0x20009` (131081) | `0x20010` (131088) |
| `com_maxTicScale` | `0x22584E0` | `0x2258528` | `0x2000C` (131084) | `0x20010` (131088) |
| `g_enableGameTimeScaling` | `0x2893A20` | `0x2893A68` | `0x20009` (131081) | `0x20010` (131088) |

Then `set <cvar> <value>` goes through the engine's own setter. Minimal-change
alternative: only add `0x10` (e.g. `0x20019`) — the gate only checks bit `0x10`,
but leaves the `0x8` bit in place.

Caveats:

- **Per session**: the patch is memory-only, re-apply after every game restart.
- **Cheat reset**: the engine has a `Resetting cheat cvar: %s` pass
  (`FUN_140d4bbe0`); if a set value snaps back after a map load, re-apply the
  *value* after the map is up.
- Direct value write at `cvar+0x28` (the `notes/layer_logging.md` technique) also
  works and needs no flags patch; the flags patch is nicer for repeated `set`
  during testing.

## `com_fixedTic` is the demo fixed-timestep switch

Its only direct consumers in the whole binary are `Common::RecordPlayback`'s
record and playback functions (`FUN_140040530` / `FUN_140040a20`), which set it
to `1` while a demo runs and back to `0` after. While it is on, the game
advances a fixed chunk of simulation time per rendered frame (one nominal
60 Hz-class tic per frame), so **the whole game runs at ≈ fps/60 × real speed**
— 120 fps → 2×, 240 fps → 4× ("comically fast" is expected, not a bug).

That is direct evidence for the simulation being per-rendered-frame under the
hood: the default path (`com_fixedTic 0`) re-times game time to real time via
the `g_enableGameTimeScaling` / `com_maxTicScale` system, but per-frame logic
(AI state updates) still gets more updates per real second at higher fps.

`com_maxTicScale` (default `2.f`) is a *slow-frame* guard only: it caps how many
nominal tics one long frame may advance. At 120 fps each frame contributes 0.5
tics, so lowering it to `1` changes nothing above ~30 fps.

## Related: chapter 1 Sadist chase framerate dependence

Observed at runtime (this machine): at 30 fps the corridor-chase Sadist never
catches a player who keeps moving; at 60+ fps he sometimes does; at 120 fps his
stride/approach appears longer and he sidesteps without provocation. A/B test
with `set g_enableGameTimeScaling 0` (after the flags patch above) showed **no
difference** — consistent with the chase movement being per-rendered-frame and
not covered by the game-time scaling layer. `AI_STATE_MODE_B_SIDESTEP` /
`AI_STATE_EVADE_TRAP` / `PARRY_PROJECTILE` states (state-name table base
`0x141F26600`, `AI_STATE_MODE_B_CHASE` = index 27) explain the bottle-sidestep
behaviour. Practical equalizer: cap fps at 60.

## Key addresses (same layout in both installs)

| What | Address |
|---|---|
| cvar registrar | `FUN_140d495c0` → `FUN_140d4aab0` |
| `set`/`seta` handler (gated) | `FUN_140d4d320` |
| cvar-as-command handler (gated) | `FUN_140d4a150` |
| cheat-cvar reset pass | `FUN_140d4bbe0` |
| `SetGameTimeManagerHz` stub | `FUN_1400455d0` → prints removal notice |
| `Common::Record` / `Playback` (com_fixedTic users) | `FUN_140040530` / `FUN_140040a20` |
| AI state-name table base | `0x141F26600` |
| `"%s is read only\n"` / `"%s can only be set on the command line\n"` | `0x1417B38D0` / `0x1417B38A8` |
| `Resetting cheat cvar: %s\n` | `0x1417B3938` |
