---
title: Some notes on data processing
url: https://anteru.net/blog/2014/some-notes-on-data-processing
published: '2014-07-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

This is the long explanation behind a recent tweet:

https://twitter.com/NIV_Anteru/status/489349219120340993

The problem I’m aiming at here is processing of large data sets. Imagine you have a 500 million polygon model you need to compute normals for. The first idea is pretty simple, let’s open the model, load it, compute per triangle normals and write them back into the same file. VoilÃ , no temporary disk space used, data is mutated in place and everything is fine. Right?

Turns out, any kind of in-place mutation is actually the wrong thing to do when it comes to big data sets. To understand why, let’s look at a two use-cases and then we’ll take a short trip into computer science 101 to get the solution.

How do you **compose operations**? You want to triangulate, create level-of-detail, sort your mesh and extract vertex positions. For this example, the vertex position extraction simply identifies unique vertices and only keeps them, removing the topology information. Now you want the vertex positions of the triangulated, simplified mesh and of the initial mesh. If you mutate in-place, this means you have to make a copy of your mesh, run the vertex position extraction, then take the input mesh again, run your triangulation and simplification, make a copy again, and then run the vertex extraction. All because the vertex position extraction is in-place and destructive.

How do you **cache**? If your data is mutable, you cannot cache outputs or inputs of one processing step. Let’s assume you have a three step pipeline: Part one procedurally generates a mesh, the second part triangulates it and finally, you compute normals. Now you fix a bug in the normal computation. If you mutate in-place, your normal computation now needs a new operation mode to work on data which already has (incorrect) normals if you want to work on the “cached” triangulation output. Otherwise, you have to run again on the source data and triangulate & compute the normals from scratch. Oh, and if you fix something in the triangulation, you’ll always have to run the procedural generation first, as the in-place mutated mesh cannot be fixed.

If you think a bit about the problems, then you’ll notice that we’re actually fighting the side-effects of our computation. If you know a bit about programming theory, you’ll notice that these problems are exactly those which can be trivially solved by functional programming. Or to be more precisely, by modelling our operations as **pure functions** and treating all our data as **immutable**.

So what is a pure function? It’s a function which given some input, will always produce the same output. On its own, it’s not that amazing, but if you add immutable data, things get really interesting.

Immutable data might sound a bit weird at first, but it’s actually part of the definition. If data would be mutable, running a function on the same data twice would yield different results. What it means in practice is that a pure function will construct a new result.

If you followed so far, you’ll probably see where I’m heading: Disk space is cheap these days, and writing your code to mutate data in-place is not an optimization – it’s a serious problem which will make your code hard to maintain, hard to optimize and hard to reuse.

Let’s look at our sample problems from above and how immutable data & functional programming solves them. Composition: Trivial. We simply chain our operations, and no copying will take place. Instead, the input will be read only once and handed over to the individual operators.

Caching: Again, trivial. We simply compute a hash value of each input. If we need to re-run some part, we’ll only do so for the parts of the pipeline which actually changed. For example, if we fix the triangulation, we will run it for all inputs (which are cached). If some parts of the triangulation produce the same results, the normal generation won’t run for them (as the input hash for that step will be the same.)

The major downside of this approach is that you’ll be using a lot more disk space than before if you don’t chain operations in memory. As mentioned before, I’m using a [stream-oriented format for my geometry](https://anteru.net/2012/08/25/1904/), which allows me to chain operations in-memory easily, but if you do have to work on complete meshes, you’ll be using quite a bit more disk space in some cases than if you would do in-place mutation. For instance, changing vertex colours will now require you to re-write the whole file.

In practice, it turns out that more disk space is rarely an issue though, but composition, caching and robustness are. If you can compose functions without worrying, it’s usually possible to perform a lot of steps in memory and only write the output once, without intermediate files. It’s also easier to provide a node network to process data if every node has a well-defined input and output; in-place mutation is basically impossible to model in such a scheme.

Second, caching is trivial to add, as well as checksums for robustness. If you mutate in-place, there’s always a risk that something will destroy your data. This is much lower if your input is immutable.

Finally, there are also advantages when it comes to parallel execution. These are well-known from functional languages; for example, you can freely change your evaluation order – run a thread for each input element, or run a thread for each operator, or both.

It’s interesting that on the run-time side, I tend to go for a more functional programming style whenever I can. In my C++ code, nearly everything is const – functions, class members, and objects. This allows me to easily reason about data flow, thread safety and to provide strong unit tests. Yet, when thinking about GiB-sized files, I fell back into the “in-place”, imperative programming mind-set.

On my tool side, I since moved nearly everything over to completely functional & immutable processing. Right now, there’s only one function left which has to be converted to a pure function, which will be also fixed soon hopefully. So far, the new approach have turned out to be successful. The only downside I had was that I have to be a bit more careful about intermediate outputs, if I don’t want to waste disk space, but in practice, this was far less problematic than I anticipated.

To conclude this: Mutable data is bad; be it run-time or disk. Even for large files, the short-term gains in disk I/O performance and usage are not worth it in the long run. Just say no and go for a functional approach:)