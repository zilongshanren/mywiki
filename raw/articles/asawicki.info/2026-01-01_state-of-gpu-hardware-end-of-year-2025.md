---
title: State of GPU Hardware (End of Year 2025)
url: https://asawicki.info/articles/state_of_gpu_hardware_2025.php
published: '2026-01-01'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

*This is a guest article by Dmytro “Boolka” Bulatov.*

D3D12 is already [over 10 years old](https://therealmjp.github.io/posts/ten-years-of-d3d12/). Over the years, GPUs got a huge number of new features. However, you need to answer some questions before using those - “Can we require users to have support for that feature? If not, is it even worth using, if we’ll need to implement fallback for users that lack support? Maybe we can use it for some optional feature or an optimization?”.

I’ve compiled some data to show state of the market for the End of Year 2025, and using that we’ll try to come up with a list of features that you can or can’t use and help you pick minimum supported GPU architecture for games targeting D3D12. We won’t try to suggest which VRAM amount to require or which specific GPU to require, since it will heavily depend on the game.

This post mainly targets developers of custom engines, since you don’t have a lot of control over features described in this post if you use a commercially available engine. Also, this post assumes that your engine uses the latest Agility SDK. If you haven’t already integrated it, you really should.

We will primarily use information from 2 sources:

First is [D3d12infoDB](https://d3d12infodb.boolka.dev/). It is a database of D3D12 hardware that lets you see feature support for different GPUs. It is a community driven database - anyone can submit reports by running [D3d12infoGUI](https://github.com/Devaniti/D3d12infoGUI/releases/latest).

Second is [Steam Hardware Survey](https://store.steampowered.com/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam). It is hardware statistics of Steam users. With it you can see GPU distribution of your potential users. We don’t know exactly how those statistics are compiled, and they had some anomalies in the past, but it is the best public data that we have. Steam Hardware Survey is updated monthly, and data we are using is for November 2025, which is latest available data as of writing this article.

This is the most important consideration - whether users’ machines even support the feature. And for that, we are using Steam Hardware Survey, specifically “DIRECTX 12 SYSTEMS (WIN10 WITH DX 12 GPU)” section from [GPU information page](https://store.steampowered.com/hwsurvey/directx/).

However, if you try to look at that data, you’ll realize that it is too far from something that would be useful for us. It just lists specific GPUs with their respective market shares. To transform it into something more useful, the strategy that I used is twofold: calculating market share of each GPU architecture and mapping out feature support for each. First part is done via manually authoring mapping of GPU names from Steam Hardware Survey to Architectures ([GitHub](https://github.com/Devaniti/SteamHWSurveyGPUArchStats)). The second part is done via aggregation of data from D3d12infoDB.

Result is those 2 pages on D3d12infoDB: [Architecture x Feature matrix](https://d3d12infodb.boolka.dev/FeatureTable.html), [Feature tables](https://d3d12infodb.boolka.dev/CanIUse.html).

After compiling all that data, you will still always have at least 12.33% of uncertainty of support for any feature. Reasons for that are: You can’t always map GPU name to its architecture (e.g. “AMD Radeon (TM) Graphics”), Only GPUs that met a certain threshold of market share are included in Steam Hardware Survey (e.g. “Intel Arc A770” is not included), D3d12infoDB lacks information about older architectures (e.g. “GCN1/2”). But it is as good as we can get with just public data, and the remaining 87.67% is still a lot. For the same reasons, market share numbers are an underestimate. Some architectures are not even in the stats, since none of the GPUs of those architectures made it past threshold market share.

Steam Hardware Survey may be a good representation of Steam users, but it is not necessarily a good representation of your target audience.

If you develop a game that focuses on graphics, your target audience will likely drift closer to newer/higher-end hardware. On the other hand, if you are developing a simple indie game, your target audience will likely drift closer to older/lower-end hardware.

Sadly, we don’t have any public information to try quantifying this bias. However, if you do have access to some user statistics that is closer to your target audience, maybe from previous entries of a game you are working on, or from a game launcher made by a company you work at, you should definitely check that data before deciding on minimum system requirements and/or which GPU features you can use.

It may not be desirable to support GPUs that no longer get regular driver updates. If you stumble upon a driver bug on such a GPU, no one will be able to help you. Here’s a table of supported GPU Architectures by vendor.

| Vendor | Oldest supported architecture |
|---|---|
| AMD | RDNA1 |
| Nvidia | Turing |
| Intel | Xe |
| Qualcomm | X1 |

Older architectures may still get security updates, but that won’t help you with driver bugs. That said, it is not necessarily off the table to support older hardware, if you accept associated risks.

If we cross-reference those architectures with market share:

Game development is anything but a quick process. If you start developing a game right now, it can take anywhere from a few months to a decade of development time. So, it is also important to consider that conditions will change over time. Meaning that we’ll need to do our best to try to predict how exactly it will change.

We have already received some mixed signals about RDNA1/2 driver support from AMD. It was announced that [those are now in a separate driver branch](https://www.amd.com/en/blogs/2025/continued-support-for-every-radeon-gamer.html), so it is plausible that RDNA1/2 will lose driver support in coming years.

On Nvidia end, they just recently dropped support for Maxwell, Pascal, and Volta cards, so it doesn’t seem likely that Turing will lose support anytime soon.

It is harder to analyze Intel’s driver support. They dropped support for Gen 9.5 - Gen 11 GPUs in 2022. If you assume a similar timeline for end of support for Xe, support may end in 2026. On the other hand, Xe GPUs should have similar architecture to newer Xe-HPG/Xe-LPG counterparts, so it doesn’t seem likely that Intel will drop support for some of them, but not others. Yet again, if you look at features supported by Xe and Xe-HPG, they will differ a lot. Maybe those are not as similar as names suggest. So, we just can’t predict what Intel’s driver support timelines would look like.

When it comes to buying new computer parts, I can’t put it any other way: We are cooked.

If you don’t know what I’m talking about, here’s a quick recap of recent events: many PC components require memory chips; GPUs are no exception. [Only 3 companies produced 93% of those chips](https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share), while production capabilities were already quite stretched. AI created a lot of demand on top of that. Then suddenly [OpenAI bought 40% of global DRAM output](https://www.mooreslawisdead.com/post/sam-altman-s-dirty-dram-deal), and from that point it all went tumbling down: [DDR5 prices tripled](https://pcpartpicker.com/trends/price/memory/), one of those 3 companies announced that [they are killing their consumer brand that has been around for 30 years](https://www.reuters.com/business/micron-exit-crucial-consumer-memory-business-2025-12-03/), [Nvidia plan to reduce production of consumer GPUs in 2026](https://www.techpowerup.com/344177/nvidia-plans-to-reduce-rtx-50-production-by-up-to-40-in-early-2026) and due to all this [it is expected that GPU prices will also rise](https://www.techspot.com/article/3054-dram-pricing-gpu-next/).

At least it is not hard to speculate:

Just because a shiny new feature shipped doesn’t mean that it is useful in your case. If you don’t have many reflective surfaces in your game - it doesn’t make a lot of sense to spend development time and VRAM budget on raytraced reflections, even if all your users have raytracing capable GPUs.

I’m not advocating for mindlessly adopting new features or raising minimum system requirements beyond what you need. All those features are described in context that you have a good reason to use them.

All recommendations about usage (or avoidance) of any given feature are only referring to:

If you decide to require one feature from this list and increase minimum system requirements accordingly, it will affect how “expensive” would any additional feature be. For example, if you require DXR, you get Mesh Shaders for “free”, since all DXR capable hardware happens to also be Mesh Shader capable. There’s a table further down in the post that illustrates this.

Now it’s time to go over various features that you may want to use.

Let’s first look at the situation with Nvidia’s Pascal and Turing GPUs. Unfortunately, within those architectures, raytracing support is inconsistent. To keep it short, here’s breakdown:

With that information we can narrow down uncertainty window.

Support stats among all GPUs:

Among GPUs with active driver support (excluding “No data” portion), 86.62% support DXR in hardware.

And last thing to consider - DXR is something that is almost exclusive to graphics-oriented games. That means your target audience will likely be biased towards newer GPUs.

DXR Usage options:

The first thing you can clearly see from this table is that there’s pretty much 0 reason to require anything lower than 6.5, as support for it is basically ubiquitous. Which means that you pretty much always have access to a lot of nice features from SM [6.0](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.0), [6.1](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.1), [6.2](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.2), [6.3](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.3), [6.4](https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.4), and [6.5](https://microsoft.github.io/DirectX-Specs/d3d/HLSL_ShaderModel6_5.html).

To go up to [SM 6.6](https://microsoft.github.io/DirectX-Specs/d3d/HLSL_ShaderModel6_6.html) you only need to drop support for Nvidia Kepler and Intel Gen 9/9.5 GPUs, which combined have less than 2% market share. Which is worth it for any developer that works on low-level rendering code, as it gets you [Dynamic Resources](https://microsoft.github.io/DirectX-Specs/d3d/HLSL_SM_6_6_DynamicResources.html) (aka full bindless), among other additions.

To go up to [SM 6.7](https://microsoft.github.io/DirectX-Specs/d3d/HLSL_ShaderModel6_7.html) you only need to drop support for AMD GCN3 which translates to 0.05% market share. Compared to other Shader Models, additions in 6.7 are relatively minor, so we won’t describe those here. At this point, we are still covering all GPUs with active driver support.

Going up to [SM 6.8](https://microsoft.github.io/DirectX-Specs/d3d/HLSL_ShaderModel6_8.html) require you to give up 5,07% of market share, which includes *all* Intel and Qualcomm GPUs. Apart from support for Work Graphs, which require an additional feature on top of SM 6.8, it only adds some minor features. Most notable of those is [Extended Command Information](https://microsoft.github.io/DirectX-Specs/d3d/HLSL_ShaderModel6_8.html#extended-command-information). Developers that are more familiar with Vulkan or OpenGL may consider it a basic feature, but for years DirectX 12 developers passed those values manually. So, this is not as major of a feature as some of you may think.

Shader Models to consider for minimum system requirements:

Mesh Shader support is almost identical to hardware DXR support, with only difference is that GTX 16xx cards do support Mesh Shaders, but don’t have hardware DXR support.

Support stats among all GPUs:

Among GPUs with active driver support (excluding “No data” portion), 95.95% support Mesh Shaders.

Primary use-case for Mesh Shaders is optimization for scene geometry rendering. If you have a lot of highly detailed geometry, you can get some nice performance improvements. On the other hand, you won’t benefit much from Mesh Shaders if geometry in your game is not too complex.

Mesh Shaders usage options:

Enhanced barriers are different from other features on this list. If you decide to use Enhanced barriers, you replace one of the core concepts of D3D12 used throughout your renderer. As for benefits, despite not giving you any new exciting opportunities, it makes development experience nicer and gives you a little bit of extra performance.

As for market share, most GPUs have support. If you take GPUs with active driver support - only Intel’s Xe lacks Enhanced barriers, generation that only has iGPUs. If you go beyond that, you also lose AMD GCN *, AMD Vega, Intel Gen * GPUs.

Support stats among all GPUs:

Among GPUs with active driver support (excluding “No data” portion), 97.62% support Enhanced Barriers, you only lose Intel’s Xe architecture, which only consists of iGPUs.

Enhanced Barriers usage options:

VRS is another interesting feature. Its only use case is optional optimization - if you implement VRS usage in any given pass, it is trivial to also support completely disabling it.

Support stats among all GPUs:

Support stats among GPUs with active driver support (excluding “No data” portion):

We will only focus on Tier 2. Tier 1 does not allow you to use image-based shading rate selection, which is what you’ll need to selectively apply lower rate in low frequency areas of your image. Tier 1 only hardware is also very small portion of the user base.

Interesting property of VRS is that its usefulness scales with resolution. In Mesh Shaders part I argued that optimizations that leave out older hardware are not as useful, as it is older hardware that needs most optimization. But users of older hardware will run at lower resolution, so it wouldn’t have improved performance as much. It is newer hardware that will run your game at higher resolutions and can benefit more from VRS.

However, if your game uses upscaling, VRS is probably not for you. When using upscaling, you are lowering your render resolution, so VRS won’t give you as much performance improvement, but will still require a lot of complexity related to the implementation. But even bigger problem is that some upscalers will not produce good results when using them together with VRS. This topic is not well covered by available resources, but CoD force disabled VRS if you use any upscaler or sharpening other than TAA.

So, whether VRS is worth it or not depends on the game:

Sampler Feedback has been barely used since its introduction. The closest thing to real-world example I was able to find is Half-Life 2 RTX, which is a tech demo, not a full game. However, in that tech demo, you can see how [Sampler Feedback Streaming can save a lot of VRAM](https://www.youtube.com/watch?v=NfgJJbtfjs8). We will only consider this streaming use case, since 2nd most prominent use case for Sampler Feedback - Texture Space Shading, got even less traction.

Support stats among all GPUs:

Support stats among GPUs with active driver support (excluding “No data” portion):

Difference between Tier 1.0 and 0.9 is in what kind of samplers are compatible with sampler feedback - 0.9 is limited to samplers that use WRAP or CLAMP address modes and cover whole resource (can’t specify MIP or TextureArray range or use Min LOD Clamp). In practice those limitations shouldn’t matter as you are likely to use samplers compatible with 0.9 anyway, so you probably don’t need Tier 1.0.

Saving VRAM may not sound like a particularly interesting feature, but there’s more to it. We are currently in the middle of memory shortage - it is just a matter of time until high VRAM GPUs become even more unaffordable than they already are. Secondly, if you are going to use DXR, you will need a lot of VRAM for acceleration structures. And since every DXR capable GPU also has Sampler Feedback support of at least Tier 0.9, this does sound like a reasonable strategy to counteract increased VRAM usage due to DXR.

However, instead of using hardware Sampler Feedback, you can always manually implement something similar. The benefits of such approach are:

So, most games would want to skip Sampler Feedback as a hardware feature.

This feature is very new, with [release of Tier 1.0](https://devblogs.microsoft.com/directx/d3d12-work-graphs/) and [preview for Tier 1.1 with Mesh Nodes](https://devblogs.microsoft.com/directx/d3d12-mesh-nodes-in-work-graphs/) having come out just last year (2024).

Support stats among all GPUs:

Support among GPUs with active driver support (excluding “No data” portion) is 74.1%.

Mesh Nodes from Tier 1.1 is basically a mesh shader that you can run inside work graph to perform rasterization/shading work. So, it is reasonable to expect that all GPUs with Tier 1.0 support will also support Tier 1.1, since they all also support Mesh Shaders.

Work Graphs are very new and allow implementing wildly different algorithms. Everyone’s use case will be different. We don’t even have any good examples of Work Graph usage in shipped games, except Unreal Engine’s optimization for Nanite. But we’ll try our best to estimate how worth may it be.

Work Graphs usage options:

Here’s [Support for GPU Upload Heaps](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS16.GPUUploadHeapSupported), but before you check the data, here’s a disclaimer:

For GPU Upload Heaps to be supported on any given system, ReBAR must be enabled in UEFI settings and user must run on Windows 11 24H2 or later. Older GPUs may also lack support from driver, which also can prevent you from using GPU Upload Heaps. Unfortunately, we don’t have good data for that. D3d12infoDB is a community driven database - we can’t know whether any given report lacks support due to driver or due to ReBAR not being enabled. So, entry in that table may be false negative.

You also can’t reason whether any given user has support for GPU Upload Heaps based on GPU model alone - user may have RTX 5090 but lack support for GPU Upload Heaps due to disabled ReBAR.

There is an exception for iGPUs, as they can achieve the same behavior as GPU Upload Heaps by using custom heaps without reliance on any new features. But that doesn’t change the overall picture.

So, it is hard to reason about GPU Upload Heaps as-is, but it is not even the worst thing. Let’s say you want to require GPU Upload Heaps. Your minimum supported GPU does support GPU Upload Heaps. You specifically call out that GPU Upload Heaps are required and that users must enable ReBAR in system requirements. You will still face a lot of issues:

If you think that it won’t affect many users, remember - [“Even when they’re trying to compensate for it, experts in anything wildly overestimate the average person’s familiarity with their field.”](https://xkcd.com/2501/)

So, the only real option you have - using GPU Upload Heaps as an optional optimization. Fortunately, implementing fallback for GPU Upload Heaps is easy, so it is generally worth it to use.

One more suggestion I do have is that for streaming, you may want to use DirectStorage instead of manually using GPU Upload Heaps.

Not exactly a feature, but worth mentioning here, as there are a few misconceptions worth clearing up:

So, there’s really no reason not to use it, plus you’ll get additional improvements in future updates.

Unfortunately for console developers, neither Nvidia nor Intel supports it. Support is 6.69% among all GPUs, and 8.89% among GPUs with active driver support (excluding “No data” portion). So, you can’t require support for this.

You can use it for AMD specific optimizations - changing format of some textures is trivial, so even if a few users will benefit from this, such efforts may be worth it. Plus, console ports can copy over existing optimizations.

Here’s list of features that don’t require much explanation or analysis:

[Native 16-bit shader operations](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS4.Native16BitShaderOpsSupported) - Tier 3 on all GPUs with active driver support. For Older GPUs support is not great though.

[SV_Barycentrics](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS3.BarycentricsSupported) - Support is very similar to DXR, except that Turing 16xx has support and Intel’s Xe-HPG / Xe-LPG does not.

[Conservative rasterization](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS.ConservativeRasterizationTier) - Tier 3 on all GPUs with active driver support, which also means all DXR capable GPUs have Tier 3 as well. For older hardware support is neither perfect, nor terrible.

[Resource Heap](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS.ResourceHeapTier) - Tier 2 on all GPUs with active driver support, except for some inexplicable reason Intel Xe-HPG, which is only Tier 1. Nvidia GPUs of Pascal and older architectures are also only Tier 1. Tier 1 limitations are not that bad though, just slightly annoying.

[Double precision float shader operations](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS.DoublePrecisionFloatShaderOps) - No support on some Intel GPUs and all Qualcomm GPUs, but in general support is still quite broad. Probably not something games would want to use though, since performance won’t be great.

[Int 64 shader operations](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS1.Int64ShaderOps), [Casting fully typed formats](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS3.CastingFullyTypedFormatSupported), [Wave operations](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS1.WaveOps) - Supported on all reasonable hardware.

[Resource binding](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS.ResourceBindingTier) - Tier 3 on all reasonable hardware.

[PS specified stencil reference value](https://d3d12infodb.boolka.dev/CanIUse.html?q=D3D12_FEATURE_DATA_D3D12_OPTIONS.PSSpecifiedStencilRefSupported) - No support on Nvidia, almost 100% support on everything else.

Finally, these tables will help you visualize features overlap

| AMD | |||
|---|---|---|---|
| Architecture | Market Share | Cumulative Market Share | Added Features |
| GCN3 | 0.05% | 0.05% | SM 6.6 |
| GCN4 | 2.26% | 2.31% | SM 6.7 |
| Vega | 0.80% | 3.11% | 16-bit Shader Ops |
| RDNA | 1.04% | 4.15% | SM 6.8 Enhanced Barriers |
| RDNA2 | 3.93% | 8.08% | Mesh Shaders DXR VRS Tier 2 Sampler Feedback Tier 1.0 R9G9B9E5 RTV/UAV |
| RDNA3 | 2.60% | 10.68% | Work Graphs |
| RDNA4 | 0.16% | 10.84% |

| Nvidia | |||
|---|---|---|---|
| Architecture | Market Share | Cumulative Market Share | Added Features |
| Fermi | 0.01% | 0.01% | SM 5.1 |
| Kepler | 0.17% | 0.18% | SM 6.5 |
| Maxwell1 | 0.46% | 0.64% | SM 6.8 Enhanced Barriers |
| Maxwell2 | 0.66% | 1.30% | |
| Pascal | 6.23% | 7.53% | |
| Turing 16 | 7.01% | 14.54% | Mesh Shaders VRS Tier 2 Sampler Feedback Tier 0.9 16-bit Shader Ops |
| Turing 20 | 5.49% | 20.03% | DXR |
| Ampere | 21.76% | 41.79% | Work Graphs |
| Ada | 22.40% | 64.19% | |
| Blackwell | 8.83% | 73.02% |

| Intel | |||
|---|---|---|---|
| Architecture | Market Share | Cumulative Market Share | Added Features |
| Gen7.5 | 0.21% | 0.21% | SM 5.1 |
| Gen9 | 0.35% | 0.56% | SM 6.5 |
| Gen9.5 | 1.24% | 1.80% | 16-bit Shader Ops |
| Gen11 | ~0% | 1.80% | SM 6.7 VRS Tier 1 |
| Xe | 1.96% | 3.76% | Sampler Feedback Tier 0.9 |
| Xe-HPG | ~0% | 3.76% | Mesh Shaders DXR VRS Tier 2 Enhanced Barriers |
| Xe-LPG | ~0% | 3.76% | |
| Xe2-HPG | ~0% | 3.76% | Sampler Feedback Tier 1.0 |

| Qualcomm | |||
|---|---|---|---|
| Architecture | Market Share | Cumulative Market Share | Added Features |
| 8cx 3 | ~0% | 0.00% | SM 6.2 VRS Tier 1 |
| X1 | 0.05% | 0.05% | SM 6.7 VRS Tier 2 16-bit Shader Ops Enhanced Barriers |

Now we are ready to reason about what you should use for minimum system requirements. We’ll pick different kinds of games and try to pick something suitable in each case.

The most practical way to do that is going over architecture tables you just saw and figuring out what you can get without losing too much of a potential audience. This is a strategy we’ll use for following examples.

Just a reminder, we are still discussing it in context of just features. We don’t consider performance and VRAM amounts of GPUs. You may pick minimum requirements in a similar method and then increase it to something that runs your game well.

Chosen minimum requirements are:

Logic is:

Resulting potential users’ stats:

I see 2 different strategies you can choose, so let’s look separately at each one

Minimum requirements are:

Logic is:

Resulting potential users’ stats:

The drawback of this strategy is that we lose a large portion of potential users by dropping support for Nvidia Pascal. Hence, Strategy 2.

Minimum requirements are:

Logic is:

Resulting potential user stats:

Drawback of this strategy is that you now need to accept risks associated with GPUs that lack driver support. You also lose 16-bit Shader Ops, which is a quite useful feature.

Minimum requirements are:

Logic is:

Resulting potential user stats:

However, those stats are not representative of what we’ll see in 2028. We should see increase in percentage of users that can run the game, but with current GPU market it is hard to say how much exactly.

We are getting to a breaking point where it is starting to become reasonable to require support for new GPU features. Hopefully this post helps you to understand value and cost of each of them. Maybe even some of you will be able to sell an idea to increase or lower system requirements for a game you are working on.

If you find this post useful, or have any feedback, please let me know. You can find me on Twitter (self-proclaimed X) as [@dmytro_bulatov](https://twitter.com/dmytro_bulatov). Other contact information can be found on [boolka.dev](https://boolka.dev/). If there’s a demand for this kind of analysis, I could make it into a yearly thing.

In writing this post I also realized what kind of data is valuable to developers when deciding on hardware support. So, expect relevant updates to D3d12infoDB.

And finally, if you have access to older or hard to find GPUs, like GCN1/2, please submit a report to D3d12infoDB via [latest build of D3d12infoGUI](https://github.com/Devaniti/D3d12infoGUI/releases/latest).