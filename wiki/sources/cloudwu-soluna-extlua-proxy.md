---
tags: [source, lua, 动态链接, soluna, c-api, cloudwu, 中文博客]
date: 2026-04-19
sources: 1
---

# soluna 外挂 C 模块（云风 / blog.codingnow.com）

[[cloudwu|云风]] 发表于 2026 年 3 月 11 日的工程笔记，解决 [[soluna-2d-engine|soluna]] 这类"静态链接 Lua + 不导出 C API"的单 exe 宿主如何加载预编译 Lua C 扩展库的问题——通过一个利用 `lua_getextraspace` 的代理虚拟机 + 两阶段加载的新做法。

## 摘要

问题出在 soluna 默认把 Lua 静态链到唯一执行文件里，没导出 Lua C API 符号。标准 Lua C 扩展（`.so` / `.dll`）编译时是动态链接 Lua C API 的，放进 soluna 这种环境里，Windows DLL 因为不允许未完成符号会直接加载失败。即便能加载，**静态链接 Lua 实现有多份副本的问题——nil 指向的"空对象"会出现多个，引用比较会错误**。Lua 自己后来加了 `luaL_checkversion()` 来识别这种坑，5.4 又把空对象移入 `lua_State` 结构让误链接的项目也能勉强工作，但云风坚持"一个进程只应该有一份 Lua 实现"。

Ant Engine 当年的做法是发布一个**假代理 DLL**：只包含 Lua C API 符号，所有调用转发到 engine 内部的 Lua 实现。外部库正确动态链接这个代理 DLL 即可。新 soluna 方案把代理层从运行期 DLL 前置到**构建期**：外部库只需额外链接 soluna 项目里的 `extlua/extlua.c` 单文件，并导出一个非标准入口函数 `extlua_init(L)`，里面先调 `luaapi_init(L)` 再 `luaL_newlib` 注入原本的模块入口。`luaapi_init` 的全部魔法只依赖一个官方宏 `lua_getextraspace(L)`——每个 `lua_State` 前预留一个指针空间，soluna 的加载器先构建一个空的临时 Lua 虚拟机，把宿主进程里的所有 Lua C API 指针表塞进这个空虚拟机的 extraspace；`extlua_init` 被 `package.loadlib` 读出当作标准 `lua_CFunction` 调用，传入这个带 API 表的空虚拟机，`luaapi_init` 就能从 extraspace 把 API 导入外部库的代理符号；然后 `luaL_newlib` 把真正的模块入口函数表挂上。soluna 再从空虚拟机把入口函数表复制到目标虚拟机、销毁临时 VM，加载完成。

这个方案还兼容 iOS 这种不允许动态库的场景：静态链接模块时把 `luaapi_init` 定义为空函数、不链接 `extlua.c`、直接把 `extlua_init` 导入主程序、调用 `soluna.extlua.load(entry)` 加载——同一套代码同时支持动态和静态链接。

## 关键要点

- 进程中多份 Lua 实现导致"多个空对象"，引用比较错误是经典坑
- Windows DLL 未完成符号限制让标准 Lua C 扩展无法直接挂到静态链接 Lua 的宿主上
- Ant Engine 方案：运行期代理 DLL，外部库动态链接代理，调用转发到宿主
- soluna 新方案：构建期代理（一个 `extlua.c` 单文件），外部库的 `extlua_init` 入口函数不依赖真 Lua 实现
- 魔法全在 `lua_getextraspace` 这个官方宏上——用临时空 VM 的 extraspace 传递 C API 指针表
- 两阶段加载：`package.loadlib` 读入口 → 传空 VM 注入 API → `luaL_newlib` 挂真正入口 → 复制到目标 VM
- 同一套构建方式可同时兼容 iOS 静态链接（`luaapi_init` 空实现、直接导入入口）

## 链接到的概念

- [[lua-c-api-dylib-proxy]]
- [[lua-design-philosophy]]
- [[soluna-2d-engine]]
- [[ant-engine]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2026/03/soluna_external_lib.html
- 本地：`raw/articles/blog.codingnow.com/2026-03-11_yun-feng-de-blog-2.md`
