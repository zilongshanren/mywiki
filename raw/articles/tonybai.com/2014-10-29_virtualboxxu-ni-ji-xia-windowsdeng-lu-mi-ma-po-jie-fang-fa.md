---
title: VirtualBox虚拟机下Windows登录密码破解方法
url: https://tonybai.com/2014/10/29/crack-windows-logon-password-under-virtualbox/
published: '2014-10-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# VirtualBox虚拟机下Windows登录密码破解方法

近两年虚拟机的发展给开发人员带来了极大便利，安装一个新环境，只需从别人那里copy一份虚拟机文件即可，分分钟搞定。我之前一直在[Ubuntu](http://tonybai.com/tag/Ubuntu/)下工 作，Windows偶尔使用，于是在Ubuntu[ VirtualBox](http://virtualbox.org/)下安装了一个Windows 7。今年将工作环境迁移到Mac Air下了，但偶尔也有Windows的使用需求，于是直接从我原来的[Ubuntu](http://tonybai.com/2012/12/04/upgrade-ubuntu-to-1204-lts/)下将Win7的Vdi文件Copy到Air上，便直接可以使用Win7 了，省去了重新安装Win7以及庞大的Office组件的工作。

前两天，打开Mac Air下的VirtualBox，启动Win7虚拟机，在Win7登录界面输入密码后，系统提示我密码错误。反复输入多次，将我常用的密码都试了一遍依旧 无法进入。我只能在原Ubuntu下临时用用Win7。但毕竟在Air上没有Win7十分不便，一些Word, PPT文档需要在两天机器上传来传去。无奈下，我都由了重新在Air下安装一个Win7甚至是Win8的打算了。

今天又有一个PPT编写的task，这件事再次被提上日程。我换了下思维：能不能破解一下Win7登录密码呢？于是求助度娘（谷哥离去好久了）。还别说， 还真是有破解方法，多数是通过PE工具盘快速修改登录密码。但PE工具盘挺大（几百兆，公司下载不便），我的又是虚拟机环境，这种方法不是我的菜啊。于是 又看到另外一种思路：通过某个Linux livecd或安装盘引导，mount windows分区，将C:\Windows\System32\cmd.exe改名为osk.exe。osk.exe是虚拟键盘程序。在Win7登录页 面的左下角可以启动这个虚拟键盘程序。一旦我替换成功，启动虚拟键盘程序就变成了启动Win7命令行程序。有了命令行，我们就可以通过net user命令查看当前账户列表、重置某个用户的password了。思路很清晰，是我的菜。

在我的Ubuntu机器上倒是有几个Linux发行版的live cd iso文件，比如ubuntu 14.04.1 desktop, centos7 desktop，不过个头都太大了，传到我的Air上还是很费劲的。我想最好有一个tiny的linux发行版。度娘告诉我有很多选择。我首先选了[Tiny Core Linux](http://distro.ibiblio.org/tinycorelinux/)， TinyCore-5.4.iso才不到14M。于是打开Win7虚拟机的“设置”页面，将 TinyCore-5.4.iso作为虚拟iso“插入”IDE光驱。TinyCore的启动就是秒秒的事情。TinyCore的桌面风格模仿Mac OS，桌面下方放置了一个dock条。TinyCore自带mount tools，打开后，用鼠标点击sda2，sda2盘符由红变绿，说明mount成功。

打开TinyCore的Terminal程序，进入/mnt/sda2，本想安装方案修改cmd.exe的名字，但Tiny Core提示：这是个Read-Only Filesystem。显然这是个只读mount。于是各种尝试读写挂在（包括修改/etc/fstab、mount -a, mount -o remount等），都无法改变Read-Only Filesystem的事实，于是放弃。

换国人的发行版：[CDLinux](http://cdlinux.info/wiki/)，这个发行版似乎已经不再更新，最新版本 CDlinux_mini-0.9.7.1.iso，发布时间是2012年3月18日。CDLinux的Size比TinyLinux稍大些，36M。 CDLinux启动略慢，并且只是Console Only（标准版带有桌面环境），没有图形桌面。进入命令行后，执行一下mount命令，发现/dev/sda2居然是rw方式挂载载/media /xxx下的，于是进入该目录，尝试touch test.txt，完全没有问题。

于是按照方案说明，将C:\Windows\System32下的osk.exe备份一下，将cmd.exe改名为osk.exe。

将光盘盘片删除，启动Win7，进入登陆页面时，点击左下角“轻松访问”按钮，选择“不使用键盘键入”，确定。命令行窗口弹出。

在命令行窗口执行net user 查看用户名列表。我的用户名是tonybai，再通过net user tonybai newpassword重置tonybai的密码。执行成功后，用新密码登陆，顺利进入Win7 Desktop。Crack成功！

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论