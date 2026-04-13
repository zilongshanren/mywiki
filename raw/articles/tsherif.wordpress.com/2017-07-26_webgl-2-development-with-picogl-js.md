---
title: WebGL 2 Development with PicoGL.js
url: https://tsherif.wordpress.com/2017/07/26/webgl-2-development-with-picogl-js/
author: Tarek Sherif
published: '2017-07-26'
source_blog: Tarek Sherif
source_site: https://tsherif.wordpress.com
category: game programming
fetched: '2026-04-13'
---

![3D-texture](../../assets/30283dd0e7d8863c.png)


[WebGL 2](https://www.khronos.org/registry/webgl/specs/latest/2.0/) is a substantial update to the WebGL API that requires a deeper understanding of the graphics pipeline than was necessary for WebGL 1. Many of the new features require manually ensuring that handles and memory are correctly laid out so that the pipeline can use them efficiently, but this setup can fail in subtle ways that can be difficult to debug.

[PicoGL.js](https://tsherif.github.io/picogl.js/) is a small WebGL 2 library with the modest goal of simplifying usage of new features without obscuring the functioning of the GL. The constructs one works with are the constructs of the GL: vertex array objects, vertex buffer objects, programs, transform feedbacks. PicoGL.js simply provides a more convenient API for interacting with those constructs, manages GL state, and also provides workarounds for some [known bugs](https://github.com/tsherif/webgl2bugs) in WebGL 2 implementations.

This tutorial series will provide an introduction to WebGL 2 development though PicoGL.js. Readers are expected to have some familiarity with WebGL 1 or another 3D graphics API. While I will try to fully describe the concepts that will be discussed, this series will be challenging for those with no graphics background. I’d recommend the [Udacity Interactive 3D Graphics](https://www.udacity.com/course/interactive-3d-graphics--cs291) course or [WebGL 2 Fundamentals](https://webgl2fundamentals.org/) for total beginners

This page will act as a table of contents that will be updated as the series progresses.

[Part 1: The Triangle](https://tsherif.wordpress.com/2017/07/26/webgl-2-development-with-picogl-js-part-1-the-triangle/)[Part 2: Textures and Framebuffers](https://tsherif.wordpress.com/2017/07/31/webgl-2-development-with-picogl-js-part-2-textures-and-framebuffers/)[Part 3: Uniform Buffers and Instanced Drawing](https://tsherif.wordpress.com/2017/08/04/webgl-2-development-with-picogl-js-part-3-uniform-buffers-and-instanced-drawing/)[Part 4: Transform Feedback](https://tsherif.wordpress.com/2017/08/08/webgl-2-development-with-picogl-js-part-4-transform-feedback/)[Part 5: A Particle System](https://tsherif.wordpress.com/2017/08/13/webgl-2-development-with-picogl-js-part-5-a-particle-system/)


Is there a “camera control” for navigating within the PicoGL system, something like Three’s OrbitControls? .. and thanks for the great library!

Glad you’re enjoying it, Owen! There are no camera controls since there’s no “camera” concept in WebGL, and I’ve written PicoGL to be a relatively thin wrapper around WebGL. I usually use the lookAt function from glMatrix for camera operations: http://glmatrix.net/docs/module-mat4.html#.lookAt