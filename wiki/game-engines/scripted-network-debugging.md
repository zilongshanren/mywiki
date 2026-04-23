---
tags: [networking, debugging, tooling, console, lua, ruby]
date: 2026-04-19
sources: 1
---

# 脚本化网络调试

网络 bug 的复现成本高到离谱：异步消息、乱序、丢包、第三方黑盒（PSN/Steam/路由器/防火墙/乱插手的杀软），加上"一次测试要搭多机、同步可执行、同步数据、拉同事一起联机跑几十轮"。[[niklas-frykholm]] 在 *Scripted Network Debugging* 里把这件事分成两层：一套**通用基础设施**，加上一个**脚本化会话驱动器**把复现跑到数百次。

基础设施四件套：(1) 超时集中禁用开关——在调试器里停住的机器不应该被对端判定为掉线，调试器在手里才能真的"停下来看"；(2) Visual Studio 可以**同时附加多个进程**，一次调试器会话跟踪 8 个节点间的消息流；(3) 允许同机多实例（不同端口）——绕开跨机奔跑的成本，Steam/主机因账号限制例外；(4) 整套网络流量可录制：一个开关把收发包写盘，配专用 GUI 解析+按原时序 **replay** 回网络层——很多事后追查靠的就是这一层。

更有价值的是第二层：**写一个 Ruby 脚本把一场多人测试从头到尾自动跑完**。作者的网络测试脚本做了五件事：分发可执行、分发项目数据、起进程、搭多人房间、跑玩法。

- **分发可执行**：靠 BitTorrent Sync 把开发机的 `toolchain/` 同步到所有测试机，重新 build 自动扩散。
- **分发数据**：不需要——Bitsquid 引擎本身支持 **file server 模式**，所有节点启动时 `-host <dev-ip> -project <p>` 从开发机拉数据。
- **起进程**：本地 `system("start ...")`；远端用 `PsExec` 抽象成 `exec.launch(arg)`，`Node` 配置里每台机器绑定自己的启动方式，新平台（PS3/X360）只需加一种 `Exec` 实现。
- **搭房间 + 玩游戏**：这是关键杠杆。所有 Bitsquid dev build 都起一个 TCP 控制台服务端口，连上就能发 Lua 脚本字符串给运行中的游戏。Ruby 脚本因此用 `Console.send_script(lua)` 往每个节点喷代码：服务端跑 `force_menu_choice = "Create Lobby"`、客户端跑 `"Find Lobby"` 和 `"Niklas Test Lobby"`、服务端 `"Start Game"`——一场 Steam lobby 就从脚本里建起来。进入游戏后再用同样通道 spawn box、设速度、做 `GameSession.create_game_object`，让复现场景完全脚本化。

作者靠这套在桌上三台机器里跑了 500 次迭代、几小时内复现了一个手工几乎不可能稳定重现的 bug。背后的真正支点是两件事：**dev 可执行默认自带脚本控制台**（[[script-tool-mode|把运行期当成可脚本化服务]]），以及**引擎本身支持 file server 模式**（不用管版本同步）。两者合在一起，一个 Ruby 脚本就能把"多机联机测试"折叠成一句 `ruby run.rb`。

## Sources

- [[sources/bitsquid-scripted-network-debugging]]
