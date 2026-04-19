---
title: Tools that I use.
url: https://c0de517e.com/016_tools_that_I_use.htm
author: Angelo Pesce
published: '2011-04-20'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

Finally "moving over" to this new website my old

[tools that I use](http://c0de517e.blogspot.com/2011/04/2011-tools-that-i-use.html) page. As before - no corporate / big apps (office - visualstudio - photoshop - maya etc) listed - you/I will know to install these regardless. I work win Windows and Mac only - so I list apps for these - no Linux I'm afraid.

This is sort-of a CSV:

ENTRY, TYPE, OS, MUST-HAVE, NEW ENTRY?, NOTES

You can copy-paste and easily filter/sort!

**Prerequisites.**
Package managers and apps to deal with apps...

-

[Titus Tech Tool](https://christitus.com/windows-tool/), prerequisite, win, *, NEW!, WinGet is now installed by default on Win10+ - and it is AMAZING. This script leverages WinGet to manage commonly installed apps and most importantly - to tweak and debloat Windows. Unfortunately - even to my low and non-paranoid standards - Win11 has rapidly been adding more and more malware.

-

[Brew](https://brew.sh), prerequisite, mac, *, -, Not quite as good as WinGet - but the best I've found for Mac.

-

[CakeBrew](https://www.cakebrew.com), prerequisite, mac, *, -, After installing brew - can simply do brew install --cask cakebrew.

-

[Sandboxie](https://sandboxie-plus.com), prerequisite, win, -, -, A prerequisite in some cases - but not a must have - Sandboxie allows to install Windows applications in an isolated sandbox without paying the performance costs of a full VM. Fun fact: Windows has even its own

[sandboxing system](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-overview) but that one does not preserve state. See also

[BoxedApp](https://www.boxedapp.com/) to create "portable" installs.

-

[Pearclearner](https://github.com/alienator88/Pearcleaner), prerequisite, mac, *, -, A better way to uninstall Mac apps.

-

[Latest](https://max.codes/latest/), prerequisite, mac, *, -, A program to check and download app updates. On Windows there's no need because the built-in winget is fantastic!

-

[Snappy Driver Installer](https://sdi-tool.org/), prerequisite, win, -, -, Searches for driver updates. I typically don't use this, but on some machines it can come in handy - and I never experienced an issue thus far. Portable.

-

[Driver Store Explorer / RAPR](https://github.com/lostindark/DriverStoreExplorer), prerequisite, win, -, -, Almost a complement to the SDI above - this one removes from the windows drivers, old versions that accumulate over time. You don't really need it (old drivers should not create problems), but it's a small portable program that shouldn't hurt anything.

**File/Disk Tools.**
I know lots of people swear by the classic two-panel file managers ala Norton Commander. I never found them useful in GUI environments - I do install Midnight Commander in terminals.

-

[Everything](http://www.voidtools.com/), files, win, *, -, Life-changing - you end up using it for... everything! After installing it I also I limit windows search indexing options only to the start menu (and email if using Outlook).

-

[Find Any File](https://findanyfile.app), files, mac, -, -, Similar to Everything - but unfortunately there is no way on Mac/APFS to match Everything's speed on NTFS - and Mac's Spotlight is already decent so this is less of a must-have.

-

[FastCopy](https://fastcopy.jp), files, win, -, -, Benchmarked to be indeed the fastest - nifty to sync large Perforce or GIT repos across machines. I do not fully trust it though.

-

[TeraCopy](https://www.codesector.com/teracopy), files, win/mac, -, -, Like FastCopy - perhaps slower but it has an Mac version if you need it. On windows it integrates with explorer, works with copy/paste etc.

-

[7zip](https://www.7-zip.org), files, win, *, -, 7z is the best archiever for windows, never found anything better.

-

[Keka](https://www.keka.io/en/), files, mac, *, -, Note that if you don't want to donate there is a small link to a direct download on the page (not app store). An alternative is https://theunarchiver.com

-

[WinRar](https://www.win-rar.com/start.html), files, win, -, -, I don't use WinRar often - but it has a few nifty features that can be useful: can add redundancy to recover archives in case of corruption - and last I checked it handled symlinks and hardlinks better.

-

[FileOptimizer](https://nikkhokkho.sourceforge.io/static.php?page=FileOptimizer), files, win, -, -, The author's webpage looks like a scam - but the software is a nifty collection of all kinds of file shrinkers - useful for the web for example. "Portable".

-

[Czkawka](https://github.com/qarmin/czkawka), files, win/mac, -, -, Find duplicates - near duplicates - empty files etc etc. An app I keep around in "portable" form. On Mac, can be installed via brew.

-

[WizTree](https://diskanalyzer.com), files, win, *, -, Fast disk usage/directory size. Can be "portable".

-

[Disk Inventory X](https://www.derlien.com/index.html), files, mac, *, -, Same as WizTree above, but for Mac. GrandPerspective and SquirrelDisk are other free alternatives.

-

[SuperDuper!](https://www.shirt-pocket.com/SuperDuper/SuperDuperDescription.html), files, mac, -, -, Mac whole-disk backup, can also create bootable copies.

-

[Mounty](https://mounty.app), files, mac, *, -, Allows to mount NTFS in r/w mode on Mac. Do it at your own risk! Mac support for non-Apple partition formats is terrible, even exfat does not work well/support all options... Still, can be handy if you're ok w/the risks.

-

[TestDisk](https://www.cgsecurity.org/wiki/TestDisk_Download), file, win/mac/linux, *, -, The best partition/file recovery tool out there. Must have, preferrably on a bootable USB.

[Recuva Portable](https://portableapps.com/apps/utilities/rcvportable) is also good.

**Text Editors.**
For me - the war of the text editors ended: nowadays I use VSCode for everything. It's fast - available everywhere - has an amazing extension ecosystem. Previously I relied on Notepad++ for the most part (dabbled with others for course - Sublime Text is great for example). I also used to use some specialized text editors for markdown (Typora - Markdeep - Marp...) but they are irrelevant to me today.

This does not mean that I moved to VSCode as my main IDE - for serious C++ at least I still prefer by a comfortable margin to go with Visual Studio "proper" - especially for debugging (and XCode for Mac of course). I don't use any other third-party IDE - sorry JetBrains.

-

[Visual Studio Code](https://code.visualstudio.com), text, win/mac, *, -, The winner!

-

[TeXstudio](https://github.com/texstudio-org/texstudio), text, win/mac, -, -, When I need (rarely nowadays) TeX for publications. I use BasicTeX as the actual TeX distro: https://tug.org/mactex/morepackages.html

-

[HxD](https://mh-nexus.de/en/hxd/), text, win, -, -, For huge files and binary files it's good to have an hex editor.

**Coding.**
I guess the biggest change I've seen through the years is a shift from native C++ coding tools to the inclusion of more prototyping and scripting tools - even if I've always been a polyglot when it comes to programming and always adored REPLs and live-coding.

I used to love

[Mathematica](http://c0de517e.blogspot.com/2013/10/wolframs-mathematica-101.html) for visualization and experimentation - but nowadays the

[scientific python ecosystem](http://c0de517e.blogspot.com/2019/05/numpy-by-example.html) matured to a degree that it does not make sense to me to pay the price of working in a system fewer people can and know how to use. Programming languages have always been mostly about community. And I find python to be an amazingly well designed language - the perfect evolution of BASIC.

I removed from the list

[Lattix](https://www.lattix.com/products/) -

[CppDepend](https://www.cppdepend.com) -

[CppCheck](https://cppcheck.sourceforge.io) as I have not used them in a while. They are still likely the best at what they do.

-

[MiniConda](https://docs.anaconda.com/miniconda/), code, win/mac, *, -, Anaconda is my favorite python distribution and conda is a great package manager. As I like to install all packages that I need - and no other bloat - I go for the MiniConda variant.

-

[Fork](https://git-fork.com), code, win/mac, -, -, I hate GIT. Fork makes GIT a tiny bit more tolerable - albeit it might be an illusion - in the end your best bet is to use the commandline. Fork can though be nifty to visualize what's going on. Sourcetree is an alternative: https://www.sourcetreeapp.com

-

[BeyondCompare](https://www.scootersoftware.com/home), code, win/mac, -, -, IMHO still the best diff app. Unfortunately the move to git comes often with moving to github and web-based code review workflows that make this less relevant.

-

[AraxisMerge](https://www.araxis.com/merge/), code, win/mac, -, -, Similar to BeyondCompare - it's the best in class merge app. I used to use both. Now I have not used either in a while. Might come off this list.

-

[Zeal](https://zealdocs.org), code, win, -, -, I hate that we don't have good offline documentation anymore! ZealDocs solves that.

-

[Dependency Walker](http://www.dependencywalker.com), code, win, -, -, Old but gold. One of these tools I keep around in a "portable" install for the once every year time you need it...

**CPU/GPU profilers and debuggers.**
For a while there was quite some movement in this category - with new debuggers and profilers from small "indie" teams showing up left and right. That is still probably the case today but I noticed that already a few I had on my "to try" list seem to have been abandoned.

[Orbit](https://orbitprofiler.com) for example - the last version is from 2018. Similarly I wanted to try

[Optick](https://github.com/bombomby/optick) - but that too seems abandoned and the homepage is no more online. Also abandoned seems

[Lux](https://luxdebugger.com) looking at the what's new page at least :(

-

[Superluminal](https://superluminal.eu), prof-debug, win, -, -, An exception to the blurb above, Superluminal is both new and still kicking!

-

[VerySleepy](http://www.codersnotes.com/sleepy/), prof-debug, win, -, -, A simple sampling profiler.

-

[VTune](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html), prof-debug, win, -, -, Intel's venerable VTune is now free!

-

[RenderDoc](https://renderdoc.org), prof-debug, win, *, -, The king of GPU captures!

-

[AMD developer tools](https://www.amd.com/en/developer.html), prof-debug, win, -, -, Good CPU profiler and GPU profiler.

-

[Intel GPA](https://www.intel.com/content/www/us/en/developer/tools/graphics-performance-analyzers/overview.html), prof-debug, win, -, -, Intel's GPA lately has risen from a medicre GPU capture tool to one of the best. It's my first alternative now to RenderDoc if for some reason that fails me.

-

[Pyramid Shader Analyzer](https://github.com/jbarczak/Pyramid), prof-debug, win, -, -, Still useful - even if

[Shader Playground](http://timjones.io/blog/archive/2018/05/19/introducing-shader-playground) is in most cases a better alternative now.

**Rendering and Graphics.**
I removed from the list the various HDR image tools I used to install - e.g. Picturenaut - HDRShop - PTgui. Some still exist but I doubt they are the best now that HDR stuff is common in consumer hardware and applications. Also - I have not had to deal with tonemapping and HDR cubemaps and all that jazz in a while.

I'm also so glad we have Blender now. Way back in the days (when I used to dabble in 3d art myself) - my favorite app was Lightwave - now practically defunct as it is defunct its spiritual successor - Luxology/The Foundry's Modo. Beyond these - the next 3d app I knew how to use decently was 3dsMax. But I never ever loved that. Today I can install Blender and that's it!

-

[IrfanView](https://www.irfanview.com), gfx, win, *, -, I've been probably using this for a couple of decades now! On Mac I used to use Xee - but that's quite old now. I thought I would replace it with

[Nomacs](https://github.com/nomacs/nomacs) but it seems they provide builds for everything but Mac e.g. including OS/2! And to be honest - Mac's built-in preview app is decent.

-

[MeshLab](https://sourceforge.net/projects/meshlab/), gfx, win/mac, -, -, Still the king of geometry processing.

-

[Blender](https://www.blender.org), gfx, win/mac, -, *, I am astounded at Blender. It is not just the only good opensource art app I've ever seen (I hate GIMP -

[Krita](https://krita.org/en/) is mediocre imho and the same for

[InkScape](https://inkscape.org) - albeit I use the latter sometimes) - but it is now truly one of the best 3d gfx apps "on the market". I use it also for prototyping and datavis.

-

[Toolbag](https://marmoset.co), gfx, win/mac, -, -, Great fun tool for small-scale realtime rendering.

[cmftStudio](https://github.com/dariomanesku/cmftStudio) used to be sort-of an opensource alternative / cubemap baker - but it has been abandoned now.

**Prototyping.**
I have - as most programmers do I guess - a variety of my owns tiny testbeds to prototype graphics stuff or other algorithms. But truth to be said these are less and less relevant as we have now a few engines and tools that are simply good enough for most things!

-

[Processing](https://processing.org), proto, win/mac, -, -, I still use processing "often": for bespoke interactive datavis - to prototype small algorithms - and for generative art! Processing-JS is great too - and with some effort in certain Java IDEs it is possible to live-code (hotswap) processing java code as well.

-

[DrawBot](https://www.drawbot.com/index.html), proto, mac, -, -, A good alternative to processing - even more minimalistic and based on Python. I don't use it often but it is neat for "doodling" smaller code ideas.

-

[CToy](https://github.com/anael-seghezzi/CToy), proto, win/mac, -, -, Often I want to test and idea and I want to do it in C because I know it's a small snippet of code I then want to move directly into a real C++ application. CToy is great for this! Even if now in one of my own frameworks I integrated TCC in a similar fashion.

-

[Unity](https://unity.com), proto, win/mac, -, -, Unity has become one of my favorite tools for prototyping. You can do quite a bit even with the

[simple legacy pipelines](http://c0de517e.blogspot.com/2016/07/unity-101-rendering.html) - without going to the new fancy scriptable rendering stuff. Moreover... I know how to use it. I guess if I was more familiar with

[Godot](https://godotengine.org) I'd use that instead.

-

[KodeLife](https://hexler.net/kodelife), proto, win/mac, -, -, A better shader editor than shadertoy if you need to really work on stuff.

-

[Lobster](https://strlen.com/lobster/), proto, win/mac, There are a lot of interesting languages out there and even more frameworks and libraries - I won't list them but Lobster deserves a special mention because it is quite attuned to game and graphics prototyping.

**Visual Studio Extensions.**
Visual Studio (not code) extensions get abandoned fast. If you have a set you love in a given version of VS you must expect many not to be ported over to the next. This makes keeping a list up-to-date an annoying task. I used to use the popular Visual Assist X plugin instead of Intellisense as the latter used to be way too slow - but it's less relevant nowadays.

-

[Debug Single Thread](https://marketplace.visualstudio.com/items?itemName=mayerwin.DebugSingleThread), code-vs, win, *, -, Supports VS 2022.

-

[Concurrency Visualizer](https://marketplace.visualstudio.com/items?itemName=Diagnostics.DiagnosticsConcurrencyVisualizer2022), code-vs, win, *, -, Supports VS 2022.

-

[Output Enhancer](https://marketplace.visualstudio.com/items?itemName=NikolayBalakin.Outputenhancer), code-vs, win, *, -, Colorizes the output and build windows to highlight errors.

-

[Debug Command Line](https://marketplace.visualstudio.com/items?itemName=SamHarwell.DebugCommandLine), code-vs, win, -, -, Up to VS 2019.

-

[Smart Commandline](https://marketplace.visualstudio.com/items?itemName=MBulli.SmartCommandlineArguments2022), code-vs, win, *, -, Similar to the above, but for VS 2022.

-

[VSHistory](https://marketplace.visualstudio.com/items?itemName=KenCross.VSHistory2022), code-vs, win, -, -, Supports VS 2022.

-

[Indent Guides](https://marketplace.visualstudio.com/items?itemName=SteveDowerMSFT.IndentGuides2022), code-vs, win, -, -, Supports VS 2022.

-

[Continuous Formatting](https://vlasovstudio.com/continuous-formatting/), code-vs, win, -, -, Supports VS 2022/26 - on new projects - if I'm king - I like to never think about formatting and stick to autoformat from day one.

-

[Color Theme Editor - 2019](https://marketplace.visualstudio.com/items?itemName=VisualStudioPlatformTeam.VisualStudio2019ColorThemeEditor), code-vs, win, -, -, Editing color schemes for VS is a huge PITA - this extension is a decent help - unfortunately it is deprecated and the new ones MS made are worse.

-

[Symbol Sort](http://gameangst.com/?p=320), code-vs, win, -, -, A utility for measuring C++ code bloat from PDBs or DumpBin dumps.

**Other desktop apps.**
I used to install

[CCleaner](https://www.ccleaner.com/ccleaner) everywhere - on Mac and Windows - but it has become more dubious lately and it was not really that useful to begin with to be honest. It's still the easiest way I know to look at all the startup programs in Windows FWIW. Also - there were a ton of apps to control the arrangement of windows on... Windows - which now don't make sense to me as Win11 has decent window snapping behavior and shortcuts.

-

[VideoLan](http://www.videolan.org/vlc/), desktop, win/mac, *, -, A must - not just for playing video but to transcode too. Also good for screen captures - even if nowadays both Windows capture tool and Mac's Quicktime player app natively do screen recording.

-

[IINA](https://iina.io), desktop, mac/mobile, *, -, Good HDR (and not...) video player. I use it on my iPad as well!

-

[AutoIt](https://www.autoitscript.com/site/autoit/), desktop, win, -, -, It's nifty. I used AutoIt to create small GUI programs around command-line tools or batch workflows. TBH nowadays I'll most likely if the need arises do the same with python/clicknium.

-

[SumatraPDF](https://www.sumatrapdfreader.org/free-pdf-reader), desktop, win/mac, *, -, ...because Acrobat Reader is a bloated mess. And even if browsers nowadays are fine PDF readers - sumatra is better and can also open a variety of other formats (epub mobi cbr/cbz djvu etc).

[muPdf](https://mupdf.com) is an alternative as well.

-

[Procrastitracker](https://strlen.com/procrastitracker/), desktop, win, -, -, I used to use this quite a bit - and I also really like the Pomodoro method. But it depends on the kind of work I'm doing.

-

[SysInternal Tools](https://learn.microsoft.com/en-us/sysinternals/), desktop, win, *, -, Must have them... somewhere. They are "portable". Related

[Process Hacker](https://processhacker.sourceforge.io) and

[NirSoft tools](https://www.nirsoft.net).

-

[RapidEE](https://www.rapidee.com/en/about), desktop, win, -, -, Because editing environment variables on Windows is annoying otherwise...

-

[Scroll Reverser](https://pilotmoon.com/scrollreverser/), desktop, mac, *, -, Another must have - Apple's natural scrolling direction is correct for trackpads - but OBVIOUSLY the wrong choice on a mouse wheel :)

-

[Background Music](https://github.com/kyleneideck/BackgroundMusic), desktop, mac, -, -, Nifty tool to control the volume per-app on Mac.

-

[Parsec](https://parsec.app), desktop, win/mac, *, -, The best desktop streaming tool ever. I use it often to control computers even in the same room now - or different continents (you might need

[this](https://support.parsec.app/hc/en-us/articles/360045297592-How-to-port-forward-Parsec)) - it's just that convenient! There are now hardware devices like

[JetKVM](https://jetkvm.com) that do the same thing - but so far I have not had a use for them because the systems I need to control are powerful enough and Parsec just works.

-

[Apollo/Artemis/Sunshine/Moonlight](https://github.com/ClassicOldSong/Apollo), desktop, win/mac, -, -, An opensource alternative to Parsec. Moonlight is the OG, Sunshine and Apollo are forks. Meant for game streaming from PC to Mobile, on a LAN, can work PC to PC as well. Could work over the internet by using something like tailscale.

-

[Synergy](https://symless.com/synergy), desktop, win/mac, *, -, Must have with a caveat - it is so only when you have multiple computers and multiple monitors all on the same desk setup.

[Barrier](https://github.com/debauchee/barrier) is a fork.

- "defaults write com.apple.Dock autohide-delay -float 0", desktop, mac, *, -, Kills the lag of the dock autohide (which is the way I use the Mac dock).

[TinkerTool](https://www.bresink.com/osx/TinkerTool.html) and

[Defaults-write](https://www.defaults-write.com) are apps that can do that and other tweaks - if you care.

-

[VMWare Fusion and Workstation](https://www.vmware.com), desktop, win/mac, -, -, Now both are free for personal use. Vmware competed neck and neck with

[Parallels](https://www.parallels.com) for virtualization and I don't know at any given point who has an edge. Parallels and Fusion are nifty on a arm64 Mac as you can install arm64 Windows11 VMs. VirtualBox and Qemu are other options - I don't really use them even if the latter has been wrapped in the cute

[UTM](https://mac.getutm.app) Mac app - mostly to run vintage systems.

-

[Whisky](https://getwhisky.app), desktop, mac, *, NEW!, Whisky combines Wine+WineTricks+Rosetta+GamePortingToolkit to make Windows games run on an arm64 mac!

[Heroic](https://heroicgameslauncher.com/) game launcher also does something similar, but takes care of integrating/replication various game stores as well.

- Amphetamine app-store, desktop, mac, -, -, A wrapper for the caffeinate command - keeps the Mac awake. Nowadays though I just use the command-line built-in tool.

- Be Focused app-store, desktop, mac, -, -, A decent free Pomodoro timer.

-

[Heic Converter](https://sindresorhus.com/heic-converter), desktop, mac, *, -, Another tiny Mac app I use often.

-

[CheatSheet](https://www.mediaatelier.com/CheatSheet/feedNotes.php), desktop, mac, *, -, A nifty app that shows shortcuts for many Mac programs. Unfortunately it seems abandoned.

-

[Adapter](https://macroplant.com/adapter), desktop, mac, -, -, Good if you need to convert video - wraps ffmpeg and VLC.

-

[OpenEmu](https://iina.io), desktop, mac, -, -, A nice multi-emulation frontend for Mac.

-

[Hidden Bar](https://github.com/dwarvesf/hidden), desktop, mac, *, -, Hides menu bar icons so you have more space...

-

[OpenRGB](https://openrgb.org), desktop, win, *, -, A must have as most perhiperhials nowadays come with RGB leds and you want to control or disable them without installing whatever malware the "drivers" would come with.

-

[MS Powertoys](https://learn.microsoft.com/en-us/windows/powertoys/), desktop, win, *, -, A bit messy/bloaty compared to the old powertoys - but still has some important utilities - I use Awake often which is similar to the Mac Amphetamine mac app listed above.

**Internet and networking.**
I quit the browser wars too. I realized they are all terrible in different ways at different times - so now I use only whatever comes with the OS - I configure it to reduce the damage (Microsoft Edge is full of malware by default - including really crappy stuff like shopping coupons) and that's it! I definitely do not use Chrome because it always forces you to login with Google and it is actually annoying to me - as I have many google accounts and I want to mix and match them in the same browser window/session!

-

[NextDNS](https://nextdns.io), net, win/mac, -, -, A really nifty way to block ads and other crap - I don't put it as a must-have because blocking ads is not that important for me - and because at home I use a pi-hole.

-

[WinSCP](https://winscp.net/eng/index.php), net, win, -, -, I don't know when FTP died but I need it. Also SFTP etc. This is a good client for Windows.

-

[FileZilla](https://filezilla-project.org), net, win/mac, -, -, Another FTP et al client - this one exists for Mac too.

-

[Firefox](https://www.mozilla.org/en-US/firefox/), net, win/mac, *, -, I said I just use the default browsers - so why firefox? Because I like

[Tab session manager](https://tab-session-manager.sienori.com) to save sessions safely across devices - for work stuff - and that extension does not work on Safari. So on Mac - for work stuff - I use Firefox.

-

[Kristall](https://github.com/ikskuh/kristall), net, win/mac, -, -, A browser for Gopher and Gemini.

-

[LimeChat](http://limechat.net/mac/), net, mac, -, -, IRC can still be fun...

**Terminal & Linux.**
I guess I lied when I said I won't list things for Linux. I use it at home - on a raspberry pi for a few services - and sometimes through the excellent Windows WSL2 - especially as ML/DL stuff is still primarily a Linux thing. WSL2 also replaced the need to use Docker for Windows.

Also - I do use the terminal a bit on Mac too (and all the terminal apps listed are installed via brew)! I should have said more accurately that I don't really use Linux windowing desktop interfaces :)

I found linux mint to be a good distro for desktop use, for my home server I currently use ubuntu server.

-

[Alacritty](https://github.com/alacritty/alacritty), terminal, win/mac, -, -, A good GPU accellerated terminal emulator. Technically desktop software of course. I used to use Cathode on Mac - but that's dead - and then

[Cool Retro Term](https://github.com/Swordfish90/cool-retro-term) which is opensource but not actively developed (see

[for a Mac/arm64 build of CRT](https://github.com/charlie0129/cool-retro-term/releases)).

-

[Ripgrep](https://github.com/BurntSushi/ripgrep), terminal, win/mac/linux, -, -, A fast regex searcher in files.

-

[yt-dlp](https://github.com/yt-dlp/yt-dlp), terminal, win/mac/linux, *, -, The best youtube (and other video websites) downloader.

-

[Midnight commander](https://midnight-commander.org), terminal, win/mac/linux, *, -, I use it only on Linux. Should also try

[nnn](https://github.com/jarun/nnn).

-

[p7Zip](https://wiki.archlinux.org/title/P7zip), terminal, mac/linux, -, -, Gives you the power of 7z archives.

-

[tldr](https://tldr.sh), terminal, mac/linux, -, -, Better man.

-

[Micro](https://micro-editor.github.io), terminal, win/mac/linux, *, -, Because life is too short for VIM/Emacs et al. I set this as the default editor for git too.

-

[Miniserve](https://github.com/svenstaro/miniserve), terminal, win/mac/linux, -, -, Easy way to share a file.

-

[tmux](https://github.com/tmux/tmux/wiki), terminal, linux, *, -, You need this, if you're using remote shells.

-

[https://github.com/Byron/dua-cli](https://github.com/Byron/dua-cli), terminal, win/mac/linux, *, -, Fast directory size.

-

[streamlink](https://streamlink.github.io), terminal, win/mac/linux, -, -, Streams web video without the websites.

-

[weechat](https://weechat.org), terminal, win/mac/linux, -, -, IRC for terminals.

-

[glances](https://nicolargo.github.io/glances/), terminal, win/mac/linux, -, -, Better "top".

**Local deep models/learning.**
Another new category!

-

[LM-Studio](https://lmstudio.ai), deepl, win/mac, -, -, Currently experimenting with Qwen 2.5 but this stuff moves so fast...

-

[DiffusionBee](https://diffusionbee.com), deepl, mac, -, -, Best local stablediffusion frontend for Mac. Abandoned? Beware it keeps all images generated and imported in its data directory - even if you delete them from the app.

-

[SD-WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui), deepl, win/linux, -, -, Like DiffusionBee, more poweful but much less polished - for windows.

-

[ComfyUI](https://github.com/comfyanonymous/ComfyUI) deepl, win/linux/mac, -, -, It used to be a bit of a mess, only for power-users, nowadays it's better polished and the best way to play with generative AI.

-

[NerfStudio](https://docs.nerf.studio), deepl, win/linux, -, -, It used to be fiddly to install but it has been improving (and Pixi should solve all the issues... didn't try that way yet). For nerfs and gaussian splatting and similar. Today there are tons of alternatives, both for R&D and for "production" GS. Works under Windows/WSL2.

**Mobile and web apps.**
I won't put here shadertoy and compiler explorer because if you are here you surely know about them. I also won't list the tons of mobile apps that I might have installed on my devices - this would be useless both to you and to me - as I never need to reinstall apps on mobile when I migrate. I will instead only list a handful of must-haves that I use every single day.

-

[Desmos](https://www.desmos.com), apps, web, *, -, The best graphing calculator.

[GeoGabra](https://www.geogebra.org/) is also amazing when one needs to reason about geometrical constuctions.

-

[Dropbox](https://www.dropbox.com), apps, all, *, -, Now that I run

[my small home server](https://www.c0de517e.com/JOURNAL/log_002.htm#26) I could get rid of Dropbox. In practice I already removed most data from it but I am still using it for certain things. I also use a variety of USB memory things that I

[backup](https://www.c0de517e.com/JOURNAL/log_003.htm#36) time to time for work-in-progress stuff and a variety of portable apps and data I like to carry with me. Detailing all of that would take a post on its own...

-

[Reeder](https://reederapp.com), apps, mobile, *, -, Best RSS reader app. I use

[Feedly](https://feedly.com) as an aggregator.

-

[Foobar2000](https://www.foobar2000.org), apps, mobile, *, -, A music player for my mp3 collection. Yes. No spotify.

-

[Overcast](https://overcast.fm), apps, mobile, *, -, I listen to a ton of podcasts. Audiobooks too (Audible) and NYT audio.

-

[Sitescape](https://www.sitescape.ai), apps, mobile, -, -, Fun with the ios lidar.

-

[SimpleText](https://simpletext.app), apps, mobile, *, -, I use it for distraction-free writing on my ipad (with an external keyboard - usually the small Apple aluminum one).

-

[Paper](https://wetransfer.com/explore/paper), apps, mobile, -, -, I used to be very particular about my drawing / notes app on the ipad. This is the only one that still survives for me - but I might get rid of it too and just use the built-in notes and freeform apps.

[Freenotes](https://www.freenotetech.com) is decent too FWIW - as well as

[Tayasui sketches](https://www.tayasui.com/sketches/). I also got rid of all PDF apps and annotation-over-PDF apps - I just use the built-in preview and files instead.

-

[Nomad sculpt](https://nomadsculpt.com), apps, mobile, -, -, Fun!

-

[iDos 3](https://litchie.com/apps), apps, mobile, *, NEW!, Now that Apple opened to emulators - there is a lot of fun to be had. I used to have iDos already before because it briefly made it to the store and I grabbed just in time... I love DOS.

**Other notable links.**
For self-hosting:

Copy-party and piHole made my raspberry pi useful. I have a

[journal post here](https://c0de517e.com/JOURNAL/log_002.htm#26) detailing the configuration (at least at that time).

For "obsolete" macs:

[OpenCore Legacy Patcher](https://dortania.github.io/OpenCore-Legacy-Patcher/) allows to update older Intel macs. See

[this journal post for more](https://c0de517e.com/JOURNAL/log_005.htm#58).