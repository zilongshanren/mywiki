---
title: 'Shader Showcase Saturday #10: Fortnite Procedural Animations - Alan Zucconi'
url: https://www.alanzucconi.com/2018/09/17/shader-showcase-saturday-10/
author: Alan Zucconi
published: '2018-09-17'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

It is no mystery that *Fortnite* has now become one of the most successful computer games of all time. While many see it as a case study for excellence in marketing and game design, the game itself features some very interesting shader effects.

![](../../assets/ffd69b187e5f14c6.gif)


From a Technical Artist perspective, the most striking effect featured in Fortnite is the self-building effect. When an object is being constructed, its individual pieces appear one by one out of thin air, and fly into position. The same effect is somehow played, in reverse, when an object is damaged, by showing those very pieces flying away and disappearing (above).


Most of the information about this effect comes from a GDC talk that Senior Technical Artist [Jonathan Lindquist](https://twitter.com/techartjon) gave at GDC 2013, titled “[The Inner Workings of Fortnite’s Shader-Based Procedural Animations](https://www.youtube.com/watch?v=7Fl3so0Z5Tc)“. The talk itself is non-technical and can be followed by anyone with a basic understanding of 3D modelling and shader coding. The animations shown in this article comes from that presentation.

However, if you are interested just in understanding how this effect works, this is the article you have been looking forward.

Animations like the ones seen in Fornite could be potentially created by an artist, whose task is to animate every single piece of a mesh by hand. Such a process is costly, not only in terms of working hours required, but also to run on a machine. Attaching complex animations to each piece of the world might be computationally unfeasible for a game as large as Fortnite, where keeping a smooth framerate is essential.

For these reasons, all construction and destruction animations are done procedurally, using a **vertex shader**. This website has dozens of articles and online courses dedicated to vertex shaders and vertex animations, since they are one of the most efficient and versatile tools available to Technical Artists. If you are unfamiliar with the technique, [A Gentle Introduction To Shaders](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/) is a good starting point. Vertex animations have also been featured in three previous instalments of *Shader Showcase Saturday*: [Interactive Grass](https://www.alanzucconi.com/?p=9545) (SSS#3), [Fire With Shaders](https://www.alanzucconi.com/?p=9637) (SSS#4) and [Dynamic Snow](https://www.alanzucconi.com/?p=9755) (SSS# 6).

In a nutshell, vertex shaders process each vertex in a mesh, and are able to change its coordinates. This allows for simple, yet very efficient, 3D manipulations. Translating, rotating and scaling can be done efficiently in a vertex shader, hence why so many developers are relying on them for the most diverse effects.

## Toon Shading

Before venturing any further into the mechanics of vertex shading, it is important to notice that *Fornite* uses a custom **lighting model** to give a slightly cartoony finish to all of his characters. While that exact lighting model will be discussed in a future instalment, you can rely on a technique called **Cel shading** (sometimes referred to as **Toon shading** instead) to get you started. One of the most reliable assets for this is [Toony Colors Pro 2](https://assetstore.unity.com/packages/vfx/shaders/toony-colors-pro-2-8105?aid=1100l45Ay&pubref=az_sss_10), which allows for many variations and customisations.

Compared to most Cel shaders, [Toony Colors Pro 2](https://assetstore.unity.com/packages/vfx/shaders/toony-colors-pro-2-8105?aid=1100l45Ay&pubref=az_sss_10) allows retaining part of the original illumination, resulting in a more vivid rendering (below).

If you need an environment that works well with that style, I would suggest [Fantasy Adventure Environment](https://assetstore.unity.com/packages/3d/environments/fantasy/fantasy-adventure-environment-70354?aid=1100l45Ay&pubref=az_sss_10), one of the finalist assets for the **Unity Awards 2017**.

## From Vertices to Submeshes

In a 3D model, there is the concept of mesh and submeshes. Models can be nested, in the same way GameObject can. However, once the model is processed through a shader, all that information is lost. Vertex shaders only care about vertices, and they have no idea where they came from.

Since this important information is lost, finding which vertex corresponds to which block in a mesh is simply not impossible. To go around this limitation, Jonathan Lindquist explained how his team created a tool to encode such an information in the vertex data itself. Each vertex, in fact, can hold a certain amount of additional data (typucally colours, UVs, normals and tangents). By exploiting these extra fields it was possible to give not only an order to each block, but also to specify its pivot point and preferred axis of rotation.

## Deconstructing the Self-Building Effect

If you are striving to become a Technical Artist, you might already know that every effect (no matter how complicated it looks) can actually be decomposed in many simpler ones. Fornite self-building and destruction effect is no exception.

Jonathan Lindquist explained how the procedural destruction animation has been achieved, by layering eight separate effects on the vertices of the mesh. Each one adds a different movement to the mesh; together, they sum up to produce the final effect.

Let’s analyse each one.

###### 1. Gravity Acceleration

When an element is destructed, the first effect that is applied is gravity. To do this, the vertex shader simply subtracts a certain amount to the Y coordinate of each vertex. This amount is increased in each frame, to simulate the accelerating rate at which gravity is pushing objects towards the ground.

![](../../assets/6cc2afdf45068bac.gif)


###### 2. Flight Direction

When a block is destroyed, it does not only fall downwards. It is actually projected outwards. While there is only one clear *down direction*, the same cannot be said for the outward direction. Jonathan Lindquist explained that a bit was stored in each vertex to indicate whether that specific mesh should fly left or right. With the addition of gravity, this forces the mesh to fall in a parabolic path.

![](../../assets/eba791cfd4fa8748.gif)


###### 3. Radial Velocity

To add an extra bit of realism, the vertex shader adds a vector that is tangent to the flying direction. This radial velocity looks as is the block is being detached and pushed away from a force that originated in the centre of the mesh.

![](../../assets/f68ce5ea23aa4a37.gif)


###### 4. Pivot Rotation

Each block that is currently flying away is being rotated. If you are familiar with vector algebra you should know that rotations require an axis. This means that each block needs to have its own rotation axis, in order for this effect to work correctly. The pivots and rotation axis are stored in the vertex data, so that the shader can access them.

![](../../assets/2e991ae12e9f4abd.gif)


###### 5. Breaking Order

Each block is detached at a different time. This is done by encoding an extra integer number in each vertex. The material that is shared between all the blocks has a timer, which is used to control the flow of the overall animation. The order integer stored in each vertex is used to decide at which time each block should start and stop animating.

![](../../assets/689950c89c5fc68f.gif)


###### 6. Simultaneous Breaks

What we have after point 5, is a material with a timer that can be used to control the destruction animation. Each block is detached at a different time, so that playing the animation destroys a block at a time. Every time the object is hit and a block must be removed, we can simply move the timer forward with an animation. This works well when an object is destroyed piece by piece. But there might be situations in which so much damaged is inflicted that the entire object must be destroyed at once. This effect is achieved by adding another parameter that changes the animation times so that they can overlap. By doing so, we created a clear connection between a gameplay element (the damage) and an aesthetic ones (the destruction animation).

![](../../assets/9e039aca11586133.gif)


###### 7. Warping

One of the nicest effects that is applied to each destructible block is a subtle warping. This effect alone improves the perception that wood planks are subjected to a sheer force. To do this, the borders of a block are animated slightly ahead of the current time. This “bends” the objects, creating the illusion they are warped.

![](../../assets/d2d1aa69550da563.png)


###### 8. Disappearing

Finally, when the single meshes have been fully animated, they disappear. This is done in a fragment shader, by simply fading their overall colour and transparency.


Each one of those eight effects is relatively easy to implement. If you are using Unreal, [UnrealCG](https://twitter.com/unrealcg) made an interesting tutorial on how to recreate these effects. The same technique, however, can be easily applied to Unity as well.

However, if you do not feel comfortable with writing shader code yourself, I highly recommend trying [Amplify Shader Editor](https://www.assetstore.unity3d.com/#!/content/68570?aid=1100l45Ay&pubref=az_sss_10), which is possibly the most advanced tools specifically designed to create shaders in Unity without any code.

[Amplify Shader Editor](https://www.assetstore.unity3d.com/#!/content/68570?aid=1100l45Ay&pubref=az_sss_10) also comes with several examples you can use, and there is plenty of support for **custom lighting models** (below), which are a good starting point to recreate the one used in Fornite.

## Leave a Reply Cancel reply