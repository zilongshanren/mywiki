---
title: 使用autoconf解决可移植性问题
url: https://tonybai.com/2011/08/23/solve-portable-problem-with-autoconf/
published: '2011-08-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用autoconf解决可移植性问题

昨天在编译项目代码时遇到了这样一个错误：

xx_base.h:72:2: 错误：#error "One of _BIG_ENDIAN or _LITTLE_ENDIAN must be defined."

这是预编译器的错误输出。原因很明显：预编译器在处理xx_base.h时没有发现_BIG_ENDIAN或_LITTLE_ENDIAN的定义，#error预处理宏输出了如上错误。下面是出现错误位置的源码片断：

/* xx_base.h*/

#if defined(_BIG_ENDIAN)

… …

#elif defined(_LITTLE_ENDIAN)

… …

#else

#error "One of _BIG_ENDIAN or _LITTLE_ENDIAN must be defined."

#endif

xx_base.h是部门一基础库中的一个头文件，上面的做法对于基础库自身来说并无太大问题。基础库的Makefile通过检测CPU类型定义了对应的[字节序](http://tonybai.com/2005/09/28/also-talk-about-byte-order/)宏，并在编译时作为gcc的命令行选项传入：

/* Makefile */

ifeq ($(CPU), x86)

DEFS += -D_LITTLE_ENDIAN

else ifeq ($(CPU), sparc)

DEFS += -D_BIG_ENDIAN

else

$(error $(CPU) is not supported!)

endif

但是一旦这个基础库被某项目复用，且该xx_base.h文件被项目代码引用，编译就会出现问题，因为各个项目的Makefile中并没有定义_LITTLE_ENDIAN或_BIG_ENDIAN宏。如果基础库不做修改，那么复用该基础库的项目代码中就都需要考虑这两个宏的定义问题。这未免有些"强加"的意味，对于一个几乎被所有项目复用的基础库而言，这样的做法显然不妥。

那如何解决这个问题呢？一个思路是如果基础库在发布后依旧携带这些宏的定义，那就可以避免这样的问题了。在很多使用[autotools](http://tonybai.com/2010/09/26/hello-autoconf-and-automake/)(包括autoconf, automake, [libtool](http://tonybai.com/2010/12/14/create-libraries-with-libtool/)等)协助进行代码构建的开源包中经常会看到一个名为config.h的源文件，那里面包含了与移植相关的宏定义。这个config.h是[configure脚本](http://tonybai.com/2010/03/19/also-talk-about-solving-the-problem-of-configure-script/)根据config.h.in模板自动生成的。

我们的基础库如果完全用autotools改造显然也可以解决这个问题，但这样一来以前编写的一些构建脚本就要被全部抛弃，能否折中一下呢：利用autoconf生成config.h，但不输出Makefile，依旧使用原先的Makefile？

实验证明这样是可以的。只需对configure.in(或configure.ac)做一些调整即可，将类似AC_CONFIG_FILES([Makefile src/Makefile src/example/Makefile])这样的代码从configure.in中移除即可：

# -*- Autoconf -*-

# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.64])

AC_INIT([baselib], [1.0.0], [xx@gmail.com])

AC_CONFIG_HEADERS([include/config.h])

# Checks for header files.

AC_CHECK_HEADERS([stddef.h stdlib.h string.h])

# Checks for typedefs, structures, and compiler characteristics.

AC_TYPE_SIZE_T

# Checks for library functions.

AC_FUNC_MALLOC

AC_CHECK_FUNCS([memset])

AC_OUTPUT

AC_CONFIG_HEADERS这句是关键！修改完configure.in后，执行autoheader，我们就会在include下发现config.h.in模板文件被生成了出来。执行autoconf生成的configure脚本后，我们在include下就得到了config.h。

下面就是在config.h中加入我们期望的宏。在我们的问题中，我们希望在configure时可以探测到当前host所用的字节序(endianess)，并将结果反映到config.h中。幸运的是autoconf内置了字节序的[测试宏](http://www.gnu.org/s/hello/manual/autoconf/Existing-Tests.html#Existing-Tests)AC_C_BIGENDIAN。增加了AC_C_BIGENDIAN测试宏的configure.in经过autoheader处理后得到的config.h.in文件中多了如下这组代码：

/* Define WORDS_BIGENDIAN to 1 if your processor stores words with the most

significant byte first (like Motorola and SPARC, unlike Intel). */

#if defined AC_APPLE_UNIVERSAL_BUILD

# if defined __BIG_ENDIAN__

# define WORDS_BIGENDIAN 1

# endif

#else

# ifndef WORDS_BIGENDIAN

# undef WORDS_BIGENDIAN

# endif

#endif

在Sun SPARC小机上运行configure，我们得到的config.h中有关字节序的宏定义代码如下：

/* Define WORDS_BIGENDIAN to 1 if your processor stores words with the most

significant byte first (like Motorola and SPARC, unlike Intel). */

#if defined AC_APPLE_UNIVERSAL_BUILD

# if defined __BIG_ENDIAN__

# define WORDS_BIGENDIAN 1

# endif

#else

# ifndef WORDS_BIGENDIAN

# define WORDS_BIGENDIAN 1

# endif

#endif

config.h中定义了WORDS_BIGENDIAN宏，说明Sun Sparc小机采用的是BigEndian。这样只要基础库的头文件都在最开始包含了config.h，那么上面的问题就解决了。

不过有些朋友不喜欢WORDS_BIGENDIAN这个宏的命名，想自己给标识字节序的宏命名，比如BASELIB_IS_BIGENDIAN。那么我们如何来支持呢？这里我也找到了一个办法：

首先，就是手工编辑config.h.in(注意这之后你就不要通过autoheader生成config.h.in了)，在结尾加上这样一行：

#undef BASELIB_IS_BIGENDIAN

然后，修改configure.in，通过AC_DEFINE来定义一个新的BASELIB_IS_BIGENDIAN宏：

AC_C_BIGENDIAN

if test $ac_cv_c_bigendian = yes; then

AC_DEFINE(BASELIB_IS_BIGENDIAN, 1)

fi

我们通过AC_C_BIGENDIAN的检测结果来确定是否定义BASELIB_IS_BIGENDIAN宏，ac_cv_c_bigendian显然是AC_C_BIGENDIAN内置的一个变量，如果需要，我们也可以模仿其命名规则得到其他测试宏内置的变量。

最后，执行autoconf和configure，我们就可以在include/config.h的结尾看到这样一行定义：

#define BASELIB_IS_BIGENDIAN 1

AC_DEFINE不一定非要与测试宏绑定在一起，它的用法很灵活。如果我们的代码中需要根据不同操作系统的类型来调用不同的代码，那么我们需要在config.h中放置几个标识操作系统类型的宏，比如BASELIB_LINUX和BASELIB_SUNOS。和BASELIB_IS_BIGENDIAN一样，我们首先需要手工编辑config.h.in，增加如下两行代码：

#undef BASELIB_LINUX

#undef BASELIB_SUNOS

然后，修改configure.in，加入自定义的OS测试代码，并且定义对应的宏：

os=`uname -s`

case $os in

Linux)

AC_DEFINE(BASELIB_LINUX, 1)

;;

SunOS)

AC_DEFINE(BASELIB_SUNOS, 1)

;;

*)

AC_ERROR([host is unsupported.])

;;

esac

最后，执行autoconf和configure。如果我们在redhat上，我们就会在config.h中看到如下代码：

#define BASELIB_LINUX 1

/* #undef BASELIB_SUNOS */

autoconf也内置了一系列系统类型测试宏，比如AC_CANONICAL_SYSTEM(依赖install-sh、config.sub和config.guess三个脚本)，其测试后的结果放在了$host变量中，你也可以通过判断$host变量来确定到底在config.h中定义哪个宏。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论