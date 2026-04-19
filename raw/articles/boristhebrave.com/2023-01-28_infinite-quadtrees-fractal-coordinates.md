---
title: Infinite Quadtrees – Fractal Coordinates
url: https://www.boristhebrave.com/2023/01/28/infinite-quadtrees-fractal-coordinates/
author: Boris
published: '2023-01-28'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

A cool technique I’ve wanted to write up for a while is “Fractal Coordinates” described in [a paper by Peter Mawhorter](https://cs.wellesley.edu/~pmwh/papers-fcpcg/FDG2021-Mawhorter-fractal-author.pdf). Don’t be scared by the name, it’s essentially a variant on [quadtrees](https://en.wikipedia.org/wiki/Quadtree) that covers the entire 2d plane. Fractal coordinates have some interesting properties that are useful for procedural generation.

But first, let’s catch up on quadtrees.

## Quadtrees

A quadtree is a “spatial partitioning” data structure, used for a variety of purposes like organizing and efficiently accessing a bunch of shapes arranged on a plane.

It works by starting with a square that bounds the whole region you are working with. That forms the root of the tree. Then we subdivide that square into 4 smaller squares, each half the size of the original. Those squares become the 4 nodes that are children to the root. We can keep subdividing those squares to get smaller and smaller descendants of the root, as needed for whatever application we have in mind.

Quadtrees are one of the simpler spatial data structures to work with. Unlike more complex trees like [R-trees](https://en.wikipedia.org/wiki/R-tree) or [K-d trees](https://en.wikipedia.org/wiki/K-d_tree), they are naturally self-balancing, as the subdivisions are made at fixed points. But that same self-balancing can also mean they subdivide the space less efficiently than other approaches, and often have many more nodes needed. I’ve used them for a experimental unreleased extension of Box2d to create gigantic terrains efficiently.

![](../../assets/86a736a6d571b455.gif)

## Going Infinite

One annoyance of a quadtree is that you have to know the region of interest in advance, because it is entirely based on subdivision. This makes working with infinite spaces difficult.

But as I’ve mentioned before, an infinite space is really just a finite space you can lazily evaluate and expand.

So, rather than thinking of quadtrees as subdivisions of a particular “root” square, we’ll instead consider it as a collection of square grids, each of which fully covers the plane.

**The level 0 grid** is the normal square grid. Each square is size 1, and has a coordinate (x,y). The square with coordinate (0, 0) for example, has bottom-left point (0, 0) and top-right (1, 1).

**The level 1 grid** is twice the size. Each square is size 2. So the square (0, 0) extends bottom-left (0, 0) and top-right (2, 2). Thus every square in the level 1 grid contains exactly 4 squares from the level 0 grid.

**The level 2 grid** is twice the size of the level 1 grid, so every square in this grid contains 4 squares from the level 1 grid, or 16 squares from the level 0 grid. We could also define the level -1 grid which is half the size of the level 0 grid.

We’ll use h (height) to describe which grid we’re talking about, so we can uniquely describe any square as ( h / (x, y) ), which is its fractal coordinate. So we could say that ( 1 / (0, 0) ) has 4 children:

- ( 0 / (0, 0) )
- ( 0 / (0, 1) )
- ( 0 / (1, 0) )
- ( 0 / (1, 1) )

In this way, we’ve defined a sort of “infinite tree”. Every square has exactly 4 children squares in the layer below, and one parent square, in the layer above.

![](../../assets/acbbffe8a9097a3b.gif)

Expressed as code:

```
def bottom_left(h, x, y):
size = 2 ** h
return (x * size, y * size)
def size(h, x, y):
return (2 ** h, 2 ** h)
def parent(h, x, y):
return (h + 1, floor(x / 2), floor(y / 2))
def children(h, x, y):
return [
(h - 1, 2 * x + 0, 2 * y + 0),
(h - 1, 2 * x + 1, 2 * y + 0),
(h - 1, 2 * x + 0, 2 * y + 1),
(h - 1, 2 * x + 1, 2 * y + 1),
]
```


Expressing the squares as coordinates like this is very convenient. You can move infinitely far horizontally or vertically, but also zoom in and out any amount by changing the level. We can construct a tree of nodes if needed for various purposes, but we can also talk about the squares not in the tree.

One approach that is handy is to keep a dictionary where the keys are a fractal coordinate. Compared with a tree, it’s much easier to locate a specific entry without walking down from the root. Useful for zoomable maps where you need to store quads at every zoom level.

## Alternating Coordinates

The actual coordinate system Peter introduces in his paper is slightly different. In the system above, ( 0 / (0, 0) ), is the **bottom-left child **of ( 1 / (0, 0) ), which is the **bottom-left child **of ( 2 / (0, 0) ), and so on. That means, no matter how high a level you go to, the origin of the plane will always be the corner of a square. Another problem is, no matter how high up the tree you go, the squares ( 0 / (0, 0) ) and ( 0 / (-1, 0) ) won’t have a parent in common, despite being right next to each other spatially.

Instead, what we’ll do is **alternate**. In the new system, ( 0 / (0, 0) ), is the **top-right child **of ( 1 / (0, 0) ), which is the **bottom-left child **of ( 2 / (0, 0) ), which is the **top-right **of… etc

![](../../assets/f0e71f9fc9aaabc3.gif)

The maths for this is a little fiddlier, but I’ve worked it out for you here:

```
def bottom_left(h, x, y):
offset = (4 ** ceil(h/2)) / 3
size = 2 ** h
return (x * size - offset, y * size - offset)
def size(h, x, y):
return (2 ** h, 2 ** h)
def parent(h, x, y):
if h % 2 == 0:
return (h + 1, floor((x + 1) / 2), floor((y + 1) / 2))
else
return (h + 1, floor(x / 2), floor(y / 2))
def children(h, x, y):
if h % 2 == 0:
return [
(h - 1, 2 * x + 0, 2 * y + 0),
(h - 1, 2 * x + 1, 2 * y + 0),
(h - 1, 2 * x + 0, 2 * y + 1),
(h - 1, 2 * x + 1, 2 * y + 1),
]
else:
return [
(h - 1, 2 * x - 1, 2 * y - 1),
(h - 1, 2 * x + 0, 2 * y - 1),
(h - 1, 2 * x - 1, 2 * y + 0),
(h - 1, 2 * x + 0, 2 * y + 0),
]
```


## Using Fractal Coordinates

Using alternating squares like this has a really nice property that normal quadtrees don’t have: **for any finite region of the plane you can find a single square that wholly contains it**.

```
def find_square_at_level(pos_x, pos_y, h):
(left, bottom) = bottom_left(h, 0, 0)
(s, _) = size(h, 0, 0)
dx = pos_x - left
dy = pos_y - bottom
return (h, floor(dx / s), floor(dy, s))
def find_containing_square(min_x, min_y, max_x, max_y):
# Start at the lowest level it could be
level = ceil(math.log2(max(max_x - min_x, max_y - min_y)))
# Keep walking up levels until we find one that contains everything
while True:
square1 = find_square_at_level(min_x, min_y, level)
square2 = find_square_at_level(max_x, max_y, level)
if square1 == square2:
return square1
level += 1
```


This is really handy! Suppose you are using the quadtree to store a bunch of shapes of various sizes. You can find the bounding square for each shape, and store the shape in that node of the tree. Then to find shapes in some given area, you can just walk over that part of the tree, a pretty easy operation.

Regular quadtrees are much more awkward – a shape might be covered by several different squares, so you need to track it in each of them, and worry about duplicates.

The original use of fractal coordinates is also pretty interesting. Peter defines a maze drawing algorithm, which randomly draws lines between squares, at every level of coordinates ( h ge 0 ).

![](../../assets/4a1687f25da31160.png)

You’d think if you have to draw lines for an infinite number of levels, the algorithm would never terminate. But we’re only interested in drawing a finite region. And the lines associated with a square are designed to never go near the center of that square, they are only near the borders. So though an infinite amount of larger and larger squares contain the region, only a finite number of them will actually draw lines inside the region, as the region will be too far from the edge of the larger ones.

So the drawing routine is: Find the smallest containing square for the region we want to draw, move up the tree a fixed number of steps, then recurse down the tree to draw all the squares inside it.

Because of this careful design, despite being relatively simple to evaluate, these mazes are infinite and **have structural detail at all levels**. The maze above, for example, guarantees that there is always a path from any point to any other point in the infinite plane. That’s a very tricky thing to design. The paper describes similar mazes with other properties – a maze with exactly one path between any two points, or a labyrinth that traverses the entire plane in a single line.

The paper also introduces scale factors other than a factor of two. At a scale factor of 5, each layer of squares is 5 times the size of the previous and holds 25 smaller squares. Odd scale factors don’t need any alternation, so are slightly easier to work with.

If you want to know more, check out the [slides](https://cs.wellesley.edu/~pmwh/papers-fcpcg/presentation/slides.html) and [youtube video](https://www.youtube.com/watch?v=CvPWZyf9nKQ).

I put off this post for a few years because I really wanted to *do* something with the idea. But having sat on it and done exactly nothing, I think it’s time to share. I’m sure this is a really useful concept, and yet I’ve struggled to find a killer use case. Can you suggest something?