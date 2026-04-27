---
tags: [source, rendering, stencil, deferred-rendering, light-volume, x-plane]
date: 2026-04-27
sources: 1
---

# There Must Be Fifty Ways to Fail Your Stencil（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2018 年 3 月的文章，复盘 X-Plane 延迟渲染中双面 stencil 光源体积方案的两次失败以及单次 pass 替代方案的尝试。

## 摘要

X-Plane 在 10.0 引入延迟渲染时，为节省 fill rate 对点光源使用了**双面 stencil 包围体**技术（back-face increment、front-face decrement，第二 pass stencil > 0 的像素才执行光照）。首次尝试因「二次过体积的顶点带宽代价 > fill rate 收益」而放弃。再次拾起时又遇到第二个问题：stencil 的 3 位（8 档）计数器在 8 个光源叠加的像素处发生**绕回（wrap-around）**，将 stencil 值归零，导致正中心区域出现「黑洞」——因为其他 stencil 用途挤占了可用 bit 数。Supnik 随后尝试退化为单 pass 方案（用正面深度测试代替 stencil 预处理），借助 `GL_ARB_depth_clamp` 防止前剪裁面切掉体积，但发现视锥体侧平面在摄像机处交汇，摄像机在光源体积内部时侧面背后的部分被剔除，单 pass 方案在此情况下无法给出正确的屏幕覆盖。

## 关键要点

- 双面 stencil 体积的标准算法：inc-with-wrap（back depth-fail）+ dec-with-wrap（front depth-fail），结果 > 0 表示「在包围体内部且有可光照几何」。
- 实际工程中 stencil 的 bit 数极容易被其他特性（portal、反射、outline 等）蚕食，导致计数器绕回产生错误剔除。
- Wrap-around bug 的视觉症状：恰好累计到绕回点的像素区域突变为全黑，轮廓清晰。
- 单 pass 正面深度测试替代方案的死角：当摄像机在光源体积内时，frustum 侧面在摄像机后方裁掉体积侧面，屏幕覆盖丢失——depth clamp 只能处理近/远剪裁面，不能处理侧面剔除。
- 与 [[deferred-light-volume-stencil-depth-clamp-hack]] 的关系：那篇处理远剪裁面切背面的问题，本文聚焦 bit 溢出和单 pass 的视锥剔除缺陷，是同一套系统的两个独立失效点。

## 链接到的概念

- [[stencil-buffer]]
- [[deferred-rendering]]
- [[deferred-light-volume-stencil-depth-clamp-hack]]
- [[stencil-failure-modes-deferred-lighting]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2018/03/there-must-be-fifty-ways-to-fail-your.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2018-03-27_there-must-be-fifty-ways-to-fail-your-stencil.md`
