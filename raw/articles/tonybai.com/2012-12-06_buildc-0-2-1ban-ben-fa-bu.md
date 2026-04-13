---
title: buildc 0.2.1版本发布
url: https://tonybai.com/2012/12/06/buildc-0-2-1-release/
published: '2012-12-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.2.1版本发布

[buildc 0.2.1版本](http://buildc.googlecode.com/files/buildc-0.2.1.tar.gz)是一个bugfix版本，修正了两个重要问题。

* 修正执行buildc pack –cmode=32-bit时无法创建32位安装包的问题

之前的buildc pack命令在打包安装程序时忽略了–cmode这个选项，这样即便传入32-bit这个参数，打出的安装包中的应用程序依旧是64位编译的。这次修正了这个问题，让buildc真正支持打32位程序的安装包。

* 修正buildc cache相关命令与cmode选项结合的问题

其实这是一个因当初设计考虑不周而遗留下来的问题。最初考虑[buildc](http://code.google.com/p/buildc)在一个Workplace下面要么只管理64-bit的库，要么只管理 32-bit的库，没有考虑支持两者都cache以及两者可分别管理。而现实开发中，我们的开发人员在自己的workplace下既有64位程序，也有 32位程序，这样在用到buildc时反倒比较麻烦，因此这次将buildc cache的管理命令与–cmode选项结合，做了新的定义：

– buildc cache init ： 根据.buildc.rc初始cache本地库，既初始下载64-bit库，也下载32-bit库；

– buildc cache init –cmode=64-bit : 根据.buildc.rc初始cache本地库，只初始下载64-bit库；

– buildc cache init –cmode=32-bit : 根据.buildc.rc初始cache本地库，只初始下载32-bit库；

– buildc cache update ：根据.buildc.rc更新本地cache库，既更新64-bit库，也更新32-bit库；

– buildc cache update –cmode=64-bit：根据.buildc.rc更新本地cache库，只更新64-bit库；

– buildc cache update –cmode=32-bit：根据.buildc.rc更新本地cache库，只更新32-bit库；

– buildc cache upgrade ：根据最新变更的.buildc.rc升级本地cache库，既升级64-bit库，也升级32-bit库；

– buildc cache upgrade –cmode=64-bit：根据最新变更的.buildc.rc升级本地cache库，只升级64-bit库；

– buildc cache upgrade –cmode=32-bit：根据最新变更的.buildc.rc升级本地cache库，只升级32-bit库；

– buildc cache remove ：根据.buildc.rc配置，删除本地cache库，既删除64-bit库，也删除32-bit库；

– buildc cache remove –cmode=64-bit：根据.buildc.rc配置，删除本地cache库，只删除64-bit库；

– buildc cache remove –cmode=32-bit：根据.buildc.rc配置，删除本地cache库，只删除32-bit库。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论