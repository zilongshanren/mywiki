---
title: Graphics Programming weekly - Issue 191 - July 11, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-191/
author: Jendrik Illner
published: '2021-07-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of The Visibility Buffer approach
- compares the technique against forward and deferred shading at varying texture densities
- presenting performance results
- including a discussion of derivative calculation and the effect on helper lanes
- additionally discusses several considerations and future developments

![](../../assets/1c4793bb06dd57a0.jpg)


- Alex covers many ideas and algorithms
- classical tools require the artist to deal with technical aspects at all time
- removing soft constraints allows the artist to focus on the art
- presents how cluster culling and LOD selection removes the polygon count soft constraint
- shows different ways to work with SDFs
- closes with a look at the volumetric rendering and Neural Radiance Fields (NeRF)

![](../../assets/2040e41ebca422fc.png)


- collection of ray tracing experiments and presentation of results
- covering ray divergence, hybrid global illumination, shadow mapped GI
- additionally shows the effect of second bounce GI as well as improved reverse z-buffer precision

![](../../assets/9660347db5a1681d.png)


nDreams is a world-leading virtual reality game developer and publisher, combining innovation with excellence. Our projects are a leap forward for VR and for the studio and we are looking for talented people to help turn them into a reality.

We’re the studio behind the #1 Selling, Best of E3 Award-winning, Phantom: Covert Ops and we’ve got several exciting projects planned for 2021 and beyond, including Fracked, our recently announced PS VR exclusive. Once you’ve seen what we’re up to, we’re convinced you’ll want to be involved…

Our artists believe in the power of VR to immerse and entertain players like no other medium can. We are seeking a Principal Technical Artist to collaborate with and support the team, ensuring their content looks great in-game whilst adhering to the technical constraints of projects and hardware. Whether you are a games industry veteran or an experienced VFX Technical Artist/Director who’d like to make a change, we’d love to hear from you.


- first free chapter from ray tracing gems 2 has been released
- discusses the implementation of a path tracer that is aimed at being us as a reference renderer for in-engine integration
- source code is provided

![](../../assets/1c8a539bb58c70a0.png)


- author presents an introduction to automated visual testing
- discusses how to reduce the combinations that need to be tested
- how to make sure that runs are deterministic
- additionally provides source examples of how to use python to run the visual testing

![](../../assets/a18593669a425269.jpg)


- the blog post discusses if it makes sense to compare images in the frequency domain
- presents a few typical approaches, discuss their shortcomings and recommendations

![](../../assets/332275882ce8693f.png)


- preview video if a view of the papers presented at HPG 2021
- see the video presentation of the papers in
[day 1](https://www.youtube.com/watch?v=eGfX1iWzkh0)

![](../../assets/92f70c5ab4769aea.png)


- second part of the series explaining the WebGPU basics by presenting the equivalent concepts from a metal perspective
- shows how to apply displacement mapping onto a plane to approximate a terrain
- covers how to load and sample textures
- resource binding, pipeline setup for 3d depth testing enabled

![](../../assets/0bb8daefdab10e75.png)


- the article presents a brief overview of NeRF (neural radiance fields)
- then presents 3 methods that enable the relighting
- discussing differences and tradeoffs between the techniques

![](../../assets/4af5068f81c5f57f.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.