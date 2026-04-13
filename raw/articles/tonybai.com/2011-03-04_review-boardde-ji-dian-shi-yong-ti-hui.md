---
title: Review Board的几点使用体会
url: https://tonybai.com/2011/03/04/some-experience-on-using-review-board/
published: '2011-03-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Review Board的几点使用体会

近期产品线研发体系正式将[Review Board](http://tonybai.com/2009/09/19/review-board-installation-and-configuration/)这款优秀的基于Web的[代码评审](http://tonybai.com/2006/05/31/code-review-is-necessary/)开源工具引入到开发过程中，作为产品线内各项目组进行代码评审的辅助工具。我对Review Board近两年多的关注总算没有白费，算是有了一个还算不错的结果。不过Review Board的正式使用并不代表一种结束，反而恰恰是一个新的开始。我们下一步要关注的是如何用好Review Board，让它真真正正地为改善产品质量和开发效率出力。

在“[关于在线代码评审的几点考量](http://tonybai.com/2010/12/18/thoughts-on-online-coding-review/)”这篇博文中我提到了在线代码评审工具在开发过程中所处的角色、使用时机以及使用时的注意事项，不过当时也多是凭直觉有感而发。真正用了Review Board这样的评审工具后，有些想法还要进一步细化。

的确，我们在近一个多月的使用过程中发现了许多问题，在公司内部我把这些问题以及解决方法整理成了一页Wiki Page放到了产品线的知识库中，这里我也和大家分享一下。

下面是我整理的关于如何用好Review Board的一个Tips列表：

* 务必保持每个Review Request内容的内聚性

如果你提交一个Review Request，其中包含了对A库的bugfix，给B库增加一个新feature，以及对C库重构的一段代码，那你的这个Review Request就是不合格的。该Request内容上包含了三个不相干的内容，严重缺乏内聚，这会给后续评审带来不良影响，诸如评审者关注点分散，效率下降；评审者不愿理睬这种Request等等。对于上述的问题Request，建议拆分为三个Request，让每个Request内容单一内聚。

* 请为你的Review Request设定评审结束时间

切记为每个Review Request设定一个有效评审时间范围，否则你的评审将被视为永远有效，这样的Request久而久之就会变成"塑料制品垃圾"塞满你的Dashboard。由于Review Board上似乎没有设定评审截止时间的位置，所以一般可在Description中增加该Request对应的评审结束时间，例如加上：

"评审截止时间：2011-03-07 12:00"

* 保持你的Dashboard Clean，别忘了关闭你的Review Request

使用Review Board一段时间后，你就会发现你的Dashboard中有很多Incoming和Outgoing的 Requests，让人心生不悦。建议大家在Request评审完毕或过期后关闭你发起的Request，保持Dashboard的clean。

在每个Request里有一个close标签，下面有三个选项：

- summited 表示评审结束，代码已经提交，不须继续评审

- discarded 丢弃的评审请求

- delete permanently 应该删除的请求

一般我们会用到summited。

* 请为评审请求选择适当的干系人列表

每个评审请求都应该有特定的干系人列表，不要泛泛的发给Review Board系统中设定的所有Group。否则你既不会收到那些不相干人的有效的评审，还干扰了对方的工作。

一般来说发起代码评审请求前先要明确此次评审的目的，无非以下几种或它们的组合：

- 希望相关干系人找出代码中的代码逻辑缺陷；

- 希望相关干系人找出代码中的业务逻辑缺陷；

- 分享你的代码，将你的代码中的美展现给大家。

明确了目的之后，想必你就应该清楚干系人列表中究竟该有谁了。

* 请评审者聚焦本次Request中的变动

在Review Board实际使用过程中，常常发现这样的情况：某位同事发起一段针对遗留代码修改的评审请求。很多评审者给出的一些评审意见针对的却并非是本次修改的代码，而是此次变更源码文件中的其他代码。这样可能会导致下面两个问题：

- 提交Request的评审人很可能无法修正非本Request之外的代码问题；

- 评审过程可能因此被拉长，很可能无法在截止时间内完成此次评审，甚至可能反复多次，造成效率上的浪费。

针对这种情况，我们建议评审者聚焦本次改动。如果评审过程中发现其他非本次改动相关的问题，可通过向代码所在的项目的Todolist或某种问题跟踪系统提交一个issue/ticket，后续由该项目的主维护者统一安排处理。

最后说说[post-review](http://www.reviewboard.org/docs/manual/1.5/users/tools/post-review/)这个工具的使用。Review Board的原理其实就是评审diff文件。一般情况下大家通过Review Board提供的web页面提交自己手动生成的diff文件，这种方法无可厚非。不过Review Board官方还推荐使用另外一种更有效率的方法，那就是使用post-review脚本发起Review Request。以下内容描述了工作中常见的三种使用post-review工具的情形，前提是你已经将post-review安装到你的主机上了。

* 在代码Commit前发起评审请求

有些时候，项目要求代码未经评审不允许commit到Code Repository中，这种情况我们称之为pre-commit review。这种情况下可以这样来发起一个Review Request，先在你的本地代码库拷贝中完成对代码的修改，然后进入到你的本地代码目录，执行：

post-review –server=http://xxx.xxx.xxx.xxx/reviews

post-review就会将当前目录以及其子目录下所有变更作为一个diff提交到Review Board形成一个Request Draft等待你的发布。当然你也可以通过post-review直接设定Request的Descripton等字段，并可通过增加–publish参数立刻发布该Request。

* 代码commit后发起评审请求

有些时候，某些代码是在提交到Code Repository后才评审的，这种情况我们称之为post-commit review。我们可通过版本库的revision number间的差异来构造Review Request，具体方法如下：

post-review –server=http://xxx.xxx.xxx.xxx/reviews –revision-range=n:m –branch=YOUR_REPOSITORY_PATH

当然你也可以不指定–branch，不过需要在你本地代码库拷贝目录下执行post-review。

* 更新已存在的评审请求

已经提交到Review Board的请求经过评审后，可能需要你再次修改代码并更新diff文件以继续评审。这时你可以通过指定已存在的Review Request id的方式更新已存在Request的diff，方法如下：

post-review –server=http://xxx.xxx.xxx.xxx/reviews ….. –review-request-id=58

注意，如果你的unix/linux账户下设置了http_proxy环境变量，那么在执行post-review之前需要将http_proxy设置为空，否则post-review的请求将被代理拦截而失败。

部门里越来越多的人开始关注和使用Review Board了，好趋势，可喜可贺！

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论