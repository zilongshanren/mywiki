---
tags: [source, 渲染, 反走样, post-aa, mlaa]
date: 2026-04-19
sources: 1
---

# Recipe for antialiasing as a post（Angelo Pesce / C0DE517E 2011-01-12）

[[angelo-pesce]] 2011 年 1 月发的一篇实验笔记：给出一份**最小化的梯度驱动后处理反走样滤镜**，作为 MLAA 的廉价替代方案。

## 摘要

Pesce 把 post-AA 滤镜的设计空间归纳为三步：**（1）识别边——从颜色还是从法线/深度？实践证明后者更稳；（2）把一个基元拟合到边上——直线、过像素中心的直线、曲线？MLAA 用 pattern matching 拟合长直线，这也是它不友好于 DX9 GPU 的原因；（3）沿基元混合——前景/背景按覆盖度插值，或沿基元积分/采样。** 他给出的 Pixel Bender 配方属于第三类最便宜的实现：只看当前像素及其梯度，不做远邻搜索。具体做法是用 Rec. 709 亮度权重算水平 / 垂直差分，把梯度旋转 90° 得到沿边方向，沿该方向取两个额外样本与原点相加做 3-tap 平均，混合系数按梯度模长（clamp 到一个阈值，论文里用 0.25）线性插值。

与 Intel MLAA 在 *Dead Rising 2* 上的对比：**MLAA 在笔直长边更好**（例如长椅）；**Pesce 的滤镜在曲线、有机表面更好**（树叶、角色），而且 MLAA 会把频繁换向的细节（僵尸头左侧的金属栏杆）糊掉。核心教训是：**只用局部梯度的滤镜天然缺乏长直线判据**——要么加大邻域（付出性能代价），要么承认自己只能处理曲线主导的场景。Pesce 在 PS3 上用它补强 2× quincunx 对抗 360 的 4× MSAA。

评论区读者确认：该配方在自家场景上只对近对角、定义清晰的边有效；近水平 / 近垂直边仍是 MLAA 的主场；*Force Unleashed II* 公开的技术与之相似。

## 关键要点

- post-AA 三段式模板：**识别边 → 拟合基元 → 沿基元混合**。
- 边识别：颜色不如法线 + 深度稳——深度 / 法线的不连续更能界定几何走样。
- MLAA 强在**全局模式匹配能找长近水平 / 近垂直直线**，代价是 CPU / SPU 式逻辑，对当时 GPU 不友好。
- 梯度 + 沿边 blur 属「本地滤镜」，天然只善于处理曲线与小特征，对长直线无能。
- Pixel Bender 配方：Rec. 709 亮度差分 → 梯度旋转 90° → 两点 3-tap 平均 → 梯度模长当混合权重。
- 组合策略：**MSAA + post-AA filter**——在 MSAA 的 sample 分辨率上做 edge filter，再 downscale，避免先 resolve 丢掉几何区分信息。
- 2011 年已存在 ATI HPG'09 关于 MSAA + edge filter 组合的综述（Pesce 在正文引用）。

## 链接到的概念

- [[angelo-pesce]]
- [[gradient-based-post-aa]]
- [[aa-techniques-survey-2011]]
- [[msaa-ssaa]]
- [[analytical-antialiasing]]
- [[temporal-antialiasing]]
- [[deferred-rendering]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/01/recipe-for-antialiasing-as-post.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-01-12_recipe-for-antialiasing-as-post.md`
