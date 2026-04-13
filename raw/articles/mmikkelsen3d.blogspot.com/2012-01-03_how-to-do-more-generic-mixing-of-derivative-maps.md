---
title: How to do more generic mixing of derivative maps?
url: http://mmikkelsen3d.blogspot.com/2012/01/how-to-do-more-generic-derivative-map.html
author: Morten S Mikkelsen
published: '2012-01-03'
source_blog: Mikkelsen and 3D Graphics
source_site: http://mmikkelsen3d.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Since I wrote this post I've written a new technical paper called "Surface Gradient Based Bump Mapping Framework" which does a better and more complete job describing the following.**

**All my papers can be found at**

[https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html](https://mmikkelsen3d.blogspot.com/p/3d-graphics-papers.html)I have added a shader to the demo which shows how to do mixing of derivative maps in a more typical scenario in which auto bump scale is used and all derivative maps are using same base unwrap but using different scales and offsets on the texture coordinate. The auto bump scale is what allows us to achieve scale invariance like we are used to with normal mapping.

The location of the demo is still the same:

[source](https://www.dropbox.com/s/pfgin7kvcsjkhin/bumpdemo_src.zip?dl=0)and

[binary](https://www.dropbox.com/s/dfthauvthg2deca/bumpdemo_bin.zip?dl=0). Also notice that dHdst_derivmap() can be made shorter by passing

*VirtDim / sqrt(abs(VirtDim.x * VirtDim.y))*as a constant

*.*Furthermore, this vector constant is ±1.0 when

*VirtDim.x ==*

*VirtDim.y*. Finally, the scale and offset which is applied to the texture coordinate can be moved to the vertex shader. However, this requires the use of multiple interpolators so this might not be the preferred way.

One relevant thing to notice here is that the numerator

*VirtDim*is a float2 and not part of the bump scale. It serves to convert the height derivatives to the normalized texture domain from which we apply the chain rule. The factor

*1 / sqrt(abs(VirtDim.x * VirtDim.y))*on the other hand

**is part of the bump scale**. The distinction is subtle when doing bump mapping but becomes relevant when we do

[parallax mapping](http://mmikkelsen3d.blogspot.com/2012/02/parallaxpoc-mapping-and-no-tangent.html).

If for instance you are using derivative maps made with xNormal or you are just using this way of

[auto calculating a bump scale](http://mmikkelsen3d.blogspot.com/2011/11/derivative-maps-in-xnormal.html)then the expression for the bump scale is:

*bump_scale = g_fMeshSpecificAutoBumpScale / sqrt(abs(VirtDim.x * VirtDim.y))*

where g_fMeshSpecificAutoBumpScale is the square root of the average ratio of the surface to normalized texture area. There is code which shows how to calculate this in the demo. The final value bump_scale is the same as the value which is returned by

[SuggestInitialScaleBumpDerivative() in xNormal](http://mmikkelsen3d.blogspot.com/2011/11/derivative-maps-in-xnormal.html).

## No comments:

## Post a Comment