---
title: Stealth Vision in Unity URP
url: https://danielilett.com/2023-04-07-tut6-4-stealth-vision/
author: Daniel Ilett
published: '2023-04-07'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

One of the core gameplay hallmarks of modern stealth games is the mechanic whereby you can ‘tag’ enemies or other objects and then see them through walls - you could call it “x-ray vision” or “stealth game vision”. You could implement the effect in many ways, and in this tutorial, I’ll show you one approach that works in Universal Render Pipeline. We’ll be using Renderer Features to do this.

For this tutorial, we are using Unity 2021.3.0f1 (LTS) and URP 12.1.6.

![Lava Lamp Shader. An X-ray shader effect which features swirls and some animation.](../../assets/c7fab416d2f6f35b.png)


# Renderer Features

With Renderer Features in URP, we can force objects in specific layers to render on top of everything else if they are positioned behind a wall. First, let’s set up a layer and add at least one object to it to test the effect. For this example, I’ll use a character mesh. Click on any object and go to *Layer -> Add Layer* at the top of the Inspector, then create a new layer named “RenderOnTop” (or whatever you want) and assign all your tagged objects to this layer. In a real game, you would need to build a gameplay system that lets you add or remove tags from objects or enemies, but I’ll focus only on the shader part in this article.

Next, find your project’s URP Renderer asset, which can be found in the Settings folder in a brand-new URP project. Before we can deal with X-ray vision, we must first disable the normal rendering of all objects in the `RenderOnTop`

layer, which we can do by deselecting that layer from the *Opaque Layer Mask* and *Transparent Layer Mask* dropdown settings. Once you do that, the objects in those layers should pop out of existence.

![URP Renderer Asset. The URP Renderer asset lets us customize rendering.](../../assets/e12eff9654c975e7.png)


Now we will add back rendering the objects when they are behind walls. On your URP Renderer, at the bottom, go to *Add Renderer Feature -> Render Objects*, which is a special Renderer Feature provided by Unity that lets us override certain aspects of the core rendering loop. Name it “Highlight Opaque” and set the *Event* to *AfterRenderingOpaques*. In the Filters dropdown, the *Queue* should be *Opaque* and the *Layer Mask* should contain only the `RenderOnTop`

layer. Essentially, these settings mean that Unity will try to draw all the opaque geometry in the `RenderOnTop`

layer after all other opaque objects have been drawn - but that’s just *when* it will draw them, not *how* it will draw them.

In the *Overrides* dropdown, we’ll add some crucial behavior. First, drag a test material into the Material slot (I’m using an unlit white material for now), then in *Depth* (which you should tick), we’ll modify the depth test. We want to render only if the depth of a `RenderOnTop`

object is greater than the depth of any existing opaque object, so change the *Depth Test* to *Greater* and make sure that *Write Depth* is left unticked.

![Highlight Opaque. This Renderer Feature will highlight objects behind walls.](../../assets/d97303d4a4c2153a.png)


Once you’ve done that, you’ll be able to see your objects again, but only if they are behind a wall.

![X-ray Rendering. The object is only visible when it is behind a wall.](../../assets/2082a0564ae26ab6.png)


Now we’ll add back normal rendering of the layer whenever objects are not behind a wall. Add a second Render Objects feature and name it “Normal Opaque”, then give it the same *Event*, *Queue*, and *Layer Mask* settings as the first feature. This time, in *Overrides*, leave the material as blank because we don’t want to replace the objects’ regular material, and set the *Depth Test* to *Less Equal*. We should also write the depth value so tick that too.

![Normal Opaque. This feature will add back normal object rendering.](../../assets/76663b141e1a906a.png)


Now, we can view objects normally when they are not hidden behind a wall, but the moment parts of the object are obscured, we’ll see the unlit white material.

![X-ray and Normal. Both normal rendering and X-ray rendering is completed.](../../assets/f4b59710e711bcc1.png)


If you plan to use transparent objects in the `RenderOnTop`

layer, then we’ll need to add two more Render Objects features; duplicate the existing two but change the *Event* to *AfterRenderingTransparents* and swap the *Queue* to *Transparent*. You might also want to rename them “Highlight Transparent” and “Normal Transparent” respectively.

The basic effect is complete, but I also want to bundle in a couple of shaders to use for the X-rayed objects because unlit white is a bit uninspiring!

# X-ray Material

This shader is a fairly static shader that helps to highlight the edges of the object. That way, it’s more stylistic than a basic color, but it still helps you to establish the silhouette of the object. Right-click the Project View and select *Create -> Shader -> Universal Render Pipeline -> Lit Shader Graph*, and name it “Stealth Vision”. Both the shaders we will create should be transparent, so go to the Graph Settings and change the *Surface* to *Transparent*.

This shader is straightforward - all I want to do is add an emissive Fresnel effect to the object. Start by adding a `Base Color`

property and make sure it is HDR-enabled, then add a `Fresnel Power`

`Float`

property too - this will control the thickness of the outlines. Drag the `Fresnel Power`

property onto the graph and use it as the input to a `Fresnel Effect`

node, then multiply it together with the `Base Color`

property. Output the result to the *Emission* node of the master stack, then use a `Split`

node to connect the alpha component to the *Alpha* output block. The shader is now complete!

![X-ray Shader Graph. The X-ray Shader Graph is relatively straightforward.](../../assets/44f0a02b2349e55b.png)


We can see it in action by choosing a high-intensity red color on a material using this shader, then dragging it onto the material override on the Renderer Features in place of the unlit white material we were previously using. This material works best on organic objects with some curves, as Fresnel is only apparent on flat surfaces viewed at certain angles.

![X-ray Shader. An X-ray shader effect which uses Fresnel to form an object silhouette.](../../assets/ac1e0fee2e45eae1.png)


# Lava Lamp Material

This second shader is a little more complicated and features some animation. Like the first shader, it is also transparent. It uses a similar HDR-enabled `Base Color`

property, as well as a `Float`

property called `Speed`

to control the animation - give it a default value of 0.25. Later, we will also incorporate two more `Float`

properties called `Noise Scale`

and `Thickness`

.

First, drag the `Speed`

property onto the graph and multiply it by a `Time`

node. If we `Modulo`

the result by 1, then it will count to 1 and then loop back to 0 before ticking up again continually. Next, I’ll be using a noise cloud to define the pattern this effect uses. Add a `Simple Noise`

node with the `Noise Scale`

property in its *Scale* pin, then output the result to the *In* pin of two `Step`

nodes. Here, we will provide two thresholds.

![Modulo Clock. These nodes form a modulo clock and provide a noise cloud pattern.](../../assets/75c3e7b2384f11f6.png)


For the first `Step`

node, pass the modulo clock we just made into its *Edge* pin. Then, for the second `Step`

node, add the `Thickness`

property to the modulo clock and use that for the *Edge* pin. Now we have two thresholds, and one uses a higher value than the other. If we take the second `Step`

and use `One Minus`

on the output, then multiply it with the first `Step`

node, we have essentially found all values that fall within both thresholds. In our case, this is a thin slice of noise values. We can output this value to the *Alpha* output block, then multiply by the `Base Color`

property and output the result to the *Base Color* output block.

![Multiple Thresholds. Two thresholds can be used to find a thin band of noise values.](../../assets/14f1b128f94c6a53.png)


You can leave things there, or for a slightly more interesting pattern, go back to the start of the graph and use a `Position`

node in world space as the input to a `Polar Coordinates`

node, then use the result for the UV slot of the `Simple Noise`

node.

![Polar Coordinates. Polar coordinates give us swirling patterns in the output.](../../assets/6b0e70ad8b446b2c.png)


That should give you more curvy patterns.

![Lava Lamp Shader. An X-ray shader effect which features swirls and some animation.](../../assets/c7fab416d2f6f35b.png)


# Conclusion

The Render Objects feature makes it rather easy to override rendering settings. Conventionally, you would have to write different depth settings directly into your shaders and then attach two materials to your objects, but we managed to avoid that here with Render Objects. The biggest advantage here is that we can swap out the material of every object to an X-ray material, no matter what material those objects started with, although it’s a shame that Unity has a hard limit on the total number of layers, which might be a problem in some projects (especially as the layers are shared by the physics system, which is a bizarre design choice). I also used Render Objects for [my Impossible Geometry tutorial](https://danielilett.com/2022-01-05-tut5-22-impossible-geom-stencils/) if you’re in the mood for more!

Subscribe to my Patreon for perks including early access, your name in the credits of my videos, and bonus access to several premium shader packs!