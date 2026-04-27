---
tags: [source, rendering, 渲染哲学, roi, 生产流程]
date: 2026-04-27
sources: 1
---

# Rendering Doesn't Matter Anymore?（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2019 年 3 月的文章，标题故意制造悬念，实为探讨渲染工作的 ROI（投资回报率）框架——尤其是如何在「明显有用的功能」与「炫酷的渲染研究」之间做决策。

## 摘要

Pesce 从十三年生产经验出发，提出渲染已不再是游戏「类型定义者」——技术不再创造新的游戏玩法类型，只是美学层面的差异化工具。但他随即指出，这并不意味着渲染研究失去价值，反而是价值优先级需要重新审视。

真正的论点是：当代 AAA 游戏的图像质量与性能瓶颈，往往不在于「缺少最新的渲染特效」，而在于**资产生产本身**——数量/多样性不足、迭代能力受限、技术复杂度导致次优决策、艺术指导灵活性被锁死。从这个角度看，一套能自动生成 LOD/材质/实例的系统，比一个后期特效重要几个数量级。ROI 不是要精确量化，而是要时刻保持这个警惕心：我做的事情，是在服务产品，还是在自我满足？

## 关键要点

- 渲染已从「类型定义者」退化为「美学差异化工具」，这不是悲剧，是现实
- ROI 框架：先做「必须有」，再做「帮助人」，最后才是「炫酷研究」
- 不需要精确量化 ROI，但需要时刻问自己「这是否在服务产品」
- 当前大多数产品的图像质量瓶颈 = 资产生产流程，而非缺少渲染技巧
- PBR 是成功案例：减少了 hack、解耦了材质和光照，真正帮助了艺术家工作流
- 过度追求照片真实感可能反而损害「有趣的图形」——精力不够，世界多样性受损
- 熟悉度成本（familiarity cost）是真实代价：改变技术哪怕完全有利，也要付出重新学习的成本

## 链接到的概念

- [[rendering-roi-philosophy]]
- [[realtime-quality-vs-quantity]]
- [[physically-based-shading]]
- [[rendering-pipeline]]

## 原文

- 链接：https://c0de517e.blogspot.com/2019/03/rendering-doesnt-matter-anymore.html
- 本地：`raw/articles/c0de517e.blogspot.com/2019-03-11_rendering-doesnt-matter-anymore.md`
