---
tags: [渲染, 后处理, hdr, 色调映射]
date: 2026-04-14
sources: 3
---

# 局部色调映射（Local Tonemapping，LTM）

**全局色调映射**（global tonemapping）用一条统一的曲线把高动态范围（HDR）场景压回 LDR 显示空间。在动态范围很大的场景里——例如阳光直射的户外加上深阴影——任何单一曲线都做不到「亮处不过曝、暗处不死黑」：选中间曝光会丢两端细节，选低对比会让画面发灰。**局部色调映射**通过让曝光/对比的处理依赖于像素的邻域（局部亮度），在不同区域应用不同的曲线，从而同时保留高光和阴影细节。

## 为什么游戏需要它

物理正确的光照管线（physical sun/sky、PBR 材质）会自然地产生大动态范围。游戏可以「假」一切（拉亮 albedo、加 fill light、改变天空亮度），但每一次这样的 hack 都会撕裂物理一致性，让其他时间段的光照模型崩坏。LTM 提供了一个相对正交的工具：**把动态范围压缩交给后处理，让光照保持物理正确**。

[[bartosz-wronski|Bart Wronski]] 在 God of War 上用「Gaussian 模糊亮度后做曝光决定」实现过一版简陋 LTM，但推到极限就会出现明显的 **halo**（光晕）：亮区压暗时把周围的中间调一起拽下去，反之亦然。

## 主流方法谱

| 方法 | 思路 | 主要问题 |
|---|---|---|
| 逐像素 blending | 直接按亮度选曝光 | 局部对比破坏，色彩泛白 |
| Gaussian blending | 对亮度先模糊再决策 | 强 halo |
| Bilateral blending | 边缘保持滤波 | 梯度反转、边缘振铃 |
| Bilateral + Gaussian | Jasmin Patry 在 Ghost of Tsushima 用 | 在 halo 与振铃间折中 |
| Guided filter | 用 [[guided-filter]] 转移低分辨率亮度 | 边缘略糊、局部对比下降 |
| **[[exposure-fusion]]** | 在 Laplacian 金字塔不同尺度上用不同半径 blending | 计数曝光、参数有点反直觉 |
| Bilateral grid | Chen 等人的高维采样滤波 | 实现复杂 |

## 频率与尺度的关键洞察

LTM 的核心观察：**曝光变化的频率应当和图像内容的频率相关**。在平坦无纹理的区域，曝光要在大半径上慢慢渐变，眼睛才察觉不到；在有强边缘和细节的区域，曝光要在边缘附近迅速完成切换，让变化「藏在边缘里」。这是 [[exposure-fusion]] 把不同尺度 Laplacian 用不同 Gaussian 权重混合的根本原因。

## 与摄影历史的连贯性

Ansel Adams 的 [Zone System / dodge & burn] 已经是手工做的 LTM；Lightroom / Adobe Camera Raw 的默认开图就是一种局部色调映射；Lightroom 的「Clarity」滑块是 [Local Laplacian Filter] 类的局部对比调节。Google Pixel 的 HDR+「look」很大一部分功劳也来自 LTM——Wronski 加入 Google 后参与的就是这条流水线。

## 相关

- [[exposure-fusion]]
- [[laplacian-pyramid]]
- [[guided-filter]]
- [[color-space]]
- [[bartosz-wronski]]
- [[tone-mapping]] — 全局色调映射算子概述，与 LTM 互补

## Sources

- [[sources/bartwronski-exposure-fusion]]
- [[sources/c0de517e-tone-mapping-local]] — Pesce：用渲染器 illuminance pass 直接做局部 TM，零滤波成本
- [[sources/c0de517e-tone-mapping-silly]] — Pesce：大半径高斯 ND 滤镜 + 胶片颗粒扩展动态范围的快速实验
- [[sources/bruop-tone-mapping]] — Bruop：全局色调曲线综述（Reinhard / ACES / GT / Lottes），逐亮度 vs 逐通道的权衡
