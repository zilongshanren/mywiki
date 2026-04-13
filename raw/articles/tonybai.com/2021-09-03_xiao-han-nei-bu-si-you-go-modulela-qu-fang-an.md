---
title: 小厂内部私有Go module拉取方案
url: https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house/
published: '2021-09-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 小厂内部私有Go module拉取方案

![](../../assets/1547404cf187fb36.png)


[本文永久链接](https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house) – https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house

### 1. 问题来由

[Go 1.11版本](https://mp.weixin.qq.com/s?__biz=MzIyNzM0MDk0Mg==&mid=100000482&idx=1&sn=b5a588b8b4cd63ac57b29ee6e64438aa&chksm=6863e5035f146c152ae2a7460dea924df4b14a56bbcbee1966934abed3fcfd492bc6f56928b2#rd)引入[Go module](https://tonybai.com/tag/gomodule)后，Go命令拉取依赖的公共go module不再是“痛点”。如下图所示：

![](../../assets/3faed3df1c36326a.png)



我们在公司/组织内部仅需要为环境变量GOPROXY配置一个公共GOPROXY服务即可轻松拉取所有公共go module(公共module即开源module)。

但随着公司内Go使用者增多以及Go项目的增多，“代码重复”问题就出现了。抽取公共代码放入一个独立的、可被复用的内部私有仓库成为必然。这样我们便**有了拉取私有go module的需求！**

一些公司或组织的所有代码都放在公共vcs托管服务商那里(比如github.com)，私有go module则直接放在对应的公共vcs服务的private repository(私有仓库)中。如果你的公司也是如此，那么拉取托管在公共vcs私有仓库中的私有go module也很容易，见下图：

![](../../assets/1436121875cb1dc4.png)



当然这个方案的一个前提是：每个开发人员都需要具有访问公共vcs服务上的私有go module仓库的权限，凭证的形式不限，可以是basic auth的user和password，也可以是personal access token(类似github那种)，只要按照公共vcs的身份认证要求提供即可。

但是如果私有go module放在公司内部的vcs服务器上，就像下面图中所示：

![](../../assets/a266c4681d9202e4.png)



那么我们该如何让Go命令自动拉取内部服务器上的私有go module呢？

一些gopher会说：“**这很简单啊! 这和拉取托管在公共vcs服务上的私有go module没有什么分别啊**”。持这种观点的gopher多半来自大厂。大厂内部有完备的IT基础设施供开发使用，大厂内部的vcs服务器都可以通过域名访问(比如git.bat.com/user/repo)，因此大厂内部员工可以像访问公共vcs服务那样访问内部vcs服务器上的私有go module，就像下面图中所示：

![](../../assets/96bef475cea38407.png)



我们看到：在上面这个方案中，公司搭建了一个内部goproxy服务(即上图中的in-house goproxy)，这样的目的一来是为那些无法直接访问外网的开发机器以及ci机器提供拉取外部go module的途径，二来由于in-house goproxy的cache的存在，还可以加速公共go module的拉取效率。对于私有go module，开发机将其配置到GOPRIVATE环境变量中，这样Go命令在拉取私有go module时不会再走GOPROXY，而会采用直接访问vcs(如上图中的git.bat.com)的方式拉取私有go module。

当然大厂还可能采用下图所示方案将外部go module与私有go module都交给内部统一的Goproxy服务去处理：

![](../../assets/05511f6295040a4c.png)



在这种方案中，开发者仅需要将GOPROXY配置为in-house goproxy便可以统一拉取外部go module与私有go module。但由于go命令默认会对所有通过goproxy拉取的go module进行sum校验（到sum.golang.org)，而我们的私有go module在公共sum验证server中没有数据记录，因此，开发者需要将私有go module填到GONOSUMDB环境变量中，这样go命令就不会对其进行sum校验了。不过这种方案有一处要注意：那就是in-house goproxy需要拥有对所有private module所在repo的访问权限，这样才能保证每个私有go module的拉取成功！

好了，问题来了！对于那些没有完备内部IT基础设施，还想将私有go module放在公司内部的vcs服务器上的小厂应该如何实现私有go module的拉取方案呢？

### 2. 可供小厂参考的一个解决方案

小厂虽小，但目标不能低。小厂虽然IT基础设施薄弱或不够灵活，但也不能因此给开发人员带去太多额外的“负担”。因此，对比了上面的两个大厂可能采用的方案，我们更倾向于后者。这样，我们就可以**将所有复杂性都交给in-house goproxy这个节点，开发人员就可以做的足够简单**。但小厂没有DNS，无法用域名…，我们该怎么实现这个方案呢？在这一节中，我们就实现这个方案。

#### 0. 方案示例环境拓扑

我们先为后续的方案实现准备一个示例环境，其拓扑如下图：

![](../../assets/2a34a232e4becb18.png)


#### 1. 选择一个goproxy实现

[Go module proxy协议规范](https://pkg.go.dev/cmd/go@master#hdr-Module_proxy_protocol)发布后，Go社区出现了很多成熟的Goproxy开源实现。从最初的[athens](https://tonybai.com/2018/11/26/hello-go-module-proxy/)，再到国内的两个优秀的开源实现：[goproxy.cn](https://github.com/goproxy/goproxy)和[goproxy.io](https://github.com/goproxyio/goproxy)。其中，goproxy.io在官方站点给出了[企业内部部署的方法](https://goproxy.io/zh/docs/enterprise.html)，基于这一点，我们就基于goproxy.io来实现我们的方案（其余的goproxy实现应该也都可以实现)。

我们在上图中的in-house goproxy节点上执行下面步骤安装goproxy：

```
$mkdir ~/.bin/goproxy
$cd ~/.bin/goproxy
$git clone https://github.com/goproxyio/goproxy.git
$cd goproxy
$make
```


编译后，会在当前的bin目录(~/.bin/goproxy/goproxy/bin)下看到名为goproxy的可执行文件。

建立goproxy cache目录：

```
$mkdir /root/.bin/goproxy/goproxy/bin/cache
```


启动goproxy：

```
$./goproxy -listen=0.0.0.0:8081 -cacheDir=/root/.bin/goproxy/goproxy/bin/cache -proxy https://goproxy.io
goproxy.io: ProxyHost https://goproxy.io
```


启动后goproxy在8081端口监听(即便不指定，goproxy的默认端口也是8081)，指定的上游goproxy服务为goproxy.io。

注意：goproxy的这个启动参数并不是最终版本的，这里仅仅想验证一下goproxy是否能按预期工作。


接下来，我们来验证一下goproxy的工作是否如我们预期。

我们在开发机上配置GOPROXY环境变量指向10.10.20.20:8081：

```
// .bashrc
export GOPROXY=http://10.10.20.20:8081
```


生效环境变量后，执行下面命令：

```
$go get github.com/pkg/errors
```


结果如预期，开发机顺利下载了github.com/pkg/errors包。

在goproxy侧，我们看到了下面日志：

```
goproxy.io: ------ --- /github.com/pkg/@v/list [proxy]
goproxy.io: ------ --- /github.com/pkg/errors/@v/list [proxy]
goproxy.io: ------ --- /github.com/@v/list [proxy]
goproxy.io: 0.146s 404 /github.com/@v/list
goproxy.io: 0.156s 404 /github.com/pkg/@v/list
goproxy.io: 0.157s 200 /github.com/pkg/errors/@v/list
```


并且在goproxy的cache目录下，我们也看到了下载并缓存的github.com/pkg/errors包：

```
$cd /root/.bin/goproxy/goproxy/bin/cache
$tree
.
└── pkg
└── mod
└── cache
└── download
└── github.com
└── pkg
└── errors
└── @v
└── list
8 directories, 1 file
```


#### 2. 自定义包导入路径并将其映射到内部的vcs仓库

小厂可能没有为vcs服务器分配域名，我们也不能在Go私有包的导入路径中放入ip地址，因此我们需要给我们的私有go module自定义一个路径，比如：mycompany.com/go/module1。我们统一将私有go module放在mycompany.com/go下面的代码仓库中。

接下来的问题是，当goproxy去拉取mycompany.com/go/module1时，应该得到mycompany.com/go/module1对应的内部vcs上module1 仓库的地址，这样goproxy才能从内部vcs代码服务器上下载到module1对应的代码。

![](../../assets/ccae4bd1f94ae051.png)



其实[方案不止一种](https://tonybai.com/2020/11/15/another-approach-to-customize-package-import-path)。这里我们使用一个名为[govanityurls](https://tonybai.com/2017/06/30/go-get-go-packages-in-private-code-repo-by-govanityurls)的工具，这个工具在[我以前的文章](https://tonybai.com/2017/06/28/set-custom-go-get-import-path-for-go-package)中曾提到过。

结合govanityurls和nginx，我们就可以将私有go module的导入路径映射为其在vcs上的代码仓库的真实地址。下面的图解释了具体原理：

![](../../assets/8c90a5301a778963.png)


首先，goproxy要想将收到的拉取私有go module(mycompany.com/go/module1)的请求不转发给公共代理，需要在其启动参数上做一些手脚，如下面修改后的goproxy启动命令：

```
$./goproxy -listen=0.0.0.0:8081 -cacheDir=/root/.bin/goproxy/goproxy/bin/cache -proxy https://goproxy.io -exclude "mycompany.com/go"
```


这样凡是与-exclude后面的值匹配的go module拉取请求，goproxy都不会转给goproxy.io，而是直接请求go module的“源站”。而上面图中要做的就是将这个“源站”的地址转换为企业内部vcs服务中的一个仓库地址。由于mycompany.com这个域名并不存在，从图中我们看到：我们在goproxy所在节点的/etc/hosts中加了这样一条记录：

```
127.0.0.1 mycompany.com
```


这样goproxy发出的到mycompany.com的请求实则是发向了本机。而上图中所示，监听本机80端口的正是nginx，nginx关于mycompany.com这一主机的配置如下：

```
// /etc/nginx/conf.d/gomodule.conf
server {
listen 80;
server_name mycompany.com;
location /go {
proxy_pass http://127.0.0.1:8080;
proxy_redirect off;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
}
}
```


我们看到对于路径为mycompany.com/go/xxx的请求，nginx将请求转发给了127.0.0.1:8080，而这个服务地址恰是[govanityurls](https://github.com/GoogleCloudPlatform/govanityurls)工具监听的地址。

govanityurls这个工具是前Go核心开发团队成员[Jaana B.Dogan](https://rakyll.org)开源的一个工具，这个工具可以帮助gopher快速[实现自定义Go包的go get导入路径](https://tonybai.com/2017/06/30/go-get-go-packages-in-private-code-repo-by-govanityurls/)。

govanityurls本身就好比一个“导航”服务器。当go命令向自定义包地址发起请求时，实则是将请求发送给了govanityurls服务，之后govanityurls将请求中的包所在仓库的真实地址(从vanity.yaml配置文件中读取)返回给go命令，后续go命令再从真实的仓库地址获取包数据。

注：govanityurls的安装方法很简单，直接go install/go get github.com/GoogleCloudPlatform/govanityurls即可。


在我们的示例中，vanity.yaml的配置如下：

```
host: mycompany.com
paths:
/go/module1:
repo: ssh://admin@10.10.30.30/module1
vcs: git
```


也就是说当govanityurls收到nginx转发的请求后，会将请求与vanity.yaml中配置的module路径相匹配，如果匹配ok，则会将该module的真实repo地址通过go命令期望的应答格式予以返回。在这里我们看到，module1对应的真实vcs上的仓库地址为：ssh://admin@10.10.30.30/module1。

于是goproxy会收到这个地址，并再次向这个真实地址发起请求，并最终将module1缓存到本地cache并返回给客户端。

注意：由于这个方案与大厂的第二个方案是一样的，因此goproxy需要有访问mycompany.com/go下面所有go module对应的真实vcs仓库的权限。


#### 3. 开发机(客户端)的设置

前面示例中，我们已经将开发机的GOPROXY环境变量设置为goproxy的服务地址。但我们说过凡是通过GOPROXY拉取的go module，go命令默认都会将其sum值到公共GOSUM服务器上去校验。但我们实质上拉取的是私有go module，GOSUM服务器上并没有我们的go module的sum数据。这样会导致go build命令报错，无法继续构建过程。

因此，开发机客户端还需将mycompany.com/go作为一个值设置到GONOSUMDB环境变量中，这就告诉go命令，凡是与mycompany.com/go匹配的go module，都无需做sum校验了。

#### 4. 方案的“不足”

当然上述方案也不是完美的，它也有自己的不足的地方：

- 开发者还是需要额外配置GONOSUMDB变量

由于Go命令默认会对从GOPROXY拉取的go module进行sum校验，因此我们需要将私有go module配置到GONOSUMDB环境变量中，这给开发者带来了一个小小的“负担”。

缓解措施：小厂可以将私有go项目都放在一个特定域名下，这样就无需为每个go私有项目单独增加GONOSUMDB配置了，只需要配置一次即可。

- 新增私有go module，vanity.yaml需要手工同步更新

这个是这个方案最不灵活的地方了，由于目前govanityurls功能有限，我们针对每个私有go module可能都需要单独配置其对应的vcs仓库地址以及获取方式(git, svn or hg)。

缓解方案：在一个vcs仓库中管理多个私有go module，就像[etcd](https://github.com/etcd-io/etcd)那样。相比于最初go官方建议的一个repo只管理一个module，新版本的go在[一个repo管理多个go module](https://golang.google.cn/doc/modules/managing-source#multiple-module-source)方面已经有了长足的进步。

不过对于小厂来说，这点额外工作与得到的收益相比，应该也不算什么！^_^

- 无法划分权限

在上面的方案说明时也提到过，goproxy所在节点需要具备访问所有私有go module所在vcs repo的权限，但又无法对go开发者端做出有差别授权，这样只要是goproxy能拉取到的私有go module，go开发者都能拉取到。

不过对于多数小厂而言，内部所有源码原则上都是企业内部公开的，这个问题似乎也不大。如果觉得这是个问题，那么只能使用上面的大厂的第一个方案了。

### 3. 小结

无论大厂小厂，当对Go的使用逐渐深入后，接纳的人增多，开发的项目增多且越来越复杂后，拉取私有go module这样的问题肯定会摆到桌面上来。

对于大厂的gopher来说，这可能不是问题，甚至对他们都是透明的。但对于小厂等内部IT基础设施不完备的组织而言，的确需要自己动手解决。

这篇文章为小厂搭建Go私有库以及从私有库拉取私有go module提供了一个思路以及一个参考实现。

如果觉得上面的安装配置步骤有些繁琐，有兴趣深入的朋友可以将上述几个程序(goproxy, nginx, govanityurls)打到一个容器镜像中，实现一键安装设置。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我们的做法是架设一个 git 认证代理，对内网开放 go get 协议的拉取，顺便可以实现路径映射。

用 nexus 代理公网的 proxy 和 sumdb。

没那么复杂，一天工作量就搞定的事。

嗯，私有go module拉取方案有多种，这个要看“场情”:)。我们这里就不允许架设git认证代理。