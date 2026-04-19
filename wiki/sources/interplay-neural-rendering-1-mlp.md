---
tags: [source, 神经渲染, MLP, 辐照度, BRDF, 渲染]
date: 2026-04-19
sources: 1
---

# Adventures in Neural Rendering Part 1: MLPs in Rendering（Kostas / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 发表于 2026 年 2 月 10 日，一个资深图形程序员（自称无 NN 背景）从零把小 MLP 当成可训练的信号编码器接入实时渲染的各种场景——cubemap 辐亮度 / 辐照度、球面深度、RTAO 缓存、specular BRDF——用 compute shader 做 inference，实测"相似存储成本下 MLP vs L2 SH"的表达力 trade-off。

## 摘要

背景：NN 在 AA / upscaling / texture compression / material 表达 / 间接光里越来越常见，作者想亲自摸一摸。MLP 基础：全连接层、每节点对上一层做加权和 + bias、过激活函数（用 [LeakyReLU](https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html)、alpha=0.01）。实现上 compute shader 里 weights / biases 存 ByteAddressBuffer、LAYER_COUNT / NODE_COUNT 静态定义避免动态循环、实现 Adam 优化器做训练。

**实验 1：Cubemap 辐亮度编码**（输入=normal xyz，输出=rgb）。3-3-3 MLP 用 24 floats 就能编码出比 L2 SH（27 floats）更清晰的方向性。减到 2 节点隐藏层（17 floats）还保留大致方向性但引入色偏；1 节点（10 floats）接近 L2 SH 粗糙度但色偏不可用。结论：**同等存储下 MLP 编码辐亮度好于 L2 SH**。

**实验 2：辐照度**（用 Monte Carlo 作 ground truth 训练）。3-3-3 MLP 接近但不如 L2 SH 准确。换上 normal map 后差距明显——小 MLP 的方向性不够，floor bounce 会"漏"到墙砖正面。要追上 L2 SH 得 2 层 × 4 节点的 51 floats，**明显不如 L2 SH 27 floats 的密度**。**辐照度是"滤波过"的光信号，MLP 和 SH 谁更擅长很依赖场景**——辐亮度 MLP 赢、辐照度 SH 赢。

**实验 3：球面深度**（raytrace GT，depth cubemap 替代品）。3-3-3-1 太粗。3-32-32-32-1 开始看出结构。3-128-128-128-1 ≈ 33.7k floats（134KB）能用，小 depth cubemap 128×128×6 要 393KB——**MLP 确实压缩**，代价是 **44ms inference**（3080 mobile），compute shader 无可救药。

**实验 4：RTAO 缓存**（6-32-32-32-1 / 6-64-64-64-1）。单视角 AO 能学，但换视角回来 MLP 忘掉了；不像直接体素缓存。更大网络+更多训练时间也许可以，但 compute shader 的 240ms 直接劝退。

**实验 5：Cook-Torrance specular BRDF**。13-128-128-128-3 直接喂 (N / L / V / F0 / roughness) 都逼不出 specular lobe，尤其低 roughness。换成 **Rusinkiewicz 参数化**（以 half vector 为参考，各向同性 BRDF 的 phi_h 等于 0），3-64-64-64-3 就能抓住 lobe 主体，3-32-32-3 都能大致拟合。**输入参数化**对收敛比网络大小影响更大——这是神经 BRDF 文献的共识，作者亲自验证。加回 F0 / roughness 后又退化，需要更多训练时间。

结论偏诚实：MLP 实现简单、跑通容易，但**参数旋钮太多**（层数 / 节点数 / 激活函数 / loss / 训练时间）且训练要等。编码辐亮度 / 压缩深度贴图等场景有潜力，但 compute shader inference 成本禁止实时用——指向 Part 2 的 Cooperative Vectors / Tensor core。

## 关键要点

- 3-3-3 MLP 编码辐亮度 24 floats 好于 L2 SH 27 floats
- 辐照度信号 SH 赢 MLP，尤其是在 normal-mapped 表面上
- 深度 cubemap 用 MLP 能压缩到原来的 1/3，但 inference 成本太高 compute shader 不可实时
- MLP 做 AO 缓存在单视角可用、换视角忘得快，数据驱动缓存更简单
- BRDF 编码关键不是网络大小而是参数化选择——Rusinkiewicz（半向量）让各向同性 BRDF 收敛大幅变好
- 固定 roughness / F0 的单材质 BRDF 能拟合；通用版本需要大网络 + 长训练
- LeakyReLU + Adam 优化器收敛比 ReLU + 普通 SGD 好
- 静态声明 LAYER / NODE 帮助编译器展开循环
- compute shader inference 是实时应用的硬瓶颈——引出 Tensor core 讨论

## 链接到的概念

- [[mlp-signal-encoding-rendering]]
- [[neural-graphics-primitives]]
- [[spherical-harmonics]]
- [[microfacet-brdf]]
- [[spatial-hash-rtao-cache]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2026/02/10/adventures-in-neural-rendering/
- 本地：`raw/articles/interplayoflight.wordpress.com/2026-02-10_adventures-in-neural-rendering.md`
