---
title: 'Carpet Mod: Enhancing Your Minecraft World'
url: https://www.sea-of-memes.com/revolutionizing-gameplay-with-the-carpet-mod-in-minecraft/
author: Brionna Feil
published: '2023-08-11'
source_blog: Sea of Memes
source_site: http://www.sea-of-memes.com
category: game programming
fetched: '2026-04-13'
---

Carpet Mod offers you unparalleled control within the realm of Minecraft. Have you ever harbored the fantasy of assuming godlike dominion? To wield authority over every in-game entity, the passage of time, spatial configurations, and atmospheric conditions? If you seek a modification that fulfills this aspiration, consider incorporating Carpet Mod into your gameplay! Following the installation of Carpet Mod, a host of novel commands will endow you with amplified influence, enabling you to manipulate the swiftness, potency, and vitality of each entity, even permitting you to preclude the appearance of certain creatures within the game. Furthermore, the ability to accelerate, decelerate, or halt the progression of time is at your fingertips. Steering airborne entities? An effortless endeavor, facilitated by the commands intrinsic to Carpet Mod. The integration of Carpet Mod guarantees an augmented gaming experience, for it confers absolute sovereignty over your domain; every individual, creature, or object lies within the ambit of your command.

## What is Carpet Mod?

Carpet stands as a modification for standard Minecraft, offering a comprehensive grip on the game’s technical aspects.

![gameplay in Minecraft - ninja with sword and its enemies](../../assets/ea1168d3d0bfa557.png)

Key features include:

- Swiftly test farms over hours in just moments with
**/tick warp**, aligned with your computer’s speed; - Gain insights into item production via detailed breakdowns using
**hopperCounters**; - Witness real-time updates on server mobcap, TPS, and more through the
**/log**command; - Unlock the potential for pistons to move block entities like chests, thanks to
**movableBlockEntities**.

## Settings

### allowListingFakePlayers

- Grants the ability to list fake players on the multiplayer screen.

### allowSpawningOfflinePlayers

- Enables spawning offline players in online mode when the specified name doesn’t exist as an online-mode player
- Type: Boolean
- Default value: true

### antiCheatDisabled

- Prevents players from rubberbanding due to excessive speed or being kicked out for ‘flying’;
- Increases trust in client positioning and extends player’s allowed mining distance to 32 blocks;
- Type: Boolean
- Default value: false

### carpetCommandPermissionLevel

- Defines the permission level for Carpet commands;
- Can only be configured via the .conf file;
- Type: String
- Default value: ops

### carpets

- Placing carpets may trigger carpet commands for non-op players.
- Type: Boolean
- Default value: false

### chainStone

- Chains stick together on their long ends and adhere to directly connected blocks.
- Option “stick_to_all” makes chains stick even when not visually connected.
- Type: ChainStoneMode
- Default value: false

### cleanLogs

- Eliminates obnoxious log messages, such as ‘Maximum sound pool size 247 reached’.
- Especially useful for farms and contraptions.
- Type: Boolean
- Default value: false

### commandDistance

- Activates the /distance command to measure in-game distances between points.
- Also enables brown carpet placement action if ‘carpets’ rule is enabled.
- Type: String
- Default value: true

### commandDraw

- Enables /draw commands, allowing the creation of complex shapes.
- Can be restricted to certain permission levels.
- Type: String
- Default value: ops

### commandInfo

- Enables /info command for block information.
- Also enables gray carpet placement action if ‘carpets’ rule is enabled.
- Type: String
- Default value: true

### commandLog

- Enables the /log command to monitor events through chat and overlays.
- Can be limited to specific permission levels.
- Type: String
- Default value: true

### commandPerimeterInfo

- Enables the /perimeterinfo command to scan for potential spawnable spots around a block.
- Can be restricted to specific permission levels.
- Type: String
- Default value: true

### commandPlayer

- Enables the /player command to control and spawn players.
- Can be limited to specific permission levels.
- Type: String
- Default value: ops

### commandProfile

- Enables the /profile command to monitor game performance (subset of /tick command capabilities).
- Can be limited to specific permission levels.
- Type: String
- Default value: true

### commandScript

- Enables the /script command, providing an in-game scripting API for the Scarpet programming language.
- Can be restricted to specific permission levels.
- Type: String
- Default value: true

### commandScriptACE

- Enables restrictions for arbitrary code execution with Scarpet.
- Affects loading apps or running /script commands.
- Type: String
- Default value: ops

commandSpawn

- Enables the /spawn command for spawn tracking.
- Can be limited to specific permission levels.
- Type: String
- Default value: ops

### commandTick

- Enables the /tick command to control game clocks.
- Can be limited to specific permission levels.
- Type: String
- Default value: ops

### commandTrackAI

- Allows tracking of mobs AI using the /track command.
- Can be restricted to specific permission levels.
- Type: String
- Default value: ops

### creativeFlyDrag

- Adjusts creative air drag, slowing down flight.
- Requires speed adjustments for optimal flight experience.
- Client-side setting, doesn’t affect dedicated servers.
- Type: Double
- Default value: 0.09
- Categories: CREATIVE, CLIENT

### creativeFlySpeed

- Multiplies creative flying speed.
- Client-side setting, doesn’t affect dedicated servers.
- Type: Double
- Default value: 1.0
- Categories: CREATIVE, CLIENT

### creativeNoClip

- Enables creative No Clip mode.
- Requires client and server settings for proper functioning.
- No effect if only set on the server.
- Allows phasing through walls, potentially with trapdoor trick.
- Type: Boolean
- Default value: false
- Categories: CREATIVE, CLIENT

### creativePlayersLoadChunks

- Toggles creative players’ chunk loading behavior, similar to spectators.
- Mimics the gamerule spectatorsGenerateChunks.
- Type: Boolean
- Default value: true
- Categories: CREATIVE, FEATURE

### ctrlQCraftingFix

- Enables dropping entire stacks from the crafting UI result slot.
- Type: Boolean
- Default value: false
- Categories: BUGFIX, SURVIVAL

### customMOTD

- Sets a custom MOTD message when connecting to the server.
- Use ‘_’ to adopt the startup setting from server.properties.
- Type: String
- Default value: _
- Suggested options: _
- Categories: CREATIVE

### defaultLoggers

- Sets default logger configurations for new players.
- Use CSV format, like ‘tps,mobcaps’ for multiple loggers.
- ‘none’ for no loggers.
- Type: String
- Default value: none
- Suggested options: none, tps, mobcaps, tps
- Categories: CREATIVE, SURVIVAL

### desertShrubs

- Converts saplings into dead shrubs in hot and water-deprived environments.
- Type: Boolean
- Default value: false
- Categories: FEATURE

### explosionNoBlockDamage

- Prevents explosions from damaging blocks.
- Type: Boolean
- Default value: false
- Categories: CREATIVE, TNT

### fastRedstoneDust

- Optimizes redstone dust for reduced lag.
- Addresses locational behaviors and vanilla redstone issues.
- Behavior of vanilla contraptions not guaranteed.
- Type: Boolean
- Default value: false
- Categories: EXPERIMENTAL, OPTIMIZATION

### fillLimit

- [Deprecated] Set customizable volume limits for fill/fillbiome/clone commands.
- Use vanilla gamerule instead; this setting will be removed in 1.20.0.
- Type: Integer
- Default value: 32768
- Suggested options: 32768, 250000, 1000000
- Categories: CREATIVE

### fillUpdates

- Causes block updates during fill/clone/setblock and structure block commands.
- Type: Boolean
- Default value: true
- Categories: CREATIVE

### flippinCactus

- Enables players to flip and rotate blocks while holding cactus.
- No block updates triggered during rotation/flip.
- Applies to various blocks, including pistons, observers, etc.
- Type: Boolean
- Default value: false
- Categories: CREATIVE, SURVIVAL, FEATURE

### fogOff

- Removes fog from the client in the Nether and the End.
- Improves visibility but may appear unusual.
- Type: Boolean
- Default value: false
- Categories: CLIENT

### forceloadLimit

- Allows customization of the forceload chunk limit.
- Type: Integer
- Default value: 256
- Suggested options: 256
- Categories: CREATIVE
- Additional notes: Choose a value from 1 to 20M.

### hardcodeTNTangle

- Sets horizontal random angle on TNT for TNT contraption debugging.
- Set to -1 for default behavior.
- Type: Double
- Default value: -1.0
- Suggested options: -1
- Categories: TNT
- Additional notes: Must be between 0 and 2pi, or -1.

### hopperCounters

- Hoppers pointing to wool count items passing through them.
- Enables the /counter command and actions with red and green carpets on wool.
- Use /counter <color?> reset to reset, and /counter <color?> to query.
- In survival, place green carpet on same color wool to query, red to reset counters.
- Counters are global and shared between players, with 16 channels available.
- Counts up to one stack per tick per hopper.
- Type: Boolean
- Default value: false
- Categories: COMMAND, CREATIVE, FEATURE

### huskSpawningInTemples

- Only husks spawn in desert temples.
- Type: Boolean
- Default value: false
- Categories: FEATURE

### interactionUpdates

- Placing blocks causes block updates.
- Type: Boolean
- Default value: true
- Categories: CREATIVE

### lagFreeSpawning

- Optimizes spawning for reduced CPU and Memory usage.
- Type: Boolean
- Default value: false
- Categories: OPTIMIZATION

### language

- Sets the language for Carpet.
- Type: String
- Default value: en_us
- Allowed options: en_us, fr_fr, pt_br, zh_cn, zh_tw
- Categories: FEATURE

### lightningKillsDropsFix

- Lightning kills the items dropped when it kills an entity.
- Setting to true prevents lightning from killing drops.
- Fixes MC-206922.
- Type: Boolean
- Default value: false
- Categories: BUGFIX

### liquidDamageDisabled

- Disables block damage caused by flowing liquids.
- Type: Boolean
- Default value: false
- Categories: CREATIVE

### maxEntityCollisions

- Allows customization of maximal entity collision limits.
- Set to 0 for no limits.
- Type: Integer
- Default value: 0
- Suggested options: 0, 1, 20
- Categories: OPTIMIZATION
- Additional notes: Must be a positive number or 0.

### mergeTNT

- Merges stationary primed TNT entities.
- Type: Boolean
- Default value: false
- Categories: TNT

### missingTools

- Glass can be broken faster with pickaxes.
- Type: Boolean
- Default value: false
- Categories: SURVIVAL

### moreBlueSkulls

- Increases the number of blue skulls shot by the wither for testing purposes.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: CREATIVE

### movableAmethyst

- Enables moving of Budding Amethyst blocks using pistons.
- Provides extra drop when mining with silk touch pickaxes.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE

### movableBlockEntities

- Allows pistons to push block entities like hoppers and chests.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: EXPERIMENTAL, FEATURE

### optimizedTNT

- Reduces lag caused by TNT explosions in the same spot or in liquids.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: TNT

### perfPermissionLevel

- Specifies the required permission level for the /perf command.
- Type: Integer
- Default value: 4
- Allowed options: 2, 4
- Categories: CREATIVE

### persistentParrots

- Parrots remain on your shoulders until you receive proper damage.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: SURVIVAL, FEATURE

### piglinsSpawningInBastions

- Enables piglins to respawn in bastion remnants.
- Includes piglins, brutes, and some hoglins.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE

### pingPlayerListLimit

- Customizes the playerlist sample limit for server list ping (Multiplayer menu).
- Type: Integer
- Default value: 12
- Suggested options: 0, 12, 20, 40
- Categories: CREATIVE
- Additional notes: Choose a positive number or 0.

### placementRotationFix

- Addresses block placement rotation issues when placing blocks rapidly.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: BUGFIX

### portalCreativeDelay

- Sets the delay ticks required to use a Nether portal in creative mode.
- Type: Integer
- Default value: 1
- Suggested options: 1, 40, 80, 72000
- Categories: CREATIVE
- Additional notes: Choose a value from 1 to 72000.

### portalSurvivalDelay

- Sets the delay ticks required to use a Nether portal in survival mode.
- Type: Integer
- Default value: 80
- Suggested options: 1, 40, 80, 72000
- Categories: SURVIVAL
- Additional notes: Choose a value from 1 to 72000.

### pushLimit

- Allows customization of the piston push limit.
- Type: Integer
- Default value: 12
- Suggested options: 10, 12, 14, 100
- Categories: CREATIVE
- Additional notes: Choose a value from 1 to 1024.

### quasiConnectivity

- Pistons, droppers, and dispensers check for power to the block(s) above them.
- Defines the range for which these blocks check for ‘quasi power’.
- Type: Integer
- Default value: 1
- Categories: CREATIVE

### railPowerLimit

- Customizable power range for powered rails.
- Type: Integer
- Default value: 9
- Suggested options: 9, 15, 30
- Categories: CREATIVE
- Additional notes: Choose a value from 1 to 1024.

### renewableBlackstone

- Nether basalt generators without soul sand below will convert into blackstone instead.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE

### renewableCoral

- Coral structures will grow with bonemeal from coral plants.
- Expanded mode also allows growing from coral fans for sustainable farming outside warm oceans.
- Type: RenewableCoralMode
- Default value: false
- Allowed options: false, expanded, true
- Categories: FEATURE

### renewableDeepslate

- Lava and water generate deepslate and cobbled deepslate below Y0.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE

### renewableSponges

- Guardians turn into Elder Guardians when struck by lightning.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE

### rotatorBlock

- Dispensers with cacti rotate blocks.
- Rotates blocks anti-clockwise if possible.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE, DISPENSER

### scriptsAppStore

- Sets the location of the online repository of Scarpet apps.
- Set to ‘none’ to disable.
- Point to any GitHub repo with Scarpet apps using //contents/<path…>.
- Type: String
- Default value: gnembon/scarpet/contents/programs
- Categories: SCARPET
- Additional notes: Appstore link should point to a valid GitHub repository.

### scriptsAutoload

- Scarpet scripts from world files will autoload on server/world start if /script is enabled.
- Type: Boolean
- Default value: true
- Allowed options: true, false
- Categories: SCARPET

### scriptsDebugging

- Enables scripts debugging messages in the system log.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: SCARPET

### scriptsOptimization

- Enables scripts optimization.
- Type: Boolean
- Default value: true
- Allowed options: true, false
- Categories: SCARPET

### sculkSensorRange

- Allows customization of the sculk sensor range.
- Type: Integer
- Default value: 8
- Suggested options: 8, 16, 32
- Categories: CREATIVE
- Additional notes: Choose a value from 1 to 1024.

### shulkerSpawningInEndCities

- Shulkers will respawn in end cities.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE

### silverFishDropGravel

- Silverfish drop a gravel item when breaking out of a block.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE

### simulationDistance

- Adjusts the server’s simulation distance.
- Set to 0 to not override the value in server settings.
- Type: Integer
- Default value: 0
- Suggested options: 0, 12, 16, 32
- Categories: CREATIVE
- Additional notes: Choose a value from 0 (use server settings) to 32.

### smoothClientAnimations

- Enhances client animations for smoother experience in low TPS settings.
- Only effective in single-player (SP) mode and may slow down players.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: CREATIVE, SURVIVAL, CLIENT
- Additional notes: A client command applicable when connecting to non-carpet/vanilla servers. Will impact the executing player independently.

### spawnChunksSize

- Alters the size of spawn chunks, determining their new radius.
- Setting to 0 will disable spawn chunks.
- Type: Integer
- Default value: 11
- Suggested options: 0, 11
- Categories: CREATIVE

### stackableShulkerBoxes

- Empty shulker boxes can stack when dropped on the ground or within inventories.
- Type: String
- Default value: false
- Suggested options: false, true, 16
- Categories: SURVIVAL, FEATURE
- Additional notes: Value must be true, false, or a number between 2-64.

### structureBlockIgnored

- Modifies the block ignored by the Structure Block.
- Type: String
- Default value: minecraft:structure_void
- Suggested options: minecraft:structure_void, minecraft:air
- Categories: CREATIVE

### structureBlockLimit

- Customizable limit of structure blocks along each axis.
- Permanent setting required for proper loading.
- Setting ‘structureBlockIgnored’ to air recommended for saving large structures.
- Needed on the client of the player editing the Structure Block.

### structureBlockOutlineDistance

- ‘structureBlockOutlineDistance’ may be necessary for correct long structure rendering.
- Type: Integer
- Default value: 48
- Suggested options: 48, 96, 192, 256
- Categories: CREATIVE
- Additional notes: Value must be greater than or equal to 48.

### structureBlock

- Customizable render distance for Structure Block outlines.
- Required on the client for proper function.
- Type: Integer
- Default value: 96
- Suggested options: 96, 192, 2048
- Categories: CREATIVE, CLIENT
- Additional notes: Must be a positive number or 0. A client command applicable when connecting to non-carpet/vanilla servers.

### summonNaturalLightning

- Summoning a lightning bolt replicates natural lightning’s effects.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: CREATIVE

### superSecretSetting

- Enigmatic placeholder text for an experimental feature.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: EXPERIMENTAL

### thickFungusGrowth

- Enables growth of nether fungi with a 3×3 base using bonemeal.
- ‘all’ makes all nether fungi grow into 3×3 trees.
- ‘random’ results in 6% of nether fungi growing into 3×3 trees (consistent with worldgen).
- Type: FungusGrowthMode
- Default value: false
- Allowed options: false, random, all
- Categories: SURVIVAL, FEATURE

### tickSyncedWorldBorders

- Links world border movement to in-game time rather than real time.
- Adjusts world border speed proportionally when tick rate changes.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: FEATURE

### tntDoNotUpdate

- Prevents TNT from updating when placed adjacent to a power source.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: CREATIVE, TNT

### tntPrimerMomentumRemoved

- Eliminates random TNT momentum upon priming.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: CREATIVE, TNT

### tntRandomRange

- Establishes a fixed range for random TNT explosions.
- Set to -1 for default behavior.
- Type: Double
- Default value: -1.0
- Suggested options: -1
- Categories: TNT
- Additional notes: Requires optimizedTNT to be enabled. Value cannot be negative except for -1.

### updateSuppressionBlock

- Placing an activator rail on top of a barrier block can overload the neighbor updater stack upon rail deactivation.
- The entered integer defines how many updates should remain in the stack.
- Setting to -1 disables this feature.
- Type: Integer
- Default value: -1
- Suggested options: -1, 0, 10, 50
- Categories: CREATIVE
- Additional notes: The value indicates the required updates before logging them. Must be -1 or greater.

### viewDistance

- Alters the server’s view distance.
- Setting to 0 maintains the value from server settings.
- Type: Integer
- Default value: 0
- Suggested options: 0, 12, 16, 32
- Categories: CREATIVE
- Additional notes: Must choose a value between 0 (server settings) and 32.

### xpFromExplosions

- Grants experience drops from explosion-affected experience-yielding blocks.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: SURVIVAL, FEATURE

### xpNoCooldown

- Enables players to instantly absorb XP without delay.
- Type: Boolean
- Default value: false
- Allowed options: true, false
- Categories: CREATIVE

## Conclusion

This comprehensive guide has unveiled the essence of Carpet Mod and provided a comprehensive list of its customizable settings. By exploring the inner workings of this versatile tool, readers can now grasp its potential to elevate their Minecraft experience. Whether it’s fine-tuning gameplay mechanics, optimizing performance, or introducing novel features, Carpet Mod stands as a gateway to a realm of creative possibilities. As players navigate through the diverse settings outlined in this article, they hold the key to shaping their virtual landscapes with precision, redefining the boundaries of their Minecraft ventures.