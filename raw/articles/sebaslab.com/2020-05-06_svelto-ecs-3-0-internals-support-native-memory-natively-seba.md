---
title: 'Svelto ECS 3.0 Internals: Support Native Memory Natively - Seba''s Lab'
url: https://www.sebaslab.com/svelto-ecs-3-0-internals-support-native-memory-natively/
author: Sebastiano Mandalà
published: '2020-05-06'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

With the approaching third major release, **Svelto.ECS** internals have been overhauled to support **Burst **and *native memory* (among other features that I will discuss in different articles). The idea to support native memory in a c# framework is counter intuitive, but Burst is such an incredible piece of technology that the many hours invested to find a proper solution cannot be considered anything else than absolutely necessary for the future of the Svelto framework.

Unity started to design the **DOTS **technology before c# 7 was released, hence much of the design currently in use is missing out on the improvements that the new language introduced, with severe consequences on who, like me, designs frameworks with c# for Unity. If c# 7 and **Memory<T>/Span<T>** were already available, my guess (or better say my hope) is that Unity team could have had the chance to rethink some approaches and make them more c# oriented than c oriented.

Nowadays Memory<T>/Span<T> are still not available in unity, forcing finding less efficient workarounds to be able to support native memory and managed memory when necessary.

#### Supporting Native and Managed memory with one data structure only

Svelto.ECS database revolves around one data structure only, the **Svelto.Common** * FasterDictionary*. It was originally called FasterDictionary only because, compared to the original c# Dictionary, FasterDictionary was returning the values as a simple managed array. When you query an array of components in Svelto, you are ultimately asking to return the values held by a FasterDictionary.

FasterDictionary was originally designed to hold only managed memory, so making it manage optionally native memory, without using Span<T>/Memory<T>, proved to be an interesting challenge.

#### First solution: Pinning Memory

My first solution relied on the use of **GCHandle.Alloc** to pin the managed buffers of Svelto and return pointers that could be used by Burst. This solution worked well, but it was bothering me for a couple of reasons: the buffer pinned needed to be released (which ultimately means more boilerplate code for the user) and also potentially I could miss out in performance benefits from using native arrays directly (which eventually it seems aren’t that relevant). So I decided to try something else.

#### Second solution: finding a way to hold native or managed memory without using Memory<T>

C# managed arrays are as fast as they can be and the jitter is able to optimize out checks if they are deemed not necessary, in such a way that iterating a c# array becomes very similar to iterate a c array. In c# [there is nothing as fast as iterating a managed array](https://www.sebaslab.com/fastest-way-to-iterate-an-array-in-c/), except, of course, iterating a native array.

First I had to figure out how to let FasterDictionary handle native memory too. My first idea, obviously, was to use Memory<T>. However Memory<T> is currently largely unusable in Unity: while a compatible **System.Buffers **assembly exists, the implementation is slow. I need to be clear though, that the proper solution to this problem is to use Memory<T>. One of the reasons Memory<T> has been designed, is precisely to let a single data structure using, optionally, different kind of memory without resorting to the use of generics or interfaces and objects to wrap it, thus achieving maximum speed.

#### First solution (Again): Using Generics

Without Memory<T>, there aren’t many options available to solve the issue. In order to avoid the use of interfaces, I could use generic parameters in my FasterDictionary to be able to define the allocation strategy to use (Native or Managed). This would result in the most efficient way to handle the problem, but also in a more complex API, because the generic parameter must be known at compile time, forcing its propagation up to the final user interface, making it more awkward to use. Currently it is svelto to decide if a FasterDictionary should use managed or native memory, according to the nature of the data to hold. If the data is *unmanaged*, Svelto will automatically use native memory. This would have been possible to achieve with generic parameters too, however when it is time to query the array of components, the user would have needed to know if the current data to query is unmanaged or not.

In this case, the dictionary looks like:

```
var sveltoDictionaryGenerics = new SveltoDictionaryGeneric<uint, Test, ManagedStrategy<Test>>(dictionarySize);
var sveltoNativeDictionaryGenerics = new SveltoDictionaryGeneric<uint, Test, NativeStrategy<Test>>(dictionarySize);
```


In order to avoid the need to know the nature of the data beforehand, the use of an interface, to abstract the nature of the buffer, is required.

#### Second solution (for real): Using interfaces

With interfaces instead of generics, I need to hold the memory wrapper as an object rather than a struct, adding an extra layer of indirection. In real life this cost is not excessive, so I decided eventually to go with this solution, as it will let to maintain the API perfectly intact. The dictionary looks like:

```
sveltoDictionary = new SveltoDictionary<uint, Test>(dictionarySize, new ManagedStrategy<Test>());
```


#### Profiling the solutions

Now that I explained my solutions to the problem, let’s see how effective they are. I will profile them in Unity, because it’s the target at the moment, but also in a .net core application, using **Benchmark.net**, so that you could see how a *Fast Span* support affects performance.

For the Unity profiling, I used the *Unity Performance Testing API and the Test Report*. The code of the test looks like:

```
Measure.Method(() =>
{
using (Measure.Scope("Insert"))
{
for (int index = 0; index < dictionarySize; index++)
{
ref var randomIndex = ref randomIndices[index];
sveltoDictionary[randomIndex] = new Test((int) randomIndex);
}
}
using (Measure.Scope("ReadAndCheck"))
{
for (int index = 0; index < dictionarySize; index++)
{
ref var randomIndex = ref randomIndices[index];
if (sveltoDictionary[randomIndex].a != randomIndex)
throw new Exception("what");
}
}
})
.WarmupCount(3)
.MeasurementCount(10)
.IterationsPerMeasurement(1)
.Run();
```


And now the results:

![](../../assets/2350787b420d6286.png)

![](../../assets/48509f5a657c01db.png)

![](../../assets/df9db2d2e68dafe9.png)

![](../../assets/aa8352e3252b0da6.png)

Pay attention that most of the time should be spent in the hashing and searching part, so how to access the dictionary should be not relevant (even if I am iterating 1 million times). This is true with all the tests, except the Span<T>, that shows how the slow Span<T> suffers from the lack of the support from the CLR.

Note: I am really curios to see how this would perform with IL2CPP, but unluckily the Test API crashes with it. Bug already reported! I may update this if Unity teams fix the problem and I find the results interesting.

*Now let’s see how it looks like wit the support of fast Span<T>:*

![](../../assets/11a984645db6f353.png)

There you go. As you can see now we are more or less where it should be. Also it seems that the .Net team optimized the standard dictionary a bit more than the mono version 🙂