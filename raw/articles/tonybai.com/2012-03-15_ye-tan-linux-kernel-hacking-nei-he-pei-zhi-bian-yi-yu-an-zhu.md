---
title: 也谈Linux Kernel Hacking – 内核配置、编译与安装
url: https://tonybai.com/2012/03/15/linux-kernel-hacking-series-kernel-config-compile-and-install/
published: '2012-03-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈Linux Kernel Hacking – 内核配置、编译与安装

* Linux Kernel之于C程序员，就好比世界之巅珠穆朗玛之于专业登山客。* — Tony Bai^_^

记得2006年初我曾花了些时间研究Linux Kernel，但后来迷失在了Linux Kernel

[引导阶段](http://tonybai.com/2006/02/08/retired-bootsect/)，无法自拔，最终选择了"知难而退"。如今，随着我们的产品越来越多地运行在[Linux](http://tonybai.com/tag/Linux)主机上，我又愈发感觉自己对Linux底层了解得不够深入，于是我又一次开启了[Linux Kernel Hacking](http://www.kernelnewbies.org/KernelHacking)的征程。经过这几年的发展，Linux Kernel变得更加复杂了，版本也从当时的2.6.x演进到今天的3.2.x(3.3正在开发中)。但相应地，Linux Kernel方面的资料也多了许多，这对我的Hacking显然是利好消息，至少目前手头上就有几本"大砖头"可作为参考(Linux Kernel方面的书籍均具有防身之特性^_^)。

这次Hacking前先给自己设定了几个目标(也算是想清楚为何要这么做)：

* 追溯本源

用Linux内核运转原理解释上层应用的行为并指导上层应用的开发。

* 定制优化

在对Linux Kernel有了深入了解之后，尝试定制适合产品特性的Linux内核。

* 走进内核开发，尝试提交补丁

对我个人来说，这算是在Linux Kernel领域的终极目标了。每天重复念叨这个目标，就相当于给自己打鸡血了，让自己始终保持兴奋劲儿。

以上这些目标显然不是短期内能达成的，饭还得一口一口吃，路还得一步一步走。今天我就迈出这第一步：编译一个属于自己的Linux内核。

经过这么多年的发展，Linux Kernel的编译已经简化了许多了，甚至简化到了让我觉得有些吃惊的地步(在我原先的意识中，Linux Kernel的编译是件很复杂的事情^_^)。

编译内核是Linux Kernel开发者的基本活动，几乎所有Kernel开发者都是在自己编译的内核上工作的。下面我就详细说明一下Linux Kernel的配置、编译和安装过程。

一、准备工作

1、准备一台装有Linux的PC

不建议在Windows或

[Solaris](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/)下编译Linux Kernel，那样只会自找麻烦。Linux Kernel在Linux下编译才是正路(除非你真的要做跨平台交叉编译)。我这里用了一台运行在[XenServer](http://en.wikipedia.org/wiki/XenServer)5.6 p2上的装有Red Hat Enterprise Linux(RHEL) 5.5的虚拟机。在该虚拟机上执行'uname -r'，可以得到当前Linux内核版本信息为：2.6.18-194.el5xen。2、获取内核源码包

Linux Kernel，特别是之前发布的稳定版内核，几乎都可以100%的顺利通过编译。为了能与手头资料"兼容"，我选择了2.6.28版本内核。Linux Kernel的发布版本可在http://www.kernel.org/pub/linux/kernel下找到，这里执行下面命令获取源码：

wget -c http://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.28.tar.gz

下载后的源码包无需放在系统目录(/usr/src/linux)下，在你自己的普通权限用户下建立一个临时目录存放源码包即可，比如我们在/home/tonybai下建立linux-kernel目录，将下载的linux-2.6.28.tar.gz放入该目录中，解压后(tar xvzf linux-2.6.28.tar.gz)，我们会看到：

/home/tonybai/linux-kernel$ ls

linux-2.6.28/ linux-2.6.28.tar.gz

3、检查编译内核所依赖的工具及版本是否满足要求

在linux-2.6.28/Documentation/Changes中有该版本内核编译所依赖的工具以及最低版本信息列表，需确认一下当前主机上是否安装了这些工具，版本是否满足最低要求。通过linux-2.6.28/scripts/ver_linux可以快速获取当前主机上各个工具以及当前版本的信息，可将这些信息与编译该内核的最低版本比对，以确定是否需要安装或升级工具版本。

二、配置内核

Linux Kernel的编译有些类似于那些使用

[autotools](http://tonybai.com/2010/09/26/hello-autoconf-and-automake/)创建构建脚本的开源包，需要先Configure，然后make和make install。不同的是Linux Kernel的"Configure"要稍显"复杂"，毕竟与普通开源包相比，Linux Kernel算得上是一个庞然大物了。不过Linux Kernel的开发者们显然在这方面也做了很多工作，通过提供各种命令和默认配置来简化配置过程，下面是常用的几个配置命令。* make config

这个是最基本的配置命令，同时也是配置过程最复杂、耗时最长的配置命令。该命令会将Linux Kernel所有配置项逐一在控制台窗口输出，并让你作出yes、no或是module的选择。我查看了一下RHEL 5.5的配置项个数，总共有2300多项，想必这个过程下来，你已经筋疲力尽了。所以除了某些特殊情况，我们是不会使用这个命令的。该命令会在linux-2.6.28目录下面创建一个.config隐藏文件，该文件存储了你的配置选择，类似这样：

# .config

#

# Automatically generated make config: don't edit

# Linux kernel version: 2.6.28

# Wed Mar 14 17:13:23 2012

#

# CONFIG_64BIT is not set

CONFIG_X86_32=y

# CONFIG_X86_64 is not set

CONFIG_X86=y

CONFIG_ARCH_DEFCONFIG="arch/x86/configs/i386_defconfig"

CONFIG_GENERIC_TIME=y

… …

* make defconfig

一个一个选择配置太累，内核开发者显然也不原意这样做，因此内核提供了另外一个命令make defconfig。这个命令会为你生成一份默认的.config文件，而整个过横无需你作出任何选择。而实际上该命令是直接将arch/x86/configs/i386_defconfig或x86_64_defconfig(以x86平台为例)拷贝为.config放在linux-2.6.28下面。

* make menuconfig

虽然有了默认配置，但开发者总是有修改配置的需求。内核提供了make menuconfig命令，允许开发者以图形界面(基于

[ncurses](http://en.wikipedia.org/wiki/Ncurses))的形式修改特定的配置项。根据大家的喜好不同，内核还提供了基于gtk+图形界面的make gconfig和基于X11图形界面的make xconfig来修改配置项，这两个命令在功用上与make menuconfig是等同的。另外还有一种方法配置内核，那就是直接使用Linux发行版自带的.config或其他开发者的.config来配置你的内核。如果你是第一次配置内核，建议直接使用所在主机的Linux的.config。我所用的Linux的.config文件在/usr/src/kernels/2.6.18-194.el5-xen-x86_64下面。不过由于我下载的Kernel版本是2.6.28，与该.config不匹配，所以还需执行'make

oldconfig'命令来更新配置。该命令会保留.config已有的配置项的值，而对于新Kernel版本引入的新配置项提供交互式的选择。我用的就是这种方法：

$ make oldconfig

scripts/kconfig/conf -o arch/x86/Kconfig

#

# configuration written to .config

#

三、编译内核

配置好内核后，我们就可以执行内核编译了，和上层应用一样，只需一个Make就好。

$ make

… ..

CC arch/x86/boot/tty.o

CC arch/x86/boot/video.o

CC arch/x86/boot/video-mode.o

CC arch/x86/boot/version.o

CC arch/x86/boot/video-vga.o

CC arch/x86/boot/video-vesa.o

CC arch/x86/boot/video-bios.o

LD arch/x86/boot/setup.elf

OBJCOPY arch/x86/boot/setup.bin

OBJCOPY arch/x86/boot/vmlinux.bin

HOSTCC arch/x86/boot/tools/build

BUILD arch/x86/boot/bzImage

Root device is (8, 1)

Setup is 10988 bytes (padded to 11264 bytes).

System is 3561 kB

CRC f4d6ad54

Kernel: arch/x86/boot/bzImage is ready (#1)

Building modules, stage 2.

MODPOST 3 modules

CC arch/x86/kernel/test_nx.mod.o

LD [M] arch/x86/kernel/test_nx.ko

CC drivers/hid/hid-dummy.mod.o

LD [M] drivers/hid/hid-dummy.ko

CC drivers/scsi/scsi_wait_scan.mod.o

LD [M] drivers/scsi/scsi_wait_scan.ko

整个编译过程(非跨平台交叉编译，只是本地编译)大约20多分钟，编译成功后，我们得到了许多新文件，其中重要的文件有：

linux-2.6.28/vmlinux

linux-2.6.28/System.map

linux-2.6.28/arch/x86/boot/bzImage

其中bzImage就是我们编译好的可引导的、压缩的Linux内核映像文件。而System.map则是内核符号表文件，vmlinux是未经压缩的内核文件。

四、安装内核

安装内核与配置、编译内核不同，它需要root权限。切换到root后，我们首先需要安装的是内核模块，内核模块将会被安装到/lib/modules下面：

$make modules_install

… …

$ls -l /lib/modules/

总计 8

drwxr-xr-x 6 root root 4096 11-17 15:14 2.6.18-194.el5xen/

drwxr-xr-x 3 root root 4096 03-14 08:58 2.6.28

接下来就可以安装内核了。不过在安装之前，我们先看看当前系统内核文件是什么样子、Grub的配置又是怎样的：

$ ls -l /boot

-rw-r–r– 1 root root 66548 2010-03-17 config-2.6.18-194.el5xen

-rw——- 1 root root 3397337 11-17 15:14 initrd-2.6.18-194.el5xen.img

-rw-r–r– 1 root root 1208685 2010-03-17 System.map-2.6.18-194.el5xen

-rw-r–r– 1 root root 2047518 2010-03-17 vmlinuz-2.6.18-194.el5xen

-rw-r–r– 1 root root 417317 2010-03-17 xen.gz-2.6.18-194.el5

-rwxr-xr-x 1 root root 969808 2010-03-17 xen-syms-2.6.18-194.el5

$ vi /boot/grub/grub.conf

#boot=/dev/hda

default=0

timeout=5

splashimage=(hd0,0)/grub/splash.xpm.gz

hiddenmenu

title Red Hat Enterprise Linux Server (2.6.18-194.el5xen)

root (hd0,0)

kernel /xen.gz-2.6.18-194.el5 crashkernel=128M@32M

module /vmlinuz-2.6.18-194.el5xen ro root=/dev/VolGroup00/LogVol00 rhgb quiet

module /initrd-2.6.18-194.el5xen.img

可以看出vmlinuz-*这个文件就是内核映像文件，它其实就是arch/x86/boot/bzImage的拷贝；但我们无法通过直接压缩vmlinux来得到vmlinuz-*，据说vmlinuz在头部放置了gzip的解压代码。

我们通过make install进行内核安装：

$ make install

sh /home/tonybai/linux-kernel/linux-2.6.28/arch/x86/boot/install.sh 2.6.28 arch/x86/boot/bzImage System.map "/boot"

make install调用的是对应arch下提供的install.sh来安装内核。arch/x86/boot/install.sh检测系统中是否安装了installkernel脚本，如果有则调用installkernel工具安装内核，否则进行默认安装。至少在Red Hat的发行版上我们是可以找到installkernel这个脚本的。installkernel除了将bzImage和System.map安装到/boot下之外，还调用了/sbin/new-kernel-pkg制作了initrd-2.6.28.img，并修改了grub.conf(使用grubby配置grub)的内容：

$ ls -l /boot

-rw——- 1 root root 3369458 03-14 08:59 initrd-2.6.28.img

lrwxrwxrwx 1 root root 33 03-14 10:41 System.map -> /boot/System.map-2.6.28

-rw-r–r– 1 root root 1397880 03-14 08:58 System.map-2.6.28

lrwxrwxrwx 1 root root 30 03-14 10:41 vmlinuz -> /boot/vmlinuz-2.6.28

-rw-r–r– 1 root root 2080528 03-14 08:58 vmlinuz-2.6.28

$ vi /boot/grub/grub.conf

default=1

timeout=5

splashimage=(hd0,0)/grub/splash.xpm.gz

hiddenmenu

title Red Hat Enterprise Linux Server (2.6.28)

root (hd0,0)

kernel /vmlinuz-2.6.28 ro root=/dev/VolGroup00/LogVol00 rhgb quiet

initrd /initrd-2.6.28.img

title Red Hat Enterprise Linux Server (2.6.18-194.el5xen)

root (hd0,0)

kernel /xen.gz-2.6.18-194.el5 crashkernel=128M@32M

module /vmlinuz-2.6.18-194.el5xen ro root=/dev/VolGroup00/LogVol00 rhgb quiet

module /initrd-2.6.18-194.el5xen.img

make install虽然对grub.conf进行了修改，但默认引导的内核依旧是原先的内核，我们需要手工将default改为0来引导我们新编译的2.6.28内核。

五、引导新内核

安装了新内核后，我们尝试使用新内核引导启动。执行Reboot后，新内核引导一切顺利。用'uname -r'查看结果如下：

$ uname -r

2.6.28

至此，我们成功用上了自己编译的内核(后续应该会有关于内核引导阶段的详细Hacking描述^_^)。

六、升级内核

升级内核是内核开发者的日常活动之一。当有其他开发者发布新补丁或自己在现有内核上做了修改后，都会重新配置、编译和安装内核，也就是升级内核。

升级内核一般按如下如下命令序列执行：

$ make oldconfig

$ make

$ make install(如果有kernel module更新，应该先执行make modules_install)

对于版本号不变的内核重新执行install，我们会在/boot下看到如下内容：

$ ls -l /boot

-rw——- 1 root root 3369458 03-14 08:59 initrd-2.6.28.img

lrwxrwxrwx 1 root root 33 03-14 10:41 System.map -> /boot/System.map-2.6.28

-rw-r–r– 1 root root 1397880 03-14 08:58 System.map-2.6.28

-rw-r–r– 1 root root 1397880 03-14 08:51 System.map-2.6.28.old

lrwxrwxrwx 1 root root 30 03-14 10:41 vmlinuz -> /boot/vmlinuz-2.6.28

-rw-r–r– 1 root root 2080528 03-14 08:58 vmlinuz-2.6.28

-rw-r–r– 1 root root 2080528 03-14 08:51 vmlinuz-2.6.28.old

安装脚本会将上一次安装的2.6.28内核改名为2.6.28.old，然后将新内核安装到/boot下。grub.conf内容没有被修改。再次反复执行install，安装脚本始终会将老内核改名为.old，然后保证最新同版本内核被安装。

七、定义自己的个性化内核版本号

XenServer下的Rhel 5.5的内核版本号为2.6.18-194.el5xen，Ubuntu 10.04下的内核版本号为2.6.32-30-generic(通过uname -r查看)，我们如何定义一个属于自己的个性化内核版本号呢？其实很简单，修改顶层Makefile即可。

# Makefile

VERSION = 2

PATCHLEVEL = 6

SUBLEVEL = 28

EXTRAVERSION = -tonybai-dev

一个Kernel的版本号KERNELVERSION = $(VERSION).$(PATCHLEVEL).$(SUBLEVEL)$(EXTRAVERSION)，因此我们可通过修改EXTRAVERSION的内容来定义一个个性化的版本号，就像上面代码中的那样。

修改Makefile后，执行make clean; make ;make modules_install; make install即可。执行后，你就会在/boot下面、/lib/modules下面以及grub.conf里面看到2.6.28-tonybai-dev这个版本的内核信息了。修改grub.conf使之默认引导2.6.28-tonybai-dev这个新内核，重新引导后，你执行'uname -r'的结果就会变成'2.6.28-tonybai-dev'了。

至此，内核配置、编译与安装的部分就暂时告一段落了。在这个过程中，我参考了许多资料，这其中包括：

相信后续的Hacking过程中，这些资料还将会发挥至关重要的作用。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Why compile a new kernel? For what?