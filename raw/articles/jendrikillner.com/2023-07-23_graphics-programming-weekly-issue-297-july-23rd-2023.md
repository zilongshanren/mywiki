---
title: Graphics Programming weekly - Issue 297 - July 23rd 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-297/
author: Jendrik Illner
published: '2023-07-23'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the talk presents is a combination of leadership methods and rendering techniques of God of War Ragnarök
- covering lightings units, optimization techniques, PS5 Enhacements such as raytraced cubemaps reflections
- presents optimization appraoches used for shadows, geometry, and how it was tracked

![](../../assets/07ba196b0cda336b.png)


- the article provides a list of best practice recommendations for usage of PSOs with D3D12
- additionally also presents what patterns are not recommendation
- explaining why these recommendations are made

![](../../assets/fc05f62af920d436.jpg)


- small twitter thread that presents how to use Quad intrinsics and IsHelperLane to visulize how efficent quad shading is

![](../../assets/be26bfab566439ce.png)


Join nDreams, a world-leading VR game developer and publisher, as a Principal Graphics Programmer and be at the forefront of VR gaming innovation.

As part of our team, you will research, implement, and support new rendering features and shaders, collaborate with technical and creative staff, and optimize code and systems for optimal performance. We offer a state-of-the-art collaborative workflow, flexible hours, and a range of exciting benefits.

Apply now to join our team and shape the future of VR gaming!


- the quick video presents a method to render an outline of an object by taking advantage of wireframe rendering mode
- relies on rendering backfaces only and drawing lines that are thicker than 1 pixel
- presents how to implement the technique using OpenGL

![](../../assets/7707966929802e2b.png)


- the article explains how most tecture encoding formats operate in blocks, presenting how this reduces time complexity
- Additional computational complexity of encoding textures depends on the search space of possible endpoint/mode combinations, which can be reduced using heuristics and pruning techniques

![](../../assets/a2b5ae27541800cd.png)


- Santa Monica Studio release the slides for all GDC 2023 presentations
- covers not only rendering topics but also AI, Animation, Testing, Art, accessbility and visual scripting

![](../../assets/5d11b9e2334adb1a.png)


- the article presents an in-depth look at SDF font rendering techniques
- shows issues with common implementations and show how to correctly render on a sub-pixel level
- discusses how to blend more complex shapes such as Emoji
- additionally presents how the glyps are cached into runtime dynamic texture atlas

![](/img/posts/graphics-programming-weekly-297/sdf_outlines.png)


Join nDreams Studio Orbital as a Graphics Programmer and be at the forefront of developing groundbreaking VR experiences that will captivate players for years to come.

As part of our remote team, you will collaborate with a diverse and innovative group, taking ownership of visual fidelity and rendering performance in Unreal Engine 5.

If you are passionate about pushing the boundaries of VR gaming technology and want to make your mark on the industry, apply now and be part of our exciting journey to redefine the future of VR!


- the blog post provides a first high level overview of the micro-mesh technique
- contains links to nvidia sources that discuss the technique in more detail

![](/img/posts/graphics-programming-weekly-297/micro_mesh_displace.png)


- the article presents what ReBAR is and how it allows GPU resource to be directly CPU adressable
- shows recommendations when and how to use the technique
- addiotinally discusses hardware constraints, and how to validate the availbility

![](../../assets/ec159780a55261cc.png)


- the presentation present a neural network approach used to upscale textures
- shows an overview of BC7 block compression, explaining different modes available and tradeoffs
- discusses the implementation of the network, preseting performance and quality

![](../../assets/b46885be9fbe1f29.png)


- the video tutorial presents how one can use clip planes to cut geomeetry along plane equations
- presents the underlything math as well as how to implement the feature using OpenGL

![](../../assets/98865a3bacdefe50.png)

Thanks to [Hasen Judy](https://hasen.substack.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.