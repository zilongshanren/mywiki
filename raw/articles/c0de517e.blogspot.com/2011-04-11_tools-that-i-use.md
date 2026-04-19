---
title: Tools that I use
url: https://c0de517e.blogspot.com/2011/04/2011-tools-that-i-use.html
published: '2011-04-11'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Update**: I've dropped the "2011" from the title, as I've kept this list more or less up-to-date every time I change a computer.

Other than what's required - usually Visual Studio, Photoshop, Office/Outlook, 3dsMax/Maya/Modo/... and Perforce (sadly nowadays often git), these are the tools that I always have installed on my development computer.

- In
~~strikethrough~~are tools that I used to install / might still be useful, but don't really rely upon anymore (these might go away as I update the list) - I don't use OSX for development much - I included a few OSX tools but you won't find as much programming stuff - will be marked in maroon.
- MUST-HAVE! are tools I always install

**Install management**



On OSX:


[ZeroInstall](http://0install.net/)is an alternative - and I always add homebrew/[Cakebrew](https://www.cakebrew.com)as package managers, which I use for command-line tools.
The opposite, uninstall, is also best served by some bulk/batch tools, I did have success with

[Absolute Uninstaller](http://www.glarysoft.com/absolute-uninstaller/)and[BCU](https://www.bcuninstaller.com/), but I'm sure there are many alternatives.Lastly, to keep things up to date... there are many tools for drivers and app updates, CCleaner has an app version checker built-in,

[SUMo](https://www.kcsoftwares.com/?sumo)/DUMo are nice, but the best free driver updater I've found is "driver booster for steam" that you can download... from Steam, run once, and uninstall :)**File tools**

- MUST-HAVE!
[Everything](http://www.voidtools.com/)is by far the tool I use the most. It's life-changing. After installing it I also I limit windows search indexing options only to the start menu and email, as the latter is required by Outlook).[Agent Ransack](http://www.mythicsoft.com/page.aspx?type=agentransack&page=home)is nice too. - Nowadays I'm working more across workstations it's handy to have a faster file copier over the network, I use
[FastCopy](http://ipmsg.org/tools/fastcopy.html.en)(see[http://www.raymond.cc/blog/12-file-copy-software-tested-for-fastest-transfer-speed/](http://www.raymond.cc/blog/12-file-copy-software-tested-for-fastest-transfer-speed/)) so I can sync Perforce depots (and then use p4 flush) on both machines without going through the p4 server (also, if you have HDD space, use a local p4 proxy, it's nifty!).[TeraCopy](https://www.codesector.com/teracopy)is similar and has a Mac version too. [WizDir](https://diskanalyzer.com/)or WinDirStat or similar, but as I don't really need it often, I just get the[portable version](http://portableapps.com/apps/utilities/treesize-free-portable)[as needed](http://portableapps.com/apps/utilities/windirstat_portable)(OSX:[Grand Perspective](http://grandperspectiv.sourceforge.net/)).- MUST-HAVE
[7-Zip](http://www.7-zip.org/)(OSX:[Keka](http://www.kekaosx.com/en/)or[The Unarchiver](https://theunarchiver.com)). I found that[WinRAR](https://www.win-rar.com/start.html?&L=0)can still be very useful if you need to handle symlinks / hardlinks - and if you want to add redundancy (recovery bytes). Most other compressors don't! [TestDisk](http://www.cgsecurity.org/wiki/TestDisk)and[Recuva](http://www.piriform.com/recuva)for file recovery are absolutely MUST-HAVE but I don't have them always installed, I typically carry testdisk on an usb key.- If you're tight on space (or cloud space) -
[FileOptimizer](https://nikkhokkho.sourceforge.io/static.php?page=FileOptimizer)is nifty, albeit the author's webpage is... bad, and I would not 100% trust the results (backup!). I list some near duplicate image finders in the graphics section below. And[Compactor](https://github.com/Freaky/Compactor)helps with windows file compression. [BareTail](https://www.baremetalsoft.com/baretail/index.php)seems nice.

**Coding**

- Visual Studio plugins/extensions
- MUST-HAVE Extensions (from the VS extension store):
[Debug Command Line](https://marketplace.visualstudio.com/items?itemName=SamHarwell.DebugCommandLine)(adds a drop-down that allows to quickly switch between recently used command-lines) - not available for vs2022 :(- Debug Single Thread, Concurrency Visualizer
[Clang-Format](http://clang.llvm.org/docs/ClangFormat.html)is powerful and[easy](http://clangformat.com/)~~and~~[CodeMaid](http://www.codemaid.net/)is very nifty as well.- Other less-used ones:
[Indent guides](https://marketplace.visualstudio.com/items?itemName=SteveDowerMSFT.IndentGuides2022)is not bad. I like[Continuous formatting](http://vlasovstudio.com/continuous-formatting/)as I found auto-formatting to be great but hard to apply in existing codebases.[SymbolSort](http://gameangst.com/?p=320)(not really a plugin...). Visual Studio[Color Theme Editor](https://marketplace.visualstudio.com/items?itemName=VisualStudioPlatformTeam.VisualStudio2019ColorThemeEditor)- not available for vs2022 - the replacement seems... worse :/ ~~I used to rely on~~[Visual Assist X](http://www.wholetomato.com/)(and[disabling Intellisense](http://c0de517e.blogspot.com/2008/02/visual-studio-2005-intellisense.html)), but nowadays I just use find in files (SSDs!) most of the times...- Text editors
- The following two where my previous "must have" choices, but VScode (below) is so good nowadays that I don't need other things (while I do need VS code for python, javascript etc...)
[NotePad++](http://notepad-plus-plus.org/)for almost everything (with[this HLSL](http://mynameismjp.wordpress.com/2012/11/04/hlsl-udl/)syntax add-on by Pettineo).[Sublime Text](http://www.sublimetext.com/)(especially for OSX, where NotePad++ is not available)~~Markdown editors~~(I used to like... but really markdown does nothing for me that plain .txt does not, so that exploration ended...)~~I still write a lot of plain .txt files, and using markdown gets you some formatting for free.~~[Typora](https://www.typora.io/)is my choice (available on OSX too).[MarkDeep](https://casual-effects.com/markdeep/)is nice,[Marp](https://yhatt.github.io/marp/)can be cute as well (for presentations, there are many other similar ones).- LaTeX for publications
- I use
[TexStudio](https://sourceforge.net/projects/texstudio/)and[BasicTeX](https://tug.org/mactex/morepackages.html)(a smaller version of MacTeX) on OSX (then manually add packages I need via the command line package manager). - Sometimes you need
[a hex editor](http://mh-nexus.de/en/hxd/)(e.g. to open huge files) - IDEs / environments.
- MUST-HAVE Visual Studio Code is great nowadays (also on OSX)
- Python
- MUST-HAVE
[Anaconda](http://www.continuum.io/downloads)is my favorite scientific python distribution (I use it on OSX too) [Python tools for Visual Studio](https://pytools.codeplex.com/),[PyCharm](https://www.jetbrains.com/pycharm/)(OSX too)~~I like interactive environments like~~[Spyder](https://code.google.com/p/spyderlib/)and IPython/Jupyter, which are included in many "scientific" python distributions.~~For most other things (and for OSX...),~~[JetBrains](http://www.jetbrains.com/)has an IDE.- Everybody in (AAA) videogames is on P4, but the outside world likes GIT too.
[Fork](https://git-fork.com)is my current poison - but I still hate git. Also works on OSX[SourceTree](http://www.sourcetreeapp.com/)is a good alternative, also works on OSX- Other development tools:
- MUST-HAVE
[Beyond Compare](http://www.scootersoftware.com/moreinfo.php)is a must for programming.[Araxis Merge](http://www.araxis.com/merge/)is also nice to have. [Very Sleepy](http://www.codersnotes.com/sleepy)(windows sampling profiler) as in most cases I don't have[VTune](https://software.intel.com/en-us/intel-vtune-amplifier-xe)around. AMD[CodeXL](http://developer.amd.com/tools-and-sdks/opencl-zone/codexl/)is very useful too- Faster "find in files":
[SilverSearcher](https://github.com/ggreer/the_silver_searcher)~~/~~[RipGrep](https://github.com/BurntSushi/ripgrep) [ZealDocs](https://zealdocs.org/)offline documentation browser (OSX too - Dash).[Cheatsheet](https://www.mediaatelier.com/CheatSheet/)on Mac is also nifty[Include files dependency watcher](http://www.mobile-mir.com/cpp/),[Dependency walker](http://www.dependencywalker.com/)~~Sometimes, C++ analysis software~~[Lattix](http://www.lattix.com/)and[VisualC++Depend](http://www.cppdepend.com/), compiler/compilers like[Antlr](http://www.antlr.org/), but this is not really part of my daily routine nor of my "default" install[CppCheck](http://cppcheck.sourceforge.net/), OpenCppCoverage[Volatility framework](http://code.google.com/p/volatility/)and[Intel Pin](https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool)for really nasty stuff

**Graphics and Rendering**

- MUST-HAVE
[IrfanView](http://www.irfanview.ca/)is my image viewer. [Picturenaut](http://www.hdrlabs.com/picturenaut/), HDRShop and PTGui for HDR images.[VisiPics](http://www.visipics.info/index.php?title=Main_Page)is the best near-duplicate image finder I've found so far.[Czkwaka](https://github.com/qarmin/czkawka)seems a good alternative too, and much more modern (albeit with a messy UI)...- MUST-HAVE
[RenderDoc](https://github.com/baldurk/renderdoc)is great, a must![ApiTrace](../../assets/2ff568137d8d1cd4.img)is promising, [Intel's GPA](http://software.intel.com/en-us/vcsource/tools/intel-gpa)went from "ok" back to reccomended! And sometimes it manages to capture easily processes where RenderDoc fails to attach.[Pyramid ShaderAnalyzer](https://github.com/jbarczak/Pyramid)- MUST-HAVE
[VideoLan](http://www.videolan.org/vlc/)(OSX too) - Also for screen captures! I just use the desktop capture device and encode a mp4. On OSX, the built-in Quicktime allows do to screen recording.
not needed anymore as Win11 capture tool can do movie recording now (and OSX quicktime does as well)[Giffing](http://www.giffingtool.com/)and[ScreenToGif](https://screentogif.codeplex.com/)are great for desktop capture too (using webM encoding) Giphy capture works wonders as well (and it's on OSX too) -- Prototyping
- MUST-HAVE
[Processing](http://processing.org/)(also on OSX). - MUST-HAVE
[C-Toy](https://github.com/anael-seghezzi/CToy)(also on OSX). - Quite nifty! Tiny-C-Compiler integrated with some graphic drawing functions and wrapped with a file-monitor so your project live updates. Very useful to quickly test C algorithms!
~~SharpDX~~- MUST-HAVE
[Unity3D](http://unity3d.com/)is great for prototypes! [KodeLife](https://hexler.net/software/kodelife/)for shader experiments. (also on OSX)- Other stuff
[MeshLab](http://meshlab.sourceforge.net/)for 3d stuff.[Marmoset Toolbag](http://www.marmoset.co/)and[cmftStudio](https://github.com/dariomanesku/cmftStudio)which is somewhat similar, but opensource.- I hate Gimp but I do use sometimes the portable version if I don't have Photoshop on a given machine.
- MUST-HAVE
[Blender](https://www.blender.org/)is great now!

**Desktop**

[AutoIt](http://www.autoitscript.com/site/autoit/)is NIFTY!- I use it to craft quick GUIs around command-line tools or to automate GUI tools... It's really nice when you have to do a given thing over and over, and its basic-inspired language makes me nostalgic too. Also, is "portable", which I always prefer.
[AutoHotKey](http://www.autohotkey.com/)uses AutoIt scripting, but I didn't use it yet. ~~MUST-HAVE OSX I use~~[Alfred](http://www.alfredapp.com/)- MUST-HAVE Acrobat
[Reader](http://get.adobe.com/reader/)or better[SumatraPDF](http://blog.kowalczyk.info/software/sumatrapdf/free-pdf-reader.html)or[MuPDF](https://mupdf.com/)(also reads EPUB and other formats) that does not annoy the user with endless updates. But usually I get acrobat pre-installed on work computers at which point I don't bother with alternatives. [ProcrastiTracker](http://www.procrastitracker.com/)... Also for "productivity" I like sometimes to use the "pomodoro technique", I have a kitchen timer on my work desk that seems to work best (I like it being physical and ringing), but[ChronoSlider](https://itunes.apple.com/ca/app/chronoslider-lite/id450150098?mt=12)on OSX doesn't seem to suck as well (you'd be surprised how bloated or bad most timer apps are...)- System tools
(for some reason, I did not have the need for this one in a long time - used to be a must have)~~Unlocker~~[Sysinternals tools](http://technet.microsoft.com/en-ca/sysinternals)(ProcMon, FileMon,[VMMap](http://technet.microsoft.com/en-ca/sysinternals/dd535533.aspx),[RamMap](http://technet.microsoft.com/en-ca/sysinternals/ff700229.aspx)...)- MUST-HAVE
[CCleaner](http://www.piriform.com/ccleaner)(now also on OSX) [Process Hacker](http://processhacker.sourceforge.net/)[RapidEE](http://www.rapidee.com/en/about)(environment variable checker/editor), also portable.[NirSoft](https://www.nirsoft.net/)tools-~~ShutUp10~~[BloatyNosy](https://github.com/builtbybel/BloatyNosy)is important as Win11 is really starting to pack A LOT of malware. Edge is a cesspool too - I still use it, but one needs to disable a ton of crap!- All of these are deprecated now mostly because I can't dual boot Arm Macs into Windows...
~~MUST-HAVE~~[SharpKeys](http://www.randyrants.com/sharpkeys/)**if**I need to remap some of my keyboard keys~~Some keyboards emit "weird" scancodes (e.g. my wired Apple Italian keyboard) the only program which I've found to be flexible enough to recognize them is~~[KeyTweak](http://eltepedia.blogspot.com/2008/07/swap-alt-commandwindows-logo-in-boot.html).~~By the way, Win 8.1/bootcamp on my MBPr2013 does dragging horribly, but it seems better if you enable the (unrelated!) "tap to click" and "dragging" options in bootcamp.~~[Trackpad++](http://lifehacker.com/5927160/trackpad%252B%252B-greatly-improves-your-macbooks-trackpad-in-windows)is also related but I haven't tried it yet - same people do a number of bootcamp-related apps[http://www.forbootcamp.org/](http://www.forbootcamp.org/)- MUST-HAVE On OSX when using the external mouse you might want to not use natural scrolling, while keeping it enabled for the trackpad.
[Scroll Reverser](https://pilotmoon.com/scrollreverser/)does that! ~~MUST-HAVE This website -might- have more up-to-date AMD GPU drivers for Bootcamp~~[https://www.bootcampdrivers.com/](https://www.bootcampdrivers.com/)(but check also the official AMD bootcamp page)~~Other OSX MUST-HAVE~~~~is~~Not relevant anymore for M1 et al Macs...[gSwitch](https://github.com/CodySchrank/gSwitch)to force integrated GPU only (or discrete only).[Background Music](https://github.com/kyleneideck/BackgroundMusic)allows to change audio volume per app.- MUST-HAVE when I have multiple machines:
[Synergy](http://synergy-foss.org/)for keyboard/mouse sharing across computers. - Command-line / Terminal
~~I love Cathode (unfortunately abandoned) on OSX. Also on OSX:~~~~CoolRetroTerm, which is opensource, but it's not quite as great.~~Nowadays, I use[Alacritty](https://github.com/alacritty/alacritty)- I'm not really a command-line ninja, but I've started adopting it a bit more. I usually install tmux, nnn, tldr, a recent version of nano.
~~Window management various~~~~1Up industries stuff is really good:~~[Fences](http://www.stardock.com/products/fences/),[Bins](http://www.1upindustries.com/bins/)([7Stacks](http://alastria.com/?p=software-7s)is somewhat similar, and free, emulates OSX stacks).[SysTools Desktops](http://technet.microsoft.com/en-us/sysinternals/cc817881.aspx)is a tiny free utility for virtual desktops~~My own bugfixed version of AnAppADay~~[Jedi Concentrate](http://www.anappaday.com/downloads/2006/09/day-10-jedi-concentrate.html)(a Windows clone of the OSX[Think](http://freeverse.com/mac/product/?id=7013)[Isolator](http://willmore.eu/software/isolator/),[Spirited Away](http://etherealmind.com/osx-spirited-away-productivity-tool/)is a nice complement to these too, there are clones as well).[WindowFX 4](http://www.stardock.com/products/windowfx/)does the same too (and much more)~~On OSX some people/setups seem to need~~[SmoothMouse](http://smoothmouse.com/)to avoid mouse lag~~There are a lot of other tools that look nifty but I didn't end up using them often...~~[Displayfusion](http://www.displayfusion.com/)looks neat but I didn't try it yet, the most interesting feature for me is placing a second taskbar with only the applications used on the second monitor there,[MultiMon](http://www.mediachance.com/free/multimon.htm)does it for free. A tiling window manager is good if you have a lot of screen space, like[WinSplit](http://www.winsplit-revolution.com/)(OSX alternative:[SizeUP](http://www.irradiatedsoftware.com/sizeup/))- MUST-HAVE OSX: not a tool, but
**important, kill the lag in the dock autohide**: defaults write com.apple.Dock autohide-delay -float 0 - There are tools that provide a GUI on top of the
[defaults system](https://www.defaults-write.com/). E.g.[TinkerTool](https://www.bresink.com/osx/TinkerTool.html)

~~Speaking of using Apple hardware, if you have a laptop and you like your natural scrolling direction on the touchpad,~~

~~Speaking of using Apple hardware, if you have a laptop and you like your natural scrolling direction on the touchpad,~~[WizMouse]can enable that.

**Virtualization**


- It's nifty to be able to run VMs, I typically do that both to isolate my personal stuff on work computers, to quickly run experiments, to try things that are available only on other OS, and if I need windows on mac...
[VirtualBox](https://www.virtualbox.org/)can be useful and it's free, even if I usually prefer VmWare (sometimes I use the Player with pre-made OS images).- HyperV, included with Windows, can be great too, it's not a bad idea to keep your different work environments in different VMs / drives nowadays, as drive space is not a big deal.
- MUST-HAVE On OSX, Parallels is really good! Can run Windows 11 ARM in a VM on M1 macs, with really good performance. Windows 11 can, in turn, run x64 apps (ala Rosetta for mac). Magic!
- UTM is decent (qemu based) but not as well optimized
- I sometimes used
[Docker](https://www.docker.com/)when I needed some python library is available on Linux only or that is complicated to configure (e.g. happens for deep neural network stuff...).

**Internet & Remoting**

~~MUST-HAVE~~[Chrome](http://www.google.com/chrome/?brand=CHMB&utm_campaign=en&utm_source=en-ha-na-us-sk&utm_medium=ha)(w/a session manager to not swear if things crash, a tab auto-suspender, and I also disable flash/other plugins auto-start and use the[morphine](https://chrome.google.com/webstore/detail/morphine/fbnpehpbojenlldmfcopeajkichnnjpo?hl=en)extension at work)- MUST-HAVE No longer using Chrome! I really don't love Google's dominion these days, and the fact that Chrome forces to associate the session with a profile is really inconvenient for me. Nowadays, I tend to use the native browser (Edge on windows, Safari on OSX) for "casual" browsing, where especially on OSX I hope/think Safari will do a better job at preserving battery, and for work I use Firefox with
[tab session manager](https://github.com/sienori/Tab-Session-Manager), which allows me to sync tabs across computers/browsers. - MUST-HAVE
[DropBox](http://www.dropbox.com/)(even if I'm thinking to migrate out of it) [Google Calendar Sync](http://support.google.com/calendar/bin/answer.py?hl=en&answer=98565), if the company doesn't have decent intranet VPN access- MUST-HAVE Zoom is GREAT! Works seamlessly, it's really an amazingly made app.
~~MUST-HAVE~~[Skype](http://www.skype.com/en/).- MUST-HAVE
[Parsec](https://parsec.app)is GREAT! The best remote desktop app ever! - Note, on one router I found that I had to manually force a port in Parsec and then
[open that port](https://support.parsec.app/hc/en-us/articles/360045297592-How-to-port-forward-Parsec)to allow the connection. YMMV. ~~For home at least I use a free~~[TeamViewer](http://www.teamviewer.com/en/index.aspx)account ([join.me](http://join.me/)is nifty), which I find many times easier/better than setting up UltraVNC.[Splashtop](http://www.splashtop.com/home)looks promising.

**Math**

~~I still use the~~[PowerToy](http://www.microsoft.com/windowsxp/downloads/powertoys/default.mspx)Calculator ([patched](http://blog.red-stars.net/technology/software/hacking-windows-xp-powertoy-calculator-to-run-in-vista/)to install on Win7/Vista)[Desmos](https://www.desmos.com/)nowadays is better.- MUST-HAVE
[Mathematica](http://www.wolfram.com/mathematica/)(OSX too) if the studio has a license for it (or I make them buy one!) [GeoGabra](http://www.geogebra.org/cms/en/)can be useful when tinkering with geometrical constructions, it's quite powerful (currently the beta of v5 supports 3d too, and it's available "portable" as well) but slightly more focused on contraints than I'd like (I'd love something very interactive with optional constrained stuff, like a parametric CAD)~~Some people swear by~~[TikZ](http://sourceforge.net/projects/pgf/)([examples](http://www.texample.net/tikz/examples/tag/3d/)), looks extremely cool but it's not interactive...~~On the simpler side, and 2d only,~~[DrGeo](http://www.drgeo.eu/)(portable as well) is great to tinker[SciLab](http://www.scilab.org/)which I prefer over Octave (that is though more compatible w/MatLab), but nowadays I don't really care about MatLab-like environments, I prefer either Mathematica or SciPy (Anaconda)

## 7 comments:

Thanks for the links - esp. to processing. I should have found that years ago:D

Wow, this is really close to the settings that I had a while ago (before migrating to osx for work), with the exception of visual assist which I found to be a real life saver once properly configured.

use linux and shit like unlocker you will not need.

Anon: Agreed, in Linux I won't need unlocker.




I would just need a replacement for visual studio, photoshop, 3dsmax, directX, the console SDKs and everything needed to make videogames...

So basically I would have no job, but yes, I would need no unlocker.

Thanks for the tip!

Don't forget Rapid Environment Editor for inspecting those pesky env vars:


http://www.rapidee.com/en/about

I am missing Ditto on the list. Copy/paste history, a must-have and game-changer for me.

Try out Ditto, a copy-paste history app. Gamechanger.

Post a Comment