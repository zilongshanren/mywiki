---
title: Bresenham Lines
url: https://www.vertexfragment.com/ramblings/bresenham-lines/
author: Steven Sell
published: '2019-01-17'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

The Bresenham Line algorithm is an approach to drawing integer-based lines. It comes from a time when real-time rendering on PCs was nearly non-existant, and the drawing of a simple image was measured not in milli- or nano-seconds, but in seconds and minutes. It offered primitive lines at high speed, especially in it’s assembly form, at the cost of fidelity.

Developed in 1962, it was later supplanted by [Xiaolin Wu’s Line algorithm](https://en.wikipedia.org/wiki/Xiaolin_Wu%27s_line_algorithm) in 1992 which boasted fast antialiased lines (though slower then Bresenham). Wu’s arrival was nearly three decades ago, so of what use is Bresenham’s in 2019, 57 years after it’s initial development?

Well, sometimes you just need a simple, integer-based line algorithm. Which is exactly what Bresenham’s is.

To start, Bresenham uses only the slope of the line, in the form of x and y delta values. That, used in combination with the current position, is sufficient for plotting the line points.

The algorithm takes in a starting point `(x0, y0)`

and an ending point `(x1, y1)`

. It calculates the deltas and then begins to step along the line going from the start to the end. For each step, we always move once along the major line axis. If it is a horizontal line we always move along the x-axis, if it is a vertical line we always move along the y-axis.

All points in the plane can be split into two categories: those that lie exactly on the line, and those that are on one side of the line. During each step of the algorithm, we keep a running `error`

value which tracks how far off from the line the last point was.

When the `error`

value is too large (greater or equal to `0`

), then we move once along our minor axis. The pseudo-code for calculating the `error`

is as follows:

|
|

Intuitively this can be thought of as we move once along the minor axis each time the line moves halfway between cells along the minor axis. Or, the `error`

value is large enough that we know the next point on the minor axis is closer to the true line.

The graphic below shows the step-by-step progress of plotting a Bresenham line. Notice that only the first and last points are exactly on the line, and that we plot with an origin in the upper-left corner. Some adaptations have an origin in the center of the cell which misses the point that Bresenham is first and foremost an integer-based line.

As we step along the major `x`

axis we can see the `error`

increasing. Once it is greater or equal to zero, the `error`

is re-adjusted and we move once along the minor `y`

axis. The number of steps taken is always equal to the major delta plus one, so for a horizontal line we take `(x1 - x0) + 1`

steps.

Hopefully at this point you have an understanding of the Bresenham algorithm. Below is an implementation in C++, which can be easily adapted to any other language.

|
|

Cool, now what?

I assume that you came into this post with ideas in mind for what you were going to use Bresenham’s for. That you googled `2d line drawing`

or something similar, and if that is the case I will leave it to you to go forth and implement the algorithm for your own use.

However, if you stumbled upon this post by accident, or you knew what Bresenham’s was but didn’t have a good use for it, I will share my particular case.

In mid-2018 I began development on a modern Roguelike, [ Realms](https://www.vertexfragment.com/projects). Though it makes use of many newish technologies (Unity 5, C#, ECS programming, etc.) it, as a by-product of being a Roguelike, still has some old-school problems which require old-school solutions.

One such problem is calculating diagonal movement along a tile grid. In short, when traveling in the cardinal directions we can simply move one unit. The distance from `(0, 0)`

to `(1, 0)`

is 1. However moving diagonally from `(0, 0)`

to `(1, 1)`

the distance is √2 which isn’t quite as neat.

In fact, it can quickly start getting messy and you may begin contemplating using hex tiles instead. Plus there are addtional challenges when we want to move further than one space at a time, or we want to shoot a fireball at a far-away target. And that is where Bresenham’s comes in, and it can be seen in use by a multitude of games, including other Roguelikes such as [ Dungeon Crawl Stone Soup](https://crawl.develz.org).

*There is a follow-up ramble in which an implementation of Variable Length Bresenham Lines is discussed.*

![Bresenham Line in Dungeon Crawl Stone Soup Bresenham Line in Dungeon Crawl Stone Soup](../../assets/3cba67c69dd71d31.png)


- Abrash, Michael.
*Graphics Programming Black Book*. Coriolis, 1997, pp. 654–678.[http://downloads.gamedev.net/pdf/gpbb/gpbb35.pdf](http://downloads.gamedev.net/pdf/gpbb/gpbb35.pdf).