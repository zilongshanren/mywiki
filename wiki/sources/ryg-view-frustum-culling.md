---
tags: [source, 渲染, 剔除, simd, spu, ryg]
date: 2026-04-14
sources: 1
---

# View frustum culling（ryg / The ryg blog）

[[fabian-giesen]] 在 2010 年 10 月对 Zeux 的 view frustum culling 优化系列的长篇回应。出发点是 Zeux 那句「我没实现 p/n-vertex，但我确信它不会更快」——ryg 直接从 8 顶点 × 6 平面的 baseline 一路演化到 SPU 上 ≈24 cycle/box 的 SIMD 实现，证明 p/n-vertex 路线可以比 clip-space 路线快一倍以上。

## 摘要

文章把 AABB-vs-frustum 的所有经典做法整理成一条方法链。**Method 1** 是世界空间逐顶点逐平面；**Method 2** 是把顶点变换到 clip space 再用简单的 `|x|,|y|,|z| ≤ w` 比较；**Method 2b** 通过公共子表达式把乘法数 4× 降低（非 FMA 平台才划算）；**Method 3** 扔掉 z 分量做偏齐次变换，再降 25%；**Method 4** 是 p/n-vertex——只看「沿轴最内侧/最外侧」顶点，等价于 `max(min·p, max·p)` 沿每轴独立取最大再相加；**Method 4b** 用 center/extent 表示法 + absPlane 把整件事压成 12 个 dot product 测 6 个平面（对比 Method 3 的 24 个）；**Method 5** 放弃 inside/intersecting 二态，用 IEEE float 的符号位做 xor 把两个 dot product 合成一个，最终只需 6 dot + 6 add + 6 xor + 6 compare。SIMD 实现部分给出 SPU 伪代码，4 个 box 并行时 ≈95 cycle，即每 box ≈24 cycle，是 Zeux 原版理论下限的一半多。ryg 在文末承认这个 cycle 对比不够公平——Zeux 的版本顺手算了 world-view-projection 和 clip-space 顶点，如果你本来就需要这些中间量，齐次路线并不亏。

## 关键要点

- p/n-vertex 测试的本质：8 个 dot product 沿三轴独立取 max，可折叠成 `dot(center, plane) + dot(extent, absPlane)`
- 12 dot product vs 24 dot product：p/n-vertex 比 clip-space 路线理论乘加数少一半
- 用 center/extent 表示 AABB 后，**absPlane 对一组 box 只需算一次**（它是 plane 的 componentwise abs）
- 省内循环 `0.5` 的小 trick：`center = min+max`、`extent = max-min`，代价是对比基准要预乘 2
- 终极压缩：抽出 `plane & 0x80000000` 和 extent 做 xor，把两个 dot 合成一个 → 6 dot + 6 add + 6 xor + 6 compare
- **SIMD 最优策略**：一次测 4 个 box，储存 6 个向量 × 4 box 的 SoA 格式
- SPU 实现每 box ≈24 cycle，是 Zeux 原版理论下限的 ~1/2
- 代价：不同时计算 clip-space 坐标；需要额外转换若后续还需要 world-view-projection

## 链接到的概念

- [[view-frustum-culling-ryg]]
- [[culling]]
- [[sse-tricks]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/10/17/view-frustum-culling/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-10-17_view-frustum-culling.md`
