---
tags: [渲染, 立体, reprojection, inpainting, post-effect]
date: 2026-04-19
sources: 1
---

# 立体渲染的单眼重投影与洞补

把立体 3D 每帧都渲两遍的成本是白白翻倍——[[angelo-pesce]] 2010 年底的 *Stereoscopic test* 草草验证了另一条路：**只渲一只眼，把画面 reproject 到另一只眼**。左右眼的视差几乎全在屏幕 X 轴上，因此对基准眼的每个像素，在屏幕空间沿 X 方向扫一段，把**带深度的邻域样本**重投影到新眼的视空间、再投影回屏幕，看哪些样本会落到当前像素位置，取最近深度者作为答案。Pesce 在实验里用了 FX Composer + HLSL，brute-force 扫 127 个 tap，只是为了说明 idea，不打算拿来做产品。

## 重投影的第一性问题：洞

任何 reprojection 方案的共性难题都是**遮挡解除处**（disocclusion）。基准眼看不见被遮挡的背景，但另一只眼能看到一条细边——reproject 时这一块没有源数据，产生"洞"。同样的问题在 [[temporal-sao-reprojection|temporal SAO]] 里叫 dangerous samples / smooth invalidation，在 [[motion-blur-reconstruction|motion blur]] 和 DoF reconstruction 里叫 foreground extension / inpainting。Pesce 在这篇里**明确承认这是 reprojection / motion blur / DoF 共有的问题**，而他自己给出的"启发式 fallback"（选一个 `rowDist² / depth` 最小的邻居颜色）只是占位，真正的方法留给后续文章——可惜那篇后续并没有出现。

## 实验里的工程细节

- **深度重新编码到 RGBA8**：用 `(1, 255, 65025, 160581375)` 的经典 base-256 分解，把线性深度塞进 RGB 里，留出 alpha 位装测试 pattern——Pesce 的 test scene 是一个 `frac(UV*10) * 0.5 + 0.25` 的方格图案，便于肉眼看重投影是否对位
- **Linear-Z from projection matrix**：从 `Proj[3][2] / Proj[2][2]` 直接反推 near / far，不依赖外部 semantic 传进来（FX Composer 不给），属于图形老兵常备 trick（和 [[linear-z-trick|linear-Z]] 家族同源）
- **只沿 X 扫描**：`ReprojectView(viewPos) = viewPos + (0.2, 0, 0)`——硬编码的 IPD 偏移沿 view-space X，所以扫描也只在屏幕 X 维度展开，大幅降维
- **覆盖判定用的不是像素距离而是投影后 `rowDist < 2 / width`**：让 reprojection 在 1 像素厚的容差内吸附目标像素
- **brute-force 127 taps / pixel**：作者自己标注 "note: brute force = bad"，正式实现应该做 hi-Z / hi-stencil prime 再只对剩余空洞重绘

## 评论区的灵魂一问

"这个方案的意义是不是只是比两次渲染更快？" Pesce 的回答直接：**两次全渲染绝对错了**；至少应该 reproject 一次，然后只在空洞位置启用 hi-Z / hi-stencil 做部分重绘——把第二眼的 GPU 工作量从 1.0× 压到只有 disocclusion 比例的若干 percent。这个思路在 [[reprojected-planar-reflection|Bitsquid 的 reprojected reflection]]、[[temporal-supersampling|temporal supersampling]] 里一次次复现，是现代实时渲染的核心杠杆之一。

## 相关

- [[temporal-supersampling]] —— 时域版的同一结构（历史样本 + 失效补洞）
- [[temporal-sao-reprojection]] —— dangerous samples / smooth invalidation 的成熟化身
- [[reprojected-planar-reflection]] —— Bitsquid 把同一思路用在平面反射上
- [[linear-z-trick]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-stereoscopic-test]]
