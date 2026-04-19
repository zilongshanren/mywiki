---
tags: [lua, 动态链接, c-api, 嵌入, 引擎架构]
date: 2026-04-19
sources: 1
---

# Lua C API 代理：宿主静态链接 + 外部扩展动态加载

把 Lua 静态链进宿主（游戏引擎 / 工具）且**不导出 C API 符号**时，如何让第三方预编译 Lua C 扩展仍然能 `require` 加载？[[cloudwu|云风]] 先后给出两代方案，解决的是同一个本质问题：**进程里只能存在一份 Lua 实现**，所有外部 C 扩展必须通过某种代理层和宿主的那份 Lua 握手。

## 问题根源

Lua C 扩展标准做法是动态链接 Lua 实现。如果宿主也动态导出 Lua C API 让扩展直接链过来，没问题。但如果宿主**静态链接 Lua**（单 exe 分发、iOS 不允许动态库、安全策略等），扩展无法正确找到符号：Windows DLL 因为不允许未完成符号直接加载失败；即便在 Linux 上加载器兜底起来，**扩展自己再静态链一份 liblua.a** 就会让进程出现两份 Lua 实现。后果是 Lua 内部用来表示 nil 的"空对象"会出现两份，两个实现交换数据时引用比较错误，bug 藏得极深。官方后来加的 `luaL_checkversion()` 就是用来检测这种误用的，Lua 5.4 把空对象移入 `lua_State` 让误链接也能运行——但[[cloudwu|云风]] 坚持"一个进程只应有一份 Lua 实现"。

## 一代方案：运行期代理 DLL（Ant Engine）

[[ant-engine|Ant Engine]] 早年的做法：单独发布一个**假代理 DLL**，只包含 Lua C API 的所有符号，每个实现都是把调用转发到 engine 内部链接的真 Lua。第三方扩展正常动态链接这个代理 DLL 就能跑。不用外挂时代理 DLL 可以不发布。

缺点：代理 DLL 里每个 Lua C API 都要写一份转发存根。

## 二代方案：构建期代理（soluna extlua）

[[soluna-2d-engine|soluna]] 的新做法把代理前置到**扩展自己的构建期**：

1. 扩展额外链接 soluna 项目里的单文件 `extlua/extlua.c`，它声明了所有 Lua C API 的本地（代理）实现；
2. 扩展导出一个非标准入口 `extlua_init(L)`，第一行先调 `luaapi_init(L)`，然后像平常一样 `luaL_newlib` 注册原本的模块入口（如 `luaopen_foobar`）。

`luaapi_init` 的全部魔法只依赖一个官方宏：

```c
#define lua_getextraspace(L) ((void *)((char *)(L) - LUA_EXTRASPACE))
```

每个 `lua_State` 结构前都预留了一个指针大小的空间。soluna 的加载器做两阶段加载：

- 先构建一个**临时空 Lua 虚拟机**，把宿主进程里全部 Lua C API 指针表塞进这个空 VM 的 extraspace；
- 用 `package.loadlib` 把扩展的 `extlua_init` 当作标准 `lua_CFunction` 读出；
- 传入临时 VM 调用 `extlua_init` → `luaapi_init` 从 extraspace 读出 API 指针表填入扩展的代理符号表 → `luaL_newlib` 把真正的模块入口挂上（仍在临时 VM 里）；
- 宿主再把临时 VM 里的入口函数表复制到目标 VM，销毁临时 VM。

这样扩展在 `luaopen_foobar` 被真正调用时，所有 Lua C API 符号都已经指向宿主的真实实现。

## 兼顾 iOS 静态链接

iOS 不允许动态库，必须静态链接。同一套代码只需：

- 静态链接扩展模块
- **不**链接 `extlua/extlua.c`
- 把 `luaapi_init` 定义成空函数
- 把扩展的 `extlua_init` 入口导入主程序
- 手动 `soluna.extlua.load(extlua_init)`

构建期代理比运行期代理 DLL 更轻：少一个 binary 依赖，跨平台一致。代价是扩展的构建脚本要加两行（链 `extlua.c` + 额外导出入口）。

## 相关

- [[lua-design-philosophy]]
- [[ant-engine]]
- [[soluna-2d-engine]]
- [[cloudwu]]

## Sources

- [[sources/cloudwu-soluna-extlua-proxy]]
