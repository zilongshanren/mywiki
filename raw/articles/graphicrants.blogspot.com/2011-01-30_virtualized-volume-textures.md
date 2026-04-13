---
title: Virtualized volume textures
url: http://graphicrants.blogspot.com/2011/01/virtualized-volume-textures.html
author: Brian Karis
published: '2011-01-30'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Irradiance volumes using volume textures is a technique that has been getting some use lately. Check out the following for some places I've noticed it.

[Split/Second](http://www.bungie.net/images/Inside/publications/siggraph/BlackRockStudio/Siggraph2009_BlackRock.pptx)

[Cryengine 3](http://www.crytek.com/cryengine/cryengine3/presentations/cascaded-light-propagation-volumes-for-real-time-indirect-illumination)(Cascaded Light Propagation Volumes)

[FEAR 2](http://www.microsoft.com/downloads/en/details.aspx?familyid=d68a47f9-ae4d-464c-9b40-9550c0aea3ec&displaylang=en)

[Rust](http://copypastepixel.blogspot.com/2010/09/light-volumes-sponza-attrium.html)

Probably the biggest downside to volumes vs more traditional lightmaps is the resolution. Volume textures take up quite a bit of memory so they need to be fairly low resolution. Unfortunately much of this data is covering empty space. It's convenient for empty space to have some data coverage so that the same solution can be used for dynamic objects but the same resolution is certainly not needed. How would you store a different resolution of volume data on world geometry than in empty space?

The most straight forward solution to me is an indirection texture. Interestingly what this turns into is virtualizing the volume texture just like you would a 2d texture. That indirection volume texture acts like the page table to your physical texture. Each page table texel translates the XYZ coordinates into a page or brick in the physical volume texture and subsequently the UVW coordinates in the physical volume texture. If you need a refresher on virtual texturing check out

[Sean Barrett's](http://www.silverspaceship.com/src/svt/)and

[id's](http://mrelusive.com/publications/presentations/2010_gtc/GTC_2010_Virtual_Textures.pdf)presentations on the topic. All the same limitations apply in 3d as they do in 2d. Pages will need borders to have proper filtering. The smaller the page size the more waste due to borders and the larger the page table gets.

Another way of thinking of this is as a sparse voxel octree. Instead of the page table being managed like a quadtree it would work like an octree. Typically this data structure is thought of only for ray casting but there's nothing inherent about it that requires that. SVO's have also only been stored as trees, requiring traversal to get to the leaves. So long as you have bricks and aren't working with the granularity of individual voxels the traversal can be changed into a single texture look up just like the quadtree traversal in a 2d virtual texture.

Thinking about it as a SVO is helpful because volume data usually has more sparseness than 2d textures. In this case we don't really care about bricks where there is no geometry. If you use a screen read back to determine which pages to load this will happen automatically. Better yet you don't need to even store this data on disk. Better than that you don't need to generate that data in the first place during the offline baking process. Don't worry about dynamic objects. There is still data covering the empty space, it is just at the resolution of one page covering the world. If you need it at a higher resolution than that you can force a minimum depth to the octree.

In the end it still likely can't compete with the resolution a lightmap can get you if high res is what you are looking for. If lower res is the target it probably will be quite a bit more memory efficient because of not having any waste due to 2d parameterization. As for what a good page size would be I'm not sure as I haven't implemented any of this. If I did I probably couldn't talk about it yet. If anyone does implement this I'd love to hear about it.

## 2 comments:

Have a look at:






Smooth Mixed-Resolution GPU Volume Rendering

(http://medvis.vrvis.at/fileadmin/publications/vg08_smooth.pdf)

which does exactly what you propose: using a small 3d index texture to locate the bricks in the 3D cache texture.

And the smae approach with the octree structure on the GPU:

GigaVoxels : Ray-Guided Streaming for Efficient and Detailed Voxel Rendering

http://artis.imag.fr/Publications/2009/CNLE09/

which adds a feedback loop to the basic bricking idea.

Cool stuff, I'm doing something similar using Octree textures on the GPU representing colour data for more efficient and regularly sampled real-time volumetric painting.

Post a Comment