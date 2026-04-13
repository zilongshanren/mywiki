---
title: 图解git原理的几个关键概念
url: https://tonybai.com/2020/04/07/illustrated-tale-of-git-internal-key-concepts/
published: '2020-04-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 图解git原理的几个关键概念

![img{512x368}](../../assets/1ce374118ab9c2e9.png)


[git](https://git-scm.com/)是那个“爱骂人”的[Linux](https://www.kernel.org/)之父[Linus Torvalds](https://github.com/torvalds)继Linux内核后奉献给全世界程序员的第二个礼物（不能确定已经逐渐老去的Torvalds能否迸发第三春，第三次给我们一个超大惊喜^_^）。这里再强调一下，git读作**/git/**，而不是**/dʒit/**。

在诞生十余载后(2005年发布第一版)，**git**毫无争议地成为了程序员版本管理工具的首选，它改变了全世界程序员的**代码版本管理和生产协作的模式**，极大促进了开源软件运动的发展。进化到今天的**git**已经成为了一个比较复杂的工具，多数程序员都将目光聚焦在如何记住这些命令并用好这些命令，对这些复杂命令行背后的原理却知之不多，虽然大多数程序员的确不太需要深刻了解git背后的原理^_^。

关于git原理的文章在互联网上也呈现出“汗牛充栋”之势，有些文章“蜻蜓点水”，有些文章“事无巨细”，看后似乎都无法让我满意。结合自己对git原理的学习，我觉得多数人把握住**git运作机制**的几个关键概念即可，于是就有了这篇文章，我努力尝试给大家讲清楚。

## 一. 我就是仓库，**我拥有全部**

我们首先要明确一个git与先前的版本管理工具（主要是[subversion](https://subversion.apache.org/)）的不同。下面是使用[subversion](https://tonybai.com/tag/svn)版本管理工具时，程序员进行代码生产以及程序员间围绕代码仓库进行协作的模式：

![img{512x368}](../../assets/2feb0483de7b7259.png)


众所周知，subversion是**基于中心版本仓库进行版本管理协作的版本管理工具**。就像上图中那样，所有开发人员开始生产代码的前提是**必须先从中心仓库checkout一份代码拷贝到自己本地的工作目录**；而进行版本管理操作或者与他人进行协作的前提也是：**中心版本仓库必须始终可用**。这有点像以太网的“半双工的集线器(hub)模式”：svn中心仓库就像集线器本身，每个程序员节点就像连接到集线器上的主机；当一个程序员提交(commit)代码到中心仓库时，其他程序员不能提交，否则会出现冲突；如果中心仓库挂掉了，那么整个版本管理过程也将停止，程序员节点间无法进行协作，这就像集线器(hub)挂掉后，所有连接到hub上的主机节点间的网络也就断开无法相互通信一样。

如果我们使用git，我们是**不需要“集线器”**的：

![img{512x368}](../../assets/eeb7dba2c981186c.png)


如上图所示，git号称分布式版本管理系统，本质上是没有像subversion中那个所谓的“中心仓库”的。**每个程序员都拥有一个本地git仓库**，而不仅仅是一份代码拷贝，这个仓库就是一个**独立的版本管理节点**，它拥有程序员进行代码生产、版本管理、与其他程序员协作的**全部信息**。即便在一台没有网络连接的机器上，程序员也能利用该仓库完成代码生产和版本管理工作。在网络ready的情况下，任意两个git仓库之间可以进行点对点的协作，这种协作无需中间协调者(中心仓库)参与。

## 二. github实现了基于git网络协作的**控制平面**

git实现了分布式版本管理系统，每个git仓库节点都是自治的。诸多git仓库节点一起形成了一个**分布式git版本管理网络**。这样的一个分布式网络存在着与普通分布式系统的类似的问题：如何发现对端节点的git仓库、如何管理和控制仓库间的访问权限等。如果说linus的git本身是这个分布式网络的数据平面工具(实现client/server间的双向数据通信)，那么这个分布式网络还缺少一个**“控制平面”**。

而[github](https://github.com)恰恰给出了一份git分布式网络控制平面的实现：托管、发现、控制…。其名称中含有的“hub”字样让我们想起了上面的“hub模式”：

![img{512x368}](../../assets/24c9732d211bb2cf.png)


我们看到在github的git协作模式实践中，引入了“中心仓库”的概念，各个程序员的节点git仓库源于(clone于)中心仓库。但是它和subversion的“中心仓库”有着本质的不同，这个仓库只是一个“upstream”库、是一个权威库。它并不是“集线器”，也没有按照“集线器”的那种工作模式进行协作。所有程序员节点的代码生产和版本管理操作完全可以脱离该所谓“中心库”而独立实施。

## 三. **objects**是个筐，什么都往里面装

上面都是从“宏观”谈git的一些与众不同的理念，而git原理，其实是从这一节才真正开始的^_^。

我们知道：每个git仓库的所有数据都存储在仓库顶层路径下的**.git**目录下：

```
$tree -L 1 -F
.
├── COMMIT_EDITMSG
├── HEAD
├── config
├── description
├── hooks/
├── index
├── info/
├── logs/
├── objects/
└── refs/
5 directories, 5 files
```


而在这些目录和文件中，又以**objects**路径下的数据内容最多，也最为重要。在git的设计中，**objects目录就是一个“筐”，git的核心对象(object)都往里面“装”**。

![img{512x368}](../../assets/477889c2dd143ea5.png)


从上图中，我们看到objects中存储的最主要的有三类对象：blob、commit和tree。这时你可能还不知道它们究竟是啥。不过没关系，我们通过一个例子来做一下“对号入座”。

我们在一个目录下建立git-internal-repo-demo目录，进入该目录，执行下面命令创建一个git仓库：

```
➜ /Users/tonybai/test/git/git-internal-repo-demo git:(master) ✗ $git init .
Initialized empty Git repository in /Users/tonybai/Test/git/git-internal-repo-demo/.git/
```


这是一个处于初始状态的git仓库，我们看看存储git仓库数据的**.git**目录下的结构：

```
➜ /Users/tonybai/test/git/git-internal-repo-demo git:(master) $tree .git
.git
├── HEAD
├── config
├── description
├── hooks
│ ├── applypatch-msg.sample
│ ├── commit-msg.sample
│ ├── fsmonitor-watchman.sample
│ ├── post-update.sample
│ ├── pre-applypatch.sample
│ ├── pre-commit.sample
│ ├── pre-push.sample
│ ├── pre-rebase.sample
│ ├── pre-receive.sample
│ ├── prepare-commit-msg.sample
│ └── update.sample
├── info
│ └── exclude
├── objects
│ ├── info
│ └── pack
└── refs
├── heads
└── tags
8 directories, 15 files
```


这个时候，**objects这个筐还是空的**！我们这就为仓库添点内容：

```
$mkdir -p cmd/demo
在cmd/demo目录下添加main.go文件，内容如下:
// cmd/demo/main.go
package main
import "fmt"
func main() {
fmt.Println("hello, git")
}
```


接下来我们使用git add将cmd/demo目录加入到stage区：

```
$git add .
$git status
On branch master
No commits yet
Changes to be committed:
(use "git rm --cached <file>..." to unstage)
new file: cmd/demo/main.go
```


这时我们来看一下objects这个筐是否有变化：

```
├── objects
│ ├── 3e
│ │ └── 759ef88951df9b9b07077a7ec01f96b8e659b3
│ ├── info
│ └── pack
```


我们有一个object已经被装入到“筐”中了。我们看到objects目录下是一些以哈希值命名的文件和目录，其中目录由两个字符组成，是每个object hash值的前两个字符。hash值后续的字符串用于命名对应的object文件。在这里我们的object的hash值(实质是sha-1算法)为3e759ef88951df9b9b07077a7ec01f96b8e659b3，于是这个对象就被放入名为3e的目录下，对应的object文件为759ef88951df9b9b07077a7ec01f96b8e659b3。

我们使用git提供的**低级命令**查看一下这个object究竟是什么，其中git cat-file -t查看object的类型，git cat-file -p查看object的内容：

```
$git cat-file -t 3e759ef889
blob
$git cat-file -p 3e759ef889
package main
import "fmt"
func main() {
fmt.Println("hello, git")
}
```


我们看到objects这个筐中多了一个blob类型的对象，对象内容就是前面main.go文件中内容。

接下来，我们提交一下这次变更：

```
$git commit -m"first commit" .
[master (root-commit) 3062e0e] first commit
1 file changed, 7 insertions(+)
create mode 100644 cmd/demo/main.go
```


再来看看**.git/objects**中的变化：

```
├── objects
│ ├── 1f
│ │ └── 51fe448aacc69c0f799def9506e61ed3eb60fa
│ ├── 30
│ │ └── 62e0ebad9415b704e96e5cee1542187b7ed571
│ ├── 3d
│ │ └── 2045367ea40c098ec5c7688119d72d97fb09a5
│ ├── 3e
│ │ └── 759ef88951df9b9b07077a7ec01f96b8e659b3
│ ├── 40
│ │ └── 6d08e1159e03ae82bcdbe1ad9f076a04a41e2b
│ ├── info
│ └── pack
```


我们看到筐里被一下子新塞入4个object。我们分别看看新增的4个object类型和内容都是什么：

```
$git cat-file -t 1f51fe448a
tree
$git cat-file -p 1f51fe448a
100644 blob 3e759ef88951df9b9b07077a7ec01f96b8e659b3 main.go
$git cat-file -t 3062e0ebad
commit
$git cat-file -p 3062e0ebad
tree 406d08e1159e03ae82bcdbe1ad9f076a04a41e2b
author Tony Bai <bigwhite.cn@aliyun.com> 1586243612 +0800
committer Tony Bai <bigwhite.cn@aliyun.com> 1586243612 +0800
first commit
$git cat-file -t 3d2045367e
tree
$git cat-file -p 3d2045367e
040000 tree 1f51fe448aacc69c0f799def9506e61ed3eb60fa demo
$git cat-file -t 406d08e115
tree
$git cat-file -p 406d08e115
040000 tree 3d2045367ea40c098ec5c7688119d72d97fb09a5 cmd
```


这里我们看到了另外两种类型的object被加入“筐”中：commit和tree类型。objects这个筐里目前有了5个object，我们不考虑git是以何种格式存储这些object的，我们想知道的是这几个object的关系是什么样的。请看下一小节^_^。

## 四. 每个**commit**都是一个git仓库的快照

要理清objects“筐”中各object间的关系，就必须要把握住一个关键概念：“每个**commit**都是git仓库的一个快照” – 以一个commit为入口，我们能将当时objects下面的所有object联系在一起。因此，上面5个object中的那个commit对象就是我们分析各object关系的入口。我们根据上述5个object的内容将这5个object的关系组织为下面这幅示意图：

![img{512x368}](../../assets/0ea75e1094023a2c.png)


通过上图我们看到：

-
commit是对象关系图的入口；

-
tree对象用于描述目录结构，每个目录节点都会用一个tree对象表示。目录间、目录文件间的层次关系会在tree对象的内容中体现；

-
每个commit都会有一个root tree对象；

-
blob对象为tree的叶子节点，它的内容即为文件的内容。


上面仅是一次commit后的关系图，为了更清晰的看到多个commit对象之间关系，我们再来对git repo进行一次变更提交:

```
我们创建pkg/foo目录：
$mkdir -p pkg/foo
然后创建文件pkg/foo/foo.go，其内容如下：
// pkg/foo/foo.go
package foo
import "fmt"
func Foo() {
fmt.Println("this is foo package")
}
```


提交这次变更：

```
$git add pkg
$git commit -m"add package foo" .
[master 6f7f08b] add package foo
1 file changed, 7 insertions(+)
create mode 100644 pkg/foo/foo.go
```


下面是提交变更后的“筐”内的对象：

```
$tree objects
objects
├── 1f
│ └── 51fe448aacc69c0f799def9506e61ed3eb60fa
├── 29
│ └── 3ae375dcef1952c88f35dd4d2a1d4576dea8ba
├── 30
│ └── 62e0ebad9415b704e96e5cee1542187b7ed571
├── 3d
│ └── 2045367ea40c098ec5c7688119d72d97fb09a5
├── 3e
│ └── 759ef88951df9b9b07077a7ec01f96b8e659b3
├── 40
│ └── 6d08e1159e03ae82bcdbe1ad9f076a04a41e2b
├── 65
│ └── 5dd3aae645813dc53834ebfa8d19608c4b3905
├── 6e
│ └── e873d9c7ca19c7fe609c9e1a963df8d000282b
├── 6f
│ └── 7f08b14168beb114c3cc099b8dc1c09ccd4739
├── cc
│ └── 9903a33cb99ae02a9cb648bcf4a71815be3474
├── info
└── pack
12 directories, 10 files
```


object已经多到不便逐一分析了。但我们把握住一点：**commit是分析关系的入口**。我们通过commit的输出或commit log(git log)可知，新增的commit对象的hash值为6f7f08b141。我们还是以它为入口分析新增object的关系以及它们与之前已存在的object的关系：

![img{512x368}](../../assets/974ef1833b5aed81.png)


从上图我们看到：

-
git新创建tree对象对应我们新建的pkg目录以及其子目录；

-
cmd目录下的子目录和文件内容并未改变，因此这次commit所对应的root tree对象(293ae375dc)直接使用了已存在的cmd目录对应的对象(3d2045367e);

-
新commit对象会将第一个commit对象作为parent，这样多个commit对象之间构成一个单向链表。


上面的两个提交都是新增内容，我们再来提交一个commit，这次我们对已有文件内容做变更：

```
将cmd/demo/main.go文件内容变更为如下内容：
// cmd/demo/main.go
package main
import (
"fmt"
"github.com/bigwhite/foo"
)
func main() {
fmt.Println("hello, git")
foo.Foo()
}
提交变更：
$git commit -m"call foo.Foo in main" .
[master 2f14635] call foo.Foo in main
1 file changed, 6 insertions(+), 1 deletion(-)
```


和上面的分析方法一样，我们通过最新commit对应的hash值2f146359b4对新对象和现存对象的关系进行分析：

![img{512x368}](../../assets/3acf2bbbaec5ca92.png)


如上图，第三次变更提交后，我们看到：

-
由于main.go文件变更，git重建了main.go blob对象、demo、cmd tree对象

-
由于pkg目录、其子目录布局、子目录下文件内容没有改变，于是新commit对象对应的root tree对象直接“复用”了上一次commit的pkg tree对象。

-
新commit对象加入commit对象单向链表，并将上一次的commit对象作为parent。


我们看到沿着最新的commit对象(2f146359b4)，我们能获取当前仓库的最新结构布局以及各个blob对象的最新内容，即最新的一个快照！

## 五. object是不可变的，默克尔树(Merkle Tree)判断变化

从上面的三次变更，我们看到无论哪种对象object，**一旦放入到objects这个“筐”就是不可变的(immutable)**。即便是第三次commit对main.go进行了修改，git也只是根据main.go的最新内容**创建一个新的blob对象**，而不是修改或替换掉第一版main.go对应的blob对象。

对应目录的tree object亦是如此。如果某目录下的二级目录发生变化或目录下的文件内容发生改变，git会新生成一个对应该目录的tree对象，而不是去修改原先已存在的tree对象。

实际上，git tree对象的组织本身就是一棵[默克尔树(Merkle Tree)](http://en.wikipedia.org/wiki/Merkle_tree)。

默克尔树是一类基于哈希值的二叉树或多叉树，其叶子节点上的值通常为数据块的哈希值，而非叶子节点上的值，是将该节点的所有孩子节点的组合结果的哈希值。默克尔树的特点是，底层数据的任何变动，都会传递到其父亲节点，一直到树根。

![img{512x368}](../../assets/14fc988f751b7a36.png)


以上图为例：我们自下向上看，D0、D1、D2和D3是叶子节点包含的数据。N0、N1、N2和N3是叶子节点，它们是将数据（也就是D0、D1、D2和D3）进行hash运算后得到的hash值；继续往上看，N4和N5是中间节点，N4是N0和N1经过hash运算得到的哈希值，N5是N2和N3经过hash运算得到的哈希值。（注意，hash值计算方法：把相邻的两个叶子结点合并成一个字符串，然后运算这个字符串的哈希）。最后，Root节点是N4和N5经过hash运算后得到的哈希值，这就是这颗默克尔树的根哈希。当N0包含的数据发生变化时，根据默克尔树的节点hash值形成机制，我们可以快速判断出：**N0、N4和root节点会发生变化**。

对应git来说，叶子节点对应的就是每个文件的hash值，tree对象对应的是中间节点。因此，通过默克尔树(Merkle Tree)的特性，我们可以快速判断哪些对象对应的目录或文件发生了变化，应该重新创建对应的object。我们还以上面的第三次commit为例：

![img{512x368}](../../assets/96d47f36c8c85217.png)


如上图所示，第三次commit是因为cmd/demo/main.go内容发生了变化，根据merkle tree特性，我们可以快速判断红色的object会随之发生变化。于是git会自底向上逐一创建这些新对象：main.go文件对应的blob对象以及demo、cmd以及根节点对应的tree对象。

## 六. branch和tag之所以轻量，因为它们都是“指针”

使用subversion时，创建branch或打tag使用的是svn copy命令。svn copy执行的就是真实的文件拷贝，相当于将trunk下的目录和文件copy一份放到branch或tag下面，建立一个trunk的副本，这样的操作绝对是“超重量级”的。如果svn仓库中的文件数量庞大且size很大，那么svn copy执行起来不仅速度慢，而且还会在svn server上占用较大的磁盘存储空间，因此使用svn时，打tag和创建branch是要“谨慎”的。

而git的branch和tag则极为轻量，我们来给上面例子中的仓库创建一个dev分支：

```
$git branch dev
```


我们看看.git下有啥变化：

```
.
└── refs
├── heads
│ ├── dev
│ └── master
└── tags
```


我们看到.git/refs/heads下面多出了一个dev文件，我们查看一下该文件的内容：

```
$cat refs/heads/dev
2f146359b475909f2fdcdef046af3431c8077282
$git log --oneline
2f14635 (HEAD -> master, dev) call foo.Foo in main
6f7f08b add package foo
3062e0e first commit
```


对比发现，dev文件中的内容恰是最新的commit对象：2f146359b475909f2fdcdef046af3431c8077282。

我们再来给repo打一个tag：

```
$git tag v0.0.1
```


同样，我们来查看一下.git目录下的变化：

```
└── refs
├── heads
│ ├── dev
│ └── master
└── tags
└── v0.0.1
```


我们看到在refs/tags下面增加一个名为v0.0.1的文件，查看其内容：

```
$cat refs/tags/v0.0.1
2f146359b475909f2fdcdef046af3431c8077282
```


和dev分支文件一样，它的内容也是最新的commit对象：2f146359b475909f2fdcdef046af3431c8077282。

可见，使用git创建分支或tag仅仅是创建了一个指向某个commit对象的**“指针”**，这与subversion的副本操作相比，简直不能再轻量了。

前面说过，一个commit对象都是一个git仓库的快照，切换到(git checkout xxx)某个branch或tag，就是将本地工作拷贝切换到commit对象所代表的仓库快照的状态。当然也会将commit对象组成的单向链表的head指向该commit对象，这个head即.git/HEAD文件的内容。

## 七. 小结

到这里，git原理的几个关键概念就交代完了，再回顾一下：

-
和subversion这样的集中式版本管理工具最大的不同就是每个程序员节点都是git仓库，拥有全部开发、协作所需的全部信息，完全可以脱离“中心节点”；

-
如果说git聚焦于数据平面的功能，那么github则是一个基于git网络协作的

**控制平面**的实现； -
**objects**是个筐，什么都往里面装。git仓库的核心数据都存在.git/objects下面，主要类型包括：blob、tree和commit； -
每个

**commit**都是一个git仓库的快照，记住commit对象是分析对象关系的入口; -
git是基于数据内容的hash值做等值判定的，object是不可变的，默克尔树(Merkle Tree)用来快速判断变化。

-
branch和tag因为是“指针”，因此创建、销毁和切换都非常轻量。


## 八. 参考资料

-
[Pro Git v2](https://git-scm.com/book/en/v2)– https://git-scm.com/book/en/v2 -
[git介绍](https://www.cnblogs.com/kisun168/p/11408346.html)– https://www.cnblogs.com/kisun168/p/11408346.html -
[git内部原理](https://zhuanlan.zhihu.com/p/53750883)– https://zhuanlan.zhihu.com/p/53750883 -
[git仓库内部结构](https://www.jianshu.com/p/72f9f8c9c47e)– https://www.jianshu.com/p/72f9f8c9c47e

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

很清晰

感谢博主，文章简单易懂，真的很棒。

清晰深刻，谢谢！

感谢白大，非常直观清晰