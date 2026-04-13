---
title: Graphics Programming weekly - Issue 82 — April 28, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-82/
author: Jendrik Illner
published: '2019-04-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- shows the window system abstraction
- can be used to render to a window or into an offscreen render target
- how to allocate temporary data that is only required for the duration of the frame

![](../../assets/9af8a25ecbc0e003.png)


- the article describes the process to locate a bug in Babylon.js PBR pipeline
- comparison against other rendering engines confirmed the problem
- caused by the difference between spherical polynomials and spherical harmonics

![](../../assets/b4ddae26ef203384.jpg)


- shows the effect on PBR scene when no tone mapping is applied
- why tone mapping is required and explanation of exposure
- presents how to calculate luminance and the final average exposure required

![](../../assets/5c4a064b65f53646.png)


- presents the process of tone mapping and how curves are used
- shows different kinds of tone mapping curves and their final result
- highlighting what different considerations need to be considered when deciding on a solution

![](../../assets/f12ef115c85399b4.png)


- new PIX version contains a preview of a new timing view
- will support larger capture durations, up to hours
- designed to better visualize a large amount of data collected
- preview because a large number of features are still missing
- team is looking for feedback

![](../../assets/382103cd5544e28e.png)


- presents how render passes are expressed in the user-facing API
- shows how layout transition for external dependencies are handled
- separate logic for user-created, WSI images and transient images
- suggests that barriers should be treated at a higher level inside a frame graph architecture

![](../../assets/f365cda193521657.png)


- presents a new technique for a stochastic sampling of spherical area lights that is suitable for GPU implementations
- able to reduce noise from unoccluded areas significantly
- based on cutting the projected spherical cap into disks and sampling the disks instead

![](../../assets/bf3032facf82e01d.png)


- the second part of the volumetric cloud rendering series
- explains transmittance and phase functions
- 3D path visualization that presents how phase functions influence the way rays traverse the volume

![](../../assets/bd37eccd6b1ba95b.jpg)


- an extended version of the GDC 2019 talk
- overview of AABB and BVH
- shows how to build a BVH using bottom up and top down building algorithms and update dynamically
- presenting different strategies

![](../../assets/39faeec82791bef6.png)

Thanks to [Giuseppe Modarelli](https://twitter.com/gmodarelli) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.