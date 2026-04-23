---
tags: [source, 渲染, 延迟渲染, depth-buffer, g-buffer, x-plane]
date: 2026-04-19
sources: 1
---

# Deferred Depth: 3 Ways（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2012 年 7 月的 G-Buffer 深度复用笔记，正值 X-Plane 10.10 延迟管线整改期。把"光照 pass 如何拿到眼空间深度"这个看似小的问题讲出三条互斥路线及其选型逻辑。

## 摘要

延迟渲染的光照 pass 同时需要两件事：**采样深度重建位置**、**绑定深度做硬件深度测试**（支持 light volume stencil trick、soft particle 剔除等）。同一张深度要既当纹理又当 depth attachment——API 冲突怎么解？Supnik 列了三条：(A) 每帧 `glCopyTexSubImage` 把 D24S8 拷到一张独立深度纹理——简单通用，现代驱动下性能不再是问题；(B) 用 `GL_NV_texture_barrier` 让同一张深度纹理既绑 FBO depth 又被 shader 采样，关 depth write 后一 draw 内可读写共存——**仅 NV Windows**，Supnik 没实测；(C) 直接把眼空间 Z 写到 G-Buffer——浪费一个通道但绕开所有 API 冲突。X-Plane 最终选 C，原因是它画**两个深度域**（外部世界 + 3D 座舱），单一 D24S8 装不下跨量级深度；16F 眼空间 Z 才能把"分段深度"扁平化成一份位置信息。16F 是对近处精度（阴影）与远处精度（雾）的取舍，ATI 上 16F 比 32F 填充更快。评论里讨论了 Outerra 的 log-depth 方案：Supnik 放弃——`log(z)` 在 z<0 未定义，且 fragment shader 改写 depth 会禁用 early-Z。

## 关键要点

- 三条路线：拷贝深度 / texture-barrier 复用 / G-Buffer 写眼空间 Z。
- X-Plane 选 C，根因是**双深度域**（近 1cm 座舱 + 远 100km 世界）超出 D24S8 的可表示范围。
- 16F 深度权衡：近处精度够阴影，远处只喂雾可接受；ATI 上 16F 比 32F 填充快。
- `GL_NV_texture_barrier` 放宽同 draw 纹理读写约束——但是 Windows / NV 独家。
- log-depth（Outerra 方案）两坑：负 Z 未定义、fragment 改 depth 禁用 early-Z。

## 链接到的概念

- [[deferred-depth-reuse-tradeoffs]]
- [[deferred-rendering]]
- [[xplane-gbuffer-format]]
- [[multiple-render-targets]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2012/07/deferred-depth-3-ways.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2012-07-24_deferred-depth-3-ways.md`
