---
title: Dirt Roads
url: https://outerra.blogspot.com/2010/06/dirt-roads.html
author: Outerra
published: '2010-06-09'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In the previous post about


Dirt roads are using the very same mechanism as normal roads, in fact the only difference is that road nodes here contain a different road type identifier. That is used to look up the corresponding road profile in shaders that generate the roads, and it determines other things as well - the pavement and border materials, for example.


Road profile specifies "exactness" values across the road width, in range from 0 to 1. Normal roads have value 1 across the whole road width, meaning that the elevation given by the road spline interpolation is exact and the resulting surface will be smooth and level. Values less than 1 will cause that the computed surface elevation is blended with the actual underlying terrain elevation with given blending coefficient. Additionally, the less exact the road surface elevation is, the more it is randomized by fractal to make it rougher.



The roughness created by the fractal noise can vary with the road type. The depth of the furrows can be determined by setting road surface under the terrain by a specific amount, and it can change node by node. On the sample road above it creates deeper or shallower parts. Or even a ridge when the way points are not set densely enough to follow the terrain accurately.


Here is a road that was created from way points lying 0.4m (on average) below the terrain surface with high roughness:




Another one that was put only slightly under the terrain and the roughness is low:



Lastly, few screen shots how it all looks in the terrain.



In order to utilize the generated detail we also set a finer level to be used for vehicle physics. In the previous



Forum topic

[roads](http://outerra.blogspot.com/2010/05/integrating-vector-data-roads.html)in Outerra I mentioned that different road types can be created by using road profiles. Here comes one example.Dirt roads are using the very same mechanism as normal roads, in fact the only difference is that road nodes here contain a different road type identifier. That is used to look up the corresponding road profile in shaders that generate the roads, and it determines other things as well - the pavement and border materials, for example.

Road profile specifies "exactness" values across the road width, in range from 0 to 1. Normal roads have value 1 across the whole road width, meaning that the elevation given by the road spline interpolation is exact and the resulting surface will be smooth and level. Values less than 1 will cause that the computed surface elevation is blended with the actual underlying terrain elevation with given blending coefficient. Additionally, the less exact the road surface elevation is, the more it is randomized by fractal to make it rougher.

The roughness created by the fractal noise can vary with the road type. The depth of the furrows can be determined by setting road surface under the terrain by a specific amount, and it can change node by node. On the sample road above it creates deeper or shallower parts. Or even a ridge when the way points are not set densely enough to follow the terrain accurately.

Here is a road that was created from way points lying 0.4m (on average) below the terrain surface with high roughness:

Another one that was put only slightly under the terrain and the roughness is low:

Lastly, few screen shots how it all looks in the terrain.

In order to utilize the generated detail we also set a finer level to be used for vehicle physics. In the previous

[video with Tatra truck](http://www.youtube.com/watch?v=RNw7_lyxPmA)the resolution for physics was around 1.2m, and it was quite visible. In the following video the resolution for physics is around 0.15m, 8 times better. The wheels are simulated as simple ray casts so it may be occasionally visible. Also, Angrypig toyed with the suspension and I left it in for the video; Tatra truck now sways way too much, but at least it serves to show the response to the terrain shape.Forum topic

## 3 comments:

Very, very cool. Don't know how you get the time and knowledge to do all this.

The whole profile idea for imprinting roads into the terrain is, to use Zaphod Beeblebrox's vernacular, " amazingly amazing".



Time well spent sir.

Is it possible to make really difficult off-road tracks by blending between two profiles? Maybe using LERPs to change one profile into another. That would enable the occasional deep pot hole. Not that this isn't good enough for most applications.

Thanks.

I think that occasional deep holes could be created by adjusting the depth on particular road nodes. I didn't have a UI for the road placing till now, so the road parameters were constant as set initially from the code. But they can change at each node - width, depth, slant, markings. The roughness would change with the depth.

Post a Comment