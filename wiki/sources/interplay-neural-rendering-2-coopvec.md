---
tags: [source, 神经渲染, cooperative-vectors, tensor-cores, d3d12, hlsl]
date: 2026-04-19
sources: 1
---

# Adventures in Neural Rendering Part 2: Cooperative Vectors（Kostas / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 发表于 2026 年 2 月 21 日，紧接 Part 1 的"MLP inference 成本太高"，这篇用**预览版 Agility SDK 的 Cooperative Vectors API** 把 MLP 跑到 Tensor cores 上，实测在大网络 RTAO 上拿到 **173× 加速**。

## 摘要

Tensor core 动机：Volta 2017 起每 SM 放 8 颗 Tensor core，每个做 4×4 MMA（A×B + C，A/B fp16、C/D fp16 或 fp32）一个时钟做完 64 次 fma，而 CUDA core 每时钟一次 fma——单 SM 上 Tensor 512 fma/时钟 vs CUDA 64 fma/时钟，理论 8× 峰值。MLP 层的 "weights × input + bias" 本质就是 MMA，只是 vector 一般不 align 成 4×4，GPU 可以把多 warp 的输入 / bias 拼成矩阵块共用 weight。

**Cooperative Vectors** 是 [HLSL 提案 0029](https://github.com/microsoft/hlsl-specs/blob/main/proposals/0029-cooperative-vector.md)，给 HLSL 加**任意长 vector 类型** + `MulAdd` / `MakeInterpretedVector` / `MatrixRef` / `VectorRef` 等内建，实际会调 Tensor core。Agility SDK 1.717.1-preview + DXC SM6.9 + Nvidia 590.26 preview 驱动三件套。工程踩坑：

- `D3D12_SDK_VERSION` 预定义宏对 preview SDK 不生效，必须直接写 `717`
- 创建 device 前要 `D3D12EnableExperimentalFeatures` 显式开 `D3D12ExperimentalShaderModels` 和 `D3D12CooperativeVectorExperiment`
- Experimental features 会**禁用 Debug Layer**，挂了没报错
- 作者一开始用 float32 weights/biases，PSO 创建时直接崩溃没提示；最后靠 `CheckFeatureSupport` 查到 float32 matrix-vector mul **根本不支持**，换成 float16 才过
- weights / biases 要存 ByteAddressBuffer，同一 buffer 里各层起点有对齐要求：weights 每层 **128 字节对齐**、biases 每层 **64 字节对齐**
- float32 原始权重可通过 `ConvertLinearAlgebraMatrix` 命令转 float16，还能选 `MATRIX_LAYOUT_MUL_OPTIMAL` 让实现自己布局

HLSL 用法极简：`vector<TYPE,COUNT>` 长向量 + `MatrixRef<DATA_TYPE, ROWS, COLS, LAYOUT>` + `VectorRef<DATA_TYPE>` 指向 buffer，然后 `MulAdd<TYPE>(weightsRef, MakeInterpretedVector<DATA_TYPE>(input), biasRef)` 出结果，外面再套 LeakyReLU。作者 `MLP` 推理代码就是三段这样的调用。

**实测（3080 mobile, 1080p）**：

| 场景 | compute shader | Cooperative Vectors | speedup |
|---|---|---|---|
| 3-3-3-3 辐亮度 cubemap | 0.05 ms | 0.02 ms | ~2× |
| 6-3-3-1 小 RTAO MLP | 1.26 ms | 0.64 ms | ~2× |
| 6-32-32-32-1 | 30.5 ms | 0.73 ms | **41.7×** |
| 6-64-64-64-1 | 240.5 ms | 1.39 ms | **173×** |

小网络加速有限——Tensor core 吃不饱，也提示"shader 里普通的 matrix-vector 变换用 Tensor core 没意义"。网络一大就爆炸性线性扩展。GPU trace 看 Tensor core 利用率在 6-64 版本直接点亮，小版本几乎没动。compute shader 版本的 L2 throughput 被权重读爆、Tensor 版因为 shared memory（L1TEX）缓存权重而 L1TEX 吞吐高 + SM throughput 整体更高。

诚实 disclaimer：compute 版本是 naive float32 直接读 VRAM，再优化（float16 + LDS 缓 weight + 避免重复读）可能压 10×，但仍然远落后 Tensor core。

API 的坏消息：**这个形式的 Cooperative Vectors 不会正式上线**，被 [Linear Algebra Matrix](https://github.com/microsoft/hlsl-specs/blob/main/proposals/0035-linalg-matrix.md) spec 取代，预计 SM 6.10。API 形态会变，但 Tensor core 能被通用 HLSL shader 用这件事确定了。

## 关键要点

- Tensor core 本质是 4×4 MMA 硬件单元，一个时钟 64 fma，Volta 2017 起每 SM 8 颗
- MLP 层推理本质是 MMA，可被 Tensor core 天然加速
- Cooperative Vectors（HLSL 0029 提案）给 HLSL 加任意长 vector + MulAdd 内建
- 小网络 inference 加速有限（~2×），大网络（64 节点 × 3 隐藏层）能到 173×
- fp16 必需——fp32 matrix-vector mul 不支持，开发期无 debug layer 提示
- 一个 MLP 的 weights / biases 可同 buffer，分别 128 / 64 字节对齐
- `ConvertLinearAlgebraMatrix` 命令做 fp32 → fp16 硬件布局转换
- Tensor core 实现用 shared memory 缓权重，相比 compute shader 直读 VRAM 的 L2 打爆方式吞吐更高
- Cooperative Vectors preview 版不会正式发布，Linear Algebra Matrix（SM6.10）接任

## 链接到的概念

- [[hlsl-cooperative-vectors-tensor-cores]]
- [[mlp-signal-encoding-rendering]]
- [[d3d12-resource-binding]]
- [[neural-graphics-primitives]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2026/02/21/adventures-in-neural-rendering-part-2-cooperative-vectors/
- 本地：`raw/articles/interplayoflight.wordpress.com/2026-02-21_adventures-in-neural-rendering-part-2-cooperative-vectors.md`
