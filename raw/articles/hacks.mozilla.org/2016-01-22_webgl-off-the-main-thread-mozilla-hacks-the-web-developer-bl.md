---
title: WebGL Off the Main Thread – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/01/webgl-off-the-main-thread/
author: Mozilla
published: '2016-01-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We’re happy to announce WebGL in Web Workers in Firefox 44+! Using the new [OffscreenCanvas API](https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas) you can now create a WebGL context off of the main thread.

To follow along, you’ll need a copy of Firefox 44 or newer (currently [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) or [Firefox Nightly](https://nightly.mozilla.org/)). You’ll have to enable this API by navigating to about:config in Firefox, searching for `gfx.offscreencanvas.enabled`

, and setting it to true. You can grab [the code examples from GitHub](https://github.com/nickdesaulniers/webgl-worker) or preview it [here](https://nickdesaulniers.github.io/webgl-worker/animation-worker.html) in Firefox 44+ with `gfx.offscreencanvas.enabled`

set to true. ~~This functionality is not yet available on Windows pending ANGLE support.~~ [AlteredQualia points out](https://twitter.com/alteredq/status/690595129854410753) things are running great on Windows/FF Nightly 46. Shame on me for not verifying!

## Use Cases

This API is the first that allows a thread other than the main thread to change what is displayed to the user. This allows rendering to progress no matter what is going on in the main thread. You can see more use cases in [the working group’s in-progress specification](https://wiki.whatwg.org/wiki/OffscreenCanvas#Use_Case_Description).

## Code Changes

Let’s take a look at [a basic example of WebGL animation](https://github.com/nickdesaulniers/RawWebGL/blob/gh-pages/examples/animation.html) from [my Raw WebGL talk](https://nickdesaulniers.github.io/RawWebGL/#/). We’ll port this code to run in a worker, rather than the main thread.

![WebGL in Workers](../../assets/274eb012246884ec.gif)


The first step is moving all of the code from WebGL context creation to draw calls into a separate file.

```
<script src="gl-matrix.js"></script>
<script>
// main thread
var canvas = document.getElementById('myCanvas');
...
gl.useProgram(program);
...
```


becomes:

```
// main thread
var canvas = document.getElementById('myCanvas');
if (!('transferControlToOffscreen' in canvas)) {
throw new Error('webgl in worker unsupported');
}
var offscreen = canvas.transferControlToOffscreen();
var worker = new Worker('worker.js');
worker.postMessage({ canvas: offscreen }, [offscreen]);
...
```


Recognize that we’re calling [HTMLCanvasElement.prototype.transferControlToOffscreen](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/transferControlToOffscreen), then transferring that to a newly constructed worker thread. `transferControlToOffscreen`

returns a new object which is an instance of [OffscreenCanvas](https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas), as opposed to [HTMLCanvasElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement). While similar, you can’t access properties like `offscreen.clientWidth`

and `offscreen.clientHeight`

, but you can access `offscreen.width`

and `offscreen.height`

. By passing it as the second argument to postMessage, we transfer ownership of the variable to the second thread.

Now in the worker thread, we’ll wait to receive the message from the main thread with the canvas element, before trying to get a WebGL context. The code for getting a WebGL context, creating and filling buffers, getting and setting attributes and uniforms, and drawing does not change.

```
// worker thread
importScripts('gl-matrix.js');
onmessage = function (e) {
if (e.data.canvas) {
createContext(e.data.canvas);
}
};
function createContext (canvas) {
var gl = canvas.getContext('webgl');
...
```


`OffScreenCanvas`

simply adds one new method to `WebGLRenderingContext.prototype`

called [commit](https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/commit). The commit method will push the rendered image to the canvas element that created the `OffscreenCanvas`

used by the WebGL context.

## Animation Synchronization

Now to get the code animating, we can proxy [requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame) timings from the main thread to the worker with postMessage.

```
// main thread
(function tick (t) {
worker.postMessage({ rAF: t });
requestAnimationFrame(tick);
})(performance.now());
```


and onmessage in the worker becomes:

```
// worker thread
onmessage = function (e) {
if (e.data.rAF && render) {
render(e.data.rAF);
} else if (e.data.canvas) {
createContext(e.data.canvas);
}
};
```


and our render function now has a final [gl.commit();](https://github.com/nickdesaulniers/webgl-worker/blob/6094e270ead4db7ef216318a5ab0b0dca6a70722/worker.js#L75) statement rather than setting up another `requestAnimationFrame`

loop.

```
// main thread
function render (dt) {
// update
...
// render
gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
gl.drawArrays(gl.TRIANGLES, 0, n);
requestAnimationFrame(render);
};
```


becomes:

```
// worker thread
function render (dt) {
// update
...
// render
gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
gl.drawArrays(gl.TRIANGLES, 0, n);
gl.commit(); // new for webgl in workers
};
```


## Limitations with this approach

While in the example code, I’m not doing proper velocity-based animation (by not using the value passed from `requestAnimationFrame`

, I’m doing frame rate dependate animation, as opposed to the more correct velocity based animation which is frame rate independent), we still have an issue with this approach.

Assume we moved the rendering logic off of the main thread to avoid pauses from the JavaScript Virtual Machine’s Garbage Collector (GC pauses). GC pauses on the main thread will slow down invocations of `requestAnimationFrame`

. Since calls to `gl.drawArrays`

and `gl.commit`

are asynchronously triggered in the worker thread by postMessages in a `requestAnimationFrame`

loop on the main thread, GC pauses in the main thread will block rendering on the worker thread. Note: GC pauses in the main thread should not block progress in a worker thread (at least they don’t in Firefox’s [SpiderMonkey](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey) Virtual Machine). GC pauses are per Worker in SpiderMonkey.

While we could try to do something clever in the worker to account for this, the solution will be to make `requestAnimationFrame`

[available in a Worker context](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Functions_and_classes_available_to_workers). The bug tracking this work can be found [here](https://bugzilla.mozilla.org/show_bug.cgi?id=1203382).

## Summary

Developers will now be able to render to the screen without blocking on the main thread, thanks to the new OffscreenCanvas API. There’s still more work to do with getting `requestAnimationFrame`

on Workers. I was able to port existing WebGL code to run in a worker in a few minutes. For comparison, see [animation.html](https://github.com/nickdesaulniers/webgl-worker/blob/6094e270ead4db7ef216318a5ab0b0dca6a70722/animation.html) vs. [animation-worker.html](https://github.com/nickdesaulniers/webgl-worker/blob/6094e270ead4db7ef216318a5ab0b0dca6a70722/animation-worker.html) and [worker.js](https://github.com/nickdesaulniers/webgl-worker/blob/6094e270ead4db7ef216318a5ab0b0dca6a70722/worker.js).

## 6 comments

Brian GavinJanuary 24th, 2016 at 05:02ZimondaiJanuary 24th, 2016 at 17:45Morris TsengJanuary 27th, 2016 at 19:44Gordon RankinJanuary 28th, 2016 at 08:27Niels RoodJanuary 29th, 2016 at 03:10Alex BellFebruary 8th, 2016 at 12:49