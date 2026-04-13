---
title: Passing Particle System Data into Shadergraph (Custom Vertex Streams)
url: https://cyangamedev.wordpress.com/2020/07/19/custom-vertex-streams/
author: Cyan
published: '2020-07-19'
source_blog: Cyan
source_site: https://cyangamedev.wordpress.com
category: game programming
fetched: '2026-04-13'
---

## Intro

This post provides information on how to use the **Custom Vertex Streams** option on the **Particle System** component (also called Shuriken) to pass per-particle data into the shader. Note that it won’t go over how to use the component itself but there are plenty of tutorials online – [here’s one](https://www.raywenderlich.com/138-introduction-to-unity-particle-systems) that looks well written. In order to use a custom shader on a Particle System component you need to assign a **Material** in the **Renderer** module.

I’m working in the **Universal Render Pipeline** (URP) but the same concept should work for other pipelines too.

You may also want to look into the [Visual Effect Graph](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@8.2/manual/index.html). It can handle much more particles as it runs on the **GPU** rather than the **CPU**, but it is more complicated to set up and I think is currently only in preview for URP. I haven’t used it all that much but I believe you can pass data from the Visual Effect Graph into Shader Graph by using the **Visual Effect Master** node and setting up **exposed** **properties** in the shadergraph blackboard. However in order to use the shader in the VFX Graph, you may need to enable “Experimental Operators/Blocks” under **Edit → Preferences**, then a **Shader Graph** option on the **Output Particle Quad/Triangle/Mesh** block should appear. When set, the exposed properties should also be listed so you can control the inputs.

The rest of this tutorial isn’t related to that though and focuses on the Shuriken Particle System instead, just thought I’d mention it anyway.

## Particle Colour

The particle system component controls the colour of a particle by using the **vertex colour** (a colour value assigned to each vertex). This is the final colour result from the **Start Color**, combined with **Color over Lifetime** and **Color by Speed** modules if they are enabled on the Particle System.

In our shader we can use the **COLOR** semantic in the vertex shader inputs to obtain this vertex colour, and pass it through to the fragment shader. In shadergraph this is handled for us, we just need to use the **Vertex Color** node.

Inside the graph, we would also need to **Split** and put the **A** output into the **Alpha** on the **Master** node if we wanted the alpha of the vertex colour to control the transparency of the particle. We should also set the graph **Surface** mode to **Transparent** (by clicking the small cog on the **Master** node). The below graph is an example of this, which tints a texture with the colour.

## Custom Vertex Streams

As well as colour, it can be useful to pass extra data from the particle system component into the shader. This can be handled using the **Custom Vertex Streams** option under the **Renderer** module on the Particle System component.

![](../../assets/6ce0f0a2dc711ad1.png)

For this example I’m adding the **Lifetime → AgePercent** and **Random → Stable.x** options.

**AgePercent**allows us to obtain the**lifetime**of the particle in a**normalised 0-1 range**(**0**being just emitted and**1**at the end of its lifetime)**StableRandom.x**obtains a random value between**0**and**1**that the particle system generates for each particle, (that doesn’t change per frame like the**VaryingRandom**option does).

When adding these to the **Custom Vertex Streams** list, they are attached to one of the **TEXCOORD** shader inputs (known as **UV** channels in shadergraph). **TEXCOORD0.xy** is already used by the **UV** input for the particle texture, but each channel can include up to **4** values, **x, y, z and w**. The **AgePercent** and **StableRandom.x** values are single floats, so are added to the unused **z** and **w** components of the **TEXCOORD0** channel, based on whichever order they appear in the list.

If we wanted two **StableRandom** values (**.xy**), it would continue to the next channel (so would be **TEXCOORD0.w** and **TEXCOORD1.x**). In this case, it may be better to reorder them so that **StableRandom.xy** uses **TEXCOORD0.zw** and **AgePercent** used **TEXCOORD1.x** so the values are slightly more organised. For this example we’ll just need a single random value though.

Note that an error/warning might appear stating the “*Vertex Streams do not match the shader inputs*”. As this suggests, the shader inputs should match the values in this list. For example this warning might show if the **COLOR** is included in the list while the shader doesn’t use the **COLOR** semantic for the vertex input struct (or **Vertex Color** node in terms of shadergraph).

Here’s some images to show how the **AgePercent** and **StableRandom.x** values look when output as colour (while still applying a texture so they aren’t just quads), and the final result of the shader effect I’m using for this example.

![](../../assets/8d0a6aa89e0398be.png)

![](../../assets/304f75467cb4702b.png)

![](../../assets/fd8b542966323db8.png)

Now that we’ve set up the **Custom Vertex Streams** we can look at the shader graph to produce this effect.

For this example I’m using the **StableRandom.x** value as input to a **Flipbook** node to select a random tile from a [texture](https://cyangamedev.wordpress.com/wp-content/uploads/2020/07/smoke.png) that contains multiple cloud/smoke shapes to add variation into the particles. It’s also used to slightly affect the particle colour by putting it into a **Lerp** to remap the **0-1** range to **0.9** to **1.1** and multiplying it by the **Vertex Color**.

The **AgePercent** value is used to **Step** against the texture result to create a dissolve-like shader effect. The **Preview** nodes in the graph aren’t required, but I’m using them with a group to name the values so it’s clearer. Also note that while the **Split** is labelled RGBA, it’s the same as XYZW.

With a few adjustments to the settings on the Particle System component, mainly **Color over Lifetime**,** Size over Lifetime **and **Rotation over Lifetime**, this produces the result as shown before, also animated in this twitter gif here :

We could have instead applied the colour variation by setting the particle system’s **Start Color** to be **Random Between Two Colors** instead, as well as use the **Color over Lifetime** module’s **alpha** to control the dissolve amount, rather than the **AgePercent** input. I think the texture tiles can also be achieved through the **Texture Sheet Animation** module on the particle system too, but I wanted to use the **Custom Vertex Streams** more to demonstrate how it works. Also note the shadergraph above also ignores the **Vertex Color** alpha entirely as I didn’t want partially transparent particles.

## Custom Data

Another useful option is the **Custom Data **module on the Particle System. This provides two slots to set some extra data which can be passed into the shader using the **Custom1** and **Custom2** options on the **Custom Vertex Streams** list. The **Custom Data** can be set to either a **Color** or **Vector**.

![](../../assets/686758518f8db998.png)

If Color is chosen, it has a dropdown next to the colour to switch between:

**Color**: A single colour is used and stays constant**Gradient**: The colour goes through the gradient over the lifetime of each particle**Random Between Two Colors**: The resulting colour is chosen as a random linear interpolation between the two given colours**Random Between Two Gradients**: The resulting colour is a random linear interpolation between the two colours given by each gradient over the lifetime of each particle

When using **Color**, you should also make sure to use the **Custom1.xyzw** (or **Custom2.xyzw** for the second slot), to ensure all components of the colour are passed into the shader. It’s also worth noting that unlike the colours/gradients used by the rest of the particle system, the **Custom Data** ones can be **HDR**, so have an **Intensity** to have colours brighter than **(1, 1, 1)**, which can be useful when using **Bloom** post processing.

If **Vector** is chosen, you can control the number of components needed (up to the maximum of **4**, or **8** if both **Custom Data** slots are used). For each component, there is a dropdown to switch between :

• **Constant** : A value which stays constant

• **Curve** : The value goes through the curve over the lifetime of each particle

• **Random Between Two Constants** : The resulting value is chosen as a random linear interpolation between the two given values

• **Random Between Two Curves** : The resulting value is a random linear interpolation between the two values given by each curve over the lifetime of each particle

The **Vector** option as a **Curve** is particularly useful if you want a value to change over the lifetime, similar to what we did in the previous dissolve example – but a curve allows more control over how it dissolves rather than just the **AgePercent** and **Lerp** combo in the graph.

Thanks for reading, hope this is useful!