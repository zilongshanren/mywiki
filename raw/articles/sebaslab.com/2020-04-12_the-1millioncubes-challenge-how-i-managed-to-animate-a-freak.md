---
title: 'The #1Millioncubes challenge. How I managed to animate a freakload of cubes
  on windows using Unity - Seba''s Lab'
url: https://www.sebaslab.com/the-1millioncubes-challenge-how-i-managed-to-animate-a-freakload-of-cubes-on-windows-using-unity/
author: Sebastiano Mandalà
published: '2020-04-12'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

### 20/03/2023 update

I wrote a new demo that doesn’t need to use GPUInstancer. [Code is now available on github.](https://github.com/sebas77/MillionsCubes) Note that I also updated the code to use **GraphicBuffers **instead than **ComputeBuffers**.

For the game I am currently developing, [Gamecraft](https://store.steampowered.com/app/1078000/Gamecraft/), we are using Svelto.ECS for the game logic, Unity ECS for the physic and [GPUInstancer](https://assetstore.unity.com/packages/tools/utilities/gpu-instancer-117566) compute shader pipeline for the rendering. I have never had the time to benchmark the UECS rendering pipeline against the GPUInstancer one, mainly because I decided directly to use GPUInstancer, as its performance even on low-end GPUs (read intel HD4000) is astonishing.

Recently, on twitter, I have been asked if it was feasible to move 1 million 3D objects. I already knew that GPUInstancer wouldn’t break a sweat, but I also knew from my previous experiments that uploading from the CPU to the GPU 1 million matrices would have been impossible to use practically.

With GPUInstancer you are not supposed to update ALL the objects, but only the ones that actually moves, which usually are less. However knowing what the bottleneck is, I wondered if it was possible to upload the data to the GPU asynchronously or in any other way.

It turns out that Unity 2020 introduced two new **ComputeBuffer **methods, called **BeginWrite **and **EndWrite**. This sounded exactly what I needed to make this experiment work!

Let’s see what happens before and after using these methods. This is the entire code used to create the demo as seen in the tweet:

//#define OLD_WAY using System; using GPUInstancer; using Unity.Burst; using Unity.Collections; using Unity.Collections.LowLevel.Unsafe; using Unity.Jobs; using Unity.Mathematics; using Unity.Profiling; using UnityEngine; public class Bootstrap : MonoBehaviour { static readonly int numberOfObjectsPerSide = 1000; static readonly int totalObjects = numberOfObjectsPerSide * numberOfObjectsPerSide; // Start is called before the first frame update void Start() { _manager = FindObjectOfType<GPUInstancerPrefabManager>(); var prototypeGameObject = Resources.Load<GameObject>("Cube"); _prefabPrototype = _manager.DefineGameObjectAsPrefabPrototypeAtRuntime(prototypeGameObject); var matrices = new Matrix4x4[totalObjects]; GPUInstancerAPI.InitializeWithMatrix4x4Array(_manager, _prefabPrototype, matrices); _transformationMatrixVisibilityBuffer = _manager.GetRuntimeData(_prefabPrototype, true).transformationMatrixVisibilityBuffer; //not that nice, but it's a quick way to be able to do the EndWrite at the begin og the Update() var array = _transformationMatrixVisibilityBuffer.BeginWrite<Matrix4x4>(0, totalObjects); for (var i = numberOfObjectsPerSide - 1; i >= 0; --i) for (var j = numberOfObjectsPerSide - 1; j >= 0; --j) array[i + j * numberOfObjectsPerSide] = float4x4.TRS(new float3(i * 1.5f, 0, j * 1.5f), quaternion.identity, new float3(1, 1, 1)); _then = DateTime.Now; #if OLD_WAY _array = new NativeArray<Matrix4x4>(matrices, Allocator.Persistent); #endif } #if OLD_WAY void OnDestroy() { _array.Dispose(); } #endif // Update is called once per frame void Update() { _jobhandle.Complete(); #if OLD_WAY var profilerMarker = new ProfilerMarker("SetData"); profilerMarker.Begin(); _transformationMatrixVisibilityBuffer.SetData(_array); profilerMarker.End(); #else var profilerMarker = new ProfilerMarker("SetData"); profilerMarker.Begin(); //now that we are sure that the job is complete, we can do end write and start a new write. //not sure if this is actually necessary _transformationMatrixVisibilityBuffer.EndWrite<Matrix4x4>(totalObjects); _array = _transformationMatrixVisibilityBuffer.BeginWrite<Matrix4x4>(0, totalObjects); profilerMarker.End(); #endif var nativeArray = UnsafeUtility.As<NativeArray<Matrix4x4>, NativeArray<float4x4>>(ref _array); _jobhandle = new UpdateDataJob((float) (DateTime.Now - _then).TotalMilliseconds) { array = nativeArray }.ScheduleBatch(totalObjects, 32); } [BurstCompile] struct UpdateDataJob : IJobParallelForBatch { [NoAlias] [NativeDisableParallelForRestriction] public NativeArray<float4x4> array; public UpdateDataJob(float time) : this() { _time = time * 0.001f; } public void Execute(int startIndex, int count) { for (var index = startIndex + count - 1; index >= startIndex; index--) { float j = index / numberOfObjectsPerSide; float i = index % numberOfObjectsPerSide; var y = math.sin(2 * math.PI * (i - _time) / 10); array[index] = float4x4.TRS(new float3(i * 1.5f, y, j * 1.5f), quaternion.identity , new float3(1, 1, 1)); } } readonly float _time; } DateTime _then; NativeArray<Matrix4x4> _array; GPUInstancerPrefabManager _manager; GPUInstancerPrefabPrototype _prefabPrototype; ComputeBuffer _transformationMatrixVisibilityBuffer; JobHandle _jobhandle; }

This code won’t run unless you buy the GPUInstancer plugin. As I said GPUInstancer implements most of the rendering pipeline using *Compute Shaders*, however it still relies on Unity pipeline (in this case URP) for few things, like computing the lighting. Materials and shaders are also the ones you would use normally with Unity, with some slight variations to support *Compute Buffer structured buffers*. I won’t go into details about it, if you are interested just check the extensive [GPUInstancer wiki page](https://wiki.gurbu.com/index.php?title=GPU_Instancer:GettingStarted). Just know that it’s very simple to use even for a person like me who knows almost zero about compute shaders.

The **#define OLD_WAY** would be how you normally use the plugin. However, because how slow **ComputeBuffer SetData** is, uploading 1 million matrices would make this solution unpractical. I have already suggested to the GPUInstancer authors if they can put more thoughts about the data optimizations. a 4×4 matrix may be much more than I need to upload to the GPU (for example if I just need to translate the object).

The Job uses burst to transform 1 Million cubes, Burst will do a good job (no pun intended), considering that maybe that simple math could be even optimized:

![](../../assets/ce3398dfc2d42d23.png)


![](../../assets/ce3398dfc2d42d23.png)

however the** ComputeBuffer.SetData **method would take too long to upload the entire array of matrices

![](../../assets/4d00becbba4cad75.png)


![](../../assets/4d00becbba4cad75.png)

But what happens if I switch to a [SubUpdates buffer](https://docs.unity3d.com/2020.1/Documentation/ScriptReference/ComputeBufferMode.SubUpdates.html)? Well I have no clue what’s happening and no interest for now to learn it. This was just an exercise after all. I believe that, somehow, the Nvidia Driver let me directly write in to the memory that is used by the GPU to reserve the compute buffer. What I know is that I get this in the profiler:

![](../../assets/2d8a3f2f9677358d.png)


![](../../assets/2d8a3f2f9677358d.png)

which means plenty of CPU avaiable to even make a game!

In order to achieve this, I had to hack a bit the GPUInstancer code (which ships with the plugin). I just changed the buffer initialization to:

```
runtimeData.transformationMatrixVisibilityBuffer =
new ComputeBuffer(runtimeData.bufferSize, GPUInstancerConstants.STRIDE_SIZE_MATRIX4X4, ComputeBufferType.Structured, ComputeBufferMode.SubUpdates);
```


*Careful though, I spent almost one hour to understand why Begin/EndWrite wasn’t working at first. Turned out that currently it works only with the Vulkan Renderer, although Unity documentation doesn’t mention this anywhere!*

Edit: it seems that is not necessary to call Begin/EndWrite every frame, but only when needed. I am not sure about it honestly, so if someone could shed some light, it would be appreciated.

>I still haven’t got when call EndWrite though, you say you call it before each job, but from you explanation it seems that you should never call it, because if you call it you will dispose the buffer?

Yes I call it before job scheduling AND before new BeginWrite 🙂 Loop looks like that:

…-> StartFrame -> BeginWrite, Schedule Job ->EndFrame -> StartFrame -> EndWrite, new BeginWrite, Schedule Job – >EndFrame ->…

Nope, this call only “dispose” native array reference which you use for writing. It not disposing buffer itself

well then you are using more or less like I used in my demo, the only difference is that you call end write before the job and not after. I don’t understand where the cache is then.

You already cache ComputeBuffer, if you do this only once in Start:

runtimeData.transformationMatrixVisibilityBuffer = new ComputeBuffer(…);

Because nativeArray disposed right after EndWrite and job not run yet (Schedule not mean execute from this place, it start execution later in frame)

Hi, dear eizenhorn and Sebastiano Mandalà! I hope that you will see my comment and could help me First of all, thank you very much for sharing of such cutting-edge technology regarding async writing of data to GPU! There are almost no good tutorials with source code about this theme. I tested code from Sebastiano with GPU Instancer – after some modifications based on comments from eizenhorn it started to work. Moreover, my own code started to work, where no usage of GPU Instancer at all, only pure Indirect Instancing by Unity. BUT.. all this stuff works only on Vulkan… Read more »

Hello, unfortunately this is not my field of expertise. This was just an experiment and gpu programming is not what I usually do.

ohh..

But could you say, please – could you launch your code on DX 11?

From your conversation with eizenhorn I understood that in the beginning you could get right results only on Vulkan, but eizenhorn said you some things, how to make your code running without problem on DX 11.

Did you have success with applying of his recommendations and did you get right results on DX 11?

Moreover this code should throw exception like that:

oh now I understand. I thought you were talking about caching the NativeArray returned by BeginWrite. We are on the same page now. The only thing I am still not sure about is what’s the difference between calling EndWrite before and after the job.

Thus you close write stream without any thing written in to that. For Vulcan it can work because on hardware level it’s, maybe, not closing write stream and you still can access GPU memory.

Oh you doing it a bit wrong, I just looked at your code 🙂 You call EndWrite right after scheduling, job not done yet it’s just scheduling, you should call EndWrite after Complete call (or you can not force that and check IsCompleted for waiting untill job done by self and call EndWrite after that and shedule next jobs)

yes that was an oversight, thank you!

I hope you could help with my question above regarding DX 11

I think you now should remove end part of article, for excluding misleading someone 🙂

It works not only with Vulcan. We’re using it on DX11. There some limitations for Begin\EndWrite: currently you might hit a slightly slower path on the render thraed if the buffer has been created just before calling begin write. So try to reuse the buffer as much as posssible and on DX11 you should not begin/end write several times in a frame.

thank you for the feedback. If I used it with DX11 the cubes were simply not moving. It may be due to the large quantity. I didn’t understand what you are saying about reusing the buffer. I can keep the buffer “open” without using end write as long as I want to?

Edit: I just tested it again, with DX11 the cubes do not even appear on the screen.

Thus it’s only GPUInstance implementation problem, not Unity, because we’re using raw DrawMeshInstanceDIndirect and it works perfectly for our custom animation and rendering system, as proof – animation and fog of war here – DrawMeshInstancedIndirect and ComputeBuffer’s with Begin\EndWrite: https://youtu.be/dUq2oVhInSU I didn’t understand what you are saying about reusing the buffer For example create buffer at OnCreate\Awake and reuse them, if buffer need to be resized – resize only when it necessery. Not call BeginWrite right after buffer creation, otherwise it will work slower. Nothing to force you EndWrite in same frame. In our case we schedule job every 3rd… Read more »

ok this is the kind of feedback I was looking for. I was in doubt myself about when EndWrite should be called.

However what does EndWrite precisely do and why should it make a difference when it’s called?

“Not call BeginWrite right after buffer creation, otherwise it will work slower”

then when should it be called?

“Thus it’s only GPUInstance implementation problem, not Unity,”

this doesn’t explain why it works with Vulkan.

then when should it be called? As I said (and this is what Unity engineers told me when we discussed this with them) cache and reuse buffers. Create buffers at OnCreate\Awake, and then use them in Update. By slower path I mean render thread processing will be slower. Main Thread or Jobs writing cost stay the same (because it’s just operation with memory), thus it affects only performance of render thread itself. this doesn’t explain why it works with Vulkan. I don’t know, again it’s most likely GPUInstancer implementation problem, I don’t know what they do underhood, maybe using platform… Read more »

GPUInstancer doesn’t have any special code for Vulkan and it doesn’t support SubUpdates. I hacked the code to support SubUpdates, but you can still be correct about it.

So your point is this: as long as the buffers do not change, cache them. I got it. I still haven’t got when call EndWrite though, you say you call it before each job, but from you explanation it seems that you should never call it, because if you call it you will dispose the buffer?

Lol it throws 403 when previous comment have “On Update \Update” string (without spaces), after removing “On Update \”(without spaces) all become fine, seems inside quote \U not supported )))

New comments plugin enabled, now this thread is a mess, but the plugin seems good! 🙂

wordpress is super annoying