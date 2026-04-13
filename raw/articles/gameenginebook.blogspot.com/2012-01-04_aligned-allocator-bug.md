---
title: Aligned Allocator Bug
url: http://gameenginebook.blogspot.com/2012/01/from-dave-asbell-hey-jason-i-am-reading.html
author: Jqgregory
published: '2012-01-04'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**From:**Dave Asbell

Hey Jason,

I am reading your book and I think there is a bug in the aligned allocator. Shouldn't the code be casting the alignedAddress to a U8 instead of a U32 and subtracting 1 byte instead of 4? I believe this would write the offset into the byte preceding the aligned address instead of the word. Similarly shouldn't the free routine be using a 1 byte offset as well? Perhaps I am missing something. In any event I love the book and look forward to finishing it.

_________________________________________

You are quite right; the code was written originally with 4-byte offsets, but I changed it (very sloppily!) to use 1-byte offsets without double-checking it. It's one of the errata I plan to post on the book's site when I get some free time.

Glad you're enjoying it! Do send along any other errata you notice.

Cheers,

J

## No comments:

## Post a Comment