---
title: 基于Harbor和CephFS搭建高可用Private Registry
url: https://tonybai.com/2017/06/09/setup-a-high-availability-private-registry-based-on-harbor-and-cephfs/
published: '2017-06-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 基于Harbor和CephFS搭建高可用Private Registry

我们有给客户搭建私有容器仓库的需求。开源的私有容器registry可供选择的不多，除了docker官方的[distribution](https://github.com/docker/distribution)之外，比较知名的是VMware China出品的[Harbor](https://github.com/vmware/harbor)，我们选择了harbor。

harbor在[docker distribution](https://github.com/docker/distribution)的基础上增加了一些安全、访问控制、管理的功能以满足企业对于镜像仓库的需求。harbor以[docker-compose](https://github.com/docker/compose)的规范形式组织各个组件，并通过docker-compose工具进行启停。

不过，harbor默认的安装配置是针对single node的，要想做得可靠性高一些，我们需要自己探索一些可行的方案。本文将结合harbor和[CephFS](http://tonybai.com/tag/cephfs)搭建一个满足企业高可用性需求的private registry。

## 一、实验环境

这里用两台阿里云ECS作为harbor的工作节点：

```
node1: 10.47.217.91
node2: 10.28.61.30
```


两台主机运行的都是[Ubuntu](http://tonybai.com/tag/ubuntu) 16.04.1 LTS (GNU/Linux 4.4.0-58-generic x86_64)，使用root用户。

[docker版本](http://tonybai.com/tag/docker)与docker-compose的版本如下：

```
# docker version
Client:
Version: 1.12.5
API version: 1.24
Go version: go1.6.4
Git commit: 7392c3b
Built: Fri Dec 16 02:42:17 2016
OS/Arch: linux/amd64
Server:
Version: 1.12.5
API version: 1.24
Go version: go1.6.4
Git commit: 7392c3b
Built: Fri Dec 16 02:42:17 2016
OS/Arch: linux/amd64
# docker-compose -v
docker-compose version 1.12.0, build b31ff33
```


[ceph](http://tonybai.com/tag/ceph)版本如下：

```
# ceph -v
ceph version 10.2.7
```


ceph的安装和配置可参考[这里](http://tonybai.com/2017/05/08/mount-cephfs-acrossing-nodes-in-kubernetes-cluster/)。

## 二、方案思路

首先，从部署上说，我们需要的Private Registry是独立于[k8s cluster](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)存在的，即在k8s cluster外部，其存储和管理的镜像供k8s cluster 组件以及运行于k8s cluster上的应用使用。

其次，企业对registry有高可用需求，但我们也要有折中，我们的目标并不是理想的完全高可用，那样投入成本可能有些高。一般企业环境下更注重数据安全。因此首要保证harbor的数据安全，这样即便harbor实例宕掉，保证数据依然不会丢失即可。并且生产环境下registry的使用很难称得上高频，对镜像仓库的性能要求也没那么高。这种情况下，harbor的高可用至少有两种方案：

- 多harbor实例共享后端存储
- 多harbor实例相互数据同步（通过配置两个harbor相互复制镜像数据）

harbor原生支持双实例的镜像数据同步。不过这里我们采用第一种方案：即多harbor实例共享后端存储，因为我们有现成的cephfs供harbor使用。理想的方案示意图如下：

![img{512x368}](../../assets/49de979e83a01d5b.png)


- 每个安放harbor实例的node都mount cephfs；
- 每个node上的harbor实例（包含组件：ui、db、registry等）都volume mount node上的cephfs mount路径；
- 通过Load Balance将request流量负载到各个harbor实例上。

但这样做可行么？如果这么做，Harbor实例里的mysql container就会“抱怨”：

```
May 17 22:45:45 172.19.0.1 mysql[12110]: 2017-05-17 14:45:45 1 [ERROR] InnoDB: Unable to lock ./ibdata1, error: 11
May 17 22:45:45 172.19.0.1 mysql[12110]: 2017-05-17 14:45:45 1 [Note] InnoDB: Check that you do not already have another mysqld process using the same InnoDB data or log files.
```


MySQL多个实例无法共享一份mysql数据文件。

那么，我们会考虑将harbor连接的mysql放到外面来，使用external database；同时考虑到session共享，我们还需要增加一个存储session信息的redis cluster，这样一来，方案示意图变更如下：

![img{512x368}](../../assets/05ffe742c4b5e5df.png)


图中的mysql、redis你即可以用cluster，也可以用单点，还是看你的需求和投入。如果你具备现成的mysql cluster和redis cluster，那么直接用就好了。但是如果你没有，并且你还不想投入这么多(尤其是搞mysql cluster)，那么用单点就好了。考虑到数据安全，可以将单点mysql的数据存储在cephfs上，如果你已经有了现成的cephfs。

## 三、在一个node上安装Harbor

### 1、初装步骤

以一个node上的Harbor安装为例，harbor提供了详细的[安装步骤文档](https://github.com/vmware/harbor/blob/master/docs/installation_guide.md)，我们按照步骤逐步进行即可(这里我使用的是1.1.0版本，截至目前为止的最新稳定版本为1.1.1版本)：

```
~/harbor-install# wget -c https://github.com/vmware/harbor/releases/download/v1.1.0/harbor-offline-installer-v1.1.0.tgz
~/harbor-install# tar zxvf harbor-offline-installer-v1.1.0.tgz
~/harbor-install/harbor# ls -F
common/ docker-compose.notary.yml docker-compose.yml harbor.cfg harbor.v1.1.0.tar.gz install.sh* LICENSE NOTICE prepare*
~/harbor-install/harbor./install.sh
[Step 0]: checking installation environment ...
Note: docker version: 1.12.5
Note: docker-compose version: 1.12.0
[Step 1]: loading Harbor images ...
... ...
[Step 2]: preparing environment ...
Generated and saved secret to file: /data/secretkey
Generated configuration file: ./common/config/nginx/nginx.conf
Generated configuration file: ./common/config/adminserver/env
Generated configuration file: ./common/config/ui/env
Generated configuration file: ./common/config/registry/config.yml
Generated configuration file: ./common/config/db/env
Generated configuration file: ./common/config/jobservice/env
Generated configuration file: ./common/config/jobservice/app.conf
Generated configuration file: ./common/config/ui/app.conf
Generated certificate, key file: ./common/config/ui/private_key.pem, cert file: ./common/config/registry/root.crt
The configuration files are ready, please use docker-compose to start the service.
[Step 3]: checking existing instance of Harbor ...
[Step 4]: starting Harbor ...
Creating network "harbor_harbor" with the default driver
Creating harbor-log
Creating harbor-db
Creating registry
Creating harbor-adminserver
Creating harbor-ui
Creating nginx
Creating harbor-jobservice
ERROR: for proxy Cannot start service proxy: driver failed programming external connectivity on endpoint nginx (fdeb3e538d5f8d714ea5c79a9f3f127f05f7ba5d519e09c4c30ef81f40b2fe77): Error starting userland proxy: listen tcp 0.0.0.0:80: bind: address already in use
```


harbor实例默认的监听端口是80，但一般node上的80口都会被占用，因此我们需要修改一个端口号。注意：此时harbor仅启动成功了一些container而已，尚无法正常工作。

### 2、修改harbor proxy组件的listen端口

harbor的proxy组件就是一个nginx，通过nginx这个反向代理，将不同的服务请求分发到内部其他组件中去。nginx默认监听node的80端口，我们用8060端口替代80端口需要进行两处配置修改：

```
1、harbor.cfg
hostname = node_public_ip:8060
2、docker-compose.yml
proxy:
image: vmware/nginx:1.11.5-patched
container_name: nginx
restart: always
volumes:
- ./common/config/nginx:/etc/nginx:z
networks:
- harbor
ports:
- 8060:80 <--- 修改端口映射
- 443:443
- 4443:4443
```


由于我们修改了harbor.cfg文件，我们需要重新prepare一下，执行下面命令：

```
# docker-compose down -v
Stopping harbor-jobservice ... done
Stopping nginx ... done
Stopping harbor-ui ... done
Stopping harbor-db ... done
Stopping registry ... done
Stopping harbor-adminserver ... done
Stopping harbor-log ... done
Removing harbor-jobservice ... done
Removing nginx ... done
Removing harbor-ui ... done
Removing harbor-db ... done
Removing registry ... done
Removing harbor-adminserver ... done
Removing harbor-log ... done
Removing network harbor_harbor
# ./prepare
Clearing the configuration file: ./common/config/nginx/nginx.conf
Clearing the configuration file: ./common/config/ui/env
Clearing the configuration file: ./common/config/ui/app.conf
Clearing the configuration file: ./common/config/ui/private_key.pem
Clearing the configuration file: ./common/config/adminserver/env
Clearing the configuration file: ./common/config/jobservice/env
Clearing the configuration file: ./common/config/jobservice/app.conf
Clearing the configuration file: ./common/config/db/env
Clearing the configuration file: ./common/config/registry/config.yml
Clearing the configuration file: ./common/config/registry/root.crt
loaded secret from file: /mnt/cephfs/harbor/data/secretkey
Generated configuration file: ./common/config/nginx/nginx.conf
Generated configuration file: ./common/config/adminserver/env
Generated configuration file: ./common/config/ui/env
Generated configuration file: ./common/config/registry/config.yml
Generated configuration file: ./common/config/db/env
Generated configuration file: ./common/config/jobservice/env
Generated configuration file: ./common/config/jobservice/app.conf
Generated configuration file: ./common/config/ui/app.conf
Generated certificate, key file: ./common/config/ui/private_key.pem, cert file: ./common/config/registry/root.crt
The configuration files are ready, please use docker-compose to start the service.
# docker-compose up -d
Creating network "harbor_harbor" with the default driver
Creating harbor-log
Creating harbor-adminserver
Creating registry
Creating harbor-db
Creating harbor-ui
Creating harbor-jobservice
Creating nginx
```


我们可以通过docker-compose ps命令查看harbor组件的状态：

```
# docker-compose ps
Name Command State Ports
--------------------------------------------------------------------------------------------------------------------------------
harbor-adminserver /harbor/harbor_adminserver Up
harbor-db docker-entrypoint.sh mysqld Up 3306/tcp
harbor-jobservice /harbor/harbor_jobservice Up
harbor-log /bin/sh -c crond && rm -f ... Up 127.0.0.1:1514->514/tcp
harbor-ui /harbor/harbor_ui Up
nginx nginx -g daemon off; Up 0.0.0.0:443->443/tcp, 0.0.0.0:4443->4443/tcp, 0.0.0.0:8060->80/tcp
registry /entrypoint.sh serve /etc/ ... Up 5000/tcp
```


如果安全组将8060端口打开，通过访问:http://node_public_ip:8060，你将看到如下harbor的web页面：

![img{512x368}](../../assets/b32305b3b775cce4.png)


我们可以通过harbor内置的默认用户名和密码admin/Harbor12345登录harbor ui。当然，我们更重要的是通过cmdline访问harbor，push和pull image。如果这时你直接尝试docker login harbor_url，你可能会得到如下错误日志：

```
# docker login -u admin -p Harbor12345 node_public_ip:8060
Error response from daemon: Get https://node_public_ip:8060/v1/users/: http: server gave HTTP response to HTTPS client
```


这是因为docker默认采用https访问registry，因此我们需要在docker engine的配置中，添加–insecure-registry option。关于ubuntu 16.04下docker配置的问题，请参考[这里](http://tonybai.com/2016/12/27/when-docker-meets-systemd/)：

```
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4 --registry-mirror=https://xxxxx.mirror.aliyuncs.com --insecure-registry=node_public_ip:8060"
```


重启docker engine后尝试再次登录harbor：

```
docker login -u admin -p Harbor12345 node_public_ip:8060
Login Succeeded
```


一旦docker client login ok，我们就可以通过docker client对harbor中的相关repository进行操作了。

## 四、挂载路径修改

默认情况下，harbor将数据volume挂载到主机的/data路径下面。但由于我们采用ceph共享存储保证数据的高可用，需要修改harbor组件内容器的挂载路径，将其mount到共享存储挂载node上的路径：/mnt/cephfs/harbor/data/。对比两个路径，可以看出前缀由”/”变为了”/mnt/cephfs/harbor/”，我们需要修改docker-compose.yml和harbor.cfg两个文件。

由于docker-compose.yml文件较长，这里将原始文件改名为docker-compose.yml.orig，并将其与修改后的docker-compose.yml做对比：

```
# diff docker-compose.yml.orig docker-compose.yml
8c8
< - /var/log/harbor/:/var/log/docker/:z
---
> - /mnt/cephfs/harbor/log/:/var/log/docker/:z
20c20
< - /data/registry:/storage:z
---
> - /mnt/cephfs/harbor/data/registry:/storage:z
40c40
< - /data/database:/var/lib/mysql:z
---
> - /mnt/cephfs/harbor/data/database:/var/lib/mysql:z
59,61c59,61
< - /data/config/:/etc/adminserver/config/:z
< - /data/secretkey:/etc/adminserver/key:z
< - /data/:/data/:z
---
> - /mnt/cephfs/harbor/data/config/:/etc/adminserver/config/:z
> - /mnt/cephfs/harbor/data/secretkey:/etc/adminserver/key:z
> - /mnt/cephfs/harbor/data/:/data/:z
80,81c80,81
< - /data/secretkey:/etc/ui/key:z
< - /data/ca_download/:/etc/ui/ca/:z
---
> - /mnt/cephfs/harbor/data/secretkey:/etc/ui/key:z
> - /mnt/cephfs/harbor/data/ca_download/:/etc/ui/ca/:z
100c100
< - /data/job_logs:/var/log/jobs:z
---
> - /mnt/cephfs/harbor/data/job_logs:/var/log/jobs:z
102c102
< - /data/secretkey:/etc/jobservice/key:z
---
> - /mnt/cephfs/harbor/data/secretkey:/etc/jobservice/key:z
```


harbor.cfg文件需要修改的地方不多：

```
// harbor.cfg
#The path of cert and key files for nginx, they are applied only the protocol is set to https
ssl_cert = /mnt/cephfs/harbor/data/cert/server.crt
ssl_cert_key = /mnt/cephfs/harbor/data/cert/server.key
#The path of secretkey storage
secretkey_path = /mnt/cephfs/harbor/data
```


配置修改完毕后，执行如下命令：

```
# docker-compose down -v
# prepare
# docker-compose up -d
```


新的harbor实例就启动起来了。注意：这一步我们用cephfs替换了本地存储，主要的存储变动针对log、database和registry三个输出数据的组件。你也许会感受到cephfs给harbor ui页面加载带来的影响，实感要比之前的加载慢一些。

## 五、使用外部数据库(external database)

前面提到了挂载ceph后，多个node上harbor实例中的db组件将出现竞争问题，导致只有一个node上的harbor db组件可以工作。因此，我们要使用外部数据库(或db集群)来解决这个问题。但是harbor官方针对如何配置使用外部DB很是“讳莫如深”，我们只能自己探索。

假设我们已经有了一个external database，并且建立了harbor这个user，并做了相应的授权。由于harbor习惯了独享database，在测试环境下可以考虑

```
GRANT ALL ON *.* TO 'harbor'@'%';
```


### 1、迁移数据

如果此时镜像库中已经有了数据，我们需要做一些迁移工作。

attach到harbor db组件的container中，将registry这张表dump到registry.dump文件中：

```
#docker exec -i -t 6e1e4b576315 bash
在db container中：
# mysqldump -u root -p --databases registry > registry.dump
回到node，将dump文件从container中copy出来：
#docker cp 6e1e4b576315:/root/registry.dump ./
再mysql login到external Database，将registry.dump文件导入：
# mysql -h external_db_ip -P 3306 -u harbor -p
# mysql> source ./registry.dump;
```


### 2、修改harbor配置，使得ui、jobservice组件连接external db

根据当前[harbor architecture](https://github.com/vmware/harbor/wiki/Architecture-Overview-of-Harbor)图所示：

![img{512x368}](../../assets/810e60c1ffccea39.png)


与database“有染”的组件包括ui和jobservice，如何通过配置修改来让这两个组件放弃老db，访问新的external db呢？这要从挖掘配置开始。harbor的组件配置都在common/config下：

```
~/harbor-install/harbor# tree -L 3 common
common
├── config
│ ├── adminserver
│ │ └── env
│ ├── db
│ │ └── env
│ ├── jobservice
│ │ ├── app.conf
│ │ └── env
│ ├── nginx
│ │ └── nginx.conf
│ ├── registry
│ │ ├── config.yml
│ │ └── root.crt
│ └── ui
│ ├── app.conf
│ ├── env
│ └── private_key.pem
└── templates
... ...
```


在修改config之前，我们先docker-compose down掉harbor。接下来，我们看到ui和jobservice下都有env文件，这里想必就是可以注入新db的相关访问信息的地方，我们来试试！

```
// common/config/ui/env
LOG_LEVEL=debug
CONFIG_PATH=/etc/ui/app.conf
UI_SECRET=$ui_secret
JOBSERVICE_SECRET=$jobservice_secret
GODEBUG=netdns=cgo
MYSQL_HOST=new_db_ip
MYSQL_PORT=3306
MYSQL_USR=harbor
MYSQL_PWD=harbor_password
// common/config/jobservice/env
LOG_LEVEL=debug
CONFIG_PATH=/etc/jobservice/app.conf
UI_SECRET=$ui_secret
JOBSERVICE_SECRET=$jobservice_secret
GODEBUG=netdns=cgo
MYSQL_HOST=new_db_ip
MYSQL_PORT=3306
MYSQL_USR=harbor
MYSQL_PWD=harbor_password
```


同时，由于不再需要harbor_db组件，*因此切记：要将其从docker-compose.yml中剔除！*。docker-compose up -d重新创建harbor各组件容器并启动！Harbor的日志可以在挂载的ceph路径： /mnt/cephfs/harbor/log下查找到：

```
/mnt/cephfs/harbor/log# tree 2017-06-09
2017-06-09
├── adminserver.log
├── anacron.log
├── CROND.log
├── jobservice.log
├── mysql.log
├── proxy.log
├── registry.log
├── run-parts.log
└── ui.log
```


我们以ui.log为例，我们发现harbor启动后，ui.log输出如下错误日志(jobservice.log也是相同)：

```
Jun 9 11:00:17 172.19.0.1 ui[16039]: 2017-06-09T03:00:17Z [INFO] initializing database: type-MySQL host-mysql port-3306 user-root database-registry
Jun 9 11:00:18 172.19.0.1 ui[16039]: 2017-06-09T03:00:18Z [ERROR] [utils.go:94]: failed to connect to tcp://mysql:3306, retry after 2 seconds :dial tcp: lookup mysql: no such host
```


我们明明注入了新的db env，为何ui还是要访问“tcp://mysql:3306”呢？我们docker inspect一下ui的container，看看env是否包含我们添加的那些：

```
# docker inspect e91ab20e1dcb
... ...
"Env": [
"DATABASE_TYPE=mysql",
"MYSQL_HOST=database_ip",
"MYSQL_PORT=3306",
"MYSQL_PWD=harbor_password",
"MYSQL_USR=harbor",
"MYSQL_DATABASE=registry",
],
.... ...
```


env已经注入，那么为何ui、jobservice无法连接到external database呢？要想搞清楚这点，我们只能去*“啃代码”*了。还好harbor代码并非很难啃。我们发现基于beego实现的ui、jobservice两个组件并未直接通过os.Getenv去获取这些env变量，而是调用了adminserver组件的服务。adminserver在初始化时，在RESET环境变量为true的情况下，读取了common/config/adminserver/env下的所有环境变量。

搞清楚原理后，我们知道了要修改的是common/config/adminserver/env，而不是common/config/ui/env和common/config/jobservice/env。我们将后两个文件还原。修改common/config/adminserver/env文件：

```
//common/config/adminserver/env
... ...
MYSQL_HOST=new_db_ip
MYSQL_PORT=3306
MYSQL_USR=harbor
MYSQL_PWD=harbor_password
... ...
RESET=true <--- 改为true，非常关键
```


重新up harbor服务后，我们发现ui, jobservice与新database的连接成功了！打开harbor web页面，登录进去，我们看到了之前已经添加的用户、项目和镜像文件。

### 3、一劳永逸

如果你重新执行prepare，那么上面对config目录下的配置修改将被重新覆盖。如果要一劳永逸，那么需要修改的是common/templates下面的同位置同名配置文件。

## 六、安装其他节点上的harbor实例

前面，我们只搭建了一个节点，为的是验证方案的可行性。要实现高可用，我们还需要在其他节点上安装harbor实例。由于多个节点上harbor实例共同挂载ceph的同一目录，因此考虑到log的分离，在部署其他节点上的harbor时，最好对docker-compose.yml下log组件的volumes映射路径进行调整，以在多个节点间做隔离，便于日志查看，比如：

```
volumes:
- /mnt/cephfs/harbor/log1/:/var/log/docker/:z
```


除此之外，各个节点上的harbor配置与上述配置完全一致。

## 七、共享session设置

到harbor的请求被负载均衡分发到多个node上的harbor实例上，这样就有了session共享的需求。Harbor对此已经给予了支持。在ui组件的代码中，我们发现ui在初始化时使用Getenv获取”_REDIS_URL”这个环境变量的值，因此我们只需要将_REDIS_URL这个环境变量配置到各个节点harbor ui组件的env文件中即可：

```
// common/config/adminserver/env
LOG_LEVEL=debug
CONFIG_PATH=/etc/ui/app.conf
UI_SECRET=LuAwkKUtYjF4l0mQ
JOBSERVICE_SECRET=SmsO1kVo4SrmgOIp
GODEBUG=netdns=cgo
_REDIS_URL=redis_ip:6379,100,redis_password,0
```


重新up harbor后，session共享生效。

不过光有一个外部redis存储共享session还不够，请求在多个harbor实例中的registry组件中进行鉴权需要harbor各个实例share相同的[key和certificate](https://github.com/vmware/harbor/blob/master/docs/customize_token_service.md)。好在，我们的多harbor实例通过ceph共享存储，key和cert本就是共享的，都存放在目录：/mnt/cephfs/harbor/data/cert/的下边，因此也就不需要在各个harbor实例间同步key和cert了。

## 八、更换为域名访问

我们有通过域名访问docker registry的需求，那么直接通过域名访问harbor ui和registry是否可行呢？这要看harbor nginx的配置:

```
# docker ps |grep nginx
fa92765e8871 vmware/nginx:1.11.5-patched "nginx -g 'daemon off" 3 hours ago
Up 3 hours 0.0.0.0:443->443/tcp, 0.0.0.0:4443->4443/tcp, 0.0.0.0:8060->80/tcp nginx
# docker exec fa92765e8871 cat /etc/nginx/nginx.conf
... ...
http {
server {
listen 80;
... ...
}
```


nginx在http server block并未对域名或ip进行匹配，因此直接将域名A地址设置为反向代理的地址或直接解析为Harbor暴露的公网ip地址都是可以正常访问harbor服务的，当然也包括image push和pull服务。

注意：如果使用域名访问harbor服务，那么就将harbor.cfg中的hostname赋值为你的”域名+端口”，并重新prepare。否则你可能会发现通过harbor域名上传的image无法pull，因为其pull的地址为由ip组成的地址，以docker push hub.tonybai.com:8989/myrepo/foo:latest为例，push成功后，docker pull hub.tonybai.com:8989/myrepo/foo:latest可能提示你找不到该image，因为harbor中该imag


e的地址可能是my_ip_address:8989/myrepo/foo:latest。

## 九、统一registry的证书和token service的私钥

这是在本篇文章发表之后发现的问题，针对该问题，我专门写了一篇文章：《[解决登录Harbor Registry时鉴权失败的问题](http://tonybai.com/2017/06/15/fix-auth-fail-when-login-harbor-registry/)》,请移步这篇文章，完成HA Harbor的搭建。

## 十、参考资料

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

看了您的文章，感觉很棒，我自己也动手实验了一下，共享Mysql和cephfs挂载按照你的流程都很成功，但是我对于node_public_ip的设置不是很明白。比如我现在有两个Harbor实例放在同一个局域网的两台主机（IP_A，IP_B）上，我两个harbor.cfg里面的host都填的是其中一个主机的局域网IP（IP_A），那么结果当我两个Harbor实例都启动的时候发现IP_B的主机似乎没有起到什么作用，如果把IP_A的Harbor实例down下来，那么浏览器就访问不到IP_A了（虽然IP_B的Harbor实例仍在运行）。

请问这是因为没有用公网IP的原因吗？只有用公网IP才能实现自动的负载分配吗？

IP_A上的harbor down掉后，浏览器访问IP_A的request自然得不到相应的处理。由于request是发往IP_A的，IP_B上的harbor没有收到任何请求，因此就像没有起到作用似的，这也正常啊。局域网也可以做负载均衡啊。前端加一个nginx反向代理，nginx将访问harbor的requests均衡分布到两个后端的harbor实例上去（每个harbor各自harbor.cfg中的host配置各自的ip）。

Hi, tony, 这两篇文章超赞

Hi, tony, 这两篇文章超赞，参照你的方案，VPC1-主机1上面有公网、VPC2-主机2没有公网，两台主机都使用了存储，发现一切ok，就是唯独 公网域名访问VPC1-主机1，一直无法访问不了！是不是还有其他地方要修改？

ooops，知道问题所在之处了，是我这边防火墙的配置的原因导致的！

多谢回复多谢回复！也就是说可以在harbor自己起的那个nginx容器以外另外自己再配置一个nginx反向代理是嘛？让访问IP_A的request给分配到IP_A和IP_B上，是这个意思嘛？

肯定是需要一个外部的反向代理软件，至于这个反向代理部署在IP_A上还是IP_A、IP_B之外的节点上，你自己来定。原理上是可行的。具体的实施步骤和调试你需要自己搞定了。

明白啦！谢谢谢谢！

对了补充一下，在harbor1.1.2版本里面，_REDIS_URL要写在ui/env里面才有效。

harbor管理镜像的标签，怎么只一个一个删除tag标签，比如regitsry:v1、regitsry:v2、regitsry:v3，删除v1保留v2和v3

界面上是可以单独删除指定tag的，如果你是删除一个tag而导致其他tag的问题，请参考我下面的说明，当初我也怀疑是bug：

删除项目里的一个镜像的tag，会导致该镜像所有tag都被删除。后来发现原因是，这些tag都是通过同一个镜像直接改tag生成的，之间是没有任何对镜像层的改动的，所以删除的时候估计会认为这些tag都是一模一样的镜像，所以一起删除了。

我用本地磁盘做存储，push 200M镜像大约花费10秒钟，

用ceph rbd 做存储，push该镜像，差不多也是10秒，

但是当我用cephfs做存储，push该镜像要花费80秒左右（ceph是新集群，没有其他io影响）

求大神支招

cephfs正常就是比rbd要慢的，因为cephfs多一个mds的环节。一些关于cephfs vs cephrbd的benchmark对比经验值差不多是慢3倍左右。cephfs优化的事情我可不是专家，建议到ceph社区去求优化方案。

谢谢。

另外发现一个问题：

我LB的vip是10.20，harbor01是10.31，harbor02是10.32

当我push一个镜像后，docker push 10.62.10.20/library/busybox:latest，我在web页面上查看，发现一个奇怪的现象：

1，底层非共享存储，采用复制方法

10.20上显示 docker push 10.62.10.31/library/busybox:latest

10.31上显示 docker push 10.62.10.31/library/busybox:latest

10.32上显示 docker push 10.62.10.32/library/busybox:latest

2，底层cephfs共享存储

10.20上显示 docker push 10.62.10.31/library/busybox:latest

10.31上显示 docker push 10.62.10.31/library/busybox:latest

10.32上显示 docker push 10.62.10.31/library/busybox:latest

请教，如何才能在界面上显示的是 docker push 10.62.10.20/library/busybox:latest呢，至少打开20的那个界面的这样显示吧，不然给用户用那就麻烦了。

文中有这样一段话：“注意：如果使用域名访问harbor服务，那么就将harbor.cfg中的hostname赋值为你的”域名+端口”，并重新prepare。否则你可能会发现通过harbor域名上传的image无法pull，因为其pull的地址为由ip组成的地址，以docker push hub.tonybai.com:8989/myrepo/foo:latest为例，push成功后，docker pull hub.tonybai.com:8989/myrepo/foo:latest可能提示你找不到该image，因为harbor中该image的地址可能是my_ip_address:8989/myrepo/foo:latest。” ，这是我使用域名时的做法；如果你的最终image地址组成是lb_vip+端口的方式，那就将harbor.cfg中的hostname赋值为你的lb_vip:port，重新prepare。

感谢及时回复，再次感谢

你好，tony！我按照这个文档已经把harbor集群搭建起来了，目前的架构是完全按你的架构图来搭建的，反向代理使用了nginx。目前harbor使用一切正常，但是跑了几天发现redis中并没有什么session共享数据，一点数据都没有。我的疑问是，是不是不需要redis也可以正常使用？

这个我还真没有细究过。从harbor中ui组件的代码中来看，如果配置上_REDIS_URL，的确会打开beego的session共享：


`// github.com/vmware/harbor/src/ui/main.go`

redisURL := os.Getenv("_REDIS_URL")

if len(redisURL) > 0 {

beego.BConfig.WebConfig.Session.SessionProvider = "redis"

beego.BConfig.WebConfig.Session.SessionProviderConfig = redisURL

}

您好，我在挂载cephfs的时候碰到了一点问题：我把挂载的data目录换成我的cephfs之后，访问harbor仓库时提示502 Bad Gateway，请问这是什么原因呢

首先docker-compose ps确认所有组件都启动ok了，然后查查harbor的proxy(nginx)的配置和log吧。进一步，如果你是cli login的，就看看registry日志；如果是web ui 访问的，看看ui的log日志。