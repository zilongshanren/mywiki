---
title: WebGL & CreateJS for Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/01/webgl-createjs-for-firefox-os/
author: Louis Stowasser
published: '2014-01-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post by the developers at gskinner. Mozilla has been working with the CreateJS.com team at gskinner to bring new features to their open-source libraries and make sure they work great on Firefox OS.*

Here at [gskinner](http://www.gskinner.com/), it’s always been our philosophy to contribute our solutions to the dev community — the last four years of which have been focused on web-standards in HTML and Javascript. Our [CreateJS](http://www.createjs.com/) libraries provide approachable, modular, cross-browser-and-platform APIs for building rich interactive experiences on the open, modern web. We think they’re awesome.

For example, the [CreateJS CDN](http://code.createjs.com/) typically receives hundreds of millions of impressions per month, and Adobe has selected CreateJS as their official framework for creating HTML5 documents in [Flash Professional CC](http://www.adobe.com/products/flash.html).

Firefox OS is a perfect fit for CreateJS content. It took us little effort to ensure that the latest libraries are supported and are valuable tools for app and game creation on the platform.

We’re thrilled to welcome Mozilla as an official sponsor of CreateJS, along with some exciting announcements about the libraries!

## WebGL

As WebGL becomes more [widely supported](http://caniuse.com/webgl) in browsers, we’re proud to announce that after working in collaboration with Mozilla, a shiny new WebGL renderer for EaselJS is now in early beta! Following research, internal discussions, and optimizations, we’ve managed to pump out a renderer that draws a subset of 2D content anywhere from 6x to 50x faster than is currently possible on the Canvas 2D Context. It’s fully supported in both the browser and in-app contexts of Firefox OS.

We thought about what we wanted to gain from a WebGL renderer, and narrowed it down to three key goals:

- Very fast performance for drawing sprites and bitmaps
- Consistency and integration with the existing EaselJS API
- The ability to fall back to Context2D rendering if WebGL is not available

Here’s what we came up with:

## SpriteStage and SpriteContainer

Two new classes, SpriteStage and SpriteContainer, enforce restrictions on the display list to enable aggressively optimized rendering of bitmap content. This includes images, spritesheet animations, and bitmap text. SpriteStage is built to automatically make additional draw calls per frame as needed, avoiding any fixed maximum on the number of elements that can be included in a single draw call.

These new classes extend existing EaselJS classes (Stage and Container), so creating WebGL content is super simple if you’re familiar with EaselJS. Existing content using EaselJS can be WebGL-enabled with a few keystrokes.

## Layering Renderers

This approach allows WebGL and Context2D content to be layered on screen, and mouse/touch interactions can pass seamlessly between the layers. For example, an incredibly fast game engine using WebGL rendering can be displayed under a UI layer that leverages the more robust capabilities of the Context2D renderer. You can even swap assets between a WebGL and Context2D layer.

Finally, WebGL content is fully compatible with the existing Context2D renderer. On devices or browsers that don’t support WebGL, your content will automatically be rendered via canvas 2D.

While it took some work to squeeze every last iota of performance out of the new renderer, we’re really happy with this new approach. It allows developers to build incredibly high performance content for a wide range of devices, and also leverage the extremely rich existing API and toolchain surrounding CreateJS. Below, you’ll find a few demos and links that show off its capabilities.

## Example: Bunnymark

A very popular (though limited) benchmark for web graphics is Bunnymark. This benchmark simply measures the maximum number of bouncing bunny bitmap sprites (try saying that 5 times fast) a renderer can support at 60fps.

![Bunnymark](../../assets/f5b9d1c4e6a28368.png)


The following table compares Bunnymark scores using the classic Context2D renderer and the new WebGL renderer. Higher numbers are better.

| Environment | Context2D | WebGL | Change |
|---|---|---|---|
| 2012 Macbook Pro, Firefox 26 | 900 | 46,000 | 51x |
| 2012 Macbook Pro, Chrome 31 | 2,300 | 60,000 | 26x |
| 2012 Win 7 laptop, IE11 (x64 NVIDIA GeForce GT 630M, 1 GB VRAM) | 1,900 | 9,800 | 5x |
| Firefox OS 1.2.0.0-prerelease (early 1.2 device) | 45 | 270 | 6x |
| Nexus 5, Firefox 26 | 225 | 4,400 | 20x |
| Nexus 5, Chrome 31 | 230 | 4,800 | 21x |

Since these numbers show maximum sprites at 60fps, the above numbers can increase significantly if a lower framerate is allowed. It’s worth noting that the only Firefox OS device we have in house is an early Firefox OS 1.2 device (has a relatively low-powered GPU), yet we’re still seeing significant performance gains.

## Example: Sparkles Benchmark

This very simple demo was made to test the limits of how many particles could be put on screen while pushing the browser to 24fps.

![Sparkles](../../assets/bb3f1427ebbfd2fb.png)


## Example: Planetary Gary

We often use the Planetary Gary game demo as a test bed for new capabilities in the CreateJS libraries. In this case, we retrofitted the existing game to use the new SpriteStage and SpriteContainer classes for rendering the game experience in WebGL.

![Planetary Gary](../../assets/73e3a4b5418a1617.jpg)


This was surprisingly easy to do, requiring only three lines of changed or added code, and demonstrates the ease of use, and consistency of the new APIs. It’s a particularly good example because it shows how the robust feature set of the Context2D renderer can be used for user interface elements (ex. the start screen) in cooperation with the superior performance of the WebGL renderer (ex. the game).

Even better, the game art is packaged as vector graphics, which are drawn to sprite sheets via the Context2D renderer at run time (using EaselJS’s [SpriteSheetBuilder](http://www.createjs.com/Docs/EaselJS/classes/SpriteSheetBuilder.html)), then passed to the WebGL renderer. This allows for completely scaleable graphics with minimal file size (~85kb over the wire) and incredible performance!

## Roadmap

We’ve posted a [public preview](https://github.com/CreateJS/EaselJS) of the new WebGL renderer on GitHub to allow the community to take it for a test drive and [provide feedback](http://community.createjs.com/discussions/easeljs). Soon it will be included it in the next major release.

Follow [@createjs](https://twitter.com/createjs) and [@gskinner](https://twitter.com/gskinner) on twitter to stay up to date with the latest news and let us know what you think — thanks for reading!

## About
[
Louis Stowasser ](http://louisstowasser.com)

I am a Partner Engineer for Mozilla, maintainer of [Gamedev Weekly](http://gamedevweekly.com) and creator of the [CraftyJS](http://craftyjs.com) game engine, based in Brisbane Australia.

## 6 comments

daf182January 17th, 2014 at 09:41heinzJanuary 18th, 2014 at 05:40jean-michelJanuary 19th, 2014 at 07:30TrevorJanuary 28th, 2014 at 08:52Italo PortinhoFebruary 4th, 2014 at 11:52TrevorFebruary 4th, 2014 at 15:39