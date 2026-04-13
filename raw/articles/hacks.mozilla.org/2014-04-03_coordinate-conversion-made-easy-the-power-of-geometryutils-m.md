---
title: Coordinate Conversion Made Easy – the power of GeometryUtils – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2014/04/coordinate-conversion-made-easy/
author: Roc
published: '2014-04-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In a [previous post](https://hacks.mozilla.org/2014/03/introducing-the-getboxquads-api/) we introduced the [GeometryUtils](http://dev.w3.org/csswg/cssom-view/#the-geometryutils-interface) interface and the `getBoxQuads()`

API for retrieving the CSS box geometry of a DOM node. GeometryUtils also takes care of another important problem: converting coordinates reliably from one DOM node to another. For example, you might want to find the bounding-box of one element relative to another element, or you might want to convert event coordinates from the viewport to some arbitrary element.

## Existing APIs

Until now, simple cases could be handled using `getBoundingClientRect()`

and some math, but complex cases (e.g. involving CSS transforms) were almost impossible to handle using standard APIs. The nonstandard APIs `webkitConvertPointToPage`

and `webkitConvertPageToPoint`

are a big improvement, but apart from not being standardized, they’re not as powerful as they need to be. In particular it’s more convenient and more robust to provide an API for directly converting coordinates from one element to another.[[1]](https://hacks.mozilla.org#note1)

## New APIs

`GeometryUtils`

introduces three new methods for coordinate conversion:

`to.convertPointFromNode(point, from)`

converts a a point relative to the top-left of the first border-box of “from” to a point relative to the top-left of the first border-box of “to”. The point is a`DOMPointInit`

, which means you can pass a`DOMPoint`

or a JS object such as`{x:0, y:0}`

.`to.convertRectFromNode(rect, from)`

converts a a`DOMRect`

relative to the top-left of the first border-box of “from” to a DOMQuad relative to the top-left of the first border-box of “to” by converting the vertices of the`DOMRect`

. It converts to a`DOMQuad`

to ensure that the result is accurate even if it needs to be rotated or skewed by CSS transforms.`to.convertQuadFromNode(quad, from)`

converts a`DOMQuad`

from “from” to “to”. It’s just like`convertRectFromNode`

except for taking a`DOMQuad`

.

As with `getBoxQuads`

, a node can be an `Element`

, `TextNode`

or `Document`

; when a `Document`

is used, the coordinates are relative to the document’s viewport.

Example:

```
```

```
var p1 = document.convertPointFromNode({
x:0, y:0
}, document.getElementById("e")
);
// p1.x == 100, p1.y == 100
var p2 = document.convertPointFromNode({
x:0, y:0
}, document.getElementById("d")
);
// p2.x == 150, p2.y == 150 - 50*sqrt(2) (approx)
p2 = document.getElementById("e").convertPointFromNode({
x:0, y:0
}, document.getElementById("d")
);
// p2.x == 50, p2.y == 50 - 50*sqrt(2) (approx)
var q1 = document.convertRectFromNode(
new DOMRect(0, 0, 50, 50),
document.getElementById("e")
);
// q1.p1.x == 100, q1.p1.y == 100
// q1.p2.x == 150, q1.p2.y == 100
// q1.p3.x == 150, q1.p3.y == 150
// q1.p4.x == 100, q1.p4.y == 150
var q2 = document.convertQuadFromNode(
new DOMQuad({
x:60, y:50
}, {
x:90, y:50
}, {
x:100, y:100
}, {
x:50, y:100
}),
document.getElementById("e")
);
// q2.p1.x == 100, q2.p1.y == 100
// q2.p2.x == 150, q2.p2.y == 100
// q2.p3.x == 140, q2.p3.y == 150
// q2.p4.x == 110, q2.p4.y == 150
```

Sometimes it’s useful to convert to or from an element’s CSS content-box, padding-box or margin-box. This is supported via an optional `ConvertCoordinateOptions`

dictionary with the following options:

`fromBox`

: one of`"content"`

,`"padding"`

,`"border"`

or`"margin"`

, selecting which CSS box of the first fragment of the`from`

node the input point(s) are relative to.`toBox`

: selects which CSS box of the first fragment of the`to`

node the returned point(s) are relative to.

As a special case, this makes it easy to convert points between different

CSS box types of the same element. For example, to convert a point from an

element’s border-box to be relative to its content-box, use

`element.convertPointFromNode(point, element, {toBox:"content"})`

.

Example:

```
```

```
var p1 = document.convertPointFromNode({
x:0, y:0
}, document.getElementById("e"),
{fromBox:"content"}
);
// p1.x == 120, p1.y == 120
p1 = document.getElementById("e").convertPointFromNode({
x:120, y:120
}, document,
{toBox:"content"}
);
// p1.x == 0, p1.y == 0
p1 = document.getElementById("e").convertPointFromNode({
x:0, y:0
}, document.getElementById("e"),
{fromBox:"content"}
);
// p1.x == 20, p1.y == 20
p1 = document.getElementById("e").convertPointFromNode({
x:20, y:20
}, document.getElementById("e"),
{toBox:"content"}
);
// p1.x == 0, p1.y == 0
```

These APIs are available in [Firefox nightly builds](http://nightly.mozilla.org/) and should be released in Firefox 31. Firefox is the first browser to implement these APIs.

#### Footnote

[[1]] Consider the following example:

```
...<>
...<>
```In this case, converting a point relative to `a`

to be relative to `b`

by converting first to page coordinates and then back to `b`

doesn’t work, because the `scale(0)`

maps every point in `a`

to a single point in the page.

## About
[
roc ](http://robert.ocallahan.org)

Robert O'Callahan is a distinguished engineer at Mozilla Corporation. Prior to joining MoCo he was a volunteer Mozilla contributor for several years (since 2000).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.