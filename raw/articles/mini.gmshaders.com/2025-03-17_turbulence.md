---
title: Turbulence
url: https://mini.gmshaders.com/p/turbulence
author: Xor
published: '2025-03-17'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Turbulence

### Approximating fluid dynamics and flames efficiently with shaders

Bonjour! Hope you are well!

What do water, fire, dust, magic, wind, fog, smoke and clouds have in common? They are all heavily influenced by turbulent dynamics.

Gases and non-viscous liquids twirl and flow in a way that is quite difficult to compute. There is a lot of mathematical research into problems of fluid and[ there is even a $1,000,000 prize](https://en.wikipedia.org/wiki/Millennium_Prize_Problems#Navier%E2%80%93Stokes_existence_and_smoothness) if you solve one of them. I don’t say this to discourage you, but I felt this context is important.

Today, we are not going to be solving the Navier-Stokes equations (but I will include some resources at the end if you want to). Instead, we will fake it! Proper simulations require multiple shader passes, are slow, memory intensive, and are limited by resolution. Most of the time, we can get away with cheaper real-time approximations and still create impressive effects. Let’s hop in!

# Waves

In essence, all we need to do is add some sine wave displacement. We’ll need to rotate each wave separately to create some curves and break up the visible alignment patterns. The rotation angle isn’t super important as long as the results look natural (not 90 degrees or 45 degrees). For better results, we can also increase the frequency and decrease the amplitude proportionally.

Making a simple horizontal wave might look like this:

```
//Shift the x-coordinates with a sine wave
pos.x += WAVE_AMP * sin(pos.y * freq) / freq;
```


WAVE_AMP can be a constant or macro between 0.0 and 1.0 which sets the overall waviness and the frequency can increase with each pass.

We can rotate with a mat2x2, “rot” and animate with the waves with a time uniform:

```
//Scroll along the rotated y coordinate
float phase = freq * (pos * rot).y + WAVE_SPEED * u_time;
//Add a perpendicular sine wave offset
pos += WAVE_AMP * rot[0] * sin(phase) / freq;
```


Now let’s bring it all together with a loop like so:

```
//Number of turbulence waves
#define TURB_NUM 10.0
//Turbulence wave amplitude
#define TURB_AMP 0.7
//Turbulence wave speed
#define TURB_SPEED 0.3
//Turbulence frequency
#define TURB_FREQ 2.0
//Turbulence frequency multiplier
#define TURB_EXP 1.4
//Turbulence starting scale
float freq = TURB_FREQ;
//Turbulence rotation matrix
mat2 rot = mat2(0.6, -0.8, 0.8, 0.6);
//Loop through turbulence octaves
for(float i=0.0; i<TURB_NUM; i++)
{
//Scroll along the rotated y coordinate
float phase = freq * (pos * rot).y + TURB_SPEED*iTime + i;
//Add a perpendicular sine wave offset
pos += TURB_AMP * rot[0] * sin(phase) / freq;
//Rotate for the next octave
rot *= mat2(0.6, -0.8, 0.8, 0.6);
//Scale down for the next octave
freq *= TURB_EXP;
}
```


Here’s an illustration of the compounding waves:

Here we are starting with a red and green grid to visualize wave distortions. On the left side, we add the first wave (highlighted in blue). The blue arrow represents the direction and length of the waves. As we move right, we add additional waves, and you can see the compounding distortion as more waves are added. This simple effect is enough to create a sense of turbulence in the coordinates.

We can use a texture or noise instead of a grid. Even just 8 iterations can produce convincing results!

[Try my full ShaderToy demo here](https://www.shadertoy.com/view/WclSWn). By adjusting the parameters you can get smooth or swirly turbulence. Here’s what various frequency multiplier values look like”

Increasing the multiplier makes finer, more detailed whirls.

# Fire

This technique works great for fire as well!

It follows the same basic principle with the layering waves, but also with scrolling upward and stretching the coordinates. It starts with the waves tightly compressed horizontally and stretched vertically to simulate fast expansion upwards. As it rises, the space stretches out horizontally and squishes a little vertically for horizontal expansion. It’s pretty subtle, but these fine tweaks can make a big difference.

I won’t put the code here, but you can check out the [full source code over on ShaderToy as well](https://www.shadertoy.com/view/wffXDr)!

# Conclusion

The technique for fluid-like motion is surprisingly simple, yet it produces some pretty decent results! In real-time applications, full fluid simulations are often too expensive, complicated, or too limited to be practical. This method is very practical in a wide range of applications like fluids, flames, steam, smoke, or magic effects!

To recap, it all starts with a sine wave. Just shift the coordinates with a sine wave, rotate, scale, and repeat. After just a few iterations, you’ll get some nice swirls and fluid motion!

Now subscribers can help pick the next tutorial

# Extras

Here are some great resources I found while putting this tutorial together:

** Navier Stokes by Gijs:** This is an excellent example of how simple a Navier Stokes simulation can be implemented in 2D with minimal code!

** Chimera's Breath by Nimitz: **Taking the simulations a bit further with “vorticity confinement”, this shows off some impressive 2D fire and smoke effects.

** Cloud Simulation by wyatt: **Here is a good example of a 3D steam cloud simulation.

** Fast Fluid Dynamics Simulation on the GPU by Mark J. Harris: **For a thorough tutorial on fluid simulation, start here! It covers some of the background context, math, and the implementation.


Okay, that’s it for today. Au revoir!

Great article

:)