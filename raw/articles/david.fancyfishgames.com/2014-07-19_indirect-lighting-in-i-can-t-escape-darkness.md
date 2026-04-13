---
title: 'Indirect Lighting in I Can''t Escape: Darkness'
url: http://david.fancyfishgames.com/2014/07/indirect-lighting-in-i-cant-escape.html
author: Legend
published: '2014-07-19'
source_blog: The Legend of GameDev
source_site: http://david.fancyfishgames.com/
category: graphics
fetched: '2026-04-13'
---

In I Can't Escape: Darkness (ICED), lighting plays an important role in the gameplay. I had several game-specific requirements I needed to meet, however the resulting algorithm could easily have wider applications. In this post I'll go into some detail about my lighting approach, the steps I took to reach it, and how to implement it.

So here's the problem I faced: I won't explain the game mechanics (no spoilers!), but some areas of the map needed to be pitch black (no ambient light) for the game to work. However, direct lighting alone wouldn't be enough, as that would make the levels

*too*dark (everything not directly lit would be pure black). Additionally, adding ambient light in an area of effect around light sources would lead to the light bleeding through walls (which would break gameplay, lighting areas that should be pitch black).
Obviously, I needed something like global illumination with visibility, but for those of you who have done any graphics research, you'd know that this is an open problem, with lots of research and very few algorithms that would work in this case (without requiring high end graphics card). Lightmapping also doesn't work, as some of the light sources are dynamic (like the flashlight).

Knowing that true global illumination is expensive to render, I decided to use a physically inspired, but not physically accurate approach. For those hoping for an accurate, real time (even on integrated cards) global illumination algorithm, I'm sorry, I'm not a magician. However, this approach is very useful, especially for 2D games or cell based games (like ICED or Minecraft). In fact, while I don't know exactly what Minecraft does, their approach looks visually similar to mine (light does not bleed through blocks, but doesn't appear to correctly bounce off walls).

Final direct+indirect lighting in I Can't Escape: Darkness.

### The Idea

The idea is actually inspired by heat transfer. Instead of bouncing light off walls in a very complicated computation, heat transfer distributes heat along a surface in an embarrassingly parallel way (well suited for graphics cards). From the heating elements (the light sources), heat spreads and attenuates over distance like light, and by varying the conduction along the surface, we can make blockers (walls) that the heat has to travel around instead of through, satisfying my "no bleeding through walls" requirement. Lets look at an image of this in action:

The top left image is the conduction of my map, where white is open space, and black is walls. I also removed a one pixel border around the walls so that the walls could receive indirect light. Gray pixels could be added to have semi-transparent cells (like partially open doors or windows). This is in 2D as I didn't care about light transfer between levels, but in a Minecraft style game, you could easily augment this algorithm as a 3D volume instead of a 2D texture.

After the conduction mask is created, I place the lights as points, shown in the top middle image. Then, by iteratively spreading out the heat using the conduction mask to block heat transfer through walls (I'll show the algorithm for this later), you get the top right image after 5 iterations, the bottom left image after 10 iterations, and the bottom right image after 20 iterations. 20 iterations was enough for my purposes, and given how fast each iteration is and how small the map is, this renders realtime even on integrated graphics cards. The bottom middle image is also 20 iterations, but has a door closed so you can see how light is blocked from the bottom left room when the door is closed, and can enter when the door opens. Note that this image has been brightened so that you can see the transfer more clearly.

If your game is 2D, simply use the resulting texture (bottom right) as the indirect lighting. Blocking cells won't allow light to leak through, and indirect light will spread throughout your scene. In ICE, by indexing this texture using the x/y coordinates of the geometry, I can get the indirect light at any given point. This is why the 1 pixel border around the walls is needed (otherwise, walls would index a blocker pixel and have no indirect lighting. Since the walls have thickness despite the border, they still correctly block light and stop bleeding). The result is as follows:

With both indirect and direct lighting. There are strong shadows from direct lighting, but instead of being pitch black, there is a little indirect light to lighten the scene. This image has been brightened to make it clearer.

With only indirect illumination. The light appears to come out of the gap, and the right wall is very dark despite the torch being towards the right (you can see the torch position from the previous image with direct lighting) . This has also been brightened.

Here is direct lighting only - as you can see, the walls and room outside are pure black, and there is a pure black shadow where the wall's corner blocks the light. The direct lighting includes dust, another lighting element of ICED that is not mentioned in this blog post. This scene has also been brightened.

As for how realistic this approach is, the answer is not very. It doesn't take height into account at all (although you could with a 3D volume texture), and the walls facing the camera are brighter than they should be, as they would only receive minor illumination from the floor and ceiling. However, it is similar to indirect illumination, and it meets all of my criteria (attenuating as it travels away from the light source, and not able to bleed through walls, it has to wrap around them).

Some interesting notes about this algorithm: in 2D, it's about as close of an approximation you can get to indirect lighting without some knowledge of the depth of the scene (as there's no way to know how light would bounce). Also, this can be extended into a pathfinding algorithm: by "hill climbing" (always traveling to the brightest cell), you could cheaply get a horde of units to travel around walls and reach the closest point (within the number of iterations).

### The Implementation

Hopefully you understand the idea at this point and have a vague idea of how it works (and whether you'd want to add it to your game). Obviously, any games with complex geometry that can't be well defined in a 2D or 3D grid for the conduction mask wont work, but for blocky tile-based games, this works very well and even runs realtime on a seven year old computer (with an Nvidia GeForce 9200M GS graphics card, so not top of the line even during it's time)!

The first step is to create the conduction mask. This can be done on the CPU if the scene is relatively static, or by rendering simplified geometry to the texture. In ICED, the conduction mask is four times the size of the levels (so 128x128 for a 32x32 tile level) to allow me to remove a 1 pixel border while still having at least a 2 pixel thickness to the walls.

Next, create two floating point textures of the same size as the conduction mask - the front and back indirect lighting buffers. Render the lights as points to the front buffer (with additive blending enabled in case two points overlap). I actually rendered each light as four points, so that if a light was between cells, it would still add the correct amount of light to nearest four cells. This is the only step that is dependent on the number of lights, so even if your scene has THOUSANDS of lights, rendering thousands of points is no trouble at all (even for old computers), so this algorithm runs quickly almost regardless of how many lights in your scene. Hint: this works well with deferred rendering, as that allows you to add many direct light sources, and all you need to do is render the indirect lighting with additive blending to the direct lighting.

Finally, for each iteration, first swap the front/back buffers. Then render into the front buffer the weighted average of all adjacent pixels. This is similar to a 1 pixel radius gaussian blur, except the pixels have to also be weighted by the conduction mask to determine if light can transfer between the two pixels. Also note that this is NOT a separable kernel, because of the conduction mask. Here is the GLSL shader I wrote that computes each iteration:

[http://pastebin.com/pTGsx4vf](http://pastebin.com/pTGsx4vf)
The shader adds the weighted pixels from the previous pass (and keeps track of the weights), then divides by the sum of the weights. Yes, this could've been done with a double for loop, but I unrolled it by hand (uglier, but faster).

For those who like terminology, this is the laplace operator that computes the heat transfer. When your last iteration is done, the front buffer texture contains the indirect lighting that you can index by position to get the indirect light for that point in your scene! Pretty easy huh? You can also modify the weights to determine how the light spreads (in the above shader, I gave higher weights to points further from the center to get it to spread more with fewer iterations - you wouldn't want to do this if your applications was pathfinding). You can also take the square root of the indirect lighting value to slow its dropoff. But, this is the basic algorithm, and you can tweak it to work for your setup.

### Side Note: Direct Lighting

I just thought I'd make a brief mention of direct lighting, since in ICED it actually uses the conduction mask for visibility! The direct lighting is pretty standard deferred rendering, but I didn't want to render a shadow map for each light source (would be slow). Instead, to compute visibility, I decided to raytrace through the conduction map since it already tells me the scene's (simplified) visibility! All I did was multiply the direct lighting by eight evenly spaced pixels in the conduction mask between the light position and the scene position. Depending on the size of each pixel in the mask, eight is probably enough to ensure that the samples will not miss a wall until the direct lighting is dark enough that visibility doesn't matter. Not a bad way to add visibility to all light sources for only eight texture reads, huh?

## No comments:

## Post a Comment