---
title: 使用Fluentd和ElasticSearch Stack实现Kubernetes的集群Logging
url: https://tonybai.com/2017/03/03/implement-kubernetes-cluster-level-logging-with-fluentd-and-elasticsearch-stack/
published: '2017-03-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Fluentd和ElasticSearch Stack实现Kubernetes的集群Logging

在本篇文章中，我们继续来说[Kubernetes](http://tonybai.com/tag/kubernetes)。

经过一段时间的探索，我们先后完成了[Kubernetes集群搭建](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)，[DNS](http://tonybai.com/2016/10/23/install-dns-addon-for-k8s/)、[Dashboard](http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/)、[Heapster](http://tonybai.com/2017/01/20/integrate-heapster-for-kubernetes-dashboard/)等插件安装，[集群安全配置](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)，搭建[作为Persistent Volume的CephRBD](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)，以及[服务更新](http://tonybai.com/2017/02/09/rolling-update-for-services-in-kubernetes-cluster)等[探索](http://tonybai.com/2017/01/24/explore-kubernetes-cluster-installed-by-kubeadm)和实现工作。现在Kubernetes[集群层面的Logging](https://kubernetes.io/docs/user-guide/logging/overview/)需求逐渐浮上水面了。

随着一些小应用在我们的Kubernetes集群上的部署上线，集群的运行迈上了正轨。但问题随之而来，那就是如何查找和诊断集群自身的问题以及运行于Pod中应用的问题。日志，没错！我们也只能依赖Kubernetes组件以及Pod中应用输出的日志。不过目前我们仅能通过kubectl logs命令或[Kubernetes Dashboard](http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/)来查看Log。在没有cluster level logging的情况下，我们需要分别查看各个Pod的日志，操作繁琐，过程低效。我们迫切地需要为Kubernetes集群搭建一套集群级别的集中日志收集和分析设施。

对于任何基础设施或后端服务系统，日志都是极其重要的。对于受Google内部容器管理系统Borg启发而催生出的Kubernetes项目来说，自然少不了对Logging的支持。在“[Logging Overview](https://kubernetes.io/docs/user-guide/logging/overview/)“中，官方概要介绍了Kubernetes上的几个层次的Logging方案，并给出Cluster-level logging的参考架构：

![img{512x368}](../../assets/3c397dc8082591d8.png)


Kubernetes还给出了参考实现：

– Logging Backend：[Elastic Search](https://www.elastic.co/) stack(包括：[Kibana](https://www.elastic.co/products/kibana))

– Logging-agent：[fluentd](http://www.fluentd.org/)

ElasticSearch stack实现的cluster level logging的一个优势在于其对Kubernetes集群中的Pod没有侵入性，Pod无需做任何配合性改动。同时EFK/ELK方案在业内也是相对成熟稳定的。

在本文中，我将为我们的Kubernetes 1.3.7集群安装ElasticSearch、Fluentd和Kibana。由于1.3.7版本略有些old，EFK能否在其上面run起来，我也是心中未知。能否像《[生化危机：终章](https://movie.douban.com/subject/20471852/)》那样有一个完美的结局，我们还需要一步一步“打怪升级”慢慢看。

### 一、Kubernetes 1.3.7集群的 “漏网之鱼”

Kubernetes 1.3.7集群是通过kube-up.sh搭建并初始化的。按照[K8s官方文档](https://kubernetes.io/docs/user-guide/logging/elasticsearch/)有关elasticsearch logging的介绍，在kubernetes/cluster/ubuntu/config-default.sh中，我也发现了下面几个配置项：

```
// kubernetes/cluster/ubuntu/config-default.sh
# Optional: Enable node logging.
ENABLE_NODE_LOGGING=false
LOGGING_DESTINATION=${LOGGING_DESTINATION:-elasticsearch}
# Optional: When set to true, Elasticsearch and Kibana will be setup as part of the cluster bring up.
ENABLE_CLUSTER_LOGGING=false
ELASTICSEARCH_LOGGING_REPLICAS=${ELASTICSEARCH_LOGGING_REPLICAS:-1}
```


显然，当初如果搭建集群伊始时要是知道这些配置的意义，可能那个时候就会将elastic logging集成到集群中了。现在为时已晚，集群上已经跑了很多应用，无法重新通过kube-up.sh中断集群运行并安装elastic logging了。我只能手工进行安装了！

### 二、镜像准备

1.3.7源码中kubernetes/cluster/addons/fluentd-elasticsearch下的manifest已经比较old了，我们直接使用kubernetes最新源码中的[manifest文件](https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/fluentd-elasticsearch)：

```
k8s.io/kubernetes/cluster/addons/fluentd-elasticsearch$ ls *.yaml
es-controller.yaml es-service.yaml fluentd-es-ds.yaml kibana-controller.yaml kibana-service.yaml
```


分析这些yaml，我们需要三个镜像：

```
gcr.io/google_containers/fluentd-elasticsearch:1.22
gcr.io/google_containers/elasticsearch:v2.4.1-1
gcr.io/google_containers/kibana:v4.6.1-1
```


显然镜像都在墙外。由于生产环境下的Docker引擎并没有配置加速器代理，因此我们需要手工下载一下这三个镜像。我采用的方法是通过另外一台配置了加速器的机器上的[Docker引擎](http://tonybai.com/tag/docker)将三个image下载，并重新打tag，上传到我在hub.docker.com上的账号下，以elasticsearch:v2.4.1-1为例：

```
# docker pull gcr.io/google_containers/elasticsearch:v2.4.1-1
# docker tag gcr.io/google_containers/elasticsearch:v2.4.1-1 bigwhite/elasticsearch:v2.4.1-1
# docker push bigwhite/elasticsearch:v2.4.1-1
```


下面是我们在后续安装过程中真正要使用到的镜像：

```
bigwhite/fluentd-elasticsearch:1.22
bigwhite/elasticsearch:v2.4.1-1
bigwhite/kibana:v4.6.1-1
```


### 三、启动fluentd

fluentd是以[DaemonSet](https://kubernetes.io/docs/admin/daemons/)的形式跑在K8s集群上的，这样k8s可以保证每个k8s cluster node上都会启动一个fluentd(注意：将image改为上述镜像地址，如果你配置了加速器，那自然就不必了)。

```
# kubectl create -f fluentd-es-ds.yaml --record
daemonset "fluentd-es-v1.22" created
```


查看daemonset中的Pod的启动情况，我们发现：

```
kube-system fluentd-es-v1.22-as3s5 0/1 CrashLoopBackOff 2 43s 172.16.99.6 10.47.136.60
kube-system fluentd-es-v1.22-qz193 0/1 CrashLoopBackOff 2 43s 172.16.57.7 10.46.181.146
```


fluentd Pod启动失败，fluentd的日志可以通过/var/log/fluentd.log查看：

```
# tail -100f /var/log/fluentd.log
2017-03-02 02:27:01 +0000 [info]: reading config file path="/etc/td-agent/td-agent.conf"
2017-03-02 02:27:01 +0000 [info]: starting fluentd-0.12.31
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-mixin-config-placeholders' version '0.4.0'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-mixin-plaintextformatter' version '0.2.6'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-docker_metadata_filter' version '0.1.3'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-elasticsearch' version '1.5.0'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-kafka' version '0.4.1'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-kubernetes_metadata_filter' version '0.24.0'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-mongo' version '0.7.16'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-rewrite-tag-filter' version '1.5.5'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-s3' version '0.8.0'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-scribe' version '0.10.14'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-td' version '0.10.29'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-td-monitoring' version '0.2.2'
2017-03-02 02:27:01 +0000 [info]: gem 'fluent-plugin-webhdfs' version '0.4.2'
2017-03-02 02:27:01 +0000 [info]: gem 'fluentd' version '0.12.31'
2017-03-02 02:27:01 +0000 [info]: adding match pattern="fluent.**" type="null"
2017-03-02 02:27:01 +0000 [info]: adding filter pattern="kubernetes.**" type="kubernetes_metadata"
2017-03-02 02:27:02 +0000 [error]: config error file="/etc/td-agent/td-agent.conf" error="Invalid Kubernetes API v1 endpoint https://192.168.3.1:443/api: 401 Unauthorized"
2017-03-02 02:27:02 +0000 [info]: process finished code=256
2017-03-02 02:27:02 +0000 [warn]: process died within 1 second. exit.
```


从上述日志中的error来看：fluentd访问apiserver secure port(443)出错了：Unauthorized! 通过分析 cluster/addons/fluentd-elasticsearch/fluentd-es-image/build.sh和td-agent.conf，我们发现是fluentd image中的[fluent-plugin-kubernetes_metadata_filter](https://github.com/fabric8io/fluent-plugin-kubernetes_metadata_filter)要去访问API Server以获取一些kubernetes的metadata信息。不过未做任何特殊配置的fluent-plugin-kubernetes_metadata_filter，我猜测它使用的是kubernetes为Pod传入的环境变量：KUBERNETES_SERVICE_HOST和KUBERNETES_SERVICE_PORT来得到API Server的访问信息的。但API Server在secure port上是开启了[安全身份验证机制](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)的，fluentd直接访问必然是失败的。

我们找到了fluent-plugin-kubernetes_metadata_filter项目在github.com上的[主页](https://github.com/fabric8io/fluent-plugin-kubernetes_metadata_filter)，在这个页面上我们看到了fluent-plugin-kubernetes_metadata_filter支持的其他配置，包括：ca_file、client_cert、client_key等，显然这些字眼非常眼熟。我们需要修改一下fluentd image中td-agent.conf的配置，为fluent-plugin-kubernetes_metadata_filter增加一些配置项，比如：

```
// td-agent.conf
... ...
<filter kubernetes.**>
type kubernetes_metadata
ca_file /srv/kubernetes/ca.crt
client_cert /srv/kubernetes/kubecfg.crt
client_key /srv/kubernetes/kubecfg.key
</filter>
... ...
```


这里我不想重新制作image，那么怎么办呢？Kubernetes提供了[ConfigMap](https://kubernetes.io/docs/user-guide/configmap/)这一强大的武器，我们可以将新版td-agent.conf制作成kubernetes的configmap资源，并挂载到fluentd pod的相应位置以替换image中默认的td-agent.conf。

需要注意两点：

* 在基于td-agent.conf创建configmap资源之前，需要将td-agent.conf中的注释行都删掉，否则生成的configmap的内容可能不正确；

* fluentd pod将创建在kube-system下，因此configmap资源也需要创建在kube-system namespace下面，否则kubectl create无法找到对应的configmap。

```
# kubectl create configmap td-agent-config --from-file=./td-agent.conf -n kube-system
configmap "td-agent-config" created
# kubectl get configmaps -n kube-system
NAME DATA AGE
td-agent-config 1 9s
# kubectl get configmaps td-agent-config -o yaml
apiVersion: v1
data:
td-agent.conf: |
<match fluent.**>
type null
</match>
<source>
type tail
path /var/log/containers/*.log
pos_file /var/log/es-containers.log.pos
time_format %Y-%m-%dT%H:%M:%S.%NZ
tag kubernetes.*
format json
read_from_head true
</source>
... ...
```


fluentd-es-ds.yaml也要随之做一些改动，主要是增加两个mount: 一个是mount 上面的configmap td-agent-config，另外一个就是mount hostpath：/srv/kubernetes以获取到相关client端的数字证书：

```
spec:
containers:
- name: fluentd-es
image: bigwhite/fluentd-elasticsearch:1.22
command:
- '/bin/sh'
- '-c'
- '/usr/sbin/td-agent 2>&1 >> /var/log/fluentd.log'
resources:
limits:
memory: 200Mi
#requests:
#cpu: 100m
#memory: 200Mi
volumeMounts:
- name: varlog
mountPath: /var/log
- name: varlibdockercontainers
mountPath: /var/lib/docker/containers
readOnly: true
- name: td-agent-config
mountPath: /etc/td-agent
- name: tls-files
mountPath: /srv/kubernetes
terminationGracePeriodSeconds: 30
volumes:
- name: varlog
hostPath:
path: /var/log
- name: varlibdockercontainers
hostPath:
path: /var/lib/docker/containers
- name: td-agent-config
configMap:
name: td-agent-config
- name: tls-files
hostPath:
path: /srv/kubernetes
```


接下来，我们重新创建fluentd ds，步骤不赘述。这回我们的创建成功了：

```
kube-system fluentd-es-v1.22-adsrx 1/1 Running 0 1s 172.16.99.6 10.47.136.60
kube-system fluentd-es-v1.22-rpme3 1/1 Running 0 1s 172.16.57.7 10.46.181.146
```


但通过查看/var/log/fluentd.log，我们依然能看到“问题”：

```
2017-03-02 03:57:58 +0000 [warn]: temporarily failed to flush the buffer. next_retry=2017-03-02 03:57:59 +0000 error_class="Fluent::ElasticsearchOutput::ConnectionFailure" error="Can not reach Elasticsearch cluster ({:host=>\"elasticsearch-logging\", :port=>9200, :scheme=>\"http\"})!" plugin_id="object:3fd99fa857d8"
2017-03-02 03:57:58 +0000 [warn]: suppressed same stacktrace
2017-03-02 03:58:00 +0000 [warn]: temporarily failed to flush the buffer. next_retry=2017-03-02 03:58:03 +0000 error_class="Fluent::ElasticsearchOutput::ConnectionFailure" error="Can not reach Elasticsearch cluster ({:host=>\"elasticsearch-logging\", :port=>9200, :scheme=>\"http\"})!" plugin_id="object:3fd99fa857d8"
2017-03-02 03:58:00 +0000 [info]: process finished code=9
2017-03-02 03:58:00 +0000 [error]: fluentd main process died unexpectedly. restarting.
```


由于ElasticSearch logging还未创建，这是连不上elasticsearch所致。

### 四、启动elasticsearch

启动elasticsearch：

```
# kubectl create -f es-controller.yaml
replicationcontroller "elasticsearch-logging-v1" created
# kubectl create -f es-service.yaml
service "elasticsearch-logging" created
get pods：
kube-system elasticsearch-logging-v1-3bzt6 1/1 Running 0 7s 172.16.57.8 10.46.181.146
kube-system elasticsearch-logging-v1-nvbe1 1/1 Running 0 7s 172.16.99.10 10.47.136.60
```


elastic search logging启动成功后，上述fluentd的fail日志就没有了！

不过elastic search真的运行ok了么？我们查看一下elasticsearch相关Pod日志：

```
# kubectl logs -f elasticsearch-logging-v1-3bzt6 -n kube-system
F0302 03:59:41.036697 8 elasticsearch_logging_discovery.go:60] kube-system namespace doesn't exist: the server has asked for the client to provide credentials (get namespaces kube-system)
goroutine 1 [running]:
k8s.io/kubernetes/vendor/github.com/golang/glog.stacks(0x19a8100, 0xc400000000, 0xc2, 0x186)
... ...
main.main()
elasticsearch_logging_discovery.go:60 +0xb53
[2017-03-02 03:59:42,587][INFO ][node ] [elasticsearch-logging-v1-3bzt6] version[2.4.1], pid[16], build[c67dc32/2016-09-27T18:57:55Z]
[2017-03-02 03:59:42,588][INFO ][node ] [elasticsearch-logging-v1-3bzt6] initializing ...
[2017-03-02 03:59:44,396][INFO ][plugins ] [elasticsearch-logging-v1-3bzt6] modules [reindex, lang-expression, lang-groovy], plugins [], sites []
... ...
[2017-03-02 03:59:44,441][INFO ][env ] [elasticsearch-logging-v1-3bzt6] heap size [1007.3mb], compressed ordinary object pointers [true]
[2017-03-02 03:59:48,355][INFO ][node ] [elasticsearch-logging-v1-3bzt6] initialized
[2017-03-02 03:59:48,355][INFO ][node ] [elasticsearch-logging-v1-3bzt6] starting ...
[2017-03-02 03:59:48,507][INFO ][transport ] [elasticsearch-logging-v1-3bzt6] publish_address {172.16.57.8:9300}, bound_addresses {[::]:9300}
[2017-03-02 03:59:48,547][INFO ][discovery ] [elasticsearch-logging-v1-3bzt6] kubernetes-logging/7_f_M2TKRZWOw4NhBc4EqA
[2017-03-02 04:00:18,552][WARN ][discovery ] [elasticsearch-logging-v1-3bzt6] waited for 30s and no initial state was set by the discovery
[2017-03-02 04:00:18,562][INFO ][http ] [elasticsearch-logging-v1-3bzt6] publish_address {172.16.57.8:9200}, bound_addresses {[::]:9200}
[2017-03-02 04:00:18,562][INFO ][node ] [elasticsearch-logging-v1-3bzt6] started
[2017-03-02 04:01:15,754][WARN ][discovery.zen.ping.unicast] [elasticsearch-logging-v1-3bzt6] failed to send ping to [{#zen_unicast_1#}{127.0.0.1}{127.0.0.1:9300}]
SendRequestTransportException[[][127.0.0.1:9300][internal:discovery/zen/unicast]]; nested: NodeNotConnectedException[[][127.0.0.1:9300] Node not connected];
... ...
Caused by: NodeNotConnectedException[[][127.0.0.1:9300] Node not connected]
at org.elasticsearch.transport.netty.NettyTransport.nodeChannel(NettyTransport.java:1141)
at org.elasticsearch.transport.netty.NettyTransport.sendRequest(NettyTransport.java:830)
at org.elasticsearch.transport.TransportService.sendRequest(TransportService.java:329)
... 12 more
```


总结了一下，日志中有两个错误：

- 无法访问到API Server，这个似乎和fluentd最初的问题一样；

- elasticsearch两个节点间互ping失败。

要想找到这两个问题的原因，还得回到源头，去分析elastic search image的组成。

通过cluster/addons/fluentd-elasticsearch/es-image/run.sh文件内容：

```
/elasticsearch_logging_discovery >> /elasticsearch/config/elasticsearch.yml
chown -R elasticsearch:elasticsearch /data
/bin/su -c /elasticsearch/bin/elasticsearch elasticsearch
```


我们了解到image中，其实包含了两个程序，一个为/elasticsearch_logging_discovery，该程序执行后生成一个配置文件： /elasticsearch/config/elasticsearch.yml。该配置文件后续被另外一个程序：/elasticsearch/bin/elasticsearch使用。

我们查看一下已经运行的docker中的elasticsearch.yml文件内容：

```
# docker exec 3cad31f6eb08 cat /elasticsearch/config/elasticsearch.yml
cluster.name: kubernetes-logging
node.name: ${NODE_NAME}
node.master: ${NODE_MASTER}
node.data: ${NODE_DATA}
transport.tcp.port: ${TRANSPORT_PORT}
http.port: ${HTTP_PORT}
path.data: /data
network.host: 0.0.0.0
discovery.zen.minimum_master_nodes: ${MINIMUM_MASTER_NODES}
discovery.zen.ping.multicast.enabled: false
```


这个结果中缺少了一项：

```
discovery.zen.ping.unicast.hosts: ["172.30.0.11", "172.30.192.15"]
```


这也是导致第二个问题的原因。综上，elasticsearch logging的错误其实都是由于/elasticsearch_logging_discovery无法访问API Server导致 /elasticsearch/config/elasticsearch.yml没有被正确生成造成的，我们就来解决这个问题。

我查看了一下/elasticsearch_logging_discovery的[源码](https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/fluentd-elasticsearch/es-image/elasticsearch_logging_discovery.go)，elasticsearch_logging_discovery是一个典型通过[client-go](https://github.com/kubernetes/client-go)通过service account访问API Server的程序，很显然这就是我在《[在Kubernetes Pod中使用Service Account访问API Server](http://tonybai.com/2017/03/03/access-api-server-from-a-pod-through-serviceaccount)》一文中提到的那个问题：默认的service account不好用。

解决方法：在kube-system namespace下创建一个新的service account资源，并在es-controller.yaml中显式使用该新创建的service account。

创建一个新的serviceaccount在kube-system namespace下：

```
//serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
name: k8s-efk
# kubectl create -f serviceaccount.yaml -n kube-system
serviceaccount "k8s-efk" created
# kubectl get serviceaccount -n kube-system
NAME SECRETS AGE
default 1 139d
k8s-efk 1 17s
```


在es-controller.yaml中，使用service account “k8s-efk”：

```
//es-controller.yaml
... ...
spec:
replicas: 2
selector:
k8s-app: elasticsearch-logging
version: v1
template:
metadata:
labels:
k8s-app: elasticsearch-logging
version: v1
kubernetes.io/cluster-service: "true"
spec:
serviceAccount: k8s-efk
containers:
... ...
```


重新创建elasticsearch logging service后，我们再来查看elasticsearch-logging pod的日志：

```
# kubectl logs -f elasticsearch-logging-v1-dklui -n kube-system
[2017-03-02 08:26:46,500][INFO ][node ] [elasticsearch-logging-v1-dklui] version[2.4.1], pid[14], build[c67dc32/2016-09-27T18:57:55Z]
[2017-03-02 08:26:46,504][INFO ][node ] [elasticsearch-logging-v1-dklui] initializing ...
[2017-03-02 08:26:47,984][INFO ][plugins ] [elasticsearch-logging-v1-dklui] modules [reindex, lang-expression, lang-groovy], plugins [], sites []
[2017-03-02 08:26:48,073][INFO ][env ] [elasticsearch-logging-v1-dklui] using [1] data paths, mounts [[/data (/dev/vda1)]], net usable_space [16.9gb], net total_space [39.2gb], spins? [possibly], types [ext4]
[2017-03-02 08:26:48,073][INFO ][env ] [elasticsearch-logging-v1-dklui] heap size [1007.3mb], compressed ordinary object pointers [true]
[2017-03-02 08:26:53,241][INFO ][node ] [elasticsearch-logging-v1-dklui] initialized
[2017-03-02 08:26:53,241][INFO ][node ] [elasticsearch-logging-v1-dklui] starting ...
[2017-03-02 08:26:53,593][INFO ][transport ] [elasticsearch-logging-v1-dklui] publish_address {172.16.57.8:9300}, bound_addresses {[::]:9300}
[2017-03-02 08:26:53,651][INFO ][discovery ] [elasticsearch-logging-v1-dklui] kubernetes-logging/Ky_OuYqMRkm_918aHRtuLg
[2017-03-02 08:26:56,736][INFO ][cluster.service ] [elasticsearch-logging-v1-dklui] new_master {elasticsearch-logging-v1-dklui}{Ky_OuYqMRkm_918aHRtuLg}{172.16.57.8}{172.16.57.8:9300}{master=true}, added {{elasticsearch-logging-v1-vjxm3}{cbzgrfZATyWkHfQYHZhs7Q}{172.16.99.10}{172.16.99.10:9300}{master=true},}, reason: zen-disco-join(elected_as_master, [1] joins received)
[2017-03-02 08:26:56,955][INFO ][http ] [elasticsearch-logging-v1-dklui] publish_address {172.16.57.8:9200}, bound_addresses {[::]:9200}
[2017-03-02 08:26:56,956][INFO ][node ] [elasticsearch-logging-v1-dklui] started
[2017-03-02 08:26:57,157][INFO ][gateway ] [elasticsearch-logging-v1-dklui] recovered [0] indices into cluster_state
[2017-03-02 08:27:05,378][INFO ][cluster.metadata ] [elasticsearch-logging-v1-dklui] [logstash-2017.03.02] creating index, cause [auto(bulk api)], templates [], shards [5]/[1], mappings []
[2017-03-02 08:27:06,360][INFO ][cluster.metadata ] [elasticsearch-logging-v1-dklui] [logstash-2017.03.01] creating index, cause [auto(bulk api)], templates [], shards [5]/[1], mappings []
[2017-03-02 08:27:07,163][INFO ][cluster.routing.allocation] [elasticsearch-logging-v1-dklui] Cluster health status changed from [RED] to [YELLOW] (reason: [shards started [[logstash-2017.03.01][3], [logstash-2017.03.01][3]] ...]).
[2017-03-02 08:27:07,354][INFO ][cluster.metadata ] [elasticsearch-logging-v1-dklui] [logstash-2017.03.02] create_mapping [fluentd]
[2017-03-02 08:27:07,988][INFO ][cluster.metadata ] [elasticsearch-logging-v1-dklui] [logstash-2017.03.01] create_mapping [fluentd]
[2017-03-02 08:27:09,578][INFO ][cluster.routing.allocation] [elasticsearch-logging-v1-dklui] Cluster health status changed from [YELLOW] to [GREEN] (reason: [shards started [[logstash-2017.03.02][4]] ...]).
```


elasticsearch logging启动运行ok！

### 五、启动kibana

有了elasticsearch logging的“前车之鉴”，这次我们也把上面新创建的serviceaccount：k8s-efk显式赋值给kibana-controller.yaml:

```
//kibana-controller.yaml
... ...
spec:
serviceAccount: k8s-efk
containers:
- name: kibana-logging
image: bigwhite/kibana:v4.6.1-1
resources:
# keep request = limit to keep this container in guaranteed class
limits:
cpu: 100m
#requests:
# cpu: 100m
env:
- name: "ELASTICSEARCH_URL"
value: "http://elasticsearch-logging:9200"
- name: "KIBANA_BASE_URL"
value: "/api/v1/proxy/namespaces/kube-system/services/kibana-logging"
ports:
- containerPort: 5601
name: ui
protocol: TCP
... ...
```


启动kibana，并观察pod日志：

```
# kubectl create -f kibana-controller.yaml
# kubectl create -f kibana-service.yaml
# kubectl logs -f kibana-logging-3604961973-jby53 -n kube-system
ELASTICSEARCH_URL=http://elasticsearch-logging:9200
server.basePath: /api/v1/proxy/namespaces/kube-system/services/kibana-logging
{"type":"log","@timestamp":"2017-03-02T08:30:15Z","tags":["info","optimize"],"pid":6,"message":"Optimizing and caching bundles for kibana and statusPage. This may take a few minutes"}
```


kibana缓存着实需要一段时间，请耐心等待！可能是几分钟。之后你将会看到如下日志：

```
# kubectl logs -f kibana-logging-3604961973-jby53 -n kube-system
ELASTICSEARCH_URL=http://elasticsearch-logging:9200
server.basePath: /api/v1/proxy/namespaces/kube-system/services/kibana-logging
{"type":"log","@timestamp":"2017-03-02T08:30:15Z","tags":["info","optimize"],"pid":6,"message":"Optimizing and caching bundles for kibana and statusPage. This may take a few minutes"}
{"type":"log","@timestamp":"2017-03-02T08:40:04Z","tags":["info","optimize"],"pid":6,"message":"Optimization of bundles for kibana and statusPage complete in 588.60 seconds"}
{"type":"log","@timestamp":"2017-03-02T08:40:04Z","tags":["status","plugin:kibana@1.0.0","info"],"pid":6,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2017-03-02T08:40:05Z","tags":["status","plugin:elasticsearch@1.0.0","info"],"pid":6,"state":"yellow","message":"Status changed from uninitialized to yellow - Waiting for Elasticsearch","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2017-03-02T08:40:05Z","tags":["status","plugin:kbn_vislib_vis_types@1.0.0","info"],"pid":6,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2017-03-02T08:40:05Z","tags":["status","plugin:markdown_vis@1.0.0","info"],"pid":6,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2017-03-02T08:40:05Z","tags":["status","plugin:metric_vis@1.0.0","info"],"pid":6,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2017-03-02T08:40:06Z","tags":["status","plugin:spyModes@1.0.0","info"],"pid":6,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2017-03-02T08:40:06Z","tags":["status","plugin:statusPage@1.0.0","info"],"pid":6,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2017-03-02T08:40:06Z","tags":["status","plugin:table_vis@1.0.0","info"],"pid":6,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2017-03-02T08:40:06Z","tags":["listening","info"],"pid":6,"message":"Server running at http://0.0.0.0:5601"}
{"type":"log","@timestamp":"2017-03-02T08:40:11Z","tags":["status","plugin:elasticsearch@1.0.0","info"],"pid":6,"state":"yellow","message":"Status changed from yellow to yellow - No existing Kibana index found","prevState":"yellow","prevMsg":"Waiting for Elasticsearch"}
{"type":"log","@timestamp":"2017-03-02T08:40:14Z","tags":["status","plugin:elasticsearch@1.0.0","info"],"pid":6,"state":"green","message":"Status changed from yellow to green - Kibana index ready","prevState":"yellow","prevMsg":"No existing Kibana index found"}
```


接下来，通过浏览器访问下面地址就可以访问kibana的web页面了，注意：Kinaba的web页面加载也需要一段时间。

```
https://{API Server external IP}:{API Server secure port}/api/v1/proxy/namespaces/kube-system/services/kibana-logging/app/kibana#/settings/indices/
```


下面是创建一个index（相当于mysql中的一个database）页面：

![img{512x368}](../../assets/38c4f9c13f7bd0c7.png)


取消“Index contains time-based events”，然后点击“Create”即可创建一个Index。

点击页面上的”Setting” -> “Status”，可以查看当前elasticsearch logging的整体状态，如果一切ok，你将会看到下图这样的页面：

![img{512x368}](../../assets/cba455807b16e616.png)


创建Index后，可以在Discover下看到ElasticSearch logging中汇聚的日志：

![img{512x368}](../../assets/fe5da3613b49846c.png)


### 六、小结

以上就是在Kubernetes 1.3.7集群上安装Fluentd和ElasticSearch stack，实现kubernetes cluster level logging的过程。在[使用kubeadm安装的Kubernetes 1.5.1环境](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm)下安装这些，则基本不会遇到上述这些问题。

另外ElasticSearch logging默认挂载的volume是emptyDir，实验用可以。但要部署在生产环境，必须换成Persistent Volume，比如：[CephRBD](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd)。

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我是在1.5.3上跑的EFK，现在能获取到ES的信息，但是访问KIBANA报错http://172.16.100.215:32619/api/v1/proxy/namespaces/kube-system/services/kibana-logging/app/kibana{“statusCode”:404,”error”:”Not Found”}# kubectl logs kibana-logging-1918083406-j1z97 –namespace=kube-systemserver.basePath: /api/v1/proxy/namespaces/kube-system/services/kibana-logging{“type”:”log”,”@timestamp”:”2017-02-26T05:02:41Z”,”tags”:["info","optimize"],”pid”:7,”message”:”Optimizing and caching bundles for kibana and statusPage. This may take a few minutes”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:46Z”,”tags”:["info","optimize"],”pid”:7,”message”:”Optimization of bundles for kibana and statusPage complete in 425.30 seconds”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:46Z”,”tags”:["status","plugin:kibana@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:elasticsearch@1.0.0","info"],”pid”:7,”state”:”yellow”,”message”:”Status changed from uninitialized to yellow – Waiting for Elasticsearch”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:kbn_vislib_vis_types@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:markdown_vis@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:metric_vis@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:spyModes@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:statusPage@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:table_vis@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["listening","info"],”pid”:7,”message”:”Server running at http://0.0.0.0:5601“}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:52Z”,”tags”:["status","plugin:elasticsearch@1.0.0","info"],”pid”:7,”state”:”yellow”,”message”:”Status changed from yellow to yellow – No existing Kibana index found”,”prevState”:”yellow”,”prevMsg”:”Waiting for Elasticsearch”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:56Z”,”tags”:["status","plugin:elasticsearch@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from yellow to green – Kibana index ready”,”prevState”:”yellow”,”prevMsg”:”No existing Kibana index found”}{“type”:”response”,”@timestamp”:”2017-02-27T05:51:19Z”,”tags”:[],”pid”:7,”method”:”head”,”statusCode”:200,”req”:{“url”:”/”,”method”:”head”,”headers”:{“host”:”10.46.0.6:5601″,”user-agent”:”curl/7.29.0″,”accept”:”*/*”,”x-forwarded-for”:”127.0.0.1″,”x-forwarded-uri”:”/api/v1/proxy/namespaces/kube-system/services/kibana-logging/”},”remoteAddress”:”10.40.0.0″,”userAgent”:”10.40.0.0″},”res”:{“statusCode”:200,”responseTime”:35,”contentLength”:9},”message”:”HEAD / 200 35ms – 9.0B”}{“type”:”log”,”@timestamp”:”2017-02-28T18:39:38Z”,”tags”:["status","plugin:elasticsearch@1.0.0","error"],”pid”:7,”state”:”red”,”message”:”Status changed from green to red – Request Timeout after 3000ms”,”prevState”:”green”,”prevMsg”:”Kibana index ready”}{“type”:”response”,”@timestamp”:”2017-03-06T07:20:44Z”,”tags”:[],”pid”:7,”method”:”get”,”statusCode”:404,”req”:{“url”:”/api/v1/proxy/namespaces/kube-system/services/kibana-logging/app/kibana”,”method”:”get”,”headers”:{“host”:”172.16.100.215:32619″,”connection”:”keep-alive”,”cache-control”:”max-age=0″,”upgrade-insecure-requests”:”1″,”user-agent”:”Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36″,”accept”:”text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8″,”referer”:”http://172.16.100.215:32619/“,”accept-encoding”:”gzip, deflate, sdch”,”accept-language”:”zh-CN,zh;q=0.8″},”remoteAddress”:”10.40.0.0″,”userAgent”:”10.40.0.0″,”referer”:”http://172.16.100.215:32619/“},”res”:{“statusCode”:404,”responseTime”:3,”contentLength”:9},”message”:”GET /api/v1/proxy/namespaces/kube-system/services/kibana-logging/app/kibana 404 3ms – 9.0B”}# kubectl logs fluentd-es-v1.22-ccpkd –namespace=kube-system /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:3: warning: already initialized constant JSON::VERSION/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:3: warning: previous definition of VERSION was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:4: warning: already initialized constant JSON::VERSION_ARRAY/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:4: warning: previous definition of VERSION_ARRAY was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:5: warning: already initialized constant JSON::VERSION_MAJOR/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:5: warning: previous definition of VERSION_MAJOR was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:6: warning: already initialized constant JSON::VERSION_MINOR/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:6: warning: previous definition of VERSION_MINOR was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:7: warning: already initialized constant JSON::VERSION_BUILD/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:7: warning: previous definition of VERSION_BUILD was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:99: warning: already initialized constant JSON::NaN/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:99: warning: previous definition of NaN was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:101: warning: already initialized constant JSON::Infinity/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:101: warning: previous definition of Infinity was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:103: warning: already initialized constant JSON::MinusInfinity/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:103: warning: previous definition of MinusInfinity was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:128: warning: already initialized constant JSON::UnparserError/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:128: warning: previous definition of UnparserError was hereIt seems there is something wrong with the fluentd.@KeithTtAttach files by dragging & dropping,, or pasting from the clipboard.Styling with Markdown is supported# kubectl logs fluentd-es-v1.22-ccpkd –namespace=kube-system /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:3: warning: already initialized constant JSON::VERSION/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:3: warning: previous definition of VERSION was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:4: warning: already initialized constant JSON::VERSION_ARRAY/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:4: warning: previous definition of VERSION_ARRAY was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:5: warning: already initialized constant JSON::VERSION_MAJOR/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:5: warning: previous definition of VERSION_MAJOR was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:6: warning: already initialized constant JSON::VERSION_MINOR/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:6: warning: previous definition of VERSION_MINOR was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:7: warning: already initialized constant JSON::VERSION_BUILD/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:7: warning: previous definition of VERSION_BUILD was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:99: warning: already initialized constant JSON::NaN/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:99: warning: previous definition of NaN was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:101: warning: already initialized constant JSON::Infinity/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:101: warning: previous definition of Infinity was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:103: warning: already initialized constant JSON::MinusInfinity/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:103: warning: previous definition of MinusInfinity was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:128: warning: already initialized constant JSON::UnparserError/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:128: warning: previous definition of UnparserError was here这应该是fluentd出问题了吧？

我是在1.5.3上跑的EFK，现在能获取到ES的信息，但是访问KIBANA报错http://172.16.100.215:32619/api/v1/proxy/namespaces/kube-system/services/kibana-logging/app/kibana{“statusCode”:404,”error”:”Not Found”}# kubectl logs kibana-logging-1918083406-j1z97 –namespace=kube-systemserver.basePath: /api/v1/proxy/namespaces/kube-system/services/kibana-logging{“type”:”log”,”@timestamp”:”2017-02-26T05:02:41Z”,”tags”:["info","optimize"],”pid”:7,”message”:”Optimizing and caching bundles for kibana and statusPage. This may take a few minutes”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:46Z”,”tags”:["info","optimize"],”pid”:7,”message”:”Optimization of bundles for kibana and statusPage complete in 425.30 seconds”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:46Z”,”tags”:["status","plugin:kibana@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:elasticsearch@1.0.0","info"],”pid”:7,”state”:”yellow”,”message”:”Status changed from uninitialized to yellow – Waiting for Elasticsearch”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:kbn_vislib_vis_types@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:markdown_vis@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:metric_vis@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:spyModes@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:statusPage@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["status","plugin:table_vis@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from uninitialized to green – Ready”,”prevState”:”uninitialized”,”prevMsg”:”uninitialized”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:47Z”,”tags”:["listening","info"],”pid”:7,”message”:”Server running at http://0.0.0.0:5601“}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:52Z”,”tags”:["status","plugin:elasticsearch@1.0.0","info"],”pid”:7,”state”:”yellow”,”message”:”Status changed from yellow to yellow – No existing Kibana index found”,”prevState”:”yellow”,”prevMsg”:”Waiting for Elasticsearch”}{“type”:”log”,”@timestamp”:”2017-02-26T05:09:56Z”,”tags”:["status","plugin:elasticsearch@1.0.0","info"],”pid”:7,”state”:”green”,”message”:”Status changed from yellow to green – Kibana index ready”,”prevState”:”yellow”,”prevMsg”:”No existing Kibana index found”}{“type”:”response”,”@timestamp”:”2017-02-27T05:51:19Z”,”tags”:[],”pid”:7,”method”:”head”,”statusCode”:200,”req”:{“url”:”/”,”method”:”head”,”headers”:{“host”:”10.46.0.6:5601″,”user-agent”:”curl/7.29.0″,”accept”:”*/*”,”x-forwarded-for”:”127.0.0.1″,”x-forwarded-uri”:”/api/v1/proxy/namespaces/kube-system/services/kibana-logging/”},”remoteAddress”:”10.40.0.0″,”userAgent”:”10.40.0.0″},”res”:{“statusCode”:200,”responseTime”:35,”contentLength”:9},”message”:”HEAD / 200 35ms – 9.0B”}{“type”:”log”,”@timestamp”:”2017-02-28T18:39:38Z”,”tags”:["status","plugin:elasticsearch@1.0.0","error"],”pid”:7,”state”:”red”,”message”:”Status changed from green to red – Request Timeout after 3000ms”,”prevState”:”green”,”prevMsg”:”Kibana index ready”}{“type”:”response”,”@timestamp”:”2017-03-06T07:20:44Z”,”tags”:[],”pid”:7,”method”:”get”,”statusCode”:404,”req”:{“url”:”/api/v1/proxy/namespaces/kube-system/services/kibana-logging/app/kibana”,”method”:”get”,”headers”:{“host”:”172.16.100.215:32619″,”connection”:”keep-alive”,”cache-control”:”max-age=0″,”upgrade-insecure-requests”:”1″,”user-agent”:”Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36″,”accept”:”text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8″,”referer”:”http://172.16.100.215:32619/“,”accept-encoding”:”gzip, deflate, sdch”,”accept-language”:”zh-CN,zh;q=0.8″},”remoteAddress”:”10.40.0.0″,”userAgent”:”10.40.0.0″,”referer”:”http://172.16.100.215:32619/“},”res”:{“statusCode”:404,”responseTime”:3,”contentLength”:9},”message”:”GET /api/v1/proxy/namespaces/kube-system/services/kibana-logging/app/kibana 404 3ms – 9.0B”}# kubectl logs fluentd-es-v1.22-ccpkd –namespace=kube-system /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:3: warning: already initialized constant JSON::VERSION/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:3: warning: previous definition of VERSION was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:4: warning: already initialized constant JSON::VERSION_ARRAY/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:4: warning: previous definition of VERSION_ARRAY was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:5: warning: already initialized constant JSON::VERSION_MAJOR/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:5: warning: previous definition of VERSION_MAJOR was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:6: warning: already initialized constant JSON::VERSION_MINOR/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:6: warning: previous definition of VERSION_MINOR was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/version.rb:7: warning: already initialized constant JSON::VERSION_BUILD/opt/td-agent/embedded/lib/ruby/2.1.0/json/version.rb:7: warning: previous definition of VERSION_BUILD was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:99: warning: already initialized constant JSON::NaN/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:99: warning: previous definition of NaN was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:101: warning: already initialized constant JSON::Infinity/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:101: warning: previous definition of Infinity was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:103: warning: already initialized constant JSON::MinusInfinity/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:103: warning: previous definition of MinusInfinity was here/opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/json-1.8.1/lib/json/common.rb:128: warning: already initialized constant JSON::UnparserError/opt/td-agent/embedded/lib/ruby/2.1.0/json/common.rb:128: warning: previous definition of UnparserError was here这应该是fluentd出问题了吧？

fluentd pod输出的warn log在我的集群里也有，但应该不是问题。kibana输出日志来看，kibana的启动似乎也正常。但通过浏览器访问后，这句日志的问题需进一步查一下为何timeout：["status","plugin:elasticsearch@1.0.0","error"],”pid”:7,”state”:”red”,”message”:”Status changed from green to red – Request Timeout after 3000ms”,”prevState”:”green”,”prevMsg”:”Kibana index ready”} 是什么timeout了？elastic-logging正常么？

# kubectl logs elasticsearch-logging-v1-24xbx –namespace=kube-system [2017-02-26 04:45:14,565][INFO ][node ] [elasticsearch-logging-v1-24xbx] version[2.4.1], pid[18], build[c67dc32/2016-09-27T18:57:55Z][2017-02-26 04:45:14,566][INFO ][node ] [elasticsearch-logging-v1-24xbx] initializing …[2017-02-26 04:45:15,472][INFO ][plugins ] [elasticsearch-logging-v1-24xbx] modules [reindex, lang-expression, lang-groovy], plugins [], sites [][2017-02-26 04:45:15,500][INFO ][env ] [elasticsearch-logging-v1-24xbx] using data paths, mounts [[/data (/dev/vda1)]], net usable_space [6.3gb], net total_space [9.9gb], spins? [possibly], types [xfs][2017-02-26 04:45:15,500][INFO ][env ] [elasticsearch-logging-v1-24xbx] heap size [990.7mb], compressed ordinary object pointers [true][2017-02-26 04:45:18,609][INFO ][node ] [elasticsearch-logging-v1-24xbx] initialized[2017-02-26 04:45:18,609][INFO ][node ] [elasticsearch-logging-v1-24xbx] starting …[2017-02-26 04:45:18,770][INFO ][transport ] [elasticsearch-logging-v1-24xbx] publish_address {10.46.0.4:9300}, bound_addresses {[::]:9300}[2017-02-26 04:45:18,775][INFO ][discovery ] [elasticsearch-logging-v1-24xbx] kubernetes-logging/CyV6J3XHR2KtMpCyeD4cUQ[2017-02-26 04:45:21,866][INFO ][cluster.service ] [elasticsearch-logging-v1-24xbx] detected_master {elasticsearch-logging-v1-7kh92}{0fMEO1PpTM6XteJXy6Xq1Q}{10.32.0.7}{10.32.0.7:9300}{master=true}, added {{elasticsearch-logging-v1-7kh92}{0fMEO1PpTM6XteJXy6Xq1Q}{10.32.0.7}{10.32.0.7:9300}{master=true},}, reason: zen-disco-receive(from master [{elasticsearch-logging-v1-7kh92}{0fMEO1PpTM6XteJXy6Xq1Q}{10.32.0.7}{10.32.0.7:9300}{master=true}])[2017-02-26 04:45:21,873][INFO ][http ] [elasticsearch-logging-v1-24xbx] publish_address {10.46.0.4:9200}, bound_addresses {[::]:9200}[2017-02-26 04:45:21,873][INFO ][node ] [elasticsearch-logging-v1-24xbx] started# kubectl logs elasticsearch-logging-v1-7kh92 –namespace=kube-system [2017-02-26 04:44:37,094][INFO ][node ] [elasticsearch-logging-v1-7kh92] version[2.4.1], pid[18], build[c67dc32/2016-09-27T18:57:55Z][2017-02-26 04:44:37,095][INFO ][node ] [elasticsearch-logging-v1-7kh92] initializing …[2017-02-26 04:44:37,893][INFO ][plugins ] [elasticsearch-logging-v1-7kh92] modules [reindex, lang-expression, lang-groovy], plugins [], sites [][2017-02-26 04:44:37,917][INFO ][env ] [elasticsearch-logging-v1-7kh92] using data paths, mounts [[/data (/dev/vda1)]], net usable_space [5.7gb], net total_space [9.9gb], spins? [possibly], types [xfs][2017-02-26 04:44:37,917][INFO ][env ] [elasticsearch-logging-v1-7kh92] heap size [990.7mb], compressed ordinary object pointers [true][2017-02-26 04:44:41,517][INFO ][node ] [elasticsearch-logging-v1-7kh92] initialized[2017-02-26 04:44:41,586][INFO ][node ] [elasticsearch-logging-v1-7kh92] starting …[2017-02-26 04:44:41,712][INFO ][transport ] [elasticsearch-logging-v1-7kh92] publish_address {10.32.0.7:9300}, bound_addresses {[::]:9300}[2017-02-26 04:44:41,718][INFO ][discovery ] [elasticsearch-logging-v1-7kh92] kubernetes-logging/0fMEO1PpTM6XteJXy6Xq1Q[2017-02-26 04:45:11,787][WARN ][discovery ] [elasticsearch-logging-v1-7kh92] waited for 30s and no initial state was set by the discovery[2017-02-26 04:45:11,796][INFO ][http ] [elasticsearch-logging-v1-7kh92] publish_address {10.32.0.7:9200}, bound_addresses {[::]:9200}[2017-02-26 04:45:11,796][INFO ][node ] [elasticsearch-logging-v1-7kh92] started[2017-02-26 04:45:21,849][INFO ][cluster.service ] [elasticsearch-logging-v1-7kh92] new_master {elasticsearch-logging-v1-7kh92}{0fMEO1PpTM6XteJXy6Xq1Q}{10.32.0.7}{10.32.0.7:9300}{master=true}, added {{elasticsearch-logging-v1-24xbx}{CyV6J3XHR2KtMpCyeD4cUQ}{10.46.0.4}{10.46.0.4:9300}{master=true},}, reason: zen-disco-join(elected_as_master, joins received)[2017-02-26 04:45:21,991][INFO ][gateway ] [elasticsearch-logging-v1-7kh92] recovered [0] indices into cluster_state[2017-02-26 05:09:53,192][INFO ][cluster.metadata ] [elasticsearch-logging-v1-7kh92] [.kibana] creating index, cause [api], templates [], shards / , mappings [config][2017-02-26 05:09:53,792][INFO ][cluster.routing.allocation] [elasticsearch-logging-v1-7kh92] Cluster health status changed from [RED] to [YELLOW] (reason: [shards started [[.kibana][0]] …]).[2017-02-26 05:09:54,247][INFO ][cluster.routing.allocation] [elasticsearch-logging-v1-7kh92] Cluster health status changed from [YELLOW] to [GREEN] (reason: [shards started [[.kibana][0]] …]).这里ES跑了两个pod，不知道节点够不够？从日志上看好像是green的

而且我能访问到ES# curl -L http://localhost:8080/api/v1/proxy/namespaces/kube-system/services/elasticsearch-logging{ “name” : “elasticsearch-logging-v1-24xbx”, “cluster_name” : “kubernetes-logging”, “cluster_uuid” : “C_dC0NQMQl-c8ObIBFQ8Fw”, “version” : { “number” : “2.4.1″, “build_hash” : “c67dc32e24162035d18d6fe1e952c4cbcbe79d16″, “build_timestamp” : “2016-09-27T18:57:55Z”, “build_snapshot” : false, “lucene_version” : “5.5.2″ }, “tagline” : “You Know, for Search”}

好像被吞了一条，补一下ES日志# kubectl logs elasticsearch-logging-v1-24xbx –namespace=kube-system [2017-02-26 04:45:14,565][INFO ][node ] [elasticsearch-logging-v1-24xbx] version[2.4.1], pid[18], build[c67dc32/2016-09-27T18:57:55Z][2017-02-26 04:45:14,566][INFO ][node ] [elasticsearch-logging-v1-24xbx] initializing …[2017-02-26 04:45:15,472][INFO ][plugins ] [elasticsearch-logging-v1-24xbx] modules [reindex, lang-expression, lang-groovy], plugins [], sites [][2017-02-26 04:45:15,500][INFO ][env ] [elasticsearch-logging-v1-24xbx] using data paths, mounts [[/data (/dev/vda1)]], net usable_space [6.3gb], net total_space [9.9gb], spins? [possibly], types [xfs][2017-02-26 04:45:15,500][INFO ][env ] [elasticsearch-logging-v1-24xbx] heap size [990.7mb], compressed ordinary object pointers [true][2017-02-26 04:45:18,609][INFO ][node ] [elasticsearch-logging-v1-24xbx] initialized[2017-02-26 04:45:18,609][INFO ][node ] [elasticsearch-logging-v1-24xbx] starting …[2017-02-26 04:45:18,770][INFO ][transport ] [elasticsearch-logging-v1-24xbx] publish_address {10.46.0.4:9300}, bound_addresses {[::]:9300}[2017-02-26 04:45:18,775][INFO ][discovery ] [elasticsearch-logging-v1-24xbx] kubernetes-logging/CyV6J3XHR2KtMpCyeD4cUQ[2017-02-26 04:45:21,866][INFO ][cluster.service ] [elasticsearch-logging-v1-24xbx] detected_master {elasticsearch-logging-v1-7kh92}{0fMEO1PpTM6XteJXy6Xq1Q}{10.32.0.7}{10.32.0.7:9300}{master=true}, added {{elasticsearch-logging-v1-7kh92}{0fMEO1PpTM6XteJXy6Xq1Q}{10.32.0.7}{10.32.0.7:9300}{master=true},}, reason: zen-disco-receive(from master [{elasticsearch-logging-v1-7kh92}{0fMEO1PpTM6XteJXy6Xq1Q}{10.32.0.7}{10.32.0.7:9300}{master=true}])[2017-02-26 04:45:21,873][INFO ][http ] [elasticsearch-logging-v1-24xbx] publish_address {10.46.0.4:9200}, bound_addresses {[::]:9200}[2017-02-26 04:45:21,873][INFO ][node ] [elasticsearch-logging-v1-24xbx] started# kubectl logs elasticsearch-logging-v1-7kh92 –namespace=kube-system [2017-02-26 04:44:37,094][INFO ][node ] [elasticsearch-logging-v1-7kh92] version[2.4.1], pid[18], build[c67dc32/2016-09-27T18:57:55Z][2017-02-26 04:44:37,095][INFO ][node ] [elasticsearch-logging-v1-7kh92] initializing …[2017-02-26 04:44:37,893][INFO ][plugins ] [elasticsearch-logging-v1-7kh92] modules [reindex, lang-expression, lang-groovy], plugins [], sites [][2017-02-26 04:44:37,917][INFO ][env ] [elasticsearch-logging-v1-7kh92] using data paths, mounts [[/data (/dev/vda1)]], net usable_space [5.7gb], net total_space [9.9gb], spins? [possibly], types [xfs][2017-02-26 04:44:37,917][INFO ][env ] [elasticsearch-logging-v1-7kh92] heap size [990.7mb], compressed ordinary object pointers [true][2017-02-26 04:44:41,517][INFO ][node ] [elasticsearch-logging-v1-7kh92] initialized[2017-02-26 04:44:41,586][INFO ][node ] [elasticsearch-logging-v1-7kh92] starting …[2017-02-26 04:44:41,712][INFO ][transport ] [elasticsearch-logging-v1-7kh92] publish_address {10.32.0.7:9300}, bound_addresses {[::]:9300}[2017-02-26 04:44:41,718][INFO ][discovery ] [elasticsearch-logging-v1-7kh92] kubernetes-logging/0fMEO1PpTM6XteJXy6Xq1Q[2017-02-26 04:45:11,787][WARN ][discovery ] [elasticsearch-logging-v1-7kh92] waited for 30s and no initial state was set by the discovery[2017-02-26 04:45:11,796][INFO ][http ] [elasticsearch-logging-v1-7kh92] publish_address {10.32.0.7:9200}, bound_addresses {[::]:9200}[2017-02-26 04:45:11,796][INFO ][node ] [elasticsearch-logging-v1-7kh92] started[2017-02-26 04:45:21,849][INFO ][cluster.service ] [elasticsearch-logging-v1-7kh92] new_master {elasticsearch-logging-v1-7kh92}{0fMEO1PpTM6XteJXy6Xq1Q}{10.32.0.7}{10.32.0.7:9300}{master=true}, added {{elasticsearch-logging-v1-24xbx}{CyV6J3XHR2KtMpCyeD4cUQ}{10.46.0.4}{10.46.0.4:9300}{master=true},}, reason: zen-disco-join(elected_as_master, joins received)[2017-02-26 04:45:21,991][INFO ][gateway ] [elasticsearch-logging-v1-7kh92] recovered [0] indices into cluster_state[2017-02-26 05:09:53,192][INFO ][cluster.metadata ] [elasticsearch-logging-v1-7kh92] [.kibana] creating index, cause [api], templates [], shards / , mappings [config][2017-02-26 05:09:53,792][INFO ][cluster.routing.allocation] [elasticsearch-logging-v1-7kh92] Cluster health status changed from [RED] to [YELLOW] (reason: [shards started [[.kibana][0]] …]).[2017-02-26 05:09:54,247][INFO ][cluster.routing.allocation] [elasticsearch-logging-v1-7kh92] Cluster health status changed from [YELLOW] to [GREEN] (reason: [shards started [[.kibana][0]] …]).

看这里的es的日志也都很正常，暂没看出问题在哪。

你觉得还有什么可能性造成timeout

我重新跑了kibana的rc，起来还是这样….

似乎还是网络问题，这个issue似乎和你的很想：https://discuss.elastic.co/t/es-request-timeout-after-30000ms/38250/7。你试试在kinaba container里去访问一下es logging的服务端口：kubectl exec xxxx curl xxxxx or docker exec xxxx curl xxxx，不知道kibana的image中是否有curl之类的网络工具。

其实我觉得，最起码kibana要能打开页面，能连接es获取数据是第二步…

我切到kibana-logging都可以找到elasticsearch-logging，但是访问还是不行，我没有配ingress,只是直接把kibana-logging端口暴露到主机，错误和你一样的http://192.168.122.34:31522/api/v1/proxy/namespaces/kube-system/services/kibana-logging/app/kibana{“statusCode”:404,”error”:”Not Found”}oot@kibana-logging-1918083406-41zq9:/# curl -L http://elasticsearch-logging:9200 { “name” : “elasticsearch-logging-v1-53k51″, “cluster_name” : “kubernetes-logging”, “cluster_uuid” : “xEkdjb9YSEKp3JvWbPBPLg”, “version” : { “number” : “2.4.1″, “build_hash” : “c67dc32e24162035d18d6fe1e952c4cbcbe79d16″, “build_timestamp” : “2016-09-27T18:57:55Z”, “build_snapshot” : false, “lucene_version” : “5.5.2″ }, “tagline” : “You Know, for Search”}root@kibana-logging-1918083406-41zq9:/#

我碰到同样问题

很有用，学习了。另外有个地方：kibana中创建的是一个针对index-patten的视图，实际index是数据进来时候就auto create了的选择time-base mode，然后在field中使用date 或者 @timestamp 分时，保存覆盖，这样日志会在界面上会按时间维度展示，看日志更方便些。ps:看到博主在2017gopher是受邀演讲嘉宾了，期待

感谢提醒。time-base mode看起来的确方便好多。

大佬，我有一个疑问，就是我发现fluentd从log中读到的是json格式的日志，实际上业务的日志在log这个字段中，想请问一下，如何才能把这个字段的日志提出来再配上自己的表达式

您好，我在启动elasticsearch时，配置了serviceAccount，还是报“failed to send ping to [{#zen_unicast_1#}{127.0.0.1}{127.0.0.1:9300}]”的错误，请问这可能是哪里的问题呢，谢谢

kubernetes官方最新版的yaml文件已经不需要修改这些了, 一键就创建好了.