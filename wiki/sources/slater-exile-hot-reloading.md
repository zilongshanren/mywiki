---
tags: [source, 游戏开发, 工具链, 引擎, C++]
date: 2026-04-14
sources: 1
---

# Exile: Hot Reloading（Max Slater）

[[max-slater|Max Slater]] 2018 年 7 月发表的 Exile 引擎工程笔记之一，介绍如何在 **C++ 主程序里热重载游戏逻辑 DLL**——不引入脚本语言的前提下复刻「改一行代码就能即时生效」的开发体验。

## 摘要

文章以一个最小可工作的 Win32 例子开篇：游戏逻辑导出 `start_up` / `main_loop` / `shut_down` 三个 C ABI 函数，主程序 `LoadLibrary` 进来后维护一个 mtime 监视器，发现 DLL 重新构建就 `FreeLibrary` 再 load 一次。剩下的章节分别处理 unload 时会被抹掉的所有东西：**memory**（库内 globals/heap 全部失效，必须把分配器或预分配区从主程序透传给库）、**threads**（库创建的线程在 unload 后栈消失，需 `begin_reload`/`end_reload` 暂停所有 worker）、**function pointers**（重编后地址会变，必须按 name 重新解析；C++ vtable 因此完全不能跨 reload 存活）、**string literals**（住在 `.rodata`，地址同样不稳）、**struct layouts**（最难解，需要序列化整个 state——Slater 在 Exile 里有反射框架但还未启用）。结尾对比了 Live++ 那种 live patching 方案：能解决所有问题但实现复杂度远超 DLL swap。

## 关键要点

- **无脚本语言的热重载** 仅用 `LoadLibrary` + 三入口约定即可实现，几十行代码起步。
- **DLL boundary 自然就是 platform / game 的分层**——这恰好与 Casey Muratori 的 Handmade Hero 路线相同。
- **状态归属问题** 比换 DLL 难得多：memory / threads / function pointers / string literals / struct layouts 五道坎一道道踩。
- **C++ vtable 跨 reload 必死**——任何持有虚函数对象的设计都得改成函数指针表 + name 解析。
- **struct layout 漂移** 是热重载的玻璃天花板：理论解法是 [[cpp-runtime-reflection|反射序列化]]，工程上多数项目接受「reload 主要用来调参」的妥协。
- **Live++ 走的是另一条路**：直接在地址空间里 patch 机器码，能解所有问题但难写。
- 与 [[engine-layering]] 的精神契合：DLL 作为 platform layer / game layer 的物理边界，强制单向依赖。

## 链接到的概念

- [[binary-hot-reload]]
- [[cpp-runtime-reflection]]
- [[linear-allocator]]
- [[engine-layering]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Hot-Reloading-in-Exile/
- 本地：`raw/articles/thenumb.at/2018-07-25_exile-hot-reloading.md`
