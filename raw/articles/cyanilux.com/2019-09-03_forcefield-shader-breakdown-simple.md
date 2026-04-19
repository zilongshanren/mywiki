---
title: Forcefield Shader Breakdown (Simple)
url: https://www.cyanilux.com/tutorials/forcefield-shader-breakdown-simple/
author: Cyanilux
published: '2019-09-03'
source_blog: Cyanilux Shader Tutorials
source_site: https://www.cyanilux.com/
category: graphics
fetched: '2026-04-19'
---

# Forcefield Shader Breakdown (Simple)

## Intro

This shader uses a rim / fresnel and the camera’s depth texture to produce a simple forcefield (or energy shield) that has glowing edges and intersections with objects in the scene. We could also add scrolling textures to make the glow and sides of the forcefield more interesting although we won’t be going through that in this post.

## Notes

- This is an
**Unlit**shader.**Transparent**surface mode and**Alpha**blending. - For a more advanced forcefield effect, with distortion and rippling effects, see the
[Forcefield Shader Breakdown](https://www.cyanilux.com/tutorials/forcefield-shader-breakdown).

## Breakdown

We’ll first create a **Color** node and put it into the **Color** input on the **Master** node. Set it to **HDR** mode and use a blue colour with an **Intensity** of **2**. Having a more intense colour will allow us to also use Post Processing effects such as Bloom in order to make the forcefield glow more. Note that bloom can be quite expensive though, especially if targetting mobile platforms.

We also need to click the small cog on our **Master** node and set the shader to use **Transparent** rendering, **Alpha** blending and enable **Two Sided**.

Next, create a **Fresnel Effect** node. This will output a value based on the normal and view direction. This produces what looks like a “glow” around the edge of the object. We can increase the **Power** input to make this glow closer to the edges – I’m using a value of **8**. For more info about this node see the [Fresnel Effect node docs page](https://docs.unity3d.com/Packages/com.unity.shadergraph@17.4/manual/Fresnel-Effect-Node.html).

We’ll be using this as the **Alpha** input on the **Master** node, to have areas on the edges of our object appear, but have areas in the middle (where the Fresnel returns 0) to be transparent. However, for our back faces this node will output 1 as the normals of those vertices are facing away from the view direction. To prevent this, we can first put the **Fresnel Effect** output into the **True** input on a **Branch** node, with the **Predicate** set to the **Is Front Face** node. We can then leave the **False** input as **0**, so we are only using the fresnel result for the front faces.

We’ll take the output of the **Branch** node and **Multiply** it by **2** and then put it into an **Add** node with a value of **0.02**. This allows us to tint the forcefield alpha, so it is slightly less transparent.

We next need to handle the intersection effect with scene objects. To do this, we’ll create a **Screen Position** node with the mode set to **Raw** and put it into a **Split**. This gives us the **depth** of the pixel/fragment on the surface of the object in the **W/A** component.

We can then create a **Scene Depth** node set to the **Eye** sampling mode, put it into the first input on a **Subtract** node, and take the **W/A** component from the **Split** and put it into the second input. By subtracting these two things, we obtain the difference in depth between the scene and object. We can then put this into a **Saturate** node to clamp it between 0 and 1, then put it into a **One Minus** node. We can then put this into a **Power** node with a value of **15**, **Add** it to our previous alpha value and then put it into the **Alpha** input on the **Master** node.

## Thanks for reading! 😊

If you find this post helpful, please consider sharing it with others / on socials

Donations are also **greatly** appreciated! 🙏✨

(Keeps this site free from ads and allows me to focus more on tutorials)