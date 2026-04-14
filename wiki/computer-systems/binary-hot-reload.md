---
tags: [游戏开发, 工具链, 动态链接, C++, 引擎]
date: 2026-04-14
sources: 1
---

# C++ 二进制热重载

游戏程序员爱上脚本语言（Lua / C#）的最大动机之一，是「改一行代码、不重启游戏就能看到效果」。但其实 **不引入第二门语言** 也能拿到这个收益——把游戏逻辑编译成动态库（DLL / .so），主程序在运行时用 `LoadLibrary` / `dlopen` 加载它，监控文件时间戳，一旦发现重写过就 `FreeLibrary` + `LoadLibrary` 一遍。任何能导出 C ABI 的语言都能套这个框架。Max Slater 在体素引擎 [Exile](https://github.com/TheNumbat/exile) 里实现过这套系统，但「能换 DLL」只是问题的开始——真正棘手的是 **状态在两次加载之间如何幸存**。

## 三函数 API

约定动态库导出三个入口：

```cpp
__declspec(dllexport) void* start_up(platform_api* api);
__declspec(dllexport) bool main_loop(engine* state);
__declspec(dllexport) void shut_down(engine* state);
```

主程序的循环简化为：load → start_up → 每帧 main_loop + 检查文件 mtime → 改变就 free + reload → 退出 shut_down。这套结构下，**整个引擎可以被瞬间替换**——只要还能找回上次的 `state` 指针。

## 五个坑

实际工程里要单独处理五个会被 unload 抹掉的 things：

**Memory.** 库 unload 时它的整个虚拟地址空间会消失，包括 globals、statics、以及 malloc 出来的堆。两条路：（1）主程序预分配一大块 VM，传给库，库自己用 [[linear-allocator|linear allocator]] 切片；（2）把主程序的 malloc/free 函数指针放进 platform_api 透传给库。Slater 选了 (2)，但他承认 (1) 更灵活也更快——能上分级分配器、profile hooks，且不用每次 alloc 都过函数指针。

**Threads.** 库创建的线程不会随 unload 终止，但它们的栈和 TLS 都属于库的地址空间——不杀就崩溃。需要 `begin_reload` / `end_reload` 这对回调，库里要在重载前停掉所有 worker、重载后重启。代价是当前 atomic 任务必须跑完，重载存在 stall。

**函数指针.** 持久化函数指针非常危险——重载后函数的相对地址会变。两个折中：（1）干脆不存函数指针，每帧拿一次；（2）只存 `(void*, name)` 对，重载时按 name `GetProcAddress` 重新解析。Slater 选了 (2)，因为 Modding API 需要这种灵活性。代价：**C++ 虚函数无法跨重载存活**——vtable 是函数指针表。

**字符串字面量.** 它们住在 `.rodata`，地址同样会变。规避方法是不存指针——要么每帧重新构造，要么 heap copy。

**Struct 布局.** 最难治的：旧数据在内存里、新代码 expects 不同的字段顺序或 size。Slater 没解决这个，承认热重载主要用于「调参」而不是「动数据结构」。理论解法是 unload 时 [[cpp-runtime-reflection|反射序列化]] 整个 state，load 后再反序列化——他在 Exile 里实现了反射框架，但还没用到这一步。

## 与 Live++ 的区别

完整版的 [Live++](https://molecular-matters.com/products_livepp.html) 走的是另一条路：**live patching**，直接在进程里改机器码、不重新加载整个库。它能解决 vtable 与 struct layout 问题，但实现难度远高于 DLL swap。对于「我自己的引擎要不要做？」，Slater 的答案是：DLL 方案两天能写出来，能解决 80% 的迭代速度问题，剩下 20% 学会绕开。

## 相关

- [[cpp-runtime-reflection]] — Slater 在 Exile 里实现的反射框架，是热重载升级版的前置条件
- [[linear-allocator]] — 把堆从主程序分给库的实现选择
- [[engine-layering]] — DLL boundary 自然就是 platform layer / game layer 的分界
- [[max-slater]]

## Sources

- [[sources/slater-exile-hot-reloading]]
