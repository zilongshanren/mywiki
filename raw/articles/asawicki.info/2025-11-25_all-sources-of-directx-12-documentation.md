---
title: All Sources of DirectX 12 Documentation
url: https://asawicki.info/news_1794_all_sources_of_directx_12_documentation
published: '2025-11-25'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

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