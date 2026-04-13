---
title: Using Embree generated BVH trees for GPU raytracing
url: https://interplayoflight.wordpress.com/2020/07/21/using-embree-generated-bvh-trees-for-gpu-raytracing/
author: Kostas Anagnostou
published: '2020-07-21'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Intel released it’s [Embree collection of raytracing kernels](https://github.com/embree/embree), with source, sometime ago and I recently had the opportunity to try and compare the included BVH generation library against my own implementation in terms of BVH tree quality. The quality of a scene’s BVH is critical for quick traversal during raytracing and typically a number of techniques, such as the Surface Area Heuristic one [I am currently using](https://interplayoflight.wordpress.com/2018/09/04/hybrid-raytraced-shadows-part-2-performance-improvements/), is applied during the tree generation to improve it.

It appears that Embree is tuned for CPU-side traversal and by default it produces wide BVH trees, such as BVHs with 4 or 8 children (BVH4 or BVH8) suitable for SIMD acceleration. Such trees are harder to use during a GPU-based traversal. It does provide a sample (bvh_builder) though that showcases how to generate a BVH with 2 children (BVH2) and this is the one I based the Embree integration on . I built the Embree libraries directly from source although Intel provides prebuilt versions if you prefer.

The process of integrating Embree to the toy engine was pretty straightforward, I pretty much followed the [bvh_builder tutorial](https://github.com/embree/embree/blob/master/tutorials/bvh_builder/bvh_builder_device.cpp), filling in vector of RTCBuildPrimitive elements with the primitives of the scene, creating a RTCDevice and building a tree of Embree BVH Nodes.

Each RTCBuildPrimitive primitive is described by a min/max bounds of the axis aligned bounding box, a primitive ID what points to the data of this primitive (which have to be stored externally) and a geometry ID that can be used to identify a mesh.

```
avector<RTCBuildPrimitive> prims;
RTCBuildPrimitive prim;
prim.lower_x = bbox.MinBounds.x;
prim.lower_y = bbox.MinBounds.y;
prim.lower_z = bbox.MinBounds.z;
prim.geomID = 0;
prim.upper_x = bbox.MaxBounds.x;
prim.upper_y = bbox.MaxBounds.y;
prim.upper_z = bbox.MaxBounds.z;
prim.primID = index;
prims.push_back(prim);
```

To create the BVH tree one needs to create a RTCBVH object, fill in a struct with appropriate arguments and call rtcBuildBVH to create the bvh.

```
RTCBVH bvh = rtcNewBVH(g_device);
/* settings for BVH build */
RTCBuildArguments arguments = rtcDefaultBuildArguments();
arguments.byteSize = sizeof(arguments);
arguments.buildFlags = RTC_BUILD_FLAG_NONE;
arguments.buildQuality = quality;
arguments.maxBranchingFactor = 2;
arguments.maxDepth = 1024;
arguments.sahBlockSize = 1;
arguments.minLeafSize = 1;
arguments.maxLeafSize = 1;
arguments.traversalCost = 1.0f;
arguments.intersectionCost = 1.0f;
arguments.bvh = bvh;
arguments.primitives = prims.data();
arguments.primitiveCount = prims.size();
arguments.primitiveArrayCapacity = prims.capacity();
arguments.createNode = InnerNode::create;
arguments.setNodeChildren = InnerNode::setChildren;
arguments.setNodeBounds = InnerNode::setBounds;
arguments.createLeaf = LeafNode::create;
arguments.splitPrimitive = splitPrimitive;
arguments.buildProgress = nullptr;
arguments.userPtr = nullptr;
Node* root = (Node*) rtcBuildBVH(&arguments);
```

A couple of things worth noting, maxBranchingFactor should be set to 2 to create a BVH with 2 children per node. Also a number of callbacks need to be passed that control creation of nodes. I based mine on the ones showcases in the bvh_builder tutorial with a small tweak: Embree’s BVH trees store the bounding boxes of the children in the parent node, while in my implementation I store each node with its bounding box. So I changed the setBounds callback to reflect that.

```
static void setBounds (void* nodePtr, const RTCBounds** bounds, unsigned int numChildren, void* userPtr)
{
assert(numChildren == 2);
((InnerNode*)nodePtr)->bounds = merge(*(const BBox3fa*)bounds[0], *(const BBox3fa*)bounds[1]);
}
```

I also tweaked the sah() member function of the InnerNode, that calculates the node cost for the Surface Area Heuristic, as well because of this.

```
float sah()
{
BBox3fa& bounds0 = children[0]->bounds;
BBox3fa& bounds1 = children[1]->bounds;
return 1.0f + (area(bounds0)*children[0]->sah() + area(bounds1)*children[1]->sah())/area(merge(bounds0,bounds1));
}
```

The buildQuality is another important argument as it determines the quality of the generated tree. Embree supports 3 levels ([more information about BVH generation](https://www.embree.org/papers/2014-Siggraph-Embree.pdf)):

- RTC_BUILD_QUALITY_LOW: fast generation, based on Morton codes, but lower quality, suggested for dynamic scenes
- RTC_BUILD_QUALITY_MEDIUM: Balanced generation time and tree quality, using binned SAH.
- RTC_BUILD_QUALITY_HIGH: Slower tree generation but highest tree quality, using SAH and spatial splits.

Actually there is a 4th mode supported, RTC_BUILD_QUALITY_REFIT, which can refit a BVH when only the vertex buffer (positions) changes. I didn’t evaluate this mode in this instance.

The BVH tree creation is invasive and alters the source primitive data, so the bvh_builder example allocates an extra vector and makes a copy of the data.

```
avector<RTCBuildPrimitive> prims;
prims.reserve(prims_i.size() + extraSpace);
prims.resize(prims_i.size());
/* we recreate the prims array here, as the builders modify this array */
for (size_t j=0; j<prims.size(); j++) prims[j] = prims_i[j];
```

**NB: **Pay attention to the **extraSpace **variable. The spatial splits SAH path of the High quality mode will attempt to store split primitives at the end of the prims vector, so we need to allocate some extra memory space for this (I doubled the size of the prim vector). **If you omit this step Embree will silently fall back to a Medium quality tree**. The same will happen if you omit the splitPrimitive() callback in the arguments above.

The part that [converts the BVH to the serialised form](https://interplayoflight.wordpress.com/2018/07/04/hybrid-raytraced-shadows-and-reflections/) to be used during GPU tracing remained exactly the same.

I then did some performance test to compare the library with my own, single-threaded, SAH BVH tree quality, using the Sponza scene. The tests took place on my old HD4000 laptop with an i7-4510U@2GHz CPU running on battery.

![](../../assets/0c191c6ea692b99d.png)


![](../../assets/0c191c6ea692b99d.png)

In terms of BVH generation time, Embree beats my Reference implementation, at all quality levels, by a wide margin especially at lower quality levels. This is expected as BVH generation with Embree is multithreaded.

![](../../assets/907f09063830257e.png)

In terms of the memory required to store the GPU BVH tree buffer, all methods are similar, with the high quality Embree mode taking up some more.

![](../../assets/509fa65fe254a611.png)

Finally the raytracing cost for the Sponza scene, Embree performs really well, surpassing my Reference implementation in all quality modes, with especially great results at High.

![](../../assets/70f98de64fb02c55.png)

I repeated the test with a more complicated scene, comprised of a number of trees (I didn’t use alpha testing in this instance). This scene has smaller and more uniform triangles and is also more dense with more opportunities for bounding box overlap.

![](../../assets/541894073e8390a2.png)


![](../../assets/541894073e8390a2.png)

The BVH generation test returned some interesting results, the High quality Embree mode is now slightly slower than my Reference implementation. It is maybe the case that the Spatial-Split SAH BVH algorithm does not cope well with that particular scene.

![](../../assets/bd154788a4f69288.png)

No surprises from the memory requirements test, the High quality mode occupies slightly more space than the other modes.

![](../../assets/62ed35aa99d5d6de.png)

The Raytracing cost test returned another set of interesting results. This time around my Reference implementation is faster than the Low quality Embree tree and much closer to the Medium and High modes.

![](../../assets/53dd1f1e3e069f10.png)

In overall the Embree library produced high quality BVH trees, with fast generation times, which speed up traversal significantly (depending on the scene) and has become part of my toy engine from now on.

[…] Using Embree generated BVH trees for GPU raytracing […]