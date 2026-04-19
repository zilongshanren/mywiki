---
title: Task Management -- A Practical Example
url: https://bitsquid.blogspot.com/2010/03/task-management-practical-example.html
author: Niklas
published: '2010-03-25'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

The previous iteration of our task scheduler was based on Vista ThreadPools and mainly supported data parallelism. (Though we still had a degree of task parallelism from running two main threads -- an update thread and a render thread -- which both posted batches of jobs to the task manager.)

For the rewrite, I had a number of goals:

- Move away from Vista Thread Pools. We want complete control over our job threads.
- Minimize context switching. This is a guessing game on Windows, since the OS will do what the OS will do, but minimizing oversubscription of threads should help.
- Make a system that can run completely task based. I. e., everything in the system is run as a task and there are no explicit
*wait()*calls. Instead the entire code flow is controlled by task dependencies. Such a design allows us to exploit all possibilities for parallelism in the code which leads to maximum core utilization. - Still be "backwards compatible" with a system that uses one or more "main threads" that
*wait()*for data parallel jobs to complete, so that we can move incrementally to a more and more task based code flow. - Support tasks that run on external processors, such as SPUs or GPUs.
- Support hierarchical decomposition of tasks.

By hierarchical decomposition I mean that it should be possible to analyze the system in terms of tasks and subtasks. So that, at a higher level, we can regard the animation system as a single task that runs in parallel to other system tasks:

But then we can zoom in on the animation task and see that in fact is composed of a number of subtasks which in turn parallelize:



Hierarchical decomposition makes it possible to analyze systems and subsystems at different levels of abstraction rather than having to keep the entire task dependency graph in our heads. This is good because my head just isn't big enough.


A task in the new implementation is a simple data structure:

Here




I do not explicitly track completed task. Instead I keep a list of all open (i.e. not completed) tasks. Any task that is not in the open list is considered completed. Note that the open list is separate from the queue of work items that need to be performed. Items are removed from the queue when they are scheduled to a worker thread and removed from the open list when they have completed.


The


Having a single dependency is not a limitation, because if we want to depend on more than one task we can just introduce an anonymous task with no work item that has all the tasks we want to depend on as children. That task will complete when all its children has completed, so depending on that task gives us the wanted dependencies.


The


The



The total number of threads managed by the task manager thus equals the number of cores in the system, so we have no over- or undersubscription.


The worker threads are in a constant loop where they check the task manager for work items to perform. If a work item is available, they perform it and then notify the task manager of its completion. If no work items are available, they sleep and are woken by the task manager when new work items become available.


The main threads run their normal serial code path. As part of that code path, they can create tasks and subtasks that get queued with the task manager. They can also


The main threads can also process tasks while waiting for other events by calling a special function in the task manager


This means that all task manager threads are either running their serial code paths or processing jobs -- as long as there are jobs to perform and they don't get preempted by the OS. This means that as long as we have lots of jobs and few sync points we will achieve 100 % core utilization.


This approach also allows us to freely mix serial code with a completely task based approach. We can start out with a serial main loop (with data parallelization in the



void World::update()

{

_animation->update()

_scene_graph->update();

_gui->update();

render();

_sound->update();

}



And gradually convert it to fully braided parallelism (this code corresponds to the task graph shown above):



void World::update()

{

TaskId animation = _tasks->add( animation_task(_animation) );

TaskId scene_graph = _tasks->add( scene_graph_task(_scene_graph) );

_tasks->depends_on(scene_graph, animation);

TaskId gui = _tasks->add( gui_task(_gui) );


TaskId gui_scene = _tasks->add_empty();

_tasks->add_child(gui_scene, scene_graph);

_tasks->add_child(gui_scene, gui);


TaskId render = _tasks->add( render_task(this) );

_tasks->depends_on(render, gui_scene);


TaskId sound = _tasks->add( sound_update_task(_sound) );


TaskId done = _tasks->add_empty();

_tasks->add_child(done, render);

_tasks->add_child(done, sound);


_tasks->wait(done);

}



Note that tasks, subtasks and dependencies are created dynamically as part of the execution of serial code or other tasks. I believe this "immediate mode" approach is more flexible and easier to work with than some sort of "retained" or "static" task graph building.


A screenshot from our profiler shows this in action for a scene with 1000 animated characters with state machines:


Notice how the main and render threads help with processing tasks while they are waiting for tasks to be completed.


Once we have a task graph we want to make sure that our scheduler runs it as fast possible. Theoretically, we would do this by finding the critical path of the graph and making sure that tasks along the critical path are prioritized over other tasks. It's the classical


In a game, the critical path can vary a lot over different scenes. Some scenes are render bound, others are CPU bound. Of the CPU bound scenes, some may be bounded by script, others by animation, etc.


To achieve maximum performance in all situations we would have to dynamically determine the critical path and prioritize the tasks accordingly. This is certainly feasible, but I am a bit vary of dynamically reconfiguring the priorities in this way, because it makes the engine harder to profile, debug and reason about. Instead I have chosen a simpler solution for now. Each job is given a priority and the highest priority jobs are performed first. The priorities are not fixed by the engine but configured per-game to match its typical performance loads.


This seems like a resonable first approach. When we have more actual game performance data it would be interesting to compare this with the performance of a completely dynamic scheduler.


In the current implementation, all tasks are posted to and fetched from a global task queue. There are no per thread task queues and thus no task stealing. At our current level of task granularity (heavy jobs are split into a maximum of


OS context switching still hits us occasionally in this system. For example one of the animation blending tasks in the profiler screenshot takes longer than it should:


I have an idea for minimizing the impact of such context switches that I may try out in the future. If a task is purely functional (idempotent) then it doesn't matter how many times we run the task. So if we detect a situation where a large part of the system is waiting for a task on the critical path (that has been switched out by the OS) we can allocate other threads to run the same task. As soon as


I haven't implemented this because it complicates the model by introducing two different completion states for tasks. One where

A task in the new implementation is a simple data structure:

Here

**work**is a work item to be performed on an SPU, CPU or GPU.**affinity**can be set for items that must be performed on particular threads.**parent**specifies child/parent relationships between tasks. A task can have any number of children/subtasks. A task is considered*completed*when its work has been executed and all its children has completed. In practice this is implemented by the**open_work_items**counter. The counter is initially set to the number of child tasks + 1 (for the task's own work item). When a task completes, it reduces the**open_work_items***count of its parent and when that figure reaches zero, the parent work is completed.*I do not explicitly track completed task. Instead I keep a list of all open (i.e. not completed) tasks. Any task that is not in the open list is considered completed. Note that the open list is separate from the queue of work items that need to be performed. Items are removed from the queue when they are scheduled to a worker thread and removed from the open list when they have completed.

The

**dependency**field specifies a task that the task depends on. The task is not allowed to start until its dependency task has completed. Note that a task can only have a single dependency. The reason for this is that I wanted the task structure to be a simple POD type and not include any arrays or other external memory references.Having a single dependency is not a limitation, because if we want to depend on more than one task we can just introduce an anonymous task with no work item that has all the tasks we want to depend on as children. That task will complete when all its children has completed, so depending on that task gives us the wanted dependencies.

The

**priority**field specfies the importance of the task. When several tasks are available, we will pick the one with the highest priority. I will discuss this a bit more in a minute.The

*Task Manager*has a number of threads for processing tasks. Some of these are "main threads" that are created by other parts of the system and registered with the thread manager (in our case, an*update*thread and a*render*thread). The rest are worker threads created internally by the task manager. The number of worker threads is:*worker_thread_count = number_of_cores - main_thread_count*

The total number of threads managed by the task manager thus equals the number of cores in the system, so we have no over- or undersubscription.

The worker threads are in a constant loop where they check the task manager for work items to perform. If a work item is available, they perform it and then notify the task manager of its completion. If no work items are available, they sleep and are woken by the task manager when new work items become available.

The main threads run their normal serial code path. As part of that code path, they can create tasks and subtasks that get queued with the task manager. They can also

*wait()*for tasks to complete. When a thread waits for a task it doesn't go idle. Instead it loops and helps the task manager with completing tasks. Only when there are no more tasks in the queue does the thread sleep. It wakes up again when there are more tasks to perform or when the task it originally waited for has completed.The main threads can also process tasks while waiting for other events by calling a special function in the task manager

*do_work_while_waiting_for(Event &)*. For example, the update thread calls this to wait for the frame synchronization event from the render thread.This means that all task manager threads are either running their serial code paths or processing jobs -- as long as there are jobs to perform and they don't get preempted by the OS. This means that as long as we have lots of jobs and few sync points we will achieve 100 % core utilization.

This approach also allows us to freely mix serial code with a completely task based approach. We can start out with a serial main loop (with data parallelization in the

*update()*functions):void World::update()

{

_animation->update()

_scene_graph->update();

_gui->update();

render();

_sound->update();

}

And gradually convert it to fully braided parallelism (this code corresponds to the task graph shown above):

void World::update()

{

TaskId animation = _tasks->add( animation_task(_animation) );

TaskId scene_graph = _tasks->add( scene_graph_task(_scene_graph) );

_tasks->depends_on(scene_graph, animation);

TaskId gui = _tasks->add( gui_task(_gui) );

TaskId gui_scene = _tasks->add_empty();

_tasks->add_child(gui_scene, scene_graph);

_tasks->add_child(gui_scene, gui);

TaskId render = _tasks->add( render_task(this) );

_tasks->depends_on(render, gui_scene);

TaskId sound = _tasks->add( sound_update_task(_sound) );

TaskId done = _tasks->add_empty();

_tasks->add_child(done, render);

_tasks->add_child(done, sound);

_tasks->wait(done);

}

Note that tasks, subtasks and dependencies are created dynamically as part of the execution of serial code or other tasks. I believe this "immediate mode" approach is more flexible and easier to work with than some sort of "retained" or "static" task graph building.

A screenshot from our profiler shows this in action for a scene with 1000 animated characters with state machines:

Notice how the main and render threads help with processing tasks while they are waiting for tasks to be completed.

Once we have a task graph we want to make sure that our scheduler runs it as fast possible. Theoretically, we would do this by finding the critical path of the graph and making sure that tasks along the critical path are prioritized over other tasks. It's the classical

*task scheduling problem*.In a game, the critical path can vary a lot over different scenes. Some scenes are render bound, others are CPU bound. Of the CPU bound scenes, some may be bounded by script, others by animation, etc.

To achieve maximum performance in all situations we would have to dynamically determine the critical path and prioritize the tasks accordingly. This is certainly feasible, but I am a bit vary of dynamically reconfiguring the priorities in this way, because it makes the engine harder to profile, debug and reason about. Instead I have chosen a simpler solution for now. Each job is given a priority and the highest priority jobs are performed first. The priorities are not fixed by the engine but configured per-game to match its typical performance loads.

This seems like a resonable first approach. When we have more actual game performance data it would be interesting to compare this with the performance of a completely dynamic scheduler.

In the current implementation, all tasks are posted to and fetched from a global task queue. There are no per thread task queues and thus no task stealing. At our current level of task granularity (heavy jobs are split into a maximum of

*5 * thread_count*tasks) the global task queue should not be a bottleneck. And a finer task granularity won't improve core utilization. When we start to have >32 cores the impact of the global queue may start to become significant, but until then I'd rather keep the system as simple as possible.OS context switching still hits us occasionally in this system. For example one of the animation blending tasks in the profiler screenshot takes longer than it should:

I have an idea for minimizing the impact of such context switches that I may try out in the future. If a task is purely functional (idempotent) then it doesn't matter how many times we run the task. So if we detect a situation where a large part of the system is waiting for a task on the critical path (that has been switched out by the OS) we can allocate other threads to run the same task. As soon as

*any*of the threads has completed the task we can continue.I haven't implemented this because it complicates the model by introducing two different completion states for tasks. One where

*some*thread has completed the task (and dependent jobs can run) and another where*all*threads that took on the task have completed it (and buffers allocated for the task can be freed). Also, context switching is mainly a problem on PC which isn't our most CPU constrained platform anyway.
Great blog post and interesting design! I am curious to hear about any profiling findings based on specific game workloads and scaling results in regard to your single-queue and core-number assumption.









ReplyDeleteThe open list sounds like a neat idea - though I wonder how it will scale if you ever need more than one task-queue - though for sure a problem that can and will be solved when it shows to be a bottleneck.

In regard to the open list and the task ids - do you assume that all tasks the queue is empty on the start of every main loop cycle and will be empty again on the end of the cycle so there won't ever be any id collisions (might also simplify memory handling)?

Do you use dynamic memory (with a memory pool) to handle the task queue or a ring-buffer approach (sounds like a dynamic approach to me)?

I have got one question about the world::update example code: you add the "done" task at the end and add two children to it - does the child-add function check if the children are open and add the parent to them then (so the function that moves tasks from the open list manages the open work item count / parent relationship)? If you do that I assume that the whole open list is blocked when searching or manipulating it to prevent race conditions (add parent to a task while the task concurrently finishes and tries to be removed from the open list)?

Does the task::wait function check if it is called from inside a worker thread so it can warn that a whole thread might be blocked?

Are tasks enqueued on creation or do you have a batch-enqueue mode too?

Sorry for flooding you with all these questions - your tech and the openness you blog about it is amazing and inspiring - thank you for sharing it!

Cheers,

Bjoern

Thanks for the nice words Bjoern.







ReplyDeleteNo I don't assume that the task queue is empty on each main loop cycle. It is up to higher level systems to decide if they want to enforce that or not. The id is a 32 bit increasing counter. So if a higher level system created a task with very low priority and left it in the queue for the 24 hours or so that it will take for the id counter to wrap around we would have a problem. But that would be a silly thing to do :) There are always 64 bit ids if you really need them.

The task queue is a dynamically growing ring buffer. I.e. the ring buffer is backed by a vector that grows when the ring buffer becomes full.

You have skillfully detected that the sample code is actually a bit simplified! I did that to make the concepts clearer and not bog the reader down with details. What actually happens is that task creation is split in two parts begin_add() and finsih_add(). begin_add() creates the task, adds the work item to the queue and adds the task to the open list. But it sets the open_work_items field to 2 rather than 1. This means that the task will not be able to complete, even if a thread races away and executes its work item, because the open_work_items count will then still be at 1. So you can add child tasks, dependencies etc without worrying about race conditions. Then when you call finish_add(), the open_work_items counter is reduced by 1. This will complete the task if its work item has been exectued and no child tasks were added.

The task::wait() function works the same from worker threads as it does from main threads. It will consume tasks while waiting for the task to complete. So it is equally safe to call it from both worker threads and main threads.

A task is enqueued by TaskManager::begin_add(WorkItem &). There is also a faster function for adding a batch of tasks that don't have subtasks (and thus don't need begin_add, finish_add): TaskManager::add(size_t count, WorkItem *).

Cheers!

I have a question. From my understanding, the BitSquid engine mostly uses LUA for all of it's code. How do you manage that update, when LUA it's self isn't threaded?


DeleteDo you leave the LUA game-logic update on the main thread, and issue out threaded C++ calls as it's needed?

Yes, exactly.

DeleteOk, So as the Lua scripts run, the scripts will call out C++ functions when they are needed. Which gets dumped to another thread to run at the same time? If so, won't LUA hang on the function, while it waits for it to be completed?


DeleteOr, did you do something else?

Yes, the Lua->C++ calls does not run asynchronously in general.

DeleteThanks for your fast reply and explanations. The idea with the higher work item count is clever - great idea to use it that way.




ReplyDeleteAmazing that you implemented this in just a few days!

Looking forward to your next blog posts and to hear about more companies using the BitSquid Engine!

Cheers!

Nice.


ReplyDeleteDoes wait() wait for all tasks to complete? Because that would mean you can't have long running tasks.

No wait() just waits for a specific task.

ReplyDeleteThis is probably just another simplification in your sample code:



ReplyDelete> TaskId animation = _tasks->add( animation_task(_animation) );

> TaskId scene_graph = _tasks->add( scene_graph_task(_scene_graph) );

> _tasks->depends_on(scene_graph, animation);

It seems like this would kick off both the animation and scene_graph task immediately while you really want to delay the scene_graph execution until the animation task has completed. Or am I missing something?

In which way do you handle priorities:






ReplyDelete- Do you sort the task queue based on priorities, or

- do you sort chunks of it (to fight priority inversion)?

- Or does each worker look into a number of possible tasks before it decides to pick one (with locking of the whole queue/chunk)?

If a worker picks a task with the wrong affinity or which has to wait on its child tasks (or on the tasks dependent on it) does it requeue the task or didn't it pick it in the first case?

All of these questions come down to: do you lock the whole queue for picking a task (with your coarse granularity I assume this won't hurt that much as long as the core count is small) so you can evaluate tasks and when picking one out of input order reorganize the queue - or how do you fight fragmentation of the single queue?

Are the profiler graphs from your engines runtime profiler? How do you detect that a worker thread got context switched especially when you have no idea if all tasks are short or long running?

Wow, quite a meaty blog post ;-)

Cheers

What do you think about approach to process task based on data's dependence rather task's priority?


ReplyDeleteThis was in recently Ubisoft presentation at GDC 2010.

Phil: Yes it is another simplification. In reality the dependency is passed as an argument to begin_add(). Hmm... maybe I should have posted the real code instead of all these simplifications.

ReplyDeleteBjoern: Currently the task queue is implemented as a priority queue backed by a heap. (I've changed it from a ring buffer since my last reply.) And yes, job threads lock the queue when they look for new tasks (critical section with spin count). With finer granularity it might pay off to look into a lockless solution.




ReplyDeleteTasks with a dependency are kept in a "holding area" and not queued until their dependency is fulfilled. Affinity tasks are kept in separate per-thread queues. (Currently only single affinity is supported, not affinity masks.)

Yes, the graphs are from our profiler. Currently we don't detect context switches directly. The only way is to see that some tasks seem to take longer than they "should". Also, the color of each bar is mapped to the core that the thread was running on at the start of the job so color changes means that a job has jumped to a different core.

It would be nice to detect context switches directly and add that to the display, but I haven't had time.

Tomat: I'm not sure exactly what you mean. In a sense task order is already controlled by dependencies -- a task cannot run until it dependencies are fulfilled.



ReplyDeleteWhat you could do beyond that, I guess, is to sort on the length of the dependency chain. I. e., a task that has more things "depending on it" gets scheduled earlier. But it is a rather coarse instrument, since it doesn't take into account how long each task takes to process.

Using priorities seems better to me since it gives you a more diret control over the task execution order.

Thank you Niklas. Your two answers to Bjoern really made things clearer. Though showing the real code could be nice.


ReplyDeleteI think it is fairly challenging to determine context switches. The only way I have found is through some undocumented windows NT calls (http://undocumented.ntinternals.net/UserMode/Undocumented%20Functions/System%20Information/NtQuerySystemInformation.html) and I am not sure of the overhead yet. Let us know if you find a better way :)

Niklas: Thanks for all your answers and insights!

ReplyDeleteThanks for another great post :) I'm just wondering if you tried TBB scheduler and if yes why you decided to roll your own one :)

ReplyDeleteI've looked at the API briefly, but I haven't really tried it out.




ReplyDeleteMiddleware never does exactly what you want. Plugging in a middleware solution doesn't increase your understanding of the original problem (instead you now have to understand both the original problem, and the middleware solution to it). It tends to come with its own pre-conceived notion of how things are supposed to work that make your code rigid and inflexible. It often contains lots and lots of code, because it doesn't just solve your particular problem, but a host of related problems that other people might have. Often the code is deeply intertwined so you can't just extract the parts you need. Now you have tens of thousands of more lines of code in your engine with potential performance problems and bugs that you need to understand. Often the APIs and the documentation are bad by my standards (though there are exceptions, Lua is excellent, for instance).

I don't use middleware lightly. I think often its benefits are exaggerated and its costs overlooked.

I would never use middleware for something like this, where I need deep understanding of how it works, complete control so that I can experiment with different ideas and make it work as good as possible on all target platforms. And where, at the same time, the problem is quite small and there is really not that much code to write.

Thanks a lot for your insights. I was suspecting you would answer something like this :)




ReplyDeleteI guess when coding games for platforms with limited resources one always wants to have the full control over the one's code.

It's interesting too see to what extent one wants to go with such approach. Where is the edge? For example why roll another smart ptr implementation if there's nice collection of them in boost(despite the fact boost is considered to be a big fat "no" for game dev) Probably it's just the matter of the personal taste.

P.S. And, yes, you are right Lua has very beautiful internal implementation.

One more question, Niklas, if you don't mind. Do you ever have tasks which may span more than one frame? As for TBB it's not designed for such goals - what about your scheduler?


ReplyDeleteI'm a MMO developer and it's a pretty common situation to have some tasks which may last several frames(e.g. database query, hosts communication, etc).

My advise for handling long running tasks:



ReplyDelete- don't have long running tasks, instead split them so they can run asynchronously, e.g. have

-- a task for initiating an async query,

-- arrival of the finished query request is an event which creates a new task to handle it (see the concept of "sources" in Grand Central Dispatch)

Well, at least I'd suggest such an approach as long as we have only few cores/threads to handle computations and where blocking a core takes too many computational resources from us.

The event source (request ready, message arrived, timer fired, etc.) could use async methods offered by the platform or could itself be implemented by a (few) thread(s) that don't compute much other than slowly polling/waiting/blocking for events (so the don't need much processing time and won't need many context switches so they don't "block" a core from computations). Doing this in a cross-platform way will be lots of work and handling of platform special cases...

Long running tasks are either async-waiting for external events (network data, file reads, etc). For such tasks, the manager in charge of the system just polls for data every frame and handles it when it is available. The scheduler is not involved. (Except that we might spawn a task to handle a data chunk.)


ReplyDeleteOr, they are expensive computations whose result is not needed immediately. An example might be a recomputation of the AI graph. Such tasks are split into suitable "chunks" to be performed every frame and then we just queue one such chunk task every frame. This gives an even load balance over the frames, which is what we want.

@Niklas: could you please give a bit more details regarding your handling of long running tasks by specific subsystem managers? Does it boil down to having some sort of thread pool where long running tasks are executed and managers checking the statuses of these tasks?

ReplyDelete@bjoernknafla: thanks for your ideas, I'm definitely going to have a closer look at GCD. Is there a good howto/tutorial on it?

ReplyDelete@pachanga Grand Central Dispatch is an Apple technology (parts of it are open source) nonetheless it is worth studying because it is very streamlined and the "sources" concept is a step forward but it is not primarily targeted at performance oriented developers (no way to control locality/caches).


ReplyDeleteOk, after so much disclaiming - take a look here:

http://www.mikeash.com/pyblog/ - search on the site for "Grand Central Dispatch" for many in-depth blog articles - or google it and hit the official intro and reference pages by Apple.

Great article!


ReplyDeleteCan only the main thread post tasks or, for example, can other tasks spawn/create tasks or all "main threads" (both render and update threads) spawn tasks too?

I think you're doing the right thing having the tasks dynamically generated (after all, very little code has a static call graph - perhaps a shallow layer at the top, and possibly at the very leaves (where you want data parallelism anyway), but the middle is full of if-statements or even virtual calls and you really don't want to have to create "choice tasks" to do those - that would be painful as hell to work with).




ReplyDeleteFor the solution to the starvation problem I see basically two approaches:

1. Try to be clever with priorities (dynamically updated etc), optimistic evaluation etc.

2. Brute force it. Kick off *tons* of tasks to over-subscribe the system and give you enough parallel slackness that you always have stuff to do even when a task with lots of dependants takes longer than normal to finish.

In the long run 2 seems like the right option, IMO. Partly because Almdahl's law is going to dictate that your bottle neck will end up being any synchronisation points (so make sure they're dirt cheap - don't want to mess around with priorities here, just pick the next task, any one of them, and get started doing useful work!), and more threads will dictate that you want to tasks to be very cheap in the first place (so don't want any complicated logic determining the priority). So I think the best option is to focus on optimizing task spawning (get it down to an order of magnitude within the cost of a function call) by ignoring any cleverness, and then just spawn tons and tons of tasks without trying to do anything advanced w.r.t. scheduling.

See cilk for an example of this latter approach.

First of all many thanks for a great blog, I have learned a lot by reading it.



ReplyDeleteA couple of questions from a university student:

What are your workitems? Are they function pointers or some other kind of data structure?

Does the thread tell the task manager that it's free or does task manager poll the threads?

Sorry for a late comment to the post.

They are function pointers together with data blocks. The data blocks can contain raw data that is processed directory or pointers to memory areas where data should be read and/or written.


ReplyDeleteThe threads poll the task managers for new jobs and go into a waiting state if there are no jobs available. The task manager wakes the threads when it posts a new job.

Hi, there. Great blog and great articles!




ReplyDeleteI am wondering about your profiler implementation. You are gathering data from each core and then sending it via tcp/ip to the profiler. What is interesting to me is how do you solve the time-stamp problem of modern computers? We have many out-of-sync cores and on top of that, each core can be throttled up and down in time. The only thing, that comes to my mind is:

Idea 1) Measure time on each core and send, that data.

Idea 2) On a per core basis just check duration but the start-timestamp is always measured on one core. The one, that sends data over tcp/ip.

Idea 3) The timestamp is measured upon arrival in the profiler.

Each solution has its own set of problems. How can one reliably observe and measure multithreaded code?

That's not exactly what we do.



ReplyDeleteWe don't have a TCP/IP client running on each core. We only have a TCP/IP client on the main thread. For the other threads, we have synchronization points where the profiler data from that thread gets submitted to the main thread. Later, the main thread forwards the data to the profiler over TCP/IP.

At the synchronization point we can synchronize the clocks between the main thread and the other thread that is synchronizing.

Does this mean, that you affinitize threads on the PC in order to get consistent timer results?

DeleteWe haven't found that necessary. QueryPerformanceCounter() gives stable results (except on some old motherboards with buggy drivers).

DeleteHey, I was wondering how streaming is handled using this system. Are there tasks that will just keep running, are they split up? Or is there a completely separate thread to handle streaming?

ReplyDeleteYes, streaming is handled by a completely separate background thread that only is active when data is streamed.

ReplyDeleteYour blog is really wonderful. Thanks for sharing with us

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteHello there,



ReplyDeleteI'm 10 years late, I know, but I really wanted to understand how does some job becomes a task.

With that , I mean, how do you match some function signature with the "WorkItem" function pointer?

And we do understand we need you to appreciate for this.

ReplyDeleteMost of the illustrations you made, the easy web site menu.

Pedia4D adalah bandar togel online terbaik di indonesia saat ini, ayo daftar sekarang juga.

Mulai bermain situs totobet online

Situs agen judi totobet online

Bandar resmi situs totobet online

Pasang nomor situs totobet online

Cara taruhan situs totobet online

Dapat jackpot situs totobet online

대구출장샵


ReplyDelete대전출장샵

부산출장샵

울산출장샵

정선출장샵

울산출장샵

대구출장샵

부산출장샵

계룡출장샵


ReplyDelete춘천출장샵

청양출장샵

충북출장샵

강릉출장샵

충북출장샵

강릉출장샵

홍성출장샵