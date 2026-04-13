---
title: CSE 190 - GPU Programming UCSD class Winter 2014
url: http://diaryofagraphicsprogrammer.blogspot.com/2014/01/cse-190-gpu-programming-ucsd-class.html
author: Wolfgang Engel
published: '2014-01-02'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

GPU Programming

With the new console generation and the advances in PC hardware, compute support is becoming more important in games. The new course in 2014 will therefore start with compute and we will spend about a 1/3 of the whole course talking about how it is used on next-gen consoles and in next-gen games. We will also look into several case studies and discuss the feasibility to "re-factor" existing game algorithms so that they run in compute. An emphasis is put here on effects that are traditionally used for post-processing effects.


The remaining 2 / 3 of the course will focus on the DirectX 11.2 graphics API and how it is used in games to create a rendering engine for a next-gen game. We will cover most of the fundamental concepts like the HLSL language, renderer design, lighting in games, how to generate shadows and we also discuss how transparency can be mimicked with techniques other than alpha blending.

The course will end with a survey of different real-time Global Illumination algorithms that are used in different types of games.



First Class

Overview

-- DirectX 11.2 Graphics

-- DirectX 11.2 Compute

-- Tools of the Trade - how to setup your development system

Introduction to DirectX 11.2 Compute

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

Direct3D 11.2 Graphics Pipeline Part 1

- Direct3D 9 vs. Direct3D 11

- Direct3D 11 vs. Direct3D 11.1

- Direct3D 11.1 vs. Direct3D 11.2

- Resources (typeless memory arrays)

- Resource Views

- Resources Access Intention

- State Objects

- Pipeline Stages

-- Input Assembler

-- Vertex Shader

-- Tesselation

-- Geometry Shader

-- Stream Out

-- Setup / Rasterizer

-- Pixel Shader

-- Output Merger

-- Video en- / decoder access


Fifth Class

Direct3D 11.2 Graphics Pipeline Part 2

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

-- Case Study: implementing Blinn-Phong lighting with DirectX 11.2

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


Eigth Class

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


Prerequisite

Each student should bring a DirectX 11.0 or higher capable notebook with Windows 7 or 8 into class. All the examples accompanying the class are build in C/C++ in Visual Studio 2013.

With the new console generation and the advances in PC hardware, compute support is becoming more important in games. The new course in 2014 will therefore start with compute and we will spend about a 1/3 of the whole course talking about how it is used on next-gen consoles and in next-gen games. We will also look into several case studies and discuss the feasibility to "re-factor" existing game algorithms so that they run in compute. An emphasis is put here on effects that are traditionally used for post-processing effects.

The remaining 2 / 3 of the course will focus on the DirectX 11.2 graphics API and how it is used in games to create a rendering engine for a next-gen game. We will cover most of the fundamental concepts like the HLSL language, renderer design, lighting in games, how to generate shadows and we also discuss how transparency can be mimicked with techniques other than alpha blending.

The course will end with a survey of different real-time Global Illumination algorithms that are used in different types of games.

First Class

Overview

-- DirectX 11.2 Graphics

-- DirectX 11.2 Compute

-- Tools of the Trade - how to setup your development system

Introduction to DirectX 11.2 Compute

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

Direct3D 11.2 Graphics Pipeline Part 1

- Direct3D 9 vs. Direct3D 11

- Direct3D 11 vs. Direct3D 11.1

- Direct3D 11.1 vs. Direct3D 11.2

- Resources (typeless memory arrays)

- Resource Views

- Resources Access Intention

- State Objects

- Pipeline Stages

-- Input Assembler

-- Vertex Shader

-- Tesselation

-- Geometry Shader

-- Stream Out

-- Setup / Rasterizer

-- Pixel Shader

-- Output Merger

-- Video en- / decoder access

Fifth Class

Direct3D 11.2 Graphics Pipeline Part 2

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

-- Case Study: implementing Blinn-Phong lighting with DirectX 11.2

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

Eigth Class

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

Prerequisite

Each student should bring a DirectX 11.0 or higher capable notebook with Windows 7 or 8 into class. All the examples accompanying the class are build in C/C++ in Visual Studio 2013.

## 4 comments:

Will it be possible to post your course lecture slides online somewhere so that others can make use of this awesome course?

Yeah, anything like that would be hugely welcome as I'm from Europe

I am wondering this as well, is there anywhere the classes lecture notes/slides are posted?

How many hours one class lasts?

Post a Comment