---
title: 'Beyond Hard Shadows: Moment Shadow Maps for Single Scattering, Soft Shadows
  and Translucent Occluders'
url: http://momentsingraphics.de/I3D2016.html
published: '2016-01-01'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Beyond Hard Shadows: Moment Shadow Maps for Single Scattering, Soft Shadows and Translucent Occluders

Christoph Peters, Cedrick Munstermann, Nico Wetzstein, Reinhard Klein.

2016–02 in *Proceedings of the 20th ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games*. ACM.

[Official version](https://doi.org/10.1145/2856400.2856402)

## Abstract

Building upon previous works, we transfer the recently proposed moment shadow mapping to three new applications. Like variance shadow maps and convolution shadow maps, moment shadow maps can be filtered directly. Classically, this is used to filter hard shadows but previous works explore other applications. Prefiltered single scattering uses convolution shadow maps to render single scattering in homogenous participating media, variance soft shadow mapping uses variance shadow maps for approximate soft shadows and Fourier opacity mapping uses convolution shadow maps for translucent occluders. We combine these three techniques with moment shadow mapping to arrive at better heuristics with less computational overhead.

**Keywords:** filterable shadow maps, moment shadow mapping, participating media, real-time rendering, single scattering, soft shadows, translucent occluders

## Images

![SingleScattering](../../assets/36ea9688b3a5e443.jpg)


![SingleScattering](../../assets/36ea9688b3a5e443.jpg)

![FoliageMSM6](../../assets/4026678439112cc5.jpg)


![FoliageMSM6](../../assets/4026678439112cc5.jpg)

![QuadbotMSSM](../../assets/c6d583913c0b6bf1.jpg)


![QuadbotMSSM](../../assets/c6d583913c0b6bf1.jpg)

![SeaportMSSM](../../assets/0693347bf654bb0e.jpg)


![SeaportMSSM](../../assets/0693347bf654bb0e.jpg)

![SintelMSSM](../../assets/e22534fc369259e4.jpg)


![SintelMSSM](../../assets/e22534fc369259e4.jpg)

![TranslucentOccluder4MSM](../../assets/17f5f2e718ae78f7.jpg)


![TranslucentOccluder4MSM](../../assets/17f5f2e718ae78f7.jpg)

## Video

## Executable Demo

We provide an executable demo showcasing all novel techniques presented in the paper and some related work. For example, exponential variance shadow maps with 16-bit quantization are now supported. Please refer to the ReadMe.pdf that comes with the download for more information. Shader code with documentation is provided in a separate download.

## Notes

An extended version of this paper has been invited to the [Journal of Computer Graphics Techniques](http://jcgt.org/).