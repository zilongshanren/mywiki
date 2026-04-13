---
title: Svelto.ECS+Tasks to write Data Oriented, Cache Friendly, Multi-Threaded code
  - Seba's Lab
url: https://www.sebaslab.com/svelto-ecs-svelto-tasks-to-write-data-oriented-cache-friendly-multi-threaded-code-in-unity/
author: Sebastiano Mandalà
published: '2017-10-21'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

*Note: this article assumes that the reader knows how to use Svelto.ECS and Svelto.Tasks although the findings are interesting regardless.*

## Introduction

New exciting features are coming to [Svelto.ECS](https://github.com/sebas77/Svelto.ECS) and [Svelto.Tasks](https://github.com/sebas77/Svelto.Tasks) libraries. As I am currently focused on optimizing Robocraft for Xbox One, I added several functionalities that can help making our game faster. Therefore I decided to write a simple example to show some od them. I have to be honest, it’s very hard to think about a simple example that makes sense. Every game has its own needs and what makes sense for one couldn’t be that meaningful for others. However everything boils down to the fact that I added features to exploit data locality (CPU cache) and easily write multi-threaded code. I have already discussed about how to use [Svelto.Tasks](http://www.sebaslab.com/svelto-taskrunner-run-serial-and-parallel-asynchronous-tasks-in-unity3d/)[ multi-threaded ](http://www.sebaslab.com/svelto-taskrunner-run-serial-and-parallel-asynchronous-tasks-in-unity3d/)* ITaskRoutine*, so I hope I can now show how to use them with

**. Spoiler alert: this article only won’t be sufficient to show you the potentiality of the library, as being more thorough would make this post too long and complex, therefore I encourage you to experiment on your own or wait for my next articles (that come every six months or so :P). This article also assumes that you know the basic concepts behind**

[Svelto.ECS](http://www.sebaslab.com/ecs-1-0/)*Svelto.ECS*and

*Svelto.Tasks*.

Initially I wanted to write an example that would mimic the **boids** demo showed at the unite roadmap talk that you can briefly see on this [unity blog](https://blogs.unity3d.com/2017/06/27/unite-europe-2017-keynote-recap-connecting-creating-and-the-future-of-unity/) post. I soon decided to stop going down that route because it’s obvious that Joachim took advance of the new thread safe transform class or even wrote a new rendering pipeline on purpose for this demo, as the standard *Transform* class and even the *GameObject* based pipeline would be the biggest bottleneck impossible to parallelize ([Note: I eventually found a work around to this problem to show visually the power of the multi core Svelto.Tasks approach](http://www.sebaslab.com/svelto-tasks-million-points-on-multiple-cpu-cores-with-multi-threaded-csharp-and-unity3d/)). Since I believe that massive parallelism makes more sense on the **GPU** and that multi-threading should be exploited on **CPU** in a different way, I decided to not invest more time on it. However as I had some interesting results, I will use what is left of this useless example I wrote to show you what potential gain in milliseconds you may get using Svelto.ECS and Svelto.Tasks. I will eventually discuss how this approach can potentially be used in a real life scenario too.

Svelto.ECS and Svelto.Tasks have a symbiotic relationship. Svelto.ECS allows to naturally encapsulate logic running on several entities and treat each engine flow as a separate “[ fiber](https://en.wikipedia.org/wiki/Fiber_(computer_science))“. Svelto.Tasks allows to run these independent “fibers” asynchronously even on other threads.

GPUs work in a totally different fashion than CPUs and operative systems take the burden to handle how processes must share the few cores usually available. While on a GPU we talk about hundreds of cores, on a CPU we can have usually only 2-12 cores that have to run thousands of threads. However each core can run only one thread at time and it’s thanks to the OS scheduling system that all these threads can actually share the CPU power. More threads run, more difficult is the OS task to decide which threads to run and when. That’s why massive parallelism doesn’t make much sense on CPU. At full capacity, you can’t physically run more threads than cores, thus multi-threading on CPU is not meant for intensive operations.

## The Example

You can proceed now downloading the new ** Svelto.ECS cache example** and open the scene under the

**Svelto-ECS-Parallelism-Example**folder. Since I removed everything from the original demo I was building, I can focus on the code instructions only and that’s why this example is the simplest ever I made so far, as it has only one

**Engine**and one

**Node.**The demonstration will show four different levels of optimization, using different techniques and how is possible to make the same instructions run several times faster. In order to show the optimization steps, I decided to use some ugly defines (sorry, I can’t really spend too much time on these exercises), therefore we need to stop the execution of the demo in the editor and change the define symbols every time we want to proceed to the next step. Alternative you can build a separate executable for each combination of defines, so you won’t have to worry about the editor overhead during the profiling. The first set of defines will be:


*FIRST_TIER_EXAMPLE**;*

**.**

*PROFILER*Let’s open and analyse the code. As usual you can find our standard **Context** and **relative composition** **root** (*MainContextParallel* and *ParallelCompositionRoot*). Inside the context initialization, a *BoidEngine* is created (I didn’t bother renaming the classes) as well as 256,000 entities. Seems a lot, but we are going to run very simple operations on them, nothing to do with a real flock algorithm. Actually the instructions that run are basically random and totally meaningless. Feel free to change them as you wish.

The operations that must be executed are written inside the *BoidEnumerator* class. While the code example is ugly, I wrote it to be allocation free to be as fast as possible. A preallocated *IEnumerator *can be reused for each frame. This enumerator doesn’t yield at all, running synchronously, and operates on a set of entities that must be defined beforehand. The set of operations to run, as already said, are totally meaningless and written just to show how much time very simple operations can take to run on a large set of entities.

The main loop logic, enclosed in the *Update* enumerator, will run until the execution is stopped. It’s running inside a standard **Update Scheduler** because I am assuming that the result of the operations must be available every frame. In the way it’s designed, the main thread cannot be faster than the execution of the operations even if they run on other threads. This is very easily achievable with **Svelto.Tasks**.

### The Naive Code (Editor 113ms, client 58ms)

So, assuming you didn’t get too much confused by the things happening under the hood, running the example will show you that the operations takes several milliseconds to be executed (use the stats window if you use the editor). in my case, **on my I7 CPU**, running the **FIRST_TIER_EXAMPLE*** *operations takes around **113ms. **

this is how the code looks at the moment:

var position = entities[index].node.position; var direction = realTarget - position; var sqrdmagnitude = direction.sqrmagnitude; entities[index].node.position = direction / (sqrdmagnitude);

Let’s have a look a the MSIL code generated

// var position = entities[index].node.position; IL_0036 ldloc.0 IL_0037 ldloc.3 IL_0038 callvirt Svelto.ECS.Example.Parallelism.BoidNode Svelto.DataStructures.FasterList`1<Svelto.ECS.Example.Parallelism.BoidNode>::get_Item(System.Int32) IL_003D ldfld Svelto.ECS.Example.Parallelism.IBoidComponent Svelto.ECS.Example.Parallelism.BoidNode::node IL_0042 callvirt UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.IBoidComponent::get_position() IL_0047 stloc.s position // var direction = realTarget - position; IL_0049 ldloc.1 IL_004A ldloc.s position IL_004C call UnityEngine.Vector3 UnityEngine.Vector3::op_Subtraction(UnityEngine.Vector3,UnityEngine.Vector3) IL_0051 stloc.s direction // var sqrdmagnitude = direction.sqrMagnitude; IL_0053 ldloca.s direction IL_0055 call System.Single UnityEngine.Vector3::get_sqrMagnitude() IL_005A stloc.s sqrdmagnitude // entities[index].node.position = direction / (sqrdmagnitude); IL_005C ldloc.0 IL_005D ldloc.3 IL_005E callvirt Svelto.ECS.Example.Parallelism.BoidNode Svelto.DataStructures.FasterList`1<Svelto.ECS.Example.Parallelism.BoidNode>::get_Item(System.Int32) IL_0063 ldfld Svelto.ECS.Example.Parallelism.IBoidComponent Svelto.ECS.Example.Parallelism.BoidNode::node IL_0068 ldloc.s direction IL_006A ldloc.s sqrdmagnitude IL_006C call UnityEngine.Vector3 UnityEngine.Vector3::op_Division(UnityEngine.Vector3,System.Single) IL_0071 callvirt System.Void Svelto.ECS.Example.Parallelism.IBoidComponent::set_position(UnityEngine.Vector3) IL_0076 nop

this set of operations runs 4 times for each entity; As I stated before, they are meaningless and random, it’s just a set of common and simple operations to run.

### The Callless Code (Editor 57ms, Client 23ms)

Let’s now switch to ** SECOND_TIER_EXAMPLE**, changing the defines in the editor and replacing

**. Let the code recompile. Exactly the same operations, but with different instructions, now take around**

*FIRST_TIER_EXAMPLE***65ms (client 24ms)**…what changed? I simply instructed the compiler to not use the

**Vector3**methods, running the operations directly on the components.

The code looks like:

IBoidComponent boidNode = entities[index].node; var position = boidNode.position; var x = (realTarget.x - position.x); var y = (realTarget.y - position.y); var z = (realTarget.z - position.z); var sqrdmagnitude = x * x + y * y + z * z; boidNode.position.Set(x / sqrdmagnitude, y / sqrdmagnitude, z / sqrdmagnitude);

// IBoidComponent boidNode = entities[index].node; IL_003C ldloc.0 IL_003D ldloc.3 IL_003E callvirt Svelto.ECS.Example.Parallelism.BoidNode Svelto.DataStructures.FasterList`1<Svelto.ECS.Example.Parallelism.BoidNode>::get_Item(System.Int32) IL_0043 ldfld Svelto.ECS.Example.Parallelism.IBoidComponent Svelto.ECS.Example.Parallelism.BoidNode::node IL_0048 stloc.s boidNode // var position = boidNode.position; IL_004A ldloc.s boidNode IL_004C callvirt UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.IBoidComponent::get_position() IL_0051 stloc.s position // var x = (realTarget.x - position.x); IL_0053 ldloc.1 IL_0054 ldfld System.Single UnityEngine.Vector3::x IL_0059 ldloc.s position IL_005B ldfld System.Single UnityEngine.Vector3::x IL_0060 sub IL_0061 stloc.s x // var y = (realTarget.y - position.y); IL_0063 ldloc.1 IL_0064 ldfld System.Single UnityEngine.Vector3::y IL_0069 ldloc.s position IL_006B ldfld System.Single UnityEngine.Vector3::y IL_0070 sub IL_0071 stloc.s y // var z = (realTarget.z - position.z); IL_0073 ldloc.1 IL_0074 ldfld System.Single UnityEngine.Vector3::z IL_0079 ldloc.s position IL_007B ldfld System.Single UnityEngine.Vector3::z IL_0080 sub IL_0081 stloc.s z // var sqrdmagnitude = x * x + y * y + z * z; IL_0083 ldloc.s x IL_0085 ldloc.s x IL_0087 mul IL_0088 ldloc.s y IL_008A ldloc.s y IL_008C mul IL_008D add IL_008E ldloc.s z IL_0090 ldloc.s z IL_0092 mul IL_0093 add IL_0094 stloc.s sqrdmagnitude // boidNode.position.Set(x / sqrdmagnitude, y / sqrdmagnitude, z / sqrdmagnitude); IL_0096 ldloc.s boidNode IL_0098 callvirt UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.IBoidComponent::get_position() IL_009D stloc.s V_10 IL_009F ldloca.s V_10 IL_00A1 ldloc.s x IL_00A3 ldloc.s sqrdmagnitude IL_00A5 div IL_00A6 ldloc.s y IL_00A8 ldloc.s sqrdmagnitude IL_00AA div IL_00AB ldloc.s z IL_00AD ldloc.s sqrdmagnitude IL_00AF div IL_00B0 call System.Void UnityEngine.Vector3::Set(System.Single,System.Single,System.Single) IL_00B5 nop

It appears to me that the main difference is the number of call/callvirt executed, which obviously involves several extra operations. All the calls involve saving the current registries and some variables on the stack, call virt involves an extra pointer dereference to get the address of the function to call. More importantly, we avoid the copy of the Vector3 struct due to the fact that the method results are passed through the stack.

Let’s quickly switch to * THIRD_TIER_EXAMPLE*. The code now runs at around

**57ms (client 23ms, almost no difference, interesting),**but the code didn’t change at all.

**What changed then? I simply exploited the**

*FasterList*method to return the array used by the list. This removed another extra

*callvirt*, as the

*operator[]*of a collection like

*FasterList*(but same goes for the standard

*List*) is actually a method call. An

*Array*instead is known directly by the compiler as a contiguous portion of allocated memory, therefore knows how to treat it efficiently.

### The Cache Friendly Code (Editor 24ms, Client 16ms)

[Have you have heard how ECS design can easily enable data oriented code?](https://www.youtube.com/watch?v=tGmnZdY5Y-E&feature=youtu.be) This is what the * FOURTH_TIER_EXAMPLE define is about.* The code now runs at around

**24ms,**another big jump, but again it seems that the instructions didn’t change much. Let’s see them:

var boidNode = entities[index]; var x = (realTarget.x - boidNode.position.x); var y = (realTarget.y - boidNode.position.y); var z = (realTarget.z - boidNode.position.z); var sqrdmagnitude = x * x + y * y + z * z; boidNode.position.x = x * sqrdmagnitude; boidNode.position.y = y * sqrdmagnitude; boidNode.position.z = z * sqrdmagnitude; entities[index] = boidNode;

// var boidNode = entities[index]; IL_003C ldloc.0 IL_003D ldloc.3 IL_003E ldelem Svelto.ECS.Example.Parallelism.BoidNode IL_0043 stloc.s boidNode // var x = (realTarget.x - boidNode.position.x); IL_0045 ldloc.1 IL_0046 ldfld System.Single UnityEngine.Vector3::x IL_004B ldloc.s boidNode IL_004D ldfld UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_0052 ldfld System.Single UnityEngine.Vector3::x IL_0057 sub IL_0058 stloc.s x // var y = (realTarget.y - boidNode.position.y); IL_005A ldloc.1 IL_005B ldfld System.Single UnityEngine.Vector3::y IL_0060 ldloc.s boidNode IL_0062 ldfld UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_0067 ldfld System.Single UnityEngine.Vector3::y IL_006C sub IL_006D stloc.s y // var z = (realTarget.z - boidNode.position.z); IL_006F ldloc.1 IL_0070 ldfld System.Single UnityEngine.Vector3::z IL_0075 ldloc.s boidNode IL_0077 ldfld UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_007C ldfld System.Single UnityEngine.Vector3::z IL_0081 sub IL_0082 stloc.s z // var sqrdmagnitude = x * x + y * y + z * z; IL_0084 ldloc.s x IL_0086 ldloc.s x IL_0088 mul IL_0089 ldloc.s y IL_008B ldloc.s y IL_008D mul IL_008E add IL_008F ldloc.s z IL_0091 ldloc.s z IL_0093 mul IL_0094 add IL_0095 stloc.s sqrdmagnitude // boidNode.position.x = x * sqrdmagnitude; IL_0097 ldloca.s boidNode IL_0099 ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_009E ldloc.s x IL_00A0 ldloc.s sqrdmagnitude IL_00A2 mul IL_00A3 stfld System.Single UnityEngine.Vector3::x // boidNode.position.y = y * sqrdmagnitude; IL_00A8 ldloca.s boidNode IL_00AA ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_00AF ldloc.s y IL_00B1 ldloc.s sqrdmagnitude IL_00B3 mul IL_00B4 stfld System.Single UnityEngine.Vector3::y // boidNode.position.z = z * sqrdmagnitude; IL_00B9 ldloca.s boidNode IL_00BB ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_00C0 ldloc.s z IL_00C2 ldloc.s sqrdmagnitude IL_00C4 mul IL_00C5 stfld System.Single UnityEngine.Vector3::z // entities[index] = boidNode; IL_00CA ldloc.0 IL_00CB ldloc.3 IL_00CC ldloc.s boidNode IL_00CE stelem Svelto.ECS.Example.Parallelism.BoidNode

It’s true that now the code is call free, but would this justifies the big jump? The answer is no. Just removing the last call left would have saved around **10ms** only, while now the procedure is more than 30ms faster. The big saving must be found in the new *EntityViewStruct* feature that is enabled by[ ](http://www.sebaslab.com/ecs-1-0/#StructNodeEngine)the ** FOURTH_TIER_EXAMPLE **enables. Svelto.ECS allows now to build EntityViews as class and as struct. When they are built as struct, you can exploit the full power of writing cache friendly data oriented code.

If you don’t know how data is laid out in memory, well, stop here and study how data structures work. If you know c++ you are already advantaged, because you know how pointers work, but otherwise, you must know that you can write contiguous data in memory only with array of value types, including struct, assuming that these structs contain only value types! Svelto ECS now allows to store EntityViews either as classes and structs, but when structs are used, the EntityViews are always stored as simple array of structs, so that you can achieve the fastest result, depending how you design your structs ([Structure of Arrays or Array of Structures, it’s up to you!](https://stackoverflow.com/questions/40163722/is-my-understanding-of-aos-vs-soa-advantages-disadvantages-correct))

To put it simply, when you use references, the memory area pointed by the reference, is very likely nowhere in the memory near where the reference itself is. This means that the CPU cannot exploit the cache to read contiguous data. Array of value types (which can be struct containing valuetypes) are instead always stored contiguously.

Cache is what makes the procedure much faster. Nowadays CPUs can read a continuous block of data up to *64 bytes in one single memory access from the L1 cache (which takes around 4 cycles of clock)*. The L1 cache is efficiently filled by the CPU on data access, caching 32KB of consecutive data. As long as the data you need to access is in those 32KB of cache, the instructions will run much faster. Missing data from the cache will initialize a very slow RAM memory access, which can be hundreds of cycles slow! There are many articles around talking about modern CPU architecture and how data oriented code takes full advantage of it, so I won’t spend more time, but I will link some resources once I have the time, so check the end of the article for new edit every now and then.

var x = (realTarget.x - entities[index].position.x); var y = (realTarget.y - entities[index].position.y); var z = (realTarget.z - entities[index].position.z); var sqrdmagnitude = x * x + y * y + z * z; entities[index].position.x = x * sqrdmagnitude; entities[index].position.y = y * sqrdmagnitude; entities[index].position.z = z * sqrdmagnitude;

// var x = (realTarget.x - entities[index].position.x); IL_004B ldloc.1 IL_004C ldfld System.Single UnityEngine.Vector3::x IL_0051 ldloc.0 IL_0052 ldloc.s index IL_0054 ldelema Svelto.ECS.Example.Parallelism.BoidNode IL_0059 ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_005E ldfld System.Single UnityEngine.Vector3::x IL_0063 sub IL_0064 stloc.s x // var y = (realTarget.y - entities[index].position.y); IL_0066 ldloc.1 IL_0067 ldfld System.Single UnityEngine.Vector3::y IL_006C ldloc.0 IL_006D ldloc.s index IL_006F ldelema Svelto.ECS.Example.Parallelism.BoidNode IL_0074 ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_0079 ldfld System.Single UnityEngine.Vector3::y IL_007E sub IL_007F stloc.s y // var z = (realTarget.z - entities[index].position.z); IL_0081 ldloc.1 IL_0082 ldfld System.Single UnityEngine.Vector3::z IL_0087 ldloc.0 IL_0088 ldloc.s index IL_008A ldelema Svelto.ECS.Example.Parallelism.BoidNode IL_008F ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_0094 ldfld System.Single UnityEngine.Vector3::z IL_0099 sub IL_009A stloc.s z // var sqrdmagnitude = x * x + y * y + z * z; IL_009C ldloc.s x IL_009E ldloc.s x IL_00A0 mul IL_00A1 ldloc.s y IL_00A3 ldloc.s y IL_00A5 mul IL_00A6 add IL_00A7 ldloc.s z IL_00A9 ldloc.s z IL_00AB mul IL_00AC add IL_00AD stloc.s sqrdmagnitude // entities[index].position.x = x * sqrdmagnitude; IL_00AF ldloc.0 IL_00B0 ldloc.s index IL_00B2 ldelema Svelto.ECS.Example.Parallelism.BoidNode IL_00B7 ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_00BC ldloc.s x IL_00BE ldloc.s sqrdmagnitude IL_00C0 mul IL_00C1 stfld System.Single UnityEngine.Vector3::x // entities[index].position.y = y * sqrdmagnitude; IL_00C6 ldloc.0 IL_00C7 ldloc.s index IL_00C9 ldelema Svelto.ECS.Example.Parallelism.BoidNode IL_00CE ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_00D3 ldloc.s y IL_00D5 ldloc.s sqrdmagnitude IL_00D7 mul IL_00D8 stfld System.Single UnityEngine.Vector3::y // entities[index].position.z = z * sqrdmagnitude; IL_00DD ldloc.0 IL_00DE ldloc.s index IL_00E0 ldelema Svelto.ECS.Example.Parallelism.BoidNode IL_00E5 ldflda UnityEngine.Vector3 Svelto.ECS.Example.Parallelism.BoidNode::position IL_00EA ldloc.s z IL_00EC ldloc.s sqrdmagnitude IL_00EE mul IL_00EF stfld System.Single UnityEngine.Vector3::z

Caching is weird though. For example it could come natural to store the whole *EntityViewStruct* in a local variable, while this seems a harmless instruction, in a data oriented context it can be disaster! How does removing the storing to a local variable of the struct make it faster? *Well this is where things get very tricky*. The reason is that the contiguous amount of data you need to read must be not too big and must be able to be *read in one memory access (32 to 64bytes, depending the CPU)*.

Since our *BoidNode* struct is quite small, caching the variable here actually would have made the execution just slightly slower. However if you make the *Boidnode struct* larger (Try to add other four Vector3 fields and cache the whole structure in a local variable), you will wreck the processor and the execution will become largely slower! (edit: this problem could be solved with the [new Ref feature of c# 7](https://www.danielcrabtree.com/blog/128/c-sharp-7-ref-returns-ref-locals-and-how-to-use-them) which, unluckily, is still not supported by Unity)

Instead *accessing directly the single component won’t enable the struct-wide read due to the copy to a local variable* and since x,y,z are read and cached at once, these instructions will run at the same speed regardless the size of the struct. Alternatively you can cache locally just the position Vector3 in a local variable, which won’t make it faster, but it will be still work fast regardless the size of the struct.

### The Multi Threaded Cache Friendly Code (Editor 8ms, Client 3ms)

To conclude, let’s keep the **FOURTH_TIER_EXAMPLE*** *define, but add a new one, called * TURBO_EXAMPLE*. The code now runs at around

**8ms**. This because the new


*MultiThreadedParallelTaskCollection***Svelto.Tasks feature is now enabled. The operations, instead to run on one thread, are split and run on 8 threads. As you already figured out, 8 threads doesn’t mean 8 times faster (unless you actually have 8 cores :)) and this is the reality. Splitting the operations over multiple threads**

*doesn’t only give sub-linear gains, but also diminishing return*, as more the threads, less and less faster will the operations run, until increasing threads won’t make any difference. This is due to what I was explaining earlier. Multi-threading is no magic. Physically your CPU cannot run more threads than its cores and this is true for all the threads of all the processes running at the same time on your Operative System. That’s why CPU multi-threading makes more sense for asynchronous operations that can run over time or operations that involve waiting for external sources (sockets, disks and so on), so that the thread can pause until the data is received, leaving the space to other threads to run meanwhile. Memory access is also a big bottleneck, especially when cache missing is involved (the CPU may even decide to switch to other threads while waiting for the memory to be read, this is what Hyperthreading actually does)

This is how I use the *MultiThreadedParallelTaskCollection*** **in the example:

count = _nodes.Count; int numberOfThreads = (int)Mathf.Min(NUM_OF_THREADS, count); var countn = count / numberOfThreads; _multiParallelTask = new MultiThreadedParallelTaskCollection(numberOfThreads); for (int i = 0; i < numberOfThreads; i++) _multiParallelTask.Add(new BoidEnumerator(_nodes, countn * i, countn));

This collection allows to add **Enumerators** to be executed later *on multiple threads*. The number of threads to activate is passed by constructor. It’s interesting to note that the number of enumerators to run is independent by the number of threads, although in this case they are mapped 1 to 1.* The MultiThreadedParallelTaskCollection, being an IEnumerator, can be scheduler on whatever runner, but the sets of tasks will always run on their own, pre-activated, threads.*

The way I am using threading in this example is not the way it should be used in real life. First of all I am actually blocking the main thread to wait for the other threads to finish, so that I can actually measure how long the threads take to finish the operations. In a real life scenario, the code shouldn’t be written to wait for the threads to finish. For example, handling AI could run independently by the frame rate. I am thinking about several way to manage synchronization so that will be possible not just to exploit continuation between threads, but even run tasks on different threads at the same time and synchronize them. *WaitForSignalEnumerator*** **is an example of what I have in mind, more will come.

All right, we are at the end of the article now. I need to repeat myself here: this article doesn’t show really what is possible to do with Svelto.ECS and Svelto.Tasks in its entirety, this is just a glimpse of the possibilities opened by this infrastructure. Also the purpose of this article wasn’t about showing the level of complexity that is possible to handle easily with the Svelto framework, but just to show you how important is to know how to optimize our code. The most important optimizations are *first the algorithmic ones, then the data structure related ones and eventually the ones at instruction level*. Multi-threading is not about optimization, but instead being able to actually exploit the power of the CPU used. I also tried to highlight the CPU threading is not about massive parallelism and GPUs should be used for this purpose instead.

### The Importance of the Compiler (Client 1.5ms!!)

I started to wonder, what if I had the chance to use a good c++ compiler to see if it could do a better work with auto-vectorization? After all, we are aware of the fact that the JIT compiler can’t do miracles in this sense. Since IL2CPP is not available for Windows platform, I compiled the same code for UWP, using the IL2CPP option. I guess the results are pretty clear, IL2CPP produces an executable that is twice as fast as the c# version. Since there isn’t any call to the native code, can’t be because of the benefit due to the lack of marshalling. I haven’t had the time to verify yet what the real difference is, but auto-vectorization *may* be the reason.

## Conclusions

While this article is implicitly (and strongly) advising you to follow the *Entity-Component-System *pattern to centralize and modularize the logic of your game entities and gives another example of Svelto.Tasks usage to easily exploit multithreading, it has the main goal to show you why is needed to pay attention to how the code is written even if we talk about c# and Unity. While the effectiveness of these extreme optimizations largely depend on the context, understanding how the compiler generates the final code is necessary to not degrade the performance of large projects.

Having a light knowledge of modern CPUs architectures (like I do) helps to understand how to better exploit the CPU cache and optimize memory accesses. Multi-threading really needs more separate articles, but I now can state with certainty that exploiting the full power of the CPU with Unity is more than feasible, although the biggest bottleneck will remain the rendering pipeline itself.

To be honest, most of the Unity optimization issues are often related to the *marshalling* that the Unity framework performs when is time to call the Unity native functions. Unluckily these functions are many and are called very often, becoming the biggest issue we found during our optimizations. *GameObject* hierarchy complexity, calling *Transform* functions multiple times and similar problems can really kill the performance of your product. I may talk about these finding in future with a separate article, but many have been discussed already by other developers. The real goal to pursue is to find the right balance of what you can do in c# and what must be left to Unity. The ECS pattern can help with this a lot, avoiding the use of *MonoBehaviour* functionalities when they are not strictly necessary.

For example, Iet’s try to instantiate *256k GameObjects* (yes it’s possible to do) and add a *Monobehaviour* each that simply runs the fastest version of the test. On my PC, it runs at *105ms*, and even if profiling with Unity doesn’t give the best accuracy, it seems that half of this time is spent for Marshalling (very likely the time between switching between c# and c++ for each update, my current assumption is that Monobehaviours are stored as native objects and they need to switch to managed code for each single Update called, this is just crazy!).

Final Results: |
||
Editor |
Client |
|
| ECS Naive Code | 113ms |
58ms |
| ECS No Calls Involved | 57ms |
23ms |
| ECS Structs only | 24ms |
16ms |
| ECS Multithreading (8 threads) | 8ms |
3ms |
| ECS Multithreading UWP/IL2CPP (8 threads) | n/a |
1.5ms |
| Classic GameObject/Update approach (no calls inside) | 105ms |
45ms |
| Classic GameObject/Update approach (no calls inside) UWP | n/a |
22ms |

*TL;DR:*

- I crammed too many points in this article 🙂
- Optimize your algorithms first, you don’t want any quadratic algoritm in your code. Logarithmic is the way to go.
- Optimize your datastructures next, you must know how your data structures work in memory to efficiently use them. There is difference between an array, a list and a linkedlist!
- Optimize your instructions paying attention to memory accesses and caching for last (if you want to squeeze those MS OUT!). Coding to exploit the CPU cache is as important as using multi-threading. Of course not all the Engines need to be so optimized, so it depends by the situation. I will link some good references when I have the time, as there is much more to discuss about this point.
- When using Unity, be very careful to minimize the usage of wrappers to native functions. These are many and often can be easily identified in Visual Studio navigating to the declaration of the function.
- Mind that Unity callbacks (Update, LateUpdate etc) are often Marshalled from native code, making them slow to use. The Unity hierarchical profiler tells you half the truth, showing the time taken inside the Update, but not between Updates (usually shown on the “others” graph). The Timeline view will show “gaps” between Update calls, which is the time used for Marshalling them.
- Multithreading is tricky but Svelto.Task can massively help
- ECS pattern allows to write code that exploits
[temporal and spatial locality](https://en.wikipedia.org/wiki/Locality_of_reference)(As you can manage all your entities in one central place). Try Svelto.ECS to see what you can do 😉 - ECS pattern will also help you to minimize the use of Unity functionalities which most of the time involve costly marshalling operations to switch to the native code. Most of them are not really justified and due to old legacy code that has never been updated in 10 years!
- I understand that is hard to relate to an example that iterates over 256k entities. However moving logic from Monobehaviours to ECS engines saved dozens of milliseconds in the execution of the real-life code of our projects.
- Why don’t they finish IL2CPP for standalone platforms? At least windows only!
- Don’t use the editor to profile 🙂

Please leave here your thoughts, I will probably expand this article with my new findings, especially the ones related to the cache optimizations.

For more Multi-threading shenanigans check my new article: [Learning Svelto Tasks by example: The Million Points example ](https://wp.me/p5PZ12-no)

External resources:

[Is my understanding of AoS vs SoA advantages/disadvantages correct?](https://stackoverflow.com/questions/40163722/is-my-understanding-of-aos-vs-soa-advantages-disadvantages-correct)[Unite Austin 2017 – Writing High Performance C# Scripts](https://www.youtube.com/watch?v=tGmnZdY5Y-E)[Implementation of a component-based entity system in modern C++ by Vittoreo Romeo for CPPCon](https://github.com/CppCon/CppCon2015/blob/master/Tutorials/Implementation%20of%20a%20component-based%20entity%20system%20in%20modern%20C%2B%2B/Implementation%20of%20a%20component-based%20entity%20system%20in%20modern%20C%2B%2B%20-%20Vittorio%20Romeo%20-%20CppCon%202015.pdf)[What is data oriented design StackOverflow](http://stackoverflow.com/questions/1641580/what-is-data-oriented-design)[Introduction to data oriented design DICE](https://www.ea.com/frostbite/news/introduction-to-data-oriented-design)[Gameprogrammingpatterns: Data Locality](http://gameprogrammingpatterns.com/data-locality.html)[Parallelizing the Naughty Dog engine using fibers](http://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine)[Optimizing scripts in Unity games](https://learn.unity.com/tutorial/fixing-performance-problems-2019-3)[SIMD at Insomniac Games](https://deplinenoise.files.wordpress.com/2015/03/gdc2015_afredriksson_simd.pdf)[Practical Examples in Data Oriented Design](https://docs.google.com/presentation/d/17Bzle0w6jz-1ndabrvC5MXUIQ5jme0M8xBF71oz-0Js/present?slide=id.i0)[CPU Caches and Why You Care](http://www.aristeia.com/TalkNotes/ACCU2011_CPUCaches.pdf)[Gallery of Processor Cache Effects](http://igoro.com/archive/gallery-of-processor-cache-effects/)(pay attention at the False cache line sharing part)[Pitfalls of Object Oriented Programming](http://harmful.cat-v.org/software/OO_programming/_pdf/Pitfalls_of_Object_Oriented_Programming_GCAP_09.pdf)[More Performance, more gameplay](https://t.co/3SW4OVj6va?amp=1)[A CONCURRENT COMPONENT-BASED ENTITY ARCHITECTURE FOR GAME DEVELOPMENT](https://web.archive.org/web/20170923024217/https://ics.upjs.sk/~krajci/skola/ine/SVK/pdf/Majerech.pdf)

Very good and interesting article! Just a note on the preamble (sorry :P) – “However each core can run only one thread at time”, there are some exceptions: in SMT more threads are executed in the same time on the same core. – “That’s why massive parallelism doesn’t make much sense on CPU”; actually this is not stricly related to context switching. Indeed, CPUs have OpenCL back-end implementations, which of course do not translate thousand of threads to thousand of OS threads, but still can’t get the same performances for data-parallel algorithms. To be noted that even on GPU there… Read more »

thanks for the reply! 1) I am not aware of any SMT architecture running games. Edit: ok I checked on wiki, with SMT you mean the intel Hyper Threading. HyperThreading doesn’t allow two threads to run at the same time, it allows a super fast context switching, so that a second thread can run while the first one is waiting for something slow, like a RAM memory access. 2) I didn’t say (and if I did I didn’t mean it) that massive parallelism doesn’t make sense on a consumer-CPU because of the context switching, but because you can’t really run… Read more »

1) AMD Ryzen, for example, is 2-way SMT. It is not super fast context switching, instead both threads are active in the same time; context is not switched between both, because local resources are allocated for both threads. 2) Even on GPUs with 1000 cores you usually launch kernels with even more than a million threads. They are just issued and completed in groups of threads; when one group completes its processing, it releases its local resources that could be used by the next group in the queue. Yeah vectorized calculations are at the basis of GPU optimized cores, even… Read more »

That’s all super interesting. I’ll do more research and read your post. Are you sure you don’t want to work in the uk? 😉

Eheh. Thanks, it would be super-cool <3 but you know I'm crazy and I've just bought a house in Rome xD

Hey mate, I’ve finally found the time to work through your whole article and checked out all the different defines so I could watch the FPS increases on my machine. Very cool! Lots of fun! As already written (somewhere else), I’ve setup a cube collisions demo (where cubes move randomly on a plane and change color once they bump into another cube – inspired from Adam Martin’s Blog). In order to have a “lean” basis – which would allow me to integrate your ECS framework and learn while doing so. My git repo is here: https://github.com/CreativeWarlock/CubeCollisionsECS After reproducing all basic… Read more »

The entitystruct is quite an advanced topic and I will need to dedicate an article on the good practices with those. From what you wrote it seems you aren’t using them as they should be used. Please follow the cache example I wrote that uses them although it’s not a good examples. It’s use is also limited to very specific applications where the efficiency is crucial, but trust me I still have to find a practical example where they actually needed :). You would need to iterate on hundreds of entities to actually appreciate them and the code must be… Read more »