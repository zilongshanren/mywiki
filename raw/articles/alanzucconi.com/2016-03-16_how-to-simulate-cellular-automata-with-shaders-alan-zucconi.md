---
title: How to Simulate Cellular Automata with Shaders - Alan Zucconi
url: https://www.alanzucconi.com/2016/03/16/cellular-automata-with-shaders/
author: Alan Zucconi
published: '2016-03-16'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post will show how to simulate cellular automata using shaders. The popular cellular automaton developed by John Conway, Game of Life, will be used as an example for this tutorial. To learn how to set up your project, check out the first two parts of this tutorial: [How to Use Shaders For Simulations](https://www.alanzucconi.com/2016/03/02/4539/) and [How to Simulate Smoke with Shaders](https://www.alanzucconi.com/2016/03/09/simulate-smoke-with-shaders/).

![life](../../assets/995cda4463ab703a.gif)

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[Conway’s Game of Life](https://www.alanzucconi.com#part1) - Part 2.
[Implementation](https://www.alanzucconi.com#part2) - Part 3.
[Optimisation](https://www.alanzucconi.com#part3) - Part 4.
[Improvements](https://www.alanzucconi.com#part4) [Conclusion & Downloads](https://www.alanzucconi.com#conclusion)

If you have seen the tutorial on [How to Simulate Smoke with Shaders](https://www.alanzucconi.com/2016/03/09/simulate-smoke-with-shaders/), you are probably familiar with the limitations that using shaders introduce in the context of simulations. The first of most obvious is the fact that you cannot alter any other pixel but the one you’re currently iterating onto. Working with shaders is a little bit like having a for loop that allows you to only edit the current item. This forces to write all the equations of our simulation in an explicit form, which might not always be feasible or effective.

![texture5](../../assets/78228051d606a65d.gif)

If we want to use shaders for simulation, it is imperative to find a problem that lend itself perfectly to these limitations. Luckily enough, there is a very interesting class of problems that fit this definition. The term *cellular automaton* refers to a specific class of simulations which are loosely inspired by biological processes. Cellular automata are grid-based techniques which can be described very well with textures. The concept behind them is that the state of each pixel (or *cell*) only depends on the state of the neighbour pixels. Something similar happens to cell and bacteria, which change their behaviours according to their surrounding, which they cannot usually alter.

The most famous cellular automaton is [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), developed by John Conway in 1970. It is based on a grid, with each cell either “dead” or “alive”. Time flows at discrete intervals, according to these simple rules:

**Under population.**Any live cell with fewer than two live neighbours dies.**Over population.**Any live cell with more than three live neighbours dies.**Reproduction.**Any dead cell with exactly three live neighbours becomes a live cell.**Sustainability.**Any live cell with two or three live neighbours lives on to the next generation.

These four simple rules were designed to simulate a living colony, introducing intuitive concept of over and under population. Game of Life fails to reproduce the behaviours of a living colony; however, it has incredibly complex properties. First of all, it has been proved to be Turing-complete. This means that they can run any program or algorithm of your choice, if properly encoded in its grid. Game of life is so powerful that yes, you can simulate Game of Life within Game of Life.

If we want to replicate Game of Life in a shader, we first need a way to create a grid-like representation on a texture. This has been discussed already in the second part of this series, [How to Simulate Smoke with Shaders](https://www.alanzucconi.com/2016/03/09/simulate-smoke-with-shaders/). That technique is applied within a fragment shader to sample the state of the neighbour cells, encoded in the red channel.

// Cell centre fixed2 uv = round(i.uv * _Pixels) / _Pixels; half s = 1 / _Pixels; float tl = tex2D(_MainTex, uv + fixed2(-s, -s)).r; // Top Left float cl = tex2D(_MainTex, uv + fixed2(-s, 0)).r; // Centre Left float bl = tex2D(_MainTex, uv + fixed2(-s, +s)).r; // Bottom Left float tc = tex2D(_MainTex, uv + fixed2(-0, -s)).r; // Top Centre float cc = tex2D(_MainTex, uv + fixed2(0, 0)).r; // Centre Centre float bc = tex2D(_MainTex, uv + fixed2(0, +s)).r; // Bottom Centre float tr = tex2D(_MainTex, uv + fixed2(+s, -s)).r; // Top Right float cr = tex2D(_MainTex, uv + fixed2(+s, 0)).r; // Centre Right float br = tex2D(_MainTex, uv + fixed2(+s, +s)).r; // Bottom Right

The second part is the actual implementations of the four rules:

int count = tl + cl + bl + tc + bc + tr + cr + br; // Death if (count < 2 || count > 3) return float4(0, 0, 0, 1); // Life if (count == 3) return float4(1, 1, 1, 1); // Stay return cc;

White and black are used to indicate live and dead cells, respectively.

The Game of Life is often implemented on a toroidal grid. What this means is that the both the left-right and the top-down sides are connected. If you want this to be the case, make sure the render texture you are using is imported with **Wrap Mode** set to **Repeat**. Conceptually, the geometry of the world can be represented as a single, continuous 3D object like in the following video:

To avoid any issue, is also important that **Filter Mode** is set to **Point**.

### ⭐ Recommended Unity Assets

The technique described in the previous paragraph has two main disadvantages. The first one is that changing the rule requires to actually change the code of the shader. The second is that if statements are notoriously slow when used within a shader. In this particular case, it is possible to use an alternative way to express the rule. Since each cell can have any number of living neighbours ranging from zero to eight, we can use an array of nine items to indicate the next state:

static int2 rule[9] = { int2(0,0), int2(0,0), int2(1,0), // 2 neighours = survive int2(0,1), // 3 neighours = born int2(0,0), int2(0,0), int2(0,0), int2(0,0), int2(0,0), };

Each item has two components. The first one indicates if the current cell survives to the next stage or not. The second whether a new cell should be created. The rules can now be expressed as:

int2 r = rule[count]; int status = cc * r.x + r.y; return float4(status, status, status, 1);

It is important to notice that in order for the `rule`

array to keep its value, the keyword `static`

is necessary.

One interesting graphical improvements can be achieved by changing the colours of the cells depending on how long they have been living for. This is possible because we are only using the red channel of our texture for the calculations. The other channels can filled with other colours. In the example shown at the beginning of this tutorial, cells are getting progressively more red the longer they have lived.

float3 cc = tex2D(_MainTex, uv + fixed2(0, 0)); if (cc.r == 1 && status == 1) return float4(status, ccc.g*0.9, ccc.b*0.9, 1); else return float4(status, status, status, 1);

Cellular automaton are incredible tools, which have many real applications in game development. [Sebastian Lague](https://twitter.com/SebastianLague) is using a similar technique to procedurally generate cave-like structure.

**Cellular automata can simulate many natural behaviours, including the way water flows. This will be covered in the next part of this series.**

You can download the full Unity project of this tutorial [here](https://www.patreon.com/posts/13678769/).

#### Other resources

- Part 1.
[How to Use Shaders for Simulations](https://www.alanzucconi.com/2016/03/02/4539/) - Part 2.
[How to Simulate Smoke with Shaders](https://www.alanzucconi.com/2016/03/09/simulate-smoke-with-shaders/) - Part 3.
**How to Simulate Cellular Automata with Shaders**

## Leave a Reply Cancel reply