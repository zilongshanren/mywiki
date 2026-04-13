---
title: 'Shader Showcase Saturday #6: Dynamic Snow - Alan Zucconi'
url: https://www.alanzucconi.com/2018/08/18/shader-showcase-saturday-6/
author: Alan Zucconi
published: '2018-08-18'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

After two previous instalments of *Shader Showcase Saturday* focused on [wind](https://www.alanzucconi.com/?p=9545) and [rain](https://www.alanzucconi.com/?p=9731), talking about **snow** was simply unavoidable.

Creating realistic snow is a serious challenge, which will be further explored in the following months. This week, we focus on how shaders can be used to add snow to an existing scene. Most of the references shown in this post will not be photorealistic. We will show on how to simulate photorealistic snow and frost in a few weeks. If you cannot wait, I would strongly advise having a look at [Winter Suite](https://www.assetstore.unity3d.com/#!/content/13927?aid=1100l45Ay&pubref=az_sss_06). It contains some of the most realistic shaders for snowy and frosty surfaces.

As you can see from the image above, it supports **translucency**, **subsurface scattering** and the **shimmering effect** that is typically seen in snow.

I have also dedicated a proper tutorial on snow shading, which you can find in the article titled [Surface Shading in Unity](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/).

###### Animating The Snow

What happens to an object when is covered in snow? Answering this question is the first step to decide how to recreate such an effect with shaders. The most obvious change is that snow makes objects white, due to its high reflectivity. Technically speaking, snow looks white because its ice crystals reflect all visible wavelengths of light equally.

This means that tinting an object white is a first step to simulate snow. Most non-photorealistic games indeed rely on this technique. One such example is the following GIF from [Overland](https://store.steampowered.com/app/355680/Overland/). The developers have shared an early test for a snow shader, which progressively tints all ground in pure white.

early early tests for snow

[pic.twitter.com/O0UYarTaMM]— Overland (@OverlandGame)

[March 11, 2018]

Looking at the GIF, it seems that such a transition is done using a **noise texture**. Like the name suggests, they are images which contain a random pattern of some kind. In most cases, noise textures are used as a convenient way to generate (and control) randomness from within a shader. **Perlin noise** is possibly the most well-known process used to generate simple, yet effective, noise textures which are **continuous**. This means that there is always a gentle transition between two nearby points. To understand how important this property is, have a look at the image below.

![](../../assets/e81c1f271586aeb8.png)


On the left, you can see a texture generated from **white noise**, in which each pixel is generated independently from each other. On the right, an example of **Perlin noise **which is smooth and looks more organic.

The snowy transition seen in Overland can be replicated using a grayscale, smooth noise texture. The UV coordinates of the ground mesh are used to sample a colour from that texture. If we only consider its red component, now each pixel has access to a random number in the range ![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


###### Normal-Based Snow

If you attempt to use the solution presented in Overland on a non-flat object, you will get very weird results. This is because snow does not accumulate on every surface equally. All sides that are facing up are directly exposed to snow, and they are the first to be affected. While a noise texture is still a valid starting point, another rule must be integrated for non-flat surfaces. A beautiful example can be seen in the following video posted by Videogame Artist [Olly Wilson](https://twitter.com/Olninyo) for the expansion of [The Signal From Tölva](https://store.steampowered.com/app/457760/The_Signal_From_Tlva/). The frost on the rock starts from the top, and then expands to all other sides.

The snow shader I built for the Tölva expansion, based on object normal, scaling, and position.

[#gameart][pic.twitter.com/6PsA1Z7BNn]— 🔶Cursed Ngon🔶 (@Olninyo)

[May 25, 2017]

While it is possible to do this using a custom made texture, this requires to author a snow texture for each asset. A better solution is to use the **surface normal** of each face. 3D models are made out of triangles, each having a **front face**, which is the side they are looking at. The surface normal is a vector that indicates, for each face, its direction. We can take the direction snow comes from (usually from above) and comparing it with the surface normal of each face. This is usually done using an operator called the **dot product**, which returns a number in the range ![Rendered by QuickLaTeX.com \left[-1,+1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ae9ff7abb09a3e5a1f27ed8b3ef28b87_l3.png)

[Physically Based Rendering and Lighting Models](https://www.alanzucconi.com/2015/06/24/physically-based-rendering/) is a good starting point.

Once we know how aligned the surface normal is compared to the snow direction, we can simply use a threshold to decide whether to colour the surface white or not.

While this technique is very effective, it is also true that you cannot simply expect a shader to make all the work for you. Transitioning from Winter to Spring is not just about changing assets to white. If you need high-quality models and textures you can rely on, I suggest having a look at [Dynamic Nature – Starter](https://www.assetstore.unity3d.com/#!/content/79388?aid=1100l45Ay&pubref=az_sss_06), which comes with hundreds of custom-made rocks, trees, grasses and materials.

###### Snow Accumulation

Snow does not only change the colour of an object. Its accumulation piles up and changes the overall geometry, making snowy surfaces look bulkier. It is possible to simulate this effect using a technique called **vertex displacement**, which has been featured in virtually every instalment of *Shader Showcase Saturday* so far. If you want to learn more about it, you should have a look at [Surface Shading in Unity](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/).

As always, [MinionsArt](https://twitter.com/minionsart) has an amazing tutorial on how to use vertex displacement to simulate the accumulation of snow on exposed surfaces.

❄️Adding a layer of snow to models ❄️

[#gamedev][#indiedev][#unity3d]

Shader code in first replyMore stuff >>

[https://t.co/FqAsMb9Plg][pic.twitter.com/whnZ2DN66k]— Joyce(MinionsArt) (@minionsart)

[December 18, 2017]

If you have a project that is already set up, changing all of your materials can be a pain. [Global Snow](https://www.assetstore.unity3d.com/#!/content/79795?aid=1100l45Ay&pubref=az_sss_06) uses a completely different approach which works in screen space, exactly like a post-processing effect. If you have a big scene, this might be your best bet at adding snow in just a few clicks without having to change all of your existing assets.

Fom the Asset Store…

## Leave a Reply Cancel reply