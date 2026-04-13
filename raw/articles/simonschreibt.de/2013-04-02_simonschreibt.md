---
title: Simonschreibt.
url: https://simonschreibt.de/gat/007-legends-the-world/
author: Simon
published: '2013-04-02'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Today we’re James Bond and investigate how the world works. Well, the world in a slightly smaller scale. On a display. In a game. But nevertheless, we’ll discover awesome stuff which was created by **Q**. This is related to the [Diablo Case](http://simonschreibt.de/gat/diablo-3-resource-bubbles/) but deserves its own paper. It’s all about the rotating sphere you see here:

+++ TOP SECRET +++

I could reveal the identity of **Q**! It is [MikieX](http://www.polycount.com/forum/member.php?u=75360)! He’s the mastermind behind all this and [asked](http://www.polycount.com/forum/showpost.php?p=1802103&postcount=176) how *we* think it was done. My guess: Texture animation **or** a sphere – squeezed like when you press any air out of a ball. Rolling the UVs over the *flattened* sphere would look “round”.

![](../../assets/c38a5fb40cb8f9f8.gif)


On the left you see a UV space where normally texture space is associated with a polygon:

![](../../assets/f3f55292adc0cbf9.gif)

**R** and **G**! Let’s imagine the UV space as colors: The R channel could be used as **U** coordinate and the G channel as **V**. If you add a red and a green gradient (both reaching from 0 to 255) you end up with what you can see to the right.

It means, *this time* we use ** colors** to associate texture space and positions within the UV space. Of course, your shader has to accept such a texture as UV input. And of course support UV panning for animated results. Here are some examples (

**top**: UV input texture

**bottom**: outcome):

![]() |
![]() |
![]() |
![]() |
![]() |
![]() |
![]() |
![]() |


- Just a unmodified UV input texture. Nothing happens.
- Smudged around with Photoshop. The textures “floats” along the smudge.
- A smaller version of the whole UV input texture. It’s a screen-in-screen effect.
- Our goal: a spherical UV input texture. Below you can read more about it.

![](../../assets/fe3d8a48b9b50110.jpg)

**blue plane** is my baking plane).


Q: “That’s it, Mr. Bond.”

Of course you should create a black/white mask to cut out the corners of the texture but since we only need the **R** and **G** channel, this mask could be stored in the B channel of the texture.

+++ IMPORTANT +++

Important fact (thx to [sinistergfx](http://sinistergfx.com/)) if you want create the base texture with Photoshop. You have to set the gradient **smoothness** to **0%**. If not, the gradient isn’t linear and this leads to weird stretching artifacts. I made an example how different the texture looks with 100% and 0%:

![]() |
![]() |

Thanks to [alfalfasprossen](http://www.polycount.com/forum/member.php?u=45601) for his help when UDK trolled me again.

Oh and i got a [nice link](http://dl.dropbox.com/u/16703380/scrollingUV/scrollingUV.html) from [Tamarin](http://www.zenchuck.com/) where he made this effect with Unity. With sliders!

Thanks for your work, it’s all very interesting. I’m trying to replicate this in the udk but I’ve got terrible compression artifacts. Which setting did you use to get a smooth result?

Thank you :) The spherical Normal Map (i did 4 examples and i mean the texture on the right side ) is set to “TC_NormalmapUncompressed”. The Diffuse Texture (checker pattern + polycount smiley) is set to “TC_Default”.

I know it’s late to answer but you cannot really remove that since it is not really a compression effect but a deformation effect (i think that’s what you are experiencing) and a texture space is not the better space to apply a 3D deformation. I will advise you to compute the right texture coordinates directly in a shader instead of using a UV texture. It worked for me and there is no weird deformation.

Thans for the info! It’s never too late for good comments. :)

I did a version for the game that generated the uv’s in the shader but for some reason I didn’t swap it to that. It might have been cost or time I didn’t have. I was reminded of this again because I found a video of it I made while working on the project.

https://www.youtube.com/watch?v=XsegHXXzQvQ