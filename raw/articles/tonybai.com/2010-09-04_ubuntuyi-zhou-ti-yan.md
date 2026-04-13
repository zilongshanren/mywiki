---
title: Ubuntu一周体验
url: https://tonybai.com/2010/09/04/one-week-experience-of-ubuntu/
published: '2010-09-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Ubuntu一周体验

[安装Ubuntu](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)已有一周多，无论是在工作单位还是在家里，Ubuntu都作为我的第一OS，Win7基本上处于被打入“冷宫”状态。事实证明对我来说，Ubuntu完全可以取代Windows。

公司提供有线和[无线网络](http://tonybai.com/2008/03/08/configure-wireless-router/)两种接入方式，对于致力于追求“理想的无线世界”的我来说，无线接入是我的第一选择。公司的无线接入采用[TTLS](http://en.wikipedia.org/wiki/Extensible_Authentication_Protocol)认证方式，在WinXP和Win7上都有相应的客户端([SecureW2](http://www.securew2.com))可供使用，但在Ubuntu上是否有此类客户端我还不知道，咨询了公司的IT服务部门，得到的回答也是“不知道”（想必在公司内部像我这样使用Linux OS的少之又少）。在网络上寻找答案也未果。我之前对无线接入认证那些术语了解甚少，甚至不知道公司采用的是哪种认证方式，但通过SecureW2官方站以及Wikipedia了解到了公司用的是TTLS认证。我无意中打开Ubuntu无线网络连接配置，在连接“编辑”对话框的“无线安全性”标签中居然看到了"隧道TLS"方式，难道Ubuntu内置就支持TTLS？于是我就按照Windows上的配置方式尝试配置了一下，包括密钥协议和内部认证等，点击连接，哇，居然真的连上了！打开[Firefox](http://tonybai.com/2008/12/17/accelerate-the-firefox-on-ubuntu/)测试了一下，一切OK，问题解决。我将配置方法简单写成了一个Mail发给了公司IT服务部门，希望能为公司其他同遇到这个问题的同事提供一些帮助。

Ubuntu默认采用的是Gnome桌面环境。Gnome近期最受关注的要属计划2011年发布的多次“跳票”的Gnome 3.0了，Gnome 3.0的一个核心组件就是[Gnome shell](http://live.gnome.org/GnomeShell)。网上有不少关于Gnome shell的抢鲜体验，其实通过Ubuntu自带的软件中心，大家都可以体验到Gnome Shell，软件中心提供的版本是2.28。安装后使用Alt+F2打开“运行”对话框，输入“gnome-shell –replace”即可启动Gnome shell，也许是之前看过一些抢鲜体验介绍的缘故吧，Gnome shell并未让我感觉有多惊艳。通过Alt+F2，输入debugexit即可退出Gnome shell。因为不是最终稳定版，所以建议不要将之作为默认窗口管理器。

我很喜欢收集电子书，本子里至少有几个G的电子书，不过有很多电子书是chm格式的，Ubuntu下无法打开。安装Wine后似乎自带了一个hh程序用来打开chm电子书，但是我试了一下打开失败。Google了一下，发现有很多Linux下阅读chm的工具，首先试着安装了一下[xchm](http://xchm.sourceforge.net)这个工具。工具不大，瞬间安装完毕，试了一本中文chm电子书，打开是没有问题，但是中文字符全部显示为乱码。我找了半天也没有设置[中文字符编码](http://tonybai.com/2007/11/03/also-talk-about-char-encoding/)的地方。又试了一下纯英文书籍，支持的很好！中文chm不能看，我心里总是不那么舒坦。在Ubuntu中文论坛上又有人介绍[chmsee](http://code.google.com/p/chmsee)这款小工具，又试了一下，这回中文算是没问题了，就是它了。

前两天尝试安装了一下[Macbuntu](http://sourceforge.net/projects/macbuntu)以体验一下Mac的风格主题界面，结果安装失败，只有登录界面改成Mac形式的了，其他界面主体丝毫没变，问题出在哪里并不清楚，关键是居然没有卸载选项，还搞的我的[GVIM](http://tonybai.com/2008/12/30/in-depth-study-vim/)一启动就自动退出，并提示："gtk warning Invalid input string"，后来在网上找到了解决方法：

cd /usr/share/vim/vim72/lang

sudo ln -s menu_zh_cn.utf-8.vim menu_zh_cn.utf8.vim

难不成Macbuntu修改了中文区域设置？

今天在[奶牛博客](http://www.nenew.net/)上看到Macbuntu版本更新到v2.1了(之前装的是v2.0)，抱着侥幸的心理又试一下，这回似乎又进了一步，桌面、Firefox都换成了Mac主题，不过所有的菜单上的中文文字后面都莫名其妙的出现了许多“方格”，十分难看。还好v2.1版本提供uninstall功能，遂回退了。这次回退后Gvim居然也没有问题。

Launchy一直用的很好，但是不知最近安装或卸载了什么软件，每次启动Launchy，都提示Alt+Space的热键已经被占用，但是通过“首选项”->“键盘快捷键”查看，并没有那个程序占用了Alt+Space，诡异的是Launchy也仅仅给个提示，提示后Alt+Space依旧绑定在Launchy上，照用不误！

用wine1.2运行secureCRT，导致secureCRT界面实在是很丑陋！后来干脆都不咋使用secureCRT了，直接在本机编写代码，后来一想：Linux本来就是用来写代码的，还用什么secureCRT啊！

在[Ubuntu中文论坛](http://forum.ubuntu.org.cn)上看到10.04版的[Ubuntu官方桌面教程中文版](http://people.ubuntu.com/~happyaron/udc-cn/)已经发布，对于我这样的Ubuntu新手来说浏览一遍官方教程还是大有裨益的。另外发现官方中文Wiki有一页讲解的都是[Ubuntu的操作Skills](http://wiki.ubuntu.org.cn/UbuntuSkills)，值得细致品读。

另外找了一本电子书"[Ubuntu – Powerful Hacks and Customizations](http://book.douban.com/subject/4810836/)"，打算花几天读完它，争取早日摆脱初级选手的这顶帽子^_^。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论