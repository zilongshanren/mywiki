---
title: Go defer的C实现
url: https://tonybai.com/2013/02/03/implement-go-defer-in-c/
published: '2013-02-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go defer的C实现

[Go语言](http://golang.org)中引入了一个新的关键字defer，个人认为这个语法关键字让异常处理也变得得心应手许多，对改善代码的可读性和可维护性大有裨益，是典型的语法棒棒糖^_^。

像下面这种代码（伪代码）：

void foo() {

apply resource1;

retv = action1;

if not success

release resource1

apply resource2;

retv = action2;

if not success

release resource1

release resource2

}

有了defer后，代码就变得优美多了。

void foo_with_defer() {

apply resource1;

defer (release_resource1)

retv = action1;

if not success

return

apply resource2;

defer (release_resource2)

retv = action2;

if not success

return

}

如果能在[C语言](http://tonybai.com/tag/C)中实现defer这样的语法糖，那该多棒！是否可行呢？经过一段时间钻研，找到一个不那么美的实现方法，约束也很多，也不甚严谨， 谈不上什么可移植性，切不可用到产品环境，权当一种探讨罢了。

Go中defer的语义大致是这样的：

* 在使用defer的函数退出前，defer后面的函数将会被执行；

* 如果一个函数内有多个defer，那么defer按后进先出（LIFO）的顺行执行；

* 即使发生Panic，defer依然可以得到执行

最后一个比较难于模拟，这里仅先尝试前两个语义。下面从设计思路说起。

*** “借东风”**

要想模拟defer，首先要考虑的一点那就是defer后的语句是在函数return之前执行的。在标准C中，我们无任何举措可以实现这些。要在 C中实现defer，势必要借用一些编译器扩展特性，比如Gcc的扩展。这里实验所使用的编译器是[Gcc](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)(4.6.3 ([Ubuntu 12.04](http://tonybai.com/2012/12/04/upgrade-ubuntu-to-1204-lts/)))。Gcc扩展支持-finstrument-functions编译选项，该选项可以在函数执行前后插入一段运行代码。在之前写过的一篇名 为“[为函数添加enter和exit级trace](http://tonybai.com/2011/07/13/add-enter-and-exit-trace-for-your-function/)”的文章中对此有较为详细的说明，这里我们还要用到这个扩展特性。

*** 偷天换日**

如果完全模仿Go的语法，在C中使用defer，大致是这样一种形式：

void foo(void) {

FILE * fp = NULL;

fp = fopen("foo.txt", "r");

if (!fp) return;

defer(fclose(fp));


/* use fp */

… …

return;

}

但C毕竟是C，一门静态的编译型语言，我们如何将fclose(fp)这个信息传递给编译器自动插入的代码中呢？在C语言中，几乎没有手段获得函 数的元信息以及运行时参数信息，并再通过这些信息重新调用和执行该函数。我们得“想招”将这些信息存储起来。

大家知道C语言中的函数，比如这里的fclose，其实是一个函数起始地址；如果我们知道函数地址或又叫函数指针，再加上函数的参数，我们就可以 拼凑在一起执行该函数了。但理论上来说，函数指针也是有类型的，比如：

typedef int (*FUNC_POINTER)(int, int);

这个函数指针类型可以用来执行诸如：int foo(int a, int b)这样的函数，比如：

FUNC_POINTER fp = foo；

fp(1, 2);

但defer后面执行的函数千差万别，我们如何能够得知函数对应的函数指针类型呢？用void*存储？比如：

void *p = foo;

p(1, 2);

编译器会给你一个严重错误！p不是函数指针，不能这么用。那我们如何能让编译器知道这个指针是一个可调用的函数指针呢？我们试试来定义一个“通用 的函数指针”：

typedef void (*defer_func)();

没有返回值，没有参数，这样的函数指针能否执行foo这样的函数呢？答案是可以的，但不是那么完美。至少你不会得到返回值。这么做有两点考虑：

a) 至少可以让编译器知道这是一个函数指针，可以被用来执行函数。

b) 通常我们并不关心defer后面函数的返回值。

c) 参数列表的不同至少目前可以逃过编译器的错误检查，至多给个Warning。

函数指针的问题暂时算是有着落了，那参数怎么办？也就是说defer(fclose(fp))中的fp如何存储下来呢？如果在C中真的使用 defer(fclose(p))这种形式的语法，那么我是砸破脑袋也想不出啥招了！因此我们应该重新设计一下C中的defer应该如何使用？我 们用下面的语法来替代：

defer(fclose, 1, p);

fclose是函数起始地址，1是参数个数，p则是传给fclose的参数。这样fclose和p都可以单独分离出来存储了。但是还是那句 话：defer后面可以执行的函数千万种，哪能穷尽？怎么才能表示成一种通用的方式存储参数呢？回想一下自己在编码过程中用于释放资源的那几类函 数，无非就是关闭文件、关闭文件描述符(包括socket)、释放内存等，这些函数传递的参数不是指针就是整型数，少有传浮点类型或将一个自定义 结构体以传值的方式传入的。我们不妨再次尝试一次“偷天换日” – 用void*存储整型参数或任意指针类型参数。当然其约束就像刚才所说的那些。不过对付大多数资源释放函数而言，应该是足够的了。至于将参数个数也作为一 个固定参数放入defer中，也是鉴于目前无法通过操作可变个数参数列表相关宏来获得参数数量。

最后一个问题。由于被defer的函数的参数个数不定。defer无法将[可变个数参数](http://tonybai.com/2008/05/07/also-talk-about-c-variable-length-args/)重组后传给被defer的函数。因此目前暂只能通过一种“丑陋”的方式来实现。样例中最多只支持两个参数的被defer函数。

*** 样例**

首先看看我们的examples的主函数文件main.c。

#include <stdio.h>

#include <stdlib.h>

#include "defer.h"

int bar(int a, char *s) {

printf("a = [%d], s = [%s]\n", a, s);

}

int main() {

FILE *fp = NULL;

fp = fopen("main.c", "r");

if (!fp) return;

defer(fclose, 1, fp);

int *p = malloc(sizeof(*p));

if (!p) return;

defer(free, 1, p);

defer(bar, 2, 13, "hello");

return 0;

}

从这里我们可以看到defer的用法，但这不是重点，重点是实现。

有了上面的一些设计思路的阐述，下面的代码也就不难理解了。核心是defer.c。

/* defer.h */

typedef void (*defer_func)();

struct zero_params_func_ctx {

defer_func df;

};

struct one_params_func_ctx {

defer_func df;

void *p1;

};

struct two_params_func_ctx {

defer_func df;

void *p1;

void *p2;

};

struct defer_func_ctx {

int params_count;

union {

struct zero_params_func_ctx zp;

struct one_params_func_ctx op;

struct two_params_func_ctx tp;

} ctx;

};

void stack_push(struct defer_func_ctx *ctx);

struct defer_func_ctx* stack_pop();

int stack_top();

/* defer.c */

struct defer_func_ctx ctx_stack[10];

int top_of_stack = 0; /* stack top from 1 to 10 */

void stack_push(struct defer_func_ctx *ctx) {

if (top_of_stack >= 10) {

return;

}

ctx_stack[top_of_stack] = *ctx;

top_of_stack++;

}

struct defer_func_ctx* stack_pop() {

if (top_of_stack == 0) {

return NULL;

}

top_of_stack–;

return &ctx_stack[top_of_stack];

}

int stack_top() {

return top_of_stack;

}

void defer(defer_func fp, int arg_count, …) {

va_list ap;

va_start(ap, arg_count);

struct defer_func_ctx ctx;

memset(&ctx, 0, sizeof(ctx));

ctx.params_count = arg_count;

if (arg_count == 0) {

ctx.ctx.zp.df = fp;

} else if (arg_count == 1) {

ctx.ctx.op.df = fp;

ctx.ctx.op.p1 = va_arg(ap, void*);

} else if (arg_count == 2) {

ctx.ctx.tp.df = fp;

ctx.ctx.tp.p1 = va_arg(ap, void*);

ctx.ctx.tp.p2 = va_arg(ap, void*);

ctx.ctx.tp.df(ctx.ctx.tp.p1, ctx.ctx.tp.p2);

}

va_end(ap);

stack_push(&ctx);

}

多个defer的FIFO调用顺序用一个固定大小的stack来实现。这里只是为了演示，所以stack实现的简单和固定些。

组装后的函数在funcexit.c中执行：

extern struct defer_func_ctx ctx_stack[10];

__attribute__((no_instrument_function))

void __cyg_profile_func_exit(void *this_fn, void *call_site) {

struct defer_func_ctx *ctx = NULL;

while ((ctx = stack_pop()) != NULL) {

if (ctx->params_count == 0) {

ctx->ctx.zp.df();

} else if (ctx->params_count == 1) {

ctx->ctx.op.df(ctx->ctx.op.p1);

} else if (ctx->params_count == 2) {

ctx->ctx.tp.df(ctx->ctx.tp.p1, ctx->ctx.tp.p2);

}

}

}

最后我们将defer.c、funcexit.c编译成一个.so文件：

gcc -g -fPIC -shared -o libcdefer.so funcexit.c defer.c

而编译main.c的方法如下：

gcc -g main.c -o main -finstrument-functions -I ../lib -L ../lib -lcdefer

一切OK后，先将libcdefer.so放在main同级目录下，执行main即可。

$> ./main

a = [13], s = [hello]

具体代码已经传至[这里](http://code.google.com/p/bigwhite-code)(trunk/cdefer)，需要的童鞋可自行下载。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我也做了个C++版本的defer:http://my.oschina.net/chai2010/blog/117920

相当于给自己做了个ROP