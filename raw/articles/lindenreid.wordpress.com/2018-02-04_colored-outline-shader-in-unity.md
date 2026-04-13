---
title: Colored Outline Shader in Unity
url: https://lindenreidblog.com/2018/02/04/colored-outline-shader-in-unity/
author: View all posts by Linden Reid
published: '2018-02-04'
source_blog: Linden Reid
source_site: https://lindenreid.wordpress.com
category: graphics
fetched: '2026-04-13'
---

It seems like I’m on a roll with outline shaders! I’ve already written a [basic cel shader with outline tutorial](https://lindenreid.wordpress.com/2017/12/19/cel-shader-with-outline-in-unity/) and an [animated dotted outline shader](https://lindenreid.wordpress.com/2017/12/24/animated-dotted-outline-shader-in-unity/), and now I’m doing this colored outline.

The special thing about the color of this outline is that it’s using the color of the texture, so that the **outline color always matches the pixel it’s closest to**. I find it’s a common tool used by 2D artists to make outlines feel more natural, as opposed to using a solid color like black for the whole outline.

Here’s an example of the difference it makes with an example from 2D pixel art from [u/croakiee on Reddit](https://www.reddit.com/r/PixelArt/comments/3e2gio/occc_two_game_characters_should_i_do_black/):

![outlineEx](../../assets/f8a5267795e366f2.png)


This tutorial teaches you how to do this effect in 3D.

**IMPORTANT:** Since I already went over [the basics of how to do the outline here](https://lindenreid.wordpress.com/2017/12/19/cel-shader-with-outline-in-unity/), I’m not going to repeat that explanation in this tutorial. **Do the basic tutorial first** if you’re not sure how to create an outline at all.

Here’s the full code for the shader for reference, under a non-commercial open-source license:

Also, The 3D model is from [this free asset pack](https://assetstore.unity.com/packages/3d/characters/humanoids/character-pack-free-sample-79870).

Now, on with the tutorial!


## Colored Outline

This effect is quite simple, and happens completely inside the **vertex shader**.

If you remember from the basic outline tutorial, our outline is created by scaling the original model along each vertex’s normal direction. Now, to make the outline color the same as the vertex color, we simply **sample the vertex color** and add it to the **vertex shader output.**

Firstly, add a color to your **vertex output** struct:

struct vertexOutput { float4 pos : SV_POSITION;float4 color : TEXCOORD0;}

And add one extra line of code in the vertex shader to **sample the color**:

output.color = tex2Dlod(_MainTex, float4(input.texCoord.xy, 0, 0));

And your output should look like this:

![outlineColorstep1](../../assets/c862b42253c45ca0.png)


Why **sample the color at each vertex**, you might ask, **instead of at each fragment** like we usually do? Basically, this is a lazy way of blurring the outline color. The vertex shader is run less often (only for every vertex on the mesh) than the fragment shader (basically for every pixel), and the colors between each fragment are interpolated, which essentially blurs away details. If we sample at every fragment instead, we get too much **detail**, and the outline ends up looking like this:

![outlinecolorpixel](../../assets/8d9256f4654b24f1.png)

Now that you’ve got your outline sampling the vertex color, let’s **make the outline distinguishable** from the model’s texture. As you can see right now, they’re a little bit too similar.

To do this, we’re going to add an outline color property and **multiply our sampled color by the outline color. **

output.color = tex2Dlod(_MainTex, float4(input.texCoord.xy, 0, 0));output.color *= _OutlineColor;

Tune the outline color to a dark grey to get this final result! You can, of course, use whatever color and blending mode you want.

![coloredOutline](../../assets/35b2dffe53459c94.gif)


Good job, you made it!

## Fin

Here’s the [link to the full code for the Unity Colored Outline Shader](https://github.com/thelindseyreid/Unity-Shader-Tutorials/blob/master/Assets/Materials/Shaders/celColoredOutline.shader) again. The full code also includes a cel-shaded lighting pass and shadow pass- if you only want to look at the outline technique, look for the pass labled “// Outline pass”.

I hope you learned something from this tutorial- if not a new technique, possibly just some inspiration for how to expand on common techniques like 3D outlines 🙂

If y’all have any questions about writing shaders in Unity, I’m happy to share as much as I know. I’m not an expert, but I’m always willing to help other indie devs 🙂 And do give me feedback about the tutorials, I love hearing from y’all!

Good luck,

Lindsey Reid [@so_good_lin](https://twitter.com/so_good_lin)

Hey Linden, these outline shader tutorials are great! How would I go about modifying the outline to change color based on whether the pixel is in shadow? So a black outline turns white when in darkness? You already have a shader pass so it seems as the groundwork has already been laid. Any light you could shed would be helpful.

LikeLike

Thank you!! I like that idea. You could do a lighting calculation similar to how you do one in your regular lighting pass 😉

LikeLike

Great tutorial but I’ve run into a problem

I’m using unity 2018 and the outlines only render in editor not the game window

LikeLike

Hello there ! I’m a beginner in shader programming and I wanted to know if it was possible to change the outline’s color depending on the surrounding lights. So far I’ve managed to affect the outline’s color with the directional light, but as soon as I try other light sources the code just switches to the closest one and changes the outline’s color to match that one. If it is possible, would you mind sharing a tutorial about it ? Thanks for your answer, and keep up the good work !

LikeLike