---
title: 提高您的kubectl生产力（第三部分）：集群上下文切换、使用别名减少输入和插件扩展
url: https://tonybai.com/2019/08/31/kubectl-productivity-part3/
published: '2019-08-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 提高您的kubectl生产力（第三部分）：集群上下文切换、使用别名减少输入和插件扩展

本文翻译自[《Boosting your kubectl productivity》](https://learnk8s.io/blog/kubectl-productivity/)。

第一部分：[什么是kubectl？](https://tonybai.com/2019/08/29/kubectl-productivity-part1/)

第二部分：[命令完成、资源规范快速查看和自定义列输出格式什么是kubectl？](https://tonybai.com/2019/08/30/kubectl-productivity-part2/)

## 4. 轻松切换集群和名称空间

当kubectl必须向[Kubernetes](https://tonybai.com/tag/k8s) API发出请求时，它会读取系统上所谓的kubeconfig文件，以获取它需要访问的所有连接参数并向API服务器发出请求。

默认的kubeconfig文件是~/.kube/config。此文件通常由某个命令自动创建或更新（例如，aws eks update-kubeconfig或者gcloud container clusters get-credentials，如果您使用托管Kubernetes服务）。


使用多个集群时，您的kubeconfig文件中配置了多个集群的连接参数。这意味着，您需要一种方法来告诉kubectl 您希望它连接到哪个集群。

在集群中，您可以设置多个[名称空间](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)（名称空间是物理集群中的一种“虚拟”集群）。Kubectl也会从kubeconfig文件确定用于请求的命名空间。因此，您需要一种方法来告诉kubectl 您希望它使用哪个命名空间。

本节将介绍kubectl切换集群上下文的原理以及它是如何轻松完成的。

请注意，您还可以在

[KUBECONFIG环境变量]中列出多个kubeconfig文件。在这种情况下，所有这些文件将在执行时合并为单个有效配置。您还可以使用–kubeconfig指定kubectl命令的选项以覆盖默认的kubeconfig文件。请参阅[官方文档]。

### Kubeconfig文件

让我们看看kubeconfig文件实际包含的内容：

![img{512x368}](../../assets/c1defc6c0d2411d2.png)


如您所见，kubeconfig文件由一组上下文组成。上下文包含以下三个元素：

- 集群(cluster)：集群的API服务器的URL
- 用户(user)：集群的特定用户的身份验证凭据
- 命名空间(namespace)：连接到集群时使用的命名空间

实际上，人们经常在他们的kubeconfig文件中为每个集群的配置一个上下文。但是，你也可以为每个集群配置多个上下文，其用户或命名空间不同。但这似乎不太常见，因此通常在集群和上下文之间存在一对一的映射。


在任何给定时间，其中一个上下文被设置为当前上下文（通过kubeconfig文件中的专用字段）：

![img{512x368}](../../assets/35db046577206667.png)


当kubectl读取kubeconfig文件时，它总是使用当前上下文中的信息。因此，在上面的例子中，kubectl将连接到Hare集群。

因此，要切换到另一个集群，您只需更改kubeconfig文件中的当前上下文：

![img{512x368}](../../assets/6e4f998209be28cf.png)


在上面的示例中，kubectl现在将连接到Fox集群。

要切换到同一集群中的另一个命名空间，您可以更改当前上下文的命名空间元素的值：

![img{512x368}](../../assets/b5e490d549a58d40.png)


在上面的示例中，kubectl现在将使用Fox群集中的Prod命名空间（而不是之前设置的Test命名空间）。

请注意，kubectl还提供了–cluster，–user和–namespace，以及–context允许您覆盖单个元素和当前上下文本身的选项，无论kubeconfig文件中设置了什么。见kubectl options。


理论上，您可以通过手动编辑kubeconfig文件来执行这些更改。但当然这很乏味。以下部分介绍了允许您自动执行这些更改的各种工具。

### 使用kubectx

[kubectx](https://github.com/ahmetb/kubectx/)是一种非常流行的用于在集群和命名空间之间切换的工具。

此工具提供允许您分别更改当前上下文和命名空间的命令kubectx和kubens命令。

如上所述，如果每个集群只有一个上下文，则更改当前上下文意味着更改集群。


在这里，您可以看到这两个命令：

![img{512x368}](../../assets/03bc5b43723bc3e2.gif)


在表象之下，这些命令只是编辑kubeconfig文件，如上一节中所述。


要安装kubectx，只需按照[GitHub页面上的说明操作即可](https://github.com/ahmetb/kubectx/#installation)。

kubectx和kubens都通过完成交办提供命令完成(command completion)。这允许您自动完成上下文名称和名称空间，这样您就不必完全键入它们。您也可以在[GitHub页面](https://github.com/ahmetb/kubectx/#installation)上找到设置完成的说明。

kubectx的另一个有用功能是[交互模式](https://github.com/ahmetb/kubectx/#interactive-mode)。这与[fzf](https://github.com/junegunn/fzf)工具结合使用，您必须单独安装（事实上，安装fzf，将自动启用kubectx交互模式）。交互模式允许您通过交互式模糊搜索界面（由fzf提供）选择目标上下文或命名空间。

### 使用shell别名

实际上，您并不需要单独的工具来更改当前上下文和命名空间，因为kubectl也提供了执行此操作的命令。特别是，该kubectl config命令提供了用于编辑kubeconfig文件的子命令。这里是其中的一些：

- kubectl config get-contexts：列出所有上下文
- kubectl config current-context：获取当前上下文
- kubectl config use-context：更改当前上下文
- kubectl config set-context：更改上下文的元素

但是，直接使用这些命令并不是很方便，因为它们很难输入。但是你可以做的是将它们包装成可以更容易执行的shell别名。

我基于这些命令创建了一组别名，这些命令提供了与kubectx类似的功能。在这里你可以看到他们的行动：

![img{512x368}](../../assets/f13fd33120112f27.gif)


请注意，别名使用fzf来提供交互式模糊搜索界面（如kubectx的交互模式）。这意味着，您需要安装fzf才能使用这些别名。


以下是别名的定义：

```
# Get current context
alias krc='kubectl config current-context'
# List all contexts
alias klc='kubectl config get-contexts -o name | sed "s/^/ /;\|^ $(krc)$|s/ /*/"'
# Change current context
alias kcc='kubectl config use-context "$(klc | fzf -e | sed "s/^..//")"'
# Get current namespace
alias krn='kubectl config get-contexts --no-headers "$(krc)" | awk "{print \$5}" | sed "s/^$/default/"'
# List all namespaces
alias kln='kubectl get -o name ns | sed "s|^.*/| |;\|^ $(krn)$|s/ /*/"'
# Change current namespace
alias kcn='kubectl config set-context --current --namespace "$(kln | fzf -e | sed "s/^..//")"'
```


要安装这些别名，你只需要在上面定义添加到您的~/.bashrc或~/.zshrc文件，并重新加载你的shell(source ~/.bashrc or source ~/.zshrc)！

### 使用插件

Kubectl允许安装可以像本机命令一样调用的插件。例如，您可以安装名为kubectl-foo的插件，然后将其调用为kubectl foo。

Kubectl插件将在本文的后续部分中详细介绍。


能够像这样更改当前上下文和命名空间不是很好吗？例如，运行kubectl ctx以更改上下文，kubectl ns更改名称空间？

我创建了两个允许这样做的插件：

在内部，插件构建在上一节的别名之上。

在这里你可以看到插件的实际效果：

![img{512x368}](../../assets/eaf7e4d24fdd0303.gif)


请注意，插件使用fzf来提供交互式模糊搜索界面。这意味着，您需要安装fzf才能使用这些插件。


要安装插件，你只需要将名为的shell脚本[kubectl-ctx](https://raw.githubusercontent.com/weibeld/kubectl-ctx/master/kubectl-ctx)和[kubectl-ns](https://raw.githubusercontent.com/weibeld/kubectl-ns/master/kubectl-ns)的脚本下载以到PATH下的任何目录中，并使他们具备可执行权限（例如，使用chmod +x）。紧接着，你就应该能够使用kubectl ctx和kubectl ns！

## 5. 使用自动生成的别名减少输入

Shell别名通常是减少手工输入的好方法。该[kubectl-aliases](https://github.com/ahmetb/kubectl-aliases)项目就是以这个想法为核心，并提供800多个kubectl命令别名。

您可能想知道如何记住800个别名？实际上，您不需要记住它们，因为它们都是根据一个简单的方案生成的，下面将显示一些示例别名：

![img{512x368}](../../assets/777f7f8bd101b56a.png)


如您所见，别名由**组件(component)**组成，每个组件代表kubectl命令的特定元素。每个别名可以有一个用于基本命令，操作和资源的组件，以及用于选项的多个组件，您只需根据上述方案从左到右“填充”这些组件。

例如，别名kgpooyamlall代表命令kubectl get pods -o yaml –all-namespaces：

![img{512x368}](../../assets/02209cd70d115a80.png)


请注意，大多数选项组件的相对顺序无关紧要。所以，kgpooyamlall相当于kgpoalloyaml。

您不需要将所有组件用于别名。例如k，kg，klo，ksys，或者kgpo是有效的别名也。此外，您可以在命令行中将别名与其他单词组合使用。

例如，您可以k proxy用于运行kubectl proxy：

![img{512x368}](../../assets/09d9de9dfab58796.png)


或者您可以kg roles用于运行kubectl get roles（目前不存在Roles资源的别名组件）：

![img{512x368}](../../assets/eb4eed881766480b.png)


要获取特定Pod，您可以使用kgpo my-pod以运行kubectl get pod my-pod：

![img{512x368}](../../assets/93d7be5613a00d18.png)


请注意，某些别名甚至需要在命令行上的进一步参数。例如，kgpol别名代表kubectl get pods -l。该-l选项需要一个参数（标签规范）。所以，你必须使用这个别名，例如，像这样:

![img{512x368}](../../assets/1e803236df6f407a.png)


出于这个原因，你可以使用a，f以及l只在一个别名的结尾部分。


一般来说，一旦你掌握了这个方案，就可以直观地从你想要执行的命令中推断出别名，并节省大量的输入！

### 安装

要安装kubectl-别名，你只需要下载[.kubectl-aliases](https://raw.githubusercontent.com/ahmetb/kubectl-aliases/master/.kubectl_aliases)GitHub文件，并在你的~/.bashrc或~/.zshrc文件生效它：

```
source ~/.kubectl_aliases
```


重新加载shell后，您应该能够使用所有800个kubectl别名！

### 命令完成

如您所见，您经常在命令行上向别名添加更多单词。例如：

```
$kgpooyaml test-pod-d4b77b989
```


如果你使用kubectl命令完成，那么你可能习惯于自动完成资源名称之类的事情。但是当你使用别名时，你还可以这样做吗？

这是一个重要的问题，因为如果它不起作用，那将消除这些别名的一些好处！

答案取决于您使用的shell。

对于Zsh，完成对于别名是开箱即用的。

不幸的是，对于Bash，默认情况下，对于别名，完成功能不起作用。好消息是它可以通过一些额外的步骤来完成。下一节将介绍如何执行此操作。

### 在Bash中启用别名的完成

Bash的问题在于它尝试在别名上尝试完成（每当你按Tab键），而不是在别名命令（如Zsh）上。由于您没有所有800个别名的完成脚本，因此不起作用。

[complete-alias](https://github.com/cykerway/complete-alias)项目提供了解决这个问题的通用解决方案。它使用别名的完成机制，在内部将别名扩展到别名命令，并返回扩展命令的完成建议。这意味着，它使别名的完成行为与别名命令完全相同。

在下文中，我将首先解释如何安装complete-alias，然后如何配置它以启用所有kubectl别名的完成。

#### 安装complete-alias

首先，complete-alias依赖于[bash-completion](https://github.com/scop/bash-completion)。因此，您需要确保在安装complete-alias之前安装了bash-completion。早先已经为Linux和macOS提供了相关说明。

对于macOS用户的重要注意事项：与kubectl完成脚本一样，complete-alias不适用于Bash 3.2，这是macOS上Bash的默认版本。特别是，complete-alias依赖于bash-completion v2（brew install bash-completion@2），它至少需要Bash 4.1。这意味着，要在macOS上使用complete-alias，您需要安装较新版本的Bash。


要安装complete-alias，您只需bash_completion.sh从GitHub存储库下载脚本，并将其在您的~/.bashrc文件中source：

```
source ~/bash_completion.sh
```


重新加载shell后，应正确安装complete-alias。

#### 启用kubectl别名的完成

从技术上讲，complete-alias提供了_complete_aliasshell函数。此函数检查别名并返回别名命令的完成建议。

要将其与特定别名挂钩，您必须使用completeBash内置来设置别名_complete_alias的完成功能。

举个例子，我们k来看一下代表kubectl命令的别名。要设置_complete_alias此别名的完成功能，您必须执行以下命令：

```
$complete -F _complete_alias k
```


这样做的结果是，无论何时在k别名上自动完成，_complete_alias都会调用该函数，该函数检查别名并返回kubectl命令的完成建议。

作为另一个例子，让我们采用kg代表的别名kubectl get：

```
$complete -F _complete_alias kg
```


同样，这样做的结果是，当您自动完成时kg，您将获得与之相同的完成建议kubectl get。

请注意，可以以这种方式对系统上的任何别名使用complete-alias。


因此，要启用所有 kubectl别名的完成，您只需为每个别名运行上述命令。以下代码片段完全相同（假设您安装了kubectl-aliases ~/.kubectl-aliases）：

```
for _a in $(sed '/^alias /!d;s/^alias //;s/=.*$//' ~/.kubectl_aliases); do
complete -F _complete_alias "$_a"
done
```


只需将此片段添加到您的~/.bashrc文件中，重新加载您的shell，现在您应该可以使用所有800 kubectl别名的完成！

## 6. 使用插件扩展kubectl

从[版本1.12](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.12.md#sig-cli-1)开始，kubectl包含一个[插件机制](https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/)，允许您使用自定义命令扩展kubectl。

以下是kubectl插件的示例，可以调用为kubectl hello：

```
$ kubectl hello
Hello, I'm a kubectl plugin!
```


kubectl插件机制将严格遵循Git插件机制的设计。


本节将向您展示如何安装插件，您可以在哪里找到现有的插件，以及如何创建自己的插件。

#### 安装插件

Kubectl插件作为简单的可执行文件分发，其名称的形式为kubectl-x。前缀kubectl-是必需的，接下来是允许调用插件的新kubectl子命令。

例如，上面显示的hello插件将作为名为的文件分发kubectl-hello。

要[安装插件](https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/#installing-kubectl-plugins)，您只需将kubectl-x文件复制到您的任何目录中PATH并使其可执行（例如，使用chmod +x）。之后，您可以立即调用该插件kubectl x。

您可以使用以下命令列出系统上当前安装的所有插件：

```
$kubectl plugin list
```


如果您有多个具有相同名称的插件，或者存在不可执行的插件文件，则此命令还会显示警告。

### 使用krew查找和安装插件

Kubectl插件可以像软件包一样共享和重用。但是在哪里可以找到其他人共享的插件？

该[krew项目](https://github.com/GoogleContainerTools/krew)旨在提供一个统一的解决方案，共享，查找，安装和管理kubectl插件。该项目将自己称为“kubectl插件的包管理器”（名称krew是brew的提示）。

Krew 以kubectl[插件索引](https://github.com/GoogleContainerTools/krew-index)为中心，您可以从中选择和安装。

```
$ kubectl krew search | less
$ kubectl krew search view
$ kubectl krew info view-utilization
$ kubectl krew install view-utilization
$ kubectl krew list
```


如您所见，krew本身是一个kubectl插件。这意味着，安装krew本质上就像安装任何其他kubectl插件一样。您可以在[GitHub页面](https://github.com/GoogleContainerTools/krew/#installation)上找到krew的详细安装说明。

最重要的krew命令如下：

```
# Search the krew index (with an optional search query)
$ kubectl krew search [<query>]
# Display information about a plugin
$ kubectl krew info <plugin>
# Install a plugin
$ kubectl krew install <plugin>
# Upgrade all plugins to the newest versions
$ kubectl krew upgrade
# List all plugins that have been installed with krew
$ kubectl krew list
# Uninstall a plugin
$ kubectl krew remove <plugin>
```


请注意，使用krew安装插件并不妨碍以传统方式安装插件。即使你使用krew，你仍然可以通过其他方式安装你在其他地方找到的插件（或自己创建）。

请注意，该kubectl krew list命令仅列出已使用krew安装的插件，而该kubectl plugin list命令列出了所有插件，即使用krew安装的插件和以其他方式安装的插件。


### 在其他地方寻找插件

Krew仍然是一个年轻的项目，目前[krew索引](https://github.com/GoogleContainerTools/krew-index/)中只有大约30个插件。如果你在那里找不到你需要的东西，你可以在其他地方寻找插件，例如，在GitHub上。

我建议查看[kubectl-plugins GitHub主题](https://github.com/topics/kubectl-plugins)。你会发现有几十个可用的插件值得一看。

### 创建自己的插件

当然，您可以[创建自己的kubectl插件](https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/#writing-kubectl-plugins)，这很容易实现。

您只需创建一个可执行文件，执行您想要的操作，为其命名kubectl-x，然后按上述方法安装它。

可执行文件可以是任何类型，Bash脚本，编译的Go程序，Python脚本，它确实无关紧要。唯一的要求是它可以由操作系统直接执行。

我们现在创建一个示例插件。在上部分中，您使用kubectl命令列出每个pod的容器镜像。您可以轻松地将此命令转换为可以调用的插件，比如说kubectl img。

为此，只需创建一个名为kubectl-img以下内容的文件：

```
#!/bin/bash
kubectl get pods -o custom-columns='NAME:metadata.name,IMAGES:spec.containers[*].image'
```


现在使文件可执行，chmod +x kubectl-img并将其移动到您的任何PATH中的目录。之后，您可以立即开始使用该插件kubectl img！

如上所述，kubectl插件可以用任何编程语言或脚本语言编写。如果使用shell脚本，则可以从插件轻松调用kubectl。但是，您可以使用实际编程语言编写更复杂的插件，例如，使用

[Kubernetes客户端库]。如果使用[Go]，您还可以使用[cli-runtime库]，它专门用于编写kubectl插件。

### 分享你的插件

如果您认为其中一个插件可能对其他人有用，请随时在GitHub上分享。确保将其添加到[kubectl-plugins主题](https://github.com/topics/kubectl-plugins)中，以便其他人可以找到它。

您还可以请求将您的插件添加到[krew索引](https://github.com/GoogleContainerTools/krew-index/)中。您可以在[krew GitHub存储库](https://github.com/GoogleContainerTools/krew/blob/master/docs/DEVELOPER_GUIDE.md)中找到有关如何执行此操作的说明。

### 命令完成

目前，插件机制遗憾的是还不支持命令完成。这意味着您需要完全键入插件名称以及插件的任何参数。

但是，在kubectl GitHub存储库中有一个处于open状态的[功能请求issue](https://github.com/kubernetes/kubectl/issues/585)。因此，此功能有可能在将来的某个时间得到实现。

以上就是有关kubectl高效使用的所有内容了！

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