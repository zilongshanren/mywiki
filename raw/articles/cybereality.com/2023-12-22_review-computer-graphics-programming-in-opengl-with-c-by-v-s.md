---
title: 'Review: Computer Graphics Programming in OpenGL with C++ by V. Scott Gordon'
url: https://cybereality.com/review-computer-graphics-programming-in-opengl-with-c-by-v-scott-gordon/
author: Cybereality
published: '2023-12-22'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/c0c7cb7b15f2f1a5.jpg)

Right here we have a pretty solid intro into OpenGL, from what appears to be the coursework of two university professors and their students. It is by no means “modern” techniques, but I feel like it gets the job done for a thorough first look at the API. Though many say that OpenGL is “dead”, it will likely be maintained for backwards compatibility purposes for a long time. Beyond that, while newer APIs like Vulkan are certainly more powerful, beginners may be overwhelmed by the complexity, so it’s a good idea to learn OpenGL, even if only for educational purposes.

Clocking in at over 500 pages, it’s quite a good length while also covering a variety of topics and not being boring. Inside are a total of 17 chapters, covering everything from the basics, like math, shaders, textures and shadows, to more advanced topics like tessellation, geometry shaders, software ray tracing, and even some stereoscopic 3D and VR treatment at the end. Overall fairly comprehensive for what appears to be an introductory text. While this is definitely not the most in-depth look at each topic, it gives a good overview and also has a few tips and tricks that are useful. You likely won’t find too much about hardcore performance optimization, but there is at least a section on using the Nsight debugger.

Overall I felt the book was worth reading, though it’s definitely geared toward the beginner to intermediate level. You should know how to use C++ first, though the authors wrote a companion book with the same material in Java (if you prefer). I was mostly interested in this since it covers some stereo 3D, and I found the explanations to be clear (for example, how to set up an asymmetric frustum manually) so that was worth the price of admission alone. The coverage of geometry shaders and tessellation was also helpful to me, as a lot of material for GL online is older and doesn’t cover this. That said, there were a few sections that seemed confusing, like the lighting chapter. The authors present the lighting model as “ADS lighting” where it seemed to me to be Blinn-Phong, and I thought the non-standard naming was unnecessary. But otherwise I would say it’s a solid text.