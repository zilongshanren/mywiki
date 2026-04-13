---
title: 使用core-vagrant方式安装CoreOS
url: https://tonybai.com/2015/07/20/install-coreos-by-coreos-vagrant/
published: '2015-07-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用core-vagrant方式安装CoreOS

[CoreOS](http://coreos.com)是一种专门为运行类[docker](http://tonybai.com/tag/docker)容器而生的linux发行版。与其他通用linux发行版（[ubuntu](http://tonybai.com/tag/ubuntu)、[debian](http://www.debian.org)、[redhat](http://www.redhat.com))相 比，它具有体型最小，消耗最小，支持滚动更新等特点。除此之外CoreOS内置的分布式系统服务组件也给开发者和运维者组建分布式集群、部署分布式服务应 用带来了极大便利。

CoreOS与知名容器[Docker](http://docker.com)脚前脚后诞生，到目前为止已经较为成熟，国外主流云平台提供商如[Amazon EC2](http://aws.amazon.com/ec2)、[Google Compute Engine](https://cloud.google.com/compute)、[Microsoft Azure](http://azure.microsoft.com)、[Digtial Ocean](https://www.digitalocean.com/?refcode=bff6eed92687)等均提供了CoreOS image，通过这些服务，你可以一键建立一个CoreOS实例，这似乎也是CoreOS官方推荐的主流install方式（最Easy）。

CoreOS当然支持其他方式的安装，比如支持虚拟机安装([vagrant](https://www.vagrantup.com)+[virtualbox](https://virtualbox.org))、PXE(preboot execute environment)安装以及iso install to 物理disk方式。如果仅仅是做一些实验，虚拟机安装是最简单也是最安全的方式。不过由于CoreOS的官方下载站在大陆无法直接访问（大陆程序员们好悲 催啊），因此这一最简单的虚拟机安装CoreOS的过程也就不那么简单了。

通过core-vagrant安装的直接结果是CoreOS被安装到一个VirtualBox虚拟机中，之后我们利用Vagrant命令来进行 CoreOS虚拟机的启停。CoreOS以及Vagrant都在持续演进，尤其是CoreOS目前在active dev中，版本号变化很快，这也是CoreOS滚动升级的必然结果。因此在安装操作演示前，我们有必要明确一下这个安装过程使用的软件版本：

物理机OS:

Ubuntu 12.04 3.8.0-42-generic x86_64

VirtualBox:

Oracle VM VirtualBox Manager 4.2.10

Vagrant:

Vagrant 1.7.3

CoreOS:

stable 717.3.0

coreos-vagrant source:

commit b9ed7e2182ff08b72419ab3e89f4a5652bc75082

**一、原理**

如果没有Wall，CoreOS的coreos-vagrant安装将非常简单：

1、git clone https://github.com/coreos/coreos-vagrant

2、编辑配置文件

3、vagrant up

4、vagrant ssh

但是现在有了Wall，步骤3：vagrant up会报错：无法连接到http://stable.release.core-os.net/amd64-usr/717.3.0/xx这个url，导致安装失败。

我大致分析了一下vagrant up的执行过程：

1、设置配置默认值

$num_instances = 1

$instance_name_prefix = "core"

$update_channel = "alpha"

$image_version = "current"

$enable_serial_logging = false

$share_home = false

$vm_gui = false

$vm_memory = 1024

$vm_cpus = 1

$shared_folders = {}

$forwarded_ports = {}

2、判断是否存在config.rb这个配置，如果有，则加载。

3、设置config.vm.url，并获取对应的json文件：

{

"name": "coreos-stable",

"description": "CoreOS stable",

"versions": [{

"version": "717.3.0",

"providers": [{

"name": "virtualbox",

"url": "http://stable.release.core-os.net/amd64-usr/717.3.0/coreos_production_vagrant.box",

"checksum_type": "sha256",

"checksum": "99dcd74c7cae8b1d90f108f8819f92b17bfbd34f4f141325bd0400fe4def55b6"

}]

}]

}

4、根据config.vm.provider（是virtualbox还是vmvare等）来决定采用哪种虚拟机创建逻辑。

这里我们看到，整个过程只需要从core-os.net下载两个文件：coreos_production_vagrant.box和coreos_production_vagrant.json。如果我们提前将这两个文件下载到本地，并放在一个临时的http server下，修改Vagrantfile和coreos_production_vagrant.json这两个文件，就应该可以通过coreos-vagrant安装了。

**二、coreos-vagrant安装single instance CoreOS**

好了，根据上述原理，我们首先要下载coreos_production_vagrant.box和coreos_production_vagrant.json这两个文件，根据我们的channel和版本选择，两个文件的下载地址分别为：

http://stable.release.core-os.net/amd64-usr/717.3.0/coreos_production_vagrant.box

http://stable.release.core-os.net/amd64-usr/717.3.0/coreos_production_vagrant.json

接下来就是不管你用什么梯子，只要把这两个文件下载到本地，并放到一个目录下就好了。

我们需要修改一下coreos_production_vagrant.json，将其中的url改为：


"url": "http://localhost:8080/coreos_production_vagrant.box"

我们要将这两个文件放到一个local file server中，后续供core-vagrant访问。最简单的方法就是使用:

python -m SimpleHTTPServer 8080

当然使用Go实现一个简单的http file server也是非常简单的：

//fileserver.go

package main

import "net/http"

import "log"

func main() {

log.Fatal(http.ListenAndServe(":8080", http.FileServer(http.Dir("./"))))

}

接下来我们就可以按照正常步骤，下载coreos-vagrant并up了：

$git clone https://github.com/coreos/coreos-vagrant

修改Vagrantfile：

$ diff Vagrantfile Vagrantfile.bak

14,15c14,15

< $update_channel = "stable"

< $image_version = "717.3.0"

—

> $update_channel = "alpha"

> $image_version = "current"

55c55

< config.vm.box_url = "http://localhost:8080/coreos_production_vagrant.json"

—

> config.vm.box_url = "http://%s.release.core-os.net/amd64-usr/%s/coreos_production_vagrant.json" % [$update_channel, $image_version]

将user-data.sample改名为user-data，并编辑user-data，在etcd2下面增加一行：

etcd2:

name: core-01

将units:下面对于etcd2的注释去掉，以enable etcd2服务。（将etcd服务注释掉）

万事俱备，只需vagrant up。

$ vagrant up

Bringing machine 'core-01' up with 'virtualbox' provider…

==> core-01: Box 'coreos-stable' could not be found. Attempting to find and install…

core-01: **Box Provider: virtualbox**

core-01: **Box Version: 717.3.0**

==> core-01: **Loading metadata for box 'http://localhost:8080/coreos_production_vagrant.json'**

core-01: URL: http://localhost:8080/coreos_production_vagrant.json

==> core-01: Adding box 'coreos-stable' (v717.3.0) for provider: virtualbox

core-01: **Downloading: http://localhost:8080/coreos_production_vagrant.box**

core-01: Calculating and comparing box checksum…

==> core-01: Successfully added box 'coreos-stable' (v717.3.0) for 'virtualbox'!

==> core-01: Importing base box 'coreos-stable'…

==> core-01: Matching MAC address for NAT networking…

==> core-01: Checking if box 'coreos-stable' is up to date…

==> core-01: Setting the name of the VM: coreos-vagrant_core-01_1437121834188_89503

==> core-01: Clearing any previously set network interfaces…

==> core-01: Preparing network interfaces based on configuration…

core-01: Adapter 1: nat

core-01: Adapter 2: hostonly

==> core-01: Forwarding ports…

core-01: 22 => 2222 (adapter 1)

==> core-01: Running 'pre-boot' VM customizations…

==> core-01: Booting VM…

==> core-01: Waiting for machine to boot. This may take a few minutes…

core-01: SSH address: 127.0.0.1:2222

core-01: SSH username: core

core-01: SSH auth method: private key

core-01: Warning: Connection timeout. Retrying…

==> core-01: Machine booted and ready!

==> core-01: Setting hostname…

==> core-01: Configuring and enabling network interfaces…

==> core-01: Running provisioner: file…

==> core-01: Running provisioner: shell…

core-01: Running: inline script

登入你的coreos实例：

$ vagrant ssh

CoreOS stable (717.3.0)

core@core-01 ~ $

在vagrant up时，你可能会遇到如下两个错误：

错误1：

Progress state: VBOX_E_FILE_ERROR

VBoxManage: error: Could not open the medium storage unit '/home1/tonybai/.vagrant.d/boxes/coreos-stable/717.3.0/virtualbox/coreos_production_vagrant_image.vmdk'.

VBoxManage: error: VMDK: inconsistent references to grain directory in '/home1/tonybai/.vagrant.d/boxes/coreos-stable/717.3.0/virtualbox/coreos_production_vagrant_image.vmdk' (VERR_VD_VMDK_INVALID_HEADER).

这个问题的原因很可能是你的Virtualbox版本不对，比如版本太低，与**coreos_production_vagrant.box**格式不兼容**。可**尝试安装一下高版本virtualbox来解决。

错误2：

core-01: SSH address: 127.0.0.1:2222

core-01: SSH username: core

core-01: SSH auth method: private key

core-01: Warning: Connection timeout. Retrying…

core-01: Warning: Connection timeout. Retrying…

core-01: Warning: Connection timeout. Retrying…

coreos虚拟机创建后，似乎一直无法连接上。在coreos的github issue中，有人遇到了这个问题，目前给出的原因是因为cpu的支持虚拟化技术的vt开关没有打开，需要在bios中将其开启。这主要在安装64bit box时才会发生。

到这里，我们已经完成了一个single instance coreos虚拟机的安装。vagrant halt可以帮助你将启动的coreos虚拟机停下来。

$ vagrant halt

==> core-01: Attempting graceful shutdown of VM…

**三、 CoreOS**** cluster**

上面虽然成功的安装了coreos，然并卵。在实际应用中，CoreOS多以Cluster形式呈现，也就是说我们要启动多个CoreOS实例。

使用vagrant启动多个coreos实例很简单，只需将配置中的$num_instances从1改为n。

这里我们启用config.rb这个配置文件(将config.rb.sample改名为config.rb)，并将其中的$num_instances修改为3：

# Size of the CoreOS cluster created by Vagrant

$num_instances=3

该配置文件中的数据会覆盖Vagrantfile中的默认配置。

三个instance中的etcd2要想组成集群还需要一个配置修改，那就是在etcd.io上申请一个token：

$curl https://discovery.etcd.io/new

https://discovery.etcd.io/fe81755687323aae273dc5f111eb059a

将这个token配置到user-data中的etcd2下：

etcd2:

#generate a new token for each unique cluster from https://discovery.etcd.io/new

#discovery: https://discovery.etcd.io/<token>

discovery: https://discovery.etcd.io/fe81755687323aae273dc5f111eb059a

我们再来up看看：

$ vagrant up

Bringing machine 'core-01' up with 'virtualbox' provider…

Bringing machine 'core-02' up with 'virtualbox' provider…

Bringing machine 'core-03' up with 'virtualbox' provider…

==> core-01: Checking if box 'coreos-stable' is up to date…

==> core-01: VirtualBox VM is already running.

==> core-02: Importing base box 'coreos-stable'…

==> core-02: Matching MAC address for NAT networking…

==> core-02: Checking if box 'coreos-stable' is up to date…

==> core-02: Setting the name of the VM: coreos-vagrant_core-02_1437388468647_96550

==> core-02: Fixed port collision for 22 => 2222. Now on port 2200.

==> core-02: Clearing any previously set network interfaces…

==> core-02: Preparing network interfaces based on configuration…

core-02: Adapter 1: nat

core-02: Adapter 2: hostonly

==> core-02: Forwarding ports…

core-02: 22 => 2200 (adapter 1)

==> core-02: Running 'pre-boot' VM customizations…

==> core-02: Booting VM…

==> core-02: Waiting for machine to boot. This may take a few minutes…

core-02: SSH address: 127.0.0.1:2200

core-02: SSH username: core

core-02: SSH auth method: private key

core-02: Warning: Connection timeout. Retrying…

==> core-02: Machine booted and ready!

==> core-02: Setting hostname…

==> core-02: Configuring and enabling network interfaces…

==> core-02: Running provisioner: file…

==> core-02: Running provisioner: shell…

core-02: Running: inline script

==> core-03: Importing base box 'coreos-stable'…

==> core-03: Matching MAC address for NAT networking…

==> core-03: Checking if box 'coreos-stable' is up to date…

==> core-03: Setting the name of the VM: coreos-vagrant_core-03_1437388512743_68112

==> core-03: Fixed port collision for 22 => 2222. Now on port 2201.

==> core-03: Clearing any previously set network interfaces…

==> core-03: Preparing network interfaces based on configuration…

core-03: Adapter 1: nat

core-03: Adapter 2: hostonly

==> core-03: Forwarding ports…

core-03: 22 => 2201 (adapter 1)

==> core-03: Running 'pre-boot' VM customizations…

==> core-03: Booting VM…

==> core-03: Waiting for machine to boot. This may take a few minutes…

core-03: SSH address: 127.0.0.1:2201

core-03: SSH username: core

core-03: SSH auth method: private key

core-03: Warning: Connection timeout. Retrying…

==> core-03: Machine booted and ready!

==> core-03: Setting hostname…

==> core-03: Configuring and enabling network interfaces…

==> core-03: Running provisioner: file…

==> core-03: Running provisioner: shell…

core-03: Running: inline script

$vagrant ssh core-02

CoreOS stable (717.3.0)

core@core-02 ~ $

可以看到Vagrant启动了三个coreos instance。关闭这些instance，同样用halt：

$ vagrant halt

==> core-03: Attempting graceful shutdown of VM…

==> core-02: Attempting graceful shutdown of VM…

==> core-01: Attempting graceful shutdown of VM…

**四、小结**

以上仅仅是CoreOS最基本的入门，虽然现在安装ok了，但CoreOS的各种服务组件的功用、配置；如何与Docker配合形成分布式服务系统；如何用[Google Kubernetes](http://github.com/GoogleCloudPlatform/kubernetes)管理容器集群等还需更进一步深入学习，这个后续会慢慢道来。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Bringing machine ‘core-01′ up with ‘virtualbox’ provider…Bringing machine ‘core-02′ up with ‘virtualbox’ provider…Bringing machine ‘core-03′ up with ‘virtualbox’ provider…==> core-01: Box ‘coreos-stable’ could not be found. Attempting to find and install… core-01: Box Provider: virtualbox core-01: Box Version: >= 0==> core-01: Box file was not detected as metadata. Adding it directly…==> core-01: Adding box ‘coreos-stable’ (v0) for provider: virtualbox core-01: Downloading: http://localhost/box/coreos_production_vagrant.json core-01: Progress: 100% (Rate: 22000/s, Estimated time remaining: –:–:–)The box failed to unpackage properly. Please verify that the boxfile you’re trying to add is not corrupted and try again. Theoutput from attempting to unpackage (if any):bsdtar.EXE: Error opening archive: Unrecognized archive format这个问题可能是什么情况呢，帮忙分析下。

1、vagrant版本、virtualbox版本是否满足要求2、box下载是否完整？3、box是压缩文件，本地是否能解压？

你好，1、这是我的配置， 物理机OS: windows7 VirtualBox: Oracle VM VirtualBox Manager 4.1.6 Vagrant: Vagrant 1.7.4 CoreOS: stable 717.3.0 2、3都是好的。

用搜索引擎搜一下吧，看到有些人遇到和你类似的问题