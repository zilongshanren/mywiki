---
title: 'Svelto ECS 3.4 internals: How to run ECS systems on the GPU - Seba''s Lab'
url: https://www.sebaslab.com/svelto-ecs-3-4-internals-how-to-integrate-computesharp/
author: Sebastiano Mandalà
published: '2023-03-31'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

## Introduction:

Ever since Altimesh announced *Hybridizer* in 2017, I’ve been eager to write C# Svelto engines that run on GPUs through *compute shaders*. Hybridizer promised a seamless integration of a compiler capable of automatically and transparently converting C# code into compute shaders. think of DOTS Burst, but for compiling compute shaders instead.

Unfortunately, the company didn’t deliver on its promises. However, I was thrilled to discover that a single individual, [Sergio Pedri](https://twitter.com/SergioPedri), not only created a working compiler with the same objective but also released it for free on [GitHub](https://github.com/Sergio0694/ComputeSharp)!

Naturally, I couldn’t resist embarking on an experiment with another goal in mind: *demonstrating how it’s possible to modify the Svelto.ECS component data holders to accommodate any custom data structure*. For this example to be meaningful, I needed the components of the entities to be stored directly in *Compute buffers*, eliminating the need for any additional copy.

The outcome is a new version of the [Stride Engine-based Doofuses demo](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example1-Stride-DoofusesMustEat/DOOFUSES_STRIDE_COMPUTESHARP) featuring a couple of engines running on GPU. This demo serves solely academic purposes, as to make it practically useful, I will need to address several points, which I will pose at the conclusion of this article. [A console-only example is also available without using any game engine.](https://github.com/sebas77/Svelto.MiniExamples/tree/master/Example8-ComputeSharp)

My hope is that this demo and article will spark your curiosity, encouraging you to explore the opportunities it can open up. I will be happy to assist you, but unless I get some support on how to improve ComputeSharp usage, my experiments with it are done.

This is a * Stride Engine* demo, not a Unity one, so once you download the project, you can just open the project file (.sln) be sure that the

**RELEASECOMPUTE_SHADERS**config is selected and just run it.

## Modifying Svelto to store components in custom data structures

The core of Svelto.ECS is **SveltoDictionary**, a custom implementation of a hashmap that can be modified to utilize any kind of data structure for storing keys and values. As long as the data structure implements the ** IBufferStrategy **interface, it can be used by SveltoDictionary.

The user can inject their implementation of IBufferStrategy through the use of a custom [ IComponentBuilder](https://github.com/sebas77/Svelto.MiniExamples/blob/master/Example1-DoofusesMustEat/DOOFUSES_STRIDE_COMPUTESHARP/Svelto/com.sebaslab.svelto.ecs.computesharp/ComputeComponentBuilder.cs) and a custom

**. Eventually, the IBufferStrategy implementation allocates a custom**

[ITypeSafeDictionary](https://github.com/sebas77/Svelto.MiniExamples/blob/master/Example1-DoofusesMustEat/DOOFUSES_STRIDE_COMPUTESHARP/Svelto/com.sebaslab.svelto.ecs.computesharp/ComputeSharpTypeSafeDictionary.cs)**to hold the actual data. So the user needs to implement four custom implementations of Svelto-provided interfaces to be able to store components in custom data structures.**

[IBuffer](https://github.com/sebas77/Svelto.MiniExamples/blob/master/Example1-DoofusesMustEat/DOOFUSES_STRIDE_COMPUTESHARP/Svelto/com.sebaslab.svelto.ecs.computesharp/ComputeSharpBuffer.cs)In order to show this feature, I have created a new assembly called **Svelto.ECS.ComputeSharp**. An extension of Svelto.ECS to be usable with ComputeSharp.

This assembly is NOT ready for prime time, is just a rough implementation for the sake of this experiment, however, I may decide to make it production ready, if someone is interested and I get the support I need.

Once the custom implementations are created, then we can just use them to implement a custom component like:

public struct ComputeMatrixComponent : IEntityComputeSharpComponent { public Matrix matrix; }

and then declaring it in our **EntityDescriptor **like:

class DoofusEntityDescriptor: ExtendibleEntityDescriptor<StrideEntityDescriptor> { public DoofusEntityDescriptor() { Add<StrideComponent>(); ExtendWith( new IComponentBuilder[] { new ComputeComponentBuilder<ComputeMatrixComponent>(), new ComputeComponentBuilder<ComputePositionComponent>(), new ComputeComponentBuilder<ComputeRotationComponent>(), new ComputeComponentBuilder<ComputeVelocityComponent>(), new ComponentBuilder<MealInfoComponent>(), new ComputeComponentBuilder<ComputeSpeedComponent>(), }); }

so what’s the big deal? It’s that now, any time a new entity is built, all the data stored in **IEntityComputeSharpComponent** components are copied inside *ComputeSharp Compute Buffer,* like shown here:

public struct ComputeSharpBuffer<T>:IBuffer<T> where T:unmanaged { public ComputeSharpBuffer(in UploadBuffer<T> array, ReadWriteBuffer<T> readWritebuffer) : this() { _readWritebuffer = readWritebuffer; _ptr = array; } [MethodImpl(MethodImplOptions.AggressiveInlining)] public IntPtr ToNativeArray(out int capacity) { throw new NotImplementedException(); } public ReadWriteBuffer<T> ToComputeBuffer() { _ptr.CopyTo(_readWritebuffer); return _readWritebuffer; } public void Update() { _readWritebuffer.CopyTo(_ptr.Span); } public int capacity { [MethodImpl(MethodImplOptions.AggressiveInlining)] get => (int) _ptr.Length; } public bool isValid => _ptr != null; public ref T this[uint index] { [MethodImpl(MethodImplOptions.AggressiveInlining)] get { #if ENABLE_DEBUG_CHECKS if (index >= _ptr.Length) throw new Exception($"NativeBuffer - out of bound access: index {index} - capacity {capacity}"); #endif return ref _ptr.Span[(int)index]; } } public ref T this[int index] { [MethodImpl(MethodImplOptions.AggressiveInlining)] get { #if ENABLE_DEBUG_CHECKS if (index < 0 || index >= _ptr.Length) throw new Exception($"NativeBuffer - out of bound access: index {index} - capacity {capacity}"); #endif return ref _ptr.Span[index]; } } //todo: maybe I should do this for the other buffers too? internal void Dispose() { _ptr.Dispose(); _readWritebuffer.Dispose(); } readonly UploadBuffer<T> _ptr; readonly ReadWriteBuffer<T> _readWritebuffer; }

where **UploadBuffer** and **ReadWriteBuffer **are **ComputeSharp **data structures.

It is now possible to retrieve this data with a simple query shown in this Svelto engine:

public class VelocityToPositionDoofusesEngine: IQueryingEntitiesEngine, IUpdateEngine { public void Step(in float deltaTime) { var doofusesEntityGroups = entitiesDB.QueryEntities<ComputePositionComponent, ComputeVelocityComponent, ComputeSpeedComponent>( GameGroups.DOOFUSES_EATING.Groups); foreach (var ((positions, velocities, speeds, count), _) in doofusesEntityGroups) { _graphicsDevice.For( count, new ComputePostionFromVelocityJob( (positions.ToComputeBuffer(), velocities.ToComputeBuffer(), speeds.ToComputeBuffer()), deltaTime)); positions.Update(); //sync the data back } } readonly GraphicsDevice _graphicsDevice; } }

In this demo, I have used ComputeSharp only on two engines **VelocityToPositionDoofusesEngine **and ** ComputeTransformEngine**.

## Integrating ComputeSharp

Compute Sharp is extremely straightforward to use. The following code is automatically compiled and executed as compute shader once the application run:

[AutoConstructor] readonly partial struct ComputePostionFromVelocityJob: IComputeShader { public ComputePostionFromVelocityJob( (ReadWriteBuffer<ComputePositionComponent> positions, ReadWriteBuffer<ComputeVelocityComponent> velocities, ReadWriteBuffer<ComputeSpeedComponent> speeds) doofuses, float deltaTime) { _positions = doofuses.positions; _velocities = doofuses.velocities; _speeds = doofuses.speeds; _deltaTime = deltaTime; } public void Execute() { var index = ThreadIds.X; float distance = _deltaTime * _speeds[index].speed; var velocity = _velocities[index].velocity; Vector3 position = default; position.X = velocity.X * distance; position.Y = velocity.Y * distance; position.Z = velocity.Z * distance; var result = _positions[index].position; result.X += position.X; result.Y += position.Y; result.Z += position.Z; _positions[index].position = result; } readonly float _deltaTime; readonly ReadWriteBuffer<ComputePositionComponent> _positions; readonly ReadWriteBuffer<ComputeVelocityComponent> _velocities; readonly ReadWriteBuffer<ComputeSpeedComponent> _speeds; }

note the use of **ThreadIds.X** the *code will run in parallel on the GPU threads.*

and as you already saw this code runs through the call:

_graphicsDevice.For(count, new ComputePostionFromVelocityJob( (positions.ToComputeBuffer(), velocities.ToComputeBuffer(), speeds.ToComputeBuffer()), deltaTime));

there is nothing else to do, the code just works.

Of course, as it happens with DOTS Burst, ComputeSharp has a ton of just constraints, so you need to read [its readme to understand the more than reasonable limits](https://github.com/Sergio0694/ComputeSharp/wiki/3.-Getting-started-📖).

## What’s next

As I mentioned earlier, unless I receive the proper support to make faster progress with ComputeSharp, my experiments will come to a halt. However, if I find answers to my following questions, I may publish a production-ready extension that people can use in their projects. I should also note that I am not a compute shader expert, and I am aware that I am missing a great deal of nuance regarding their dispatching.

- First, it’s crucial to understand the scope of this extension. There are three options:
- Execute GPU only: only compute shaders can read and write into the buffers. The results are used inside
**Geometry/Vertex/Pixel Shaders**.**However is it even possible to share compute buffers between the Compute Sharp device and the hosting game engine device?**I hope so but I have no clue how to do so! - Execute compute shaders
*asynchronously*across various engines, and then sync back to the CPU at a sync point (similar to what would happen with DOTS jobs). However, I didn’t understand how to run Compute Shaders asynchronously with ComputeSharp. Although the option seems to exist, I’m unclear on how to execute it.**Additionally, I would need to be able to wait for all the shaders to complete on the sync point, so I would need something to poll to stall the main thread until the execution of the compute shaders is done (in case the user wants to read back the data from the GPU)** - The third option, demonstrated in this demo, is not practical: executing the shader synchronously and immediately syncing the data back to the CPU. Although the shader runs in parallel, the overhead of executing it and syncing the data back negates any performance gain. Apparently is still faster than running on a single thread, but surely slower than running the code in parallel on the CPU.
**A potential advantage of this approach is that when multiple devices are accessible, the user has the flexibility to execute compute shaders on their preferred device. Additionally, this method presents an opportunity to run CPU engines on separate threads, allowing one thread to await the completion of GPU compute shader execution.**

- Execute GPU only: only compute shaders can read and write into the buffers. The results are used inside
- In my previous experiment with Compute Buffers, I was able to use new options provided by modern drivers to directly copy data from the CPU to Compute Buffers without extra temporary copies. I believe ComputeSharp does this through
**UploadBuffer<T>**and**ReadBackBuffer<T>**; however, I haven’t received confirmation, so I’m uncertain if I’m using ComputeSharp optimally even in this simple case. By the way:[The future of CPU/GPU interoperation](https://devblogs.microsoft.com/directx/preview-agility-sdk-1-710-0/)looks exciting. - In this demo, I don’t allow resizing the entity arrays. The arrays are preallocated and cannot grow larger. This is because I’m unsure if it’s a good idea to resize compute buffers on the CPU, and I would need advice on this matter.

## A bit of profiling

as I said this demo is in reality inefficient, but still interesting. Let’s have a look at the profiling:

**ComputeTransformEngine.Step** takes, on average**, 2.702 ms** to compute 20.000 matrices.

**1.2ms** are to wait for the shader to conclude

**0.8ms** to upload the data from the CPU to the GPU, I am not sure if **UploadBuffer **is working as I expected. this is the time spent calling

_uploadBuffer.CopyTo(_readWritebuffer);

**0.6ms** are spent syncing back the data from the GPU to the CPU. This is the time to execute:

_readWritebuffer.CopyTo(_uploadBuffer.Span);

However, if I transform 20.000 matrices on the CPU using c# it then takes an average of **4.79ms**. So after all a naive win.

Last Minute update: I have been asked to try to use the Numerics data-structures instead than the Stride ones since they use SIMD intrinsics to compute. The difference is massive moving to **2.43ms **and so very close to the naive compute shader approach.

To see 20.000 doofuses chasing food, run the demo and use WASD to move the camera, right click + mouse to rotate the camera and left click/middle click to place food.

![](../../assets/edb307d97fd42c0c.png)

May you share the PC specs that these numbers were measured on? More specifically, what CPU and what GPU?

next time, too late for this article now