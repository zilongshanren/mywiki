---
tags: [source, 渲染, 头发, deferred, forward]
date: 2026-04-14
sources: 1
---

# Hair rendering trick(s)（Bart Wronski，2014-07）

[[bartosz-wronski|Bart Wronski]] 2014 年 7 月的博客，记录他在 CD Projekt Red 为 Witcher 3 / Cyberpunk 2077 原型期使用的一个头发渲染 trick——本质上是**把 alpha-tested 发丝条拆成不透明主体 + 半透明边缘两段，分别走 deferred / forward** 的 hybrid pipeline，避免 fat G-Buffer 材质分支与头发锯齿的双重代价。

## 摘要

作者先梳理 deferred 渲染下头发的两个经典痛点：各向异性头发 BRDF 塞不进 G-Buffer（需要分支 / material ID，vgpr 爆炸），以及 alpha-test 发丝带来的严重锯齿（MSAA/alpha-to-coverage 都不能干净解决）。Forward + OIT（AMD TressFX）是正解，但成本过高。他的 trick 分四步：第一步用高 Aref 只挑最实心的发丝写入 G-Buffer，关闭 specular；第二步跑标准 deferred 光照；第三步 `ZTest=Equal` 重画同一批像素，在 forward 里算真正的头发 BRDF 加到 lighting buffer；第四步反向 alpha test 挑出半透明发梢，开启 alpha blending 画最后一 pass。优点是任意 BRDF、无 fat G-Buffer 分支、绝大部分 depth 已写、alpha blend 区域极小、sorting 友好；代价是 3 个几何 pass 与更复杂的 pipeline。文末顺带记录 Witcher 2 的 SSS hack：把 unmodulated specular 写进 lighting buffer 的 alpha 通道，Jimenez SSS blur 后再画皮肤网格。作者在 2020 年后记里承认该 trick 随着 GPU 分支代价下降已「部分过时」，但**「不透明 + 半透明边缘分离」的核心想法**在移动端 forward 引擎里依然适用。

## 关键要点

- **Deferred 的头发痛点**：各向异性 BRDF 塞不进 G-Buffer，alpha test 发丝严重锯齿。
- **Trick 核心**：按 alpha 值把发丝切成「主体」与「边缘」两段，分别走 deferred / forward。
- **四 pass 流程**：G-Buffer（高 Aref 无 specular）→ deferred 光照 → `ZEqual` forward specular → 反向 alpha test + alpha blend 画发梢。
- **`ZTest = Equal`** 保证 forward specular pass 零 overdraw；绝大部分发丝写了 depth，与粒子/透明物体互相兼容。
- **独立原型**：同期 Crytek GDC 2014 演讲独立提出相似做法；更早 Scheuermann 2004 也有类似多 pass 思路（但纯 forward）。
- **不适用场景**：spline/tessellation 级别超复杂头发——应直接用 TressFX / OIT。
- **SSS hack**：用 lighting buffer 的 alpha 通道承载 unmodulated specular，配合 Jimenez bilateral blur 实现皮肤 SSS 而不模糊 albedo / specular。代价是丢失镜面色度。
- **后记（2020）**：现代 GPU 对分支与 fat G-Buffer 更友好，trick 部分过时，但移动端 forward 引擎仍然受用。

## 链接到的概念

- [[hybrid-hair-rendering]]
- [[deferred-rendering]]
- [[deferred-alpha-lighting]]
- [[alpha-blending]]
- [[dither-alpha-clipping]]
- [[msaa-ssaa]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/07/20/hair-rendering-tricks/
- 本地：`raw/articles/bartwronski.com/2014-07-20_hair-rendering-trick-s.md`
