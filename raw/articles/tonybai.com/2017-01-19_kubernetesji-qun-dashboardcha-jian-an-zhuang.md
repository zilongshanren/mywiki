---
title: Kubernetes集群Dashboard插件安装
url: https://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/
published: '2017-01-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes集群Dashboard插件安装

第一次[利用kube-up.sh脚本方式安装Kubernetes 1.3.7集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu)时，我就已经顺利地将[kubernetes dashboard](https://github.com/kubernetes/dashboard) addon安装ok了。至今在这个环境下运行十分稳定。但是毕竟是一个试验环境，有些配置是无法满足生产环境要求的，比如：安全问题。今天有时间对Dashboard的配置进行一些调整，顺带将之前Dashboard插件的安装和配置过程也记录下来，供大家参考。

### 一、Dashboard的默认安装步骤

#### 1、基于默认配置项的安装

采用kube-up.sh在[Ubuntu](http://tonybai.com/tag/ubuntu)上安装dashboard的原理与[安装DNS插件](http://tonybai.com/2016/10/23/install-dns-addon-for-k8s)大同小异，主要涉及的脚本文件和配置项包括：

```
// kubernetes/cluster/config-default.sh
... ...
# Optional: Install Kubernetes UI
ENABLE_CLUSTER_UI="${KUBE_ENABLE_CLUSTER_UI:-true}"
... ...
// kubernetes/cluster/ubuntu/deployAddons.sh
... ...
function deploy_dashboard {
if ${KUBECTL} get rc -l k8s-app=kubernetes-dashboard --namespace=kube-system | grep kubernetes-dashboard-v &> /dev/null; then
echo "Kubernetes Dashboard replicationController already exists"
else
echo "Creating Kubernetes Dashboard replicationController"
${KUBECTL} create -f ${KUBE_ROOT}/cluster/addons/dashboard/dashboard-controller.yaml
fi
if ${KUBECTL} get service/kubernetes-dashboard --namespace=kube-system &> /dev/null; then
echo "Kubernetes Dashboard service already exists"
else
echo "Creating Kubernetes Dashboard service"
${KUBECTL} create -f ${KUBE_ROOT}/cluster/addons/dashboard/dashboard-service.yaml
fi
echo
}
init
... ...
if [ "${ENABLE_CLUSTER_UI}" == true ]; then
deploy_dashboard
fi
```


kube-up.sh会尝试创建”kube-system” namespace，并执行下面命令：

```
kubectl create -f kubernetes/cluster/addons/dashboard/dashboard-controller.yaml
kubectl create -f kubernetes/cluster/addons/dashboard/dashboard-service.yaml
```


这和我们在cluster中创建一个rc和service没有多大区别。

当然上面的安装方式是伴随着k8s cluster的安装进行的，如果要单独安装Dashboard，那么Dashboard主页上的安装方式显然更为简单：

```
kubectl create -f https://rawgit.com/kubernetes/dashboard/master/src/deploy/kubernetes-dashboard.yaml
```


#### 2、调整Dashboard容器启动参数

dashboard-controller.yaml和dashboard-service.yaml两个文件内容如下：

```
//dashboard-controller.yaml
apiVersion: v1
kind: ReplicationController
metadata:
name: kubernetes-dashboard-v1.1.1
namespace: kube-system
labels:
k8s-app: kubernetes-dashboard
version: v1.1.1
kubernetes.io/cluster-service: "true"
spec:
replicas: 1
selector:
k8s-app: kubernetes-dashboard
template:
metadata:
labels:
k8s-app: kubernetes-dashboard
version: v1.1.1
kubernetes.io/cluster-service: "true"
spec:
containers:
- name: kubernetes-dashboard
image: gcr.io/google_containers/kubernetes-dashboard-amd64:v1.1.1
resources:
# keep request = limit to keep this container in guaranteed class
limits:
cpu: 100m
memory: 50Mi
requests:
cpu: 100m
memory: 50Mi
ports:
- containerPort: 9090
livenessProbe:
httpGet:
path: /
port: 9090
initialDelaySeconds: 30
timeoutSeconds: 30
// dashboard-service.yaml
apiVersion: v1
kind: Service
metadata:
name: kubernetes-dashboard
namespace: kube-system
labels:
k8s-app: kubernetes-dashboard
kubernetes.io/cluster-service: "true"
spec:
selector:
k8s-app: kubernetes-dashboard
ports:
- port: 80
targetPort: 9090
```


这两个文件的内容略微陈旧些，用的还是目前已不推荐使用的ReplicationController。

不过这样默认安装后，你可能还会遇到如下问题：

（1） Dashboard pod创建失败：这是由于kubernetes-dashboard-amd64:v1.1.1 image在墙外，pull image失败导致的。

可以通过使用加速器或使用替代image的方式来解决，比如：mritd/kubernetes-dashboard-amd64:v1.4.0。修改一下dashboard-controller.yaml中image那一行即可。

（2）Dashboard无法连接到master node上的api server

如果唯一的dashboard pod（由于replicas=1）被调度到minion node上，那么很可能无法连接上master node上api server(dashboard会在cluster中自动检测api server的存在，但有时候会失败)，导致页面无法正常显示。因此，需要指定一下api server的url，比如：我们在dashboard-controller.yaml中为container启动增加一个启动参数–apiserver-host：

```
// dashboard-controller.yaml
... ...
spec:
containers:
- name: kubernetes-dashboard
image: mritd/kubernetes-dashboard-amd64:v1.4.0
imagePullPolicy: Always
ports:
- containerPort: 9090
protocol: TCP
args:
- --apiserver-host=http://{api server host}:{api server insecure-port}
... ...
```


（3）增加nodeport，提供外部访问路径

dashboard以cluster service的角色运行在cluster中，我们虽然可以[在Node上访问该service或直接访问pod](http://tonybai.com/2017/01/17/understanding-flannel-network-for-kubernetes/)，但要想在外部网络访问到dashboard，还需要另外设置，比如：设置nodeport。

在dashboard-service.yaml中，修改配置如下：

```
spec:
type: NodePort
ports:
- port: 80
targetPort: 9090
nodePort: 12345
```


这样你就可以通过node 的public ip+nodeport访问到dashboard了。

不过这时，你的dashboard算是在“裸奔”，没有任何安全可言：

- dashboard ui没有访问管理机制，任何access都可以全面接管dashboard；

- 同时在背后，dashboard通过insecure-port访问apiserver，没有使用加密机制。

### 二、dashboard通过kubeconfig文件信息访问apiserver

我们先来建立dashboard和apiserver之间的安全通信机制。

当前master上的kube-apiserver的启动参数如下：

```
// /etc/default/kube-apiserver
KUBE_APISERVER_OPTS=" --insecure-bind-address=0.0.0.0 --insecure-port=8080 --etcd-servers=http://127.0.0.1:4001 --logtostderr=true --service-cluster-ip-range=192.168.3.0/24 --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,SecurityContextDeny,ResourceQuota --service-node-port-range=80-32767 --advertise-address={master node local ip} --basic-auth-file=/srv/kubernetes/basic_auth_file --client-ca-file=/srv/kubernetes/ca.crt --tls-cert-file=/srv/kubernetes/server.cert --tls-private-key-file=/srv/kubernetes/server.key"
```


dashboard要与apiserver建立安全通信机制，务必不能使用insecure port。kubernetes apiserver默认情况下secure port也是开启的，端口为6443。同时，apiserver开启了basic auth(–basic-auth-file=/srv/kubernetes/basic_auth_file)。这样一来，dashboard光靠传入的–apiserver-host参数将无法正常访问apiserver的secure port并通过basic auth。我们需要找到另外一个option：

我们来看一下dashboard还支持哪些cmdline options：

```
# docker run mritd/kubernetes-dashboard-amd64:v1.4.0 /dashboard -help
Usage of /dashboard:
--alsologtostderr value log to standard error as well as files
--apiserver-host string The address of the Kubernetes Apiserver to connect to in the format of protocol://address:port, e.g., http://localhost:8080. If not specified, the assumption is that the binary runs inside aKubernetes cluster and local discovery is attempted.
--heapster-host string The address of the Heapster Apiserver to connect to in the format of protocol://address:port, e.g., http://localhost:8082. If not specified, the assumption is that the binary runs inside aKubernetes cluster and service proxy will be used.
--kubeconfig string Path to kubeconfig file with authorization and master location information.
--log-flush-frequency duration Maximum number of seconds between log flushes (default 5s)
--log_backtrace_at value when logging hits line file:N, emit a stack trace (default :0)
--log_dir value If non-empty, write log files in this directory
--logtostderr value log to standard error instead of files (default true)
--port int The port to listen to for incoming HTTP requests (default 9090)
--stderrthreshold value logs at or above this threshold go to stderr (default 2)
-v, --v value log level for V logs
--vmodule value comma-separated list of pattern=N settings for file-filtered logging
```


从输出的options来看，只有–kubeconfig这个能够满足需求。

#### 1、kubeconfig文件介绍

采用kube-up.sh脚本进行kubernetes默认安装后，脚本会在每个Cluster node上创建一个~/.kube/config文件，该[kubeconfig文件](https://kubernetes.io/docs/user-guide/kubeconfig-file/)可为k8s cluster中的组件（比如kubectl等）、addons(比如dashboard等)提供跨全cluster的安全验证机制。

下面是我的minion node上的kubeconfig文件

```
# cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
certificate-authority: /srv/kubernetes/ca.crt
server: https://{master node local ip}:6443
name: ubuntu
contexts:
- context:
cluster: ubuntu
namespace: default
user: admin
name: ubuntu
current-context: ubuntu
kind: Config
preferences: {}
users:
- name: admin
user:
password: {apiserver_password}
username: {apiserver_username}
client-certificate: /srv/kubernetes/kubecfg.crt
client-key: /srv/kubernetes/kubecfg.key
```


kubeconfig中存储了clusters、users、contexts信息，以及其他一些杂项，并通过current-context指定当前context。通过该配置文件，类似kubectl这样的cluster操作工具可以很容易的在各个cluster之间切换context。一个context就是一个三元组：{cluster、user、namespace}，current-context指定当前选定的context，比如上面的kubeconfig文件，当我们执行kubectl时，kubectl会读取该配置文件，并以current-context指定的那个context中的信息去查找user和cluster。这里current-context是ubuntu。

ubuntu这个context三元组中的信息是：

```
{
cluster = ubuntu
namespace = default
user = admin
}
```


之后kubectl到clusters中找到name为ubuntu的cluster，发现其server为https://{master node local ip}:6443，以及其CA信息；到users中找到name为admin的user，并使用该user下的信息：

```
password: {apiserver_password}
username: {apiserver_username}
client-certificate: /srv/kubernetes/kubecfg.crt
client-key: /srv/kubernetes/kubecfg.key
```


通过kubectl config命令可以配置kubeconfig文件，具体命令可以参考[这里](https://kubernetes.io/docs/user-guide/kubeconfig-file/)。

另外上面的/srv/kubernetes/ca.crt、/srv/kubernetes/kubecfg.crt和/srv/kubernetes/kubecfg.key都是kube-up.sh在安装k8s 1.3.7时在各个node上创建的，可以直接用来作为访问apiserver的参数传递给kubectl或其他要访问apiserver的组件或addons。

#### 2、修改dashboard启动参数，使用kubeconfig文件

现在我们要让dashboard使用kubeconfig文件，我们需要修改dashboard-controller.yaml文件中涉及containers的配置信息：

```
spec:
containers:
- name: kubernetes-dashboard
image: mritd/kubernetes-dashboard-amd64:v1.4.0
volumeMounts:
- mountPath: /srv/kubernetes
name: auth
- mountPath: /root/.kube
name: config
imagePullPolicy: Always
ports:
- containerPort: 9090
protocol: TCP
args:
- --kubeconfig=/root/.kube/config
livenessProbe:
httpGet:
path: /
port: 9090
initialDelaySeconds: 30
timeoutSeconds: 30
volumes:
- name: auth
hostPath:
path: /srv/kubernetes
- name: config
hostPath:
path: /root/.kube
```


由于要用到各种证书以及kubeconfig，我们在pod里挂载了host主机的path： /root/.kube和/srv/kubernetes。

重新部署dashboard后，dashboard与kube-apiserver之间就有了安全保障了（https+basic_auth）。

### 三、实现dashboard UI login

虽然上面实现了dashboard与apiserver之间的安全通道和basic auth，但通过nodeport方式访问dashboard，我们依旧可以掌控dashboard，而dashboard依旧没有任何访问控制机制。而实际情况是dashboard目前还[不支持identity and access management](http://blog.kubernetes.io/2016/07/dashboard-web-interface-for-kubernetes.html)，不过在不久的将来，[dashboard将添加这方面的支持](https://github.com/kubernetes/dashboard/issues/964)。

那么在当前版本下，如何实现一个简易的login流程呢？除了前面提到的nodeport方式访问dashboard UI外，官方在[trouble shooting](https://github.com/kubernetes/dashboard/blob/master/docs/user-guide/troubleshooting.md)里还提供了另外两种访问dashboard的方法，我们一起来看看是否能满足我们的最低级需求^0^。

#### 1、kubectl proxy方式

kubectl proxy的方式默认只允许local network访问，但是kubectl proxy提供了若干flag options可以设置，我们来试试：

我们在minion node上执行：

```
# kubectl proxy --address='0.0.0.0' --port=30099
Starting to serve on [::]:30099
```


我们在minion node上的30099端口提供外网服务。打开浏览器，访问: http://{minion node public ip}:30099/ui，得到如下结果：

```
<h3>Unauthorized</h3>
```


到底哪没授权呢？我们查看kubectl proxy的flag options发现下面一个疑点：

```
--accept-hosts='^localhost$,^127\.0\.0\.1$,^\[::1\]$': Regular expression for hosts that the proxy should accept.
```


显然–accept-hosts默认接受的host地址形式让我们的访问受限。重新调整配置再次执行：

```
# kubectl proxy --address='0.0.0.0' --port=30099 --accept-hosts='^*$'
Starting to serve on [::]:30099
```


再次打开浏览器，访问：http://{minion node public ip}:30099/ui

浏览器会跳转至下面的地址：

```
http://{minion node public ip}:30099/api/v1/proxy/namespaces/kube-system/services/kubernetes-dashboard/#/workload?namespace=default
```


dashboard ui访问成功！不过，这种方式依旧无需你输入user/password，这不符合我们的要求。

#### 2、直接访问apiserver方式

trouble shooting文档提供的最后一种访问方式是直接访问apiserver方式：

```
打开浏览器访问：
https://{master node public ip}:6443
```


这时浏览器会提示你：证书问题。忽略之（由于apiserver采用的是自签署的私有证书，浏览器端无法验证apiserver的server.crt），继续访问，浏览器弹出登录对话框，让你输入用户名和密码，这里我们输入apiserver —basic-auth-file中的用户名和密码，就可以成功登录apiserver，并在浏览器页面看到如下内容：

```
{
"paths": [
"/api",
"/api/v1",
"/apis",
"/apis/apps",
"/apis/apps/v1alpha1",
"/apis/autoscaling",
"/apis/autoscaling/v1",
"/apis/batch",
"/apis/batch/v1",
"/apis/batch/v2alpha1",
"/apis/extensions",
"/apis/extensions/v1beta1",
"/apis/policy",
"/apis/policy/v1alpha1",
"/apis/rbac.authorization.k8s.io",
"/apis/rbac.authorization.k8s.io/v1alpha1",
"/healthz",
"/healthz/ping",
"/logs/",
"/metrics",
"/swaggerapi/",
"/ui/",
"/version"
]
}
```


接下来，我们访问下面地址：

```
https://{master node public ip}:6443/ui
```


你会看到页面跳转到：

```
https://101.201.78.51:6443/api/v1/proxy/namespaces/kube-system/services/kubernetes-dashboard/
```


我们成功进入dashboard UI中! 显然这种访问方式满足了我们对dashboard UI采用登录访问的最低需求！

### 三、小结

到目前为止，dashboard已经可以使用。但它还缺少metric和类仪表盘图形展示功能，这两个功能需要额外安装[Heapster](https://github.com/kubernetes/heapster/)才能实现，不过一般功能足以满足你对k8s cluster的管理需求。

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

非常感谢, 由于是摸索阶段, 所以没有为apiserver指定证书, 在配置dns与dashboard插件时遇到了点麻烦. 就是因为没有指定insecure的apiserver地址, 非常感谢博主的两篇文章给我的提醒.