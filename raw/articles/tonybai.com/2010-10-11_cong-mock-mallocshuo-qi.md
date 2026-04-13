---
title: 从mock malloc说起
url: https://tonybai.com/2010/10/11/start-with-mock-malloc/
published: '2010-10-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 从mock malloc说起

上午对一段代码进行单元测试，由于需要用到[mock](http://tonybai.com/2008/04/12/mock-test-in-c-unit-test/)，所以选择使用[cmockery](http://tonybai.com/2009/08/22/introduce-cmockery-for-c-unit-test/)

作为[Unit Testing](http://tonybai.com/2005/11/08/the-design-and-implementation-of-c-unittest-framework/)框架([lcut](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)还未提供mock功能)。测试代码里需要mock malloc以模拟分配内存失败的异常情况。

编写一个用例后，Build，提示出错：multiple definition of `malloc'。经检查发现Makefile中定义mock malloc的那个目标文件(.o文件)居然被link了两次，类似于下面的这种错误情形：

$ gcc testmain.c malloc.o malloc.o

malloc.o: In function `malloc':

malloc.c:(.text+0×0): multiple definition of `malloc'

malloc.o:malloc.c:(.text+0×0): first defined here

collect2: ld returned 1 exit status

去掉一个显式链接的malloc.o文件后Build顺利通过，运行该单元测试，程序dump core，对此很是疑惑！使用gdb查看core文件，很快发现了问题所在：因为[cmockery](http://code.google.com/p/cmockery)本身也使用了malloc，但在链接过程中，cmockery库中的malloc符号被绑定到了malloc.c中的那个malloc实现上了，而我们mock的那个malloc在测试用例中又被设置返回NULL，这样非法地址访问就不足为奇了。

对以上两个问题的理解或多或少都需要一些链接方面的知识，这里你可能会问到以下两个问题：

1、C运行库(libc.a)是要被作为默认库隐式提供给ld程序做链接的，那么用自己实现的malloc替代C标准库中的malloc，链接器在链接时为什么没有检查出重定义？

2、cmockery库中的malloc是如何绑定到我们自己实现的那个malloc上的呢？为什么不绑定到C运行库中的那个malloc？

从问题内容我们也似乎可隐约推论出一点：那就是链接器对目标文件(.o)和归档文件(.a)的对待似乎是不同的。没错，的确是这样的。

可执行程序是由一系列.o文件“合并”而成。以静态链接为例，.o文件集合中除了包含我们显式(.c->.o)提供的.o文件外，还有从归档文件(.a)中提取出来的.o文件。这类.o文件是“按需”从.a中提取出来的，这也符合.a文件最初设计的初衷(减少可执行文件的size + 减少可执行文件load到内存后的内存占用)。

我们用一个的例子来解释.o文件“按需”从.a中提取的过程，也顺便回答上面的两个问题。

我们有三个源文件testmain.c、print.c和libprint.c，三个文件都很简单：

/* testmain.c */

extern void print();

int main() {

print();

return 0;

}

/* print.c */

#include

void print() {

printf("print in object files\n");

}

/* libprint.c */

#include

void print() {

printf("print in archive files\n");

}

我们将libprint.c构建为一个.a文件(gcc -c libprint.c; ar rcs libprint.a libprint.o)，用于模拟库中的符号。print.c中的print则是我们自定义函数，试图用来替换库中同名函数。

执行gcc testmain.c print.c -L ./ -lprint，编译顺利通过。执行a.out，输出“print in object files”。显然testmain.c中的print调用被绑定到print.o中的print函数了。分析这个编译链接过程，我们就能回答上面的两个问题了。

我们知道[gcc](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)只是一组gnu compile tools的外部名称，gcc像个指挥官，协调一系列tools去完成任务。其中链接是最后一环，ld的输入是.o文件和.a文件。以这个例子来说，最后一步执行的是ld testmain.o print.o -L ./ -lprint …..，其中…..代表的是默认传入的C运行库。链接器从左向右扫描命令行参数中的.o和.a，目的是确定最终.o集合以及为每个.o中的外部符号(引用了但是未在本.o文件中定义)确定具体定义的位置。

链接器依从左到右顺序首先扫描testmain.o，将testmain.o加入到"最终.o文件集合"(初始该集合为空)，并发现testmain.o中引用了符号print，但却未定义，将该符号放到"undefined集合"中（初始"undefined集合"为空），另外testmain中还有一个符号main，与print不同，该符号为已定义的符号，同样链接器将之放到"defined集合"中(初始"defined集合"为空)。

继续从左向右扫描，轮到print.o这个目标文件了。该文件中有一个已定义的符号print和一个引用但未定义的外部符号printf，链接器的处理过程是：发现print是当前"undefined集合"中的元素，将print从"undefined集合"中取出，放入"defined集合"中; printf因无法确定定义，放入"undefined集合"，print.o放入"最终.o文件集合"。

继续向右扫描，遇到libprint.a。上面说过链接器对待.a与.o不同，.a中的符号是按需提取，这里的“按需”指的就是"undefined集合"中的符号。当前"undefined集合"中只有一个元素：printf，链接器尝试在libprint.a中查找printf的定义，未果。则链接器略过libprint.a，继续向右扫描。

最后剩下的就是libc.a了，也就是默认传递的C运行库。libc.a中包含了成百上千个.o文件。但目前只剩下printf一个符号没有得到定义了，我们只需要libc.a中包含printf符号定义的那个.o文件，也就是print.o，链接器找到print.o后将print.o放入"最终.o文件集合"，将printf符号从"undefined集合"挪到"defined集合"中，此致"undefined集合"变为空集合了。也就说明这次链接是成功的。

相信上面的两个问题通过这段过程描述已经可以被解释了。

如果我们将构建语句写为:gcc testmain.c -L./ -lprint print.c会发生什么呢？我们看看执行结果：

/tmp/ccSNKvLP.o: In function `print':

print.c:(.text+0×0): multiple definition of `print'

.//libprint.a(libprint.o):libprint.c:(.text+0×0): first defined here

collect2: ld returned 1 exit status

出现重定义错误！不过有了之前的基础，这里的重定义也很好理解了。gcc testmain.c -L./ -lprint print.c执行到最后一步是ld testmain.o -L./ -lprint print.o ….; 链接器扫描完libprint.a后，print的符号已经从libprint.a中的libprint.o目标文件中被"按需"提取出来放入"defined集合"中了。接下来链接器扫描print.o居然又发现了一个名为print的全局定义的符号，与"defined集合"中冲突，ld自然就会报错。

我们再来做点修改，构造一个稍微复杂些的例子：

/* testmain.c */

extern void do_print();

int main() {

do_print();

return 0;

}

/* print.c */

#include

void print() {

printf("print in object files\n");

}

/* libprint.c */

#include

void print();

void do_print() {

print();

}

void print() {

printf("print in archive files\n");

}

在testmain.c中我们换作调用do_print了，do_print在libprint.a中有定义。执行gcc testmain.c print.c -L ./ -lprint，结果出错：

.//libprint.a(libprint.o): In function `print':

libprint.c:(.text+0xd): multiple definition of `print'

/tmp/ccoWjHZS.o:print.c:(.text+0×0): first defined here

collect2: ld returned 1 exit status

这回怎么又变成“重定义”了呢？我们来分析一下：

*扫描testmain.o，"undefined集合"中有了符号do_print;

*扫描print.o，"undefined集合"未变，"defined集合"中增加了print

*碰到libprint.a，按照"按需"提取的原则，我们找到了do_print定义，"undefined集合"中的do_print被移到"defined集合"，libprint.a中的libprint.o被放置到"最终.o文件集合"中;与前面例子不同的是libprint.o中有两个符号do_print和print，作为"最终.o文件集合"中的一分子，libprint.o的地位与testmain.o和print.o是一致的，链接器需要扫描其全部内容，而不仅仅只是提取do_print，这样链接器又发现一个print的定义，与"defined集合"中的print符号重复，链接器报错！

如果要进一步了解链接器相关内容的话，推荐阅读一下下面几本书籍：

1、《[链接器与加载器](http://book.douban.com/subject/4083265)》

2、《[深入理解计算机系统](http://book.douban.com/subject/1230413)》

3、国人总结性质的大作《[程序员的自我修养–链接、装载与库](http://book.douban.com/subject/3652388)》

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论