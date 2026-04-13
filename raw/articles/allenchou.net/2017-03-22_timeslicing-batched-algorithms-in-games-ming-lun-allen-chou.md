---
title: Timeslicing Batched Algorithms in Games | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2017/03/timeslicing-batched-algorithms-across-multiple-frames/
author: Allen Chou
published: '2017-03-22'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

The source files for generating the animations in this post are on [GitHub](https://github.com/TheAllenChou/timeslicing).

本文之中文翻譯[在此](https://wayne-c.github.io/2017/07/08/timeslicing-batched-algorithms-across-multiple-frames/) (by [Wayne Chen](https://wayne-c.github.io/))

Timeslicing is a very useful technique to improve the performance of batched algorithms (multiple instances of the same algorithm): instead of running all instances of algorithms in a single frame, spread them across multiple frames.

For instance, if you have 100 NPCs in a game level, you typically don’t need to have every one of them make a decision in every single frame; having 50 NPCs make decisions in each frame would effectively reduce the decision performance overhead by 50%, 25 NPCs by 75%, and 20 NPCs by 80%.

Note that I said timeslicing the decisions, __not__ the whole update logic of the NPCs. In every frame, we’d still want to animate every NPC, or at least the ones closer and more noticeable to the player, based on the **latest decision**. The extra animation layer can usually hide the slight latency in the timesliced decision layer.

Also bear in mind that I will not be discussing how to finish a single algorithm across multiple frames, which is another form of timeslicing that is not within the scope of this post. Rather, this post will focus on spreading multiple instances of the same algorithm across multiple frames, where each instance is small enough to fit in a single frame.

Such timeslicing technique applies to batched algorithms that are not hyper-sensitive to latency. If even a single frame of latency is critical to certain batched algorithms, it’s probably not a good idea to timeslice them.

In this post, I’d like to cover:

- An example that involves running multiple instances of a simple algorithm in batch.
- How to timeslice such batched algorithms.
- A categorization for timeslicing based on the timing of input and output.
- A sample implementation of a timeslicer utility class.
- Finally, how threads can be brought into the mix.


### The Example

The example I’m going to use is a simple logic that orients NPCs to face a target. Each NPC’s decision layer computes the desired orientation to face the target, and the animation layer tries to rotate the NPCs to match their desired orientation, capped at a maximum angular speed.

First, let’s see an animated illustration of what it might look like if this algorithm is run for every NPC in every frame (Update All).

The moving circle is the target, the black pointers represent NPCs and their orientation, and the red indicators represent the NPCs’ desired orientation.

![](../../assets/e325237b174c604b.gif)


And the code looks something like this:

void NpcManager::UpdateFrame(float dt) { for (Npc &npc : m_npcs) { npc.UpdateDesiredOrientation(target); npc.Animate(dt); } } void Npc::UpdateDesiredOrientation(const Object &target) { m_desiredOrientation = LookAt(target); } void Npc::Animate(float dt) { Rotation delta = Diff(m_desiredOrientation, m_currentOrientation); delta = Limit(delta, m_maxAngularSpeed); m_currentOrientation = Apply(m_currentOrientation, delta); }

As mentioned above, you typically don’t need to update all the NPCs’ decisions in one frame. We can achieve rudimentary timeslicing like this:

void NpcManager::UpdateFrame(float dt) { const unsigned kMaxUpdates = 4; unsigned npcUpdate = 0; while (npcUpdated < m_numNpcs && npcUpdated < kMaxUpdates) { m_aNpc[m_iNpcWalker].UpdateDesiredOrientation(target); m_iNpcWalker = (m_iNpcWalker + 1) % m_numNpc; ++npcUpdated; } for (Npc &npc : m_npcs) { npc.Animate(dt); } }

This straightforward approach could be enough. However, sometimes you just need more control over the timing of input and output. Using the more involved timeslicing logic presented below, you can have a choice of different timing of input and output to suit specific needs.

Before going any further, let’s take a look at the terminology that will be used throughout this post.

### Terminology

- Completing a
**batch**means finishing running the decision logic once for each NPC. - A
**job**represents the work to run an instance of decision logic for an NPC. - The
**input**is the data required to run a job. - The
**output**is the results from a job after it’s finished

Now the timeslicing logic.

### Timeslicing

Here are the steps of one way to timeslice batched algorithms. It’s probably not the absolute best in terms of efficiency or memory usage, but I find it logically clear and easy to maintain (which also means it’s good for presentational purposes). So unless you absolutely need to micro-optimize, I wouldn’t worry about it too much.

- Start a new batch.
- Figure out all the jobs that need to be done. Associate each job with a unique
**key**that can be used to infer the required input for the job. - For each job, prepare an instance of job
**parameters**that is a collection of its key, input, and output. - Start and finish up to a max number of jobs per frame.
- Depending on the timing of output (more on this later),
**save**the**results**of a job, including the job’s output and its associated key, by pushing it to athat represents the**ring buffer****history**of job results. The rest of the game logic to query latest results by key. - After all jobs are finished, the batch is finished. Rinse and repeat.

One advantage of looking up output by key is that different timesliced systems can work with each other just fine, even if they reference each other’s output. As far as a system is concerned, it’s looking up output from another system using a key, and the other system is reporting back the latest valid output available associated with the given key. Sort of like a mini database.

In our example, since each job is associated with an NPC, it seems fitting to use the NPCs as individual keys.

Next, here’s a categorization of timeslicing, based on the timing of reading input and saving output.

NOTE: The use of words “synchronous” and “asynchronous” here has nothing to do with multi-threading. The words are only used to distinguish the timing of operations. Everything presented before the “Threads” section later in this post is single-threaded.

**Asynchronous Input**: input is read by a job only when it’s started.**Synchronous Input**: input is read by all jobs when a new batch starts.**Asynchronous Output**: a job’s output is saved as soon as the job finishes.**Synchronous Output**: output of all jobs is saved when a batch finishes.

A ring buffer is used so that the rest of the game logic can be completely agnostic to the timing, and assume that the output (queried by key) is the latest.

Mixing and matching different timing of input and output gives 4 combinations. Async input / async output (AIAO), sync input / sync output (SISO), sync input / async output (SIAO), and async input / sync output (AISO). Let’s look at them one by one.

For demonstrational purposes, all animated illustrations below reflect a setup where only one job is started in each frame. The number should be set higher in a real game if it is introducing unacceptable latency.

### Async Input / Async Output

For our specific example of NPCs turning to face the target, the AIAO combination probably makes the most sense. The input is read only when the job starts, so the job has the latest position of the target. The output is saved as soon as the job finishes with results of NPC’s desired orientation, so the NPC’s animation layer can react to the latest desired orientation immediately.

Here’s an animated illustration of what it could look like if we run the jobs at 10Hz (10 NPC jobs per second).

![](../../assets/9a02fcc95a39c1a1.gif)


And here’s what it looks like if done at 30Hz.

![](../../assets/36f77db056a04512.gif)


You can see each that NPC waits until its job starts before getting the latest position of the target, and updates its desired orientation as soon as the job finishes.

### Sync Input / Asyn Output

For cases where asynchronous input from the AIAO combination as shown above is causing unwanted staggering, yet NPCs are still desired to react as soon as each of their job finishes, we can use the SIAO combination.

Here’s the 10Hz version.

![](../../assets/748813eaa02ad87e.gif)


And here’s the 30Hz version.

![](../../assets/f27a2d459c67b9aa.gif)


Note that when each job starts, it’s using the same target position as input, which has been synchronized at the start of each batch, while the output is saved for immediate NPC reaction as soon as each job finishes.

This is effectively the same as the first “basic first attempt” at timeslicing shown above.

### Sync Input / Sync Output

The SISO combination is probably best explained by looking at the animated illustrations first. In order, below are the 10Hz and 30Hz versions of this combination.

![](../../assets/92876083dfb3d788.gif)


![](../../assets/dacd94f429562e0b.gif)


It’s basically a “laggy” version of the very first animated illustration where every NPC is fully updated in every frame. All job input is synchronized upon batch start, and all output is saved out upon batch finish. Essentially this is kind of a “double buffer”, where the latest results aren’t reflected until all jobs in a batch are finished. For this reason, the history ring buffer must be **at least twice as large** as the max batch size for combinations with **synchronized output** to work properly.

The SISO combination is probably not ideal for our specific example. However, for cases like updating influence maps, heat maps, or any kind of game space analysis, the SISO combination could prove useful.

### Async Input / Sync Output

To be frank, I can’t think of a proper scenario to justify the use of the AISO combination. It’s only included here for comprehensive purposes. See the animated illustrations below in the order of the 10Hz version and 30Hz version. If you can think of a case where the AISO combination is a superior choice to the other three, please share your ideas in the comments or email me. I’d really like to know.

![](../../assets/0ba06f4a48dd0f5b.gif)


![](../../assets/a9b997f104232e62.gif)


### Sample Implementation

Now that we’ve seen all four combinations of timeslicing, it’s time to look at a sample implementation that does exactly what has been shown above.

Before going straight to the core timeslicing logic, let’s first look at how it plugs into the sample NPC code we saw earlier.

The timeslicer utility class allows users to provide a function that sets up keys for a new batch (writes to an array and returns new batch size), a function to set up input for job (writes to input based on key), and a function that is the logic to be timesliced (writes to output based on key and input).

class NpcManager { private: struct NpcJobInput { Point m_targetPos; }; struct NpcJobOutput { Orientation m_desiredOrientation; }; // timeslicing utility class Timeslicer < Npc*, // key NpcJobInput, // input NpcJobOutput, // output kMaxNpcs, // max batch size false, // sync input flag (false = async) false // sync output flag (false = async) > m_npcTimeslicer; // ...other stuff }; void NpcManager::Init() { // set up keys for new batch auto newBatchFunc = [this](Npc **aKey) unsigned { for (unsigned i = 0; i < m_numNpcs; ++i) { aKey[i] = GetNpc(i); } return m_numNpcs; }; // set up input for job auto setUpInputFunc = [this](Npc *pNpc, Input *pInput)->void { pInput->m_targetPos = GetTargetPosition(pNpc); } // logic to be timesliced auto jobFunc = [this](Npc *pNpc, const Input &input, Output *pOutput)->void { pOutput->m_desiredOrientation = LookAt(pNpc, input.m_targetPosition); }; // initialize timeslicer m_npcTimeslicer.Init ( newBatchFunc, setUpInputFunc, jobFunc ); } void NpcManager::UpdateFrame(float dt) { // timeslice decision logic m_timeslicer.Update(maxJobsPerFrame); // animate all NPCs based on latest decision results for (Npc &npc : m_npcs) { Output output; if (!m_timeSlicer.GetOutput(&npc, &output)) { npc.SetDesiredOrientation(output.m_desiredOrientation); } npc.Animate(dt); } }

And below is the timeslicer utility class in its entirety.

template < typename Input, typename Output, typename Key, unsigned kMaxBatchSize, bool kSyncInput, bool kSyncOutput > class Timeslicer { private: struct JobParams { Key m_key; Input m_input; Output m_output; }; struct JobResults { Key m_key; Output m_output; }; // number of jobs in current batch unsigned m_batchSize; // keep track of jobs in current frame unsigned m_iJobBegin; unsigned m_iJobEnd; // required to start jobs JobParams m_aJobParams[kMaxBatchSize]; // keep track of job results (statically allocated) static const unsigned kMaxHistorySize = kSyncOutput ? 2 * kMaxBatchSize // more on this later : kMaxBatchSize; typedef RingBuffer<JobResults, kMaxHistorySize> History; History m_history; // set up keys for new batch // (number of keys = batch size = jobs per batch) typedef std::function<unsigned (Key *)> NewBatchFunc; NewBatchFunc m_newBatchFunc; // set up input for job typedef std::function<void (Key, Input *)> SetUpInputFunc; SetUpInputFunc m_setUpInputFunc; // logic to be timesliced // (takes key and input, writes output) typedef std::function<void (Key, const Input &, Output *)> JobFunc; JobFunc m_jobFunc; public: void Init ( NewBatchFunc newBatchFunc, SetUpInputFunc setUpInputFunc, JobFunc jobFunc ) { m_newBatchFunc = newBatchFunc; m_setUpInputFunc = setUpInputFunc; m_jobFunc = jobFunc; Reset(); } void Reset() { m_batchSize = 0; m_iJobBegin = 0; m_iJobEnd = 0; } bool GetOutput(Key key, Output *pOutput) const { // iterate from newest history (last queued output) for (const JobResults &results : m_history.Reverse()) { if (key == results.m_key) { *pOutput = results.m_output; return true; } } return false; } void Update(unsigned maxJobsPerUpdate) { TryStartNewBatch(); StartJobs(maxJobsPerUpdate); FinishJobs(); } private: void TryStartNewBatch() { if (m_iJobBegin == m_batchSize) { // synchronous output saved on batch finish if (kSyncOutput) { for (unsigned i = 0; i < m_batchSize; ++i) { const JobParams ¶ms = m_aJobParams[i]; SaveResults(params); } } Reset(); Key aKey[kMaxBatchSize]; m_batchSize = m_newBatchFunc(aKey); for (unsigned i = 0; i < m_batchSize; ++i) { JobParams ¶ms = m_aJobParams[i]; params.m_key = aKey[i]; // synchronous input set up on new batch start if (kSyncInput) { m_setUpInputFunc(params.m_key, ¶ms.m_input); } } } } void StartJobs(unsigned maxJobsPerUpdate) { unsigned numJobsStarted = 0; while (m_iJobEnd < m_batchSize && numJobsStarted < maxJobsPerUpdate) { JobParams ¶ms = m_aJobParams[m_iJobEnd]; // asynchronous input set up on job start if (!kSyncInput) { m_setUpInputFunc(params.m_key, ¶ms.m_input); } m_jobFunc ( params.m_key, params.m_input, ¶ms.m_output ); ++m_iJobEnd; ++numJobsStarted; } } void FinishJobs() { while (m_iJobBegin < m_iJobEnd) { const JobParams ¶ms = m_aJobParams[m_iJobBegin++]; // asynchronous output saved on job finish if (!kSyncOutput) { SaveResults(params); } } } void SaveResults(const JobParams ¶ms) { JobResults results; results.m_key = params.m_key; results.m_output = params.m_output; if (m_history.IsFull()) { m_history.Dequeue(); } m_history.Enqueue(results); } };

### Threads

If your game engine allows multi-threading, we can go one step further by offloading jobs to threads. Starting a job now creates a thread that runs the timesliced logic, and finishing a job now waits for the thread to finish. We need to use [ read/write locks](https://en.wikipedia.org/wiki/Readers%E2%80%93writer_lock) to make sure the timeslicer plays nicely with the rest of game logic. Required changes to code are highlighted below.

class Timeslicer { // ...unchanged code omitted RwLock m_lock; struct JobParams { std::thread m_thread; Key m_key; Input m_input; Output m_output; }; bool GetOutput(Key key, Output *pOutput) const { ReadAutoLock readLock(m_lock); // iterate from newest history (last queued output) for (const JobResults &results : m_history.Reverse()) { if (key == results.m_key) { *pOutput = results.m_output; return true; } } return false; } void TryStartNewBatch() { WriteAutoLock writeLock(m_lock); if (m_iJobBegin == m_batchSize) { // synchronous output saved on batch finish if (kSyncOutput) { for (unsigned i = 0; i < m_batchSize; ++i) { const JobParams ¶ms = m_aJobParams[i]; SaveResults(params); } } Reset(); Key aKey[kMaxBatchSize]; m_batchSize = m_newBatchFunc(aKey); for (unsigned i = 0; i < m_batchSize; ++i) { JobParams ¶ms = m_aJobParams[i]; params.m_key = aKey[i]; // synchronous input set up on new batch start if (kSyncInput) { m_setUpInputFunc(params.m_key, ¶ms.m_input); } } } } void StartJobs(unsigned maxJobsPerUpdate) { WriteAutoLock writeLock(m_lock); unsigned numJobsStarted = 0; while (m_iJobEnd < m_batchSize && numJobsStarted < maxJobsPerUpdate) { JobParams ¶ms = m_aJobParams[m_iJobEnd]; // asynchronous input set up on job start if (!kSyncInput) { m_setUpInputFunc(params.m_key, ¶ms.m_input); } params.m_thread = std::thread([¶ms]()->void { m_jobFunc ( params.m_key, params.m_input, ¶ms.m_output ); }); ++m_iJobEnd; ++numJobsStarted; } } void FinishJobs() { WriteAutoLock writeLock(m_lock); while (m_iJobBegin < m_iJobEnd) { JobParams ¶ms = m_aJobParams[m_iJobBegin++]; params.m_thread.join(); // asynchronous output saved on job finish if (!kSyncOutput) { SaveResults(params); } } } };

If your game can afford to have one more frame of latency and you don’t want the timeslicer squatting a thread, you can tweak the update function a bit, where jobs are started at the end of update in the current frame, and are finished at the beginning of update in the next frame.

void TimeSlicer::Update(unsigned maxJobsPerUpdate) { FinishJobs(); TryStartNewBatch(); StartJobs(maxJobsPerUpdate); }

### Summary

That’s it! We’ve seen how timeslicing batched algorithms can help with game performance, as well as the 4 combinations of input and output with different timing, each having its own use (well, maybe not the last one). We’ve also seen how the timeslicing logic can be further adapted to make use of threads.

I hope you find this useful. 🙂