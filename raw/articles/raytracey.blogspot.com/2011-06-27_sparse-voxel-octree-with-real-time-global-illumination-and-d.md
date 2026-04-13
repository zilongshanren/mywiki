---
title: Sparse voxel octree with real-time global illumination and dynamic geometry
url: http://raytracey.blogspot.com/2011/06/sparse-voxel-octree-with-real-time.html
author: Sam Lapere
published: '2011-06-27'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Cyril Crassin has posted a very nice video on his blog at


Major improvements on previously published results (


The global illumination algorithm resembles photon mapping: instead of photon tracing, the scene is rasterized from the perspective of the light source and radiance is stored in the octree, followed by filtering in screen-space and a final gathering step using approximate cone tracing. More details:


[http://blog.icare3d.org/2011/06/interactive-indirect-illumination-and.html](http://blog.icare3d.org/2011/06/interactive-indirect-illumination-and.html)showing the latest developments in his sparse voxel octree research which will be presented at Siggraph 2011 in Vancouver.Major improvements on previously published results (

[http://artis.imag.fr/Membres/Cyril.Crassin/](http://artis.imag.fr/Membres/Cyril.Crassin/)) include real-time indirect lighting (for diffuse and glossy materials) and support for fully dynamic voxel objects (by fast mesh voxelization and updating the voxel octree in real-time). There has been research in animated sparse voxel octrees before (using rasterization, see[http://bautembach.de/wordpress/?page_id=7](http://bautembach.de/wordpress/?page_id=7),[http://www.youtube.com/watch?v=Tl6PE_n6zTk](http://www.youtube.com/watch?v=Tl6PE_n6zTk),[http://www.youtube.com/watch?v=Hnvr0hxyDvk](http://www.youtube.com/watch?v=Hnvr0hxyDvk)and[http://www.youtube.com/watch?v=gNZtx3ijjpo](http://www.youtube.com/watch?v=gNZtx3ijjpo), which doesn't look as detailed as[Jon Olick's raycasted static sparse voxel octree tech from Siggraph 08](http://www.youtube.com/watch?v=VpEpAFGplnI)), but this is the first time it's being done with ray casting (cone tracing actually).The global illumination algorithm resembles photon mapping: instead of photon tracing, the scene is rasterized from the perspective of the light source and radiance is stored in the octree, followed by filtering in screen-space and a final gathering step using approximate cone tracing. More details:

## 6 comments:

is it wrong for me to shed a tear from watching the video? amazing technology

Yeah it definitely is amazing.


Crytek is interested in this technology, so maybe CryEngine4 will have it :).

Yeah it definitely is amazing.




Crytek is interested in this technology, so maybe CryEngine4 will have it :).

Where did you hear that, i would love a source.

Great site i always enjoy checking up on it, its really amazing how often you are updating your site raytracing is really taking off these last few years.

Hi and thanks for the nice comment! I'm planning to write up a lot more updates once I'm getting the hang of programming my own stuff in C++ and CUDA :-)


Well, there are several clues that Crytek is interested in this tech, one of them is that Crytek invited Cyril Crassin to present his research on a conference talk in 2009 (look for "Gigavoxels: Voxels come into play" at http://artis.imag.fr/Membres/Cyril.Crassin/) Another clue is that Crytek has been talking about sparse voxel octrees and sparse surfel octrees in their recent presentations(http://raytracey.blogspot.com/2010/06/crytek-aims-for-cloud-and-sparse-voxel.html)

Thanks i will give it a read.


ive seen a voxel based version of cryteks light propagation volumes add correct shadows with cone tracing like Cyril and and a non uniform grid structure. You could cut down on the amount of voxelization of dynamic geometry by restricting it to shadow edges visable per frame just like a ray tracer.

"ive seen a voxel based version of cryteks light propagation volumes add correct shadows with cone tracing like Cyril and and a non uniform grid structure."


Sounds interesting. Do you have a link to this?

Post a Comment