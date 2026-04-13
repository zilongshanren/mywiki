---
title: Solving Trigonometric Moment Problems for Fast Transient Imaging
url: http://momentsingraphics.de/SiggraphAsia2015.html
published: '2015-01-01'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Solving Trigonometric Moment Problems for Fast Transient Imaging

Christoph Peters, Jonathan Klein, Matthias B. Hullin, Reinhard Klein.

2015–10 in *ACM Transactions on Graphics (Proc. SIGGRAPH Asia)* 34, 6.

[Official version](https://doi.org/10.1145/2816795.2818103)

## Abstract

Transient images help to analyze light transport in scenes. Besides two spatial dimensions, they are resolved in time of flight. Cost-efficient approaches for their capture use amplitude modulated continuous wave lidar systems but typically take more than a minute of capture time. We propose new techniques for measurement and reconstruction of transient images, which drastically reduce this capture time. To this end, we pose the problem of reconstruction as a trigonometric moment problem. A vast body of mathematical literature provides powerful solutions to such problems. In particular, the maximum entropy spectral estimate and the Pisarenko estimate provide two closed-form solutions for reconstruction using continuous densities or sparse distributions, respectively. Both methods can separate m distinct returns using measurements at m modulation frequencies. For m=3 our experiments with measured data confirm this. Our GPU-accelerated implementation can reconstruct more than 100000 frames of a transient image per second. Additionally, we propose modifications of the capture routine to achieve the required sinusoidal modulation without increasing the capture time. This allows us to capture up to 18.6 transient images per second, leading to transient video. An important byproduct is a method for removal of multipath interference in range imaging.

**Keywords:** AMCW lidar systems, transient imaging, range imaging, closed-form solution, trigonometric moment problem

## Images

![0Teaser](../../assets/d785613ae9d83796.png)


![0Teaser](../../assets/d785613ae9d83796.png)

![1NumberedMirrorsFullHD](../../assets/5a699e41c342ecfe.png)


![1NumberedMirrorsFullHD](../../assets/5a699e41c342ecfe.png)

![2Hardware](../../assets/c241ae3f323f204c.jpg)


![2Hardware](../../assets/c241ae3f323f204c.jpg)

![3NumberedMirrors](../../assets/3de821d0e639a280.png)


![3NumberedMirrors](../../assets/3de821d0e639a280.png)

![6TransientVideoFrames](../../assets/bad03f3b613c47c8.png)


![6TransientVideoFrames](../../assets/bad03f3b613c47c8.png)

![5PointCloudsCorner](../../assets/25dfeb2c239b989d.png)


![5PointCloudsCorner](../../assets/25dfeb2c239b989d.png)

![4StreakImage](../../assets/4179c629ef9508e0.png)


![4StreakImage](../../assets/4179c629ef9508e0.png)