---
title: 'Unity 4D #2: Extending Unity to 4D - Alan Zucconi'
url: https://www.alanzucconi.com/2023/07/06/unity-3d-to-4d/
author: Alan Zucconi
published: '2023-07-06'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This article will show how to extend Unity to support four-dimensional geometry. This is the second article in a series of four, and the first one which will probably start discussing the Mathematics and the C# code necessary to store and manipulate 4D objects in Unity.

![](../../assets/cd39e2aebca07998.gif)

![](../../assets/d222d6ad179fda06.gif)

![](../../assets/2a585b4e75ed6335.gif)

You can find all the articles in this series here:

**Part 1:**[Understanding the Fourth Dimension](https://www.alanzucconi.com/?p=14778)**Part 2:**[Extending Unity from 3D to 4D](https://www.alanzucconi.com/?p=14808)**Part 3:**[Rendering 4D Objects](https://www.alanzucconi.com/?p=14825)**Part 4:**[Creating 4D Objects](https://www.alanzucconi.com/?p=14864)

A link to download the Unity4D package can be found at the end of this article.

## Introduction

Most of the readers following my blog are familiar with Pikuniku, a whimsical game I worked on in 2019. Not many of you, however, remember all of the teaser trailers that were posted prior to its release. Back in 2017, the official Pikuniku Twitter account posted a short video showing a 4D version of the game.

Many were quick to assume that was just a joke, ignoring what they saw was an actual 4D version of the titual character, Piku, rendered in four dimensions.

Five years later, this tutorial will finally explain how that video was created, and how Unity can be extended from its canonical three dimensions, to support four. In this instalment will focus on implementing the backbones of 4D geometry; the next article will focus on the rendering instead.

## Anatomy

There are countless ways in which Unity could be extended to support four-dimensional objects. The solution proposed in this series is to create analogous 4D classes to Unity’s existing ones. For instance, a `Mesh4D`

class will mirror the role of Unity’s `Mesh`

. The table below maps the main components used in this project, and their analogous to the “traditional” Unity 3D.

The familiar `MeshFilter`

component has not been implemented, as `Mesh4D`

objects are linked directly.

On top of the principal components and scriptable objects seen above, this project also requires the introduction of data types that can support 4D calculations. In some cases, Unity already contains classes that can be used. For instance, Unity has its own definition of a `Vector4`

, which already comes with everything needed. Unity also supports 4 by 4 matrices with `Matrix4x4`

. Unfortunately, this class does not have feature parity with its 3D counterpart (`Matrix3x3`

), as it does not implement basic operations such as the matrix product. In this case, extension methods will be used to seamlessly extend its capabilities.

Lastly, there will be some completely new classes that need to be created. For instance: Unity stores the rotations in the `Transform`

class, using `Vector3`

variables. This is not really possible in 4D, since there are 6 Euler angles in 4D; this requires a new type called `Euler4`

.

| Unity | Unity 4D |
|---|---|
`Vector3` | `Vector4` Used for all coordinates in 4D. |
| – | `Euler4` 🆕Stores the rotation along the 6 rotational axes in 4D. |
| – | `Edge` 🆕Defines an edge between two vertices. Traditional meshes do not explicitly contain this information, but it is very useful for certain representations. |
`Matrix3x3` | `Matrix4x4` Used to represent rotation matrices, necessary to rotate the objects in 4D. |
| – | `Matrix4x4Extension` 🆕Used to provide basic functionalities to `Matrix4x4` class, including: matrix multiplication, component-wise product and division, inner and dot product. |

On top of these classes, we will need a few more to physically build the `Mesh4D`

scriptable objects representing hypercubes and hyperspheres, and to arbitrarily “extrude” three-dimensional meshes into four-dimensional ones.

## The Mathematics of the Fourth Dimension

A traditional 3D model in Unity is represented by the `Mesh`

class, which contains a list of its vertices along with the triangles that connect them. Together, they form the scaffolding of every 3D object. In four dimension, we will do pretty much the same. The main difference is that vertices will be stored using `Vector4`

s, rather than `Vector3`

s.

In this section, we will see how to represent them via code, and also how to extend the translation, scale and rotation from 3D to 4D. This will allow us to recreate the functionalities offered by the `Transform`

component.

### Geometry

The class that contains the information about the 4D geometry is `Mesh4D`

. Similarly to Unity’s `Mesh`

, it contains a list of vertices; but unlike `Mesh`

, it stores a list of edges, not triangles.

public class Mesh4D : ScriptableObject { public Vector4[] Vertices; public Edge[] Edges; }

An edge is a connection between two vertices. It is stored using the `Edge`

struct, which simply contains the indices of the respective vertices in the `Vertices`

array.

[Serializable] public struct Edge { public int Index0; public int Index1; public Edge(int index0, int index1) { Index0 = index0; Index1 = index1; } }

Both 3D and 4D meshes are built out of triangles. The only difference is that in 3D the vertices of those triangles are `Vector3`

, while in 4D they should be `Vector4`

. In this implementation, however, we are not storing triangles. The reason is simple: when visualising a 4D mesh, we need to calculate its intersection with the 3D world. Intersecting four-dimensional triangles with the 3D space is way more complex than intersecting edges.

By storing edges, we are still able to define a 4D mesh, and the overall code to bring it into the 3D world will be much simpler. As a drawback, unfortunately, this technique only works with convex geometries. This is not really an issue, as even many 3D algorithms (such as the ones related to physics and collisions) only work on convex meshes. Ultimately, working with convex meshes is not a limitation as concave ones can be built by composition.

## Transform

The `Mesh4D`

class works like an actual 3D model. The information contained inside is not supposed to be changed at runtime. Translation, rotation and scaling are applied by the `Transform4D`

component, which serves as a 4D analogous to Unity’s `Transform`

.

To make the class more computationally efficient, the positions of the transformed vertices are stored, alongside the **rotation matrix** and its inverse (which will be very helpful later on).

public class Transform4D : MonoBehaviour { [Header("Mesh4D")] public Mesh4D Mesh; private Vector4[] Vertices; [Header("Transform")] public Vector4 Position; public Euler4 Rotation; public Vector4 Scale = new Vector4(1,1,1,1); private Matrix4x4 RotationMatrix; private Matrix4x4 RotationInverse; }

Both `Position`

, `Rotation`

and `Scale`

have to account for the fact that four dimensions are now available. This means using `Vector4`

for `Position`

and `Scale`

, and a hypothetical `Vector6`

or `Rotation`

. In fact, while there are 3 rotation axes in 3D, there are 6 rotation planes in 4D; Unity does not contain a `Vector6`

struct, so a custom type has to be created. For the occasion, it is called `Euler4`

, as it represents Euler angles in 4D:

[Serializable] public struct Euler4 { [Range(-180, +180)] public float XY; // Z (W) [Range(-180, +180)] public float YZ; // X (w) [Range(-180, +180)] public float XZ; // Y (W) [Range(-180, +180)] public float XW; // Y Z [Range(-180, +180)] public float YW; // X Z [Range(-180, +180)] public float ZW; // X Y }

Understanding how rotations work in 4D is fairly complex, so a later section will expand on the topic, and clarify why 4D dimensions have 6 rotation planes, and not just 4 rotation axes.

The responsibility of the `Transform4D`

component is to update the vertices based on the desired position, rotation and scale. To do so, the component calculates the current rotation matrix, and updates the vertices using the `Transform`

method that effectively maps a `Vector4`

point from **object space** to **world space**.

private void Update() { UpdateRotationMatrix(); UpdateVertices(); } private void UpdateVertices () { for (int i = 0; i < Mesh.Vertices.Length; i++) Vertices[i] = Transform(Mesh.Vertices[i]); }

At this point in the article is worth reminding that both rotation and scaling are typically performed through the same mechanism: matrix multiplication. A 3D point can be rotated and scaled using a 3×3 matrix; likewise, the same can be obtained in 4D using a 4×4 matrix. Translation, unfortunately, cannot be done like this. If you are familiar with how 3D graphic works, you might have heard of **affine transformations** and **homogenous coordinates**. In 3D, this means representing coordinates as ![Rendered by QuickLaTeX.com \left[x,y,z,1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6e5b8514f34ef7a59d1491cfedcd0855_l3.png)

[TRS matrix](https://docs.unity3d.com/ScriptReference/Matrix4x4.TRS.html)).

Affine transformations work in 4D as well, and we could technically encode a 4D vertice in a 5D vector ![Rendered by QuickLaTeX.com \left[x,y,z,w,1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0456c907951c854093a19e7c22b6eb13_l3.png)


// Takes a 4D point and translate, rotate and scale it // according to this transform public Vector4 Transform (Vector4 v) { // Rotates around zero v = RotationMatrix.Multiply(v); // Scales around zero v.x *= Scale.x; v.y *= Scale.y; v.z *= Scale.z; v.w *= Scale.w; // Translates v += Position; return v; }

What is now missing is to understand how to create the rotation matrix.

### Rotations

Understanding rotations in 2D and 3D comes naturally to us, since we have evolved to manipulate complex objects in space. However, anyone who has studied the mathematics behind rotations can verify how messy it gets. What is geometrically intuitive for us, becomes impossibly counterintuitive when we start formalising it mathematically. It does not help that there are several different ways to model both orientations and rotations. Unity supports three of them: **Euler angles**, **rotation matrices** and **quaternions**. The last ones are used internally by the engine. Despite their popularity, quaternions are deemed among the most technically challenging subjects in geometry. So much so that in the past they have even been labelled as “evil” by Lord Kelvin:

«Quaternions came from Hamilton after his really good work had been done; and, though beautifully ingenious, have been an unmixed evil to those who have touched them in any way, including Clerk Maxwell.»

Lord Kelvin, 1892.

In this article, we will expose the orientation of a 4D mesh using Euler angles, which is Unity’s method of choice to display them in the inspector. The “Rotation” field of the Transform component in every game object is, in fact, displaying Euler angles. Euler angles are a way to visualise the orientation of an object by decomposing it as three successive rotations around different axes. In Unity, these rotations are performed around the Z axis, the X axis, and the Y axis. The order in which these are performed is important, as rotations are not commutative: doing them in a different order might result in a different final orientation.

One common misconception that needs to be clarified is that *there are three rotation axes in 3D because there are 3 dimensions*: this is not correct. In fact, there are 6 rotation planes in 4D, not 4. The root of this misconception is that in 3D there are as many rotation axes as dimensions; but that is a coincidence, and does not occur in other dimensions. For instance, there is only one rotation axis in 2D, not 2.

As explained by Steven Richard Hollasch in “[Four-Space Visualization of 4D Objects](https://hollasch.github.io/ray4/Four-Space_Visualization_of_4D_Objects.html)“, rotations […] are more properly thought of not as rotations about an axis, but as rotations parallel to a 2D plane. There is only one rotation axis in 2D, because there is only one 2D plane. Such rotation can be defined by the plane in which it takes place (XY) or by the normal to that plane (Z axis). Incidentally, all points on the rotation axis are unchanged. Another way to see this is to imagine the normal as a handle that rotates the plane it is attached to.

There are three rotation axes in 3D, because there are three 2D planes: XY, YZ and XZ, which normals correspond to Z, X and Y axes.

![](../../assets/e03beed50693b59d.gif)

![](../../assets/36a37852888f4e37.gif)

![](../../assets/8b14d6d6d2d696ad.gif)

Likewise, there are six rotation axes in 4D, because there are six 2D planes: XY, YZ, XZ, XW, YW and ZW. While 2D and 3D rotations leave the points on their rotation axes unchanged, in 4D there is an entire plane of points unaffected by the rotation.

![](../../assets/cd39e2aebca07998.gif)

![](../../assets/d222d6ad179fda06.gif)

![](../../assets/2a585b4e75ed6335.gif)

Generally speaking, in an ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com {n \choose 2}](../../assets/21d5e57f46cd4f1b.png)


| 2D | 3D | 4D |
|---|---|---|
| XY plane (Z axis fixed) | XY plane (Z axis fixed) | XY plane (ZW plane fixed) |
| YZ plane (X axis fixed) | YZ plane (XW plane fixed) | |
| XZ plane (Y axis fixed) | XZ plane (YW plane fixed) | |
| XW plane (YZ plane fixed) | ||
| YW plane (XZ plane fixed) | ||
| ZW plane (XY plane fixed) |

Now that we understand that there are 6 rotation planes in 4D, and that rotation can be performed using matrix multiplication, the next step is to define them. In this article, we will not derive them as this is outside the scope. However, If you are interested I suggest reading the following articles which provide a detailed explanation of how rotation matrices are derived:

The proposed solution for this problem is to have a static function that can produce the rotation matrix for each separate rotation plane. For instance, `RotateXY(Mathf.PI/2f)`

will return the rotation matrix that performs a 90° rotation around the XY plane. Once we have that, we can chain all rotations by multiplying together their respective rotation matrices:

private Matrix4x4 UpdateRotationMatrix() { RotationMatrix = Matrix4x4.identity .RotateXY(Rotation.XY * Mathf.Deg2Rad) .RotateYZ(Rotation.YZ * Mathf.Deg2Rad) .RotateXZ(Rotation.XZ * Mathf.Deg2Rad) .RotateXW(Rotation.XW * Mathf.Deg2Rad) .RotateYW(Rotation.YW * Mathf.Deg2Rad) .RotateZW(Rotation.ZW * Mathf.Deg2Rad); RotationMatrixInverse = RotationMatrix.inverse; return RotationMatrix; }

In the function above, we use `Mathf.Deg2Rad`

since Euler angles are expressed in *degrees*, while the various `Rotate--`

functions take *radians* as input.

Below, you can find the definition for all the various rotation matrices.

## What’s Next…

This article explained in details the mathematics of four-dimensional objects, as a direct extension of the more traditional Euclidean geometry. We also created a new set of classes capable of storing and manipulating 4D meshes, in a way that is not dissimilar to how Unity stores and manipulates conventional 3D meshes.

The next instalment in this series will explore three different techniques to render 4D meshes.

![](../../assets/65f39f13318b4dc8.gif)

You can read the remaining articles in the series here:

**Part 1:**[Understanding the Fourth Dimension](https://www.alanzucconi.com/?p=14778)**Part 2:****Extending Unity from 3D to 4D****Part 3:**[Rendering 4D Objects](https://www.alanzucconi.com/?p=14825)**Part 4:**[Creating 4D Objects](https://www.alanzucconi.com/?p=14864)

### Additional Resources

If you are interested in learning more about the fourth dimension and the hidden beauty of the objects it contains, I would suggest having a look at the following articles and books:

- 🌐
[Tesseract](https://ciechanow.ski/tesseract/)by Bartosz Ciechanowski, one of the best explorables about hypercubes. - 🌐
[Four-Space Visualization of 4D Objects](https://hollasch.github.io/ray4/Four-Space_Visualization_of_4D_Objects.html)by Steven Richard Hollasch, a comprehensive article on how to implement and render 4D shapes. - 📖
[The Visual Guide To Extra Dimensions](https://amzn.to/3NVvIxs)by Chris McMullen, one of the best books about understanding 4D geometries. - 📖
[Flatland](https://amzn.to/44d4QyP)by Edwin A. Abbott, a classic story about creatures living on a 2D world.

### 📦 Download Unity4D Package

![](../../assets/18396766e580bab9.png)


![](../../assets/18396766e580bab9.png)

All of the diagrams and animations seen in this tutorial have been made with **Unity4D**, the unity package that extends support for 4D meshs in Unity.

![](../../assets/2f7c47694fb8c2fa.png)

The **Unity4D** package contains everything needed to replicate the visual seen in this tutorial, including the shader code, the C# scripts, the 4D meshes, and the scenes used for the diagrams and animations. It is available through [Patreon](https://www.patreon.com/posts/85682045/).

## Leave a Reply Cancel reply