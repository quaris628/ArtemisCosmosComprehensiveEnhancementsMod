# Artemis Cosmos Comprehensive Enhancements Mod
Mod for the Artemis Cosmos Spaceship Bridge Simulator game intended to provide bugfixes, quality-of-life enhancements, better parity with Artemis version 2, and other enhancements that generally align with the spirit of the vanilla game.

###  To download the latest version:
1) Go to https://github.com/quaris628/ArtemisCosmosComprehensiveEnhancementsMod/releases/latest
2) Download the "Source Code" zip file.

### To install:
1) Unzip the mod files (right-click the zip file you downloaded, then select "Extract All...")
2) Browse to your Artemis Cosmos folder that contains the game files that you wish to apply this mod to. If you bought Artemis Cosmos through steam, you can open this folder from your library by right-clicking Artemis Cosmos in the list of games (on the left), hover over "Manage", then select "Browse local files".
3) Optional, but strongly recommended: Create a backup copy of your entire Artemis Cosmos folder.
4) Take the mod files you extracted and copy them into your Artemis Cosmos folder, such that the mod files overwrite the vanilla files.
5) A window should appear that says the destination already has files with the same names. (If this doesn't happen, then something went wrong in step 4.) When this happens, choose to replace the files in the destination.

### To report bugs, give feedback, etc:

If you believe the bug/feedback/etc is only pertinent to this mod, then create a public issue on github ( https://github.com/quaris628/ArtemisCosmosComprehensiveEnhancementsMod/issues ) or you may privately email me at `quaris314@gmail.com`.

If you believe the bug/feedback/etc is only pertinent to vanilla Artemis Cosmos, then create a github issue here: https://github.com/artemis-sbs/LegendaryMissions/issues/new/choose

If you are unsure whether the bug/feedback/etc is pertinent to this mod or vanilla, then assume it's pertinent to this mod; I should be able to sort out which is which, and if it's vanilla I'll forward it.

# List of features:

Misc GUI:
- Buttons and other gui elements are colored light blue
- Many buttons and other gui elements have white text, to contrast with background colors better
- Rearranged widgets of each console to be more consistent across consoles and across different screen sizes
- Fix Engineering, science, and comms widgets not having their custom positions persist between screen refreshes (vanilla feature request [#653](https://github.com/artemis-sbs/LegendaryMissions/issues/653))

Console selection screen:
- Allow selecting multiple consoles at once (Artemis 2 parity) (vanilla feature request [#475](https://github.com/artemis-sbs/LegendaryMissions/issues/475))
- Prevent multiple clients from selecting the same console (Artemis 2 parity) (vanilla feature request [#35](https://github.com/artemis-sbs/LegendaryMissions/issues/35))
  - Which consoles do/don't allow multiple clients is configurable in LegendaryMissions/settings.yaml . By default, the exclusive consoles are helm, weapons, engineering, science, and comms.
- Display number of ready and connected clients on each player ship
- Allow opening the help document from console selection
- Allow clients with mainscreen selected to edit their ship name and ship class (Artemis 2 parity)
- Display detailed ship specifications when editing ship name and class
- Display which player ships, if any, have been destroyed (i.e. lost)
- Prettier background

Game setup screen (the screen that shows on the server before the game starts):
- Allow configuring player ship names and ship classes (Artemis 2 parity) (vanilla feature request [#266](https://github.com/artemis-sbs/LegendaryMissions/issues/266))
- Environment settings that are overridden by the currently-selected map are replaced with that overriding value
- Added more convenient button to reboot the currently-running mission script
- Prettier background

Pause menu:
- Added button to end the game (Artemis 2 parity)
- Added confirmation step to ending the game and rebooting mission scripts
- Prettier background

Game results screen:
- Display more detailed statistics about the game (Artemis 2 parity)
- Replace the "all your base are belong to us" phrase with "all allied bases have been destroyed".
- Prettier background

Weapons:
- Prevent converting homings to energy if doing so would make energy go over 1000 (Artemis 2 parity)
- Prevent converting non-homing ordinance to energy (Artemis 2 parity)

Engineering:
- Display repair condition of each individual system (Artemis 2 parity) (vanilla feature request [#549](https://github.com/artemis-sbs/LegendaryMissions/issues/549))
- Damcons start in crew rooms, if possible
- Overheat systems when energy is over 4000 (Artemis 2 parity)
- Add warp resistor coils and APU toggle to engineering
  - Warp resistor coils make the warp drive extremely energy-inefficient. Useful when you need to dump a lot of energy.
  - The APU very slowly generates energy.
  - Automatic mode keeps the APU on only while under 1000 energy, and the warp resistor coils on only while over 4000 energy.
- Increase size of grid node icons by 1.5x

Science:
- Scan info includes vessel type description (vanilla feature request [#453](https://github.com/artemis-sbs/LegendaryMissions/issues/453))
- Wreck scan info includes description of possible anomaly types it could drop (vanilla feature request [#506](https://github.com/artemis-sbs/LegendaryMissions/issues/506))
- Remove irrelevant randomly-generated information from wreck scan info
- Intel on captains includes whether they are brave or cowardly (Artemis 2 parity)
- Removed possible taunt information related to bravery and cowardice, to avoid confusion with the special brave/cowardly mechanic

Comms:
- Surrendering enemy ships has been overhauled (vanilla issue [#306](https://github.com/artemis-sbs/LegendaryMissions/issues/306))
  - You can ask a ship to surrender an unlimited number of times, with no penalty (Artemis 2 parity)
  - If the enemy is farther than 5k away, surrender requests will always fail (Artemis 2 parity)
  - If the enemy's weakest shield is below 50% and below 50 points, then they might surrender when asked
  - If the enemy's weakest shield is below 10% and below 10 points, then they will either surrender or say they will never surrender when asked
  - An enemy's shields must worsen in order for subsequent surrender requests to have any chance at succeeding
  - Brave captains surrender less easily (Artemis 2 parity)
  - Cowardly captains surrender more easily, and will never be never-surrenderable (Artemis 2 parity)
  - Code cases are now activated using a special comms message to transmit codes
  - Enemy responses to surrenders now better match the Artemis 2 messages, including the unique message for a secret code case (Artemis 2 parity)
- Surrendered ships may be given navigation commands
  - If the player ship that gives the command is too far away for too long (10k away for ~60 seconds), then the surrendered ship will no longer comply
- Surrendered ships have a grace period of ~2 minutes before the players lose contact with it, and contact won't be lost while a player ship is closer than 16k

Single-seat craft:
- Switching away from the cockpit screen will not eject you from the craft; you will only be ejected if you deselect the hangar console or disconnect
- Add alternative gui controls that are (hopefully) quicker to respond and clearer to read than the built-in grid of buttons
  - Shield balance radio
  - Ordinance type radio
  - Eject button
  - Mothership dropdown
- Display repair condition of individual craft systems (e.g. beams, maneuver, etc.) (vanilla feature request [#550](https://github.com/artemis-sbs/LegendaryMissions/issues/550))
- Add zoom and color mode controls to hangar map

Mainscreen:
- When opened, show the correct view, facing, and mode (vanilla issues [#595](https://github.com/artemis-sbs/LegendaryMissions/issues/595) and [#291](https://github.com/artemis-sbs/LegendaryMissions/issues/291))
- Different clients will always show the same skybox (vanilla issue [#627](https://github.com/artemis-sbs/LegendaryMissions/issues/627))
- Fix console selection sometimes suddenly switching to mainscreen (vanilla issue [#610](https://github.com/artemis-sbs/LegendaryMissions/issues/610))
- Allow configuring default view, facing, and mode in LegendaryMissions/settings.yaml

New consoles:
- Add simple 2d map console

Operator mode:
- Allow configuring server to run in quasi-headless mode, in which it will render (almost) nothing on its screen
- Allow configuring which 
- NOTE: The setting to lock clients to specific consoles is not respected by this mod. This is difficult to fix, but I plan to try fixing this in some future version.

Pirates:
- Added these pirate player ships (Artemis 2 parity)
  - Strongbow
  - Longbow
  - Brigantine
- Strongbow and Brigantine have configurable beam arcs that weapons can control
- Added these pirate single-seat craft
  - Adventure (shuttle)
  - Dart (fighter)
  - Corsair (bomber)
- Pirates can loot surrendered vessels (Artemis 2 parity)
  - Must rendezvous within 500 of the surrendered vessel for a few seconds (Artemis 2 parity)
  - Larger ships give more loot, and smaller ships give less loot (Artemis 2 parity)
  - Looting larger ships is slower, and looting smaller ships is faster
  - Surrendered vessels' hail responses will indicate if they've already been looted
  - Comms may demand surrendered ships prepare to be boarded
    - Ships that are prepared for boarding take less time to loot
    - Comms can toggle whether the player ship will loot all surrendered ships (default) or only loot surrendered ships that are prepared for boarding
  - Delay game end for 60 seconds to allow looting when all enemies are defeated but there are still surrendered ships (that are not about to lose contact with the players)
- Do not end the game when all friendly stations have been destroyed if at least one player ship is a pirate
- Special docking permissions for player pirate ships (Artemis 2 parity)
  - Player pirate ships must kill an enemy before they are allowed to dock at TSN stations (Artemis 2 parity)
  - Player pirate ships that killed a friendly ship or station are permanently banned from docking at TSN stations, regardless of how many enemies they have killed (Artemis 2 parity)
  - Player pirate ships cannot recieve nukes from TSN stations (Artemis 2 parity)
  - Player pirate ships cannot recieve mines from TSN stations
  - Ships that do not have docking permissions at a station cannot tell the station what ordinance to produce (Artemis 2 parity)
  - Ships that do not have docking permissions at a station cannot view what ordinance the station has stored or is producing
  - Ships that do not have docking permissions at TSN stations cannot successfully order TSN and civilian ships where to go
  - Kills made by pirate single-seat craft are counted as kills made by their mothership, and so affect their mothership's docking privileges accordingly
  - Pirate single-seat can only dock at pirate capital ships
  - Non-pirate single-seat craft can never dock at pirate capital ships
  - NOTE: Kills made with mines might or might not affect docking privileges due to vanilla bug [#495](https://github.com/artemis-sbs/LegendaryMissions/issues/495)

- Pirate-exclusive side quests (Artemis 2 parity)
  - Every 4 minutes, a side quest will be offered in the form of a comms message (Artemis 2 parity)
  - Performing the side quest involves rendezvousing with one ship or station to steal supplies, then rendezvousing with a second ship or station to exchange their the supplies for ransom (Artemis 2 parity)
  - Possible rewards are 800 energy, 2 nukes, extra engineering coolant, and enhanced shield generators (Artemis 2 parity)
  - Comms message to start the side quest is about intercepting a secret message, which is different from Artemis 2; all other side quest comms message content matches Artemis 2

Misc:
- Docking stations show their type as a 3-letter code in their name; for example, SCI for science station, CMD for command base, etc. (vanilla feature request [#427](https://github.com/artemis-sbs/LegendaryMissions/issues/427))
- Hide surrendered ships' beam arcs (Artemis 2 parity) (vanilla feature request [#448](https://github.com/artemis-sbs/LegendaryMissions/issues/448))
- Increase rate at which energy and ordinance are replenished while docked with a station
- Increase refresh rate for all resupply and refit operations
- TSN and civilian vessels might drop wrecks when destroyed
- Rename the "Terran" origin to "TSN", to avoid confusion with mostly-terran-pirates

These independent mods are included:
- [Unofficial Patch](https://github.com/quaris628/ArtemisCosmosUnofficialPatch)
- [Cheery Beeps Mod](https://github.com/quaris628/ArtemisCosmosCheeryBeepsMod)

#  Compatibility:

Supported vanilla versions:
- 1.3.0

Mission Compatibility:

Mission | Is it ok to run this mission with this mod installed? | Does the Comprehensive Enhancements Mod work? | Other comments
--- | --- | --- | ---
[LegendaryMissions](https://github.com/artemis-sbs/LegendaryMissions) | Yes | Yes |
[remote_mssion_pick](https://github.com/artemis-sbs/remote_mission_pick) | Yes | Yes | Other missions started via remote_mission_pick will have the same compatibility as if they were started via any other way.
All Others | Yes | Partially |

Mod compatibility:

Mod (& version) | Is it ok to install both mods? | In what order should they be installed? | Would the Comprehensive Enhancements Mod work? | Other comments
--- | --- | --- | --- | ---
[Unofficial Patch](https://github.com/quaris628/ArtemisCosmosUnofficialPatch) any version | Yes, but there's no reason to | Unofficial Patch first, Comprehensive Enhancements Mod second | Yes | The Comprehensive Enhancements Mod already includes the Unofficial Patch
[Cheery Beeps Mod](https://github.com/quaris628/ArtemisCosmosCheeryBeepsMod) any version | Yes, but there's no reason to | Any | Yes | The Comprehensive Enhancements Mod already includes the Cheery Beeps Mod
[TSN Mod](https://github.com/tsnrp/TSN-Cosmos-Mod) Conversion | Yes | Comprehensive Enhancements Mod first, TSN mod second | Partially |
[TNG Mod](https://github.com/ScornMandark/Cosmos-TNG-Mod) v0.2.3 | Yes | Comprehensive Enhancements Mod first, TNG mod second. | Partially | The TNG mod hasn't been updated since vanilla 1.3.0 was released, so it might not even be compatible with vanilla 1.3.0.

Disclaimer: I have not tested every mod and mission script combination. Instead, this compatibility information is based on which files are modified/provided by each mod or mission script. Therefore, this information might not be completely accurate.

# Credits

Contributors:
- Quaris

Mission scripting assistance from:
- Doug Reichard
- Astrolamb
- Bassellope

Playtesting and feedback:
- PirateLord
- Bassellope
- Gypsyjuggler
- Asiansnowman
- Bart
- steveoe
- Dave Trinh
- PoingFerret
- Liberty4All
- VonErebos

Special thanks to:
- Thom Robertson for sharing development versions of Artemis Cosmos
- Bassellope for hosting playtests
