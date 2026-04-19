---
title: 'Review: Game Engine Design and Implementation by Alan Thorn'
url: https://cybereality.com/review-game-engine-design-and-implementation-by-alan-thorn/
author: Cybereality
published: '2013-12-05'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![Game Engine Design](../../assets/5d8c1d8304db8b6c.jpg)


Alan Thorn’s Game Engine Design and Implementation was quite an interesting read. Overall I thought it was good, but the book struggles at times to find it’s audience. On one hand, it covers a lot of great topics and there are some good code snippets to be found. On the other hand, it seems to jump around between APIs and frameworks and never really culminates with a complete engine. Even so, engine development is no breeze and any help in this area is much appreciated.

The text begins with the basics: downloading Visual Studio or Code::Blocks and configuring a development environment. It shows you how to create and call a DLL. Some brief coverage of the STL. All useful stuff. Then it moves on to some basic engine features, like logging errors and handling exceptions. Again a great place to start. It continues with a resource manager based on XML. Then a 2D scene manager and renderer using SDL. Supporting sound and music with the BASS library. Processing input with OIS. Then a renderer with DirectX 10. Great stuff. Then in the next chapter it throws out everything you just learned and jumps to working with OGRE. Don’t get me wrong, OGRE is a great API. But it seems strange for a book titled “Game Engine Design and Implementation” to use an off-the-shelf library and not code the, erm, implementation themselves. The book follows up with coverage of Bullet physics and ends with a brief overview of DX Studio, which is an all-in-one game engine solution.

While each chapter alone is very interesting and informative, I feel like the book as a whole lost it’s focus somewhere and the engine that you think you are creating at the beginning of the book never materializes. I almost feel bad, it’s like the author started with one premise of creating an engine from scratch, and then gives up half-way. I even agree that using pre-built tools are a good idea in many cases, and most people don’t want to re-invent SDL or OGRE or whatever. But there are other books that focus on these engines and frameworks. People picking up a book like “Game Engine Design and Implementation” probably are more interested in rolling their own engine.

That said, I still feel like the book was a worthwhile read and I did learn a little bit about some stuff and found it useful. Going in I had read the reviews on Amazon, and I knew the author was going to jump around with different libraries. Had I not known this I may have been more upset. As is, Alan Thorn is a competent writer and clearly knows a thing or two about game engines. I guess I just wish there was more of a focus on creating something cohesive and original and not just a jumble of introductions into different APIs. However, if you are on a journey (like me) of creating a 3D game engine you will need as much ammo as possible and this book certainly has a place in the arsenal. Just not the first place.