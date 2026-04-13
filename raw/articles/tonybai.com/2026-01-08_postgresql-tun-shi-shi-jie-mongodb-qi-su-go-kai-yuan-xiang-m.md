---
title: PostgreSQL 吞噬世界，MongoDB 起诉 Go 开源项目：2025 数据库年度盘点
url: https://tonybai.com/2026/01/08/databases-in-2025-a-year-in-review/
published: '2026-01-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# PostgreSQL 吞噬世界，MongoDB 起诉 Go 开源项目：2025 数据库年度盘点

![](../../assets/c95f86a1b405dfb2.png)


[本文永久链接](https://tonybai.com/2026/01/08/databases-in-2025-a-year-in-review) – https://tonybai.com/2026/01/08/databases-in-2025-a-year-in-review

大家好，我是Tony Bai。

数据库领域的“毒舌”，CMU教授 Andy Pavlo 再次发布了他的[年度回顾](https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html)（虽然这次是站在 2026 年初的回望）。2025 年对于数据基础设施是疯狂的一年：PostgreSQL 继续确立其霸主地位，引发了巨头间的收购狂潮；AI Agent 通过 MCP 协议正式接管数据库交互；而 Go 社区熟知的 FerretDB 则陷入了与 MongoDB 的法律泥潭。本文将为你深度梳理这份报告背后的技术趋势与行业信号。

![img{512x368}](../../assets/980cf328c1adaf29.png)


## PostgreSQL 的统治：云巨头的“军备竞赛”

如果说 2021 年 Andy Pavlo 首次提出“PostgreSQL 正在吞噬数据库世界”，那么 2025 年则是这一预言的**终极验证**。PostgreSQL 不再仅仅是一个选项，它已经成为了行业标准，引发了云巨头之间近乎疯狂的并购与研发竞赛。

### 核心事件与技术演进

：终于引入了[PostgreSQL v18 发布](https://www.postgresql.org/about/news/postgresql-18-released-3142/)**异步 I/O (Asynchronous I/O)**存储子系统，这意味着 Postgres 终于开始摆脱对操作系统页缓存（OS Page Cache）的依赖，向现代化 DBMS 架构迈出了关键一步。此外还增加了对 Skip Scans 的支持。**天价收购案**：**Databricks 以 10 亿美元收购 Neon**：Neon 是著名的“Serverless Postgres”开创者，其存算分离架构是现代云数据库的标杆。**Snowflake 以 2.5 亿美元收购 CrunchyData**：为了不甘人后，Snowflake 也迅速补齐了其 Postgres 拼图。**Microsoft 发布 HorizonDB**：作为回应，微软推出了自己的下一代 Postgres DBaaS。


对于后端和 Go 开发者而言，这意味着 **PostgreSQL 协议已成为事实上的“通用语”**。无论底层是 Aurora、AlloyDB 还是 Neon，应用层都只需通过标准的 pgx 或 lib/pq 驱动进行连接。掌握 Postgres 的深层特性和优化技巧，将成为未来五年内最具价值的技能之一。

## MCP：AI Agent 时代的“中间件革命”

2025 年被定义为**所有 DBMS 都支持 MCP (Model Context Protocol)** 的一年。

### 什么是 MCP？

MCP 是由 Anthropic 提出，并随后被 OpenAI 采纳的一种标准化客户端-服务器 JSON-RPC 接口。它允许大语言模型（LLM）与外部工具和数据源进行交互，而无需编写定制的胶水代码。

**角色定位**：MCP 服务器充当了数据库前的**中间件**。它向 LLM 暴露工具、数据和动作列表。**工作流**：LLM (MCP Client) -> MCP Server -> Database Query (SQL)。

Andy Pavlo 指出，除了官方实现外，还有数百个第三方的 MCP Server 实现。这对于 Go 开发者是一个巨大的机会：**编写高性能、并发安全的 MCP 中间件是 Go 的拿手好戏**。

然而，这也带来了安全隐患。Pavlo 警告说，简单的代理只是将 MCP 请求翻译成 SQL，如果没有深度的内省和防护机制，AI Agent 可能会像“在应用里点了 18,000 杯水”一样，意外地摧毁数据库（比如 DROP DATABASE）。企业级 DBMS 开始内置 AI 防火墙，而开源生态则需要更多像 **DBHub** 这样提供查询限制和超时保护的中间件。

## 开源与法律：MongoDB v. FerretDB

这是 Go 社区最需要关注的法律纠纷。**FerretDB** 是一个用 Go 编写的开源项目，它提供了一个 MongoDB 兼容的代理层，后端使用 PostgreSQL 存储数据。这让用户可以用 Mongo 的驱动操作 Postgres。

### 诉讼焦点

**起因**：MongoDB Inc. 向 FerretDB 发出停止侵权函，并在 2025 年 5 月正式提起联邦诉讼。**指控**：侵犯专利、版权、商标，以及违反 MongoDB 的文档和线协议规范的许可。MongoDB 特别针对 FerretDB 声称自己是“Drop-in replacement”（直接替换）这一点，认为其不仅误导开发者，还损害了 MongoDB 的声誉。**背景**：微软也将其 MongoDB 兼容的 DocumentDB 捐赠给了 Linux 基金会，但这似乎没有引发同样的法律反击，可能是因为巨头间的相互制衡。

### 警示

这一案件可能会成为 API 兼容性实现的法律判例。对于那些致力于编写“兼容层”或“协议转换器”的 Go 开发者来说，这是一个危险的信号：**模仿专有软件的 API 和线协议，可能会面临越来越大的法律风险。**

## 文件格式战争：Parquet 的挑战者们

在数据工程领域，[Parquet 格式](https://tonybai.com/2023/07/31/a-guide-of-using-apache-arrow-for-gopher-part6)已经统治了近 15 年。但在 2025 年，为了适应现代硬件（NVMe SSD, GPU）和 AI 负载，新的挑战者涌现。

**挑战者联盟**：**SpiralDB 的 Vortex**（已捐赠给 Linux 基金会）、CWI 的 FastLanes、以及学术界的 F3 和 AnyBlox。**核心痛点**：现有的 Parquet 生态过于碎片化。Pavlo 的团队分析发现，94% 的 Parquet 文件仍在使用 2013 年的 v1 特性。**未来趋势**：**F3 格式**（由 CMU, 清华大学等合作）提出了一种有趣的思路——在文件中嵌入**WASM (WebAssembly)**解码器。这意味着只要读取端支持 WASM，就可以解析任何自定义编码的数据，无需升级读取器本身。

## 行业大洗牌：并购与消亡

**IBM 的野心**：收购了**DataStax**($3B) 和**Confluent**(Kafka 商业化公司)，试图在数据流和 NoSQL 领域占据高地。**向量数据库的退潮**：随着所有主流 DBMS（Postgres, Oracle, Mongo）都内置了向量索引，单纯的“向量数据库”公司生存空间被挤压。**Pinecone**正在寻求被收购，而**MyScaleDB**已经关闭。**GPU 数据库的黄昏**：**Voltron Data**的倒闭和**HeavyDB**被 Nvidia 收购，似乎宣告了通用 GPU 数据库作为独立商业模式的终结。

## 总结与展望

Andy Pavlo 的这篇回顾虽然笔调幽默甚至带有讽刺，但其揭示的技术趋势却是严肃的：

**架构趋同**：存算分离、基于日志的架构（Log-based architecture）已成为云数据库的标配。**AI 融合**：数据库不再只是被动存储，而是通过 MCP 和内置向量能力，主动融入 AI Agent 的工作流。**Go 的角色**：在基础设施层（Docker/K8s 之后），Go 正在成为连接 AI 与数据的**关键胶水语言**（MCP Server, Proxy, 协议转换器）。

对于 Gopher 来说，关注 PostgreSQL 的协议生态、学习构建安全的 MCP 服务、并警惕开源协议的法律边界，将是 2025 年（及以后）的重要课题。

资料链接 – [Databases in 2025: A Year in Review by Andy Pavlo](https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html)

**你的数据库“军火库”**

数据库的世界正在发生剧变。在你的项目中，PostgreSQL 是否已经成为了默认选择？你如何看待 AI Agent 直接操作数据库的未来？

欢迎在评论区分享你的选型思考或对 FerretDB 事件的看法！让我们一起看清趋势，少走弯路。

如果这篇文章为你打开了数据库领域的新视野，别忘了点个【赞】和【在看】，并转发给你的架构师朋友！

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