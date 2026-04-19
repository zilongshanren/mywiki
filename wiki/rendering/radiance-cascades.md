---
tags: [渲染, 全局光照, GI, raymarching, 2D, shader]
date: 2026-04-19
sources: 2
---

# Radiance Cascades（辐射度级联）

**Radiance Cascades（RC）** 是 Alexander Sannikov（Grinding Gear Games / Path of Exile 资深图形程序员）2023-2024 年提出的一种**噪声友好的全局光照算法**。核心观察叫 **[[penumbra-hypothesis|半影假设]]**：阴影半影（penumbra）在**靠近光源处需要高 linear 分辨率**（细密的像素/探针），在**远离光源处需要高 angular 分辨率**（每个探针发出更多方向的射线）——两者**反比**。RC 用一个**级联结构**直接按这个反比分配采样预算，**用有限的射线方向模拟出无限方向**，得到没有蒙特卡洛噪声、不需要时域降噪、不依赖 blue noise + bilateral filter 的干净结果。

本页整理 Yaazarai 在 GM Shaders 发表的两部分 2D 屏幕空间 RC 实现——第一部分讲几何直觉，第二部分讲**direction-first 内存布局 + pre-averaging** 这两项关键优化如何把 RC 压到一个单 shader 实现。

## 级联层级

设屏幕 `1024×1024`，一共 4 层级联：

| 级联 | 探针数 (spatial) | 每探针射线数 (angular) | 总射线 |
|---|---|---|---|
| Cascade 0 | 16×16 | 8×8（=64） | 16,384 |
| Cascade 1 | 8×8 | 16×16（=256） | 16,384 |
| Cascade 2 | 4×4 | 32×32 | 16,384 |
| Cascade 3 | 2×2 | 64×64 | 16,384 |

关键性质：**每级总射线数相同**——因此所有级联**纹理大小相同**，GPU 内存布局齐整，相邻级联之间的 merge 操作尺寸对齐。4× 比例（空间减 1/4、角度增 4x）是 Sannikov 给 2D 的最优选择，不是硬要求。

级联数上限由"射线起点不应超过屏幕对角"决定：

```
diagonal = sqrt(width² + height²)
cascadeCount = ceil(log4(diagonal / interval0))
```

超过这个层数，射线起点就跑出屏幕外、对 radiance field 没贡献。

## 射线区间：几何级数长度

`interval0` 是 cascade 0 的射线长度（接近光源处的细短射线）。每上一级，射线 **起点偏移 4×、长度乘 4×**：

```
offset_N = interval0 * (1 - 4^N) / (1 - 4)    // 几何级数和
range_N  = interval0 * 4^N
```

这样每条射线只覆盖**一个特定距离段**，所有级联的射线拼起来覆盖从光源到屏幕对角的完整范围——这就是 penumbra 假设在算法层的直接映射。

## 探针内部：把 1D 射线列表映射到 2D 纹理

每个探针发射一个**按角度均匀分布**的射线集合，但存储在 2D 纹理里。`ray_index = y * width + x` 把 2D texel 坐标翻译成 1D 射线编号，`theta = 2π * ray_index / total_rays` 给出射线角度。这个设计让 **cascade 本身就是一张 2D 纹理**——shader 里不需要特殊数据结构，一切都是 `texture2D`。

## 级联合并：bilinear 交织出无限方向

合并从最高级联向 cascade 0 反向进行：`cascadeN` 的每条射线找到 `cascadeN+1` 中 **4 个最近邻探针**的**方向匹配的 4 条射线**，按当前探针在这 4 个相邻探针中的相对位置做 **bilinear 插值**。

- 每条 N 级射线只需对 N+1 级做 16 次采样（4 probes × 4 ray directions）。
- N+1 级每条射线对应 N 级的 4 条同向射线——把这 4 条的 radiance 预先 pre-average，只要存 1 个值，合并就退化成单次 bilinear 查询。
- Bilinear 插值等价于 **"在连续方向上积分"**——这就是"有限射线方向模拟无限方向"的出处。

合并时使用 **ray visibility term**：raymarch 结果里 alpha = 0 表示射线命中了表面（有实际 radiance），alpha = 1 表示未命中（需要从上级借 radiance）。只对 alpha=1 的射线做合并——否则会在 occlusion 边缘把上级的亮度错误地传播进阴影区。

## 最终合成：把 cascade 0 展平成 radiance field

合并完所有级联后，cascade 0 的每个 texel 包含完整方向积分后的 radiance。把 cascade 0 按**每个探针的所有射线求平均**降到探针分辨率，硬件双线性采样上采样到屏幕——结果就是 per-pixel GI。

## 实现陷阱（Part 2）

第二部分记录了 Part 1 实现的三类问题和修复：

### 1. Pre-averaging：75% 内存/带宽节省

如果你最终都要平均 4 条同向射线，为什么要分开存？**发 4 条射线，立即平均，只存 1 个值**——内存和 merge 采样数同时减 75%。这改变了"每 texel 存一条射线"的朴素布局：现在每 texel 存的是 "4 条同向射线的平均"。

### 2. Direction-First 布局 + 硬件插值

原版"position-first"布局（每个内存块代表一个探针，块内 texel 是不同方向）在 merge 时要对 4 个探针各做 1 次采样、共 4 次。

**Direction-first** 把布局翻过来：每个内存块代表"同一方向的一组射线，分别来自不同探针"。把 GPU 的**双线性插值**打开，对邻近 4 个探针做一次采样就得到加权平均——**4 次合并采样降到 1 次**，再叠上 pre-averaging（已经把 4 条同向射线合为 1）——总合并采样从 16 降到 1。

> 作者在 2024-07 修订时加了一条更新：*在他当年的 GameMaker 版本里 direction-first 其实因为引擎 bug 反而慢*；但这个布局**调试友好**（可以直接可视化任何方向的所有采样）——工程上还是值得用。

### 3. Light Leak Fix

级联间的空间过渡会在 merge 边界产生**微小的光泄漏**。修复方式：把每级射线长度**额外加一点 overlap**（`range += length(cascadeN+1 probe spacing)`）让相邻级联覆盖段微微重叠。

## 和朴素采样的对比：为什么 RC 不一定更快

Part 2 的评论区有一个值得记下的观察：**6 级 cascade × 4 rays ≈ 每像素 24 射线**——这和"每像素随机撒 24 条射线 + blue noise + bilateral filter"在**总射线数**上几乎一样。实际上在有些机器上 **朴素采样 GPU 占用 70%，RC 只占 40%**，另一些机器上 RC 反而更慢。原因：

- RC 的**内存访问模式**（多级纹理 read/write + merge pass）对 GPU 纹理缓存更友好——密集空间局部性。
- 但多 pass 和 direction-first 布局也引入了额外 bandwidth。
- **最终 GPU-bound** 的胜负取决于硬件：cache 小、带宽大的 GPU 上 RC 优势明显；桌面 RTX 上差距可能被访存并行吃掉。

**RC 的真正价值在于"免噪声"**——没有时域降噪、没有 SPP scaling、软 penumbra 开箱即用。这让它在 2D 游戏和实验性 3D demo 里特别有吸引力。

## 相关

- [[penumbra-hypothesis]] —— 算法背后的几何观察
- [[jump-flooding-algorithm]] —— 2D RC 常用 JFA 生成 SDF 做 raymarch
- [[instant-radiosity-vpl]] —— 另一种 GI 方案（基于 virtual point lights，不是级联）
- [[sparse-shadows-cone-tracing]] —— 概念谱系相近（多级角度采样）
- [[temporal-antialiasing]] —— 朴素 GI 需要它，RC 不需要
- [[poisson-disk-sampling]] —— 朴素 GI 的 blue noise 抖动
- [[bilinear-sample-blur-optimization]] —— merge 阶段利用硬件双线性采样的同思路
- [[alexander-sannikov]] —— 算法提出者
- [[alex-yaazarai]] —— GM Shaders 实现与教程作者

## Sources

- [[sources/yaazarai-radiance-cascades]]
- [[sources/yaazarai-radiance-cascades-2]]
