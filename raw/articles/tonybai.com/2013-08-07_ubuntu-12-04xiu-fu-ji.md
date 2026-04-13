---
title: Ubuntu 12.04修复记
url: https://tonybai.com/2013/08/07/ubuntu-12-04-repairing-notes/
published: '2013-08-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Ubuntu 12.04修复记

今天一早发现[Ubuntu 12.04](http://tonybai.com/2012/12/04/upgrade-ubuntu-to-1204-lts/)坏掉了，于是用了大半天对其做了修复，修复过程十分坎坷，但结果还不错，遂记之以备忘。

*** 毁掉Ubuntu**

[Ubuntu](http://www.ubuntu.com)坏掉完全是由于我的错误决策。昨天一天Ubuntu桌面右上方的状态拦一直有一个红色的错误提示符，提示系统包冲突，建议执行sudo apt-get install -f解决。apt-get也提示索引冲突，无法卸载和安装任何包。于是执行了sudo apt-get install -f，虽然我不知道这个命令对系统做了哪些更改。但结果是那个错误提示符的确不见了。

不过等到晚上回家启动电脑后才发现笔记本的快捷键都不好用了。比如无法通过fn+f6 or f7对屏幕亮度进行调节（默认启动时是最大亮度，太刺眼，每次都要调）。更要命的是声音快捷键居然不好用了，而且其为关闭状态。并且状态栏上到小喇叭也无 法点击，“系统设置->声音”也根本打不开。没有声音，如何听歌看电影啊，于是乎想到了upgrade。

执行upgrade，有400多M的包要升级，于是让电脑自己升级，我去睡觉去了。今天早上起来发现Ubuntu upgrade ok了。重启、引导，似乎一切似乎很正常。但输入密码登录后，画面就始终停留在墙纸背景上了。啥都没有出现。快捷键依旧无法使用，反复重启几次均如此，超 级杯具了！

*** 重装Ubuntu**

上班后，试图用livecd引导修复Ubuntu，但ubuntu没有修复菜单选项，要么删除当前已经安装的ubuntu 12.04.2并重新安装，丢弃HOME路径下的数据；要么就是保持现有版本OS不动，新安装一个OS，原OS HOME路径下的数据不会有损失。我只能选择后者。这时我才发现，livecd在我的笔记本中发现的已有OS版本居然变成了ubuntu 12.10！靠，upgrade居然直接将12.04.2升级到了12.10。

原12.04.2安装在/dev/sda1分区，livecd将该分区拆分成两个分区，有点类似于Win7高级磁盘分区工具中对大分区的压缩，压缩后变成安装了老系统的/dev/sda1和新分区/dev/sda10，livecd在/dev/sda10上面安装新系统。

新Ubuntu很快就安装好了，重启后顺利的进入了桌面，一切正常。接下来又是老一套，恢复数据+装软件。

*** 自动挂接各分区**

由于采用的是默认安装，没有自定义挂接点，于是需要手工编写/etc/fstab文件，将诸多分区做自定义挂接，使之能在系统启动时自动挂接。

首先执行sudo blkid，查看各分区信息：

$> sudo blkid

/dev/sda1: UUID="d0d1424b-e3a8-43d9-887a-1c58c64ecff3" TYPE="ext3"

/dev/sda5: UUID="8bda8d60-b5cb-43aa-b408-dd6ce4957923" TYPE="ext3"

/dev/sda6: UUID="c415cf1c-624c-42ce-a8a6-6c072b5ee232" TYPE="ext3"

/dev/sda7: UUID="b8f6c810-bbb0-458c-8306-7b4a834ad726" TYPE="swap"

/dev/sda8: UUID="E208-E865" TYPE="vfat"

/dev/sda9: UUID="6BB3-FA39" TYPE="vfat"

/dev/sda10: UUID="1477776e-fe68-40f6-9804-c752b5efb149" TYPE="ext4"

接下来编辑/etc/fstab，该文件中swap分区以及前面的分区是系统安装时就设置好的。后面三个是我自己设置的：

# <file system> <mount point> <type> <options> <dump> <pass>

proc /proc proc nodev,noexec,nosuid 0 0

# / was on /dev/sda10 during installation

UUID=1477776e-fe68-40f6-9804-c752b5efb149 / ext4 errors=remount-ro 0 1

# swap was on /dev/sda7 during installation

UUID=b8f6c810-bbb0-458c-8306-7b4a834ad726 none swap sw 0 0

UUID=8bda8d60-b5cb-43aa-b408-dd6ce4957923 /home1 ext3 defaults 0 0

UUID=c415cf1c-624c-42ce-a8a6-6c072b5ee232 /home2 ext3 defaults 0 0

UUID=d0d1424b-e3a8-43d9-887a-1c58c64ecff3 /oldlinux ext3 defaults 0 0

重启后，就会发现，根目录下自动挂载了/home1、/home2和/oldlinux三个分区。别忘了对这几个挂载点做一下chown操作，这样你的用户才能对这些路径有写权限。

*** 恢复用户数据**

主要是迁移原home目录下的数据。在原系统中，我单独将一个分区挂接到/home路径上，其中的/home/tonybai设置为HOME路径。重装 os后，系统在/dev/sda10分区建立了/home/tonybai作为HOME目录。而之前的那个存放HOME路径的数据分区被我映射为 /home1了，但其中的数据完好无损。我于是打开/etc/passwd，将我的用户到home路径由/home/tonybai改为/home1 /tonybai，这样重新登录后，我又回到了熟悉的HOME环境中了。不过一些原先为/home/tonybai路径的配置需要修改为/home1 /tonybai了。

剩下的就是安装各种软件了。

*** 问题再现，有惊无险**

经过大半天的折腾，工作环境基本得以恢复。晚上回到家里，打算再补一些软件。结果刚进入Ubuntu就发现了异常：触控板失灵、无线网卡失灵、静音并无法 调节、指点杆失灵、所有快捷键失灵等。并且总是弹出对话框，提示系统错误，建议重启。重启若干次依旧是老样子。靠！这不又回到了最初的问题状态了吗。难道 还得推倒重来？

死马当活马医。试着执行一下sudo apt-get install -f，居然提示：用"sudo dpkg –configure -a"可以解决。遂按照后面的命令执行了一下。命令的效果是系统在重新配置包 – 所有包。执行完毕后，注销登录，发现大不相同了。重启后再看一下，一切恢复正常。估计又是我装了什么软件导致包依赖异常导致的。如果早知道dpkg –configure -a可以解决问题，我这大半天时间就可以专注于其他事情了，唉。

生命也许就在于折腾^_^！！！

再次提醒：用Ubuntu的童鞋apt-get update/install要谨慎，upgrade尽量就不要做了，成功率低得很！

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

“但输入密码登录后，画面就始终停留在墙纸背景上了。啥都没有出现。快捷键依旧无法使用，反复重启几次均如此，超级杯具了！”——之前也遇到这样的问题，一度转向其它发行版。现在我的Ubuntu 12.04每次开机也是这样，只好每次悲剧发生时，按Ctrl+Alt+F1登陆终端，执行sudo service lightdm restart。