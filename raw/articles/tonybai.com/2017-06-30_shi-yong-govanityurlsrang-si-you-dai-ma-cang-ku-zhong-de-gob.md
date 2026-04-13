---
title: 使用govanityurls让私有代码仓库中的go包支持go get
url: https://tonybai.com/2017/06/30/go-get-go-packages-in-private-code-repo-by-govanityurls/
published: '2017-06-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用govanityurls让私有代码仓库中的go包支持go get

《[定制Go Package的Go Get导入路径](http://tonybai.com/2017/06/28/set-custom-go-get-import-path-for-go-package/)》一文中我们讲到了通过使用[govanityurls](http://github.com/bigwhite/govanityurls)服务，我们可以定制go package的go get导入路径。不过，govanityurls的用途还不止这些，它还可以让你的私有代码仓库中的go package支持go get。

众所周知，开源的Go package一般分布在github、bitbucket等站点，但商业组织内部闭源的Go package则不一定都托管在像github这样的代码管理服务站点上，虽然使用github private repository服务的组织和个人正在日益增多（国内用户可能会用到码云git.oschina.net、code.csdn.net等）。很多企业或组织会自己搭建私有代码仓库(一般使用[git](https://git-scm.com/))来满足组织内部的代码版本管理需求，而目前市面上主流且成熟的支持本地搭建的代码管理软件包括[gitlab](https://about.gitlab.com/)、[bitbucket](https://bitbucket.org/product)等。那么如何让go get支持从这些私有代码仓库中获取go package呢？本文将来回答这个问题。

很多人会问：为什么要让私有仓库中的go package支持go get呢？直接git clone不就行了么？用过go get的gopher们都清楚：go get可以自动分析go package的依赖，并帮助自动下载相关依赖。虽然go get下载依赖有[各种局限](http://tonybai.com/2017/06/08/first-glimpse-of-dep/)，但没有go get的帮助，手工去下载各种依赖会更加“痛苦”。好了，接下来我们将用一个具体的例子来演示一下go get是如何一步步的支持从私有代码仓库下载Go包的。

我所在的开发团队使用的代码仓库就是在阿里云ECS上自行搭建的，使用的是[Atlassian](https://www.atlassian.com/)出品的[bitbucket](https://bitbucket.org/product)。虽然bitbucket在在线服务市场占有率可能不及github，但在线下自建代码仓库方面，bitbucket也是不可小觑的重量级选手。

不过bitbucket如何安装不是这里的重点，bitbucket的安装方法参考其[官网manual](https://confluence.atlassian.com/bitbucket)即可。安装后的bitbucket 仓库中的Project foo的repository bar的clone地址样式如下：

```
http://bitbucket_ip:bitbucket_port/scm/foo/bar.git
```


注意：我们的bitbucket仓库没有启用https，auth的方式采用的是普通的user和password方式（bitbucket支持客户端SSH key方式访问repository）。除此之外，我们并没有为bitbucket仓库绑定域名。


## 一、尝试go get“裸库”

我们以foo这个在demo project下的go repository为例，这个repository的clone地址为：http://10.11.12.13:31990/scm/demo/foo.git，于是我们先来尝试一下直接go get这个未经任何“修饰”的“裸库”(由于没有使用https，因此我们在go get的命令行参数中增加了-insecure选项):

```
# go get -insecure -v 10.11.12.13:31990/scm/demo/foo.git
# cd .; git ls-remote git://10.11.12.13:31990/scm/demo/foo
fatal: protocol error: bad line length character: HTTP
# cd .; git ls-remote https://10.11.12.13:31990/scm/demo/foo
fatal: unable to access 'https://10.11.12.13:31990/scm/demo/foo/': gnutls_handshake() failed: An unexpected TLS packet was received.
# cd .; git ls-remote http://10.11.12.13:31990/scm/demo/foo
fatal: could not read Username for 'http://10.11.12.13:31990': terminal prompts disabled
# cd .; git ls-remote git+ssh://10.11.12.13:31990/scm/demo/foo
ssh_exchange_identification: Connection closed by remote host
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.
# cd .; git ls-remote ssh://10.11.12.13:31990/scm/demo/foo
ssh_exchange_identification: Connection closed by remote host
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.
10.11.12.13:31990/scm/demo/foo.git (download)
root@10.11.12.13's password:
```


以失败告终！我们来分析一下go get -v输出的日志! 通过日志可以看出go get先后尝试用不同访问方式去获取repository数据，尝试的顺序依次是：git、https、http和git+ssh，结果都无功而返。

- 对于git方式，我们并未开通bitbucket的git访问服务，失败是必然的；
- 对于https，我们的bitbucket server同样未予支持；
- 对于http方式，日志提示：” terminal prompts disabled”，即客户端终端的提示被禁了，也就是无法输入user和password；
- 对于最后一种git+ssh，由于没有ssh登录bitbucket主机的密码也失败了。

在四种访问方式中，http是我们期望的。为了http方式能成功获取数据，我们需要开启termnial prompts(通过GIT_TERMINAL_PROMPT=1)，于是我们再次尝试：

```
# GIT_TERMINAL_PROMPT=1 go get -v -insecure 10.11.12.13:31990/scm/demo/foo.git
# cd .; git ls-remote git://10.11.12.13:31990/scm/demo/foo
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.
# cd .; git ls-remote https://10.11.12.13:31990/scm/demo/foo
fatal: unable to access 'https://10.11.12.13:31990/scm/demo/foo/': gnutls_handshake() failed: The TLS connection was non-properly terminated.
Username for 'http://10.11.12.13:31990': tonybai
Password for 'http://tonybai@10.11.12.13:31990':
10.11.12.13:31990/scm/demo/foo.git (download)
Username for 'http://10.11.12.13:31990': tonybai
Password for 'http://tonybai@10.11.12.13:31990':
package foo/config: unrecognized import path "foo/config" (import path does not begin with hostname)
package foo/routers: unrecognized import path "foo/routers" (import path does not begin with hostname)
github.com/mattes/migrate (download)
package github.com/mattes/migrate/driver/mysql: cannot find package "github.com/mattes/migrate/driver/mysql" in any of:
/root/.bin/go18/src/github.com/mattes/migrate/driver/mysql (from $GOROOT)
/root/go/src/github.com/mattes/migrate/driver/mysql (from $GOPATH)
```


我们看到这次go get在尝试http访问repository时，我们有机会输入user和password了，go get也成功了！至于下面的“unrecognized import path” error那是由于repository在GOPATH下的位置变更导致的。我们查看一下已经下载到本地的foo repository：

```
# tree -L 1 10.11.12.13\:31990/scm/demo/foo.git/
10.11.12.13:31990/scm/demo/foo.git/
├── foo.json
├── foo.yaml
├── conf
├── config
├── controllers
├── Dockerfile
├── errors
├── front-static
├── index
├── main.go
├── Makefile
├── migrations
├── models
├── README
├── routers
├── service
├── static
├── tests
├── topic
├── utils
├── vendor
├── views
└── websocket
17 directories, 6 files
```


虽然go get成功了， 但对于gopher来讲，foo下package的导入路径变成了：

```
import 10.11.12.13:31990/scm/demo/foo.git/some-package
```


这种格式、这种长度的导入路径是无法接受的。那我们该如何解决呢？

一种方法就是在bitbucket server端进行配置，通过为私有镜像仓库赋予域名的方式来去除import path中ip、port、不必要的前缀路径：scm/demo以及不必要的repository名中的后缀”.git”。但这种配置方式可能是非常复杂的，且是与你使用的git server软件相关的：bitbucket可能有bitbucket的配置方法，换作gitlab，可能就需要另外一种配置方法了。

另外一种方法就是用[govanityurls](http://github.com/bigwhite/govanityurls)来屏蔽server端复杂的配置，也屏蔽了与git server软件的相关性。

## 二、使用govanityurls让私有代码仓库中的go包支持go get

在《[定制Go Package的Go Get导入路径](http://tonybai.com/2017/06/28/set-custom-go-get-import-path-for-go-package/)》一文中，我们已经详细说明了govanityurls的使用和配置方法，这里就不赘述了，仅给出必要配置。

### 1、配置和启动govanityurls

这里我们使用pkg.tonybai.com这个域名来作为tonybai.com下面所有go package的导入路径的前缀，以foo package为例，它的导入路径将为”import pkg.tonybai.com/foo”，这样我们的vanity.yaml的配置如下：

```
/foo:
repo: http://10.11.12.13:31990/scm/demo/foo.git
```


启动govanityurls：

```
$ nohup govanityurls -host pkg.tonybai.com &
```


### 2、配置nginx并做域名重指向

在我的环境中，我将govanityurls部署到与bitbucket相同的server上了。在这台主机上，我们配置一下nginx，让govanityurls的服务以80端口呈现：

```
# cat /etc/nginx/conf.d/default.conf
server {
listen 80;
server_name pkg.tonybai.com;
location / {
proxy_pass http://10.11.12.13:8080;
proxy_redirect off;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
}
```


重启nginx使配置生效：nginx -s reload

### 3、验证

到目前为止foo这个repo的go get path变成了pkg.tonybai.com/foo了，我们来试着go get一下：

```
# GIT_TERMINAL_PROMPT=1 go get -insecure -v pkg.tonybai.com/foo
Fetching https://pkg.tonybai.com/foo?go-get=1
Parsing meta tags from https://pkg.tonybai.com/foo?go-get=1 (status code 200)
get "pkg.tonybai.com/foo": found meta tag main.metaImport{Prefix:"pkg.tonybai.com/foo", VCS:"git", RepoRoot:"http://10.11.12.13:31990/scm/demo/foo.git"} at https://pkg.tonybai.com/foo?go-get=1
tonybai.com/foo (download)
Password for 'http://10.11.12.13:31990':
package foo/config: unrecognized import path "foo/config" (import path does not begin with hostname)
package foo/routers: unrecognized import path "foo/routers" (import path does not begin with hostname)
github.com/mattes/migrate (download)
package github.com/mattes/migrate/driver/mysql: cannot find package "github.com/mattes/migrate/driver/mysql" in any of:
/root/.bin/go18/src/github.com/mattes/migrate/driver/mysql (from $GOROOT)
/root/go/src/github.com/mattes/migrate/driver/mysql (from $GOPATH)
```


go get成功！查看一下本地foo的repository情况：

```
# tree -L 1 go/src/pkg.tonybai.com/foo
go/src/pkg.tonybai.com/foo
├── foo.json
├── foo.yaml
├── conf
├── config
├── controllers
├── Dockerfile
├── errors
├── front-static
├── index
├── main.go
├── Makefile
├── migrations
├── models
├── README
├── routers
├── service
├── static
├── tests
├── topic
├── utils
├── vendor
├── views
└── websocket
17 directories, 6 files
```


## 三、小结

- 通过govanityurls，我们可以很容易让私有代码仓库中的go包支持go get；
- 对于本身就不支持go get的git server，那
[govanityurls](http://github.com/bigwhite/govanityurls)也是无能为力的。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

博主最近这段时间太高产了。。。我一篇没写完，你写10篇了。

之前积累的很多资料，只是近一段时间有空把它们整理了一下:)。

请问一下 再goland里 go get的时候 怎么添加-insecure选项

我macbook中的goland一直在落灰，基本没用过:(。这个问题，还是查看一下goland官方doc吧。