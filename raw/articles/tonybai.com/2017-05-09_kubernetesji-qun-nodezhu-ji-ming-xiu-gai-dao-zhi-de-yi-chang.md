---
title: Kubernetes集群node主机名修改导致的异常
url: https://tonybai.com/2017/05/09/exception-caused-by-kubernetes-node-hostname-change/
published: '2017-05-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes集群node主机名修改导致的异常

除了在生产环境使用的[Kubernetes 1.3.7集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)之外，我这里还有[一套1.5.1的Kubernetes测试环境](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)，这个测试环境一来用于验证各种技术方案，二来也是为了跟踪Kubernetes的最新进展。本篇要记录的一个异常就是发生在该测试Kubernetes集群中的。

### 一、缘起

前两天我在Kubernetes测试环境搭建一套[Ceph](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)，为了便于ceph-deploy的安装，我通过hostnamectl命令将阿里云默认提供的复杂又冗长的主机名改为短小且更有意义的主机名：

```
iZ25beglnhtZ -> yypdmaster
iz2ze39jeyizepdxhwqci6z -> yypdnode
以yypdmaster为例，修改过程如下：
# hostnamectl --static set-hostname yypdmaster
# hostnamectl status
Static hostname: yypdmaster
Transient hostname: iZ25beglnhtZ
Icon name: computer-vm
Chassis: vm
Machine ID: 91aa4b8f2556de49e743dc2f53e8a5c4
Boot ID: 5d0e642ebafa460086388da4177e488e
Virtualization: kvm
Operating System: Ubuntu 16.04.1 LTS
Kernel: Linux 4.4.0-58-generic
Architecture: x86-64
# cat /etc/hostname
yypdmaster
hostnamectl并未修改/etc/hosts，我手动在/etc/hosts中将yypdmaster对应的ip配置上：
xx.xx.xx.xx yypdmaster
```


重新登录后，我们看到主机名状态：Transient hostname不见了，只剩下了静态主机名：

```
# hostnamectl status
Static hostname: yypdmaster
Icon name: computer-vm
Chassis: vm
Machine ID: 91aa4b8f2556de49e743dc2f53e8a5c4
Boot ID: 5d0e642ebafa460086388da4177e488e
Virtualization: kvm
Operating System: Ubuntu 16.04.1 LTS
Kernel: Linux 4.4.0-58-generic
Architecture: x86-64
```


另外一台主机也是如此修改。主机名修改后，整个k8s集群工作一切正常，因此我最初以为hostname的修改对k8s cluster的运行没有影响。

### 二、集群”Crash”

昨天在做[跨节点挂载Cephfs](http://tonybai.com/2017/05/08/mount-cephfs-acrossing-nodes-in-kubernetes-cluster/)测试时，发现在yypdmaster上kubectl exec另外一个node上的pod不好用，提示：连接10250端口超时！而且从错误日志来看，yypdmaster上的k8s组件居然通过yypdnode的外网ip去访问yypdnode上的10250端口，也就是yypdnode上kubelet监听的端口。由于aliyun的安全组规则限制，这个端口是不允许外网访问的，因此timeout错误是合理的。但为什么之前集群都是好好的？突然间出现这个问题呢？为什么不用内网的ip地址访问呢？

我尝试重启了yypdnode上的kubelet服务。不过似乎没什么效果！正当我疑惑时，我发现集群似乎”Crash”了，下面是当时查看集群的pod情况的输出：

```
# kubectl get pod --all-namespaces -o wide
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
default ceph-pod2 1/1 Unknown 0 26m 172.30.192.4 iz2ze39jeyizepdxhwqci6z
default ceph-pod2-with-secret 1/1 Unknown 0 38m 172.30.192.2 iz2ze39jeyizepdxhwqci6z
default ceph-pod2-with-secret-on-master 1/1 Unknown 0 34m 172.30.0.51 iz25beglnhtz
default nginx-kit-3630450072-2c0jk 0/2 Pending 0 12m <none>
default nginx-kit-3630450072-3n50m 2/2 Unknown 20 35d 172.30.0.44 iz25beglnhtz
default nginx-kit-3630450072-90v4q 0/2 Pending 0 12m <none>
default nginx-kit-3630450072-j8qrk 2/2 Unknown 20 72d 172.30.0.47 iz25beglnhtz
kube-system dummy-2088944543-9382n 1/1 Running 0 12m xx.xx.xx.xx yypdmaster
kube-system dummy-2088944543-93f4c 1/1 Unknown 16 130d xx.xx.xx.xx iz25beglnhtz
kube-system elasticsearch-logging-v1-dhl35 1/1 Running 0 12m 172.30.192.6 yypdnode
kube-system elasticsearch-logging-v1-s3sbj 1/1 Unknown 9 35d 172.30.0.45 iz25beglnhtz
kube-system elasticsearch-logging-v1-t8wg0 1/1 Unknown 29 68d 172.30.0.43 iz25beglnhtz
kube-system elasticsearch-logging-v1-zdp19 1/1 Running 0 12m 172.30.0.3 yypdmaster
kube-system etcd-iz25beglnhtz 1/1 Unknown 17 130d xx.xx.xx.xx iz25beglnhtz
kube-system etcd-yypdmaster 1/1 Running 17 17m xx.xx.xx.xx yypdmaster
kube-system fluentd-es-v1.22-ggvv4 1/1 NodeLost 24 68d 172.30.0.46 iz25beglnhtz
kube-system fluentd-es-v1.22-rj871 1/1 Running 0 17m 172.30.0.1 yypdmaster
kube-system fluentd-es-v1.22-xn77x 1/1 NodeLost 0 6d 172.30.192.0 iz2ze39jeyizepdxhwqci6z
kube-system fluentd-es-v1.22-z82rz 1/1 Running 0 18m 172.30.192.5 yypdnode
kube-system kibana-logging-3746979809-dplzv 1/1 Running 0 12m 172.30.0.4 yypdmaster
kube-system kibana-logging-3746979809-lq9m3 1/1 Unknown 9 35d 172.30.0.49 iz25beglnhtz
kube-system kube-apiserver-iz25beglnhtz 1/1 Unknown 19 104d xx.xx.xx.xx iz25beglnhtz
kube-system kube-apiserver-yypdmaster 1/1 Running 19 17m xx.xx.xx.xx yypdmaster
kube-system kube-controller-manager-iz25beglnhtz 1/1 Unknown 21 130d xx.xx.xx.xx iz25beglnhtz
kube-system kube-controller-manager-yypdmaster 1/1 Running 21 17m xx.xx.xx.xx yypdmaster
kube-system kube-discovery-1769846148-wh1z4 1/1 Unknown 12 73d xx.xx.xx.xx iz25beglnhtz
kube-system kube-discovery-1769846148-z2v87 0/1 Pending 0 12m <none>
kube-system kube-dns-2924299975-206tg 4/4 Unknown 129 130d 172.30.0.48 iz25beglnhtz
kube-system kube-dns-2924299975-g1kks 4/4 Running 0 12m 172.30.0.5 yypdmaster
kube-system kube-proxy-3z29k 1/1 Running 0 18m yy.yy.yy.yy yypdnode
kube-system kube-proxy-kfzxv 1/1 Running 0 17m xx.xx.xx.xx yypdmaster
kube-system kube-proxy-n2xmf 1/1 NodeLost 16 130d xx.xx.xx.xx iz25beglnhtz
```


观察这个输出，我们看到几点异常：

- 不常见的Pod状态：Unknown、NodeLost
- Node一列居然出现了四个Node: yypdmaster、yypdnode、 iz25beglnhtz和 iz2ze39jeyizepdxhwqci6z

等了一会儿，这种状态依然不见好转。我于是重启了master上的kubelet、重启了两个节点上的docker engine，不过启动后问题依旧！

查看Running状态的Pod情况：

```
# kubectl get pod --all-namespaces -o wide|grep Running
kube-system dummy-2088944543-9382n 1/1 Running 0 18m xx.xx.xx.xx yypdmaster
kube-system elasticsearch-logging-v1-dhl35 1/1 Running 0 18m 172.30.192.6 yypdnode
kube-system elasticsearch-logging-v1-zdp19 1/1 Running 0 18m 172.30.0.3 yypdmaster
kube-system etcd-yypdmaster 1/1 Running 17 23m xx.xx.xx.xx yypdmaster
kube-system fluentd-es-v1.22-rj871 1/1 Running 0 23m 172.30.0.1 yypdmaster
kube-system fluentd-es-v1.22-z82rz 1/1 Running 0 24m 172.30.192.5 yypdnode
kube-system kibana-logging-3746979809-dplzv 1/1 Running 0 18m 172.30.0.4 yypdmaster
kube-system kube-apiserver-yypdmaster 1/1 Running 19 23m xx.xx.xx.xx yypdmaster
kube-system kube-controller-manager-yypdmaster 1/1 Running 21 23m xx.xx.xx.xx yypdmaster
kube-system kube-dns-2924299975-g1kks 4/4 Running 0 18m 172.30.0.5 yypdmaster
kube-system kube-proxy-3z29k 1/1 Running 0 24m yy.yy.yy.yy yypdnode
kube-system kube-proxy-kfzxv 1/1 Running 0 23m xx.xx.xx.xx yypdmaster
kube-system kube-scheduler-yypdmaster 1/1 Running 22 23m xx.xx.xx.xx yypdmaster
kube-system kubernetes-dashboard-3109525988-cj74d 1/1 Running 0 18m 172.30.0.6 yypdmaster
mioss-namespace-s0fcvegcmw console-sm7cg2-101699315-f3g55 1/1 Running 0 18m 172.30.0.7 yypdmaster
```


似乎Kubernetes集群并未真正”Crash”，但从Node列来看，正常的pod归属的node不是yypdmaster就是yypdnode， iz25beglnhtz和 iz2ze39jeyize

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

抱歉，暂停评论。