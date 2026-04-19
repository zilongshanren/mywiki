---
title: Polar Coordinates
url: https://www.cyanilux.com/tutorials/polar-coordinates/
author: Cyanilux
published: '2019-05-13'
source_blog: Cyanilux Shader Tutorials
source_site: https://www.cyanilux.com/
category: graphics
fetched: '2026-04-19'
---

# Polar Coordinates

When using UVs you are typically using the **Cartesian coordinate system**. Values along the X or U axis start at 0 and increase to 1 horizontally, and the same goes for the Y or V axis but vertically. But in some cases it can be useful to convert this to a **Polar coordinate system**, which can be done by using the **Polar Coordinates** node.

In the [Polar Coordinates system](https://en.wikipedia.org/wiki/Polar_coordinate_system) each point is defined by a **distance from a reference point**, and an **angle from a reference direction**. In Shader Graph this reference point is the **Center** input on the node, and the reference direction is always downwards, which can been seen on the preview of the node where the green gradient stops.

If you are interested in the maths used to convert between these spaces, this is the generated code for the node:

|
|

If we put the output of the **Polar Coordinates** node into a **Split** node, the **R** output will give us the **distance** from the **Center**.

-
The

**Preview**node shows this as the center point is black (0), and as points get further away it increases showing red. -
I’ve drawn circles to represent the values of 0.5 and 1 (assumes a

**Radial Scale**of**1**)

The **G** output will give us the **angle** from the downwards direction.

-
Unlike in regular polar coordinates, this isn’t measured in degrees or radians. Assuming a

**Length Scale**of**1**it ranges from**-0.5 to 0.5**, increasing clockwise which can be seen via the green part of the preview. -
Note that previews won’t display negative numbers any differently from 0, hence why the left half is all black, but they are there! You could use an

**Absolute**or**Negate**node temporarily to help visualise them.

## Examples

### Sampling Textures

One thing that we can do with these new coordinates is use them as new **UVs** to sample textures. Here I’m using a **Sample Texture 2D** node to sample a noise texture. Rather than it being flat (like in the other node) it’s become warped around the center point.

Note that the texture used here is **seamless** so it repeats without any noticeable seams. If you still see a seam you can turn off Mip Maps for the texture, or use the **Sample Texture 2D LOD** node set to 0 instead.

This setup is great for portal/wormhole/whirlpool effects. We can also animate it by using a **Time** node and offsetting the values using **Add** (or **Subtract**).

Polar Coordinates are also useful for creating procedural patterns/shapes, such as :

### Sprial

### Lines

### Star

### Flower

### Cog

### Other

The **Polar Coordinates** node is also used in the following breakdowns :

## Thanks for reading! 😊

If you find this post helpful, please consider sharing it with others / on socials

Donations are also **greatly** appreciated! 🙏✨

(Keeps this site free from ads and allows me to focus more on tutorials)