---
title: GPU Sorting - Alan Zucconi
url: https://www.alanzucconi.com/2017/12/13/gpu-sorting-1/
author: Alan Zucconi
published: '2017-12-13'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This article introduces the concept of **parallel sorting**, discussing the theory and implementation of a shader that can sort pixels.

![](../../assets/0bc0c0585a487cf6.gif)

You can read the full series here:

- Part 1.
**GPU Sorting** - Part 2.
**GPU Sorting**

You can find a link to download the **Unity source code** at the end of this tutorial.

#### Introduction

If you did not study Computer Science in the 80s or 90s, chances are you will struggle to understand the excitement some developers have for **sorting algorithms**. What could seem at first like a minor task, turns out to be a cornerstone of Computer Science.

But first of all, what *are* sorting algorithm? Imagine that you have a list of numbers. A sorting algorithm is a program that takes that same list and reorders its numbers. Sorting algorithms are often introduced during the study of **Computational Complexity**, another vast subject that will be covered extensively in a future series. There are countless ways in which a list of items can be sorted, and each strategy offers a unique trade-off between cost and performance.

Most of the complexity of sorting algorithms comes from the way the problem is defined and approached. In order to decide how to rearrange the elements, an algorithm must compare numbers. In the scientific literature, each comparison performed adds up to the complexity of the algorithm. The number of comparisons one performs is the way complexity is measured.

However, things are not that easy: the number of comparisons and swaps depend on the list itself. This is why in the field of Computational Complexity there are more objective ways to measure the performance of an algorithm. What is the worst possible scenario for an algorithm? How many steps will it take, at most, to sort the most un-sorted list it can work with? Such a way to approach the problem is known, unsurprisingly, as **worst-case scenario** analysis. We can ask the same question for the best-case scenario. What is the minimum amount of comparisons that an algorithm has to perform to sort an array? Loosely speaking, the latter is often with the **Big O notation**, which measures complexity as a function of the number of elements to sort, ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com \mathcal{O}\left(n\log n\right)](../../assets/4858e7aec78dcc4c.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n\log n](../../assets/07e2d108e0853111.png)


#### The Limitations of the GPU

Traditional sorting algorithms are built based on two simple concepts:

**Comparison**: the act of comparing two elements of a list, in order to decide which one is larger;**Swaps**: the act of swapping the position of two elements, in order to bring the list in a new state that is closer to the desired one.

The list to be sorted is often given in the form of an array. Accessing random elements of an array is extremely efficient, and it is possible to swap any two elements with no restrictions.

If we want to use a shader to sort, we first need to understand the intrinsic limitations of this new medium. While it is possible to provide a list of number to a shader, that is not the best way to exploits its parallelism. Conceptually, we can imagine the GPU executing the same shader code on each pixel, at the same time. This is not generally what happens, since a GPU is unlikely to have the computational power to parallelize the computation for each pixel. Some parts of the image *will* be processed in parallel, but we shouldn’t make any assumptions on which ones. For this reason, the shader code has to operate under the same constraints of *true* parallelism, even if in reality that is not necessarily how it runs.

The most serious constraint, however, is the fact that the shader code is localised. If the GPU is executing a piece of code on a pixel at coordinate ![Rendered by QuickLaTeX.com \left[x, y\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-818eb0603d8252dd120528445166c7d9_l3.png)

![Rendered by QuickLaTeX.com \left[x, y\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-818eb0603d8252dd120528445166c7d9_l3.png)


### ⭐ Recommended Unity Assets

#### Sorting on a GPU

The approach presented in this tutorial is conceptually simple.

- The data to sort is provided in a texture;
- If we have an array of

elements, we create a texture of size

pixels; - The value in the red channel of each pixel contains the number to sort;
- Each rendering pass will bring the array
*closer*to its final state.

For example, let’s imagine we have a list of fours numbers to sort: ![Rendered by QuickLaTeX.com \left[4,3,2,1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-00610a37ca37ec793b18c6853bb640a0_l3.png)

![Rendered by QuickLaTeX.com 4\times 1](../../assets/931ca58f69c1423a.png)


![](../../assets/90d2f5e4dbafab75.png)

As discussed before, the swap operation is much more complex when done in a shader, since it needs to be executed in parallel by two independent pixels. The easiest way to work with such a limitation is to swap nearby couples of pixels (below):

![](../../assets/2c95fce6b98c53f4.png)

It’s important to notice that, conversely to what happens on a CPU, the process happens somehow in reverse. The first pixel samples its previous value, ![Rendered by QuickLaTeX.com 4](../../assets/0725b22597534378.png)

![Rendered by QuickLaTeX.com 3](../../assets/dc7e9389c9a6a6e2.png)

**swap couple**, it needs to take the smaller one. The second pixel in the couple needs to perform the opposite operation.

Since those calculations are done independently, both pieces of code should agree on which value to propagate down without any communication. This is where the challenge of parallel sorting lies. If we are not careful, both pixels in the swap couple could pick the same number, de-facto duplicating it.

If we repeat this swapping process, nothing would change. Each couple can be sorted in a single step. Replicating this process will not lead to any changes. The way to overcome this, is to change the swapping couples. We can see this in the diagram below:

![](../../assets/2202dbe559506c47.png)

We can keep alternating these two steps, until the entire image is sorted:

![](../../assets/ac1d55a5ee5d1c41.png)

Such a technique has been around for quite a long time, and it exists in many different flavours and variations. It is often referred to as [ odd-even sort](https://en.wikipedia.org/wiki/Odd%E2%80%93even_sort), since it alternates swaps between odd/even and even/odd indices. It’s working mechanism is deeply connected with the bubble sort, so it is not surprising to find this algorithm under the name of

**parallel bubble sort**.

#### Complexity

When working on a GPU, we should assume that the same shader code is executed on each pixel independently, and at the same time. In a traditional CPU, we should consider each comparison/swap as an individual operation. A shader pass would count as ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


What is the complexity in the worst case scenario? We can see that each step brings a pixel closer to its final position. The further a pixel can travel is ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)


If we look at this problem from a more traditional perspective, things are very different. Each shader pass analyses each pixel at least once, which means adding complexity ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com \mathcal{O}\left(n^2\right)](../../assets/da2579143fa8427e.png)


#### Coming Next…

The next post will focus on the implementation details of this algorithm. We will see how to recreate it in Unity, using a vertex and fragment shader.

You can read the full series here:

- Part 1.
**GPU Sorting** - Part 2.
**GPU Sorting**

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets necessary to reproduce a GPU sorting shader. There are two downloads available:

## Leave a Reply Cancel reply