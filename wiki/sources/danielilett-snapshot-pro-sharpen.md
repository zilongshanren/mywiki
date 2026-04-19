---
tags: [source, 渲染, unity, urp, 后处理, sharpen]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Sharpen（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Sharpen 锐化后处理的唯一参数。

## 摘要

Sharpen 是 *Snapshot Shaders Pro* 里最简的一个后处理：把画面变"不那么糊"。产品面板只暴露一个参数 `Intensity` 控制锐化强度。底层数学是 [[sharpen-filter|经典 unsharp mask]]——原图减去自身的模糊版本得到高频残差，按 `Intensity` 乘回去；等价地也可以写成一张 3×3 sharpen 卷积核（中心 `1+4k`、四邻 `-k`）。Pro 版把半径、模糊类型、kernel 形状全部锁死，只留一个滑块，是"风格化后处理"UI 极简设计的典型样本。

## 关键要点

- 唯一参数 `Intensity` —— unsharp mask 公式中的 `k`
- 产品把模糊 pass 的实现（box / 高斯 / 半径）都锁死了——换取面板零学习成本
- 实时用途：TAA / DRS / 上采样之后做"找回锐度"的补偿
- 配色阶量化风格化后处理（[[color-quantization-retro]]）时**不该叠**——会让色块边缘长出振铃

## 链接到的概念

- [[sharpen-filter]]
- [[image-convolution-kernel]]
- [[convolution-separability-blur]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/sharpen/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-sharpen.md`
