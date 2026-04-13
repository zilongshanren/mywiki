---
title: 'Shader Showcase Saturday #5: Dripping Rain - Alan Zucconi'
url: https://www.alanzucconi.com/2018/08/10/shader-showcase-saturday-5/
author: Alan Zucconi
published: '2018-08-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

The first time I played *Diablo 2* I remember how impressed I was to see rain causing ripples on the river just behind the Rogue Encampment. But only when I looked closer I realised that those ripples were not *actually* caused by any raindrop. Both ripples and raindrops were simply unrelated. As it often happens, improving graphics in modern computer games is not a quest for **realism**: it’s all about **believability**.

When it comes to 2D games, creating ripples in water is relatively easy, as that is often done with particles. But for 3D objects, things are a little bit more complicated. Since meshes can be curved, is hard to have particles following those shapes correctly. Technically speaking, such an effect could be perfectly simulated with physics, but as we have seen already, **fluid simulations** are expensive and hard to control.

This is why most games in which you see water slowly dripping on a 3D surface often rely on **shaders**.

If this is your first time approaching shaders, I highly encourage you to read [A Gentle Introduction to Shaders](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/), which will get you started.


VFX Artist [Klemen Lozar](https://twitter.com/klemen_lozar) has created a photorealistic **raindrop shader** (below) in Unreal Engine 4, which features three main effects. The first one is the presence of tiny droplets which can be seen at all time on the material. The second is the sudden appearance of short-lived droplets that simulates incoming raindrops. Finally, rain streaks are dripping downwards, following the model’s geometry.

Raindrop shader. Three layers, two dynamic, one static. Packed tiling textures with normals and opacity mask. More detailed breakdown on the way, look for replies to this thread!

[#UE4][#gamedev][#indiedev][pic.twitter.com/xmVSpsefXq]— Klemen (@klemen_lozar)

[January 17, 2018]

Klemen has explained how these effects were achieved in a follow-up thread (below), where he also provided a nice animation. A rain streak pattern is encoded in a texture which is then applied on top of the material. By offsetting the Y coordinate of the texture over time, it is possible to simulate a downward movement. This is a very common technique which is called **UV offset**, since the X and Y coordinates of a texture in a shader are referred to as U and V. By using a **noise texture**, the UV coordinates of the rain streaks texture are distorted to give the illusion that drops are moving erratically. There are several tutorials on this blog that will teach you how many different effects can be implemented by simply playing with the UV coordinates. If you are interested, [LCD Shader Effect](https://www.alanzucconi.com/?p=4707) might be a good starting point.

The appearing drops are done with a different technique. Klemen relies on a grid texture in which the colour of each square is used to decide the “arrival time” of the raindrop.

Streaks on top, a tiling tex, distortion is animated so you can see the influence of the distortion tex on the left. Drops on the bottom, I use a very small but uncompressed tex that holds different UV values per pixel, this is used to distribute another tex around.

[#UE4][#gamedev][pic.twitter.com/JSEarXxtNI]— Klemen (@klemen_lozar)

[January 17, 2018]

The above-mentioned effect is perfect for objects with complex geometries. However, it can be tricky to use on flat surfaces. This is because heavy rain is not simply drawn onto a 3D model. [Realistic Rain Storm](https://www.assetstore.unity3d.com/#!/content/46192?aid=1100l45Ay&pubref=az_sss_05) is the perfect asset for photorealistic rain, as it uses particles to simulate not just the ripples caused by raindrops, but also their ground splashes. This gives a new dimension to a rainy landscape, and it works perfectly for VR. That is because most flat effects that look perfect on a screen can appear unnatural in VR, since they lack depth.

A big step forward has been made by [Taizyd Korambayil](https://twitter.com/DeepSpaceBanana/), who crafted a shader which simulates rain streaks based on the inclination of a model. In the video below you can see how the same shader blends between raindrops and rain streaks on the fly, with exceptionally believable results.

Slope Aware Rainy Surface Material Function in

[#UE4]. Easily to layer on top of any existing surface materials[#gameart][#shader][#gamedev][pic.twitter.com/QFg5zNT6aG]— Taizyd Korambayil (@DeepSpaceBanana)

[June 9, 2017]

Taizyd wrote two articles which describe how to recreate his effect. In the tutorial titled [Rainy Surface Shader – Part 1](https://deepspacebanana.github.io/deepspacebanana.github.io/blog/shader/art/unreal%20engine/Rainy-Surface-Shader-Part-1), he explains how to recreate the ripple effect that appears on horizontal surfaces. He uses a similar, yet different approach from Klemen. I highly encourage you to look at both versions, as there is a lot to learn on how to master the art of shaders. The most interesting bits are in [Rainy Surface Shader – Part 2](https://deepspacebanana.github.io/blog/shader/art/unreal%20engine/Rainy-Surface-Shader-Part-2) where Taizyd explains how he achieved the “slope awareness” seen in his video. He simply blends between the horizontal raindrop effects and the vertical rain streaks, based on the inclination of the mesh surface. To be more technical, the strength of both effects is modulated by the **surface normal** of the face being rendered, expressed **world space**. This means that the concept of “horizontal” and “vertical” depends on the inclination of the objects in the world.

A similar technique is often used to procedurally textures on complex landscapes. It is called **triplanar shading**, since it usually blends three textures, based on the alignment of the surface normal to the X, Y or Z axis. [MinionsArt](https://twitter.com/minionsart) made an amazing animation that shows how this effect works.

The basics of a UV-Free TriPlanar shader for terrain, with a grassy top layer 🙂

[#gamedev][#indiedev][#tutorial]

Shader Code Sample in first reply

More stuff >[https://t.co/FqAsMb9Plg][pic.twitter.com/Yb5rpkFuzx]— Joyce(MinionsArt) (@minionsart)

[January 31, 2018]

If you are looking for a more technical explanation, Tech Artist [Ben Golus](https://twitter.com/bgolus) wrote an article titled [Normal Mapping for a Triplanar Shader](https://medium.com/@bgolus/normal-mapping-for-a-triplanar-shader-10bf39dca05a) which explains how to really master this technique.

The problem with both the rain effects seen so far is that they only apply to a single material. Another great asset that allows avoiding that is [Rain](https://www.assetstore.unity3d.com/#!/content/35156?aid=1100l45Ay&pubref=az_sss_05). The name is simple, but the asset delivers high-quality distortions that are perfect to simulate heavy rains.

Another key aspect to the believable of raindrops is to ensure that they change the look of the materials like real water would do. What this means is actually different based on which material is affected by water. For metal surfaces, this means reducing their **metallic value** close to zero, and increasing the **smoothness** to give a shinier look. However, this is not what happens to fabric, which becomes darker but retains its original roughness and metallicity. Below, you can see a beautiful rendering made by [Sina Mehralinia](https://twitter.com/gryphiz) in Houdini, where the water drops indeed change the physical look of the material below.

Rain shader(wip)


Thanks to[@andrewpprice]for awesome tutorial![@sidefx][#houdini][#shader][#cgi][#3d][pic.twitter.com/NnhNTN86RW]— Sina سینا (@gryphiz)

[January 30, 2016]

One of the best assets that you can use to replicate the look and feel of wet surfaces is [Raindrop Wet Surface](https://www.assetstore.unity3d.com/#!/content/56650?aid=1100l45Ay&pubref=az_sss_05). It is perfect for flat surfaces, both natural and metropolitan. It is perfect to simulate puddles on concrete, tarmac and even bricks. It can also be animated to transit from a dry to wet, and the shape of the puddle can be modelled using an additional texture.

## Leave a Reply Cancel reply