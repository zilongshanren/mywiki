---
title: 理解Docker的多阶段镜像构建
url: https://tonybai.com/2017/11/11/multi-stage-image-build-in-docker/
published: '2017-11-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 理解Docker的多阶段镜像构建

[Docker](http://tonybai.com/tag/docker)技术从[2013年诞生](https://www.infoq.com/news/2013/03/Docker)到目前已经4年有余了。对于已经接纳和使用[Docker技术](https://en.wikipedia.org/wiki/Docker_(software))在日常开发工作中的开发者而言，构建[Docker镜像](https://docs.docker.com/get-started)已经是家常便饭。但这是否意味着Docker的image构建机制已经相对完美了呢？不是的，Docker官方依旧在持续优化镜像构建机制。这不，从今年发布的[Docker 17.05版本](https://github.com/moby/moby/releases/tag/v17.05.0-ce)起，Docker开始支持容器镜像的[多阶段构建(multi-stage build)](https://docs.docker.com/engine/userguide/eng-image/multistage-build/)了。

什么是[镜像多阶段构建](https://docs.docker.com/engine/userguide/eng-image/multistage-build/)呢？直接给出概念定义太突兀，这里先卖个关子，我们先从日常开发中用到的镜像构建的方式和所遇到的镜像构建的问题说起。

## 一、同构的镜像构建

我们在做镜像构建时的一个常见的场景就是：应用在开发者自己的开发机或服务器上直接编译，编译出的二进制程序再打入镜像。这种情况一般要求编译环境与镜像所使用的base image是兼容的，比如说：我在[Ubuntu 14.04](https://hub.docker.com/_/ubuntu/)上编译应用，并将应用打入基于[ubuntu系列base image](https://hub.docker.com/_/ubuntu/)的镜像。这种构建我称之为“同构的镜像构建”，因为应用的编译环境与其部署运行的环境是兼容的：我在Ubuntu 14.04下编译出来的应用，可以基本无缝地在基于ubuntu:14.04及以后版本base image镜像(比如：16.04、16.10、17.10等)中运行；但在不完全兼容的base image中，比如[centos](https://hub.docker.com/_/centos/)中就可能会运行失败。

### 1、同构镜像构建举例

这里举个同构镜像构建的例子(后续的章节也是基于这个例子的)，注意：我们的编译环境为**Ubuntu 16.04 x86_64虚拟机、 Go 1.8.3和docker 17.09.0-ce**。

我们用一个Go语言中最常见的http server作为例子：

```
// github.com/bigwhite/experiments/multi_stage_image_build/isomorphism/httpserver.go
package main
import (
"net/http"
"log"
"fmt"
)
func home(w http.ResponseWriter, req *http.Request) {
w.Write([]byte("Welcome to this website!\n"))
}
func main() {
http.HandleFunc("/", home)
fmt.Println("Webserver start")
fmt.Println(" -> listen on port:1111")
err := http.ListenAndServe(":1111", nil)
if err != nil {
log.Fatal("ListenAndServe:", err)
}
}
```


编译这个程序：

```
# go build -o myhttpserver httpserver.go
# ./myhttpserver
Webserver start
-> listen on port:1111
```


这个例子看起来很简单，也没几行代码，但背后Go net/http包在底层做了大量的事情，包括很多系统调用，能够反映出应用与操作系统的“耦合”，这在后续的讲解中会体现出来。接下来我们就来为这个程序构建一个docker image，并基于这个image来启动一个myhttpserver容器。我们选择ubuntu:14.04作为base image：

```
// github.com/bigwhite/experiments/multi_stage_image_build/isomorphism/Dockerfile
From ubuntu:14.04
COPY ./myhttpserver /root/myhttpserver
RUN chmod +x /root/myhttpserver
WORKDIR /root
ENTRYPOINT ["/root/myhttpserver"]
执行构建：
# docker build -t myrepo/myhttpserver:latest .
Sending build context to Docker daemon 5.894MB
Step 1/5 : FROM ubuntu:14.04
---> dea1945146b9
Step 2/5 : COPY ./myhttpserver /root/myhttpserver
---> 993e5129c081
Step 3/5 : RUN chmod +x /root/myhttpserver
---> Running in 104d84838ab2
---> ebaeca006490
Removing intermediate container 104d84838ab2
Step 4/5 : WORKDIR /root
---> 7afdc2356149
Removing intermediate container 450ccfb09ffd
Step 5/5 : ENTRYPOINT /root/myhttpserver
---> Running in 3182766e2a68
---> 77f315e15f14
Removing intermediate container 3182766e2a68
Successfully built 77f315e15f14
Successfully tagged myrepo/myhttpserver:latest
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
myrepo/myhttpserver latest 77f315e15f14 18 seconds ago 200MB
# docker run myrepo/myhttpserver
Webserver start
-> listen on port:1111
```


以上是最基本的image build方法。

接下来，我们可能会遇到如下需求：

* 搭建一个Go程序的构建环境有时候是很耗时的，尤其是对那些依赖很多第三方开源包的Go应用来说，下载包就需要很长时间。我们最好将这些易变的东西统统打包到一个用于Go程序构建的builder image中；

* 我们看到上面我们构建出的myrepo/myhttpserver image的SIZE是200MB，这似乎有些过于“庞大”了。虽然每个主机node上的docker有cache image layer的能力，但我们还是希望能build出更加精简短小的image。

### 2、借助golang builder image

Docker Hub上提供了一个带有go dev环境的官方[golang image repository](https://hub.docker.com/_/golang/)，我们可以直接使用这个golang builder image来辅助构建我们的应用image；对于一些对第三方包依赖较多的Go应用，我们也可以以这个golang image为base image定制我们自己的专用builder image。

我们基于golang:latest这个base image构建我们的golang-builder image，我们编写一个Dockerfile.build用于build golang-builder image:

```
// github.com/bigwhite/experiments/multi_stage_image_build/isomorphism/Dockerfile.build
FROM golang:latest
WORKDIR /go/src
COPY httpserver.go .
RUN go build -o myhttpserver ./httpserver.go
```


在同目录下构建golang-builder image:

```
# docker build -t myrepo/golang-builder:latest -f Dockerfile.build .
Sending build context to Docker daemon 5.895MB
Step 1/4 : FROM golang:latest
---> 1a34fad76b34
Step 2/4 : WORKDIR /go/src
---> 2361824677d3
Removing intermediate container 01d8f4e9f0c4
Step 3/4 : COPY httpserver.go .
---> 1ff14bb0bc56
Step 4/4 : RUN go build -o myhttpserver ./httpserver.go
---> Running in 37a1b76b7b9e
---> 2ac5347bb923
Removing intermediate container 37a1b76b7b9e
Successfully built 2ac5347bb923
Successfully tagged myrepo/golang-builder:latest
REPOSITORY TAG IMAGE ID CREATED SIZE
myrepo/golang-builder latest 2ac5347bb923 3 minutes ago 739MB
```


接下来，我们就基于golang-builder中已经build完毕的myhttpserver来构建我们最终的应用image：

```
# docker create --name appsource myrepo/golang-builder:latest
# docker cp appsource:/go/src/myhttpserver ./
# docker rm -f appsource
# docker rmi myrepo/golang-builder:latest
# docker build -t myrepo/myhttpserver:latest .
```


这段命令的逻辑就是从基于golang-builder image启动的容器appsource中将已经构建完毕的myhttpserver拷贝到主机当前目录中，然后删除临时的container appsource以及上面构建的那个golang-builder image；最后的步骤和第一个例子一样，基于本地目录中的已经构建完的myhttpserver构建出最终的image。为了方便，你也可以将这一系列命令放到一个Makefile中去。

### 3、使用size更小的alpine image

builder image并不能帮助我们为最终的应用image“减重”，myhttpserver image的Size依旧停留在200MB。要想“减重”，我们需要更小的base image，我们选择了[alpine](https://hub.docker.com/_/alpine/)。[Alpine image](https://news.ycombinator.com/item?id=10782897)的size不到4M，再加上应用的size，最终应用Image的Size估计可以缩减到20M以下。

结合builder image，我们只需将Dockerfile的base image改为alpine:latest：

```
// github.com/bigwhite/experiments/multi_stage_image_build/isomorphism/Dockerfile.alpine
From alpine:latest
COPY ./myhttpserver /root/myhttpserver
RUN chmod +x /root/myhttpserver
WORKDIR /root
ENTRYPOINT ["/root/myhttpserver"]
```


构建alpine版应用image:

```
# docker build -t myrepo/myhttpserver-alpine:latest -f Dockerfile.alpine .
Sending build context to Docker daemon 6.151MB
Step 1/5 : FROM alpine:latest
---> 053cde6e8953
Step 2/5 : COPY ./myhttpserver /root/myhttpserver
---> ca0527a62d39
Step 3/5 : RUN chmod +x /root/myhttpserver
---> Running in 28d0a8a577b2
---> a3833af97b5e
Removing intermediate container 28d0a8a577b2
Step 4/5 : WORKDIR /root
---> 667345b78570
Removing intermediate container fa59883e9fdb
Step 5/5 : ENTRYPOINT /root/myhttpserver
---> Running in adcb5b976ca3
---> 582fa2aedc64
Removing intermediate container adcb5b976ca3
Successfully built 582fa2aedc64
Successfully tagged myrepo/myhttpserver-alpine:latest
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
myrepo/myhttpserver-alpine latest 582fa2aedc64 4 minutes ago 16.3MB
```


16.3MB，Size的确降下来了！我们基于该image启动一个容器，看应用运行是否有什么问题：

```
# docker run myrepo/myhttpserver-alpine:latest
standard_init_linux.go:185: exec user process caused "no such file or directory"
```


容器启动失败了！为什么呢？因为alpine image并非ubuntu环境的同构image。我们在下面详细说明。

## 二、异构的镜像构建

我们的image builder: myrepo/golang-builder:latest是基于golang:latest这个image。[golang base image](https://github.com/docker-library/golang/)有两个模板：Dockerfile-debain.template和Dockerfile-alpine.template。而golang:latest是基于debian模板的，与ubuntu兼容。构建出来的myhttpserver对[动态共享链接库](http://tonybai.com/2010/12/13/also-talk-about-shared-library/)的情况如下：

```
# ldd myhttpserver
linux-vdso.so.1 => (0x00007ffd0c355000)
libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007ffa8b36f000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ffa8afa5000)
/lib64/ld-linux-x86-64.so.2 (0x000055605ea5d000)
```


[debian](https://www.debian.org/)系的linux distribution使用了[glibc](http://tonybai.com/2009/04/11/glibc-strlen-source-analysis/)。但alpine则不同，[alpine](https://alpinelinux.org/)使用的是[musl libc](http://www.musl-libc.org/)的实现，因此当我们运行上面的那个容器时，[加载器](http://tonybai.com/2008/02/03/symbol-linkage-in-shared-library/)因找不到myhttpserver依赖的libc.so.6而失败退出。

这种构建环境与运行环境不兼容的情况我这里称之为“异构的镜像构建”。那么如何解决这个问题呢？我们继续看：

### 1、静态构建

在主流编程语言中，[Go的移植性](http://tonybai.com/2017/06/27/an-intro-about-go-portability/)已经是数一数二的了，尤其是[Go 1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)之后，Go将runtime中的C代码都用Go重写了，对libc的依赖已经降到最低了，但仍有一些feature提供了两个版本的实现：[C实现](http://tonybai.com/tag/c)和Go实现。并且默认情况下，即在CGO_ENABLED=1的情况下，程序和预编译的标准库都采用了C的实现。关于这方面的详细论述请参见我之前写的[《也谈Go的可移植性》](http://tonybai.com/2017/06/27/an-intro-about-go-portability/)一文，这里就不赘述了。于是采用了不同libc实现的debian系和alpine系自然存在不兼容的情况。要解决这个问题，我们首先考虑对Go程序进行静态构建，然后将静态构建后的Go应用放入alpine image中。

我们修改一下Dockerfile.build，在编译Go源文件时加上CGO_ENABLED=0：

```
// github.com/bigwhite/experiments/multi_stage_image_build/heterogeneous/Dockerfile.build
FROM golang:latest
WORKDIR /go/src
COPY httpserver.go .
RUN CGO_ENABLED=0 go build -o myhttpserver ./httpserver.go
```


构建这个builder image：

```
# docker build -t myrepo/golang-static-builder:latest -f Dockerfile.build .
Sending build context to Docker daemon 4.096kB
Step 1/4 : FROM golang:latest
---> 1a34fad76b34
Step 2/4 : WORKDIR /go/src
---> 593cd9692019
Removing intermediate container ee005d487ad5
Step 3/4 : COPY httpserver.go .
---> a095eb69e716
Step 4/4 : RUN CGO_ENABLED=0 go build -o myhttpserver ./httpserver.go
---> Running in d9f3b3a6c36c
---> c06fe8dccbad
Removing intermediate container d9f3b3a6c36c
Successfully built c06fe8dccbad
Successfully tagged myrepo/golang-static-builder:latest
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
myrepo/golang-static-builder latest c06fe8dccbad 31 seconds ago 739MB
```


接下来，我们再基于golang-static-builder中已经build完毕的静态连接的myhttpserver来构建我们最终的应用image：

```
# docker create --name appsource myrepo/golang-static-builder:latest
# docker cp appsource:/go/src/myhttpserver ./
# ldd myhttpserver
not a dynamic executable
# docker rm -f appsource
# docker rmi myrepo/golang-static-builder:latest
# docker build -t myrepo/myhttpserver-alpine:latest -f Dockerfile.alpine .
```


运行新image:

```
# docker run myrepo/myhttpserver-alpine:latest
Webserver start
-> listen on port:1111
```


Note: 我们可以用strace来证明静态连接时Go只使用的是Go自己的runtime实现，而并未使用到libc.a中的代码：

```
# CGO_ENABLED=0 strace -f go build httpserver.go 2>&1 | grep open | grep -o '/.*\.a' > go-static-build-strace-file-open.txt
```


打开[go-static-build-strace-file-open.txt](http://tonybai.com/wp-content/uploads/go-static-build-strace-file-open.txt)文件查看文件内容，你不会找到libc.a这个文件（在Ubuntu下，一般libc.a躺在/usr/lib/x86_64-linux-gnu/下面），这说明go build根本没有尝试去open libc.a文件并获取其中的符号定义。

### 2、使用alpine golang builder

我们的Go应用运行在alpine based的container中，我们可以使用alpine golang builder来构建我们的应用(无需静态链接)。前面提到过golang有alpine模板：

```
REPOSITORY TAG IMAGE ID CREATED SIZE
golang alpine 9e3f14138abd 7 days ago 269MB
```


alpine版golang builder的Dockerfile内容如下：

```
//github.com/bigwhite/experiments/multi_stage_image_build/heterogeneous/Dockerfile.alpine.build
FROM golang:alpine
WORKDIR /go/src
COPY httpserver.go .
RUN go build -o myhttpserver ./httpserver.go
```


后续的操作与前面golang builder的操作并不二致：利用alpine golang builder构建我们的应用，并将其打入alpine image，这里就不赘述了。

## 三、多阶段镜像构建：提升开发者体验

在Docker 17.05以前，我们都是像上面那样构建镜像的。你会发现即便采用异构image builder模式，我们也要维护两个Dockerfile，并且还要在docker build命令之外执行一些诸如从容器内copy应用程序、清理build container和build image等的操作。Docker社区看到了这个问题，于是实现了[多阶段镜像构建机制](https://docs.docker.com/engine/userguide/eng-image/multistage-build/)（multi-stage）。

我们先来看一下针对上面例子，multi-stage build所使用Dockerfile：

```
//github.com/bigwhite/experiments/multi_stage_image_build/multi_stages/Dockerfile
FROM golang:alpine as builder
WORKDIR /go/src
COPY httpserver.go .
RUN go build -o myhttpserver ./httpserver.go
From alpine:latest
WORKDIR /root/
COPY --from=builder /go/src/myhttpserver .
RUN chmod +x /root/myhttpserver
ENTRYPOINT ["/root/myhttpserver"]
```


看完这个Dockerfile的内容，你的第一赶脚是不是把之前的两个Dockerfile合并在一块儿了，每个Dockerfile单独作为一个“阶段”！事实也是这样，但这个Docker也多了一些新的语法形式，用于建立各个“阶段”之间的联系。针对这样一个Dockerfile，我们应该知道以下几点：

- 支持Multi-stage build的Dockerfile在以往的多个build阶段之间建立内在连接，让后一个阶段构建可以使用前一个阶段构建的产物，形成一条构建阶段的chain；
- Multi-stages build的最终结果仅产生一个image，避免产生冗余的多个临时images或临时容器对象，这正是我们所需要的：我们只要结果。

我们来使用multi-stage来build一下上述例子：

```
# docker build -t myrepo/myhttserver-multi-stage:latest .
Sending build context to Docker daemon 3.072kB
Step 1/9 : FROM golang:alpine as builder
---> 9e3f14138abd
Step 2/9 : WORKDIR /go/src
---> Using cache
---> 7a99431d1be6
Step 3/9 : COPY httpserver.go .
---> 43a196658e09
Step 4/9 : RUN go build -o myhttpserver ./httpserver.go
---> Running in 9e7b46f68e88
---> 90dc73912803
Removing intermediate container 9e7b46f68e88
Step 5/9 : FROM alpine:latest
---> 053cde6e8953
Step 6/9 : WORKDIR /root/
---> Using cache
---> 30d95027ee6a
Step 7/9 : COPY --from=builder /go/src/myhttpserver .
---> f1620b64c1ba
Step 8/9 : RUN chmod +x /root/myhttpserver
---> Running in e62809993a22
---> 6be6c28f5fd6
Removing intermediate container e62809993a22
Step 9/9 : ENTRYPOINT /root/myhttpserver
---> Running in e4000d1dde3d
---> 639cec396c96
Removing intermediate container e4000d1dde3d
Successfully built 639cec396c96
Successfully tagged myrepo/myhttserver-multi-stage:latest
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
myrepo/myhttserver-multi-stage latest 639cec396c96 About an hour ago 16.3MB
```


我们来Run一下这个image：

```
# docker run myrepo/myhttserver-multi-stage:latest
Webserver start
-> listen on port:1111
```


## 四、小结

多阶段镜像构建可以让开发者通过一个Dockerfile，一次性地、更容易地构建出size较小的image，体验良好并且更容易接入CI/CD等自动化系统。不过当前多阶段构建仅是在Docker 17.05及之后的版本中才能得到支持。如果想学习和实践这方面功能，但又没有环境，可以使用[play-with-docker](https://labs.play-with-docker.com/)提供的实验环境。

![img{512x368}](../../assets/9cce36afbc6ee8fd.png)


Play with Docker labs

以上所有示例代码可以在

[这里]下载到。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

在最先前的例子里，为什么不直接在myhttpserver里打包呢，这样就在一个container里打包，并且运行。

为什么要把打包的过程专门提取出来？

谢谢！

您说的这种构建方式得到的结果是：1、打包时间更为漫长，至少首次是这样，因为在容器里搭建编译环境需要很长时间；2、打包出来的image size太过庞大。如果按照我文中的思路，您的这种方式应该是在我的第一个例子之前。

不过您说的方式的确是大多数人刚入门docker时最喜欢用的镜像构建方法。这倒是提醒我了，3ks。

您好，您这样执行的时候不会出现临时镜像吗？

我执行多阶段构建之后出现了一个镜像：

CentOS /tmp/app docker build -t react-app:latest . [15:06:46]

Sending build context to Docker daemon 370.2kB

Step 1/7 : FROM node:alpine as build-deps

—> 466bcf8bf36e

Step 2/7 : COPY ./react-app /tmp/react-app

—> f8dfedb48209

Step 3/7 : RUN cd /tmp/react-app && yarn && yarn run build

—> Running in 75c1e9b08a1c

yarn install v1.3.2

[1/4] Resolving packages…

[2/4] Fetching packages…

info fsevents@1.1.2: The platform “linux” is incompatible with this module.

info “fsevents@1.1.2″ is an optional dependency and failed compatibility check. Excluding it from installation.

info fsevents@1.1.3: The platform “linux” is incompatible with this module.

info “fsevents@1.1.3″ is an optional dependency and failed compatibility check. Excluding it from installation.

[3/4] Linking dependencies…

[4/4] Building fresh packages…

success Saved lockfile.

Done in 11.63s.

yarn run v1.3.2

$ react-scripts build

Creating an optimized production build…

Compiled successfully.

File sizes after gzip:

35.65 KB build/static/js/main.35d639b7.js

299 B build/static/css/main.c17080f1.css

The project was built assuming it is hosted at the server root.

To override this, specify the homepage in your package.json.

For example, add this to build it for GitHub Pages:

“homepage” : “http://myname.github.io/myapp”,

The build folder is ready to be deployed.

You may serve it with a static server:

yarn global add serve

serve -s build

Done in 4.99s.

Removing intermediate container 75c1e9b08a1c

—> 548f099870d7

Step 4/7 : FROM nginx:alpine

—> e9b19873bc49

Step 5/7 : COPY –from=build-deps /tmp/react-app/build /usr/share/nginx/html

—> e5b5fbd38b17

Step 6/7 : EXPOSE 80

—> Running in 1ce462466f6d

Removing intermediate container 1ce462466f6d

—> 0bda3fdfed18

Step 7/7 : CMD ["nginx", "-g", "daemon off;"]

—> Running in 2b77e31095ab

Removing intermediate container 2b77e31095ab

—> 77848deca49d

Successfully built 77848deca49d

Successfully tagged react-app:latest

cyl at CentOS /tmp/app docker image ls [15:08:01]

REPOSITORY TAG IMAGE ID CREATED SIZE

react-app latest 77848deca49d 28 seconds ago 17.4MB

548f099870d7 29 seconds ago 295MB

我在ubuntu 16.04上使用docker 17.09构建的镜像没有发现临时镜像啊。

我尝试了一下ubuntu 16.04 docker 17.12ce 构建，构建完成后运行docker image ls，还是出现了临时镜像：

REPOSITORY TAG IMAGE ID CREATED SIZE

react-app latest b866c5ab8a51 4 seconds ago 17.4MB

7a5b51d49acb 5 seconds ago 302MB

nginx alpine e9b19873bc49 9 days ago 16.8MB

node alpine 466bcf8bf36e 3 weeks ago 67.6MB

我和您的差异应该就只差docker版本了吧，是不是这个版本引起的问题，还是我的Dockerfile写得不对？劳驾您帮我看看我的Dockerfile :

FROM node:alpine as builder

RUN yarn global add create-react-app && cd /tmp && create-react-app app && cd app && yarn run build

FROM nginx:alpine

COPY –from=builder /tmp/app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

不好意思才发现这个输入工具防xss直接把我说那个临时镜像的名称给过滤了，我试一下转义能不能输入进来：

REPOSITORY TAG IMAGE ID CREATED SIZE

react-app latest b866c5ab8a51 4 seconds ago 17.4MB

<none> <none> 7a5b51d49acb 5 seconds ago 302MB

nginx alpine e9b19873bc49 9 days ago 16.8MB

node alpine 466bcf8bf36e 3 weeks ago 67.6MB

这回我终于看清了。原来你说的是 这种中间image啊，我的build也存在，当然不光是多阶段构建，普通构建也是会产生这种中间image。我之前以为您说的是一次build，出来了两个具名镜像呢。:) 这个:就是docker build的一种cache机制，为了加快后续build的速度。docker官方似乎不把这个问题当成”bug”。你是否发现第二次以及后续执行docker build构建时的speed非常快。如果你每次都用docker built –no-cache，那么每次都会“产生”一个或多个的中间镜像。如果看着不顺眼，新版本的docker可以使用“ docker system prune”清理。关于这类image ，这篇文章解释的不错，可以看看 https://www.projectatomic.io/blog/2015/07/what-are-docker-none-none-images/

嗯，感谢感谢，我后来也看大家说这种缓存机制会有不少帮助，所以中间none镜像不应该被默认删除。

条理清晰的好文章，解答了我的疑惑，顶