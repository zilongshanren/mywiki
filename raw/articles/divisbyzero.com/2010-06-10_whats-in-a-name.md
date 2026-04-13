---
title: What’s in a name?
url: https://divisbyzero.com/2010/06/10/whats-in-a-name/
author: Dave Richeson
published: '2010-06-10'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I had an interesting interaction on Twitter today. I’m doing some research with a student that involves a little graph theory. We needed some graph theory terminology that I was sure was well-known (but not known to us), so [I turned to Twitter](http://twitter.com/divbyzero/status/15849116622).

Let be a vertex of directed graph. Define

to be the set of all vertices that point to

and

to be the set of all vertices that

points to.


For example, in the graph below and

.


My question was: what do we call the sets and

?


I received quite a few replies, and quickly discovered that there is no standard terminology. Here’s what I heard:

| inset | outset |
| parents | children |
| predecessors | successors |
| incoming vertices | outgoing vertices |
| preset | postset |
| in-neighbors | out-neighbors |
| backward star | forward star |

(Alasdair McAndrew (@amca01) suggested I come up with my own terminology and gave [some](http://twitter.com/amca01/status/15851710765) creative [suggestions](http://twitter.com/amca01/status/15852212705) of his own.)

While I thought there would be one answer, I guess it isn’t too surprising that there isn’t—we can’t even decide on basic terminology: graph/network, vertex/node, etc. There are many places in mathematics in which there are multiple names or symbols for the same mathematical object. Just think of all the ways to write the derivative: ,

,

, and

(and calculus is much older than graph theory). Even multiplication can be expressed in multiple ways:

,

,

and

.


Maybe we should institute a mathematical standards board…. nah!

The parents/children terminology is common when dealing with directed acyclic graphs. I just assumed the terminology was also used for general directed graphs, but I could be wrong. I like it because it is suggests a whole range of other family-tree terminology, e.g. descendants for all vertices reachable by a path from a given vertex or cousins for connected (ignoring direction) vertices not reachable by a path. In directed acyclic graphs, it makes sense because you cannot have a parent that is also a child, or indeed a descendant that is also an ancestor. Indeed, a general directed acyclic graph is just a family tree for a species with a variable number of genders.

I was just this morning reading an old(1924) article by Florian Cajori, “The Unification of Mathematical Notations in the Light of History”. Early on he suggests, “The admonition of History is clearly that the chance, haphazard proceedure of the past will NOT lead to uniformity.” I think the same can be said, perhaps more so, for terminology than notation.

In the end, his quote from Kipling may be the most apt

“There are nine and sixty ways

Of constructing tribal lays

And every single one of them is right.”

May the set’s names have changed? I think first column names are for B(v) and second column names are for A(v)

Oops. Thanks. I fixed it.