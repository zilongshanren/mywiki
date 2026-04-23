---
tags: [渲染, 抗锯齿, temporal, taa]
date: 2026-04-14
sources: 1
---

# Temporal Antialiasing（TAA）

**TAA 的核心思想**：把超采样的计算分散到多帧——每一帧以 sub-pixel 的抖动偏移渲染一次，再把历史帧结果累积融合，得到接近 16x 超采样的质量，而单帧只付出 1x 的成本。代价是引入了一整套新问题（ghosting、blurring、flicker），而这些问题的解决方案几乎构成了现代实时渲染最深的工程泥潭。

## 为什么要做 TAA

图形中的 [[aliasing]] 来源远不止几何边缘——alpha test、镜面高光、高频 normal map、parallax mapping、低分辨率效果（SSAO、SSR）、dithering、噪声都会制造锯齿。传统的 [[msaa-ssaa|MSAA]] 只对几何边缘有效，屏幕空间的 edge detection（FXAA/SMAA）对所有高频内容一视同仁地模糊，都只能覆盖一个子集。TAA 的野心是**用同一个机制解决所有类型的 aliasing**，代价是必须维护「历史」。

## Jitter：抖动投影矩阵

最干净的实现方式是在每一帧把投影矩阵往 frustum plane 方向平移半个像素以内的量。偏移序列要用 quasi-random 序列（Halton、Sobol）而不是纯随机，避免 clumping。典型取 4–8 个样本循环。实现上只需在投影矩阵的 `[2][0]`、`[2][1]` 位置加上 `j_x`、`j_y`：

```
P' = P · T(j_x, j_y)
```

抖动过后按常规 [[rasterization|光栅化]] 产生这一帧，每帧采样的是像素内不同的 sub-pixel 位置。

## Resolve：累积与融合

最常见的实现用一个「accumulation buffer」保存历史，每一帧按很小的权重（典型 10%）混入当前帧：

```
output = currentColor * 0.1 + previousColor * 0.9
```

静态相机下这就够了。问题在于相机一动，同一个屏幕坐标对应的上一帧内容就不是同一个表面——于是出现 **ghosting**（拖影）。解决这个问题需要 **reprojection**：用当前深度反投影回世界空间，再用上一帧的 view-projection 矩阵投影到上一帧屏幕空间，从那里采样历史纹理。光有相机 reprojection 还不够，动态物体还需要自己的 [[motion-vectors|motion vectors]]。

## 历史有效性：遮挡与失配

Reprojection 解决了相机移动，但解决不了 disocclusion——当前可见的表面上一帧根本不在屏幕里，或者被其他物体遮住了。这时候去历史 buffer 里采样会拿到**错误的颜色**。针对这个问题演化出了一整族 rectification 技术（[[taa-history-rectification]]）：color clamping、depth/stencil/velocity rejection、luminance weighing。

## 模糊与 Catmull-Rom

即便没有 disocclusion，TAA 也会让图像变软。原因是 reprojection 之后的 UV 几乎不会正好落在历史像素中心——需要 reconstruction filter。bilinear filtering 引入模糊，且在 accumulation 过程中会持续累积。业界的主流方案是 **Catmull-Rom bicubic**：带负 lobe 的高阶核，能在保留锐度的同时稳定重建。Catmull-Rom 原本需要 16 次采样，利用 bilinear 采样器可以优化到 9 次，Call of Duty 团队进一步砍到 5 次。

## 纹理模糊

TAA 的 jitter 同样会在纹理空间造成额外模糊，因为 mipmap 选择算法是按 derivatives 做的，而 jitter 打乱了这些 derivatives。两个修复方法：

- **negative mip bias** — 强制采样更锐利的 mip，但要小心把 aliasing 又引回来
- **Unjitter UV** — 用 `ddx_fine`/`ddy_fine` 算出 jitter 对应的 UV 偏移，反向抵消掉，保留原始 bilinear filter

## 透明与 camera cuts

透明物体一般不写深度，也就拿不到 motion vectors——必须手动写 blended velocity，或者标记为「responsive AA」跳过 rectification。camera cut 时历史完全失效，需要短暂回退到其他 AA 或者加速收敛。

## 批评与权衡

TAA 被诟病「整个画面都在糊」——这是事实。它是一个**妥协**：用可接受的软度换掉所有形式的 aliasing，在现代延迟渲染 + 物理 BRDF + 随机采样的组合下几乎是唯一工程可行的路。MSAA 在这些管线下性能惩罚太大，也阻碍很多现代光栅化变体。

## 相关
- [[aliasing]]
- [[msaa-ssaa]]
- [[motion-vectors]]
- [[taa-history-rectification]]
- [[rasterization]]
- [[emilio-lopez-ros]]
- [[temporal-supersampling]] — Wronski 对 AC4 TAA 的祖师级复盘，覆盖 motion vector pipeline 的全部踩坑
- [[ground-truth-ambient-occlusion]] — Use.GPU 的 GTAO 靠 3D motion vector + depth/normal bilateral 做 reprojection，与 TAA 同构
- [[aa-techniques-survey-2011]] —— Supnik 2011 把 TAA 归到 post-process 档，显示当时它还没独立成类

## Sources

- [[sources/elopezr-taa-holy-trail]]
- [[sources/bartwronski-temporal-supersampling]]
