---
title: Non-linearly Quantized Moment Shadow Maps
url: http://momentsingraphics.de/HPG2017.html
published: '2017-01-01'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Non-linearly Quantized Moment Shadow Maps

Christoph Peters.

2017–07 in *Proceedings of High Performance Graphics*. ACM.

[Official version](https://doi.org/10.1145/3105762.3105775)

## Abstract

Moment shadow maps enable direct filtering to accomplish proper antialiasing of dynamic hard shadows. For each texel, the moment shadow map stores four powers of the depth in either 64 or 128 bits. After filtering, this information enables a heuristic reconstruction. However, the rounding errors introduced at 64 bits per texel necessitate a bias that strengthens light leaking artifacts noticeably. In this paper, we propose a non-linear transform which maps the four moments to four quantities describing the depth distribution more directly. These quantities can then be quantized to a total of 32 or 64 bits. At 64 bits, the results are virtually indistinguishable from moment shadow mapping at 128 bits per texel. Even at 32 bits, there is hardly any additional light leaking but banding artifacts may occur. At the same time, the computational overhead for the reconstruction is reduced. As a prerequisite for the use of these quantization schemes, we propose a compute shader that applies a resolve for a multisampled shadow map and a 9² two-pass Gaussian filter in shared memory. The quantized moments are written back to device memory only once at the very end. This approach makes our technique roughly as fast as variance shadow mapping with 32 bits per texel. Since hardware-accelerated bilinear filtering is incompatible with non-linear quantization, we employ blue noise dithering as inexpensive alternative to manual bilinear filtering.

**Keywords:** moment shadow mapping, non-linear quantization, 32-bit quantization, on-chip filtering, compute shader, fast Gaussian blur, shadows, real-time rendering

## Images

![1_Teaser](../../assets/8388e3611b0afb10.png)


![1_Teaser](../../assets/8388e3611b0afb10.png)

![2_RepresentativeImage](../../assets/8d77854cda417380.jpg)


![2_RepresentativeImage](../../assets/8d77854cda417380.jpg)

![3_FourthMomentOffset](../../assets/a0df41d1ad3ca8c6.png)


![3_FourthMomentOffset](../../assets/a0df41d1ad3ca8c6.png)

![4_Dithering](../../assets/9f7f7a6d7da34e05.png)


![4_Dithering](../../assets/9f7f7a6d7da34e05.png)

## Animation of compute shader

Here is an animated version of Figure 6 in the paper visualizing shared memory access patterns of the compute shader.