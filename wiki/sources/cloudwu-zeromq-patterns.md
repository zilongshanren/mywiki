---
tags: [source, 消息队列, ZeroMQ, 分布式系统, 游戏服务器]
date: 2026-04-14
sources: 1
---

# ZeroMQ 的模式（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2011 年 2 月的读书笔记，读完 ZeroMQ Guide 后对其通讯模式做的高层总结，并给网络游戏服务器架构给出了推荐用法。

## 摘要

他把 ZeroMQ 的核心价值概括为：不是"又一个 socket 封装"，而是比 TCP 高一级的协议——它放弃"通讯基于一对一连接"的假设，改为按 **模式** 定义端点。API 因此大幅简化，`bind / listen / accept` 被抹平，不必在意谁先启动。ZeroMQ 把通讯需求归为四类（第一类一对一结对只是为了兼容传统 socket，不推荐），常用的只有三种：**请求/回应**（两端都可 1:N，可通过 Device 扩展为 N:M，端点地址上层透明）、**发布/订阅**（发布端单向广播、不保证订阅端在线，若需反馈另起 request/reply socket）、**管道 Push/Pull**（从 PUSH 单向推到 PULL）。任何分布式并行需求都可以用这三种组合出来。他还提到 Transient / Durable socket 的区分不是"是否保持 TCP 连接"而是概念层面的生命期，必要时甚至允许把 buffer 落到磁盘。对网络游戏，他推荐的架构是：玩家 client-server 部分仍然用几年前那篇 blog 写的连接服务器（定制网关）承载，网关之内的服务集群用 ZeroMQ 协议通讯。

## 关键要点

- ZeroMQ 不是 socket 封装，而是更高层级的通讯模型
- 四类模式中只有三类常用：req/rep、pub/sub、push/pull
- req/rep 的收发一定成对出现；两端可以 1:N，Device 扩展为 N:M
- pub/sub：订阅前发出的数据直接丢弃，连接后保证不丢；反馈需另一条 socket
- push/pull：单向 fan-out 工作分发
- Transient / Durable 是生命期概念而非 TCP 实现细节
- 游戏服务器推荐：玩家侧用定制连接网关，集群内用 ZeroMQ
- 这三种模式是 Erlang / Go `select/chan` 在分布式层面的自然延伸

## 链接到的概念

- [[zeromq-messaging-patterns]]
- [[connection-multiplexer-gateway]]
- [[go-goroutine-channels]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2011/02/
- 本地：`raw/articles/blog.codingnow.com/2011-02-25_yun-feng-de-blog.md`
