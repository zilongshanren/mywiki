---
title: Kuberize Ceph RBD API服务
url: https://tonybai.com/2016/11/21/kuberize-ceph-rbd-api-service/
published: '2016-11-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kuberize Ceph RBD API服务

在《[使用Ceph RBD为Kubernetes集群提供存储卷](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)》一文中，我们提到：借助[Kubernetes](http://tonybai.com/tag/kubernetes)和[Ceph](http://ceph.com/)的集成，Kubernetes可以使用Ceph RBD为集群内的Pod提供Persistent Volume。但这一过程中，RBD所使用的image的创建、删除还需要手动管理，于是我们又基于[go-ceph](https://github.com/ceph/go-ceph/)实现了[对RBD image的程序化管理](http://tonybai.com/2016/11/09/operate-ceph-rbd-images-with-go-ceph/)，我们的最终目标是要这种对RBD image的管理服务以一个K8s service的形式发布到Kubernetes集群中去，这就是本文标题中描述的那样：Kuberize Ceph RBD API服务。

#### 一、Dockerize Ceph RBD API服务

要想使得ceph rbd api Kuberizable，首先要Dockerize Ceph RBD API Service，即容器化。由于go-ceph是[Go语言](http://tonybai.com/tag/golang)开发，我们的rbd-rest-api同样用[Go语言](https://golang.org/)开发。使用Go语言开发有一个众所周知的好处，那就是可以编译为静态二进制文件，可以在运行时不依赖任何外部库，生来自带“适合容器”标签。但由于go-ceph是一个go binding for librados和librbd，其通过[cgo](http://tonybai.com/2012/09/26/interoperability-between-go-and-c/)实现Go语言对C库的链接和调用。这样一来，我们如果要做static linking，那么我们就要准备齐全所有librados和librbd所依赖的第三方库的.a(archive file)。如果你仅仅是执行下面编译命令，你将得到w行级别的错误信息输出：

```
$ go build --ldflags '-extldflags "-static"' .
```


从错误的信息中，我们可以得到rbd-rest-api静态编译依赖的各种第三方库，包括[boost](http://www.boost.org/)库（apt-get install libboost-all-dev)、libssl(apt-get install libssl)以及libnss3(apt-get install libnss3-dev)。安装好这些库，再修改一下命令行，可将编译错误输出降低到百行以内：

```
# go build --ldflags '-extldflags "-static -L /usr/lib/x86_64-linux-gnu -lboost_system -lboost_thread -lboost_iostreams -lboost_random -lcrypto -ldl -lpthread -lm -lz -lc -L /usr/lib/gcc/x86_64-linux-gnu/4.8/ -lstdc++"' .
```


不过，你将依旧得到诸多错误：

```
... ...
/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../../lib/librados.a(Crypto.o): In function `CryptoAESKeyHandler::init(ceph::buffer::ptr const&, std::basic_ostringstream<char, std::char_traits<char>, std::allocator<char> >&)':
/build/ceph-10.2.3/src/auth/Crypto.cc:280: undefined reference to `PK11_GetBestSlot'
/build/ceph-10.2.3/src/auth/Crypto.cc:291: undefined reference to `PK11_ImportSymKey'
/build/ceph-10.2.3/src/auth/Crypto.cc:304: undefined reference to `PK11_ParamFromIV'
/build/ceph-10.2.3/src/auth/Crypto.cc:282: undefined reference to `PR_GetError'
/build/ceph-10.2.3/src/auth/Crypto.cc:293: undefined reference to `PR_GetError'
... ...
```


这些”undefined reference”指向的符号都是[libnss3-dev库](https://github.com/nss-dev/nss)中的，但由于libnss3-dev的安装并没有包含libnss3.a文件，因此即便将libnss3显式放在链接参数列表中，比如：”-lnss3″也无法链接成功：

```
/usr/bin/ld: cannot find -lnss3
```


libnss库着实不是一个省油灯，经过几番折腾发现，要想使用libnss的static archive，我们只能手工编译，代码在这里可以获取到：https://github.com/nss-dev/nss，并且这里提供了nss的手工编译方法。

综上可以看出，纯静态编译rbd-rest-api是很繁琐的，于是我们这次选择默认的[动态链接](http://tonybai.com/2008/02/03/symbol-linkage-in-shared-library/)方式，我们只需在docker image中安装librados和librbd这两个依赖库即可，于是rbd-rest-api的Dockerfile的雏形可见：

```
From ubuntu:14.04
MAINTAINER Tony Bai <author@xxx.com>
# use aliyun source for ubuntu
# before building image ,make sure copy /etc/apt/sources.list here
# COPY sources.list /etc/apt/
RUN apt-get update && apt-get install -y --no-install-recommends librados-dev librbd-dev \
&& rm -rf /var/lib/apt/lists/*
RUN mkdir -p /root/rbd-rest-api
COPY rbd-rest-api /root/rbd-rest-api
COPY conf /root/rbd-rest-api/conf
RUN chmod +x /root/rbd-rest-api/rbd-rest-api
EXPOSE 8080
WORKDIR /root/rbd-rest-api
ENTRYPOINT ["/root/rbd-rest-api/rbd-rest-api"]
```


我们一直在Ubuntu 14.04.x环境下进行各种测试，于是我们自然而然的选择[ubuntu:14.04](http://tonybai.com/tag/ubuntu)作为我们的base image，构建镜像：

```
# docker build -t "test/rbd-rest-api" .
... ...
Setting up librados-dev (0.80.11-0ubuntu1.14.04.1) ...
Setting up librbd-dev (0.80.11-0ubuntu1.14.04.1) ...
Processing triggers for libc-bin (2.19-0ubuntu6.9) ...
---> c987abc7a24d
Removing intermediate container 5257ac37392a
Step 5 : RUN mkdir -p /root/rbd-rest-api
---> Running in dcabdb990c60
---> ce0db2a027aa
Removing intermediate container dcabdb990c60
Step 6 : COPY rbd-rest-api /root/rbd-rest-api
---> 453fd4b9a27a
Removing intermediate container 8b07b5de7537
Step 7 : COPY conf /root/rbd-rest-api/conf
---> e956add07d60
Removing intermediate container 6eaf6e4cf334
Step 8 : RUN chmod +x /root/rbd-rest-api/rbd-rest-api
---> Running in cb278d1919c7
---> 1e7b86072011
Removing intermediate container cb278d1919c7
Step 9 : EXPOSE 8080
---> Running in 6a3f457eefca
---> e60cefb50f77
Removing intermediate container 6a3f457eefca
Step 10 : WORKDIR /root/rbd-rest-api
---> Running in 703baf8c5564
---> 6f1a5e5e145c
Removing intermediate container 703baf8c5564
Step 11 : ENTRYPOINT /root/rbd-rest-api/rbd-rest-api
---> Running in 16dd4e7e3995
---> 43f885b958c7
Removing intermediate container 16dd4e7e3995
Successfully built 43f885b958c7
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
test/rbd-rest-api latest 43f885b958c7 57 seconds ago 298 MB
```


测试启动镜像，注意我们“只读”挂载了本地路径/etc/ceph：

```
# docker run --name rbd-rest-api --rm -p 8080:8080 -v /etc/ceph/:/etc/ceph/:ro test/rbd-rest-api
2016/11/14 14:58:17 [I] [asm_amd64.s:2086] http server Running on http://:8080
```


我们来测试一下这个Docker中的rbd-rest-api service：

```
# curl -v http://localhost:8080/api/v1/pools/
* Hostname was NOT found in DNS cache
* Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 8080 (#0)
> GET /api/v1/pools/ HTTP/1.1
> User-Agent: curl/7.35.0
> Host: localhost:8080
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Length: 130
< Content-Type: application/json; charset=utf-8
* Server beegoServer:1.7.1 is not blacklisted
< Server: beegoServer:1.7.1
< Date: Mon, 14 Nov 2016 14:59:29 GMT
<
{
"Kind": "PoolList",
"APIVersion": "v1",
"Items": [
{
"name": "rbd"
},
{
"name": "rbd1"
}
]
* Connection #0 to host localhost left intact
}
```


测试OK。

这里不得不提的是：如果你挂载的是仅仅是/etc/ceph/ceph.conf的话，那么当rbd-rest-api服务收到请求后，会返回：

```
Errcode=300, errmsg:
error rados: No such file or directory
```


这是因为容器中的rbd-rest-api没有看到ceph.client.admin.keyring，因此在登录ceph monitor时鉴权失败了。当然你也可以不映射本地目录，取而代之的是将/etc/ceph/ceph.conf和/etc/ceph/ceph.client.admin.keyring放入到镜像中，后一种方法这里就不详细描述了。librados给出的错误提示真是太差了，本来应该是一个权限的问题，居然说找不到librados。

#### 二、Kuberize Ceph RBD API服务

容器化测试成功了，接下来就是将Ceph RBD API Kuberize化。根据上面Docker镜像的设计，承载Ceph RBD API服务 Pod的Node上，必须要安装了Ceph client，即包括ceph.conf和ceph.client.admin.keyring，于是有选择性的调度Ceph RBD API服务到安装了ceph client的kubernetes node上是这一节必须考虑的问题。

我们的思路是将rbd-rest-api的pod通过k8s调度到带有指定label的k8s node上去，我们给kubernetes集群的node打标签，安装了ceph client的集群node，打的标签为：zone=ceph。

```
# kubectl label nodes 10.46.181.146 zone=ceph
# kubectl label nodes 10.47.136.60 zone=ceph
# kubectl get nodes --show-labels
NAME STATUS AGE LABELS
10.46.181.146 Ready 32d beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=10.46.181.146,zone=ceph
10.47.136.60 Ready 32d beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=10.47.136.60,zone=ceph
```


接下来就是在rbd-rest-api service的yaml中设定pod的调度策略了：

```
//rbd-rest-api.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: rbd-rest-api
spec:
replicas: 2
template:
metadata:
labels:
app: rbd-rest-api
spec:
containers:
- name: rbd-rest-api
image: registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest
#imagePullPolicy: IfNotPresent
imagePullPolicy: Always
ports:
- containerPort: 8080
volumeMounts:
- mountPath: /etc/ceph
name: ceph-default-config-volume
volumes:
- name: ceph-default-config-volume
hostPath:
path: /etc/ceph
nodeSelector:
zone: ceph
imagePullSecrets:
- name: rbd-rest-api-default-secret
---
apiVersion: v1
kind: Service
metadata:
name: rbd-rest-api
labels:
app: rbd-rest-api
spec:
ports:
- port: 8080
selector:
app: rbd-rest-api
```


我们可以看到在Deployment的spec中有一个[nodeSelector](http://kubernetes.io/docs/user-guide/node-selection/)，这个设置可以让k8s scheduler在调度service时只选择具备zone=ceph label的Node。注意关于imagePullSecrets的设置，可以参考《[Kubernetes从Private Registry中拉取容器镜像的方法](http://tonybai.com/2016/11/16/how-to-pull-images-from-private-registry-on-kubernetes-cluster/)》一文。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论