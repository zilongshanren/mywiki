---
title: 'Review: Physics for Game Programmers by Grant Palmer'
url: https://cybereality.com/review-physics-for-game-programmers-by-grant-palmer/
author: Cybereality
published: '2014-09-01'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/0b9069ca91525e7f.jpg)


Today I will be reviewing Physics for Game Programmers by Grant Palmer, another stepping stone on my quest to build a custom physics engine. Overall I enjoyed reading the book, and I feel like I learned a lot of general things but not enough to base a physics implementation on. Please read on for more details.

What I found most interesting about this text was the explanations of certain aspects of physics that I had not seen covered before. I have already read about 3 or 4 different books all on game physics, and I was expecting this title to be more of a refresher than anything. However, I was surprised to find a lot of things I didn’t know about. In particular, the coverage of drag forces was extremely detailed including things like turbulent and laminar flow and the Reynolds number. Some of the topics covered include: Newtonian mechanics, kinematics, projectiles, collisions, sports simulation (golf, soccer, basketball), cars and motorcycles, boats, airplanes, rockets and missiles, explosions, and lasers. Quite a lot in a little under 500 pages.

There is certainly a breadth of knowledge living inside this book. It was undeniably an interesting read, and I felt like I learned a decent amount. However, I am not sure it really got me any closer to building the physics engine I have set out to create. Let me explain. While there are equations listed in the text, and some example code is given, it is mostly used to support the 2D sample applications. I am not sure there is much I could just pull from the book an paste into a 3D engine. The concepts are sound, and it wouldn’t be a huge stretch to make it work, it’s just not spelled out for you. To be fair, some topics are explained well, like his discussion on differential equations and drag forces among other things.

My main gripe with the book is that it did not really try to explain rigid-body dynamics at all. There are some interesting things talked about, like sports and boats and planes and all that. And certainly there are probably a ton of sports games and simulators that would benefit from that focus. For my purposes, I was looking more for a rigid or soft body solver, and how bodies can interact with each other. Unfortunately, that was not discussed at all.

It’s not that I want to get down on Physics for Game Programmers, and I think Grant Palmer did a great job within the scope of what he was trying to do. The book was entertaining and relevant, it just wasn’t a one-stop-shop for all your physics needs. However, it does cover some basic things well, and includes topics not even touched by some of the other books I’ve read. That alone would make it worth reading, just set your expectations correctly. Once you are ready to make an actual implementation, you will likely need to seek other books or papers. But I guess it is almost always the case as one book can rarely impart all the knowledge you need in any given topic. To sum up: I liked it but wanted more.