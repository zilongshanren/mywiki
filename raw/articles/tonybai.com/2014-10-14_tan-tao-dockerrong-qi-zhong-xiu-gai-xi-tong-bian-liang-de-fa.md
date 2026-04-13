---
title: 探讨Docker容器中修改系统变量的方法
url: https://tonybai.com/2014/10/14/discussion-on-the-approach-to-modify-system-variables-in-docker/
published: '2014-10-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 探讨Docker容器中修改系统变量的方法

探讨完[Docker对共享内存状态持久化的支持状况](http://tonybai.com/2014/10/12/discussion-on-shared-mem-support-in-docker/)后，我将遗留产品build到一个pre-production image中，测试启动是否OK。很显然，我过于乐观了，[Docker](http://www.docker.com)之路并不平坦。我收到了shmget报出的EINVAL错误码，提示参数非法。 shmget的manual对EINVAL错误码的说明如下：

EINVAL：

A new segment was to be created and size < SHMMIN or size > SHMMAX, or no new segment was to be created, a segment with given key existed, but size is greater than the size of that segment.

显然我们要创建的shared memory的size很可能大于SHMMAX这个系统变量了。那么一个从base image创建出的容器中的系统变量到底是什么值呢？我们来查看一下，我们基于"centos:centos6"启动一个Docker容器，并检查其中的 系统变量值设置：

$ sudo docker run -it "centos:centos6" /bin/bash

bash-4.1# cat /proc/sys/kernel/shmmax

33554432

bash-4.1# sysctl -a|grep shmmax

kernel.shmmax = 33554432

可以看出默认情况下，当前容器中root账号看到的shmmax值我33554432， 我的程序要创建的shm size的确要大于这个值，报出EINVAL错误也就无可厚非了。我尝试按照物理机上的方法临时修改一下该值：

bash-4.1# echo 68719476736 > /proc/sys/kernel/shmmax

bash: /proc/sys/kernel/shmmax: Read-only file system

/proc/sys/kernel/shmmax居然是只读的，无法修改。

我又尝试修改/etc/sysctl.conf这个持久化系统变量的地方，但打开/etc/sysctl.conf文件，我发现我又错了，这 个文件中shmmax的值如下：

# Controls the maximum shared segment size, in bytes

kernel.shmmax = 68719476736

/etc/sysctl.conf文件 中的系统变量shmmax的值是68719476736，而系统当前的实际值则是33554432，难道是/etc /sysctl.conf中的值没有生效，于是我手工重新加载一次该文件：

-bash-4.1# sysctl -p

error: "Read-only file system" setting key "net.ipv4.ip_forward"

error: "Read-only file system" setting key "net.ipv4.conf.default.rp_filter"

error: "Read-only file system" setting key "net.ipv4.conf.default.accept_source_route"

error: "Read-only file system" setting key "kernel.sysrq"

error: "Read-only file system" setting key "kernel.core_uses_pid"

error: "net.ipv4.tcp_syncookies" is an unknown key

error: "net.bridge.bridge-nf-call-ip6tables" is an unknown key

error: "net.bridge.bridge-nf-call-iptables" is an unknown key

error: "net.bridge.bridge-nf-call-arptables" is an unknown key

error: "Read-only file system" setting key "kernel.msgmnb"

error: "Read-only file system" setting key "kernel.msgmax"

error: "Read-only file system" setting key "kernel.shmmax"

error: "Read-only file system" setting key "kernel.shmall"

我得到了和之前类似的错误结果：只读文件系统，无法修改。于是乎两个问题萦绕在我的面前：

1、为什么容器内当前系统变量值与sysctl.conf中的不一致？

2、为什么无法修改当前系统变量值?

在翻阅了Stackoverflow, github docker issues后，我得到了的答案如下：

1、Docker的base image做的很精简，甚至都没有init进程，原本在OS启动时执行生效系统变量的过程(sysctl -p)也给省略了，导致这些系统变量依旧保留着kernel默认值。以CentOs为例，在linux kernel boot后，init都会执行/etc/rc.d/rc.sysinit，后者会加载/etc/sysctl.conf中的系统变量值。下面是 CentOs5.6中的rc.sysinit代码摘录：

… …

# Configure kernel parameters

update_boot_stage RCkernelparam

sysctl -e -p /etc/sysctl.conf >/dev/null 2>&1

… …

2、Docker容器中的系统变量在non-priviledged模式下目前(我使用的时docker 1.2.0版本)就无法修改，这 和resolv.conf、hosts等文件映射到宿主机对应的文件有不同。

$ mount -l

…. ….

/dev/mapper/ubuntu–Server–14–vg-root on /etc/resolv.conf type ext4 (rw,relatime,errors=remount-ro,data=ordered)

/dev/mapper/ubuntu–Server–14–vg-root on /etc/hostname type ext4 (rw,relatime,errors=remount-ro,data=ordered)

/dev/mapper/ubuntu–Server–14–vg-root on /etc/hosts type ext4 (rw,relatime,errors=remount-ro,data=ordered)

… …

那么我们该如何修改系统变量值来满足遗留产品的需求呢？

**一、使用–privileged选项**

我们使用–privileged这个特权选项来启动一个基于centos:centos6的新容器，看看是否能对shmmax这样的系统变量值 进行修改：

$ sudo docker run -it –privileged "centos:centos6" /bin/bash

bash-4.1# cat /proc/sys/kernel/shmmax

33554432

bash-4.1# echo 68719476736 > /proc/sys/kernel/shmmax

bash-4.1# cat /proc/sys/kernel/shmmax

68719476736

bash-4.1# sysctl -p

net.ipv4.ip_forward = 0

net.ipv4.conf.default.rp_filter = 1

net.ipv4.conf.default.accept_source_route = 0

kernel.sysrq = 0

kernel.core_uses_pid = 1

… …

kernel.msgmnb = 65536

kernel.msgmax = 65536

kernel.shmmax = 68719476736

kernel.shmall = 4294967296

可以看出，通过–privileged选项，容器获得了额外的特权，并且可以对系统变量的值进行修改了。不过这样的修改是不能保存在容器里的， 我们stop 容器，再重启该容器就能看出来：

$ sudo docker start 3e22d65a7845

$ sudo docker attach 3e22d65a7845

bash-4.1# cat /proc/sys/kernel/shmmax

33554432

shmmax的值在容器重启后又变回了原先的那个默认值。不过重启后的容器依旧具有privileged的特权，我们还可以重新手工执行命令对系 统变量进行修改：

bash-4.1# echo 68719476736 > /proc/sys/kernel/shmmax

bash-4.1# cat /proc/sys/kernel/shmmax

68719476736

但即便这样，也无法满足我们的需求，我们总不能每次都在容器中手工执行系统变量值修改的操作吧。privileged选项的能力能否带到 image中呢？答案是目前还不能，我们无法在build image时通过privileged选项修改系统变量值。

这样一来，我们能做的只有把产品启动与系统变量值修改放在一个脚本中了，并将该脚本作为docker 容器的cmd命令来执行，比如我们构建一个Dockerfile：

FROM centos:centos6

MAINTAINER Tony Bai [<bigwhite.cn@gmail.com>](mailto:bigwhite.cn@gmail.com)

RUN yum install python-setuptools -y

RUN easy_install supervisor

RUN mkdir -p /var/log/supervisor

COPY ./supervisord.conf /etc/supervisord.conf

COPY ./start.sh /bin/start.sh

RUN chmod +x /bin/start.sh

CMD ["/bin/start.sh]

//start.sh

sysctl -p

/usr/bin/supervisord

这样，start.sh在supervisord启动前将系统变量值重新加载，而supervisord后续启动的程序就可以看到这些新系统变量 的值了。不过别忘了利用这个image启动容器时要加上–priviledged选项，否则容器启动就会失败。

**二、使用phusion/baseimage**

前面说过/etc/sysctl.conf中的值没有生效是因为docker官方提供的centos:centos6把init进程的初始化过程给精 简掉了。[phusion/baseimage](https://registry.hub.docker.com/u/phusion/baseimage/)是目前docker registery上仅次于ubuntu和centos两个之后的base image，其提供了/sbin/my_init这个init进程，用于在container充当init进程的角色。那么my_init是否可以用于执行sysctl -p呢？我们试验一下：

我们先pull这个base image下来：sudo docker pull phusion/baseimage。pull成功后，我们先基于“phusion/baseimage”启动一个容器做一些explore工作：

$ sudo docker run -i -t "phusion/baseimage"

*** Running /etc/my_init.d/00_regen_ssh_host_keys.sh…

No SSH host key available. Generating one…

Creating SSH2 RSA key; this may take some time …

Creating SSH2 DSA key; this may take some time …

Creating SSH2 ECDSA key; this may take some time …

Creating SSH2 ED25519 key; this may take some time …

invoke-rc.d: policy-rc.d denied execution of restart.

*** Running /etc/rc.local…

*** Booting runit daemon…

*** Runit started as PID 100

通过nsenter进去，查看一下/sbin/my_init的源码，我们发现这是一个python脚本，不过从头到尾浏览一遍，没有发现sysctl加载/etc/sysctl.conf系统变量的操作。

不过，phusion文档中说my_init可以在初始化过程中执行/etc/my_init.d下的脚本。那是不是我们将一个执行sysctl -p的脚本放入/etc/my_init.d下就可以实现我们的目的了呢？试试。

我们编写一个脚本：load_sys_varibles.sh

#!/bin/sh

sysctl -p > init.txt

下面是制作image的Dockerfile:

FROM phusion/baseimage:latest

MAINTAINER Tony Bai <bigwhite.cn@gmail.com>

RUN echo "kernel.shmmax = 68719476736" >> /etc/sysctl.conf

RUN mkdir -p /etc/my_init.d

ADD load_sys_varibles.sh /etc/my_init.d/load_sys_varibles.sh

RUN chmod +x /etc/my_init.d/load_sys_varibles.sh

CMD ["/sbin/my_init"]

phusion/baseimage是基于ubuntu的OS，其sysctl.conf默认情况下没啥内容，所以我们在Dockerfile中向这个文件写入我们需要的系统变量值。构建image并启动容器：

$ sudo docker build -t "myphusion:v1" ./

Sending build context to Docker daemon 13.12 MB

Sending build context to Docker daemon

Step 0 : FROM phusion/baseimage:latest

—> cf39b476aeec

Step 1 : MAINTAINER Tony Bai <bigwhite.cn@gmail.com>

—> Using cache

—> d0e9b51a3e4f

Step 2 : RUN echo "kernel.shmmax = 68719476736" >> /etc/sysctl.conf

—> Using cache

—> 2c800687cc83

Step 3 : RUN mkdir -p /etc/my_init.d

—> Using cache

—> fe366eea5eb4

Step 4 : ADD load_sys_varibles.sh /etc/my_init.d/load_sys_varibles.sh

—> a641bb595fb9

Removing intermediate container c381b9f001c2

Step 5 : RUN chmod +x /etc/my_init.d/load_sys_varibles.sh

—> Running in 764866552f25

—> eae3d7f1eac5

Removing intermediate container 764866552f25

Step 6 : CMD ["/sbin/my_init"]

—> Running in 9ab8d0b717a7

—> 8be4e7b6b174

Removing intermediate container 9ab8d0b717a7

Successfully built 8be4e7b6b174

$ sudo docker run -it "myphusion:v1"

*** Running /etc/my_init.d/00_regen_ssh_host_keys.sh…

No SSH host key available. Generating one…

Creating SSH2 RSA key; this may take some time …

Creating SSH2 DSA key; this may take some time …

Creating SSH2 ECDSA key; this may take some time …

Creating SSH2 ED25519 key; this may take some time …

invoke-rc.d: policy-rc.d denied execution of restart.

*** Running /etc/my_init.d/load_sys_varibles.sh…

sysctl: setting key "kernel.shmmax": Read-only file system

*** /etc/my_init.d/load_sys_varibles.sh failed with status 255

*** Killing all processes…

唉，还是老问题！即便是在my_init中执行，依旧无法逾越Read-only file system，查看Phusion/baseimage的Dockerfile才知道，它也是From ubuntu:14.04的，根不变，上层再怎么折腾也没用。

换一种容器run方法吧，加上–privileged：

$ sudo docker run -it –privileged "myphusion:v1"

*** Running /etc/my_init.d/00_regen_ssh_host_keys.sh…

No SSH host key available. Generating one…

Creating SSH2 RSA key; this may take some time …

Creating SSH2 DSA key; this may take some time …

Creating SSH2 ECDSA key; this may take some time …

Creating SSH2 ED25519 key; this may take some time …

invoke-rc.d: policy-rc.d denied execution of restart.

*** Running /etc/my_init.d/load_sys_varibles.sh…

*** Running /etc/rc.local…

*** Booting runit daemon…

*** Runit started as PID 102

这回灵光了。enter到容器里看看设置的值是否生效了：

root@9e399f46372a:~#cat /proc/sys/kernel/shmmax

68719476736

结果如预期。这样来看phusion/baseimage算是为sysctl -p加载系统变量值提供了一个便利，但依旧无法脱离–privileged，且依旧无法在image中持久化这个设置。

在Docker github的issue中有人提出建议在Dockerfile中加入类似RUNP这样的带有特权的指令语法，但不知何时才能在Docker中加入这一功能。

总而言之，基于目前docker官网提供的base image，我们很难找到特别理想的修改系统变量值的方法，除非自己制作base image，这个还没尝试过，待后续继续研究。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

这里提到了container内hosts文件的修改，通常这个文件修改后重启container会被覆盖，除了在start.sh中每次设置，不知道还有什么好的办法。

你好，如果使用K8S调度容器时，–privileged怎么来实现呢？是要修改apiserver的KUBE_ALLOW_PRIV=”–allow-privileged=false”默认设定吗？除了这个还有其他方法吗？

kubelet有一个–allow-privileged选项. kubernetes 1.9以及之前版本都有。