---
tags: [source, luajit, x86-64, 虚拟内存, x-plane]
date: 2026-04-19
sources: 1
---

# Integrating LuaJIT with X-Plane: 64-bit Fun（Ben Supnik / The Hacks of Life）

[[ben-supnik|Supnik]] 2012-12-09 记录把 LuaJIT 2.0 以 64-bit 集成进 X-Plane 插件架构时遇到的**地址空间约束**与实际 workaround。

## 摘要

LuaJIT 2.0 在 x86_64 上要求所有 Lua 堆分配落在进程前 2 GB 地址空间——根源是内部使用 signed 32-bit 偏移。OS X 64-bit 程序默认把零页扩到低 4 GB（用于捕捉指针截断 bug），第一步是缩零页让 0–2 GB 可用。真正难的是时序：X-Plane 插件在**用户换飞机**时才加载 LuaJIT，此时低 2 GB 已被系统 malloc 和 OpenGL 驱动占走。Supnik 的解法是 host sim 启动阶段就用 **32 MB chunk** 预占最多 1.6 GB 低 2 GB VM，然后给 Lua 挂一个基于 **hack 过的 dlmalloc** 的 custom realloc，dlmalloc 的内部池用这些预抓 chunk 做 backing，最后通过 `lua_newstate` 注入插件。OS X 的**懒提交 VM** 让"占 1.6 GB"成本近 0——只有真正 dirty 页才吃物理内存；后续 GL 驱动要新 VM 时被迫分到 2 GB 以上的高端。附带要打开 LuaJIT 2.0 在 64-bit 下被 `#define` 掉的 `lua_Alloc` 自定义 allocator API。

## 关键要点

- LuaJIT 2.0 x86_64 要求 Lua 堆在前 2 GB 地址空间（signed 32-bit 偏移的硬限）。
- OS X 零页默认覆盖低 4 GB——捕捉 32-bit 指针截断 bug 的安全网，要 `-pagezero_size` 缩小。
- **时序问题**：late-load 插件开始分配时低 2 GB 已被系统 malloc + GL 驱动占走——`vmmap` 证实两者都偏好低地址（节省 allocator metadata 上的指针宽度）。
- **解法（三步）**：(1) host sim 启动即预抓最多 1.6 GB 低 2 GB VM；(2) hack dlmalloc 把这些 32 MB chunk 当内部池；(3) 插件 `lua_newstate(custom_alloc, ...)`。
- **懒提交 VM** 让 1.6 GB 预占几乎零成本；后续 GL/system malloc 被迫分高端。
- 必须改 LuaJIT 源码——上游 shipping 代码在 64-bit 下 `#define` 掉了自定义 allocator API，假设客户端不守 2 GB 规矩。
- **限制**：(a) 单次分配 ≤ 32 MB（dlmalloc 的 direct-allocation 路径被禁）；(b) 同时只有一个 Lua 插件能跑（另一条独立坑：插件 export 全 runtime 符号到全局，多插件相互覆盖）。

## 链接到的概念

- [[luajit-2gb-address-constraint]]
- [[virtual-memory]]
- [[custom-allocator-interface]]
- [[lua-memory-profiling]]
- [[lua-incremental-gc]]
- [[x64-platform-tidbits]]
- [[lp64-vs-llp64]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2012/12/integrating-luajit-with-x-plane-64-bit.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2012-12-09_integrating-luajit-with-x-plane-64-bit-fun.md`
