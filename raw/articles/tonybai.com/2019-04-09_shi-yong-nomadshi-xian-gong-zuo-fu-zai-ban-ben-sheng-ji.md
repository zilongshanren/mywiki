---
title: 使用nomad实现工作负载版本升级
url: https://tonybai.com/2019/04/09/upgrade-workload-using-nomad/
published: '2019-04-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用nomad实现工作负载版本升级

书接[上文](https://tonybai.com/2019/03/30/cluster-management-and-microservice-deployment-and-scheduled-by-nomad/)。

在[《使用nomad实现集群管理和微服务部署调度》](https://tonybai.com/2019/03/30/cluster-management-and-microservice-deployment-and-scheduled-by-nomad/)一文中，我们介绍了使用nomad进行集群管理和工作负载调度的轻量级方案（相较于[Kubernetes方案](https://tonybai.com/tag/kubernetes)）。在本文中，我们继续对方案进行延展，介绍一下在nomad集群中工作负载版本升级的一些常用模式和实现方法，包括[滚动升级](https://en.wikipedia.org/wiki/Rolling_release)、[蓝绿部署](https://www.martinfowler.com/bliki/BlueGreenDeployment.html)和[金丝雀部署](https://martinfowler.com/bliki/CanaryRelease.html)。

## 一. 初始状态

这里我们利用基于tcp+sni路由(listener端口为9996)的httpsbackend-sni-1的job作为演示job，该job的初始部署nomad job文件为：[httpsbackend-tcp-sni-1.nomad](https://github.com/bigwhite/experiments/blob/master/nomad-demo/part1/jobs/httpsbackend-tcp-sni-1.nomad) (注：不同的是，这里将count初始值改为了3)。

当前httpsbackend-sni-1这个job的状态如下：

```
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-08T10:57:29+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 3 0 3 0
Allocations
ID Node ID Task Group Version Desired Status Created Modified
7ac186b8 7acdd7bc httpsbackend-sni-1 22 run running 1m18s ago 1m1s ago
8a79085f c281658a httpsbackend-sni-1 22 run running 1m18s ago 46s ago
f9ffef32 9e3ef19f httpsbackend-sni-1 22 run running 1m18s ago 59s ago
0ed95591 9e3ef19f httpsbackend-sni-1 20 stop complete 5d19h ago 7m16s ago
604d2151 9e3ef19f httpsbackend-sni-1 20 stop complete 5d19h ago 7m16s ago
06404fff 7acdd7bc httpsbackend-sni-1 20 stop complete 5d20h ago 7m14s ago
```


fabio路由表如下：

![img{512x368}](../../assets/ccd01f1cb3ae87b8.png)


```
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.0
```


接下来，我们就以这个job为基础，使用各种版本升级模式对其进行更新。

## 二. 滚动更新(rolling update)

下面是blog.itaysk.com上一篇文章中的有关滚动更新的示意图：

![img{512x368}](../../assets/a9f2f45103a82c9e.png)


可以大致看出所谓**滚动更新**就是对目标环境下老版本的程序进行逐批的替换，每批的数量可以是1，也可以大于1，根据目标实例的个数自定义。替换过程中，新老版本是并存的，直到所有目标实例都被替换为新版本。

nomad支持通过在job描述文件中增加update配置来支持滚动更新。我们创建httpsbackend-tcp-sni-1-rolling-update.nomad，考虑篇幅，这里仅列出与httpsbackend-tcp-sni-1.nomad的差异：

```
# diff httpsbackend-tcp-sni-1-rolling-update.nomad ./httpsbackend-tcp-sni-1.nomad
14,19d13
< update {
< max_parallel = 1
< min_healthy_time = "30s"
< healthy_deadline = "5m"
< }
<
23c17
< image = "bigwhite/httpsbackendservice:v1.0.1"
---
> image = "bigwhite/httpsbackendservice:v1.0.0"
```


新job nomad文件使用了v1.0.1版本的httpsbackendservice image，增加了update {…}配置环节，其中的max_parallel指示的是滚动更新每批更新的数量，这里是1，也就是说一批仅用新版本替换一个老版本实例。

执行滚动更新：

```
# nomad job run httpsbackend-tcp-sni-1-rolling-update.nomad
==> Monitoring evaluation "8d39ab53"
Evaluation triggered by job "httpsbackend-sni-1"
Evaluation within deployment: "348ef16b"
Allocation "88c1a29e" created: node "7acdd7bc", group "httpsbackend-sni-1"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "8d39ab53" finished with status "complete"
```


httpsbackendservice job的task group有三个task实例，因此更新需要一些时间，我们在更新过程中查看job status：

```
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-08T13:06:35+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 3 0 4 0
Latest Deployment
ID = 348ef16b
Status = running
Description = Deployment is running
Deployed
Task Group Desired Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 3 1 0 0 2019-04-08T13:16:35+08:00
Allocations
ID Node ID Task Group Version Desired Status Created Modified
88c1a29e 7acdd7bc httpsbackend-sni-1 23 run running 44s ago 41s ago
7ac186b8 7acdd7bc httpsbackend-sni-1 22 run running 2h9m ago 2h9m ago
8a79085f c281658a httpsbackend-sni-1 22 run running 2h9m ago 2h9m ago
f9ffef32 9e3ef19f httpsbackend-sni-1 22 stop complete 2h9m ago 44s ago
```


我们看到nomad job status命令输出的信息中多出了“Latest Deployment”一个小节，在该小节中，我们看到了一个ID为348ef16b的deployment正在run。这个deployment对应的就是这次的滚动更新，我们看到下面的allocations列表中，一个version为22的allocation已经stop，一个version为23的allocation已经run，这说明nomad已经完成了一个task实例的版本升级。

我们再来查看一下job执行的最终状态：

```
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-08T13:06:35+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 3 0 6 0
Latest Deployment
ID = 348ef16b
Status = successful
Description = Deployment completed successfully
Deployed
Task Group Desired Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 3 3 3 0 2019-04-08T13:18:43+08:00
Allocations
ID Node ID Task Group Version Desired Status Created Modified
da1b545b 7acdd7bc httpsbackend-sni-1 23 run running 34s ago 2s ago
44da5693 9e3ef19f httpsbackend-sni-1 23 run running 1m25s ago 36s ago
88c1a29e 7acdd7bc httpsbackend-sni-1 23 run running 2m10s ago 1m26s ago
7ac186b8 7acdd7bc httpsbackend-sni-1 22 stop complete 2h11m ago 1m24s ago
8a79085f c281658a httpsbackend-sni-1 22 stop complete 2h11m ago 34s ago
f9ffef32 9e3ef19f httpsbackend-sni-1 22 stop complete 2h11m ago 2m10s ago
```


我们看到job执行的最终结果：ID为348ef16b的deployment执行成功；所有version 为23的allocations都处于running状态。task group的三个task实例都处于healthy状态。这说明滚动更新成功了！

我们也可以通过nomad提供的deployment子命令查看deployment的状态，deployment id作为命令参数：

```
# nomad deployment list
ID Job ID Job Version Status Description
348ef16b httpsbackend-sni-1 23 successful Deployment completed successfully
# nomad deployment status 348ef16b
ID = 348ef16b
Job ID = httpsbackend-sni-1
Job Version = 23
Status = successful
Description = Deployment completed successfully
Deployed
Task Group Desired Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 3 3 3 0 2019-04-08T13:18:43+08:00
```


滚动更新后的路由：

![img{512x368}](../../assets/ccd01f1cb3ae87b8.png)


测试一下部署成功的新版本服务：

```
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.1
```


## 三. 金丝雀部署(canary deployment)

金丝雀部署是另外一种十分有用的部署模式，下面示意图来自blog.itaysk.com：

![img{512x368}](../../assets/4ad47b6e8dcf38a2.png)


金丝雀 (Canary)得名于矿工的一个工作习惯：下矿洞前，先会放一只金丝雀进去探测是否有有毒气体，看金丝雀能否活下来。如果金丝雀活下来，则继续下矿操作；否则停止下矿。金丝雀部署亦是先部署少量新版本的服务实例，发布后，开发者可简单地通过手工测试验证新版本实例，又或通过完善的自动化测试基础设施对新版本实例进行详尽验证；甚至是直接接收部分生产流量以充分验证新版本功能、稳定性、性能等，**以给予开发者更多信心**。如果金丝雀实例通过全部测试验证，则把所有老版本全部升级为新版本。如果金丝雀测试失败，则直接回退金丝雀实例，发布失败。

nomad支持两种模式的canary部署：既支持部署canary实例去直接接收生产流量（按比例权重），也可以将其与生产实例隔离开来（利用路由）单独测试验证，下面分别说说这两种模式。

### 1. 部署canary实例去直接接收生产流量（按比例权重）

我们创建一个新的nomad job文件：httpsbackend-tcp-sni-1-canary-1.nomad

```
# diff httpsbackend-tcp-sni-1-canary-1.nomad httpsbackend-tcp-sni-1-rolling-update.nomad
18d17
< canary = 1
24c23
< image = "bigwhite/httpsbackendservice:v1.0.2"
---
> image = "bigwhite/httpsbackendservice:v1.0.1"
```


我们看到除了新版本task使用v1.0.2版image之外，最大的不同就是在update {…}配置区域增加了一行：

```
canary = 1
```


我们来plan一下该nomad文件：

```
# nomad job plan httpsbackend-tcp-sni-1-canary-1.nomad
+/- Job: "httpsbackend-sni-1"
+/- Task Group: "httpsbackend-sni-1" (1 canary, 3 ignore)
+/- Update {
AutoRevert: "false"
+/- Canary: "0" => "1"
HealthCheck: "checks"
HealthyDeadline: "300000000000"
MaxParallel: "1"
MinHealthyTime: "30000000000"
ProgressDeadline: "600000000000"
}
+/- Task: "httpsbackend-sni-1" (forces create/destroy update)
+/- Config {
+/- image: "bigwhite/httpsbackendservice:v1.0.1" => "bigwhite/httpsbackendservice:v1.0.2"
logging[0][type]: "json-file"
port_map[0][https]: "7777"
}
Scheduler dry-run:
- All tasks successfully allocated.
... ...
```


我们看到nomad分析的结果是：需要创建一个canary实例，忽略三个已经存在的旧版本task实例。同时task group的canary属性从“0”变为了“1”。

我们来run该job：

```
# nomad job run httpsbackend-tcp-sni-1-canary-1.nomad
==> Monitoring evaluation "0494a8a9"
Evaluation triggered by job "httpsbackend-sni-1"
Evaluation within deployment: "3e541fb3"
Allocation "4d678e67" created: node "c281658a", group "httpsbackend-sni-1"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "0494a8a9" finished with status "complete"
```


查看job的run状态：

```
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-08T21:04:49+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 4 0 6 0
Latest Deployment
ID = 3e541fb3
Status = running
Description = Deployment is running but requires promotion
Deployed
Task Group Promoted Desired Canaries Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 false 3 1 1 0 0 2019-04-08T21:14:49+08:00
Allocations
ID Node ID Task Group Version Desired Status Created Modified
4d678e67 c281658a httpsbackend-sni-1 24 run running 31s ago 15s ago
da1b545b 7acdd7bc httpsbackend-sni-1 23 run running 7h57m ago 7h56m ago
44da5693 9e3ef19f httpsbackend-sni-1 23 run running 7h57m ago 7h57m ago
88c1a29e 7acdd7bc httpsbackend-sni-1 23 run running 7h58m ago 7h58m ago
# nomad deployment status 3e541fb3
ID = 3e541fb3
Job ID = httpsbackend-sni-1
Job Version = 24
Status = running
Description = Deployment is running but requires promotion
Deployed
Task Group Promoted Desired Canaries Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 false 3 1 1 1 0 2019-04-08T21:15:35+08:00
```


我们看到：

-
处于running状态的allocations变成了4个，但是只有一个是version = 24的，其余都为version = 23。version = 24这个显然是我们新部署的canary实例，而另外三个则为原有的老版本实例。

-
在Deployment输出信息中，我们看到了一个描述信息：“Deployment is running but requires promotion”，意思是此次用于部署canary实例的Deployment已经running了，但是还未到最终状态，还需要promote命令。只有promote后，整个的更新工作才算是ok。


下面是canary部署后的fabio的路由：

![img{512x368}](../../assets/a5655288e3461566.png)


我们看到canary实例与其余老版本的路由规则是一致的，并平分的负载权重。也就是说新部署的canary实例与老版本实例一起承载生产流量(canary实例占25%的权重)，我们来验证一下：

```
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.2
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.1
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.1
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.1
```


我们看到第一个请求的流量就打到了我们部署的Canary实例身上了。

如果经过一段时间的验证后，证明canary实例满足要求，我们就要继续推动部署的进程使得该nomad deployment走向最终状态：即将老版本的实例都升级为新版本。

```
# nomad deployment promote 3e541fb3
==> Monitoring evaluation "b5e29b1a"
Evaluation triggered by job "httpsbackend-sni-1"
Evaluation within deployment: "3e541fb3"
Allocation "085a518e" created: node "7acdd7bc", group "httpsbackend-sni-1"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "b5e29b1a" finished with status "complete"
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-08T21:04:49+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 3 0 9 0
Latest Deployment
ID = 3e541fb3
Status = successful
Description = Deployment completed successfully
Deployed
Task Group Promoted Desired Canaries Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 true 3 1 3 3 0 2019-04-08T21:30:54+08:00
Allocations
ID Node ID Task Group Version Desired Status Created Modified
40276d89 9e3ef19f httpsbackend-sni-1 24 run running 56s ago 11s ago
085a518e 7acdd7bc httpsbackend-sni-1 24 run running 1m49s ago 58s ago
4d678e67 c281658a httpsbackend-sni-1 24 run running 16m17s ago 1m49s ago
da1b545b 7acdd7bc httpsbackend-sni-1 23 stop complete 8h12m ago 56s ago
44da5693 9e3ef19f httpsbackend-sni-1 23 stop complete 8h13m ago 1m48s ago
88c1a29e 7acdd7bc httpsbackend-sni-1 23 stop complete 8h14m ago 1m47s ago
```


通过deployment promote命令使得canary deployment进程继续推进，直到将所有老版本的实例都用canary实例替换掉。也就是我们最终看到的上面的version = 24的allocations都处于running状态，并且一共是三个实例。

我们再来测试一下升级后的服务：

```
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.2
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.2
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.2
```


我们看到：所有实例都升级到了v1.0.2版本。

### 2.将canary实例与生产实例隔离开来（利用路由）单独测试验证

如果开发者对自己的代码很有信心，不需要将canary实例暴露在生产流量中去验证，nomad也支持将canary实例与生产实例隔离开来（利用路由）单独测试验证。

我们基于httpsbackend-tcp-sni-1-canary-1.nomad改写出一个httpsbackend-tcp-sni-1-canary-2.nomad：

```
# diff httpsbackend-tcp-sni-1-canary-2.nomad httpsbackend-tcp-sni-1-canary-1.nomad
24c24
< image = "bigwhite/httpsbackendservice:v1.0.3"
---
> image = "bigwhite/httpsbackendservice:v1.0.2"
43d42
< canary_tags = ["urlprefix-canary.mysite-sni-1.com/ proto=tcp+sni"]
```


我们看到，在新的job文件中，我们除了将image版本升级为v1.0.3，我们还在service{…}配置区域增加了下面这行：

```
canary_tags = ["urlprefix-canary.mysite-sni-1.com/ proto=tcp+sni"]
```


该配置是canary实例专有的，这里我们通过在canary_tags为canary实例单独定义了路由，以免和老版本实例共享路由分担生产流量。

我们照例运行该job并查看job执行后的status：

```
# nomad job run httpsbackend-tcp-sni-1-canary-2.nomad
==> Monitoring evaluation "44e36161"
Evaluation triggered by job "httpsbackend-sni-1"
Evaluation within deployment: "e43d2551"
Allocation "73319890" created: node "7acdd7bc", group "httpsbackend-sni-1"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "44e36161" finished with status "complete"
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-08T21:35:03+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 4 0 9 0
Latest Deployment
ID = e43d2551
Status = running
Description = Deployment is running but requires promotion
Deployed
Task Group Promoted Desired Canaries Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 false 3 1 1 1 0 2019-04-08T21:45:51+08:00
Allocations
ID Node ID Task Group Version Desired Status Created Modified
73319890 7acdd7bc httpsbackend-sni-1 25 run running 2m24s ago 1m36s ago
40276d89 9e3ef19f httpsbackend-sni-1 24 run running 17m18s ago 16m33s ago
085a518e 7acdd7bc httpsbackend-sni-1 24 run running 18m11s ago 17m20s ago
4d678e67 c281658a httpsbackend-sni-1 24 run running 32m39s ago 18m11s ago
```


这个输出信息和之前的canary模式差别不大。但是从fabio路由表上我们看到如下信息：

![img{512x368}](../../assets/ac3e29c03bc0f6af.png)


fabio单独为canary实例生成了一个新路由，以区别于老版本的三个实例的路由。

开发人员单独测试canary实例时，可以通过下面方式注入流量:

```
# curl -k https://canary.mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.3
```


而生产流量依旧流入老版本的实例中：

```
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.2
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.2
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.2
```


canary实例经过测试验证后，同样可以通过promote完成对老版本的升级部署：

```
# nomad deployment promote e43d2551
==> Monitoring evaluation "34a67391"
Evaluation triggered by job "httpsbackend-sni-1"
Evaluation within deployment: "e43d2551"
Allocation "193cbc2f" created: node "c281658a", group "httpsbackend-sni-1"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "34a67391" finished with status "complete"
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-08T21:35:03+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 3 0 12 0
Latest Deployment
ID = e43d2551
Status = successful
Description = Deployment completed successfully
Deployed
Task Group Promoted Desired Canaries Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 true 3 1 3 3 0 2019-04-08T21:58:24+08:00
Allocations
ID Node ID Task Group Version Desired Status Created Modified
528a75bd 7acdd7bc httpsbackend-sni-1 25 run running 51s ago 10s ago
193cbc2f c281658a httpsbackend-sni-1 25 run running 1m39s ago 52s ago
73319890 7acdd7bc httpsbackend-sni-1 25 run running 13m31s ago 1m39s ago
40276d89 9e3ef19f httpsbackend-sni-1 24 stop complete 28m25s ago 50s ago
085a518e 7acdd7bc httpsbackend-sni-1 24 stop complete 29m18s ago 1m38s ago
4d678e67 c281658a httpsbackend-sni-1 24 stop complete 43m46s ago 1m39s ago
```


同时，canary实例在fabiolb上的路由也会自动删除掉。canary_tags在promote后将不再起作用，fabio使用的是tags。

```
# curl -k https://canary.mysite-sni-1.com:9996/
curl: (35) gnutls_handshake() failed: The TLS connection was non-properly terminated.
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.3
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.3
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.3
```


## 四. 蓝绿部署(blue-green deployment)

下面的蓝绿部署模式的示意图同样来自blog.itaysk.com：

![img{512x368}](../../assets/a8fb9f7fe12fddc6.png)


与之前的滚动更新、金丝雀部署不同的是，蓝绿部署需要“两套”环境，通过路由指向来切换流量究竟经过哪套环境。

但是在[nomad官方关于blue-green部署的例子](https://github.com/hashicorp/nomad-guides/tree/master/application-deployment/go-blue-green)中，nomad实际只维护了一套环境，并且例子中是利用nomad的canary机制来实现的蓝绿部署。这种实现方式并非严格遵循“蓝绿部署”的公认的定义。

但nomad官方对于blue-green部署的理解似乎仅限如此。我们也来看一下nomad的这种“全量金丝雀”的蓝绿方案：

我们创建httpsbackend-tcp-sni-1-blue-green.nomad文件，重点内容差异如下：

```
# diff httpsbackend-tcp-sni-1-blue-green.nomad httpsbackend-tcp-sni-1-canary-1.nomad
18c18
< canary = 3
---
> canary = 1
24c24
< image = "bigwhite/httpsbackendservice:v1.0.4"
---
> image = "bigwhite/httpsbackendservice:v1.0.2"
```


我们看到这里canary = 3，与count值相同，这也是将其称为“全量金丝雀”的原因。

使用该文件部署新版本实例：

```
# nomad job run httpsbackend-tcp-sni-1-blue-green.nomad
==> Monitoring evaluation "7a5074f3"
Evaluation triggered by job "httpsbackend-sni-1"
Evaluation within deployment: "3c8740f2"
Allocation "338ee344" created: node "c281658a", group "httpsbackend-sni-1"
Allocation "3dec73d2" created: node "9e3ef19f", group "httpsbackend-sni-1"
Allocation "e6975673" created: node "9e3ef19f", group "httpsbackend-sni-1"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "7a5074f3" finished with status "complete"
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-09T13:38:49+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 6 0 12 0
Latest Deployment
ID = 3c8740f2
Status = running
Description = Deployment is running but requires promotion
Deployed
Task Group Promoted Desired Canaries Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 false 3 3 3 3 0 2019-04-09T13:49:41+08:00
Allocations
ID Node ID Task Group Version Desired Status Created Modified
338ee344 c281658a httpsbackend-sni-1 26 run running 57s ago 5s ago
3dec73d2 9e3ef19f httpsbackend-sni-1 26 run running 57s ago 11s ago
e6975673 9e3ef19f httpsbackend-sni-1 26 run running 57s ago 10s ago
528a75bd 7acdd7bc httpsbackend-sni-1 25 run running 15h52m ago 15h51m ago
193cbc2f c281658a httpsbackend-sni-1 25 run running 15h52m ago 15h52m ago
73319890 7acdd7bc httpsbackend-sni-1 25 run running 16h4m ago 15h52m ago
```


部署ok后，6个实例共同接收生产流量。当然我们也可以通过canary_tags为新的部署设定不同路由，选择哪一种要看部署新实例后打算对新实例如何进行测试。

测试验证ok后，像canary deployment一样，通过promote命令用新版本替换老版本。

```
# nomad deployment promote 3c8740f2
==> Monitoring evaluation "fad3a69b"
Evaluation triggered by job "httpsbackend-sni-1"
Evaluation within deployment: "3c8740f2"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "fad3a69b" finished with status "complete"
# nomad job status httpsbackend-sni-1
ID = httpsbackend-sni-1
Name = httpsbackend-sni-1
Submit Date = 2019-04-09T13:38:49+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpsbackend-sni-1 0 0 3 0 15 0
Latest Deployment
ID = 3c8740f2
Status = successful
Description = Deployment completed successfully
Deployed
Task Group Promoted Desired Canaries Placed Healthy Unhealthy Progress Deadline
httpsbackend-sni-1 true 3 3 3 3 0 2019-04-09T13:49:41+08:00
Allocations
ID Node ID Task Group Version Desired Status Created Modified
338ee344 c281658a httpsbackend-sni-1 26 run running 4m43s ago 15s ago
3dec73d2 9e3ef19f httpsbackend-sni-1 26 run running 4m43s ago 15s ago
e6975673 9e3ef19f httpsbackend-sni-1 26 run running 4m43s ago 15s ago
528a75bd 7acdd7bc httpsbackend-sni-1 25 stop complete 15h55m ago 14s ago
193cbc2f c281658a httpsbackend-sni-1 25 stop complete 15h56m ago 15s ago
73319890 7acdd7bc httpsbackend-sni-1 25 stop complete 16h8m ago 14s ago
```


测试结果：

```
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.4
```


如果要快速切换回原来的版本，可以使用：

```
nomad job revert httpsbackend-sni-1 {old_allocation_version}
```


## 五. 其他

本文涉及到的nomad job文件源码可在[这里](https://github.com/bigwhite/experiments/tree/master/nomad-demo/part2)下载。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

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

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论