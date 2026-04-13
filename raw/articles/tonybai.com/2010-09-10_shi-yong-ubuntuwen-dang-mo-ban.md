---
title: 使用Ubuntu文档模板
url: https://tonybai.com/2010/09/10/use-the-document-template-of-ubuntu/
published: '2010-09-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Ubuntu文档模板

每次[安装Ubuntu](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)后，主文件夹(你的$HOME目录)下都会默认建立起一些目录，诸如：下载、音乐、图片等，这些目录的用途通过其名字都可以猜个八九不离十，只有一个叫作“模板”的目录一直让我摸不到头脑。直到这次[彻底迁移到Ubuntu](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)，我才发现这个“模板”目录的妙用！

平时工作中常常需要新建一些文档，以前用Windows时都会使用右键菜单，点击“新建”，然后选择不同的文档类型。但在Ubuntu上却发现右键快捷菜单中“创建文档”的二级菜单项中默认只有"空文件”这一种文档类型，这显然不能满足我的需求！

在网上Google如何将更多文档类型添加到右键快捷菜单中。首先得到的答复是：[Ubuntu Tweak](http://ubuntu-tweak.com)可以做到。

启动Ubuntu Tweak，选择“个人设定”-> "管理模板“。这里有一堆"未启用的模板"，诸如.odt、.ods、Html文档等模板类型，你可以把你需要的模板拖到左侧”已启用模板“列表中。选择完后，你在右键菜单“创建文档”中就可以看到这些类型的文档模板了。

不过如何添加Ubuntu Tweak里没有包含的文档模板类型呢？继续Google！在[Ubuntu中文论坛](http://forum.ubuntu.org.cn)上我找到了最终答案：将你期望的文档模板放入“模板”文件夹即可。恍然大悟，原来“模板”目录的用途是这样的啊。

打开$HOME目录下的模板文件夹，发现刚刚使用Ubuntu Tweak拖拽过来的文档模板都存放在这里。把一个word_template.doc的Ms Word文件作为文档模板放入此文件夹，打开右键菜单，果然看到了"word_template.doc"的菜单项。点击该菜单项，一个新doc文件就创建成功了，其实Ubuntu就是将“模板”目录下的word_template.doc文档模板复制了一份供你使用。

这种灵活性让人大呼过瘾！因为你完全可以将自己定制的文档模板放入右键菜单中！比如：公司一般都有很多办公或设计的模板文件，需要时要么在本机找到这些模板文件Copy一份，要么到公司办公网络上下载一份新的。这样一来很多人(包括我^_^)常因无法找到存储模板文件的位置或记不住下载地址而浪费了很多时间！使用Ubuntu文档模板后你只需要将文档模板放入“模板”目录，下次你就可以通过右键菜单创建新文档了！如果你是C程序员，你也可以将一份定制好的.h或.c或Makefile文件放到右键菜单中。如果你的公司模板文件太多，都放在“模板”目录下会导致右键菜单显示过长，你可以通过在“模板”目录下建立分类子目录来解决这个问题。这些子目录也将出现在右键菜单中，并可级联打开下一级菜单，显示子目录下的文档模板列表。如此灵活的功能是Windows所无法提供的（起码我目前还不知道Windows中有类似功能^_^）。

这里顺便将近期使用Ubuntu时学到的一些技巧叨咕叨咕：

* 关于Ubuntu剪切板

与Windows上全局一个剪切板不同的是，Ubuntu上提供两个剪切板：一个叫Primary clipboard，通过标准的Ctrl+v(终端用Ctrl+Shift+c)/Ctrl+v复制和粘贴。而另外一个是Selection Clipboard，顾名思义，选择即复制，鼠标中键粘贴。遗憾的是这两个剪切板居然不能混合使用。Primary Clipboard的内容无法通过敲击鼠标中键粘贴，反之亦然。安装[Parcellite](http://parcellite.sourceforge.net/)(GTK+剪切板管理器）可以在一定程度上解决这个问题。安装后，在其"首选项"配置中将以下三项均选上：

-> Use Copy (Ctrl-C)

-> Use Primary (Selection)

-> Sync clipboards

这样两个剪切板的内容就可以共享了，即通过选择复制的内容，可以使用Ctrl+v粘贴了。

* apt-get代理设置

在单位通过公司代理上网，使用Ubuntu 9.04的时候，只需在.bashrc中配置http_proxy环境变量即可，apt-get可以顺利连接到Internet。但是换了Ubuntu 10.04后，http_proxy即使设置了，apt-get也无法连接到Internet。这个问题曾经一度无解，直到近期才找到答案：通过配置/etc/apt/apt.conf(若无此文件，则新建)达到为apt-get设置代理的目的。在apt.conf中添加如下一行：

Acquire::http::Proxy "http://user:pass@server:port";

* Gconf-editor

Ubuntu下也有一个类似注册表编辑器的工具：[gconf-editor](http://en.wikipedia.org/wiki/Gconf-editor)，用来对Gnome桌面环境和相关应用配置。其设置项目甚多，目前了解不多，这里就不深叨咕了^_^。

后记：短短两周的时间，部门内部已经相继有三位同事在各自的电脑中安装了Ubuntu 10.04，看来Ubuntu的魅力还是"不可小觑"的^_^。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论