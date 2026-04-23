---
tags: [source, bitsquid, 系统设计, 耦合, 引擎架构]
date: 2026-04-19
sources: 1
---

# Managing Coupling（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 1 月 Bitsquid Blog。系列第一篇，讲引擎内部子系统解耦的**四条实操原则**。原文最先发在 AltDevBlogADay。

## 摘要

"维持一个大型复杂软件系统神志清醒的唯一办法，是把它视作许多更小、更简单的系统的集合；而这只有在这些系统被合理解耦之后才可能。"每个子系统应独占自己的数据结构、`update()`、文件目录；新人看一个子系统时应只需读那一个目录的文件；整块重写或删除都不应影响其他代码。完全隔离不可能，关键是在必须的交互前**保住这种隔离感**。Niklas 把**"想在 toy project 里验证想法，而不是直接在引擎里试"**这个直觉列为耦合过度的信号。他也直言**coupling creep**：deadline 一到就有人开后门，久而久之就烂。

针对"烂"的四条反制：
1. **警惕 framework** —— root class、RTTI、序列化、refcount 这种全局设施会强制所有子系统接受某个设计选择，侵入深后反而不可改。每个子系统自己的 `save/load` 往往更干净。
2. **用高层调度低层** —— 脚步声需要 anim + material + sound 三家，但三家互不相识；gameplay 层在 Lua/Flow 里 poll + 粘合，**语言边界是天然防火墙**，防止乱糟糟的逻辑渗回 clean engine core。
3. **代码重复有时是对的** —— 共享代码**增加系统耦合**。滥用 `String`、强签名 `const Vector<T>&`、为重用 10 行而搭共享库引入 `#define TOOL_COMPILE`……这些都是代价。问题从来不是多写 10 行代码，是那些阻止你写代码的 coupling。
4. **用 ID 而不是指针引用外部对象** —— 裸指针 / `shared_ptr` 把生命期权交出去；`weak_ptr` / handle 还是让两系统共享间接指针，阻碍 reorganize / double-buffer / threading。ID 是 POD，没有释放动作，可以随便拷贝/DMA/给 Lua；内部用固定大小 `Object *lookup[MAX]` + `(index, unique)` 组合 ID + **in-place free list** 做映射，失败是明确 API。

## 关键要点

- **Framework 嫌疑名单**：root class、RTTI/reflection、serialization、refcount——它们的"易维护"经常是 early-stage 幻觉，后期会绑死整个引擎。
- **Engine core vs gameplay glue** 分层：clean core / messy glue；后者关在脚本语言里作为防火墙。
- **DRY 的代价**是 coupling：`const Vector<T>&` 换成 `const T* begin, const T* end`，API 受众广一倍。
- **Tool 与 Engine 分离**：C# 工具重写 bundle header 解析是对的，剥库 + `#define TOOL_COMPILE` 是错的。
- **ID 引用**：位宽切分（12 位 index + 20 位 unique）、`lookup[]` 数组 + in-place free list、失败返回 null；评论里补充 "null 对象" 技巧——0 号 slot 作可读写但无害的对象，读写失效 ID 变成无分支安全操作。
- **`std::map` 不算"快的 map"**——作者直言。
- **共享 lookup 查询成本**：ID → 对象要经过一次 array + valid check；branch hint 后基本免费；作者主张 ID 用在"相对粗粒度的 setter/getter"上，而不是每帧每对象的 hot path。
- **对象删除时机**：Niklas 的做法是把 delete 延后到明确同步点（与 background 处理不冲突的时机），而不是加锁保护当前执行。

## 链接到的概念

- [[system-decoupling-patterns]]
- [[polling-callbacks-events]] — 本系列第二篇
- [[id-based-lifetime-with-kill-flag]]
- [[handle-based-resource-manager]]
- [[c-opaque-struct-modules]]
- [[decoupled-tool-engine-json-rpc]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/01/managing-coupling.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-01-30_managing-coupling.md`
