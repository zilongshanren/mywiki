---
tags: [coordinate-system, handedness, engine-comparison, graphics-api]
date: 2026-04-19
sources: 1
---

# 3D 软件坐标系对照表

主流引擎和 API 的「右 / 上 / 前」轴约定并不统一，[[pekka-vaananen]] 在 30fps.net 上维护了一张对照表，专治移植数据时搞不清楚该不该翻 Z、该不该交换 Y/Z 的场景。这一页把它整理成中文速查，方便在 [[coordinate-spaces]] 体系里找到具体引擎落点。

## View space（相机空间）

| 名称 | Right | Up | Forward | 手性 |
|---|---|---|---|---|
| OpenGL | +x | +y | -z | 右手 |
| Three.js | +x | +y | -z | 右手 |
| ARKit | +x | +y | -z | 右手 |
| Maya | +x | +y | -z | 右手 |
| Houdini | +x | +y | -z | 右手 |
| Direct3D | +x | +y | +z | 左手 |
| Unity | +x | +y | +z | 左手 |

> "Right" 与 "Up" 指屏幕上的方向，"Forward" 指相机看出去的方向。

## World space（世界空间）

| 名称 | Right | Up | Forward | 手性 |
|---|---|---|---|---|
| Blender | +x | +z | +y | 右手 |
| 3ds Max | +x | +z | +y | 右手 |
| Unreal Engine | +y | +z | +x | 左手 |
| Quake | +x | +z | +y | 右手 |
| glTF | -x | +y | +z | 右手 |

> 世界空间取俯视图：Right 向地理东方，Forward 向北方，Up 背离重力。

## 观察与陷阱

- **手性不是唯一变量**：同为右手系的 Blender 和 OpenGL view space，"哪根轴是 Up" 也不同——Blender 把 Z 当 Up（地理直觉），OpenGL view space 把 Y 当 Up（屏幕直觉）。
- **Unreal 尤其反常**：Forward = +X、Right = +Y、Up = +Z，再加上左手系，导入 glTF / FBX 时常需要整体旋转一次再翻转。
- **glTF 的 -x Right** 是 2.0 规范特有的约定，容易被当成数据错误。
- 从引擎 A 导资产到引擎 B 时，**只看手性不够**，还得判断三轴的具体角色——这张表的价值正是一眼看清整组约定。

## 相关

- [[coordinate-spaces]] —— 渲染流水线整体的坐标空间体系
- [[mvp-transform]]
- [[gltf-workflow]]

## Sources

- [[sources/30fps-coordinate-system-table]]
