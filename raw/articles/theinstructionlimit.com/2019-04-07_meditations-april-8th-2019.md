---
title: Meditations – April 8th 2019
url: https://theinstructionlimit.com/meditations-april-9th-2019
author: Author Renaud Bédard
published: '2019-04-07'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

![](../../assets/1171c325e9b8f894.png)

In March 2018, I attended [Train Jam](https://trainjam.com/) and chatted there with [Rami Ismail](https://ramiismail.com/) about a project he was starting up : contemplative, 5-minute games released day-by-day. I thought it was neat, but I didn’t commit to anything since my time for side-projects is super limited.

In late November 2018, I was asked by [Jupiter Hadley](https://twitter.com/Jupiter_Hadley) whether I’d like to contribute to a super secret project she and others were working on… I asked about details, and realized it’s the same thing Rami pitched me months earlier : [Meditations](https://meditations.games/)! Jupiter explained that I should spend no more than 6 hours on the project, and submit it before December 14th 2018. The timing worked out, so I decided to give it a go.

I picked April 9th as the date (it was moved back 1 day to April 8th after the fact), and started browsing my Google Photos to see what the heck happened on an April 9th in my life… 2013 jumped out as a memorable one. My then-girlfriend (now wife) MC and I went to [Nara, Japan](https://goo.gl/maps/LPaFo11SFtD2) where we met [bowing deer](https://www.youtube.com/results?search_query=nara+bowing+deer) and strolled the city on a beautiful sunny day. The cherry trees were at the peak of their flowering time, and they shed pink petals everywhere.

![](../../assets/f4bc8dbd2759821d.jpg)

So I figured I’d do a little vignette game with a tree, falling petals, and heavy emphasis on the soundscape. I wanted it to feel vaguely like [Proteus](https://en.wikipedia.org/wiki/Proteus_(video_game)), with a [Boards of Canada](https://www.youtube.com/watch?v=MWh-2l0Hv0Y) kind of musical vibe. Other stylistic references I had in mind : [Devine Lu Linvega](https://twitter.com/neauoire)‘s [Kanikule](https://wiki.xxiivv.com/#kanikule), and [@ktch0](https://twitter.com/ktch0)‘s [Places](http://ktch0.tumblr.com/).

I asked my friend and colleague [Rodrigo Rubilar](https://soundcloud.com/rodrigo-rubilar) whether he’d like to do sound design and music. I originally planned to do it myself with my limited audio gear, but I was excited to work with him on a small project like this, and he’d produce quality results 10 times faster than I could! We jammed an afternoon on an ambient track with a few layers, and one-shot sounds for the leaves hitting the ground.

At the same time I started hacking at a fractal tree generator in Unity. It’s actually the first time I’d tried to write one, so it was interesting to see how the simplest algorithm could apply to 3D, with some randomness injected into it. I exposed a ton of parameters, and played with them until I was happy with the result.

![](../../assets/f6728fe9b2d824ba.png)

Then I started thinking about the petals, and how I wanted them to move in the air. I started with a basic Unity particle system and wind zones, but I suck at authoring those and I could never get the look I wanted. So I resorted to manually updating the petals with simple physics. But then I wanted a lot of petals… *thousands *of them. So I started toying around with Unity 2018’s [job system](https://docs.unity3d.com/Manual/JobSystem.html).

Optimization ended up being the most interesting engineering aspect of the project for me, and the biggest time-sink. There is *no way* I respected the development time limit of 6 hours (probably spent more than 40 hours on it), but it was hard to let go. So I’d like to at least document what I ended up doing and why.

**If you just want to look at the code, it’s ****all here****.**

## Jobified update

I ended up with [a single job](https://github.com/renaudbedard/meditations-april-9th/blob/master/Assets/Scripts/FractalTree.cs#L570) that does most petal-related work :

- Update physics based on wind parameters
- Detect ground collisions
- Detect player interactions (you can rise petals from off the ground by walking near them)

I want to update all the active petals every frame, so I schedule the job in the earliest `Update`

callback (you can tweak that using [Script Execution Order](https://docs.unity3d.com/Manual/class-MonoManager.html)), and complete it in `LateUpdate`

.

I wanted petals hitting the ground to trigger sounds, so the naive way of making this happen in Unity (and my initial approach) is to have one `GameObject`

per petal, with an `AudioSource`

component. The `AudioSource`

s don’t have to be enabled all the time, only when they’re playing a sound, but that does mean that I have to update their `Transform`

so that the sound plays at the right 3D position.

![](../../assets/36f06f7c43988a76.png)

It’s possible to access and update `Transform`

s from within a job by implementing [ IJobParallelForTransform](https://docs.unity3d.com/ScriptReference/Jobs.IJobParallelForTransform.html), and pass the transforms to the job using a

[. A major gotcha with the current version of the job system is that only root](https://docs.unity3d.com/ScriptReference/Jobs.TransformAccessArray.html)

`TransformAccessArray`

`Transform`

s will be assigned to different threads. I originally had petals as child of an empty game object just for grouping, but then my job was using a single worker thread. Reading [this forum post](https://forum.unity.com/threads/ijobparallelfortransform-15000-transforms-executed-on-single-job-thread-any-hints.537723/)explained it, but it’s still baffling to me, and makes for a pretty hideous

*Hierarchy*tab.

I ended up not using `Transform`

s for petals at all, but more on this later.

One thing that I found interesting is how one returns data from the job to the game code. For instance, I want to know which petals should trigger a sound by returning a list of petal indices that touched the ground. You can declare a field in the job as

(which is part of the [NativeQueue](https://docs.unity3d.com/Manual/JobSystemNativeContainer.html)<int>.Concurrent*Collections* package) , and enqueue data as the job runs on multiple threads. From the calling site, you need a `NativeQueue<int>`

to be created, but when it’s passed to the job instance, you need to use the `.ToConcurrent()`

method to make it usable. Then, once the job is complete, you can use `.TryDequeue()`

to extract elements from it. Works great!

I enabled [Burst](https://docs.unity3d.com/Packages/com.unity.burst@0.2/manual/index.html) on my job very naively, and spent zero time optimizing the generated code. I did take care of the basics : make sure to mark job fields appropriately as [ [ReadOnly]](https://docs.unity3d.com/ScriptReference/Unity.Collections.ReadOnlyAttribute.html) and

[, use the SIMD-capable](https://docs.unity3d.com/ScriptReference/Unity.Collections.WriteOnlyAttribute.html)

`[WriteOnly]`

[package whenever possible. In the end, the job runs way faster than I need, so I just moved on.](https://github.com/Unity-Technologies/Unity.Mathematics)

`Unity.Mathematics`

Burst had a dramatic effect on the job’s performance. Here’s a profile of the same code running on the same system, with Burst compilation toggled off and on. The biggest noticeable difference is that `LateUpdate`

does not need to wait on jobs at all when they are Burst-enabled, which means it runs fully in parallel!

![](../../assets/23c1d7dcfa7ca876.png)

![](../../assets/5384887bd640414e.png)

**with**

**Burst**enabled : 0.05ms

## Rendering

*Note : even though I’m using Unity 2018.3, I did not use the Scriptable Render Pipeline in this project, so the following probably only applies for the legacy rendering pipeline.*

I initially had every petal `GameObject`

with a `MeshRenderer`

, a simple quad mesh, and the [Unity Standard Shader](https://docs.unity3d.com/Manual/shader-StandardShader.html) with [instancing](https://docs.unity3d.com/Manual/GPUInstancing.html) turned on. It definitely worked, but Unity spent a lot of time in culling and batching, and I thought I could do better… by short-circuiting it completely.

It might sound like rendering everything all the time is a bad call, but in this game, the worst-case scenario of all petals being visible at once is the very first thing you see. Might as well make it a fast general case!

One way to draw objects manually is to use [Command Buffers](https://docs.unity3d.com/Manual/GraphicsCommandBuffers.html). By specifying a mesh, a material and a bunch of transformation matrices, you can use the

method to draw up to 1022 (that number I got empirically, but it appears to be undocumented) instances at once, in a single call. There is no renderer on the game objects themselves, so Unity acts as if they don’t exist, apart from issuing draw commands.[DrawMeshInstanced()](https://docs.unity3d.com/ScriptReference/Rendering.CommandBuffer.DrawMeshInstanced.html)

My petal update job’s final step is then to bake the petal’s current position, rotation and scale into a 4×4 transformation matrix, so that I can use them in my command buffers later. But there it gets annoying :

`DrawMeshInstanced()`

takes a`Matrix4x4[]`

, nothing else, so we’ll have to copy our`NativeArray`

to a managed array.- We have to respect the batch size of 1022, so we have to use

to take 1022-element slices of our[NativeSlice](https://docs.unity3d.com/ScriptReference/Unity.Collections.NativeSlice_1.html)`NativeArray`

.

copies element by element, and it’s very slow.[NativeSlice.CopyTo()](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Runtime/Export/NativeArray/NativeSlice.cs#L244)

I found [a faster CopyTo implementation on the Unity forums](https://forum.unity.com/threads/allow-setting-mesh-arrays-with-nativearrays.536736/#post-3541836) which [I slightly modified](https://github.com/renaudbedard/meditations-april-9th/blob/master/Assets/Scripts/NativeSliceExtensions.cs#L8), and it does perform much better, but it’s a lot of moving data around for no reason. I wish that `NativeSlice`

s were directly usable with command buffers.

![](../../assets/11a20709f7fc3a7c.png)

I end up with two very similar command buffers : one for depth rendering inside shadow-maps and for the camera’s depth pass, and one for regular opaque rendering.

The depth rendering command buffer uses the

pass from the [ShadowCaster](https://docs.unity3d.com/ScriptReference/Rendering.PassType.ShadowCaster.html)*Standard* shader, and hooks to the

event on lights as well as the [AfterShadowMapPass](https://docs.unity3d.com/ScriptReference/Rendering.LightEvent.AfterShadowMapPass.html)

event on the camera. I needed the camera depth pass for SSAO using [AfterDepthTexture](https://docs.unity3d.com/ScriptReference/Rendering.CameraEvent.AfterDepthTexture.html)[Keijiro Takahashi’s MiniEngineAO Unity implementation](https://github.com/keijiro/MiniEngineAO).

## Triggering audio

As I hinted to earlier, I ended up ditching `GameObject`

s for petals entirely. The only reason I originally kept them around (and updated at all times) was for audio, but it’s a lot of data shuffling just for sporadic sound triggers, so I opted for a simple audio trigger [object pool](https://github.com/renaudbedard/meditations-april-9th/blob/master/Assets/Scripts/Pool.cs) instead.

I pre-initialize 1500 (again, empirical) dummy `GameObject`

s with a disabled `AudioSource`

component that lay dormant in the pool until an audio event happens. At that point, I take one from the pool, enable audio, position it at where the impact happens, and play the audio clip. There is no update cost to having them around otherwise, and they are disabled & returned to the pool when the sound playback is complete.

Petals are then strictly represented by a data structure that lives in a `NativeArray`

, not by a `GameObject`

. And the update job becomes a

, mutating elements of that array. Neat![IJobParallelFor](../../assets/bd002da49eb22925.img)

You may wonder how dramatic a performance difference this makes. So here’s a comparison, taken from the same Macbook, of the CPU time spent only scheduling jobs between the version using Transforms and the version without. Something about how Unity handles transform access to a job definitely incurs sizeable overhead.

![](../../assets/73f72e8ce6c882c8.png)

`Transform`

s (1.79ms spent scheduling jobs)![](../../assets/47956db51b0ff995.png)

**Without**

**Transform**

**s**(0.03ms spent scheduling jobs)

## Bending the tree

When I had the petals mostly working well, it still felt strange that the tree didn’t animate at all. I wanted branches to sway in the wind, and I figured I could make that happen easily in its vertex shader.

It turned out to be a lot trickier than I expected, for a few reasons :

- The tree is generated as a single baked mesh, there is (ironically) no tree structure to it. No great reason for this apart from lack of foresight.
- The petals aren’t really attached to branches, their position is just set to the endpoint of branches when generating the tree.

To make the smaller branches bend but not the trunk, I set a *bendability* parameter during generation (how far away from the trunk that vertex is) in the texture coordinates.

![](../../assets/ba2dda3e2b43d25c.png)

*bendability*parameter for a generation

I then define the a bend axis perpendicular to wind direction, a bend angle dependent on wind force, and a *shake* factor which is just a bunch of low-frequency and high-frequency sine functions multiplied together, to make it feel a bit more noisy & organic.

These variables are mapped to shader globals, and I used [keijiro’s angle-axis to float3x3 HLSL function](https://gist.github.com/keijiro/ee439d5e7388f3aafc5296005c8c3f33) to apply this in the vertex shader of my tree. So far so good!

Where it got tricky is for petals. I need to differentiate when they’re attached or detached, so I can apply the wind bending selectively. I ended up using a [ MaterialPropertyBlock](https://docs.unity3d.com/ScriptReference/MaterialPropertyBlock.html) to have per-instance data (a single float) encoding this state.

In the vertex shader (which is part of a simple [Surface Shader](https://docs.unity3d.com/Manual/SL-SurfaceShaders.html)), it took me a minute to understand how to do world-space transformations on vertex data. The simplest way I found was to transform the vertex to world-space, and take it back in object-space when I’m done. Not super efficient… ¯\_(ツ)_/¯

![](../../assets/9f543ec7f6d45a40.png)

[Rider](https://www.jetbrains.com/rider/)

On the application-side, I did use a `NativeArray<float>`

for instance data, but I’m not sure it’s the easiest way to go about it. I don’t actually read from or write to it from within my update job, it’s all happening in the regular `Update()`

. It allowed me, however, to re-use `Slice()`

and `CopyToFast()`

to make 1022-sized chunks for rendering.

One thing to note : unlike with the draw arrays, `MaterialPropertyBlock`

s cannot be reused for multiple batches, so I create all the ones I need up-front and iterate through them.

Another thing I realized, is that I need to apply the exact same function I used in the vertex shader to my petals the moment they are detached from the tree. This effectively bakes the tree’s bend at that moment in time into their transform, and avoids them visually warping around as they are detached.

In the end it still looks kinda stiff, but it’s better than the cement tree I started with.

## Closing thoughts

I’m super happy with the final result. It’s relaxing, soft, yet sometimes surprisingly intense. It ended up feeling a lot more mournful than I expected, but I’m fine with that. I really enjoy the visual transition from a mess of pink sheets of paper to a menacing, pointy web.

But since everything was done in a rush, there’s some things I wish I’d done differently.

In Feburary 2019 I stumbled upon this rather excellent tree by Joe Russ, developer on Jenny LeClue :

It made me realize that my tree shape and animation could be so much better. Having the branch splits be less even, more jagged and well, *tree-like*, would add a lot. And by having the branches hierarchically laid out, I could have bent the sub-trees and produce a much more convincing wind swaying effect.

Spending so much time on performance optimization made me wonder if doing a whole forest of trees, instead of a single one, would be possible at all. Wouldn’t that be neat? But it brought additional headaches that I didn’t want to deal with.

But there’s something to be said about making a small thing, with a tiny scope, a reasonable amount of polish, and putting it out there. Just the fact that I was excited enough about making this that I convinced Rodrigo to tag along made it worthwhile.

So big thanks to Rami, Jupiter and everyone involved in [the Meditations project](https://meditations.games/) for making this happen. And thanks as always to my wife MC for humoring me while I spent precious evenings & weekends time endlessly debugging my stupid tree. ♡

#### Addendum : So what about ECS?

You might be wondering why I went straight with the Job System but didn’t use [Entities](https://docs.unity3d.com/Packages/com.unity.entities@0.0/manual/index.html), since they were showcased in the [Megacity demo](https://unity.com/megacity) and Unity is really selling it as The Way to do massive amounts of objects with acceptable performance.

I don’t really have a good answer to this, except that I was short on time and was familiar with the idea of data parallelism, but not so much with ECS… and didn’t want to spend time learning how to use ECS properly. And I’m stubborn and will go down a path I’ve set for myself even if it’s a bad idea.

There’s good chances that using ECS is the best way to do what I was trying to achieve, but I didn’t go down that path yet. It would be interesting to revisit the project and do it that way; maybe I will!

I’m also curious to hear from people who have tried Unity’s ECS. Would it really make this easier to design? Would the rendering portion be simplified? Let me know!