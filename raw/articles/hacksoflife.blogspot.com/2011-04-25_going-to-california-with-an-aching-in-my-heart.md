---
title: Going to California (with an Aching in My Heart)
url: http://hacksoflife.blogspot.com/2011/04/going-to-california-with-aching-in-my.html
author: Benjamin Supnik
published: '2011-04-25'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[this article](http://duartes.org/gustavo/blog/post/what-your-computer-does-while-you-wait). In particular, putting memory distance in human terms helps give you a sense of the metaphorical groan your CPU must make every time it misses a cache.

- L1 cache: it's on your desk, pick it up.
- L2 cache: it's on the bookshelf in your office, get up out of the chair.
- Main memory: it's on the shelf in your garage downstairs, might as well get a snack while you're down there.
- Disk: it's in, um, California. Walk there. Walk back. Really.*

If anything, that's a testimant to how good the operating systems are at

[hiding the disk drive from us](http://duartes.org/gustavo/blog/post/page-cache-the-affair-between-memory-and-files)most of the time.

The moral of the story: the disk can look a lot faster than it is, but only if you let it. Unfortunately, there is one aspect of X-Plane that fails miserably at this: the use of a gajillion tiny text file for scenery packages. The solution is simple:

[pack the files into one bigger file](http://wiki.x-plane.com/DSF_Art_Asset_Storage_RFC). This will let the OS pick up the (hopefully consecutive) single larger file and dump significant amounts of it into the page cache in one swoop without doing a million seeks. California is far away.

* The author's metaphor maps one cycle to one human second. That's the equivalent of 474. days for a 3 ghz CPU to take a 41 ms wait on a disk seek. You'd have to put up better than 12 miles a day to make it to California and back from the East coast. If you actually live out west, um, pretend you're an SSD.

Great Link!

ReplyDelete