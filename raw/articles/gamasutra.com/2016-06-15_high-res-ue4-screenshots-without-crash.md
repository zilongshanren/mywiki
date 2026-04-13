---
title: High-Res UE4 Screenshots without Crash
url: https://www.gamedeveloper.com/art/high-res-ue4-screenshots-without-crash
author: Niber Bergstrom
published: '2016-06-15'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# High-Res UE4 Screenshots without Crash

Even Epic's own documentation admits that their tool will crash if you push the resolutions too high. Luckily I've discovered a way to push it to the extreme!

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

One of the great things about GPU rendering is how insanely fast you can render high resolution. While rendering things like lightmaps with GI is still time-consuming and resource-hungry, the actual 3d rendering is near resolution-independent. Do you want to render at 4 times your usual resolution for a print? As long as you have an extra spare couple of seconds, you’re in luck!

Unlike most engines, in [UE4 (Unreal Engine 4)](http://niberspace.com/blog/category/game-dev/ue4-unreal-engine-4/) taking a high-res screenshots needs neither custom code, plug-ins or even memorizing command-line syntax. Simply use [Epic’s provided ‘High Resolution Screenshots Tool’](http://niberspace.com/blog/ue4-high-resolution-screenshots/).

There is only one little problem…

Al thought the tool is programmed flawlessly (as is the case with all of Epic’s tools), you may run into a problem from another source. With hardware accelerated 3d being primarily developed for realtime graphics, your graphics card assumes you desire to run a smooth frame-rate. When your ridiculously detailed screenshot is taking forever to render, your graphics card assumes a bug and terminate the process.

Al though 2 seconds may be an eternity in a world of 60 fps gaming, it’s nothing for rendering still images. Coming from CPU offline rendering where a single image render can be an overnight process, 2 or even 100 seconds is less than it takes me to go fill my cup of water.

Luckily I found there is a way to tell your well-meaning computer to take a chill-pill. To bump up its default panic mode threshold of 2 seconds into whatever value you desire. After setting mine to a glorious 40 seconds, I can now save screenshots at an arousing 15360 by 8640 pixels (including buffer visualization targets). I find this to be the ultimate resolution as it down-samples perfectly into 8k (my ideal editing resolution).

## Regedit Fix to Take High Resolutions Screenshots

Warning! The following is a hacky regedit fix which may break your computer. Under no circumstances should you listen to any of my regedit advice no matter how awesome.

Navigate to the following folder in your regedit:


“HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers”Create (or modify) a key of type “DWORD (32-bit)” name “TdrDelay” with a value of 40 as Hexadecimal value.

Reboot your computer.


Congratulations, you’ve now told your computer to wait a full 40 seconds before freaking out about a seemingly never-ending frame render. Your life as you know it will never be the same!

This is my first blog post here at Gamasutra so starting easy with this little quick tip, but hopefully more interesting things to come in the future. For more gems like these (as well as stories of my game dev adventures in China) be sure to check out [my indie game development blog](http://niberspace.com/blog/)!