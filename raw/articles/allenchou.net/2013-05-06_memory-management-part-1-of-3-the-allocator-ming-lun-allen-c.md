---
title: 'Memory Management part 1 of 3: The Allocator | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2013/05/memory-management-part-1-of-3-the-allocator/
author: Allen Chou
published: '2013-05-06'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Memory Management Series](http://allenchou.net/memory-management-series/).

### Why Bother Building Your Own Memory Management System?

Memory management is crucial for game development. It is even more important for console game development, since consoles have hard memory limits. Many game developers rely on garbage collectors that come with some programming languages. As convenient as garbage collectors are, their behavior is not consistent and not always reliable. Perhaps one out of a hundred garbage collection cycle, the garbage collector needs to do a big clean up, so it drags a couple of frames down to 10fps. Very likely, you cannot foresee this performance hit; you game runs smoothly most of the time, but every now and then there’s a little lag. It’s playable, and the players might be fine with the sporadic lags; however, in order to perfect the player’s overall experience, you should aim for eliminating every possible performance hit.

Building your own memory management system is one improvement you can do.

In order to build a custom memory management system, a language that allows raw memory access is needed. Languages that come with built-in garbage collectors and do not allow low-level memory access are out of the question. Lots of PC games and most console games are developed in C++, and that is what I’m going to use here.

Part 1 of this series is going to cover the fix-sized memory allocator, the foundation the rest of the series is built upon. In [part 2](http://allenchou.net/2013/05/memory-management-part-2-of-3-c-style-interface/), I will show how to use the allocator to implement a C-style interface that supports variable-sized memory allocation, as well as create C++ function templates for syntactic sugar. Finally, [part 3](http://allenchou.net/2013/05/memory-management-part-3-of-3-stl-compatible-allocators/) is going to cover an allocator implementation that is compatible with STL containers.


### The Big Picture: Using `new/delete`

Is Not Good Enough

If you’re writing your game in C++, you are already using the built-in `new`

and `delete`

operators to manage dynamic game data. However, this is not good enough. Every allocation (`new`

) and deallocation (`delete`

) call has its overhead, since the default memory manager (the implementation is compiler-dependent) needs to scan the available memory to look for a fit block. The fix-sized allocator we’re going to build takes constant-time to allocate a memory block; there is no need to scan for a fit when every block is of the same size. As [part 2](https://allenchou.net/allenchou.net/2013/05/memory-management-part-2-of-3-c-style-interface/) will show, even with a variable-sized allocator interface, constant-time can be achieved by using a pre-calculated look-up table.

To speed up the allocation and deallocation process, we will use the `new`

operator to pre-allocate big chunks of raw memory (big `char`

arrays), and manage these memory chunks on our own. This approach has several advantages:

- The use of
`new`

and`delete`

is greatly reduced. Way less system call overhead. - We own all the memory chunks, so we can easily insert extra data for debugging, such as padding for detecting buffer overrun.
- We can have much better control over what we’d like to do with the memory chunks, such as deciding whether we have enough time in a frame to perform a quick internal memory defragmentation.

### Pages & Blocks

Each memory chunks we allocate is called a **page**, and each small part of a page that we use to store one whole piece of data is called a **block**.

For the examples in this series, an allocator can only create fix-sized pages and allocate fix-sized blocks to client code. Each allocator has a **page list** that keeps track of all pages created by the allocator; it also has a **free list** that keeps track of all blocks that can be allocated.

The lists are implemented as singly-linked lists, so each page only has a memory overhead of one extra pointer. Each block would also have a pointer, but that memory space will be shared (i.e. union-ed) with user data once the block is allocated (because the pointer is not needed when a block is allocated).

Here are the header structures used for pages and blocks:

struct BlockHeader { // union-ed with data BlockHeader *Next; }; struct PageHeader { // followed by blocks in this page PageHeader *Next; // helper function that gives the first block BlockHeader *Blocks(void) { return reinterpret_cast<BlockHeader *>(this + 1); } };

### The Allocator Interface

Finally, the allocator. I’m going to show you the interface of the `Allocator`

class first:

class Allocator { public: // debug patterns static const unsigned char PATTERN_ALIGN = 0xFC; static const unsigned char PATTERN_ALLOC = 0xFD; static const unsigned char PATTERN_FREE = 0xFE; // constructor Allocator ( unsigned dataSize, unsigned pageSize, unsigned alignment ); // destructor ~Allocator(void); // resets the allocator to a new configuration void Reset ( unsigned dataSize, unsigned pageSize, unsigned alignment ); // allocates a block of memory void *Allocate(void); // deallocates a block of memory void Free(void *p); // deallocates all memory void FreeAll(void); private: // fill a free page with debug patterns void FillFreePage(PageHeader *p); // fill a free block with debug patterns void FillFreeBlock(BlockHeader *p); // fill an allocated block with debug patterns void FillAllocatedBlock(BlockHeader *p); // gets the next block BlockHeader *NextBlock(BlockHeader *p); // the page list PageHeader *m_pageList; // the free list BlockHeader *m_freeList; // size-related data unsigned m_dataSize ; unsigned m_pageSize ; unsigned m_alignmentSize; unsigned m_blockSize ; unsigned m_blocksPerPage; // statistics unsigned m_numPages ; unsigned m_numBlocks ; unsigned m_numFreeBlocks; // disable copy & assignment Allocator(const Allocator &clone); Allocator &operator=(const Allocator &rhs); };

The **debug patterns**, as their names suggest, are used to fill in memory chunks for debug purposes. The **constructor** and ** Reset** method decide the size of each block and page, as well as alignment (more on this later). The

**method “allocates”, or returns the address of, a block of memory that can then be used by client code. The**

`Allocate`

**method does just the opposite: it puts a block of memory back into the free list so that it can be re-used. The**

`Free`

**method frees all pages; this method is for cleaning up all pages created by the allocator.**

`FreeAll`

### Sample Client Code

You would create an allocator and use it to allocate and free blocks in client code like this:

// create allocator Allocator alloc(sizeof(unsigned), 1024, 4); // allocate memory unsigned *i = reinterpret_cast<unsigned *>(alloc.Allocate()); // manipulate memory *i = 0u; // free memory alloc.Free(i);

### The Constructor & Destructor

The constructor and the `Reset`

method basically do the same thing, so it’s not surprising that the constructor simply calls the `Reset`

method. Same thing goes for the destructor and the `FreeAll`

method.

Allocator::Allocator ( unsigned dataSize, unsigned pageSize, unsigned alignment ) : m_pageList(nullptr) , m_freeList(nullptr) { Reset(dataSize, pageSize, alignment); } Allocator::~Allocator(void) { FreeAll(); }

### The `Reset`

Method

The `Reset`

method first frees all pages, and re-configures the allocator with the new data size, page size, and alignment size. The **data size** is basically the size of memory block the client wishes to allocate; the actual physical block size can be equal to or larger than the data size due to alignment.

The **alignment size** is the number of extra bytes added to a block, so that the block size is a multiple of the specified alignment. This is for efficient memory access. If your machine’s CPU loads data at 4-byte physical memory boundary, you most likely would not have your data starting at non-4-byte boundary; otherwise, the CPU might spend extra cycles loading the data into registers.

The maximum of data size and block header size is chosen to be the actual block size (minus alignment), because we still want each block to be large enough to fit in a block header even when the client code specifies a smaller data size.

void Allocator::Reset ( unsigned dataSize, unsigned pageSize, unsigned alignment ) { FreeAll(); m_dataSize = dataSize; m_pageSize = pageSize; unsigned maxHeaderData = Max(sizeof(BlockHeader), m_dataSize); m_alignmentSize = (maxHeaderData % alignment) ? (alignment - maxHeaderData % alignment) : (0); m_blockSize = maxHeaderData + m_alignmentSize; m_blocksPerPage = (m_pageSize - sizeof(PageHeader)) / m_blockSize; }

### The `Allocate`

Method

The `Allocate`

method is the meat of the allocator. It creates pages, fills the pages with debug patterns, pushes new pages to the page list, links all the new free blocks, and pushes them to the free list.

void *Allocator::Allocate(void) { // free list empty, create new page if (!m_freeList) { // allocate new page PageHeader *newPage = reinterpret_cast<PageHeader *> (new char[m_pageSize]); ++m_numPages; m_numBlocks += m_blocksPerPage; m_numFreeBlocks += m_blocksPerPage; FillFreePage(newPage); // page list not empty, link new page if (m_pageList) { newPage->Next = m_pageList; } // push new page m_pageList = newPage; // link new free blocks BlockHeader *currBlock = newPage->Blocks(); for (unsigned i = 0; i < m_blocksPerPage - 1; ++i) { currBlock->Next = NextBlock(currBlock); currBlock = NextBlock(currBlock); } currBlock->Next = nullptr; // last block // push new blocks m_freeList = newPage->Blocks(); } // pop free block BlockHeader *freeBlock = m_freeList; m_freeList = m_freeList->Next; --m_numFreeBlocks; FillAllocatedBlock(freeBlock); return freeBlock; }

### The `Free`

& `FreeAll`

Methods

The `Free`

method simply puts a block back into the free list.

void Allocator::Free(void *p) { // retrieve block header BlockHeader *block = reinterpret_cast<BlockHeader *>(p); FillFreeBlock(block); // push block block->Next = m_freeList; m_freeList = block; ++m_numFreeBlocks; }

And the `FreeAll`

method frees all pages created by the allocator.

void Allocator::FreeAll(void) { // free all pages PageHeader *pageWalker = m_pageList; while (pageWalker) { PageHeader *currPage = pageWalker; pageWalker = pageWalker->Next; delete [] reinterpret_cast<char *>(currPage); } // release pointers m_pageList = nullptr; m_freeList = nullptr; // re-init stats m_numPages = 0; m_numBlocks = 0; m_numFreeBlocks = 0; }

### Helper Methods

Finally, the helper methods. I’m just going to post the implementation, because the code is quite self-explanatory.

void Allocator::FillFreePage(PageHeader *p) { // page header p->Next = nullptr; // blocks BlockHeader *currBlock = p->Blocks(); for (unsigned i = 0; i < m_blocksPerPage; ++i) { FillFreeBlock(currBlock); currBlock = NextBlock(currBlock); } } void Allocator::FillFreeBlock(BlockHeader *p) { // block header + data std::memset ( p, PATTERN_FREE, m_blockSize - m_alignmentSize ); // alignment std::memset ( reinterpret_cast<char *>(p) + m_blockSize - m_alignmentSize, PATTERN_ALIGNMENT, m_alignmentSize ); } void Allocator::FillAllocatedBlock(BlockHeader *p) { // block header + data std::memset ( p, PATTERN_ALLOCATED, m_blockSize - m_alignmentSize ); // alignment std::memset ( reinterpret_cast<char *>(p) + m_blockSize - m_alignmentSize, PATTERN_ALIGNMENT, m_alignmentSize ); } Allocator::BlockHeader * Allocator::NextBlock (BlockHeader *p) { return reinterpret_cast<BlockHeader *> (reinterpret_cast<char *>(p) + m_blockSize); }

### Done!

This concludes the first part of this series. I hope you find this post useful 🙂

Nice article, though due to design errors this allocator is unusable as is. For example, the first block in every page doesn’t follow the alignment specification. It’s simply placed at the address immediately followed by the page header (sizeof(void*) + 1). If the specified alignment is for example 16 bytes, then the first block shouldn’t be placed at 4 (x86) or 8 (x64) bytes. This is easily solved by having the starting address of the first block to begin at the 2nd block so to speak. In other words; the page header already consumes an entire block anyway within that page; there’s no reason not to fix this misalignment error by placing the first block appropriately.

In addition, the allocator uses a loop in the Allocate(). This obviously is a no go, a performance killer and cache destroyer. There’s no need to link all blocks upon page allocation. To make this function correct and performant, you simply have to setup 1 next pointer in each call to Allocate() for as long as you have to. For reference I refer to the Fast Efficient Fixed-Sized Memory Pool-paper by Ben Kenwright. Which brings me to the following:

The allocator has a tremendous overhead; every single page 1 full block is wasted due to the page header. There is no need for page headers.All you need is a few bytes (< 64) of management data for the allocator provided you'd be using indices rather than pointers. Again I refer to the named paper, which principle applies to dynamically sized data as well.

Also, the allocator is non-portable at best. Apart from the calls to the CRT, which is nonportable in itself, it uses a predefined page size of 8192. Memory page size is highly platform-, system-, and runtime-dependant. Some systems don't even support pages as small or as large as 8192, and for most systems the page size is not 8192 at all.

Nevertheless, nice article for people trying to get a better idea of memory management techniques.

Thanks (very belated…) for the reply!

Makes sense… This is indeed a very tricky topic to wrap my head around. I’ve gotten spoiled by using the stack/heap for my memory allocations. I recently began tinkering with Wii Homebrew, I may have to really take a long hard look at this and my memory usage practices.

Pingback: Billiards Part 4 – Android Studio Asset Class - Programming Money

Great articles! One question if I may… I read later (in part 3) about using a custom allocator with STL containers. How would you use it for any other type of allocation like say to store an SDL_Texture?

Just like you would with the primitive types shown in the examples. You write something like: