---
title: Interview with Micah Elizabeth Scott, winner of the Web Workers Dev Derby –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/08/interview-with-micah-elizabeth-scott-winner-of-the-web-workers-dev-derby/
author: John Karahalis
published: '2013-08-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![Micah Elizabeth Scott](https://hacks.mozilla.org/wp-content/uploads/2013/07/micah-elizabeth-scott1-250x255.jpg)

[Web Workers Dev Derby](https://developer.mozilla.org/demos/devderby/2013/april) with [Zen photon garden](https://developer.mozilla.org/demos/detail/zen-photon-garden), her impressive (and fun) interactive web raytracer. Recently, I had the chance to learn more about Micah: her work, her ambitions, and her thoughts on the future of web development.

## The interview

### How did you become interested in web development?

I’ve been into building things for as long as I can remember. I love

making things, and I’ll often learn new tools just for the sake of

giving myself a different set of challenges and constraints to work

with. My first big web project was an early collaboration tool for

open source development, dubbed “CIA” because it spies on your source

code commits.

### Can you tell us a little about how Zen photon garden works?

Zen photon garden is a type of [raytracer](http://wikipedia.org/wiki/Ray_tracer), which is to say it simulates

the path that individual rays of light take as they bounce around in a

scene. It’s a two-dimensional raytracer though, which opens up kind of

a neat new possibility for visualizing how light works.

A traditional three-dimensional raytracer traces rays “backwards”,

casting rays out from each pixel on a virtual camera, bouncing it off

of the objects in your scene, until it finally reaches a source of

light. Each pixel of the scene comes about by counting, on average,

how many photons would reach that portion of the virtual camera.

In Zen photon garden, light rays emanate from a lamp and move along

the image plane in two dimensions. Instead of visualizing the single

point where a ray reaches the camera, I visualize the entire ray as it

bounces through the scene. Each ray turns into a sequence of line

segments, beginning at the light source and bouncing off of any number

of objects before it’s eventually absorbed. This process repeats

hundreds of thousands of times, and the image you see is a statistical

average of these many light rays.

The inner loop of Zen photon garden is quite specialized. For each

light ray, I need to trace its path by intersecting it with the

objects in the scene, and each segment of this path is visualized by

drawing an anti-aliased line into a high-dynamic-range 32-bit

accumulation buffer. After tracing a bunch of these rays, the

high-dynamic-range buffer is mapped to an 8-bit-per-channel image

according to the current camera exposure setting, and that image is

drawn to a [Canvas](https://developer.mozilla.org/docs/Web/HTML/Element/canvas).

These anti-aliased lines need to be fast and very high quality. Any

errors in the uniformity of the line’s brightness, for example, will

affect the smoothness of the final image. To get the combination of

speed and accuracy I need, this line drawing algorithm is implemented

in pure [Javascript](https://developer.mozilla.org/docs/Web/JavaScript) by a pool of [Web Worker](https://developer.mozilla.org/docs/Web/API/Worker) threads. This pool has to

be managed carefully so that the app can draw with high throughput

when you leave it alone, but it can still respond with low latency

when you’re interactively adding objects to the scene.

### What was your biggest challenge in developing Zen photon garden?

The hardest part of implementing Zen photon garden was making it run

as fast as possible on all of the latest web browsers. Thankfully

these days it’s relatively easy to write an app that runs on all

browsers, but making it run optimally is tricky when your application

is CPU-bound. Small changes to the inner loops would cause big

differences in how well each Javascript engine’s optimizer performs.

This required a lot of trial and error, and a few trips back to the

drawing board.

### What makes the web an exciting platform for you?

To me the killer feature of the web is its universality. Modern web

browsers are nearly ubiquitous, and it’s the fastest way to take a

weird new experimental concept and get it into people’s hands right

now. As someone who loves exploring the intersection of art and

technology, this means it’s finally possible to send your friends a

link to your latest art project without having to worry about what

operating system they’re using or whether they have the right library

dependencies installed.

### What new web technologies are you most excited about?

[WebGL](https://developer.mozilla.org/docs/Web/WebGL) is really exciting to me, but as someone who used to write

graphics drivers and worry about security for a living it also kind of

terrifies me!

The web technology I’m most excited about would have to be [asm.js](http://asmjs.org/)

actually. I’ve always enjoyed getting my hands dirty with low-level

graphics code, and even in today’s world of GPU acceleration and

high-level 2D canvas APIs, I still find plenty of reasons to push

pixels. Having a way to get near-native performance in a very reliable

way across all major browsers would open up some great new creative

possibilities, and I’m excited to see where that leads.

### If you could change one thing about the web, what would it be?

It’d be great if we could find a way to ease the tension between those

who see the web as a content platform and those who see it as a

software operating system. Right now it feels like HTML is too

unwieldy to be a document markup language, and it’s just barely

starting to get the services you’d expect from a modern operating

environment.

### Do you have any advice for other ambitious web developers?

Plan to prototype a lot of things, keep the ideas that stick, and

throw the rest away. Respect the web as a platform, and try to be

playful about exploring its margins. Understand but don’t begrudge the

ways in which web programming is different from other kinds of

programming.

## Further reading

[Optimizing your JavaScript game for Firefox OS](https://hacks.mozilla.org/2013/05/optimizing-your-javascript-game-for-firefox-os/)[Building a simple paint game with HTML5 Canvas and Vanilla JavaScript](https://hacks.mozilla.org/2013/06/building-a-simple-paint-game-with-html5-canvas-and-vanilla-javascript/)[The concepts of WebGL](https://hacks.mozilla.org/2013/04/the-concepts-of-webgl/)