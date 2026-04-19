---
title: Marching Cubes Tutorial
url: https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/
author: Boris
published: '2018-04-15'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

*How to Mesh without Mess*


In Minecraft, you can dig in any direction – removing a block at a time with well defined edges. But other games manage to destruct terrain smoothly, without all the blockiness of Minecraft.

Here’s [No Man’s Sky](https://www.nomanssky.com/), for example:

Similar use cases could be be displaying [MRI scans](https://www.youtube.com/watch?v=OS9NtvCnnBk), [metaballs](https://en.wikipedia.org/wiki/Metaballs) and voxelizing terrain.

The following tutorial in Marching Cubes, a technique for achieving destructible terrain, and more generally, creating a smooth boundary mesh to something solid. In this series, we’ll cover 2d in this first article, follwed by [3d in the next ](http://www.boristhebrave.com/2018/04/15/marching-cubes-3d-tutorial/), and [Dual Contouring in the third](http://www.boristhebrave.com/2018/04/15/dual-contouring-tutorial/). This last is a more advanced technique for achieving the same effect.

So let’s begin.

## The aim

First, let’s define exactly what we want to do. Suppose we have a function that can be sampled over an entire space, and want to plot the boundary. In other words identifying where the function switches from positive to negative, or vice versa. With the destructible terrain example, we’re interpreting the areas that are positive to be solid, and the areas that are negative to be empty.

A function is a great way of describing an arbitrary shape, but it doesn’t help you draw it.

To draw it, you need to know the **boundary**, i.e. the points between positive and negative, where the function crosses zero. The Marching Cubes algorithm takes such a function, and produces a polygonal approximation to the boundary, which can then be used for rendering. In 2d, this boundary will be a continuous line. When we get to 3d, a mesh.

## 2d Marching Cubes – Implementation

**Brevity Alert:**This tutorial covers concepts and ideas more than methods and code. If you are more interested in the implementation, make sure you check out the

[python implementation](https://github.com/BorisTheBrave/mc-dc/blob/a165b326849d8814fb03c963ad33a9faf6cc6dea/marching_cubes_2d.py), which contains commented example code with all the nitty gritty.

Let’s start in 2d for clarity. We’ll get to 3d later. I refer to both the 2d and 3d cases as “Marching Cubes” as they are essentially the same algorithm.

### Step 1

First, we split the space into a uniform grid of squares (cells). Then, for each cell, we can measure whether each vertex of the cell is inside or outside the solid by evaluating the function.

Below, I’m using function that describes a circle and colored each vertex black if that position evaluates to positive.

### Step 2

Then we process each cell individually, filling it with an appropriate boundary.

A [simple look up table ](https://github.com/BorisTheBrave/mc-dc/blob/a165b326849d8814fb03c963ad33a9faf6cc6dea/marching_cubes_2d.py#L19) provides the 16 possible combinations of the corners being inside or outside. For each case it describes what boundary needs to be drawn in each case.

### Step 3

Once you repeat over all the cells, the boundaries join up to create a complete mesh, even though each cell can be considered independently.

Nice! I guess it *kinda* looks like the original circle provided by the formula. But as you can see everything is all angular, with lines at 45 degree angles. That’s because we are choosing the boundary vertices (the red squares) to be equidistant from the points of the grid.

## Adaptation

The best way to fix the fact all lines are at 45 degree angles is **adaptive** marching cubes. Rather than merely setting all boundary vertices from the cell midpoints, they can be spaced to best match the underlying solid. To do this, we need to know more than what we just used – whether a point is inside or outside – we also need to know *how deep* it is.

This means we need a function that gives some measure of how far inside / outside it is. This doesn’t need to be precise as we only use it for approximations. In the case of our ideal circle, which has a radius of 2.5 units, we use the [following function](https://github.com/BorisTheBrave/mc-dc/blob/a165b326849d8814fb03c963ad33a9faf6cc6dea/marching_cubes_2d.py#L77).

\[ f(x, y) = 2.5 – \sqrt{x^2 + y^2} \]

Where positive values are inside, and negative values are outside.

We can use then use the numerical values of \(f\) on either side of an edge to [determine how far along the edge to put the point ](https://github.com/BorisTheBrave/mc-dc/blob/a165b326849d8814fb03c963ad33a9faf6cc6dea/common.py#L16).

When put together, it looks like this.

Despite having the exact same vertices and lines before, the slight adjustment in position makes the final shape much more circle-like.

## Continue Reading

To learn how to apply the Marching Cubes algorithm in 3d [here](https://www.boristhebrave.com/2018/04/15/marching-cubes-3d-tutorial/). Or if you want to jump ahead to an improved technique checkout [Dual Contouring](https://www.boristhebrave.com/2018/04/15/dual-contouring-tutorial/).