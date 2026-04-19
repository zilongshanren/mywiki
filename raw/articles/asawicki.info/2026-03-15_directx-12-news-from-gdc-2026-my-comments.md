---
title: DirectX 12 News from GDC 2026 - My Comments
url: https://asawicki.info/news_1801_directx_12_news_from_gdc_2026_-_my_comments
published: '2026-03-15'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

Sun

15

Mar 2026

[Game Developers Conference (GDC)](https://gdconf.com/) just took place on 9–13 March 2026 (renamed this year to “GDC Festival of Gaming”). Microsoft announced lots of interesting news during the event regarding further development of DirectX 12, its accompanying libraries, and tools. I didn’t attend the conference this year, but the announcements were also published on their [DirectX Developer Blog](https://devblogs.microsoft.com/directx/). In this article, I will gather and summarize these news items, provide links to the appropriate web pages, and include my comments.

When I was working at AMD, I was deeply involved in this area - writing code, publishing articles on the [GPUOpen website](https://gpuopen.com/), attending GDC, and even giving a talk there twice. Back then, I didn’t post much about it on my personal blog, as I would have needed to watch my words and secure corporate approvals. Now, as I’m just a programmer at Plastic - a small game development studio - I can observe these developments from the outside and comment on them freely, which I am going to do with brutal honesty 🙂 If I had a YouTube channel, I would record a “reaction” type of video, but since I’m writing a blog, this will be my reaction in text form.

*Disclaimer: Everything in this article is based on information shared publicly by Microsoft and GPU vendors and could be gathered by any graphics programmer. No insider information was used.*

Every year, GDC is the pinnacle moment for game developers, including rendering programmers. Whether it’s worth going there is a separate question, considering the cost of travel (especially for someone living in Europe) and the price of a hotel in San Francisco. There are other important events as well: Nvidia has [GTC](https://www.nvidia.com/gtc/), Epic has [Unreal Fest](https://www.unrealengine.com/en-US/unreal-fest), Vulkan has the [Vulkanised conference](https://vulkan.org/events/vulkanised-2026) as its main event, and graphics researchers gather at [SIGGRAPH](https://www.siggraph.org/). But GDC in March is the annual opportunity for people from all these worlds to get together, listen to talks, and socialize, so we should all pay attention to what happens there.

** DirectX Innovation at GDC 2026** is the article announcing the talks Microsoft delivered during the event. “DirectX State of the Union” is the main one, spanning a variety of topics related to recent DX12 developments. “DirectX is Bringing Console-Level Developer Tools to Windows” is also very interesting, announcing unprecedented progress in graphics tooling, especially PIX. Microsoft was joined on stage by representatives of all four current PC GPU vendors (AMD, Intel, Nvidia, Qualcomm), who normally compete with each other. This is always a sign that something important is happening (like the memorable presentation

GPU vendors also posted their announcements simultaneously, expressing support for Microsoft’s announcements.

On one hand, for Microsoft and GPU vendors (also called Independent Hardware Vendors - IHVs), GDC is a major milestone every year. Developers crunch on their code to finish demos, articles and slide decks are prepared, travel and meetings get scheduled... On top of the engineering effort, there is surely politics involved. Cooperation between teams in a big corporation is difficult enough. Here, Microsoft needed to coordinate with all PC GPU vendors. I believe it is even more challenging for Khronos, where all hardware and software vendors that care about graphics (both desktop and mobile) come together, but I’m sure it was a hectic time there as well.

But on the other hand, what has been announced in these talks will only ship to the public in the upcoming months, basically “when it’s done”, so nothing really changed this week. We just received new information that had been secret so far. It’s like watching a teaser video for a new game (when we read an article announcing new technology) or maybe a gameplay trailer (when we can see an actual API spec), with the game shipping later this year.

The main blog post on DirectX Developer Blog:
[DirectX: Bringing Console-Level Developer Tools to Windows](https://devblogs.microsoft.com/directx/directx-bringing-console-level-developer-tools-to-windows/)

This topic is the most interesting and most important for me personally. Compared to the debuggers we have for CPU programming languages (whether high-level like Python or native like C and C++), I think GPU debugging is really in the Stone Age. GPU crashes (also known as Timeout Detection and Recovery - TDR - whether caused by a timeout or a memory page fault) are especially difficult to debug. Sure, frame capture tools like [PIX on Windows](https://devblogs.microsoft.com/pix/) and [RenderDoc](https://renderdoc.org/) are helpful in debugging various problems, but they require a frame that successfully rendered until the `Present()`

call. The Debug Layer and GPU-Based Validation also do a great job. Finally, crash capture tools like [DRED](https://microsoft.github.io/DirectX-Specs/d3d/DeviceRemovedExtendedData.html) and custom vendor tools - [Nvidia Aftermath](https://developer.nvidia.com/nsight-aftermath) and [Radeon GPU Detective](https://gpuopen.com/radeon-gpu-detective/) - help identify the cause of a crash... when they work, because sometimes they don’t show any meaningful information.

I wish we had a proper debugger for shaders, just like we have debuggers for CPU code - with breakpoints, step-by-step execution, watching the values of local variables, etc. (They would likely need to be conditional breakpoints for a specific frame, draw call, and pixel coordinate or thread ID, because there are thousands of threads running simultaneously on the GPU and millions of them starting every frame.) Sure, PIX and RenderDoc offer shader debugging, but RenderDoc does it by emulating shaders on the CPU, which can break in many cases because it doesn’t show what really happens on the GPU. What if there are timing issues or race conditions, such as a missing barrier? What if there is a bug in the shader compiler for a specific GPU?

Of course, this is not as easy on the GPU as it is on the CPU, where a thread or a process can be suspended while the operating system, IDE, and other apps continue running. On a GPU, the entire chip may be busy executing just a single draw call. However, I can still imagine a scenario where the GPU is stopped, breaking into a debugging session, while the debugger runs on a separate machine or on the same machine with the desktop rendered using integrated graphics. In fact, stopping the entire machine and debugging it from a remote system connected through a network is possible using [WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/windbg-overview), but that is kernel-mode, low-level, hardcore debugging. So we can say that making GPU debugging possible is mostly a matter of developing good high-level tools.

Despite the confidentiality of console SDKs, it shouldn’t be a secret if Microsoft disclosed it in the title of their talk that consoles like Xbox have better graphics tools than the PC. In ** DirectX: Bringing Console-Level Developer Tools to Windows**, they announced a major update to PIX on Windows, along with other tools and APIs intended for debugging. Let’s see what exactly they announced.

First of all, they disclosed a plan to support new DirectX Dump Files (.dxdmp), containing a dump of the GPU state after it crashes. They will be available to open in PIX. It’s great to see they have buy-in from all GPU vendors, as this surely requires their deep involvement and support. It’s also great that there will be a toggle to adjust the trade-off between performance overhead and *"actionability"* (as they called it), since gathering more data may impact performance, which in turn could hide the bug. The “no overhead” mode, where supported, may even be suitable to leave always enabled for end users. Dump files will be available for manual management or collected by Microsoft via Watson.

This all looks very promising. I have just one concern. Based on the example screenshots shown from all four GPU vendors, I suspect this whole system may just be a generic placeholder, with the specific data gathered and displayed being highly dependent on the GPU. We can only hope that the actual crash dumping and the data gathered from the crash will be:

From the screenshots shown:

`ID3D12Device::MakeResident`

.`VS_INVOCATION_COUNT_RCSUNIT_BE_`

and their hexadecimal values. It’s great that they are able to dump the exact state of the GPU at the moment it crashed, but do they really believe game developers will read thousands of pages of Next, Microsoft announced the PIX API - a programmatic way to access all the data a PIX capture and the new crash dump can contain, available to C++, C#, and Python. This is a great step forward. It will definitely be useful for various kinds of automation. I can also imagine developing an MCP server, so an AI agent could use such captures to help with graphics debugging or performance optimization. It’s worth mentioning that by doing this, PIX is basically catching up with RenderDoc, which already has its own [Python API](https://renderdoc.org/docs/python_api/index.html).

Next, they are going to add a HLSL intrinsic function `DebugBreak()`

. See the specification: [0039 - Debugging Intrinsics](https://github.com/microsoft/hlsl-specs/blob/main/proposals/0039-debugbreak.md). It will be similar to the `assert`

macro known from C++ and other CPU languages, triggering an instant crash, which can help identify exactly where an asserted condition was hit - in which frame, which draw call or dispatch, and hopefully also with a pixel or thread ID. It definitely has a chance to work more reliably than my hacky [ShaderCrashingAssert library](https://github.com/sawickiap/ShaderCrashingAssert).

Too bad they didn’t define any parameter that would allow the shader to return some data to the crash dump. Even a single `uint`

or `uint4`

would make a huge difference. Dear Microsoft, can we have that, please???

I also wish that together with this “assert” function, they worked on some standardized “printf” function that would let shaders output messages and data while running, even without crashing. Having those two would move GPU debugging to the Medieval Ages. Implementing convenient logging in HLSL has been discussed many times, including in the good article [An Experimental Approach to printf in HLSL](https://www.abolishcrlf.org/2025/12/31/Printf.html) by Chris Bieneman - still unofficial, despite the fact that he is a Microsoft employee. After this year’s GDC there are still no signs that Microsoft is working on standardizing this, unfortunately.

Then we have PIX events (also known as markers) - the begin/end events with custom strings that we use to organize our draw calls into a logical hierarchy for easier debugging in PIX or RenderDoc. Microsoft announced that they will finally be passed to the graphics driver. This is a huge thing. Let me explain why.

There are basically two ways graphics debugging tools can operate. The first is injecting themselves into the game process and intercepting all calls to the graphics API. That’s what PIX, RenderDoc, and [GfxReconstruct](https://github.com/LunarG/gfxreconstruct) do. This is great, because it captures all the calls and all the data at a high level, exactly as the game developer passed them. On the other hand, it causes multiple problems:

The second mode is a tool connecting directly to the graphics driver (e.g. through a socket) and fetching data from it. That’s how [Radeon Developer Tools](https://gpuopen.com/tools/) operate. It works independently of what game is running or how it was launched. The game process is not altered in any way. A strategic decision to implement tools like this has many advantages. They work very reliably. However, there is one big caveat: the calls that the driver sees are not necessarily the same calls that the game developer made using the graphics API.

In Vulkan, this is not such a big issue, because the driver basically implements the API “on the other side”. It can also expose new extensions (like VK_EXT_debug_utils) that are available to the game code for direct use. With DirectX 12, however, this is not that simple. The sequence looks like this: Game engine code -> DX12 API -> DirectX Runtime (Microsoft code) -> Device Driver Interface (DDI) API -> Driver. Some information gets lost along the way. This includes PIX events. Because of that, AMD had to define their own way of submitting events so they become visible in their tools, in the form of the [AMD GPU Services (AGS) library](https://github.com/GPUOpen-LibrariesAndSDKs/AGS_SDK) or a replacement header for PIX events. See [RGD documentation - Known issues and workarounds](https://gpuopen.com/manuals/rgd_manual/help_manual/#known-issues-and-workarounds) for more details. Now, with Microsoft changing their mind and allowing standard PIX events to reach the driver, this will no longer be necessary. Finally!

I hope that together with begin/end events, Microsoft will also pass to the driver the string names that we assign to our textures and buffers using `ID3D12Object::SetName`

calls. Preferably also data set through `ID3D12Object::SetPrivateData`

- that would provide much more flexibility. Their new [PIX Markers spec](https://microsoft.github.io/DirectX-Specs/d3d/D3D12PIXMarkers.html) mentions `SetName`

to be passed to DDI. This is great, because currently, AMD tools fetch these names through the Event Tracing for Windows (ETW) mechanism, which is a workaround and doesn’t always work reliably. (Which is not a secret - see the article [Viewing DirectX® 12 Named Resources with Radeon™ Memory Visualizer 1.3](https://gpuopen.com/learn/rmv-directx-named-resources/)).

By the way, I personally like the Vulkan approach of formally defining a way to inject layers into the API. I believe it’s high time for Microsoft to do the same. I was secretly hoping they would add such support for layers a long time ago, but they still haven’t, so every tool like PIX, RenderDoc, GfxReconstruct, or [GPU Reshape](https://github.com/GPUOpen-Tools/GPU-Reshape) needs to implement its own solution and struggle with numerous issues. [Nvidia Streamline](https://github.com/NVIDIA-RTX/Streamline) seems to be an effort in this direction, providing a generic layer system for DX12, but because it’s made by Nvidia, unfortunately other GPU vendors didn’t join the effort to spread its adoption. (Hopefully they will have more luck with the [Slang shading language](https://shader-slang.org/).)

Microsoft also announced they are working on *“real-time, on-chip shader debugging”*. This almost sounds too good to be true. But they are giving themselves time until 2027, so I believe that by then they may be able to achieve it, with intense effort and support from GPU vendors. That would be the holy grail that could bring GPU debugging into modern times, catching up with CPU programming languages.

One big challenge in bringing this feature to PC is stopping the GPU and inspecting its state at the exact moment, as I described above. But another problem is showing and stepping through the shader code. I hope it won’t be the GPU assembly (ISA) or the intermediate language (DXIL, SPIR-V), but the real high-level shader language (HLSL, GLSL) as written by the game developer. Supporting this would require all stages of shader compilation to preserve the correlation between ISA instructions and high-level shader source lines, as well as between GPU registers and variables in the shader source. Shaders are highly optimized, with everything inlined. There is no call stack to inspect. Providing a decent debugging experience must therefore be a complex endeavor.

The main blog post on the DirectX Developer Blog:
[Evolving DirectX for the ML Era on Windows](https://devblogs.microsoft.com/directx/evolving-directx-for-the-ml-era-on-windows/)

Let's say it plainly: machine learning using deep neural networks is, at a low level, largely about matrix multiplication. GPUs are great at that. We still call them "graphics processing units", but developers discovered a long time ago that they perform well for many other kinds of tasks. First it was breaking ciphers, then crypto mining, and now it's AI. At a high level, such workloads may look very similar to graphics, which is also about regular, massively parallel processing of vectors and matrices. However, when we dig deeper, there are many differences, including:

GPU vendors introduced dedicated hardware to accelerate these types of ~~matrix multiplication~~ ML workloads. Nvidia has been the most effective at marketing theirs, making sure that even average gamers have heard about Tensor Cores, but AMD also has its Wave Matrix Multiply-Accumulate (WMMA) instructions, and Intel has its XMX units. The problem is that they are available in purely compute-oriented APIs like Nvidia CUDA, AMD HIP/ROCm, and Intel oneAPI, not in graphics APIs and shader languages. They are also used in proprietary upscaling technologies: DLSS, FSR 4, and XeSS, respectively - all implemented as black-box libraries performing some vendor-specific magic under the hood.

Is this the desired and target state of things? Having a custom, proprietary, high-quality technology like DLSS surely gives a vendor some competitive advantage when gamers decide which graphics card to buy. But on the other hand, do GPU vendors really like the fact that precious transistors on their chips and their potential TOPS of computational power stay idle most of the time? I don't think so. I think the real issue is exposing these capabilities in a way that is unified across vendors, high-level, and convenient enough for game developers on one hand, while still utilizing the full performance potential of the hardware on the other.

Vulkan faces the same problem. They solve it in a typical Vulkan way - by introducing extensions. We have VK_KHR_shader_integer_dot_product, VK_KHR_cooperative_matrix, VK_KHR_shader_float16_int8, VK_EXT_shader_float8, and many others. In DirectX 12, Microsoft has made several attempts to offer similar capabilities, with mixed success.

`D3D12_FEATURE_DATA_WAVE_MMA`

to the Agility SDK 1.711.3-preview in June 2023. It was supposed to add support for instructions performing Matrix Multiply-Accumulate cooperatively across a wave, with an API to enumerate all supported matrix dimensions and element data types. Judging by its name, it could have been related to what AMD added to their hardware. Apparently it was a false start, because Microsoft retracted it from the Agility SDK before it shipped in the retail version. Fun fact: one leftover of this abandoned API still remains in retail DX12 in the form of the `D3D12_FEATURE_DATA_D3D12_OPTIONS9::WaveMMATier`

structure member.Side note: [GPU Work Graphs](https://github.com/microsoft/DirectX-Specs/blob/master/d3d/WorkGraphs.md) are not this kind of technology. This recent addition to the DX12 API allows the execution of entire graphs of different shaders. However, we still need to focus our implementation on individual threads and manually control how they are spawned. There is no automatic operator fusion or other optimization performed automatically, like ML frameworks do. Work Graphs are more intended for compute work serving rendering workloads, as an extension of Indirect calls that let the GPU spawn new work on its own. They provide more flexibility by supporting a switch to a different shader, as opposed to only changing the vertex/index buffers and the number of vertices/instances/threads, as in Indirect calls.

Here we are now, after GDC 2026, and Microsoft's current plans to expose these ML-related hardware capabilities seem to come from both angles at once:

**1. As instructions available in normal shaders**

These can be useful for implementing inference of small ML models as part of existing vertex/pixel/compute shaders. For example, this could include neural texture (de)compression, approximation of complex material and lighting models (BRDFs), character animation, or approximate physics simulation. In the future, we may have many small models evaluated every render frame.

These are not really news from this week, because they were announced and their specifications have been available for quite some time. Microsoft develops its HLSL language advancements quite openly by sharing [HLSL specification proposals](https://microsoft.github.io/hlsl-specs/proposals/).

**Long vectors**, as specified in proposal [0026 - HLSL Long Vectors](https://github.com/microsoft/hlsl-specs/blob/main/proposals/0026-hlsl-long-vector-type.md). It adds support for vectors with more than four elements, e.g. `vector<float, 15>`

. Note that they are still normal variables, local to an individual shader thread.

**Linear algebra**, as specified in proposal [0035 - Linear Algebra Matrix](https://microsoft.github.io/hlsl-specs/proposals/0035-linalg-matrix/). It adds a matrix type, such as `Matrix<ComponentType::F16, 8, 32, MatrixUse::A, MatrixScope::Wave>`

, as well as vector-matrix and matrix-matrix operations like `Multiply`

and `MultiplyAccumulate`

.

Note that the matrix has many template parameters:

`I8`

and two `F8`

formats).`A, B, Accumulator`

), meaning the intended role as arguments of the `a * b + c`

operation.`Thread, Wave, ThreadGroup`

), meaning whether the matrix is local and different in each thread, or uniform across the entire wave or thread group and thus shareable across threads and processed cooperatively.`[RW]ByteAddressBuffer`

, there is also "Layout" (`RowMajor, ColumnMajor, MulOptimal, OuterProductOptimal`

), which allows matrices containing intermediate results that we do not need to access directly to be stored in some opaque, GPU-specific layout optimized for the best performance.This API looks very clean and convenient. I believe they may have found a good abstraction. Hopefully, with enough effort put into developing shader compilers, it can also deliver good performance while utilizing the hardware capabilities of each GPU. My concern is whether the API will keep up with new hardware capabilities that GPU vendors may want to expose. By the time it ships in the retail SDK, they may already want support for more data types (like INT4) or even features that go beyond what the API offers, such as sparsity.

**2. DirectX Compute Graph Compiler**

That's a new announcement from GDC 2026. Microsoft teased it as a completely new technology that will consume entire ML models and optimize them for efficient execution on a specific GPU. It will feature *"graph optimization, memory planning, and operator fusion"*. This is clearly an approach to executing ML workloads intended to keep the entire GPU busy for some time, similar to upscaling and other screen-space effects. They will likely execute as multiple compute dispatches, maybe even as separate command buffer submissions.

Note that ML frameworks can already do these things. With this project, Microsoft is basically creating another one, but tailored for cooperation with DirectX 12 and graphics workloads.

Note also that the graph approach is well known in the game development community. Advanced game engines often implement their own graphs representing render passes and dependencies between them, like the [Render Dependency Graph](https://dev.epicgames.com/documentation/en-us/unreal-engine/render-dependency-graph-in-unreal-engine) in Unreal Engine. AMD also developed a similar solution called [Render Pipeline Shaders](https://gpuopen.com/rps/). However, it never gained traction, possibly because developers saw it as overkill to employ LLVM to compile a custom domain-specific language. I'm not sure if it was ever used in any game. The project looks abandoned now. Game engines already have their own graph solutions, which are often simpler and based on C++ templates or macros.

Will the new DirectX Compute Graph Compiler allow game developers to create their own ML-based effects like DLSS or FSR, executed with comparable performance? I hope so. That would finally allow them to fully utilize these GPU hardware capabilities with their own code. But here we are only talking about inference. Designing and training an ML model, and gathering enough high-quality training data, is a separate topic. Training on data from a specific game title could be beneficial in some cases, but on the other hand, IHVs cooperating with many game developers and having access to so many games will still give them a competitive advantage when training their ~~image upscaling~~ super resolution and other models.

The main blog post on DirectX Developer Blog:
[Advanced Shader Delivery: What’s New at GDC 2026](https://devblogs.microsoft.com/directx/advanced-shader-delivery-whats-new-at-gdc-2026/)

Specification:
[Advanced Shader Delivery - Shader Compiler Plugin](https://microsoft.github.io/DirectX-Specs/d3d/ShaderCompilerPlugin.html)

This is basically yet another announcement of [what they already announced before](https://devblogs.microsoft.com/directx/introducing-advanced-shader-delivery/). The problem is this: every GPU has a different instruction set, so shaders cannot be compiled to native code like the .exe files of our games. The second stage of shader compilation (from DXIL/SPIR-V intermediate code to GPU ISA) currently happens inside the graphics driver. The shader compiler is basically one of the driver modules.

I'm not sure it's such a big deal. We will just change "compiling shaders..." to "downloading shaders...", and it will still happen whenever we update the game or the graphics driver. The only hope is that downloading these shaders will be faster than compiling them. The work done by shader compilers is difficult - trying to optimize the shader while still finishing the process within milliseconds. Allowing the compilation to take longer can result in better optimization. I remember debugging a game once that was supposedly hanging on startup, only to find out there were ray tracing shaders taking over a minute each to compile.

But the second feature they’ve announced may provide more performance benefits, even during game development, when shaders keep changing. [Partial Graphics Programs](https://microsoft.github.io/DirectX-Specs/d3d/PartialGraphicsPrograms.html) will allow creating pipeline objects that contain only "pre-rasterization" shaders (like a vertex shader) or only a pixel shader, and later linking them together, which hopefully won’t require full recompilation at that point.

The main blog post on DirectX Developer Blog:
[DirectStorage 1.4 release adds support for Zstandard](https://devblogs.microsoft.com/directx/directstorage-1-4-release-adds-support-for-zstandard/)

I must admit I don't follow the development of this API very closely. Overall, it looks like a good idea. Update 1.4 brings support for the [Zstandard aka zstd](https://github.com/facebook/zstd) compression format, which is open, free, and developed by Meta. Before that, Microsoft promoted the GDeflate algorithm proposed by Nvidia. This change may be perceived as a step in the right direction - toward greater neutrality among GPU vendors.

On top of that, they presented the [Game Asset Conditioning Library](https://github.com/microsoft/Game-Asset-Conditioning-Library) - a library offering pre-/post-processing of data, swizzling it so the core lossless compression algorithm performs better. Doing such tricks to squeeze the maximum potential out of a compression algorithm is known in the demoscene, for example, and is used to create those amazing intros that fit into 4 KB or 64 KB. The library supports BC1–5 and BC7 texture formats, which also looks like a good idea, considering that textures typically constitute a major portion of game asset data.

There is still some concern about the benefits and adoption of DirectStorage overall. As far as I know, many years after the initial release, we are still waiting to see the API used by a large number of games or integrated and enabled by default in major game engines. Whether that ever happens depends on whether the API can consistently demonstrate sufficient benefits over traditional file reading APIs. It definitely has potential thanks to more direct access to SSD NVMe drives and GPU-accelerated decompression directly into buffers and textures in video memory. Whether we see wider adoption or not, the API is public and production-grade, so it is very unlikely Microsoft will silently kill it, as they did with DirectSR.

Specification:
[DirectX Raytracing (DXR) Functional Spec, Part 2](https://microsoft.github.io/DirectX-Specs/d3d/Raytracing2.html)

A new update to the ray tracing API, defined as `D3D12_RAYTRACING_TIER_2_0`

and Shader Model 6.10, will bring the following features, focused mostly on the process of building and updating acceleration structures:

**Cluster Level Acceleration Structure (CLAS)**. This makes acceleration structures three-level. CLAS will be like a meshlet for ray tracing, representing a small piece of a triangle mesh, up to 256 vertices and 256 triangles. Then, an actual Bottom Level Acceleration Structure (BLAS) can be created from such CLASes. This can improve performance and also distribute the performance cost of building acceleration structures more evenly across frames by splitting it into smaller pieces of work.

**Cluster Template** - like CLAS but without vertex positions. An actual CLAS can be "instantiated" from such a template by providing vertex positions, possibly many times when the object is animated. This can provide another performance gain. This API is *"intended to be an upgrade versus traditional updates / refits"*.

Interestingly, they also proposed a new compressed representation of vertex positions, called ** Compressed1 position encoding**, which seems to use shared exponents and delta values to save memory. It reminds me of the

**Partitioned TLAS (PTLAS)** adds another level to the hierarchy by defining a PTLAS as a new kind of Top Level Acceleration Structure (TLAS) that stores references to Partitions, which in turn reference Instances. A Partition holding a range of 100–1000 instances is recommended. This can definitely help solve the problem of rebuilding the entire TLAS every frame, which games typically do today as the set of objects in the virtual world keeps changing dynamically.

Finally, the new specification also introduces acceleration structure building operations as Indirect commands.

[Comments](https://asawicki.info/news_1801_directx_12_news_from_gdc_2026_-_my_comments#disqus_thread) |
[#microsoft](https://asawicki.info/news?x=tag&tag=microsoft) [#directx](https://asawicki.info/news?x=tag&tag=directx)
[Share](http://www.addtoany.com/share_save?linkurl=https%3A%2F%2Fasawicki.info%2F%2Fnews_1801_directx_12_news_from_gdc_2026_-_my_comments&linkname=DirectX+12+News+from+GDC+2026+-+My+Comments)