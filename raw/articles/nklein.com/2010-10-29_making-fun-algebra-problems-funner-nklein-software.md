---
title: 'Making Fun Algebra Problems Funner :: nklein software'
url: http://nklein.com/2010/10/making-fun-algebra-problems-funner/
author: Pat
published: '2010-10-29'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

A month ago, a friend posted the following problem on Facebook. I just noticed it this week.

![circle-puzzle Drawing of a circle with radius r sitting on a line with two squares wedged against it. One square has side-length 1, the other side-length 2. There are six units between the squares.](../../assets/33fe59c2ca7a51a4.png)


The goal is to find the exact length of the radius .


I love this kind of math problem. Â It has a bunch of features that make it a great, toy math problem.


- It looks like it’s going to be easy, but at the same time seems at a glance to not have enough information
- It looks like a geometry problem but only requires that you know:

- All radii of a circle have the same length
- A radius to a point where a tangent line touches the circle is perpendicular to that tangent line
- It requires only very basic algebra:

- Pythagorean theorem
- Solving quadratics
- The numbers in the problem are small, non-zero integers

I spent the next 25 minutes and six pieces of paper working the problem. About 20% of the time that I spent was rechecking my work. Why did I bother rechecking my work on a toy problem?

*Warning: Spoilers ahead. If you like this kind of problem, stop reading now and play with it first.*

### The problem with the problem

This problem failed to satisfy one of my other criterion for great, toy puzzle problems.


- The answer is a small natural number (or the current year)

I am notorious for messing up signs when doing large algebra calculations. I had to check and recheck all of my work to make sure that I hadn’t done and gotten

somewhere. If I had come up with an integer value for

, I’d have been done. Instead, the answer involved a half-integer plus a multiple of

.


What? ?!? Raise your hand if you’ve ever seen that written anywhere before this problem.


That’s what I thought.

So, I spent the next hour looking for a different set of numbers to put in for 1, 2, and 6 so that the radius would come out to an integer. My approach was Brownian, at best. I threw Pythagorean triples at a wall until one stuck.


The sticky triple left me with to put in place of

. So, I put the problem down for awhile.


The next time that I was in the car, I realized that the radius for the sticky triple was less than . That meant that the larger box was touching the upper half of the circle instead of the lower half. The circle had to overlap the box.


So, I was back to the drawing board. Of course, I’d have been back to the drawing board at some point anyway because that sticky triple violated both of my small numbers criteria.

*Warning: If you want to play around with finding a set of numbers that work, do it before you read the following. There are even more spoilers ahead.*

### Infinitely many combinations to get an integer radius

When I next sat down to play (pronounced: /OBSESS/) with this problem, I quickly hit upon the following way to take any Pythagorean triple and make a version of the above puzzle where the radius

is an integer.


![circle-puzzle-triple Same sort of diagram as above except radius is c, boxes are height c-b and c-a, and some (a,b,c) triangles are drawn in](../../assets/55842fb4ed00df7b.png)


In fact, using a 3-4-5 triangle, it is obvious that had the distance between the blocks in the original problem been 7 instead of 6, the radius would have been a small natural number.

Now. Now, I had infinitely many ways to construct this problem so that the radius was an integer. But, did I have all of the ways?

### All your configuration are belong to us

When looking at that last diagram, the first question that comes to mind (for me) is: Do I really need to use the same Pythagorean triple on the left and right triangles?

The answer, of course, is No.


If I have two Pythagorean triples and

and

is any (positive) divisor of both

and

, then I can start with an

triangle on the left and an

triangle on the right. I can then scale up the left triangle by

and scale the right triangle up by

. Now, both triangles have the same hypotenuse.


This means that if the left block has height , the right block has height

, the distance between the two blocks is

, and the resulting circle has radius

.


![circle-puzzle-two-triples A more general version of the previous diagrams](../../assets/4687ce06e41336dc.png)


Does this cover all of the solutions? Could I possibly have non-integer and

such that

is still integer?


Well, for the problem to be formulated entirely with integers, we certainly need the hypotenuse of the right triangles to be an integer. Further, to make the blocks integer heights then both of the legs of the right triangles along the vertical radius must also be integer. So, if the triangle on the left had hypotenuse , vertical leg

and horizontal leg

, then we know that

where both

and

are integers. Thus,

must be the square root of an integer.


It is easy to see that if were a non-integer rational number, then its square would also be a non-integer rational number. So, either

is integer or it is the irrational square root of an integer.


So, can be an irrational number? If

were an irrational number, then the horizontal leg of the other triangle would have to be some integer

minus the irrational

for the distance between the two blocks to be an integer. Let’s say the vertical leg of the triangle on the right is

. Just like

in the first triangle,

must be an integer. We also know that

. This, in turn, means that

. The right hand side is clearly rational, so

could not have been irrational.


So, there you have it: all of the numbers that make this problem have all integers on the drawing and an integer answer.

Do you have the written solution to this problem. I have been working on it for a while now and can’t figure it out.

Thanks

Thanks for this. I figured out the problem with 6 soon enough, but it is inelegant, as you say. It took me a few to catch on to what you were doing with the matching triangles–I thought you were saying it was true still with a 6:1 ratio–but now I see. Quite lovely. Yes, the problem should have been stated with a distance of 7.