---
title: Solve Less General Problems
url: http://hacksoflife.blogspot.com/2018/08/solve-less-general-problems.html
author: Benjamin Supnik
published: '2018-08-11'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Two decades ago when I first started working at Avid, one of the tasks I was assigned was porting our product (a consumer video editor - think iMovie before it was cool) from the PCI-card-based video capture we first shipped with to digital video vie 1394/Firewire.


Being the fresh-out-of-school programmer was, I looked at this and said "what we need is a hardware abstraction layer!" I dutifully designed and wrote a HAL and parameterized more or less everything so that the product could potentially use


This seemed at the time like really good design, and it did get the job done - we finished DV support.


After we shipped DV support, the product was canceled, I was moved to a different group, and the HAL was never used again.


In case it is not obvious from this story:




There's been plenty of written by lots of software developers about not 'future-proofing' a design speculatively. The short version is that it's more valuable to have a smaller design that's easy to refactor than to have a larger design with abstractions that you don't use; the abstractions are a maintenance tax.



In my next model I started learning from the school of hard knocks. I started with a templated data model ("hey, I'm going to reuse this and it'll be glorious") and about part way through recognized that I was being killed by an abstraction tax that wasn't paying me back. (At the time templates tended to crash the compiler, so going fully templated was really expensive.) I made the right decision, after trying all of the other ones first - very American.



Here's another way to put this: every solution has strengths and weaknesses. You're better off with a solution where the weaknesses are the part of the solution




Being the fresh-out-of-school programmer was, I looked at this and said "what we need is a hardware abstraction layer!" I dutifully designed and wrote a HAL and parameterized more or less everything so that the product could potentially use

*any*video input source we could come up with a plugin for.This seemed at the time like really good design, and it did get the job done - we finished DV support.

After we shipped DV support, the product was canceled, I was moved to a different group, and the HAL was never used again.

In case it is not obvious from this story:

- The decision to build a HAL was a totally stupid one. There was no indication in any of the product road maps that we had the legs to do a lot of video formats.
- The fully generalized HAL design had a much larger scope than parameterizing only the stuff that actually had to change for DV.
- We never were able to leverage any of the theoretical upsides of generalizing the problem.
- I'm pretty embarrassed by the entire thing - especially the part where I told my engineering manager about how great this was going to be.

There's been plenty of written by lots of software developers about not 'future-proofing' a design speculatively. The short version is that it's more valuable to have a smaller design that's easy to refactor than to have a larger design with abstractions that you don't use; the abstractions are a maintenance tax.

### It's Okay To Be Less General

One way I view my growth as a programmer over the last two decades is by tracking my becoming okay with being less general. At the time I wrote the HAL, if someone more senior had told me "just go special-case DV", I almost certainly would have explained how this was terrible design, and probably have gone and pouted about it if required to do the fast thing. I certainly wouldn't have appreciated the value to the business of getting the feature done in a fraction of the time.In my next model I started learning from the school of hard knocks. I started with a templated data model ("hey, I'm going to reuse this and it'll be glorious") and about part way through recognized that I was being killed by an abstraction tax that wasn't paying me back. (At the time templates tended to crash the compiler, so going fully templated was really expensive.) I made the right decision, after trying all of the other ones first - very American.

### Being Less General Makes the Problem Solvable

I wrote[about this previously](http://hacksoflife.blogspot.com/2016/01/work-stealing-and-lock-free-chaos.html), but Fedor Pikus is pretty much saying the same thing - in the very hard problem of lock-free programming, a fully general design might be impossible. Better to do something more specific to your design and have it actually work.Here's another way to put this: every solution has strengths and weaknesses. You're better off with a solution where the weaknesses are the part of the solution

*you don't need*.### Don't Solve Every Problem

Turns out[Mike Acton](https://www.youtube.com/watch?v=rX0ItVEVjHc)is kind of saying the same thing. The mantra of the Data-Oriented-Design nerds is "know your data". The idea here is to solve the*specific*problem that your*specific*data presents. Don't come up with a general solution that works for your data and other data that your program will literally never see. General solutions are more expensive to develop and probably have down-sides you don't need to pay for.### Better to Not Leak

I haven't had a stupid pithy quote on the blog in a while, so here's some parental wisdom: it's better not to leak.Prefer specific solutions that don't leak to general but leaky abstractions.It can be hard to make a really general non-leaky abstraction. Better to solve a more specific problem and plug the leaks in the areas that really matter.

YAGNI prevails! :)


ReplyDeleteThis reminds me of Chandler Carruth's talk on efficient data structures (https://www.youtube.com/watch?v=vElZc6zSIXM), where he mentions that the issues with a lot of the C++ std data structures stem from having a bad *spec* in terms of iterator invalidation rules, memory allocations, and so on. Those rules might surely be useful in some really specific scenarios, but for the rest of the world, it's just a tax you pay at runtime. (Carruth's solution is, of course, to have less general but faster data structures for use in the 99% of cases where you don't need the extra guarantees.)

This is true from the other side too: if your work applies to a lot of things, it is not too useful.

ReplyDeletePartially related to the YAGNI principle as well.


ReplyDeleteThanks for the article.

The correct meaning of a general solution is not to have support for everything under the sun, like in this case not every playable format. The true meaning of a general solution is to build composable structures that can come together to build more and more complicated abstraction to fit any solution. In this case any playable format could in theory be build if need be.

ReplyDeleteIf it is bad for you why does it feel so good? Is it possible that if you keep designing HALs you will eventually figure out how to do it in a way that is robust?

ReplyDeleteThanks! This is great advice. I've run down this path before and it's good to hear someone articulate the problem.

ReplyDelete