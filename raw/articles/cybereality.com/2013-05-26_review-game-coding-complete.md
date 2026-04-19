---
title: 'Review: Game Coding Complete'
url: https://cybereality.com/review-game-coding-complete/
author: Cybereality
published: '2013-05-26'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![Game Coding Complete](../../assets/3ead772e562c12ff.jpg)


Finally, I’ve got around to reading (and finishing) Game Coding Complete, and it’s up there on the list of great game development resources. I’d been meaning to read this book for quite some time, but got distracted with DirectX and Windows hooking for use with my 3D driver. Now that I’m back on the 3D engine kick, it seems like a good time to hit this book. Reading through this, I was thoroughly impressed by the content and the writing style. Don’t be discouraged by the lengthy size, this text is well worth the time to read.

The authors, both seasoned game developers, working on the Ultima series and various Sims games, have a lot of collective knowledge and it comes through in the book. There are a lot of snippets and stories about things the went right (or wrong) on the production of some of the games they worked on. I found these insights to be refreshing, and certainly interesting to read about. It also helps to teach people what professional game development is like, and things to expect if you are looking for a job in the industry.

Aside from the stories, there is a lot of topics covered in the book. They go over game loops, component architecture, process system, an event system, 3D math, DirectX, audio, collision and physics, scripting with Lua, AI, a game editor in C#, debugging, version control, multi-threading, etc. Really almost everything you would need to know. They weren’t joking when they said “Complete.” Although the book is long, it’s really amazing what they managed to cram in there. Granted, most topics only get one chapter, which isn’t really enough to fully cover everything. But it’s a great overview on a ton of stuff.

I found the coverage of the event and process system to be every insightful, and I will probably be using a variation of these in my own engine. The event system basically allows different objects to fire events at key points, and then have other objects respond without tight coupling. The process system allows objects to spawn logic loops, that will be updated along with the rest of the engine. So, for example, the player can hit a key to throw a grenade. That would fire an event, which would spawn a grenade with the proper velocity. The grenade itself would have a process, that would count down a few seconds and then explode. At the time of explosion, this could fire another event, which would then cause the audio system to play a sound and the particle engine to create a visual effect. This is a very clean way of handling events and processes, and this is probably the single more useful thing I found in the text.

If you are looking at creating your own game or engine, or just want to see what goes into a commercial title, Game Coding Complete may be one of the best resources to do so. While there is a good amount of C++ code in the book, it is not so much of a “cookbook”, it is more of an overview of architecture. The writing style is casual and friendly, and I really love all the stories told throughout the book. This is a great resource, and should not be missed. My only regret is that I did not read this book sooner. Highly recommended.