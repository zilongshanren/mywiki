---
title: Graphics Programming weekly - Issue 196 - August 15, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-196/
author: Jendrik Illner
published: '2021-08-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the talk presents how Activision had to rethink the geometry pipeline when moving from tightly controlled levels to open worlds
- focusing on the shipped F+ and experimental V+ implementation
- shows what mesh types use what technique and explains the reasons
- showing how the GPU based pipeline has been implemented around bitmasks and data expansion
- presents performance numbers, final F+ culling pipeline reduces rendering time significantly
- additionally contains a look at a possible tile-based V+ / F+ hybrid pipeline

![](../../assets/c2738b4c9e5c829d.png)


- the video discusses biases and assumptions that are baked into the graphics research
- discussing the biases in terms such as skin, hair, flesh tones, human face
- presents a look at history and how the same biases developed, and how it has been repeated
- suggests future developments to address these biases going forward

![](../../assets/a83b39c0ab03de5b.png)


- the article presents a new D3D12 Nvidia extension that enables a developer to allocate CPU-Visible VRAM memory directly
- this allows developers to write directly into VRAM from the GPU
- explains what tools are available to detect cases where it would be beneficial
- additionally shows how to detect possible performance problems caused by reading from the CPU

![](../../assets/22393f135c399a16.png)


We are searching for a highly skilled and experienced Senior Render Programmer.

You could be developing state-of-the-art rendering solutions for our in-house game engine VRAGE, games such as Space Engineers or new, unannounced projects.

You’ll be working as part of the Rendering team, working closely with the Art and Design teams to help them achieve the artistic vision for our games.

![](../../assets/c52b264efd534de6.png)


- the paper presents a new distance sampling method
- presents an extension for the null-collision integral formulation that improves efficiency for low-order heterogeneous (such as fog)
- additionally presents an approach using a spatial guiding data structure

![](../../assets/30d9e058b8a15810.png)


- the article presents a polygon extension-based method for the generation of 2D shadows
- explains the necessary math and how to generate the required mesh data
- also discusses problems, performance implications, and optimization techniques
- additionally presents two alternative techniques

![](../../assets/e75ce210bd020a6f.png)


- the blog post extends the previously discussed hard shadow method to support penumbra based soft shadows
- presents how to generate the mesh data to include the penumbra and be able to derive the falloff from linear operations
- presents the shader implementation using GLSL

![](../../assets/337cf083bc130b0e.png)


- the blog post presents a new helper class (CD3DX12FeatureSupport) that unifies the D3D12 feature checking into a single class
- part of d3dx12
- aims to unify the patterns and behavior across the different existing methods in stock d3d12

![](../../assets/408ea71fa129f0ab.png)


- the article presents an overview of a master thesis about caching shading information in world space
- technique is based on implicit point generation and accumulation into global hash tables
- the presented example shows the technique applied for ambient occlusion

![](../../assets/33c04e99e467e414.png)


Pilotier is a startup tackling one of the toughest outstanding engineering challenges: autonomous urban driving. We are taking a camera-first approach and are designing for hardware that is two to three years out. If you like big challenges and working with smart people, join us on our quest.

Your job will be to collaborate with simulation and deep learning engineers and help us build a ground-breaking product from scratch.

You have an eclectic background. You’ve delved deep into the graphics pipeline. You’ve worked with game engines. Maybe you’ve built your own. You’ve written many lines of C++ (even though maybe you secretly can’t stand it). You like solving hard problems, startups, and working with smart people. Nothing scares you. Vulkan? Hah! Maybe you’ve dabbled with functional programming languages, like Erlang or Elixir. Perhaps even Haskell. You’re independent and self-motivated. You love learning new things. Nothing is impossible, some things just take a bit longer to figure out. It’s just code.

We are based in Montreal but are all remote, so your physical location is not an issue.

![](../../assets/74819a5301d0777c.png)


- course page for the content of Siggraph 2021
- covering Spatial Upscaling through FidelityFX, Concurrent Binary Trees for Large-scale Terrain Rendering
- Nanite Virtualized Geometry, Large-Scale Global Illumination
- Lighting, Atmosphere, and Tonemapping in Ghost of Tsushima and Global Illumination Based on Surfels

![](../../assets/079a2b5f01925265.png)


- a new course happening for the first time in 2021
- focusing on the architectural aspect of real-time rendering engines
- currently publicly released slides include
- Activision Engine Architecture and Geometry Rendering Pipeline
- Roblox / Unity Rendering Engine Architecture,

![](../../assets/fb87d41d0c12693f.png)


- article presents how tone mapping can be implemented into UE 4 using Vulkan sub passes
- shows how much more efficient the implementation is on Quest2 when using sub passes vs. an additional render pass

![](../../assets/6d3bf39596a41abe.png)

Thanks to [Matt Pharr](https://pharr.org/matt) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.