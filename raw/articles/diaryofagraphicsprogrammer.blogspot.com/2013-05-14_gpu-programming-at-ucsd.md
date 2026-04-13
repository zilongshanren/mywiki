---
title: GPU Programming at UCSD
url: http://diaryofagraphicsprogrammer.blogspot.com/2013/05/gpu-programming-at-ucsd.html
author: Wolfgang Engel
published: '2013-05-14'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

My first outline for a new GPU Programming class at UCSD. Let me know what you think:



First Class

Overview

-- DirectX 11.1 Graphics

-- DirectX 11.1 Compute

-- Tools of the Trade - how to setup your development system


Introduction to DirectX 11.1 Compute

-- Advantages

-- Memory Model

-- Threading Model

-- DirectX 10.x support



Second Class

Simple Compute Case Studies

- PostFX Color Filters

- PostFX Parallel Reduction

- DirectX 11 Mandelbrot

- DirectX 10 Mandelbrot



Third Class

DirectCompute performance optimization

- Histogram optimization case study



Fourth Class

Direct3D 11.1 Graphics Pipeline Part 1

- Direct3D 9 vs. Direct3D 11

- Direct3D 11 vs. Direct3D 11.1

- Resources (typeless memory arrays)

- Resource Views

- Resources Access Intention

- State Objects

- Pipeline Stages

-- Input Assembler

-- Vertex Shader

-- Tessellation

-- Geometry Shader

-- Stream Out

-- Setup / Rasterizer

-- Pixel Shader

-- Output Merger

-- Video en- / decoder access



Fifth Class

Direct3D 11.1 Graphics Pipeline Part 2

-- HLSL

--- Keywords

--- Basic Data Types

--- Vector Data Types

--- Swizzling

--- Write Masks

--- Matrices

--- Type Casting

--- SamplerState

--- Texture Objects

--- Intrinsics

--- Flow Control

-- Case Study: implementing Blinn-Phong lighting with DirectX 11.1

--- Physcially / Observational Lighting Models

--- Local / Global Lighting

--- Lighting Implementation

---- Ambient

---- Diffuse

---- Specular

---- Normal Mapping

---- Self-Shadowing

---- Point Light

---- Spot Light



Sixth Class

Physically Based Lighting

- Normalized Blinn-Phong Lighting Model

- Cook-Torrance Reflectance Model



Seventh Class

Deferred Lighting, AA

- Rendering Many Lights History

- Light Pre-Pass (LPP)

- LPP Implementation

- Efficient Light rendering on DX 9, 10, 11

- Balance Quality / Performance

- MSAA Implementation on DX 10.0, 10.1, XBOX 360, 11

Screen-Space Materials

- Skin



Eight Class

Shadows

- The Shadow Map Basics

- “Attaching” a Shadow Map frustum around a view frustum

- Multi-Frustum Shadow Maps

- Cascaded Shadow Maps (CSM) : Splitting up the View

- CSM Challenges

- Cube Shadow Maps

- Softening the Penumbra

- Soft Shadow Maps



Nineth Class

Order-Independent Transparency

- Depth Peeling

- Reverse Depth Peeling

- Per-Pixel Linked Lists



Tenth Class

Global Illumination Algorithms in Games

- Requirement for Real-Time GI

- Ambient Cubes

- Diffuse Cube Mapping

- Screen-Space Ambient Occlusion

- Screen-Space Global Illumination

- Reflective Shadow Maps

- Splatting Indirect Illumination (SII)

First Class

Overview

-- DirectX 11.1 Graphics

-- DirectX 11.1 Compute

-- Tools of the Trade - how to setup your development system

Introduction to DirectX 11.1 Compute

-- Advantages

-- Memory Model

-- Threading Model

-- DirectX 10.x support

Second Class

Simple Compute Case Studies

- PostFX Color Filters

- PostFX Parallel Reduction

- DirectX 11 Mandelbrot

- DirectX 10 Mandelbrot

Third Class

DirectCompute performance optimization

- Histogram optimization case study

Fourth Class

Direct3D 11.1 Graphics Pipeline Part 1

- Direct3D 9 vs. Direct3D 11

- Direct3D 11 vs. Direct3D 11.1

- Resources (typeless memory arrays)

- Resource Views

- Resources Access Intention

- State Objects

- Pipeline Stages

-- Input Assembler

-- Vertex Shader

-- Tessellation

-- Geometry Shader

-- Stream Out

-- Setup / Rasterizer

-- Pixel Shader

-- Output Merger

-- Video en- / decoder access

Fifth Class

Direct3D 11.1 Graphics Pipeline Part 2

-- HLSL

--- Keywords

--- Basic Data Types

--- Vector Data Types

--- Swizzling

--- Write Masks

--- Matrices

--- Type Casting

--- SamplerState

--- Texture Objects

--- Intrinsics

--- Flow Control

-- Case Study: implementing Blinn-Phong lighting with DirectX 11.1

--- Physcially / Observational Lighting Models

--- Local / Global Lighting

--- Lighting Implementation

---- Ambient

---- Diffuse

---- Specular

---- Normal Mapping

---- Self-Shadowing

---- Point Light

---- Spot Light

Sixth Class

Physically Based Lighting

- Normalized Blinn-Phong Lighting Model

- Cook-Torrance Reflectance Model

Seventh Class

Deferred Lighting, AA

- Rendering Many Lights History

- Light Pre-Pass (LPP)

- LPP Implementation

- Efficient Light rendering on DX 9, 10, 11

- Balance Quality / Performance

- MSAA Implementation on DX 10.0, 10.1, XBOX 360, 11

Screen-Space Materials

- Skin

Eight Class

Shadows

- The Shadow Map Basics

- “Attaching” a Shadow Map frustum around a view frustum

- Multi-Frustum Shadow Maps

- Cascaded Shadow Maps (CSM) : Splitting up the View

- CSM Challenges

- Cube Shadow Maps

- Softening the Penumbra

- Soft Shadow Maps

Nineth Class

Order-Independent Transparency

- Depth Peeling

- Reverse Depth Peeling

- Per-Pixel Linked Lists

Tenth Class

Global Illumination Algorithms in Games

- Requirement for Real-Time GI

- Ambient Cubes

- Diffuse Cube Mapping

- Screen-Space Ambient Occlusion

- Screen-Space Global Illumination

- Reflective Shadow Maps

- Splatting Indirect Illumination (SII)

## 11 comments:

what you think about heterogeneous programming? Is a technique for the present/future and hard to find a good class to learn more about it.

what you think about heterogeneous programming? Is a technique for the present/future and hard to find a good class to learn more about it.

Will this course be open to the public?

Looks like a great syllabus with a lot of interesting topics! My only concern, being a student myself, is the availability of DirectX. Perhaps the situation is different among UCSD students, but in my CS department most everyone is either running Linux (mostly linux) or OS X, and most of the computer labs are running Ubuntu. Finding a machine with DirectX, let alone an up to date DirectX, could prove difficult if I were taking this at my school.

As far as I know the class is part of the extension program at UCSD and so everyone can join.

DirectX: the students bring their notebooks and we set them up in the class. In some of the last classes people also brought MacBooks running MacOS and then they handed in their homework on MacOS. I accept pretty much any hardware / software combination :-)

Heterogenous programming: that's just a marketing term. Any DirectX graphics or compute application is heterogenous programming. You always program parts on the CPU and then other parts on the GPU. You use the processor that is best tailored to the data layout. Similar repeating data might go to the GPU, more complex data -like volumetric data- might go to the CPU ...

Great. But I would like to have a different point of view. What do you think to put anything about OpenGL ?

Great. But I would like to have a different point of view. What do you think to put anything about OpenGL ?

Hello,


The content of this course sounds very interesting. I am located in Singapore, can you tell me if there are any ways to participate at these classe remotely?

Heterogenous programming: the easiest way to learn this is using DirectCompute. It abstracts a bit more than CUDA and OpenCL.


The course is open to the public. As far as I understand UCSD has what they call an extension program.

Wolfgang, will your courses be available to industry professionals looking to up their game?

You want to talk to UCSD about this. As far as I know it is available through the extension program. So in previous years there were people in there that came after work. I give this class starting at 5pm in the afternoon.

Post a Comment