---
title: '2D game art: the procedure of making a facebook hidden object puzzle'
url: https://www.gamedeveloper.com/art/2d-game-art-the-procedure-of-making-a-facebook-hidden-object-puzzle
author: Junxue Li
published: '2013-11-05'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# 2D game art: the procedure of making a facebook hidden object puzzle

This article is about the scene art making for a facebook hidden object game.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Our 2D art team recently work on a facebook game: Seaside Hideaway. It’s a theme hidden object game, featuring many beautiful coastal resorts. It’s link:

Here I gave the procedure for making one of the hidden object puzzles. From design to finished.

It’s a roulette room inside of a casino. The client wants the layout look like this picture, with the interior redesigned:

![](../../assets/2c0163b810e354d7.img)


Although the client doesn’t strictly require the scene should be created in 3D, they only require the style and quality meet, we think incorporating 3D making into the creation, would save some labor. Because it’s an interior scene, in 3D it would be easier to adjust camera angle and furniture, if the client asks us to do so.

1.Design Stage:

The idea is to construct the scene by 3D models, then render neat line art out of the 3D scene, and deliver it to the client to review.

Here is the scene we construct in Maya:

![](../../assets/dec7444a59b6ff2c.img)


In fact it takes less time than you may think. Here are how we get the models:

Roulette table: We search on google “free 3D model roulette”, and choose a good one. The Wheel is very close to the camera, so it needs good details. But the downloaded model is very basic geometry, barely a cylinder on this part, it needs more work. You can see the white parts on the wheel, we hand model them. In fact they are very simple geometries too.


There are thousands of chairs there, but it’s strange that finding a chair exactly what you want is so difficult! We find a close chair, and add the rim by ourselves. You can see the green highlighted part.

The blackjack table to the left, is borrowed from another scene, for we have made so many casino scenes for this game.

The background of the room is modeled by hand. You can see they are very simple geometries too.


And then, here we go, it is the line art we render from this scene. I have a separate blog article about how to render the line art out of 3D scene.

![](../../assets/14dfd7acec2788cf.img)


Then we hand paint the color and lighting design. Now the design stage is done.

![](../../assets/65c86101eaa61dbf.img)


2.Finished Art Stage:

At this stage, we first render a 3D image, then overpaint it in 2D, to meet what the client wants.

Below is the 3D render we have made.

![](../../assets/04adc98f721f7c34.img)


The 3D work has two main steps: texture mapping and lighting.

In the texture mapping step, we spend the bulk of the time looking for fitting textures. We look into our own inventory, google, and paid online texture store.

We need a high definition pattern for the table, but we can’t find, so we made one:

![](../../assets/af7f8df921522248.img)


The mapping is very simple. To save time, we only use basic UV projection tools, such as plane projection, cylinder projection, automatic projection. We don’t fix texture seams and other mapping issues, because we can address them in the later 2D overpaint stage.

And the lighting is simple, too. We just put a point light above each of the roulette table. And throw in a few specular-only lights to create highlights for the objects. Just keep in mind, to save time and budget, keep the lighting simple. The lack in the lighting can be complemented by 2D overpainting.

Once we have the 3D render image, we pass it to 2D artist. The artist would overpaint it, making it more like a painting. The most important jobs to be done at this stage, are as follow:

Add more subtle lights, to make the lighting of the scene more rich;

Add brush stroke to everything, to make the picture more like a painting.


In the future articles, I will give more detailed walkthrough of this 2D overpainting stage.

![](../../assets/2fba9d79e7176c58.img)


3.Object placement & overpainting

Since it’s a hidden object game, it’s time to populate the scene with objects. Making hidden objects also involves many rules and tricks, I will explain in future articles.

![](../../assets/4b623fa1d15e1e22.img)