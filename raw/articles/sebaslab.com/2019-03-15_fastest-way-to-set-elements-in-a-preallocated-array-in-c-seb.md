---
title: Fastest way to set elements in a preallocated array in c# - Seba's Lab
url: https://www.sebaslab.com/fastest-way-to-iterate-an-array-in-csharp/
author: Sebastiano Mandalà
published: '2019-03-15'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Finally I found the time to play with *unmanaged arrays* and *Memory<T>/Span<T>*. In order to investigate possible improvements of the data structures used by [Svelto.ECS](https://github.com/sebas77/Svelto.ECS), I wanted to know what the fastest way to set elements in a preallocated array could be. Using the very powerful [BenchmarkDotNet](https://github.com/dotnet/BenchmarkDotNet) and with the help of the .net community, I got my answer:

```
| Method | Runtime | Toolchain | Mean | Error | StdDev | Median |
|------------------------------- |-------- |----------------------------- |----------:|----------:|----------:|----------:|-
| StandardArrayInsert | Clr | net472 | 4.332 ms | 0.0185 ms | 0.0173 ms | 4.328 ms |
| StandardArrayInsert | Core | netcoreapp3.0 | 4.587 ms | 0.0405 ms | 0.0379 ms | 4.591 ms |
| StandardArrayInsert | CoreRT | Core RT 1.0.0-alpha-27515-01 | 4.623 ms | 0.0455 ms | 0.0403 ms | 4.607 ms |
| StandardArrayInsert | Mono | Default | 6.002 ms | 0.0103 ms | 0.0092 ms | 6.000 ms |
| | | | | | | |
| StandardUnmanagedArrayInsert | Clr | net472 | 4.331 ms | 0.0324 ms | 0.0304 ms | 4.345 ms |
| StandardUnmanagedArrayInsert | Core | netcoreapp3.0 | 4.336 ms | 0.0197 ms | 0.0175 ms | 4.329 ms |
| StandardUnmanagedArrayInsert | CoreRT | Core RT 1.0.0-alpha-27515-01 | 4.399 ms | 0.0394 ms | 0.0349 ms | 4.400 ms |
| StandardUnmanagedArrayInsert | Mono | Default | 4.882 ms | 0.0199 ms | 0.0186 ms | 4.878 ms |
| | | | | | | |
| StandardPinnedArrayInsert | Clr | net472 | 4.330 ms | 0.0073 ms | 0.0061 ms | 4.330 ms |
| StandardPinnedArrayInsert | Core | netcoreapp3.0 | 4.440 ms | 0.0981 ms | 0.1666 ms | 4.359 ms |
| StandardPinnedArrayInsert | CoreRT | Core RT 1.0.0-alpha-27515-01 | 4.425 ms | 0.0263 ms | 0.0233 ms | 4.425 ms |
| StandardPinnedArrayInsert | Mono | Default | 4.877 ms | 0.0140 ms | 0.0131 ms | 4.880 ms |
| | | | | | | |
| StandardListInsert | Clr | net472 | 15.693 ms | 0.0402 ms | 0.0376 ms | 15.684 ms |
| StandardListInsert | Core | netcoreapp3.0 | 15.690 ms | 0.0733 ms | 0.0650 ms | 15.670 ms |
| StandardListInsert | CoreRT | Core RT 1.0.0-alpha-27515-01 | 16.058 ms | 0.1697 ms | 0.1587 ms | 16.077 ms |
| StandardListInsert | Mono | Default | 29.432 ms | 0.2700 ms | 0.2525 ms | 29.518 ms |
| | | | | | | |
| StandardManagedSpanInsert | Clr | net472 | 6.713 ms | 0.0174 ms | 0.0145 ms | 6.707 ms |
| StandardManagedSpanInsert | Core | netcoreapp3.0 | 4.861 ms | 0.0208 ms | 0.0195 ms | 4.861 ms |
| StandardManagedSpanInsert | CoreRT | Core RT 1.0.0-alpha-27515-01 | 4.891 ms | 0.0199 ms | 0.0186 ms | 4.886 ms |
| StandardManagedSpanInsert | Mono | Default | 13.833 ms | 0.0294 ms | 0.0245 ms | 13.827 ms |
| | | | | | | |
| StandardUnmanagedSpanInsert | Clr | net472 | 6.717 ms | 0.0161 ms | 0.0150 ms | 6.719 ms |
| StandardUnmanagedSpanInsert | Core | netcoreapp3.0 | 4.849 ms | 0.0171 ms | 0.0143 ms | 4.847 ms |
| StandardUnmanagedSpanInsert | CoreRT | Core RT 1.0.0-alpha-27515-01 | 4.861 ms | 0.0283 ms | 0.0265 ms | 4.854 ms |
| StandardUnmanagedSpanInsert | Mono | Default | 12.620 ms | 0.0376 ms | 0.0352 ms | 12.620 ms |
| | | | | | | |
| StandardUnmanagedSpanBenInsert | Clr | net472 | 4.846 ms | 0.0123 ms | 0.0115 ms | 4.845 ms |
| StandardUnmanagedSpanBenInsert | Core | netcoreapp3.0 | 4.887 ms | 0.0569 ms | 0.0559 ms | 4.868 ms |
| StandardUnmanagedSpanBenInsert | CoreRT | Core RT 1.0.0-alpha-27515-01 | 4.859 ms | 0.0259 ms | 0.0242 ms | 4.847 ms |
| StandardUnmanagedSpanBenInsert | Mono | Default | 5.079 ms | 0.0288 ms | 0.0269 ms | 5.068 ms |
```


The code is very straightforward:

```
using System;
using System.Buffers;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Configs;
using BenchmarkDotNet.Running;
namespace Svelto.DataStructures
{
public unsafe class UnmanagedMemoryManager<T> : MemoryManager<T>
{
readonly int _elementCount;
readonly IntPtr _ptr;
public UnmanagedMemoryManager(int elementCount)
{
_elementCount = elementCount;
_ptr = Marshal.AllocHGlobal(elementCount * Unsafe.SizeOf<T>());
}
protected override void Dispose(bool disposing)
{
Marshal.FreeHGlobal(_ptr);
}
public override Span<T> GetSpan()
{
return new Span<T>((void*) _ptr, _elementCount);
}
public override MemoryHandle Pin(int elementIndex)
{
throw new Exception();
}
public override void Unpin()
{
throw new Exception();
}
}
//[DisassemblyDiagnoser(printAsm: true, printSource: true)] // !!! use the new diagnoser!!
//[ClrJob, MonoJob, CoreJob]
// [EtwProfiler]
// [HardwareCounters(HardwareCounter.BranchMispredictions,HardwareCounter.BranchInstructions)]
//CoreRt --coreRtVersion "1.0.0-alpha-27515-01"
//[MaxWarmupCount(2)]
//[MaxIterationCount(2)]
//[MinWarmupCount(1)]
//[MinIterationCount(1)]
[GroupBenchmarksBy(BenchmarkLogicalGroupRule.ByCategory)]
public unsafe class ArrayBenchmark
{
int* unmanagedArray;
Memory<int> unmanagedMemory;
int* arrayPinned;
GCHandle arrayPinnedGC;
int[] managedArray;
List<int> list;
UnmanagedMemoryManager<int> unmanagedMemoryManager;
Memory<int> managedMemory;
const int DictionarySize = 10_000_000;
const int DictionarySizeSmall = 1_000_000;
int[] RandomAccess = new int[DictionarySize];
[GlobalSetup]
public void GlobalSetupA()
{
unmanagedArray = (int*) Marshal.AllocHGlobal(DictionarySize * sizeof(int));
arrayPinnedGC = GCHandle.Alloc(new int[DictionarySize], GCHandleType.Pinned);
arrayPinned = (int*) arrayPinnedGC.AddrOfPinnedObject();
unmanagedMemoryManager = new UnmanagedMemoryManager<int>(DictionarySize);
unmanagedMemory = unmanagedMemoryManager.Memory;
managedMemory = new Memory<int>(new int[DictionarySize]);
managedArray = new int[DictionarySize];
list = new List<int>(DictionarySize);
var random = new Random();
for (int i = 0; i < list.Capacity; i++)
{
list.Add(i);
RandomAccess[i] = random.Next() % DictionarySize;
}
}
[GlobalCleanup]
public void GlobalCleanUpA()
{
Marshal.FreeHGlobal(new IntPtr(unmanagedArray));
arrayPinnedGC.Free();
((IDisposable) unmanagedMemoryManager).Dispose();
}
[Benchmark(Baseline = true), BenchmarkCategory("StandardArrayInsert")]
public void StandardArrayInsert()
{
for (int i = 0; i < managedArray.Length; i++) managedArray[i] = i;
}
[Benchmark, BenchmarkCategory("StandardUnmanagedArrayInsert")]
public void StandardUnmanagedArrayInsert()
{
for (int i = 0; i < DictionarySize; i++) unmanagedArray[i] = i;
}
[Benchmark, BenchmarkCategory("StandardPinnedArrayInsert")]
public void StandardPinnedArrayInsert()
{
for (int i = 0; i < DictionarySize; i++) arrayPinned[i] = i;
}
[Benchmark, BenchmarkCategory("StandardListInsert")]
public void StandardListInsert()
{
for (int i = 0; i < list.Count; i++) list[i] = i;
}
[Benchmark, BenchmarkCategory("StandardManagedSpanInsert")]
public void StandardManagedSpanInsert()
{
var sarray = managedMemory.Span;
for (int i = 0; i < sarray.Length; i++) sarray[i] = i;
}
[Benchmark, BenchmarkCategory("StandardUnmanagedSpanInsert")]
public void StandardUnmanagedSpanInsert()
{
var sarray = unmanagedMemory.Span;
for (int i = 0; i < sarray.Length; i++) sarray[i] = i;
}
[Benchmark, BenchmarkCategory("StandardUnmanagedSpanBenInsert")]
public void StandardUnmanagedSpanBenInsert()
{
var sarray = unmanagedMemory.Span;
ref var firstElement = ref MemoryMarshal.GetReference(sarray);
for (int i = 0; i < sarray.Length; i++) Unsafe.Add(ref firstElement, i) = i;
}
[Benchmark, BenchmarkCategory("StandardArrayInsertChecked")]
public void StandardArrayInsertChecked()
{
for (int i = 0; i < DictionarySizeSmall; i++)
managedArray[RandomAccess[i]] = i;
}
[Benchmark, BenchmarkCategory("StandardUnmanagedArrayInsertChecked")]
public void StandardUnmanagedArrayInsertChecked()
{
for (int i = 0; i < DictionarySizeSmall; i++) unmanagedArray[RandomAccess[i] ] = i;
}
[Benchmark, BenchmarkCategory("StandardPinnedArrayInsertChecked")]
public void StandardPinnedArrayInsertChecked()
{
for (int i = 0; i < DictionarySizeSmall; i++) arrayPinned[RandomAccess[i] ] = i;
}
[Benchmark, BenchmarkCategory("StandardListInsertChecked")]
public void StandardListInsertChecked()
{
for (int i = 0; i < DictionarySizeSmall; i++) list[RandomAccess[i] ] = i;
}
[Benchmark, BenchmarkCategory("StandardManagedSpanInsertChecked")]
public void StandardManagedSpanInsertChecked()
{
var sarray = managedMemory.Span;
for (int i = 0; i < DictionarySizeSmall; i++) sarray[RandomAccess[i]] = i;
}
[Benchmark, BenchmarkCategory("StandardUnmanagedSpanInsertChecked")]
public void StandardUnmanagedSpanInsertChecked()
{
var sarray = unmanagedMemory.Span;
for (int i = 0; i < DictionarySizeSmall; i++) sarray[RandomAccess[i] ] = i;
}
[Benchmark, BenchmarkCategory("StandardUnmanagedSpanBenInsertChecked")]
public void StandardUnmanagedSpanBenInsertChecked()
{
var sarray = unmanagedMemory.Span;
ref var firstElement = ref MemoryMarshal.GetReference(sarray);
for (int i = 0; i < DictionarySizeSmall; i++) Unsafe.Add(ref firstElement, RandomAccess[i] ) = i;
}
}
class Program
{
static void Main(string[] args)
{
//BenchmarkRunner.Run<ArrayBenchmark>();
BenchmarkSwitcher.FromAssembly(typeof(Program).Assembly).Run(args, DefaultConfig.Instance);
}
}
}
```


Some considerations:

Pinning large arrays is obviously not the way to go, I just wanted to see if there was any difference with using native memory (allocated through AllocHGlobal). As suspected, using unsafe pointers is the fastest option.

Span<T> using native memory is actually faster than I thought! Very close! However, using mono (Unity) I just can’t iterate a span using the operator[] as Mono still doesn’t support the optimized span implementation (still much faster than using a list). [Ben Adams](https://twitter.com/ben_a_adams), supreme bearer of

.net knowledge, suggested the solution that you can check in the “*StandardUnmanagedSpanBenInsert*” benchmark. However, I have to say, iterating an old plain c# array is not that slow either, which is surprising, isn’t it? Where are the bounding checks that should make c# arrays slower to iterate? *Well if you check the assembly they are actually not there. The jitter is smart enough to understand that the index can never go outside the bounds so they are disabled!* That’s why I had to add a version with random access, *which is 10 times slower *(however it’s very likely so because of cache misses and not because of random access). Let’s see the assembly:

![](../../assets/3a61f57dd055e6ec.png)


![](../../assets/3a61f57dd055e6ec.png)

As you can see the **ArrayInsertChecked **as one extra compare compared to **UnmanagedArrayInsertChecked**. However the cpu clocks taken by the extra compare are nothing compared to the time spent in cache misses. Now the results (not these functions iterate 10 times less to have comparable results, however as you can see the time lost inside extra compare is almost nothing compared to cpu cache misses)

```
| StandardArrayInsertChecked | Clr | net472 | 9.943 ms | 0.1525 ms | 0.1273 ms | 10.002 ms |
| StandardArrayInsertChecked | Core | netcoreapp3.0 | 9.884 ms | 0.0557 ms | 0.0521 ms | 9.894 ms |
| StandardArrayInsertChecked | CoreRT | Core RT 1.0.0-alpha-27515-01 | 9.963 ms | 0.1039 ms | 0.0972 ms | 9.974 ms |
| StandardArrayInsertChecked | Mono | Default | 9.864 ms | 0.0782 ms | 0.0732 ms | 9.840 ms |
| | | | | | | |
| StandardUnmanagedArrayInsertChecked | Clr | net472 | 9.965 ms | 0.1772 ms | 0.1657 ms | 9.952 ms |
| StandardUnmanagedArrayInsertChecked | Core | netcoreapp3.0 | 9.856 ms | 0.0739 ms | 0.0655 ms | 9.862 ms |
| StandardUnmanagedArrayInsertChecked | CoreRT | Core RT 1.0.0-alpha-27515-01 | 10.118 ms | 0.3387 ms | 0.5752 ms | 9.794 ms |
| StandardUnmanagedArrayInsertChecked | Mono | Default | 9.693 ms | 0.0613 ms | 0.0512 ms | 9.690 ms |
| | | | | | | |
| StandardPinnedArrayInsertChecked | Clr | net472 | 10.447 ms | 0.2051 ms | 0.4097 ms | 10.488 ms |
| StandardPinnedArrayInsertChecked | Core | netcoreapp3.0 | 9.855 ms | 0.0731 ms | 0.0684 ms | 9.819 ms |
| StandardPinnedArrayInsertChecked | CoreRT | Core RT 1.0.0-alpha-27515-01 | 9.992 ms | 0.1168 ms | 0.1093 ms | 9.984 ms |
| StandardPinnedArrayInsertChecked | Mono | Default | 9.860 ms | 0.0704 ms | 0.0658 ms | 9.883 ms |
| | | | | | | |
| StandardListInsertChecked | Clr | net472 | 13.905 ms | 0.2169 ms | 0.2029 ms | 13.912 ms |
| StandardListInsertChecked | Core | netcoreapp3.0 | 13.424 ms | 0.0504 ms | 0.0394 ms | 13.419 ms |
| StandardListInsertChecked | CoreRT | Core RT 1.0.0-alpha-27515-01 | 13.451 ms | 0.2548 ms | 0.2384 ms | 13.400 ms |
| StandardListInsertChecked | Mono | Default | 14.111 ms | 0.0390 ms | 0.0304 ms | 14.108 ms |
| | | | | | | |
| StandardManagedSpanInsertChecked | Clr | net472 | 10.327 ms | 0.2021 ms | 0.2963 ms | 10.350 ms |
| StandardManagedSpanInsertChecked | Core | netcoreapp3.0 | 9.921 ms | 0.0489 ms | 0.0457 ms | 9.914 ms |
| StandardManagedSpanInsertChecked | CoreRT | Core RT 1.0.0-alpha-27515-01 | 9.922 ms | 0.1527 ms | 0.1428 ms | 9.922 ms |
| StandardManagedSpanInsertChecked | Mono | Default | 10.040 ms | 0.0862 ms | 0.0807 ms | 10.053 ms |
| | | | | | | |
| StandardUnmanagedSpanInsertChecked | Clr | net472 | 9.934 ms | 0.2766 ms | 0.2840 ms | 9.799 ms |
| StandardUnmanagedSpanInsertChecked | Core | netcoreapp3.0 | 9.871 ms | 0.0702 ms | 0.0622 ms | 9.883 ms |
| StandardUnmanagedSpanInsertChecked | CoreRT | Core RT 1.0.0-alpha-27515-01 | 9.844 ms | 0.0872 ms | 0.0815 ms | 9.829 ms |
| StandardUnmanagedSpanInsertChecked | Mono | Default | 9.766 ms | 0.0812 ms | 0.0760 ms | 9.769 ms |
| | | | | | | |
| StandardUnmanagedSpanBenInsertChecked | Clr | net472 | 10.697 ms | 0.2134 ms | 0.5546 ms | 10.560 ms |
| StandardUnmanagedSpanBenInsertChecked | Core | netcoreapp3.0 | 9.930 ms | 0.1229 ms | 0.1150 ms | 9.921 ms |
| StandardUnmanagedSpanBenInsertChecked | CoreRT | Core RT 1.0.0-alpha-27515-01 | 9.910 ms | 0.1249 ms | 0.1168 ms | 9.876 ms |
| StandardUnmanagedSpanBenInsertChecked | Mono | Default | 10.262 ms | 0.3184 ms | 0.5406 ms | 9.980 ms |
```


Conclusion:

- Span are very fast with net core, not that fast in net framework, slow with Mono
- using unsafe pointers is the fastest solution
- pure arrays are as fast, when they are not checked
- the jitter is smart!
- your worst enemy is the cache miss
- for what I can see, I don’t think is worth to use unmanaged memory for array of int and structs.

**Note**: all the reasoning above make sense only if we talk about unmanaged structs and value types. For array of objects more complicated operations happen, because of the garbage collector, and the difference may be much more important between managed and unmanaged code. However for my purposes I need to take in consideration only pure value types.

P.S.: I enabled the CoreRT version just for fun, but basically there isn’t any difference. I should check with Unity IL2CPP too.