---
tags: [source, 渲染, frame-analysis, post-processing, adriancourreges]
date: 2026-04-27
sources: 1
---

# GTA V – Graphics Study Part 3（Adrian Courrèges）

[[people/adrian-courreges]] 发表于 2015 年 11 月的帧分析第三篇，聚焦《GTA V》的后处理效果栈，涵盖镜头光晕、变形镜头条纹、景深三大特效的实现细节。

## 摘要

本文延续 Part 1/2 的逐帧拆解思路，专注于场景渲染完成后的后处理阶段。GTA V 的后处理在深度与细节上均超出常规游戏的水准：镜头光晕同时使用基于图像（提取亮点区域）和基于精灵（太阳的 70 个精灵沿轴线排列）的混合方案；变形镜头条纹仅对正面朝向摄像机的强光源（如车灯）激活；景深则由带符号 CoC 贴图驱动，分前景与背景分别处理，用 compute shader 完成大核 blur，让前景模糊像素正确向焦点区域"溢出"。此外还有热气晕、体积光（既有屏幕空间溢出版本，也有场景内手放 mesh 版本）和运动模糊（仅按摄像机旋转方向做方向性模糊，用 stencil 排除玩家）等更多效果。

## 关键要点

- 镜头光晕采用图像 + 精灵双轨：图像流程生成左下角蓝色光晕（bright-pass buffer 的对称投影），精灵流程为太阳单独渲染 12 条旋转光柱 + 70 个光晕精灵
- 光晕大小随相机光圈变化：突然面向太阳时光晕巨大，曝光收敛后自动缩小；第一人称视角几乎无光晕（模拟人眼而非相机）
- 变形镜头条纹通过精灵实现，仅对极亮光源（如直射摄像机的车头灯）生效
- 景深：带符号 CoC 贴图（正值=背景离焦，负值=前景离焦），前景 CoC 先单独模糊一遍以消除硬轮廓，最终 blur 用 compute shader 以原始分辨率完成
- "Wasted"死亡画面是纯后处理：场景正常渲染 → 模糊 → 去饱和 → 暗角 + 胶片颗粒 → 叠字幕

## 链接到的概念

- [[circular-separable-dof]]
- [[gather-bokeh-dof]]
- [[physically-based-lens-flare]]
- [[thin-lens-model]]
- [[bloom-threshold-blur-composite]]

## 原文

- 链接：http://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study-part-3/
- 本地：`raw/articles/adriancourreges.com/2015-11-02_gta-v-graphics-study-part-3-adrian-courreges.md`
