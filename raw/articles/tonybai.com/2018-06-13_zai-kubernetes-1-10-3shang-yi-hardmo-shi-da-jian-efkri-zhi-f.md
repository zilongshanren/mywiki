---
title: 在Kubernetes 1.10.3上以Hard模式搭建EFK日志分析平台
url: https://tonybai.com/2018/06/13/setup-efk-on-kubernetes-1-10-3-in-the-hard-way/
published: '2018-06-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 在Kubernetes 1.10.3上以Hard模式搭建EFK日志分析平台

在一年多之前，我曾写过一篇文章[《使用Fluentd和ElasticSearch Stack实现Kubernetes的集群Logging》](https://tonybai.com/2017/03/03/implement-kubernetes-cluster-level-logging-with-fluentd-and-elasticsearch-stack/)，文中讲解了如何在[Kubernetes](https://tonybai.com/tag/kubernetes)上利用EFK（[elastic](https://www.elastic.co/), [fluentd](https://www.fluentd.org/), [kibana](https://www.elastic.co/products/kibana)）搭建一套可用的集中日志分析平台。当时的k8s使用的是[1.3.7版本](https://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)，创建EFK使用的是[kubernetes项目](https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/fluentd-elasticsearch)中**cluster/addons/fluentd-elasticsearch**下面的全套yaml文件，yaml中Elastic Search的volume用的还是emptyDir，并未真正持久化。

经过一年多的发展，Kubernetes发生了[“翻天覆地”的变化](https://www.cncf.io/announcement/2018/03/06/cloud-native-computing-foundation-announces-kubernetes-first-graduated-project/)，EFK技术栈也有了很大的进展。虽然那篇文章中的方案、步骤以及问题的解决思路仍有参考价值，但毕竟“年代”不同了，有些东西需要“与时俱进”。恰好近期在协助同事搭建一个[移动互联网医院](http://www.gov.cn/zhengce/content/2018-04/28/content_5286645.htm)的演示环境时，我又一次搭建了一套“较新”版本的EFK，这里记录一下搭建过程、遇到的坑以及问题的解决过程，算是对之前“陈旧知识”的一个更新吧。

## 一. 环境和部署方案

这次部署我使用了较新的Kubernetes stable版本：[1.10.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.10.3)，这是一个单master node和三个worker node组成的演示环境，集群由[kubeadm](https://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)创建并引导启动。经过这些年的发展和演进，kubeadm引导启动的集群已经十分稳定了，并且搭建过程也是十分顺利（集群使用的是[weave network](https://www.weave.works/)插件）。

在EFK部署方案上，我没有再选择直接使用[kubernetes项目](https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/fluentd-elasticsearch)中**cluster/addons/fluentd-elasticsearch**下面的全套yaml文件，而是打算逐个组件单独安装的hard模式。

下面是一个部署示意图：

![img{512x368}](../../assets/21e4dad82b8aa217.png)


虽然Kubernetes在持久化存储方面有[诸多机制](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)和插件可用，但总体来说，目前的k8s在storage这块依旧是短板，用起来体验较差，希望[Container Storage Interface, CSI](https://kubernetes.io/blog/2018/04/10/container-storage-interface-beta/)的引入和未来发展能降低开发人员的心智负担。因此，这次我将Elastic Search放在了k8s集群外单独单点部署，并直接使用local file system进行数据存取；fluentd没有变化，依旧是以DaemonSet控制的Pod的形式运行在每个k8s node上; kibana部署在集群内部，并通过ingress将服务暴露到集群外面。

## 二. 部署Elastic Search

按照部署方案，我们将Elastic Search部署在k8s集群外面，但我们依旧使用容器化部署方式。Elastic Search的官方镜像仓库已经由docker hub迁移到[elasticsearch自己维护的仓库](https://www.docker.elastic.co/)了。

我们下载当前ElasticSearch的最新版6.2.4：

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.2.4
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
docker.elastic.co/elasticsearch/elasticsearch 6.2.4 7cb69da7148d 8 weeks ago 515 MB
```


在本地创建elasticsearch的数据存储目录：~/es_data，修改该目录的owner和group均为1000：

```
# mkdir ~/es_data
# chmod g+rwx es_data
# chgrp 1000 es_data
# chown 1000 -R es_data
# ls -l /root/es_data/
total 8
drwxrwxr-x 2 1000 1000 4096 Jun 8 09:50 ./
drwx------ 8 root root 4096 Jun 8 09:50 ../
```


注意：务必对es_data按上述命令执行修改，否则在启动elasticsearch容器可能会出现如下错误：

```
[WARN ][o.e.b.ElasticsearchUncaughtExceptionHandler] [] uncaught exception in thread [main]
_*org.elasticsearch.bootstrap.StartupException: java.lang.IllegalStateException: Failed to create node environment*_
at org.elasticsearch.bootstrap.Elasticsearch.init(Elasticsearch.java:125) ~[elasticsearch-6.2.4.jar:6.2.4]
... ...
Caused by: java.nio.file.AccessDeniedException: /usr/share/elasticsearch/data/nodes
at sun.nio.fs.UnixException.translateToIOException(UnixException.java:84) ~[?:?]
... ...
```


启动elasticsearch容器：

```
# docker run -d --restart=unless-stopped -p 9200:9200 -p 9300:9300 -v /root/es_data:/usr/share/elasticsearch/data --ulimit nofile=65536:65536 -e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.2.4
```


如果看到下面日志，说明elasticsearch容器启动成功了!

```
[INFO ][o.e.c.m.MetaDataCreateIndexService] [sGZc7Wa] [.monitoring-es-6-2018.06.08] creating index, cause [auto(bulk api)], templates [.monitoring-es], shards [1]/[0], mappings [doc]
[INFO ][o.e.c.r.a.AllocationService] [sGZc7Wa] Cluster health status changed from [YELLOW] to [GREEN] (reason: [shards started [[.monitoring-es-6-2018.06.08][0]] ...]).
```


检查es健康状态：

```
# curl http://127.0.0.1:9200/_cat/health
1528424599 02:23:19 docker-cluster green 1 1 1 1 0 0 0 0 - 100.0%
```


es工作一切健康！

## 三. 部署Fluentd

相比较而言，fluentd的部署相对简单，因为[fluentd官网文档](https://docs.fluentd.org/v0.12/articles/kubernetes-fluentd)有明确的安装说明。由于k8s默认授权机制采用了RBAC，因此我们使用[fluentd-daemonset-elasticsearch-rbac.yaml](https://github.com/fluent/fluentd-kubernetes-daemonset/blob/master/fluentd-daemonset-elasticsearch-rbac.yaml)来创建fluentd daemonset。

不过在创建前，我们需要打开fluentd-daemonset-elasticsearch-rbac.yaml修改一下它连接的elasticsearch的地址信息：

```
containers:
- name: fluentd
image: fluent/fluentd-kubernetes-daemonset:elasticsearch
env:
- name: FLUENT_ELASTICSEARCH_HOST
value: "172.16.66.104" // 172.16.66.104就是我们的elasticsearch运行的节点的ip
```


接下来创建fluentd:

```
# kubectl apply -f fluentd-daemonset-elasticsearch-rbac.yaml
serviceaccount "fluentd" created
clusterrole.rbac.authorization.k8s.io "fluentd" created
clusterrolebinding.rbac.authorization.k8s.io "fluentd" created
daemonset.extensions "fluentd" created
```


查看某一个fluentd pod的启动日志如下：

```
# kubectl logs -f pods/fluentd-4rptt -n kube-system
[info]: reading config file path="/fluentd/etc/fluent.conf"
[info]: starting fluentd-0.12.33
[info]: gem 'fluent-plugin-elasticsearch' version '1.16.0'
[info]: gem 'fluent-plugin-kubernetes_metadata_filter' version '1.0.2'
[info]: gem 'fluent-plugin-record-reformer' version '0.9.1'
[info]: gem 'fluent-plugin-secure-forward' version '0.4.5'
[info]: gem 'fluentd' version '0.12.33'
[info]: adding match pattern="fluent.**" type="null"
[info]: adding filter pattern="kubernetes.**" type="kubernetes_metadata"
[info]: adding match pattern="**" type="elasticsearch"
[info]: adding source type="tail"
... ...
[info]: following tail of /var/log/containers/weave-net-9kds5_kube-system_weave-13ef6f321b2bc64dc920878c7d361440c0157b91f6025f23c631edb5feb3473a.log
[info]: following tail of /var/log/containers/fluentd-4rptt_kube-system_fluentd-bdc80586d5cafc10729fb277ce01cf28d595059eabf96b66324f32b3b6873e28.log
[info]: Connection opened to Elasticsearch cluster => {:host=>"172.16.66.104", :port=>9200, :scheme=>"http", :user=>"elastic", :password=>"obfuscated"}
... ...
```


没有报错！似乎fluentd启动ok了。

再来通过elasticsearch日志验证一下：

```
[INFO ][o.e.c.m.MetaDataCreateIndexService] [sGZc7Wa] [logstash-2018.06.07] creating index, cause [auto(bulk api)], templates [], shards [5]/[1], mappings []
[INFO ][o.e.c.m.MetaDataCreateIndexService] [sGZc7Wa] [logstash-2018.06.08] creating index, cause [auto(bulk api)], templates [], shards [5]/[1], mappings []
[INFO ][o.e.c.m.MetaDataMappingService] [sGZc7Wa] [logstash-2018.06.07/XetLly2ZQFKKd0JVvxl5fA] create_mapping [fluentd]
[INFO ][o.e.c.m.MetaDataMappingService] [sGZc7Wa] [logstash-2018.06.07/XetLly2ZQFKKd0JVvxl5fA] update_mapping [fluentd]
[INFO ][o.e.c.m.MetaDataMappingService] [sGZc7Wa] [logstash-2018.06.07/XetLly2ZQFKKd0JVvxl5fA] update_mapping [fluentd]
[INFO ][o.e.c.m.MetaDataMappingService] [sGZc7Wa] [logstash-2018.06.08/j5soBzyVSNOvBQg-E3NkCA] create_mapping [fluentd]
[INFO ][o.e.c.m.MetaDataMappingService] [sGZc7Wa] [logstash-2018.06.08/j5soBzyVSNOvBQg-E3NkCA] update_mapping [fluentd]
[INFO ][o.e.c.m.MetaDataMappingService] [sGZc7Wa] [logstash-2018.06.08/j5soBzyVSNOvBQg-E3NkCA] update_mapping [fluentd]
[INFO ][o.e.c.m.MetaDataMappingService] [sGZc7Wa] [logstash-2018.06.07/XetLly2ZQFKKd0JVvxl5fA] update_mapping [fluentd]
[INFO ][o.e.c.m.MetaDataMappingService] [sGZc7Wa] [logstash-2018.06.08/j5soBzyVSNOvBQg-E3NkCA] update_mapping [fluentd]
```


fluentd已经成功连接上es了！

## 四. 部署Kibana

我们将kibana部署到Kubernetes集群内，我们使用kubernetes项目中的cluster/addons/fluentd-elasticsearch下的kibana yaml文件来创建kibana部署和服务：

```
https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/fluentd-elasticsearch/kibana-deployment.yaml
https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/fluentd-elasticsearch/kibana-service.yaml
```


创建前，我们需要修改一下kibana-deployment.yaml：

```
... ...
image: docker.elastic.co/kibana/kibana:6.2.4 // 这里，我们使用最新的版本：6.2.4
- name: ELASTICSEARCH_URL
value: http://172.16.66.104:9200 //这里，我们用上面的elasticsearch的服务地址填入到value的值中
.... ...
```


创建kibana：

```
# kubectl apply -f kibana-service.yaml
service "kibana-logging" created
# kubectl apply -f kibana-deployment.yaml
deployment.apps "kibana-logging" created
```


查看启动的kibana pod，看到如下错误日志：

```
{"type":"log","@timestamp":"2018-06-08T07:09:08Z","tags":["fatal"],"pid":1,"message":"\"xpack.monitoring.ui.container.elasticsearch.enabled\" setting was not applied. Check for spelling errors and ensure that expected plugins are installed and enabled."}
FATAL "xpack.monitoring.ui.container.elasticsearch.enabled" setting was not applied. Check for spelling errors and ensure that expected plugins are installed and enabled.
```


似乎与xpack有关。我们删除kibana-deployment.yaml中的两个环境变量：XPACK_MONITORING_ENABLED和XPACK_SECURITY_ENABLED，再重新apply。查看kibana pod日志：

```
# kubectl logs -f kibana-logging-648dbdf986-bc24x -n kube-system
{"type":"log","@timestamp":"2018-06-08T07:16:27Z","tags":["status","plugin:kibana@6.2.4","info"],"pid":1,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"uninitialized","prevMsg":"uninitialized"}
{"type":"log","@timestamp":"2018-06-08T07:16:27Z","tags":["status","plugin:elasticsearch@6.2.4","info"],"pid":1,"state":"yellow","message":"Status changed from uninitialized to yellow - Waiting for Elasticsearch","prevState":"uninitialized","prevMsg":"uninitialized"}
... ...
{"type":"log","@timestamp":"2018-06-08T07:16:30Z","tags":["info","monitoring-ui","kibana-monitoring"],"pid":1,"message":"Starting all Kibana monitoring collectors"}
{"type":"log","@timestamp":"2018-06-08T07:16:30Z","tags":["license","info","xpack"],"pid":1,"message":"Imported license information from Elasticsearch for the [monitoring] cluster: mode: basic | status: active | expiry date: 2018-07-08T02:06:08+00:00"}
```


可以看到kibana启动成功！

使用kubectl proxy启动代理，在浏览器中建立sock5 proxy，然后在浏览器访问：http://localhost:8001/api/v1/namespaces/kube-system/services/kibana-logging/proxy， 你应该可以看到下面的kibana首页:

![img{512x368}](../../assets/b583d3e865f83b4a.png)


创建index pattern后，等待一会，查看边栏中的”Discover”，如果你看到类似下面截图中的日志内容输出，说明kibana可以正常从elasticsearch获取数据了：

![img{512x368}](../../assets/d0e007b6a43bfa0a.png)


## 五. 为kibana添加ingress

使用kubectl proxy查看kibana虽然简单，但略显麻烦，将kibana服务暴露到集群外更为方便。下面我们就给kibana添加带basic auth的ingress。

### 1. 部署ingress controller及默认后端(如果cluster已经部署过，则忽略此步骤)

我们选择k8s官方的[ingress-nginx](https://github.com/kubernetes/ingress-nginx)作为ingress controller，并部署默认后端default-backend，我们把ingress-nginx controller和default-backend统统部署在**kube-system**命令空间下。

```
下载https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
mandatory.yaml中的namespace的值都改为kube-system
docker pull anjia0532/defaultbackend:1.4
docker tag anjia0532/defaultbackend:1.4 gcr.io/google_containers/defaultbackend:1.4
docker pull quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.15.0
# kubectl apply -f mandatory.yaml
deployment.extensions "default-http-backend" created
service "default-http-backend" created
configmap "nginx-configuration" created
configmap "tcp-services" created
configmap "udp-services" created
serviceaccount "nginx-ingress-serviceaccount" created
clusterrole.rbac.authorization.k8s.io "nginx-ingress-clusterrole" created
role.rbac.authorization.k8s.io "nginx-ingress-role" created
rolebinding.rbac.authorization.k8s.io "nginx-ingress-role-nisa-binding" created
clusterrolebinding.rbac.authorization.k8s.io "nginx-ingress-clusterrole-nisa-binding" created
deployment.extensions "nginx-ingress-controller" created
```


此时nginx-ingress controller已经安装完毕，nginx-ingress controller本质上就是一个nginx，目前它还没有暴露服务端口，我们通过nodeport方式暴露nginx-ingress service到集群外面：

```
下载https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/provider/baremetal/service-nodeport.yaml
修改service-nodeport.yaml:
apiVersion: v1
kind: Service
metadata:
name: ingress-nginx
namespace: kube-system
spec:
type: NodePort
ports:
- name: http
port: 80
targetPort: 80
nodePort: 30080
protocol: TCP
- name: https
port: 443
targetPort: 443
nodePort: 30443
protocol: TCP
selector:
app: ingress-nginx
# kubectl apply -f service-nodeport.yaml
service "ingress-nginx" created
# lsof -i tcp:30080
COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
kube-prox 24565 root 9u IPv6 10447591 0t0 TCP *:30080 (LISTEN)
```


我们验证一下nginx-ingress controller工作是否正常：

```
在任意一个集群node上：
# curl localhost:30080
default backend - 404
```


### 2. 为kibana添加ingress

[ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)是一种抽象。对于[nginx](https://tonybai.com/2016/11/22/deploy-nginx-service-for-the-services-in-kubernetes-cluster/) ingress controller来说，创建一个ingress相当于在nginx.conf中添加一个server入口，并nginx -s reload生效。

我们创建kibana的ingress yaml:

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
annotations:
name: kibana-logging-ingress
namespace: kube-system
spec:
rules:
- host: kibana.tonybai.com
http:
paths:
- backend:
serviceName: kibana-logging
servicePort: 5601
```


由于ingress中的host只能是域名，这里用 kibana.tonybai.com，然后在/etc/hosts中增加该域名的ip地址映射。

创建kibana-logging-ingress：

```
# kubectl apply -f kibana-logging-ingress.yaml
ingress.extensions "kibana-logging-ingress" created
```


此时，我们打开浏览器，访问http://kibana.tonybai.com:30080，我们得到了如下结果：

```
{"statusCode":404,"error":"Not Found","message":"Not Found"}
```


我们再次用curl试一下：

```
# curl -L kibana.tonybai.com:30080
<script>var hashRoute = '/api/v1/namespaces/kube-system/services/kibana-logging/proxy/appl;
var defaultRoute = '/api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana';
var hash = window.location.hash;
if (hash.length) {
window.location = hashRoute + hash;
} else {
window.location = defaultRoute;
```


这显然不是我们预想的结果。我们查看一下kibana pod对应的日志，并对比了一下使用kubectl proxy访问kibana的日志：

```
通过ingress访问的错误日志：
{"type":"response","@timestamp":"2018-06-11T10:20:55Z","tags":[],"pid":1,"method":"get","statusCode":404,"req":{"url":"/api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana","method":"get","headers":{"host":"kibana.tonybai.com:30080","connection":"close","x-request-id":"b066d69c31ce3c9e89efa6264966561c","x-real-ip":"192.168.16.1","x-forwarded-for":"192.168.16.1","x-forwarded-host":"kibana.tonybai.com:30080","x-forwarded-port":"80","x-forwarded-proto":"http","x-original-uri":"/api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana","x-scheme":"http","cache-control":"max-age=0","upgrade-insecure-requests":"1","user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-language":"zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"},"remoteAddress":"192.168.20.5","userAgent":"192.168.20.5"},"res":{"statusCode":404,"responseTime":4,"contentLength":9},"message":"GET /api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana 404 4ms - 9.0B"}
通过kubectl proxy访问的正确日志：
{"type":"response","@timestamp":"2018-06-11T10:20:43Z","tags":[],"pid":1,"method":"get","statusCode":304,"req":{"url":"/ui/fonts/open_sans/open_sans_v13_latin_regular.woff2","method":"get","headers":{"host":"localhost:8001","user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36","accept":"*/*","accept-encoding":"gzip, deflate, br","accept-language":"zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7","if-modified-since":"Thu, 12 Apr 2018 20:57:06 GMT","if-none-match":"\"afc44700053c9a28f9ab26f6aec4862ac1d0795d\"","origin":"http://localhost:8001","referer":"http://localhost:8001/api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana","x-forwarded-for":"127.0.0.1, 172.16.66.101","x-forwarded-uri":"/api/v1/namespaces/kube-system/services/kibana-logging/proxy/ui/fonts/open_sans/open_sans_v13_latin_regular.woff2"},"remoteAddress":"192.168.16.1","userAgent":"192.168.16.1","referer":"http://localhost:8001/api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana"},"res":{"statusCode":304,"responseTime":3,"contentLength":9},"message":"GET /ui/fonts/open_sans/open_sans_v13_latin_regular.woff2 304 3ms - 9.0B"}
```


我们看到通过ingress访问，似乎将/api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana这个url path也传递给后面的kibana了，而kibana却无法处理。

我们回头看一下kibana-deployment.yaml，那里面有一个env var:

```
- name: SERVER_BASEPATH
value: /api/v1/namespaces/kube-system/services/kibana-logging/proxy
```


问题似乎就出在这里。我们去掉这个env var，并重新apply kibana-deployment.yaml。然后再用浏览器访问：http://kibana.tonybai.com:30080/app/kibana，kibana的页面就会出现在眼前了。

但是这样更新后，**通过kubectl proxy方式似乎就无法正常访问kibana了**，这里也只能二选一了，我们选择ingress访问。

### 3. 添加basic auth for kibana-logging ingress

虽然kibana ingress生效了，但目前kibana ingress目前在“裸奔”，我们还是要适当加上一些auth的，我们选择basic auth，从原理上讲这是加到[nginx](https://tonybai.com/2016/11/22/deploy-nginx-service-for-the-services-in-kubernetes-cluster/)上的basic auth，kibana自身并没有做basic auth：

我们借助htpasswd工具生成用户名和密码，并基于此创建secret对象：

```
# htpasswd -c auth tonybai
New password:
Re-type new password:
Adding password for user tonybai
# cat auth
tonybai:$apr1$pQuJZfll$KPfa1rXJUTBBKktxtbVsI0
#kubectl create secret generic basic-auth --from-file=auth -n kube-system
secret "basic-auth" created
# kubectl get secret basic-auth -o yaml -n kube-system
apiVersion: v1
data:
auth: dG9ueWJhaTokYXByMSRwUXVKWmZsbCRLUGZhMXJYSlVUQkJLa3R4dGJWc0kwCg==
kind: Secret
metadata:
annotations:
kubectl.kubernetes.io/last-applied-configuration: |
{"apiVersion":"v1","data":{"auth":"dG9ueWJhaTokYXByMSRwUXVKWmZsbCRLUGZhMXJYSlVUQkJLa3R4dGJWc0kwCg=="},"kind":"Secret","metadata":{"annotations":{},"name":"basic-auth","namespace":"kube-system"},"type":"Opaque"}
creationTimestamp: 2018-06-11T23:05:42Z
name: basic-auth
namespace: kube-system
resourceVersion: "579134"
selfLink: /api/v1/namespaces/kube-system/secrets/basic-auth
uid: f6ec373e-6dcb-11e8-a0e8-00163e0cd764
type: Opaque
```


在kibana-logging-ingress.yaml中增加有关auth的annotations：

```
// kibana-logging-ingress.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
annotations:
nginx.ingress.kubernetes.io/auth-type: basic
nginx.ingress.kubernetes.io/auth-secret: basic-auth
nginx.ingress.kubernetes.io/auth-realm: "Authentication Required - tonybai"
name: kibana-logging-ingress
namespace: kube-system
spec:
rules:
- host: kibana.tonybai.com
http:
paths:
- backend:
serviceName: kibana-logging
servicePort: 5601
```


apply kibana-logging-ingress.yaml后，我们再次访问：kibana.tonybai.com:30080

![img{512x368}](../../assets/4cb61590272d382d.png)


至此，一个演示环境下的EFK日志平台就搭建完毕了。相信有了这种hard way的安装搭建经验，我们可以灵活应对针对其中某个组件的变种部署了（比如[将elasticsearch放到k8s中部署](https://tonybai.com/2017/03/03/implement-kubernetes-cluster-level-logging-with-fluentd-and-elasticsearch-stack/)）。

**更多内容可以通过我在慕课网开设的实战课程 《Kubernetes实战 高可用集群搭建、配置、运维与应用》学习。**

[51短信平台](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

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

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

为什么我创建好kibana后再外部访问是Connection refused？

kibana是运行在cluster中的，仅在k8s node上可以直接访问kibana的service或pod地址。默认应该是不暴露到集群外的吧。如果要暴露到集群外，需要为kibana添加ingress配置。