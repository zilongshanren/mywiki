---
title: Moment-Based Order-Independent Transparency
url: http://momentsingraphics.de/I3D2018.html
published: '2018-05-15'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Moment-Based Order-Independent Transparency

Cedrick Münstermann, Stefan Krumpen, Reinhard Klein, Christoph Peters.

2018–07 in *Proceedings of the ACM on Computer Graphics and Interactive Techniques (Proc. i3D)* 1, 1.

[Official version](https://doi.org/10.1145/3203206)

## Abstract

Compositing transparent surfaces rendered in an arbitrary order requires techniques for order-independent transparency. Each surface color needs to be multiplied by the appropriate transmittance to the eye to incorporate occlusion. Building upon moment shadow mapping, we present a moment-based method for compact storage and fast reconstruction of this depth-dependent function per pixel. We work with the logarithm of the transmittance such that the function may be accumulated additively rather than multiplicatively. Then an additive rendering pass for all transparent surfaces yields moments. Moment-based reconstruction algorithms provide approximations to the original function, which are used for compositing in a second additive pass. We utilize existing algorithms with four or six power moments and develop new algorithms using eight power moments or up to four trigonometric moments. The resulting techniques are completely order-independent, work well for participating media as well as transparent surfaces and come in many variants providing different tradeoffs. We also utilize the same approach for the closely related problem of computing shadows for transparent surfaces.

**Keywords:** moment shadow mapping, moment-based, order-independent transparency, partial coverage, power moments, real-time rendering, shadows, transparent shadow casters, trigonometric moments

## Images

![TeaserMBOIT6HP](../../assets/0992d4514f23e816.png)


![TeaserMBOIT6HP](../../assets/0992d4514f23e816.png)

![TeaserTMBOIT3SP](../../assets/44b1e7dad79411c6.png)


![TeaserTMBOIT3SP](../../assets/44b1e7dad79411c6.png)

![TeapotsMBOIT4HP](../../assets/fbfe466899a396c0.png)


![TeapotsMBOIT4HP](../../assets/fbfe466899a396c0.png)

![CloudShadowsMBOIT6](../../assets/1e0eb1f8288029ba.png)


![CloudShadowsMBOIT6](../../assets/1e0eb1f8288029ba.png)

## Video

## Notes

This work will be presented at the ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games 2018 on 15th of May 2018. The author's version has been published on 4th of May 2018.