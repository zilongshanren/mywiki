---
title: 关于编译阶段符号多重定义的问题
url: https://tonybai.com/2012/04/11/multiple-definitions-of-the-compiling-phase/
published: '2012-04-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 关于编译阶段符号多重定义的问题

印象中关于编译以及链接的问题早已是老生常谈了。但今天又遇到了一个这样的问题，这里还总想提及一下下^_^。

这次要说的问题依旧发生在使用

[lcut](http://code.google.com/p/lcut)进行[单元测试](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)的过程中。一位同事在编译使用了[mock](http://tonybai.com/2010/10/29/lcut-add-mock-support/)函数的测试用例代码时出现了"multiple definition of 'xxx'“的错误。这里简单模拟其场景如下：/* testall.c */

/* mock lib function */

int lib_function(…) {

…

return (int)LCUT_MOCK_RETV();

}

int function_to_be_tested(…) {

…

ret = lib_function(…);

…

}

void test_case(lcut_tc_t *tc, void *data) {

ret = function_to_be_tested(…);

LCUT_INT_EQUAL(tc, 0, ret);

}

lib_function是静态

[共享库](http://tonybai.com/2010/12/13/also-talk-about-shared-library/)中的一个接口，但这里被mock了。不过由于一些其他test_case使用了静态共享库(.a)的其他接口，因此在编译时程序链接了这个静态共享库。但结果编译器却报错：lib_function被多重定义了。经过各种排查(编译器命令行中的目标文件与库链接顺序是否正确等)，我们发现编译器报错的原因居然是忘记mock几个与lib_function同属一库模块(xx.o)的接口。

这里就不拐弯抹角了。由于漏掉了一些本该mock的接口，因此程序在编译testall.c时有许多unresolved的符号需要到静态共享库中去查找。这里又涉及到了符号resolve的过程，而更为重要的一点是要弄清楚编译器是如何对待静态共享库中那个拥有testall.o中未resolved的符号的库模块的(一个静态库.a文件实际上是由诸多库模块.o文件组合而成的)。我们来看看下面例子。

一个libcommon.a的组成如下：

libcommon.a

– foo.o

– function: foo1

– function: foo2

– bar.o

– function: bar1

– function: bar2

我们来看一下一个调用了foo1函数且链接了libcommon.a的可执行文件(a.out，对应的源文件main.c)中都有哪些已定义的符号：

$ nm a.out

…

080483d4 T foo1

080483b4 T main

080483e2 T foo2

…

通过nm输出的结果可以看到，最终的可执行程序中居然包含了程序并未调用的函数foo2的定义。似乎一切都清晰了：编译器在libcommon.a的foo.o中找到了unresolved的符号foo1，但编译器并非只是将foo1的定义放入最终的可执行文件中，而是将foo.o从libcommon.a中取出，并将其与main.o放在一处同等对待，编译器会扫描foo.o中所有的符号，并确保其中的符号都是具有定义的，这样才能保证最终的可执行程序中所有的符号都是具有定义的。

现在我们可以回过头来回答本文开始处所遇到的那个"多重定义"的问题了。因为testall.c中存在未resolved的符号，即那些被漏掉的未mock的库接口，因此编译器找到了静态共享库中定义了这些库接口的库模块(某个.o文件)，但编译器并非只是处理这些符号，和上面的例子一样，编译器还会扫描这个库模块文件中的所有符号以确保所有符号都有定义。而就在这个过程中编译器发现了其中有的符号(比如lib_function)的定义与testall.c中mock的同名接口(lib_function)定义相冲突，从而才作出了错误提示。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

多谢，这篇文章对我很有帮助。之前一直为这个问题困扰了好几天了，终于在这儿找到答案了。

有帮助就好