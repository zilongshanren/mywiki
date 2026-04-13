---
title: Godot Engine In-game Splat Map Texture Painting (Dirt Removal Effect)
url: https://alfredbaudisch.com/godot-engine/godot-engine-in-game-splat-map-texture-painting-dirt-removal-effect/
author: Alfred Reinold Baudisch
published: '2022-07-30'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

This is my solution to perform runtime Texture Painting, in order to paint a splat map in-game with the Godot Engine. My initial objective was to accomplish a Car Wash effect, i.e. remove a dirt texture that is overlaid on top of the car mesh's texture. But the final implementation can be used in many different scenarios and effects, such as:

- Actual painting something in game
- Terrain and mesh deformation
- Anything else you can imagine by blending textures. Because it's just a matter of interpolating the painted textures with anything else with shaders (sample shader included here).

Download the [source-code and sample project from my Github](https://github.com/alfredbaudisch/GodotRuntimeTextureSplatMapPainting) (you can walk in the world with WASD and to paint click and drag with the left mouse button). My journey in order to find the final solution is documented in the [Godot Forums](https://godotforums.org/d/30491-how-to-translate-a-world-coordinate-to-uv-coordinate).

![](../../assets/8dafe9f9e62ce4cb.jpg)


![](../../assets/8dafe9f9e62ce4cb.jpg)

## Features

- Any kind of brush
- Multiple brushes
- Multiple splat maps and multiple textures blended
- Mesh can be anywhere in the world and can be rotated

## World Position to UV

The first and most important step is to map a World Vector3 Position to a Mesh UV Position, in order to map the raycast from the current position the camera is looking at to the precise texture coordinate of the mesh.

This is easily accomplished in Unity with [RaycastHit.textureCoord](https://docs.unity3d.com/ScriptReference/RaycastHit-textureCoord.html) and in Unreal Engine with [Find Collision UV](https://docs.unrealengine.com/4.27/en-US/BlueprintAPI/Collision/FindCollisionUV/).

Unfortunately Godot does not provide any built-in mechanism to map a world position to UV, which led me to implement my own solution with GDScript to accomplish that.

## GDScript Get UV Coordinates from Vector3

The solution I found with Godot involves loading the Mesh vertices and normals with MeshDataTool, and then using Barycentric Coordinates to find the UV from a Vector3.

The final code is heavily adapted from this [Godot 2 repository from 2017](https://github.com/thefryscorer/GodotPaintDemo) by Daniel Byron. I also got the Barycentric calculation function from [Arnklit's Waterways Godot Plugin](https://github.com/Arnklit/WaterwaysDemo).

Since Daniel's code works only with meshes at the world origin (`Vector3(0,0,0)`

) and it regenerates the Mesh Data any time you need to find the UV), I improved it to make it work at runtime, with a mesh in any position in the world, as well I cache the vertex data and of course, I made it work with Godot 3.

### Code – [UVPosition.gd](http://UVPosition.gd)

```
extends Node
var meshtool
var mesh
var mesh_instance
var transform_vertex_to_global = true
var _face_count := 0
var _world_normals := PoolVector3Array()
var _world_vertices := []
var _local_face_vertices := []
func set_mesh(_mesh_instance):
mesh_instance = _mesh_instance
mesh = _mesh_instance.mesh
meshtool = MeshDataTool.new()
meshtool.create_from_surface(mesh, 0)
_face_count = meshtool.get_face_count()
_world_normals.resize(_face_count)
_load_mesh_data()
func _resize_pools():
pass
func _load_mesh_data():
for idx in range(_face_count):
_world_normals[idx] = mesh_instance.global_transform.basis.xform(meshtool.get_face_normal(idx))
var fv1 = meshtool.get_face_vertex(idx, 0)
var fv2 = meshtool.get_face_vertex(idx, 1)
var fv3 = meshtool.get_face_vertex(idx, 2)
_local_face_vertices.append([fv1, fv2, fv3])
_world_vertices.append([
mesh_instance.global_transform.xform(meshtool.get_vertex(fv1)),
mesh_instance.global_transform.xform(meshtool.get_vertex(fv2)),
mesh_instance.global_transform.xform(meshtool.get_vertex(fv3)),
])
func get_face(point, normal, epsilon = 0.2):
for idx in range(_face_count):
var world_normal = _world_normals[idx]
if !equals_with_epsilon(world_normal, normal, epsilon):
continue
var vertices = _world_vertices[idx]
var bc = is_point_in_triangle(point, vertices[0], vertices[1], vertices[2])
if bc:
return [idx, vertices, bc]
return null
func get_uv_coords(point, normal, transform = true):
# Gets the uv coordinates on the mesh given a point on the mesh and normal
# these values can be obtained from a raycast
transform_vertex_to_global = transform
var face = get_face(point, normal)
if face == null:
return null
var bc = face[2]
#
var uv1 = meshtool.get_vertex_uv(_local_face_vertices[face[0]][0])
var uv2 = meshtool.get_vertex_uv(_local_face_vertices[face[0]][1])
var uv3 = meshtool.get_vertex_uv(_local_face_vertices[face[0]][2])
return (uv1 * bc.x) + (uv2 * bc.y) + (uv3 * bc.z)
func equals_with_epsilon(v1, v2, epsilon):
if (v1.distance_to(v2) < epsilon):
return true
return false
func cart2bary(p : Vector3, a : Vector3, b : Vector3, c: Vector3) -> Vector3:
var v0 := b - a
var v1 := c - a
var v2 := p - a
var d00 := v0.dot(v0)
var d01 := v0.dot(v1)
var d11 := v1.dot(v1)
var d20 := v2.dot(v0)
var d21 := v2.dot(v1)
var denom := d00 * d11 - d01 * d01
var v = (d11 * d20 - d01 * d21) / denom
var w = (d00 * d21 - d01 * d20) / denom
var u = 1.0 - v - w
return Vector3(u, v, w)
func transfer_point(from : Basis, to : Basis, point : Vector3) -> Vector3:
return (to * from.inverse()).xform(point)
func bary2cart(a : Vector3, b : Vector3, c: Vector3, barycentric: Vector3) -> Vector3:
return barycentric.x * a + barycentric.y * b + barycentric.z * c
func is_point_in_triangle(point, v1, v2, v3):
var bc = cart2bary(point, v1, v2, v3)
if (bc.x < 0 or bc.x > 1) or (bc.y < 0 or bc.y > 1) or (bc.z < 0 or bc.z > 1):
return null
return bc
```


## Coffee, Coins and Thumbs Up

If you like my content or if you learned something from it, [buy me a coffee](https://ko-fi.com/alfredbaudisch) ☕, [be my Patreon](https://www.patreon.com/alfredbaudisch) or simply check [all of my links](https://linktr.ee/alfredbaudisch) 🔗 and follow me/subscribe/star my repositories/whatever you prefer. If you want to learn Godot, be sure to check [my courses](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) 📚!

**Or you can simply add my game to your Steam Wishlist – that helps GREATLY and it's easy and free 🙂**

## Dynamic Texture Render Target (Viewport)

The runtime paint strokes (or hits) are saved in a dynamic viewport texture.

Those are my settings:

![](../../assets/648a81b95b7f42d1.png)


And it has the following script attached ([DrawViewport.gd](http://DrawViewport.gd)):

```
extends Viewport
onready var brush = $Brush
func move_brush(position : Vector2):
set_update_mode(UPDATE_ONCE)
brush.set_position(position)
func brush_size():
return brush.texture.get_height()
```


As a child of the Viewport add a Sprite with the brush as texture.

## Mesh Setup

- Must have a collider.
- Shader which blends the Mesh main textures, with the Dirt/Damage textures and the splat map texture.
- If the mesh is high poly it's a must to have a very low-poly LOD to serve as the collider and to have the World to UV mapping, otherwise performance will be degraded (check the example project to see how I have done this).

![](../../assets/aa076545d11c5b83.png)


### Registering Paint Hits in the Render Target with Raycasts

Place a script in a Spatial Node anywhere in a Scene that has the Viewport Render Target, then assign the Viewport Texture to the `SplatMapTexture`

of the above shader.

Example: `material.set_shader_param("SplatMapTexture", viewport0.get_texture())`


Then, cast a ray, get the UV coordinates with `get_uv_coords`

and move the viewport brush sprite:

```
if result.size() > 0:
var uv = uv_positions.get_uv_coords(result.position, result.normal, true)
if uv:
get("viewport" + str(ray_idx)).move_brush(uv * tex_size)
```


And this is it! The splat map is drawn and since it's interpolated into the mesh's material, you are going to see the results immediately.

## Source-code and Sample Project

The Godot 3 sample project and source-code [is available on my Github](https://github.com/alfredbaudisch/GodotRuntimeTextureSplatMapPainting).