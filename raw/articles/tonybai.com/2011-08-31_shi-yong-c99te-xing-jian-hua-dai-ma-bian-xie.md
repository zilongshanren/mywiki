---
title: 使用C99特性简化代码编写
url: https://tonybai.com/2011/08/31/simplify-coding-in-c99/
published: '2011-08-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用C99特性简化代码编写

至今我还记得第一次听说[C99标准](http://en.wikipedia.org/wiki/C99)还是在读大一时，那时同寝一位兄弟手头有一本[Herbert Schildt](http://en.wikipedia.org/wiki/Herbert_Schildt)编写的《C: The Complete Reference，Fourth Edition》(中文名：[C语言大全](http://book.douban.com/subject/1205911/))，书封皮的右上角上赫然写着"详解C99 ANSI/ISO最新标准"，那时离C99标准发布仅仅才一年。

那个时候我们大学授课以及实验用的还是Borland的[Turbo C 2.0](http://en.wikipedia.org/wiki/Borland_Turbo_C)，C99标准根本无从谈起。转眼间十多年过去了，C99标准逐渐成熟，各大编译器厂商以及开源编译器都完善了自己的产品，对C99有了很好的支持，像Gcc编译器在最新的4.6版本里几乎完全支持所有[C99特性](http://gcc.gnu.org/c99status.html)。但如果你依旧在用Microsoft的Visual Studio，那么很遗憾你可能依旧无法使用C99的诸多新特性。

工作以来一直使用[GCC](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)作为C的编译器，但一直采用的是GCC的默认C标准，即gnu89，也就是C90标准加上一些GCC自行的扩展。直到去年年末与[Dreamhead](http://dreamhead.blogbus.com)闲聊时，Dreamhead提出可利用C99标准简化代码编写的想法，我这才有意识地去主动了解一些有关C99与上一版标准不同的地方，并在今年的项目中尝试用gnu99(-std=gnu99)替代gnu89。

与上一版标准相比，C99做了几十处修订，可用于简化代码编写的新增特性虽然不多，不过大多都还算很实用，其中一些是GCC在自己的扩展中已经存在了多年的特性，这次也被正式纳入C99标准中了。

下面我就列举一些可以帮助你简化C代码编写的C99特性（也许还不够全面）：

* 布尔类型

很多C程序员都很向往Java以及C#等语言中提供的原生bool类型，在C语言没有真正提供bool类型之前，很多C程序中都有这样的代码：

#undef bool

#undef true

#undef false

typedef enum {

false,

true

} bool;

C99标准中正式引入了布尔类型_Bool，注意是_Bool而不是bool。虽然不是bool，而是一个对于类型名称而言有些丑陋的名字，但这也给C程序员带来了些许福音。C标准委员会显然也考虑到了大家的质疑，遂又为C99引入了一个标准头文件"stdbool.h"，在该文件中我们看到了bool，true和false的定义，只不过它们不是原生的，而是宏：

#define bool _Bool

#define true 1

#define false 0

即使是这样，我们依旧可以无需编写自己的bool类型了（不过如果考虑在不同版本编译器之间的移植的话，还是需要根据__STDC_VERSION__来选择到底使用内置bool还是自定义bool的）。

#include

bool found = true;

bool empty = false;

bool is_foo();

int xx_hash_create(xx_hash_t **h, bool shared);

或者用_Bool类型关键字：

/* no header needed */

_Bool found = 1;

_Bool empty = 0;

_Bool is_foo();

int xx_hash_create(xx_hash_t **h, _Bool shared);

* 可变参数宏

在不支持可变参数宏的日子里，我们经常这么定义一些宏：

#define compare2(compf, arg1, arg2) \

compf(arg1, arg2)

#define compare3(compf, arg1, arg2, arg3) \

compf(arg1, arg2, arg3)

#define compare4(compf, arg1, arg2, arg3, arg4) \

compf(arg1, arg2, arg3, arg4)

… …

有了可变参数宏后，我们只需一个定义即可：

#define compare(compf, …) \

compf(__VA_ARGS__)

compare(strcmp, "hello", "world");

compare(triplestrcmp, "hello", "world", "foo");

… …

* Compound Literals

这个特性比较难于译成中文，直译起来就是"复合字面量"。其实它类似一个匿名变量，其语法形式为"(类型){初始值列表}"，下面是一些例子可以帮助你理解：

在没有"Compound Literals"特性之前，我们可以这样编写代码：

struct xx_allocator_t allocator;

allocator.af = malloc;

allocator.ff = free;

xx_hash_new(.., &allocator);

使用C99特性，我们就可以省掉xx_hash_new之前的那个变量定义和初始化了：

xx_hash_new(.., &(struct xx_allocator_t){.af = malloc, .ff = free});

* Designated initializers(指定初始化器)

在没有这个特性之前，我们在用初始化器初始化一个数组或者一个结构体时，一般要给所有元素都赋值：

struct foo {

int a;

char b;

char s[20];

};

int a[5] = {1, 2, 3, 4, 5};

struct foo f = {1, 'A', "hello"};

struct foo v[3] = {

{1, 'A', "hello"},

{2, 'B', "hi"},

{3, 'C', "hey"}

};

如果我们只想为数组中某一个元素赋值，或者为结构体中某一个字段赋值的话，我们就不能使用初始化器了，只能这样来做：

int a[5];

a[2] = 3;

struct foo f;

strcpy(f.s, "hello");

struct foo v[3];

v[1].a = 2;

v[1].b = 'B';

strccpy(v[1].s, "hi");

C99给我们带来了指定初始化器的特性，我们可以在初始化时指定为哪个结构体字段或数组元素赋值：

int a[5] = {[2] = 3, [4] = 5};

struct foo f = {.s = "hello"};

struct foo v[3] = {

[1] = {.a = 2, .b= 'B', .s = "hi"}

};

* 为选择与迭代语句引入新的块范围

这个C++程序员定然不陌生，在C++中我们可以这样定义一个循环：

for (int i = 0; i < 100; i++) {

… …

}

但在老版本C中，我们只能这样做：

int i;

for (i = 0; i < 100; i++) {

… …

}

不过使用C99后，你就可以和C++程序员同等待遇了。

和近几年涌现的一些新语言相比，古老的C语言中可以用于简化代码编写的[语法糖](http://en.wikipedia.org/wiki/Syntactic_sugar)就显得少得有些可怜。[C1x标准](http://en.wikipedia.org/wiki/C1X)目前正在制定中，但也不要对C1x期望太高，毕竟C语言的精髓并非旨在改善开发效率。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论