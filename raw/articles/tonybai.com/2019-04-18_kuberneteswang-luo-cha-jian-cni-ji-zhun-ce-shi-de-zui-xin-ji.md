---
title: Kubernetes网络插件（CNI）基准测试的最新结果
url: https://tonybai.com/2019/04/18/benchmark-result-of-k8s-network-plugin-cni/
published: '2019-04-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes网络插件（CNI）基准测试的最新结果

本文翻译自Alexis Ducastel的文章[《Benchmark results of Kubernetes network plugins (CNI) over 10Gbit/s network (Updated: April 2019)》](https://itnext.io/benchmark-results-of-kubernetes-network-plugins-cni-over-10gbit-s-network-updated-april-2019-4a9886efe9c4)。

本文是我[之前的基准测试](https://itnext.io/benchmark-results-of-kubernetes-network-plugins-cni-over-10gbit-s-network-36475925a560)的最新更新，这次测试在最新版[Kubernetes 1.14](https://kubernetes.io/blog/2019/03/25/kubernetes-1-14-release-announcement/)上运行，其中CNI版本在2019年4月更新。

首先，非常感谢[Cilium团队](https://cilium.io/)对我的帮助，包括协助审查测试结果以及更正我的指标监控脚本。

## 自2018年11月以来都有哪些新变化

如果你只是想知道自上次以来发生的变化，这里有一个简短的总结：

[Flannel](https://tonybai.com/2017/01/17/understanding-flannel-network-for-kubernetes/)仍然是[CNI](https://github.com/containernetworking/cni)竞赛中最快和最精简的那个选手，但它仍然不支持NetworkPolicies(网络策略)，也不支持加密。

[Romana](https://github.com/romana/cni)不再维护，因此我们决定将其从基准测试中剔除。

[WeaveNet](https://github.com/weaveworks/weave)现在同时支持[Ingress](https://tonybai.com/2018/06/21/kubernetes-ingress-controller-practice-using-four-examples/)和Egress的NetworkPolicies！但性能要略低于之前的版本。

如果您想获得最佳性能，[Calico](https://www.projectcalico.org/)仍需要手动定制MTU。Calico为安装CNI提供了两个新选项，无需专用[ETCD存储](https://tonybai.com/tag/etcd)：

- 将状态存储在Kubernetes API中作为数据存储区（集群<50个节点）
- 使用Typha代理将状态存储在Kubernetes API中，以减轻K8S API（集群> 50个节点）的压力

Calico宣布在[Istio](https://tonybai.com/2018/01/03/an-intro-of-microservices-governance-by-istio/)之上支持应用层策略(Application Layer Policy)，为应用层带来安全性。

Cilium现在支持加密！Cilium使用IPSec隧道提供加密，并为WeaveNet提供了加密网络的替代方案。但是，在启用加密的情况下，WeaveNet比Cilium更快。这是由于Cilium 1.4.2仅支持CBC加密，若使用GCM将会更好，但它将是1.5版本的Cilium的一部分。

由于嵌入了ETCD operator，因此Cilium现在更容易部署。

Cilium团队还通过降低内存消耗和CPU成本，努力减少CNI占用空间。但他们仍然比其他选手更重。

## 基准测试的上下文

基准测试是在通过Supermicro 10Gbit交换机连接的三台Supermicro裸机服务器上进行的。服务器通过DAC SFP +无源电缆直接连接到交换机，并在激活巨型帧（MTU 9000）的同一VLAN中设置。

[Kubernetes](https://tonybai.com/2018/10/17/imooc-course-kubernetes-practice-go-online/) 1.14.0在[Ubuntu](https://tonybai.com/tag/ubuntu) 18.04 LTS上运行，运行[Docker](https://tonybai.com/tag/docker) 18.09.2（此linux版本中的默认docker版本）。

为了提高可重复性，我们选择始终在第一个节点上设置master，在第二个服务器上设置基准测试的服务器部分，在第三个服务器上设置客户端部分。这是通过Kubernetes deployments中的NodeSelector实现的。

以下是我们将用于描述基准测试结果和解释的表情图：

![img{512x368}](../../assets/09eaab149a6f77a3.png)


## 为基准测试选择CNI

这个基准测试仅仅关注那些入选kubernetes正式文档：[“create a single master cluster with kubeadm”](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/)中的CNI列表。在提到的9个CNI中，我们只测试其中的6个，不包括那些我们无法轻松安装和/或不通过以下文档开箱即用的工具（Romana，Contiv-VPP和JuniperContrail / TungstenFabric）

以下是我们将要比较的CNI列表：

- Calico v3.6
- Canal v3.6（事实上，Flannel用于网络+ Calico用于防火墙）
- Cilium 1.4.2
- Flannel 0.11.0
- Kube-router 0.2.5
- WeaveNet 2.5.1

## 安装

CNI越容易设置，我们对其第一印象就越好。所有参与基准测试的CNI都很容易设置（一个或两个命令行）。

如前所述，服务器和交换机都配置了Jumbo帧激活（通过将MTU设置为9000）。我们非常感谢CNI可以自动发现要使用的MTU，具体取决于适配器。事实上，Cilium和Flannel是唯一能够正确自动检测MTU的选手。大多数其他CNI在GitHub中引发了启用MTU自动检测的问题，但是现在，我们需要通过修改Calico，Canal和Kube-router的ConfigMap或WeaveNet的ENV var来手动修复它。

也许您想知道错误的MTU会产生什么影响？这里有一个图表，显示WeaveNet与默认MTU和WeaveNet与Jumbo帧之间的区别：

![img{512x368}](../../assets/28f542bfbeda738a.png)


那么，既然我们知道MTU对性能非常重要，那么这些CNI如何自动检测MTU：

![img{512x368}](../../assets/62ff0915255c849e.png)


正如我们在上图中看到的，我们必须对Calico，Canal，Kube-router和WeaveNet应用一些MTU调整以获得最佳性能。Cilium和Flannel能够自行正确地自动检测MTU，确保开箱即用的最佳性能。

## 安全

在比较这些CNI的安全性时，我们谈论两件事：它们加密通信的能力，以及它们对Kubernetes网络策略的实现（根据实际测试，而不是来自他们的文档）。

只有两个CNI可以实现加密通信：Cilium和WeaveNet。通过将加密密码设置为CNI的ENV变量可以来启用WeaveNet加密。WeaveNet文档有点令人困惑，但这很容易做到。Cilium加密是通过创建Kubernetes Secrets和daemonSet修改的命令设置的（比WeaveNet复杂一点，但是Cilium有很棒的文档记录了它）。

在网络策略实现方面，通过实施Ingress和Egress规则，Calico，Canal，Cilium和WeaveNet是最好的控制面板。Kube-router实际上只实现了Ingress规则。

Flannel没有实现网络策略。

以下是结果摘要：

![img{512x368}](../../assets/7dd2c8e14b9b3996.png)


## 性能

该基准测试显示每次测试的三次运行（至少）的平均带宽。我们正在测试TCP和UDP性能（使用iperf3），真实应用程序，如HTTP（使用Nginx和curl），或FTP（使用vsftpd和curl），最后是使用SCP协议进行应用程序加密的行为（使用OpenSSH服务器和客户端）。

对于所有测试，我们还在裸机节点（绿色条）上运行基准测试，以比较CNI与本机网络性能的有效性。为了与我们的基准比例保持一致，我们在图表上使用以下颜色：

- 黄色=非常好
- 橙色=好
- 蓝色=一般
- 红色=差

因为我们不关注错误配置的CNI的性能，所以我们只会显示MTU调整的CNI基准测试结果。（NOTA BENE：如果激活加密，Cilium无法正确计算MTU，因此您必须在v1.4中手动将MTU降低到8900.下一版1.5将自动适应。）

结果如下：

![img{512x368}](../../assets/ec1431eb7da306e5.png)


每个CNI都在TCP基准测试中表现良好。由于加密成本，启用加密的CNI远远落后于其他CNI。

![img{512x368}](../../assets/30c6da37edd1fd22.png)


同样，在UDP基准测试中，所有CNI都表现良好。加密的CNI现在彼此非常接近。Cilium落后于其竞争对手，但事实上，它仅略高于裸机结果的2,3％，这是公平的。我们应该记住的是，Cilium和Flannel都是唯一能够正确自动检测MTU的CNI，从而提供了开箱即用的结果。

![img{512x368}](../../assets/55674d760de57265.png)


真实世界的应用程序怎么样？使用HTTP基准测试，我们可以看到全局性能略低于TCP测试。即使HTTP支持TCP，在TCP基准测试中，iperf3配置为避免任何“TCP慢启动”副作用，这可以有效地影响HTTP基准测试。这里的每个选手的表现都相当不错，Kube-router有明显的优势，WeaveNet在这项测试中表现非常糟糕，比裸机少了约20％。Cilium加密和WeaveNet加密现在都远远落后于裸机性能。

![img{512x368}](../../assets/4f5c26d9f2e4be80.png)


使用FTP，另一个TCP支持的协议，结果更加复杂。虽然Flannel和Kube-router的表现非常好，但是Calico，Canal和Cilium稍稍落后，在裸机速度下约为10％。WeaveNet与裸机性能相差甚远，差距为17>％。无论如何，WeaveNet的加密版本比Cilium加密的性能高出约40％。

![img{512x368}](../../assets/44494d96c92c30cc.png)


通过SCP，我们可以清楚地看到SSH协议的加密成本。大多数CNI表现良好，但WeaveNet再次落后于其他人。当然，由于双重加密成本（SSH加密+ CNI加密）。

以下是性能摘要总结：

![img{512x368}](../../assets/983b53aa7a0afcec.png)


## 资源消耗

现在让我们比较这些CNI在负载很重的情况下处理所带来的资源消耗如何（在TCP 10Gbit传输期间）。在性能测试中，我们将CNI与裸金属（绿色条）进行比较。对于资源消耗测试，我们还显示了没有任何CNI设置的新闲置Kubernetes（紫色条）的消耗。然后我们可以计算出CNI真正消耗的开销。

让我们从内存方面开始吧。以下是传输期间以MB为单位的平均节点RAM使用率（无缓冲区/缓存）。

![img{512x368}](../../assets/5fce9698f3f7f8d2.png)


Flannel和Kube-router表现非常好，只有大约50MB的内存占用，其次是Calico和Canal，70MB。WeaveNet的消费量明显高于其竞争对手，资源占用约为130MB。凭借400MB的内存占用，Cilium具有最高的基准内存消耗。

现在，让我们检查CPU消耗。警告：图形单位不是百分比，而是permil。因此裸金属的38 permil实际上是3.8％。结果如下：

![img{512x368}](../../assets/8936bee7d1ec7a46.png)


Calico，Canal，Flannel和Kube-router都非常高效的CPU使用，与没有CNI的kubernetes相比，开销仅多出2％。远远落后于WeaveNet，开销约为5％，然后是Cilium，CPU开销超过7％。

以下是资源消耗的摘要：

![img{512x368}](../../assets/92fac25edfa2a57f.png)


## 摘要

以下是所有结果的汇总概述：

![img{512x368}](../../assets/b958ed936137f12d.png)


## 结论

最后一部分是主观的，并传达了我自己对结果的解释。请记住，此基准测试仅在一个非常小的集群（3个节点）上测试单个连接中的吞吐速度。它不反映大型集群（> 50个节点）的网络行为，也没有多少连接并发。

如果你在相应的场景中，我建议使用以下CNI：

- 您的群集中有低资源节点（只有几GB的RAM，几个核心）并且您不需要安全功能，请使用Flannel。它是我们测试过的最精简的CNI之一。此外，它与大量架构兼容（amd64，arm，arm64等）。它是唯一一个能够正确自动检测MTU的CNI，和Cilium一起，因此您无需配置任何内容即可使其正常工作。Kube-router也很好，但标准较低，需要您手动设置MTU。
- 出于安全原因，您需要加密网络，请使用WeaveNet。如果您使用巨型帧并通过在环境变量中提供密码来激活加密，请不要忘记设置MTU大小。但话说回过来，忘掉性能，这就是加密的代价。
- 对于其他常见用法，我会推荐Calico。这种CNI广泛用于许多kubernetes部署工具（Kops，Kubespray，Rancher等）。就像WeaveNet一样，如果您使用的是巨型帧，请不要忘记在ConfigMap中设置MTU。事实证明，它在资源消耗，性能和安全性方面具有多用途和高效性。

最后但并非最不重要的，我建议你关注Cilium的工作。他们的团队非常活跃，他们正在努力提高他们的CNI（功能，资源节约，性能，安全性，多集群跨越……），他们的路线图听起来非常有趣。

![img{512x368}](../../assets/8f78ff7aa0da183c.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

你好，calico有ipip和bgp模式，能问下你测试的是那种模式吗？

这篇是翻译的文章哦:)。