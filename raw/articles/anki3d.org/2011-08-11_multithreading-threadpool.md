---
title: 'Multithreading: Threadpool'
url: https://anki3d.org/multithreading-threadpool/
author: Panagiotis Christopoulos Charitos
published: '2011-08-11'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

Multithreading is a concept that exist for many decades in computer science, nevertheless, only in recent years it become a trend in game development with the arrival of multi-core CPUs in our home PCs. In this small article we will discuss how AnKi utilizes the power of multiple processors. Also the source code of an example can be found at the end of the article.

The concept of multiple threads offers many advantages in applications that execute many uniform jobs at the same time, for example a webserver needs to serve multiple hosts at the same time and without a host waiting for a previous request to finish. A game application though used to have a very standard and linear flow. For example, we first update the AI, then the physics, then we update the world, we do visibility determination and lastly we render, then we repeat the same again. Sometimes its difficult to execute some of these distinctive steps in parallel because the data of the previous step will be used by the next. I bet high class development studios have found ways to blend these steps but in AnKi we use a more simple approach. We use multiple threads to run uniform jobs in parallel.

One good example to illustrate how AnKi uses the power of multiple threads is the visibility determination algorithm. One step of visibility determination is the test for every renderable scene node against the camera’s view frustum. If we have N nodes to test and M threads we can roughly assign for testing the first N/M nodes to the first thread, the next N/M nodes to the next thread etc.


AnKi features a job manager that executes N jobs in parallel in N different threads. One thing to note is that the threads are being created only once (upon the manager’s initialization) and not for every parallel run. This gives an obvious performance advantage (over OpenMP for example) because creating and destroying threads is time consuming and not efficient at all. The job manager works from the main thread like this:

Assign job to first thread Assign job to second thread ... Assign job to N thread Wait for all threads to finish

The implementation of the job manager is pretty simple. Underneath it utilizes the boost threading library (as always) and it uses:

- N condition variables
- N mutexes
- N threads
- One barrier

If you are not familiar with these concepts please refer to a good textbook about parallel programming.

The condition variables are being used for thread waiting. When the thread is not assigned to do a job it waits using a condition variable. Every condition variable comes with a mutex and that’s the reason we need N mutexes. The reason of using N threads is pretty obvious but the usage of the barrier is not. The barrier is being used for thread synchronization. What we synchronize is the N threads along with the main thread.

According to the boost documentation:

When a barrier is created, it is initialized with a thread count N. The first N-1 calls to wait() will all cause their threads to be blocked. The Nth call to wait() will allow all of the waiting threads, including the Nth thread, to be placed in a ready state. The Nth call will also “reset” the barrier such that, if an additional N+1th call is made to wait(), it will be as though this were the first call to wait(); in other words, the N+1th to 2N-1th calls to wait() will cause their threads to be blocked, and the 2Nth call to wait() will allow all of the waiting threads, including the 2Nth thread, to be placed in a ready state and reset the barrier. This functionality allows the same set of N threads to re-use a barrier object to synchronize their execution at multiple points during their execution.


We actually initialize the barrier with N+1, the number of the N threads plus the main thread.

When we say that we assign a job to the job manager what we actually mean is that we pass to the thread a pointer to a function to execute along with a set of arguments. So lets see how we use the job manager in AnKi’s view frustum test:

VisJobParameters jobParameters; jobParameters.cam = &cam; jobParameters.skipShadowless = skipShadowless; jobParameters.visibilityInfo = &storage; jobParameters.scene = &scene; jobParameters.msRenderableNodesMtx = &msRenderableNodesMtx; jobParameters.bsRenderableNodesMtx = &bsRenderableNodesMtx; for(uint i = 0; i < parallel::ManagerSingleton::getInstance().getThreadsNum(); i++) { parallel::ManagerSingleton::getInstance().assignNewJob(i, getRenderableNodesJobCallback, jobParameters); } parallel::ManagerSingleton::getInstance().waitForAllJobsToFinish();

The code for waitForAllJobsToFinish() is the simple:

barrier->wait();

# Getting the source

You can download the job manager and an example bellow. The build instructions and usage are inside the readme file.