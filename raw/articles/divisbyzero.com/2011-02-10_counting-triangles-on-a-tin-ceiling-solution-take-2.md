---
title: Counting triangles on a tin ceiling (solution, take 2)
url: https://divisbyzero.com/2011/02/10/counting-triangles-on-a-tin-ceiling-solution-2/
author: Dave Richeson
published: '2011-02-10'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

This is the solution to a problem I posed in [my previous blog post](https://divisbyzero.com/2011/02/10/counting-triangles-on-a-tin-ceiling). Please read that post first.

[Update: I posted a solution to this problem two days ago. Yesterday [Brent Yorgey](http://www.cis.upenn.edu/~byorgey/index.html) pointed out that my analysis of “type 2” triangles was not quite correct. (See his comment below.) So I went back to the whiteboard and worked out the correct solution. Hopefully the formula given below is correct. Thanks, Brent!]

Here’s a recap of the problem: How many triangles are there in an grid of squares with X’s through them (as shown below)?


![](../../assets/5ed5947303a6c593.png)


We realized that there are two types of triangles. We’ll say a triangle is of “type 1” if the legs of the triangle run horizontally and vertically (as shown below).

![](../../assets/620ebff32945c232.png)


A triangle is of “type 2” if the hypotenuse runs either horizontally or vertically (as shown below).

![](../../assets/8d1285cb6333f567.png)


**Type 1**

Consider the type 1 triangles with horizontal (or vertical) segments in each leg. Examples of

are shown in the diagram. When

there are

such triangles in the ceiling. In particular, there are

having the orientation shown, but then they can be rotated 90, 180, or 270 degrees. When

there are

such triangles. When

there are

, etc. Thus, the total number of type 1 triangles is


**Type 2**

Counting the type 2 triangles is tricker. Let denote the number of segments in the hypotenuse of the triangle. Examples of

are shown in the diagram. The key observation is that each time

increases by one unit the horizontal distance (in the given configuration) increases by a half unit.


For example, when here are the number of type 2 triangles of a given orientation for the possible values of

(so the final count will be four times the sum of these).


And here are the number when .


In general, for a given and

and a given orientation we can fit

triangles in one direction and

in the other. Thus the number of type 2 triangles is


It follows that there is a different closed form for this summation for even and

odd.


Consider the case that is even. I’ll skip most of the algebraic details, but essentially I summed the values for even

and odd

separately.


Now suppose is odd.


Adding the number of type 1 and type 2 triangles and simplifying the expression we find that the total number of triangles in an grid is


when is even and


when is odd.


Thus, here are the number of triangles for the first few -values:


In particular, there are 268 triangles in the example at the start of the blog post.


When I posted my first solution I claimed that this sequence was not in the [On-line Encyclopedia of Integer Sequences](http://oeis.org/) database. Now that I’ve corrected the formula (and hence the fourth term of the sequence), I discovered that [it is already there](http://oeis.org/A100583)!. (They give more terms of sequence A100583: 8, 44, 124, 268, 492, 816, 1256, 1832, 2560, 3460, 4548, 5844, 7364, 9128, 11152, 13456, 16056, 18972, 22220, 25820, 29788, 34144, 38904, 44088, 49712, 55796, 62356, 69412, 76980, 85080, 93728, 102944, 112744, 123148, 134172, 145836.)

I don’t think your analysis of type 2 triangles is quite right. Every time you increase the hypotenuse of a type 2 triangle by 1 unit, the width (given the orientation you illustrated for type 2) only increases by 1/2 unit, so there are not always i(i-1) of them. The number of triangles that will fit from top-bottom decreases by 1 each time, but the number of triangles that fit left-right only decreases by 1 every OTHER time. For example, in the 4×4 grid shown, you can see that there are actually 3 (not 2) type 2 triangles with a hypotenuse of 4.

This makes things a bit trickier (although it does mean that the first case is actually not a special case!). I think the correct formula for the number of type 2 triangles is

although I am not sure of a nice way to simplify this off the top of my head.

Of course, I meant to say, 12 type 2 triangles with a hypotenuse of 4, three in each orientation.

Ugh! Thanks, Brent. You are definitely correct about our mistake. Clearly I should have waited more than 20 minutes before typing up and publishing our “result” :-) I’m going to pull this off my blog temporarily until I can find a fix (or determine that there isn’t an elegant one).

Check it out now. I think it is fixed.

Looks good to me! You ought to submit a link to this blog post to be included in the OEIS entry.

I’m not sure about a closed form, but in counting triangles of Type 2, we can do the following. The number of triangles with hypotenuse on a particular vertical line is T(n), except for those that don’t fit in the n x n grid, which is easily seen to be A002623, the partial sum of alternate triangular numbers. Thus, {the number of triangles of type 2} = 4 n T(n) – {the (n-2)th term of A002623).

Beautiful problem and an elegant solution, although i think we can count total number of triangles using coordinates of the points. I will think on this problem and as soon as I will post it in my blog. I have another problem on combinatorics, please help.

“THERE ARE 10 BOYS STANDING IN A QUEUE FOR A TICKET WORTH 5 RS. 5 OF THEM HAVING 5 RS NOTE AND 5 OF THEM HAVING 10 RS NOTE. IN HOW MANY WAYS THEY CAN STAND IN THE QUEUE SUCH THAT NONE HAVE TO WAIT FOR A CHANGE( THE SALESMAN DO NOT HAVE ANY MONEY TO BEGIN WITH). You can change RS with $ if you wish.