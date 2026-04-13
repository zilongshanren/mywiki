---
title: 当Docker遇到systemd
url: https://tonybai.com/2016/12/27/when-docker-meets-systemd/
published: '2016-12-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 当Docker遇到systemd

近期在做[Kubernetes](http://kubernetes.io/)集群的升级的相关试验，即从原先的[K8s 1.3.7版本](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu)升级到最新的K8s 1.5.1版本。k8s自1.4版本开始引入[kubeadm](http://kubernetes.io/docs/admin/kubeadm/)，试图简化K8s的安装和使用门槛，提升开发者体验。但kubeadm仅支持16.04及以上的[Ubuntu](http://tonybai.com/tag/ubuntu)版本，于是我们在升级K8s集群前会遇到另外一个问题：Ubuntu 16.04已经由[Upstart](http://upstart.ubuntu.com/)初始化系统换成了[systemd](https://en.wikipedia.org/wiki/Systemd)初始化系统，Ubuntu 16.04上的[Docker](http://tonybai.com/tag/docker) engine的使用和配置方法与以前在Ubuntu 14.04上将有所不同。Docker是K8s支持的容器引擎之一，也是目前最主流的容器引擎，弄清楚Docker的配置和使用也是后续用好K8s的前提之一。于是这里打算记录一下Docker与Systemd是如何相生共存的^0^。

### 一、Ubuntu 16.04安装Docker

Aliyun目前上没有提供官方Ubuntu 16.04 ECS，最高仅支持到Ubuntu 14.04.4。因此在Aliyun ECS上用16.04需要手工upgrade到16.04（不过建议在upgrade前做个snapshot，一旦upgrade失败，好恢复）。升级后的Ubuntu环境信息如下：

```
Ubuntu 16.04.1 LTS (GNU/Linux 4.4.0-58-generic x86_64)
```


[kubeadm文档](http://kubernetes.io/docs/getting-started-guides/kubeadm/)中认为Docker 1.11.2版本与之更配哟，不过对于更新的版本似乎配合起来也没有什么大问题。我们这里安装目前可以找到的最新stable release: docker 1.12.5：

```
# docker version
Client:
Version: 1.12.5
API version: 1.24
Go version: go1.6.4
Git commit: 7392c3b
Built: Fri Dec 16 02:42:17 2016
OS/Arch: linux/amd64
Server:
Version: 1.12.5
API version: 1.24
Go version: go1.6.4
Git commit: 7392c3b
Built: Fri Dec 16 02:42:17 2016
OS/Arch: linux/amd64
```


上面是你安装docker成功后，才能输出的version信息哦^0^。

安装Docker的方法随着docker的快速演进也在变化中，随着Docker的成熟，其方法趋于稳定。官方提供的[在Ubuntu安装Docker的方法](https://docs.docker.com/engine/installation/linux/ubuntulinux/)成为主流，我们这里也不例外的参考这一方法。不过这一方法有一前提，那就是你最好配备的“加(fan)速(qiang)器(qi)”，否则好慢，甚至是不成功。

详细步骤如下：（熟悉之的观众可略过之^_^）

#### 1、从keyserver获取key

```
# apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
Executing: /tmp/tmp.OoFaQ0V0gx/gpg.1.sh --keyserver
hkp://p80.pool.sks-keyservers.net:80
--recv-keys
58118E89F3A912897C070ADBF76221572C52609D
gpg: requesting key 2C52609D from hkp server p80.pool.sks-keyservers.net
gpg: key 2C52609D: public key "Docker Release Tool (releasedocker) <docker@docker.com>" imported
gpg: Total number processed: 1
gpg: imported: 1 (RSA: 1)
```


#### 2、添加Docker源

创建/etc/apt/sources.list.d/docker.list文件，写入：

```
deb https://apt.dockerproject.org/repo ubuntu-xenial main
```


执行apt-get update更新包信息：

```
... ...
Get:11 https://apt.dockerproject.org/repo ubuntu-xenial InRelease [30.2 kB]
Fetched 30.2 kB in 2s (14.1 kB/s)
Reading package lists... Done
```


#### 3、安装Docker engine

执行安装命令，安装Docker engine：

```
# apt install docker-engine
... ...
Setting up docker-engine (1.12.5-0~ubuntu-xenial) ...
Setting up liberror-perl (0.17-1.2) ...
Setting up git-man (1:2.7.4-0ubuntu1) ...
Setting up git (1:2.7.4-0ubuntu1) ...
Processing triggers for libc-bin (2.23-0ubuntu5) ...
Processing triggers for systemd (229-4ubuntu13) ...
Processing triggers for ureadahead (0.100.0-19) ...
```


验证安装结果：

```
# which docker
/usr/bin/docker
# docker version
... ... //输出和上一节相同的结果
# ps -ef|grep docker
root 22132 1 0 11:18 ? 00:00:00 /usr/bin/dockerd -H fd://
root 22162 22132 0 11:18 ? 00:00:00 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --shim docker-containerd-shim --metrics-interval=0 --start-timeout 2m --state-dir /var/run/docker/libcontainerd/containerd --runtime docker-runc
```


安装后，Docker引擎自动启动了。

### 二、Docker服务的使能与启停

控制Docker服务开机自启以及启停操作的脚本已经由upstart初始化系统的/etc/init.d/docker变为了systemd初始化系统的/lib/systemd/system/docker.service。

在systemd下，docker service的脚本路径通过下面命令可以找到：

```
# systemctl show --property=FragmentPath docker
FragmentPath=/lib/systemd/system/docker.service
```


通过下面命令可以查看docker service的是否是开机自启：

```
# systemctl is-enabled docker
enabled
```


通过systemctl enable和disable命令可以使能开机自启或取消开机自启。

传统Ubuntu通过service docker start/stop/restart启动、停止或重启服务，换到systemd后，我们需要用systemctl start/stop/restart docker来启动、停止或重启服务。

### 三、Docker的EnvironmentFile

以前我们给Docker engine设置一个http_proxy、设置–insecure-registry或–registry-mirror、配置一个dns啥的，都可以通过/etc/default/docker中的DOCKER_OPTS以及相关export的环境变量实现。但在Ubuntu 16.04下这个配置文件变成了这样：

```
# Docker Upstart and SysVinit configuration file
#
# THIS FILE DOES NOT APPLY TO SYSTEMD
#
# Please see the documentation for "systemd drop-ins":
# https://docs.docker.com/engine/articles/systemd/
... ...
```


问题来了！我们怎么配置Docker engine呢？Docker官方推荐在如下路径下面创建配置文件（比如http-proxy.conf），以override默认的docker.service文件中的配置：

```
/etc/systemd/system/docker.service.d
```


不过经测试后（after systemctl daemon-reload; systemctl restart docker），发现并不生效。

我们来使用EnvironmentFile对Docker Engine进行配置。编辑/lib/systemd/system/docker.service文件，添加如下内容：

```
ExecStart=/usr/bin/dockerd -H fd:// $DOCKER_OPTS
EnvironmentFile=-/etc/default/docker
```


习惯了使用/etc/default/docker配置DOCKER_OPTS等配置，于是在EnvironmentFile中直接使用了该文件。

```
///etc/default/docker
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"
# If you need Docker to use an HTTP proxy, it can also be specified here.
#export http_proxy="http://127.0.0.1:3128/"
http_proxy="http://xxxxx"
https_proxy="xxxx"
no_proxy="127.0.0.1,localhost"
```


保存后，执行：

```
systemctl daemon-reload
systemctl restart docker
```


你会发现配置生效了。

经常接触/etc/default/docker的人会发现，上述文件中的http_proxy等变量前面的export关键字没有了。没错，在systemd环境下，不再需要export了，如果加上export，反倒会导致配置不生效。

### 四、Docker引擎的日志

最后，Docker引擎的日志哪里去了？以前不是在/var/log/upstart/下面么？Ubuntu 16.04中，这个目录下连docker字样的影儿都没看到。

在systemd下面，我们需要搬出[journalctl](https://www.freedesktop.org/software/systemd/man/journalctl.html)工具。想看docker service的实时日志，请执行：

```
# journalctl -u docker -f
```


看历史日志：

```
# journalctl --since "1 hour ago" -u docker
```


更多journalctl用法，可以参考其[man pages](https://www.freedesktop.org/software/systemd/man/journalctl.html)。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 仅有 1 条评论