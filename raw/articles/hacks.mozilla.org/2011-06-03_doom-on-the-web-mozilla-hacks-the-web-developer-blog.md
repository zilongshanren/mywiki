---
title: Doom on the Web – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/06/doom-on-the-web/
author: Janet Swisher
published: '2011-06-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Update**: We had a doubt whether this port of the Open Source Doom respected its term of use. We decided to remove it from our Website before taking an informed and definitive decision.

*This is a guest post written by Alon Zakai. Alon is one of the Firefox Mobile developers, and in his spare time does experiments with JavaScript and new web technologies. One of those experiments is Emscripten, an LLVM-to-JavaScript compiler, and below Alon explains how it uses typed arrays to run the classic first-person shooter *

As a longtime fan of first-person shooters, I’ve wanted to bring them to the web. Writing one from scratch is very hard, though, so instead I took the original Doom, which is open source, and compiled it from C to JavaScript using [Emscripten](https://github.com/kripken/emscripten). The result is a version of Doom that can be [ played on the web](https://hacks.mozilla.org#), using standard web technologies.

Doom renders by writing out pixel data to memory, then copying that pixel data to the screen, after converting colors and so forth. For this demo, the compiled code has *memory* that is simulated using a large JavaScript array (so element N in that array represents the contents of memory address N in normal native code). That means that rendering, color conversion, and copying to the screen are all operations done on that large JavaScript array. Basically the code has large loops that copy or modify elements of that array. For that to be as fast as possible, the demo optionally uses JavaScript typed arrays, which look like normal JavaScript arrays but are guaranteed to be *flat* arrays of a particular data type.

// Create an array which contains only 32-bit Integers var buffer = new Int32Array(1000); for ( var i = 0 ; i < 1000 ; i++ ) { buffer[i] = i; }

When using a typed array, the main difference from a normal JavaScript array is that the elements of the array all have the type that you set. That means that working on that array can be much faster than a normal array, because it corresponds very closely to a normal low-level C or C++ array. In comparison, a normal JavaScript array can also be *sparse*, which means that it isn't a single contiguous section of memory. In that case, each access of the array has a cost, that of calculating the proper memory address. Finding the memory address is much faster with a typed array because it is simple and direct. As a consequence, in the Doom demo the frame rate is almost twice as fast with typed arrays than without them.

Typed arrays are very important in WebGL and in the [Audio Data](https://developer.mozilla.org/en/Introducing_the_Audio_API_Extension) API, as well as in [Canvas](https://developer.mozilla.org/en/HTML/Canvas) elements (the pixel data received from `getImageData()`

is, in fact, a typed array). However, typed arrays can also be used independently if you are working on large amounts of array-like data, which is exactly the case with the Doom demo. Just be careful that your code also works if the user's browser does not support typed arrays. This is fairly easy to do because typed arrays look and behave, for the most part, like normal ones — you access their elements using square brackets, and so forth. The main potential pitfalls are:

- Typed arrays do not have the
`slice()`

. Instead they have the`subarray()`

, which does not create a copy of the array — instead it's a view into the same data. - Don't forget that the type of the typed array is silently enforced. If you write 5.25 to an element of an integer-typed array and then read back that exact same element, you get 5 and not 5.25.

## About
[
louisremi ](http://twitter.com/louis_remi)

Developer Relations Team, long time jQuery contributor and Open Web enthusiast. [@louis_remi](http://twitter.com/louis_remi)

## 14 comments

ShmerlJune 3rd, 2011 at 09:13Not foundJune 4th, 2011 at 02:09nemoJune 4th, 2011 at 12:31skierpageJune 4th, 2011 at 13:41MikeJune 4th, 2011 at 18:39nemoJune 5th, 2011 at 12:23farinJune 9th, 2011 at 03:26louisremiJune 9th, 2011 at 03:32ZippoLagJune 14th, 2011 at 08:17Janet SwisherJune 17th, 2011 at 13:00jmdespJune 20th, 2011 at 08:01James HaleyJuly 20th, 2011 at 20:40louisremiJuly 21st, 2011 at 07:46James HaleyAugust 5th, 2011 at 16:03