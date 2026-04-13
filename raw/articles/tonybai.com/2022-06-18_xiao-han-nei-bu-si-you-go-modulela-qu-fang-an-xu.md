---
title: 小厂内部私有Go module拉取方案（续）
url: https://tonybai.com/2022/06/18/the-approach-to-go-get-private-go-module-in-house-part2/
published: '2022-06-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 小厂内部私有Go module拉取方案（续）

![](../../assets/dc2c6ba7af38c319.png)


[本文永久链接](https://tonybai.com/2022/06/18/the-approach-to-go-get-private-go-module-in-house-part2) – https://tonybai.com/2022/06/18/the-approach-to-go-get-private-go-module-in-house-part2

自从去年在公司[搭建了内部私有Go module proxy](https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house)后，我们的私有代理工作得基本良好。按理说，这篇续篇本不该存在:)。

日子一天天过去，Go团队逐渐壮大，空气中都充满了“Go的香气”。

突然有一天，业务线考虑将目前在用的[gerrit](https://www.gerritcodereview.com)换成[gitlab](https://about.gitlab.com)。最初使用gerrit的原因不得而知，但我猜是想使用gerrit强大且独特的code review机制和相应的工作流。不过由于业务需求变化太快，每个迭代的功能都很多，“+2”的review机制到后来就形同虚设了。

如果不用gerrit review工作流，那么gerrit还有什么存在的价值呢。从管理员那边反馈，gerrit配置起来也是比较复杂的，尤其是权限。两者叠加就有了迁移到gitlab的想法。这样摆在Go团队面前的一个事情就是**如何让我们内部私有go module代理适配gitlab**。

如果你还不清楚我们搭建私有Go module代理的原理，那么在进一步往下阅读前，请先阅读一下

[《小厂内部私有Go module拉取方案》]。

### 适配gitlab

回顾一下我们的私有Go module代理的原理图：

![](../../assets/8c90a5301a778963.png)


基于这张原理图，我们分析后得出结论：要适配gitlab仓库，其实很简单，只需修改govanityurls的配置文件中的各个module的真实repo地址即可，这也符合更换一个后端代码仓库服务理论上开发人员无感的原则。

下面我们在gitlab上创建一个foo repo，其对应的module path为mycompany.com/go/foo。我们使用ssh方式拉取gitlab repo，先将goproxy所在主机的公钥添加到gitlab ssh key中。然后将gitlab clone按钮提示框中给出的clone地址：git@10.10.30.30:go/foo.git填到vanity.yaml文件中：

```
//vanity.yaml
... ...
/go/foo:
repo: ssh://git@10.10.30.30:go/foo.git
vcs: git
```


我门在一台开发机上建立测试程序，该程序导入mycompany.com/go/foo，执行go mod tidy命令的结果如下：

```
$go mod tidy
go: finding module for package mycompany.com/go/foo
demo imports
mycompany.com/go/foo: cannot find module providing package mycompany.com/go/foo: module mycompany.com/go/foo: reading http://10.10.20.20:10000/mycompany.com/go/foo/@v/list: 404 Not Found
server response:
go list -m -json -versions mycompany.com/go/foo@latest:
go: mycompany.com/go/foo@latest: unrecognized import path "mycompany.com/go/foo": http://mycompany.com/go/foo?go-get=1: invalid repo root "ssh://git@10.10.30.30:go/foo.git": parse "ssh://git@10.10.30.30:go/foo.git": invalid port ":go" after host
```


从goproxy返回的response内容来看，似乎是goproxy使用的go命令无法识别：”ssh://git@10.10.30.30:go/foo.git”，认为10.10.30.30后面的分号后面应该接一个端口，而不是go。

我们将repo换成下面这样的格式：

```
/go/foo:
repo: ssh://git@10.10.30.30:80/go/foo.git
vcs: git
```


重启govanityurls并重新执行go mod tidy，依旧报错：

```
$go mod tidy
go: finding module for package mycompany.com/go/foo
demo imports
mycompany.com/go/foo: cannot find module providing package mycompany.com/go/foo: module mycompany.com/go/foo: reading http://10.10.20.20:10000/mycompany.com/go/foo/@v/list: 404 Not Found
server response:
go list -m -json -versions mycompany.com/go/foo@latest:
go: module mycompany.com/go/foo: git ls-remote -q origin in /root/.bin/goproxycache/pkg/mod/cache/vcs/4d37c02c151342112bd2d7e6cf9c0508b31b8fe1cf27063da6774aa0f53d872f: exit status 128:
kex_exchange_identification: Connection closed by remote host
fatal: Could not read from remote repository.
```


直接在主机上通过git clone git@10.10.30.30:80/go/foo.git也是报错的！ssh不行，我们再来试试http方式。 使用http方式呢，每次clone都需要输入用户名密码，不适合goproxy。是时候让personal token上阵了！在gitlab上分配好personal token，然后在本地建立~/.netrc如下：

```
# cat ~/.netrc
machine 10.10.30.30
login tonybai
password [your personal token]
```


然后我们将vanity.yaml中的repo改为如下形式：

```
// vanity.yaml
/go/foo:
repo: http://10.10.30.30/go/foo.git
vcs: git
```


这样再执行go mod tidy，foo仓库就被顺利拉取了下来。

### 答疑

#### 1. git clone错误

在搭建goproxy时，我们通常会在goproxy服务器上手工验证一下是否可以通过git成功拉取私有仓库，如果git clone出现下面错误信息，是什么问题呢？

```
$ git clone ssh://tonybai@10.10.30.30:29418/go/common
Cloning into 'common'...
Unable to negotiate with 10.10.30.30 port 29418: no matching key exchange method found. Their offer: diffie-hellman-group14-sha1,diffie-hellman-group1-sha1
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.
```


这里的错误提示信息其实是很清楚明了的。git服务器端支持diffie-hellman-group1-sha1和diffie-hellman-group14-sha1这两种密钥交换方法，而git客户端却默认一个都不支持。

怎么解决呢？我们需要在goproxy所在主机增加一个配置.ssh/config：

```
// ~/.ssh/config
Host 10.10.30.30
HostName 10.10.30.30
User tonybai
Port 29418
KexAlgorithms +diffie-hellman-group1-sha1
IdentityFile ~/.ssh/id_rsa
```


有了这条配置后，我们就可以成功clone。

#### 2. 使用非安全连接

有些童鞋使用这个方案后会遇到下面问题：

```
$go get mycompany.com/go/common@latest
go: module mycompany.com/go/common: reading http://10.10.30.30:10000/mycompany.com/go/common/@v/list: 404 Not Found
server response:
go list -m -json -versions mycompany.com/go/common@latest:
go list -m: mycompany.com/go/common@latest: unrecognized import path "mycompany.com/go/common": https fetch: Get "https://mycompany.com/go/common?go-get=1": dial tcp 127.0.0.1:443: connect: connection refused
```


首先，go get得到的服务端响应信息中提示：无法连接127.0.0.1:443，查看goproxy主机的nginx access.log，也无日志。说明goproxy没有发起请求。也就是说问题出在go list命令这块，它为什么要去连127.0.0.1:443？我们的代码服务器使用的可是http而非https方式访问。

这让我想起了Go 1.14中增加的GOINSECURE，go命令默认采用的是secure方式，即https去访问代码仓库的。如果不要求非得以https获取module，或者即便使用https，也不再对server证书进行校验，那么需要设置GOINSECURE环境变量，比如；

```
export GOINSECURE="mycompany.com"
```


这样再获取mycompany.com/…下面的go module时，就不会出现上面的错误了！

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](http://image.tonybai.com/img/tonybai/go-programming-from-beginner-to-master-qr.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

大佬好，请教个问题，我按照你的方式搭建了企业内部的拉取方案，vcs也用的gitlab，但遇到个问题，就是不能按版本拉取package，一旦给repo打上tag，go get的时候会包vx.y.z is not a tag这样的错，不打标签的话是可以正常拉取的，不知道你们是否有遇到过这样的问题

我这里用下面两种方式，都没问题：

$go get example.com/go/common/log

go: downloading example.com/go/common v0.1.0

go: added example.com/go/common v0.1.0

$go get example.com/go/common/log@v0.1.0

go: added example.com/go/common v0.1.0

是不是gitlab repo权限设置问题啊，tag是否有单独权限管理，导致可以获取主干，但无法获取tag版本？