---
title: 3D Software Coordinate System Table
url: https://30fps.net/xyz/
published: '2023-03-17'
source_blog: Computer Graphics & Programming with Pekka Väänänen — 30fps.net
source_site: https://30fps.net/
category: graphics
fetched: '2026-04-19'
---

| Name | Right | Up | Forward | Handedness |
| OpenGL View Space | +x | +y | -z | right |
| Three.js | +x | +y | -z | right |
| ARKit | +x | +y | -z | right |
| Maya | +x | +y | -z | right |
| Houdini | +x | +y | -z | right |
| Direct3D View Space | +x | +y | +z | left |
| Unity | +x | +y | +z | left |
| Blender | +x | +z | +y | right |
| 3ds Max | +x | +z | +y | right |
| Unreal Engine | +y | +z | +x | left |
| Quake | +x | +z | +y | right |
| GLTF | -x | +y | +z | right |

View space axis names: "Right" and "Up" correspond to their respective directions on screen. The "Forward" axis points to the direction the camera is looking.

World space axis names: Consider a top-down view of the world. The "Right" and "Forward" axes increase to the right and up, respectively. So "Right" corresponds to "easting" and "Forward" to "northing". The "Up" axis points away from gravity vector.

Maintained by Pekka Väänänen at [30fps.net](https://30fps.net)