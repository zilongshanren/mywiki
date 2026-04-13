---
title: Rate-distortion optimization
url: https://fgiesen.wordpress.com/2018/12/10/rate-distortion-optimization/
published: '2018-12-10'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Rate-distortion optimization

“Rate-distortion optimization” is a term in lossy compression that sounds way more complicated and advanced than it actually is. There’s an excellent chance that by the end of this post you’ll go “wait, that’s it?”. If so, great! My goal here is just to explain the basic idea, show how it plays out in practice, and maybe get you thinking about other applications. So let’s get started!

### What does “rate-distortion optimization” actually mean?

The mission statement for lossless data compression is pretty clear. A lossless compressor transforms one blob of data into another one, ideally (but not always) smaller, in a way that is reversible: there’s another transform (the decoder) that, when applied to the second blob, will return an *exact* copy of the original data.

Lossy compression is another matter. The output of the decoder is usually at least slightly different from the original data, and sometimes very different; and generally, it’s almost always possible to take an existing lossily-compressed piece of data, say a short video or MP3 file, make a slightly smaller copy by literally deleting a hundred bytes from the middle of the file with a hex editor, and get another version of the original video (or audio) file that is still clearly recognizable yet degraded. Seriously, if you’ve never done this before, try it, especially with MP3s: it’s quite hard to mangle a MP3 file in a way that will make it not play back anymore, because MP3s have no required file-level headers, tolerate arbitrary junk in the middle of the bitstream, and are self-synchronizing.

With lossless compression, it makes sense to ask “what is the smallest I can make this file?”. With lossy compression, less so; you can generally get files far smaller than you would ever want to use, because the data is degraded so much it’s barely recognizable (if that). Minimizing file size alone isn’t interesting; we want to minimize size while simultaneously maximizing the quality of the result. The way we do this is by coming up with some error metric that measures the distance between the original image and the result the decoder will actually produce given a candidate bitstream. Now our bitstream has two associated values: its length in bits, the (bit) *rate*, usually called R in formulas, and a measure of how much error was introduced as a result of the lossy coding process, the *distortion*, or D in formulas. R is almost always measured in bits or bytes; D can be in one of many units, depending on what type of error metric is used.

Rate-distortion optimization (RDO for short) then means that an encoder considers several possible candidate bit streams, evaluates their rate and distortion, and tries to make an optimal choice; if possible, we’d like it to be *globally* optimal (i.e. returning a true best-possible solution), but at the very least optimal among the candidates that were considered. Sounds great, but what does “better” mean here? Given a pair and another pair

, how do we tell which one is better?


### The pareto frontier

Suppose what we have 8 possible candidate solutions we are considering, each with their own rate and distortion scores. If we prepare a scatter plot of rate on the x-axis versus distortion on the y-axis, we might get something like this:

![Rate vs. Distortion scatterplot](../../assets/e2c2d4eea61d1045.png)


The thin, light-gray candidates aren’t very interesting, because what they have in common is that there is at least one other candidate solution that is strictly better than them in every way. That is, some other candidate point has the same (or lower) rate, and also the same (or lower) distortion as the grayed-out points. There’s just no reason to ever pick any of those points, based on the criteria we’re considering, anyway. In the scatterplot, this means that there is at least one other point that is both to the left (lower rate) and below (lower distortion).

For any of the points in the diagram, imagine a horizontal and a vertical line going through it, partitioning the plane into four quadrants. Any point that ends up in the lower-left quadrant (lower rate and lower distortion) is clearly superior. Likewise, any point in the upper-right quadrant (higher rate and higher distortion) is clearly inferior. The situation with the other two quadrants isn’t as clear.

Which brings us to the other four points: the three fat black points, and the red point. These are all points that have no other points to the left and below them, meaning they are [pareto efficient](https://en.wikipedia.org/wiki/Pareto_efficiency). This means that, unlike the situation with the light gray points, we can’t pick another candidate that improves one of the metrics without making the other worse. The set of points that are pareto efficient constitutes the *pareto frontier*.

These points are not all the same, though. The three fat black points are not just pareto efficient, but are also on the convex hull of the point set (the lower left contour of the convex hull here is drawn using blue lines), whereas the red point is not. The points that are both pareto and on the convex hull of the pareto frontier are particularly important, and can be characterized in a different way.

Namely, imagine taking a straightedge, angling it so that it’s either horizontal, “descending” (with reference to our graph) from left to right, or vertical, and then sliding it slowly “upwards” from the origin without changing its orientation until it hits one of the points in our set. It will look something like this:

![Rate vs. Distortion scatterplot with lines](../../assets/a52ed114416adfeb.png)


The shading here is meant to suggest the motion of the green line; we keep sliding it up until it eventually catches on the middle of our three fat black points. If we change the angle of our line to something else, we can manage to hit the other two black points, but not the red one. This has nothing to do with this particular problem and is a general property of convex sets: any vertices of the set must be extremal in some direction.

Getting a bit more precise here, the various copies of the green line I’ve drawn correspond to lines

and the constraints I gave on the orientation of the line boil down to (with at least one being nonzero). Sliding our straightedge until we hit a point corresponds to the minimization problem


for a given choice of w1 and w2, and the three black points are the three possible solutions we might get for our set of candidate points. So we’ve switched from purely minimizing rate or purely minimizing distortion (both of which, in general, tend to give somewhat pathological results) towards minimizing some linear combination of the two with non-negative weights; and doing so with various choices of the weights w1 and w2 will allow us to sweep out the lower left convex hull of the pareto frontier, which is often the “interesting” part (although, as the red point in our example illustrates, this process excludes some of the points on the pareto frontier).

This does not seem particularly impressive so far: we don’t want to purely minimize one quantity or the other, so instead we’re minimizing a linear combination of the two. That seems it would’ve been the obvious next thing to try. But looking at the characterization above does at least give us some idea on what looking at these linear combinations ends up doing, and exactly what we end up giving up (namely, the pareto points not on the convex hull). And there’s another massively important aspect to consider here.

### The Lagrangian connection

If we take our linear combination above and divide through by w1 or w2 (assuming they are non-zero; dividing our objective by a scalar constant does not change the results of the optimization problem), respectively, we get:



which are essentially the [Lagrangians](https://en.wikipedia.org/wiki/Lagrange_multiplier) we would get for continuous optimization problems of the form “minimize R subject to D=const.” (L1) and “minimize D subject to R=const.” (L2); that is, if we were in a continuously differentiable setting (for data compression we usually aren’t), trying to solve the problems of either minimizing bit rate while hitting a set distortion target or minimizing distortion within a given bit rate limit woud lead us to study the same type of expression. Generalizing one step further, allowing not just equality but also inequality constraints (i.e. rate or distortion *at most* a certain value, rather then requiring exact match) still leads to essentially the same functions, this time by way of the [KKT conditions](https://en.wikipedia.org/wiki/Karush%E2%80%93Kuhn%E2%80%93Tucker_conditions).

In this post, I intentionally went “backwards” by starting with the Lagrangian-esque expressions and then mentioning the connection to continuous optimization problems because I want to emphasize that this type of linear combination of the different metrics arises naturally, even in a fully discrete setting; starting out with Lagrange or KKT multipliers would get us into technical difficulties with discrete decisions that do not necessary admit continuously differentiable objectives or constraint functions. Since the whole process makes sense even without explicitly mentioning Lagrange multipliers at all, that seemed like the most natural way to handle it.

### What this means in practice

I hopefully now have you convinced that looking at the minima of the linear combination

is a sensible thing to do, and both our direct derivation and the two Lagrange multiplier formulations for continuous problems I mentioned lead us towards it. Neither our direct derivation nor the Lagrange multiplier version tells us what to set our mystery weight parameters to, however. In fact, the Lagrange multiplier method flat-out tells you that for every instance of your optimization problem, there *exist* the right values for the Lagrange multipliers that correspond to an optimum of the problem you’re interested in, but it doesn’t tell you how to get them.

However, what’s nice is that the same thing also works in reverse, as we saw earlier with our line-sweeping procedure: picking the angle of the line we’re sliding around corresponds to picking a Lagrange multiplier. No matter which one we pick, we are going to end up finding an optimal point for *some* trade-off, namely one that is pareto; it just might not be the exact trade-off we wanted.

For example, suppose we decide that a single-variable parameterization like in the Lagrange multiplier scenario is convenient, and we pick something like L1, namely w1 fixed at 1, w2 = λ. We were assuming from the beginning that we have some method of generating candidate solutions; all that’s left to do is to rank them and pick a winner. Let’s start with λ=1, which leads to a solution with some (R,D) pair that minimizes . Note it’s often useful to think of these quantities with units attached; we typically measure R in bits and [D] is whatever it is, so the unit of λ must be [λ] = bits/[D], i.e. λ is effectively an exchange rate that tells us how many units of distortion are worth as much as a single bit. We can then look at the R and D values of the solution we got back. If say we’re trying to hit a certain bit rate, then if R is close to that target, we might be happy and just stop. If R is way above the target bit rate, we overshot, and clearly need to penalize high distortions less; we might try another round with λ=0.1 next. Conversely, if say R is a few percent below the target rate, we might try another round with slightly higher lambda, say λ=1.02, trying to penalize distortion a bit more so we spend more bits to reduce it, and see if that gets us even closer.


With this kind of process, even knowing nothing else about the problem, you can systematically explore the options along the pareto frontier and try to find a better fit. What’s nice is that finding the minimum for a given choice of parameters (λ in our case) doesn’t require us to store all candidate options considered and rank them later; storing all candidates is not a big deal in our original example, where we were only trying to decide between a handful of options, but in practice you often end up with huge search spaces (exponential in the problem size is not unheard of), and being able to bake it down to a single linear function is convenient in other ways; for example, it tends to work well with efficient dynamic programming solutions to problems that would be infeasible to handle with brute force.

### Wait, that’s it?

Yes, pretty much. Instead of trying to purely minimize bit rate or distortion, you use a combination and vary λ to taste to hit your targets. Often, you know enough about your problem space to have a pretty good idea of what values λ should have; for example, in video compression, it’s pretty common to tie the λ used when coding residuals to quantizer step size, based on the (known) behavior of the quantizer and the (expected) characteristics of real-world signals. But even when you don’t know anything about your data, you can always use a search process for λ as outlined above (which is, of course, slower).


Now the one thing to note in practice is that you rarely use just a single distortion metric; for example, in video coding, it’s pretty common to use one distortion metric when quantizing residuals, a different one for motion search, and a third for overall block mode decision. In general, the more frequently something is done (or the bigger the search space is), the more willing codecs are to make compromises with their distortion measure to enable more efficient searches. In general, good results require both decent metrics and doing a good job exploring the search space, and accepting some defects in the metrics in exchange for a significant increase in search space covered in the same amount of time is often a good deal.

But the basic process is just this: measure bit rate and distortion (in your unit of choice) for every option you’re considering, and then rank your options based on their combined (or

, which is a different but equivalent parameterization) scores. This gives you points on the lower left convex hull of the pareto frontier, which is what you want.


This applies in other settings as well. For example, the various lossless compressors in Oodle are, well, lossless, but they still have a bunch of decisions to make, some of which take more time in the decoder than others. For a lossless codec, measuring “distortion” doesn’t make any sense (it’s always 0), but measuring decode time does; so the Oodle encoders optimize for a trade-off between compressed size and decode time.

Of course, you can have more parameters too; for example, you might want to combine these two ideas and do joint optimization over bit rate, distortion, and decode time, leading to an expression of the type with two Lagrange multipliers, with λ as before, and a second multiplier μ that encodes the exchange rate from time units into bits.


Either way, the details of this quickly get complicated, but the basic idea is really quite simple. I hope this post de-mystifies it a bit.