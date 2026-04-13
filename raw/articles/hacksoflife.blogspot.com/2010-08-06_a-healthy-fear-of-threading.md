---
title: A Healthy Fear of Threading
url: http://hacksoflife.blogspot.com/2010/08/healthy-fear-of-threading.html
author: Benjamin Supnik
published: '2010-08-06'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

There are only two kinds of programmers: programmers with a healthy fear of threaded code and programmers who should fear code.Now I'm not saying "never thread". I'm just saying "you better be getting something good for that threading, because it's driving up your development costs."

In particular, the effective execution order of threaded code can change with every run, and there is no guarantee that you have seen every combination of execution order by running your program a finite number of times.

Thus methods of checking your code quality by running your program (perhaps many times) won't detect bugs in threaded code. You may not find out until that user with one more core and a background program chewing up cycles hits an execution order that you haven't seen yet.

Instead for threaded code you have to prove logically that the execution order constraints applied (via locking, etc.) create a bounded set of execution combinations, and that each one is correct. This isn't quick or easy to do.

One way we cope with this development cost in X-Plane (where we need to use threads to fully utilize multiple cores) is to use threading design patterns with known execution limits. The most common one is a message queue, where ownership of data access flows with the message down a queue. This idiom not only guarantees serialized access to data without locks, but the implementation in C++ tends to make errors rare; if you have the message you have the pointer, and thus you have rights on the data. If you don't have the message, you have nothing to dereference.

## No comments:

## Post a Comment