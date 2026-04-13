---
title: Procedural Mesh Extrusion Tutorial
url: https://lindenreidblog.com/2017/11/05/procedural-mesh-extrusion-tutorial/
author: View all posts by Linden Reid
published: '2017-11-05'
source_blog: Linden Reid
source_site: https://lindenreid.wordpress.com
category: graphics
fetched: '2026-04-13'
---

*DISCLAIMER #1: Code presented here is pseudocode that does NOT necessarily reflect production Limit Theory code.*

*DISCLAIMER #2: This tutorial assumes you have at least basic knowledge of 3D geometry and related math.*

This week, I’m writing as many procedural generation tutorials as I can to help out participants of #PROCJAM! Today, I’m going to explain **how to extrude the triangles in a mesh**. For the purpose of this tutorial, extrusion is the process of copying all of the verticies in a triangle and** translating them in the direction of the surface normal,** so that you end up with a triangular prism.


![23336258_10214218042263374_1429825725_o](../../assets/edebaf10709b0eed.jpg)


As with the [stellation tutorial](https://lindenreid.wordpress.com/2017/11/04/procedural-stellation-tutorial/), let’s focus on just one triangle before we get to the rest of the mesh. Let’s note the triangle’s **three vertex positions** as three 3D vectors (or Vec3) called v1, v2, and v3 with x, y, and z coordinates.

First, we’ll need to define the **axis** that we want to extrude the face on. For that, we need to define the **surface normal** of the triangle.

**surface normal**is perpendicular to the face of the triangle, which can be calculated by taking the

**cross product of two vectors pointing along the edge of the triangle**. We then

**normalize**that vector to ensure its length is 1, as all we want for the surface normal is a direction, and not a length.

Vec3 e1 = v2 - v1 Vec3 e2 = v3 - v2 Vec3 normal = e1:cross(e2) normal = normal:normalize()

With that information determined, we can begin the extrusion. We want to **create three new ****vertices** that are **translated in the direction of the normal. **To translate each vertex, we **add the normal to each vertex**.** **“h” in this pseudocode is an optional distance to extrude the vertex by. The bigger it is, the longer our resulting pyramid will be.

Vec3 v4 = v1 + (normal * h) Vec3 v5 = v2 + (normal * h) Vec3 v6 = v3 + (normal * h)

**7 triangles to complete the pyramid**, we just need to make sure that we’re storing the indicies in the correct direction. Let’s call the indicies of v1, v2, and v3 –> i1, i2, and i3, respectively, and the indicies for the new verticies v4, v5, and v6 –> n1, n2, and n3, respectively. If you haven’t already been doing this,

**drawing a picture**helps massively with figuring out indicies. Assuming that you store indicies in a counter-clockwise direction (as we do on Limit Theory), the triangles are as follows:

-- top tri1 = Tri(n1, n3, n2) -- side tri2 = Tri(n1, i1, n2) tri3 = Tri(n2, i1, i2) -- side tri4 = Tri(n3, n2, i2) tri5 = Tri(n3, i2, i3) -- side tri6 = Tri(n3, i3, i1) tri7 = Tri(n3, i1, n1)

![23313424_10214218198867289_1198500641_o](../../assets/7b661b8699af4754.jpg)

**all of the old and new verticies and the new indicies**. You can

**disregard the original triangle**at (i1, i2, i3) if you’re about to apply this to a whole mesh, as that triangle would be hidden anyway.

-- determine surface normal Vec3 e1 = v2 - v1 Vec3 e2 = v3 - v2 Vec3 normal = e1:cross(e2) normal = normal:normalize() -- create extruded verticies Vec3 v4 = v1 + (normal * h) Vec3 v5 = v2 + (normal * h) Vec3 v6 = v3 + (normal * h) -- create tris -- top tri1 = Tri(n1, n3, n2) -- side tri2 = Tri(n1, i1, n2) tri3 = Tri(n2, i1, i2) -- side tri4 = Tri(n3, n2, i2) tri5 = Tri(n3, i2, i3) -- side tri6 = Tri(n3, i3, i1) tri7 = Tri(n3, i1, n1)

**every triangle on a mesh**. The tricky thing here is aligning the index locations correctly on our new mesh. For this algorithm, I add all of the original verticies first, then iterate on all of the old tris and extrude them 1 by 1, then add the extruded vertex & tris to the mesh. The key here is that I k

**eep track of the index of the “new” vertex**by incrementing it by 3 each time I add a new vertex. We add 3 because we add 3 new verticies each run of the loop. In addition,

**that index starts at the length of the old mesh’s vertex list.**See the bolded parts of the complete algorithm below to see what I mean.

function Extrude (Mesh oldMesh, int h) newMesh = Mesh() -- add ALL of the verticies from the old mesh Vec3[] oldVerticies = oldMesh.verticies for i = 1, #oldVerticies do newMesh:addVertex(oldVerticies[i]) end -- create new extruded verticies & trislocal vi = #newMesh.verticiesfor i = 1, #oldMesh.tris do -- old indicies int i1 = oldMesh.tris[i].i1 int i2 = oldMesh.tris[i].i2 int i3 = oldMesh.tris[i].i3 -- old verticies Vec3 v1 = oldMesh.verticies[i1] Vec3 v2 = oldMesh.verticies[i2] Vec3 v3 = oldMesh.verticies[i3] - normal Vec3 e1 = v2 - v1 Vec3 e2 = v3 - v2 Vec3 normal = e1:cross(e2) normal = normal:normalize() -- new vertex newMesh:addVertex( v1 + (normal * h) ) newMesh:addVertex( v2 + (normal * h) ) newMesh:addVertex( v3 + (normal * h) ) -- new tris -- top newMesh:addTri(n1, n3, n2) -- side newMesh:addTri(n1, i1, n2) newMesh:addTri(n2, i1, i2) -- side newMesh:addTri(n3, n2, i2) newMesh:addTri(n3, i2, i3) -- side newMesh:addTri(n3, i3, i1) newMesh:addTri(n3, i1, n1)vi = vi + 3end return newMesh end

[stellation](https://lindenreid.wordpress.com/2017/11/04/procedural-stellation-tutorial/), by varying h, applying it to the same mesh multiple times… etc. Get creative ;0



![ico](../../assets/5961e10133a941ec.png)


![extrusion](../../assets/62e2a886767887ec.png)




If you enjoyed this tutorial, see any typos or bugs, or have any other feedback, leave me a comment or tweet at me! You can follow me here on WordPress or on [Twitter @so_good_lin](https://twitter.com/so_good_lin). And be sure to keep track of [@LimitTheory on Twitter](https://twitter.com/LimitTheory) – when it comes out, the production version of all of this code & more will be available for exploring and modding. 🙂

*DISCLAIMER: Code presented here is pseudocode that does NOT necessarily reflect production Limit Theory code.*

Hi greeat reading your post

LikeLike