---
title: 'Game Programming: Time Slicing | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2021/05/time-slicing/
author: Allen Chou
published: '2021-05-28'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Source files and future updates are available on [Patreon](https://www.patreon.com/TheAllenChou).

You can follow me on [Twitter](https://twitter.com/TheAllenChou).

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

## Prerequisite

## Introduction

In the previous tutorial, I used exposure avoidance as an example to demonstrate how to optimize computation with delayed result gathering. The basic idea is: kick jobs to run on worker threads and gather the results later. This prevents the main thread from being stalled.

If the game can afford one-frame latency, then we can kick the job in one frame and gather the results in the next frame. If the game cannot afford such latency, it’s still worth trying kicking the job early and gather the results later in the same frame.

What if the job takes too long to fit in a single frame? Or what if the job is just taking longer than we’d like? Then we can split the work across multiple frames. This is the core idea of time slicing, another optimization technique I picked up at work and one of my longtime favorites.

If you think about it, time slicing is everywhere. Texture streaming, seamless loading, etc., work that happens “in the background” without tanking a game’s frame rate. Can’t do it all in one frame? Then do it across multiple! It’s a simple but very effective idea.

## The Exposure Map Example Revisited

Recall our [last iteration](http://allenchou.net/2021/05/delayed-result-gathering/) on the exposure map example. The jobs to set up raycasts, perform raycasts, and gather raycast results are kicked at the end of the update function and waited for completion at the start of the update function in the next frame.

Here are the job structs:

```
struct RaycastSetupJob : IJobParallelFor
{
public Vector3 EyePos;
[ReadOnly]
public NativeArray<Vector3> Grid;
[WriteOnly]
public NativeArray<RaycastCommand> Commands;
public void Execute(int index)
{
Vector3 cellCenter = Grid[index];
Vector3 vec = cellCenter - EyePos;
Commands[index] =
new RaycastCommand(EyePos, vec.normalized, vec.magnitude);
}
}
struct RaycastGatherJob : IJobParallelFor
{
[ReadOnly]
public NativeArray<RaycastHit> Results;
[WriteOnly]
public NativeArray<bool> ExposureMap;
public void Execute(int index)
{
bool exposed = (Results[index].distance <= 0.0f);
ExposureMap[index] = exposed;
}
}
```

Here is the update function:

```
id UpdateExposureMap()
{
// wait for jobs from last frame to complete
hGatherJob.Complete();
// double-buffering
SwapExposureBackBuffer();
// dispose of job data allocated from last frame
if (Commands.IsCreated)
Commands.Dispose();
if (Results.IsCreated)
Results.Dispose();
// allocate data shared across jobs
var allocator = Allocator.TempJob;
Commands =
new NativeArray<RaycastCommand>(NumCells, allocator);
Results =
new NativeArray<RaycastHit>(NumCells, allocator);
// create setup job
var setupJob = new RaycastSetupJob();
setupJob.EyePos = EyePos;
setupJob.Grid = Grid;
setupJob.Commands = Commands;
// create gather job
var gatherJob = new RaycastGatherJob();
gatherJob.Results = Results;
gatherJob.ExposureMap = ExposureMap;
// schedule setup job
var hSetupJob = setupJob.Schedule(NumCells, JobBatchSize);
// schedule raycast job
// specify dependency on setup job
var hRaycastJob =
RaycastCommand.ScheduleBatch
(
Commands,
Results,
JobBatchSize,
hSetupJob
);
// schedule gather job
// specify dependency on raycast job
hGatherJob =
gatherJob.Schedule(NumCells, JobBatchSize, hRaycastJob);
// kick jobs
JobHandle.ScheduleBatchedJobs();
}
```

And here is what the profiler shows:

![](../../assets/d7970935d5417ccf.png)

The jobs run outside the span of the update function, freeing up the main thread and not stalling it.

## Time Slicing

Now, let’s see how we can further reduce the CPU time spent on the raycast job with time slicing. Here is the pattern I usually use for time slicing:

- Declare an index (or iterator) that to keep track of the current progress of time slicing.
- Initialize the index at the start of a new batch of work.
- Advance the index as additional portion of the work is done in each time slice.
- Execute final processing logic when the last portion of the work is done.
- Go back to step 2 to start a new batch of work.

Let’s modify our job structs so that they only process a portion of the exposure map in one frame. Here are the changes:

- Add a
`TimeSliceBaseIndex`

field (initialized to 0) to keep track of time slicing progress. - Add an index field to the job strcuts to mark the beginning of the range of exposure map cells to process in each frame.
- Change the
`WriteOnly`

attribute on the`ExposureMap`

field of the`RaycastGatherJob`

struct to`NativeDisableParallelForRestriction`

in order to remove Unity’s safeguard that limits the access to native arrays to only the index passed into the jobs’`Execute`

functions.

So the job structs become:

```
struct RaycastSetupJob : IJobParallelFor
{
public Vector3 EyePos;
[ReadOnly]
public NativeArray<Vector3> Grid;
[ReadOnly]
public NativeArray<RaycastCommand> Commands;
public int TimeSliceBaseIndex;
public void Execute(int localIndex)
{
int globalIndex = localIndex + TimeSliceBaseIndex;
Vector3 cellCenter = Grid[globalIndex];
Vector3 vec = cellCenter - EyePos;
Commands[localIndex] =
new RaycastCommand(EyePos, vec.normalized, vec.magnitude);
}
}
struct RaycastGatherJob : IJobParallelFor
{
[ReadOnly]
public NativeArray<RaycastHit> Results;
[NativeDisableParallelForRestriction]
public NativeArray<bool> ExposureMap;
public int TimeSliceBaseIndex;
public void Execute(int localIndex)
{
int globalIndex = localIndex + TimeSliceBaseIndex;
bool exposed = (Results[localIndex].distance <= 0.0f);
ExposureMap[globalIndex] = exposed;
}
}
```

And this is the new update function:

```
void UpdateExposureMap(int numRaysPerTimeSlice)
{
// wait for jobs from last frame to complete
hGatherJob.Complete();
// trim excess ray count for the last time slice of batch
int numExcessRays =
TimeSliceBaseIndex + numRaysPerTimeSlice - NumCells;
numRaysPerTimeSlice -= Mathf.Max(0, numExcessRays);
// batch ended?
if (TimeSliceBaseIndex < 0)
{
// double-buffering
SwapExposureBackBuffer();
// reset time slicing index
TimeSliceBaseIndex = 0;
}
// dispose of job data allocated from last frame
if (Commands.IsCreated)
Commands.Dispose();
if (Results.IsCreated)
Results.Dispose();
// allocate data shared across jobs
var allocator = Allocator.TempJob;
Commands =
new NativeArray<RaycastCommand>
(
numRaysPerTimeSlice,
allocator
);
Results =
new NativeArray<RaycastHit>
(
numRaysPerTimeSlice,
allocator
);
// create setup job
var setupJob = new RaycastSetupJob();
setupJob.EyePos = EyePos;
setupJob.Grid = Grid;
setupJob.Commands = Commands;
setupJob.TimeSliceBaseIndex = TimeSliceBaseIndex;
// create gather job
var gatherJob = new RaycastGatherJob();
gatherJob.Results = Results;
gatherJob.ExposureMap = ExposureMap;
gatherJob.TimeSliceBaseIndex = TimeSliceBaseIndex;
// schedule setup job
var hSetupJob =
setupJob.Schedule
(
numRaysPerTimeSlice,
JobBatchSize
);
// schedule raycast job
// specify dependency on setup job
var hRaycastJob =
RaycastCommand.ScheduleBatch
(
Commands,
Results,
JobBatchSize,
hSetupJob
);
// schedule gather job
// specify dependency on raycast job
hGatherJob =
gatherJob.Schedule
(
numRaysPerTimeSlice,
JobBatchSize,
hRaycastJob
);
// advance time slice index
TimeSliceBaseIndex += numRaysPerTimeSlice;
// end of batch?
if (TimeSliceBaseIndex >= NumCells)
{
// signal end of batch
TimeSliceBaseIndex = -1;
}
// kick jobs
JobHandle.ScheduleBatchedJobs();
}
```

If we set the number of rays per time slice to be 10% of the total rays per batch, it will take 10 frames to finish all raycasts for a batch and trigger a buffer swap. In the video below, you can see the front exposure map buffer being refreshed every time all raycasts are finished for a batch. A lower frame rate is used in this video to make the debug draw last longer per frame, so at full frame rate, the latency of updating the exposure map wouldn’t be as long.

If it can be guaranteed that there won’t be any race condition when the gathered raycast results are used to update the exposure map, it is possible to do away with double buffering and directly update a single exposure map buffer as raycast results come in. The end result is that the updated portion of the exposure map is reflected every frame and the overall system is more responsive.

As for performance, here are the stats for running 10k raycasts at different levels of time slicing (all with delayed gathering):

**No Time Slicing:**

CPU time on main thread: 0.073ms

Average raycast time on each busy CPU core: 0.156ms

Total raycast time on all CPU cores: 1.87ms

Exposure map update latency: 1 frame**50% Rays Per Time Slice:**

CPU time on main thread: 0.058ms

Average raycast time on each busy CPU core: 0.093ms

Total raycast time on all CPU cores: 1.11ms

Exposure map update latency: 2 frames**10% Rays Per Time Slice:**

CPU time on main thread: 0.044ms

Average raycast time on each busy CPU core: 0.018ms

Total raycast time on all CPU cores: 0.21ms

Exposure map update latency: 10 frames

The CPU time on the main thread reduces slightly as time slicing gets more aggressive. The CPU time on raycasts is roughly proportional to the number of rays per time slice.

## Conclusion

I have shown an example of how to use time slicing to split work across multiple frames. With time slicing, there is quite some freedom to adjust the balance between computation time budget and update latency.

If you’re familiar with [Unity’s coroutines](https://docs.unity3d.com/Manual/Coroutines.html), you might realize that it’s possible to implement a form of time slicing using coroutines and yielding after a portion of work is finished. That is technically correct, but be aware that Unity’s coroutines only run on the main thread and does not take advantage of worker threads, so they are actually stalling the main thread when running. It’s highly recommended to take advantage of all CPU cores and leave as little work to the main thread as possible.

If you enjoyed this tutorial and would like to see more, please consider supporting me on [Patreon](https://www.patreon.com/TheAllenChou). By doing so, you can also get updates on future tutorials. Thanks!