---
title: More efficient Javascript animations with mozRequestAnimationFrame – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/08/more-efficient-javascript-animations-with-mozrequestanimationframe/
author: Paul Rouget
published: '2010-08-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a re-post from Robert O’Callahan’s blog.*

`<b>mozRequestAnimationFrame</b>`

is an experimental API to make Javascript animations more efficient. We do not guarantee to support it forever, and I wouldn’t evangelize sites to depend on it. We’ve implemented it so that people can experiment with it and we can collect feedback. At the same time we’ll propose it as a standard (minus the moz prefix, obviously), and author feedback on our implementation will help us make a better standard.

*This feature will be available in Firefox 4 Beta 4.*

In Firefox 4 we’ve added support for two major standards for declarative animation — SVG Animation (aka SMIL) and CSS Transitions. However, I also feel strongly that the Web needs better support for JS-based animations. No matter how rich we make declarative animations, sometimes you’ll still need to write JS code to compute (“sample”) the state of each animation frame. Furthermore there’s a lot of JS animation code already on the Web, and it would be nice to improve its performance and smoothness without requiring authors to rewrite it into a declarative form.

Obviously you can implement animations in JS today using setTimeout/setInterval to trigger animation samples and calling Date.now() to track animation progress. There are two big problems with that approach. The biggest problem is that there is no “right” timeout value to use. Ideally, the animation would be sampled exactly as often as the browser is able to repaint the screen, up to some maximum limit (e.g., the screen refresh rate). But the author has no idea what that frame rate is going to be, and of course it can even vary from moment to moment. Under some conditions (e.g. the animation is not visible), the animation should stop sampling altogether. A secondary problem is that when there are multiple animations running — some in JS, and some declarative animations — it’s hard to keep them synchronized. For example you’d like a script to be able to start a CSS transition and a JS animation with the same duration and have agreement on the exact moment in time when the animations are deemed to have started. At each paint you’d also like to have them sampled using the same “current time”.

These problems have come up from time to time on mailing lists, for example on [public-webapps](http://www.mail-archive.com/public-webapps@w3.org/msg05877.html). A while ago I worked out [an API proposal](http://weblogs.mozillazine.org/roc/archives/2009/07/progress.html) and Boris Zbarsky just implemented it; it’s in Firefox 4 beta 4. Here’s the API, it’s really simple:

`window.mozRequestAnimationFrame()`: Signals that an animation is in progress, requests that the browser schedule a repaint of the window for the next animation frame, and requests that a`MozBeforePaint`event be fired before that repaint.- The browser fires a
`MozBeforePaint`event at the window before we repaint it. The`timeStamp`attribute of the event is the time, in milliseconds since the epoch, deemed to be the “current time” for all animations for this repaint. - There is also a
`window.mozAnimationStartTime`attribute, also in milliseconds since the epoch. When a script starts an animation, this attribute indicates when that animation should be deemed to have started. This is different from Date.now() because we ensure that between any two repaints of the window, the value of window.mozAnimationStartTime is constant, so all animations started during the same frame get the same start time. CSS transitions and SMIL animations triggered during that interval also use that start time. (In beta 4 there’s a bug that means we don’t quite achieve that, but we’ll fix it.)

That’s it! Here’s [an example](http://people.mozilla.com/~roc/mozRequestAnimationFrame-demo.html); the relevant sample code:

```
var start = window.mozAnimationStartTime;
function step(event) {
var progress = event.timeStamp - start;
d.style.left = Math.min(progress/10, 200) + "px";
if (progress < 2000) {
window.mozRequestAnimationFrame();
} else {
window.removeEventListener("MozBeforePaint", step, false);
}
}
window.addEventListener("MozBeforePaint", step, false);
window.mozRequestAnimationFrame();
```

It's not very different from the usual setTimeout/Date.now() implementation. We use window.mozAnimationStartTime and event.timeStamp instead of calling Date.now(). We call window.mozRequestAnimationFrame() instead of setTimeout(). Converting existing code should usually be easy. You could even abstract over the differences with a wrapper that calls setTimeout/Date.now if mozAnimationStartTime/mozRequestAnimationFrame are not available. Of course, we want this to become a standard so eventually such wrappers will not be necessary!

Using this API has a few advantages, even in this simple case. The author doesn't have to guess a timeout value. If the browser is overloaded the animation will degrade gracefully instead of uselessly running the step script more times than necessary. If the page is in a hidden tab, we'll be able to throttle the frame rate down to a very low value (e.g. one frame per second), saving CPU load. (This feature has not landed yet though.)

One important feature of this API is that mozRequestAnimationFrame is "one-shot". You have to call it again from your event handler if your animation is still running. An alternative would be to have a "beginAnimation"/"endAnimation" API, but that seems more complex and slightly more likely to leave animations running forever (wasting CPU time) in error situations.

This API is compatible with browser implementations that offload some declarative animations to a dedicated "compositing thread" so they can be animated even while the main thread is blocked. (Safari does this, and we're building something like it too.) If the main thread is blocked on a single event for a long time (e.g. if a MozBeforePaint handler takes a very long time to run) it's obviously impossible for JS animations to stay in sync with animations offloaded to a compositing thread. But if the main thread stays responsive, so MozBeforePaint events can be dispatched and serviced between each compositing step performed by the compositing thread, I think we can keep JS animations in sync with the offloaded animations. We need to carefully choose the animation timestamps returned by mozAnimationStartTime and event.timeStamp and dispatch MozBeforePaint events "early enough".

**EDIT: The mozRequestAnimationFrame Frame Rate Limit**

*(from Robert O'Callahan’s blog)*

A few people have been playing with [mozRequestAnimationFrame](http://weblogs.mozillazine.org/roc/archives/2010/08/mozrequestanima.html) and noticed that they can't get more than 50 frames per second. *This is intentional, and it's a good feature.*

On modern systems an application usually cannot get more than 50-60 frames per second onto the screen. There are multiple reasons for this. Some of them are hardware limitations: CRTs have a fixed refresh rate, and LCDs are also limited in the rate at which they can update the screen due to [bandwidth limitations in the DVI connector and other reasons](http://www.tweakguides.com/Graphics_8.html). Another big reason is that modern operating systems tend to use "compositing window managers" which redraw the entire desktop at a fixed rate. So even if an application updates its window 100 times a second, the user won't be able to see more than about half of those updates. (Some applications on some platforms, typically games, can go full-screen, bypass the window manager and get updates onto the screen as fast as the hardware allows, but obviously desktop browsers aren't usually going to do that.)

So, firing a MozBeforePaint event more than about 50 times a second is going to achieve nothing other than wasting CPU (i.e., power). So we don't. Apart from saving power, reducing animation CPU usage helps overall performance because we can use the free time to perform garbage collection or other house-cleaning tasks, reducing the incidence or length of frame skips.

We need to do some followup work to make sure that on each platform we use the optimal rate; modern platforms have APIs to tell us the window manager's composition rate. But 50Hz is almost always pretty close.

This all means that measuring FPS is a bad way to measure performance, once you're up to 50 or more. At that point you need to increase the difficulty of your workload.

Tell us what you think.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 14 comments

LucaAugust 16th, 2010 at 06:25Robert O’CallahanAugust 17th, 2010 at 02:31Julián CeballosAugust 21st, 2010 at 22:49Daniel CassidyAugust 26th, 2010 at 14:46how.,eSeptember 4th, 2010 at 17:11louis-rémiOctober 21st, 2010 at 11:32EvgenyNovember 7th, 2010 at 01:54Reyboz BlogDecember 13th, 2010 at 12:42VictorJanuary 16th, 2011 at 23:44JorgeMarch 24th, 2011 at 11:34JoeAugust 26th, 2011 at 16:59miloJune 30th, 2012 at 18:52miloJune 30th, 2012 at 18:58GregOctober 20th, 2012 at 12:36