---
title: Zero allocation code in C# and Unity - Seba's Lab
url: https://www.sebaslab.com/zero-allocation-code-in-unity/
author: Sebastiano Mandalà
published: '2019-12-15'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

A recent tweet asking about how to achieve zero allocation code in Unity inspired me to write a short piece about the importance of memory allocation in c# and game development.

C# wasn’t initially designed for game development, but today, thanks to *Unity, ECS and Burst*, we can achieve great results in terms of performance that were previously the only domain of c++ developed products. However, in order to get these results, the c# programmer must understand the fundamental limitations of operative systems and CPU architectures, as a c++ programmer does. The c# programmer must also know how c# works at its core to understand why seemingly harmless behaviours can actually heavily affect the execution performance.

This article is therefore aimed at people who want to be sure they are using their tools optimally. If you don’t need this kind of performance, the article is still useful for knowledge.

### Allocating data structures and objects

Let’s start from the c# memory allocation strategy. We all know that c# uses garbage collection, but this doesn’t come for free. According my tests, allocating an empty class is 3 times slower than allocating the same class using native memory (*Marshal.AllocHGlobal*) and *50 times slower* than creating a new struct. Structs are much faster because no allocation is ever involved with them unless by mistake boxing/unboxing happens.

There is more to it though: object references are not garbage collected until they are referenced by something. How does the GC know if a reference is still held though? Contrary to what one may think, a reference assigned to a field of an object is not just an assignment! More, slower, stuff happens under the hood to help the garbage collector detect what is referenced by what, *hence working with references, instead of structs, is slower not just for allocations*.

Of course, let’s not forget that allocating continuously eventually leads to a garbage collection kicking in *at any point of the execution time* which is made worse by the fact that the Unity garbage collection is one of the slowest implementations out there.

If you want to know more about what happens under the hood with c# memory allocation, you should definitively read this book:

Remember that even with GC, memory leaking is still possible! The most common cause of memory leaking is usually due to stateful static classes not clearing their references. *As static classes are never collected, what they reference will never be released either!*

C++ coders know well that per-frame allocations must be avoided at all costs. I don’t know any valid argument that would justify continuous allocations either. User input based allocations, which happen every now and then, may be OK.

The standard strategy is then* to preallocate and reuse as much as you can*. If you are going to use 1000 bullets at most, allocate an array of 1000 bullets even if normally much less are used.

Avoid using any data structure that allocates continuously. Y*our friends are Arrays, Lists and Dictionaries*. Preallocate them, and don’t allow any resizing during the execution of the game.

Object Pools are your friends exactly for the same reason. They allow you to reuse objects in a preallocated array instead to need to create them every time! Use Object Pools.

### Boxing/Unboxing and other trickier allocations

Regarding c# allocation this was the simplest part so far. The trickier sneakier allocations are relative instead to* boxing/unboxing, external variable capturing and wrong use of delegates.*

These are so tricky, that the only way to be sure that you don’t fall for them is to use tools that help visualise what’s going on, like:

**Jetbrains Rider**and its**heap Allocation Viewer plugin**. This is useful most of the times although sporadically it is not reliable. Visual Studio also has something similar, but I haven’t used it in a while,[so try it](https://marketplace.visualstudio.com/items?itemName=MukulSabharwal.ClrHeapAllocationAnalyzer)(at least Visual Studio has a free version)**Static code analyzers**. Unity is maintaining[Project Auditor](https://github.com/mtrive/ProjectAuditor). I didn’t use it yet, but I love these kind of tools. Leave me some feedback about it if you use it please. Static code analyzers are able to check your code and tell you the places where things can go wrong.- Use any
**IL viewer**and check the code you have doubts on. Of course this is the worst tool, because you need to have some suspects first, while the others will warn you about what’s wrong. - Use the
**Unity Profiler**(see below). - Use the
[Unity Test suite to write functional tests for your code.](https://docs.unity3d.com/Packages/com.unity.test-framework@1.1/manual/reference-custom-constraints.html)

If you don’t know what boxing is, you should look it up. Briefly, as I hinted, c# treats differently objects from structs/value types. However, there are cases where the user may accidentally ask c# to convert a struct/value type in an object, ending up in a new allocation of this object.

#### Interface boxing

Boxing is the process, hidden from the user, to transform a Struct into an Object, boxing the struct inside the new object that must be allocated. It’s even worse than allocating an object because boxing can happen multiple times without the user realising it. The most common way to box is to cast a struct to an interface. Let’s say that you have a struct (TestStructI) that implements the interface (ITest) then you decide to cast the struct to ITest or you assign it to a class that has an **ITest** field. WRONG, BOXING will trigger an allocation!

![](../../assets/3da4d437a309c527.png)

in the same way, assigning the return value of a *GetEnumerator()* to IEnumerator results in boxing as most of the time** Enumerators are implemented as structs**.

Tip: when you implement your own enumerable/enumerator, implement it as a struct. There is no reason to use classes for custom enumerators. You don’t need even to implement the *IEnumerator/IEnumerable* interface. *Foreach *will look for the *GetEnumerator()* method regardless. In this way, *foreach *will also be slightly faster because the *IDisposable *pattern code won’t be generated. A proof of concept can be [found here](https://sharplab.io/#v2:C4LglgNgPgAgTARgLACgYGYAE9MGFMDeqmJmAzsAE4CuAxsJgLICeAogHbUC2AppQIYAjCD2KkiKUlOxYKNepgBi/CnwAiYemAD27fpWYBpHswBq/CNR4duffsG2Ux0ws5ekMmQdu0Qm2gDceADkeAA9gAAoASjd3V0l49xgAdkwAMwsyHgBuOPcAX1R8l08wdgZcakpKHgrMAF4APkwABjzElyLO6RKZJRVgdU1gHT0DYzMLKxteAQdKTABxHmBZuwWYvokkjzT2HgB3AdVKDS1dfSMTc0trTjn7RxiO+O6pd9I3TxgAFiYYgl4gF9JghhR1gJhDxGpgDscWJChCIXn10o4ePxaAALTCREGLcEMcpgngQh52aGxHpSHaFNzdApAA===).

Note that once Unity Mono implementation had a bug that forced boxing every Enumerator inside a *foreach*, but this is not the case anymore.

#### Boxing struct through IEqualityComparer

In previous projects I worked on, this happened a few times. Algorithms that need the *IEqualityComparer* and use [ EqualityComparer<T>.Default](http://msdn.microsoft.com/en-us/library/ms224763.aspx) would generate tons of allocations if T is a struct without the IEqualityComparer defined explicitly. A common case is using structs as a key for a dictionary without implementing

*IEqualityComparer*. Nowadays I am so wary of it that, if needed, I actually implement

*IEquatable<T>*and

*IEqualityComparer<T>*and if it makes sense

*IComparable<T>*too

#### Iterator blocks

If you use [Iterator blocks](https://csharpindepth.com/articles/StreamingAndIterators) (*which are IEnumerator functions that use the yield keyword, ergo: coroutines*), be aware that every time you use an Iterator block like *StartCoroutine(IteratorBlock())* a new iterator block object is created and allocated!

*Coroutines *are tricky as well, but another simple piece of advice is to try to reuse as much as you can the *Unity Yield Instructions*, like *WaitForSeconds*. Do not new them every time you need to yield them, [but cache the variable and reuse it](https://forum.unity.com/threads/c-coroutine-waitforseconds-garbage-collection-tip.224878/).

#### Careful about initializing structs used as generic parameter.

Recently I have been surprised by the profiler, I suddenly got this (consider that our product is allocation free at run time)

![](../../assets/111de652fa957905.png)


![](../../assets/111de652fa957905.png)

Why all of a sudden, thousands of allocations? It’s because I naively did this:

```
struct AllocatingConstraints<TBuffer> where TBuffer:struct
{
public AllocatingConstraints(bool test)
{
_buffer = new TBuffer(); //call !!0 [System.Private.CoreLib]System.Activator::CreateInstance<!TBuffer>() seriously?
}
TBuffer _buffer;
}
```


instead of this:

```
struct AllocatingConstraintsNoNew<TBuffer> where TBuffer:struct
{
public AllocatingConstraintsNoNew(bool test):this()
{
}
TBuffer _buffer; //this is initialized as a struct phewww
}
```


Even if the constraints struct is used, with the former the buffer is initialized through reflection! [Madness!](https://sharplab.io/#v2:C4LglgNgPgAgTARgLACgYGYAE9MGFMDeqmJmAzsAE4CuAxsJgIIQQD2tAhsGAHYDmuVjwqUOvYGQA8AFQBC1AGYKAppQB8mAO4ALVcsxzFKyiBF1gxUkRSlb2LMzadu/QcKpieEgBQAjVqwQmMDKFACUlnaEkVGkAPq+RqqYALyYPMqaBvJKqt5hANyYAPTFnCyYAISVAAyYANowCAB0AAqUYABuXMrNgpTKADJgvgC6Tc2M9F1crCYguAM9AJLuHDy0ypKVhrnq+eSqYKzUZBAAngD8MbYAvjekDyS7xpgJSZQFMfc2j78kZnoTBY7C4vAEQhEngkADlWDDMjIcsYNDo9NkPqYqOYYtZYvZgU4wa5IR5xGQ4QjNH4AkEQuEQMBtGAyPkntF/nYfvj2S9ku89kVSkyWZhRbwwNwOBAwAAvZQAE0wHDIyvI2KBAAddJpdd8YjEMNgACyYACyBzxpB+tyAA===)

#### The params keyword

Using the [ params keyword](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/params) for function parameters also

[leads to sneak allocations](https://stackoverflow.com/questions/38679180/will-params-in-c-sharp-always-cause-a-new-array-to-be-allocated-on-every-call), as an array is always allocated under the hood, even if just one parameter is used!

#### Lambdas and Delegates

If you use many *lambas and delegates* you are asking for trouble. Passing actions (and other delegates) by parameter always allocate unless you preallocate the delegate beforehand. In the following examples I am using the* Unity Test Package* to test memory allocation, which may confuse you (sorry about that). For the first case, I wrote a function, **TestDelegate**, that accepts a **System.Action**. In the way I am using it (passing a lambda) I will cause an allocation:

![](../../assets/9bfc5b965909290b.png)

![](../../assets/d4c77e065fa289ef.png)

*in reality in the *case of *a simple lambda, C# under the hood does exactly the same thing, the lambda will be allocated once, cached and reused.*

However, generally, lambda should be avoided *as once you accidentally catch an external variable, c# is not able to automatically cache the implementation*. Catching an external variable means using any variable from outside the scope of the Lambda.

Local functions won’t help either once passed as parameters as there isn’t a *struct *implementation of the delegate class, hence an object will be always created.

If you need to use preallocated delegates that need parameters, then they should be used like this:

```
public class C
{
System.Action<int> _preallocatedAction;
C()
{
_preallocatedAction = MethodToCall;
}
void MethodToCall(int parameter)
{
System.Console.WriteLine(parameter);
}
void MethodCallingTheDelegateLaterOn(System.Action<int> delegateAction, int parameter)
{
delegateAction(parameter);
}
public void M() {
MethodCallingTheDelegateLaterOn(_preallocatedAction, 2);
}
}
```


note that I preallocate the **MethodToCall **delegate using the *_preallocatedAction *field, which can then be used later on by the **MethodCallingTheDelegateLaterOn **method. This example looks weird, but in reality it’s quite a common case when delegates are involved.

#### Linq and Tasks

By the way, I am not even touching **Linq **here. While Linq is a terrific tool, it should be avoided like the plague for game development. Linq has been optimized a lot over time, but it is still the cause, at least, of many enumerator allocations. Note that there are libraries that promise Linq-like 0 allocation code. Do the work? No clue as I don’t use Linq, but you can have a look: [https://github.com/NetFabric/NetFabric.Hyperlinq](https://github.com/NetFabric/NetFabric.Hyperlinq)

I should also mention the use of the **Task** class** **and *await/async*, but if you use those, you probably already know what you are doing. If you still want to know more, [check out this link which explains everything](https://devblogs.microsoft.com/dotnet/understanding-the-whys-whats-and-whens-of-valuetask/).

### Strings

let’s face it, if you are using strings at run-time (frame-based operations), you are doing something wrong. Always find an alternative to strings, but when it’s totally necessary, be aware that most of the operations involving strings result in an allocation. Many articles will tell you to use StringBuilder as a way to alleviate the problem, but be aware that it won’t solve it. In fact, even if it will save a lot of allocations during concatenations and other operations, the final result, which happens through a *ToString()*, will allocate a new string. A **StringBuilder **is effective only if it’s reused and not recreated every single time.

### Profile It

Once you learn these tricks and good practices what it is left to do is to run the game and open the **Unity editor profiler**. Click on the *Call Stack *button (Unity 2019.3, previously called *allocation callstack*) and check closely for red allocations. In the following example, I am making the mistake to assign a struct to an interface. Every 10 frames the Unity Profiler will show a red mark in the timeline view (the hierarchical view is useful as well to check overall allocations)

[crayon start-line=”9″]public class Allocate : MonoBehaviour

{

// Update is called once per frame

void Update()

{

if (Time.frameCount % 10 == 0)

{

using (new ProfilerMarker(“Allocating Frame”).Auto())

{

ITestInterface test = new TestInterface();

}

}

Thread.Sleep(10);

}

interface ITestInterface

{ }

struct TestInterface : ITestInterface

{ }

}

[/crayon]

![](../../assets/1575b3c87877fd09.png)


![](../../assets/1575b3c87877fd09.png)

Since 2019.3 is even possible to track GC allocation from specific standalone clients (Windows for example). This is probably the easiest way to track and fix allocations at the moment.

The example shows just a tiny allocation, that really won’t affect your performance, however, when boxing creeps in, it’s easy to end up boxing in loops having, as result, thousands of allocations per frame.

All the optimizations discussed so far shouldn’t be applied until the profiler shows you that there is a real problem, otherwise, you will fall into the early optimization issue. However for people like me who write 100% objectless ECS code, not striving to zero allocation may end up in milliseconds spent in thousands of allocations per frame.

I also suggest you have a look at the Unity [performance test API](https://docs.unity3d.com/Packages/com.unity.test-framework.performance@1.2/manual/index.html). It is really convenient and it can tell you if allocations happen as well.

If I forgot something or you have any questions or you need more details on something, leave a comment below and I will reply ASAP.

Could yo please expand a little bit more tasks and awaits? Isn’t it better to use awaits than coroutines?

they are two different things. Very similar in the implementation as they are both state machines (and they allocate for the same reasons), but they should be used for different purposes. Do you use them?

Await/Async and coroutines have a lot of similarities and yet are different enough to be used in different contexts. They both generate state machine like code that can be executed over the time (time-splitting execution), however await/async works in multithread. Unless you know what you are doing, multithreading can be very dangerous. If you know what you are doing, you probably would know that await/async allocates more or less like coroutines do when iterator blocks are created. Await/Async haven’t been designed for games really. The pattern can be used for games if you use it in the right way, otherwise… Read more »

Might be worth adding the details for how a sync/await allocate to the article as they can be used on the main thread in MonoBehaviours without Tasks in Unity, so might become more commonplace.

Do foreach loops still generate garbage or boxing in unity 2019?

no they don’t, but foreach are still slower than for when used on anything else than pure managed arrays. If the datastructure supports an indexer (even better if a by ref indexer) than it’s better to use a for.

“According my tests, allocating an empty class is 3 times slower than allocating the same class using native memory”

That’s impossible Allocating a single object is merely changing one pointers value.

did you try? If you do try with Unity as well, as .net core may have better performance there.

thank you for this article. really was well written and enlightening