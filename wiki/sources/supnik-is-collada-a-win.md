---
tags: [source, 资源管线, collada, dcc, 工具链]
date: 2026-04-19
sources: 1
---

# Is COLLADA a Win?（Ben Supnik / hacksoflife）

[[ben-supnik|Supnik]] 2011-01-28 的反思：在跨 DCC 的开放平台 X-Plane 上，**资源交换格式该怎么选**。

## 摘要

X-Plane 这类开放平台的资产来自各家第三方 DCC，每家都要带引擎特有元数据（billboard、硬表面属性等）。Supnik 总结出三条路线：(A) 给每款 DCC 写一个 full-featured exporter——当时 X-Plane 走的路，扩展性线性恶化，每新增引擎特性都要在 N 个 exporter 里重复实现，他自己维护的 AC3D exporter 跟不上自家格式演进；(B) 自造「简单中间格式 + 后处理工具」——类似 X-Plane scenery 的 DSF / DSF2Text 双层结构，exporter 变薄、复杂度集中到一个离线工具里；(C) 采用 COLLADA 这类现成交换格式——理论上白嫖 DCC 侧已有的 exporter，但现实是每家 DCC 的 COLLADA 输出是**方言**（3ds Max、Maya、Blender 各不相同），引擎侧仍要对每个方言做兼容层，且 DCC 是否把引擎专属元数据录进 `<extra>` 不保证。Supnik 倾向的结论（评论区同行的亲身经验支持）：**处理 N 种方言依然比写 N 个 full native exporter 便宜**——类比「N 家实现了同一个 API 的变体，你只写一次公共面，再 patch 差异」。更多是一个「为什么交换格式值得用、以及它的折扣在哪」的决策框架。

## 关键要点

- 三条路线：N 个原生 exporter / 简单中间格式 + 离线工具 / 现成交换格式。
- 原生 exporter 的失败模式：**引擎特性对齐度随 DCC 数量递减**。
- 中间格式（DSF / DSF2Text 模式）：复杂度收敛到一份离线工具，脚本语言友好。
- COLLADA 的折扣：**通用性太大 → DCC 方言发散**，仍需引擎侧 patch；引擎元数据靠 `<extra>` 节点传递，DCC 支持不齐。
- 尽管有折扣，处理方言 × N 仍比写 full exporter × N 便宜（公共面已规格化）。
- 现代延伸：glTF 2.0 事实上取代了 COLLADA，正是因为**更窄更 opinionated**，压下了方言离散度。

## 链接到的概念

- [[asset-exchange-format-strategy]]
- [[game-resource-pack-format]]
- [[decoupled-tool-engine-json-rpc]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/01/is-collada-win.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-01-28_is-collada-a-win.md`
