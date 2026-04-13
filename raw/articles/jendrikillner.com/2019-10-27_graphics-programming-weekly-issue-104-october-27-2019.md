---
title: Graphics Programming weekly - Issue 104 — October 27, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-104/
author: Jendrik Illner
published: '2019-10-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents the different meaning of the term gamma in different color contexts
- suggest to always use a piece-wise sRGB function

![](../../assets/46b612f7375e9097.png)


- presents an overview of the difference between static and dynamic branching
- dynamic is a lot more expensive of PowerVR hardware
- shows examples of problematic cases with dynamic branching
- presents an extension that can be used to make the dynamic branch a lot more performant if all threads agree on a condition

![](../../assets/48f926170558b9c0.png)


- introduction of marching cube pre-pass stage reduces the mesh shader example GPU time by 33% to 50%

![](../../assets/463adcb9ee63a525.jpg)



- the author presents his solution on how to implement painting onto textures using unity
- intersects mouse position with meshes, converting into UV space to be able to apply painting information using signed distance fields

![](../../assets/e8fa3e64c17ccf49.png)


- the article presents the D3D12 resource state promotion and decay rules related to the common resource state
- mentions the AssertResourceState debug API that can be used to validate resource state promotion/decay behavior
- explains the ExecuteCommandLists behavior concerning resource states

![](../../assets/3b06fd27f121a9b2.jpg)


- the article presents how the author took the CPU implementation of Ray Tracing in a Weekend and converted it to run on the GPU using a GLSL implementation

![](../../assets/52ba051049036967.png)


- a brief presentation by Embark Studios showing RLSL, a subset of rust compiled to SPIR-V
- experimental stage
- showing how/what it is currently implemented, vision for the future
- presents examples of how shaders are implemented
- integration into the rust ecosystem

![](../../assets/4a15ff685e5e4e7f.png)

Thanks to [Steven Cannavan](https://twitter.com/pedanticcoder) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.