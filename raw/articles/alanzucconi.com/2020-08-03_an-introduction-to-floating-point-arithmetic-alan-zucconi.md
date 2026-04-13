---
title: An Introduction to Floating-Point Arithmetic - Alan Zucconi
url: https://www.alanzucconi.com/2020/08/03/floating-point-arithmetic/
author: Alan Zucconi
published: '2020-08-03'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will introduce you to floating-point arithmetic, and how many modern languages—C# included—represent real numbers. This is a series in two parts:

At the end of this article, you will find a link to download a simple C# library that provides a new type which improves the precision of traditional `float`

and `double`

variables.

For the ones of you who have been following my work for some time, you might have noticed the recurrent ~~obsession~~ theme for astronomy. From [tools to visualize exoplanets](https://alanzucconi.itch.io/exoplanetsviewer), to [games about orbital mechanics](https://store.steampowered.com/app/278440/0RBITALIS/). All of these, share something in common: gravity. Simulating gravity is exceptionally easy with a modern computer. Simulating it well, however, is exceptionally complicated.

Part of this challenge comes from the fact that the equations that govern gravity are, for better or worse, chaotic. This means that very small deviations in the present can cause massive changes in the future. A significant part of this often comes from the measurements, which are necessarily imprecise and come with their own uncertainty. However, a more insidious source of error comes from Maths itself. Or at least, it comes from how mathematical operations are implemented in modern computers.

## Floating-Point Representation

Numbers are easy to imagine, but hard to store. Each number has the potential to be unbounded in *both* directions, either being impossibly large, or impossibly small. And so, storing them in memory is a challenge that has to find a compromise between memory allocation and computational speed. When it comes to **real numbers**, the standard technique used to store them in memory uses what is known as **floating-point representation**.

To understand how floating-point numbers are represented in memory, let’s start with a simple example. Imagine you have a real number to write on the field of a paper form. What is the lastest—and the smallest—number that you put in that field? If we include the constraint that one of the boxes in the field needs to be reserved to the decimal separator, then you might answer like this:

![](../../assets/dbd21bded2f159b6.png)

The floating-point representation of real numbers works in a similar way. On top of storing the number, it also stores where the separator—the point—is. And exactly because the point can “float”, it is called floating-point.

Most programming languages offer floating-point representation for real numbers. C#, for instance, supports three different types of floating-point numbers `float`

s, `double`

s and `decimal`

s.

C# type | Approximate range | Precision | Size | .NET type |
`float` | ![]() ![]() | ~6-9 digits | 4 bytes | `System.Single` |
`double` | ![]() ![]() | ~15-17 digits | 8 bytes | `System.Double` |
`decimal` | ![]() ![]() | 28-29 digits | 16 bytes | `System.Decimal` |

[Floating-point numeric types](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/floating-point-numeric-types).

## A Problematic Representation…

Now, there is an obvious issue here. This technique works well with very large numbers and with very small numbers. But it does not work so well with large numbers that also have a lot of decimals. Moving the point to the left increases the precision, but also reduces the maximum number that can be stored. And the same is true for the opposite.

There is another, possibly more insidious problem with floating-point: arithmetic operations. What happens if we try to sum up both the numbers seen above? Since there are no decimals left, the second one is simply discarded; we added two numbers, but effectively nothing has changed.

This is more than a hypothetical issue. In the context of game development, the further a model is from the world origin (0,0,0), the more distorted it will appear. This is because the floating-point representation is using most of its bits to store the position, leaving little space for the fine details. The animation below shows how dramatic this effect can be when a model moves further and further away.

![](../../assets/1f1d01720f0878e0.gif)

A common solution—one that is actually adopted by many games—is to simply translate everything “back” to (0,0,0) when the player has ventured too far from the world.

Some game engines also come with their own mechanism to mitigate the impact that floating-point precision has on rendering distant objects. Unity, for instance, offers a feature called [Camera-relative rendering](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@7.1/manual/Camera-Relative-Rendering.html) available in its latest rendering pipeline (HDRP). It works by bringing the camera (and everything else) to (0,0,0) before rendering. This takes place during the rendering stage of the scene, so it has no impact on the actual position of the objects.

However, such a solution—resetting the position to (0,0,0)—cannot always be used. When working with high-precision simulations—such as gravitational ones—this is a big problem. Space is impossibly vast, and the speeds of our rockets and probes are rather small in comparison. Over time, these small errors add up, leading to a constant drift from the expected outcome. What are supposed to be stable orbits, for instance, could quickly spiral out of control.

For many applications, the problem of floating-point errors can be attenuated by cleverly re-arranging the order in which certain operations are performed. Since the main culprit is adding large numbers with small ones together, a common technique is to add elements “in order”. Adding up the smaller numbers first allows keeping as much precision as possible. Many different techniques have also been proposed to this problem, such as the [pairwise summation](https://en.wikipedia.org/wiki/Pairwise_summation) or the [compensated summation](https://en.wikipedia.org/wiki/Kahan_summation_algorithm) (also known as the “Kahan summation algorithm”).

## What’s Next and Download

This post introduced the concept of floating-point arithmetic, and why it often leads to inaccurate results. The second part of this series will show how to partially overcome these limitations with the `Quad`

library.

You can download the C# `Quad`

library on [Patreon](https://www.patreon.com/posts/39965604). It is available fully compatible with Unity.

## Leave a Reply Cancel reply