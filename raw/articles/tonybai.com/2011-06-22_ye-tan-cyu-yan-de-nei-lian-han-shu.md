---
title: 也谈C语言的内联函数
url: https://tonybai.com/2011/06/22/also-talk-about-inline-function-in-c/
published: '2011-06-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈C语言的内联函数

有这样一段代码：

/* foo.c */

#include "stdio.h"

inline void foo() {

printf("inline foo in %s\n", __FILE__);

}

int main() {

foo();

return 0;

}

我采用[C99](http://en.wikipedia.org/wiki/C99)标准，并在不加任何优化选项的情况下编译之：

$ gcc -std=c99 foo.c -o foo

foo.c: In function ‘foo’:

/tmp/ccLGkuIK.o: In function `main':

foo.c:(.text+0×7): undefined reference to `foo'

collect2: ld returned 1 exit status

这样的结果出乎我的意料。我原以为用inline修饰的函数定义，如上面的foo函数，在编译器未开启内联优化时依旧可以作为外部函数定义被编译器使用。但通过上面[gcc](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)输出的错误信息来看，inline函数的定义并没有被看待为外部函数定义，这样链接器才无法找到foo这个符号。C99标准新增的inline似乎与我对inline语义的理解有所不同。

C语言原本是不支持inline的，但C++中原生对inline的支持让很多C编译器也为C语言实现了一些支持inline语义的扩展。C99将inline正式放入到[标准C语言](http://en.wikipedia.org/wiki/ANSI_C)中，并提供了inline关键字。和C++中的inline一样，C99的inline也是对编译器的一个提示，提示编译器尽量使用函数的内联定义，去除函数调用带来的开销。inline只有在开启编译器优化选项时才会生效。正如上面的例子，当我们打开优化选项并重新编译时，我们会看到：

$ gcc -std=c99 foo.c -O2 -o foo

$./foo

$ inline foo in foo.c

在-O2的优化选项下，编译器进行了内联优化，并采用了foo的inline定义。通过汇编代码我们也可以看出：foo.s中并没有显式地使用call进行函数调用，函数调用被优化掉了：

/* foo.s : gcc -std=c99 foo.c -O2 -S */

.file "foo.c"

.section .rodata.str1.1,"aMS",@progbits,1

.LC0:

.string "foo.c"

.LC1:

.string "inline foo in %s\n"

.text

.p2align 4,,15

.globl main

.type main, @function

main:

pushl %ebp

movl %esp, %ebp

andl $-16, %esp

subl $16, %esp

movl $.LC0, 8(%esp)

movl $.LC1, 4(%esp)

movl $1, (%esp)

call __printf_chk

xorl %eax, %eax

leave

ret

.size main, .-main

.ident "GCC: (Ubuntu 4.4.3-4ubuntu5) 4.4.3"

.section .note.GNU-stack,"",@progbits

我们在另外一个文件bar.c中提供一个foo的外部函数定义：

/* bar.c */

#include

void foo() {

printf("global foo in %s\n", __FILE__);

}

我们将foo.c和bar.c放在一起编译（未开启优化选项）：

$ gcc -std=c99 foo.c bar.c -o foo

$ ./foo

$ global foo in bar.c

链接器为foo.c中的符号foo选择了bar.c中的foo函数定义。这样看来我们甚至可以有两个同名（名字都是foo）的函数定义，只不过一个是inline定义，一个是外部定义，它们并不冲突。

再开启优化选项，我们得到：

$ gcc -std=c99 foo.c bar.c -o foo

$ ./foo

$ inline foo in foo.c

这一次编译器选择了foo的inline定义。

究其原因：foo.c和bar.c分处于两个不同的编译单元，在未开启内联优化的情况下，foo.c对应的目标文件foo.o中foo只是一个未定义的符号，而bar.o中的foo却是一个global符号，并对应一块独立的实现代码。[链接器](http://tonybai.com/2007/12/08/those-things-about-symbol-linkage/)自然采用了bar.c中的foo函数定义。而在开启了内联优化的情况下，编译器在进行foo.o这个编译单元的编译期间就直接对foo进行了优化，并采用了foo的inline定义，直接放到了main函数的[汇编代码](http://tonybai.com/2005/11/12/open-the-gate-to-assembly-language/)中，没有显式地call foo，并且foo.o中并未为foo单独生成Global函数代码，这样在最后的链接阶段，bar.o就变成"打酱油"的了^_^。

以上只是为了说明C99内inline语义而做的试验。在现实开发中，我们绝不应该这么去做。我们要确保函数的inline定义和非inline定义的语义一致性。那能否做到让一份函数定义既可以作为inline定义，也可以作为外部函数定义呢？这意味着我们在开启内联优化时，既要在inline函数定义的编译单元里执行内联优化，也要为inline函数生成一份独立的global的函数定义（汇编码）。

我们增加一个头文件foo.h：

/* foo.h */

extern void foo();

/* foo.c */

#include

#include "foo.h"

inline void foo() {

printf("foo in %s\n", __FILE__);

}

int main() {

foo();

return 0;

}

我们在开启优化和未开启优化两种情况下分别编译执行：

$ gcc -std=c99 foo.c -o foo

$ ./foo

$ foo in foo.c

$ gcc -std=c99 foo.c -o foo -O2

$ ./foo

$ foo in foo.c

我们看到：无论哪种情况，我们都可以顺利通过编译，并且得到正确的执行结果。我们来看看汇编码有何变化：

在未开启优化的情况下，我们得到如下汇编码：

.globl foo

.type foo, @function

foo:

pushl %ebp

… …

call printf

leave

ret

.size foo, .-foo

… …

main:

pushl %ebp

movl %esp, %ebp

andl $-16, %esp

call foo

… …

ret

内联优化并未生效，main代码中进行了foo的函数调用。但与本文开始时的那个例子不同的是，编译器为foo生成了一份独立的global的函数定义汇编码块，这块代码可以直接被外部引用，也就是说在未开启优化的情况下，foo定义被看成了外部函数定义。

但开启优化选项的情况下，我们得到如下汇编码：

.globl foo

.type foo, @function

foo:

pushl %ebp

… …

call __printf_chk

leave

ret

… …

main:

pushl %ebp

movl %esp, %ebp

andl $-16, %esp

subl $16, %esp

movl $.LC0, 8(%esp)

movl $.LC1, 4(%esp)

movl $1, (%esp)

call __printf_chk

xorl %eax, %eax

leave

ret

内联优化生效了，main代码中并未显式地进行foo的函数调用。并且编译器依旧为foo生成了一份独立的global的函数定义汇编码块，这块代码可以直接被外部引用，也就是说在开启优化的情况下，foo定义在本编译单元被看作内联定义，同时对其他编译单元而言，也是外部函数定义。

我们通过在头文件中增加一个外部函数声明实现了我们的目标！不过上面方法虽然实现了一份定义既可以当作inline定义，也可以作为外部定义，但inline定义仅局限于定义它的那个编译单元，其他编译单元即使在开启内联优化时，依旧无法实施内联优化。如果我们希望多个编译单元共享一份inline定义并且这份定义也可以同时作为外部函数定义，我们该如何做呢？ – 那我们只能把inline定义放到头文件中了！见下面代码：

/* foo.h */

inline void foo() {

printf ("foo in %s\n", __FILE__);

}

/* foo.c */

#include

#include "foo.h"

int main() {

foo();

return 0;

}

/* bar.c */

#include

#include "foo.h"

void bar() {

foo();

}

$ gcc -std=c99 foo.c -S -O2

我们看看开启优化情况下的bar.c和foo.c对应的汇编代码，以foo.s为例：

/* foo.s */

… …

main:

pushl %ebp

movl %esp, %ebp

andl $-16, %esp

subl $16, %esp

movl $.LC0, 8(%esp)

movl $.LC1, 4(%esp)

movl $1, (%esp)

call __printf_chk

xorl %eax, %eax

leave

ret

… …

内联优化生效，bar.s也是一样，不过编译器没有为我们生成foo的独立外部定义代码，这样的foo定义只能作为inline定义，而不能被作为外部函数定义。如果此时不开启优化选项编译，我们还会得到如下错误：

/tmp/ccpp1E7i.o: In function `main':

foo.c:(.text+0×7): undefined reference to `foo'

/tmp/ccQk872R.o: In function `bar':

bar.c:(.text+0×7): undefined reference to `foo'

collect2: ld returned 1 exit status

我们稍作改动，在foo.c和bar.c的文件开始处，我们加上这样一行代码："extern inline void foo();"，加上后，我们重新编译，这回foo在被内联优化的同时，也被生成了一份独立的外部函数定义。我们的目标又达到了!

总之，C99中inline相对比较怪异，使用时务必小心慎重。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

在第一个程序的inline前面加上static也行。本来以为加上extern应该也行的，结果不行。