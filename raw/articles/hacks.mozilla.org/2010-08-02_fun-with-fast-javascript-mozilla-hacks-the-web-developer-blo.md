---
title: Fun With Fast JavaScript – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/08/fun-with-fast-javascript/
author: Christopher Blizzard
published: '2010-08-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This post is by Vladimir Vukićević and is a re-post from his personal weblog.*

Fast JavaScript is a cornerstone of the modern web. In the past, application authors had to wait for browser developers to implement any complex functionality in the browser itself, so that they could access it from script code. Today, many of those functions can move straight into JavaScript itself. This has many advantages for application authors: there’s no need to wait for a new version of a browser before you can develop or ship your app, you can tailor the functionality to exactly what you need, and you can improve it directly (make it faster, higher quality, more precise, etc.).

Here are two examples that show off what can be done with the improved JS engine and capabilities that will be present in Firefox 4. The first example shows ![JavaScript Darkroom](http://blog.vlad1.com/wp-content/uploads/2010/07/2010-06-24_1353.png)


[a simple web-based Darkroom](http://people.mozilla.com/~vladimir/demos/darkroom/darkroom.html)

[that allows you to perform color correction on an image. The HTML+JS is around 700 lines of code, not counting jQuery. This is based on a demo that’s included with Google’s Native Client (NaCl) SDK; in that demo, the color correction work is done inside native code going through NaCl. That demo (originally presented as “too slow to run in JavaScript”) is a few thousand lines of code, and involves downloading and installing platform-specific compilers, multiple steps to test/deploy code, and installing a plugin on the browser side.]

I get about 15-16 frames per second with the default zoomed out image (around 5 million pixels per second — that number won’t be affected by image size) on my MacBook Pro, which is definitely fast enough for live manipulation. The algorithm could be tightened up to make this faster still. Further optimizations to the JS engine could help here as well; for example, I noticed that we spend a lot of time doing floating point to integer conversions for writing the computed pixels back to the display canvas, due to how the canvas API specifies image data handling.

The Web Darkroom tool also supports drag & drop, so you can take any image from your computer and drop it onto the canvas to load it. A long (long!) time ago, back in 2006, I wrote [an addon called “Croppr!”](http://people.mozilla.com/~vladimir/corppr/). It was intended to be used with Flickr, allowing users to play around with custom crops of any image, and then leave crop suggestions in comments to be viewed using Croppr. It almost certainly doesn’t work any more, but it would be neat to update it: this time with both cropping and color correction. Someone with the addon (perhaps a [Jetpack](https://jetpack.mozillalabs.com/) now!) could then visit a Flickr photo and experiment, and leave suggestions for the photographer.

The ![JavaScript Video FFT](http://blog.vlad1.com/wp-content/uploads/2010/07/2010-06-24_1352.png)


[second example](http://people.mozilla.com/~vladimir/demos/jsfft/jsfft.html)is based on some work that Dave Humphrey and others have been doing to bring audio manipulation to the web platform. Originally, their spec included a pre-computed FFT with each audio frame delivered to the web app. I suggested that there’s no need for this — while a FFT is useful for some applications, for others it would be wasted work. Those apps that want a FFT could implement one in JS. Some benchmark numbers backed this up — using the

[typed arrays](https://cvs.khronos.org/svn/repos/registry/trunk/public/webgl/doc/spec/TypedArray-spec.html)originally created for

[WebGL](http://webgl.org/), computing an FFT in JS was approaching the speed of native code. Again, both could be sped up (perhaps using SSE2 or something like Mono.Simd on the JS side), but it’s fast enough to be useful already.

The demo shows this in action. A numeric benchmark isn’t really all that interesting, so instead I take a video clip, and as it’s playing, I extract a portion of the green channel of each frame and compute its 2D FFT, which is then displayed. The original clip plays at 24 frames per second, so that’s the upper bound of this demo. Using Float32 typed arrays, the computation and playback proceeds at around 22-24fps for me.

You can grab the video controls and scrub to a specific frame. (The frame rate calculation is only correct while the video is playing normally, not while you’re scrubbing.) The video source uses Theora, so you’ll need a browser that can play Theora content. (I didn’t have a similar clip that uses WebM, or I could have used that.)

These examples are demonstrating the strength of the trace-based JIT technique that Firefox has used for accelerating JavaScript since Firefox 3.5. However, not all code can see such dramatic speedups from that type of acceleration. Because of that, we’ll be including a full method-based JIT for Firefox 4 (for more details, see [David Anderson’s blog](http://www.bailopan.net/blog/?p=683), as well as [David Mandelin’s blog](http://blog.mozilla.com/dmandelin/2010/05/10/jm-halfway/)). This will provide significantly faster baseline JS performance, with the trace JIT becoming a turbocharger for code that it would naturally apply to.

Combining fast JavaScript performance alongside new web platform technologies such as WebGL and Audio will make for some pretty exciting web apps, and I’m looking forward to seeing what developers do with them!

*Edit: Made some last-minute changes to the demos, which ended up pulling in a slightly broken version of jQuery UI that wasn’t all that happy with Safari. Should be fixed now!*

## 3 comments

Daniel HendrycksAugust 5th, 2010 at 09:48Daniel HendrycksAugust 6th, 2010 at 09:31nemoAugust 17th, 2010 at 10:25