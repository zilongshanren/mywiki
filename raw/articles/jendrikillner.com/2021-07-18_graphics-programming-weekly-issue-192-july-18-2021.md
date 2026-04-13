---
title: Graphics Programming weekly - Issue 192 - July 18, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-192/
author: Jendrik Illner
published: '2021-07-18'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents a method that decouples geometry samples from shading samples
- explains the difference of human vision between the ability to detect edge aliasing and internal aliasing and why geometric frequency is required to be higher
- explains performance implication of triangle sizes and MSAA
- shows how TAA, MSAA, and Decoupled Visibility Multisampling (DMV) compare in performance and quality

![](../../assets/3b59a8e3be90304e.jpg)


- the article presents a refresher on the concept of slope
- shows that slope space is a representation for unit vectors in the upper
- presents the properties of slope space, what advantages it has
- additionally discusses how slope space is used in normal distribution functions (NDF)

![](../../assets/d8b6f2332ac51b13.png)


- the article explains how the destruction system was implemented
- based around a world map damage textures that contain a mask to mark destroyed areas
- this mask is then sampled during a geometry to cull and transform geometry to represent the destruction

![](../../assets/9097476f17e9912d.jpg)


- the article presents a natural SDF based detail mapping / Fractal Noise displacement mapping
- technique presented uses spheres of varying radius to represent a varying level of octaves to represent the details
- presents how to combine the different layers and suggests alternative possibilities
- additionally presents a video that shows a clear visualization of the different layers being combined

![](../../assets/5715944b7a7893bf.jpg)


nDreams is a world-leading virtual reality game developer and publisher, combining innovation with excellence. Our projects are a leap forward for VR and for the studio and we are looking for talented people to help turn them into a reality.

We’re the studio behind the #1 Selling, Best of E3 Award-winning, Phantom: Covert Ops and we’ve got several exciting projects planned for 2021 and beyond, including Fracked, our recently announced PS VR exclusive. Once you’ve seen what we’re up to, we’re convinced you’ll want to be involved…

Our artists believe in the power of VR to immerse and entertain players like no other medium can. We are seeking a Principal Technical Artist to collaborate with and support the team, ensuring their content looks great in-game whilst adhering to the technical constraints of projects and hardware. Whether you are a games industry veteran or an experienced VFX Technical Artist/Director who’d like to make a change, we’d love to hear from you.


- collection of tweets about technical art
- covering particles, stylized shading, portfolios, and game breakdowns

![](../../assets/45dc0932d0f35864.png)



- the article explains how a visibility buffer approach is used
- presents how the shading pass has been implemented (Frostbite BRDF, tangent frames, …)
- covers area light implementation using Linearly transformed cosines and compares different representation and discuss the tradeoffs
- additionally covers different noise types and the effect on denoising

![](../../assets/4de622ec2271d5d0.png)


- the first part of the series discusses where mobile GPUs are used
- presents how the hardware design is setup
- shows how power usage and thermal efficiency budgets are influencing all systems on a chip

![](../../assets/2303c182fdb40d70.png)


- pre-release chapter from ray tracing gems 2
- presents weighted reservoir sampling, a technique for the efficient sampling stochastic data
- shows how optimized variants of algorithms exist to sample with different properties, weighting behaviors, or duplicate output behavior

![](../../assets/8c0411456847e77b.png)


- the source code for the technique has been published on Github
- also contains a sample implementation of how it can be integrated
- the technique only relies on color buffer information for the upsampling pass

![](../../assets/d3d899f3783b4eff.png)

Thanks to [Jens Hartmann](http://top-or.de/projects) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.