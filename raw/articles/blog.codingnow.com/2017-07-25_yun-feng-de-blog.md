---
title: 云风的 BLOG
url: https://blog.codingnow.com/2017/07/
published: '2017-07-25'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 浮点运算潜在的结果不一致问题

昨天阿楠发现了项目中的一个 bug ，是因为浮点运算的前后不一致导致的。明明是完全相同的 C 代码，参数也严格一致，但是计算出了不相同的结果。我对这个现象非常感兴趣，仔细研究了一下成因。

原始代码比较繁杂。在弄清楚原理后，我简化了出问题的代码，重现了这个问题：

static void foo(float x) { float xx = x * 0.01f; printf("%d\n", (int)(x * 0.01f)); printf("%d\n", (int)xx); } int main() { foo(2000.0f); return 0; }

使用 gcc 4.9.2 ，强制使用 x87 浮点运算编译运行，你会发现令人诧异的结果。

gcc a.c -mfpmath=387 19 20

前一次的输出是 19 ，后一次是 20 。

这是为什么呢？让我们来看看 gcc 生成的代码，我截取了相关的段落：

flds 16(%rbp) flds .LC0(%rip) fmulp %st, %st(1) fstps -4(%rbp) ; 1. x * 0.01f 结果保存到内存中的 float 变量中 flds 16(%rbp) flds .LC0(%rip) fmulp %st, %st(1) fisttpl -20(%rbp) ; 2. x * 0.01f 结果直接转换为整型 movl -20(%rbp), %eax movl %eax, %edx leaq .LC1(%rip), %rcx call printf flds -4(%rbp) ; 3. 读出 1. 保存的乘法结果 fisttpl -20(%rbp) movl -20(%rbp), %eax movl %eax, %edx leaq .LC1(%rip), %rcx call printf

这里我做了三行注释。

首先，0.01 是无法精确表示成 2 进制的，所以 * 0.01 这个操作一定会存在误差。

两次运算都是 x * 0.01f ，虽然按 C 语言的转换规则，表达式中都是 float 时，按 float 精度运算。但这里 gcc 生成的代码并没有严格设置 FPU 的精度控制，在注释 2 这个地方，乘法结果是直接从浮点寄存器转换为整数的。而在注释 1 这个地方，把乘法结果通过 fstps 以低精度形式保存到内存，再在注释 3 的地方 flds 读回。

所以在注释 2 和注释 3 的地方，浮点寄存器 st 内的值其实是有差别的，这导致了 fisttpl 转换为整数后结果不同。

2018 年 6 月 14 日补充：

[在 DDJ 1997 年的一篇访谈文章中](http://collaboration.cmc.ec.gc.ca/science/rpn/biblio/ddj/Website/articles/DDJ/1997/9711/9711a/9711a.htm)，谈及了类似的问题。

引用如下：

Let me give an example, which arose yesterday. A student was doing a computation involving a simulation of a plasma. It turns out that as you go through this computation there will be certain barriers. This may be a reflecting barrier. That means if a particle moves through this barrier, it should not really go through, it should be reflected. Others may be absorbing, others may be periodic. He has a piece of code that is roughly

float x, y, z; int j; ... x = y + z; if (x >= j) replace (x); y = x; ...

As far as we can tell, when he turns on optimization, the value of x is computed in a register with extra width. This happens on the Intel machine because the registers have extra width. It also happens on some others. The value of x that he computes is not, in fact, a float. It's in a register that's wider. The machine stores x somewhere, and in the course of doing that, converts it to a float. But the value used in the comparison is the value in the register. That x is wider. The condition that the register x be greater than or equal to j doesn't guarantee that x, when stored in y, will be less than j. Sometimes y=j, and that should never be. My student counted on what compiler writers call "referential transparency" and was disappointed because the compiler writer saved some time in optimization by not reloading the register from the stored value.