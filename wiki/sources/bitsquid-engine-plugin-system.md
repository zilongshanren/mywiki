---
tags: [source, 游戏引擎, plugin, c-abi, bitsquid]
date: 2026-04-19
sources: 1
---

# Building an Engine Plugin System（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2014 年 4 月的文章，说清楚 Bitsquid 给引擎加 plugin 系统时碰到的两类 API 设计问题，以及最终选 **C-based versioned interface query** 路线的理由。

## 摘要

Plugin 系统真正难的不是 plugin 暴露给引擎的 `init/update/shutdown` 入口，而是**引擎暴露给 plugin 的服务 API**——plugin 要播声音、生成 unit、做渲染，这一面越扩越大，耦合问题就越棘手。Niklas 否决了"共享 DLL"（最后会把半个引擎塞进去）和"全走 Lua 桥接"（对 C++ plugin 太绕、暴露面太大）两种常见路线，选的是**interface querying**：引擎把 `get_engine_api(api_id, version)` 函数指针交给 plugin，plugin 在 `init` 里自助领取它要的模块——`WorldApi_v0`、`LuaApi_v0` 等等。要破坏性修改 API？**新开 v1，让 v0 继续躺着**，所有老 plugin 继续能跑。为对称性，plugin 侧也只 export 一个 `get_plugin_api`——plugin API 自身也能独立演进。全程用 C 接口而非 C++ 虚函数表，因为 **C++ ABI 跨编译器不稳定**，plugin 用了就是工具链锁定；plugin 作者内部想写 C++ 没问题，接口层的 C 约定保证了二进制兼容。这套"函数指针表 + 模块 ID + 版本号"与 Bitsquid 的 [[data-driven-architecture|data-oriented 风格]]同构，也为后来的 [[bitsquid-data-oriented-entity-system|ECS]] 铺了路——plugin 要给 entity 加新组件，注册新的 ComponentManager 即可。

## 关键要点

- **Plugin 架构有两套 API**：plugin→engine 和 engine→plugin，前者简单、后者才是难点
- **拒绝共享 DLL**：会把半个引擎塞进去、任何内部改动都破 plugin
- **拒绝脚本桥接**：C++ plugin 通过 Lua 调引擎太绕，暴露面也过大
- **Interface query 模式**：`get_engine_api(api_id, version)` 函数指针 + 模块 ID + 版本号
- **老 API 永远不删**：`WorldApi_v0` 和 `WorldApi_v1` 共存，老 plugin 自动兼容
- **Plugin 侧对称**：只 export `get_plugin_api`，plugin API 自身也能独立演进
- **选 C 不选 C++ vtable**：C++ ABI 跨编译器不稳定，plugin 作者工具链必须自由
- **Plugin 逼出 ECS**：要让 C++ plugin 给 entity 加新能力，component 架构是最自然的装配方式

## 链接到的概念

- [[engine-plugin-c-abi-versioned-api]]
- [[bitsquid-data-oriented-entity-system]]
- [[middleware-vs-open-source]]
- [[c-interface-oop]]
- [[c-opaque-struct-modules]]
- [[data-driven-architecture]]

## 原文

- 链接：https://bitsquid.blogspot.com/2014/04/building-engine-plugin-system.html
- 本地：`raw/articles/bitsquid.blogspot.com/2014-04-25_building-an-engine-plugin-system.md`
