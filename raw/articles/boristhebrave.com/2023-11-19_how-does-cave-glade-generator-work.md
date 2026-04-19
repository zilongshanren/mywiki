---
title: How does Cave/Glade Generator Work
url: https://www.boristhebrave.com/2023/11/19/how-does-cave-glade-generator-work/
author: Boris
published: '2023-11-19'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

[Watabou’s Cave Generator](https://watabou.itch.io/cave-generator) is one in a series of RPG-ready map generators that Watabou has created over the years. [All his work](https://watabou.itch.io/) oozes style, but the cave generator was always the one I found most mysterious.

I discovered that the entire thing was exported with extremely readable javascript, so naturally I started to poke and prod. Let’s go over how it works.

Table of Contents

We’ll focus on how this map is generated for version 2.0.2:

![](../../assets/82a7c9ab54685403.png)

The main thing to initialize are tags. These are randomly picked, but can also be set by the user.

![](../../assets/4102acc0d54e8169.png)

Tags control the later generation steps. Sometimes they switch between different algorithms, but more commonly they act as presets for numeric parameters. I’ll refer to tags `like this` when they are referenced. Some tags are mutually exclusive – e.g. only one of `small` / `medium` / `large` can be chosen.

Some other global parameters are randomly chosen at the start, such as chamber size and connectedness preference for area growth. This gives each dungeon a more consistent feel across the map.

Like all procedural generators, there is a seed parameter that controls all sources of randomness. This enables permalinks for maps by storing the seed.

It’s not obvious, but in fact everything in the generator is done on a hex grid. Let’s see the final output again, this time with all the graphical details turned off – no wobbly lines, no random rocks, no water, no superimposed square gridlines.

![](../../assets/0d3795f9f6a47ec7.png)

Now you can see the actual specifics of the map. But how is the layout actually achieved?

After creating the hex grid, it is immediately converted into a data structure called a [Doubly connected edge list](https://en.wikipedia.org/wiki/Doubly_connected_edge_list), which is essentially a fancy way of representing a mesh of polygons and their neighbours. Everything in the generator operates on this mesh data structure – it’s not tied to hexes at all. I was able to hack in square grids without much difficulty, the author just didn’t find a use for this feature.

![](../../assets/dc098519cf88cf5b.png)

The majority of the map is generated with an algorithm called seed growth 1. It picks a random starting location and then adds adjacent cells at random until a predetermined size has been met. This is then repeated to give several areas. Areas are not permitted to touch each other.

![](../../assets/4c15968957f6e465.png)

Most of the details of the generation are determined by tags:

The number of areas is 9-19 for a `large` map, 3-8 for a `medium` and 2-3 for a `small`. If no tags are present has a 1 in 20 chance of picking 2 or 20, otherwise it uses a random formula.

The size of each area is also a random function. For `hub` generations, there is one area of size 60-79, and other areas of size 8-13. For `chamber`, a random chamber size is chosen between 11-14, and then each area is randomly offset from that by 0-2. And for `burrow`, it uses formula `10 + 80 * pow((rand() + rand() + rand()) / 3, 3)`

which gives rooms around size 23, but occasionally much larger.

When choosing which cell to add to the area, they are weighted differently according to various algorithms. By default, it weights each cell as `pow(c, gamma)`

where c is the number of adjacent cells already in the area, and gamma is a random variable indicating the preference for connection. High gamma tends to cause rounder areas with fewer jutting pieces. `cavities` fixes the gamma of 6, while `coral` uses a negative gamma so each area prefers narrow tendrils. `chaotic` prefers cells with 2 connections.

![](../../assets/8349d6aa2f052f89.png)

`coral`is probably the most distinctive style.

Now its time to connect up all the areas. First, the algorithm identifies all cells that border two elements.

![](../../assets/1c59a2a186c70b0f.png)

The possible area-pairs are then culled. For `tree`, a simple [depth first search](https://en.wikipedia.org/wiki/Depth-first_search) ensures each area is only reachable a single way (no loops). For `connected`, if it finds 3 areas all adjacent, it disconnects one pair. Otherwise, all pairs are kept.

![](../../assets/9b0c6346ec8587f0.png)

For each pair, a single door cell is randomly chosen from amongst the possibilities and added to the map.

![](../../assets/816596d7e71f937f.png)

Some areas are randomly chosen to shrink to corridors. It prefers areas with a large number of doors for the area, and some tags, particularly `burrows`, greatly increase the chances.

To shrink an area, points are repeatedly removed, and flood-fill is used to ensure that the doors are all still connected, which I describe more in [Chiseled Paths Revisited](https://www.boristhebrave.com/2022/03/20/chiseled-paths-revisited/).

![](../../assets/0d3795f9f6a47ec7.png)

At this point, exits are chosen too, which are randomly selected from eligible border cells. Cells further from the center get higher weights. The exact number of exits can be controlled with tags `sealed`, `entrance`, `passage`, `junction`.

The water is simply an independent [Perlin noise](https://en.wikipedia.org/wiki/Perlin_noise), which is compared against a threshold. It’s more obvious in v2.1.0, where you can play with a slider.

![](../../assets/7ed8977effec645b.gif)

The hexagonal nature of the walls is hidden via several steps:

- Every edge is subdivided
- The outline is smoothed (“bumpiness”)
- Vertices in corridors are moved towards the face center.
- The points are randomly offset (“irregularity”)
- Two more iterations of subdivision and randomness (“roughness”)
- The boundary is converted to curves with
[Chaikin’s Algorithm](https://observablehq.com/@pamacha/chaikins-algorithm)(not shown in gif)

![](../../assets/64f4e83a56203ed5.gif)

Some random small polygons are dropped on the map to make stones and rubble. [Dyson hatching](https://www.patreon.com/posts/hatching-in-1pdg-31716880) is applied near the boundary.

The title of each map is generated using a [Tracery](https://tracery.io/) script. Many features contribute to the choices – “demonic” names are more likely for certain tags, and the presence of water increases the chance of damp names like “Bog”.

The top-level rule gives you an idea of what it’s like:

```
"name" : [
"#compound_noun# #noun#",
"#adj# #noun#",
"0.2?-#noun# of #fantasy#",
"!LARGE&0.2?-#person#'s #noun#",
"!SMALL&0.1?-#noun# of #epic_noun#"],
```


Glade mode re-purposes the entire generator for making forest clearings. The main differences are the trees randomly drawn along the border, and the name generator switches to a different script. I love how you can switch it on and see the same map completely re-interpreted.

![](../../assets/37988aaf57ad633c.png)

Oleg’s generator illustrates a common maxim in procedural generation. Great results don’t come from applying a super advanced algorithm, but rather by combining several simple rules effectively, and with an eye to the look and style you are aiming for.

In my opinion, Some of the rules used here, notably seed growth, and path chiseling offer a nice balance of simplicity to useful results and are generally underappreciated as techniques.

- We’ve seen “seed growth” before in my
[Binding of Isaac](https://www.boristhebrave.com/2020/09/12/dungeon-generation-in-binding-of-isaac/)article. But there’s no widely known name for this technique that I’m aware of.[↩︎](https://www.boristhebrave.com#8b84f512-06eb-431d-9cd4-7fa20b515d17-link)

Interesting writeup! I don’t know of an official term for “seed growth” either. I’ve been calling it “randomized flood fill”.

Beautiful article! I had seen his work a lot on twitter and always wondered about the techniques used. Not too complicated in the end!