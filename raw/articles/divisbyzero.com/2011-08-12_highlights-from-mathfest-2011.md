---
title: Highlights from MathFest 2011
url: https://divisbyzero.com/2011/08/12/highlights-from-mathfest-2011/
author: Dave Richeson
published: '2011-08-12'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Last weekend I was in Lexingon, Kentucky for [MathFest 2011](http://www.maa.org/mathfest/mathfest.html). I had a very nice time and saw some very good talks. I thought, just for fun, that I’d share a couple of juicy mathematical tidbits I learned.

**Fibonacci numbers and the golden ratio**

Ed Burger of Williams College gave a talk entitled “Planting your roots in the natural numbers: A rational and irrational look at 1, 2, 3, 4,…” From his talk I learned the following interesting facts.

In 1939 [Edouard Zeckendorf proved](http://en.wikipedia.org/wiki/Zeckendorf's_theorem) that every natural number can be decomposed uniquely into a sum of [Fibonacci numbers](http://en.wikipedia.org/wiki/Fibonacci_number) in such a way that no two of the Fibonacci numbers are consecutive. Recall, of course, that the Fibonacci numbers are 1, 1, 2, 3, 5, 8, 13, 21, 34, 55,… In particular, they satisfy the relation ,

, and

.


For example:

1=1

2=2

3=1+2

4=1+3

5=5

6=1+5

7=2+5


30=1+8+21


48=1+13+34


Then, in 1957 [G. Bergman proved](http://mathworld.wolfram.com/PhiNumberSystem.html) that every natural number can be written uniquely as the sum of distinct nonconsecutive integer powers of (where

the “

[golden ratio](http://en.wikipedia.org/wiki/Golden_ratio)” ). For example:







(

[check it here](http://www.wolframalpha.com/input/?i=%5B%281%2Bsqrt%285%29%29%2F2%5D%5E3%2B%5B%281%2Bsqrt%285%29%29%2F2%5D%5E%281%29%2B%5B%281%2Bsqrt%285%29%29%2F2%5D%5E%28-4%29) if you don’t believe it)

Then, in 2008 [Dale Gerdemann noticed](http://www.fq.math.ca/Abstracts/46_47-3/gerdemann.pdf) that these facts are related.

First of all, the fact that implies that

, which is a very Fibonacci-like relation.


Moreover, notice that and that

.


Similarly, and

.


Do you see the connection yet? How about this:

Indeed, Gerdemann proved that if and only if

(for

sufficiently large).


So, for example, . So from this we can conclude that

,

[which it is](http://www.wolframalpha.com/input/?i=%5B%281%2Bsqrt%285%29%29%2F2%5D%5E4%2B%5B%281%2Bsqrt%285%29%29%2F2%5D%5E%28-4%29). Isn’t that cool?

Burger went on to describe some work he did with his REU students to extend these results to other sequences and other irrational numbers.

**Beyond the Pythagorean theorem**

Roger Nelson gave an excellent talk entitled “Math Icons.” It is base on material in his new book (with Claudi Alsina) * Icons of Mathematics*. They look at the mathematics behind several famous images (icons) in mathematics.

He started by talking about the “bride’s chair.” This is the famous image which gives the geometric interpretation of the Pythagorean theorem. Rather than our usual algebraic , it shows that the sum of the areas of the squares on sides

and

is equal to the area of the square on the side

.


He went on to point out, for instance, that the figures on the sides of the triangle need not be squares. Any similar shapes will do. For example, in the figure below we see that the area sum property holds for semicircles as well. (This is in Euclid’s [ Elements, VI.31](http://aleph0.clarku.edu/~djoyce/java/elements/bookVI/propVI31.html): In right-angled triangles the figure on the side opposite the right angle equals the sum of the similar and similarly described figures on the sides containing the right angle.)

He also discussed various properties of the so-called Vecten configuration. This is the same as the brides’ chair, but for triangles that aren’t right.

One property that I thought was particular nice is that if we take a Vecten configuration and draw in the three “flanks” (the red triangles below), then the area of each of the three flanks is the same as the area of the original (blue) triangle.

Finally, we turn to a Vecten-type configuration, but with equilateral triangles on each face. In this case, if we join the midpoints of each of the equilateral triangles, we obtain a new equilateral triangle (the red triangle below). This is now known as [Napoleon’s theorem](http://en.wikipedia.org/wiki/Napoleon's_theorem) (yes, that [Napoleon](http://en.wikipedia.org/wiki/Napoleon), and no, although he was interested in mathematics, we don’t believe that he discovered or proved this theorem).

This entire talk was fascinating. There was a lot more great material in it. I’ll have to check out their book!![napolean](../../assets/d1cb34e7a8423784.png)


**How to draw a towel on a beach**

Annalisa Crannell gave an amazing talk called “In the shadow of Desargues” on math, art, and perspective drawing. The main focus of her talk was [Desargues’s theorem](http://en.wikipedia.org/wiki/Desargues'_theorem) and using it to draw a towel on a beach. I couldn’t do the topic justice here, so you’ll have to check out her new book (with Marc Franz) called [Viewpoints: Mathematical Perspective and Fractal Geometry in Art](http://press.princeton.edu/titles/9496.html). I’m excited to read it.

**MAA: The Musical**

Finally, I was honored to be asked to participate in *MAA: The Musical, *which was performed during the opening banquet. I was happy to be asked and even happier *not* to be asked to sing in the production. I was enlisted as tech support (running the slide-show that went along with their songs). That was right up my alley. The MAA players were Alissa Crans, Annalisa Crannell, Art Benjamin, Bud Brown (musical director), Dan Kalman, David Bressoud, Francis Su, Frank Farris, Jennifer Beineke, Jenny Quinn, Matthew DeLong, Norm Richert, Paul Zorn, Talithia Williams. They did an amazing job (at least one song [is now on YouTube](http://www.youtube.com/watch?v=ZRlAPlp59bA)).

[Update: Francis Su recorded the entire performance on his phone. It is [now available online](https://files.me.com/francis.su/0wus7w.mp3) (audio only). Enjoy!]

All-in-all, it was a great conference.

## One Comment

Comments are closed.