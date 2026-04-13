---
title: asm.js performance improvements in the latest version of Firefox make games
  fly! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/05/asm-js-performance-improvements-in-the-latest-version-of-firefox-make-games-fly/
author: Alon Zakai
published: '2014-05-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [latest version of Firefox which launched last week](https://blog.mozilla.org/blog/2014/04/29/mozilla-introduces-the-most-customizable-firefox-ever-with-an-elegant-new-design/) includes a major update to the user interface as well as to features like Sync. Another area in which this release brings significant improvements is in **asm.js performance**, which as we will see below is very important for things like games. To put that aspect of Firefox’s performance in context, we’ll take a look at benchmark results comparing Firefox to other browsers, which show that Firefox is faster at executing asm.js code.

## asm.js speedups

[asm.js](http://asmjs.org/) is a subset of JavaScript that is very easy to optimize and is particularly useful for porting code in C or C++ to the Web. We’ve blogged about how Firefox can [optimize asm.js code using 32-bit floating point operations](https://hacks.mozilla.org/2013/12/gap-between-asm-js-and-native-performance-gets-even-narrower-with-float32-optimizations/), which, together with all the other work on optimizing asm.js, allows it to run at around **1.5x slower** than the speed of the same C/C++ when compiled natively. So, while not quite native speed yet, things are getting very close. At the time of that blog post those optimizations were only on nightly builds, but they are now reaching hundreds of millions of Firefox users in Firefox 29, which is now the release version of Firefox.

Another important set of asm.js optimizations concern **startup speed**. As [blogged about by Luke](https://blog.mozilla.org/luke/2014/01/14/asm-js-aot-compilation-and-startup-performance/) a few months ago, Firefox performs ahead of time (AOT) compilation and can cache the results, for significant speedups in startup times. Those optimizations also shipped to users in Firefox 29.

## Web browser comparisons

Now that all those optimizations have shipped, it’s interesting to look at up-to-date browser comparisons on asm.js code. The above graph shows the [Emscripten](http://emscripten.org/) [benchmark suite](http://kripken.github.io/embenchen/) running the latest stable versions of Google Chrome, Internet Explorer and Firefox on Windows 8.1. Lower numbers are better in all the results here, which are real-world codebases compiled to asm.js (see notes in the graph).

## Unity, Emscripten and asm.js

asm.js is a subset of JavaScript, so it is just one of many styles of JavaScript out there. But it represents an important use case. As [we announced at GDC](https://blog.mozilla.org/blog/2014/03/18/mozilla-and-unity-bring-unity-game-engine-to-webgl/), [Unity](http://unity3d.com/), one of the most popular game creation tools on the market, will [support the Web by using Emscripten to compile their engine to asm.js](http://blogs.unity3d.com/2014/04/29/on-the-future-of-web-publishing-in-unity/).

But videos are no substitute for the real thing! You can try the games shown there in your browser right now, with Unity’s recently released ** Dead Trigger 2** and

**demos. If you run those in the latest version of**

[Angry Bots](http://beta.unity3d.com/jonas/AngryBots/)[Firefox](https://www.mozilla.org/firefox), you’ll see many of the asm.js optimizations mentioned earlier in action. For example, if you visit one of those links more than once then asm.js caching will allow it to avoid recompiling the game (so it starts up faster), and also gameplay will be smoother due to faster asm.js execution.

Being able to execute asm.js-style code efficiently makes it possible for games like this to run well on the Web, without proprietary, nonstandard plugins. That’s why it’s exciting to see more asm.js optimizations reach Firefox users in Firefox 29. And while benchmark results can sometimes seem like nothing more than abstract numbers, speedups on asm.js benchmarks directly improve things like games, where performance is extremely important and very noticeable.

(Thanks to Marc Schifer for helping with the benchmark measurements.)

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 15 comments

JulienWMay 5th, 2014 at 07:36Anthony HughesMay 5th, 2014 at 16:05shavounetMay 6th, 2014 at 08:44AkiMay 12th, 2014 at 17:30Wernfried RheinmaierMay 5th, 2014 at 09:16Alon ZakaiMay 5th, 2014 at 10:11njnMay 6th, 2014 at 03:08Wernfried RheinmaierMay 6th, 2014 at 17:38RyanMay 12th, 2014 at 16:29Dereck L.May 12th, 2014 at 18:08MikeMay 12th, 2014 at 23:50gaby de wildeMay 12th, 2014 at 20:37MikeMay 12th, 2014 at 23:46Alon ZakaiMay 13th, 2014 at 10:09BrianMay 13th, 2014 at 08:02