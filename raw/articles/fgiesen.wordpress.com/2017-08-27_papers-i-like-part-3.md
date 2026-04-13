---
title: Papers I like (part 3)
url: https://fgiesen.wordpress.com/2017/08/27/papers-i-like-part-3/
published: '2017-08-27'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Papers I like (part 3)

Continued from [part 2](https://fgiesen.wordpress.com/2017/08/14/papers-i-like-part-2/).

### 12. Chazelle-[“Filtering search: a new approach to query-answering”](https://www.cs.princeton.edu/~chazelle/pubs/FilteringSearch.pdf) (1986; computational geometry/information retrieval)

The part I specifically recommend is sections 1 through 3. For most of these problems, there are simpler solutions using different data structures by now (especially via the persistent search trees we saw earlier in part 1), so don’t hurt yourself with the parts dealing with the hive graph; but it’s definitely worth your time to grok these first few sections.

Filtering search deals with “retrieval”-type problems: you have a set of objects, and you want to run a query that finds the subset of those objects that matches some given criterion. In the interval overlap problem the paper uses as its first example, the set of objects is a bunch of 1-dimensional intervals:

![A few 1D intervals](../../assets/9a2e30717314e512.png)


I’m drawing each interval in its own line so overlaps don’t get messy, but that’s just a visualization aid; this is a 1D problem. Our queries are going to be “report all intervals in the database that intersect a given query interval”.

How would you set up a data structure that answers these queries efficiently?

A natural enough approach is to chop our 1D x-axis into slices, creating a new “window” (that’s the terminology the paper uses) whenever an interval begins or ends:

![1D intervals, sliced](../../assets/d6d64e941efa4587.png)


Because the begin and end points of intervals are the only locations when the answer to “which intervals overlap a given x-coordinate” change, the answer is the same within each window. Therefore, if we compute this partition in advance and store it in say a search tree (or an external search tree like a database for bigger sets), and each window stores a list of which intervals overlap it, we can answer one of our original questions directly: given a 1D point, we can find all the intervals overlapping it by finding out which of the windows it overlaps by looking it up our search tree, and then reporting the stored list.

Furthermore, given a solution for point queries, we can take a first stab at solving it for interval queries: find all the windows overlapping our query interval, and then return the union of all the lists for the individual windows. Computing unions of those sets can be done in linear time if we store the data appropriately: for example, if we give each interval stored in our database some unique integer ID and make sure all our lists of “intervals overlapping this window” are sorted by the interval IDs, then the union between a m-element list and a n-element list can be computed in time (using a variant of the standard list merging algorithm used in mergesort).


It’s fairly easy to convince yourself that this works, in the sense that it gives the correct answer; but is it efficient? How big can a database for n intervals get? This matters not just for storage efficiency, but also for queries: if the user queries a gigantic interval (say encompassing all intervals in the image above), we end up computing the union of all interval lists stored in the entire database. We know the final answer can only contain at most n intervals (because that’s how many are in the database), but do we have any nice bounds on how long it will take to determine that fact?

Alas, it turns out this approach doesn’t really work for our problem. Without further ado, here’s an example set that kills this initial approach for good:

![n intervals in a problematic configuration](../../assets/7daa51ee0de023ef.png)


Here, we have 5 intervals with the same center: the first one has a width of 1 unit, the second is 3 units wide, the third 5 units wide, and so on. The middle window overlaps all 5 intervals; the two windows to either side overlap 4 intervals each, all but the first; the next windows on either side overlap 3 intervals each, and so forth.

Therefore, the bottom-most interval gets stored in 1 list; the one up from it gets stored in 3 lists; the next one up gets stored in 5 lists, and so on. For our 5 input intervals, the total size of the lists sums to , and in general,

. So our database will end up with

size just to store the sorted lists, and if someone executes a query overlapping all n intervals, we will iterate over that entire database and try to merge n

2 list elements to produce a final result set with n intervals in it. No good. And note that even if the query part was nice and fast, having to build a -sized search structure for n elements would make this completely impractical for large data sets.


Now, on to the actual paper: Chazelle points out that in the entire class of retrieval problems, if the input size is n, and the number of elements reported for a particular query is k, the worst-case time for that query will in general be of the form where f is some (hopefully slow-growing, say logarithmic) function of n. This is because reporting a given result is not free; it’s generally an

operation.


Consider extreme cases like our “return me the entire universe” range query: in that case, we have k=n, and if we have say , the resulting time complexity for that query is going to be

; if we ask for the entire database, it really doesn’t make a big difference how smart our indexing structure is (or isn’t). The total operation cost is going to be dominated by the “reporting” portion.


This revised cost estimate tells us where we were going wrong with the structure we were building before. It’s important to be able to locate regions of the database overlapped by only a few intervals quickly. But when we have many “active” intervals, the cost of reporting them exceeds the cost of finding them anyway, and caching all those pre-made lists does more harm than good!

Instead, what we want to do is adapt the data structure to the size of the answer (the number of results given). In regions where there are only a few active intervals, we want to locate them quickly; where there’s many active intervals, we don’t want to make a new list of intervals every time a single one of them begins or ends, because when we do, we’ll waste most of our query time merging almost-identical lists.

And that, finally, brings us to filtering search: instead of storing a new list every time the answer changes, we adapt the frequency with which we store lists to the number of active intervals. Once we do this, we need to do a bit more processing per list entry: we need to check whether it actually overlaps our query point (or interval) first – but that’s an check per list entry (this is the “filtering” part of “filtering search” – rejecting the false positives).


In return, we get a *significantly* smaller database. Using the scheme described in section 3 of the paper (briefly: make the number of intervals per window proportional to the lowest number of active intervals at any point in the window), our data structure for n intervals takes space and gives

query time (and with simple construction and search algorithms too, no hidden huge constant factors). And in particular, if we know that the

*entire database* has size proportional to n, not only do we know that this will scale just fine to large data sets, it also means we won’t hit the “lots of time spent pointlessly merging lists” problem in our original approach.

That’s why I recommend this paper: the underlying insight is easy to understand – we can afford to be “sloppy” in areas where we’ll spend a lot of time reporting the results anyway – and the resulting algorithm is still quite simple, but the gains are significant. And as Chazelle notes, even if you don’t care about the particular problems he talks about, the overall approach is applicable to pretty much all retrieval problems.

### 13. McIllroy – [“A Killer Adversary for Quicksort”](http://www1.cs.dartmouth.edu/~doug/mdmspe.pdf) (1999; algorithms/testing)

This paper is short (4 pages only!) and sweet. It’s not news that Quicksort will go quadratic for some inputs. Nor is it news how to write a mostly-Quicksort that avoids the quadratic case altogether; that was solved by Musser’s [Introsort](https://en.wikipedia.org/wiki/Introsort) in 1997 (if you don’t know the trick: limit the recursion depth in Quicksort to some constant factor of a logarithm of the input size, and when you get too deep, switch to Heapsort).

The cool thing about this paper is that, given *any* Quicksort implementation that conforms to the C standard library `qsort`

interface (the relevant part being that the sorting function doesn’t compare the data directly and instead asks a user-provided comparison function), it will produce a sequence that makes it go quadratic. Guaranteed, on the first try, under fairly mild assumptions, as long as the function in question actually implements some variant of Quicksort.

As-is, this paper is obviously useful to implementers of Quicksort. If you write one, you generally know that there are inputs that result in quadratic run time, but you might not know which.

But more generally, I think this paper is worth reading and understanding because it shows the value of adversarial testing: the solution isn’t hard; it relies on little more than knowing that a Quicksort proceeds as a sequence of partitioning operations, and an individual partition will compare all remaining elements in the current list against the chosen pivot. Treating the rest of the code as a black box, it turns out that knowing this much is basically enough to defeat it.

The details are different every time, but I found the paper quite inspiring when I first read it, and I’ve gotten a lot of mileage since out of building test cases by trying to make an algorithm defeat itself. Even (particularly?) when you don’t succeed, it tends to deepen your understanding.

### 14. Knuth – [“Structured Programming with go to Statements”](https://sbel.wisc.edu/Courses/ME964/Literature/knuthProgramming1974.pdf) (1974; programming languages)

I’ll write “go to statements” as gotos in the following, since that’s the spelling we mostly have these days.

This paper is the primary source of the (in)famous “premature optimization is the root of all evil” quote. So to get that out of the way first, it’s on page 8 of the PDF, printed page number 268, right column, second paragraph. I recommend reading at least the preceding 2 paragraphs as well, as well as the paragraph that follows, before quoting it at others. It’s definitely different in context.

Zooming further out, this is a long paper covering a wide range of topics, a lot of which might not interest you, so I’ll go over the structure. It starts by recounting a lot of 1970s arguing back and forth about structured programming that’s mainly of historical interest these days; structured control flow constructs are a done deal these days.

After that, he goes over several algorithms and discusses their use of goto statements, which might or might not interest you.

One section that is definitely worthwhile if you haven’t seen it before is the section on “Systematic Elimination” starting on page 13 in the PDF (printed page number 273) which explains ways of converting any goto-ridden program into one that uses purely structured control flow and gives pointers to the underlying theory – note that some of these ways are quite anticlimactic!

The sections after are, again, interesting archaeology from a time before `break`

and `continue`

statements existed (the “structured” gotos we now generally consider unproblematic).

Then we get into “2. Introduction of goto statements”, which again is nowadays mostly standard compiler fare (covering certain control flow transformations), but worth checking out if you haven’t seen it before. Note that most modern compilers eventually transform a program into a set of basic blocks with an associated control-flow graph, which is essentially lists of statements connected by gotos; it turns out that such a (more expressive) notation makes control flow transformations simpler, and passes that need more structure generally recover it from the control flow graph. Thus, contrary to popular belief, such compilers don’t care all that much whether you write say loops using built-in loop constructs or via ifs and gotos. It does, however, make a difference semantically for objects with block-scoped lifetimes in languages that have them.

The final section I’ll point out is “Program Manipulation Systems”, starting on page 22 in the PDF (printed page number 282). Modern optimizers implement many more transforms than 1970s-era compilers do, yet still I feel like the problem Knuth observed in the 1970s still exists today (admittedly, speaking as a fairly low-level programmer): many of the transforms I wish to apply are quite mechanical, yet inexpressible in the source language. Various LISP dialects probably get closest; the metaprogramming facilities of more mainstream languages generally leave a lot to be desired. I still feel like there’s a lot of potential in that direction.

### 15. Bryant-[“Graph-Based Algorithms for Boolean Function Manipulation”](http://mtv.ece.ucsb.edu/courses/ece156B_14/randy_obdd86.pdf) (1986; data structures)

For a long time, this used to be one of the widest-cited papers in all of CS. Not sure if that’s still the case.

It introduces a data structure properly called a Reduced Ordered Binary Decision Diagram (ROBDD), often just called BDDs, although there exist other variants that are not ordered or reduced, so there’s some potential for confusion. Watch out! That said, I’ll just be writing BDD for the remainder; note that I’m always talking about the ROBDD variant here.

So what is a BDD? It’s a data structure that encodes a Boolean truth table as a directed graph. It’s “reduced” because identical subgraphs are eliminated during construction, and “ordered” because the resulting BDD is specific to a particular ordering of input variables. The paper gives some examples.

Why does anyone care? Because truth tables have exponential size, whereas BDDs for many functions of interest have very tractable size. For example, an important result is that BDDs for the outputs of binary adders of arbitrary widths (with the right variable ordering) have a linear number of nodes in the width of the adder. And a BDD shares many of the properties of a truth table: it’s easy to evaluate a function given as a BDD, it’s easy to build them incrementally out of a description of some logic function, and they’re canonical – that is, with a given variable ordering, there is exactly one ROBDD that represents a given function. Which in turn means that we can check whether two binary functions are identical by checking whether their BDDs agree.

This last property is why BDDs were such a hot topic when they were introduced (leading to the aforementioned high citation count): they are very handy for formal verification of combinational logic and other problems arising in hardware design.

For example, say you have a clever 64-bit adder design you wish to implement, but you need to prove that it gives the correct result for all possible pairs of 64-bit input numbers. Checking the proposed design by exhaustively testing all 2128 possible inputs is out of the question; even if had a machine that managed to verify over a trillion combination per second, say 240 of them, and we had over a million such machines, say 220 of them, we’d still have to wait 268 seconds to get the result – that’s about 9.36 trillion years, 680 times the age of the universe.

This is not going to work. But luckily, it doesn’t need to: we can build a BDD for the new adder design, another BDD for a simple known-good adder design (say a ripple-carry adder), and check whether they agree. That validation, written in interpreted Python and run on a single workstation, takes [just a moment](https://codewords.recurse.com/issues/four/the-language-of-choice).

BDDs aren’t a panacea; for example, BDDs for multiplier circuits have exponential size, so formally verifying those isn’t as easy. As far as I know, modern tools combine different (non-canonical) representations such as [and-inverter graphs](https://en.wikipedia.org/wiki/And-inverter_graph) with SMT solvers to tackle more difficult Boolean equivalence problems.

Nonetheless, BDDs are a simple, elegant data structure that immediately solved a serious practical problem, and they’re worth knowing about.