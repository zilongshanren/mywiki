---
title: C语言项目构建管理辅助工具 – buildc
url: https://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/
published: '2011-12-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# C语言项目构建管理辅助工具 – buildc

这几年我一直从事[C语言](http://tonybai.com/tag/C)项目的开发。这些项目的规模都不算小，少则十几万代码，多则几十万行代码，至少也都算得上是中型项目吧。项目构建工具使用的是传统的Make工具，构建脚本都是自行编写的，构建时直接在顶层目录下敲入make即可。

这种传统的构建方式其实是很耗时费力的。比如执行make之前你需要根据项目代码的实际路径重新设定一些环境变量或修改Makefile中的某些标识路径的变量；你还要将项目依赖的各种内部公共库、第三方开源库悉数找到，并安装在指定目录下，修改Makefile中这些第三方库的路径配置。只有做完这些后，你才能顺利地执行Make。以后每当你更换一个环境，你就要将上面的步骤重复执行一遍。有的项目第三方依赖较多，要完整地搭建一个项目构建环境所耗费的时间也是很惊人的，特别是对一些不熟悉项目构建的新人更是如此。另外随着产品被要求具备在多个平台上运行的能力，你的构建脚本还要支持在多个平台上的构建，你要为项目所依赖的第三方库准备多个平台的版本；当某个依赖库版本进行了升级，你还要手工在多个环境下进行更新。

为了使项目构建更加容易，我们曾经对Makefile脚本进行了改进，比如自动判断和设定当前顶层路径、自动判定当前项目代码所在的平台，并根据不同平台设定不同的变量值；甚至将项目依赖的第三方库放入[subversion](http://tonybai.com/2011/03/23/also-talk-about-solving-the-svn-conflicts/)服务器，构建项目时通过Shell脚本自动checkout对应平台的依赖库并链接。这些改进都是有效的，但在修改了多个项目后，我们发现了坏味道，那就是在不同项目的Makefile中充斥着大量重复性的脚本代码，这让后续构建脚本的维护十分困难，在一个项目中修正了构建脚本的bug后，很容易遗忘另外几个项目中存在着同样bug。此外每次构建都重新下载项目依赖的第三方库会导致构建变的十分缓慢。

我们在构建中遇到的问题大致就是这么多了。估计很多人会问：你们为何不用[autotools](http://tonybai.com/2010/09/26/hello-autoconf-and-automake/)生成的configure来生成项目构建脚本？为何不用[scons](http://tonybai.com/2008/12/14/learn-scons/)等更加高级的构建工具呢？我的回答是即使使用了这些工具依旧无法解决现有的所有问题。比如利用configure->make可以屏蔽掉一些平台移植的问题，但依旧无法解决第三方库依赖的问题。scons我也试用过，但了解不甚深入，我的印象中它的主要功用是简化构建脚本的编写，让大家从Makefile那纷繁复杂的源文件依赖关系中解脱出来，至于在区别平台以及解决第三方库依赖方面估计也无能为力；另外还有一个原因那就是让大家从已经十分熟悉的构建模式中转到scons的成本也是不小的。

我们的问题其实并非构建脚本的编写问题，而是构建环境的管理问题。autotools和scons所解决的问题属于前者，即构建脚本的编写问题。而解决C语言项目构建环境管理的工具我了解的不多，在互联网上也没有google到。在这方面Java项目倒是有一个很好的工具 – [Maven](http://maven.apache.org)。利用Maven可以做很多事情，我对其了解不多，这里也不多说，但这里提到Maven是因为它的一个Feature启发了我，这个Feature就是对第三方依赖包的管理。虽说C项目依赖的第三方开源包也越来越多，但与Java项目相比那还是小屋见大屋。实际情况是一个Java项目如果不依赖十几个或几十个第三方开源包都不好意思拿出去说。这样一来如果手工找齐这数目庞大的开源包会让Java程序员头痛不已。Maven的这个Feature恰好帮助Java程序员解决了这个难题。Maven可以根据配置自动从互联网上下载指定版本的依赖包，后续Java项目的构建可直接使用已经下载到本地的包；Maven似乎还会定期自动更新第三方包的版本。

受到Maven这个特性的启发，我于是就开发了这款C语言项目构建管理辅助工具 – [buildc](http://code.google.com/p/buildc/)(项目主页http://code.google.com/p/buildc)。buildc工具本身是用[Python](http://python.org)语言实现的，这主要是考虑到Python较高的开发效率以及自带功能强大的标准库。这也是我第一次用Python写程序，个人认为buildc的代码十分混乱，内部实现耦合较高，扩展性差，也谈不上什么风格，都是命令式语言的思维，代码本身并没什么价值，以后有时间定会[重构](http://tonybai.com/2006/03/28/c-refactoring/)^_^。

buildc目前主要实现了两个功能：

1、第三方依赖库的远程获取和本地管理

2、根据目标主机环境、目标主机本地缓存的第三方库情况以及项目本身所依赖的第三方库的最新配置，自动生成一份包含了依赖库环境变量信息的Make.rules文件，或重新更新已有Make.rules文件(上一次由buildc生成的)。项目中的Makefile只需包含(include)Make.rules文件并使用该文件中的变量即可。

buildc的使用是有前提条件的，那就是第三方库必须按特定规划集中存储在一个版本控制服务器中，buildc目前仅支持Subversion。我不是很清楚Maven是如何从互联网上获取对应第三方开源包的jar包的，但我们很难直接获得C第三方库的二进制版本。这里面主要有两点原因：

1、C语言的第三方包多以源码包的形式提供；

2、Java号称"一次编写，到处运行"，也就是说Java第三方库仅需提供一份jar包即可运行在多个平台上；但C的二进制库不能，每种平台都会有对应的特定的版本，我们无法将一种二进制库应用到多个平台上。

因此我们首先需要构建组织内部的第三方库集中存储服务器，将各个产品需要的第三方库在各个平台上进行构建，并将得到的静态库或动态库放入版本服务器中。符合buildc要求的二进制库的组织形式如下。比如在svn://127.0.0.1:6666/3rds这个repository下面我们的第三方库按如下组织形式存放：

3rds/

– libevent/

– 2.0.10/

– README

– source_code_package

– sparc_32_solaris/

– include/

– lib/

– sparc_64_solaris/

– x86_32_solaris/

– x86_64_solaris/

– x86_32_linux/

– x86_64_linux/

– netsnmp/

– 5.2.0/

…

– 5.7.0/

…

… …

可以看到每个第三方库的组织形式都像下面这样：

package_name/

– version/

– CPU_MODE_OS

– include

– lib

一旦第三方库都按如此形式存储，buildc就可以获取到该服务器上的二进制库了。前提满足后，我们就来看看buildc在日常构建过程中的使用方法。

一、buildc的安装

buildc目前尚未做成python安装包，只是以源码形式提供的。所以现有情况下只需Checkout或下载buildc源码包到本地即可以使用。

buildc的源码目录结构如下：

buildc* # 脚本入口

build_utils/ # 源码库

templates/ # Make.rules.in模板

samples/ # 配置样例

为了方便在任意路径下使用buildc，可将存放buildc源码的目录加入到PATH环境变量中去。另外你可能还需执行'chmod u+x buildc'来为buildc加上执行权限。

二、环境初始化

执行buildc init，buildc会在你的HOME目录下建立.buildc.rc文件。该文件用于配置所有可用的第三方库的信息。

$> buildc init

Copy /home/tonybai/proj/build_tools/samples/buildc.rc.sample to /home/tonybai/.buildc.rc OK!

Please config /home/tonybai/.buildc.rc before you use other buildc commands!

Copy /home/tonybai/proj/build_tools/samples/buildc.cfg.sample to ./buildc.cfg OK!

Please config buildc.cfg before you use other buildc commands!

# $HOME/.buildc.rc

foo_repository = ('svn://10.10.0.156:6666/foo',

'~/.buildc_libs/foo',

[

('snmp', '5.7.0', 'lib/libnetsnmp.a'),

('libexpat', '2.0.1', 'lib/libexpat.a'),

('libiconv', '1.13.1', 'lib/libiconv.a'),

('libevent', '2.0.10', 'lib/libevent.a'),

('lcut', '0.2.0', 'lib/liblcut.a'),

('instantclient', '10.2.0.5.0', 'lib/libnnz10.so')

]

)

bar_repository = ('svn://10.10.0.156:6667/bar',

'~/.buildc_libs/bar',

[]

)

external_repositories = [

foo_repository,

bar_repository

]

其中foo_repository和bar_repository分别代表两个可用的集中存储第三方库的服务器，每个repository中的详细配置包括svn repository的url、这个repository的本地缓存路径以及构建所需的该repository中的第三方库信息。

buildc init还会提供一个buildc.cfg配置文件，该配置文件在后面再细说。

三、第三方库的本地缓存管理

有了正确的.build.rc配置，我们就可以初始化第三方库在本地的缓存了，执行buildc cache init。

$> buildc cache init

===>Begin init repository [svn://10.10.0.156:6666/foo]

Create dir: /home/tonybai/.buildc_libs/foo

library [snmp] does not exist!

Checkout [svn://10.10.0.156:6666/foo/snmp/5.7.0/x86_64_linux]…

Checkout [svn://10.10.0.156:6666/foo/snmp/5.7.0/x86_64_linux] OK!

library [libexpat] does not exist!

Checkout [svn://10.10.0.156:6666/foo/libexpat/2.0.1/x86_64_linux]…

Checkout [svn://10.10.0.156:6666/foo/libexpat/2.0.1/x86_64_linux] OK!

… …

buildc cache init命令会根据.buildc.rc中的配置，从各个repository中下载对应该主机平台的第三方库，存放在对应的缓存路径下备用。

如果repository有更新，我们可以执行buildc cache update来更新本地缓存(在实际的日常开发过程中你可以将该命令加入到crontab中来定期自动更新本地缓存)：

$ buildc cache update

===>Begin update repository [svn://10.10.125.156:3560/3rds]

Update [snmp]…

Update [snmp] OK!

Update [libexpat]…

Update [libexpat] OK!

… …

当不需要本地缓存时，我们可以通过buildc cache remove删除之：

$> buildc cache remove

===>Begin remove repository [svn://10.10.0.156:6666/foo]

Remove [/home/tonybai/.buildc_libs/foo] OK!

<=== End remove repository [svn://10.10.0.156:6666/foo]

… …

四、生成项目Make.rules

第三方库的本地缓存建立好后，我们就可以来配置项目了。在前面执行完buildc init时，buildc生成了一个项目配置模板文件buildc.cfg(.buildc.rc和buildc.cfg本身也都是Python源文件)，我们将该文件移到项目的顶层目录下，然后对该文件进行配置，下面是一个例子：

#(proj_name, (major, minor, revision), author)

project = ('foo', (1, 3, 1), 'tonybai')

# [(libname, libversion, [archives*])*]

external_libs = [

("snmp" , "5.7.0", ["libnetsnmpagent.a", "libnetsnmphelpers.a", "libnetsnmpmibs.a", "libnetsnmp.a"]),

("libexpat" , "2.0.1", ["libexpat.a"])

]

# [def*]

# e.g. ['-Dprint_msg=printf', '-D_SELF_DEBUG_']

custom_defs = [

'-Dprint_msg=printf',

'-Derr_msg=printf'

]

# [(var, value)*]

# e.g. [ ('WITHOUT_DB_IMPORT', 'TRUE'), ('SUPPORT_MYSQL', 'TRUE') ]

custom_vars = [

('WITHOUT_IMPORT', 'TRUE'),

('WITHOUT_NM', 'TRUE')

]

# [include_path*]

# e.g. ['./include', '/home/tonybai/.include']

custom_includes = [

'./include'

]

# [(lib_path, [archives])*]

# e.g. [('/home/tonybai/.lib', ['libfoo.a', 'libbar.so']), (‘.libs’, ['libzoo.a'])]

custom_libs = [

('.libs', ['libfoo.a']),

('', ['libzoo.so'])

]

这里简要说明一下这个配置文件的各个配置项：

* external_libs是项目所使用的第三方库列表，这些第三方库必须存在于该主机的本地缓存中，也就是.buildc.rc中拥有这些库的配置；

* custom_defs是项目需要额外传递给编译器的命令选项集合；

* custom_vars是你想额外在Make.rules定义的变量集合；

* custom_includes是额外需要单独指定的的头文件包含路径集合；

* custom_libs是项目所需额外的(不在本地第三方库中存储的)库路径，比如一些系统库。

完成buildc.cfg的配置，我们就可以通过buildc config-make来生成Make.rules文件：

$ buildc config-make

Can not found Make.rules in current directory!

Generate [/home/tonybai/proj/foo/Make.rules] …

Config [/home/tonybai/proj/foo/Make.rules]…

Config [/home/tonybai/proj/foo/Make.rules] OK!

Generate [/home/tonybai/proj/foo/Make.rules] OK!

生成的Make.rules如下：

#

# Make.rules for foo

#

# tonybai

# 2011-12-08

#

# @Generated by buildc@

#

# Project information

TOPDIR = /home/tonybai/proj/foo#@topdir@

# Platform information

OS = linux#@os@

CPU = x86#@cpu@

CMODE = 64-bit#@cmode@

# Version information, (MAJOR.MINOR.REVISION)

MAJOR = 1#@major@

MINOR = 3#@minor@

REVISION = 1#@revision@

VERSION = $(MAJOR).$(MINOR).$(REVISION)

# Compiler options

DEFS = -D_REENTRANT -D_POSIX_PTHREAD_SEMANTICS -D_DEBUG_ -DVERSION=\"${VERSION}\"

… …

CUSTOM_DEFS = -Dprint_msg=printf -Derr_msg=printf #@custom_defs@

CC = gcc -m64#@cc@

CFLAGS = $(FDEBUG) $(FWALL) $(FPIC) $(FOPTIMIZE) $(DEFS) $(CUSTOM_DEFS) $(INCLUDES)

# Library infomation

snmp_ROOT = ~/.buildc_libs/foo/snmp/5.7.0/x86_64_linux#@lib_roots@

libexpat_ROOT = ~/.buildc_libs/foo/libexpat/2.0.1/x86_64_linux#@lib_roots_end@

LIB_INCLUDES = -I $(snmp_ROOT)/include -I $(libexpat_ROOT)/include #@lib_includes@

LIBS_DEPEND = -L $(snmp_ROOT)/lib -lnetsnmpagent -lnetsnmphelpers -lnetsnmpmibs -lnetsnmp -L $(libexpat_ROOT)/lib -lexpat#@ libs_depend@

CUSTOM_LIBS = -L .libs -lfoo -lzoo#@custom_libs@

# Headers

DEFAULT_INCLUDES = #@default_includes@

CUSTOM_INCLUDES = -I ./include #@custom_includes@

INCLUDES = -I $(TOPDIR)/include $(LIB_INCLUDES) $(CUSTOM_INCLUDES) $(DEFAULT_INCLUDES)

# Libraries

DEFAULT_LIBS = #@default_libs@

LIBS = $(LIBS_DEPEND) $(CUSTOM_LIBS) $(DEFAULT_LIBS)

# Other definitions

WITHOUT_IMPORT = TRUE#@custom_vars@

WITHOUT_NM = TRUE#@custom_vars_end@

… …

你可以对比着项目buildc.cfg的配置来查看Make.rules的构成。如果bulidc.cfg配置发生变化，那么再次执行buildc config-make会更新当前路径下的Make.rules。Make.rules的生成和更新使用了基于模板的标记替换技术。

五、利用Make.rules构建项目

可以看出Make.rules中将平台信息和第三方库的依赖信息都放置在对应的变量中了。项目的Makefile只需要包含Make.rules便可以利用这些信息进行项目的构建。可以利用的Make.rules中的主要变量包括：CFLAGS、LIBS。我们甚至可以为项目再编写一个"一键构建"脚本，该脚本中只需包含两行代码即可：

buildc config-make

make

你无需将Make.rules提交到源码版本库中，但需要将buildc.cfg作为项目的一部分。这样在任一一个通过buildc做项目构建管理的环境中，你的项目就都可以进行"一键式"构建了，再也无需为配置项目路径和寻找构建第三方依赖库而发愁了。另外通过buildc进行构建管理的项目将会很容易地集成到持续集成过程中。

buildc与make的组合模式很类似于maven和[ant](http://ant.apache.org/)的组合，但buildc目前的功能还无法与maven相比，不过buildc也不打算做成maven的模样。buildc后续可能会支持从更多种版本管理服务器(比如git)下载第三方库，支持按指定模板生成Make.rules(目前只有一种模板)等特性。从目前实践的情况来看，[buildc](http://code.google.com/p/buildc/)这个项目构建管理辅助工具十分适合我们内部的C项目构建，也许它也同样适合你的项目，有兴趣的朋友不妨试试。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

好工具!