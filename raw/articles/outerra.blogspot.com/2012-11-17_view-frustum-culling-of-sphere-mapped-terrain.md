---
title: View Frustum Culling of Sphere-mapped Terrain
url: https://outerra.blogspot.com/2012/11/view-frustum-culling-of-sphere-mapped.html
author: Outerra
published: '2012-11-17'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

View frustum culling is quite important part of any 3D engine, more so of engines focusing on a large scale terrain rendering. For objects we are using a variant of “p/n vertex” approach for culling object bounding boxes, represented as a center and a half-extent vector. The algorithm was described, for example, in the


The idea is to check the intersection of individual frustum planes with the axis-aligned box by computing the distance of the corner point of the box that is farthest “into” the plane. There’s an elegant way how to do that. Provided you have an axis-aligned box represented with a center and a half-extents of the box for x, y and z, you can compute the signed distance from the center to the plane (using dot with the plane normal). Plane normal points inside the frustum, so for the center points inside of it you get a positive distance, and a negative one otherwise.


The box corner that lies farthest into the plane (the one that we need to check against) is the one that would maximize the signed distance from the plane. We can get the distance by projecting the half-extents onto the plane normal and summing up the absolute values (or, since the extents are positive values, by taking the absolute values of plane normal components).



This method can be generalized to oriented bounding boxes by rotating the plane into the OBB space first.



The algorithm is of course applicable for culling a tiled terrain. For a plane-mapped terrain the situation would be much simpler. Certainly one would choose the terrain tiles to be axis-aligned from the start, avoiding the need for rotating the frustum planes into the oriented bounding-box space.


However, for spherical worlds it’s more complicated. Not only the tiles on sphere surface will be arbitrarily oriented, but because there’s no way to wrap a rectangular grid over a sphere seamlessly, the tiles will be also deformed.



You’ll notice that the individual tiles generally aren’t rectangular. The major deformation component is the shear. Upper-level tiles are more deformed in other, non-symmetric ways, but as we go lower we go in the quad-tree hierarchy, the shear becomes the dominant one.


We can wrap the tiles in oriented or even axis aligned bounding boxes. but in many cases it would be wasteful, leading to false positives.


But here’s an interesting thing. Since the shear is an affine transform, one can actually rotate the frustum planes directly into the skewed space and perform the culling test there normally.



This can be done by multiplying the rotation matrix by our shear matrix, and transforming the planes with the transpose of the inverse of the resulting matrix.


(Update: simplified the math)


The resulting rotation matrix can be simply made from normalized vectors of the skewed tile space itself, like this:



The following code tests whether a skewed box lies in the frustum:



The


Lastly, here’s a short video showing it in action on an extreme case of shear:



[Real-Time Rendering](http://www.realtimerendering.com/)book. Also, Fabian Giesen has a nice[comparison and evolution of view frustum culling methods](http://fgiesen.wordpress.com/2010/10/17/view-frustum-culling/)on his blog.The idea is to check the intersection of individual frustum planes with the axis-aligned box by computing the distance of the corner point of the box that is farthest “into” the plane. There’s an elegant way how to do that. Provided you have an axis-aligned box represented with a center and a half-extents of the box for x, y and z, you can compute the signed distance from the center to the plane (using dot with the plane normal). Plane normal points inside the frustum, so for the center points inside of it you get a positive distance, and a negative one otherwise.

The box corner that lies farthest into the plane (the one that we need to check against) is the one that would maximize the signed distance from the plane. We can get the distance by projecting the half-extents onto the plane normal and summing up the absolute values (or, since the extents are positive values, by taking the absolute values of plane normal components).

This method can be generalized to oriented bounding boxes by rotating the plane into the OBB space first.

### Culling terrain tiles

The algorithm is of course applicable for culling a tiled terrain. For a plane-mapped terrain the situation would be much simpler. Certainly one would choose the terrain tiles to be axis-aligned from the start, avoiding the need for rotating the frustum planes into the oriented bounding-box space.

However, for spherical worlds it’s more complicated. Not only the tiles on sphere surface will be arbitrarily oriented, but because there’s no way to wrap a rectangular grid over a sphere seamlessly, the tiles will be also deformed.

We can wrap the tiles in oriented or even axis aligned bounding boxes. but in many cases it would be wasteful, leading to false positives.

But here’s an interesting thing. Since the shear is an affine transform, one can actually rotate the frustum planes directly into the skewed space and perform the culling test there normally.

This can be done by multiplying the rotation matrix by our shear matrix, and transforming the planes with the transpose of the inverse of the resulting matrix.

(Update: simplified the math)

The resulting rotation matrix can be simply made from normalized vectors of the skewed tile space itself, like this:

The following code tests whether a skewed box lies in the frustum:

The

*npv = abs(R*plane)*can be precomputed, from a certain level of the quad-tree the*u*and*v*vectors of tiles don't change much, and thus the matrix R changes only marginally and*npv*can be cached and reused.Lastly, here’s a short video showing it in action on an extreme case of shear:

## 6 comments:

Nice! But what are plane,center and R types? vec3,vec3,mat3?





so if we have unnormalized frustum planes in world space(or viewer relative world space), tile center and u,v vectors in world space(or viewer relative world space), we can do the following:

vec4 planes[6]; // frustum ws

vec3 center,u,v,extents; // tile ws

mat3 R;

R[0] = u;

R[1] = v;

R[2] = normalize(cross(u,v));

// test:

for (int i = 0; i < 6; ++i) {

float d = dot(center, planes[i].xyz) + planes[i].w;

float3 npv = abs(R * planes[i]); // how to transform here ? wtb w component?

float r = dot(extents, npv);

if(d+r > 0) return ... // partially inside

if(d-r >= 0) return ... // fully inside

}

Quite confused :/ Could you clarify a lil bit, please? Thanks!

Oh, someone found it useful :)




plane is vec4 with plane normal (normalized) and distance. I forgot to add that our frustum is centered in the camera point, and thus all frustum planes except the far one go through it and hence the fourth component d=0. We aren't culling with the far plane. That means dot(box_center,plane_normal) gets us the distance from the center to the plane directly.

Now R*plane.xyz is a projection of plane normal into the uvn space, and dot with abs() of it and box half-extents (those are in uvn space) gets us the distance from the center to the farthest/nearest corner of the box from given plane.

Hope that helps, I'll add the missing info to the post.

Wow )


Thanks for quick reply!

Yeah, it's really usefull, i've got a lot of forest tiles to cull, and your solution is better than simple sphere test for that case :}

I`ll go try now...

Partially get it working, but still having false rejects. Frustum setup is same as yours (left,right,top,bottom,near planes go from origin, far plane - not used), plane normals - normalized.

I`m wondering if my R matrix is correct. code is as follows (OpenGL):

mat3 R; R[0] = u; R[1] = v; R[2] = cross(u,v);

R = inverse(R); // R is now transform from camera-relative world space to uvn space

Is it correct ?

R is made of u,v and n world-space vectors in rows, in glsl that would be


R = transpose(mat3(u,v,n))

Works correct now, thank you

Post a Comment