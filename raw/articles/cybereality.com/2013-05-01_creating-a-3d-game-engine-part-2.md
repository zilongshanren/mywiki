---
title: Creating a 3D Game Engine (Part 2)
url: https://cybereality.com/creating-a-3d-game-engine-part-2/
author: Cybereality
published: '2013-05-01'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

With the first part of this series I have listed a few motivating reasons for developing a 3D game engine in the first place. In this next part I will go deeper into some of the research I have been doing for amassing the skills I feel are necessary to actually complete a project like this. As I have mentioned, one of the core reasons I am working on this engine is for knowledge building and personal development. Researching computer graphics plays a huge part in this. So I’d like to share some of the books I have been reading in the past year or so in preparation for creating my dream engine.

![Real-Time Rendering](../../assets/1b9f402b83b0757e.jpg)


** Real-Time Rendering, Third Edition (Tomas Akenine-Moller, et al):** This is one of the best books I have read so far on real-time graphics for gaming. There are a lot of equations, but they are usually explained well. However, there is not a lot of code here to just straight copy-and-paste. It’s not a cookbook. It’s really more of a 1000 foot view of gaming and real-time technology. It talks about all the different lighting and shading models currently used, discusses texturing, collision detection, intersection methods, image-based effects, 3D math for gaming, etc. Really a great overview of the types of things a 3D engine has to handle. As mentioned, it’s not a cookbook. There is very little code, if at all. But I found this to give a helpful glance at a lot of topics of interest, of course with sources to find more detailed information. Highly recommended.

![GamEngineArch](../../assets/435d085bf044ef45.jpg)


** Game Engine Architecture (Jason Gregory):** This is another amazing text. It talks about all the things that go into building a professional game and game engine. So 3D math is covered, as well as version control tools, fundamentals of coding in C++ (with cool tricks like memory alignment), main loops for rendering and game logic, debugging, character animation, collision and physics, and more. I found this book very insightful and actually made some of the topics listed a lot more understandable. I was especially surprised by some examples of main loops, as they were a lot more straight-forward than I previously thought. If you are attempting to code your own engine, this book should certainly be on the list.

![Game Coding Complete](../../assets/3ead772e562c12ff.jpg)


** Game Coding Complete, Fourth Edition (Mike McShaffry):** All I can say about this book is “Wow!”. There is an unbelievable amount of knowledge in these pages. This is the book I am currently reading, about 25% through so far, and I have already learned a bunch. This is another 1000 foot view, but they ground it with some really useful snippets of code. They give examples of different main/game loops, actor and component architecture, an event system, loading and caching resources, DirectX, scripting in LUA, collision, physics, creating an editor in C#, even network programming. This book is amazing! I’m not even finished yet and already I feel like I have learned so much. This is a must read.

![3D Math Primer](../../assets/6c5f61fbe15aa78f.jpg)


** 3D Math Primer for Graphics and Game Development, 2nd Edition (Fletcher Dunn):** I actually read the first edition, but I’m sure the updated text is just as good or better. It’s a book on 3D math for games. Certainly this is the type of book that’s great for foundation learning. Creating a good 3D engine will require a deep understanding of this type of math (mostly linear algebra) and this is a great book to get you started. Even though a lot of the equations are dense, I found the writing style to be approachable. It talks about all the stuff you would expect: vectors, matrices, orientation, transformations, etc. I would also recommend this book.

![](../../assets/1f6acb86a7a12bf2.jpg)


** Introduction to 3D Game Programming with DirectX 11 (Frank Luna):** This is one for my wishlist. I have read the older edition on DirectX 9.0c, but haven’t got around to this latest version. However, the series is one of the most recommended and highest rated books on the DirectX API. Luna’s writting style is very clear, and there is a lot of ground covered in the book. 3D math, drawing basic primatives, texture mapping, lighting, shadowing, normal/parallax mapping, ambient occlusion, etc. I like the little things that make the demo apps very polished (like being able to switch between windowed and full-screen with the touch of a button). If you plan to use the DirectX API for your engine, then this book is an absolute must.

![C++ Primer](../../assets/c62c59e55b8c3e42.jpg)


** C++ Primer (5th Edition) (Stanley B. Lippman):** Although I have been learning and working with C++ for years, I read this book recently and ended up learning a lot. Keep in mind this book covers the new C++11 standard, though most of the discussion still applies to the previous standard. This is, hands down, the most comprehensive book I’ve seen on C++. Most books teach you the basics, but fail to explain the intricacies of the language. Not here. The author goes deep and shows you everything you need to know (and more). I also liked that he kept the code samples short and to the point. There is not even one sample that you are expected to type in and test. If there was, the book would probably be twice as long (and it’s already pretty long at 1000+ pages). Rather the author chose to highlight relevant structures and algorithms with as little code possible. I found this method to be very effective. If you are just starting out with C++ then I would recommend reading

[C++ Primer Plus](https://www.amazon.com/Primer-Plus-6th-Developers-Library/dp/0321776402)first. However, if you already know some C++ and just want to brush up on your skills, this is a great resource.

Of course, I’m not going to list every book I’ve ever read on programming. These are just a few recent ones that I found useful. I will continue to post links to new books and other material that help me get closer to completing my 3D game engine. Even reading these books, there is still a lot of knowledge that can only be found by doing, and I hope future posts in this series will address that. After I get a better idea of the architecture of the engine, I can post some simple samples for review and for performance testing. Again, this is a learning process for me, so I would love to hear feedback from the community of this. Don’t be shy.