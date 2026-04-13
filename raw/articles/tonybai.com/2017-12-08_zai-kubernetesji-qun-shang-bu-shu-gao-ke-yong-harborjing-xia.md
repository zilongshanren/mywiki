---
title: 在Kubernetes集群上部署高可用Harbor镜像仓库
url: https://tonybai.com/2017/12/08/deploy-high-availability-harbor-on-kubernetes-cluster/
published: '2017-12-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 在Kubernetes集群上部署高可用Harbor镜像仓库

关于[基于Harbor的高可用私有镜像仓库](http://tonybai.com/2017/06/09/setup-a-high-availability-private-registry-based-on-harbor-and-cephfs/)，在我的博客里[曾不止一次提到](http://tonybai.com/2017/06/15/fix-auth-fail-when-login-harbor-registry/)，在[源创会2017沈阳站](http://tonybai.com/2017/10/24/go-evolution-for-ten-years-an-interview-by-osc/)上，我还专门[以此题目和大家做了分享](http://tonybai.com/2017/10/23/the-speech-script-practice-on-deploying-a-ha-harbor-cluster-for-osc-shenyang-2017/)。事后，很多人通过[微博私信](https://weibo.com/bigwhite20xx)、[个人公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000004&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483828&idx=1&sn=d8bcc352a0ad2fdb5e02f3a2c40c4b2b&send_time=)或博客评论问我是否可以在[Kubernetes集群](http://tonybai.com/tag/kubernetes)上安装高可用的[Harbor](https://github.com/vmware/harbor)仓库，今天我就用这篇文章来回答大家这个问题。

## 一、Kubernetes上的高可用Harbor方案

首先，我可以肯定给出一个回答：Harbor支持在Kubernetes部署。只不过Harbor官方的默认安装并非是高可用的，而是“单点式”的。在[《基于Harbor的高可用企业级私有容器镜像仓库部署实践》](http://tonybai.com/2017/10/23/the-speech-script-practice-on-deploying-a-ha-harbor-cluster-for-osc-shenyang-2017/)一文中，我曾谈到了一种在裸机或VM上的、基于[Cephfs](http://tonybai.com/2017/05/08/mount-cephfs-acrossing-nodes-in-kubernetes-cluster/)共享存储的高可用Harbor方案。在Kubernetes上部署，其高可用的思路也是类似的，可见下面这幅示意图：

![img{512x368}](../../assets/dedfcc300c033c47.png)


围绕这幅示意图，简单说明一下我们的方案：

- 通过在Kubernetes上启动Harbor内部各组件的多个副本的方式实现Harbor服务的计算高可用；
- 通过挂载CephFS共享存储的方式实现镜像数据高可用；
- Harbor使用的配置数据和关系数据放在外部(External)数据库集群中，保证数据高可用和实时一致性；
- 通过外部
[Redis](https://redis.io/)集群实现UI组件的session共享。

方案确定后，接下来我们就开始部署。

## 二、环境准备

在Harbor官方的[对Kubernetes支持的说明](https://github.com/vmware/harbor/blob/master/docs/kubernetes_deployment.md)中，提到当前的Harbor on kubernetes相关脚本和配置在Kubernetes v1.6.5和Harbor v1.2.0上验证测试通过了，因此在我们的实验环境中，[Kubernetes](http://tonybai.com/tag/kubernetes)至少要准备v1.6.5及以后版本。下面是我的环境的一些信息：

```
Kubernetes使用v1.7.3版本：
# kubelet --version
Kubernetes v1.7.3
Docker使用17.03.2版本：
# docker version
Client:
Version: 17.03.2-ce
API version: 1.27
Go version: go1.7.5
Git commit: f5ec1e2
Built: Tue Jun 27 03:35:14 2017
OS/Arch: linux/amd64
Server:
Version: 17.03.2-ce
API version: 1.27 (minimum version 1.12)
Go version: go1.7.5
Git commit: f5ec1e2
Built: Tue Jun 27 03:35:14 2017
OS/Arch: linux/amd64
Experimental: false
```


关于Harbor的相关脚本，我们直接用master branch中的，而不是v1.2.0这个release版本中的。**切记**！否则你会发现v1.2.0版本源码中的相关kubernetes支持脚本根本就没法工作，甚至缺少adminserver组件的相关脚本。不过Harbor相关组件的image版本，我们使用的还是**v1.2.0**的：

```
Harbor源码的版本：
commit 82d842d77c01657589d67af0ea2d0c66b1f96014
Merge pull request #3741 from wy65701436/add-tc-concourse on Dec 4, 2017
Harbor各组件的image的版本：
REPOSITORY TAG IMAGE ID
vmware/harbor-jobservice v1.2.0 1fb18427db11
vmware/harbor-ui v1.2.0 b7069ac3bd4b
vmware/harbor-adminserver v1.2.0 a18331f0c1ae
vmware/registry 2.6.2-photon c38af846a0da
vmware/nginx-photon 1.11.13 2971c92cc1ae
```


除此之外，高可用Harbor使用外部的DB cluster和redis cluster，DB cluster我们采用MySQL，对于MySQL cluster，可以使用[mysql galera cluster](http://galeracluster.com/products/)或MySQL5.7以上版本自带的Group Replication (MGR) 集群。

## 三、探索harbor on k8s部署脚本和配置

我们在本地创建harbor-install-on-k8s目录，并将Harbor最新源码下载到该目录下：

```
# mkdir harbor-install-on-k8s
# cd harbor-install-on-k8s
# wget -c https://github.com/vmware/harbor/archive/master.zip
# unzip master.zip
# cd harbor-master
# ls -F
AUTHORS CHANGELOG.md contrib/ CONTRIBUTING.md docs/
LICENSE make/ Makefile NOTICE partners.md README.md
ROADMAP.md src/ tests/ tools/ VERSION
```


将Harbor部署到k8s上的脚本就在make/kubernetes目录下：

```
# cd harbor-master/make
# tree kubernetes
kubernetes
├── adminserver
│ ├── adminserver.rc.yaml
│ └── adminserver.svc.yaml
├── jobservice
│ ├── jobservice.rc.yaml
│ └── jobservice.svc.yaml
├── k8s-prepare
├── mysql
│ ├── mysql.rc.yaml
│ └── mysql.svc.yaml
├── nginx
│ ├── nginx.rc.yaml
│ └── nginx.svc.yaml
├── pv
│ ├── log.pvc.yaml
│ ├── log.pv.yaml
│ ├── registry.pvc.yaml
│ ├── registry.pv.yaml
│ ├── storage.pvc.yaml
│ └── storage.pv.yaml
├── registry
│ ├── registry.rc.yaml
│ └── registry.svc.yaml
├── templates
│ ├── adminserver.cm.yaml
│ ├── jobservice.cm.yaml
│ ├── mysql.cm.yaml
│ ├── nginx.cm.yaml
│ ├── registry.cm.yaml
│ └── ui.cm.yaml
└── ui
├── ui.rc.yaml
└── ui.svc.yaml
8 directories, 25 files
```


- k8s-prepare脚本：根据templates下的模板文件以及harbor.cfg中的配置生成各个组件，比如registry等的最终configmap配置文件。它的作用类似于用docker-compose工具部署Harbor时的prepare脚本；
- templates目录：templates目录下放置各个组件的配置模板文件（configmap文件模板），将作为k8s-prepare的输入；
- pv目录：Harbor组件所使用的存储插件的配置，默认情况下使用hostpath，对于高可用Harbor而言，我们这里将使用cephfs；
- 其他组件目录，比如：registry：这些目录中存放这各个组件的service yaml和rc yaml，用于在Kubernetes cluster启动各个组件时使用。

下面我用一个示意图来形象地描述一下配置的生成过程以及各个文件在后续Harbor组件启动中的作用：

![img{512x368}](../../assets/0b4a33f9152c7d8d.png)


由于使用external mysql db，Harbor自带的mysql组件我们不会使用，对应的pv目录下的storage.pv.yaml和storage.pvc.yaml我们也不会去关注和使用。

## 四、部署步骤

### 1、配置和创建挂载Cephfs的pv和pvc

我们先在共享分布式存储CephFS上为Harbor的存储需求创建目录：apps/harbor-k8s，并在harbor-k8s下创建两个子目录：log和registry，分别满足jobservice和registry的存储需求：

```
# cd /mnt // CephFS的根目录挂载到了/mnt下面
# mkdir -p apps/harbor-k8s/log
# mkdir -p apps/harbor-k8s/registry
# tree apps/harbor-k8s
apps/harbor-k8s
├── log
└── registry
```


关于CephFS的挂载等具体操作步骤，可以参见我的[《Kubernetes集群跨节点挂载CephFS》](http://tonybai.com/2017/05/08/mount-cephfs-acrossing-nodes-in-kubernetes-cluster/)一文。

接下来，创建用于k8s pv挂载cephfs的ceph-secret，我们编写一个ceph-secret.yaml文件：

```
//ceph-secret.yaml
apiVersion: v1
data:
key: {base64 encoding of the ceph admin.secret}
kind: Secret
metadata:
name: ceph-secret
type: Opaque
```


创建ceph-secret：

```
# kubectl create -f ceph-secret.yaml
secret "ceph-secret" created
```


最后，我们来修改pv、pvc文件并创建对应的pv和pvc资源，要修改的文件包括pv/log.xxx和pv/registry.xxx，我们的目的就是用cephfs替代原先的hostPath：

```
//log.pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
name: log-pv
labels:
type: log
spec:
capacity:
storage: 1Gi
accessModes:
- ReadWriteMany
cephfs:
monitors:
- {ceph-mon-node-ip}:6789
path: /apps/harbor-k8s/log
user: admin
secretRef:
name: ceph-secret
readOnly: false
persistentVolumeReclaimPolicy: Retain
//log.pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
name: log-pvc
spec:
accessModes:
- ReadWriteMany
resources:
requests:
storage: 1Gi
selector:
matchLabels:
type: log
// registry.pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
name: registry-pv
labels:
type: registry
spec:
capacity:
storage: 5Gi
accessModes:
- ReadWriteMany
cephfs:
monitors:
- 10.47.217.91:6789
path: /apps/harbor-k8s/registry
user: admin
secretRef:
name: ceph-secret
readOnly: false
persistentVolumeReclaimPolicy: Retain
//registry.pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
name: registry-pvc
spec:
accessModes:
- ReadWriteMany
resources:
requests:
storage: 5Gi
selector:
matchLabels:
type: registry
```


创建pv和pvc：

```
# kubectl create -f log.pv.yaml
persistentvolume "log-pv" created
# kubectl create -f log.pvc.yaml
persistentvolumeclaim "log-pvc" created
# kubectl create -f registry.pv.yaml
persistentvolume "registry-pv" created
# kubectl create -f registry.pvc.yaml
persistentvolumeclaim "registry-pvc" created
# kubectl get pvc
NAME STATUS VOLUME CAPACITY ACCESSMODES STORAGECLASS AGE
log-pvc Bound log-pv 1Gi RWX 31s
registry-pvc Bound registry-pv 5Gi RWX 2s
# kubectl get pv
NAME CAPACITY ACCESSMODES RECLAIMPOLICY STATUS CLAIM STORAGECLASS REASON AGE
log-pv 1Gi RWX Retain Bound default/log-pvc 36s
registry-pv 5Gi RWX Retain Bound default/registry-pvc 6s
```


### 2、创建和初始化Harbor用的数据库

我们需要在External DB中创建Harbor访问数据库所用的user(harbork8s/harbork8s)以及所使用的数据库(registry_k8s)：

```
mysql> create user harbork8s identified by 'harbork8s';
Query OK, 0 rows affected (0.03 sec)
mysql> GRANT ALL PRIVILEGES ON *.* TO 'harbork8s'@'%' IDENTIFIED BY 'harbork8s' WITH GRANT OPTION;
Query OK, 0 rows affected, 1 warning (0.00 sec)
# mysql> create database registry_k8s;
Query OK, 1 row affected (0.00 sec)
mysql> grant all on registry_k8s.* to 'harbork8s' identified by 'harbork8s';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```


由于目前Harbor还不支持自动init数据库，因此我们需要为新建的registry_k8s数据库做初始化，具体的方案就是先使用docker-compose工具在本地启动一个harbor，通过mysqldump将harbor-db container中的数据表dump出来，再导入到external db中的registry_k8s中，具体操作步骤如下：

```
# wget -c http://harbor.orientsoft.cn/harbor-1.2.0/harbor-offline-installer-v1.2.0.tgz
# tar zxvf harbor-offline-installer-v1.2.0.tgz
进入harbor目录，修改harbor.cfg中的hostname:
hostname = hub.tonybai.com:31777
# ./prepare
# docker-compose up -d
找到harbor_db的container id: 77fde71390e7，进入容器，并将数据库registry dump出来：
# docker exec -i -t 77fde71390e7 bash
# mysqldump -u root -pxxx --databases registry > registry.dump
离开容器，将容器内导出的registry.dump copy到本地：
# docker cp 77fde71390e7:/tmp/registry.dump ./
修改registry.dump为registry_k8s.dump，修改其内容中的registry为registry_k8s，然后导入到external db：
# mysqldump -h external_db_ip -P 3306 -u harbork8s -pharbork8s
mysql> source ./registry_k8s.dump;
```


### 3、配置make/harbor.cfg

harbor.cfg是整个配置生成的重要输入，我们在k8s-prepare执行之前，先要根据我们的需要和环境对harbor.cfg进行配置：

```
// make/harbor.cfg
hostname = hub.tonybai.com:31777
db_password = harbork8s
db_host = {external_db_ip}
db_user = harbork8s
```


### 4、对templates目录下的configmap配置模板(*.cm.yaml)进行配置调整

- templates/adminserver.cm.yaml:

```
MYSQL_HOST: {external_db_ip}
MYSQL_USR: harbork8s
MYSQL_DATABASE: registry_k8s
RESET: "true"
```


注：adminserver.cm.yaml没有使用harbor.cfg中的有关数据库的配置项，而是需要单独再配置一遍，这块估计将来会fix掉这个问题。

- templates/registry.cm.yaml:

```
rootcertbundle: /etc/registry/root.crt
```


- templates/ui.cm.yaml:

ui组件需要添加session共享。ui组件读取_REDIS_URL环境变量：

```
//vmware/harbor/src/ui/main.go
... ..
redisURL := os.Getenv("_REDIS_URL")
if len(redisURL) > 0 {
beego.BConfig.WebConfig.Session.SessionProvider = "redis"
beego.BConfig.WebConfig.Session.SessionProviderConfig = redisURL
}
... ...
而redisURL的格式在beego的源码中有说明：
// beego/session/redis/sess_redis.go
// SessionInit init redis session
// savepath like redis server addr,pool size,password,dbnum
// e.g. 127.0.0.1:6379,100,astaxie,0
func (rp *Provider) SessionInit(maxlifetime int64, savePath string) error {...}
```


因此，我们在templates/ui.cm.yaml中添加一行：

```
_REDIS_URL: {redis_ip}:6379,100,{redis_password},11
```


jobservice.cm.yaml和nginx.cm.yaml无需改变。

### 5、对各组件目录下的xxx.rc.yaml和xxx.svc.yaml配置模板进行配置调整

- adminserver/adminserver.rc.yaml

```
replicas: 3
```


- adminserver/adminserver.svc.yaml

不变。

- jobservice/jobservice.rc.yaml、jobservice/jobservice.svc.yaml

不变。

- nginx/nginx.rc.yaml

```
replicas: 3
```


- nginx/nginx.svc.yaml

```
apiVersion: v1
kind: Service
metadata:
name: nginx
spec:
type: NodePort
ports:
- name: http
port: 80
nodePort: 31777
protocol: TCP
selector:
name: nginx-apps
```


- registry/registry.rc.yaml

```
replicas: 3
mountPath: /etc/registry
```


**这里有一个严重的 bug**，即registry.rc.yaml中configmap的默认mount路径：/etc/docker/registry与registry的docker image中的registry配置文件的路径/etc/registry不一致，这将导致我们精心配置的registry的configmap根本没有发挥作用，数据依然在memory中，而不是在我们配置的Cephfs中。这样一旦registry container退出，仓库的image数据就会丢失。同时也无法实现数据的高可用。因此，我们将mountPath都改为与registry image的一致，即：/etc/registry目录。

- registry/registry.svc.yaml

不变。

- ui/ui.rc.yaml

```
replicas: 3
```


- ui/ui.svc.yaml

```
- name: _REDIS_URL
valueFrom:
configMapKeyRef:
name: harbor-ui-config
key: _REDIS_URL
```


### 6、执行k8s-prepare

执行k8s-prepare，生成各个组件的configmap文件：

```
# ./k8s-prepare
# git status
... ...
adminserver/adminserver.cm.yaml
jobservice/jobservice.cm.yaml
mysql/mysql.cm.yaml
nginx/nginx.cm.yaml
registry/registry.cm.yaml
ui/ui.cm.yaml
```


### 7、启动Harbor组件

- 创建configmap

```
# kubectl apply -f jobservice/jobservice.cm.yaml
configmap "harbor-jobservice-config" created
# kubectl apply -f nginx/nginx.cm.yaml
configmap "harbor-nginx-config" created
# kubectl apply -f registry/registry.cm.yaml
configmap "harbor-registry-config" created
# kubectl apply -f ui/ui.cm.yaml
configmap "harbor-ui-config" created
# kubectl apply -f adminserver/adminserver.cm.yaml
configmap "harbor-adminserver-config" created
# kubectl get cm
NAME DATA AGE
harbor-adminserver-config 42 14s
harbor-jobservice-config 8 16s
harbor-nginx-config 3 16s
harbor-registry-config 2 15s
harbor-ui-config 9 15s
```


- 创建harbor各组件对应的k8s service

```
# kubectl apply -f jobservice/jobservice.svc.yaml
service "jobservice" created
# kubectl apply -f nginx/nginx.svc.yaml
service "nginx" created
# kubectl apply -f registry/registry.svc.yaml
service "registry" created
# kubectl apply -f ui/ui.svc.yaml
service "ui" created
# kubectl apply -f adminserver/adminserver.svc.yaml
service "adminserver" created
# kubectl get svc
NAME CLUSTER-IP EXTERNAL-IP PORT(S)
adminserver 10.103.7.8 <none> 80/TCP
jobservice 10.104.14.178 <none> 80/TCP
nginx 10.103.46.129 <nodes> 80:31777/TCP
registry 10.101.185.42 <none> 5000/TCP,5001/TCP
ui 10.96.29.187 <none> 80/TCP
```


- 创建rc，启动各个组件pods

```
# kubectl apply -f registry/registry.rc.yaml
replicationcontroller "registry-rc" created
# kubectl apply -f jobservice/jobservice.rc.yaml
replicationcontroller "jobservice-rc" created
# kubectl apply -f ui/ui.rc.yaml
replicationcontroller "ui-rc" created
# kubectl apply -f nginx/nginx.rc.yaml
replicationcontroller "nginx-rc" created
# kubectl apply -f adminserver/adminserver.rc.yaml
replicationcontroller "adminserver-rc" created
#kubectl get pods
NAMESPACE NAME READY STATUS RESTARTS AGE
default adminserver-rc-9pc78 1/1 Running 0 3m
default adminserver-rc-pfqtv 1/1 Running 0 3m
default adminserver-rc-w55sx 1/1 Running 0 3m
default jobservice-rc-d18zk 1/1 Running 1 3m
default nginx-rc-3t5km 1/1 Running 0 3m
default nginx-rc-6wwtz 1/1 Running 0 3m
default nginx-rc-dq64p 1/1 Running 0 3m
default registry-rc-6w3b7 1/1 Running 0 3m
default registry-rc-dfdld 1/1 Running 0 3m
default registry-rc-t6fnx 1/1 Running 0 3m
default ui-rc-0kwrz 1/1 Running 1 3m
default ui-rc-kzs8d 1/1 Running 1 3m
default ui-rc-vph6d 1/1 Running 1 3m
```


## 五、验证与Troubleshooting

### 1、docker cli访问

由于harbor默认使用了http访问，因此在docker login前先要将我们的仓库地址加到/etc/docker/daemon.json的insecure-registries中：

```
///etc/docker/daemon.json
{
"insecure-registries": ["hub.tonybai.com:31777"]
}
```


systemctl daemon-reload and restart后，我们就可以通过docker login登录新建的仓库了(初始密码：Harbor12345)：

```
docker login hub.tonybai.com:31777
Username (admin): admin
Password:
Login Succeeded
```


### 2、docker push & pull

我们测试上传一个busybox image：

```
# docker pull busybox
Using default tag: latest
latest: Pulling from library/busybox
0ffadd58f2a6: Pull complete
Digest: sha256:bbc3a03235220b170ba48a157dd097dd1379299370e1ed99ce976df0355d24f0
Status: Downloaded newer image for busybox:latest
# docker tag busybox:latest hub.tonybai.com:31777/library/busybox:latest
# docker push hub.tonybai.com:31777/library/busybox:latest
The push refers to a repository [hub.tonybai.com:31777/library/busybox]
0271b8eebde3: Preparing
0271b8eebde3: Pushing [==================================================>] 1.338 MB
0271b8eebde3: Pushed
latest: digest: sha256:179cf024c8a22f1621ea012bfc84b0df7e393cb80bf3638ac80e30d23e69147f size: 527
```


下载刚刚上传的busybox:

```
# docker pull hub.tonybai.com:31777/library/busybox:latest
latest: Pulling from library/busybox
414e5515492a: Pull complete
Digest: sha256:179cf024c8a22f1621ea012bfc84b0df7e393cb80bf3638ac80e30d23e69147f
Status: Downloaded newer image for hub.tonybai.com:31777/library/busybox:latest
```


### 3、访问Harbor UI

在浏览器中打开http://hub.tonybai.com:31777，用admin/Harbor12345登录，如果看到下面页面，说明安装部署成功了：

![img{512x368}](../../assets/348c90e39a3a3f0d.png)


## 六、参考资料

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

你好，在docker的生态中国外有docker hub ，quay.io 等，但是国内还没有独立镜像仓库服务商，你觉得如果有这样的商家提供类似hubor或者quay.io的功能你会使用吗？当然也包括docker hub的镜像功能。

我会用。至少个人的一些开源项目或小工具会使用。至于组织或公司这个级别是否会用，这个因公司情况而定，当然也和服务商提供的服务是否能满足需求有关了。

那你认为如果要给公司提供什么样的服务会让公司有意向使用呢？我的考虑可能是私有部署，高可用，易管理。跨机房同步。我在考虑这个创业方案时也担心想daocloud这样的docker厂商集成了基础镜像管理导致独立镜像服务比较难进入企业服务

您是想在国内做一个quay.io这样的独立镜像仓库服务？

基本是这个思路，所以请教下您认为是否靠谱？

靠不靠谱不敢妄言:) 用过国内的一些非单纯以镜像服务作为主业的，比如aliyun的镜像服务，虽然是免费的，但体验并不是特别好。说明这块的确有改善空间。但这样的独立服务，个人觉得只能针对独立开发者或中小型开发企业或组织。规模再大一些的企业势必会自建镜像仓库服务，几乎不会或最终都不会(早期可能会)将镜像放在外面的。对于中小型开发组织，镜像服务的安全可能不是那么重要了(>当然对外宣称一定是安全的)，稳定、性能、使用体验、与开发运流水线的集成难易程度、与其他代码托管服务、ci服务的对接是否easy等可能会影响这些企业是否使用这样服务的决定。

谢谢给了那么多建议。我这边已经开始着手修改harbor了，因为现在只有一个人，进度会慢点。一个月内会出一个基础版本，实现企业权限管理（当然horbar基本包括，但还需要修改一些东西），接着会开始做docker hub的mirror的功能。同时进行小批量测试和推广，我的mirror和其他mirror会很大不一样。对于这个产品，使用体验和方便管理应该是重点，当然性能、稳定和第三方集成是必须的。第三方集成会和国内的代码仓库集成推广（有可能的话），gitlab、GitHub也会支持。另外也会考虑做成一个分享的平台，如docker hub

哈哈，感觉我也没提啥好建议。不过很佩服您的魄力。您所说的版本发布，是指用户应用镜像如何发布到用您的产品搭建的平台上？

我是指我开发的平台如果发布希望您能帮忙试用下，给给意见。。哈哈

嗯嗯。期待您的大作早日问世。

如何版本发布也希望您能帮忙提提意见。。呵呵

经过年后这段时间的准备，我开发了一个精简版的docker镜像仓库产品：https://douwa.tech/

希望兄台能抽空帮忙提下意见，主要是在功能上。我想把CI/CD作为下一步大的计划，当前这个镜像仓库目前还有很多需要完善的。准备把daocloud.io和codefresh.io作为竞品。好像目前过来做Docker方面SaaS并不多，现在七牛也开始做容器了。我的定位是做镜像仓库、CI、CD，不做服务器和K8S，那些让阿里云这样的大厂去解决。

架构上目前还没有做HA，这个问题不大，目前就只有数据库mysql会存在单点问题，这个后续会切换到直接支持ha的newsql上。存储方面直接使用oss保证可用性。

方便使用邮箱和您沟通吗？

我的邮箱，bigwhite.cn@aliyun.com，欢迎沟通。您要做的这个平台也不算小，兄台背后应该有一个团队吧？

大大的赞。codefresh.io这个很不错。国内这方面的服务似乎多是绑定某个容器云平台了。没有独立的。

harbor可以对接redis三主三从嘛

这个我没试过，不能给出结论:)。