---
title: 2d Marching Cubes with Multiple Colors
url: https://www.boristhebrave.com/2021/12/29/2d-marching-cubes-with-multiple-colors/
author: Boris
published: '2021-12-29'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

**2d Marching cubes **(sometimes called **marching squares**) is a [way of drawing a contour around an area](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/). Alternatively, you can think of it as a drawing a dividing line between two different areas. The areas are determined by a boolean or signed number value on each vertex of a grid:

But what if we didn’t have a boolean value? What if we had *n* possible colors for each vertex, and we wanted to draw separating lines between all of them?

Catlike Coding has an [extremely in depth tutorial](https://catlikecoding.com/unity/tutorials/marching-squares-5/) on how to do exactly that. But I found his approach pretty complex, as it is Unity-specific, and has a lot of code dealing with sharpness. As I’ve discussed before, sharpness is really a [Dual Contouring](https://www.boristhebrave.com/2018/04/15/dual-contouring-tutorial/) feature – Marching Cubes doesn’t normally have it.

So I’ve designed an approach for multiple colors that I think better preserves the essence of marching cubes. Like in [my original tutorial](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/), every cell (grid square) is evaluated separately, and does the following steps

**Determine what case**to use for this cell*(optional)***Adapt the case**to better fit the true contour- Output the edges from that case.

## Determining the Case

Marching cubes originally had 16 cases. That’s because there are 2 possibilities for each of the four vertices of the cell, and 2*2*2*2 = 16.

Does that mean if we now have 5 colors, we now need support 5*5*5*5 different cases? No. We don’t really care about which specific colors are at which vertex. We just care about where to draw boundaries, which only means we need to know which vertices have the same colors, and which ones are different. In the end, you only need 15 different cases to cover all possible combinations.

The above lists all the cases. The circles in the corner are the vertex coloring, and the red lines are the output for each case.

I show 4 different colors, white, red, green and blue, which are associated with 0,1,2,3. All other possible combinations can be transformed into one of the above, simply by relabelling colors until they are in the correct order.

In other words, whichever color is in the top right, call that “0”. Then move counter-clockwise. The next color you see will be color 1, the next after that 2, and if you see a fourth color, then it is called 3. You can never have more than four relevant colors as there are only four vertices.

Here’s some python code for doing exactly that:

```
def classify(case):
labels = dict()
uniq_case = []
for corner in case:
uniq_case.append(labels.setdefault(corner, len(labels)))
return uniq_case
# E.g. classify("RGRG") == [0, 1, 0, 1]
```


We can then use a bit counting trick to find a single number for a case, similar to the normal marching cubes.

```
def uniq_case_id(uniq_case):
return uniq_case[1] * 16 + uniq_case[2] * 4 + uniq_case[3]
# E.g. uniq_case_id([0, 1, 0, 1]) == 17
```


Each case dictates exactly what boundary lines to draw (or polygons, if you are filling things in). Case 17 is special, it is ambiguous, exactly like in the normal marching cubes case.

## Adaptivity

If you just uses the cases as is, then the generated output will look very blocky – all the lines are at 45 degree angles. Just like in original marching cubes, if we shift the output vertices around, we can get a much better fit without having to add much more complication.

For marching cubes, adapativity needed a signed number per-vertex: positive values indicates inside the area, and negative values outside. Now we have multiple colors, we’ll forget the positive negative thing. For each vertex, store the color, and the **weight**. The weight is a positive number which indicates how much this vertex pushes the boundary away from it. Usually you can derive weights from the true shape you are trying to draw – the weight should be the distance from the current vertex to the shape boundary.

If the boundary is between two vertices of different colors and with weights `w1`

, and `w2`

, then we need to interpolate between the two vertices as follows:

```
t = w1 / (w1 + w2)
return interp(t, v1, v2)
# Or equivalently
return (v1 * w2 + v2 * w1) / (w1 + w2)
```


Unlike the original marching cubes, we also have to worry about cases where we need to draw a vertex in the **middle** of the cell. I recommend the following formula for this.

`return (v1 / w1 + v2 / w2 + v3 / w3 + v4 / w4) / (1 / w1 + 1 / w2 + 1 / w3 + 1 / w4) `


Of you could do something similar to [dual contouring](https://www.boristhebrave.com/2018/04/15/dual-contouring-tutorial/), which has a more sophisticated way of finding the appropriate middle.

## Summary

That’s pretty much it. As in normal marching cubes, you iterate (“march”) over every cell and apply the above to every cell in the grid. The edges will automatically line up, though in more sophisiticated implementations you automatically share data between cells to avoid extra computation and give a contuous boundary.

Note that this technique is only really useful in 2d. In 3d, I’d recommend that you just to regular marching cubes to get a single sufaces for all colors, then use a pixel shader or triangle subdivision to colorize that surface.

No code is available this time – I’m too lazy to actually implement the above, so let me know if it works out for you!