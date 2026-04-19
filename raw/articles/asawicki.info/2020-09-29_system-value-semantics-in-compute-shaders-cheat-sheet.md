---
title: System Value Semantics in Compute Shaders - Cheat Sheet
url: https://asawicki.info/news_1733_system_value_semantics_in_compute_shaders_-_cheat_sheet
published: '2020-09-29'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

Tue

29

Sep 2020

After compute shaders appeared, programmers no longer need to pretend they do graphics and render pixels when they want to do some general-purpose computations on a GPU (GPGPU). They can just dispatch a shader that reads and writes memory in a custom way. Such shader is a short (or not so short) program to be invoked thousands or millions of times to process a piece of data. To work correctly, it needs to know which is the current thread. Threads (invocations) of a compute shader are not just indexed linearly as 0, 1, 2, ... It's more complex than that. Their indexing can use up to 3 dimensions, which simplifies operation on some data like images or matrices. They also come in groups, with the number of threads in one group declared statically as part of the shader code and the number of groups to execute passed dynamically in CPU code when dispatching the shader.

This raises a question of how to identify the current thread. HLSL offers a number of [system-value semantics](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics#system-value-semantics) for this purpose and so does GLSL by defining equivalent built-in variables. For long time I couldn't remember their names, as the ones in HLSL are quite misleading. If `GroupID`

is an ID of the entire group, and `GroupThreadID`

is an ID of the thread within a group, `GroupIndex`

should be a flattened index of the entire group, right? Wrong! It's actually an index of a single thread within a group. GLSL is more consistent in this regard, clearly stating "WorkGroup" versus "Invocation" and "Local" versus "Global". So, although Microsoft provides a great explanation of their SVs with a picture on pages like [SV_DispatchThreadID](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/sv-dispatchthreadid), I thought it would be nice to gather all this in form of a table, a small cheat sheet:

| HLSL Semantics | GLSL Variable | Type (Dimension) | Unit | Reference |
|---|---|---|---|---|
| SV_GroupID | gl_WorkGroupID | uint3 (3D) | Entire group | Global in dispatch |
| SV_GroupThreadID | gl_LocalInvocationID | uint3 (3D) | Single thread | Local in group |
| SV_DispatchThreadID | gl_GlobalInvocationID | uint3 (3D) | Single thread | Global in dispatch |
| SV_GroupIndex | gl_LocalInvocationIndex | uint (flattened) | Single thread | Local in group |

*Update 2023-08-30: There is another article about this topic that I recommend: "Dispatch IDs and you".*

[Comments](https://asawicki.info/news_1733_system_value_semantics_in_compute_shaders_-_cheat_sheet#disqus_thread) |
[#vulkan](https://asawicki.info/news?x=tag&tag=vulkan) [#opengl](https://asawicki.info/news?x=tag&tag=opengl) [#directx](https://asawicki.info/news?x=tag&tag=directx) [#gpu](https://asawicki.info/news?x=tag&tag=gpu)
[Share](http://www.addtoany.com/share_save?linkurl=https%3A%2F%2Fasawicki.info%2F%2Fnews_1733_system_value_semantics_in_compute_shaders_-_cheat_sheet&linkname=System+Value+Semantics+in+Compute+Shaders+-+Cheat+Sheet)