---
title: HelloWorld.s
url: https://tonybai.com/2010/02/28/helloworld-in-assembly/
published: '2010-02-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# HelloWorld.s

都说汇编不易学习和使用，的确不假。自己自大学以来也曾多次尝试[学习汇编](http://tonybai.com/2005/11/12/open-the-gate-to-assembly-language/)，甚至大学时还有相应课时，但是自己对汇编依旧是浅尝辄止。工作后也少有使用，对汇编的认识也就停留在基础层面。汇编的学习与对计算机系统的理解是密不可分的。工作这些年也算是一直浸淫于系统层面，经过多本底层相关书籍的教诲以及工作中的实践，对计算机系统的理解就自然而然加深了。昨天下载了一本名为：“[Professional Assembly Language](http://www.douban.com/subject/1446250/)(中文名：汇编语言程序设计)” 的电子书，目的是想了解一下[C内联汇编](http://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html)（Inline Assmebly）。花了半个小时读后，居然感觉轻松自如，和自己大脑中的知识融会贯通起来。发现这本书在[卓越网](http://tonybai.com/2007/11/15/buy-book-on-internet-for-the-first-time/)还有“剩本”，也就抓紧买了下来，下周到货。

本书使用linux和AT&T汇编语法，正合我的胃口。以下是根据书中例子改出来的一段汇编版HelloWorld.s：

# HelloWorld.s

# as -o HelloWorld.o HelloWorld.s

# ld -o HelloWorld HelloWorld.o

.section .data

output:

.ascii "hello world\n"

.section .text

.globl _start

_start:

nop

movl $output, %ecx

movl $4, %eax # the index of sys call 'write'

movl $1, %ebx # file descriptor

movl $12, %edx # length of the string

int $0×80

movl $1, %eax # the index of sys call 'exit'

movl $0, %ebx

int $0×80

在调试上面代码时有两个注意事项要考虑：

1、调用write时，%edx务必赋值，否则将无法正确输出；

2、在Ubuntu 9.04下，如果结尾不调用exit，执行程序后会有'段错误'，目前依然不得其解，通过[GDB](http://tonybai.com/2009/03/22/also-talk-about-debugging-software/)调测后猜测是未作收尾处理，处理器继续取EIP所指地址的指令内容，执行出错。

将这段代码拿到[Solaris10](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/) for x86上执行，无法输出“hello world”，并伴有'段错误'，目前尚不得其解。

让HelloWorld.s作为再次尝试熟悉汇编的一个起点吧^_^。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

汇编~正想找这方面知识学习.

还有逻辑和算法的~~

你好，听说你以前在china-pub上买过书。我现在也急需那本计算理论导引，但是等级不够，能否帮忙代购，我的qq号是454992519。