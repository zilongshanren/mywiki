---
title: Adding static water with pixel art and 3D
url: https://www.gamedeveloper.com/art/adding-static-water-with-pixel-art-and-3d
author: Roque Rey
published: '2015-01-15'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Adding static water with pixel art and 3D

In this post we'll be talking about the water in Okhlos, and how we went about making it using Unity. Very artist friendly post!

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

In today's post we'll be talking about the water in [Okhlos](http://okhlos.com/)' fourth world, Atlantis, and how we went about making it using Unity.

Mind you, we won't be talking about fluids simulation or anything like that - these will just be a few notes about our experience developing water for the game. Do keep in mind as you read on, that in Okhlos, we try to blend pixel art with a low poly aesthetic, but we also use shadows, HDR, bloom, and lots of "new" effects - just because we can!

The composition of the water in Okhlos is quite simple: it's a plane. ![waterPlane waterPlane](../../assets/0ab4818daac05fc7.png)


The water is above the actual ground of the game... duh.

It's a plane above the actual ground of the level, so the units, buildings, and enemies never interact with it. The ground is the one that posseses all the physics components, so it still handles all the collisions itself. The water is just a mesh child of the ground.

The water has a transpartent/diffuse material, and there isn't much more to it than that. We don't reduce the opacity of the texture, we just change it in the materials settings. This gives us much more control, and, since we're working directly on the final look as we make changes, we can just do it all within Unity instead of having to export out a texture for every tweak we want to make.

![matProp matProp](../../assets/d09ee5d977d4e1e3.png)


"Agua" in spanish means water :P

As far as water within other objects goes, all the water in streams and containers was made in 2DToolkit, which makes animating it so much easier and gives us far more versatility. ![agua agua](../../assets/4bb0538a9203a583.png)


As you can see from the picture above, almost all the water streams for the objects are made using sprites. We animate them frame by frame. 2DToolkit has an incredibly useful pipeline for this kind of work. We still need to export the sprites, but we change their sizes, shapes, and orientations very quickly, and we can see the results almost immediately.

![barrilbebedero barrilbebedero](../../assets/8c09f53d9cc55adb.png)



![waterFountain2 waterFountain2](../../assets/acc9cbb39c0b740f.gif)


This fountain has 8 different sprite animations, just to illustrate the versatility of our system.

![fuente fuente](../../assets/6e11003fbe35a525.png)


The only real problem we had with this approach was that we had to change the material of the water within the objects to differentiate it from the water plane. The water has an Additive Vertex color material, which is why it almost seems to glow.


The cascading water, as we mentioned before, is a sprite animation, but the ripples are produced using Unity's particle system. ![waterFlow waterFlow](../../assets/3b1397eed70b458b.gif)


It's actually a pretty simple effect, it's just a looping particle that throws instances every now and then.

![Captura de pantalla 2015-01-07 11.07.37 Captura de pantalla 2015-01-07 11.07.37](../../assets/c370b28fcf7fbddb.png)


With just a few tweaks we can apply the effect to a character. We just need to change the Emission from Time to Distance, and the simulation space to local. ![waterRipplesCharacter waterRipplesCharacter](../../assets/10f0430fcbc853a4.gif)



So, there you have it. If you want to add static water to your game this can be a good approach. It's far from perfect, but it has proven to be quite useful for a game like ours.

And, as always, any feedback is welcome!

This article was proofread and edited by [@pfque_](https://twitter.com/pfque_)!