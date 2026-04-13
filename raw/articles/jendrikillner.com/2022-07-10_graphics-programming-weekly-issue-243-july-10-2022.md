---
title: Graphics Programming weekly - Issue 243 - July 10, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-243/
author: Jendrik Illner
published: '2022-07-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper discusses a decoupled shading implementation that separates rasterization from shading by shading pixels before they are rasterized
- presents how it determines what pixels will need to be shaded
- what space to allocate for storing the shading results and how to execute the shading
- discusses strengths and weaknesses of the approach
- presents performance comparisons against a forward shading implementation
- it additionally covers numerous considerations that are required for a robust implementation

![](../../assets/5bdd8ceca2a0519c.png)


- the paper presents how to generate multiple 2D blue noise textures so that the blue noise is both spatially and temporally a blue noise pattern
- the presented solution is a drop-in replacement for applications that are already using independent blue noise textures
- discusses how to generate the textures and compare multiple methods
- it additionally presents a comparison of the technique in multiple test cases and compares against other methods
- take a look at the supplemental for more practical information for real-time use cases

![](../../assets/f56bce328ca6605c.png)


The Indie Stone, developers of Project Zomboid, are looking for AAA coders to join them on their quest for the ultimate zombie survival simulation.

The applicant would be in charge of maintaining and developing our game’s animation system for Project Zomboid using a custom built OpenGL engine, while also working with the animator to improve our output, systems and toolset. Initial tasks would deal with root motion, blending and masking – later moving on to integration of inverse kinematics and ragdoll physics.

The Zomboid team is small and have their fingers in a lot of pies, so there are many opportunities to get involved in other areas of the game too - depending on the applicant’s skillset.

Competitive salary and a prominent role in a tight, passionate team. Remote and flexible working, anti-crunch mindset.

![](../../assets/c1e70cae43ef992a.jpg)


- the 4-hour video stream discusses the evolution of the Vulkan API
- discusses the underlying concepts, issues, and how the changes in Vulkan 1.3 try to improve
- talking about pipeline management, render passes, new synchronization API
- it additionally also covers the other more minor extensions added to the core

![](../../assets/a697d8706dd640e7.png)


- the paper presents a neural network architecture that allows both denoising and supersampling to be applied as part of a single network
- this is achieved by sharing a joint feature extractor
- discusses the different stages of the network, what inputs are required and how they interact
- presents a comparison against existing solutions and offers performance numbers

![](../../assets/ee69f131948e481d.png)


- the paper presents a new GPU-based method to generate 2D contour strokes from 3D meshes
- proposed solution uses a preprocessing step to analyze the adjacency and geometric information
- discusses the different steps of implementation
- it additionally shows how to further utilize the counter edge lines to support different patterns
- example implementation in Unity is provided

![](../../assets/fd03d81be09fe224.png)


- the lesson provides the foundations of ray marching through a volume
- explains how light interacts with a medium, introducing the required terms along the way

![](../../assets/6843abd2a7fd6501.png)


Double Fine Productions is looking for a full time graphics programmer to join its San Francisco based development studio. Having recently shipped the award winning Psychonauts 2, we are looking to expand our graphics and systems programming team to support the development of our future titles.

You will be responsible for developing rendering features, optimizing game performance and memory usage, and building low level systems on PC and Xbox.

Applicants should have a strong preference for working in a highly creative, innovative, and nimble development environment, where collaborating with design, audio, art, animation, tech, and other disciplines is standard.

![](../../assets/27034fe5c580ce80.png)


- the new home for the AMD research team
- provides a collection of publications, projects, presentations as well as blog posts

![](../../assets/0d7a885c03f36e82.png)


- the post provides a walkthrough of all the D3D12 elements that are involved in getting started with a raytracing workload
- discusses the different concepts and how they relate to each other
- shows how to author raytracing shaders
- it additionally shows how the integration in Microsoft Mini Engine has been achieved

![](../../assets/ed937d673ed51a46.png)


- the paper introduces a visibility-aware transmittance sampling technique for rendering atmospheric scattering
- this is achieved by adjusting the sample locations along the view vector past the shadow boundary so that all samples contribute meaningful data
- compares the solutions against others and presents cases where the proposed solution is not able to improve
- it additionally provides an example of a CPU implementation

![](../../assets/3a554f15adea94fd.png)

Thanks to [Jonathan Tinkham](https://zincfox.red) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.