---
title: Shockwave Shader Graph - Game Dev Bill
url: https://gamedevbill.com/shockwave-shader-graph/
author: Bill
published: '2020-12-08'
source_blog: Game Dev Bill
source_site: https://gamedevbill.com/
category: game programming
fetched: '2026-04-13'
---

![Shockwave shader graph title](../../assets/4600e5012a70eeb7.png)

A shockwave shader graph (or shock wave shader graph) is a relatively simple effect, that can add a lot of pop to actions in your game. Today I’m going to cover both how to do it as a fragment shader effect (for sprites or full-screen) and as a vertex shader effect (for more complex models).

The reason I’m doing this tutorial at all is because someone commented on one of my [YouTube ](https://www.youtube.com/c/GameDevBill)videos requesting it. I bring this up just to mention that if you have anything you’d like to see, please let me know in the comments of one of my videos!

This tutorial has a matching youtube [video here](https://youtu.be/dFDAwT5iozo).

*This article may contain affiliate links, mistakes, or bad puns. Please read the *[disclaimer](https://gamedevbill.com/disclaimer/) for more information.

[disclaimer](https://gamedevbill.com/disclaimer/)for more information.

Assets used in article and video:

## Concepts

A shockwave is just a single ripple of motion, emanating out from a point. Similar to a water ripple, it is intended to portray an energy field, but is simpler than the water case. Where a water ripple will have a negative ring behind the positive (bump, then dip), a shockwave generally just has the one. And a water ripple will generally have a few rings of decreasing strength inside each other.

Here are the two samples we’ll be working towards.

![](../../assets/1e1d7b48b73c1581.gif)

![](../../assets/67713f21ee81339c.gif)

## Sprite Shader Graph

To make a sprite or screen effect look like it’s coming towards you, we scale the texture. In our case, what we’ll do in a ring shape, having it ramp up from a 1x scale, and then back down.

First crate an unlit shader graph. This is unlit because for sprites or full-screen shader graphs we don’t need lighting.

Make a material based on this new shader graph, and assign the material to a sprite. If you wish to use this shader graph on a full screen effect instead, be sure to reference [my tutorial on how to set that up](https://gamedevbill.com/full-screen-shaders-in-unity/).

Add an input called “MainTex” to the shockwave shader graph, and set the Reference to “_MainTex”. Feed this input into a Sample Texuture 2D node, and feed that into the Color of the master node. This will give us a baseline shader that correctly samples the sprite.

![](../../assets/53084adbf442e4d3.png)


![](../../assets/53084adbf442e4d3.png)

### The Ring

I could work on the ring or the scale first, but I feel it’s easier to visualize if we start with the ring logic. To set that up, we need three inputs to the shader:

**FocalPoint**– Vector2 – Default (0.5, 0.5) – this is the point (in normalized space) from which the effect will emanate.**Size**– Vector1 – Default (0.1) – this determines how wide the ring of the effect will be.**Magnitude**– Vector1 – Default (-0.1) – this determines strong the effect is. While in the sprite version, we want this to be negative. In Vertex version, we’ll want it to be positive.**Speed**– Vector1 – Default (1) – this determines how quickly the ring moves

Next create a UV node, and subtract the FocalPoint from that. Then feed that into a Length node. To keep things organized, I’ll put the subtract node into a group by itself called Direction and the Length node into a group by itself called Distance.

Note that this won’t work for all objects. If you’re following along, and things look wrong in-scene, be sure to check out “When UV distance won’t work” below.

![](../../assets/2d93ce7439b6bf81.png)


![](../../assets/2d93ce7439b6bf81.png)

In another area, we’ll set up the actaul movement. For now I’ll base this on Time, but later (in the vertex based example) I’ll show how it could be input based as well.

Create a Time node, and multiply the Time output by Speed input. Then feed that into a Fraction node. Speed input will let us control how quickly time moves for this graph.

![](../../assets/2041e10c6f62ea2c.png)


![](../../assets/2041e10c6f62ea2c.png)

This creates a value that ramps from 0 to 1 repeatedly. Now we need to use that to grab a chunk of area based on distance from FocalPoint. So feed the Time-Fraction output into both an Add and a Subtract node (A input). Feed our Size input into each of the B inputs of those nodes. That’ll make edges at (time + size) and (time – size). Feed those both into the edges of a Smoothstep node (subtract in edge1, add in edge2). For the input of the Smoothstep, grab that Distance value we created earlier.

![](../../assets/c5657168b5f073f2.png)


![](../../assets/c5657168b5f073f2.png)

This Smoothstep output will be 0 before Time-Size, then ramp up to 1, reaching 1 at Time+Size. To turn that into a ramp up, and back down to 0, feed the Smoothstep output into a One Minus node, and multiply the one-minus by the original.

![](../../assets/61558a772c6efc8f.png)


![](../../assets/61558a772c6efc8f.png)

### The Scale

If you remember from my basics [article ](https://gamedevbill.com/shader-series-1-high-level-concepts/)or [video](https://youtu.be/FLVNfBQgeQc), for pixel shaders you don’t “push” a color, you pull it. So to scale up the texture, we pull color outwards, to stretch it.

So how do we know what “outwards” is? Remember that node I put in a group called “Direction”? Feed that into a Normalize node and it’ll give a vector of length 1 pointing away from the FocalPoint.

Multiply that by the Magnitude input we created earlier, and then multiply that by the ring

![](../../assets/4851465cd3e0ae99.png)


![](../../assets/4851465cd3e0ae99.png)

To use that to offset our UVs, create another UV node, feed that into an Add with our ring offset. Feed the output of the Add into the UV input of the texture sample set up at the very beginning.

![](../../assets/0e31029653b58f90.png)


![](../../assets/0e31029653b58f90.png)

![](../../assets/1e1d7b48b73c1581.gif)

### When UV distance doesn’t work

I need to revisit one section of our shockwave shader graph. At the very beginning, I fed (UV – FocalPoint) into a Length node to figure out how far we were from the focal point. This logic assumed that our UVs were 0-1 on both the X and Y in our sprite. For a simple sprite, this is the case. For something more complex, it may not be. In this instance, you have two choices to fix it. One is to know what part of the UVs you’re dealing with. You can do this is you are sampling into some understood sprite sheet.

The more general-purpose solution is to use object position instead. Depending on your shape, you’ll likely need the (X,Y) or (X,Z) coordinates of object position. I go into this a little more in the video version of this tutorial.

![](../../assets/0f7cd2f3f386a66f.png)


![](../../assets/0f7cd2f3f386a66f.png)

### Handle non-squares

So far, my sprite has been square, and the shader graph has taken advantage of that. If you use this shock wave shader graph as a full screen effect, or on a non-square sprite, you’ll run into an issue. The ring won’t be circular.

To fix that, add another input called SizeRatio. In my case I set it to 1.777 which is 16 divided by 9, as I’m running my game at a 16:9 aspect ratio.

Head over to the Distance and Direction groups we crated earlier. Between the subtract and the Length nodes (between Direction and Distance) add a Split and Combine node. Between the Split and Combine, feed the Y value (G) directly through, but multiply the X (R) by our SizeRatio.

![](../../assets/1473870f47237657.png)


![](../../assets/1473870f47237657.png)

## Vertex Shader Graph

When doing a shock wave shader graph on a more complex model, messing with the pixels will probably look weird. I’ve got an example of this in the video above.

Instead, we’ll move the vertices around. With pixels, we moved them outwards to simulate a towrd-camera movement. Since we can actually move in 3 dimensions vertex shaders, we’ll do that instead.

So make a PBR shader graph (meaning a lit shader). In my case, I’ve already set it up to sample the multiple textures needed for the model I’m using.

![](../../assets/e2f2192d2e18c1a2.png)


![](../../assets/e2f2192d2e18c1a2.png)

Since we’re doing things to the vertices, we’ll need to base our logic on object position, not UV coordinates. This was described above. To start, we’ll get all the nodes from the graph so far, including the position based distance.

![](../../assets/4136e1f0bf3b6e5b.png)


![](../../assets/4136e1f0bf3b6e5b.png)

Next, remove the parts of this we don’t need. Specifically this will be the Normalize node inside the Direction block (but keep the multiply it was driving), and the Add and UV at the very end.

I kept the Add & UV nodes in the screenshot below so you can see that what was driving them will drive our new logic.

That new logic will be a Position node (in Object Space) fed into a split and a combine. For my model, I want to keep the X & Z unchanged, but add my ring to the Y. This will depend on your model.

Drive the output of the Combine into the Position input of the master node.

![](../../assets/e64a805a0f6b3b94.png)


![](../../assets/e64a805a0f6b3b94.png)

That’s it for mutating the vertices. I’ve shown it below for my specific case, slowed down a bit so you can clearly see it despite the gif compression.

![](../../assets/67713f21ee81339c.gif)

## References

That’s all there is to the shockwave shader graph. Remember a lot of this is explained in the [video version as well](https://youtu.be/dFDAwT5iozo), in some cases with easier to follow visuals.

Important Links

[Full Screen shaders in URP (with shader graph)](https://gamedevbill.com/full-screen-shaders-in-unity/)[Infinity PBR – Weapons and Armor](https://assetstore.unity.com/packages/3d/props/weapons/weapons-armor-pbr-pack-1-44714?aid=1011l3QFn)[DOTween Pro](https://assetstore.unity.com/packages/tools/visual-scripting/dotween-pro-32416?aid=1011l3QFn)[Gaia2](https://assetstore.unity.com/packages/tools/terrain/gaia-2-terrain-scene-generator-42618?aid=1011l3QFn)- Hosting by
[Bluehost](https://www.bluehost.com/track/gamedevbill/AboutMe)

*Do something. Make progress. Have fun*.