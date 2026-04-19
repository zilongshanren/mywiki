---
title: 'Dolphin Progress Report: Release 2407 and 2409'
url: https://dolphin-emu.org/blog/75/
author: JosJuice
published: '2024-09-04'
source_blog: Dolphin Emulator - GameCube/Wii games on PC
source_site: https://dolphin-emu.org/
category: graphics
fetched: '2026-04-19'
---

After an exciting round of feature articles, it's Progress Report time once again! However, a lot has changed. Dolphin has finally left the 5.0 era behind, and has entered the *Release Era*. Not only did we get our first release in eight years, but we also established a commitment to continuous releases going forward.

For the Reports, things will be more or less the same, but with a few changes.

Progress Reports are now also *release changelogs*. We'll be going over the notable additions and changes between each release in every Progress Report going forward, rather than within a range of dates. As such, the name of the Reports will reflect the release accompanying it - if you want the new features, just update to the version at the top or higher and you'll have them! (However, since 2407 had a release article without a changelog, this Report will be covering the changes in both Release 2407 and Release 2409.)

That also means that the next release is happening *right now!* Accompanying this report is **Dolphin 2409**. It is now rolling out via our updater, and is available for download here on our website.

But there was also another feature article since our last Report. Dolphin now has RetroAchievements support!

For those waiting for it to show up in a release build, the wait is now over. Throughout the past couple of months, we've ironed out one major issue alongside many smaller issues with RetroAchievements. The first iteration of RetroAchievements in a release build is stable, but not all that flashy. The groundwork is there for future improvements, but many features and options are yet to be finished. As well, Android support is still deadlocked with a few issues. Please pardon our progress!

We have a bunch of cool statistics from the RetroAchievements team regarding the launch, however, we need to get on with the Report! So just [click this handy link](https://dolphin-emu.org#the-first-month-of-dolphin-retroachievements) to be taken to the bottom of the Report if you'd like to read more!

But before we get to the Notable Changes, we have a couple of things to cover.

**Google Play Update Delay**[¶](https://dolphin-emu.org#google-play-update-delay)

Last month, we got a surprise email from Google Play saying that Dolphin doesn't comply with their policies because it "installs, but doesn't load". We have gotten emails like this before regarding Android TV, presumably because someone at Google tried to install Dolphin on one out of the vast majority of Android TV devices that don't meet Dolphin's hardware requirements, but this is the first time we've gotten a rejection for Android as a whole. Seeing as Dolphin generally does load correctly on devices that are able to install it, we're not quite sure what happened here.

What does this mean for Dolphin? Dolphin is still available on Google Play, but the next update we release has to be manually checked by Google before it becomes available to users. Because of this, it will take longer than normal for the 2409 release to show up on Google Play, but any updates after that should be smooth sailing again. If you're impatient and want the latest version of Dolphin right now, it's available [on this website](https://dolphin-emu.org/download/) as always!

**Visual Studio Twenty-Twenty-Woes**[¶](https://dolphin-emu.org#visual-studio-twenty-twenty-woes)

During the rollout of the latest release, a lot of people updated Dolphin for the first time in a while! But for some of our Windows users, when they fired up Dolphin 2407 for the first time they were met *with a silent crash*. They reached out to us, and the support vanguards on our Discord quickly found a solution - reinstalling the 64-bit Microsoft Visual C++ redistributable for Visual Studio 2022 got Dolphin working for them once again.

We're not entirely sure why exactly this happened. But we have a theory.

The Visual C++ 2022 Redistributable is a runtime library that contains everything needed to run programs compiled with Microsoft Visual Studio 2022. However, Visual Studio 2022 *is not static*: there are many subversions, and it gets regular updates. These updates *should* be backwards compatible with any other version of Visual Studio 2022. It would be **madness** to make a change to Visual Studio 2022 that breaks compatibility with Visual Studio 2022's own runtime libraries. However, Microsoft did exactly that.

In Visual Studio 2022 v17.10.0, Microsoft made a non-backwards compatible change to `std::mutex::lock`

. This was [reported to Microsoft](https://developercommunity.visualstudio.com/t/Access-violation-with-std::mutex::lock-a/10664660), however, the issue report was marked as "Closed - Not a Bug". Apparently this was intended!

This puts us, as an application that uses Visual Studio, into a weird place. We set up an automated process to update our Visual Studio builder to new subversions as they come out, confident that it will never break anything. It's just subversions. So we have told our Windows users that all they need to run Dolphin is the Visual C++ 2022 Redistributable, confident that it would work. However, Visual Studio automatically utilized the new version of `std::mutex::lock`

when compiling our Windows builds. If a user is running *an older version of the Visual C++ 2022 Redistributable* before that new version of `std::mutex::lock`

was implemented, they may download and run our program and see a silent crash. And of course, if we ask them if they are using the Visual C++ 2022 runtime, *they'll say yes*, because they have it installed.

According to Microsoft, this is our problem. Their expectation is for applications to be distributed with installers that will include the redistributable and install it with the app if required. However, they hand out the redistributable to users precisely for applications like us that ship without an installer. It's not like what we're doing is novel. And perhaps Microsoft should have made it fail in a way that communicates to the user that they need to update the redistributable, instead of just crashing silently? Or perhaps just include the Visual C++ 2022 runtime libraries *in Windows Update* so every user is guaranteed to have the latest version and applications don't even need to worry about it?

...Anyway, unfortunately, we don't have a great solution for this issue. We could disable our automated update process for our Visual Studio builder, but there are security benefits to keeping it, so this is something we'd rather not do. For now, all we can tell our Windows users is that if you run a new version of Dolphin and encounter a crash, redownload and reinstall Visual C++ 2022 Redistributable. As always, we have a link to the redistributable [on our download page](https://dolphin-emu.org/download/).

On a happier note, it's time for our Notable Changes!

**Notable Changes**[¶](https://dolphin-emu.org#notable-changes)

All of the changes below are available in Release 2409.

When Windows 11 released in late 2021, it brought the first major visual overhaul to Windows since [Windows Phone](https://en.wikipedia.org/wiki/Windows_phone) from 2010. Gone were the sharp edges, bold colours, and dense squares of the *Live Tile* era, and in their place were soft tones, spacious design, and friendly round edges.

However, as part of this new aesthetic, Windows 11 applies round edges *everywhere*, even to game windows! Pixels that your computer spent your hard-earned money rendering are now *hidden* in windowed mode by default.



![](../../assets/45f392e446ee6313.png)

**112 pixels!**With an 8x native window, 0.0005% of your pixels cannot be viewed! What?!


**This was unacceptable!**

Recognizing this *travesty*, ** Filoppi** came to the rescue and saved our pixels. By configuring

`DWM_WINDOW_CORNER_PREFERENCE`

in our Windows builds, all pixels that Dolphin renders (on Windows 11 and in windowed mode) are now once again free to be seen by our illustrious eyeballs.If only such relief could be bestowed upon our macOS users as well...

**Balloon Tooltip Quality of Life Updates** - [5.0-21123](https://dolphin-emu.org/download/dev/master/5.0-21123/), [5.0-21635](https://dolphin-emu.org/download/dev/master/5.0-21635), and [2407-130](https://dolphin-emu.org/download/dev/master/2407-130/) by [Dentomologist](https://github.com/Dentomologist)[¶](https://dolphin-emu.org#balloon-tooltip-quality-of-life-updates-50-21123-50-21635-and-2407-130-by-dentomologist)

[Dentomologist](https://github.com/Dentomologist)

A few years ago we introduced our [custom balloon tooltips](https://dolphin-emu.org/blog/2020/12/10/dolphin-progress-report-october-2020/#50-13163-remove-description-box-in-graphics-tabs-and-use-custom-tooltips-instead-by-iwubcode). Rather than have a large description area permanently taking up space or a terrible native tooltip defined by the OS, we created our own custom tooltips that gave us the best of both worlds.

They have been serving us well since. However, after they were rolled out for the graphics area of our config, they haven't really been *touched* since then. Now that's changing, and our Balloon Tooltips are finally getting some much needed love and a wider rollout!

First is [5.0-21123](https://dolphin-emu.org/download/dev/master/5.0-21123/), which reworked how they are drawn to resolve *many* longstanding quibbles with the tooltips.

Next is [5.0-21635](https://dolphin-emu.org/download/dev/master/5.0-21635/), which added tooltips to the Interface tab of Config.

And finally [2407-130](https://dolphin-emu.org/download/dev/master/2407-130/), which rolls out our tooltips to the General tab of Config!

** Dentomologist** is still chipping away at the tooltips, so expect them to continue to improve and be applied to more windows over time!

After the merge of "Cached Interpreter 2.0", we've seen some misinformation floating around emulation communities regarding what the cached interpreter is and what this change has brought. So for the Progress Report, we felt it was prudent to take a deep dive, and properly explain a bunch of concepts we've been putting off for years now. Strap in everyone, *we're going deep!*

The primary task of CPU emulation is translation: we take code that was originally designed for a specific type of CPU and translate it into something that a different type of CPU can understand. This is not free. Even ignoring the work involved in the act of translating in and of itself (more on that later), having to account for hardware differences means that the resulting translated code will usually be many times larger and more complex than the original code was on the original hardware. As such, there are many different approaches to CPU emulation.

**Interpretation** is the most basic and literal CPU translation method. An interpreter decodes each individual instruction from the emulated architecture (guest), then translates that into the instruction**s** (plural) that allow the host to perform the same work. And yes, it translates *one instruction at a time*. This is extremely accurate (able to preserve all nuance) and very straightforward, making interpreters the perfect entry point for most emulators and a fallback for other translation methods. However, interpreters are so straightforward that they have barely any wiggle-room for optimization. Interpreters will always be costly.

**Recompilation** gives us that wiggle-room. By translating the code in *blocks* rather than per instruction, recompilers can peek into what the code is doing and reimplement troublesome code in ways that are faster for the host hardware. However, reimplementation often causes inaccuracy, and correcting for that without sacrificing speed leads to ballooning complexity. Making a recompiler both fast *and* accurate can easily take thousands of hours from passionate engineers.

There are many different types of recompilers, but we're just going to focus on the primary recompiler type that Dolphin uses: JITs.

**Just-In-Time Recompilation** (JIT) recompiles small blocks of code *while the program is running*. A JIT will fetch blocks of code from the program, analyze and reimplement as much as it can, then pass the JITed code to the host system to be processed and ready *just* before the program needs to consume those blocks.

"Just-In-Time" is literal.

The live analysis that JITs perform is overhead. While modern JITs will mitigate this somewhat by caching JITed code blocks, the analysis is still work, which some other recompilation techniques avoid. However, JITs have many benefits. By recompiling blocks of code while the program is running, JITs are able to adapt to whatever the program is doing and don't need to rely on assumptions. This allows for maximum optimization potential, even in self-modifying programs!

With that, we've covered the two most common CPU emulation techniques. Generally, there is nothing inbetween these two options. Emulator authors make an interpreter first, and use it as a reference for building a recompiler. And that's it. Recompilers *are so much faster* than interpreters that making an interpreter faster is largely irrelevant.

There are several reasons for this. For example, interpreters can't place guest registers into the host registers, so any time the emulated CPU wants to read its registers, an interpreter has to fetch the registers' contents from host system memory, which is *two orders of magnitude* slower. Also, for Dolphin, our interpreter has the [MMU](https://dolphin-emu.org/blog/2016/09/06/booting-the-final-gc-game/#memory-management-unit-emulation) enabled *at all times*, and the constant memory manipulation is *even slower* in the interpreter than it is for a JIT!

However, what slows down interpreters the most is **branching**.

In computer science, a [branch](https://en.wikipedia.org/wiki/Branch_(computer_science)) is the act of diverging from the current flow of instructions. If a CPU is executing instructions sequentially, it can process them *very very fast*. But if an unpredictable branch occurs, the CPU will need to stop everything, flush all its pipelines, and spend the next 10-20 cycles building them back up again before it can resume processing. Branching is one of the most expensive low level operations in computing! As such, modern CPUs do *everything they possibly can* to improve branch performance, with branch prediction and speculative branch execution trying to get ahead of any branches and keep the pipelines flowing. These features are so important that improved branch prediction is one of the primary reasons why a 2024 CPU core at 4ghz is faster than a 2004 CPU core at 4ghz. It's that significant.

By operating on each instruction from the guest, one at a time, an interpreter will need to branch *very frequently* - several times for even a single instruction. And these branches are usually *unpredictable*, directly hurting what makes modern CPUs fast. With all factors combined and in a worst case scenario, a single instruction from the guest could take **over a hundred cycles** for our interpreter to decode! This occurs *millions of times per second*, thrashing our host CPU.

Interpreters are simple, straightforward, and readable, but they are *fundamentally inefficient*. A recompiler will always be faster, so there is little incentive to make an interpreter faster. Except, perhaps, *for fun*.

![](../../assets/fddf8d2eaa992609.avif)

Nine years ago, [degasus](https://github.com/degasus) had a fun idea. How fast could an interpreter be made (while still being an interpreter) if we applied a bunch of ideas from JITs? The result of this little experiment was the *Cached Interpreter*.

With a JIT, code is collected into blocks and recompiled into host-specific [machine code](https://en.wikipedia.org/wiki/Machine_code) all together. This allows the JIT to reimplement some of the code to be faster for the host, but also allows the JIT to *cache* these JITed code blocks, so that any time code is reused, the JIT will just jump to the cache and skip the analysis for a speedup.

Dolphin's **Cached Interpreter** borrows this idea. Code is collected into blocks exactly like a JIT. However, rather than recompile it into JITed machine code, which is specific to the host and may be reimplemented, the code block is instead translated into an *intermediate representation* - code which stores the decoded instructions as "commands" that can be compiled into machine code that the host CPU can run.

This benefits our Cached Interpreter in many ways. Just like a JIT, the code blocks can be *cached*. Any time code reappears, the Cached Interpreter can just reuse the already decoded version in the cache, skipping the decode and all its associated branching. The act of interpreting in blocks rather than per instruction also reduces branching outright, down to roughly one branch per command, and makes branches more predictable too. This also reduces the cost of fetching instructions through the MMU, and brings several other benefits from the JIT, such as [Idle Skipping](https://dolphin-emu.org/blog/2016/11/01/dolphin-progress-report-october-2016/#idle-skipping-option-removal). *

All combined, the Cached Interpreter was over twice as fast as our interpreter when it released! However, it was still an order of magnitude slower than our JITs. For most users, it was more or less irrelevant. However, the Cached Interpreter has found its niches. As it is still an interpreter, it retains the impeccable accuracy that interpreters provide, as well as the ability to run on any architecture - it's our interpreter, but faster. As such, it has become a useful tool for testing and JIT development. Plus, in [situations where JIT recompilers are unavailable](https://dolphin-emu.org/blog/2024/04/30/dolphin-progress-report-february-march-and-april-2024/#why-dolphin-isnt-coming-to-the-ios-app-store), the substantial speedup versus the standard interpreter is always welcome.

But what if the Cached Interpreter could be taken *further?*

![](../../assets/1f2c09552efd9bf5.avif)

Fast forward to 2024, and ** mitaclaw** and

**got into a competition to see just how optimized the Cached Interpreter could be. Eventually they merged their efforts, in what**

[Sam-Belliveau](https://github.com/Sam-Belliveau)**dubbed**

[mitaclaw](https://github.com/mitaclaw)**Cached Interpreter 2.0**.

This change brought *many* optimizations to the Cached Interpreter, but the biggest change by far was *variable sized commands*. Previously, the commands inside the Cached Interpreter's intermediate representation had a fixed size, but ** mitaclaw** and

**realized that by allowing the commands to be any size, the most common bookkeeping commands could be bundled together into a single command. This significantly reduces the number of bookkeeping commands in total, further reducing the amount of branching in our Cached Interpreter.**

[Sam-Belliveau](https://github.com/Sam-Belliveau)Just how big of an impact could these optimizations have? Let's get to the numbers!



With a 10 to 25% uplift, the Cached Interpreter is better than ever! It's also now 3 to 4 times faster than the interpreter, and in games with lots of idle loops to skip, such as [Cave Story](https://wiki.dolphin-emu.org/index.php?title=Cave_Story), Cached Interpreter leaves our interpreter in the dust. However, our JITs are still MUCH faster in every scenario, so its role in Dolphin is unchanged. The Cached Interpreter still cannot serve as a JIT alternative. And according to ** mitaclaw**, further optimizations had a negligible impact on its performance. Dolphin's Cached Interpreter will likely not see another significant performance bump again.

Nevertheless, for the niches where the Cached Interpreter thrives, it is now faster than it has ever been.

One of the best things about macOS is *application bundles*.

On Windows, programs are largely intended to bring their own dependencies. However, each program will need many different files in many different *and bizarre* places, so much so that it is standard to ship a *dedicated program* whose only purpose is to place or remove all of the disparate files an application needs to function. If something goes wrong with this process, **good luck**.

Linux, on the other hand, works more like code - dependencies are separate from the program and should be linked, not duplicated. However, dependencies will need to be installed along with the application, so Linux has package managers to install applications and any dependencies that are needed. While this is certainly better than the backwards-compatibility mess that is Windows, installing a single application in Linux still results in installing lots of things in lots of places.

macOS is different. It has something called *application bundles*. All apps on macOS (with the exception of command-line tools and scripts) are distributed in the bundle format. Application bundles are really just regular folders that follow a very specific structure with their contents. They allow all of an application's files and dependencies to be grouped together in a single folder, nice and neat. To the user, however, the bundle is shown as a single icon and they never see or know about all of the files inside. This allows for one of the best things about bundles - the process of installing or uninstalling an app is just... drag and drop. That's it. And to run the application, just double-click the bundle as if it were the application itself.

However, for the past several years Dolphin on macOS has shipped not one, but two bundles - Dolphin, and Dolphin Updater. The updater didn't do anything if you double-clicked it, and would just give an error; it was intended to be used only by Dolphin itself. Unfortunately, this has occasionally caused confusion with users. After all, the majority of macOS apps are distributed as a single bundle. Why does Dolphin have two?

Fortunately, this has now been fixed. When creating the main Dolphin bundle during a build, we now insert the updater bundle inside of it! Whenever we need to perform a Dolphin update, we just load the updater bundle from within the main Dolphin bundle, create a copy of it in a separate temporary location, and run that. With this change, the user only ever sees one bundle when installing Dolphin for the first time. Glorious single drag and drop installation has been achieved!

[2407-173](https://dolphin-emu.org/download/dev/master/2407-173/) removes all remnants of the separate updater bundle if any are present. If you have previously installed both Dolphin and the updater to your Applications folder, by the time you are reading this the separate Dolphin Updater will likely already be gone. If not, update and it will be removed.

*Note: A bug was fixed in 2407-111 which caused the updater to crash on startup on some Macs. If you are using an older build of Dolphin, you may need to update your copy of Dolphin manually first.*

Audio emulation has gone through an interesting transformation throughout the many eras of Dolphin. In the release era, HLE (High Level Emulation) audio is pretty much universally used for almost everything. Over the course of time, almost every gap in accuracy between HLE and the more in-depth LLE (Low-Level Emulation) has been closed up. Infamous HLE audio bugs like the screeching in [Star Wars: Rogue Squadron](https://wiki.dolphin-emu.org/index.php?title=Star_Wars_Rogue_Squadron_II:_Rogue_Leader) games? Solved. The Grand Star hang in [Super Mario Galaxy](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Galaxy)? Long gone.

It has been a massive struggle to get HLE audio to this point. Back in the old days, you had a choice to make - potentially broken audio (or even no audio in some games!) with HLE, or deal with the massive performance demand that came with getting proper audio using LLE. This all started to change back in the 3.5 era, when massive rewrites hit Dolphin's audio code.

Why does this all matter? Well, users didn't like LLE audio, and these massive rewrites to HLE audio had tons of benefits. The problem with HLE audio is that Dolphin has to correctly handle the functions of every revision of every microcode in order for things to work. [Pikmin](https://wiki.dolphin-emu.org/index.php?title=Pikmin) and [Pikmin 2](https://wiki.dolphin-emu.org/index.php?title=Pikmin_2) use what we call the "Zelda Microcode". This microcode is used in games like [the](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_The_Wind_Waker) [Zelda](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_Four_Swords_Adventures) [games](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_Twilight_Princess) (except [Skyward Sword](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_Skyward_Sword)), [the](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Sunshine) [Super](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Galaxy) [Mario](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Galaxy_2) games and [Luigi's Mansion](https://wiki.dolphin-emu.org/index.php?title=Luigi%27s_Mansion).

The problem with this is that *pretty much every game* uses a different version of the microcode. This meant that in order to emulate *each game*, you had to figure out what functions they supported, and how to emulate them correctly. For example, all of the microcode revisions will have functions to control volume, but earlier microcodes might have bugs that need to be emulated, later microcodes might have additional features, like controlling volume individually for different things. Apply this to *everything*, and it becomes apparent how much of a pain in the rear this can be.

In order to get these massive rewrites merged, support for each individual microcode wasn't necessarily perfect. Upon testing, the games sounded mostly correct, and the various problems of old-HLE audio were fixed. However, there were minor issues spread across the various games. Originally, New-Zelda-HLE had issues with the volume of echoes in [Mario Kart: Double Dash](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart:_Double_Dash%E2%80%BC). This was a known issue when it was merged, but was deemed acceptable due to all the other improvements.

The only difference between that and [Pikmin](https://wiki.dolphin-emu.org/index.php?title=Pikmin) and [Pikmin 2](https://wiki.dolphin-emu.org/index.php?title=Pikmin_2) is that their small issues seemed like they were never going to be addressed. In fact, most users didn't even realize there was a problem. They were by and large playable, and unless you played the game recently on console, you wouldn't know that some menu sounds were the wrong pitch, or there were missing sounds for puffs of smoke in the opening cutscene. Thankfully, when New-Zelda-HLE was merged, the issues we did discover were archived, and ** flacs** saw them and investigated them while looking for more audio issues to fix.

*for years!*

These may seem minor, but back in the day there were hundreds of issues like these due to HLE audio's imperfect emulation of the microcode. It seems almost surreal that, in most cases, HLE audio and LLE audio are now indistinguishable.

Once upon a time, Dolphin bugs were obvious: a simple *screenshot* was all it took to convey just how broken Dolphin was in a particular title. [Grey Zelda](https://www.youtube.com/watch?v=2jta4PkYBRk), [Spider-man as a flying box](https://dolphin-emu.org/blog/2014/09/30/dolphin-progress-report-september-2014/#40-3194-fioras-fantastic-faster-mmu-by-fiora), [uwu Kirby](https://dolphin-emu.org/m/user/blog/progress-report/2409/DearGod.webp), [Batman as a flying crotch](https://dolphin-emu.org/m/user/blog/progress-report/september-2014/batman-the-flying-crotch.png), on and on. However, once Dolphin's fundamental inaccuracies were resolved in the 3.5 and 4.0 eras, that largely became a thing of the past. Today, we have to use fifologs and automation to catch changes, and carefully pixel-peep against console to verify that something is in fact actually incorrect.

[Wallace and Gromit in Project Zoo](https://wiki.dolphin-emu.org/index.php?title=Wallace_%26_Gromit_in_Project_Zoo) bucks this trend. The game's shadows looked fairly good on console, but in Dolphin? **They could ƒ^&%ing explode.**

PHOTOSENSITIVITY WARNING. Click to play.

We had no idea why the shadows in this fairly obscure game would sometimes fail so catastrophically, but something was clearly very wrong, so in 2013 we added a patch to *remove these shadows from the game.* It was an extreme solution, but the game had an extreme problem, so we did what we could to at least make the game playable. It was certainly better than the video above. But as time passed, the developers who investigated the problem moved on, and these troublesome shadows slowly faded from memory...

**Ten years later**, ** flacs** happened to notice that Project Zoo's shadows were still broken, and looked into the issue. They soon spotted something suspicious: the game's

[display list](https://www.songho.ca/opengl/gl_displaylist.html)(a group of GPU commands stored for later execution) wasn't aligned. Rather than prevaricate about the bush,

**went straight to hardware testing and quickly adapted the**

[flacs](https://github.com/Tilka)[triangle test homebrew](https://github.com/devkitPro/gamecube-examples/tree/master/graphics/gx/triangle)to use display lists.

Turns out that hunch was spot on target! [Wallace and Gromit in Project Zoo](https://wiki.dolphin-emu.org/index.php?title=Wallace_%26_Gromit_in_Project_Zoo) submits display lists unaligned, and Dolphin was erroneously processing them exactly as they were submitted. The hardware aligns the memory address by dropping its lower bits. So for example, the game would point toward 0x80fc9b04, and Dolphin would start executing from there (getting bad opcodes) when hardware would *drop* the lowest 5 bits as it was 32-byte aligned and start at 0x80fc9b00. By not forcing alignment, Dolphin thought the game wanted to render *random garbage* and told the GPU driver to render it, which the GPU driver would try its best to do. Sometimes this only resulted in minor visual bugs, other times it would utterly explode as shown above.

With a very small change to Dolphin, we can now render these shadows just fine, and yet another hardware quirk is being emulated correctly.



![](../../assets/90d7103b043096c5.avif)

![](../../assets/abf91cd810f434a1.png)

Last year, [JosJuice](https://github.com/JosJuice)[rewrote our Android controller input handling from scratch](https://dolphin-emu.org/blog/2023/05/21/dolphin-progress-report-february-march-april-2023/#50-18920-rewrite-android-input-handling-by-josjuice). This rewrite replaced the old Java input handler with a brand new one written in C++ that more closely matched how Dolphin's PC input handlers work. Not only did this clean up some crusty old code with known problems, but it also unlocked dozens of "new" features for our Android users that were previously only in our desktop builds!

However, one very significant feature that was a part for that overhaul last year was disabled when the overhaul eventually landed - sensor input (accelerometers and gyroscopes) from external controllers, a feature available in Android 12 and up. During the final testing of the input rewrite, ** JosJuice** received reports that using controller sensors could make Dolphin crash when navigating between screens. Because their phone was stuck on Android 11, they couldn't test the feature themselves, and decided that rather than hold off the rewrite to address the issue, it was best to just disable external sensors for the time being and continue the rollout without it.

With over a year passed since then, ** dreamsyntax** showed up with not only willingness to investigate the crash, but also the needed hardware. The first step: Finding out why the crash is happening. The reports from a year prior included a stack trace showing where in the code the crash occurred, and

**had used this information to theorize that when Dolphin turned off unused sensors to save battery, Android would start notifying Dolphin about a sensor that Dolphin never had asked to be notified about.**

[JosJuice](https://github.com/JosJuice)**was able to replicate the crash and get a match stack trace, and then managed to take a step beyond the old investigation by figuring out the root cause of the crash. The sensor that Dolphin didn't recognize wasn't actually a new sensor - it was a new object representing the same sensor as before. The cause of the bug was that Dolphin checked if two sensor objects were literally the same object (**

[dreamsyntax](https://github.com/dreamsyntax)*referential equality*) rather than checking if the objects had the same content (

*structural equality*).

With that, it was time for the second step: Properly fixing the issue. ** dreamsyntax** began by making a quick solution to check that their approach was correct, but alas, Dolphin was still crashing! It turned out there was a

*second crash*that nobody had discovered until now because the other crash always happened first! Somewhere within the code of Android itself, a

`ConcurrentModificationException`

was being thrown when Dolphin turned sensors off. **couldn't quite make sense of why this was happening, but with all the information he had gathered,**

[dreamsyntax](https://github.com/dreamsyntax)**once again stepped into the picture. They discovered that the cause of the crash was a simple coding mistake in the operating system itself -**

[JosJuice](https://github.com/JosJuice)[removing objects from a list while looping through the list](https://cs.android.com/android/_/android/platform/frameworks/base/+/389eed52e469cadfc704708e10ddeec77ea807ae:core/java/android/hardware/input/InputDeviceSensorManager.java;l=285)- and implemented a workaround for this crash and a proper solution for the earlier crash. Finally,

**tested the change to make sure motion controls were now working properly.**

[dreamsyntax](https://github.com/dreamsyntax)With the issues now solved, sensors from external controllers are available for mapping in Dolphin on Android! The sensors in controllers such as the DualShock 4 can now be used to better emulate motion in Dolphin. Keep in mind that the feature only works for controllers your version of Android has sensor support for. If you're using Android 11 or older, sensors aren't supported for any controllers at all.

**Last Month's Contributors...**[¶](https://dolphin-emu.org#last-months-contributors)

Special thanks to [all of the contributors](https://github.com/dolphin-emu/dolphin/graphs/contributors?from=2024-05-01&to=2024-09-04&type=c) that incremented Dolphin 349 commits in the final days of the 5.0 era, and 279 commits after Release 2407!

**The First Month of Dolphin RetroAchievements**[¶](https://dolphin-emu.org#the-first-month-of-dolphin-retroachievements)

The RetroAchievements team has shared with us a bunch of statistics for the first month of RetroAchievement support in Dolphin! And there's a lot of interesting bits in here. Enjoy!

**General Statistics**[¶](https://dolphin-emu.org#general-statistics)

**Total Unlocks: 860,290**

**Total Hardcore Unlocks: 815,944**

**Total Points Earned: 5,864,862**

**Total Hardcore Points Earned: 5,558,151**

**Total Sessions: 284,432**

**Top Ten Games with the Most Players**[¶](https://dolphin-emu.org#top-ten-games-with-the-most-players)

| Game | Players |
|---|---|
| Super Mario Sunshine | 2532 |
| Super Smash Bros. Melee | 2230 |
| Mario Kart: Double Dash!! | 1908 |
| Luigi's Mansion | 1148 |
| Legend of Zelda, The: The Wind Waker | 1084 |
| WarioWare, Inc.: Mega Party Games! | 946 |
| Kirby Air Ride | 893 |
| Legend of Zelda, The: Twilight Princess | 888 |
| Animal Crossing | 847 |
| Pikmin | 758 |

**Top Ten Most Mastered Games**[¶](https://dolphin-emu.org#top-ten-most-mastered-games)

| Game | Masteries |
|---|---|
| Super Mario Sunshine | 284 |
| Piglet's Big Game | 195 |
| Magical Mirror Starring Mickey Mouse | 172 |
| Pokemon Channel | 163 |
| ~Hack~ Samus Goes to the Fridge to Get a Glass of Milk 3D | 152 |
| Winnie the Pooh's Rumbly Tumbly Adventure | 144 |
| ~Hack~ Luigi's Mansion Beta Restoration | 140 |
| Legend of Zelda, The: The Wind Waker | 120 |
| Wario World | 112 |
| WarioWare, Inc.: Mega Party Games! | 101 |

**Top Ten Most Beaten Games**[¶](https://dolphin-emu.org#top-ten-most-beaten-games)

| Game | Times Beaten |
|---|---|
| Super Mario Sunshine | 626 |
| WarioWare, Inc.: Mega Party Games! | 551 |
| Luigi's Mansion | 505 |
| Super Smash Bros. Melee | 339 |
| Dance Dance Revolution: Mario Mix | 305 |
| Pokemon Channel | 297 |
| Mario Kart: Double Dash!! | 297 |
| Pikmin | 273 |
| Legend of Zelda, The: The Wind Waker | 243 |
| Naruto: Clash of Ninja | 232 |