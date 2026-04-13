---
title: Animating like you just don’t care with Element.animate – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2016/08/animating-like-you-just-dont-care-with-element-animate/
author: Brian Birtles
published: '2016-08-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In [Firefox 48](https://developer.mozilla.org/en-US/Firefox/Releases/48) we’re shipping the `<a href="https://developer.mozilla.org/docs/Web/API/Element/animate" target="_blank"><b>Element.animate()</b></a>`

** API** — a new way to programmatically animate DOM elements using JavaScript. Let’s pause for a second — “big deal”, you might say, or “what’s all the fuss about?” After all, there are already plenty of animation libraries to choose from. In this post I want to explain what makes `Element.animate()`

special.

## What a performance

`Element.animate()`

is the first part of the [ Web Animations API](https://developer.mozilla.org/docs/Web/API/Web_Animations_API) that we’re shipping and, while there are plenty of nice features in the API as a whole, such as better synchronization of animations, combining and morphing animations, extending CSS animations, etc., the biggest benefit of

`Element.animate()`

is performance. *In some cases,*

`Element.animate()`

lets you create jank-free animations that are simply impossible to achieve with JavaScript alone.Don’t believe me? Have a look at the following demo, which compares best-in-class JavaScript animation on the left, with `Element.animate()`

on the right, whilst periodically running some time-consuming JavaScript to simulate the performance when the browser is busy.

To see for yourself, try ![Performance of regular JavaScript animation vs Element.animate()](../../assets/72d0c0441aa259d2.gif)


[in the latest release of Firefox or Chrome. Then, you can check out the](https://people.mozilla.org/~bbirtles/demos/jank-example/jank-example.html)

**loading the demo**[full collection of demos](https://mozdevs.github.io/Animation-examples/)we’ve been building!

When it comes to animation performance, there is a lot of conflicting information being passed around. For example, you might have heard amazing (and untrue) claims like, “CSS animations run on the GPU”, and nodded along thinking, “Hmm, not sure what that means but it sounds fast.” So, to understand what makes `Element.animate()`

fast and how to make the most of it, let’s look into what makes animations slow to begin with.

## Animations are like onions (Or cakes. Or parfait.)

In order for an animation to appear smooth, we want all the updates needed for each frame of an animation to happen within about 16 milliseconds. That’s because browsers try to update the screen at the same rate as the refresh rate of the display they’re drawing to, which is usually 60Hz.

On each frame, there are typically two things a browser does that take time: calculating the layout of elements on the page, and drawing those elements. By now, hopefully you’ve *heard* the advice, “Don’t animate properties that update layout.” I am hopeful here — [current usage metrics](https://www.chromestatus.com/metrics/css/animated) suggest that web developers are wisely choosing to animate properties like [ transform](https://developer.mozilla.org/docs/Web/CSS/transform) and

[that don’t affect layout whenever they can. (](https://developer.mozilla.org/docs/Web/CSS/opacity)

`opacity`

[is another example of a property that doesn’t require recalculating layout, but we’ll see in a moment why opacity is better still.)](https://developer.mozilla.org/docs/Web/CSS/color)

`color`

If we can avoid performing layout calculations on each animation frame, that just leaves drawing the elements. It turns out that programming is not the only job where laziness is a virtue — indeed [animators worked out a long time ago](http://www.tofugu.com/japan/anime-vs-cartoons/#pull-cels) that they could avoid drawing a bunch of very similar frames by creating partially transparent cels, moving the cels around on top of the background, and snapshotting the result along the way.

![Example of cels used to create animation frames](../../assets/ed8bb61c10c034ff.gif)


*Example of creating animation frames using cels.*

* (Of course, not everyone uses fancy cels; some people just cut out Christmas cards.)*

A few years ago browsers caught on to this “pull cel” trick. Nowadays, if a browser sees that an element is moving around without affecting layout, it will draw two separate layers: the background and the moving element. On each animation frame, it then just needs to re-position these layers and snapshot the result without having to redraw anything. That snapshotting (more technically referred to as **compositing**) turns out to be something that GPUs are very good at. What’s more, when they composite, GPUs can apply 3D transforms and opacity fades all without requiring the browser to redraw anything. As a result, if you’re animating the transform or opacity of an element, the browser can leave most of the work to the GPU and stands a much better chance of making its 16ms deadline.

*Hint: If you’re familiar with tools like Firefox’s **Paint Flashing Tool** or Chrome’s **Paint Rectangles**you’ll notice when layers are being used because you’ll see that even though the element is animating nothing is being painted! To see the actual layers, you can set layers.draw-borders to true in Firefox’s *

*about:config*

*page, or choose “Show layer borders” in Chrome’s rendering tab.*

## You get a layer, and you get a layer, everyone gets a layer!

The message is clear — layers are great and you are expecting that surely the browser is going to take full advantage of this amazing invention and arrange your page’s contents like a [mille crêpe cake](http://www.pbs.org/food/fresh-tastes/mille-crepe-cake/). Unfortunately, layers aren’t free. For a start, they take up a lot more memory since the browser has to remember (and draw) all the parts of the page that would otherwise be overlapped by other elements. Furthermore, if there are too many layers, the browser will spend more time drawing, arranging, and snapshotting them all, and eventually your animation will actually get slower! As a result, a browser only creates layers when it’s pretty sure they’re needed — e.g. when an element’s `transform`

or `opacity`

property is being animated.

Sometimes, however, browsers don’t know a layer is needed until it’s too late. For example, if you animate an element’s transform property, up until the moment when you apply the animation, the browser has no premonition that it should create a layer. When you suddenly apply the animation, the browser has a mild panic as it now needs to turn one layer into two, redrawing them both. This takes time, which ultimately interrupts the start of the animation. The polite thing to do (and the best way to ensure your animations start smoothly and on time) is to give the browser some advance notice by setting the [ will-change](https://developer.mozilla.org/docs/Web/CSS/will-change) property on the element you plan to animate.

For example, suppose you have a button that toggles a drop-down menu when clicked, as shown below.

![Example of using will-change to prepare a drop-down menu for animation](../../assets/32837a0c97e872dc.gif)


We could hint to the browser that it should prepare a layer for the menu as follows:

```
nav {
transition: transform 0.1s;
transform-origin: 0% 0%;
will-change: transform;
}
nav[aria-hidden=true] {
transform: scaleY(0);
}
```


But you shouldn’t get too carried away. Like [the boy who cried wolf](https://en.wikipedia.org/wiki/The_Boy_Who_Cried_Wolf), if you decide to `will-change`

all the things, after a while the browser will start to ignore you. You’re better off to only apply `will-change`

to bigger elements that take longer to redraw, and only as needed. The [Web Console](https://developer.mozilla.org/docs/Tools/Web_Console) is your friend here, telling you when you’ve blown your `will-change`

budget, as shown below.

![Screenshot of the DevTools console showing a will-change over-budget warning.](../../assets/8fa2ff1d67fb867d.png)


## Animating like you just don’t care

Now that you know all about layers, we can finally get to the part where `Element.animate()`

shines. Putting the pieces together:

- By animating the right properties, we can avoid redoing layout on each frame.
- If we animate the
or`opacity`

properties, through the magic of layers we can often avoid redrawing them too.`transform`

- We can use
to let the browser know to get the layers ready in advance.`will-change`


But there’s a problem. It doesn’t matter how fast we prepare each animation frame if the part of the browser that’s in control is busy tending to other jobs like responding to events or running complicated scripts. We could finish up our animation frame in 5 milliseconds but it won’t matter if the browser then spends 50 milliseconds doing [ garbage collection](https://developer.mozilla.org/docs/Tools/Performance/Allocations#Allocations_and_garbage_collection). Instead of seeing silky smooth performance our animations will stutter along, destroying the illusion of motion and causing users’ blood pressure to rise.

However, if we have an animation that we know doesn’t change layout and perhaps doesn’t even need redrawing, it should be possible to let someone else take care of adjusting those layers on each frame. As it turns out, browsers already have a process designed precisely for that job — a separate thread or process known as the **compositor** that specializes in arranging and combining layers. All we need is a way to tell the compositor the whole story of the animation and let it get to work, leaving the main thread — that is, the part of the browser that’s doing everything else to run your app — to forget about animations and get on with life.

This can be achieved by using none other than the long-awaited [Element.animate()](https://developer.mozilla.org/docs/Web/API/Element/animate) API! Something like the following code is all you need to create a smooth animation that can run on the compositor:

```
elem.animate({ transform: [ 'rotate(0deg)', 'rotate(360deg)' ] },
{ duration: 1000, iterations: Infinity });
```


By being upfront about what you’re trying to do, the main thread will thank you by dealing with all your other scripts and event handlers in short order.

Of course, you can get the same effect by using [CSS Animations](https://developer.mozilla.org/docs/Web/CSS/CSS_Animations/Using_CSS_animations) and [CSS Transitions](https://developer.mozilla.org/docs/Web/CSS/CSS_Transitions/Using_CSS_transitions) — in fact, in browsers that support Web Animations, the same engine is also used to drive CSS Animations and Transitions — but for some applications, script is a better fit.

## Am I doing it right?

You’ve probably noticed that there are a few conditions you need to satisfy to achieve jank-free animations: you need to animate `transform`

or `opacity`

(at least for now), you need a layer, and you need to declare your animation up front. So how do you know if you’re doing it right?

The animation inspector in Firefox’s DevTools will give you a handy little lightning bolt indicator for animations running on the compositor. Furthermore, as of [Firefox 49](https://developer.mozilla.org/en-US/Firefox/Releases/49), the animation inspector can often tell you *why* your animation didn’t make the cut.

![Screenshot showing DevTools Animation inspector reporting why the transform property could not be animated on the compositor.](../../assets/ae1f13e3c78e8bea.png)


See the [relevant MDN article](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Work_with_animations#Further_information_about_animation_compositing) for more details about how this tool works.

*(Note that the result is not always correct — there’s a known bug where animations with a delay sometimes tell you that they’re not running on the compositor when, in fact, they are. If you suspect DevTools is lying to you, you can always include some long-running JavaScript in the page like in the first example in this post. If the animation continues on its merry way you know you’re doing it right — and, as a bonus, this technique will work in any browser.)*

Even if your animation doesn’t qualify for running on the compositor, there are still performance advantages to using `Element.animate()`

. For instance, you can avoid reparsing CSS properties on each frame, and allow the browser to apply other little tricks like ignoring animations that are currently offscreen, thereby prolonging battery life. Furthermore, you’ll be on board for whatever other performance tricks browsers concoct in the future (and there are many more of those coming)!

## Conclusion

With the release of [Firefox 48](https://developer.mozilla.org/en-US/Firefox/Releases/48), `Element.animate()`

is implemented in release versions of both Firefox and Chrome. Furthermore, there’s a [polyfill](https://github.com/web-animations/web-animations-js) (you’ll want the [ web-animations.min.js](https://github.com/web-animations/web-animations-js/blob/master/web-animations.min.js) version) that will fall back to using

[for browsers that don’t yet support](https://developer.mozilla.org/docs/Web/API/window/requestAnimationFrame)

`requestAnimationFrame`

`Element.animate()`

. In fact, if you’re using a framework like Polymer, you might already be using it!There’s a lot more to look forward to from the [Web Animations API](https://developer.mozilla.org/docs/Web/API/Web_Animations_API), but we hope you enjoy this first installment ([demos](https://mozdevs.github.io/Animation-examples/) and all)!

## About
[
Brian Birtles ](https://birtles.wordpress.com/)

Brian works on animations and layout in Firefox at Mozilla in Tokyo, Japan. He also edits the W3C Web Animations and CSS Animations specifications and has been trying to animate SVG for far too long. Despite his profile picture he is a big fan of the ocean and dreams of swimming or surfing to work.

## 9 comments

Simon TAugust 3rd, 2016 at 10:50Brian BirtlesAugust 3rd, 2016 at 16:11Simon TAugust 3rd, 2016 at 16:36Brian BirtlesAugust 3rd, 2016 at 16:40Christoph OAugust 6th, 2016 at 03:49Brian BirtlesAugust 8th, 2016 at 16:28Christoph OAugust 10th, 2016 at 00:31ClaireAugust 8th, 2016 at 02:25Brian BirtlesAugust 8th, 2016 at 16:29