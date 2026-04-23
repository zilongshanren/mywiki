---
tags: [引擎架构, 场景图, data-oriented, bitsquid]
date: 2026-04-19
sources: 1
---

# 按实体组织的场景图

"场景图（scene graph）"这个词在教科书里往往指**一棵覆盖整个世界的树**，每个节点是一个可渲染对象，父子关系表达变换继承。[[niklas-frykholm|Niklas Frykholm]] 在 Bitsquid 的实践里走了相反一步：**场景图只覆盖一个 entity 内部**，entity 与 entity 之间没有共同的场景图根。

这是一个看起来简单、但把后续一堆数据结构问题都消掉的决定。

## 为什么要这么拆

一个角色 entity 可能有骨骼 / 蒙皮 mesh / 武器挂点，这些之间需要 parent-child 的变换继承——于是在 entity 内部保留一棵小场景图。但整个世界里不同 entity 之间**很少需要变换继承**：怪物 A 和怪物 B 之间没有"A 是 B 的父节点"这种关系，最多是临时父子化（角色拿起某个物体），而这通过在那一刻做 matrix concat 即可解决，不需要常驻在同一棵树里。

一旦场景图只在 entity 内部，每棵树都很小（十几到几十个节点）、而且**生命周期绑定到 entity**——entity 活着时树结构几乎不变。

## 连带后果：增删不是常见操作

在常见"全局场景图"里，增删节点是高频操作——每创建一个对象就要挂进树里，每销毁就要从树里拔掉。于是需要复杂的数据结构（双向链表、hash、slot-map 之类）来让 O(1) 增删成立。

Frykholm 对此直接回答："我们的场景图不常做这些事。"

- **添加节点**：典型情况是作为叶子加到末尾（比如给角色装备新部件），直接 append 到数组末尾即可；
- **删除节点**：不做也没关系——老节点可以就留在数组里，反正 entity 生命期结束时整个场景图一起释放；
- **重链接父子关系**（比如把骨骼层级改掉）：数组中间的元素要移位，成本高——但这在正常工作流里几乎不会发生，"你不会在运行时把手从肩膀之前挪到之后"——所以用慢路径专门处理即可。

这是典型的 [[data-driven-architecture|数据导向]] 思路：**识别常见情况，为它把数据结构做到极致；罕见情况用普通代码处理**。场景图数据在数组里线性排布，每帧遍历做 transform propagation 时完全是 cache-friendly 的顺序读写，这正是做实时性能所需要的。

## 对增删复杂度的理论松绑

如果设计者把"场景图"直接理解成"全局层级容器"，就会落入一定要优化 `remove_node` 的陷阱。Frykholm 的反例说明：**把问题重新 frame**——"场景图只用在 entity 内部"——比"想办法把 remove 做成 O(1)"更根本。

这和 [[scene-graph-unnecessary-in-engine|cloudwu 认为引擎内不需要场景图]] 的观点方向一致：都是在问"你真的需要一个通用、全局的层级结构吗"。区别是 cloudwu 直接砍掉场景图、让变换在 gameplay 层算；Frykholm 保留了场景图但**把它限定在一个 entity 里**，作为 mesh 关节层级的工具。两条路都能工作，共同点是拒绝让场景图承载过多职责。

## 相关
- [[scene-graph-unnecessary-in-engine]]
- [[scene-graph-matrix-stack-visitor]]
- [[data-driven-architecture]]
- [[ecs-data-oriented-revert]]
- [[niklas-frykholm]]
- [[ragdoll-velocity-inheritance]] — 场景图常驻 last_world 是 Bitsquid 给 ragdoll 速度继承的选择

## Sources

- [[sources/bitsquid-practical-dod-scene-graphs]]
