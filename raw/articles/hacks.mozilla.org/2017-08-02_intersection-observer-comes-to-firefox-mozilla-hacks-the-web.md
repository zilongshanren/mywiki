---
title: Intersection Observer comes to Firefox – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/08/intersection-observer-comes-to-firefox/
author: Dan Callahan
published: '2017-08-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

What do infinite scrolling, lazy loading, and online advertisements all have in common?

They need to know about—and react to—the visibility of elements on a page!

Unfortunately, knowing whether or not an element is visible has traditionally been difficult on the Web. Most solutions listen for [scroll](https://developer.mozilla.org/en-US/docs/Web/Events/scroll) and [resize](https://developer.mozilla.org/en-US/docs/Web/Events/resize) events, then use DOM APIs like[ getBoundingClientRect()](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect) to manually calculate where elements are relative to the viewport. This usually works, but it’s inefficient and doesn’t take into account other ways in which an element’s visibility can change, such as a large image finally loading higher up on the page, which pushes everything else downward.

Things get worse for advertisements, since *real money* is involved. As [Malte Ubl](https://twitter.com/cramforce) explained in [his presentation](https://www.youtube.com/watch?v=jO1TNGNTwpc#t=3m30) at JSConf Iceland, advertisers don’t want to pay for ads that never get displayed. To make sure they know when ads are visible, they cover them in dozens of tiny, single-pixel Flash movies whose visibility can be inferred from their framerate. On platforms without Flash, like smartphones, advertisers set up timers to force browsers to recalculate the position of each ad every few milliseconds.

These techniques kill performance, drain batteries, and would be *completely unnecessary* if the browser could just *notify us* whenever an element’s visibility changed.

That’s what [IntersectionObserver](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver) does.

**Hello, new IntersectionObserver()**

At its most basic, the IntersectionObserver API looks something like:

```
let observer = new IntersectionObserver(handler);
observer.observe(target); // <-- Element to watch
```


The [demo](https://codepen.io/callahad/pen/YxXpyN) below shows a simple handler in action.

A single observer can watch many target elements simultaneously; just repeat the call to `observer.observe()`

for each target.

**Intersection? I thought this was about visibility?**

By default, IntersectionObservers calculate how much of a target element overlaps (or *“intersects with”*) the visible portion of the page, also known as the browser’s “viewport:”

However, observers can also monitor how much of an element intersects with an arbitrary parent element, regardless of actual on-screen visibility. This can be useful for widgets that load content on demand, like an infinitely scrolling list inside a container `div`

. In those cases, the widget could use IntersectionObservers to help load just enough content to fill its container.

For simplicity, the rest of this article will discuss things in terms of “visibility,” but remember that IntersectionObservers aren’t necessarily limited to *literal* visibility.

**Handler basics**

Observer handlers are callbacks that receive two arguments:

- A list of
[IntersectionObserverEntry](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserverEntry)objects, each containing metadata about how a target’s intersection has changed since the last invocation of the handler. - A reference to the observer itself.

Observers default to monitoring the browser’s viewport, which means the demo above just needs to look at the `isIntersecting`

property to determine if any part of a target element is visible.

By default, handlers only run at the moment when target elements transition from being completely off-screen to being partially visible, or vice versa, but what if you want to distinguish between partially-visible and fully-visible elements?

Thresholds to the rescue!

**Working with Thresholds**

In addition to a handler callback, the IntersectionObserver constructor can take an object with several configuration options for the observer. One of these options is `threshold`

, which defines breakpoints for invoking the handler.

```
let observer = new IntersectionObserver(handler, {
threshold: 0 // <-- This is the default
});
```


The default `threshold`

is `0`

, which invokes the handler whenever a target becomes partially visible or completely invisible. Setting `threshold`

to `1`

would fire the handler whenever the target flips between fully visible and partially visible, and setting it to `0.5`

would fire when the target passes point of 50% visibility, in either direction.

You can also supply an array of thresholds, as shown by `threshold: [0, 1]`

in the [demo](https://codepen.io/callahad/pen/OjVRrg/) below:

Slowly scroll the target in and out of the viewport and observe its behavior.

The target starts fully visible—its `intersectionRatio`

is `1`

—and changes twice as it scrolls off the screen: once to something like `0.87`

, and then to `0`

. As the target scrolls back into view, its `intersectionRatio`

changes to `0.05`

, then `1`

. The `0`

and `1`

make sense, but where did the additional values come from, and what about all of the *other* numbers between `0`

and `1`

?

Thresholds are defined in terms of transitions: the handler fires whenever the browser notices that a target’s `intersectionRatio`

has grown or shrunk past one of the thresholds. Setting the thresholds to `[0, 1]`

tells the browser “notify me whenever a target crosses the lines of no visibility (`0`

) and full visibility (`1`

),” which effectively defines three states: fully visible, partially visible, and not visible.

The observed value of `intersectionRatio`

varies from test to test because the browser must wait for an idle moment before checking and reporting on intersections; those sorts of calculations happen in the background at a lower priority than things like scrolling or user input.

Try [editing the codepen](https://codepen.io/callahad/pen/OjVRrg) to add or remove thresholds. Watch how it changes when and where the handler runs.

**Other options**

The IntersectionObserver constructor can take two other options:

`root`

: The area to observe (default: the browser viewport).`rootMargin`

: How much to shrink or expand the root’s logical size when calculating intersections (default:`"0px 0px 0px 0px"`

).

Changing the `root`

allows an observer to check for intersection with respect to a parent container element, instead of just the browser’s viewport.

Growing the observer’s `rootMargin`

makes it possible to detect when a target nears a given region. For example, an observer could wait to load off-screen images until *just before* they become visible.

**Browser support**

IntersectionObserver is available by default in Edge 15, Chrome 51, and Firefox 55, which is due for release next week.

A [polyfill](https://github.com/WICG/IntersectionObserver/tree/gh-pages/polyfill) is available which works effectively everywhere, albeit without the performance benefits of native implementations.

**Additional Resources:**

[MDN: Intersection Observer](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)[Cross-browser Polyfill](https://github.com/WICG/IntersectionObserver/tree/gh-pages/polyfill)[Can I Use](http://caniuse.com/#feat=intersectionobserver)browser support information

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 8 comments

SimonAugust 3rd, 2017 at 00:06Šime VidasAugust 3rd, 2017 at 01:10Eric ShepherdAugust 4th, 2017 at 07:12EduardoAugust 4th, 2017 at 07:35OliverAugust 9th, 2017 at 02:04Dan CallahanAugust 9th, 2017 at 13:00Jeremy WagnerAugust 10th, 2017 at 11:22Dan CallahanAugust 11th, 2017 at 11:47