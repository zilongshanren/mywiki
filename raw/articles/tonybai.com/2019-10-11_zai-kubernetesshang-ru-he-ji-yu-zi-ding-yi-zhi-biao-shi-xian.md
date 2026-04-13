---
title: 在Kubernetes上如何基于自定义指标实现应用的自动缩放
url: https://tonybai.com/2019/10/11/autoscaling-apps-on-kubernetes/
published: '2019-10-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 在Kubernetes上如何基于自定义指标实现应用的自动缩放

![img{512x368}](../../assets/0e3a87a1d2493aed.png)


## 如何在Kubernetes上实现应用缩放？

使用静态配置将应用程序部署到生产环境并不是最佳选择。

流量模式可能会快速变化，应用程序应该能够实现自适应：

- 当需求增加时，应用程序应扩大规模（增加副本数）以保持响应速度。
- 当需求减少时，应用程序应缩小规模（减少副本数量），以免浪费资源。

[Kubernetes](https://tonybai.com/tag/kubernetes)以Horizontal Pod Autoscaler的形式为自动缩放应用程序提供了出色的支持。

下面我们将学习如何使用它。

## 不同类型的自动缩放

首先，为了消除任何误解，让我们澄清一下Kubernetes中的术语“自动缩放”的不同用法。

在Kubernetes中，有几件事可被称为“自动缩放”，包括：

- 水平Pod自动缩放器：调整应用程序的副本数
- Vertical Pod Autoscaler：调整容器的资源请求(request)和限制(limit)
- 集群自动缩放器：调整集群的节点数

尽管这些组件都可以“自动缩放”某些东西，但是它们彼此之间完全不相关。

它们都针对非常不同的用例，并使用不同的概念和机制。

它们是在单独的项目中开发的，可以彼此独立使用。

**本文介绍的是水平Pod自动缩放器。**

## 什么是水平Pod自动缩放器？

水平Pod自动配置器是Kubernetes内置的功能，允许基于一个或多个被监测的指标水平缩放应用规模。

水平缩放意味着增加和减少副本数量。垂直缩放意味着增加和减少单个副本的计算资源。


从技术上讲，Horizontal Pod Autoscaler是Kubernetes控制器管理器(controller manager)中的控制器(controller)，它是由[HorizontalPodAutoscaler资源对象](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#horizontalpodautoscaler-v2beta2-autoscaling)配置的。

Horizontal Pod Autoscaler可以监视有关应用程序的指标，并不断调整副本数以最佳地满足当前需求。

Horizontal Pod Autoscaler可缩放的资源包括Deployment，StatefulSet，ReplicaSet和ReplicationController。


为了自动缩放应用程序，Horizontal Pod自动缩放器会执行一个永久控制循环：

![img{512x368}](../../assets/cfb59a7dcaae4986.png)


此控制循环的步骤为：

- 查询缩放指标
- 计算所需的副本数
- 将应用程序缩放到所需数量的副本

控制循环的默认周期为15秒


所需副本数的计算基于缩放度量和该度量的用户提供的目标值。

目的是计算一个副本计数，该副本计数将使度量值尽可能接近目标值。

例如，假设缩放指标是每个副本的每秒请求速率：

- 如果目标值为10 req / sec，而当前值为20 req / sec，则Horizontal Pod Autoscaler将按比例放大应用程序（即增加副本数），以使度量标准减小并更接近目标值。
- 如果目标值为10 req / sec，当前值为2 req / sec，则Horizontal Pod Autoscaler将按比例缩小应用程序（即减少副本数），以使度量标准增加并更接近目标值。

用于计算所需副本数的算法基于以下公式：

```
X = N * (c/t)
```


其中X是所需的副本数，N是当前副本数，c是度量的当前值，t是目标值。

您可以在

[文档]中找到有关算法的详细信息。

这就是Horizontal Pod Autoscaler的工作方式，但是如何使用它呢？

## 如何配置水平pod自动缩放器？

通过创建HorizontalPodAutoscaler资源，可以将Horizontal Pod Autoscaler配置为自动缩放应用程序。

此资源使您可以指定以下参数：

- 可扩展的资源（例如，部署）
- 最小和最大副本数
- 缩放指标
- 缩放指标的目标值

创建此资源后，Horizontal Pod Autoscaler将使用提供的参数开始对您的应用执行上述控制循环。

具体的HorizontalPodAutoscaler资源如下所示：

```
//hpa.yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
name: myhpa
spec:
scaleTargetRef:
apiVersion: apps/v1
kind: Deployment
name: myapp
minReplicas: 1
maxReplicas: 10
metrics:
- type: Pods
pods:
metric:
name: myapp_requests_per_second
target:
type: AverageValue
averageValue: 2
```


存在清单文件结构不同的HorizontalPodAutoscaler资源的不同版本。上面的示例使用version v2beta2，它是撰写本文时的最新版本。


此资源myapp根据myapp_requests_per_second一个目标值为2 的指标指定一个名为Deployment的部署，该部署将在1到10个副本之间自动缩放。

您可以想象到，该myapp_requests_per_second指标代表此部署中各个Pod的请求率-因此，本规范的目的是自动调整Deployment的目标，以使每个Pod保持每秒2个请求的请求率。

到目前为止，这听起来不错，但有一个问题。

指标来自哪里？

## 什么是指标注册表？

整个自动缩放机制均基于代表应用程序当前负载的指标。

定义HorizontalPodAutoscaler资源时，您必须指定此类指标。

但是Horizontal Pod Autoscaler如何知道如何获取这些指标？

事实证明，还有另一个组件在起作用-指标注册表。

Horizontal Pod Autoscaler从指标注册表查询指标：

![img{512x368}](../../assets/d2af67cd48acbce3.png)


度量标准注册表是集群中的中心位置，度量标准（任何类型）向客户端（任何类型）公开。

Horizontal Pod Autoscaler是这些客户端之一。

度量标准注册表的目的是为客户端提供从中查询度量标准的标准接口。

指标注册表的接口包含三个单独的API：

![img{512x368}](../../assets/03c5a44a3c57f552.png)


这些API旨在提供不同类型的指标：

- 资源度量标准API： Pod和节点的预定义资源使用度量标准（CPU和内存）
- 自定义指标API：与Kubernetes对象关联的自定义指标
- 外部指标API：与Kubernetes对象不关联的自定义指标

所有这些度量标准API都是[扩展API](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)。

这意味着它们是核心Kubernetes API的扩展，可通过Kubernetes API服务器进行访问。

如果要自动缩放应用程序，这对您意味着什么？

您想要用作缩放指标的任何指标都必须通过这三个指标API之一公开。

因为只有这样，Horizontal Pod Autoscaler才能访问它们。

因此，要自动缩放应用程序，您的任务不仅是配置Horizontal Pod自动缩放器…

**您还必须通过度量标准注册表公开所需的缩放度量标准。**

如何通过度量标准API公开度量标准？

通过在集群中安装和配置其他组件。

对于每个度量标准API，您需要一个相应的度量标准API服务器，并且需要对其进行配置以通过度量标准API公开特定的度量标准。

默认情况下，Kubernetes中未安装任何度量标准API服务器，这意味着默认情况下未启用度量标准API 。


此外，您需要一个指标收集器，该指标收集器从源（例如，从目标应用的Pod）收集所需的指标，并将其提供给指标API服务器。

![img{512x368}](../../assets/06222bf8267a0c85.png)


对于不同的度量标准API，度量标准API服务器和度量标准收集器有不同的选择。

**资源指标API：**

- 指标收集器是
[cAdvisor](https://github.com/google/cadvisor)，它在每个工作程序节点上作为kubelet的一部分运行（因此默认情况下已安装） - 资源指标API的官方指标API服务器是
[metrics-server](https://github.com/kubernetes-incubator/metrics-server)

**自定义指标API和外部指标API：**

- 指标收集器的一个流行选择是Prometheus。但是，也可以使用其他指标系统（例如Datadog或Google Stackdriver）代替
- 该
[prometheus适配器](https://github.com/DirectXMan12/k8s-prometheus-adapter)是与普罗米修斯集成为度量收集的度量标准API服务器-但是，其他度量收集器有自己的度量标准API服务器

因此，要通过一种度量标准API公开度量标准，您必须执行以下步骤：

- 安装指标收集器（例如Prometheus）并将其配置为收集所需指标（例如从您的应用程序的Pod中收集）
- 安装度量标准API服务器（例如Prometheus适配器）并将其配置为通过相应的度量标准API从度量标准收集器暴露度量数据

请注意，这专门适用于提供自定义指标的自定义指标API和外部指标API。Resource Metrics API仅提供默认指标，而不能配置为提供自定义指标。


以上信息很多，让我们把它们放在一起再完整过一遍。

## 放在一起

让我们来看一个完整的示例，该示例将应用配置为由Horizontal Pod Autoscaler自动缩放。

想象一下，您想基于副本的平均每秒请求速率来自动缩放Web应用程序。

另外，假设您要使用基于Prometheus的设置来通过Custom Metrics API公开请求率指标。

请求速率是与Kubernetes对象（Pods）关联的自定义指标，因此必须通过Custom Metrics API公开。


以下是达到目标的一系列步骤：

- 设置您的应用程序，以将接收到的请求总数作为Prometheus指标公开
- 安装Prometheus并将其配置为从应用程序的所有Pod中收集此指标
- 安装Prometheus适配器并将其配置为将度量标准从Prometheus转换为每秒请求速率（使用PromQL）并且作为myapp_requests_per_second指标通过Custom Metrics API 公开
- 创建一个HorizontalPodAutoscaler资源（如上所示），指定myapp_requests_per_second为缩放指标和适当的目标值

一旦创建HorizontalPodAutoscaler资源，Horizontal Pod Autoscaler就会启动，并开始根据您的配置自动缩放您的应用程序。

现在，您可以观察您的应用程序适应流量的情况。

本文为基于自定义指标自动缩放应用程序设置了理论框架。

在以后的文章中，您将把这些知识付诸实践，并在自己的集群上使用自己的应用程序执行上述步骤。

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

## 评论