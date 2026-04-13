---
title: 'WebGL 2 Development with PicoGL.js, Part 4: Transform Feedback'
url: https://tsherif.wordpress.com/2017/08/08/webgl-2-development-with-picogl-js-part-4-transform-feedback/
author: Tarek Sherif
published: '2017-08-08'
source_blog: Tarek Sherif
source_site: https://tsherif.wordpress.com
category: game programming
fetched: '2026-04-13'
---

![transformfeedback](../../assets/e0bd9cba41ad9d1a.png)


*This post is part of the series WebGL 2 Development with PicoGL.js.*

In [part 3](https://tsherif.wordpress.com/2017/08/04/webgl-2-development-with-picogl-js-part-3-uniform-buffers-and-instanced-drawing/), we learned how to use uniform buffers and instanced drawing to make our rendering more efficient. **Transform feedback** is another WebGL 2 feature that targets performance and can significantly improve the performance of animations. In WebGL 1, you would normally have to update object transforms on the CPU, which meant iterating over them serially. With transform feedback, we can capture vertex shader outputs from one frame into a buffer and use them as inputs for the next frame. This allows us to move our animation updates to the GPU, taking advantage of its massive parallelism.


We’ll start with our [boilerplate html page](https://github.com/tsherif/picogl-tutorial/blob/master/boilerplate.html) and fill in the vertex shader:

#version 300 es #define PI 3.14159 layout(location=0) in vec2 position; layout(location=1) in vec3 color; out vec2 vPosition; out vec3 vColor; void main() { float cos2 = cos(PI / 90.0); float sin2 = sin(PI / 90.0); mat2 rotation = mat2( cos2, sin2, -sin2, cos2 ); vPosition = rotation * position; vColor = color; gl_Position = vec4(vPosition, 0.0, 1.0); }

There are a few parts that are new here, so let’s go over them one by one:

- We
`#define`

a constant,`PI`

, that will help us set up a rotation. - We use
`PI`

to create a rotation matrix that rotates our positions by 2 degrees. Doing this in the vertex shader allows us to update the animation on the GPU. - We output the transformed position to the
`out`

variable,`vPosition`

, as well as using it to set`gl_Position`

. We’ve used vertex shader`out`

variables before to pass data to the fragment shader, but this one’s being used to capture the transformed positions so they can be used in the next frame.

The fragment shader is identical to the one we wrote in [part 1](https://tsherif.wordpress.com/2017/07/26/webgl-2-development-with-picogl-js-part-1-the-triangle/):

#version 300 es precision highp float; in vec3 vColor; out vec4 fragColor; void main() { fragColor = vec4(vColor, 1.0); }

Creating the program is similar to what we’ve done before but with one important difference:

var vsSource = document.getElementById("vertex-shader").text.trim(); var fsSource = document.getElementById("fragment-shader").text.trim(); var program = app.createProgram(vsSource, fsSource, ["vPosition"]);

Notice the third argument to `createProgram()`

. This is an array of **transform feedback varyings**, which are the `out`

variables from our vertex shader that we want to capture in a feedback buffer.

Now the critical part of setting up our buffers for transform feedback:

var positionsA = app.createVertexBuffer(PicoGL.FLOAT, 2, new Float32Array([ -0.3, -0.3, 0.3, -0.3, 0.0, 0.3 ])); var positionsB = app.createVertexBuffer(PicoGL.FLOAT, 2, 6); var colors = app.createVertexBuffer(PicoGL.FLOAT, 3, new Float32Array([ 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0 ])); var triangleArrayA = app.createVertexArray() .vertexAttributeBuffer(0, positionsA) .vertexAttributeBuffer(1, colors); var triangleArrayB = app.createVertexArray() .vertexAttributeBuffer(0, positionsB) .vertexAttributeBuffer(1, colors); var transformFeedbackA = app.createTransformFeedback() .feedbackBuffer(0, positionsA); var transformFeedbackB = app.createTransformFeedback() .feedbackBuffer(0, positionsB); var drawCallA = app.createDrawCall(program, triangleArrayA) .transformFeedback(transformFeedbackB); var drawCallB = app.createDrawCall(program, triangleArrayB) .transformFeedback(transformFeedbackA);

There’s a lot going on here, so we’ll go through it step by step:

- Lines 1-7: We create
**two**position buffers.`positionsA`

contains our initial positions,`positionsB`

starts out empty and will be updated after we start rendering. On a given frame, one of these buffers will be used as input to the vertex shader, and the other will capture the output. On the following frame, the input and output buffers are swapped. - Lines 9-13: The color buffer isn’t part of the transform feedback, so we only need one.
- Lines 15-21: We create a separate vertex array for each position buffer. They share the color buffer.
- Lines 23-27: We create two transform feedback objects, one for each position buffer.
- Lines 29-33: We create two draw calls, one for each configuration of input and output position buffers.
`drawCallA`

will read from`positionsA`

and write vertex shader results to`positionsB`

.`drawCallB`

reads from`positionsB`

and writes to`positionsA`

.

When we refer to vertex shader results, we mean whatever we write to the transform feedback varyings in our vertex shader, i.e. `vPosition`

in this case.

With all those dots connected, running the animation is straightforward:

var currentDrawCall = drawCallA; function draw() { app.clear(); currentDrawCall.draw(); currentDrawCall = currentDrawCall === drawCallA ? drawCallB : drawCallA; requestAnimationFrame(draw); } requestAnimationFrame(draw);

We reference the draw call to use for the current frame in `currentDrawCall`

. Make sure this starts as `drawCallA`

, since our initial positions are in `positionsA`

. On each frame, we draw using the current draw call, then swap to the other draw call for the next frame. Because of how we set things up, this has the effect of swapping the input and output position buffers. We use the output from the previous frame as input for the current frame, and that allows us to continue the animation. If all went well, you should see the triangle from the top of this post rotating counterclockwise. A live version is available [here](https://tsherif.github.io/picogl-tutorial/part4.html).

The complete code for this example is available [here](https://github.com/tsherif/picogl-tutorial/blob/master/part4.html). If you have any questions, feel free to post them in the comments, visit the PicoGL.js [Gitter chat room](https://gitter.im/picogl-js/general), or look me up on [Twitter](https://twitter.com/thsherif).

## 2 thoughts on “WebGL 2 Development with PicoGL.js, Part 4: Transform Feedback”