---
title: The Four Horsemen of the Performance Apocalypse
url: http://hacksoflife.blogspot.com/2015/01/the-four-horsemen-of-performance.html
author: Benjamin Supnik
published: '2015-01-31'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In my


That's a strong claim to make, particularly given how many very smart people are saying things like "profile first, optimize later" (which is better, I guess, than "write code, don't profile, randomly try to make it faster by poking it with a stick"). So I want to make the case that there are specific factors which hurt performance, and that they actually tend to get settled a lot earlier in the process of writing software than we might think.


I am also trying to come up with enough pithy quotes and catchily-named coding ideas that, when I become unemployable due to my ever-spreading gray-hair, I will be able to write some kind of book of coding wisdom and transition into a career of tech punditry. I have already figured out how to make 3-d transitions in Keynote!






Stupid examples:



When it comes to unnecessary work, think bigger than algorithmic efficiency:




[previous post](http://hacksoflife.blogspot.com/2015/01/high-performance-code-is-designed-not.html), I made the claim that really high performance software is designed to be high performance, and that a two-step process of writing code without consideration of performance and then trying to "fix it later" (guided by performance tools to show you the worst performance problems) would not work.That's a strong claim to make, particularly given how many very smart people are saying things like "profile first, optimize later" (which is better, I guess, than "write code, don't profile, randomly try to make it faster by poking it with a stick"). So I want to make the case that there are specific factors which hurt performance, and that they actually tend to get settled a lot earlier in the process of writing software than we might think.

I am also trying to come up with enough pithy quotes and catchily-named coding ideas that, when I become unemployable due to my ever-spreading gray-hair, I will be able to write some kind of book of coding wisdom and transition into a career of tech punditry. I have already figured out how to make 3-d transitions in Keynote!

### When Does Performance Matter

We all know that 100% of our software does not need to be optimized. So let me be clear about the scope where these ideas apply: sometimes (perhaps often) software's performance matters to its functionality.

- When you open an application, how long do you have to wait before the application is ready for you to use?
- When you interact with an editor, how long does it take for the editor to respond to each edit? Does the UI feel slow and unresponsive due to this speed? If you hit undo, do you have to wait while the undo takes place? Do you lose track of what you were doing because it took so long?
- When you scroll around a document, is the scrolling smooth and fluid, or can you see the screen refreshing only 2 times a second? Does it feel like "work" to move the document because tracking your scroll motion is so unresponsive?

If your dialog box opens in 30 ms, I don't care. It might be really lame that a dialog box takes 30 ms on a 3 ghz machine to appear, but opening a dialog box isn't a hard problem. But there are plenty of things we do with computers where performance absolutely does matter. It may be necessary to make the user experience pleasant, or it may be necessary to allow a user to reach their full potential creativity while using your program, or it may matter for allowing your application to run on a wider range of hardware (e.g. mobile phones).

So as we proceed, think about parts of your code base where performance scalability does matter. If it's a source control program, how fast is it to change branches? If it's a flight simulator, how many 3-d buildings can you show in a city? If it's an audio program, how many audio tracks and edits can a user make and still play back the composition? If it's a lego modeling program, how many lego bricks can the user add to a creation?

### Meet the Four Horsemen

Now that we know that we're working on some kind of "core" problem and not the UI code for preferences, let's meet the

**four horsemen of the performance apocalypse**. It looks like Google returns zero search results for that query, so on with the punditry! I really only have three horsemen and a qualifying statement, but "pithy" has to trump "accuracy" if we're going to get anywhere.
The four horsemen are:

- Doing Unnecessary Work.
- Ignoring constant time inefficiencies.
- Unnecessary generalization.
- Compound Interest.

### 1. Doing Unnecessary Work

The first way to have slow code instead of high performance code is to**do unnecessary work**. All of that[big-O notation](http://en.wikipedia.org/wiki/Big_O_notation)("your sort algorithm is O(N^2), dumbass") falls into this bucket. If your code is going to be high performance, it needs to do what needs to be done but not more than what needs to be done.Stupid examples:

- When your application has to re-draw a table, does it fetch data for the entire table instead of just the part of the table the user can see? Those extra fetches are unnecessary!
- When a value is computed and used over and over, do you save the computation or just re-compute from scratch each time? All but the first computation might be unnecessary.
- When you draw with OpenGL, do you change OpenGL state between draws even though the state you need is already the current state? Those "redundant" state change are unnecessary, and the massive thrash inside the driver that is caused by this is definitely unnecessary.
- When your editor program edits a large number of items in a document, do you update the UI for every item, or just once at the end? If the former, then all but the last UI update might be unnecessary.

When it comes to unnecessary work, think bigger than algorithmic efficiency:

- In your game, do you need to shade the terrain using the GPU? Or could you have shaded the terrain ahead of time and saved the shading to disk? If so, all of that shading is unnecessary! "Ahead of time" is often the best time to do work.
- In your racing game, do you need houses everywhere on the level, or only really close to the track where the driver can see them? If you put houses everywhere, the work spent to load them from disk, cull them, and possibly render them is all unnecessary.

Is avoiding unnecessary work something that we can save until the end of the development process? Clearly the answer is



Paying attention to constant time is all the rage now - if you've heard




The string map< occurs 588 times in the WED code base. set< occurs 822 times! Approximately 100% of this code is running a lot slower than it could be. This performance problem is the cumulative result of using slow-constant-time coding techniques for years.


So if we're going to avoid slow constant time techniques, we need to figure out what is inefficient and find an efficient replacement. And we need to do this early on, so that we can use the right idiom in our code, not the wrong one. This doesn't sound like something that can be done after coding is complete, in a late-stage optimization pass.



Unnecessary generalization is using an algorithm to take the intersection of two arbitrary polygons with holes when all we really want to do is clip a triangle against an axis-aligned bounding box.


Unnecessary generalization is making a "drawing" function that draws a universal triangle (a triangle with color, texture and position) and then making every single part of the application use that canonical call.


Unnecessary generalization is when your selected solution to a problem doesn't fit the problem like a glove.


Unnecessary generalization can come in the form of a "simplifying abstraction". WorldEditor redraws the


There are lots of ways to create overly general code:



Can we fix overly general code after the fact? Probably not without a rewrite. When the general code is in the form of an interface (the drawing module's interface is "I will draw one textured triangle") then huge amounts of code can require a serious rewrite to fix the problem.



Compounding is why a 1% fee is a big deal in finance and why a


You can say "oh, well, if anything's



Good performance comes from keeping multiple performance problems from compounding. Look at our sources of poor performance:



In



**no**. Avoiding unnecessary work is about determining how your program solves a user's problem and about selecting the algorithms and design constraints under which you will do this. This is stuff you do early in the design process!### 2. Ignoring Constant Time Inefficiencies

Avoiding unnecessary work is critical to good performance, but there will be some work your program must do, and when your program computes, it needs to not totally suck in the process. Algorithms often discuss the relationship between input data size and compute time (Big-O notation) but the constant factor - how fast each item is processed - really matters.Paying attention to constant time is all the rage now - if you've heard

[Mike Acton](https://www.youtube.com/watch?v=rX0ItVEVjHc)ranting about inefficient node-based game engines or

[Chandler Carruth](https://www.youtube.com/watch?v=fHNmRkzxHWs)telling you to stop using std::map, you've heard discussion of constant-time factors. Examples of constant-time fail:

- Dynamically allocating data with malloc when it could be stored statically (on-stack, globally, or in-class).
- Using std::map when a sorted std::vector will work. The map has terrible locality and has to call malloc a gajillion times.
- Using virtual functions when static free functions or inline functions would do.
- Using dynamic_cast when static cast would work.
- Using memory structures that have poor cache locality.

- The gap between CPU and memory performance is widening, so the "little" things aren't so little anymore. If a cache miss to main memory takes 300 cycles while the L1 cache takes 3 cycles, then the "constant" in the constant time factor of cache locality is 100x!!!!!
- Some of the constant time factors that are not so bad on desktop (where we have super-high performance chips that do aggressive things to hide latency) are still quite bad on consoles. I experienced this myself when working on mobile: the sloppy code I would barf out on desktop would run "okay" on a Mac Pro but would run terribly on an iPhone 4S.

*same*set of tools for most of the code we write. The result is that slow constant time techniques tend to get into 100% of our code; ripping out a slow constant time technique and fixing it isn't a matter of a "hot spot" - it can be a complete app rewrite.

The string map< occurs 588 times in the WED code base. set< occurs 822 times! Approximately 100% of this code is running a lot slower than it could be. This performance problem is the cumulative result of using slow-constant-time coding techniques for years.

So if we're going to avoid slow constant time techniques, we need to figure out what is inefficient and find an efficient replacement. And we need to do this early on, so that we can use the right idiom in our code, not the wrong one. This doesn't sound like something that can be done after coding is complete, in a late-stage optimization pass.

#### 3. The Weight Of Unnecessary Generalization

We're programmers. We generalize things; it's just what we do. But when we generalize code unnecessarily, performance goes out the window.Unnecessary generalization is using an algorithm to take the intersection of two arbitrary polygons with holes when all we really want to do is clip a triangle against an axis-aligned bounding box.

Unnecessary generalization is making a "drawing" function that draws a universal triangle (a triangle with color, texture and position) and then making every single part of the application use that canonical call.

Unnecessary generalization is when your selected solution to a problem doesn't fit the problem like a glove.

Unnecessary generalization can come in the form of a "simplifying abstraction". WorldEditor redraws the

*entire*screen when

*any*part of the screen needs redrawing. This is a simplifying abstraction - none of the code needs to worry about keeping track of dirty regions or invalidating the right parts of the screen. We solve the general problem of filling the whole screen instead of the specific (but more complex) problem of filling in specific areas. You can see the performance problem here: the general form of the problem does unnecessary work because the optimization we could have taken with the specific version of the problem is lost.

There are lots of ways to create overly general code:

- Using an overly general solution to a specific problem. The programmer thinks he or she is making the code "future proof", but really the programmer is simply making Mike Acton even more grumpy.
- Solving a simpler problem that is more computationally expensive.
- Applying simplifying (but performance-expensive) abstractions between parts of the program that make the direct expression of specific solutions impossible.

*hard to fix*after the fact. Once you have an abstraction in place,

*lots of code*ends up being written in terms of that abstraction. Getting rid of the abstraction can mean a huge rewrite.

Can we fix overly general code after the fact? Probably not without a rewrite. When the general code is in the form of an interface (the drawing module's interface is "I will draw one textured triangle") then huge amounts of code can require a serious rewrite to fix the problem.

### 4. Compound Interest

This is the last and most important problem: performance problems**compound**. If you have three generalizations and each makes your code run 25% slower, your code is now

*almost twice*as slow as without them. Generalizations weigh down on top of constant time penalties, and that slow code then has to plow through too much data. It's easy to dismiss all of these problems (doing more work than necessary, slow constant-time factors, and unnecessary generalization) because any

*one*of these things might not be that bad.

Compounding is why a 1% fee is a big deal in finance and why a

[1% performance gain or loss](http://hacksoflife.blogspot.com/2010/11/is-1-lot.html)is a big deal for driver writers.

You can say "oh, well, if anything's

*really*bad I'll pick it off with a profiler and fix it". But because of compounding, your code might be slow due to a large number of small factors, and it might be a lot of coding to fix them all. (This is the dreaded "uniformly slow code" case where every function takes 1% of CPU and you have to make one hundred separate performance optimizations to improve performance at all.)

### Good Performance Comes From Design

This brings me to the point I originally wanted to make about Knuth and premature optimization before Joshua beat me to it: if a program has good performance, it is because somebody*designed*it to be that way.

Good performance comes from keeping multiple performance problems from compounding. Look at our sources of poor performance:

- Doing unnecessary work. This has to get fixed at algorithm design time and even product definition time. If you have the wrong algorithm, that's a bad design choice.
- Using slow coding idioms. This permeates
*all*of your code, so rewriting with faster technique later is going to be expensive. - Including generalizations that are unaffordable and unnecessary. Once you depend on the abstractions and generalizations, removing them are painful.

In

[Knuth's original paper](http://web.archive.org/web/20130731202547/http://pplab.snu.ac.kr/courses/adv_pl05/papers/p261-knuth.pdf)he suggests:

that all compilers written from now on should be designed to provide all programmers with feedback indicating what parts of their programs are costing the most; indeed, this feedback should be supplied automatically unless it has been specifically turned off.But this isn't enough. It's not enough to measure how fast code is, and then change it. To make a program meet it's performance guidelines you need to

*design*for performance.

- Understand the size of your data sets and the scope of the computation needed; select an algorithm that can solve the problem within resources.
- Pick coding idioms that will implement that algorithm "on budget".
- Add only abstractions that add value and don't penalize your performance target.

Well written, sir. Especially #4, which is really easy to overlook!

ReplyDeleteThough I'd say that the most important design decision is to make software that is un-generalizable, e.g. something like C++ template specialization in a broader sense.

Because the truth is, first and the most important 90% of the code is for developers to learn what works and what not, and it's very easy to narrow possibilities too early in the process.