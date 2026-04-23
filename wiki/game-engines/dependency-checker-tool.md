---
tags: [游戏引擎, 工具链, 资源管理, 内容管线, bitsquid]
date: 2026-04-19
sources: 1
---

# Dependency Checker：资源依赖图的集中治理

一个中型项目的资产库稍一变大，就会跑出四个典型问题：

- **误删**：有人删了一个实体，结果某关卡引用了它，运行时才发现；
- **暗链**：改了一张贴图，发现它同时被三个物件共用；
- **不敢改名**：资源名拼错了，但它被太多处引用，没人敢动；
- **dead content**：项目里有一批"应该删，但不知道能不能删"的资源。

这四条背后其实是同一个缺失：**项目没有关于"谁引用谁"的权威索引**。Bitsquid 的解决办法是一个 500 行的小工具 —— [[niklas-frykholm|Niklas Frykholm]] 叫它 **Dependency Checker**。

## 为什么 500 行就够

前提来自两条架构纪律：

- 所有资源文件格式都基于 **SJSON**（Bitsquid 的 JSON 方言）；
- 跨资源引用一律写成 `(type, name)` 二元组。

基础统一之后，**解析任何一种资源来抽取依赖都是同一段代码**。没有自定义二进制、没有隐式引用、没有序列化框架里藏着指针。500 行就能覆盖全部类型。

## 能做什么

拿到完整依赖图之后：

- **Missing list**：被引用但文件不在——防误删、找拼写错；
- **Dangling list**：文件存在但无人引用——清 dead content 的依据；
- 点任一资源看 in / out edges，即时回答"这张贴图都被谁用"；
- **Replace**：把 `font_missing.tex` 的所有引用 patch 成另一张贴图，一次性修复；
- **Move**：rename 一个资源时同步改全部 referrer；
- **Copy** + 选择性重定向：克隆资源并把**子集**的引用切到副本——**按关卡 fork 资源**的自然入口。

## 工程启示

- **统一的文件格式与引用约定**把治理难度从 O(#格式) 降到 O(1)；相反，如果每个资源类型都要写自己的解析器，500 行会变成 5000 行，谁都不愿写；
- 依赖图是**所有资产治理功能的共同底座**——missing / dangling / replace / move / copy 五种操作都是"改图 + patch referrer"的同构变换；
- 作者说没做 CLI，是因为内部没需求；"trivially added"——治理工具的**数据层比 UI 层重要得多**。

## 和其他设计的对照

- 这条路线的上游是 [[decoupled-tool-engine-json-rpc|tool / engine 解耦架构]]：工具层持有完整 source 树的知识，runtime 层只消费编译产物。Dependency Checker 完全跑在工具层。
- 和 [[offset-based-resource-blobs]] 形成两端闭环：source 端用 SJSON + `(type, name)` 引用，runtime 端用 hash-to-pointer 解析——中间的 data compiler 是翻译器。
- 同时代很多引擎（Unreal 也是）后来都独立做了自己的依赖分析工具（Reference Viewer），本质思路一致：只有知道资源间的引用图，大项目才敢做破坏性操作。

## Sources

- [[sources/bitsquid-dependency-checker]]
