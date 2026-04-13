---
title: Intro to Procedural Geometry, Part 2
url: https://lindenreidblog.com/2018/02/24/intro-to-procedural-geometry-part-2/
author: View all posts by Linden Reid
published: '2018-02-24'
source_blog: Linden Reid
source_site: https://lindenreid.wordpress.com
category: graphics
fetched: '2026-04-13'
---

If you [follow me on Twitter](https://twitter.com/so_good_lin), you’ll know that I post polls to determine the content of these tutorials! Y’all are keeping up the trend of voting for this procedural geometry series, so as requested, here’s part 2 😀

Which tutorial topic do y’all want to see next week?

— Lindsey Reid (@thelindseyreid)

[February 4, 2018]

If you missed [Intro to Procedural Geometry, Part 1](https://lindenreid.wordpress.com/2018/01/20/intro-to-procedural-geometry-part-1/), and you’re unfamiliar with how vertices and triangles work, I highly recommend checking out that tutorial first.

This tutorial **assumes you know**:

- Basics of using Unity (creating objects, attaching scripts, using the inspector)
- How to code in C# (or at least a similar language)
- The high-level of how 3D geometry is represented in code (vertices and triangles)
- How to use Unity’s Mesh API to create geometry
- How to create a plane mesh in code

This tutorial **will** **teach you**:

- How to create a cube’s vertices and triangles
- How normals & UVs work (part 3)
- How to texture procedural meshes (part 4)

Let’s get started!


## Procedural Cube

In this tutorial, let’s flex our geometry and mesh knowledge by making a more complicated 3D shape.

Let’s start with the code to create a new mesh and create a new list for the vertices and indices. I separated the CreateBox() function into a method outside of start so that the same file can contain different shapes to test. As with the last tutorial, this is a script attached to a plane in the scene, although you could attach it to any 3D shape.

void Start () { CreateBox(); } void CreateBox() { // create a new mesh & assign it to our MeshFilter Mesh mesh = new Mesh(); meshFilter.mesh = mesh; // create a new list of vertices Vector3[] vertices = new Vector3[8]; // ((VERTEX ASSIGNMENT GOES HERE)) mesh.vertices = vertices; int[] tris = new int[36]; // ((TRIANGLE ASSIGNMENT GOES HERE)) mesh.triangles = tris; mesh.RecalculateNormals(); }

![cube](../../assets/8f7d1de7c550e4a0.jpg)


First of all, we need to figure out the **location of the vertices** in 3D space. It always helps to draw a picture. Here’s my attempt at a depiction of a cube **centered at the origin. **You could center yours elsewhere, but know that your vertex locations will be different.

Note that I’ve also marked the vertex locations with a number starting with 0. This number indicates the **index in the vertex list**. If you remember from part 1, this is important because the index of each vertex is used to create triangles. I purposefully decided to put the vertices in a clockwise winding order relative to the top face of the cube.

So, let’s get started figuring out the **vertex locations in 3D space.** We’re going to create a cube that’s **2x2x2 units**. Since we’re centered at the origin, this makes the vertex locations all 1 unit away from the closest axis, which makes figuring out their positions easier.

Let’s focus on just the **top face** first.

![plane](../../assets/66d126ce1236d342.jpg)


The y-position for all of these is easy- since this is the **top face**, all of these vertices are **1 unit up on the y-axis**. I omitted drawing the y-axis so that we can focus on the z and x positions.

```
// top
vertices[0] = new Vector3( ?, 1, ?); // 0
vertices[1] = new Vector3( ?, 1, ?); // 1
vertices[2] = new Vector3( ?, 1, ?); // 2
vertices[3] = new Vector3( ?, 1, ?); // 3
```

The drawing shows the direction in which the x and z axes are positive (+x and +z). Remember that we’re simplifying this cube by having all of the cube dimensions be 2, which makes each value for each vertex position be 1.

**Try to figure out all of the vertex positions yourself before looking below!**

You ready??

Ok, here’s the answer:

```
// top
vertices[0] = new Vector3(-1, 1, 1); // 0
vertices[1] = new Vector3( 1, 1, 1); // 1
vertices[2] = new Vector3( 1, 1, -1); // 2
vertices[3] = new Vector3(-1, 1, -1); // 3
```

Put this code in the section above marked ((VERTEX ASSIGNMENT GOES HERE)).

Since you’ve figured this out, it should now be easy to move on to the bottom half! These vertex positions are all the exact same, but the **y-values are now -1 instead of 1.**

// bottom vertices[4] = new Vector3(-1,-1, 1); // 4 vertices[5] = new Vector3( 1,-1, 1); // 5 vertices[6] = new Vector3( 1,-1, -1); // 6 vertices[7] = new Vector3(-1,-1, -1); // 7

Awesome, we’ve now got all of our vertex positions figured out! Let’s move on to triangles.

Our list of triangles has **36 spots**. Each spot stores a vertex index. The cube has 6 square faces, which require 2 triangles each, which each have 3 vertices. 6x2x3 = 36, so we need 36 spots.

```
// create a new list of triangles
int[] tris = new int[36];
```

Now, let’s figure out all of the triangles by figuring out just the top face first.

![quad](../../assets/df483c4a4d905d66.jpg)


Recall that Unity uses a **clockwise winding order**, which means that the direction we create our triangles needs to go in a clockwise direction from vertex to vertex. Remember that each set of 3 spots in the tris list creates a triangle by indicating an index location in the vertices list for a vertex.

The image above shows you the **top face** of the cube and the triangles used to create it. The arrows are showing the winding order of the triangles. With this drawing, it’s easy to create the **triangles for the top face**:

```
// top
tris[0] = 0;
tris[1] = 1;
tris[2] = 2;
tris[3] = 0;
tris[4] = 2;
tris[5] = 3;
```

If you put this code in the section marked ((TRIANGLE ASSIGNMENT GOES HERE)), and you’ve correctly created the vertices and triangles for this mesh, you should now see just the top of your cube!

Now, instead of copying the code for the rest of the triangles, I’m going to encourage you to figure them out yourself. If you need to, **draw a picture** like the one above for each face. Remember that the winding order is clockwise relative to the direction of the face- that is, the side that you want to see is the side you use to determine the winding order.

With all of the vertices and triangles calculated correctly, your cube should now be complete!

Buuuuuut… **the lighting is messed up**. That’s where we get into normals and UVs, which we’ll go over in Part 3!

## Fin

Hopefully, this tutorial helped you get a better grasp on how to generate vertices and triangles for a 3D mesh.

We’ll be going over how to properly set up normals and UVs for a mesh, which are important for texturing and lighting!

— > Go to Part 3 Here!!

Good luck,

Lin Reid [@so_good_lin](https://twitter.com/so_good_lin)


Need to update the “follow me on Twitter” link at the top with your new handle.

Good stuff on the new articles. Great reading, even for experienced devs.

LikeLike

Ah, fixed, thank you! I’m glad you like it ^^

LikeLike

Hi Linden, awesome work and I’m happy there is content like this when people are starting to learn Shader development with Unity 🙂

Just noticed a couple of things;

– The assignment Vector3[] vertices = new Vector3[4]; , should be Vector3[] vertices = new Vector3[8];

– The assignment int[] tris = new int[42]; , should be int[] tris = new int[36]; . For this one, you mention the new assignment to 36, but I feel a bit confusing the original value of 42.

LikeLike

Got it, thank you for the typo correction!

LikeLike