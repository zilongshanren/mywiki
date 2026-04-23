---
tags: [source, bitsquid, 资源管理, 工具链, 内容管线]
date: 2026-04-19
sources: 1
---

# The Dependency Checker（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 10 月的文章，介绍 Bitsquid tool chain 里一个 500 行的小工具——Dependency Checker。

## 摘要

项目越做越大会遇到四种典型痛点：有人误删一个被某关卡引用的实体；有人为了让一个物件更好看改了某张贴图但忘了它被另两处共用；有个资源名字拼错了但没人敢改，因为被引用太多处；项目里有一批"dead resources"谁都不知道能不能删。Bitsquid 用一个**集中式 Dependency Checker** 解决这类问题：工具懂所有 Bitsquid 资源文件格式（全部基于 **SJSON**，引用方式统一是 `(type, name)` 对），遍历 source 树就能建立完整的依赖图。这段解析 + 改写逻辑一共只要 500 行——这是"统一文件格式"最大的红利。有了依赖图就能做：列出缺失资源（被引用但文件不存在）；列出悬空资源（文件存在但没人引用，可以安全删除）；点一个资源看它的 in / out 依赖；以及最有价值的——**把引用替换/移动/复制**。把缺失的 font 贴图替换成别的、rename 一个资源时同步 patch 所有引用它的文件、copy 一份资源并选择性地把部分引用重定向到副本（相当于"按场景 fork"）。

## 关键要点

- **前提**：所有资源文件格式都走 SJSON + 统一的 `(type, name)` 引用；统一基础才能让 500 行吃下全部格式；
- 依赖图是所有资产治理功能的共同底座；
- **missing / dangling** 两条列表的价值：前者帮防误删、后者帮清 dead content；
- **replace / move / copy** 三种图变换，都是"改依赖 + patch 所有 referrer"的同构操作；
- copy + 选择性重定向 = 按需 fork 资源——例如把 `key` 实体在 `himalaya` 关卡里用一份特化版本；
- 对外暴露的只是 UI，但核心价值是**把人工记忆在资源间的引用关系显式化**；
- 评论里有人问 CLI——作者说没做，但"trivially added"。

## 链接到的概念

- [[dependency-checker-tool]]
- [[decoupled-tool-engine-json-rpc]]
- [[handle-based-resource-manager]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/10/dependency-checker.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-10-05_the-dependency-checker.md`
