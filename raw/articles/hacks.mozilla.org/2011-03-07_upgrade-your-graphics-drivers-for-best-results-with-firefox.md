---
title: Upgrade your graphics drivers for best results with Firefox 4 – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2011/03/upgrade-your-graphics-drivers-for-best-results-with-firefox-4/
author: Janet Swisher
published: '2011-03-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Benoit Jacob from the platform engineering team has a blog post on how to best take advantage of hardware acceleration and WebGL in Firefox 4, namely: [Upgrade your graphics drivers!](http://blog.mozilla.com/bjacob/2011/03/04/upgrade-your-graphics-drivers/)

Firefox 4 automatically disables the hardware acceleration and WebGL features if the graphics driver on your system has bugs that cause Firefox to crash. You still get all the other benefits of Firefox 4, of course, just not the newest graphics features. But for best results, you need an up-to-date graphics driver that fixes those bugs.

- Windows users with Intel cards: you need a
[very recent driver](https://wiki.mozilla.org/Blocklisting/Blocked_Graphics_Drivers#Intel_cards). - Windows users with NVIDIA cards: you need
[driver version 257.21 or newer](https://wiki.mozilla.org/Blocklisting/Blocked_Graphics_Drivers#NVIDIA_cards). - Windows users with ATI cards: you need
[driver version 10.6 or newer](https://wiki.mozilla.org/Blocklisting/Blocked_Graphics_Drivers#AMD.2FATI_cards). - Instructions are also given for
[Mac](https://wiki.mozilla.org/Blocklisting/Blocked_Graphics_Drivers#On_Mac)and[X11 (Linux/Unix)](https://wiki.mozilla.org/Blocklisting/Blocked_Graphics_Drivers#On_X11).

If you’re planning to develop using WebGL, you need to also spread this message to your users, so they will be able to experience the awesome results of your hard work.

## 17 comments

WeanerMarch 7th, 2011 at 12:10DavidMarch 7th, 2011 at 20:22JonathanMarch 18th, 2011 at 08:47ПожарMarch 8th, 2011 at 02:38Benoit JacobMarch 8th, 2011 at 06:10DavidMarch 8th, 2011 at 09:06NoxMarch 8th, 2011 at 08:54DavidMarch 8th, 2011 at 09:08WeanerMarch 8th, 2011 at 14:39Yuhong BaoMarch 8th, 2011 at 20:30StevenMarch 18th, 2011 at 04:01KhaledMarch 23rd, 2011 at 06:20Benoit JacobMarch 23rd, 2011 at 08:54KhaledMarch 23rd, 2011 at 15:50nemoMarch 24th, 2011 at 14:43Chris ThomasMarch 25th, 2011 at 08:45Dre TuchOctober 25th, 2011 at 14:45