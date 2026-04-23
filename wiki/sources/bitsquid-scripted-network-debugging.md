---
tags: [source, bitsquid, networking, debugging, tooling]
date: 2026-04-19
sources: 1
---

# Scripted Network Debugging（Niklas Frykholm / Bitsquid, 2013-09-25）

[[niklas-frykholm]] 2013 年 9 月的博客，记录 Bitsquid 如何用 Ruby 脚本 + 引擎内置控制台把"多机联机 bug 复现"折叠成一条命令。

## 摘要

网络 bug 复现昂贵——异步、乱序、丢包、第三方黑盒、多机同步数据+人手。作者先列出基础设施四件套：(1) 超时集中禁用开关（调试器停机时别被对端踢掉）、(2) Visual Studio 一次附加多进程同步看消息流、(3) 允许同机多实例（不同端口）、(4) 全量网络流量录制 + replay 回网络层做事后复盘。真正提升杠杆的是**把会话脚本化**：一个 Ruby 脚本完成分发可执行（靠 BitTorrent Sync 把 toolchain 自动镜像到测试机）、分发数据（引擎自带 file server 模式，节点 `-host <ip>` 从开发机拉）、起进程（本地 `system()`、远端 `PsExec`，抽成 `Node.exec` 接口）、搭多人房间（每个 dev build 默认起 TCP 控制台服务端口，Ruby 用 `Console.send_script(lua)` 发 Lua 字符串，利用 `force_menu_choice` 从菜单一步步驱动：Create Lobby / Find Lobby / Start Game）、以及游戏内脚本化玩法（spawn box、set velocity、GameSession.create_game_object）。作者用它在桌上 3 台机上跑 500 次迭代，几小时复现出手动无法稳定触发的 bug。

## 关键要点

- 网络调试基础设施：超时禁用、多进程附加、同机多实例、traffic 录制+replay
- 每个 dev build 自动暴露 TCP 脚本控制台（发 Lua 字符串驱动）
- 引擎 file server 模式省掉了数据分发环节
- 用 `force_menu_choice` 从 Ruby 脚本一步步驱动菜单到联机场景
- `Node` 抽象让"本地 / PsExec / 主机"共用同一个启动接口
- 价值不在工具，而在**能把一次复现跑 500 遍**

## 链接到的概念

- [[scripted-network-debugging]]

## 原文

- 链接：https://bitsquid.blogspot.com/2013/09/scripted-network-debugging.html
- 本地：`raw/articles/bitsquid.blogspot.com/2013-09-25_scripted-network-debugging.md`
