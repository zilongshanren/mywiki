---
title: 官宣：慕课网课程“Kubernetes实战：高可用集群搭建、配置、运维与应用”上线了
url: https://tonybai.com/2018/10/17/imooc-course-kubernetes-practice-go-online/
published: '2018-10-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 官宣：慕课网课程“Kubernetes实战：高可用集群搭建、配置、运维与应用”上线了

距离我的第一门网课[《Kubernetes基础：开启云原生之门》](https://www.imooc.com/learn/978)上线已经过去5个多月了，我的实战课[《Kubernetes实战：高可用集群搭建、配置、运维与应用》](https://coding.imooc.com/class/chapter/284.html)终于在9月27日正式上线了。

![img{512x368}](../../assets/9567b5343cdf5896.png)


### 一. 课程介绍

![img{512x368}](../../assets/fd85e599f9257d51.png)


![img{512x368}](../../assets/aeb42d4596e43a26.png)


[《Kubernetes实战：高可用集群搭建、配置、运维与应用》](https://coding.imooc.com/class/chapter/284.html)的课程内容与最初课程设计时规划的内容大纲没有太多出入，基本就是根据我最初的想法拟定的内容，**这也基本是我这两年学习k8s、积累的k8s实践的路线**。整个课程基于kubernetes 1.10.2版本([docker](https://tonybai.com/tag/docker) 17.03.2ce)。课程内容大致分为七个部分（与课程主页的课程目录结构稍有差异，但课程内容是一致的）：

第一章 搭建你的第一个[Kubernetes集群](https://tonybai.com/tag/kubernetes)

本章介绍了一个使用[kubeadm](https://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)引导的Kubernetes集群的搭建和基本配置方法。

- 1-1: 导学
- 1-2: 安装准备
- 1-3: 初始化集群master节点
- 1-4: 向集群加入worker节点
- 1-5:
[安装dashboard和heapster](https://tonybai.com/2017/09/26/some-notes-about-deploying-kubernetes-dashboard-1-7-0/) - 1-6: 验证集群安装结果

第二章 [Kubernetes集群探索](https://tonybai.com/2017/01/24/explore-kubernetes-cluster-installed-by-kubeadm/)

本章对kubeadm初始化集群的原理进行了讲解，并对已经建立的k8s集群中的各个组件进行详细介绍，包括功用、原理和配置等

- 2-1: kubeadm init流程揭秘
- 2-2: kubeadm join流程揭秘
- 2-3: kubernetes核心组件详解
- 2-4:
[kubectl](https://tonybai.com/2018/06/14/the-authentication-and-authorization-of-kubectl-when-accessing-k8s-cluster/)详解

第三章 Kubernetes网络、安全与存储

本章讲解k8s集群的三个难点：网络、安全与存储的概念和运行原理。

3-1：kubernetes[集群网络](https://tonybai.com/2017/01/17/understanding-flannel-network-for-kubernetes/)

- 3-1-1: kubernetes集群的“三个网络”
- 3-1-2: kubernetes网络的设计要求
- 3-1-3: kubernetes网络实现
- 3-1-4: pod网络实现原理
- 3-1-5: pod网络方案对比
- 3-1-6: service网络实现原理

3-2: [kubernetes集群安全](https://tonybai.com/2018/06/14/the-authentication-and-authorization-of-kubectl-when-accessing-k8s-cluster/)

- 3-2-1: kube-apiserver安全模型
- 3-2-2: 传输安全
- 3-2-3:
[身份验证](https://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/) - 3-2-4: 授权
- 3-2-5: 准入控制

3-3 kubernets集群存储

- 3-3-1: Volume
- 3-3-2:
[PV和PVC](https://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/) - 3-3-3: StorageClass和动态PV供给
- 3-3-4: Kubernetes存储模型

第四章 [高可用Kubernetes集群](https://tonybai.com/2017/05/15/setup-a-ha-kubernetes-cluster-based-on-kubeadm-part1/)搭建方案

本章介绍了什么是高可用k8s集群，并给出了一个可行的高可用Kubernetes集群的搭建方案。

- 4-1: 什么是高可用Kubernetes集群
- 4-2: 高可用Kubernetes集群方案

第五章 Kubernetes集群常见运维操作

本章讲解了Kubernetes集群的基本运维操作，包括node管理、service、pod管理、日志查看等。并讲解了面对k8s集群问题时如何做troubleshooting。

- 5-1: 管理Node与Label
- 5-2: 管理Namespace、Service和Pod
- 5-3:
[计算资源管理](https://tonybai.com/2017/10/16/out-of-node-resource-handling-in-kubernetes-cluster/) - 5-4: 查看事件和容器日志
- 5-5: 常用TroubleShooting方法

第六章 Kubernetes支撑[云原生应用](https://www.cncf.io/)开发案例

本章讲解了Kubernetes集群的应用：支撑云原生应用开发。并通过实际操作讲解了镜像仓库、集中日志以及云应用治理框架的搭建和使用。

- 6-1: Kubernetes与云原生应用
- 6-2:
[高可用私有镜像仓库搭建](https://tonybai.com/2017/12/08/deploy-high-availability-harbor-on-kubernetes-cluster/) - 6-3:
[基于ElasticSearch Stack搭建集群Logging设施](https://tonybai.com/2018/06/13/setup-efk-on-kubernetes-1-10-3-in-the-hard-way/) - 6-4:
[基于istio service mesh实现服务治理](https://tonybai.com/2018/01/03/an-intro-of-microservices-governance-by-istio/)

第七章 课程回顾与总结

### 二. 做网课目的与课程思路

当初接下慕课商务的这门课主要是出于两个目的：

- 通过这门课程对自己的k8s学习和实践做一个阶段性的系统总结
- 尝试一下网课这个“新鲜”事物

现在看来，当初这两个“目的”都实现了。但是录制网课的确是件很“辛苦”的事情，不知道多少的夜晚和周末都留给了“网课资料编写和录制”。尤其是Kubernetes这个主题，讲起来“顾虑”很多：

-
和编程语言课不同，Kubernetes平台是个复杂的平台，外延生态很庞大。k8s概念多，如果不把概念和原理交待清楚、讲透彻，直接就上手操作，那样学习后，对k8s的理解仍然不会很深刻，很多问题仍然无法自己去解决，尤其是中高级阶段。 这就导致很多小伙伴认为课程概念讲解“有些多”；

-
生产环境中k8s集群有大有小，使用目的也是大不相同，安装方式也是有很多种(官方就列了10多种)，所在的网络环境以及使用的pod网络插件也是区别很大，遇到的问题更是千差万别，这里在准备 课程时也是思来想去，无法覆盖所有生产环境的所有情况。最后决定使用kubeadm搭建一个4节点的集群(使用weave network plugin)，可能能更好的满足初学者的需求，学员们更容易获取搭建这样一个 k8s环境所需的资源。而关于课程中实际操作部分重点集中在前面的k8s搭建、集群探索以及后面的k8s对云应用支撑的环节。所以如果小伙伴们的环境与课程不同，可以在课程后提问，我会尽量第一时间、细致的回答各位的问题。

-
关于时长，我在课程里尽量做到没有”废话“。现在的网课多根据“时长”定价（虽然不赞同，但是目前也没有一个更好的量化课程质量的方法）：比如10个小时以上可能就会定到399元，但是不足10小时，可能就在199元这个价位。

**于是我努力地将课程做到了“199”这个价位上了**。对于真正想学习k8s的小伙伴们，这也许是一个“好消息”:)。

### 三. 课程小结

Kubernetes还在快速不断地演进！我个人觉得学完本门课程也仅仅是“Kubernetes实践之路”的一个开始而已！应用上云的趋势已经不可逆转，对于云应用开发人员来说，**了解和学习Kubernetes就像当年单机时代开发人员要去了解PC操作系统一样重要**！希望本门课程能给更多的开发者带去帮助！

下面是课程的自制海报，欢迎转发:)

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018 – 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

因为学过 Kubernetes：开启云原生之门 ，觉得讲的很不错，这次的实战已经付费开始学习了。请问今后还有更实践性的教学计划吗？比如，跨云、chart 部署等实操部分的讲解

感谢支持！有问题及时交流。后续可能以“微实战课”的形式 讲解一些实践性很强的专题。

一直看tony老师的博客，收益良多，《Kubernetes：开启云原生之门》就讲的不错，这次果断把《Kubernetes实战：高可用集群搭建、配置、运维与应用》给下了！话说tony老师好久没更新博文了啊~：）

这两个月录制视频占用了很多业余时间，加之最近工作真的比较忙，于是blog更新不那么频繁了:(。这种情况我也希望不要持续太久:) 感谢关注我的网课！有问题及时交流。

已购买,支持一下。

谢谢支持！