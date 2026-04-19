---
title: 'Dolphin Progress Report Tenth Anniversary Special: February, March, and April
  2024'
url: https://dolphin-emu.org/blog/2024/04/30/dolphin-progress-report-february-march-and-april-2024/
author: Mitaclaw
published: '2024-04-30'
source_blog: Dolphin Emulator - GameCube/Wii games on PC
source_site: https://dolphin-emu.org/
category: graphics
fetched: '2026-04-19'
---

[In late 2012](https://forums.dolphin-emu.org/Thread-dolphin-has-a-new-website), Dolphin moved to a brand new website - [dolphin-emu.org](https://dolphin-emu.org/). With complete control of our own home and infrastructure for the first time, we noticed the accessibility to users that it gave us. Not only did we get a new home, but we also got a *platform*, one that allowed us to communicate directly to our users! We used it to great effect, explaining big changes to the emulator such as [tev_fixes_new](https://dolphin-emu.org/blog/2014/03/15/pixel-processing-problems/), getting ahead of controversy when we [removed the popular D3D9 graphics backend](https://dolphin-emu.org/blog/2013/10/12/d3d9-why-its-not-part-dolphins-future/), [calling out broken drivers](https://dolphin-emu.org/blog/2013/09/26/dolphin-emulator-and-opengl-drivers-hall-fameshame/), and more! The Dolphin Blog was born!

However, we quickly realized that while single dedicated articles were great for big changes, Dolphin was improving *all the time* and tons of important and/or interesting changes were being overlooked simply because they weren't "big enough" to warrant a feature article. We needed something that would let us cover the continuing development of the emulator. Something like, a periodical article filled with a collection of *notable changes*, so we could *report* on the *progress* of Dolphin within a set window of time. And after much experimentation, we built a format to fulfill this role, and released the first of its kind to the world on the 30th of April, 2014.

Ten years ago today, the [first Dolphin Progress Report was launched](https://dolphin-emu.org/blog/2014/04/30/dolphin-progress-report-april-2014/)! Since then, our blog has exploded in popularity, and tens of thousands of people read every Report! And in that time, we've made **79** Dolphin Progress Reports, with **797** Notable Changes, **54** special sections, and **301,807** words! Thanks for reading!

As the writers of the Dolphin blog, we are proud of what we have accomplished here. We've highlighted tons of cool changes, educated our users (and ourselves!) on how Dolphin works, we've helped reel in fresh talent for the emulator, we've helped people get into universities and launch their careers, and even helped a few people meet their life partners! Progress Reports have been so impactful, that they have reached far beyond Dolphin. The once novel concept of emulator Progress Reports has become *a standard means of user communication throughout emulation!*

But of course, ten years is a long time, and we've changed along the way and will continue to change over time. The Reports may grow or shrink, become more or less frequent, structure and style may change, and writers may come and go. And truth be told, *this is hard*, and we nearly reached the breaking point a few times along the way. But no matter what happens, as the writers of the Dolphin Blog, it is our goal and our hope that for as long there are Notable Changes being made to Dolphin, there will be Progress Reports to feature them!

Speaking of which, anniversary or not, this is a Progress Report. We have Notable Changes to cover! So without further ado, please enjoy the Tenth Anniversary Dolphin Progress Report, and the last Dolphin Progress Report of the 5.0 era.

**Surprise!**[¶](https://dolphin-emu.org#surprise)

OK, a little further ado. We have prepared a little something to celebrate this Anniversary. Enjoy!

Now back to our regularly scheduled Dolphin Progress Report.

**Notable Changes**[¶](https://dolphin-emu.org#notable-changes)

In March 2024, ** Geotale** found a crash in Dolphin and drilled it down to its root cause. GameCube software runs on the metal - it has absolute control of the hardware without any operating system whatsoever. In order to save console-wide settings, such as mono versus stereo audio, the GameCube stores 64 bytes of data in a battery-backed SRAM chip. Whenever a game boots, it will read the battery-backed SRAM and collect these settings without asking the user to set stereo sound over and over again. Normally, games don't try to read or write beyond the 64 byte mark, but if they for some reason were to do that,

**found that Dolphin would access memory beyond the end of the memory buffer it allocates for SRAM data.**

[Geotale](https://github.com/Geotale)** ElectrifiedStrawberry** then wrote up a bug report about the issue to relay it to the Dolphin developers. Upon seeing the report,

**quickly realized that the bug might be exploitable by specifically crafted software to take control of Dolphin, and fixed the problem by adding a bounds check. As far as we know, nobody has tried to exploit this bug yet, but to be on the safe side, we decided to release an out-of-schedule Beta release just a few days later to get the fix out to users.**

[JosJuice](https://github.com/JosJuice)How come one missing bounds check can open up for exploits of this magnitude? If you've read about differences between different programming languages, one term you might have come across is *memory safety*. [Even the White House](https://www.whitehouse.gov/oncd/briefing-room/2024/02/26/press-release-technical-report/) talked about it recently! In a memory safe language, trying to access memory beyond the end of a buffer or trying to access memory using a pointer that doesn't even point to valid memory to begin with is either impossible or handled in an orderly way. For instance, Java raises an `ArrayIndexOutOfBoundsException`

or `NullPointerException`

respectively for these situations, and the programmer can either write code to handle these exceptions in whatever way they prefer, or ignore the exceptions and have the program crash. But Dolphin is written in C++, which isn't memory safe. While nowadays there are languages that target both memory safety and good performance, like ** Rust**, back when Dolphin was started in 2003, all the available memory safe languages came with notable performance penalties. And when emulating a

*cutting-edge*console like the GameCube, you need all the performance you can get!

In C and C++, going beyond the end of a buffer or using an invalid pointer is formally *undefined behavior*, meaning literally anything could happen. In practice, usually one of two things happens. If you try to access memory that the operating system considers to be invalid, the program normally crashes. While that may be unpleasant for the user, it's safe in the sense that there's no way for an attacker to exploit the behavior. On the other hand, if you try to access memory that the operating system thinks your program should be allowed to access... then the program accesses that memory. This is exactly what happens in the bug ** Geotale** found. If you go beyond the buffer allocated for SRAM data, you'll start accessing

**other parts of Dolphin's memory**, which are valid memory regions but were never intended to be accessed by the emulated software! As mentioned before, we're not aware of anyone having created an exploit for this, but because Dolphin stores lots of important data after the SRAM buffer and because the emulated software can freely mix reads and writes and can skip over addresses it isn't interested in, it's likely that it would be possible to create an exploit that escapes out of the emulated console.

While in theory a program written in C or C++ can be memory safe if carefully written to avoid bugs, writing a large program without bugs occasionally slipping in is really, really hard, bordering on impossible. So unfortunately, there's a risk of bugs like this being found lurking when someone unearths a part of Dolphin's code that hasn't been touched in a long time. But when bugs like this are found, we take them seriously and move to fix them.

Last year, **Cristian64** noticed that there were black lines always present to the right and bottom of the image whenever Dolphin was in Windowed mode. They looked into it, and found some errors in how Dolphin's aspect ratio correction interacts with our presentation. They posted their findings in our discord, ** Filoppi** whipped up a fix, and that was merged in

[5.0-20048](https://dolp.in/5.0-20048). With that, the cursed black errant pixels were removed from the edges of the screen!

Fast forward to today, and ** Filoppi** noticed that some titles at 1x Native were softer than they should be.

Bisecting the issue, he traced it back to [5.0-20048](https://dolp.in/5.0-20048), his own change! It turns out that the previous presentation fixes brought our old friend *floating point rounding errors* into the party! There are many opportunities for small floating point rounding inaccuracies throughout Dolphin's presentation and aspect ratio correction code, and sometimes (depending on the game and its native resolution) these could add up to incorrectly make Dolphin think that scaling the image *by one pixel* was necessary. This was the cause of our blurring! Apparently the errant pixel borders Dolphin had previously were accidentally shielding Dolphin against this kind of error.

Since realistically* there should never* be a case where scaling by a single pixel is correct*, ** Filoppi** fixed this with a simple exception - if Dolphin decides to scale by a single pixel, pass through the unscaled image instead. Problem solved! Now

[Four Swords Adventures](https://wiki.dolphin-emu.org/index.php/The_Legend_of_Zelda:_Four_Swords_Adventures)and any other affected games are properly crisp at 1x Native once again.

* Next time on the Dolphin Progress Report...

While Dolphin's primary purposes of preservation and enhancement are focused on play, as an emulator we can grant DEEP access to GameCube and Wii hardware and software. Dolphin can be a powerful utility for GameCube and Wii modding and reverse engineering! This change adds a new debugging feature called the *Branch Watch*, a powerful new tool that enables better code searching than ever before!

Since this is a feature by developers for developers, we're not going to hold back. *Let's get technical!*

Back in April of 2022, the [Code Diff Tool was added to the Code View widget](https://github.com/dolphin-emu/dolphin/pull/8732). Created by ** TryTwo** and

**, the Code Diff Tool aimed to replicate a feature of the popular program Cheat Engine called "Ultimap."**

[dreamsyntax](https://github.com/dreamsyntax)![](../../assets/ffcfc8a12c754b34.png)


![](../../assets/ffcfc8a12c754b34.png)

The way the former Code Diff Tool worked was by recycling a JIT profiling feature that had been inaccessible since [the removal of DolphinWX in June of 2018](https://dolphin-emu.org/blog/2018/07/06/dolphin-progress-report-june-2018/#50-8279-remove-dolphinwx-by-spycrab0). By differencing the number of times a block of recompiled code has run since the last time you checked, it was possible to track down sections of the original code that execute only when an action is performed in the emulated software.

Unfortunately, the recycled JIT profiling feature was in no way built for what the Code Diff Tool was trying to do, leading to some limitations. The Code Diff Tool was not compatible with the Interpreter due to the Interpreter not being a JIT (obviously), nor was it compatible with the pseudo-JIT we call the Cached Interpreter due to that JIT lacking the profiling feature. It was also susceptible to JIT cache clears happening out of its control, interfering with progress in any ongoing diff. For semi-arbitrary design reasons, the Code Diff Tool required debugging symbols to operate. A diff would only include recompiled blocks of code associated with the starting address of a debugging symbol, which was problematic when the start of a function may never be recompiled as its own block due to branch following optimizations in the JIT(s). Additionally, the same segment of the original code could be recompiled multiple times, potentially resulting in misleading run counts. Finally, any changes to debugging symbols over the course of a diff would cause some diff results to be unrecognized when checking what has been run since the last check.

Naturally, these limitations were frustrating to work with, but it was ** mitaclaw** who finally grew frustrated enough to try to do something about it. He first set off to improve the Code Diff tool, but eventually he came to the conclusion that JIT profiling data wouldn't cut it any more; Dolphin needed a new component built for the purpose. Thus, the Branch Watch was born.

The job of the Branch Watch is to receive information from the emulated CPU about every executed branch's origin, destination, and PowerPC instruction. It also receives implicit information about the current address translation mode as well as if a conditional branch is taking its true path or false path. After an optimized associative lookup, an entry added to or found in one of the BranchWatch's "Collection" containers will have its hit count incremented by one. From the user-facing Branch Watch Tool, it is then possible to direct the Branch Watch to perform some differencing (not unlike the former Code Diff Tool would) to collate references to the "Collection" containers' entries that meet a given criteria into a separate list - the BranchWatch's "Selection" container. This "Selection" container is what can be seen in the user-facing Branch Watch Tool. The whole process makes viewing the information sufficiently thread-safe, allowing for real-time updates (every 100 ms) to the Branch Watch Tool's interface.

Implementing all of this was a breeze for the interpreter, and support naturally came to the Cached Interpreter as it's barely a JIT. Support for the proper JITs was not so simple. A branch might not be recompiled at all due to the aforementioned branch following optimization. The JITs also have idle loop detection, which can cause specific branches to be recompiled differently. The x86_64 JIT also supports merging PowerPC comparison instructions and PowerPC conditional branch instructions into a single x86_64 instruction that does both. The most involved JIT-ism to support was an optimization for a looping pattern commonly seen when invalidating memory with the `dcbx`

family of instructions. After relentlessly hunting down every corner case, and with ** JosJuice**'s invaluable guidance on writing safe recompiler code, the JITs were finally able to match the Interpreter perfectly.

The new Branch Watch Tool comes with a robust set of options and features to empower code searching. It is possible to filter candidate branches by address and debugging symbol (both at the origin and destination), by true path or false path (for conditional branches), and even by 12 different instruction kinds. When replacing a tool with existing users, it's imperative to leave no feature behind. The authors of the former Code Diff Tool were given council to make sure features from the former Code Diff Tool were not forgotten, such as saving and loading in-progress searches (including an auto-save feature) and "inspecting" results by modifying instructions to stub functionality (previously done inspections are marked with a bold red font). All-in-all, the new Branch Watch Tool should be able to satisfy everyone by providing a superset of features previously available.

If you would like to take the new Branch Watch Tool for a spin, look for the "Branch Watch" button in the Code View widget and check out the Branch Watch Tool's help message tutorial found under Tool > Help. As an aside for non-debugging users, we assure you that this new feature should have zero performance implications for recompiled code when not in use.

The previous Progress Report saw the introduction of the [Custom Aspect Ratio setting](https://dolphin-emu.org/blog/2024/02/10/dolphin-progress-report-november-and-december-2023-january-2024/#50-20785-support-custom-aspect-ratios-by-filoppi), allowing users to set any arbitrary aspect ratio they want! However, we ended that section by warning that the new Custom aspect ratio option bypassed our aspect ratio corrections, and the image would be slightly distorted basically all the time.

Fortunately, ** Filoppi** wasn't through with this feature, and the custom aspect ratio setting now has Dolphin's aspect ratio corrections! If you are using an ultra-wide screen code, you can just set a Custom Aspect Ratio to match your screen and/or code and it will just work, without need to worry about or compensate for subtle aspect ratio issues!

However, if you liked the old behavior, you can use the new "Custom (Stretch)" option, which still does not have any aspect ratio correction.

Ever since [Dolphin added its own Wii Remote driver that allowed for using the Wii Remote as a configurable controller in Dolphin](https://dolphin-emu.org/blog/2020/04/05/dolphin-progress-report-february-2020/#50-11684-add-support-for-wii-remotes-over-inputcommon-by-billiard), one of the biggest questions has been "When is Infrared Support coming?" Dolphin's Wii Remote driver could do just about anything with the Wii Remote, include using it to simulate almost all Wii Remote functions and *even* passthrough the battery level to the emulated game. But, when it came to infrared, there was no way to properly handle it on a standard Wii Remote, and you'd be forced to use the "Real Wii Remote" setting or Bluetooth Passthrough if you wanted to use a sensor bar for infrared data.

![](../../assets/d00a3f73e79a4403.png)


![](../../assets/d00a3f73e79a4403.png)

"Point Passthrough" is a new feature for Dolphin's Wii Remote driver that allows you to use a real sensor bar with the emulated Wii Remote option.

Some of you may be scratching your head after reading that, as there *is* a way to get the Wii Remote pointer working with Dolphin's Wii Remote driver. However, that method of getting the pointer working doesn't use infrared at all, it simply simulates the Wii Remote's pointer direction using the MotionPlus gyro (and is compatible with non-Wii Remotes that have a gyro) and uses that to *reasonably* simulate the controller's position in 3D space, from which Dolphin can calculate where the Wii Remote is pointing. This is what lets players easily play games like [Super Mario Galaxy](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Galaxy) on modern controllers with gyro capabilities.

There are some limitations to this, and people with Wii Remote hardware have long been asking for *real* infrared support with our Wii Remote driver. Unlike real infrared, which has a physical reference in space, gyro infrared suffers from drifting and you have to manually recenter it (usually with a button combo on the controller) once in a while. In most games this isn't too bad, but if you're doing a lot of rapid movements, gyro aiming can fall apart fast! There are also some cases where the gyro simulation didn't produce accurate enough results. Here are some of the best examples where infrared support makes a big difference.

![](../../assets/6330e1e840ee7d6e.jpg)

**Features**[¶](https://dolphin-emu.org#features)

-
**Netplay**- In netplay, only emulated controllers can be used due to the strict requirement of absolute determinism. This means you cannot fall back to using the "Real Wii Remote"*or*the Bluetooth Passthrough settings. However, since[5.0-11684](https://dolphin-emu.org/blog/2020/04/05/dolphin-progress-report-february-2020/#50-11684-add-support-for-wii-remotes-over-inputcommon-by-billiard)physical Wii Remotes were still usable on netplay through connecting Wii Remotes for emulated controllers. A lack of infrared support meant that using a real Wii Remote on netplay had the hard requirement of having MotionPlus if you were using the pointer. This also meant any game that requires precise pointer controls would not work. We'll have some examples later. -
**Savestates**- Saving the state of the emulator is always a perilous task. Each of Dolphin's methods of handling Wii Remotes affects savestates differently.-
Bluetooth Passthrough makes things

*very*difficult, because we use a*real hardware Bluetooth Adapter directly*- and we cannot save the state of that physical device. There*is*limited savestate support, but it requires the user to get the adapter to match the state it was in when the savestate was made. You could accomplish this by connecting the same Wii Remotes in the same order with the same attachments and hope that Wii Remotes are using the same reporting mode as when the savestate was made. Otherwise? It'll deadlock. -
Real Wii Remotes

*aren't as bad*, but users aren't exactly thrilled by our softlock workarounds. As mentioned above, Wii Remotes have various reporting modes, and because we're dealing with a physical device outside of the emulator, we can't simply restore it to the state it was in when the savestate was made. In order to prevent potential softlocks with Wii Remotes, Dolphin will*disconnect and reconnect*Wii Remotes on loadstate. This resets the state of the Wii Remote to ensure they match, but results in a small delay on loadstate and the game potentially complaining that the controller was disconnected. It may sound annoying, but it is also greatly increases the stability of savestates for Wii games. -
Emulated Wii Remotes have none of these problems, as the thing the game is directly communicating with is within Dolphin's ecosystem. This means that Dolphin can just restore the state of the emulated Wii Remote, without the need for any workarounds or mitigations for softlocks. This is because the "physical" controller just communicating through our driver to our emulated controller. With the new Point (Passthrough) feature, you can get the full benefits of a real sensor bar and savestates all at once. Perfect for speedrun practice or getting past a difficult pointer puzzle.


-

**Game Specific**[¶](https://dolphin-emu.org#game-specific)

-
- This game in particular asks a lot of the Pointer, having you swap between pointing at the screen and pointing off screen. Gyro Point struggles with pointing far off screen, so oftentimes users would have to map the hotkey "hide pointer" in order to get the game to behave in a reasonable manner. With a real sensor bar, it just works.[Super Paper Mario](https://wiki.dolphin-emu.org/index.php?title=Super_Paper_Mario) -
- This is a rather funny case that really messes with our Gyro Pointer. Skyward Sword[The Legend of Zelda: Skyward Sword](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_Skyward_Sword)*already uses the gyro for its pointer*, using infrared only for a reference point and for active recalibration to combat drift during play. This means when Dolphin is using the gyro to generate the pointer position,[Skyward Sword](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_Skyward_Sword)is using our emulated point in space to correct for gyro drift, yet our emulated point in space is from the same gyro that it is trying to recalibrate.*Calibrating a gyro to itself*results in a lot of wonky pointer behavior, but users have made it work with complex control schemes and copious recentering. Using a real sensor bar with emulated Wii Remotes gets the game behaving just as it does on the Real Wii Remote options. -
,[Trauma Center](https://wiki.dolphin-emu.org/index.php?title=Category:Trauma_Center_(Series)),[Another Code R](https://wiki.dolphin-emu.org/index.php?title=Another_Code:_R_-_A_Journey_into_Lost_Memories)and other precision pointer games - Unlike the other situations, there wasn't an easy workaround for these games when using Gyro Point. These games have various levels where you're required to push the Wii Remote toward the screen or pull it away from the screen. While games can use the accelerometer for this, they[WarioWare: Smooth Moves](https://wiki.dolphin-emu.org/index.php?title=WarioWare:_Smooth_Moves)*also*use the sensor bar's two clusters of lights as a reference point. When you push the Wii Remote closer, the two clusters separate more, and that's how the game can tell the Wii Remote is closer to the screen. Gyro Point has*no way of handling this currently*, and the only way to make this work without a real sensor bar is to map a bunch of emulated movements to the controller. While this is possible, you get a very different experience and using a real sensor bar keeps it simple and authentic.

**Limitations**[¶](https://dolphin-emu.org#limitations)

With this major update to the emulated Wii Remotes, the bridge between Real Wii Remotes and Emulated Wii Remotes shrinks further. Considering that we still have *three* different ways of connecting Wii Remotes, one may question when it'd be time to simplify things. Unfortunately, Emulated Wii Remotes still have a few shortcomings that make Real Wii Remotes a necessary option.

While things like battery life work, unfortunately physical Wii Remote Speakers aren't supported on the Emulated Wii Remote. Many users (and developers) may argue speaker data doesn't work properly even on *Real Wii Remote*, but one feature that is definitely missing on Emulated Wii Remotes is the Wii Remote Eeprom. This Eeprom could store a small amount of data, usually for Miis. Real Wii Remote *does* support this, but this might be very complicated to support within our driver.

If you want to try out infrared support, it's automatically mapped correctly when loading Dolphin's default Wii Remote profile. To try it out, go to the Motion Input tab and disable the standard "Point" setting that uses the Gyro, and enable Point (Passthrough). That will allow you to use your real sensor bar.

![](../../assets/ba5265837dc3e266.png)


![](../../assets/ba5265837dc3e266.png)

**HDR Enhancements**: [5.0-19931 - Add AutoHDR post process shader](https://dolp.in/5.0-19931) by [Filoppi](https://github.com/Filoppi) and [5.0-21232 - Add HDR to Metal + Perceptual HDR](https://dolphin-emu.org/download/dev/master/5.0-21232/) by [samb](https://github.com/Sam-Belliveau)[¶](https://dolphin-emu.org#hdr-enhancements-50-19931-add-autohdr-post-process-shader-by-filoppi-and-50-21232-add-hdr-to-metal-perceptual-hdr-by-samb)

[Filoppi](https://github.com/Filoppi)

[samb](https://github.com/Sam-Belliveau)



*HDR is currently very challenging to demonstrate in browsers. Frustrated, the blog authors resorted to old memes. We apologize in advance.*

Several months ago, ** Filoppi**'s

**was merged, which gave Dolphin the ability to properly emulate the gamma and color space of the GameCube and Wii. The difference isn't significant, and since it results in slightly reduced brightness and saturation it could be considered undesirable, hence it being off by default. But more accuracy is more accuracy, and even subtle improvements are important for a mature emulator such as Dolphin!**

[5.0-19716 - Support Accurate NTSC/PAL Color Spaces](https://dolphin-emu.org/blog/2023/08/13/dolphin-progress-report-may-june-and-july-2023/#50-19716-support-accurate-ntscpal-color-spaces-by-filoppi)However, to facilitate accurate gamma and color spaces, Dolphin needed more control over the host display. Ironically, this required Dolphin to support **HDR**. High Dynamic Range is typically used to display a *larger* color space, yet this feature was using it to *limit* the color space to accurate levels. Regardless of the reasoning, this change added the *HDR Post-Processing* feature to Dolphin.

What happened next was easy to see coming.

In ** 5.0-19928**,

**added an HDR enhancement shader to Dolphin! A "slimmed down port" of**

[Filoppi](https://github.com/Filoppi)**'s prior**

[Filoppi](https://github.com/Filoppi)[Reshade shader](https://github.com/Filoppi/PumboAutoHDR), our AutoHDR shader is designed to be

*additive*- it expands highlights into HDR luminance while leaving the rest of the image unmodified. This gives games a bit more pop while still mostly maintaining their original SDR look.

AutoHDR has several options to allow users to dial in the experience.

- Shoulder Pow - Modulates the Auto HDR highlights curve. Low values bleed a bit into midtones to give a gentle, soft edge around the HDRified highlights, while high values only brighten the hightlights for pin sharp edges.
- Shoulder Start Alpha - Determines how bright the source SDR color needs to be before it can be used to generate fake HDR highlights
- HDR Display Max Nits - Sets the maximum brightness of the HDR highlights

If you want to closely follow the original look of the game but add a little HDR pop, AutoHDR is for you! Do note however that GameCube and Wii games have *very primitive* lighting models, more primitive than what AutoHDR was originally designed for. More often than not, our AutoHDR shader will benefit from tweaking for each individual game's lighting quirks.

For a bit more pop, ** samb**'s

**brings PerceptualHDR, a much more HDRy enhancement option! PerceptualHDR uses a logarithmic approach to its**

[5.0-21232](https://dolphin-emu.org/download/dev/master/5.0-21232/)[inverse tonemapping](https://en.wikipedia.org/wiki/Tone_mapping)curve. This results in brightness and saturation scaling that looks more "natural" to the eye, though less accurate. It also has the side effect of making it very tolerant of the poor lighting models of GameCube and Wii titles, and reducing the need for customization! It also has higher saturation and brightness overall, with a more "HDR look". However, PerceptualHDR significantly changes the look of the game, and is definitely not for those pursuing accuracy.

The two shaders have very different looks and goals, neither one is "better" than the other. AutoHDR is very conservative, trying to enhance but respect the original look. Plus it is very customizable, allowing it to adapt to any game's lighting. Meanwhile, PerceptualHDR throws out the original look for all the HDR pop it can offer! While it is generally more tolerant, it is also not customizable (outside of amplification), so if a game doesn't work well with it you're basically out of luck, but AutoHDR can be adjusted to match. Whichever shader you use is up to you and what you'd like out of an HDR enhancement!

To demonstrate these differences, we're going to need to go into the *High Dynamic Range!*

**HDR Block**[¶](https://dolphin-emu.org#hdr-block)

Click the image below to enter the HDR Block, an addendum article where we use cutting edge browser features to show you actual HDR comparisons rendered in your very own browser!

You'll need an HDR display to see the differences, so if you are using an SDR display, feel free to skip.


![](../../assets/d7992c177c1ddffa.jpg)


![](../../assets/d7992c177c1ddffa.jpg)

Now that we have established the differences and options, it's time for us to *temper your expectations.*

The GameCube and Wii are entirely SDR consoles with very basic lighting models that were designed for small and dim displays. They are absolutely not designed for HDR. By dragging them kicking and screaming into high dynamic range, we are putting these games that have no idea what HDR is in charge of an absurdly powerful display technology.

*Our HDR enhancements are not magic. Expect quirks and problems*.

For example, there is no concept of "paper-white" in these games. While our HDR enhancement shaders differ in their approach and the inverse tone mapping of middle values, the extremes are the same - complete black in SDR space will be complete black in HDR space, and complete white in SDR space will be the maximum HDR output of the shader or your display. If you crank your display brightness to the max, turn on an enhancement shader and crank it to the max, and launch a game that has an entirely white screen, you could be bombarded with thousands of nits of brightness. And guess what console starts *every single game* with a **solid white screen** - the Nintendo Wii!

This was her experience.

You can easily flashbang yourself with these features, so use this power responsibly.

**Furthermore**, if you are using an HDR display without calibrating it, any time you view SDR content *you are already experiencing inverse tone mapping*. Most current generation displays, televisions and phones especially, don't care about accurate SDR recreation and by default boost saturation and brightness way beyond SDR spec. They are *already* turning SDR content into HDR content *by default!*

As such, you may turn on AutoHDR or PerceptualHDR and see a dimmer and duller appearance than you had without any HDR enhancements. If this occurs, our HDR enhancements' inverse tone mapping is more conservative than what you are used to!

The world of HDR is a varied and wild place. With "HDR" spanning everything from 300 nits peak brightness to 10,000, and from 8-bit dithered 50% DCI-P3 to 12-bit 100% Rec2020 reference monsters, HDR can be very different things depending on your display. Our HDR enhancements add to your existing tools for customizing inverse tone mapping on your HDR display, and you will need to use *all of the tools available to you* for best results. HDR is like that.

That being said, if you are ok with experimenting, HDR has a lot to offer as an enhancement. When everything lines up, these HDR enhancements can improve the game's visuals on a scale similar to raising internal resolution! Games like [Super Mario Galaxy](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Galaxy) and [Sonic Colors](https://wiki.dolphin-emu.org/index.php?title=Sonic_Colors) look *great* with these enhancements! HDR is messy and complicated and a pain, but when everything lines up and it works correctly, there is nothing quite like it.

While our Post-Processing shaders will appear on all platforms, our HDR Post-Processing feature is currently only available in our desktop Qt interface, and requires HDR to work. Functionally, that means that currently our HDR enhancements can only be used on Windows, macOS, and *a tiny subset of Linux* (that includes the Steam Deck OLED).

HDR Post-Processing is currently not available on Android.

The GameCube was released in the early days of the ubiquitous internet. In 2001, dial-up was still a normal way to go online, but broadband was increasingly spreading its tendrils throughout the globe, and our chronically-online doom-scrolling future was already well on its way to consuming us all. To facilitate experimenting with this terrifying new frontier, the GameCube had an accessory port on the bottom that could fit the GameCube BroadBand Adapter (BBA), a 10/100mbps ethernet adapter that allowed the GameCube entry to the *information superhighway!*

Since it was an addon accessory for an experimental feature, [it saw limited support in the GameCube lineup](https://wiki.dolphin-emu.org/index.php?title=Broadband_Adapter). Some games used the BBA for its LAN mode, allowing players to connect multiple GameCubes together locally for crazy high player numbers while avoiding that whole scary internet thing. But a select few games dove right into the Online mode, *requiring* an internet adapter and an internet connection! The iconic *Phantasy Star Online* MMO franchise survived the fall of the Dreamcast this way.

However, while the BBA is reasonably well known amoungst GameCube enthusiasts, there was *another* accessory that could go into that port - The GameCube Modem Adapter. This was a 56kbps *dial-up modem* alternative to the BBA. While it lacked the LAN mode, the Modem Adapter granted more or less the same online features as the BroadBand Adapter, just... worse. All online-mode games that supported the BroadBand Adapter also supported the Modem Adapter, so users were expected to just pick the internet adapter that matched their connection and access the same online content. Though, with *some mild variation* in user experience.

*Except,* for one game. There is one game that **requires the GameCube Modem Adapter**, and does not work with the BroadBand Adapter! This game is [Phantasy Star Online Episode I & II Trial Edition](https://wiki.dolphin-emu.org/index.php?title=Phantasy_Star_Online_Episode_I_%26_II_Trial_Edition). The final version of PSO I & II supports the BBA, but its Trial *does not*. Dolphin only supported the BroadBand Adapter, so *for the entirety of Dolphin's existence*, PSO I & II Trial Edition required game modification to be playable in Dolphin!

This change resolves that. [fuzziqersoftware](https://github.com/fuzziqersoftware), a developer behind PSO reverse engineering tools and PSO custom servers, has implemented tapserver-based Modem Adapter emulation in Dolphin! By combining modem adapter emulation with a compatible custom server, [Phantasy Star Online Episode I & II Trial Edition](https://wiki.dolphin-emu.org/index.php?title=Phantasy_Star_Online_Episode_I_%26_II_Trial_Edition) is playable in Dolphin for the very first time without action replay codes or game patches!

Not only is this a win for preservation of this interesting era of GameCube hardware and PSO development, it's also a mark off the very short list of GameCube games that cannot be played in Dolphin without modification.

As was mentioned [earlier in this Progress Report](https://dolphin-emu.org#50-21162-branchwatchdialog-a-total-replacement-for-codediffdialog-by-mitaclaw), software JIT profiling is one of a small group of debug features left inaccessible by the [transition from DolphinWX to DolphinQt](https://blog.dolphin-emu.org/blog/2018/05/02/legend-dolphin-lens-between-worlds/). The underlying feature had a partial return as the component powering the Code Diff Tool, before that tool was replaced with the *Branch Watch Tool* shown previously. Following this, ** mitaclaw** decided he must restore software JIT profiling to its former glory - it's the least he could do after leaving it abandoned once again. It's unlikely this feature will have many users, even among Dolphin's developers, but it's good to see an old feature get rekindled rather than extinguished.

**Last Month's Contributors...**[¶](https://dolphin-emu.org#last-months-contributors)

Special thanks to [all of the contributors](https://github.com/dolphin-emu/dolphin/graphs/contributors?from=2024-02-01&to=2024-04-30&type=c) that incremented Dolphin from [5.0-21090](https://dolphin-emu.org/download/dev/master/5.0-21090/) through to [5.0-21460](https://dolphin-emu.org/download/dev/master/5.0-21460/)!

**Social Media Update**[¶](https://dolphin-emu.org#social-media-update)

We are now maintaining three social media presences: [Mastodon](https://social.dolphin-emu.org/@dolphin), [Bluesky](https://bsky.app/profile/dolphin-emu.org), and [Twitter](https://twitter.com/Dolphin_Emu)!

The content on these accounts will largely mirror each other. Our [Mastodon](https://social.dolphin-emu.org/@dolphin) is our flagship social media presence, it is strongly under our control (literally living on our servers) and truest to our open source philosophy. [Twitter](https://twitter.com/Dolphin_Emu) is our oldest account, with over a decade of history! *Hopefully that will continue.* And finally, our [Bluesky](https://bsky.app/profile/dolphin-emu.org) is brand new! Feel free to follow us on whichever you'd like!

**Why Dolphin Isn’t Coming to the iOS App Store**[¶](https://dolphin-emu.org#why-dolphin-isnt-coming-to-the-ios-app-store)

In early April, Apple shocked the emulation community by updating their App Store Guidelines to permit retro game console emulators on the App Store. While there was some initial debate over whether the new guidelines only permitted "officially-developed" emulators, community-made emulators soon began appearing on the App Store. The floodgates were open.

Ever since this happened, one question we've been frequently asked is "*when will Dolphin come to the App Store?*"

**Unfortunately, due to other restrictions set by Apple, we are not able to release Dolphin on the App Store. This also applies to app marketplaces in Europe, like AltStore PAL.**

The GameCube and Wii both use a PowerPC-based CPU, while most modern devices use x86-64 (Intel & AMD) and AArch64 (ARM) based processors. To be able to run GameCube and Wii machine code, Dolphin uses a Just-in-Time (JIT) recompiler to translate it into code that our modern CPUs can understand. This works well on all of our supported platforms.

There's just one problem: **Apple does not allow third-party apps to use JIT recompilers on iOS and iPadOS.**

Dolphin does have both the Interpreter and Cached Interpreter, which are JIT-less methods for emulating the CPU. However, *they are many times slower than Dolphin's JITs, making them unusable for actually playing games*.

For longer versions of these videos with sound:

[Interpreter](https://youtu.be/aM_jIDCSMcc),[JIT](https://youtu.be/QTg-q1s_awY)There is one very narrow exception to the "no JIT" rule on iOS - alternative web browsers in Europe. This is because many web browsing engines utilize JITs to speed up JavaScript execution. As allowing alternative browsers is required in Europe under the Digital Markets Act (DMA), Apple gave these apps a special exemption in iOS 17.4. However, Dolphin is not a web browser, and Apple has [very specific requirements that they use to check whether an app is really a web browser or not](https://developer.apple.com/support/alternative-browser-engines/#web-entitlement). JITs in web browsers are also subject to additional security requirements, such as [separating the JIT into its own isolated and locked down process](https://developer.apple.com/documentation/browserenginekit/designing-your-browser-architecture). This is extremely problematic for Dolphin, which expects everything to be included in one process. While retooling Dolphin to work within these constraints is *theoretically possible*, it would require a large architectural redesign and a significant amount of effort just for one platform. Apple may also just choose to ban our app in the end anyways for pretending to be a web browser.

After reading about web browsers being able to use JIT recompilers, you may be wondering "*why not just make a version of Dolphin that runs in a web browser?*" Well, easier said than done! To make a usable web version of Dolphin, someone would need to write a brand new JIT targeting [WebAssembly](https://webassembly.org/) *and* add [WebGL](https://www.khronos.org/webgl/) support to our OpenGL video backend. While we don't want to say that a web version of Dolphin is completely impossible, working on one just isn't in any of our plans at the moment.

Another suggestion we've received is that we should use ahead-of-time compilation (AOT) on these platforms. This would involve re-compiling all of a game's code to AArch64 in advance, which lets us avoid having to generate the code on the actual device with a JIT. Unfortunately, having to rely solely on AOT compilation would likely cause several compatibility problems. These issues largely stem from the fact that games are *freely able to self-modify their code*. Some EA games, for example, store their code compressed on disc, and then decompress it at runtime. Other games are even able to *generate entirely new code with a JIT of their own*! The official Nintendo 64 emulator used in Virtual Console releases is one notable example of this, as it includes a JIT for emulation of the Nintendo 64's MIPS-based CPU. Since we aren't able to know with certainty what code will be executed before the game runs, it isn't feasible to use an AOT recompiler as the sole method for emulating the CPU.

As such, barring Apple having another sudden change of heart or some other miracle, an iOS App Store release is off the table for Dolphin.