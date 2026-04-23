---
tags: [luajit, x86-64, 虚拟内存, 分配器, x-plane]
date: 2026-04-19
sources: 1
---

# LuaJIT 2.0 的「低 2 GB」地址空间约束与 X-Plane 的预占式 workaround

LuaJIT 2.0 在 x86_64 上有一条与"64 位就该有大地址空间"的朴素预期相悖的硬性约束：**所有 Lua 堆分配必须落在进程的前 2 GB 地址空间内**。这个限制来源于 LuaJIT 内部广泛使用**偏移地址**——这些偏移是 signed 32-bit，表示范围只有 [−2 GB, +2 GB)，为了让偏移永远能覆盖堆内任意一对指针，整块 Lua 堆必须塞进 **0x00000000–0x7FFFFFFF** 这段低地址。这是一种用地址空间换指令密度的设计（32-bit 偏移比 64-bit 绝对地址在指令 encoding 上短得多，对 JIT 出来的代码 cache 友好）。

[[ben-supnik|Supnik]] 2012-12 为把 LuaJIT 以 64-bit 集成进 X-Plane 写了一篇踩坑记录，把围绕这条约束的**实际工程路径**描清楚了：OS 行为、时序问题、到修 LuaJIT 源码。

## 与 OS X 默认行为的冲突

OS X 64-bit 程序默认把"零页"扩到**整个低 4 GB**——任何落在低 4 GB 的访问都会立刻 SIGBUS。目的是把"指针被误截断到 32-bit"这种历史遗留 bug 直接炸出来：截断后的指针必然落在非法页，一访问就崩。

这个安全网和 LuaJIT 的"必须分到低 2 GB"**直接冲突**。集成的第一步就是定制 zero page 大小，让 0–2 GB 可用。OS X 在链接时可以通过 `-pagezero_size` 选项（或等价的 `__PAGEZERO` segment 改动）把零页压到 4 KB。

## 真正难的是**时序**：低 2 GB 会被先占走

X-Plane 的插件在用户**换飞机**时才加载——这是程序启动后分钟级的事件。问题是：这时候**低 2 GB 地址空间早已被系统 malloc 与 OpenGL 驱动的各种内部分配吃掉了**。`vmmap` dump 证实这两个 consumer 偏好低地址（一样是为了节省 allocator metadata 上的指针宽度）。

LuaJIT 启动时向 OS 要内存，拿到的基本都是 > 2 GB 的高地址，直接失败。

## Workaround：sim 启动时预占 1.6 GB + 自定义 allocator

Supnik 的做法是把这条约束从"分配时处理"提前到"进程启动时处理"：

1. **host sim 启动阶段**就向 OS 预申请最大限度的低 2 GB 虚拟地址空间，按**固定大小的 chunk**（当前 32 MB）一块块抓。目标是把低 2 GB 的 VM 地址**占住**，不让系统 malloc 和 GL 驱动抢走。
2. 实现一个 Lua 端的 **custom realloc**，内部基于 hack 过的 **dlmalloc**：dlmalloc 的内部池直接建立在第 1 步预抓的 32 MB chunk 之上，不再向 OS 要内存。
3. 插件 Lua runtime 通过 `lua_newstate(custom_alloc, ...)` 把这个 allocator 注入进 LuaJIT。

**关键 OS 行为**：OS X 对 VM 地址是**懒提交**的——`mmap` 1.6 GB 不会立刻把 1.6 GB 物理内存绑上去，只是把虚拟地址"占座"；真正 dirty 的页才占物理内存。所以 sim 启动时"占 1.6 GB"成本接近 0。后续 GL 驱动/系统 malloc 要新 VM 时，**必然**分到 2 GB 以上的高端——因为低端已经被 X-Plane 占走。

这是一种把"VM 地址占位"当做**资源预留锁**的用法，和 [[virtual-memory|虚拟内存与物理内存解耦]] 的典型利用方式一致。

## 要改 LuaJIT 源码

LuaJIT 2.0 的 shipping 代码里，**`lua_Alloc` 注入 API 在 64-bit 下被 `#define` 掉了**——上游假设客户端不会遵守"低 2 GB"这条规矩，干脆在 64-bit 编译时禁掉自定义 allocator，强制用 LuaJIT 内部分配器（它自己会想办法在低 2 GB mmap）。

X-Plane 用的是插件动态注入 Lua 的场景，内部 allocator 此时已经无计可施。Supnik 的补丁把那几条 `#define` 打开——API 本来就是完整的，只是被 stub 掉了。这一步必须修上游源码，无法绕。

## 实现限制

- **单次分配 ≤ 32 MB**。dlmalloc 的 direct-allocation 路径（走 `mmap`）在这套 hack 下被禁用——因为它会向 OS 要新 VM，绕过池。要求大于 chunk 的分配就直接失败。实用上 Lua 脚本的典型负载远小于这个阈值；真遇到就把 chunk size 调大。理论上可以让池在已有 chunk 间搜索连续区域凑 > 32 MB 的块，但 Supnik 认为不值得做。
- **同时只有一个插件能加载 LuaJIT**。这不是 2 GB 约束带来的，是另一条独立的 LuaJIT 集成坑：Lua plugin 往往把整套 LuaJIT runtime 的符号 export 成全局 dynamic symbol，多个插件同时加载导致符号互相覆盖，runtime state 打架。那是另一篇博客的主题。

## 连接到更大的图景

这个案例示范了几件事：

- **JIT 的指令密度/性能优化会侵入进程级地址布局约束**——不是"语言/runtime 的内部事务"。V8、JavaScriptCore 等现代 JIT 也都有类似的 low-address 或 heap-locality 要求。
- **插件/runtime late-load 场景**天生和低地址约束冲突——宿主程序**必须**在启动阶段就介入 VM 布局。这是把 [[custom-allocator-interface|自定义分配器抽象接口]] 从"性能/预算工具"升级为"地址空间预留工具"的现实案例。
- OS 的懒提交 VM 语义是**低成本预留**的使能前提——在没有 overcommit 的系统（某些配置的 Linux、Windows）上同样技巧需要额外的 `MEM_RESERVE vs MEM_COMMIT` 拆分。

更细的内存/指针宽度背景：[[x64-platform-tidbits]] 讨论 x86-64 上 C 提升规则带来的指令膨胀；[[lp64-vs-llp64]] 讨论 int/long/pointer 宽度在不同 64-bit 平台上的分裂——都是同一类"64 位抽象会从边缘漏出"的题材。

## 相关

- [[virtual-memory]] —— 懒提交 VM 是本方案的使能前提
- [[custom-allocator-interface]] —— `lua_newstate` 的自定义 allocator 接口是底层机制
- [[lua-memory-profiling]] —— LuaJIT 的内存诊断主题页（不同问题，同一层）
- [[lua-incremental-gc]] —— 标准 Lua 5.1 GC，LuaJIT 有自己的替代方案
- [[lp64-vs-llp64]]
- [[x64-platform-tidbits]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-luajit-x-plane-64bit]]
