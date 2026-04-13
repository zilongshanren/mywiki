---
title: 原子操作的瓶颈与Go的多核扩展性之痛：深入剖析sync.ShardedValue及per-CPU提案
url: https://tonybai.com/2025/05/19/shardedvalue-per-cpu-proposal/
published: '2025-05-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 原子操作的瓶颈与Go的多核扩展性之痛：深入剖析sync.ShardedValue及per-CPU提案

![](../../assets/bf749396048e6043.png)


[本文永久链接](https://tonybai.com/2025/05/19/shardedvalue-per-cpu-proposal) – https://tonybai.com/2025/05/19/shardedvalue-per-cpu-proposal

大家好，我是Tony Bai。

在追求极致性能的道路上，Go 语言凭借其简洁的并发模型和高效的调度器，赢得了众多开发者的青睐。然而，随着现代服务器 CPU核心数量的不断攀升，一些我们曾经习以为常的“快速”操作，在高并发、多核环境下，也逐渐显露出其性能瓶颈。其中，**原子操作 (atomic operations)** 的扩展性问题，以及标准库中一些依赖原子操作的并发原语（如 sync.RWMutex）的性能表现，成为了社区热议的焦点。

最近，fasthttp 的作者及 VictoriaMetrics 数据库的联合创始人 Aliaksandr Valiakin (valyala) 在 X.com 上的一番“叹息”，更是将原子计数器的扩展性问题推向了前台：

![](../../assets/9d0eb480bd08edac.png)


Valyala 指出：“基于原子操作的计数器更新性能在多 CPU 核心上无法扩展，因为每个 CPU 核心在增量操作期间都需要从慢速内存中原子加载实际的计数器值。因此，实际性能受限于内存延迟（约 15ns，即每秒 6 千万次增量）。通过使用可缓存于 CPU L1 缓存的 per-CPU 计数器，可以将单 CPU 核心性能提升至每秒数十亿次增量。遗憾的是，Go 语言本身并未提供高效处理 per-CPU 数据的函数。”

这番话点出了一个残酷的现实：即使是看似轻量级的原子操作，在多核“混战”中也可能成为性能的阿喀琉斯之踵。那么，这背后的深层原因是什么？Go 社区又在如何探索解决之道呢？今天，我们就来深入剖析这个问题，并解读 Go 项目 issue 中几个重要的相关提案，同时看看社区是如何先行一步尝试解决这类问题的。

## 原子操作为何在高并发多核下“失速”？sync.RWMutex 的痛点

要理解原子操作的瓶颈，我们需要潜入到 CPU 缓存的微观世界。现代多核 CPU 为了加速内存访问，都配备了多级缓存（L1, L2, L3）。当多个核心同时读写同一块内存区域时，就需要**缓存一致性协议 (Cache Coherence Protocols)**（如 MESI，Modify-Exclusive-Shared-Invalid）来确保数据的一致性。

当我们对一个共享变量（即使是原子变量）进行写操作时，例如 atomic.AddInt64，会发生什么？

- 执行该操作的 CPU 核心需要获得对该变量所在
**缓存行 (Cache Line)**的独占访问权 (Exclusive state)。 - 如果其他核心的缓存中也存在这份缓存行的副本（即使是共享状态 Shared state），它们会被标记为无效 (Invalidate)。
- 当其他核心再次需要访问这个变量时，就会发生缓存未命中 (Cache Miss)，需要从更高级别的缓存或主内存中重新加载数据，并可能再次引发缓存行在不同核心间的同步。

在高并发场景下，如果多个核心**频繁地对同一个缓存行中的原子变量进行写操作**，就会导致：

**缓存行在不同核心的 L1/L2 缓存之间频繁失效和同步**，这个过程被称为“缓存行乒乓 (Cache Line Ping-Ponging)”。- 产生大量的
**总线流量和内存访问延迟**。

这就是所谓的**真共享 (True Sharing)** 争用。即使原子操作本身在单个核心上执行得非常快，这种跨核心的缓存同步开销也会让其整体性能急剧下降。

这个问题的典型体现之一，便是 Go 标准库中的 sync.RWMutex。正如 github.com/jonhoo/drwmutex 项目在其 README 中指出的：“Go 默认的 sync.RWMutex 在多核下扩展性不佳，因为所有读操作者在尝试原子性地增加同一个内存位置（用于读者计数）时会产生争用。” 对于读多写少的场景，本应高效的读锁操作，却因为内部共享计数器的原子更新而受到了性能限制。

## 社区的先行者：jonhoo/drwmutex 的分片读写锁实践

面对标准库 sync.RWMutex 在多核环境下的扩展性瓶颈，社区早已开始了积极的探索。一个显著的例子便是 jonhoo/drwmutex，一个 n 路分片读写锁（Distributed Read-Write Mutex）的实现，也被称为“大读者”锁。

其核心思想非常直观：**为每个 CPU 核心提供其自己的 RWMutex 实例。读者只需要获取其核心本地的读锁，而写者则必须按顺序获取所有核心上的锁。** 这种设计通过将读操作的争用分散到各个核心，从而显著提升了读多写少场景下的并发性能。

![](../../assets/48b73e8547939368.png)


jonhoo/drwmutex 的实现也揭示了构建这类 per-CPU 优化方案的一些关键技术点和挑战：

**获取当前 CPU ID：**为了将操作路由到正确的本地锁，需要一种方法来确定当前 goroutine 正在哪个 CPU 核心上运行。drwmutex 在 Linux x86 平台上使用了 CPUID 汇编指令来获取 APICID，并在程序启动时构建 APICID 到 CPU 索引的映射。这突显了获取可靠且高效的 CPU/P 标识是实现此类优化的一个难点。**CPU 信息可能过时：**README 中也坦诚地指出，goroutine 获取到的 CPU 信息可能是过时的（因为 goroutine 可能已被调度到其他核心），但这主要影响性能而非正确性（只要读者记住它获取的是哪个锁）。OS 内核通常会尽量将线程保持在同一核心以提高缓存命中率，这在一定程度上缓解了这个问题。**性能表现与 NUMA 效应：**jonhoo/drwmutex 的性能测试表明，在核心数较多，特别是写操作比例低于 1% 时，其性能远超 sync.RWMutex。有趣的是，其性能图表还揭示了 NUMA (Non-Uniform Memory Access) 效应的影响——在测试机器上每增加一个包含 10 个核心的 NUMA 节点，跨核心流量的成本就会增加，导致性能曲线出现波动。

jonhoo/drwmutex 的实践不仅提供了一个解决 sync.RWMutex 性能问题的有效方案，也为后续 Go 官方和社区在 per-CPU 数据结构方面的探索提供了宝贵的经验和参照。

## 官方的早期探索：sync.ShardedValue 的初心与挑战 (#18802)

在社区积极探索的同时，Go 核心团队也早已关注到这类问题。一个重要的早期官方提案便是由 Austin Clements 在 2017 年提出的 **sync.ShardedValue (issue #18802)**。

sync.ShardedValue 的核心思想与 jonhoo/drwmutex 有异曲同工之妙：**提供一种机制来创建和使用分片值，将一个逻辑上的共享值分散到多个独立的“分片”中，每个分片与一个 CPU 核心或更准确地说是 Go 调度器中的 P (Processor) 相关联。** 这样，每个 P 上的 goroutine 优先访问其本地分片，从而大大减少对单一共享内存位置的争用。

该提案围绕 Get()、Put() 和 Do() 等核心 API 进行了深入讨论，涉及了诸多设计维度，例如 Get/Put 的阻塞性、溢出处理、Do 操作的一致性等。尽管因难以就“最重要的问题达成共识”而被搁置，但 sync.ShardedValue 提案为后续的探索奠定了重要的基础，并清晰地指明了通过“分片”来提升多核扩展性的方向。

## 新的尝试：valyala 的 sync.PLocalCache (#69229) 与 sync.MLocal (#73667)

近期，valyala 基于其在 fasthttp 和 VictoriaMetrics 等高性能项目中的实践经验，提出了两个更聚焦、API 更简洁的提案，试图从特定场景切入，解决 per-CPU/per-P/per-M 数据的高效访问问题。

**1. sync.PLocalCache (issue #69229): Per-P 对象缓存**

**设计目标：**为 CPU 密集型的算法提供一个高效且可随 CPU 核心数线性扩展的**状态缓存机制**。**API 设计：**核心是 Get() (返回 P 本地对象，若无则返回 nil) 和 Put() (将对象放回 P 本地存储)，保证 Get() 返回的对象只能被当前 goroutine 访问，无需额外同步。**解决痛点：**旨在解决 sync.Pool 在作为严格 per-P 缓存时存在的问题，如跨 P 窃取、内存浪费和 GC 清理等。

**2. sync.MLocal[T any] (issue #73667): Per-M (OS 线程) 泛型存储**

**设计目标：**为需要在 OS 线程层面实现数据隔离以达到线性扩展性的并发代码，提供 M 本地存储。**API 设计 (泛型)：**提供 Get() (返回当前 M 的 *T 项) 和 All() (返回所有 M 上的项)。**解决痛点：**直接应对 valyala 在 VictoriaMetrics 中遇到的共享缓冲区互斥锁争用导致的扩展性瓶颈。

## 这些提案的共性、差异与启示

无论是社区的 jonhoo/drwmutex 实践，还是官方及 valyala 的提案，它们的核心目标都是一致的：**通过数据的分片或本地化，最大限度地减少多核间的共享内存争用，从而提升高并发应用在多核处理器上的性能和可伸缩性。**

然而，它们在具体实现、API 设计的通用性、易用性以及针对的场景上有所不同：

- jonhoo/drwmutex 是一个针对特定问题（读写锁）的具体解决方案，它依赖平台相关的 CPUID 指令，并自己处理了核心映射和数据同步。
- sync.ShardedValue 试图提供一个更通用的分片值抽象，但也因此面临更大的设计复杂性和社区共识挑战。Austin Clements 后续也反思了早期设计，并提出了更优的“检出/检入”模型。
- sync.PLocalCache 和 sync.MLocal 则更为聚焦，API 更简洁，分别针对 per-P 缓存和 per-M 存储这两个具体场景。

这些探索过程也充满了 Go 社区对技术细节的极致追求和严谨思辨，例如关于命名（”sharding” vs “perCPU” vs “SplitValue”）、GOMAXPROCS 动态变化的影响、与 GC 的交互、API 语义的精确性（如 mknyszek 提出的包含 Merge 方法的 ShardedValue API 及其多种语义可能）以及泛型的应用等。

## 展望未来：Go 如何更好地拥抱多核时代？

原子操作的瓶颈、标准库并发原语的局限，以及社区和官方对 per-CPU/P/M 存储方案的持续探索，清晰地表明了 Go 语言在追求极致多核扩展性方面仍有提升空间。解决这类底层并发原语的性能问题，对于 Go 在高性能服务器、大规模分布式系统、数据库、监控系统等领域的持续领先至关重要。

未来，我们或许会看到：

**更底层的运行时支持：**Go 运行时可能会暴露更底层的、与调度器（P、M）相关的亲和性原语，或提供高效获取当前 P/核心 ID 的标准方法，正如 jonhoo/drwmutex 所尝试的那样。**标准库中出现新的同步原语：**借鉴这些提案和社区实践的精华，可能会有新的、经过精心设计的同步原语加入到 sync 或 sync/atomic 包中。**社区持续贡献优秀的解决方案：**像 jonhoo/drwmutex 这样的项目，即使官方没有立即提供标准方案，社区也会基于现有技术孵化出优秀的第三方库。

## 小结

从 valyala 对原子操作性能的“叹息”，到 jonhoo/drwmutex 的巧妙实践，再到 Go 社区围绕 sync.ShardedValue、sync.PLocalCache、sync.MLocal 等提案的深入探讨，我们看到了 Go 语言在追求极致性能道路上永不停歇的脚步。这不仅仅是关于几个新的 API，更是关于 Go 如何在多核时代继续保持其并发优势和工程效率的战略思考。

作为 Gopher，关注这些讨论和提案的进展，理解其背后的设计哲学和技术挑战，不仅能让我们更深刻地认识 Go 语言，也能启发我们在自己的高性能项目中进行类似的性能优化思考和实践。

让我们共同期待 Go 在多核扩展性方面能迈出更坚实的步伐，为构建更高性能的未来系统提供更强大的动力！

## 参考资料

[Distributed Read-Write Mutex in Go](https://github.com/jonhoo/drwmutex)– https://github.com/jonhoo/drwmutex[proposal: sync: support for sharded values #18802](https://github.com/golang/go/issues/18802)– https://github.com/golang/go/issues/18802[proposal: sync: add M-local storage #73667](https://github.com/golang/go/issues/73667)– https://github.com/golang/go/issues/73667[proposal: sync: add PLocalCache #69229](https://github.com/golang/go/issues/69229)– https://github.com/golang/go/issues/69229

**聊一聊，也帮个忙：**

**在你的 Go 项目中，是否也曾遇到过原子操作或 sync.RWMutex 在高并发多核下的性能瓶颈？你是如何解决的？是否尝试过类似 jonhoo/drwmutex 的分片锁方案？****对于 Go 社区提出的这些 per-CPU/P/M 存储提案，你认为哪种设计思路更具潜力？或者你有什么更好的建议？****你认为 Go 语言在提升多核扩展性方面，未来最应该关注哪些方向？**

欢迎在**评论区**留下你的经验、思考和问题。如果你觉得这篇文章对你有所启发，也请**转发给你身边的 Gopher 朋友们**，让更多人参与到这场关于 Go 性能未来的讨论中来！

![](../../assets/ab2d7a5176ba4b48.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论