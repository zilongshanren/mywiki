---
title: 'Shader Showcase Saturday #11: Return of the Obra Dinn - Alan Zucconi'
url: https://www.alanzucconi.com/2018/10/24/shader-showcase-saturday-11/
author: Alan Zucconi
published: '2018-10-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Most indie developers might know [Lucas Pope](https://twitter.com/dukope) as the developers of the critically acclaimed [Papers, Please](https://store.steampowered.com/app/239030/Papers_Please/). Thanks to its simple, yet thoughtful mechanics, *Papers, Please* helped to shape an entirely new genre of video games. And it even inspired a short film with the same name.

Despite its success, one of the most recurring criticisms the game has faced is related to the apparent simplicity of its execution. With *Return of the Obra Dinn*, Lucas Pope clears any doubt with a game that, by itself, is nothing less than an achievement in technical excellence.


Most of the content from this week’s *Shader Showcase Saturday* comes directly from the [Return of the Obra Dinn [DevLog]](https://forums.tigsource.com/index.php?topic=40832.0), which Lucas Pope himself started back in 2014. The aesthetics of the game heavily relies on an effect called **dithering**, which allows representing greyscale images with only two colours: black and white.

If you are only interested in a quick way to add dithering to your game, I would suggest trying [Stylizer – Basic](https://assetstore.unity.com/packages/vfx/shaders/fullscreen-camera-effects/stylizer-basic-93677?aid=1100l45Ay&pubref=az_sss_11). The asset comes with several other effects available, all designed to add a retro vibe to your scenes.

If you want to learn more, keep reading.

## Anatomy of the Obra Dinn

The style of *Return of the Obra Dinn* is achieved with three separate techniques. The most obvious one is the **dithering effect** that renders the game with dots. Lucas Pope developed his own variant, which he referred to as **blue noise dithering**.

A significant amount of work was put into making sure that the dithering effect had temporal consistency between frames. This was achieved by remapping the dithering effect on a sphere.

Lastly, *Return of the Obra Dinn* features very crisp lines. That is done thanks to an **edge detection post-processing effect**, which will not be discussed today. This blog will soon dedicate an entire tutorial on the topic, inspired by the exceptional aesthetics of [Sable](https://store.steampowered.com/app/757310/Sable/), which is based on a similar technique.

## Dithering

Dithering has been very pioneered by the printing industry, which traditionally used black ink on white paper. The most simple technique to render images in black and white is to use a **threshold**, so that all pixels darker than a certain value are coloured black. As seen in the image below, thresholding yields very poor results:

![](../../assets/e4dc056380bf697e.png)


The introduction of dithering arose as an attempt to solve that problem, creating the illusion of a gradient by alternating black and white dots with different densities.

Since dithering was first used, there have been countless implementations, each one with its specific advantages and limitations. The most used technique nowadays is the **Floyd-Steinberg dithering**, firstly introduced by Robert W. Floyd and Louis Steinberg in 1976. You can see how well it performs below.

![](../../assets/3c22dfed3f97daef.png)


Dithering, however, has two main problems. The first one is that is a *non-local effect*. This means that, conversely to thresholding, it cannot be executed on a per-pixel basis. The Floyd-Steinberg dithering requires to propagate the computation to nearby pixels; a process that is notoriously tricky to do via shaders.

If you need more control over your effects, you can try the extended version of [Stylizer – Basic](https://assetstore.unity.com/packages/vfx/shaders/fullscreen-camera-effects/stylizer-basic-93677?aid=1100l45Ay&pubref=az_sss_11), unsurprisingly called [Stylizer – Extended](https://assetstore.unity.com/packages/vfx/shaders/fullscreen-camera-effects/stylizer-extended-92269?aid=1100l45Ay&pubref=az_sss_11).

### Lookup Texture

A cheaper solution is to use a *lookup texture*, which can be sampled in *world-space* based on an object *reflectance *(often indicated as **NdotL**). The result can be pretty effective, although is prone to inaccuracies. [Ciro Continisio](https://twitter.com/cirocontns/) has implemented this technique in ShaderGraph (below) to simulate a hatching effect.

Another shader experiment in ShaderGraph. I like this one, it's taking shape! Still loads to do, but I like the direction.

[pic.twitter.com/ZtmnkTjFtB]— Ciro Continisio (@CiroContns)

[August 18, 2018]

It is also possible to sample the texture in *UV space*, which the hatching follows the curvature of the 3D models. The technique is discussed in [Real-Time Hatching](http://hhoppe.com/hatching.pdf), where Emil Praun and his colleagues relied on mip-mapped lookup textures which they referred to as **tonal art map** (below).

![](../../assets/7ddb3148592b1d1f.png)


Technical Artist [Kyle Halladay](https://twitter.com/khalladay) wrote an interesting tutorial on that very paper, titled [A Pencil Sketch Effect](http://kylehalladay.com/blog/tutorial/2017/02/21/Pencil-Sketch-Effect.html), later improved by [Ben Golus](https://twitter.com/bgolus/status/834822859583320064).

### Ordered Dithering

A more advanced technique to perform real dithering requires a post-processing effect. **Ordered dithering** decides if a pixel should be black or white by analysing its local neighbourhood. Such an operation requires to sample the texture several times, but is highly parallelisable and works relatively well in a shader. A specific implementation of ordered dithering uses a matrix to governs how nearby pixels should be taken into account, often referred to as **Bayer matrix**.

A variant of this technique has been used in *Return of the Obra Dinn*. As explained in his [devlog](https://forums.tigsource.com/index.php?topic=40832.msg1045205#msg1045205), the game initially adopted Bayer dithering. Lucas Pope later developed its own variant (referred to as **blue noise dithering**) because it survived much better to both screen scaling and video compression.

Trying a new dither matrix. Blue noise instead of Bayer. Devlog:

[http://t.co/3RAS9ri9xR][#screenshotsaturday][pic.twitter.com/hSyoG5utFP]— Lucas Pope (@dukope)

[July 25, 2014]

## Temporal Dithering

One massive problem with ordered dithering is that each frame is calculated independently from the previous one. This lack of **temporal correlation** causes the dither pattern to move erratically. This has a negative impact not only on the video compression, but also on the overall playability.

Lucas Pope attempted overcoming these challenges by mapping the dithering effect on a sphere.

Reducing 1-bit dot flicker via sphere-mapped dither pattern:

[https://t.co/rcxdgLBrLU][pic.twitter.com/LoDoEuxneU]— Lucas Pope (@dukope)

[November 23, 2017]

Lucas Pope wrote an exceptionally detailed devlog entry on how such a technique works, and on all of his earlier attempts. If you are interested, I would strongly advise to read it.


If you are struggling to replicate those effects, you can try using one of the many professional assets that are available on the Asset Store. Another great package for dithering is [Graphics Adapter Pro](https://assetstore.unity.com/packages/vfx/shaders/fullscreen-camera-effects/graphics-adapter-pro-55981?aid=1100l45Ay&pubref=az_sss_11), which offers a variety of post-processing effects to emulates retro videocards.

## Leave a Reply Cancel reply