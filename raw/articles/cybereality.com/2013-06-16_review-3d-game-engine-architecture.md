---
title: 'Review: 3D Game Engine Architecture'
url: https://cybereality.com/review-3d-game-engine-architecture/
author: Cybereality
published: '2013-06-16'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/f74e95be48dad0e8.jpg)

In preparation for my 3D game engine, I have been trying to read all I can on 3D engine design and architecture. Although there are some good books out there, it’s very difficult to find a text that will walk you through everything you need to know. That said, 3D Game Engine Architecture: Engineering Real-Time Applications with Wild Magic by David H. Eberly gives it a good attempt.

The book covers the author’s Wild Magic engine, and discusses certain choices he made when developing the engine. It briefly touches on OpenGL, discusses abstracting away platform-specific details, 3D mathematics (and there is a lot of math in this book), an object system, scene-graphs, level of detail, render states, sorting, terrain, animation, collision detection, physics, and more. A lot of ground is covered in less than 800 pages.

However, I found much of the book difficult to follow and still feel like I could have a better picture of the “architecture” of an engine. When I think of “architecture” I think about a broad 500 foot view of a project. I think of flow charts or UML. I expect discussion on how all these disparate elements come together a form a whole. Sadly, that is mostly missing from this book. What the author provides is a good insight into his particular engine, and certain specific aspects of that engine. While this is still a great example to look at, I feel the text could have been more robust in terms of painting the big picture. Some of the things that I found missing were an event system, which seems crucial to an object-oriented engine, or a component architecture, really any type of structure that allows communication between classes.

Additionally, I found myself getting lost multiple times while reading the book. The author would frequently put in dense mathematical equations and proofs, sometimes spanning multiple pages, and by the end you would be left to wonder what the purpose of the equation even was. I feel like having proofs of equations was not really relevant to the architecture, and surely there are many books on straight math if the reader needed that. Some math is necessary, of course, for a 3D engine but the space could have been used for more important topics.

Not really a jab at the book so much as it is the author’s coding conventions, I really did not like his style. I realize this is somewhat of a holy-war with programmers, but I guess we all have a style that is comfortable for us. Personally I found the author’s style to be really obtuse, and made reading the code snippets more difficult. For example, for a camera’s forward vector, he would use something like:

m_pkFVec

Where “m_” was a member variable, “p” is a pointer, “k” is of a class type, and “FVec” for forward vector. Personally I would use simply:

forwardVector

Just glancing through the code, which one is more apparent to what it is? This really bothered me to no end, but I guess you can chock it up to personal taste.

All-in-all it may sound like I am putting down on this book, but I actually did find it useful in a lot of ways. Certainly if you are aiming to create a 3D game engine from scratch, you will need any and all the help you can get. So yes, still read this book. However, I had much higher expectations and I feel it was a missed opportunity for the author. While it is still a decent resource, this should not be your first stop in engine development.