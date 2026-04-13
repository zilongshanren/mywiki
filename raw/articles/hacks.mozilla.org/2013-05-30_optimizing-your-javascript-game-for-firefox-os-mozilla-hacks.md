---
title: Optimizing your JavaScript game for Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/05/optimizing-your-javascript-game-for-firefox-os/
author: Louis Stowasser
published: '2013-05-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*When developing on a quad core processor with 16 gigabytes of RAM you can easily forget to consider how it will perform on a mobile device. This article will detail some best practices and things to consider for moving a game to Firefox OS or any similar hardware target.*

## Making the best of 256 Mb RAM/800 Mhz CPU

There are many areas of focus to keep in mind while developing a game. When your goal is to draw 60 times a second, garbage collection and inefficient drawing calls start to get in your way. Let’s start with the basics…

### Don’t over-optimize

This might sound counter-intuitive in an article about game optimization but optimization is the last step; performed on complete, working code. While it’s never a bad idea to keep these tips and tricks in mind, you don’t know whether you’ll need them until you’ve finished the game and played it on a device.

## Optimize Drawing

Drawing on [HTML5 2D canvas](https://developer.mozilla.org/en-US/docs/HTML/Canvas) is the biggest bottleneck in most JavaScript games, as all other updates are usually just algebra without touching the DOM. Canvas operations are hardware accelerated, which can give you some extra room to breath.

### Use whole-pixel rendering

Sub-pixel rendering occurs when you render objects on a canvas without whole values.

```
ctx.drawImage(myImage, 0.3, 0.5)
```

This causes the browser to do extra calculations to create the anti-aliasing effect. To avoid this, make sure to round all co-ordinates used in calls to `drawImage`

using `Math.floor`

or as you’ll reader further in the article, `bitwse`

operators.

### Cache drawing in an offscreen canvas

If you find yourself with complex drawing operations on each frame, consider creating an offscreen canvas, draw to it once (or whenever it changes) on the offscreen canvas, then on each frame draw the offscreen canvas.

```
myEntity.offscreenCanvas = document.createElement(“canvas”);
myEntity.offscreenCanvas.width = myEntity.width;
myEntity.offscreenCanvas.height = myEntity.height;
myEntity.offscreenContext = myEntity.offscreenCanvas.getContext(“2d”);
myEntity.render(myEntity.offscreenContext);
```

### Use moz-opaque on the canvas tag (Firefox Only)

If your game uses canvas and doesn’t need to be transparent, set the `moz-opaque`

attribute on the canvas tag. This information can be used internally to optimize rendering.

```
```

Described more in [Bug 430906 – Add moz-opaque attribute on canvas](https://bugzilla.mozilla.org/show_bug.cgi?id=430906).

### Scaling canvas using CSS3 transform

CSS3 transforms are faster by using the GPU. Best case is to not scale the canvas or have a smaller canvas and scale up rather than a bigger canvas and scale down. For Firefox OS, target 480 x 320 px.

```
var scaleX = canvas.width / window.innerWidth;
var scaleY = canvas.height / window.innerHeight;
var scaleToFit = Math.min(scaleX, scaleY);
var scaleToCover = Math.max(scaleX, scaleY);
stage.style.transformOrigin = "0 0"; //scale from top left
stage.style.transform = "scale(" + scaleToFit + ")";
```

See it working in [this jsFiddle](http://jsfiddle.net/digitarald/bYSkr/).

### Nearest-neighbour rendering for scaling pixel-art

Leading on from the last point, if your game is themed with pixel-art, you should use one of the following techniques when scaling the canvas. The default resizing algorithm creates a blurry effect and ruins the beautiful pixels.

```
canvas {
image-rendering: crisp-edges;
image-rendering: -moz-crisp-edges;
image-rendering: -webkit-optimize-contrast;
-ms-interpolation-mode: nearest-neighbor;
}
```

or

```
var context = canvas.getContext(‘2d’);
context.webkitImageSmoothingEnabled = false;
context.mozImageSmoothingEnabled = false;
context.imageSmoothingEnabled = false;
```

More documentation is available on [MDN for image-rendering](https://developer.mozilla.org/en-US/docs/CSS/image-rendering).

### CSS for large background images

If like most games you have a static background image, use a plain DIV element with a CSS background property and position it under the canvas. This will avoid drawing a large image to the canvas on every tick.

### Multiple canvases for layers

Similar to the last point, you may find you have some elements that are frequently changing and moving around whereas other things (like UI) never change. An optimization in this situation is to create layers using multiple canvas elements.

For example you could create a UI layer that sits on top of everything and is only drawn during user input. You could create game layer where the frequently updating entities exist and a background layer for entities that rarely update.



### Don’t scale images in drawImage

Cache various sizes of your images on an offscreen canvas when loading as opposed to constantly scaling them in drawImage.

### Be careful with heavy physics libraries

If possible, [roll your own physics](http://gamedev.tutsplus.com/series/custom-game-physics-engine/) as libraries like Box2D don’t perform well on low-end Firefox OS devices.

When [asm.js](http://asmjs.org/) support lands in Firefox OS, Emscripten-compiled libraries can take advantage of near-native performance. More reading in [Box2d Revisited](http://j15r.com/blog/2013/04/25/Box2d_Revisited).

### Use WebGL instead of Context 2D

Easier said than done but giving all the heavy graphics lifting to the GPU will free up the CPU for greater good. Even though WebGL is 3D, you can use it to draw 2D surfaces. There are some libraries out there that aim to abstract the drawing contexts.

## Minimize Garbage Collection

JavaScript can spoil us when it comes to memory management. We generally don’t need to worry about memory leaks or conservatively allocating memory. But if we’ve allocated too much and garbage collection occurs in the middle of a frame, that can take up valuable time and result in a visible drop in FPS.

### Pool common objects and classes

To minimise the amount of objects being cleaned during garbage collection, use a pre-initialised pool of objects and reuse them rather than creating new objects all the time.

#### Code example of generic object pool:



### Avoid internal methods creating garbage

There are various JavaScript methods that create new objects rather than modifying the existing one. This includes: `Array.slice`

, `Array.splice`

, `Function.bind`

.

#### Read more about JavaScript garbage collection

### Avoid frequent calls to localStorage

LocalStorage uses file IO and blocks the main thread to retrieve and save data. Use an in-memory object to cache the values of localStorage and even save writes for when the player is not mid-game.

#### Code example of an abstract storage object:



### Async localStorage API with IndexedDB

IndexedDB is a non-blocking API for storing data on the client but may be overkill for small and simple data. Gaia’s library to make localStorage API asynchronous, using IndexedDB is available on Github: [async_storage.js](https://github.com/mozilla-b2g/gaia/blob/master/shared/js/async_storage.js).

## Miscellaneous micro-optimization

Sometimes when you’ve exhausted all your options and it just won’t go any faster, you can try some micro-optimizations below. However do note that these only start to make a difference in heavy usage when every millisecond counts. Look for them in your hot game loops.

- Use
`x | 0`

instead of`Math.floor`

- Clear arrays with
`.length = 0`

to avoid creating a new Array - Sacrifice some CPU time to avoid creating garbage.
- Use
`if .. else`

over`switch`

[jsPerf – switch vs if-else](http://jsperf.com/switch-if-else)- Date.now() over (+ new Date)
[jsPerf – Date.now vs new Date().getTime() vs +new Date](http://jsperf.com/date-now-vs-new-date-gettime/2)- Or performance.now() for a sub-millisecond solution
- Use TypedArrays for floats or integers (e.g. vectors and matrices)
[gl-matrix – Javascript Matrix and Vector library for High Performance WebGL apps](https://github.com/toji/gl-matrix)

## Conclusion

Building for mobile devices and not-so-strong hardware is a good and creative exercise, and we hope you will want to make sure your games work well on all platforms!

## About
[
Louis Stowasser ](http://louisstowasser.com)

I am a Partner Engineer for Mozilla, maintainer of [Gamedev Weekly](http://gamedevweekly.com) and creator of the [CraftyJS](http://craftyjs.com) game engine, based in Brisbane Australia.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 12 comments

Maurizio LupoMay 30th, 2013 at 01:39Harald KirschnerMay 30th, 2013 at 09:06Rikard HerlitzMay 30th, 2013 at 02:27Harald KirschnerMay 30th, 2013 at 08:35AshleyMay 30th, 2013 at 05:02Harald KirschnerMay 30th, 2013 at 08:28André FiedlerMay 31st, 2013 at 00:23André FiedlerMay 30th, 2013 at 07:35Harald KirschnerMay 31st, 2013 at 11:20Jim McGinleyJune 5th, 2013 at 10:35EdJune 21st, 2013 at 00:36Rob WalchJune 22nd, 2013 at 15:08