---
title: BraidTiles—A Mathematical Braid Puzzle
url: https://divisbyzero.com/2019/05/01/braidtiles/
author: Dave Richeson
published: '2019-05-01'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

We can view [braids mathematically](https://en.wikipedia.org/wiki/Braid_group) as *n *strings hanging from a horizontal bar. Each piece of string runs downward and can cross neighboring strings. In the 1920s [Emil Artin](https://en.wikipedia.org/wiki/Emil_Artin) observed that braids of *n *strings form an [algebraic group](https://en.wikipedia.org/wiki/Group_(mathematics)). To “multiply” two braids, we append the bottom of one braid with the top of another braid. The identity element in this group is the non-braid; that is, *n *strings hanging down with no twists. Every braid has an inverse—it is the braid that untwists the given braid. We can see that this is a nonabelian group; that is, braid multiplication is not commutative.

![BraidPhoto.jpg](../../assets/b6ae252ae399fac9.jpg)


Several years ago, I encountered [KnoTiles](https://www.mathartfun.com/FractalKnots/KnoTiles.html), which are puzzle pieces that can be used to make mathematical knots. Inspired by KnoTiles, I made puzzle pieces that can be assembled to make mathematical braids. I call the puzzle pieces *BraidTiles.* (Here’s a [printable pdf](https://divisbyzero.com/wp-content/uploads/2019/05/braids.pdf), which I recommend printing in color on heavy cardstock.)

Notice that the twists come in two varieties—left strand over right strand and right strand over left strand. If you replace one twist with the other, you will get a different braid!