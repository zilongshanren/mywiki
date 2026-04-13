---
title: Graphics Programming weekly - Issue 286 - May 7th 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-286/
author: Jendrik Illner
published: '2023-05-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- AMD released an extensive tutorial on how to use the Render Pipeline Shaders SDK
- broken down into multiple parts, it explains the basics to more advanced concepts
- shows how to render a triangle, express more complex resource dependencies, as well as how to interact between the graph and host application
- additionally shows how to take advantage of multithreading when recording commands

![](../../assets/db9fd79b7d4e3e1f.png)


- the paper proposes a new method for the combination of rough surface NDFs
- The presented techniques aim to accurately simulate multiple scattering from heightfields with height-dependent roughness and material properties
- the solution is based on a layered-Smith microfacet model

![](../../assets/90bf7dbb40d1b9e8.jpg)


- The paper presents a new method to represent materials utilizing learned hierarchical textures combined with neural decoders
- presents how to integrate the technique into real-time applications such as path tracers

![](../../assets/fef29f551dbd2b01.jpg)


- the article presents a history of graphics API and how WebGPU fits into the history
- shows an overview of how WebGPU works
- presents possible implementations for different programming languages and how to get started

![](../../assets/241b1b4ffae450f6.png)


- the guide contains best practices for using Sample Feedback on Nvidia hardware
- shows what is expected to perform well, what is not supported, and possible edge cases to consider

![](../../assets/70e24cf74527e372.jpg)


- the article presents the video functionality that Vulkan exposes
- discusses how to use the API and what pitfalls were encountered
- as the Wicked Engine is open source, code and links to the necessary implementation are provided

![](../../assets/3ceefa6bc8d04674.jpg)


- the article presents an overview of Unit Gradient Fields (UGFs)
- UGFs offer a generalization over SDFs, enabling a more expressive language for implicit modeling
- this is only part one of a planned series on the topic

![](../../assets/fd275b1ede30bd5f.png)


- the article presents an in-depth look at the performance of the latest Cyberpunk 2077 update
- shows how the hardware is utilized and what the bottlenecks are
- additionally shows how RDNA2 and RDN3 workloads compare

![](../../assets/85d6fe127c7a9e92.png)


- the video tutorial about rendering terrain using OpenGL continues by explaining how LODs can be implemented for the terrain system
- covers how to create LODs and make sure the terrain doesn’t have any cracks

![](../../assets/75e7951465a52a8e.png)

Thanks to [Angel Ortiz](https://twitter.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.