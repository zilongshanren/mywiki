---
title: Shader Primer | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/02/shader-primer/
author: Allen Chou
published: '2011-02-17'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

I’ve been studying shaders recently, in order to get myself prepared for shader programming with [Molehill](http://labs.adobe.com/technologies/flash/molehill/), the upcoming update to Flash Player that exposes low-level GPU-accelerated APIs. For those who are not familiar with shaders, and are also eager to get ready for shader programming with Molehill, I’ll share what I have learned about shaders in this post.

To present the concept in a clean way, I write in pseudocode. You may apply the concept in any shader language you like, such as [GLSL](http://en.wikipedia.org/wiki/GLSL), [HLSL](http://en.wikipedia.org/wiki/High_Level_Shader_Language), and the shading language in Molehill.

**Shaders**

A shader is a piece of compiled program that lies in the GPU memory, which can be executed by the GPU. It’s pretty much like a piece of program in the main memory that can be executed by the CPU. Unlike ordinary CPU-executed program, a shader program consists of instructions that can be executed extremely fast by the dedicated hardware, the GPU.

There are generally two types of shaders: the **vertex shader** and the **fragment shader** (or pixel shader). Normally, in a rendering pipeline, vertex data are passed in to the vertex shader, transformed, and then passed to the fragment shader; finally, the fragment shader decides the final result of each pixel on the screen, based on the output of the vertex shader (e.g. within a triangle if you’re using the vertices to draw triangles). A vertex shader is run once for each vertex, and a fragment shader is run once for each pixel on the screen.

To get the most out of the GPU, shaders are essentially executed in parallel for each vertex and each pixel. As a reasonable result, the context of each shader program is independent of and have no access to the result of other input vertices and pixels. For those familiar with [Pixel Bender](http://en.wikipedia.org/wiki/Adobe_Pixel_Bender), its programs also have this property since it’s shader-based.

**Vertex Shaders**

Okay, let’s take a look at an example for a vertex shader. We’d like to create a very simple vertex shader that simply transforms a vertex with a matrix. This is actually useful enough if you want to project a vertex in 3D space into 2D screen space.

The input is the single vertex to be transformed, and the transform matrix is declared as a **parameter**, which can be set by the main program. In the pseudo code, the vertex in 3D space is stored as a 4D float vector, and the matrix representing a 3D transform is stored as a 4-by-4 float matrix; in this way, we can express translation in 3D space in a single matrix multiplication, which is not possible if you use 3D float vectors and 3-by-3 float matrices.

input float4 vertex; parameter matrix44 transform; output float4 result; void main() { result = transform * vertex; }

**Fragment Shaders**

Usually, in the main program you would associate custom data with each vertices. For instance, a very common extra vertex data is the **UV coordinate**, which is mainly used for [UV mapping](http://en.wikipedia.org/wiki/UV_mapping), a texturing technique. Each pixel on the screen is most likely to lie inside a triangle formed by three vertices projected onto the screen, and for each pixel, the **interpolated value** of these extra data can be calculated in the fragment shader. Generally, you mark a variable as interpolated with a modifier in the shader program, and the value is automatically interpolated by the GPU when the shader program is run.

Below is a fragment shader example, which interpolates the UV coordinate of the output pixel, takes as input a texture (a image4 parameter representing 4-channel bitmap), and outputs the final color of the pixel. Note that the interpolation is not ordinary linear interpolation; the interpolation is done in a **perspective-correct** manner, meaning that the sample points become more “sparse” for farther points (“deeper pixels” in screen coordinates). Normally, a shader language would allow you to specify the how the interpolation is done (perspective-correct, non-perspective, etc), and usually the perspective-correct interpolation is the default approach.

input float2 uvCoord; interpolated float2 interpolatedUVCoord; paramter image4 texture; output float4 result; void main() { //interpolated automatically interpolatedUVCoord = uvCoord; result = sample(texture, interpolatedUVCoord); }

Done! With these two example shaders combined, you can render with basic matrix transformation and UV mapping. I’ve pretty much covered the concepts you need to know to get started with shader programming.

Get yourself prepared for Molehill! 🙂

Brilliant summary about shaders! Wish I had also done summarizing these right after I read about OpenGL ES too.. before they did vaporize away from inside my head.

One thing I couldn’t get clear of is that how the “perspective-correct” thing is done. In a vertex shader we seem to be able to apply either an orthographic or a perspective projection matrix, but are we able to (or perhaps, do we have to?) specify the way interpolation is done, or you’re suggesting that sometimes it’s always done in a perspective-correct manner?

p.s. One of your headlines says “Pixel Shaders” but by the context I’m sure you meant “Vertex Shaders”? 🙂

Thanks for pointing out for the incorrect header. I’ve corrected it 🙂

And yes, normally you are allowed to specify how the interpolation is done. Here I only mentioned the perspective-correct interpolation for simplicity. I’ve added more description in the post to make this point clear.