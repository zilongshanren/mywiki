---
tags: [source, zig, abi, dll, 热重载, c]
date: 2026-04-19
sources: 1
---

# Zig, hot reload, and ABI trouble（Sebastian Schöner）

[[sebastian-schoener]] 2026 年 4 月的长文，讲他把一个依赖 DLL 热重载的 C 风格引擎骨架搬到 Zig 时撞上的 ABI 墙。

## 摘要

作者的引擎把几乎所有代码都做成可热重载的 DLL——外层 shell 负责加载主 DLL 及其依赖，reload 时 patch 其它 DLL 的 import table。**DLL 逼出两件事：一个 ABI，以及「代码和数据住在哪」的决策**。Zig 在这两件事上都别扭。Zig 没定义自己语言特性（slice、tagged union、error union）的跨 DLL ABI，导出函数时签名只能用 C 类型；Zig 的 `!T` 错误返回依赖隐式线穿的 `error return trace`，跨 DLL 必然断；`@import` 等于把别的文件并入当前编译单元，默认产出单体，想切 DLL 又得退回 C ABI「重新发明头文件」。他的绕法是三文件结构：`impl.zig`（真实实现 + export_surface 标注）、`thunks.zig`（生成的 C ABI 薄壁）、`string.zig`（半手写半生成的「头文件」），其中转发函数用 `comptime link_options.is_dy` 切换动态/静态调用路径——一份 API 同时覆盖 DLL 与单体构建两种形态。这不是「稳定 ABI」（需要再生成每个函数专用的 `extern struct`），只是「同编译器同选项下的一致 ABI」。作者的大结论是：**替代甚至仅仅改良 C 都很难**，DLL 作为代码容器（例如热重载）的用途让没有 ABI 故事的语言显得吃力。

## 关键要点

- DLL 两件事：ABI + 数据/代码定位
- Zig slice 报错：`slices have no guaranteed in-memory representation` → 只能走 `?*anyopaque`
- Error return trace 跨 DLL 断
- `@import` 默认单体，要分编译单元必须手造 C ABI 壁垒
- 降级规则：值取地址 / 已是指针转不透明指针 / 返回值变 out 参数 / 标量按值 / 拒绝 error union
- `string.zig` = 手写类型 + 生成 forwarders + `comptime` 分支（动态 / 静态）
- Zig stdlib 带 allocator 用函数指针，配合 DLL 热重载有潜在隐患
- 作者尚未决定 Zig 是否值得替代 C，会继续压榨

## 链接到的概念

- [[zig-c-abi-boundary]]
- [[binary-hot-reload]]
- [[header-file-vs-pub-export]]

## 原文

- 链接：https://blog.s-schoener.com/2026-04-16-zig-abi/
- 本地：`raw/articles/blog.s-schoener.com/2026-04-16_zig-hot-reload-and-abi-trouble-sebastian-schoner.md`
