---
tags: [渲染, 浮点精度, 大世界, opengl, x-plane, 顶点抖动]
date: 2026-04-27
sources: 1
---

# 大世界单精度浮点 Pre-Offset 技术

当引擎无法依赖 GPU 的 64-bit 浮点（fp64），而世界坐标又大到让 32-bit float 产生可见抖动时，一种无需移动 mesh 数据、也无需修改 tile 粒度的方案：**在 vertex shader 执行变换之前，先在世界坐标中减去一个稳定的偏移量**。

[[ben-supnik]] 在 X-Plane 11.10 中实现并总结了这套技术。

## 为什么会抖动

32-bit float 的尾数只有 23 位（约 700 万有效数字）。当顶点坐标达到 50 km 量级（1.5×10⁷ 量级），精度约为 1 cm，而离地近看时 1 个屏幕像素可能只对应 1 mm——这意味着摄像机轻微移动时，顶点在 clip space 中会以 >1 像素的步长跳跃。

根本原因是 MVP 变换要做两个大量的**精确抵消（cancellation）**：顶点坐标旋转 + 摄像机偏移旋转，两者求和后的余量应该只是「顶点在 view space 中的小偏移」。两个大量都经过 GPU fp32 旋转之后相加，低位信息已经丢失，抵消剩余量不稳定。

## 解决思路：把大量消掉再旋转

标准变换顺序：`v_eye = v_world * MV`，其中 MV 的平移分量隐含着将「大 world 坐标」搬到「小 eye 坐标」的大偏移。

Pre-offset 方案改变操作顺序：

```
v_eye = (v_world - O) * MV'
```

其中 `O` 是一个**网格对齐的静态偏移**（例如以 4 km 为粒度对摄像机位置取整）。这样 `v_world - O` 的量级与「顶点到 offset 中心的距离」相当，通常只有几 km 甚至几百米，远离摄像机的顶点本来就对像素精度无要求，抖动自然消失。

## CPU 端算法

给定 CPU 上 double precision 的 model-view 矩阵（R 为旋转，T 为平移）：

```
C       = transpose(R) * T          // 反变换出摄像机在世界坐标中的位置
C_snap  = grid_round(C)             // 网格取整（4 km 粒度）
T      -= R * C_snap                // 补偿矩阵平移，使其与 pre-offset 自洽
O       = -C_snap                   // Shader 端需要的 pre-offset
```

Shader 代码：`v_eye = (v_world - O) * modelview_matrix`

CPU 端只需对自己的变换栈升级为 double（吃 CPU 代价，不影响 GPU）；矩阵最终截断为 float 发送到 GPU。

## Hardware Instancing 的处理

若引擎有 hardware instancing，实例化矩阵同样包含世界坐标平移，直接减去 `C_snap` 即可：

```
instance_transform.translation -= C_snap
```

这样实例在世界坐标展开后已接近摄像机，不再有大量抵消问题。

## 与其他方案的比较

| 方案 | 是否需要 fp64 GPU | 是否需要拆分 mesh | 适用场景 |
|------|:-----------------:|:-----------------:|---------|
| GPU fp64 | 是 | 否 | 仅桌面高端 GPU |
| 拆小 tile | 否 | 是 | 改造成本高 |
| double scene graph + 只 draw 时转 float | 否 | 否 | 简单，精度略低 |
| **Pre-offset（本技术）** | **否** | **否** | 适合已有大 tile 引擎 |

Pre-offset 的关键约束：GPU 端**必须按「先减 offset 再乘 MV」的顺序执行**，驱动对运算顺序优化敏感，`precise`/`invariant` qualifier 不足以保证，必须代码结构本身就是正确顺序。

## 相关

- [[huge-world-coordinate-precision]] — 大世界坐标精度问题的更广泛讨论，含 stop-the-world 与 tile-local-space 方案
- [[coordinate-spaces]] — MVP 变换的标准层次
- [[gpu-latency-microbench-methodology]]

## Sources

- [[sources/supnik-camera-shake-float-precision]]
