---
title: What is the cardinality of the Euclidean topology?
url: https://divisbyzero.com/2010/02/12/what-is-the-cardinality-of-the-euclidean-topology/
author: Dave Richeson
published: '2010-02-12'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I’m teaching topology this semester. The students are looking at different topologies on the real number line. For homework I asked them to think about which topologies are “the same” (if any) and which are “different,” and why they thought that was the case. We haven’t yet talked about continuous maps or homeomorphisms, so I told them that two topologies were the same if we could rename all of the points so that one topology turned into the other.

They came back with the answers I expected. For example, the trivial topology has only two open sets and all the others have infinitely many, so the trivial topology must be different from the rest. One-point sets are open in the discrete topology, but not in any of the others, so it must be different from the rest.

One student pointed out that the discrete topology is the power set of the real numbers, and we know (by

[Cantor’s Theorem](http://en.wikipedia.org/wiki/Cantor's_theorem)) that has a different cardinality than

. So he wanted to know what the cardinalities of the other topologies were. For example, if the usual Euclidean topology on

which we’ll denote

has the cardinality of the continuum (the cardinality of

then this would be another way to show that these two topologies aren’t the same.


My first reaction was joy—I was thrilled with this excellent observation. Then I realized that I didn’t know the cardinality of I told the class that I strongly suspected that it had the cardinality of the continuum, but that I couldn’t say for sure on the spot.


This is probably “a fact well known to those who know it well” (this was a quote from [a book](http://www.amazon.com/Hollow-Chocolate-Bunnies-Apocalypse-GollanczF/dp/0575074019) I once read), but I wasn’t one of those people. So I decided to prove it (with the help of my colleague Jeff).

**Theorem.** and

have the same cardinality.


By definition, every set in can be written as the union of

-balls,

. In fact, it is not difficult to see that every open set can be written as the union of

-balls with rational center and rational


In particular, there is a surjective function Namely, for


We know that is countable, and the power set of a countable set has the cardinality of the continuum. Thus there is a bijective function

Hence

is surjective.


On the other hand, there is a surjective function For example, for

let


Thus by the [Cantor–Bernstein–Schroeder theorem](http://en.wikipedia.org/wiki/Cantor–Bernstein–Schroeder_theorem) (or, technically, the dual version of the theorem), and

have the same cardinality.


I’m wondering how you motivate the definition of a ‘topology’ for these students. Have they been exposed to metric spaces and seen that for many purposes (the ones we end up calling ‘topological’, but they wouldn’t know that at the time), you only need the open sets and not the metric?

All of these students have been through a thorough Real Analysis class in which they’ve learned about the topology of the real number line, including open and closed sets, compactness, limit points, etc.

This topology class starts with basic point set definitions. I re-introduce the “usual” (Euclidean) topology at the beginning of the course along with other topologies. That way they can look at the new definitions with their Real Analysis eyes and also look at them in other weirder topologies.

Makes sense! This is pretty much my experience, too. But I was curious. Thanks.

Reblogged this on Andrey Hihlovskiy.