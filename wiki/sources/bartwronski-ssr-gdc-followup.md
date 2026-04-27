---
tags: [source, 渲染, ssr, filtering, upsampling, bartwronski]
date: 2026-04-27
sources: 1
---

# GDC follow-up: Screenspace Reflections Filtering and Up-sampling（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 3 月 GDC 后发表的补充博文，详解 Assassin's Creed 4 中 SSR 缓冲区的过滤与上采样实现细节，是对 GDC 演讲中未展开部分的正式补充。

## 摘要

文章拆解了 AC4 SSR 在滤波阶段需要解决的四类需求：模拟不同粗糙度表面的 BRDF 高光波瓣宽度、填补 ray miss 的空洞、压制 aliasing 与 flicker、以及从半分辨率上采样到全分辨率。上采样部分放弃了标准的深度边界感知双边上采样，转为以**表面反射率**（gloss-based specular response + Fresnel 合成值）作为上采样权重——在水坑与脏土地的粗糙度边界上效果明显优于深度权重。滤波部分以 cross 形预模糊降采样源颜色缓冲区为预处理，再做按 gloss 变化半径的可分离高斯模糊；滤波权重只依赖两因素：样本 alpha（ray miss 还是命中）+ 高斯函数；刻意跳过了深度差权重，因为深度不连续处本就没有反射信息，不会产生 leaking。对于空洞区域，作者引入 push-pull 策略：命中样本往外 push、缺失像素往大邻域 pull，空洞处混合权重不置零（AFAIR 0.3）以保留 cubemap fallback 的自然过渡。

## 关键要点

- **反射率权重上采样**：用 gloss × Fresnel 合成的反射率取代深度作为边界感知权重，在粗糙度剧变区（水坑/泥土边界）比传统双边上采样更鲁棒。
- **源颜色 cross 预模糊**：降采样时做 cross 形轻模糊，压制半分辨率颜色缓冲的亚像素 aliasing，与 Mittring/Epic 的 bloom 降采样建议相同思路。
- **可分离模糊的妥协**：分离高斯在两个方向半径不同时理论上不正确，但因为表面 glossiness 在屏幕上空间连贯，未观察到可见的混合 pattern 问题。
- **Push-Pull 填洞**：miss 像素不置零权重，而是降权（约 0.3）以自然淡出到 cubemap fallback，同时向更大邻域寻找命中样本。
- **距离锥度扩展被放弃**：严格物理上模糊半径应随距离扩大（反射锥展开），但实验显示只在粗糙平坦表面近距离下差异明显，normal map 和有机表面上视觉差可忽略，故舍弃以节省 ALU。

## 链接到的概念

- [[screenspace-reflections]]
- [[depth-aware-upsampling]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/03/23/gdc-follow-up-screenspace-reflections-filtering-and-up-sampling/
- 本地：`raw/articles/bartwronski.com/2014-03-23_gdc-follow-up-screenspace-reflections-filtering-and-up-sampl.md`
