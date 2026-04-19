---
tags: [source, graphics, rendering-pipeline, math]
date: 2026-04-19
sources: 1
---

# Different Coordinate Spaces（Apoorva Joshi）

[[apoorva-joshi]] 2025 年 1 月的短文，是对渲染管线坐标空间链的清晰重述：object → world → view → clip → NDC → screen。这是一篇**最小复述**，用来定锚 wiki 里其他讨论深度、投影、透视矫正的页面。

## 摘要

文章的骨架是一张流水图：

```
顶点流 (object-space)
  ↓ vertex shader: mul(M_mvp, v)
Clip-space (4D, 齐次)
  ↓ fixed-function: /w
NDC (3D, [-1,1])
  ↓ viewport transform
Screen-space (像素 + depth)
  ↓ pixel shader
```

作者强调：**透视除法（/w）是非线性发生的位置**。在 view → clip 的矩阵乘法里所有变换都线性，真正让「远处物体看起来小」的是 NDC 里按 w 的除法，因此 CS.z 对物体几何深度不是线性，但 CS.z / CS.w 对 NDC 深度是线性。接下来把 DirectX 风格的投影矩阵展开，验证在 near / far 平面上代入时 CS.z/CS.w 分别等于 0 和 1（reversed-Z 则交换），这是为什么**深度缓冲精度在近处高、远处低**。

## 关键要点

- 顶点着色器输出 4D clip-space，**不是** NDC——透视除法在固定功能硬件完成。
- **view-space → clip-space 是线性变换**；**clip-space → NDC 是非线性的**（除以 w）。
- near 平面对应 CS.z/CS.w = 0，far 对应 = 1（DirectX），因此 [[reversed-z]] 把它翻转以让浮点精度集中在远处。
- Fullscreen shader 可以直接从 vertex shader 输出 clip-space 坐标，跳过 IA 阶段。

## 链接到的概念

- [[coordinate-spaces]]
- [[mvp-transform]]
- [[perspective-correct-interpolation]]
- [[reversed-z]]

## 原文

- 链接：https://apoorvaj.io/ndc-clip
- 本地：`raw/articles/apoorvaj.io/2025-01-09_different-coordinate-spaces-and-how-they-relate-to-the-shade.md`
