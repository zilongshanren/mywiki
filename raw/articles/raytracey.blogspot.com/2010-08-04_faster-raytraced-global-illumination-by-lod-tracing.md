---
title: Faster raytraced global illumination by LOD tracing
url: http://raytracey.blogspot.com/2010/08/faster-raytraced-global-illumination-by.html
author: Sam Lapere
published: '2010-08-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://bps10.idav.ucdavis.edu/talks/13-fascionePantaleoni_PantaRay_BPS_SIGGRAPH2010.pdf](http://bps10.idav.ucdavis.edu/talks/13-fascionePantaleoni_PantaRay_BPS_SIGGRAPH2010.pdf)

The idea is simple and elegant: use the full res geometry for tracing primary rays and use lower LOD geometry for tracing secondary rays. The amount of triangles to test intersection with is significantly reduced, which speeds up the GI computation considerably.

These papers use the same principle:

"R-LODs: Fast LOD based raytracing for massive models" by Yoon

"Two-Level Ray Tracing with Reordering for Highly Complex Scenes" by Hanika, Keller and Lensch

The idea is similar to Lightcuts and point based color bleeding (which both use a hierarchy to cluster sets of lights or points to reduce the computational cost of tracing) but is used for geometry instead of lights. It is also being used by Dreamworks:

![](../../assets/1a57aa43b512dbbd.jpg)


![](../../assets/1a57aa43b512dbbd.jpg)

Picture from

[Siggraph presentation by Tabellion (PDI Dreamworks)](http://www.graphics.cornell.edu/%7Ejaroslav/gicourse2010/giai2010-04-eric_tabellion-slides.pdf)

From

[http://www.graphics.cornell.edu/~jaroslav/gicourse2010/giai2010-04-eric_tabellion-notes.pdf](http://www.graphics.cornell.edu/%7Ejaroslav/gicourse2010/giai2010-04-eric_tabellion-notes.pdf):

We describe here one of the main ways in which we deal with geometric complexity. When rays are cast, we do not attempt to intersect the geometry that is finely tessellated down to pixel-size micropolygons - this would be very expensive and use a lot of memory. Instead we tessellate geometry using a coarser simplified resolution and the raytracing engine only needs to deal with a much smaller set of polygons. This greatly increases the complexity of the scenes that can be rendered with a given memory footprint, and also helps increase ray-tracing efficiency. To avoid artifacts due to the offset between the two geometries, we use a “smart bias” algorithm described in the next slides.

Since rays originate from positions on the micropolygon tessellation of the surface and can potentially intersect a coarser tessellation of the same surface, self intersection problems can happen.

The image above illustrates cross-section examples of a surface tessellated both into micropolygons and into a coarse set of polygons. It also shows a few rays that originate from a micropolygon whith directions distributed over the hemisphere. To prevent self intersection problems to happen, we use a ray origin offsetting algorithm. In this algorithm, we adjust the ray origin to the closest intersection before / after the ray origin along the direction of the ray, within a user-specified distance. The ray intersection returned as a result of the ray intersection query is the first intersection that follows the adjusted ray origin. The full algorithm is described in [Tabellion and Lamorlette 2004].

Here is a comparison between a reference image that was rendered while raytracing the micropolygons micropolygons. The image in the center was rendered with our technique while raytracing the coarser polygon tessellation illustrated in the image on the right.

It has been shown in [Christensen 2003] that it is possible to use even coarser and coarser tessellations of the geometry to intersect rays with larger ray footprints. This approach is also based on using only coarser tessellation and is not able to provide very coarse tessellations with much fewer polygons than there are primitives (fur, foliage, many small overlapping surfaces, etc.), which would be ideal for large ray footprints. This problem is one of the main limitations of ray-tracing based GI in very complex scenes and is addressed by the clustering approach used in point-based GI, as discussed in later slides.

With this technique, you could have a 1 million polygon scene to trace primary rays, while secondary rays are traced against a 100K or a 50K polygon LOD version of the scene. When using voxels, this becomes a walk in the park, since LOD is automatically generated (see

[http://voxelium.wordpress.com/2010/07/25/shadows-and-global-illumination/](http://voxelium.wordpress.com/2010/07/25/shadows-and-global-illumination/)for an awesome example)

## No comments:

Post a Comment