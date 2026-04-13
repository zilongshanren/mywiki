---
title: Frequently Asked Questions About The Aztez Art Style
url: https://www.gamedeveloper.com/art/frequently-asked-questions-about-the-aztez-art-style
author: Ben Ruiz
published: '2014-07-09'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Frequently Asked Questions About The Aztez Art Style

Ben Ruiz of Team Colorblind discusses some of the art tips and tricks used in their upcoming game, Aztez. Traditional 3d outlines, shaders, 2d and 3d usage, and art styles in general.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Hi! This is [Ben Ruiz](http://www.benruiz.net), artist and combat designer at Team Colorblind, developers of [Aztez](http://aztez.com).


We've had Aztez on the promotional tour for some time now, and we get these questions a LOT and I wanted to take a chance to answer them:


Is Aztez 2d or 3d?

How do you outline your assets in black?

What shader are you using to create your look?

Why make a game in this style?


### 1. Is Aztez 2d or 3d?

Aztez is indeed fully 3d! That's why it works with the Oculus. Our characters are skinned skeletal meshes with 3d animations. The only 2d assets we use are in effects.

![AztezIs3DAndInk1 AztezIs3DAndInk1](../../assets/a01e7f8a3af35e18.gif)


### 2. How Do You Outline Your Assets In Black?

![AztezIs3DAndInk2 AztezIs3DAndInk2](../../assets/9bd8d00a965e4ca6.jpg)


Read More...

So unless you've told your game engine to render both sides of faces, then the object will look outlined regardless of what angle you look at them from. This is a primitive solution and any object with an outline of this kind is going to have some bad angles. But it ultimately comes down to the style of your game. And for whatever it's worth, it's substantially less intensive a solution than post processing shaders, since it's just a couple more faces.

![AztezIs3DAndInk3 AztezIs3DAndInk3](../../assets/01ec95bfcaa8adb4.gif)


### 3. What Shader Are You Using To Create Your Look?

As for our shader, it simply self illuminates everything 100%, but also allows me to adjust the black parts of a texture from black to grey to white. This shader powers 95% of our game's objects, and I simply adjust the grayness per environment layer by duplicating the shader, adjusting the greyness, and naming it appropriately. So all objects in the foreground use "Structural Swatch - Foreground", and all objects in background layer 1 use "Structural Swatch - Background", and etc. This way, there is consistency, and anytime I adjust the material, it cascades to all objects in that layer.

![AztezShader AztezShader](../../assets/08f2ff3505fd4bf3.jpg)


### 4. Why Make A Game In This Style?

First and foremost, it's because I think it's cool. Production sucks unless you're making something you actually like producing. But it grants us a massive advantage, which I have outlined in this image. Click the image for a larger version!

![Why-Black-And-White Why-Black-And-White](../../assets/9dfa7cc9bd329e6c.jpg)


That's it for now! I hope this was insightful and useful. I will keep adding to this list over at the [Aztez devblog](http://aztez.com/blog/) as I remember more frequently asked art questions.