---
tags: [scene-graph, engine-architecture, renderable-entity, 引擎架构, 反模式]
date: 2026-04-19
sources: 1
---

# 3D 引擎不需要场景图

[[angelo-pesce|Angelo Pesce]] 在 *The pitfalls of experience*（2010）评论区里回复读者时，系统阐述了一个他反复主张的观点：**通用的 scene graph 对一个 3D 引擎来说基本是一种浪费甚至危害**。这和 [[scene-graph-matrix-stack-visitor|"矩阵栈 + visitor 的场景图"]] 那种经典教科书式讲法形成直接对立，因此值得单独立页。

## 先问为什么要用场景图

Pesce 的反问很直白：*"ask yourself why are you using those scenegraphs in the first place."*

**理由一：层级变换？** 绝大多数场景对象根本不带动画。把"每个节点都可能跟随父节点动"这条假设塞进整个对象数据结构，相当于为了少数动态对象付出对全部对象的内存、cache、遍历开销——这是典型的"为 1% 的用例优化 99% 的数据结构"。而且动画本身是**游戏逻辑**的事，不是 3D 引擎的事（引擎只需要关心 skinning 之类的提交阶段）。

**理由二：剔除？** 不同对象的最优剔除方式根本不一样：**地形**是层级 chunk / quadtree；**角色**是包围球加门限距离；**光源**需要自己特化的 [[tiled-light-culling|瓦片剔除]]；**阴影投射者**要走 [[shadow-caster-culling-front-back|额外的单独剔除]]。用一棵统一的 graph 做 [[culling|剔除]] 意味着对所有这些特殊场景都打折扣。

## 替代方案：按 renderable 类型特化

Pesce 的建议是：**3D 引擎根本不应该关心"object"这个抽象**。它应该提供：

- 图形设备管理（命令提交、资源绑定）
- 渲染服务与工具（材质系统、shader 基础设施）
- 多线程与提交调度
- 数学与几何基础函数
- 反射、序列化、内存管理

具体的 draw call 由**一组"渲染实体"**自己发起——每一种 renderable 都是为自己特化的代码路径：

- `terrain` —— 自己管自己的 chunk、LOD、**[[terrain-splatmap-shader-graph|splatmap]]**、culling
- `players` —— 自己管骨骼、动画、skinning
- `lights` —— 自己管光剔除与着色管线
- `shadows` —— 自己管 caster 收集与 [[shadow-mapping-basics|阴影图]] 生成
- ……

每一种都写得又快又专，各自最优。没有"万能引擎"的伪装，也就没有场景图这种为了容纳任意东西而存在的通用结构。

## 什么时候场景图反而合理

Pesce 并不是彻底否定。他指出场景图真正的使用场景是**"声称能渲染任何东西的通用引擎"**——Unreal、Gamebryo 这类。但讽刺的是，这些"通用引擎"其实也只做一类游戏。就算真的需要这种通用性，他建议也是做成"可配置的渲染实体工厂"：外部数据声明某个 3D 资源该由哪个 renderable 实例加载和渲染——**以数据驱动装配，而不是以父子树组织**。

## 两种立场并存

这种主张和 [[scene-graph-matrix-stack-visitor]] 代表的"矩阵栈+访问者"模式并不互相证伪。后者教的是：*"如果你已经决定要用场景图，请这样组织它"*，重点在把全局变换从节点拆出来，让多父亲、多 visitor 共享。Pesce 的立场是上一层：*"你真的需要场景图吗？"* 对 AAA 级专用引擎的答案通常是——不。

两种视角合起来就是：**小规模学习用、编辑器里的对象层级展示、DCC 工具**可以用 visitor 式场景图；**真正上生产的渲染引擎**应当按 renderable 类型分层特化，把场景图这一层整个抽走。

## 相关

- [[angelo-pesce]]
- [[scene-graph-matrix-stack-visitor]] —— 正面立场：如果一定要有场景图，该怎么组织
- [[engine-layering]]
- [[engine-thin-wrapper-per-genre]] —— 类似的"引擎该按品类特化"哲学
- [[data-driven-architecture]]
- [[false-abstraction]] —— 场景图就是 Pesce 眼里的典型"假抽象"
- [[rendering-pipeline]]
- [[culling]]

## Sources

- [[sources/c0de517e-pitfalls-of-experience]]
