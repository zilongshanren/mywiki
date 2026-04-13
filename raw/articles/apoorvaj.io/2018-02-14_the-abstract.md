---
title: The abstract
url: https://apoorvaj.io/efficient-rendering-of-linear-brush-strokes
published: '2018-02-14'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

I wrote a graphics paper that was published by the Journal of Computer Graphics Techniques. This is the a hopefully simple explanation of it.

You can find the paper [here](http://www.jcgt.org/published/0007/01/01/) ([PDF](http://www.jcgt.org/published/0007/01/01/paper.pdf)).

While developing [Papaya](https://github.com/ApoorvaJ/Papaya), I looked at how
existing image editors implement brushing. I found that most of them
compute the [Bresenham
line](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm) joining the last mouse position, and its current position. Then
they add the brush stamp along that line.

![](../../assets/183d911708c95f36.png)


The GPU repeatedly writes to memory wherever the stamps overlap, which is bad for performance. This is also a classic problem in 3D realtime graphics, and is called overdraw.

The paper attempts to address this problem by rendering a single quad every frame instead of the many overlapping ones in the classic approach.

A brush stroke is controlled by four parameters:

Here’s a brush stroke with a low flow. Note how the left and the right pixels are less intense because they are overlapped by fewer stamps. This is also true to a lesser extent for the pixels on the upper and lower edges of the stroke.

![](../../assets/2592f626dc9d73e0.png)


Observe that the intensity at each pixel on the stroke depends on how
many stamps overlapped it. The pixels on the far right and left of the
stroke are only overlapped by one stamp and hence are the faintest. The
pixels along the central stroke axis are stamped by a *diameter*
amount of pixels.

The key insight of the paper is to model a stroke as if the stamp was continuously slid across the central stroke axis, instead of the traditional way of treating stamps as discrete additive blends.

In our new model, the stamp slides horizontally along the middle of the stroke. So the stamp is always at a point (x, 0.5), where x varies as the stamp slides.

For any given pixel (X,Y) in our stroke, we compute the function f(x, X, Y), which gives us the instantaneous alpha value contributed to that pixel when the center of the stamp is at (x, 0.5).

As the stamp slides from left to right, any given pixel is only inside the circular stamp for a finite amount of time. Stamps in the middle of the stroke stay inside for the longest, and hence have the most intensity.

We can find the centers of the first and the last circular stamp that touched any given pixel. Let’s call the first (left-most) center (X_1, 0.5) and let’s call the last (right-most) center (X_2, 0.5). This means that our pixel (X, Y) was inside the stamp as the stamp moved horizontally from X_1 to X_2.

Now, we can simply integrate over these two centers, and get the total alpha (i.e. intensity) that a pixel experienced while it was inside the sliding stamp:

\alpha(X,Y) = \int_{X_1}^{X_2} f(x, X, Y).dx

The alphabets here can get a bit confusing, so here’s a recap:

By doing this, we can compute the intensity at a point in one go, without having to repeatedly write to texture memory. This means we’re doing additional computations to reduce memory usage, which is usually a good thing.

With this technique, multiple strokes line up perfectly when blended additively as seen below. There are two strokes here, but you cannot tell them apart when they become the same color. This means we can get smooth, arbitrarily shaped strokes using chained line segments, which was not possible using my initial distance-based shader.

The paper describes how to compute these things when brush diameter, hardness and flow vary along the stroke, as is required when using pressure-sensitive input devices.

**The “Our Approach” section in the paper combines all of these
concepts into a succinct list of formulae that directly map to a pixel
shader. If you find the math scary, be sure to read the appendices; they
are a lot friendlier.**

**To reiterate, you can find the paper here (PDF).**

The paper has pretty comparison images. Be sure to check them out! Here are a few teaser images comparing the discrete method (top) vs this approach (bottom):

![](../../assets/63104deaa0c4f176.png)

![](../../assets/fa8d7015f6879fa5.png)