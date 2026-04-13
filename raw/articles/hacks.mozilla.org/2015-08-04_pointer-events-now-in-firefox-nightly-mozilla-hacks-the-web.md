---
title: Pointer Events now in Firefox Nightly – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/08/pointer-events-now-in-firefox-nightly/
author: Matt Brubeck
published: '2015-08-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[**Important Update:** After this article was published, Pointer Events were [disabled in Firefox Nightly](https://bugzilla.mozilla.org/show_bug.cgi?id=1181564) because of a stability bug. They will be re-enabled after this bug is fixed. You can still test Pointer Events in Firefox by setting `dom.w3c_pointer_events.enabled`

to “true” in `about:config`

.]

This past February [Pointer Events](http://www.w3.org/TR/pointerevents/) became a W3C Recommendation. In the intervening time [Microsoft Open Tech](https://msopentech.com/) and [Mozilla](https://www.mozilla.org) have been working together to implement the specification. As consumers continue to expand the range of devices that are used to explore the web with different input mechanisms such as touch, pen or mouse, it is important to provide a unified API that developers can use within their applications. In this effort we have just reached a major milestone: Pointer events are now available in [Firefox Nightly](https://nightly.mozilla.org/). We are very excited about this effort which represents a great deal of cooperation across several browser vendors in an effort to produce a high quality industry standard API with growing support.

Be sure to download Firefox Nightly and give it a try and give us your feedback on the implementation either using the [dev-platform](https://lists.mozilla.org/listinfo/dev-platform) mailing list or the [mozilla.dev.platform](https://groups.google.com/forum/#!forum/mozilla.dev.platform) group. If you have feedback on the specification please send those to public-pointer-events@w3.org.

The intent of this specification is to expand the open web to support a variety of input mechanisms beyond the mouse, while maintaining compatibility with most web-based content, which is built around [mouse events](https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent). The API is designed to create one solution that will handle a variety of input devices, with a focus on pointing devices (mouse, pens, and touch). The pointer is defined in the spec as a hardware-agnostic device that can target a specific set of screen coordinates. Pointer events are intentionally similar to the current set of events associated with mouse events.

In the current Nightly build, pointer events for mouse input are now supported. Additionally, if you’re using Windows, once you’ve set two preferences, touch events can be enabled now. The first property, Async Pan & Zoom ([APZ](https://wiki.mozilla.org/Platform/GFX/APZ)) is enabled by setting the `layers.async-pan-zoom.enabled`

Firefox [configuration preference](https://developer.mozilla.org/en-US/docs/Mozilla/Preferences/A_brief_guide_to_Mozilla_preferences#Modifying_preferences) to true. The `dom.w3c_touch_events.enabled`

should also be enabled by setting this value to 1 in your preferences.

This post covers some of the basic features of the new API.

## Using the Pointer API

Before getting started with the Pointer API, it’s important to test whether your current browser supports the API. This can be done with code similar to this example:

```
if (window.PointerEvent) {
.....
}else{
// use mouse events
}
```

The Pointer API provides support for `pointerdown, pointerup, pointercancel, pointermove, pointerover, pointerout, gotpointercapture,`

and `lostpointercapture`

events. Most of these should be familiar to you if you have coded event handling for mouse input before. For example, if you need a web app to move an image around a canvas when touched or clicked on, you can use the following code:

```
function DragImage() {
var imageGrabbed = false;
var ctx;
var cnv;
var myImage;
var x = 0;
var y = 0;
var rect;
this.imgMoveEvent = function(evt) {
if (imageGrabbed) {
ctx.clearRect(0, 0, cnv.width, cnv.height);
x = evt.clientX - rect.left;
y = evt.clientY - rect.top;
ctx.drawImage(myImage, x, y, 30, 30);
}
}
this.imgDownEvent = function(evt) {
//Could use canvas hit regions
var xcl = evt.clientX - rect.left;
var ycl = evt.clientY - rect.top;
if (xcl > x && xcl < x + 30 && ycl > y && ycl < y + 30) {
imageGrabbed = true;
}
}
this.imgUpEvent = function(evt) {
imageGrabbed = false;
}
this.initDragExample = function() {
if (window.PointerEvent) {
cnv = document.getElementById("myCanvas");
ctx = cnv.getContext('2d');
rect = cnv.getBoundingClientRect();
x = 0;
y = 0;
myImage = new Image();
myImage.onload = function() {
ctx.drawImage(myImage, 0, 0, 30, 30);
};
myImage.src = 'images/ff.jpg';
cnv.addEventListener("pointermove", this.imgMoveEvent, false);
cnv.addEventListener("pointerdown", this.imgDownEvent, false);
cnv.addEventListener("pointerup", this.imgUpEvent, false);
}
}
}
```

`PointerCapture`

events are used when there’s the possibility that a pointer device could leave the region of an existing element while tracking the event. For example, suppose you’re using a slider and your finger slips off the actual element –you’ll want to continue to track the pointer movements. You can set `PointerCapture`

by using code similar to this:

```
var myElement = document.getElementById("myelement");
myelement.addEventListener("pointerdown", function(e) {
if (this.setPointerCapture) {
//specify the id of the point to capture
this.setPointerCapture(e.pointerId);
}
}, false);
```

This code guarantees that you still get `pointermove`

events, even if you leave the region of `myelement`

. If you do not set the `PointerCapture`

, the pointer move events will not be called for the containing element once your pointer leaves its area. You can also release the capture by calling `releasePointerCapture`

. The browser does this automatically when a `pointerup`

or `pointercancel`

event occurs.

## The Pointer Event interface

The `PointerEvent`

interface extends the `MouseEvent`

interface and provides a few additional properties. These properties include `pointerId, width, height, pressure, tiltX, tiltY, pointerType`

and `isPrimary`

.

The `pointerId`

property provides a unique id for the pointer that initiates the event. The `height`

and `width`

properties provide respective values in CSS pixels for the contact geometry of the pointer. When the pointer happens to be a mouse, these values are set to 0. The `pressure`

property contains a floating point value from 0 to 1 to indicate the amount of pressure applied by the pointer, where 0 is the lowest and 1 is the highest. For pointers that do not support pressure, the value is set to 0.5.

The `tiltY`

property contains the angle value between the X-Z planes of the pointer and the screen and ranges between -90 and 90 degrees. This property is most useful when using a stylus pen for pointer operations. A value of 0 degrees would indicate the pointer touched the surface at an exact perpendicular angle with respect to the Y-axis. Likewise the `tiltX`

property contains the angle between the Y-Z planes.

The `pointType`

property contains the device type represented by the pointer. Currently this value will be set to `mouse, touch, pen, unknown`

or an empty string.

```
var myElement = document.getElementById("myelement");
myElement.addEventListener("pointerdown", function(e) {
switch(e.pointerType) {
case "mouse":
console.log("Mouse Pointer");
break;
case "pen":
console.log("Pen Pointer");
break;
case "touch":
console.log("Touch Pointer");
break;
default:
console.log("Unknown Pointer");
}
}, false);
```

The `isPrimary`

property is either `true`

or `false`

and indicates whether the pointer is the primary pointer. A primary pointer property is required when supporting multiple touch points to provide multi-touch input and gesture support. Currently this property will be set to `true`

for each specific pointer type (mouse, touch, pen) when the pointer first makes contact with an element that is tracking pointer events. If you are using one touch point and a mouse pointer simultaneously both will be set to `true`

. The `isPrimary`

property will be set to `false`

for an event if a different pointer is already active with the same `pointerType`

.

```
var myElement = document.getElementById("myelement");
myelement.addEventListener("pointerdown", function(e) {
if( e.pointerType == "touch" ){
if( e.isPrimary ){
//first touch
}else{
//handle multi-touch
}
}
}, false);
```

## Handling multi-touch

As stated earlier, touch pointers are currently implemented only for Firefox Nightly running on Windows with `layers.async-pan-zoom.enabled`

and `dom.w3c_touch_events.enabled`

preferences enabled. You can check to see whether multi-touch is supported with the following code.

```
if( window.maxTouchPoints && window.maxTouchPoints > 1 ){
//supports multi-touch
}
```

Some browsers provide default functionality for certain touch interactions such as scrolling with a swipe gesture, or using a pinch gesture for zoom control. When these default actions are used, the events for the pointer will not be fired. To better support different applications, Firefox Nightly supports the CSS property `touch-action`

. This property can be set to `auto, none, pan-x, pan-y`

, and `manipulation`

. Setting this property to `auto`

will not change any default behaviors of the browser when using touch events. To disable all of the default behaviors and allow your content to handle all touch input using pointer events instead, you can set this value to `none`

. Setting this value to either `pan-x`

or `pan-y`

invokes all pointer events when not panning/scrolling in a given direction. For instance, `pan-x`

will invoke pointer event handlers when not panning/scrolling in the horizontal direction. When the property is set to `manipulation`

, pointer events are fired if panning/scrolling or manipulating the zoom are not occurring.

```
// Very Simplistic pinch detector with little error detection,
// using only x coordinates of a pointer event
// Currently active pointers
var myPointers = [];
var lastDif = -1;
function myPointerDown(evt) {
myPointers.push(evt);
this.setPointerCapture(evt.pointerId);
console.log("current pointers down = " + myPointers.length);
}
//remove touch point from array when touch is released
function myPointerUp(evt) {
// Remove pointer from array
for (var i = 0; i < myPointers.length; i++) {
if (myPointers[i].pointerId == evt.pointerId) {
myPointers.splice(i, 1);
break;
}
}
console.log("current pointers down = " + myPointers.length);
if (myPointers.length < 2) {
lastDif = -1;
}
}
//check for a pinch using only the first two touchpoints
function myPointerMove(evt) {
// Update pointer position.
for (var i = 0; i < myPointers.length; i++) { if (evt.pointerId = myPointers[i].pointerId) { myPointers[i] = evt; break; } } if (myPointers.length >= 2) {
// Detect pinch gesture.
var curDif = Math.abs(myPointers[0].clientX - myPointers[1].clientX);
if (lastDif > 0) {
if (curDif > lastDif) { console.log("Zoom in"); }
if (curDif < lastDif) { console.log("Zoom out"); }
}
lastDif = curDif;
}
}
```

You can [test the example code here](http://limpet.net/pointer.html). For some great examples of the Pointer Events API in action, see [Patrick H. Lauke’s](http://www.splintered.co.uk/) collection of [Touch and Pointer Events experiments](https://patrickhlauke.github.io/touch/) on GitHub. Patrick is a member of the W3C Pointer Events Working Group, the W3C Touch Events Community Group, and Senior Accessibility Consultant for [The Paciello Group](http://www.paciellogroup.com/blog/2015/02/pointer-events-advance-to-w3c-recommendation/).

## Conclusion

In this post we covered some of the basics that are currently implemented in Firefox Nightly. To track the progress of this API, check out the [Gecko Touch Wiki page](https://wiki.mozilla.org/Gecko/Touch). You can also follow along on the main [feature bug](https://bugzilla.mozilla.org/show_bug.cgi?id=960316) and be sure to report any issues you find while testing the new Pointer API.

## 17 comments

Patrick H. LaukeAugust 4th, 2015 at 09:55Patrick H. LaukeAugust 4th, 2015 at 12:12Patrick H. LaukeAugust 4th, 2015 at 12:19FelixAugust 4th, 2015 at 15:18Matt BrubeckAugust 4th, 2015 at 15:55PabloAugust 5th, 2015 at 01:23Matt BrubeckAugust 5th, 2015 at 16:41PabloAugust 16th, 2015 at 07:16FredAugust 5th, 2015 at 05:14Matt BrubeckAugust 5th, 2015 at 16:38Code is double html escaped!August 5th, 2015 at 08:48Dan CallahanAugust 5th, 2015 at 10:17ecloudAugust 6th, 2015 at 05:19Matt BrubeckAugust 6th, 2015 at 10:43GeorgeAugust 8th, 2015 at 00:26Matt BrubeckAugust 8th, 2015 at 10:28NevilleAugust 9th, 2015 at 15:29