---
title: Fractals 101 - Alan Zucconi
url: https://www.alanzucconi.com/2016/08/17/fractals-101/
author: Alan Zucconi
published: '2016-08-17'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This new series of tutorials will explain what fractals are, why they are so important and what we can learn from them. This first lesson is a gentle introduction to the concept of iterated fractals and their dimension.

![Mandelbrot_sequence_new](../../assets/ee040114e8da137e.gif)

Since fractals naturally occur in nature, this series will be particularly interesting to all artists and game developers who want to create realistic outdoor environments.

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[Fractal Dimension](https://www.alanzucconi.com#part1) - Part 2.
[Measuring the Complexity](https://www.alanzucconi.com#part2) [Conclusion](https://www.alanzucconi.com#conclusion)

If you take a sphere and look close enough, you’ll reach a point in which its surface appears flat. We experience this every day on this very planet, but the idea works for every other traditional solid you can think of. Even the most detailed polyhedron will eventually look flat, if you zoom close enough. The true nature of a sphere is, in a nutshell, only appreciable at a certain distance. While this sounds obvious, there are geometric entities that escape this definition. **Fractals** – that’s how they’re called – are special shapes that gift us with an infinite level of detail. No matter how much you zoom on the its surface, a fractal will always offer more detail to look at. Even more bizarrely, some fractals exhibit a property called **self-similarity**: zooming on a part reveals the same complexity of the whole shape. This inception-like figures can be often created by iterating a process an infinite number of time.

![170px-Von_Koch_curve](../../assets/593c57a6ee95fb79.gif)

The animation on the left shows a [Koch snowflake](https://en.wikipedia.org/wiki/Koch_snowflake), which is a very simple type of fractal. It is created in steps, adding more complexity with each iteration. Its first iteration is a simple triangle. The next iteration takes the previous three edges and places a triangle on top of them, creating a six point star. The Koch snowflake only truly appears after an infinite amount of iterations. It is easy to see why it has an infinite amount of detail. The process which created is, by definition, creating an endless complexity. Each iteration increases the perimeter of the snowflake by a tiny amount; the real Koch snowflake has, in fact, an infinite perimeter.

There’s a specific reason why fractals are called like that. But in order to understand it, we need to first introduce the concept of **dimension**. We’re all familiar with the idea that lines are 1-dimensional entities, planes are 2-D and volumes are 3-D. But what truly makes a line 1-dimensional? The idea behind the concept of dimension lies in the intuition that any point in a 1-dimensional object only require a single number to be uniquely addressed. You can think about the problem in these terms: if you’re living on a street, each house is uniquely addressed by its house number. Which is, basically, the distance from the beginning of the street. Given a fixed origin (grey), each point on a 1-dimensional line (red) can be addressed by its distance from the origin itself (below, left).

![fractal](../../assets/261e0a1779e34450.png)

The same applies to a 2-dimensional shape, in which two coordinates are actually required to address each point . Whether they are expressed in Cartesian coordinates (up, middle) or polar coordinates (up, right), there’s no escape from the fact that two numbers are needed.

If we go back to the Koch snowflake presented in the previous section, we expect it to behave like a 1-dimensional entity, since it is made out of a single line. Unfortunately, a single number is not enough to uniquely identify a point on the curve. This is because the length between any two given points on a Koch snowflake is the same: infinity. The snowflake is not a 2-dimensional entity, since it has no surface, but it cannot be addressed with a single coordinate. Its dimension is somehow trapped between 1 and 2. The Koch snowflake has a dimension that is not an whole number, but a proper fraction: this is why is it said to have a **fractal dimension**.

![220px-Fractaldimensionexample](../../assets/5f64eb1541447e02.png)

There are different ways to measure this fractal dimension, depending on the way fractals are built. In the case of the Koch snowflake, the [Hausdorff dimension](https://en.wikipedia.org/wiki/Hausdorff_dimension) is used; it is a metric designed to capture how much the length, surface or volume of a fractal changes with each iteration. When you double a line, its length is also doubled (scaled by a factor of one). When you double the side of a rectangle, its area increases four times (scaled by a factor of two). When you double the edge of a cube, its volume increases eight times (scaled by a factor of three). Hence, their Hausdorff dimensions will be one, two and three, respectively.

![220px-Blueklineani2](../../assets/7dec716956efae57.gif)

To create a Koch snowflake, what we have to do is to scale each segment by a third, and copy it four time. The process is then repeated onto each new segment created. All fractals that are generated with such an iterative process have, by definition, fractal Hausdorff dimension equal to ![Rendered by QuickLaTeX.com \log_3 \left(4\right)\sim 1.26](../../assets/357142a09da2f1e2.png)


Wikipedia has an interesting list of fractals ([here](https://en.wikipedia.org/wiki/List_of_fractals_by_Hausdorff_dimension)), sorted by their Hausdorff dimension.

This post was a quick, gentle introduction to the concept of fractals. The next posts in this series will explore why fractals occur so often in nature, and why they’re so important.

![fractal_10](../../assets/3c43806290de896d.jpg)

#### Other resources

- Part 1.
**Fractals 101** - Part 2.
[Fractals 101: The Mandelbrot Set](https://www.alanzucconi.com/?p=5533)

## Leave a Reply Cancel reply