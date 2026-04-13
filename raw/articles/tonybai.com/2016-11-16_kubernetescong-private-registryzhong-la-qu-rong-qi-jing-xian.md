---
title: Kubernetes从Private Registry中拉取容器镜像的方法
url: https://tonybai.com/2016/11/16/how-to-pull-images-from-private-registry-on-kubernetes-cluster/
published: '2016-11-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes从Private Registry中拉取容器镜像的方法

话接上文，在《[使用go-ceph管理Ceph RBD映像](http://tonybai.com/2016/11/09/operate-ceph-rbd-images-with-go-ceph/)》一文中我们提到了，我们需要自建一个ceph rbd api service用于给我的产品控制台提供RESTful API服务接口。这个服务我也是打算放在kubernetes集群中作为一个Service运行的。这两天完成了这个服务开发，并编写完Service的Dockerfile，将镜像build, tag并push到了我们在阿里云的私有镜像库。但在通过kubectl创建这个Service时，我们遇到了 ErrImagePull、ImagePullBackOff等Pod status，通过kubectl describe pod/{MyPod}命令查看，发现下面错误提示：

```
23s 5s 2 {kubelet 10.57.136.60} spec.containers{rbd-rest-api} Warning Failed Failed to pull image "registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest": image pull failed for registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest, this may be because there are no credentials on this request. details: (Error: image xxxx/rbd-rest-api:latest not found)
```


面前这个坑就是Kubernetes集群如何从Private Registry获取容器镜像的问题。关于这个问题，[K8s官方文档](http://kubernetes.io/docs)有较为[详细的说明](http://kubernetes.io/docs/user-guide/images/#using-a-private-registry)，但填过坑的人都知道，那些说明还是远远不够的，实践中你会碰到很多意想不到的问题。这里就来结合实际操作说说K8s与私有容器镜像仓库是如何在一起欢乐的工作的^_^。

#### 一、环境

由于[Kubernetes](http://tonybai.com/tag/kubernetes)和[Docker](http://tonybai.com/tag/docker)都在Active Develop的过程中，两个项目的变动都很快，因此，特定的操作和说明在某些版本是好用的，但对另外一些版本却是不灵光的。这里先把环境确定清楚，避免误导。

```
OS：
Ubuntu 14.04.4 LTS Kernel：3.19.0-70-generic #78~14.04.1-Ubuntu SMP Fri Sep 23 17:39:18 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
Docker：
# docker version
Client:
Version: 1.12.2
API version: 1.24
Go version: go1.6.3
Git commit: bb80604
Built: Tue Oct 11 17:00:50 2016
OS/Arch: linux/amd64
Server:
Version: 1.12.2
API version: 1.24
Go version: go1.6.3
Git commit: bb80604
Built: Tue Oct 11 17:00:50 2016
OS/Arch: linux/amd64
Kubernetes集群：1.3.7
私有镜像仓库：阿里云镜像仓库
Docker镜像：非公共镜像，大家在测试中可以在自己的私有仓库建立自己的测试镜像
registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest
```


Kubernets在文档中描述了几种访问私有仓库的方法，这里挑选了那些可操作的，逐一测试一下。

#### 二、方法1：利用Node上的配置访问Private Registry

在玩Docker时，很多朋友都[搭建过自己的Private Registry](http://tonybai.com/2016/02/26/deploy-a-private-docker-registry/)。Docker访问那些以basic auth方式进行鉴权的Private Registry，只需在本地执行docker login，输入用户名、密码后，就可以自由向Registry Push镜像或pull 镜像到本地了：

```
# docker login registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api
Username: {UserName}
Password:
Login Succeeded
```


在这一过程结束后，Docker实际上会在~/.docker目录下创建一个config.json文件，保存后续与Registry交互过程中所要使用的鉴权串（这个鉴权串只是一个base64编码结果，安全性欠佳^_^）：

```
# cat ~/.docker/config.json
{
"auths": {
"registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api": {
"auth": "xxxxyyyyzzzz"
}
}
}
```


一但Node上有了这个配置，那么K8s就可以通过docker直接访问Private Registry了，这是[K8s文档中与私有镜像仓库交互的第一个方法](http://kubernetes.io/docs/user-guide/images/#using-a-private-registry)。考虑到Pod可以被调度到集群中的任意一个Node上，需要在每个Node上执行上述login操作，或者可以简单地将~/.docker/config.json scp到各个node上的~/.docker目录下。

实际效果如何呢? 我们创建了一个Pod yaml，测试一下是否能run起来：

```
//rbd-rest-api-using-node-config.yaml
apiVersion: v1
kind: Pod
metadata:
name: rbd-rest-api-using-node-config
spec:
containers:
- name: rbd-rest-api-using-node-config
image: registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest
imagePullPolicy: Always
```


我们来创建一下这个Pod并查看pod的创建状态：

```
# kubectl create -f rbd-rest-api-using-node-config.yaml
pod "rbd-rest-api-using-node-config" created
# kubectl get pods
NAME READY STATUS RESTARTS AGE
rbd-rest-api-using-node-config 0/1 ErrImagePull 0 5s
```


通过describe查看Pod失败的详细信息：

```
# kubectl describe pod/rbd-rest-api-using-node-config
... ...
Events:
FirstSeen LastSeen Count From SubobjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
1m 1m 1 {default-scheduler } Normal Scheduled Successfully assigned rbd-rest-api-using-node-config to 10.66.181.146
1m 42s 3 {kubelet 10.66.181.146} spec.containers{rbd-rest-api-using-node-config} Normal Pulling pulling image "registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest"
1m 42s 3 {kubelet 10.66.181.146} spec.containers{rbd-rest-api-using-node-config} Warning Failed Failed to pull image "registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest": image pull failed for registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest, this may be because there are no credentials on this request. details: (Error: image xxxx/rbd-rest-api:latest not found)
1m 42s 3 {kubelet 10.66.181.146} Warning FailedSync Error syncing pod, skipping: failed to "StartContainer" for "rbd-rest-api-using-node-config" with ErrImagePull: "image pull failed for registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest, this may be because there are no credentials on this request. details: (Error: image xxxx/rbd-rest-api:latest not found)"
... ...
```


这个方法对我们的环境并不有效。并且经过多次测试，结果依旧，K8s无法从Private Registry获取我们想要的镜像文件:(。

#### 三、方法2：通过kubectl创建docker-registry的secret

K8s提供的第二种方法是通过kubectl创建一个 docker-registry的secret，并在Pod描述文件中引用该secret以达到从Private Registry Pull Image的目的。

操作之前，我们先删除掉各个Node上的~/.docker/config.json。

执行kubectl create secret docker-registry时需要提供private registry的访问UserName和Password：

```
# kubectl create secret docker-registry registrykey-m2-1 --docker-server=registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api --docker-username={UserName} --docker-password={Password} --docker-email=team@domain.com
secret "registrykey-m2-1" created
# kubectl get secret
NAME TYPE DATA AGE
registrykey-m2-1 kubernetes.io/dockercfg 1 29s
```


secret: registrykey-m2-1创建成功。我们来测试一下引用这个secret对象的Pod是否能Pull Image成功并Run起来。Pod yaml文件如下：

```
//rbd-rest-api-registrykey-m2-1.yaml
apiVersion: v1
kind: Pod
metadata:
name: rbd-rest-api-registrykey-m2-1
spec:
containers:
- name: rbd-rest-api-registrykey-m2-1
image: registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest
imagePullPolicy: Always
imagePullSecrets:
- name: registrykey-m2-1
```


创建Pod，并观察Pod状态：

```
# kubectl create -f rbd-rest-api-registrykey-m2-1.yaml
pod "rbd-rest-api-registrykey-m2-1" created
# kubectl get pods
NAME READY STATUS RESTARTS AGE
rbd-rest-api-registrykey-m2-1 1/1 Running 0 7s
rbd-rest-api-using-node-config 0/1 ImagePullBackOff 0 29m
```


通过describe pod，查看创建的event序列：

```
Events:
FirstSeen LastSeen Count From SubobjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
1m 1m 1 {default-scheduler } Normal Scheduled Successfully assigned rbd-rest-api-registrykey-m2-1 to 10.57.136.60
1m 1m 1 {kubelet 10.57.136.60} spec.containers{rbd-rest-api-registrykey-m2-1} Normal Pulling pulling image "registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest"
1m 1m 1 {kubelet 10.57.136.60} spec.containers{rbd-rest-api-registrykey-m2-1} Normal Pulled Successfully pulled image "registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest"
1m 1m 1 {kubelet 10.57.136.60} spec.containers{rbd-rest-api-registrykey-m2-1} Normal Created Created container with docker id d842565e762d
1m 1m 1 {kubelet 10.57.136.60} spec.containers{rbd-rest-api-registrykey-m2-1} Normal Started Started container with docker id d842565e762d
```


正如我们期望的那样，引用了secret: registrykey-m2-1的Pod成功Run起来了。

如果一个pod中有来自不同私有仓库的不同镜像，我们需要怎么做呢？通过kubectl create secret docker-registry我们一次只能建立一个registrykey，如果要访问两个镜像仓库，我们就需要分别为每个仓库创建一个registrykey。我们再来创建一个registrykey，对应的仓库为：registry.cn-hangzhou.aliyuncs.com/xxxx/test：

```
# kubectl create secret docker-registry registrykey-m2-2 --docker-server=registry.cn-hangzhou.aliyuncs.com/xxxx/test --docker-username={UserName} --docker-password={Password} --docker-email=team@domain.com
secret "registrykey-m2-2" created
root@node1:~/pullimagetest/test# kubectl get secret
NAME TYPE DATA AGE
registrykey-m2-1 kubernetes.io/dockercfg 1 1h
registrykey-m2-2 kubernetes.io/dockercfg 1 6s
```


接下来，我们来建一个包含多个container的Pod：

```
//rbd-rest-api-multi-registrykeys-m2-2.yaml
apiVersion: v1
kind: Pod
metadata:
name: rbd-rest-api-multi-registrykeys-m2-2
spec:
containers:
- name: rbd-rest-api-multi-registrykeys-m2-2
image: registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest
imagePullPolicy: Always
- name: test-multi-registrykeys-m2-2
image: registry.cn-hangzhou.aliyuncs.com/xxxx/test:latest
imagePullPolicy: Always
command:
- "tail"
- "-f"
- "/var/log/bootstrap.log"
imagePullSecrets:
- name: registrykey-m2-1
- name: registrykey-m2-2
```


在secret引用中，我们将两个key都引用了进来。

创建该Pod：

```
# kubectl create -f rbd-rest-api-multi-registrykeys-m2-2.yaml
pod "rbd-rest-api-multi-registrykeys-m2-2" created
# kubectl get pod
NAME READY STATUS RESTARTS AGE
rbd-rest-api-multi-registrykeys-m2-2 2/2 Running 0 5s
```


通过pod的event，我们看看启动的操作顺序：

```
Events:
FirstSeen LastSeen Count From SubobjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
44s 44s 1 {default-scheduler } Normal Scheduled Successfully assigned rbd-rest-api-multi-registrykeys-m2-2 to 10.57.136.60
43s 43s 1 {kubelet 10.57.136.60} spec.containers{rbd-rest-api-multi-registrykeys-m2-2} Normal Pulling pulling image "registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest"
43s 43s 1 {kubelet 10.57.136.60} spec.containers{rbd-rest-api-multi-registrykeys-m2-2} Normal Pulled Successfully pulled image "registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest"
42s 42s 1 {kubelet 10.57.136.60} spec.containers{rbd-rest-api-multi-registrykeys-m2-2} Normal Created Created container with docker id 7c09048a41f6
42s 42s 1 {kubelet 10.57.136.60} spec.containers{rbd-rest-api-multi-registrykeys-m2-2} Normal Started Started container with docker id 7c09048a41f6
42s 42s 1 {kubelet 10.57.136.60} spec.containers{test-multi-registrykeys-m2-2} Normal Pulling pulling image "registry.cn-hangzhou.aliyuncs.com/xxxx/test:latest"
42s 42s 1 {kubelet 10.57.136.60} spec.containers{test-multi-registrykeys-m2-2} Normal Pulled Successfully pulled image "registry.cn-hangzhou.aliyuncs.com/xxxx/test:latest"
42s 42s 1 {kubelet 10.57.136.60} spec.containers{test-multi-registrykeys-m2-2} Normal Created Created container with docker id 9930834fe4a3
42s 42s 1 {kubelet 10.57.136.60} spec.containers{test-multi-registrykeys-m2-2} Normal Started Started container with docker id 9930834fe4a3
```


k8s分别从两个镜像仓库尝试pull image，并且最终都成功了！

#### 四、方法3：通过secret yaml文件创建pull image所用的secret

除了上面通过kubectl可以快捷的创建pull image所用的secret外，我们还可以使用常规的手段-yaml描述文件来创建我们需要的secret资源。

```
//registrykey-m3-1.yaml
apiVersion: v1
kind: Secret
metadata:
name: registrykey-m3-1
namespace: default
data:
.dockerconfigjson: {base64 -w 0 ~/.docker/config.json}
type: kubernetes.io/dockerconfigjson
```


前面说过docker login会在~/.docker下面创建一个config.json文件保存鉴权串，这里secret yaml的.dockerconfigjson后面的数据就是那个json文件的base64编码输出（-w 0让base64输出在单行上，避免折行）。

创建registrykey-m3-1 secret：

```
# kubectl create -f registrykey-m3-1.yaml
secret "registrykey-m3-1" created
# kubectl get secret
NAME TYPE DATA AGE
myregistrykey3 kubernetes.io/dockerconfigjson 1 3h
registrykey-m2-1 kubernetes.io/dockercfg 1 1h
registrykey-m2-2 kubernetes.io/dockercfg 1 23m
registrykey-m3-1 kubernetes.io/dockerconfigjson 1 29s
```


对比后，我们发现通过kubectl和yaml创建的两个registrykey secret的类型略有不同，前者是kubernetes.io/dockercfg，后者是kubernetes.io/dockerconfigjson。

接下来，我们编写一个引用了registrykey-m3-1的Pod：

```
//rbd-rest-api-registrykey-m3-1.yaml
apiVersion: v1
kind: Pod
metadata:
name: rbd-rest-api-registrykey-m3-1
spec:
containers:
- name: rbd-rest-api-registrykey-m3-1
image: registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest
imagePullPolicy: Always
imagePullSecrets:
- name: registrykey-m3-1
```


创建Pod：

```
# kubectl create -f rbd-rest-api-registrykey-m3-1.yaml
pod "rbd-rest-api-registrykey-m3-1" created
# kubectl get pods
NAME READY STATUS RESTARTS AGE
rbd-rest-api-registrykey-m3-1 1/1 Running 0 8s
```


创建成功。

那么这种方法如何应对含有来自多个镜像仓库container的Pod的呢？这里的思路与方法2略有不同。我们不需要创建并引用两个或多个secret，而是创建一个可以访问多个私有镜像仓库的secret，我们需要将多个镜像仓库的访问鉴权串都放到~/.docker/config.json中：

按照方法1的介绍，我们先login registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api，得到config.json如下：

```
{
"auths": {
"registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api": {
"auth": "....省略...."
}
}
}
```


我们再login registry.cn-hangzhou.aliyuncs.com/xxxx/test，得到config.json如下：

```
{
"auths": {
"registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api": {
"auth": "....省略...."
},
"registry.cn-hangzhou.aliyuncs.com/xxxx/test": {
"auth": "....省略...."
}
}
}
```


我们看到Docker自动将新login的private registry的鉴权串merge到了同一个config.json中了。现在我们基于该包含了两个库鉴权串的config.json创建一个新secret：registrykey-m3-2：

```
//registrykey-m3-2.yaml
apiVersion: v1
kind: Secret
metadata:
name: registrykey-m3-2
namespace: default
data:
.dockerconfigjson: {base64 -w 0 ~/.docker/config.json}
type: kubernetes.io/dockerconfigjson
```


创建secret: registrykey-m3-2

```
# kubectl create -f registrykey-m3-2.yaml
secret "registrykey-m3-2" created
# kubectl get secrets
NAME TYPE DATA AGE
registrykey-m2-1 kubernetes.io/dockercfg 1 1h
registrykey-m2-2 kubernetes.io/dockercfg 1 42m
registrykey-m3-1 kubernetes.io/dockerconfigjson 1 19m
registrykey-m3-2 kubernetes.io/dockerconfigjson 1 6s
```


我们编辑一个包含两个容器，引用secret “registrykey-m3-2″ 的Pod yaml：

```
//rbd-rest-api-multi-registrykeys-m3-2.yaml
apiVersion: v1
kind: Pod
metadata:
name: rbd-rest-api-multi-registrykeys-m3-2
spec:
containers:
- name: rbd-rest-api-multi-registrykeys-m3-2
image: registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest
imagePullPolicy: Always
- name: test-multi-registrykeys-m3-2
image: registry.cn-hangzhou.aliyuncs.com/xxxx/test:latest
imagePullPolicy: Always
command:
- "tail"
- "-f"
- "/var/log/bootstrap.log"
imagePullSecrets:
- name: registrykey-m3-2
```


创建该Pod：

```
# kubectl create -f rbd-rest-api-multi-registrykeys-m3-2.yaml
pod "rbd-rest-api-multi-registrykeys-m3-2" created
# kubectl get pod
NAME READY STATUS RESTARTS AGE
rbd-rest-api-multi-registrykeys-m3-2 2/2 Running 0 4s
```


Pod创建成功！

#### 五、调用API创建registrykey secret

对比了方法2和方法3，方法2更简洁，方法3更强大。但在任何一个产品中，secret都不应该是手动创建的，在这种情况下，[API](http://kubernetes.io/docs/api-reference/v1/operations/)创建[registrykey secret](http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_secret)便是必经之路。一旦选择通过API创建，我们显然将依仗着方法2中的原理，将config.json中的内容通过API请求的Body Post给K8s api server。

如何在远端构建出config.json的内容呢继而构建出secret yaml中.dockerconfigjson的值数据呢？我们发现config.json套路中，唯一不确定的就是每个private repository下的auth串，那么这个串是啥呢？你大可base64 -d一下：

```
# echo -n "VXNlck5hbWU6UGFzc3dvcmQ="|base64 -d
UserName:Password
```


没错，实质上这个auth串就是UserName:Password的base64编码值。因此，你首先要用某个仓库的UserName和Password按照’UserName:Password’格式进行base64编码，利用编码的结果值构造json内容，比如：

```
{
"auths": {
"registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api": {
"auth": "VXNlck5hbWU6UGFzc3dvcmQ="
}
}
```


然后对这段json数据再做base64编码，所得到的值就是secret yaml中的.dockerconfigjson的值数据。至此，我们来通过API创建一个secret：

```
$ curl -v -H "Content-type: application/json" -X POST -d ' {
"apiVersion": "v1",
"kind": "Secret",
"metadata": {
"name": "registrykey-m4-1",
"namespace": "default"
},
"data": {
".dockerconfigjson": "{cat ~/.docker/config.json |base64 -w 0}"
},
"type": "kubernetes.io/dockerconfigjson"
}' http://10.57.136.60:8080/api/v1/namespaces/default/secrets
# kubectl get secret
NAME TYPE DATA AGE
registrykey-m2-1 kubernetes.io/dockercfg 1 2h
registrykey-m2-2 kubernetes.io/dockercfg 1 1h
registrykey-m3-1 kubernetes.io/dockerconfigjson 1 43m
registrykey-m3-2 kubernetes.io/dockerconfigjson 1 24m
registrykey-m4-1 kubernetes.io/dockerconfigjson 1 18s
```


基于registrykey-m4-1，我们启动一个Pod：

```
//rbd-rest-api-registrykey-m4-1.yaml
apiVersion: v1
kind: Pod
metadata:
name: rbd-rest-api-registrykey-m4-1
spec:
containers:
- name: rbd-rest-api-registrykey-m4-1
image: registry.cn-hangzhou.aliyuncs.com/xxxx/rbd-rest-api:latest
imagePullPolicy: Always
imagePullSecrets:
- name: registrykey-m4-1
# kubectl create -f rbd-rest-api-registrykey-m4-1.yaml
pod "rbd-rest-api-registrykey-m4-1" created
# kubectl get pod
NAME READY STATUS RESTARTS AGE
rbd-rest-api-registrykey-m4-1 1/1 Running 0 5s
```


Pod创建成功！

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

抱歉，暂停评论。