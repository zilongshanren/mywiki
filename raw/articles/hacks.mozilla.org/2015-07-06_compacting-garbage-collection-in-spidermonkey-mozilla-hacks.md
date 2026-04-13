---
title: Compacting Garbage Collection in SpiderMonkey – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/07/compacting-garbage-collection-in-spidermonkey/
author: Jon Coppeard
published: '2015-07-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Overview

Compacting is a new feature of our [garbage collector](https://en.wikipedia.org/wiki/Garbage_collection_%28computer_science%29), released in Firefox 38, that allows us to reduce external fragmentation in the JavaScript heap. The aim is to use less memory in general and to be able to recover from more out-of-memory situations. So far, we have only implemented compacting for JavaScript objects, which are one of several kinds of garbage-collected cells in the heap.

## The problem

The JavaScript heap is made up of 4K blocks of memory called *arenas*, each of which is divided into fixed-size cells. Different arenas are used to allocate different kinds of cells; each arena only contains cells of the same size and kind.

The heap contains various kinds of cell, including those for JavaScript objects, strings, and symbols, as well as several internal kinds such as scripts (used to represent units of JS code), shapes (used to determine the layout of object properties in memory), and jitcode (compiled JIT code). Of these, object cells usually take up the most memory.

An arena cannot be freed while it contains any live cells. Cells allocated at the same time may have different lifetimes and so a heap may end up in a state where there are many arenas that contain only a few cells. New cells of the same kind can be allocated into this space, but the space cannot be used for cells of a different kind or returned to the operating system if memory is low.

Here is a simplified diagram of some data on the heap showing arenas containing two different kinds of cell:

![heap layout smallest](../../assets/f5abda302e72de26.png)


Note that if the free space in arena 3 were used to hold the cells in arena 5, we could free up a whole arena.

## Measuring wasted heap space

You can see how much memory these free cells are taking up by navigating to about:memory and hitting the ‘Measure’ button. The totals for the different kinds of cell are shown under the section `js-main-runtime-gc-heap-committed/unused/gc-things`

. (If you’re not used to interpreting the about:memory reports, there is [some documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Performance/about:memory) here).

Here’s a screenshot of the whole `js-main-runtime-gc-heap-committed`

section with compacting GC disabled, showing the difference between ‘used’ and ‘unused’ sizes:

![unused heap screenshot](../../assets/d7993fd7c27d4d40.png)


I made some rough measurements of my normal browsing profile with and without compacting GC (details of how to do this are below at the end of the post). The profile consisted of Google Mail, Calendar, many bugzilla tabs and various others (~50 tabs total), and I obtained the following readings:

| Total explicit allocations | Unused cells | |
|---|---|---|
| Before compacting | 1,324.46 MiB | 69.58 MiB |
| After compacting | 1,296.28 MiB | 40.18 MiB |

This shows a reduction of 29.4MiB ([mebibytes](https://en.wikipedia.org/wiki/Mebibyte)) worth of explicit allocations. That’s only about 2% of total allocations, but accounts for over 8% of the space taken up by the JS heap.

## How does compacting work?

To free up this space we have to allow the GC to move cells between arenas. That way it can consolidate the live cells in fewer arenas and reuse the unused space. Of course, this is easier said than done, as every pointer to a moved cell must be updated. Missing a single one is a sure-fire way to make the browser crash!

Also, this is a potentially expensive operation as we have to scan many cells to find the pointers we need to update. Therefore the idea is to compact the heap only when memory is low or the user is inactive.

The algorithm works in three phases:

- Select the cells to move.
- Move the cells.
- Update the pointers to those cells.

### Selecting the cells to move

We want to move the minimum amount of data and we want to do it without allocating any more memory, as we may be doing this when we don’t have any free memory. To do this, we take all the arenas with free space in them and put them in a list arranged in decreasing order of the number of free cells they contain. We split this list into two parts at the first point at which the preceding arenas have enough free cells to contain the used cells in the subsequent arenas. We will move all the cells out of the subsequent arenas.

### Moving the cells

We allocate a new cell from one of the arenas we are not moving. The previous step ensures there is always enough space for this. Then we copy the data over from the original location.

In some cases, we know the cell contains pointers to itself and these are updated at this point. The browser may have external references to some kinds of object and so we also call an optional hook here to allow these to be updated.

When we have moved a cell, we update the original location with a forwarding pointer to the new location, so we can find it later. This also marks the cell, indicating to the GC that the cell has been moved, when updating pointers in the next phase.

### Updating pointers to moved cells

This is the most demanding part of the compacting process. In general, we don’t know which cells may contain pointers to cells we have moved, so it seems we have to iterate through all cells in the heap. This would be very expensive.

We cut down this cost in a number of ways. Firstly, note that the heap is split into several zones (there is a zone per browser tab, and others for system use). Compacting is performed per-zone, since in general cells do not have cross-zone pointers (these are handled separately). Compacting per zone allows us to spread the total cost over many incremental slices.

Secondly, not every kind of cell can contain pointers to every other kind of cell (indeed not all kinds of cells can contain pointers) so some kinds of cell can be excluded from the search.

Finally, we can parallelise this work and make use of all CPU resources available.

It’s important to note that this work was enabled by our shift to exact stack rooting, [described in this blog post](https://blog.mozilla.org/javascript/2013/07/18/clawing-our-way-back-to-precision/). It is only possible to move objects if we know which stack locations are roots, otherwise we could overwrite unrelated data on the stack if it happened to look like a moved cell pointer.

## Scheduling heap compaction

As mentioned earlier, compacting GC doesn’t run every time we collect. Currently it is triggered on three events:

- We ran out of memory and we’re performing a last-ditch attempt to free up some space
- The OS has sent us a memory pressure event
- The user has been inactive for some length of time (currently 20 seconds)

The first two should allow us to avoid some out-of-memory situations, while the last aims to free up memory without affecting the user’s browsing experience.

## Conclusion

Hopefully this has explained the problem compacting GC is trying to solve, and how it’s done.

One unexpected benefit of implementing compacting GC is that it showed us a couple of places where we weren’t correctly tracing cell pointers. Errors like this can cause hard-to-reproduce crashes or potential security vulnerabilities, so this was an additional win.

## Ideas for future work

The addition of compacting is an important step in improving our GC, but it’s not the end by any means. There are several ways in which we can continue to develop this:

Currently we only compact cells corresponding to JavaScript objects, but there are several other kinds of cells in the heap. Moving these would bring greater memory savings.

Is it possible to determine in advance which cells contain pointers to cells we want to move? If we had this information we could cut the cost of compacting. One possibility is to scan the heap in the background to determine this information, but we would need to be able to detect changes made by the mutator.

The current algorithm mixes together cells allocated at different times. Cells with similar lifetimes are often allocated at the same time, so this may not be the best strategy.

If compacting can be made fast enough, we might be able to do it whenever the collector sees a certain level of fragmentation in the heap.

## How to measure heap space freed up by compacting

To measure roughly how much space is freed by compacting, you can perform the following steps:

- Disable compacting by navigating to about:config and setting
`javascript.options.mem.gc_compacting`

to false. - It makes it easier to disable multiprocess Firefox as well at this point. This can be done from the main Preferences page.
- Restart the browser and open some tabs. I used ‘Reload all tabs’ to open all my pages from last time. Wait for everything to load.
- Open about:memory and force a full GC by clicking ‘Minimize memory usage’ and then click ‘Measure.’ Since memory usage can take a while to settle down, I repeated this a few times until I got a consistent number.
- Note the total ‘explicit’ size and that of
`js-main-runtime-gc-heap-committed/unused/gc-things`

. - Enable compacting again by setting
`javascript.options.mem.gc_compacting`

to true. There is no need to restart for this to take effect. - Click ‘Minimize memory usage’ again and then ‘Measure.’
- Compare the new readings to the previous.

This does not give precise readings as all kinds of things might be happening in the background, but it can provide a good ballpark figure.

## About Jon Coppeard

Software engineer working mainly on garbage collection in the JavaScript engine.

## 6 comments

Robert KnightJuly 7th, 2015 at 12:57Jon CoppeardJuly 8th, 2015 at 04:58xunxunJuly 12th, 2015 at 17:30Jon CoppeardJuly 13th, 2015 at 02:05LukeJuly 28th, 2015 at 18:25Jon CoppeardJuly 29th, 2015 at 03:25