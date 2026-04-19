---
title: 'Dolphin Progress Report: Release 2512'
url: https://dolphin-emu.org/blog/2025/12/22/dolphin-progress-report-release-2512/
author: OatmealDome
published: '2025-12-22'
source_blog: Dolphin Emulator - GameCube/Wii games on PC
source_site: https://dolphin-emu.org/
category: graphics
fetched: '2026-04-19'
---

With the holiday season reaching its apex, we have a few surprises for those of you that have been patiently waiting. The latest release of Dolphin is stuffed with treats. Our first present is presentation - *frame presentation*, that is. Two new options have arrived and will help users both reduce latency and smooth out games that struggle with frame pacing.

Some games do outright naughty things that make emulation difficult. A slew of them are being coerced onto the nice list this year thanks to a sack full of patches that bypass their troublesome behaviors. Fans of the Broadband Adapter (BBA) have a great present tailored just to them: a new local mode BBA! Designed for allowing multiple instances of Dolphin on the same computer to connect together, it's perfect for use with Parsec or other similar services. And perhaps another gift will have you singing your favorite Wii hits?

But alas, what fun would the holiday season be if we spoiled all the gifts? Read on to unwrap the latest edition of the Dolphin Progress Report.

...

...

Huh? We've received word that apparently the *Android users* have made the nice list? Really? That can't be right... but this gift is addressed to them.

After *more than a couple* bumps in the road, RetroAchievements support has finally arrived on the Android version of Dolphin! In Release 2512, the core achievement experience is now available in your pocket. This initial version hasn't quite reached parity yet with the desktop experience, but we didn't want to hold things up any longer. The important thing for Android RetroAchievements users is that you can log in and unlock achievements in [supported GameCube games](https://retroachievements.org/system/16-gamecube/games). Because some menus are incomplete, it may be best to have the [RetroAchievements website](https://retroachievements.org/) open in the background for achievement lists and other things while we finish up the in-app UI.

**Notable Changes**[¶](https://dolphin-emu.org#notable-changes)

All changes below are available in Release 2512.

Latency was once a huge challenge for emulators, and it is still a major concern. At one point not too long ago, it was pretty much infeasible for most emulators to match the latency of their console counterparts. Compared to a dedicated game console racing the beam on a CRT television, emulators had to deal with sluggish OS window managers with on-by-default triple-buffer V-Sync holding three frames back, first-gen wireless controllers that added latency right at the source of input, slower displays that added several [additional frames of latency](https://www.gamesindustry.biz/digitalfoundry-tech-focus-battle-against-latency) (much more if that display was a TV without game mode), and on top of everything the emulator still needed to do its job and take time to actually emulate everything.

Dolphin *just* missed out on the worst of this. By the time Dolphin's performance and compatibility were good enough for users to worry about things like latency, the overall situation had improved dramatically. Low latency and high refresh rate monitors paired with features like [Exclusive Fullscreen](https://dolphin-emu.org/blog/2014/07/31/dolphin-progress-report-july-2014/#40-2286-d3d-exclusive-fullscreen-by-armada651) removed most of the major bottlenecks that emulators had to fight against.

The designs of the GameCube and Wii *also* afford Dolphin some opportunities that other emulators don't have. The GameCube/Wii are double buffer V-Sync'd by default, resulting in a final input latency of roughly 60ms on a CRT in an optimized 60fps title. However, because of [how the XFB Output Pipeline works](https://dolphin-emu.org/blog/2017/11/19/hybridxfb/), Dolphin has the opportunity to bypass the buffers and grab those XFB copies early, and immediately present them directly to the screen. We call this feature *Immediately Present XFB*, and it cuts out quite a bit of the latency present on the console.

Tricks like these let Dolphin match console latency as long as the host device is capable enough. On extremely optimal setups with low latency VRR monitors combined with *Immediately Present XFB*, Dolphin could even dip a frame *below* real console latency!

There are some caveats, though. While *Immediately Present XFB* is a powerful tool for reducing latency, it is also a hack that relies on games behaving in a specific manner. If a game messes with the XFB pipeline, such as if it applies post processing using the CPU, or stitches together multiple XFB Copies, the hack will cause Dolphin to output nonsensical garbage.



![stitching-RS2.png](../../assets/96d201f8c64047ae.jpg)

FLICKER WARNING

FLICKER WARNING

**intense**flicker.

Click/tap to Play.

Even when *Immediate* isn't outright breaking the game, the XFB pipeline is a big part of how some games handle frame pacing, so bypassing it can make the game feel less smooth. For the best experience in many games, a user probably would prefer superior latency *and* good frame pacing.



![marioparty4quickdraw_thumb.avif](../../assets/787e40c707a00a41.avif)



![fzero43_thumb.avif](../../assets/b45cf30b27497ab3.avif)

[F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX)pushes players to their limits with grueling courses and unforgiving opponents. Any extra latency only makes things harder.

And that was ** Billiard's** goal. He saw an opportunity to improve the situation and started work on two new options. One feature was a way to reduce latency without disrupting how the game rendered, and the other would allow smoother frame pacing even in games that struggled on real console. How would he accomplish these feats? Well, by making the emulator throttle

*smarter*.

Modern computers are powerful enough to emulate [ most](https://wiki.dolphin-emu.org/index.php?title=Star_Wars_Rogue_Squadron_III:_Rebel_Strike) GameCube and Wii games faster than the original hardware could run them. Disable the framelimiter and try it for yourself! To keep emulation on pace, Dolphin’s

*Throttle*function stalls emulation to produce a

*mostly*properly paced simulation of the original hardware. Throttling is necessary for playable emulation on modern systems, but making the host CPU wait

*adds time*. If input from the user and stalls are aligned poorly, throttling can add a small amount of latency.

To address this, Billiard has added a new throttling mode called *Rush Frame Presentation*, where throttling becomes centered around presenting the frame as soon as it can after the input is read. In theory, this reduces the time between click and photon and can have a very noticeable effect, especially in lower frame rate titles. To the end user, all of this is completely invisible. All of this is happening *sub-frame*, so Dolphin still will throttle the appropriate amount of time to maintain the correct frame rate.

The faster your computer, the more of an effect this will have because it will be able to emulate the part of the frame faster. We can easily catch the difference in [The Legend of Zelda: Wind Waker](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_The_Wind_Waker) and [Super Mario Sunshine](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Sunshine) by using a high speed camera, for example.

Click/tap to Play.

Some games will also see a *further* benefit by combining *Immediately Present XFB* with *Rush Frame Presentation*. Unfortunately, this combination can lead certain games to looking gnarly as they will just be spitting out the image at whatever point they're finished rendering during a frame. That's why the second new option is important.

**Smoothing Things Out**[¶](https://dolphin-emu.org#smoothing-things-out)

*Immediately Present XFB* could already cause poor frame pacing, and now *Rush Frame Presentation* could make it even worse. In some games, it can get so poor that VRR monitors will fall out of their operating range!

*Smooth Frame Presentation* allows Dolphin to delay presentation by roughly 1-2ms so that it can more consistently output frames, using previous frame times as a heuristic. This option can be used in any game that has poor frame pacing in order to try to improve the situation.



![ImmediateRushNoSmooth_thumb.avif](../../assets/d69c79ac8de618f7.avif)



![ImmediateRushSmooth_thumb.avif](../../assets/ada766f42221f830.avif)

The results of *Smooth Frame Presentation* are good enough that a lot of games that needed the XFB Output Pipeline enabled by default because of frame pacing issues can now take advantage of the lower input latency provided by *Immediately Present XFB* and *Rush Frame Presentation* without any noticeable side-effects.

Even if you're using neither of the latency features, some games just have bad frame pacing even on real console. *Smooth Frame Presentation* can help them, too. There are rare cases, especially when using *Rush Frame Presentation* alongside *Immediately Present XFB*, where a game's output will be so inconsistent that smoothing won't help. We're looking at you, [Dragon Ball Z: Budokai](https://wiki.dolphin-emu.org/index.php?title=Dragon_Ball_Z:_Budokai).



![dbzb.png](../../assets/1f2c538fecb300df.png)

**Outside Verification**[¶](https://dolphin-emu.org#outside-verification)

All of these results sound great, but outside of a few camera tests on lower frame rate games, we were mostly trusting latency offset numbers *provided by Dolphin*. Testers did also report better latency, but given that the [placebo effect](https://en.wikipedia.org/wiki/Placebo) exists and these are such small differences, we wanted more concrete data. But other than just *game feel*, how do you test latency?

In the past, we've used the light sensor present on [Rock Band 3](https://wiki.dolphin-emu.org/index.php?title=Rock_Band_3) guitars alongside an in-game synchronization test to get some very rough offset values. The problem with that is that it will only ever test one game, and the guitar controller isn't particularly viable in most games outside of unusual controller runs.

Before making any claims about our latency, we wanted to do our due dilligence in respect to both Dolphin and real hardware. To accomplish this, we contacted some professionals that have been fighting against latency for quite some time. ** Fizzi** from

[Slippi.gg](https://slippi.gg/)and adapter expert

**graciously donated their time and helped us measure latency in the latest version of Dolphin versus console.**

[Arte](https://github.com/JulienBernard3383279)

[Arte](https://github.com/JulienBernard3383279)[specifically developed a GameCube controller adapter with a photon sensor](https://www.input-integrity.com/)designed to determine controller latency, which is rather convenient because

*that's exactly what we want to measure*.

Their GameCube controller adapter polls the controller at 1000Hz, and a light sensor on it can be programmed to look for certain changes in output from the game. By having access to both the source of the input and the change on the screen, the adapter can provide a real world measurement of how exactly how long it takes for a user input to result in a change on the display - what is commonly referred to as "click to photon". As an added bonus, the adapter can also be hooked up to real console with no conversion or added latency, letting us compare directly with games running on real hardware and a CRT.



The exciting thing about these numbers is that they confirm our experience. Dolphin's latency compares favorably to console. To be fair to the GameCube, ** Arte**'s emulation setup included a modern low-latency 144Hz monitor and the lowest latency controller adapter. Dolphin couldn't quite compete with Slippi, but most of that can be attributed to deep modifications to how

[Super Smash Bros. Melee](https://wiki.dolphin-emu.org/index.php?title=Super_Smash_Bros._Melee)outputs.

For all the samples above, an input bug present in the original game has been patched out. This is to make getting consistent results a little bit easier. That fix did mean that combining *Rush Frame Presentation* and *Immediately Present XFB* no longer benefited that title when testing. However, ** Arte** modified the test to work with other games, and some games respond incredibly well when combining Rush and Immediate.



Due to time constraints with holiday vacations, adjusting the photon sensor for different games, we weren't able to gather all of the numbers we wanted from other games. However, with [Wind Waker](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_The_Wind_Waker) the numbers were interesting enough that we managed to get enough samples *right under the wire*, at least in Dolphin. The graph above shows latency with default settings, *Immediately Present XFB* and the combined efforts of *Immediately Present XFB* and *Rush Frame Presentation*. Note that the default settings were measured last, and as such the error range is estimated.

The reason why we wanted to squeeze in this particular case is because it demonstrates that combining *Rush Frame Presentation* and *Immediately Present XFB* can result in lower latency than what was possible before. This is not always true, and this 10ms reduction is from an ideal example. Unmodified [Melee](https://wiki.dolphin-emu.org/index.php?title=Super_Smash_Bros._Melee), for instance, showed the combination reducing latency by less than 4ms. Some games saw no benefit from combining both features together.

In the end, how much these two new options will help varies greatly depending on the game and setup. Currently, we've left them both disabled by default in the Configuration -> Advanced Tab, but that may change as the settings get more testing and we gauge what users want the most.

Unlike the wacky Wii Remote and its mess of attachments, the GameCube Controller mostly mirrors modern controllers. Sure, the sticks can't be pushed in, it's missing a shoulder button, the two stage analog+digital triggers can be tricky, and the face buttons are weird. But at the end of the day, it's a four face button, twin stick controller with a D-pad. Close enough?

So we have added an SDL Profile that players can use to speed up their GameCube controller mapping.

Using the profile is simple:

- Go the GameCube "Standard Controller" mapping window.
- Select your controller from the Device dropdown. Pick the variant that starts with "SDL".
- Select the
`SDL Gamepad (Stock)`

Profile and click Load. - Optional: Calibrate your joysticks (please don't skip this Hall effect users!) and set up deadzone.
- Enjoy.

Since the GameCube controller doesn't map 1:1 to modern controllers, this is a *best guess* stock profile that will *reasonably* work for most people, most controllers, and most games. If a game demands a button combination that doesn't work with your hands on your controller, or if the face buttons or any other button simply aren't to your liking, you can build from the stock profile and adjust everything until it's just right.

[2509-237](https://dolphin-emu.org/download/dev/master/2509-237/) and [2509-339](https://dolphin-emu.org/download/dev/master/2509-339/) - **Add Option to Reset Settings Back to Default** by [JoshuaVandaele](https://github.com/JoshuaVandaele) and [Simonx22](https://github.com/Simonx22)[¶](https://dolphin-emu.org#2509-237-and-2509-339-add-option-to-reset-settings-back-to-default-by-joshuavandaele-and-simonx22)

[2509-237](https://dolphin-emu.org/download/dev/master/2509-237/)

[2509-339](https://dolphin-emu.org/download/dev/master/2509-339/)

[JoshuaVandaele](https://github.com/JoshuaVandaele)

[Simonx22](https://github.com/Simonx22)

Dolphin is a complicated emulator with a lot of options. Some of it is definitely our fault, and some of it is just the reality of trying to emulate something as complicated as the GameCube and Wii. To the average user, a lot of these settings aren't immediately obvious, even with descriptions.

"*Emulated Memory this? EFB, XFB that, VBI what?*"

The most experienced users (and even developers) can sometimes get frustrated enough with an issue that [percussive maintenance](https://en.wiktionary.org/wiki/percussive_maintenance) is necessary, leading to one changing lots of settings around until *something* happens. Sometimes this works, leading to a temporary moment of joy, before it all comes crashing down when none of your other games will boot. Some people might be able to backtrack and figure out what went wrong, but a lot of users are left lost.

Until recently, users had to delete the Dolphin settings files from their computer to restore everything to default. No one liked that, but a button to reset settings was non-trivial thanks to [Dolphin's multiple layers of settings](https://dolphin-emu.org/blog/2017/07/01/dolphin-progress-report-june-2017/#50-4171-videoconfig-port-to-layered-configuration-system-by-merrymage) that are a handful to manage.

Thankfully, ** JoshuaVandaele** was finally able to sort out all of the implementation details and give us the long awaited "Reset All Settings" button.



![](../../assets/485d3d1de2fddfdb.png)

*settings*. It will not delete things like controller profliles or game save data.

Thanks to ** Simonx22**, Android users also get access to this feature. It can be found in the advanced settings menu in the Android GUI.

[2509-217 - GamePatch: Modify Certain Games to Behave Better in Dolphin](https://dolphin-emu.org/download/dev/master/2509-217/) by [SuperSamus](https://github.com/SuperSamus) with additional contributors[¶](https://dolphin-emu.org#2509-217-gamepatch-modify-certain-games-to-behave-better-in-dolphin-by-supersamus-with-additional-contributors)

[2509-217 - GamePatch: Modify Certain Games to Behave Better in Dolphin](https://dolphin-emu.org/download/dev/master/2509-217/)

[SuperSamus](https://github.com/SuperSamus)

Some games are more strenuous to emulate than others. Sometimes it's because the [game pushes the console](https://wiki.dolphin-emu.org/index.php?title=The_Last_Story), and other times it's because the game does something [annoying to emulate - maliciously or not.](https://dolphin-emu.org/blog/2025/09/16/dolphin-progress-report-release-2509/#2506-29-game-patch-defang-the-disney-trio-of-destruction-by-josjuice-and-billiard)

The latter situation can be especially frustrating, as sometimes 99% of what the game does is fine, with just *one* little behavior, design decision, or sometimes even an underlying bug causing problems for Dolphin.

** SuperSamus** identified a few common game behaviors that causes Dolphin a lot of headaches. Properly fixing these issues would difficult, with some requiring large rewrites to the emulator that probably will never come. Fortunately, there is a simpler solution: patch out the difficult to emulate game behaviors. These small patches increase emulation performance, and sometimes even work around other unwanted behaviors.

**Complex Idle Loops**[¶](https://dolphin-emu.org#complex-idle-loops)

Idle loops are a sequence of instructions that makes the CPU run laps doing nothing while it waits for something to happen. Obviously, emulating a CPU burning cycles doing nothing isn't efficient for an emulator, so one of Dolphin's earliest optimizations was the ability to detect and skip these idle loops. This feature is fairly standard among emulators and is called *Idle Skipping*.

Idle loops are more common than you might think. It's very rare for a game to absolutely max out the console's CPU, so *for the majority of frames* the CPU will idle a bit. And as long as Dolphin can detect the idle loops, they can be skipped to increase overall performance. *Idle Skipping* is one of the key things that make some areas of a game more demanding than others, especially on the CPU side of things. Essentially, *Idle Skipping* is less effective the more that the CPU has to do.

Dolphin can't detect all idle loops, and the scope of what it can find is rather limited. We have to find as many idle loops as accurately as possible while also ensuring that we don't invest too much time and resources into finding them. The more complex the heuristic is, the more of an impact it will have on the JIT. As such, some games have annoying idle loops that we know about but are not worth detecting.

[Need for Speed: Nitro](https://wiki.dolphin-emu.org/index.php?title=Need_for_Speed:_Nitro) and [Rayman Raving Rabbids](https://wiki.dolphin-emu.org/index.php?title=Rayman_Raving_Rabbids) are two such games with these complex idle loops. After examining their code in detail, ** SuperSamus** realized that their idling behaviors could be modified with a patch that would allow Dolphin to more easily detect and skip them.

This results in *massive* performance boosts, especially in lighter areas, with some menus running at four times as fast. Of course, heavier areas see less of a benefit. We'll have a chart showing some of the raw numbers at the end.

**Running Uncapped**[¶](https://dolphin-emu.org#running-uncapped)

Dolphin is not a cycle accurate emulator. In fact, Dolphin is fundamentally not designed to be cycle accurate, especially with GPU operations. Dolphin's emulated GPU was designed to be **infinitely fast**, only being limited by other factors like CPU emulation or the maximum performance of the host device. Nowadays, it has been tamed a bit with synchronization points that provide a rough approximation of the timings of the original [command processor](https://dolphin-emu.org/blog/2025/09/16/dolphin-progress-report-release-2509/#processor-processing), but it is still by no means accurate, let alone *cycle* accurate. Also, rendering is still infinitely fast, as the only thing that limits it is the speed of your host GPU.

And yet, most games run at the correct frame rate, because they *limit themselves*.

The GameCube and Wii were designed for analog TVs, so they used the analog television's sign to start a new frame as a synchronization point called the [Vertical Blanking Interupt (VBI)](https://dolphin-emu.org/blog/2023/02/12/dolphin-progress-report-december-2022-january-2023/#50-18271-video-hack-vbi-skip-by-sam-belliveau). All a game had to do was start a new frame every time it saw a VBI and finish the frame before the next VBI, and it would be perfectly synchronized to the frame rate of the display. That's it. It was simple and efficient, so the vast majority of GameCube and Wii library tie their frame rates to the VBI. Thanks to that, Dolphin's early developers didn't even need to care about how fast the emulated GPU runs; as long Dolphin emits VBIs at the correct frequency, most games will just run at the correct frame rate regardless of what's going on under the hood. And this gives Dolphin bonuses like not emulating GPU slowdown, allowing games that struggled on console to perform much better in Dolphin.

But the GameCube and Wii don't have operating systems. Games run on the bare metal and have full control of the machine, so developers could do *whatever they wanted*. And some games eschew the VBI and run **uncapped**.

Uncapped games break Dolphin's assumptions. They can render way, *way* too fast. For example, when running [Hulk (2003)](https://wiki.dolphin-emu.org/index.php?title=Hulk) in Dolphin, it only displays at 60 FPS, but the physics engine could be doing hundreds of steps per second behind the scenes. This is cool because technically a game like this can easily be hacked to run at higher frame rates, but *terrible* because it hammers people's devices with all kinds of unnecessary work!

It gets even worse from here. The physics engine's independence from the output frame rate isn't *perfect*. If the number of steps per second gets too high, small rounding and math errors start to accumulate, and parts of the game not properly tuned to run at these higher frame rates start to break. This mostly results in dialogue timing issues, but in one stage halfway through the game, it causes a physics calculation issue where a required ledge can't be climbed, essentially softlocking the player.



![hulk2003_thumb.avif](../../assets/d8c6c29a574a68e2.avif)

Some other games choose to synchronize to the VBI, but don't bother in incredibly simple scenes where the frame rate doesn't matter. This is most commonly seen with splash screens and loading screens. One such game with this behavior is [Bully: Scholarship Edition](https://wiki.dolphin-emu.org/index.php?title=Bully:_Scholarship_Edition). Most of the time it is perfectly stable, but because the loading screens are uncapped, it can actually cause the game to randomly hang on transitions. [The Simpsons Hit & Run](https://wiki.dolphin-emu.org/index.php?title=The_Simpsons_Hit_%26_Run) also has this issue, but only during the initial load. While most desktop computers are able to handle the initial load relatively well, Android users have reported tremendous slowdowns where the loading time would take more than 45 seconds.

** SuperSamus** identified these problems and either created patches for these behaviors themselves, or helped others with those titles create patches. Most of these patches are only one or two lines and simply limit the game's frame rate to the VBI frequency. The patches prevent the game from slamming Dolphin's overpowered emulated GPU, greatly increasing performance while fixing issues caused by the games running internally at too high of a frame rate.

This comes with a little bonus - since they are now bound to the VBI frequency, you can now use *VBI Frequency Override* to adjust their frame rate up or down as desired, allowing Dolphin to take advantage of the fact that these games "support" running at higher frame rates.

In addition to the games above that had emulation bugs caused by framelimiting, ** SuperSamus** and

**also created limiter patches for the following games purely for performance reasons:**

[Billiard](https://github.com/jordan-woyak)


Somewhat ironically, by slowing down uncapped games we improve their performance in Dolphin, so when turning off Dolphin's framelimiter they go much faster. ...ignore that and use this as a measure of their performance improvement. If a game's frame rate doubled in this chart, then the performance required to run that game at fullspeed has been roughly halved.

These numbers don't tell the whole story on some of these games. [Hulk (2003)](https://wiki.dolphin-emu.org/index.php?title=Hulk) and other games which ran uncapped would get progressively worse performance in Dolphin depending on how *light* the scene was to render.

As a final reminder, these patches should not be considered proper solutions to fixing uncapped games. They are purely to increase playability of these titles.

**Eggmania: Eggstream Madness**[¶](https://dolphin-emu.org#eggmania-eggstream-madness)

The *Force Progressive Output* patch we included for the Japanese version of this game was causing it to crash on boot. Since we were adding new patches and ** extrems** had already pointed us to a

*correct*version of the patch, we decided to update it alongside all of the other patches.

Despite being the Japanese version of a rather obscure game, this crash was somehow reported multiple times by different users. For the two of you out there waiting, the fix is finally here.

[2509-242 - BBA: IPC for BBA Between Multiple Instances of Dolphin on the Same Machine](https://dolphin-emu.org/download/dev/master/2509-242/) by [cristian64](https://github.com/cristian64)[¶](https://dolphin-emu.org#2509-242-bba-ipc-for-bba-between-multiple-instances-of-dolphin-on-the-same-machine-by-cristian64)

[2509-242 - BBA: IPC for BBA Between Multiple Instances of Dolphin on the Same Machine](https://dolphin-emu.org/download/dev/master/2509-242/)

[cristian64](https://github.com/cristian64)

The Broadband Adapter (BBA) for the GameCube was all about connecting games to a network. Whether across the hall with a Local Area Network (LAN) or across the continent with the information superhighway, the BBA brought Nintendo consoles together like nothing before it! Well, except the [Modem Adapter](https://dolphin-emu.org/blog/2024/04/30/dolphin-progress-report-february-march-and-april-2024/#50-21253-implement-modem-adapter-by-fuzziqersoftware), but we're not talking about that today.

Dolphin has supported the BBA emulation for many years. An early LLE implementation was fairly accurate, but required the user to setup TAP servers and suffered from performance bottlenecks with said TAP servers depending on the operating system. It wasn't until [BBA-HLE](https://dolphin-emu.org/blog/2022/09/13/dolphin-progress-report-july-and-august-2022/#50-16838-add-hle-broadband-device-by-schthack-and-many-additional-fixes-by-sepalani) in 2022 that BBA emulation became readily accessible to the average user.

![](../../assets/34eed6a955e20794.jpg)


![](../../assets/34eed6a955e20794.jpg)

BBA-HLE is great if you want to connect Dolphin to another computer or real hardware. But if you want to run multiple instances *on the same computer*, things get more complicated. While it was technically possible through networking trickery, it was far beyond what we'd expect of the average user.

** cristian64** realized that this problem could be pretty cleanly solved by using a library called

`cpp-ipc`

. This library would allow *separate instances*of Dolphin on the same machine to share data easily and efficiently through Inter-Process Communication (IPC). Instead of using a network stack, we can just simulate the instances of Dolphin being in their very own network and let them communicate without the need for any outside support.

With BBA-IPC added, here's a quick rundown of the many options you have for BBA.

**Broadband Adapter (TAP)**: Dolphin's LLE solution for the Broadband Adapter that requires a TAP interface.**Broadband Adapter (XLink-Kai)**: LLE solution that can connect to the Xlink-Kai service to allow players on separate networks to connect together. Success highly depends on each game's latency tolerance and the latency between the players.**Broadband Adapter (HLE)**: HLE solution that hooks the Broadband Adapter up to the host's network interface to connect with other devices on the network or to a server for certain online games.**Broadband Adapter (IPC)**: HLE solution that allows Dolphin instances on the same machine to share memory and communicate directly without the need for a host network.

BBA-IPC allows for easy testing of BBA features on a single PC, and can also be used in conjunction with game streaming services like Parsec to play BBA titles over the internet without needing to meet the strict latency requirements of emulating the BBA over the internet. This is admittedly a rather niche usecase for BBA, but the feature is relatively compact and easy to maintain.

Currently, only Windows and Linux are supported by BBA-IPC, but if there is enough interest, ** cristian64** has already found another library that could let us support this in other operating systems.

Playing [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii) online in Dolphin back when WFC support was first added was a rather rough experience. It was functional, but slow and stuttery, just enough to be playable and help players with preserving traffic to the official WFC in the final months before the servers were finally shut down.

But that wasn't the end. Thanks to revival efforts, many Wii games still have online communities, with [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii) being quite possibly the biggest. In the years since, Dolphin's Wi-Fi emulation has gotten to the point that users can play alongside real Wiis in most games without any issues.

Well, *most* users. Unfortunately, even in modern builds of Dolphin there were a couple of users having severe stuttering and freezing problems, and all of them were using Android devices. These problems were handwaved away as typical Android performance issues at first, but after closer examination, it was obvious that there was something else going wrong. One user recorded us tons of examples and helped narrow down what was happening.

Click/tap to Play. File has audio.

They (accurately!) surmized that it had something to do with a player joining or leaving the online lobby. In [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii), players can join or leave a race mid-match, with new players spectating until the next race began. The only mystery left was figuring out why this was only happening to a couple of users while everyone else was fine.

Using their wealth of knowledge from working on the [Monster Hunter Tri](https://wiki.dolphin-emu.org/index.php?title=Monster_Hunter_Tri) [replacement Wi-Fi servers](https://forum.wii-homebrew.com/index.php/Thread/60432-Monster-Hunter-Tri-private-server-progress/), ** sepalani** jumped in and investigated the issue. Same as us, they couldn't find any issues at first. They were able to play without any kind of freezing, even on their phone. However, after unlocking the frame rate on a desktop computer,

**noticed a small hitch when the function**

[sepalani](https://github.com/sepalani)`InetAToN`

was called. This hitch was impossible to see when running at normal speed, but when running at 1000%+ speed, the dip was just barely noticeable.`InetAToN`

is a standard networking function that takes an IP address string and converts it into its equivalent binary form. For example, the string `192.51.100.50`

would be transformed into the hexadecimal number `0xC0336432`

. On the Wii, `InetAToN`

has some additional functionality that is unusual: in addition to text-based IPs, it also accepts *hostnames* as inputs. This means that a developer can choose to pass a hostname like `google.com`

into `InetAToN`

, and the function will perform a [Domain Name System](https://www.cloudflare.com/en-us/learning/dns/what-is-dns/) (DNS) lookup to resolve the hostname into an IP address.

** sepalani** figured out that if a hostname was provided to

`InetAToN`

and the resulting DNS lookup was slow enough, the function would cause a stutter because Dolphin waits for the result of the lookup before continuing. The time it takes for a DNS lookup to finish varies depending on various factors, such as the user's internet connection. On a desktop PC connected to home internet, the lookup would complete before the user even saw a frame drop. But many of our Android users are connected to the internet via cellular data, which can have particularly poor latency depending on signal strength and network congestion.Therefore, ** sepalani** changed

`InetAToN`

to be non-blocking so that DNS resolution can take as long as it wants without locking up the emulator.There's no way to sugarcoat this one. This was a pretty bad %$#& up. Dolphin's SD card emulation was broken, and has been broken for a very long time. Yet somehow, *it worked*. This is one of the dangers of emulation - sometimes you can do something very wrong yet the software just trudges on.

The modern Wii homebrew scene lives off of SD Cards. It's a convenient tool available on *most* Wiis, and can be used in conjunction with the [Homebrew Channel](https://wiki.dolphin-emu.org/index.php?title=Homebrew_Channel), BootMii, and other essential homebrew. It's not uncommon to see a 32GB SD card in a Wii loaded with homebrew emulators, software, and game mods.

One oddity about the Wii is that it was released *without* support for the then new [SDHC standard](https://en.wikipedia.org/wiki/SD_card#SDHC) (2GB to 32GB SD cards). This would be rectified in [an update three years later](https://wiibrew.org/wiki/System_Menu_4.0), but the damage was done. [Thanks to the way Nintendo designed the Wii's software stack](https://hackmii.com/2009/02/why-the-wii-will-never-get-any-better/), games released prior to SDHC support being added would be forced to use older IOSes that lacked SDHC support. Even if your System Menu, homebrew, and newer games worked with your big SD card, a game like [Super Smash Bros. Brawl](https://wiki.dolphin-emu.org/index.php?title=Super_Smash_Bros._Brawl) wouldn't. At least without some help.

The [Brawl](https://wiki.dolphin-emu.org/index.php?title=Super_Smash_Bros._Brawl) community refused to be restricted by Nintendo's paltry limitations. They used homebrew to load the game with newer IOS versions and even patched the game to remove the nonsensical 3 minute time limit on replays. Small patches like these were just the beginning, as the community started making bigger changes to the game, like balance patches Brawl+ and Brawl-, and eventually full game overhauls like Project M and its offspring.

The Smash Bros. community is still pushing the limits of homebrew on both the Wii and Dolphin. One such effort is [Super Smash REX](https://www.rexbuild.site/). REX has an astounding amount of stages, music, and characters to the point that just the base mod is over *8GB* in size. And that's where we come into all of this.

A developer from REX reached out to us about how they were reaching some kind of limit with the virtual SD card in Dolphin. Once the amount of data on the SD card exceeded **10.7GiB**, Dolphin's SD card support would completely fall apart.

This actually wasn't *too surprising*. There have been scattered reports from [Rock Band 3](https://wiki.dolphin-emu.org/index.php?title=Rock_Band_3) and [Just Dance](https://wiki.dolphin-emu.org/index.php?title=Category:Just_Dance_(Series)) failing when too much DLC was installed to the SD card. However, reproducing those issues required owning a mountain of DLC, which none of us did. With REX, everything was readily available and the actual launcher was just a homebrew application. This made reproducing the issue much easier, and they did most of the work for us.

The key detail was that the files on the SD card didn't even have to relate to the mod. We could just fill it with cat pictures, load up the [Homebrew Channel](https://wiki.dolphin-emu.org/index.php?title=Homebrew_Channel) or any other homebrew that relied on the SD card, and watch the fireworks. What could be going wrong?

In a community as old as the GameCube/Wii scene, there are some voices that *must* be heeded. Before the REX developers reached out to us, one of the Supreme GameCube/Wii Sages, ** extrems**, hadst been prognosticating doom since the new year if a bug with the card ID (CID) and card-specific data (CSD) registers in our SD card emulation was not mended. Verily, it came to pass.

The problem was extremely straightforward. When the emulated Wii queried the virtual SD card for its capabilities, such as size and speed, Dolphin would return *complete garbage* due to the reports being in the wrong byte order. The strange part of this was that SD card emulation even worked *at all*.

When REX reported there were SD card issues, we quickly thought of the flaws that ** extrems** pointed out to us. However, knowing the problem and fixing it were two very different things. Our attempts to make things right only made things worse. Two different developers took a stab at it, and both left SD card emulation completely non-functional. We were left defeated and efforts on the problem slowed.

In mid-November, ** Billiard** was perusing

**did finally get to reviewing it, he saw that it**

[Billiard](https://github.com/jordan-woyak)*also fixed Dolphin's CID and CSD byte ordering*.

A few quick reviews and a rebase later, and the bug was finally quelled. Now Dolphin properly works with virtual SD cards up to 32GB in size.

The Logitech Microphone is an iconic accessory for the Nintendo Wii. [Roughly 100 games](https://wiki.dolphin-emu.org/index.php?title=Category:USB_Microphone_(Input_supported)), including popular titles in the [Guitar Hero](https://wiki.dolphin-emu.org/index.php?title=Category:Guitar_Hero_(Series)) and [Rock Band](https://wiki.dolphin-emu.org/index.php?title=Category:Rock_Band_(Series)) series, support the peripheral.

Dolphin has had support for the *physical* Logitech Microphone via USB Passthrough for years, but even as other USB peripherals received their emulated counterparts, those wanting to sing into an emulated Wii using generic microphones had to wait. [Even the maligned Wii Speak received support](https://dolphin-emu.org/blog/2025/06/04/dolphin-progress-report-release-2506/#2503-580-wii-speak-emulation-by-shuffle2-degasus-noahpistilli-and-sepalani) before the Logitech Microphone, despite the fact that it supported far fewer games and was much more complicated to implement. This is just how emulation works sometimes. The more complicated, less useful accessory was just far more interesting than the popular, yet generic accessory.

But the foundation created for emulating the Wii Speak did lend itself well toward implementing a second microphone accessory in Dolphin. After all, the Wii Speak *was* a microphone, so a few people took shots at adapting the Wii Speak code to work with the Logitech Microphone.

First, [supermilkdude67](https://github.com/supermilkdude67) posted a WIP fork with very basic support that fizzled out. A few months later, [a certain announcement](https://retroachievements.org/forums/topic/32317) brought renewed interest toward making the many singing games more accessible to users. ** Biendeo** took over the mantle using the initial fork as a base. With some help from veteran Dolphin developers, a few fixes, and some upgrades to the GUI, it was ready to go.



![logitechmicsettings_thumb.avif](../../assets/130b51522cedc121.avif)

You can now emulate the Logitech Microphone with any standard PC microphone! The exact volume levels might need to be adjusted depending on the input source, so make sure you properly calibrate before your first jam session. Given that this is a new feature, compatiblity isn't perfect, and some games may take more fiddling than others.

For our Android users, things aren't ready yet. While the core feature should be mostly compatible between the two environments, it will need a completely different GUI. As such, it might be a while before everything gets ported over to our Android builds.

Dolphin's On-Screen Display is an important part of communicating with users, whether it's statistics, performance metrics, or notifications from features like RetroAchievements. Unfortunately, the pixel font we were using could be hard to read, especially for some users with HiDPI screens. ** TryTwo** improved the situation by

[adding the ability to change the font size of on-screen display messages](https://dolphin-emu.org/download/dev/master/2509-59/), but this didn't solve the problem - making a pixel font larger can look quite bad, especially at non-integer scales. Dolphin needed a new font that could scale to arbitrary resolutions while still looking clear.

With this change, Dolphin's OSD now uses a proper vector font!



![](../../assets/9f7ef72e2ab7b9dd.png)



![](../../assets/1cae6d9f8430bc8b.png)



![](../../assets/74debcb5e50f3f0d.png)

Vera Sans Mono is the new default font. We think that in pretty much every scenario, it's easier to read than our old font. However, ** TryTwo** figured that since we were adding a font anyway, that Dolphin could just provide the ability for users to override the font. So if you're unsatisfied with our typography tastes, add the font of your choice to the "Load" folder of your User directory and name it "OSD_Font.ttf". Any TrueType font will work!

Now that the On-Screen Display has even more options, we've decided to consolidate them within their own config section. So if you're looking to adjust what is displayed, font size, or if you want them disabled altogether, the settings can now be found in one place within the On-Screen Display section of the Configuration window.

If you were an arcade junkie in the late 90s and early 2000s, then you're probably familiar with the Midway classic * NFL Blitz*. Authentic teams thrust into a deliberately inaccurate simulation with colorful gameplay and flashy graphics made the series a bombastic hit in arcades. And of course, the blisteringly difficult AI that would

*absolutely cheat*drained quarters from avid players, making it enticing for arcade owners as well.



![nfl-blitz_thumb.avif](../../assets/96675a2d90e6d6e1.avif)

[ReBoot](https://en.wikipedia.org/wiki/ReBoot)."Writer 2: "It's from 2000."Writer 1: "Oh..."

Image Credit:

[arcadesmarket.com](https://arcadesmarket.com/products/nfl-blitz-arcade-with-lots-of-new-parts-extra-shop)In this, we're not talking about beloved or hated arcade games, but instead the home console exclusive [NFL Blitz Pro](https://wiki.dolphin-emu.org/index.php?title=NFL_Blitz_Pro). This attempt to adapt to the console landscape was a commercial failure that lacked the charm and personality of the earlier titles. And we can confirm the popularity thing - this title had broken audio by default in Dolphin for *over four years* with no one making a formal bug report and only two forgotten comments throughout our community.

It wasn't until ** Billiard** was testing games to see if they worked with

*Immediately Present XFB*that we became aware that the game's sound was broken.

![](../../assets/4ffd6476b16cc76d.png)

After doing some quick testing, ** Billiard** realized that DSP-LLE resolved the issue, and with no further leads he made a setting adjustment and

[disabled HLE audio for this game by default in 2509-551](https://dolphin-emu.org/download/dev/master/2509-551/).

![24-hours-later.avif](../../assets/f3f0294189194450.avif)

The very next day, ** flacs** saw the audio regression, found what build broke it, figured out why it was broken,

*and*fixed the issue.

[NFL Blitz Pro](https://wiki.dolphin-emu.org/index.php?title=NFL_Blitz_Pro)is another game that uses the low-pass filter. In Dolphin, the low-pass filter was notoriously broken and left

[completely disabled for many, many years](https://dolphin-emu.org/blog/2021/08/01/dolphin-progress-report-june-and-july-2021/#50-14712-dsp-hle-re-enable-low-pass-filter-by-flacs-original-fix-by-merrymage). During the process in which the feature was finally fixed and re-enabled, no one thought to test this game. If we had, we would have noticed that it hit an edge-case in the HLE implementation of the low-pass filter.

When the game reserves a region of memory, its memory allocator sets all bytes within the region to `0xAB`

. This behavior isn't necessarily abnormal, as the initial state of the memory shouldn't matter. When using freshly allocated memory, it is best practice to first initialize it with sane default values before attempting to use it. Unfortunately, the developers of [NFL Blitz Pro](https://wiki.dolphin-emu.org/index.php?title=NFL_Blitz_Pro) forgot to perfom this initialization when reserving memory for the game's audio engine. The [MusyX library](https://www.ign.com/articles/1999/07/30/the-musyx-experience) determines if the low-pass filter is enabled by checking if the appropriate bytes within its assigned memory region are not zero. Because `0xAB`

is not zero, the library assumes that the low-pass filter should be enabled.

Because most audio related memory is still in the default state of `0xAB`

, the two low pass filter coefficients are *also* set to `0xABAB`

. When DSP-HLE goes to calculate how much the low-pass filter should quiet or amplify things, it adds these values together. For our purposes, the values are interpreted by the game as 16-bit fixed point values, so the coefficients would be roughly `1.341156`

. These two values *added together* are supposed to add up to about `1.0`

, but in this case the result is roughly `2.682312`

. DSP-HLE sees this number and boosts the volume accordingly, making things sound rather unpleasant.



The programmers were using uninitialized memory by accident, which is a game bug. Regardless of their intent, these were the values that the game used. So why was Dolphin broken? ** flacs** figured out that the second filter value is actually a

*signed*value. For a typical 16-bit fixed point value, this means positive values are

`0x0000`

to `0x7FFF`

, and negative values are `0x8000`

to `0xFFFF`

. `0xABAB`

is supposed to be interpreted as a *negative*value.

With the bug fixed, the equation changes to `1.34 + (-0.66)`

, giving us a coefficient sum of roughly `0.68`

. The filter is still active and now *lowering* the volume of the game, but this is accurate to real hardware. It seems that the developers worked around the filter's unintentional activation by just making the game louder to compensate. By handling these uninitialized values correctly, DSP-HLE now produces proper audio in this title.



**This Release's Contributors...**[¶](https://dolphin-emu.org#this-releases-contributors)

Special thanks to [all of the contributors](https://github.com/dolphin-emu/dolphin/graphs/contributors?from=2025-09-15&to=2025-12-21&type=c) that incremented Dolphin by 585 commits after Release 2509!