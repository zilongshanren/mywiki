---
title: Graphics Programming weekly - Issue 333 - March 31st, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-333/
author: Jendrik Illner
published: '2024-03-31'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the GDC presentation provides an overview of the profiler tools available from AMD
- presents the updated shader analysis tool, including a preview of the single shader stage mode
- additionally presents an overview of the raytracing and memory debugging tool improvements

![](../../assets/ac0718481c640504.png)


- the article presents a walkthrough of how to implement a post-processing effect that emulates Jean Giraud’s art style
- shows how the author approached object outlines, shadows, and lighting patterns
- provides interactive WebGL implementations that showcase the individual stages of the implementation

![](../../assets/9140d77c747ab334.png)


- the blog post announces that the Windows PIX runtime has been released as OpenSource
- this includes logic to decode PIX events as well as the runtime logic that writes ETW entries
- additionally, the team is looking for feedback for a proposed task API for PIX

![](../../assets/1a156083d0dffde9.png)


- the article introduces an alternative low discrepancy sampling strategy for circles
- provides a quick introduction to rejection sampling
- shows how adaption could be used to sample only within a quad within the disk and still fill the whole circle with samples
- compares the characteristics of the technique and presents the applications to different shapes

![](../../assets/11e33c1f3b4d5abc.png)


- the blog post describes how to use the CUDA Compute Sanitizer to implement a resize-aware memory pool
- additionally discusses the APIs available to allow memory debugging more insightful

![](../../assets/4b378e7b2f898061.png)


- the GDC presentation discusses how the GPU Reshape tool enables GPU timeline validation
- explains how the validation logic can be written in an API-agnostic manner
- provides a look at future developments where the same infrastructure could be used for profiling or data debugging

![](../../assets/d517ace5343a6e2f.png)


- the article provides an introduction to ray marching
- explains the underlying concept and how it compares to ray-tracing
- extends the concepts to introduce the various operations (scaling, translations, boolean operations) required to express geometry
- combines the knowledge to build a fractal object called the Menger Sponge

![](../../assets/97f5e3ecfae4bd7f.png)

Thanks to Jhon Adams for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.