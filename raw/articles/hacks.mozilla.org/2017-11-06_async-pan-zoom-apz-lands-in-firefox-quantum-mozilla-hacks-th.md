---
title: Async Pan/Zoom (APZ) lands in Firefox Quantum – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/11/async-panzoom-apz-lands-in-firefox-quantum/
author: Belén Albeza
published: '2017-11-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Asynchronous pan and zoom (APZ) is landing** in Firefox Quantum, which means jank-free, **smooth scrolling** for all! We talked [about APZ in this earlier article](https://hacks.mozilla.org/2016/02/smoother-scrolling-in-firefox-46-with-apz/), but here’s a recap of how it works:

Until now, scrolling was part of the main JavaScript thread. This meant that when JavaScript code was being executed, the user could not scroll the page. With APZ, **scrolling is decoupled from the JavaScript thread**, and happens on its own, leading to a smoother scrolling experience, especially in slower devices, like mobile phones. There are some caveats, like [checkerboarding](https://hacks.mozilla.org/2016/02/smoother-scrolling-in-firefox-46-with-apz/), when scrolling happens faster than the browser is able to render the page, but even this is a reasonable trade-off for a better experience overall, in which the browser stays responsive and does not seem to hang or freeze.

In Firefox to date, we’ve gotten APZ working for some input methods (trackpad and mouse wheel), but in Quantum all of them will be supported, including touch and keyboard.

What does this mean for developers?

- The
`scroll`

event will have a short delay until it is triggered. - There are circumstances in which the browser has to disable APZ, but we can prevent some of them with our code.

## The scroll event

Without APZ, while the JavaScript thread is blocked, scrolling doesn’t occur and thus the `scroll`

event is not triggered. But now, with APZ, this scrolling happens regardless of whether or not the thread is blocked.

However, there is something we need to be aware of: now **there will be a delay** between the scrolling taking place and the scroll event being dispatched.

Usually this delay will be of a few frames only, but sometimes we can bypass it by using a pure CSS solution instead of JavaScript. Some common uses cases that rely on scrolling events are sticky banners, or parallax scrolling.

In the case of **sticky banners** –i.e., those which remain fixed the same position regardless of scrolling–, there is already a CSS property to achieve this, so there is no need to track user scrolling via JavaScript. Meet `position: sticky`

!

```
.banner {
position: -webkit-sticky;
position: sticky;
top: 0;
left: 0;
/* … */
}
```


Note: You can ![Sticky banner demo - screenshot](../../assets/c2598c7eecd47023.png)


[check out the live demo here](https://belen-albeza.github.io/scroll-demos/sticky.html).

**Parallax scrolling** is a popular effect in games, movies and animation. It creates the illusion of depth in a 2D environment by scrolling layers at different speeds. In the real world you can observe a similar effect when you are riding a vehicle: things that are closer to the road pass by really quickly (e.g. traffic signs, trees, etc.) whereas elements that are located further away move much more slowly (e.g. mountains, forests, etc.).

[In this demo](https://belen-albeza.github.io/scroll-demos/parallax.html), parallax scrolling is achieved with only CSS. If you scroll, you will see how objects belong to different “layers” that move at different speeds: a spaceship, text, stars…

The trick to achieve parallax scrolling with CSS uses a combination of `perspective`

and `translateZ`

. When `perspective`

has a value other than zero, translations over the Z axis will create the illusion of the element being closer to or further from the user. The further the element, the smaller it will appear and the slower it will move when the user scrolls. This is just what we need to achieve the parallax effect! To counter the “getting smaller” bit, we scale up the element.

```
.stars {
transform: translateZ(-4px) scale(5);
/* … */
}
```


It’s also important to note that `perspective`

must be applied to a container that wraps all the parallax layers, and not to the layers themselves:

```
.parallax-wrapper {
perspective: 1px;
/* … */
}
```


You can read more about these techniques in the [ Scroll linked effects page on MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Performance/Scroll-linked_effects), or this

[.](http://keithclark.co.uk/articles/pure-css-parallax-websites/)

*Pure CSS Parallax Websites*article## Preventing delaying of scrolling

Sometimes,** the browser needs to delay** or disable APZ because it doesn’t know whether a user action to initiate scrolling will be cancelled (for instance, by calling `preventDefault`

on a `wheel`

or touch event), or whether the user focus switches to an element that should get the input instead of scrolling. In these cases, scrolling is delayed so the browser can ensure consistency.

Note: Events that can delay scrolling by calling `preventDefault`

are: `wheel`

, `touchstart`

, `touchmove`

–plus the deprecated `DOMMouseScroll`

, `mousewheel`

and `mozMousePixelScroll`

.

For events, there are two potential solutions:

It is possible to **attach the event listener to the element that really needs it**, instead of listening globally with `document`

or `window`

. In this solution, APZ is delayed only when that element triggers the event, but does not affect the rest of the page.

Another potential solution is to **set the **`passive`

**flag to** `true`

**in the event listener.** By using this flag, we tell the browser that we will not call `preventDefault`

in the handler of that event, so it knows that scrolling *will* happen and does not need to wait until the callback is executed.

```
container.addEventListener('touchstart', function () {
// your handler here
}, { passive: true });
```


You can read more about this technique for [ improved scrolling performance](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#Improving_scrolling_performance_with_passive_listeners) on MDN.

Keep in mind that **APZ is very conservative in regards to keyboard input,** and will be disabled for this input method many times. For instance, a `click`

or `mousedown`

can potentially change the focus, and maybe the input via keyboard should get directed to the newly focused element (like a spacebar keystroke to a `<textarea>`

), instead of it being a scroll action. Unfortunately, there’s no coding workaround for these cases.

Altogether, I think that the experience that APZ provides for users is worth the small inconveniences, like the checkerboarding or the event delays. If you have any questions about APZ, feel free to leave a comment here!

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## One comment

strmNovember 6th, 2017 at 09:45