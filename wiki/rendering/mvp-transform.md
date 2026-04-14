---
tags: [渲染, 数学]
date: 2026-04-05
sources: 1
---

# MVP 变换

Model-View-Projection 变换——顶点从局部坐标系到裁剪空间的三阶段矩阵链。

## 链条

```
vertex_local → [M] → world → [V] → view → [P] → clip
```

- **Model 矩阵（M）**：local → world。
- **View 矩阵（V）**：world → view。
- **Projection 矩阵（P）**：view → clip。

## 为什么分开，不预乘？

矩阵运算意义上可以预乘成一个 `MVP = P*V*M`，但实际渲染管线保留分步，因为：

- **光照计算需要 World 或 View 空间位置**（法线、方向光、相机距离）。
- 阴影映射需要把顶点变到 light 的 clip space——重用 world position 省一次变换。
- 后处理需要从 clip 还原到 view（depth reconstruction）。

## 相关坐标空间

详见 [[coordinate-spaces]]：Model → World → View → Clip → NDC → Screen。

## Scheme vs DirectX / OpenGL 约定

- OpenGL：right-handed，Z looking down -Z in view space。
- DirectX：left-handed（历史）。
- 投影矩阵在两者间略不同，NDC Y 方向约定也不同。

## 物理对应

投影矩阵的 `fovY` 不是数学参数——它对应真实相机 **field of view**。参见 [[pinhole-camera]]，那里给出 `FoV = 2·atan(sensor/(2·distance))` 的物理推导，以及为什么游戏引擎的标准相机等价于针孔模型（无景深）。需要 bokeh / DoF 时参见 [[thin-lens-model]]。

## 相关

- [[coordinate-spaces]]
- [[pinhole-camera]] — 虚拟相机的物理本体
- [[thin-lens-model]]
- [[rendering-pipeline]]
- [[z-buffer]]
- [[perspective-correct-interpolation]]
- [[motion-vectors]] — 两帧 MVP 之差用来生成屏幕空间运动矢量，是 temporal 技术的基础
- [[3d-rotation-math]] — 旋转矩阵的三种来源（Euler / Axis-Angle / 四元数）
- [[shader-vector-math-primer]] —— 从零解释 "矩阵乘向量 = 换坐标系" 的入门版本

## Sources

- [[sources/rtr-day03]]
- [[sources/ciechanow-cameras-and-lenses]]
