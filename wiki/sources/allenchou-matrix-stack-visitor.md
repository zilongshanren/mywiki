---
tags: [source, scene-graph, visitor-pattern, 引擎架构, allen-chou]
date: 2026-04-14
sources: 1
---

# Matrix Stack and the Visitor Pattern（Allen Chou, 2011）

[[allen-chou|Allen Chou]] 2011 年 2 月在 allenchou.net 发表的短文，讲他为自己的 2D / 2.5D 引擎（ZedBox、Pyronova、Bunnyhill）摸索出的一个场景图遍历套路：**用访问者模式持有矩阵栈，节点只存 local transform**。

## 摘要

文章从他早期的一个错误做法讲起：在 ZedBox 里每个 scene tree 节点都持有一份自己的 global transform，渲染遍历时从根向下递归刷新。跑起来没问题，代码却越写越乱，而且一旦从 tree 推广到真正的 scene graph（允许一个节点有多个父亲），这个假设就不成立了。作者在和 Minko 3D 引擎作者 Jean-Marc Le Roux 交流后，学到访问者模式在这种场景下的正确用法：矩阵栈不挂在节点上，而是被一个 visitor 对象持有；visitor 在遍历时"访问"每个节点，节点只在被访问的瞬间读栈顶得到自己的全局变换。进入容器节点时 push `top * localTransform`，离开时 pop。这样同一节点被多条路径访问时，各自拿到的全局变换互不干扰。文末附 ActionScript 3 风格的接口和 ContainerNode 实现。

## 关键要点

- "每节点持有 global transform" 是只适合 scene **tree** 的捷径，scene **graph** 下天然失效。
- 矩阵栈 push/pop 与深度优先遍历天然匹配，栈顶即"从根到当前节点的累积变换"。
- 访问者模式让遍历状态（矩阵栈）与节点结构解耦，同一棵场景图可以被多种 visitor 复用：渲染、拾取、包围盒计算等。
- 这个思路和早期固定管线 OpenGL 的 `glPushMatrix` / `glPopMatrix` 机制本质相同，只是把它从 GPU 状态挪到 CPU 场景层。

## 链接到的概念

- [[scene-graph-matrix-stack-visitor]]
- [[mvp-transform]]
- [[coordinate-spaces]]
- [[composite-command-pattern]]

## 原文

- 链接：https://allenchou.net/2011/02/matrix-stack-and-the-visitor-pattern/
- 本地：`raw/articles/allenchou.net/2011-02-11_matrix-stack-and-the-visitor-pattern-ming-lun-allen-chou-zho.md`
