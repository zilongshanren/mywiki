---
tags: [go, 并发, 消息传递, 协程]
date: 2026-04-14
sources: 1
---

# Go 的 goroutine 与 channel

Go 把 CSP 风格的并发模型作为语言的一等公民：goroutine 是极轻量的用户态协程，`chan` 是带类型的同步/异步消息管道，`select` 在多条 channel 上多路复用事件。对于长期用 C 写服务器的人而言，这几乎是一次结构性的解放：过去需要自己实现的[[coroutine]]、[[ring-buffer-virtual-stream|事件环]]、信号量与工作队列，全部被语言收编。

[[cloudwu]] 在 2010 年尝试 Go 时的感受很有代表性：他曾花八年时间锤炼用纯 C 构建带有初始化顺序、包隔离、接口聚合和 coroutine 支持的代码规范，结果发现那些规范只是在"拙劣地模仿 Go"。Go 的 interface 更接近他在 C 里惯用的 mix-in 面向对象风格——没有继承层次，只有组合功能；[[c-interface-oop|用函数指针把各个平坦模块聚合在一起]]在有了 interface 语法后变得舒服许多。

`defer` 取代了 C++ 在栈对象析构上打的 RAII 补丁，`panic / recover` 以极少的语法面积替代了 exception。包系统明确区分 init 而无 exit，这与他长期对 [[modular-design|模块生命期]]的主张完全吻合——所有数据结构一律以 0 初始化 (类似 calloc)，不再有未定义状态。goroutine + `select/chan` 则把网络服务器常见的"阻塞 IO + 事件驱动"两种风格统一了起来：每个连接用独立 goroutine 阻塞读写，主循环只对 channel 做 select，外观类似 Erlang 事件模型而语法是纯正 C 系血统。

云风用这一套把自己 2006 年写的 [[connection-multiplexer-gateway|多连接汇聚服务器]]用大约 240 行 Go 重写。对外 N 条 socket、对内 1 条管道，`len + id` 的三字节头把 N 路 TCP 合并为单流；控制指令走 0 号特殊连接，用 in-memory pipe 转成 `bufio.Reader` 按行解析；性能上唯一需要手工优化的点是给对外包加头时批量向 16K 数组借 slice——他特意强调 Go 的 slice 只是对 array 的部分引用，创建极廉价，这种"区分引用与值"的清晰度让 Go 比 Java 更像 C，却提供了 C++ 给不出的安全性。

## 相关
- [[cloudwu]]
- [[connection-multiplexer-gateway]]
- [[c-interface-oop]]
- [[garbage-collector]]
- [[modular-design]]
- [[stackless-vs-stackful-coroutines]] —— goroutine 走可增长栈的 stackful 路线，C++20 走 stackless 状态机路线，对比参见 Ben Supnik 的分析

## Sources

- [[sources/cloudwu-go-first-impressions]]
