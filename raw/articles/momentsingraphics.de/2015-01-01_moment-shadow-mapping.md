---
title: Moment Shadow Mapping
url: http://momentsingraphics.de/I3D2015.html
published: '2015-01-01'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Moment Shadow Mapping

Christoph Peters, Reinhard Klein.

2015–02 in *Proceedings of the 19th ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games*. ACM.

[Official version](https://doi.org/10.1145/2699276.2699277)

## Abstract

We present moment shadow mapping, a novel technique for fast, filtered hard shadows. Like variance shadow mapping it allows for the application of all kinds of efficient texture filtering and antialiasing to its moment shadow map. However it is designed to provide a substantially higher quality. Moment shadow maps store four moments of the depth within the filter kernel. Using this information, our efficient algorithm computes the sharpest possible lower bound as approximation to the shadow intensity. The choice to compute such a bound using four moments is based upon an automated evaluation of thousands of alternatives and thus known to be optimal. To reduce memory and bandwidth requirements we present an optimized quantization scheme to allow 16-bit quantization of moment shadow maps. Our evaluation demonstrates that moment shadow mapping produces high quality results with a single shadow map sample per fragment using 64 bits per shadow map texel.

**Keywords:** automated evaluation, filtered hard shadows, moment problem, shadow mapping, variance shadow mapping

## Images

![1_Teaser](../../assets/15d146d04ccaa14d.jpg)


![1_Teaser](../../assets/15d146d04ccaa14d.jpg)

![2_SeaportCity](../../assets/e9d06cb03b1d88bb.jpg)


![2_SeaportCity](../../assets/e9d06cb03b1d88bb.jpg)

![3_SeaportSquare](../../assets/cebea552230f66eb.jpg)


![3_SeaportSquare](../../assets/cebea552230f66eb.jpg)

![4_VSM](../../assets/7cefcdb78f64ec42.jpg)


![4_VSM](../../assets/7cefcdb78f64ec42.jpg)

![5_4MSM](../../assets/7f3755a5a0b72874.jpg)


![5_4MSM](../../assets/7f3755a5a0b72874.jpg)

![6_MomentHull](../../assets/e6ff7c5ec1630aad.jpg)


![6_MomentHull](../../assets/e6ff7c5ec1630aad.jpg)

## Video

## Errata

Two typos found their way into the official version:

- Page 5, first sentence of Section 4.1: It is stated that the upcoming algorithm solves Problem 1 for \(I=[0,1]\) but it should be \(I=\mathbb{R}\).
- Page 6, second line of continuous text: The paper states that \(1-w_3\) has to be returned, but it should be \(1-w_1\).

For your convenience these mistakes are corrected in the author's version available here.