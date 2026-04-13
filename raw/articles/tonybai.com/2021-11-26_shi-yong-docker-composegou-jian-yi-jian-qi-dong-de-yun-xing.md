---
title: 使用Docker Compose构建一键启动的运行环境
url: https://tonybai.com/2021/11/26/build-all-in-one-runtime-environment-with-docker-compose/
published: '2021-11-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Docker Compose构建一键启动的运行环境

![](../../assets/561f3c9d2ebdfded.png)


[本文永久链接](https://tonybai.com/2021/11/26/build-all-in-one-runtime-environment-with-docker-compose) – https://tonybai.com/2021/11/26/build-all-in-one-runtime-environment-with-docker-compose

如今，不管你是否喜欢，不管你是否承认，微服务架构模式的流行就摆在那里。作为架构师的你，如果再将系统设计成个大单体结构，那么即便不懂技术的领导，都会给你送上几次白眼。好吧，妥协了！开拆！“没吃过猪肉，还没见过猪跑吗！”。拆不出40-50个服务，我就不信还拆不出4-5个服务^_^。

终于拆出了几个服务，但又犯难了：以前单体程序，搭建一个运行环境十分easy，程序往一个主机上一扔，配置配置，启动就ok了；但自从拆成服务后，开发人员的调试环境、集成环境、测试环境等搭建就变得异常困难。

有人会说，现在都云原生了？你不知道[云原生操作系统k8s](https://kubernetes.io)的存在么？让运维帮你在k8s上整环境啊。 一般小厂，运维人员不多且很忙，开发人员只能“自力更生，丰衣足食”。开发人员自己整k8s？别扯了！没看到这两年k8s变得越来越复杂了吗！如果有一年不紧跟k8s的演进，新版本中的概念你就可能很陌生，不知源自何方。一般开发人员根本搞不定(如果你想搞定，可以看看[我的k8s实战课程](https://coding.imooc.com/class/284.html)哦，包教包会^_^)。

那怎么办呢？角落里**曾经的没落云原生贵族docker**发话了：要不让我兄弟试试！

### 1. docker compose

[docker](https://tonybai.com/2017/12/21/the-concise-history-of-docker-image-building)虽然成了“过气网红”，但docker依然是容器界的主流。至少对于非docker界的开发人员来说，一提到容器，大家首先想到的还是docker。

docker公司的产品推出不少，开发人员对多数都不买账也是现实，但我们也不能一棒子打死，毕竟docker是可用的，还有一个可用的，那就是docker的兄弟：[docker compose](https://docs.docker.com/compose/)。

Compose是一个用于定义和运行多容器Docker应用程序的工具。使用Compose，我们可以使用一个[YAML文件](https://tonybai.com/2019/02/25/introduction-to-yaml-creating-a-kubernetes-deployment/)来配置应用程序的所有服务组件。然后，只需一条命令，我们就可以创建并启动配置中的所有服务。

**这不正是我们想要的工具么**! Compose与k8s很像，都算是容器编排工具，最大的不同：Compose更适合在单节点上的调试或集成环境中（虽然也支持跨主机，基于被淘汰的docker swarm)。Compose可以大幅提升开发人员以及测试人员搭建应用运行环境的效率。

### 2. 选版本

使用docker compose搭建运行环境，我们仅需一个yml文件。但docker compose工具也经历了多年演化，这个文件的语法规范也有多个版本，截至目前，docker compose的配置文件的语法版本就有2、2.x和3.x三种。并且不同规范版本支持的docker引擎版本还不同，这个对应关系如下图。图来自[docker compose文件规范页面](https://docs.docker.com/compose/compose-file/)：

![](../../assets/1ecd08e17f1c7676.png)


选版本是最闹心的。选哪个呢？设定两个条件：

- docker引擎版本怎么也得是17.xx
- 规范版本怎么也得是3.x吧

这样一来，版本3.2是最低要求的了。我们就选3.2：

```
// docker-compose.yml
version: "3.2"
```


### 3. 选网络

docker compose默认会为docker-compose.yml中的各个service创建一个bridge网络，所有service在这个网络里可以相互访问。以下面docker-compose.yml为例：

```
// demo1/docker-compose.yml
version: "3.2"
services:
srv1:
image: nginx:latest
container_name: srv1
srv2:
image: nginx:latest
container_name: srv2
```


启动这个yml中的服务：

```
# docker-compose -f docker-compose.yml up -d
Creating network "demo1_default" with the default driver
... ...
```


docker compose会为这组容器创建一个名为demo1_default的桥接网络:

```
# docker network ls
NETWORK ID NAME DRIVER SCOPE
f9a6ac1af020 bridge bridge local
7099c68b39ec demo1_default bridge local
... ...
```


关于demo1_default网络的细节，可以通过docker network inspect 7099c68b39ec获得。

对于这样的网络中的服务，我们在外部是无法访问的。如果要访问其中服务，我们需要对其中的服务做端口映射，比如如果我们要将srv1暴露到外部，我们可以将srv1监听的服务端口80映射到主机上的某个端口，这里用8080，修改后的docker-compose.yml如下：

```
version: "3.2"
services:
srv1:
image: nginx:latest
container_name: srv1
ports:
- "8080:80"
srv2:
image: nginx:latest
container_name: srv2
```


这样启动该组容器后，我们通过curl localhost:8080就可以访问到容器中的srv1服务。不过这种情况下，服务间的相互发现比较麻烦，要么借助于外部的发现服务，要么通过容器间的link来做。

开发人员大多只有一个环境，不同服务的服务端口亦不相同，让容器使用host网络要比单独创建一个bridge网络来的更加方便。通过network_mode我们可以指定服务使用host网络，就像下面这样：

```
version: "3.2"
services:
srv1:
image: bigwhite/srv1:1.0.0
container_name: srv1
network_mode: "host"
```


在host网络下，容器监听的端口就是主机上的端口，各个服务间通过端口区别各个服务实例(前提是端口各不相同)，ip使用localhost即可。

使用host网络还有一个好处，那就是我们在该环境之外的主机上访问环境中的服务也十分方便，比如查看prometheus的面板等。

### 4. 依赖的中间件先启动，预置配置次之

如今的微服务架构系统，除了自身实现的服务外，外围还有大量其依赖的中间件，比如：redis、kafka(mq)、nacos/etcd(服务发现与注册）、prometheus(时序度量数据服务)、mysql(关系型数据库)、jaeger server(trace服务器)、elastic(日志中心)、pyroscope-server(持续profiling服务)等。

这些中间件若没有启动成功，我们自己的服务多半启动都要失败，因此我们要保证这些中间件服务都启动成功后，再来启动我们自己的服务。

如何做呢？compose规范中有一个[迷惑人的“depends_on”](https://docs.docker.com/compose/compose-file/compose-file-v3/#depends_on)，比如下面配置文件中srv1依赖redis和nacos两个service：

```
version: "3.2"
services:
srv1:
image: bigwhite/srv1:1.0.0
container_name: srv1
network_mode: "host"
depends_on:
- "redis"
- "nacos"
environment:
- NACOS_SERVICE_ADDR=127.0.0.1:8848
- REDIS_SERVICE_ADDR=127.0.0.1:6379
restart: on-failure
```


不深入了解，很多人会认为depends_on可以保证先启动依赖项redis和nacos，并等依赖项ready后再启动我们自己的服务srv1。但实际上，depends_on仅能保证先启动依赖项，后启动我们的服务。但它不会探测依赖项redis或nacos是否ready，也不会等依赖项ready后，才启动我们的服务。于是你会看到srv1启动后依旧出现各种的报错，包括无法与redis、nacos建立连接等。

要想真正实现依赖项ready后才启动我们自己的服务，我们需要借助外部工具了，[docker compose文档对此有说明](https://docs.docker.com/compose/startup-order/)。其中一个方法是使用[wait-for-it脚本](https://github.com/vishnubob/wait-for-it)。

我们可以改变一下自由服务的容器镜像，将其entrypoint从执行服务的可执行文件变为执行一个start.sh的脚本：

```
// Dockerfile
... ...
ENTRYPOINT ["/bin/bash", "./start.sh"]
```


这样我们就可以在start.sh脚本中“定制”我们的启动逻辑了。下面是一个start.sh脚本的示例：

```
#! /bin/sh
./wait_for_it.sh $NACOS_SERVICE_ADDR -t 60 --strict -- echo "nacos is up" && \
./wait_for_it.sh $REDIS_SERVICE_ADDR -- echo "redis is up" && \
exec ./srv1
```


我们看到，在start.sh脚本中，我们使用[wait_for_it.sh脚本](https://github.com/vishnubob/wait-for-it/blob/master/wait-for-it.sh)等待nacos和redis启动，如果在限定时间内等待失败，根据restart策略，我们的服务还会被docker compose重新拉起，直到nacos与redis都ready，我们的服务才会真正开始执行启动过程。

在exec ./srv1之前，很多时候我们还需要进行一些配置初始化操作，比如向nacos中写入预置的srv1服务的配置文件内容以保证srv1启动后能从nacos中读取到自己的配置文件，下面是加了配置初始化的start.sh：

```
#! /bin/sh
./wait_for_it.sh $NACOS_SERVICE_ADDR -t 60 --strict -- echo "nacos is up" && \
./wait_for_it.sh $REDIS_SERVICE_ADDR -- echo "redis is up" && \
curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' -d dataId=srv1.yml --data-urlencode content@./conf/srv1.yml "http://127.0.0.1:8848/nacos/v1/cs/configs?group=MY_GROUP" && \
exec ./srv1
```


我们通过curl将打入镜像的./conf/srv1.yml配置写入已经启动了的nacos中供后续srv1启动时读取。

### 5. 全家桶，一应俱全

就像前面提到的，如今的系统对外部的中间件“依存度”很高，好在主流中间件都提供了基于docker启动的官方支持。这样我们的开发环境也可以是一个一应俱全的“全家桶”。不过要有一个很容易满足的前提：你的机器配置足够高，才能把这些中间件全部运行起来。

有了这些全家桶，我们无论是诊断问题(看log、看trace、看度量数据），还是作性能优化（看持续profiling的数据），都方便的不要不要的。

### 6. 结合Makefile，简化命令行输入

docker-compose这个工具有一个“严重缺陷”，那就是名字太长^_^。这导致我们每次操作都要敲入很多命令字符，当你使用的compose配置文件名字不为docker-compose.yml时，更是如此，我们还需要通过-f选项指定配置文件路径。

为了简化命令行输入，减少键盘敲击次数，我们可以将复杂的docker-compose命令与Makefile相结合，通过定制命令行命令并将其赋予简单的make target名字来实现这一简化目标，比如：

```
// Makefile
pull:
docker-compose -f my-docker-compose.yml pull
pull-my-system:
docker-compose -f my-docker-compose.yml pull srv1 srv2 srv3
up: pull-my-system
docker-compose -f my-docker-compose.yml up
upd: pull-my-system
docker-compose -f my-docker-compose.yml up -d
up2log: pull-my-system
docker-compose -f my-docker-compose.yml up > up.log 2>&1
down:
docker-compose -f my-docker-compose.yml down
ps:
docker-compose -f my-docker-compose.yml ps -a
log:
docker-compose -f my-docker-compose.yml logs -f
# usage example: make upsrv service=srv1
service=
upsrv:
docker-compose -f my-docker-compose.yml up -d ${service}
config:
docker-compose -f my-docker-compose.yml config
```


另外服务依赖的中间件一般都时启动与运行开销较大的系统，每次和我们的服务一起启停十分浪费时间，我们可以将这些依赖与我们的服务分别放在不同的compose配置文件中管理，这样我们每次重启自己的服务时，没有必要重新启动这些依赖，这样可以节省大量“等待”时间。

### 7. .env文件

有些时候，我们需要在compose的配置文件中放置一些“变量”，我们通常使用环境变量来实现“变量”的功能，比如：我们将srv1的镜像版本改为一个环境变量：

```
version: "3.2"
services:
srv1:
image: bigwhite/srv1:${SRV1_VER}
container_name: srv1
network_mode: "host"
... ...
```


docker compose支持通过同路径下的.env文件的方式docker-compose.yml中环境变量的值，比如：

```
// .env
SRV1_VER=dev
```


这样docker compose在启动srv1时会将.env中SRV1_VER的值读取出来并替换掉compose配置文件中的相应环境变量。通过这种方式，我们可以灵活的修改我们使用的镜像版本。

### 8. 优点与不足

使用docker compose工具，我们可以轻松拥有并快速启动一个all-in-one的运行环境，大幅度加速了部署、调试与测试的效率，在特定的工程环节，它可以给予开发与测试人员很大帮助。

不过这样的运行环境也有一些不足，比如：

- 对部署的机器/虚拟机配置要求较高；
- 这样的运行环境有局限，用在功能测试、持续集成、验收测试的场景下可以，但不能用来执行压测或者说即便压测也只是摸底，数据不算数的，因为所有服务放在一起，相互干扰；
- 服务或中间件多了以后，完全启动一次也要耐心等待一段时间。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


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


微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论