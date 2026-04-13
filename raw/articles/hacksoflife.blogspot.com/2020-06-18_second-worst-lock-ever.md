---
title: Second. Worst. Lock. Ever.
url: http://hacksoflife.blogspot.com/2020/06/second-worst-lock-ever.html
author: Benjamin Supnik
published: '2020-06-18'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Four years ago I wrote a short post


To recap the problem: X-Plane's art assets are immutable and reference counted, so they can be accessed lock-free (read-only) from rendering threads.


But X-Plane also has a lookup table from file path to art asset that is functionally a table of weak references; on creation of an art asset we use the table to find that we already loaded the art asset and bump its count. On destruction we have to grab the table lock to clear out the entry.


So version one of the code, which was really really bad, looked like this:




The fix at the time was this:



Since the table is locked before the decrement, no one can get in and grab our object - we block out all other asset loaders before we decrement; if we hit zero reference count, we take out the sledge hammer and trash the object.



We hold the table lock during asset creation - the API contract for loaders is that you get back a valid* C++ object representing the art asset when the creation API returns, so this effectively means we have to hold the lock so that a second thread loading the same object can't return the partially constructed object being built by a first thread. This means the lock isn't a spin lock - it can be held across disk access for tens of milliseconds.


Well, that's not good. What happens when you put your object into a C++ smart handle that retains and releases the reference count in the constructor/destructor?


The answer is: you end up calling release all over the place and are constantly grabbing the table lock for one atomic op, and sometimes you're going to get stuck because someone else is doing real loading.


The reason this is a total fail is: client code would not expect that simply



void object::release()

{


This is sort of like double-checked locking: we do an early first check of the count to optimize out the table lock when it is obvious we aren't the deleter (our reference count is greater than zero after we decrement). Once we take the table lock, we then re-check that no one beat us into the table between the decrement and the lock, and if we are still okay, we delete.


The win here is that we only take the table lock in the case where we are very likely to deallocate - and client code should only be hitting that case if the client code is prepared to deallocate a resource, which is never fast. With this design, as long as resource deallocation (at the client level) is in the background with resource creation, we never hit the table lock from any critical rendering path or incidental book-keeping.


* With the Vulkan renderer we now have art assets that complete some of their loading asynchronously - this is more or less mandatory because DMA transfers to the GPU are always asynchronous. So the synchronous part of loading is establishing a C++ object functional enough to "do useful stuff with it."


We could start to erode this time by having more functionality be asynchronously available and less be always-guaranteed. But in practice it's not a real problem because entire load operations on the sim itself are already in the background, so lowering load latency doesn't get us very much real win.

[describing a dumb race condition](http://hacksoflife.blogspot.com/2016/07/worst-lock-ever.html)in our reference counted art assets.To recap the problem: X-Plane's art assets are immutable and reference counted, so they can be accessed lock-free (read-only) from rendering threads.

But X-Plane also has a lookup table from file path to art asset that is functionally a table of weak references; on creation of an art asset we use the table to find that we already loaded the art asset and bump its count. On destruction we have to grab the table lock to clear out the entry.

So version one of the code, which was really really bad, looked like this:

void object::release() { if(m_count.decrement() == 0) { // Race goes here RAII_lock (m_table_lock()); m_table.erase(this->name); delete this; } }This code is bad because after we decrement our reference count, but before we lock the table, another thread can go in, lock the table, find our art asset, increment its reference count and unlock the table - this would be caused by an async load of the same art asset (in another thread) hitting the "fast path". We then delete a non-zero-count object.

The fix at the time was this:

void object::release() { RAII_lock (m_table_lock()); if(m_count.decrement() == 0) { m_table.erase(this->name); delete this; } }

Since the table is locked before the decrement, no one can get in and grab our object - we block out all other asset loaders before we decrement; if we hit zero reference count, we take out the sledge hammer and trash the object.

### Correct But Stupid

The problem with this new design is that it holds the table lock across*every*release operation - even ones where there is*no*chance of actually releasing the object.We hold the table lock during asset creation - the API contract for loaders is that you get back a valid* C++ object representing the art asset when the creation API returns, so this effectively means we have to hold the lock so that a second thread loading the same object can't return the partially constructed object being built by a first thread. This means the lock isn't a spin lock - it can be held across disk access for tens of milliseconds.

Well, that's not good. What happens when you put your object into a C++ smart handle that retains and releases the reference count in the constructor/destructor?

The answer is: you end up calling release all over the place and are constantly grabbing the table lock for one atomic op, and sometimes you're going to get stuck because someone else is doing real loading.

The reason this is a total fail is: client code would not expect that simply

*moving around*ownership of the reference would be a "slow" operation the way true allocation/deallocation is. If you say "I release an art asset on the main thread and the sim glitched" I tell you you're an idiot. If you say "my vector resized and I locked the sim for 100 ms", that's not a good API.### Third Time's a Charm

The heart of the bug is that we eat the expensive table lock when we release regardless of whether we need it. So here's take three:void object::release()

{

void object::release() { if(m_count.decrement() == 0) { RAII_lock (m_table_lock()); // If someone beat us to the table lock, check and abort. if(m_count.load() > 0) return; m_table.erase(this->name); delete this; } }

This is sort of like double-checked locking: we do an early first check of the count to optimize out the table lock when it is obvious we aren't the deleter (our reference count is greater than zero after we decrement). Once we take the table lock, we then re-check that no one beat us into the table between the decrement and the lock, and if we are still okay, we delete.

The win here is that we only take the table lock in the case where we are very likely to deallocate - and client code should only be hitting that case if the client code is prepared to deallocate a resource, which is never fast. With this design, as long as resource deallocation (at the client level) is in the background with resource creation, we never hit the table lock from any critical rendering path or incidental book-keeping.

* With the Vulkan renderer we now have art assets that complete some of their loading asynchronously - this is more or less mandatory because DMA transfers to the GPU are always asynchronous. So the synchronous part of loading is establishing a C++ object functional enough to "do useful stuff with it."

We could start to erode this time by having more functionality be asynchronously available and less be always-guaranteed. But in practice it's not a real problem because entire load operations on the sim itself are already in the background, so lowering load latency doesn't get us very much real win.

> moving around ownership of the reference would be a "slow" operation ...


ReplyDeleteWouldn't a move constructor/assignment that does not fiddle with the reference count fix this? It would imply that "moved-from" objects are invalid, but should not be a big deal.

I think you're right that a move operation would be fast. The problem is: sometimes the client can't use move semantics. For example: the scene graph has an entity (and holds a strong reference).



DeleteThe rendering code is going to "collect" visible scene graph entities for drawing, and in doing so, _must_ take out its own references because it (1) cannot steal a reference from the scene graph (which lives on) and (2) cannot guarantee that later, while the collection is being drawn, the scene graph won't be mutated, releasing the reference.

This is a real case in our code that requires us to not have a smart handle copy constructor take a lock.