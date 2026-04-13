---
title: Faster Canvas Pixel Manipulation with Typed Arrays – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2011/12/faster-canvas-pixel-manipulation-with-typed-arrays/
author: Paul Rouget
published: '2011-12-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Edit: See the section about [ Endiannes](https://hacks.mozilla.org#endiannes).

[Typed Arrays](https://developer.mozilla.org/en/JavaScript_typed_arrays) can significantly increase the pixel manipulation performance of your HTML5 2D canvas Web apps. This is of particular importance to developers looking to use HTML5 for making browser-based games.

This is a guest post by [Andrew J. Baker](https://twitter.com/#!/andrew_j_baker2). Andrew is a professional software engineer currently working for [Ibuildings UK](http://www.ibuildings.co.uk/) where his time is divided equally between front- and back-end enterprise Web development. He is a principal member of the [browser-based games channel #bbg on Freenode](http://hashbbg.com/), spoke at the first HTML5 games conference in September 2011, and is a scout for Mozilla’s WebFWD innovation accelerator.

Eschewing the higher-level methods available for drawing images and primitives to a canvas, we’re going to get down and dirty, manipulating pixels using ImageData.

## Conventional 8-bit Pixel Manipulation

The following example demonstrates pixel manipulation using image data to generate a greyscale moire pattern on the canvas.

Let’s break it down.

First, we obtain a reference to the canvas element that has an id attribute of *canvas* from the DOM.

```
var canvas = document.getElementById('canvas');
```

The next two lines might appear to be a micro-optimisation and in truth they are. But given the number of times the canvas width and height is accessed within the main loop, copying the values of `canvas.width`

and `canvas.height`

to the variables `canvasWidth`

and `canvasHeight`

respectively, can have a noticeable effect on performance.

```
var canvasWidth = canvas.width;
var canvasHeight = canvas.height;
```

We now need to get a reference to the 2D context of the canvas.

```
var ctx = canvas.getContext('2d');
```

Armed with a reference to the 2D context of the canvas, we can now obtain a reference to the canvas’ image data. Note that here we get the image data for the entire canvas, though this isn’t always necessary.

```
var imageData = ctx.getImageData(0, 0, canvasWidth, canvasHeight);
```

Again, another seemingly innocuous micro-optimisation to get a reference to the raw pixel data that can also have a noticeable effect on performance.

```
var data = imageData.data;
```

Now comes the main body of code. There are two loops, one nested inside the other. The outer loop iterates over the y axis and the inner loop iterates over the x axis.

```
for (var y = 0; y < canvasHeight; ++y) {
for (var x = 0; x < canvasWidth; ++x) {
```

We draw pixels to image data in a top-to-bottom, left-to-right sequence. Remember, the y axis is inverted, so the origin (0,0) refers to the top, left-hand corner of the canvas.

The *ImageData.data* property referenced by the variable *data* is a one-dimensional array of integers, where each element is in the range 0..255. *ImageData.data* is arranged in a repeating sequence so that each element refers to an individual channel. That repeating sequence is as follows:

```
data[0] = red channel of first pixel on first row
data[1] = green channel of first pixel on first row
data[2] = blue channel of first pixel on first row
data[3] = alpha channel of first pixel on first row
data[4] = red channel of second pixel on first row
data[5] = green channel of second pixel on first row
data[6] = blue channel of second pixel on first row
data[7] = alpha channel of second pixel on first row
data[8] = red channel of third pixel on first row
data[9] = green channel of third pixel on first row
data[10] = blue channel of third pixel on first row
data[11] = alpha channel of third pixel on first row
...
```

Before we can plot a pixel, we must translate the x and y coordinates into an index representing the offset of the first channel within the one-dimensional array.

```
var index = (y * canvasWidth + x) * 4;
```

We multiply the y coordinate by the width of the canvas, add the x coordinate, then multiply by four. We must multiply by four because there are four elements per pixel, one for each channel.

Now we calculate the colour of the pixel.

To generate the moire pattern, we multiply the x coordinate by the y coordinate then bitwise AND the result with hexadecimal 0xff (decimal 255) to ensure that the value is in the range 0..255.

```
var value = x * y & 0xff;
```

Greyscale colours have red, green and blue channels with identical values. So we assign the same value to each of the red, green and blue channels. The sequence of the one-dimensional array requires us to assign a value for the red channel at index, the green channel at index + 1, and the blue channel at index + 2.

```
data[index] = value; // red
data[++index] = value; // green
data[++index] = value; // blue
```

Here we're incrementing index, as we recalculate it with each iteration, at the start of the inner loop.

The last channel we need to take into account is the alpha channel at index + 3. To ensure that the plotted pixel is 100% opaque, we set the alpha channel to a value of 255 and terminate both loops.

```
data[++index] = 255; // alpha
}
}
```

For the altered image data to appear in the canvas, we must put the image data at the origin (0,0).

```
ctx.putImageData(imageData, 0, 0);
```

Note that because *data* is a reference to *imageData.data*, we don't need to explicitly reassign it.

## The ImageData Object

At time of writing this article, the HTML5 specification is still in a state of flux.

Earlier revisions of the HTML5 specification declared the ImageData object like this:

```
interface ImageData {
readonly attribute unsigned long width;
readonly attribute unsigned long height;
readonly attribute CanvasPixelArray data;
}
```

With the introduction of typed arrays, the type of the data attribute has altered from CanvasPixelArray to Uint8ClampedArray and now looks like this:

```
interface ImageData {
readonly attribute unsigned long width;
readonly attribute unsigned long height;
readonly attribute Uint8ClampedArray data;
}
```

At first glance, this doesn't appear to offer us any great improvement, aside from using a type that is also used elsewhere within the HTML5 specification.

But, we're now going to show you how you can leverage the increased flexibility introduced by deprecating CanvasPixelArray in favour of Uint8ClampedArray.

Previously, we were forced to write colour values to the image data one-dimensional array a single channel at a time.

Taking advantage of typed arrays and the ArrayBuffer and ArrayBufferView objects, we can write colour values to the image data array an entire pixel at a time!

## Faster 32-bit Pixel Manipulation

Here's an example that replicates the functionality of the previous example, but uses unsigned 32-bit writes instead.

NOTE: If your browser doesn't use Uint8ClampedArray as the type of the data property of the ImageData object, this example won't work!

The first deviation from the original example begins with the instantiation of an ArrayBuffer called *buf*.

```
var buf = new ArrayBuffer(imageData.data.length);
```

This ArrayBuffer will be used to temporarily hold the contents of the image data.

Next we create two ArrayBuffer views. One that allows us to view *buf* as a one-dimensional array of unsigned 8-bit values and another that allows us to view *buf* as a one-dimensional array of unsigned 32-bit values.

```
var buf8 = new Uint8ClampedArray(buf);
var data = new Uint32Array(buf);
```

Don't be misled by the term 'view'. Both *buf8* and *data* can be read from **and** written to. More [information about ArrayBufferView](https://developer.mozilla.org/en/JavaScript_typed_arrays/ArrayBufferView) is available on MDN.

The next alteration is to the body of the inner loop. We no longer need to calculate the index in a local variable so we jump straight into calculating the value used to populate the red, green, and blue channels as we did before.

Once calculated, we can proceed to plot the pixel using only one assignment. The values of the red, green, and blue channels, along with the alpha channel are packed into a single integer using bitwise left-shifts and bitwise ORs.

```
data[y * canvasWidth + x] =
(255 << 24) | // alpha
(value << 16) | // blue
(value << 8) | // green
value; // red
}
}
```

Because we're dealing with unsigned 32-bit values now, there's no need to multiply the offset by four.

Having terminated both loops, we must now assign the contents of the ArrayBuffer *buf* to *imageData.data*. We use the Uint8ClampedArray.set() method to set the *data* property to the Uint8ClampedArray view of our ArrayBuffer by specifying *buf8* as the parameter.

```
imageData.data.set(buf8);
```

Finally, we use putImageData() to copy the image data back to the canvas.

## Testing Performance

We've told you that using typed arrays for pixel manipulation is faster. We really should test it though, and that's what [this jsperf test](http://jsperf.com/canvas-pixel-manipulation) does.

At time of writing, 32-bit pixel manipulation is indeed faster.

## Wrapping Up

There won't always be occasions where you need to resort to manipulating canvas at the pixel level, but when you do, be sure to check out typed arrays for a potential performance increase.

[EDIT]: Endianness

As has quite rightly been highlighted in the comments, the code originally presented does not correctly account for the [endianness of the processor](http://en.wikipedia.org/wiki/Endianness) on which the JavaScript is being executed.

The code below, however, rectifies this oversight by testing the endianness of the target processor and then executing a different version of the main loop dependent on whether the processor is big- or little-endian.

A [corresponding jsperf test](http://jsperf.com/canvas-pixel-manipulation/6) for this amended code has also been written and shows near-identical results to the original jsperf test. Therefore, our final conclusion remains the same.

Many thanks to all commenters and testers.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 21 comments

BorisDecember 1st, 2011 at 14:38Andrew J. BakerDecember 1st, 2011 at 15:00BorisDecember 1st, 2011 at 19:12JoeDecember 1st, 2011 at 15:26BorisDecember 1st, 2011 at 15:31Ryan BadourDecember 1st, 2011 at 16:53BorisDecember 2nd, 2011 at 05:50barryvanDecember 1st, 2011 at 17:29BorisDecember 2nd, 2011 at 05:55GordonDecember 1st, 2011 at 17:59JoeDecember 2nd, 2011 at 12:55BorisDecember 2nd, 2011 at 12:57David WilhelmDecember 1st, 2011 at 19:03Andrew J. BakerDecember 2nd, 2011 at 14:15JonDecember 1st, 2011 at 19:084esn0kDecember 1st, 2011 at 20:17JoeDecember 4th, 2011 at 00:02dhaberApril 16th, 2012 at 09:38Paul NeaveApril 25th, 2012 at 02:05Andrew J. BakerApril 25th, 2012 at 08:39Andrew J. BakerMay 9th, 2012 at 09:13