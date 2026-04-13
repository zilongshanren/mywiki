---
title: 升级到Ubuntu 12.04LTS
url: https://tonybai.com/2012/12/04/upgrade-ubuntu-to-1204-lts/
published: '2012-12-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 升级到Ubuntu 12.04LTS

[Ubuntu 10.04 ](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)LTS已经伴随我两年了，经过我这么长时间的折腾，Ubuntu早已不堪重负^_^。在未升级前，Ubuntu 10.04已经表现出诸多问题：

- 在家中连接无线路由器时间漫长，且经常掉线；

- 在公司用有线网络经常掉线；

- 由于反复安装软件，系统中残留较多垃圾数据；

- Ubuntu 10.04官方源中的软件版本都有些低，很多软件手工安装高版本比较费力；

另外原先与Ubuntu 10.04共存的Windows 7系统已经早在大半年前就罢工了，无法引导进入，原因不明，我也懒得去fix，平时根本也用不到Windows系统。因此这次升级系统还有另外一个目的， 那就是将Windows 7的残余数据彻底清除出我的本本。

虽然Ubuntu最新版本是刚刚发布不久的12.10，但本着只用LTS版的原则，这次打算升级12.04 LTS，目前的最新版本是12.04.1。

原以为我的老旧的ThinkPad X60可以安装64位的12.04，但在安装时引导程序提示X60的CPU不是X86-64类型的，而是一颗双核的i686 CPU。恼火啊！下载和刻录一个iso容易吗，尤其在公司这个代理网络里！无奈只能重新折腾，重新下载和刻录32位的Ubuntu 12.04.1。

安装方法这里不赘述了。这次在安装时我使用了安装界面上可选的自定义安装分区的方法将12.04安装到了原Windows 7的分区中了，但安装结束重启后，Grub2的引导初始页面居然依旧显示以前的系统菜单，并且菜单中并没有我新装的12.04菜单项。重新安装，这次格掉 了原Ubuntu 10.04的安装分区。经过漫长等待后重启机器，映入眼帘的是"grub rescue>"，引导再次失败，显而易见，Grub2依旧没有找到正确的引导分区。

Google了一把，原来是我对Grub2的引导原理理解还不够，Grub2是两阶段引导。直接格式化原有分区并安装新系统并未重新刷新 MBR(主引导记录)中的第二阶段引导分区的id，因此机器启动后，MBR依旧按原有的配置去寻找那个分区ID，但装有Ubuntu的分区ID已 经发生了变化，原引导分区被重新格式化并且无系统，因此Grub2无法找到分区，无法开启第二阶段引导。

无奈只能使用livecd，进入terminal，执行如下命令（ubuntu 12.04安装在sda1）：

> sudo mount /dev/sda1 /mnt

> sudo grub-install –boot-directory=/mnt/boot /dev/sda

再次重启后，系统引导正常，终于可以进入12.04了。网上说利用grub rescue命令也可以刷新MBR记录，不过我没能试验成功。

不同Ubuntu的配置过程大同小异，我早已轻车熟路了：

- 添两个源：搜狐和网易的ubuntu 12.04的源，然后更新软件包列表；

- 打开更新管理器，设置首选软件源；

- 打开“语言支持”，下载和更新语言包；

- 安装Google Chrome、Vim、iptux、rdesktop、Filezilla、subversion、htop、git、golang、apache2、 parcellite等工具；

- Thunderbird配置恢复(Ubuntu 12.04已经将[thunderbird](http://tonybai.com/2011/03/21/upgrade-thunderbird/)作为默认mail客户端)；

- 恢复用户配置，包括.bashrc、[模板](http://tonybai.com/2010/09/10/use-the-document-template-of-ubuntu/)、vim配置和插件等；

- 恢复hosts、apache2等配置；

Ubuntu演进到今天，对中文的支持已经很好了。默认情况下的iBus拼音已经很好用了。更新完语言包后，输入法变成SunPinyin，用起 来的确比小企鹅输入法智能多了。

Ubuntu默认的桌面环境是自行开发的Unity，至少目前感觉还行，其Dash程序启动器比较好用，基本可以替代原先在Gnome下用的 launchy。不过对于我用的X60 12寸普通屏幕(非宽屏)来讲，左边的Dock启动栏显然占据了应用本已不大的界面空间。

Ubuntu 12.04配置与应用安装时遇到了两个问题，这里做个分享和备忘：

1、ext3分区自动挂载以及权限问题

这次安装时，原安装ubuntu 10.04的分区被重新格式化了，但并未挂载目录。系统启动后，该分区未被自动挂载，只能手动挂载。于是尝试通过修改/etc/fstab自动挂载该ext3分区。

root下建立/home1目录，在/etc/fstab中添加一行，将该分区自动挂载到/home1：

# / was on /dev/sda3 during installation

UUID=1ed84fc1-5ba2-4e82-94f5-c3e4f5654036 /home1 ext3 defaults,errors=remount-ro 0 0

重启后，该分区如预期一样被自动挂载。但有出现了新问题，该分区下无法用普通用户权限创建文件，也就是没有写权限。反复改了几次fstab中的挂载参数， 都无法解决。后想到既然分区已经挂载到了/home1目录，那修改/home1目录的权限是否可以解决这个问题呢？于是sudo chmod 777 /home1。命令执行完后重启。新分区自动挂载，并可写了。

2、恢复iptux默认配置

部门都用飞秋作为内部IM工具。Linux下的feiq协议兼容工具是iptux。Ubuntu 12.04下用apt-get就可以正确安装iptux，运行也一切OK。但我在配置iptux时，无意中选择了“启动后主面板自动隐藏”，导致始终无法 看到iptux主界面，也就无法发送消息。于是开始尝试恢复iptux的默认配置。

直接上方法：

- 后台杀掉iptux；

- cd ~/.gconf/apps/iptux

- 删除iptux配置文件

- 执行gconftool-2 –recursive-unset /apps/iptux

注意如果不用上面方法，即便是卸载再重装iptux也是无济于事的。

© 2012 – 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

上mac吧，别浪费时间吓折腾了。

就是爱折腾，哈哈。对苹果的产品总不是很感冒，呵呵。