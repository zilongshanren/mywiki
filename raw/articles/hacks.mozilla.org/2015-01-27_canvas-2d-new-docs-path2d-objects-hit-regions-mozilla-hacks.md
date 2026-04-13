---
title: 'Canvas 2D: New docs, Path2D objects, hit regions – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2015/01/canvas-2d-new-docs-path2d-hit-regions/
author: Florian Scholz
published: '2015-01-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Over the last year, a couple of new HTML Canvas 2D features were implemented in Firefox and other recent browsers, with the help of the [Adobe Web platform team](http://blogs.adobe.com/webplatform/). Over on MDN, the [documentation for Canvas 2D](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) got a major update to reflect the current canvas standard and browser implementation status. Let’s have a look what is new and how you can use it to enhance your canvas graphics and gaming content.

`Path2D`

objects

The new `<a href="https://developer.mozilla.org/en-US/docs/Web/API/Path2D">Path2D</a>`

API (available from Firefox 31+) lets you store paths, which simplifies your canvas drawing code and makes it run faster. The [constructor](https://developer.mozilla.org/en-US/docs/Web/API/Path2D.Path2D) provides three ways to create a `Path2D`

object:

```
new Path2D(); // empty path object
new Path2D(path); // copy from another path
new Path2D(d); // path from from SVG path data
```

The third version, which takes [SVG path data](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths) to construct, is especially handy. You can now re-use your SVG paths to draw the same shapes directly on a canvas as well:

`var p = new Path2D("M10 10 h 80 v 80 h -80 Z");`

When constructing an empty path object, you can use the usual [path methods](https://developer.mozilla.org/en-US/docs/Web/API/Path2D#Methods), which might be familiar to you from using them directly on the `<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D">CanvasRenderingContext2D</a>`

context.

```
// create a circle
var circle = new Path2D();
circle.arc(50, 50, 50, 0, 2 * Math.PI);
// stroke the circle onto the context ctx
ctx.stroke(circle);
```

To actually draw the path onto the canvas, several APIs of the context have been updated to take an optional `Path2D`

path:

`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.fill">ctx.fill(path)</a>`

`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.stroke">ctx.stroke(path)</a>`

`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.clip">ctx.clip(path)</a>`

`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.isPointInPath">ctx.isPointInPath(path)</a>`

`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.isPointInStroke">ctx.isPointInStroke(path)</a>`


## Hit regions

Starting with Firefox 32, experimental support for [hit regions](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Hit_regions_and_accessibility#Hit_regions) has been added. You need to switch the `canvas.hitregions.enabled`

preference to `true`

in order to test them. Hit regions provide a much easier way to detect if the mouse is in a particular area without relying on manually checking coordinates, which can be really difficult to check for complex shapes. The Hit Region API is pretty simple:

`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.addHitRegion">CanvasRenderingContext2D.addHitRegion()</a>`

- Adds a hit region to the canvas.
`<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.removeHitRegion">CanvasRenderingContext2D.removeHitRegion()</a>`

- Removes the hit region with the specified
`id`

from the canvas. `<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.clearHitRegions">CanvasRenderingContext2D.clearHitRegions()</a>`

- Removes all hit regions from the canvas.

The `addHitRegion`

method, well, adds a hit region to a current path or a `Path2D`

path. The `<a href="https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent">MouseEvent</a>`

interface got extended with a `<a href="https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent.region">region</a>`

property, which you can use to check whether the mouse hit the region or not.

Check out the [code example on MDN](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.addHitRegion#Using_the_addHitRegion_method) to see it in action (and be sure to enable flags/preferences in at least Firefox and Chrome).

## Focus rings

Also in Firefox 32, the `<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.drawFocusIfNeeded">drawFocusIfNeeded(element)</a>`

property has been made available without a preference switch. This API allows you to draw focus rings on a canvas, if a provided fallback element inside the `<canvas></canvas>`

element gains focus. If the fallback element gets focused (for example when tabbing through the page that contains the canvas), the pixel representation / shape of that element on the canvas can draw a focus ring to indicate the current focus.

## CSS/SVG filters exposed to Canvas

Although still behind a preference (`canvas.filters.enabled`

), and not yet in the latest canvas specification (but expected to be added), Firefox 35 gained support for[ filters on the canvas rendering context](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.filter). The syntax is the same as the [CSS filter property](https://developer.mozilla.org/en-US/docs/Web/CSS/filter).

## Misc

- The
is now implemented (Firefox 30). An opaque canvas can`alpha`

context attribute[speed things up](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas)! - You can now
[add transformations to patterns](https://developer.mozilla.org/en-US/docs/Web/API/CanvasPattern.setTransform)(Firefox 33). `<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D.resetTransform">ctx.resetTransform()</a>`

to reset transformations has been added (Firefox 36).- More coming! The latest canvas specification contains some new APIs and their implementation in browsers
[is](https://code.google.com/p/chromium/issues/detail?id=281529)[underway](https://bugzilla.mozilla.org/show_bug.cgi?id=1119470).

## Documentation

If you would like to read more about Canvas 2D graphics, check out the [Canvas tutorial on MDN](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial), which guides you through the[ Canvas APIs](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API). A good bookmark is also the large `<a href="https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D">CanvasRenderingContext2D</a>`

interface, which you will use often when working with Canvas.

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.