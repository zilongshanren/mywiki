---
title: Hello，autoconf和automake
url: https://tonybai.com/2010/09/26/hello-autoconf-and-automake/
published: '2010-09-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Hello，autoconf和automake

部门绝大多数的产品都运行在Sun的小型机上，底层的操作系统是[Solaris](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/)。这两年公司开始主推[刀片机](http://en.wikipedia.org/wiki/Blade_server)(物美价廉^_^)，不过刀片机上运行的也是Solaris 10 for x86版本。基于同种OS的前提下在Sparc和x86两种体系之间做移植比较简单，主要考虑[字节序问题](http://tonybai.com/2005/09/28/also-talk-about-byte-order/)就可以了。不过对于可移植性的考虑不足还是让我们付出了较大的工作量。 在即将进行的新版本产品开发中，可移植性依旧没有被列入到必须要考虑实现的特性列表中，不过从未来产品演化和发展的角度考虑，现在就应该未雨绸缪，在可移植性方面多下工夫！

对于用C语言实现的服务器后端程序而言，[GNU](http://www.gnu.org)(/'gnu:/)的[autoconf](http://www.gnu.org/software/autoconf/)和[automake](http://www.gnu.org/software/automake)([GNU autotools](http://www.lrde.epita.fr/~adl/autotools.htm)工具包的主要组成部分)显然已经成为这方面的事实标准！诸多知名开源应用和工具都采用autoconf和automake来生成相关的Build环境，"configure -> make -> make install"是采用这两个工具的应用软件的标准编译安装流程。不过autoconf和automake的学习门槛却不低，记得几年前曾尝试学习过这两个工具，结果被其纷繁芜杂的依赖关系搞得晕头转向，加之当时缺少些许耐心，也就放弃了（估计很多人都有与我类似的经历^_^）。

autoconf，顾名思义是用来做“自动配置”的，配置什么呢？配置软件代码包，目的是用来使软件包适应种类繁多的“Posix-like system"。automake，则是用来生成Makefile的原型-Makefile.in的。在大工程里，各种依赖关系纠结，如果采用纯手工编写Makefile方式，复杂度很高，而且Makefile的学习门槛也不低，想写出一份扩展性良好的通用Makefile也非易事。automake则试图将程序员从那些"扯不断理还乱"的依赖关系中解脱出来，你只需告诉automake你的工程里有哪些源文件、哪些目标文件、要连接什么库及各个文件的位置即可，automake帮你自动生成一份Makefile.in，Makefile.in则是[configure脚本](http://tonybai.com/2010/03/19/also-talk-about-solving-the-problem-of-configure-script/)自动生成Makefile过程的输入。

重新学习使用autoconf和automake，最重要的就是迅速获得一个正反馈！这就好比学习一门新的计算机编程语言，如果能在3分钟之内迅速写出一个["Hello World"](http://en.wikipedia.org/wiki/Hello_world)程序，编译运行成功，并在屏幕上看到有"Hello World"输出，那么有了这个正反馈后你八成才会有继续学习的动力，否则很多耐性不足的人就会止步于此（例如很多Java语言初学者就止步于配置JDK环境变量上）。

我将这个“正反馈”寄托在使用autoconf和automake来migrate一个几年前写的小工具库上了。这个工具库没比"hello world"复杂多少^_^，其大致组织结构是这样的:

lcut/

– src/

– apr_ring.h

– lcut.h

– lcut.c

– example/

– runtests.c

autoconf和automake虽然名字中都有一个"auto"，但这并不意味着不需要任何“手工”操作。你起码需要手工完成两个文件：configure.in和Makefile.am。configure.in全工程只有一个，放置在工程最顶层目录下。这个文件包含一系列autoconf测试宏，用于告知autoconf生成的configure脚本需要在目标主机上做哪些check工作;至于Makefile.am，看文件后缀也可以知道这个文件是给automake使用的。Makefile.am可以有多个，简单来说只要你想在哪个目录下放置一个Makefile就需要在这个目录下编写一个对应的Makefile.am。Makefile.am的功用前面提到过，它要比Makefile简单许多，层次也更高，有些类似一种"[声明式(declarative)语言](http://en.wikipedia.org/wiki/Declarative_programming)”的脚本，你无须告知它怎么做，只需告知它要做的事情是什么样子的即可。

增加configure.in和Makefile.am后的源码包组织形式如下(新增文件用'+'标识)：

lcut/

+ configure.in

+ Makefile.am

– src/

– apr_ring.h

– lcut.h

– lcut.c

+ Makefile.am

– example/

+ Makefile.am

– runtests.c

configure.in的生成是“半自动”的。GNU提供了一个名为autoscan的工具以帮助生成一个configure.in的模板。在lcut的目录下运行autoscan –verbose，我们得到一个名为configure.scan的文件，并得到autoscan的运行日志如下：

tonybai@tonybai-ubuntu-laptop:~/lcut$ autoscan –verbose

autoscan: srcdir = .

cfiles: src/apr_ring.h src/lcut.h src/lcut.c src/example/runtests.c

makefiles:

shfiles:

function:

malloc: src/lcut.c:132 src/lcut.c:203 src/lcut.c:241

memset: src/lcut.c:139 src/lcut.c:209 src/lcut.c:247

header:

stddef.h: src/apr_ring.h:40

stdlib.h: src/lcut.h:45

string.h: src/lcut.c:17

identifier:

size_t: src/lcut.h:214 src/lcut.c:78

program:

cc: src/apr_ring.h src/lcut.h src/lcut.c src/example/runtests.c

makevar:

librarie:

可以看出autoscan将lcut下的各类文件做了个全面扫描，根据其内部规则找出带有移植性问题的函数、头文件以及标识符等，并在configure.scan中放置了对应的autoconf测试宏，configure.scan的初始版本内容如下：

AC_PREREQ([2.65])

AC_INIT([FULL-PACKAGE-NAME], [VERSION], [BUG-REPORT-ADDRESS])

AC_CONFIG_SRCDIR([src/apr_ring.h])

AC_CONFIG_HEADERS([config.h])

# Checks for programs.

AC_PROG_CC

# Checks for libraries.

# Checks for header files.

AC_CHECK_HEADERS([stddef.h stdlib.h string.h])

# Checks for typedefs, structures, and compiler characteristics.

AC_TYPE_SIZE_T

# Checks for library functions.

AC_FUNC_MALLOC

AC_CHECK_FUNCS([memset])

AC_OUTPUT

将configure.scan直接改名为configure.in(或configure.ac)，我们就得到了configure.in的模板，剩下的工作就是根据需要修改该模板了。configure.in文件包含一组autoconf测试宏，关于这些测试宏的具体含义可参考GNU [autoconf手册](http://www.gnu.org/software/autoconf/manual/)。这里仅针对某些宏做简要说明：

-> AC_PREREQ 这个宏是一个指示符，用于告知autoconf该configure.in需要的最低autoconf版本号是多少，上面例子中版本号是2.65，如果你用低于2.65版本的autoconf来处理configure.in，就会提示版本太低。

-> AC_INIT和AC_OUTPUT这两个宏标识着configure.in主体(body)内容的开始和结束，两个宏都可以接收一些options(参见[manual](http://www.gnu.org/software/autoconf/manual/))。

-> AC_CONFIG_SRCDIR 则是放置在configure脚本中的一个safety检测，用于检查特定文件的存在性，以确保软件包本身结构的正确性。

-> AC_CONFIG_HEADERS 指示需要输出config.h，config.h是configure过程输出的结果之一，其内容为一组#define directive，你的源件包代码可以包含config.h(在所有其他header files的前面)并使用这些directive来编写一些具有良好移植性的代码。

上述configure.in模板不完全能满足我们的要求，所以我们需要对configure.in内容进行修改，修改后的configure.in如下：

AC_PREREQ([2.65])

AC_INIT([lcut], [0.1], [bigwhite.cn@gmail.com])

AM_INIT_AUTOMAKE([foreign -Wall -Werror])

AC_CONFIG_SRCDIR([src/apr_ring.h])

AC_CONFIG_HEADERS([src/config.h])

AC_CONFIG_FILES([Makefile src/Makefile src/example/Makefile])

# Checks for programs.

AC_PROG_CC

# Checks for libraries.

AC_PROG_RANLIB

# Checks for header files.

AC_CHECK_HEADERS([stddef.h stdlib.h string.h])

# Checks for typedefs, structures, and compiler characteristics.

AC_TYPE_SIZE_T

# Checks for library functions.

AC_FUNC_MALLOC

AC_CHECK_FUNCS([memset])

AC_OUTPUT

以下对修改的地方做一些简要说明：

-> AM_INIT_AUTOMAKE 初始化automake并告知automake打开所有警告，另外[将警告视为错误](http://tonybai.com/2010/09/05/view-warning-as-error/)，注意：这里的-Wall -Werror虽和GCC的某些options名字相同，但这只是巧合，这里的-Wall -Werror并不是给gcc传递-Wall和-Werror选项，这两个选项是针对automake本身的。foreign选项则是告知automake此软件包非GNU软件包，不必严格遵循GNU软件包的标准，比如软件包必须包含ChangeLog、AUTHORS等文件。

-> AC_CONFIG_FILES 则是告知需要生成并输出相关文件，上面的AC_CONFIG_FILES([Makefile src/Makefile src/example/Makefile])与 AC_OUTPUT([Makefile src/Makefile src/example/Makefile])是等价的。

-> AC_PROG_RANLIB 在需要生成.a静态链接库的软件包中都要加上这个宏。

configure.in告一段落，下一个需要手工编辑的是Makefile.am。在这个lcut的例子里，我们需要三个Makefile.am(如上面的规划所描述)。 顶层Makefile.am内容如下：

SUBDIRS = src src/example

src/Makefile.am内容如下：

lib_LIBRARIES = liblcut.a

liblcut_a_SOURCES = lcut.c

include_HEADERS = apr_ring.h lcut.h

src/example/Makefile.am内容如下：

noinst_PROGRAMS = runtests

runtests_SOURCES = runtests.c

runtests_LDADD = $(top_srcdir)/src/liblcut.a

这里的Makefile.am相对比较简单，其语法格式在[automake manual](http://www.gnu.org/software/automake/manual)里有详尽说明，这里不重述。值得一提的是noinst_XX，对于不需要安装(install)的可执行程序、静态库等，都使用noinst_XX作为前缀描述。另外top_srcdir是内置的全局变量，可直接使用。

configure.in和Makefile.am都已经具备，只欠“东风”了，下面的Makefile生成操作都是“auto”的了。

首先在源码包顶层目录下使用autoheader生成config.h.in，在例子里我们的config.h.in放置在src下了;

然后同样在源码包顶层目录下运行aclocal，aclocal将根据configure.in生成aclocal.m4;

最后运行autoconf，configure脚本被自动生成; 运行automake，我们得到所有Makefile.in。

Build环境就此初步搭建完毕。运行"configure -> make -> make install"，我们顺利的得到了安装后的库，example下的runtests程序运行也OK。以上脚本在[Ubuntu 10.04](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)和Solaris 10 for x86下均测试通过。另外Ubuntu linux默认自带了全部autotools工具，这让我的学习过程变得更加轻便顺畅了！

我们再按照顺序回顾一下使用autoconf和automake的步骤：

-> 策划你的项目目录结构，将编写好的第一版源码文件放到各个位置上;

-> 在顶层目录下运行autoscan获得configure.in模板 (configure.scan->configure.in)

-> 手工编辑configure.in，满足个性化需要

-> 手工建立并编辑各个层次的Makefile.am

-> 在顶层目录下运行autoheader，生成相应config.h.in

-> 在顶层目录下运行aclocal，生成aclocal.m4

-> 在顶层目录下运行autoconf，生成configure

-> 在顶层目录下运行automake，生成各级Makefile.in

autoconf和automake很是强大，以上也仅仅算是学到了这两个工具的一些皮毛。面对更加复杂的软件包，学习和实践还在继续！

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论