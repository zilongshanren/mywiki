---
title: 'GPU path tracing tutorial 3: GPU-friendly Acceleration Structures. Now you''re
  cooking with GAS!'
url: http://raytracey.blogspot.com/2016/01/gpu-path-tracing-tutorial-3-take-your.html
author: Sam Lapere
published: '2016-01-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

(In case you were wondering, my pun-loving girlfriend came up with the title for this post). This tutorial is the longest, but most crucial one so far and deals with the implementation ray tracing acceleration structure that can be traversed on the GPU. The code from the previous tutorial works okay for simple triangle meshes with less then 10,000 triangles, but since render times grow linearly or O(n)with the complexity of the scene (each ray needs to test every primitive in the scene for intersection), anything above that number becomes unfeasible. To address this issue, ray tracing researchers came up with several acceleration structures such as grids, octrees, binary space partitioning trees (BSP trees), kd-trees and BVHs (bounding volume hierarchy), allowing render times to scale logarithmically or O(log n) instead of linearly with scene complexity, a huge improvement in speed and efficiency. Acceleration structures are by far the most important ingredient to building a fast ray tracer and an enormous amount of research has gone into improving and refining the algorithms to build and traverse them, both on the CPU on the GPU (the latter since 2006, around the same time unified shader architecture was introduced on GPUs).

Scratch-a-Pixel (again) has a great introduction to acceleration structures for ray tracing (grids and bounding volume hierarchies) that includes example code:


An overview of the latest state-of-the-art research in acceleration structures for GPUs can be found in this blogpost on Robbin Marcus' blog:

[http://www.scratchapixel.com/lessons/advanced-rendering/introduction-acceleration-structure](http://www.scratchapixel.com/lessons/advanced-rendering/introduction-acceleration-structure). Peter Shirley's "Realistic Ray Tracing" book also contains a good description and implementation of a BVH with C++ code.An overview of the latest state-of-the-art research in acceleration structures for GPUs can be found in this blogpost on Robbin Marcus' blog:

[http://robbinmarcus.blogspot.co.nz/2015/10/real-time-raytracing-part-2.html](http://robbinmarcus.blogspot.co.nz/2015/10/real-time-raytracing-part-2.html)
This tutorial focuses on the implementation of a BVH acceleration structure on the GPU, and comes with complete annotated source code for BVH construction (on the CPU) and BVH traversal (on the GPU using CUDA). The reason for choosing a BVH over a grid or kd-tree is because BVHs map better to modern GPU architectures and have also been shown to be the acceleration structure which allows the fastest build and render times (see for example

[https://anteru.net/research/quantitative-analysis-of-voxel-raytracing-acceleration-structures/](https://anteru.net/research/quantitative-analysis-of-voxel-raytracing-acceleration-structures/)). Another reason for choosing BVHs is that they are conceptually simple and easy to implement. The Nvidia research paper "[Understanding the efficiency of ray traversal on GPUs](https://code.google.com/p/understanding-the-efficiency-of-ray-traversal-on-gpus/)" by Aila and Laine comes with open source code that contains a highly optimised BVH for CUDA path tracers which was used in Cycles, Blender's GPU path tracing renderer ([http://wiki.blender.org/index.php/Dev:Source/Render/Cycles/BVH](http://wiki.blender.org/index.php/Dev:Source/Render/Cycles/BVH)).
The code in this tutorial is based on a real-time CUDA ray tracer developed by Thanassis Tsiodras, which can be found on


For the purpose of clarity and to keep the code concise (as there's quite a lot of code required for BVH construction), I removed quite a few nice features from Thanassis' code which are not essential for this tutorial, such as multithreaded BVH building on the CPU (using SSE intrinsics), various render modes (like point rendering), backface culling, a scheme to divide the image in rendertiles in Morton order (along a space filling Z-curve) and some clever workarounds to deal with CUDA's limitations such as separate templated kernels for shadow rays and ambient occlusion.

[http://users.softlab.ntua.gr/~ttsiod/cudarenderer-BVH.html](http://users.softlab.ntua.gr/~ttsiod/cudarenderer-BVH.html)and which I converted to support path tracing instead. The BVH from this renderer is already quite fast and relatively easy to understand.For the purpose of clarity and to keep the code concise (as there's quite a lot of code required for BVH construction), I removed quite a few nice features from Thanassis' code which are not essential for this tutorial, such as multithreaded BVH building on the CPU (using SSE intrinsics), various render modes (like point rendering), backface culling, a scheme to divide the image in rendertiles in Morton order (along a space filling Z-curve) and some clever workarounds to deal with CUDA's limitations such as separate templated kernels for shadow rays and ambient occlusion.

One of the more tricky parts of implementing a BVH for ray tracing on the GPU is how to store the BVH structure and BVH node data in a GPU friendly format. CPU ray tracers store a BVH as a hierarchical structure starting with the root node, which contains pointers to its child nodes (in case of an inner node) or pointers to triangles (in case of a leaf node). Since a BVH is built recursively, the child nodes in turn contain pointers to their own child nodes and this keeps on going until the leaf nodes are reached. This process involves lots of pointers which might point to scattered locations in memory, a scenario which is not ideal for the GPU. GPUs like coherent, memory aligned datastructures such as indexable arrays that avoid the use of too many pointers. In this tutorial, the BVH data (such as nodes, triangle data, triangle indices, precomputed intersection data) are therefore stored in flat one-dimensonal arrays (storing elements in depth first order by recursively traversing the BVH), which can be easily digested by CUDA and are stored on the GPU in either global memory or texture memory in the form of CUDA textures (hardware cached). The BVH in this tutorial is using CUDA texture memory, since global memory on older GPUs is not cached (as opposed to texture memory). Since the introduction of Fermi however, global memory is also cached and the performance difference when using one or the other is hardly noticeable.

In order to avoid wasting time by rebuilding the BVH every time the program is run, the BVH is built only once and stored in a file. For this to work, the BVH data is converted to a cache-friendly format which takes up as little memory space as possible (but the compactness of the data makes it also harder to read). A clever scheme is used to store BVH leaf nodes and inner nodes using the same data structure: instead of using a separate struct for leaf nodes and inner nodes, both types of nodes occupy the same memory space (using a union), which stores either two child indices to the left and right child when dealing with an inner node or a start index into the list of triangles and a triangle count in case of a leaf node. To distinguish between a leaf node and an inner node, the highest bit of the triangle count variable is set to 1 for a leaf node. The renderer can then determine at runtime if it has intersected an inner node or a leaf node by checking the highest bit (with a bitwise AND operation).

A lot of the triangle intersection data (such as triangle edges, barycentric coordinates, dot products between vertices and edge planes) is precomputed at the scene initialisation stage and stored. Since modern GPUs have much more raw compute power than memory bandwidth, it would be interesting to know whether fetching the precomputed data from memory is faster or slower compared to computing that data directly on the GPU.

-

["](http://www.sci.utah.edu/~wald/Publications/2007/ParallelBVHBuild/fastbuild.pdf)by Ingo Wald, 2007. This paper is a must read in order to understand what the code is doing.

**On fast construction of SAH based Bounding Volume Hierarchies**"- "

[" by Wald, Boulos and Shirley, 2007](http://www.cs.cmu.edu/afs/cs/academic/class/15869-f11/www/readings/wald07_packetbvh.pdf)

**Ray tracing deformable scenes using dynamic Bounding Volume Hierarchies**-

["](http://dcgi.felk.cvut.cz/home/havran/ARTICLES/ingo06rtKdtree.pdf)by Wald and Havran, 2006

**On building fast kd-trees for ray tracing, and on doing that in O(N log N)**"**Overview of algorithm for building the BVH on the CPU**



- the main() function (in main.cpp) calls prepCUDAscene(), which in turn calls UpdateBoundingVolumeHierarchy()

- UpdateBoundingVolumeHierarchy() checks if there is already a BVH for the scene stored (cached) in a file and loads that one or builds a new BVH by calling CreateBVH()

- CreateBVH():

- computes a bbox (bounding box) for every triangle and calculate the bounds (top and bottom)
- initialises a "working list" bbox to contain all the triangle bboxes
- expands the bounds of the working list bbox so it encompasses all triangles in the scene by looping over all the triangle bboxes
- computes each triangle bbox centre and adds the triangle bbox to the working list
- passes the working list to Recurse(), which builds the BVH tree structure
- returns the BVH root node

Recurse() recursively builds the BVH tree from top (rootnode) to bottom using binning, finding optimal split planes for each depth. It divides the work bounding box into a number of equally sized "bins" along each axis, chooses the axis and splitting plane resulting in the least cost (determined by the surface area heuristic or SAH: the larger the surface area of a bounding box, the costlier it is to raytrace) and finding the bbox with the minimum surface area:

- Check if the working list contains less then 4 elements (triangle bboxes) in which case create a leaf node and push each triangle to a triangle list
- Create an inner node if the working list contains 4 or more elements
- Divide node further into smaller nodes
- Start by finding the working list bounds (top and bottom)
- Loop over all bboxes in current working list, expanding/growing the working list bbox
- find surface area of bounding box by multiplying the dimensions of the working list's bounding box
- The current bbox has a cost C of N (number of triangles) * SA (Surface Area) or C = N * SA
- Loop over all three axises (X, Y, Z) to find best splitting plane using "binning"
- Binning: try splitting the current axis at a uniform distance (equidistantly spaced planes) in "bins" of size "step" that gets smaller the deeper we go: size of "sampling grid": 1024 (depth 0), 512 (depth 1), etc
- For each bin (equally spaced bins of size "step"), initialise a left and right bounding box
- For each test split (or bin), allocate all triangles in the current work list based on their bbox centers (this is a fast O(N) pass, no triangle sorting needed): if the center of the triangle bbox is smaller than the test split value, put the triangle in the left bbox, otherwise put the triangle in the right bbox. Count the number of triangles in the left and right bboxes.
- Now use the Surface Area Heuristic to see if this split has a better "cost": calculate the surface area of the left and right bbox and calculate the total cost by multiplying the surface area of the left and right bbox by the number of triangles in each. Keep track of cheapest split found so far.
- At the end of this loop (which runs for every "bin" or "sample location"), we should have the best splitting plane, best splitting axis and bboxes with minimal traversal cost
- If we found no split to improve the cost, create a BVH leaf, otherwise create a BVH inner node with L and R child nodes. Split with the optimal value we found above.
- After selection of the best split plane, distribute each of the triangles into the left or right child nodes based on their bbox center
- Recursively build the left and right child nodes (repeat steps 1 - 16)
- When all recursive function calls have finished, the end result of Recurse() is to return the root node of the BVH

Once the BVH has been created, we can copy its data into a memory saving, cache-friendly format (CacheFriendlyBVHNode occupies exactly 32 bytes, i.e. a cache-line) by calling CreateCFBVH(). which recursively counts the triangles and bounding boxes and stores them in depth first order in one-dimensional arrays by calling PopulateCacheFriendlyBVH().

The data of the cache friendly BVH is copied to the GPU in CUDA global memory by prepCUDAscene() (using the cudaMalloc() and cudaMemcpy() functions). Once the data is in global memory it's ready to be used by the renderer, but the code is taking it one step further and binds the BVH data to CUDA textures for performance reasons (texture memory is cached, although global memory is also cached since Fermi). The texture binding is done by cudarender() (in cuda_pathtracer.cu) which calls cudaBindTexture(). After this stage, all scene data is now ready to be rendered (rays traversing the BVH and intersecting triangles).

**Overview of algorithm for traversing the BVH on the GPU**



- after cudarenderer() has bound the data to CUDA textures with cudaBindTexture() the first time it's being called, it launches the CoreLoopPathTracingKernel() which runs in parallel over all pixels to render a frame.

- CoreLoopPathTracingKernel() computes a primary ray starting from the interactive camera view (which can differ each frame) and calls path_trace() to calculate the ray bounces

- path_trace() first tests all spheres in the scene for intersection and then tests if the ray intersects any triangles by calling BVH_IntersectTriangles() which traverses the BVH.

- BVH_IntersectTriangles():

- initialise a stack to keep track of all the nodes the ray has traversed
- while the stack is not empty, pop a BVH node from the stack and decrement the stack index
- fetch the data associated with this node (indices to left and right child nodes for inner nodes or start index in triangle list + triangle count for leaf nodes)
- determine if the node is a leaf node or triangle node by examining the highest bit of the count variable
- if inner node, test ray for intersection with AABB (axis aligned bounding box) of node --> if intersection, push left and right child node indices on the stack, and go back to step 2 (pop next node from the stack)
- if leaf node, loop over all the triangles in the node (determined by the start index in the list of triangle indices and the triangle count),
- for each triangle in the node, fetch the index, center, normal and precomputed intersection data and check for intersection with the ray
- if ray intersects triangle, keep track of the closest hit
- recursively traverse the left and right child nodes, if any (repeat steps 2 - 9)
- after all recursive calls have finished, the end result returned by the function is a bool based on the index of the closest hit triangle (true if index is not -1)

- after the ray has been tested for intersection with the scene, compute the colour of the ray by multiplying with the colour of the intersected object, calculate the direction of the next ray in the path according to the material BRDF and accumulate the colours of the subsequent path segments (see GPU path tracing tutorial 1).

In addition to the BVH, I added an interactive camera based on the interactive CUDA path tracer code from Yining Karl Li and Peter Kutz (

[https://github.com/peterkutz/GPUPathTracer](https://github.com/peterkutz/GPUPathTracer)). The camera's view direction and position can be changed interactively with mouse and keyboard (a new orthornormal basis for the camera is computed each frame). The camera produces an antialiased image by jittering the primary ray directions. By allowing primary rays to start randomly on a simulated disk shaped lens instead of from a point. a camera aperture (the opening in the diaphragm) with focal plane can be simulated, providing a cool, photographic depth-of-field effect. The focal distance can also be adjusted interactively.
The material system for this tutorial allows five basic materials: ideal diffuse, ideal specular, ideal refractive, Phong metal (based on code from Peter Shirley's "Realistic Ray Tracing" book) with a hardcoded exponent and a coat (acrylic) material (based on Karl Li and Peter Kutz' CUDA path tracer).





The source code for this tutorial can be found at




As in the previous tutorials, I aimed to keep the code as simple and clear as possible and added plenty of comments throughout (in addition to the original comments). If some steps still aren't clear, let me know. Detailed compilation instructions for Windows and Visual Studio are in the readme file:







All scene elements in this executable are hardcoded. Changing the scene objects, materials and lights is only possible by directly editing and re-compiling the source code.

**CUDA/C++ source code**The source code for this tutorial can be found at

[https://github.com/straaljager/GPU-path-tracing-tutorial-3/](https://github.com/straaljager/GPU-path-tracing-tutorial-3/)As in the previous tutorials, I aimed to keep the code as simple and clear as possible and added plenty of comments throughout (in addition to the original comments). If some steps still aren't clear, let me know. Detailed compilation instructions for Windows and Visual Studio are in the readme file:

[https://github.com/straaljager/GPU-path-tracing-tutorial-3/blob/master/README.md](https://github.com/straaljager/GPU-path-tracing-tutorial-3/blob/master/README.md)**Download executable (Windows only)**[https://github.com/straaljager/GPU-path-tracing-tutorial-3/releases](https://github.com/straaljager/GPU-path-tracing-tutorial-3/releases)All scene elements in this executable are hardcoded. Changing the scene objects, materials and lights is only possible by directly editing and re-compiling the source code.

**Screenshots**

Screenshots produced with the code from this tutorial (Stanford Dragon and Happy Buddha .ply models from the

[Stanford 3D scanning repository](http://graphics.stanford.edu/data/3Dscanrep/))
Glossy Stanford dragon model (871,000 triangles)

Happy Buddha model (1,088,000 triangles) with Phong metal material

The next tutorial will add even more speed: I'll dive deeper into the highly optimised BVH acceleration structure for GPU traversal from Aila and Laine, which uses spatial splitting to build higher quality (and faster) trees. It's also the framework that the GPU part of Blender Cycles is using.

Other features for upcoming tutorials are support for textures, sun and sky lighting, environment lighting, more general and accurate materials using Fresnel, area light support, direct light sampling and multiple importance sampling.

References

- "Realistic Ray Tracing" by P. Shirley

## 57 comments:

Great post, I appreciate the writeup of the acceleration structure. I'm wondering though, you use a stack for every ray traversal to store the state. Do you have a fixed size for this stack, or calculate it dynamically based on the maximal tree depth?


I found it very troubling to decide stack size wrt performance. I'm currently looking into stackless methods, but can't find any performance worthy ones without having to switch to voxelization methods completely.

Thanks Robbin. The code uses a fixed stack size per ray of depth 32. It works fine for models of up to 1 million triangles. I haven't really looked into optimising the performance of the BVH from this tutorial as I'm switching to Aila/Laine's BVH traversal code for the next tutorial which is already highly optimised (but the BVH construction algorithm is also more involved which is why I opted for a simpler BVH for this tutorial).


I'm also exploring a novel kind of acceleration structure which doesn't require a stack and has some other very nice properties which are ideally suited to massively parallel processors with limited memory bandwidth like GPUs. It's different from the usual suspects like grid/octree/kd-tree/BVH and is very outside-the-box thinking. But that's for a future post.

Hi Sam, I've been a long time reader of your blog and followed all your GPU path tracing developments with great interest.

Since I've started my own Blog about high-performance CPU path tracing just a few days ago, I hope you don't mind a little advertising :)

The first post features new state-of-the-art batch and packet traversal algorithms for CPUs, potentially useful also for GPUs.

Really nice post,

Sam! :)I'm also very curious about that future post about the

"outside-the-box-thinking-novel-acceleration-structure"! ;)What's the official name for that data structure? :P

Hi Valentin, perhaps I should start selling advertising space for other blogs :) The speedup (for primary ray packets) reported in your paper sounds impressive. You could link a bunch of computers with beefy CPUs together and do coherent path tracing in parallel (graphics.ucsd.edu/~iman/coherent_path_tracing.php, applying ray packet traversal for secondary rays by forcing them to be coherent using the same random number sequence for all pixels in a sample) so you can effectively do real-time path tracing.

@ xico2kx: Thanks! No official name for that data structure yet. I think it should have 'quantum' in its name as it can serve as multiple representations of the scene at once (similar like a sparse voxel octree, but more advanced), but also has other properties that are even more interesting and solve some long standing problems in ray tracing. I'll explain it in more detail later when the construction algorithm is more optimised.

Great tutorial! Don't forget that "Megakernels Considered Harmful" :)

Thanks Irakli. I'll talk about that paper in another tutorial about code optimisation. For now the megakernel concept is simpler to understand. Btw, Takahiro Harada's presentation on OpenCL path tracing (http://www.slideshare.net/takahiroharada/introduction-to-monte-carlo-ray-tracing-opencl-implementation-cedec-2014) also provides some insight into the issues of megakernels and how to implement kernel splitting in OpenCL.

Sam, many thanks for your tutorial, it is an invaluable resource for understanding


how path tracing on GPUs works.

But I have one question: is it possible that you forgot

this time in the main cuda kernel (CoreLoopPathTracingKernel)

to divide the accumulated color through the number of samples?

I think this causes the effect that by increasing the number of samples to 4 or 8 the rendered image gets much brighter.

Hi Christian: glad the tutorial is useful to you. You are right indeed, the radiance returned should be divided by the number of samples. It's fixed now (line 728 in cuda_pathtracer.cu). Thanks a lot!

Hey Sam can you explaine the pros and cons of Acceleration Structures





that are used in current realtime applications ?

It seems like distance fields and voxels are most promising.

DFAO is used in a bunc of art/tech demos.

https://vimeo.com/152968508

VXAO is rumored to be in the PC Version of the new Tomb Raider game.

http://wccftech.com/nvidias-vxao-to-be-featured-in-rise-of-the-tomb-raider-heres-what-we-know/

And i found this :

http://graphics.cs.aueb.gr/graphics/research_illumination.html

Might add to this topic if you havent already seen it.

Thanks for the links. I haven't tried voxels or distance fields, so I can't such much about their pros and cons other than what I've read. There was a rumour that Unreal Engine dropped voxel GI because it eats too much memory, but that could be alleviated to some extent by using cascaded voxel cone tracing. Supporting dynamic objects also requires real-time rebuilds of the voxel grids, and I haven't seen any voxel GI demos that included lots of dynamic deforming characters. For example Nvidia's moon landing scene to show off VXGI was completely static. Cryengine has voxel GI as well, but I've only seen it used in walkthroughs of static architectural scenes. This page describes the limitations of their voxel based GI in detail: http://docs.cryengine.com/display/SDKDOC2/Voxel-Based+Global+Illumination


As for distance field GI, I only know of Unreal Engine currently using/developing that. I beleive it has similar limitations as voxels when it comes to dynamic scenes (the distance fields are too expensive to be recomputed on the fly) and it's only used for far away scene objects, because the distance field is only an approximation of the scene geometry. There's more details here: https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/DistanceFieldAmbientOcclusion/index.html

Hi Sam. Nice article!



btw VXGI "revoxelizes the whole scene geometry every frame".

https://www.youtube.com/watch?v=F9nNLJ5OtY8

Really cool demo, like light emitting calamares. That's the most promising demo of VXGI I've seen so far, might give it a try myself.

What really is in demand is differential/cascode Emitter Coupled Logic multi-core RISC processor {no graphics core at all, video DAC soldered onto motherboard; cache, multi-threading & ILP tricks must all be eliminated} with one large {>>16GB} ECL SRAM module, so that game developers could easily create appropriate applications without operating system, graphics driver, API, and users could run them that way, thus taking advantage of 100% processing power. In fine, extreme performance guaranteed.

Im just leaving this here :





Some thoughts from an Intel Hardware Engineer on raytracing hardware.

https://www.linkedin.com/pulse/ray-tracing-hardware-ever-replace-rasterization-based-abhishek-nair?articleId=6096355072839540736#comments-6096355072839540736&trk=prof-post

From the european association for computer graphics :

http://diglib.eg.org/handle/10.2312/hpg.20141091.029-040

They simulated a raytracing hardware integration on an AMD R9 290X.

As a result the precision for ray traversal was vastly reduced.

(1bit in one case)

In the end they pulled 3,4 billion rays per second out of that gpu.

250-nanometres FET CMOS Pentium II — 333 MHz



1-micron Bipolar ECL CPU — 335 MHz

???

CPFUUU: thanks for the links, interesting read, especially the reduced precision ray tracing hardware. 3.4 billion rays per second would yield about 24 samples per pixel (4 rays per path on average) when rendering at 30 fps and 720p. That would look very decent in outdoor/well lit scenes.

Jenson - We'll have optical computing long before anyone starts resorting to ECL (too much power draw and too expensive) to break the drag on Moore's law.


CPFUUU and Sam: It's important to understand that is a simulated value. If you've been into all the previous whitepapers on pathtracing you'll know simulated results and actual results are two different animals :D

Brian. For instance, at 3.5 GHz, CMOS is 7 times power hungrier than ECL.

Jenson - I've seen your arguments for ECL many times here over the years, if you really want to convince people that we can get some order-of-magnitude greater performance from ECL without any of the downsides that caused us to use CMOS decades ago, then you have to post sources to your claims. I can't find a single research paper or article stating that ECL is superior. I can't find anything on modern ECL CPUs.

Brian: good point regarding the simulated numbers, I forgot about that. So realistically speaking, I guess the peak performance should about 1/3 to 1/2 that number. If it's really as easy to add ray tracing acceleration hardware to GPUs as the paper claims, it could be an interesting short-term strategy for AMD to leapfrog Nvidia in GPU ray tracing performance.

I remembered that commentary from John Carmack in 2013 :



"I am 90% sure that the eventual path to integration of ray tracing hardware into consumer devices will be as minor tweaks to the existing GPU microarchitectures."

In my opinion the paper shows what he might have had in mind.

Another reason to be optimistic is the fact that the R9 290X will soon be

a very outdated piece of hardware. Maxed out Polaris (14nm) would pack

3x the tflop performance and bandwith (HBM2). The first gen will be out in mid 2016.

According to roadmaps 10nm will be again twice as fast and available in 2018-2019.

Would be a good node for new consoles and entry point for more raytracing friendly

hardware. Its the only road to boost game graphics and reduce dev work loads.

Indeed, 2016 should be an interesting year for GPU architectures, finally freed from the shackles of 28 nm technology (which has been the main manufacturing process since 2012).

Brian, then take a look at some ONSemi papers about.




Actually, at 1-micron node, ECL CPU has approx. 6 times higher clock speed compared to CMOS CPU.

What's more, at least, Intel's current/roadmapped nodes are essentially false & eventually the '3-nm FinFET' will turn out to be real 10-nm gate length which is the best that can be done.

SiGe HBT differential/cascode Emitter Coupled Logic pure CISC single-core APU with one very large ECL SRAM module. Cache, multi-threading & ILP tricks must all be eliminated. A graphics designer could write own graphics driver directly in machine code at that working with the hardware on the lowest-possible level.

Going to be a great year for pathtracing! HBM is big. 14/16nm is big. Mixed-precision can be big if we can figure out creative ways to use it. Don't forget about interconnect! NVLink is big (in a multi-gpu setup we easily lose 10ms per frame to transfer overhead).


On top of that we'll get to see Knight's Landing with AVX512 and a plethora of cores as an actual host CPU, which can be big if you've got the CPU involved at all.

Will that Polaris (14nm) support true SSAA 1024X at least for ten-year-old games ?

Chris, there's some interesting things you can do with mixed precision. Not sure about Knight's Landing, the $4000 price of these cards positions them in the Nvidia Tesla GPU range, which excludes them from mainstream use. Unless Intel comes up with an affordable, mass market Xeon Phi add-on card (which is what Larrabee was supposed to be), I'm not going to bother.

You're right, they won't be mass market, they will likely stay in workstations where the really expensive Xeon processors currently are. I just mean in terms of pushing the bleeding edge of realtime pathtracing. A 72-core 512-wide

hostprocessor (not the co-processor version) is a compelling place to build your BVH as a direct drop-in to replace your 4-8 core.Many GPUs provide hardware support for H.265. However, the video will get high definition solely as soon as it is not at all compressed. Video will not look naturally 3D and simply real until it is recorded digitally at a rate in excess of 200 frames per second. 48-bit Deep Colour is just another thing that may improve the quality.


Meanwhile, real world lighting does require yet lot faster hardware than path tracing does. That vastly contrasts with, say, facial animation which highly relies on software improvement.

Man these Intel Knights require a lot of coin for their performance.





I think only NV or AMD have the conditions to develop proper hardware.

You can already estimate a somewhat realistic entry point for path tracing.

A highend 250W 10nm gpu could reach 30 tflop, that would be some horsepower.

We can hope for more raytracing friendly hardware because they will need it

for gi solutions in rasterizer engines.

I dont think that pt will be used for aaa games at first. It is much more likely

that indie devs try it out. But only if the raytracing community could deliver

a usefull pt engine for free. Small teams could experiment with the technology

and achieve amazing graphics. Something with limited dynamic geometry and

open environment. A rally racer or some survival game for example.

Enthusiast with multi gpu setups in the 100 tflop area would upload their

letsplays on youtube and make the technology more popular.

Seemingly, path tracing development will continue stalling as long as the developers ignore machine code.



Independent game developers have much freedom for extreme optimization on AMD GPUs & probably Intel CPUs. Though, they more prefer releasing such pieces as 'Caffeine' instead.

The ECL APU with ECL SRAM, although the fastest computer hardware ever invented by a human, must be strictly correlated with the room temperature, which is almost +20.761°C, whilst operating at its highest performance level with no cooling system. For aught I know SiGe HBT is currently the most perfect element for VLSI.

@CPFUUU - We'll get there. For the past 2 years I've been working on a realtime pathtracer that I am releasing for Unity and Unreal Engine, in 1-2 months. I just recently broke 1B rays/s on a variety of scenes with the traversal scheme (no shading, nearest intersection) on a gtx 680, so it will be very competitive. Supports fully dynamic geometry and all platforms/backends: multi-gpu, windows/linux/mac, AMD/NVidia, and OpenGL/DirectX.


Now the bummer is, I went completely broke in the process so I will be charging for it. Something on par with offline pathtracers but reasonable for the indies. Of course Sam will get one for free if he is interested, been lurking this blog for years :)

1. CMOS incredibly high power dissipation simply stuns




2. Albeit the most urgent task for everyone living in conditions of Earth's psychosphere is to kill the Core Evil (this is serious what is happening on the planet, so that even Christ was born only from the seventh attempt), Microsoft was unable only to make Wave files 64-bit.

Chris something like a plug in would be ideal to start.


Of course you should earn money with it, for "free" i thought about business models

like UE4 or something like that. Just cheap enough for people without big

investment money.

Noise wouldnt be so important because its new and experimental.

Would be fun to see if simple indie games look much better than current aaa titles.

Jenson Button, >> "so that even Christ was born only from the seventh attempt". Looks like driving a McLaren has impaired your cognitive abilities.


Chris: 1 billion rays/sec on a GTX680 is not bad. Are the rays incoherent? And what traversal scheme are you using?

Sam: Yes, that's an average over multiple incoherent bounces. I don't want to detail the acceleration structure here, but it is a homebrew and it isn't anything like a BVH. If you want, I'd be happy to detail it for you through e-mail sometime after release.

@CPFUUU: Unreal has a lot of big customers and are high volume, I don't think I could get away with a royalty-only license like they do. I'm just going to set a reasonable price for small studios ($400 or so) - the hobbyists are going to torrent it or pass it around anyway

Interesting, looking forward to know more. I'm also researching a novel acceleration structure which is unlike any of the traditional ones. Even though a BVH (with or without spatial splits) currently offers the best performance for GPU ray tracing, it's not flexible enough.

I just can't get it to compile and run correctly - any chance you build a windows binary with the suitable dlls files inside so I can run the demo please?

Anon, you can download the executable (Win 32) here: https://github.com/straaljager/GPU-path-tracing-tutorial-3/releases

I am sure the rays made of Christ spritual charge are super fast and super coherent.


Now it all makes sense Jenson, it really does...

EU project Ions4Set working on Single-Electron Transistors with the promise of using 10x less energy.



5 component halfadder was realized in 2012. http://phys.org/news/2012-11-smallest-logic-circuit-fabricated-single-electron.html

The SET had multivalue reRAM on the device(SET) itself.

Although it sounds pretty crazy right now i am pretty sure that the future of path tracing will be mobile.

Nvidia X1 achieves 250GFLOPs/W.

I am so sure because i believe/know that Magic Leap's device will be again a new motivator and driver for the whole mobile chip industry.

My prediction therefore is that in 10 years there are going to be mobile chips with 10TFLOPs/W efficiency. Faster non-volatile memory included.

The desktop PC will go extinct like the CRT. :P

>> "The desktop PC will go extinct like the CRT."


I think there will be a revival of the PC platform, especially since Microsoft announced to abandon the console business yesterday.

I think there will be a revival of the PC platform, especially since Microsoft announced to abandon the console business yesterday.



I think the PC platform will be new defined. A technological tectonic shift. haha

But it is not going to happen overnight.

Every year hundreds of millions of high end smartphones get sold. How do they get used?

Well, i don think i need to answer that. XD

Once those superprocessors receive a worthy visual interface and real keyboard things are going to change.

Backpain, headaches , all caused by sitting at a desktop, destroying entire social relationships will be gone once you carry the visual interface on your head.

Then the PC will bend to us rather than we to it.

I expect those goggles to get lighter and lighter(matrix Style) unlike the Rift which now weighs a whopping 470gramms. ^^

I have backpain, so i want the desktop platform to go extinct. haha

Although.....

https://www.youtube.com/watch?v=Gy3nhYPUd7I

Mobile processors are and always will be capable of less than a desktop-class processor without the restrictions on power, heat, and size. I don't think NVidia's TK1/X1/etc. line of processors will ever outmatch their deskop offerings, and their is no plan for them to be able to do so.



Desktop-class processors will continue to lead the bleeding edge. Even when we reach some theoretical point where pathtracing is possible in realtime, we still have more need for compute in the area of physics (position-based dynamics, etc.) to get realistic movement.

As for AR, this is a more subjective opinion and I could definitely be wrong, but I don't think AR will ever take off. If I were an investor I would not pump any money into it. I still see AR as a "solution without a problem". Contrary to this, I think VR headsets have unlimited potential, and that is where I would put my money.

Of course they won't ever outmatch more raw silicon area for computing or your power socket.


The best batteries we'll have will have a energy density of about 1180 Wh/liter (Sakti3,incorporated by Dyson). So 118 Wh for a very portable battery weighing 250 grams.

But there is also another constraint. How hot can a device get hold by your hand? 10-20 Watts max.

There are still lots of improvements that can be done beside Moore's law.

one example https://www.youtube.com/watch?v=wU0bEnQZAF4

Even exascale supercomputers are going to be 20 times more efficient.

That paper on reduced precision hardware seems really interesting.



How many spp/s can Brigade handle?

6% of one FPU of a GPU? What exactly is the FPU of a GPU and how big is it?

Is there in every shader core a FPU?

Seems almost like an april fools joke to me.

A few mm² at 1 Watt? + the add operations.....

Where does all the power go on a GPU if 5 TFLOPs only need 27 Watt.

Off -chip access to DRAM? INstruction unit?

Would there also be a path to accelerate shading operations for a Monte Carlo simulation?

I mean 1 Watt..... that is looking like path tracing would converge towards mobile integration one day.

A Tegra X1 yields 1 TFlops at half precision and 4 Watts.

The start up Parallela wants to produce a 64,000 core processor by 2018 executing 1TFLOP/Watt. 64GB of scratchpad memory, 1MB per core.

Where is path tracing going ?

Could it be that it will be one good day(2022?) executed at 5-10 Watts on a mobile device with a 20-40Whours battery?

Is it just a question of circuit organization ?

Is this method the one used in the path traced quake 2 for dynamic objects?


If not can you tell me it's name, I would like to try something new.

PS:Great blog ;)

Is this acceleration structure the one used in the path traced quake 2 for dynamic objects?


If not can you tell me it's name?

PS: great post and blog.

Hi, loving your blog!


I have a question regarding performance in this example. When I build it myself, everything's running so slow, like 1 frame every 4 seconds, and this is even with smaller model (bunny) and on 640*480 resolution. On GTX970. However, when I run your binary (https://github.com/straaljager/GPU-path-tracing-tutorial-3/releases) , I'm getting great performance. Can't figure out what's causing this, any ideas?

Hi Mykolas, that doesn't sound right, you should get over 60fps with a gGTX970. Are you building it in Release mode?

Ah, yes, I found that my project was in debug mode (debug symbols enabled for CUDA). Now it's working fine! :)

Good to know it's working :)

Thank you for this post! It has really helped me understand BVHs. I have been building a small path tracing using an OpenGL compute shader. I was just wondering what you though about a stackless traversal algorithm by storing the index of the each nodes sibling (in each node structure) and simply iterating along a depth first array of nodes incrementing the node index if the ray intersects the node, and setting the node index to the sibling index if it does not.



Thanks for the great post! It has really helped me understand BVHs. I am building a small path tracer using an openGL compute shader. I was wondering what you though about a stackless traversal algorithm, for each node in the (depth first) array of bvh nodes, storing the index of its sibling node. then to traverse the tree you could simply iterate over each node in the depth first array, incrementing the nodeindex if the ray intersect the node, and setting the nodeindex to the sibling index of the current node is it does not. Thanks!

Post a Comment