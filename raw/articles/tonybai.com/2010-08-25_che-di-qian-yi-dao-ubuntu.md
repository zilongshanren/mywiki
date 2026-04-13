---
title: 彻底迁移到Ubuntu
url: https://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/
published: '2010-08-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 彻底迁移到Ubuntu

自从知道[Ubuntu](http://tonybai.com/2006/01/23/got-the-ubuntu-disc/)这个linux发行版后，就有了彻底迁移到Linux上的想法。但迫于各种各样的因素一直未能下定决心，这期间Ubuntu发行版已经从6.10进化到了10.04。经过长时间(近四年，时间长的的确有些夸张^_^)的准备，再借着Ubuntu 10.04 LTS发布的东风， 我终于下决心彻底走进Ubuntu的世界。

[安装Ubuntu](http://tonybai.com/2008/02/17/install-ubuntu-7-10-the-first-time/)对我来说已经是驾轻就熟的事情了，这里也没什么好说的。对我来说，迁移到Ubuntu的主要工作集中在：

1、完成两个平台数据共享和迁移

2、选择和安装用于替代Windows上常见应用的软件

Ubuntu在与Windows分区互操作方面作了很多工作，Ubuntu下打开Windows分区与访问Ubuntu分区基本没什么区别，无论是NTFS还是FAT32(vfat)分区，保存在Windows分区中的数据都可以直接被访问和使用。

我平时使用最多的就是文本文件了，在Windows下使用GVIM或记事本打开;在Ubuntu下可继续使用GVIM(gedit已经被我卸载)。当然,VIM需要做一些字符集转换方面的设置才能保证对文件中的中文字符做正确的转换，具体如何配置可参考我的[上一篇文章](http://tonybai.com/2009/09/28/also-talk-about-vim-charset-configuration/)。

平时工作中最常用的沟通方式就是Mail了，之前在Windows下使用Thunderbird收发Mail。当初之所以舍弃Outlook而转用Thunderbird也是为今天转移到Linux上工作做的准备，因为只有Thunderbird才能很好的支持在多个平台间共享数据，共享数据的配置方法可参考我去年写的一篇[关于thunderbird的文章](http://tonybai.com/2009/11/20/cross-platform-configuration-of-thunderbird/)。

之前在[体验Ubuntu9.10](http://tonybai.com/2009/11/16/upgrade-to-ubuntu-9-10/)时知道了iBus这个新输入法框架，当时的体验还不错，不过使用10.04后，发现Gvim/Vim和iBus有冲突，在Vim下Insert模式和Normal模式切换时iBus提词窗口总是自动退出，严重影响输入效率，后换成[fcitx](http://www.fcitx.org)后冲突解决。

公司的办公软件早在年初就都切换到OpenOffice 3.0上了，公司的所有模板、通启也都以OpenOffice的文件格式发布了，所以在日常文档编辑和数据交换方面不存在什么问题。不过对于Microsoft专有格式的Project和Visio我目前还没有找到合适的替代品。

日常开发过程中，组内同事喜欢使用[Feiq](http://www.feiq18.com)作为内部即时通信工具，可惜Feiq只有Windows版本，我曾经尝试用Wine 1.2去装载和运行Feiq，但都提示错误。无奈下，只能选择[iptux](http://code.google.com/p/iptux)。iptux采用的是以前飞鸽传书(ipmsg)的协议，只支持文字和文件传输，不支持在对话框中直接贴图。

思维导图软件近几年很受大家欢迎，之前一直在使用MindManager。迁移到Ubuntu上后，急需找到一款MindManager的替代品，而且还必须可以打开MindManager格式的文件。[XMind](http://www.xmind.net)恰是我所需要的。测试了一下，使用习惯和界面布局与MindManager差不多，且导入MindManager的文件也很顺利。

[tortoriseSVN](http://tortoisesvn.tigris.org/)想必是每个使用svn作为代码版本控制工具的程序员必装的一款svn客户端软件，功能很强大，易用性也很好。不过在Ubuntu下可没有这么好的运气，也曾尝试过用Wine运行TortoriseSVN，但以失败告终。看见Ubuntu软件中心中有一款名为RapidSVN的工具，安装试用了一下，发现与TortoriseSVN差距很大，在没有找到更好的软件之前，先凑合用着。

Windows优化大师之类的软件我是一概不会安装的，但在Ubuntu下，国人开源的一款工具[Ubuntu Tweak](http://ubuntu-tweak.com)值得支持一下。特别是对linux桌面和窗口配置还不是很熟悉的情况下。

注重实效(pragmatic)的程序员都会在电脑里安装一款能帮助快速打开程序、快速定位文件的程序。Ubuntu下有Gnome Do，但是我更喜欢[Launchy](http://www.launchy.net)，之前在Windows上就用Launchy。现在发现Launchy也有Ubuntu版本，这样就不须重新学习了。

公司的某些OA系统对Firefox的支持很差，于是我下载安装了[Chromium Web Browser](http://www.chromium.org)，这个浏览器的体验不错，而且上述问题也得到了解决。不过由于使用[Firefox + Vimperator](http://tonybai.com/2009/09/20/vimperator-plugin-for-firefox/)时间久了，习惯了用一个'd'关闭一个标签页的VIM化的快捷命令，我暂时只将Chromium作为备份浏览器使用。

公司办公以台式机居多，这样在开会的时候我们会经常通过远程桌面访问到自己的PC上; Ubuntu内置远程桌面访问工具，而且可以命令行操作，rdesktop -f ip -u USER_NAME -p PASSWD即可直接进入你的PC桌面，就好比你在操作你自己的机器一样。你可以在.bashrc中用alias给上面命令串起个别名，这样只需敲入一串别名即可完成远程登录和操作了。

上周安装Ubuntu 10.04.1后，曾经有一种删除本子上Win7的冲动，但后来还是将Win7保留了下来。因为还有一些操作是在Ubuntu下无法做到的，比如说招行专业版。另外国内很多知名站点（如中国网络电视台）对非IE浏览器的支持都不好，有些时候你还不得不使用IE。

Ubuntu 10.04总体来说还是很稳定的，不过在使用过程中也有一些小插曲，比如：XWindows曾两次提示重启，点击确定后，N长时间也无法回到GUI界面，无奈只能重启系统。再比如：Ubuntu接投影后，桌面只能显示出2/3区域，似乎是我安装的Docky出现了什么问题。关闭Docky后，一切OK。

适应Ubuntu Linux的过程还在继续，希望过了磨合期后一切都会越来越好^_^。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

有几位同事最近也转投Ubuntu的怀抱：）

gnome下有一个和nautilus集成的, gnubversion

没有好一些的java的IDE啊。eclipse直接卡到爆。忍痛又回到window了

很可能是X Windows在响应方面效率不高所致。