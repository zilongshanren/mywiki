---
title: Demonizing Nested Loops
url: https://www.vertexfragment.com/ramblings/demonizing-nested-loops/
author: Steven Sell
published: '2019-12-13'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

Frequently I hear/read other developers demonizing nested loops and immediately casting them as something that needs to be fixed. The majority of the time this is at best backed up by a claim that a nested loop always results in poor performance (despite the fact that they ignore performance impacts in the rest of their code) and that the vague “they” say that a nested loop should never be used.

To this I disagree.

Before going any further this is not a condoning of all nested loops or arguing against refactoring them to single loops or unrolling the loop entirely. This is however a condemnation against the blanket condemnation of all nested loops.

Let’s look at a simple scenario. I have seen a similar loop used as an interview question where the interviewee is asked to perform a review of a chunk of code. Nearly all of them mention that the nested loop could be turned into a single loop for a “performance gain.” When asked why it would be a performance gain they typically respond with a statement about Big O complexity.

Here is the loop:

```
for (int y = 0; y < iterations; ++y)
{
for (int x = 0; x < iterations; ++x)
{
// Do thing.
```


Refactored to a single loop:

```
int iterationsSquared = iterations * iterations;
for (int i = 0; i < iterationsSquared; ++i)
{
// x = (i % iterations)
// y = (i / iterations)
// Do thing.
```


And because I know someone would suggest LINQ:

```
var coords = from y in Enumerable.Range(0, iterations)
from x in Enumerable.Range(0, iterations)
select new { x, y };
foreach (var coord in coords)
{
// x = coord.x
// y = coord.y
// Do thing.
```


After calculating an average elapsed ticks for each of the above approaches, with 10 samples and `iterations=10000`

, we see the following result on my development machine running .NET Core 3.1:

| Approach | Average Ticks | % Best |
|---|---|---|
| Nested | 4,153,902 | 100% |
| Single | 6,703,180 | 161.37% |
| LINQ | 26,875,268 | 646.99% |

Some may say the above test was overly simple or contrived, but many of those developers would also shun the nested solution before seeing any results.

Which comes to my final point: one should write their code for readability/maintainability until proper benchmarking demonstrates a need otherwise. Fortunately for me I believe the nested solution is the easiest to read and it is the most performant.

The code used to perform this test can be found below.

```
using System;
using System.Diagnostics;
using System.Linq;
namespace NetCoreLoopComparison
{
public static class Program
{
private const int Iterations = 10000;
private const int TestSamples = 10;
static void Main()
{
Console.WriteLine("Warming up ...");
LoopNested(Iterations, DoThing);
LoopSingle(Iterations, DoThing);
LoopLinq(Iterations, DoThing);
Console.WriteLine("Beginning benchmark ...");
long cumulativeNestedTicks = 0, cumulativeSingleTicks = 0, cumulativeLinqTicks = 0;
for (int i = 0; i < TestSamples; ++i)
{
Console.WriteLine($"Test #{i + 1} ...");
var resultNestedTick = SampleCase(LoopNested, DoThing);
cumulativeNestedTicks += resultNestedTick;
Console.WriteLine($"\tNested: {resultNestedTick}");
var resultSingleTick = SampleCase(LoopSingle, DoThing);
cumulativeSingleTicks += resultSingleTick;
Console.WriteLine($"\tSingle: {resultSingleTick}");
var resultLinqTick = SampleCase(LoopLinq, DoThing);
cumulativeLinqTicks += resultLinqTick;
Console.WriteLine($"\tLINQ: {resultLinqTick}");
}
float nestedAvg = cumulativeNestedTicks / TestSamples;
float singleAvg = cumulativeSingleTicks / TestSamples;
float linqAvg = cumulativeLinqTicks / TestSamples;
float minAvg = Math.Min(nestedAvg, Math.Min(singleAvg, linqAvg));
Console.WriteLine($"Average ...");
Console.WriteLine($"\tNested:\t{nestedAvg} ({(nestedAvg / minAvg) * 100.0f}%)");
Console.WriteLine($"\tSingle:\t{singleAvg} ({(singleAvg / minAvg) * 100.0f}%)");
Console.WriteLine($"\tLINQ: \t{linqAvg} ({(linqAvg / minAvg) * 100.0f}%)");
}
static long SampleCase(Action<int, Action<int, int>> sample, Action<int, int> operation)
{
Stopwatch time = new Stopwatch();
time.Start();
sample(Iterations, operation);
time.Stop();
return time.Elapsed.Ticks;
}
static void LoopNested(int dimension, Action<int, int> operation)
{
for (int y = 0; y < dimension; ++y)
{
for (int x = 0; x < dimension; ++x)
{
operation(x, y);
}
}
}
static void LoopSingle(int dimension, Action<int, int> operation)
{
int total = (dimension * dimension);
for (int i = 0; i < total; ++i)
{
operation(i % dimension, i / dimension);
}
}
static void LoopLinq(int dimension, Action<int, int> operation)
{
var coords = from y in Enumerable.Range(0, dimension)
from x in Enumerable.Range(0, dimension)
select new { x, y };
foreach (var coord in coords)
{
operation(coord.x, coord.y);
}
}
static void DoThing(int x, int y)
{
int total = x + y;
}
}
}
```