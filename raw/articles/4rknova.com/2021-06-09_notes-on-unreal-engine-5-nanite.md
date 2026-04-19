---
title: Notes on Unreal Engine 5, Nanite
url: https://www.4rknova.com/blog/2021/06/09/unreal-5-nanite
author: Nikolaos Papadopoulos
published: '2021-06-09'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

This post is a collection of notes on the exciting new technology of Nanite in Unreal engine 5. The information was gathered from watching videos and reading articles on the tech both from the developers and third party sources.

# Nanite

Nanite is a virtual micropolygon geometry system introduced in Unreal engine 5.

The main characteristics of Nanite are:

- Only the geometry that can be seen is drawn for a given frame.
- Geometry virtualization means that only the data that is required to render a given frame is streamed into memory.
- Artists can author film quality assets that contain millions of triangles and add millions of instances in a scene without worrying about the rendering cost (i.e. polycount, draw calls, memory footprint).
- There is no need to bake fine grained detail of a model to normal maps.

The system follows a similar logic to that of a virtual texturing system where only texture data for what is rendered in the frame is stream into memory. This way the artists don’t have to worry about texture memory budgets and can use ultra high resolution textures.

# Valley of the Ancient demo

Epic showed an impressive demo to demostrate the new tech in Unreal engine 5.

Traditional terrain techniques rely on a height map to offset the geometry of a tesselated plane. When assets such as rocks intersect the terrain geometry, blending / feathering is used to eliminate hard edges and create a softer, more natural look.

The terrain in the Unreal demo follows a different approach. The surface is hand assembled using densely tesselated geometry assets from megascans. This allows for incredibly granular terrain with cliff overhangs that protrude horizontally and interesting relief detail which is impossible to achieve using heightmaps. This level of detail also applies in smaller scale geometry such as underground rocks sticking out of dirt.

# Occlusion culling

Nanite performs fine grained occlusion culling, which removes hidden geometry. Traditionally only objects that are entirely occluded would be culled, but with Nanite, if two assets are intersecting with each other, the occluded parts of their geometry are quite often culled, eliminating overdraw. The cost of rendering with Nanite scales with screen resolution no matter how high the polygon count is for the rendered geometry.

There are cases where the occlusion mechanism does not work well. The screenshot below shows a visualization of overdraw in the demo’s terrain using a heatmap. The bright orange / yellow areas is where there is a higher degree of overdraw.

![01](../../assets/538b48647b1492fd.png)


Brian Karis explains [2] that this is caused by surfaces that are really close to one another, which is something that is prevalent across this demo’s map. This issue is worse when there are lots of surface layers that are setup in that fashion. The development team observed that Nanite can be up to twice as expensive for content that is heavily stacked this way when compare with other content examples that they’ve previously tested. However, even with this heavy overdraw, they are able to hit 30Hz on XBox and PS5.

Occlusion culling in Nanite works by taking the bounds of pieces of geometry (i.e. clusters of triangles) and testing for visibility. When viewing geometry from a glazing angle, or from a distance, some patches of geometry appear flat, even if they are heavily detailed and stack on top of other layers, increasing overdraw. The screenshot below shows the overdraw heatmap when looking at the terrain from a glazing angle.

and below is another view from high up.

It’s worth mentioning that the demo map has areas where there are 10 layers of overlapping geometry.

# A deeper dive to the technology of Nanite

Nanite is designed to do for geometry what virtual texturing does for textures. That might sound conceptually trivial, however, this concept becomes much harder when it comes to geometry:

- Geometry virtualization is more than just a memory management challenge.
- Geometry detail directly impacts rendering cost.
- Geometry is not trivially filterable. It’s trivial to create a mip chain for a texture, but it’s not trivial to do the equivalent with geometry.

The purpose of Nanite was to replace the way meshes are managed in the graphics workflow without that affecting textures, materials, or related tooling.

# Pipeline

A traditional GPU pipeline is driven by a retained mode renderer. All the data for the scene exists in GPU memory with data being sparsely updated, and all vertex/index information is stored in a single large resource. Per view the GPU culls instances of geometry and the remaining triangles are rasterized. If only rendering depth, the entire scene can be drawn with a single indirect call.

In order to reduce the cost of rendering triangles that are not visible, Nanite groups the geometry into clusters of 128 triangles and calculates a bounding box for each cluster. Clusters can then be rejected using frustum and occlusion culling.

Visibility is decoupled from material and is calculated on a per pixel basis to avoid high costs associated with:

- Switching shaders during rasterization,
- Overdraw and evaluation of materials for hidden fragments
- Depth pre-pass (that would otherwise be necessary to avoid overdraw)
- Pixel quad inefficiencies from extremely dense meshes.

Nanite implements deferred materials using a visiblity buffer to separate material evaluation from rasterization of the geometry. A single draw call happens for each material that is present in the scene.

Each material pass writes to the GBuffer to integrate with the rest of the deferred shading renderer in Unreal engine 5. Brian Karis explains the the team’s long term ambition is to support the forward renderer as well.

All opaque geometry is rasterized once, without the need for a depth pre-pass.

# Geometry scaling

Nanite’s goal is to allow drawing huge number of instances of densely detailed geometry that contains millions of triangles per instance, This is practically impossible to achieve with a naive implementation where all the triangles of every geometry instance are resident in memory and are always rasterized in every frame.

Ideally we would not want to be drawing more triangles than pixels. Thinking of this in terms of triangle clusters, the goal is to draw the same number of clusters per frame regardless of how many objects are on screen or how dense they are. In reality, it’s impractical to be perfect with regards to that, but the general rule of thumb is that the cost of rendering geometry should scale with screen resolution and not scene complexity.

Nanite creates a binary tree of LODs for each cluster where the parent nodes in that hierarchy are simplified versions of the children nodes.

At runtime, on a per cluster basis, Nanite finds a cut of the tree containing the desired LOD to be rasterized, meaning different parts of the same mesh can be on different levels of details based on what is needed. This is done in a view dependent way based on the screen space projected error of the cluster. A parent node will be chosen instead of a child node if the difference if imperceptible for a given point of view.

![01](../../assets/5b59ae7c5c9df9da.png)


The above is all that is required for the virtualization part of the system as it’s not necessary to keep the entire LOD tree in memory for each cluster. Any cut of the tree can be used to mark the affected nodes as leaves and the remaining subtrees below those nodes can be discarded. Similarly to virtual texturing, data is streamed in and out depending of what is required to render the frame and what is already in memory.

In general pixel sized features require pixel sized triangles to represent them, without introducing visible error that would compromise the visual quality. Tiny triangles are generally not efficent for rendering with GPU rasterizers as they are designed to be highly parallellized in the number of pixels they process, not the number of triangles. The GPU rasterizer chokes on very small triangles as it’s unable to schedule them efficiently, hurting occupancy and ultimately performance [5].

Nanite implements a software rasterizer that performs 3 times faster on average, when compared to the fastest primitive shader implementation that they measured, even more so for pure micro polygon case, and a lot more when comparing with the old vertex / pixel shader path instead of primitive shaders.

The vast majority of triangles on screen are pixel sized. Those triangles are software rasterized (cyan in the image below), however, the remaining large triangles (red in the image below) are hardware rasterized as the hardware rasterizer can render those more efficiently. The decision of which rasterizer to use is made on a per cluster basis.

![01](../../assets/a95a5e8e35539d25.png)


# Performance

For a typical scenario of rendering to 2496x1404 and upsampling to 4K with Temporal Anti-Aliasing and Upscaling (TAAU):

- ~2.5ms to cull and rasterize all of the geometry with nearly 0 CPU time.
- ~2.0ms base pass to apply all the deferred materials with a small CPU cost and 1 draw call per material. This scales with the number of materials to be applied.

# Compression

Nanite uses a proprietary compression format to significantly reduce the amount of on-disk storage space that is required for its data.

# Limitations

Nanite does not currently support the following:

- Translucent or masked materials
- Non-rigid deformation, skeletal animation, etc.
- Tesselation and displacement
- Aggregates (eg. grass, leaves, hair)