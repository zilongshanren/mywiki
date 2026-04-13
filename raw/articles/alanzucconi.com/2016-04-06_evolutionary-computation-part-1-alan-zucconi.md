---
title: Evolutionary Computation - Part 1 - Alan Zucconi
url: https://www.alanzucconi.com/2016/04/06/evolutionary-coputation-1/
author: Alan Zucconi
published: '2016-04-06'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This series of tutorial is about evolutionary computation: what it is, how it works and how to implement it in your projects and games. At the end of this series you’ll be able to harness the power of evolution to find the solution to problems you have no idea how to solve. As a toy example, this tutorial will show how evolutionary computation can be used to teach a simple creature to walk. If you want to try the power of evolutionary computation directly in your browser, try [Genetic Algorithm Walkers](http://rednuht.org/genetic_walkers/).

![evolution](../../assets/f0dc16bee64e692f.gif)


![evolution](../../assets/f0dc16bee64e692f.gif)

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
~~Natural~~Artificial Selection - Part 2.
[Phenotype and Genotype](https://www.alanzucconi.com#part2) - Part 3.
[Evolutionary Programming](https://www.alanzucconi.com#part3) - Part 4.
[Local Maxima](https://www.alanzucconi.com#part4) [Conclusion](https://www.alanzucconi.com#conclusion)

As a programmer, you might be familiar with the concept of algorithm. When you have a problem, you write a precise set of instructions to solve it. But what happens when the problem is too complex, or you have no idea how to solve it? While there’s a very precise strategy to optimally play Sudoku, this is not the case for face recognition. How can we code the solution to a problem, when we have no idea how solve it in the first place?

This is a typical scenario in which artificial intelligence finds a real application. One of the easiest techniques that can be used to solve this class of problems is [evolutionary computation](https://en.wikipedia.org/wiki/Evolutionary_algorithm). In a nutshell, it is based on the idea of applying Darwinian evolution to a computer program. The aim of evolution is to improve the quality of an poor solution, by randomly mutating it until it solves the problem with the necessary accuracy. In this tutorial we will explore how evolutionary computation can be applied to learn an optimal walking strategy. You can see a more advanced work in the video below (article: [Flexible Muscle-Based Locomotion for Bipedal Creatures](http://www.goatstream.com/research/papers/SA2013/)).

Chances are you have heard of Darwin’s concept of the **survival of the fittest**. The basic idea is simple: surviving is a hard task, and the creatures who can do it have a higher chance of reproducing. The environment **naturally selects** the creatures who best fit it, killing the ones that fail in such a task. This is often shown in the over simplified (and highly misleading) example of the giraffes: a longer neck helped giraffes to reach higher branches. Over time, this supposedly selected giraffes with longer and longer necks. There has never been a direct force to “extend” the neck of giraffes. Over time, the ones with naturally longer necks have been favourited by the environment.

The same mechanism can be applied to computer programs. If we have an approximate solution to a problem, we can randomly alter it and test whether the change we have made improves (or not) its performance. If we keep iterating this process, we always end up with a better (or equal) solution. Natural selections is truly agnostic to the problem; at its core, it’s driven by random mutations.

In order to understand how computing meets evolution, we need to understand the role of evolution in biology first. In nature, every creature has a body and a set of behaviours. They are know as its **phenotype**, which is the way a creature appears and behave. Hair, eyes and skin colour are all part of your phenotype. The look of a creature is mostly determined by a set of instructions written in its own cells. This is called **genotype**, and it refers to the information that is carried out, mostly in our DNA. While the phenotype is how a house looks like once its built, the genotype is the original blueprint that drove its construction. The first reason why we keep phenotype and genotype separate is simple: the environment plays a huge role in the final look of a creature. The same house, built with a different budget, could look very different.

The environment is, in most cases, what determines the success of a genotype. In biological terms, surviving long enough is succeeding. Successful creatures have a higher chance of reproducing, transmitting their genotype to their offspring. The information to design the body and the behaviours of each creature is store in its DNA. Every time a creature reproduces, its DNA is copied and transmitted to its offspring. Random mutations can occur during the duplication process, introducing changes in the DNA. These changes can potentially result in phenotypical changes.

*Evolutionary computation* is rather broad and vague umbrella term that groups together many different – yet similar – techniques. To be more specific, we will focus on [evolutionary programming](https://en.wikipedia.org/wiki/Evolutionary_programming): the algorithm we are iterating over is fixed, but its parameters are open to optimisation. In biological terms, we are only using a natural selection on the brain of our creature, not on its body.

Evolutionary programming works simply replicating the mechanism of natural selection:

![Copy of Copy of Untitled drawing](../../assets/7561e85a3561fa45.png)

**Initialisation.**Evolution requires to be seeded with an initial solution. Choosing a good starting point is essential, since they might lead to totally different results.**Duplication.**Many copies of the current solution are made.**Mutation.**Each copy is randomly mutated. The extent of the mutation is critical, as it controls the speed at which the evolutionary process run.**Evaluation.**The score of a gene is measured depending on the performance of the creature that has generated. In many cases this requires an intensive simulation step.**Selection.**Once creatures have been evaluated, only the best ones are allowed to be duplicated to seed the next generation.**Output.**Evolution is an iterative process; at any point it can be stopped to obtain an improved (or unaltered) version of the previous generation.

What evolution does, it trying to maximise the fitness of a genome, to better fit a certain environment. Despite being deeply connected to Biology, this can be seen purely as an optimisation problem. We have a fitness function, and we want to find its maximum point. The problem is that we don’t know how the function looks like, and we can only make a guess by sampling (simulating) the points around our current solution.

![Copy of Copy of Copy of Untitled drawing](../../assets/c77907c15c0941fd.png)

The diagram above shows how different mutations (on the X axis) leads to different fitness scores (Y axis). What evolution does is sampling random points in the local neighbourhood of ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

**local maxima**. They are solutions that are locally optimal, but not globally. It is very common to find local maxima in the middle of fitness valleys. When this happens, evolution might be unable to find a better nearby solution, getting stuck. It is often said that cockroaches are stuck in an evolutionary local maxima ([Can An Animal Stop Evolving?](http://www.bbc.co.uk/earth/story/20150413-can-an-animal-stop-evolving)): they are extremely successful at what they do, and any long-term improvement requires a too high short-term penalty on their fitness.

This post introduced the concept of evolution, and the role it plays in Artificial Intelligence and Machine Learning.

**The next post will start the actual tutorial on how to implement evolutionary computation. Designing the body of a creature that can be evolved is the first necessary step.**

![walker_5](../../assets/3affa10b79199060.gif)

If you are interested in games which gameplay resolves around real evolution, I would highly suggest checking out the Creatures series.

#### Other resources

- Part 1.
**Evolutionary Computation: Theory** - Part 2.
[Evolutionary Computation: Phenotype](https://www.alanzucconi.com/?p=4774) - Part 3.
[Evolutionary Computation: Genotype](https://www.alanzucconi.com/?p=4736) - Part 4.
[Evolutionary Computation: Loop](https://www.alanzucconi.com/?p=4765)

## Leave a Reply Cancel reply