---
title: Optimisation lessons learned (part 1)
url: http://joostdevblog.blogspot.com/2012/07/optimisation-lessons-learned-part-1.html
author: Joost van Dongen
published: '2012-07-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers](http://www.swordsandsoldiers.com)for the Wii, I had never done any optimisation. At university I had already learned a lot about time complexity (big O notation, like

*O(n)*), but optimising an actual game with a big codebase is a different beast entirely. I was like a virgin that had never been seduced by a handsome profiler yet.

I just started fooling around with optimisations, reading tutorials and articles on Nintendo's dev website and the internet in general, and learning as I went along. Since no pro ever taught me how to optimise, I guess I might still be unaware of some really important tricks. Yet somehow I managed to get Swords & Soldiers from an initial 10fps to 100fps on the Wii (if VSync is turned off), and

[Awesomenauts](http://www.awesomenauts.com)from 10fps to 70fps on the Playstation 3.

In past five years I spent some six months in total on several kinds of optimisation. Quite a lot of that was on bandwidth optimisations, but also a lot on framerate and loading-times optimisations, so I have quite a bit of experience with it by now. There is a lot of interesting stuff to say about it, so in the coming weeks I would like to share the most important lessons that I learned. Today's concepts are rather general, next week I will share some more detailed pieces of (hopefully) 'wisdom'. ^_^

**Don't make any assumptions**

This is by far the most important one. When I want to optimise something, I always have a some ideas in my head about which parts of the game must be causing the low framerates. In practice, however, it turns out that I am hardly ever right. When I fire up a profiler and analyse where time is really spent, the big optimisations almost always turn out to be somewhere else than expected. This is still the case, even though in the past five years I have spent so much time full-time on optimisation (especially Awesomenauts was a really complex beast to tame), optimising code for Wii, PS3, Xbox360 and PC. So much experience, yet my expectations are still usually wrong.

So the rule I derive from this, is to never take any action based on assumptions. Always let go of your assumptions. Take real measurements and work from there. And once something has been changed, measure again to see whether it really works. As Dutch physics teachers often say: "

*Meten is weten*" ("

*Measuring is knowing*").

**Profilers are awesome**

Which brings me to the best part: profilers (measuring tools) are awesome! They give insane amounts of detail on all kinds of things. The core for me is the hierarchical view. This starts in your main() function and tells you it is using 100% of the time (oh really...). From there you can keep opening function calls in a tree-like form, to see in ever more detail where the time is spent. Beyond this, profilers have all kinds of nifty tools. If you ever want to do any optimisation, be sure to start by getting a proper profiler!

![](../../assets/e96702213df0d3d7.gif)

I have to say, though, that I have not been able to find a really good, affordable profiler for PC. Wii, PS3 and Xbox360 all have excellent profilers that only work on that platform, but on PC, most profilers I have seen are either incredibly expensive (like the one in Visual Studio Team Edition), or lack the concept of a "frame" and thus don't allow me to find framerate hickups. The best one for PC I have seen so far is

[Very Sleepy](http://www.codersnotes.com/sleepy/), even though it completely destroys the framerate while running and doesn't know what a frame is either. But Very Sleepy is easy to use and the hierarchical tree-view is really clear. So if anyone has any recommendations for a better profiler for optimising games that are written in C++, then please let me know!

**Premature optimisation is the root of all evil**

I already mentioned that you should not make any assumptions, and this also leads to another important point. "

*Premature optimisation is the root of all evil*" is a quote from the famous computer scientist Donald Knuth, and it is all too true. Most optimisations make code more complex, more difficult to maintain and evolve, and more sensitive to bugs. Also, in practice, 99% of the code is completely irrelevant to performance. A couple of hotspots take up most of the CPU's time, and the rest just doesn't occur often enough to be relevant to optimise. So my conclusion is to not really care about performance and just write the cleanest, most readable code I can. Until the profiler says otherwise.

![](../../assets/8c0654d35e7b3a78.jpg)

To give a simple example from C++: sometimes using a

*const char**is a lot faster than an

*std::string*. However, the latter is so much safer to use, that I never use

*const char**until the profiler tells me I have a problem, and then I change it in that specific spot.

**Modern consoles are ridiculously fast**

When you look online for optimisation tips, or when you talk to hardened industry veterans, you will learn a lot of things that I dare claim are just not relevant any more. Consoles and PCs these days are so fast, that you can just waste performance on all kinds of things and still get a good framerate. Of course, I am not talking about the big games here: if you are working on the next Uncharted and need to squeeze every last bit of power out of the Playstation 3, then it probably becomes really important to look after every little performance detail, but in general: modern consoles are so fast that you can waste most of your processor time on inefficient code and still easily get a good framerate.

To give an example: a rule that some studios have is that dynamic allocations are forbidden. So calling

*new*or

*malloc*during gameplay is not allowed. Everything that is going to be used, must be allocated during loading, and then kept in pools for quick usage. This helps against memory fragmentation, but is also supposedly necessary to achieve a good framerate. I personally think this limits the code design way too much. It makes code more difficult to manage and extend during development, so I never do this. It turns out that even the Wii, supposedly the slowest of the current generation, can easily run 60fps with 100 characters walking around in Swords & Soldiers.

(Note that I did end up making my own memory manager to speed up allocations on the Wii, which I will discuss in a future blog post. But calling

*new*tons of times each frame was not a problem in the end.)

My point here is not that everything is always possible, but I do think it is important to realise that unless you are making a triple-A console game, you should not worry about performance too much, definitely not early in development.

![](../../assets/32953cafe4bbc07e.jpg)

I personally find optimisation a lot of fun to do, so there is a lot more I would like to say about it. Next week I will be a bit more specific and follow this post up with some lessons that I learned about timing, threading, hiccups, and where the biggest performance improvements can be made.

Good points. I do feel the need to say something about "premature optimisation is the root of all evil."



ReplyDeleteYou have to be careful with how you interpret it. I take it to say: be efficient with your development time. It kind of says: take the easy way out. But it doesn't say: be stupid and lazy. Spending time to do something well can be a correct investment. If you _know_ you're going to get into trouble, don't bother doing the bad code first. (But because of "Don't make any assumptions," this can be hard.) But lets say you _know_ your real game levels won't possibly fit in memory once they get made. Don't code yourself into a corner where you can't handle that. It'll be a pain in the ass to overhaul everything.

There's a saying attributed to Len Lattanzi: "Belated pessimization is the leaf of no good." That doesn't entirely make sense :P. But the message is this: don't fetishise the quick-and-dirty. Sometimes you'll save yourself a world of hurt by doing The Right Thing in the first place. That's mostly an architectural thing I guess, more so than low-level line-by-line optimisation.

You are right that too much of a good thing is not a good idea. In some cases you just know performance is going to be an issue, and principally ignoring that knowledge is not smart.


DeleteI think programming always needs to strike a certain balance between things like readability, bug-proof-ness, time spent coding, performance and flexibility. I just think that in this balance, performance is relatively unimportant, but definitely still a topic of importance.

I look forward to this series of posts. I've coded for scientific applications in the past, where optimization of every small detail can make the difference between a program running for one day vs. for one month. However, I'm now learning to code games and similar programs and I stop myself from premature optimization or wanting to optimize every last thing as I write it.


ReplyDeleteI hope these posts will help further break me of this habit!

I use Intel VTune Amplifier XE for profiling on Windows, though I used Very Sleepy for a long time as well. VTune interfaces directly with Visual Studio, and has an API for specifying frame swaps, naming threads, and so on.

ReplyDeleteI really liked this post! I'm kinda new to reading blogs, but I want to read more.. Are there any other blogs that have these kinds of topics about GameDevelopment/Programming?

ReplyDeleteAm I correct when saying you are only talking about cpu optimalisation in this post?




ReplyDeleteFor Windows gpu profiling I always use Nvidia PerfHUD. It works great but you will need a Nvidia card though. It is reason enough for me to get one though.

For cpu/code profiling I just use the buildin Unity profiler, which also works with mobile devices these days.

Looking forward to the next posts, hopefully you'll include some cases you came across while developing Awesomenauts as I'm curious to know what the general limiting factors are on consoles.

Keep up the good stuff!

I guess I am talking mainly about CPU profiling, but all the points I am making here are valid for GPUs as well. They too have great profilers and are so fast that you shouldn't care about performance too much. We had to do insane overdraw on Awesomenauts and Swords & Soldiers before the GPU became any kind of a problem, and there, too, we solved the problems after we encountered them, instead of planning for them too much. There's a bit about GPU performance in this previous blogpost:



Deletehttp://joostdevblog.blogspot.nl/2012/04/depth-of-field-blur-swiss-army-knife.html

As for limiting factors on consoles: the only one that really matters in my opinion is memory. Which makes me realise that that would make for an interesting future blog post! :)