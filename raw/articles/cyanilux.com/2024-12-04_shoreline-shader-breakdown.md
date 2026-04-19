---
title: Shoreline Shader Breakdown
url: https://www.cyanilux.com/tutorials/shoreline-shader-breakdown/
author: Cyanilux
published: '2024-12-04'
source_blog: Cyanilux Shader Tutorials
source_site: https://www.cyanilux.com/
category: graphics
fetched: '2026-04-19'
---

# Shoreline Shader Breakdown

## Intro

Heya! I’ve had a couple mini-breakdown threads related to shoreline/coastline water shaders on twitter/X for while, but since that site might implode at any minute… it’s probably best to convert them into a post here. I could just copy those threads, but wanted to go into a bit more detail. And as both shaders have some similarities/overlap, I decided to merge them and basically rewrite everything… (whoops? 😅)

## Original Twitter/X Threads

As with most of my work, I lean more on the stylised side, though it’s possible it could be adapted to work in a realistic/PBR style. And to be clear, I’m focusing on shoreline-specific parts of the water shader in this post, not sand material(s) or other details in the water which you might want - such as refraction or caustics (for that see the [Water Shader Breakdown](https://www.cyanilux.com/tutorials/water-shader-breakdown/) or other links under the Water section of the [Resources page](https://www.cyanilux.com/resources/#water)). The shader does use some transparency / alpha blending to darken the material below though, to simulate the sand being wet.

There’s two main ways I’m discussing that can be used to map the waves to the scene - using the **Depth Texture** or **Manual UVs**. Below I’ve listed some notes/pros/cons of each method. The later sections work for either of those setups.

**Sections :**

[Depth-Based Shoreline](https://www.cyanilux.com#depth-based)- Potentially a simpler setup, but causes waves to follow along / projected onto the ground
*below*the water. Therefore it might only look correct on quite shallow-sloped beaches and top-down camera perspectives. - Is more difficult to give the waves a particular shape/texture. The depth produces a gradient towards the beach but not a horizontal one along it. You can map textures (i.e. noise) with a planar worldspace mapping, but those won’t scroll in the same direction as the waves.
- Would also automatically cause the waves/foam to appear on any objects intersecting with the water. (Could probably be seen as both a pro or a con, depending on the situation)

- Potentially a simpler setup, but causes waves to follow along / projected onto the ground
[UV-Based Shoreline](https://www.cyanilux.com#uv-based)- Requires 3D modelling a custom shoreline/water mesh and manually setting appropiate UVs to map the waves correctly.
- But unlike the depth method, the waves are actually on water surface and you have better control over what they look like (as you can map textures to those UVs)
- Waves/foam won’t appear on other objects. You could still use depth to handle that intersection separately (e.g. edge foam example below), or use an alternative method to show interaction with water, such as spawning particles.

[Approaching Waves](https://www.cyanilux.com#waves)[Swash Wave](https://www.cyanilux.com#swash)[Wet Sand](https://www.cyanilux.com#wet-sand)

## Depth-Based Shoreline

One of the simplest ways to have water interact with the rest of the scene is by using the depth texture, such as the *very* common “depth intersection / edge foam” technique you see in a lot of toon/stylised water shader tutorials. For example :



![(Image)](../../assets/a0c19d31ac102486.png)

Or using the W/A component from Raw **Screen Position** for the B input, which is the same but only works for perspective projections, while `abs(positionVS.z)`

should work in orthographic too!

Though this method tends to have some warping as the camera rotates, likely because depth values are relative to the camera plane.

Similar to the [Fog Plane Shader Breakdown](https://www.cyanilux.com/tutorials/fog-plane-shader-breakdown/), I instead tend to **reconstruct the world position from depth**, then take the Y coordinate of that and subtract it from the Y of the water plane.

Provided the water plane GameObject isn’t marked to use static batching, we can obtain it’s Y coord from the **Object** node (**Position** output), which returns the origin point of the mesh. Alternatively, you could use a **Float Property** and just control this value from the material inspector.

This produces a *gradient of how deep the surface below the water is*, which you could **Step** in the same way as the earlier example to produce edge foam - But more importantly since it doesn’t have that warping, and assuming the shore/beach terrain is sloped, we can also map waves using it!

You can optionally have a **Multiply** node after this to apply scaling - though it’ll also scale depending on the steepness of the beach.

May also want to **Saturate** to clamp any values outside the 0-1 range, and then **One Minus** to invert the gradient - so it matches how the UV method below works and the graphs later produce correct results.

[ShaderGraphVariables](https://github.com/Cyanilux/ShaderGraphVariables)package to add

**Register Variable**&

**Get Variable**nodes (installed via Package Manager -> Add package via git URL :

`https://github.com/Cyanilux/ShaderGraphVariables.git`

)
([Optional skip to Approaching Waves section](https://www.cyanilux.com#waves) if you’re following this method)

## UV-Based Shoreline

Another way to obtain a gradient towards the beach would be to use a custom mesh, where you could map Vertex Colors or unwrap UVs in a particular way. (This could also probably work on a tileset for a procedurally generated approach, i.e. a sections of beach which piece together to form an island)

Unlike the depth approach, this would let us map waves to the water surface, rather than projected below. Using UVs also allows us to map textures of the waves, for more control over what they look like (and potentially cheaper if you swap out some of the calculations for additional textures? - but that’s something you’d have to test/profile)

As an example of how you might set up a mesh for this, if we model the **shoreline water** as a strip of quads, in Blender you can then UV unwrap using these steps :

- Select one quad in the face selection mode
- Use
**UV**(heading at top or U key shortcut) →**Reset**- May also want to check the orientation by applying a texture. In particular, I use a UV.y value of 0 for water/sea, and 1 at the shore/sand. Though it’s not super important as you can also swap the axis or invert in shader later

- Select all quads along shoreline
- While holding shift, double right-click to unselect and reselect the quad already unwrapped (to set it as the “active face”, if it isn’t already)
- Use
**UV → Follow Active Quads** - Optionally scale UVs horizontally in UV Editor window (or can apply scaling in shader later)

## Further modelling/adjustments

After this, I used a duplicate of this mesh to model the section of beach, where the top set of vertices matches up to avoid any seams.

Also optional and may not be important right now, but in the water mesh I also added a loop cut (near the top / beach-side of the quads) and moved the lower quads (water-side) down slightly, matching that loop with the slope of the beach (but slightly above to avoid any z-fighting). This creates a sloped section in the shoreline mesh will be where the waves move back and forth.

In Shader Graph, start by using the **UV** node then **Swizzle** - in my case using the “Y” axis. (Alternatively **Split** and use **G** port). This obtains a *gradient towards the shore/beach*, which is important if we want to map waves and have them scroll in that direction.

The output of this may be used multiple times, but instead of long connections you can easily duplicate this group as it’s small and not doing any calculations.

## Approaching Waves

A few stylised water shaders I’ve seen (and made) actually have some small scrolling lines, as a way to “dissolve/combine” depth based edge foam into the rest of the water. That’s the same technique but typically much more squished and scrolling in the opposite direction.

Firstly, we can introduce some noise (either by sampling a seamless noise texture or procedurally via **Gradient Noise** node) to distort the gradient a little, and then use **Time** to make the waves scroll/move - In this case using **Subtract**, as the gradient is 0 at the beach and increases to 1 in the water. (If it’s reversed for you, can **Add** the time instead, or use **One Minus** on the gradient to invert it)

To create repeating lines, we can then **Multiply** by some value (e.g. 3.2) and either use :

**Fraction**(`frac`

in hlsl), repeating at each integer value**Cosine**, producing a line at every`2*Pi`

(aka`Tau`

),**Sine**works too, but is offset by`1/2 Pi`

- To make this more consistent, I’ve used a
**Multiply**by the TAU**Constant**, but you could manually handle this by using a different scaling value (i.e. 20 instead of 3.2)

- To make this more consistent, I’ve used a

Then **Smoothstep** to remap the range of values, making the lines thinner. It also clamps any negatives. (Can alternatively use **Inverse Lerp** & **Saturate**)

To have the waves fade in, use **Smoothstep** on the gradient (e.g. with an **Edge1** of 0 and **Edge2** of 0.5), and **Multiply** to apply that

You can also optionally mask the waves with some noise to break up the lines a bit, as shown below. If using the depth-based method for the shoreline gradient, using an XZ planar mapping may be more suitable than the UVs on the water mesh.

For applying colours, I’m using **Lerp** with the the shoreline gradient in the **T** input, to interpolate between a blue and cyan - so the colour gets lighter at the shore. Then another **Lerp** to apply the wave foam colour (set to white / 1,1,1,1)

## Swash Wave

In real life after waves hit the shore, a foamy layer of water (known as [swash](https://en.wikipedia.org/wiki/Swash) in geography) moves up the beach until it loses enough energy, then retreats back to the sea. The easiest way to simulate this in the shader (that I could think of), is to add another wave which moves back and forth, synced with the scrolling of the others (though I won’t lie, it took me far too long to figure out how to properly sync it 🙃)

To handle that motion, we can use a **Cosine** node (or **Sine** if you use that for the approaching waves). This may not be entirely accurate to real life, where the flow of water up the shore tends to have a shorter duration than when it retreats, but I think it’s good enough.

The input needs to be **Time**, multipled by the same *“Scroll Speed”* and *“Wave Count”* (value in “no. of waves” group) as used in the Approaching Waves section above. I’ve converted those to **Float Properties** in both places, so they can be adjusted from the material and always match.

We also need to **Multiply** by the TAU **Constant** - (unless you use the **Cosine**/**Sine** method for repeating lines and already removed the **Divide** earlier!)

Those multipliers means after one period/cycle of the swash wave (a back-and-forth), one approaching-wave will pass. The actual motions won’t line up since one wave is sinusoidal and the other scrolling linear - but the durations are the same. But the phase might not match up yet, so as shown above, we also need to **Add** a **Float Property** which I’ve named *“Time Offset”*. This can be controlled from the material so we can manually sync it. (e.g. a value of roughly **-2.5** seems good when using a *Wave Count* of **3.2**)

Since the **Cosine** returns a value between -1 and 1, we **Multiply** by a small value to adjust how far the wave will move. You *miiight* want this value dependant on the *Wave Count* (e.g. calculated as `0.5 * (1/waveCount)`

), but it’s not that important to match perfectly. I’m just hardcoding it as **0.1** here.

We apply this to the distorted shoreline gradient from earlier using an **Add** node, then **Smoothstep** to remap and position the wave (centered at around 0.8 along that 0-1 gradient)

### Combine Waves

The output of this can be combined with the approaching waves using a **Maximum** node, before the **Lerp** that applies the foam colour (“water vs (wave) foam” group)

Also take the output of the “apply offset” group and use another **Smoothstep** with **Edge1** and **Edge2** values of 0.85 and 0.84 to produce a mask of where the water/swash ends. We’ll temporarily use this for the **Alpha** output in the **Master Stack**.

Could alternatively use **Step** here, but I’m using **Smoothstep** so the edge is slightly anti-aliased. There are also better ways to make an anti-aliased version of step with fwidth/**DDXY** node, such as in [this article by Ronja](https://www.ronja-tutorials.com/post/046-fwidth/).

### Adding Voronoi

That could work as-is, but it’s a little boring, so lets add a texture to the swash wave. I’ll be using this seamless Voronoi/Worley Noise I baked out. (The **Voronoi** node could also work but using a texture here is likely cheaper)

Use the **Sample Texture 2D** node to sample that texture. Like the earlier noise, using a XZ planar mapping for the UV input may be more suitable if using the Depth-Based Shoreline method.

For the UV-Based Shoreline we can make the texture move with the swash wave, by using the output of the “apply offset” from the last graph screenshot in the **Y** of a **Vector2** node, with the **X** set to the **R/X** of the **UV**

To combine this texture with our wave, we can **Multiply** the **R** output with a small value (e.g. 0.15) then **Add** in between the “apply offset” group and **Smoothstep**

### Animating Values

To better animate the wave, take the output of the **Cosine** / “swash motion” group and remap it into a 0-1 range using an **Inverse Lerp** node using **A** and **B** inputs set to -1 and 1. (Alternatively can **Multiply** by 0.5 then **Add** 0.5)

**One Minus** to invert this, producing a value of 0 when the wave is retreated, and 1 when fully up the beach/shore. We can **Multiply** this by our voronoi (before the **Add**) so the texture fades in as it approaches the shore.

To add a bit of a “dissolve” effect, we can also animate the **Edge1** (on **Smoothstep**) using the **Inverse Lerp** output into the **T** of a **Lerp**, with **A** set to 0.7 and **B** set to 0.8. (You can adjust these values if you want, but make sure **B** isn’t greater than the **Edge2** input or the **Smoothstep** result flips!)

## Wet Sand

A somewhat important effect I wanted to simulate was letting the swash wave leave the sand behind **wet** - which is basically just darker (and more reflective)

Instead of making pixels/fragments beyond the swash wave completely transparent, we can use a black colour with a very low alpha. This is a main reason why I chose to use alpha blending instead of vertex displacement (which might also show too much of the geometry when as it clips)

For the **Base Color** port in the **Master Stack**, we can take the current result and **Multiply** by what we currently have in the **Alpha** (output of “sand (0) / water (1)” group)

For the **Alpha** port, we’ll re-use the distorted gradient (from the start of the Approaching Waves section - quite a while ago!), and another **Smoothstep** to mask out the area we want the sand to be wet in. This is also to avoid seeing the top edges of the shoreline geometry/mesh.

We’ll combine this with the current alpha value using **Add** then **Saturate** to make sure values don’t go above 1. (Can alternatively use **Maximum**)

To allow the water and wet sand to be shiny, could likely also use a duplicate of this setup for the **Smoothness** port, assuming a **Lit Graph** type. But with a higher value than 0.2. I rarely work with PBR so I’ll leave that up to you.

I guess you could also calculate specular highlights manually even in an Unlit Graph - my [Custom Lighting](https://github.com/Cyanilux/URP_ShaderGraphCustomLighting) package has a node that might help with that for URP.

## Thanks for reading! 😊

If you find this post helpful, please consider sharing it with others / on socials

Donations are also **greatly** appreciated! 🙏✨

(Keeps this site free from ads and allows me to focus more on tutorials)