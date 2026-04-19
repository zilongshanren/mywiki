---
title: Triangle Grids
url: https://www.boristhebrave.com/2021/05/23/triangle-grids/
author: Boris
published: '2021-05-23'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Ah, the triangle grid. Square grids are virtually ubiquitous, laying out out everything from the pixels in an image to houses in a city block. The hex grid has a decent showing too, particularly in board games. But triangle grids – regular tilings of the 2d plane with equilateral triangles – just don’t seem popular. I’ve seen claims they are useless, or that the maths is hard. But I’m here to prove both of these are wrong: the maths is actually **easier** than working with hexes, and triangles have all sorts of neat advantages.

I’ve worked out all the maths in my [reference code on github](https://github.com/BorisTheBrave/grids/blob/main/src/updown_tri.py), but it’s worth explaining why and how to use these grids.

Table of Contents

To be clear, when I say triangle grid, I mean a tile map where each tile is an equal sized equilateral triangle, arranged in alternating rows (or columns).

What’s important is every cell has exactly three neighbours. You sometimes see games with a drawn grid of triangles, but the actual pieces are placed on the *corners*. Each corner connects to six other corners, so this is not really a triangle grid, it’s actually a hexagon grid.

![Hamla](../../assets/ffd2127f975ee5c1.jpg)

**hex grid**, here styled to look triangular.

Conversely, any game played on the corners of a hexagon grid is actually a triangle grid. Uniform hexagon grids and triangle grids are called [ dual](https://mathworld.wolfram.com/DualTessellation.html) because of this property.

There’s three main reasons why triangles are awesome:

- They’re always planar
- They’re simple
- They have nicer geometry

If you pick any 3 points in 3d space, it’s possible to draw a flat plane through them. So given those three points, you can always draw a triangle on the surface of that plane. That’s not true for polygons with more vertices. If you pick 4 3d vertices, connecting them to up to form a 4 vertex polygon becomes difficult to do in a sensible unambiguous way. Polygons suffering this problem are called **non-planar**, and they can be a big problem in computer graphics – nearly all realtime graphics converts everything to triangles to avoid this problem.

Even though I’m here to talk about 2d tilings, this is still a useful property if we want to introduce a heighmap. With a triangle grid, you can have every vertex at a different height, and it’ll still work perfectly. Do the same with a square grid, and you immediately run into non-planar vertices.

![](../../assets/58f1064a65656a81.png)

![](../../assets/a640bb306fed30fe.png)

It’s a mathematical fact that 3 is less than 4 or 6 [citation needed]. That’s the smallest number of vertices a polygon can have, making triangles the best shape for any algorithm that scales with the number of points or edges.

For example, when in my tutorial on [Marching Cubes](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/), I explained that you need to create \( 2^4 = 16 \) different tiles in order to cover all cases in 2d. That’s because each of the 4 corners has 2 choices. Triangles come in two varieties, up and down, and each variety needs \( 2^3 = 8 \) different tiles. So you are creating 16 tiles either way.

But that’s just the basic case. If you allow for tile rotations, then triangles have less cases (4 vs 6). Or if you want [more than 2 possible values](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/3corn.html) at each corner (54 vs 81, or 10 vs 21 with rotations/reflections).

Here’s a [ShaderToy](https://www.shadertoy.com/view/WtfGDX) showing marching cubes on a triangle.

Triangles are also good for linear interpolation. Interpolating three values accross a triangle is straightforward with [Barycentric Co-ordinates](https://observablehq.com/@jobleonard/linear-interpolation-along-a-triangle-with-barycentric-co), while squares require [bilinear interpolation](https://en.wikipedia.org/wiki/Bilinear_interpolation) which is fundamentally more complex. This difference is why [Simplex Noise](https://en.wikipedia.org/wiki/Simplex_noise) was invented to replace Perlin Noise – they work the same, but simplex noise uses a triangle grid (in 2d).

When working with hexes, you quickly realize their **edges **are a huge pain. They don’t line in a straight line! That makes it impossible to subdivide the grid with a line. You cannot build a big hex out of lots of little ones.

In the next section, we’ll rely heavily on straight edge lines for intuition about how triangle grids work.

Triangles are also very good if you are working on a sphere (e.g. for a planet simulator) – it’s possibly to make a uniform sphere mesh out of just triangles, but using squares or hexes requires having some special areas that behave oddly, like the poles, or the pentagons on a traditional football design.

Admittedly, triangle grids do have their own geometry annoyances, mostly to do with how you need to handle triangles pointing in different directions.

**Brevity Alert:**This tutorial covers concepts and ideas more than methods and code. If you are more interested in the implementation, make sure you check out

[the reference implementation](https://github.com/BorisTheBrave/grids/blob/main/src/updown_tri.py)I’ve made.

Ok, I should preface this section by saying there are many different ways to work with triangle grids. What I’m going to describe here is the one I think is best – it’s simple to understand, and has simple expressions for nearly everything you are likely to do with triangles. I’m going to describe triangle arranged in rows (“up-down” triangles), but everything works similarly for grids rotated 90 degrees.

The trick is to think of a triangle grid as defined by three sets of evenly spaced parallel lines overlaid on each other:

The space between each of those parallel lines are called **lanes**. We’ll call the three different directions of lanes a, b, and c, and number the lanes in order.

Then the co-ordinate for a triangle is simply three integers a, b, c which describe what lanes the triangle can be found in. It’s that simple!

You might be wondering why we use three numbers to represent a cell in a 2d grid. It just works out more conveniently this way. If you try use a two-number co-ordinate system, you end up having to make more even-odd exceptions or other inconsistencies. A similar trick is used when working with Hex grids, see [this article on “cube” co-ordinates for hex grids](https://www.redblobgames.com/grids/hexagons/#coordinates-cube). The third co-ordinate is mostly redundant though – in this system a + b + c always sums up to either 1 or 2. So you could just store a, b and an extra boolean.

Note there’s no triangle with co-ordinates (0, 0, 0). I’ve numbered the lanes so that the origin is actually a vertex, surrounded by the 6 triangles in lanes 0 and 1. The system works just as well with different lane numberings.

Whenever you move from one triangle to another, you are crossing one of the lines separating lanes. I’ve arranged it so that to move out of a downwards pointing triangle, you add one to a co-ordinate. And for an up triangle, you subtract one.

```
def tri_neighbours(a, b, c):
"""Returns the tris that share an edge with the given tri"""
points_up = a + b + c == 2
if points_up:
return [
(a - 1, b , c ),
(a , b - 1, c ),
(a , b , c - 1),
]
else:
return [
(a + 1, b , c ),
(a , b + 1, c ),
(a , b , c + 1),
]
```


Because moving to adjacent triangles is always a step of a given size in one of the three lanes, the given triangle can be found just by summing up all the steps taken in the three different directions.

```
def tri_center(a, b, c):
"""Returns the center of a given triangle in cartesian co-ordinates"""
return (( 0.5 * a + -0.5 * c) * edge_length,
(-sqrt3 / 6 * a + sqrt3 / 3 * b - sqrt3 / 6 * c) * edge_length)
```


As every step is changing a co-ordinate by one, the formula for distance is just the difference in each co-ordinate.

```
def tri_dist(a1, b1, c1, a2, b2, c2):
"""Returns how many steps one tri is from another"""
return abs(a1 - a2) + abs(b1 - b2) + abs(c1 - c2)
```


I discuss an alternative distance function in [a followup article](https://www.boristhebrave.com/2021/05/27/some-triangle-grid-extensions/).

To locate the triangle containing a given point, you just need work out what three lanes the triangle is in. This can be done by measuring the distance perpendicular to the lane from the origin, easily done with a [dot product](https://en.wikipedia.org/wiki/Dot_product), then truncating from a floating point to an integer.

```
def pick_tri(x, y):
"""Returns the triangle that contains a given cartesian co-ordinate point"""
return (
ceil(( 1 * x - sqrt3 / 3 * y) / edge_length),
floor(( sqrt3 * 2 / 3 * y) / edge_length) + 1,
ceil((-1 * x - sqrt3 / 3 * y) / edge_length),
)
```


`ceil`

rounds a number *up* to the nearest integer, and `floor`

rounds *down*. You can’t just round all three lanes in the same direction or you end up with difficulties when dealing with points like (0, 0), which lie at the corner of 6 different triangles.

There’s many other operations you might want to do on a grid, like measure distances, draw lines, and rotations. All these are described in detail in [my reference implementation](https://github.com/BorisTheBrave/grids/blob/main/src/updown_tri.py), on github.

You can compare them to the [hex grid implementation](https://github.com/BorisTheBrave/grids/blob/main/src/flat_topped_hex.py). Triangles are so much simpler than hexes that I’ve implemented many hexagon operations by first doing the equivalant triangle operation, then converting to hexes.

Hopefully I’ve convinced you that triangle grids are an underappreciated tool.

[Tessera](https://assetstore.unity.com/packages/tools/level-design/tessera-procedural-tile-based-generator-155425)

RedBlobGaming’s write up of [grids](http://www-cs-students.stanford.edu/~amitp/game-programming/grids/) is still the best place to get started with understanding grids. I hear they are working on an updated copy too.

I can also recommend [Justin Pombrio’s article on pixel to hex conversions](https://justinpombrio.net/programming/2020/04/28/pixel-to-hex.html), which turned me on to how neatly this triangle system works, and how it relates to hex grids.

I also have worked on triangular grids, though I used the hex dual to define the points as opposed to the center of the triangle. My work is based on the QRS coordinate system put forward by redblobgames. You can find my paper write up at https://davehardee.com/QRSCoords/