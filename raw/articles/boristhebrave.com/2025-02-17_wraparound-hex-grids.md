---
title: Wraparound Hex Grids
url: https://www.boristhebrave.com/2025/02/17/wraparound-hex-grids/
author: Boris
published: '2025-02-17'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

A user requested adding [wrapping hex grids](https://github.com/BorisTheBrave/sylves/blob/87ef03614e174b5deb9770661d71ccf360192bd2/src/Sylves/Grid/Extras/WrappingHexGrid.cs#L16) to [Sylves](https://www.boristhebrave.com/docs/sylves/1/). That is, a grid that is a collection of hexagons, and the collection itself is also hexagonal shaped. When you exit from one side, you re-enter on the opposite side.

The maths for this turned out to be surprisingly fiddly, and not listed by [RedBlobGames](https://www.redblobgames.com/grids/hexagons/#wraparound), so I thought I’d share it here.

The idea is to partition the full, infinite, grid of hexes into identical chunks, using [code from Sander Evers](https://observablehq.com/@sanderevers/hexagon-tiling-of-an-hexagonal-grid). Then we compute the translation from each chunk back to the central chunk. That allows us to identify every cell in the full grid with the central chunk, ensuring things wrap neatly.

```
from math import floor
def map_to_center(x, y, z, r):
"""
x,y,z contains the cell co-ordinates of a particular hex,
and r is the radius of the wrapping grid.
Returns a new cell co-ordinate x,y,z with
-r <= x <= r, -r <= y <= r, -r <= z <= r
"""
shift = 3 * r + 2
area = r * shift + r + 1
# Computes the co-ordinates of the big hex
# this cell is in
# https://observablehq.com/@sanderevers/hexagon-tiling-of-an-hexagonal-grid
var xh = floor((y + shift * x) / area)
var yh = floor((z + shift * y) / area)
var zh = floor((x + shift * z) / area)
var i = floor((1 + xh - yh) / 3f)
var j = floor((1 + yh - zh) / 3f)
# Translates that hex back onto the central one
x -= (2 * r + 1) * i + r * j
y -= -r * i + (r + 1) * j
z = -x - y
return x, y, z
```


If there’s a shorter way, let me know, this seems so inelegant!