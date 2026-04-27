---
tags: [source, rendering, pbr, brdf, 物理假设, 近似]
date: 2026-04-27
sources: 1
---

# Seeing the Whole Physically-Based Picture（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2019 年 5 月的文章，副标题「Building our rendering on solidly shaky grounds」，系统梳理了 PBR 管线从物理框架到最终像素的完整假设链，揭示每一层都存在多少被默默接受的近似。

## 摘要

文章从几何光学框架出发，逐层剥开 PBR 管线的物理假设：色彩空间（三色刺激/RGB 代替光谱），微表面理论（不考虑衍射、diffraction grating），BRDF 推导（积分本身无法闭合，需要再做近似），光源积分（像素足迹、面积光近似、直接光 vs 全局照明），直至体积散射与 participating media。每一步都有被扫到地毯下的错误。

Pesce 的结论不是「PBR 是骗局」，而是呼吁整体性地看待这些近似——不应在已经有大量误差的管线末端，再无谓地追求某一局部的精确性（比如一个更精确的 GGX 尾巴），而应优先弄清楚端到端的主要误差来源在哪里。

## 关键要点

- 几何光学本身已无法建模衍射、干涉、荧光——PBR 的物理底座从一开始就有局限
- RGB 代替光谱渲染是巨大妥协，结果靠艺术家调灯光和后处理掩盖
- 微表面理论中：扩散光（diffuse）本质是把 microfacet 换成 Lambertian 漫反射面，并不真正模拟体散射
- BRDF 推导中默默略去了多次弹射（→ 能量流失，参见 [[microfacet-brdf]] 的多散射补偿）
- 像素足迹（pixel footprint）只考虑了法线统计，忽略了光线方向变化和几何遮蔽
- 面积光积分：不同光源形状（点、线、面、环境）各有独立近似，相互之间不一定一致
- 全局照明是单独一套假设体系，与直接光的 PBR 精度不在同一水平
- 艺术家会「自动」补偿所有错误——这使得从图像反推误差来源极为困难
- 正确答案：收集真实世界数据 → 暴力计算参考 → 分析感知上哪些误差重要 → 有针对性地改进

## 链接到的概念

- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[ibl-multiple-scattering]]
- [[spectral-rendering]]
- [[color-space]]
- [[pbr-approximation-stack]]

## 原文

- 链接：https://c0de517e.blogspot.com/2019/05/seeing-whole-physically-based-picture.html
- 本地：`raw/articles/c0de517e.blogspot.com/2019-05-15_seeing-the-whole-physically-based-picture.md`
