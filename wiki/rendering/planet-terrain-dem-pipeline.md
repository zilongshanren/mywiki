---
tags: [行星渲染, 地形, dem, srtm, fractal, outerra]
date: 2026-04-19
sources: 2
---

# 行星尺度 DEM 数据管线（Outerra 的 SRTM / NasaDEM 实践）

把一整颗地球放进运行时地形引擎，**原始 DEM 的质量上限决定了视觉上限**。Outerra 的数据管线做的事情本质是：拿全球公开数据（SRTM 1″/3″、NasaDEM、Viewfinder Panoramas、bathymetric）→ 重投影到 quad-sphere 网格 → 按目标分辨率（OT 里常见的 38m / 76m）做 fractal resample → 剩下的小尺度细节在运行时由 procedural refinement 接管（与 [[diamond-square-noise]]、[[fractal-texturing]]、[[erosion-filter-procedural]] 同源的思路）。

## 分辨率记号

Outerra 2015 年切换到 30m SRTM 时用的是 `A/B` 记号——`A` 是输出分辨率、`B` 是数据源分辨率：

- `76/90` 老版本：76m 输出，源是 90m SRTM3，等价一次双线性下采样。
- `76/30`：76m 输出，但源是 30m SRTM1 做 fractal resample。**尺寸不变，观感显著优于 `76/90`**。
- `38/30`：38m 输出，数据量约从 12.5GB 涨到 39GB（3×）。细节再加一档，但 procedural refinement 会在 `38/30` 上**过响应**，在雪地等平坦区域产生人为小凹坑——说明「真实数据 + 程序化细分」的尺度接缝需要仔细调。

结论：**数据源分辨率比输出分辨率更重要**。从 90m 升到 30m 源，即便输出维持 76m 也能拿到大部分视觉收益，数据量几乎不变。

## SRTM 源的系统性问题

- **空间低通**：30m SRTM 数据本身被明显平滑过；叠加引擎侧的 procedural refinement 后，原应存在的山脊高频被提前滤掉了。Outerra 考虑用「crest sharpening filter」在数据入库时先锐化山脊再存，而不是指望运行时补。
- **空洞与假值**：SRTM 采集期间常年云层覆盖的区域（西南亚、东北非、热带雨林）有大量 void 和人工平面。90m 数据集做过较彻底的人工修补；30m 数据集保留了更多问题。
- **城市偏高**：大城市/大型建筑被「烘进」高程里（肯尼迪航天中心的 VAB 尤其明显），30m 下变得更扎眼。解决方案是叠一个 urban mask 把这些区域强制平整——但 urban mask 本身分辨率比 DEM 还粗，会在边界引入另一类伪影。
- **bathymetric（海底）upscale 伪影**：把 1km 海底深度强行上采到 500m 并标记为 mandatory（禁止 fractal 再细分）会产生很糟糕的阶梯伪影（Hawaii 岛案例）。Outerra 的教训是：**任何人为上采样都比保留原分辨率 + fractal refine 更差**。

## NasaDEM 并没有魔法

2018 年 Outerra 试用 NasaDEM 的 preliminary build（NasaDEM = 用新 void-fill 源重新处理 SRTM 原始数据）。在 SRTM1 原本出 bug 的 s50w075 tile（南美安第斯），NasaDEM 仍然有大量 void、线性伪影和错误高程；在原本 OK 的 Amazon delta（n00w051）也没见提升。结论是不要指望 NasaDEM 本身解决现有痛点；更靠谱的补洞源是独立维护的 Viewfinder Panoramas（全球 3″，用各地本地地图填 SRTM 空洞，基本无伪影）。

## 设计启示

- **源数据分辨率 × fractal resample 是最佳组合**；`76/30` 是用同样存储拿到更好观感的甜点。
- **不要让引擎相信一切上采样数据**。如果某层数据标记为「mandatory，不准 fractal refine」，它必须真的可靠——否则 fractal 反而是救命稻草。
- **数据层的缺陷需要 mask 机制**而不是高频滤波：urban mask / crest sharpening / void fill 三件套分别对应「把城市压平、把山脊加回来、把空洞填掉」。

## 相关

- [[outerra-team]]
- [[fractal-texturing]]
- [[diamond-square-noise]]
- [[erosion-filter-procedural]]
- [[infinite-chunked-procedural-generation]]
- [[fp64-sincos-minimax]] —— 同引擎在 GPU 端给 quad-sphere 坐标换 fp64 sin/cos

## Sources

- [[sources/outerra-srtm-30m-evaluation]]
- [[sources/outerra-nasadem-comparison]]
