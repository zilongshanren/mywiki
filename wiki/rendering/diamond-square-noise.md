---
tags: [noise, heightmap, compute-shader, procedural, fbm]
date: 2026-04-14
sources: 1
---

# Diamond-Square 噪声

Diamond-Square 是 1982 年提出的有界噪声算法，输入一张 2D 灰度种子纹理，输出同分辨率的高度图，适合做地形 base heightmap 再叠加侵蚀等效果。它的性格与 Perlin/Simplex 类「理论上无限域」的噪声不同：

- **定义域强制为正方形且边长必须是 `2^n + 1`**——依赖递归二分，尺寸一旦定下就不能无缝平移。
- **需要持久状态**——每个像素采样自已经写入的邻居，因此不是无状态函数，不适合 shader toy 里纯片元着色器的一次性实现。
- **可控性极高**——种子纹理让美术或关卡设计者直接「这里来座山，那里来个湖」地指定大形态，算法只在细节上随机化。
- **速度一般偏慢**——大量自采样，单线程 C# 跑 8192² 接近 13 秒，是 [[layered-grid-noise]] 之外的另一条噪声路径。

算法是一个标准的 [[fbm]] 外层循环，但与逐像素蒸煮的噪声不同：每个 iteration 按步长 `Dimensions/2, /4, /8 …` 只 touch 一部分像素。每次 iteration 先跑 **Diamond**（采 4 个对角邻居，取平均 + 随机偏移），再跑 **Square**（采 4 个边邻居，取平均 + 随机偏移），然后步长减半、振幅按 persistence 衰减，直到步长为 1。随机偏移范围随振幅一起衰减，这是它还能被视作 FBM 的关键。

## 从 Fragment 到 Compute：状态依赖的着陆点

Steven Sell 给出了三种实现并做了性能对比（8192²）：

| 实现 | 时间 (ms) |
|---|---|
| 单线程 C# | 13042 |
| 多线程 C#（128² chunk） | 3121 |
| GPU compute shader | 778 |

GPU 版相对单线程提速约 17 倍。作者先后尝试过三次 GPU 化：ShaderToy 的 fragment shader 版因为无法保持跨 iteration 的可写状态而失败；Unity 双缓冲 render target 版本因为 fragment shader 里「精确像素寻址 vs 插值浮点」的 fuzziness 导致与 CPU 版永远差一点；最终用 compute shader 干脆利落地跑通，因为 compute 可以在 [[cuda-memory-hierarchy]] 风格的 structured buffer 上精确索引。值得记住的 takeaway 是：**GPU 版约一半的耗时花在把最终 buffer 从 GPU marshal 回 CPU**——算法本身很快，瓶颈转到了 readback。这也是为什么它依然不适合逐帧生成，但对「一次性或低频生成基础地形」已经绰绰有余。

在更大的 noise 家族里，Diamond-Square 属于「有状态、bounded、用户可控」这一支，跟 [[layered-grid-noise]] 那种无状态叠加的噪声、[[poisson-disk-sampling]] 那种点集分布都不在一条路径上。它的适用场景非常具体：地形 heightmap 的 greybox 层。

## Sources

- [[sources/vertexfragment-diamond-square-gpu]]
