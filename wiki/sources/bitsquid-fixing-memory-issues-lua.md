---
tags: [source, bitsquid, lua, 内存诊断, 垃圾回收]
date: 2026-04-19
sources: 1
---

# Fixing memory issues in Lua（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 8 月的文章，把 Lua 在游戏项目里的内存问题分两类——**用得太多**与 **GC 跑太久**——并给出针对每类的诊断与修法。

## 摘要

**问题 1（用得太多）**：给出一份 Lua 内置可跑的 `count_all(f)` 函数——从 `_G` 递归 DFS 所有 table 与 userdata，对每个首次见到的对象调 `f`。配上 `type_name(o)`（利用"全局类对象同时是 metatable"的模式反查名字）就能做**按类型计数**——`AiPathNode` 在涨就定位到泄漏源。扩展 `count_all` 沿途记录 key 路径即可报出 `_G.managers.ai_managers.active_paths[2027]` 这种完整追溯。

**问题 2（GC 太慢）**：先用 `lua_gc(L, LUA_GCSTEP, 0)` 循环跑固定毫秒预算；再用**反馈回路**让 garbage 比例稳在 10 %（超则加预算，低则减）。作者给出平衡方程：sweep 速率 `s ≤ g / a`——总内存 m 消掉了，决定 GC 工作量的只有**垃圾生成速率 g** 和**允许占比 a**；a ≤ 1 是硬上限，所以长期解只有降 g。降 g 的具体招：改更新现有 table、返回引用、函数多返回值而非 table、池复用、少字符串拼接。

**定位垃圾热点**：等游戏进稳态（总 Lua 内存不变），此时任何 alloc 都是即将回收的 garbage；给 `lua_Alloc` 挂 hook，用 `lua_getstack` 抓 Lua 调用栈、`murmur64(stack_frames)` 聚合到 HashMap，按 alloc_count 排序就是 top 热点清单。作者经验："花几小时修最大几个热点，GC 时间通常降一个数量级。"

## 关键要点

- **`count_all(_G)` + type_name** → 按类型计数定位内存主角；
- 改造 count_all 沿路径累加即可输出**从 `_G` 到泄漏点的完整 key path**；
- GC：**step 0 + 固定 ms 预算**；可搬到后台线程；
- **feedback 回路**让 `garbage / total ≈ 10 %`，画曲线防振荡；
- 平衡方程 `s ≤ g / a`：**总内存不重要、垃圾生成速率决定 GC 成本**；
- 降 g 的工程技巧：更新而非新建 table、返回引用、多返回值代替 table、池复用、少字符串拼接；
- **稳态时任何 alloc 都是 garbage** —— 用 `lua_Alloc` + Lua stack trace hashmap 抓热点；
- 前提：C 侧绑定不自己造垃圾（详见 [[lua-light-userdata-bindings]]）；
- 假设：标准 Lua 5.1 GC；LuaJIT GC 不同，策略要移植。

## 链接到的概念

- [[lua-memory-profiling]]
- [[lua-incremental-gc]]
- [[lua-light-userdata-bindings]]
- [[non-cryptographic-hash]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/08/fixing-memory-issues-in-lua.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-08-09_fixing-memory-issues-in-lua.md`
