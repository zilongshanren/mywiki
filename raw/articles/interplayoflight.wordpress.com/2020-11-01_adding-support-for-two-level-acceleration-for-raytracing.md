---
title: Adding support for two-level acceleration for raytracing
url: https://interplayoflight.wordpress.com/2020/11/01/adding-support-for-two-level-acceleration-for-raytracing/
author: Kostas Anagnostou
published: '2020-11-01'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

In my (compute shader) [raytracing](https://interplayoflight.wordpress.com/2019/09/07/hybrid-screen-space-reflections/) [experiments](https://interplayoflight.wordpress.com/2018/09/04/hybrid-raytraced-shadows-part-2-performance-improvements/) so far I’ve been using a bounding volume hierarchy (BVH) of the whole scene to accelerate ray/box and ray/tri intersections. This is straightforward and easy to use and also allows for pre-baking of the scene BVH to avoid calculating it on load time.

This approach has at least 3 shortcomings though: first, as the (monolithic) BVH requires knowledge of the whole scene on bake, it makes it hard to update the scene while the camera moves around or to add/remove models to the scene due to gameplay reasons. Second, since the BVH stores bounding boxes/tris in world space, it makes it hard to raytrace animating models (without rebaking the BVH every frame, something very expensive). Last, the monolithic BVH stores every instance of the same model/mesh repeatedly, without being able to reuse it, potentially wasting large amounts of memory.

To improve this, I experimented with a two-level acceleration structure hierarchy, not unlike the one supported by raytracing APIs like [DXR](https://developer.nvidia.com/rtx/raytracing/dxr/DX12-Raytracing-tutorial-Part-1). The first step was to create a BVH tree for each unique model in the scene (Bottom Level Acceleration Structure – BLAS). It was trivial to repurpose the [Embree pipeline I am using](https://interplayoflight.wordpress.com/2020/07/21/using-embree-generated-bvh-trees-for-gpu-raytracing/) to support this. Each model’s BVH tree can be prebaked and loaded from disk if needed. A significant difference with the previous approach is that each BVH is built in **object **and not world space. Also, each model BVH tree is complete, i.e. it can be raytraced in isolation and return hit or no hit. All the unique BVH trees were stored in a single buffer, in the first instance, for convenience.

Next, I created as second BVH tree, processing the world space bounding boxes of each model instance in the scene (Top Level Acceleration Structure – TLAS). Each model instance points to the model BVH it corresponds to and also has an offset into the BLAS BVH tree buffer created above. Since the Embree pipeline I am using processes bounding boxes it was trivial to use it again for building the TLAS. There is also the option to rebuild the TLAS every frame, if needed, in cases scenes models animate.

A TLAS leaf node corresponds to a model instance in the scene and contains an offset to the single buffer with all the BVHs trees mentioned above and the model instance’s **world to object** matrix. I previously talked about how each model’s BVH is stored in object space to make it reusable. The issue with this is that, normally, we would have to transform it with a model instance’s object to world matrix to place it in the world and ray trace it correctly. That transformation would have to be performed, on-the-fly, while tracing each ray, on all processed bounding boxes and triangles which can be very expensive. So to avoid all those multiplications, instead of transforming the BVH into world space we transform the ray and origin into each model’s object space, only once per processed bottom level BVH, and perform BVH tracing there.

The following should help summarise and clarify the design of the system.

![](../../assets/52ff3f74e90a5fae.png)


![](../../assets/52ff3f74e90a5fae.png)

I next set up a programmer art scene to determine potential performance cost. The scene is made up of the sponza atrium and 100 model instances, 10 of which are unique (each colour signifies a unique model). I am also raytracing hard directional light shadows, one ray per pixel @ 1280×720 on my HD4000 laptop (on battery).

![](../../assets/cd030d58ee4fe3e1.png)


![](../../assets/cd030d58ee4fe3e1.png)

Now, that GPU is not the best hardware to profile raytracing on and numbers fluctuate quite a bit, but it seems that the TLAS/BLAS configuration costs around **31ms** on the GPU and **~1.2ms** on the CPU to rebuilt the TLAS. For comparison, the original, monolithic BVH approach costs around **30.5ms**, so the overhead on the GPU is not significant. The TLAS is built using the low quality setting, to keep the cost low. In all, raytracing the TLAS/BLAS configuration does not seem to add an overhead to raytracing.

While this approach is good, it is still not ideal that one has to load and store all unique model BVHs in a single buffer regardless of them being used or not, so I wondered if we could keep each model BVH as a unique resource (buffer) and access it in a unbounded SRV array. This would be ideal as we could bind to the shader only the BVHs for the required model instances and not for the whole level. This was a simple change as well, I created the unique BVHs/buffers and bound them to the shader and modified the TLAS generation phase to include the BVH SRV index, instead of a BVH buffer offset, in each leaf. In this case I am binding 10 unique BVH buffers to the shader.

Unfortunately the driver didn’t like the unbounded SRV array access with the shader optimisations flag on (very old GPU and drivers), so I had to switch them off to get it to work, so comparisons are not totally fair. At any rate, indexing the BVH SRVs during raytracing increased the cost for the shadow pass to ~42ms so it doesn’t sound like a viable option on this platform.

Supporting a TLAS/model BHV instances allows us to implement features not previously possible with the monolithic BVH, for example shadows from animating models.

The cost of raytracing shadows for the animated models is ~31ms and it costs ~1.2ms to regenerate the TLAS on the CPU.

Using a TLAS/BLAS structure is great for BVH reuse and raytracing animating meshes but controlling raytracing with a TLAS has an additional advantage: it allows us to control what models will get raytraced per pass by generating a different TLAS. As an example, I have a raytraced reflections pass in the the toy engine which is particularly expensive on the HD4000 for the above scene. I can still get some raytraced reflections though if I generate a new TLAS for that pass with only the models (spheres), excluding the background.

![](../../assets/77b681b7deb86208.png)


![](../../assets/77b681b7deb86208.png)

Having the option to specify what gets raytraced per pass can be useful for many effects such as raytraced AO, shadows and reflections. A nice example of this was presented in the Digital Dragons 2020 presentation on [Call of Duty: Modern Warfare local light shadows](https://www.activision.com/cdn/research/Raytraced_Shadows_in_Call_of_Duty_Modern_Warfare.pdf), in which they used a TLAS per light to restrict what will get raytraced for shadows.

To sum it up, the two level acceleration structure is good for reuse, reducing the memory requirements and controlling raytracing at no significant performance cost increase.

Very nice, thanks for sharing your results! I really like the idea of building multiple local TLAS trees.

How do you efficiently traverse two-level structure on a GPU?

It’s ok if bottom-level is just a mesh, but what about cases where you have custom primitives (eg, mesh, sphere, disk, etc.)? Do you combine top level hits based on the object they hit and then intersect each primitive separately with a different shader?

No all work is done in the same shader, first traversing the TLAS BVH and then each BLAS BVH. The shader is quite complex indeed. If the shaders finds a hit in the BLAS it stops else it goes out and tries the next TLAS node.