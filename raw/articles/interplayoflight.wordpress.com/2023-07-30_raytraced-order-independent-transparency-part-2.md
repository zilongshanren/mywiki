---
title: Raytraced Order Independent Transparency part 2
url: https://interplayoflight.wordpress.com/2023/07/30/raytraced-order-independent-transparency-part-2/
author: Kostas Anagnostou
published: '2023-07-30'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

In the previous [blog post](https://interplayoflight.wordpress.com/2023/07/15/raytraced-order-independent-transparency/) I discussed how raytracing can be used to achieve order independent transparency (OIT) for some types of transparencies and how it compares to other OIT methods like per pixel linked lists and Multi-layer Alpha blending (MLAB). The basic idea, since DXR doesn’t support distance sorted traversal of the BVH, was to use a closest hit shader to find the closest to the camera intersection and then use the position of the intersection as the origin of a new ray to trace through the BVH. That worked well in that it achieves OIT but the fact that each ray has to traverse the TLAS from the top every time we find an intersection is not ideal.

Back in the dark ages of the Intel HD4000 GPU, when I was tinkering with [raytracing using compute shaders](https://interplayoflight.wordpress.com/2022/04/09/raytracing-a-4-year-retrospective/), I had actually experimented with combining raytracing with “per pixel linked lists”, storing the result of each intersection in a per pixel array and combining the results at the end to implement OIT. That did work, assuming that one didn’t try to render a very large number of overlapping transparencies, but the cost of the pass was very high.

Wondering how this would work in the context of DXR, I did a quick experiment to combine raytracing with a more traditional OIT method. DXR provides a mechanism to process all intersections through the acceleration structure using an anyhit shader, without the need to start traversal from the top every time, which sounds ideal for our use case.

Given that there is no pixel access order issues with raytracing, unlike rasterisation, there is no need for synchronisation when accessing a per pixel structure, neither atomics nor raster order views. We do need to pass around that per pixel structure through the payload though, and since for performance we need to keep this as small as possible, storage space is something that we will need to consider. A per pixel array to store the intersections, similarly to a per-pixel list, could run out of space in complex transparency rendering scenarios creating artifacts, or if we reserve a lot of space, affect performance negatively. An adaptive technique is more suitable in memory limited scenarios and MLAB is the one I tried in this case.

This all was fairly easy to set up, I just added an anyhit shader to the hit group and moved [all lighting code](https://interplayoflight.wordpress.com/2023/07/15/raytraced-order-independent-transparency/) out of the the ray gen shader and into the anyhit shader. On top of that I added the MLAB implementation straight out of the rasterised version which I described in [an older post](https://interplayoflight.wordpress.com/2022/07/02/order-independent-transparency-part-2/). I restricted the implementation to 4 nodes per pixel (MAX_NODE_COUNT is 4) which seems to provide a good balance between quality and memory. The shader looks broadly like the following, I removed the lighting parts to keep it short(-er). For a detailed explanation of how MLAB works it is worth checking the blog post I mentioned earlier:

```
[shader("anyhit")]
void AnyHit(inout Payload payload : SV_RayPayload, in Attributes attr : SV_IntersectionAttributes)
{
uint geometryID;
uint materialID;
// Material and geometry ID are packed into InstanceID
UnpackInstanceID(InstanceID(), materialID, geometryID);
float3 barycentrics = float3((1.0f - attr.uv.x - attr.uv.y), attr.uv.x, attr.uv.y);
HitPointData data = GetHitpointData(geometryID, PrimitiveIndex(), barycentrics);
float fragmentDepth = float(RayTCurrent() / CAMERA_FAR);
float3 viewDir = -WorldRayDirection();
// Load material properties at the hit point
Material material = LoadMaterial(materialID, data.uv);
// light the transparent surface
uint fragmentColour = .....
fragmentTransmission = 1.0 - float(material.Albedo.a);
if (payload.depth[0] < AOIT_MAX_DEPTH) // AOIT_MAX_DEPTH is 1.0
{
float depth[MAX_NODE_COUNT + 1];
float trans[MAX_NODE_COUNT + 1];
uint color[MAX_NODE_COUNT + 1];
for (int i = 0; i < MAX_NODE_COUNT; i++)
{
depth[i] = payload.depth[i];
trans[i] = payload.trans[i];
color[i] = payload.color[i];
}
int index = 0;
float prevTrans = 1.0;
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
for (int i = MAX_NODE_COUNT - 1; i >= index; i--)
{
depth[i + 1] = depth[i];
trans[i + 1] = trans[i] * fragmentTransmission;
color[i + 1] = color[i];
}
//adjust the fragment's transmission
float newFragTrans = fragmentTransmission * prevTrans;
//insert new fragment
depth[index] = fragmentDepth;
trans[index] = newFragTrans;
color[index] = fragmentColour;
// pack representation if we have too many nodes
if (depth[MAX_NODE_COUNT] != AOIT_MAX_DEPTH)
{
float3 toBeRemovedCol = FromRGBE(UnpackRGBA(color[MAX_NODE_COUNT])).rgb;
float3 toBeAccumulCol = FromRGBE(UnpackRGBA(color[MAX_NODE_COUNT - 1])).rgb;
float3 newColour = toBeAccumulCol + toBeRemovedCol * trans[MAX_NODE_COUNT - 1] * rcp(trans[MAX_NODE_COUNT - 2]);
color[MAX_NODE_COUNT - 1] = PackRGBA(ToRGBE(float4(newColour, 1)));
trans[MAX_NODE_COUNT - 1] = trans[MAX_NODE_COUNT];
}
for (int i = 0; i < MAX_NODE_COUNT; i++)
{
payload.depth[i] = depth[i];
payload.trans[i] = trans[i];
payload.color[i] = color[i];
}
}
else
{
payload.depth[0] = fragmentDepth;
payload.trans[0] = fragmentTransmission;
payload.color[0] = fragmentColour;
}
//ignore this hit to continue traversing the BVH
IgnoreHit();
}
```

Compared to the previous implementation of raytraced OIT where the closest hit shader returned the hit point data (position, normal, material id etc) and the raygen shader fetched material data and did the lighting, in this version the anyhit shader has to do everything, since we need to store the final, lit transparent fragment in the MLAB structure. This makes for a pretty large anyhit shader, which in general is not ideal in terms of performance.

The payload structure looks like this:

```
struct Payload
{
float depth[MAX_NODE_COUNT];
float trans[MAX_NODE_COUNT];
uint color[MAX_NODE_COUNT];
};
```

it stores depth, transmission and colour for 4 fragments, the colour [converted to RGBE and packed into a uint](https://github.com/GameTechDev/AOIT-Update/blob/master/OIT_DX11/AOIT%20Technique/AOIT.hlsl).

After we have updated the MLAB structure with a new fragment, we “ignore” this hit so that traversal can continue, without resetting to the top of the acceleration structure like the technique described in the previous blog post. Also, any changes we make to the payload persists despite us rejecting the hit, which allows us to gradually blend all fragments.

Once traversal is done, we return to the raygen shader to blend the fragments, already correctly sorted:

```
TraceRay( Scene,
RAY_FLAG_SKIP_CLOSEST_HIT_SHADER, // skip closest hit shader, not needed.
0xFF,
0,
1,
0,
ray,
payload);
float3 colour = 0;
float transmission = 1;
uint i = 0;
while (i < MAX_NODE_COUNT && payload.depth[i] < AOIT_MAX_DEPTH)
{
colour += transmission * FromRGBE(UnpackRGBA(payload.color[i])).rgb;
transmission = payload.trans[i];
i++;
}
float3 bg = output[screenPos].rgb;
output[screenPos] = float4(colour.rgb + transmission * bg, 0);
```

Like discussed, the anyhit shader is very large, does this approach offer any benefit compared to the previous approach (of using the closest hit shader and using the hit point as an origin of a new ray)?

For reference, this is the rasterised MLAB with 4 fragments rendering at 1080p on an RTX 3080 laptop, costing 2.02 ms

![](../../assets/25a6440b93ed2b5c.png)


![](../../assets/25a6440b93ed2b5c.png)

This is the same scene raytraced with the technique described in the previous blog post, at 3.64 ms

![](../../assets/b36752b553fa97ff.png)


![](../../assets/b36752b553fa97ff.png)

Finally, this is raytraced MLAB, again with 4 fragments, rendering at 2.46 ms.

![](../../assets/9a4861a2e28ea375.png)


![](../../assets/9a4861a2e28ea375.png)

It turns out that despite using an anyhit shader and despite the shader being long and complicated, it still beats using a closest hit shader and firing new rays at the intersections. Worth mentioning that the payload size does not contribute that much to the total cost, I tried packing depth and transmission from 2 floats to 1 uint per fragment node and that dropped the cost by about 0.02ms.

There is a caveat though with using an anyhit shader, we lose the ability to modify the ray direction per intersection to implement refraction. Also, if you squint, there is a small difference in the final image between rasterised and raytraced MLAB, noticeable in the distance. This is because MLAB is not **truly **order independent. As the fragment structure overflows it will blend the last 2 nodes and depending on the order the fragments arrive, blending the last 2 nodes could provide the wrong results as it loses any distance information. It is very likely that the order rasterised MLAB visits the surfaces is different to that of raytraced MLAB leading to minor differences.

Raytraced MLAB is a bit more expensive than rasterised MLAB but has none of the memory overhead of the technique (68MB for the current implementation for a 1080p resolution). There is another interesting feature with raytraced MLAB, I tried to up the number the nodes per pixel to 8, from 4, and the cost increased to 2.50 ms from 2.44 ms (I used the packed payload). The same node increase for rasterised MLAB increased the cost to 3.16 ms from 2.02 ms, so it appears that the raytraced version scales much better.