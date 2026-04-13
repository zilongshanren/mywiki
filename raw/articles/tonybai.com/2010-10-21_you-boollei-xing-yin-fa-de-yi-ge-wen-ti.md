---
title: 由bool类型引发的一个问题
url: https://tonybai.com/2010/10/21/a-problem-caused-by-bool-type/
published: '2010-10-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 由bool类型引发的一个问题

[C99](http://en.wikipedia.org/wiki/C99) 原生支持布尔类型，类型名字为_Bool。对C程序员来说，这个名字有些“不伦不类”，还好一般C标准库 实现的头文件中都用宏bool来替代_Bool。C99虽说是C语言当前的最新标准，但是它也有10年历史之久了。据说[C1x标准](http://en.wikipedia.org/wiki/C1X) 正在讨论制定中，有兴趣的朋友可以到[标准C工作组](http://www.open-std.org/jtc1/sc22/wg14/) 官方站点上去瞧瞧。

有些跑题了^_^！其实这篇文章想说的不是C1x标准，而是一个与布尔类型有关的问题的分析解决过程。

上周为项目的复用库增加了一个小功能，对外表现形式就是一组函数。使用[lcut](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/) 对这组函数进行了详尽的[单元测试](http://tonybai.com/2005/11/08/the-design-and-implementation-of-c-unittest-framework/) ，所有用例都顺利通过。今天和一位同事交流后，觉得应该对这个功能作些改动，针对一些异常情况作些完善。修改方案很简单，就是在一个外部可见的结构体里增加一个表示当前状态的布尔类型的字段，然后在各个函数接口中设置该字段的值并根据该字段的值做相应的处理。

按照既定的思路修改后，原先的用例依旧可以全部pass。继续修改单元测试代码，增加针对此次改动的用例。编译并运行测试，这次则没有那么幸运-有几个用例失败了。查看失败原因，确有一两个是因为逻辑上的问题导致。

修正后，继续运行测试，依旧有两个用例无法通过。 仔细查看了一遍库代码以及单元测试代码，没有发现明显的错误。将LCUT_TRUE断言换成LCUT_INT_EQUAL断言，重新运行测试，发现期望值为true的断言，实际值却是一个-3146789这样的大数。看到这种情况我的第一反应是：是不是内存被污染了？比如代码里有内存覆盖或Buffer溢出的情况。又仔细浏览了一遍代码，依旧没有发现蛛丝马迹。采用[gdb](http://tonybai.com/2006/01/08/debug-multiple-process-program-using-gdb/) 单步执行测试程序，无奈lcut采用了许多回调函数，导致在gdb中无法追踪到我期望的符号。未果后，我尝试换成最原始的增加打印日志输出的调试方式，终于发现了问题端倪。

具体是这样的：在库代码和测试用例代码中，我都输出了bool类型的size，但结果却大相径庭。库代码中输出的sizeof(bool)等于1，而在测试程序中输出的值却为4，这个长度差异直接导致了前面的-3146789的出现。

这里我要补充一下，C99的布尔类型(bool)在stdbool.h中定义：#define bool _Bool(注: _Bool是原生的)，这只有在C99下才生效。考虑到有些编译器不支持C99或默认语言标准不是C99，为了兼容，自定义了一份bool的定义，并通过预编译宏与标准定义隔开：

#if __STDC_VERSION__ >= 199901L

#include

#else

#undef bool

#undef true

#undef false

typedef enum {

false,

true

} bool;

#endif /* __STDC_VERSION__ >= 199901L */

难道原因是库中代码采用了标准bool类型，而测试代码中采用的是自定义的bool类型？似乎没道理啊。突然间看到了屏幕上编译测试代码的gcc命令行输出：

gcc std=c99 -c -o testall.o testall.c … (后面还有较长的链接库的参数，这里省略）

gcc -o testall testall.c …

怎么对testall.c编译了两次呢？测试代码目录下的Makefile并没有包含第一个gcc命令啊，又翻了翻顶层目录下的Makefile，我找到了答案：原来顶层目录下的Makefile中采用了如下脚本：

OBJ = $(SRC:.c=.o)

${OBJ}: ${SRC}

${CC} ${CFLAGS} -c ${SRC}

脚本根据.c文件替换获得.o文件名，并在同名.o和.c间建立依赖，这样所有.c文件都会被先编译为.o文件。

不过第一次编译的结果显然做了无用功，因为第二行命令执行后会覆盖第一行命令生成的.o文件。但恰恰第二行gcc命令中没有加入-std=c99的编译选项，导致testall.c这个编译单元中的bool使用了自定义的bool，导致了其长度为4个字节。

真相终于大白，就是因为testall.c所在目录下的Makefile编写时忘记添加-std=c99选项才导致了上述的问题。又检查了一下其他的存放单元测试代码的目录，发现所有Makefile都存在此问题。以前在没有使用bool类型时这样的Makefile是不会有问题的，关键就是这次我们用了bool类型，问题才暴露出来。

使用C语言，你就不得不常常与指针内存问题、编译器或[链接器](http://tonybai.com/2007/12/08/those-things-about-symbol-linkage/) 问题做斗争，其中的痛苦你最清楚，但处理这些事的过程中所蕴含的快乐也只有你自己最能体会到。继续痛并快乐着吧！

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论