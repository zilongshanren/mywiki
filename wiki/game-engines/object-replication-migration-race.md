---
tags: [网络, 对象复制, peer-to-peer, 游戏引擎, bitsquid]
date: 2026-04-19
sources: 1
---

# 对象复制的迁移竞态与 migration counter 方案

[[niklas-frykholm|Niklas Frykholm]] 2013 年在 Bitsquid 网络栈里修的一个真实竞态——描述了**对象所有权跨 peer 迁移（migration）时，多源异步消息序到达带来的 paradox**，以及他最终选择的最简单修复：**migration counter**。

## 起点：Bitsquid 网络模型

栈自底向上三层：

1. **packet delivery**（UDP 之上）：提供 ACK、不可靠流、以及两个 endpoint 之间的**有序可靠流**。
2. **RPC + object replication**：应用层既能发 Lua RPC，也能用对象复制广播状态。推荐做法是"能用 replication 就不要 RPC"——后者带宽更高、更易错。
3. **客户-服务器 / P2P 两种拓扑**：差别只在消息是否经服务器中转。

对象复制的消息流是：

```
A: CREATE [wait for ack] UPDATE_1 ... UPDATE_n DESTROY
```

`CREATE` 和 `DESTROY` 走可靠流；`UPDATE` 走不可靠流（以保带宽/延迟）。不可靠 update 早到或晚到都无所谓——乱序的 update 直接忽略。

## 问题：Migration 把三方卷进来

"迁移"即改变对象的**所有者 peer**（玩家掉线、负载均衡、picking-up-a-rock 需要就近权威）。做法是由一个特殊的 `HOST` peer 发**可靠** `MIGRATE` 消息，让所有人知道新 owner。整体消息流：

```
A:    C Ua Ua Ua Ua Ua
HOST: M_ab
B:    Ub Ub Ub Ub Ub Ub Ub Ub D
```

这里埋着 bug：**两对 endpoint 之间是有序流，但不同 endpoint 之间没有任何全局序**。考虑旁观者 `X`，如果 `A → X` 流延迟，`HOST → X` 和 `B → X` 按时到，`X` 看到的可能是：

```
M_ab  Ub Ub Ub D  C Ua Ua Ua
```

——即"还没创建的对象先被迁移、再被删除，然后才收到 CREATE"。对象进了错乱态。

## 四种解法的取舍

Niklas 把能想到的方案全列了一遍，然后拒绝了三条：

1. **全局消息序**：如果 `HOST` 在收到 `C` 之后才发 `M_ab`，就保证别人也按这顺序收。听起来对，但实现上灾难——要是 `A` 在发 `C` 给 `X` 之前死了，这条未送达就要**同时阻塞** `HOST → X` 和 `B → X`。
2. **迁移握手**：让所有 peer 都 ACK 了 `M_ab` 再让 `B` 接管。多一趟 RTT，而且对象在中间"悬空"。
3. **改 ACK 粒度**：让 `X` 在收到 `C` 之前不 ACK `M_ab`，强制 `HOST` 重发。当前 Bitsquid ACK 的是 UDP 包而非 message，改粒度影响巨大。
4. **内部排队修复**：收到"未来消息"先藏起来，等合法再 replay。"长期埋雷的经典反模式"——作者直接标记为 truly horrible。

共同缺点：**全都让网络代码变复杂**。Niklas 反复念叨一句话："Reasoning about network code is hard enough as it is"——网络代码的复杂度必须被**极度节制**。

## 他选的方案：去掉 HOST 做消息源 + 版本号

**第一步：简化。让新 owner 自己宣布迁移**，`HOST` 只做"决定权"的仲裁——内部告诉 `B` "你现在是新 owner 了"，然后由 `B` 对外广播 `M_ab`。三方博弈降成两方。

```
A: C     [wait] Ua Ua Ua Ua Ua
B: M_ab  [wait] Ub Ub Ub Ub Ub Ub Ub Ub D
```

`B` 在发 `M_ab` 之后同样 **wait-for-ack** 再开始发 update——和最初 `CREATE` 的做法对称。

**第二步：migration counter**。`X` 仍可能看到 `M_ab C` 或 `M_ab D C` 这样的顺序。解决这个问题只需两条规则：

- 如果收到 `MIGRATE` 指向一个不存在的对象 → **`MIGRATE` 自动起到 `CREATE` 作用**。
- 如果之后才收到"旧的" `CREATE` → 忽略。

要判断"旧"，给对象加一个 **migration counter**：创建时 `0`，`HOST` 每次触发迁移就 `+1`，所有 `CREATE / MIGRATE / DESTROY` 消息带上当前 counter。举例：

```
A: C_0   [wait] Ua Ua Ua Ua Ua
B: M_ab_1 [wait] Ub Ub Ub Ub Ub Ub Ub Ub D_1
```

`X` 可能看到任何顺序：

- `C_0 M_ab_1 D_1` — 正常
- `M_ab_1 C_0 D_1` — M 起 create 作用，`C_0` 旧被忽略
- `M_ab_1 D_1 C_0` — 同上，对象已经被删，`C_0` 旧被忽略

**多次连环迁移**（A→B→C）也正确：

```
A: C_0   [wait] Ua Ua
B: M_ab_1 [wait] Ub Ub Ub
C: M_bc_2 [wait] Uc Uc Uc D_2
```

所有可能的乱序下都能收敛到正确态。

## 工程教训

- **简化比正确更重要**——"消除一方参与者" 是真正把问题压下来的手段，版本号只是在精简的拓扑上加 4 字节。
- 版本号是分布式系统里最"万金油"的抗乱序工具（同类手法见 [[dots-chunk-change-version]]、[[snapshot-diff-persistence]]）；在此场景里它充当"migration 的 Lamport clock"。
- **reliable 流不等于因果序**：Bitsquid 的 reliable stream 只保证**同一对端点之间**的 FIFO，跨 endpoint 的因果序要另外维护。这是大多数 UDP 游戏网络的共识，新手常误以为"可靠 = 全局有序"。

## 相关

- [[flow-graph-data-oriented-runtime]] — Bitsquid 引擎的另一侧；和这篇一样来自 Niklas 的 2013 年系列。
- [[agent-state-sync-broadcast]] — 另一个"状态广播"的设计对照。
- [[message-queue-thread-ownership]] — 消息模型的所有权命题，在单机场景里的平行。

## Sources

- [[sources/bitsquid-object-replication-migration-race]]
