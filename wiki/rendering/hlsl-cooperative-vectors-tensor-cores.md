---
tags: [hlsl, tensor-cores, cooperative-vectors, d3d12, 神经渲染]
date: 2026-04-19
sources: 1
---

# HLSL Cooperative Vectors 与 Tensor Core

通用 HLSL shader 访问 Nvidia Tensor core / AMD Matrix core 的 API 入口。Cooperative Vectors 是 [HLSL 提案 0029](https://github.com/microsoft/hlsl-specs/blob/main/proposals/0029-cooperative-vector.md)，2026 年通过 Agility SDK 1.717.1-preview + DXC SM6.9 + Nvidia 590.26 驱动放出 preview。**这个形态不会正式发布**（被 Linear Algebra Matrix 提案取代，预计 SM 6.10），但它是神经渲染走出 compute shader inference 硬墙的关键 enable。[[kostas-anagnostou|Kostas Anagnostou]] 2026 年做过受控实验。

## Tensor Core 的动机

- Volta 2017 起每 SM 放 8 颗 Tensor core
- 每颗做 **4×4 MMA**：A·B + C = D，A/B 必 **fp16**，C/D 可 fp16/fp32
- 一个时钟完成 64 fma；CUDA core 每时钟 1 fma
- 单 SM 理论峰值 Tensor 512 fma/时钟 vs CUDA 64 fma/时钟，**8× 上限**
- MLP 层的 "weights × input + bias" 本质就是 MMA，天然匹配

## API 形态

HLSL 新增：

```hlsl
// 任意长 vector 类型
vector<float16_t, NODE_COUNT> inputVector = { ... };

// buffer 引用类型
MatrixRef<DATA_TYPE_FLOAT16, ROWS, COLS, MATRIX_LAYOUT_MUL_OPTIMAL>
    weightsLayer = { weightsBuffer, weightsOffset, 0 };
VectorRef<DATA_TYPE_FLOAT16> biasLayer = { biasesBuffer, biasesOffset };

// MMA 内建
vector<float16_t, LAYER_N> layer =
    MulAdd<float16_t>(weightsLayer,
                      MakeInterpretedVector<DATA_TYPE_FLOAT16>(inputVector),
                      biasLayer);
layer = select((layer >= 0.0), layer, layer * LEAKY_RELU_SLOPE);
```

MATRIX_LAYOUT_MUL_OPTIMAL 让实现按硬件选最佳布局（行列主序或 tile swizzle）。

## 踩坑清单

- `D3D12_SDK_VERSION` 宏对 preview SDK **不生效**，直接写 `717`
- 创建 device 前 `D3D12EnableExperimentalFeatures` 显式开 `D3D12ExperimentalShaderModels` + `D3D12CooperativeVectorExperiment`
- **Debug Layer 被禁**——PSO 创建失败直接崩不报错
- **fp32 matrix-vector mul 根本不支持**，必须 fp16 权重；查清楚要看 `CheckFeatureSupport(D3D12_FEATURE_COOPERATIVE_VECTOR)` 返回的合法组合
- weights / biases 同 buffer 时**逐层对齐**：weights 128 字节、biases 64 字节
- fp32 原始权重转 fp16 用 `ConvertLinearAlgebraMatrix` 命令，`D3D12_LINEAR_ALGEBRA_MATRIX_CONVERSION_INFO` 填好源目标布局 / 类型，`GetLinearAlgebraMatrixConversionDestinationInfo` 返回对齐后的 DestSize

## 实测加速（3080 mobile, 1080p）

| 网络 | compute shader | Cooperative Vectors | speedup |
|---|---|---|---|
| 3-3-3-3（小辐亮度编码） | 0.05 ms | 0.02 ms | 2× |
| 6-3-3-1（小 RTAO） | 1.26 ms | 0.64 ms | 2× |
| 6-32-32-32-1 | 30.5 ms | 0.73 ms | **41.7×** |
| 6-64-64-64-1 | 240.5 ms | 1.39 ms | **173×** |

- 小网络加速有限：Tensor core 吃不饱——**shader 里零星的 matrix-vector 变换用 Tensor core 无意义**
- 大网络爆炸性线性扩展；GPU trace 看 Tensor 利用率几乎打满
- compute 版本 L2 throughput 被权重读爆；Tensor 版走 shared memory (L1TEX) 缓权重，L1TEX 吞吐高 + SM throughput 高

## 后续

Cooperative Vectors preview 被 [Linear Algebra Matrix](https://github.com/microsoft/hlsl-specs/blob/main/proposals/0035-linalg-matrix.md) 提案取代（SM6.10）。API 细节会变，但"通用 shader 访问 Tensor core"这件事确定了——[[mlp-signal-encoding-rendering|神经渲染]] 的实时门槛从此可以降到可接受区间。

## 相关

- [[mlp-signal-encoding-rendering]]
- [[neural-graphics-primitives]]
- [[d3d12-resource-binding]]
- [[gpu-utilisation-holistic-tuning]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-neural-rendering-2-coopvec]]
