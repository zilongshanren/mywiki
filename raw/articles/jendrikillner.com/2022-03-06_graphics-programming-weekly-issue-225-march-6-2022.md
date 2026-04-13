---
title: Graphics Programming weekly - Issue 225 - March 6, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-225/
author: Jendrik Illner
published: '2022-03-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an explanation of common tone mapping issues, comparing multiple local tone mapping solutions
- discusses the Exposure fusion technique in detail
- the technique combines multiple exposed images with varying radii based on the frequency changes in the image
- present a WebGL demo implementation of the technique

![](../../assets/09a9680f1998cb01.png)


- the presentation talks about techniques to use VRS (Variable Rate Shading) to reduce the cost of lighting calculations for deferred shading
- presents implementation details for PC/Series X and presents performance comparisons of the techniques
- additionally introduces a technique to reduce block artifacts

![](../../assets/ed349f19848b343b.jpg)


- the presentations cover the experience of implementing VRS into Doom Eternal and Gears5
- contains lessons learned, performance expectations as well as implementation details
- additionally covers how VRS performance with UE5 Nanite pipelines

![](../../assets/ad3e3ab909b49d1b.jpg)


- the article discusses the effect that human perception and images appear different
- presents shortcomings of linear perspective
- shows how different types of focal lengths and perspectives create different effects

![](../../assets/d2bf742eb8ba6a21.jpg)


- the article presents a collection of code samples that allow the selection of random samples from a list of items
- shows different cases from known/unknown sizes, weight vs. unweighted sampling
- additionally presents how to combine multiple lists into a coherent sampling strategy

![](../../assets/78d51d22d697c5de.png)


- the paper presents a method for improving the quality of motion blur on dynamic triangulated objects
- it approximates the nonlinear depth, normal, and UV functions
- the adaptive solution is based on prism volume and will adapt based on the motion and features

![](../../assets/1fc0a55eb988e357.png)


- the article presents Vulkan for Safety-Critical applications
- presents how Vulkan SC 1.0 differes from Vulkan 1.2
- main differences are pipeline lading and more rigid memory allocation requirements
- all pipelines need to be compiled ahead of time into caches. No runtime compilation is allowed
- provides tools to inspect the compiler cache outputs

![](../../assets/7a5f3ee015e23d55.jpg)


- the video panel discussion presents a look at the VFX development for Dune
- discussions about the processes, improvements and the effects of the sand screen compared against classical blue screen techniques

![](../../assets/70f4beaa68d6895b.png)


- the article presents a method to uniformly sample floats in the [0, 1) range
- shows how floating-point precision can introduce biasing from integer division
- shows alternative ways that improve the uniformity

![](../../assets/4e575d3b1748b649.png)


- the video tutorial explains the concepts required for shadow mapping
- explains the foundational concepts, discussing transformations
- presents how to implement shadow mapping using OpenGL

![](../../assets/0779241a8b1c2a96.png)

Thanks to [Unai Landa](https://twitter.com/unai_landa) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.