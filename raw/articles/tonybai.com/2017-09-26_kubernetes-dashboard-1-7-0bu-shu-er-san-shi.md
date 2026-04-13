---
title: Kubernetes Dashboard 1.7.0部署二三事
url: https://tonybai.com/2017/09/26/some-notes-about-deploying-kubernetes-dashboard-1-7-0/
published: '2017-09-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes Dashboard 1.7.0部署二三事

由于开发的平台要进行内部公开测试，我们这周在公司内部私有云搭建了一套平台。涉及到[Kubernetes](http://tonybai.com/tag/kubernetes)相关的基础软件，由我来部署。Kubernetes以及其相关组件都在积极的开发中，版本更新也很快。截至本文撰写时，K8s发布最新稳定版是[v1.7.6](https://github.com/kubernetes/kubernetes/releases/tag/v1.7.6)，而与之配套的[Dashboard](https://github.com/kubernetes/dashboard)则是[v1.7.0](https://github.com/kubernetes/dashboard/releases/tag/v1.7.0)。

最初在部署规划时，我选择了Kubernetes v1.7.6+ [dashboard v1.6.3](https://github.com/kubernetes/dashboard/releases/tag/v1.6.3)的组合。之前K8s v1.7.3的稳定让我对使用最新Release版有一些信心，但dashboard v1.7.0则是三天前刚发布的，看[dashboard](http://tonybai.com/tag/dashboard/)的commit log，之前还大规模revert了一次。因此，我保守的选择了v1.6.3。

## 一、但Dashboard v1.6.3与Kubernetes 1.7.6似乎不匹配

在[Kubernetes Dashboard](http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/)的兼容性矩阵中，我们能看到dashboard 1.6.x与k8s 1.7.x的兼容性是一个问号。最新dashboard兼容性矩阵点击[这里](https://github.com/kubernetes/dashboard/wiki/Compatibility-matrix)可以找到：

![img{512x368}](../../assets/ed85a6c1a11508b4.png)


也就是说由于K8S API可能的变动，Dashboard 1.6.x的某些功能可能无法使用。之前我在阿里云上的测试环境中使用的是[k8s 1.7.3+dashboard 1.6.3的组合](http://tonybai.com/2017/08/09/fix-kube-apiserver-restart-exceptionally-in-k8s-1-7-3/)，我需要的功能均可以使用。因此这里我首先尝试了dashboard v1.6.3。

安装过程不赘述。我依旧通过kube-apiserver暴露服务的方式来访问dasbboard，kube-apiserver采用basic auth的身份验证方式。我尝试在浏览器中访问下面路径：

```
https://{kube-apiserver}:6443/ui
```


在浏览器弹出的身份验证对话框中输入user/password后，url跳转到：

```
https://{kube-apiserver}:6443/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy
```


不过等了许久，浏览器页面依旧一片空白。Dashboard的内容并未鲜露出来。通过chrome浏览器自带的”检查”功能，发现一些静态资源（css、js）的get请求都返回404错误。由于时间有限，没有细致查问题所在。我打算用Dashboard 1.7.0试试。

## 二、采用Dashboard v1.7.0

1.7.0版本dashboard主要强化了安全性，增加了登录页面和相关菜单项，并增加了一个kubernetes-dashboard-init-amd64 init容器。我们无需再依赖[浏览器弹框](http://tonybai.com/2017/07/20/fix-cannot-access-dashboard-in-k8s-1-6-4/)了。dashboard调整了源码目录结构，安装1.7.0需要执行下面命令：

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
```


安装后，我们继续按原有方式访问dashboard，即访问https://{kube-apiserver}:6443/ui，但我们得到如下错误信息：

```
Error: 'malformed HTTP response "\x15\x03\x01\x00\x02\x02"'
Trying to reach: 'http://10.40.0.5:8443/'
```


回头再看dashboard的wiki，发现其告知的通过kube-apiserver访问dashboard的url如下：

```
https://{kube-apiserver}:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy
```


访问该地址后，我们在浏览器中看到如下登录页面：

![img{512x368}](../../assets/293093c8496c6a77.png)


dashboard v1.7.0默认支持两种身份校验登录方式：kubeconfig和token两种。我们说说token这种方式。点击选择:Token单选框，提示你输入token。token从哪里获取，我们从来没有生成过token？其实当前K8s中已经有了很多token：

```
root@ubuntu-k8s-1:~# kubectl get secret -n kube-system
NAME TYPE DATA AGE
attachdetach-controller-token-8pps2 kubernetes.io/service-account-token 3 4d
bootstrap-signer-token-jfj4q kubernetes.io/service-account-token 3 4d
... ....
service-controller-token-9zqbz kubernetes.io/service-account-token 3 4d
statefulset-controller-token-m7shd kubernetes.io/service-account-token 3 4d
token-cleaner-token-sfvm8 kubernetes.io/service-account-token 3 4d
ttl-controller-token-dxjz9 kubernetes.io/service-account-token 3 4d
weave-net-token-zfgbp kubernetes.io/service-account-token 3 4d
```


想看那个secret对应的token，就执行kubectl describe secret/{token_name} -n kube-system。比如，我们查看一下service-controller-token-9zqbz 对应的token是多少：

```
root@ubuntu-k8s-1:~# kubectl describe secret/service-controller-token-9zqbz -n kube-system
Name: service-controller-token-9zqbz
Namespace: kube-system
Labels: <none>
Annotations: kubernetes.io/service-account.name=service-controller
kubernetes.io/service-account.uid=907b4a3b-9f59-11e7-a3ea-0650cc001a5b
Type: kubernetes.io/service-account-token
Data
====
ca.crt: 1025 bytes
namespace: 11 bytes
token: eyJhbG...QH9rfu7QI81QJg
```


现在你可以把上面token key对应那一长串copy到dashboard的token输入框中，点击：signin。即可登录。不过由于token对应的Service account的权限不同，即使进入dashboard，也干不了啥，甚至是啥也不能干。

## 三、让Dashboard v1.7.0支持basic auth login方式

我们要用basic auth方式登录dashboard，需要对kubernetes-dashboard.yaml进行如下修改：

```
args:
- --tls-key-file=/certs/dashboard.key
- --tls-cert-file=/certs/dashboard.crt
- --authentication-mode=basic <---- 添加这一行
```


然后apply一下该yaml文件，等dashboard pod重新创建ok后，我们就可以user、password方式登录dashboard了：

![img{512x368}](../../assets/214bc7574cf29f9f.png)


## 四、集成heapster

heapster当前最新版本v1.4.2，我们采用influxdb作为后端，因此使用的是下面的一些yaml文件：

```
root@ubuntu-k8s-1:~/k8s176-install/dashboard/heapster-1.4.2/deploy/kube-config/influxdb# ls
grafana.yaml heapster.yaml influxdb.yaml
```


不过在创建这些pod之前，我们先要创建一些权限绑定：

```
root@ubuntu-k8s-1:~/k8s176-install/dashboard/heapster-1.4.2/deploy/kube-config/rbac# kubectl create -f heapster-rbac.yaml
clusterrolebinding "heapster" created
```


heapster使用的grafana是v4.2.0版本，该版本有一个[bug](https://github.com/kubernetes/heapster/issues/1709)，一旦运行后，会出现类似如下的错误：

```
# kubectl logs -f monitoring-grafana-762361155-p9vwj -n kube-system
Starting a utility program that will configure Grafana
Starting Grafana in foreground mode
t=2017-08-09T06:10:57+0000 lvl=crit msg="Failed to parse /etc/grafana/grafana.ini, open /etc/grafana/grafana.ini: no such file or directory%!(EXTRA []interface {}=[])"
```


我们需要将grafana升级到v4.4.1版本。修改上面的heapster-1.4.2/deploy/kube-config/influxdb/grafana.yaml:

```
spec:
containers:
- name: grafana
image: gcr.io/google_containers/heapster-grafana-amd64:v4.4.1
```


创建heapster:

```
root@ubuntu-k8s-1:~/k8s176-install/dashboard/heapster-1.4.2/deploy/kube-config# kubectl create -f influxdb/
deployment "monitoring-grafana" created
service "monitoring-grafana" created
serviceaccount "heapster" created
deployment "heapster" created
service "heapster" created
deployment "monitoring-influxdb" created
service "monitoring-influxdb" created
```


dashboard在页面上增加了一些新的展示组件，就像下面这样的：

![img{512x368}](../../assets/d8c8046fd5345bf2.png)


**更多内容可以通过我在慕课网开设的实战课程 《Kubernetes实战 高可用集群搭建、配置、运维与应用》学习。**

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017 – 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我的kubernetes是1.7.3,网络用calico,用过1.6和1.7的bashboard，发现在dashboard部署后二十分左右，会出现dashboard占用cpu100%的情况，日志查看正常，不知你是否出现过。

我看了一下，在k8s1.7.3和dashboard 1.6.3的环境中，dashboard cpu占用很少。但是在最新的k8s 1.7.6和dashboard 1.7的环境里，dashboard占用cpu很高：99%：

PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND

596 root 20 0 51928 38744 20560 S 99.0 1.0 1477:39 dashboard

我后续查查看是什么原因。多谢提醒。

是官方镜像的问题,v1.7.1已经解决了CPU占用过高的bug.

谢谢提醒。经实际操作：升级到dashboard v1.7.1之后，cpu占用高的问题的确得到解决了。

你好，我用的k8s版本是1.7.5，apiserver验证机制，好像不能添加basic auth，我添加后，apiserver无法启动，我也想用dashboard采用basic auth验证，但apiserver好像无法使用basic auth这种机制了，默认是证书验证，

可以看看这个《解决Kubernetes 1.7.3 kube-apiserver频繁异常重启的问题》http://tonybai.com/2017/08/09/fix-kube-apiserver-restart-exceptionally-in-k8s-1-7-3/ authenticating机制是“或”的关系，k8s apiserver 会 逐一试basic auth, client crt, bearer token等机制，有一个方式验证通过，即可通过。

大神能提供下国内1.7.1的镜像地址吗？

抱歉，我都是直接使用国外默认的镜像。在国内没找到可用的且持续维护的k8s相关的公共镜像仓库。

请教一个问题 K8s 是1.7.3 dashboard是v1.7.1 连接apiserver的时候 报这个错误 (e.g., it has invalid apiserver certificates or service accounts configuration) or the –apiserver-host param points to a server that does not exist. Reason: Get https://10.0.0.110:6443/version: x509: failed to load system roots and no roots provided

问题我没遇到过，不过翻了一下dashboard的issue list，似乎这个issue的问题和你遇到的相同：https://github.com/kubernetes/dashboard/issues/1287 你可以参考一下。

你好！ 我按照你这篇文章部署成功了，但在使用 basic auth login方式登录的时候遇到了问题。用户名和密码我无从得知，是需要在哪里配置吗？ 还是有默认的。

需要修改apiserver的启动参数，添加basic auth启动参数，比如：–basic-auth-file=/etc/kubernetes/basic_auth_file ，basci_auth_file是你自建的。具体可以参考我另外一篇文章：《Kubernetes集群Dashboard插件安装》http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/

做basic auth的时候修改api-server 添加basic auth apiserver重启报错。应该参数不认。我的是1.8的k8s，用token登陆 点sign in 很久没反应。。看pod日志就提示了一个返回值200.。。 Outcoming response to 192.168.229.0:49690 with 200 status code

补充一下。。anonymous可以进得去。。也就是skip

请问下1.7的支持中文了吗，还是我看错了？

我们的1.7.x dashboard页面上大部分左栏中的菜单项显示的是中文。不过这个不是配置的，默认安装后，就是这样的。

basic auth方式登录dashboard 支持配置账户名和密码吗

老版本的kubernetes dashboard都是不支持配置用户名密码的，所以我才用访问kube-apserver的basic auth方式来做一次鉴权，放置k8s dashboard裸奔。不过最新的版本的k8s dashboard(好像是从1.7.1开始)，k8s dashboard增加了login 鉴权页面。

嗯。是的！可以调出这个认证界面 但是不知道在那里面配置这个账户名和密码 ，请大神指教

可以看看这篇：《Kubernetes集群Dashboard插件安装》http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/ dashboard版本虽然不同，原理相同。

我安装的dashboard 1.8，集群是k8s 1.8，启动参数不管是–auto-generate-certificates还是指定–tls-key-file=dashboard.key、–tls-cert-file=dashboard.crt，使用k8s自动创建的secret都无法登入，只skip进入，不知道是哪里出问题，你安装过程中有没有出现这样的问题。

我目前还没试过1.8版本。