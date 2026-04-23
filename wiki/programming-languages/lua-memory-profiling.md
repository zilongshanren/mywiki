---
tags: [lua, 内存诊断, 垃圾回收, 性能优化, bitsquid]
date: 2026-04-19
sources: 1
---

# Lua 内存诊断与 GC 预算反馈控制

[[niklas-frykholm|Niklas Frykholm]] 2011 年的这篇把 Bitsquid 真实项目里遇到的 Lua 内存问题拆成两类：**用得太多**（泄漏 / 数据结构臃肿）和 **GC 跑得太久**（每帧停顿过大）。每一类都有一套**不依赖 profiler 工具链**的诊断手法。

所有手法都建立在"[[lua-light-userdata-bindings|C 绑定尽量不产生垃圾]]"之上——否则 Lua 程序员怎么努力都救不回来。

## 问题 1：Lua 用了太多内存

### 用 Lua 盘点 Lua 对象

要定位"谁在占内存"，通常的想法是给 `lua_Alloc` 挂 hook 追分配。作者给出一个更轻的做法：**用 Lua 自己遍历 Lua**——

```lua
function count_all(f)
    local seen = {}
    local count_table
    count_table = function(t)
        if seen[t] then return end
        f(t)
        seen[t] = true
        for k,v in pairs(t) do
            if type(v) == "table" then
                count_table(v)
            elseif type(v) == "userdata" then
                f(v)
            end
        end
    end
    count_table(_G)
end
```

从 `_G` 递归 DFS，每遇到一个没见过的 table 或 userdata 就调用 `f`。按需再补上 registry、metatable、function upvalues 的遍历，就覆盖了整个可达对象图。

### 按类型计数

`count_all` 最朴素的用法是**按类型计数**：

```lua
function type_count()
    local counts = {}
    count_all(function(o)
        local t = type_name(o)
        counts[t] = (counts[t] or 0) + 1
    end)
    return counts
end
```

`type_name` 取决于项目 class 系统——Bitsquid 的典型模式是全局类对象同时是实例的 metatable：

```lua
Car = {}; Car.__index = Car
function Car.honk(self) print "toot" end
local my_car = setmetatable({}, Car)
```

于是构造 `global_type_table` 一次性把 `_G` 里所有值反向映射到名字（`Car → "Car"`），`type_name(o)` 就是 `global_type_table[getmetatable(o)]`。

### 定位泄漏路径

数字只告诉你"`AiPathNode` 在持续变多"，要抓到**从 \_G 怎么走到它**，就把 `count_all` 改成沿路径 push/pop key 名：

```
_G.managers.ai_managers.active_paths[2027]
```

一眼看出是 `active_paths` 没清。这种**带路径的对象图遍历**是 Lua 独有的廉价工具——同样的事在 C++ 里要上 Valgrind。

## 问题 2：GC 跑得太慢

### 每帧固定预算 + LUA_GCSTEP

Lua 默认 GC 方案（哪怕是 [[lua-incremental-gc|5.1 的增量式]]）在实时程序里直接跑会产生可感知 hitch。标准做法是用 step 0 + 手动配预算：

```cpp
auto start = time();
while (milliseconds_elapsed_since(start) < milliseconds_to_run)
    lua_gc(L, LUA_GCSTEP, 0);
```

任何非 Lua-running 的线程都能跑 GC——主线程在做非 Lua 的事时把 GC 丢到后台线程，能进一步把总停顿时间摊到帧边缘。

### Feedback 控制：让 garbage 占比稳在 10%

难题是"每帧给多少毫秒"。作者用**反馈回路**：动态调整 GC 预算，使得 garbage 始终 ≤ 10 % 总 Lua 内存。超过就加预算，低于就减。和所有 feedback 系统一样，最好画出 `memory(t)` / `gc_time(t)` 曲线，确认收敛而不是振荡。

作者给了简洁的平衡方程。令 `g` 为程序每秒产生的垃圾、`s` 为 GC 每秒清扫的字节数、`a` 为允许的 garbage 占比：

- 扫完全部内存 `m` 的时间 `t = m / s`；
- 在 `t` 内产生的垃圾必须 `t·g ≤ a·m`；
- 代入消掉 `m`：**`s ≤ g / a`**。

三条有意思的推论：

1. **`m` 消失了**——真正决定 GC 工作量的是**垃圾生成速率**，不是总内存大小；
2. **预算与 g 线性相关、与 a 反相关**——堆得起更多内存（大 a）就可以少跑 GC；
3. **a ≤ 1 是硬上限**——真正 sustainable 的优化是降低 `g`，不是让你自己堆 a。

### 降 g 的 5 个重构招

- **更新现有 table 而非新建**；
- **返回成员引用而非拷贝**，必要时再复制；
- **函数用多值而非 table 包裹**：`make_point(2,3)` 而非 `make_point({2,3})`；
- **真要临时对象时做池复用**；
- **少做字符串拼接**。

## 用 lua_Alloc stack trace 抓垃圾热点

要把"哪行代码在造垃圾"定位到具体 Lua 栈，作者的做法很具体：等**游戏进入稳态**（Lua 总内存不增不减），此时任何 alloc 都意味着它将在下一个周期被回收、即 garbage；给 `lua_Alloc` 挂 trace hook，用 `lua_getstack` 抓 Lua 调用栈，用 `HashMap<uint64, TraceEntry>` 按 `murmur64(stack_frames)` 聚合：

```cpp
struct TraceEntry {
    String trace;
    unsigned alloc_count;
    unsigned alloc_bytes;
};
HashMap<uint64, TraceEntry> _traces;
if (_tracing_allocs) {
    lua_Debug stack[5] = {0};
    int count = lua_debugger::stack_dump(L, stack, 5);
    uint64 hash = murmur_hash_64(&stack[0], sizeof(lua_Debug)*count);
    TraceEntry &te = _traces[hash];
    te.alloc_count += 1;
    te.alloc_bytes += (new_size - old_size);
    if (te.trace.empty())
        lua_debugger::stack_dump_to_string(L, te.trace);
}
```

按 `alloc_count` 降序排，前几个就是 gameplay 组该收拾的热点。作者经验："花几个小时处理几个最大的 hot spot，GC 时间通常能降一个数量级。"

## 适用范围

以上都假设是**标准 Lua 5.1/5.2 的增量 GC**。LuaJIT 走自己的分代/增量方案并已有替换计划，本文策略需要对应移植，但"稳态时抓 alloc 热点"这个方法仍然是通用且廉价的第一招。

## 相关

- [[lua-incremental-gc]] —— 三色标记 + 双白乒乓；本文是在这个机制之上做**预算调度与热点定位**
- [[lua-light-userdata-bindings]] —— 减少垃圾的第一步是绑定层面就不造垃圾
- [[lua-cpp-binding]] —— 对照：教学级绑定默认就在制造垃圾
- [[non-cryptographic-hash]] —— murmur64 做 stack trace 聚合键
- [[game-monitoring-event-buffer]] —— 把 `memory(t)` / `gc_time(t)` 送到 monitoring 系统实时画曲线

## Sources

- [[sources/bitsquid-fixing-memory-issues-lua]]
