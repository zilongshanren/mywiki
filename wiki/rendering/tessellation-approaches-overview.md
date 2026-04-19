---
tags: [渲染, 几何, tessellation, displacement, nanite, reyes]
date: 2026-04-19
sources: 3
---

# Tessellation 与位移贴图的可选方案

2026 年初 [[brian-karis|Brian Karis]] 在 Graphic Rants 公开了 UE5.4 **Nanite Tessellation** 设计日志。第一组三篇博文先把问题本身摊开：当一张 mesh 要动态细分并根据 shader 里的**位移函数**（displacement function）产生几何时，有哪些路可走、各自为什么不行，最终为什么落回 **Reyes 风格**的 split/dice 流水线。

## 问题的本质

位移才是艺术家面向的功能，tessellation 只是实现细节。给定一条基础三角网（Nanite mesh）和一个从 material graph 生成的 displacement shader，问题是：**如何在运行时以接近「每像素 1 三角形」的密度把表面摊出来、让它既能参与遮挡和阴影，又不要把 Nanite 原本节省的数据带宽全部吐回去**。

Karis 列出了两大类解法：

### 追踪（tracing）类

- **Shell mapping 及其后继** —— 把基础三角形沿顶点法线拉成棱柱（prism），在棱柱里沿切线空间做 ray march。缺点是棱柱很高时空间浪费严重，没有沿位移方向的加速结构。
- **Displaced Micro Maps (DMM)** —— NVIDIA 的方案，用 barycentric 空间的 quadtree 替代 ray march，但依然无位移方向加速，仍要求棱柱很浅；离线构建，和 Nanite 的"基础 mesh 可能是任意密度"冲突。
- **Thonat et al.** —— quadtree 同时约束位移方向，但假定位移是**单张纹理**能生成 minmax mipmap；shader 生成的位移不适用。可通过把 shader 结果缓存到纹理来绕过，但代价过高。

结论：追踪路走不通，回到**光栅化 + 某种细分**。

### 扩展 Nanite 簇层级（amplification within Nanite）

最优雅的想法是让 Nanite 的 [[nanite-virtualized-geometry|cluster 层级]] 既能向上简化（原本就有），又能向下"合成"更细的 cluster，省去磁盘 IO 换生成时间。Karis 解释为什么这条路最终放弃：

1. **同时需要简化与放大**。位移让原本大于一像素的三角形不再平坦、需要进一步细分；但同一张 mesh 里别处的微三角形依然要简化掉。层级不能简单地"多加几层"。
2. **adaptive tessellation 难以匹敌 quadric 简化**。offline Nanite 能把三角形按曲率智能分布，运行时生成做不到同样紧凑。
3. **位移信号未知**。displacement 是用户 shader，不是能预处理的已知数据，只能当**采样速率**近似作为误差度量；这里遇到的是**真正的 micropoly**——所有三角形都要 ≤ 1 像素，不是 Nanite 原本的"1 像素误差"目标。

因此：跳出 Nanite 框架、每帧动态细分 patch。

## Reyes 作为参考架构

Pixar 的 [[nanite-reyes-comparison|Reyes]] 是历史上第一个系统化处理 micropoly + displacement 的渲染器：**Bound → Split → Dice → Shade → Rasterize**。split 递归地把 primitive 拆到一定大小之前反复做可见性测试；dice 把足够小的 primitive 一次性网格化成 micropoly。Nanite Tessellation 是据 Karis 所知**第一个在游戏里实际 shipping 的实时 Reyes 实现**（UE5.4，Fortnite 地面），同时保持所有 Nanite 的软光栅与 [[visibility-buffer]] 管线。

## 为什么 dice 需要"Tessellation Table"

dice 阶段要把一个 patch 以**尽可能均匀的密度**切成小三角形。Karis 拒绝 D3D 硬件 tessellator 的方案——那种切法在等边三角形上做拓扑均匀的再分，但**不是密度均匀**，会多出 ~45% 冗余三角形。取而代之：

- 把每条边的 **TessFactor**（"这条边希望被切成几段"）从边长的屏幕投影 / DiceRate 得到——UE 默认 DiceRate = 2 像素；
- 离线做 [Botsch-Kobbelt 2004] 风格的 isotropic remesh，把所有 (a, b, c) 的 TessFactor 组合枚举出来，存进一张 **Tessellation Table**；
- 运行时只需查表拿到"每对 TessFactor 组合对应哪一套 barycentric 顶点 / 索引"。

表大小通过按 TessFactor 排序（"大到小"是唯一索引）从 `N³` 压到 `N(N+1)(N+2)/6`（N=16 时 4096 → 816），缓存友好。**16 bit barycentric 量化**时要把 1.0 映射到 65534（偶数）才能让 0.5 精确对齐——否则补丁之间沿边界处会裂缝。

同一张表也用于 **split**：split 选择更宽的 branching factor 比二分更好（更浅的递归树、更少 queue 往返、更均匀的子 patch）。`SplitFactor = min(TessFactor / MaxDiceFactor, MaxSplitFactor)` 经实测最优。

## 结果

Tessellation Table 的均匀密度 dicing 只产生 D3D 拓扑均匀方案 **69%** 的三角形；均匀 split 产生二分 split **68%** 的子 patch。Karis 指出这张表可脱离 UE 使用——`nvpro-samples/vk_tessellated_clusters` 已经在用。

## 相关

- [[nanite-tessellation-approach]] —— 流水线和实现细节（ClusterRasterize / PatchSplit / PatchRasterize）
- [[nanite-reyes-comparison]] —— 与经典 Reyes 的对照
- [[variable-sized-work-pattern]] —— 支撑 split/dice 的 wave 内负载均衡原语
- [[nanite-virtualized-geometry]] —— 基础几何虚拟化系统
- [[hull-domain-tessellation-urp]] —— 传统 D3D11 hull/domain 管线，作为对照
- [[brian-karis]]

## Sources

- [[sources/karis-nanite-tessellation-intro]]
- [[sources/karis-possible-approaches-tessellation]]
- [[sources/karis-how-to-tessellate]]
