---
title: YAML入门：以创建一个Kubernetes deployment为例
url: https://tonybai.com/2019/02/25/introduction-to-yaml-creating-a-kubernetes-deployment/
published: '2019-02-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# YAML入门：以创建一个Kubernetes deployment为例

[YAML](https://yaml.org/)语言似乎已经成为了事实标准的“云配置”语言，无论是容器事实标准[docker](https://tonybai.com/tag/docker)(主要是[docker-compose](https://docs.docker.com/compose/)使用)、SDN，还是容器编排王者[kubernetes](https://tonybai.com/tag/kubernetes)，又或是虚拟机时代的王者[openstack](https://www.openstack.org)采用的配置文件都是[yaml文件格式](https://yaml.org/refcard.html)。不过需要承认的是我个人最初刚接触yaml时还不是很适应（个人更适应json），在后续运维kubernetes时，每每都要去参考k8s doc中的各种k8s对象的模板才能把yaml文件写“正确”。本文是一篇译文，这篇文章很好地讲解了yaml语言的语法格式，并用kubernetes deployment配置来作为示例。至少我看完这篇文章后是受益多多，因此这里将该文章快速翻译出来，供广大的k8s爱好者、实践者参考。

本文翻译自[《Introduction to YAML: Creating a Kubernetes deployment》](https://www.mirantis.com/blog/introduction-to-yaml-creating-a-kubernetes-deployment/)。（译注：[CNCF](https://www.cncf.io/)也转发了[Openstack](https://tonybai.com/2016/05/04/deploy-devstack/)开发背后的主力推手[Mirantis公司](https://www.mirantis.com)博客的[这篇文章](https://www.cncf.io/blog/2019/02/21/introduction-to-yaml-creating-a-kubernetes-deployment/)。)

在之前的文章中，我们一直在讨论如何使用Kubernetes来启动和操作资源实例。到目前为止，我们一直都专注于命令行操作。但其实有一种更简单，更有用的方法：使用YAML创建配置文件。在本文中，我们将了解YAML的工作原理，并使用它来先定义一个Kubernetes Pod，然后再定义一个Kubernetes Deployment。

## YAML基础

如果您正在做与一些软件领域相关的事情 – 尤其是涉及Kubernetes，SDN和OpenStack等领域，那么你将很难“摆脱”YAML 。YAML是一种人类可读的、专门用于配置信息的文本格式，例如，在本文中，我们将使用YAML定义创建第一个Pod，然后是Deployment。YAML可以理解为Yet Another Markup Language的缩写，也可以理解为”YAML Ain’t Markup Language”的缩写，这取决于你问的是谁。

使用YAML进行K8s定义会带来许多优势，包括：

- 方便：您不再需要将所有参数都添加到命令行中
- 可维护： YAML文件可以添加到源代码版本控制仓库中，因此你可以跟踪文件的修改
- 灵活性：通过YAML，您能够创建比在命令行上更为复杂的结构

YAML是JSON的超集，这意味着任何有效的JSON文件也是有效的YAML文件。所以一方面，如果你知道JSON并且你只想写自己的YAML（而不是阅读其他人的那些），那么你就完全可以开始了。另一方面，不幸的是，这不太可能。即使你只是想在网上找些例子，他们更有可能是YAML格式（非JSON），所以我们不妨来习惯这种格式。尽管如此，在某些情况下JSON格式可能更为方便，因此最好知道JSON仍然可供您使用。

幸运的是，在YAML中你只需要了解两种类型的结构：

- Lists(列表)
- Maps

没错！你可能会用maps of lists和lists of maps，等等，但是一旦你掌握了这两个结构，那么你就可以开始了。这并不是说你不能做更复杂的事情，但总的来说，这就是你开始时需要的全部内容了。

## YAML Maps

让我们先来看看YAML maps。maps允许您关联键值对(name-value pairs)，在尝试设置配置信息时，这非常方便。例如，您可能有一个如下所示的配置文件：

```
---
apiVersion: v1
kind: Pod
```


第一行是分隔符，除非您尝试在单个文件中定义多个结构，否则它是可选的。在那之后，如您所见，我们有两个值：v1 和Pod ，映射到两个键：apiVersion 和kind 。

当然，这种事情非常简单，它等价于下面的JSON内容：

```
{
"apiVersion": "v1",
"kind": "Pod"
}
```


请注意，在我们的YAML版本中，引号是可选的; 处理程序可以告诉您正在查看基于这种格式的一个字符串。

您还可以通过创建一个映射到另一个map而不是字符串的键来指定更为复杂的结构，如下所示：

```
---
apiVersion: v1
kind: Pod
metadata:
name: rss-site
labels:
app: web
```


在这种情况下，我们有一个键: metadata，其值为一个带有2个键：name和labels的map。该labels键本身有一个map作为其值。您可以根据需要嵌套这些。

YAML处理程序之所以知道所有这些部分是如何相互关联的，是因为我们做了行缩进。在这个例子中，我使用了2个空格以便于阅读，但空格的数量并不重要 – 只要它至少为1，并且只要你的缩进是一致的。例如，name和labels处于相同的缩进级别，因此处理程序知道它们都是同一个map的一部分; 它知道app 是labels的值，因为它进一步缩进了。

**注意：永远不要在YAML文件中使用tab **

因此，如果我们将其转换为JSON，它将是如下所示这样的：

```
{
"apiVersion": "v1",
"kind": "Pod",
"metadata": {
"name": "rss-site",
"labels": {
"app": "web"
}
}
}
```


现在我们来看list类型。

## YAML Lists

YAML lists实际上是一个对象序列。例如：

```
args:
- sleep
- "1000"
- message
- "Bring back Firefly!"
```


正如您在此处所看到的，您可以在list中包含几乎任意数量的元素，这些元素为以短划线（ – ）开始并相对于父项缩进一级。所以如果用JSON展示，将是这样：

```
{
"args": ["sleep", "1000", "message", "Bring back Firefly!"]
}
```


当然，list中的元素也可以是maps：

```
---
apiVersion: v1
kind: Pod
metadata:
name: rss-site
labels:
app: web
spec:
containers:
- name: front-end
image: nginx
ports:
- containerPort: 80
- name: rss-reader
image: nickchase/rss-php-nginx:v1
ports:
- containerPort: 88
```


正如您在这里看到的，我们有一个container“对象” 列表，每个container都包含一个name，一个image和一个port列表。ports下的每个列表项本身都是一个containerPort及其值的map。

为了完整起见，让我们快速查看等效的JSON：

```
{
"apiVersion": "v1",
"kind": "Pod",
"metadata": {
"name": "rss-site",
"labels": {
"app": "web"
}
},
"spec": {
"containers": [{
"name": "front-end",
"image": "nginx",
"ports": [{
"containerPort": "80"
}]
},
{
"name": "rss-reader",
"image": "nickchase/rss-php-nginx:v1",
"ports": [{
"containerPort": "88"
}]
}]
}
}
```


正如你所看到的，我们的例子开始变得更为复杂了，不过我们还没有遇到特别复杂的例子！难怪YAML如此快地取代JSON。

所以让我们回顾一下。我们了解了：

- maps，它们是键值对的组
- lists，它们包含独立的元素(成员)
- maps of maps
- maps of lists
- lists of lists
- lists of maps

基本上，无论你想要组合什么结构，你都可以用这两种结构来做。

## 使用YAML创建Pod

好了，现在我们已经掌握了基础知识，让我们看看如何使用它。我们将首先使用YAML创建Pod，然后再创建Deployment。

如果您尚未安装Kubernetes集群和kubectl，请在继续之前查看本系列中有关[搭建Kubernetes的集群](https://tonybai.com/tag/kubernetes)的文章。没关系，我们等一下……

回来了吗？好！让我们从Pod开始吧。

### 创建pod文件

在前面的示例中，我们使用YAML描述了一个简单的Pod：

```
—
apiVersion: v1
kind: Pod
metadata:
name: rss-site
labels:
app: web
spec:
containers:
– name: front-end
image: nginx
ports:
– containerPort: 80
– name: rss-reader
image: nickchase/rss-php-nginx:v1
ports:
– containerPort: 88
```


我们一行行分开看，我们从API版本开始; 这里只是v1。（当我们讲解Deployment时，我们必须指定不同的版本，因为v1中不存在Deployment。）

接下来，我们指定要创建Pod; 这里我们可能会指定deployment，job，service等其他类型，具体取决于我们要实现什么。

接下来我们指定metadata。这里我们指定Pod的name，以及我们用来识别Kubernetes pod的label。

最后，我们将指定构成pod的实际对象。该规范(spec)的属性包括容器，存储卷，或其他Kubernetes需要了解的属性，比如：重新在启动容器失败时重启的选项。您可以在Kubernetes API规范中找到Kubernetes Pod属性的完整列表。让我们仔细看看典型的容器定义：

```
...
spec:
containers:
- name: front-end
image: nginx
ports:
- containerPort: 80
- name: rss-reader
...
```


在这种情况下，我们有一个简单、短小的定义：name（前端），它所基于容器镜像（nginx ），以及容器将在内部监听的一个端口（80 ）。在这些中，实际上只是name是必须的，但一般来说，如果你想要它做任何有用的事情，你需要更多的信息。

您还可以指定更复杂的属性，例如在容器启动时运行的命令，使用的参数，工作目录，或者每次实例化容器时是否拉取镜像的新副本等。您还可以指定一些更深入的信息，例如容器退出日志的存放位置。以下是您可以为Container设置的属性：

- name
- image
- command
- args
- workingDir
- ports
- env
- resources
- volumeMounts
- livenessProbe
- readinessProbe
- lifecycle
- terminationMessagePath
- imagePullPolicy
- securityContext
- stdin
- stdinOnce
- tty

现在让我们继续并实际创建pod。

### 使用YAML文件创建Pod

当然，第一步是创建一个文本文件。将其命名为pod.yaml 并添加以下文本，就像我们之前指定的那样：

```
---
apiVersion: v1
kind: Pod
metadata:
name: rss-site
labels:
app: web
spec:
containers:
- name: front-end
image: nginx
ports:
- containerPort: 80
- name: rss-reader
image: nickchase/rss-php-nginx:v1
ports:
- containerPort: 88
```


保存文件。接下来告诉Kubernetes创建pod：

```
> kubectl create -f pod.yaml
pod "rss-site" created
```


如您所见，K8引用了我们Pod的名称。如果你要求一个pod列表，你可以看到下面内容：

```
> kubectl get pods
NAME READY STATUS RESTARTS AGE
rss-site 0/2 ContainerCreating 0 6s
```


如果您提前检查，您可以看到仍在创建中的pod。几秒钟后，您应该看到容器正在运行：

```
> kubectl get pods
NAME READY STATUS RESTARTS AGE
rss-site 2/2 Running 0 14s
```


从这里开始，您可以测试Pod（就像我们在上一篇文章中所做的那样），但最终我们想要创建一个Deployment，所以让我们继续并删除它，这样就没有任何名称冲突：

```
> kubectl delete pod rss-site
pod "rss-site" deleted
```


### Pod创建故障诊断

当然，有时事情并没有像你期望的那样发展。也许您遇到了网络问题，或者您在YAML文件中输入了错误的内容。您可能会看到如下错误：

```
> kubectl get pods
NAME READY STATUS RESTARTS AGE
rss-site 1/2 ErrImagePull 0 9s
```


在这种情况下，我们可以看到我们的一个容器启动得很好，但是另一个容器出了问题。要追查问题，我们可以向Kubernetes询问有关Pod的更多信息：

```
> kubectl describe pod rss-site
Name: rss-site
Namespace: default
Node: 10.0.10.7/10.0.10.7
Start Time: Sun, 08 Jan 2017 08:36:47 +0000
Labels: app=web
Status: Pending
IP: 10.200.18.2
Controllers: <none>
Containers:
front-end:
Container ID: docker://a42edaa6dfbfdf161f3df5bc6af05e740b97fd9ac3d35317a6dcda77b0310759
Image: nginx
Image ID: docker://sha256:01f818af747d88b4ebca7cdabd0c581e406e0e790be72678d257735fad84a15f
Port: 80/TCP
State: Running
Started: Sun, 08 Jan 2017 08:36:49 +0000
Ready: True
Restart Count: 0
Environment Variables: <none>
rss-reader:
Container ID:
Image: nickchase/rss-php-nginx
Image ID:
Port: 88/TCP
State: Waiting
Reason: ErrImagePull
Ready: False
Restart Count: 0
Environment Variables: <none>
Conditions:
Type Status
Initialized True
Ready False
PodScheduled True
No volumes.
QoS Tier: BestEffort
Events:
FirstSeen LastSeen Count From SubobjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
45s 45s 1 {default-scheduler } Normal Scheduled Successfully assigned rss-site to 10.0.10.7
44s 44s 1 {kubelet 10.0.10.7} spec.containers{front-end} Normal Pulling pulling image "nginx"
45s 43s 2 {kubelet 10.0.10.7} Warning MissingClusterDNS kubelet does not have ClusterDNS IP configured and cannot create Pod using "ClusterFirst" policy. Falling back to DNSDefault policy.
43s 43s 1 {kubelet 10.0.10.7} spec.containers{front-end} Normal Pulled Successfully pulled image "nginx"
43s 43s 1 {kubelet 10.0.10.7} spec.containers{front-end} Normal Created Created container with docker id a42edaa6dfbf
43s 43s 1 {kubelet 10.0.10.7} spec.containers{front-end} Normal Started Started container with docker id a42edaa6dfbf
43s 29s 2 {kubelet 10.0.10.7} spec.containers{rss-reader} Normal Pulling pulling image "nickchase/rss-php-nginx"
42s 26s 2 {kubelet 10.0.10.7} spec.containers{rss-reader} Warning Failed Failed to pull image "nickchase/rss-php-nginx": Tag latest not found in repository docker.io/nickchase/rss-php-nginx
42s 26s 2 {kubelet 10.0.10.7} Warning FailedSync Error syncing pod, skipping: failed to "StartContainer" for "rss-reader" with ErrImagePull: "Tag latest not found in repository docker.io/nickchase/rss-php-nginx"
41s 12s 2 {kubelet 10.0.10.7} spec.containers{rss-reader} Normal BackOff Back-off pulling image "nickchase/rss-php-nginx"
41s 12s 2 {kubelet 10.0.10.7} Warning FailedSync Error syncing pod, skipping: failed to "StartContainer" for "rss-reader" with ImagePullBackOff: "Back-off pulling image \"nickchase/rss-php-nginx\""
```


正如您所看到的，这里有很多信息，但我们对事件(event)最感兴趣- 特别是一旦警告和错误开始出现。从这里我能够很快发现我忘了将”:v1″ label添加到我的image中，所以它正在寻找”:latest”标签，但该标签并不存在。

为了解决这个问题，我首先删除了Pod，然后修复了YAML文件并重新启动。相反，我可以修复镜像仓库（译注：比如增加:latest标签)，以便Kubernetes可以找到它正在寻找的东西，并且它会继续，好像什么也没发生过一样。

现在我们已经成功运行起来一个Pod，接下来让我们看看为deployment做得同样的事情。

## 使用YAML创建Deployment

最后，我们要创建一个实际的deployment。然而，在我们这样做之前，很值得去了解一下我们实际上在做什么。

记住，K8管理基于容器的资源。在使用deployment的情况下，您将创建一组要管理的资源。例如，我们在上一个示例中创建了Pod的单个实例，我们可能会创建一个Deployment来告诉Kubernetes管理该Pod的一组副本 – 字面意思就是ReplicaSet – 以确保它们中的一定数量是始终可用。所以我们可以像这样开始我们的deployment定义：

```
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: rss-site
spec:
replicas: 2
```


在这里，我们将apiVersion指定为”extensions/v1beta1″ – 记住，我们想要一个deployment, 但deployment不像pod那样在v1中。接下来我们指定name。我们还可以指定我们想要的任何其他元数据，但现在让我们保持简单。

最后，我们进入规范(spec)。在Pod规范中，我们提供了有关实际进入Pod的内容的信息; 我们将在这里使用deployment做同样的事情。在这种情况下，我们先描述我们要部署什么Pod，我们总是希望有 2个副本。当然，您可以根据需要设置此数字，并且还可以设置其他属性，例如定义受此部署影响的Pod的selector，或者在被认为“ready”之前，pod必须启动且没有任何错误的最小秒数。您可以在Kuberenetes v1beta1 API参考中找到Deployment规范属性的完整列表。

好的，现在我们知道我们需要2个副本，我们需要回答这个问题：“什么的副本？”它们由模板定义：

```
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: rss-site
spec:
replicas: 2
template:
metadata:
labels:
app: web
spec:
containers:
- name: front-end
image: nginx
ports:
- containerPort: 80
- name: rss-reader
image: nickchase/rss-php-nginx:v1
ports:
- containerPort: 88
```


看起来熟悉？就应该是这样; 它与上一节中的Pod定义几乎完全相同，而且就是这样设计的。模板只是要复制的对象的定义 – 在其他情况下，可以通过自己创建的对象。

现在让我们继续创建deployment。将YAML添加到名为deployment.yaml 的文件中，并让Kubernetes创建它：

```
> kubectl create -f deployment.yaml
deployment "rss-site" created
```


要了解它是如何做的，我们可以检查deployment列表：

```
> kubectl get deployments
NAME DESIRED CURRENT UP-TO-DATE AVAILABLE AGE
rss-site 2 2 2 1 7s
```


正如您所看到的，Kubernetes已经启动了两个副本，但只有一个可用。您可以像以前一样通过描述deployment来检查事件日志：

```
> kubectl describe deployment rss-site
Name: rss-site
Namespace: default
CreationTimestamp: Mon, 09 Jan 2017 17:42:14 +0000=
Labels: app=web
Selector: app=web
Replicas: 2 updated | 2 total | 1 available | 1 unavailable
StrategyType: RollingUpdate
MinReadySeconds: 0
RollingUpdateStrategy: 1 max unavailable, 1 max surge
OldReplicaSets: <none>
NewReplicaSet: rss-site-4056856218 (2/2 replicas created)
Events:
FirstSeen LastSeen Count From SubobjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
46s 46s 1 {deployment-controller } Normal ScalingReplicaSet Scaled up replica set rss-site-4056856218 to 2
```


正如你在这里看到的，没有问题，它还没有完成扩展(scale)。再过几秒钟，我们可以看到两个Pod都在运行：

```
> kubectl get deployments
NAME DESIRED CURRENT UP-TO-DATE AVAILABLE AGE
rss-site 2 2 2 2 1m
```


## 到这里我们得到了什么

好的，让我们回顾一下。我们基本上涵盖了三个主题：

- YAML是一种人类可读的基于文本的格式，通过使用键值对的map和list（以及相互嵌套）的组合，您可以轻松指定配置类型信息。
- YAML是使用Kubernetes对象最方便的方法，在本文中我们研究了创建Pod和Deployments。
- 通过要求Kubernetes 描述(describe)它们，您可以获得有关运行（或应该运行）对象的更多信息。

这是我们的基本YAML教程。我们将在未来几个月内处理大量与Kubernetes相关的内容，因此，如果您想了解具体内容，请在评论中告知我们，或在@MirantisIT上发推特。

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

受益匪浅，感谢 ~