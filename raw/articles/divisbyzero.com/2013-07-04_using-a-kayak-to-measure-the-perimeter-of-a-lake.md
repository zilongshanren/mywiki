---
title: Using a kayak to measure the perimeter of a lake
url: https://divisbyzero.com/2013/07/04/using-a-kayak-to-measure-the-perimeter-of-a-lake/
author: Dave Richeson
published: '2013-07-04'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I’m on vacation this week on a lake in northern Michigan (hold up your right hand, palm toward you, point at the first knuckle of your middle finger—that’s where I am). Yesterday I paddled around the perimeter of the lake in a kayak. On a whim I brought my GPS-enabled phone. My route is shown below. Note that the cartographer didn’t do a perfect job—despite what you see, I can assure you that I paddled only on water.

![](../../assets/0c4c285b9cd2781d.png)


When I got back, the GPS said that I had paddled for 2.74 miles (14470 feet). Let’s say that I stayed exactly 50 feet off the shore for the entire trip. What is the perimeter of the lake?

We should probably make some assumptions about the shoreline and about my path. For simplicity, let’s say that my path is differentiable, that it bounds a region , and that the lake is the set

, where


is the *radius neighborhood of *. Intuitively, the boundary of

[The Mathematics of Doodling](http://math.stanford.edu/~vakil/files/monthly116-129-vakil.pdf)” for more about this set.)

You may not think you have enough information to solve the problem, but you do! The clue is found in a well-known puzzler. Suppose we have an electrical wire running round the equator of the earth. We want to get it up off the ground and put it at the top of 50-foot electrical poles. How much longer must the wire be? [If you haven’t seen this puzzler before, stop now and think about it.] If the radius of the Earth is feet, then the original wire must be

feet long. The new wire is a circle with a radius 50 feet longer than before, so its length must be

feet. That is, it must be

feet longer.


It turns out that this argument can be generalized in various ways (again, see Vakil’s article for more information). First of all, if is any convex set with a polygonal boundary, then, just like in the puzzle, the perimeter of

is

units longer than the perimeter of

. Vakil illustrates this with the picture below.


![](../../assets/b27c094699e27d7e.png)


It turns out that the exact same result holds if is nonconvex—such as the region enclosed by my kayak trip. As the kayak goes in coves and around peninsulas, the “extra” regions of convexity and nonconvexity cancel each other out. In the end it is the same as going around a circle one time. Thus the perimeter of the lake is

feet longer than my kayak path:

feet.


From the title of this post on twitter, I assumed this post was going to be about fractals: http://en.wikipedia.org/wiki/Coastline_paradox

And now I’m wanting to think about playing the doodling game with fractals (it really seems like something should break) — but, being in the UK, I will go to bed instead.

But, neat idea — I’d quickly read Ravi’s article, but hadn’t thought about “real world” application of it.

I guessed Houghton Lake, and google maps confirmed that Houghton Lake is about at the first knuckle on the middle finger. But it’s not the right shape. I searched all over the map and couldn’t find your lake. There seem to be at least 4 Little Bear Lakes in Michigan. Now I’ve found it. You must have meant the other first knuckle. Sounds like fun. I’m at Big Whitefish Lake (near Pierson). Maybe I should try kayaking around it. I think my trip would be about 4 miles long.

Paul, when I wrote my article “Centers of the United States” http://www.jstor.org/stable/30044887 I read about how the USGS used different length “rulers” to measure the “shoreline” and the “coastline” of a country (these are technical terms, precisely defined).

Sue—the one near Lewiston, MI. Hope you had a nice paddle.

Surprised that this works. The example of using earth makes perfect sense to me, but when you are trying to find the perimeter of the lake I was skeptical. Just adding the 2pi times the distance from the shore doesn’t seem like it should work. Impressive though that it does. Very interesting and informing.