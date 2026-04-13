---
title: Visual Studio 2013 / Demo Skeleton Programming
url: http://diaryofagraphicsprogrammer.blogspot.com/2013/11/visual-studio-2013-demo-skeleton.html
author: Wolfgang Engel
published: '2013-11-07'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I updated my demo skeleton in the google code repository. It is using now Visual Studio 2013, that now partially supports C99 and therefore can compile the code.
I updated the compute shader code a bit and I upgraded Crinkler to version 1.4. The compute shader example now also compiles the shader into a header file and then Crinkler compresses this file as part of the data compression. It packs now overall to 2,955 bytes.




If you have fun with this code, let me know ... :-)

[https://code.google.com/p/graphicsdemoskeleton/](https://code.google.com/p/graphicsdemoskeleton/)If you have fun with this code, let me know ... :-)

## 2 comments:

So what's the size of the blob once compiled? Did you try including the source instead?

I've not been following demoscene for a while,but it's been common practice to include shaders with names stripped down to a minimum (1 character), removed carriage returns/tabs etc.And it also compresses nicely.

I compiled the shader to a header file and included the header file. This way Crinkler probably optimizes what is left from the original shader in the data segment.

Post a Comment