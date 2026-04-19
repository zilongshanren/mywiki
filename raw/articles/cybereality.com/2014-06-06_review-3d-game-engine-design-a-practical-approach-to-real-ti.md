---
title: 'Review: 3D Game Engine Design: A Practical Approach to Real-Time Computer
  Graphics by David H. Eberly'
url: https://cybereality.com/review-3d-game-engine-design-a-practical-approach-to-real-time-computer-graphics-by-david-h-eberly/
author: Cybereality
published: '2014-06-06'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![3D Game Engine Design](../../assets/f69a818d5c039a1e.jpg)


3D Game Engine Design: A Practical Approach to Real-Time Computer Graphics by David H. Eberly was an quite a read, at slightly over 1,000 pages. However, after a few chapters in I was already getting fatigued and I really had to push my way to the end. That’s not to say that the book was bad, it was not, however it was nothing like what I expected. Let me explain.

Imagine you walk into a restaurant and sit down with a friend. After several minutes of thought, you decide to order a steak. The waiter comes, takes your order, and about 15 minutes later returns with a plate. Except when you go to eat, you realize he has brought you a grilled chicken instead. It’s not that grilled chicken tastes bad, it’s just not what you ordered. I feel the same way about this book. The title says: 3D Game Engine Design: A Practical Approach to Real-Time Computer Graphics, however there is very little to no design in the book, it’s not very practical, and there is not much coverage of computer graphics itself.

But at 1,000+ pages there must be some information in there, and indeed there is. However, it is almost 99% math. I don’t have a problem with math. What I do have a problem with is pages and pages of mathematical proofs, when an explanation of an algorithm would have sufficed. The math is just really heavy, and made even harder to follow due to formatting errors on the Kindle e-book. For example, some symbols would be replaced by squares, making them almost impossible to decipher. In addition, most of the equations and formula were images, but some were too small to read and difficult to click on. Again, making it hard to follow. For a technical book this is all but unacceptable, and makes it next to useless to base an implementation on. I found many times I was reading 2 or 3 pages into a proof and I just would forget what the formula was even calculating. It’s not that I am slow. I have read other 3D math books and had a good time. The explanations here are just somewhat lacking and dry.

The main gripe I have is that the design of a game engine is nowhere to be found. You would expect overviews of class structures, game loops, how to communicate between objects, event systems, scene graphs, encapsulation of graphical APIs, input abstraction, etc. Nope, not here. It’s not even until the end of the book, in chapter 18, that he even mentions OOP. Most of that chapter is general OOP concepts (that you expect anyone that made it that far into a book like this already knows) and at the end sub-chapter the author goes into some topics that I would consider game engine design focused.

Fine, but surely there is something to like. I will say that the coverage of certain aspects of core math of an engine were covered in-depth. Specifically, bounding volumes, collision/intersection detection, and distance testing were given good coverage. Just looking at the table of contents is deceiving because it appears that much more is covered. For example, there is a chapter on physics, yet it is only about 20 pages and is not very helpful at all. Only in the last chapter was really any graphical concepts covered and, again, it was brief and only scratched the surface.

I’m not sure what David Eberly, the author, is trying to do here. This is the second book of his I read, and I had the same complaints about that. The book was mislabeled and deceptive. Had he just titled it “Game Engine Mathematics” I would have been a lot happier. Granted, I may have purchased the book anyway, but at least I would have known what I was getting into. I wanted a design book, I purchased what I thought was a design book, and all I got were a bunch of mathematical proofs. Sorry, I am disappointed.

If you are looking to do research on 3D math then there are better, more approachable, books out there. See 3D Math Primer for Graphics and Game Development, by Fletcher Dunn and Ian Parberry or Mathematics for 3D Game Programming and Computer Graphics, by Eric Lengyel. If you want a game engine design book then Game Engine Architecture by Jason Gregory has a great overview and 3D Game Engine Programming by Stefan Zerbst is better for implementation. Honestly, there could be more books in this field. Unfortunately, 3D Game Engine Design doesn’t fill it’s own shoes.