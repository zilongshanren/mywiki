---
title: 'Svelto ECS 3.0 Internals: profiling the Entity Collection - Seba''s Lab'
url: https://www.sebaslab.com/svelto-ecs-3-0-internals-the-entity-collection/
author: Sebastiano Mandalà
published: '2020-05-17'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Previously, in *Svelto.ECS*, it was possible to query entity components directly as a managed array, which would have resulted in the fastest way to iterate over the components in c#. Since Svelto.ECS 3.0 and because now the framework supports natively native memory as well, I decided to remove this possibility in order to unify the interface for querying *managed *and *unmanaged *entity components (to be precise, it’s still possible, but it needs to be explicitly done and the user must know if they are iterating a native or managed array).

To those who are not familiar with the terminology, unmanaged structs are struct that holds exclusively value types and, not coincidentally, native memory can store only unmanaged types. Clearly, the only reason why I introduced this new code, is **Burst**, but as previously said, it was worth and necessary. Burst can naturally handle only native memory and consequentially only unmanaged structs.

Since native memory cannot handle managed structs and svelto **IEntityViewComponents **are managed, [I had to find a solution to let the Svelto ECS internal datastructure handle both managed memory and native memory without using Memory<T> and Span<T> which are currently unusable in Unity.](https://www.sebaslab.com/svelto-ecs-3-0-internals-support-native-memory-natively/)

The challenge was not just finding a technical solution to this problem, but also how to present the data to the final user, without letting them worry too much about how the memory is managed.

This is where the struct **EntityCollection **comes into play.

EntityCollection was initially designed to wrap a **Memory<T> **(possibly even a **Span<T> **if I decide to keep it as ref struct) to abstract the access to the implementation of the final buffer without passing through interfaces. Today EntityCollection needs to hold an **IBuffer<T>** interface and the cost to pay for it is something I am going to analyze in this article, introducing some interesting thoughts and discoveries.

Since this article is not about learning Svelto, let’s assume that we know how to use its interface (don’t worry, if I don’t have a breakdown before I have the chance to, I will write a series of articles about Svelto.ECS 3.0) and then use the following code to profile the performance:

```
[Test, Performance]
public void TestEntityCollectionPerformance()
{
Measure.Method(() =>
{
EntityCollection<Test> entityCollection =
((IUnitTestingInterface) _enginesroot).entitiesForTesting.QueryEntities<Test>(TESTGROUP);
using (Measure.Scope("Iterate EC"))
{
for (uint index = 0; index < entityCollection.count; index++)
{
entityCollection[index].a = 4;
}
}
using (Measure.Scope("Iterate Buffer"))
{
IBuffer<Test> entities = entityCollection.ToBuffer();
for (int index = 0; index < entityCollection.count; index++)
{
entities[index].a = 4;
}
}
using (Measure.Scope("Casted Iterate Buffer"))
{
var entities = entityCollection.ToNativeBuffer<Test>();
for (int index = 0; index < entityCollection.count; index++)
{
entities.buffer[index].a = 4;
}
}
using (Measure.Scope("Iterate Native Array"))
{
unsafe
{
var entities = (Test*)entityCollection.ToNativeBuffer<Test>().buffer.ToNativeArray(out _);
for (int index = 0; index < entityCollection.count; index++)
{
entities[index].a = 4;
}
}
}
using (Measure.Scope("Iterate Managed Array"))
{
for (int index = 0; index < entityCollection.count; index++)
{
testArray[index].a = 4;
}
}
})
.WarmupCount(3)
.MeasurementCount(10)
.IterationsPerMeasurement(10)
.Run();
}
```


This code uses the **Unity Performance API package** together with the **Test Runner** to gather timings with a given degree of accuracy. I am profiling how quick is to iterate 1 million entities using respectively:

*EntityCollection**directly the buffer as IBuffer**directly the buffer but casted to its implementation**directly a native array**at last, a managed array for comparison.*

Before to proceed to analyze the results, I need to spend two words on profiling with Unity.

*.net* is a very complex beast. It was born with safety and security in mind and it was not really much about performance, as performance critical paths could have been performed anyway through “unsecure” native plugins and interoperability with native code.

Nowadays .net is changing direction, a lot. With .net core and possibly .net 5, many of the obsolete initial assumptions, on how to use .net, have been deprecated, leaving a leaner CLR that can now be used to perform heavier tasks than thought before. Part of this performance boost is given by the improvement of the Jitter. The current .net jitter is called **RyuJit**. RyuJit has the responsibility to convert the Intermediate Language code into native code for the current running platform.

Since the jitter must compile on the fly, it cannot afford to be too slow to not affect the performance of the run time. Even though the code, of course, is compiled once, it’s compiled every time the application runs (which is frankly a bit of a shame, but understandable).

At the same time the Jitter has some tricks up the sleeve that a normal ahead of time compiler cannot have. The jitter can rely on some run time data to perform extra optimizations!

Mono doesn’t use Ryujit. It has a custom jitter that may or may not be up to date with the new .net optimizations. Mono for Unity is even worse. Unity hacked Mono quite a bit, therefore apply optimizations gets harder and harder, especially the ones related to the garbage collection, as unity has a completely custom garbage collection implementation.

However, I could prove that even unity Mono does quite a bit of optimization at run time and *these optimizations are NOT enabled if the code is built to with Debugging Scripts on*. As I recently tweeted, be careful about this, as the difference is astonishing!

This holds very true for profiling in the editor and why the introduction of the Release Mode in Unity 2020 is a big deal.

Look at the the result of iterating 1 million entities when profiling inside the editor

![](../../assets/9f0865fb3a387b23.png)

What I don’t understand, and I will ask on the forum about this, is why if I click on *Run all in player (StandaloneWindows64)* [the results are very different and misleading:](https://forum.unity.com/threads/testrunner-run-all-in-player.891376/)

![](../../assets/b6174f5c40c1f241.png)

![](../../assets/b43f5c0fb6d1c273.png)

Edit: I did more tests and found out that the results are not reliable in either case. I get different values when iterating standard arrays. However they are either in the ballpark of 2ms or 0.7ms. Maybe something depending on the current Mono CLR state, but it needs further investigation.

For this reason, I decided to continue the profiling using just a simple Stopwatch in a built client. The results are similar to the profiler API results in the player:

```
Iterate EC -> 3.0205
Iterate EC -> 3.0345
Iterate EC -> 3.1084
Iterate buffer -> 3.1847
Iterate buffer -> 3.0815
Iterate buffer -> 3.053
Iterate casted buffer -> 2.0987
Iterate casted buffer -> 2.1246
Iterate casted buffer -> 2.1057
Iterate casted buffer 2 -> 2.0369
Iterate casted buffer 2 -> 2.0197
Iterate casted buffer 2 -> 2.0272
Iterate Native Array -> 2.0751
Iterate Native Array -> 2.0645
Iterate Native Array -> 2.0686
Iterate array -> 2.0421
Iterate array -> 2.0451
Iterate array -> 2.0108
```


Iterate an EntityCollection is 50% slower than iterating an array. This is a noticeable degradation in performance, however, the reason why I don’t think it needs to be optimized is explained once we put the profiling code in a more realistic context. At the moment all I am doing is just assigning a value to a struct. While in an ECS scenario this is nothing uncommon, I expect that most of the time the overhead of the code written inside the iteration is bigger than the performance degradation introduced by EntityCollection.

Nonetheless, I did my research anyway to see how I could fix this. The answer is that I can’t now, but I could in future, *hoping Unity will update mono in line with what’s happening with Ryujit*.

These are 2 possible solutions. Maybe 3, but I think the third is not worth it. Let’s have a look for knowledge, I am sure what I learnt can be of some interest to someone:

#### Proper Solution: Span<T>

The proper solution is, of course, using Span<T>. We already said that, but this is how it would work with simplified code:

```
public readonly ref struct EntityCollection<T>
{
public EntityCollection(IntPtr buffer, uint count)
{
unsafe
{
_buffer = new Span<T>((void *)buffer, (int)count);
}
}
public EntityCollection(T[] buffer, uint count)
{
_buffer = buffer;
}
public ref T this[int i]
{
[MethodImpl(MethodImplOptions.AggressiveInlining)]
get => ref _buffer[i];
}
readonly Span<T> _buffer;
}
```


I drop the use of IBuffer<T> to move to Span<T>. [I previously proved that Span<T>, with modern jitters and CLR, is on a par with array iteration](https://www.sebaslab.com/fastest-way-to-iterate-an-array-in-c/). So this would be the definitive solution.

Anything else than this would be awkward, but an alternative solution could be this:

#### Use casted Buffers

```
[JitGeneric(typeof(Unmanaged)), JitGeneric(typeof(Managed))]
public readonly ref struct EntityCollection<T> where T:struct
{
public EntityCollection(IBuffer<T> buffer, uint count):this()
{
if (RuntimeHelpers.IsReferenceOrContainsReferences<T>())
_managedbuffer = (MB<T>)buffer;
else
_nativebuffer = (NB<T>)buffer;
}
public ref T this[int i]
{
[MethodImpl(MethodImplOptions.AggressiveInlining)]
get
{
if (RuntimeHelpers.IsReferenceOrContainsReferences<T>())
return ref _managedbuffer[i];
return ref _nativebuffer[i];
}
}
readonly NB<T> _nativebuffer;
readonly MB<T> _managedbuffer;
}
```


This is basically an awkward version of what Span<T> would do, with the benefit to be as fast as iterating an array (see the result of iterate casted buffer) when Fast Span<T> is not available.

However, this won’t work in Unity either for two reasons:

- Mono jitter doesn’t provide “smart” optimizations based on read only static values. In fact, you must know that the
*if*inside the*get*would disappear once the code is compiled, if Ryujit was used. That’s why the code would be as fast as iterating the casted version of the buffer. You can see what I mean from[sharlab.io](https://sharplab.io/#v2:EYLgxg9gTgpgtADwGwBYA0AXEBDAzgWwB8ABAJgEYBYAKGIAYACY8gOgCUBXAOwwEt8YLAMIR8AB14AbGFADKMgG68wMXAG4a9BrIAW2KGIAy2YO258BG6poDMDXBigcwGBgDkAQgB4AKgD4QAEkPDgAzUJlfPwYAdx0ZGAYfEAcnFxoGTIYAbwys/OI7TwAKQJ4ABUcGfShsAE80Bg5eHgYwbDFsMF4MOoBKBhAGDB1eXGK+vPzM3Opp+YYAfTEqgF5qqFq6qwXpxfbO7t6GdYOunu2p6YBfGiuCu2IUbRgMUoqqmvrG5tazo/69yys12+WWVWm6y+lzmoMy+w652Op0RAJ2C1u1lh80KDFgoSSw1GuAA2i1XC0ACYwBAAXSBMwZ0xJAFlXjoIJTAuJJMU2SNOdyxJIAPIrXgQLi4FgAQQA5nLYLhcLwFDAypIWi05X16djQXLXkz8iC4dNuLhsBFjQtTWaFsQAOx4mAEgCqUqtghluDYrqixQ9loissplIDxSeACoBuCoI0qTS+n10fbMpj7RmMXd9flfq4EYcLqnpriyhhKlAlisoCXMTncalnK4Wd5/EEQuFIv5YvFYEkUo5m1c7aW7K3ij4SbTMtCBkMRmMJkzR7tFsAwhEq1DNvUS/ks/Mmbj8YTF6TyQxE3SVzbMqz2YKeXzH1yeWK+JLpfLFaoVWqNS1LgdT1e1DVcVZolPddNxkMkuGpOl9yyetcyyKcZxgrtayuVCmDsckZFCLpEmCWCoCiEcmVPHwiTGeCKQQmkZ2yBhwLUBhD04q4aCbFwGA9fBsC4bBDUpGhR3zYZVAwKxUL4lthNEmBxOoEErmYRgMBkuScxJAApHoAHEYC4GRlGKXoxBgCBQkDLghJEsTk0aQyMBMsyoAsqybLslklOc3UMhPGBsEpSVJDqF0CQUhgAFEeAuERJGkFwJS4KJewSAcFKotDMlxBK+F6ZLUs/LhSk7LdMo3bCfkvSBzD6EBz2XfKcjvK8CWKThEoEAAJGBJGsqBpUCX1XQSLgVBFKARB4bAWgmrdTJUXAA2Te1OqyRZHOUylaq3E4GD5Ns/D6Q6ZGQ0EhtwGBtvhES+DVS7txOzwogu8jru4rFdlgMKIqij6e0WJ7VRgV6foB8KuEihhW0y3aApUqGc12EKCVo88GKvUDbU6h8BTfYUX2JoVRXFL9ZQVJV/3VOGgJAzrwIYTrVzNXhut6iwYEG4aZDG5appmubJQwRapT9FbptUDaBjNB6CmdaC9rE16yVpH7diVpgVddJZwZe8jNe1lCmS464gA===)checking the assembly output of the method. Without this optimization,*get*would become super slow because of the*if*. - This check won’t work with IL2CPP. This is a big shame though, I am not sure why LLVM couldn’t be, at least, aware if T is unmanaged or not, to apply the optimization.

So second solution is a no no too.

Third solution is viable, but still awkward so I won’t use it. Since EntityCollection is a ref struct, I could do something like:

#### Iterating native/pinned memory

```
public readonly ref struct EntityCollection<T> where T : IEntityComponent
{
public EntityCollection(IntPtr ptr, uint count):this()
{
_buffer = ptr;
}
public EntityCollection3(T[] buffer, uint count):this()
{
_handle = GCHandle.Alloc(buffer, GCHandleType.Pinned);
_buffer = _handle.AddrOfPinnedObject();
}
public ref T this[int i]
{
[MethodImpl(MethodImplOptions.AggressiveInlining)]
get
{
unsafe
{
return ref Unsafe.AsRef<T>(Unsafe.Add<T>((void*) _buffer, (int) i));
}
}
}
public void Dispose()
{
if (_handle.IsAllocated)
_handle.Free();
}
readonly IntPtr _buffer;
readonly uint _count;
readonly GCHandle _handle;
}
```


Problem about this is that, obviously, I don’t want the user to care about disposing the EntityCollection, which is needed exclusively because I pinned the memory of managed arrays (when T is managed).

c# 8 (which will land soon in the alpha version of Unity) supports *Disposable ref struct, so the problem could be mitigated.* Still, if the user forgets to use *using*, it will not dispose it. It would potentially look like this:

`using EntityCollection<Test> entityCollection = ((IUnitTestingInterface) _enginesroot).entitiesForTesting.QueryEntities<Test>(TESTGROUP);`


Honestly, I am not totally sold on the new disposable ref struct and inline using, just because people could forget to add *using*. There must be a way to force the user doing it to make it viable. I would have preferred a solution where *Dispose *is called automatically when the struct gets out of the scope and, maybe, use a new parameter modifier to instruct the code to not call (or call) dispose on ref struct passed by parameter into methods. As it is, I don’t like it much, unless I am missing something.

#### Conclusion

So in conclusion, using **EntityCollection **will be slower than used to be. The impact would probably be small and there is any way a workaround. If you really want to be fast, you need to ask for the casted buffer, through the EntityCollection methods** ToNativeBuffer() **and **ToManagedBuffer()**. problem sorted. Note that, in order to use Burst, the use of ToNativeBuffer() is necessary and, in Unity, if performance is critical, Burst must be used. *After all, this is the reason I am doing all of this.*

The only small thing that bugs me is that while it’s impossible to call ToNativeBuffer on a managed type, thanks to the* T:unmanaged* check, it’s possible to call, by mistake, ToManagedBuffer() with an unmanaged T, which would cause a runtime crash.

*That’s why I think that c# strongly needs a T:managed contraints too. T:class wouldn’t work, because T is a struct.*

I now conclude the article with the timings from the release mode Il2CPP player:

```
Iterate EC -> 8.1156
Iterate EC -> 7.8337
Iterate EC -> 8.3503
Iterate buffer -> 6.5813
Iterate buffer -> 7.6723
Iterate buffer -> 7.3025
Iterate casted buffer -> 5.5273
Iterate casted buffer -> 5.6536
Iterate casted buffer -> 4.5451
Iterate casted buffer 2 -> 5.7129
Iterate casted buffer 2 -> 5.1101
Iterate casted buffer 2 -> 5.5347
Iterate Native Array -> 0.5034
Iterate Native Array -> 0.5028
Iterate Native Array -> 0.501
Iterate array -> 0.7787
Iterate array -> 0.7975
Iterate array -> 0.7685
```


OUCH! This is not what I expected, this is way slower than mono! However IL2CPP does put a lot of extra checks that I now need to understand how to disable to feel comfortable with this. *Note that it’s also suspicious that iterating a native array is so faster in IL2CPP*. It should be the same in Mono. Something doesn’t add up. They do look like the iteration when I was profiling from inside the release editor. It’s something that I hope the unity guys will shed some light upon. My only guess is that IL2CPP C++ compilation is vectorising the iteration of the array.

#### TL;DR;

In order to abstract the memory model, Svelto.ECS EntityCollection iteration got slower. The difference in performance doesn’t really justify further optimizations, which would be very nice to have if Unity will update its mono implementation. Be also careful about how you use unity to Profile your code! Be careful with IL2CPP as it can generate code that is way slower than Mono does.

Great stuff. Where can we download 3.0? I can only find 2.9

I have been developing Svelto.ECS 3.0 the whole year, and now it’s officially out. New articles coming out soon.