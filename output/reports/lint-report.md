---
tags: [lint, 健康检查]
date: 2026-04-05
---

# Wiki 健康检查报告

## 总体健康状况

**整体：良好。**

| 指标 | 值 |
|---|---|
| 总文件数 | 124 |
| 概念文章 | 92 |
| 源摘要 | 24 |
| 人物页 | 5 |
| 特殊页面 | 3（index、log、overview） |
| 源文件总数 | 24（全部覆盖） |
| 总 wikilink 数 | 882 |
| 唯一链接目标 | 137 |
| 平均每页入链 | ~7.1 |
| 最高入链数 | 25（deep-modules） |

**无坏链，无失效 frontmatter，无 index 遗漏。** 共发现 **28 个可改进点**，分布在 6 个类别。

## 关键发现

- **没有坏链**：所有 882 个 wikilinks 都能解析到存在的文件。
- **没有 frontmatter 缺失**：所有 121 个概念/源/人物页都有 tags/date/sources。
- **没有孤儿页**：所有页面至少被引用 1 次。
- **Index 完整**：123/123 非特殊页面都在 index 中。
- **24 个源都有摘要**，目录层级清晰。

---

## 🔴 优先级 1：连接性问题

### 低入链页面（≤ 2 个入链，除 index 外）

- [ ] **[[overview]]**（1 入链，仅来自 index）— 综合页本应是多入口枢纽，建议在至少一个每大类的顶层概念页（`complexity`、`rendering-pipeline`、`game-engine`、`elements-of-programming`、`memory-hierarchy`）底部添加一个"整体视角：[[overview]]"链接。
- [ ] **[[unity-complexity-patterns]]**（1 入链，仅来自 index）— 应至少从 [[classitis-in-games]]、[[ecs]]、[[resource-system-design]] 三个游戏开发页交叉引用。
- [ ] **[[continuous-design]]**（2 入链）— 应从 [[strategic-programming]] 和 [[zero-tolerance]] 互相引用（它们是同一个哲学簇）。
- [ ] **[[red-flags]]**（2 入链）— 应从 [[complexity]] 和 [[strategic-programming]] 引用，因为 red-flags 是识别 complexity 的工具。
- [ ] **[[stencil-buffer]]**（2 入链）— 应从 [[fragment-shader]]、[[z-buffer]]、[[early-z-late-z]] 中至少 1-2 处引用。
- [ ] **[[mttf-reliability]]**（2 入链）— 计算机系统板块孤立，与其它主题连接弱。可从 [[memory-hierarchy]] 末尾添加引用。
- [ ] **[[hennessy-patterson]]**、**[[jason-gregory]]**、**[[sussman-abelson]]**（2 入链，仅摘要页和 index）— 人物页天然入链少，但可以从各自领域的核心概念页末尾添加作者链接增强可访问性。

---

## 🟡 优先级 2：概念缺口

以下概念在多个文件中被提及但缺少专属页面：

- [ ] **BSP Tree**（3 处提及）— engine-evolution 的关键历史节点，第一代可见性解决方案，可以作为独立页纳入 `rendering/` 或新建 `rendering/visibility-algorithms/`。
- [ ] **Lumen**（7 处提及）— UE5 动态 GI 系统，在 engine-evolution、deferred-rendering 中反复出现，应有独立页。
- [ ] **Nanite**（8 处提及）— UE5 虚拟几何系统，类似 Lumen，提及频繁但无页。
- [ ] **SRP Batcher**（6 处提及）— Unity 性能优化核心工具，在 draw-call、batching、unity-vs-unreal 中反复出现，值得独立页。
- [ ] **GPU Instancing**（6 处提及）— 批处理的关键具体技术，在 draw-call、batching、culling 中出现，值得独立页。
- [ ] **Burst**（5 处提及）— Unity DOTS 的关键编译器，在 ecs、aos-vs-soa 中被多次引用。
- [ ] **G-Buffer**（4 处提及）— deferred-rendering 的核心概念，可独立成页或在 deferred-rendering 中扩展描述。
- [ ] **Portal + PVS**（3+2 处提及）— engine-evolution 的第二代可见性方案，与 BSP Tree 并列应有页。
- [ ] **Depth Pre-Pass**（3 处提及）— early-z-late-z、hsr-tbdr、overdraw 共同优化手段，可作为独立页或扩展 z-buffer 页。
- [ ] **LOD（Level of Detail）**（3 处提及）— culling 层级的关键技术，值得独立页。

---

## 🟡 优先级 3：缺失的交叉引用

Related/相关 区建议补充的连接：

- [ ] **[[shallow-modules]]** 应在 Related 中显式链接到 [[classitis-in-games]]——游戏开发中的具体体现。
- [ ] **[[z-buffer]]** 应链接到 [[stencil-buffer]]（技术上相邻，常并存使用）。
- [ ] **[[alpha-blending]]** 应链接到 [[overdraw]]（透明物体的 overdraw 特别严重）。
- [ ] **[[aliasing]]** 应链接到 [[perspective-correct-interpolation]]（插值/采样是相关主题）。
- [ ] **[[coordinate-spaces]]** 应链接到 [[rasterization]]（Screen Space 由光栅化使用）。
- [ ] **[[amdahls-law]]** 应链接到 [[aos-vs-soa]]（提高有效 p 值的手段）—— aos-vs-soa 已链接到 amdahls-law 但反向缺失。
- [ ] **[[dependencies]]** 应链接到 [[engine-layering]]（引擎分层原则的抽象基础）。
- [ ] **[[information-hiding]]** 应链接到 [[procedural-abstraction]]（同一思想的两次表达）。
- [ ] **[[strategic-programming]]** 应链接到 [[red-flags]] 和 [[continuous-design]]（同一哲学簇）。
- [ ] **[[complexity]]** 应链接到 [[red-flags]](识别工具)。
- [ ] **[[higher-order-functions]]** 应链接到 [[lambda-calculus]]（已有）和 [[closure]]（高阶函数 + 闭包密不可分）。
- [ ] **[[closure]]** 应链接到 [[higher-order-functions]]。

---

## 🟢 优先级 4：数据缺口

以下主题在 wiki 中较薄弱，可收集更多源：

- [ ] **Clean Code / Robert Martin 的视角**——目前 APoSD 与 Clean Code 的冲突只在 APoSD 一方讲述；收录 Clean Code 原始论点会让对照更完整。
- [ ] **设计模式（GoF）**——多处提到"GoF 模式经常是浅模块"，但没有设计模式本身的专门分析页。
- [ ] **渲染的光照/阴影章节**——RTR 只覆盖前 6 章（管线），Shading、Lighting、Shadow Mapping、PBR 等核心渲染内容未收录。
- [ ] **动画系统**——GEA 和 Unity 的动画系统未收录。
- [ ] **物理引擎**——提及多次（PhysX/Havok），但没有专门页。
- [ ] **数据抽象（SICP 第 2 章）**——SICP 只覆盖第 1 章（过程）；第 2 章（数据抽象、tagged data、generic operations）未收录。
- [ ] **环境模型与状态（SICP 第 3 章）**——当代换模型失效时如何推理。

---

## 🟢 优先级 5：样式一致性

- [ ] **[[custom-srp]]** 使用 `## 相关概念` 而其他所有页用 `## 相关`——统一为 `## 相关`。

---

## 🟢 优先级 6：待研究的问题

lint 过程中浮现的、可以作为后续 query 的问题：

- [ ] **「深模块 vs SRP」的张力如何解决？**——Ousterhout 与 Clean Code 在此直接冲突。是否有统一框架？是否能从 SICP 的过程抽象里推出判断准则？
- [ ] **数据导向设计（DOD）vs 面向对象设计（OOP）的工程权衡**——ECS/SoA 的性能优势 vs OOP 的可维护性优势。在游戏引擎的实战中如何划分边界？
- [ ] **技术债的偿还周期规律**——从 BSP 到 Lumen 每个架构都偿还了前代的债务。是否存在可预测的"债务周期"？[[engine-evolution]] 中有讨论但未系统化。
- [ ] **移动端 GPU 架构的未来**——TBDR 的带宽优势会延续吗？Apple Silicon 模糊了 mobile/desktop 界限后，这一分野还存在吗？
- [ ] **Amdahl 定律的实际 p 值测算方法**——理论清晰，但团队实际做 DOTS 重构前如何评估回报？
- [ ] **游戏引擎的边界应该怎么划？**——GEA Day 1 说这个边界是"动态的"，但实战中如何做决策？

---

## 建议新增源

- **Clean Code**（Robert Martin）——与 APoSD 的直接对照。
- **Game Programming Patterns**（Robert Nystrom）——补充 GEA 的模式视角。
- **Physically Based Rendering**（Pharr et al.）——扩展渲染数学基础。
- **SICP 第 2、3 章**——补齐语言基础。
- **Patterns of Enterprise Application Architecture**（Fowler）——架构层面的对照。

---

## 健康度评分：A-

| 维度 | 评分 | 说明 |
|---|---|---|
| 完整性 | A | 所有源都有摘要，index 完整 |
| 正确性 | A | 无坏链，无矛盾 |
| 连通性 | B+ | 少数页入链偏低 |
| 一致性 | A- | 格式高度一致，仅 1 处小偏差 |
| 深度 | A | 核心主题覆盖深入 |
| 广度 | B | RTR/GEA/SICP 只覆盖前几章 |

**核心建议**：优先处理优先级 1-2 的事项（低入链和概念缺口），能快速提升知识库的可发现性与完整性。
