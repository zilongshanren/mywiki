---
tags: [渲染, 数学]
date: 2026-04-05
sources: 1
---

# 坐标空间（Coordinate Spaces）

渲染中顶点依次经过的坐标系列，每一个空间存在是为了某个操作的**数学简单性**。

| 空间 | 用途 | 特征 |
|---|---|---|
| **Model Space** | 资产可复用 | 本地原点 |
| **World Space** | 物理、光照 | 首个绝对意义的空间 |
| **View Space** | 投影数学简化 | 相机在原点，朝 -Z |
| **Clip Space** | 统一剪裁 | 齐次坐标，透视除法前 |
| **NDC** | API 无关 | 标准范围 [-1,1] |
| **Screen Space** | 像素位置 | 最终输出 |

## 每个空间存在的理由

- **Model Space**：不同缩放/位置的同一个资产能共享顶点数据。
- **World Space**：物理世界需要绝对坐标；灯光和阴影需要在这里计算；是第一个**所有物体共享**的坐标系。
- **View Space**：相机在原点简化投影矩阵；z 分量直接表示深度。
- **Clip Space**：剪裁使用**固定的单位立方体**（齐次 w=1 时 [-1,1]³），硬件剪裁算法不需要关心 frustum 形状。
- **NDC**：不同图形 API 的标准化中间表示。
- **Screen Space**：从 NDC 映射到视口像素。

## 关键操作发生的位置

- **MVP 变换**：见 [[mvp-transform]]。
- **剪裁**：Clip Space 进行，**透视除法前**（避免 w≈0 数值问题）。
- **插值**：光栅化阶段，屏幕空间线性但对应 3D 空间非线性，需要 [[perspective-correct-interpolation|透视校正]]。

## 相关

- [[mvp-transform]]
- [[rendering-pipeline]]
- [[z-buffer]]
- [[perspective-correct-interpolation]]

## Sources

- [[sources/rtr-day03]]
