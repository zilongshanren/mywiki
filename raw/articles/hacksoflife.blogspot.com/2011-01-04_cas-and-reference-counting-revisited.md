---
title: CAS and Reference Counting Revisited
url: http://hacksoflife.blogspot.com/2011/01/cas-and-reference-counting-revisited.html
author: Benjamin Supnik
published: '2011-01-04'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[suggested](http://hacksoflife.blogspot.com/2009/07/cas-and-reference-counting-dont-mix.html)that we can't use atomic compare and swap (CAS) and reference counting together to update an arbitrary data structure because we can't atomically dereference the pointer and increase our reference count at the same time. The problem is that there is an instant while we are 'off the end' of the pointer that we haven't increased our reference count; an updater would have no idea that throwing out the copy of the data we are using is a poor idea.

Here's possible work-around: use the low bit of the pointer we want to CAS as a "lock" bit and spin. The algorithm would go something like this:

read begin:The idea here is that we can enforce spinning for a short time on other readers while we read the pointer to our block of data by always CASing in the low bit. (This assumes that memory is at least 2-byte aligned, which is an acceptable design assumption on pretty much all modern machines.) Thus we are holding a spin lock while we get our reference count registered.

while(1){ // this spins if someone else is trying to

ret = ptr // read-begin.

if(ptr, ptr | 1)) break

}

atomic_inc(&ptr->ref_count);

CAS(ptr, ptr & ~1);

return ret

read_end(data)

if atomic_dec(&data->ref_count)==0)

delete data

update:

while(1)

old = read_begin // take a ref count because we are copying from data

create new copy from old

if CAS(old,new){

assert(atomic_dec(&old->ref_count) > 0);

read_end(old) // two decs,

break

} else {

read_end(old) // we failed to swap, retry.*

delete new }

This code assumes that the data we are protecting has a baseline reference count of one - thus once an updater has replaced it, the updater removes this 'baseline' count, and the last reader to stop counting it (and an updater is a reader) releases it.

One reason why I only come back to RCU-style algorithms every few months is that (at least for this one) there's no way to block to ensure that the old copy of the data has been fully released. Knowing that your update is "fully committed" to all thread contexts is an important property that this algorithm does not have.

Reference counting works does work with concurrent updates, you just need so called strongly thread-safe RC. There are a lot of variations of the algorithms, here is one example:

ReplyDeletehttps://sites.google.com/site/1024cores/home/lock-free-algorithms/reader-writer-problem/wait-free-object-storage-with-single-word-atomic-operations

It allows only small fixed number of deferred objects in exchange for single-word atomic RMW operations. With double-word XADD/XCHG it's possible to implement very nice wait-free strongly thread-safe reference counting.

Dmitry, that's pretty cool. :-) In some ways, it's the same trick: cram more stuff into your 32 bits so you can 'atomically' update two things at once.


ReplyDeleteThe reference count + index solution is an interesting one...I will have to think about what other uses there might be for such overloading.

I've posted an article on the concept of strongly thread-safe differential reference counting:

ReplyDeletehttp://www.1024cores.net/home/lock-free-algorithms/object-life-time-management/differential-reference-counting

Right...so with differential reference counting there's no spin. On acquire, we increment the outer counter on ptr read, increment the inner counter, then go to decrement the outer counter. If the outer counter can't be decremented (because the base ptr has changed) we decrement the inner counter instead, because our count is transfered.





ReplyDeleteOn pointer-swap/update we first increment the inner counter with the outer counter's count. We then try the swap, and if it succeeds, we win. If we fail, we decrement the inner counter count we added and try again.

It does seem we have a slight bit-count issue...on a 32-bit machine we can either:

- Use a few bits for counters + a real ptr...but that's going to limit the outer counter by allocation granularity...I can see situations where we have more cores than free low bits, and thus we risk counter overflow (although the counter would have to be _highly_ contested for this to happen).

- Use an array offset for the ptr. But then we have a finite number of allocations we can do in a table, which strikes me as slightly less preferable to real object creation/deletion.

> ... then go to decrement the outer counter. If the outer counter can't be decremented (because the base ptr has changed) we decrement the inner counter instead, because our count is transfered.


ReplyDeleteNo, we just decrement the inner counter.

> On pointer-swap/update we first increment the inner counter with the outer counter's count. We then try the swap, and if it succeeds, we win. If we fail, we decrement the inner counter count we added and try again.


ReplyDeleteNo, we swap first, then update inner counter. The logic is wait-free.

> - Use a few bits for counters + a real ptr...but that's going to limit the outer counter by allocation granularity...




ReplyDeleteYou can control alignment dynamically. That is, if you have 64 worker threads, align objects on 64 bytes.

> - Use an array offset for the ptr.

You can consider it not as array, but as bounded pool. For example, reserve X MB of memory, organize bounded pool on top of the block. Then you can strip both low bits (due to alignemnt) and high bits (due to bounded pool).