---
title: 使用Libtool创建库文件
url: https://tonybai.com/2010/12/14/create-libraries-with-libtool/
published: '2010-12-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Libtool创建库文件

除了[autoconf和automake](http://tonybai.com/2010/09/26/hello-autoconf-and-automake/)，GNU的autotools工具包中还有一种工具，它就是[libtool](http://www.gnu.org/software/libtool/libtool.html)。顾名思义，libtool是一个关于库文件制作、安装和使用的工具，它屏蔽了各个平台在库制作、安装和使用方面的差异，为上层提供了统一的接口。你可以直接使用libtool创建静态或共享库，也可以将libtool与autoconf、automake结合在一起使用。第二种方式显然更具实际意义，也更为简单。

在一个使用[autoconf](http://www.gnu.org/software/autoconf/autoconf.html)和[automake](http://www.gnu.org/software/automake/automake.html)构建的编译环境中添加libtool的支持，只需改动几处即可：

首先，你需要在configure.in(或configure.ac)中添加AC_PROG_LIBTOOL宏(注意：去掉AC_PROC_RANLIB宏)。

其次，修改Makefile.am：

如果是建立库文件，则需将lib_LIBRARIES改为lib_LTLIBRARIES，同时将库的后缀名由.a改为.la，这将告诉automake采用libtool来创建相关库：

lib_LIBRARIES = libfoo.a => lib_LTLIBRARIES = libfoo.la

libfoo_a_SOURCES = libfoo.c => libfoo_la_sources = libfoo.c

如果是使用上面生成的库文件，则将可执行程序链接的库改为.la，如：

fooapp_SOURCES = fooapp.c

fooapp_LDADD = libfoo.la

更新完上述配置后，删除aclocal.m4，执行aclocal和autoreconf，此时如果你的系统中没有安装libtool的话，autoconf会提示"undefined macro AC_PROG_LIBTOOL"，安装libtool(sudo apt-get install libtool)后，错误提示消失。autoreconf会初始化libtool环境，并将libtool和ltmain.sh两个脚本拷贝到你的工程目录下。由于修改了Makefile.am，你还需要重新执行依次automake。

后面的操作大家就很熟悉了，configure -> make -> make install。libtool默认状态下会将静态库(.a)和共享库(.so)都生成出来，不过你可以通过configure命令行参数来控制这一切：

–disable-shared 不生成共享库

–disable-static 不生成静态库

–enable-shared 生成共享库

–enable-static 生成静态库

你同样可以在configure.in中控制创建的库的类型，比如，在configure.in中增加AC_DISABLE_SHARED宏就可以让libtool只创建静态库，而不生成共享库。

执行make install将库安装完后，你会发现在安装的lib目录下还保留有一份.la文件，通过该.la文件，我们可以继续通过libtool来使用这些库。当然你也可以完全略过.la而直接链接静态库(.a)和共享库(.so)。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论