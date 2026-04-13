---
title: 也谈共享库2
url: https://tonybai.com/2011/07/07/also-talk-about-shared-library-2/
published: '2011-07-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈共享库2

我之前写过一篇名为"[也谈共享库](http://tonybai.com/2010/12/13/also-talk-about-shared-library/)"的博文，对共享库的查找和[符号解析](http://tonybai.com/2008/02/03/symbol-linkage-in-shared-library/)机制做了还算比较详细的说明，不过百密一疏，总有一些意想不到的情况发生。这不今天我又遇到了一个有关共享库的新问题，这里将这个问题及其解决过程记录下来，也算是对上一篇文章中未涉及内容的一个补充吧。

N年前我曾参与过部门的一个可复用系统的设计开发，当时我们设计了一种插件式的系统结构，其中所谓的"插件"是以共享库的形式提供。主程序通过读取配置，获取插件的位置，并在运行期利用dlopen动态加载插件(.so文件)，用dlsym查找、绑定并执行.so中的特定业务函数。

我们可以用下面样例代码简单地模拟出这种设计：

/*

* 主程序 main.c */

* 需include dlfcn.h、link.h等标准头文件，这里省略

*/

typedef int (*PLUGIN_MAIN_FUNC)(void);

int main() {

void *handle = NULL;

char *dso = "plugin.so";

char *func_name = "plugin_main";

PLUGIN_MAIN_FUNC func = NULL;

handle = dlopen(dso, RTLD_LAZY);

if (handle == NULL) {

printf("dlopen (%s)失败!\n", dso);

return -1;

}

func = dlsym(handle, func_name);

if (func == NULL) {

printf("dlsym (%s)失败!\n", func_name);

return -1;

}

printf("%d\n", my_add(4, 8));

printf("%d\n", func());

dlclose(handle);

return 0;

}

以下my_add接口可以理解为主程序所使用的底层库，亦可为plugin程序使用。

/* add.h */

int my_add(int a, int b);

/* add.c */

int my_add(int a, int b) {

return a + b;

}

/* 以下是plugin.so的源代码 */

/* plugin.c */

#include "add.h"

int plugin_main() {

return my_add(5, 6);

}

在Solaris 10 for x86, Gcc 3.4.6下编译plugin和主程序：

$ gcc -fPIC -shared -o plugin.so plugin.c

$ gcc -o main main.c add.c -ldl

执行main，我们得到了期望的结果：

12

11

将该样例拿到Solaris 10 for sparc平台上编译运行一样没有问题。最后，我把源代码拿到了我的[Ubuntu 10.04](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)下，Gcc的版本是4.4.3，编译过程很顺利，但是执行的结果却与预期不符，执行main后得到的结果是：

12

main: symbol lookup error: ./plugin.so: undefined symbol: my_add

居然提示无法找到符号my_add！在Solaris上明明可以正确执行的程序，搬到Linux下却出错。这种问题十分对我的胃口，开始“破案”^_^。

我们先来收集证据，先看看plugin.so的符号表：

$ nm -f sysv plugin.so

Name Value Class Type Size Line Section

… …

my_add | | U | NOTYPE| | |*UND*

plugin_main |0000046c| T | FUNC|0000002c| |.text

my_add符号的确是Undefined（未定义）的，也就是说在主程序获得my_add符号并准备执行时(注意我们在dlopen的参数中使用了RTLD_LAZY)，加载器需要在此时为my_add这个符号寻找其定义。main这个可执行文件中是定义了这个符号的，我们可以通过nm命令看到这一情况：

$ nm -f sysv main

Name Value Class Type Size Line Section

… …

main |080484f4| T | FUNC|000000ee| |.text

my_add |080485e4| T | FUNC|0000000e| |.text

按照我原先的理解，加载器在为my_add符号寻找定义时，是应该可以将main中的my_add定义与之相绑定的，但是事实却是加载器无法找到my_add这个符号的定义，导致执行出错。

你也许会立刻想出一种解决方法，将add.c与plugin.c一起编译：

$ gcc -fPIC -shared -o plugin.so plugin.c

这样编译后的plugin.so中的确有了my_add的定义：

$ nm -f sysv plugin.so

Name Value Class Type Size Line Section

… …

my_add |00000498| T | FUNC|0000000e| |.text

plugin_main |0000046c| T | FUNC|0000002c| |.text

main也可以正确执行了。但这显然不是我么想要的结果。作为一个plugin，其编译时很可能无法得到add.c或者add.c对应的静态库，也许只能得到add.h，所以这种方法很局限。另外这个方案也在plugin源码与主程序源码之间无端建立一个耦合，导致后续的一些不方便。

接下来，我使用readelf工具对main的ELF格式做了一次全面检查：

$ readelf -a main

在readelf输出的内容中，我发现了两个“符号表(Symbol table)”：

Symbol table '.dynsym' contains 9 entries:

Num: Value Size Type Bind Vis Ndx Name

… …

3: 00000000 0 FUNC GLOBAL DEFAULT UND [dlclose@GLIBC_2.0](mailto:dlclose@GLIBC_2.0) (2)

4: 00000000 0 FUNC GLOBAL DEFAULT UND [__libc_start_main@GLIBC_2.0](mailto:__libc_start_main@GLIBC_2.0) (3)

5: 00000000 0 FUNC GLOBAL DEFAULT UND [dlsym@GLIBC_2.0](mailto:dlsym@GLIBC_2.0) (2)

6: 00000000 0 FUNC GLOBAL DEFAULT UND [dlopen@GLIBC_2.1](mailto:dlopen@GLIBC_2.1) (4)

7: 00000000 0 FUNC GLOBAL DEFAULT UND [printf@GLIBC_2.0](mailto:printf@GLIBC_2.0) (3)

… …

Symbol table '.symtab' contains 70 entries:

Num: Value Size Type Bind Vis Ndx Name

… …

52: 080485e4 14 FUNC GLOBAL DEFAULT 14 my_add

54: 00000000 0 FUNC GLOBAL DEFAULT UND [dlclose@@GLIBC_2.0](mailto:dlclose@@GLIBC_2.0)

55: 00000000 0 FUNC GLOBAL DEFAULT UND [__libc_start_main@@GLIBC](mailto:__libc_start_main@@GLIBC)_

58: 00000000 0 FUNC GLOBAL DEFAULT UND [dlsym@@GLIBC_2.0](mailto:dlsym@@GLIBC_2.0)

60: 00000000 0 FUNC GLOBAL DEFAULT UND [dlopen@@GLIBC_2.1](mailto:dlopen@@GLIBC_2.1)

63: 00000000 0 FUNC GLOBAL DEFAULT UND [printf@@GLIBC_2.0](mailto:printf@@GLIBC_2.0)

68: 080484f4 238 FUNC GLOBAL DEFAULT 14 main

… …

仔细观察一下这两个表，你会发现有些函数是重复的，如dlopen在两个表里面都有，但my_add却只在.symtab中出现。也许问题就在这里。迅速翻阅了一些资料（比如"[Linkers and Loaders](http://book.douban.com/subject/4083265)"），发现这两个符号表的功用确有不同。

.symtab中的符号也称为normal symbol，表中包含了所有ELF文件中涉及的所有符号，用于普通的链接器；.dynsym中的符号则是由未定义的动态链接符号以及该ELF文件本身导出(export)的用于动态链接的符号组成。说到这里，头绪渐渐明晰。在本例中，.symtab这个普通符号表中虽然包含了my_add符号，但是这并不能说明my_add是main导出的用于动态链接的符号(dynamic symbol)，只有my_add出现在.dynsym中时，加载器才能在符号查找时看到my_add，而本例中my_add恰恰没有出现在.dynsym表中。

使用nm -D命令，我们也可以查看.dynsym符号表：

$ nm -D -f sysv main

Symbols from main:

Name Value Class Type Size Line Section

… …

dlclose | | U | FUNC| | |*UND*

dlopen | | U | FUNC| | |*UND*

dlsym | | U | FUNC| | |*UND*

… …

让我奇怪的是为何在Solaris上main的执行是没有问题的呢，换到Solaris下，我们同样使用nm -D查看上面的main文件：

$ nm -D main

main:

[Index] Value Size Type Bind Other Shndx Name

…

[10] | 134547364| 305|FUNC |GLOB |0 |10 |main

[19] | 134547353| 11|FUNC |GLOB |0 |10 |my_add

…

从结果可以看出，Solaris上main文件的.dynsym符号表中是包含了my_add符号的，这也就是main在Solaris上可以正常执行的原因。

难道与Gcc版本有关系？Solaris上的Gcc是3.4.6，而我的Ubuntu上的Gcc是4.4.3。"[Binary Hacks](http://book.douban.com/subject/4251048)"一书中曾提到使用-rdynamic选项可为可执行文件留下可用于动态连接的符号。向gcc传入-rdynamic，则链接器会得到-export-dynamic选项。我在Ubuntu下试一下这个选项：

$ gcc -o main main.c add.c -ldl -rdynamic

$ main

12

11

问题果然解决了。我们再用nm -D查看一下这个新版main文件：

$ nm -D -f sysv main

Symbols from main:

Name Value Class Type Size Line Section

… …

dlsym | | U | FUNC| | |*UND*

main |080486e4| T | FUNC|000000ee| |.text

my_add |080487d4| T | FUNC|0000000e| |.text

…

果然，.dynsym表扩大了好多，my_add也出现在了该表中，这样在main执行时加载器就可以为plugin.so中的my_add符号绑定到其定义了。

我在Solaris下的gcc命令行上也增加-rdynamic选项，但编译后得到的结果却是：

gcc: unrecognized option `-rdynamic'

查看了[Gcc](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)官方的[Manual](http://gcc.gnu.org/onlinedocs)后发现，在Gcc 4.1.2版本之前的Manual中都无法找到-rdynamic这一选项，也就是说这个选项是后加入Gcc中的。之前我们看到Solaris上main文件的dynsym表默认就包含了my_add，而4.1.2版本后的Gcc则默认不将自定义的全局函数导出。这是为什么呢？也许是为了提升可执行程序动态链接的性能，这个性能估计与dynsym表的大小不无关系。表越小，需要动态链接的符号越少，符号解析和绑定的速度也就越快；同时由于该表的内容需要在执行时加载到内存，这样表越小，加载的时间以及内存的占用也都很少，所以GCC更改了策略，默认选择不导出自定义的全局符号，并提供-rdynamic让程序员选择是否导出已定义的符号用于动态链接。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论