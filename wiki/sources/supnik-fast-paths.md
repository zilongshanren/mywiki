---
tags: [source, api设计, opengl, x-plane, 性能]
date: 2026-04-19
sources: 1
---

# Fast Paths（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 1 月的文章，从 OpenGL 驱动实现和 X-Plane SDK 设计两个角度提炼出的 API 快慢路径原则：**API 设计时关心「快路径能不能被挡住」，API 实现时关心「默认行为对总体性能的影响」**，两个问题不要混着答。

## 摘要

开场是 OpenGL 驱动面对冗余 `glEnable` 的两种选择：查状态避免冗余（对粗心客户端省开销、对仔细客户端多一次 1-bit 比较）vs 总是执行（对仔细客户端提供最快路径）。Supnik 说两种都合理，但驱动必须**明文声明哪条路径快**，否则两类客户端都输。正面例子是 X-Plane SDK 的 `dataref`：`XPLMFindDataRef` 是「慢」操作（字符串→handle，应在 init 期缓存），`XPLMGetDataf/SetDataf` 是「快」操作（handle→数据，Sandy 和 Ben 会盯住代码开销、故意不做校验）。把慢和快拆成不同函数名，而不是「同一入口内部分流」，让客户端从代码里就能看出性能等级。快路径不做校验意味着传错 handle 导致不确定行为（nasal demons）——这是接受的失败模式，用以保证好写的插件不被糟糕插件拖累。文末附 C switch fall-through 的例子：70 年代编译器装不下内存，语法本身承载「程序员不明写最优代码就不会有最优代码」这条前提；现代语言（Go/Rust）禁止 fall-through 是在换权。

## 关键要点

- 把高频操作和低频操作拆成**不同函数名**，而不是同一函数内部分流——编译器优化和人类阅读都受益。
- 快路径故意不校验是合法设计，但必须配套写清契约（有效前置条件、失败模式）。
- 一旦宣告「这条慢」，客户端就会做缓存；实现端后来优化的收益不消失，因为**文档契约比实现契约更长久**。
- X-Plane 的 `XPLMFindDataRef` 原先是线性的，改成对数时间后客户端代码完全不动——正是文档契约带来的弹性。
- 驱动级状态缓存在真实 3D 引擎里收益比想象的低——X-Plane 每帧相机角度不同，state snapshot 重复度极低。

## 链接到的概念

- [[api-fast-path-design]]
- [[rendering-api-depth]]
- [[information-hiding]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2010/01/fast-paths.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-01-14_fast-paths.md`
