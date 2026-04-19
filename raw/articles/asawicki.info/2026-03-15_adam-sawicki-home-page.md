---
title: Adam Sawicki Home Page
url: https://asawicki.info/index
published: '2026-03-15'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

[#](https://asawicki.info/news_1801_directx_12_news_from_gdc_2026_-_my_comments) DirectX 12 News from GDC 2026 - My Comments

Sun

15

Mar 2026

[Game Developers Conference (GDC)](https://gdconf.com/) just took place on 9–13 March 2026 (renamed this year to “GDC Festival of Gaming”). Microsoft announced lots of interesting news during the event regarding further development of DirectX 12, its accompanying libraries, and tools. I didn’t attend the conference this year, but the announcements were also published on their [DirectX Developer Blog](https://devblogs.microsoft.com/directx/). In this article, I will gather and summarize these news items, provide links to the appropriate web pages, and include my comments.

When I was working at AMD, I was deeply involved in this area - writing code, publishing articles on the [GPUOpen website](https://gpuopen.com/), attending GDC, and even giving a talk there twice. Back then, I didn’t post much about it on my personal blog, as I would have needed to watch my words and secure corporate approvals. Now, as I’m just a programmer at Plastic - a small game development studio - I can observe these developments from the outside and comment on them freely, which I am going to do with brutal honesty 🙂 If I had a YouTube channel, I would record a “reaction” type of video, but since I’m writing a blog, this will be my reaction in text form.

*Disclaimer: Everything in this article is based on information shared publicly by Microsoft and GPU vendors and could be gathered by any graphics programmer. No insider information was used.*




[Comments](https://asawicki.info/news_1801_directx_12_news_from_gdc_2026_-_my_comments#disqus_thread) |
[#microsoft](https://asawicki.info/news?x=tag&tag=microsoft) [#directx](https://asawicki.info/news?x=tag&tag=directx)
[Share](http://www.addtoany.com/share_save?linkurl=https%3A%2F%2Fasawicki.info%2F%2Fnews_1801_directx_12_news_from_gdc_2026_-_my_comments&linkname=DirectX+12+News+from+GDC+2026+-+My+Comments)

[#](https://asawicki.info/news_1800_total_commander_-_a_plugin_supporting_a_custom_archive_format_-_a_new_article) Total Commander - a Plugin Supporting a Custom Archive Format - a New Article

Sat

07

Mar 2026

Today I would like to present my new article: "Total Commander – a Plugin Supporting a Custom Archive Format". In this article, we will design our own file format that allows multiple files to be packed and compressed into a single archive, similar to formats like ZIP or 7Z. Using the C++ language and the Visual Studio environment on Windows, we will then write a plugin for the Total Commander file manager that enables creating and manipulating such an archive, including freely adding and removing files inside it.

The article was first published few months ago in Polish in [issue 5/2025 (120) of the Programista magazine](https://programistamag.pl/programista-52025-120-pazdzierniklistopad-2025-total-commander-wtyczka-obslugujaca-wlasny-format-archiwum/). Now I have a right to show it publicly for free, so I share it in two language versions:

See also GitHub repository with the source code accompanying the article: **sawickiap/TotalCommanderPluginTutorial**

[#](https://asawicki.info/news_1799_a_formula_for_overall_system_load) A Formula for Overall System Load

Thu

26

Feb 2026

Some time ago I've shared my thoughts about coming up with a nice formula to calculate [memory fragmentation](https://asawicki.info/news_1757_a_metric_for_memory_fragmentation). I've recently had another such math puzzle, this time themed around "system load". Below you will find the formula I developed, this time with an interactive demo!

The problem is this: Imagine a system that consists of several sub-systems, each having a gauge indicating the current load, 0...100%. It may be some real device like a computer (with CPU busy %, GPU busy % and the current memory consumption), some vehicle (a car, an airplane), or some virtual contraption, like a spaceship in a sci-fi video game (with the current engine load, force field strength, temperature that can make it overheat, etc.) Apart from the load of the individual subsystems, we want to show a main indicator of the **overall system load**.

What formula should be used to calculate it? All the load values, displayed as 0...100%, are internally stored as numbers in the range 0.0...1.0. The key principle is that if at least one subsystem is overloaded (at or near 100%), the entire system is considered overloaded. A good formula for the overall system load should have the following properties:

Note that these requirements don't specify what happens between 0 and 1. For example, should the output become 0.5 if just one input reaches 0.5, or only after all inputs reach 0.5? We have full freedom here.

#1. My first idea was to use `AVERAGE(input[i])`

. It meets requirement 1 and 3, but it doesn't meet requirement 2, because it requires all inputs to be 1 for the output to become 1.

#2. My second idea was to use `MAX(input[i])`

. It meets requirement 1 and 2, but it doesn't meet requirement 3, because for any input other than the largest one, a change in its value doesn't change the output.

#3. There is a more complex formula that meets all 3 requirements. It may be called the "inverse product" and it looks like this:

output1 = 1.0 - ( (1.0 - input[0]) * (1.0 - input[1]) * ... )

You can think of it as multiplying the "headrooms" left in each subsystem.

#4. Unfortunately, the formula shown above has a tendency to give very high values nearing 100% even for low input values, which is not very user-friendly. A result that is closer to `MAX()`

reflects the overall system load better. Considering this, but still wanting to preserve our requirement 3, I ended up blending `AVERAGE()`

with the inverse product 50/50:

finalOutput = (AVERAGE(input[i]) + output1) * 0.5

Here is an interactive demo of all the formulas described above. You can move the sliders to control the input values.

Further modifications are possible:

[#](https://asawicki.info/news_1798_graphics_apis_yesterday_today_and_tomorrow_-_a_new_article) Graphics APIs – Yesterday, Today, and Tomorrow - a New Article

Tue

20

Jan 2026

Today I would like to present my new article: "Graphics APIs – Yesterday, Today, and Tomorrow". In this article, we will take a quick walk through the history of graphics APIs such as DirectX, OpenGL, Vulkan, and the accompanying development of graphics cards on the one hand, and video games on the other, over the years. We will not be learning how to program in any of these APIs. This article should be understandable and may be engaging for anyone curious about games or graphics, or at least for those who played games in childhood.

The article was first published few months ago in Polish in [issue 4/2025 (119) (July/August 2025) of the Programista magazine](https://programistamag.pl/programista-42025-119-lipiecsierpien-2025-api-graficzne-wczoraj-dzis-i-jutro/). Now I have a right to show it publicly for free, so I share it in two language versions:

[Comments](https://asawicki.info/news_1798_graphics_apis_yesterday_today_and_tomorrow_-_a_new_article#disqus_thread) |
[#productions](https://asawicki.info/news?x=tag&tag=productions) [#directx](https://asawicki.info/news?x=tag&tag=directx) [#vulkan](https://asawicki.info/news?x=tag&tag=vulkan) [#opengl](https://asawicki.info/news?x=tag&tag=opengl) [#rendering](https://asawicki.info/news?x=tag&tag=rendering)
[Share](http://www.addtoany.com/share_save?linkurl=https%3A%2F%2Fasawicki.info%2F%2Fnews_1798_graphics_apis_yesterday_today_and_tomorrow_-_a_new_article&linkname=Graphics+APIs+%E2%80%93+Yesterday%2C+Today%2C+and+Tomorrow+-+a+New+Article)

[#](https://asawicki.info/news_1797_state_of_gpu_hardware_end_of_year_2025_-_new_article) State of GPU Hardware (End of Year 2025) - New Article

Mon

29

Dec 2025

I published a guest article by Dmytro “Boolka” Bulatov, providing an overview of the current GPU market in context of what features are supported on end-users machines:

[Comments](https://asawicki.info/news_1797_state_of_gpu_hardware_end_of_year_2025_-_new_article#disqus_thread) |
[#gpu](https://asawicki.info/news?x=tag&tag=gpu) [#hardware](https://asawicki.info/news?x=tag&tag=hardware) [#directx](https://asawicki.info/news?x=tag&tag=directx)
[Share](http://www.addtoany.com/share_save?linkurl=https%3A%2F%2Fasawicki.info%2F%2Fnews_1797_state_of_gpu_hardware_end_of_year_2025_-_new_article&linkname=State+of+GPU+Hardware+%28End+of+Year+2025%29+-+New+Article)

[#](https://asawicki.info/news_1796_how_i_fixed_my_app_taking_5_minutes_to_start) How I Fixed My App Taking 5 Minutes to Start

Mon

22

Dec 2025

I recently got a new Windows PC, which I use for development. I work on a game based on Unreal Engine, and I build both the game and the engine from C++ source code using Visual Studio. From the very beginning, I had an annoying problem with this machine: **every first launch of the game took almost five minutes.** I don’t mean loading textures, other assets, or getting into gameplay. I mean the time from launching the app to seeing *anything* on the screen indicating that it had even started loading. I had to wait that long every time I started or restarted the system. Subsequent launches were almost instantaneous, since I use a fast M.2 SSD. Something was clearly slowing down the first launch.

**Solution: open Windows Settings and disable Smart App Control.** This is a security feature that Microsoft enables by default on fresh Windows installations, and it can severely slow down application launches. If you installed your system a long time ago, you may not have it enabled. Once you turn it off, it cannot be turned back on - but that’s fine for me.

**Full story:** I observed my game taking almost five minutes to launch for the first time after every system restart. Before I found the solution, I tried many things to debug the problem. When running the app under the Visual Studio debugger, I noticed messages like the following slowly appearing in the Output panel:

'UnrealEditor-Win64-DebugGame.exe' (Win32): Loaded (...)Engine\Binaries\Win64\UnrealEditor-(...).dll. Symbols loaded.

That’s how I realized that loading each .dll was what took so long. In total, launching the Unreal Engine editor on my system requires loading 914 unique .exe and .dll files.

At first, I blamed the loading of debug symbols from .pdb files, but I quickly ruled that out, because launching the game without the debugger attached (Ctrl+F5 in Visual Studio) was just as slow - only without any indication of what the process was doing during those five minutes before anything appeared on the screen.

Next, I started profiling this slow launch to see what was happening on the call stack. I used the [Very Sleepy profiler](https://github.com/VerySleepy/verysleepy), as well as [Concurrency Visualizer extension](https://learn.microsoft.com/en-us/visualstudio/profiling/concurrency-visualizer?view=visualstudio) for Visual Studio. However, I didn’t find anything unusual beyond standard `LoadLibrary`

calls and other generic system functions. That led me to suspect that something was happening in kernel space or in another process, while my process was simply blocked, waiting on each
DLL load.

Naturally, my next assumption was that some security feature was scanning every .dll file for viruses. I opened Windows Settings → Protection & security → Virus & threat protection and added the folder containing my project’s source code and binaries to the exclusions list. That didn’t help. I then completely disabled real-time protection and the other toggles on that page. That didn’t help either. For completeness, I should add that I don’t have any third-party antivirus software installed on this machine.

I was desperate to find a solution, so I thought: what if I wrote a separate program that calls `LoadLibrary`

on each .dll file required by the project, in parallel, using multiple threads? Would that “pre-warm” whatever scanning was happening, so that launching the game afterward would be instantaneous?

I saved the debugger log containing all the “Loaded … .dll” messages to a text file and wrote a small C++ program to process it, calling `LoadLibrary`

on each entry. It turned out that doing this on multiple threads didn’t help at all - it still took 4–5 minutes. Apparently, there must be some internal mutex preventing any real parallelism within a single process.

Next, I modified the tool to spawn multiple separate processes, each responsible for loading every N-th .dll file. That actually helped. Processing all files this way took less than a minute, and afterward I could launch my game quickly. Still, this was clearly just a workaround, not a real solution.

I lived with this workaround for weeks, until I stumbled upon an article about the Smart App Control feature in Windows while reading random IT news. I immediately tried disabling it - and it solved the problem completely.

Apparently, Microsoft is trying to improve security by scanning and potentially blocking every executable and .dll library before it loads, likely involving sending it to their servers, which takes a very long time. I understand the motivation: these days, most users launch only a web browser and maybe one or two additional apps like Spotify, so every newly seen executable could indeed be malware trying to steal their banking credentials. However, for developers compiling and running large software projects with hundreds of binaries, this results in an egregious slowdown.

[#](https://asawicki.info/news_1795_secrets_of_direct3d_12_the_behavior_of_clearunorderedaccessviewuintfloat) Secrets of Direct3D 12: The Behavior of ClearUnorderedAccessViewUint/Float

Wed

17

Dec 2025

This article is about a quite niche topic - the functions `ClearUnorderedAccessViewUint`

and `ClearUnorderedAccessViewFloat`

of the `ID3D12GraphicsCommandList`

interface. You may be familiar with them if you are a programmer using DirectX 12. Their official documentation - [ClearUnorderedAccessViewUint](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-clearunorderedaccessviewuint) and [ClearUnorderedAccessViewFloat](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-clearunorderedaccessviewfloat) - provides some details, but there is much more to say about their behavior. I could not find sufficiently detailed information anywhere on the Internet, so here is my take on this topic.




[#](https://asawicki.info/news_1794_all_sources_of_directx_12_documentation) All Sources of DirectX 12 Documentation

Tue

25

Nov 2025

Every API needs documentation. Even more so in the case of a graphics API, where there is no single implementation (like in the case of a specific library), but countless users of the API (video games and other graphics apps) and several implementers on the other side of the API (graphics drivers for GPUs from various vendors like AMD, Intel, and Nvidia).

[Vulkan documentation](https://docs.vulkan.org/spec/latest/index.html), for example, is very extensive, detailed, and precise. Sure, it is not perfect, but it's getting better over time. It's also very formal and difficult to read, but that's how a reference specification should be. For learning the basics, third-party tutorials are better. Documentation is needed for more advanced, day-to-day work with the API. I like to think of the documentation as law. A software bug is like a crime. When the application crashes, you as a programmer are a detective investigating "who killed it". You check the specification to see if the app "broke the law" by using the API incorrectly - meaning your app is guilty of the bug - or whether the usage is correct and the culprit is on the other side: a bug in the graphics driver. There are, of course, some gray areas and unclear situations as well.

**Direct3D 12**, unfortunately, doesn't have just one main documentation. In this post, I would like to gather and describe links to all official documents that describe the API... and also complain a bit about the state of all this.

This looks like the main page of the D3D12 documentation. Indeed, we can find many general chapters there describing various concepts of the API, as well as the API reference for individual interfaces and methods. For example:

`ID3D12Device, ID3D12Device1, ..., 10`

.`D3D12_FEATURE_D3D12_OPTIONS20`

, but it links only to documentation up to the But there are also hidden gems - sections that, in my opinion, deserve separate pages, yet are buried inside the documentation of specific API elements. For example:

The documentation linked in point 1 is not fully complete. Direct3D 12, although revolutionary and not backward-compatible, still builds on top of Direct3D 11 in some ways. For that older API, there is this one long and comprehensive document. Sometimes you may need to resort to that specification to find answers to more advanced questions. For example, I remember searching it to find out the alignment requirements for elements of a vertex or index buffer. Be aware through that the parts of this document that apply to D3D12 are only those that D3D12 documentation doesn't define, and that are applicable to D3D12 at all.

On the other hand, recent updates to DirectX 12 are also not included in the documentation mentioned in point 1, as Microsoft now puts their new documents in a GitHub repository. You can find .md files there describing new features added in newer versions of the DirectX 12 Agility SDK - from small ones like [ID3D12InfoQueue1](https://microsoft.github.io/DirectX-Specs/d3d/MessageCallback.html), to very large ones like [DirectX Raytracing (DXR)](https://microsoft.github.io/DirectX-Specs/d3d/Raytracing.html) or [Work Graphs](https://microsoft.github.io/DirectX-Specs/d3d/WorkGraphs.html). This repository also provides pages describing what's new in each shader model, starting from [6.0](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.0), [6.1](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.1), [6.2](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.2), etc... up to [6.8](https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_ShaderModel6_8.md) (at the moment I’m writing this post).
A convenient way to read these docs is through link: [microsoft.github.io/DirectX-Specs/](https://microsoft.github.io/DirectX-Specs/).

Then there is the HLSL shader language and its compiler: DXC. Microsoft also maintains documentation for the compiler and the shader language in a separate GitHub repo, this time using the GitHub Wiki feature. There, we can find descriptions of language features like [16 Bit Scalar Types](https://github.com/microsoft/DirectXShaderCompiler/wiki/16-Bit-Scalar-Types), what's new in each major HLSL language version (2015, 2016, ..., 2021 - see [Language Versions](https://github.com/microsoft/DirectXShaderCompiler/wiki/Language-Versions)), and... again a list of what has been added in recent shader models (see [Shader Model](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model)).

When it comes to the HLSL language itself, it’s sometimes hard to tell what code is correct and supported, because there is no fully formal specification like there is for C++, for example. There is only the [High-level shader language (HLSL)](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl) section of the documentation mentioned in point 1, which briefly describes elements of the syntax. However, Microsoft recently started writing new documentation for HLSL, which can be found in yet another GitHub repository that is most convenient to read online at [microsoft.github.io/hlsl-specs/](https://microsoft.github.io/hlsl-specs/).

I should also mention the DirectX Developer Blog, which is worth following for the latest news about new releases of the Agility SDK and recent additions to the API, as well as updates on related projects like PIX, DirectStorage, and DirectSR (which is pretty much dead now - it was removed from the preview Agility SDK before reaching the retail version). The blog also features nice standalone articles, such as [Getting Started with the Agility SDK](https://devblogs.microsoft.com/directx/gettingstarted-dx12agility/) or the [HLSL 2021 Migration Guide](https://devblogs.microsoft.com/directx/hlsl-2021-migration-guide/), which could easily be part of the main documentation.

As one example I stumbled upon just last week: the description of [ByteAddressBuffer at learn.microsoft.com](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/sm5-object-byteaddressbuffer) mentions that it has methods `Load, Load2, Load3, Load4`

that read `uint`

values from a buffer. But to learn that modern HLSL versions also support templated `Load<MyType>`

, I had to go to a separate document [ByteAddressBuffer Load Store Additions](https://github.com/microsoft/DirectXShaderCompiler/wiki/ByteAddressBuffer-Load-Store-Additions) on the DirectXShaderCompiler Wiki - which describes only that specific addition.

What a mess! Why is the DirectX 12 documentation so scattered across so many websites in different shapes and forms? Of course, I don't know - I don't work at Microsoft. But having worked at big companies for more than 10 years, it isn’t shocking to me. I can imagine how things like this happen. First, engineering managers, project/program managers, and other decision-makers tend to focus on adding new features (everyone wants to “build their pyramid”) while also moving quickly and cutting costs. Creating good documentation is not a top priority. Then, there is Conway’s Law, which states that “Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations.” So if there are separate teams developing DXC, the Agility SDK, etc., they will likely want their own outlets for publishing documentation, while no one takes responsibility for the overall user experience. Still, seeing new initiatives like the HLSL specification, I’m hopeful that things will get better over time.

Finally, [DirectX Landing Page](https://devblogs.microsoft.com/directx/landing-page/) is also worth mentioning, as it gathers links to many SDKs, tools, helpers, samples, and other projects related to DirectX.

[.net](https://asawicki.info/news?x=tag&tag=.net)
[algorithms](https://asawicki.info/news?x=tag&tag=algorithms)
[books](https://asawicki.info/news?x=tag&tag=books)
[c++](https://asawicki.info/news?x=tag&tag=c%2B%2B)
[career](https://asawicki.info/news?x=tag&tag=career)
[commonlib](https://asawicki.info/news?x=tag&tag=commonlib)
[competitions](https://asawicki.info/news?x=tag&tag=competitions)
[compilers](https://asawicki.info/news?x=tag&tag=compilers)
[compo](https://asawicki.info/news?x=tag&tag=compo)
[demoscene](https://asawicki.info/news?x=tag&tag=demoscene)
[directx](https://asawicki.info/news?x=tag&tag=directx)
[engine](https://asawicki.info/news?x=tag&tag=engine)
[events](https://asawicki.info/news?x=tag&tag=events)
[flash](https://asawicki.info/news?x=tag&tag=flash)
[fractals](https://asawicki.info/news?x=tag&tag=fractals)
[gallery](https://asawicki.info/news?x=tag&tag=gallery)
[games](https://asawicki.info/news?x=tag&tag=games)
[ggj](https://asawicki.info/news?x=tag&tag=ggj)
[gpu](https://asawicki.info/news?x=tag&tag=gpu)
[graphics](https://asawicki.info/news?x=tag&tag=graphics)
[gui](https://asawicki.info/news?x=tag&tag=gui)
[hardware](https://asawicki.info/news?x=tag&tag=hardware)
[history](https://asawicki.info/news?x=tag&tag=history)
[homepage](https://asawicki.info/news?x=tag&tag=homepage)
[humor](https://asawicki.info/news?x=tag&tag=humor)
[ideas](https://asawicki.info/news?x=tag&tag=ideas)
[igk](https://asawicki.info/news?x=tag&tag=igk)
[java](https://asawicki.info/news?x=tag&tag=java)
[libraries](https://asawicki.info/news?x=tag&tag=libraries)
[life](https://asawicki.info/news?x=tag&tag=life)
[linux](https://asawicki.info/news?x=tag&tag=linux)
[literature](https://asawicki.info/news?x=tag&tag=literature)
[math](https://asawicki.info/news?x=tag&tag=math)
[microsoft](https://asawicki.info/news?x=tag&tag=microsoft)
[mobile](https://asawicki.info/news?x=tag&tag=mobile)
[music](https://asawicki.info/news?x=tag&tag=music)
[networking](https://asawicki.info/news?x=tag&tag=networking)
[optimization](https://asawicki.info/news?x=tag&tag=optimization)
[origami](https://asawicki.info/news?x=tag&tag=origami)
[philosophy](https://asawicki.info/news?x=tag&tag=philosophy)
[photography](https://asawicki.info/news?x=tag&tag=photography)
[politics](https://asawicki.info/news?x=tag&tag=politics)
[productions](https://asawicki.info/news?x=tag&tag=productions)
[psytrance](https://asawicki.info/news?x=tag&tag=psytrance)
[redmond](https://asawicki.info/news?x=tag&tag=redmond)
[rendering](https://asawicki.info/news?x=tag&tag=rendering)
[scripts](https://asawicki.info/news?x=tag&tag=scripts)
[shopping](https://asawicki.info/news?x=tag&tag=shopping)
[software](https://asawicki.info/news?x=tag&tag=software)
[software engineering](https://asawicki.info/news?x=tag&tag=software+engineering)
[stl](https://asawicki.info/news?x=tag&tag=stl)
[studies](https://asawicki.info/news?x=tag&tag=studies)
[teaching](https://asawicki.info/news?x=tag&tag=teaching)
[tools](https://asawicki.info/news?x=tag&tag=tools)
[video](https://asawicki.info/news?x=tag&tag=video)
[visual studio](https://asawicki.info/news?x=tag&tag=visual+studio)
[vj](https://asawicki.info/news?x=tag&tag=vj)
[vulkan](https://asawicki.info/news?x=tag&tag=vulkan)
[warsztat](https://asawicki.info/news?x=tag&tag=warsztat)
[web](https://asawicki.info/news?x=tag&tag=web)
[webdev](https://asawicki.info/news?x=tag&tag=webdev)
[winapi](https://asawicki.info/news?x=tag&tag=winapi)
[windows](https://asawicki.info/news?x=tag&tag=windows)