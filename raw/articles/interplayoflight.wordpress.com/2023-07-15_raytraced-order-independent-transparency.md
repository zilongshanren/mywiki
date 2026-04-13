---
title: Raytraced Order Independent Transparency
url: https://interplayoflight.wordpress.com/2023/07/15/raytraced-order-independent-transparency/
author: Kostas Anagnostou
published: '2023-07-15'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

About a year ago I reviewed a number of Order Independent Transparency (OIT) techniques ([part 1](https://interplayoflight.wordpress.com/2022/06/25/order-independent-transparency-part-1/), [part 2](https://interplayoflight.wordpress.com/2022/07/02/order-independent-transparency-part-2/), [part 3](https://interplayoflight.wordpress.com/2022/07/10/order-independent-transparency-endgame/)), each achieving a difference combination of performance, quality and memory requirements. None of them fully solved OIT though and I ended the series wondering what raytraced transparency would look like. Recently I added (some) DXR support to the toy engine and I was curious to see how it would work, so I did a quick implementation.

The implementation was really simple. Since there is no mechanism to sort the nodes of a BLAS/TLAS based on distance from the camera, the ray generation shader keeps tracing rays using the result of the closest hit shader as the origin for the next ray until there is nothing else to hit. The acceleration structures only contain transparent meshes:

```
float transmission = 1.0;
float3 radiance =float3(0.0, 0.0, 0.0);
while (payload.hasHit())
{
payload.materialID = INVALID_ID;
TraceRay( Scene,
RAY_FLAG_NONE,
0xFF,
0,
1,
0,
ray,
payload);
if (payload.materialID != INVALID_ID)
{
// Load material properties at the hit point
Material material = LoadMaterial(payload.materialID, payload.uv);
// Light the hit point
float3 hitPointLit = ......;
// blend using the "under" operator
radiance.rgb += transmission * material.Albedo.a * hitPointLit;
transmission *= (1 - material.Albedo.a);
// use the hit position as the origin of the next ray
ray.Origin = payload.position;
}
}
// load background pixel
float3 bg = output[screenPos].rgb;
// apply transmission to background and overlay transparency
output[screenPos] = radiance.rgb + transmission * bg;
```

In this case the first ray origin is the camera and the ray direction is from the camera towards the scene, unlike the more common applications of raytraced shadows, AO etc, which use the world position of a surface point as the origin.

Briefly, we retrieve the payload from the closest hit shader, resolve material data, perform lighting of the hit point (i.e. the point on the transparent surface) and then composite the result using the material alpha value. One thing worth calling out is that since we are effectively compositing front-to-back we can’t use the “over” operator, typically used when rendering transparency sorted back-to-front, we need to use the [“under” operator](https://developer.nvidia.com/content/transparency-or-translucency-rendering). That’s pretty much all that is needed to get raytraced transparencies working.

I will use the original (quite frankly unrealistic) test case to get a feel of how much better (or worse) this is compared to the OIT techniques I have [prototyped](https://interplayoflight.wordpress.com/2022/06/25/order-independent-transparency-part-1/), and that was the full Sponza scene being transparent.

Rendered with normal, hardware alpha blending it costs 1.2ms at 1080p on a RTX3080 mobile GPU. This is the cheapest approach but the transparency sorting is all wrong.

![](../../assets/da1170796a81cb39.png)


![](../../assets/da1170796a81cb39.png)

Rendered with a per pixel linked list with 8 nodes, it costs 4.62 ms

![](../../assets/c87975dccc286e20.png)


![](../../assets/c87975dccc286e20.png)

Rendered with Multi-layer Alpha blending (MLAB) with 4 nodes, it costs 5.13ms

![](../../assets/89ffbe6c759812b2.png)


![](../../assets/89ffbe6c759812b2.png)

And finally, rendered with raytracing, it costs 12.1 ms.

![](../../assets/c7df6905ba309d54.png)


![](../../assets/c7df6905ba309d54.png)

Since we are raytracing from the camera into the scene, calculating the transmission after each hit, we have the option to stop raytracing if the trasmission falls below a threshold. For the example below I stop when transmission becomes smaller than 0.05 for example, something that drops the cost to 9.58ms. The effectiveness of this tweak will vary a lot based on the scene of course.

![](../../assets/9ad9ba5e2c692d40.png)


![](../../assets/9ad9ba5e2c692d40.png)

Putting the cost aside for a moment to discuss memory, which was a big issue with the previous techniques. I discussed in a [previous post](https://interplayoflight.wordpress.com/2022/07/02/order-independent-transparency-part-2/) how MLAB requires 68MB of memory space for 4 nodes and a per pixel linked list requires 200MB for 8 nodes, targeting 1080p. We would have to multiply that number by 4 if we were targeting a 4K resolution. The raytracing acceleration structure for the above scene is 17.6 MB regardless of the rendering resolution.

Going back to the cost, which is quite significant in that scene. Visualising the bounding boxes of the meshes for Sponza in Nsight we can see how much overlap there is, due the batching of the meshes (red corresponds to 16x overlap).

![](../../assets/6b44a0fbac1fe827.png)


![](../../assets/6b44a0fbac1fe827.png)

This will slow down traversal of the acceleration structure. While inefficient mesh batching can negatively affect rasterisation based techniques as well, especially when it comes to culling, they are less sensitive to it than raytracing.

My content authoring skills are not enough to allow me to edit that scene to make it more raytracing friendly, so I used a simpler scene to investigate the effect of mesh batching.

Normal alpha blending at 0.52ms

![](../../assets/82d3d5029a7e87d2.png)


![](../../assets/82d3d5029a7e87d2.png)

Per pixel linked list at 1.23ms

![](../../assets/37b1f4d654276a54.png)


![](../../assets/37b1f4d654276a54.png)

MLAB at 1.56ms

![](../../assets/a5039b25636e404f.png)


![](../../assets/a5039b25636e404f.png)

Raytraced transparency at 1.97ms

![](../../assets/a017c99b148dd50b.png)


![](../../assets/a017c99b148dd50b.png)

The rendering cost is more comparable now. Also, the memory cost for MLAB and per pixel linked lists remain the same as above as it is linked to the rendering resolution while the acceleration structure cost is 14.9MB.

Visualising mesh axis aligned box (AABB) overlap heatmap in Nsight we notice how much less it is in this case, as each chess piece is its on BLAS instance without any mesh batching.

![](../../assets/7c05bcae17f1fedf.png)


![](../../assets/7c05bcae17f1fedf.png)

Also worth noticing is that this overlap varies quite a bit, depending on the view.

![](../../assets/acd7c9defdd7063b.png)


![](../../assets/acd7c9defdd7063b.png)

![](../../assets/7efffb8d49aab4d3.png)


![](../../assets/7efffb8d49aab4d3.png)

For a simple, “orbit”, Y axis-rotation around the scene, I noticed a variation in the raytracing cost between 1.4 to above 2ms, without effectively changing the transparent mesh coverage on screen. This is an interesting difference between this technique, where the rays originate from the camera, and say raytraced ambient occlusion where the traversal cost depends on the world position and not the camera location/direction (as long as the world position is in-view that is).

Another issue with raytraced transparency is that, assuming that you don’t raytrace opaque meshes from the camera’s point of view as well, there won’t be any interaction with the opaque geometry in the scene, something that rasterisation based OIT techniques can easily do with a depth test.

![](../../assets/a862e4c4d6254467.png)


![](../../assets/a862e4c4d6254467.png)

A solution to that would be to bind the depth buffer to the raygen shader, calculate the per pixel camera distance to the opaque surface, compare the hitpoint distance to that distance and stop the traversal when it becomes greater.

![](../../assets/6bab05a8e0612fcf.png)


![](../../assets/6bab05a8e0612fcf.png)

Since we are raytracing from the camera’s point of view, in contrast to other raytracing techniques like RTGI and RTAO, we can use frustum culling to only add camera visible transparent meshes to the TLAS.

There is another advantage of raytraced transparency to discuss. With any rasteration OIT technique (with normal alpha blending as well), refraction is a challenge. Refraction of other transparent surfaces is an even harder problem, impossible to solve efficiently for multiple layers of transparency.

Not so with raytraced transparency. All we have to do is calculate a refraction ratio and use the normal at the hitpoint to refract the ray direction. We can also account for rays entering and exiting transparent objects by checking the normal direction (relative to the ray) and inverting the refraction ratio.

```
float refractionRatio = 1 / 1.2; // assume entering from air to a "glassy" surface
if (dot(payload.normal, -ray.Direction) < 0.0f)
{
payload.normal = -payload.normal;
refractionRatio = rcp(refractionRatio );
}
ray.Origin = payload.position;
ray.Direction = normalize(refract(ray.Direction, payload.normal, refractionRatio ));
```

This allows for physically plausible refractions of the scene, of transparent objects as well (which refract other transparent objects themselves).

![](../../assets/23e1569e5a7105be.png)


![](../../assets/23e1569e5a7105be.png)

We talked about frustum culling transparent BLASes above to trim the TLAS to only camera visible content. Refraction of transparent meshes, which may well be off screen, may complicate this and we can choose to ignore them or inflate the frustum to include more transparencies.

We haven’t talked about the elephant in the room yet, and that is particles and how to handle them. It is possible to [add them to the acceleration structure](https://developer.nvidia.com/blog/best-practices-using-nvidia-rtx-ray-tracing/) and raytrace them, but while this can work ok in the context of raytraced reflections, raytraced trasmissive shadows etc that want a simple representation of a particle effect (more like of it’s “volume”), for main view particle raytracing that simple representation may not be enough. There is also the particle quad representation to be considered, there are a few options here: it could either be a BLAS per quad or recreate/update the BLAS per frame with the whole particle emitter, neither of which may be very appealing given the complexity of modern particle effects. There is also [mixing lower resolution particles](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-23-high-speed-screen-particles) with high resolution transparent surfaces while maintaining the correct sorting order but this is a problem that affects most raster based OIT techniques as well (apart from [Weight Blended OIT](https://jcgt.org/published/0002/02/09/paper.pdf) perhaps). I haven’t experimented with raytraced particle blending in this instance, whether it will be of reasonable cost to be feasible yet it remains to be seen.

As with all graphics techniques, whether raytraced transparency is suitable or not depends on your circumstances: target resolution, memory restrictions that make raster based OIT prohibitive, scene complexity. Particles, depending on their complexity, can also be a big issue with this technique. One can also argue that the set up expected for raytracing to perform well, i.e avoid mesh batching and AABB overlap are incompatible with the scenarios OIT is supposed to help with, bad batching, mesh overlap etc, where distance sorting can’t help as much.

In certain scenarios raytraced transparency can come quite close to rasterisation based OIT techniques at a fraction of the memory cost and at higher quality.

Raytraced transparency can solve long-standing and hard to solve issues in games that rasterised transparency can’t easily though, such as correct sorting and refraction, and the more capable the hardware becomes the more appealing it will appear.

Thank you for yet another detailed and useful analysis!

Do you know anything about how offline path tracers handle particle effects for movies?