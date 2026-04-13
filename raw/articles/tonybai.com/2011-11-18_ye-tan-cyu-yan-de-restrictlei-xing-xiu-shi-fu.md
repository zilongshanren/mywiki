---
title: 也谈C语言的restrict类型修饰符
url: https://tonybai.com/2011/11/18/also-talk-about-restrict-type-qualifier-in-c/
published: '2011-11-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈C语言的restrict类型修饰符

restrict关键字是[C99标准](http://tonybai.com/2005/07/28/introduction-on-c-standard-overview-series/)中新引入的一个类型修饰符(type qualifier)。如果你看过[GNU C库](http://tonybai.com/2009/04/11/glibc-strlen-source-analysis/)的源码或是其[manual](http://www.gnu.org/software/libc/manual/)，你就会发现restrict修饰符被广泛地应用在GNU C库中。[restrict关键字](http://www.lysator.liu.se/c/restrict.html)到底是用来做什么的呢？估计很多对C语言细节研究不够的程序员都无法给出答案，我个人也只是停留在"知道"这一关键字的层次上，于是乎今天我又对着C99规范钻研了一番，略有收获，这里也说道说道。

为何C标准委员会要在C99标准中引入restrict呢？这当然是有历史原因的。我们先来看看下面这个例子：

/* foo.c */

void foo(int *p, int *q, int *r) {

*p += *r;

*q += *r ;

}

int main() {

int a = 1;

int b = 2;

int c = 3;

foo(&a, &b, &c);

}

[C语言](http://tonybai.com/tag/C/)的设计哲学之一就是性能至上，为了性能可以舍弃一切。C程序员都希望编译器能为自己编写的程序生成高性能的目标代码，我们现在就来看看[GCC编译器](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)(在优化开关-O2已打开的情况下)为这段程序生成的目标代码是什么样子的。

(gdb) disas foo

Dump of assembler code for function foo:

0x080483c0 : push %ebp

0x080483c1 : mov %esp,%ebp

0x080483c3 : mov 0×10(%ebp),%edx

0x080483c6 : mov 0×8(%ebp),%ecx

0x080483c9 : mov 0xc(%ebp),%eax

0x080483cc : push %ebx

0x080483cd : mov (%edx),%ebx

0x080483cf : add %ebx,(%ecx)

0x080483d1 : mov (%edx),%edx

0x080483d3 : add %edx,(%eax)

0x080483d5 : pop %ebx

0x080483d6 : pop %ebp

0x080483d7 : ret

End of assembler dump.

这段汇编代码不是很难，我们将关键部分抽取出来并在每行汇编码后面给出解释：

mov 0×10(%ebp),%edx ; r -> %edx，将指针r指向的内存对象的地址放入寄存器edx

mov 0×8(%ebp),%ecx ; p -> %ecx，将指针p指向的内存对象的地址放入寄存器ecx

mov 0xc(%ebp),%eax ; q -> %eax，将指针q指向的内存对象的地址放入寄存器eax

push %ebx

mov (%edx),%ebx ; *r -> %ebx，将指针r指向的内存对象的值加载到寄存器ebx中

add %ebx,(%ecx) ; *r + *p -> *p， 将寄存器ebx中的数值与指针p所指内存对象的值相加，结果存放在指针p所指的内存对象中

mov (%edx),%edx ; *r -> %edx，将指针r指向的内存对象的值加载到寄存器edx中

add %edx,(%eax) ; *r + *q -> *q，将寄存器edx中的数值与指针q所指内存对象的值相加，结果存放在指针q所指的内存对象中

这段汇编代码是否是经过优化过的呢？我们结合foo函数的源代码分析后可以发现生成的目标码并非是经过优化的。在foo函数中指针r指向的内存对象一直都作为右值，其值没有被改动，编译器在第二次加法操作中完全可以直接利用第一次加载*r值的寄存器，而不是重新从内存中加载*r。但编译器为何没有优化掉这次访存操作呢？原因就在于编译器凭借C源代码中已有的信息是无法作出这种优化决策的。因为当编译器在foo的实现的上下文中看到三个指针时，它并不能判断出这三个指针所指向的地址是否有重叠，也就是说编译器并不能确定在第二次加法操作之前，r指向的内存对象是否被改变，编译器只能中规中矩地生成未经优化的目标代码，即每次都重新加载*r到寄存器，否则擅自优化会导致一些不可预期的行为。

那如何能帮助编译器作出正确的优化决策呢？这就需要程序员显式地为编译器提供用于决策的信息。在C99以前，很多编译器通过提供#Pragma参数或自扩展的关键字来实现这一点。比如：GCC为程序员提供了__restrict__或__restrict扩展关键字，有了这些关键字后，C程序员就可以显式地向编译器传达信息了。还以foo为例，我们看看加上__restrict__后编译器为函数foo生成的目标代码是什么样子的：

void foo(int *__restrict__ p, int *__restrict__ q, int * __restrict__r) {

*p += *r;

*q += *r ;

}

(gdb) disas foo

Dump of assembler code for function foo:

0x080483c0 : push %ebp

0x080483c1 : mov %esp,%ebp

0x080483c3 : mov 0×10(%ebp),%edx

0x080483c6 : mov 0×8(%ebp),%ecx

0x080483c9 : mov 0xc(%ebp),%eax

0x080483cc : mov (%edx),%edx

0x080483ce : add %edx,(%ecx)

0x080483d0 : add %edx,(%eax)

0x080483d2 : pop %ebp

0x080483d3 : ret

End of assembler dump.

我们主要来看下面连续的三行汇编代码：

0x080483cc : mov (%edx),%edx ; *r -> %edx，将指针r指向的内存对象的值加载到寄存器edx中

0x080483ce : add %edx,(%ecx) ; *r + *p -> *p，将寄存器edx中的数值与指针p所指内存对象的值相加，结果存放在指针p所指的内存对象中

0x080483d0 : add %edx,(%eax) ; *r + *q -> *q，将寄存器edx中的数值与指针q所指内存对象的值相加，结果存放在指针q所指的内存对象中

可以看到这次编译器生成了优化后的代码，第二次加法操作直接用的是缓存在寄存器中的*r值。以上就是C99引入restrict关键字的一个基本考虑，通过restrict，C程序员可以告知编译器大胆地去执行优化，程序员来保证代码符合restrict语义的约束要求，这可以看作是一种程序员与编译器间的契约。

前面说过restrict是一种类型修饰符，但不同于其他两种修饰符const和volatile，restrict仅用于修饰指针类型与不完整类型(incomplete types)，C99规范中对restrict的诠释是这样的："Types other than pointer types derived from object or incomplete types shall not be restrict-qualified"。用restrict修饰指针是最常见的情况，被restrict修饰的指针到底有何与众不同呢？

用restrict修饰某指针变量意味着在该指针变量的生命周期内，该指针是其所指内存对象的唯一访问和修改入口，即所有对其所指的内存对象数据的访问和修改都是通过该指针完成的。或是说在特定上下文中该指针所指的内存对象不存在别名(Alias)。何为别名？引用同一内存对象的多个变量互为别名。比如：

int a = 5;

int *p = &a;

int *q = p;

这样p, q, a互为别名，它们都引用到地址&a。另外如果两个指针所指向的内存对象有相互重叠，那相互也算做是一种别名。

restrict的语义约束可以分成两个方面，一个是对内部的，一个是对外部的。我们还以上面的foo函数为例，这里稍作改动，去掉p，q两个参数的restrict修饰：

void foo(int *p, int *q, int *restrict r) {

*p += *r;

*q += *r ;

}

从foo内部来看，r是一个被restrict修饰的指针，其生命周期从foo执行开始一直到foo执行结束。按照上面对restrict的诠释，在foo函数内部不应该存在指针r所指内存对象的别名，即不应该存在下面情况：

void foo(int *p, int *q, int *restrict r) {

int *z = r;

…later, use r and z…

}

这的约束是foo的实现者保证的。

对于外部而言，即foo的使用者依然要保证传入实参后p或q不是r所指内存对象的别名，下面这样的代码将违反约束：

int a = 5;

int b = 6;

foo(&a, &b, &b);

这里还有一个问题：虽然r用了restrict修饰符，但编译器在看到void foo(int *p, int *q, int *restrict r)这个函数原型后就一定会生成优化的代码吗？显然通过这个原型信息，编译器依旧无法保证p或q不是r所指内存地址的别名，所以对上面这段代码编译器无法给出优化，即使r是被restrict修饰的，至少在我的Ubuntu gcc 4.4.3上是不会生成优化目标代码的。也就是说这个例子中foo的设计者与编译器之间的契约不够充分，无法让Compiler完全信服地去执行优化。这就需要进一步的补充契约，也就是让Compiler意识到p, q, r在foo中都是各自所指内存地址的唯一入口，为了达到这一点，我们只能为p, q也加上restrict修饰，这样契约变成foo内部的p, q, r是给自所指内存的唯一入口，p, q, r也就不可能是对方的别名了。

但即使所有指针参数都加上restrict修饰，Compiler就一定会生成优化的代码吗，事实是也不一定。看下面例子：

void foo1(int *restrict p, int *restrict q, char *restrict r) {

*p += (int)*r;

*q += (int)*r;

}

void foo2(int *restrict p, int *restrict q, long long int *restrict r) {

*p += (int)*r;

*q += (int)*r;

}

可以看到我们分别将foo函数的最后一个参数r的类型换为了char*和long long int*并,形成两个函数foo1和foo2，我们尝试用GCC生成对应的目标代码，通过反编译，我们可以得到如下结果：

(gdb) disas foo1

Dump of assembler code for function foo1:

0×08048430 : push %ebp

0×08048431 : mov %esp,%ebp

0×08048433 : mov 0×10(%ebp),%edx

0×08048436 : mov 0×8(%ebp),%ecx

0×08048439 : mov 0xc(%ebp),%eax

0x0804843c : push %ebx

0x0804843d : movsbl (%edx),%ebx

0×08048440 : add %ebx,(%ecx)

0×08048442 : movsbl (%edx),%edx

0×08048445 : add %edx,(%eax)

0×08048447 : pop %ebx

0×08048448 : pop %ebp

0×08048449 : ret

End of assembler dump.

(gdb) disas foo2

Dump of assembler code for function foo2:

0×08048450 : push %ebp

0×08048451 : mov %esp,%ebp

0×08048453 : mov 0×10(%ebp),%edx

0×08048456 : mov 0×8(%ebp),%ecx

0×08048459 : mov 0xc(%ebp),%eax

0x0804845c : mov (%edx),%edx

0x0804845e : add %edx,(%ecx)

0×08048460 : add %edx,(%eax)

0×08048462 : pop %ebp

0×08048463 : ret

End of assembler dump.

我们可以看到GCC只为foo2生成了优化后的代码，而foo1并未被优化。这个结果让人有些摸不着头脑。难道编译器认为char*指针有成为int*指针所指对象的alias的潜在可能，而int*指针无法成为long long int*指针所指对象的alias？在C99规范中我也没能找到解释这一现象的答案。看来即使增加了restrict，编译器也是有选择的信任，至少Gcc是这样的。

restrict的作用范围与其修饰的指针的生命周期一致，你可以声明文件作用域(file scope)的restrict指针变量，也可以在某个代码block中使用restrict指针。如果某个结构体成员是restrict pointer类型，那该指针的生命周期就等同于该结构体实例的生命周期。

如果你恶意破坏你和Compiler之间的契约，别指望Compiler会有Warning提示，Compiler在这方面是完全信赖程序员的，不确定行为不可避免。比如：

void foo(int *restrict p, int *restrict q, int *restrict r) {

*p += *r;

*q += *r;

}

int main() {

int a = 1;

int b = 2;

int c = 3;

foo(&a, &b, &a);

printf("a = %d, b = %d, c = %d\n", a, b, c);

}

执行优化后的程序，我们得到的输出为：

$ a.out

a = 2, b = 4, c = 3

这显然与预期的a = 2, b = 3, c = 3不符，错误原因就在于你单方面违反了restrict契约。

C99规范中对restrict关键字的讲解还算不少，甚至还给出了formal definition(C99 6.7.3.1)，不过这个定义简直就像一段天书，实在是晦涩难懂(《[The New C Standard](http://book.douban.com/subject/3420775/)》一书对此有逐句的解释，不过依旧很难理解)。另外restrict的存在对程序本身的语义没有任何影响，对于不支持restrict的编译器也大可忽略restrict修饰符。

至于在平时开发中如何使用restrict，我个人觉得最好是在有一定理解的前提下使用。这对C程序员能力还是有一定要求的。首先要明确你编写的函数内部是否有可以优化的地方，如果根本没有可优化的潜力，那使用restrict就画蛇添足了；当然还有一种情况下你用restrict并不是期望编译器给予优化，而是你的实现算法是基于参数指针所指内存对象无alias的前提的，你在函数原型中用restrict修饰参数主要是想将你的意图告知该函数的使用者；第二要知道restrict对函数内部实现的约束，不要在内部实现时违反约束，导致未定义行为；第三如果你是一个使用者，面对采用了restrict修饰的函数接口，如void *memcpy(void * restrict s1, const void * restrict s2, size_t n)，你要注意不能违反restrict约束，否则也会导致未定义行为。如果你是一个公共库的开发者，你更应该尽量采用restrict，这对你的库代码的性能会是大有裨益的。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

char 比int 短long long 比int 长，前者有交叠的危险所以失效

aa

活到老学到老

感谢 学习了