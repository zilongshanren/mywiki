---
title: Graphics Programming weekly - Issue 69 — January 20, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-69/
author: Jendrik Illner
published: '2019-01-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 69 — January 20, 2019

- describes lookup table based (LUT) color grading in LDR color space
- shows how to represent the 3D color space in a 2D image
- LUT is embedded into the picture during color grading and later used to apply the transform at runtime
- walkthrough of the implementation using Unity


- explains how to port an existing iOS OpenGL application to use Metal
- shows everything required for a spinning 3D cube on screen
- including shader authoring, render pipeline creation, uploading of data from the CPU to the GPU and draw call execution
- providing resources for future steps at the end of the article


- implementation of ray marching
- renders the back faces of the bounding volume to determine on which pixels raymarching needs to be done
- simplified absorption model, ignoring the scattering effects
- the vertex shader is used to calculate the ray direction and pass it to the pixel-shader
- lookup texture is used to color to the greyscale information from the 3D volume texture


- cellular noise created from a quadtree grid structure
- presents a method that calculates the optimal order in which neighboring cells need to be visited in 2D
- introduces how to generalize this into higher dimensions and provides a python script can generate lookup tables to store the optimal visit order
- the technique reduces computation time by around 15%


- explains how the distant rain shafts in The Witcher 3 are implemented
- large cylinders in the distant use noise textures with UV distortion
- reading back the scene depth buffer is used to fade out the effect on distance objects
- reverse engineered source code provided


- the first book on raytracing “An Introduction to Ray Tracing” from 1989 is now freely available as PDF


- full path tracing implementation of Quake 2
- implemented Vulkan and the RTX raytracing extension
- uses an adaptive temporal filter for light transport paths to reduce noise


- start of weekly curation of tweets about 3D (technical) art, shaders, and VFX