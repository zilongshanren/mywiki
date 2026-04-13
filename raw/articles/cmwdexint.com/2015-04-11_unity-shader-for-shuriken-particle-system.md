---
title: Unity Shader for Shuriken Particle System
url: https://cmwdexint.com/2015/04/11/unity-shader-for-shuriken-particle-system/
author: Ming Wai Chan
published: '2015-04-11'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

I know many people are curious about how to make shaders available for **Shuriken Particle System** to use, the concept is very simple!!


The key is just the** INPUT COLOR** given by Shuriken Particle System:

The** input color** is the only value that particle system can pass to shaders. And of course shaders must grab this value and use it to calculate the output color.

This is the same case as those GUI plugins like NGUI and Unity 2D sprites, they let you have different colors on different sprites but just using the same material.

Okay now, so **how to “grab” the input color?** Let’s start with an **SURFACE SHADER** example of changing the unity default Mobile/Diffuse Shader into a particle-system-supported transparent diffuse Shader.

1. duplicates the shader you want to edit, prepare a texture and creates a material. Assign the material with shader and texture. You can always download Unity default shaders package [here](http://unity3d.com/get-unity/download/archive). Below is the texture I used:

2. Remember to change the setting of the texture if you want to use the texture alpha value.

3. open up the shader and edit the Mobile/Diffuse shader as follows:

4. you now have a Particle diffuse shader xD!

What about unlit shaders? It is better to use **VERTEX and FRAGMENT shaders** if you are not interacting with lights (cheaper in performance) Here is the example. Again, I used Unity default Unlit/Transparent shader:

Easy enough right?

To be inspired, the input color is a float4 value…..that means you have four 0-to-1 floating point numbers to play with! Beside using them to control colors and alpha, they can also be used to control the magnitude of different effects like distortion, dissolve, displacement…more and more!

****

Here are some videos that I made particle dissolve shaders for my partner. He used the shaders and create different effects:

They are of course vert and frag shaders. The dissolve effects used the** input color alpha** as the variable to decide whether that pixel should be vanished or stay visible.

Hard dissolve used **‘step’ **function:

Soft dissolve used** ‘smoothstep’** function: