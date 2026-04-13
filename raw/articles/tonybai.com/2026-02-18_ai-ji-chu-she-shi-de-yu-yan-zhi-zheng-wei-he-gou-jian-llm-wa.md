---
title: AI 基础设施的语言之争：为何构建 LLM 网关时，我们放弃了 Python 选择了 Go？
url: https://tonybai.com/2026/02/18/why-we-chose-go-over-python-for-llm-gateways/
published: '2026-02-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# AI 基础设施的语言之争：为何构建 LLM 网关时，我们放弃了 Python 选择了 Go？

![](../../assets/1d78b6f82440ed61.png)


[本文永久链接](https://tonybai.com/2026/02/18/why-we-chose-go-over-python-for-llm-gateways) – https://tonybai.com/2026/02/18/why-we-chose-go-over-python-for-llm-gateways

大家好，我是Tony Bai。

在 2026 年的今天，人工智能早已走出了实验室，成为企业级应用的核心驱动力。Python，凭借其在机器学习领域的绝对统治地位——拥有 PyTorch、TensorFlow、Hugging Face 等无可匹敌的生态系统——长期以来被视为 AI 开发的“默认语言”。

然而，随着 AI 应用从模型训练（Training）走向推理服务（Inference）和应用编排（Orchestration），工程重心发生了微妙的转移。当我们谈论模型本身时，Python 是王者；但当我们谈论**承载模型流量的基础设施**——网关、代理、路由器时，Python 还是最佳选择吗？

近日，[开源 LLM 网关项目 Bifrost](https://github.com/maximhq/bifrost) 的维护者在 Reddit 上分享了一篇题为《[Why we chose Go over Python for building an LLM gateway](https://www.reddit.com/r/golang/comments/1r27pqx/why_we_chose_go_over_python_for_building_an_llm/)》的技术复盘，引发了社区的强烈反响。他们放弃了拥有 LiteLLM 等成熟竞品的 Python 生态，转而使用 Go 重写了核心网关。结果令人咋舌：延迟降低了约 700 倍，内存占用降低了 68%，吞吐量提升了 3 倍。

这场技术选型的背后，折射出的是 AI 工程化进入深水区后，对[并发模型](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4105816518230016005#wechat_redirect)、资源效率与部署架构的重新审视。

![](../../assets/e9c16d84a31ad3b6.png)


## Python 的“舒适区”与“性能墙”

在项目的初期，选择 Python 似乎是理所当然的。

**1. 生态惯性与“胶水”优势**

绝大多数 AI 工程师都是 Python Native。从 LangChain 到 LlamaIndex，几乎所有的 Agent 开发框架都优先支持 Python。使用 Python 构建网关，意味着可以直接复用现有的库，甚至可以直接挂载一些轻量级的 Python 逻辑来处理 Embeddings 或 RAG（检索增强生成）流程。FastAPI 的易用性更是让开发者能在几分钟内搭建起一个服务。

**2. 遭遇瓶颈：网关的本质是 I/O**

然而，LLM 网关的业务属性决定了它的性能痛点。与计算密集型（CPU-bound）的模型推理不同，网关是典型的 I/O 密集型应用。它的核心职责是：

- 接收成千上万的客户端请求。
- 将请求转发给上游提供商（如 OpenAI, Anthropic, 或自建的 vLLM）。
- 等待上游响应（这是最耗时的环节，LLM 的首字延迟 TTFT 通常在秒级）。
- 将流式响应（SSE）回传给客户端。

在这个过程中，网关绝大部分时间都在“等待”。

**3. Python 的并发痛点**

Bifrost 团队在测试中发现，当并发请求数达到 500-1000 RPS（每秒请求数）时，Python 的瓶颈开始显现。

- GIL（全局解释器锁）的幽灵：虽然 Python 的 asyncio 可以处理 I/O 并发，但 GIL 依然限制了多核 CPU 的利用率。对于需要处理大量并发连接、同时可能涉及少量数据处理（如 Token 计数、PII 过滤）的网关来说，线程竞争（Thread Contention）成为了不可忽视的开销。
- 昂贵的上下文切换：在 Python 中维持数千个并发连接，其上下文切换的开销远高于编译型语言。

## Go 的降维打击——数据背后的技术真相

Bifrost 团队最终选择了 Go。这一决定并非出于对语言的偏好，而是基于冷冰冰的 Benchmark 数据。让我们深入分析他们披露的核心指标。

![](../../assets/dd86f31bdd9d755e.png)


### 延迟（Latency）：微秒与毫秒的鸿沟


数据对比：

*Bifrost (Go): ~11 微秒 (0.011ms) / 请求

*LiteLLM (Python): ~8 毫秒 / 请求

这是一个惊人的 **700 倍** 差距。

虽然 8 毫秒在人类感知中似乎微不足道，但在高并发架构中，这被称为“开销放大”。

- 累积效应：在一个复杂的 AI Agent 工作流中，可能涉及几十次 LLM 调用。如果每一层网关都增加 8ms 的延迟，累积起来就是可感知的卡顿。
- 高负载下的劣化：在 10,000 个并发请求下，Go 引入的总处理时间仅为 110ms，而 Python 方案则产生了惊人的 80 秒总 CPU 时间开销。这意味着 Python 方案需要消耗更多的 CPU 核心来维持同样的响应速度，否则请求就会排队，导致尾部延迟（Tail Latency）飙升。

此外，Go 的 net/http 标准库在处理 HTTP 请求时经过了极致优化。Go 不需要像 Python 那样依赖 ASGI/WSGI 服务器（如 Uvicorn），其原生的 HTTP 处理能力配合 Goroutine，使得每个请求的内存分配和 CPU 周期都降到了最低。

### 并发模型：Goroutine vs Asyncio


架构对比：

*Go: 10,000 个 Goroutines，每个仅占用 ~2KB 栈空间。

*Python: 受限于 OS 线程开销或 Event Loop 的单核瓶颈。

LLM 网关的特殊性在于长连接。LLM 的流式输出可能持续数秒甚至更久。这意味着网关必须同时维护成千上万个活跃连接。

Go 的 GMP（Goroutine-Machine-Processor）调度模型天生适合这种场景。成千上万个 Goroutine 可以复用少量的系统线程，上下文切换由 Go Runtime 在用户态极速完成，几乎不消耗系统内核资源。

相比之下，Python 即使使用了 uvloop，在面对海量并发连接的数据搬运时，其解释器的开销依然是一个沉重的包袱。

### 内存效率与成本


数据对比：

*Go: 内存占用降低 ~68%。

*生产环境: Go 跑在 t3.medium (2 vCPU, 4GB) 上即可；Python 则需要 t3.xlarge。

对于大规模部署 AI 服务的企业来说，这意味着基础设施成本直接减半。

Python 的动态类型系统和垃圾回收机制导致其对象内存占用较大。而 Go 的结构体布局紧凑，且编译器能进行逃逸分析（Escape Analysis），将大量对象分配在栈上而非堆上，从而显著降低了 GC 压力和内存占用。

## 社区深度探讨——AI 时代的语言版图重构

这篇帖子在 r/golang 引发了极高质量的讨论，评论区揭示了行业内更深层次的趋势。

### “AI 能够写代码”改变了竞争规则

过去，Python 的一大优势是“开发效率高”。写 Python 代码通常比写 Go 或 Rust 快。

但在 2026 年，“Agentic Coding”（即利用 AI Coding Agent 辅助编程）已经成为主流。

有开发者指出：“LLM 让编写 Rust 和 Go 变得非常高效，你完全可以享受到高性能语言的红利，而不用支付编写它们的‘学习成本’。”

这是一个极其深刻的洞察。

- Rust 的借用检查器：以前是新手的噩梦，现在 LLM 可以很好地处理生命周期标注。
- Go 的样板代码：if err != nil 虽然繁琐，但 Copilot/Cursor/Claude Code等 可以一键生成。

当“编写代码”不再是瓶颈时，“运行时性能”和“稳定性”的权重就被无限放大了。这进一步削弱了 Python 在后端基础设施层的竞争力。

### Rust 还是 Go？

既然要高性能，为什么不直接上 Rust？

评论区对此展开了激辩。虽然 Rust 在理论上拥有比 Go 更高的性能上限和内存安全性（无 GC），但 Go 在“开发效率”与“运行效率”之间找到了完美的平衡点。

- Rust: 适合构建数据库、搜索引擎内核等对延迟极其敏感且逻辑复杂的底层组件。但 Rust 的“认知负担”依然较重，且编译速度较慢。
- Go: 提供了 80% 的 Rust 性能，但只有 20% 的开发难度。对于网关、代理这类中间件，Go 的标准库（特别是 net/http）极其成熟，编译速度极快，且自带 GC 能让开发者从内存管理的细节中解脱出来，专注于业务逻辑（如限流、计费）。

对于大多数 AI 网关场景，Go 是性价比最高的选择。

### Python 的归宿：模型与胶水

这是否意味着 Python 将被淘汰？绝不。

社区共识非常明确：Python 的护城河在于 ML 生态。

- 模型训练与微调：PyTorch/JAX 无可替代。
- 数据科学与探索：Jupyter Notebook 是数据科学家的后花园。
- 快速原型开发：在验证想法阶段，Python 依然是最快的。

但在生产环境部署（Production Serving）阶段，架构正在发生分离：

- 控制平面（Control Plane）：由 Go/Rust 接管，负责流量调度、鉴权、日志、监控。
- 数据平面（Data Plane）：核心推理引擎（如 vLLM）虽然内部可能有 C++/CUDA 优化，但外层接口仍常由 Python 封装。

## Go 在 AI 领域的未来展望

Bifrost 的案例只是冰山一角。我们正在目睹 Go 语言在 AI 领域的“新基建”运动。

### 静态二进制文件的魅力

Deployment simplicity 是作者提到的另一个关键点。

部署 Python 应用通常意味着：配置 Docker -> 安装 Python -> pip install requirements.txt -> 解决依赖冲突 -> 虚拟环境管理。

而部署 Go 应用：COPY bifrost /usr/local/bin/ -> Run。

在容器化和 K8s 盛行的今天，Go 的静态链接二进制文件极大地简化了 CI/CD 流程，减小了镜像体积，提升了冷启动速度（这对于 Serverless AI 推理尤为重要）。

### AI 专有工具链的完善

虽然 Go 在 Tensor 操作库上不如 Python 丰富，但在应用层工具上正在迅速补齐。

- LangChainGo: 社区正在移植 LangChain 的核心能力。
- Vector Database Clients: Milvus, Weaviate, Pinecone 等向量数据库都有优秀的 Go SDK。
- 主流大模型 GenAI SDK: 像Google等主流大模型厂商官方对 Go 的支持力度都很大，Gemini、Claude、OpenAI 等模型的 Go SDK 体验都还不错。

### 架构师的决策建议

如果你正在构建一个 AI 应用平台：

- 不要用 Python 写网关：不要让 GIL 成为你高并发路上的绊脚石。
- 不要用 Go 写模型训练：不要试图挑战 PyTorch 的地位，那是徒劳的。
- 采用“三明治架构”：
- 上层：Go 处理高并发 HTTP 请求、WebSocket、SSE。
- 中层：Go 处理业务逻辑、数据库交互、Redis 缓存。
- 底层：Python/C++ 容器专门负责模型推理，通过 gRPC 与 Go 层通信。


## 小结

Bifrost 从 Python 到 Go 的迁移，不仅仅是一次代码重写，更是一次架构理念的升级。它证明了在 AI 浪潮中，基础设施的性能与模型的智能同等重要。

随着 LLM 应用规模的爆发式增长，计算成本和响应延迟将成为企业关注的焦点。Go 语言凭借其高效的并发模型、极低的资源占用和极简的部署体验，正在成为 AI 基础设施层的“事实标准”。

对于 Gopher 而言，这是一个最好的时代。我们不需要成为算法专家，只需要发挥 Go 语言最擅长的能力——构建高性能、高可靠的管道，就能在 AI 时代占据不可或缺的一席之地。

资料链接：https://www.reddit.com/r/golang/comments/1r27pqx/why_we_chose_go_over_python_for_building_an_llm/

**你认为 Python 会被“边缘化”吗？**

随着 Agentic Coding 的普及，高性能语言的入门门槛正在消失。在你的 AI 实践中，是否也感受到了 Python 在生产部署时的无奈？你认为 Go 在 AI 领域还会攻下哪些阵地？

欢迎在评论区分享你的看法！

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


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


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论