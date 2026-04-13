---
title: 'Animating with javascript: from setInterval to requestAnimationFrame – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2011/08/animating-with-javascript-from-setinterval-to-requestanimationframe/
author: Louisremi
published: '2011-08-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Animating DOM elements [1] or the content of a canvas is a classical use case for setInterval. But the interval is not as reliable as it seems, and a more suitable API is now available…*

### Animating with setInterval

To animate an element moving 400 pixels on the right with javascript, the basic thing to do is to move it 10 pixels at a time on a regular interval.

An HTML5 game based on this logic would normally run at ~60fps[[2]](https://hacks.mozilla.org#endnote2), but if the animations were too complex or running on a low-spec. device (a mobile phone for instance) and processing a frame were taking more than 16ms, then the game would run at a lower framerate: when processing 1 frame takes 33ms, the game runs at 30fps and game elements move twice as slowly as they should. Animations would still look smooth enough, but the game experience would be altered.

### Animating at constant speed

To animate at constant speed, we need to calculate the time delta since the last frame and move the element proportionally.


### Animating with requestAnimationFrame

Since the interval parameter is irrelevant in complex animations, as there’s no guarantee that it will be honored, a new API has been designed: [requestAnimationFrame](https://developer.mozilla.org/en/DOM/window.mozRequestAnimationFrame). It’s simply a way to tell the browser “before drawing the next frame on the screen, execute this game logic/animation processing”. The browser is in charge of choosing the best moment to execute the code, which results in a more efficient use of resources[[3]](https://hacks.mozilla.org#endnote3).

Here’s how an animation with requestAnimationFrame would be written.

**Note: Following code snippets don’t include feature detections and workarounds necessary to work in current browsers. Should you want to play with them, you should try the ready-to-use animLoop.js.**

### Dealing with inactive tabs

requestAnimationFrame was built with another benefit in mind: letting the browser choose the best frame interval allows to have a long interval in inactive tabs. Users could play a CPU intensive game, then open a new tab or minimize the window, and the game would pause[[4]](https://hacks.mozilla.org#endnote4), leaving resources available for other tasks.

*Note: the potential impact of such behavior on resource and battery usage is so positive that browser vendors decided to adopt it for setTimeout and setInterval as well [5].*

This behavior also means that the calculated time delta might be really high when switching back to a tab containing an animation. This will result in animation appearing to jump or creating “[wormholes](http://en.wikipedia.org/wiki/Wormhole)“[[6]](https://hacks.mozilla.org#endnote6), [as illustrated here](http://jsfiddle.net/louisremi/qWcMG/3/).

Wormholes can be fixed by clamping the time delta to a maximum value, or not rendering a frame when the time delta is too high.


[JSFiddle demo](http://jsfiddle.net/louisremi/KDaEh/2/).

### Problems with animation queues

Libraries such as jQuery queue animations on elements to execute them one after the other. This queue is generally only used for animations that are purposefully consecutive.

But if animations are triggered by a timer, the queue might grow without bound in inactive tabs, as paused animations stack up in the queue. When switching back to affected tabs, a user will see a large number of animations playing consecutively when only one should happen on a regular interval:

This problem is visible in some auto-playing slideshows such as [mb.gallery](http://pupunzi.com/#mb.components/mb.gallery/gallery.html). To work around it, developers can empty animation queues before triggering new animations[[7]](https://hacks.mozilla.org#endnote7).

[JSFiddle demo](http://jsfiddle.net/louisremi/An834/).

### Conclusion

The delays of setTimeout and setInterval and of course requestAnimationFrame are unpredictable and much longer in inactive tabs. These facts should be taken into account not only when writing animation logic, but in fps counters, time countdowns, and everywhere time measurement is crucial.

[[1]](https://hacks.mozilla.org#note1) The DOM can now be animated with [CSS3 Transitions](https://developer.mozilla.org/en/CSS/CSS_transitions) and [CSS3 Animations](https://developer.mozilla.org/en/CSS/CSS_animations).

[[2]](https://hacks.mozilla.org#note2) 1 frame every 16ms is 62.5 frames per second.

[[3]](https://hacks.mozilla.org#note3) See the [illustration of this fact](http://msdn.microsoft.com/en-us/ie/hh272906) on msdn.

[[4]](https://hacks.mozilla.org#note4) The behavior of requestAnimationFrame in inactive tabs is still [being worked on](http://www.w3.org/TR/2011/WD-animation-timing-20110602/) at the w3c, and might differ in other browsers.

[[5]](https://hacks.mozilla.org#note5) See [related Firefox bug](https://bugzilla.mozilla.org/show_bug.cgi?id=633421) and [related chromium bug](http://code.google.com/p/chromium/issues/detail?id=66078).

[[6]](https://hacks.mozilla.org#note6) This term was first coined by [Seth Ladd](http://sethladd.com/) in his “[Intro to HTML5 Game Development](http://io-2011-html5-games-hr.appspot.com/#36)” talk.

[[7]](https://hacks.mozilla.org#note7) See documentation of your js library, such as [effects](http://api.jquery.com/category/effects/) and [stop()](http://api.jquery.com/stop) for jQuery.

## About
[
louisremi ](http://twitter.com/louis_remi)

Developer Relations Team, long time jQuery contributor and Open Web enthusiast. [@louis_remi](http://twitter.com/louis_remi)

## 12 comments

FerossAugust 19th, 2011 at 23:02PabloSeptember 3rd, 2011 at 04:40Kris GraySeptember 15th, 2011 at 12:03PabloSeptember 16th, 2011 at 05:59Chad ElliottJanuary 1st, 2012 at 13:17Erik LandvallMay 21st, 2012 at 11:22Ivan KuckirJuly 26th, 2012 at 00:49Jens Ahrengot BoddumSeptember 30th, 2012 at 14:34Jens Ahrengot BoddumSeptember 30th, 2012 at 14:48zogzogDecember 25th, 2012 at 05:03zogzog78December 25th, 2012 at 11:23DCJanuary 19th, 2013 at 22:36