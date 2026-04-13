---
title: 提高您的kubectl生产力（第二部分）：命令完成、资源规范快速查看和自定义列输出格式
url: https://tonybai.com/2019/08/30/kubectl-productivity-part2/
published: '2019-08-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 提高您的kubectl生产力（第二部分）：命令完成、资源规范快速查看和自定义列输出格式

本文翻译自[《Boosting your kubectl productivity》](https://learnk8s.io/blog/kubectl-productivity/)。

第一部分：[什么是kubectl？](https://tonybai.com/2019/08/29/kubectl-productivity-part1/)

## 1. 通过命令完成(command completion)减少输入

命令完成是提高你的kubectl生产力的最有用但经常被忽视的技巧之一。

命令完成允许您使用Tab键自动完成kubectl命令的各个部分。这适用于子命令，选项和参数，包括资源名称等难以输入的内容。

在这里你可以看到kubectl命令完成的动作：

![img{512x368}](../../assets/cd6ad50c67f0b256.gif)


在[官方文档](https://kubernetes.io/docs/tasks/tools/install-kubectl/#enabling-shell-autocompletion)中包含有关设置命令完成的详细说明，下面的章节我们再带着大家回顾一下。

### 命令完成的工作原理

通常，命令完成是一个shell功能，它通过completion script(完成脚本)的方式工作。完成脚本是一个shell脚本，用于定义特定命令的完成行为。获取完成脚本可以完成相应的命令。

Kubectl可以使用以下命令自动生成并打印出Bash和Zsh的完成脚本：

```
$kubectl completion bash
# or
$kubectl completion zsh
```


理论上，在适当的shell中获取此命令的输出可以完成kubectl命令。

但是，在实践中，Bash（包括Linux和macOS之间的差异）和Zsh的细节不同。以下部分解释了所有这些情况：

- 在Linux上为Bash设置命令完成
- 在macOS上设置Bash的命令完成
- 设置Zsh的命令完成

### 在Linux上的Bash

Bash的完成脚本取决于[bash-completion项目](https://github.com/scop/bash-completion)，因此您必须先安装它。

您可以使用[各种包管理器](https://github.com/scop/bash-completion#installation)安装bash-completion 。例如：

```
$sudo apt-get install bash-completion
# or
$yum install bash-completion
```


您可以使用以下命令测试是否正确安装了bash-completion：

```
$type _init_completion
```


如果这输出shell函数的代码，则已正确安装bash-completion。如果该命令输出not found错误，则必须将以下行添加到您的~/.bashrc文件中：

```
$source /usr/share/bash-completion/bash_completion
```


是否必须将此行添加到您的~/.bashrc文件中，取决于您用于安装bash-completion的包管理器。对于APT来说，这是必要的，对于yum，则无需。


安装bash-completion后，您必须进行设置，以便在所有shell会话中获取kubectl 完成脚本。

一种方法是将以下行添加到您的~/.bashrc文件中：

```
source <(kubectl completion bash)
```


另一种可能性是将kubectl完成脚本添加到/etc/bash_completion.d目录中（如果它不存在则创建它）：

```
$kubectl completion bash >/etc/bash_completion.d/kubectl
```


/etc/bash_completion.d目录中的所有完成脚本都是由bash-completion自动获取的。


两种方法都是等价的。

重新加载shell后，kubectl命令完成应该正常工作！

### 在MacOS上的Bash

有了macOS，就会出现轻微的复杂情况。原因是macOS上的Bash默认版本是3.2，这已经过时了。遗憾的是，kubectl完成脚本至少需要Bash 4.1，因此不适用于Bash 3.2。

Apple在macOS中包含过时版本的Bash的原因是较新版本使用Apple不支持的GPLv3许可证。


这意味着，要在macOS上使用kubectl命令完成，**您必须安装较新版本的Bash**。您甚至可以将它设为新的默认shell，这将为您节省很多此类麻烦。这实际上并不困难，您可以在我之前编写的macOS文章中的升级Bash中找到说明。

**在继续之前，请确保您现在确实使用的是Bash 4.1或更新版本（请查看bash –version）**。

Bash的完成脚本取决于[bash-completion项目](https://github.com/scop/bash-completion)，因此您必须先安装它。

您可以使用[Homebrew](https://brew.sh/)安装bash-completion ：

```
$brew install bash-completion@2
```


bash-completion v2的@2代表。kubectl完成脚本需要bash-completion v2，而bash-completion v2至少需要Bash 4.1。这就是您不能在低于4.1的Bash版本上使用kubectl完成脚本的原因。


该brew install命令的输出包含一个“警告”部分，其中包含将以下行添加到您的~/.bash_profile文件的说明：

```
export BASH_COMPLETION_COMPAT_DIR=/usr/local/etc/bash_completion.d
[[ -r "/usr/local/etc/profile.d/bash_completion.sh" ]] && . "/usr/local/etc/profile.d/bash_completion.sh"
```


您必须这样做才能完成bash-completion的安装。但是，我建议将这些行添加到您~/.bashrc文件中而不是~/.bash_profile文件中。这能确保子shell中也可以使用bash-completion。

重新加载shell后，可以使用以下命令测试是否正确安装了bash-completion：

```
$type _init_completion
```


如果这输出shell函数的代码，那么你就完成了。

现在，您必须进行设置以便kubectl 完成脚本在所有shell会话中获取。

一种方法是将以下行添加到您的~/.bashrc文件中：

```
source <(kubectl completion bash)
```


另一种可能性是将kubectl完成脚本添加到/usr/local/etc/bash_completion.d目录：

```
$kubectl completion bash >/usr/local/etc/bash_completion.d/kubectl
```


这仅在您使用Homebrew安装bash-completion时才有效。在这种情况下，bash-completion会在此目录中提供所有完成脚本。


如果您还使用Homebrew安装了kubectl，您甚至不必执行上述步骤，因为完成脚本应该已经通过kubectl howbrew formula放在/usr/local/etc/bash_completion.d目录中了。在这种情况下，kubectl完成应该在安装bash-completion后自动开始工作。

最后，所有这些方法都是等效的。

重新加载shell后，kubectl完成应该正常工作！

### Zsh

Zsh的完成脚本没有任何依赖项。因此，您所要做的就是设置所有内容，以便在所有shell会话中获取源代码。

您可以通过在~/.zshrc文件中添加以下行来完成此操作：

```
source <(kubectl completion zsh)
```


如果在重新加载shell后出现错误:command not found: compdef，则必须启用compdef内置功能，您可以通过将以下内容添加到~/.zshrc文件的开头来执行此操作：

```
autoload -Uz compinit
compinit
```


## 2. 快速查找资源规范

创建YAML资源定义时，您需要知道这些资源的字段及其含义。一个可以查找到此类信息的位置是在[API参考文档](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.13/)中，那里包含了所有资源的完整规范。

但是，每次需要查找某些内容时都要切换到Web浏览器很乏味。因此，kubectl提供了kubectl explain命令，可以打印出终端中所有资源的资源规范。

kubectl explain用法如下：

```
$kubectl explain resource[.field]...
```


该命令输出所请求资源或字段的规范。kubectl explain显示的信息与API参考中的信息相同。

默认情况下，kubectl explain仅显示单个级别的字段。您可以使用显示整个字段树的标志:–recursive：

```
$kubectl explain deployment.spec --recursive
```


如果您不确定可以使用哪些资源名称，可以使用kubectl explain以下命令显示所有这些名称：

```
$kubectl api-resources
```


此命令以复数形式显示资源名称（例如，deployments而不是deployment）。对于拥有短名称的资源，它还显示该资源的短名称（例如：deploy）。不要担心这些差异，对于kubectl来说，所有这些名称变体都是等同的。也就是说，你可以在kubectl explain中使用它们中的任何一个。

例如，以下所有命令都是等效的：

```
$kubectl explain deployments.spec
# or
$kubectl explain deployment.spec
# or
$kubectl explain deploy.spec
```


## 3. 使用自定义列输出格式

kubectl get命令的默认输出格式（用于读取资源）如下：

```
$kubectl get pods
NAME READY STATUS RESTARTS AGE
engine-544b6b6467-22qr6 1/1 Running 0 78d
engine-544b6b6467-lw5t8 1/1 Running 0 78d
engine-544b6b6467-tvgmg 1/1 Running 0 78d
web-ui-6db964458-8pdw4 1/1 Running 0 78d
```


这对于人类而言，是一种很好的可读格式，但它只包含有限的信息。如您所见，每个资源只显示一些字段（与完整资源定义相比）。

这就是自定义列输出格式的用武之地。它允许您自由定义要显示在其中的列和数据。您可以选择要在输出中显示为单独列的资源的任何字段

自定义列输出选项的用法如下：

```
-o custom-columns=<header>:<jsonpath>[,<header>:<jsonpath>]...
```


您必须将每个输出列定义为一

<

header>:

-
<


header> 是列的名称，您可以选择任何您想要的。

*

我们来看一个简单的例子：

```
$ kubectl get pods -o custom-columns='NAME:metadata.name'
NAME
engine-544b6b6467-22qr6
engine-544b6b6467-lw5t8
engine-544b6b6467-tvgmg
web-ui-6db964458-8pdw4
```


这里，输出包含一个显示所有Pod名称的列。

选择Pod名称的表达式是metadata.name。这样做的原因是Pod的名称在Pod资源字段的metadata的name字段中定义（您可以在API参考中查找或使用kubectl explain pod.metadata.name）。

现在，假设您要在输出中添加一个附加列，例如，显示每个Pod正在运行的节点。为此，您只需向自定义列选项添加适当的列规范：

```
$kubectl get pods \
-o custom-columns='NAME:metadata.name,NODE:spec.nodeName'
NAME NODE
engine-544b6b6467-22qr6 ip-10-0-80-67.ec2.internal
engine-544b6b6467-lw5t8 ip-10-0-36-80.ec2.internal
engine-544b6b6467-tvgmg ip-10-0-118-34.ec2.internal
web-ui-6db964458-8pdw4 ip-10-0-118-34.ec2.internal
```


选择节点名称的表达式是spec.nodeName。这是因为已调度Pod的节点保存在Pod的spec.nodeName字段中（请参阅参考资料kubectl explain pod.spec.nodeName）。

请注意，Kubernetes资源字段区分大小写。


您可以通过这种方式将资源的任何字段设置为输出列。只需浏览资源规范并尝试使用您喜欢的任何字段！

但首先，让我们仔细看看这些字段选择表达式。

### JSONPath表达式

选择资源字段的表达式基于[JSONPath](https://goessner.net/articles/JsonPath/index.html)。

JSONPath是一种从JSON文档中提取数据的语言（类似于XPath for XML）。选择单个字段只是JSONPath的最基本用法。它有很多功能，如列表选择器，过滤器等。

但是，kubectl explain仅支持JSONPath功能的一部分。以下通过示例用法总结了这些支持的功能：

```
# Select all elements of a list
$kubectl get pods -o custom-columns='DATA:spec.containers[*].image'
# Select a specific element of a list
$kubectl get pods -o custom-columns='DATA:spec.containers[0].image'
# Select those elements of a list that match a filter expression
$kubectl get pods -o custom-columns='DATA:spec.containers[?(@.image!="nginx")].image'
# Select all fields under a specific location, regardless of their name
$kubectl get pods -o custom-columns='DATA:metadata.*'
# Select all fields with a specific name, regardless of their location
$kubectl get pods -o custom-columns='DATA:..image'
```


特别重要的是[]操作符。Kubernetes资源的许多字段都是列表，此运算符允许您选择这些列表中的项目。它通常与通配符一起使用，[*]以选择列表中的所有项目。

您将在下面找到一些使用此表示法的示例。

### 示例应用程序

使用自定义列输出格式的可能性是无穷无尽的，因为您可以在输出中显示资源的任何字段或字段组合。以下是一些示例应用程序，但您可以自己探索并找到对您有用的应用程序！

提示：如果您经常使用其中一个命令，则可以为其创建shell别名。


#### 显示Pods的容器镜像

```
$kubectl get pods \
-o custom-columns='NAME:metadata.name,IMAGES:spec.containers[*].image'
NAME IMAGES
engine-544b6b6467-22qr6 rabbitmq:3.7.8-management,nginx
engine-544b6b6467-lw5t8 rabbitmq:3.7.8-management,nginx
engine-544b6b6467-tvgmg rabbitmq:3.7.8-management,nginx
web-ui-6db964458-8pdw4 wordpress
```


此命令显示每个Pod的所有容器镜像的名称。

请记住，Pod可能包含多个容器。在这种情况下，单个Pod的容器镜像在同一列中显示为逗号分隔列表。


#### 显示节点的可用区域

```
$kubectl get nodes \
-o custom-columns='NAME:metadata.name,ZONE:metadata.labels.failure-domain\.beta\.kubernetes\.io/zone'
NAME ZONE
ip-10-0-118-34.ec2.internal us-east-1b
ip-10-0-36-80.ec2.internal us-east-1a
ip-10-0-80-67.ec2.internal us-east-1b
```


如果您的Kubernetes群集部署在公共云基础架构（例如AWS，Azure或GCP）上，则此命令非常有用。它显示每个节点所在的可用区域。

可用区域是云的概念，表示地理区域内的一个可复制点。


每个节点的可用区域通过特殊标签failure-domain.beta.kubernetes.io/zone获得。如果集群在公共云基础结构上运行，则会自动创建此标签，并将其值设置为节点的可用区域的名称。

标签不是Kubernetes资源规范的一部分，因此您无法在API参考中找到上述标签。但是，如果将节点输出为YAML或JSON，则可以看到它（以及所有其他标签）：

```
$kubectl get nodes -o yaml
# or
$kubectl get nodes -o json
```


除了探索资源规范之外，这通常是发现有关资源的更多信息的好方法。

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