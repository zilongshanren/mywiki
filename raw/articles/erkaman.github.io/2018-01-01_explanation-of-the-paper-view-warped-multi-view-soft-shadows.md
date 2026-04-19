---
title: Explanation of the paper 'View-warped Multi-view Soft Shadows for Local Area
  Lights'
url: https://erkaman.github.io/posts/marrs2018.html
published: '2018-01-01'
source_blog: Eric Arnebäck
source_site: https://erkaman.github.io/
category: graphics
fetched: '2026-04-19'
---

**UPDATE:** after receiving a [small correction](https://twitter.com/acmarrs/status/1024729654068998150) from one of the authors of the paper, the
article has been corrected.

I will in this post write down an explanation of the intuition behind the paper
['View-warped Multi-view Soft Shadows for Local Area Lights'](http://www.jcgt.org/published/0007/03/01/).

The paper describes a real-time technique for soft shadows. Area-lights do not create a sharp shadow. Instead, they create a soft shadow, as can be seen in the image below.

The yellow object is an area-light that emits light, and the blue object is an occluder that occludes light.
The area-light casts a shadow on the flat plane below the occluder.
Points that are not at all visible from the area-light are in complete darkness,
which is called the *umbra*. Points which are partly visible from the
area-light are part of the penumbra. The penumbra gradually goes from
shadow to non-shadow, as is illustrated by the gradient in the bottom of the image.
If a point is not in the umbra or the penumbra, all points on the area-light are
visible from that point, and it is thus a non-shadowed point. On the other hand,
if only a subsection of the area-light is visible from the point,
then it will receive a certain amount of light from that subsection, and
will thus not be in complete darkness, and it will be in the penumbra. Finally, points that are
part of the umbra are completely hidden from the area-light, and thus
receive no light from it, and are black.
The below image illustrates soft-shadows, as implemented in a 3D rendering engine:

In order to implement soft shadows, we need to find a value in the range $[0,1]$ for each point on the plane. $1$ signifies that the point is not in shadow, $0$ means the point is in the umbra, and values in-between are part of the penumbra. Multi-view rasterization is a solution to the problem of rendering soft-shadows that provides good quality. The idea is simple: pick a number of arbitrary points on the area-light, and render shadow maps from these points, as illustrated below:

The red, green, and blue triangles illustrates shadow map frustums. Using these shadow maps, we can compute soft-shadows for every point on the plane. We loop through all the shadow maps, and check whether the point is visible from the shadow map frustum; this gives us a binary result, either a $0$ and $1$. Now, if we take the average of all these results, we get a soft shadow. This is because points that are visible from many shadow maps, like P1, will have a value that is close to 1 if we compute the average, which is exactly what we want. Furthermore, points like P0 that are in the umbra, will not be visible from a single shadow map, so P0 will get a value of 0. Finally, points like P2, that are near the umbra, will not be visible from very many shadow maps, and so it will get a value that is close to 0; again, exactly our desired outcome.

The main issue with MVR, is that we have to render a lot of shadow maps for good results. The paper presents an elegant solution to the problem: We convert our geometry into a point cloud, and reprojects these points into all of our shadow map frustums. First, we make a frustum that entirely contains the area light source, as is illustrated below.

As can be seen, the frustum entirely contains our yellow light source. We rasterize our geometry from the perspective of this frustum, and all geometry contained in the frustum will be rasterized into a fragment. Every rasterized fragment will give us a point, and we append that point to a buffer(for HLSL, a AppendStructuredBuffer). The below image illustrates the points we get from rasterizing a single triangle.

After rasterizing all geometry, we will have a huge buffer of points. We will create shadow maps from these points(and the shadow map frustums are just like in MVR, just positioned at arbitrary points on the area light). We execute a compute shader(the authors also tried using a pixel shader, but it was slower, so we won't discuss that alternative), that reprojects these points into the clip-space of one of the shadow maps. The reprojected point will map into one of the texels of the shadow map. If the depth value of the reprojected point is larger than the value already stored in the shadow map(or smaller, depending on your choice of convention), we will update the depth value stored in the shadow map. In practice, this has to be implemented using GPU atomic operations(InterlockedMax in HLSL). We create all of our shadow maps from the point cloud in this manner. We now use these shadow maps just like in MVR. So we average over the shadow maps, in order to compute a soft shadow.

One important implementation detail, is that we disable z-testing when rasterizing and creating the point cloud. See the below image

The points Q1 and Q0 both fall into the same texel. If z-testing is enabled, then the point Q1 would not be included in the point cloud. So it would not be visible in any of the reprojected shadow maps, which may lead to artifacts since Q1 is now unable to cast any shadows since it's not in the point cloud(see figure 4 of the original paper)

The huge advantage the technique described in the paper has over MVR, is that the geometry must only be rasterized once. All the triangle-setup and rasterization overhead is only paid for once, which makes this technique much faster than MVR. Also, the reprojection step can be executed using only a compute shader, which makes it possible to use it together with async compute. When some geometry-heavy task is executed, such as shadow map rendering, often not all GPU-cores are properly utilized. So we can use async compute to run our point cloud reprojection step at these times, so that all GPU-cores are properly utilized.