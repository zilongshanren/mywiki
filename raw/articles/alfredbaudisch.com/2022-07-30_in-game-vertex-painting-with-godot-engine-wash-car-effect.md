---
title: In-game vertex painting with Godot Engine (Wash Car Effect)
url: https://alfredbaudisch.com/experiment-logs/in-game-vertex-painting-with-godot-engine-wash-car-effect/
published: '2022-07-30'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

As stated in the [experiment page](https://alfredbaudisch.com/experiments/gamedev/runtime-in-game-vertex-painting-to-simulate-dirt-removal/), the intention here is to add and remove dirt from meshes dynamically during runtime. My implementation works in packaged games and projects, without any performance hit (dealing with vertex colors is cheap).

In any case, I am not going to use this implementation and this approach. I decided to move forward with splat maps and [realtime texture painting with Render Textures from Viewports](https://alfredbaudisch.com/blog/gamedev/godot-engine/godot-engine-in-game-splat-map-texture-painting-dirt-removal-effect/), because then I don't have to worry about mesh density. But it's fine to use this implementation for simple meshes and simple use cases.

The source-code and a sample [working project is available on my Github](https://github.com/alfredbaudisch/GodotInGameVertexPaintingDirtEffect).

## Mesh and Material Setup

- In any mesh, paint in any of the vertex color RGB channels (or in all of them for different effects) where you want to have dirt (or any kind of texture)
- In the material, you interpolate between the different textures with the main texture of the mesh, where the amount/alpha are the vertex colors.

### Painting in the editor (Preloading vertex colors)

In order to map the starting colors of the vertices (for example, where in the car it's going to be dirty?), the vertices have to be pre-painted.

They can be painted both in an external 3D package (Blender, etc) or inside Godot, but to paint inside Godot you need the [VPainter addon](https://github.com/tomankirilov/VPainter).

Then, with this implementation, you can paint the vertices at runtime, for example, to remove dirt and other effects.

## Implementation

- Attach a script to your character or camera.
- Point your camera to a mesh with vertex colors painted and a mesh that has the previous material, and paint (or clean!).
- Download the sample project from GitHub.

```
extends Spatial
var recheck := false
var ray_length = 1000
var brush_size:float = .3
var brush_opacity:float = .25
var brush_hardness:float = 0.2
var paint_color = Color(1, 1, 1, 1)
var click_position
export var mesh_path : NodePath
var current_mesh : MeshInstance
func _ready():
current_mesh = get_node(mesh_path) as MeshInstance
func _unhandled_input(event):
if event is InputEventMouseMotion:
recheck = true
func _physics_process(delta):
if recheck:
var position2D = get_tree().root.get_mouse_position()
var camera = $Camera
var from = camera.project_ray_origin(position2D)
var to = from + camera.project_ray_normal(position2D) * ray_length
var space_state = get_world().direct_space_state
# use global coordinates, not local to node
var result = space_state.intersect_ray(from, to, [self], 1, true, true)
if result.size() > 0:
click_position = result.position
_paint_tool()
recheck = false
#
# This code segment is taken from https://github.com/tomankirilov/VPainter
# Copyright (c) 2020 toman kirilov (MIT License)
#
func _paint_tool() -> void:
var data = MeshDataTool.new()
data.create_from_surface(current_mesh.mesh, 0)
for i in range(data.get_vertex_count()):
var vertex := current_mesh.to_global(data.get_vertex(i))
var vertex_distance:float = vertex.distance_to(click_position)
if vertex_distance < brush_size/2:
var linear_distance = 1 - (vertex_distance / (brush_size/2))
var calculated_hardness = linear_distance * brush_hardness
data.set_vertex_color(i, data.get_vertex_color(i).linear_interpolate(paint_color, brush_opacity))
current_mesh.mesh.surface_remove(0)
data.commit_to_surface(current_mesh.mesh)
```


## Coffee, Coins and Thumbs Up

If you like my content or if you learned something from it, [buy me a coffee](https://ko-fi.com/alfredbaudisch) ☕, [be my Patreon](https://www.patreon.com/alfredbaudisch) or simply check [all of my links](https://linktr.ee/alfredbaudisch) 🔗 and follow me/subscribe/star my repositories/whatever you prefer. If you want to learn Godot, be sure to check [my courses](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) 📚!

**Or you can simply add my game to your Steam Wishlist – that helps GREATLY and it's easy and free 🙂**

## Where to place the materials?

In the example project, the example Mesh is a car from Kenney, which has many different surfaces.

In this case, MeshInstance's "Surface 3" contains the material `R_M_SuvHood.tres`

and "Surface 5" contains the material `R_M_SuvWindows.tres`

.