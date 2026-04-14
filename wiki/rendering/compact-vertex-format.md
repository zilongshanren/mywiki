---
tags: [渲染, 顶点格式, 内存优化, 位压缩]
date: 2026-04-14
sources: 1
---

# 紧凑顶点格式（Compact Vertex Format）

**Compact vertex format** 是把一个顶点的所有属性按位塞进 1~2 个 32 位整数的做法。动机简单：大批量静态 mesh 的瓶颈是**内存和带宽**，而不是顶点 shader 算力；把 `vec3 pos + vec2 uv + ...` 从 28+ 字节降到 8 字节就是 3× 的 VRAM 节省和 3× 的 vertex fetch 吞吐。

## Exile 的例子：每顶点 8 字节

Max Slater 的体素引擎 Exile 里，每个面顶点是一个 `uvec2`（2 × `uint32`），8 字节：

```
uint32_t #0: [x:8][z:8][u:8][v:8]
uint32_t #1: [y:12][tex_id:12][ao0:2][ao1:2][ao2:2][ao3:2]
```

- **$x,z$（chunk 内水平坐标）8 bit 各**：因为 chunk 只有 $31 \times 31$，而 $x, y$ 都乘以 8（支持 1/8 格的顶点捕捉），所以 $31.875 \times 8 = 255$ 正好是 8 bit 范围。
- **$u, v$ 8 bit 各**：贪心合并出的大 quad 可能覆盖 31 × 31 格，所以纹理重复次数也要到 255。
- **$y$ 12 bit**：chunk 高度 511 格 × 8 = 4088，需要 12 bit，所以 chunk 最大高度由此反推成 511。
- **tex_id 12 bit**：最多 4096 张纹理，比 array texture 的硬件上限（~2048）还高一点，预留切换 bank 的空间。
- **ao0~ao3 各 2 bit**：每顶点保存所属 quad **全部** 4 个顶点的 AO 等级——这样 [[voxel-ambient-occlusion|AO]] 可以在片段着色器里做双线性插值而不依赖 GPU 三角形重心。

总共 64 bit，跟一个 `uvec2` 恰好对齐。

## 解包在 vertex shader

解包是一串 `>>` 和 `&` mask。因为 Exile 把每个 quad 以**实例化四顶点三角带**的方式提交——每个实例 4 个 `gl_VertexID`，从 instance attribute 中取对应的打包 `uvec2`——vertex shader 可以读到所有 4 个顶点，现场算法线：`cross(v2 - v1, v3 - v1)`。法线不需要存，因为体素 quad 必然轴对齐。

## 权衡

- **位数不够的坑**：32 chunk 会让 $x/z$ 溢到 256（8 bit 不够）。Exile 因此选 31——「接口被硬件限制暴露」的典型 [[information-leakage]] 案例。
- **解包成本**：shader 里多几条 mov / shift，相对节省的带宽 / cache miss 可以忽略。
- **和 geometry shader 的对比**：完全只存 face origin + size 的方案更紧凑，但 geometry shader 性能在很多 GPU 上糟糕——实践上「适度紧凑的静态 mesh」比「极度紧凑的 GS 生成」快。

## 更一般的原则

「把固定取值范围的属性量化到最少位、拼到对齐的整数里」是图形里的一个 folklore：normal 压成 oct32（2 × int16）、tangent bitangent 用符号压到单个 byte、bone index 用 uint8。核心是**让内存带宽而不是计算成为你的朋友**。

## 相关

- [[greedy-voxel-meshing]] — 制造这些顶点的管线
- [[voxel-ambient-occlusion]] — 为什么 4 个 AO 值都要广播
- [[cache-friendliness]] — 紧凑格式的根本动机
- [[perspective-correct-interpolation]] — 下游如何消费这些属性

## Sources

- [[sources/slater-exile-voxel-rendering]]
