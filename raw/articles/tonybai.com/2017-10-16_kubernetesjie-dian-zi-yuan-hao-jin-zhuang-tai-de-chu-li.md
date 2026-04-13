---
title: Kubernetes节点资源耗尽状态的处理
url: https://tonybai.com/2017/10/16/out-of-node-resource-handling-in-kubernetes-cluster/
published: '2017-10-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes节点资源耗尽状态的处理

今天上午一到工位，就收到来自同事的“投诉”：私有云上的[Kubernetes](http://tonybai.com/tag/kubernetes) cluster中的一个node似乎不工作了，因为专门部署于那个节点上的应用挂掉了，并且长时间没有恢复。这个公司私有云上Kubernetes集群是[v1.7.5版本](https://github.com/kubernetes/kubernetes/releases/tag/v1.7.5)，部署于双节假期之前。最近感觉K8s开发明显提速，连续发布版本，截至发稿时，最新发布的版本为[v1.8.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.8.1)了。这个集群一直运行相对稳定，今天这个异常到底是怎么一回事呢？于是打开terminal，开始了问题的调查。

## 一、问题现象

我们这个小集群一共有三个Kubernetes Node。首先，我查看集群中的所有Pods状态，发现node1和node2上的Pods均正常(running状态)，但位于node3上的三个Pods均为“Pending”状态，这三个pod是weave-net-rh6r4、kube-proxy-v4d1p以及portal-3613605798-txq4l，其中portal-3613605798-txq4l是我们的应用Pod。K8s自身的组件kube-proxy都异常了，显然node3节点出问题了。如果你此刻去尝试查看(kubectl describe) 这几个pod的状态，多半你会失败，因为Pod在频繁重启，1-2s钟新创建的Pod就会被kill掉，导致你无法查看其状态。

我直接查看一下node3的状态，果不其然，我得到了一些Warning events:

```
# kubectl describe ubuntu-k8s-3
... ...
Events:
FirstSeen LastSeen Count From SubObjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
51m 51m 1 kubelet, ubuntu-k8s-3 Normal NodeNotSchedulable Node ubuntu-k8s-3 status is now: NodeNotSchedulable
9d 51m 49428 kubelet, ubuntu-k8s-3 Warning EvictionThresholdMet Attempting to reclaim nodefs
5m 5m 1 kubelet, ubuntu-k8s-3 Normal Starting Starting kubelet.
5m 5m 2 kubelet, ubuntu-k8s-3 Normal NodeHasSufficientDisk Node ubuntu-k8s-3 status is now: NodeHasSufficientDisk
5m 5m 2 kubelet, ubuntu-k8s-3 Normal NodeHasSufficientMemory Node ubuntu-k8s-3 status is now: NodeHasSufficientMemory
5m 5m 2 kubelet, ubuntu-k8s-3 Normal NodeHasNoDiskPressure Node ubuntu-k8s-3 status is now: NodeHasNoDiskPressure
5m 5m 1 kubelet, ubuntu-k8s-3 Normal NodeAllocatableEnforced Updated Node Allocatable limit across pods
5m 5m 1 kubelet, ubuntu-k8s-3 Normal NodeHasDiskPressure Node ubuntu-k8s-3 status is now: NodeHasDiskPressure
5m 14s 23 kubelet, ubuntu-k8s-3 Warning EvictionThresholdMet Attempting to reclaim nodefs
```


两点有价值的内容：

1、Node ubuntu-k8s-3 status is now: NodeHasDiskPressure

2、Warning: “EvictionThresholdMet Attempting to reclaim nodefs”

从以上内容大致可以判断出node3处于磁盘空间不足的状态下，并且该node上的kubelet daemon判断达到了Eviction阀值，试图回收磁盘空间（通过某种杀Pod的方式，I Guess）。

既然提到了Kubelet，我们再来看看这一后台service的log：

```
# journalctl -u kubelet -f
10月 16 09:50:55 ubuntu-k8s-3 kubelet[17144]: W1016 09:50:55.056703 17144 eviction_manager.go:331] eviction manager: attempting to reclaim nodefs
10月 16 09:50:55 ubuntu-k8s-3 kubelet[17144]: I1016 09:50:55.057322 17144 eviction_manager.go:345] eviction manager: must evict pod(s) to reclaim nodefs
10月 16 09:50:55 ubuntu-k8s-3 kubelet[17144]: E1016 09:50:55.058307 17144 eviction_manager.go:356] eviction manager: eviction thresholds have been met, but no pods are active to evict
... ...
10月 16 09:54:14 ubuntu-k8s-3 kubelet[12844]: W1016 09:54:14.823152 12844 eviction_manager.go:142] Failed to admit pod weave-net-3svfg_kube-system(e5a5d474-b214-11e7-a98b-0650cc001a5b) - node has conditions: [DiskPressure]
10月 16 09:54:14 ubuntu-k8s-3 kubelet[12844]: W1016 09:54:14.824246 12844 eviction_manager.go:142] Failed to admit pod kube-proxy-d9lk0_kube-system(e5ff8fde-b214-11e7-a98b-0650cc001a5b) - node has conditions: [DiskPressure]
```


kubelet日志也印证了上面的判断：node3因为磁盘不足不再参与pod调度，但尝试回收磁盘空间时却发现已经没有active pod可以kill了！

## 二、原因分析

既然提到了磁盘不足，我们就来看看磁盘占用情况：

```
# df -h
文件系统 容量 已用 可用 已用% 挂载点
udev 2.0G 0 2.0G 0% /dev
tmpfs 396M 46M 350M 12% /run
/dev/sda1 5.8G 5.1G 448M 92% /
tmpfs 2.0G 288K 2.0G 1% /dev/shm
tmpfs 5.0M 0 5.0M 0% /run/lock
tmpfs 2.0G 0 2.0G 0% /sys/fs/cgroup
/dev/sdb1 99G 5.2G 89G 6% /data
tmpfs 396M 0 396M 0% /run/user/0
... ...
```


我们看到root分区的磁盘占用率已经达到了92%，仅剩下不到500M空间可以使用了。我们的私有云提供的ubuntu vm模板太过死板（无法定制），每个vm挂载的root分区只能是6G，多一点都不可以。这样在安装完一些必要的软件后，根分区占用率就很高了。为此，之前我们还特意挂载了一块专用盘(/dev/sdb1)用于存储docker的相关image和容器运行数据，并将原先的docker数据迁移到新位置(/data/docker)。

附：docker运行时数据迁移方法（适用于

[docker]1.12.x以后版本）：

a) 创建/etc/docker/daemon.json文件内容如下：


{

“graph”: “/data/docker”,

“storage-driver”: “aufs”

}b) 停止docker并迁移数据


systemctl stop docker

mv /var/lib/docker /datac) 重启docker


systemctl daemon-reload

systemctl restart docker

由于某些原因，我们的那个portal pod必须运行于该node上（通过[nodeSelector](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/)选定node的方式）。在无法扩充根分区size的情况下，为了临时恢复pod运行，我们只能进一步“压榨”node了。于是我们的思路是：通过调整node的eviction threshold值来让node恢复healthy。

## 三、解决方案

要解决这一问题，我们需要阅读一下k8s官方的[关于”Eviction Policy”的说明](https://kubernetes.io/docs/tasks/administer-cluster/out-of-resource/)。大致意思就是：每个node上的kubelet都负责定期采集资源占用数据，并与预设的 threshold值进行比对，如果超过 threshold值，kubelet就会尝试杀掉一些Pod以回收相关资源，对Node进行保护。kubelet关注的资源指标threshold大约有如下几种：

```
- memory.available
- nodefs.available
- nodefs.inodesFree
- imagefs.available
- imagefs.inodesFree
```


每种threshold又分为eviction-soft和eviction-hard两组值。soft和hard的区别在于前者在到达threshold值时会给pod一段时间优雅退出，而后者则崇尚“暴力”，直接杀掉pod，没有任何优雅退出的机会。这里还要提一下nodefs和imagefs的区别：

- nodefs: 指node自身的存储，存储daemon的运行日志等，一般指root分区/；
- imagefs: 指docker daemon用于存储image和容器可写层(writable layer)的磁盘；

在我们的例子中，我们的imagefs是/dev/sdb1,磁盘占用率很低；而nodefs，即/分区占用率很高（92%)。

我们重启一次kubelet，查看一下这些threshold的当前值(通过journalctl -u kubelet -f查看)：

```
10月 16 09:54:09 ubuntu-k8s-3 systemd[1]: Started kubelet: The Kubernetes Node Agent.
10月 16 09:54:09 ubuntu-k8s-3 kubelet[12844]: I1016 09:54:09.381711 12844 feature_gate.go:144] feature gates: map[]
10月 16 09:54:09 ubuntu-k8s-3 kubelet[12844]: I1016 09:54:09.437470 12844 client.go:72] Connecting to docker on unix:///var/run/docker.sock
10月 16 09:54:09 ubuntu-k8s-3 kubelet[12844]: I1016 09:54:09.438075 12844 client.go:92] Start docker client with request timeout=2m0s
10月 16 09:54:09 ubuntu-k8s-3 kubelet[12844]: I1016 09:54:09.471485 12844 manager.go:143] cAdvisor running in container: "/system.slice/kubelet.service"
... ...
10月 16 09:54:09 ubuntu-k8s-3 kubelet[12844]: I1016 09:54:09.615818 12844 container_manager_linux.go:246] container manager verified user specified cgroup-root exists: /
10月 16 09:54:09 ubuntu-k8s-3 kubelet[12844]: I1016 09:54:09.616263 12844 container_manager_linux.go:251] Creating Container Manager object based on Node Config: {RuntimeCgroupsName: SystemCgroupsName: KubeletCgroupsName: ContainerRuntime:docker CgroupsPerQOS:true CgroupRoot:/ CgroupDriver:cgroupfs ProtectKernelDefaults:false NodeAllocatableConfig:{KubeReservedCgroupName: SystemReservedCgroupName: EnforceNodeAllocatable:map[pods:{}] KubeReserved:map[] SystemReserved:map[] HardEvictionThresholds:[{Signal:memory.available Operator:LessThan Value:{Quantity:100Mi Percentage:0} GracePeriod:0s MinReclaim:<nil>} {Signal:nodefs.available Operator:LessThan Value:{Quantity:<nil> Percentage:0.1} GracePeriod:0s MinReclaim:<nil>} {Signal:nodefs.inodesFree Operator:LessThan Value:{Quantity:<nil> Percentage:0.05} GracePeriod:0s MinReclaim:<nil>}]} ExperimentalQOSReserved:map[]}
10月 16 09:54:09 ubuntu-k8s-3 kubelet[12844]: I1016 09:54:09.617680 12844 kubelet.go:263] Adding manifest file: /etc/kubernetes/manifests
10月 16 09:54:09 ubuntu-k8s-3 kubelet[12844]: I1016 09:54:09.618196 12844 kubelet.go:273] Watching apiserver
... ...
```


把涉及到threshold的信息重新格式化一下：

```
HardEvictionThresholds: [
{
Signal: memory.availableOperator: LessThanValue: {
Quantity: 100MiPercentage: 0
}GracePeriod: 0sMinReclaim: <nil>
}{
Signal: nodefs.availableOperator: LessThanValue: {
Quantity: <nil>Percentage: 0.1
}GracePeriod: 0sMinReclaim: <nil>
}{
Signal: nodefs.inodesFreeOperator: LessThanValue: {
Quantity: <nil>Percentage: 0.05
}GracePeriod: 0sMinReclaim: <nil>
}
]
```


我们看到初始情况下，kubelet并没有设置Soft Eviction，只是对memory和nodefs设置了hard eviction threshold值。这里最值得我们关注的是：nodefs.available percentage: 0.1。也就是说当nodefs的可用空间低于10%时，该node上的kubelet将会执行eviction动作。而我们的根分区剩余可用空间为8%，显然满足了这个条件，于是问题就发生了。

我们要做的就是临时修改这个值，可以将其设为<5%。

## 四、解决步骤

我们需要为kubelet重新设定nodefs.available的threshold值。怎么做呢？

[kubelet](https://kubernetes.io/docs/admin/kubelet/)是运行于每个kubernetes node上的daemon，它在system boot时由[systemd](http://en.wikipedia.org/wiki/Systemd)拉起:

```
root@ubuntu-k8s-3:~# ps -ef|grep kubelet
root 5718 5695 0 16:38 pts/3 00:00:00 grep --color=auto kubelet
root 13640 1 4 10:25 ? 00:17:25 /usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true --network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin --cluster-dns=10.96.0.10 --cluster-domain=cluster.local --authorization-mode=Webhook --client-ca-file=/etc/kubernetes/pki/ca.crt --cadvisor-port=0
```


查看一下kubelet service的状态：

```
root@ubuntu-k8s-3:~# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
Drop-In: /etc/systemd/system/kubelet.service.d
└─10-kubeadm.conf
Active: active (running) since 一 2017-10-16 10:25:09 CST; 6h ago
Docs: http://kubernetes.io/docs/
Main PID: 13640 (kubelet)
Tasks: 18
Memory: 62.0M
CPU: 18min 15.235s
CGroup: /system.slice/kubelet.service
├─13640 /usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true --
└─13705 journalctl -k -f
.... ...
```


通过status的输出，我们看到关于kubelet service有两个systemd service配置文件与之启动相关：

```
- /lib/systemd/system/kubelet.service
Drop-In: /etc/systemd/system/kubelet.service.d
└─10-kubeadm.conf
```


/lib/systemd/system/kubelet.service比较简单：

```
[Unit]
Description=kubelet: The Kubernetes Node Agent
Documentation=http://kubernetes.io/docs/
[Service]
ExecStart=/usr/bin/kubelet
Restart=always
StartLimitInterval=0
RestartSec=10
[Install]
WantedBy=multi-user.target
```


/etc/systemd/system/kubelet.service.d/10-kubeadm.conf是systemd中用于override kubelet.service中部分配置的drop-in文件，kubelet的启动配置都在这里：

```
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true"
Environment="KUBELET_SYSTEM_PODS_ARGS=--pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true"
Environment="KUBELET_NETWORK_ARGS=--network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin"
Environment="KUBELET_DNS_ARGS=--cluster-dns=10.96.0.10 --cluster-domain=cluster.local"
Environment="KUBELET_AUTHZ_ARGS=--authorization-mode=Webhook --client-ca-file=/etc/kubernetes/pki/ca.crt"
Environment="KUBELET_CADVISOR_ARGS=--cadvisor-port=0"
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_SYSTEM_PODS_ARGS $KUBELET_NETWORK_ARGS $KUBELET_DNS_ARGS $KUBELET_AUTHZ_ARGS $KUBELET_CADVISOR_ARGS $KUBELET_EXTRA_ARGS
```


systemd启动kubelet时会用10-kubeadm.conf中的ExecStart覆盖/lib/systemd/system/kubelet.service中的ExecStart，这样我们才能看到上面kubelet后面那一长溜命令行启动参数。我们要做的就是在这行启动参数后面添加上我们想设置的nodefs.available的threshold值。

出于配置风格一致的考量，我们定义一个新的Environment var，比如就叫：KUBELET_EVICTION_POLICY_ARGS：

```
Environment="KUBELET_EVICTION_POLICY_ARGS=--eviction-hard=nodefs.available<5%"
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_SYSTEM_PODS_ARGS $KUBELET_NETWORK_ARGS $KUBELET_DNS_ARGS $KUBELET_AUTHZ_ARGS $KUBELET_CADVISOR_ARGS $KUBELET_EXTRA_ARGS $KUBELET_EVICTION_POLICY_ARGS
```


重启kubelet，我们通过日志看threshold的新值是否生效：

```
10月 16 16:56:10 ubuntu-k8s-3 kubelet[7394]: I1016 16:56:10.840914 7394 container_manager_linux.go:251] Creating Container Manager object based on Node Config: {RuntimeCgroupsName: SystemCgroupsName: KubeletCgroupsName: ContainerRuntime:docker CgroupsPerQOS:true CgroupRoot:/ CgroupDriver:cgroupfs ProtectKernelDefaults:false NodeAllocatableConfig:{KubeReservedCgroupName: SystemReservedCgroupName: EnforceNodeAllocatable:map[pods:{}] KubeReserved:map[] SystemReserved:map[] HardEvictionThresholds:[{Signal:nodefs.available Operator:LessThan Value:{Quantity:<nil> Percentage:0.05} GracePeriod:0s MinReclaim:<nil>}]} ExperimentalQOSReserved:map[]}
```


我们看到下面这一行，表明新配置已经生效：

```
Signal:nodefs.available Operator:LessThan Value:{Quantity:<nil> Percentage:0.05}
```


查看pods状态，原先处于pending状态的三个pod均变成了”running”状态，问题得以解决。

## 五、参考资料

1) 《[Handling Out of Resource Errors](https://docs.openshift.org/latest/admin_guide/out_of_resource_handling.html)》

2) 《[Configure Out Of Resource Handling](https://kubernetes.io/docs/tasks/administer-cluster/out-of-resource/)》

3) 《[Systemd 入门教程：实战篇](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)》

4) 《[System bootup process](https://www.freedesktop.org/software/systemd/man/bootup.html)》

5) 《[Systemd for upstart users- ubuntu wiki](https://wiki.ubuntu.com/SystemdForUpstartUsers)》

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

博主好，这篇博文给我了很大的帮助，不过想咨询一下，既然可以通过修改docker挂载数据盘的方式保证imagefs不会超过阈值，是否可以修改nodefs的挂载数据盘使nodefs也不会超过阈值呢？最近遇到了些比较棘手的问题，主要是因为nodefs需要的根目录容量不够了，而又不能轻易的删除文件，所以想问问是否有修改nodefs挂载数据盘的方式？谢谢博主！

nodefs就是指kubernetes node节点的根目录吧，即文件系统的/目录。这个如果要设置也是在kubelet的启动参数中设置，但kubelet似乎没有设置nodefs的地方。而imagefs的值其实是kubelet向docker询问的结果，在docker中可以通过docker info查看runtime dir。

kubelet flag –root-dir 可以配置

多谢指教:)

very good article, thanks

白老师，您好，想请教一下，如果k8s所在的node的根分区实现了动态扩容（例如使用了XFS文件系统的扩容命令，扩大了根分区的容量），是不是必须重启kubelet的方式才能让这次扩容被k8s的node识别出来，有不用重启kubelet的办法么？

个人觉得kubelet是有一个定期采集node disk参数的机制的，以定期判断是否出现了node disk pressure。