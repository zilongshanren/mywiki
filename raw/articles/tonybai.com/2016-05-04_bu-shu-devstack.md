---
title: 部署devstack
url: https://tonybai.com/2016/05/04/deploy-devstack/
published: '2016-05-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 部署devstack

新公司是一家数据与基础设施提供商(to B)。初来乍到，和这里的同事了解了一些云计算平台和大数据平台的技术栈。对于“新鲜”(only to me)的技术栈，自己总有一种折腾的冲动，于是就有了这一篇备忘性质的文章，记录一下自己部署[devstack](https://github.com/openstack-dev/devstack)的步骤、遇到的问题和解决方法。

和诸多国内提供公有云的厂商一样，公司的云产品也是基于成熟的[OpenStack](https://www.openstack.org/)云计算平台框架和组件搭建的，并做了一些定制。长久以来，我一直以为OpenStack等都是Java技术栈的，对Java技术栈出品的东西总有一种莫名的恐惧感，现在我才发现原来OpenStack是Python系（那个汗汗汗啊）。而OpenStack的另外一个竞争对手:[CloudStack](http://cloudstack.apache.org/)才是正经八百的Java系。

OpenStack是一堆云计算平台组件（诸如存储、网络、镜像管理等）的合称，十分庞大且十分复杂，入门门槛不低，即便是为开发目的而进行的OpenStack部署也会让你折腾许久，甚至始终无法搭建成功。为此OpenStack为入门者和开发者推出了一个OpenStack开发环境：[devstack](https://github.com/openstack-dev/devstack)。通过devstack，你可以在一个主机节点上部署一个“五脏俱全”的OpenStack Cloud。

### 一、安装devstack

建议将devstack部署在物理机上，这样可以屏蔽掉许多在虚拟机上部署devstack的问题(具体不详，很多书籍都推荐这么做^_^)。这里讲devstack部署在一台ubuntu 14.04.1的刀片服务器上。

#### 1、下载devstack源码

```
$ git clone https://github.com/openstack-dev/devstack.git ./devstack
Cloning into './devstack'...
remote: Counting objects: 33686, done.
remote: Compressing objects: 100% (10/10), done.
Receiving objects: 1% (337/33686), 92.01 KiB | 35.00 KiB/s
Receiving objects: 4% (1457/33686), 452.01 KiB | 62.00 KiB/s
... ...
```


这里直接用trunk上的最新revision：

```
devstack版本 revision：
commit 96ffde28b6e2f55f95997464aec47ae2c6cf91d3
Merge: c4a0d21 e3a04dd
Author: Jenkins <jenkins@review.openstack.org>
Date: Tue Apr 26 10:21:16 2016 +0000
```


#### 2、创建stack账户

```
$cd devstack/tools
~/devstack/tools$ sudo ./create-stack-user.sh
[sudo] password for baiming:
Creating a group called stack
Creating a user called stack
Giving stack user passwordless sudo privileges
$ cat /etc/passwd|grep stack
stack:x:1006:1006::/opt/stack:/bin/bash
```


修改devstack目录的owner和group权限：

```
$ sudo chown -R stack:stack ./devstack/
```


切换到stack用户下：

```
baiming@baiming:~$ sudo -i -u stack
stack@baiming:~$ cd /home/baiming/devstack
stack@baiming:/home/baiming/devstack$ ls
clean.sh exerciserc extras.d functions-common HACKING.rst LICENSE openrc run_tests.sh setup.py tests unstack.sh
data exercises files FUTURE.rst inc MAINTAINERS.rst pkg samples stackrc tools
doc exercise.sh functions gate lib Makefile README.md setup.cfg stack.sh tox.ini
```


### 二、启动devstack

我们在devstack目录下创建配置文件：local.conf

```
# Credentials
ADMIN_PASSWORD=devstack
MYSQL_PASSWORD=devstack
RABBIT_PASSWORD=devstack
SERVICE_PASSWORD=devstack
SERVICE_TOKEN=token
#Enable/Disable Services
disable_service n-net
enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-meta
enable_service neutron
enable_service tempest
HOST_IP=10.10.105.71
#NEUTRON CONFIG
#Q_USE_DEBUG_COMMAND=True
#CINDER CONFIG
VOLUME_BACKING_FILE_SIZE=102400M
#GENERAL CONFIG
API_RATE_LIMIT=False
# Output
LOGFILE=/home/baiming/devstack/logs/stack.sh.log
VERBOSE=True
LOG_COLOR=False
SCREEN_LOGDIR=/home/baiming/devstack/logs
```


执行devstack下的stack.sh来启动各OpenStack组件，stack.sh是devstack“一键安装”的总控脚本，stack.sh执行ok了，devstack也就部署OK了：

```
$>./stack.sh
```


但问题接踵而至！

### 三、问题与解决方法

stack.sh的执行过程是漫长的，且问题也是多多。

#### 1、git协议 or https协议

stack.sh执行后会去openstack官方库下载一些东西，于是遇到了第一个错误：

```
+functions-common:git_timed:599 timeout -s SIGINT 0 git clone git://git.openstack.org/openstack/requirements.git /opt/stack/requirements
Cloning into '/opt/stack/requirements'...
fatal: unable to connect to git.openstack.org:
git.openstack.org[0: 104.130.246.128]: errno=Connection timed out
git.openstack.org[1: 2001:4800:7819:103:be76:4eff:fe06:63c]: errno=Network is unreachable
+functions-common:git_timed:602 [[ 128 -ne 124 ]]
+functions-common:git_timed:603 die 603 'git call failed: [git clone' git://git.openstack.org/openstack/requirements.git '/opt/stack/requirements]'
+functions-common:die:186 local exitcode=0
+functions-common:die:187 set +o xtrace
[Call Trace]
./stack.sh:708:git_clone
/home/baiming/devstack/functions-common:536:git_timed
/home/baiming/devstack/functions-common:603:die
[ERROR] /home/baiming/devstack/functions-common:603 git call failed: [git clone git://git.openstack.org/openstack/requirements.git /opt/stack/requirements]
Error on exit
./stack.sh: line 488: generate-subunit: command not found
```


stack.sh尝试用git clone git://xxxx，但由于我的主机在代理后面，因此git协议不能被支持，需要改为支持的协议类型，比如https。

解决方法：修改stackrc，更换git_base协议，并且增加http和https代理变量：

```
# Base GIT Repo URL
# Another option is https://git.openstack.org
GIT_BASE=${GIT_BASE:-https://git.openstack.org}
export http_proxy='http://10.10.126.187:3129'
export https_proxy='http://10.10.126.187:3129'
```


stackrc之于stack.sh类似.bashrc之于bash，在stack.sh执行时会对stackrc进行source，使其中的export环境变量生效。http_proxy等环境变量添加到stackrc中的效果就是：在stack.sh执行过程中会有类似如下语句出现：

```
sudo -H http_proxy=http://10.10.126.187:3129 https_proxy=http://10.10.126.187:3129 no_proxy= PIP_FIND_LINKS= /usr/local/bin/pip2.7 install -c /opt/stack/requirements/upper-constraints.txt -U virtualenv
```


#### 2、重启stack.sh

解决完上述问题后，如果直接重新执行stack.sh，那么会收到“有另外一个stack.sh session在执行的”错误信息。

为此，每次重启stack.sh之前都要先执行：./unstack.sh，清理一下环境。

#### 3、apt包下载错误

在stack.sh执行过程中，会更新ubuntu apt repository，并下载许多第三方包或工具：

```
Preconfiguring packages ...
(Reading database ... 123098 files and directories currently installed.)
Preparing to unpack .../libitm1_4.8.4-2ubuntu1~14.04.1_amd64.deb ...
Unpacking libitm1:amd64 (4.8.4-2ubuntu1~14.04.1) over (4.8.4-2ubuntu1~14.04) ...
Preparing to unpack .../libgomp1_4.8.4-2ubuntu1~14.04.1_amd64.deb ...
Unpacking libgomp1:amd64 (4.8.4-2ubuntu1~14.04.1) over (4.8.4-2ubuntu1~14.04) ...
Preparing to unpack .../libasan0_4.8.4-2ubuntu1~14.04.1_amd64.deb ...
Unpacking libasan0:amd64 (4.8.4-2ubuntu1~14.04.1) over (4.8.4-2ubuntu1~14.04) ...
Preparing to unpack .../libatomic1_4.8.4-2ubuntu1~14.04.1_amd64.deb ...
Unpacking libatomic1:amd64 (4.8.4-2ubuntu1~14.04.1) over (4.8.4-2ubuntu1~14.04) ...
Preparing to unpack .../libtsan0_4.8.4-2ubuntu1~14.04.1_amd64.deb ...
Unpacking libtsan0:amd64 (4.8.4-2ubuntu1~14.04.1) over (4.8.4-2ubuntu1~14.04) ...
Preparing to unpack .../libquadmath0_4.8.4-2ubuntu1~14.04.1_amd64.deb ...
Unpacking libquadmath0:amd64 (4.8.4-2ubuntu1~14.04.1) over (4.8.4-2ubuntu1~14.04) ...
Preparing to unpack .../libstdc++-4.8-dev_4.8.4-2ubuntu1~14.04.1_amd64.deb ...
.... ..... ....
Setting up libitm1:amd64 (4.8.4-2ubuntu1~14.04.1) ...
Setting up libgomp1:amd64 (4.8.4-2ubuntu1~14.04.1) ...
Setting up libasan0:amd64 (4.8.4-2ubuntu1~14.04.1) ...
Setting up libatomic1:amd64 (4.8.4-2ubuntu1~14.04.1) ...
Setting up libtsan0:amd64 (4.8.4-2ubuntu1~14.04.1) ...
.... .....
* Setting sysfs variables... [ OK ]
Setting up vlan (1.9-3ubuntu10) ...
Processing triggers for libc-bin (2.19-0ubuntu6) ...
Processing triggers for ureadahead (0.100.0-16) ...
Processing triggers for initramfs-tools (0.103ubuntu4.2) ...
update-initramfs: Generating /boot/initrd.img-3.16.0-57-generic
.... ....
```


如果你的source.list中添加了一些不稳定的源，那么这个包更新过程很可能会失败，从而导致stack.sh执行失败。解决方法就是识别出哪些源导致的失败，将之注释掉！

#### 4、MySQL access denied

继续执行stack.sh，我们遇到了如下MySQL访问错误：

```
+lib/databases/mysql:configure_database_mysql:91 sudo mysql -u root -p devstack -h 127.0.0.1 -e 'GRANT ALL PRIVILEGES ON *.* TO '\''root'\''@'\''%'\'' identified by '\''devstack'\'';'
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
+lib/databases/mysql:configure_database_mysql:1 exit_trap
+./stack.sh:exit_trap:474 local r=1
++./stack.sh:exit_trap:475 jobs -p
+./stack.sh:exit_trap:475 jobs=
+./stack.sh:exit_trap:478 [[ -n '' ]]
+./stack.sh:exit_trap:484 kill_spinner
+./stack.sh:kill_spinner:370 '[' '!' -z '' ']'
+./stack.sh:exit_trap:486 [[ 1 -ne 0 ]]
+./stack.sh:exit_trap:487 echo 'Error on exit'
Error on exit
+./stack.sh:exit_trap:488 generate-subunit 1461911655 5243 fail
+./stack.sh:exit_trap:489 [[ -z /opt/stack/logs ]]
+./stack.sh:exit_trap:492 /home/baiming/devstack/tools/worlddump.py -d /opt/stack/logs
World dumping... see /opt/stack/logs/worlddump-2016-04-29-080139.txt for details
```


这个问题浪费了我不少时间，遍历了许多网上资料，最终下面这个方法解决了问题：

查看/etc/mysql/debian.cnf文件：

```
# Automatically generated for Debian scripts. DO NOT TOUCH!
[client]
host = localhost
user = debian-sys-maint
password = WY9OFagMxMb4YmyV
socket = /var/run/mysqld/mysqld.sock
[mysql_upgrade]
host = localhost
user = debian-sys-maint
password = WY9OFagMxMb4YmyV
socket = /var/run/mysqld/mysqld.sock
basedir = /usr
```


修改mysql root密码：

```
$ [root@localhost ~]# mysql -u debian-sys-maint - p
输入密码： WY9OFagMxMb4YmyV ，进入到mysql数据库
mysql>use mysql ；
mysql>update user set password=password("你的新密码") where user="root";
mysql>flush privileges;
mysql>exit
```


然后尝试使用新密码登录，如果登录成功，说明密码修改ok。再执行stack.sh就不会出现MySQL相关错误了。

#### 5、openvswitch/db.sock权限问题

接下来我们遇到的问题是openvswitch/db.sock权限问题，错误日志如下：

```
+lib/keystone:create_keystone_accounts:368 local admin_project
++lib/keystone:create_keystone_accounts:369 openstack project show admin -f value -c id
Discovering versions from the identity service failed when creating the password plugin. Attempting to determine version from URL.
Could not determine a suitable URL for the plugin
+lib/keystone:create_keystone_accounts:369 admin_project=
+lib/keystone:create_keystone_accounts:1 exit_trap
+./stack.sh:exit_trap:474 local r=1
++./stack.sh:exit_trap:475 jobs -p
+./stack.sh:exit_trap:475 jobs=
+./stack.sh:exit_trap:478 [[ -n '' ]]
+./stack.sh:exit_trap:484 kill_spinner
+./stack.sh:kill_spinner:370 '[' '!' -z '' ']'
+./stack.sh:exit_trap:486 [[ 1 -ne 0 ]]
+./stack.sh:exit_trap:487 echo 'Error on exit'
Error on exit
+./stack.sh:exit_trap:488 generate-subunit 1461920296 413 fail
+./stack.sh:exit_trap:489 [[ -z /opt/stack/logs ]]
+./stack.sh:exit_trap:492 /home/baiming/devstack/tools/worlddump.py -d /opt/stack/logs
World dumping... see /opt/stack/logs/worlddump-2016-04-29-090510.txt for details
2016-04-29T09:05:10Z|00001|reconnect|WARN|unix:/var/run/openvswitch/db.sock: connection attempt failed (Permission denied)
ovs-vsctl: unix:/var/run/openvswitch/db.sock: database connection failed (Permission denied)
+./stack.sh:exit_trap:498 exit 1
```


我们手工执行ovs-vsctl命令：

```
$ sudo service openvswitch-switch status
openvswitch-switch start/running
$ ovs-vsctl show
2016-04-29T09:44:19Z|00001|reconnect|WARN|unix:/var/run/openvswitch/db.sock: connection attempt failed (Permission denied)
ovs-vsctl: unix:/var/run/openvswitch/db.sock: database connection failed (Permission denied)
```


同样的错误。这个问题在网上似乎也没有很好的答案，这里做了一个权限更改处理：

```
$>chmod 777 /var/run/openvswitch/db.sock
```


问题解决了！

#### 6、http proxy问题

我们接下来停在了这里：

```
++lib/keystone:create_keystone_accounts:369 openstack project show admin -f value -c id
Discovering versions from the identity service failed when creating the password plugin. Attempting to determine version from URL.
Could not determine a suitable URL for the plugin
```


还是停在这里，但这回不是/var/run/openvswitch /db.sock权限问题了。似乎是stack.sh想访问某个url获得一些version信息，但没有获取到。我开始怀疑是代理设置的问题：这个环境是有代理设置的，一旦走代理访问自己，那么肯定什么信息都得不到。但代理还不能去掉，因此很多组件下载都需要使用到代理访问外网。为此我们需要在stackrc中加上no_proxy环境变量：

```
export no_proxy='10.10.105.71'
```


再执行stack.sh，至少这个问题是pass了。

### 四、devstack部署ok

在经过很不耐烦的漫长等待后，devstack终于算是部署成功了！stack.sh打印出了下面信息后成功退出了：

```
=========================
DevStack Component Timing
=========================
Total runtime 2574
run_process 57
apt-get-update 120
pip_install 859
restart_apache_server 11
wait_for_service 32
apt-get 14
=========================
This is your host IP address: 10.10.105.71
This is your host IPv6 address: ::1
Horizon is now available at http://10.10.105.71/dashboard
Keystone is serving at http://10.10.105.71:5000/
The default users are: admin and demo
The password: devstack
2016-05-03 08:01:03.667 | stack.sh completed in 2574 seconds.
```


我们看devstack究竟运行了哪些组件：

```
$ ps -ef|grep python
stack 1464 1461 0 15:24 pts/5 00:00:14 /usr/bin/python /usr/bin/dstat -tcmndrylpg --output /opt/stack/logs/dstat-csv.log
stack 1465 1461 6 15:24 pts/5 00:03:01 /usr/bin/python /usr/bin/dstat -tcmndrylpg --top-cpu-adv --top-io-adv --swap
stack 11641 11490 0 15:48 pts/10 00:00:03 /usr/bin/python /usr/local/bin/glance-registry --config-file=/etc/glance/glance-registry.conf
stack 11899 11641 0 15:48 pts/10 00:00:00 /usr/bin/python /usr/local/bin/glance-registry --config-file=/etc/glance/glance-registry.conf
stack 11900 11641 0 15:48 pts/10 00:00:00 /usr/bin/python /usr/local/bin/glance-registry --config-file=/etc/glance/glance-registry.conf
stack 11978 11821 1 15:48 pts/11 00:00:24 /usr/bin/python /usr/local/bin/glance-api --config-file=/etc/glance/glance-api.conf
stack 12105 11978 1 15:48 pts/11 00:00:30 /usr/bin/python /usr/local/bin/glance-api --config-file=/etc/glance/glance-api.conf
stack 12106 11978 1 15:48 pts/11 00:00:30 /usr/bin/python /usr/local/bin/glance-api --config-file=/etc/glance/glance-api.conf
stack 13411 13262 2 15:51 pts/12 00:00:29 /usr/bin/python /usr/local/bin/nova-api
stack 13551 13411 0 15:52 pts/12 00:00:03 /usr/bin/python /usr/local/bin/nova-api
stack 13552 13411 0 15:52 pts/12 00:00:03 /usr/bin/python /usr/local/bin/nova-api
stack 13823 13411 0 15:52 pts/12 00:00:00 /usr/bin/python /usr/local/bin/nova-api
stack 13824 13411 0 15:52 pts/12 00:00:00 /usr/bin/python /usr/local/bin/nova-api
stack 14309 14159 1 15:52 pts/13 00:00:25 /usr/bin/python /usr/local/bin/nova-conductor --config-file /etc/nova/nova.conf
stack 15092 14941 3 15:52 pts/14 00:00:39 /usr/bin/python /usr/local/bin/nova-network --config-file /etc/nova/nova.conf
stack 15352 14309 2 15:52 pts/13 00:00:38 /usr/bin/python /usr/local/bin/nova-conductor --config-file /etc/nova/nova.conf
stack 15353 14309 2 15:52 pts/13 00:00:38 /usr/bin/python /usr/local/bin/nova-conductor --config-file /etc/nova/nova.conf
stack 15432 15274 1 15:52 pts/15 00:00:14 /usr/bin/python /usr/local/bin/nova-scheduler --config-file /etc/nova/nova.conf
stack 15920 15768 0 15:52 pts/16 00:00:05 /usr/bin/python /usr/local/bin/nova-novncproxy --config-file /etc/nova/nova.conf --web /opt/stack/noVNC
stack 16571 16415 1 15:52 pts/17 00:00:13 /usr/bin/python /usr/local/bin/nova-consoleauth --config-file /etc/nova/nova.conf
stack 17134 17131 3 15:53 pts/18 00:00:46 /usr/bin/python /usr/local/bin/nova-compute --config-file /etc/nova/nova.conf
stack 17890 17740 1 15:54 pts/19 00:00:23 /usr/bin/python /usr/local/bin/cinder-api --config-file /etc/cinder/cinder.conf
stack 18027 17890 0 15:54 pts/19 00:00:00 /usr/bin/python /usr/local/bin/cinder-api --config-file /etc/cinder/cinder.conf
stack 18028 17890 0 15:54 pts/19 00:00:01 /usr/bin/python /usr/local/bin/cinder-api --config-file /etc/cinder/cinder.conf
stack 18363 18212 2 15:54 pts/20 00:00:33 /usr/bin/python /usr/local/bin/cinder-scheduler --config-file /etc/cinder/cinder.conf
stack 18853 18699 1 15:54 pts/21 00:00:22 /usr/bin/python /usr/local/bin/cinder-volume --config-file /etc/cinder/cinder.conf
stack 19060 18853 2 15:54 pts/21 00:00:28 /usr/bin/python /usr/local/bin/cinder-volume --config-file /etc/cinder/cinder.conf
```


果然很复杂。devstack的安装体验比OpenStack似乎也好不到那里去。stack.sh执行的时间足够编译10次linux os内核了。好多依赖，好多download。

在devstack目录下，我们还可以执行一下devstack的测试，./exercise.sh会执行这些测试：

```
*********************************************************************
SUCCESS: End DevStack Exercise: /home/baiming/devstack/exercises/volumes.sh
*********************************************************************
=====================================================================
SKIP neutron-adv-test
SKIP swift
PASS aggregates
PASS client-args
PASS client-env
PASS sec_groups
PASS volumes
FAILED boot_from_volume
FAILED floating_ips
=====================================================================
```


此刻访问 http://10.10.105.71/dashboard，我们可以看到devstack horizon的首页：

![img{512x368}](../../assets/5d9e6776dda34972.png)


不过由于是通过SecureCRT端口映射访问到的主页，不知为何，登录后始终无法显示dashboard的页面。但通过后台horizon的日志来看，登录(admin/devstack)是成功的。我们仅能探索cli操作devstack的方式了。

### 五、CLI方式操作devstack

devstack提供了CLI方式对虚拟机、存储和网络等组件进行操作，其功能还要超过GUI所能提供的。在使用cli工具前，我们需要设置一些cli所需的用户变量，放在shell文件中（比如.bashrc）：

```
export OS_USERNAME=admin
export OS_PASSWORD=devstack
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://10.10.105.71:5000/v2.0
```


上述变量生效后，我们就可以通过cli来hack devstack了：

nova位置和nova版本：

```
$ which nova
/usr/local/bin/nova
$ nova --version
4.0.0
```


当前image列表：

```
$ nova image-list
WARNING: Command image-list is deprecated and will be removed after Nova 15.0.0 is released. Use python-glanceclient or openstackclient instead.
+--------------------------------------+---------------------------------+--------+--------+
| ID | Name | Status | Server |
+--------------------------------------+---------------------------------+--------+--------+
| b3f25af2-b5e1-43fe-8648-842fe48ed380 | cirros-0.3.4-x86_64-uec | ACTIVE | |
| d6bcc064-e2aa-4550-89e7-fd2f6a454758 | cirros-0.3.4-x86_64-uec-kernel | ACTIVE | |
| 788dec66-8989-4e84-8722-d9f4c9ee5ab0 | cirros-0.3.4-x86_64-uec-ramdisk | ACTIVE | |
+--------------------------------------+---------------------------------+--------+--------+
```


虚拟机规格列表：

```
$ nova flavor-list
+----+-----------+-----------+------+-----------+------+-------+-------------+-----------+
| ID | Name | Memory_MB | Disk | Ephemeral | Swap | VCPUs | RXTX_Factor | Is_Public |
+----+-----------+-----------+------+-----------+------+-------+-------------+-----------+
| 1 | m1.tiny | 512 | 1 | 0 | | 1 | 1.0 | True |
| 2 | m1.small | 2048 | 20 | 0 | | 1 | 1.0 | True |
| 3 | m1.medium | 4096 | 40 | 0 | | 2 | 1.0 | True |
| 4 | m1.large | 8192 | 80 | 0 | | 4 | 1.0 | True |
| 42 | m1.nano | 64 | 0 | 0 | | 1 | 1.0 | True |
| 5 | m1.xlarge | 16384 | 160 | 0 | | 8 | 1.0 | True |
| 84 | m1.micro | 128 | 0 | 0 | | 1 | 1.0 | True |
| c1 | cirros256 | 256 | 0 | 0 | | 1 | 1.0 | True |
| d1 | ds512M | 512 | 5 | 0 | | 1 | 1.0 | True |
| d2 | ds1G | 1024 | 10 | 0 | | 1 | 1.0 | True |
| d3 | ds2G | 2048 | 10 | 0 | | 2 | 1.0 | True |
| d4 | ds4G | 4096 | 20 | 0 | | 4 | 1.0 | True |
+----+-----------+-----------+------+-----------+------+-------+-------------+-----------+
```


启动一个虚拟机：

```
$ nova boot --flavor 1 --image b3f25af2-b5e1-43fe-8648-842fe48ed380 devstack_instance_1
+--------------------------------------+----------------------------------------------------------------+
| Property | Value |
+--------------------------------------+----------------------------------------------------------------+
| OS-DCF:diskConfig | MANUAL |
| OS-EXT-AZ:availability_zone | |
| OS-EXT-SRV-ATTR:host | - |
| OS-EXT-SRV-ATTR:hostname | devstack-instance-1 |
| OS-EXT-SRV-ATTR:hypervisor_hostname | - |
| OS-EXT-SRV-ATTR:instance_name | instance-00000005 |
| OS-EXT-SRV-ATTR:kernel_id | d6bcc064-e2aa-4550-89e7-fd2f6a454758 |
| OS-EXT-SRV-ATTR:launch_index | 0 |
| OS-EXT-SRV-ATTR:ramdisk_id | 788dec66-8989-4e84-8722-d9f4c9ee5ab0 |
| OS-EXT-SRV-ATTR:reservation_id | r-3rpqat0r |
| OS-EXT-SRV-ATTR:root_device_name | - |
| OS-EXT-SRV-ATTR:user_data | - |
| OS-EXT-STS:power_state | 0 |
| OS-EXT-STS:task_state | scheduling |
| OS-EXT-STS:vm_state | building |
| OS-SRV-USG:launched_at | - |
| OS-SRV-USG:terminated_at | - |
| accessIPv4 | |
| accessIPv6 | |
| adminPass | dGBd6vj55vP2 |
| config_drive | |
| created | 2016-05-03T09:00:33Z |
| description | - |
| flavor | m1.tiny (1) |
| hostId | |
| host_status | |
| id | bdb93a06-0c4f-434f-a1b5-ae2ca9293c58 |
| image | cirros-0.3.4-x86_64-uec (b3f25af2-b5e1-43fe-8648-842fe48ed380) |
| key_name | - |
| locked | False |
| metadata | {} |
| name | devstack_instance_1 |
| os-extended-volumes:volumes_attached | [] |
| progress | 0 |
| security_groups | default |
| status | BUILD |
| tenant_id | ce19134da8774d509bfa15daaca83665 |
| updated | 2016-05-03T09:00:34Z |
| user_id | 45436c9a744b4f41921edb3c368ce5f7 |
+--------------------------------------+----------------------------------------------------------------+
```


通过nova list可以查看到当前主机上的虚拟机详情：

```
$ nova list
+--------------------------------------+---------------------+--------+------------+-------------+------------------+
| ID | Name | Status | Task State | Power State | Networks |
+--------------------------------------+---------------------+--------+------------+-------------+------------------+
| bdb93a06-0c4f-434f-a1b5-ae2ca9293c58 | devstack_instance_1 | ACTIVE | - | Running | private=10.0.0.5 |
+--------------------------------------+---------------------+--------+------------+-------------+------------------+
```


在host上ping该虚拟机实例，可以ping通：

```
$ ping 10.0.0.5
PING 10.0.0.5 (10.0.0.5) 56(84) bytes of data.
64 bytes from 10.0.0.5: icmp_seq=1 ttl=64 time=0.935 ms
64 bytes from 10.0.0.5: icmp_seq=2 ttl=64 time=0.982 ms
^C
--- 10.0.0.5 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.935/0.958/0.982/0.038 ms
```


通过网桥工具查看网桥设备，看到多出一个br100的网桥，eth0、vnet0~vnet2均连接在该网桥上：

```
$ brctl show
bridge name bridge id STP enabled interfaces
br100 8000.0017a447a8a9 no eth0
vnet0
vnet1
vnet2
```


挂起虚拟机：

```
$ nova suspend bdb93a06-0c4f-434f-a1b5-ae2ca9293c58
$ nova list
+--------------------------------------+---------------------+-----------+------------+-------------+------------------+
| ID | Name | Status | Task State | Power State | Networks |
+--------------------------------------+---------------------+-----------+------------+-------------+------------------+
| bdb93a06-0c4f-434f-a1b5-ae2ca9293c58 | devstack_instance_1 | SUSPENDED | - | Shutdown | private=10.0.0.5 |
+--------------------------------------+---------------------+-----------+------------+-------------+------------------+
```


### 六、小结

devstack号称是为开发准备的，已经“一键化”，但从实际效果来看，体验依旧不佳。由此也可以估计出OpenStack的部署难度和坎坷度了:)。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

至今还没有成功部署过一次 OpenStack 的计算环境……

求问单网卡可以么？您的lan环境，也就是devstack的wan口ip是多少？

我记得我那个试验的刀片环境就是单物理网卡的，只有一个lan口：10.10.105.71，文章里有。

Discovering versions from the identity service failed when creating the password plugin. Attempting to determine version from URL.

Could not determine a suitable URL for the plugin

+ functions-common:get_or_create_user:813 : user_id=

+ functions-common:get_or_create_user:1 : exit_trap

+ ./stack.sh:exit_trap:494 : local r=1

++ ./stack.sh:exit_trap:495 : jobs -p

+ ./stack.sh:exit_trap:495 : jobs=

+ ./stack.sh:exit_trap:498 : [[ -n '' ]]

+ ./stack.sh:exit_trap:504 : kill_spinner

+ ./stack.sh:kill_spinner:390 : ‘[' '!' -z '' ']‘

+ ./stack.sh:exit_trap:506 : [[ 1 -ne 0 ]]

+ ./stack.sh:exit_trap:507 : echo ‘Error on exit’

Error on exit

+ ./stack.sh:exit_trap:508 : generate-subunit 1521468979 434 fail

+ ./stack.sh:exit_trap:509 : [[ -z /opt/stack/logs ]]

+ ./stack.sh:exit_trap:512 : /opt/stack/devstack/tools/worlddump.py -d /opt/stack/logs

World dumping… see /opt/stack/logs/worlddump-2018-03-19-142334.txt for details

+ ./stack.sh:exit_trap:518 : exit 1

出现了上面这样的问题，没有openvswitch/db.sock权限问题的提示，也添加了no_proxy，请问还有什么解决方法吗

时间太久了，我也没有devstack的环境了，建议到项目的github issue中找找有无类似问题以及解决方法。

请问如果出现g-api该如何解决

+functions:wait_for_service:432 rval=124

+functions:wait_for_service:437 time_stop wait_for_service

+functions-common:time_stop:2254 local name

+functions-common:time_stop:2255 local end_time

+functions-common:time_stop:2256 local elapsed_time

+functions-common:time_stop:2257 local total

+functions-common:time_stop:2258 local start_time

+functions-common:time_stop:2260 name=wait_for_service

+functions-common:time_stop:2261 start_time=1525667590487

+functions-common:time_stop:2263 [[ -z 1525667590487 ]]

++functions-common:time_stop:2266 date +%s%3N

+functions-common:time_stop:2266 end_time=1525667650541

+functions-common:time_stop:2267 elapsed_time=60054

+functions-common:time_stop:2268 total=58

+functions-common:time_stop:2270 _TIME_START[$name]=

+functions-common:time_stop:2271 _TIME_TOTAL[$name]=60112

+functions:wait_for_service:438 return 124

+lib/glance:start_glance:352 die 352 ‘g-api did not start’

+functions-common:die:187 local exitcode=0

+functions-common:die:188 set +o xtrace

[Call Trace]

./stack.sh:1240:start_glance

/opt/stack/devstack/lib/glance:352:die

[ERROR] /opt/stack/devstack/lib/glance:352 g-api did not start

Error on exit

World dumping… see /opt/stack/logs/worlddump-2018-05-07-043411.txt for details

以前没遇到过，现在也没有devstack环境了。不过 google了一下，找到了两个和你遇到相似问题的帖子，希望能帮助到你。https://answers.launchpad.net/glance/+question/231020 以及 https://blog.csdn.net/a479898045/article/details/11522659

@洪城浪子 我也遇到同样的问题：‘g-api did not start’，不知道你解决了没有