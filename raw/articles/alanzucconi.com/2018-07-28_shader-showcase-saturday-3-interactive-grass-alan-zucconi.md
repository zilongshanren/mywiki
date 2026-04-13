---
title: 'Shader Showcase Saturday #3: Interactive Grass - Alan Zucconi'
url: https://www.alanzucconi.com/2018/07/28/shader-showcase-saturday-3/
author: Alan Zucconi
published: '2018-07-28'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Forests and fields have always been present in video games. These environments are particularly challenging to reproduce with high fidelity, mostly due to the fact that the behaviour of grass and leaves is exceptionally complex to capture. There are three main challenges.

### Grass Placement

As a rough estimate, there are 250 millions individual blades of grass on a football field. It’s easy to see that placing them individually is simply impossible. Unity itself comes with a simple tool that allows for the placement of grass using bushes to retain some artistic control. However, their solution is pretty limited and does not allow the level of customisation that you might need to produce a more advanced aesthetic. [Casey Muratori](https://twitter.com/cmuratori) wrote an interesting article titled [The Nebraska Problem](https://caseymuratori.com/blog_0011), in which he talks about different strategies to place grass procedurally in *The Witness*.

If you want your game to feature a realistic environment, your best bet is to invest in a tool like [Nature Renderer 6 Pro](https://prf.hn/click/camref:1100l45Ay/destination:https://assetstore.unity.com/packages/tools/terrain/nature-renderer-6-pro-285950), which allows placing grass and trees efficiently and effectively.

### Wind Simulation

Most plants are light and flexible enough to bend even in the presence of the most gentle breeze. This is a big challenge, because modelling each strand of grass and each leaf using rigid bodies and flexible meshes is simply unfeasible.

If we want a solution that can scale well and be efficient, we have no alternative but to fake it. The most common solution that you can see nowadays in games uses a **vertex function **to simulate the movement of the grass as if it was affected by wind. Vertex functions operate on the vertices of a model, and can change its shape. Bending a single blade can be done cheaply by moving the X and Z coordinates based on their distance from the ground. This leaves the bottom part unaffected, but gets stronger and stronger the taller the grass is. Many tutorials on this blog cover vertex functions and how to use them. For a gentle introduction, you can refer to the relative section in the article about [Physically Based Rendering](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/).

To make sure that each individual blade moves as if affected by wind, most developers use sine waves to generate a so-called **wind field**. When used properly, wind fields can be very effective in reproducing a believable wind-grass interaction.

For some high-end applications, simulating how wind interacts with each blade requires a fluid simulation. This approach was used in Unity’s most recent interactive experience *Book of the Dead* (above). In his article [Book of the Dead: Photogrammetry Assets, Trees, VFX](https://blogs.unity3d.com/2018/06/15/book-of-the-dead-photogrammetry-assets-trees-vfx/), Techincal Artist Zdravko Pavlov explains how his team baked the result of a fluid simulation into a texture atlas. This means that, while exceptionally accurate, their solution could not be changed freely during the game. If you are interested, the forest section seen in the video is available on the Asset Store for free: [Book Of The Dead: Environment](https://www.assetstore.unity3d.com/#!/content/121175?aid=1100l45Ay&pubref=az_sss_03).

If your game features grass, there are many assets that can help you achieve a consistent and professional look. One of the most popular is [Advanced Foliage Shaders v.5](https://prf.hn/click/camref:1100l45Ay/destination:https://assetstore.unity.com/packages/vfx/shaders/advanced-foliage-shaders-v-5-68907), which indeed come with a fully customisable wind animation.

For a non-photorealistic look, [Fantasy Adventure Environment](https://prf.hn/click/camref:1100l45Ay/destination:https://assetstore.unity.com/packages/3d/environments/fantasy/fantasy-adventure-environment-70354) is probably the most professional asset you can get, especially if you want that *Breath of the Wild* feeling for your game.

### Object Interaction

Wind is not the only force grass is subjected to. When a character walks on grass, or passes through dense vegetation, we should expect it to move out of the way and then to swing back. Once again, this kind of interaction is often done in the vertex function. [MinionsArt](https://twitter.com/minionsart) published a short video showing how this works. The position of the player is passed to the shader, which uses it to add an outward displacement around that area.

This solution does not scale well, and is only limited to just a few characters. More complex solutions require drawing the interactable objects onto a separate texture, which is then used to control the grass bending. This can also be used to have persistent bending, as it sometimes happens when you walk grass.

## From Twitter…

To get you inspired, have a look at these videos that have been recently shared on Twitter.

## Leave a Reply Cancel reply