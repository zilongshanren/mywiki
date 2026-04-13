---
title: Building your mental toolbox for solving coding problems
url: http://joostdevblog.blogspot.com/2015/07/building-your-mental-toolbox-for.html
author: Joost van Dongen
published: '2015-07-19'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*mental toolbox*, your own personal set of approaches and techniques to help your mind tackle topics that are too complex to otherwise solve.

By "mental toolbox" I basically just mean a bunch of tricks to help you think. Such tricks are very personal: what works for one person might not work for someone else. The important thing is to try different approaches and find out what works for you. In today's post I would like to share my own tricks, hoping some of these can help others as well.

**Make schemes**

Don't try to create an overview in your head, do it on paper! Draw flowcharts, timelines, mindmaps, UML diagrams, lists, relationship graphs or whatever else that might help you see the entire problem, or see the problem in a different light.

![](../../assets/66de2cfba6dda49e.jpg)

**Write down**

*all*your thoughtsThis is my most personal trick, as I have never heard of anyone else who does this, but it is also my best one. Whenever I am truly stuck I fall back to writing down all my thoughts.

To me the biggest problem when trying to solve something is that at some point my mind grinds to a halt as it tries to hold too many thoughts at once, leaving no room for new ones. This is a common thing in humans: in psychology it is called "

[The Magical Number Seven, Plus or Minus Two](https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two)", stating that the average human can hold 7 ± 2 objects in working memory. The problem is that as soon as I have a bunch of thoughts that I think are interesting, I try to remember them and lose the capacity to come up with new ones.

My solution is to just write down

*all*my thoughts, including the bad ones. For a complex problem I might scribble an entire A4 full of miniscule notes. For half of those I realise they are irrelevant before I even finish writing them down, but this doesn't matter. The only point is to clear my mind: whatever is on the paper doesn't have to be remembered, so there is room for new thoughts. Letting my mind ramble on and writing it all down often leads me to a solution. This is by far the strongest tool in my box.

**Split the problem into smaller pieces**

If a problem is really big it might help to just ignore half of it and only solve the other half. Often the parts of a problem depend on each other and trying to figure out the dependencies might be what makes the problem too complex to solve. Try solving only one part while ignoring everything else. Only once the part is solved, try to figure out how to make it work with the rest of the problem.

![](../../assets/518931b157f5741a.jpg)

*(More info in*

[this blogpost on AI movement in Awesomenauts)](http://joostdevblog.blogspot.nl/2014/06/solving-path-finding-and-movement-in-2d.html)**Try different angles**

It can help to force yourself to try a completely different angle, sometimes to even try angles that might seem ridiculous at first. A good example is randomness: if you can't find an exact solution, you might try to generate random solutions and choose the best one. This is rarely the best approach, but looking at it from an angle like that might generate new ideas. For example, this particular approach makes you think about how to compare random results to figure out which is best. The algorithm for comparing results might be the starting point of a real solution. The goal is to force yourself to let go of your current line of thought and try completely different angles.

**Just start coding**

Sometimes you already have some ideas on how to tackle parts of a problem, but not the rest of it. In this case it might help to just start coding. The code you write will probably end up being thrown away once you figure out the real solution. This is fine: the goal is to turn general ideas into concrete code so that you understand it better. When using this approach be sure to throw away the garbage code afterwards!

**Leave markers to avoid being sidetracked**

Often while programming something complex I come up with additional problems that I will also need to solve, or edge cases that need to be handled. Doing those all at once makes me lose focus, but I don't want to ignore them either, because I might not remember them later on. So whenever I think of something, I leave a small comment in my code as a reminder and leave it at that, allowing me to keep my focus on one thing at a time. To be able to find those comments quickly once the core code is finished, I add the letters "

[QQQ](http://joostdevblog.blogspot.nl/2011/12/qqq.html)" to them.

**The internet**

Caption Obvious would like to mention that you can search online for solutions.

**Ask for help**

Surprisingly, quit a lot of programmers would rather be stuck on something for days than ask for help. I have supervised a ton of interns and quite often they keep chewing on a problem without real progress for way too long before asking for help. Asking a question online seems to have a similar barrier. There is no shame in looking for help or discussing a problem with someone else, and often just explaining the problem to someone else clears up the mind enough that you figure out a solution yourself.

**Ignore performance and requirements**

Often it is easier to solve a problem in an inefficient way than in an efficient way. Letting go of performance requirements is a great way to open your mind to solutions. Often an efficient solution is just a clever variation on an inefficient one.

The same goes for requirements. If you are stuck, let go of all the additional requirements and first try to solve only the core problem. Then try to adapt your solution to those requirements.

![](../../assets/f7734a190d1cf568.jpg)

**Know lots of programming patterns**

I often struggle with finding a really good class structure to make my code as clear and maintainable as possible. For such situations it helps to know a lot of design patterns. Design patterns are common structures that can be applied to specific problems. There is an enormous amount of design patterns and the more you know, the better. Wikipedia has

[a nice overview](https://en.wikipedia.org/wiki/Software_design_pattern), including well-known ones like Observer, Factory, Singleton and Strategy.

**Know lots of algorithmic techniques**

Many problems are completely different, but can be solved in similar ways. Often you can find a solution by trying approaches you have seen in other algorithms. The more approaches you have seen, the larger the chance you know something suitable. Here are a bunch of categories of solutions of which it is good to have seen a couple of examples of algorithms that use each approach:

- Recursive algorithms
- Heuristics (or: approximate solutions versus exact solutions)
- Greedy algorithms
- Dynamic programming algorithms
- Iterative improvement (running the same algorithm over and over again to improve the result with each run)
- Smaller steps (splitting a simulation into smaller steps instead of once with a big step, like in
[this collision trick](http://joostdevblog.blogspot.nl/2010/10/dirty-collision-detection-trickery-in.html)I used in[Proun](http://www.proun-game.com/)) - Monte Carlo versus Las Vegas algorithms

**Take your mind off the problem**

If all else fails you can choose to simply leave the problem be for a day or two and work on something else. A solution might pop up when least expected. Under the shower, while cycling or taking a walk. I personally get lots of good ideas on the toilet... Key to this approach is to allow your mind to wander. Don't fill every waking minute of your day with entertainment/work as your mind would be too occupied for new thoughts.

Your mental toolbox is something you can improve and work on. You can experiment with new approaches and ask others what theirs are. Give all kinds of things a try, and see what works for you.

What are your tricks for solving complex problems?

Often when I have to find a solution to a problem i cannot come up with immediately, I go to the toilet. When coming back, I often have the fix, hihi.

ReplyDeleteYou mentioned the wiki for programming patterns, which is great. This is another excellent reference, with games and "ease of reference" in mind: http://gameprogrammingpatterns.com/ (it's like an online book)

ReplyDeleteThat sounds like a great book, I'll have a look, might be something I should read. :)

DeleteRegarding algorithms, Tomasz Wegaznowski once posted about his data processing toolkit.

ReplyDeleteNice blog post again Joost, I have really enjoyed the content on here over the last couple of years. Hope you can keep it up a few more :)

ReplyDelete