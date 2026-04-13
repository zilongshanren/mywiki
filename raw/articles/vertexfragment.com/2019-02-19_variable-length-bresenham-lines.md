---
title: Variable Length Bresenham Lines
url: https://www.vertexfragment.com/ramblings/variable-length-bresenham-lines/
author: Steven Sell
published: '2019-02-19'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

In my [previous ramble](https://www.vertexfragment.com/bresenham-lines), we explored the standard Bresenham algorithm for drawing 2D integer-based lines.

This time I will present a *deoptimized* variation of the Bresenham line. But first lets take a step back and review what exactly the standard algorithm sets out to achieve, which can be summed up as follows:

The Bresenham algorithm efficiently plots a line from an integer point

`(x0,y0)`

to`(x1,y1)`

.

But what if we want a variable length line? That starts from `(x0,y0)`

but continues on for a specified range? In that case the standard implementation is insufficient due to its highly optimized nature.

The Bresenham algorithm defines lines based on octants, which is illustrated in the above graphic. Red-shaded octants represent horizontal (x-dominant) lines wheras green-shaded octants represent vertical (y-dominant) lines.

However, there is a clever optimization that the standard algorithm employs so that it must only consider four of the octants:

- Left-to-right, bottom-to-top (+x, +y) (horizontal)
- Right-to-left, bottom-to-top (-x, +y) (horizontal)
- Left-to-right, bottom-to-top (+x, +y) (vertical)
- Right-to-left, bottom-to-top (-x, +y) (vertical)

As you can see, Bresenham considers only the top-half of the octants and all lines are drawn from bottom-to-top. This is achieved by the swaps performed at the very beginning of the `plotBresenham`

function which ensures that the line drawing always begins at the bottom. Regardless of whether the starting point `(x0,y0)`

is the bottom or the top.

Because of this, depending on orientation, the line drawing will sometimes start at the first point `(x0,y0)`

and at other times it will start at the last point `(x1,y1)`

. However, if we want to draw a variable length line we must always begin drawing at the starting point. This behavior is demonstrated in the demo below, where the line gets darker as it gets further along the drawing. You can see that depending on the line the starting point is either at the line start (grid center) or at the line end (mouse location).

*(Keep in mind that HTML5 canvas elements have their origin at the top-left.)*

If we attempt to draw a variable length line starting at the end then it will result in a line that is moving opposite of the intended direction, overshooting the starting point. So how can we overcome this deliberate behavior?

Fortunately, drawing a variable length line with Bresenham requires only a few modifications. Primarily we have to unwind our implementation and explicitly handle lines from all octants, and not just the four comprising the top half.

Once we handle all octants we then need to update the horizontal and vertical functions to iterate over the specified distance and not just from `(x0,y0)`

to `(x1,y1)`

.

So to start, we first modify the `plotBresenham`

function to remove the starting point swap and we also check against all octants:

|
|

Wait, thats it? Checking against all eight octants is less than half the code of checking only four of them? This is primarily possible since we use the absolute of the delta to determine whether its a horizontal or vertical line, instead of the original implementation which must check if the delta is negative.

The other two functions, `plotBresenhamHorizontal`

and `plotBresenhamVertical`

, receive only minor adjustments as well to handle variable length lines.

|
|

And thats all there is. We can now draw variable length Bresenham lines starting from `(x0,y0)`

, we can also continue to draw only to `(x1,y1)`

if the `range`

parameter is set to zero. In either case, the lines are always drawn from start to finish.

At this point we can compare the performance of both implementations, as Bresenham was originally designed to be fast.

Surprisingly, however, the variable-length algorithms slightly outperforms the standard implementation in [JavaScript performance tests](https://jsperf.com/bresenham-comparison/3). On my development machine running Chrome v72.0, the results are as follows:

| Implementation | Ops/sec | % |
|---|---|---|
| Standard Bresenham | 47,432,265 | 97.35% |
| Variable Length Bresenham | 48,722,462 | 100.00% |

Much could probably be said about the advancements in the past several decades that have allowed for the intentionally *unoptimized* version to outperform the optimized one, but all that we need to know is that the difference in performance when using the variable length algorithm is at worst negligible.

None this time.