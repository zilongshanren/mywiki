---
title: 解决登录Harbor Registry时鉴权失败的问题
url: https://tonybai.com/2017/06/15/fix-auth-fail-when-login-harbor-registry/
published: '2017-06-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 解决登录Harbor Registry时鉴权失败的问题

今天在测试之前搭建好的[高可用Harbor](http://tonybai.com/2017/06/09/setup-a-high-availability-private-registry-based-on-harbor-and-cephfs/)时，发现了一个问题：使用docker login harbor时，有时成功，有时失败：

```
# docker login -u user -p passwd http://hub.my-domain.com:36666
Login Succeeded
# docker login -u user -p passwd http://hub.my-domain.com:36666
Error response from daemon: login attempt to http://hub.my-domain.com:36666/v2/ failed with status: 401 Unauthorized
```


我们在DNS中将hub.my-domain.com这个域名解析成两个IP，分别是两个Harbor节点的public IP，这可能是问题的诱发原因，但我还不知道问题根源在哪里。以下是问题的查找过程记录。

### 1、保证每个Harbor node都是可以login ok的

我在client端通过修改/etc/hosts将hub.my-domain.com分别解析成上述说到的两个node IP并测试。测试结果表明：无论单独解析成哪个IP，docker login http://hub.my-domain.com:36666都会100%的成功。

### 2、查看两个Harbor node上的registry log，弄清问题现象

将/etc/hosts中hub.my-domain.com的硬解析删除，恢复DNS解析。打开两个terminal tab分别监视连个Harbor node上的registry的日志。经过几次测试，发现一个现象：当docker login成功时，都是一个node上的日志出现更新；而当docker login fail时，我们会看到两个Node上的registry日志都有变化，*似乎请求发给了两个node*。

```
node1:
Jun 15 14:40:01 172.19.0.1 registry[30242]: time="2017-06-15T06:40:01.245822446Z" level=debug msg="authorizing request" go.version=go1.7.3 http.request.host="hub.my-domain.com:36666" http.request.id=62add46e-e176-4eb8-b36a-84a9fbe7ac9c http.request.method=GET http.request.remoteaddr=xx.xx.xx.xx http.request.uri="/v2/" http.request.useragent="docker/1.12.5 go/go1.6.4 git-commit/7392c3b kernel/4.4.0-58-generic os/linux arch/amd64 UpstreamClient(Docker-Client/1.12.5 \\(linux\\))" instance.id=43380207-7b61-4d45-b06a-a017c9a075af service=registry version="v2.4.1+unknown"
Jun 15 14:40:01 172.19.0.1 registry[30242]: time="2017-06-15T06:40:01.246002519Z" level=error msg="token signed by untrusted key with ID: \"BASH:RNPJ:PEBU:7THG:2NAR:OSFV:CG6U:ANV4:CCNB:ODZR:4BL6:TMD6\""
node2:
Jun 15 14:40:01 172.18.0.1 registry[28674]: time="2017-06-15T06:40:01.213604228Z" level=debug msg="authorizing request" go.version=go1.7.3 http.request.host="hub.my-domain.com:36666" http.request.id=bb6eeb8f-99f1-47a0-8cae-dae9b402b758 http.request.method=GET http.request.remoteaddr=xx.xx.xx.xx http.request.uri="/v2/" http.request.useragent="docker/1.12.5 go/go1.6.4 git-commit/7392c3b kernel/4.4.0-58-generic os/linux arch/amd64 UpstreamClient(Docker-Client/1.12.5 \\(linux\\))" instance.id=2a364e0c-425f-47a9-b144-887d439243ba service=registry version="v2.4.1+unknown"
Jun 15 14:40:01 172.18.0.1 registry[28674]: time="2017-06-15T06:40:01.21374491Z" level=warning msg="error authorizing context: authorization token required" go.version=go1.7.3 http.request.host="hub.my-domain.com:36666" http.request.id=bb6eeb8f-99f1-47a0-8cae-dae9b402b758 http.request.method=GET http.request.remoteaddr=xx.xx.xx.xx http.request.uri="/v2/" http.request.useragent="docker/1.12.5 go/go1.6.4 git-commit/7392c3b kernel/4.4.0-58-generic os/linux arch/amd64 UpstreamClient(Docker-Client/1.12.5 \\(linux\\))" instance.id=2a364e0c-425f-47a9-b144-887d439243ba service=registry version="v2.4.1+unknown"
Jun 15 14:40:01 172.18.0.1 registry[28674]: 172.18.0.3 - - [15/Jun/2017:06:40:01 +0000] "GET /v2/ HTTP/1.1" 401 87 "" "docker/1.12.5 go/go1.6.4 git-commit/7392c3b kernel/4.4.0-58-generic os/linux arch/amd64 UpstreamClient(Docker-Client/1.12.5 \\(linux\\))"
```


### 3、探寻Harbor原理，弄清问题根源

打开harbor在github.com的wiki页，在”[Architecture Overview of Harbor](https://github.com/vmware/harbor/wiki/Architecture-Overview-of-Harbor)“中我找到了docker login的流程：

![img{512x368}](../../assets/35f86f5c6f0bb56e.png)


从图片上，我一眼就看到了从docker client发出的*”两个请求: a和c流程”，看来docker client的确不止一次向Harbor发起了请求。wiki上对docker login流程给了简明扼要的解释。大致的流程是:

- docker向registry发起请求，由于registry是基于token auth的，因此registry回复应答，告诉docker client去哪个URL去获取token；
- docker client根据应答中的URL向token service(ui)发起请求，通过user和passwd获取token；如果user和passwd在db中通过了验证，那么token service将用自己的私钥(harbor/common/config/ui/private_key.pem)生成一个token，返回给docker client端；
- docker client获得token后再向registry发起login请求，registry用自己的证书(harbor/common/config/registry/root.crt)对token进行校验。通过则返回成功，否则返回失败。

从这个原理，我们可以知道问题就出在docker client多次向Harbor发起请求这个环节：对于每次请求，DNS会将域名可能解析为不同IP，因此不同请求可能落到不同的node上。这样当docker client拿着node1上token service分配的token去到node2的registry上鉴权时，就会出现鉴权失败的情况。

### 4、统一私钥和证书，问题得以解决

token service的私钥(harbor/common/config/ui/private_key.pem)和registry的证书(harbor/common/config/registry/root.crt)都是在prepare时生成的，两个节点都独立prepare过，因此两个node上的private_key.pem和root.crt是不同的，这就是问题根源。

解决这个问题很简单，就是统一私钥和证书。比如：将node1上的private_key.pem和root.crt复制到node2上，并重新创建node2上的container：

```
// node2上
将node1上的harbor/common/config/ui/private_key.pem复制到node2上的harbor/common/config/ui/private_key.pem；
将node1上的harbor/common/config/registry/root.crt复制到harbor/common/config/registry/root.crt；
$ docker-compose down -v
$ docker-compose up -d
```


更换了private_key.pem和root.crt的node2上的Harbor启动后，再进行login测试，就会100%成功了！

```
# docker login -u admin -p passwd http://hub.my-domain.com:36666
Login Succeeded
```


微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论