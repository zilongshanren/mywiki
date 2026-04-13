---
title: 将Unity换成Gnome3
url: https://tonybai.com/2012/12/06/replace-unity-with-gnome3/
published: '2012-12-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 将Unity换成Gnome3

[Ubuntu 12.04](http://tonybai.com/2012/12/04/upgrade-ubuntu-to-1204-lts/)已经体验一天多了，Unity还是用的不大习惯，左侧的程序启动栏感觉还是别扭，以前用windows的时候就不喜欢将任务栏放在左侧或右侧； 应用窗口的菜单栏融合到桌面顶端也没给我太多惊喜；总而言之，给自己找几个换回[Gome](http://www.gnome.org)的理由还是很容易的^_^。况且Gnome也发生了巨变， 由传统的Gnome2更新到了全新的Gnome3，正好我也想体验一下Gnome3，于是继续折腾。

Ubuntu 12.04.1官方源里就有Gnome3，因此只需执行sudo apt-get install gnome-shell即可安装Gnome3。Gnome3还有一个高级配置工具，可以执行sudo apt-get install gnome-tweak-tool安装。安装后注销，在登录窗口选择Gnome桌面即可。

Gnome3默认桌面十分简洁，除了左上角的“活动”之外，别无它物。据说Unity也是基于Gnome开发的，只是比Gnome3多了一个左侧 程序启动栏（虽然也可以隐藏，但试过，感觉十分不灵敏）。我并未删除Unity，主要是担心删除后可能会给系统带来不稳定性。

点击“活动”后展现的界面我还是蛮喜欢的：中间是所有打开的窗口缩略图，左边是应用收藏夹，与Unity左侧的程序启动栏类似。右侧是半隐藏的 “工作区”栏。最下方是隐藏了主界面的程序的图标栏，该栏是自动隐藏的，将鼠标指针放到屏幕右下角时，该栏会出现。另外通过Win快捷键可以直接 打开“活动”主界面，十分方便。“活动”界面中的搜索框还可以作为程序启动器来用。

Gnome3默认取消了窗口中的最大、最小化按钮，不过利用gnome-tweak-tool这个高级配置工具可以恢复最大、最小化按钮：打开 tweak工具，找到shell -> arrangement of buttons on the titlebar，选择all即可。

Gnome3的切换窗口快捷键Alt + Tab将相同程序的不同窗口叠加在一起，这个我不甚喜欢，还得动用方向键选择，我更喜欢所有窗口不分类别的平铺。对于处理这种折叠窗口的情况，我更喜欢用 Win键打开“活动”界面，然后在上面选择我需要的窗口。

Gnome3窗口最大化的快捷键为“ctrl + win + 上箭头”，但我还没发现最小化的快捷键。

Gnome3的文件管理器左侧的快捷方式边栏似乎不能像Gnome2那样自定义快捷方式，这样无法快速访问常用的一些文件夹。

Gnome3的体验暂且就是这些，后续还待慢慢挖掘。

另外这两天还针对Ubuntu 12.04做了一些改造：

* 用Clipit替换Parcellite

我的Parcellite启动后，无法在提示栏显示出小图标，无法对其进行配置，也就无法做剪切板的同步。后安装了Clipit，它是 Parcellite的一个分支，功能与Parcellite一致。用apt-get install即可。

* 安装OpenJDK

本想安装Oracle提供的JDK的，但无奈从Oracle提供的链接下载太慢，只能以OpenJDK替代。据说Oracle后续JDK也是基于 OpenJDK的，只是额外加上了一些私有代码。

sudo apt-get install openjdk-7-jre openjdk-7-jdk

$ java -version

java version "1.7.0_09"

OpenJDK Runtime Environment (IcedTea7 2.3.3) (7u9-2.3.3-0ubuntu1~12.04.1)

OpenJDK Client VM (build 23.2-b09, mixed mode, sharing)

* SunPinyin配置

SunPinYin默认不支持逗号和句号键翻页，执行/usr/lib/ibus-sunpinyin/ibus-setup- sunpinyin可以重新配置翻页键；同理用/usr/lib/ibus-pinyin/ibus-setup-pinyin也可以对默认携带 的拼音输入法进行设置。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论