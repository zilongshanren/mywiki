---
title: Asynchronous Job Scheduler
url: https://outerra.blogspot.com/2010/09/asynchronous-job-scheduler.html
author: Outerra
published: '2010-09-26'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One of the essential components is an asynchronous job scheduler, named simply

*jobmaster*in the engine. Its task is to execute jobs that have to be carried out asynchronously because they contain code that usually blocks while waiting for disk I/O or network operations to complete. This code has to run decoupled from the main application and the renderer threads as it would introduce stuttering.

However, programming asynchronous routines is not that straightforward as it is with the synchronous ones. Previously we used special job processors that used a fixed number of threads to process jobs, that explicitly handled their state and issued respins to allow running other jobs while waiting for their asynchronous operations to complete.

This was cumbersome to use and consequently we often coded some things as synchronous routines, pushing it to a queue of things to be done "later". As you can guess, many things queued there and we had to think how to make this simpler and more enjoyable.

Jobmaster came as a solution to this, because it allowed us to write a simple synchronous code to handle things like texture and terrain data loading and downloading terrain data over bittorrent, while still effectively handling multiple jobs in parallel. Another important property is that one can set the number of threads that will run concurrently, adjustable to the number of processor cores available on the system and thus not fighting for the resources unnecessarily.

Jobmaster keeps a pool of threads that it uses to handle jobs. A thread can be in one of three states - either sleeping when no job is assigned to it, running a job code, or sleeping while waiting for a blocking operation to complete. At any time only the designated maximum number of threads can be running. Other jobs will have to wait until the active jobs terminate or hit a block. In that case the thread looks if there is another job that can continue because its blocking operation completed already, or if there's a free thread that can run another queued job. In any case, the current thread suspends itself afterward, keeping the context of the job's routine.

A blocker can be also an explicit wait operation for completion of other jobs, usually of the children ones that were spawned from the job previously. Consequently it has to prioritize jobs that are likely to progress because all jobs they are waiting for were completed already.

The jobmaster is programmed using lock-free queues and pools to maintain its state.

So far the testing shows this system is much more convenient to use than the previous one, what is probably also its major advantage.

***

Another component worth mentioning is the logger/grapher used to identify performance problems and timing issues in jobs and the main threads. The graphs can be fed from custom timers used to measure time durations or amount of resources. They are resizing dynamically to cover the actual range of values.

Graphs are used to point to the problematic component during a particular activity and as such are mainly complementing the log system, so there are means of identifying the frame numbers that showed some erroneous behavior, that are then used to locate more detailed information in the logs.

## 3 comments:

The joys of thread pooling. I'm writing some EventMachine-managed code right now, but for a decidedly less exciting project :-(


Also, cool graphs! Do you use some kind of windowing system for the interface? I notice some of the windows have close buttons.

The windowing system is just a simple one for printing text and drawing the graphs. Otherwise we are using the embedded browser and html for most of the UI.

Nice windows. :)

Post a Comment