---
title: 'Dolphin Progress Report: Release 2509'
url: https://dolphin-emu.org/blog/7E/
author: OatmealDome
published: '2025-09-16'
source_blog: Dolphin Emulator - GameCube/Wii games on PC
source_site: https://dolphin-emu.org/
category: graphics
fetched: '2026-04-19'
---

The Dolphin Blog is full of stories surrounding games, their development, and the challenges they present to emulate them. And in these stories, we sometimes have some recurring characters that we gain a better understanding of over time. Factor 5 and their [Star Wars: Rogue Squadron](https://wiki.dolphin-emu.org/index.php?title=Category:Rogue_Squadron_(Series)) games continue to amaze us time and time again as we find different ways that they push the hardware to its limits. [The Legend of Zelda: The Wind Waker](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_The_Wind_Waker) uses many graphical tricks to create a timeless style, that surprises again and again with just how much care was put into every detail. And, of course the [Metroid Prime](https://wiki.dolphin-emu.org/index.php?title=Metroid_Prime) series shows up often given its sensitivity to even subtle changes to emulation.

However, as with every story, there have to be villains as well. One such *villain* is the **The Disney Trio of Destruction™**. For years, users have awaited the final showdown with these games. And guess what? They're finally playable *right now*. But are these games truly villains? Or were they just misunderstood? In this report, we dive into The Disney Trio of Destruction™ once and for all to determine their true nature.

Not every returning character is a game. Sometimes we also have to deal with our own issues, such as *Dual Core mode*. It is constantly breaking games, disabled in many popular games by default, and the source of most crashes in Dolphin. But is Dual Core really a hack? Or is Dolphin simply doing something wrong. In this report, we'll dive into the history of Dual Core and make a change that was long overdue.

On top of all of this, several longstanding features in Dolphin also saw some major upgrades, and we'll also get to those throughout the Dolphin Progress Report. With that, let us begin.

**NSOh No**[¶](https://dolphin-emu.org#nsoh-no)

![Nintendo Switch Online GameCube Controller](../../assets/59d187896dc609ad.avif)

Since the release of the Nintendo Switch 2, we have been repeatedly asked if Dolphin supports the [Nintendo Switch 2 NSO GameCube Controller](https://www.nintendo.com/us/store/products/nintendo-switch-2-nintendo-gamecube-controller-120833/). The short answer is not yet. The long answer is that Switch 2 controllers do some weird things; rather than take this on ourselves, we are waiting for the professionals at SDL to figure it all out. Currently they have an implementation, but it's early and missing features. Once they get it to a good place and it is in an SDL release, we will adopt it into Dolphin.

For now, please be patient.

**Notable Changes**[¶](https://dolphin-emu.org#notable-changes)

All changes below are available in Release 2509.

It is no secret that Dual Core mode in Dolphin is unstable. If you've ever had Dolphin randomly crash while going into fullscreen, switching windows, or simply for no apparant reason, you've likely run into a Dual Core crash. In fact, pretty much any time someone comes to us with a crash, the first thing we tell them is to turn off Dual Core.

However, we doubt users understand the full extent of the problem.

But if Dual Core mode is so bad, why haven't we removed it?

For all of its downsides, *Dual Core is fast*. Dolphin is largely bound by single thread performance, leaving the many cores of a modern CPU sitting idle. Splitting our primary emulation thread in two can spread the load across more cores and better fit modern CPU designs. This is very effective, and was in fact *necessary* in the early days to get playable speeds *at all*, and some users still rely on it even today.

Instead, we have tried to *fix* Dual Core repeatedly over the years. The most successful of those efforts was *Synchronize GPU Thread* (SyncGPU). Never heard of it before? Well, that's because despite being the most successful of our efforts, it didn't exactly catch on.

In a typical game, SyncGPU is in-between Dual Core and Single Core, in every sense. And that's the feature's biggest failing. It's neither as stable as Single Core nor as fast as Dual Core, and ends up appealing to neither group. In a game with Dual Core instability that SyncGPU was designed to solve - [Metroid Prime 2](https://wiki.dolphin-emu.org/index.php?title=Metroid_Prime_2:_Echoes_(GC)) in the graph above - it performs no better than Single Core mode, yet isn't as stable. To make matters worse, the additional synchronization between threads creates **stutters**, so SyncGPU *feels* worse than Single Core or Dual Core.

So, what's the solution to this problem? We can't make Single Core mode faster without making it less stable, and we can't make Dual Core mode more stable without slowing it down. This has been troubling us for many years.

Fortunately, time has provided us with an alternative. You may have noticed from the graph above that all three processor emulation techniques are *way beyond full speed*. In 2025, most of our desktop users have PCs that are **overpowered** for Dolphin. We are at the point where many of our users can comfortably use Single Core at full speed, but most *don't* because it's not the default. So why not do just that?

We have finally made the decision to disable Dual Core mode by default on desktop. We'd much rather have users mutter about Dolphin being slower than be heartbroken over lost save data caused by a setting they didn't even realize existed. If your computer isn't powerful enough and you need the speed, feel free to turn it back on at your own risk.

If you are on Android, we realize the situation is a bit different on that platform. With all the other things that Android users have to deal with - suspect graphics drivers, aggressive CPU governors, and generally weaker hardware, to name a few - we don't think it's time to swap the default there yet. As such, Dual Core will remain enabled by default on Android for the foreseeable future.

Now, you may be reading this and thinking *why is Dual Core bad?* In the process of writing this article, we decided to split the more technical discussion into its own section. You can find an in-depth dive into Dual Core mode and why it is so unstable at the bottom of this report. Feel free to zip straight to it with [this handy link](https://dolphin-emu.org#a-dual-corerection) if you're interested!

Back in 2022, ** xperia64** made a slew of improvements to Dolphin's DSP accelerator code. Unfortunately, due to the difficulty of reviewing code like this and the fact that it had little in the way of visible results, it wasn't merged right away. Additionally, earlier this year, a bug was found in the original pull request that caused audio to be missing in certain cases.

However, after finally receiving approvals from several reviewers along with additional fixes and testing, it was finally merged as [2503-509](https://dolphin-emu.org/download/dev/master/2503a-509/) as a seemingly low-risk addition before the next release. Even though this code would globally affect DSP-HLE, DSP-LLE Recompiler, and DSP-LLE Interpreter, we unfortunately didn't test the less commonly used backends nearly as much as we should have.

While DSP-HLE and DSP-LLE Interpreter were both fine, oversights in how DSP-LLE Recompiler handled exceptions caused hangs in select titles after the improvements. While we don't recommend using the DSP-LLE backends due to how performance intensive they are, there is one major reason to do so: Surround Sound support. Users using DSP-LLE Recompiler for that feature found that their games weren't booting in the 2506 release.

After realizing what was wrong, ** AdmiralCurtiss** jumped into action with two hotfixes to how the DSP-LLE Recompiler handled exceptions. One was simply updating the recompiler to allow for exceptions on store instructions, while the other had to do with exception flag handling in specific cases.

With these updates, our DSP-LLE Recompiler users can finally relax, as it is again is functioning how it always has: slowly, but reliably.

The Disney Trio of Destruction™. Much like the Four Horsemen of the Apocalypse before them, the Trio of Destruction™ are a fearsome group that bring despair in their wake. Once thought to just be ordinary games, we learned very quickly not to underestimate them. First, [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3) appeared. Then, [Cars 2](https://wiki.dolphin-emu.org/index.php?title=Cars_2). And finally, [Disney Infinity](https://wiki.dolphin-emu.org/index.php?title=Disney_Infinity). By the year 2013, the unholy trinity was complete.

Each game challenged what was expected of a Wii game. Our efforts started with [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3), as it was the first of the trio to make it to the market in 2010 and did not work in Dolphin! The rest would release before *any* of them worked. However, in 2014, [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3) [would seemingly be defeated](https://dolphin-emu.org/blog/2014/10/31/dolphin-progress-report-october-2014/#40-3669-correct-the-physical-memory-access-to-mem2-via-the-mmu-by-skidau). A crack in the armor of the inpenetrable three, we thought. Soon the others would fall, we thought.

How foolish we were.

Even after fixing [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3), the other two games would still fail shortly after boot. The failure was so spectacular that everyone thought that Dolphin had to be doing something very wrong. Never did we consider that perhaps we were doing *exactly* what the game wanted us to do.

Over the years, we've been lucky enough to talk to a few developers that worked on various GameCube and Wii games. Most developers are very open toward emulation and *happy* to see us fix emulation bugs in the games they worked so hard on. However, we're going to go out on a limb and say that [Avalanche Software](https://wiki.dolphin-emu.org/index.php?title=Category:Avalanche_Software_(Developer)), the team behind the Trio of Destruction™, weren't so fond of us. Not only did they leave [crude messages hidden in game data for "hackers" to find](https://tcrf.net/Meet_the_Robinsons_(GameCube)#Dev_Message), but we also suspect that someone on their team was *actively monitoring us*.

While [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3) took a few years to get working, the writing was on the wall for quite some time that *eventually* it would be solved. So, for Avalanche's next two games, we believe that they left a trap specifically designed to defeat Dolphin: the **dcache suicide pill.**

It takes (relatively) a lot of time to move data between RAM and the CPU. To speed up memory operations, the GameCube and Wii's CPU has something known as the *dcache* (a special [L1 cache](https://en.wikipedia.org/wiki/CPU_cache)). This "data cache" holds the contents of recently accessed memory. Any subseqent reads or writes to that memory can be handled by the dcache instead of RAM, which greatly increases performance. [Until 2022](https://dolphin-emu.org/blog/2023/02/12/dolphin-progress-report-december-2022-january-2023/#50-18192-emulate-ppc-datacache-by-mkwcat), Dolphin didn't emulate the dcache whatsoever, and just had all memory operations work directly with RAM.

This created a vulnerability.

All Avalanche had to do was tell the CPU to write garbage data into a region of memory where critical game code was stored. However, the game would write *exactly enough* garbage data to fill up the dcache without the CPU automatically flushing the changes to RAM. Then, the game would tell the CPU "never mind" and *invalidate the dcache*. Overwriting critical game code with garbage should leave the game non-functional, but the cache invalidation would prevent the garbage from ever reaching RAM! Dolphin, however, didn't emulate the dcache, so the instruction would just immediately overwrite the critical code in RAM and disable the game.

This trick is dirty, devious, and very effective at stopping Dolphin, but it doesn't really do much else. While Dolphin has ran into [various anti-piracy techniques over the years](https://dolphin-emu.org/blog/2024/12/02/dolphin-progress-report-release-2412/#2409-313-fix-kirbys-adventure-wii-metafortress-bypass-patch-by-vaguerant), all of them were intended to detect USB/SD loaders on real hardware. The dcache suicide pill *will never trigger on console*, even when using the shoddiest of USB loaders. We can't think of any other reason for it to exist except to stop Dolphin from emulating [Cars 2](https://wiki.dolphin-emu.org/index.php?title=Cars_2) and [Disney Infinity](https://wiki.dolphin-emu.org/index.php?title=Disney_Infinity).

Once we figured this out, we had two options: leave the games broken and hope someone would eventually implement dcache emulation, or fight fire with fire and create a hack that prevents the game from overwriting itself. [We chose to do the latter, as it should have been enough to make the games fully playable](https://dolphin-emu.org/blog/2017/02/01/dolphin-progress-report-january-2017/#50-2204-hack-to-protect-lower-mem1-from-malicious-game-code-by-booto). While Dolphin later [gained the ability to actually emulate the dcache](https://dolphin-emu.org/blog/2023/02/12/dolphin-progress-report-december-2022-january-2023/#50-18192-emulate-ppc-datacache-by-mkwcat), enabling it incurs a *significant* performance penalty, so it is best avoided whenever possible.

Nowadays, those that demand accuracy and those that want performance can both be happy, right? Unfortunately, by the time all of this was solved, the games ran terribly in Dolphin. Even [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3) had poor performance, despite it supposedly running *okay* at one point. So what the heck was going on now?

The answer... was [ Dynamic BATs](https://dolphin-emu.org/blog/2016/09/06/booting-the-final-gc-game/).

[Star Wars: The Clone Wars](https://wiki.dolphin-emu.org/index.php?title=Star_Wars:_The_Clone_Wars) earned its right as [the final GameCube game Dolphin booted](https://dolphin-emu.org/blog/2016/09/06/booting-the-final-gc-game/) by doing something no other GameCube game did. It not only allocated the BATs (Block Address Translations) to non-standard locations, but it also did so dynamically during execution. Dolphin's memory management emulation was built on the idea that it knows where valid virtual memory is going to be in advance, and games that subverted those expectations outright **broke** Dolphin. Supporting Dynamic BATs required a *full rewrite* of Dolphin's memory management emulation.



![Booting the Final GameCube Game article header](../../assets/b5507f9d4d7f5ed0.jpg)

As tends to happen during a large scale rewrite, there was *so much to do* that a few things fell through the cracks. And while working on Dynamic BATs and preparing the gigantic article on the achievement of booting the last GameCube game, we overlooked something important.

Dynamic BATs *destroyed* performance in [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3), despite it not affecting any other Wii games. To make matters worse, the dcache suicide pills in [Cars 2](https://wiki.dolphin-emu.org/index.php?title=Cars_2) and [Disney Infinity](https://wiki.dolphin-emu.org/index.php?title=Disney_Infinity) were hacked out *after* Dynamic BATs was finished. As far as we knew, these games were always incredibly slow.

All of the clues were there for us to take on the final mystery, but we didn't put the pieces together until a few months ago, when a user complained that [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3) ran a lot better in Dolphin 5.0 than the newer releases. That, followed up with a bisect to Dynamic BATs, prompted some investigation.

With the subtlety of a wrecking ball, ** Billiard** decided to try to just hack out Dynamic BATs in the latest builds and see if that restored performance. It was a quick and dirty hack that broke a bunch of other games.

*But it worked*. Not only was

[Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3)'s performance problem resolved, but the entire Trio started running at reasonable speeds!

After some discussion, we had an eureka moment. Dynamic BATs made the games slower because *we started emulating them more accurately*.

The Disney Trio of Destruction™ use the typical memory addresses that any other Wii game would use. However, they *remove the default BATs* and rely on Page Tables in those areas of memory. Memory accesses via Page Tables always goes through our slowmem code, meaning that they don't benefit from fastmem - one of Dolphin's biggest performance optimizations. That's why the Trio was so slow! This is also why simply disabling MMU [didn't speed up the Trio](https://dolphin-emu.org/blog/2022/05/17/dolphin-progress-report-february-march-and-april-2022/#50-16005-remove-mmu-default-in-disney-trio-of-destructiontm-by-jmc47). Dolphin still supported moving the BATs to different locations, so disabling MMU ended up doing exactly nothing.

Upon seeing the success of the hack, ** JosJuice** jumped into action. They had an idea that would allow Dolphin to harness the power of BATs without needing to gut the emulator. After identifying the game code that actually set up the BATs,

**forced the games to put them back at the default locations. And since the Trio**

[JosJuice](https://github.com/JosJuice)*all use nearly identical code*, the same patch works in all three games, with the only differences being the instruction locations.

This means that in 2025, you can *finally* emulate [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3), [Cars 2](https://wiki.dolphin-emu.org/index.php?title=Cars_2), and [Disney Infinity](https://wiki.dolphin-emu.org/index.php?title=Disney_Infinity) on powerful hardware at **full speed**. These games are still demanding despite being defanged, but a modern gaming PC should be able to handle them. If your PC is *absolutely unhinged*, you can even use [VBI Frequency Override](https://dolphin-emu.org/blog/2025/06/04/dolphin-progress-report-release-2506/#2503-517-add-vbi-frequency-override-by-samb-and-supersamus) to push them beyond 60 FPS for high refresh rate gaming!

For those of you that have been waiting for this moment, we hope you enjoy it. It's been a lot of fun investigating and wondering what could be wrong with [Toy Story 3](https://wiki.dolphin-emu.org/index.php?title=Toy_Story_3), [Cars 2](https://wiki.dolphin-emu.org/index.php?title=Cars_2), and [Disney Infinity](https://wiki.dolphin-emu.org/index.php?title=Disney_Infinity).

While our battle with the Disney Trio of Destruction™ is finally over, we have yet to defeat *the final bosses of all final bosses*: [Star Wars: Rogue Squadron II: Rogue Leader](https://wiki.dolphin-emu.org/index.php?title=Star_Wars_Rogue_Squadron_II:_Rogue_Leader) and [Star Wars: Rogue Squadron III: Rebel Strike](https://wiki.dolphin-emu.org/index.php?title=Star_Wars_Rogue_Squadron_III:_Rebel_Strike). Both of these games *heavily rely on Page Tables*, and a simple patch isn't going to fix either one. Their design was not out of malice, but because Factor 5 had no choice but to use Page Tables if they wanted to tap into the extra memory available in the GameCube's ARAM chip. And this was Factor 5, so *of course they did*. Thus, while we were able to hack the Disney Trio of Destruction™, if we ever want to make the Rogue Squadron games fast, we need to get good at Page Tables.

And for one *final* twist, a developer close to Avalanche Software during the development of these games reached out to us back in 2021. While they couldn't speak on the dcache suicide pill, they claimed that the interesting behaviors in the Trio of Destruction™'s memory managers weren't anti-emulation tricks. Instead, they had simply taken inspiration from [a presentation at GDC 2002 on virtual memory](https://www.gdcvault.com/play/1022542/Virtually-Limitless-Virtual-Memory-on)... **by the Director of Technology at Factor 5**.

The developer that reached out to us had a *pretty good point*, to be honest. After we ran into the dcache suicide pill, we were very quick to blame just about every odd behavior in these games as being anti-Dolphin tricks. In this case, using Page Tables instead of BATs as an anti-emulation trick doesn't really make any sense. After all, replacing the default BATs with Page Tables would have done nothing to stop Dolphin in 2010. The default BATs were hardcoded at the time and would have always been used regardless of what the game requested.

[2506-171](https://dolphin-emu.org/download/dev/master/2506-171/) and [2506-330](https://dolphin-emu.org/download/dev/master/2506-330/) - **Bluetooth Passthrough Improvements and Realtek Firmware Loading** by [Billiard](https://github.com/jordan-woyak)[¶](https://dolphin-emu.org#2506-171-and-2506-330-bluetooth-passthrough-improvements-and-realtek-firmware-loading-by-billiard)

[2506-171](https://dolphin-emu.org/download/dev/master/2506-171/)

[2506-330](https://dolphin-emu.org/download/dev/master/2506-330/)

[Billiard](https://github.com/jordan-woyak)

While Wii Remotes (and Balance Boards) connect using standard Bluetooth, they have some quirks that make them difficult to use with other devices. Connecting Wii Remotes works pretty well on Linux, though it's rather spotty on Windows. macOS has problems with even *pairing* Wii Remotes in the first place, as its Bluetooth stack doesn't like Nintendo's non-standard PIN codes. And you can forget Android entirely - while connecting Wii Remotes did work in the far past, it has been prohibited for some time. Sometimes, a Wii Remote will even just refuse to connect for unknown reasons, especially on Windows.

Assuming we can get the Wii Remotes connected, we still have to make some compromises to get things working. Nintendo made the odd decision to use the power-saving Bluetooth feature called “sniff mode” to adjust the Wii remote’s polling rate from 100Hz to 200Hz. Because “sniff mode” is a low level feature generally handled by the Bluetooth stack, regular applications are not able to control it. This effectively halves the rate at which we are able to poll the Wii Remote. Dolphin can duplicate input reports to “simulate” 200Hz and prevent games from getting upset over dropped inputs, but doing so can cause problems with motion control detection. This is why titles like [Sonic and the Secret Rings](https://wiki.dolphin-emu.org/index.php?title=Sonic_and_the_Secret_Rings) can be even more cumbersome when using real Wii Remotes, and why Wii Remote speaker audio is far worse when compared to a real Wii.

Wii Remotes also don't use a standard HID ([USB Human Interface Device](https://en.wikipedia.org/wiki/USB_human_interface_device_class)) descriptor, making them unusable as standard game controllers without special drivers. Dolphin mostly works around this by talking with them at the HID layer. Unfortunately, doing this does come with some downsides. For example, other programs running on the host device can disrupt communication. We most often see this with Steam on Windows.

Thankfully, a solution *was* devised almost a decade ago to deal with all of these problems. [In 2016](https://dolphin-emu.org/blog/2016/10/24/bluetooth-passthrough/), [leoetlino](https://github.com/leoetlino) added the ability to "pass through" a Bluetooth adapter directly to the emulated Wii with [a little bit of extra setup](https://wiki.dolphin-emu.org/index.php?title=Bluetooth_Passthrough). Bluetooth Passthrough avoids the headaches of dealing with unwieldy operating system Bluetooth stacks by simply giving the emulated Wii full control over the adapter. Because the Wii’s Bluetooth adapter operates using the standard [HCI protocol](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/host-controller-interface/host-controller-interface-functional-specification.html), many off the shelf Bluetooth adapters can be used with minimal adjustments. We could have proper 200Hz input polling, support off-brand Wii Remotes that standard Bluetooth stacks can't, and even handle the Wii Remote speaker data properly. You could even attach a real Wii's Bluetooth adapter to a USB port and get perfect or near-perfect Wii Remote support!

Bluetooth Passthrough does have some downsides, though. Because the emulated Wii has full control over the Bluetooth adapter, you can't connect other Bluetooth devices like headphones or controllers unless you have a second adapter. In addition, certain Dolphin features are not accessible when using Bluetooth Passthrough, like save states. Windows users are also required to install a special driver to override the manufacturer's driver and prevent it from loading. Despite these problems, however, Bluetooth Passthrough remains a popular feature because of all the benefits it brings.

Unfortunately, we've recently observed that more and more modern Bluetooth adapters aren't compatible with Bluetooth Passthrough, and it wasn't immediately apparent why.

While helping users out in our Discord, ** Billiard** noticed that many of the support requests seemed to be coming from users with Bluetooth adapters built off the Realtek RTL8761 chipset. Once he got his hands on one for himself,

**quickly found the problem. This particular chipset expects to have its firmware loaded by the operating system every time it is connected. When Dolphin has control over the adapter during Bluetooth Passthrough, the operating system doesn't get the chance to load that necessary firmware!**

[Billiard](https://github.com/jordan-woyak)** Billiard** took action to rectify this issue. First,

[2506-171](https://dolphin-emu.org/download/dev/master/2506-171/)overhauled the Bluetooth Passthrough code to improve general performance through better timing of packets and other minor tweaks. These changes affect

*every*adapter. Most importantly, it also separated Dolphin's emulation logic from the LibUSB logic as a step toward fixing the Realtek firmware problem.

[2506-330](https://dolphin-emu.org/download/dev/master/2506-330/) built upon the previous changes to add the ability to load Realtek firmware. When attempting to use a Realtek adapter with Bluetooth Passthrough for the first time, you will be prompted to allow Dolphin to download the appropriate firmware file from the internet. Once the firmware is downloaded, it is silently loaded on the device, just like the operating system would do. This takes what was previously a completely unsupported chipset and makes it work with Bluetooth Passthrough.

While fixing a single chipset might not seem that significant, given how common it is in modern Bluetooth adapters, this fix has *greatly* improved Bluetooth Passthrough's overall compatibility. Widespread adapters like the [TP-Link Bluetooth 5.3 Nano](https://www.amazon.com/TP-Link-Bluetooth-Receiver-Controller-UB500/dp/B09DMP6T22) and [Asus USB-BT500](https://www.amazon.com/ASUS-USB-BT500-Bluetooth-Backward-Compatible/dp/B08DFBNG7F) can now work with Bluetooth Passthrough!

You may have noticed our settings UI on desktop has been changing over the past few months. This is part of a greater overhaul that we will cover in detail in the future.

In the meantime, a new feature in Dolphin's Qt GUI is the "Map and Calibrate" button.

The Map and Calibrate option allows you to simply map and calibrate your joystick at the same time - just click and rotate the stick clockwise a couple of times. For basically any joystick, you'll get the ranges perfectly matched to that of a GameCube Controller, Classic Controller, or Nunchuck, with but a single click and a spin! For those needing specialized setups, you can still manually map everything normally then calibrate after.

HD Texture Packs are one of the most meaningful enhancements you can throw at GameCube and Wii games. Limited by the storage medium and memory capacity, game developers at the time worked hard to optimize texture resolution. Typically, heroes and main locations were the focus of texture resources, while background elements got the N64 treatment. Those choices look alright at SD resolutions, but when blown up to 4k, the low resolution textures can become extremely obvious.

As such, it shouldn't be surprising to know that Dolphin has supported HD textures since ** 2009** and that the feature has continued to evolve over the years. We've added several texture formats (

[many that can run natively on the GPU itself without conversion)](https://dolphin-emu.org/blog/2017/09/02/dolphin-progress-report-july-and-august/#50-4894-support-loading-bc7-bptc-textures-from-dds-files-by-stenzek),

[optional preloading](https://dolphin-emu.org/blog/2015/06/01/dolphin-progress-report-may-2015/#40-6415-preload-custom-textures-by-degasus),

[resource packs](https://dolphin-emu.org/blog/2019/02/01/dolphin-progress-report-dec-2018-and-jan-2019/#50-9217-implement-resource-packs-by-spycrab), and

[reduced duplication through smarter handling of mipmaps](https://dolphin-emu.org/blog/2015/02/01/dolphin-progress-report-january-2015/#40-5234-improve-custom-texture-handling-by-degasus)and more over the last fifteen years.

The biggest fundamental change to how custom textures were loaded was just two years ago, when we quietly added a new asset management system that allowed for loading textures without blocking emulation. This change didn't really amount to much, except that now instead of performance stuttering while textures are loaded, any custom textures that weren't loaded in time would pop-in. Depending on your computer, you might not have noticed this change at all!

The resource manager is a further evolution of this change. It further allows Dolphin to manage custom textures to ensure that HD Texture Packs can work on a wider variety of hardware. The resource manager tracks the requests per frame and orders them based on what was requested last. The newest requests get serviced first, leading to better perceived performance for loading textures. The resource manager also tracks memory usage and can purge textures that haven't been used as much if the machine is low on RAM in order to prevent out of memory issues.

One more bonus is that custom texture loading is now *multithreaded*. This ensures that texture loading no longer needs to borrow resources from Dolphin's main CPU emulation thread and can live on its own CPU core. This greatly improves the performance of loading many textures at once and reduces pop-in on modern multi-core CPUs. Combined with the other improvements the resource manager brings, HD Texture Packs should no longer cause performance issues in most cases.

One of the reasons that various [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii) online services have a problem with Dolphin users isn't just the ease at which it makes cheating, but that even innocent users can also cause some havoc. While you may think that *lagging* during a race would be a disadvantage, due to the way [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii) works, it can *actually put you ahead*. During the race, you'll be in a lower position, getting better items and avoiding blue shells. But when you finish, the game only uses your *final time* to calculate your finish position. If you lagged for three seconds over the course of the race and visually finished two seconds behind the leader, you will end up winning the race in the results screen. Yikes.

Modern [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii) fan servers have protection for this, but it's still an annoying behavior and can definitely cause problems in other games that aren't big enough to get patches to work around Dolphin's quirks.

For this situation and others like it, ** Billiard** has brought a new option that will help smooth over small lag spikes.

**Correct Time Drift**allows Dolphin to speed up after a lag spike in order to keep Dolphin lined up with real-time progression.

If something causes emulation to slow down or stutter for a short period, Dolphin will use the next opportunity to speed up and catch back up to real time. For temporary issues like network packet drops during NetPlay, shader compilation, and JIT cache flushing, this feature can keep Dolphin locked to the actual time. Outside of certain online games like [Mario Kart Wii](https://wiki.dolphin-emu.org/index.php?title=Mario_Kart_Wii), this can also be useful for speedrunners to ensure that the emulated time is synchronized to the real time even during any minor bobbles in emulation.

Note that some actions will cause Dolphin to abandon time correction. If you disable the speed limiter (holding TAB by default) at any point, Dolphin will not try to slow down for the duration that you are bypassing the speed limit and will choose a new "par time" once the limit is restored.

**This Release's Contributors...**[¶](https://dolphin-emu.org#this-releases-contributors)

Special thanks to [all of the contributors](https://github.com/dolphin-emu/dolphin/graphs/contributors?from=2025-06-01&to=2025-09-14&type=c) that incremented Dolphin by 433 commits after Release 2506!

**A Dual Coreーrection**[¶](https://dolphin-emu.org#a-dual-corerection)

It has become established within the Dolphin project that Dual Core mode is a hack. It's well known that it is unstable, current developers have called it a hack, we've said it repeatedly here on the blog, and ector (one of Dolphin's founders) has said he [regretted Dual Core](https://dolphin-emu.org/m/user/blog/progress-report/2507/dualcoremistake.png). That really sounds like a hack! However, in the process of writing this article, we consulted with retired Dolphin developers about Dual Core, and had an enlightening conversation.

They told us that Dual Core mode is not a hack. In fact, **Dual Core mode is more like the original hardware than Single Core mode.** And yet, Single Core mode is more accurate.

To explain this, we need to go into detail on what Dual Core mode and Single Core mode actually do.

**Processor Processing**[¶](https://dolphin-emu.org#processor-processing)

The following are the processors on the GameCube, and how Dolphin emulates them. The Wii does have some differences, but most of them are minor outside of the addition of the Starlet processor. For simplicity, we will be focusing on the GameCube throughout this section.

**Central Processing Unit**- A single PowerPC CPU core. The emulated software lives within this core, and Dolphin, for the most part, isn't aware of what's going on in here. To Dolphin, everything the emulated CPU is doing is just instructions.*A lot of instructions that go by very very fast.*Dolphin translates the instructions (via[recompilation or interpretation](https://dolphin-emu.org/blog/2024/09/04/dolphin-progress-report-release-2407-2409/#2407-103-cached-interpreter-20-by-mitaclaw)) into something the host CPU can understand, but for the most part it doesn't know what they are doing.*NOTE: Dual Core mode does not split the emulated CPU onto two host CPU cores. We can't do that.*

**Graphics Processing Unit****Command Processor**- A simple integrated circuit that sits between the CPU and the GPU. The CPU creates lists of commands for the GPU and throws them at the command processor, then carries on with its business. The command processor parses the command list and prepares the GPU to do the work, such as configuring the[TEV unit](https://dolphin-emu.org/blog/2014/03/15/pixel-processing-problems/)and setting up registers. Dolphin emulates the command processor, and assuming a hardware graphics backend is being used, it converts the GameCube GPU commands into commands for the selected graphics API (Vulkan, OpenGL, etc) then passes the work to the host's graphics driver.**Rendering Components (TEV/XF/EFB/etc)**- Continuing from above, once the host GPU driver has received commands it will convert those into the specific instructions and shaders that will actually run on the host GPU. This is still work for the host CPU, but it is done outside of Dolphin. The actual rendering, and thus most of the GPU emulation, happens on the host GPU (when using a hardware graphics backend).

**Digital Signal Processor**- A Macronix DSP that handles various audio processing duties. DSP-HLE is quite light since it technically emulates the*results*of the DSP and not the processor itself. DSP-LLE actually emulates this processor and it is quite heavy.



![Image showing the components of the GameCube](../../assets/63c1d480f85e7a99.avif)

Flipper dieshot from the

[Nintendo GameCube Architecture Presentation](https://cubemedia.ign.com/media/news/documents/embeddedforumkeynote.pdf).All of the processors above work **asynchronously** - each processor performs their work independently of all the others. To coordinate and prevent [race conditions](https://en.wikipedia.org/wiki/Race_condition), *synchronization points* must be used, communicating things like "VBlank just happened and we should start a new frame", or "there is work for you waiting in this memory region", or "the work I was assigned is now completed and I am waiting for more".

What is analogous to this in a modern PC? A multi-core processor. While cores may share some resources, they are more or less separate processors that operate asynchronously, and multithreaded applications need to synchronize across their threads. So of course, if a programmer wants to emulate a console with several processors running asynchronously, their *very first thought* would be to have separate threads for each emulated processor. This makes the host hardware behave like the original hardware, plus those threads can spread out across the many CPU cores of the host, better utilizing the host hardware and easing the emulator's CPU requirements. Makes perfect sense!

**That's Dual Core mode.** ﹡

Dual Core mode isn't a hack, because it closely mimics the original hardware!

**Dual Core, Dual Problems**[¶](https://dolphin-emu.org#dual-core-dual-problems)

But then, why is Dual Core so unstable? There are two reasons for that.

**Game Development is Hard**[¶](https://dolphin-emu.org#game-development-is-hard)

The GameCube does not have an operating system. While it does have SDKs and various Nintendo-provided assistance, ultimately, games run on the bare metal, and they have complete control over the system. They can do whatever they want.

And *the software* controls synchronization.

A game following best practices will set a synchronization point whenever there is potential for a race and will not ignore interrupts that the hardware sends back. If done correctly, the asynchronous processors cannot race at all. Games made by Nintendo's development teams, such as [Super Mario Galaxy](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Galaxy), are rock solid ﹡ in Dual Core mode because they safely and thoroughly synchronize.

But game development is hard, and "best practices" are an early casualty of crunch. All too often games run the hardware *a little loose.*

For example, a common occurance is that the game will have the CPU send work to the GPU before the game has completely scheduled all of the GPU's resources. If the CPU can return and fill out the rest of those resources before the command processor and GPU are finished with the work they were already assigned, this won't cause any problems. And since each GameCube should behave more or less identically to any other GameCube, if it is fine on the developer's GameCube, it should be fine on *any* GameCube.

However, this is a *race condition*, and coding like this is asking for trouble.

And unfortunately for us...

**Your Computer Is Not A GameCube**[¶](https://dolphin-emu.org#your-computer-is-not-a-gamecube)

In Dual Core mode, the emulated processors are spread across the host CPU cores, and Dolphin synchronizes *at least* as much as the original console. However, the time it takes for the host cores to do work could be **literally anything**. Modern CPUs adjust clockspeeds on a per-core basis and change their frequency all the time based on heuristics entirely outside of our control, the operating system will constantly move our threads around the host CPU and can decide to put one of our threads to sleep without warning, the CPU could be heterogeneous and another program competing for resources could convince the OS to elevate one of its threads to the big cores and kick one of our threads to the little cores, on and on and on. Race conditions are inherently unsafe on modern hardware!

Even Dolphin *itself* can unbalance the race. Normal emulation scenarios, like a big burst of shader compilation or the emulation threads stalling by saving state or saving a screenshot, are more than enough to change the victor of racing threads.

So if a game lets the chips race, the predictable and consistent race they were expecting on the original hardware is instead an *unpredictable* and *inconsistent* race in Dolphin. And if the race's outcome differs from the original hardware, the game and/or Dolphin may crash!

And despite our many attempts, there isn't really anything we can do about it. Assuming we behave like the original hardware, that is.

**The Solution: Don't Act Like A GameCube**[¶](https://dolphin-emu.org#the-solution-dont-act-like-a-gamecube)

In Single Core mode, Dolphin does not spread the emulated processors across the host's processors. Instead, it gathers all of those processors and emulates them in *a single host CPU thread*. This gives Dolphin full control over synchronization, allowing Dolphin to force work to be consumed at the same granularity as the original hardware. Even if a game runs a little too loose, even if the host OS gets up in our business, even if syncing with another instance of Dolphin on the other side of the world, Single Core can handle it.

This is not at all how the original hardware works, but the *result* is higher accuracy and stability. The only downside of course, is performance.

**Lessons Learned**[¶](https://dolphin-emu.org#lessons-learned)

This experience has given us a reminder that the developers who founded Dolphin *really knew their stuff*. Splitting the GameCube's processors across host CPU cores is inherently risky. The fact that Dual Core was stable enough to be Dolphin's default for *over fifteen years* is a testament to the capabilities of Dolphin's early developers. Dual Core mode is more or less as good as this implementation can get - as our repeated failures to improve it can attest.

And Dual Core mode was extremely influencial. After Dolphin went open source, *it could run some games at fullspeed*. It was extremely buggy, it required top tier hardware of the time, and it was not a lot of games, but Dolphin **could be used for play**. That was a possibility given to us by Dual Core mode, as Single Core wouldn't reach playable speeds on high end systems for another ten years or so. This was incredibly important in Dolphin's early days, as the ability to play attracted users, which attracted more developers, which attracted more users, giving Dolphin momentum to get off the ground after it went open source. Dolphin would not be where it is now without Dual Core mode.

That being said, times have changed. Our predecessors had to deal with Dual Core mode's instability to get playable performance, but, [as we covered earlier](https://dolphin-emu.org#2506-334-desktop-enable-single-core-by-default-by-joshuavandaele), we don't have to. Dual Core is no longer necessary for most of our desktop users, and should no longer be the default on desktop.

Then, what has changed now that we know all this? We will never call Dual Core mode a hack ever again.

**Aside: Why Not Just Synchronize More?**[¶](https://dolphin-emu.org#aside-why-not-just-synchronize-more)

That is what SyncGPU does. Specifically, in addition to all the synchronization points already in Dual Core, SyncGPU will only allow the processors to race a certain amount of emulated time before it forces a synchronization of its own.

In practice, SyncGPU was neither as fast as Dual Core nor as stable as Single Core, leaving it in a place where it simply didn't matter. But [you already saw the charts](https://dolphin-emu.org#2506-334-desktop-enable-single-core-by-default-by-joshuavandaele).