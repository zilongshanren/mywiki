---
tags: [source, graphics, shader-graph, rendering-architecture]
date: 2026-04-19
sources: 1
---

# The Shader Graph Contract（Apoorva Joshi）

[[apoorva-joshi]] 2024 年 5 月的长文，正面回应「为什么 shader graph 不能无限灵活」。他的观点：shader graph 的**约束就是它的力量来源**，放开约束就会破坏延迟渲染、Visibility Buffer、GBuffer 压缩等一系列下游设计决策。这是少有的一篇从**引擎架构师视角**而不是艺术家视角谈 shader graph 的文章。

## 摘要

作者先把 shader graph 还原为图论对象：**DAG**，source 节点（法线/位置/UV）自动出现，sink 节点（master node）决定输出契约。sink 节点分三类：

1. **Unlit**——只有 color 输出，艺术家完全自由，代价是放弃 PBR、延迟渲染；
2. **Lit**——必须输出 metallic/smoothness/emission 这类 GBuffer 通道，艺术家可编程的只是「往 GBuffer 里写什么」；
3. **Layered & mixed lit**（MaterialX / Unreal Substrate）——层叠 BSDF，艺术家可控表达力最强。

Substrate 的工程取舍尤其精彩：它把 BSDF 打包成**预定义结构 Slab**（顺序固定：diffuse → specular → fuzz → subsurface），并在 GBuffer laydown 阶段做 **tree flattening**——计算每层的 coverage 与 transmittance，把 BSDF 树压平成一组扁平参数；延迟 lighting 阶段只看这组参数而不重建树。这样既保住了艺术家的表达力（可层叠 mix），又避免在 lighting 阶段支付树遍历的成本。文章最后给设计者和使用者两条建议：艺术家要理解 graph 是有 contract 的不能无边界自由；引擎作者要把 contract 作为**首要设计决策**，不要事后再补。

## 关键要点

- shader graph 的强约束来自**sink 节点契约**——它决定了谁能写 GBuffer、谁能改 lighting loop、谁能跨平台 scale。
- Lit master node 把艺术可编程性限制在「GBuffer 写入之前」，因此延迟渲染、Visibility Buffer 的解析导数都能成立。
- Unreal Substrate 的 **slab + tree flattening** 是让「层叠 BSDF」既工程可行又延迟渲染友好的关键工艺。
- 「能不能用 shader graph 写 toon shader」这类问题的答案不是技术限制，而是 contract 选择——要彻底自由就得选 Unlit sink，然后放弃 PBR。

## 链接到的概念

- [[shader-graph-contract]]
- [[shader-graph-custom-function-hlsl]]
- [[visibility-buffer]]
- [[deferred-rendering]]

## 原文

- 链接：https://apoorvaj.io/the-shader-graph-contract
- 本地：`raw/articles/apoorvaj.io/2024-05-05_quick-terminology-refresher.md`
