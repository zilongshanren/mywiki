---
title: 视警告为错误
url: https://tonybai.com/2010/09/05/view-warning-as-error/
published: '2010-09-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 视警告为错误

每当你Build Project代码的时候，如果看到的是满屏的Warning，那么提醒你小心了，不妨看看[《高效程序员的45个习惯》](http://book.douban.com/subject/4164024/)中对Warning的态度和处理方式。该书中的第34个习惯讲的是“警告就是错误”！ 当然这个“习惯”所阐述的内容并不是这本书首创，在很多经典的传授编程之道的书中也都提到过。

将警告作为错误来处理，说起来容易，可作起来可并不那么简单。这不仅仅只是一个态度的问题，有时候还需要有技术手段或技巧去帮助你完成。《高效程序员的45个习惯》一书的作者也在该习惯所对应的“平衡的艺术”中提到：“如果确实没有应对之策的话，那就不要再浪费更多时间了。但类似这种情况很少发生”。另外他建议应该经常使用编译器的directive（指示器），将一些实在无法避免但又确定不是潜在缺陷的警告进行提示，告知编译器这个地方的警告可以不去理会。

将警告视为错误首先需要的就是勇气，大胆的在你的Makefile中将-Werror赋予给[Gcc](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)吧。Gcc则为你提供了一定的技术手段来帮你处理面对无法避免的警告时“左右为难”的情况。

Gcc为我们提供的技术手段就是Pragmas，虽然[Gcc手册](http://gcc.gnu.org/onlinedocs/)中建议我们一般情况下不要显式的使用[Pragmas](http://gcc.gnu.org/onlinedocs/Pragmas.html)，但必要时还是需要这个工具的帮助的。

#pragma directives这个指示器嵌入在源码中，用于在源码编译时给GCC编译器提供一些指示信息。Pragmas有多种分类，这里我们需要的是[Diagnostic Pragmas](http://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Pragmas.html)。简单的说，嵌入在源码中的Diagnostic Pragmas给我们提供了如下一些能力：

-> 将某类编译警告按编译错误处理 (如：#pragma GCC diagnostic error "-Wformat")

-> 将某类编译错误按编译警告处理 (如：#pragma GCC diagnostic warning "-Wformat")

-> 忽略某类编译警告 (如：#pragma GCC diagnostic ignored "-Wformat")

Gcc对Diagnostic Pragmas的支持是随着版本进化而逐渐增强的，在gcc 3.4.6版本下[Diagnostic Pragmas](http://gcc.gnu.org/onlinedocs/gcc-3.4.6/gcc/Pragmas.html#Pragmas)是不被accepted的，Gcc只accept五类Pragmas;到了gcc 4.4.4版本，Gcc已经可以支持12类Pragmas，这其中就包括[Diagnostic Pragmas](http://gcc.gnu.org/onlinedocs/gcc-4.4.4/gcc/Pragmas.html#Pragmas)。

通过实际的测试也可以证实以上说明。

e.g.

/* testpragma.c , gcc -Wall testpragma.c */

#include

#pragma GCC diagnostic error "-Wformat"

int main() {

printf("%d\n", "Diagnostic Pragmas Test");

return 0;

}

在Sparc [Solaris 10](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/)上使用gcc 3.4.6编译结果如下：

gcc -Wall testpragma.c

testpragma.c:3: warning: ignoring #pragma GCC diagnostic

testpragma.c: In function `main':

testpragma.c:5: warning: int format, pointer arg (arg 2)

编译器提示忽略了diagnostic pragma指示。

而在[Ubuntu 10.04](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/) Gcc 4.4.3版本下编译结果如下：

gcc -Wall testpragma.c

testpragma.c: In function ‘main’:

testpragma.c:5: error: format ‘%d’ expects type ‘int’, but argument 2 has type ‘char *’

编译器正确执行了我们给出的指示^_^。

#pragma directive的作用范围也很好理解：

首先肯定是在同一编译单元范围内有效，在A编译单元中设置的#pragma directive，在B编译单元是无效的。比如我另外编写一个utils.c，其内容如下：

#include

void foo() {

printf("%d\n", "In another compile unit");

}

我们将utils.c与testpragma.c一起编译，gcc -Wall testpragma.c utils.c，得到的结果是：

testpragma.c: In function ‘main’:

testpragma.c:5: error: format ‘%d’ expects type ‘int’, but argument 2 has type ‘char *’

utils.c: In function ‘foo’:

utils.c:4: warning: format ‘%d’ expects type ‘int’, but argument 2 has type ‘char *’

在testpragma.c这个编译单元，#pragma directive生效，但是在utils.c这个编译单元并不生效，依旧被诊断为Warning。

其次，在同一个编译单元中，#pragma directive影响的范围是其所在行之后的代码，直到下一次修改针对同样warning option的#pragma被放置。还是举例说明，我们改造一下testpragma.c：

/* testpragma.c */

#include

#pragma GCC diagnostic error "-Wformat"

void foo() {

printf("%d\n", "Diagnostic Pragmas Scope Test");

}

int main() {

printf("%d\n", "Diagnostic Pragmas Test");

return 0;

}

编译命令执行后，Gcc给出的输出结果是：

testpragma.c: In function ‘foo’:

testpragma.c:5: error: format ‘%d’ expects type ‘int’, but argument 2 has type ‘char *’

testpragma.c: In function ‘main’:

testpragma.c:9: error: format ‘%d’ expects type ‘int’, but argument 2 has type ‘char *’

#pragma directive从头置尾一直发挥作用，两个format Warning都被当作Error报告了。

现在我们对main中的问题放松要求，将源码变为：

/* testpragma.c */

#include

#pragma GCC diagnostic error "-Wformat"

void foo() {

printf("%d\n", "Diagnostic Pragmas Scope Test");

}

#pragma GCC diagnostic ignored "-Wformat"

int main() {

printf("%d\n", "Diagnostic Pragmas Test");

return 0;

}

执行编译命令后，Gcc的提示变为：

testpragma.c: In function ‘foo’:

testpragma.c:5: error: format ‘%d’ expects type ‘int’, but argument 2 has type ‘char *’

显然对-Wformat按照Error处理的作用范围仅限于foo这个函数，因为在foo之后我们修改了对-Wformat的指示！

有了编译器的支持，我们将更有信心去养成“视警告为错误”的习惯了。实际工作中，#pragma directive应用应该不多，因为多数情况下的警告都是可以通过正常的代码完善消除掉的。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论