---
title: Graphics Programming weekly - Issue 51 — August 12, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-51/
author: Jendrik Illner
published: '2018-08-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- using ideas from imperfect shadow map point-cloud rendering to implement reflections
- generates a point cloud around the track
- screen space pixels that are close to points of the point cloud transfer their color onto the points
- the point cloud is then projected onto a sphere around the car and used as an environment map to add reflections on the cars

![](../../assets/d6b560fe3bbcfb96.jpg)


- breaks down the engine into two separate related concepts, Resource and Command management
- discusses how to interact with resources
- introduces the idea of state scopes to prevent state leaking
- commands are recorded into engine specific command buffers that are later converted into the API specific format

![](../../assets/fc5f51c537bd5145.png)


- Nvidia tutorial on how to integrate DirectX raytracing and rasterization so that both rendering paths can be used within the same application
- how to initialize the API, create DXR acceleration structures
- how the ray tracing pipeline works, manage shaders, resources, and shader binding tables
- implementation of the required raytracing shaders to produce identical results with the rasterization pipeline

![](../../assets/7bcaa419fea900a4.jpg)


. short description of the different aspects of the Disney BSDF, including source code

![](../../assets/3fbc765b56d0afe1.png)

- a technique to render screen space water using unity
- water particles write information into offscreen buffers to accumulate water information
- these buffers are then resolved to form a continues water surface instead of individual blobs

![](../../assets/9994584ea8eab65e.png)


- improves upon the multiple scattering approximation from the previous part of the series
- the result is a model that only requires a 2D LUT to be pre-calculated

![](../../assets/36233c8d017fc819.png)


- walkthrough of two vegetation shaders created with the visual shader editor that was added in Unity 2018.1

![](../../assets/3a4fea4bc9516ba5.png)


- how to improve the generation of uniform points in a sphere, disk, and a spherically capped cone

![](../../assets/f448941a14077390.png)

- a tutorial that shows how to clip a mesh in a pixel shader against a plane using unity

![](../../assets/2a56141f10501e61.png)

- a web tool that allows the conversion from HLSL Shaders to HLSL 6.2, GLSL 4.5 and Metal 2.1

![](../../assets/1268e0adc737e07e.png)

- choosing a different algorithm to optimize triangle-ray intersection tests and vectorizing the calculations

![](../../assets/eb8d3df4843fc19d.png)


- explores source to source optimizations techniques using the LunarGlass framework with GLSL shaders
- comparison of different optimization techniques and the effects on runtime performance
- results vary significantly between different shaders and target platforms

![](../../assets/a6669cac2191f0b9.png)


- overview of libraries available to write GPGPU applications using the Rust programming language

- description of the “unlit” light system being used
- it allows lights to modify tint, brightness and contrast to enable the 2D characters to match the environment better

![](../../assets/71320c3a62b9a33b.png)


- a short explanation and Metal shader code for different blend modes as described in the PDF specification

![](../../assets/bba80cccb8ae6b89.jpg)

- overview of different fire effects that are based around animated noise textures

![](../../assets/e67bfb2e77f4efb9.png)

- overview of different rain effects with links to more in-depth articles discussing the showcased effects

![](../../assets/4d7e6c49740f2574.jpg)