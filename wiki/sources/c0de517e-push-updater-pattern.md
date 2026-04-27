---
tags: [source, software-design, game-engines, performance]
date: 2026-04-27
sources: 1
---

# Design Pattern: The Push Updater（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2014 年 2 月的文章，以 Warhammer 40K: Space Marine 的优化经历为例，介绍"推式更新"模式——将共享数据的间接指针替换为主动广播，从而消除渲染循环中的 cache miss。

## 摘要

文章从一个真实案例出发：Space Marine 后期 CPU 成为瓶颈，原因是每个 drawcall 需要沿指针链（material → texture class → GPU texture handle）逐层解引用，导致大量 cache miss。当时的应急方案包括 LOD 材质合并、顶点色烘焙等，最终靠排序和数据结构调整勉强达到 30fps。

事后复盘提出"Push Updater"：引入一个 UpdateManager，记录某块共享数据的所有"使用方"位置；当数据变化时，主动把新值推送（写入）到所有注册位置，而非在读取时沿指针跳转。这样访问路径变为直接读本地副本，无需间接寻址。UpdateManager 还可以按内存地址排序推送，进一步提升写入的局部性。文章还指出，可见性剔除的"把 visible 对象指针追加到列表"本质上就是一种隐式的推式消息。

## 关键要点

- 间接指针（indirection）是渲染 CPU 性能杀手，尤其在远处低 LOD 的大量 draw 中
- Push Updater：UpdateManager 存储所有副本位置，变更时主动广播，读取路径零跳转
- 与引用计数/热加载/流式加载兼容：只需在 create/destroy/update 时通知 manager
- 推送时可按内存地址排序，使写入更缓存友好
- 可见性剔除的"追加可见列表"是隐式 push pattern 的实例

## 链接到的概念

- [[game-engines/data-driven-architecture]]
- [[rendering/draw-call]]
- [[software-design/performance-by-design]]
- [[game-engines/handle-based-resource-manager]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/02/design-pattern-push-updater.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-02-10_design-pattern-the-push-updater.md`
