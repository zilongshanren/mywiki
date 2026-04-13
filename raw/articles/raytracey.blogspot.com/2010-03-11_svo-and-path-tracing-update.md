---
title: SVO and path tracing update
url: http://raytracey.blogspot.com/2010/03/svo-and-path-tracing-update.html
author: Sam Lapere
published: '2010-03-11'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Hans Krieg, the (only?) programmer of the Voxelstein 3d engine incorporated a path tracing extension to the engine which uses SVO and BIH (bounding interval hierarchy) to render the voxels. The code runs on both CPU and GPU(CUDA) and the first images are rather crude, but have a warm and natural global illumination to them.

For pictures and details about the engine, visit

[http://www.jonof.id.au/forum/index.php?topic=1411.msg12406#msg12406](http://www.jonof.id.au/forum/index.php?topic=1411.msg12406#msg12406)

UPDATE: Samuli Laine has written an excellent paper entitled "Efficient Sparse Voxel Octrees" which uses a nifty trick to make the contours of the voxels much less blocky. On top of that, he posted a video and the complete open sourced CUDA code of his technique as well. All can be found, read, watched on

[http://code.google.com/p/efficient-sparse-voxel-octrees/](http://code.google.com/p/efficient-sparse-voxel-octrees/ ). Fantastic work and probably the most practical and "efficient" implementation of SVOs yet, ready to be abused by graphics engineers :-)

## No comments:

Post a Comment