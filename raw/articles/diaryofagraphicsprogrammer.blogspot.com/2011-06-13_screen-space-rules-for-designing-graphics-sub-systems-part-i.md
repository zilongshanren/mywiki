---
title: 'Screen-Space: Rules for Designing Graphics Sub-systems (Part I)'
url: http://diaryofagraphicsprogrammer.blogspot.com/2011/06/screen-space-rules-for-designing.html
author: Wolfgang Engel
published: '2011-06-13'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Here are three of them:

1. Screen-Space (Part I - this part)

2. No Look-up Tables (Part II)

3. Even Error Distribution (Part III)

Today we focus on the Screen-Space design rule. It says: "do everything you can in Screen-Space because it is more efficient most of the time". This is easy to say for the wide range of effects that are part of a Post-Processing Pipeline like Depth of Field, Motion Blur, Tone Mapping and color filters, light streaks and others (read more in [Engel07]), as well as anti-aliasing techniques like MLAA that anti-alias the image in screen-space.

With the increased number of arithmetic instructions available and the stagnating growth of memory bandwidth, two new groups of sub-systems can be moved into screen-space.

Accompanying Deferred Lighting systems, more expensive materials like skin and hair can now be applied in screen-space; this way a screen-space material system is possible [Engel], solving some of the bigger challenges to implementing a Deferred Lighting pipeline.

Global Illumination and Shadow filter kernels can be moved into screen-space as well. For example, for a large number of Point or Ellipsoidal Shadow Maps, all the shadow data can be stored in a shadow collector in screen-space and then an expensive filter kernel can be applied to this screen-space texture [Engel2010].

The wide range of abilities available with screen-space filter kernels makes it valuable to look at the challenges while implementing them in general. The common challenges to applying materials or lights and shadows with the help of large-scale filter kernels in screen-space are mostly:

1. Scale filter kernel based on camera distance

2. Add anisotropic "behavior" to the screen-space filter kernel

3. Restricting the filter kernel based on the Z value of the Tap

**Scaling Filter Kernel based on Camera Distance**

Using a screen-space filter kernel for filtering shadows, GI, emulating sub-surface scattering for skin or rendering hair, requires at some point to scale the filter kernel based on the distance from the camera or, better yet, the near plane to the pixel in question. What has worked in the past is:

```
// linear depth read more in [Gilham]
// Q = FarClip / (FarClip – NearClip)
// Depth = value from a hyperbolic depth buffer
float depthLin= (-NearClip * Q) / (Depth - Q);
```

```
// scale based on distance to the viewer
// renderer->setShaderConstant4f("TexelSize", vec4(width, height, 1.0f / width, width / height));
sampleStep.xy = float2(1.0f, TexelSize.w) * sqrt(1.0f / ((depthLin.xx * depthLin.xx) * bias));
```

Scaling only happens based on linearized depth values that are going from 0.0..1.0 between the near and far plane. This considers the camera's near and far plane settings. The bias value is a user defined "magic" value. The last channel in the TexelSize variable holds the x and y direction ratio of the pixel. The inner term - 1.0/distance2- of the equation resembles a simple light attenuation function. We will improve this equation in the near future.

**Anisotropic Screen-Space Filter Kernel**

Following [Geusebroek], anisotropy can be added to a screen-space filter kernel by projecting into a ellipse following the orientation of the geometry.

![](http://altdevblogaday.com/wp-content/uploads/2011/06/ssss_aniso.jpg)


![](http://altdevblogaday.com/wp-content/uploads/2011/06/ssss_aniso.jpg)

*Image 1 - Anisotropic Screen-Space Filter Kernel*

Normals that are stored in a world-space buffer in a G-Buffer can be compared to the view vector. The elliptical "response" is achieved by taking the square root of this operation.

`float Aniso = saturate(sqrt(dot( viewVec, normal )));`

**Restricting the filter kernel based on the Z value of the Tap**

One of the challenges with any screen-space filter kernel is the fact that the wide filter kernel can smear values into the penumbra around "corners" of geometry (read more in [Gumbau].

![](http://altdevblogaday.com/wp-content/uploads/2011/06/Error-1024x575.jpg)


![](http://altdevblogaday.com/wp-content/uploads/2011/06/Error-1024x575.jpg)

*Image 2 - Error introduced by running a large filter kernel in screen-space*

A common way to solve this problem is to compare the depth values of the center of the filter kernel with the depth values of the filter kernel taps and define a certain threshold where we consider the difference between the depth values large enough to early out. A source code snippet for this might look like this.

```
bool isValidSample = bool( abs(sampleDepth - d) < errDepth );
if (isValidSample && isShadow)
{
// the sample is considered valid
sumWeightsOK += weights[i+1]; // accumulate valid weights
Shadow += sampleL0.x * weights[i+1]; // accumulate weighted shadow value
}
```

**Acknowledgements**

I would like to thank Carlos Dominguez for the discussions about how to scale filter kernels based on camera distance.

**References**

[Engel] Wolfgang Engel, "Deferred Lighting / Shadows / Materials", FMX 2011,

[http://www.confettispecialfx.com/confetti-on-fmx-in-stuttgart-ii](http://www.confettispecialfx.com/confetti-on-fmx-in-stuttgart-ii)

[Engel07] Wolfgang Engel, "Post-Processing Pipeline", GDC 2007, http://www.coretechniques.info/index_2007.html

[Engel2010] Wolfgang Engel, "Massive Point Light Soft Shadows",

[http://www.confettispecialfx.com/massive-point-light-soft-shadows](http://www.confettispecialfx.com/massive-point-light-soft-shadows)

[Geusebroek] Jan-Mark Geusebroek, Arnold W. M. Smeulders, J. van de Weijer, “Fast anisotropic Gauss filtering”, IEEE Transactions on Image Processing, Volume 12 (8), page 938-943, 2003

[Gilham] David Gilham, "Real-Time Depth-of-Field Implemented with a Post-Processing only Technique", ShaderX5: Advanced Rendering, Charles River Media / Thomson, pp 163 - 175, ISBN 1-58450-499-4

[Gumbau] Jesus Gumbau, Miguel Chover, and Mateu Sbert, “Screen-Space Soft Shadows”, GPU Pro, pp. 477 - 490

## 2 comments:

Images are missing

Images are missing.

Post a Comment