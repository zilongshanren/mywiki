---
title: C# List Removal Performance
url: https://www.vertexfragment.com/ramblings/list-removal-performance/
author: Steven Sell
published: '2021-10-18'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

Recently I implemented a blue noise sampler based on the paper [Fast Poisson Disk Sampling in Arbitrary Dimensions](https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf). Part of the algorithm involves selecting random indices from a list and then removing them. This can be a fairly expensive operation in the standard `System.Collections.Generic.List<T>`

data structure as it requires a renumbering (shifting) of all elements behind it.

When you call RemoveAt to remove an item, the remaining items in the list are renumbered to replace the removed item. For example, if you remove the item at index 3, the item at index 4 is moved to the 3 position. In addition, the number of items in the list (as represented by the Count property) is reduced by 1. (

[source])

This poisson implementation isn’t the only algorithm I have implemented that requires a large amount of random element removal, and past benchmarks have shown it can eat up a significant amount of time.

So how can we speed it up? Well there is a simple solution if the order of the list does not matter. Simply swap the value at the “removed” index with the value at the back, and then remove from the back.

```
public static class ListExtensions
{
public static void RemoveUnorderedAt<T>(this List<T> list, int index)
{
list[index] = list[list.Count - 1];
list.RemoveAt(list.Count - 1);
}
}
```


A quick performance comparison later, and we can see the difference. The table shows how long it took to remove all elements from a list of a given size, in random order. All time is in milliseconds.

| 1,000 | 10,000 | 100,000 | 1,000,000 | |
|---|---|---|---|---|
`List.RemoveAt` |
0.0328 | 1.5743 | 239.997 | 75,223.3918 |
`List.RemoveUnorderedAt` |
0.0076 | 0.0796 | 0.6381 | 9.7378 |

At a million elements, the unordered removal is a 99.987% reduction in runtime.

```
using System;
using System.Collections.Generic;
using System.Diagnostics;
namespace ListDeletion
{
public static class Program
{
private static void Main(string[] args)
{
// Warm up
1000);
// Real test
1000);
PerformanceCompareListRemoval(10000);
PerformanceCompareListRemoval(100000);
PerformanceCompareListRemoval(1000000);
Console.ReadLine();
}
private static void PerformanceCompareListRemoval(int listSize)
{
List<int> listStandard = new List<int>(listSize);
List<int> listUnordered = new List<int>(listSize);
List<int> removeIndices = new List<int>(listSize);
Random rng = new Random();
// Fill the lists and pre-generate the random indices to remove.
for (int i = 0; i < listSize; ++i)
{
int v = rng.Next();
listStandard.Add(v);
listUnordered.Add(v);
removeIndices.Add(v % (listSize - i));
}
Stopwatch swStandard = Stopwatch.StartNew();
EmptyListStandard(listStandard, removeIndices);
swStandard.Stop();
Stopwatch swUnordered = Stopwatch.StartNew();
EmptyListUnordered(listUnordered, removeIndices);
swUnordered.Stop();
Console.WriteLine($"Emptied list with {listSize} items in");
Console.WriteLine($"\tRemoveAt in {swStandard.Elapsed.TotalMilliseconds} ms");
Console.WriteLine($"\tRemoveUnorderedAt in {swUnordered.Elapsed.TotalMilliseconds} ms");
}
private static void EmptyListStandard(List<int> list, List<int> removeIndices)
{
for (int i = 0; i < removeIndices.Count; ++i)
{
list.RemoveAt(removeIndices[i]);
}
}
private static void EmptyListUnordered(List<int> list, List<int> removeIndices)
{
for (int i = 0; i < removeIndices.Count; ++i)
{
list.RemoveUnorderedAt(removeIndices[i]);
}
}
}
public static class ListExtensions
{
public static void RemoveUnorderedAt<T>(this List<T> list, int index)
{
list[index] = list[list.Count - 1];
list.RemoveAt(list.Count - 1);
}
}
}
```


Assuredly this is not a novel solution, but I personally had not seen it before. However after coming up with `RemoveUnorderedAt`

I came across this in the [accompanying source](https://www.cs.ubc.ca/~rbridson/download/curlnoise.tar.gz) of the paper listed at the start of this ramble.

**util.h**

```
template<class T>
void erase_unordered(std::vector<T> &a, unsigned int index)
{
a[index]=a.back();
a.pop_back();
}
```