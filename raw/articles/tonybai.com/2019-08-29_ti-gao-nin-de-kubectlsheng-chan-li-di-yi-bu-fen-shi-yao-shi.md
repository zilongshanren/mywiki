---
title: 提高您的kubectl生产力（第一部分）：什么是kubectl
url: https://tonybai.com/2019/08/29/kubectl-productivity-part1/
published: '2019-08-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 提高您的kubectl生产力（第一部分）：什么是kubectl

![img{512x368}](../../assets/683106b0e466dc1b.jpg)


本文翻译自[《Boosting your kubectl productivity》](https://learnk8s.io/blog/kubectl-productivity/)。

如果您使用[Kubernetes](https://coding.imooc.com/class/chapter/284.html)，那么[kubectl](https://tonybai.com/2018/06/14/the-authentication-and-authorization-of-kubectl-when-accessing-k8s-cluster/)可能是您最常用的工具之一。每当您花费大量时间使用某种特定工具时，值得深入了解并了解如何有效地使用它。

本文包含一系列提示和技巧，使您对kubectl的使用更加高效和有效。同时，它旨在加深您对[Kubernetes](https://tonybai.com/tag/k8s)各方面工作的理解。

本文的目标是让您在Kubernetes的日常工作更高效、更愉快！

## 简介：什么是kubectl？

在学习如何更有效地使用kubectl之前，您应该基本了解它是什么以及它是如何工作的。

从用户的角度来看，kubectl是控制Kubernetes的驾驶舱。它允许您执行所有可能的Kubernetes操作。

从技术角度来看，kubectl是[Kubernetes API](https://tonybai.com/2017/03/03/access-api-server-from-a-pod-through-serviceaccount/)的客户端。

Kubernetes API是一个HTTP REST API。此API是真正的Kubernetes用户接口。通过API我们可以完全控制Kubernetes。这意味着每个Kubernetes操作都作为API端点公开，并且可以通过对此端点的HTTP请求来执行。

因此，kubectl的主要工作是对Kubernetes API执行HTTP请求

![img{512x368}](../../assets/cb8f4b6ebfc10ad5.png)


Kubernetes是一个完全以资源为中心的系统。这意味着，Kubernetes保持内部资源状态，所有Kubernetes操作都是对这些资源的

[CRUD操作]。您可以通过操纵这些资源来完全控制Kubernetes（并且Kubernetes根据当前的资源状态确定要做什么）。因此，[Kubernetes API的参考文档]是按资源类型列表及其关联操作进行组织的。

让我们考虑一个例子。

想象一下，您想要创建ReplicaSet资源。为此，您需要在名为replicaset.yaml file 的文件中定义ReplicaSet ，然后运行以下命令：

```
kubectl create -f replicaset.yaml
```


显然，这会在Kubernetes中创建ReplicaSet。但是幕后会发生什么？

Kubernetes具有创建ReplicaSet操作，并且与所有Kubernetes操作一样，它作为API端点公开。此操作的特定API端点如下：

```
POST /apis/apps/v1/namespaces/{namespace}/replicasets
```


您可以在API参考文档中找到所有Kubernetes操作的API端点（包括

[上述端点]）。要向端点发出实际请求，您需要将API服务器的URL添加到API参考中列出的端点路径。

因此，当您执行上述命令时，kubectl会向上述API端点发出HTTP POST请求。ReplicaSet定义（您在replicaset.yaml文件中提供的）定义在请求正文中传递。

这就是kubectl如何适用于与Kubernetes集群交互的所有命令。在所有这些情况下，kubectl只是向适当的Kubernetes API端点发出HTTP请求。

请注意，完全可以curl通过手动向Kubernetes API发出HTTP请求等工具来控制Kubernetes 。Kubectl让您更容易使用Kubernetes API。


这些是kubectl的基础知识以及它是如何工作的。但是每个kubectl用户应该知道的Kubernetes API还有很多。为此，让我们简要介绍一下Kubernetes的内部结构。

### Kubernetes内部

Kubernetes由一组独立组件组成，这些组件在集群节点上作为单独的进程运行。某些组件在主节点上运行，而其他组件在工作节点上运行，每个组件都有一个非常特定的功能。

这些是主节点上最重要的组件：

- 存储后端：存储资源定义（通常使用etcd）
- API服务器：提供Kubernetes API并管理存储后端
- 控制器管理器：确保资源状态符合规范
- 调度程序：将Pod调度到工作节点

这是工作节点上最重要的组件：

[Kubelet](https://tonybai.com/2017/10/16/out-of-node-resource-handling-in-kubernetes-cluster/)：负责管理工作节点上的容器执行

为了了解这些组件如何协同工作，让我们考虑一个例子。

假设您刚刚执行kubectl create -f replicaset.yaml。kubectl向创建ReplicaSet API端点发送HTTP POST请求（传递ReplicaSet资源定义）。

集群中有什么影响？观看以下内容：

![img{512x368}](../../assets/98c82813f7d9b2f5.png)


图：执行kubectl create -f replicaset.yaml，API服务器将ReplicaSet资源定义保存在存储后端中。

![img{512x368}](../../assets/37fc958e7a9a403f.png)


图：这会触发控制器管理器中的ReplicaSet控制器，后者会监视ReplicaSet资源的创建，更新和删除。

![img{512x368}](../../assets/05e9979ffbb9498c.png)


图：ReplicaSet控制器为ReplicaSet的每个副本创建一个Pod定义（根据ReplicaSet定义中的Pod模板）并将它们保存在存储后端中。

![img{512x368}](../../assets/083eb977f9237b16.png)


图：这会触发监视尚未分配给工作节点的Pod的调度程序。

![img{512x368}](../../assets/fe1227cf76da1bc7.png)


图：调度程序为每个Pod选择合适的工作节点，并将此信息添加到存储后端中的Pod定义。

![img{512x368}](../../assets/8b8d253e730f5cf9.png)


图：这会触发已调度Pod的工作节点上的kubelet，后者监视已调度到其工作节点的Pod。

![img{512x368}](../../assets/5bd1f23cb0416cba.png)


图：kubelet从存储后端读取Pod定义，并指示容器运行时（例如Docker）在工作节点上运行容器。

以下是文字说明。

创建ReplicaSet端点的API请求由API服务器处理。API服务器对请求进行身份验证，并将ReplicaSet资源定义保存在存储后端中。

此事件触发ReplicaSet控制器，它是控制器管理器的子进程。ReplicaSet控制器监视存储后端中ReplicaSet资源的创建，更新和删除，并在发生这种情况时通过事件得到通知。

ReplicaSet控制器的工作是确保存在ReplicaSet所需数量的副本Pod。在我们的示例中，尚未存在Pod，因此ReplicaSet控制器会创建这些Pod定义（根据ReplicaSet定义中的Pod模板）并将它们保存在存储后端中。

新Pod 的创建会触发调度程序，后者监视尚未调度到工作节点的Pod定义。调度程序为每个Pod选择合适的工作节点，并使用此信息更新存储后端中的Pod定义。

请注意，到目前为止，集群中的任何位置都没有运行工作负载代码。到目前为止所做的就是在主节点上的存储后端创建和更新资源。


此事件触发监视调度到其工作节点的Pod的kubelet。已安排ReplicaSet Pods的工作节点的kubelet指示已配置的容器运行时（可能是[Docker](https://tonybai.com/tag/docker)）下载所需的容器映像并运行容器。

此时，最后，您的ReplicaSet应用程序正在运行！

### Kubernetes API的作用

从上面的示例中可以看出，Kubernetes组件（API服务器和存储后端除外）通过监视存储后端中的资源更改和操作存储后端中的资源来工作。

但是，这些组件不直接访问存储后端，而只能通过Kubernetes API访问存储后端。

请考虑以下示例：

- ReplicaSet控制器使用列表ReplicaSets API端点 API操作以及watch用于监视ReplicaSet资源更改的参数。
- ReplicaSet控制器使用create Pod API端点来创建Pod。
- 调度程序使用修补程序Pod API端点来更新Pod，其中包含有关所选工作节点的信息。

如您所见，这与kubectl也使用的API相同。

Kubernetes API对内部组件和外部用户的双重使用是Kubernetes的基本设计概念。

有了这些知识，您可以总结Kubernetes的工作原理如下：

- 存储后端存储Kubernetes的状态（即资源）。
- API服务器以Kubernetes API的形式提供存储后端的接口。
- 所有其他Kubernetes组件和用户通过Kubernetes API读取，观察和操纵Kubernetes的状态（即资源）。

熟悉这些概念将有助于您更好地理解kubectl并充分利用它！

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