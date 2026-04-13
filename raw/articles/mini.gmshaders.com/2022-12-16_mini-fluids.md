---
title: 'Mini: Fluids'
url: https://mini.gmshaders.com/p/gm-shaders-mini-fluids-1507038
author: Xor
published: '2022-12-16'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Fluids

### Making a metaball shader to enhance fluid particles!

Hi people!

I recently wrote a little shader for a fluid system in GameMaker and I wanna share how it works here!

**Note:** This is not a fluid solver shader, but some shader magic to make GameMaker's physics particles even better! These tricks can be applied to any particle system though, so you're welcome to adapt them to your specific needs. Example included at the bottom!

## The problem

Take a look at a basic fluid system:

Here you can clearly see the water is composed of many little circles (the mask shown in the top-right corner). This isn't very convincing. It looks more like sand than fluid. We could make the particles smaller, but it will cost more performance.

Instead, we can try some with a gradient:

This looks much closer, but it is a bit fuzzy now. We can fix this by adding alpha contrast using a shader.

## Setup

Before we can apply a shader, there's a little bit of setup that we need to do first. We want to draw all the particles to a surface so that we can apply a shader to blended particles.

Here's how I did it:

Create a water surface. This should be the size of the room or view,

Set the blend mode so that

[alpha is blended correctly](http://gamemaker.io/en/blog/alpha-and-surfaces):`gpu_set_blendmode_ext_sepalpha(bm_src_alpha, bm_inv_src_alpha, bm_one, bm_one);`

Draw the particles on the surface and reset the surface and blend mode.

Apply the water shader to the app surface with the water surface included as a uniform sampler.


Here's the code I used:

Okay, now we're ready to modify the water surface with a shader!

## Metaballs

Metaballs are used to smoothly blend balls or droplets together, producing more fluid results!

In the fragment shader, we need to sample the water surface and the base texture so that we can handle the alpha blending ourselves:

`vec4 water = texture2D(u_surf_water, v_vTexcoord);`


Here's the contrasted formula I'm using for the corrected alpha:

`float alpha = smoothstep(0.7, 0.8, pow(water.a,2.0));`


The 0.7 sets the minimum alpha threshold, while 0.8 is the maximum value.

Feel free to play around with the values here! Lower values will make the droplets larger and higher values (up to 1) will make the droplets smaller. And a greater difference between the values will make the drops softer.

Finally, the power's exponent (here is 2.0) changes the extent of blobbiness.

Next, we sample the base color (from the application surface):

`vec4 col = texture2D(gm_BaseTexture, v_vTexcoord);`


And blend water with it using this alpha value:

`col.rgb = mix(col.rgb, col.rgb * water.rgb, alpha);`


Notice how I'm mixing `col`

with `col * water`

. This gives the water a translucent look!

Here are the results!

That looks so much better than anything above! Here's the full fragment shader I used:

## Refraction

As an optional extra step, you can add a simple refraction effect at the edges of the water. Unfortunately, I'm running short on time, so I'll leave this as an extra challenge for anyone who wants to try it (example included below).

Essentially, I sample the alpha of the water in 4 neighboring directions and use this to compute a direction vector that points toward the water's edge.

Then I offset the base texture using this displacement vector. I also added a small "refraction" factor which scales the texture coordinates down slightly toward the center. This makes the underwater scale slightly larger and helps differentiate underwater from out-of-water.

Here's what that distortion looks like:

Here's the frag shader I used:

## Conclusion

As promised, here's the [source code](https://github.com/XorDev/2DFluids)!

Unfortunately, **Revue is shutting down** soon, so I have to find a new place to post my mini tutorials. When I find an appropriate alternative, I will let you guys know! In the meantime, consider following me on [Twitter](https://twitter.com/XorDev)!

Anyway, this tutorial was a little different. Most of my tutorials up to this point are about general shader tips and while this one can be applied in other particle systems, it's still pretty specific. Let me know if you liked this!

Thanks for reading and have a great day/night

-Xor