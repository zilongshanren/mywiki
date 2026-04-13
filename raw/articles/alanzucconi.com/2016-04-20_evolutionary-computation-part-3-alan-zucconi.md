---
title: Evolutionary Computation - Part 3 - Alan Zucconi
url: https://www.alanzucconi.com/2016/04/20/evolutionary-computation-3/
author: Alan Zucconi
published: '2016-04-20'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

When we are looking at a problem through the lens of evolution, we always have to take into account its two faces: the **phenotype** and **genotype**. The previous post focused on creating the body of the creature, together with its brain. It is now time to focus on the genotype, which is the way such information is represented, transmitted and mutated.

![walker_4](../../assets/c2c99a7e8c3fdda3.gif)

As previously introduced, each leg is controller by a sine wave ![Rendered by QuickLaTeX.com s](../../assets/864f28b25521f331.png)

![Rendered by QuickLaTeX.com m](../../assets/ae1726b8a02e3872.png)

![Rendered by QuickLaTeX.com M](../../assets/17b6ead89daa2266.png)

![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com o](../../assets/145b04bf6101cdc0.png)


![Rendered by QuickLaTeX.com \[s = \frac{M-m}{2} \left(1+\sin \left( {\left(t+o\right) \frac{2\pi}{p}} \right) \right) + m\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c32c677a828f1ca73502661422d011a1_l3.png)


Which is just a normal sine wave with period ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com m](../../assets/ae1726b8a02e3872.png)

![Rendered by QuickLaTeX.com M](../../assets/17b6ead89daa2266.png)

![Rendered by QuickLaTeX.com o](../../assets/145b04bf6101cdc0.png)


Learning how to walk is now a problem of finding a point in a space with 8 dimensions (4 for each leg). Let’s start creating the genome for a single leg. This is hosted in a structure called `GenomeLeg`

. It wraps the four necessary parameters, and it provides a way to evaluate the sinusoid it represents:

[System.Serializable] public struct GenomeLeg { public float m; public float M; public float o; public float p; public float EvaluateAt (float time) { return (M - m) / 2 * (1 + Mathf.Sin((time+o) * Mathf.PI * 2 / p)) + m; } }

We now need to wrap two `GenomeLeg`

in a single structure that will hold the genome in its entirety:

[System.Serializable] public struct Genome { public GenomeLeg left; public GenomeLeg right; }

At this stage, we have the complete structure that determines the walking strategy of a creature. This allows to complete the `Creature`

class that was left in the previous post:

public class Creature { public Genome genome; public LegController left; public LegController right; public void Update () { left.position = genome.left.EvaluateAt(Time.time); right.position = genome.right.EvaluateAt(Time.time); } }

At the heart of evolution, there is the concept of transmission and mutation of the genome. In order for evolution to work, we need to create copies of a genome, and apply random mutations to it. Let’s start by adding a `Clone`

method to the `GenomeLeg`

struct:

public GenomeLeg Clone () { GenomeLeg leg = new GenomeLeg(); leg.m = m; leg.M = M; leg.o = o; leg.p = p; return leg; }

As well as to the `Genome`

struct:

public Genome Clone () { Genome genome = new Genome(); genome.left = left.Clone(); genome.right = right.Clone(); return genome; }

It’s worth noticing that since they are *shallow structs*, there is no need for a `Clone`

method. Structs are treated like primitive types: they are always copied when passed or assigned.

The really interesting part of this tutorial is, obviously, mutation. Let’s start with the easy bit: mutating the `Genome`

struct. We randomly pick a leg and mutate it:

public void Mutate () { if ( Random.Range(0f,1f) > 0.5f ) left.Mutate(); else right.Mutate(); }

What we have to do now is taking the genome of a leg and apply a random mutation that can potentially improve its fitness. There are endless ways in which you can do that. The one I have chosen for this tutorial simply picks a random parameter and alter it by a small amount:

public void Mutate () { switch ( Random.Range(0,3+1) ) { case 0: m += Random.Range(-0.1f, 0.1f); m = Mathf.Clamp(m, -1f, +1f); break; case 1: M += Random.Range(-0.1f, 0.1f); M = Mathf.Clamp(M, -1f, +1f); break; case 2: p +=Random.Range(-0.25f, 0.25f); p = Mathf.Clamp(p, 0.1f, 2f); break; case 3: o += Random.Range(-0.25f, 0.25f); o = Mathf.Clamp(o, -2f, 2f); break; } }

The method `Mutate`

contains many *magic numbers*; constants that appears out of nowhere. While it is sensible to constraint the values of our parameters, deciding the extent of the mutation here is quite inefficient. A more sensible approach is to tune the change of a parameters according to how close we are to a solution. When you’re close to your target, you want to slow down to avoid overshooting and missing it. This aspect, often known as *adaptive learning rate*, is an important optimisation step that is not covered in this tutorial.

It is also worth noticing that changing values by small quantities can sometimes prevent better solution from being found. A better approach would, sometimes, randomly replace one of the parameters entirely.

This post explained how to represent the behaviour of the creature previously designed in a way that is amenable to evolutionary computation techniques.

**The next post will conclude this series about evolution, showing the last bit necessary: the evolution loop itself.**

#### Other resources

- Part 1.
[Evolutionary Computation: Theory](https://www.alanzucconi.com/?p=4730) - Part 2.
[Evolutionary Computation: Phenotype](https://www.alanzucconi.com/?p=4774) - Part 3.
**Evolutionary Computation: Genotype** - Part 4.
[Evolutionary Computation: Loop](https://www.alanzucconi.com/?p=4765)

## Leave a Reply Cancel reply