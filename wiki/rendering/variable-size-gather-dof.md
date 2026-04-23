---
tags: [渲染, 后处理, 景深, bokeh, 相机]
date: 2026-04-19
sources: 1
---

# Variable-Size Gather DoF（按 CoC 调节采样半径的聚拢式景深）

2010 年前后游戏里最常见的景深做法是 **sharp + blur + lerp**：渲一张清晰图，再整屏 Gaussian 重度模糊一张，然后按深度 / CoC 在两张之间插值。问题在于——取"重度模糊图"与"清晰图"的平均，并不等价于"做一次中等程度的模糊"。稍微失焦的物体在这套管线里会明显显得"脏"。

ATI 的 Thorsten Scheuermann 在 *Advanced Depth Of Field*（GDC 2004）给出了一个更物理友好的做法：**每个输出像素做一次 gather，但采样圆盘的半径随该像素的 CoC 动态变化**。稍失焦的像素做小半径 gather、大失焦的像素做大半径 gather——省掉了整屏重度模糊预处理，也天然避免了 sharp 图被"稀释"的问题。

## 代价：无法走可分离

传统 Gaussian blur 可拆成水平 + 垂直两 pass，9 × 9 的 kernel 用 9 + 9 = 18 次采样就能复刻 81 次的效果。但 variable-size gather 里每个像素的半径不同，分成水平、垂直两 pass 没意义——必须一 pass 内真的打满 N 个 tap。[[joost-van-dongen|Joost van Dongen]] 在 *Proun*（2010）里就是这么做：Very High 档 64 tap / 像素、High 档 32 / Medium 16 / Very Low 关闭整个效果。最终 DoF 占掉整个游戏 90% 的 GPU 时间——他认为值，因为 Proun 的抽象风格里，景深是**判断深度的唯一线索**。

## 噪声：美术风格决定能不能偷工

tap 数不够时自然想法是对采样偏移加随机扰动掩盖条带。van Dongen 试了，技术上能用，但 Proun 的画面几乎没有纹理细节，噪点在大片纯色表面上一眼可见，只能放弃。这条经验可以反过来推广到一般抽象 / 卡通 / 低频美术风格里：**任何依赖噪声掩盖欠采样的后处理都要警惕**，噪声需要小频纹理作掩护。

## 前景漏边问题

sharp + blur + lerp 还有另一个老毛病——前景清晰物体的边缘会被背景的重度模糊"污染"，在亮轮廓外产生一圈 glow。van Dongen 点名批评了 *StarCraft II* 的过场。Scheuermann 的 variable-size gather 因为采样半径由本像素 CoC 决定，不会去读失焦邻居然后再混进来，这一类漏边问题天然就没有。

## 和 scatter / 现代 gather 的位置

- 和 [[scatter-bokeh-dof|scatter bokeh]] 的关系：scatter 是"源像素撒 bokeh 精灵"，物理上正确但带宽爆炸；variable-size gather 是"目标像素 gather"的早期版本。
- 和 [[gather-bokeh-dof|现代 gather bokeh]]（DOOM 2016 / Courrèges）的关系：后者在 Scheuermann 思路上补了**形状可调**（方形 → 圆盘 → n 边形）、**CoC 下采 + max 过滤**、**McIntosh flood-fill 降噪**几项关键工程优化，能把 tap 数压到个位数同时保持大光斑干净。Scheuermann 2004 / van Dongen 2010 的版本是这条线上最朴素的一版。

## 相关

- [[gather-bokeh-dof]] —— 同路线的现代工程版
- [[scatter-bokeh-dof]] —— 物理对的另一条路
- [[thin-lens-model]] —— CoC 的推导
- [[separable-gaussian-blur]] —— 解释了为什么 variable-size 没法 separable
- [[circular-separable-dof]] —— 用复数基函数找回 separable 的 gather 变种
- [[joost-van-dongen]]

## Sources

- [[sources/joostdevblog-dof-blur-proun]]
