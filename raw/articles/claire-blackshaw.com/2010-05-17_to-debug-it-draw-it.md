---
title: To Debug it… Draw it
url: https://claire-blackshaw.com/blog/2010/05/to-debug-it-draw-it/
author: Claire Blackshaw
published: '2010-05-17'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![To Debug it… Draw it](../../assets/4e402aebc4c1a4e8.png)

## To Debug it… Draw it

Many people will tell you this but whenever you have a problem try to visualise it. This can be applied to almost everything (except cases where visualisation is a constraint, think advanced maths and quantum). So above you see the debug frustum.

Well after fighting with all these various problems I’m thinking to myself… I need to double check my Frustrum. Five minutes to write and **BAM** problem is instantly visible. The problem I was debugging for 5 hours solved in 5 minutes.

Printf & Debug Draw rocks.

### Problem: Shadows giving strange LightViewSpace results

Well the problem manifested in many ways. I was debugging shaders and tweaking render targets. Not to mention twiddling the depth bias so often that it was indecent.

The problem was two fold. Firstly the sun view & position didn’t match up. The result of a quick hack to get the sun in the right place, hacks bad. The second issue was todo with the scene bounds.

The view matrix is built with a look-at call. Well the key is that the centre of the bounds must be equal to the look-at target. Why is this? Well draw some random shapes on an A4 page. Now draw a circle which contains all those objects. Now measure the radius of the circle and draw a square at the centre of the page with double that length per side.

You see the problem, unless the circle is at the centre of the page their will be bits of it outside of the box, which means they won’t be shadowed.

So you compensate for offset and increase the radius. To do this instead of measuring the radius of the circle measure the distance from the centre of the page to the furthest point of the circle.

Before you ask we can’t move the box from the centre of the page as that would change the angle the light was coming from.

Onwards and upwards.