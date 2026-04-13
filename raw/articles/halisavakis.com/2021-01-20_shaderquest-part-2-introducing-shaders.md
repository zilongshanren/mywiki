---
title: 'ShaderQuest Part 2: Introducing Shaders'
url: https://halisavakis.com/shaderquest-part-2-introducing-shaders/
published: '2021-01-20'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This ShaderQuest post is brought to you by these awesome Patrons:

- Not Invader Zim
- Tiph’ (DN)
- orels1

## Introduction

Yeah, this is an introduction to an introduction, what are you gonna do about it?

In this part we’ll start talking about the main point of the series: Shaders! We might not see a lot about how to write them and how they’re working, but we’ll get into what they do and how they fit into our workflows.

We still won’t really be touching any game engines or tools for shader creation just yet, because I think it’s valuable to have a more complete context around what exactly we’ll be creating.

Let’s get started!

## What are shaders?

In general, **shaders **are small programs that define how objects are shaded and rendered on our screen. These programs are running on the **GPU** instead of the CPU and there’s a good reason why.

## GPU Cores

Think of how many cores your CPU has. At best, it might have 32 cores with 64 threads? I don’t know about yours, but my GPU has around 1664 (CUDA) cores, and it’s not even a good one anymore. The reason for such a big gap in core counts is that GPU cores are great at handling lots of data and performing calculations in parallel, but not much else, as they don’t have the speed and larger instruction set that CPU cores have.

Additionally, because of the way the GPU works, a GPU core can at one frame work on one task, while at the next frame it can work on a completely different task. The same core can render a pixel on your video at one point and at the next frame it can render the pixels on your cursor.

If the CPU cores are like the fellowship of the ring, communicating and caring for each other and having specific common goals, GPU cores are like Uruk Hais tearing apart whatever task they get their hands on first.

Why am I telling you all that, though?

Well, in order to wrap your head around how shaders work (especially in written form) it’s important to understand the restrictions around how the GPU works and the parallel nature of its cores.

Consider this ultra naïve hypothetical scenario: let’s say you have to draw all the pixels on your entire FullHD screen – all 1920*1080 of them. The most straightforward approach someone with no programming experience would think would be to have a two-dimensional array where each cell corresponds to the output color and they’d use a loop (or nested loops) to iterate upon each cell and modify their color. Assuming you have infinite memory and processing power, that would give you the option to maybe also keep a history of what a pixel displayed or check what a pixel’s neighbors are displaying. What a fun world that would probably be!

But that’s not the case; **shaders operate** **on one specific piece of data**, as they run in parallel. If we’re talking about pixel/fragment shaders, whatever you write in that shader will operate on the pixel that’s currently being processed. You have some information about that specific pixel but not about much else (like what other pixels are doing or some other context information). It’s easy to lose track of that in node-based shader creation tools, but it’s still something to keep in mind. If you are to keep anything in mind from this post, actually, let it be this paragraph.

## Rendering pipeline and shader types

Let’s take a look at some overly used images around rendering:

![](https://i0.wp.com/www.khronos.org/opengl/wiki_opengl/images/RenderingPipeline.png?w=1080&ssl=1)

![](../../assets/8c9b704f750dd4c4.jpg)

In the OpenGL pipeline image, notice the blue boxes (Vertex shader, Tessellation, Geometry Shader, Fragment Shader), while on the DirectX pipeline image notice the rounded boxes (Vertex Shader Stage, Hull Shader Stage, Domain Shader Stage, Geometry Shader Stage and Pixel Shader Stage).

These are the programmable stages of the pipeline, and the stages for which we can write shaders. This also presents us with the different shader types.

## Shader Types

### Most common shader types

Here are the major shader types we’ll be working with:

#### Vertex Shader

Vertex shaders operate once on each vertex of a 3D model that’s given to the graphics processor (check out the [previous ShaderQuest part](https://halisavakis.com/shaderquest-part-1-graphics-concepts/) for some more context on vertices, graphics-wise). Their purpose is to transform each vertex’s 3D position to the 2D coordinate at which it appears on the screen and to, ultimately, pass information down to the next stages of the pipeline.

The 2D coordinates to which the 3D position of a vertex gets transformed are known as “**clip space position**“. In simple words, the vertex shader projects the 3D positions on our screen based on the camera’s projection mode (perspective/orthographic) and outputs coordinates going from -1 to 1 in a 2D space. Any value outside that range gets **clipped** (or **discarded**), so we don’t bother rendering any vertices whose 3D position gets projected outside our screen.

Note that while vertex shaders handle information around the vertices of an object, **new vertices cannot be created in this stage**. Additionally, keep in mind that vertex shaders operate, well, on vertices. **They have no awareness of other primitives like edges, triangles, quads etc.** The do not know what triangle contains a specific vertex out of the box and, frankly, they don’t give a damn about that.

Also, remember all the cool stuff that’s stored in a 3D object’s vertices, like the position, UV coordinates, normal vector and colors? This is the stage where you can access those! How fun! You can do stuff directly in the vertex shader with that information or you can just pass them along to the next stages of the rendering pipeline. You’ll see this happening a lot in hand-written shaders.

#### Fragment/Pixel Shader

Fragment (or pixel) shaders are responsible of computing the final color and other attributes of each pixel that ends up on your screen.

They receive a stream of data from the previous stages of the pipeline and are use that data to perform the final calculations that contribute to the rendering of an object, such as lighting, shading, texture sampling etc.

### Less common shader types

Here’s some other shader types that aren’t as common as vertex and fragment shaders, in the context of this series, but it’s good to keep them in mind:

#### Geometry Shaders

Geometry shaders operate after vertex shaders. They take primitives (points, edges or triangles) as their input and they can output new geometry; including new vertices, lines or even new triangles.

Geometry shaders can give you a lot of control over how and where to generate new data as you can also get adjacency information in some cases.

Some common uses for geometry shaders include effects like grass or fur, as well as useful computations that can adjust the complexity of the mesh as needed.

You can find more hands-on examples on how geometry shaders work in [my tutorial on geometry shaders in Unity](https://halisavakis.com/my-take-on-shaders-geometry-shaders/).

#### Tessellation/ Hull & Domain Shaders

One difference you might have noticed on the different rendering pipelines (OpenGL and DirectX) is that the OpenGL pipeline has a scriptable “Tessellation” stage, while the DirectX pipeline has two scriptable shader stages (Hull and Domain) with a non-scriptable “Tessellator” stage in-between.

The bottom line of both pipelines is the same though – the tessellation stage. This stage allows for simpler meshes to be subdivided into finer, more complex meshes to allow for more geometric detail while taking different factors into account, like the distance from the viewing camera for active LOD (level of detail) scaling.

In the context of this tutorial (or any tutorial I release soon 👀) we probably won’t be looking into writing shaders like this, although we might use tessellation at some point.

#### Compute Shaders

Compute shaders are general-purpose shaders that can be used for a plethora of applications, not only limited to graphics applications. They basically take advantage of the speed and parallel nature of the GPU to perform calculations with incredible speed and efficiency, compared to the CPU.

We might take a look into simple compute shaders in this series at some point, but if you’re already curious, you can look into [this great tutorial by Ronja](https://www.ronja-tutorials.com/post/050-compute-shader/).

## Interpolating Data

As I mentioned, a pattern you’re gonna see a lot with hand-written shaders is passing information from the vertex shader stage to the fragment shader stage. A very common use case for that is passing the UV coordinates from the vertices to the fragment shader so they can be used to sample textures and map them onto our objects.

When we get into hand-written shaders you will see that we store the information we want from one stage to another into some structs, which in some contexts you might see them called **interpolators**. So I thought it would be good to give you an idea of what we mean when we say that some date get **interpolated**.

Let’s say your 3D object is a single triangle, with only 3 vertices. Given what we talked in [the previous ShaderQuest part](https://halisavakis.com/shaderquest-part-1-graphics-concepts/), your vertex shader would have a set of data for each of the 3 vertices – including the position, UV coordinates etc. Let’s assume the object’s UVs look like this:

![](../../assets/0dfbb4d284fc3a3e.png)

It’s very fair to assume that the number of pixels this triangle will take on our screen (when it’s visible that is) will be fairly larger than the number of its vertices, which is just 3. Hell, if the object’s large enough it can cover the entire screen! So if we only have the 3 sets of UV coordinates (one for each vertex), how would we know to what UVs a pixel corresponds so that we can sample a texture accordingly?

Here’s where interpolation comes into play. If the pixel we’re examining falls exactly where a vertex is, it’s fair to assume that it’ll utilize the same UV coordinates as the vertex. If, however, it’s in the middle of the bottom two vertices, for example, the UV coordinates it will have will correspond to the middle point of the two vertices, in this case it will be ((0,0) + (1,0)) / 2 = (0.5, 0), because the UVs are being interpolated.

A more visual example of this was with the vertex colors shown in the previous part:

![](../../assets/fba26f1b090676cd.png)

Here only the corner vertices of the top face have vertex colors assigned to them, but you can see the colors blending together and forming gradients between the edges. That’s because the vertex colors of the vertices get interpolated when they get in the fragment shader stage.

### Note

Because in general vertices tend to be less than pixels, vertex shaders usually get called less times than fragment shaders which makes it more effective to perform certain calculations in the vertex shader instead of the fragment shader, as long as we know that the data will be interpolated correctly.

For example, it makes sense to calculate the world position of a vertex in the vertex shader instead of the fragment shader because the position values will be properly interpolated. However, sampling a texture in the vertex shader will give us one color value for each vertex based on its UV coordinates and these colors will be blended together in a manner that is inaccurate compared to the original texture.

## Creating Shaders

Ok, now you know what shaders are and the different shaders out there. Let’s now get into creating them.

### Shader Coding Languages

For hand-written shaders, the most common shader coding languages are:

- CG
- HLSL
- GLSL

The cool thing about these languages is that they’re all very similar in their syntax and the way they operate.

In Unity, most shaders for the built-in rendering pipeline are written in CG, while, more recently, a lot of shaders are written in HLSL for better compatibility with the URP. You can write shaders for the built-in pipeline in HLSL and GLSL as well, but most documentation and tutorials out there favor CG. It doesn’t matter a lot to the engine, though, because in the end the shader will just be converted to GLSL or HLSL, depending on the target platform.

You’ll find a lot of shaders written with GLSL in a plethora of different visual environments, like Shadertoy, as it’s the shading language preferred by application written in OpenGL and WebGL. For example, [the book of shaders](https://thebookofshaders.com) is using GLSL for its interactive examples.

Other environments can use different shading languages, but even when that’s the case, there’s a lot of similarities with languages like the ones above. Therefore, understanding the basic principles of hand-written shader code can help you adjust in pretty much any environment.

### Visual Shader Authoring Tools

In many game development environments there are visual shader authoring tools, usually node-based, that provide a much-needed level of abstraction when it comes to shader creation.

Visual shader creation tools are really useful for quick experimentation and for allowing people with not much experience in shader coding to create any custom effects they can think of.

In general, node-based shader creation tools do not lack any features against hand-written shaders. However, having an idea of what a node-based shader will turn into during compilation is incredibly useful in order to make sure that our shaders will be more flexible and efficient. Additionally, starting with hand-written shaders makes the transition to a node-based tool much easier than the other way around.

With the release of the Scriptable Render Pipelines (URP/HDRP), Unity introduced a node-based shader authoring tool, Shader Graph, while there are other popular third-party tools like Shader Forge and Amplify Shader Editor.

![](https://i0.wp.com/unity.com/sites/default/files/styles/16_9_s_scale_width/public/shader_graph-1-1.jpg?w=1080&ssl=1)

![](../../assets/3ccc5d186f2a0cf0.jpg)

![](../../assets/7f6b074538e43438.png)

Unreal Engine 4 includes its own node-based shader creation tool called Material Editor.

![](../../assets/a5c392cf6a7badf1.png)

While each visual tool has its strengths and weaknesses, they all share a similar approach to shader creation and, much like shading languages, going from one system to another is in most cases an easy transition.

## Conclusion

We’re one step closer to seeing how to start creating shaders in the context of games, but I really wanted to cover some more general information beforehand. I believe that knowing why shaders operate the way they do helps one wrap their head around their weird syntax and their weird restrictions. Even in visual environments, knowing the parallel nature of shaders helps to understand what your nodes operate upon.

In the next part, we’ll probably be taking a look at how shaders and materials are used in the context of game engines, how they get integrated in our scenes and their overall architecture. Hope you’re excited about it!

See you in the [next part of ShaderQuest](https://halisavakis.com/shaderquest-part-3-shaders-and-materials/)❗

## Comments

Great series ! Asking my self to the newsletter ! Thanks !

How do I access the third part T-T

Author

The third part should be now accessible to everone =]

https://halisavakis.com/shaderquest-part-3-shaders-and-materials/