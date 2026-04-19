---
title: '16BPP.net: Blog / HTML5 Canvas Bindings for Nim''s JavaScript Target'
url: https://16bpp.net/blog/post/html5-canvas-bindings-for-nims-javascript-target
published: '2017-01-11'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

It seems like every one to two weeks I've been writing a new package for Nim. I've been playing around with the [JavaScript target](http://nim-lang.org/docs/nimc.html#backend-language-options). There is some basic stuff there in the [dom module](http://nim-lang.org/docs/dom.html) for HTML manipulation but I noticed something very important was missing; the `canvas`

tag. So well, [I added a thin wrapper for it](https://gitlab.com/define-private-public/HTML5-Canvas-Nim) ([GitHub mirror](https://github.com/define-private-public/HTML5-Canvas-Nim)). It's available under the `html5_canvas`

package in nimble.

When I first heard about HTML5 and read the spec a little, I think one of the most important things that was added was the `canvas`

tag, and along with it a JavaScript API for all sorts of drawing operations. Interactive content for the web that was being made with technologies like Flash and Java (applets) could now closer to the browser level (and have better performance to boot)!

The only thing is that I don't really like writing JS code; it's my least favorite language out there. But you know we live in a time where you don't have to write JavaScript to write JavaScript anymore! While Nim's JS backend is still marked as experimental I think that its nice enough where we can still make some cool stuff with it.

I tried to keep the API as close as possible to the one listed in [the Mozilla docs](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D). Though I did have to make a few changes. One of those in particular are the `fillStyle`

and `strokeStyle`

getters and setters. The problem with these two fields of `CanvasRenderingContext2D`

is that they can be one of any three different types ([see here](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fillStyle)). Nim being a strongly typed language wouldn't let me put those properties right under the `type ... object`

definition. Luckily though there is still a way to keep the API so it looks like we're setting a field instead of having to add a `setFillStyle()`

proc. Taken from the source, look a this:

proc `fillStyle=`*( ctx: CanvasRenderingContext2D; color: cstring ) {.inline.} = {.emit: [ctx, ".fillStyle=", color, ";"].} # Can do this now! ctx.fillStyle = rgb(255, 0, 255)

But as for the getters I had to do this:

proc fillStyleColor*(ctx: CanvasRenderingContext2D): cstring {.inline.} = {.emit: [result, "=", ctx, ".fillStyle;"].}

There's one for `Gradient`

and one for `Pattern`

as well.

For some extra fun, I ported over my [3D Canvas Cube from Dart](https://16bpp.net/blog/post/trying-out-dart) (another language that compiles to JS). I've put the source up in [my toybox repo](https://github.com/define-private-public/toybox/blob/master/nim_js/3d_canvas_cube/cube.nim). What's also pretty cool is that the compressed JS output from `dart2js`

was about 90 kilobytes, where as Nim's compressed JS is around 20 kilobytes! Originally when when did full imports (i.e. `import math`

) I was getting 124 KB compressed, but when I changed to selective imports (`from math import Pi, sin, cos, floor`

) I was able to drastically reduce the size.



I was able to get the animation to work by adding a mini proc to wrap JS's `setTimeout()`

function:

proc setTimeout(function: proc(); ms: float) = {.emit: ["setTimeout(", function, ",", ms, ");"].}

If you're bored with 2D graphics and want to do something 3D in Nim (and in the browser), take a look at stisa's nice [WebGL wrapper](https://github.com/stisa/webgl).

Here is the [link to the repo for this again](https://gitlab.com/define-private-public/HTML5-Canvas-Nim) ([GitHub mirror](https://github.com/define-private-public/HTML5-Canvas-Nim)). It's also on nimble under `html5_canvas`

. Have fun!