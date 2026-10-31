# The Evil Within — Console Command Inventory

Reference for the retail Windows build of The Evil Within.

| | |
|---|---|
| Target | `Epic\TheEvilWithin\EvilWithin.exe` |
| Engine | id Tech 5 ("Tango") — same command system as RAGE / Wolfenstein: TNO |

## Summary

**494 distinct console command names** are registered with the engine's
command system (`idCmdSystemLocal::AddCommand`). They fall into three classes:

| Class | Count | Behaviour when typed |
|---|---:|---|
| Functional | 188 | Runs the real command handler |
| No-op stub | 10 | Registered, but the handler is an empty `return` |
| Removed in retail | 296 | Prints `CONSOLE COMMAND REMOVED IN SHIPPING RETAIL: <name> <desc>` |

Some commonly used commands resolve as:

- `find` — functional (`0x140042600`, "finds all system elements containing the given search string")
- `ToggleDebugCamera` — functional (`0x14009B8D10`)
- `God` — functional (`0x140BEF360`, prints `godmode ON` / `godmode OFF`)

Command names are matched case-insensitively by the engine (`idStr::Icmp`), so
`god`, `GOD` and `God` all work. There is no plain `map`/`devmap` in this build
(replaced by `omap` / `slowmap` / `restartmap`).

---

## Functional console commands (188)

| Command | Handler | Description |
|---|---|---|
| `aasLoad` | `0x1408CD690` | load a particular AAS |
| `aasStats` | `0x1408CD700` | shows AAS stats |
| `addarrow` | `0x1408CD790` | adds a debug arrow |
| `addClamp` | `0x140D4CD80` | — |
| `addline` | `0x1408CD790` | adds a debug line |
| `addPlayerViewPrefForPreview` | `0x1408CD9D0` | adds a preference of player's view for plreview |
| `addWrap` | `0x140D4CEA0` | — |
| `backToMainMenu` | `0x14004FF60` | back to main menu |
| `bind` | `0x14007D2F0` | — |
| `bink` | `0x14026C500` | — |
| `bink_pause` | `0x14026C830` | — |
| `bink_stop` | `0x14026C850` | — |
| `blinkline` | `0x1408CDD50` | blinks a debug line |
| `break` | `0x1400424E0` | causes a debug breakpoint |
| `buildRenderProg` | `0x1403A9760` | — |
| `buildRenderProgs` | `0x1403A9870` | — |
| `centerview` | `0x1408CDFB0` | centers the view (set pitch to 0) |
| `changeWetness` | `0x140266E90` | — |
| `clearDebugPoints` | `0x140820AB0` | empties the list of debug points |
| `clearHistory` | `0x140068E90` | — |
| `clearLights` | `0x1408CE130` | clears all lights |
| `clearPlayerViewPrefForPreview` | `0x1408CE2C0` | clears all player's preferences |
| `closeViewNotes` | `0x1408CE320` | close the view showing any notes for this map |
| `compressFile` | `0x140050240` | compresses a file |
| `con_unwatch` | `0x140069000` | removes the specified console watch. Specify 'all' to remove all watches. |
| `con_watch` | `0x140069140` | adds a new console watch - displays per frame results of console var/function printed output |
| `connect` | `0x1403584B0` | connect to the specified IP (only when net_usePlatformBackend 0) |
| `copy` | `0x140D4F090` | copy a file |
| `crash` | `0x140042500` | causes a crash |
| `cvar_restart` | `0x140D4D220` | — |
| `cvarAdd` | `0x140D4CFC0` | — |
| `cvarMultiply` | `0x140D4D060` | — |
| `cvarRandom` | `0x140D4D120` | — |
| `cvarsModified` | `0x140D4D290` | — |
| `damage` | `0x1408CE400` | apply damage to an entity |
| `decompressFile` | `0x1400505B0` | decompresses a file |
| `deleteGenerated` | `0x1400509D0` | deletes the generated path |
| `deleteGeneratedModels` | `0x140050910` | deletes the generated models path |
| `dir` | `0x140D4F4C0` | lists a folder |
| `dirtree` | `0x140D4F280` | lists a folder with subfolders |
| `disconnect` | `0x140050C90` | disconnects from a game |
| `dumpWarnings` | `0x140044A10` | Dump all warnings to a text file. |
| `echo` | `0x140D5AA50` | prints text |
| `EntityInstanceNum` | `0x14097CD40` | print a count of entity instance |
| `envshot` | `0x140284A70` | takes an environment shot |
| `envshot2` | `0x140284900` | takes an environment shot |
| `error` | `0x1400425D0` | causes an error |
| `exec` | `0x140D5AAE0` | executes a config file |
| `exit` | `0x140043710` | exits the game |
| `find` | `0x140042600` | finds all system elements containing the given search string |
| `findImageInMaterial` | `0x1402373B0` | Scans parsed materials for an image |
| `freeze` | `0x140043640` | freezes the game for a number of seconds |
| `gameError` | `0x1408CE6C0` | causes a game error |
| `getviewpos` | `0x1408CE6F0` | prints the current view position |
| `God` | `0x140BEF360` | — |
| `history` | `0x140068EA0` | — |
| `hitch` | `0x140051E50` | hitches the game |
| `kill` | `0x1408CEE70` | kills the player |
| `killEnemies` | `0x1408CE8E0` | removes all enemies |
| `killEntity` | `0x1408CE8F0` | removes the entity with the given name, 'kill entityname' will remove that single entity, 'kill all entityname' removes all entities matching the class of the given name |
| `killItems` | `0x1408CEAA0` | removes all Items |
| `killMoveables` | `0x1408CEAE0` | removes all moveables |
| `killNpcies` | `0x1408CEB20` | removes all Npcies |
| `killPartners` | `0x1408CEB60` | removes all Partners |
| `killshot` | `0x1408CEB90` | fire a shot guaranteed to kill any actor in the player's focus |
| `leaveGame` | `0x140052580` | disconnects from a game |
| `listBinds` | `0x14007D500` | — |
| `listCmds` | `0x140D5B930` | lists commands |
| `listCvars` | `0x140D4D2B0` | — |
| `listDecls` | `0x1403AB6D0` | lists all decls |
| `listImages` | `0x140237890` | lists images |
| `listInventory` | `0x1408CEFA0` | lists players inventory or inventory of actor player is targeting with cursor |
| `listLines` | `0x1408CEEC0` | lists all debug lines |
| `listMegaLayers` | `0x1402716A0` | — |
| `listModels` | `0x1401B97C0` | lists all models |
| `listRenderLights` | `0x140298730` | lists the renderLights |
| `listRenderModels` | `0x140298830` | lists the renderModels |
| `listVirtualTextures` | `0x1402D5BB0` | lists all the referenced virtual texture pagefile pathnames |
| `loadGameSteam` | `0x1400525F0` | loads a game from the steam cloud |
| `localizeRebind` | `0x14007D5A0` | — |
| `LP_AreaFileInfo` | `0x140222210` | — |
| `LP_BakeAll` | `0x1402223E0` | — |
| `LP_BakeHere` | `0x1402223E0` | — |
| `LP_Clear` | `0x140222410` | — |
| `LP_DebugRenderMode` | `0x140222430` | — |
| `LP_ForceColor` | `0x140222510` | — |
| `LP_Info` | `0x140222860` | — |
| `LP_Merge` | `0x140223810` | — |
| `LP_PickHere` | `0x140223DB0` | — |
| `LP_Reload` | `0x140223EB0` | — |
| `LP_UpdatePK5` | `0x140223ED0` | — |
| `menumap` | `0x140053CB0` | goto menu map |
| `morphemeTester_ChangeState` | `0x1408CE060` | changes state of the specified MorphemeTester |
| `morphemeTester_SendRequest` | `0x1408CFC10` | sends a request to the specified MorphemeTester |
| `morphemeTester_SetModel` | `0x1408CFCE0` | sets model of MorphemeTester |
| `morphemeTester_SetParameter` | `0x1408CFEC0` | sets a parameter of the specified MorphemeTester |
| `net_debugOutputSignedInUsers` | `0x140343280` | Outputs all the local users and other debugging information from the sign in manager |
| `net_removeUserFromLobby` | `0x1403432D0` | Removes the given user from the lobby |
| `nextmap` | `0x140053F40` | transitions to the next map, maintaining inventory |
| `Noclip` | `0x140BEF4D0` | — |
| `omap` | `0x140050C10` | loads a map using DevMap_f |
| `ParallelJobStats` | `0x140D70990` | — |
| `parse` | `0x140D5BC80` | prints tokenized string |
| `path` | `0x140D55560` | lists search paths |
| `playCutscene` | `0x1408CF0D0` | Play Cutscene |
| `playEvents` | `0x1400436C0` | playEvents <name> playback sys events F12 will stop playback |
| `plog_disable` | `0x140D99560` | — |
| `plog_enable` | `0x140D99610` | — |
| `plog_toggle` | `0x140D996D0` | — |
| `popDebugPoint` | `0x140827D40` | removes a debug point from the list of debug points |
| `popLight` | `0x1408CF1C0` | removes the last created light |
| `pushDebugPoint` | `0x140827D70` | adds a debug point to the list of debug points |
| `quit` | `0x140043710` | quits the game |
| `randomTest` | `0x1408D28E0` | superficial test of random number generators |
| `recordCutscene` | `0x1408CF3A0` | Record Cutscene |
| `recordEvents` | `0x1400438D0` | recordEvents <name> start recording sys events |
| `recordEventsBase` | `0x140043740` | recordEvents <name> start recording sys events save to base path |
| `recordViewNotes` | `0x1408CF490` | system record the current view position with notes |
| `reexportDecls` | `0x1403ACD30` | reparses and saves decls of a specific type |
| `reloadDecls` | `0x1403ADC70` | reloads decl files that have changed |
| `reloadEntity` | `0x1408CF790` | reloads the specified entity |
| `reloadLanguage` | `0x140043920` | reload language dict |
| `reloadModels` | `0x1401B9C00` | reloads models |
| `reloadNonVirtualMaterials` | `0x140238700` | reloads image files that have changed |
| `remoteDepotStatus` | `0x140D74C40` | prints the on/off status of the remote depot system. |
| `removeline` | `0x1408CF900` | removes a debug line |
| `removePlayerLight` | `0x1408CF9D0` | remove a light(binded player) |
| `renameRenderProg` | `0x140285270` | temporarily replace a renderProg with a different one |
| `reset` | `0x140D4D2C0` | — |
| `resetBreakables` | `0x1408CFB00` | reset breakables |
| `resetViewParms` | `0x1408CFB80` | Resets the current view renderParms |
| `restartmap` | `0x1400547C0` | restarts the current map |
| `rp` | `0x140284FB0` | Displays or modifies a renderparm |
| `s_restart` | `0x140315DE0` | restart sound system |
| `saveGameSteam` | `0x140054980` | saves a game to the steam cloud |
| `set` | `0x140D4D320` | — |
| `seta` | `0x140D4D320` | — |
| `setPlayerViewParamForPreview` | `0x1408CFFD0` | changes a preference parameter of player's view for plreview |
| `setviewpos` | `0x1408D0720` | sets the current view position |
| `showInstallStatus` | `0x140054B20` | Print Installation Status |
| `showViewNotes` | `0x1408D0A40` | show any view notes for the current map, successive calls will cycle to the next note |
| `slowmap` | `0x140050C10` | loads a map using slow non shipping render path in developer mode |
| `startServer` | `0x140359490` | start a multiplayer game lobby |
| `StartSlowMotion2` | `0x140045A20` | — |
| `StopSlowMotion` | `0x140045B30` | — |
| `stripStrings` | `0x140043950` | strip strings containing the specified substring or prefix |
| `teleport` | `0x1408D1130` | teleports the player to an entity location |
| `teleportCam` | `0x1408CDE30` | teleports the player to x,y,z, facing yaw pitch |
| `testDeath` | `0x1408D1240` | tests death |
| `testImage` | `0x140285440` | displays the given image centered on screen |
| `testLight` | `0x1408D1390` | tests a light |
| `testParallelLight` | `0x1408D18F0` | tests a point light |
| `testPlayerLight` | `0x1408D1F20` | tests a point light (bind player)  ( size , intensity, material ) |
| `testPlayerLight2` | `0x1408D1B80` | tests a point light (bind player)  ( size , intensity, material ) |
| `testPlayerSpotLight` | `0x1408D2210` | tests a point light (bind player)  ( size , intensity, material ) |
| `testPointLight` | `0x1408D25B0` | tests a point light |
| `TestPostEffect` | `0x140A3F4B0` | — |
| `testRenderTarget` | `0x140285EB0` | displays the images for a given render target |
| `testSound` | `0x1403163B0` | tests a sound |
| `testStatsBegin` | `0x140043D20` | starts a test session for recording stats |
| `testStatsEnd` | `0x140043D60` | ends a test session for recording stats and exits the game |
| `testWorld` | `0x140286720` | copies current world to the testWorld |
| `toggle` | `0x140D4D4A0` | — |
| `toggleAllMegaLayers` | `0x140271720` | — |
| `ToggleDebugCamera` | `0x1409B8D10` | — |
| `ToggleMainMenu` | `0x14085E6C0` | — |
| `toggleMegaLayers` | `0x1402717D0` | — |
| `touchDecl` | `0x1403AE030` | reparses a decl |
| `trace` | `0x1400448B0` | forces a trace |
| `trigger` | `0x1408D2840` | triggers an entity |
| `unbind` | `0x14007D830` | — |
| `unbindAll` | `0x14007D700` | — |
| `vid_restart` | `0x140045310` | resizes/fullscreens the game window |
| `vstr` | `0x140D5C080` | inserts the current value of a cvar as command text |
| `vt_benchmark` | `0x1402D2330` | Benchmark the virtual texture transcoding |
| `vt_emptyCache` | `0x1402D3890` | empties and zeros the physical images |
| `vt_info` | `0x1402DBA30` | Reports information on the current virtual texture system |
| `vt_lockPages` | `0x1402D6710` | locks physical pages |
| `vt_reload` | `0x1402D6FA0` | reload all the currently loaded virtual textures |
| `vt_restart` | `0x1402D7610` | reallocates the physical images for changes in size or compression |
| `vt_transcodeBenchmark` | `0x1402D9210` | Benchmark the virtual texture transcoding |
| `vt_validateCache` | `0x1402DB2E0` | consistency checks the page buffers |
| `vt_visualBenchmark` | `0x1402DBEF0` | Benchmark the virtual texture transcoding |
| `wait` | `0x140D5C0F0` | delays remaining buffered commands one or more frames |
| `where` | `0x1408CE6F0` | prints the current view position |
| `writeConfig` | `0x1400448F0` | writes a config file |
| `writeEntitiesFile` | `0x140045ED0` | — |
| `writeImage` | `0x140238CD0` | Writes a tga for a given image |

---

## Command syntax and arguments

Based on each command's own usage text where it has one. Where no usage text is
printed, the argument count the command expects is shown instead (command name included).
Tokens in `<>` are required, `[]` optional.

| Command | Syntax / arguments | Source |
|---|---|---|
| `addarrow` | `addline <x y z> <x y z> <color>` | usage text |
| `addClamp` | `addClamp [variablename] [add] [min] [max]` | usage text |
| `addline` | `addline <x y z> <x y z> <color>` | usage text |
| `addWrap` | `addWrap [variablename] [add] [min] [max]` | usage text |
| `bind` | `bind <key> [command] : attach a command to a key` | message text |
| `blinkline` | `blinkline <num>` | usage text |
| `changeWetness` | `changeWetness target seconds` | usage text |
| `copy` | `copy <src> <dst> (os paths)` | usage text |
| `cvarRandom` | `cvarRandom <cvar> <from> <to>` | usage text |
| `damage` | `damage <name of entity to damage> <damageDecl>` | usage text |
| `dir` | `dir <directory> [extension]` | usage text |
| `dirtree` | `dirtree <directory> [extension]` | usage text |
| `dumpWarnings` | `com_dumpWarnings <file name>` | usage text |
| `envshot` | `envshot <basename> [size] [blends]` | usage text |
| `envshot2` | `envshot2 <basename> [size] [blends]` | usage text |
| `exec` | `exec <filename> : execute a script file` | message text |
| `find` | `find <search string>` | usage text |
| `findImageInMaterial` | `FindImageInMaterial <imageName>` | usage text |
| `freeze` | `freeze <seconds>` | message text |
| `killshot` | `killshot <projectile decl>` | usage text |
| `listImages` | `listImages [unloaded] [scratch] [files] [cubes] [covers] [isolated] [block] [ active \| sorted \| touched \| classify \| oversized ]` | usage text |
| `LP_AreaFileInfo` | `LP_AreaFileInfo <filename>` | message text |
| `menumap` | `syntax: menumap <mapnameTarget>` | message text |
| `nextmap` | `syntax: nextMap <mapname> <checkpointname> <addWorldSpawnLayersFromNextMapIfFirstTime> <worldIndex>` | message text |
| `playCutscene` | `PlayCutscene <CutsceneID> [ <startFrame> <endFrame> ]` | usage text |
| `plog_disable` | `plog_disable <group1> [group2] [...]` | usage text |
| `plog_enable` | `plog_enable <group1> [group2] [...]` | usage text |
| `plog_toggle` | `plog_toggle <group1> [group2] [...]` | usage text |
| `pushDebugPoint` | `debugPoint x y z debugPoint ( x y z ) debugPoint ( x, y, z ) debugPoint { x=0, y=0, z=0 )` | usage text |
| `recordCutscene` | `RecordCutscene <CutsceneID> [ <startFrame> <endFrame> ]` | usage text |
| `reexportDecls` | `reexportDecls type <name>` | usage text |
| `removeline` | `removeline <num>` | usage text |
| `renameRenderProg` | `renameRenderProg <renderProg> [newProg]` | usage text |
| `reset` | `reset <variable>` | usage text |
| `rp` | `rp <renderParmName> [value]` | usage text |
| `stripStrings` | `stripStrings <match string>` | usage text |
| `teleport` | `teleport <name of entity to teleport to>` | usage text |
| `testImage` | `testImage [-depth] [-flipX] [-flipY] [-lod val] [-channel val] [-YCoCg] [-range minVal maxVal scaleVal] [-scale val] [-offset xVal yVal] image` | usage text |
| `testSound` | `testSound <file>` | usage text |
| `toggle` | `toggle <variable> - toggles between 0 and 1 toggle <variable> <value> - toggles between 0 and <value> toggle <variable> [string 1] [string 2]...[string n] - cycles through all strings` | usage text |
| `toggleAllMegaLayers` | `toggleAllMegaLayers <0/1>` | message text |
| `toggleMegaLayers` | `toggleMegaLayers <layerId> <0/1>` | message text |
| `touchDecl` | `touchDecl <type> [name]` | usage text |
| `trigger` | `trigger <name of entity to trigger>` | usage text |
| `unbind` | `unbind <key> : remove commands from a key` | message text |
| `vstr` | `vstr <variablename> : execute a variable command` | message text |
| `writeConfig` | `writeconfig <filename>` | usage text |
| `writeEntitiesFile` | `writeEntitiesFile <mapname>` | usage text |
| `writeImage` | `writeImage <destFile> <imageProgram>` | usage text |

Handlers that only validate an argument count (no usage text):

| Command | Expected tokens |
|---|---|
| `addPlayerViewPrefForPreview` | `14` tokens (command + 13 args) |
| `centerview` | `2` tokens (command + 1 arg) |
| `crash` | `2` tokens (command + 1 arg) |
| `hitch` | `2` tokens (command + 1 arg) |
| `Noclip` | `2` tokens (command + 1 arg) |
| `reloadEntity` | `2` tokens (command + 1 arg) |
| `setPlayerViewParamForPreview` | `3` tokens (command + 2 args) |
| `teleportCam` | `6` tokens (command + 5 args) |
| `wait` | `2` tokens (command + 1 arg) |

Notes:

- `killshot` **requires** a projectile decl argument. The handler checks `argc > 1` and
  otherwise prints `USAGE: killshot <projectile decl>` and returns. The name is resolved
  through the decl system, so a bad name prints `Unknown projectile decl '<name>'`. Use
  `listDecls` (or `find`) to enumerate valid decl names.
- `set` / `seta` refuse to touch read-only cvars (`%s is read only`) and report
  `Archived CVar '%s' in production mode` — relevant when a `set` appears to do nothing.
- `nextmap` prints `syntax: nextMap <mapname> <checkpoint>` and only works while a map is
  running (`nextMap only works if a map is running!`).
- `killEntity` / `reloadEntity` both require an entity name and print
  `Must pass in an entity name to ...` / `Entity '%s' not found.`

---

## Registered no-op stubs (10)

These names are accepted by the parser but their handler is the empty function
at `0x140A2B800`, i.e. they silently do nothing.

| Command | Handler | Description |
|---|---|---|
| `activateConsole` | `0x140A2B800` | — |
| `changeBoogeymanGpuParticleParameter` | `0x140A2B800` | change GPU particle parameter |
| `clear` | `0x140A2B800` | — |
| `disasmScript` | `0x140A2B800` | disassembles script |
| `idStudio` | `0x140A2B800` | — |
| `listTangoRenderModelParticles` | `0x140A2B800` | lists the renderModels |
| `restartmaphere` | `0x140A2B800` | restarts the current map and teleports the player back to the current position |
| `script` | `0x140A2B800` | executes a line of script |
| `swapThirdPerson` | `0x140A2B800` | swap thirdperson  mode |
| `vt_setSource` | `0x140A2B800` | Explicitly change the page file for a virtual material to compare |

---

## Removed in the shipping retail build (296)

These commands keep their original descriptions, but typing one only prints the
removal notice — no action is performed.

| Command | Description |
|---|---|
| `achievementsClear` | clears state of an achievement |
| `achievementsClearAll` | clears state of all online achievements |
| `achievementsList` | Lists all the online achievements |
| `achievementsProgress` | shows the progress of all the achievements for the user |
| `achievementsTest` | This tests all the achievements online to make sure the decls match |
| `actionButtonShow` | Shows/hides the Tango HUD ActionButton |
| `addGameFlag` | add a game flag to the game flag db |
| `anim_checkCompressionError` | checks the compression error setting for animations in the specified folder |
| `benchmarkGameData` | Test seek and read of the gameresources file |
| `bgl_Report` | — |
| `bitmapConsole` | tests bitmap console |
| `BoogeymanEffectTest` | Test BoogeymanEffect |
| `Build1dTexureAtlasMainGameDLC1Test` | Build1dTexureAtlasMainGameDLC1Test |
| `BuildInfo` | Display relevant build information. |
| `BuildInfoToClipBoard` | Copy build information to windows clipboard. |
| `CaptureCutscene` | write out screenshot after time passed in |
| `CaptureCutsceneSub` | write out screenshot after time passed in |
| `chapterClearShow` | Show ChapterClear Menu |
| `CheckGpuParticleAutoDiv` | CheckGpuParticleAutoDiv |
| `CheckLoadedMaterialSurfTypes` | CheckLoadedMaterialSurfTypes |
| `CheckPrt1dTexture` | CheckPrt1dTexture |
| `checkSWF` | Loads and unloads a swf to report memory usage and check for leaks |
| `cleanMapFolders` | Cleans out old map files (.bcm, .bmodel and .proc) from map folders) |
| `CleanupCasDirectory` | Deletes all but the latest version of each content addressable file |
| `ClearDebugDrawing` | Clears all the debug lines |
| `clearWarnings` | clears the warnings list (only show) |
| `clearWarnings2` | clears the warnings list |
| `CmdMacroPlay` | <optional filename> <optional loop count>. Plays CmdMacro |
| `CmdMacroRecord` | Records a cmd macro. Optionally specify filename |
| `CmdMacroStop` | Stops recording and playback of cmd macro |
| `conDump` | dumps the console text to a file |
| `ConvertIsUsedFlag` | ConvertIsUsedFlag |
| `ConvertPoiPlayerColor` | Converts the color for player POI from hex to int and sets the poi_PlayerColor cvar |
| `convertToSuperScript` | converts a .script file to a .ss file |
| `countModelsPerNode` | — |
| `createResourceIDs` | Create resource IDs without conflicts. |
| `CreateTestCube` | Writes a single pixel sized cube map with different colors on the sides for radiosity validation |
| `credits` | Shows the Zwei credits |
| `debugMegaShadows` | (workshop)prints debug info about the megashadows |
| `DelayedScreenshot` | write out screenshot after time passed in |
| `Delete` | delete one or more items |
| `DeleteSelected` | deletes selected entity from the game world, but does not remove it from the map file. |
| `devMapStart` | map Start from declMapStart |
| `dialogClear` | clears all dialogs that may be hung |
| `dialogShow` | show a dialog  arg0:DialogType |
| `DisableDebugCamera` | Disable the debug camera |
| `discSwapper_getDiscNumber` | Returns which disc is in use |
| `discSwapper_testTokenization` | Tests how the string is going to be broken up |
| `dlcBoxShop` | Opens the Boxman DLC Shop Menu |
| `DrawCollision` | Visualize the collision model for the world |
| `DumpDeclCutsceneEv` | Dump DeclCutsceneEv |
| `dumpHeapEntries` | Walks the heap in debug builds |
| `dumpRenderObjectsMaxNum` | dumpRenderObjectsMaxNum |
| `EnableDebugCamera` | Enable the debug camera |
| `EnableStreamFileLog` | Allocate memory for the stream file log |
| `ExportDamageParts` | Export Damage Parts Entity -> idDeclDamageParts |
| `ExportPlayerAmmo` | exports all the ammo types the player can have |
| `ExportPlayerInventoryCosts` | exports costs to a csv from the appropriate decls |
| `ExportPlayerWeaponStats` | exports weapon stats to a csv from the appropriate decls |
| `exportTriggers` | export all trigger information to file triggers.txt |
| `fc_clearHDC` | Clear both the memory cache and hard drive backing cache. |
| `fc_clearMem` | Clear the memory cache but leave the hard disk backing cache. |
| `fc_stats` | Reports file cache statistics. |
| `fc_testCacheDrive` | — |
| `filmStripper` | generate a texture film strip from all the textures in a specified directory |
| `findMemoryLeakClass` | check a class allocation and free |
| `FindTriangleData` | Scans for models that still hold CPU side data |
| `FindUnlocalizedStrings` | Goes through the decls and writes out a file of some of the unlocalized strings, if given a parameter that'll be the file it writes to. |
| `FindUnreferencedStrings` | Goes through the lang file and finds ones that aren't in decls. (doesn't mean it's not in a map though) |
| `force_disconnect_all` | force disconnect on all users |
| `ForceIdListsToReallocateEveryAppend` | Enable idList debugging tool |
| `ForgeStartAnalysis` | start recording analysis reports |
| `ForgeStartRecordingMetrics` | record performance metrics |
| `ForgeStopAnalysis` | stop recording analysis reports |
| `ForgeStopRecordingMetrics` | stop performance metrics recording |
| `fullUpgrade` | Upgrade All Skills |
| `GenDamageSkin` | Generates Damage Skins |
| `GenerateEnvMaps` | Generate environment cube maps from the center of all environment areas |
| `GenerateOrthoMap` | creates high-res map images of the current map |
| `getAllColectItem` | get All ColectionItems |
| `GetTestParticleImpactPosTNG` | Get test particle impact position |
| `GfxInfo` | show graphics info |
| `Give` | gives one or more items |
| `GiveDialogTest` | gives one or more items with a dialog test |
| `guardPages` | Covers all allocated memory with guard pages |
| `GuardResources` | Sets a guard page on all idResources, use reportGuardedResources to see which have not been touched |
| `HideGamePlayer` | hide player model |
| `ImportPlayerAmmo` | imports ammo from a csv and writes to appropriate decls |
| `ImportPlayerInventoryCosts` | imports costs from a csv and writes to appropriate decls |
| `ImportPlayerWeaponStats` | imports weapon stats from a csv and writes to appropriate decls |
| `in_restart` | Restart the input sysem |
| `ItemsInMap` | get the stats from all items in the level |
| `KillPlayer` | Kill player |
| `KillTestParticlesTNG` | Kill test particles |
| `List` | Lists all resources of a given type |
| `listDevices` | Lists the connected sound devices |
| `listHudVisible` | print idPlayerHud_Render visible list |
| `listLoadAnim` | list up Active Tango Loading Animations |
| `listMemTags` | lists the TAG_* names for each numeric value |
| `ListParticleMemoryInfoTNG` | List particle static buffer memory usage information |
| `ListRenderModelsGrouped` | lists the renderModels grouped by Model name and sorted by total number |
| `listSpawnCheckFlag` | list spawnCheckFlag |
| `listSWF` | Lists all current idSWF objects |
| `ListTangoDeclParticleTextureMemory` | Lists tango decl particle texture memory. |
| `ListVfxAtlas1dImages` | Lists the images registered in the _vfxatlas1d |
| `Load` | Loads a resource type / name |
| `LoadAllDeclParticle` | LoadAllDeclParticle |
| `loadoutsClearAll` | clears all stored loadouts for the master user and returns to the defaults |
| `MakeAmbientMap` | makes an ambient map |
| `makeConsoleFont` | writes consoleFont.cpp |
| `MakeTest` | makeTest <mapName> [##] Starts recording a regression test using layer ## |
| `MakeTestLoadGame` | makeTestLoadGame <mapName> <layer #> Starts recording a regression test for loading a savegame |
| `mapCollectComplete` | Map pecies collect complete |
| `mapFileInfo_LoadTest` | — |
| `mapFileInfo_SaveTest` | — |
| `mapFileInfo_ShowLayerInfo` | — |
| `MegaScreenShot` | take a mega-screenshot |
| `MQTestBitBuffer` | Tests AMQP Frame bit buffer writing and reading |
| `MQTestForgeRPCBridge` | Test RPC between idTech and Forge |
| `MQTestPresenceBuffer` | Tests AMQP Frame property presence buffer writing and reading |
| `MQTestRPCAsyncLoop` | Test MQ RPC Async Loop |
| `MQTestRPCAsyncTimeout` | Test MQ RPC Async Timeouts |
| `MQTestRPCParams` | Tests AMQP Protobuf RPC parameter functionality |
| `MQTestRRCall` | Test MQ RPC client functionality. |
| `Net_BandwidthChallenge` | Test network bandwidth |
| `Net_DropClient` | Drop a client |
| `net_snapshot_metrics_clear` | Clear named watch/ignore |
| `net_snapshot_metrics_ignore` | Ignore snapshot metrics containing this name |
| `net_snapshot_metrics_print` | Prints next snapshot report to console log |
| `net_snapshot_metrics_watch` | Only show snapshot metrics containg this |
| `Net_ThrottlePeer` | Test network bandwidth |
| `nextRegressionTest` | force NextTest() call on regression system |
| `Notarget` | disables the player as a target |
| `openURL` | open web browser |
| `playerInfoIconsState` | change State the Tango HUD playerInfoIcons |
| `playerInfoIconsVisible` | Shows/hides the Tango HUD playerInfoIcons |
| `playFlyThrough` | play back a fly through |
| `PlayTest` | playTest <events\|folder> [startUp] Plays a regression test. Use third argument if running from command line |
| `playtest_DebugDraw` | draws the current playtest log info in debug mode, parameter is ms to draw for, 60000 by default |
| `playtest_SaveAndClear` | saves the playtest log to a file and clears the data |
| `playtest_SaveNoClear` | saves the playtest log to a file does not clear the data |
| `PlayTestAndExit` | playTestAndExit <events\|folder> [startUp] Plays a regression test or folder tree, then shuts down the game |
| `Print` | Prints information about all resources that match the provided name |
| `printMapStartDeclList` | MapStart Decl List Print |
| `PrintSessionCorrelationInfo` | Print session correlation information. |
| `PrintSharedRenderParms` | Print render parms that are used by both a vertex and fragment program |
| `r_lightningStormParms` | r_lightningStormParms <azimuth in degrees> <azimuth window in degrees> <incline in degrees> <incline window in degrees> <max duration> <max brightness> <max frequency> <max period>  set random lightning characteristics |
| `r_lightningStrikeOnce` | r_lightningStrikeOnce <azimuth in degrees> <incline in degrees> <duration> <brightness> <frequency 0> <frequency 1> <frequency 2>  trigger one lightning strike |
| `rebuildRenderProgs` | Deletes one or all of the pre-translated renderprogs and forces them to reload.  Necessary when an include file is modified. |
| `Reload` | Calls ReloadIfStale() for either all resources, or a specific type |
| `Remove` | remove a game entity |
| `renameFile` | Tests idFileSystemLocal::RenameFile(), mostly for delete-target and directory change semantics |
| `RenameResource` | Temporarily replace a resource definition with a different one |
| `ReportGraphicsDriverVersion` | Prints registry info |
| `ReportGuardedResources` | Determine which resources tripped their guard pages |
| `reportHeaps` | reports the allocations in the global and map heaps |
| `reportMainMenuFonts` | reports font usage in main menu |
| `reportMemoryAllocations` | Reports on all the current memory allocations |
| `reportMemoryMappedFile` | dump the current memory mapped file |
| `reportMeshMemory` | Reports on different vertex/index formats used by md6 meshes |
| `reportNumRenderModels` | Writes the number of render models in the map to the console |
| `reportSoundWorld` | Reports emitter / channel information |
| `ReportStalePointers` | Looks for global heap pointers to the map heap |
| `reportStaticModelMemory` | Reports on different vertex/index formats used by static models |
| `ReportStreamFileLog` | Dump the recorded stream file log information |
| `reportSWFMemory` | Lists all current idSWF dictType objects |
| `reportTagStrings` | Walks the heap in debug builds |
| `reportThreadSpeedLogs` | Write a file suitable for excel |
| `ReportWorldSurfaces` | Reports the total surface and parm count |
| `resetProfile` | clears stats, achievements, and loadouts for the master user |
| `ResourceErrors` | Reports all resource errors |
| `Resources` | Reports on all the idResourceLists |
| `s_language` | — |
| `Sample_GuiModel` | Documentation sample |
| `Sample_PixelEdges` | Documentation sample |
| `Sample_Viewport` | Documentation sample |
| `save1dAtlas` | Save the 1dAtlas bimage to disk |
| `savegamePrintErrors` | Prints error code corresponding to each bit |
| `savegameSetErrorBit` | Allows you to set savegame_error by bit instead of integer value |
| `ScreenShotOffAllDiff` | This turns off everything that potentially makes the shot different everytime we run the game |
| `ScreenShotSmokeTestLogic` | This is the logic for our AutoScreenShotSmokeTest |
| `setGameFlag` | set a value of a game flag to the game flag db |
| `SetGameTimeManagerHz` | Sets the game speed |
| `setHudVisible` | set idPlayerHud_Render visible ( HudNo, visible ) |
| `setProfileDefaults` | sets profile settings to default and saves |
| `setSpawnCheckFlag` | set spawnCheckFlag <flagname> <val 0 or 1> |
| `setStatGame` | test function for game stats |
| `SetUiTestParticlesStateTNG` | Set Ui Test Particles State |
| `ShowAlbedoPrograms` | show all used lpp albedo program names |
| `showEntityStats` | shows stats ( and waste ) for loaded entities |
| `ShowGamePlayer` | show player model |
| `showHUD` | Shows/hides the Tango HUD |
| `showLoadAnim` | Shows/hides the Tango Loading Animation |
| `showLoadAnim2` | Shows/hides the Tango Loading Animation |
| `showMegaShadowMap` | (workshop) shows a mega shadowmap on the screen for debugging |
| `ShowOccluderPrograms` | show all used lpp occluder program names |
| `ShowShadowPrograms` | show all used lpp shadow program names |
| `ShowTexLod` | Adds or removes the models generated by texLod for the current map |
| `SoundReportFrequencies` | Displays a frequency histogram of all sound files |
| `SoundReportNonMatchingFrequencies` | Reports sounds that don't match given frquency |
| `Spawn` | spawns a game entity |
| `StartToneMap` | start tone map anim |
| `startUI` | UI - activate |
| `statsClearAll` | clears all lifetime stats for the master user |
| `statsClearGame` | clears all game stats for the master user |
| `SteamResetStats` | Reset all of your steam stats |
| `StepParticleTimeTNG` | modifies a global particle 'timeline' to debug particles in game |
| `StopEmitterTestParticlesTNG` | Stop emitter test particles |
| `StopSlowMotion2` | Stops SlowMotion |
| `StopTest` | stopTest Stops a regression test recording or playback |
| `StopTestFx` | stops the current test fx |
| `StopToneMap` | stop tone map anim |
| `suicide` | suicide the player. |
| `sys_dumpMemory` | Walks the heap and reports stats |
| `sys_dumpMemorydetail` | Walks the heap and reports stats detail |
| `sys_setBreakTag` | — |
| `sys_testAllocPerf` | Test allocation performance |
| `sys_writeMemoryReport` | Walks the heap and writes stats to XML file |
| `test_dlc_rewards` | Call give dlc rewards on the player |
| `Test_tngCStringTable` | — |
| `TestAllIES` | Loads every file in the ies directory |
| `testArray` | Test idArray |
| `testArrayWrapper` | Test idArrayWrapper |
| `testBrightness` | testDiskSwap - Testing mainmenu's SP -> MP disk swap |
| `TestCompressionSpeeds` | Compares zlib and our code |
| `testCreateOSPath` | tests idFileSystemLocal::CreateOSPath |
| `TestCubeImage` | displays the given cube image mapped to a sphere |
| `TestDefMemory` | Test memory savings |
| `TestDeInterleaveBits` | test bit extract |
| `TestDictIniFile` | Tests the writing/reading of various items in a dict to/from an ini file |
| `TestDictJSONFile` | Tests the writing/reading of various items in a dict to/from a JSON file |
| `testDiskSwap` | testDiskSwap - Testing mainmenu's SP -> MP disk swap |
| `testEnv` | overrides default dynamic environment processing with a specific declEnv |
| `TestFMT_X16` | Tests the X16 texture format to make sure it reads as integers in fragment shaders |
| `TestFont` | Render text to the screen |
| `TestFx` | tests a fx impact |
| `TestGammaTable` | Checks for perfect inversion |
| `testGuardPages` | Enables guard pages and performs memory operations to test |
| `testGuardPagesOnNew` | Enables guard pages and performs memory operations to test |
| `TestHansoftReport` | Tests the Hansoft Report code |
| `TestIES` | Tests the sampling of IES lights |
| `TestJiraReport` | Tests the Jira Report code |
| `TestJobParallelHQDXTCompress` | compress an image |
| `TestLoadImage` | Tries to load an image with type based on the extension |
| `TestLocalReport` | Tests the Local Report code |
| `TestMapVolumeFromFadeDB` | Tests TestMapVolumeFromFadeDB |
| `TestMaterial` | displays the given material centered on screen |
| `testMemoryMappedFile` | test idMemoryMappedFile |
| `TestObjLoader` | Tests the new obj file loader |
| `TestParseFaceLine` | Tests part of the obj file parsing |
| `TestParticleTNG` | Tests a particle system |
| `testPlayerCostume` | change the costume of the player |
| `TestPlayerViewParticle` | tests a player view particle |
| `TestPoisonAllocs` | Check for extremely bad allocation times |
| `TestPreprocessorMacros` | check analyze warning |
| `testPrettyMapName` | returns the pretty map name of string passed in or current map |
| `testRemoveAllLocalUsers` | Forces removal of local users - mainly for PC testing |
| `testRenderProgs` | Builds console specific renderprogs as buildGame will |
| `TestRnd` | Tests random number generators |
| `testRobKeyMotion` | — |
| `testSaveGameCheck` | tests existence of savegame |
| `testSavegameDelete` | deletes a savegames without confirmation |
| `testSavegameDeleteAll` | delete all savegames without confirmation |
| `testSavegameEnumerate` | enumerates the savegames available |
| `testSavegameEnumerateFiles` | enumerates all the files in a folder (blank for 'current slot' folder, use 'autosave' for the autosave slot) |
| `TestSaveGameFile` | Exercises the pipelined savegame code |
| `testSavegameGetCurrentSlot` | returns the current slot in use |
| `testSaveGameOutputEnumeratedSavegames` | outputs the list of savegames already enumerated, this does not re-enumerate |
| `testSavegameSetCurrentSlot` | returns the current slot in use |
| `TestSignBit` | Test the INT32_SIGNBIT functions |
| `TestStaleIdListReference` | Tests the test code |
| `TestStreamFileLog` | Flushes all caches and logs the events to bring everything in |
| `TestUiTNG` | Tests an ui system |
| `TestVMTR` | displays the given vmtr centered on the screen |
| `testXML` | tests the idXML classes |
| `testZipBuilderCombineFiles` | test routine for memory zip file building |
| `testZipBuilderExtractFiles` | test routine for memory zip file extraction |
| `tngUIFilePathList` | ui resouce FilePath List / Platform And Language |
| `ToggleCursorGrab` | Toggles the cursor grab status when mouse input is active. |
| `togglePlayerStatTracking` | toggles player stat tracking |
| `ToggleTrailerCamera` | Toggle the trailer camera |
| `tutorialHide` | Shows/hides the Tango HUD Tutorial |
| `tutorialShow` | Shows/hides the Tango HUD Tutorial |
| `ui_option_brightnessImage_Level` | change blackLevel of brightness image |
| `uiEffectBuild` | uiEffectBuild <##.prt2> Builds the specified UI Effect |
| `uiShopMenu` | Opens the Shop Menu |
| `uiSkillsMenu` | Opens the Skills Menu |
| `unlinkRaceModels` | remove models we don't want |
| `upgradeEquippedWeapon` | upgrade equipped weapon |
| `VanishTestParticlesTNG` | Vanish test particles |
| `voicechat_mute` | TEMP |
| `vt_testVmtrRead` | Test reading from the VMTR file |
| `WriteGammaTable` | Writes the static code for the 2.2 gamma table |
| `wsImageDiffer` | Screenshot difference |
| `wsTestSendEmail` | test if sending email is possible from the machine |
| `yawToVector` | convert a yaw value to a normalized vector |

---

## Why the removed commands cannot be re-enabled

The 296 removed commands are not sitting behind a disabled switch. Each one only prints
`CONSOLE COMMAND REMOVED IN SHIPPING RETAIL: <name> <desc>` and returns — there is no
implementation to turn back on.

- All 296 share the same behaviour: the name and description are formatted into the
  removal notice and the command returns. There is no flag test, no branch and no call
  into game code.
- The "gate" cvars `com_allowDebugCommandMode` and `com_allowDebugGui` are registered but
  referenced exactly once — at the point where they are defined. Nothing reads them, so no
  cvar, config or memory flag can turn these commands back on.
- The 10 no-op handlers point at `0x140A2B800`, whose entire body is `return;`.

Consequence: restoring any of these needs the command reimplemented (or ported from a
development build), not a switch flipped.

---

## Notes and caveats

- Console commands are only half of the system: the game also registers a much
  larger set of **cvars** (`r_*`, `com_*`, `g_*`, `player_*`, `vt_*`, …) in a separate
  `idCVar` system. Those are documented in `cvars.md` (3,326 entries, with defaults and
  per-cvar usage notes).
- `base/release.cfg` ships with `con_noPrint 1`, `com_allowDebugCommandMode 0` and
  `com_allowDebugGui 0`; `base/default.cfg` controls the rest. Those gate console
  visibility/output, not the command table itself.
- `base/consoleHistory.txt` in this install shows the exact spellings that were
  previously typed on this machine (`find teleport`, `toggledebugcamera`,
  `noclip`, `god`, `Com_showFPS`, `list`, …), which matches the table above.
- Descriptions are the in-game help strings; a few are empty or are placeholder text
  left by the developers.
- Counts are of registered command *names*; the 296 removed entries are, by
  definition, not usable in this build.

---

## Appendix - Decl catalogue

Decls are the game's data definitions. They live under `generated/decls/<type>/<name>.decl`
in the packaged resources, so a decl is addressed by a **type** plus a **name**.
The game ships **54,328 decls across 63 types**.

This matters for the commands that take a decl argument (`killshot`, `damage`,
`playCutscene`, `testImage`, `testSound`, ...): the decl name is not an inventory item
name, it is `<type>/<path>` as listed below.

Note: `listDecls` prints only per-type totals (`size_kb  count  type`), which is why it
shows groups such as `throwable` instead of individual entries. `reexportDecls <type>`
and `touchDecl <type>` iterate a type and print each name (both re-parse/re-save decls).

### Decl types

| Type | Count |
|---|---:|
| `sound` | 13682 |
| `material` | 11548 |
| `materialvfxtng` | 7554 |
| `particletng` | 6442 |
| `entitydef` | 5655 |
| `md6def` | 2454 |
| `env` | 1553 |
| `renderprog` | 1409 |
| `talkscript` | 850 |
| `renderparm` | 601 |
| `damage` | 371 |
| `attack` | 325 |
| `collectionitem` | 234 |
| `breakable` | 193 |
| `projectileimpacteffect` | 123 |
| `inventoryitem` | 113 |
| `cutscene` | 95 |
| `cutscenevfx` | 91 |
| `cutsceneev` | 89 |
| `weapon` | 88 |
| `projectile` | 85 |
| `cutscenesnd` | 85 |
| `achievement` | 80 |
| `layer` | 61 |
| `tutorial` | 53 |
| `ammo` | 50 |
| `table` | 48 |
| `fx` | 47 |
| `npcvoice` | 47 |
| `randomentityspawn` | 34 |
| `loadanimation` | 33 |
| `playerviewpref` | 28 |
| `mapinfo` | 28 |
| `damagepartsinfo` | 25 |
| `randommessage` | 23 |
| `throwable` | 18 |
| `dlckid_easyposteffect` | 15 |
| `dlckid_easyposteffectparameters` | 14 |
| `wsdeclforceeffect` | 13 |
| `unlockdata` | 9 |
| `weaponhit` | 8 |
| `doorbreakeffect` | 5 |
| `credits` | 5 |
| `volumelight` | 4 |
| `dlckid_multibgmvolumes` | 4 |
| `uiparam` | 4 |
| `uisystemparam` | 4 |
| `uimodelviewer` | 3 |
| `playerprops` | 3 |
| `soundbus` | 2 |
| `health` | 2 |
| `playerupgradesettings` | 2 |
| `uisoundtrackplayer` | 2 |
| `playermorphemesettings` | 2 |
| `goresetting` | 2 |
| `aispy` | 2 |
| `upgradeprice` | 2 |
| `dlckidplayermorphemesettings` | 1 |
| `trapupgradesettings` | 1 |
| `boxmanupgradesettings` | 1 |
| `itemboxupgradesettings` | 1 |
| `saveroomitembox` | 1 |
| `wpswing` | 1 |

### `throwable` (18)

The group behind the `throwable` label you saw in `listDecls`.

```
dlc_box_2/player/dynamite, dlc_box_2/player/molotov, dlc_box_2/player/steel_trap
dlc_kid/throwable/default, dlc_kid/throwable/grenade/sonar, dlc_kid/throwable/player/bottle
dlc_kid/throwable/trap/default, dlc_kid/throwable/trap/mb_bomb
dlc_kid/throwable/trap/mb_camera, dlc_kid/throwable/trap/mb_shock
dlc_kid_2/throwable/grenade/light, zwei/throwable/bottle/bottle_00
zwei/throwable/bottle/bottle_03, zwei/throwable/bottle/default, zwei/throwable/default
zwei/throwable/grenade/default_dont_give, zwei/throwable/grenade/m24
zwei/throwable/prop/bottle
```

### `projectile` (85)

Argument for `killshot <projectile decl>`.

```
dlc_box_2/player/dynamite, dlc_box_2/player/harpoon, dlc_box_2/player/molotov
dlc_box_2/player/rocket, dlc_box_2/player/steel_trap, dlc_box_2/sadist/rocket
dlc_kid/projectile/player/melee/knife, dlc_kid/projectile/small_pistol/for_bossjoseph
dlc_kid/projectile/throwable/grenade/default, dlc_kid/projectile/throwable/grenade/sonar
dlc_kid/projectile/throwable/trap/default, dlc_kid/projectile/throwable/trap/mb_bomb
dlc_kid/projectile/throwable/trap/mb_camera, dlc_kid/projectile/throwable/trap/mb_shock
dlc_kid/weapons/projectile/pistol, dlc_kid/weapons/projectile/pistol_infinite
dlc_kid/weapons/projectile/shotgun/buckshot_spread
dlc_kid_2/projectile/throwable/grenade/light, projectile/base/bullet_default
projectile/base/bullet_rifle_default, projectile/base/bullet_standard, projectile/base/melee
projectile/base/rocket, projectile/base/wp/throw, projectile/brass_knuckles/melee
projectile/dlc_box_2/bossjoseph/firebottle, projectile/dlc_box_2/bossjoseph/small_pistol
projectile/dlc_box_2/sebastian/agony_bomb, projectile/dlc_box_2/sebastian/magnum
projectile/fists/melee, projectile/gatling_gun/enemy, projectile/gatling_gun/standard
projectile/gatling_gun/vs_alpha3, projectile/harpoon_gun/standard2
projectile/machinegun/standard, projectile/magnum/melee, projectile/magnum/standard
projectile/partner/joseph/axe, projectile/partner/joseph/rifle
projectile/partner/joseph/small_pistol, projectile/pistol/melee, projectile/pistol/standard
projectile/rifle/melee, projectile/rifle/standard, projectile/rocketlauncher/chainsaw
projectile/rocketlauncher/for_alpha3, projectile/rocketlauncher/standard
projectile/shotgun/buckshot_spread, projectile/shotgun/melee
projectile/small_pistol/for_alpha3, projectile/small_pistol/for_arrow_trap
projectile/trap_gun/bomb, projectile/trap_gun/em/bomb, projectile/trap_gun/fire
projectile/trap_gun/flash, projectile/trap_gun/freeze, projectile/trap_gun/harpoon
projectile/trap_gun/poison, projectile/trap_gun/tesla, projectile/wp/wp0600
projectile/wp/wp0600_pl, projectile/wp/wp5001, projectile/wp/wp5001_pl, projectile/wp/wp5003
projectile/wp/wp5004, projectile/wp/wp5007, projectile/wp/wp5007/base, projectile/wp/wp5008
projectile/wp/wp5008_pl, projectile/wp/wp5009, projectile/wp/wp5009/base, projectile/wp/wp5016
projectile/wp/wp5017, projectile/wp/wp5020, projectile/wp/wpe0000, projectile/wp/wpe0400
projectile/wp/wpe0710, projectile/wp/wpe0800, projectile/wp/wpe2000
projectile/zwei/throwable/bottle/bottle_00, projectile/zwei/throwable/bottle/bottle_03
projectile/zwei/throwable/bottle/default, projectile/zwei/throwable/grenade/default
projectile/zwei/throwable/grenade/m24, projectile/zwei/throwable/prop/op_bottle
```

### `damage` (371)

Argument for `damage <entity> <damageDecl>`.

```
damage/base/bullet_standard, damage/code_referenced/damage1, damage/code_referenced/fatalfall
damage/code_referenced/hardfall, damage/code_referenced/softfall
damage/code_referenced/suicide, damage/code_referenced/telefrag, damage/gatlinggun/enemy
damage/gatlinggun/standard, damage/harpoon_gun/standard2, damage/harpoon_gun/standard2_graze
damage/kick_opened_door/light, damage/kick_opened_door/standard, damage/machinegun/standard
damage/magnum/standard, damage/pistol/standard, damage/rifle/standard
damage/rocketlauncher/splash, damage/shotgun/buckshot_standard
damage/small_pistol/for_arrow_trap, damage/zwei/common/damage1
damage/zwei/enemy/em0000_village/assaultrifle, damage/zwei/enemy/em0000_village/door_break
damage/zwei/enemy/em0000_village/explode, damage/zwei/enemy/em0000_village/explode_fireman
damage/zwei/enemy/em0000_village/fire, damage/zwei/enemy/em0000_village/handgun
damage/zwei/enemy/em0000_village/melee/barehand/bite
damage/zwei/enemy/em0000_village/melee/barehand/choking
damage/zwei/enemy/em0000_village/melee/barehand/dying_throw
damage/zwei/enemy/em0000_village/melee/barehand/fire
damage/zwei/enemy/em0000_village/melee/barehand/metal
damage/zwei/enemy/em0000_village/melee/barehand/normal
damage/zwei/enemy/em0000_village/melee/barehand/stomp
damage/zwei/enemy/em0000_village/melee/barehand/threaten
damage/zwei/enemy/em0000_village/melee/dead
damage/zwei/enemy/em0000_village/melee/dead_noimpulse
damage/zwei/enemy/em0000_village/melee/onehand/slash
damage/zwei/enemy/em0000_village/melee/onehand/slashdead
damage/zwei/enemy/em0000_village/melee/twohand/metal
damage/zwei/enemy/em0000_village/oscar/synchroattack, damage/zwei/enemy/em0000_village/shotgun
damage/zwei/enemy/em0000_village/sniperrifle, damage/zwei/enemy/em0000_village/throw
damage/zwei/enemy/em0000_village/window_break, damage/zwei/enemy/em0600_zombie/acid
damage/zwei/enemy/em0600_zombie/bite, damage/zwei/enemy/em0600_zombie/death
damage/zwei/enemy/em0600_zombie/door, damage/zwei/enemy/em0600_zombie/down_l_slash
damage/zwei/enemy/em0600_zombie/finish_blow, damage/zwei/enemy/em0600_zombie/grap_miss
damage/zwei/enemy/em0600_zombie/iron_grille, damage/zwei/enemy/em0600_zombie/l_slash
damage/zwei/enemy/em0600_zombie/r_slash, damage/zwei/enemy/em0600_zombie/tentacle
damage/zwei/enemy/em0610_minizombie/center, damage/zwei/enemy/em0610_minizombie/left
damage/zwei/enemy/em0610_minizombie/right, damage/zwei/enemy/em0700_giant/corpse_swing
damage/zwei/enemy/em0700_giant/corpse_takedown, damage/zwei/enemy/em0700_giant/fist
damage/zwei/enemy/em0700_giant/grap_dead, damage/zwei/enemy/em0700_giant/kick
damage/zwei/enemy/em0700_giant/qte_failed, damage/zwei/enemy/em0700_giant/qte_succeded
damage/zwei/enemy/em0700_giant/run_blow, damage/zwei/enemy/em0700_giant/weapon
damage/zwei/enemy/em0700_giant/weapon_blow, damage/zwei/enemy/em0700_giant_dlc/run_blow
damage/zwei/enemy/em1000_reborn/body_touch, damage/zwei/enemy/em1000_reborn/crash
damage/zwei/enemy/em1000_reborn/crash_finish, damage/zwei/enemy/em1000_reborn/fatal
damage/zwei/enemy/em1000_reborn/scratch, damage/zwei/enemy/em1000_reborn/scratch_enemy
damage/zwei/enemy/em1000_reborn/window_break
damage/zwei/enemy/em1003_reborn_hand/melee/attack
damage/zwei/enemy/em1100_chainsaw/door_break, damage/zwei/enemy/em1100_chainsaw/dummy
damage/zwei/enemy/em1100_chainsaw/ladder, damage/zwei/enemy/em1100_chainsaw/nata
damage/zwei/enemy/em1100_chainsaw/neck_cutter, damage/zwei/enemy/em1100_chainsaw/normal_cutter
damage/zwei/enemy/em1200_trauma/chain_l_1, damage/zwei/enemy/em1200_trauma/chain_l_2
damage/zwei/enemy/em1200_trauma/chain_l_3, damage/zwei/enemy/em1200_trauma/chain_m
damage/zwei/enemy/em1200_trauma/claw_l_normal, damage/zwei/enemy/em1200_trauma/claw_r_big
damage/zwei/enemy/em1200_trauma/claw_r_little, damage/zwei/enemy/em1200_trauma/claw_r_normal
damage/zwei/enemy/em1200_trauma/combo_l, damage/zwei/enemy/em1200_trauma/combo_r
damage/zwei/enemy/em1200_trauma/tackle, damage/zwei/enemy/em3000_lightwoman/attack
damage/zwei/enemy/em4000_big_wolf/breakout_explode, damage/zwei/enemy/em4000_big_wolf/charge
damage/zwei/enemy/em4000_big_wolf/hurl, damage/zwei/enemy/em4000_big_wolf/mount_kill
damage/zwei/enemy/em8000_boogeyman/barn_fire, damage/zwei/enemy/em8000_boogeyman/maze_wall
damage/zwei/enemy/em8000_boogeyman/mortal, damage/zwei/enemy/em8000_boogeyman/touch
damage/zwei/enemy/em8400_boxman/fatal, damage/zwei/enemy/em8400_boxman/fatal_30
damage/zwei/enemy/em8400_boxman/fatal_finish, damage/zwei/enemy/em8400_boxman/fatal_finishkill
damage/zwei/enemy/em8400_boxman/hammer, damage/zwei/enemy/em8400_boxman/hammer_breakable
damage/zwei/enemy/em8400_boxman/sack, damage/zwei/enemy/em8400_boxman/tackle
damage/zwei/enemy/em8500_crocodile/dive_kill, damage/zwei/enemy/em8600_squid/crash_finish
damage/zwei/enemy/em8600_squid/impact, damage/zwei/enemy/em8600_squid/normal
damage/zwei/enemy/em8620_squidworm/rupture_l, damage/zwei/enemy/em8620_squidworm/rupture_s
damage/zwei/enemy/em8700_spider/blow, damage/zwei/enemy/em8700_spider/blow2
damage/zwei/enemy/em8700_spider/loop, damage/zwei/enemy/em8710_spiderchild/blow
damage/zwei/enemy/em8800_mansion/car/crash, damage/zwei/enemy/em8800_mansion/car/explosion
damage/zwei/enemy/em8800_mansion/car/press
damage/zwei/enemy/em8800_mansion/mode_a/deadly_bite
damage/zwei/enemy/em8800_mansion/mode_a/deadly_bite_attack
damage/zwei/enemy/em8800_mansion/mode_a/deadly_bite_finish
damage/zwei/enemy/em8800_mansion/mode_a/forward_step
damage/zwei/enemy/em8800_mansion/mode_a/mode_a_breakable
damage/zwei/enemy/em8800_mansion/mode_a/move, damage/zwei/enemy/em8800_mansion/mode_a/normal
damage/zwei/enemy/em8800_mansion/mode_a/strike, damage/zwei/enemy/em8800_mansion/mode_b/cabin
damage/zwei/enemy/em8800_mansion/mode_b/cabin_catch
damage/zwei/enemy/em8800_mansion/mode_b/cabin_entrance_break
damage/zwei/enemy/em8800_mansion/mode_b/cabin_impact
damage/zwei/enemy/em8800_mansion/mode_b/cabin_miss
damage/zwei/enemy/em8800_mansion/mode_b/cabin_throw
damage/zwei/enemy/em8800_mansion/mode_b/cleave, damage/zwei/enemy/em8800_mansion/mode_b/combo
damage/zwei/enemy/em8800_mansion/mode_b/dash, damage/zwei/enemy/em8800_mansion/mode_b/dash_end
damage/zwei/enemy/em8800_mansion/mode_b/dash_graze
damage/zwei/enemy/em8800_mansion/mode_b/modechange
damage/zwei/enemy/em8800_mansion/mode_b/move
damage/zwei/enemy/em8800_mansion/mode_b/soundblast, damage/zwei/enemy/em8801_alpha1_cave/chase
damage/zwei/enemy/em8801_alpha1_cave/fatal, damage/zwei/enemy/em8801_alpha1_cave/fatal_grapple
damage/zwei/enemy/em8810_alpha1_tentacl/test, damage/zwei/enemy/em8900_alpha3/chase/fatal
damage/zwei/enemy/em8900_alpha3/chase/tentacle, damage/zwei/enemy/em8900_alpha3/dodge/trample
damage/zwei/enemy/em8900_alpha3/kill, damage/zwei/enemy/em8900_alpha3/level_design/break_ceil
damage/zwei/enemy/em8900_alpha3/level_design/break_floor
damage/zwei/enemy/em8900_alpha3/level_design/break_floor_final
damage/zwei/enemy/em8900_alpha3/moribund, damage/zwei/env/lamp/fire, damage/zwei/env/oil/fire
damage/zwei/env/oil/fire_for_player, damage/zwei/env/poison/gero
damage/zwei/env/rope/electric, damage/zwei/hithard, damage/zwei/hitsoft, damage/zwei/hitsuper
damage/zwei/minigame/escape_boxman_head, damage/zwei/minigame/lobotomy_puzzle/failed
damage/zwei/partner/axe_00, damage/zwei/partner/axe_02, damage/zwei/partner/melee_ladder
damage/zwei/partner/mission_failed, damage/zwei/partner/rifle
damage/zwei/partner/small_pistol, damage/zwei/player/assasinate_with_knife
damage/zwei/player/assassinate_chainsaw, damage/zwei/player/assassinate_chainsaw_flash
damage/zwei/player/death/acid_trap_final, damage/zwei/player/death/acid_trap_step
damage/zwei/player/drowing, damage/zwei/player/melee_brass_knuckles
damage/zwei/player/melee_fist, damage/zwei/player/melee_handaxe, damage/zwei/player/melee_kick
damage/zwei/player/melee_knife, damage/zwei/player/melee_matchfire
damage/zwei/player/melee_pistol, damage/zwei/player/melee_rifle
damage/zwei/player/melee_shotgun, damage/zwei/player/melee_stomping
damage/zwei/player/melee_torch, damage/zwei/throwable/bottle
damage/zwei/throwable/grenade/m24, damage/zwei/throwable/prop/op_bottle
damage/zwei/trap/acid_shower, damage/zwei/trap/arrow_trap_grinder, damage/zwei/trap/ball
damage/zwei/trap/bear_trap, damage/zwei/trap/bomb_debris, damage/zwei/trap/bot_bomb
damage/zwei/trap/bus, damage/zwei/trap/busopen, damage/zwei/trap/ceiling
damage/zwei/trap/electric_break, damage/zwei/trap/fire_ball, damage/zwei/trap/fire_pipe_type_b
damage/zwei/trap/flamethrower, damage/zwei/trap/flamethrower2, damage/zwei/trap/gas_trap
damage/zwei/trap/killerbot, damage/zwei/trap/long_blade, damage/zwei/trap/mine_trap
damage/zwei/trap/moveable, damage/zwei/trap/moving_wall, damage/zwei/trap/needle
damage/zwei/trap/needle_sp, damage/zwei/trap/oilcan_explosion
damage/zwei/trap/pylon_electric_shock, damage/zwei/trap/pylon_trap_for_enemy
damage/zwei/trap/pylon_trap_for_player, damage/zwei/trap/roller_spike
damage/zwei/trap/roller_spike_slider, damage/zwei/trap/roller_spike_slider_cero
damage/zwei/trap/saw, damage/zwei/trap/spike, damage/zwei/trap/static_bomb
damage/zwei/trap/thresher, damage/zwei/trap/treasure_box, damage/zwei/trap/wind_noise
damage/zwei/trap/wirebomb, damage/zwei/trap_gun/basic, damage/zwei/trap_gun/em/mine_trap
damage/zwei/trap_gun/fire, damage/zwei/trap_gun/flash_lv1, damage/zwei/trap_gun/flash_lv3
damage/zwei/trap_gun/flash_lv5, damage/zwei/trap_gun/freeze, damage/zwei/trap_gun/harpoon
damage/zwei/trap_gun/harpoon_fire, damage/zwei/trap_gun/harpoon_graze
damage/zwei/trap_gun/harpoon_graze_fire, damage/zwei/trap_gun/poison
damage/zwei/trap_gun/tesla_lv1, damage/zwei/trap_gun/tesla_lv3, damage/zwei/trap_gun/tesla_lv5
dlc_box_2/damage/bg8000/break, dlc_box_2/damage/bg8000/move, dlc_box_2/damage/em0780/breakable
dlc_box_2/damage/em0780/finish_kill, dlc_box_2/damage/em0780/finish_kill_fatal
dlc_box_2/damage/em0780/finish_kill_term, dlc_box_2/damage/em0780/weapon
dlc_box_2/damage/em0780/weapon_blow, dlc_box_2/damage/em1003/melee/attack
dlc_box_2/damage/em1180/rocket, dlc_box_2/damage/em1180/tackle, dlc_box_2/damage/em1400/catch
dlc_box_2/damage/em1400/charge, dlc_box_2/damage/em1400/choking
dlc_box_2/damage/em1400/explosion, dlc_box_2/damage/em5001/axe_00
dlc_box_2/damage/em5001/axe_02, dlc_box_2/damage/em5001/dash
dlc_box_2/damage/em5001/finish_kill, dlc_box_2/damage/em5001/finish_kill_fatal
dlc_box_2/damage/em5001/finish_kill_term, dlc_box_2/damage/em5001/firebottle
dlc_box_2/damage/em5001/handgun, dlc_box_2/damage/em5001/push_boxman
dlc_box_2/damage/em5001/push_other, dlc_box_2/damage/em5002/agony_bomb
dlc_box_2/damage/em5002/dash, dlc_box_2/damage/em5002/magnum, dlc_box_2/damage/em5002/punch
dlc_box_2/damage/em5002/push_boxman, dlc_box_2/damage/em5002/push_other
dlc_box_2/damage/em8480/catch, dlc_box_2/damage/em8480/chainsaw
dlc_box_2/damage/em8480/chainsawdash, dlc_box_2/damage/em8480/chainsawdown
dlc_box_2/damage/em8480/chairthrow, dlc_box_2/damage/em8480/dummy
dlc_box_2/damage/em8480/finishblow, dlc_box_2/damage/em8480/hammer1
dlc_box_2/damage/em8480/hammer2, dlc_box_2/damage/em8480/hammer3
dlc_box_2/damage/em8480/hammerdash, dlc_box_2/damage/em8480/hammerdown
dlc_box_2/damage/em8480/shadowdash, dlc_box_2/damage/em8480/stamp
dlc_box_2/damage/em8480/sword1, dlc_box_2/damage/em8480/sword2, dlc_box_2/damage/em8480/sword3
dlc_box_2/damage/em8480/sword4, dlc_box_2/damage/em8480/sword5
dlc_box_2/damage/em8480/sworddash, dlc_box_2/damage/em8480/sworddown
dlc_box_2/damage/em8480/swordenemy, dlc_box_2/damage/em8880/blowoff
dlc_box_2/damage/em8880/melee, dlc_box_2/damage/em8880/melee_ex
dlc_box_2/damage/em8880/press_down, dlc_box_2/damage/em8880/press_up
dlc_box_2/damage/em8880/shout, dlc_box_2/damage/em8880/spring
dlc_box_2/damage/em8880/trample_enemy, dlc_box_2/damage/em8880/trample_player
dlc_box_2/damage/enemy/em0000_village/meat_explode
dlc_box_2/damage/enemy/em0000_village/thrown_ragdoll
dlc_box_2/damage/gimmick/harpoon_launcher_blowoff, dlc_box_2/damage/player/dynamite
dlc_box_2/damage/player/harpoon, dlc_box_2/damage/player/molotov
dlc_box_2/damage/player/rocket, dlc_kid/damage/enemy/em0000_bridge/explode
dlc_kid/damage/enemy/em0000_village/door_break
dlc_kid/damage/enemy/em0000_village/melee/barehand/bite
dlc_kid/damage/enemy/em0000_village/melee/barehand/choking
dlc_kid/damage/enemy/em0000_village/melee/barehand/chokinglast
dlc_kid/damage/enemy/em0000_village/melee/barehand/dying_throw
dlc_kid/damage/enemy/em0000_village/melee/barehand/fire
dlc_kid/damage/enemy/em0000_village/melee/barehand/metal
dlc_kid/damage/enemy/em0000_village/melee/barehand/normal
dlc_kid/damage/enemy/em0000_village/melee/barehand/stomp
dlc_kid/damage/enemy/em0000_village/melee/barehand/threaten
dlc_kid/damage/enemy/em0000_village/melee/dead
dlc_kid/damage/enemy/em0000_village/melee/grabfoot
dlc_kid/damage/enemy/em0000_village/melee/onehand/slash
dlc_kid/damage/enemy/em0000_village/melee/onehand/slashdead
dlc_kid/damage/enemy/em0000_village/throw, dlc_kid/damage/enemy/em0000_village/window_break
dlc_kid/damage/enemy/em3000_lightwoman/electric_zone
dlc_kid/damage/enemy/em5000_bossjoseph/choking_dot
dlc_kid/damage/enemy/em5000_bossjoseph/choking_fatal
dlc_kid/damage/enemy/em5000_bossjoseph/grapple, dlc_kid/damage/enemy/em5000_bossjoseph/handgun
dlc_kid/damage/enemy/em5000_bossjoseph/looking_dot
dlc_kid/damage/enemy/em5000_bossjoseph/swipe, dlc_kid/damage/player/assasinate_with_knife
dlc_kid/damage/player/melee/kick, dlc_kid/damage/player/melee/knife
dlc_kid/damage/player/melee/trample, dlc_kid/damage/player/obstruct_self
dlc_kid/damage/player/pistol, dlc_kid/damage/player/pistol_infinite
dlc_kid/damage/player/shotgun/buckshot_standard, dlc_kid/damage/throwable/trap/shock
dlc_kid/damage/zwei/enemy/em1220_trauma/chain_l_1
dlc_kid/damage/zwei/enemy/em1220_trauma/chain_l_2
dlc_kid/damage/zwei/enemy/em1220_trauma/chain_l_3
dlc_kid/damage/zwei/enemy/em1220_trauma/chain_m
dlc_kid/damage/zwei/enemy/em1220_trauma/claw_l_normal
dlc_kid/damage/zwei/enemy/em1220_trauma/claw_r_big
dlc_kid/damage/zwei/enemy/em1220_trauma/claw_r_little
dlc_kid/damage/zwei/enemy/em1220_trauma/claw_r_normal
dlc_kid/damage/zwei/enemy/em1220_trauma/combo_l
dlc_kid/damage/zwei/enemy/em1220_trauma/combo_r
dlc_kid/damage/zwei/enemy/em1220_trauma/tackle, dlc_kid_2/enemy/dk0401_leslie/haunt_hit
dlc_kid_2/enemy/dk0401_leslie/haunt_touch, dlc_kid_2/enemy/em5100_shadow_kid/grapple
dlc_kid_2/enemy/em5100_shadow_kid/grapple_kill, dlc_kid_2/enemy/em5100_shadow_kid/melee
dlc_kid_2/enemy/em6000_shadow_man/grapple_impact, dlc_kid_2/enemy/em6000_shadow_man/life_drain
dlc_kid_2/enemy/em6000_shadow_man/shockwave, dlc_kid_2/enemy/em6100_shadow_arm/strike
dlc_kid_2/enemy/em8720_spider_leg/fatal, dlc_kid_2/gimmick/elv_shock
dlc_kid_2/gimmick/shadowman_wave
```

### `cutscene` (95)

Argument for `playCutscene <CutsceneID>`.

```
cs1000, cs1001, cs1002, cs1003, cs1004, cs1005, cs1007, cs1008, cs1009, cs1010, cs1011, cs1013
cs1014, cs1015, cs1018, cs1019, cs1020, cs1021, cs1022, cs1023, cs1024, cs1025, cs1026, cs1027
cs1028, cs1030, cs1031, cs1032, cs1033, cs1034, cs1035, cs1036, cs1037, cs1041, cs1042, cs1043
cs1044, cs1045, cs1046, cs1100, cs1101, cs1102, cs1103, cs1104, cs1105, cs1106, cs1107, cs1108
cs1109, cs1110, cs1111, cs1112, cs1200, cs1201, cs1202, cs1203, cs1204, cs1206, cs1207, cs1208
cs1209, cs1210, cs1302, cs1303, cs1304, cs1305, cs1306, cs1307, cs1308, cs1309, cs1310, cs1400
cs1401, cs1402, cs1403, cs1404, cs1406, cs1408, cs1500, cs1501, cs1502, cs1503, cs2003, cs2103
cs2107, cs2114, cs2132, cs2142, cs7000, cs7001, cs7002, cs7003, cs7004, cs7005, cs7006
```

### `ammo` (50)

```
ammo/fists/melee, ammo/gatling_gun/enemy, ammo/gatling_gun/standard
ammo/gatling_gun/vs_alpha3, ammo/machinegun/standard, ammo/magnum/standard
ammo/partner/pistol/standard, ammo/partner/rifle/standard, ammo/pistol/standard
ammo/rifle/standard, ammo/rocketlauncher/chainsaw, ammo/rocketlauncher/for_alpha3
ammo/rocketlauncher/standard, ammo/shotgun/buckshot_spread, ammo/small_pistol/for_alpha3
ammo/small_pistol/for_arrow_trap, ammo/trap_gun/bomb, ammo/trap_gun/em/bomb
ammo/trap_gun/fire, ammo/trap_gun/flash, ammo/trap_gun/freeze, ammo/trap_gun/harpoon
ammo/trap_gun/poison, ammo/trap_gun/tesla, ammo/wp/wp5001, ammo/wp/wp5003, ammo/wp/wp5004
ammo/wp/wp5007, ammo/wp/wp5008, ammo/wp/wp5009, ammo/wp/wp5016, ammo/wp/wp5017, ammo/wp/wp5020
ammo/wp/wp8400, ammo/wp/wpe0000, ammo/wp/wpe0400, ammo/wp/wpe0710, ammo/wp/wpe0800
ammo/wp/wpe2000, dlc_box_2/ammo/bossjoseph/firebottle, dlc_box_2/ammo/bossjoseph/small_pistol
dlc_box_2/ammo/player/rocket, dlc_box_2/ammo/sadist/rocket
dlc_box_2/ammo/sebastian/agony_bomb, dlc_box_2/ammo/sebastian/magnum
dlc_kid/ammo/player/melee/knife, dlc_kid/ammo/player/pistol
dlc_kid/ammo/player/pistol_infinite, dlc_kid/ammo/player/shotgun/buckshot_spread
dlc_kid/ammo/small_pistol/for_bossjoseph
```

### `weapon` (88)

```
dlc_box_2/weapon/bossjoseph/axe, dlc_box_2/weapon/bossjoseph/firebottle
dlc_box_2/weapon/bossjoseph/small_pistol, dlc_box_2/weapon/player/it0018
dlc_box_2/weapon/player/rocket_launcher, dlc_box_2/weapon/sadist/rocket_launcher
dlc_box_2/weapon/sebastian/agony, dlc_box_2/weapon/sebastian/brass_knuckles
dlc_box_2/weapon/sebastian/magnum, dlc_box_2/weapon/wp/wp5030
dlc_kid/weapon/player/doublebarrel_shotgun, dlc_kid/weapon/player/flashlight
dlc_kid/weapon/player/melee/axe, dlc_kid/weapon/player/melee/knife
dlc_kid/weapon/player/pistol, dlc_kid/weapon/player/pistol_infinite
dlc_kid/weapon/small_pistol_bossjoseph, dlc_kid/weapon/wp/wp5001, dlc_kid/weapon/wp/wp5003
dlc_kid/weapon/wp/wp5004, dlc_kid/weapon/wp/wp5008, dlc_kid/weapon/wp/wp5012
dlc_kid/weapon/wp/wp5016, dlc_kid/weapon/wp/wp5020, dlc_kid/weapon/wp/wp5021
dlc_kid_2/weapon/player/burn_wood, weapon/brass_knuckles, weapon/burst_handgun
weapon/busmachingun, weapon/busmachingun_em, weapon/doublebarrel_shotgun, weapon/fists
weapon/harpoon_gun, weapon/machinegun, weapon/magnum, weapon/partner/axe, weapon/partner/rifle
weapon/partner/small_pistol, weapon/partner/small_pistol_kidd, weapon/penetrating_rifle
weapon/pistol, weapon/regimeshotgun, weapon/rifle, weapon/rocketlauncher
weapon/rocketlauncher_chainsaw, weapon/rocketlauncher_last, weapon/small_pistol
weapon/small_pistol_last, weapon/turret_on_truck, weapon/upgrade/handgun
weapon/upgrade/magnum, weapon/upgrade/rifle, weapon/upgrade/shotgun, weapon/upgrade/trapgun
weapon/wp/wp0600, weapon/wp/wp5000, weapon/wp/wp5001, weapon/wp/wp5001_pl, weapon/wp/wp5002
weapon/wp/wp5003, weapon/wp/wp5004, weapon/wp/wp5005, weapon/wp/wp5006, weapon/wp/wp5007
weapon/wp/wp5008, weapon/wp/wp5008_left, weapon/wp/wp5008_pl, weapon/wp/wp5009
weapon/wp/wp5010, weapon/wp/wp5011, weapon/wp/wp5012, weapon/wp/wp5013, weapon/wp/wp5015
weapon/wp/wp5016, weapon/wp/wp5017, weapon/wp/wp5019, weapon/wp/wp5020, weapon/wp/wp5021
weapon/wp/wp5023, weapon/wp/wp8400, weapon/wp/wp8480, weapon/wp/wp8481, weapon/wp/wpe0000
weapon/wp/wpe0400, weapon/wp/wpe0710, weapon/wp/wpe0800, weapon/wp/wpe2000, weapon/wp/wpe3100
```

### `inventoryitem` (113)

```
dlc3/bonus/bonus_shop_ammo_count, dlc3/bonus/bonus_shop_chainsaw
dlc3/bonus/bonus_shop_golden_hammer, dlc3/bonus/bonus_shop_infinite_ammo
dlc3/bonus/bonus_shop_katana, dlc3/bonus/bonus_shop_molotov
dlc3/bonus/bonus_shop_rocket_launcher, dlc3/bonus/bonus_shop_speed
dlc3/bonus/bonus_shop_weapon_power, dlc_kid/model_viewer/black_cat
dlc_kid/model_viewer/bridge_enemy, dlc_kid/model_viewer/haunted_mobius
dlc_kid/model_viewer/joseph_haunted, dlc_kid/model_viewer/oscar, dlc_kid/sound_track/trophy_1
dlc_kid/sound_track/trophy_2, dlc_kid/sound_track/trophy_3, dlc_kid/sound_track/trophy_4
dlc_kid/sound_track/trophy_5, dlc_kid2/sound_track/trophy_10, dlc_kid2/sound_track/trophy_6
dlc_kid2/sound_track/trophy_7, dlc_kid2/sound_track/trophy_8, dlc_kid2/sound_track/trophy_9
dlc_kid_2/model_viewer/infected_sebastian, dlc_kid_2/model_viewer/lightwoman
dlc_kid_2/model_viewer/office_sebastian, dlc_kid_2/model_viewer/shadowman
dlc_kid_2/model_viewer/young_sebastian, keyitem/bus/hemostatic
keyitem/catacombs/relief_door_item_01, keyitem/catacombs/relief_door_item_01_attach
keyitem/catacombs/relief_door_item_02_attach, keyitem/catacombs/relief_door_item_03_attach
keyitem/catacombs/valve_part, keyitem/church/glasses, keyitem/city/card_key2
keyitem/city/key_01, keyitem/default, keyitem/dlc_box_2/file1, keyitem/dlc_box_2/file10
keyitem/dlc_box_2/file11, keyitem/dlc_box_2/file12, keyitem/dlc_box_2/file13
keyitem/dlc_box_2/file14, keyitem/dlc_box_2/file15, keyitem/dlc_box_2/file16
keyitem/dlc_box_2/file17, keyitem/dlc_box_2/file18, keyitem/dlc_box_2/file19
keyitem/dlc_box_2/file3, keyitem/dlc_box_2/file4, keyitem/dlc_box_2/file5
keyitem/dlc_box_2/file6, keyitem/dlc_box_2/file7, keyitem/dlc_box_2/file8
keyitem/dlc_box_2/file9, keyitem/dlc_box_2/letter1, keyitem/dlc_box_2/letter10
keyitem/dlc_box_2/letter12, keyitem/dlc_box_2/letter13, keyitem/dlc_box_2/letter15
keyitem/dlc_box_2/letter16, keyitem/dlc_box_2/letter18, keyitem/dlc_box_2/letter19
keyitem/dlc_box_2/letter2, keyitem/dlc_box_2/letter21, keyitem/dlc_box_2/letter3
keyitem/dlc_box_2/letter4, keyitem/dlc_box_2/letter8, keyitem/dlc_box_2/letter9
keyitem/dlc_kid/chapter1/card_key, keyitem/dlc_kid/chapter1/card_research
keyitem/dlc_kid/chapter2/fuse_00, keyitem/dlc_kid/chapter2/lightwoman_head
keyitem/dlc_kid/chapter2/statue_a, keyitem/dlc_kid/chapter2/statue_b
keyitem/dlc_kid/chapter2/statue_c, keyitem/dlc_kid_2/chapter3/light_puzzle_parts01
keyitem/dlc_kid_2/chapter3/light_puzzle_parts02, keyitem/dlc_kid_2/chapter4/card_key
keyitem/light_house_asylum/key, keyitem/mansion/battery, keyitem/mansion/dial_of_the_safe
keyitem/mansion/dial_of_the_safe2, keyitem/subway/fuse_00
keyitem/underground_village/card_key, keyitem/village/chainsaw, keyitem/village/puzzle_parts
saveroom_key/default, zwei/partner/cp0467, zwei/partner/it0104, zwei/partner/lantern
zwei/player/dlc_box2/upgrade_item, zwei/player/dlc_box_2/ability_defense
zwei/player/dlc_box_2/ability_infinite_ammo, zwei/player/dlc_box_2/ability_life
zwei/player/dlc_box_2/ability_speed, zwei/player/dlc_box_2/chainsaw
zwei/player/dlc_box_2/dynamite, zwei/player/dlc_box_2/firebottle
zwei/player/dlc_box_2/golden_hammer, zwei/player/dlc_box_2/hammer
zwei/player/dlc_box_2/rocketlauncher, zwei/player/dlc_box_2/shop_locked_item
zwei/player/dlc_box_2/sword, zwei/player/dlc_box_2/trap
zwei/player/dlc_kid_2/dlc_kid_succession, zwei/player/lantern, zwei/player/matchbox
zwei/player/matchstick, zwei/player/trap_parts, zwei/player/upgrade_item
```
