---
title: 部署私有Docker Registry
url: https://tonybai.com/2016/02/26/deploy-a-private-docker-registry/
published: '2016-02-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 部署私有Docker Registry

安装部署一个私有的Docker Registry是引入、学习和使用[Docker](https://github.com/docker/docker)这门技术的必经之路之一。尤其是当[Docker](http://tonybai.com/tag/docker)被所在组织接受，更多人、项目和产品开始接触和使用Docker时，存储和分发自制的Docker image便成了刚需。Docker Registry一如既往的继承了“Docker坑多”的特点，为此这里将自己搭建”各类”Registry过程中执行的步骤、遇到的问题记录下来，为己备忘，为他参考。

Docker在2015年推出了[distribution](https://github.com/docker/distribution)项目，即Docker Registry 2。相比于[old registry](https://github.com/docker/docker-registry)，Registry 2使用[Go](http://tonybai.com/tag/golang)实现，在安全性、性能方面均有大幅改进。Registry设计了全新的Rest API，并且在image存储格式等方面不再兼容于old Registry。去年8月份，docker官方hub使用Registriy 2.1替代了原先的old Registry。如果你要与Registry2交互，你的Docker版本至少要是Docker 1.6。

Docker的开发者也一直在致力于改善Registry安装和使用的体验，通过提供[官方Registry Image](https://hub.docker.com/_/registry/)以及[Docker Compose工具](https://github.com/docker/compose)等来简化Registry的配置。不过在本文中，我们只是利用Docker以及Registry的官方Image来部署Registry，这样更便于全面了解Registry的部署配置细节。

Registry2在镜像存储方面不仅支持本地盘，还支持诸多主流第三方存储方案。通过分布式存储系统你还可以实现一个分布式Docker Registry服务。这里仅以本地盘以及single node registry2为例。

### 一、环境

这里还是复用以往文章中的Docker环境：

```
Docker Registry Server: 10.10.105.71 Ubuntu 14.04 3.16.0-57-generic；docker 1.9.1
其他两个工作Server：
10.10.105.72 Ubuntu 14.04 3.19.0-25-generic; docker 1.9.1
10.10.126.101 Ubuntu 12.04 3.16.7-013607-generic; docker 1.9.1
```


本次Registry使用当前最新stable版本:Registry 2.3.0。由于镜像采用本地磁盘存储，root分区较小，需要映射使用其他volume。

### 二、初次搭建

本以为Docker Registry的搭建是何其简单的，甚至简单到通过一行命令就可以完成的。比如我们在Registry Server上执行：

```
在~/dockerregistry下，执行：
$sudo docker run -d -p 5000:5000 -v `pwd`/data:/var/lib/registry --restart=always --name registry registry:2
Unable to find image 'registry:2' locally
2: Pulling from library/registry
f32095d4ba8a: Pull complete
9b607719a62a: Pull complete
973de4038269: Pull complete
2867140211c1: Pull complete
8da16446f5ca: Pull complete
fd8c38b8b68d: Pull complete
136640b01f02: Pull complete
e039ba1c0008: Pull complete
c457c689c328: Pull complete
Digest: sha256:339d702cf9a4b0aa665269cc36255ee7ce424412d56bee9ad8a247afe8c49ef1
Status: Downloaded newer image for registry:2
e9088ef901cb00546c59f89defa4625230f4b36b0a44b3713f38ab3d2a5a2b44
$ docker images
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
registry 2 c457c689c328 9 days ago 165.7 MB
$ docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
e9088ef901cb registry:2 "/bin/registry /etc/d" About a minute ago Up About a minute 0.0.0.0:5000->5000/tcp registry
```


Registry container已经跑起来了，其启动日志可以通过：docker logs registry查看。

我们在71本地给busybox:latest打一个tag，并尝试将新tag下的image push到Registry中去：

```
$ docker tag busybox:latest 10.10.105.71:5000/tonybai/busybox:latest
$ docker images
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
registry 2 c457c689c328 9 days ago 165.7 MB
busybox latest 65e4158d9625 9 days ago 1.114 MB
10.10.105.71:5000/tonybai/busybox latest 65e4158d9625 9 days ago 1.114 MB
... ...
```


push到Registry中：

```
$ docker push 10.10.105.71:5000/tonybai/busybox
The push refers to a repository [10.10.105.71:5000/tonybai/busybox] (len: 1)
unable to ping registry endpoint https://10.10.105.71:5000/v0/
v2 ping attempt failed with error: Get https://10.10.105.71:5000/v2/: Tunnel or SSL Forbidden
v1 ping attempt failed with error: Get https://10.10.105.71:5000/v1/_ping: Tunnel or SSL Forbidden
```


出错了！简单分析了一下，可能是71上docker daemon配置中加了http代理的缘故，导致无法ping通registry endpoint。于是在/etc/default/docker中注释掉export http_proxy=”xxx”的设置，并重启docker daemon。

再次尝试push：

```
$ docker push 10.10.105.71:5000/tonybai/busybox
The push refers to a repository [10.10.105.71:5000/tonybai/busybox] (len: 1)
unable to ping registry endpoint https://10.10.105.71:5000/v0/
v2 ping attempt failed with error: Get https://10.10.105.71:5000/v2/: tls: oversized record received with length 20527
v1 ping attempt failed with error: Get https://10.10.105.71:5000/v1/_ping: tls: oversized record received with length 20527
```


虽然还是失败，但错误信息已有所不同了。这次看来连接是可以建立的，但client端通过https访问server端，似乎想tls通信，但这一过程并未完成。

在其他机器上尝试push image到registry也遇到了同样的错误输出，如下：

```
10.10.105.72:
$ docker push 10.10.105.71:5000/tonybai/ubuntu
The push refers to a repository [10.10.105.71:5000/tonybai/ubuntu] (len: 1)
unable to ping registry endpoint https://10.10.105.71:5000/v0/
v2 ping attempt failed with error: Get https://10.10.105.71:5000/v2/: tls: oversized record received with length 20527
v1 ping attempt failed with error: Get https://10.10.105.71:5000/v1/_ping: tls: oversized record received with length 20527
```


从错误信息来看，client与Registry交互，默认将采用https访问，但我们在install Registry时并未配置指定任何tls相关的key和crt文件，https访问定然失败。要想弄清这个问题，只能查看[Registry Manual](https://github.com/docker/distribution/blob/master/docs/deploying.md)。

### 三、Insecure Registry

Registry的文档还是相对详尽的。在文档中，我们找到了[Insecure Registry](https://github.com/docker/distribution/blob/master/docs/insecure.md)，即接收plain http访问的Registry的配置和使用方法，虽然这不是官方推荐的。

实际上对于我们内部网络而言，Insecure Registry基本能满足需求，部署过程也避免了secure registry的那些繁琐步骤，比如制作和部署证书等。

为了搭建一个Insecure Registry，我们需要先清理一下上面已经启动的Registry容器。

```
$ docker stop registry
registry
$ docker rm registry
registry
```


修改Registry server上的Docker daemon的配置，为DOCKER_OPTS增加–insecure-registry：

```
DOCKER_OPTS="--insecure-registry 10.10.105.71:5000 ....
```


重启Docker Daemon，启动Registry容器：

```
$ sudo service docker restart
docker stop/waiting
docker start/running, process 6712
$ sudo docker run -d -p 5000:5000 -v `pwd`/data:/var/lib/registry --restart=always --name registry registry:2
5966e92fce9c34705050e19368d19574e021a272ede1575385ef35ecf5cea019
```


尝试再次Push image:

```
$ docker push 10.10.105.71:5000/tonybai/busybox
The push refers to a repository [10.10.105.71:5000/tonybai/busybox] (len: 1)
65e4158d9625: Pushed
5506dda26018: Pushed
latest: digest: sha256:800f2d4558acd67f52262fbe170c9fc2e67efaa6f230a74b41b555e6fcca2892 size: 2739
```


这回push ok！

我们将本地的tag做untag处理，再从Registry pull相关image：

```
$ docker images
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
registry 2 c457c689c328 9 days ago 165.7 MB
10.10.105.71:5000/tonybai/busybox latest 65e4158d9625 9 days ago 1.114 MB
busybox latest 65e4158d9625 9 days ago 1.114 MB
ubuntu 14.04 6cc0fc2a5ee3 5 weeks ago 187.9 MB
$ docker rmi 10.10.105.71:5000/tonybai/busybox
Untagged: 10.10.105.71:5000/tonybai/busybox:latest
$ docker images
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
registry 2 c457c689c328 9 days ago 165.7 MB
busybox latest 65e4158d9625 9 days ago 1.114 MB
ubuntu 14.04 6cc0fc2a5ee3 5 weeks ago 187.9 MB
$ docker pull 10.10.105.71:5000/tonybai/busybox
Using default tag: latest
latest: Pulling from tonybai/busybox
Digest: sha256:800f2d4558acd67f52262fbe170c9fc2e67efaa6f230a74b41b555e6fcca2892
Status: Downloaded newer image for 10.10.105.71:5000/tonybai/busybox:latest
$ docker images
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
registry 2 c457c689c328 9 days ago 165.7 MB
10.10.105.71:5000/tonybai/busybox latest 65e4158d9625 9 days ago 1.114 MB
busybox latest 65e4158d9625 9 days ago 1.114 MB
ubuntu 14.04 6cc0fc2a5ee3 5 weeks ago 187.9 MB
```


可以看到：Pull过程也很顺利。

在Private Registry2中查看或检索Repository或images，[将不能用docker search](https://github.com/docker/distribution/blob/master/ROADMAP.md#indexing-search-and-discovery)：

```
$ docker search 10.10.105.71:5000/tonybai/busybox/
Error response from daemon: Unexpected status code 404
```


但通过v2版本的API，我们可以实现相同目的：

```
$curl http://10.10.105.71:5000/v2/_catalog
{"repositories":["tonybai/busybox"]}
$ curl http://10.10.105.71:5000/v2/tonybai/busybox/tags/list
{"name":"tonybai/busybox","tags":["latest"]}
```


在其他主机上，我们尝试pull busybox：

```
10.10.105.72:
$docker pull 10.10.105.71:5000/tonybai/busybox
Using default tag: latest
Error response from daemon: unable to ping registry endpoint https://10.10.105.71:5000/v0/
v2 ping attempt failed with error: Get https://10.10.105.71:5000/v2/: tls: oversized record received with length 20527
v1 ping attempt failed with error: Get https://10.10.105.71:5000/v1/_ping: tls: oversized record received with length 20527
```


我们发现依旧不能pull和push！在Registry手册中讲到，如果采用insecure registry的模式，那么所有与Registry交互的主机上的Docker Daemon都要配置：–insecure-registry选项。

我们按照上面的配置方法，修改105.72上的/etc/default/docker，重启Docker daemon，再执行pull/push就会得到正确的结果：

```
$ sudo vi /etc/default/docker
$ sudo service docker restart
docker stop/waiting
docker start/running, process 10614
$ docker pull 10.10.105.71:5000/tonybai/busybox
Using default tag: latest
latest: Pulling from tonybai/busybox
5506dda26018: Pull complete
65e4158d9625: Pull complete
Digest: sha256:800f2d4558acd67f52262fbe170c9fc2e67efaa6f230a74b41b555e6fcca2892
Status: Downloaded newer image for 10.10.105.71:5000/tonybai/busybox:latest
$ docker images
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
ubuntu 14.04 36248ae4a9ac 8 days ago 187.9 MB
10.10.105.71:5000/tonybai/ubuntu 14.04 36248ae4a9ac 8 days ago 187.9 MB
10.10.105.71:5000/tonybai/busybox latest 65e4158d9625 9 days ago 1.114 MB
$ docker push 10.10.105.71:5000/tonybai/ubuntu
The push refers to a repository [10.10.105.71:5000/tonybai/ubuntu] (len: 1)
36248ae4a9ac: Pushed
8ea5373bf5a6: Pushed
2e0188208e83: Pushed
e3c70beaa378: Pushed
14.04: digest: sha256:72e56686cb9fb38438f0fd68fecf02ef592ce2ef7069bbf97802d959d568c5cc size: 6781
```


### 四、Secure Registry

Docker官方是推荐你采用Secure Registry的工作模式的，即transport采用tls。这样我们就需要为Registry配置tls所需的key和crt文件了。

我们首先清理一下环境，将上面的Insecure Registry停掉并rm掉；将各台主机上Docker Daemon的DOCKER_OPTS配置中的–insecure-registry去掉，并重启Docker Daemon。

如果你拥有一个域名，域名下主机提供Registry服务，并且你拥有某知名CA签署的证书文件，那么你可以建立起一个Secure Registry。不过我这里没有现成的证书，只能使用自签署的证书。严格来讲，使用自签署的证书在Docker官方眼中依旧属于Insecure，不过这里只是借助自签署的证书来说明一下Secure Registry的部署步骤罢了。

#### 1、制作自签署证书

如果你有知名CA签署的证书，那么这步可直接忽略。

```
$ openssl req -newkey rsa:2048 -nodes -sha256 -keyout certs/domain.key -x509 -days 365 -out certs/domain.crt
Generating a 2048 bit RSA private key
..............+++
............................................+++
writing new private key to 'certs/domain.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:Liaoning
Locality Name (eg, city) []:shenyang
Organization Name (eg, company) [Internet Widgits Pty Ltd]:foo
Organizational Unit Name (eg, section) []:bar
Common Name (e.g. server FQDN or YOUR name) []:mydockerhub.com
Email Address []:bigwhite.cn@gmail.com
```


#### 2、启动Secure Registry

启动带证书的Registry：

```
$ docker run -d -p 5000:5000 --restart=always --name registry \
-v `pwd`/data:/var/lib/registry \
-v `pwd`/certs:/certs \
-e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
-e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
registry:2
35e8ce77dd455f2bd50854e4581cd52be8a137f4aaea717239b6d676c5ea5777
```


由于证书的CN是mydockerhub.com，我们需要修改一下/etc/hosts文件:

```
10.10.105.71 mydockerhub.com
```


重新为busybox制作一个tag:

```
$docker tag busybox:latest mydockerhub.com:5000/tonybai/busybox:latest
```


Push到Registry:

```
$ docker push mydockerhub.com:5000/tonybai/busybox
The push refers to a repository [mydockerhub.com:5000/tonybai/busybox] (len: 1)
unable to ping registry endpoint https://mydockerhub.com:5000/v0/
v2 ping attempt failed with error: Get https://mydockerhub.com:5000/v2/: x509: certificate signed by unknown authority
v1 ping attempt failed with error: Get https://mydockerhub.com:5000/v1/_ping: x509: certificate signed by unknown authority
```


push失败了！从错误日志来看，docker client认为server传输过来的证书的签署方是一个unknown authority（未知的CA），因此验证失败。我们需要让docker client安装我们的CA证书：

```
$ sudo mkdir -p /etc/docker/certs.d/mydockerhub.com:5000
$ sudo cp certs/domain.crt /etc/docker/certs.d/mydockerhub.com:5000/ca.crt
$ sudo service docker restart //安装证书后，重启Docker Daemon
```


再执行Push，我们看到了成功的输出日志。由于data目录下之前已经被push了tonybai/busybox repository，因此提示“已存在”：

```
$docker push mydockerhub.com:5000/tonybai/busybox
The push refers to a repository [mydockerhub.com:5000/tonybai/busybox] (len: 1)
65e4158d9625: Image already exists
5506dda26018: Image already exists
latest: digest: sha256:800f2d4558acd67f52262fbe170c9fc2e67efaa6f230a74b41b555e6fcca2892 size: 2739
```


#### 3、外部访问Registry

我们换其他机器试试访问这个secure registry。根据之前的要求，我们照猫画虎的修改一下hosts文件，安装ca.cert，去除–insecure-registry选项，并重启Docker daemon。之后尝试从registry pull image：

```
$ docker pull mydockerhub.com:5000/tonybai/busybox
Using default tag: latest
latest: Pulling from tonybai/busybox
Digest: sha256:800f2d4558acd67f52262fbe170c9fc2e67efaa6f230a74b41b555e6fcca2892
Status: Downloaded newer image for mydockerhub.com:5000/tonybai/busybox:latest
$ docker images
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
10.10.105.71:5000/tonybai/ubuntu 14.04 36248ae4a9ac 9 days ago 187.9 MB
ubuntu 14.04 36248ae4a9ac 9 days ago 187.9 MB
10.10.105.71:5000/tonybai/busybox latest 65e4158d9625 9 days ago 1.114 MB
mydockerhub.com:5000/tonybai/busybox latest 65e4158d9625 9 days ago 1.114 MB
```


这样来看，如果使用自签署的证书，那么所有要与Registry交互的Docker主机都需要安装mydockerhub.com的ca.crt(domain.crt)。但如果你使用知名CA，这一步也就可以忽略。

### 五、Registry的鉴权管理

Registry提供了一种基础的鉴权方式。我们通过下面步骤即可为Registry加上基础鉴权：

在Register server上，为Registry增加foo用户，密码foo123：（之前需要停掉已有的Registry，并删除之）

```
//生成鉴权密码文件
$ mkdir auth
$ docker run --entrypoint htpasswd registry:2 -Bbn foo foo123 > auth/htpasswd
$ ls auth
htpasswd
//启动带鉴权功能的Registry：
$ docker run -d -p 5000:5000 --restart=always --name registry \
-v `pwd`/auth:/auth \
-e "REGISTRY_AUTH=htpasswd" \
-e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
-e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
-v `pwd`/data:/var/lib/registry \
-v `pwd`/certs:/certs \
-e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
-e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
registry:2
199ad0b3591fb9613b21b1c96f017267f3c39661a7025d30df636c6805e7ab50
```


在105.72上，我们尝试push image到Registry：

```
$ docker push mydockerhub.com:5000/tonybai/busybox
The push refers to a repository [mydockerhub.com:5000/tonybai/busybox] (len: 1)
65e4158d9625: Image push failed
Head https://mydockerhub.com:5000/v2/tonybai/busybox/blobs/sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4: no basic auth credentials
```


错误信息提示：鉴权失败。

在72上执行docker login:

```
$docker login mydockerhub.com:5000
Username: foo
Password:
Email: bigwhite.cn@gmail.com
WARNING: login credentials saved in /home/baiming/.docker/config.json
Login Succeeded
```


login成功后，再行Push：

```
$ docker push mydockerhub.com:5000/tonybai/busybox
The push refers to a repository [mydockerhub.com:5000/tonybai/busybox] (len: 1)
65e4158d9625: Image already exists
5506dda26018: Image already exists
latest: digest: sha256:800f2d4558acd67f52262fbe170c9fc2e67efaa6f230a74b41b555e6fcca2892 size: 2739
```


Push ok！

### 六、Registry中images的管理

前面提到过，通过V2版Rest API可以查询Repository和images：

```
$ curl --cacert domain.crt --basic --user foo:foo123 https://mydockerhub.com:5000/v2/_catalog
{"repositories":["tonybai/busybox","tonybai/ubuntu"]}
```


但如果要删除Registry中的Repository或某个tag的Image，目前v2还不支持，原因见[Registry的roadmap中的说明](https://github.com/docker/distribution/blob/master/ROADMAP.md#deletes)。

不过如果你的Registry的存储引擎使用的是本地盘，倒是有一些第三方脚本可供使用，比如：[delete-docker-registry-image](https://github.com/burnettk/delete-docker-registry-image)。

### 七、小结

Registry2发布不到1年，目前还有许多问题待解决，就比如delete image的问题，相信在2.4以及后续版本这些问题会被逐个解决掉或能找到一个相对理想的方案。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

好文，帮了我太多了，老实说registry官方镜像手册真太水了啊

写的太好了

感谢分享，自定义证书坑太多了，还是买一个靠谱。

写得很详细，感谢分享

我制作好证书之后价格证书分发给客户端，然后在客户端，但是为什么客户端依旧提示

“Error response from daemon: Get https://sixie.local:5000/v2/: x509: certificate signed by unknown authority”

你有遇到这种情况吗？

多半是证书生成过程中出现了问题。文章中使用了自签署CA的方式发布的服务端公钥证书，即server端的key就是CA私钥，server端的公钥证书同时也是CA公钥证书。如果不明白原理，可以看看我的这篇文章：https://tonybai.com/2015/04/30/go-and-https