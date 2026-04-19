---
title: A Metric for Memory Fragmentation
url: https://asawicki.info/news_1757_a_metric_for_memory_fragmentation
published: '2022-04-06'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

Wed

06

Apr 2022

In this article, I would like to discuss the problem of memory fragmentation and propose a formula for calculating a metric telling how badly the memory is fragmented.

The problem can be stated like this:

So it is a standard memory allocation situation. Now, I will explain what do I mean by fragmentation. Fragmentation, for this article, is an unwanted situation where free memory is spread across many small regions in between allocations, as opposed to a single large one. We want to measure it and preferably avoid it because:

`VirtualAlloc`

) and sub-allocating them for the user's allocation requests, high fragmentation my require allocating another block to satisfy the request, making the program using more system memory than really needed.A solution to this problem is to perform defragmentation - an operation that moves the allocations to arrange them next to each other. This may require user involvement, as pointers to the allocations will change then. It may also be a time-consuming operation to calculate better places for the allocations and then to copy all their data. It is thus desirable to measure the fragmentation to decide when to perform the defragmentation operation.

What would be an ideal metric for memory fragmentation? Here are some properties I would like it to have: First, it should be normalized to range 0..1, or 0%..100%, with a higher number meaning higher fragmentation - more unfavorable situation. It should not depend on the size of the considered memory - same layout of allocations and free regions between them should give the same result regardless of whether their sizes are bytes or megabytes.

A single empty range is the best possible case, means no fragmentation, so it should give F = 0.

|###############|.......................

An opposite situation, the worst possible fragmentation, happens when the free space is spread evenly across free ranges in between allocations. Then, the fragmentation should be 1 or as high as possible.

........|######|........|######|........

It should not depend on the total amount of free versus allocated memory. The amount of memory acquired from the system but not used by the allocations is an important quantity, but a completely different one. Here we just want to measure how badly is this space fragmented. Following case should give the same result as the previous one:

....|############|....|############|....

The metric should not depend on the number of allocations. One large allocation should give the same result as many small ones, as long as they lie next to each other.

....|#####|.......|####################|

....|##|##|.......|###|#######|##|##|##|

Note, however, that more allocations give an opportunity for higher fragmentation if empty spaces occur between them.

Memory completely empty or completely full are two special cases that don't need to be handled. Fragmentation is undefined then. We can handle these cases separately, so the designed formula is free to return 0, 1, or even cause division by 0.

........................................

|####|#########|#######|###|###########|

How could the formula look like? First idea is to just measure the largest free region, like this:

Fragmentation_Try1 = 1 - LargestFreeRegionSize / TotalFreeSize

It will correctly return 0 when entire free memory is contained within one region. The smaller the largest free region is comparing to the total amount of free memory, the higher the fragmentation. This formula would give a not-so-bad estimate of the fragmentation. After all, it is all about being able to find a large enough continuous region for a new allocation. But there is a problem with this simple metric: it completely ignores everything besides the single largest free region. Following two situations would give the same result, while we would prefer the second situation to report higher fragmentation.

|##|##|##|........|##|..................

|##|..|##|..|##|..|##|..................

Another idea could be to consider the number of free regions between allocations. The more of them, the higher fragmentation. It sounds reasonable, as the name "fragmentation" itself means empty space divided into many fragments.

Fragmentation_Try2 = (FreeRegionCount - 1) / AllocationCount

There are problems with this formula, though. First, it considers the number of allocations, which we prefer not to do, as described above. Second and more importantly, small holes between allocations would raise the fragmentation estimate significantly, while they should have only a small influence on the result when there are also some large free regions.

|##|##|##|........|##|..................

|##|.|##|.|##|....|##|..................

I propose the following formula. Given just a list of sizes of free regions:

Quality = 0

TotalFreeSize = 0

for(int i = 0; i < FreeRegionCount; ++i)

{

Quality += FreeRegionSize[i] * FreeRegionSize[i]

TotalFreeSize += FreeRegionSize[i]

}

QualityPercent = sqrt(Quality) / TotalFreeSize

Fragmentation = 1 - (QualityPercent * QualityPercent)

If you prefer a more scientific form over a code snippet, here it is:

![Formula for memory fragmentation](../../assets/b49087ab5e278795.png)


*F* - result fragmentation metric*n* - number of free regions*f i* - size of a free region number

The whole secret here is the usage of square and square root. Final calculations are optional and only transform the result to a desired range. (1-*x*) is there to return higher number for higher fragmentation, as natively it does the opposite (therefore I called the intermediate variable "quality"). The last square is also just to change the shape of the characteristics, so it can be omitted or changed to something else if desired.

This metric fulfills most of the requirements described above. Given the array of sizes of free regions on input and observing the output, we can see that: For just one free region, fragmentation is 0:

[1000] -> F = 0

When the free space is spread evenly across two regions, it is 1/2 = 50%:

[500,500] -> F = 0.5

When there are 3 free regions of equal size, the result is 2/3 = 0.6666, for 4 regions it is 3/4 = 0.75, etc. This may be considered a flaw, as the result is not 1, despite we are talking about the worst possible fragmentation situation here. It also depends on the number of free regions and it approaches 1, as we have more of them. For example, 20 equal free ranges give fragmentation = 95%:

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] -> F = 0.95

Everything else works as desired. Having one free region larger and one smaller gives fragmentation estimate lower than 50%:

[200,800] -> F = 0.32

Adding some tiny holes between allocations doesn't change the result much:

[200,800,1,1,1,1] -> F = 0.3254

I am quite happy with this formula. I think it can be used to estimate memory fragmentation, for example, to benchmark various allocation algorithms or to decide whether it is time to defragment.

I came up with this formula a few months ago, after discussions with my friend Łukasz Izdebski. The whole topic of memory allocation is my area of interest because I develop [Vulkan Memory Allocator](https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator/) and [D3D12 Memory Allocator](https://github.com/GPUOpen-LibrariesAndSDKs/D3D12MemoryAllocator/) libraries as part of my work at AMD.

I didn't research prior work that has been done on this subject too thoroughly. Now I can see my idea is not new. I googled for "formula memory fragmentation metric" and [the very first result](https://github.com/rhempel/umm_malloc/issues/14) mentions the same formula, using square root of sum of squares of free region sizes.

Everything I described above was about a single block of memory. If an allocator manages an entire set of such blocks, we can talk about completely distinct problems. For example, a defragmentation operation could move some allocations out of an almost-empty block to return it to the system. This would be the most desirable outcome, so finding such opportunities is far more important than measuring how bad is the fragmentation in a single block.

[Comments](https://asawicki.info/news_1757_a_metric_for_memory_fragmentation#disqus_thread) |
[#gpu](https://asawicki.info/news?x=tag&tag=gpu) [#algorithms](https://asawicki.info/news?x=tag&tag=algorithms) [#optimization](https://asawicki.info/news?x=tag&tag=optimization)
[Share](http://www.addtoany.com/share_save?linkurl=https%3A%2F%2Fasawicki.info%2F%2Fnews_1757_a_metric_for_memory_fragmentation&linkname=A+Metric+for+Memory+Fragmentation)