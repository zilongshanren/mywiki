---
tags: [source, skynet, lua, 虚拟机, cloudwu, 中文博客]
date: 2026-04-19
sources: 1
---

# Skynet 升级到 Lua 5.5.0（云风 / blog.codingnow.com）

[[cloudwu|云风]] 发表于 2025 年 12 月 23 日的 skynet 版本升级说明，记录把 skynet 内置 Lua 升级到刚发布的 5.5.0 的过程、取舍与展望。

## 摘要

skynet 长期维护一份**修改版 Lua**，允许多个虚拟机共享函数原型以减少服务启动时间和内存占用。最困难的是"外部导入字符串"如何与 VM 内部 intern 池共存——云风 2019 年有篇专文讨论字符串比较算法即为此。副产品是打过 patch 的 VM 还可用 `skynet.sharetable` 跨 VM 共享只读常量表。

Lua 5.5 引入 **external strings** 特性大幅加速字节码加载，云风倾向于**新项目避免再依赖共享常量表 patch**，让未来能摆脱私有 patch 减少维护成本。5.5 兼容 5.4，绝大多数 skynet 项目无需改动，但必须用 `make cleanall` 而非 `make clean`——Lua 的编译中间文件不在后者清理范围。

云风推荐关注的 5.5 新特性：`global` 关键字（减少拼写错误 bug）、分代 GC 步进化（老版本对大内存服务停顿严重）、`...args` 变长参数新语法（可简化 skynet 自身 Lua 代码）。

## 关键要点

- skynet 维护私有 Lua patch 用于跨 VM 共享函数原型，解决字符串 interning 兼容问题
- Lua 5.5 external strings 已原生加速字节码加载，未来可逐步去除 patch 依赖
- 新项目不推荐再依赖 `skynet.sharetable`
- 5.5 升级兼容 5.4，但必须 `make cleanall` 才能重编 Lua
- `global` 关键字 / 分代 GC 步进化 / `...args` 是值得升级的三个特性

## 链接到的概念

- [[skynet-lua-sharetable-patch]]
- [[cloudwu]]
- [[lua-design-philosophy]]
- [[lua-incremental-gc]]
- [[ltask-scheduler]]

## 原文

- 链接：https://blog.codingnow.com/2025/12/skynet_lua_550.html
- 本地：`raw/articles/blog.codingnow.com/2025-12-23_yun-feng-de-blog-2.md`
