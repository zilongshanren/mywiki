---
tags: [渲染, 反走样, ssaa, fxaa, x-plane]
date: 2026-04-19
sources: 1
---

# 非方形 OGSSAA × FXAA（Supnik 2012）

[[ben-supnik|Supnik]] 2012 年 10 月在 X-Plane 10 上做了一个轻量实验：**把 OGSSAA（ordered grid SSAA）从方形网格换成非方形（如 1×2、2×4），再让 FXAA 在 SSAA 空间里跑**，而不是在 downsample 之后跑。这是一次针对"哪个方向的锯齿更扰眼"的定向加采样。

## 为什么不方形

传统 OGSSAA 采样数只有 1/4/16 可选——2× 就是 1×2、4× 就是 2×2、8× 就是 2×4。X-Plane 的画面**时间稳定性**（temporal stability）瓶颈主要出在**竖向**：背景里长而细的水平线（屋顶、道路、建筑轮廓）在相机平移时会"爬"。横向走样远没有纵向扰眼。

于是 8× 的非方形分布（2 列 × 4 行）把四倍的采样数花在竖直方向，而不是平均分布到方形。静态单帧画质的改善不明显（Supnik 自承"我不擅长看 AA"），但**时序稳定性**的提升肉眼可见：那些细屋顶不再跳动。

另一个被考虑过但放弃的选项是 **1.4×1.4 scaling**——总填充 2× 但走 box filter。代价是画面整体糊，而且 FXAA 无法工作：**FXAA 必须知道"像素"在哪里**，subpixel box 模糊会破坏它的边缘方向检测。

## FXAA 跑在 SSAA 空间里

Timothy Lottes（[[fxaa|FXAA]] 作者）亲自指点过 Supnik 正确的组合方式：**先在 SSAA 超分辨率 buffer 上跑 FXAA，再在同一个 pass 里把结果 mix 下来到目标分辨率**，而不是先 downsample 再 FXAA。这样 FXAA 看到的边缘在高分辨率下更尖锐，边缘检测和重建都更可靠；下采样在最后一步做，顺带把 SSAA 的 coverage 和 FXAA 的 morphological 修补平均到最终像素。

X-Plane 当时从旧 FXAA 版升到 FXAA 3.11，管线已经准备好这种"采样在 SSAA，混合在最后"的拓扑。

## 和 [[aa-techniques-survey-2011]] 的关系

Supnik 2011 那份 AA 五档分类把 SSAA 放在"Universal"档、把 FXAA 放在"Post-process"档，并在文末承认自己没深挖 MLAA vs FXAA。一年后这篇是他在产品上把两档拼起来的工程备忘：**SSAA 处理 shader 内走样 + 增加采样分布，FXAA 处理残余几何锯齿 + 低成本修边**。两种方案在问题域上并不冲突，重叠部分（几何锯齿）由非方形网格的方向偏置解决，而非多花 4× fill rate。

## 相关

- [[aa-techniques-survey-2011]]
- [[msaa-ssaa]]
- [[temporal-antialiasing]]
- [[subpixel-reconstruction-antialiasing]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-non-square-ogssaa-fxaa]]
