---
title: 为什么 VictoriaMetrics 正在替换 Prometheus？一次大规模可观测性迁移实录
url: https://tonybai.com/2025/07/26/migrate-from-prometheus-to-victoriametrics/
published: '2025-07-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为什么 VictoriaMetrics 正在替换 Prometheus？一次大规模可观测性迁移实录

![](../../assets/cc9c66cac2184b73.png)


[本文永久链接](https://tonybai.com/2025/07/26/migrate-from-prometheus-to-victoriametrics) – https://tonybai.com/2025/07/26/migrate-from-prometheus-to-victoriametrics

大家好，我是Tony Bai。

在云原生可观测性的领域，Prometheus 无疑是王者。凭借其简洁的模型、强大的 PromQL 和活跃的社区，Prometheus 几乎定义了现代监控的行业标准。许多顶尖技术公司，包括 PingCAP，都将其作为核心产品的监控与告警解决方案。

然而，Prometheus 的架构缺陷使其在大规模监控中显得力不从心。我们经常看到像 Pinterest 这样的大型企业面临的真实挑战。当一个 TiDB 集群规模达到 **700+ 节点**，每秒处理 **700K+ QPS** 时，曾经可靠的“王者”开始露出疲态。用于故障诊断的核心工具 TiDB Clinic 在回放和分析这些大规模集群的指标时，Prometheus 开始频繁崩溃。

这迫使整个行业直面一个残酷的现实：在极限规模下，Prometheus 不再是最佳选择。最近，[PingCAP 官方发布的一篇博文](https://www.pingcap.com/blog/tidb-observability-migrating-prometheus-victoriametrics/) 详细记录了他们如何应对这一挑战，并最终选择用 VictoriaMetrics 完成“换心手术”的全过程。

## 压垮 Prometheus 的“五宗罪”

为了支持 Pinterest 这样的大客户，pingcap工程团队为 Prometheus 分配了“怪兽级”的硬件资源：一台拥有 **96 核心 CPU 和 768GB RAM** 的 i4i.24xlarge 实例。许多人曾天真地以为，只要资源给够，一切问题都能解决。

但事实并非如此。在高基数、高吞吐量的指标冲击下，Prometheus 暴露出了几个致命的、与资源无关的瓶颈：

-
Out of Memory (OOM) 崩溃


在执行大型、复杂的查询时，尤其是时间跨度较长时，Prometheus 的内存消耗会急剧飙升，最终被系统 OOM Killer 无情终结。 -
漫长的恢复时间


OOM 之后，Prometheus 需要通过重放 WAL (Write-Ahead Log) 来恢复数据。对于海量数据，这个过程动辄需要**40 分钟以上**，有时甚至会因为各种原因彻底失败。 -
“死亡循环”


最令人绝望的是，WAL 重放过程本身就是一个高资源消耗的操作，它很可能**再次触发 OOM**。文章中提到，工程团队遇到过 Prometheus 在崩溃和重启的“死亡循环”中挣扎，迟迟无法恢复服务的情况。 -
查询性能瓶颈


为了避免 OOM，工程师们不得不将排查问题的查询时间范围，严格限制在**15 分钟以内**。一旦超过这个窗口，查询就会变得极慢或直接失败。这对于需要进行历史数据分析的故障根因定位，是致命的。 -
高昂的 TCO (总拥有成本)


为它配置了顶级的硬件，却换来了不稳定的服务和受限的查询能力。这笔投入的性价比，显然是极低的。

这一系列的“血泪教训”让我们明白，问题的根源不在于资源不足，而在于 Prometheus 的架构设计，在面对超大规模场景时，已经触及其能力的“天花板”。

## 救世主登场：VictoriaMetrics 的崛起

带着这些痛点，工程团队开始寻找替代方案。VictoriaMetrics (VM) 进入了他们的视野，它从设计之初就为大规模、长周期监控场景而生。

值得一提的是，在云原生监控领域，VictoriaMetrics 的崛起并非偶然。曾几何时，InfluxDB 也是 Prometheus 的一个强力竞争者。然而，[自从 InfluxDB 决定用 Rust 重写其 3.0 版本核心](https://mp.weixin.qq.com/s/lNmztKNmlWT-D9aEpmurmw)后，其在 Go 社区和云原生生态中的声量和影响力似乎有所下降。与此同时，完全用 Go 编写、性能卓越且与 Prometheus 生态高度兼容的 VictoriaMetrics，则抓住了这个机会，迅速填补了市场空白，赢得了越来越多大规模用户的青睐。

经过一系列严谨的测试，PingCAP 的团队发现 VictoriaMetrics 在几个关键点上完美地解决了 Prometheus 的困境。

**1. 资源利用率大幅优化**

迁移到 VictoriaMetrics 后，奇迹发生了。在处理同样体量的指标时：

* **CPU 使用率稳定在 50% 以下。**

* **内存使用率保持在 35% 以下。**

* **OOM 崩溃彻底消失。**

VM 用更少的资源，提供了更强的稳定性。

**2. 查询能力质的飞跃**

这才是最关键的提升。过去在 Prometheus 上 15 分钟就必定失败的复杂查询，现在在 VictoriaMetrics 上可以轻松地将时间范围**扩展到数小时**。这意味着工程师在排查问题时，终于可以从“戴着镣铐跳舞”变得游刃有余。

**3. 数据为证：性能的碾压**

口说无凭，PingCAP 团队在 Pinterest 的集群上进行了直接的性能对比测试，结果不言自明：

| 指标 | 时间范围 | Prometheus 性能 | VictoriaMetrics (Tuned) 性能 |
|---|---|---|---|
| KV Request (简单查询) | 15分钟 | 失败 |
成功 (1分钟内) |
| 99% gRPC duration (复杂查询) | 30分钟 | 失败 (26秒后) |
成功 (7.4秒) |
| 99% gRPC duration (复杂查询) | 1小时 | 失败 (15秒后) |
成功 (7.4秒) |

表格清晰地显示，Prometheus 在处理稍长时间范围的查询时便迅速败下阵来，而 VictoriaMetrics 则表现得轻松自如，甚至在处理 1 小时的数据时，查询耗时也仅为个位数秒。

## 迁移实录：“零停机”三步走策略

当然，替换一个生产环境的核心监控系统，是一项高风险的“换心手术”。为了确保万无一失，PingCAP 的工程师们设计并执行了一套平滑、无感知的迁移策略：

**Step 1: 并行部署，双轨并行**

他们没有直接关闭 Prometheus，而是在旁边部署了一套 VictoriaMetrics，让它们同时从 TiDB 集群采集完全相同的数据。

**Step 2: 对比验证，建立信任**

在双轨运行阶段，工程师们持续对比两个系统的数据准确性、查询性能和资源消耗。这个阶段让他们用真实数据验证了 VM 的所有优势，并建立了切换的信心。

**Step 3: 优雅切换，最终交割**

在确认一切平稳后，他们将 Grafana 的数据源从 Prometheus 指向 VictoriaMetrics，然后从容地关闭了 Prometheus 服务。整个过程对用户和工程师完全透明，没有造成任何监控停机或数据丢失。

## 小结

这次从 Prometheus 到 VictoriaMetrics 的迁移，不是一次对 Prometheus 的否定。Prometheus 依然是一个极其优秀、定义了行业的伟大工具，对于 90% 的场景，它简单、可靠，是最佳选择。

但这个案例证明，**技术选型没有永恒的“银弹”，只有在特定规模和场景下的“最合适的工具”。**

当你的系统规模跨越了某个临界点，过去让你引以为傲的“简单”架构，就可能成为你继续前进的“诅咒”。勇于直面工具的边界，并基于翔实的数据和严谨的流程做出改变，这本身就是一种宝贵的工程能力。

更值得关注的是，就在近期，VictoriaMetrics 团队宣布将其另外两个关键的可观测性产品——[VictoriaLogs](https://github.com/VictoriaMetrics/VictoriaLogs) 和 [VictoriaTrace](https://github.com/VictoriaMetrics/VictoriaTraces)——作为独立的开源项目发布。这意味着 VictoriaMetrics 不再仅仅满足于成为一个 Metrics 领域的强者，它的目标是构建一个覆盖 **Metrics, Logs, Traces** 的全方位、高性能可观测性平台。

对于 TiDB 和其他面临类似挑战的大规模系统而言，VictoriaMetrics 已经被证明是一个坚实的基础。而对于整个云原生社区，一个更强大、更全面的可观测性“新王”，或许正在悄然加冕。

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


资料地址：https://www.pingcap.com/blog/tidb-observability-migrating-prometheus-victoriametrics/

商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论