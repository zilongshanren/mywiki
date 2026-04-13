---
title: Kubernetes集群中Service的滚动更新
url: https://tonybai.com/2017/02/09/rolling-update-for-services-in-kubernetes-cluster/
published: '2017-02-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes集群中Service的滚动更新

在移动互联网时代，消费者的消费行为已经“全天候化”，为此，商家的业务系统也要保持7×24小时不间断地提供服务以满足消费者的需求。很难想像如今还会有以“中断业务”为前提的服务系统更新升级。如果[微信](http://weixin.qq.com/)官方发布公告说：每周六晚23:00~次日凌晨2:00进行例行系统升级，不能提供服务，作为用户的你会怎么想、怎么做呢？因此，各个平台在最初设计时就要考虑到服务的更新升级问题，部署在[Kubernetes集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)中的Service也不例外。

### 一、预备知识

#### 1、滚动更新Rolling-update

传统的升级更新，是先将服务全部下线，业务停止后再更新版本和配置，然后重新启动并提供服务。这样的模式已经完全不能满足“时代的需要”了。在并发化、高可用系统普及的今天，服务的升级更新至少要做到“业务不中断”。而滚动更新(Rolling-update)恰是满足这一需求的一种系统更新升级方案。

简单来说，滚动更新就是针对多实例服务的一种不中断服务的更新升级方式。一般情况，对于多实例服务，滚动更新采用对各个实例逐个进行单独更新而非同一时刻对所有实例进行全部更新的方式。“滚动更新”的先进之处在于“滚动”这个概念的引入，笔者觉得它至少有以下两点含义：

a) “滚动”给人一种“圆”的映像，表意：持续，不中断。“滚动”的理念是一种趋势，我们常见的“[滚动发布](https://en.wikipedia.org/wiki/Rolling_release)”、“[持续交付](https://en.wikipedia.org/wiki/Continuous_delivery)”都是“滚动”理念的应用。与传统的大版本周期性发布/更新相比，”滚动”可以让用户更快、更及时地使用上新Feature，缩短市场反馈周期，同时滚动式的发布和更新又会将对用户体验的影响降到最小化。

b) “滚动”可向前，也可向后。我们可以在更新过程中及时发现“更新”存在的问题，并“向后滚动”，实现更新的回退，可以最大程度上降低每次更新升级的风险。

对于在[Kubernetes集群部署](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)的Service来说，Rolling update就是指一次仅更新一个Pod，并逐个进行更新，而不是在同一时刻将该Service下面的所有Pod shutdown，避免将业务中断的尴尬。

#### 2、Service、Deployment、Replica Set、Replication Controllers和Pod之间的关系

对于我们要部署的Application来说，一般是由多个抽象的Service组成。在Kubernetes中，一个[Service](https://kubernetes.io/docs/user-guide/services/)通过[label selector](https://kubernetes.io/docs/user-guide/labels/) match出一个Pods集合，这些Pods作为Service的endpoint，是真正承载业务的实体。而Pod在集群内的部署、调度、副本数保持则是通过[Deployment](https://kubernetes.io/docs/user-guide/deployments/)或[ReplicationControllers](https://kubernetes.io/docs/user-guide/replication-controller/)这些高level的抽象来管理的，下面是一幅示意图：

![img{512x368}](../../assets/fa5112fce77d8c44.png)


新版本的Kubernetes推荐用[Deployment](https://kubernetes.io/docs/user-guide/managing-deployments/)替代ReplicationController，在Deployment这个概念下在保持Pod副本数上实际发挥作用的是隐藏在背后的[Replica Set](https://kubernetes.io/docs/user-guide/replicasets/)。

因此，我们可以看到Kubernetes上Service的[rolling update](https://kubernetes.io/docs/user-guide/rolling-updates/)实质上是对Service所match出来的Pod集合的Rolling update，而控制Pod部署、调度和副本调度的却又恰恰是Deployment和replication controller，因此后两者才是kubernetes service rolling update真正要面对的实体。

### 二、kubectl rolling-update子命令

kubernetes在kubectl cli工具中仅提供了对Replication Controller的rolling-update支持，通过kubectl -help，我们可以查看到下面的命令usage描述：

```
# kubectl -help
... ...
Deploy Commands:
rollout Manage a deployment rollout
rolling-update Perform a rolling update of the given ReplicationController
scale Set a new size for a Deployment, ReplicaSet, Replication Controller, or Job
autoscale Auto-scale a Deployment, ReplicaSet, or ReplicationController
... ...
# kubectl help rolling-update
... ...
Usage:
kubectl rolling-update OLD_CONTROLLER_NAME ([NEW_CONTROLLER_NAME] --image=NEW_CONTAINER_IMAGE | -f
NEW_CONTROLLER_SPEC) [options]
... ...
```


我们现在来看一个例子，看一下kubectl rolling-update是如何对service下的Pods进行滚动更新的。我们的kubernetes集群有两个版本的[Nginx](https://nginx.org/en/)：

```
# docker images|grep nginx
nginx 1.11.9 cc1b61406712 2 weeks ago 181.8 MB
nginx 1.10.1 bf2b4c2d7bf5 4 months ago 180.7 MB
```


在例子中我们将Service的Pod从nginx 1.10.1版本滚动升级到1.11.9版本。

我们的rc-demo-v0.1.yaml文件内容如下：

```
apiVersion: v1
kind: ReplicationController
metadata:
name: rc-demo-nginx-v0.1
spec:
replicas: 4
selector:
app: rc-demo-nginx
ver: v0.1
template:
metadata:
labels:
app: rc-demo-nginx
ver: v0.1
spec:
containers:
- name: rc-demo-nginx
image: nginx:1.10.1
ports:
- containerPort: 80
protocol: TCP
env:
- name: RC_DEMO_VER
value: v0.1
```


创建这个replication controller：

```
# kubectl create -f rc-demo-v0.1.yaml
replicationcontroller "rc-demo-nginx-v0.1" created
# kubectl get pods -o wide
NAME READY STATUS RESTARTS AGE IP NODE
rc-demo-nginx-v0.1-2p7v0 1/1 Running 0 1m 172.30.192.9 iz2ze39jeyizepdxhwqci6z
rc-demo-nginx-v0.1-9pk3t 1/1 Running 0 1m 172.30.192.8 iz2ze39jeyizepdxhwqci6z
rc-demo-nginx-v0.1-hm6b9 1/1 Running 0 1m 172.30.0.9 iz25beglnhtz
rc-demo-nginx-v0.1-vbxpl 1/1 Running 0 1m 172.30.0.10 iz25beglnhtz
```


Service manifest文件rc-demo-svc.yaml的内容如下：

```
apiVersion: v1
kind: Service
metadata:
name: rc-demo-svc
spec:
ports:
- port: 80
protocol: TCP
selector:
app: rc-demo-nginx
```


创建这个service：

```
# kubectl create -f rc-demo-svc.yaml
service "rc-demo-svc" created
# kubectl describe svc/rc-demo-svc
Name: rc-demo-svc
Namespace: default
Labels: <none>
Selector: app=rc-demo-nginx
Type: ClusterIP
IP: 10.96.172.246
Port: <unset> 80/TCP
Endpoints: 172.30.0.10:80,172.30.0.9:80,172.30.192.8:80 + 1 more...
Session Affinity: None
No events.
```


可以看到之前replication controller创建的4个Pod都被置于rc-demo-svc这个service的下面了，我们来访问一下该服务：

```
# curl -I http://10.96.172.246:80
HTTP/1.1 200 OK
Server: nginx/1.10.1
Date: Wed, 08 Feb 2017 08:45:19 GMT
Content-Type: text/html
Content-Length: 612
Last-Modified: Tue, 31 May 2016 14:17:02 GMT
Connection: keep-alive
ETag: "574d9cde-264"
Accept-Ranges: bytes
# kubectl exec rc-demo-nginx-v0.1-2p7v0 env
... ...
RC_DEMO_VER=v0.1
... ...
```


通过Response Header中的Server字段，我们可以看到当前Service pods中的nginx版本为1.10.1；通过打印Pod中环境变量，得到RC_DEMO_VER=v0.1。

接下来，我们来rolling-update rc-demo-nginx-v0.1这个rc，我们的新rc manifest文件rc-demo-v0.2.yaml内容如下：

```
apiVersion: v1
kind: ReplicationController
metadata:
name: rc-demo-nginx-v0.2
spec:
replicas: 4
selector:
app: rc-demo-nginx
ver: v0.2
template:
metadata:
labels:
app: rc-demo-nginx
ver: v0.2
spec:
containers:
- name: rc-demo-nginx
image: nginx:1.11.9
ports:
- containerPort: 80
protocol: TCP
env:
- name: RC_DEMO_VER
value: v0.2
```


rc-demo-new.yaml与rc-demo-old.yaml有几点不同：rc的name、image的版本以及RC_DEMO_VER这个环境变量的值：

```
# diff rc-demo-v0.2.yaml rc-demo-v0.1.yaml
4c4
< name: rc-demo-nginx-v0.2
---
> name: rc-demo-nginx-v0.1
9c9
< ver: v0.2
---
> ver: v0.1
14c14
< ver: v0.2
---
> ver: v0.1
18c18
< image: nginx:1.11.9
---
> image: nginx:1.10.1
24c24
< value: v0.2
---
> value: v0.1
```


我们开始rolling-update，为了便于跟踪update过程，这里将update-period设为10s，即每隔10s更新一个Pod：

```
# kubectl rolling-update rc-demo-nginx-v0.1 --update-period=10s -f rc-demo-v0.2.yaml
Created rc-demo-nginx-v0.2
Scaling up rc-demo-nginx-v0.2 from 0 to 4, scaling down rc-demo-nginx-v0.1 from 4 to 0 (keep 4 pods available, don't exceed 5 pods)
Scaling rc-demo-nginx-v0.2 up to 1
Scaling rc-demo-nginx-v0.1 down to 3
Scaling rc-demo-nginx-v0.2 up to 2
Scaling rc-demo-nginx-v0.1 down to 2
Scaling rc-demo-nginx-v0.2 up to 3
Scaling rc-demo-nginx-v0.1 down to 1
Scaling rc-demo-nginx-v0.2 up to 4
Scaling rc-demo-nginx-v0.1 down to 0
Update succeeded. Deleting rc-demo-nginx-v0.1
replicationcontroller "rc-demo-nginx-v0.1" rolling updated to "rc-demo-nginx-v0.2"
```


从日志可以看出：kubectl rolling-update逐渐增加 rc-demo-nginx-v0.2的scale并同时逐渐减小 rc-demo-nginx-v0.1的scale值直至减到0。

在升级过程中，我们不断访问rc-demo-svc，可以看到新旧Pod版本共存的状态，服务并未中断：

```
# curl -I http://10.96.172.246:80
HTTP/1.1 200 OK
Server: nginx/1.10.1
... ...
# curl -I http://10.96.172.246:80
HTTP/1.1 200 OK
Server: nginx/1.11.9
... ...
# curl -I http://10.96.172.246:80
HTTP/1.1 200 OK
Server: nginx/1.10.1
... ...
```


更新后的一些状态信息：

```
# kubectl get rc
NAME DESIRED CURRENT READY AGE
rc-demo-nginx-v0.2 4 4 4 5m
# kubectl get pods
NAME READY STATUS RESTARTS AGE
rc-demo-nginx-v0.2-25b15 1/1 Running 0 5m
rc-demo-nginx-v0.2-3jlpk 1/1 Running 0 5m
rc-demo-nginx-v0.2-lcnf9 1/1 Running 0 6m
rc-demo-nginx-v0.2-s7pkc 1/1 Running 0 5m
# kubectl exec rc-demo-nginx-v0.2-25b15 env
... ...
RC_DEMO_VER=v0.2
... ...
```


官方文档说kubectl rolling-update是由client side实现的rolling-update，这是因为roll-update的逻辑都是由kubectl发出N条命令到APIServer完成的，在kubectl的代码中我们可以看到这点：

```
//https://github.com/kubernetes/kubernetes/blob/master/pkg/kubectl/cmd/rollingupdate.go
... ...
func RunRollingUpdate(f cmdutil.Factory, out io.Writer, cmd *cobra.Command, args []string, options *resource.FilenameOptions) error {
... ...
err = updater.Update(config)
if err != nil {
return err
}
... ...
}
//https://github.com/kubernetes/kubernetes/blob/master/pkg/kubectl/rolling_updater.go
func (r *RollingUpdater) Update(config *RollingUpdaterConfig) error {
... ...
// Scale newRc and oldRc until newRc has the desired number of replicas and
// oldRc has 0 replicas.
progressDeadline := time.Now().UnixNano() + config.Timeout.Nanoseconds()
for newRc.Spec.Replicas != desired || oldRc.Spec.Replicas != 0 {
// Store the existing replica counts for progress timeout tracking.
newReplicas := newRc.Spec.Replicas
oldReplicas := oldRc.Spec.Replicas
// Scale up as much as possible.
scaledRc, err := r.scaleUp(newRc, oldRc, desired, maxSurge, maxUnavailable, scaleRetryParams, config)
if err != nil {
return err
}
newRc = scaledRc
... ...
}
```


在rolling_updater.go中Update方法使用一个for循环完成了逐步减少old rc的replicas和增加new rc的replicas的工作，直到new rc到达期望值，old rc的replicas变为0。

通过kubectl rolling-update实现的滚动更新有很多不足：

- 由kubectl实现，很可能因为网络原因导致update中断；

- 需要创建一个新的rc，名字与要更新的rc不能一样；虽然这个问题不大，但实施起来也蛮别扭的；

- 回滚还需要执行rolling-update，只是用的老版本的rc manifest文件；

- service执行的rolling-update在集群中没有记录，后续无法跟踪rolling-update历史。

不过，由于Replication Controller已被Deployment这个抽象概念所逐渐代替，下面我们来考虑如何实现Deployment的滚动更新以及deployment滚动更新的优势。

### 三、Deployment的rolling-update

kubernetes Deployment是一个更高级别的抽象，就像文章开头那幅示意图那样，Deployment会创建一个Replica Set，用来保证Deployment中Pod的副本数。由于kubectl rolling-update仅支持replication controllers，因此要想rolling-updata deployment中的Pod，你需要修改Deployment自己的manifest文件并应用。这个修改会创建一个新的Replica Set，在scale up这个Replica Set的Pod数的同时，减少原先的Replica Set的Pod数，直至zero。而这一切都发生在Server端，并不需要kubectl参与。

我们同样来看一个例子。我们建立第一个版本的deployment manifest文件：deployment-demo-v0.1.yaml。

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: deployment-demo
spec:
replicas: 4
selector:
matchLabels:
app: deployment-demo-nginx
minReadySeconds: 10
template:
metadata:
labels:
app: deployment-demo-nginx
version: v0.1
spec:
containers:
- name: deployment-demo
image: nginx:1.10.1
ports:
- containerPort: 80
protocol: TCP
env:
- name: DEPLOYMENT_DEMO_VER
value: v0.1
```


创建该deployment：

```
# kubectl create -f deployment-demo-v0.1.yaml --record
deployment "deployment-demo" created
# kubectl get deployments
NAME DESIRED CURRENT UP-TO-DATE AVAILABLE AGE
deployment-demo 4 4 4 0 10s
# kubectl get rs
NAME DESIRED CURRENT READY AGE
deployment-demo-1818355944 4 4 4 13s
# kubectl get pods -o wide
NAME READY STATUS RESTARTS AGE IP NODE
deployment-demo-1818355944-78spp 1/1 Running 0 24s 172.30.0.10 iz25beglnhtz
deployment-demo-1818355944-7wvxk 1/1 Running 0 24s 172.30.0.9 iz25beglnhtz
deployment-demo-1818355944-hb8tt 1/1 Running 0 24s 172.30.192.9 iz2ze39jeyizepdxhwqci6z
deployment-demo-1818355944-jtxs2 1/1 Running 0 24s 172.30.192.8 iz2ze39jeyizepdxhwqci6z
# kubectl exec deployment-demo-1818355944-78spp env
... ...
DEPLOYMENT_DEMO_VER=v0.1
... ...
```


deployment-demo创建了ReplicaSet：deployment-demo-1818355944，用于保证Pod的副本数。

我们再来创建使用了该deployment中Pods的Service：

```
# kubectl create -f deployment-demo-svc.yaml
service "deployment-demo-svc" created
# kubectl get service
NAME CLUSTER-IP EXTERNAL-IP PORT(S) AGE
deployment-demo-svc 10.109.173.225 <none> 80/TCP 5s
kubernetes 10.96.0.1 <none> 443/TCP 42d
# kubectl describe service/deployment-demo-svc
Name: deployment-demo-svc
Namespace: default
Labels: <none>
Selector: app=deployment-demo-nginx
Type: ClusterIP
IP: 10.109.173.225
Port: <unset> 80/TCP
Endpoints: 172.30.0.10:80,172.30.0.9:80,172.30.192.8:80 + 1 more...
Session Affinity: None
No events.
# curl -I http://10.109.173.225:80
HTTP/1.1 200 OK
Server: nginx/1.10.1
... ...
```


好了，我们看到该service下有四个pods，Service提供的服务也运行正常。

接下来，我们对该Service进行更新。为了方便说明，我们建立了deployment-demo-v0.2.yaml文件，其实你也大可不必另创建文件，直接再上面的deployment-demo-v0.1.yaml文件中修改也行：

```
# diff deployment-demo-v0.2.yaml deployment-demo-v0.1.yaml
15c15
< version: v0.2
---
> version: v0.1
19c19
< image: nginx:1.11.9
---
> image: nginx:1.10.1
25c25
< value: v0.2
---
> value: v0.1
```


我们用deployment-demo-v0.2.yaml文件来更新之前创建的deployments中的Pods：

```
# kubectl apply -f deployment-demo-v0.2.yaml --record
deployment "deployment-demo" configured
```


apply命令是瞬间接收到apiserver返回的Response并结束的。但deployment的rolling-update过程还在进行：

```
# kubectl describe deployment deployment-demo
Name: deployment-demo
... ...
Replicas: 2 updated | 4 total | 3 available | 2 unavailable
StrategyType: RollingUpdate
MinReadySeconds: 10
RollingUpdateStrategy: 1 max unavailable, 1 max surge
Conditions:
Type Status Reason
---- ------ ------
Available True MinimumReplicasAvailable
OldReplicaSets: deployment-demo-1818355944 (3/3 replicas created)
NewReplicaSet: deployment-demo-2775967987 (2/2 replicas created)
Events:
FirstSeen LastSeen Count From SubObjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
12m 12m 1 {deployment-controller } Normal ScalingReplicaSet Scaled up replica set deployment-demo-1818355944 to 4
11s 11s 1 {deployment-controller } Normal ScalingReplicaSet Scaled up replica set deployment-demo-2775967987 to 1
11s 11s 1 {deployment-controller } Normal ScalingReplicaSet Scaled down replica set deployment-demo-1818355944 to 3
11s 11s 1 {deployment-controller } Normal ScalingReplicaSet Scaled up replica set deployment-demo-2775967987 to 2
# kubectl get pods
NAME READY STATUS RESTARTS AGE
deployment-demo-1818355944-78spp 1/1 Terminating 0 12m
deployment-demo-1818355944-hb8tt 1/1 Terminating 0 12m
deployment-demo-1818355944-jtxs2 1/1 Running 0 12m
deployment-demo-2775967987-5s9qx 0/1 ContainerCreating 0 0s
deployment-demo-2775967987-lf5gw 1/1 Running 0 12s
deployment-demo-2775967987-lxbx8 1/1 Running 0 12s
deployment-demo-2775967987-pr0hl 0/1 ContainerCreating 0 0s
# kubectl get rs
NAME DESIRED CURRENT READY AGE
deployment-demo-1818355944 1 1 1 12m
deployment-demo-2775967987 4 4 4 17s
```


我们可以看到这个update过程中ReplicaSet的变化，同时这个过程中服务并未中断，只是新旧版本短暂地交错提供服务：

```
# curl -I http://10.109.173.225:80
HTTP/1.1 200 OK
Server: nginx/1.11.9
... ...
# curl -I http://10.109.173.225:80
HTTP/1.1 200 OK
Server: nginx/1.10.1
... ...
# curl -I http://10.109.173.225:80
HTTP/1.1 200 OK
Server: nginx/1.10.1
... ...
```


最终所有Pod被替换为了v0.2版本：

```
kubectl exec deployment-demo-2775967987-5s9qx env
... ...
DEPLOYMENT_DEMO_VER=v0.2
... ...
# curl -I http://10.109.173.225:80
HTTP/1.1 200 OK
Server: nginx/1.11.9
... ...
```


我们发现deployment的create和apply命令都带有一个–record参数，这是告诉apiserver记录update的历史。通过kubectl rollout history可以查看deployment的update history：

```
# kubectl rollout history deployment deployment-demo
deployments "deployment-demo"
REVISION CHANGE-CAUSE
1 kubectl create -f deployment-demo-v0.1.yaml --record
2 kubectl apply -f deployment-demo-v0.2.yaml --record
```


如果没有加“–record”，那么你得到的历史将会类似这样的结果：

```
# kubectl rollout history deployment deployment-demo
deployments "deployment-demo"
REVISION CHANGE-CAUSE
1 <none>
```


同时，我们会看到old ReplicaSet并未被删除：

```
# kubectl get rs
NAME DESIRED CURRENT READY AGE
deployment-demo-1818355944 0 0 0 25m
deployment-demo-2775967987 4 4 4 13m
```


这些信息都存储在server端，方便回退！

Deployment下Pod的回退操作异常简单，通过rollout undo即可完成。rollout undo会将Deployment回退到record中的上一个revision（见上面rollout history的输出中有revision列）：

```
# kubectl rollout undo deployment deployment-demo
deployment "deployment-demo" rolled back
```


rs的状态又颠倒回来：

```
# kubectl get rs
NAME DESIRED CURRENT READY AGE
deployment-demo-1818355944 4 4 4 28m
deployment-demo-2775967987 0 0 0 15m
```


查看update历史:

```
# kubectl rollout history deployment deployment-demo
deployments "deployment-demo"
REVISION CHANGE-CAUSE
2 kubectl apply -f deployment-demo-v0.2.yaml --record
3 kubectl create -f deployment-demo-v0.1.yaml --record
```


可以看到history中最多保存了两个revision记录（这个Revision保存的数量应该可以设置）。

### 四、通过API实现的deployment rolling-update

我们的最终目标是通过API来实现service的rolling-update。Kubernetes提供了针对[deployment的Restful API](https://kubernetes.io/docs/api-reference/extensions/v1beta1/operations/)，包括：create、read、replace、delete、patch、rollback等。从这些API的字面意义上看，patch和rollback很可能符合我们的需要，我们需要验证一下。

我们将deployment置为v0.1版本，即：image: nginx:1.10.1，DEPLOYMENT_DEMO_VER=v0.1。然后我们尝试通过patch API将deployment升级为v0.2版本，由于patch API仅接收json格式的body内容，我们将 deployment-demo-v0.2.yaml转换为json格式：deployment-demo-v0.2.json。patch是局部更新，这里偷个懒儿，直接将全部deployment manifest内容发给了APIServer，让server自己做merge^0^。

执行下面curl命令：

```
# curl -H 'Content-Type:application/strategic-merge-patch+json' -X PATCH --data @deployment-demo-v0.2.json http://localhost:8080/apis/extensions/v1beta1/namespaces/default/deployments/deployment-demo
```


这个命令输出一个merge后的[Deployment json文件](https://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_deployment)，由于内容太多，这里就不贴出来了，内容参见：[patch-api-output.txt](https://github.com/bigwhite/experiments/blob/master/k8s-rolling-update-demo/deployments/patch-api-output.txt)。

跟踪命令执行时的deployment状态，我们可以看到该命令生效了：新旧两个rs的Scale值在此消彼长，两个版本的Pod在交替提供服务。

```
# kubectl get rs
NAME DESIRED CURRENT READY AGE
deployment-demo-1818355944 3 3 3 12h
deployment-demo-2775967987 2 2 2 12h
# curl -I http://10.109.173.225:80
HTTP/1.1 200 OK
Server: nginx/1.10.1
... ...
# curl -I http://10.109.173.225:80
HTTP/1.1 200 OK
Server: nginx/1.11.9
... ...
# curl -I http://10.109.173.225:80
HTTP/1.1 200 OK
Server: nginx/1.10.1
... ...
```


不过通过这种方式update后，通过rollout history查看到的历史就有些“不那么精确了”：

```
#kubectl rollout history deployment deployment-demo
deployments "deployment-demo"
REVISION CHANGE-CAUSE
8 kubectl create -f deployment-demo-v0.1.yaml --record
9 kubectl create -f deployment-demo-v0.1.yaml --record
```


目前尚无好的方法。但rolling update的确是ok了。

Patch API支持三种类型的Content-type：json-patch+json、strategic-merge-patch+json和merge-patch+json。对于后面两种，从测试效果来看，都一样。但json-patch+json这种类型在测试的时候一直报错：

```
# curl -H 'Content-Type:application/json-patch+json' -X PATCH --data @deployment-demo-v0.2.json http://localhost:8080/apis/extensions/v1beta1/namespaces/default/deployments/deployment-demo
{
"kind": "Status",
"apiVersion": "v1",
"metadata": {},
"status": "Failure",
"message": "json: cannot unmarshal object into Go value of type jsonpatch.Patch",
"code": 500
}
```


kubectl patch子命令似乎使用的是strategic-merge-patch+json。源码中也没有过多说明三种方式的差别：

```
//pkg/kubectl/cmd/patch.go
func getPatchedJSON(patchType api.PatchType, originalJS, patchJS []byte, obj runtime.Object) ([]byte, error) {
switch patchType {
case api.JSONPatchType:
patchObj, err := jsonpatch.DecodePatch(patchJS)
if err != nil {
return nil, err
}
return patchObj.Apply(originalJS)
case api.MergePatchType:
return jsonpatch.MergePatch(originalJS, patchJS)
case api.StrategicMergePatchType:
return strategicpatch.StrategicMergePatchData(originalJS, patchJS, obj)
default:
// only here as a safety net - go-restful filters content-type
return nil, fmt.Errorf("unknown Content-Type header for patch: %v", patchType)
}
}
// DecodePatch decodes the passed JSON document as an RFC 6902 patch.
// MergePatch merges the patchData into the docData.
// StrategicMergePatch applies a strategic merge patch. The patch and the original document
// must be json encoded content. A patch can be created from an original and a modified document
// by calling CreateStrategicMergePatch.
```


接下来，我们使用deployment rollback API实现deployment的rollback。我们创建一个deployment-demo-rollback.json文件作为请求的内容：

```
//deployment-demo-rollback.json
{
"name" : "deployment-demo",
"rollbackTo" : {
"revision" : 0
}
}
```


revision:0 表示回退到上一个revision。执行下面命令实现rollback：

```
# curl -H 'Content-Type:application/json' -X POST --data @deployment-demo-rollback.json http://localhost:8080/apis/extensions/v1beta1/namespaces/default/deployments/deployment-demo/rollback
{
"kind": "Status",
"apiVersion": "v1",
"metadata": {},
"status": "Failure",
"message": "rollback request for deployment \"deployment-demo\" succeeded",
"code": 200
}
# kubectl describe deployment/deployment-demo
... ...
Events:
FirstSeen LastSeen Count From SubObjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
... ...
27s 27s 1 {deployment-controller } Normal DeploymentRollback Rolled back deployment "deployment-demo" to revision 1
... ...
```


通过查看deployment状态可以看出rollback成功了。但这个API的response似乎有些bug，明明是succeeded了(code:200)，但status却是”Failure”。

如果你在patch或rollback过程中还遇到什么其他问题，可以通过kubectl describe deployment/deployment-demo 查看输出的Events中是否有异常提示。

### 五、小结

从上面的实验来看，通过Kubernetes提供的API是可以实现Service中Pods的rolling-update的，但这更适用于无状态的Service。对于那些[有状态的Service](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)（通过[PetSet](https://kubernetes.io/docs/user-guide/petset)或是1.5版本后的[Stateful Set](https://kubernetes.io/docs/tasks/manage-stateful-set/scale-stateful-set)实现的），这么做是否还能满足要求还不能确定。由于暂时没有环境，这方面尚未测试。

上述各个manifest的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/k8s-rolling-update-demo)下载到。

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

您好，看了文章，讲的很好，因为apply执行后是马上就返回结果。如果想跟踪后续新的副本是否完全替代旧的副本，即滚动更新时候发布成功，如何用api实现呢？盼复，谢谢

kubectl 执行的所有操作在kubernetes api中都有对应的api的接口，建议详细查看kubernetes api文档，找到并调用对应接口查看rolling update的结果。

您好，我也遇到了跟您一样的问题(跟踪后续新的副本是否完全替代旧的副本，即滚动更新是否发布成功)，请问您找到对应的api了吗，或者说您是怎么实现这个功能的呢？盼复，谢谢！