---
title: WebGL 2 lands in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/01/webgl-2-lands-in-firefox/
author: Jeff Gilbert
published: '2017-01-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With the release of Firefox 51, **WebGL 2 support has landed**! WebGL is a standard API to render 3D graphics in the Web. It is based on OpenGL ES, which is commonly used by mobile games.

To date, we have been able to use WebGL 1 (based on OpenGL ES 2) to render fancy graphics into a <canvas> element. WebGL 2, however, is **based on the **[ OpenGL ES 3.0](https://www.khronos.org/registry/gles/specs/3.0/es_spec_3.0.pdf) specification, which introduces new features – many of them aimed at increasing performance and visual fidelity.

Until today, WebGL 2 had been usable behind a flag or in the Developer Edition or Nightly, but with Firefox 51, it’s now unlocked for all users of Firefox on Windows, MacOS, and Linux.

## Demo: “After the Flood” (PlayCanvas)

To give you a taste of the content WebGL 2 enables, we’re excited to highlight [ After the Flood](https://playcanv.as/e/p/44MRmJRU/), an interactive WebGL 2 demo by

**PlayCanvas**. (Please note that this demo is currently desktop only, with mobile support coming soon.) Take a walk through the fantastical environment of water, glass, and steel running entirely within your web browser!

## How to use WebGL 2

To request a [WebGL 2 context](https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext), all we need to do is ask for one from a <canvas> element. The string we use to request WebGL 2 is “webgl2”.

```
let canvas = document.querySelector('canvas');
let ctx = canvas.getContext('webgl2');
```


WebGL 2 might not be present in all browsers, so you should include some fallback code:

```
let canvas = document.querySelector('canvas');
let ctx = canvas.getContext('webgl2');
let isWebGL2 = !!ctx;
if (!isWebGL2) { // try to fallback to webgl 1
ctx = canvas.getContext('webgl') ||
canvas.getContext('experimental-webgl');
}
if (!ctx) {
console.log('your browser does not support WebGL');
}
```


### A word of caution…

Keep in mind that while WebGL 2 is based on OpenGL ES 3.0, it’s not *identical.* For instance, WebGL 2 does not support program binaries, and a number of optional restrictions in OpenGL are made mandatory for WebGL 2. The differences between the two are [laid out in the WebGL 2 spec](https://www.khronos.org/registry/webgl/specs/latest/2.0/#5), so if you’re already familiar with OpenGL, you’ll be able to get up to speed with WebGL 2 quickly.

Another thing to note is that **WebGL 2 is not strictly backwards compatible** with WebGL 1, so there is the possibility that your WebGL 1 code will not work as expected when using a WebGL 2 context. That said, the differences are fairly minimal, and you should be able to port your code and shaders without too much hassle. You can read a [backwards incompatibility list](https://www.khronos.org/registry/webgl/specs/latest/2.0/#4.1) in the spec, as well as this [quick guide from WebGL2 Fundamentals](http://webgl2fundamentals.org/webgl/lessons/webgl1-to-webgl2.html) about **migrating code** from WebGL 1 to WebGL 2.

Keep in mind that while WebGL 2 will be bringing these new features to many of our users, we cannot offer WebGL 2 to users with old or outdated graphics cards and drivers.

## Highlighted features

### Updated shading language

WebGL 2 supports **OpenGL ES Shading Language 3.0**, which allows for much more capable and efficient shading programs. The new toys include:

- True integer types
- Uniform blocks
- Binding the location indices for shader inputs and outputs in the shader source
- Fragment discard
- Dynamic loops
- Sophisticated texture sampling built-ins

### Multiple render targets (“MRTs”)

This allows you to render to several color buffers or textures in one pass, using multiple outputs from the fragment shader.

This feature was enabled in WebGL 1 via an extension, but now forms part of the core set of features of WebGL 2, so there’s no need to worry about a fallback path.

One of the main applications of MRTs is a technique called deferred shading – and we have already [written about it in Hacks](https://hacks.mozilla.org/2014/01/webgl-deferred-shading/) before. It’s a rendering technique that allows for *a lot* of dynamic lights in a scene, since the complexity on rendering doesn’t depend on the amount of lights, but on the actual number of pixels that are being lit.

### Instanced geometry drawing

Instancing allows you to render multiple instances of a geometry with a single draw call, which reduces the burden on the CPU. Note that each instance can have its own attributes, like a transformation matrix, so you could use this to render a lot of similar objects, like particles, trees in a forest, people in a crowd, etc.

The following THREE.js demo uses instancing via an extension – which, remember, is no longer needed in WebGL 2.

![instanced-rendering](../../assets/9920f6310e2c53d2.jpg)


### New texture features

3D or volume textures are textures where we access the data using three coordinates instead of two (like in regular, 2D textures). These are most commonly used for tone mapping, but also can be helpful for rendering volumetric effects, like smoke, fog, and rays.

2D array textures hold a series of separate 2D layers, which a shader can index into in order to select just one of the contained 2D textures.

[Sampler objects](https://developer.mozilla.org/en-US/docs/Web/API/WebGLSampler) are new in WebGL 2. These decouple the way the texture is sampled from the texture selected for sampling, so a single texture can be sampled in several ways, and multiple textures can point to the same sampler object.

WebGL 2 also removes restrictions on [non-power-of-two (NPOT) textures](https://www.khronos.org/opengl/wiki/NPOT_Texture).

### Transform feedback

[Transform feedback captures](https://developer.mozilla.org/en-US/docs/Web/API/WebGLTransformFeedback) the output of the vertex shader into a buffer object, often using this output as input to the next frame. This creates a loop that doesn’t leave the GPU, offloading the CPU of these computations. Particle systems often take advantage of transform feedback to iterate each particle’s position and move it in each frame without CPU interaction.

Transform feedback can also be combined with “rasterizer discard”, which allows running the vertex shader without the fragment shader. This allows for natural “map” [GPGPU (general-purpose computing on graphics processing units)](https://en.wikipedia.org/wiki/General-purpose_computing_on_graphics_processing_units) data processing flows.

![transform-feedback](../../assets/073315d71edab3e9.jpg)


### And more!

There are many more features that have arrived in WebGL 2, including [Vertex Array Objects](https://developer.mozilla.org/en-US/docs/Web/API/WebGLVertexArrayObject), MSAA renderbuffers, and Uniform Buffer Blocks to name a few. For a full list of everything new in WebGL 2, you can [have a look at the official spec](https://www.khronos.org/registry/webgl/specs/latest/2.0/), since it contains just the differences between WebGL 1 and 2.

A number of these features can be seen in relative isolation on the [WebGL 2 samples](http://webglsamples.org/WebGL2Samples) page. These feature-specific demos serve to illustrate the effects possible with new features, as well as to provide example code for how to use them.

## What’s next

We’re releasing the API for widespread use today, but there’s still more work to do. We’re looking forward to working on performance improvements, relaxing some restrictions, and improving general polish. We know performance in particular is on a lot of your minds, so we have some exciting work in store to provide applications with the performance they need to deliver even more sophisticated and impactful experiences.

In addition to seeing apps add WebGL 2 support, we look forward to seeing WebGL 2 integration into existing WebGL frameworks and engines. [PlayCanvas](https://playcanvas.com/) is supporting WebGL 2, as shown off in our highlight of **After the Flood**. [Three.js](https://threejs.org/) also has support for utilizing WebGL 2. Keep an eye out for other engines receiving WebGL 2 support later this year!

Running into an issue? Please [file a bug on our Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&component=Canvas%3A%20WebGL). (Remember: GitHub logins work too!)

## About Jeff Gilbert

Jeff leads Firefox WebGL development and is co-editor of the WebGL specs.

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## 24 comments

Omar ShehataJanuary 24th, 2017 at 09:32Joseph PetersonJanuary 24th, 2017 at 10:00MarcoJanuary 25th, 2017 at 12:04Andre VrignaudJanuary 24th, 2017 at 10:59JohnJanuary 24th, 2017 at 19:40mkvJanuary 25th, 2017 at 11:46Jeff GilbertJanuary 25th, 2017 at 13:19OlivierJanuary 26th, 2017 at 12:02Jeff GilbertFebruary 8th, 2017 at 17:29OlivierFebruary 9th, 2017 at 06:04OlivierFebruary 9th, 2017 at 06:35XuerJanuary 25th, 2017 at 15:24dandJanuary 26th, 2017 at 07:26Daniel C. HenningJanuary 25th, 2017 at 18:47Jeff GilbertJanuary 27th, 2017 at 15:26clemJanuary 25th, 2017 at 19:26Jeff GilbertFebruary 8th, 2017 at 17:27mkvJanuary 26th, 2017 at 05:32Martin BestJanuary 26th, 2017 at 23:51wissingJanuary 30th, 2017 at 06:08Jeff GilbertFebruary 8th, 2017 at 17:26Wellington TorrejaisFebruary 6th, 2017 at 07:58Muchlas BarkatFebruary 19th, 2017 at 04:19Rober VillarFebruary 19th, 2017 at 12:21