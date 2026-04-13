---
title: buildc 0.1.8版本发布
url: https://tonybai.com/2012/07/02/buildc-0-1-8-release/
published: '2012-07-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.1.8版本发布

[buildc](http://code.google.com/p/buildc/)这个小工具逐渐在项目组内部扩大了使用范围，还有一名专门的同事负责为每个项目制作[安装包](http://tonybai.com/2012/02/10/add-packing-feature-to-buildc/)工程，这样也可以在使用中发现buildc的问题。

本次[buildc 0.1.8](http://buildc.googlecode.com/files/buildc-0.1.8.tar.gz)的相关修正以及新增的feature就是我的这位年轻同事一手操刀完成的，他也是一个python新手，同样也是边翻手册边进行编码的。这次改动主要集中在templates目录下的几个文件，这里的文件多为因工程的不同而异的。

这次buildc主要的功能点改动如下：

1、删除Make.rules模板中的FOPTIMIZE变量

原先在模板中将FOPTIMIZE变量的值写死为o2。但在实际应用中，不是所有项目都会使用o2优化级别，通过在buildc.cfg中自定义变量也可以达到同样的效果，因此这里删除了该变量。

2、为setup.py.in增加了backup功能、log facility等

setup.py.in这个文件改动较大，主要包括：

- 在setup.py.in这个安装包模板中增加了backup命令，用于将目标服务器上运行的老版本应用环境进行打包备份处理。该命令支持两个参数all和conf，分别用于备份打包全部环境和打包配置文件目录；

- 将setup.py中原install命令的参数full改为'all'；

- 为setup.py的执行过程增加了log facility，可以在"install_时间戳.log"中看到所有详细的安装过程；

- 当目标路径存在与安装包要安装的文件同名的文件时，setup.py.in会自动生成这两个同名文件的diff，供安装人员后续手动进行冲突解决。

3、提供一个deps_check.py的更为详尽的参考实现

deps_check.py是用于在目标环境进行环境约束检测的，十分必要。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论