---
title: Graphics Programming weekly - Issue 182 — May 9, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-182/
author: Jendrik Illner
published: '2021-05-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper investigates how shading reuse is perceived when visibility and shading rate is decoupled
- presents that even in dynamic scenes, it’s possible to reuse a large amount of shading information
- shows different methods that can be used to predictively shade, compares the results, and present limitations

![](../../assets/1fe45f18745559bd.png)


- the paper presents extensions and improvements to the probe-based irradiance-field-with-visibility representation technique
- presents a multiresolution cascaded volumes representation to support large worlds
- improved probe pruning, faster convergence through perception-based irradiance encoding
- additionally presents how to use irradiance probes to shade glossy reflection rays

![](../../assets/c4a0bd61011a5ef5.png)


- the video explains how to generate 2D Perlin noise and how to use it in Unity
- provides sources for other noise kinds
- additionally presents a few examples of how to use Noise

![](../../assets/8193127253981543.png)


We are looking for a Rendering Engineer with experience in developing high-quality, high-performance software: in games or otherwise.

This role will suit someone who is keen to take the next step forward in their career and in interactive tech. We are working on core immersive technology that spans the full range of XR, and this is an opportunity to help shape the future of spatial computing.

Simul is an established leader in real-time graphics middleware; the company’s customers include Bandai Namco, Microsoft Game Studios, Sony, and Ubisoft. In 2020, Simul won the TIGA 2020 Best Technical Innovation Award for our work on trueSKY, the leading real-time weather SDK. We have a culture of agile development focused on quality, performance and precision. We believe in equal opportunity and a diverse, inclusive and supportive workplace.

You will be:

- Researching and developing new immersive technologies,
- Working in an agile team,
- Finding and fixing bugs and performance issues,
- Profiling and optimizing CPU, GPU and network code,
- Representing Simul at technical and non-technical events, in-person and online.

The benefits Simul offers are:

- Flexible remote working,
- Regular salary reviews and career progression,
- 22 days holiday + bank holidays,
- Dedicated self-development time.

![](../../assets/ff7737dd6e745c46.png)


- presents how D3D12 Raytracing support was implemented in Battlefield V
- mix of screenspace reflections and raytracing
- shows the pipeline implementation, adaptive ray count selection, ray defragmentation, binning, and denoising
- techniques to improve BVH updates, culling hierarchies, partial updates,
- how to deal with shader graph authored shaders, integration with shading, particles, and vegetation

![](../../assets/6691c24fc07f1b73.png)


- the article presents a walkthrough of the API abstractions on top of D3D11, D3D12, and Vulkan used in the Wicked Engine
- shows the resource, pipeline, command list, queues, and barrier abstractions
- discussing some limitations of the current approach and how it might develop in the future

![](../../assets/c6846671d0b5cee7.png)


- an interactive article about debugging a C++ crash
- more about C++ than graphics, but I really liked the interactive article :)

![](../../assets/fb2eac4763599284.png)

- the article shows how to generate planes, cones, cylinders, and a torus
- implementation provided in C++

![](../../assets/3345d2757a2fc5dc.png)


- the paper presents a novel model that splits a Direct Delta Mush into two layers
- this can approximate the deformation with improved runtime performance and lower memory requirement
- the video shows a comparison against other methods
- additionally presents performance numbers for the technique

![](../../assets/4614fa0fe70caaef.png)


- the paper presents antithetic variance reduction technique used to estimate the interior integrals
- shows the usage of the technique for Monte Carlo differentiable rendering of glossy and BSDFs
- antithetic sampling is the use of negatively correlated samples instead of independent samples

![](../../assets/9e89eb003b54523d.png)


- Two Minute Paper provides an overview of the Interactive Wood Combustion for Botanical Tree Models paper from 2017
- shows what parameters are exposed, what kind of effects it can generate

![](../../assets/4b405e72b1cba623.png)

Thanks to [Adalberto Bruno](https://www.linkedin.com/in/adalbertobruno/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.