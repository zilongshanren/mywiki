---
title: 从 0 到 1.5 亿 QPS：Uber 核心存储架构的十年演进与缓存设计哲学
url: https://tonybai.com/2025/09/01/uber-150-million-reads/
published: '2025-09-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 从 0 到 1.5 亿 QPS：Uber 核心存储架构的十年演进与缓存设计哲学

![](../../assets/71bc5452f727d0ad.png)


[本文永久链接](https://tonybai.com/2025/09/01/uber-150-million-reads) – https://tonybai.com/2025/09/01/uber-150-million-reads

大家好，我是Tony Bai。

在 Uber 这样体量的公司，其核心在线存储系统不仅要处理 PB 级的海量数据，还要以毫秒级的延迟响应每秒上亿次的请求。这一切是如何实现的？本文将深度整合 Uber 工程团队这几年公开发布的三篇文章，和大家一起穿越其核心存储架构的十年演进史：从最初为解决 MySQL 扩展性难题而生的 Schemaless，到拥抱 SQL 和强一致性的分布式数据库 Docstore，再到最终通过集成式缓存 CacheFront 将读取性能推向 1.5 亿 QPS 的极致。这是一个关于在 MySQL 之上构建分布式巨兽的真实故事，充满了工程上的权衡、妥协与创新。

![](https://tonybai.com/wp-content/uploads/2025/paid/system-programming-in-go-pr.png)


## Schemaless 的诞生——戴着镣铐的舞蹈

故事的起点，是 Uber 早期对 PostgreSQL 的依赖，以及随后因性能和扩展性问题向 MySQL 的迁移。然而，即便是 MySQL，在面对 Uber 业务爆炸式增长带来的写入和分片（sharding）压力时，也很快捉襟见肘。Schemaless——Uber 的第一个自研存储系统——正是在这样的背景下诞生的。

### 核心动机：解决 MySQL 的扩展性瓶颈

Schemaless 的设计目标非常明确：在 MySQL 之上构建一个水平可扩展的、对开发者透明的分片层。它并非要取代 MySQL，而是要成为 MySQL 的“放大器”。其核心设计充满了对当时工程约束的精巧妥协：

**无模式 (Schemaless)**：这并非真的没有模式，而是“读时模式”（schema-on-read）。数据以 JSON blob 的形式存储在 MySQL 的一个简单表中。这极大地简化了数据库端的管理，但也给应用层带来了数据解析和验证的负担。**仅追加 (Append-only) 与不可变性 (Immutability)**：为了简化系统设计和避免复杂的并发控制，Schemaless 的核心数据单元——Cell——被设计为不可变的。更新操作实际上是写入一个新的 Cell 版本。这使得系统非常健壮，但也让其难以用作通用数据库。**二级索引**：通过一个独立的索引系统，Schemaless 实现了对非主键字段的查询，这在当时是一个重要的创新。

Schemaless 成功地解决了 Uber 早期的规模化问题，证明了在成熟数据库之上构建抽象层的可行性。但它的“极简主义”设计，也为后来的演进埋下了伏笔。

## Docstore 的演进——从 NoSQL 回归 SQL 的怀抱

随着时间的推移，Schemaless 的局限性日益凸显。其仅追加的 API 和“读时模式”对开发者不够友好，导致许多团队转向了当时流行的 Cassandra。然而，Cassandra 的最终一致性模型给应用开发者带来了巨大的心智负担，同时其运维复杂性和资源效率也未能满足 Uber 的严苛要求。

在亲身经历了 Schemaless 和 Cassandra 的优缺点后，Uber 团队做出了一个关键决策：**将 Schemaless 演进为一个通用的、支持事务的分布式 SQL 数据库**。Docstore 就此诞生。

### 设计哲学：两全其美

Docstore 的目标是提供“两全其美”的体验：既有 NoSQL 文档模型的灵活性，又有传统关系型数据库的模式强制和强一致性。

**写时模式 (Schema-on-write)**：与 Schemaless 相反，Docstore 默认强制执行模式。表结构（列、类型）被明确定义，数据库负责保证数据的规整性。这极大地提升了数据的可靠性和开发效率。**灵活的文档模型**：Docstore 支持嵌套数据类型和“关联”（Associations），允许开发者在同一张表中模拟关系模型（一对多、多对多）和层级化的文档模型。**开发者控制的数据局部性**：通过引入**分区键 (Partition Key)**的概念，Docstore 允许开发者显式地控制哪些数据应该物理上存储在一起，这对于优化查询性能至关重要。

### 架构核心：MySQL 之上的 Raft 与强一致性

Docstore 的架构是一个精巧的分层设计，其核心是在 MySQL 之上构建了一个强一致的复制层。

![](../../assets/4f2c57ebf7a163c0.png)


**分层架构**：系统分为无状态的**查询引擎层**和有状态的**存储引擎层**。查询引擎负责路由、分片、鉴权等，而存储引擎负责数据的持久化。**分区与复制**：数据被分片（shard）后，分布在多个**分区 (Partition)**中。每个分区是一个由 3-5 个 MySQL 节点组成的复制组，跨可用区部署以实现高可用。

![](../../assets/bed4fc17a46045d9.png)


**Raft 共识协议**：每个分区内部运行**Raft 共识协议**来保证数据的一致性。所有写操作都由 Leader 节点发起，并通过 Raft 的复制日志同步到 Follower 节点。**严格可串行化 (Strict Serializability)**：得益于 Raft，Docstore 在分区级别提供了最高的一致性保证——严格可串行化。这意味着开发者可以像操作单机数据库一样思考事务，而无需担心并发异常。

![](../../assets/0e69fc7d562ccd99.png)


**事务的实现**：Docstore 巧妙地将 MySQL 的原生事务能力暴露给了上层。一个 Docstore 事务，其本质就是一个在 Leader 节点上执行的 MySQL 事务，这个事务本身（而非其结果）作为 Raft 日志的单元被复制。这既保证了 ACID 语义，又实现了高可用。

Docstore 的诞生，标志着 Uber 存储系统的一次成熟蜕变。它从一个专用的键值存储，演变成了一个功能丰富的、通用的分布式 SQL 数据库，并成功地在 Uber 内部取代了 Cassandra，成为众多核心业务的首选。

## CacheFront 的极致优化——迈向 1.5 亿 QPS

随着 Docstore 的广泛应用，新的挑战再次出现。许多业务场景呈现出典型的“读多写少”模式，读取 QPS 可能是写入的数十倍甚至上百倍。仅仅依靠 Docstore 存储引擎的 NVMe SSD 已经无法经济高效地满足对超低延迟和超高吞吐量的极致追求。

为了解决这个问题，Uber 团队没有让每个业务团队各自为战地搭建缓存，而是选择了一条更艰难但更具价值的道路：**为 Docstore 构建一个深度集成的、透明的分布式缓存层——CacheFront**。

### 核心目标：透明、高效、一致

CacheFront 的设计目标清晰而宏大：

**对用户透明**：开发者无需修改代码或引入新的客户端，只需开启配置即可享受缓存带来的好处。**极致的低延迟**：显著降低 P75、P99 甚至 P99.9 的读取延迟。**成本效益**：用相对廉价的缓存资源（Redis）来卸载昂贵的数据库存储层负载。**更强的一致性**：解决传统[旁路缓存（Cache-Aside）模式](https://tonybai.com/2025/04/28/five-cache-strategies)中常见的缓存与数据库不一致问题。

### 架构与设计：缓存即服务，深度集成

![](https://tonybai.com/wp-content/uploads/2025/uber-150-million-reads-5.png)


CacheFront 被无缝地集成在 Docstore 的**查询引擎层**。所有读取请求都会先经过缓存层，缓存未命中时再穿透到存储引擎，并将结果异步写回缓存。这个看似简单的“缓存旁路”模式，在 Uber 的规模下，充满了工程上的挑战与创新。

#### 缓存失效的“圣杯”：CDC 的妙用

缓存系统中最难的问题永远是**缓存失效 (Cache Invalidation)**。CacheFront 没有采用简单的 TTL（Time-To-Live）过期策略，因为它无法保证数据的一致性。其真正的“杀手锏”是利用了 Docstore 内建的**变更数据捕获（Change Data Capture, CDC）**服务——**Flux**。

**Flux**会持续地追踪（tail）底层 MySQL 的二进制日志（binlog）。- 当任何数据（包括条件更新）发生变更时，Flux 会捕获这些事件，并
**在亚秒级内**向 Redis 发送失效或更新指令。 - 这种基于 CDC 的异步失效机制，极大地缩短了数据不一致的时间窗口，提供了远强于 TTL 的
**最终一致性**保证。

![](../../assets/e82d53ae9a4c5519.png)


#### 追求更强的一致性：同步失效的引入

随着业务对一致性要求的提高，仅仅依赖异步的 CDC 已经不够。CacheFront 的第二次重大升级，是实现了**同步缓存失效**。

通过对 Docstore 存储引擎的改造，现在每一次写事务在提交前，都能返回该事务所影响的所有行的主键。查询引擎层在收到这些主键后，可以**在写请求返回给客户端之前，同步地向 Redis 发送失效指令**。

这一改进，结合仍在后台运行的 Flux（作为兜底），为 CacheFront 提供了近乎**读己所写 (Read-your-own-writes)** 的强一致性保证，使得更多对一致性敏感的业务得以放心地使用缓存。

#### 可观测性与弹性设计

为了在 Uber 的规模下可靠运行，CacheFront 还构建了一系列令人印象深刻的弹性与可观测性特性：

**Cache Inspector**：一个独立的 CDC 消费者，它会延迟一分钟消费 binlog，并持续地将数据库中的“真相”与缓存中的数据进行对比，实时度量缓存的**不一致率**（Staleness），并将其作为核心 SLO 指标。**跨地域缓存预热 (Cache Warming)**：通过复制 Redis 的写操作流（而非数据本身）到灾备区域，并在灾备区域模拟“读请求”来填充缓存，实现了高效且数据一致的跨地域缓存预热。**自适应超时 (Adaptive Timeouts)**：动态调整对 Redis 的请求超时时间，以匹配当前 P99.99 的网络延迟，避免了因超时设置不当导致的大量缓存穿透。**熔断器 (Circuit Breakers)**：当某个 Redis 节点出现故障时，能快速熔断对该节点的请求，防止雪崩效应。**智能分片**：缓存的分片键与数据库的分片键故意设计为不同，以避免当某个 Redis 集群故障时，压力集中冲击到数据库的单个分片上。

## 成果：支撑 1.5 亿 QPS 的巨兽

经过多年的迭代，CacheFront 取得了惊人的成果：

**支撑超过 1.5 亿 QPS 的峰值读取**，缓存命中率高达 99% 以上。- P75 延迟降低
**75%**，P99.9 延迟降低**67%**。 - 通过缓存卸载，为一个核心用例节省了约
**57,000**个 CPU 核心的数据库容量。 - 缓存不一致率维持在
**99.99%**以上的极高水平。

## 小结：没有银弹，唯有持续演进

Uber 存储架构的约十年演进史(2016~2025)，是一个从解决眼前问题到构建长远平台，从拥抱 NoSQL 灵活性到回归 SQL 强一致性，最终通过极致的缓存优化来平衡成本与性能的经典故事。

它为所有构建大规模后端系统的工程师提供了宝贵的启示：

**基于成熟组件构建**：Docstore 的成功，在于它没有重新发明轮子，而是巧妙地站在了 MySQL 这个巨人的肩膀上。**演进式架构**：没有一劳永逸的架构。系统必须能够根据业务需求的变化而持续演进，甚至进行方向性的调整。**缓存不是“银弹”，而是系统工程**：一个生产级的缓存系统，远不止是“放一个 Redis 在前面”那么简单。它需要深度的系统集成、精巧的一致性保障机制和强大的可观测性与弹性设计。

最终，支撑 Uber 全球业务的，并非某一项神秘的“黑科技”，而是一系列坚实的、经过深思熟虑的、在真实世界的炮火中不断迭代和完善的工程决策。

## 参考资料

[Evolving Schemaless into a Distributed SQL Database](https://www.uber.com/blog/schemaless-sql-database/)– https://www.uber.com/blog/schemaless-sql-database/[How Uber Serves Over 40 Million Reads Per Second from Online Storage Using an Integrated Cache](https://www.uber.com/blog/how-uber-serves-over-40-million-reads-per-second-using-an-integrated-cache)– https://www.uber.com/blog/how-uber-serves-over-40-million-reads-per-second-using-an-integrated-cache[How Uber Serves over 150 Million Reads per Second from Integrated Cache with Stronger Consistency Guarantees](https://www.uber.com/blog/how-uber-serves-over-150-million-reads/)– https://www.uber.com/blog/how-uber-serves-over-150-million-reads

**想系统学习Go，构建扎实的知识体系？**

我的新书《Go语言第一课》是你的首选。源自2.4万人好评的极客时间专栏，内容全面升级，同步至Go 1.24。首发期有专属五折优惠，不到40元即可入手，扫码即可拥有这本300页的Go语言入门宝典，即刻开启你的Go语言高效学习之旅！

![](../../assets/d3fd3ab3e1fd7a7e.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论