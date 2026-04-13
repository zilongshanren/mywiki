---
title: 也谈指针运算
url: https://tonybai.com/2010/02/23/also-talk-about-pointer-arithmetics/
published: '2010-02-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈指针运算

指针在C语言中的位置这里就不多说了，这里说一下C的指针运算。指针运算一般针对的是同一连续内存块，不同内存块之间的指针运算无意义，甚至可能导致异常情况。

指针运算主要针对数组，常见的运算类型：+i, -i, ++, –以及 < , >等。

我们以+i操作为例。运算时编译器需要知道一些必要的信息，比如p = p + 1操作时编译器需要知道这个运算后，p这个指针需要移动多少个字节，那这个信息哪里来呢，由指针p所指数据单元的类型来确定。

比如：

int *p; [...] ; p = p + i => p指向int型数据，p加i运算后移动i * sizeof(int)个字节，即i * 4个字节。

char *p; [...] ; p = p + i => p指向char型数据，p加i运算后移动i * sizeof(char)个字节，即i * 1个字节。

struct Foo *p; [...] ; p = p + i => p指向struct Foo型数据，p加i运算后移动i * sizeof(struct Foo)个字节.

char *p[4](<=> (char*)p[4]，可用char **p指向该数组中的某一个元素); [...] ; p = p + i => p指向char*数据，p加i运算后移动i * sizeof(char*)个字节，即i * 4个字节.

char (*p)[4](p是一个指向二维数组的指针，该二维数组的行宽度为char[4]); [...] ; p = p + i => p指向char[4]型数据，p加i运算后移动i * sizeof(char[4])个字节，即i * 4个字节。

int (*p)[7](p是一个指向二维数组的指针，该二维数组的行宽度为int[7]); [...] ; p = p + i => p指向int[7]型数据，p加i运算后移动i* sizeof(int[7])个字节，即i * 28个字节。

再考虑一个稍微复杂些的指针运算：有一个多维数组int a[5][6]，一般取其中某个元素时可采用*(*(a + i) + j)的形式来达到目的。这个指针运算有些复杂，起码不那么一目了然，我们不妨用”代换法”来分析一下:

我们可将int a[5][6]理解为一个拥有5个元素，每个元素是int[6]类型的一维数组，其实若写成(int[6]) a[5]则更好理解(但可惜这不是C语言的语法)，那么(int[6]) *p1则是指向数组(int[6]) a[5]中某个元素的指针,且可进行p1 = a这样的赋值；现在我们换成C语言语法那就是int (*p1)[6]；p1 = a。这样一来我们将二维化为一维，就可以利用前面的规则了。a + i <=> p1 + i，指针移动 i * sizeof(int[6]);

我们让p2 = *(a + i) <=> *(p1 + i)，这样p2同样也变成一维数组(int型一维数组)，p2作为数组名，自然也可作指针操作；p2 + j后，指针再移动 sizeof(int) * j个字节。

综上，*(*(a + i) + j)运算后，指针实际移动了 i * sizeof(int[6]) + j * sizeof(int)个字节。

[多维数组](http://bigwhite.blogbus.com/logs/3937009.html)的指针运算必要信息是由除最左维度外其他所有维度的长度信息所共同组成的，比如一个三维数组：char a[5][6][7]，匹配该数组的指针类型为char (*p)[6][7]; 二三维度的长度为编译器提供了指针运算的必要信息，这里也提醒我们在将多维数组作为参数传递时务必要小心参数匹配的问题，维度信息不同会导致多维数组与相应的函数形参匹配，比如：

char a[5][6][7]与void func(char a[][7][8])；因维度信息不同而无法匹配。

char a[5][6][7] or char (*p)[6][7]则与void func(char a[5][6][7])/void func(char (*p)[6][7])匹配。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论