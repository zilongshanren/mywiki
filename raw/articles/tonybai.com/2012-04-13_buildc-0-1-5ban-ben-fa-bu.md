---
title: buildc 0.1.5版本发布
url: https://tonybai.com/2012/04/13/buildc-0-1-5-release/
published: '2012-04-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.1.5版本发布

这两天对[buildc](http://code.google.com/p/buildc)的改动比较频繁，今天又修正了一些问题，也增加了一些小功能。主要包括这么几点：

1、在Make.rules.in中增加了STATIC_LIBS和DYNAMIC_LIBS

项目源代码和项目中

[单元测试](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)代码使用同一个Make.rules，也此编译时也就共享同一个LIBS变量。对于静态[共享库](http://tonybai.com/2010/12/13/also-talk-about-shared-library/)还好说，但对于动态共享库，诸如Oracle的instantclient库，单元测试代码中即使没有使用到动态共享库中的接口，也要对该动态共享库产生一个依赖。这样在执行单元测试用例时就会因无法寻得动态共享库而导致用例执行失败。为此，我在Make.rules.in中增加了STATIC_LIBS和DYNAMIC_LIBS两个变量，即将原LIBS变量中的静态共享库和动态共享库分开，分别放入STATIC_LIBS和DYNAMIC_LIBS中。然后让项目中单元测试代码的编译只依赖STATIC_LIBS，上述问题就得到了解决(如果你的单元测试真实需要链接动态共享库，那就另当别论了)。

2、添加system_libs，并进一步明确了external_libs、custom_libs和新增的system_libs的含义

buildc设计之初，设计了三种lib：external_libs、custom_libs和default_libs，最初的设想是这样的：

* external_libs – 一般配置第三方库或组织内部公共库；

* custom_libs – 项目相关的C运行库和*nix系统库依赖库，或一些项目内部实现的库；

* default_libs – C后台应用一般都需要链接的C运行库和*nix系统库，惯例优于配置，直接写死在代码中。

但实际运用时发现，custom_libs如果既配置C运行库或*nix系统库依赖库，又配置一些项目内部实现的库，会存在静态

[共享库依赖顺序问题](http://tonybai.com/2010/10/11/start-with-mock-malloc/)，另外custom_libs与external_libs之间也会因此而存在库链接顺序之问题。而default_libs目前为空，因为很难找到各个项目的一般依赖。于是这次我对这个设计进行了一些修正，增加了SYSTEM_LIBS，并进一步明确了这些lib配置的含义，依顺序如下：

* custom_libs – 一般配置项目自实现、自用的库，可能包含在项目源码库内部，与项目源码库一并发布；

* external_libs – 一般配置第三方库或组织内部的公共库；

* system_libs – 用来替代default_libs，配置项目需要的C运行时库或*nix系统库，放在所有库的最后面。

default_libs似乎没有太大必要了，后续也许会从代码中remove出去。

3、增加cache upgrade

通过实践发现，目前buildc提供的对本地缓存的Library的管理手段还有欠缺，特别是当.buildc.rc发生变更时，需要执行buildc cache remove和buildc cache init才能正确完成更新，稍显繁琐，因此今天给buildc增加了一个cache upgrade命令，用于改善这个情况。而buildc cache update一般仅用于.buildc.rc的库配置没有改变，但subversion库中的库二进制文件被更新(比如重新制作了)的情况。这样看来还是.buildc.rc变更的情况常见些，比如某个库的版本升级了(例如，

[lcut](http://code.google.com/p/lcut)从0.2.0升级为[0.3.0](http://tonybai.com/2012/04/10/lcut-0-3-0-release/))，或某个库的位置发生了变化，或删减了某些库或新增了某些库等等。© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论