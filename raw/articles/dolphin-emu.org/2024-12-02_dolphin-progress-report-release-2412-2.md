---
title: 'Dolphin Progress Report: Release 2412'
url: https://dolphin-emu.org/blog/7A/
author: Mitaclaw
published: '2024-12-02'
source_blog: Dolphin Emulator - GameCube/Wii games on PC
source_site: https://dolphin-emu.org/
category: graphics
fetched: '2026-04-19'
---

Dolphin 2412 is here and we've got the details for what's new in the latest release. The biggest thing to note is that there's a lot of polishing to help make playing games a little more pleasant. Several key fixes to Dolphin's HLE audio helps bring a few more games toward audio perfection, and adjustments to Dolphin's CPU <-> GPU syncing reduces the number of harmless, but annoying, popup errors that happen in certain games.

That isn't to say there aren't any titles seeing significant improvements. [LIT (School of Darkness)](https://wiki.dolphin-emu.org/index.php?title=LIT) had a unique problem that exposed yet another unemulated hardware behavior. And if you're looking for a deep dive into problematic behavior in a game? We have one of those as well. [Eternal Darkness](https://wiki.dolphin-emu.org/index.php?title=Eternal_Darkness:_Sanity%27s_Requiem) has been a thorn in our side the past couple of months and required some special attention to get working again in time for this release.

For details on all that and more, join us for Release 2412's Notable Changes!

**Notable Changes**[¶](https://dolphin-emu.org#notable-changes)

All of the changes below are available in Release 2412.

** Tilka** has been perfecting DSP-HLE over the last few years. A majority of their changes have been minor and fix subtle effects that most users won't notice unless they've recently played the game on console with a high-end sound system. In the last progress report,

[we covered their implementation of the Zelda microcode's low-pass and biquad filters](https://dolphin-emu.org/blog/2024/09/04/dolphin-progress-report-release-2407-2409/#zelda-hle-pikmin-fixes-2407-177-and-2407-225-by-flacs), but we didn't mention that

**also took the time to**

[Tilka](https://github.com/tilka)[implement the biquad filter in the AX microcode](https://dolphin-emu.org/download/dev/master/2407-257/)! Doing so fixed an issue in

[I SPY: Spooky Mansion](https://wiki.dolphin-emu.org/index.php?title=I_SPY:_Spooky_Mansion)where the wind was too loud.

Unfortunately, it also started causing issues in [Need for Speed: Nitro](https://wiki.dolphin-emu.org/index.php?title=Need_for_Speed:_Nitro)'s audio.

Thankfully, the issue was found relatively quickly after it was reported. The implementation of the filters didn't take into account that the real AX microcode was using the DSP's set40 (40-bit sign extension) mode, which caused some calculations to be incorrect. After fixing an off-by-one error and adding some clamping, [Need for Speed: Nitro](https://wiki.dolphin-emu.org/index.php?title=Need_for_Speed:_Nitro)'s issues were resolved.

Since [the epic battle against Bounding Box](https://dolphin-emu.org/blog/2021/06/06/dolphin-progress-report-april-and-may-2021/) that lasted throughout [a good chunk of 2021](https://dolphin-emu.org/blog/2021/08/01/dolphin-progress-report-june-and-july-2021/), our foe has remained mostly subdued. But much like Bowser inevitably returns again and again after being defeated by ~~Mario~~ Luigi, a Bounding Box issue has risen from the ashes.

Unlike previous Bounding Box issues, this one wasn't as simple to reproduce. Users have been reporting it for a better part of the year, but upon actually trying to investigate it, the issue would often disappear. We did know that it wasn't specific to any particular bounding box title. It could happen in [Disney's Magical Mirror: Starring Mickey Mouse](https://wiki.dolphin-emu.org/index.php?title=Disney%27s_Magical_Mirror_starring_Mickey_Mouse) all the way to the most complicated of Bounding Box games, [Paper Mario: The Thousand Year Door](https://wiki.dolphin-emu.org/index.php?title=Paper_Mario:_The_Thousand-Year_Door).

The only constant was that resetting the user's graphics settings would permanently fix the issue. *Something* was interacting poorly with Bounding Box, but we didn't know what.

On the issue tracker, ZephyrSurfer eventually managed to figure out that the issue centered around Dolphin's Auto IR (Internal Resolution) setting. Auto IR lets Dolphin automatically set the internal resolution based on the size of the window or full-screen monitor (rounded to the closest whole multiple). Users who don't want to mess with their settings can just set this and forget it. The key discovery that had us realize it was the problem was that *changing the window size while the game was running* was all it took for the affected users to reproduce.

In order to get this fixed, ** TellowKrinkle** jumped in and analyzed the issue. He figured out that Dolphin was forgetting to mark the pixel shader manager as dirty when changing the window size with Auto IR. Essentially, Dolphin is letting the GPU driver know that scaling values used for the bounding box calculation in the pixel shader have changed in RAM, so that the GPU driver will send the data to VRAM again. Because Dolphin wasn't doing that, all bounding box calculations were using the old internal resolution even after the window size changed. Oops.

A simple one line change later and Bounding Box works correctly when using Auto IR.

Around March of this year, several of Dolphin's developers on Linux began noticing that they shared a rather inconvenient issue. When using the Vulkan video backend with proprietary Nvidia drivers, attempting to resize the game window while emulation was running would often completely lock up Dolphin's UI.

The deadlock was quickly traced to a call to the `vkWaitForFences`

function in the Vulkan backend's command buffer manager. Seeing this, [ Pokechu22](https://github.com/Pokechu22) joined the conversation and dug deeper to figure out what sequence of events was causing the blockage. Eventually, it was discovered that a call to the

`vkAcquireNextImageKHR`

function was failing in a way that was not being handled entirely correctly, leaving a [semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming))unsignaled forever.

With a cause found, it was time to bisect recent changes to figure out which one was to blame for it. What happened next was unexpected. *Every* build that could be tested, going as far back as [The Great VideoCommon Unification of 2019](https://dolphin-emu.org/blog/2019/04/01/the-new-era-of-video-backends/), was exhibiting this deadlock. But hang on, wasn't this a relatively recent issue? Something wasn't adding up, and without an obvious mistake to fix, the case went cold.

![](../../assets/3fa8d92029cc8822.webp)

As [ JMC47](https://github.com/JMC47) was reviewing

['s](https://github.com/TellowKrinkle)

**TellowKrinkle**[fix for auto IR size](https://dolphin-emu.org#2409-71-auto-ir-size-fix-bounding-box-corruption-by-tellowkrinkle), he naturally needed to test resizing the game window. However, as a developer on Linux using the Vulkan backend, he had to pause emulation before doing so in order to prevent the deadlock from occuring. It became such a nuisance that he brought it up in conversation on the

[official Dolphin Discord server](https://dolphin-emu.org/blog/2023/01/07/announcing-official-dolphin-discord/). This time, the issue caught the attention of

[, who joined the conversation after independently discovering the problem that](https://github.com/CasualPokePlayer)

**CasualPokePlayer**[found earlier.](https://github.com/Pokechu22)

**Pokechu22**Already knee-deep in graphics backend work and aided by CasualPokePlayer's insight, **TellowKrinkle** decided he should remedy this issue once and for all. Amazingly, he was able to put together a working solution all while being unaffected by the issue himself! Once it was confirmed to work by other developers who *were* affected by the issue, the fix was in.

![](../../assets/e437b30cf19884c3.webp)

The exact source of the Linux + NVIDIA + Vulkan deadlock was still a mystery even though it was already fixed. However, after a bit of digging, we found the smoking gun. In the [changelog for Nvidia's Linux x64 (AMD64/EM64T) Display Driver 550.54.14](https://www.nvidia.com/en-us/drivers/details/218826/) from **February 23, 2024**, it says this:

Fixed a bug where vkAcquireNextImageKHR() was not returning VK_ERROR_OUT_OF_DATE_KHR when it should with WSI X11 swapchains.


This error code being returned by the `vkAcquireNextImageKHR`

function was one of the symptoms that was observed while debugging this deadlock! Does that mean that this version of the proprietary Nvidia driver broke Dolphin? We installed an older version of Dolphin and various proprietary Nvidia driver versions onto a fresh copy of Debian Linux to find out.

- ✅
[550.54.14](https://www.nvidia.com/en-us/drivers/details/218826/)from**February 23, 2024**, the aforementioned version, would deadlock. - ❌
[550.40.07](https://www.nvidia.com/en-us/drivers/details/218119/)from**January 24, 2024**, the preceding version and the first beta of the 550 series, would*not*deadlock. - ✅
[565.57.01](https://www.nvidia.com/en-us/drivers/details/233008/)from**October 22, 2024**, the latest beta version, would deadlock. - ❌
[535.216.01](https://www.nvidia.com/en-us/drivers/details/233000/)from**October 22, 2024**, the latest long-term support version at the time of writing, would*not*deadlock.

It's also worth noting that the `vkAcquireNextImageKHR`

function in driver versions without the deadlock would always return `VK_SUCCESS`

, even while aggressively resizing the game window. So, in conclusion, every proprietary Nvidia driver from the 550 series and onward (excluding the first 550 beta version) exhibits this new behavior has to be accounted for by Dolphin.

Nowadays, it's rare that Dolphin sees an actual core emulation change to fix a game, but it still happens occasionally! We recently received an issue report that the WiiWare title [LIT](https://wiki.dolphin-emu.org/index.php?title=LIT) (known as *School of Darkness* in Japan) had severe graphical issues in Dolphin involving the text on its map and menu screens.

When ** pokechu22** looked into the issue, they found that the devs at WayForward accidentally enabled lighting when rendering the text. The geometry which made up the text also didn't include any

[normals](https://en.wikipedia.org/wiki/Normal_(geometry)), which are used when calculating lighting. If a normal vector isn't specified and lighting is enabled, Dolphin uses a default value of (0, 0, 0) in lighting calculations. This is what results in the text showing up as all black. But why doesn't the bug appear on real hardware?

To figure out why, ** pokechu22** used the fifoplayer to reproduce the problem on an actual Wii and wrote some hardware tests. They found that when lighting is enabled without any corresponding normals, a real Wii GPU instead

*reuses the last normal it received*. In LIT, the last valid normal vector sent to the GPU is (0, 0, 1), which comes from rendering the map's background. Using this value in the lighting calculations allows the text to show up with its intended color.

After normal vector caching was implemented in Dolphin, the text was fixed!

This GPU quirk is actually similar to [one that was abused by Factor 5 in the Rogue Squadron series for bump mapping](https://dolphin-emu.org/blog/2022/05/17/dolphin-progress-report-february-march-and-april-2022/#50-16301-videocommon-handle-emboss-texgen-with-only-a-single-normal-by-pokechu22). In those games, Factor 5 sends a single dummy triangle containing common bi-normal and tangent vectors to the GPU, and then sends the actual geometry which relies on the vectors but doesn't include them. As the GPU reuses the bi-normal and tangent vectors from the dummy triangle when rendering the real geometry, the game doesn't need to send them multiple times. This saves memory and improves performance.

One of the highest levels of accuracy in emulation is when an emulator is deemed "cycle accurate." Assuming all things are handled properly, a cycle accurate emulator will, in theory, allow a game to run **exactly** the same as it would on original console. This would include things like framerate lag, timing issues, race conditions, and everything else you'd expect. Given identical start states, an input recording from a cycle accurate emulator would play back exactly the same on the original console. This is how we have console verified Tool Assisted Speedruns on many older consoles.

Dolphin isn't cycle accurate and doesn't try particularly hard to reach cycle accuracy. Why is that?

Obtaining cycle accuracy is a *ton* of work and a lot slower than just using estimations. Just emulating a few pieces of cycle accuracy (such as the CPU instruction pipeline, cycle timings, and various cache hits/misses) is arduous and would massively reduce performance. And that's only just *part* of what we'd need for one component. Cycle accurate GameCube/Wii emulation is a long ways off for the purpose of actually playing games.

Dolphin is a general use emulator that wants to be as accurate and compatible as it *reasonably* can while maintaining good performance. All throughout Dolphin you'll find *tons* of tradeoffs between accuracy, performance, and compatibility. Many of the most accurate options in Dolphin are *disabled by default* to keep performance at an acceptable level.

For something like cycle timings, Dolphin just tries to get *close enough*. On the GameCube/Wii CPU, how many cycles an instruction can take varies greatly. Sometimes the code might hit the L1/L2 cache, sometimes it won't. Sometimes *the instructions around an instruction* can reduce the number of cycles it takes to execute that instruction! And that's just what we as blog writers can understand about it. The actual details are frightening, but what you need to know is that Dolphin just fudges the numbers to get reasonably close and most games are fine with this.

The amusing thing about Dolphin's estimations is that it will sometimes be a little faster than console, and sometimes a little slower. A good example of a scenario where Dolphin is slower is the video player in [Tales of Symphonia](https://wiki.dolphin-emu.org/index.php?title=Tales_of_Symphonia). The video decoding logic is super optimized for the GameCube's CPU, and Dolphin's estimations on how many cycles can be used per frame is off by enough to cause stuttering during playback. Note that [Tales of Symphonia](https://wiki.dolphin-emu.org/index.php?title=Tales_of_Symphonia) is only being used as an example of the problems that can happen with a non-cycle accurate emulator, and this particular problem is not being addressed at this time.

For the GameCube/Wii, there are also other complications, with one of them being CPU <-> GPU communication. How fast each runs and how often they are allowed communicate can greatly affect both compatibility and performance. Too little communication and interrupts can get missed or fired at the wrong time, and the state that each component is in might not match what they are expecting!

**Warning: Dual Core Rant**

Dual core is a performance hack that allows Dolphin to separate the CPU and GPU emulation into their own threads and let them run independently of one another (with occasional synchronization points). Because they are running at the same time and synchronization has to be kept at a minimum in order to gain performance, it is entirely possible that performance hiccups can cause one thread to fall too far behind the other. And because the *actual state* of the component can be affected, these are slowdowns that the emulated software can actually feel! Depending on how sensitive a game is to these problems, they may be perfectly stable in dual core, or entirely unusable to the point where it has to be force disabled.

There are also interesting cases where some games are perfectly fine *as long as the host computer is fast enough*. [Fire Emblem: Path of Radiance](https://wiki.dolphin-emu.org/index.php?title=Fire_Emblem:_Path_of_Radiance) is perfectly stable when using dual core on most devices, but becomes unstable on the extremely low-end hardware that needs dual core the most. Developers have tried to fix dual core in the past, however all of the attempts have either greatly reduced dual core's performance advantage while still not matching single core's compatibility, or further reduced its compatibility in exchange for determinism. Dual Core as it is has proven hard to replace despite the downsides.

Single core does not have these problems at the expense of running both the CPU and GPU threads on the same core. Performance hiccups cannot leak through to the emulated software and stability is essentially guaranteed, or at least guaranteed to be consistent in cases where something is broken. The following explanation describes *single core's* deterministic way of syncing the CPU and GPU works.

Dolphin switches between emulating the CPU and emulating the GPU in set intervals. As a balance between accuracy and performance, Dolphin doesn't swap every emulated cycle. Instead, Dolphin emulates the CPU and GPU in time slices. Essentially, Dolphin will let GPU commands accumulate in memory for 1000 cycles, and then make the GPU catch up. However, when Dolphin is emulating the GPU, there is a possibility that the data at the end of that command stream doesn't form a complete command yet. If that happens, **and** the game reconfigures the location in memory from where the GPU reads the command stream, then that incomplete command can be combined with a *new* unrelated command!

When this happens, there's a chance that this new command could become an unknown opcode that causes an annoying popup for users. In order to fix this, ** Tilka** changed it so Dolphin now forcibly processes all pending GPU commands if the game reconfigures the location in memory that it is reading from.

Doing this fixes unknown opcode popups in over 20 games!

- Bass Pro Shops games (
[The Hunt](https://wiki.dolphin-emu.org/index.php?title=Bass_Pro_Shops:_The_Hunt),[The Strike](https://wiki.dolphin-emu.org/index.php?title=Bass_Pro_Shops:_The_Strike), etc) [Captain America: Super Soldier](https://wiki.dolphin-emu.org/index.php?title=Captain_America:_Super_Soldier)[Country Dance 2](https://wiki.dolphin-emu.org/index.php?title=Country_Dance_2)[Def Jam Rapstar](https://wiki.dolphin-emu.org/index.php?title=Def_Jam_Rapstar)[Disney Guilty Party](https://wiki.dolphin-emu.org/index.php?title=Disney_Guilty_Party)[Food Network: Cook or Be Cooked!](https://wiki.dolphin-emu.org/index.php?title=Food_Network:_Cook_or_Be_Cooked)[Ghostbusters: The Video Game](https://wiki.dolphin-emu.org/index.php?title=Ghostbusters:_The_Video_Game)[Metroid Prime](https://wiki.dolphin-emu.org/index.php?title=Metroid_Prime)[Mushroom Men: The Spore Wars](https://wiki.dolphin-emu.org/index.php?title=Mushroom_Men:_The_Spore_Wars)[Nickelodeon Dance](https://wiki.dolphin-emu.org/index.php?title=Nickelodeon_Dance)[Nickelodeon Dance 2](https://wiki.dolphin-emu.org/index.php?title=Nickelodeon_Dance_2)[PDC World Championship Darts 2009](https://wiki.dolphin-emu.org/index.php?title=PDC_World_Championship_Darts_2009)[PDC World Championship Darts: Pro Tour](https://wiki.dolphin-emu.org/index.php?title=PDC_World_Championship_Darts:_Pro_Tour)[Pékin Express](https://wiki.dolphin-emu.org/index.php?title=P%C3%A9kin_Express)[Resident Evil Zero](https://wiki.dolphin-emu.org/index.php?title=Resident_Evil_Zero)[Rogue Trooper: Quartz Zone Massacre](https://wiki.dolphin-emu.org/index.php?title=Rogue_Trooper:_Quartz_Zone_Massacre)[Roogoo: Twisted Towers](https://wiki.dolphin-emu.org/index.php?title=Roogoo:_Twisted_Towers)[Star Wars: The Force Unleashed II](https://wiki.dolphin-emu.org/index.php?title=Star_Wars:_The_Force_Unleashed_II)[Super Monkey Ball: Banana Blitz](https://wiki.dolphin-emu.org/index.php?title=Super_Monkey_Ball:_Banana_Blitz)[The Baseball 2003 - Battle Ball Park Sengen Perfect Play Pro Yakyuu](https://wiki.dolphin-emu.org/index.php?title=The_Baseball_2003-Battle_Ball_Park_Sengen_Perfect_Play_Pro_Yakyuu)[Thor: God of Thunder](https://wiki.dolphin-emu.org/index.php?title=Thor:_God_of_Thunder)[Victorious: Taking the Lead](https://wiki.dolphin-emu.org/index.php?title=Victorious:_Taking_the_Lead)[Wipeout: The Game](https://wiki.dolphin-emu.org/index.php?title=Wipeout:_The_Game)- and many more...

Note that almost all of these unknown opcodes were non-fatal and mostly just an annoyance for users. Still, the fact they were popping up showed that emulation *was* problematic to some degree in these titles. Overall, we expected this change to boost our accuracy without introducing any regressions. As an added bonus, the changes to the command processing allows [Harvest Moon: Tree of Tranquility](https://wiki.dolphin-emu.org/index.php?title=Harvest_Moon:_Tree_of_Tranquility) to finally boot without green flashes in single core mode.

The previous change tightened up Dolphin's CPU/GPU synchronization to prevent unknown opcodes. There's no way that could cause a regression, right?

...

One of the potential issues with making timings more accurate is that sometimes you break things that *shouldn't* have been working, but were working for the wrong reasons. In this case, [Eternal Darkness](https://wiki.dolphin-emu.org/index.php?title=Eternal_Darkness:_Sanity%27s_Requiem) started hanging on boot.



![](../../assets/4402cc525961f7a8.avif)

The previous opcode decoding fixes *were an improvement to overall accuracy*, so ** Tilka** didn't want to revert them because of one game. That meant diving into

[Eternal Darkness](https://wiki.dolphin-emu.org/index.php?title=Eternal_Darkness:_Sanity%27s_Requiem)in a way no one else ever had.

As with many of the remaining broken games, Dolphin was only *half* of the problem. The other half was actually an issue in the game itself. Make no mistake - with the opcode decoding fixes, Dolphin was now emulating the game *closer to how it would run on console*. However, by being closer, it was now triggering a race condition that would never happen on real hardware.

In order to explain this issue, we have to get a bit messy with an in-depth explanation. If you're not interested in the internal behavior of this game's FIFO, feel free to skip the next two paragraphs.

In essence, [Eternal Darkness](https://wiki.dolphin-emu.org/index.php?title=Eternal_Darkness:_Sanity%27s_Requiem) has a race condition within its graphics rendering code. It uses the `GXSetDrawDone`

function to add a draw done command to the command stream, which makes the GPU raise an interrupt when executed. Some time after adding the command, it then reconfigures the GPU command stream. As previously mentioned, Dolphin wouldn't properly execute commands at the end of the stream. This meant that the draw done command was never executed and the interrupt was never raised. Because of that, the game didn't hang in Dolphin! Wait, what?

The difference between Dolphin and real hardware is that an actual GameCube GPU would always raise the draw done interrupt *before* Eternal Darkness has a chance to change the command stream address. Without the opcode decoding fixes, the draw done interrupt would never be raised due to its command being ignored, avoiding the race condition altogether. However, with the opcode decoding fixes, we now get interesting behavior that's *closer* to console but still not quite correct. This time, all the GPU commands are processed as per normal and the draw done command is executed. However, because our cycle timings are inaccurate, Dolphin has [a hack that delays raising the draw done interrupt by a minimum of 500 cycles](https://github.com/dolphin-emu/dolphin/blob/401d6e70f644afd4418a93778148d53f90954d75/Source/Core/VideoCommon/PixelEngine.cpp#L220-L222). This hack gives games some time to finish any necessary setup that may not be finished if the interrupt is raised immediately. Eternal Darkness is able to change the GPU command stream address during the delay. When the interrupt is finally raised 500+ cycles later, the game promptly hangs because the code that handles the interrupt doesn't expect a different command stream address at that point in time.

This hang is technically a game bug, albeit one that never manifests on real hardware. We could change the 500 cycle delay until we found a number that won the race, but we ultimately decided not to make an arbitrary decision like that based on the results of one game. Instead, ** Tilka** made a patch for Eternal Darkness to replace the problematic

`GXSetDrawDone`

function with the safer `GXDrawDone`

, which forces the game to wait for the interrupt to be raised before it can proceed. This is an incredibly efficient fix, as it comes with no performance cost, doesn't require any change to Dolphin itself, and means we won't break any other games while trying to find a delay that works for Eternal Darkness. Correct emulation would require incredibly small GPU slices which would drag down performance of the emulator in general.To prevent any confusion surrounding this regression, the patch has automatically been enabled in the latest release for all regional variants of the game. If you wish to disable the patch or view what patches are available for other games, simply access the game properties page and go to the "Patches" tab.

The Wii Remote is a rather complex controller to emulate. It has attachments, a weird layout, motion controls, a small amount of savedata, infrared, and even a speaker! The speaker part of the Wii Remote is one of its more forgotten features simply because most games used it for entirely optional sound flourishes (the Wii allows the player to turn the speaker off), and the speaker itself was rather puny. When using an emulated Wii Remote, Dolphin pumps the Wii Remote speaker data to the standard audio output device. However, when using Real Wii Remotes or Bluetooth Passthrough, Wii Remote audio *can* work in Dolphin just as it does on console. In fact, with Bluetooth Passthrough and a strong enough adapter, you can enjoy the same mediocre sound quality as console!

The fact this feature has been so maligned is why very few people noticed or cared that Wii Remote audio was very broken in some games. For a revision of the [AX microcode](https://dolphin-emu.org/blog/2014/11/12/the-rise-of-hle-audio/) used early in the Wii's lifecycle, there were some serious bugs in our DSP-HLE implementation:

- The size difference between the high-pass and biquad filter was not accounted for, causing adjacent memory to become corrupted.
- The Wiimote sample buffer pointers were advanced by 32 samples per millisecond instead of 6 samples. Any audio corruption caused by this was usually hidden by the first bug.
- PB updates on Wii were being byte-swapped twice. However, no games that use this feature were found.

While we don't know if the third bug affected any games, the first two affect *a lot* of games released between 2006 and 2007. ** Tilka** gave us an example list of games that they noted are fixed by their changes:

[Excite Truck](https://wiki.dolphin-emu.org/index.php?title=Excite_Truck)[Ice Age 2: The Meltdown](https://wiki.dolphin-emu.org/index.php?title=Ice_Age_2:_The_Meltdown_(Wii))[Kororinpa: Marble Mania](https://wiki.dolphin-emu.org/index.php?title=Kororinpa:_Marble_Mania)[Rapala Tournament Fishing](https://wiki.dolphin-emu.org/index.php?title=Rapala_Tournament_Fishing)[Shrek the Third](https://wiki.dolphin-emu.org/index.php?title=Shrek_the_Third)[Super Monkey Ball: Banana Blitz](https://wiki.dolphin-emu.org/index.php?title=Super_Monkey_Ball:_Banana_Blitz)[Tiger Woods PGA Tour 07](https://wiki.dolphin-emu.org/index.php?title=Tiger_Woods_PGA_Tour_07)[WarioWare: Smooth Moves](https://wiki.dolphin-emu.org/index.php?title=WarioWare:_Smooth_Moves)[Wing Island](https://wiki.dolphin-emu.org/index.php?title=Wing_Island)- maybe more?

Fun fact - [WarioWare: Smooth Moves](https://wiki.dolphin-emu.org/index.php?title=WarioWare:_Smooth_Moves) was the only one of these titles with [an active issue report](https://bugs.dolphin-emu.org/issues/11725) saying that Wii Remote audio was broken.

Also, games that use the [Zelda microcode](https://dolphin-emu.org/blog/2015/08/19/new-era-hle-audio/) were not affected by these bugs. For example, [The Legend of Zelda: Twilight Princess](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_Twilight_Princess_(Wii)) was not affected despite being released in 2006.

Unlike Windows and macOS, there isn't a single OS that you can point to and call "Linux". Instead, when a user wants to run Linux on their system, they are able to choose between many different "flavours" of Linux known as distributions. Each distribution bundles the Linux kernel together with a set of packages containing various drivers, software, libraries, frameworks, and more. There are many benefits to this system. For example, a user can choose a distribution that is tailored to their own needs. Newbies might gravitate towards beginner-friendly distributions like [Ubuntu](https://ubuntu.com), while more advanced users may prefer distributions that offer lots of customizability, like [Arch Linux](https://archlinux.org/) or [NixOS](https://nixos.org/).

However, this system also comes with several disadvantages. The biggest issue relevant to us at Dolphin is that each distribution tends to have its own vision for how software should be packaged and installed on the system. They also update their packages independently of each other, meaning that one distribution could have the most up to date version of a specific framework, while another distribution is stuck on an out of date version. Unfortunately for app developers, all these factors make it difficult to create a single build of an app that can run across every possible Linux distribution. As a result, creating desktop apps on Linux has historically been a bit of a mess. While Dolphin has offered official builds for Ubuntu in the past, those builds wouldn't install on other non-Ubuntu distributions, and would only be guaranteed to work correctly on the specific Ubuntu version that it was built for. After we stopped offering official Ubuntu builds, our policy has been to just let each distribution be responsible for producing their own Dolphin builds. If a Linux user wanted to install Dolphin, they would either need to compile it themselves or use the package from their distribution.

*the creator of Linux*, once described the process of making Linux app builds as "a major #$@&ing pain in the %@$".

In an attempt to solve the problem, several competing solutions for packaging Linux apps with cross-distribution compatibility have emerged over the past decade. One of these solutions is known as [Flatpak](https://flatpak.org/). Flatpak allows a developer to build their app against a common base "runtime", which contains all of the libraries and frameworks that an app may need. When an app is installed, its corresponding runtime is also downloaded and installed along with it. Since all of the dependencies are found in the runtime or bundled with the app itself, a Flatpak build of an app doesn't rely on the packages provided by the installed distribution! [The distribution just has to support the Flatpak system itself.](https://flatpak.org/setup/)

But why are we choosing to make Flatpak builds over all of the other competing solutions? The answer lies in the Steam Deck. [Valve has adopted Flatpak as the official way to install non-Steam apps on SteamOS](https://help.steampowered.com/en/faqs/view/671A-4453-E8D2-323C). When a user wants to install something that isn't available on the Steam Store, all they have to do is switch to Desktop Mode and open the Discover Software Center. There, they can find a plethora of software available for download in the Flatpak format, including many emulators!

Apps in Flatpak format are most commonly distributed by [repositories](https://docs.flatpak.org/en/latest/repositories.html), and the largest Flatpak repository is known as [Flathub](https://flathub.org). The Steam Deck has Flathub installed by default, which is what allows users to instantly get access to a large library of Flatpak software. Surprisingly, Dolphin is actually one of the oldest apps that was added to Flathub. Ever since Flathub launched in 2017, [a group of dedicated individuals](https://github.com/flathub/org.DolphinEmu.dolphin-emu/graphs/contributors) has been maintaining an unofficial Flatpak version of Dolphin! When we heard about this, it only made sense that we ask them for assistance in making our own Flatpak builds.

With the help of ** cpba** and

**, all of the necessary files to create Flatpak builds have now been merged into the upstream Dolphin repository.**

[ColinKinloch](https://github.com/ColinKinloch)**completed the necessary infrastructure work to allow our Buildbot CI to create Flatpak builds.**

[OatmealDome](https://github.com/OatmealDome)You can now add one of the following repositories to install our Flatpak builds:

- Release builds:
[https://flatpak.dolphin-emu.org/releases.flatpakrepo](https://flatpak.dolphin-emu.org/releases.flatpakrepo) - Development builds:
[https://flatpak.dolphin-emu.org/dev.flatpakrepo](https://flatpak.dolphin-emu.org/dev.flatpakrepo)

Alternatively, you can also download single-file bundles for specific builds on our [downloads page](https://dolphin-emu.org/download).

While we're launching our Flatpak builds with this report, we should note that there's a slight catch. The builds found on Flathub are still unofficial due to some pending changes to our infrastructure and various important people being away on vacation. (Yes, eagle-eyed readers, this is also why Dolphin isn't verified on Flathub yet.) We hope to have this fixed soon!

And to all of our AppImage fans: [we're aware of the demand](https://github.com/dolphin-emu/dolphin/pull/13055). We want to work on getting Flatpak up and running first.

Just when we thought we were done, we were pulled back in. After all of the work ** Tilka** did to reduce the number of unknown opcode errors that games would spew, we started seeing the worrying trend of

*new*unknown opcode errors popping up across more games. Fortunately, none of these were fatal and almost every one centered around closing games.

[New Super Mario Bros. Wii](https://wiki.dolphin-emu.org/index.php?title=New_Super_Mario_Bros._Wii) was the first culprit reported, so ** Tilka** conducted an investigation to figure out what was going on.

If you've been reading the rest of the progress report, then you'll remember that in single core, Dolphin lets GPU commands accumulate in memory for 1000 cycles. There's something we didn't mention earlier, though: every now and then we also copy these commands from the game's memory into a Dolphin-internal buffer, partially to hide from the game that we're letting many commands accumulate. When processing these commands, we look at the Dolphin buffer first, and then whatever is in the game's memory.

If the console is asked to shut down, [New Super Mario Bros. Wii](https://wiki.dolphin-emu.org/index.php?title=New_Super_Mario_Bros._Wii) calls `GXAbortFrame`

to stop rendering the current frame and reset the GPU. When this happens, Dolphin empties its internal buffer but doesn't empty the game's memory as well. The last bytes seen by the opcode decoder could be a partial command in the internal buffer *followed by* bytes from commands in memory that were not cleared! In order to prevent command buffer execution from resuming in the middle of a command, Dolphin now allows the GPU to catch up to the CPU's reality *and then* resets the internal buffer. That means if there are only a few commands left to process, they will go through fine and there will be no problems.

Because the target of this fix was [New Super Mario Bros. Wii](https://wiki.dolphin-emu.org/index.php?title=New_Super_Mario_Bros._Wii)'s regression, we weren't expecting to fix any previously broken games. To our surprise, it turns out this flaw *was* causing problems across several games, even under the old GPU syncing behavior!

[Deadliest Catch - Sea of Chaos](https://wiki.dolphin-emu.org/index.php?title=Deadliest_Catch:_Sea_of_Chaos)[G.I. Joe - The Rise of Cobra](https://wiki.dolphin-emu.org/index.php?title=G._I._Joe:_The_Rise_of_Cobra)[Monster 4x4 - World Circuit](https://wiki.dolphin-emu.org/index.php?title=Monster_4x4:_World_Circuit)[The Oregon Trail](https://wiki.dolphin-emu.org/index.php?title=The_Oregon_Trail)

If you're keeping count, this means that ** Tilka** has improved compatibility across at least thirty-four games for this release!

Unfortunately, this solution is a stop gap. The core issue of the internal buffers being cleared without clearing the game's buffer still exists. If a lot of GPU commands have been accumulated, problems can still occur. This is what causes [SpongeBob SquarePants featuring Nicktoons: Globs of Doom](https://wiki.dolphin-emu.org/index.php?title=SpongeBob_SquarePants_featuring_Nicktoons:_Globs_of_Doom) to be broken in the latest release version. ** Tilka** also conducted additional hardware testing and found some additional behavior that needs to be implemented. We'll hopefully have all these improvements in a future release.

The name MetaFortress should ring a bell to long-time readers. For the unfamiliar, MetaFortress was an anti-piracy system used by [a handful of games on the Wii](https://wiki.dolphin-emu.org/index.php?title=Category:Games_that_use_MetaFortress_Anti-Piracy). We previously covered MetaFortress's presence in the all-time classic game [The Smurfs: Dance Party](https://wiki.dolphin-emu.org/index.php?title=The_Smurfs:_Dance_Party) back in 2017:

While modern versions of Dolphin are able to handle MetaFortress's anti-piracy checks, we still include patches for bypassing MetaFortress entirely in some games. While MetaFortress's primary purpose is to check for piracy, it also does some trickery to *detect if the game itself has been modified*, just in case any of its anti-piracy checks were patched out. This can cause problems when making cheats and mods for MetaFortress-protected titles, as modifying the game's code could trip MetaFortress.

One of the games that we ship a MetaFortress bypass patch for is [Kirby's Return to Dream Land](https://wiki.dolphin-emu.org/index.php?title=Kirby%27s_Return_to_Dream_Land) (also known as *Kirby's Adventure Wii* in Europe). Unfortunately, when the patch was ported from the North American version to the European version, some mistakes were made in the porting process. If a user enabled the MetaFortress bypass patch and tried starting the game, it would hang on a black screen due to some patch addresses being incorrect. [A lone user did report on the forums that the patch was broken earlier this year](https://forums.dolphin-emu.org/Thread-wii-kirby-s-return-to-dream-land?pid=533193#pid533193), but their post unfortunately fell through the cracks.

** vaguerant** independently discovered that the European version of the MetaFortress bypass patch was broken and took it upon themselves to fix it.

With this change, we hope that the scourge of MetaFortress has now been defeated once and for all.

**Casual readers beware!**[¶](https://dolphin-emu.org#casual-readers-beware)

The following two sections cover changes to Dolphin's debugging interface, a normally hidden suite of tools used for deep-dives into the workings of emulated software. If this does not interest you, then that concludes today's Progress Report! Feel free to [skip ahead for this release's contributors and a special message regarding the Stop Killing Games campaign](https://dolphin-emu.org#this-releases-contributors).

...

Are you still here? Well then, *let's get technical!*

[5.0-21724 - Branch Watch Tool: Add Set Breakpoints Submenu](https://dolphin-emu.org/download/dev/master/5.0-21724/) and [2409-15 - Branch Watch Tool: Refactors, Fixes, and Features](https://dolphin-emu.org/download/dev/master/2409-15/) by [mitaclaw](https://github.com/mitaclaw)[¶](https://dolphin-emu.org#50-21724-branch-watch-tool-add-set-breakpoints-submenu-and-2409-15-branch-watch-tool-refactors-fixes-and-features-by-mitaclaw)

[5.0-21724 - Branch Watch Tool: Add Set Breakpoints Submenu](https://dolphin-emu.org/download/dev/master/5.0-21724/)

[2409-15 - Branch Watch Tool: Refactors, Fixes, and Features](https://dolphin-emu.org/download/dev/master/2409-15/)

[mitaclaw](https://github.com/mitaclaw)

Dolphin 5.0? What is a feature from that era doing in this progress report? Well, you may remember the Branch Watch Tool from its showing in the [progress report for February, March, and April](https://dolphin-emu.org/blog/2024/04/30/dolphin-progress-report-february-march-and-april-2024/#50-21162-branchwatchdialog-a-total-replacement-for-codediffdialog-by-mitaclaw). Determined to make it feature-complete, [ mitaclaw](https://github.com/mitaclaw) continued building upon this reverse-engineering tool in the months following its release. The goal was to finish both of these improvements in time for the

[September progress report](https://dolphin-emu.org/blog/2024/09/04/dolphin-progress-report-release-2407-2409/), but unfortunately the second pull request just barely missed the deadline. Thus, we're covering them both now!

As with the existing features of the Branch Watch Tool, a tutorial on the operation of these new features can be found in the Branch Watch Tool's menu bar, under Tool > Help.

The first new addition to the Branch Watch Tool is the ability to set instruction breakpoints en masse from a row selection. This is potentially useful when a number of branch candidates are found, but the order in which they are hit is in question. Additionally, the context menu shows if the locations selected already have breakpoints set; the large circle icon indicates every location already does, while the small square icon indicates only some locations do.

The second new addition to the Branch Watch Tool is more ways to inspect conditional branch candidates. Before, all one could do was replace a conditional branch with a no-operation instruction (`nop`

). This is equivalent to forcing a conditional branch to always take its false path, but now one can also force a conditional branch to always take its true path by making it unconditional. But that's not all! For any conditional branch, one can now invert the branch's condition (turning `beq`

into `bne`

, `ble`

into `bgt`

, and so on) or invert the branch's decrement check (turning `bdnz`

into `bdz`

, and vice versa).

We hope these new features are helpful to anyone who uses the Branch Watch Tool for research and development.

Among the likes of the code widget or the memory widget, there is the lesser-known JIT widget. Made to assist Dolphin's developers in understanding the output of its just-in-time recompiler, the JIT widget has an incredibly niche userbase. After all, only a fraction of Dolphin's developers are interested in working on the JITs! Thus, it should not be surprising that the JIT widget has not evolved much since its conception.

Apart from surviving the [migration from DolphinWX to DolphinQt](https://dolphin-emu.org/blog/2018/05/02/legend-dolphin-lens-between-worlds), the JIT widget's design and features have remained in 2008*. In its current form, the JIT widget does not display the far-code cache—a memory region where lesser-used recompiled code is sent to—as it predates the concept by [nearly six years](https://dolphin-emu.org/download/dev/master/4.0-3194/)! What's more, using the JIT widget with the Cached Interpreter results in nonsense, as it predates that CPU emulation engine by [nearly seven years](https://dolphin-emu.org/download/dev/master/4.0-7125/)! The large table consuming a great deal of space in the JIT widget is, and always has been, [a placeholder](https://github.com/dolphin-emu/dolphin/blob/24e9fc120c1b02b78cbf854c0eae78df0dbb60c1/Source/Core/DolphinQt/Debugger/JITWidget.cpp#L147)!

It would take a developer seriously interested in Dolphin's JITs *and* in writing Qt widgets for the JIT widget to get the update it deserves. Luckily, that developer has arrived. While [ mitaclaw](https://github.com/mitaclaw) was working on his software JIT profiling restoration, which was featured in a

[previous progress report](https://dolphin-emu.org/blog/2024/04/30/dolphin-progress-report-february-march-and-april-2024/#50-21345-jitcache-software-profiling-restoration-by-mitaclaw), he was simultaneously overhauling the JIT widget to make this profiling data easier to view while also fleshing out this skeleton of a widget. So, what does the JIT widget look like now?



![](../../assets/a78f08fef508ab85.avif)

Packed with new features, it's a huge improvement! For the first time, a list of every cached block of recompiled code is displayed by the JIT widget. It is also now possible to erase selected blocks of recompiled code from the JIT's cache, forcing them to be recompiled again for debugging purposes. The "PPC vs Host" action available from the code widget's context menu, which in the past was the only route to the functionality of the JIT widget, has been generalized as a filter option in the JIT widget (the "Recompiles Physical Address" input field). Finally, the missing support for the far-code cache and the Cached Interpreter has been addressed. Our hope is that, for the few people this drastic overhaul matters to, it can greatly benefit their work.

**This Release's Contributors...**[¶](https://dolphin-emu.org#this-releases-contributors)

Special thanks to [all of the contributors](https://github.com/dolphin-emu/dolphin/graphs/contributors?from=2024-09-04&to=2024-12-01&type=c) that incremented Dolphin by 323 commits after Release 2409!

**What's Up with the Blue Banner?**[¶](https://dolphin-emu.org#whats-up-with-the-blue-banner)

You might have noticed that we've added a banner for the [Stop Killing Games](https://www.stopkillinggames.com/) movement at the top of this website. If you're curious why, we'd like to take the opportunity to explain in a format less cramped than a small banner.

2024 has been a year of bad news for the emulation scene. Nintendo not only forced [Switch emulator Yuzu](https://www.eurogamer.net/switch-emulator-yuzu-shuts-down-as-creator-agrees-to-pay-nintendo-24m) and [Switch emulator Ryujinx](https://www.pcgamer.com/gaming-industry/switch-emulator-ryujinx-goes-offline-after-creator-gets-an-offer-from-nintendo-they-cant-refuse/) to shut down, but also [hit 3DS emulator Citra as collateral damage](https://www.pcgamer.com/software/nintendo-3ds-emulator-citra-taken-offline-as-collateral-damage-in-yuzu-settlement/). The US Copyright Office [refused to let researchers remotely access emulated versions of out-of-print copy-protected video games](https://arstechnica.com/gaming/2024/10/copyright-office-libraries-cant-share-remotely-emulated-versions-of-physical-games/) even though it's already allowed for other forms of media. And Sega will [delist SEGA Mega Drive & Genesis Classics from Steam on December 6](https://www.theverge.com/2024/11/7/24290671/sega-classic-games-delisted), one of the few ways to legally get direct downloads of ROM files.

All of this goes to show that corporations in general don't really care if people can still play old games. Sure, the big classics like Super Mario Bros. will probably keep getting rereleases in perpetuity, but a lack of financial incentive for rereleasing less popular games has led an estimated [87 percent of older games](https://gamehistory.org/study-explainer/) to go out of print. The community is eager to help preserve video games, but they're held back by the current state of copyright law, and if you ask the [Entertainment Software Association](https://www.theesa.com/) (the video game industry's lobbying organization in the United States), [they'd very much like to keep the law as it is](https://www.gamedeveloper.com/business/esa-org-won-t-cooperate-game-preservation).

But still - at least for older consoles - the emulation scene is alive and kicking. For newer consoles, even if emulators aren't being developed right now, that time can come in the future. And even though old games can be hard to legally get hold of for the average person, the history of the console space so far has shown that few video games are at risk of being completely lost to time.

With one big exception: online-only games.

In the year the GameCube launched, console games that let you connect to the internet were a rarity, and popular PC games like Counter-Strike expected you to host your own server if you wanted to play online. Today, fueled by the rise of live service games, many multiplayer games can only be played by going online and connecting to the publisher's servers. There are now even single-player games that require a connection to a server! The mobile market is even worse, as games that can be played offline are the *exception to the rule* there. This is inconvenient if you don't have a reliable internet connection or if there are server outages, but the insidious part is what happens once the publisher loses interest in the game. Not only do they stop selling the game, but because they also shut down the servers, every copy of the game becomes unplayable in one fell swoop. Emulators aren't of much help when a game doesn't even work on the original hardware!

This is what the Stop Killing Games movement wants to stop. Their position is that when you buy a game as a one-time purchase, the company behind the game shouldn't be allowed to later render it unplayable. They're presenting the problem not only as a matter of game preservation but a matter of consumer rights, and through that angle, they're trying to get through to lawmakers and consumer protection agencies. Depending on the laws of your country, when you buy a product, it usually comes with some kind of warranty where if the product breaks within a certain timespan due to a defect that's the manufacturer's fault, they have to repair the product or refund you. But what about when you buy a live service game? The game's servers might shut down at any time, and you usually won't know the date until the shutdown is already imminent. So far, games companies haven't gotten any real pushback from consumer protection agencies for this.

In more concrete terms, the movement is trying to create change in two ways right now, both of which are detailed on [the Stop Killing Games website](https://www.stopkillinggames.com/). The first is asking consumers who bought the recently shut down Ubisoft game The Crew to complain to their consumer protection agency. The second is petitioning legislators in various countries. In particular, [their European Citizens' Initiative](https://citizens-initiative.europa.eu/initiatives/details/2024/000007_en) is currently ongoing, and the petition of theirs is the most likely to end up making a change. But it has a tough goal to meet: **one million signatures**.

The outcome of Stop Killing Games won't directly affect Dolphin, since GameCube and Wii games aren't being made anymore. But as a project that would like to see video games both from the past and the future preserved, we recommend that you sign [their European Citizens' Initiative](https://citizens-initiative.europa.eu/initiatives/details/2024/000007_en) if you can! Note that **you must be an EU citizen to sign**.

**Does it matter if I sign?**[¶](https://dolphin-emu.org#does-it-matter-if-i-sign)

Yes! This isn't some change.org petition where nothing in particular is guaranteed to happen. If a European Citizens' Initiative hits one million signatures, it will be taken to the European Commission. The Commission isn't guaranteed to turn the proposal into law - they'll first thoroughly evaluate the proposal, and then decide what they think is best to do - but other European Citizens' Initiatives have led to real change before. And the EU is no stranger to taking a stand against big tech companies to [improve things for consumers](https://www.theverge.com/24040543/eu-dma-digital-markets-act-big-tech-antitrust) and [fight planned obsolescence](https://www.euronews.com/green/2023/06/22/new-eu-law-to-force-smartphone-makers-to-build-easily-replaceable-batteries). But if the one million mark isn't reached, nothing will happen... Except maybe video game companies looking at the hundred thousands strong signature count and [ceding some ground](https://www.pcgamer.com/games/racing/after-eating-it-for-killing-the-crew-ubisoft-promises-to-bring-offline-support-to-the-crew-2-and-the-crew-motorfest/)?

**How would this even work? Would publishers have to keep servers online forever?**[¶](https://dolphin-emu.org#how-would-this-even-work-would-publishers-have-to-keep-servers-online-forever)

No, they wouldn't be required to keep servers online forever. The proposal by Stop Killing Games would still allow selling games that require a connection to the publisher's servers, and would still allow the publisher to shut down those servers whenever they want to end support for the game. But before they would be allowed to shut down the servers, they would have to take steps to make the game playable without any connection to the publisher. There's various ways to accomplish this, and they're free to choose whichever one suits a given game best. For instance, for a single-player game, they could release a patch that makes the game playable offline. Or for a multiplayer game, they could release the server software, or create a patch that lets the game host matches peer-to-peer. The requirement would be to keep the major functionality of the game working, with the company having an option to leave out less critical parts like matchmaking or leaderboards.

It would mean extra work for companies that make live service games, that's true. But it would take much less work if the game is designed with the requirement in mind to begin with, and the requirement isn't much more onerous than some other regulations live service game developers have had to deal with for the benefit of users, like [the GDPR](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation). And in the end: do we want a world where consumers buy games that might stop working at any time, where people making games are spending their time and effort on something the publisher will erase from existence as soon as it's no longer profitable, and where old games won't be available for the next generation of players? If we don't, then that extra bit of work is necessary.