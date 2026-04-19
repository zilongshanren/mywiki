---
tags: [lua, 垃圾回收, 增量-GC, 三色标记]
date: 2026-04-14
sources: 1
---

# Lua 的增量式 GC

Lua 5.0 及以前的 GC 是典型的 stop-the-world：一触发就必须把整个标记 + 清理跑完。对交互式脚本没问题，但游戏服务器这种实时系统即便"内存不大"也可能管理成千上万的对象，一次性停顿代价不可忽略。Lua 5.1 把 GC 改为**增量式**：仍然不是并发 GC，而是把流程切成若干小步，每步做一点，然后把控制权还给用户代码；总开销略高于一次跑完，但每次最大停顿被压得很低。[[cloudwu]] 在 2011 年读 Lua 5.1.4 源码时做了一份相当细的剖析，以下是核心设计。

## 五阶段状态机

GC 在 `global_State.gcstate` 上跑一个五态机：

- `GCSpause`：每轮的起点，`markroot` 把主线程、全局表、注册表、元表打上初始标记，立即切到 propagate。
- `GCSpropagate`：迭代阶段，只要 gray 链非空就一次 `propagatemark` 一个节点；gray 链清空后进入不可被打断的 `atomic(L)` 把 mark 阶段封顶。
- `GCSsweepstring`：string table 是单独管理的，每步清掉一条 hash 桶。
- `GCSsweep`：清理其余 GCObject，结构同上，每步一小段链表。
- `GCSfinalize`：逐个调用带 `__gc` 元方法的 userdata 的 finalizer（`GCTM`），用户数据本身的内存则要等下一轮 GC 或 `lua_close` 再释。

每一步消耗一个预算（像 `GCSWEEPCOST` 这样的"神秘数字"），用于换算 GC 进度与用户分配的比例。

## 三色标记 + 双白色乒乓

每个 GCObject 的 `marked` 字节按位编码颜色。白色有两种（`WHITE0BIT / WHITE1BIT`），灰色不用独立位——"非白非黑"即灰色。为什么需要两种白？因为增量 GC 最棘手的问题是：**标记结束后、清理尚未完成前**，新建对象怎么着色？如果直接涂黑，它在本轮结束后就再也不会被重置回白；如果直接涂白则可能被错杀。Lua 的解法是引入一个乒乓开关——当前轮清理的是 0 型白，新生对象就涂 1 型白受保护；下一轮再切换。`otherwhite()` / `luaC_white()` 两个宏就是用来拿当前白色状态的。

## 其他保护位

- `FINALIZEDBIT`（bit 3）防止同一个 userdata 的 `__gc` 元方法被反复调用。
- `KEYWEAKBIT`（bit 3）/ `VALUEWEAKBIT`（bit 4）标记 table 的 weak 属性。
- `FIXEDBIT`（bit 5）把字符串钉住不被回收，典型用法是保留字和元方法名。Lua 运行时把 `__index / __newindex / __add / ...` 这些字符串全部 `luaS_fix` 住并缓存到 `global_State.tmname[]`，以后比较元方法名时只要比指针，比 `strcmp` 或 `lua_pushlstring` 再查 string table 快得多——因为 Lua 的 GC 不做内存迁移，`FIXED` 的字符串地址永不变。
- `SFIXEDBIT`（bit 6）只给主 mainthread 用。`luaC_freeall` 在 `lua_close` 时会"把一切当白色"强制回收，但 SFIXED 的主线程结构要最后才由 `close_state` 显式 free，并在结尾 `assert(totalbytes == sizeof(LG))`——确认整个世界只剩下一个根。

## 对 Lua 哲学的注解

云风特别欣赏的一点是 Lua 把"字符串作为不可变的共享对象、比较退化为指针比较"这件事贯彻到 GC 设计里：`FIXEDBIT` 不仅是防回收，还反过来变成运行时的性能武器。这和 Lua 的整体[[lua-design-philosophy|小而能组合]]风格一致——一块 `marked` 字节、两种白色、几个宏，就把"增量标记 + 清理 + finalize + 永久字符串"四件事串起来了。

## 相关

- [[cloudwu]]
- [[garbage-collector]]
- [[simple-cpp-mark-sweep-gc]]
- [[lua-design-philosophy]]
- [[skynet-lua-sharetable-patch]] —— skynet 跨 VM 共享函数原型 patch 与 Lua 5.5 external strings

## Sources

- [[sources/cloudwu-lua-incremental-gc]]
