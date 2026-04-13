---
title: Good tactics of producing 2D game scene
url: https://www.gamedeveloper.com/art/good-tactics-of-producing-2d-game-scene
author: Junxue Li
published: '2013-07-19'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Good tactics of producing 2D game scene

This article is about the method of the 2D game background art creation.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Please first take a look of this picture, this is a screenshot from a facebook hidden object game Jane Austen Unbound. The setting is in early 1800s England. (This picture is not produced by our team, because it is a picture in the public domain, we take it as example to illustrate the ideas in this article.)![](../../assets/8a7457b715d1cb90.jpg)


For scenes like this, after the design is greenlighted, we would think of the production of the picture. We can break down the picture to individual elements. Here we have couch, clock, piano, frames, stair, etc. To make an individual thing, for example, the couch, the most easy way, is to find a photograph, which is in the right shape and perspective, and with enough pixel resolution. Then you compose the photograph to the picture, apply some overpainting, then it’s done.

In most cases, you can find tons of photos of desired shape, but none is in the right perspective. Then lots of extra effort is demanded. You would cut parts of different photos, legs, plates, add some deformation, then stitch them together to get the thing you want.

Sometimes you get a good photo, but the details are too blur, rendering it useless.

In these situations, you can think a bit of 3D. The basic ideas is to download free models from the web, do some simple render, then add overpainting.

Here are few good sites to download free 3D models:


For the above particular scene, let’s see the result of a few model searches in archive3d.net

![](../../assets/7fadbd012b543073.jpg)


On this site, there are usually scores of models of certain object, for example there are over 2000 models in the “Couch” category. You can choose the one fits your need best.

After having decided what objects in your scene should be 3D, the best tactics is to gather all these models, put them together in a 3D scene, render out a single color image, then proceed to 2D editing&overpainting.

Keep in mind, the final image depends much on 2D overpainting, so you don’t need to employ high end method of 3D production as the movie industry would demand, such as very complex shaders, advanced lightings. Try to get the 3D images by cheap method, to produce your scene fast and reduce cost (But by no means compromise quality.)

Let me give you a simple example to illustrate this idea. Sorry I can’t show our full 3D scenes, let’s go with a single furniture.

Download this cabinet model form [www.3dmodelfree.com](http://www.3dmodelfree.com/).

It’s UVs is not very good. That I use cylinder projection to fix the legs. If you get a model with bad UVs, only use basic projection tools, such as plane projection, cylinder projection, automatic projection. This can save the labor to the minimal shape. Don’t manual tweak UVs, and don’t mind the seam of the textures. Keep mind we can address these issues easily in 2D overpainting phase.

Then find a good wood texture for it, use a basic blinn shader, crank the highlight of the shader a bit. And the drawer handle is assigned only a simple white shader.

About lighting, only give a key light and a fill light. Keep in mind we will give more subtle lighting in 2D afterward. Don’t try advanced lightings such as global illumination and final gather, they are slow.

Ok, then render a color image.

![](../../assets/f7e3931c9fdb9802.jpg)


Then an ambient occlusion(AO) image.![](../../assets/1c142927e6359f1d.jpg)


Compose the AO image on top of the color image, which gives a sense of structure and volume, it’s a good compensation to our cheap way of texturing and lighting.![](../../assets/5a765745a7011069.jpg)


Then we go to the final 2D overpainting stage.

To our experience, either you overpaint photo objects, or first 3D render then overpaint, the quality and style of the resulted graphics are of no difference. And about which method to choose, it’s very singular: we only 3D render those objects in the scene that a good photo is not available.

So in your production, don’t insist on a all 2D or all 3D scene, try to find the most labor saving combination.

Things good for 3D: furniture, machines, architectures, manmade items;

Things good for 2D: rivers, mountains, plants, grounds.

There’s a trick worth mentioning. If you design a scene from scratch for your client. For example, if you need a vintage sofa in your picture. Before drawing the line art, first look into the 2D photo and 3D model library. Only if you can find a desirable sofa in the library, that you put it into your design. And later in production stage, it’s very straight forward process, only a matter to overpaint the sofa you already have; on the contrary, if you design the sofa totally by mental work, and later you can’t find an identical sofa photo or 3D model, that means you must build this thing all from scratch, a lot more of works!

This trick doesn’t apply if your picture style is hand-painting. By even in this style, 3D rendering would do you some help. It would give you precise shapes and perspective. One of my friends make pictures in this way: he first builds everything in the picture in 3D, then he doesn’t assign any texture and lighting. He just renders a grey scale image by ambient occlusion, then he hand paint the whole picture.