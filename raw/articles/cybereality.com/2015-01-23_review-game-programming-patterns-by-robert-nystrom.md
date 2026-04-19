---
title: 'Review: Game Programming Patterns by Robert Nystrom'
url: https://cybereality.com/review-game-programming-patterns-by-robert-nystrom/
author: Cybereality
published: '2015-01-23'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![Game Patterns](../../assets/643e8c01a5fe02c2.jpg)


I will start by saying this book is game programming GOLD! Whether you are a pro or a novice looking to learn, this book deserves to place on your shelf (or I guess in memory if you buy the e-book). While some of the chapters may seem like obvious things for people that have programmed games before, I think even advanced coders will discover a few things they didn’t know.

So let me talk about what this book is. Basically it covers common challenges in game programming and some useful ways of resolving the problem. Though the theme of the book is game development, a lot of this stuff is applicable to any sort of visual or object-oriented programming. Nystrom starts by revisiting the classic design patterns popularized by the seminal book by the “gang of four” in 1994. Surprisingly, 20 years later a lot of those ideas still hold up. Next he moves onto more game specific topics like double buffering (not just for graphics), a game loop, and updating objects. Then he goes into bytecode (really a simple compiler), components, event queues, singletons, object pools, dirty flag and spatial partitioning. It’s actually not the longest book out there at 354 pages, but this is a breathe of fresh air after persevering through The C++ Programming Language (which was great, just very long). The author does not waste pages, though. There are nuggets of knowledge littered throughout the text.

One thing I like is how the book is not tied to a particular API or library. The pseudo-code is in C++, but really you could implement the ideas in almost any language. He even goes as far as not using the STL (for example, rolling his own linked list for a few examples). In a real application, you would probably not want to reinvent the wheel for basic containers, but it’s nice that the examples stand alone without any nasty dependencies. I could see a lot of the code here being copied into a real game and being usable with only minor additions. Well, of course you have to modify for your platform or engine or whatever, but the concepts are solid.

Another point is that this makes design patterns concrete (please, no abstract class jokes…). I read the original Design Patterns book years ago but some of the patterns never made sense to me. They were too abstract and, though interesting, sometimes didn’t click for me. This book, on the other hand, clicked the whole way through. Everything made sense, and was immediately clear why it was useful. Sure, I’ve probably learned a lot in the past few years, making Game Programming Patterns more approachable. But I think almost any game coder (or aspiring coder) could get value from this book. I’d give it 5 stars, 10 out of 10, 2 thumbs up, and definite “buy it now.”