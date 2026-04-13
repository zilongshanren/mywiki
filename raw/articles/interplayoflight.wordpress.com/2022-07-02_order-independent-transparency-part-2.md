---
title: Order independent transparency, part 2
url: https://interplayoflight.wordpress.com/2022/07/02/order-independent-transparency-part-2/
author: Kostas Anagnostou
published: '2022-07-02'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

In the [previous blog post](https://interplayoflight.wordpress.com/2022/06/25/order-independent-transparency-part-1/) we discussed how to use a per-pixel linked list (PPLL) to implement order independent transparency and how the unbounded nature of overlapping transparent surfaces can be problematic in terms of memory requirements, and ultimately may lead to rendering artifacts. In this blog post we explore approximations that are bounded in terms of memory.

Also in the previous blog post we discussed the transmittance function

and how it can be used to describe how radiance is reduced as it travels through transparent surfaces

If we were to plot a transmittance function, it could look something like this:

![](../../assets/f983bd1f0ad18438.png)


![](../../assets/f983bd1f0ad18438.png)

The various z-distances are measured from the camera. The function starts at a value of one and reduces asymptotically towards zero (which means it gets close but never reaches it)

If there was a way to figure out what that function is before we rendered the transparent surfaces, then there would be no need to sort the fragments, we could get truly order-independent transparency (R is the background colour).

This is not that easy of course, techniques that use the transmittance function to implement OIT typically perform 2 geometric passes, one to calculate that function and one to use it to render the transparent surfaces without sorting. The other issue is that, like in the per-pixel linked list approach discussed in the previous blog post, the number of samples required to represent this function is unbounded depending on the number of overlapping surfaces on screen. For this reason we resort to calculating an approximation of the transmittance function that can fit in limited memory space.

Before we delve deeper, it is worth taking a break to talk about custom alpha blending. When we submit a number of drawcalls which use a pixel shader writing to a rendertarget, the GPU is free to schedule the warps/wavefronts are it sees fit and indeed the drawcalls may overtake each other as the shaders fight for resources. When it comes to writing to the rendertarget though, the fun stops and the GPU enforces a strict access order to the rendertarget to ensure that drawcalls that were issued first will get to write their output first. If, instead to writing to a rendertarget through the fixed-function [ROP unit](https://developer.nvidia.com/content/life-triangle-nvidias-logical-pipeline), we choose to read and write to a UAV to implement a custom blending mode we lose this access order guarantee and artifacts arise which are non-deterministic and very distracting. Enter [Rasteriser Order Views](https://www.intel.com/content/www/us/en/developer/articles/technical/rasterizer-order-views-101-a-primer.html) (ROVs). This is a relatively old GPU feature, dating back to Intel’s PixelSync extensions and now being formally part of graphics APIs including DX12 in which it is listed as [an optional feature](https://microsoft.github.io/DirectX-Specs/d3d/RasterOrderViews.html). Effectively, ROVs reintroduce the strict access order to a rendertarget when accessed through a UAV in a pixel shader. They are also very easy to use, all we have to do is replace (ROVs are supported for buffers as well)

`RWTexture2D transparencyRT : register(u0);`


with

`RasterizerOrderedTexture2D transparencyRT : register(u0);`


ROVs don’t come for free unfortunately, implementing normal alpha blending with a custom blend instead of using the fix-function unit raises the cost from 1.37 ms to 3.24 ms on an RTX3080 laptop GPU, rendering at 1080p. In some older experiments I noticed that the impact is less on Intel GPUs. AMD GPUs do not seem to support this feature at all at the moment.

With ROV rendering, adjacent (in the timeline) drawcalls that overlap in the screen can introduce more delay than normal hardware blending, since the GPU will be forced to serialise them. To quickly demonstrate this I rendered a grid of planes (5x3x50), ordering them in such a way that they are rendering depth first.

![](../../assets/1f626882c8feb72a.png)


![](../../assets/1f626882c8feb72a.png)

With ROV blending, this costs 3.20 ms at 1080p. If I shuffle the list of drawcalls to reduce the probability of planes that overlap on screen render consecutively, the cost drops to 2.1ms.

Regardless, it is an interesting feature that opens the door to a number of transparency rendering solutions, for example if we attach a 2 channel buffer along with the ROV UAV rendertarget, to store the depth of the closest to the camera fragment and the accumulated pixel transmission, and use the “over” operator if the new fragment is closer and “under” if it is further

```
float3 colour = transparencyRT[screenPos].rgb;
float2 depthAlpha = transparentDepthAlphaRT[screenPos];
const float fragmentDepth = input.worldPos.x / input.worldPos.y;
if (fragmentDepth < depthAlpha.x)
{
//fragment closer to the camera, use over operator
colour = colour + litPixel.rgb * litPixel.a;
}
else
{
// use under operator
colour = depthAlpha.y * litPixel.a * litPixel.rgb + colour;
}
//accumulate transmission
depthAlpha.y *= (1 - litPixel.a);
transparentDepthAlphaRT[screenPos] = depthAlpha;
transparencyRT[screenPos] = colour;
```

we can achieve some fairly decent transparency sorting, although, of course, not error free, for 3.9 ms.

![](../../assets/7a7562fb7e44b372.png)


![](../../assets/7a7562fb7e44b372.png)

This is the scene rendered with hardware alpha blending for comparison purposes (1.37 ms).

![](../../assets/454d13d4e6256262.png)


![](../../assets/454d13d4e6256262.png)

Going back to OIT and transmissive functions, one technique that approximates it with a limited per pixel memory budget is [Adaptive Transparency](https://www.intel.com/content/dam/develop/external/us/en/documents/37944-adaptive-transparency-hpg11.pdf). The technique allocates a small number of N “nodes” per pixel, each containing the transmission and depth of a fragment. During the first geometry pass it populates the nodes of this list, a difference with a PPLL being that if the number of nodes exceed the preallocated number N, it will compress the transmittance function removing nodes that don’t contribute significantly to make it fit.

![](../../assets/e44b96b6dd82b690.png)


![](../../assets/e44b96b6dd82b690.png)

During the second geometry pass the technique uses the function to composite the fragments in an OIT fashion. This is an interesting technique, if you don’t mind the two geometry passes, which gracefully handles overrun of the preallocated per pixel data.

I didn’t actually implement this method but a newer variation which only needs one geometry pass to render OIT, called [Multi-layer Alpha Blending](https://www.intel.com/content/www/us/en/developer/articles/technical/multi-layer-alpha-blending.html) (MLAB). Conceptually this technique is even simpler, we still preallocate a small number of nodes per pixel, each node containing premultiplied colour, transmission and depth. The per-pixel buffer is kept sorted, on the fly, as each fragment arrives. The original paper suggests using bubble sort but this moves a lot of data around so I based my implementation on Intel’s [AOIT sample](https://github.com/GameTechDev/AOIT-Update) which finds the appropriate place for the new node and pushes any following nodes down the list to make room for it. In diagrams, assuming an array to store N nodes with an extra node for overrun:

**Max **is just a value to denote that the node is empty. Nodes are pushed to the right to make room and the new fragment is inserted in the correct position and depth.

Finally, since the array has overrun, we need to merge the last 2 nodes to keep the total allocation to N nodes.

To store each node I use 8 bytes, and I encode the premultiplied colour into a unsigned int as discussed in the previous post.

```
struct TransparentFragment
{
uint colour;
uint transmission : 8;
uint depth : 24;
};
```

The node arrays are stored in a structured buffer and accessed through a ROV to eliminate data races. In HLSL filling the buffer looks like this.

```
struct TransparentFragment
{
uint colour;
uint transmission : 8;
uint depth : 24;
};
struct OITData
{
TransparentFragment frags[MAX_NODE_COUNT];
};
RasterizerOrderedTexture2D<uint> clearMask : register(u0);
RasterizerOrderedStructuredBuffer<OITData> fragments : register(u1);
[earlydepthstencil]
void PSMain(PSInputTransparent input)
{
float4 litPixel = CalculateLitPixel(input);
uint2 screenPos = uint2(input.position.xy);
// flag to determine if the pixel is clear
bool clear = clearMask[screenPos];
// find offset into the structured buffer for this pixel
uint offsetAddress = (SCREEN_WIDTH * screenPos.y + screenPos.x);
TransparentFragment frags[MAX_NODE_COUNT];
// depth, colour and transmission for the new fragment
const float dist = saturate(input.worldPos.y / CAMERA_FAR);
const uint fragmentDepth = uint(dist * AOIT_MAX_DEPTH);
const uint fragmentColour = PackRGBA(ToRGBE(float4(litPixel.rgb * litPixel.a, 1)));
const float fragmentTransmission = 1 - litPixel.a;
//if pixel is clear, initialise node array
if (clear)
{
frags[0].colour = fragmentColour;
frags[0].transmission = uint(fragmentTransmission * AOIT_MAX_TRANSMISSIVE);
frags[0].depth = uint(fragmentDepth);
for (int i = 1; i < MAX_NODE_COUNT; i++)
{
frags[i].colour = 0;
frags[i].transmission = AOIT_MAX_TRANSMISSIVE;
frags[i].depth = AOIT_MAX_DEPTH;
}
// pixel not clear any more
clearMask[screenPos] = false;
}
else
{
frags = fragments[offsetAddress].frags;
uint depth[MAX_NODE_COUNT + 1];
float trans[MAX_NODE_COUNT + 1];
uint color[MAX_NODE_COUNT + 1];
//split data into different arrays
for (int i = 0; i < MAX_NODE_COUNT; i++)
{
depth[i] = frags[i].depth;
trans[i] = frags[i].transmission / float(AOIT_MAX_TRANSMISSIVE);
color[i] = frags[i].colour;
}
int index = 0;
float prevTrans = 1;
//find position we need to insert the new fragment
for (int i = 0; i < MAX_NODE_COUNT; i++)
{
if (fragmentDepth > depth[i])
{
index++;
prevTrans = trans[i];
}
}
// Make room for the new fragment.
for (int i = MAX_NODE_COUNT - 1; i >= index ; i--)
{
depth[i + 1] = depth[i];
trans[i + 1] = trans[i] * fragmentTransmission;
color[i + 1] = color[i];
}
//adjust the fragment's transmission
const float newFragTrans = fragmentTransmission * prevTrans;
//insert new fragment
depth[index] = fragmentDepth;
trans[index] = newFragTrans;
color[index] = fragmentColour;
// pack representation if we have too many nodes
if ( depth[MAX_NODE_COUNT] != AOIT_MAX_DEPTH)
{
float3 toBeRemovedCol = FromRGBE(UnpackRGBA(color[MAX_NODE_COUNT])).rgb;
float3 toBeAccumulCol = FromRGBE(UnpackRGBA(color[MAX_NODE_COUNT - 1])).rgb;
float3 newColour = toBeAccumulCol + toBeRemovedCol * trans[MAX_NODE_COUNT - 1] * rcp(trans[MAX_NODE_COUNT - 2]);
color[MAX_NODE_COUNT - 1] = PackRGBA(ToRGBE(float4(newColour, 1)));
trans[MAX_NODE_COUNT - 1] = trans[MAX_NODE_COUNT];
}
//prepare data to copy to structure buffer
for (int i = 0; i < MAX_NODE_COUNT; ++i)
{
frags[i].transmission = uint(trans[i] * AOIT_MAX_TRANSMISSIVE);
frags[i].depth = uint(depth[i]);
frags[i].colour = color[i];
}
}
fragments[offsetAddress].frags = frags;
}
```

The purpose of the clear mask, which is a UINT8 screen size rendertarget, is only to provide us with a quick way to mark whether each pixel has a valid array of fragments and to subsequently clear it if yes, to avoid touching the structure buffer.

Once all the transparent surfaces has been rendered and the buffer has been populated we need a screen space resolve step to get final transmission and colour and blend with the background

```
StructuredBuffer<OITData> fragments : register(t0);
RWTexture2D<float4> mainRT : register(u0);
RWTexture2D<uint> clearMask : register(u1);
[numthreads(8, 8, 1)]
void CSMain(uint3 Gid : SV_GroupID, uint3 DTid : SV_DispatchThreadID, uint3 GTid : SV_GroupThreadID, uint GI : SV_GroupIndex)
{
uint2 screenPos = uint2(DTid.xy);
// only process pixels that we have fragment data for
bool clear = clearMask[screenPos];
// get the color of the closest non-transparent object from the frame buffer
float3 background = mainRT[screenPos].rgb;
float3 color = background;
if (!clear)
{
uint offsetAddress = (imSize.x * screenPos.y + screenPos.x);
// read node array for this pixel from structure buffer
OITData data = fragments[offsetAddress];
float trans = 1;
color = 0;
// go over the node array and blend the fragments
uint i = 0;
while (i < MAX_NODE_COUNT && data.frags[i].depth < AOIT_MAX_DEPTH)
{
color += trans * FromRGBE(UnpackRGBA(data.frags[i].colour)).rgb;
trans = data.frags[i].transmission / float(AOIT_MAX_TRANSMISSIVE);
i++;
}
//finally blend the background colour as well.
color.rgb += background * trans;
//pixel done, clear it for next frame
clearMask[screenPos] = true;
}
mainRT[screenPos] = float4(color.rgb, 1);
}
```

With MLAB, as with other techniques that approximate the transmittance function, we have the option to vary the number of nodes to balance memory, visual quality and performance.

For example, this is the result of running MLAB with 2 nodes, rendering at 1920×1080, requiring ~35MB to store structure buffer and clear mas and costing 4.4 ms.

![](../../assets/cfc1cfc4d8e32745.png)


![](../../assets/cfc1cfc4d8e32745.png)

this is with 4 nodes, requiring ~68MB storage and costing 6.8 ms.

![](../../assets/869119ca3d06f4e6.png)


![](../../assets/869119ca3d06f4e6.png)

![](../../assets/41004fdff5c6a478.png)


![](../../assets/41004fdff5c6a478.png)

![](../../assets/ddb85d51d4b553c1.png)


![](../../assets/ddb85d51d4b553c1.png)

The 2 node version has artifacts but it is a massive improvement over no sorting, 4 nodes can handle particles better and the 8 node version is probably not worth it for that cost and memory.

The per pixel linked list we discussed in the previous blog post would take 200MB to store and 8 node list and 5.5ms to render at the same resolution, and it could not avoid artifacts.

The merging of the last two nodes step of MLAB prevents it from being fully OIT as the order the fragments arrive may make a difference but in my test cases, if there is any, it is imperceptible compared to the ground truth.

This technique works well, it is simple to implement, requires only one geometry pass and can adapt to available memory budgets much better. On the other hand it is not particularly cheap and it depends on support for ROVs which is not a given on all GPUs.

We are not done yet, there are still a couple of techniques worth discussing, in the next and final OIT blog post.

[…] sein und schließlich zu Rendering-Artefakten führen kann . . . Im selben Beitrag werden untersucht Annäherungen, die hinsichtlich des Gedächtnisses begrenzt […]