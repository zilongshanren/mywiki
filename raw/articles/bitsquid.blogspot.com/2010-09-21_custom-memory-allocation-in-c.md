---
title: Custom Memory Allocation in C++
url: https://bitsquid.blogspot.com/2010/09/custom-memory-allocation-in-c.html
author: Niklas
published: '2010-09-21'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

You can override global new and replace it with something else. This way you can get some basic memory tracking, but you still have to use the same allocation strategy for all allocations, which is far from ideal. Some systems work better with memory pools. Some can use simple frame allocation (i.e., pointer bump allocation). You really want each system to be able to have its own custom allocators.

The other option in C++ is to override

*new*on a per class basis. This has always has seemed kind of strange to me. Pretty much the only thing you can use it for are object pools. Global, per-class object pools. If you want one pool per thread, or one pool per streaming chunk -- you run into problems.

Then you have the STL solution, where containers are templated on their allocator, so containers that use different allocators have different types. It also has fun things such as

*rebind()*. But the weirdest thing is that all instances of the allocator class must be equivalent. So you must put all your data in static variables. And if you want to create two separate memory pools you have to have two different allocator classes.

I must admit that every time I run into something in STL that seems completely bonkers I secretly suspect that I have missed something. Because obviously STL has been created by some really clever people who have thought long and hard about these things. But I just don't understand the idea behind the design of the custom allocator interface at all. Can any one explain it to me? Does any one use it? Find it practical? Sane?

If it weren't for the allocator interface I could almost use STL. Almost. There is also the pretty inefficient

*map*implementation. And the fact that

*deque*is not a simple ring buffer, but some horrible beast. And that many containers allocate memory even if they are empty... So my own version of everything it is. Boring, but what's a poor gal gonna do?

Back to allocators. In conclusion, all the standard C++ ways of implementing custom allocators are (to me) strange and strangely useless. So what do I do instead? I use an abstract allocator interface and implement it with a bunch of concrete classes that allocate memory in different ways:

class Allocator { public: virtual void *allocate(size_t size, size_t align) = 0; virtual void deallocate(void *p) = 0; virtual size_t allocated_size(void *p) = 0; }

I think this is about as sane as an allocator API can get. One possible point of contention is the

*allocated_size()*method. Some allocators (e.g., the frame allocator) do not automatically know the sizes of their individual allocations, and would have to use extra memory to store them. However, being able to answer questions about allocation sizes is very useful for memory tracking, so I require all allocators to provide that information, even if it means that a frame allocator will have to use a little extra memory to store it.

I use an abstract interface with virtual functions, because I don't want to template my classes on the allocator type. I like my allocators to be actual objects that I can create more than one of, thank you very much. Memory allocation is expensive anyway, so I don't care about the cost of a virtual function call.

In the BitSquid engine, you can

**only**allocate memory through an

*Allocator*object. If you call

*malloc*or

*new*the engine will

*assert(false)*.

Also, in the BitSquid engine all allocators keep track of the total number of allocations they have made, and the total size of those allocations. The numbers are decreased on

*deallocate()*. In the allocator destructor we

*assert(_size == 0 && _allocations == 0)*and when we shut down the application we tear down all allocators properly. So we know that we don't have any memory leaks in the engine. At least not along any code path that has ever been run.

Since everything must be allocated through an

*Allocator*, all our collection classes (and a bunch of other low-level classes) take an

*Allocator &*in the constructor and use that for all their allocations. Higher level classes either create their own allocator or use one of the globals, such as

*memory_globals::default_allocator()*.

With this interface set, we can implement a number of different allocators. A

*HeapAllocator*that allocates from a heap. A

*PoolAllocator*that uses an object pool. A

*FrameAllocator*that pointer bumps. A

*PageAllocator*that allocates raw virtual memory. And so on.

Most of the allocators are set up to use a backing allocator to allocate large chunks of memory which they then chop up into smaller pieces. The backing allocator is also an

*Allocator*. So a pool allocator could use either the heap or the virtual memory to back up its allocations.

We use proxy allocators for memory tracking. For example, the sound system uses:

ProxyAllocator("sound", memory_globals::default_allocator());

which forwards all allocations to the default allocator, but keeps track of how much memory has been allocated by the sound system, so that we can display it in nice memory overviews.

If we have a hairy memory leak in some system, we can add a

*TraceAllocator*, another proxy allocator which records a stack trace for each allocation. Though, truth be told, we haven't actually had to use that much. Since our

*assert*triggers as soon as a memory leak is introduced, and the

*ProxyAllocator*tells us in which subsystem the leak occurred, we usually find them quickly.

To create and destroy objects using our allocators, we have to use placement new and friends:

void *memory = allocator.allocate( sizeof(MyClass), alignof(MyClass) ); MyClass *m = new (memory) MyClass(10); if (m) { m->~MyClass(); allocator.deallocate(m); }

My eyes! The pain! You certainly don't want to type or read that a lot. Thanks C++ for making my code so pretty. I've tried to make it less hurtful with some template functions in the allocator class:

class Allocator { template <class T, class P1> T *make_new(const P1 &p1) {return new (allocate(sizeof(T), alignof(T))) T(p1);} template <class T> void make_delete(T *p) { if (p) { p->~T(); deallocate(p); } }

Add a bunch of other templates for constructors that take a different number of arguments that can be const or non-const and now you can at least write:

MyClass *m = allocator.make_new<MyClass>(10); allocator.make_delete(m);

That's not too bad.

One last interesting thing to talk about. Since we use the allocators to assert on memory leaks, we really want to make sure that we set them up and tear them down in a correct, deterministic order. Since we are not allowed to allocate anything without using allocators, this raises an interesting chicken-and-egg problem: who allocates the allocators? How does the first allocator get allocated?

The first allocator could be

*static*, but I want deterministic creation and destruction. I don't want the allocator to be destroyed by some random

*_exit()*callback god knows when.

The solution -- use a chunk of raw memory and

*new*the first allocator into that:

char _buffer[BUFFER_SIZE]; HeapAllocator *_static_heap = 0; PageAllocator *_page_allocator = 0; HeapAllocator *_heap_allocator = 0; void init() { _static_heap = new (_buffer) HeapAllocator(NULL, _buffer + sizeof(HeapAllocator), BUFFER_SIZE - sizeof(HeapAllocator)); _page_allocator = _static_heap->make_new<PageAllocator>("page_allocator"); _heap_allocator = _static_heap->make_new<HeapAllocator>("heap_allocator", *_page_allocator); ... } void shutdown() { ... _static_heap->make_delete(_heap_allocator); _heap_allocator = 0; _static_heap->make_delete(_page_allocator); _page_allocator = 0; _static_heap->~HeapAllocator(); _static_heap = 0; }

Note how this works

*. _buffer*is initialized statically, but since that doesn't call any constructors or destructors, we are fine with that. Then we placement new a

*HeapAllocator*at the start of that buffer. That heap allocator is a static heap allocator that uses a predefined memory block to create its heap in. And the memory block that it uses is the rest of the

*_buffer*-- whatever remains after

*_static_heap*has been placed in the beginning.

Now we have our bootstrap allocator, and we can go on creating all the other allocators, using the bootstrap allocator to create them.

STL allocators were probably never designed for custom allocation techniques (e.g. pools), but rather to abstract the memory model (Stepanov mentions allowing persistent memory models). They seem to mainly have been pushed by external parties, and Stepanov himself says they are pretty flawed semantically (can't do find(a.begin(), a.end(), b[1]); where a and b are vectors with different allocators for example).


ReplyDeletehttp://www.sgi.com/tech/stl/drdobbs-interview.html

http://www.stlport.org/resources/StepanovUSA.html

Read the paper:


ReplyDeletehttp://www.google.com/search?q=reconsidering+custom+memory+allocation

malte: Ah, I see, it was mostly a way to support Win16 and segmented memory. Makes sense. And then people started using them for memory pools and what not because "they were there".

ReplyDeletelionet: Of course, one of the allocators in the system should be DougLeaAllocator (in fact, that is exactly what our HeapAllocator is). And if you are using some other allocator because you think it is faster / less fragmented / etc than the HeapAllocator you should performance test. Optimizations should always be based on real world data.

ReplyDeleteThanks for another great post, Niklas. Was thinking about memory allocators for my engine/game and now I have a solution.

ReplyDeleteNice post! Some thoughts/questions:




ReplyDelete1 - If your template methods (make_new, make_delete, etc) do not get inlined you will end up with extra functions for each object you have, what appears to be a waste of memory.

2 - Why don't you change your make_delete to receive a double pointer **T, and enforce the *T = 0 inside of the method?

3 - Using your TraceAllocator are you able to trace the file and line number of memory leaks?

1 - But wouldn't it waste even more memory if it did get inlined? The code has to be there one way or another. It's not a memory cost that I really worry about.



ReplyDelete2 - You could do that if you like to always have your pointers nulled after delete.

3 - Yes, by storing and keeping track of a stack trace for each allocation and then looking those traces upp in the PDB.

Actually STL was not very well thought through, it was a research project that was standardized in a very short amount of time. The ideas and principles of generic programming are very well thought through and very sane, STL is not :) Nor the C++ features that "supports" GP.


ReplyDeletehttp://en.wikipedia.org/wiki/Standard_Template_Library#History

Greedings a noob question: how do u handle deallocation of data.You just memset them to NULL

ReplyDeleteand defrag the rest of the data (reallocate everything)?Or data are never deleted and u work with an index scheme?

The deallocation scheme is up to the allocator. The heap allocator does normal heap deallocation, etc.


ReplyDeleteNone of the allocators I've talked about in the article are handle based and do automatic defragmentation. You could add such an allocator to the system, but it is kind of a separate topic.

Great post! It's helped me with a few details I was fuzzy on.



ReplyDeleteI have a couple of questions about your allocation tracking though. You mentioned above that you record the stack trace for each allocation. It seems you've decided not to use the __FILE__ and __LINE__ macros. I guess that would mean you'd have to wrap every allocation call with a macro to do it that way.

How are you recording the stack trace? Writing to an external file? It would seem that this sort of tracking would be a big hit on performance and isn't enabled during regular development, no?.

You are right, I don't use __FILE__ and __LINE__. The main reason is that they don't give enough information in many cases. For examples, all allocations in the Vector class would show up as vector.inl:72 or something like that, which doesn't give any information about what system is actually leaking memory.



ReplyDeleteI record the information in memory (as pointers, so it is just 4 bytes for each stack trace entry) using a special debug allocator. All debug allocations (profiler data, stack traces, etc) go through that allocator, so I always know how much memory is used for debugging and how much is used by the "real game" -- another advantage of the allocator system.

It is a hit on performance, so it is not enabled during regular development. When I use it, I usually enable it just for the particular allocator that I know is leaking, for example the "sound" allocator, if the shutdown test has shown that that allocator is leaking. That way the game runs at nearly full speed, since only a small percent of the total allocations are traced.

What if the concrete allocator must take some additional params? For example, the stack allocator may take additional argument on which side to allocate (when double ended). Then the code will need to know which allocator uses.

ReplyDeleteIn that case you could just create two different allocators that allocate from each end of the stack.

ReplyDeleteThis is a really nice post and it has been very helpful!



ReplyDeleteI just have a real noob question: You have disallowed the use of new and malloc() so how do you get your chunks of raw memory?

If you use byte arrays as above, how do you check that the allocation was successful and that you have not run out of memory? I mean there is no way for the program to report an error in allocating a static array, right?

I get memory directly from the OS. For example on Windows I use VirtualAlloc.

ReplyDeleteGreat post!! Just wondering how do you handle the main mem mapping for the RSX?

ReplyDeleteThanks for the great post, very interesting read. Couple of questions:



ReplyDelete1. How do you control internal STL allocations? You said you avoided creating custom STL allocators, but how do you ensure that any memory dynamically allocated inside the STL (Grow() etc) go through your allocators?

2. Do you have any recommended books/links on the types of allocators you've mentioned here (HeapAllocator, FrameAllocator, PageAllocator, PoolAllocator)?

@Jack







ReplyDelete1. We don't use STL. We use our own collector classes. They are quite similar to the STL classes, but they take a reference to an allocator interface in their constructors. They use that interface for all their memory allocations.

2. I've picked up information here and there. You should be able to find some pointers by just googling "memory allocations". Some more detailed information:

HeapAllocator - An allocator that allocates varied sized blocks and keeps an in-place linked list of free blocks. Look at dlmalloc, it is pretty much the standard allocator.

FrameAllocator - Also called "arena allocator" or "pointer bump allocator". An allocator that doesn't deallocate individual blocks but releases all its memory in one go. That means it has a super simple internal state (just a pointer to the next free byte and the remaining bytes of free memory).

PageAllocator - The virtual memory allocator provided by the system. Allocates memory as a number of "pages". The page size is OS dependent (typically something like 1K -- 64K). You don't want to use it for small allocations, but it can be used as a "backing allocator" for any of the other allocators. Google "virtual memory" and you should find lots of information.

PoolAllocator - An allocator that has pools for allocations of certain sizes. For example, one pool may only allocate 16 byte blocks. The pool can be packed tight in memory, you don't need headers and footers for the blocks, since they are always the same size. This saves memory and reduces fragmentation and allocation time.

Thanks for the info Niklas.


ReplyDeleteBeen powering through this blog for the last few days, some great posts and resources. Thanks for sharing!

Very interesting. Will definitely be using a similar approach on my next project.

ReplyDeleteNice article, I used it to build my own Allocator but I run into trouble with allocating arrays of objects. I made a helper method to my Allocator like the following:



ReplyDeletetemplate T *make_new_array(size_t length) {

return new (allocate(sizeof(T) * length, alignof(T))) T[length];

}

The problem with that is: If T has an destructor, placement new will write 'length' into the first 4 bytes and returns the allocated memory address offsetted by 4 bytes. This means it actually writes beyond the allocated buffer while initializing the objects. Furthermore I can't use the returned pointer to deallocate the memory again, since it is not the original one returned by the allocate method.

How did you solve this? Manually calling regular placement new on each element?

Thanks

Like Alexander solved the Gordian knot. I just don't use new[] and delete[]. I use a Vector<> instead.



ReplyDeleteOr sometimes (when I don't care about constructors, which is most of the time) a plain C array with the size kept externally, i.e.:

int len = 100;

int *a = allocate(sizeof(int) * len);

@Serge



ReplyDeleteFor the RSX mapped memory we first allocate a couple of MB from the PageAllocator for that region and map it with cellGcmMapMainMemory().

Then we create a HeapAllocator to service allocations of that memory. (Our heap allocator constructor can take a pointer and size to a memory area and will then construct the heap in that region.)

If you are using a templated "new" function you will run into the template forwarding problem at some point.




ReplyDeletehttp://www.open-std.org/jtc1/sc22/wg21/docs/papers/2002/n1385.htm

There's no nice way around it. In the past I've restricted parameters to value, const reference or pointers to work around it.

C++11 will fixes it.

True. We use both const and non-const argument references so we run into the 2^N combinatorial explosion. We have unrolled that to up to three arguments... if you need more than that you have to write placement new by hand, rather than using make_new.

ReplyDeleteI'm experimenting with this allocator strategy, rolling my own container and such.


ReplyDeleteI'm concerned by the global override of operator new/delete. While I understand that it's needed to ensure that everything is under control, by doing so we also forbid the use of any external library (or 99% of them) in their original state.

E.g. I use UnitTest++ and it does allocate using new.

Did you really don't use anything external ?

I humbly thank you for this blog and the time spent for knowledge sharing.

No, we don't use anything external that uses new() and delete(). We use some external stuff, but we only use stuff that let's us customize the memory allocation. That's the way it should be, I think. Any third party library intended for high performance use should let you supply your own memory allocators.

ReplyDeleteWow, I'm impressed ...

ReplyDeleteStill a long way to go, it seems ^^

Just for my curiosity, did you write a unit test library or did you pass on that ?

Very nice approach at all Niklas!

ReplyDeleteBut how have you implemented your HeapAllocator?

Are you simply using malloc()/free() internally or have you simply copied the full source from dlmalloc()? I'm asking because I don't see a reason why reinventing the wheel and not simply using malloc()/free() in this allocator?

We are using dlmalloc. Using that instead of standard malloc() free() means we have more insight into and control over how the heap allocator grabs system memory. So we can make sure that it "plays nice" with our other allocators and we can write functions that given a pointer can tell us if it was allocated by the heap or not.


ReplyDeleteIt also allows us to have multiple heaps. For example, we have a special heap just for debug allocations (such as profiler data) so that we can easily ignore them when we check if we are within the memory budget.

Thanks for this great explanation!

ReplyDeleteI think I will also try to wrap the dlmalloc() through template heap layers.

It's really nice to have such control over your memory budget!

I am still confused about how you handle arrays of objects. You say you use Vector<> (I assume that this is your own custom container) How does this allocate the necessary memory as well as call the constructors for each of the objects in the array?


ReplyDeleteAnd thank you so much for posting this!

It is no great mystery, memory allocated with (for example):




ReplyDeletedata = (T *)_allocator->allocate( sizeof(T) * capacity, alignof(T))

And then in-place new is used to call the constructors.

for (unsigned i=0; i<size; ++i)

new (data + i) T();

Are your allocators thread safe? If the answer is yes, what is your prefered method to achive that?

ReplyDeleteIt is up to each class implementing the Allocator interface. Most of our allocators are thread-safe, because that makes them easier and safer to use, but we have some special allocators that faster but not thread-safe.


ReplyDeleteIt is implemented with critical sections protecting the access to the shared data.

Nice article! I noticed your heap_allocator is using page_allocator as backend. my question is how page_allocator was implemented? Does it allocated a big chunk at the begin and give memory to heap_allocator when requested, and only VirtualFree the chunk in the end? Also did you also redirect dlmalloc's MMAP to the page_allocator?

ReplyDeleteNo, the page allocator, allocates pages as requested and returns them when done. It doesn't grab a big chunk at startup. It tries to be friendly to other processes/alloators that might be using the VM system at the same time.


ReplyDeleteYes for heaps that can grow, mmap() is redirected to the page allocator. (Actually, any allocator that supports the Allocator interface can be used as backing allocator.)

This is a very interesting article. Will definitely have to look into it further. Thanks for sharing.









ReplyDeleteThere is one thing i am thinking of adding to your suggestions though; adding an overload of the new operator that takes an allocator as a parameter.

void* operator new (std::size_t size, Allocator & a) throw (std::bad_alloc);

void operator delete (void* ptr, Allocator & a) throw ();

With assert of global new and proper handling of delete, i still get all of the benefits of allocator usage along with all of the syntactic sugar the new and delete keywords provide. Also alleviates the need for multiple template parameters make_new uses as the syntax is the same as it would have been except for:

HeapAllocator my_allocator;

MyClass* mc = new (my_allocator) MyClass();

Still enforces the allocator usage, and i can hide it internally if desired. Even if it wasn't hidden, someone using it would still incur correct behavior.

Still toying with the idea though. Since i allow placement new, doesn't seem too bad to allow this for my own internal usage, but will have to see if i will keep with that line of thought.

Now i just need to go research more about the actual implementations of the various types of allocators.

Yes, it has its advantages. The drawback is that you can't do the same for delete (no way of passing parameters), so you end up with different syntax for new and delete.

ReplyDeleteWhy no realloc() support for Allocator?

ReplyDeleteI think realloc() is kind of weird. It is a non-deterministic optimization. If you are really lucky and their happens to be some free space to the right of the memory buffer, then realloc() can be faster than alloc + copy + delete. But you can't really do anything to make sure that that happens.


ReplyDeleteSo you could easily add realloc support (with a default implementation of alloc + copy + delete for allocators that don't have a faster path). But to me it isn't that useful. I much prefer deterministic optimizations.

I get the determinism argument, but not sure if it is strong enough to out-weight benefits of successful realloc(). Also, I would not provide default realloc in terms of alloc+copy+del but rather return null from realloc() so that a+c+d would be a next explicit step so that it is always obvious if optimization happened or not.

DeleteIf I need a buffer that can grow without reallocating memory I use some other technique, such as a linked chain of fixed size buffers (perhaps 8K each) that I merge as a final step. That way I am sure I don't have to copy the data unnecessarily, regardless of what the memory system decides to do.

DeleteBut isn't that what Lea's allocator is doing already? I can see your point tho: you want to have full control always. Two more questions: 1) Do you use HeapCreate/Alloc on win to have different OS heaps for different systems/resources? 2) How do you handle dtor calling with allocators such as FrameAllocator where memory might be "freed" without client's explicit free() call? And sorry for not saying it with first comment: great read! :)

Delete1) No, I don't use OS heaps. All heap allocation is done by dlmalloc. I use the OS page allocator (VirtualAlloc) as a backing allocator for dlmalloc.


Delete2) If you "delete" an object in a FrameAllocator, the destructor will be called, but memory will not be freed (all memory is freed when the FrameAllocator is destroyed). When you destroy the FrameAllocator, all memory is released, but no destructors are called... So if you want destructors to be called you must call delete (the same as if you use any other allocator). With the frame allocator though, you can choose to *not* call delete, if you know that the destructor doesn't do anything useful. That should not be the normal code path though, it should be reserved for "special optimizations".

Hi Niklas, I see your heap allocator can take a pointer to a memory area and construct the heap in that region, you also said your heap allocator uses dlmalloc, how you managed to tell dlmalloc what memory region it should use?

ReplyDeleteI use create_mspace_with_base()

DeleteSince you just did: http://www.altdevblogaday.com/2012/05/05/embracing-dynamism


ReplyDeletewhat is your alloction strategy for Lua states?

We use a special allocator for Lua, so that we can track all Lua allocations (and optimize for Lua allocation patterns if needed).



DeleteWe use lightuserdata for most objects exported from C to Lua to minimize the load on the garbage collector.

We use an incremental garbage collector where we spend a certain ammount of time every frame to collect. We dynamically adapt the time we spend collecting to the ammount of garbage we generate so that the system settles down in a "steady state" with a fixed garbage collection time per frame and a fixed garbage memory overhead.

Could you give more details about how to get the deallocated size from the ptr?

ReplyDeleteIt is up to the allocator to track the size of the allocated areas. Each allocator does it differently.



DeleteFor example, dlmalloc adds some extra memory before each allocated memory block where it stores a header with that information.

A slot based allocator typically allocates slots one "chunk" at a time. In the chunk header it can then store information about the size of the slots in the chunk. If chunks are always say 8K big and aligned at 8K you can round down a slot pointer to the nearest 8K aligned address to get to the chunk header from the slot pointer, and then read the slot size from there.

I have been googlin around some about data alignment, and I'm curious of how you generally handle data alignment in the Bitsquid engine since it is multiplatform. Do you use alignas and alignof from the C++11 standar, or do you use some compiler specific methods?


ReplyDeleteAlso I'm interested of how you handle it in your allocators. if it's not to much to ask of you.

We use compiler specific attributes right now, such as __align.




ReplyDeleteAs seen above, our default allocate function takes a size and an alignment

void *allocate(size_t size, size_t align);

The alignment must be a power-of-two and <= size. The different allocators handle alignment as necessary. The simplest method is to just allocate extra memory and then offset the pointer to make sure that it has the right alignment. But most of our allocators are smarter than that. When they request a page from the system, and chop it up for allocation, they make sure that the blocks fall on reasonable alignment boundaries.

Theres something not clear to me about those headers/metadata allocated in this extra space, are they aligned themselves? In the game engine architecture book, for example, he just store an int in the previous 4 bytes from the aligned pointer...Thats not guarantee to be aligned. Isnt that a problem? Ppl dont care about allocator metadata alignment?

DeleteThanks for the post, it's always interesting to see how others do it!





ReplyDeleteI have one question regarding the deletion of instances using the templated make_delete(T *p) function, though.

If people use multiple inheritance and don't delete instances using a pointer-to-base, the pointer handed to make_delete() will be wrong because the derived-to-base-offset hasn't been accounted for.

I see two possibilities for handling this:

1) Disallow multiple inheritance

2) Tell users that they have to properly cast their pointers to base-pointers in cases of MI first

So, how do you handle this?

Thank you very much for this ineresting post.








ReplyDeleteI very much like the approach of orthogonalizing various aspects of the memory subsystem like linearization, stack traces, leak tracking and memory corruption.

However, I'm wondering:

1) How would you deal with private destructors?

2) Wouldn't it help compile-times to replace the make_new template functions with a single variadic macro?

I'm thinking of something along these lines:

#define make_new( allocator, T, ... )\

new ( (allocator)->allocate( sizeof(T), __alignof(T) ) ) T( __VA_ARGS__ )

What's your opinion?

@molecularmusings True. We don't use multiple inheritance so we don't run into this problem.

ReplyDelete@smocoder



ReplyDelete1) This doesn't work with private destructors, but regular new and delete wouldn't work in that case either. If you have a private destructor you typically have some other way of creating and destroying objects than using new/delete. In that case you would just make sure that that system worked with the allocator model.

2) Actually we have pretty much exactly that macro in our code base. And we are transitioning from using the templates to using the macro to improve compile-times and reduce object size, just as you suggest. Good point!

We use a macro-based approach in the Molecule Engine as well. It doesn't use variadic macros however, and looks somewhat similar to this:




Delete#define ME_NEW(type, arena) \ new ((arena)->Allocate(sizeof(type), ME_ALIGN_OF(type)) type

The lone "type" at the end ensures that you can just open another set of parentheses for providing constructor arguments, like so:

TestClass* tc = ME_NEW(TestClass, arena)(1, 2, 3);

This comment has been removed by the author.

DeleteHi there, great article! I just had a quick question about the allocators you use and how they are used with your container classes (in this article and the Foundation example you created).





ReplyDeleteI have been playing around with making my own Heap style allocator which allocates memory from a global pool/blob (just like in this example). I currently use an std::vector to track allocations which happen (a struct containing the the start and end address of an allocation). I use this to find and remove allocations, and detect where there are gaps in the memory blob to make new allocations if they'll fit. I realised I would like to not have to use std::vector and create my own Vector class in a similar style to the one you created in the Foundation example code, but I hit a problem. The Allocator needs a dynamic, resizing array to track allocations, but the dynamic resizing array needs an allocator itself when it is created, and that doesn't quite work as I have a sort of chicken/egg scenario. I could be completely miss understanding but from the example outlined above I assumed that you would not call new/malloc or delete/free at all (not quite sure what dlmalloc is I'm afraid). I guess what I am trying to ask is how do you track/store allocations that happen in your base allocator. I suppose I could use some sort of Scratch or Temp Allocator to hold the vector inside the Heap Allocator, but that seemed sort of messy and I was hoping there was a nicer solution. I thought I'd ask you in case I've got things horribly wrong and am barking up the wrong tree, I hope you understand what I'm prattling on about :)

Thanks!

Tom

I tend to not use traditional data structures (vectors, etc) in the implementation of the allocators, just because of this reason. It becomes tricky to keep track of what is happening if the process of allocating memory triggers a resize which triggers another memory allocation.




DeleteSo instead I use other techniques, such as chaining together blocks of memory in implicit linked lists, having "header blocks" in memory regions allocated from the backing allocator that stores information about the number and type of allocations. Perhaps also a "master header" block with global information, etc.

Dlmalloc can be found here http://g.oswego.edu/dl/html/malloc.html. You can see how it implements some of these techniques. You can find similar stuff in other memory allocators.

There are some other situations when the chicken-and-egg problem can crop-up, such as when creating the initial global allocators. I don't want to use static variables, since I want to have a clear initialization and destruction order. So instead I placement-new them into a statically allocated memory buffer (as you can see in memory.cpp in the foundation project).

Hi Niklas,







DeleteThank you very much for the response, that makes a lot of sense.

As a temporary solution (while I couldn't think of anything better) I used a simple linear allocator internal to the heap allocator which used a member variable char buffer in the heap allocator as it's memory. I set it to what seemed like an appropriate size and stuck an assert in to catch if ever it grew too large. The implicit linked list solution sounds like a nice solution, I will definitely check out Dlmalloc too.

Thank you again, the Foundation project has been incredibly interesting to poke around in, both in terms of the coding style and techniques.

Cheers!

Tom :)

This comment has been removed by the author.

ReplyDeleteHi Niklas,




ReplyDeleteJust to note that I reference this in my blog post here. I talk about applying this kind of allocator setup in the specific context of a custom STL style vector class, and also the addition of realloc() support.

Feedback welcome!

Thomas

Hi there, I tried to understand a few concepts that you've shared here.



ReplyDeleteYou have a PageAllocator (which in turn uses VirtualAlloc, mmap etc) as the top level allocator. How do you handle allocated_size() in this allocator? If you store it directly in the page you may need to allocate another page just to store this information. This way request of 4KB would need to be satisfied by allocation of 8KB of memory in 2 pages, just to store it's size and to align the space accordingly. Do you have a separate hash table inside the allocator just for the bookkeeping? Does PageAllocator even implement the Allocator interface?

As for the dlmalloc it uses only 2 global callbacks for allocating it's memory. How can you give it an allocator to allocate from? Did you modify it and pass your own callbacks and an Allocator pointer on creation, so it can allocate from it? By default, dlmalloc also coalesce adjacent segments and free them in one go (in one call to munmap()). How do you handle this behavior in your allocators?

On Windows you can use VirtualQuery() to get the size. But not all platforms provide a similar interface. On other platforms we have a hash table in the allocator for storing the size of page allocations. (As an optimization, we only store allocations > 1 page, if the page is not in the table the allocation size is assumed to be 1 page.)


ReplyDeleteYes, we have modified dlmalloc so that it uses a PageAllocator instead of mmap to allocate system memory.

Thanks for the reply!


DeleteWhat about the coalesced pages in dlmalloc? Did you turn them off as well or did you made PageAllocator to support that?

As far as I remember, I haven't done either. I use the mspace interface and provide my own versions of mmap and munmap to dlmalloc.

DeleteExcellent article with lots of useful information, many thanks.


ReplyDeleteYour method of explaining in the blog that’s superb I have no words to praise your blog.


ReplyDeletecustom base wrap

custom pool table lamps

Machine Learning is an in-depth region of AI focused within the design and creation of an algorithm which identifies and finds patterns that exist in data provided as input. This innovation will set a replacement approach of managing and regulating organizations or a further , especially companies.

ReplyDeletemachine learning course in pune

I've really been vanished just for some time, still at this time I recall as to why Document which is used to absolutely love this approach website. สล็อตออนไลน์


ReplyDeleteเว็บไซต์แห่งความสนุก BETFLIX ให้บริการเกมสล็อตออนไลน์ อย่าง BETFLIX พีจีสล็อต เว็บใหญ่ ที่มี ทางเข้าpg slot auto มือถือ และ รวมทุกค่ายผู้ให้บริการสล็อตออนไลน์ครบวงจร ในขณะนี้ เกมทำเงินผ่านมือถือ สล็อต pg เว็บตรง ไม่ผ่านเอเย่นต์ มีโปรโมชั่น ที่ยอดเยี่ยม โปรสล็อตสุดพิเศษ มากมายรองรับผู้เล่นทั้งเก่าและผู้เล่นใหม่เพียง ท่านเป็น สมาชิก กับเว็บ BETFLIX PG เล่นผ่านมือถือ


ReplyDeleteเกมส์สล็อตออนไลน์ PG SLOT เครดิตฟรี MEGA GAME เกมสล็อตที่ได้รับความนิยมจากผู้เล่นทั่วโลกในตอนนี้ การเล่นสล็อตของเพื่อนๆสมาชิกทุกท่านจะไม่น่าเบื่ออีกต่อไปด้วยความพิเศษของ ทางเข้า pgslot มือถือ ที่มีรูปแบบที่เล่นง่าย แจ็คพอตของ MEGA GAME แตกง่ายแตกบ่อยที่สุด ด้วยเว็บไซต์ของเรา MEGAGAME168.CO ในการเล่นสล็อตสามารถเล่นได้

การเล่นพนันonline ไม่ผ่าน Agent เว็บไซต์ MEGA GAME เว็บตรง 2022 เป็นการเลือกเล่นอีกแบบอย่าง ที่นิยมเป็นอย่างมาก ที่สุดในขณะนี้ betflix เพราะว่านอกเหนือจาก นักเสี่ยงโชคจะได้เพลิดเพลินใจ ไปกับการพนัน และการเลือกเล่นใน เว็บไซต์ casino online ที่ครบวงจรได้เงินจริงๆแล้ว betflik สามารถเล่นเกม website ตรงไม่ผ่าน Agent ที่ไม่มีอันตราย รวมทั้งสร้างความเชื่อมั่น และมั่นใจให้กับ นักเสี่ยงโชคผู้เล่น ได้มากกว่าการเล่น ผ่าน Agent พนัน ออนไลน์ เว็บตรง

ReplyDeleteวันนี้ MEGA GAME จะมาบอกสูตรเด็ด PG SLOT ในการเล่นสล็อตออนไลน์ หากเป็นนักเสี่ยงโชค ผู้เล่นมือใหม่ ก็ต้องไม่พลาด ที่จะมองหา betflix วิธีใช้สูตรเล่นสล็อต PGSLOT เนื่องจากอาจจะ ยังไม่ทราบ แนวทางว่า สูตรชนะ เกมpg slot สล็อต ที่เราเห็นกันนี้ มีวิธีการใช้อย่างไร ดังนั้น เราจึงได้นำเอา วิธีการใช้สูตเล่นสล็อตที่ดี มาบอกต่อ นักเสี่ยงโชคผู้เล่น betflik มือใหม่ทุกคน เพื่อที่จะสามารถเข้าไปเดิมพัน กับเกมสล็อต และทำกำไร ได้ตามที่ต้องการ

ReplyDeleteMEGA GAME ทางเว็บของเรามีเคล็ดลับหารายได้จากการเล่นสล็อตทุกค่ายมาแนะนำให้ท่านได้เรียนรู้ และสนุกไปด้วยกันอีกมากมาย ในตอนนี้การหารายได้ออนไลน์มีหลากหลายรูปแบบ เล่นสล็อต MEGA GAME ไม่ว่าจะมาจากวิธีขายผลิตภัณฑ์เสริมของเกม MEGA GAME หรือไม่ PGSLOT ก็การขายของได้เงินจริง เกี่ยวกับบนสิ่งออนไลน์ แต่ว่าไม่ว่าจะอะไรก็แล้วแต่อย่างไรก็ตามบางครั้งก็อาจจะจำต้องใข้ทุนที่สูงมากมาย ๆ

ReplyDeleteต้องขอทักทาย ผู้ที่ชื่นชอบในเกม พนันกีฬาออนไลน์ ทุก ๆ ท่านนะค่ะ และ แน่นอน การที่คุณคลิกมา อยู่ในหน้าบทความนี้ ของเว็บ betflix นั้นหมายความว่า คุณกำลังให้ความสนใจ ในการเล่นพนัน เกมกีฬาที่คุณชื่นชอบ หลายคนอาจจะทราบว่า ต้องการเล่นพนันกีฬา ประเภทไหน แต่หลายคนยังไม่ทราบ เราขอแนะนำ ให้สำหรับคนที่ยัง ไม่แน่ใจใน

ReplyDeleteเว็บ MEGAGAME บอกต่อทริกและเทคนิคในการ เล่นคาสิโนออนไลน์ เป็นที่นิยม มากขึ้นกว่าเดิม แต่ก็มีนักเสี่ยงโชคบางคน ที่ยังไม่กล้าที่จะเล่น ด้วยเหตุนี้ในหลาย ๆ เพราะสาเหตุที่ว่า ความคิดในการ เดิมพันออนไลน์ เกม PG SLOT อาจเป็นเรื่องที่น่ากลัวอยู่บ้าง เข้าใจได้ อย่างสมบูรณ์แบบ แต่การอยู่อย่างปลอดภัย betflix และมีช่วงเวลาเล่นเกมออนไลน์ ที่ดีนั้นค่อนข้างตรงไปตรงมา ลองมาดู เคล็ดลับ และเทคนิคสำหรับ นักเสี่ยงโชค ผู้เริ่มต้น คาสิโนออนไลน์ ต้องเลือกเล่นคาสิโนออนไลน์ที่น่าเชื่อถือก่อนอื่น นักเสี่ยงโชค ต้องเลือกเล่นคาสิโนออนไลน์ ที่น่าเชื่อถือ ซึ่งได้รับใบอนุญาต และครอบบคุมอย่างสมบูรณ์ ตรวจสอบสถานะ คำแนะนำ ของนักเสี่ยงโชค ให้มากที่สุด เท่าที่จำเป็น เพื่อให้มั่นใจว่า เชื่อถือได้ หากมีข้อสงสัย มีการเดิมพันที่ปลอดภัย กว่ามากมาย ดังนั้นจึงไม่คุ้มที่จะเสี่ยง

ReplyDeletebetflixเข้าสู่ห้วงจักรวาลที่ไม่มีใครรู้จัก กลาง Galaxyที่กว้างใหญ่ มีหีบสมบัติลึกลับ จากดวงดาว STAR HUNTER เกมยิงปลา โหมดต่อสู้ที่ดีที่สุดสำหรับคุณ ในการยิงแต่ละครั้ง ปืนใหญ่ไฟฟ้า พร้อมฟีเจอร์เด็ดๆ อาวุธใหม่ๆเพียบพร้อม สำหรับการล่าสมบัติ ที่ทำให้ผู้เล่น ได้รับประสบการณ์ในการเล่นที่ดี เล่นเกมได้เงินจริง


ReplyDeletebetflixเกมสล็อต ออนไลน์ ของเว็บไซด์ Betflix จากค่ายBetsoft ถือเป็นผู้ ออกแบบเกม ที่ดีที่สุดอีกค่าย ซึ่งเป็นที่รู้จักอย่างแพร่หลายไปทั่วโลก ด้วยการดีไซด์ภาพกราฟิก และ ตัวเกมที่ถูกออกแบบขึ้นมา สวยงามเป็นที่ ถูกอกถูกใจผู้เล่นเป็น อย่างมากเกมสล็อตเว็บตรง ทางค่าย Betsoft Slots ยังมีเกมมากมาย ที่ได้รับความนิยม ที่มีทีมงานคุณภาพที่


ReplyDeleteMEGA GAME ถ้าผู้เล่นท่านไหน ที่ไม่ชอบการเล่นเกมที่ยุ่งยากเหมือแต่ก่อน ทาง แอพสล็อตเว็บตรง จะสามารถตอบโจทย์ผู้เล่นได้เป็นอย่างดีและแน่นอนลว่า ต้องมีคุณภาพที่สุด เพราะในทุกวันนี้ทางเราได้มีเทคโนโลยีเกิดขึ้นมา ก็มีความก้าวหน้าเป็นอย่างมาก MEGA GAME เช่นกัน และผู้เล่นนั้นไม่จำเป็นจะต้องกังวลในเรื่องความล่าช้าในการเดิมพัน เพราะทุกวันนี้อะไร ๆ ก็ได้เปลี่ยนไปค่อนข้างเยอะแล้ว ดังนั้นการเดิมพันเกมต่าง ๆ ไม่ว่าจะเป็นเกมสล็อต หรือเกมอื่นก็สามารถทำเงินได้

ReplyDeleteBETFLIX สำหรับผู้เล่น ที่ต้องการ เล่นบาคาร่าให้ได้เงิน มักจะมี คำถามว่าจะต้องเล่น อย่างไรถึงจะ มีโอกาสทำเงิน ได้มากกว่าเสีย บอกได้เลยว่าไม่ยากเลยเพราะในวันนี้ BETFLIX จะมา สอนเล่นบาคาร่า ที่จะทำให้ ผู้เล่นมีโอกาส ทำเงินได้ง่ายขึ้น กว่าการเล่นด้วยตัวเอง เรารับประกัน ได้ว่า ถ้าหากนำเทคนิค ไปใช้อย่างเหมาะสม ก็จะสามารถทำเงินได้ตาม ที่ผู้เล่นตั้งใจ

ReplyDeletebetflixโปรโมชั่นใหม่ BETFLIX โคตรโดนใจสายฟรี ที่กำลังตามหา โปรสล็อต เกมสล็อตฟรีได้เงินจริง ได้เงินจริง ไม่ต้องลงทุนแบบแจกกันของแท้ ปั่นสล็อตฟรี ได้เงินจริง ไม่มีโม้เกมปั่นสล็อต ได้เงินจริงไม่ต้องฝาก สล็อต ทดลองเล่นฟรี ถอนได้ เข้าก่อนสักบาทเดียว เล่นได้ ถอนไปเลย คุ้มสุดๆ ไม่มีที่ไหนอีกแล้วที่เรา MEGA GAME ลืมทุกโปร จากทุกเว็บที่นักเสี่ยงโชคเคยเล่นมาให้หมด สล็อตได้เงินจริง เข้าบัญชีจริง เพราะที่นี่เราแจกเครดิตฟรี แบบจุใจ


ReplyDeleteMEGA GAME เกมสล็อตออนไลน์ เป็นเกมที่ได้รับความนิยม เป็นอย่างมาก ซึ่งการลงทุนเล่น สล็อตเล่นง่ายแตกไว ทั้งสนุกสนาน เล่นง่ายเพลินมีความสุข สร้างราย ได้ให้กับผู้เล่นได้จริง ในสมัยนี้ผ้เล่นทุกคน สามารถเข้าถึงการลงทุนเล่นเกมสล็อตได้กันทุก ๆ คนไม่ว่าจะเป็นผู้เล่นคนไทย หรือชาวต่างชาติ เพียงแค่สมัครเว็บ ไซต์ ที่เปิดให้บริการไม่กี่ขั้นตอนผ้เล่นก็เริ่มต้นลงทุนกับเกม ตัวต่อรายได้ในทันที โดยการเข้าใช้บริการบนเว็บไซต์สามารถทำได้โดย ง่ายเล่นได้ทุกที่ทุกเวลา ไม่ว่าจะอยู่ที่ใดก็ร่วมสนุก ตื่นเต้นและคลายเครียดจากการเดิมพันเกมสล็อตออนไลน์ได้ตลอดสล็อต เล่นง่าย แตกไว MEGA GAME ที่สุดสล็อต แตกง่าย แตกบ่อย กลายเป็นสิ่งที่นักพนันทั้งหลายต่างก็ชื่นชอบ และ ถูกอกถูกใจกับเกมของทางเว็บของเราเพราะนอกจาก จะได้ เล่นเกมสล็อต เพื่อความสนุก สนานยังสามารถทำกำไรได้จากการลงทุนเล่นซึ่งกำไรนั้น การเล่นเกมออนไลน์ของทางเว็บของเรานั้น จะให้ ผู้เล่นสามารถ เลือกเกมที่จะเล่นได้อย่างบตามใจของผู้เล่นเลย ชอบผู้เล่นสามารถทดลองเล่นได้ก่อนเดิม พันจริง และ สามารถเล่นได้แบบไม่มีการกำหนดขั้นต่ำ

ReplyDeleteผู้เล่นจะได้พบกับเกม คาสิโน ออนไลน์ สล็อต ได้เงินจริง ตลอดทั้งวัน โดยที่ไม่ต้อง ไปที่ไหนไกล วันนี้ เราได้รวบรวมเกม เดิมพัน ได้ครบทุกประเภท ไม่ว่าจะเป็น คาสิโนสด สล็อต แบล็คแจ็ค ไฮโล บาคาร่าออนไลน์ บาคาร่า รูเล็ต ยิงปลา เสือมังกร และเว็บ พนัน คา สิ โน ups เว็บพนันคาสิโน อื่นๆ อีกมากมายในรีวิว คาสิโนออนไลน์ MEGA GAME นี้ทางเรา ได้

ReplyDeleteBETFLIX วันนี้เราจะพาผู้เดิมพัน มาพบกับเว็บเกมสล็อต BETFLIX ส่งมาจากค่ายยักษ์ใหญ่ ทั่วอาณาจักรถูกรวมไว้อยู่ในที่เดียว เต็มไปด้วยเกมสล็อต ทุกเกมทุกค่าย ที่มีให้เล่นเยอะที่สุด ตั้งแต่ที่เคยมีมา พร้อมลุ้นรับเงินรางวัลแจ็คพอตได้ในทุกวินาที อีกทั้งยังมีระบบการเล่นที่ล้ำสมัย สมัครสมาชิก และ ทำธุรกรรมการเงิน ฝาก-ถอน ได้ด้วยตัวเองผ่านระบบอัตโนมัติทุก 24 ชั่วโมง สำหรับใครที่กำลังตามหาเว็บเล่นสล็อตที่ ครอบคลุมมากที่สุด สล็อตเว็บตรง megagame แตกง่าย 2022 เท่านั้น รับประกันในเรื่องของความปลอดภัย สล็อตเว็บใหญ่ที่สุด 2022 เป็นเว็บตรง ไม่ผ่านตัวแทนส่งตรง จากค่ายชั้นนำโดยตรง mega game

ReplyDeletebetflixเมื่อพูดถึง แหล่งรวมเกมที่มีเกม ให้คุณได้เข้า ใช้บริการมาก ที่สุดในเอเชีย BETFLIX เว็บตรง100% คาสิโนเว็บใหญ่ ที่ครบเครื่องที่สุด และมีเกมต่างๆ ให้คุณได้เข้าเล่นมากถึง 20 ค่ายใหญ่ รวมหนึ่งพันกว่าเกม และด้วยระบบเกม ที่มีความเสถียรที่สุด ที่เราได้อัพเดท และภูมิใจนำเสนอ ให้กับเหล่าสมาชิกทุกคน ได้เข้าเล่น ระบบเกมและการบริการที่ดีที่สุด ซึ่ง คาสิโนออนไลน์เว็บตรง ที่ได้ทำการ พัฒนาและอัพเดทเกมใหม่ๆ


ReplyDeleteMEGA GAME ในตอนนี้ทางค่ายเกมสล็อตของเรานั้น รีวิวสล็อต JOKER ได้ทำการรวบรวเกมสล็อตจากทางค่าย Joker Slot มาโดยตรง สล็อต ให้ผู้เล่นมารู้จักกับเกมที่มาในรูปแบบใหม่ที่สุด หรือใหม่ล่าสุดนั่นเอง เป็นเกมที่ทันสมัยมากๆ MEGA GAME และเป็นเกมที่แตกบ่อย แตกจริง ได้เงินจริง หรือว่ากันว่า ทุกท่านที่เข้ามาเล่นนั้น ไม่ควรที่จะพลาดโอกาสดีๆ ที่ทางค่ายเราจะมามอบให้ทุกท่านโดยเด็ดขาด และให้ทุกท่านมารู้จัก


ReplyDeleteเกมสล็อตมาเก๊าสิ่งที่ใฝ่ฝันของเกม Dream Of Macau ในหลาย ๆ คนที่มีความต้องการเต็มที่ไปด้วยการเล่นพนัน สล็อต และบาคาร่าที่เป็นชั้นนำของประเทศ ในเวลาตอนดึก ๆ ก็จะมีแสงสว่างไปด้วยแสงไฟส่องลงมามากมาย MEGA GAME ตามหา diamond ที่มาเก๊าได้แล้วตอนนี้ ได้มาทดลองเล่น SLOT ฟรี 2022 Macauกับเรือที่แสนสวย Dreams of

ReplyDeleteBETFLIX วันนี้ทางเรา BETFLIX จะขอมาแนะนำเกมสล็อต ที่มาในรูปแบบ ไพ่ป๊อกเด้ง ไพ่ผสมสิบ หรือไพ่เสือมังกร เป็นชื่อไพ่ที่คนส่วนมากนิยม และ ได้รับเสียงตอบรับในไทย แต่ไพ่นกกระจอก Mahjong Ways 2 ฟังจากชื่อ คงไม่ค่อยคุ้นเคยกับคนไทยมากนัก ซึ่งภาคนี้เป็นภาคที่2แล้ว ด้วยกระตอบรับเป็นอย่างดีจากภาคที่1 สามารถลุ้นเงินรางวัลได้อีกเยอะ แค่ฟังอาจจะน่าสนใจแต่เราจะรู้ได้ยังไงว่าสนุกไหมต้องไปลองเล่นดู megagame ในเกมเลย สล็อตออนไลน์ Mahjong Ways 2 PG รูปแบบใหม่ ชักนำเอาไพ่นกกระจอกมา เพื่อทำให้ผู้เดิมพันเข้าใจถึงไพ่นกกระจอกมากขึ้น ตัวเกมที่รูปแบบแตกต่างจากภาค1 เล็กน้อย โดยสัญลักษณ์ที่มีเงินรางวัลสูงสุดคือ เครื่องหมายไพ่ นกกระจอกสีแดง และ ลดไปตามความเล็กใหญ่ ของไพ่นกกระจอก mega game

ReplyDeleteสล็อต แนะนำ เกมสล็อต ค่าย pg เว็บตรง MEGA GAME นำเสนอเกมสล็อตที่โด่งดัง ไปทั่วทั้งโลก จากค่ายยักษ์ใหญ่ ที่ถูกพูดถึงอย่างมาก ในเวลานี้ มาพร้อม กับอัตราการ แจกแจ็คพอตให้ผู้เล่นได้ลุ้นกัน ในทุกเสี้ยววินาทีที่ กดหมุนสปิน สนุกไปกับ เกมสล็อตเกรด พรีเมี่ยม ที่มีแนวเกม สุดอลังการ สนุกสุดมันส์ แบบจัดเต็มทุกแนวเกม ที่ถูกออกแบบ มาอย่างไม่มีซ้ำ


ReplyDeleteThank you so much, nice to see such a post to write such a beautiful post.

ReplyDeleteigoal แทงบอล

principle of your idea it makes you perfect and i like this idea. ดาวน์โหลด wm casino

ReplyDeleteLiverpool may be without a veteran engine room until the middle of next month. ทรรศนะบอล

ReplyDeleteNice writing....Thanks for sharing.

ReplyDeleteMachine learning classes in Pune

Wow It is a great contents that I ever seen. ผลบอลสดเมื่อคืน

ReplyDeleteWow It is a great contents that I ever seen. วิเคราะห์บอลไทย

ReplyDeleteAtletico Madrid are worried Chelsea won't buy Felix in the summer. ผลบอลสด

ReplyDeleteThe post-World Cup bounce behind Atletico's revival. ผลบอลสด

ReplyDeletePep says Phillips is not 100 per cent and needs more rotation.

ReplyDeleteวิเคราะห์บอลเจลีก

Leed's survival hopes dealt blow by Fulham. วิเคราะห์บอลเจลีก

ReplyDeleteWow It is a great contents that I ever seen. วิเคราะห์บอลเจลีก

ReplyDeleteVlahovic scores an unlocked goal but is not happy enough. วิเคราะห์บอลเจลีก

ReplyDeleteRyan Mason insists there is no way to do what Klopp does. วิเคราะห์บอลเจลีก

ReplyDeletePhilips must 'convince' himself of Man City future. วิเคราะห์เจลีก

ReplyDeletePSG's Messi apologises for unauthorised Saudi trip. วิเคราะห์เจลีก

ReplyDeleteIf West Ham sell Rice for £100m, they won't be interested in swap players.

ReplyDeleteวิเคราะห์บอลเจลีก

De Bruyne stunner earns draw for Man City at Real. วิเคราะห์เจลีก

ReplyDeleteBarcelona willing to spend money and players in exchange for Neves. วิเคราะห์บอลเจลีก

ReplyDeleteThe Football Association issued a statement apologizing for the chaos in the SEA Games finals. วิเคราะห์บาสNBA

ReplyDeleteNewcastle win to move closer to Champions League. วิเคราะห์บาสNBA

ReplyDeleteThis comment has been removed by the author.

ReplyDeletepost from you my monitoring web.

ReplyDeleteข่าวด่วน

from you my monitoring web.วิธีดูแลกระเป๋าหนังแบรนด์เนม

ReplyDeleteWe consider some thing genuinely interesting regarding your own.ข่าวไอที

ReplyDeleteI was able to find good info from your blog posts.

ReplyDeleteข่าวด่วน

you my monitoring web.กระเป๋าผู้ชายหลุยส์วิตตอง

ReplyDeletething genuinely interesting regarding your own

ReplyDeleteข่าววงการไอที

you my mon Chelsea about Lukaku loan extension.7 กระเป๋าแบรนด์ที่ขายดีที่สุดตลอดกาล

ReplyDeleteChelsea about Lukaku loan extension.Marvel’s Spider Man 2

ReplyDeleteWhen discussing custom memory allocation in C++, one might think of optimizing performance much like choosing the perfect jacket for an occasion. Just as the red one jackets stand out for their vibrant appeal, effective memory management enhances the clarity and efficiency of your code, ensuring it performs at its best.








ReplyDeleteUnleash your dark side with the Tate Langdon Sweater . Eye-catching, stylish, and ultra-comfortable, it’s crafted for trendsetters who aren’t afraid to express themselves. Turn casual outfits into bold fashion statements with this one-of-a-kind sweater.

ReplyDeleteThe best tom cruise bomber jacket are the ones that make you happy. And our effort is to provide you with the best jackets. So visit our site now.

ReplyDelete3 Piece Biker Patch Custom Designs | Rush Patch Motorcycle Club Patches.



ReplyDeleteLooking for a high-quality 3 Piece Biker Patch for your riding group or club? At Rush Patch, we specialize in custom embroidered patches designed specifically for motorcycle clubs across the USA. Our premium patches are crafted with durable stitching, bold colors, and detailed artwork to create the perfect 3 piece motorcycle club patch set for jackets, vests, and riding gear. A motorcycle club 3 piece patch traditionally includes a top rocker, center emblem, and bottom rocker each representing the identity and territory of a motorcycle club. If you’ve ever wondered what does a 3 piece motorcycle patch mean or what is a 3 patch motorcycle club, it refers to a structured piece patch motorcycle club design used by established riding groups. rush patch dot com creates custom piece biker patch and piece mc patch designs tailored to your club’s logo, colors, and style. Whether you represent a new piece motorcycle club, a traditional motorcycle club, or are simply exploring piece mc patch meaning, our expert team can help bring your vision to life. From small club orders to bulk production, Rush Patch delivers durable craftsmanship and professional quality making it easy for clubs to proudly wear their custom 3 Piece Biker Patch on every ride.

Visit our website. https://rushpatch.com/blogs/news/3-piece-biker-patch-a-dream-for-passionate-rider

Great insights shared in this post. Preparation for

ReplyDeletesap-c02 dumpsbecomes more manageable with structured practice. Certification-Exam helps you stay on track and improve your understanding of important topics.