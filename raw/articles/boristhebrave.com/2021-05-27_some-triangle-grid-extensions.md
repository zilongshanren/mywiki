---
title: Some Triangle Grid Extensions
url: https://www.boristhebrave.com/2021/05/27/some-triangle-grid-extensions/
author: Boris
published: '2021-05-27'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Following [my article on triangle grids](https://www.boristhebrave.com/2021/05/23/triangle-grids/), I’ve been doing a lot more thinking about periodic grids. Here’s three neat things.

## Trihexagonal Tiling

![](../../assets/80b9efed6f048cd1.png)

[Trihex grids](https://en.wikipedia.org/wiki/Trihexagonal_tiling), also known by the mucher cooler “kagome lattices”, are a grid of alternating hexagons and triangles. It turns out we can use the exact same trick we did with triangle grids, and construct them as three overlapping sets of parallel lines, spaced double as wide as in the triangle grid case. Everything else works out straightforwardly from there, as I detail in [the source code](https://github.com/BorisTheBrave/grids/blob/main/src/flat_topped_trihex.py).

Despite being pretty, grids like this seem totally useless. I’ve never seem any computer or board games use a trihex grid. The best you can say is that if you have a hex grid where *both* the cells and vertices are relevant (such as [Settlers of Catan](https://en.wikipedia.org/wiki/Catan)), then you are really playing on a trihex grid.

Let me know if you’ve ever seen these in the wild, or are inspired to try using one.

## Quick Distance

One of the biggest shortcomings of a triangle grid is the distance function it comes with. I assumed that the natural distance between any two triangles is the number of edges you need to cross to walk from one cell to another. But the path from cell to another across edges can be pretty awkward. Given two triangles touching tip to tip, you need to take three steps around to get there.

What I failed to consider was whether other forms of movement might suit this grid better. Like how on a square grid, it’s often allowed to move diagonally in addition to adjacenctly.

Triangles are a bit more complicated than squares. If you consider all the triangles that share at least one vertex, there’s three different sorts of neighbours (called 1-neighbours, 2-neighbours, 3-neighbours):

Rasie1 gave an [excellent suggestion on reddit](https://www.reddit.com/r/gamedev/comments/nji0sf/how_to_use_triangle_grids/gzaw8s8?utm_source=share&utm_medium=web2x&context=3) – why not set the distance between a tile and its 3-neighbours to be 2 (instead of 3 as the old distance function sees it). Distance 2 seems a bit arbitrary, but actually there’s a lot of sense to it. It’s as if there was a a “shortcut” between tiles – you are allowed to step on the vertices as well as the cells. So to get to a 3-neighbour is two steps – step onto the vertex, then off again.

This is a much more sensible distance between the two triangles as you can draw straighter lines. In fact, it makes triangle distances behave very similarly to hex distances, which is one of the key reasons hex-distances are use used in the first place.

Fortunately, the new distance metric is also extremely easy to compute:

```
def tri_dist_alt(a1, b1, c1, a2, b2, c2):
"""Returns how many steps one tri is from another,
allowing steps onto vertices"""
da = a1 - a2
db = b1 - b2
dc = c1 - c2
return (abs(da - db) + abs(db - dc) + abs(dc - da)) / 2
```


Rasie1 has been working on their own triangle grid based game, so I’m not surprised they’re an expert in this sort of thing.

## Isometric Grids

Another question I got asked on reddit was about isometric grids.

Triangle grids are in fact a great way to work with isometric grids. Most of my illustrations are with rows of triangles, but if you use *columns* instead, then you right away get the classic isometric lines:

By picking pairs of triangles, you can easily draw isometric squares aligned horizontally or vertically. I’ve drawn a cube above by combining three pairs of triangles into rhombuses.

Generally I think it’s easier to think of isometric grids as a skewed square grid or even a 3d cube grid, like most tutorials show. But this representation is great if you want to draw a [Monument Valley](https://play.google.com/store/apps/details?id=com.ustwo.monumentvalley&hl=en_GB&gl=US) type game where the isometric space bends arounds like an Escher print.