---
title: Go是如何缓解供应链攻击的[译]
url: https://tonybai.com/2022/04/02/how-go-mitigates-supply-chain-attacks/
published: '2022-04-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go是如何缓解供应链攻击的[译]

![](../../assets/6863ab21378e5e29.png)


[本文永久链接](https://tonybai.com/2022/04/02/how-go-mitigates-supply-chain-attacks) – https://tonybai.com/2022/04/02/how-go-mitigates-supply-chain-attacks

这些年来，关于软件供应链的安全问题频发，软件供应链已然成为IT安全领域的一个热点，在前不久的[《聊聊Go语言的软件供应链安全》](https://mp.weixin.qq.com/s/qo6wiRIJHyO5vgAJrQFfuw)一文中我曾提到过Go在SBOM(软件物料清单)方面给开发人员带来的方便。这两天Go官博又发表了一篇由Go项目安全负责人[Filippo Valsorda](https://filippo.io/)撰写的文章[《How Go Mitigates Supply Chain Attacks》](https://go.dev/blog/supply-chain)，系统总结了Go语言应对软件供应链方面攻击的“防护秘笈”。笔者觉得文章中提到的这些点是每个Gopher都应该知道的必备知识，于是这里将文章做简单翻译，供大家参考。

现代软件工程基于相互协作，并以重用开源软件为基础。但这也使软件项目成为了供应链攻击的目标，攻击方式就是破坏软件项目的依赖(dependencies)。

尽管知道这些，为了完成项目，我们需要依赖，我们会采取一些流程或技术措施在项目与依赖之间建立一种信任关系。好在，Go的工具链与设计可以帮助我们降低各个阶段的风险。

### 所有构建都是被“锁定(locked)”的

外部世界的变化，比如项目的某个依赖发布了一个新版本，是不会影响到Go的构建的。

与其他大多数软件包管理器(package manager)所使用的配置文件不同，Go module没有将存储约束列表的文件和锁定特定版本的lock文件分开管理，对任何Go构建作出贡献的每个依赖项的版本完全由main module的go.mod文件决定。

从[Go 1.16版本](https://mp.weixin.qq.com/s/UPNn4G_m0zfvJgWxEVl_Tw)开始，Go命令默认按照这种确定性执行，[如果go.mod不完整，构建命令（go build, go test, go install, go run, …）将失败](https://go.dev/ref/mod#go-mod-file-updates)。唯一可以改变go.mod文件（当然构建也会随之改变）的命令是go get和go mod tidy。这两个命令通常不会自动运行或在CI中运行，所以对依赖树的改变必须是主观故意的，我们可以在操作前对这种改变做代码评审。

这对安全非常重要，因为当CI系统或新机器运行时，签入(checked-in)的源码是最终的和完整的，代码将说明什么会被构建，第三方没有办法影响它。

此外，当用go get添加新依赖时，由于[最小版本选择](https://go.dev/ref/mod#minimal-version-selection)的存在，它的传递依赖(transitive dependencies)的指定版本，不是最新版本，也会被添加到go.mod文件中。同样的情况也发生在调用go install example.com/cmd/devtoolx@latest 的情况下，在某些生态系统中，同样的构建发生时会绕过“已锁定”的版本(译注：去获取依赖的最新版本)。但在Go中，example.com/cmd/devtoolx的最新版本将被获取，但其所有的依赖项的版本将取决于其go.mod文件中的设置。

如果一个module被破坏，新的恶意版本被发布，没有人会受到影响，直到他们明确地更新该依赖关系，这种方式为gopher提供了审查变化的机会，并为生态系统提供时间来检测该事件会引发的影响。

### 版本内容永不改变

确保第三方不能影响构建的另一个关键属性是，module版本的内容是不可改变的。如果一个破坏某依赖项的攻击者可以重新上传该依赖项的一个现有的版本，那么他就可以自动破坏所有依赖该依赖项的项目。

这就是[go.sum文件](https://go.dev/ref/mod#go-sum-files)的作用。它包含了对构建有贡献的每个依赖项的加密哈希值的列表。同样，一个不完整的go.sum会导致一个错误，并且只有go get和go mod tidy会修改它，所以对它的任何修改都会伴随着一个主观故意的依赖性的改变。其他的构建将被保证有一套完整的校验和。

这是大多数lock文件的一个共同特征。但Go通过[校验和数据库（简称sumdb）](https://go.dev/ref/mod#checksum-database)领先了一步，sumdb是一个全局性的、仅可附加的(append)、加密验证的go.sum条目列表。当go get需要在go.sum文件中添加一个条目时，它从sumdb中获取该条目，并对sumdb的完整性进行加密证明。这不仅确保了某一module的每一次构建都使用相同的依赖，而且确保了每一个module都使用相同的依赖内容。

sumdb使那些试图用修改过的（例如放置后门的）源码来攻击特定依赖项变为不可能，甚至谷歌自己运维的Go基础设施也做不到。

它将保证你使用的代码与其他使用例如example.com/modulex v1.9.2的人所使用的代码完全相同，并且已经过审查。

最后，我最喜欢sumdb的特点：它不需要module作者的任何密钥管理，而且它与Go module的非中心化特性无缝连接。

### VCS是真相之源

大多数项目是通过一些版本控制系统（VCS）开发的。在其他生态系统中，这些项目还需要被再次上传到中心软件包库(译注：比如js生态中的npm)。这意味着有两个账户可能被入侵，一个是VCS主机，另一个是中心软件包库。对后者的攻击使用得更少，也更容易被忽视。这也意味着在上传到中心仓库的版本中更容易隐藏恶意代码，尤其是当源码作为上传的一部分被例行修改时，比如说将其最小化(译注：比如js代码的压缩)。

在Go中，不存在中心包库账户这样的东西。包的导入路径包含了go mod download所需要的信息，以便go命令直接从VCS中获取其module，vcs上的标签定义了module的版本。

我们确实有[Go Module Mirror](https://go.dev/blog/module-mirror-launch)，但那只是一个代理。module作者不需要注册账户，也不需要向代理上传版本。代理使用与go工具链相同的逻辑（事实上，代理运行go module download）来获取和缓存一个版本。由于校验数据库保证一个给定的module版本只能有一个源码树，每个使用代理的人都会看到从代理获取的结果与绕过代理直接从VCS获取的结果是相同的。(如果该版本在VCS中不再可用，或者其内容发生了变化，直接获取将导致错误，而从代理获取可能仍然有效，提高了可用性并保护生态系统免受[“左键”问题](https://blog.npmjs.org/post/141577284765/kik-left-pad-and-npm)的影响）。

在客户端运行VCS工具会暴露出一个相当大的攻击面。这也是Go module mirror的另一个作用：代理上的Go工具在一个强大的沙盒内运行，并被配置为支持所有的VCS工具，而[默认的是只支持两个主要的VCS系统（git和Mercurial）](https://go.dev/ref/mod#vcs-govcs)。任何使用代理的人仍然可以获取使用非默认的VCS系统发布的代码，但攻击者在大多数安装中无法接触到这些代码。

### 仅构建代码，但并不会执行它

Go工具链的一个明确的安全设计目标是，无论是获取还是构建代码，都不会让代码执行，无论代码是否是不被信任的和恶意的。这与其他大多数生态系统不同，许多生态系统在获取软件包时对运行代码提供了first-class的支持。这些”post-install”的钩子在过去被用作一种最方便的攻击方式：通过受到攻击的依赖攻击开发者的机器，并通过module作者进行[蠕虫攻击](https://en.wikipedia.org/wiki/Computer_worm)。

公平地说，如果你要获取一些代码，往往会在不久之后执行，要么作为开发者机器上的测试的一部分，要么作为生产中的二进制文件的一部分，所以缺乏post-install钩子只会减缓攻击者。(在构建过程中没有安全边界：任何有助于构建的软件包都可以定义一个init函数）。然而，它可以成为一个有意义的风险缓解措施，因为你可能正在执行一个二进制文件或测试一个包，而这个包只使用module依赖的一个子集。例如，如果你在macOS上构建并执行example.com/cmd/devtoolx，那么针对Windows的依赖或example.com/cmd/othertool的依赖就不可能危害到你的机器。

在Go中，没有为特定构建提供代码的module对构建没有安全影响(译注：得益于[Go 1.17引入的module依赖图修剪](https://mp.weixin.qq.com/s/Fer90nattWxXDWDC1VV55w))。

### “一点复制比一点依赖性好”

在Go生态系统中，最后一个可能也是最重要的软件供应链风险缓解措施，可能也是最没有技术含量的一个：Go有一种拒绝大型依赖树的文化，宁可复制一点也不愿意增加新的依赖关系。这可以追溯到Go的一个谚语：[“一点复制比一点依赖性好”](https://youtube.com/clip/UgkxWCEmMJFW0-TvSMzcMEAHZcpt2FsVXP65)。”零依赖”的标签总是被高质量的可重复使用的Go module所自豪地佩戴。如果你发现自己需要一个这样的库，你很可能会发现它不会导致你依赖其他作者和所有者的几十个module。

丰富的标准库和附加module（golang.org/x/…的module）也使之成为可能，这些module提供了常用的高级构建模块，如HTTP栈、TLS库、JSON编码等。

所有这些意味着只需少量的依赖关系就可以建立丰富、复杂的应用程序。无论工具有多好，它都不能消除重复使用代码的风险，所以**最有力的缓解措施永远是一个小的依赖树**。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论