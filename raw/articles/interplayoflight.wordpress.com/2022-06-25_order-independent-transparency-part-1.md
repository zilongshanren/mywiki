---
title: Order independent transparency, part 1
url: https://interplayoflight.wordpress.com/2022/06/25/order-independent-transparency-part-1/
author: Kostas Anagnostou
published: '2022-06-25'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Correctly sorting transparent meshes is one of the hard problems in realtime rendering. The typical solution to this is to sort the meshes by distance and render them back to front. This can’t address all transparency sorting artifacts, in cases when meshes intersect or self sorting artifacts in transparent meshes. Also correctly sorting particles with transparent meshes can be a challenge sometimes.

For an extreme but illustrative example, here is screenshot of Sponza rendered with transparent materials using hardware alpha blending with the over operator c1*a1 + c2*(1-a1). To mix things up I have added a particle system using additive blending (the yellow one)

![](../../assets/31f0e2276bbb307e.png)


![](../../assets/31f0e2276bbb307e.png)

For comparison, this is a ground truth image with correct transparency sorting.

![](../../assets/14bc0237cb774780.png)


![](../../assets/14bc0237cb774780.png)

Comparing these two images we can notice a lot of sorting artifacts and it quite hard to understand the spatial relationship of transparent surfaces. It would take quite a bit of mesh splitting into sort-able chunks to improve this, something that will increase the number of drawcalls and reduce batching opportunities without fully solving the problem.

An alternative to modifying the content and draw order is to utilise an order independent transparency (OIT) rendering technique. OIT techniques have been around for quite a few years and have actually been used in some games but have not found widespread use yet. I set about to investigate a few techniques to get a feel for how they perform and their visual quality.

Before we dive into specific techniques let’s pause for a bit consider the journey of a ray with radiance R travelling from a solid object towards the camera and let’s assume it intersects 4 transparent triangles at depths z0, z1, z2 and z3.

![](../../assets/33ada6cb9d535884.png)


![](../../assets/33ada6cb9d535884.png)

At each intersection point we calculate a colour **c i** and an opacity value

**a**. Closely related to the opacity at each point is the transmittance T

ii= (1-a

i) which expresses how much radiance goes through the surface at that point (aka visibility). Every time the ray goes through a surface point with transmittance T

i, only T

i*R of that radiance survives. If we assume that the ray intersects all 4 triangles, the amount of original radiance R (i.e. the colour of the cube) that will reach the camera will be

.


We can generalise this into a **transmittance function** T(z) to express the visibility (radiance allowed through) between any point with depth z and the camera

Why are we interested in this? Let’s consider a typical alpha blending scenario in which we sort the meshes and blend them back to front

This formulation may look weird at first but all I did was replace (1-ai) -> Ti in the usual “over” blending operator, for eg


**—>**

Going back to the full expansion, we notice that if we had some way to calculate the product of the transmittances (towards the camera) at any point, the order in which we blend the samples wouldn’t really matter, it is actually an addition. What this transmittance product at each point really is, is the output of the transmittance function T(z) I described above.

or to generalise for N samples

where T(z-1) = 1. The transmittance function is the basis for order independent transparency rendering. As long as we can define it that is and this is not trivial, more on that later.

After this brief context lets start exploring some OIT techniques. Like we discussed earlier, distance sorting and rendering transparent meshes back to front, in the ideal case that they don’t intersect with other meshes and have no self-sorting artifacts, can provide the correct result. This is rarely the case though, like demonstrated in the screenshot at the top of the post. Ideally we would want per pixel transparency sorting instead.

One of the ways this can be achieved is by creating [a per-pixel linked list](https://ubm-twvideo01.s3.amazonaws.com/o1/vault/gdc10/slides/Thibieroz_Nicolas_AdvancedVisualEffectsWithDirect3D_OIT_and_Indirect_Illumination_using_DX11_Linked_Lists_part1.pdf) (PPL) to store colour, transmissive (i.e. 1-a) and depth for each fragment, for basic alpha blending. Then, during a screen space pass, the per pixel list is distance sorted and composited back to front to achieve correct alpha blending. The technique is conceptually simple, one way to implement it is illustrated in the following diagram.

![](../../assets/a443f5ae9da32691.png)


![](../../assets/a443f5ae9da32691.png)

It is based on 2 buffers, the main one is a list of all the nodes, one per fragment. For this implementation I stored premultiplied colour, transmissive, depth and a pointer to the next node, packed in 12 bytes as such

```
struct Fragment
{
uint colour;
uint transmission : 8;
uint depth : 24;
uint next;
};
```

To reduce the colour footprint [I converted it](https://github.com/GameTechDev/AOIT-Update/blob/master/OIT_DX11/AOIT%20Technique/AOIT.hlsl) into [RGBE format](https://en.wikipedia.org/wiki/RGBE_image_format) and packed it into 32 bits. **Next **is the pointer to the next Node in the list.

To store the list I created a structured buffer to hold 8 nodes per pixel (so number of elements was width x height x 8). We also need a counter to keep track of how many nodes we have added to the buffer. A heads up that in contrast to DX11, in DX12 we don’t get this automatically, we need to create a separate buffer, a single element buffer of type DXGI_FORMAT_R32_TYPELESS, and pass it as an argument when creating a UAV for the structured buffer with CreateUnorderedAccessView().

The second buffer, I mentioned above, just stores the head of the list. For this I created a byte address buffer of width x height x 1 elements. This buffer is initialised to the UINT_MAX value every frame to signify that it is empty.

Code always speaks louder than words so here is a snippet of the shader that implements filling in the per pixel list.

```
RWByteAddressBuffer startOffsetBuffer : register(u0);
RWStructuredBuffer<TransparentFragment> fragments : register(u1);
[earlydepthstencil]
void PSMain(PSInputTransparent input)
{
float4 litPixel = CalculateLitPixel(input);
uint fragCount = fragments.IncrementCounter();
uint2 screenPos = uint2(input.position.xy);
uint offsetAddress = 4 * (SCREEN_WIDTH * screenPos.y + screenPos.x);
uint offsetAddressOld;
startOffsetBuffer.InterlockedExchange(offsetAddress, fragCount, offsetAddressOld);
float dist = input.worldPos.y / CAMERA_FAR; // convert to 0-1
const uint fragmentDepth = uint(dist * 0xFFFFFF); // convert to 24 bit uint
const float fragmentTransmissive = 1 - litPixel.a;
TransparentFragment frag;
frag.colour = PackRGBA(ToRGBE(float4(litPixel.rgb * litPixel.a, 1)));
frag.depth = fragmentDepth;
frag.transmission = fragmentTransmissive * 0xFF; // convert to 8 bit uint
frag.next = offsetAddressOld;
fragments[fragCount] = frag;
}
```

Simply, we increment the counter we attached to the node list (this is thread safe) and use the value as the “head” of the current pixel, atomically exchanging the new value with the old one in the per pixel offset buffer (startOffsetBuffer). Then all we need to do is calculate the colour and transmission of the current fragment and store it in the node list. In case we need to support additive blending, with can set the fragment’s transmission to 1.

Worth mentioning that since we are writing to an UAV from the pixel shader, this will deactivate [early z testing](https://fgiesen.wordpress.com/2011/07/08/a-trip-through-the-graphics-pipeline-2011-part-7/) and increase the rendering cost. It is worth prepending the pixel shader with [earlydepthstencil] to force the GPU to perform the test before running the shader.

Once we have rendered all the transparent surfaces into the per pixel list structure, all we need is a screen space to sort it by depth and blend the fragments.

```
ByteAddressBuffer startOffsetBuffer : register(t0);
StructuredBuffer<TransparentFragment> fragments : register(t1);
RWTexture2D<float4> mainRT : register(u0);
[numthreads(8, 8, 1)]
void CSMain(uint3 Gid : SV_GroupID, uint3 DTid : SV_DispatchThreadID, uint3 GTid : SV_GroupThreadID, uint GI : SV_GroupIndex)
{
uint2 screenPos = uint2(DTid.xy);
TransparentFragment frags[8];
int numFragments = 0;
uint offsetAddress = 4 * (SCREEN_WIDTH * screenPos.y + screenPos.x);
uint offset = startOffsetBuffer.Load(offsetAddress) ;
// copy the linked list for this fragment into an array
[loop]
while (offset != UINT_MAX && numFragments < 8)
{
frags[numFragments] = fragments[offset];
numFragments++;
offset = fragments[offset].next;
}
// sort the array by depth
[loop]
for (uint i = 1; i < numFragments; i++)
{
TransparentFragment toInsert = frags[i];
uint j = i;
while (j > 0 && toInsert.depth > frags[j - 1].depth)
{
frags[j] = frags[j - 1];
j--;
}
frags[j] = toInsert;
}
// get the background color from the frame buffer
float3 colour = mainRT[DTid.xy].rgb;
// combine the colors
for (i = 0; i < numFragments; i++)
{
float4 fragColour = FromRGBE(UnpackRGBA(frags[i].colour));
colour = (colour.rgb * frags[i].transmission) / 255 + fragColour.rgb;
}
mainRT[screenPos] = float4(colour.rgb, 1);
}
```

And that is it. How does technique perform? In terms of visuals, it will manage to resolve transparency correctly, as long as we don’t run out of nodes in the structured buffer, something that unfortunately happens in the, admittedly very unrealistic, test scene. The result is that it misses some transparent surfaces, especially the particles and has some flickering as different fragments find their way to the buffer per frame for some surfaces.

![](../../assets/756db156f3909813.png)


![](../../assets/756db156f3909813.png)

It also costs 4.20 ms to light the fragments and create the linked lists and another 1.32ms ms to sort and blend the fragments, at 1080p on a laptop RTX3080, compared to the 1.37 ms required to render the same scene with hardware alpha blending.

A big issue with this technique is actually its memory requirements. It would take approximately 200 MB to store the fragments for a 1080p image for 8 fragments per pixel, x4 that for a 4K image, and like we discussed it may not manage to resolve transparency correctly.

As with a lot of expensive sounding techniques though, YMMV, depending on your use case. Since we are storing the fragments in a “global” list of nodes (and not actually a separate list per pixel), this technique can assign more fragments per pixel than the original 8 layers I mentioned above implied. If there are exactly 8 overlapping transparent layers covering all the screen, then each pixel will get 8 fragments. But it is quite possible to get a maximum of 16 fragments per pixel if for example the transparent layers cover only half of the screen. So it could work reasonably well if screen coverage and number of layers is low.

Recently, a [visibility buffer was proposed](https://github.com/ConfettiFX/The-Forge) to only store the triangle index data in the linked list instead of colour/ transmissive/depth that can reduce the memory requirements to store the list significantly, but ultimately it will still support a limited number of nodes in the list and could run out of space eventually, depending on the use case.

A per pixel linked list is also great for ground truth OIT, this is actually how I produced the reference image at the top of the blog post, creating a structured buffer for 50 nodes per pixel.

PPLs can provide correct alpha sorting but require careful balance of memory/supported transparent layers and can place restrictions on how we author/place content to avoid overrunning the buffer and creating artifacts.

There are OIT techniques that lift the unbounded memory restriction, putting the transmissive function discussed earlier to good use, and this will be the topic of the next blog post.

Great post, as always!

One of my very favorite topics! :)

I actually spent many months working on an OIT solution for a game that never shipped, when I was at Valve. This was over 10 years ago and designed to run on XBox360, so the hardware constraints were much tighter – linked lists were definitely out!

My approach was very simple:

– phrase the problem as a weighted sum, as in your post

– use alpha*depth^-k as the weight for each fragment (based on the observation that visibility is an exponential falloff in a uniform density medium)

– use the alpha channel for the summed weight and divide by that in a final full-screen pass

Pros:

– very fast

– fixed memory cost

– you can render some effects at lower resolutions and combine the results in the final pass (essential for screen-filling particles)

– there is no popping as sort order changes, transitions are nice and smooth

Cons:

– requires a float16 frame buffer

– assumes a globally uniform-density transmissive medium

– does not produce correct results for all cases (eg very low opacity fragments in the foreground, with high opacity fragments in the background)

I discussed this technique with Louis Bavoil at nVidia and he published a nice paper where he explored other visibility functions.

The second ‘con’ was the most problematic. I tried all kinds of tricks to compute a more nuanced (non-uniform) visibility function, in order to yield a better result without requiring manual artist intervention. But that only made things slower and more complex, without ever quite fully solving the problem. I always ended up with noticeable screen-space artifacts, because the weighting function is so highly non-linear that errors tend to produce high-contrast transitions.

In the end my conclusion was that you needed to use low-complexity proxy geometry, rendered at a lower resolution, to seed the alpha channel with information about the visibility function (I ended up using 4 parameters defining a depth range with uniform density, with density falloff outside that region).

That uses some more memory, reduces performance a little and requires some additional work from artists/programmers (eg they would need to add a proxy sphere to a roughly spherical particle system) but provides enough control to tune the visual result and avoid the most objectionable visual artifacts.

Very interested to read part 2!

This has become my favorite blog :)

Sorry, I wrote the weight function wrong, it should be:

alpha*exp(-k*depth)

[…] Order independent transparency, part 1 […]

There were quite a few Dreamcast games that relied on the hardware’s OIT support in order to work properly. The Flycast emulator also fully supports it, you could look at their implementation.

[…] Order independent transparency, part 1 […]