---
title: 解决Kubernetes 1.6.4 Dashboard无法访问的问题
url: https://tonybai.com/2017/07/20/fix-cannot-access-dashboard-in-k8s-1-6-4/
published: '2017-07-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 解决Kubernetes 1.6.4 Dashboard无法访问的问题

前一段时间将之前[采用kubeadm安装的Kubernetes 1.5.1](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)环境升级到了[1.6.4版本](https://github.com/kubernetes/kubernetes/releases/tag/v1.6.4)，升级过程较为顺利。由于该k8s cluster是一个测试环境，当时并没有过于关注，就忙别的事情了。最近项目组打算在这个环境下做一些事情，而当我们重新“捡起”这个环境时，发现[Kubernetes Dashboard](http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/)无法访问了。

Kubernetes的[dashboard](https://github.com/kubernetes/dashboard/)可以有[很多种访问方式](https://github.com/kubernetes/dashboard/blob/master/docs/user-guide/troubleshooting.md)，比如：可以通过暴露nodeport的方式(无身份验证，不安全)、可以通过访问[apiserver](http://tonybai.com/2017/03/03/access-api-server-from-a-pod-through-serviceaccount/)的api服务的方式等。我们的Dashboard通过APIServer进行访问：

```
https://apiserver_ip:secure_port/ui
```


正常情况下通过浏览器访问：https://apiserver_ip:secure_port/ui，浏览器会弹出[身份验证](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)对话框，待输入正确的用户名和密码后，便可成功进入Dashboard了。但当前，我们得到的结果却是：

```
User "system:anonymous" cannot proxy services in the namespace "kube-system".
```


而访问apiserver(https://apiserver_ip:secure_port/)得到的结果如下：

```
User "system:anonymous" cannot get at the cluster scope.
```


## 一、问题原因分析

k8s 1.6.x版本与1.5.x版本的一个很大不同在于1.6.x版本启用了[RBAC](https://kubernetes.io/docs/admin/authorization/rbac/)的[Authorization mode](https://kubernetes.io/docs/admin/authorization/)(授权模型)，这点在K8s master init的日志中可以得到证实：

```
# kubeadm init --apiserver-advertise-address xx.xx.xx
... ...
[init] Using Kubernetes version: v1.6.4
[init] Using Authorization mode: RBAC
[preflight] Running pre-flight checks
[preflight] Starting the kubelet service
[certificates] Generated CA certificate and key.
[certificates] Generated API server certificate and key
.... ...
[apiconfig] Created RBAC rules
[addons] Created essential addon: kube-proxy
[addons] Created essential addon: kube-dns
Your Kubernetes master has initialized successfully!
... ...
```


在[《Kubernetes集群的安全配置》](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)一文中我们提到过Kubernetes API server的访问方法：

```
Authentication(身份验证) -> Authorization（授权）-> Admission Control(入口条件控制)
```


只不过在Kubernetes 1.5.x及以前的版本中，Authorization的环节都采用了默认的配置，即”AlwaysAllow”，对访问APIServer并不产生什么影响：

```
# kube-apiserver -h
... ...
--authorization-mode="AlwaysAllow": Ordered list of plug-ins to do authorization on secure port. Comma-delimited list of: AlwaysAllow,AlwaysDeny,ABAC,Webhook,RBAC
... ...
```


但K8s 1.6.x版本中，–authorization-mode的值发生了变化：

```
# cat /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
containers:
- command:
- kube-apiserver
- --allow-privileged=true
... ...
- --basic-auth-file=/etc/kubernetes/basic_auth_file
- --authorization-mode=RBAC
... ...
```


注：这里我们依旧通过basic auth方式进行apiserver的Authentication，而不是用[客户端数字证书校验](http://tonybai.com/2015/04/30/go-and-https/)等其他方式。

显然问题的原因就在于这里[RBAC授权方式](https://en.wikipedia.org/wiki/Role-based_access_control)的使用，让我们无法正常访问Dashboard了。

## 二、Kubernetes RBAC Authorization简介

RBAC Authorization的基本概念是Role和RoleBinding。Role是一些permission的集合；而RoleBinding则是将Role授权给某些User、某些Group或某些[ServiceAccount](http://tonybai.com/2017/03/03/access-api-server-from-a-pod-through-serviceaccount/)。K8s官方博客[《RBAC Support in Kubernetes》](http://blog.kubernetes.io/2017/04/rbac-support-in-kubernetes.html)一文的中的配图对此做了很生动的诠释：

![img{512x368}](../../assets/364c5bb36b0f3157.png)


从上图中我们可以看到：

Role: pod-reader 拥有Pod的get和list permissions；

RoleBinding: pod-reader 将Role: pod-reader授权给右边的User、Group和ServiceAccount。

和Role和RoleBinding对应的是，K8s还有ClusterRole和ClusterRoleBinding的概念，它们不同之处在于：ClusterRole和ClusterRoleBinding是针对整个Cluster范围内有效的，无论用户或资源所在的namespace是什么；而Role和RoleBinding的作用范围是局限在某个k8s namespace中的。

Kubernetes 1.6.4安装时内建了许多Role/ClusterRole和RoleBinds/ClusterRoleBindings：

```
# kubectl get role -n kube-system
NAME AGE
extension-apiserver-authentication-reader 50d
system:controller:bootstrap-signer 50d
system:controller:token-cleaner 50d
# kubectl get rolebinding -n kube-system
NAME AGE
system:controller:bootstrap-signer 50d
system:controller:token-cleaner 50d
# kubectl get clusterrole
NAME AGE
admin 50d
cluster-admin 50d
edit 50d
system:auth-delegator 50d
system:basic-user 50d
system:controller:attachdetach-controller 50d
... ...
system:discovery 50d
system:heapster 50d
system:kube-aggregator 50d
system:kube-controller-manager 50d
system:kube-dns 50d
system:kube-scheduler 50d
system:node 50d
system:node-bootstrapper 50d
system:node-problem-detector 50d
system:node-proxier 50d
system:persistent-volume-provisioner 50d
view 50d
weave-net 50d
# kubectl get clusterrolebinding
NAME AGE
cluster-admin 50d
kubeadm:kubelet-bootstrap 50d
kubeadm:node-proxier 50d
kubernetes-dashboard 50d
system:basic-user 50d
system:controller:attachdetach-controller 50d
... ...
system:controller:statefulset-controller 50d
system:controller:ttl-controller 50d
system:discovery 50d
system:kube-controller-manager 50d
system:kube-dns 50d
system:kube-scheduler 50d
system:node 50d
system:node-proxier 50d
weave-net 50d
```


## 三、Dashboard的role和rolebinding

Kubernetes 1.6.x启用RBAC后，诸多周边插件也都推出了适合K8s 1.6.x的manifest描述文件，比如：[weave-net](https://github.com/weaveworks/weave/releases/download/latest_release/weave-daemonset-k8s-1.6.yaml)等。Dashboard的manifest文件中也增加了关于rolebinding的描述，我当初用的是[1.6.1版本](https://raw.githubusercontent.com/kubernetes/dashboard/v1.6.1/src/deploy/kubernetes-dashboard.yaml)，文件内容摘录如下：

```
// kubernetes-dashboard.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
labels:
k8s-app: kubernetes-dashboard
name: kubernetes-dashboard
namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
name: kubernetes-dashboard
labels:
k8s-app: kubernetes-dashboard
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- kind: ServiceAccount
name: kubernetes-dashboard
namespace: kube-system
... ...
```


我们看到在kubernetes-dashboard.yaml中，描述文件新建了一个ClusterRoleBinding：**kubernetes-dashboard**。该binding将ClusterRole: **cluster-admin**授权给了一个ServiceAccount: **kubernetes-dashboard**。我们看看ClusterRole: **cluster-admin**都包含了哪些permission:

```
# kubectl get clusterrole/cluster-admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
annotations:
rbac.authorization.kubernetes.io/autoupdate: "true"
creationTimestamp: 2017-05-30T14:06:39Z
labels:
kubernetes.io/bootstrapping: rbac-defaults
name: cluster-admin
resourceVersion: "11"
selfLink: /apis/rbac.authorization.k8s.io/v1beta1/clusterrolescluster-admin
uid: 331c79dc-4541-11e7-bc9a-12584ec3a8c9
rules:
- apiGroups:
- '*'
resources:
- '*'
verbs:
- '*'
- nonResourceURLs:
- '*'
verbs:
- '*'
```


可以看到，在rules设定中，cluster-admin似乎拥有了“无限”权限。不过注意：这里仅仅授权给了一个service account，并没有授权给user或group。并且这里的**kubernetes-dashboard**是dashboard访问apiserver时使用的(下图右侧流程)，并不是user访问APIServer时使用的。

![img{512x368}](../../assets/1cd44865584c5759.png)


我们需要给登录dashboard或者说apiserver的user(图左侧)进行授权。

## 四、为user: admin进行授权

我们的kube-apiserver的启动参数中包含：

```
- --basic-auth-file=/etc/kubernetes/basic_auth_file
```


也就是说我们访问apiserver使用的是basic auth的身份验证方式，而user恰为admin。而从本文开头的错误现象来看，admin这个user并未得到足够的授权。这里我们要做的就是给admin选择一个合适的clusterrole。但kubectl并不支持查看user的信息，初始的clusterrolebinding又那么多，一一查看十分麻烦。我们知道cluster-admin这个clusterrole是全权限的，我们就来将admin这个user与clusterrole: **cluster-admin** bind到一起：

```
# kubectl create clusterrolebinding login-on-dashboard-with-cluster-admin --clusterrole=cluster-admin --user=admin
clusterrolebinding "login-on-dashboard-with-cluster-admin" created
# kubectl get clusterrolebinding/login-on-dashboard-with-cluster-admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
creationTimestamp: 2017-07-20T08:57:07Z
name: login-on-dashboard-with-cluster-admin
resourceVersion: "5363564"
selfLink: /apis/rbac.authorization.k8s.io/v1beta1/clusterrolebindingslogin-on-dashboard-with-cluster-admin
uid: 686a3f36-6d29-11e7-8f69-00163e1001d7
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
kind: User
name: admin
```


binding后，我们再来访问一下dashboard UI，不出意外的话，熟悉的dashboard界面就会出现在你的眼前。

注：Kubernetes API Server新增了–anonymous-auth选项，允许匿名请求访问secure port。没有被其他authentication方法拒绝的请求即Anonymous requests， 这样的匿名请求的username为”system:anonymous”, 归属的组为”system:unauthenticated”。并且该选线是默认的。这样一来，当采用chrome浏览器访问dashboard UI时很可能无法弹出用户名、密码输入对话框，导致后续authorization失败。为了保证用户名、密码输入对话框的弹出，需要将–anonymous-auth设置为false：


```
// /etc/kubernetes/manifests/kube-apiserver.yaml
- --anonymous-auth=false
```


用curl测试结果如下：

```
$curl -u admin:YOUR_PASSWORD -k https://apiserver_ip:secure_port/
{
"paths": [
"/api",
"/api/v1",
"/apis",
"/apis/apps",
"/apis/apps/v1beta1",
"/apis/authentication.k8s.io",
"/apis/authentication.k8s.io/v1",
"/apis/authentication.k8s.io/v1beta1",
"/apis/authorization.k8s.io",
"/apis/authorization.k8s.io/v1",
"/apis/authorization.k8s.io/v1beta1",
"/apis/autoscaling",
"/apis/autoscaling/v1",
"/apis/autoscaling/v2alpha1",
"/apis/batch",
"/apis/batch/v1",
"/apis/batch/v2alpha1",
"/apis/certificates.k8s.io",
"/apis/certificates.k8s.io/v1beta1",
"/apis/extensions",
"/apis/extensions/v1beta1",
"/apis/policy",
"/apis/policy/v1beta1",
"/apis/rbac.authorization.k8s.io",
"/apis/rbac.authorization.k8s.io/v1alpha1",
"/apis/rbac.authorization.k8s.io/v1beta1",
"/apis/settings.k8s.io",
"/apis/settings.k8s.io/v1alpha1",
"/apis/storage.k8s.io",
"/apis/storage.k8s.io/v1",
"/apis/storage.k8s.io/v1beta1",
"/healthz",
"/healthz/ping",
"/healthz/poststarthook/bootstrap-controller",
"/healthz/poststarthook/ca-registration",
"/healthz/poststarthook/extensions/third-party-resources",
"/healthz/poststarthook/rbac/bootstrap-roles",
"/logs",
"/metrics",
"/swaggerapi/",
"/ui/",
"/version"
]
}
```


微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论