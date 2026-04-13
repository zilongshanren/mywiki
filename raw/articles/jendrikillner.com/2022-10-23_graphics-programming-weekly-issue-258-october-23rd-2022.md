---
title: Graphics Programming weekly - Issue 258 - October 23rd, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-258/
author: Jendrik Illner
published: '2022-10-23'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a comparison of a large number of methods for the construction of BVHs for ray tracing workloads
- concludes by making suggestions for future technological developments that appear to offer the most potential at the time of writing

![](../../assets/4ccbde277c86443b.png)


- the 5 part series provides a walkthrough of common issues when using the FSR 2.0 upscaler in Unreal Engine Projects
- discusses why the issues occur, what solutions are available and how FSR 2.1 was improved to deal with the issues

![](../../assets/ede8836a27a3d4fd.png)


- the article presents the story of how the author experimented with binary search in a shader for accelerating SDF tracing workloads
- shows how to implement a stackless GPU-based traversal
- presents why the binary search is unable to outperform the SDF raymarching loop

![](../../assets/73c7cadac20c1807.jpg)

- the slides discussing the new GI solution implemented for Godot
- the talk will happen on Friday, 28th
[twitter DM for signup](https://twitter.com/reduzio/status/1583780332524146692) - discusses how the technique is based on sphere tracing distance fields
- how to generate the distance fields, trace lights
- additionally spends a large chunk of the presentation on optimizations to make the technique viable

![](../../assets/324a87c7b8b4bc35.png)


As a 3D Engineer at Threedy, you develop our core system’s algorithms and data structures, always optimizing data representations for efficient and cutting-edge 3D data streaming and visual computing.

![](../../assets/2365cbc531701a1a.png)


- the blog post announces that a new, more open model for HLSL language development
- discusses what feature will be able to be discussed in public and how the process will work

![](../../assets/17046948469c6ff8.jpg)

- a collection of papers from SIGGRAPH Asia 2022
- the list is updated every couple of days at this time

![](../../assets/8dda6c957802c0a8.png)

- the video shader tutorial series covers how to create a shader that allows procedural rock shading with snow support
- previous tutorials covered how to create the individual pieces, and those are combined in this part
- video shows the implementation in both Unreal and Unity visual shader authoring

![](../../assets/e37a24ddc010f683.png)


- the AMD paper presents the findings for a new dynamic GI solution
- proposes the separation into a screen and world space cache that complement each other with additional information
- provides a detailed description of the individual steps, performance results as well as known limitations

![](../../assets/96c2c0ceb08007f8.png)


- a collection of cheatsheets on the high-level concepts of topics such as AI, machine learning, and statistics

![](../../assets/40b71a994f2a0f07.jpeg)

- the video presents a history of light transport algorithms development
- shows a breakdown of each technique and improvements in each iteration

![](/img/posts/graphics-programming-weekly-258/restir.png)

- the article presents that the Godot engine supports compilation in double-precision mode
- shows how to emulate double precision calculation on GPUs that don’t support double by using two floats
- presents what limitations still exist with this solution

![](../../assets/345a54bc11806da2.png)


- the blog post provides the text version of the mesh shader talk presented
- the presentation covers the issues with the classic graphics pipeline and how mesh shaders can address these
- presents how mesh shaders are authored, limitations, and hardware preference differences

![](../../assets/b7d0832be14c5916.jpg)

Thanks to [Keith O’Conor](https://twitter.com/keithoconor) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.