---
tags: [source, bitsquid, 网络, 对象复制, p2p]
date: 2026-04-19
sources: 1
---

# A Bug in Object Replication and Message Reordering（Bitsquid, 2013-03）

[[niklas-frykholm|Niklas Frykholm]] 2013 年 3 月一篇 post-mortem 式的网络 bug 分析：对象在 peer 之间迁移所有权时，多源异步消息的到达乱序产生的 paradox，以及最后选用的简化方案。

## 摘要

Bitsquid 网络栈分三层：UDP 上自建 packet delivery（ACK + reliable/unreliable streams），上面有 RPC 服务和对象复制，客户-服务器 / P2P 两种拓扑共享同一套代码。对象的正常生命周期是 `CREATE [ack] UPDATE* DESTROY`，其中 `CREATE/DESTROY` 走 reliable、`UPDATE` 走 unreliable，乱序到达的 `UPDATE` 直接丢弃。迁移（migration）破坏这个模型：由 `HOST` peer 发 `M_ab` 把所有权从 A 移到 B，但 `A / HOST / B` 三条独立的 reliable 流之间**没有全局序**——旁观 peer `X` 可能看到 `M_ab → Ub → D → C → Ua` 这种 paradox。作者列了四种 "看起来对"的修复（全局序 / 迁移握手 / 细粒度 ACK / 内部队列），逐一拒绝：全都让已经够难的网络代码更复杂。最后他走了两步简化：第一，让新 owner `B` 自己广播 `M_ab`，把三方减成两方；第二，给 `CREATE / MIGRATE / DESTROY` 加上 **migration counter**，用两条规则（`MIGRATE` 可起 `CREATE` 作用、过期 `CREATE` 忽略）吸收所有乱序。多级迁移同样收敛。评论区有人问为什么 `CREATE` 要 reliable、不能合进首个 UPDATE——作者答：为了**让 CREATE 和 RPC 共用同一条可靠序**，这样引用该对象的 RPC 消息到达时能保证对象存在。

## 关键要点

- Bitsquid 网络分层：UDP → ACK + reliable/unreliable packet delivery → RPC + replication → client-server / P2P。
- Replication 依赖两条假设：可靠流内 FIFO；不可靠流内乱序 update 可丢。
- Migration 引入第三方 `HOST`，跨 endpoint 无全局序 → `X` 可能看到错乱 paradox。
- 四种常规修法都让网络代码复杂化 → 作者明确拒绝。
- 简化 step 1：让新 owner `B` 广播 `MIGRATE`，`HOST` 只内部通知 B——三方→两方。
- 简化 step 2：migration counter + 两条规则（`MIGRATE` 可当 `CREATE`；旧 `CREATE` 忽略）吸收所有乱序，且支持连环迁移。
- "reliable 流" 不提供 **跨 endpoint 的因果序**——常见新手误解。
- CREATE 被单独做成 reliable 的原因：与 RPC 共用同一条可靠序，保证 RPC 引用的对象已存在。

## 链接到的概念

- [[object-replication-migration-race]]
- [[flow-graph-data-oriented-runtime]]
- [[agent-state-sync-broadcast]]
- [[dots-chunk-change-version]]
- [[message-queue-thread-ownership]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2013/03/a-bug-in-object-replication-and-message.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2013-03-01_a-bug-in-object-replication-and-message-reordering.md`
