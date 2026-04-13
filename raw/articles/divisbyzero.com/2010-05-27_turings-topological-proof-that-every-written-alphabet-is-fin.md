---
title: Turing’s topological proof that every written alphabet is finite
url: https://divisbyzero.com/2010/05/27/turings-topological-proof-that-every-written-alphabet-is-finite/
author: Dave Richeson
published: '2010-05-27'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Recently one of my colleagues was reading [Alan Turing](http://en.wikipedia.org/wiki/Alan_Turing)‘s groundbreaking 1936 article “[On Computable Numbers with an Application to the Entscheidungsproblem.](http://books.google.com/books?id=x7mMr4twnloC&lpg=PA58&dq=%22definable%20numbers%22%20turing&pg=PA58#v=onepage&q&f=false)” This is the article in which Turing introduced the [turing machine](http://en.wikipedia.org/wiki/Turing_machine), solved Hilbert’s [Entscheidungsproblem](http://en.wikipedia.org/wiki/Entscheidungsproblem) (`decision problem’), and proved that the [halting problem](http://en.wikipedia.org/wiki/Halting_problem) is undecidable. It is viewed by many as the foundation of computer science.

My colleague shared it with me because it contains a neat use of topology. In this paper Turing gives a topological argument that every written alphabet must be finite. For example, our alphabet has 26 letters, 52 including both capital and lower case, 10 numerals, numerous punctuation marks, etc. Finitely many. Even if we came up with a scheme to generate new symbols, we would only be able to create finitely many.

Here is the explanation in Turing’s own words (we’re particularly interested in the accompanying footnote).

Computing is normally done by writing certain symbols on paper. We may suppose this paper is divided into squares like a child’s arithmetic book… I shall… suppose that the number of symbols which may be printed is finite. If we were to allow an infinity of symbols, then there would be symbols differing to an arbitrarily small extent.

*The effect of this restriction of the number of symbols is not very serious. It is always possible to use sequences of symbols in the place of single symbols. Thus an Arabic numeral such as 17 or 999999999999999 is normally treated as a single symbol. Similarly in any European language words are treated as single symbols (Chinese, however, attempts to have an enumerable infinity of symbols). The differences from our point of view between the single and compound symbols is that the compound symbols, if they are too lengthy, cannot be observed at one glance. This is in accordance with experience. We cannot tell at a glance whether 9999999999999999 and 999999999999999 are the same.

*If we regard a symbol as literally printed on a square we may suppose that the square is,

. The symbol is defined as a set of points in this square, viz. the set occupied by printer’s ink. If these sets are restricted to be measurable, we can define the “distance” between two symbols as the cost of transforming one symbol into the other if the cost of moving unit area of printer’s ink unit distance is unity, and there is an infinite supply of ink at

,

. With this topology, the symbols form a conditionally compact space.


Here’s my more modern topological interpretation of this claim.

**Terms from topology**

I am assuming that the reader is familiar with the terms metric, metric space, topological space, and compact set.

As a brief refresher, recall that a function is a

* metric* on

, with equality iff

,

, and

.


If has a metric

, then we say that

is a

*metric space*. Given a metric we can define open neighborhoods, and thus generate a topology. So every metric space is a topological space.

A subset of a topological space

is

* compact* if every open cover of

**The Hausdorff metric**

We would like to speak about the distance between two compact sets. That is, we’d like a metric for the set .


Let be a metric space and

and

be two compact subsets of

. Suppose

is the point in

farthest from any point in

and that this distance is

. Similarly, suppose

is the point in

farthest from any point in

and that this distance is

. Then the Hausdorff distance between

and

,

, is the larger of

and

. It is not difficult to show that

satisfies the properties of a metric listed above. This is the

* Hausdorff metric*.

For example, suppose ,

,

, and

are the colored sets shown below. The farthest point in

from

(marked

in the diagram) is 4 units away. Similarly, the farthest point in

from

(marked

) is 3 units away. Thus

. In the next picture, the blue set

is a subset of the green set

. Thus

for every

. The point

is farthest from

, with

. Thus

.


![](../../assets/698979bc5c063614.png)


One nice property of the Hausdorff metric is that if is a compact space, then so is

.


**Proof of Turing’s claim**

We would like to prove that any written alphabet is finite. First, we make the following assumptions.

- Each symbol can be drawn inside a given square. More specifically, we will assume that each symbol is a compact subset of
.

- The human eye cannot tell two symbols apart when they are too similar. That is, there is an
such that any symbols

with

are visually indistinguishable.


Let . Then

is the set of all possible symbols. Since

is compact, so is

.


Let denote the

-ball around

using the Hausdorff metric. Then the set of all possible

-balls,

, is an open cover of

. Since

is compact, there exists a finite subcover,

.


From this we can conclude that every symbol is visually indistinguishable from at least one of the

. That is, there can be no more than

visually distinct symbols. In particular, there can be no written alphabet with more than

letters!


[Note: in (1) we assume that all symbols are compact subsets of . We could have dropped the compactness assumption, but if we did then the Hausdorff metric becomes a

[pseudometric](http://en.wikipedia.org/wiki/Pseudometric_space) and things get a little messier.]

**Extensions**

There is nothing special about assuming our figures are letters in an alphabet. Using the same reasoning, we can conclude that it is possible to draw only finitely many pictures with a black pen on a given canvas.

What if we are allowed to use color? Suppose that the visible spectrum of colors is a compact set . Two colors that are very similar are visually indistinguishable. Thus we can use the identical argument, but now a symbol is a compact subset of

, to conclude that there are only finitely many color pictures on a given canvas.


Does this extend to music as well?

Good question. I’d guess “yes” if we were to frame our hypotheses right. For example, the set of pitches that we can hear is compact, the pieces cannot exceed any fixed length (time), and each note is a pure sine wave. Maybe we could relax that last one—I’m not sure.

The argument makes sense using Hausdorff distance, the way you have it, but it sounds to me like Turing intended something different, a form of earth movers’ distance.

Thanks! I was careful not to say that I was giving “Turing’s proof,” although I didn’t explicitly say that I wasn’t…! I was trying to give a proof along the same lines as his using things that I knew.

I had/have some questions about what he wrote in that short footnote. I was not sure if his “metric” was equivalent to the Hausdorff metric (thanks for posting that link), I didn’t know why he mentioned measurable sets, and I was not sure why he said that the set of symbols was conditionally compact instead of compact. Probably you need measurability to use the metric that you mention, and in that case the space is only conditionally compact. (I’m not a point set topologist.) I’ll keep thinking about it.

Interesting post! Thank you.