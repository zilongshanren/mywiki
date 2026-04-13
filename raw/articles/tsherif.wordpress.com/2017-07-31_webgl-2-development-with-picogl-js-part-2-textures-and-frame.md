---
title: 'WebGL 2 Development with PicoGL.js, Part 2: Textures and Framebuffers'
url: https://tsherif.wordpress.com/2017/07/31/webgl-2-development-with-picogl-js-part-2-textures-and-framebuffers/
author: Tarek Sherif
published: '2017-07-31'
source_blog: Tarek Sherif
source_site: https://tsherif.wordpress.com
category: game programming
fetched: '2026-04-13'
---

![part2-a](../../assets/d532c900c18258cf.png)


*This post is part of the series WebGL 2 Development with PicoGL.js.*

In [Part 1](https://tsherif.wordpress.com/2017/07/26/webgl-2-development-with-picogl-js-part-1-the-triangle/), we learned the basics of drawing with PicoGL.js:

- We created an
**app**. - We wrote some shaders in GLSL ES 3.00, and compiled them into a
**program**. - We created
**vertex buffers**to store geometry data and combined them into a**vertex array**. - We combined our
**program**and**vertex array**into a**draw call**, which we used to draw.

In this lesson, we’re going to add two important tools to our drawing toolkit: textures and framebuffers.


## Textures

Textures are just blocks of memory you can read from into your shader programs. The basic use case is a 2D image that’s sampled from to color an object, but WebGL 2 textures are much more flexible thanks to powerful new features like floating point textures, texture arrays and 3D textures. For this lesson, however, we’ll just see how to implement the basic use case in PicoGL.js.

We’ll start with our [boilerplate html page](https://github.com/tsherif/picogl-tutorial/blob/master/boilerplate.html), and download [this image](https://github.com/tsherif/picogl-tutorial/blob/master/webgl-logo.png) to use for the texture. Make sure the image is in the same directory as the html page.

Let’s fill out the vertex shader:

#version 300 es layout(location=0) in vec4 position; out vec2 vUV; void main() { vUV = position.xy + 0.5; gl_Position = position; }

Nothing too interesting going on here. We’re passing in our positions as before. We’re also creating UV coordinates that will be used to sample the texture. Normally, UV coordinates are passed in as a separate `in`

variable, but we’re cheating a bit here because we’re going to set up our geometry so that all the x,y coordinates will be between -0.5 and 0.5, so simply adding 0.5 to them will give us UV coordinates between 0 and 1.

Now the fragment shader:

#version 300 es precision highp float; in vec2 vUV; uniform sampler2D tex; out vec4 fragColor; void main() { fragColor = texture(tex, vUV); }

Again, nothing too exciting and all pretty familiar if you’re coming from WebGL 1. We have a sampler2D variable, `tex`

, that we use to sample our texture based on the interpolated UV coordinates we get in `vUV`

. One small GLSL 3.00 update to note is that we sample from the texture using the `texture()`

function, rather than `texture2D()`

as we’d use in GLSL 1.00. In GLSL 3.00, the `texture()`

function is overloaded and used for all sampler types, rather than having a different function for each type (e.g. `texture2D()`

, `textureCube()`

).

As before, we’ll create our program:

var vSource = document.getElementById("vertex-shader").text.trim(); var fSource = document.getElementById("fragment-shader").text.trim(); var program = app.createProgram(vSource, fSource);

We’ll create a vertex array similarly to before, but we’ll create a quad instead of a single triangle:

var positions = app.createVertexBuffer(PicoGL.FLOAT, 2, new Float32Array([ -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5 ])); var triangleArray = app.createVertexArray() .vertexAttributeBuffer(0, positions);

The next part involves some acrobatics to deal with loading the image asynchronously, but the important part is what’s in the image’s `onload`

handler:

var image = new Image(); image.onload = function() { var texture = app.createTexture2D(image, {flipY: true}); var drawCall = app.createDrawCall(program, triangleArray) .texture("tex", texture); app.clear(); drawCall.draw(); }; image.src = "webgl-logo.png";

First, we create a texture from the image we downloaded. The `flipY`

option is given because the y-axis in PNG images is flipped relative to WebGL’s. Then we create a draw call, as we’ve done before, but this time binding our texture to the sampler in our program. Finally, we draw to the screen in the same way we did last time.

Not incredibly exciting, since all of this is available in WebGL 1. But we’re now ready to start using textures as render targets for framebuffers, and that will give a chance to use a powerful new WebGL 2 feature: multiple render targets.

## Framebuffers

![part2-b](../../assets/113b2c1a5432c041.png)


Framebuffers are simply offscreen drawing surfaces. You bind a framebuffer, execute your draw commands, then you have the drawing results available in the framebuffer for other parts of the pipeline. If you set the render targets of the framebuffer to be textures, then those textures will be available for sampling in your shader programs. This is the foundation for many advanced rendering techniques, so let’s take a look at how we set up a simple PicoGL.js app that uses framebuffers.

We’ll start again with our [boilerplate html page](https://github.com/tsherif/picogl-tutorial/blob/master/boilerplate.html). This time we have one vertex shader that we’ll re-use and two different fragment shaders:

#version 300 es layout(location=0) in vec4 position; out vec2 vUV; void main() { vUV = position.xy * 0.5 + 0.5; gl_Position = position; } #version 300 es precision highp float; layout(location=0) out vec4 fragColor1; layout(location=1) out vec4 fragColor2; void main() { fragColor1 = vec4(1.0, 0.0, 0.0, 1.0); fragColor2 = vec4(0.0, 0.0, 1.0, 1.0); } #version 300 es precision highp float; in vec2 vUV; uniform sampler2D texture1; uniform sampler2D texture2; out vec4 fragColor; void main() { vec4 color1 = texture(texture1, vUV); vec4 color2 = texture(texture2, vUV); fragColor = mix(color1, color2, vUV.x); }

The vertex shader is similar to the one from the last section, except our UVs are being generated for a full-screen quad with coordinates from -1.0 to 1.0, so the calculation is slightly different. What’s interesting is that we’re going to use this same vertex shader for two different shapes on two separate rendering passes: a triangle on the first pass that won’t use the UVs, and a full-screen quad on the second pass that will use them. This kind of re-use is quite easy because of the control GLSL ES 3.00 gives us over attribute locations.

The first fragment shader is more interesting in that it introduces a powerful new WebGL 2 feature: multiple render targets. Note that we have two `out`

variables, and we’re writing a different color to each. Those will be written to two separate textures that we’ll set up when we create our framebuffer.

Finally, the second fragment shader will run on a second pass. The two textures it samples from will be mapped to the two outputs from the first pass. It will blend between the two colors from left to right using the x-coordinate of the UV input.

To summarize, our app will draw a triangle on the first pass to two separate offscreen render targets, drawing a different color to each. On the second pass, we’ll draw a full screen quad, and blend between the two output textures from the first pass.

Let’s create the two programs we need from those shaders:

var app = PicoGL.createApp(canvas) .clearColor(0, 0, 0, 1); var vSource = document.getElementById("vertex-shader").text.trim(); var vertexShader = app.createShader(PicoGL.VERTEX_SHADER, vSource); var fSourceMRT = document.getElementById("fragment-shader-mrt").text.trim(); var programMRT = app.createProgram(vertexShader, fSourceMRT); var fSourceBlend = document.getElementById("fragment-shader-blend").text.trim(); var programBlend = app.createProgram(vertexShader, fSourceBlend);

Note on line 5 that we create one vertex shader that we re-use in creating both programs. This saves us from having to recompile it for each program. The first program will render a triangle to the two offscreen render targets and the second will render a full-screen quad to the screen.

Now we create our geometry:

var triangePositions = app.createVertexBuffer(PicoGL.FLOAT, 2, new Float32Array([ -0.5, -0.5, 0.5, -0.5, 0.0, 0.5 ])); var triangleArray = app.createVertexArray() .vertexAttributeBuffer(0, triangePositions); var quadPositions = app.createVertexBuffer(PicoGL.FLOAT, 2, new Float32Array([ -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0 ])); var quadArray = app.createVertexArray() .vertexAttributeBuffer(0, quadPositions);

Nothing fancy here. One vertex array for the triangle on the first pass, another for the full-screen quad on the second. We then create our framebuffer:

var colorTarget1 = app.createTexture2D(app.width, app.height); var colorTarget2 = app.createTexture2D(app.width, app.height); var framebuffer = app.createFramebuffer() .colorTarget(0, colorTarget1) .colorTarget(1, colorTarget2);

This is pretty straightforward. First we create the two textures that we’ll render our scene into. Then we create the framebuffer and attach the textures as color targets at the same locations we gave for output from our fragment shader. Now we set up the draw calls for our two passes:

var drawCallMRT = app.createDrawCall(programMRT, triangleArray); var drawCallBlend = app.createDrawCall(programBlend, quadArray) .texture("texture1", framebuffer.colorAttachments[0]) .texture("texture2", framebuffer.colorAttachments[1]);

The blend draw call is the interesting one here. This is where we link the samplers for the second pass to the render target outputs from the first pass. Note that while we could have used the `colorTarget1`

and `colorTarget2`

texture objects directly, the framebuffer object conveniently keeps track of them for later use in the `colorAttachments`

array.

And finally, we draw!

app.drawFramebuffer(framebuffer).clear(); drawCallMRT.draw(); app.defaultDrawFramebuffer().clear(); drawCallBlend.draw();

Note that we use the methods `app.drawFramebuffer()`

and `app.defaultDrawFramebuffer()`

to bind our framebuffer for the first pass and then unbind it for the second.

And that’s pretty much it! The complete code for the two examples we created in this lesson are [here](https://github.com/tsherif/picogl-tutorial/blob/master/part2-a.html) and [here](https://github.com/tsherif/picogl-tutorial/blob/master/part2-b.html), and live versions are available [here](https://tsherif.github.io/picogl-tutorial/part2-a.html) and [here](https://tsherif.github.io/picogl-tutorial/part2-b.html). If you have any questions, feel free to post them in the comments, visit the PicoGL.js [Gitter chat room](https://gitter.im/picogl-js/general), or look me up on [Twitter](https://twitter.com/thsherif).

## 2 thoughts on “WebGL 2 Development with PicoGL.js, Part 2: Textures and Framebuffers”