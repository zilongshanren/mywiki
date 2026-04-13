---
title: The Magic Ring Buffer
url: https://fgiesen.wordpress.com/2012/07/21/the-magic-ring-buffer/
published: '2012-07-21'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# The Magic Ring Buffer

This is a cute little trick that would be way more useful if there was proper OS support for it. It’s useful in a fairly small number of cases, but it’s nice enough to be worth writing up.

### Ring buffers

I’m assuming you know what a ring buffer is, and how it’s typically implemented. I’ve [written about it before](https://fgiesen.wordpress.com/2010/12/14/ring-buffers-and-queues/), focusing on different ways to keep count of the fill state (and what that means for the invariants). Ring buffers are a really nice data structure – the only problem is that everything that directly interfaces with ring buffers needs to be aware of the fact, to handle wrap-around correctly. With careful interface design, this can be done fairly transparently: if you use the technique I described in [“Buffer-centric IO”](https://fgiesen.wordpress.com/2011/11/21/buffer-centric-io/), the producer has enough control over the consumer’s view on the data to make the wrap-around fully transparent. However, while this is a nice way of avoiding copies in the innards of an IO system, it’s too unwieldy to pass down to client code. A lot of code is written assuming data that is completely linear in memory, and using such code with ring buffers requires copying the data out to a linear block in memory first.

Unless you’re using what I’m calling a “magic ring buffer”, that is.

### The idea

The underlying concept is quite simple: “unwrap” the ring by placing multiple identical copies of it right next to each other in memory. In theory you can have an arbitrary number of copies, but in practice two is sufficient in basically all practical use cases, so that’s what I’ll be using here.

Of course, keeping the multiple copies in sync is both annoying and tricky to get right, and essentially doing every memory access twice is a bad idea. Luckily, we don’t actually need to keep two physical copies of the data around. Really the only thing we need is to have the same physical data in two separate (logical, or virtual) memory locations – and virtual memory (paging) hardware is, at this point, ubiquitous. Using paging means we get some external constraints: buffers have to have sizes that are (at least) a multiple of the processor’s page size (potentially larger, if virtual memory is managed at a coarser granularity) and meet some alignment constraints. If those restrictions are acceptable, then really all we need is some way to get the OS to map the same physical memory multiple times into our address space, using calls available from user space.

The right facility turns out to be memory mapped files: modern OSes generally provide support for anonymous mmaps, which are “memory mapped files” that aren’t actually backed by any file at all (except maybe the swap file). And using the right incantations, these OSes can indeed be made to map the same region of physical memory multiple times into a contiguous virtual address range – exactly what we need!

### The code

I’ve written a basic implementation of this idea in C++ for Windows. The code is available [here](https://gist.github.com/3158316). The implementation is a bit dodgy (see comments) since Windows won’t let me reserve a memory region for memory-mapping (as far as I can tell, this can only be done for allocations), so there’s a bit of a song and dance routine involved in trying to get an address we can map to – other threads might be end up allocating the memory range we just found between us freeing it and completing our own mapping, so we might have to retry several times.

On the various Unix flavors, you can try the same basic principle, though you might actually need to create a backing file in some cases (I don’t see a way to do it without when relying purely on POSIX functionality). For Linux you should be able to do it using an anonymous shared mmap followed by remap_file_pages. No matter which Unix flavor you’re on, you can do it without a race condition, so that part is much nicer. (Though it’s really better without a backing file, or at most a backing file on a RAM disk, since you certainly don’t want to cause disk IO with this).

The code also has a small example to show it in action.

**UPDATE**: In the comments there is now also a link to two articles describing how to implement the same idea (and it turns out using pretty much the same trick) on MacOS X, and it turns out that [Wikipedia](http://en.wikipedia.org/wiki/Circular_buffer#Optimized_POSIX_Implementation) has working code for a (race-condition free) POSIX variant as described earlier.

### Coda: Why I originally wanted this

There’s a few cases where this kind of thing is useful (several of them IO-related, as mentioned in the introduction), but the case where I originally really wanted this was for inter-thread communication. The setting had one thread producing variable-sized commands and one thread consuming them, with a SPSC queue inbetween them. Without a magic ring buffer, doing this was a major hassle: wraparound could theoretically happen anywhere in the middle of a command (well, at any word boundary anyway), so this case was detected and there was a special command to skip ahead in the ring buffer that was inserted whenever the “real” command would’ve wrapped around. With a magic ring buffer, all the logic and special cases just disappear, and so does some amount of wasted memory. It’s not huge, but it sure is nice.

There are a couple of in-depth articles about implementing this same idea on Mach / OS X:

http://www.mikeash.com/pyblog/friday-qa-2012-02-03-ring-buffers-and-mirrored-memory-part-i.html

http://www.mikeash.com/pyblog/friday-qa-2012-02-17-ring-buffers-and-mirrored-memory-part-ii.html

Here’s a version done on Mac OS X. This one uses three contiguous mappings.

http://www.mikeash.com/pyblog/friday-qa-2012-02-03-ring-buffers-and-mirrored-memory-part-i.html

http://www.mikeash.com/pyblog/friday-qa-2012-02-17-ring-buffers-and-mirrored-memory-part-ii.html

Cool trick. It seems to me that if you’re working entirely within your own code base, it’s very easy to just use power-of-two circular buffers and AND the index, so I don’t really see the reason to mess around. (eg. doing one AND for an SPSC queue doesn’t seem like it’s worth avoiding)

But if you have a ring buffer and you want to hand it off to some other code that assumes a linear buffer, this is a nice trick.

Another common case I run into is if you have several buffers and you want to pass them all off to some code that assumes a single linear buffer, it would be awesome if you could set up virtual address maps to make them appear contiguous.

(hell, that could even be used with std::vector so that you could just add on non-contiguous pages instead of doing a realloc and copy, but make it still appear contiguous to the client code)

The thing that would be really sweet is if you could map some virtual memory range and associate it with a user callback to service page misses. That way you could do linear -> ring mappings, or pull in chunks for IO or decompress chunks, or whatever, as needed. I guess there are good reasons why this isn’t offered, but it’s too bad because it would be a very powerful facility.

For LZ compression I’ve often wanted a simple subset of the full functionality. It would be cool if you could set up a virtual address range and then define some rules like “this range ring maps to this buffer” and “any read from this range returns a zero” or “writes in this range have no affect”. If you could do that then you could remove all the out-of-range checks from the string matching, which would be a nice speed boost.

(BTW this comment box might be even worse than the horrible one on Blogger; yegads!)

If your SPSC is just an array of pointers, then yeah just AND is fine (because writing a single entry is only ever one store). If your SPSC is an array of homogeneous items, then it presumably has an integral multiple of the item size, and again wraps will only ever happen at item boundaries – one AND per item inserted, no big deal. But *omatic has what is effectively command buffers at the hand-off between phases, not just work item queues.That is, it’s a “queue” of heterogeneous, variable-sized items. There were lots of commands that were only 4 bytes, but some could contain a kilobyte or more of payload. Constraining the latter to only ever be inserted in places where they can’t wrap around wastes memory and generates temporary spikes in the “insertion rate” – writing 1k will take some amount of time that gives the consumer thread time to catch up, but writing what’s effectively a single NOP that jumps across 1k is pretty much instant and messes up nice steady flows. So if you want to wrap around properly, you can either add ANDs *on every single write* or detect wrap-around early, redirect the regular writes to a scratch buffer, then do a wrapping memcpy to do the actual insertion. Similarly on the consumer side. Both of these are ugly and annoying. If you do it using VM, the only cost is a bit of work during init time and however many TLB entries you spend on the wrap-around area (usually 1).

Another option for heterogeneous queues is to keep a queue of pointers to the data (with an extra type field somewhere, either in the data or per queue entry). That means the queue is now simple, but now you need to allocate memory and manage lifetimes. Of course, it’s just between two threads that are producing/consuming at some steady rate, so you could just use a constant-sized ring buffer and stall if there’s not enough space to do the allocation… and then we’re back to where we started :)

LZ is a bit annoying there. You can easily make an LZ that has its window as a ring buffer with this, and that works and is really nice, but still generally requires a memcpy at the end to be useful to the consumer (to copy the data to its final destination). If you want the data to end up directly in the user’s allocation, well that can be done too but now you need to remap pages regularly through the whole operation and it becomes a whole lot less appealing – especially since you also need some address space slop on either side to handle the boundary cases.

If you can’t or don’t want to use VM, you can just allocate from the beginning of the buffer if the allocated block would wrap. This wastes some memory (i.e. the remaining of the buffer if the block doesn’t fit without warpping), but it’s useful for things like temporal dynamic vertex data allocation, and is transparent to producer/consumer. The wasted memory may not be too bad if we are talking about a large multi-MB buffer and allocations are few KB. I think I’m stating the obvious though, but I didn’t see it being mentioned anywhere so I put it out there. Anyway, the VM trick is a nice idea when it’s applicable.

On POSIX systems, you may want to check out http://vrb.slashusr.org/

Just a quick note on not being able to reserver but not commit memory mappings:

You can get around limitations of Win32 API and directly use the underlying NT APIs that have this functionality.

ZwCreateSecton

ZwMapViewOfSection

See http://msdn.microsoft.com/en-us/library/windows/hardware/ff567122(v=vs.85).aspx

The “Optimized POSIX Implementation” section has recently been removed from the linked Wikipedia article, this is the last revision that contains it:

http://en.wikipedia.org/w/index.php?title=Circular_buffer&oldid=600431497#Optimized_POSIX_implementation

I put a bit modified copy of that code here: https://github.com/vitalyvch/rng_buf

Win10 has support for this now with VirtualAlloc2

They have an example here:

https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc2

Note you need to link with mincore.lib, not kernel32.lib