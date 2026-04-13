---
title: 'Unity 4D #4: Creating 4D Objects - Alan Zucconi'
url: https://www.alanzucconi.com/2023/07/06/creating-4d-objects/
author: Alan Zucconi
published: '2023-07-06'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This article will explain how to create four dimensional objects, in a format compatible with the Unity4D extension.

![](../../assets/5da7a095f43c7a44.gif)

You can find all the articles in this series here:

**Part 1:**[Understanding the Fourth Dimension](https://www.alanzucconi.com/?p=14778)**Part 2:**[Extending Unity from 3D to 4D](https://www.alanzucconi.com/?p=14808)**Part 3:**[Rendering 4D Objects](https://www.alanzucconi.com/?p=14825)**Part 4:****Creating 4D Objects**

## Introduction

The past three articles in this series talked at length about hypercubes and hyperspheres. And while Part 1 gave some basic intuitions on how hyperobjects are built, we have yet to see any code. The purpose of this final article is to show how such shapes can be constructed within the Unity4D framework that we developed.

In particular, we need to remember that a `Mesh4D`

instance is a scriptable object which serves and the 4D counterpart of Unity’s 3D `Mesh`

. Like `Mesh`

, `Mesh4D`

contains a list of vertices. Unlike `Mesh`

, however, `Mesh4D`

contains a list of *edges*, instead of *triangles* It is also important to remember that the Unity4D library works with any 4D shape, but can only render convex ones. If you need to render a concave 4D shape, you will have to built it out of multiple convex pieces.

That being said, it should be clear that to create a 4D object in Unity4D, we will need a list of vertices and the edges connecting it. The faces between them are implicitly assumed from the **convex hull** of its vertices.

## Hypercubes

The concept of *cube* can be generalised in any dimension as an ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)


| n | Name | Vertices | Edges | Faces |
|---|---|---|---|---|
| 0 | Point | ![]() | ||
| 1 | Segment | ![]() | ![]() | |
| 2 | Square | ![]() | ![]() | ![]() |
| 3 | Cube | ![]() | ![]() | ![]() |
| 4 | Tesseract | ![]() | ![]() | ![]() |
| n | ![]() | ![]() | ![]() | ![]() |

All of them can be constructed with an iterative process. An ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com \left(n-1\right)](../../assets/24ee41762235218a.png)


![](../../assets/8b28d8f8115b996c.png)

This process can be repeated endlessly, progressively creating hypercubes in higher dimensions. This is effectively a **hyper-extrusion**: en extrusion in a higher dimension.

If we are only interested in building a ![Rendered by QuickLaTeX.com 4](../../assets/0725b22597534378.png)

*tesseract*—we can also do it manually, according to the following schematics which uses two ![Rendered by QuickLaTeX.com 3](../../assets/dc7e9389c9a6a6e2.png)


![](../../assets/7c3ca31fa8e4d0b0.png)

The following scripts encodes the vertices and edges from the diagrams above into a `Mesh4D`

object. The various `x0`

, `x1`

, `y0`

, `y1`

, `z0`

, `z1`

, `w0`

and `w1`

passed as parameters are used to indicate the X, Y, Z and W coordinates of those vertices.

public void CreateCube4 (Mesh4D mesh, float x0, float x1, float y0, float y1, float z0, float z1, float w0, float w1) { Vector4[] vertices = new Vector4[8 * 2]; Mesh4D.Edge[] edges = new Mesh4D.Edge[12 * 2 + 8]; // w = 0 // Face down vertices[0] = new Vector4(x0, y0, z0, w0); vertices[1] = new Vector4(x1, y0, z0, w0); edges[0] = new Mesh4D.Edge(0, 1); vertices[2] = new Vector4(x0, y0, z1, w0); vertices[3] = new Vector4(x1, y0, z1, w0); edges[1] = new Mesh4D.Edge(2, 3); edges[2] = new Mesh4D.Edge(0, 2); edges[3] = new Mesh4D.Edge(1, 3); // Face up vertices[4] = new Vector4(x0, y1, z0, w0); vertices[5] = new Vector4(x1, y1, z0, w0); edges[4] = new Mesh4D.Edge(4, 5); vertices[6] = new Vector4(x0, y1, z1, w0); vertices[7] = new Vector4(x1, y1, z1, w0); edges[5] = new Mesh4D.Edge(6, 7); edges[6] = new Mesh4D.Edge(4, 6); edges[7] = new Mesh4D.Edge(5, 7); // Connects the two faces edges[8] = new Mesh4D.Edge(0, 4); edges[9] = new Mesh4D.Edge(1, 5); edges[10] = new Mesh4D.Edge(2, 6); edges[11] = new Mesh4D.Edge(3, 7); // w = 0 // Face down vertices[0 + 8] = new Vector4(x0, y0, z0, w1); vertices[1 + 8] = new Vector4(x1, y0, z0, w1); edges[0 + 12] = new Mesh4D.Edge(0 + 8, 1 + 8); vertices[2 + 8] = new Vector4(x0, y0, z1, w1); vertices[3 + 8] = new Vector4(x1, y0, z1, w1); edges[1 + 12] = new Mesh4D.Edge(2 + 8, 3 + 8); edges[2 + 12] = new Mesh4D.Edge(0 + 8, 2 + 8); edges[3 + 12] = new Mesh4D.Edge(1 + 8, 3 + 8); // Face up vertices[4 + 8] = new Vector4(x0, y1, z0, w1); vertices[5 + 8] = new Vector4(x1, y1, z0, w1); edges[4 + 12] = new Mesh4D.Edge(4 + 8, 5 + 8); vertices[6 + 8] = new Vector4(x0, y1, z1, w1); vertices[7 + 8] = new Vector4(x1, y1, z1, w1); edges[5 + 12] = new Mesh4D.Edge(6 + 8, 7 + 8); edges[6 + 12] = new Mesh4D.Edge(4 + 8, 6 + 8); edges[7 + 12] = new Mesh4D.Edge(5 + 8, 7 + 8); // Connects the two faces edges[8 + 12] = new Mesh4D.Edge(0 + 8, 4 + 8); edges[9 + 12] = new Mesh4D.Edge(1 + 8, 5 + 8); edges[10 + 12] = new Mesh4D.Edge(2 + 8, 6 + 8); edges[11 + 12] = new Mesh4D.Edge(3 + 8, 7 + 8); // Connects the two cubes edges[24] = new Mesh4D.Edge(0, 0 + 8); edges[25] = new Mesh4D.Edge(1, 1 + 8); edges[26] = new Mesh4D.Edge(2, 2 + 8); edges[27] = new Mesh4D.Edge(3, 3 + 8); edges[28] = new Mesh4D.Edge(4, 4 + 8); edges[29] = new Mesh4D.Edge(5, 5 + 8); edges[30] = new Mesh4D.Edge(6, 6 + 8); edges[31] = new Mesh4D.Edge(7, 7 + 8); // Copies the new geometry mesh.Vertices = vertices; mesh.Edges = edges; }

## Hyperspheres

A naive approach to build a hypersphere should be to extude a sphere into the fourth dimension. While that is definitely a valid approach to create a 4D object, it does not ultimately create a ![Rendered by QuickLaTeX.com 4](../../assets/0725b22597534378.png)


This means to produce a hypersphere we need an entirely new approach.

### 4D Icosphere: 600-cell

Many modern game engines are building 3D spheres through subdividision of a regular **icosahedron**. This process usually requires two steps:

- Subdividing the faces of a regular icosahedron
- Projecting the vertices onto a sphere

![](../../assets/ca5a0073d811a2c1.png)

[Wikipedia](https://en.wikipedia.org/wiki/Geodesic_polyhedron))

The same approach could be used in 4D. The 4D equivalent of a icosahedron is a [600-cell](https://en.wikipedia.org/wiki/600-cell). Compared to a much more tamed tesseract, a 600-cell can be very difficult to visualise. The website qfbox wrote an interesting articles that helps visualising its inner structure: [The 600-Cell](https://www.qfbox.info/4d/600-cell).

Constructing a 600-cell via code is rather nasty. If you are interested in such a task, these are the list of vertices of a 600-cell. First, you need to include the following 8 vertices, which represents the vertices of a [16-cell](https://en.wikipedia.org/wiki/16-cell) (a 4D tetrahedron):

(1) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align*} \left( \pm 1, 0, 0, 0 \right) \\ \left( 0, \pm 1, 0, 0 \right) \\ \left( 0, 0, \pm 1, 0 \right) \\ \left (0, 0, 0, \pm 1 \right) \end{align} \end{equation*}](../../assets/c4a03e1a63442e00.png)


Secondly, you need to include the 16 vertices of a tesseract with side length ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} \left( \pm \frac{1}{2}, \pm \frac{1}{2}, \pm \frac{1}{2}, \pm \frac{1}{2} \right) \end{equation*}](../../assets/2719d9b4de19d4c2.png)


And finally including the 96 vertices of a [snub 24-cell](https://en.wikipedia.org/wiki/Snub_24-cell). They are the even permutations of the following set:

(3) ![Rendered by QuickLaTeX.com \begin{equation*} \left( \pm \frac{\phi}{2}, \pm \frac{1}{2}, \pm \frac{\phi^{-1}}{2}, 0 \right) \end{equation*}](../../assets/54bdd04de7d446cc.png)


where ![Rendered by QuickLaTeX.com \phi](../../assets/5894f23fcbaa6c26.png)

*golden ratio*.

Providing a set of vertices is not enough to construct a mesh. In fact, `Mesh4D`

also requires a list of edges. Writing such a list by hand is incredibly tedious, so an easier approach is to simply construct the convex hull that envelops the vertices, and extracting the edges from the faces.

The following function initialises the vertices and edges of a given `Mesh4D`

object, from a set of 4D vertices:

public static void ConstructConvexHull (Mesh4D mesh, IList<Vector4> vertices) { // Vertex4 to Vertex Vertex[] vertices4 = vertices.Select(x => (Vertex)x).ToArray(); // Convex hull var result = ConvexHull.Create(vertices4); // Extracts edges Vector4[] verticesC = new Vector4[result.Faces.Count() * 4]; Mesh4D.Edge[] edgesC = new Mesh4D.Edge[result.Faces.Count() * 4]; int v = 0; foreach (var face in result.Faces) { // edge(0,1) verticesC[v] = face.Vertices[0]; edgesC[v] = new Mesh4D.Edge(v, v + 1); v++; // edge(1,2) verticesC[v] = face.Vertices[1]; edgesC[v] = new Mesh4D.Edge(v, v + 1); v++; // edge(2,3) verticesC[v] = face.Vertices[2]; edgesC[v] = new Mesh4D.Edge(v, v + 1); v++; // edge(3,0) verticesC[v] = face.Vertices[3]; edgesC[v] = new Mesh4D.Edge(v, v - 3); v++; } mesh.Vertices = verticesC; mesh.Edges = edgesC; }

Where `Vertex`

is a wrapper for a `double[4]`

, which is how the `MIConvexHull`

accepts vertices.

The code shown above is far from perfect. In fact, every face is equipped with its own set of unique vertices. To use an expression that the ones of you who are familiar with 3D modelling will understand: `ConstructConvexHull`

does not weld the vertices of the constructed 4D shape.

This is what a standard 600-cell looks like as it gently moves in and out of the 3D world:

![](../../assets/5da7a095f43c7a44.gif)

Once a 600-cell is constructed, the next step is to subdivide its faces, and to reproject all of its vertices onto a sphere. This means—assuming we are constructing a unit hypersphere—normalising all vertices so that their overall length is ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


The overall process is indeed rather nasty, which is why it is only presented as a series of steps, and is not really implemented in the Unity4D package.

### Random points

Creating a hyper-icosphere is definitely not for the faint-hearted. Another approach is to simply generate a set of random points, all at the same distance from the centre. Unity comes with a method called `Random.onUnitSphere`

which returns a random point on the surface of the unit sphere.

Unfortunately, there is no such method for a ![Rendered by QuickLaTeX.com 4](../../assets/0725b22597534378.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com 4](../../assets/0725b22597534378.png)


public static Vector4 OnUnitSphere4() { return new Vector4 ( Random.Range(-1f, +1f), Random.Range(-1f, +1f), Random.Range(-1f, +1f), Random.Range(-1f, +1f) ).normalized; }

One easy solution is to generate a high number of points using `OnUnitSphere4`

, and to then construct their convex hull from which the full set of edges can be extracted. This method is very efficient, but results in cross-sections that are not necessarily very spherical.

![](../../assets/2face236318a07ca.gif)

Yes, it’s a **hyper-potato**.

### Random points uniformly distributed

The reason why a the cross-section of a random set of points on the unity ![Rendered by QuickLaTeX.com 4](../../assets/0725b22597534378.png)


A slightly better result can be obtained by ensuring the points are not overlapping too much, and possibly even performing some gentle relaxation on them:

![](../../assets/e3d76d38db677543.gif)

That is still far from being, well, spherical. One solution to this is to rely on a function that, unlikely `OnUnitSphere4`

, provides a better random distribution.

One such technique has been proposed by StackExchange user [whuber](https://stats.stackexchange.com/a/7984), and relies on the statistical properties of the Gaussian distribution. If you are unfamiliar with the concept, that is one of the most used random distributions in Statistics as it well represents the distribution of many natural phenomena. In this blog we have covered the Gaussian distribution extensively, including an efficient way to sample Gaussian random numbers.

- Part 1:
[Understanding the Gaussian distribution](https://www.alanzucconi.com/?p=1685) - Part 2:
[How to sample from the Gaussian distribution](https://www.alanzucconi.com/?p=1713)

![](../../assets/1530504dea74d6d2.png)

Assuming we have 4 numbers which are sampled from a normalised Gaussian distribution ![Rendered by QuickLaTeX.com \mathcal{N}\left(0, 1\right)](../../assets/00d8989dc533304a.png)


(18) ![Rendered by QuickLaTeX.com \begin{equation*} X_i \sim \mathcal{N}\left(0, 1\right) \end{equation*}](../../assets/51e4ed84ecd5be90.png)


Let’s calculate the following quantity:

(19) ![Rendered by QuickLaTeX.com \begin{equation*} \lambda = \sqrt{X_1^2 + X_2^2 + X_3^2 + X_4^2} \end{equation*}](../../assets/ab8595c0c8163d07.png)


Then, the following points ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)


(20) ![Rendered by QuickLaTeX.com \begin{equation*} p = \begin{bmatrix} \frac{X_1}{\lambda} \\ \frac{X_2}{\lambda} \\ \frac{X_3}{\lambda} \\ \frac{X_4}{\lambda} \end{bmatrix} \end{equation*}](../../assets/9089ff01cefe8f88.png)


This technique is fairly efficient, and generalises well in higher dimensions as well. The animation below shows a sphere with a slightly higher vertex count, resulting in a much better cross-section.

![](../../assets/6e1ec44d85b914da.gif)

## Conclusion

This article concludes our journey through the fourth dimension. Thought-out these four posts, we have learnt how visualise, represents, manipulate and create four dimensional objects. And while this tutorial was targeted at Unity users, its knowledge can be easily extended to any other gaming engine such as Unreal or Godot.

What’s not left for you to do, is to make sure you can use this knowledge to build some awesome!

![](../../assets/740f05051a0fb72a.gif)

You can read all the articles in the series here:

**Part 1:**[Understanding the Fourth Dimension](https://www.alanzucconi.com/?p=14778)**Part 2:**[Extending Unity from 3D to 4D](https://www.alanzucconi.com/?p=14808)**Part 3:**[Rendering 4D Objects](https://www.alanzucconi.com/?p=14825)**Part 4:****Creating 4D Objects**

### 📚 Recommended Books

### Additional Resources

If you are interested in learning more about the fourth dimension and the hidden beauty of the objects it contains, I would suggest having a look at the following articles and books:

- 🌐
[Tesseract](https://ciechanow.ski/tesseract/)by Bartosz Ciechanowski, one of the best explorables about hypercubes. - 🌐
[4D Visualization](https://www.qfbox.info/4d/vis/vis)by qfbox, a series of short articles explaining different methods and techniques to visualise 4D objects. - 🌐
[Poisson-Disk Sampling](https://www.jasondavies.com/poisson-disc/)by Jason Davies, an interactive page with several links related to blue noise. - 🌐
[The Color of Noise](https://caseymuratori.com/blog_0010)by Casey Muratori, a detailed article about the difference blue noise can make in 3d renderings. - 📖
[The Visual Guide To Extra Dimensions](https://amzn.to/3NVvIxs)by Chris McMullen, one of the best books about understanding 4D geometries.

### 📦 Download Unity4D Package

![](../../assets/18396766e580bab9.png)


![](../../assets/18396766e580bab9.png)

All of the diagrams and animations seen in this tutorial have been made with **Unity4D**, the unity package that extends support for 4D meshes in Unity.

![](../../assets/2f7c47694fb8c2fa.png)

The **Unity4D** package contains everything needed to replicate the visual seen in this tutorial, including the shader code, the C# scripts, the 4D meshes, and the scenes used for the diagrams and animations. It is available through [Patreon](https://www.patreon.com/posts/85682045/).

## Leave a Reply Cancel reply