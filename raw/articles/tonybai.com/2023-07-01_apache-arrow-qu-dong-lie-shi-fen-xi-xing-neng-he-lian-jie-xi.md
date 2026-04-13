---
title: Apache Arrow：驱动列式分析性能和连接性的提升[译]
url: https://tonybai.com/2023/07/01/arrow-columnar-analytics/
published: '2023-07-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Apache Arrow：驱动列式分析性能和连接性的提升[译]

![](../../assets/1598149cb0a0e55f.png)


[本文永久链接](https://tonybai.com/2023/07/01/arrow-columnar-analytics) – https://tonybai.com/2023/07/01/arrow-columnar-analytics

本文翻译自[Voltron Data公司](https://voltrondata.com)CTO [Wes McKinney](https://wesmckinney.com/)的文章[《Apache Arrow: Driving Columnar Analytics Performance and Connectivity》](https://voltrondata.com/resources/arrow-columnar-analytics)。这篇文章回顾了现代大数据分析遇到的问题、[Arrow项目](https://tonybai.com/tag/arrow)的起源、生态发展以及对未来的展望。

以下是正文部分。

## 引言

自MapReduce以来，大数据已经走了很长一段路。[Jeffrey Dean和Sanjay Ghemawat](http://static.googleusercontent.com/media/research.google.com/es/us/archive/mapreduce-osdi04.pdf)在2004年发表于Google的论文催生了Apache Hadoop开源项目，以及一系列其他新项目，这些项目是因大量开发人员有捕获，存储和处理非常大的数据集的需求而创建的。

![](../../assets/0654f2443c1e6e24.png)



虽然像Hadoop这样的第一个MapReduce框架能够处理大型数据集，但它们是为了大规模弹性（通过将每个处理步骤的结果写回分布式存储）而设计的，而并未过多考虑性能。Apache Spark于2010年首次发布，因其基于容错分布式内存处理的新架构而脱颖而出。Spark的核心是用Scala实现的，Scala是Java虚拟机（JVM）的编程语言。Spark为其他编程语言提供了binding实现，例如 C# .NET、Java、Python （PySpark） 和 R（SparkR 和 sparklyr），这有助于Spark在众多编程语言开发者社区的普及使用。

![](../../assets/c44b28f1afb26dfa.png)



在过去的十年中，像Python和R这样的解释式编程语言已经不再局限于其在科学计算和学术统计中的利基市场，一跃发展成为现代数据科学，商业分析和AI的主流工具。这些编程语言完全主导了“笔记本电脑规模”的数据处理工作。像Hadoop和Spark这样的大规模数据处理框架为Python等解释型语言提供了编程接口，但与JVM上运行的“本机”接口相比，使用这些语言绑定的性能和资源利用率通常都很差。

解释型语言在使用主流大数据系统时所付出的性能损失主要源于数据互操作性问题。为了将数据从Java应用程序的核心运行时传递给用户的自定义Python函数（“用户定义函数”或“UDF”），必须将数据转换为可以Python所接受的格式，然后再转换为内置的Python对象，如列表、字典或基于数组的对象，如pandas DataFrames。更糟糕的是，许多框架，包括Spark和Hadoop，最初只为用户定义函数提供“一次一值”的执行模型，其中NumPy或pandas等工具则提供了“一次一数组”的执行模型，以避免Python解释器的开销。数据转换和解释器的双重昂贵开销使得Python基于大数据框架进行大规模数据处理变得愈加不现实。

Apache Spark通过引入Spark DataFrames来改善与Python的一些语言互操作性问题，Spark DataFrames是Spark SQL的一种新的类似pandas的API，它无需在Spark运行时和Python之间传输数据。不幸的是，任何需要使用Python的数据科学或机器学习库的应用程序都不走运。这给数据科学家和数据工程师带来了一个艰难的选择：用Python更快地开发，以换取更慢、更昂贵的工作负载，或者用Scala或Java重写关键工作负载。

## Apache Arrow项目的起源

Apache Arrow的起源故事有点像微积分的创建：各自独立的开源开发人员团体在2010年代中期的同一时间都有过“尤里卡时刻”(译注：据说阿基米德洗澡时福至心灵，想出了如何测量皇冠体积的方法，因而惊喜地叫出了一声：“Eureka！”)。

2014年底，[我加入了Cloudera](https://www.cloudera.com/about/news-and-blogs/press-releases/2014-09-30-cloudera-acquires-datapad-technology-assets-and-team-to-strength.html)，开始与分别由Marcel Kornacker和Todd Lipcon领导的Apache Impala和Apache Kudu团队密切合作。我们对在大规模分布式存储和数据处理引擎之上为Python程序员（特别是pandas用户）构建直观和快速的开发人员体验上有一致的兴趣。当时的一个突出的问题是缺乏标准化的、高速的面向列的“数据协议”，以便在引擎和编程语言之间高效地传输数据。我们不想为我们的这个事情创建自定义数据格式，也不想使用像Google的Protocol Buffers或Apache Thrift这样的数据序列化技术，因为这些技术引入了过多的计算开销。我们开始设计一种新的列式数据格式，但我们知道，如果它是一个主要由Cloudera领导的项目，那么在大数据开源项目的高度政治化氛围中，它可能会有失败的风险。

与此同时，Julien Le Dem和Jacques Nadeau，分别是Apache Parquet文件格式和Apache Drill查询引擎的共同创建者，他们正在探索一种方法，将Drill用于查询执行的内存列格式转变为独立的开源项目。这种数据格式被用作[Dremio](https://www.dremio.com/)的基础，Dremio是一个基于SQL的开源数据湖引擎，使用它可以使得云中不同存储和数据处理系统之间更快，更高效的进行连接。

值得庆幸的是，Julien、Marcel和Todd在几年前就已经合作设计了Parquet文件格式，所以我们取得了联系并决定共同解决问题，而不是启动单独的、几乎肯定不会兼容的项目。我们举行了一系列快速的面对面会议（现在来看，在2022年那几乎是不可想象的！），我们开始招募其他开源大数据领导者加入我们创建一个新项目，包括 Julian Hyde（Apache Calcite）、Reynold Xin （Apache Spark）、Michael Stack （Apache HBase）等等。

2016年，在[将Apache Arrow作为Apache软件基金会的顶级项目推出后](https://blogs.apache.org/foundation/entry/the_apache_software_foundation_announces87)，我们一直致力于使Arrow成为需要快速移动和处理数据的数据分析系统的首选项目。从那时起，该项目已成为高效的内存中列式分析和低开销数据传输的事实标准，它支持10多种编程语言。除了提供内存数据格式和互操作性协议外，我们还创建了一个功能全面的模块化计算库工具箱，[为下一代分析计算系统打下坚实的基础](https://www.youtube.com/watch?v=wdmf1msbtVs)。

在启动Arrow项目仅一年后，[与Two Sigma的我的新同事以及IBM的合作者的合作](https://databricks.com/blog/2017/10/30/introducing-vectorized-udfs-for-pyspark.html)，让我们能够加速PySpark与Arrow的使用，在某些情况下实现了10-100倍的性能提升，并显著改善了将Python和pandas与Apache Spark一起使用的体验。看到我们对更快、更具互操作性的未来的愿景开始逐步实现，这真是令人兴奋。

2018年，我与RStudio和Two Sigma合作[成立了Ursa Labs](https://wesmckinney.com/blog/announcing-ursalabs/)，作为一个非营利性行业联盟，其使命是使Arrow成为下一代数据科学工具的强大计算基础。我参与Arrow的工作，除了解决数据互操作性问题外，还旨在解决现代硬件上的内存管理和内存计算效率问题。我們很幸运地获得了NVIDIA、Intel、G-Research、Bloomberg、ODSC和OneSixtyTwo Technologies的额外赞助。

经过4年多的Apache Arrow开发，我们清楚地认识到，要促使Arrow下一阶段的增长和对企业的影响，仅通过行业赞助还不够，还需要获得更大的资本投资才行。于是在2020年底，我们决定将Ursa Labs团队从RStudio（为Ursa Labs提供了大部分资金和运营支持）中剥离出来，组建一家营利性公司[Ursa Computing](https://ursalabs.org/blog/ursa-computing/)，并在2020年底筹集了一轮风险投资。不久之后，在2021年初，我们有机会与Arrow上的GPU分析、BlazingSQL和RAPIDS领导层的创新者联手，组建了一家统一的Arrow原生(Arrow-native)计算公司[Voltron Data](https://voltrondata.com/resources/joining-forces-for-an-arrow-native-future/)。Ursa Labs已成为[Voltron Data Labs](http://voltrondata.com/labs/)，Voltron Data内部的一个团队，其持续的使命是发展和支持Arrow生态系统，同时维护Apache Way的开放和透明的治理模型。

## Apache Arrow项目的增长

如今，Arrow开发人员社区已发展到700多人，其中67人拥有提交权限。我们以创建跨语言开放标准和构建模块化软件组件为动力，以降低系统复杂性，同时提高性能和效率。我们一直在考虑将该项目视为一个软件开发工具包，旨在使开发人员能够释放Apache Arrow内存格式的好处，并解决随之而来的一阶和二阶问题（例如从云存储中读取Parquet文件，然后进行一些内存分析处理）。如果没有一个可信的、“自带电池”的软件堆栈来构建支持Arrow的计算应用程序来配合它，Arrow的列式格式本质上只能作为一种替代文件格式。

最近，在将Arrow列式格式和协议稳定用于生产用途后，社区一直专注于提供快速的Arrow原生计算组件。这项工作在C++和Rust社区中最为活跃。使用这些语言的查询引擎项目（DataFusion for Rust 和尚未命名的C++子项目），您可以轻松地将嵌入式Arrow原生列式数据处理特性添加到您的应用程序中。这可能包括您可能使用SQL或数据帧(dataframe)库（如 pandas 或 dplyr）表示的工作负载。新的高性能数据帧库（如[Polars](https://github.com/pola-rs/polars)）从一开始就被构建为Arrow原生。在Voltron Data，我们正在积极努力使这些功能无缝地提供给Python和R程序员。

让这些项目采用Arrow数据互操作性协议的一个令人信服的理由是，与任何其他使用Arrow的项目可以实现简单快速的连接。早期采用者出于信任并收获了巨大的回报。现在，任何可以读写Arrow的项目都可以通过一个快速路径连接到数据帧库（如 pandas 和 R）和许多机器学习系统（[PyTorch](https://github.com/facebookresearch/torcharrow)、[TensorFlow](https://www.tensorflow.org/io/api_docs/python/tfio/arrow)、[Hugging Face](https://huggingface.co/docs/datasets/package_reference/table_classes.html)）。

Arrow的贡献者通过与其他开源项目的密切合作，扩展了项目的能力。最近，与[DuckDB实验室](https://duckdblabs.com/)合作，使用[DuckDB](https://duckdb.org/)作为嵌入式执行引擎实现了无缝查询。R或Python现在能够使用DuckDB无缝查询其Arrow数据，可以使用类似数据帧的API（如dplyr）或SQL。此集成是经由Arrow的[C数据接口](https://arrow.apache.org/docs/format/CDataInterface.html)实现的。

使数据服务和分布式系统更容易使用Arrow的二进制格式是推动Arrow被更广泛接纳的一个重要工作。由于将Arrow协议与一些通用数据服务框架（如 gRPC 或 Apache Thrift）联合最佳使用需要一些中间件代码，因此社区开发了[Flight](https://arrow.apache.org/docs/format/Flight.html)，这是一个用于Arrow原生数据服务的开发者框架和客户端-服务器协议。Flight提供了用于实现服务器和客户端逻辑的高级库，同时使用行业标准[gRPC库](https://grpc.io/)进行内部通信。通过在客户端和服务器中使用通用内存格式来消除不必要的数据序列化，用户可以实现以前在独立于语言的协议中无法想象的数据吞吐级别（在某些情况下每秒几千兆字节）。Flight库现在在许多Arrow语言库（C++、Python、R、Java、Rust、Go）中可用，未来肯定会添加更多语言。

![](../../assets/a38e7dee25ce1eef.png)


数据库是最普遍使用的数据服务之一，ODBC和JDBC等标准数据库接口根本上是为实现互操作性和兼容性而设计，而不是为了速度。因此，Flight带来了两全其美的可能性：互操作性而又不影响性能。但是，作为开发者框架和协议的Flight没有任何关于SQL数据库工作方式的内置概念，包括用户会话、执行查询的生命周期或预处理语句等内容。还有一个风险是，每个数据库系统实现其Flight服务器的方式略有不同，因此用户必须使用不同的Flight客户端来访问每种数据库。为了解决这些问题，包括SQL数据库的客户端/服务器标准化以及与ODBC和JDBC相似的高级功能，Arrow创建了一个称为[Flight SQL](https://www.dremio.com/subsurface/arrow-flight-sql-a-universal-jdbc-driver/)的Flight应用程序扩展。现在，数据库开发人员可以实现一个通用的Flight SQL服务器，用户将能够使用标准的Flight SQL客户端访问任何启用Flight SQL的数据库。

![](../../assets/eb2ea1fa1500d358.png)



## Apache Arrow生态系统的发展和采用

Arrow项目及其生态系统的发展得益于其早期采纳者的成功。总的来说，Arrow已经成为Python用户与以Parquet等文件格式存储的数据集进行交互的标准工具。如上所述，在项目早期，我们与Spark社区合作，使用Arrow更快地将数据传输到pandas来加速PySpark。在这些早期成功案例之后，许多其他项目都采用了Arrow来实现更快的互操作性和内存处理，并删除了以前的定制解决方案。

通过采用Arrow进行数据传输，Streamlit能够删除自定义代码，同时大幅提高应用程序性能。Streamlit的传统序列化框架基于Protocol Buffers，用于将表格数据从Python后端发送到JavaScript前端。通过将自定义序列化程序替换为Arrow，Streamlit的性能提高了15倍，并且能够通过使用现成的解决方案来简化其代码库。

![](../../assets/055bbb6f36965dc2.png)



Dremio是从头开始就以Apache Arrow为核心构建的系统。Dremio由Jacques Nadeau共同创立，是一个用于数据湖的分布式查询引擎。Dremio开发了一种基于LLVM的即时表达式编译器，称为[Gandiva](https://github.com/dremio/gandiva)（现在是Arrow项目的一部分），它可以针对Arrow列式内存的操作生成高效的机器代码。与在JVM中执行的解释表达式相比，这可实现更快的性能。

最近，Databricks发布了[Cloud Fetch connector](https://databricks.com/blog/2021/08/11/how-we-achieved-high-bandwidth-connectivity-with-bi-tools.html)，用于将商业智能工具（如Tableau或Power BI）与存储在云中的数据连接起来。过去，从传统数据仓库检索数据的速度受到了在单个线程上从单个SQL端点提取数据的速度的限制。这限制了交互式数据探索工具的有用性。Cloud Fetch 使用Arrow wire协议从云存储并行流式传输数据，与传统方法相比，性能提高了12倍。

这些只是使用Arrow项目的某些部分来加速数据移动或在内存中处理数据的项目的几个示例。随着越来越多的项目启用Arrow，用户将获得复合效率的优势。例如，在Snowflake实现以Arrow格式从其系统中检索数据后，[他们的Python和JDBC客户端的数据检索速度提高了5倍](https://www.snowflake.com/blog/fetching-query-results-from-snowflake-just-got-a-lot-faster-with-apache-arrow/)。这不仅使Snowflake查询运行得更快，而且使得与Snowflake集成的产品运行得更快。例如，人工智能驱动的分析平台Tellius能够使用Arrow[将他们与Snowflake的集成速度提高3倍](https://www.tellius.com/lightning-fast-data-transfer-between-tellius-and-snowflake-powered-by-apache-arrow/)，相比于之前的实现。

## 社区

Apache Arrow的受欢迎程度正在不断增长。事实上，Arrow的Python库PyArrow在2022年1月的下载量为4600w次，这一数字比2021年10月份创造的之前的记录增加了近800w次。我们预计，随着越来越多的项目采用Arrow作为依赖项，这一趋势将继续下去。

![](../../assets/34639ed5d6c0e86b.png)



Arrow为数据传输、对二进制文件（如 Parquet）的高速访问以及快速发展的计算引擎提供了坚实的基础。这需要多年的工作和一个庞大的社区才能实现。在过去的6年里，Arrow开发者社区得到了相当大的发展：自2016年首次发布以来，已[有676名独立的开发人员](https://github.com/apache/arrow)为该项目做出了贡献，其中105名贡献者参与了Arrow 7.0.0版本的开发。

与Apache软件基金会中的所有项目一样，我们遵循Apache Way，这是一个开放透明的开源项目治理框架。项目讨论和决策必须在公开场合进行，例如在邮件列表或GitHub上。贡献者以个人身份参与，而不是作为他们工作的公司的代表。通过公开开展所有项目业务，我们可以保持包容和专业的氛围，欢迎来自世界各地的贡献者的不同观点。Apache Way重视多种贡献：回答用户问题、分类错误报告和编写文档与提出拉取请求一样重要。Arrow项目主要的开发人员邮件列表是dev@arrow.apache.org。

在项目中持续工作一段时间后，贡献者可以通过项目管理委员会（PMC）的投票被提升为“提交者”（对项目git存储库具有写入权限）。表现出致力于发展和指导项目社区的提交者以后可能会被提升加入PMC。PMC成员是项目指导委员会，对项目中的发布和其他重大决策具有约束力的投票权。目前Arrow项目有67个提交者和38个PMC 成员。

## 未来

随着Arrow开发者社区的发展，项目范围也在扩大。该项目始于六年前，旨在设计一个独立于语言的标准来表示面向列的数据，以及一个二进制协议，用于在应用程序之间移动数据。从那时起，该项目稳步发展，提供了一个自带电池的开发工具箱，以简化构建涉及处理大型数据集的高性能分析应用程序。我们预计Arrow将成为下一代大数据系统的关键组成部分。

我们期望开放标准和接口方面的工作能够继续团结和简化分析计算生态系统。我们参与了[Substrait](https://github.com/substrait-io/substrait)，这是一个新的开源框架，提供标准化的中间查询语言（低于SQL级别），将前端用户界面（如SQL或data frame库）与后端分析计算引擎连接起来。Substrait由Arrow项目联合创始人Jacques Nadeau创立，并且发展迅速。我们认为，有了这个新项目提供的执行引擎支持，编程语言接口与分析性计算将更容易发展。

## 加入我们！

发展Apache Arrow项目是我们Voltron Data使命的重要组成部分！我们期待继续与社区合作，推动生态系统向前发展。您可以订阅我们的新闻通讯以随时了解情况，并考虑在Twitter上关注我们[@voltrondata](http://twitter.com/VoltronData)以获取更多新闻。您还可以探索[Voltron Data Enterprise Support](https://voltrondata.com/subscription/)订阅选项，这个订阅列表旨在帮助在Apache Arrow生态系统中工作的开发人员和公司。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论