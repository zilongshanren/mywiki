---
tags: [网络, 游戏服务器, 网关, IO-多路复用]
date: 2026-04-14
sources: 1
---

# 连接汇聚网关（N 对 1 gateway）

连接汇聚网关是游戏服务器常见的前置进程：它监听外部端口、承载大量 TCP 长连接，把 N 条 socket 上的数据流合并成一条内部管道递给后端主服务；反之后端的数据再按连接 id 拆分发回。对后端而言只需要处理一条流（常是另一个 socket 或 stdin/stdout），无需再面对[[latency-vs-throughput|海量连接的调度]]、心跳、慢客户端等等琐事——这把"如何承接 10 K 连接"和"业务逻辑"彻底解耦了。

[[cloudwu]] 在 2006 年的 epoll/kqueue/iocp 总结后，多次用这个网关模式来写服务器前端：处理上限 64 K 连接，用 2 字节 id 号区分，协议最简——每个片段仅 3 字节头（1 字节长度 + 2 字节 id），后面跟 payload。内部管道上看到的数据流就是 `len id_lo id_hi content ...` 的重复。网关只负责流合并，不规定应用层分包；后端通过 0 号特殊连接收发控制指令（文本协议，`\r\n` 分隔），可以强制断开某个外部连接、接收新连接/断连事件、控制监听端口开关与连接上限。

把这套模式在 [[go-goroutine-channels|Go]] 里重写只花了大约 240 行：每条 socket 一个 goroutine 用阻塞 IO 处理；主循环用 `select` 多路复用 channel；控制流用 in-memory pipe 接 `bufio.Reader` 把字节流切成文本行。唯一的性能点是为每个对外包加三字节头时批量从 16 K 预分配数组借 slice，避免 per-packet `make`。这个架构也能无缝对接 [[zeromq-messaging-patterns|ZeroMQ]]：客户端一侧仍用网关吃 TCP，网关以内的服务集群全部走 ZeroMQ 的 request/reply、pub/sub、pipeline 三种模式组合。

## 相关

- [[cloudwu]]
- [[go-goroutine-channels]]
- [[zeromq-messaging-patterns]]

## Sources

- [[sources/cloudwu-go-first-impressions]]
