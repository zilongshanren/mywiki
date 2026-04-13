---
title: iOS & Android game development on Windows
url: https://gamedevcoder.wordpress.com/2012/02/01/ios-and-android-game-development-on-windows/
published: '2012-02-01'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

UPDATE: [Read here](https://gamedevcoder.wordpress.com/2012/05/14/monstaaa-for-ios-the-first-announcement/) about my second game Monstaaa! made on Windows using Marmalade SDK.

When I started indie game development 6 months ago (see my previous post [Good bye Blue Tongue (and time for indie game development)](https://gamedevcoder.wordpress.com/2011/08/13/good-bye-blue-tongue-and-time-for-indie-game-development)) I knew I wanted to experiment with games for iOS and Android. I knew nothing about mobile development at that time but I was kind of hoping there would be ways to develop my apps cross-platform (iOS, Android and possibly other platforms as well). And I wasn’t very keen to invest into a Mac just so I could develop for iOS. That’s when I started my investigation of available solutions.

In this post I’m going to give you a quick run down of my findings when it comes to available software / SDKs for cross-platform mobile development (mostly iOS and Android) under Windows. As part of that I’m also going to compare 3 different SDKs: [DragonFire SDK](http://www.dragonfiresdk.com/), [Marmalade SDK](http://www.madewithmarmalade.com) and [Unity3D](http://www.unity3d.com).

**DragonFire SDK**

The first thing I came across while searching for ways to develop for iOS from Windows was [DragonFire SDK](http://www.dragonfiresdk.com/). It’s iOS only but it’s cheap. You develop on windows under Visual Studio and test in their simulator. And if you want to test it on the iPhone or iPad you send them (via their website) your full source code and game assets (images, sound and all other data files) and they send you back compiled binary. What I initially liked about DragonFire SDK was that it had extremely simple C-style API – just one header file with a hundred or so functions for graphics, input, files, audio etc. Everything looked pretty [straightforward](http://www.dragonfiresdk.net/help/DragonFireSDKHelp.html).

I purchased the cheapest, $50 iPhone only, license and started experimenting. I set myself a goal of making simple [sokoban](http://en.wikipedia.org/wiki/Sokoban) game as quickly as possible, just so I could test that the SDK really does the job. The game was ready in about 5 days and run very well in the simulator. There were few problems and some bugs with rendering that I had to make workarounds for but finally all worked. Now I wanted to test it on my iPad and that’s where the problems started piling up (or become more obvious).

Firstly, it turned out that the whole source code has to fit in a single CPP file. Wow. Being curious what other people do I searched their forums and found [community project](http://www.whitetreegames.com/tools/manifest-builder) that merges all CPP and H files into single CPP. Worked for me. Checked.

I paid another $50 for “ultimate iPhone” license meaning I could now test the game on the device. I packaged my build and sent to DragonFire, so they would compile the project for me. A day later I got my .app (iOS application) file and tried to install it on my device. No luck. The build wouldn’t install complaining about some incompatible configuration. I could investigate more, send question to DragonFire support or ask on the forums but there were also few other problems and all that together already made me quite uncomfortable about using DragonFire SDK. That’s when I slowly started looking around in search for other solutions out there…

In the end I haven’t even gotten to the point of getting my game to run on the iPad via DragonFire SDK. I quickly realized DragonFire SDK was not the right choice for me, and it wasn’t so for just one reason. Below my quick summary of mentioned SDK:

Cons (cons first because more important):

- extremely limited API (e.g. can only draw rectangles, no polygons; no support for “fancy” stuff like iOS GameCenter)
- buggy rendering code (at least in the simulator)
- all apps are fixed to 30 frames per second
- the whole source code has to be in a single CPP file
- assets once loaded stay in memory forever (sure, why would you ever want to free up some memory?)
- can’t make iOS build on Windows + terrible turnaround times (need to send them your source code + assets, then wait for reply; took 1 day in my case)
- terribly slow PC simulator (couldn’t even get 30 fps for my sokoban game; and I do have reasonably fast laptop)
- iOS only
- no debugging on the device (this one is pretty obvious but just wanted to make things clear)

Pros:

- cheap ($100 for iPhone or iPad license; $150 for both)
- compiles to native
[ARM](http://en.wikipedia.org/wiki/ARM_architecture)code (meaning no emulation -> fast) - extremely simple API
- can develop on PC under Visual Studio
- can submit to Apple Store without Mac

My final word is: even if you’re not serious about iOS development, you better stay away from it.

**Marmalade SDK**

The next thing I started looking at was [Marmalade SDK](http://www.madewithmarmalade.com). They had completely free 90 day trial, their API seemed way more complete than the one from DragonFire SDK yet simple and very clean. And they seemed to have pretty large and lively community. Also, knowing that games such as [To-Fu](http://toucharcade.com/2011/05/24/to-fu-the-trials-of-chi/) (one of my favorites on the Apple Store) have been made using Marmalade SDK was very encouraging.

The next day my game was already running in the Marmalade simulator on Windows. And after one more day it was running on my iPad too. One great thing about Marmalade building process is that you don’t need Mac to make iOS build, you can do it right on your PC (Windows), locally. They do however also support building from Mac.

Few more days and I also had my game running on Android and Blackberry PlayBook. Since Marmalade is based on C++, it does support wide range of devices including ones supporting [ARM](http://en.wikipedia.org/wiki/ARM_architecture) (e.g. iOS, Android), [MIPS](http://en.wikipedia.org/wiki/MIPS_architecture) (e.g. LG Smart TV) and [X86](http://en.wikipedia.org/wiki/X86) (e.g. Windows) architectures. Depending on the target architecture they just use different C++ compilers. The good thing about this is that the code you write runs natively on the device which means it’s as fast as possible.

I still plan to make a short post-mortem of the development of my game in a separate post, so I won’t go into too much detail here but I wanted to say that Marmalade was really a great choice for me. And the proof for that was that my sokoban game has been successfully released on iOS, Android and Blackberry PlayBook (check out [Puzzled Rabbit](http://puzzledrabbit.pixelelephant.com)).

Now, here’s my full summary of Marmalade SDK:

Pros:

- still pretty cheap: standard license (without Marmalade logo at startup) is $500 which gives you access to all SDK features
- great (mostly) C style API: simple, clean & flexible (e.g. if you want, you can use OpenGL ES directly; or, if you prefer, you can use their higher level IwGx rendering API)
- powerful: built-in support for so many different things (e.g. Game Center, camera, photo gallery, HTTP)
- compiles to native ARM / MIPS / X86 code (meaning no emulation -> fast)
- supports mixing with native code (e.g. Objective-C on iOS or Java on Android) to create custom extensions that do whatever you want
- great open-source community projects: lots of goodness there including ports of very many popular C/C++ libraries (see full list
[here](https://github.com/marmalade)) - can develop on PC under Visual Studio or on Mac under XCode
- can build iOS apps on Windows
- very good PC/Mac simulator
- support for native iOS builds on Mac (so, it’s possible to debug the code!)
- support for many platforms (including iOS, Android and less popular ones such as Blackberry PlayBook, Bada, WebOS or Symbian)
- support for asset pipelines: fonts, compressed textures, materials, models, animations

Cons:

- occasional bugs in the SDK (fortunately they do try to help you via support or forums – though sometimes it does takes a while)
- some issues haven’t been fixed for surprisingly long periods of time, e.g. correct splashscreen handling on various devices has been broken for months!
- not all new features get added quickly (for example iCloud support isn’t good at the time of writing this, e.g. has no support for conflict resolution)
- can’t submit to Apple Store without Mac (not a big deal though; took 5 mins on my friend’s Mac)

My final word is: Marmalade SDK is truly great piece of software. It is very well designed and it does the job even though it has some (minor) issues.

I should also mention that for the last 5 months I’ve been developing my next, much larger and more sophisticated Marmalade based, game for iOS and Android and it’s been going really great. I was able to integrate lots of (3rd party) libraries and technologies including Game Center, Open Feint, Facebook, [Box2D](http://box2d.org), camera, photo gallery or [jpeglib](http://code.google.com/p/jpeglib). I wasn’t able to add support for iCloud yet because of limited support for that in Marmalade but thanks to support for native extensions I still plan to implement it (though, yes, I’ll need a Mac/XCode for that).

**Unity 3D**

I have no experience with [Unity3D](http://unity3d.com), so I can’t say too much here. It definitely seems to be a solid piece of software and there’s been tons of projects released on iOS and Android that were using it which is a good thing. In fact 90% of my indie dev friends are using it, so I do very often get a chance to learn about it from what they tell me.

But there’s few things which, when compared to Marmalade, I didn’t really like. These also were my reasons for choosing Marmalade rather than Unity3D:

- emulation from (managed) C# via
[mono](http://www.mono-project.com)(meaning higher memory usage and worse performance; also garbage collection seems to be causing performance issues / frame rate spikes for some developers) - more expensive: license for iOS and Android without Unity3D logo at startup costs $2300 ($1500 for Unity Pro + $400 for iOS + $400 for Android); more advanced features cost you additional $1500-$400 for iOS and $1500-$400 for Android
- additional functionality (via plugins) might cost you another couple $$$ (e.g. audio recording, Game Center, GPS – see
[here](http://prime31.com/unity/)) - high level & complex object oriented code you have to deal with
- need to have Mac to deploy to iOS device

The only advantage of Unity3D over Marmalade that I know of is that it has nice 3D scene editors and other tools. Depending on what kind of game you’re making this might be a bonus.

If I missed something important while comparing Marmalade with Unity3D then simply let me know and I’ll try to fix that.

Now going back to finishing up my upcoming, still unannounced, game. Expect some news about it really soon!

nice article. hands up for marmalade ! i need to add some cons for marmalade;

* some part of documentation is poor

* some part of IwUI components are great but some part is buggy/not well documented/lacking

* forum respond is not that fast, if you hit to something, you need to spend lot of time to solve it

despite everything my favorite cross platform SDK is marmalade…

Thanks for your neat explanation. Theses comparisons are really useful.

You CAN do on-device debugging on iOS devices using Marmalade… you need to do this from a Mac/Xcode. There is an MKB option (–iphone I think) which builds your Xcode project in a form whereby on-device debugging is possible.

Wow, that is great. Just updated my post.

Thanks Nick!

Hi all,

good article

When I started the development of mobile apps I have also tested different solutions. I came to the conclusion to use Marmalade SDK.

Benefits include:

* 2D and 3D supported (import / export Maya & Max)

* Some libraries have been integrated (e.g. Box2D, AdMob)

* Some “Big” games have been ported using the SDK (e.g. PES, NFS) -> this means that its support will be provided (you can count on it)

But you still need a Mac to upload your game to the AppStore …

My game is in development: you can see it here: http://bitblitgames.wordpress.com/scubadiver/

Sylvain

Great comparison article. I too started on a similar path to yours, but luckily I went Unty3D then Marmalade. I initially started working on my own cross platform solution but quickly discovered that it was going to take a long time so gave up.

Unity3D is good, the editor is fantastic and I love coding in C#, but the overheads and limitations are too much for serious game development. For example, we deployed a very simple 2D pong style game with Unity and the executable was over 10MB. The same game with double the amount of content deployed for less than half that size with Marmalade.

The perfect combination would be Unity3D’s editor with Marmalades base engine. This is something that we are working our IwGame Engine towards (http://www.drmop.com/index.php/iwgame-engine/). We created an XML style layout language called XOML, we plan to create a game editor that can export to the XOML format to allow production of games and interactive content using mark-up and very little coding.

@Mat I had a quick look at IwGame once and it looked really nice even though it seemed there was still lots of work before you guys could compete with what Unity3D offers when it comes to scene editing. Having said that, there’s already some nice functionality in IwGame. Good luck with that.

I used Unity3d free version with Android plug-ins for developing my first android game using 3d graphics

I published it in Android market. The game name is Dino Picker

Link: https://market.android.com/details?id=com.Voicegateindia.DinoPicker

Unity is pretty good game engine with lots of in-built features and effects

I think for less complex games free version is fine

Great post. It’s hard to find any unbiased opinions about game engines. Anyways, it sounds like DragonFire is one to avoid.

Hey,

I have 2 questions:

– did you use iwgame-engine (http://www.drmop.com/index.php/iwgame-engine/) in Puzzled rabbit or just pure Marmalade SDK with some additional libs?

– Was it hard to develop game for XBLIG ?

Thanks!

@Xelf

No, I didn’t use IwGame engine. Even though it looks nice. Puzzled Rabbit was an extremely simple game, so yeah it was pretty much just Marmalade SDK.

As for the XBLIG… it wasn’t hard but I obviously had to convert my C++ code over to C# (which I was glad I started when the game was done thus avoiding changing 2 versions) and also I had to do some platform specific coding (gamepad, users, etc.). Not knowing much about XNA before, I think it took me about a week to convert Puzzled Rabbit to it. It was an interesting and fun experience but I don’t think I’ll ever release anything else for XBLIG.

Does anyone knows whether Marmelade’s binaries are bigger (and if so, how much) than those produced with the platform’s official SDKs, especially XCode?

Also, did anyone tested/compared with MoSync?

I would say that Marmalade apps are around the same size. Our latest game cOnnecticOns (http://itunes.apple.com/app/connecticons/id505645452) size is split up as follows:

Code – 900k compressed

Music – 2MB mp3’s

Graphics / sound effect, scripts, splash screens etc – 1.5MB compressed

If you do go by way of Marmalade then you may also want to check out our free open source game engine IwGame, its mark-up driven using an XML language we created called XOML. It enabled us to build cOnnecticOns in just 36 hours. The full source is also available to cOnnecticOns

@Mat The fact that the Marmalade code is 900k compressed isn’t really any useful information because in the final iOS binary (IPA) the code isn’t really being compressed. Well, it is, but compression is done _after_ encryption. And there’s a huge difference sometimes.

My Puzzled Rabbit was 1.45 MB (compressed 647 KB) and my currently work-in-progress game is 5.0 MB (while 2.0 MB compressed) – larger binary size here is the result of linking with many different libraries / Marmalade extensions.

Uncompressed the code size is 1.2MB. I believe the final size of the IPA when the app store has done with it uncompressed app size + compressed data size + 100k or so.

Nice article. But my opinion: It’s quite hard to get start using Marmalade. Unity are complex for newbie too but It’s easier to learn. It has a lot of cons. like: product binary size, performance not better than Marmalade,… but it got a friendly editor and many good built-in features which may take you more time to develop/integrate if using Marmalade (physics,…)

And I think the most important thing is gameplay and the interface of a game, not the technology behind it. So, don’t care too much about technology things, just focus to creative

Hi,

I created a cross platform mobile games framework. It’s kinda like DFSDK but you don’t have to wait a day for your ipa, it compiles instantly and automatically your source code, everything is automated. You can check it out at http://www.crossmobs.com, and please give me some feedback.

Thanks !