---
title: Smoother scrolling in Firefox 46 with APZ – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/02/smoother-scrolling-in-firefox-46-with-apz/
author: Kartikaya Gupta
published: '2016-02-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Have you ever been on Facebook or Twitter, merrily scrolling down the page, when all of a sudden, the browser appears to freeze? For several long seconds it just hangs there, and you’re not sure if it’s going to crash or not. Then, finally, something gives way, and the page jumps to catch up to your scrolling, disorienting you? That’s called *jank*, and in Firefox 46 Beta we are well on our way to making jank a thing of the past.

In Firefox 46 Beta, we’re bringing [asynchronous panning and zooming (APZ)](https://wiki.mozilla.org/Platform/GFX/APZ) to Firefox. The underlying technology was first developed for our mobile platforms, where responsiveness to touch input is one of the pillars of performance. Now we are bringing that over to our desktop platforms, and using it for mousewheel/trackpad scrolling. With APZ, scrolling down pages should be smooth and jank-free, even if the page is busy running lots of JavaScript or is slow to repaint. In future releases, we plan on enabling APZ for other methods of scrolling (such as touch and scrollbar-dragging) as well.

## Under the Hood

Browsers traditionally handled user input events on the browser’s main event-handling thread. This meant that it could get blocked by pretty much anything else the browser was doing, including running scripts and painting. In Firefox, the [Electrolysis (e10s) project](https://wiki.mozilla.org/Electrolysis) separates the content process from the main browser process. This gives us another path for handling input events. Instead of passing the input events from the parent process to the content process to drive scrolling as usual, the input events are used to drive scrolling in the parent process compositor before they are forwarded to the child process for normal processing and dispatch. This is illustrated in the diagrams below.

*Figure 1. Code flow without e10s or APZ.*


In Figure 1 above, the potentially long-running operations are indicated in red. Although the compositor thread can still composite to the screen rapidly (at 60 frames per second), it relies on getting the painted content from the main thread. Since the main thread can be blocked by long-running JavaScript or paint operations, paint updates from scroll inputs also gets blocked and can’t get to the compositor.

*Figure 2. Code flow with e10s and APZ*

In Figure 2 above, we can see how introducing e10s and APZ affects the flow. The input events arrive in the main thread of the parent process, which is free of long-running operations. Therefore, it can quickly pass on the input events to the compositor thread, where the APZ code uses it do asynchronous scrolling. Meanwhile, the input event is also forwarded to the main thread of the child process, where it is delivered to web content and triggers repainting. Even though these operations may still be slow, they no longer block the scroll updates from being composited to the screen.

This approach, although great for responsiveness, requires e10s to be enabled, and also introduces a certain complexity. For instance, the parent process needs to be able to do some amount of hit-testing on child processes to know where the input event landed. It also means that the parent process needs to have a mechanism for handling events on which `preventDefault()`

is called by web pages. For details on how this all works, refer to the [APZ documentation](https://github.com/mozilla/gecko-dev/blob/master/gfx/doc/AsyncPanZoom.md).

## Checkerboarding

Of course, nothing is free, and APZ comes at a cost. APZ does eliminate jank, but in some cases it does so by *checkerboarding* instead. Checkerboarding is what you get when you scroll faster than the browser can paint the page. When this happens, the content at your new scroll position hasn’t been painted yet, and so we just show a flat background color. (The term *checkerboarding* comes from the original iPhone implementation, which would show a checkerboard pattern.) Once the painting catches up, the content fills in.

Checkerboarding is inevitable with asynchronous scrolling due to memory limitations; it’s the cost of removing jank. However, in most cases it shouldn’t be noticeable – it only lasts a few hundred milliseconds, and we are working hard to bring that down further. The way we do this is by painting content outside of the visible area ahead of time, so that when the user scrolls it’s ready to be displayed right away. By better predicting where the user is going to scroll we can reduce the amount of checkerboard shown. Overall, trading off jank for checkerboarding results in a better user experience because the browser itself remains responsive and doesn’t appear to freeze or hang.

## Scroll-Linked Effects

APZ also has an impact on the way scroll-linked effects work. Because APZ does scrolling asynchronously from the main thread, this necessarily means that the scroll events seen by the web content will be delayed. In other words, there is some propagation delay from when the user scrolls until the scroll event can be dispatched to the web content. If the page uses the scroll event to reposition some content on the page, it will take additional time to process that change and display it to the user. This means that scroll-linked effects can appear delayed and out of sync with the scrolling. Under ideal circumstances, the delay between the user’s scrolling and the scroll-linked effect being visible should be no more than 2 frames (33ms at a frame rate of 60 frames per second). Although this is barely noticeable, in practice it may take a bit longer if the page is tying up the main thread with scripts, or if it is complex and takes a while to repaint. Therefore, it’s still important for the page to remain as responsive as possible by breaking up long-running scripts or using workers.

To eliminate this delay entirely, authors have the option to implement the scroll-linked effects using CSS positioning rather than JavaScript. We have CSS-only options available for the most widely used scroll-linked effects, including sticky positioning and the parallax effect. With CSS positioning, we can know ahead of time how the positioning will change, and so we can keep it perfectly in sync with the user’s scrolling. You can find examples and more details about [scroll-linked effects](https://developer.mozilla.org/en-US/docs/Mozilla/Performance/ScrollLinkedEffects) in the MDN article.

## About
[
Kartikaya Gupta ](https://staktrace.com)

Kartikaya Gupta is a developer on Mozilla's Platform Graphics team, and works on scrolling-related things in the Gecko rendering engine.

## 15 comments

abralFebruary 9th, 2016 at 10:11LucaFebruary 10th, 2016 at 00:48nicofrandFebruary 10th, 2016 at 01:39Kartikaya GuptaFebruary 10th, 2016 at 06:05Jason WeathersbyFebruary 10th, 2016 at 12:11abralFebruary 10th, 2016 at 13:00Jason WeathersbyFebruary 11th, 2016 at 09:29Peter J. SloetjesFebruary 13th, 2016 at 15:18PeteFebruary 14th, 2016 at 10:36Kartikaya GuptaFebruary 15th, 2016 at 20:04Kartikaya GuptaFebruary 15th, 2016 at 20:06PeteFebruary 16th, 2016 at 00:20Peter J. SloetjesFebruary 16th, 2016 at 13:45rafuseFebruary 21st, 2016 at 05:11Wellington Torrejais da SilvaFebruary 24th, 2016 at 15:11