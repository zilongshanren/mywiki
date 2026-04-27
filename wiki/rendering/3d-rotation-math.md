---
tags: [渲染, 数学, shader]
date: 2026-04-14
sources: 3
---

# 3D 旋转的几种数学形式

对一个 3D 向量做旋转，shader 里常见的三种形式各有所长：**欧拉角**、**轴角**、**四元数**。理解它们的差别，关键是看你怎么回答两个问题——「我要绕什么转？」和「我需不需要插值两个姿态？」。

## 欧拉角（Euler Angles）

最直观的一种：把 3D 旋转拆成三个独立的 2D 旋转，分别绕 X、Y、Z 轴各转一次。在 shader 里就是三次 `mat2 * vec2`：

```glsl
vector.yz = rotate2D(ROLL)  * vector.yz;   // 绕 X 轴（roll）
vector.xz = rotate2D(PITCH) * vector.xz;   // 绕 Y 轴（pitch）
vector.xy = rotate2D(YAW)   * vector.xy;   // 绕 Z 轴（yaw）
```

**特点**：

- **顺序敏感**——roll→pitch→yaw 和 yaw→pitch→roll 结果不同。反向旋转要倒序并调换 `mat*vec` → `vec*mat`。
- 适合「只需要 yaw + pitch」的第一人称摄像机、飞行器等 **自然就是 XYZ 独立的动作**。
- 缺点：绕任意轴转不直观；有 [**gimbal lock**](https://en.wikipedia.org/wiki/Gimbal_lock)（两轴对齐时丢一个自由度）；插值两个姿态不平滑。

这是 Xor 的 GM Shaders Mini 2D → 3D 延伸版本的直接做法：**先会 2D，再堆叠就是 Euler 的 3D**。

## 轴角（Axis-Angle）

绕任意单位向量 `axis` 转 `ang` 弧度。Fabrice Neyret 流传甚广的一行 GLSL 是：

```glsl
vec = mix(dot(vec, axis) * axis, vec, cos(ang))
    + sin(ang) * cross(vec, axis);
```

拆开看每一块的几何意义：

- `dot(vec, axis) * axis` —— 向量在 axis 上的**投影点**，即旋转时不动的「圆心」。
- `mix(center, vec, cos(ang))` —— 在圆心和向量之间按 `cos` 振荡，相当于 2D 旋转里 `cos * x`。
- `sin(ang) * cross(vec, axis)` —— 垂直于 axis 的那个方向乘 `sin`，相当于 2D 旋转里 `sin * y`。
- 两者相加：**绕 axis 的圆周运动**。

条件：`axis` 必须是单位向量，`ang` 单位是弧度。这其实是 [Rodrigues' rotation formula](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula) 的向量形式。

**特点**：

- 绕任意轴干净利落，不需要先变到别的坐标系。
- 比三次 2D 旋转少做不少运算。
- 没有 gimbal lock——至少单步没有。
- 不直接支持**姿态插值**——想「从姿态 A 平滑过渡到姿态 B」还是要上四元数。

## 四元数（Quaternion）

Xor 在原文里声明「留到下一篇」，本 wiki 暂作占位。四元数的本质是**在 4D 单位球上做插值**（slerp），提供无 gimbal lock、插值平滑、可高效组合的完整旋转表示。动画骨骼、物理姿态、摄像机平滑跟随都依赖它。

## 选择标准

| 需求 | 推荐 |
|---|---|
| 第一人称摄像机，只需 yaw + pitch | Euler |
| 绕任意单位轴单次旋转 | Axis-Angle |
| 姿态之间平滑插值（动画） | 四元数 |
| 硬件管线里批量变换顶点 | 3×3 或 4×4 旋转矩阵（Euler/Axis-Angle 都可转成） |

一个常见误区是「四元数总是最好」。真实项目里更常见的形态是**内部用四元数做存储与插值，在需要对向量操作时临时转回旋转矩阵或轴角**。

## 本质观察

Xor 的总结一句话：**旋转总是发生在某一个平面上**。2D 里只有一个平面，所以是最简单的情形；3D 里有无数个平面，所以才出现了这么多形式。高维（4D+）就需要更抽象的工具（如旋量/geometric algebra）。

## 相关
- [[mvp-transform]] — 旋转是 view/model 矩阵的一部分
- [[coordinate-spaces]]
- [[fragment-shader]]
- [[xor-shader-artist]]
- [[shader-vector-math-primer]] —— shader 向量运算的几何直觉（dot/cross/normalize）
- [[exponential-map-rotations]] — 用矩阵指数 / 对数把四种表示串起来，并支持 Karcher mean 平均一组旋转
- [[matrix-scale-drift]] — Matrix4x4 存 rotation+scale 的数值稳定性陷阱

## Sources

- [[sources/xor-mini-3d-rotation]]
- [[sources/slater-exponential-rotations]] — Max Slater 用 $\exp/\log$ 把 Rodrigues 公式推到李代数视角
- [[sources/3dgep-math-primer-matrices]] —— 给出绕 X/Y/Z 轴的标准 4×4 旋转矩阵和 Rodrigues 形式的展开
- [[sources/xor-mini-rotation]] —— Xor 2022 年讲 2D 旋转推导与 3D 按对轴叠加的前置教程
- [[sources/boris-quaternions-game-dev]] — Boris 的游戏开发实用视角：不需要理解理论，掌握 API 语义即可
