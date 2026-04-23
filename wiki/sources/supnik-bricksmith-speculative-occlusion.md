---
tags: [source, 渲染, bricksmith, 遮挡剔除, gpu-driven, transform-feedback, 反面案例]
date: 2026-04-19
sources: 1
---

# Theoretical Engineering: Occlusion Culling for BrickSmith（Ben Supnik）

[[ben-supnik|Ben Supnik]] 2013-08-31 的一篇 *speculative engineering* 推演：在 LDraw / BrickSmith 这种罕见的**纯顶点 bound**场景里，若真要上 GPU 遮挡剔除会长什么样——以及为什么他最终决定**不**发车。

## 摘要

BrickSmith 的 instance list 已经在 GPU 上跑，但一个大模型远视角下 125M 顶点把 GPU 顶点吞吐吃满。Supnik 推演了一条完整 GPU-side pipeline：每个部件预切**crude occluders + the rest**，先画 crude 拿 depth → ping-pong 建**"farthest" depth pyramid** → geometry shader 对每个 instance 做屏幕 AABB vs pyramid 的保守判测、输出 0 / 1 顶点进 **transform feedback** → `glDrawTransformFeedbackStreamInstanced` 驱动下一轮"只画幸存 brick 的 the rest"。典型 2×4 brick 被遮后能省 97% 顶点。**然而**他列出四条 show-stopper：(1) LDraw part library 手工切分回灌不可能；(2) 要求 DX11-class GPU + OpenGL 4.2 instanced transform feedback，2013 年 Apple 连 GL 4.0 都没出，砍 Lion / Mountain Lion；(3) per-brick transform feedback VBO 代价大；(4) 工程量超过整次 renderer 重写，业余项目扛不住。结论：回去用粗糙 LOD 模型。edit 补了 Daniel Rákos 的异步 feedback-count query 方案，但会引入 CPU-GPU 同步点。

## 关键要点

- 少见的**顶点 bound** 瓶颈是整套 pipeline 成立的前提（fill rate 不挤 ⇒ 小 draw 便宜）。
- "farthest" depth pyramid + geometry shader per-instance cull + transform feedback 回收 = 2013 版 GPU culling。
- 推演出不发车的四条 show-stopper 本身是可复用的工程检查表。
- Kostas Anagnostou 2017 的 compute + stream compaction 方案解决了 VBO 那一条，其余三条仍由项目形态决定。

## 链接到的概念

- [[bricksmith-speculative-gpu-occlusion]]
- [[occlusion-culling]]
- [[gpu-based-occlusion-culling]]
- [[hierarchical-z-buffer]]
- [[bricksmith-instancing-pipeline]]
- [[gpgpu-transform-feedback-ios]]
- [[bottleneck-analysis]]
- [[xplane-instancing-2011-numbers]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2013/08/theoretical-engineering-occlusion.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-08-31_theoretical-engineering-occlusion-culling-for-bricksmith.md`
