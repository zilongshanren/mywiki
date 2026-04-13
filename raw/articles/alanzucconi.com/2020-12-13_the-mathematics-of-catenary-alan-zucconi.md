---
title: The Mathematics of Catenary - Alan Zucconi
url: https://www.alanzucconi.com/2020/12/13/catenary-1/
author: Alan Zucconi
published: '2020-12-13'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Many modern games feature hanging wires, cables and chains; this series of tutorials will explore the mathematics behind their shape, which is known as **catenary**.

- Part 1.
**The Mathematics of Catenary** - Part 2.
[Implementing Catenaries for Games](https://www.alanzucconi.com/?p=12724)

You can find the Unity package to create catenaries in Unity at the end of the post.

## An Introduction to Catenaries

Out of the many mathematical objects that have been studied and described, there is one that is very dear to many game developers. And yet, only a small number of them actually know its name: **catenary**.

A catenary is the shape that a rope or chain will naturally converge to, when suspended at its ends. It is not a coincidence that the name *catenary* itself comes from the Latin *catenaria*—which indeed means *chain*.

Modern games feature an increasing number of run down facilities and destroyed environments. And most comes with their fair share of hanging wires. Such as the ones seen in GLaDOS’ room in “Portal”, or “Half-Life: Alyx”, just to name a couple.

![](../../assets/03040018338b9f94.jpg)

Because catenaries occurs everywhere around us, we have grown accustomed to their shape. This also means that it is very easy to spot when something is not hanging the *right* way. Like skin-complexion and cloth-physics, a wrong catenaries are hanging over an uncanny valley of their own.

![](../../assets/b7ac6bbfff8fb749.jpg)

And yet, so many games are getting catenaries wrong! The reason, however, is not surprising. While they are so easy to generate in the real world, their mathematical definition is made of the same substance of nightmares. Exception made for a few special cases, there is no “easy” equation to generate a catenary; at least not in the form that we need to properly decorate a level.

One common ways of creating physically-based catenaries “for free” is to use *rigid bodies* and *hinge joints* to create chains and ropes. This has the extra benefit of making them reactive to the player’s interaction, but at the cost of being computationally expensive. Most hanging wires and cables are part of the background, and using physics to create them would be too expensive. Consequently, being able to place static catenaries with no run-time cost is pretty critical.

On top of that, drawing catenaries comes with an additional benefit. Let’s imagine that you want to create an actual, physically-driven hanging wire for your game. How do you place the wire segments, when instantiating them? Many developers would simply place them along a line, letting the physics engine do the work for them by finding an equilibrium state. Drawing catenaries allows you to initialise physically-driven wires and cables in their equilibrium state, without having to wait for them to settle into position by themselves.

It is worth noticing that while Unity does not offer any build-in tools for cables and chains, Unreal Engine comes with a [Cable Component](https://docs.unrealengine.com/en-US/Basics/Components/Rendering/CableComponent/index.html) that solves exactly this problem through a technique called **Verlet Integration** (which, incidentally, will be the topic of a future series). And in case you are into shaders, Ross Beardsall recently came up with an [ingenious solution](https://medium.com/xrlo-extended-reality-lowdown/how-to-create-a-coiled-cable-shader-in-ue4-8bb47777d8ab) to simulate coiled cables in Unreal Engine 4…

## A Formal Definition

If we want to get physically-accurate catenaries, perhaps is best to start from the beginning. The simplest catenary one can image has a well-defined equation, which almost entirely relies on ![Rendered by QuickLaTeX.com \cosh](../../assets/8e9cdbfef75bb878.png)

[hyperbolic cosine](https://en.wikipedia.org/wiki/Hyperbolic_functions#Hyperbolic_cosine):

(1) ![Rendered by QuickLaTeX.com \begin{equation*} y=a \cosh{\left(\frac{x}{a}\right)}\end{equation*}](../../assets/c73e225abd238760.png)


The catenary equation has a parameter, ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


## Parametrising the catenary

If we want to draw physically sound catenaries, ([1](https://www.alanzucconi.com#id3707536389)) might not be the best way to do it. The reason is simple: asides from ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


A more “customisable” equation is ([2](https://www.alanzucconi.com#id436391346)), which allows to move the curve horizontally and vertically using two additional parameters, ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com q](../../assets/b43061656d5cc7df.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} y=a \cosh{\left(\frac{x-p}{a}\right)}+q\end{equation*}](../../assets/f0da25c4d5a12106.png)


Ideally, however, we would like the equation of a catenary that passes by two anchored points, ![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com P_2](../../assets/2e2bcf5cc12d64bd.png)


![Rendered by QuickLaTeX.com \[\begin{split}P_1 & = \left(x_1, y_1\right) \\P_2 & = \left(x_2, y_2\right)\end{split}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-66abb236be2be9bfd86143e3bc29e3fb_l3.png)


The parameter ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com p=0](../../assets/ff3e2f598f0cd44f.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com P_2](../../assets/2e2bcf5cc12d64bd.png)


![Rendered by QuickLaTeX.com \[p=\frac{x_1+x_2}{2}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-4f832bb46ce1970b6560303d85d7f0d8_l3.png)


This is actually perfect if both ![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com P_2](../../assets/2e2bcf5cc12d64bd.png)

![Rendered by QuickLaTeX.com y_1=y_2](../../assets/7767296885014a4b.png)


## Solving the catenary problem

The following section will show the equations of a physically correct catenary that represents a rope anchored at two points in space, ![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com P_2](../../assets/2e2bcf5cc12d64bd.png)

![Rendered by QuickLaTeX.com l](../../assets/dacf99a2de8dda2c.png)


First, let’s define two auxiliary parameters, ![Rendered by QuickLaTeX.com h](../../assets/5b0f1268bf785a2d.png)

![Rendered by QuickLaTeX.com v](../../assets/1bf6fd37becd9c3d.png)


(3) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{split}h & = x_2 - x_1 \\v & = y_2 - y_1 \\\end{split}\end{equation*}](../../assets/6fd311af041e82d0.png)


For this derivation, we are assuming that ![Rendered by QuickLaTeX.com y_1 < y_2](../../assets/10eee34a5f217d19.png)

![Rendered by QuickLaTeX.com l](../../assets/dacf99a2de8dda2c.png)


The resulting values for ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com q](../../assets/b43061656d5cc7df.png)


(4) ![Rendered by QuickLaTeX.com \begin{equation*} p=\frac{x_1+x_2-a \ln{\left(\frac{l+v}{l-v}\right)}}{2}\end{equation*}](../../assets/627fa39a1f3028b9.png)


(5) ![Rendered by QuickLaTeX.com \begin{equation*} q=\frac{y_1+y_2-l \coth{\left(\frac{h}{2a}\right)} }{2}\end{equation*}](../../assets/9f587eff547ea67d.png)


where ![Rendered by QuickLaTeX.com \coth](../../assets/73db028215d53cc0.png)


![Rendered by QuickLaTeX.com \begin{equation*}\coth{x}=\frac{\cosh{x}}{\sinh{x}}\end{equation}](../../assets/dd7477641df4f886.png)


With the interactive chart below you can move the second anchor point around (![Rendered by QuickLaTeX.com P_2](../../assets/2e2bcf5cc12d64bd.png)

![Rendered by QuickLaTeX.com l](../../assets/dacf99a2de8dda2c.png)


## Finding *a*

The section above failed to provide an equation for the first parameter of the catenary: ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

[transcendental equation](https://en.wikipedia.org/wiki/Transcendental_equation):

(6) ![Rendered by QuickLaTeX.com \begin{equation*} \sqrt{l^2-v^2}=2 a \sinh{\left(\frac{h}{2 a}\right)}\end{equation*}](../../assets/6cdfe67803246dc3.png)


To put it simply, this means that we cannot rearrange this equation in a simple form such as ![Rendered by QuickLaTeX.com a=...](../../assets/bf19469d6b3b75c6.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


When this happens, it means that we need to a different approach to calculate the value of ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

*analytical *tools fails, we resort to *numerical *ones. Which means that we need to use an algorithm to find an approximated solution.

The next post in the series will explore how we can do that.

### 📚 Recommended Books

## What’s Next…

This first post introduced **catenaries**, the mathematical objects used to model hanging chains. The next one in the series will explore how to implement them in a game engine such as Unity.

- Part 1.
**The Mathematics of Catenary** - Part 2.
[Implementing Catenaries for Games](https://www.alanzucconi.com/?p=12724)

### Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

There are two different Unity packages available for this tutorial. They contain a simple library to draw efficiently catenaries, which you can use in your games. Both packages are available through Patreon.

The [Standard package](https://www.patreon.com/posts/44985024) one contains the scripts to draw catenaries in 3D and 3D, along with a test scene. The [Advanced package](https://www.patreon.com/posts/45357589/) contains support for rigged models (such as corded cables or chains), along with some advanced code to sample catenaries uniformly.

## Leave a Reply Cancel reply