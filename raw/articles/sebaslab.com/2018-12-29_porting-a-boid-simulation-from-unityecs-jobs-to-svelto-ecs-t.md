---
title: Porting a boid simulation from UnityECS/Jobs to Svelto.ECS/Tasks - Seba's Lab
url: https://www.sebaslab.com/porting-a-boid-simulation-from-unityecs-to-svelto-ecs/
author: Sebastiano Mandalà
published: '2018-12-29'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

While I am spending part of my holidays writing **Svelto.Tasks 2.0** and relative article, I was looking for new examples that could accompany it, when my attention was drawn to this: [https://github.com/hecomi/UnityECSBoidsSimulation.](https://github.com/hecomi/UnityECSBoidsSimulation) It’s not simple to find a working boid simulation and I was curious to compare the *UnityECS/Jobs* results with what I could achieve with *Svelto.ECS/Tasks*. While the results are pretty positive (this article includes comparison and profilings), I eventually didn’t find what I was looking for (a good example), as at the end of the day, this is again another massive parallelism demo that shouldn’t run on the CPU. Still, I learned something new and interesting, hence this article.

It seems already clear what direction the Unity developers are taking, although the code is not closed any more, is being designed to be used as a black box making the integration with outside systems becoming a bit difficult. With UnityECS, I understand that the internal states cannot be used outside the main thread and the job system. It makes sense, as Unity needs to find a way to guarantee thread safety for dummies, however it makes integration with systems that use their own thread logic harder, which is something not nice in my opinion. Basically currently the black box ECS code cannot be used with, for example, Task.net or Svelto.Tasks. However this is not a big issue, and I will explain why:

I develop Svelto.ECS on my own and in my spare time, while the community around it is growing (hoping that one day someone will contribute too), the code throughput will never match the one of a whole team working full time, therefore I have to focus on what it matters: providing a framework simple to read and clear to use to the final user (which is mainly my team 🙂 ). A not overengineered library that would force the coder to think twice about what it’s doing and avoid adapting the ECS pattern to their know-how, which could lead to dangerous mash-up. All the rest comes automatically, meaning that an entire engine from scratch can be made with Svelto.ECS. Network engines, rendering engines , physic engines and so on. I will never have the time to do these, but when working in a company, is sort of normal to rewrite portion of the used development platform when this is too limiting.

However if Unity wants UnityECS to be successful, they must provide a ready to use ECS framework compatible with the entire set of Unity engine features. This is a huge amount of work, not just for sheer lines of code to write, but also just to design how the new systems must be integrated with the existing codebase. I can already notice this difficulty with the **MeshInstanceRenderSystem**, with the latter already taking over some responsibilities that currently should be on the **Scriptable Rendering Pipeline**, like *visibility culling*.

Since Unity is doing all this job anyway, I think it’s important for Svelto.ECS users being able to use UnityECS too although you may wonder, what’s the point to use Svelto.ECS then?

Svelto.ECS is fundamentally different than UnityECS and its users know the benefits. At the same time, UnityECS can be seen as black box low level API, while Svelto.ECS can be used for writing the gameplay code. I tested this theory with this porting and it turned out to work well. Let’s dive into the details:

First download the repository from [https://github.com/sebas77/Svelto.ECS.Examples.Boids](https://github.com/sebas77/Svelto.ECS.Examples.Boids) it includes the work done by the original author too (examples from 1 to 6) while you can check them, for the sake of this article, please open the example under “**Boid-SveltoECS-Sample1-MultiThreadedParallelTaskCollection**“. We will open other examples too for profiling comparison purposes.

You can run it and you should immediately see the boids going around like this:

![](../../assets/22f018e4c180adc1.png)

My porting is a direct conversion from the original “**Boid-PureECS-Sample4-JobDependencies**” so we will use this scene for comparison.

I can’t use the *Burst *version because *Burst *is still not available outside the job system, but it will eventually be, probably before March, so I will upgrade this example when it’s out. It would be fair to compare with IL2CPP too, but at the moment of writing, it seems that UnityECS is broken when compiled with IL2CPP. This is something I am going to update too when will be fixed, meanwhile we will use IL2CPP without rendering to profile the simulation part.

To start our comparison, we will build a client for both the scene (original and mine) as profiling inside the editor is a bad idea. I am also not going to talk about my code, as I will comment the code extensively, so if you want to learn Svelto.Tasks and Svelto.ECS, just check it and read my other articles.

Note that I know almost nothing about the Unity Job system and Unity ECS, therefore I have no clue if the original author got it right and coded it properly. I just assume so, but please let me know if this comparison is not fair for some reason. I built the original sample number four on my I7 at home and profiled the raw frame rate. I set both examples to run with 1000 boids. Take in account that this is a proper boid simulation, with no tricks, which means that the neighbours detection is present and being a quadratic problem, is quite slow.

This is what I get with the original sample 4 after some seconds running:

![](../../assets/2dd79674e8554e1c.png)

while with my example :

![](../../assets/85fdd2b1dc16553e.png)

Here you go, like already seen in the[ 1 Million points demo](https://www.sebaslab.com/svelto-tasks-million-points-multiple-cpu-cores-threads-unity-jobs-system/), Svelto.Tasks and Unity Jobs (minus the Burst part) are very similar. This article is not about showing off what Svelto.Tasks does, as I am not here to evangelize, but surely these results make me wonder if Unity Jobs is really needed in its current form and it hasn’t maybe overeengineered a bit for what it must do.

Here a bit more details on the code now:

As I said, I decided to use *Unity ECS* as a black boxed low level library for the rendering and totally remove *Unity Jobs *to use *Svelto.Tasks*. In fact, this is actually more a Svelto.Tasks example than a Svelto.ECS example. However it shows you how I build pure entity structs entities with Svelto.ECS and use them to store the information computed by the Svelto tasks.

*The strategy I adopted is to write a second Svelto engine to synchronize, on the main thread, the Svelto ECS entities with the Unity ECS *

*entities*. Unity ECS entities are built with the minimal set of information, containing only the component data necessary to render the boid through the Unity ECS systems.

Initially I wanted to synchronize the data between Svelto.ECS and Unity.ECS outside the main thread, but then I realized that this is not possible as Unity won’t allow me to change the component data arrays outside the main thread or unity jobs. That’s why, maybe, in future I am going to add a Svelto.Tasks runner based on Unity Jobs as well.

Let’s have a look at the synchronization engine:

```
IEnumerator SynchronizeUnityECSEntitiesWithSveltoECSEntities()
{
while (true)
{
#if !JUST_RUN_IT
//Lock the main thread and force waiting for the Svelto.Tasks threaded jobs to finish. This is not
//a normal operation and it's here just to measure the frame rate.
_synchronizationSignal.Complete();
#else
//this is the normal not blocking operation. The frame rate will be as fast as the unity main thread
//can be, but the boids will still update at the real execution rate
yield return _synchronizationSignal;
#endif
int count;
//fetch the Svelto.ECS entities
var entities = entitiesDB.QueryEntities<BoidEntityStruct>(GAME_GROUPS.BOIDS_GROUP, out count);
//fetch the Unity ECS components
var position = _unityECSgroup.GetComponentDataArray<Position>();
var rotation = _unityECSgroup.GetComponentDataArray<Rotation>();
//synchronize!
for (int i = 0; i < count; ++i)
{
position[i] = new Position()
{Value = new float3(entities[i].position.x, entities[i].position.y, entities[i].position.z)};
rotation[i] = new Rotation()
{ Value = new quaternion(entities[i].rotation.x, entities[i].rotation.y, entities[i].rotation.z,
entities[i].rotation.w)};
}
//tell to the Svelto.Tasks threads that they can carry on with the next iteration
_synchronizationSignal.SignalBack();
//yield one frame so the while (true) will not enter in an infinite loop
yield return null;
}
}
```


Note the **JUST_RUN_IT **comments. Svelto.Tasks operations are totally asynchronous, but blocking it (*Complete()* is a Svelto.Tasks extension to force execute the enumerator on the current thread in a synchronous way) was necessary to measure the frame rate with the* Graphy plugi**n*. If, in fact, I build the application with the **JUST_RUN_IT** define, this is what we get:

![](../../assets/cd68d1cd21198f0a.png)

*now this doesn’t mean that suddenly everything is faster*,* the boids are updated exactly at the same speed of before,* it just means that svelto tasks are not blocking the main thread, therefore it can carry on while the jobs are executed on the other threads. The whole concept of frame doesn’t make much sense any more, so different ways to measure how long tasks are executed for must be found. This is why Svelto.Tasks comes with a simple built-in profiler, so that you can measure how long tasks take.

OK that’s it, I am not going in to Svelto.Tasks details because you can read my other articles for this, I just wanted to show you two things:* how is possible to integrate Svelto.ECS with Unity.ECS and how really doens’t make any difference in using a pure c# multithreaded task library against Unity Jobs.*

Next step for me is to wait for Burst being available outside the unity jobs, so I can try to integrate them. Meanwhile we can see how they perform with IL2CPP. Unluckily unity ECS seems to be broken with IL2CPP, so we will only measure the length of the tasks, without seeing them in action:

There are no boids, but this is in how fast the code (without special optimizations) would run with IL2CPP if I didn’t do anything wrong. (note: this is with the blocking operations on the main thread)

![](../../assets/3d6d86af351b0bc8.png)

I will update this part of the article when I will be able to see the boids on the screen. Maybe someone wants to write a Svelto.ECS*MeshInstanceRenderSystem *instead so we can get rid of Unity ECS? 🙂

### Profiling Svelto.Tasks code

In a multi-threaded application, the concept of frame rate doesn’t make much sense any more, except to know how long it takes to present the frame on the screen. For this reason, it’s necessary to profile the tasks separately to know their real performance (don’t forget to enable the **JUST_RUN_IT** define for the sake of this article!)

Currently is possible to profile Svelto.Tasks within Unity in two ways (in future I ma add support for PIX, something I always wanted to do, but never had the time).

First way: Compile with the define** ENABLE_PLATFORM_PROFILER**. Now the Svelto.Tasks runners and tasks show up within the profiler itself and the look like this:

![](../../assets/1db57c70b75c1ef8.png)


![](../../assets/1db57c70b75c1ef8.png)

Unluckily even if Unity added the **CustomSampler **new class, I can’t still take full advantage of it for the way it has been designed, so some allocation will still happen when profling is ON. that’s why Profiling is optional through a compiler directive.

The second way is to enable the simple built-in Svelto.Tasks profiler, using the compiler directive **TASKS_PROFILER_ENABLED**. This is less effective, as you can’t profile outside the editor itself, but still useful for debugging. While the example is running, select the persistent GameObject Svelto.Tasks.Profiler and check the inspector. You will see something like:

![](../../assets/2577185631209169.png)

### Conclusion:

I end this article thanking the author of the original code and letting you know that soon I will publish Svelto.Tasks 2.0 with some good optimizations and 0 allocation code! Meanwhile please send me your feedback in case you spot something or you have any question.

I think unity Will continue to push their own ECS system also beacuse with svelto would be simpler to switch to another engine, especially when using json configuration instead of unity inspector.

let’s put in this way: why did Unity started with this ECS thing in the first place? It’s not a good marketing move (although of course they are trying everything to make it looks cool and good), it may not be intrinsically necessary, either because the audience may not needed it at all or because, as Svelto proves, c# power is enough to achieve the same goals, therefore if a big team would have invested on it, they could have done it already. Lately I thought a lot about it, but at the end of the day, as a coder,… Read more »