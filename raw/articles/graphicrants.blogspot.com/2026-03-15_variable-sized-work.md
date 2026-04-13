---
title: Variable sized work
url: http://graphicrants.blogspot.com/2026/03/variable-sized-work.html
author: Brian Karis
published: '2026-03-15'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Really what is desired is the ability to enqueue

**variable sized**work at a

**constant cost**to the producer that gets

**perfectly packed into waves**by the consumer. This is a frustratingly common problem in my experience and there is no good general purpose parallel programming primitive that I’m aware of that addresses it.

This turns out to be an extremely similar problem to rasterization where triangles are large or pixel shaders are reasonably expensive. 1 triangle expands to a variable number of pixels. That pixel work must be distributed across many threads and packed into waves. There’s more things that are rasterization specific to efficiently match up to the ROP but from a high level this is the same general problem.

In fact it is so similar that the HW rasterizer could be abused for this purpose. A generator task runs in VS and produces a variable amount of child work items, which are the pixels. The PS work can then access data from the generator task using interpolators. Using rect lists where the rects are 2xN allows the finest granularity of work expansion. There is weirdness though because of this abuse. HW rasterizers can have static assignment of pixel tiles to units, serialize on overlapping in a tile, and other things that make sense for pixels but not for arbitrary work. I did make this experiment though I jokingly called rasterizer inception since I was running a SW rasterizer inside a HW rasterizer. It was not competitive against the design I will explain.

### Minimize data movement

The other problem with small TessFactors is the cost of queuing itself. This gets to an often misunderstood aspect of Nanite. Why is Nanite’s software rasterization faster than hardware? I always have to preface this topic with the fact that I am not a hardware engineer nor do I have access to the details of any GPU’s rasterizer block.Many think the primary reason is because of pixel quads, or that it isn’t more efficient, it just uses more power, or more transistors on the task at once. Those are true but I don’t think that’s the core of the issue.

I believe it is more about data movement. Assuming the hardware is roughly similar to tile based software rasterizers like

[cudaraster](https://research.nvidia.com/publication/2011-08_high-performance-software-rasterization-gpus)or

[cuRE](https://www.tugraz.at/institute/icg/research/team-steinberger/research-projects/gpu-rendering-pipelines/cure/). Triangles get setup, that means calculating depth and attribute planes, edge equations, and bounding boxes. Those will be stored somewhere so the following stages can access them. Already this is a significant amount of data. Then the triangle gets binned, meaning added to tile lists. This might be hierarchical. That means multiple passes of reading an index from a list and a mask, then reading the triangle data to compute a new mask, then write out the index and masks again. Doing prefix sums of the masks to repack into dense waves of work. All of this is optimized and balanced for typical workloads that are pixel bound, the amount of triangles that can be setup in 1 clock, the size of caches and queues.

What the Nanite software rasterizer does instead of binning, it just writes the pixels. No need for any of the state from triangle setup to leave registers or to move at all. The amount of pixel work is small enough that expanding, consolidating, distributing, and repacking it is more expensive than just doing it.

## Local work distribution

The same data movement concern is present with tessellation. As already explained there is more generated work than the simple rasterization case such that load balancing of some kind is required, but there is also a lot of state that makes distributing that work expensive. So instead of either writing it all out to memory or rederiving it, a local approach is used. Redistribute the work only across the wave, keep the state in registers, and read it using`WaveReadLaneAt`

if it isn’t scalar.A wave starts first by deciding how much work it will produce. Each lane writes the number of items it is producing to the work queue. Then the wave switches to consuming work from the queue, a wave worth of work in each iteration until the queue is empty. A consuming lane gets the index of the producing lane and an index of which item from that producing lane it is consuming. Data for the work itself is read from the producing lane using

`WaveReadLaneAt`

or is scalar and was shared by all producing lanes.Threads are thus dynamically assigned to the work instead of statically. They are only empty and idling in the last iteration of the loop, the last wave worth of packed work. This isn’t without drawbacks. It can only distribute work amongst lanes of the same wave, no further. This means state doesn’t need to be put on the queue itself, it can be read directly from the producer by the consumer, but it also means it is a very limited form of load balancing. Care must be taken to not to produce too much work or the advantages will be outweighed by the rest of the machine idling waiting for 1 wave to retire.

```
groupshared uint WorkBatch[ THREADGROUP_SIZE ];
template< typename FTask >
void DistributeWork( FTask Task, uint GroupIndex, uint NumWorkItems )
{
const uint LaneCount = WaveGetLaneCount();
const uint LaneIndex = GroupIndex & ( LaneCount - 1 );
const uint QueueOffset = GroupIndex & ~( LaneCount - 1 );
uint FirstWorkItem = WavePrefixSum( NumWorkItems );
uint TotalWorkItems = WaveReadLaneAt( FirstWorkItem + NumWorkItems, LaneCount - 1 );
uint SourceData = ( FirstWorkItem << 8 ) | LaneIndex;
// Pull work from queue
for( uint BatchFirstItem = 0; BatchFirstItem < TotalWorkItems; BatchFirstItem += LaneCount )
{
uint ItemIndex = BatchFirstItem + LaneIndex;
WorkBatch[ GroupIndex ] = 0xFFFFFFFFu;
GroupMemoryBarrier();
if( NumWorkItems > 0u )
{
// Mark the first work item present in the batch for each source.
int FirstItemLane = int( FirstWorkItem - BatchFirstItem );
if( FirstItemLane < ( int )LaneCount && FirstItemLane + ( int )NumWorkItems - 1 >= 0 )
WorkBatch[ QueueOffset + max( FirstItemLane, 0 ) ] = SourceData;
}
GroupMemoryBarrier();
uint BatchValue = WorkBatch[ GroupIndex ];
uint BatchMask = WaveActiveBallot( BatchValue != 0xFFFFFFFFu ).x;
// Highest Index <= LaneIndex with a bit set
uint BatchLane = firstbithigh( BatchMask & ~( 0xFFFFFFFEu << LaneIndex ) );
// This is where we wrote SourceData relevant to this item.
uint SourceValue = WaveReadLaneAt( BatchValue, BatchLane );
uint SourceLane = SourceValue & 0xFFu;
uint LocalItemIndex = ItemIndex - ( SourceValue >> 8 );
bool bActive = ItemIndex < TotalWorkItems;
Task.RunChild( bActive, SourceLane, LocalItemIndex );
}
}
```


For brevity this code assumes wave32. Thanks to Rune for optimizing the original code to not need compaction when `NumWorkItems == 0`

.### Step through

I'll walk through how this works with example VGPR state. To make it easier to follow, let's pretend the wave size is 8. I replaced the packed`SourceData`

values with letters. It's more important to track where those get scattered to than caring about what the values are themselves.| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | |
| NumWorkItems | 12 | 2 | 5 | 1 | 0 | 6 | 10 | 14 |
| FirstWorkItem | 0 | 12 | 14 | 19 | 20 | 20 | 26 | 36 |
| SourceData | A | B | C | D | E | F | G | H |

`BatchFirstItem == 16`

. Only some work sources have a nonzero amount of work that fits in this batch's window. Specifically lanes 2, 3, 5 corresponding to SourceData C, D, F. I’ll color code any values associated with these sources.| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | |
| SourceData | A | B | C | D | E | F | G | H |
| FirstItemLane | -16 | -14 | -2 | 3 | 4 | 4 | 10 | 20 |

`max( FirstItemLane, 0 )`

in groupshared and then pulled back to VGPR as `BatchValue`

.| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | |
| BatchValue | C | D | F | |||||
| BatchLane | 0 | 0 | 0 | 3 | 4 | 4 | 4 | 4 |
| SourceData | C | C | C | D | F | F | F | F |
| SourceLane | 2 | 2 | 2 | 3 | 5 | 5 | 5 | 5 |
| LocalItemIndex | 2 | 3 | 4 | 0 | 0 | 1 | 2 | 3 |

`SourceLane`

’s and `LocalItemIndex`

’s. If you laid all the batches out head to tail that's what they'd look like. You can see that C’s items started in the last batch and F’s items will be completed in the next batch.### Applied

This local work distribution is a generally useful parallel programming primitive. In the tessellation use case the producer is a patch with TessFactors. It knows from the Tessellation Table how many triangles that will be produced (`NumWorkItems`

) and enqueues that work. No other patch state needs to be written to a queue. A consumer reads the source patch state directly from registers. That state includes which Tessellation Pattern to use and combines it with the item’s index to read from the Tessellation Table to produce a tessellated triangle output.This tool is used for immediate dicing and rasterization in

**ClusterRasterize**

when TessFactors <= MaxDiceFactor for the base patch. The work that is distributed is the diced triangles. The same is done for splitting. SplitFactors were already calculated so it would be a shame to do that again redundantly in **PatchSplit**

. Instead 1 step of splitting is done immediately in **ClusterRasterize**

. The writing of each subpatch to the split queue is distributed across the wave. The third place this is used is in **PatchSplit**

. Again there are SplitFactors calculated for a patch but the actual work of splitting is variable in size and may be significant. Calculating the barycentrics for the child subpatches and writing them to the split queue is distributed across the wave.
## No comments:

Post a Comment