---
tags: [消息队列, 分布式系统, ZeroMQ, 并发]
date: 2026-04-14
sources: 1
---

# ZeroMQ 的三种消息模式

ZeroMQ 不是 socket 的"另一个封装"，它比 TCP 高一级：它放弃了"通讯基于一对一连接"这个隐含假设，改为按 **角色 / 模式** 定义端点，底层既可以走 TCP，也可以走 IPC 或进程内。对上层而言，`bind / listen / accept` 这种流程被抹掉了——因为模式天然是 1:N，不必为每条通道单独留 handle；而且不必在意谁先启动，connect 先行也合法，这让原本复杂的启动脚本（谁先谁后）一并消失。

[[cloudwu]] 读完 ZeroMQ Guide 后总结：真正常用的只有三种模型，所有分布式、并行需求都能用它们组合出来——

- **请求/回应（Request/Reply）**：请求端一定是收发成对出现，回应端一定是发收成对出现；两端都可以是 1:N，常把 1 当 server、N 当 client；通过引入 device（路由节点）可以把 1:N 扩为 N:M，端点地址对上层完全透明，每个请求隐含回应地址。
- **发布/订阅（Pub/Sub）**：发布端单向广播，不保证订阅端此时是否在线——连接建立前发出的消息直接丢弃，但连接后中间不会丢。订阅端同样单向只收。若需要反馈（例如确认谁订阅了），额外再架一个 request/reply socket。
- **管道（Push/Pull）**：管道是单向流，从 PUSH 单向推送到 PULL，适合 fan-out 的工作分发。

这三种模式把"消息通讯"这件事切得足够干净，也是 [[go-goroutine-channels|Go 的 chan/select]] 或 Erlang 消息风格在分布式层面的自然延伸。ZeroMQ 的 Transient / Durable socket 并不是区分"是否保持 TCP 连接"，而是概念层面的生命期——Durable socket 的生命期可以跨越进程重启（需要时甚至能把 buffer 落到磁盘），这不是崩溃恢复，而是一种刻意保留的设计余地。

云风给网络游戏服务器的推荐架构是：玩家侧仍用定制的 [[connection-multiplexer-gateway|连接网关]]接收海量客户端，网关之内的服务集群之间全部用 ZeroMQ——业务节点只按 request/reply、pub/sub、pipeline 三种角色思考，不再纠结 socket 生命期与启动顺序。

## 相关

- [[cloudwu]]
- [[go-goroutine-channels]]
- [[connection-multiplexer-gateway]]

## Sources

- [[sources/cloudwu-zeromq-patterns]]
