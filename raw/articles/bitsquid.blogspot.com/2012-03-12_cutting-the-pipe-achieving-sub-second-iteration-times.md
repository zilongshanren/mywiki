---
title: 'Cutting the Pipe: Achieving Sub-Second Iteration Times'
url: https://bitsquid.blogspot.com/2012/03/cutting-pipe-achieving-sub-second.html
author: Niklas
published: '2012-03-12'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

After watching I had two questions I was hoping you could clarify:

1) How much of your code base is shared between your tools and your engine? Having external tools seems like a very flexible system for game development, but I can't wrap my head around how an external level editor could grab an object's internal RTTI/introspection information without some knowledge of the engine. It seems like serialization would also be troublesome without a shared core (unless only the engine serializes the object?).

2) There was another presentation about tools and debugging, given by an AI dev at EA, where the dev talked about being able to add tabs to an external C# editor from C++. They ended up using this system to make editors easier to extend and easier to display in a uniform manner. Do you support or have the need to support any features like this? I'm worried that if I go the external editors route, my artist/designers will have to learn a lot of different tools, unnecessarily.

Thanks for all of your awesome blog postings, you're one of my favorite coders on the web!

1) None. Our tools are written in C# and our engine in C++. We don't make much use of RTTI/introspection. In my experience, while such techniques will get you up and running quickly they also create strong couplings (between data layout in memory and file structure on disk or GUI layout) that are damaging in the long run. The engine and the tools communicate through readable and mergeable JSON files with a well-defined format. The files are written by the editors and read by the engine. The engine then compiles the data to its own high-performing format (blobs), but the editors don't have anything to do with that format. I believe the separation between editor and engine is a strong point, because the what is right for engine code is seldom right for editor code and vice versa.

2) We have a shared library that is used by many of our different editors to implement shared functionality. I don't think having consistency and a similar look-and-feel between different tools has that much to do with whether they reside in the same executable or not.

Sorry for just barging into an older post, but I just read the article and got curious at the line: "Don’t put all level geometry in a single ﬁle". Most objects will probably be shared between levels or are special in someway so referencing them is the logical way to do it. But what about basic geometry, such as floors and walls? Those are probably made inside the level editor and not in a DCC package, right? Is this the only geometry that'll be stored inside the level file, or will these also be split up?

Very nice article! Thanks a lot for sharing this.

ReplyDeleteAs always, Niklas, very inspiring, thanks a lot. How much time have you already invested in your engine, I wonder?

ReplyDeleteGreat Presentation, Niklas!






ReplyDeleteAfter watching I had two questions I was hoping you could clarify:

1) How much of your code base is shared between your tools and your engine? Having external tools seems like a very flexible system for game development, but I can't wrap my head around how an external level editor could grab an object's internal RTTI/introspection information without some knowledge of the engine. It seems like serialization would also be troublesome without a shared core (unless only the engine serializes the object?).

2) There was another presentation about tools and debugging, given by an AI dev at EA, where the dev talked about being able to add tabs to an external C# editor from C++. They ended up using this system to make editors easier to extend and easier to display in a uniform manner. Do you support or have the need to support any features like this? I'm worried that if I go the external editors route, my artist/designers will have to learn a lot of different tools, unnecessarily.

Thanks for all of your awesome blog postings, you're one of my favorite coders on the web!

-Jeff

Hi, thanks for the kind words.



ReplyDelete1) None. Our tools are written in C# and our engine in C++. We don't make much use of RTTI/introspection. In my experience, while such techniques will get you up and running quickly they also create strong couplings (between data layout in memory and file structure on disk or GUI layout) that are damaging in the long run. The engine and the tools communicate through readable and mergeable JSON files with a well-defined format. The files are written by the editors and read by the engine. The engine then compiles the data to its own high-performing format (blobs), but the editors don't have anything to do with that format. I believe the separation between editor and engine is a strong point, because the what is right for engine code is seldom right for editor code and vice versa.

2) We have a shared library that is used by many of our different editors to implement shared functionality. I don't think having consistency and a similar look-and-feel between different tools has that much to do with whether they reside in the same executable or not.

Sorry for just barging into an older post, but I just read the article and got curious at the line: "Don’t put all level geometry in a single ﬁle". Most objects will probably be shared between levels or are special in someway so referencing them is the logical way to do it. But what about basic geometry, such as floors and walls? Those are probably made inside the level editor and not in a DCC package, right? Is this the only geometry that'll be stored inside the level file, or will these also be split up?


ReplyDeleteAnyway, thanks for sharing and awesome work! :)

You have done awesome work on it. Yellowstone Coat

ReplyDeleteyou've created beautiful image using sagacious words. laudable work!






ReplyDeleteyellowatone hoodie coat