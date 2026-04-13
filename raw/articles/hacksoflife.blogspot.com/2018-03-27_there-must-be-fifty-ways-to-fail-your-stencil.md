---
title: There Must Be Fifty Ways to Fail Your Stencil
url: http://hacksoflife.blogspot.com/2018/03/there-must-be-fifty-ways-to-fail-your.html
author: Benjamin Supnik
published: '2018-03-27'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

When we first put deferred rendering into X-Plane 10.0, complete with lots of spot lights in-scene, I coded up stencil volumes for the lights in an attempt to save some shading power. The basic algorithm is:




Typically the stencil modes are inc/dec with wrapping so that we aren't dependent on our volume fragments going out in any particular order - it all nets out.


We ended up


I made a note at the time that we could partition our lights and only stencil the ones in the first 200m from the camera - this would get all the fill heavy lights without drawing a ton of geometry.


I came back to this technique the other day, but something had changed: we'd ended up using a pile of our stencil bits for various random purposes, leaving very little behind for stencil volumes. We were down to 3 bits for our counter, and this was the result.



That big black void in between the lights in the center of the screen is where the number of overlapping non-occluded lights hitting a light-able surface hit


I looked at whether there was something we could do in a single pass. Our default mode is to light with the back of our light volume, untested; the far clip plane is, well, far away, so we get good screen coverage.


I tried lighting with the front of the light volume, depth tested, so that cases where the light was occluded by intervening geometry would optimize out. I used GL_ARB_depth_clamp to ensure that the front of my light volume would be drawn even if it hit the front clip plane.


It did not work! The problem is: since our view is a frustum, the side planes of the view volume cross at the camera location; thus if we are inside our light volume, the part behind us will be culled out despite depth clamp. This wasn't a problem for stencil volumes because they do the actual drawing off the back of the volume, and the front is just for optimization.

- Do a stencil pre-pass on all light volumes where:
- The back of the volume failing increments. This happens when geometry is in front of the back of the light volume - this geometry
*might*be lit! - The front of the volume failing decrements. This happens when geometry is in front of the front light volume and thus occludes (in screen space) anything that could have been lit.
- Do a second pass with stencil testing for > 0. Only pixels with a positive count had geometry that were in between the two halves of the bounding volume, and thus light candidates.

Typically the stencil modes are inc/dec with wrapping so that we aren't dependent on our volume fragments going out in any particular order - it all nets out.

We ended up

*not*shipping this for 10.0 because it turned out the cure was worse than the disease - hitting the light geometry a second time hurt fps more than the fill savings for a product that was already outputting just silly amounts of geometry.I made a note at the time that we could partition our lights and only stencil the ones in the first 200m from the camera - this would get all the fill heavy lights without drawing a ton of geometry.

I came back to this technique the other day, but something had changed: we'd ended up using a pile of our stencil bits for various random purposes, leaving very little behind for stencil volumes. We were down to 3 bits for our counter, and this was the result.

That big black void in between the lights in the center of the screen is where the number of overlapping non-occluded lights hitting a light-able surface hit

*exactly*the wrap-around point in our stencil buffer - we got eight increments, wrapped to zero and the lights were stencil-tested out. The obvious way to cope with this is to use more than 3 stencil bits. :-)I looked at whether there was something we could do in a single pass. Our default mode is to light with the back of our light volume, untested; the far clip plane is, well, far away, so we get good screen coverage.

I tried lighting with the front of the light volume, depth tested, so that cases where the light was occluded by intervening geometry would optimize out. I used GL_ARB_depth_clamp to ensure that the front of my light volume would be drawn even if it hit the front clip plane.

It did not work! The problem is: since our view is a frustum, the side planes of the view volume cross at the camera location; thus if we are inside our light volume, the part behind us will be culled out despite depth clamp. This wasn't a problem for stencil volumes because they do the actual drawing off the back of the volume, and the front is just for optimization.

## No comments:

## Post a Comment