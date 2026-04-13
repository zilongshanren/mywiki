---
title: Alternatives to object handles
url: http://c0de517e.blogspot.com/2011/03/alternatives-to-object-handles.html
published: '2011-03-02'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I'm tired, so I'll write this as a "note to self" (even more than how I usually do here).

Hot-swapping (and similar concepts) are often implemented with object handles and a "manager". Refcounting is often used to manage object lifetime.


A possible implementation is to have all the resources stored in the manager, let's say in an array, and the handles could be the index into this array. Or the handle could be a pointer to a shared object that points to the resource on the heap (same as C++ TR1 shared_ptr, but sharing also the pointer, not only the refcount) and the manager can just have an array of pointers to the resources on the heap.


This works well, but it introduces an indirection that will cause cache misses every time we have to access to the actual resource, especially if the resource is small and could be stored directly in the structures that need it, for example shader constants that can be represented just with the GPU pointer that contains the data to be set in the ring buffer (i.e. NVidia OpenGL bindless API see


Also, in general reference counting is not the best idea to manage object lifetime. It leaks memory if we have cyclic references, leaks that are not hard to detect with a debugging allocator but that can be complex to fix. It's also not too fast when destructing objects, as an object desctruction can trigger a chain of RC destructions or RC decrements that can cause more cache misses.

A possible implementation is to have all the resources stored in the manager, let's say in an array, and the handles could be the index into this array. Or the handle could be a pointer to a shared object that points to the resource on the heap (same as C++ TR1 shared_ptr, but sharing also the pointer, not only the refcount) and the manager can just have an array of pointers to the resources on the heap.

This works well, but it introduces an indirection that will cause cache misses every time we have to access to the actual resource, especially if the resource is small and could be stored directly in the structures that need it, for example shader constants that can be represented just with the GPU pointer that contains the data to be set in the ring buffer (i.e. NVidia OpenGL bindless API see

[http://developer.download.nvidia.com/opengl/tutorials/bindless_graphics.pdf](http://developer.download.nvidia.com/opengl/tutorials/bindless_graphics.pdf)).Also, in general reference counting is not the best idea to manage object lifetime. It leaks memory if we have cyclic references, leaks that are not hard to detect with a debugging allocator but that can be complex to fix. It's also not too fast when destructing objects, as an object desctruction can trigger a chain of RC destructions or RC decrements that can cause more cache misses.

Ideas:

- Storing the objects to be "patched" in the manager. We avoid handles, but when a pointer to a resource is obtained, the location of the pointer is stored in the manager (via a multimap: resource pointer to list of locations that point to it).
- Pros:
**No extra indirection, nor extra space used in the objects that hold the resource (other than the resource itself)**- Still it can be wrapped in something having the interface of a shared_ptr, so the solution allows to go back to a more standard object handle implementation if wanted.
**Can move resources in memory easily!**Sort them to have cache-coherent access (if possible)- It's even an alternative to intrusive_ptr (Boost), that is a good (performance-wise) way of doing RC (without hot-swapping) that also does not incur in space penalty in the objects that point to resources but it can be used only to point to objects that implement a given interface.
- Cons:
**It will have way worse performance every time you change one of the pointers to a resource!**

- Requires a complex data structure, difficult to implement and balance.
- In general it will require more space.
- It will patch objects... not the most clean thing... nor the most robust, you can easily forget registering a temporary copy of an handle in the manager or you really have to be sure that no such temporaries exist when you swap things...
- It will have worse performance on object creation and most probably, destruction (handles and RC are not great in destruction too, it's hard to say because they can trigger a chain of RC destructions or decrements that results in cache misses).
- It will be harder and slower to make thread-safe, even assuming that the hotswapping happens while the application is single-threaded.
- "Hardcoded" Garbage Collection. Very similar to having an "update" function that triggers the caching of resource pointers to resource caches in the various classes, but without the need of having to waste space... Every class that holds references to GC objects implements a "walking" function that will mark them. Every GC object will need a flag to check if it was marked. We still need a manager with a list of all the GC objects.
- Pros:
**Safe even in presence of cycles.**- Not too much of an extra burden if you're writing methods in every class for things like reflection (actually, if you have any form of reflection of the fields in your objects, this will be "free") or serialization...
- At no extra cost you also will know which objects are holding references to your resources...
- Cons:
**Changing a resource is almost as expensive as a GC, we will need to walk through all the references!**- Different interface, can't change your mind easily.
- Error-prone, you can easily forget to update one of the tracking functions, and still you have to make sure you never create untracked copies of an handle, i.e. a temporary (or well, you have to be sure none of them are around by the time you execute the GC/hot swapping)
- You will need to be a genius to have the GC or the reference-updating process run in parallel or incrementally.
- List of references. Similar to the first idea, but instead of the multimap we just store a list of all the locations that contain resources. When we have to change them, we go through all the list and see which ones need patching
- Pros:
**No extra indirection, nor extra space used in the objects that hold the resource (other than the resource itself)**- Still it can be wrapped in something having the interface of a shared_ptr, so the solution allows to go back to a more standard object handle implementation if wanted.
- Cons:
**Changing a resource is still expensive, we will need to walk through all the references.**- We probably still would need to maintain a separate list of resources, other than the list of patching locations, if we need to be able to enumerate and find them... In general it will require more space.
- It will patch objects... not the most clean thing... see above...
- Again, harder and slower to make thread-safe

- Permutation array. We add a second indirection level, to be able to sort resources to cause less cache misses. An handle in an index into an array of indices (permutation) of the array that stores the resources.
- Pros:
- Resources can be easily moved around in memory, and be sorted to be cache-friendly.
- Cons:
**Many times we don't have a coherent memory access order...****Many times the resources are actually small, so the array of indices won't cache-miss less than the actual array of resources!***yes, this one is not a great idea most of the times...*


But maybe this is all wrong, as I said, I'm tired. I'll think about it more another day... Comments as always are welcome.


p.s. Hybrids are also possible I guess... Like dividing the locations roughly into buckets (i.e. depending on part of the msb of the pointed resource) thus trying to minimize the cost of mutating pointers in the first solution (list add and delete would be needed only if the pointer changes to a resource in a different bucket).

p.s. Hybrids are also possible I guess... Like dividing the locations roughly into buckets (i.e. depending on part of the msb of the pointed resource) thus trying to minimize the cost of mutating pointers in the first solution (list add and delete would be needed only if the pointer changes to a resource in a different bucket).

## 3 comments:

Dynamic binary translation?

PHP sidechannel metarendering?

It strongly depends on the data you want to access.




The indexed solution works great when you can order your data according to an access pattern.

If you want to e.g. store and reference 2d-points you can create a spatial hierarchy (quadtree, kdtree, etc.) and store the data in many small arrays at it's leafs.

If you don't have overlapping data ranges you can also do this in one big array.

The advantage over a simple "push back" array is that you will always get data in a common context which reduces the average cache miss rate as you will most likely access many objects in the same area.

So - Index based is great as long as you can order your data according to a common access pattern.

If you can't find such a pattern your pretty much bound to random access and fu...ed anyway (in terms of cache misses).

Post a Comment