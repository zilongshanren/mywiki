---
tags: [source, rendering, terrain, lighting, normals, glsl, outerra]
date: 2026-04-27
sources: 1
---

# Fixing the Lighting（Outerra）

[[people/outerra-team]] 发表于 2012 年 3 月的文章，记录两处地形光照 bug 的定位与修复过程。

## 摘要

文章篇幅短但诊断典型。第一个 bug 是地形**水平位移（horizontal displacement）**所在区域的法向量计算有误，导致对比度偏低：经重新推导位移 Jacobian 后，发现代码里残留了一个来自早期调试会话的错误系数 0.5，去掉后法向量恢复正确。第二个 bug 仅在 ATI 显卡上出现：把一组需要按位解释（bit-reinterpret）的浮点值写入浮点 render target 时，ATI 的混合单元会静默地修改浮点值的低位，使 bit 重解释结果出错。由于问题根源是 FP render target 的混合精度，改用整数 render target 存储需要 bit-exact 的数据后问题消失。

## 关键要点

- 位移 Jacobian 推导时忘记清理调试系数，导致多年后才触发的隐蔽 bug
- ATI 显卡的 FP render target 写入路径可能因混合单元引入低位误差，不适合存储需要 bit-exact 解释的数据
- 修复后顺带改善了 ambient lighting 在物体上的表现

## 链接到的概念

- [[planet-terrain-dem-pipeline]]
- [[sphere-mapped-terrain-culling]]

## 原文

- 链接：https://outerra.blogspot.com/2012/03/fixing-lighting.html
- 本地：`raw/articles/outerra.blogspot.com/2012-03-17_fixing-the-lighting.md`
