---
tags: [source, software-design, ui, reactive, architecture]
date: 2026-04-19
sources: 1
---

# I is for Intent（Steven Wittens / acko.net）

[[steven-wittens]] 发表于 2024 年 2 月的长文，论点一句话：真正符合用户直觉的应用程序需要在 State 之前多一层 Intent，把"用户意图"作为可非法、可越界的 source of truth 持续保留，再派生为 State；[[intent-vs-state|相关概念页]] 展开。

## 摘要

Wittens 用虚构的 Stanley（强类型强事务派后端工程师）作为反面典型：其"不允许任何非法状态"的信仰在前端根本行不通。文章从文本编辑器的列号、spreadsheet 循环引用、git merge conflict、MVC 表单字段的 validated/unvalidated 分离一路举例，论证"validation 不是一次性归一化动作，而是持续且非破坏地从 Intent 派生 State"。工程上他主张把"变更"做成一等值（Update<T>），用 `patch(value, update)` 作为应用原语；Intent 和 State 的 Update 形状对称，可以只在一个地方接触原始 Intent；WYSIWYG 预览与撤销/重做都是同一机制的变体。他反对"后端拒收脏数据+前端自己兜"的传统切分，主张前端与后端并列而非后端在前端之前，GraphQL 是"只解了一半问题"的典型反例。最后串到 React/tree-sitter/Use.GPU 的共同底层：结构保留的增量变换器，让数据与代码有相同的形状。

## 关键要点

- Intent 层允许任意越界/不一致，State 层是 `validate(Intent)` 派生出来的合法子集
- 文本编辑器的"记忆列号"是最小可辨例子——用户体验要求保留非法 Intent
- `patch(value, update)` 作为一等变更：递归不可变 merge，数组原子处理，支持 lambda 表达 "append" 等操作
- `diff(A, B)` 是 `patch` 的补集，撤销/重做天然统一
- Schema 设计由读写路径驱动：`order: List<Id>` + `values: Map<Id, T>` 拆分让重排与编辑正交
- CRDT 不是 Intent/State 的替代；大多数场景 last-write-wins + 版本号 + 冲突提示已足够
- 前端与后端应并列，共享 patch 协议；GraphQL/REST 式的"前端在后端之前"是复杂度爆炸的真因
- React/tree-sitter/Use.GPU 是同一类 reconciler：一个函数的 state 就是下一个函数的 intent

## 链接到的概念

- [[intent-vs-state]]
- [[steven-wittens]]
- [[use-gpu-reactive-runtime]]
- [[reactive-ui-rust]]

## 原文

- 链接：https://acko.net/blog/i-is-for-intent/
- 本地：`raw/articles/acko.net/2024-02-05_i-is-for-intent.md`
