---
title: Batching techniques in Unity
url: https://cmwdexint.com/2018/06/19/batching-techniques-in-unity/
author: Ming Wai Chan
published: '2018-06-19'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

Last update: Nov 2024

Update: This image is too old so please look at the **comparison table** below instead

![batchingtechniques](../../assets/4b526c6bfa4e4a53.jpg)



Static Batching | Dynamic Batching | GPU Instancing | SRP Batcher | GPU Resident Drawer/ BatchRendererGroup | |
Built-in RP support | Yes | Yes | Yes | No | Same as SRP Batcher |
Universal RP (URP) support | Yes (Enable checkbox in Player Settings) | Yes (Need to disable SPR batcher on pipeline asset, and enable Dynamic Batching checkbox) | Yes (Need to disable SRP batcher,
| Yes | Yes (Forward+ only) |
| Works on static objects? (the “ Batching Static” flag on MeshRenderer component) | Yes | No | No (if Static batching is used, instancing will be turned off) (
| Yes | Same as SRP Batcher |
Works on dynamic objects? | No | Yes | Yes | Yes | Same as SRP Batcher |
Objects can use different meshes? | Yes (Different meshes are combined into a big mesh) | Yes | No | Yes | Same as SRP Batcher |
Objects can use different materials? | No | No | No | Yes (Be-aware of shader variant) | Same as SRP Batcher |
Objects can use different shaders? | No | No | No | No | Same as SRP Batcher |
Objects can have different property values set by script?(Per-object / Per-instance properties e.g. color) | No | No | Yes (use MaterialPropertyBlock) | Yes (setup different materials) | Same as SRP Batcher |
Works on SkinnedMeshRenderer | No | No | No | Yes | No |
| Typical use case | Useful for larger unique meshes that will share the same material. Reduce draw calls (increase CPU performance). (
| For very low-poly dynamic objects that share the same material, e.g. a quad mesh. Reduce draw calls. Useful for platforms and graphics APIs that do not support GPU instancing, e.g. very low-end devices (
| Useful for drawing objects that appear repeatedly (same mesh). Reduce draw calls (increase CPU performance). (
| Useful if you have many different Materials that use the same Shader. Speeds up CPU rendering without affecting GPU performance. (
| Render a large number of environment objects where using individual GameObjects would be too resource-intensive. For example, procedurally-placed plants or rocks. (
Reduces the number of draw calls and frees CPU processing time. (
|
| Good things don’t come for free | Increase memory / storage usage (
| Has CPU overhead (decrease CPU performance if only small amount of objects are batched) (
| Has overhead on both CPU & GPU (
A bit slower on GPU (
| N/A (This is running by default whenever you use URP/HDRP) | Require platform / graphics API that supports compute. (
Make sure to profile performance as it only benefits if you have enough instances to take advantages from it. Player build time might be much longer as all DOTS_INSTANCING shader variants will be kept and thus will be compiled into player build. |
| Resources |
|

[Minimal custom shader](https://docs.unity3d.com/6000.0/Documentation/Manual/urp/writing-shaders-urp-unlit-color.html)example[Minimal custom shader](https://github.com/Unity-Technologies/EntityComponentSystemSamples/blob/master/GraphicsSamples/URPSamples/Assets/SampleScenes/6.%20Misc/SimpleDotsInstancingShader/SceneAssets/CustomDotsInstancingShader.shader)exampleBatchRendererGroup used to only work for fast rendering of Entities (DOTS / ECS) only, that’s why it’s shader keyword is named “DOTS_INSTANCING”.

Rendering of Entities is supported by the Entities Graphics package.

Entities Graphics used to call “Hybrid Renderer” that’s why the term “hybrid” remains somewhere.

Therefore:

Rendering Entities with BatchRendererGroup = Entities Graphics

Rendering GameObjects with BatchRendererGroup = GPU Resident Drawer

More nice information : [The Ultimate Guide to Draw Call Batching in Unity 2020+ by Ruben Torres Bonet](https://www.gamasutra.com/blogs/RubenTorresBonet/20200114/356520/The_Ultimate_Guide_to_Draw_Call_Batching_in_Unity_2020.php)[https://forum.unity.com/threads/srp-batcher-and-gpu-instancing.833362/#post-5521216](https://forum.unity.com/threads/srp-batcher-and-gpu-instancing.833362/#post-5521216)

Hello, so I can use SRP batching on a realtime lit scene, but is there a way to use SRP batcher with a baked lit scene? I need srp batcher’s different material and mesh batching features but its still slow on dynamically lit scenes on low end devices. I’d love to know what are your suggestions on that.

LikeLike

Yes SRP batcher does work on baked scene.(URP working fine for me)

LikeLike

I’m using a slightly modified version of simple lit shader and I can’t see srp batches on frame debugger when I use a baked scene. No problem when using realtime data.

Do you mean the static batcher works with the SRP batcher on baked scenes and handle those baked lit meshes? or am I doing something wrong with my custom implementation so that I can not get SRP batches?

LikeLike

Hi Chino, this is indeed a regression bug on the SimpleLit shader.

It will be fixed soon. Thanks for bringing up the issue!

Just double checking, are you using URP 10.x.x versions?

LikeLike

Hello, oh! Thank you for the valuable information. I was doing sanity checks to understand the problem but couldn’t figure it out. I’m using URP 7.3.1 with Unity 2019.4.19f1. But I’ll give it a go with the latest version of URP too. Thanks.

LikeLike

Sorry for not being clear.

Just checked that the bug happens on URP 10.x.x, but URP 8.1.0,8.2.0,7.3.1 are fine.

To know whether a shader is SRP batcher compatible, you can select the shader on ProjectView, and look at the inspector.

![](../../assets/3609a02df12772d5.png)


Since on my Win laptop SimpleLit is SRP batcher compatible on Unity 2019.4+URP 7.3.1, does it behaves the same on your machine? If SimpleLit is fine but the custom shader isn’t then we can tell something is wrong on the custom shader.

LikeLike