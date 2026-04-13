---
title: Introducing the getBoxQuads API – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/03/introducing-the-getboxquads-api/
author: Roc
published: '2014-03-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Web developers often need to determine where an element has been placed in the page, or more generally, where it is relative to another element. Existing APIs for doing this have significant limitations. The new [GeometryUtils](http://dev.w3.org/csswg/cssom-view/#the-geometryutils-interface) interface and its supporting interfaces [DOMPoint](http://dev.w3.org/fxtf/geometry/Overview.html#DOMPoint), [DOMRect](http://dev.w3.org/fxtf/geometry/Overview.html#DOMRect) and [DOMQuad](http://dev.w3.org/fxtf/geometry/Overview.html#DOMQuad) provide Web-standard APIs to address these problems. Firefox is the first browser to implement these APIs; they are available in [Firefox 31 Nightly](http://nightly.mozilla.org/) builds.

## Current best standardized APIs for retrieving element geometry

Currently the best standardized DOM APIs for retrieving element geometry are `element.getBoundingClientRect()`

and `element.getClientRects()`

. These return the border-box rectangle(s) for an element relative to the viewport of the containing document. These APIs are supported cross-browser but have several limitations:

- When complex CSS transforms are present, they return the smallest axis-aligned rectangle enclosing the transformed border-box. This loses information.
- There is no way to obtain the coordinates of the content-box, padding-box or border-box. In simple cases you can add or subtract computed style values from the results of
`getBoundingClientRect()`

/`getClientRects()`

but this is clumsy and difficult to get right. For example, when a <span> breaks into several fragments, its left border is only added to one of the fragments — either the first or the last, depending on the directionality of the text. - There is no way to obtain box geometry relative to another element.

## Introducing getBoxQuads()

The `GeometryUtils.getBoxQuads()`

method, implemented on `Document`

, `Element`

and `TextNode`

, solves these problems. It returns a list of `DOMQuad`

s, one for each CSS fragment of the object (normally this list would just have a single

`DOMQuad`

).

Example:

```
```

```
var quads = document.getElementById("d").getBoxQuads();
// quads.length == 1
// quads[0].p1.x == 100
// quads[0].p1.y == 100
// quads[0].p3.x == 200
// quads[0].p3.y == 200
```

### Using bounds

A `DOMQuad`

is a collection of four `DOMPoint`

s defining the corners of an arbitrary quadrilateral. Returning `DOMQuad`

s lets `getBoxQuads()`

return accurate information even when arbitrary 2D or 3D transforms are present. It has a handy `bounds`

attribute returning a `DOMRectReadOnly`

for those cases where you just want an axis-aligned bounding rectangle.

For example:

```
```

```
var quads = document.getElementById("d").getBoxQuads();
// quads[0].p1.x == 150
// quads[0].p1.y == 150 - 50*sqrt(2) (approx)
// quads[0].p3.x == 150
// quads[0].p3.y == 150 + 50*sqrt(2) (approx)
// quads[0].bounds.width == 100*sqrt(2) (approx)
```

### Passing in options

By default `getBoxQuads()`

returns border-boxes relative to the node’s document viewport, but this can be customized by passing in an optional

options dictionary with the following (optional) members:

`box`

: one of`"content"`

,`"padding"`

,`"border"`

or`"margin"`

, selecting which CSS box type to return.`relativeTo`

: a`Document`

,`Element`

or`TextNode`

;`getBoxQuads()`

returns coordinates relative to the top-left of the border-box of that node (the border-box of the first fragment, if there’s more than one fragment). For documents, the origin of the document’s viewport is used.

Example:

```
```

```
var quads = document.getElementById("e").getBoxQuads({
relativeTo:document.getElementById("d")
});
// quads[0].p1.x == 0
// quads[0].p1.y == 0
quads = document.getElementById("e").getBoxQuads({
relativeTo:document.getElementById("d"),
box:"content"
});
// quads[0].p1.x == 20
// quads[0].p1.y == 20
```

The `relativeTo`

node need not be an ancestor of the node receiving `getBoxQuads()`

. The nodes can even be in different documents, although they must be in the same toplevel browsing context (i.e. browser tab).

## Scratching the surface

If you’ve read this far, you’re probably observant enough to have noticed additional methods in GeometryUtils — methods for coordinate conversion. These will be covered in a future blog post.

## About
[
roc ](http://robert.ocallahan.org)

Robert O'Callahan is a distinguished engineer at Mozilla Corporation. Prior to joining MoCo he was a volunteer Mozilla contributor for several years (since 2000).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 10 comments

Aditya BhattMarch 27th, 2014 at 03:04Robert Nyman [Editor]March 28th, 2014 at 07:52PhistucKMarch 27th, 2014 at 12:48Robert Nyman [Editor]March 28th, 2014 at 09:57PhistucKMarch 28th, 2014 at 09:59ArasMarch 27th, 2014 at 15:52Robert O’CallahanMarch 28th, 2014 at 08:31Mikael GramontApril 2nd, 2014 at 21:47thinsoldierApril 3rd, 2014 at 14:27Robert O’CallahanApril 10th, 2014 at 21:00