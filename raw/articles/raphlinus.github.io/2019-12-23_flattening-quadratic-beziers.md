---
title: Flattening quadratic Béziers
url: https://raphlinus.github.io/graphics/curves/2019/12/23/flatten-quadbez.html
author: Raph Levien’s blog
published: '2019-12-23'
source_blog: Raph Levien’s blog
source_site: https://raphlinus.github.io/
category: game programming
fetched: '2026-04-13'
---

A classic approach to rendering Bézier curves is to *flatten* them to polylines. There are other possibilities, including working with the Bézier curves analytically, as is done for example in [Random Access Vector Graphics](http://hhoppe.com/proj/ravg/), but converting to polylines still has legs, largely because it’s easier to build later stages of a rendering pipeline (especially on a GPU) that work with polylines.

A similarly classic approach to flattening Béziers to polylines is recursive subdivision. Briefly stated, the algorithm measures the error between the chord connecting the endpoints and the curve. If this is within tolerance, it returns the chord. Otherwise, it splits the Bézier in half (using de Casteljau subdivision) and recursively applies the algorithm to the two halves. This process is described in more detail in the paper [Piecewise Linear Approximation](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.86.162&rep=rep1&type=pdf). However, there are several reasons to be dissatisfied with this approach. For one, while it’s pretty good, it’s not particularly close to optimum in the number of curve segments. Perhaps of greater concern to a modern audience, the recursive approach adapts poorly any form of parallel evaluation, including GPU and SIMD. Allocation is also difficult, as the approach doesn’t tell you in advance how many subdivisions will be needed to achieve the specified tolerance.

The interactive demo below lets you switch between the recursive subdivision method and the new technique described in this blog, so you can see how the new technique achieves the error tolerance with significantly fewer segments.

A few other discussions of the recursive subdivision idea are on [antigrain](https://web.archive.org/web/20190329074058/http://antigrain.com:80/research/adaptive_bezier/index.html), [caffeineowl](http://www.caffeineowl.com/graphics/2d/vectorial/bezierintro.html), and [Stack Overflow](https://stackoverflow.com/questions/9247564/convert-bezier-curve-to-polygonal-chain). The latter thread also links to some other approaches. A common sentiment is “maybe we shouldn’t subdivide exactly in half, but be smarter exactly where to subdivide.” This blog post is basically about how to be smarter.

Working with cubic Bézier curves is tricky, but quadratic Bézier curves are pleasantly simple; they are something of a halfway station between cubics and straight lines. In this blog post, we present an analytical approach to flattening quadratic Bézier curves into polylines. It is so good that it’s probably best to flatten other curve types (including cubic Béziers) by converting them to quadratics first, then applying the technique of this blog post.

## How many segments?

The core insight of this blog post is a closed-form analytic expression for the number of line segments needed in the continuous limit.

For a small curve segment, the maximum distance between curve and chord can be approximated as $ \Delta y \approx \frac{1}{8}\kappa \Delta s^2 $. Here, $\kappa$ represents curvature, and we use $s$ to represent an infinitesimal distance, not to be confused with $t$ as commonly used to represent the parameter for the Bézier equation.

To simplify the presentation of the math here, we’ll solve the basic parabola $y = x^2$, rather than more general quadratic Béziers. However, all quadratic Béziers are equivalent to a segment of this parabola, modulo rotation, translation, and scaling. The first two factors don’t affect flattening, and the last can be taken into account by scaling the tolerance threshold. (For the curious, this transformation is `map_to_basic`

in the [code](https://github.com/raphlinus/raphlinus.github.io/tree/master/_posts/2019-12-23-flatten-quadbez.md) for this post.) Note that $x$ in this transformed version is a linear transform of $t$ in the source Bézier: it can be written $x = x_0 + t(x_1 - x_0)$.

The basic parabola has nice, simple expressions of curvature and infinitesimal arclength in terms of the parameter $x$:

\[\kappa = \frac{2}{(1 + 4x^2)^\frac{3}{2}}\] \[\Delta s = \sqrt{1 + 4x^2} \Delta x\]Plugging these into the above formula, we get an expression for the error:

\[\Delta y = \frac{(1 + 4x^2) \Delta x^2}{4(1 + 4x^2)^\frac{3}{2}}\]Holding the error fixed, we can now simplify and solve this for the step size of the parameter $x$ per segment.

\[\Delta x = 2 \sqrt{\Delta y} \sqrt[4]{1 + 4x^2}\]The rate at which segments occur is the reciprocal of the step size (here I’m also sneaking in a change to the continuous realm).

\[\frac{\mathrm{d}\; \mbox{segments}}{\mathrm{d}x} = \frac{1}{2\sqrt{\Delta y}\sqrt[4]{1 + 4x^2}}\]Taking this to the continuous limit, we can finally write a closed form expression for the number of segments required for the parabola segment from $x_0$ to $x_1$:

\[\mbox{segments} = \frac{1}{2\sqrt{\Delta y}} \int_{x_0}^{x_1} \frac{1}{\sqrt[4]{1 + 4x^2}} dx\]As it turns out, this integral has a closed form solution, thanks to [hypergeometric functions](https://en.wikipedia.org/wiki/Hypergeometric_function), though we won’t be making too much use of this fact; we’ll be doing numerical approximations instead. (I’ve left out the constant and am making the natural assumption that $f(0) = 0$, as it’s an odd function).

But no matter how we evaluate this integral, here we have an expression that tells us how many segments we need. To make sure the solution meets or exceeds the error tolerance, we round up to the nearest integer.

### Actually subdividing

Now we need to come up with $t$ values to know *where* to subdivide. Fortunately, given the mechanisms we’ve developed, this is fairly straightforward. I’ll actually show the code, as it’s probably clearer than trying to describe it in prose:

```
my_subdiv(tol) {
// Map quadratic bezier segment to y = x^2 parabola.
const params = this.map_to_basic();
// Compute approximate integral for x at both endpoints.
const a0 = approx_myint(params.x0);
const a2 = approx_myint(params.x2);
const count = 0.5 * Math.abs(a2 - a0) * Math.sqrt(params.scale / tol);
const n = Math.ceil(count);
const x0 = approx_inv_myint(a0);
const x2 = approx_inv_myint(a2);
let result = [0];
// Subdivide evenly and compute approximate inverse integral.
for (let i = 1; i < n; i++) {
const x = approx_inv_myint(a0 + ((a2 - a0) * i) / n);
// Map x parameter back to t parameter for the original segment.
const t = (x - x0) / (x2 - x0);
result.push(t);
}
result.push(1);
return result;
}
```


Essentially we’re subdividing the interval in “count space” into $n$ equal parts, then evaluating the *inverse function* of the integral at each of those points. This loop could easily be evaluated in parallel, and, as we’ll see below, the actual formula for the approximate inverse integral is quite simple.

## Numerical techniques

A great way to evaluate this integral is Legendre-Gauss quadrature, as described in my previous [arclength](https://raphlinus.github.io/curves/2018/12/28/bezier-arclength.html) blog. But we don’t actually need to compute this very precisely; we’re rounding up to an integer. I played around and found a nice efficient function with roughly the same shape (including asymptotic behavior). Blue is the true curve, orange is our approximation.

![Approximation of the integral](../../assets/4d48c209accf4443.png)


Reading this graph is fairly intuitive; the slope is the rate at which subdivisions are needed. That’s higher in the center of the graph where the curvature is highest.

I actually had even better luck with the inverse function of the integral, which is in some ways more important; this is the one that’s evaluated (potentially in parallel) for each intermediate point.

\[f^{-1}(x) \approx x \left(0.61 + \sqrt{0.39^2 + \tfrac{1}{4}x^2}\right)\]![Approximation of the inverse of the integral](../../assets/8d561329754819d1.png)


Essentially, the first approximation gives a direct and fairly accurate solution to determining the number of segments needed, and the second gives a direct and even more accurate solution to determining the $t$ parameter values for the subdivision, so that the error is evenly divided among all the segments.

An exercise for the reader is to come up with a better approximation for the first function.

## Comparison to related work

Probably the closest existing literature is the [Precise Flattening of Cubic Bézier Segments](https://pdfs.semanticscholar.org/8963/c06a92d6ca8868348b0930bbb800ff6e7920.pdf) work, which is also the basis of the flattening algorithm in the [lyon](https://docs.rs/lyon/0.4.1/lyon/Bézier/index.html#flattening) library. This approach also uses parabolas as an approximation, and greedily generates segments of the requested error tolerance.

My technique is both more efficient to evaluate, and also more accurate. Because we round the segment count up to the nearest integer, the error is always within the tolerance. Because “fractional segments” wouldn’t make sense, the error of at least one segment is in general considerably less than the threshold. Using a greedy approach, that lower error belongs to the final lucky segment. But our approach distributes the error evenly.

Though the theory is perhaps a bit math-intensive, the code is refreshingly simple. It can probably be used as a drop-in replacement in many implementations that use recursive subdivision for flattening.

And of course, the fact that it can be evaluated in parallel, as well as predict the number of generated segments in advance, means that it’s especially well suited for GPU. I’ll very likely use this technique as I reboot [piet-metal](https://github.com/linebender/piet-metal), though I’ll likely be exploring analytical approaches to rendering quadratic Béziers.

**Update 2019-12-25:** Alan MacKinnon pointed me to Sederberg’s [CAGD notes](https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1000&context=facpub#section.10.6), which has a simpler approach to the problem based on an error bound computed from the second derivative. This solution *is* quite well suited to parallel evaluation, and is easy to understand, but is less than optimum especially when the curvature varies a lot within the segment. Alan also pointed to a reference to Wang’s method in the book “Pyramid Algorithms” by Ron Goldman. You can experiment with these by pressing the “s” or “w” key in the demo above.