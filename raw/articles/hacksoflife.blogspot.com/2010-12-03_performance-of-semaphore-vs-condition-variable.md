---
title: Performance of Semaphore Vs. Condition Variable
url: http://hacksoflife.blogspot.com/2010/12/performance-of-semaphore-vs-condition.html
author: Benjamin Supnik
published: '2010-12-03'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

X-Plane 10 features a threaded flight model (or rather, the flight model of all airplanes is executed in parallel). This is a case where we do care about latency (since we can't proceed until the flight model completes*) and the job size is not that big, so overhead matters more.

Our old message queue was based on a pthread condition variable. It was taking about 200 µsec to launch all workers, and a Shark analysis showed what I can only describe as a "total train wreck" of lock contention. The workers were waking up and immediately crashing into each other trying to acquire the mutex that protects the condition variable's "guts".

I replaced the condition variable + mutex implementation of the message queue with the implementation that already ships on Windows: a critical section to protect contents plus a semaphore to maintain count. I implemented the semaphore as an atomic wrapper around a mach semaphore. (See the libdispatch semaphore code for an idea of how to do this.) The results were about 2x better: 80 µsec to launch from sleep, about 45 µsec of which were spent signaling the mach semaphore (5-10 µsec per call) plus a little bit of overhead.

So why was the new implementation faster? I dug into the pthreads source to find out.

What Happens With PThreads

The pthread implementation on OS X (at least as of 10.5.x whose source I browsed, it's in libc btw) goes something like this:

- A spin lock protects the "guts" of both a pthread mutex and a pthread condition variable.
- An OS semaphore provides the actual blocking for a pthread mutex and a pthread condition variable.

The condition variable sequence is a little bit trickier. A signal to a condition variable with no waiters is a fast early exit, but we have to grab the spin lock twice if we signal someone. The condition wait is the painful part. pthread_cond_wait has to reacquire the locking mutex once the waiter is signaled. This is the source of the deadlock; if a lot of messages are written to a lot of worker threads at once, the worker threads bottleneck trying to reacquire the mutex that is tied to the condition variable that woke them up.

Better With Semaphores

When using the atomic semaphore/critical section design, the advantage we get is significantly finer-grained locking. The lock on our message queue now only protects the queue items themselves, and is never held while we are inside pthread code. This gets us through significantly faster. It is inevitable that if we are going to queue work to many threads via one queue, there's going to be some bottleneck trying to get the messages out. This design minimizes the cost of getting a message out and thus minimizes the serialization path.

(Shark doesn't have quite the res to measure it in the code example I have running now, but I suspect that some of the cost still in the system is the spin time waiting for messages to be pulled.)

Part of the win here is that we are using a spin lock rather than a sleep lock on the message queue; while the pthread mutex will fast-case when uncontested, it will always sleep the thread if even two threads are trying to acquire the mutex. If the protected piece of code is only a few instructions, a spin is a lot cheaper than the system call to block on a semaphore.

Better Throughput When Pre-Queued

One of the things that made the old design go haywire in the version 10 test case was that it was a two-level set of messsage queues, with the main job list containing a message to go check another queue for the actual work. (Believe it or not there is a good design reason for this, but that's another post.) In this two-level design the semaphore + critical section hits its fast case. The second queue is already full by the time we start waking up workers. Therefore the second queue's semaphore is positive, which means that the decrement in the message dequeue will hit the fast atomic operations case and be non-blocking. The workers then simply have to grab the spin lock, pop the message, and be done.

(Again, the pthread implementation can fast-case when the mutex is uncontested, but it doesn't spin.)

To forestall the comments: this is not a criticism of the performance of pthread condition variables and mutices; performance could certainly also have been boosted by using a different set of pthread synchronizers. It is mainly an observation that, because the pthread mutex is heavier than a spin lock, condition variables may be expensive when you wanted a light-weight lock but didn't get one.

Future Performance Boosts

There is one additional performance boost I have been looking at, although I am not sure when I will put it into place. The message queue (which is a lock around an STL list right now**) could be replaced with a ring buffer FIFO. With the FIFO design we would maintain:

- A pair of semaphores, counting filled and free entries. Reading/writing blocks until the needed filled/free entry is available.
- Atomic read/write pointers that can be advanced once the semaphore indicates that there is content/free space to advance to.

Two things stop me from dropping this in:

- Our current message queue API assumes that messages can always be written and that writing is reasonably fast. (The current write only needs to acquire a spin lock.) If the ring buffer can fill, we could block indefinitely until space is available, or we have to expose to client code that writes can time out. That's a pretty big change.
- The current queue has a lock-and-edit operation that is used to optimize the case where queued jobs have to be flushed. Since the ring buffer FIFO is lock free, we can't really lock it to inspect/edit it.

I am trying to implement a ring buffer FIFO with as little blocking as possible and also thought of using semaphore pairs and atomic read/write increments.

ReplyDeleteHow do you solve the issue where reader A starts reading (presumably increasing the read head) but is interrupted by reader B. Reader B finishes reading and increments the free entry semaphore. Sender C comes along and writes over what reader A is in the middle of reading.

Same issue for multiple simultaneous senders.

Hi Matthew,










ReplyDeleteIf you have multiple readers, you can't really guarantee sequential execution of the dequeued FIFO items...by this I mean: even with a fully serialized read, the thread that pulled out item 1 might then be descheduled while the thread that pulled out item 2 actually got to run.

In our design we don't worry about this. We assume that while items will be dequeued in roughly the order they are enqueued, the precise order can fluctuate a bit with thread scheduling. (In particular, if you want to ensure that all items previously queued are _completed_, you need to use some kind of separate barrier -- the FIFO won't tell you that.)

Our current design currently does have a lock -it supports some strange operations that make a non-blocking FIFO impossible , so what I am about to describe is a little bit theoretical.

With that in mind, the way you solve the FIFO problem I think is:

Read:

1. decrement the available items semaphore

2. atomically increment the read ptr (its old position is "your" item).

3. extract the item.

4. increment the available empty space semaphore

Write:

1. decrement the free space semaphore

2. atomically increment the write ptr (its old position is where we write).

3. write the item into place

4. increment the available items semaphore

In particular, at any one time, the sum of the semaphores may be _less_ than the size of the FIFO (Becasue we always decrement first, increment second). This effectively keeps the read and write ptrs from covering the entire ring buffer, thus protecting "your item".

The double-reader case works as follows:

- If there is only one available item, reader B will block on the semaphore.

- If there are two items available, both readers A and B atomically increment the read ptr (which is _not_ the semaphore) pulling out two items...NOT necessarily in order, but guaranteeing each item is sent to a reader exactly once.

If "fairness" is required (e.g. the reader queued to the semaphore first gets the first item) you need some other design...I think even a condition-variable design would fail this criteria.

cheers

ben