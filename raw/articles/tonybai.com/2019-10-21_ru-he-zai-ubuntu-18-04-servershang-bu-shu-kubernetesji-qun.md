---
title: 如何在Ubuntu 18.04 Server上部署Kubernetes集群
url: https://tonybai.com/2019/10/21/how-to-deploy-a-kubernetes-cluster-with-ubuntu-server-18-04/
published: '2019-10-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 如何在Ubuntu 18.04 Server上部署Kubernetes集群

如今，你几乎不可避免地会听到来自[Kubernetes](https://tonybai.com/tag/kubernetes)的发声，你更没有充分的理由拒绝去听。 一旦一切就绪，这个强大的容器编排工具将以您难以想象的敏捷性来扩展您的操作。

为了实际使用Kubernetes进行部署和管理容器，您首先必须[创建Kubernetes服务器集群](https://tonybai.com/2018/06/13/setup-efk-on-kubernetes-1-10-3-in-the-hard-way/)。 一旦集群建立后，您就能够部署，扩展和管理您的容器化应用程序了。

在[Ubuntu](https://tonybai.com/tag/ubuntu) Server 18.04的帮助下，我将引导您完成此过程。 我们至少需要2个[Ubuntu Server 18.04](http://releases.ubuntu.com/18.04/)实例和一个具有sudo特权的用户帐户才能完成此工作。 您需要确保所有计算机都已做完更新（使用sudo apt-get update和sudo apt-get upgrade -y命令）。

还需要一些时间，大约30分钟左右。

我将在两台机器上进行示范操作：一个master节点和一个worker节点。

我们开始吧！

## 安装[Docker](https://tonybai.com/tag/docker)

master节点和worker节点上都需要进行下面的操作。

我们要做的第一件事就是安装Docker。要安装docker，先要登录到Server上，输入并执行下面命令：

```
sudo apt-get install docker.io
```


一旦docker安装成功后，你需要将你的账号添加到docker组中(否则，每次运行docker命令，都需要带上sudo，这可能导致安全问题）。执行下面命令将你的账号添加到docker组中：

```
sudo usermod -aG docker $USER
```


登出并重新登录，这样上述配置变化才能生效。

启动并使能docker后台驻留程序：

```
sudo systemctl start docker
sudo systemctl enable docker
```


现在我们需要在所有节点上安装Kubernetes了。首先，我们通过下面命令添加Kubernetes GPG key：

```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
```


如果没有安装curl，可以通过下面命令安装：

```
sudo apt-get install curl -y
```


接下来，添加必要的仓库：

```
sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
```


通过下面命令安装必要的软件：

```
sudo apt-get install kubeadm kubelet kubectl -y
```


上面的命令将自动安装目标软件以及它们的依赖。

## 主机名

为了让后续操作更简单，我们通过下面命令为每个server赋予新的主机名。

```
sudo hostnamectl set-hostname HOSTNAME
```


HOSTNAME是主机的名字


你可以使用下面这些主机名：

- kubemaster
- node1
- node2
- node3
- 其他等等

登出并重新登录。最后，将主机名映射为IP地址。通过下面命令打开host文件并编辑：

```
sudo nano /etc/hosts
```


在文件末尾附加类似下面的内容（保证你的主机名与其正确的ip一一对应）：

```
192.168.1.218 kubemaster
192.168.1.219 kubenode1
192.168.1.220 kubenode2
```


关闭并保存文件。

## 关闭Swap

要运行kubernetes，你必须首先关闭swap。我们可以通过下面命令来做到这一点：

```
sudo swapoff -a
```


如果要使修改永久生效(否则，下次重启时，swap会重新启用)，执行下面命令：

```
sudo nano /etc/fstab
```


在fstab文件中，将swap入口注释掉，如下图：

![img{512x368}](../../assets/4d3ed4dddef7bf47.jpg)


图: 通过fstab关闭swap

## 初始化Master

接下来，我们通过下面命令来初始化master节点。

```
sudo kubeadm init --pod-network-cidr=192.168.1.90/16
```


初始化结束后，你将看到将worker node加入集群的精确命令(如下图)，保证要拷贝下该命令：

![img{512x368}](../../assets/8ebb957159b8ff89.jpg)


图: 将worker node加入master的命令

仅在master上创建下面目录：

```
mkdir -p $HOME/.kube
```


将相应的配置你文件拷贝到该目录下：

```
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
```


赋予配置文件适当的权限：

```
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```


## 部署Pod网络

在将worker加入到master之前，你必须先部署pod网络(否则，所有事情都无法按照预期那样正常工作）。[Flannel](https://tonybai.com/2017/01/17/understanding-flannel-network-for-kubernetes/)是可选的Pod网络之一。我们通过下面命令安装它（仅在master运行下面命令)：

```
sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```


## 将worker node加入到master

现在我们具备将worker node加入master的条件了。登录到worker node上，执行类型下面的命令：

```
sudo kubeadm join 192.168.1.190:6443 --token bzbwl4.ll5o9x3jjhqqwofa --discovery-token-ca-cert-hash sha256:ecb0223a05be3502c2d102f3e56104b10fcd105430eb723d3b3e816618323d73
```


在每个worker node上执行join命令。一旦join命令执行成功，返回master node执行下面命令：

```
kubectl get nodes
```


你可以看到所有加入到集群的worker node列表：

![img{512x368}](../../assets/ddcae6f872dcc77a.jpg)


图: 我们的node已经加入并处于ready状态

到此，kubernetes集群已经就绪并可以部署你的第一个容器化的应用或服务了。不要忘了，如果你要加入更多worker node（提高伸缩能力），你需要join命令。如果你忘记保存之前那个join命令了，你可以在任何时候通过下面命令获取它：

```
kubeadm token create --print-join-command
```


上面命令将输出join命令，在你的新worker node上执行它即可。

文本首次发表在[慕课网](https://www.imooc.com/article/293956)上。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

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