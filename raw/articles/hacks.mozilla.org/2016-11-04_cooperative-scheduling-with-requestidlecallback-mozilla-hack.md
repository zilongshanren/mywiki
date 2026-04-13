---
title: Cooperative Scheduling with requestIdleCallback – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/11/cooperative-scheduling-with-requestidlecallback/
author: Sergi Mansilla
published: '2016-11-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*TL;DR: requestIdleCallback support has landed in Firefox Nightly, with plans to ship in Firefox 52.*

The messiest aspect of building interactive websites boils down to this: the main thread is the same as the UI thread. Rendering the page and responding to user actions happens in contention with computation, network activity, and manipulation of the DOM. Some of these things can be moved to another thread safely and with relative ease [using Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers), but only the main thread can change the DOM and many other web platform features. Historically, there’s been no way for scripts to “play nice” with user interaction and page rendering, leading to choppy frame rates and laggy input.

Obviously, I wouldn’t be writing this post if that were still true!

If you absolutely must perform tasks on the main thread (mutating the DOM or interacting with main-thread-only Web APIs), you can now request the browser provide you with a window of time in which it is safe to do so! Previously, developers have used `setTimeout`

to give the browser room to breathe between periodic actions. At best this only delays a task until the next go-around of the event loop. And it can still cause jank.

In comes `requestIdleCallback`

. Superficially, its basic use is similar to `setTimeout`

or the even more similar [ setImmediate](https://developer.mozilla.org/en-US/docs/Web/API/Window/setImmediate):

```
requestIdleCallback(sporadicScriptAction);
```


However, the browser has much more leeway with which to serve your request. Instead of waiting a specific number of milliseconds or until the next immediate pass of the event loop, `requestIdleCallback`

allows the browser to wait until it identifies an [idle period](https://www.w3.org/TR/requestidlecallback/#idle-periods). An idle period may be a few milliseconds between painting individual frames.

Keep in mind, a buttery-smooth 60fps animation leaves only 16ms between frames, much of which might be needed by the browser. So we’re talking only a *few* milliseconds! Alternately, if there are no animations or other visual changes happening, the browser may elect to allow up to 50ms. If a user interacts with the page, visual feedback that takes less than 100ms feels “instant”. With a maximum of 50ms, there’s plenty of leeway for the browser to service any incoming user events gracefully.

So, your callback may be given a 1ms-10ms window in which to act, or a languid, leisurely 50ms! How will your code know? That’s where `requestIdleCallback`

differs from its antecedents. When your callback is called, it receives information about how much time it has to act:

```
// we know this action can take longer than 16ms,
// so let's be safe and only do it when we have the time.
function sporadicScriptAction (timing) {
if (timing.timeRemaining() > 20) {
// update DOM or what have you
} else {
// request another idle period or simply do nothing
}
}
```


Your callback will be passed an `IdleDeadline`

object containing a `timeRemaining`

method. `timeRemaining()`

will provide a real-time estimate of how much time is left in the idle period, allowing scripts to determine how much work to do, or whether to do it at all.

## What if I *Have* to Do Stuff?

Cooperative multitasking is a negotiation between parties, and for it to be successful, both sides (browser and script) need to make concessions. If your main-thread action has to happen in a certain time frame (UI updates or other timing-sensitive actions), scripts can request a `timeout`

after which the callback *must* run:

```
// Call me when you have time, but wait no longer than 1000ms
requestIdleCallback(neededUIUpdate, { timeout: 1000 });
```


If an idle period becomes available before the request’s timeout, things will proceed as before. However, if the request reaches the provided timeout and no idle period is available, the callback will run regardless. This is detectable in the callback by checking the `didTimeout`

property of the `IdleDeadline`

object:

```
function sporadicScriptAction (timing) {
// will be 0, because we reached the timeout condition
if (timing.timeRemaining() > 20) {
} else if (timing.didTimeout) { // will be true
}
}
```


## Never Mind (Canceling a Call)

As with all scheduled callback mechanisms (`setTimeout`

, `setImmediate`

, `setInterval`

), and `requestAnimationFrame`

), `requestIdleCallback`

returns a handle which can be used to cancel a scheduled function call:

```
var candyTime = requestIdleCallback(goTrickOrTreating);
// it's November.
cancelIdleCallback(candyTime);
```


## A More Coordinated Web

Just as `requestAnimationFrame`

gave us the tools to coordinate with browser paint, `requestIdleCallback`

provides a way to cooperate with the browser’s overall work schedule. When done correctly, the user won’t even notice that you’re doing work- they’ll just feel a smoother, more responsive website. We can’t go back in time and separate the UI thread from the main thread in JS, but with the right tools, separation of concerns, and planning, we can still build great interactive experiences.

## 3 comments

Ashish ChaudharyNovember 9th, 2016 at 10:23PotchNovember 14th, 2016 at 09:42Edwin MartinNovember 11th, 2016 at 06:15