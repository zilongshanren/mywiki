---
title: 'Half baked and a half: A small update.'
url: https://c0de517e.blogspot.com/2023/04/half-baked-and-half-small-update.html
published: '2023-04-12'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

[C0DE517E: Half baked: Dynamic Occlusion Culling](http://c0de517e.blogspot.com/2023/03/half-baked-dynamic-occlusion-culling.html)

Trying the idea of using the (incrementally accumulated) voxel data to augment the reprojection of the previous depth buffer.

Actually, I use here a depth from five frames ago (storing them in a ring buffer) - to simulate the (really worst-case) delay we would expect from CPU readbacks.


![](https://lh5.googleusercontent.com/BYNnJ6HcLYpYSEXNNzR7YAzll2apxicq1VcCOCgZsPLVEhVgnkS50CAXjipM587LRigpF2KaEjXoLogQyFjODgHQxskdNyUND8dhCDNnIxtxup3WmhA16_RWhhOtHcZEYu0lYGjLBwMcrOXdzttrzt4=w400-h232)


Here is the occlusion buffer, generated with different techniques. Top: without median, Bottom: with. Left to right: depth reprojection only, voxel only, both.



Debug views: accumulated voxel data. 256x256x128 (8mb) 8bit voxels, each voxel stores a 2x2x2 binary sub-voxel.

![](https://lh4.googleusercontent.com/-hoaDTpByJovNpY7f61dOfuClALcBsIpbYUCqVs8hDp5MI2ctIRFBToio4oC4TOyB-b_r2X4ckrlMk_ewqSvbX7RcKHVibs85ttAXEyY2QtgEKCX_UV5dWgkS2uzulW81AWcfvG2l8umiVoAmWH5utc=w400-h173)












And finally, only in the areas that still are "empty" from either pass, we do a further dilation (this time, a larger filter, starting from 3x3 but going up to 5x5, taking the farthest sample)

Scene and the final occlusion buffer (quarter res):

Note that the camera was undergoing fast rotation, you can see that the reprojected depth has a large area along the bottom and left edges where there is no information.

Debug views: accumulated voxel data. 256x256x128 (8mb) 8bit voxels, each voxel stores a 2x2x2 binary sub-voxel.

The sub-voxels are rendered only "up close", they are a simple LOD scheme. In practice, we can LOD more, render (splat) only up close and only in areas where the depth reprojection has holes.

Note that my voxel renderer (point splatter) right now is just a brute-force compute shader that iterates over the entire 3d texture (doesn't even try to frustum cull).

Of course that's bad, but it's not useful for me to improve performance, only to test LOD ideas, memory requirements and so on, as the real implementation would need to be on the CPU anyways.

Let's go step by step now, to further illustrate the idea thus far.

Naive Z reprojection (bottom left) and the ring buffer of five quarter-res depth buffers:

Note the three main issues with the depth reprojection:

- It cannot cover the entire frame, there is a gap (in this case on the bottom left) where we had no data due to camera movement/rotation.
- The point reprojection undersampled in the areas of the frame that get "stretched" - creating small holes (look around the right edge of the image). This is the primary job of the median filter to fix, albeit I suspect that this step can be fast enough that we could also supersample a bit (say, reproject a half-res depth into the quarter res buffer...)
- Disocclusion "holes" (see around the poles on the left half of the frame)

After the median filter (2x magnification). On the left, a debug image showing the absolute error compared to the real (end of frame) z-buffer.

The error scale goes from yellow (negative error - false occlusion) to black (no error) to cyan (positive error - false disocclusion. Also, there is a faint yellow dot pattern marking the areas that were not written at all by the reprojection.

Note how all the error right now it "positive" - which is good:

My current hole-filling median algorithm does not fix all the small reprojection gaps, it could be more aggressive, but in practice right now it didn't seem to be a problem.

Now let's start adding in the voxel point splats:

And finally, only in the areas that still are "empty" from either pass, we do a further dilation (this time, a larger filter, starting from 3x3 but going up to 5x5, taking the farthest sample)



We get the entire frame reconstructed, with an error that is surprisingly decent.



*A cute trick: it's cheap to use the subvoxel data, when we don't render the 2x2x2, to bias the position of the voxel point. Just a simple lookup[256] to a float3 with the average position of the corresponding full subvoxels for that given encoded byte.*



*This reasoning could be extended to "supervoxels", 64 bits could and should (data should be in Morton order, which would result in an implicit, full octree) encode 2x2x2 8 bit voxels... then far away we could splat only one point per 64bit supervoxels, and position it with the same bias logic (create an 8bit mask from the 64bits, then use the lookup).*



## No comments:

Post a Comment