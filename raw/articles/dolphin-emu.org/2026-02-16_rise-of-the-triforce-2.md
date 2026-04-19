---
title: Rise of the Triforce
url: https://dolphin-emu.org/blog/7G/
author: OatmealDome
published: '2026-02-16'
source_blog: Dolphin Emulator - GameCube/Wii games on PC
source_site: https://dolphin-emu.org/
category: graphics
fetched: '2026-04-19'
---

During the rapid technological advancements of the early 1990s, the video game industry was on the cusp of a massive addition - another dimension. With console shenanigans like the [Super FX chip](https://en.wikipedia.org/wiki/Super_FX) giving players a taste of 3D, hype was at an all-time high. But the games released for home consoles were nothing compared to what arcade developers were capable of doing. By employing gigantic budgets and cutting-edge hardware, the arcade gave players a chance to see the future, today.

15 FPS,

[low resolution (256x192)](https://imagequalitymatters.blogspot.com/2011/01/retro-tech-analysis-virtua-racing-md-vs.html), 6500 polygons per second, practically no textures, and no texture filtering. And this required

[extra hardware in the cartridge](https://segaretro.org/Sega_Virtua_Processor)to achieve.

**60 FPS**, ~4x the pixel count (496x384), 300,000 polygons per second, and filled with perspective-correct and trilinear-filtered textures.

Video Credit:

[arronmunroe](https://www.youtube.com/watch?v=oXgKtlRcXUc)But the future eventually arrived with the launch of the [5th generation of consoles](https://en.wikipedia.org/wiki/Fifth_generation_of_video_game_consoles). All of a sudden, the revolutionary 3D hardware features that were once exclusive to arcades were now available in home consoles. Without next-generation hype pushing players into the arcade, powerful but expensive arcade machines were no longer sustainable to develop. The industry adjusted by moving toward more cost effective solutions, with many turning to the inexpensive, already proven 3D-capable hardware available in 5th gen home consoles.

Rather than turning around the decline of the arcade, the cheaper hardware may have helped accelerate it. There were fewer unique experiences to pull players into the arcade, and previous hit exclusives were now seeing high quality home console ports that allowed them to be enjoyed without munching quarters. When the [6th generation](https://en.wikipedia.org/wiki/Sixth_generation_of_video_game_consoles) arrived with the Dreamcast and the PlayStation 2, many arcade stalwarts waved the white flag and started to shift their arcade divisions to home console projects, [with mixed success](https://en.wikipedia.org/wiki/Devil_May_Cry_2).

Sega was among those hit hardest by this era. They produced some of the greatest arcade thrills of the 1990s and enjoyed massive success in the home console market with the Sega Genesis/Mega Drive. But a string of [mistakes](https://en.wikipedia.org/wiki/32X) and [miscalculations](https://en.wikipedia.org/wiki/Sega_Saturn) combined with the slumping arcade industry sent them to the brink of bankruptcy. By 2002, the Dreamcast had been soundly defeated by the launch of the PlayStation 2, and Sega began [porting](https://wiki.dolphin-emu.org/index.php?title=Sonic_Adventure_2:_Battle) some of their [hits](https://wiki.dolphin-emu.org/index.php?title=Skies_of_Arcadia_Legends) to their former rivals' hardware just to stay afloat.

The home market was lost, but the languishing arcade scene presented Sega with an opportunity. They still had legendary arcade development teams, and if Sega could leverage them to produce a wave of arcade hits, they would be in a position to dominate a new era of arcades when most others were changing gears. There was just one problem: Sega didn't have the resources that they once did. If they were going to do this, they needed some help.

And so they did something that would have been considered unthinkable just five years prior. Sega teamed up with Nintendo to develop a *GameCube-based arcade platform*. Bolstering their ranks was Namco, another coin-op stalwart with tons of arcade veterans.

Three companies, one mission: Triforce.

Click/tap to Play. File has audio.

**Triforce Hardware**[¶](https://dolphin-emu.org#triforce-hardware)

While Triforce was a collaboration project, it still feels like a very *Sega coded* arcade system. It can even use certain [NAOMI](https://segaretro.org/Sega_NAOMI) style components! Along with the Xbox-based [Chihiro](https://segaretro.org/Sega_Chihiro), the Triforce is sometimes considered a successor to the [NAOMI 2](https://segaretro.org/Sega_NAOMI_2).



![triforcetop_thumb.avif](../../assets/e5ca74dddee71941.avif)



![triforceback_thumb.avif](../../assets/343b321901065500.avif)



![triforcebackports_thumb.avif](../../assets/42e8a7be80310718.avif)



![triforceside_thumb.avif](../../assets/722cfef1c289ad4b.avif)


Inside of this metal shell is... a GameCube! Quite literally, actually.

![First Image](../../assets/80502effaf37e0c5.avif)

![Active Image](../../assets/d91ddf0240b1ab20.avif)

Click/Tap to peek at the GameCube underneath!

The Triforce hardware is built around a stock GameCube motherboard, with two Triforce-specific boards attached to it: the AM-Baseboard and AM-Mediaboard. The *AM* (Amusement Machine) boards are the secret sauce of the Triforce and transform the stock GameCube into something capable of producing arcade experiences.

The early boot process is the same as a retail console, but a modified GameCube IPL (sometimes referred to as the GameCube BIOS) is used to initialize the Triforce hardware and load the Triforce equivalent of a "home menu", Segaboot.

Segaboot is a special disc image on the Mediaboard that can be loaded by the Triforce at will through special commands. It is responsible for loading the actual game and for providing the Service Menu, where the operator can run hardware tests and change settings on the machine.

By using [Picoboot](https://github.com/webhdx/PicoBoot) to override the boot process, it is possible to load a standard GameCube IPL or homebrew like [Swiss](https://github.com/emukidid/swiss-gc). And since all of the pins are still on the mainboard, we can also connect a standard GameCube front panel and even load full GameCube games from microSD over Serial Port 2!

The Baseboard is primarily responsible for input and output. It handles translation between JVS I/O devices (more on those later) and the GameCube's [SI bus](https://wiibrew.org/wiki/Hardware/Serial_Interface). It also takes the GameCube's digital video output and feeds it to two VGA ports on the back of the main unit.

The Mediaboard's most important responsibility is storing and serving the game software to the GameCube. It is also used to handle other tasks, such as networking, through special commands.



![am-mediaboard-type3_thumb.avif](../../assets/1a5a399cff5f45ab.avif)

The Triforce Baseboard was mostly unchanged throughout the Triforce's lifespan, but the Mediaboard could vary depending on the developer, game, and when the game was released. In fact, games weren't guaranteed to even come out on the same storage medium!

**Format Wars**[¶](https://dolphin-emu.org#format-wars)

A spinning disc and active laser were not * normally* considered reliable enough for an arcade environment. These machines will be on all day, every day for

*years*, and players were often rough on machines that they didn't own. So, the Triforce eschews the standard GameCube mini-DVD alike format for its own storage solutions.

Most games were designed for the DIMM (Dual In-line Memory Module) variant of the Triforce, where game data is shipped on [GD-ROM](https://en.wikipedia.org/wiki/GD-ROM) and loaded into RAM on the first boot. GD (Gigabyte Disc) was a format initially devised by Sega and Yamaha for use in the Dreamcast. By [increasing the data density](https://en.wikipedia.org/wiki/Double-density_compact_disc) of ordinary compact disc technology, the 12cm GD-ROM had somewhat comparable capacity to the GameCube's DVD-based 8cm disc (1GiB versus 1.46GiB).

Were GD-ROM drives more reliable than early DVD drives? Maybe! By this point, GD-ROM was an established technology that Sega was already using in arcades for years. Perhaps even more importantly, it was *cheaper*. Sega designed it so they could even reuse GD-ROM drives designed for their other arcade platforms, since they used a generic [SCSI](https://en.wikipedia.org/wiki/Parallel_SCSI)-style connector.

DIMM variant Triforces came with stickers advertising the amount of DIMM RAM on the Mediaboard. These stickers caused some confusion in the enthusiast community, as people would often mistake the amount listed as the total RAM accessible to the game. In reality, the DIMM RAM was mostly intended for use as a read-only [RAM drive](https://en.wikipedia.org/wiki/RAM_drive), rather than for general purpose use. As previously mentioned, the Triforce hardware is based around a stock GameCube motherboard, so games can only access the same 24+16 MiB of RAM that a retail GameCube uses.

Once the game was loaded into memory, it was intended to stay there. And thanks to a battery backup that maintained the data even in the event of a power failure, the GD-ROM may only be needed once in the entire lifetime of the machine. *This* was their secret toward making the Triforce GD-ROM drive reliable for the arcade. One of the main exceptions would be if a new disc were inserted. Many Triforce games saw updates, which could be shipped on new GD-ROMs.

Namco's Triforce games ditched the GD-ROM and DIMM RAM and instead used 512MB NAND cartridges to store game data. The NAND retains its contents even if the system loses power and the backup battery runs dry, which eliminates the need for GD-ROMs. These games also saw updates through SD card or over the internet, with updates able to directly modify the NAND contents.



![nandcart_thumb.avif](../../assets/ec1886be7bc07524.avif)



![tricartpcb_thumb.avif](../../assets/f9b99b43801ccd00.avif)

Both methods of storing Triforce game data have the same goal in the end: deliver a disc image to the internal GameCube. In addition to the GD-ROM or NAND cartridge, each game also has a corresponding security key that must be inserted into the Triforce unit in order for the game to run.

**Type 1, Type 3, and Saving in Arcades**[¶](https://dolphin-emu.org#type-1-type-3-and-saving-in-arcades)

There are two variants of Triforce I/O: Type 1 and Type 3. These refer to the Sega JVS Type 1 and Sega JVS Type 3. JVS stands for [JAMMA Video Standard](https://en.wikipedia.org/wiki/Japan_Amusement_Machine_and_Marketing_Association#Video), a common standard created by a group of Japanese game companies for connecting various accessories and controllers to arcade systems. It's easiest to think of JVS I/O as the arcade equivalent to USB. Other Sega JVS I/O compatible devices can work with the Triforce even if they were originally designed for other arcade platforms, but it's up to the game developers to actually add support for a particular piece of hardware. Type 3 Triforces also have the capability to support more complicated analog input devices.

Whether it was Type 1 or Type 3, Sega had a trick that was instrumental to their efforts to revive the arcade scene and almost *every* Triforce game would use it. It was a revolutionary idea that had taken hold in the home console market but was still rare to see in arcades: saving and continuing.

By using cheap cards that could hold a small amount of data, players could buy what amounted to a small memory card directly from the arcade machine using a built-in vendor. These cards could be bought for as cheap as a single credit in some cases, and had enough storage to save progress, preferences, and other unlocks. Because the data wasn't locked to the machine, these cards allowed the player to continue their progress from any arcade that had the game and a working card slot.

The end goal of this was to get players more invested in arcade experiences by having them progress and unlock content. Some Triforce games are full of so many unlockables that it'd be impossible to see everything in a single session at the arcade.



![magcardfront_thumb.avif](../../assets/6310d1555211815f.avif)



![magcardback_thumb.avif](../../assets/5d24a34144c5e9ba.avif)

If you'd like to read it,

[click here](https://dolphin-emu.org/m/user/blog/triforce/magcardback_rotated.avif).Triforce games can support two types of cards for saving: Magnetic Cards (magcards) and Integrated Circuit (IC) cards. Magcards are cheaper, fragile, and can only survive so many writes before failing. They have the added bonus of having a printable side, where the game can print a player's achievements and more. IC cards are more like old credit cards with a thicker plastic. They weren't printable, but were much sturdier.

A limit of 50 writes was imposed on magcards, likely to recoup printing costs *and* because the cards would eventually wear out. This meant that after 50 writes, the player would have to spend more money on a new card in order to continue saving their data. If an arcade was feeling generous, the operator could choose to make buying and/or refreshing cards free.



![cardcosts_thumb.avif](../../assets/44ce652daa7a7795.avif)

Regardless of the card type, if the card were somehow destroyed outside of the machine for any reason, the save data would be lost and the player would have to start over with a fresh card.

Outside of the various cards and their readers, there were plenty of other fairly generic JVS I/O devices, such as coin mechanisms, arcade sticks, buttons, steering wheels, and pedals. Because there were so few Triforce games released, we'll take a look at unique JVS I/O devices on a game-by-game basis when we start spotlighting the games.

**Bringing the Triforce Home**[¶](https://dolphin-emu.org#bringing-the-triforce-home)

Hypothetically, let's say you have a vested interest in GameCube hardware and decided to purchase a Triforce arcade unit with a game to see how it works first-hand and write an article about it. Without a cabinet and all of the additional hardware that is required to run a game, the core Triforce is just a fancy paperweight, right? Actually, no!

Using a Raspberry Pi, we can convert USB controllers into JVS devices that the games will recognize thanks to JVS I/O emulation! JVS I/O uses a USB-A style connector, but arranges the pins differently. Compared to USB, JVS I/O's differential serial signal is closer to the [RS485](https://en.wikipedia.org/wiki/RS-485) standard (aka the last [serial port](https://en.wikipedia.org/wiki/Serial_port) standard). It's not *exactly the same*, but by using a RS485 adapter connected to through USB-A with D- and D+ hooked up as the differential pair and VBUS hooked to the sense line, USB devices can communicate with JVS I/O. Combine that with [OpenJVS](https://github.com/OpenJVS/OpenJVS), and you can have a computer interface with a Triforce to emulate JVS I/O devices.

In our hypothetical, we suggested that we only purchased one Triforce. In reality, we ended up with *four* over the past few years: A Type 1 DIMM, a Type 3 DIMM, and two Type 3 NANDs. We also bought a few JVS I/O devices that popped up, including a Virtua Striker 4 Card Reader and a Chihiro/Triforce/NAOMI 2 compatible magcard reader/printer/distributor. However, our real JVS I/O devices ended up being pretty useless due to the fact we were still missing too much hardware to hook them up. JVS I/O emulation was mandatory, and was used to fake enough of the devices to get the games into a working state. To replace the Triforce's JVS power supply, we used an ATX power supply with the 20+4 pin power connector carefully modified to match its pinout. Do not attempt this at home!

[OpenJVS](https://github.com/OpenJVS/OpenJVS) does a well enough job faking devices that most Triforce games can be made to run under it. More importantly, it also let us map the various input devices attached to the games to a DS4 controller. As a bonus, we used some of the extra buttons on the controller to map actions like inserting coins to make general play easier.

All of this tinkering was *just enough* to let us control and play real Triforce games on real hardware.



![](../../assets/d34b9bb33213475d.avif)



![triforcehardwareportable_thumb.avif](../../assets/186711c35fed33b1.avif)

Now that we could play Triforce games, we had to give it a spin.

**The Triforce Games**[¶](https://dolphin-emu.org#the-triforce-games)

Given that Nintendo hardware powers the Triforce, one might expect it to have some *Nintendo-developed games*. But there aren't any. Despite Nintendo's pedigree for creating appealing and accessible games, they had no interest in making arcade games for the Triforce. Hits like [Donkey Kong](https://wiki.dolphin-emu.org/index.php?title=Donkey_Kong) and [Mario Bros](https://wiki.dolphin-emu.org/index.php?title=Mario_Bros.) were eons ago and the market had drastically changed since then. Instead, Nintendo opted to license out their IPs to the more experienced arcade developers at Sega and Namco.

This partnership resulted in a golden opportunity for the two companies. Their experienced arcade developers had access to some extremely popular IPs, and the GameCube base meant they had a powerful core machine that was also affordable. In the end, though, the Triforce only had **nine** games released for it and several of those saw home ports.

With so few titles released for the system, it affords us the rare opportunity go through each and every one. The games range from fairly typical arcade titles to high budget monstrosities that would be the crown jewel of any arcade. We'll be looking at obscure games, legendary games, and everything in between while doing our best to see how they took advantage of the Triforce hardware. Let's begin.

[Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) and [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) by Namco[¶](https://dolphin-emu.org#mario-kart-arcade-gp-and-mario-kart-arcade-gp-2-by-namco)

[Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP)

[Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2)

Did you know that the Triforce has not one, but *two* Mario Kart games? [Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) (2005) and [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) (2007) are often forgotten when people talk about the phenomenal Mario Kart series due to their limited release, especially internationally. Both games are built off the [Mario Kart: Double Dash!!](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart:_Double_Dash%E2%80%BC) engine, but have more of a focus on arcade simplicity and play closer to the style of the original [Super Mario Kart](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Kart).

Those that have played a Mario Kart game know what to expect at the surface level. This is an arcade kart racer with tons of wacky items, popular characters, and colorful tracks to race on. This time around, some popular characters from Namco properties join Mario Kart veterans, such as Pac-Man!



![mkagpcab_thumb.avif](../../assets/ebeb3164a6e5c600.avif)

Image Credit:

[NoNameHere](https://commons.wikimedia.org/wiki/File:Mario_Kart_Arcade_GP_cabinet_(cropped).jpg)on Wikimedia Commons ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))The first game launched with twelve race tracks spread across six cups. Each cup has four stages that use two of the tracks. The second time you race a track in the cup, it will be remixed slightly. Sometimes this just means some different visuals or items, but other times it might have some slight alterations to make driving the track more difficult.



![](../../assets/34e02c8d5bf45123.avif)



![mkcoursegraphics2_thumb.avif](../../assets/1782d128722efd21.avif)

[Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) has all of the tracks from the first game and four brand new ones spread out between two new cups. If this was a home console game, the amount of reused content would have been very disappointing. In the arcade setting, it's not nearly as big of a deal. Most players wouldn't have had a lot of experience on every course, and many might not have played the first game at all! That being said, [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) still feels more like an improved *version 2.0* rather than a full fledged sequel.

On that note, [Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) has some very puzzling omissions that were fixed by the sequel. For instance? Only [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) has the iconic 50cc, 100cc, and 150cc difficulty options available from the start! Both games have the same three gameplay modes: Grand Prix, Time Trial, and Versus. Grand Prix has players racing through cups one round at a time. By winning a race in a cup, you unlock the next race. Time Trial should be familiar to anyone. Players are given a triple mushroom and a solo run on a course to set the best time possible. Versus mode can only happen in multicabinet setups when multiple players are around. In this mode, up to four players can race one another on any track.

Regardless of mode, races have a time limit to keep people moving, but they are relaxed enough that they usually won't come into play.

In order to record progress, [Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) and [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) rely on magcards. When the game starts, it'll ask the player to insert or create a license profile to save their progress. On some cabinets, a camera (known as the "namcam2") will be present to take a picture that will be used during the race. Players' faces will show up in the heads-up display and with various *distraction items*, so making a goofy face could be an advantage in multiplayer. Note that these features are optional, and a player can always choose to play without taking a picture or using a magcard.



![gpcamera_thumb.avif](../../assets/08833d3401a8ecf6.avif)

There is one rather egregious oversight that is only present in the first game. [Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) **locks a player to a single character once they've created a license card**. That means before the player even gets a chance to play the game, they have to choose a character and are forced to use that character unless they start over! Characters have different driving characteristics, so this is a rather important decision!

Regardless, the developers must have realized how awkward this was and changed it so that swapping characters is possible in [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) even when using a magcard.

Whether the driving model for a Mario Kart game is good or not mostly comes down to player preference. Some players love Mario Kart DS, others swear by [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii), or even [Double Dash](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart:_Double_Dash%E2%80%BC). The GP games are definitely on the slippery side of the series, especially when using the "difficult" characters at higher CCs.

Controls are simple even compared to the already casual home Mario Kart games. The game uses a racing wheel, gas and brake pedals, and an item button. Additionally, there's a *Versus Cancel* to opt out of multiplayer to focus on winning the cups. Despite this, it takes some time to get acclimated to the arcade exclusives after coming from modern Mario Kart games. The harder courses pull no punches and will relentlessly throw tight corners. The Grand Prix mode even has hindrances added to certain tracks on their reruns. On Bowser's Castle, Kamek invades and blocks some of the racing lines on the later laps!



![bowsercastlebeforeintrusion_thumb.avif](../../assets/dff1f2cecce760be.avif)



![bowsercastleafterkamekintrusion_thumb.avif](../../assets/292b1c31da4a8b12.avif)

To win on harder difficulties, the player needs every advantage they can get. Items can be the advantage that players need. Both games feature **over 100 items**, but during a race, each player has access to a pool of three items. In harder Grand Prix cups (and sometimes later stages in earlier ones), players get the option to create their own unique item pool from their unlocked items. Even though a lot of them share properties, a surprising number of them have their own wrinkles. For example, dropping a banana can cause a spinout and immediate time loss, but dropping tacks will cause a kart to pop a tire and lean to one side, making overall driving temporarily more difficult for that player. Items aren't very balanced so unlocking powerful items gives an undeniable edge.

Throwing items are simple. Aside from the green shell, almost all forward throwing items feature a powerful lock-on effect. Lock-on is automatic and happens after keeping another driver in front for a couple of seconds. Once locked on, that item will head toward the target regardless of what they do to avoid it.



![](../../assets/6c2961b5dfbfcca0.png)



![mkitemteaser_thumb.avif](../../assets/c6fed10d2709cd6c.avif)

In the first game, players must win all four stages of a cup and the minigame that follows. These minigames are short solo challenges that test a player's control over the game in unusual situations. Sometimes this means pushing an object, getting big air over jumps, driving backwards, hitting tons of pedestrians (they're Koopa Troopas, that makes it OK), or even facing off with Bowser outside of his castle. In the sequel, the bonus games are no longer required for cup completion and only award bonus coins.



![mkbonusgame_thumb.avif](../../assets/74e737c69498d655.avif)

[Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP): the Invincibility Star!

By winning all of the cups, players unlock a *Special* mode that varies per game. In GP 1, that is 150cc mode. [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) has 150cc mode unlocked by default, so they went a different direction. Instead, players unlock new track layouts in *reverse mode*. Unlike the *mirror mode* present in other games, reverse mode significantly changes some of the tracks beyond just ruining muscle memory. Fun fact, reverse mode *was* also planned for [Mario Kart: Double Dash!!](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart:_Double_Dash%E2%80%BC) before being cut for mirror mode.

To handle the plethora of tricky corners and tracks, GP games have a drifting mechanic. By tapping the brake, players can initiate a hop. By turning in the air before landing, players can initiate a drift that allows sharp corners to be taken at higher speeds. Because of the powerful lock-on that most items have, drifting has been given an additional benefit. During a drift, players will *reflect* most items with a shield. An unexpected drift will cost some time, but could be used to block an item at the last moment. Some items also provide a shield, such as the *Invincibility Star* and *Shield* items.

Much like the original [Super Mario Kart](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Kart) and more recent Mario Kart entries, the GP games have coins strewn across the track. Collecting coins increases a kart's stop speed, adding a layer of strategy as just driving the optimal lines isn't enough. During a race, holding 15 coins pushes a kart to its maximum speed. But driving at that speed can also be dangerous, as hitting walls, bouncing off other karts, or being hit by items can cause the player to lose coins.

[Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) changes all of the coins on the track to *Mario Coins*. The first time these coins are collected they count as currency toward unlocks. If coins are dropped, players don't lose the Mario Coins and they will respawn as golden coins. Up to 25 Mario Coins can be picked up on the track along with bonuses from race ranking and minigames.

Collecting Mario Coins allows for unlocking certain karts, items, portraits, and *kart upgrades* that will make the veteran players much faster than players just starting out.



![mariocoinreward_thumb.avif](../../assets/11e415c5c44b7ace.avif)

[Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP2), minigames now just give bonus Mario Coins and are no longer required to complete a cup.

Lastly, [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) also adds one more major feature: ~~Waluigi!~~ a "live" announcer that gives updates throughout the race. This feature is proudly demonstrated during the attract menu, even! As corny as it sounds, it's rather entertaining to leave on at least a few times. Players that don't want the announcer can turn it off and their preference will be saved to their magcard.

Overall, both of these games are best as multiplayer arcade spectacles. The depth and content of these games don't quite rival contemporary home releases like [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii). But none of that matters in the arcade with friends, where loud and bombastic multiplayer experiences really shine.

The Mario Kart Arcade GP series would continue with [Mario Kart Arcade GP DX](https://www.mariowiki.com/Mario_Kart_Arcade_GP_DX) in 2013 and [Mario Kart Arcade GP VR](https://www.mariowiki.com/Mario_Kart_Arcade_GP_VR) in 2017, but those would run on newer and more standard PC-based arcade hardware.

These Mario Kart titles were the only two games Namco released on the Triforce hardware. But they had planned *at least* one other game.

**Star Fox** (working title, unreleased) by Namco[¶](https://dolphin-emu.org#star-fox-working-title-unreleased-by-namco)

Announced in 2002 as a dual GameCube and arcade release, Star Fox was originally planned to launch before either of the Mario Kart Arcade GP games in 2003. As part of a push for games that could easily be ported between GameCube and arcade, Star Fox would have had connectivity between the two versions through *GameCube memory card slots* included on the machines. That way, players could bring their own memory cards to transfer progress and/or unlockables between the home version and the arcade version of the game.

Considering the arcade style action featured in Star Fox and Star Fox 64, this seemed like a natural choice for an arcade hit. Players were already chasing high scores in Star Fox 64 and the overall game design would need little modification to work in an arcade. If rumors were true, Namco wasn't planning to skimp on the hardware, either. They were going to use the massively impressive and incredibly expensive [O.R.B.S. cabinet](https://kotaku.com/the-greatest-arcade-cabinet-that-never-was-5849339), which was designed specifically for on-rail shooters. Essentially, the player would be locked in a fully immersive orb that would place them squarely in the cockpit of an Arwing with a semi-spherical screen acting as a bubble canopy. On top of that, the cabinet could rotate and slide to reflect what was going on in-game.

Unfortunately, Star Fox Arcade [was quietly cancelled](https://lostmediawiki.com/Star_Fox_Arcade_(lost_build_of_cancelled_arcade_port_of_GameCube_rail-shooter_%22Star_Fox:_Assault%22;_2002)) and the O.R.B.S. cabinet itself would never actually be used for any arcade game. The GameCube version did *eventually* see the light of day, however. Released as [Star Fox Assault](https://wiki.dolphin-emu.org/index.php?title=Star_Fox:_Assault) in **2005**, the game was heavily reworked and padded out with third person on foot sections. Perhaps as a nod to its origins, players can unlock a port of the arcade classic [Xevious](https://wiki.dolphin-emu.org/index.php?title=Xevious_(Arcade)) by collecting all silver medals.

With that side quest complete, we've now covered the entirety of Namco's contributions to the Triforce library. Thankfully, we're not done yet, as Sega developed a variety of Triforce arcade games.

[Gekitou Pro Yakyuu](https://wiki.dolphin-emu.org/index.php?title=Gekit%C5%8D_Pro_Yaky%C5%AB_(Triforce)) is a rather unique baseball game that combines characters from various baseball manga created by [Shinji Mizushima](https://en.wikipedia.org/wiki/Shinji_Mizushima) with real-life Japanese professional baseball players of the era. The game also has a faithful home console port, [Gekitou Pro Yakyuu](https://wiki.dolphin-emu.org/index.php?title=Gekit%C5%8D_Pro_Yaky%C5%AB_(GC)), for the GameCube and PlayStation 2.

The main draw of this baseball game is that it can provide a faithful simulation style game between professional players or a zany arcade experience with special pitches, strong batters, and manga cutaways featuring the illustrated characters. What makes the game so interesting is that these two things aren't separated - both teams can be filled with a mix of illustrated and professional players, letting their contrasting styles clash right on the field.



![](../../assets/e6cc1752f7792d40.avif)



![gekitohomerun_thumb.avif](../../assets/98a07e7e79dc8802.avif)

At its core, [Gekitou Pro Yakyuu](https://wiki.dolphin-emu.org/index.php?title=Gekit%C5%8D_Pro_Yaky%C5%AB_(Triforce)) is a fairly standard late early 2000s baseball game. Pitchers can roughly place their pitches anywhere in and around the strike zone and batters in turn try to guess where the pitch will be to get a solid hit. Pitchers have a variety of pitches at their disposal that add movement to the ball, and batters in turn have multiple swing types that can counter pitches. Players with better stats generally have more options at their disposal. If the batter guesses the pitch right, their aiming reticle will turn red giving them advanced warning that they guessed correctly.

When playing in the arcade, both teams are filled with a mix of real players and manga players. This creates the interesting scenario where many manga players often feel like *superstars* that can break the game if not carefully played around. Most of them have special quirks and often have access to special abilities. Manga pitchers can make the ball disappear, zig zag, and confound the batter. Manga batters can also counter this as they have active and passive abilities of their own. One player has his contact range and power grow further out from the center of the strike zone, making him incredibly powerful if the pitcher is painting the corners.

For those interested in playing this game without a Triforce, there's good news. The home console port is incredibly faithful and even adds some additional modes and features for depth. The GameCube controller also affords players analog control, whereas the arcade original uses an eight-way gate. Once you get in game, though, it's very apparent that this is the same game.



![](../../assets/33112ee04d87637a.avif)

[blood type](https://en.wikipedia.org/wiki/Blood_type_personality_theory)and more in the surprisingly robust player creation tool. This feature is exclusive to the home console versions.

The home port, as far as we could tell, is missing *one small thing*. The Triforce version has a scoring system for putting up high scores on the machine. Rather than just trying to win baseball games, players are instead challenged to get a high score across a nine-inning game. Doing positive things like getting hits and getting the opponent out will give the player points. Big moments like double plays and grand slams will give even bigger bonuses, pushing players to the top of the leaderboards.

Players get two innings per credit or can pay 4 credits for a full nine-inning game. Players aiming for a high score *need* to do that, as those extra innings give more opportunities for scoring points, and there's a large swath of bonus points for winning the baseball game outright. After nine-innings, win or lose, the game ends. The game also lists high scores for a home run contest, but we couldn't figure out how to get to that mode.

This game suggests that it has some kind of save card support in the Service Menu, but we weren't able to find any cards for it to be sure. In all likelihood, cards would have been used to save team data and other preferences for a player. Overall, [Gekitou Pro Yakyuu](https://wiki.dolphin-emu.org/index.php?title=Gekit%C5%8D_Pro_Yaky%C5%AB_(Triforce)) is an effective, if not somewhat simple baseball game that lends itself well to the pick up and play nature of the arcade.

While it was developed by a different team within Sega, [Virtua Striker 3 ver. 2002](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_2002) is very similar to [Gekito Pro Yakyuu](https://wiki.dolphin-emu.org/index.php?title=Gekit%C5%8D_Pro_Yaky%C5%AB_(Triforce)) in some ways. It is a simple to pick up and easy to play sports game with an incredibly faithful home port that brings the same experience to console players with modes that add extra depth. [Virtua Striker 3 ver. 2002](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_2002) is a three-button game: short pass (tackle on defense), long pass, and shoot. That's it.



![](../../assets/bdfb44a54e4bd5de.avif)



![virtuastrikerscrum_thumb.avif](../../assets/c50efde0d8fcf437.avif)

The * gooooooal* of the game is to win five matches in a row against the AI to secure the championship while surviving potential intruders jumping in from the second player in standard mode. This is a

*king of the hill*style arcade game, so whoever wins gets to keep playing while the loser is knocked out. This remains true when playing against AI, so a strong player can play up to five games against the AI before reaching the credits and having to put in more money.

The game follows the rules of ~~football~~ soccer closely. There are yellow cards, red cards, offsides, corner kicks, penalty kicks, free kicks and injury time. As an arcade game, it even captures some of the pageantry of the sport with a bombastic opening as the players march onto the field. However, once you're in game it is a very no frills experience.

The arcade operator could adjust the cabinet's settings to make things more or less unfair to optimize their profits. In addition to difficulty settings, Golden Goal (short overtime period) and Penalty Kicks could be disabled to give the players less opportunities to break a tie. And this matters a lot, because *the AI wins in the event of a tie*, forcing the player to plunk in more money to continue.

For competitive events and tournaments, there's an aptly named *tournament mode* present in the settings. This mode has both players kicked off the game after match, regardless of who wins. This mode wasn't (just) added to allow the operator to maximize profits, but rather it was intended for holding in-person tournaments where players would be swapping in and out after every match.

The simplicity to the controls is both the game's selling point and an annoyance. When on defense in particular, sometimes the defender will rush to get into a particular position regardless of the direction being held on the arcade stick. This lack of control is only worsened by the fact that there's no switch player button... on the arcade version, at least. The home port is mostly faithful gameplay-wise, but it does take advantage of the extra buttons on the controller to give players the ability to change tactics and swap defenders.

One thing that we should mention is that we were playing on revision 0001 of [Virtua Striker 3 ver. 2002](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_2002). Most games on the Triforce have multiple revisions or updates, with some revisions coming with significant upgrades. Later revisions may have addressed problems in this revisions, especially if the supposed *Type 3* version exists.

[Virtua Striker 3 ver. 2002](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_2002) was a tad underwhelming in our opinion. If you're a huge fan of these games and are seething at our mini-review, we're fully aware that a lot of our frustrations might simply boil down to a * skill issue*. But since we were familiar with the rich history of the veterans at

[Amusement Vision](https://wiki.dolphin-emu.org/index.php?title=Category:Amusement_Vision_(Developer))and their legendary track record of arcade games, this one was a little disappointing.

[The Key of Avalon: The Wizard Master](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master), [The Key of Avalon 2: Eutaxy Commandment](https://wiki.dolphin-emu.org/index.php?title=The_Key_Of_Avalon_2:_Eutaxy_Commandment), and their subversions by [Hitmaker (Sega AM3)](https://wiki.dolphin-emu.org/index.php?title=Category:Hitmaker_(Developer))[¶](https://dolphin-emu.org#the-key-of-avalon-the-wizard-master-the-key-of-avalon-2-eutaxy-commandment-and-their-subversions-by-hitmaker-sega-am3)

[The Key of Avalon: The Wizard Master](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master)

[The Key of Avalon 2: Eutaxy Commandment](https://wiki.dolphin-emu.org/index.php?title=The_Key_Of_Avalon_2:_Eutaxy_Commandment)

Originally released in 2003, [The Key of Avalon: The Wizard Master](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master) is a strange and very, *very* expensive arcade game. This game was not just expensive for the players, but it was also expensive for the operator too! This game is powered by **five** Triforce cabinets: one central Triforce server for the main game screen, and four additional satellite Triforce pedestals for the players.

[The Key of Avalon: The Wizard Master](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master) is an arcade trading card board game. The objective of the game is simple - players scan in their decks and see their monsters on the big screen while battling up to three other players for supremacy.

Before playing the game, players need to purchase a starter deck of 30 random trading cards. This deck also comes with an IC card so that players can save their progress. Each satellite Triforce comes with a deck reader to allow a player to scan in their deck of cards. But how would you control the game after scanning in your cards? Why, a *touchscreen*, of course! And if that wasn't enough, the game also came with a separate card kiosk specifically for purchasing starter decks and booster packs.

There are at least six revisions of The Key of Avalon. It is important to be aware of what revision a cabinet is, as cards from newer sets will not work with older revisions. Thankfully, cards are marked with what set they came from, making it fairly easy to know which revisions each card is compatible with.

- Supports the initial 100 cards. There is a 1.10 revision with small adjustments.[The Key of Avalon: The Wizard Master](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master)This first[The Key of Avalon 1.20: Summon The New Monsters](https://wiki.dolphin-emu.org/index.php?title=The_Key_Of_Avalon_Ver.1.20:_Summon_The_New_Monsters):*major*update adds support for 52 new cards in the**N**series. Earlier prints of these cards may have different stats and are missing some information on the back of the card.



![cardrevisions_thumb.avif](../../assets/6b427f3757fdcf61.avif)

This version adds support for 35 more cards in the[The Key of Avalon 1.30: Chaotic Sabbat](https://wiki.dolphin-emu.org/index.php?title=The_Key_Of_Avalon_1.30:_Chaotic_Sabbat):**C**series. Much like Summon The New Monsters, reprints of these cards have additional information and may have slightly different stats.An update big enough to be called a sequel. It has 61 new cards, a single player mode, and much more. The cards for this revision are in the[The Key of Avalon 2: Eutaxy Commandment](https://wiki.dolphin-emu.org/index.php?title=The_Key_Of_Avalon_2:_Eutaxy_Commandment):**E**series. These cards do not appear to have any changes between early and late prints. The updated stats for older cards are used by this game.The final revision adds support for 40 new cards in the[The Key of Avalon 2.5: War of the Key](https://wiki.dolphin-emu.org/index.php?title=The_Key_Of_Avalon_2.5:_War_of_the_Key):**W**series. There are also additional**Legend**cards separate from the main catalogue.

In the end, nearly 300 total cards were released spread out over five rarities: Common, Uncommon, Rare, Very Rare, and Super Rare. Some cards are undoubtedly stronger than others, and those cards are mostly the rarer ones.

Like other collectable card games, players were expected to buy packs and trade with others to build the best possible deck. To prevent someone from getting clever with a printer and suddenly owning all the rare cards, Avalon cards have a barcode embedded into their top edge that the game reads the card data from. Though nearly invisible in normal circumstances, if held up to a light *just right*, the material of the barcode stands out against the rest of the card.

Cards weren't all about utility, though. These cards were beautifully illustrated by a myriad of artists, and each monster is represented by a detailed 3D model in game. If someone was lucky, they might've stumbled upon alternate art or holofoil versions of cards. Players could also be rewarded with unique **Ex** cards that were **only** distributed through events.



![hollowfoil_thumb.avif](../../assets/0b3b372c419fa12e.avif)

Of all of the Triforce games, this was the only one we couldn't play. Even if we had five Triforces, five GD-ROM drives, and JVS I/O emulation for the cards, it still wouldn't be enough. The game can be booted with fewer Triforces, but the touchscreen is a total mystery and there was no way to bypass it without having a working Avalon Satellite Pedestal.



![avalontitle_thumb.avif](../../assets/0d5770b9fcbcd77a.avif)



![avaloncutscene_thumb.avif](../../assets/50eef3568a8face1.avif)

We've researched the game, bought manuals, and obtained a ton of cards and understand the gameflow, but without having played it we can't really say if it's fun or not. However, based on [existing sales data](https://www.gamesindustry.biz/sega-profits-rise-as-console-game-division-approaches-break-even) and the number of updates, we know that [The Key of Avalon](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master) was moderately successful despite its high price. Sega would go on to make more trading card arcade games, including a suspiciously similar Chihiro game, [Quest of D](https://en.wikipedia.org/wiki/Quest_of_D).

Two years after [Virtua Striker 3 ver. 2002](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_2002), Sega released the next game in the Virtua Striker lineup with [Virtua Striker 4](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4). With dramatic upgrades to the controls, support for saving progress, team configuration, rank, and more, this game is often considered the best in the series by fans. And it only got better with [Virtua Striker 4 ver.2006](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4:Ver._2006), which updated the rosters and added additional online events.



![vs4layout_thumb.avif](../../assets/7aa00ad6f8ae1d77.avif)



![vs4cab_thumb.avif](../../assets/6ff902b330096969.avif)

Image Credit:

[Launchbox](https://gamesdb.launchbox-app.com/games/images/88412-virtua-striker-4)Like most Triforce games, the newer Virtua Striker games take advantage of cards for saving. [Virtua Striker 4](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4) uses IC cards to track player progress, similar to [The Key of Avalon](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master). These cards are nifty, as not only are they more durable than magcards, but they also contain an ID for logging in to ** Sega ALL.Net**. The internet was enough of a thing at this point that Sega started experimenting with it for tracking player data and progress.

This meant that instead of a local arcade leaderboard, [Virtua Striker 4](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4) could have a global leaderboard tracking players on ALL.Net-connected machines across the world. By playing against other players that had registered online, players could be promoted to higher ranks or be demoted to lower ranks. On the surface, this is an upgrade over traditional magcards, but the obvious downside is that these games rely on servers hosted by Sega. Unfortunately, support for these machines ended in 2017, meaning that the online features no longer work. Thankfully, these games can still be played offline without the online services, albeit without the special features and events.

[Virtua Striker 4](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4) was a revelation to play after the previous games. The changes are subtle, but they come together to provide a far superior experience. The ability to dash gives players much more control over attacking at the expense of stamina, and helps avoid the common problem in [Virtua Striker 3](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_2002) where athletes were constantly just banging into each other in a scrum. The *change tactics* buttons add depth as players can adjust their strategy on the fly instead of waiting for halftime. This gives the opportunity to go for that golden goal in the final seconds or play defensively to hold a tight lead.

Instead of being locked to an eight-way gate, this game uses a full analog lever that allows for more precise control. Player movement is still a little stiff, but it makes a world of difference when it comes to the accuracy of shots and passes.



![vs42006goal_thumb.avif](../../assets/258fea37f442f0d6.avif)



![vs42006victory_thumb.avif](https://dolphin-emu.org/m/user/blog/triforce/vs42006victory_thumb.avif)

For most fans of the series, [Virtua Striker 4 ver.2006](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4:Ver._2006) is the definitive version in the series, and we can see why. Unfortunately, it is also the last game in the series and it never saw a home console port.

If there was a crown jewel of the Triforce efforts, it has to be [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) and the home console game born from it, [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX). Without Nintendo collaborating with Sega, there's no way that the legendary arcade racing devs at [Amusement Vision](https://wiki.dolphin-emu.org/index.php?title=Category:Amusement_Vision_(Developer)) would have had the chance to work with the F-Zero license.

For those out of the loop, [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX) is renowned as one of the greatest arcade-style racing games ever made. It has tight controls, an incredible sense of speed, and legendary difficulty. The racing alone would make for a great game, but the developers went above and beyond with tons of content to elevate the experience. It has tons of characters with their own 3D models, F-Zero machines, and even theme songs accompanying their profiles. The garage functionality also gives players the ability to create their own vehicles with a custom appearance and stats. Topping all of that off is an iconic and difficult story mode full of goofy FMV cutscenes oozing cheesy goodness. And for those who never had a chance to play the *arcade-exclusive* tracks, the arcade tracks can actually be unlocked in [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX)!

So that's it then? [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX) has everything the arcade could offer and more. There's no reason to care about [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX), right? **Wrong**.



![](../../assets/a38f3e9595689f0c.webp)

Image Credit:

[gztomy.com](https://www.gztomy.com/products/refurbished-f-zero-ax-tomy-arcade)[F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) is still an incredible experience even for those that have completely mastered [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX). The controls and physics have been adjusted to make the game play better on a force feedback yoke and pedals. The change in controls allows players to *push* the vehicle in ways that are lost in the home console version. And, if you're lucky enough to find a deluxe cabinet, the intensity is ramped up further with pilot seat haptics - it can tilt to throw the player around corners.

The game is a visceral thrill. Everything great about the racing in [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX) is here, just with the intensity cranked up to another level. Unfortunately, it only has six tracks, with one of them being a fairly simple oval for learning the game. The other tracks are fantastic visual showcases with devious layouts. The long ice slide at the end of Green Plant: Spiral pushes players to go fast as they can with no traction, while the back-to-back right angle turns and thin straightaways force precision driving on Lighting: Thunder Road.

There are only two modes in this game: Race and Time Trial. Race has players going up against 29 other AI opponents or three other players if playing against linked cabinets. Time Trial is exactly what it sounds like and has players racing for the best time in a solo effort. Best records could be uploaded online with a code, back in the day.



![trackselect_thumb.avif](../../assets/e0c1a99013a860a5.avif)

Hidden away in the Service Menu, there are five difficulty modes to help the operator tune the experience according to the clients. In a more casual arcade, the game's difficulty could be lowered to *Very Easy* to give players more time to make mistakes and still win. If they wanted people to suffer, *Hardest* all but guarantees no one will ever win. The length of the races can also be adjusted. Even a standard three lap race can be exhausting on a cabinet, so cranking up the length can really turn the game into an endurance challenge.



![evilarcade_thumb.avif](../../assets/f3d352f83bf973e2.avif)

On the track, [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) looks like [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX). But after having the opportunity to play them back to back, the differences in how they drive became very apparent. Even ignoring the arcade atmosphere, AX gives the sensation of always being one mistake from careening out of control. After playing a lot of [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) and returning to GX, the change in feel was shocking. Treacherous turns in AX were suddenly ordinary in GX thanks what feels like higher grip and different drifting physics. The cars felt like they were glued to the track in the console version!

After spending a lot of time with both, AX definitely presents a more difficult, but rewarding to master, driving model. The arcade game *does* grant players some reprieve though. Running out of energy or flying off the track will happen now and then even to the most experienced players. This is *not* an immediate race over! Instead players will be respawned back on the track after a small time penalty. It dampens the hopes of victory, but it's usually possible to come back from one major mistake. However, unlike the console version, players are on a strict time limit by default. Once the clock hits zero, the race is over regardless of whether the player is in first or last place.



![f-zeroaxporttown_thumb.avif](../../assets/97c6f24cabd5c700.avif)



![f-zeroaxpodium_thumb.avif](../../assets/a56894aca0bc220a.avif)

Both magcards and GameCube memory cards can be used to save progress. Players are assigned a license rating that can be upgraded by winning races and earning points. Every 30,000 points, players are afforded an opportunity to buy upgrades for their own custom F-Zero Machine. This machine could be used directly in [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) or transferred to [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX) via memory card.

To beat [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX), players have to win all six races and all six target times. While doing this, players earn points that upgrade their license's rank, which allows them access to better parts for their custom F-Zero machine.

After experiencing it first hand, we can say that the game is a truly incredible arcade experience. If not for [F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX), it would be a modern tragedy that it didn't see a wider release. Still, those who love the F-Zero series should definitely give this version of the game a spin if they have the chance.

**Monster Ride**[¶](https://dolphin-emu.org#monster-ride)

It would be a crime if we didn't at least mention *Monster Ride*.

[F-Zero AX: Monster Ride](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) is a separate release of F-Zero AX and the only Sega-produced Triforce game that uses a NAND cartridge. It has fewer features, pilots, and ships than the standard version of F-Zero AX, and doesn't seem to have multiplayer or any save support whatsoever.

But in exchange, Monster Ride runs in a [Cycraft](https://segaretro.org/Cycraft) cabinet.

Imagine playing F-Zero AX inside a five degrees of freedom **motion simulator** where the player's cockpit is suspended in the air with an arm, and the cabinet literally swings the cockpit around to match the ship's movement in game. That's Monster Ride, and it's as awesome as it sounds. Unfortunately, these cabinets are *incredibly* rare and appear to have never left Japan. We invite readers to watch this clip showing it off, as this is as close as most of us will ever get to the real thing.

In most cases, something this obscure would be lost to time. But, luckily enough, a few Monster Ride Triforces have survived over the years. And thanks to [Cycraft emulation](https://github.com/bobbydilley/cycraft-emulator), Monster Ride can technically be run from a standard Type 3 NAND Triforce. Maybe some day all of this could be hooked up to a homemade Cycraft-compatible motion simulator and Monster Ride will live again. We can dream, right?

**In Retrospect**[¶](https://dolphin-emu.org#in-retrospect)

After having played each and every Triforce game to the best of our ability, it's easy to see why the platform is still beloved by its fans. Unfortunately, it was a victim of its era and most games only released in Japan. The games that did get international releases were only released in limited quantities.

As developers of a GameCube and Wii emulator, the Triforce is an especially interesting topic for us. At the core of every Triforce is a GameCube, yet that familiar hardware was used to drive a different type of experience in the arcades. It's fascinating! For this article, we wanted to shine a spotlight on this interesting step-sibling to the consoles we emulate.

Unfortunately, when it comes to emulation, arcade hardware is a very, very different challenge than emulating a home console. Even though each game is powered by a Triforce, all of the hardware around it can be unique for each game and even behave differently on different revisions of the same game! An arcade cabinet only needs to be compatible with the specific game inside of it. Because of that, unlike GameCube/Wii emulation, where fixing one game can sometimes fix dozens of others, each individual *revision* of an arcade game needs to be treated as its own challenge.

Those problems didn't stop people from trying to build Triforce emulation on top of Dolphin in the past, though! **Over 17 years ago**, [Dolphin gained the ability to emulate parts of the Triforce Baseboard](https://github.com/dolphin-emu/dolphin/commit/93b83f8d65962a10a2776bf9fb6c39ce1eb03f2d). It wasn't enough to boot any Triforce games, but it was a start. However, that was the last time anything Triforce-related hit our mainline builds. Aside from code clean up efforts, the fledgling Baseboard emulation was left untouched [until it was removed in the summer of 2016](https://dolphin-emu.org/blog/2016/09/01/dolphin-progress-report-august-2016/) to avoid misleading users into thinking that mainline Dolphin targeted Triforce hardware.

Just because Triforce emulation wasn't progressing in the main builds doesn't mean it wasn't being pursued, though. Instead, efforts were moved to a dedicated *Triforce branch*, where developers could do whatever they wanted to improve Triforce emulation. And there was some success from this approach - it was eventually able to play a few games, such as [Mario Kart Arcade GP 1](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) and [2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2).

However, a lot of this progress was achieved through **brute force**. Because so little was understood about how the Triforce worked, many *suboptimal* techniques were used to get results fast, like hacking problematic behaviors out of games and hardcoding responses. This, combined with some magic to force each game's controls to work with a standard GameCube controller, was enough to get some games running.

This was fine for a separate branch. Hacky emulation is sometimes a necessary first step to more accurate emulation, after all. But on the other hand, the hacky nature of the Triforce branch made it unacceptable to be merged into mainline builds as-is, despite its achievements. Unfortunately, the emulation quality never improved and progress stalled out. The Triforce branch was abandoned after just two years of sporadic contributions, and it eventually faded into obscurity.

Any attempt at Triforce emulation today must be held to a higher standard. It wouldn't need to be perfect at first, but the goal should be to actually *emulate* Triforce hardware, rather than to ignore that it exists. We should strive to give retro and arcade enthusiasts the tools to bring Triforce games to life with their own custom solutions for the platform's assortment of obscure hardware. In a perfect world, Dolphin would be capable enough to be the core of hobbyist arcade cabinets.

Each Triforce game brings difficult questions that Dolphin just isn't well suited to answer. Dolphin is a console emulator at heart and is not designed to tackle the hyper-specific challenges that come with arcade emulation. We already have enough problems trying to emulate all the weird [Wii Remote attachments](https://web.archive.org/web/20080530194734/http://www.siliconera.com/2007/01/23/introducing-the-densha-de-go-wii-controller/) and [USB devices](https://dolphin-emu.org/blog/2025/06/04/dolphin-progress-report-release-2506/#2503-270-disguise-rock-band-playstation-usb-devices-as-wii-equivalents-by-josjuice) out there! To do right by the Triforce would take an inordinate amount of work and expertise. And embarking on that journey for what amounts to a handful of games, many of which already saw very faithful home ports, would be a foolish endeavor at best.

Having said all of that, we're just as surprised as you to be announcing this...

**The Return of the Triforce**[¶](https://dolphin-emu.org#the-return-of-the-triforce)

**As of Dolphin 2512-395, Triforce support is here!** Readers that have been paying close attention might have noticed that some of the screenshots in this article are suspiciously high resolution. There's a reason for that!

*Every single in-game screenshot in this article comes from Dolphin!*

This is the culmination of over a decade of work. While were focused on advancing GameCube and Wii emulation, [crediar](https://github.com/crediar) doubled down and continued maintaining his own fork *specifically for* Triforce emulation. We were aware of this fork, but given the fact that we knew little about how the Triforce worked and had bad memories of the old, hacky Triforce branch, it mostly flew under our radar.

Everything changed mid-2025 when [crediar](https://github.com/crediar) contacted us about potentially making a pull request to get his Triforce emulation code into our official builds. Developers had a mixture of both excitement and concern upon hearing about this. It would be a major project, and [crediar](https://github.com/crediar)'s solo work would now be scrutinized by a bunch of people.

In the end, what won us over was the quality of emulation. The games ran beautifully, and apart from missing touchscreen support for The Key of Avalon, each game was playable. The hacky, messy Triforce emulation we remembered was gone, and something much better had taken its place.

So, we wanted Triforce emulation in Dolphin, and [crediar](https://github.com/crediar) wanted to bring it into Dolphin. Their pull request was an easy merge, right? Well, there was still one big hurdle in the way: *code review*.





![work.avif](../../assets/b277332f131cc886.avif)

Because the Triforce has a significant amount of bespoke hardware, none of the developers reviewing the code knew much about how it worked. We were put into a tough spot of having to review a large volume of code that emulated unfamiliar devices. The Triforce was mostly a black box to us at the beginning of this effort, and it still is in many ways.

To get Triforce emulation to the finish line, we had to work together and make *a lot* of compromises. We did not want to let perfect be the enemy of good, but it still had to be good enough to not hinder further development. [Billiard](https://github.com/jordan-woyak) and [sepalani](https://github.com/sepalani) gave huge assists with their own fixes and clean ups to help get the Triforce pull request ready for action. Many of our targeted clean ups focused on fixing [memory safety](https://en.wikipedia.org/wiki/Memory_safety) bugs, removing potential game hangs, and improving the overall user experience by adding safeguards and streamlining the process of configuring Dolphin to run Triforce games. After many months of review, cleanups, and testing within the team and the community, Triforce emulation is finally here. And it is here to stay.

Throughout this process, [crediar](https://github.com/crediar) has been helping us with his knowledge on the Triforce for various guides and information. He also assisted us with dumping Triforce games and provided a homebrew payload that can dump Triforce games directly over the network. It is also possible to dump GD-ROM titles without any Triforce hardware by using a PC disc drive, but it is a more complicated process and takes several steps in order to retrieve the game from the disc.

For full instructions on how to dump Triforce games, please visit [the game dumping guide on our wiki](https://wiki.dolphin-emu.org/index.php?title=Ripping_Games).

**Setting up Dolphin for Triforce Emulation**[¶](https://dolphin-emu.org#setting-up-dolphin-for-triforce-emulation)

The Triforce is ultimately a GameCube with arcade bits attached to it. Much like how Dolphin can automatically reconfigure itself depending on if you're booting a GameCube or Wii game, Dolphin will now become a *Triforce* when it detects a Triforce game being loaded. However, the Triforce Baseboard options can also be manually enabled for homebrew purposes, and there are some important settings in its configuration menus.

The Triforce Baseboard can be found as a SP1 device in Options -> Configuration -> GameCube. It has additional configuration options for various IP address redirects, which can make it easier to set up networking features of the Triforce. There's also a shortcut here to configure Triforce controls, which can also be found as a GameCube Controller Input device in Options -> Controller Settings.

Each game's arcade controls have already been roughly adapted to a GameCube controller, but be sure to configure the Coin, Service, and Test buttons! Controller port 2 can optionally be set to a baseboard as well, but Dolphin will automatically translate controls when possible without this being necessary. These are the only two places where Triforce settings need to be adjusted in Dolphin. Note that standard GameCube/Wii games should not be booted with the Baseboard set in SP1 or as a controller.



![baseboard1_thumb.avif](../../assets/ab825cf99b0a797c.avif)



![baseboard2_thumb.avif](../../assets/d364168978bf8199.avif)

One other important component of the Triforce is **Segaboot**. Without Segaboot, players can't access the Service Menu and the game's settings. This means not being able to enable free play, change difficulties, calibrate controllers, and much more. Additionally, the full boot process can only be experienced by providing a Triforce IPL *and* Segaboot combined with "Skip Main Menu". Just be prepared for a few error popups along the way as some parts of initialization are not fully emulated.

Segaboot can be found on certain Triforce update discs or in [Virtua Striker 4](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4) and [Virtua Striker 4 ver.2006](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4:Ver._2006)'s files. You can use Dolphin's filesystem explorer to locate the "firm" folder that holds Segaboot files. The correct file is 2MB, and in the case of [Virtua Striker 4 ver.2006](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4:Ver._2006), it is named `segaboot.img01`

. Renaming this file `segaboot.gcm`

and placing it in the `Triforce`

directory inside of the User folder will allow Dolphin to use it.



![](../../assets/5718c38ef04551d1.png)

Some games use *networking* for certain hardware, such as [F-Zero AX Monster Ride](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX)'s Cycraft and [Mario Kart Arcade GP 1](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP)/[2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2)'s namcam2. In both cases, a third-party server that emulates the behavior of the original device can be used with Dolphin. By default, Dolphin includes an IP Redirect to make the game look at localhost for these devices.

~~Conveniences such as save states are not yet available as Triforce emulation isn't fully integrated with all of Dolphin's features~~. This part of the article was originally a much longer "Limitations" section with a big list of warnings, shortcomings and potential problems for users, but some cheeky developers decided to go through and fix most of them after reading through the section. At this point, the biggest omissions are NetPlay and TASing support only because the new Triforce input devices aren't supported by input recordings.

Even Android users get to join in on the fun! Triforce hardware can be enabled and configured in the Android GUI like on desktop and games will run out of the box. The only limitation is that the Coin, Test, and Service buttons have not been added to Dolphin's touchscreen controller, so users will have to map them to a real controller or a physical button on the device. One exception to this is inserting a coin, which has been mapped by default to shaking your device.

Regardless of whether you're playing on PC or Android, some parts of the Triforce experience are still hardcoded. The attached JVS I/O devices for each game cannot be customized or changed in any way. This is not particularly accurate, as real cabinets could be configured in multiple ways, with some having deluxe features not present on others. This was a compromise, and we hope to make hardware features customizable in the future. Dolphin also automatically generates a magcard or IC card for each game and tracks progress on it, but users cannot swap cards, eject cards, or interact with them in any way whatsoever through Dolphin's GUI.

**Emulating Arcade Multiplayer**[¶](https://dolphin-emu.org#emulating-arcade-multiplayer)

Lastly, there is multiplayer support to talk about. Multiplayer was an important part of the arcade experience, and every Triforce game supports multiple players in some form. Single machine multiplayer should work without issues. This means that [Virtua Striker 3 ver. 2002](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_2002), [Virtua Striker 4](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4), [Virtua Striker 4 ver.2006](https://wiki.dolphin-emu.org/index.php?title=Virtua_Striker_4:Ver._2006), and [Gekitou Pro Yakyuu](https://wiki.dolphin-emu.org/index.php?title=Gekit%C5%8D_Pro_Yaky%C5%AB_(Triforce)) will all "just work".

Then there are the *multicabinet* games. [The Key of Avalon](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master) games, [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX), [Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) and [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) all had support for up to through using separate cabinets connected to a LAN (Local Area Network). Prior to these efforts, [crediar](https://github.com/crediar) had actually implemented some networking and socket features as part of emulating the monstrosity that is [The Key of Avalon](https://wiki.dolphin-emu.org/index.php?title=The_Key_of_Avalon:_The_Wizard_Master). Multicabinet is *required* for the Avalon games, even for single player, as they use a server/client model with each player on a client Triforce and the master Triforce hosting the game server. Unfortunately, due to missing touchscreen support, they still aren't playable even when the instances are able to connect with each other.

[F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) was on the opposite side of the spectrum and never showed any signs of life. The game would just get stuck on searching for other instances forever. We unfortunately can't figure out the problem right now, as we don't have any packet dumps from real networked [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) cabinets.

[Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) and [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) were the tragic pair throughout the review process. These games could actually see other instances of Dolphin on the network for a brief moment before they gave up and reverted to single cabinet mode.

In the days leading up to this article's release, [Billiard](https://github.com/jordan-woyak) and [sepalani](https://github.com/sepalani) spent some *very* late nights cleaning up parts of the networking code and hunting down regressions from those clean ups. The namcam2 for the Mario Kart games communicates via LAN on real hardware, and was particularly problematic during the clean up process. This was something that [crediar](https://github.com/crediar) already had working, so we *really* didn't want to break it.

Fortunately, testing the namcam2 only takes a couple of seconds. The game checks for it on boot during the initial hardware checks. But waiting for new builds to try would usually take anywhere from 10 minutes to multiple hours. During that waiting period, one of the few testers with access to Triforce software had to be at the ready to test things or else everything would get delayed. This led to a lot of downtime with bored testers messing with Triforce games to pass the time. It was during one of those downtimes that a tester reported that some of the attempts to fix the namcam2 were affecting multicabinet support, as multiple instances of Dolphin could no longer find each other in Mario Kart! Even though the effect was negative, it was still interesting and prompted more investigation.

After we properly fixed namcam2 support, curiosity got the best of us and we continued tinkering with various Mediaboard network commands hoping to get multicabinet working in time for launch. It seemed hopeless at times, but after multiple nights of burning the midnight oil... this happened.

At the 11th hour, we were finally able to get multiple instances of Dolphin running [Mario Kart Arcade GP 2](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP_2) to connect to each other. [Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) wasn't as easy and threw out "unhandled mediaboard command" errors despite the instances seeing one another. Thankfully, one look at the error and [crediar](https://github.com/crediar) knew exactly how to fix it. Minutes later, [Mario Kart Arcade GP](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Arcade_GP) was working just as well as its sequel. Both games now work incredibly well and are able to survive Wi-Fi latency spikes of over 80ms with little hitching and no disconnects.

We plan to write a full multicabinet emulation guide on our wiki after this article launches. Please stay tuned.

**Triforce Emulation Roadmap**[¶](https://dolphin-emu.org#triforce-emulation-roadmap)

This isn't the hacked-up Triforce emulation of 2012, but there's still a lot of work to be done. Throughout testing, a ton of features were added and many issues were addressed, but work is far from done. In order to get this massive project merged, some items on our wishlist had to be put off for later. He's a rundown of some of the bigger things we really want.

**Better IC/Magnetic Card Interface:**Currently, Dolphin automatically inserts a card that matches the current game ID in supported titles. This lets players easily play games and save without any extra setup. While this is nice, it isn't always what a player wants. We want to add the ability to buy, eject, swap, and insert cards like players could do at a real arcade.**Custom Cabinet Configurations:**Each game has its own hardcoded set of JVS I/O devices at the moment. While this means that games will always boot up with a valid configuration, it also means that alternative configurations can't easily tested, such as a cabinet without a magcard reader.**Make The Key of Avalon Games Playable:**These games are monsters to emulate, thanks to their specialized hardware. Even with multicabinet support working, there is still so much more to be done before Dolphin can bring this arcade experience home. The biggest fires to put out are the lack of touchscreen emulation and limited support for deck scanning.**Support for Force Feedback Hardware:**There are many bits and pieces on various Triforce cabinets that Dolphin can't currently handle. For example, force feedback motors are not generally supported. Only[F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX)'s steering wheel motors can be mapped at all, but even if you do map them, some forces are incorrectly interpreted.**Improved Controller Configuration GUI:**The Triforce Baseboard SI device reuses the GameCube controller configuration GUI and adapts that to each game as best as it can. In the long term, we want players to see each game's control devices and their layouts so that they can configure a controller without having to guess what each input does.**Hook up TAS Tools and NetPlay**: Dolphin's input recording tools don't support Triforce input devices, breaking these features.**Built-in Support For namcam2/Cycraft**: Currently, third-party programs are required in order to emulate Cycraft and namcam2. In order to make using third-party servers easier, Triforce games can be told to look at any address, including localhost, for these devices. In the future, an emulated option alongside real servers would be preferrable, somewhat like how Emulated USB Devices are currently handled.**Continue Fixing Crashes/Hangs:**Triforce emulation performed extremely well during our extensive testing, but to say everything is perfect would be a stretch. Given the rarity of Triforce games, not every revision of every game has been tested and some may not work.~~One common hang is that the Mario Kart titles get stuck when trying to eject the magcard after play. This doesn't result in any loss of data, but does mean the game has to be reset.~~**Edit**: The magcard eject hang was fixed just before this article was launched.

This list is by no means exhaustive, but we wanted to give an idea of how much work is still left to be done. Triforce emulation works incredibly well right now, but will continue to be a work-in-progress for the foreseeable future.

**Wrapping Things Up**[¶](https://dolphin-emu.org#wrapping-things-up)

Suddenly being thrust into Triforce emulation after all of these years was quite the experience for everyone involved. We can confidently say that this esoteric hardware is full of surprises. Just emulating these games and trying to test them was a distinct challenge far removed from anything we experienced with the GameCube and Wii! Each game has so many unique quirks, revisions, and sometimes even hardware configurations!

This couldn't have happened without [crediar](https://github.com/crediar). Going into this, most Dolphin developers knew almost nothing about Triforce emulation, and without the decade plus of knowledge he had built up while maintaining his fork, we would have stood no chance.

With everything that's been done, there was one final challenge. Our goal was for Dolphin's Triforce emulation to be good enough to drive hobbyist arcade cabinets and preserve the arcade experience these games were meant for. So we gave it a try. We built a hobbyist [F-Zero AX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_AX) cabinet kit, set up a PC with Dolphin, and let family and friends have at it. And it was a blast for everyone involved.

When we first started on this journey, most of us hadn't had the opportunity to play any of the Triforce games on an original cabinet. The best we could do was buy the core systems and games and try to get them running with what we had. The experience on bare hardware was rarely good and never great, but that was not how they were meant to be played. Triforce games were designed to be a part of an arcade experience, with a cool cabinet, interesting features, and unique control schemes. Through emulation, we were able to bring some of that arcade magic back to these games that no longer have a cabinet to call home.

But through all of those trials, it's finally here. Maybe a ~~few~~ *dozen* years later than anyone expected. However, there are still a lot of exciting changes still on the horizon, so be sure to check in for more development articles about Dolphin - the GameCube, Wii, and **Triforce** emulator!