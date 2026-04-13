---
title: Worst. Lock. Ever
url: http://hacksoflife.blogspot.com/2016/07/worst-lock-ever.html
author: Benjamin Supnik
published: '2016-07-08'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Here's some really good code:



This was the code to release an art asset in X-Plane 10.45r2.


Can you see what's wrong with it? Don't over think it; it's not a relaxed vs sequential atomics issue or a bug in the RAII code. The logic is roughly this:




The issue is a data race! The race exists




Being too clever for my own good, I thought "let's be clever and just re-check the reference count after we take the global lock; in the rare load-during-delete we can then abort the load, and in most cases releasing our reference count stays fast.


That fixes the above race condition but doesn't fix this other race condition: in the space between the decrement and the lock:




So I've come to the conclusion that the only safe thing to do is to take the table lock first before doing any decrement. In the event that we hit zero reference count, since we did so


This isn't great for performance; it means we take a global lock (per class of art asset) on any reference count decrement, but I




```
if(atomic_dec(&my_ref)==0)
{
StLock take_lock(&global_asset_lock);
global_asset_table.erase(this);
delete this;
}
```


This was the code to release an art asset in X-Plane 10.45r2.

Can you see what's wrong with it? Don't over think it; it's not a relaxed vs sequential atomics issue or a bug in the RAII code. The logic is roughly this:

- Decrement my reference count.
- If I was the last one (and my count is now zero):
- Lock the global table of art assets.
- While the table is locked, clear out my entry.
- Delete myself.

The issue is a data race! The race exists

*between*the completion of the atomic decrement and acquiring the table lock. In this space another thread can come along and:- Try to load this same art asset; it will acquire the table lock, look up our art asset, find it, increase the reference count back to 1.
- It will then drop the lock, leaving us exactly how we were
*except*our reference count is now 0. - When we proceed to nuke the art asset we will leave that other client with a bad pointer and crash.

Being too clever for my own good, I thought "let's be clever and just re-check the reference count after we take the global lock; in the rare load-during-delete we can then abort the load, and in most cases releasing our reference count stays fast.

That fixes the above race condition but doesn't fix this other race condition: in the space between the decrement and the lock:

- Another thread takes the global lock, finds our art asset, and increases its reference count, drops the table lock.
- That thread then releases its reference, which hits zero, takes the lock, deletes the art asset and the table entry and releases the lock.

*we*are the ones with a bad pointer, and we crash re-deleting the art asset.So I've come to the conclusion that the only safe thing to do is to take the table lock first before doing any decrement. In the event that we hit zero reference count, since we did so

*while*the table is locked, no one could have found our art asset by the table to increase the count (and clearly no one else already had it if we went from ref == 1 to ref == 0). So now we know it's safe to delete.This isn't great for performance; it means we take a global lock (per class of art asset) on any reference count decrement, but I

*think*we can survive this; we have already moved not only most loading but most*unloading*to asynchronous worker threads, so we're eating the lock in a place where we can afford to take our time.### A More Asynchronous Design

I can imagine a more asynchronous design:

- The table of art assets itself holds one reference count.
- When we decrement the reference count to one, we queue up an asynchronous table "garbage collection" to run on a worker thread.
- The garbage collection takes the table lock once to find and clean out unused art assets, blocking loads for a small amount of time while the table is inspected.

I have not had a chance to profile the simple solution since trying to make it correct; if it turns out to be a perf problem I'll post a follow-up. The only time we've seen a perf problem is when the table lock was required for

*all*operations (this was a design that we fixed almost a decade ago -- a design that was okay when it was single threaded and thus lock free).
The rendering path in X-Plane requires no reference count changes at all, so it is unaffected by anything on this path.

Question: if you are the only ones with a reference to this art asset, how can another thread acquire a reference to it? Sorry just not at-all familiar with X-plane internals.

ReplyDeleteFor each class of art asset, there's a map of file paths -> loaded assets that lets us recycle already-loaded assets by bumping up their reference counts. This table needs to be locked to be used, but that only imposes a penalty on load and unload operations; once you have a ref count on the asset, it's immutable until you release it, so you can just use it without a lock.

DeleteOr just don't recover from a zero ref count. When incrementing, load and cas. If you load zero the resource is dead; reload.

ReplyDeleteThe problem here is keeping the lookup-by-asset table consistent. If the resource is in the table with zero counts, it is going to get removed; how do we put our -new- copy (of the same file) into the lookup table by path without a collision?

DeleteI'm assuming that this line:





















Deleteglobal_asset_table.erase(this);

isn't actually what happens in the real code, and it really does something like:

global_asset_table.erase(this->name);

Otherwise you already have multiple mappings to the same resource and there's really no collision problem, is there?

Anyway. If all you have is a single mapping:

map<string, resource*>

There are still a lot of ways to handle this.You are obviously already holding the lock in load(), so collisions while loading can´t happen.Thus the only thing we care about is making

sure we don't erase a resource that has been replaced.

Here's one way; make the mapping:

map<string, pair<int, resource*>> rmap;

Where the first pair element is an epoch. Implement the load like:

resource* load(string const& name)

{

lock l(mutex);

auto it = rmap.find(name);

if (it == rmap.end())

{

// ...

return new_resource;

}

auto* r = it->second.second;

int count = r->my_ref.load(std::memory_order_relaxed);

for (;;)

{

if (count == 0)

{

int epoch = it->second.first;

resource* new_resource = new resource;

new_resource->epoch = epoch + 1;

it->second = std::make_pair(epoch + 1, new_resource);

return new_resource;

}

if (r->my_ref.compare_exchange_weak(count, count + 1))

break;

}

return it->second.second;

}

and the unload like:

void unload(resource* r)

{

if (r->my_ref.fetch_sub(1) > 1)

return;

lock l(mutex);

auto it = rmap.find(r->name);

if (it->second.first == r->epoch)

rmap.erase(it);

delete r;

}

Interesting solution! And yes, you are exactly right, the resource erase (from the table's standpoint) is a "nuke my key", where we know the key is in only once.

DeleteWe had the same issue in our memory manager / caching system, I wanted to get away with pure atomic in the fast path, but it is not possible without the cleanup thread idea. We also live with the lock.

ReplyDelete