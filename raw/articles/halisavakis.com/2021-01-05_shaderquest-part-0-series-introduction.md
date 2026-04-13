---
title: 'ShaderQuest Part 0: Series Introduction'
url: https://halisavakis.com/shaderquest-part-0-series-introduction/
published: '2021-01-05'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Introduction

Well hi there, and welcome to the first part of ShaderQuest! This is the first entry of the series, which will go through what this series is all about, as well as some setup information.

## What is ShaderQuest

ShaderQuest is a new series of shader tutorials that focuses on going through specific shader concepts and tools. Its purpose is to be a jumping off point to shader creation for games.

While the examples and use cases will use Unity, the themes shown will be generic enough to cover shader creation in other environments as well. I will also try to include references to other shader creation environments (like simple GLSL or UE’s Material Editor) to get a more holistic perspective of how shaders operate within a rendering environment.

One of the great things about shaders is that they’re the same pretty much anywhere, be it in Shadertoy, via a node-based editor like Shader Graph or even in other environments, like Substance Designer.

## The purpose of ShaderQuest

The main purpose of this series is not to provide you with solutions to specific problems, but, instead, give you a good idea of the basic blocks you can use to approach different effects and create your own shaders.

This series will also focus on the coding side of shaders so you can take a better look of what’s happening under the hood of your node-based shaders. This will not only give you a better understanding of how a node-based shader performs, but if will also give you more control over the effects you’re authoring in any environment.

The series will also work as a good reference point for various concepts, as I will try to keep each post focused on a specific theme and present different examples and use cases on that.

## Future posts

The list of future posts is still being processed, but I thought I’d give you a first idea of what to expect from this series. Keep in mind that the order of these is subject to change and two or more posts might get merged into one.

- Introduction to basic graphics concepts: materials, vertices, edges, faces, UVs, normals
- Introduction to shaders: what are shaders, different types of shaders, different development environments. Creating shader files/objects, applying them to materials, going through the architecture of shaders in different environments.
- Different Unity shader types: vertex-fragment/ surface, lit/unlit. Opaque and transparent materials.
- Forward and deferred rendering.
- Colors, HDR colors, adding and multiplying colors (maybe blending too).
- Helper functions – Sin, Cos, Frac and Time
- Helper functions – Step, Smoothstep, Lerp.
- UV coordinates, UV manipulation & displacement.
- Textures, sampling textures, scaling and offset. Getting a color from a texture and blending it with other colors.
- Using textures with textures – masking & texture-based displacement.
- Alpha clipping – clip/discard – dissolving effects.
- Basic vector math – adding, subtracting vectors, scalar multiplication.
- Basic vector math – Dot product & Cross product
- Lighting: Lighting models, diffuse and specular lighting, Fresnel.
- Spaces – Object space, world space and transforming from one to the other.
- Spaces – world and screen space texture mapping.
- Vertex displacement.
- Grab pass.
- Stencil shaders.
- Shader creation practices – cginc files and subgraphs, keywords.
- Image effects – pipeline and shaders.
- Shaders for texture generation tools.
- A vertex-fragment shader for the deferred rendering path.
- Custom render textures.
- Parallax effects.

## Setup

As I mentioned, the examples will focus more on Unity shaders, but I’ll try to keep the concepts as generic as possible so you could follow along in different environments as well.

Once I get into more hands-on themes, I’ll start sharing two Unity projects (one in built-in and one in URP) on GitHub that I’ll be updating with each new post, so that you can play around with the examples yourself.

Therefore, if you want to follow along with the Unity examples, I suggest [you download and install Unity](https://unity3d.com/get-unity/download) (I’m using version 2020.2.1 at the time of writing this).

## (Probably) F.A.Q.

### Why start a new series?

When I started out with shaders, what really helped me was to try and recreate specific effects and research implementations from other artists. From there I tried to reverse engineer the shaders, change stuff around and see what stuff did until I figured out how the different pieces and black boxes worked. That’s why the “My take on shaders” series focuses on specific effects and shaders and goes through them in detail. I still believe the series is a good reference point for specific effects, but I wanted to create a new series that helps people understand the presented concepts from the bottom up.

### Will there be more posts from “My take on shaders”?

Yeah, of course. I don’t plan on stopping “My take on shaders”, even though I might have a bit of trouble maintaining both series. New issues might be a bit more spread out, but I think it’s worth it.

### Will the series cover shaders made in Shader Graph?

Yes! All the examples will cover both shader coding for the built-in pipeline as well as shader creation via Shader Graph.

### Will the series cover shaders for UE4?

I really really want to and I will try to include as many examples as I can from UE4 as well. My current computer might not easily handle UE4, which will probably make it difficult to set up a lot of examples there, but I’ll do my best!

### What language will the shaders be written in?

Since I’ll be showing examples in the built-in render pipeline I’ll mostly be showing code written in CG. However, I’ll try to mention other syntaxes (like HLSL or GLSL) wherever applicable.

## Other resources

There’s some other great resources to get started as well, some of which you can find under [my archive page](https://halisavakis.com/archive/). For more generic shader tutorials I can’t recommend [the book of shaders](https://thebookofshaders.com) enough. Also, for Unity-specific tutorials for beginners, [Manuela’s tutorial series](https://www.patreon.com/teamdogpit) is probably the best one out there, so you can check that out as well.

## Disclaimer

While I definitely know a lot more now than I did when I started out “My take on shaders”, I’m still nothing close to a shader master. I’ll do my best to present what I know with as much accuracy as possible but it’s always helpful to keep in mind that, y’know, I’m still learning as well. I might not have it in the title this time, but I’ll once again mostly be presenting **my take** **on **shaders. I’ll make sure to acknowledge and correct any inaccurate piece of information I may write down but also keep in mind that I’m in no way infallible.

## Conclusion

I’m excited to start this new series and I really hope you are as well. I definitely think it will be easier for me to get more posts out too, so I think we’ll all win from this new series.

I’m always open to suggestions and feedback and I look forward to hearing your impressions on this new series.

So, let’s get you started on your ShaderQuest!

## Comments

Thanks, I found it easy to understand. Looking forward to part 1.