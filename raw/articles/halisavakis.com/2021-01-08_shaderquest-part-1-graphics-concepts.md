---
title: 'ShaderQuest Part 1: Graphics Concepts'
url: https://halisavakis.com/shaderquest-part-1-graphics-concepts/
published: '2021-01-08'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This ShaderQuest post is brought to you by these awesome Patrons:

- Not Invader Zim
- Tiph’ (DN)
- orels1

## Introduction

Welcome to the first stop on your ShaderQuest! This small post will focus on providing some valuable context in terms of 3D objects and how their elements can be used when developing shaders.

Keep in mind that I won’t be using any game engine or showing anything about shader creation here. Instead, I’ll be using Blender to go through the elements of 3D objects. Any 3D modeling suite provides the same information as Blender.

Let’s get started!

## 3D Objects

First-off, it’s important to actually get a good idea of what 3D models essentially are.

A 3D model in any rendering environment is composed of a bunch of points in space (referred to as **vertices**) that form polygons (also referred to as **faces**). The lines connecting two vertices are commonly referred to as **edges**, and while they are very useful in the context of 3D modeling, they don’t offer a lot of functionality in the realm of the most commonly used shaders.

![](../../assets/f5e23c34f01c76a2.png)

Something to keep in mind is that while in 3D modeling software a face of a model can have an indefinite number of vertices (it can be a **triangle**, a **quad** or a polygon with more than 4 points – commonly referred to as **n-gon**), when imported into a game engine all the faces get reduced to triangles (or **tris**). So, our cube in the context of a game engine will look more like this:

![](../../assets/09d4a26f1844f8a3.png)

## UV Coordinates

If you are even a bit familiar with 3D modeling you should be familiar with **UV coordinates** also referred to as **texture coordinates** or, as I commonly refer to them, simply **UVs**. Since we usually want to apply some visual elements on our 3D models that aren’t just a solid color, in 3D applications like Blender we can generate UV coordinates for our objects in order to map a texture onto them. UV coordinates are basically a projected or unwrapped version of our 3D model into 2D space.

Let’s dive a tiny bit deeper on how UVs actually work. This is how the default cube in Blender is unwrapped:

![](../../assets/43b6175113f1356e.png)

If you’re into 3D art you might be used to how the unwrapping works and what its effects are on the model, but in the context of technical art it’s important to also see the UVs for what they are: a coordinate system.

![](../../assets/fba2372be239cf48.png)

The grid shown in Blender is in fact a 2D space that spans from (0,0) to (1,1). It has two axes – **X **and **Y** (or **U **and **V** respectively) and that same coordinate system is applied on any texture you’re sampling to apply it to your object.

Applying an image texture to this object looks like this in relation to our UVs:

![](../../assets/267304275fd7f07a.png)

Regardless of whether our texture has an aspect ratio of 1:1, it gets mapped to our entire UV space, and the unwrapped faces of our object output the segment of the texture that corresponds to the space they take in the UV domain.

If we wanted each face of the cube to present the whole texture, then each face would have to take up all the space in the UV coordinates:

![](../../assets/99f7b9b77a64e14c.png)

We’ll be using UV coordinates a lot in the context of shaders, not just for regular texture sampling (like Blender here is doing) but for other uses as well. **Having some model-bound data is always useful for custom effects**.

## Normal vectors

An equally common and useful element of 3D objects is the set of its **normal vectors** or, simply, **normals**.

A normal vector is something very simple in its concept: it’s a vector that’s perpendicular to a surface. It’s basically telling us which way a face is facing.

![](../../assets/e80dd50bca5b70bf.png)

Normal vectors are used for a plethora of shader effects but the two biggies that are usually in any rendering engine by default are: **lighting** and **face culling**.

Since 3D models are usually closed hulls, we don’t want to draw their **backfaces **(the faces that face inwards in relation to the model), so rendering engines examine which way the faces are facing and decide to draw or **cull** (hide) the face and not render it at all, saving time and performance from drawing the same thing twice.

As far as how lighting takes advantage of normals is concerned, I won’t go into too many details here, but as you can probably thing of instinctively, we need to know which way a face is facing to see if it’s looking towards a light source (and should therefore be lit).

The way lighting works also makes normals determine if an object will have **flat shading** (like our cube) or **smooth shading**.

While the normals visualization above helps with understanding how normal vectors look, they’re not actually stored in the faces; **normals are stored in the vertices**.

The more correct visualization of normals looks a bit like this:

![](../../assets/3f8be903834d9b79.png)

I can explain: While intuitively and for the purpose of usability in a 3D modeling software this cube seems to have 8 vertices (one for each corner), in the context of rendering this cube actually has 24 vertices. That’s because the 12 triangles of this mesh don’t actually share vertices, each triangle is formed by 3 vertices that are used to form just that one triangle.

If you inspect the cube mesh in Unity you’ll also see that the numbers are different than what Blender tells you:

![](../../assets/5f7527319f8c7cc6.png)

Smooth shading is achieved by basically interpolating the three normal vectors towards the median vector and applying that to each vertex of the corner.

Applying smooth shading to the cube makes our normals look like this:

![](../../assets/b38dc5e079f359d4.png)

They are interpolated smoothly along the edges they connect, so, in the context of lighting, it seems as if there is a smooth curve connecting the faces.

## Vertex colors

All 3D modeling applications provide the ability to assign colors to the vertices of your model, by a process that’s usually referred to as **vertex painting**.

This is an extremely useful feature, because, much like the UVs, it provides us with a set of model-specific values that we can later on use for our custom effects.

While vertex painting can be used to get some sort of visual output on your object, it’s very restricted by the fact that it works **per-vertex**, meaning that you can’t really get a lot of detail as you can only assign one color per vertex (per vertex-paint layer).

You can see how vertex colors behave here:

![](../../assets/ffe399e911d55f69.png)

I have assigned a color to each vertex of the top face – blue, red, yellow, green going clockwise from the left outmost vertex. While I haven’t provided any other color information, the colors are blended together along the edges and faces of the mesh.

I don’t think we’ll be using vertex colors any time soon in this series, but it’s definitely something to keep in mind.

## Position

In order to know how to actually render an object we should know where all its vertices should be in our 3D space. Selecting a vertex in Blender can give us its position:

![](../../assets/64f49c15df1ea4d7.png)

But here’s the thing: in our game engine we probably won’t have every single 3D object positioned at (0,0,0) in world-space. So while this position might use the same units of length as our game engine, it doesn’t correspond to a **world-space position** but to an **object-space position**, meaning that it assumes that the center (or **pivot**) of the object is the center of the world (located at (0,0,0) ).

## Data storing

While we mentioned that faces and edges are also useful, it should be evident that the real star of the show when it comes to 3D geometry is one: the **vertex**. All the properties mentioned above are stored **per-vertex** and then passed along and interpolated accordingly.

At the end of the day, a 3D model is just a list of numbers. Literally. If you open an .obj file with any text editor you can see that. Here’s what our cube comes down to:

![](../../assets/994f4e27f45bdd90.png)

The 8 sets of numbers with the “v” notation contain the object-space position for each of our 8 points. Then you have the 14 points of the UV coordinates and their position in the UV space. You can scroll up to see exactly which point corresponds to what line as well. Then you have the normal vectors, one for each of the 6 faces.

I know what you’re gonna say: why are there only 6 faces and 8 points and the normals don’t even match the number of points? Well, this is how the .obj format handles that information. The triangulation of the faces and all the other processing that happens is handled by the rendering engine when we import that file.

What’s interesting is to see how the faces are constructed in the file above. While the vertices are the real stars of the show, we do need to know which of them actually form a face and how that face will actually be like. Therefore, the last set of numbers corresponds to the faces. Each line signifies what vertices make up the face, what texture coordinates and what normal vector to use. It’s where everything comes together basically.

You’ll notice that the numbers in these lines are in fact integers – that’s because these are the indices that correspond to each of the three lists (positions, UVs, normals). So, for example, the second point of the first face (5/2/1) is using the 5th vertex on the list (positioned at (-1.0, 1.0, -1.0) in object-space), with the second set of UV coordinates (which would be (0.875, 0.5) ) and the first normal vector on the list (which would correspond to (0.0, 1.0, 0.0)).

## Conclusion

If you’ve used any 3D applications in the past it’s very possible that you knew about all of that stuff. However, I thought it would be important to present some information around 3D objects in regards to technical art and provide some context that will prove useful when we’ll be manipulating all that information using shaders.

See you on the [next part of ShaderQuest](https://halisavakis.com/shaderquest-part-2-introducing-shaders/)❗