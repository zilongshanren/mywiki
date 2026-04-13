---
title: 没有VPS搭建govanityurls服务？别急！你依然可以自定义Go包导入路径
url: https://tonybai.com/2020/11/15/another-approach-to-customize-package-import-path/
published: '2020-11-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 没有VPS搭建govanityurls服务？别急！你依然可以自定义Go包导入路径

![img{512x368}](../../assets/70a2226a28e7fbe3.png)


我们见到的[Go包的导入路径](https://tonybai.com/2015/03/09/understanding-import-packages/)常常以github.com、bitbucket.org等代码托管站点的域名为前缀，这样的包导入路径有一个问题，那就是**当Go包的托管站点发生变更时(比如从github.om迁移到bitbucket.org或gitlab.com)，该包的使用者需要更新包的导入路径**。当然，在[支持go module+GOPROXY](https://tonybai.com/2018/11/26/hello-go-module-proxy/)的情况下，如果使用者不再升级包版本，他/她完全可以继续使用原包导入路径，但这仅是特例。

还有一些包的导入路径并非以知名代码托管站点域名作为前缀，比如：Go官方扩展包text，它的包导入路径是**golang.org/x/text**，这种包导入路径被称为**vanity import path**，字面义是**虚荣心导入路径**，即以个人或组织官方域名作为前缀的包导入路径。采用vanity import path的包**避免了包迁移对包使用者的影响**。包使用者完全无需关心包的实际存储位置是在github上还是在bitbucket上或是私有服务器上。同时将vanity import path作为包的[权威路径(canonical import path)](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)，也方便go get等对包权威路径的检查，避免包路径变更的前后不一致。

之前笔者曾经写过[两篇文章](https://tonybai.com/2017/06/30/go-get-go-packages-in-private-code-repo-by-govanityurls/)介绍了利用[govanityurls](https://github.com/bigwhite/govanityurls)这个工具实现自定义包导入路径的方法。不过这种方法有一个约束条件，那就是你需要有一台VPS主机来部署运行govanityurls。虽然现在的云主机很便宜，但是购买和自建毕竟还是要付出一定成本的。如果没有VPS搭建govanityurls服务，那我们是否还有其他方法来自定义Go包导入路径呢？答案当然是**有**。

根据Go官方[关于go get命令的文档](https://tip.golang.org/cmd/go/#hdr-Remote_import_paths)，当go get从非知名托管站点(github, bitbucket等之外的站点)获取go包时，会尝试在返回的http/https应答head标签中查找是否有如下形式meta标签：

```
<meta name="go-import" content="import-prefix vcs repo-root">
```


meta标签中的name值是固定的”go-import”，import-prefix即包vanity import path，比如：**go.tonybai.com/gocmpp**；vcs是采用的版本控制工具，git、svn或hg等；repo-root是包代码的实际存储服务器url。

下面是一个实际例子：

```
<meta name="go-import" content="go.tonybai.com/gocmpp git https://github.com/bigwhite/gocmpp">
```


对于这样的标签，go get会做进一步匹配(可参见GOROOT/src/cmd/go/internal/get/vcs.go中的matchGoImport函数实现)，看content值中的import-prefix是否是go get所需要的包的导入路径。如果是，则会向真正存储包代码的服务器再次发起代码获取请求(比如：git clone等）。

你可能会说：我用一个静态站点服务也能返回这样的应答。没错！但搭建静态站点一般还是需要VPS，这里我们介绍一种无须VPS的方法：**利用 github pages**。

下面是利用github pages实现自定义Go包导入路径的原理图：

![img{512x368}](../../assets/a5ceb216441bc0ac.png)


下面我们就以**go.tonybai.com/gocmpp**这个包导入路径的定制步骤来说明一下上述原理。

首先，我们要给**tonybai.com**这个域名添加一个子域名：**go.tonybai.com**作为我个人生产的所有Go包的导入路径前缀。我在DNS设置中为**go.tonybai.com**指定一个CNAME值：**go.tonybai.com.github.io**。这样当访问**go.tonybai.com**时，实际上是向**go.tonybai.com.github.io**发起请求。当然此刻如果你向**go.tonybai.com**发起请求时，你必然会得到404错误，因为github尚未建立起**go.tonybai.com.github.io**这个站点。

接下来，我们就来建立**go.tonybai.com.github.io**这个基于github pages的静态站点。我创建一个新的代码仓库：**github.com/bigwhite/go.tonybai.com.github.io**，在该仓库的”Settings”标签中，我们启用github pages，并将该仓库的master分支作为站点的根路径。在同一页面的**Custom domain**下，我们填入**go.tonybai.com**，点击save保存。github会在该仓库中创建一个名为CNAME的文件，其内容如下：

```
$cat CNAME
go.tonybai.com
```


表示该站点绑定了自定义域名：**go.tonybai.com**。

正常情况下，你还可以在**Settings**标签下启用该静态站点的HTTPS服务，github会自动向Let’s Encrypt发起证书申请。

注：由于我的域名之前已经在Let’s Encrypt申请过相关证书，这里始终失败。这样导致后续我们只能使用go get -insecure去获取Go包代码。


在该仓库中，我们创建一个名为gocmpp的文件：

```
<html>
<head>
<meta name="go-import" content="go.tonybai.com/gocmpp git https://github.com/bigwhite/gocmpp">
<meta http-equiv="refresh" content="0;URL='https://github.com/bigwhite/gocmpp'">
</head>
<body>
Redirecting you to the <a href="https://github.com/bigwhite/gocmpp">project page</a>...
</body>
</html>
```


该文件内容作为访问**go.tonybai.com/gocmpp**的请求的应答。

大约20分钟后，github pages内容生效。我们就可以使用下面命令去获取本存储在github.com/bigwhite/gocmpp下面的包了：

```
$go get go.tonybai.com/gocmpp
```


由于证书问题，这里我们只能用go get -insecure，即让go get使用http协议发起请求。

在gopath mode下，我们的执行结果如下：

```
$GO111MODULE=off go get -x -v -insecure go.tonybai.com/gocmpp
# get https://go.tonybai.com/gocmpp?go-get=1
# get https://go.tonybai.com/gocmpp?go-get=1: 200 OK (1.012s)
get "go.tonybai.com/gocmpp": found meta tag get.metaImport{Prefix:"go.tonybai.com/gocmpp", VCS:"git", RepoRoot:"https://github.com/bigwhite/gocmpp"} at //go.tonybai.com/gocmpp?go-get=1
go.tonybai.com/gocmpp (download)
cd .
git clone -- https://github.com/bigwhite/gocmpp /Users/tonybai/Go/src/go.tonybai.com/gocmpp
cd /Users/tonybai/Go/src/go.tonybai.com/gocmpp
git submodule update --init --recursive
cd /Users/tonybai/Go/src/go.tonybai.com/gocmpp
git show-ref
cd /Users/tonybai/Go/src/go.tonybai.com/gocmpp
git submodule update --init --recursive
.... ....
cd /Users/tonybai/Go/src/go.tonybai.com/gocmpp
/Users/tonybai/.bin/go1.14/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath "$WORK/b001=>" -p go.tonybai.com/gocmpp -complete -buildid O9VmohLTciBDjallbacN/O9VmohLTciBDjallbacN -goversion go1.14 -D "" -importcfg $WORK/b001/importcfg -pack -c=4 ./activetest.go ./client.go ./conn.go ./connect.go ./deliver.go ./fwd.go ./packet.go ./receipt.go ./server.go ./submit.go ./terminate.go
/Users/tonybai/.bin/go1.14/pkg/tool/darwin_amd64/buildid -w $WORK/b001/_pkg_.a # internal
cp $WORK/b001/_pkg_.a /Users/tonybai/Library/Caches/go-build/ec/ec99b1c49c84d1e2edf88bee646f17198acc38c2c8f5a3d859540a394d6c5d0c-d # internal
mkdir -p /Users/tonybai/Go/pkg/darwin_amd64/go.tonybai.com/
mv $WORK/b001/_pkg_.a /Users/tonybai/Go/pkg/darwin_amd64/go.tonybai.com/gocmpp.a
rm -r $WORK/b001/
/Users/tonybai/go/src git:(master) $tree -L 1 go.tonybai.com
go.tonybai.com
└── gocmpp
1 directory, 0 files
```


我们看到go get成功通过go.tonybai.com/gocmpp获取到gocmpp包，并编译安装成功(安装到GOPATH/pkg/下面)。

下面是module-aware模式下的go get获取结果：

```
$GOPROXY='direct' go get -insecure -x -v go.tonybai.com/gocmpp
# get https://go.tonybai.com/?go-get=1
# get https://go.tonybai.com/gocmpp?go-get=1
# get https://go.tonybai.com/?go-get=1: 200 OK (1.032s)
# get https://go.tonybai.com/gocmpp?go-get=1: 200 OK (1.056s)
get "go.tonybai.com/gocmpp": found meta tag get.metaImport{Prefix:"go.tonybai.com/gocmpp", VCS:"git", RepoRoot:"https://github.com/bigwhite/gocmpp"} at //go.tonybai.com/gocmpp?go-get=1
mkdir -p /Users/tonybai/Go/pkg/mod/cache/vcs # git3 https://github.com/bigwhite/gocmpp
... ...
0.017s # cd /Users/tonybai/Go/pkg/mod/cache/vcs/63c8ecfc5ed2c830894c13fd15ab1494ce9897aefba1d11c78740b046033e9ae; git cat-file blob 0f5a658fda5e029943f9b256fefe4fa4550e7906:go.mod
go get: go.tonybai.com/gocmpp@v0.0.0-20200715060927-0f5a658fda5e: parsing go.mod:
module declares its path as: github.com/bigwhite/gocmpp
but was required as: go.tonybai.com/gocmpp
```


我们看到go get同样获取到了gocmpp module，但是由于module-aware模式下，go get会对module根路径进行检查，因此go get发现了go.mod中的module根路径：github.com/bigwhite/gocmpp与要获取的module路径(go.tonybai.com/gocmpp)不符并报错。我们更新一下gocmpp项目中的go.mod内容后，这个问题将不复存在。

这样，我们在没有VPS的前提下也实现了自定义包导入路径。后续每当我创建一个新module或新包，我只需向该仓库(go.tonybai.com.github.io)提交一个以module或package名字命名的文件即可，就像上的gocmpp文件那样。

## * 参考资料：https://gianarb.it/blog/go-mod-vanity-url

我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线>了，感谢小伙伴们学习支持！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接>口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily(Go每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论