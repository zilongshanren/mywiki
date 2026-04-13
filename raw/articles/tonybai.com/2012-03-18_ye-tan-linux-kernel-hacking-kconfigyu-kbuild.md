---
title: 也谈Linux Kernel Hacking – Kconfig与Kbuild
url: https://tonybai.com/2012/03/18/linux-kernel-hacking-series-kconfig-and-kbuild/
published: '2012-03-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈Linux Kernel Hacking – Kconfig与Kbuild

** 挖掘简单现象背后的复杂本质。**– Tony Bai^_^

[上文](http://tonybai.com/2012/03/15/linux-kernel-hacking-series-kernel-config-compile-and-install/)讲到

[Linux Kernel](http://kernel.org)的配置和编译十分简单，甚至简单到可以与一个用户层应用相媲美。这一切都是因为Linux Kernel实现了一套易于使用、变更和后期维护的配置和编译体系。要知道最新Linux Kernel版本的代码量可是千万级别的，并且模块众多，其背后的配置和编译体系一定不那么简单，这次我们就来尝试Hack一下这套体系。

作为操作系统内核级系统软件，Linux Kernel在设计配置和编译体系时至少应该有如下几点考虑：

* 满足配置和编译内核以及内核模块的所有需求

* 较高的运行效率

* 配置阶段和编译阶段平滑结合

* 对内核开发者来说，这套体系应该易用、易变、易维护

* 其设计本身应该做到层次清晰

从配置和编译Linux Kernel所使用的命令来看，Linux Kernel的配置和编译体系总体上还是基于

[GNU Make](http://www.gnu.org/s/make/)的，没有另外使用其他的编译工具(比如[Scons](http://tonybai.com/2008/12/14/learn-scons/)、[CMake](http://www.cmake.org)等)。但Linux Kernel实现了Kconfig和Kbuild，用于辅助内核的配置和编译。Kconfig，顾名思义，用于辅助2.6以后版本Linux内核的配置(

**K**ernel**config**)；Kbuild，也物如其名，用于辅助2.6以后版本Linux内核的编译(**K**ernel**build**)。这里索性将Kconfig和Kbuild称作辅助工具(不单纯叫脚本或配置文件)，因为它们自身既有逻辑概念，又有物理存在。如果你曾在Linux Kernel的源码目录中徜徉过，你就会知道Kconfig文件散布在核心源码的各个角落；Kbuild文件还好，只在顶层目录、include目录下子目录、drivers下子目录以及各个arch/$ARCH/include的子目录中分布。如果Linux Kernel没有引入Kconfig和Kbuild，那么本篇文章就没有了存在的必要性 – Makefile纵使数量众多，也是可以慢慢消化的，毕竟Make的规则就那么多。但Kconfig和Kbuild的引入好似为Linux Kernel配置和编译引入了一层抽象，对外(Linux核心开发者)确实是简单了，但对于我这样的要Hack编译体系的人来说，这层抽象本身就具有一定复杂性，势必需要耗时耗力地去理解。下面我们就来结合不同阶段的使用场景来深入理解一下Kconfig和Kbuild。

一、make *config阶段

Linux Kernel的配置项都存储于散布在Kernel源码各处的Kconfig文件中。Kconfig文件之于Linux Kernel就好比configure.ac或Makefile.am之于那些使用

[autotools](http://tonybai.com/2010/09/26/hello-autoconf-and-automake/)作为构建工具的用户层应用，至少设计思路是类似的 – 先config，再make；make阶段会利用config阶段生成的一些文件。Kconfig既是配置文件，也是一种配置语言，可以理解为是一种针对Linux Kernel配置的领域特定语言(

[DSL](http://en.wikipedia.org/wiki/Domain-specific_language))。Documentation/kbuild/kconfig-language.txt文件对该种配置语言做了详尽的使用说明，这里就不做赘述了。我们主要关注的是Kconfig在配置过程中所扮演的角色以及对输出的结果的影响。Linux Kernel的配置过程也是在make的驱动下开始的，我们以"make menuconfig"的执行过程为例。

1、首先，顶层Makefile通过分析$(MAKECMDGOALS)判定"menuconfig"为config-targets，而非build-target或mixed-target(诸如make defconfig all这样的命令)；

2、"menuconfig"与Makefile中预置target进行匹配

menuconfig会匹配到Makefile中的"config %config"，下面是有关这个target的源码节选：

include $(srctree)/scripts/Kbuild.include

… …

include $(srctree)/arch/$(SRCARCH)/Makefile

export KBUILD_DEFCONFIG KBUILD_KCONFIG

config %config: scripts_basic outputmakefile FORCE

$(Q)mkdir -p include/linux include/config

$(Q)$(MAKE) $(build)=scripts/kconfig $@

"config %config"有三个依赖项：scripts_basic、outputmakefile和FORCE。其中outputmakefile、FORCE是两个空目标，而有关scripts_basic target的源码如下：

# Basic helpers built in scripts/

PHONY += scripts_basic

scripts_basic:

$(Q)$(MAKE) $(build)=scripts/basic

scripts_basic target的构建实际上就是编译scripts/basic下的源文件。build变量在scritps/Kbuild.include中定义，其值为"-f $(if $(KBUILD_SRC),$(srctree)/)scripts/Makefile.build obj"，所以上述命令展开后就是"make -f scripts/Makefile.build obj=scripts/basic"。scripts/Makefile.build这个文件在整个Linux Kernel编译过程中占据极其重要的位置，其定义了核心编译的主要target(如.o、.s等)的构建命令规则。

3、menuconfig目标的构建

在依赖项scripts_basic构建完毕后，Make驱动执行menuconfig目标的构建：

首先，创建两个目录include/linux和include/config，然后执行"make -f scripts/Makefile.build obj=scripts/kconfig menuconfig"。target依旧是"menuconfig"，但scripts/Makefile.build中似乎并没有这个target可供匹配啊。别急，我们看看scripts/Makefile.build中的这段代码：

src := $(obj)

… …

# The filename Kbuild has precedence over Makefile

kbuild-dir := $(if $(filter /%,$(src)),$(src),$(srctree)/$(src))

kbuild-file := $(if $(wildcard $(kbuild-dir)/Kbuild),$(kbuild-dir)/Kbuild,$(kbuild-dir)/Makefile)

include $(kbuild-file)

这是一段关键代码，kbuild-dir的求值结果为scripts/kconfig，由于scripts/kconfig下没有Kbuild文件，进而kbuild-file求值结果为scripts/kconfig/Makefile，并且该文件被Makefile.build包含了进来。从kbuild-file这个变量的命名可以看出为何各个子目录下的Makefile被称为Kbuild Makefile了。

scripts/kconfig/Makefile中包含了许多*config targets，其中就有"menuconfig"这个target：

ifdef KBUILD_KCONFIG

Kconfig := $(KBUILD_KCONFIG)

else

Kconfig := arch/$(SRCARCH)/Kconfig

endif

… …

menuconfig: $(obj)/mconf

$< $(Kconfig)

该目标依赖scripts/kconfig/mconf，这是一个小工具程序，Make会首先执行该程序的编译链接；然后执行"scripts/kconfig/mconf arch/x86/Kconfig"($<是一个自动变量，指代该target的第一个依赖项，这里是scripts/kconfig/mconf)。

4、"scripts/kconfig/mconf arch/x86/Kconfig"的执行过程

到这里，Kconfig配置文件终于登场了！scripts/kconfig/mconf读取arch/x86/Kconfig，后者是一个针对x86这一体系的顶层Kconfig文件，打开arch/x86/Kconfig后，你会发现它内部source了许多其他Kconfig文件，诸如：

….

source "init/Kconfig"

source "kernel/time/Kconfig"

source "mm/Kconfig"

…

mconf会依次读入这些子Kconfig文件，并将配置项的符号表建立起来。如果你是第一次进行Linux Kernel配置，尚没有.config文件，那么这些配置项的初始值从哪里得到呢(不是所有配置项都有默认值)？在init/Kconfig文件中，你会看到这样的配置项：

config DEFCONFIG_LIST

string

depends on !UML

option defconfig_list

default "/lib/modules/$UNAME_RELEASE/.config"

default "/etc/kernel-config"

default "/boot/config-$UNAME_RELEASE"

default "$ARCH_DEFCONFIG"

default "arch/$ARCH/defconfig"

mconf应该就是通过这个DEFCONFIG_LIST配置项找到一份默认config文件的，mconf自上而下依次尝试，直到对应的文件存在，就将存在的文件作为默认.config加载，为各个配置项赋值。在我的RHEL 5.5上$ARCH-DEFCONFIG被作为默认.config加载了；而在我的

[Ubuntu 10.04](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)上，mconf找到的是/boot/config-2.6.32-30-generic。下面是在RHEL 5.5上执行make menuconfig后控制台的输出结果：$ make menuconfig

scripts/kconfig/mconf arch/x86/Kconfig

#

# using defaults found in arch/x86/configs/x86_64_defconfig

#

#

# configuration written to .config

#

*** End of Linux kernel configuration.

5、生成.config文件

手工完成配置后，如果选择了save配置，那么在源码顶层目录下会生成一个.config文件，这个就是整个Kernel配置过程的最重要的输出，这类似用户层应用在configure之后生成的Makefile，.config文件实际上也是一个Makefile文件，只是其内容格式比较单一罢了(都是CONFIG_XXX=y形式的变量定义)。

至此，Linux Kernel的配置过程Hack结束了，其他*config target执行过程也是大同小异的，再总结一下make menuconfig配置的执行过程：

* 首先建立include/config目录，并编译scripts/basic下的一些工具；

* 然后编译scripts/kconfig下的工具，比如mconf等

* 执行scripts/kconfig/mconf arch/x86/Kconfig，该程序会生成.config

二、make all阶段

Make *config后，Kconfig文件的使命就算是结束了。剩下的Makefile和Kbuild文件将会在make all阶段扮演重要角色。前面说过Kbuild本身就是Makefile，分布在各个子目录中Makefile也被称为Kbuild Makefile,其实还是Makefile，总而言之，Make all阶段其实就是关于Makefile的事情了。只不过Linux Kernel的整个Makefile组织体系设计的很精巧，特别是与配置阶段输出的结果配合的天衣无缝，下面我们就来具体看看吧。

在顶层的Makefile中，我们可以直接定位到Make all的target，不过有两个，依次是：

all: vmlinux

all: modules

Make会自动合并all的依赖项，并依次对依赖项进行构建，就类似这样：

all: foo1

all: foo2

foo1:

@echo "foo1"

foo2:

@echo "foo2"

$> make

foo1

foo2

而vmlinux这个target是什么情况呢？见下面代码摘要：

# vmlinux image – including updated kernel symbols

vmlinux: $(vmlinux-lds) $(vmlinux-init) $(vmlinux-main) vmlinux.o $(kallsyms.o) FORCE

… …

$(call vmlinux-modpost)

$(call if_changed_rule,vmlinux__)

$(Q)rm -f .old_version

… …

# The actual objects are generated when descending,

# make sure no implicit rule kicks in

$(sort $(vmlinux-init) $(vmlinux-main)) $(vmlinux-lds): $(vmlinux-dirs) ;

从代码中可以看到vmlinux有若干个依赖项，我们沿着这些依赖项继续"深度"搜索，你会发现这是一个"不算浅"的依赖项树型结构，树的根节点就是vmlinux。由于这棵树太过"枝繁叶茂"，所以这里只想针对重要且关键的依赖项进行分析。

1、prepare

这个phony target是$(vmlinux-dirs)的依赖项，顾名思义，在真正地编译之前做些准备工作。目前所有的准备工作被划分到从prepare0到prepare3的多个phony targets中了，形成一个链式依赖关系，这么做也便于日后扩展：再增加一个prepare-n非常容易。

在prepare的过程中有若干的重要的文件被生成了：

**include/linux/version.h**: $(srctree)/Makefile FORCE

$(call filechk,version.h)

**include/linux/utsrelease.h**: include/config/kernel.release FORCE

$(call filechk,utsrelease.h)

**include/config/kernel.release**: include/config/auto.conf FORCE

$(Q)rm -f $@

$(Q)echo $(kernelrelease) > $@

**include/config/auto.conf**: $(KCONFIG_CONFIG)

**include/config/auto.conf.cmd**

$(Q)$(MAKE) -f $(srctree)/Makefile silentoldconfig

其中include/config/auto.conf依赖$(KCONFIG_CONFIG)和include/config/auto.conf.cmd，顶层Makefile中设置了auto.conf.cmd这个target的空规则：

# To avoid any implicit rule to kick in, define an empty command

$(KCONFIG_CONFIG) include/config/auto.conf.cmd: ;

这样实际上include/config/auto.conf在auto.conf.cmd尚未被创建的情况下只是依赖配置阶段输出的.config文件(KCONFIG_CONFIG ?= .config)。而Kernel配置后，auto.conf也未被创建，因此在这里Make执行创建auto.conf的命令：make -f Makefile silentoldconfig，该命令的执行结果是auto.conf、auto.conf.cmd、include/linux/autoconf.h以及include/config下的诸多空头文件被创建了出来。

2、$(vmlinux-dirs)

$(vmlinux-dirs)是一个非常重要的target，$(vmlinux-init)、$(vmlinux-main)、$(vmlinux-lds)都依赖$(vmlinux-dirs)。

init-y := init/

drivers-y := drivers/ sound/ firmware/

net-y := net/

libs-y := lib/

core-y := usr/

… …

core-y += kernel/ mm/ fs/ ipc/ security/ crypto/ block/

vmlinux-dirs := $(patsubst %/,%,$(filter %/, $(init-y) $(init-m) \

$(core-y) $(core-m) $(drivers-y) $(drivers-m) \

$(net-y) $(net-m) $(libs-y) $(libs-m)))

PHONY += $(vmlinux-dirs)

$(vmlinux-dirs): prepare scripts

$(Q)$(MAKE) $(build)=$@

此时vmlinux-dirs的值是一组目录集合，诸如init usr kernel mm fs ipc security crypto block drivers sound firmware net lib等。Makefile将这些目录名视为phony target。这样$(vmlinux-dirs): prepare scripts这个规则实际上就是一个multiple targets规则，会被多次执行的，即会对每个target执行一次"$(Q)$(MAKE) $(build)=$@"。我们以init这个phony target为例展开命令：make -f $(if $(KBUILD_SRC),$(srctree)/)scripts/Makefile.build

obj=init，该命令将根据Makefile.build中定义的规则对init目录进行编译。Makefile.build规则中的默认phony target为__build：

PHONY := __build

__build: $(if $(KBUILD_BUILTIN),$(builtin-target) $(lib-target) $(extra-y)) \

$(if $(KBUILD_MODULES),$(obj-m) $(modorder-target)) \

$(subdir-ym) $(always)

@:

__build"复杂"的依赖项会将必要的目标包含进来，其中较关键的是builtin-target这个目标：

ifneq ($(strip $(obj-y) $(obj-m) $(obj-n) $(obj-) $(lib-target)),)

builtin-target := $(obj)/built-in.o

endif

#

# Rule to compile a set of .o files into one .o file

#

ifdef builtin-target

quiet_cmd_link_o_target = LD $@

# If the list of objects to link is empty, just create an empty built-in.o

cmd_link_o_target = $(if $(strip $(obj-y)),\

$(LD) $(ld_flags) -r -o $@ $(filter $(obj-y), $^) \

$(cmd_secanalysis),\

rm -f $@; $(AR) rcs $@)

$(builtin-target): $(obj-y) FORCE

$(call if_changed,link_o_target)

targets += $(builtin-target)

endif # builtin-target

这样每个子目录(诸如mm、init等)下的主要目标就是built-in.o，其依赖的是$(obj-y)，展开后其实是一个.o文件列表。

这里还要提一点，那就是配置阶段的输出是如何与Build阶段结合的，我们还是看一下init/Makefile，这里节选一些代码：

obj-$(CONFIG_GENERIC_CALIBRATE_DELAY) += calibrate.o

mounts-$(CONFIG_BLK_DEV_RAM) += do_mounts_rd.o

mounts-$(CONFIG_BLK_DEV_INITRD) += do_mounts_initrd.o

mounts-$(CONFIG_BLK_DEV_MD) += do_mounts_md.o

可以看到.config中的配置项的值将各个.o文件分为几个类别，如果配置项值为y，则对应的.o文件归为obj-y列表；如果为m，则对应的.o文件归为obj-m列表，诸如此类(包括lib-y、lib-m、subdir-y、subdir-m等)。这样我们就可以通过调整配置项的值来选择是否将某功能编译到Linux Kernel中，还是以Kernel module形式存在，让人叹为观止！

3、$(vmlinux-lds)

在顶层Makefile源码中vmlinux-lds := arch/$(SRCARCH)/kernel/vmlinux.lds，vmlinux.lds是vmlinux的linker script。vmlinux.lds也是在构建$(vmlinux-dirs)目标时被构建出来的。

$(vmlinux-dirs)中包含arch/x86，而在arch/x86/Makefile中，我们发现了这行代码：

core-y += arch/x86/kernel/

这样arch/x86/kernel被纳入编译，而vmlinux.lds就是arch/x86/kernel/Makefile中变量extra-y的一个值：

extra-y := head_$(BITS).o head$(BITS).o head.o init_task.o vmlinux.lds

vmlinux.lds会被构建，而.lds目标构建规则在scripts/Makefile.build中：

# Linker scripts preprocessor (.lds.S -> .lds)

# —————————————————————————

quiet_cmd_cpp_lds_S = LDS $@

cmd_cpp_lds_S = $(CPP) $(cpp_flags) -D__ASSEMBLY__ -o $@ $<

$(obj)/%.lds: $(src)/%.lds.S FORCE

$(call if_changed_dep,cpp_lds_S)

OK，vmlinux.lds的来龙去脉也算是搞清楚了。

4、其他

vmlinux的依赖还包括vmlinux-init、vmlinux-main以及vmlinux.o，见下面顶层Makefile的节选代码：

vmlinux-init := $(head-y) $(init-y)

vmlinux-main := $(core-y) $(libs-y) $(drivers-y) $(net-y)

modpost-init := $(filter-out init/built-in.o, $(vmlinux-init))

vmlinux.o: $(modpost-init) $(vmlinux-main) FORCE

$(call if_changed_rule,vmlinux-modpost)

有了vmlinux-dirs那节的说明，这些依赖项的构建也是大同小异的。

当vmlinux的所有依赖项都构建完毕后，vmlinux的创建也就水到渠成了，这里就不多说了。

总而言之，Linux Kernel简单配置和编译的背后其实还是蛮复杂的，如果要挖掘细节，即使有了上面的Hack，也还是会耗费你一定时间的^_^。


© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Linux Kernel的代码量可是百万级别的

====

最新的3.3版本内核代码量超过了一千五百万，应该是千万量级

谢谢提醒，已更新文章内容。

学习了，我的最终目标是把kernel的kbuild系统移植到uboot上！看来我的路还远着呢！

u-boot-2014-10已经移植了KConfig和KBuild了.

后来的后来已经了解了。所以就没有再去移植了。：）

好文章，对照着内核代码看了一下，清晰很多。