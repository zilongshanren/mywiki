---
title: 关于Makefile.am中与Build相关的变量设置
url: https://tonybai.com/2010/10/26/about-variables-related-to-building-in-makefile-am/
published: '2010-10-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 关于Makefile.am中与Build相关的变量设置

今天尝试使用[autoconf和automake](http://tonybai.com/2010/09/26/hello-autoconf-and-automake/)重新构建一个遗留库的Build环境。之前改造的[lcut](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)的目录结构还是相对简单，改造时并未遇到什么难题，不过今天就没那么幸运了，我在头文件目录包含设置这个看似简单的环节上遇到了一些小麻烦。

这个库结构其实也没那么复杂，只是源文件和头文件不在一个目录下罢了：

testproj/

– Makefile.am

– configure.in

– include/

– xx.h

– yy.h

– module1

– xx.c

– Makefile.am

– moudle2

– yy.c

– Makefile.am


开始也没多想，参照以前的经验一步一步生成configure脚本。执行configure脚本生成Makefile文件，敲入make。在进入module1目录后，提示编译xx.c文件失败，无法找到xx.h！看了一下[gcc的编译选项](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)，的确没有-I上层的include目录，只有"-I."和"-I.."。翻看了一下automake的[manual](http://www.gnu.org/software/automake/manual)，发现[automake](http://www.gnu.org/software/automake/manual/automake.html#Program-Variables)默认情况下是将config.h所在的目录当作-I的参数。我的configure.in中是这样设置的:AC_CONFIG_HEADERS([config.h])，怪不得无法正确设置目录呢！将该句改为AC_CONFIG_HEADERS([include/config.h])后，重新生成Makefile并执行make，这回gcc命令行上出现了"-I../include"的字样，编译也很是顺利。

不过就这样算了，似乎总觉不妥，config.h只有一个，但如果有多个include目录的情况下该如何设置头文件包含目录呢？带着这个问题我再次翻看了automake的手册。老天不负有心人^_^，手册里确有这方面的说明。

原来automake从[autoconf](http://www.gnu.org/software/autoconf/manual)里继承了很多编译时需要的变量，诸如CC, CFLAGS, CPPFLAGS, DEFS, LDFLAGS,LIBS等等。但automake也可自己设置一些编译时用到的变量，automake与Build相关的一些变量名字也都以AM_开头，诸如AM_CPPFLAGS(与CPPFLAGS对应)。在Makefile.am中设置头文件包含的方式至少有以下两种：

* 在顶层Makefile.am中设置全局变量

AM_CPPFLAGS = -I $(top_srcdir)/include1

export AM_CPPFLAGS

这样在编译子目录（如module1)时，该全局设置也会起作用，在gcc编译命令行中你会看到-I ../include1。

* 在子目录层Makefile.am中设置局部变量

AM_CPPFLAGS = -I $(top_srcdir)/include2

这里的设置仅仅影响该目录下源文件的编译，对于其他同级目录下的源文件不起作用。另外如果此时顶层的Makefile.am中依然有AM_CPPFLAGS的设置，那么子目录下的Makefile.am中的这些设置会覆盖掉顶层的定义，在gcc编译命令行中也只会看到-I include2而无-I include1。

除了在Makefile.am中手工显式设置外，也可在执行configure脚本的时候通过传入CPPFLAGS参数来设定包含头文件位置，如configure CPPFLAGS=-I./include3。注意"CPPFLAGS"、"="和后面的值之间不能有空格。在[automake manual](http://www.gnu.org/software/automake/manual/automake.html#Flag-Variables-Ordering)中也有这方面的说明：在命令行中这里的CPPFLAGS将被放到AM_CPPFLAGS后面并一起传给gcc。

对于automake中的其他Build相关的AM_XXFLAGS变量，其道理也是相同的，这里就不赘述了。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论