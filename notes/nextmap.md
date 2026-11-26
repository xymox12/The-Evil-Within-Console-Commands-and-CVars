# The Evil Within — `nextmap` guide

Jump straight into a chapter, or into a specific part of one, without replaying the
lead-up. This is the most useful command for practising a section repeatedly.

## What it does

`nextmap` performs a normal map transition: the game saves your current loadout,
unloads the current map, loads the target map, and places you at a named spawn point.
Because it goes through the same path the game uses between chapters, **your inventory,
weapons, upgrades and ammo carry over**.

It is not a teleport inside the current level — it is a full reload with a loading
screen. That is what makes it reliable for jumping to a section: you arrive in the same
state a checkpoint load would give you.

## Syntax

```
nextmap <mapname> <spawnspot> <addWorldSpawnLayersFromNextMapIfFirstTime> <worldIndex>
```

All **four** arguments are required. If you leave any out, the command prints its
syntax line and does nothing.

| # | Argument | Meaning | Typical value |
|---|---|---|---|
| 1 | `mapname` | Map to load, as a path without `maps/` and without `.sbsp`. | `root/chapter/the_keeper` |
| 2 | `spawnspot` | Name of the spawn point to appear at inside that map. | `player_start` |
| 3 | `addWorldSpawnLayers...` | Despite the name, this becomes the map-start **active layer list** (`layersActive`). Pass the layer names for the area you are loading, space-separated, in quotes. | `"mapcontrol/fort/transition"` or a quoted list |
| 4 | `worldIndex` | Which world inside the map to start. Every story chapter uses `0`. | `0` |

Notes:

- `mapname` is the full internal name, e.g. `root/chapter/an_emergency_call`. Just
  `an_emergency_call` will not resolve.
- `spawnspot` is the **targetname of an `idPlayerStart` entity**, not a menu label. The
  generic one at the start of every map is `player_start`.
- There is no requirement that the target be a *different* map. Passing the current map
  and a different spawn spot is the normal way to skip forward inside a chapter.
- **Do not pass `0` for the third argument.** It is not a boolean. A value of `0` is
  stored as a single active layer called `0`, which does not exist, so the map loads with
  no geometry and no entities — a black void. The layer list has to come from the target
  area; a save made in that area stores the exact list (see below).

## Map names

Story chapters:

| Map name | Internal map ID | Package |
|---|---:|---|
| `root/chapter/an_emergency_call` | 1 | `an_emergency_call` |
| `root/chapter/remnants` | 2 | `remnants` |
| `root/chapter/claws_of_the_horde` | 3 | `claws_of_the_horde` |
| `root/chapter/inner_recesses` | 4 / 5 | `inner_recesses` |
| `root/chapter/losing_grip_on_ourselves` | 6 | `losing_grip_on_ourselves` |
| `root/chapter/the_keeper` | 7 | `the_keeper` |
| `root/chapter/a_planted_seed_will_grow` | 8 | `a_planted_seed_will_grow` |
| `root/chapter/the_cruelest_intentions` | 9 | `the_cruelest_intentions` |
| `root/chapter/casualties` | — | `casualties` |
| `root/chapter/reunion` | 11 | `reunion` |
| `root/chapter/the_ride` | 12 | `the_ride` |
| `root/chapter/the_craftsmans_tools` | — | `the_craftsmans_tools` |
| `root/chapter/ulterior_motives` | 14 | `ulterior_motives` |
| `root/chapter/an_evil_within` | 15 | `an_evil_within` |

The map ID is the number the game stores in a save (`game.details`). `inner_recesses`
covers both of the two chapters that use that map.

DLC:

| Map name |
|---|
| `root_dlc1/ch1/dlc1_chapter1` |
| `root_dlc1/ch2/dlc1_chapter2` |
| `root_dlc2/ch3/dlc2_chapter3` |
| `root_dlc2/ch4/dlc2_chapter4` |
| `root_dlc_box_2/stage0/dlc_box_stage_0_main` |

Other maps that exist but are not story levels:

```
root/title/title
root/title/modelviewer
root_dlc2/title/modelviewer_dlc2
root_dlc_box_2/title/title_dlc3
```

## Finding spawn spots

Every map has at least `player_start`. Named spawn spots are used by the game for
checkpoints and restarts, and their names are usually descriptive
(`..._player_start_3`, `..._player_start_boss_restart`, ...).

Four ways to find them:

1. **Use the list in the appendix below**, collected from the shipped game data.

2. **Look at your own saves.** Each save folder contains a `mapstart.zwei` with the map
   name and the spawn spot the game used. For example:

   ```
   root/chapter/inner_recesses
   st06_asylummain_player_start_chapter4_division
   ```

   That second string is a valid `spawnspot` argument. Make a save at the section you
   want, quit, then read the name — it is the exact one the game uses for that checkpoint.

3. **Probe the current map with `teleport`.** While you are already inside the map, the
   entity names from the appendix (and the map's string data) can be tested directly:

   ```
   teleport lgo_pl_start
   teleport phase00_checkpoint_3
   ```

   `teleport` needs a live entity with that targetname; it jumps you there instantly
   without a map reload. If the name is wrong it prints an error and nothing happens.

4. **`writeEntitiesFile` — developer builds only.** Retail ships the compiled `.sbsp`
   only, while this command parses the editable `.map` source and appends `.map` to the
   name. In this build it therefore always prints:

   ```
   Could not load root/chapter/<map>
   ```

   It only works if the map sources are present (a development install), so it cannot be
   used here.

## Layers (the third argument)

This is the part that catches everyone out. The third argument is stored in the map-start
structure's `layersActive` field. It is a **space-separated list of layer names**, not a
boolean.

- Passing `0` does not mean "off". It asks for a layer literally named `0`, which does
  not exist, so the map loads with no geometry or entities: a black void.
- A save made in the area you want stores the exact layer list. For a checkpoint save it
  is in `inventory.zwei` (after the map name and checkpoint name); for a chapter start it
  is in `mapstart.zwei`. The layer paths appear as plain text, for example:

  ```
  mapcontrol/saveroom_control/saveroom_operation
  mapcontrol/saveroom_control/saveroom_base
  mapcontrol/fort/transition
  mapcontrol/fort/fort_market_stationed
  ```

- Pass them as one quoted, space-separated argument:

  ```
  nextmap root/chapter/Losing_Grip_on_Ourselves player_start "mapcontrol/saveroom_control/saveroom_operation mapcontrol/saveroom_control/saveroom_base mapcontrol/fort/transition mapcontrol/fort/fort_market_stationed" 0
  ```

- For a map or area that uses the normal starting layers, try an empty quoted argument
  first:

  ```
  nextmap root/chapter/remnants player_start "" 0
  ```

If the third argument is wrong you still load the map, but you get the void — the loading
screen completes and there is nothing around you. That is the signature of a bad layer
list, not a bad map name.

### The layer list is the section selector

A story chapter is one map. Its sections — the parts the game streams in as you walk —
are not separate maps and have no separate index: a section *is* the set of layers that
is active there. So the third argument is the only thing that chooses a section.

If you have a save in the section, read the list from its `inventory.zwei`. If you do not,
record the transitions: `<repo>/notes/layer_logging.md` turns the engine's layer
messages into `base\qconsole.log`. The `changing layers:` line names the layer-jump
volume and the lines under it show which layers it switched; a save made at the section
still gives the authoritative full list.

### Worked example: chapter 6 cabin-night quicksave

`mapstart.zwei` is the **chapter-start** record: the map, the spawn used when restarting
the chapter, and the layers active at the start. It is not the checkpoint state. The
checkpoint name and the active layers at the moment of saving are stored in
`inventory.zwei`.

For the cabin quicksave:

- map: `root/chapter/Losing_Grip_on_Ourselves`
- checkpoint (from `inventory.zwei`): `phase00_checkpoint_3`
- layers (from `inventory.zwei`, count 5):

  ```
  mapcontrol/fort/fort_market_stationed
  mapcontrol/fort/fort_inside_a
  mapcontrol/fort/fort_inside_stationed
  mapcontrol/fort/switch_foglayer2
  mapcontrol/fort/fort_inside_b
  ```

So the jump is two commands — `nextmap` to load the layers, then `teleport` to the
checkpoint entity, which only exists once its layer is active:

```
nextmap root/chapter/Losing_Grip_on_Ourselves player_start "mapcontrol/fort/fort_market_stationed mapcontrol/fort/fort_inside_a mapcontrol/fort/fort_inside_stationed mapcontrol/fort/switch_foglayer2 mapcontrol/fort/fort_inside_b" 0
teleport phase00_checkpoint_3
```

The `teleport` doubles as the correctness check: `entity not found` means the layer list
is wrong. A checkpoint name is never a valid `nextmap` spawn — it is a save trigger with
no spawn transform.

The mapstart file for the same save says `player_start` with **zero** layers — that is
the chapter restart, not this checkpoint. Using those values drops you at the map start
(or into the void), not at the cabin.

### Chapter 6: the streamed sections

`root/chapter/Losing_Grip_on_Ourselves` is the whole chapter. Its sections are swapped by
18 `dev/volume/layer_jump` entities:

| Prefix | Volumes | Notes |
|---|---|---|
| `p03asrmst_...` | 1 | start / save-room area |
| `st12_gd_dev_dev_...` | 7 | first streamed block |
| `st21_gd_dev_dev_...` | 10 | second streamed block |

The chapter-start record (`SLOT5\inventory.zwei`) is `player_start` with **zero** layers,
so the chapter start is:

```
nextmap root/chapter/Losing_Grip_on_Ourselves player_start "" 0
```

`lgo_pl_start` is the other start-like entity in the package. It exists, so `teleport`
accepts it, but it drops you in the void — it is not the chapter start. The checkpoint
entities `phase00_checkpoint_2` .. `_6`, `phase01_checkpoint_7_joseph` and
`phase01_update_giant_village_checkpoint` are save triggers, not spawn points; they are
layer-gated, so `teleport` reports "entity not found" until their layer is live.

### Landing at a post-event area (no save point needed)

Areas that are streamed in by a script event usually have no checkpoint and no named
player start of their own. Two things get you there:

1. the **layer set**, so the geometry and entities exist;
2. a **position**, so you do not walk.

For the position, `where` (alias `getviewpos`) prints the current view position and
angles, and `teleportCam` sets them — neither needs an entity or a save point:

```
where
teleportCam <x> <y> <z> <yaw> <pitch>
```

`setviewpos <x> <y> <z> [yaw pitch]` also works. So the full jump is:

```
nextmap root/chapter/Losing_Grip_on_Ourselves player_start "<layer> <layer> ..." 0
teleportCam <x> <y> <z> <yaw> <pitch>
```

Capture the two values once, while standing in the area:

- **Layers:** quicksave there (a normal save, not the lantern save point) and read
  `inventory.zwei`. The active layer names are plain ASCII immediately after the map and
  spawn names. A real example from this install:

  ```
  root/chapter/Inner_Recesses
  st06_asylummain_player_start_8
  mapcontrol/village_mzone/rescue_joseph_02
  stage/st01e/gamedesign05_02
  ```

  Or run `<repo>/scripts/ew_layer_log.py` and read the transitions from
  `base\qconsole.log` (see `layer_logging.md`).
- **Position:** `where` prints it while you are standing there.

Caveat: `nextmap` restores geometry and layers only. The event script does not run, so
scripted enemies, doors and one-time triggers are missing. `trigger <entityname>` can
re-run a specific event after the layers are loaded if it does not depend on prior state.

### Finding the trigger and the coordinates without walking

`writeEntitiesFile` does **not** work in retail. It appends `.map` and runs a text-map
lexer, and the shipped game has no `.map` source, so it answers
`Could not load maps/root/chapter/...`. Use the live entity list instead.

The tool can dump the entities that exist in the current game state:

```
python <repo>\scripts\ew_layer_log.py --dump-entities
python <repo>\scripts\ew_layer_log.py --dump-entities --prefix trigger
python <repo>\scripts\ew_layer_log.py --dump-entities --prefix sroom
python <repo>\scripts\ew_layer_log.py --dump-entities --prefix checkpoint
```

It reads `idGameLocal`'s entity array directly. Use it to:

- find the trigger/event entity in the current section and fire it with
  `trigger <targetname>`;
- after that section loads, dump again and find the checkpoint or save entity that
  appeared;
- `teleport <name>` to it (and step back if you want to be just before it).

Chapter 6's early trigger/event entities are named like
`p03asrmst_gameplay_trigger_trigger_2..9`, `sroomtrstn_gameplay_trigger_trigger_*`,
`st12_gd_a01_gameplay_trigger_trigger_1..2`,
`st12_gd_a02_gameplay_trigger_trigger_1..13`, and the event managers
`078a_event_manager`, `12_gd_a02_gameplay_target_entity_event_manager_8`.

## Recipes

Start a chapter from the beginning:

```
nextmap root/chapter/remnants player_start "" 0
```

Jump to a specific part (same map, later spawn point):

```
nextmap root/chapter/the_keeper cata_gd_b1_player_start_3 "" 0
```

Resume the chapter-4/5 split point:

```
nextmap root/chapter/inner_recesses st06_asylummain_player_start_chapter4_division "" 0
```

Late-game section:

```
nextmap root/chapter/an_evil_within st40_gamedesign_part_01_player_start_rocket_restart "" 0
```

You can bind a jump to a key for quick iteration:

```
bind F9 "nextmap root/chapter/the_keeper cata_gd_b1_player_start_3 \"\" 0"
```

## Caveats

- **You must already be in a map.** At the title screen it only prints
  `nextMap only works if a map is running!`. Load any chapter first (or use `omap`).
- **Exactly four arguments.** There is no shorthand form.
- **`nextmap` is not a save load.** It restores the map and the layers you pass, but not
  the checkpoint's game state. Enemies, script variables, one-time triggers and puzzle
  state are not restored, so a jumped-to encounter can be empty. Load the save itself
  when you need the real encounter; use `nextmap` for geometry/route practice.
- **A jump is not a checkpoint restore.** Only your inventory and player state carry
  over; scripted setup for the target area is not replayed. Doors, one-time triggers,
  enemy spawns and puzzle state can be wrong, so treat a jumped-to section as a sandbox,
  not a valid run. Keep a clean save.
- **Checkpoint entities are not spawn points.** Names containing `checkpoint` or
  `func_save_check_point` are save triggers; they store your position when the game
  saves. Passing one to `nextmap` leaves no spawn transform, which drops you at the
  origin (a black void). Use a `player_start` entity name instead.
- **Invalid spawn spots** will either fail the load or drop you at the default start.
  Check the name against the appendix, or test it with `teleport` while in that map.
- **Map names are paths.** Keep the `root/chapter/...` prefix and no `.sbsp` suffix.
- Use `restartmap` to reload the current map from its beginning, `omap <mapname>` to
  load a map directly (developer path), and `slowmap` for the developer render path.
- Back up your save folder before experimenting; jumping can overwrite the autosave /
  `mapstart.zwei` state.

## Appendix — spawn spots found in the shipped data

These are entity names containing `player_start` that ship inside each map's data. The
list is not guaranteed exhaustive; maps that show no names store them in a compressed
name bank. For those, use your save's `mapstart.zwei`, or probe candidate names with
`teleport` while in the map.

### `root/chapter/an_emergency_call`

```
p00b_gd_player_start_1
player_start_3
st13_envmain_player_start_1
st13_gamedesign_b_player_start_1
st13_gamedesign_b_player_start_2
st13_gamedesign_b_player_start_3
st13_gamedesign_b_player_start_4
st13_gamedesign_b_player_start_6
st13_gamedesign_b_player_start_7
st16_prop_break_b_player_start_1
```

### `root/chapter/remnants`

_No `player_start` names in the plain data; use your save's `mapstart.zwei` or probe candidates with `teleport`._

### `root/chapter/claws_of_the_horde`

```
gd03_em_player_start_check_1
gd03_em_player_start_check_2
gd03_em_player_start_check_3
gd03_em_player_start_check_4
gd03_em_player_start_check_5
gd03_em_player_start_check_6
st01_terrain_season1_player_start_1
```

### `root/chapter/inner_recesses`

```
gd04_player_start_1
gd06_player_start_1
gd06_player_start_2
gd06_player_start_3
gd06_player_start_4
p01d_env_player_start_1
player_start_1
player_start_3
player_start_4
player_start_village_a_2
player_start_village_a_3
st06_asylummain_player_start_10
st06_asylummain_player_start_12
st06_asylummain_player_start_13
st06_asylummain_player_start_14
st06_asylummain_player_start_4
st06_asylummain_player_start_5
st06_asylummain_player_start_8
st06_asylummain_player_start_9
st06_asylummain_player_start_b
st06_asylummain_player_start_chapter4_division
st06_asylummain_player_start_kidrescue_restart_a_02
test_player_start_2
```

### `root/chapter/losing_grip_on_ourselves`

The generic chapter-start spawn is `player_start` — that is what the game itself wrote into
`SLOT5\inventory.zwei`. The plain-text scan finds no named `*_player_start_N` variants; the
only other start-like entity in the plain data is `lgo_pl_start`, which is a trap (it exists,
so `teleport` accepts it, but it places you in the void).

### `root/chapter/the_keeper`

```
cata_gd_b1_player_start_1
cata_gd_b1_player_start_2
cata_gd_b1_player_start_3
cata_gd_b1_player_start_4
cata_gd_b1_player_start_5
cata_gd_b1_player_start_6
cata_gd_b4_player_start_7
cata_gd_b4_player_start_8
p04_gd_b2_player_start_1
p04_gd_b3_player_start_1
p04_gd_b4_player_start_1
player_start_1
```

### `root/chapter/a_planted_seed_will_grow`

```
st02_cave_enemy_season1_player_start_1
st02_cave_game_system_player_start_1
st02casvprops_player_start_1
```

### `root/chapter/the_cruelest_intentions`

```
boogeymanbarnevent_player_start_2
boogeymanevent_player_start_1
boogeymanevent_player_start_3
boogeymanevent_player_start_at_piano_wire
gamedesign01_player_start_1
gamedesign01_player_start_2
gamedesign01_player_start_3
gamedesign01_player_start_4
player_start_1
srmwds_player_start_1
srmwds_player_start_2
sroomflower_player_start_1
```

### `root/chapter/casualties`

```
player_start_1
st24_gd_hgr_player_start_1
st24_gd_hgr_player_start_10
st24_gd_hgr_player_start_3
st24_gd_hgr_player_start_4
st24_gd_hkt_player_start_4
st24_gd_hkt_player_start_5
st24_gd_top_player_start_1
```

### `root/chapter/reunion`

```
p06a_gd_player_start_1
p06a_gd_reunion_player_start_11111111
p06b2nd_player_start_2
p06c_gd_player_start_4
reunion_player_start_01
st22_gamedesign_part_02_player_start_1
st22_gamedesign_part_02_player_start_2
st22_gamedesign_part_02_player_start_3
st22_gamedesign_part_03_player_start_1
st22_gamedesign_part_03_player_start_7
st22_phase_02_game_player_start_5
st22_phase_02_game_player_start_6
st22_prop_new_office_00_player_start_44444
st22_prop_new_office_00_player_start_44445
```

### `root/chapter/the_ride`

```
ch11_gd_player_start_1
st23_gd_part_01_player_start_1
st23_gd_part_01_player_start_2
st23_gd_part_01_player_start_3
st23_gd_part_01_player_start_4
st23_gd_part_01_player_start_5
```

### `root/chapter/the_craftsmans_tools`

```
st08_alpha_player_start_1
st08_alpha_player_start_2
st08_bsmtmz_player_start_1
st08_bsmtmz_player_start_3
st08_bsmtmz_player_start_4
st08_bsmtmz_player_start_5
st08_bsmtmz_player_start_6
st08_bsmtmz_player_start_7
st08_bsmtmz_player_start_8
st08_bsmtmz_player_start_9
```

### `root/chapter/ulterior_motives`

```
st25_gd_rift_player_start_2
st25_gd_rift_player_start_3
st25_gd_sew_player_start_1
st25_gd_sew_player_start_2
st25_gd_sew_player_start_4
st25_gd_ss_player_start_3
st25_gd_ss_player_start_5
st25_gd_ss_player_start_6
st25_gd_sta_player_start_1
st25_gd_sta_player_start_2
st25_gd_sta_player_start_3
st25_gd_sta_player_start_4
st25_gd_sta_player_start_5
```

### `root/chapter/an_evil_within`

```
gd_l_battle_player_start_1
gd_l_battle_player_start_3
gd_l_battle_player_start_4
gd_l_battle_player_start_5
gd_l_battle_player_start_6
lastasylum_player_start
player_start_1
player_start_3
player_start_4
st40_gamedesign_part_01_player_start_7
st40_gamedesign_part_01_player_start_bigstem_restaret
st40_gamedesign_part_01_player_start_dev_for_realstem
st40_gamedesign_part_01_player_start_restart_handgun
st40_gamedesign_part_01_player_start_rocket_restart
st40_gamedesign_part_01_player_start_rotary_start
st40_gamedesign_part_01_player_start_turret_restart
st40_gamedesign_part_03_player_start_1
```

### `root_dlc1/ch1/dlc1_chapter1`

```
dlc1_ch1_gd_after_player_start_1
dlc1_ch1_gd_after_player_start_2
dlc1_ch1_gd_after_player_start_3
dlc1_ch1_gd_after_player_start_5
dlc1_ch1_gd_before_player_start_1
dlc1_ch1_gd_memroom_player_start_1
```

### `root_dlc1/ch2/dlc1_chapter2`

_No `player_start` names in the plain data; use your save's `mapstart.zwei` or probe candidates with `teleport`._

### `root_dlc2/ch3/dlc2_chapter3`

```
psm_player_start_1
saveroom_base_player_start_1
temp_mobius_brush_player_start_1
```

### `root_dlc2/ch4/dlc2_chapter4`

_No `player_start` names in the plain data; use your save's `mapstart.zwei` or probe candidates with `teleport`._

### `root_dlc_box_2/stage0/dlc_box_stage_0_main`

_No `player_start` names in the plain data; use your save's `mapstart.zwei` or probe candidates with `teleport`._
