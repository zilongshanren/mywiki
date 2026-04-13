---
title: Shader tips and tricks
url: https://interplayoflight.wordpress.com/2022/01/22/shader-tips-and-tricks/
author: Kostas Anagnostou
published: '2022-01-22'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

In this post I have collected some random shader tips and tricks for easy access. Most of them revolve around performance improvement, as one can imagine, with a slight bias towards GCN/RDNA and DirectX. Before I begin with the list of advice, some caveats first.

**The caveats**

- Take any performance advice with a grain of salt, a lot of them fall into the “best practice” category but it is not gospel.
- Always profile before and after an “improvement”, sometimes observed results defy common knowledge
- Get to know the target platform and its particularities, eg a laptop GPU can be quite powerful but lack in memory bandwidth compared to a desktop one.

**The advice**

- Prefer reading textures/rendertargets with Load() if there is no need for texture filtering, over Sample() with point sampling.
- The texture units support some
[comparison operations](https://docs.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_filter)when sampling texture data (eg min/max), worth using them for increased speed and reduced VGPR requirements. - On the subject of using the fixed function units more, it is worth creating a texture as sRGB to avoid the linearisation in the shader.
- When sampling a single channel use Gather4() instead of Sample(), it won’t reduce memory bandwidth but will reduce the amount of traffic to the texture units and improve cache hit rate and VGPRs needed for addressing.
- Use input and output instruction modifiers. Modifiers like saturate(), x2, x4, /2, /4 on output and abs(), negate on input, can allow extra operations in shaders for free. For eg this: saturate(4*(x*-abs(z)-abs(y))) is just a single instruction on GCN: v_fma_f32 v1, v2, -abs(v3), -abs(v0) mul:4 clamp
- Use can also use
[some literals like](http://32ipi028l5q82yhj72224m8j.wpengine.netdna-cdn.com/wp-content/uploads/2017/03/GDC2017-Advanced-Shader-Programming-On-GCN.pdf)-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0 and 1.0/(2.0*pi) directly in an instruction (no register allocation, again on GCN) - Consider partially unroll loops when reading from textures (eg halve the number of iterations and do 2 textures reads in each) to improve scheduling.
- Doing the opposite can help reduce the VGPRs count in the shader and increase occupancy.
- Fully unrolling loops can increase the shader instruction count and reduce shader residency in instruction caches.
- Linear compute shader thread indexing can lead to bad cache coherence when the indices are used as texture coordinates.
[Swizzling the thread id](https://developer.nvidia.com/blog/optimizing-compute-shaders-for-l2-locality-using-thread-group-id-swizzling/)can improve texture sample locality and increase cache hits - Select buffer type (among Constant, Structured, ByteAddressed etc) appropriate for a particular GPU, for example I
[ntel GPUs can benefit from a byteaddressedbuffer](https://www.intel.com/content/www/us/en/developer/articles/guide/developer-and-optimization-guide-for-intel-processor-graphics-gen11-api.html). - Select input and output data type appropriate for your application (for eg R11G11B10 floating point rendertargets instead of RGBA16), this can reduce bandwidth and potentially VGPR use as well.
- It is worth
[converting and/or packing](https://github.com/apitrace/dxsdk/blob/master/Include/d3dx_dxgiformatconvert.inl)larger data types into smaller ones (lower precision), ALU decompression is cheaper than memory bandwidth. [fp16](https://therealmjp.github.io/posts/shader-fp16/)is a good way to reduce VGPR usage and speedup ALU ops and it is a first class citizen in newer GPUs.[Actual fp16 performance](https://twitter.com/MartinJIFuller/status/1485181350881763330?s=20)will rely on finding 2x data parallelism within a single thread and staying within the fp16 instruction set for long periods of time. Also keep an eye on automatic fp16 to fp32 promotions.[Context rolls](https://gpuopen.com/learn/understanding-gpu-context-rolls/)can matter, especially with small drawcalls, try to batch drawcalls by state- Use
[scalar and wave](https://twitter.com/KostasAAA/status/1063075770761916416)operations where possible, for faster instructions and data access. Lookout for gotchas like SV_InstanceID which is not wavefront invariant. - Even if an operation can’t be fully scalarised, you can use a
[waterfall loop](https://gpuopen.com/wp-content/uploads/slides/GPUOpen_Let%E2%80%99sBuild2020_A%20Trip%20Down%20the%20GPU%20Compiler%20Pipeline.pdf)to partially scalarise it. - Memory bandwidth is the biggest bottleneck in a shader, avoid cache misses, especially when sampling with noise, consider
[de-interleaving](https://developer.nvidia.com/sites/default/files/akamai/gameworks/samples/DeinterleavedTexturing.pdf)to achieve good locality. This can help with thread divergent work like raytracing/raymarching. - Use
[NonUniformIndex](https://www.asawicki.info/news_1608_direct3d_12_-_watch_out_for_non-uniform_resource_index)when indexing arrays of textures, even if you create them in code. - Store critical access data, as constants, straight into the root signature but don’t overdo it because it has limited space it may spill to main memory
- Group Maths operations by data type. Mixing scalar and vector types in operations, instead of grouping them by dimension, can lead to wasted ALU instructions in a shader.
[This](http://shader-playground.timjones.io/78d778ede516a60737da592727a877ed)is an example of how reordering a series of multiplications can drop the number of instructions by 25%. - Do not fear branches in the shader but reason about their use (how divergent they can be, uniform is fine, non-uniform maybe not). Leaving big branches, not often taken, in the code will bring total VGPR allocation up and can affect occupancy.
- Small branches of code may perform better when “flattened”.
- Consider using “tiled” processing (classifying in each pixel tile, say 16×16 and run a different shader for similar tiles) if there is a lot of divergence in the shader
- Both VGPR count and Local Data Store allocation can affect occupancy, worth keeping an eye on both
[Low occupancy is not always bad](https://interplayoflight.wordpress.com/2020/11/11/what-is-shader-occupancy-and-why-do-we-care-about-it/), the compiler may have other means to hide memory latency. An indication about this ability is the distance between the texture issue and texture sample use (look for instruction s_waitcnt)- High occupancy/low VGPR count is not always good: the compiler may be forced to “serialise” memory fetches to reuse VGPRs more which can lead to bad scheduling and it can also trash the cache.
- Do not do (expensive) work in
[out of rendertarget/screen threads](https://interplayoflight.wordpress.com/2021/10/28/the-curious-case-of-slow-raytracing-on-a-high-end-gpu/). - Transfer work from pixel shaders to compute shaders to remove potential export stalls (especially if the pixel shader is short). Similarly, this could benefit shader code with a lot of early-outs and varying workloads.
- Beware of
[early z](https://developer.arm.com/documentation/102224/0200/Early-Z)deactivation (writing to SV_Depth, a UAV, alpha testing, alpha to coverage etc), it can lead to wasted pixel shader work. - Stencil culling is generally faster than discarding the pixel in the pixel shader
- Use
[bit twiddling hacks](http://graphics.stanford.edu/~seander/bithacks.html), a lot of them are usable in shaders as well. - A compute shader threadgroup should fill at least a few wavefronts/warps, for eg 128/256 threads on GCN. The number also depends on the registers used per thread, to achieve good occupancy, and the need to share data between the threads of the group or not (
[for more](https://gpuopen.com/learn/optimizing-gpu-occupancy-resource-usage-large-thread-groups/)). - Avoid non native instructions like atan, they expand into a large number of native instructions
- Avoid integer division, it is a non-native operation. Keep an eye on the D3D12 debug layer, it will warn for its presence.
- Use expensive (eg
[trigonometric](https://seblagarde.wordpress.com/2014/12/01/inverse-trigonometric-functions-gpu-optimization-for-amd-gcn-architecture/)) function[approximations](https://michaldrobot.com/2014/06/03/shaderfastmath-lib-is-finally-public/)but profile to determine if it is actually an improvement. [InverseLerp](https://gamedev.net/articles/programming/general-and-gameplay-programming/inverse-lerp-a-super-useful-yet-often-overlooked-function-r5230)is a useful little function to get the fraction based on a range and a distance. I frequently use it a cheap replacement of smoothstep.- It’s worth storing indices/loop counts you pass to shaders as ints instead of floats it’ll save you some conversion instructions and maybe registers. Make sure that you do it on both ends and not only in the shader
- When using SV_DispatchThreadID in the compute shader to emulate pixel shader’s SV_Position it is worth adding half a pixel to it else you may get errors (like world position reconstruction mismatch, when doing TAA). SV_Position in the pixel shader comes with the half pixel already added.
- Packoffsets in constant buffers do not have to be
[consecutive or in order, or even start at zero](http://shader-playground.timjones.io/df2b371902ad92cb2f3aedc50cf772a1). Prepare for some debugging pain if your shader reflection data doesn’t capture this. [Bank conflicts](https://on-demand.gputechconf.com/gtc/2018/presentation/s81006-volta-architecture-and-performance-optimization.pdf)when reading LDS can increase latency of memory read instructions as it serialises them.- Setting any vertex position to NaN is a good way to cull a triangle in the Vertex Shader. Depending on the GPU, this can be achieved by
[writing 0/0 or asfloat(0x7fc00000)](https://twitter.com/longbool/status/1484984001634971655?s=20). - In HLSL, asfloat(0x7F800000) can also be used to represent “Infinity”,
[for setting the far plane to](https://link.springer.com/chapter/10.1007/978-1-4842-7185-8_3)for example. - GetDimensions() is considered a texture instruction. Better pass texture dimensions through a Constant Buffer.
- Consider moving pixel shader work to the vertex shader but bear in mind that the process of passing data from the vertex to the pixel shader can become a bottleneck if too much, you’ll always pay for the work even if the pixel is culled/discarded and that on some architectures texture access can be slower in the vertex shader due to reduced cache locality.
- NaNs can propagate through the pipeline and destroy the output.
[Catch NaNs](https://sakibsaikia.github.io/graphics/2022/01/04/Nan-Checks-In-HLSL.html)in the shader and visualise them for easier debugging - When debugging a shader feature try to reduce the problem dimensionality by, for example, providing known fixed values as an input, as opposed to a texture.
- Visual shader debugging (make the shader output a constant value, eg red, for each different path) is sometimes the fastest way to determine what is wrong with it.
- Vertex attribute interpolation happens in the shader in modern GPUs, it is worth using the “
[nointerpolation](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-struct)” modifier when no interpolation is actually needed, to reduce ALU and VGPR usage. - On some architectures,
[binding the depth buffer as a texture will decompress it](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2013/05/GCNPerformanceTweets.pdf)making subsequent z-testing more expensive. Make sure that you are done using it for geometry rendering before using it as a texture (not so easy in deferred shading engines where you need it for lighting, before rendering transparent meshes). - Speaking of z-testing,
[reverse-z](https://developer.nvidia.com/content/depth-precision-visualized)is[easy to setup](https://github.com/sebbbi/rust_test/commit/d64119ce22a6a4972e97b8566e3bbd221123fcbb)and increases depth precision in the depth buffer, and improves z-fighting, significantly. - It pays off to invest time in learning how to read
[shader assembly](https://interplayoflight.wordpress.com/2021/04/18/how-to-read-shader-assembly/)and get in the habit of inspecting the output of the shader compiler to determine the potential cost of some instructions, using tools like[Shader Playground](http://shader-playground.timjones.io/). - To achieve good performance one needs to utilise the GPU fully, both ALU and fixed-function units. This involves profiling each case to identify bottlenecks and often going against wisdom to make a shader less efficient if that means that it can overlap better with other work.
[This presentation](https://s3.amazonaws.com/nd.images/research/2020_siggraph/Low_Level_Optimizations_In_TLOU2.pptx)is a good chronicle of this.