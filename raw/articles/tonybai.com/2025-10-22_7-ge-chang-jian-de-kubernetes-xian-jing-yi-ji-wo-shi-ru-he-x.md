---
title: 7 个常见的 Kubernetes 陷阱（以及我是如何学会避免它们的）
url: https://tonybai.com/2025/10/22/seven-kubernetes-pitfalls/
published: '2025-10-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 7 个常见的 Kubernetes 陷阱（以及我是如何学会避免它们的）

![](../../assets/a7643bd8aa7d0807.png)


[本文永久链接](https://tonybai.com/2025/10/22/seven-kubernetes-pitfalls) – https://tonybai.com/2025/10/22/seven-kubernetes-pitfalls

大家好，我是Tony Bai。

本文翻译自Kubernetes官方博客《[7 Common Kubernetes Pitfalls (and How I Learned to Avoid Them)](https://kubernetes.io/blog/2025/10/20/seven-kubernetes-pitfalls-and-how-to-avoid/)》一文。

这篇文章的作者Abdelkoddous Lhajouji 以第一人称视角，系统性地梳理了从资源管理、健康检查到安全配置等多个方面，新手乃至资深工程师都极易忽视的关键点。文中的每个“陷阱”都源于真实的生产经验，其规避建议更是极具实践指导意义。无论你是 K8s 初学者还是经验丰富的 SRE，相信都能从中获得启发，审视并改善自己的日常实践。

以下是译文全文，供大家参考。

Kubernetes 有时既强大又令人沮丧，这已经不是什么秘密了。当我刚开始涉足容器编排时，我犯的错误足以整理出一整份陷阱清单。在这篇文章中，我想详细介绍我遇到（或看到别人遇到）的七个大坑，并分享一些如何避免它们的技巧。无论你是刚开始接触 Kubernetes，还是已经在管理生产集群，我都希望这些见解能帮助你避开一些额外的压力。

![](../../assets/e7aa987414f58103.png)


## 忽略资源请求（requests）和限制（limits）

**陷阱**：在 Pod 规范中不指定 CPU 和内存需求。这通常是因为 Kubernetes 并不强制要求这些字段，而且工作负载通常可以在没有它们的情况下启动和运行——这使得在早期配置或快速部署周期中很容易忽略这个疏漏。

**背景**：在 Kubernetes 中，资源请求和限制对于高效的集群管理至关重要。资源请求确保调度器为每个 Pod 预留适当数量的 CPU 和内存，保证其拥有运行所需的必要资源。资源限制则为 Pod 可以使用的 CPU 和内存设置了上限，防止任何单个 Pod 消耗过多资源，从而可能导致其他 Pod 资源匮乏。当未设置资源请求和限制时：

**资源匮乏**：Pod 可能会获得不足的资源，导致性能下降或失败。这是因为 Kubernetes 会根据这些请求来调度 Pod。如果没有它们，调度器可能会在单个节点上放置过多的 Pod，从而导致资源争用和性能瓶颈。**资源囤积**：相反，如果没有限制，一个 Pod 可能会消耗超过其应有份额的资源，影响同一节点上其他 Pod 的性能和稳定性。这可能导致其他 Pod 因内存不足而被驱逐或被内存溢出（OOM）杀手终止等问题。

### 如何避免

- 从适度的 requests 开始（例如 100m CPU，128Mi 内存），然后观察你的应用表现如何。
- 监控实际使用情况并优化你的设置；
[HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)可以帮助根据指标自动进行扩缩容。 - 留意 kubectl top pods 或你的日志/监控工具，以确认你没有过度或不足地配置资源。

**我的惨痛教训**：早期，我从未考虑过内存限制。在我的本地集群上，一切似乎都很好。然后，在一个更大的环境中，Pod 们接二连三地被 OOMKilled。教训惨痛。有关为你的容器配置资源请求和限制的详细说明，请参阅官方 Kubernetes 文档的[为容器和 Pod 分配内存资源](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/)。

## 低估存活探针（liveness）和就绪探针（readiness）

**陷阱**：部署容器时不明确定义 Kubernetes 应如何检查其健康或就绪状态。这往往是因为只要容器内的进程没有退出，Kubernetes 就会认为该容器处于“运行中”状态。在没有额外信号的情况下，Kubernetes 会假设工作负载正在正常运行——即使内部的应用程序没有响应、正在初始化或卡住了。

**背景**：

存活、就绪和启动探针是 Kubernetes 用来监控容器健康和可用性的机制。

**存活探针**决定应用程序是否仍然存活。如果存活检查失败，容器将被重启。**就绪探针**控制容器是否准备好为流量提供服务。在就绪探针通过之前，该容器会从 Service 的端点中移除。**启动探针**帮助区分长时间的启动过程和实际的故障。

### 如何避免

- 添加一个简单的 HTTP livenessProbe 来检查一个健康端点（例如 /healthz），以便 Kubernetes 可以重启卡住的容器。
- 使用一个 readinessProbe 来确保流量在你的应用预热完成前不会到达它。
- 保持探针简单。过于复杂的检查可能会产生误报和不必要的重启。

**我的惨痛教训**：我曾有一次忘记为一个需要一些时间来加载的 Web 服务设置就绪探针。用户过早地访问了它，遇到了奇怪的超时，而我花了几个小时挠头苦思。一个 3 行的就绪探针本可以拯救那一天。

有关为容器配置存活、就绪和启动探针的全面说明，请参阅官方 Kubernetes 文档中的[配置存活、就绪和启动探针](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)。

## “我们就看看容器日志好了”（著名遗言）

**陷阱**：仅仅依赖通过 kubectl logs 获取的容器日志。这通常是因为该命令快速方便，并且在许多设置中，日志在开发或早期故障排查期间似乎是可访问的。然而，kubectl logs 仅检索当前运行或最近终止的容器的日志，而这些日志存储在节点的本地磁盘上。一旦容器被删除、驱逐或节点重新启动，日志文件可能会被轮替掉或永久丢失。

### 如何避免

- 使用 CNCF 工具如
[Fluentd](https://kubernetes.io/docs/concepts/cluster-administration/logging/#sidecar-container-with-a-logging-agent)或[Fluent Bit](https://fluentbit.io/)来**集中化日志**，聚合所有 Pod 的输出。 **采用 OpenTelemetry**以获得日志、指标和（如果需要）追踪的统一视图。这使你能够发现基础设施事件与应用级行为之间的关联。**将日志与 Prometheus 指标配对**，以跟踪集群级别的数据以及应用程序日志。如果你需要分布式追踪，可以考虑 CNCF 项目如[Jaeger](https://www.jaegertracing.io/)。

**我的惨痛教训**：第一次因为一次快速重启而丢失 Pod 日志时，我才意识到 kubectl logs 本身是多么不可靠。从那时起，我为每个集群都设置了一个合适的管道，以避免丢失重要线索。

## 将开发和生产环境完全等同对待

**陷阱**：在开发、预发布和生产环境中使用完全相同的设置部署相同的 Kubernetes 清单（manifests）。这通常发生在团队追求一致性和重用时，但忽略了特定于环境的因素——如流量模式、资源可用性、扩缩容需求或访问控制——可能会有显著不同。如果不进行定制，为一个环境优化的配置可能会在另一个环境中导致不稳定、性能不佳或安全漏洞。

### 如何避免

- 使用overlays环境 或
[kustomize](https://kustomize.io/)来维护一个共享的基础配置，同时为每个环境定制资源请求、副本数或配置。 - 将特定于环境的配置提取到 ConfigMaps 和/或 Secrets 中。你可以使用专门的工具，如
[Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)来管理机密数据。 - 为生产环境的规模做好规划。你的开发集群可能用最少的 CPU/内存就能应付，但生产环境可能需要多得多。

**我的惨痛教训**：有一次，我为了“测试”，在一个小小的开发环境中将 replicaCount 从 2 扩展到 10。我立刻耗尽了资源，并花了半天时间清理残局。哎。

## 让旧东西到处漂浮

**陷阱**：让未使用的或过时的资源——如 Deployments、Services、ConfigMaps 或 PersistentVolumeClaims——在集群中持续运行。这通常是因为 Kubernetes 不会自动移除资源，除非得到明确指示，而且没有内置机制来跟踪所有权或过期时间。随着时间的推移，这些被遗忘的对象会累积起来，消耗集群资源，增加云成本，并造成操作上的混乱，尤其是当过时的 Services 或 LoadBalancers 仍在继续路由流量时。

### 如何避免

- 为
**所有东西打上标签**，附上用途或所有者标签。这样，你就可以轻松查询不再需要的资源。 **定期审计**你的集群：运行 kubectl get all -n来查看实际在运行什么，并确认它们都是合法的。 **采用 Kubernetes 的垃圾回收**：[K8s 文档](https://kubernetes.io/docs/concepts/workloads/controllers/garbage-collection/)展示了如何自动移除依赖对象。**利用策略自动化**：像[Kyverno](https://kyverno.io/)这样的工具可以在一定时期后自动删除或阻止过时的资源，或强制执行生命周期策略，这样你就不必记住每一个清理步骤。

**我的惨痛教训**：一次hackathon之后，我忘记拆除一个关联到外部负载均衡器的“test-svc”。三周后，我才意识到我一直在为那个负载均衡器付费。捂脸。

## 过早地深入研究网络

**陷阱**：在完全理解 Kubernetes 的原生网络原语之前，就引入了高级的网络解决方案——如服务网格（service meshes）、自定义 CNI 插件或多集群通信。这通常发生在团队使用外部工具实现流量路由、可观测性或 mTLS 等功能，而没有首先掌握核心 Kubernetes 网络的工作原理时：包括 Pod 到 Pod 的通信、ClusterIP Services、DNS 解析和基本的 ingress 流量处理。结果，与网络相关的问题变得更难排查，尤其是当overlays网络引入了额外的抽象和故障点时。

### 如何避免

- 从小处着手：一个 Deployment、一个 Service 和一个基本的 ingress 控制器，例如基于 NGINX 的控制器（如 Ingress-NGINX）。
- 确保你理解集群内的流量如何流动、服务发现如何工作以及 DNS 是如何配置的。
- 只有在你真正需要时，才转向功能完备的网格或高级 CNI 功能，复杂的网络会增加开销。

**我的惨痛教训**：我曾在一个小型的内部应用上尝试过 Istio，结果花在调试 Istio 本身的时间比调试实际应用还多。最终，我退后一步，移除了 Istio，一切都正常工作了。

## 对安全和 RBAC 太掉以轻心

**陷阱**：使用不安全的配置部署工作负载，例如以 root 用户身份运行容器、使用 latest 镜像标签、禁用安全上下文（security contexts），或分配过于宽泛的 RBAC 角色（如 cluster-admin）。这些做法之所以持续存在，是因为 Kubernetes 开箱即用时并不强制执行严格的安全默认设置，而且该平台的设计初衷是灵活而非固执己见。在没有明确的安全策略的情况下，集群可能会持续暴露于容器逃逸、未经授权的权限提升或因未固定的镜像导致的意外生产变更等风险中。

### 如何避免

- 使用
[RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)来定义 Kubernetes 内部的角色和权限。虽然 RBAC 是默认且最广泛支持的授权机制，但 Kubernetes 也允许使用替代的授权方。对于更高级或外部的策略需求，可以考虑像[OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)（基于 Rego）、[Kyverno](https://kyverno.io/)或使用 CEL 或[Cedar](https://cedarpolicy.com/)等策略语言的自定义 webhook 等解决方案。 - 将镜像固定到特定的版本（不要再用 :latest！）。这能帮助你确切地知道实际部署的是什么。
- 研究一下
[Pod 安全准入](https://kubernetes.io/docs/concepts/security/pod-security-admission/)（或其他解决方案，如 Kyverno），以强制执行非 root 容器、只读文件系统等。

**我的惨痛教训**：我从未遇到过重大的安全漏洞，但我听过足够多的警示故事。如果你不把事情收紧，出问题只是时间问题。

## 小结：最后的想法

Kubernetes 很神奇，但它不会读心术，如果你不告诉它你需要什么，它不会神奇地做出正确的事。通过牢记这些陷阱，你将避免大量的头痛和时间浪费。错误会发生（相信我，我犯过不少），但每一次都是一个机会，让你更深入地了解 Kubernetes 在底层是如何真正工作的。如果你有兴趣深入研究，[官方文档](https://kubernetes.io/docs/home/)和[社区 Slack](http://slack.kubernetes.io/) 是绝佳的下一步。当然，也欢迎分享你自己的恐怖故事或成功技巧，因为归根结底，我们都在这场云原生的冒险中并肩作战。

**祝你交付愉快！**

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


**想系统学习Go，构建扎实的知识体系？**

我的新书《[Go语言第一课](https://book.douban.com/subject/37499496/)》是你的首选。源自2.4万人好评的极客时间专栏，内容全面升级，同步至Go 1.24。首发期有专属五折优惠，不到40元即可入手，扫码即可拥有这本300页的Go语言入门宝典，即刻开启你的Go语言高效学习之旅！

![](https://tonybai.com/wp-content/uploads/2025/go-primer-published-4.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论