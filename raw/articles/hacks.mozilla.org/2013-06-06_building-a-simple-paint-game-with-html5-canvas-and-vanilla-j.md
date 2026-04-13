---
title: Building a simple paint game with HTML5 Canvas and Vanilla JavaScript – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/06/building-a-simple-paint-game-with-html5-canvas-and-vanilla-javascript/
author: Chris Heilmann
published: '2013-06-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When the talk is about HTML5 Canvas you mostly hear about libraries to make it work for legacy browsers, performance tricks like off-screen Canvas and ways to draw and animate sprites and tiles. This is only one part of Canvas, though. On the lowest level, Canvas is a way to manipulate pixels of a portion of the screen. Either via a painting API or by directly manipulating the pixel array (which by the way is a [typed array](http://www.khronos.org/registry/typedarray/specs/latest/) and thus performs admirably).

Using this knowledge, I thought it’d be fun to create a small game I saw in an ad for a tablet: a simple game for kids to paint letters. The result is a demo for FirefoxOS called [Letterpaint](http://codepo8.github.io/letterpaint/) which will show up soon on the [Marketplace](http://marketplace.mozilla.org/). The [code is on GitHub](https://github.com/codepo8/letterpaint/).

The fun thing about building Letterpaint was that I took a lot of shortcuts. Painting on a canvas is easy (and gets much easier using [Jacob Seidelin’s Canvas cheatsheet](http://blog.nihilogic.dk/2009/02/html5-canvas-cheat-sheet.html)), but on the first glance making sure that users stay in a certain shape is tricky. So is finding out how much of the letter has been filled in. However, by going back to seeing a Canvas as a collection of pixels, I found a simple way to make this work:

- When I paint the letter, I read out the amount of pixels that have the colour of the letter
- When you click the mouse button or touch the screen I test the colour of the pixel at the current mouse/finger position
- When the pixel is not transparent, you are inside the letter as the main Canvas by default is transparent
- When you release the mouse or stop touching the screen I compare the amount of pixels of the paint colour with the ones of the letter.

Simple, isn’t it? And it is all possible with two re-usable functions:

```
/*
getpixelcolour(x, y)
returns the rgba value of the pixel at position x and y
*/
function getpixelcolour(x, y) {
var pixels = cx.getImageData(0, 0, c.width, c.height);
var index = ((y * (pixels.width * 4)) + (x * 4));
return {
r: pixels.data[index],
g: pixels.data[index + 1],
b: pixels.data[index + 2],
a: pixels.data[index + 3]
};
}
/*
getpixelamount(r, g, b)
returns the amount of pixels in the canvas of the colour
provided
*/
function getpixelamount(r, g, b) {
var pixels = cx.getImageData(0, 0, c.width, c.height);
var all = pixels.data.length;
var amount = 0;
for (i = 0; i < all; i += 4) {
if (pixels.data[i] === r &&
pixels.data[i + 1] === g &&
pixels.data[i + 2] === b) {
amount++;
}
}
return amount;
}
```

Add some painting functions to that and you have the game done. You can see a [step by step guide of this online](http://codepo8.github.io/pixels-and-colours/) (and [pull the code from GitHub](https://github.com/codepo8/pixels-and-colours/)) and there is a screencast describing the tricks and decisions [on YouTube](http://www.youtube.com/watch?v=9rsDNifGods).

The main thing to remember here is that it is very tempting to reach for libraries and tools to get things done quickly, but that it could mean that you think too complex. Browsers have very powerful tools built in for us, and in many cases it means you just need to be up-to-date and fearless in trying something "new" that comes out-of-the-box.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 4 comments

Yannick L.June 6th, 2013 at 06:39Chris HeilmannJune 6th, 2013 at 07:15Tin Aung LinnJune 7th, 2013 at 04:59ArasJune 14th, 2013 at 00:53