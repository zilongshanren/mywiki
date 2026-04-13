---
title: Increasing wave coherence with ray binning
url: https://interplayoflight.wordpress.com/2022/05/08/increasing-wave-coherence-with-ray-binning/
author: Kostas Anagnostou
published: '2022-05-08'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Raytracing involves traversing acceleration structures (BVH), which encode a scene’s geometry, in an attempt to identify ray/triangle collisions. Depending on the rendering technique, eg raytraced shadows, AO, GI, rays can diverge a lot in direction something. This introduces additional cache and memory pressure as rays in a wave can follow very different paths in the BVH, ultimately colliding with different triangles.

Yet, ray generation is typically based on a limited set of random samples (eg a tiled blue noise texture), which we reuse across the frame, meaning that we raytrace using a limited number of ray directions. It sounds reasonable that we should be able to group rays by direction so as to enable all in a group to follow a similar path within the BVH tree and potentially hit the same triangle. Of course grouping by ray direction only is not enough, the origin of the ray matters as well, ideally we would like to group rays by both attributes.

A technique that can achieve that and increase coherence during raytracing is called ray binning. This has been used to accelerate [ray traced reflections in Battlefield V](https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s91023-it-just-works-ray-traced-reflections-in-battlefield-v.pdf). A different approach has also been implemented in Unity and [presented at Siggraph 2019](https://advances.realtimerendering.com/s2019/Benyoub-DXR%20Ray%20tracing-%20SIGGRAPH2019-final.pdf). I did a quick implementation of the latter technique to get a feel of how it works and improves raytracing.

We discussed how the ray origin is important during ray grouping, the authors solve this by performing the binning in screen tiles of 16×16 pixels with the assumption that neighbouring pixels will correspond to neighbouring surface points. There will be cases where this assumption does not hold, depending on the geometric complexity (edges), surface orientation with respect to the camera etc but it is a good starting point.

Considering randomly generated rays in a screen tile, they then project each ray to [octahedral space](https://jcgt.org/published/0003/02/01/paper.pdf), which is in 2D.

All the random rays we generate will then be projected into that 2D space. This is convenient as we can quantise the 2D space into the 16×16 tile, treat each pixel of this tile as a ray bin and derive a bin index for it.

```
rayDirection = SampleHemisphere(rand.xy);
rayDirection = rayDirection.x * tangent + rayDirection.y * bitangent + rayDirection.z * normal;
float2 octEncoded = OctahedralEncode(rayDirection);
uint2 binCoord = uint2((BINNING_TILE_SIZE -1)* octEncoded);
binIndex = binCoord.y * BINNING_TILE_SIZE + binCoord.x;
```

Code that converts 3D unit vectors to octahedral space you can find [here](https://knarkowicz.wordpress.com/2014/04/16/octahedron-normal-vector-encoding/). The method returns a float2 in the [0,1] range. The thread group size we use in the binning compute shader matches the bin tile size but it doesn’t have to like I’ll discuss later.

For every ray that falls into that bin we increase the count for it, in some groupshared memory we have allocated for that tile.

```
#define MAX_BINNING_TILE_SIZE_INDEX (BINNING_TILE_SIZE * BINNING_TILE_SIZE)
int rayBinIndex = 0;
if (binIndex != MAX_BINNING_TILE_SIZE_INDEX)
{
InterlockedAdd(binSize[binIndex], 1, rayBinIndex);
}
```

Once this is done we can find the offset of each bin

```
if (GroupThreadID.x == 0 && GroupThreadID.y == 0)
{
binOffset[0] = 0;
for (int i = 1; i < MAX_BINNING_TILE_SIZE_INDEX; ++i)
{
binOffset[i] = binOffset[i - 1] + binSize[i - 1];
}
}
```

and write out the coordinates for each bin

```
if (binIndex < MAX_BINNING_TILE_SIZE_INDEX)
{
uint groupdIndex = GroupID.y * binTileCountX + GroupID.x;
uint offset = groupdIndex * MAX_BINNING_TILE_SIZE_INDEX + binOffset[binIndex] + rayBinIndex;
rayBinCoord[offset] = ((screenPos.x & 0xffff) << 16) + (screenPos.y & 0xffff);
}
```

and the number of valid rays per tile

```
if (GroupThreadID.x == 0 && GroupThreadID.y == 0)
{
raysPerTile[GroupID.xy] = binOffset[MAX_BINNING_TILE_SIZE_INDEX-1] + binSize[MAX_BINNING_TILE_SIZE_INDEX-1];
}
```

To summarise, the binning shader outputs 3 buffers: a buffer that encodes the bin-sorted pixel coordinates for each ray **rayBinCoord**, the per-tile number of valid rays **raysPerTile**, and a screen space sized texture with the ray directions. It is worth clarifying that binning does not affect the ray directions, only their coordinates, which means that will not affect the visual quality.

Then, during raytracing, we can read that data to reorder rays to increase coherence in a wave like this:

```
// Compute the coordinates of the bin within each tile
uint2 perTileCoord = uint2(screenPos.x % BINNING_TILE_SIZE, screenPos.y % BINNING_TILE_SIZE);
uint perTileIndex = perTileCoord .y * BINNING_TILE_SIZE + perTileCoord .x;
// Get the tile coordinates
uint2 tileCoord = uint2(screenPos.x / BINNING_TILE_SIZE, screenPos.y / BINNING_TILE_SIZE);
uint tileIndex = screenPos.y * binTileCountX + screenPos.x;
// Get the screen space coordinates for this bin
uint binIndex = tileIndex * BINNING_TILE_SIZE * BINNING_TILE_SIZE + perTileIndex ;
uint binCoord = rayBinCoord[binIndex];
screenPos = uint2((binCoord & 0xffff0000) >> 16, binCoord & 0xffff);
//Read the ray direction
float3 rayDirection = raysRT[screenPos].xyz;
```

The bottom line of all that code is this: we swizzled the screenPos so that the current thread will now process a ray that belongs to a bin for similarly oriented rays, hopefully following the same path through the BVH.

To illustrate what this does in practice I generated a ray direction image using 4 ray directions alternating them per pixel:

This is the result of running the technique with this as an input:

The ray directions have been grouped into 4 bins. Waves running through this screen are have now more opportunities for coherent execution.

For a more realistic example, this is the original, randomly generated ray orientations I used to raytrace GI.

![](../../assets/12a253c2916cdba3.png)


![](../../assets/12a253c2916cdba3.png)

Ray binning rearranges the coordinates within a tile to group together rays of similar orientations (this particular image is generated with 32×32 tiles which found performs better in this context)

![](../../assets/eb7999cdc6823b0b.png)


![](../../assets/eb7999cdc6823b0b.png)

Zooming in the same area as above to make ray binning a bit more obvious:

The ray directions have now been been rearranged broadly based on their direction something that can help improve ray coherence in a wave.

I mentioned earlier that the binning is done per tile in an attempt to achieve spatial locality as well but this won’t always be the case especially with large tiles and complex surfaces. We have the option to bin using smaller tiles which may increase locality but it can also make binning based on direction less effective. For example this is the same ray direction buffer as above binned with 16 pixel bin tiles.

The ray direction bins are now smaller, something that may affect divergence in a wave.

In the implementation I described above I assumed that the bin tile size and the threadgroup size during the binning pass are the same but they don’t have to. It is quite possible to use a smaller bin tile than the threadgroup size (reminder that all the bin tile size does is quantise the octahedral ray direction representation), to make each bin size larger. For example this is a rerun of the above technique using a bin tile of size 8×8 and a threadgroup size of 32×32.

If we compare the result with the 32×32 bin tile size above we notice that it looks noisier as the bins are now larger and allow for more divergent rays. This can have an impact on performance and indeed, I found this set up to be slower than the 32 bin size one.

When using the binned ray direction buffer to raytrace we can use any threadgroup size, it doesn’t have to match the bin tile size, but it helps to be large enough so that waves can fall within coherent regions.

Finally, this is the per wave variance in number of steps through the BVH each ray does, as an indication of ray divergence.

![](../../assets/c69642b6ca1f360e.png)


![](../../assets/c69642b6ca1f360e.png)

This is the per wave variance with ray binning (32×32 bin sizes)

![](../../assets/9a01eb56ab810d55.png)


![](../../assets/9a01eb56ab810d55.png)

The image is darker in general (lower variance) and also seems improved in areas of high geometric complexity.

In terms of performance, ray binning is 7.2% faster than without when software raytracing GI using a bin tile size of 32×32 and a thread group of 16×8 for the raytrace shader. A larger bin tile seems to help, at least in this case, reducing it to 16×16 drops the increase in performance to about 2.4%. The binning pass cost is minuscule and we can piggy back it on the ray direction generation pass hybrid raytracing engines are likely to have anyway.

Very specific and useful, thank you once again! I really appreciate how easy you make it for readers to replicate your experiments.

Are you aware of any techniques that process rays in blocks grouped by BVH subtree? The goal being to correlate spatial locality with memory locality in a coarse grained way. So if the scene is divided into 100 sub-trees then there would be 100 corresponding ray queues. You would start by adding rays to these queues based on their start position when they are first generated, then you would process queues (longest first), and when a ray exits its sub-tree you append it to the queue of the neighbor sub-tree it entered.

That would clearly improve memory access locality and I would guess also reduce loop iteration count variance; you’re always processing a block of rays that are traversing the same small sub-tree… but I don’t have enough experience with compute shaders to know if queuing rays like that can be done in a performant way (too much contention on queue read/write cursors?), and you might end up with a tail of small blocks (low wave utilization), plus you could end up doing a bunch of redundant traversal work (dividing the scene into separate similarly-sized BVH sub-trees could increase the overall number of nodes/planes).