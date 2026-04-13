---
title: Graphics Programming weekly - Issue 341 - May 26th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-341/
author: Jendrik Illner
published: '2024-05-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper provides a walkthrough explanation of the different components that define a BSDF (bidirectional scattering distribution function) that defines the shading behavior of a materials
- covers the underlying theory, explaining the derivation as well as the geometric interpretations

![](../../assets/f7a1668beed92cb4.png)


- the paper introduces models to solve the reconstruction of irradiance in the vertex-normal space
- applies the developed framework to hemispherical and cone occlusion to volumetric lighting
- as well as mitigating light leakage for normal-mapped surfaces’ appearance of runtime ambient occlusion
- shadertoy implementation is provided

![](../../assets/f53bb4476d65e952.png)


- the series on voxel ray tracer continues by presenting how to accumulate samples over time with a nonstatic camera
- explains temporal pixel reprojection, how to deal with sub-pixel blending, and how to improve results with occurring object occlusions

![](../../assets/7329093a14b2a5e6.jpg)


- the blog post provides a detailed description for programmers interested in graphics programming
- explains what the job entails, different specializations in games, and what topics graphics programmers often work on
- additionally gives insights into the technologies the author recommends to start learning with

![](../../assets/dd0fbe3c28670566.png)


- the article explains an approach to implementing Sun Beams using Billboarding techniques
- implementation is shown using the visual shading language of Unity

![](../../assets/e64c49bde5cb5af6.png)


- the blog post presents that the latest D3D12 SDK update introduces support for R9B9G9E5 for Render Target and UAVs
- explains how the R9B9G9E5 format allows higher precisions compared to half-floats and less memory usage than float formats
- additionally expressed the importance of verifying hardware support

![](../../assets/ea9da1cea1138d0c.png)


- the video shows how to implement a shader effect that allows objects to change their appearance close to existing depth values in the depth buffer
- the presented technique relies on a rendering order that ensures the depth values are written before the objects want to read them
- technique is implemented using the visual shader language of Unity

![](../../assets/7bf049f8ce22f2ea.png)


- the video tutorial continues to discuss the implementation of a Vulkan renderer
- this week’s videos explain how to clear the back buffer to a solid color in every frame
- C++ implementation is shown

![](../../assets/7c6b5d7c12175aa7.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.