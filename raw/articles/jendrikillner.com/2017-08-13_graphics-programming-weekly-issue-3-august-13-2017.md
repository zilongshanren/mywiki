---
title: Graphics Programming weekly - Issue 3 — August 13, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-3/
author: Jendrik Illner
published: '2017-08-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

A basic Gaussian convolution can achieve linear time complexity by performing a horizontal and vertical pass. This is not possible when the target shape of the convolution is a circle. When performing a blur in the frequency domain it is possible to achieve separability

A shadertoy implementation of circular depth of field with inspiration by the paper above

Handling multi-monitor setups with various DPI-scaling per monitor cleanly does not have to be tricky. A good overview of the windows DPI related APIs

Photogrammetry workflow, the technology behind the de-lighting tool and how to get started with photogrammetry in Unity.

workflow e-book: [download](https://unity3d.com/files/solutions/photogrammetry/Unity-Photogrammetry-Workflow_2017-07_v2.pdf)

A new bounding shape approximation algorithm which takes as input an arbitrary surface mesh and generates a bounding shape proxy

SSR are expected to be less expensive than actual reflection rendering and more accurate than cubemap-based reflections, as long as the reflection source is present on the screen.

In controlled situations flaws can be alleviated and SSR can deliver astonishing results.

- clearly written article with code examples
- how to resolve common problems

- constrained form of SSR
- reverse the reflection tracing
- calculate which pixel is hit in the reflection, resolve later without searching
- can be selectively used where applicable
- normal maps can be approximated, but more costly
- shader code example

- meshing
- handling elevation changes and smooth LOD transitions

- overview of wave interactions
- using a shape texture to displace the mesh surface

- foam rendering and depth peeling
- two layer foams, for under and above water based on displacement texture
- using multiple layers of surface information to better approximate under water scattering


- Effect parser for Vulkan
- Offline(Generates C++) or runtime integration
- Assembling PSO in file
- Assembling shader fragments for the final shader
- Connecting depending data

- Resource Definitions and connections

A diagram that shows all of the Vulkan objects and some of their relationships, especially the order in which you create one from another and a brief description of all the objects

- Lightmaps & Light probes
- Light probes
- Decoubled visibility and incoming radiance
- Visibility baking

- Light Grid
- volumetric structure that holds the indirect lighting for the level

- Light Baking

Over at Siggraph I had a discussion with some mobile GPU engineers about the pros and cons of tiled deferred rasterization. I prompted some discussion over Twitter (and privately) as well, and this is how I understand the matter of tiled versus immediate/“forward” hardware rasterization so far…


- History of anti-aliasing techniques with description of new developments in each generation

Explanation of what Alpha to Coverage is and how to use it to reduce aliasing on alpha tested geometry with MSAA

In daylight dim lights behave local (only relevant to the nearby geometry), but in a dark room small contributions add up to significant light for the whole scene. So their behavior is global. And the latter is the real problem we’re solving here.


- build a BVH of the emitter geometry
- importance measure to be able to traverse the cluster tree

Forward may be a losing proposition on current hardware, but if this talk is about things we want to make the hardware guys do for us, then getting them to fix forward rendering is certainly on the table.

I think we might be taking for granted just how much the inline everything model has been protecting us from ourselves


- dynamic register usage adjustments
- taking C++ code and executing it directly on the GPU

- extended area-lighting framework with lines, disks and spheres
- recap of LTC
- Line lights
- Sphere / Disk Lights

Implementing real-time partial occlusion depth of field using deep G-Buffers. Partial occlusion depth of field is where sharp background objects bleed through the edges of blurry foreground objects

Introduce an extension to microfacet models that enables to add thin-film interference appearance, a thin-film model that is spectrally antialiased.


There are small arrows in the bottom right corner, need to click them otherwise slides wouldn’t change for me

Virtual reality will be the new interface to computing for everyone


- future of VR/AR technology
- rendering pipeline and adjustements for latency reduction
- future techniques to get the required fidelity
- light fields, future displays
- haptic feedback systems
- display based reprojection
- path tracing