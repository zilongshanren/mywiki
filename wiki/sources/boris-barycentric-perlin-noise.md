---
tags: [source, rendering, procedural-generation, noise, barycentric-coordinates, math]
date: 2026-04-27
sources: 1
---

# Barycentric Perlin Noise（Boris The Brave）

[[people/boris-the-brave]] 发表于 2018 年 5 月的文章，提出将标准 Perlin 噪声扩展为输出 n 维**重心坐标**向量的变体，以解决多纹理混合和生物群系划分中独立噪声方案的固有缺陷。

## 摘要

标准 Perlin 噪声输出单一标量，用于两纹理混合绰绰有余。但要混合三种或更多纹理时，直接使用多个独立噪声通道会导致"全高/全低"同时出现的区域：三个通道都极大时混合结果过亮，都极小时过暗，且归一化处理后小输入对应的大缩放比例会产生噪点。Boris 的解决思路是用**重心梯度（barycentric gradient）**替换 Perlin 的随机梯度——重心梯度是分量和为零的 n 维向量，与分量和为 1 的重心点相加仍得重心点，从而整个噪声场只在标准 n 维单纯形（三角形）内部取值，自然满足"各分量非负且和为 1"的混合约束。文章还讨论了如何设置整数格点的起始值使输出严格落在三角形内，以及将该方法用于生物群系划分的应用。

## 关键要点

- **核心修改**：用分量和为零的随机单位向量替换原始 Perlin 梯度；同时为每个整数格点设一个重心基准值（而非固定为 0），保证整个噪声场输出均为合法重心坐标
- **生成重心梯度**：在 n 维超立方体内随机采样，令最后一个分量 = 1 − 其余分量之和（保证和为零），拒绝超出单位球的样本，归一化后使用
- **真实重心版本**：根据所选梯度方向计算在三角形内前进/后退的最大距离 u/v，偏移基准值和梯度的幅度，使输出的均值为 1/n 且始终在 [0,1] 内
- **生物群系应用**：取 n 维输出的最大分量即为区域归属；取前两大分量可识别过渡区域

## 链接到的概念

- [[game-development/barycentric-perlin-noise]]
- [[classic-shader-noise]]
- [[game-development/triangle-grid]]

## 原文

- 链接：https://www.boristhebrave.com/2018/05/12/barycentric-perlin-noise/
- 本地：`raw/articles/boristhebrave.com/2018-05-12_barycentric-perlin-noise.md`
