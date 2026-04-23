---
tags: [mipmap, 纹理, cpu优化, morton, 缓存, srgb, 空间填充曲线]
date: 2026-04-19
sources: 1
---

# Morton 序并行 Mipmap 生成：一次循环里产出整个金字塔

[[ben-supnik|Supnik]] 2016 年在 X-Plane 的 PNG → GPU 上传链路上做了一个**非递归的 CPU mipmap 生成算法**：用 Morton number（Z 序曲线）地址遍历源图，一次循环同时累加所有 mip level 的目标像素。novel 点在于**所有 mip 都直接从最高级（原图）取样，避开了传统 [[mipmap-generation-sampling|recursive downsample]] 的「传话游戏」误差**。

## 三条备选算法

对一张 256×256 图建 8 级 mipmap，三条路线：

- **Recursive**：LOD 0 → LOD 1 → … → LOD 7。读样最少（总像素 ≈ 原图 × 1.33），因为每层金字塔只从上一层 4 个 texel 做 box filter。但 LOD 7 的 1 像素实际上是经过**7 次重采样**的——从信号角度看，它位于一条越来越长的电话线末端。
- **Sequential**（每层独立从原图采）：LOD k 从原图采 $2^k \times 2^k$ 块。解决 telephone 问题，但每层都要全图扫一遍，共 8 次——严格最坏，对小图而言带宽翻了一个数量级。
- **Parallel (Morton-order)**：一次线性遍历原图，按 Morton 曲线把每个像素分派给它所属的每一层 bucket；bucket 填满时计算该层目标像素并清零。**每个源像素只读一次**。

## Morton 序是唯一能让它 work 的遍历顺序

关键约束：在访问源图第 5 个像素之前，必须**先把头 4 个像素喂完所属 bucket**——这一约束在所有 mip level 上递归。实现方法是让 x、y 地址在位层面交错（bit interleaving，即 Morton code）：

> 像素编号 87 = `01010111`₂。拆出 X=`1111`、Y=`001`，所以这是第 15 列第 1 行。前 64 个像素恰好填满左下 8×8 方块（第 3 级 mip 的第一个像素需要的全部输入），接下来 16 个走右边的 4×4，再 4 个走再右的 2×2，最后 3 个用于最高层次的 2×2，一路收敛。

如果图不是方形，超过「短边维度所需位数」的高位全部用于长边——等价于在短边维度上先把完整正方形扫完。

## 致命代价：cache-unfriendly

Morton 遍历的本质是**空间填充曲线**——它在保持空间局部性上优于行扫描，**但源图在内存里是行主序（linear layout）**，不是 Morton layout。于是 Y 方向的 bit 反复跳跃，硬件 prefetcher 完全看不懂访问模式，L2 miss 率飙升。

Supnik 用模板 trait 分离三套算法做 benchmark，两套 down-sample 任务：

| filter | recursive | sequential | parallel |
|---|---|---|---|
| raw（整数平均） | **18.4** | 72.1 | 124.9 |
| sRGB（浮点 linear + 2.4 power） | 374 | 2732 | **392** |

- **Raw**：纯数据搬运，cache 命中就是一切——recursive 碾压，parallel 被 miss 拖死。
- **sRGB**：`u8 → linear float → pow(·, 2.4)` 的解码昂贵，sequential 因为每像素解 $2^k$ 次成本爆炸；**parallel 做到「每个源像素只解码一次」**，接近 recursive 的速度，但质量更好（所有 mip 都从原图采样、无 telephone 误差）。

## 评论区的正确补充：用行序就够了

读者在评论里指出的路线更聪明：**按正常行扫描**，每进一行就更新「刚好填满的那些 bucket」。第 2 行每 2 像素填完一个 LOD 1 bucket；第 4 行同时填满两个 LOD 1 bucket 和一个 LOD 2 bucket；……通用公式是「遇到第 $2^k$ 行的每 $2^k$ 列时有 LOD $k$ bucket 填满」。

这个方案**既保留 Morton 方案每源像素只处理一次**的优势，**又保持完美 cache 线性**。Supnik 承认这点——他的原文定位是：Morton 方案在「per-pixel 解码成本远大于 data movement」这个狭义条件下有用，一般场景下 **recursive 仍是王道**。

## 为什么 X-Plane 不直接用 GPU mipgen

- X-Plane 的大多数纹理是 **precomputed DDS** 带完整 mip；统一路径要求 PNG 也在 CPU 侧带 mip。
- OpenGL 驱动的 residency 管理会优先驱逐「看起来重」的资源；如果 PNG 的 mipmap 只在 GPU 侧，驱动在 swap 时的决策会不稳定。
- 未来迁到低级 API 时，统一的 system-pool → GPU 流程更好管。
- 加载是多线程异步的，CPU 时间便宜。

这四条和 [[app-space-lock-free-simplification|应用层简化]] 同一思路：**不追求通用最优，追求「我这个引擎的实际路径最简单」**。

## 相关

- [[mipmap-generation-sampling]] — 通用 mipmap 生成与采样机制
- [[aliasing]]
- [[color-space]] — sRGB 解码成本是 parallel 方案获胜的根因
- [[ben-supnik]]

## Sources

- [[sources/supnik-simultaneous-mipmap-generation]]
