---
title: Conway's Game of Life
url: https://www.4rknova.com/blog/2013/01/27/game-of-life
author: Nikolaos Papadopoulos
published: '2013-01-27'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Theory

Conway’s game of life is a cellural automaton. It was invented by John Horton Conway, an English mathematician.

A 2D plane is subdivided into a grid where each cell is either occupied or not. The simulation follows the following set of rules:

- Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
- Any live cell with more than three live neighbours dies, as if by overcrowding.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any dead cell with exactly three live neighbours becomes a live cell.

# Implementation

Here’s an implementation of the algorithm in GLSL. Each frame stores a snapshot of the simulation’s state and is used as an input for the frame after.

```
#define GRID_SZ (iResolution.xy)
uint hash( uint x )
{
x += ( x << 10u );
x ^= ( x >> 6u );
x += ( x << 3u );
x ^= ( x >> 11u );
x += ( x << 15u );
return x;
}
uint hash( uvec2 v )
{
return hash( v.x ^ hash(v.y) );
}
float random( vec2 f )
{
const uint mantissaMask = 0x007FFFFFu;
const uint one = 0x3F800000u;
uint h = hash( floatBitsToUint( f ) );
h &= mantissaMask;
h |= one;
float r2 = uintBitsToFloat( h );
return r2 - 1.0;
}
float get_cell(vec2 p, vec2 d)
{
return texture(iChannel0, (p + d) / GRID_SZ).r > 0. ? 1. : 0.;
}
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
vec2 uv = fragCoord.xy / iResolution.xy; // UV coordinates
vec2 gc = floor(GRID_SZ * uv) + 0.5; // Grid Coordinates
if (iFrame == 0) {
fragColor = vec4(step(random(gc), 0.5));
return;
}
bool is_alive = get_cell(gc, vec2(0)) > 0.;
const vec3 o = vec3(0,1,-1); // Offsets
float count = get_cell(gc, o.yx)
+ get_cell(gc, o.zx)
+ get_cell(gc, o.xy)
+ get_cell(gc, o.xz)
+ get_cell(gc, o.yy)
+ get_cell(gc, o.zz)
+ get_cell(gc, o.zy)
+ get_cell(gc, o.yz);
float res = 0.;
if (is_alive) {
// 1. Any live cell with fewer than two live neighbours dies,
// as if caused by underpopulation.
// 2. Any live cell with more than three live neighbours dies,
// as if by overcrowding.
if (count < 2. || count > 3.) res = 0.;
// 3. Any live cell with two or three live neighbours lives on
// to the next generation.
// Health points are stored in the map based on the number of
// neighbours.
else if (count == 2. || count == 3.) res = 1./count;
}
// 4. Any dead cell with exactly three live neighbours becomes a
// live cell.
else if (count == 3.) res = 1.;
fragColor = vec4(res);
}
```


Below is a live preview of the simulation. Click and hold the left mouse button for a closer view at any part of the map.