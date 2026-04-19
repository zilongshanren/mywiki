---
title: 'Review: 3D Game Engine Programming'
url: https://cybereality.com/review-3d-game-engine-programming/
author: Cybereality
published: '2013-09-23'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![3D Game Engine Programming](../../assets/6c90313681c7c402.jpg)


The quest to become a master of 3D engines has brought me to another book, 3D Game Engine Programming by Stefan Zerbst (with a forward from the legendary Andre LaMothe). This is one of the first books I’ve read in a while that wasn’t available on the Kindle, and it’s out of print, but I managed to find a used copy of the paperback without a problem. At a somewhat meaty 850 pages, it was a little cumbersome to read, especially laying down in bed. It’s really amazing how spoiled you get with new technology. Anyway, the book was great and I enjoyed the whole thing.

Though I have been reading a bunch of books on graphics programming, this one was a refreshing peek into the design of a 3D engine. It was also obvious that the engine was a living, breathing thing. Not just a sample created for the book. Zerbst covers a lot of ground here: rendering with DirectX9, sound, input, scene management, networking, a math library, even creating a simple level editor/low-poly modeler. And he goes in-depth, even to the point of hand-coding assembly for optimizing a vector class. And, somehow, he made it make sense.

I very much enjoyed the amount of code and the amount of discussion that followed each piece. There are tons of code samples throughout the book, with ample explanation as to what everything is doing. Though there were a few cases of long, multi-page code samples, for the most part the author kept things as concise as possible.

Another thing I liked was how Stefan Zerbst broke out each major component of the engine into it’s own DLL (i.e. one for graphics, one for sound, one for input, etc.). I think this is a great idea, and has the potential to speed up development without having to compile all these parts of the engine every time you need to test your game. This is certainly something I want to explore further with my engine.

Surprisingly, the book was not totally outdated considering it was first published in 2004 (almost 10 years ago, OMG!). Granted, there is some discussion of stencil shadows and the fixed-function pipeline but, for the most part, the basic concepts are still valid today. It’s also somewhat amazing (or amusing) that Microsoft created an API (DirectX9) that still going strong so many years later.

However, the book isn’t totally without fault. One thing that seemed a little strange was the authors liberal use of global variables for key parts of the engine. He would even say: “I am just using a global here to make things simple as an example, you may not want to do this in your engine” or something to that effect. I understand making things easy for illustration, but why not show us the right way to do it?

It’s not like one single book could ever cover all you need to know about writing 3D engines, certainly not in 850 pages. That being said, 3D Game Engine Programming is an awesome resource for the aspiring engine creator. It covers territory not seem in other books and really digs deep into the aspects that matter. All-in-all I found this text to be helpful and am glad to have it in my growing collection.