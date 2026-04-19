---
tags: [神经渲染, MLP, 信号编码, 渲染研究]
date: 2026-04-19
sources: 2
---

# MLP 作为渲染信号编码器

小 MLP（Multi-Layer Perceptron）可以像 [[spherical-harmonics|Spherical Harmonics]] 或 octahedral 映射一样**编码方向性信号**——辐亮度、辐照度、深度、BRDF——只不过是"学"而不是"解析"的方式。[[kostas-anagnostou|Kostas Anagnostou]] 2026 年系列博客里用小网络实测了在同等存储下 MLP vs SH 的表达力 trade-off，也发现了 compute shader inference 的硬墙（引出 [[hlsl-cooperative-vectors-tensor-cores]]）。

## 工程骨架

- 层 weights / biases 静态声明大小，ByteAddressBuffer 存
- 激活函数 LeakyReLU（alpha 0.01）比 ReLU 收敛快
- 训练用 Adam，GPU 侧做 forward / back-prop 循环
- inference 推理三层嵌套循环（层 × 节点 × 输入）

## 实验对比（同级别存储量）

| 信号 | MLP 胜 | SH 胜 | 备注 |
|---|---|---|---|
| Cubemap radiance | ✓ (24 floats vs 27) | | 3-3-3 MLP 方向性更清晰 |
| Irradiance (smooth 球) | ≈ | ≈ | 差距小 |
| Irradiance (normal-mapped) | | ✓ | 小 MLP 方向性不够，floor bounce 漏到墙砖 |
| Depth over sphere | 压缩比 ≈3× (134KB vs 393KB) | | 但 inference 44ms (3080 mobile) |
| RTAO 单视角 | 能学 | | 换视角回来会忘 |
| Specular BRDF | 靠**参数化**（Rusinkiewicz）能拟合 | | 直接喂 N/L/V/F0/rough 会失败 |

## 关键结论

- **输入参数化比网络大小更重要**。BRDF 用 Rusinkiewicz（half vector 参考系）+ 各向同性 phi_h=0，3-32-32-3 都能抓 specular lobe
- **辐亮度 / 深度适合 MLP**（方向性丰富的信号）
- **辐照度适合 SH**（已经被半球 cos 滤过，低频、SH 基函数天然匹配）
- **AO 空间信号不是 MLP 强项**——试图用 MLP 做 whole-scene AO 缓存会失败，local spatial cache（如 [[spatial-hash-rtao-cache]]）更自然
- **Compute shader inference 是硬上限**：6-32-32-32-1 → 30ms，6-64-64-64-1 → 240ms，不可实时
- 大网络的内存开销 weights/biases 几十~几百 KB 起跳，需要压 float16

## 走出 compute 的路

压缩 shader MLP 的方向上常见优化：float16 存储、LDS 缓权重、避免重复读、合并 branch。Kostas 实测这些叠加"大概也就 10× 压成本"。真正的突破在硬件：走 Tensor core / Matrix core → Cooperative Vectors（HLSL）/ 未来的 Linear Algebra Matrix spec（SM6.10），**大网络可以 100×+ 加速**，见 [[hlsl-cooperative-vectors-tensor-cores]]。

## 相关

- [[hlsl-cooperative-vectors-tensor-cores]]
- [[spherical-harmonics]]
- [[neural-graphics-primitives]]
- [[microfacet-brdf]]
- [[spatial-hash-rtao-cache]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-neural-rendering-1-mlp]]
- [[sources/interplay-neural-rendering-2-coopvec]]
