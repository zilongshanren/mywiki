---
title: 'Game Programming: Delayed Result Gathering | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2021/05/delayed-result-gathering/
author: Allen Chou
published: '2021-05-18'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Source files and future updates are available on [Patreon](https://www.patreon.com/TheAllenChou).

You can follow me on [Twitter](https://twitter.com/TheAllenChou).

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

本文之中文翻譯[在此](http://allenchou.net/2021/05/delayed-result-gathering-chinese/)

## Introduction

Back at [DigiPen](http://digipen.edu/) (my college where I learned gamedev), whenever people from the games industry came over on a company day to share their industry experience, one question always came up during Q&A: please tell us one thing you wish you had known at school (it can be anything: technical skills, social skills, production skills, etc.). I often wondered what I would tell the students if I had been at the podium. For a very long time, I had no answers in mind. But now, if I were to present on a company day, I would probably have an answer specifically for CS students. I wish I had known two particular optimization techniques when I was working on my game projects back at school: **delayed result gathering** and **time slicing**.

These are the first two techniques I learned since I [joined Naughty Dog](http://allenchou.net/2016/03/my-uncharted-journey/). And I have found them the most useful throughout my career. I have used them in numerous in-game systems up to this day. They are simple general solutions that can be applied almost everywhere and are usually very effective.

In this tutorial, I will talk about the first of the two: delayed result gathering. I will cover time slicing in the next tutorial.

## The Example: Exposure Map & Exposure Avoidance

First, I’ll introduce the example that serves as the testbed for the two optimization techniques. It will be modified throughout these two tutorials to demonstrate how to apply the optimization techniques to an existing system.

The example is exposure map & exposure avoidance. We have a grid that represents whether each cell is exposed to a “sentinel,” and we have a character that tries to move to and hide in a nearby cell that is not exposed. As the sentinel moves around, the character runs away once their current cell becomes exposed. Meet shy ball.

Here are the steps within the update loop for this mechanic:

- Update the exposure map based on the sentinel’s current position.

Cast a ray from the sentinel to each cell. If the ray is clear, the cell is exposed. - Compute the path lengths from the character to each grid cell.
- If the character’s current cell is exposed, update their destination to a nearby cell that is not exposed, and navigate the character to the destination.

And this is what the update loop looks like in code:

```
void Update()
{
UpdateExposureMap();
UpdatePathLengths();
UpdateDestination();
}
```

If I were still in college, my implementation of `UpdateExposureMap`

probably would have looked like this:

```
void UpdateExposureMap()
{
for (int iCell = 0; iCell < NumCells; ++iCell)
{
Vector3 cellCenter = Grid[iCell];
Vector3 vec = cellCenter - EyePos;
Vector3 rayDir = vec.normalized;
float rayLen = vec.magnitude;
bool exposed = !Physics.Raycast(EyePos, rayDir, rayLen);
ExposureMap[iCell] = exposed;
}
}
```

During the entirely of this tutorial and the next one, I will solely focus on optimizing step 1, i.e. `UpdateExposureMap`

, so the implementation details of steps 2 & 3, `UpdatePathLengths`

and `UpdateDesination`

, are omitted. Note that the optimization techniques are not about optimizing specific algorithms (the raycasts themselves in this case) at a lower level, but optimization how they are called at a higher level. Also, depending on the use case, raycasts might not be the best way to update exposure maps and are used here solely for demonstration purposes.

For the implementation above, this is what the profiler shows for 10k raycasts per frame:

![](../../assets/e7c651153b1d9625.png)

When zoomed in further, we can see that the wide orange rectangle is actually tons of tiny raycast sections, one for each raycast.

![](../../assets/1e48b14742506859.png)

An immediate problem arises: raycasts in large quantities are not exactly cheap. Making these function calls and waiting for them to return sequentially stalls the main thread pretty badly. Optimization is in order.

## Multi-Threading

A series of blocking raycast function calls on the main thread is pretty bad. Raycasts belong to the family of embarrassingly parallelizable operations. Each raycast does the same thing: it queries the spatial data and finds where the ray hits collision, and this operation can be self-contained on a separate thread. Instead of filling up the main thread with sequential raycast function calls, the first thing to try is offloading the work to other CPU cores, i.e. taking advantage of multi-threading. If we have 10 worker cores, then as a first pass, we can try splitting the raycast work into 10 threads.

If you’re using Unity, there is luckily an official system to make it easier to take advantage of multi-threading: Unity’s job system. There is even an official job class specifically for multi-threaded raycasts! You set up the raycasts, tell the job how many raycasts to run on each thread, kick the job, and you’re done! The raycasts will be executed on multiple CPU cores, and all that’s left to do is wait for the job to finish and gather the results.

We define two job structs: `RaycastSetupJob`

and `RaycastGatherJob`

. The setup job sets up the raycast commands before the raycast job that does the actual raycast work (kicked by calling Unity’s `RaycastCommand.ScheduleBatch`

). The gather job gathers raycast results and use them to update the exposure map. Here’s the dependency chain: The raycast job depends on the setup job, and the gahter job depends on the raycast job.

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

And the `UpdateExposureMap`

function becomes:

```
void UpdateExposureMap()
{
// allocate data shared across jobs
var allocator = Allocator.TempJob;
var commands =
new NativeArray<RaycastCommand>(NumCells, allocator);
var results =
new NativeArray<RaycastHit>(NumCells, allocator);
// create setup job
var setupJob = new RaycastSetupJob();
setupJob.EyePos = EyePos;
setupJob.Grid = Grid;
setupJob.Commands = commands;
// create gather job
var gatherJob = new RaycastGatherJob();
gatherJob.Results = results;
gatherJob.ExposureMap = ExposureMap;
// schedule setup job
var hSetupJob = setupJob.Schedule(NumCells, JobBatchSize);
// schedule raycast job
// specify dependency on setup job
var hRaycastJob =
RaycastCommand.ScheduleBatch
(
commands,
results,
JobBatchSize,
hSetupJob
);
// schedule gather job
// specify dependency on raycast job
var hGatherJob =
gatherJob.Schedule(NumCells, JobBatchSize, hRaycastJob);
// kick jobs
JobHandle.ScheduleBatchedJobs();
// wait for completion
hGatherJob.Complete();
// dispose of job data
commands.Dispose();
results.Dispose();
}
```

Now this is what the profiler shows:

![](../../assets/23e45de5b6916c07.png)

The CPU time taken up by the raycast step on the main thread is reduced. However, the main thread is still stalled while waiting for the multi-threaded raycast job on the worker threads to complete. Can we further improve this?

## Delayed Result Gathering

Within the first few days I started working at Naughty Dog, I immediately found myself needing to touch a system that involved raycasts. One of the more senior programmers walked me through the process, and gave an offhand tip: “Oh, by the way, you don’t want to cast the rays and just have the thread wait there. You’ll want to cast the rays this frame, and delay the gathering of the results until the next frame.” That lit up a huge lightbulb in my head. Of course! If the system can afford a one-frame latency, then why not kick the job and gather the results the next frame? This way, after kicking the job, the CPU core can be immediately freed up to work on something else.

Note that if the results are needed within the same frame, it is still worth attempting to kick the job early, perform some other work, and gather the results later in the same frame. The point is to avoid stalling the main thread while waiting for job completion.

In next iteration of our example, I’m going to make the main thread kick the raycast job in one frame, and delay the gathering of the raycast results until the next frame. There is now effectively nothing left to take up CPU time on the main thread except for the gathering of raycast results from the previous frame and kicking the job that sets up the raycast job for the next frame.

The gather job is now waited for completion at the start of the `UpdateExposureMap`

function. The exposure map is now double-buffered, so the jobs can work on a back buffer, while the rest of the code can access the front buffer to avoid race conditions. Also, the gather job handle and shared data across jobs are now promoted from local variables to fields, because their lifetime needs to span two frames.

```
void UpdateExposureMap()
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

And this is what the profiler shows now:

![](../../assets/c8504d63677321b9.png)

The raycast job is running on the worker threads outside of the span of `UpdateExposureMap`

. The results are not needed until the call to `UpdateExposureMap`

in the next frame. No more stalling the main thread!

## Conclusion

I have shown the evolution of the raycast example in three iterations:

- Raycast functions are called sequentially and gravely stalls the main thread.
- Raycasts are offloaded to other worker threads but are still waited for on the main thread. This still stalls the main thread to some extent.
- The main thread is used only for the delayed gathering of raycast results from the job kicked in the previous frame, as well as kicking the job that sets up the raycast job for the next frame.

Here are some numbers I gathered from profiling the 3 iterations of the example. My CPU is an Intel i7-8700K. The timing was measured for 10k raycasts per frame.

**Iteration 1 (single-threaded)**

CPU time on main thread: 4.09ms

Average raycast time on each busy CPU core: 1.24ms

Total raycast time on all CPU cores: 1.24ms**Iteration 2 (multi-threaded jobs, same-function result gathering)**

CPU time on main thread: 0.47ms

Average raycast time on each busy CPU core: 0.16ms

Total raycast time on all CPU cores: 1.96ms**Iteration 3 (multi-threaded jobs, delayed result gathering)**

CPU time on main thread: 0.073ms

Average raycast time on each busy CPU core: 0.16ms

Total raycast time on all CPU cores: 1.87ms

Even though the total raycast time on all CPU cores is the lowest for iteration 1, the overhead of individual raycast function calls results in a total of 4.09ms spent on the main thread. Plus, iteration 1 puts all the work through a single CPU core, leaving the other cores idle. For iterations 2 & 3, the total raycast time of approximately 1.87-1.96ms on all CPU cores is higher than the 1.24ms from iteration 1, likely due to overhead introduced by the job system. But that is okay. The most important metric is the average time on each busy CPU core.

The average and total CPU time for iterations 2 & 3 are almost identical as expected, as their only difference is the timing of result gathering. Iteration 2 already reduces the CPU time spent on the main thread from 4.09ms to 0.47ms. In iteration 3, the time is further lowered to 0.073ms. This is a big improvement from iteration 1 (4.09ms -> 0.073ms). CPU cores are better utilized, and the time spent on each busy core for raycasts is much lower than iteration 1 (1.24ms -> 0.16ms).

I have covered **delayed result gathering**. In the next tutorial, I will go over the other very useful optimization technique: **time slicing**, which can further optimize the last iteration of our example. Stay tuned!

If you enjoyed this tutorial and would like to see more, please consider supporting me on [Patreon](https://www.patreon.com/TheAllenChou). By doing so, you can also get updates on future tutorials. Thanks!

This is amazing, thanks so much. I’ve never heard of “Exposure Map & Exposure Avoidance” so this is blowing my mind.

one thing I’m not sure about, how would you scale that to work with a larger map? I presume it’s not going to be enough to check all “cells” in the map for distance to the player…

my best guess would be querying the map with a rectangle around the red cube ,in a similar fashion to querying a quad tree? (as in return all cells inside this rect)

thanks again 🙂

You don’t have to update the entire exposure map all the time. And depending on the use case, there are better ways to implement and update exposure maps. The focus of this tutorial is not on exposure maps through; it’s about optimization techniques.