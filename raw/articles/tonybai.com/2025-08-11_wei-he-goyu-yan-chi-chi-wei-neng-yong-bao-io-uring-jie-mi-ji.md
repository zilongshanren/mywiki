---
title: 为何Go语言迟迟未能拥抱 io_uring？揭秘集成的三大核心困境
url: https://tonybai.com/2025/08/11/why-go-not-embrace-iouring/
published: '2025-08-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为何Go语言迟迟未能拥抱 io_uring？揭秘集成的三大核心困境

![](../../assets/1d162b3c4ba9e1e7.png)


[本文永久链接](https://tonybai.com/2025/08/11/why-go-not-embrace-iouring) – https://tonybai.com/2025/08/11/why-go-not-embrace-iouring

大家好，我是Tony Bai。

在 Linux I/O 的世界里，io_uring 如同划破夜空的流星，被誉为“终极接口”。它承诺以无与伦比的效率，为数据密集型应用带来革命性的性能提升。正如高性能数据库 ScyllaDB 在其[官方博文](https://www.scylladb.com/2020/05/05/how-io_uring-and-ebpf-will-revolutionize-programming-in-linux/)中所展示的，io_uring 能够将系统性能推向新的高峰。

然而，一个令人费解的问题摆在了所有 Go 开发者面前：作为云原生infra和并发编程的标杆，Go 语言为何对这颗唾手可得的“性能银弹”表现得如此审慎，甚至迟迟未能将其拥抱入标准库的怀抱？一场在 Go 官方仓库持续了五年之久的 [Issue 讨论（#31908）](https://github.com/golang/go/issues/31908)，为我们揭开了这层神秘的面纱。这并非简单的技术取舍，而是 Go 在其设计哲学、工程现实与安全红线之间进行反复权衡的结果。本文将深入这场讨论，为您揭秘阻碍 io_uring 在 Go 中落地的三大核心困境。

## io_uring：一场 I/O 模型的革命

要理解这场争论，我们首先需要明白 io_uring 究竟是什么，以及它为何具有革命性。

在 io_uring 出现之前，Linux 上最高效的 I/O 模型是 epoll。epoll 采用的是一种“拉（pull）”模型：应用程序通过一次 epoll_wait 系统调用来询问内核：“有我关心的文件描述符准备好进行 I/O 了吗？”。内核响应后，应用程序需要再为每个就绪的描述符分别发起 read 或 write 系统调用。这意味着，**处理 N 个 I/O 事件至少需要 N+1 次系统调用**。

而 io_uring 则彻底改变了游戏规则。它在内核与用户空间之间建立了两个共享内存环形缓冲区：**提交队列（Submission Queue, SQ）**和**完成队列（Completion Queue, CQ）**。

![](https://tonybai.com/wp-content/uploads/2025/why-go-not-embrace-iouring-2.png)


其工作流程如下：

**提交请求:**应用程序将一个或多个 I/O 请求（如读、写、连接等）作为条目（SQE）放入提交队列中。这仅仅是内存操作，**几乎没有开销**。**通知内核:**应用通过一次 io_uring_enter 系统调用，通知内核“请处理队列中的所有请求”。在特定模式（SQPOLL）下，这个系统调用甚至可以被省略。**内核处理:**内核从提交队列中批量取走所有请求，并异步地执行它们。**返回结果:**内核将每个操作的结果作为一个条目（CQE）放入完成队列。这同样只是内存操作。**应用收获:**应用程序直接从完成队列中读取结果，无需为每个结果都发起一次系统调用。

这种模式的优势是颠覆性的：**它将 N+1 次系统调用压缩为 1 次甚至 0 次**，极大地降低了上下文切换的开销，并且首次为 Linux 带来了真正意义上的、无需 O_DIRECT 标志的**异步文件 I/O**。

## 最初的希望：一剂治愈 Go I/O“顽疾”的良药

讨论伊始，Go 社区对 io_uring 寄予厚望，期待它能一举解决 Go 在 I/O 领域的两大历史痛点：

**真正的异步文件 I/O：**Go 的网络 I/O 基于 epoll 实现了非阻塞，但文件 I/O 本质上是阻塞的。为了避免阻塞系统线程，Go 运行时不得不维护一个线程池来处理文件操作。正如社区所期待的，io_uring 最大的吸引力在于**“移除对文件 I/O 线程池的需求”**，让文件 I/O 也能享受与网络 I/O 同等的高效与优雅。**极致的网络性能：**对于高并发服务器，io_uring 通过将多个 read/write 操作打包成一次系统调用，能显著降低内核态与用户态切换的开销，这在“熔断”和“幽灵”漏洞导致 syscall 成本飙升的后时代尤为重要。

然而，Go 核心团队很快就为这股热情泼上了一盆“冷水”。

## 核心困境一：运行时模型的“哲学冲突”

这是阻碍 io_uring 集成最根本、最核心的障碍。Go 的成功很大程度上归功于其简洁的并发模型——goroutine，以及对开发者完全透明的调度机制。但 io_uring 的工作模式，与 Go 运行时的核心哲学存在着深刻的冲突。

**冲突的焦点在于“透明性”**。Ian Lance Taylor 多次强调，问题不在于 io_uring 能否在 Go 中使用，而在于能否**“透明地”**将其融入现有的 os 和 net 包，而不破坏 Go 开发者早已习惯的 API 和心智模型。

io_uring 的性能优势源于**批处理**。但 Go 的标准库 API，如 net.Conn.Read()，是一个独立的、阻塞式的调用。Go 用户习惯于在独立的 goroutine 中处理独立的连接。如何将这些分散的独立 I/O 请求，在用户无感知的情况下，**“透明地”**收集起来，打包成批？这几乎是一个无解的难题。

社区也提出了“每个 P (Processor) 一个 io_uring 环”的设想，但 Ian 指出这会引入极高的复杂性，包括环的争用、空闲 P 的等待与唤醒、P 与 M 切换时的状态管理等。正如一些社区成员所总结的，io_uring 需要一种全新的 I/O 模式，而这与 Go 现有网络模型的模式完全不同。强行“透明”集成，无异于“在不破坏现有 API 的情况下进行不必要的破坏”。

## 核心困境二：现实世界的“安全红线”

如果说运行时模型的冲突是理论上的“天堑”，那么安全问题则是实践中不可逾越的“红线”。

在 2024 年初，社区成员 jakebailey 抛出了一个重磅消息：**出于安全考虑，Docker 默认的 seccomp 配置文件已经禁用了 io_uring**。


引用自 Docker 的 commit 信息:“安全专家普遍认为 io_uring 是不安全的。事实上，Google ChromeOS 和 Android 已经关闭了它，所有 Google 生产服务器也关闭了它。”

这个消息对标准库集成而言几乎是致命一击。Go 程序最常见的部署环境就是容器。一个不被“普遍情况”支持的特性，无论其性能多么优越，都难以成为Go运行时和标准库的基石。

## 核心困境三：追赶一个“移动的目标”

在这场长达五年的讨论中，io_uring 自身也在飞速进化。其作者[Jens Axboe](https://github.com/axboe) 甚至亲自下场，[解答了 Go 团队早期的疑虑](https://github.com/golang/go/issues/31908#issuecomment-571651387)，例如移除了并发数限制、解决了事件丢失问题等。

但这恰恰揭示了第三重困境：**要集成一个仍在高速演进、API 不断变化的底层接口，本身就充满了风险和不确定性**。标准库追求的是极致的稳定性和向后兼容性。过早地依赖一个“移动的目标”，可能会带来持续的维护负担和潜在的破坏性变更。对于一个需要支持多个内核版本的语言运行时来说，这种复杂性是难以承受的。

## 小结：审慎的巨人与退潮的社区热情

io_uring 未能在 Go中落地，并非因为 Go 团队忽视性能，而是其成熟与审慎的体现。三大核心困境层层递进，揭示了其迟迟未能拥抱 io_uring 的深层原因：**哲学上的范式冲突、现实中的安全红线、以及工程上的稳定性质疑。**

然而，现实比理论更加残酷。在讨论初期，Go 社区曾涌现出一批充满激情的用户层 io_uring 库，如 giouring、go-uring 等，它们是开发者们探索新大陆的先锋。但时至 2025 年，我们观察到一个令人沮丧的趋势：**这些曾经的追星项目大多已陷入沉寂，更新寥寥，星光黯淡。**

与之形成鲜明对比的是，Rust 的 tokio-uring 库依然保持着旺盛的生命力，社区活跃，迭代频繁。这似乎在暗示，问题不仅在于 io_uring 本身，更在于它与特定语言运行时模型的“契合度”。[Go 运行时的 G-P-M 调度模型](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4036682086282166273#wechat_redirect)和它所倡导的编程范式，使得社区自发的集成尝试也步履维艰，最终热情退潮。

这是否意味着 Go 与 io_uring 将永远无缘？或许未来之路有二：一是等待 io_uring 自身和其生态环境（尤其是安全方面）完全成熟；二是 Go 也许可能会引入一套全新的、**非透明的**、专为高性能 I/O 设计的新标准库包。

在此之前，Go 运行时可能会选择先挖掘 epoll 的全部潜力。这场长达五年的讨论，最终为我们留下了一个深刻的启示：技术的采纳从来不是一场单纯的性能赛跑，它是一场包含了设计哲学、生态现实与工程智慧的复杂博弈。

资料链接：

- https://github.com/golang/go/issues/31908
- https://www.scylladb.com/2020/05/05/how-io_uring-and-ebpf-will-revolutionize-programming-in-linux/

关注io_uring在Linux kernel内核演进的小伙伴儿们，可以关注[io-uring.vger.kernel.org archive mirror](https://lore.kernel.org/io-uring/)这个页面，或[io_uring作者Jens Axboe的liburing wiki](https://github.com/axboe/liburing/wiki)。

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论