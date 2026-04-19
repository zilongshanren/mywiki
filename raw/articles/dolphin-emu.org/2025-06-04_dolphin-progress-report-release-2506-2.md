---
title: 'Dolphin Progress Report: Release 2506'
url: https://dolphin-emu.org/blog/7D/
author: OatmealDome
published: '2025-06-04'
source_blog: Dolphin Emulator - GameCube/Wii games on PC
source_site: https://dolphin-emu.org/
category: graphics
fetched: '2026-04-19'
---

Welcome to the Dolphin Progress Report for Release 2506! As we've alluded to a few times, we've had major changes in the pipeline that we've been very excited to show off. Some of those changes are *finally* here! Headlining this report are major adjustments to how Dolphin handled audio lag under slowdown by default. No longer will users have to choose between high-latency audio stretching or popping when dealing with small hitches in performance thanks to the new Granule Synthesis Audio System.

If the game is already running full speed, we still have some improvements for you. Dolphin has seen a suite of frame pacing improvements that will give you a smoother experience across almost every game. And, if your system is *very* powerful, there are a select group of games that can now push past the 60 FPS barrier for high frame rate gaming. Before you get *too* excited, this feature does not work with most Nintendo developed titles and has incredibly low compatibility in general. For a list of what games support this, we'll get into it later in the report.

If you care about preserving oddball Wii add-ons, we've got you covered here too. Wii Speak emulation is *finally* here after an incredibly long journey. In addition, long time incompatible game [The Daring Game For Girls](https://wiki.dolphin-emu.org/index.php?title=The_Daring_Game_for_Girls) is finally compatible with Dolphin. We'll get into that game's story and more, *but first*, we need to get through quite a bit of housekeeping.

#### The Release Hotfix Fiasco[¶](https://dolphin-emu.org#the-release-hotfix-fiasco)

We finally had some big enough problems in a release that we had to create a hotfix using our [new versioning system](https://dolphin-emu.org/blog/2024/07/02/dolphin-releases-announcement/#announcement). First, the macOS build for 2503 had the wrong version number attached, causing it to be incompatible with cross-platform NetPlay. We also found that GBA connectivity in compatible GameCube games was broken, and that there was a crashing bug when running Dolphin on older macOS versions. To rectify these problems, we created hotfix 2503a. However, in doing so, we *inadvertently* caused all development builds from that point on to take the "a" suffix. Some of our systems temporarily broke in the immediate aftermath while support for the suffix was hastily added. We technically could have removed the suffix, but we decided not to in the end because removing it would have caused even more disruption.

In future releases, if a hotfix is needed it will *not* apply a suffix to the development builds. This should make things easier on us and anyone else that is maintaining Dolphin builds of their own. We apologize for any inconvenience that this error has caused.

For reader convenience and future consistency, the hotfix suffix has been removed from all changes in this article.

[Although Windows 10 will reach End of Support later this year](https://www.microsoft.com/windows/end-of-support), it continued to receive major updates up until two and a half years ago. Thanks to that, we should be able to continue supporting the decade-old operating system for many more years. However, as new APIs, standards, and compiler features appear, our minimum Windows 10 version will slowly climb. As of [2503-152](https://dolphin-emu.org/download/dev/master/2503-152/), we are now taking advantage of time zone APIs that require Windows 10 version 1903, meaning that any older versions of Windows 10 are no longer supported.

The last Dolphin release to support Windows 10 versions 1703 to 1809 is [2503a](https://dolphin-emu.org/download/release/2503a/), and the last development build is [2503-148](https://dolphin-emu.org/download/dev/eb84b0fb9b3cd21400987a1c10c4a38d4861b9a9/).

We have also increased our minimum macOS version from macOS 10.15 Catalina to macOS 11 Big Sur. Unfortunately, Catalina lacks support for some C++20 APIs that we'd like to take advantage of, so we decided to go ahead and bump our minimum macOS version to accommodate those changes. This bump will also allow us to (finally) update the Qt in our macOS builds to 6.5 LTS, which we will aim to do before the next release.

The last Dolphin release to support macOS 10.15 Catalina is [2503a](https://dolphin-emu.org/download/release/2503a/), and the last development build is [2503-270](https://dolphin-emu.org/download/dev/afee9a56e96766d4622b1694398704e4c8d57b25/).

**Notable Changes**[¶](https://dolphin-emu.org#notable-changes)

When reporting performance issues, sometimes users don't even realize that the game is slowing down. They instead report *audio hitching* or *stuttering* as the main issue that's bothering them. In order to provide low latency audio, Dolphin employs a ring buffer. And, as long as the game is running full speed, this buffer remains full and you'll get a constant stream of audio.

When the emulator is not running at the target frame rate, the buffer won't be filled up. And when Dolphin runs out of audio in the buffer, there will be a small gap in audio that sounds rather unpleasant.

Click to Play. File has audio.

To combat this, Dolphin has given users the ability to enable *audio stretching*. At the cost of higher audio latency, Dolphin can stretch the existing data in the buffer to keep audio running smoothly. For many users, the increase in audio latency is large enough that this feature isn't worth the trouble.

** samb** wondered if there was a better way to handle things. While stuttering was annoying, he wanted a solution that improved the situation without the downsides of audio stretching. Enter the Granule Synthesis Audio System.



![](../../assets/cf2a53c07bfbc0d7.avif)



![](../../assets/cc214ac450f134c8.avif)

The actual idea of the system is rather simple. By breaking down audio granularly, piece by piece, we can get the opportunity to adjust samples just as they are being presented rather than having to hold them. If there is a gap in audio, Dolphin can see it in *real time* and stop the stutter from happening by repeating the last sample. For minor hitches and slowdowns, this almost completely hides audio oddities without increasing audio latency!

Click to Play. File has audio.

Obviously no solution will be perfect, but we believe that "Fill Gaps" provides a fairly high quality solution without the downsides provided by audio stretching. If for some reason you prefer the old behavior, you can disable the "Fill Gaps" option in the Options -> Configuration -> Audio tab in Dolphin.

Note that audio stretching is currently not implemented within the Granule Synthesis Audio System. For users that are experiencing consistent and heavy lag and used audio stretching, this may result in less than ideal audio in the short-term. However, ** samb** plans to add a full-fledged audio stretching system on top of Granule Synthesis to improve these edge cases in the future. Considering that most players are going to be attempting to play games at or near full speed, we decided that rather than delaying the feature, we'd rather merge it and add on to it later.

"Frame pacing" is a term used to describe the consistency at which frames are presented to your screen. This is an extreme example, but if you have a screen that refreshes every 16.6ms (60 Hz) and half of your frames present in 11.1 ms (90 FPS) and the other half present in 22.2 ms (45 FPS), you are in for an **extremely bad time** despite having an average frame rate of 60 FPS. It's not enough to simply run at 60 frames per second! The rendering and presentation of those frames needs to be consistent frame to frame and synchronize with your display for best results. We call that frame pacing.

Historically, Dolphin's frame pacing has been pretty good... when it was not [bogged down by Windows 7's terrible borderless window mode](https://dolphin-emu.org/blog/2014/07/31/dolphin-progress-report-july-2014/#40-2286-d3d-exclusive-fullscreen-by-armada651), or getting [screwed over by terrible graphics drivers](https://nb.dolphin-emu.org/blog/2018/12/04/dolphin-progress-report-november-2018/#dev-diary-putting-a-mac-through-its-paces-by-mayimilae), or if you were trying to run a 30 FPS title [before we implemented skip duplicate frames](https://dolphin-emu.org/blog/2020/02/07/dolphin-progress-report-dec-2019-and-jan-2020/#50-11524-improve-frame-pacing-by-manually-inserting-duplicate-frames-by-stenzek)... But those issues were solved, and Dolphin's frame pacing is now *good*! ...Right?

We thought we were doing a pretty good job, but after the merge of ** samb**'s

[FrameTime/VBlank Analyzer + Graph](https://dolphin-emu.org/blog/2023/02/12/dolphin-progress-report-december-2022-january-2023/#50-18086-new-frametimevblank-analyzer-graph-by-sam-belliveau), it was made apparent that there was still a lot of room for improvement.

The graph you see above shows two lines. "Frame", the orange line, is the time sampled immediately after the video backend pushes a frame. Ideally, this would perfectly match the amount of time the game has to render a frame. For NTSC, it should be 1001/60 ms (~16.67 ms) for a 60 FPS title and 1001/30 ms (~33.33 ms) for a 30 FPS title. The blue line is "V-Blank", which is measured at the end of each emulated video field - when the console would be pushing a frame to the screen. Ideally, this number should always be at the output rate of the emulated console. However, V-Blank is not necessarily tied directly to presentation because Dolphin has various hacks to display at different times.

All of the wiggles you see in the lines are **variance**, where either the Frame or V-Blank are missing their timing windows. The numerical statistics below the graph lists ±0.40 ms of variance for V-Blank and ±0.24 ms of variance for Frame. This results in uneven frame delivery to your screen, which appears as judder to the user.

With long obfuscated issues now in plain sight, work quickly began on improving Dolphin's frame pacing.

One of the initial things that ** samb** did after seeing these results was to throttle Dolphin more often. Throttling is essentially just a fancy way to keep the core running at the desired speed. By having Dolphin throttle 1200 times a second instead of 100, Dolphin would incidentally be more likely to throttle at a time useful for presenting frames.

** Billiard** took this concept and improved it with

[2503-54](https://dolphin-emu.org/download/dev/master/2503-54/). Instead of adding more throttling and potentially affecting performance, he removed almost all of the superfluous throttling and instead had Dolphin throttle for player input and frame presentation.

Despite these efforts, some games still had a consistent juddering. One such game was [Super Mario Sunshine](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Sunshine). After looking at it for a while, ** Billiard** realized that something strange was going on. For some reason, there were games that established different analog video timing parameters between the odd and even fields. In

[Super Mario Sunshine](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Sunshine)specifically, it gives the even field a slightly longer pre-blanking time and an equivalently shorter post blanking time. This is fine on console where output is drawn line by line. But because Dolphin was centering frame presentation based on pre-blanking time without taking into account post-blanking time, we were improperly pacing output in these titles.

[2503-56](https://dolphin-emu.org/download/dev/master/2503-56/)addresses this issue by accounting for both pre-blanking and post-blanking timings into frame presentation timings.

Finally, we have [2503-186](https://dolphin-emu.org/download/dev/master/2503-186/). This change added a high resolution timer to Dolphin on Windows, and made some other adjustments to *sleeps* on other OSes. The reason for the high resolution timer on Windows is because it was being problematic regardless of technique used and giving worse frame pacing than Linux. The timer change appears to bring it up to code with what we're expecting. The other OSes did not need this, but we were able to further improve frame pacing by adding ~1 ms of "busy waiting" to make sure we get control to present exactly when we want to instead of when the OS ends our sleep.

What was the result of all this work?

If you're sensitive to frame pacing issues, you'll notice the improvements immediately. Most of our testers reported immediate results across a variety of different titles. However, we can't guarantee every game will be perfect just yet. There's always the possibility that some titles have imperfect frame pacing even on console, or that they are doing something weird. For instance, [Alien Hominid](https://wiki.dolphin-emu.org/index.php?title=Alien_Hominid) runs at *thousands of frames per second on console!*

As a final note, *Immediately Present XFB copies* will always try to present the frame as soon as it is done to reduce input latency, which reduces the impact of these frame pacing improvements.

Anisotropic filtering is a texture filtering technique that improves the quality of textures at oblique angles. It is very memory bandwidth intensive, making high levels of anisotropic filtering still uncommon even on consoles today. When gaming on a PC, it's common to just crank it to the max and forget about it. Naturally, Dolphin has offered anisotropic filtering as an enhancement from nearly the beginning.



![](../../assets/613f31b67e8962c4.avif)



![](../../assets/734debdd3e69044d.avif)

You may not know this, but the GameCube and Wii *actually support anisotropic filtering.* It is fairly uncommon across the library due to it being **exceedingly** expensive performance-wise, but it is still a feature that these consoles support. However, rather than applying it to every texture, developers would instead apply anisotropic filtering to specific textures as needed - usually repeated textures on large floors or walls.

However, Dolphin's anisotropic filtering enhancement *is not* emulation of the consoles' anisotropic filtering. In fact, Dolphin completely ignored all anisotropic filtering requests from the game entirely! Dolphin's enhancement was everything or nothing, and there was no way to *only* enable anisotropic filtering just for the textures that would have used it on console. As such, it was impossible to get console-matching texture output - without the enhancement some textures would be too soft, and with the enhancement some textures would be too sharp. It was never quite right.

This has now changed! If Dolphin's texture filtering is set to Default and a game requests anisotropic filtering, Dolphin will now listen to the game's request and apply the specific anisotropic filtering it asked for.



![](../../assets/f5ccf6e6484a6cd0.avif)

[Pokémon Colosseum](https://wiki.dolphin-emu.org/index.php?title=Pok%C3%A9mon_Colosseum)loses all definition in the distance.



![](../../assets/eaac1c28ddc58a90.avif)



![](../../assets/47b235533330948e.avif)

[F-Zero GX](https://wiki.dolphin-emu.org/index.php?title=F-Zero_GX)are weirdly bright and distracting without anisotropic filtering, and the line on the track disappears the further it gets from the camera.



![](../../assets/8ed22a891b4eade9.avif)

Existing texture filtering configurations are not affected by this change. If you had 16x set previously, Dolphin will still use 16x anisotropic filtering on all textures.

The 7th generation of video game consoles was a wild time for official USB controllers. Before or since, we have never had more a varied selection of official shaped plastic input devices! Amusingly, PlayStation 3 and Wii-branded devices were usually cross-compatible between the consoles. However, Xbox 360 devices tended to work differently and were usually *not* compatible. But, if you were someone who played Skylanders on the PlayStation 3 and had a Portal of Power from a PlayStation 3 bundle, you could use that on a Wii without any issues.

Sadly, this wasn't always the case. The Rock Band PlayStation 3 and Wii controllers identify themselves with different device IDs, despite being nearly the same internally. And that's unfortunate, because the different IDs are the only thing that stops a PlayStation 3 Rock Band controller from working on a Wii, and vice versa.

Now, you might be asking, *what if you just tricked the game into thinking that the Wii controller was connected*? Well, that's exactly what ** JosJuice** implemented. When a game tries to identify a connected PlayStation 3 Rock Band controller, Dolphin will now tell it that the equivalent Wii controller is connected instead, allowing it to work.

If this is a behaviour that you do not want, it can be disabled via the option `DisguisePlayStationAsWii`

in the `Dolphin.ini`

configuration file.

Games can become notable for many reasons. There are those that have legendary difficulty, incredible stories, or amazing multiplayer, among other traits that make them desirable. Others are notorious, due to being rushed, broken, or downright bad and boring.

In the Dolphin community, sometimes games become famous (or infamous) due to how they behave in the emulator. [Star Wars: Rogue Squadron III](https://wiki.dolphin-emu.org/index.php?title=Star_Wars_Rogue_Squadron_III:_Rebel_Strike) is legendary as a game that's nearly impossible to emulate. [True Crime: New York City (GC)](https://dolphin-emu.org/blog/2021/11/13/dolphin-progress-report-september-and-october-2021/#50-15330-raise-program-exceptions-on-floating-point-exceptions-by-josjuice) is infamous because of how many issues it has, even on console.

And then there's [The Daring Game for Girls](https://wiki.dolphin-emu.org/index.php?title=The_Daring_Game_for_Girls). Widely regarded as ordinary Wii shovelware, it has become notorious simply because it didn't boot in Dolphin. And with the list of incompatible games dwindling every year, the fact this game in particular was *still* broken just made it more interesting to people.

When it became the only *reported* title to not boot on Dolphin's compatibility list, a crosshair was placed upon it. And *finally*, someone took a look at fixing [The Daring Game for Girls](https://wiki.dolphin-emu.org/index.php?title=The_Daring_Game_for_Girls). If you're expecting some grand investigative adventure with twists and turns, sorry to disappoint you. The reason this game didn't work was actually very similar to several other games fixed in the last two years. The game's audio engine has [a latent race condition bug that was exposed by Dolphin's poor timings](https://bugs.dolphin-emu.org/issues/10821#note-4). Thanks to debugging work by ** hthh**, a

[veteran of debugging weird game behaviors](https://dolphin-emu.org/blog/2020/10/05/dolphin-progress-report-july-and-august-2020/#fix-mvp-baseball-2004-and-mvp-baseball-2005-flickering-graphics), all

**had to do was patch the game bug.**

[flacs](https://github.com/tilka)So now a game that was *mostly notorious* for not working in Dolphin was finally working. Its legacy was gone. And while we booted the game on console in the past for testing, no one put any serious play time on it and just blew it off as Wii shovelware. This time, we put significant hours into [The Daring Game for Girls](https://wiki.dolphin-emu.org/index.php?title=The_Daring_Game_for_Girls) to make sure that it was working properly. And while it starts out like a typical crappy Wii motion-controlled minigame collection, something deeper lurked within...

![](../../assets/ff5e460d7d8cc00c.avif)

The game has a *horrible* first impression. The first two minigames you play are a *quiz* and a *slide puzzle*. At this point, our guard was down and we thought we were dealing with a standard crappy Wii game. But those minigames *weren't the point of the game*. In fact, they simply distract you from the main gameplay loop that takes place in the overworld.

The idea is that you're surrounded by a myriad of customers that want things. By following the news on local trends, you can operate your business on the side of the road. For instance, you can set up a small *garden* and grow *flowers* to sell to people. If they like your flowers, they're certain to buy from you again. If you're strapped for cash, you can also serve *lemonade*, which is a cheap and simple product to get your business back into the green.

The gameplay works best if you keep yourself to a [ schedule, 1](https://store.steampowered.com/app/3164500/Schedule_I/) task at a time. Obtain materials to create products to sell to people to make a bigger profit. Once you have enough money, you can buy yourself transportation in the form of a scooter. But if you just need to relax, there's a local basketball court where you can shoot hoops. But always remember to do things aboveboard, as breaking local ordinances could result in trouble. Don't scoot without a helmet!

[The Daring Game for Girls](https://wiki.dolphin-emu.org/index.php?title=The_Daring_Game_for_Girls) is no masterpiece by any means. To beat the game, you do have to deal with some truly uninspired and awful minigames. But if you're a trash connoisseur that can weather that storm, the game's weirdness can be charming. You'll be going along, obtaining power tools, collecting elements from the periodic table, and making lemonade, only to be sidetracked by a surprisingly in-depth *scooter building* minigame that puts [American Chopper 2](https://wiki.dolphin-emu.org/index.php?title=American_Chopper_2:_Full_Throttle) to shame.

In the end, after playing [The Daring Game for Girls](https://wiki.dolphin-emu.org/index.php?title=The_Daring_Game_for_Girls) for longer than any human should... we came to a horrifying conclusion. The game *isn't* the worst thing in the world. Is it empowering for girls? Sometimes, maybe. Does it come off as patronizing toward the target audience? A lot of the time, yes. But is it devoid of any entertainment? In our opinion, it's a weird enough game that it actually manages to escape the doldrums of being an *awful* shovelware game.

If you happen to encounter [The Daring Game for Girls](https://wiki.dolphin-emu.org/index.php?title=The_Daring_Game_for_Girls) in a garage/boot/yard sale or thrift store, it is well worth a look.

[In our last release](https://dolphin-emu.org/blog/2025/03/10/dolphin-progress-report-release-2503/#2412-305-track-time-played-core-and-qt-by-aminoa), Dolphin gained the ability to display a "Time Played" value in the game list that accurately reflects how long you've played each game. Unfortunately, Android didn't get this feature... sort of. After the initial pull request was merged, Dolphin began recording play time on Android, but there was no way to actually *see it* in the Android UI.

Thankfully, ** JosJuice** came to the rescue of our Android users and added a way to see the time played.

Emulators can allow players to experience their games in brand new ways. With higher resolution, high resolution texture packs, different controllers, and even playing local games online using netplay, emulators can push way beyond the limitations of the original hardware.

Hacks that increase frame rate are one type of enhancement that has been sweeping through the emulation community. Over the years, many popular games have been taken from their native 25/30 FPS target to 50/60 FPS via cheat codes and patches. However, in Dolphin, pushing them *further beyond* that has largely been impossible.

The GameCube and Wii were designed for analog televisions. The primary way these consoles keep track of the start or end of a frame is the *Vertical Blank Interrupt (VBI)* - an interrupt synchronized to the *vertical blanking interval* of analog displays. Most games for the GameCube and Wii listen for the VBI and either make a frame every VBI (to output 50/60 FPS) or every other VBI (to output 25/30 FPS). Getting a game to update at every VBI instead of every other VBI is fairly straightforward, but going beyond 60 FPS would require *detaching from how the consoles think of frames*. Rejecting their reality and substituting our own is **much** more difficult.

[samb](https://github.com/Sam-Belliveau), our favourite chaotic tinkerer, enjoys playing with these limitations. While they were experimenting with the [VBI Skip hack](https://dolphin-emu.org/blog/2023/02/12/dolphin-progress-report-december-2022-january-2023/#50-18271-video-hack-vbi-skip-by-sam-belliveau), which allowed games to run at *lower* frame rates, they had a rather terrible thought. What if instead of removing VBIs, they *added some*? If it was possible to make a game skip frames, would it be possible to make them add *more* through this method?

At a glance, it seemed like the answer was... kinda. The games they experimented with did output more frames, but their gameplay was also sped up. After all, the modern idea of "[delta time](https://booth.dev/tutorial/unity/what-is-delta-time)", where a game's physics are calculated independently of frame rate, wasn't standardized or even common back in the GameCube/Wii era.

[samb](https://github.com/Sam-Belliveau) was disappointed by these initial results and moved on to other shenanigans. However, the original pull request was never closed and left open for others to experiment with. After finding promising results with it, ** SuperSamus** took up the maintenance mantle and rebased it on the latest builds of Dolphin. They thought that perhaps we overlooked this feature too quickly and sought to prove that the feature should be included in Dolphin.

By combining the hack with game patches, ** SuperSamus** created incredible demonstrations that showed what was truly possible. Compatibility was still low, but the games supported became numerous enough that the potential couldn't be ignored.

To clarify things: many major titles like [Super Mario Galaxy](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Galaxy) and [Wind Waker](https://wiki.dolphin-emu.org/index.php?title=The_Legend_of_Zelda:_The_Wind_Waker) do not respond well to this hack. Their physics are programmed to function at one specific frame rate, and they don't have any variable that controls how much things move every frame. They are the worst candidates for ever supporting this hack.

But some games are the complete opposite. [Super Mario Strikers](https://wiki.dolphin-emu.org/index.php?title=Super_Mario_Strikers) and [Mario Strikers Charged](https://wiki.dolphin-emu.org/index.php?title=Mario_Strikers_Charged) don't even require patches, and will run at whatever frame rate you suggest without affecting gameplay speed!

*smearing*of the lines on the floor. 120 Hz is clearer and smoother. For more examples of stairsteppy motion, watch the movement of the ball or the 1 as the koopa rotates.


This is a 120 FPS clip. A display that supports a refresh rate of 120 Hz or higher is required to see it as intended.

This is a 120 FPS clip. A display that supports a refresh rate of 120 Hz or higher is required to see it as intended.

We can't stress enough that games which maintain the same speed regardless of VBI frequency are the exception, not the rule. However, there are some cases where you might want a game to speed up or slow down. That's because VBI Frequency Override *does not* affect audio, meaning that it if a game doesn't require technical gameplay, you can greatly speed it up without distorting sound effects or music. However, you should note that VBI Frequency Override comes with the same risks as increasing the Emulated CPU Clock (in fact, it will automatically modify it to match the VBI frequency), and may cause hangs in games that are sensitive to CPU timings.

[We've crafted a list of games that are known to respond to VBI Frequency Override.](https://wiki.dolphin-emu.org/index.php?title=Category:Supports_VBI_Frequency_Override) **A game being on this list does not mean that it is stable when adding VBIs!** It only means that these games calculate game physics using delta time. Other games do have a variable that controls game speed, but won't adjust it dynamically, meaning that it must be manually changed through a patch. Finding these games can take much experimentation, so even if a game isn't in the list, it may still be possible to make a patch for it. There are also games that arbitrarily limit the frame rate, and others that arbitrarily clamp their delta time to a certain range. Since it's very easy to control when these behaviors are in action, [Branch Watch](https://dolphin-emu.org/blog/2024/12/02/dolphin-progress-report-release-2412/#50-21724-branch-watch-tool-add-set-breakpoints-submenu-and-2409-15-branch-watch-tool-refactors-fixes-and-features-by-mitaclaw) is an incredibly useful tool for finding and patching these functions.

Even in games that use delta time, there can still be cases where developers tie something to the frame rate. For example, in [Digimon World 4](https://wiki.dolphin-emu.org/index.php?title=Digimon_World_4), certain special moves require you to spin the stick. As you increase the frame rate, the timing window for spinning the stick becomes smaller and smaller, making it more difficult to do the special move. In [XGIII: Extreme Racing](https://wiki.dolphin-emu.org/index.php?title=XG3:_Extreme_G_Racing), the actual racing uses delta time, but certain animated textures are hardcoded to advance per frame. In [Scooby Doo! Night of 100 Frights](https://wiki.dolphin-emu.org/index.php?title=Scooby-Doo!_Night_of_100_Frights), swinging on ropes will cover less distance at high frame rates.

If it isn't clear by now, don't use this feature if you're doing your first playthrough of a game, even if it is [on our list.](https://wiki.dolphin-emu.org/index.php?title=Category:Supports_VBI_Frequency_Override) We can't promise stability, we can't promise compatibility, and we can't promise that your device is fast enough to handle the feature.

But, as fans, experiencing some of these games at high frame rates is an interesting enough novelty that we want to give those interested a chance to try it themselves. We're hopeful that games which *almost* work properly can be modded and adjusted to work on a more complete level with cheat codes or patches. ** SuperSamus** has already patched several games to be more playable. One such game,

[Need For Speed: Nitro](https://wiki.dolphin-emu.org/index.php?title=Need_for_Speed:_Nitro), works pretty much perfectly in our experience, but requires incredibly high-end hardware to push to 120 FPS or higher.

As an aside, special mention has to go to Next Level Games, as [Mario Strikers Charged](https://wiki.dolphin-emu.org/index.php?title=Mario_Strikers_Charged) even *syncs up in online matches* between Dolphin instances running at different frame rates. For example, A 60 FPS player can play with a 144 FPS player without major issues. Both of the Mario Strikers games seem to work at pretty much any frame rate without any serious issues, so kudos to them.

And because the world is a very strange place, the newly supported [The Daring Game for Girls](https://wiki.dolphin-emu.org/index.php?title=The_Daring_Game_for_Girls) works with this feature as well. Joy.

![](../../assets/51662874b646dd41.avif)

Nintendo's Wii Speak was probably meant for bigger things. But every so often, one of Nintendo's accessories flops, and when they flop, they often *flop hard*. Out of the entire Wii library, the only software to outright require it is the [Wii Speak Channel](https://wiki.dolphin-emu.org/index.php?title=Wii_Speak_Channel), which is self explanatory, and [only fifteen games](https://wiki.dolphin-emu.org/index.php?title=Category:Wii_Speak_(Input_supported)) (to our knowledge) utilized it as an optional accessory.

Perhaps the most notorious usage of the Wii Speak games were the Wii versions of [Wheel of Fortune](https://wiki.dolphin-emu.org/index.php?title=Wheel_of_Fortune) and [Jeopardy!](https://wiki.dolphin-emu.org/index.php?title=Jeopardy!), which used it for voice recognition. In 2010. Completely offline. *On a console with hardware from 2001.* Anyone who had these games will remember it hearing the wrong answer when you had the right answer, giving you the right answer when you had the wrong answer, and outright ignoring what you said. It's like [Hey You, Pikachu!](https://en.wikipedia.org/wiki/Hey_You_Pikachu), but with thousands of imaginary dollars on the line!

Using Wii Speak exclusive features has been possible in Dolphin for many years, but real Wii Speak hardware was required. But now, thanks to work that bounced between four developers for over a decade, you can enjoy the Wii Speak experience with a standard microphone on your PC.

You're welcome.

On desktop you can find this feature under `Tools > Emulated USB devices > Wii Speak`

. On Android, it's located under `Settings > Config > Wii > Emulated USB Devices`

, and you'll need to give Dolphin permission to use the microphone.

**This Release's Contributors...**[¶](https://dolphin-emu.org#this-releases-contributors)

Special thanks to [all of the contributors](https://github.com/dolphin-emu/dolphin/graphs/contributors?from=2025-03-01&to=2025-06-01&type=c) that incremented Dolphin by 610 commits after Release 2503!

**Dolphin vs. Aggressive AI Scraper Bots**[¶](https://dolphin-emu.org#dolphin-vs-aggressive-ai-scraper-bots)

We've recently observed a large increase in the amount of traffic on our websites, sometimes even reaching a point where the websites would become overwhelmed and crash. Many important services like the downloads and updates system, NetPlay, and Wii System Menu Updates rely on our websites to function correctly, so any outages have a direct impact on many Dolphin users. At one point, we even got an e-mail from our hosting provider asking that we reduce our excessive server load, as it was starting to cause problems for their other customers' websites!

When we investigated what was going on, we found that scraper bots owned by AI companies were making up a significant portion of the requests sent to our websites. Text written by humans is very valuable to companies creating [large language models](https://en.wikipedia.org/wiki/Large_language_model) (LLMs). In order to create text datasets for training their models, these companies have deployed [scraper bots](https://en.wikipedia.org/wiki/Web_scraping) to download all the text they can find from the Internet. These bots request a page, copy all of its text into their dataset, and then repeat the process with all of the links found on that page. They can even make requests from multiple IP addresses simultaneously. We were effectively being [DDoSed](https://en.wikipedia.org/wiki/Denial-of-service_attack) by scrapers!

Thankfully, scrapers run by the major AI companies are generally well-behaved and comply with the [Robots Exclusion Protocol](https://en.wikipedia.org/wiki/Robots.txt). This means that we can provide files called `robots.txt`

that specifies which bots are allowed or not allowed to access our websites. We went ahead and created a blocklist based on [ai.robots.txt](https://github.com/ai-robots-txt/ai.robots.txt), an open list of bots that are run by AI companies.

Unfortunately, even after blocking these bots, some sites like our wiki were still occasionally crashing. After looking closer at our server logs, we noticed something suspicious. Why were we getting hundreds of requests from computers claiming to run **Windows 95**!?

![](../../assets/b2bf8953da6ab4df.png)

*16 years*after Windows 95. Needless to say, it does not support that operating system.

There was apparently another type of AI scraper bot plaguing our wiki. These bots did not care about being good Internet citizens. They ignored the Robots Exclusion Protocol, and instead pretended to be browsers when identifying themselves to our server. They constantly switched between mimicking modern browsers, outdated browsers, and browsers that do not exist at all (like Internet Explorer 9 on Windows 95, or Google Chrome on a PowerPC Mac). Worst of all, they often made requests for pages that take a decent amount of work for the server to render, like revision history pages. While we're not sure exactly who is operating these bots, their request patterns did suggest that they were trying to download the text off of every possible page on our wiki.

In order to prevent this traffic from continuing to cause outages, we've deployed [Anubis](https://anubis.techaro.lol/). When you first visit the wiki, your browser will now be checked by Anubis to ensure that it is a legitimate browser and not a bot. This should only take a few seconds, though it may take a bit more time on older devices. Once your browser has been verified, you will be redirected to the page that you were looking for. Checks should only occur approximately once a week, assuming you have cookies enabled.

Upon deploying Anubis, we immediately observed a drop in traffic hitting the wiki, and that it was loading much faster than before! We found that Anubis worked so well that, after seeing these results, we deployed it on our [bug tracker](https://bugs.dolphin-emu.org) and on [FifoCI](https://fifo.ci) as well.

Anubis is built around the concept of ["proof-of-work"](https://en.wikipedia.org/wiki/Proof_of_work), where each request is validated by having the client solve a problem (a "challenge") that is hard to compute, but easy for the server to verify. The idea is to make it more difficult for bots to send out automated requests en masse, as now they need to expend additional time and computing power to solve challenges. In Anubis's implementation of proof-of-work, each challenge involves [having the browser find a SHA-256 hash that starts with a specific number of zeros](https://anubis.techaro.lol/docs/design/why-proof-of-work).

While Anubis works really well, there are still some limitations. The biggest limitation right now is that JavaScript must be enabled to pass challenges. If you have JavaScript disabled, you'll need to enable it to be able to access some of our sites. [This may be resolved in a future version of Anubis.](https://anubis.techaro.lol/docs/user/frequently-asked-questions#why-cant-you-just-put-details-about-the-proof-of-work-challenge-into-the-challenge-page-so-i-dont-need-to-run-javascript) There may also be [some problems when attempting to access Anubis-protected sites on a dual-stack Internet connection](https://github.com/TecharoHQ/anubis/issues/564) (one that supports both IPv4 and IPv6). If you see an "Invalid response" error, try clicking the "Go home" link and see if the Anubis check passes there.

[We're not alone with this scraping problem.](https://arstechnica.com/ai/2025/03/devs-say-ai-crawlers-dominate-traffic-forcing-blocks-on-entire-countries/) Several major open-source organizations like [the Linux kernel](https://social.kernel.org/notice/AsgziNL6zgmdbta3lY), [Sourcehut](https://status.sr.ht/issues/2025-03-17-git.sr.ht-llms/), and [ScummVM](https://fabulous.systems/posts/2025/05/anubis-saved-our-websites-from-a-ddos-attack/) have recently spoken about AI scrapers causing excessive server load, and many have already chosen to use Anubis to block these requests. [Even the United Nations has decided to deploy Anubis.](https://xeiaso.net/notes/2025/anubis-works/)

It's a shame that we have make life a little more annoying for our users when protecting our servers, but unfortunately this is the reality of the modern Internet.