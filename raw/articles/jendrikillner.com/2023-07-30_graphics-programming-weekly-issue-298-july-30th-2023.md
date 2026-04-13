---
title: Graphics Programming weekly - Issue 298 - July 30th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-298/
author: Jendrik Illner
published: '2023-07-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a method that uses any hit shaders to implement order-independent transparency
- compares the performance and quality against the closest-hit shader method of the last post

![](../../assets/9aa17abdc9102711.png)


- AMD announced the release of a Vulkan extension to support the experimental D3D12 Work Graph concept
- The extension is called VK_AMDX_shader_enqueue and presents the API, reasons as well as open issues
- sample application is provided

![](../../assets/d4869b312e286dd2.jpg)


Rocksteady is an award-winning developer based in London, focused on combining character-driven cinematic narrative with genre-defining gameplay to create unforgettable experiences based on legendary IP. Growing our studio in London, our multicultural team takes inspiration from the culture and history of our home in one of the most diverse cities in the world.

We’re currently looking for an technical leader in rendering, to join our experienced team of game developers as we launch the highly anticipated project Suicide Squad: Kill the Justice League, and build exciting future plans.

![](../../assets/56e95fdd667ed0ee.png)


- the blog post announces that the book Real-Time Rendering is now also available in Korean

![](../../assets/4dea58a8f58e9d60.jpg)


- the article discusses different methods that are available to convert from f32 to u32 data formats losslessly
- presents use cases and what to consider when choosing between the methods

![](../../assets/5dd053a30e859f38.png)


- the article presents an overview of dithering techniques
- shows how the type of noise influences the effect
- includes a shadertoy implementation of the presented techniques

![](../../assets/0223734c68b778e6.jpeg)


Join nDreams Studio Orbital as a Graphics Programmer and be at the forefront of developing groundbreaking VR experiences that will captivate players for years to come.

As part of our remote team, you will collaborate with a diverse and innovative group, taking ownership of visual fidelity and rendering performance in Unreal Engine 5.

If you are passionate about pushing the boundaries of VR gaming technology and want to make your mark on the industry, apply now and be part of our exciting journey to redefine the future of VR!


- the article presents an introduction to the fourth dimension and explains how to imagine mathematically and geometrically accurate 3D objects
- shows the mathematical foundation
- the series aims at giving the reader the knowledge to simulate how 4D objects would behave in a 3D world

![](../../assets/69a463360e70b72c.png)


- the article provides a comprehensive overview of game color management and encoding complexities
- introduces the separation between color and radiometric units
- additionally also touches on the subjectivity of converting rendered data to displayable via “tone-mapping” operations

![](../../assets/33ab1a3c100ba344.png)


- the article presents how to render geometry to the six faces of a cubemap from a single draw call
- explains how to use the VK_EXT_shader_viewport_index_layer extension
- shows how to use the extension, what kind of hardware support can support the feature
- additionally shows a high-level performance comparison between the classical approach and the usage of the extension

![](../../assets/6a405a6626dbfab5.jpg)


Join nDreams, a world-leading VR game developer and publisher, as a Principal Graphics Programmer and be at the forefront of VR gaming innovation.

As part of our team, you will research, implement, and support new rendering features and shaders, collaborate with technical and creative staff, and optimize code and systems for optimal performance. We offer a state-of-the-art collaborative workflow, flexible hours, and a range of exciting benefits.

Apply now to join our team and shape the future of VR gaming!


- the blog post shows the talks Roblox will be presenting at SIGGRAPH
- covers Surface Simplification, Differentiable Heightfield Path Tracing, hair simulation, and much more

![](../../assets/f9dfdbd3ce43dc13.png)


- the GDC presentation covers geometrical limitations and techniques that can be used to solve the bottlenecks
- shows how Simplygon can be used to simplify models for improved rendering performance
- discusses a large number of issues that will be encountered when simplifying common workflows and how to solve the issues

![](../../assets/64cc6d483360c3d8.png)

Thanks to [Hasen Judy](https://hasen.substack.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.