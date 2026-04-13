---
title: The OpenGL Impedance Mismatch
url: http://hacksoflife.blogspot.com/2015/04/the-opengl-impedance-mismatch.html
author: Benjamin Supnik
published: '2015-04-14'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

As graphics hardware has changed from a fixed function graphics pipeline to a general purpose parallel computing architecture, mid-level graphic APIs like OpenGL don't fit the execution model of the actual hardware as well as they used to.


In my


This has been true for a while. For example, older fixed function and partly programmable GPUs might have one set of register state to control the entire fixed-function raster operations. Here's the








In fact, the impedance match makes this even worse: if we're going to have any hope of changing state quickly, the driver has to track past combinations of vertex layout, MRT indirection, and the actual GLSL linked program, and cache the "real" shader that backs this combined state. Each time we change the front-end vertex fetch format or back-end MRT layout, the driver has to go see if that combination exists in cache.


The back-end MRT layout isn't the worst problem because we are hopefully not going to change rendering targets that frequently. But the vertex format is a real mess; every call to glVertexAttribPointer potentially invalidates the vertex layout; the driver can either try to heavily check state change, or regenerate the shader front-end; both options stink.


You can see OpenGL trying to track the moving target of the hardware in the extensions:


A newer extension,


If there's an executive summary here, it's that OpenGL as an API has never been a perfect representation of what the hardware is doing, but as the hardware moves toward general purpose compute devices that work on buffers of memory, the pipeline-and-state model fits less and less.


In my next posts I'll take a look at Metal and Mantle - these new APIs let us take the red pill and see how deep the rabbit hole goes.



* I am of the opinion that VAOs were a mistake from day one. VAOs are mutable to allow them to be 'layered' on top of existing code the way VBOs were, and even if they weren't, the data location of the VBO is mutable at the driver level (because the VBO may at the time of draw be in VRAM or system memory, and may require a change to the memory map of the CPU that the GPU holds to draw, or it may require a DMA copy to move it to RAM). The result is that binding a VAO doesn't let you skip the tons of validation and synchronization needed to actually start drawing once the base pointers have been moved.

In my

[previous post](http://hacksoflife.blogspot.com/2015/04/opengl-state-change-is-deferred.html), I said that the execution of GL state change is deferred so that the driver can figure out what you'r really trying to do and efficiently change all state at once.This has been true for a while. For example, older fixed function and partly programmable GPUs might have one set of register state to control the entire fixed-function raster operations. Here's the

[R300](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/R3xx_3D_Registers.pdf)(e.g. the Radeon 9700).- The blend function and sources share a single register, but
- The alpha and RGB blend function/sources are in different registers (meaning a single glBlendFuncSeparate partly updates both).
- Alpha-blend enable shares a register with the flag to separate the blender functions. (Why the hardware doesn't just always run separate and let the driver update both sides of the blender is a mystery to me.)
- Some GL state actually matches the register (e.g. the clear color is its own register).

- Fixed function tricks like blending and stenciling are enabled by setting registers on the GPU.
- Uniforms for a given shader live on the chip while the shader is executing.
- The vertex fetcher is fixed functionality that is set up by register.

- Shader constants come from memory (this has been true for a while now) - this is a good fit for a UBOs but a bad fit for "loose uniforms" that are tied to the shader object. On the GPU, the shader object and uniforms are fully separable.
- Vertex fetch is entirely in the shader - the driver writes a pre-amble for you. Thus changing the vertex alignment format (but not the base address) is a shader edit! Ouch.
- For shaders that write to multiple render targets, OpenGL lets us remap them via
[glDrawBuffers](https://www.opengl.org/sdk/docs/man/html/glDrawBuffers.xhtml), but this export mapping is part of the fragment shader, so that's a shader edit too.

In fact, the impedance match makes this even worse: if we're going to have any hope of changing state quickly, the driver has to track past combinations of vertex layout, MRT indirection, and the actual GLSL linked program, and cache the "real" shader that backs this combined state. Each time we change the front-end vertex fetch format or back-end MRT layout, the driver has to go see if that combination exists in cache.

The back-end MRT layout isn't the worst problem because we are hopefully not going to change rendering targets that frequently. But the vertex format is a real mess; every call to glVertexAttribPointer potentially invalidates the vertex layout; the driver can either try to heavily check state change, or regenerate the shader front-end; both options stink.

You can see OpenGL trying to track the moving target of the hardware in the extensions:

[GL_ARB_vertex_array_object](https://www.opengl.org/registry/specs/ARB/vertex_array_object.txt)was made part of core OpenGL 3.0 and ties up the entire vertex fetch plus base pointer in a single "object" for quick recall. But we can see that this is now a pretty poor fit; half of the state that the VAO covers (the layout) is really part of the shader, while the other half (the actual address of the VBO plus offset) is separate.*A newer extension,

[GL_ARB_vertex_attrib_binding](https://www.opengl.org/registry/specs/ARB/vertex_attrib_binding.txt), separates the vertex format (which is part of the shader in hardware) from the actual data location; it was made part of OpenGL 4.3. I don't know how good of a fit this is; the vertex attribute binding leaves the data stride out of the "expensive" format binding. (My guess is that the intended implementation is to specify the data stride as a constant in a constant buffer somewhere.) In theory with this extension, only glVertexAttribFormat requires an expensive shader patch, and applications can change VBO sources without calling it.If there's an executive summary here, it's that OpenGL as an API has never been a perfect representation of what the hardware is doing, but as the hardware moves toward general purpose compute devices that work on buffers of memory, the pipeline-and-state model fits less and less.

In my next posts I'll take a look at Metal and Mantle - these new APIs let us take the red pill and see how deep the rabbit hole goes.

* I am of the opinion that VAOs were a mistake from day one. VAOs are mutable to allow them to be 'layered' on top of existing code the way VBOs were, and even if they weren't, the data location of the VBO is mutable at the driver level (because the VBO may at the time of draw be in VRAM or system memory, and may require a change to the memory map of the CPU that the GPU holds to draw, or it may require a DMA copy to move it to RAM). The result is that binding a VAO doesn't let you skip the tons of validation and synchronization needed to actually start drawing once the base pointers have been moved.

It should be noted that the vertex format part of VAOs are not necessarily shader state. At least, not on all hardware.



ReplyDeleteWhile AMD's GCN hardware does indeed have to patch the vertex shader to be able to fetch vertex attributes, AMDs older hardware and all Intel and NVIDIA hardware has dedicated vertex fetching logic.

Note that, while Mantle explicitly does not have any vertex fetching (you do that yourself in the vertex shader), both Vulkan and D3D12 add that back in.

I'm glad they added vertex fetch as a black box back. My view, as a smaller 3-d developer, is that when there is a task that is extremely common in its purpose ("fetch vertices"), letting the driver guys code it is going to result in everyone getting optimal code - either we use the fixed vertex fetcher, or we use the driver writer's hand-tuned, carefully optimized assembly.



DeleteI'm just not going to have time to study how good my own home-rolled vertex fetch is, for every GPU out there, in that kind of depth.

But I do wonder if we'll wake up one day and hardware or special tricks for vertex fetch is just gone for everyone...