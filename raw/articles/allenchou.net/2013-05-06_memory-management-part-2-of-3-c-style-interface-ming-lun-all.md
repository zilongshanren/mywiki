---
title: 'Memory Management part 2 of 3: C-Style Interface | Ming-Lun "Allen" Chou |
  周明倫'
url: https://allenchou.net/2013/05/memory-management-part-2-of-3-c-style-interface/
author: Allen Chou
published: '2013-05-06'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Memory Management Series](http://allenchou.net/memory-management-series/).

In [part 1 of this series I showed how to implement a memory allocator that allocates fix-sized pages and blocks. Part 2 is going to cover how to implement a C-style interface like ](http://allenchou.net/2013/05/memory-management-part-1-of-3-the-allocator/)`malloc`

and `free`

that can deal with variable-sized memory allocation using this allocator. In the end, I’ll also show a way to add syntactic sugar by creating C++ function templates.

### The C-Style Interface

So far, our allocator can only allocate fix-sized pages and blocks. Therefore, we need at least one individual allocator object for one specific block size. So how are we going to deal with variable-sized memory allocation? Well, we are not going to modify the allocator. Instead, we’re going to have a collection of allocators that allocate a wide range of different-sized memory blocks, and we will also build a look-up table to efficiently determine which allocator to use based on the memory block size requested by the client. This look-up table approach was inspired by a [Randy Gaul](http://cecilsunkure.blogspot.com/), one of my classmates at [DigiPen](https://www.digipen.edu/). You can check out his implementation here: [header](https://github.com/RandyGaul/ReflectionLib/blob/master/src/containers/BlockAllocator.h) / [source](https://github.com/RandyGaul/ReflectionLib/blob/master/src/containers/BlockAllocator.cpp).

This is the interface we will be implementing:


// allocates variable-sized memory blocks void *Allocate(unsigned size); // frees variable-sized memory blocks void Free(void *p, unsigned size);

And the client code uses this interface like this. Note the use of C-style casts.

// allocate memory unsigned *i = (unsigned *) Allocate(sizeof(unsigned); // manipulate memory *i = 0u; // free memory Free(i, sizeof(unsigned));

### Block Size Look-Up Table

In order to build the look-up table for different block sizes, we need an array of different block sizes. This information is something the client doesn’t need to know, and is local to the translation unit (i.e. the source file), so we’re going to use static data. The choice of block sizes depends on your application.

// sorted from smallest to largest static const unsigned k_blockSizes[] = { // 4-increments 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, // 32-increments 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, // 64-increments 704, 768, 832, 896, 960, 1024 };

Here I use the prefix `k_`

to denote constant data; on the other hand, the prefix `s_`

is used for static non-constant data. I picked up this naming convention recently, and I like it because it is Intellisense friendly: in Visual Studio, I can type the prefix to quickly filter out unwanted code hints.

Several extra constants are defined to aid the allocator initialization:

static const unsigned k_pageSize = 8192; static const unsigned k_alignment = 4; // number of elements in the block size array static const unsigned k_numBlockSizes = sizeof(k_blockSizes) / sizeof(k_blockSizes[0]); // largest valid block size static const unsigned k_maxBlockSize = k_blockSizes[k_numBlockSizes - 1];

Next, we store the look-up table as a static array, and we create a static array of allocators corresponding to the block size array:

static unsigned *s_blockSizeLookup = nullptr; static Allocator s_allocators[k_numBlockSizes];

### The Look-Up Helper Function

We can now implement a helper function for looking up the appropriate allocator with a requested data size. The allocator returned by this function is the one that allocates the smallest block size that is no less than the requested data size. Since this function is also for internal use only, we declare it as static. If the requested data size is too large, we fall back to using `malloc`

. You can of course choose to dynamically create allocators to handle larger data sizes, but here I just want to keep things simple and easier to manage.

static Allocator *LookUpAllocator(unsigned size) { // one-time initialization static bool s_initialized = false; if (!s_initialized) { // initialize block size lookup s_blockSizeLookup = new unsigned[k_maxBlockSize + 1]; unsigned j = 0; for (unsigned i = 0; i <= k_maxBlockSize; ++i) { if (i > k_blockSizes[j]) ++j; s_blockSizeLookup[i] = j; } // initialize allocators for (unsigned i = 0; i < k_numBlockSizes; ++i) { s_allocators[i].Reset (k_blockSizes[i], k_pageSize, k_alignment); } s_initialized = true; } // check eligibility for lookup if (size <= k_maxBlockSize) return s_allocators + s_blockSizeLookup[size]; else return nullptr; }

### The `Allocate`

& `Free`

Functions

Finally, the `Allocate`

and `Free`

functions are as simple as calling `LookUpAllocator`

to retrieve the proper allocator or falling back to `malloc`

and `free`

if the requested data size is too large.

void *Allocate(unsigned size) { Allocator *alloc = LookupAllocator(size); if (alloc) return alloc->Allocate(); else return std::malloc(size); } void Free(void *p, unsigned size) { Allocator *alloc = LookupAllocator(size); if (alloc) alloc->Free(p); else std::free(p); }

### Syntactic Sugar

The `Allocate`

and `Free`

functions still use `void`

pointers. Also, a data size is required by the `Free`

function. Woudn’t it be nice if we don’t have to perform type casts and provide type sizes in the client code? Here I’m going to show one way to achieve such syntactic sugar by creating function templates.

This is what we’d expect:

// allocate memory unsigned *i = New<unsigned>(); // manipulate memory *i = 0u; // free memory Delete(i);

We can always choose to overload the `new`

and `delete`

operators so that existing client code is not affected. But I’m just going to go ahead to show the function template approach, and you may base the overloaded operators on top of that.

The `New`

function templates uses the **placement new** operator and passes the correct data size using the `sizeof`

operator to the `Allocate`

function. Without C++ 11, you’ll need multiple templates for different number of constructor arguments. With C++ 11, you can just have one variadic template.

// 0 argument template <typename T> T *New(void) { return new (Allocate(sizeof(T))) T(); } // 1 argument template <typename T, typename A0> T *New(A0 a0) { return new (Allocate(sizeof(T))) T(a0); } // 2 arguments template <typename T, typename A0, typename A1> T *New(A0 a0, A1 a1) { return new (Allocate(sizeof(T))) T(a0, a1); } // ...and so on

The function template for `Delete`

invokes the destructor based on the type of pointers passed in, and then forward the pointer to the `Free`

function.

template <typename T> void Delete(T *p) { reinterpret_cast<T *>(p)->~T(); Free(p, sizeof(T)); }

### Done!

This concludes the second part of this series. See you in [part 3](http://allenchou.net/2013/05/memory-management-part-3-of-3-stl-compatible-allocators/) 🙂