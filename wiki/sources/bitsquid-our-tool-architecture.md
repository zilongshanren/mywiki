---
tags: [source, bitsquid, 工具链, 引擎架构, ipc]
date: 2026-04-19
sources: 1
---

# Our Tool Architecture（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 4 月公开 Bitsquid 的工具 / 引擎分离架构。

## 摘要

两个看似矛盾的目标："工具必须用真引擎做可视化" × "工具不得强耦合引擎"。Bitsquid 的解法是把两者拆成**两个进程、只通过网络消息通信**。所有协议都是 JSON struct：工具传脚本命令、断点、reload 请求，引擎回 log / profiler 数据。可视化靠**子窗口嵌入**——工具造一个父窗口把 HWND 发给引擎，引擎在里面创建子窗口做 swap chain。每个工具启动引擎时带一个 slave Lua 脚本（比如 `particle_editor_slave.lua`），slave 脚本负责在引擎侧搭场景、解释工具发来的命令。数据分层：工具只碰 **generic JSON data**，引擎内部用 **platform-specific runtime data**；data compiler 其实就是引擎本身加 `-compile` flag 启动（天然同步）；改完数据后工具发消息让引擎 reload，改动瞬间可见。bundle 模式把数据 gzip 成单文件用于 release；长构建（nav mesh / lightmap）用 manual rebuild + 同一格式而非"低精度模式"。

## 关键要点

- **JSON over socket** 作为全局协议，**Lua debugger / profiler / script / reload** 全走一条通道；
- **父窗口 handle → 子窗口 swap chain** 做可视化嵌入；未来预想 VNC 风格给主机连编辑器；
- **slave Lua 脚本**是每个工具在引擎侧的薄胶水（粒子编辑器 slave 只有 120 行）；
- **generic（JSON）vs runtime**（二进制）分层，工具永远只看 generic；
- data compiler = 引擎 + `-compile`，保证永远同步；
- 手动 `#if defined(WIN32) && defined(DEVELOPMENT)` 框住 compile 路径，防止 release / console 构建读到未编译 generic 数据；
- **反对**为长构建引入"低精度 / 高精度"两种模式——美术看到的必须等于最终游戏。

## 链接到的概念

- [[decoupled-tool-engine-json-rpc]]
- [[tools-first-iteration-loop]]
- [[runtime-editor-console-connection]]
- [[offset-based-resource-blobs]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/04/our-tool-architecture.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-04-23_our-tool-architecture.md`
