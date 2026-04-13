---
title: interact.js for drag and drop, resizing and multi-touch gestures – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/11/interact-js-for-drag-and-drop-resizing-and-multi-touch-gestures/
author: Taye Adeyemi
published: '2014-11-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[interact.js](http://interactjs.io) is a JavaScript module for Drag and drop, resizing and multi-touch gestures with inertia and snapping for modern browsers (and also IE8+).

## Background

I started it as part of my [GSoC 2012 project](http://www.google-melange.com/gsoc/project/details/google/gsoc2012/taye/5668600916475904) for [Biographer](https://code.google.com/p/biographer)‘s network visualization tool. The tool was a web app which rendered to an SVG canvas and used jQuery UI for drag and drop, selection and resizing. Because jQuery UI has little support for SVG, heavy workarounds had to be used. I needed to make the web app more usable on smartphones and tablets and the largest chunk of this work was to replace jQuery UI with interact.js which:

- is lightweight,
- works well with SVG,
- handles multi-touch input,
- leaves the task of rendering/styling elements to the application and
- allows the application to supply object dimensions instead of parsing element styles or getting DOMRects.

What interact.js tries to do is present input data consistently across different browsers and devices and provide convenient ways to pretend that the user did something that they didn’t really do (snapping, inertia, etc.).

Certain sequences of user input can lead to `InteractEvent`

s being fired. If you add event listeners for an event type, that function is given an `InteractEvent`

object which provides pointer coordinates and speed and, in gesture events, scale, distance, angle, etc. The only time interact.js modifies the DOM is to style the cursor; making an element move while a drag happens has to be done from your own event listeners. This way you’re in control of everything that happens.

## Slider demo

Here’s an example of how you could make a slider with interact.js. You can view and edit the complete HTML, CSS and JS of all the demos in this post [on CodePen](http://codepen.io/collection/qwtdB/).

See the Pen [interact.js simple slider](http://codepen.io/taye/pen/FiDvj/) by Taye A ([@taye](http://codepen.io/taye)) on [CodePen](http://codepen.io).

### JavaScript rundown

```
interact('.slider') // target the matches of that selector
.origin('self') // (0, 0) will be the element's top-left
.restrict({drag: 'self'}) // keep the drag within the element
.inertia(true) // start inertial movement if thrown
.draggable({ // make the element fire drag events
max: Infinity // allow drags on multiple elements
})
.on('dragmove', function (event) { // call this function on every move
var sliderWidth = interact.getElementRect(event.target.parentNode).width,
value = event.pageX / sliderWidth;
event.target.style.paddingLeft = (value * 100) + '%';
event.target.setAttribute('data-value', value.toFixed(2));
});
interact.maxInteractions(Infinity); // Allow multiple interactions
```

`interact('.slider')`

[[docs]](http://interactjs.io/api/#interact)creates an`Interactable`

object which targets elements that match the`'.slider'`

CSS selector. An HTML or SVG element object could also have been used as the target but using a selector lets you use the same settings for multiple elements.`.origin('self')`

[[docs]](http://interactjs.io/api/#Interactable.origin)tells interact.js to modify the reported coordinates so that an event at the top-left corner of the target element would be`(0,0)`

.`.restrict({drag: 'self'})`

[[docs]](http://interactjs.io/api/#Interactable.restrict)keeps the coordinates within the area of the target element.`.inertia(true)`

[[docs]](http://interactjs.io/api/#Interactable.inertia)lets the user “throw” the target so that it keeps moving after the pointer is released.- Calling
`.draggable({max: Infinity})`

[[docs]](http://interactjs.io/api/#Interactable.draggable)on the object:- allows drag listeners to be called when the user drags from an element that matches the target and
- allows multiple target elements to be dragged simultaneously

`.on('dragmove', function (event) {...})`

[[docs]](http://interactjs.io/api/#Interactable.on)adds a listener for the`dragmove`

event. Whenever a`dragmove`

event occurs, all listeners for that event type that were added to the target Interactable are called. The listener function here calculates a value from 0 to 1 depending on which point along the width of the slider the drag happened. This value is used to position the handle.`interact.maxInteractions(Infinity)`

[[docs]](http://interactjs.io/api/#interact.maxInteractions)is needed to enable multiple interactions on any target. The default value is`1`

for backwards compatibility.

A lot of differences in browser implementations are resolved by interact.js. MouseEvents, TouchEvents and PointerEvents would produce identical drag event objects so this slider works on iOS, Android, Firefox OS and Windows RT as well as on desktop browsers as far back as IE8.

## Rainbow pixel canvas demo

interact.js is useful for more than moving elements around a page. Here I use it for drawing onto a canvas element.

See the Pen [interact.js pixel rainbow canvas](http://codepen.io/taye/pen/tCKAm/) by Taye A ([@taye](http://codepen.io/taye)) on [CodePen](http://codepen.io).

### JavaScript rundown

```
var pixelSize = 16;
interact('.rainbow-pixel-canvas')
.snap({
// snap to the corners of a grid
mode: 'grid',
// specify the grid dimensions
grid: { x: pixelSize, y: pixelSize }
})
.origin('self')
.draggable({
max: Infinity,
maxPerElement: Infinity
})
// draw colored squares on move
.on('dragmove', function (event) {
var context = event.target.getContext('2d'),
// calculate the angle of the drag direction
dragAngle = 180 * Math.atan2(event.dx, event.dy) / Math.PI;
// set color based on drag angle and speed
context.fillStyle = 'hsl(' + dragAngle + ', 86%, '
+ (30 + Math.min(event.speed / 1000, 1) * 50) + '%)';
// draw squares
context.fillRect(event.pageX - pixelSize / 2, event.pageY - pixelSize / 2,
pixelSize, pixelSize);
})
// clear the canvas on doubletap
.on('doubletap', function (event) {
var context = event.target.getContext('2d');
context.clearRect(0, 0, context.canvas.width, context.canvas.height);
});
function resizeCanvases () {
[].forEach.call(document.querySelectorAll('.rainbow-pixel-canvas'), function (canvas) {
canvas.width = document.body.clientWidth;
canvas.height = window.innerHeight * 0.7;
});
}
// interact.js can also add DOM event listeners
interact(document).on('DOMContentLoaded', resizeCanvases);
interact(window).on('resize', resizeCanvases);
interact.maxInteractions(Infinity);
```

[Snapping](http://interactjs.io/api/#Interactable.snap) is used to modify the pointer coordinates so that they are always aligned to a grid.

```
.snap({
// snap to the corners of a grid
mode: 'grid',
// specify the grid dimensions
grid: { x: pixelSize, y: pixelSize }
})
```

Like in the previous demo, multiple drags are enabled but an extra option, `maxPerElement`

, needs to be changed to allow multiple drags on the same element.

```
.draggable({
max: Infinity,
maxPerElement: Infinity
})
```

The movement angle is calculated with `Math.atan2(event.dx, event.dy)`

and that’s used to set the hue of the paint color. `event.speed`

is used to adjust the lightness.

interact.js has tap and double tap events which are equivalent to click and double click but without the delay on mobile devices. Also, unlike regular click events, a tap isn’t fired if the mouse is [moved before being released](https://bugzilla.mozilla.org/show_bug.cgi?id=319347). (I’m working on [adding more events](https://github.com/taye/interact.js/issues/95) like these).

```
// clear the canvas on doubletap
.on('doubletap', function (event) {
...
```

It can also listen for regular DOM events. In the above demo it’s used to listen for window resize and document DOMContentLoaded.

```
interact(document).on('DOMContentLoaded', resizeCanvases);
interact(window).on('resize', resizeCanvases);
```

Similar to jQuery, It can also be used for delegated events. For example:

```
interact('input', { context: document.body })
.on('keypress', function (event) {
console.log(event.key);
});
```

## Supplying element dimensions

To get element dimensions interact.js normally uses:

`Element#getBoundingClientRect()`

for SVGElements and`Element#getClientRects()[0]`

for HTMLElements (because it includes the element’s borders)

and adds page scroll. This is done when checking which action to perform on an element, checking for drops, calculating `'self'`

origin and in a few other places. If your application keeps the dimensions of elements that are being interacted with, then it makes sense to use the application’s data instead of getting the DOMRect. To allow this, `Interactable`

s have a `rectChecker()`

[ [docs]](http://interactjs.io/api/#Interactable.rectChecker) method to change how elements’ dimensions are gotten. The method takes a function as an argument. When interact.js needs an element’s dimensions, the element is passed to that function and the return value is used.

## Graphic Editor Demo

The “SVG editor” below has a `Rectangle`

class to represent `<rect class="edit-rectangle"/>`

elements in the DOM. Each rectangle object has dimensions, the element that the user sees and a draw method.

See the Pen [Interactable#rectChecker demo](http://codepen.io/taye/pen/xEJeo/) by Taye A ([@taye](http://codepen.io/taye)) on [CodePen](http://codepen.io).

### JavaScript rundown

```
var svgCanvas = document.querySelector('svg'),
svgNS = 'http://www.w3.org/2000/svg',
rectangles = [];
function Rectangle (x, y, w, h, svgCanvas) {
this.x = x;
this.y = y;
this.w = w;
this.h = h;
this.stroke = 5;
this.el = document.createElementNS(svgNS, 'rect');
this.el.setAttribute('data-index', rectangles.length);
this.el.setAttribute('class', 'edit-rectangle');
rectangles.push(this);
this.draw();
svgCanvas.appendChild(this.el);
}
Rectangle.prototype.draw = function () {
this.el.setAttribute('x', this.x + this.stroke / 2);
this.el.setAttribute('y', this.y + this.stroke / 2);
this.el.setAttribute('width' , this.w - this.stroke);
this.el.setAttribute('height', this.h - this.stroke);
this.el.setAttribute('stroke-width', this.stroke);
}
interact('.edit-rectangle')
// change how interact gets the
// dimensions of '.edit-rectangle' elements
.rectChecker(function (element) {
// find the Rectangle object that the element belongs to
var rectangle = rectangles[element.getAttribute('data-index')];
// return a suitable object for interact.js
return {
left : rectangle.x,
top : rectangle.y,
right : rectangle.x + rectangle.w,
bottom: rectangle.y + rectangle.h
};
})
```

Whenever interact.js needs to get the dimensions of one of the `'.edit-rectangle'`

elements, it calls the `rectChecker`

function that was specified. The function finds the Rectangle object using the element argument then creates and returns an appropriate object with `left`

, `right`

, `top`

and `bottom`

properties.

This object is used for restricting when the [restrict elementRect](https://github.com/taye/interact.js/pull/72) option is set. In the slider demo from earlier, restriction used only the pointer coordinates. Here, restriction will try to prevent the element from being dragged out of the specified area.

```
.inertia({
// don't jump to the resume location
// https://github.com/taye/interact.js/issues/13
zeroResumeDelta: true
})
.restrict({
// restrict to a parent element that matches this CSS selector
drag: 'svg',
// only restrict before ending the drag
endOnly: true,
// consider the element's dimensions when restricting
elementRect: { top: 0, left: 0, bottom: 1, right: 1 }
})
```

The rectangles are made draggable and resizable.

```
.draggable({
max: Infinity,
onmove: function (event) {
var rectangle = rectangles[event.target.getAttribute('data-index')];
rectangle.x += event.dx;
rectangle.y += event.dy;
rectangle.draw();
}
})
.resizable({
max: Infinity,
onmove: function (event) {
var rectangle = rectangles[event.target.getAttribute('data-index')];
rectangle.w = Math.max(rectangle.w + event.dx, 10);
rectangle.h = Math.max(rectangle.h + event.dy, 10);
rectangle.draw();
}
});
interact.maxInteractions(Infinity);
```

## Development and contributions

I hope this article gives a good overview of how to use interact.js and the types of applications that I think it would be useful for. If not, there are more demos on the [project homepage](http://interactjs.io/) and you can throw questions or issues at [Twitter](https://twitter.com/interactjs) or [Github](https://github.com/taye/interact.js/issues?q=is%3Aissue). I’d really like to make a comprehensive set of examples and documentation but I’ve been too busy with fixes and improvements. (I’ve also been too lazy :-P).

Since the 1.0.0 release, user comments and contributions have led to loads of bug fixes and many new features including:

So please use it, share it, break it and help to make it better!

## About
[
Taye Adeyemi ](http://taye.me)

Web developer with an interest in user interaction and interface design. Author of [interact.js](http://interactjs.io).
Currently studying Computer Science in Trinity College Dublin and keeping himself sane by working on open source projects, practising capoeira and learning Italian and German.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

Riccardo ForinaNovember 12th, 2014 at 08:47Taye AdeyemiNovember 12th, 2014 at 09:01