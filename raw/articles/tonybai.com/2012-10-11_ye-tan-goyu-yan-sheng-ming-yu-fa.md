---
title: 也谈Go语言声明语法
url: https://tonybai.com/2012/10/11/understanding-go-declaration-syntax/
published: '2012-10-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈Go语言声明语法

一直在从事C语言服务端应用开发，对C的变量声明语法早已烂熟于胸，同时也深知复杂的C变量声明十分晦涩难解。记得若干年前还特意花了一些时间研究理解复 杂C变量声明的方法，记忆中这些方法包括：《C专家编程》中提到的“[优先级](http://tonybai.com/2006/03/26/understand-priority-rule-for-parse-c-declaration/)”规则、[right-left规则](http://tonybai.com/2005/08/09/an-explanation-of-complex-c-declaration/)以及[顺时针/螺旋形规则](http://c-faq.com/decl/spiral.anderson.html)等，幸运地是我们日常 开发中少有使用极为复杂的变量声明(如void (*signal (int signo, void (*func) (int)))(int);)，但C语言中这一难点却是事实存在的。

对于我这样的习惯了C变量声明语法的程序员来说，[Go](http://golang.org)的变量声明语法显得极端另类，完全与C语言反其道而行之，心中不由产生一丝厌恶。但随着对Go学习和 使用的深入，我逐渐发现Go的这种声明语法在不经意间解决了复杂声明的理解问题，你无需学习什么"优先级"规则，也无需理会什么“right-left” 规则，你只需按从左到右的顺序阅读代码，再复杂的变量声明也可以很轻易地理解。

Go语言为何要采用这种倒序语法呢？Go的设计者Rob Pike的一篇介绍[Go声明语法](http://blog.golang.org/2010/07/gos-declaration-syntax.html)的文章给出了答案，其中谈到了Go声明语法的设计考量。Go的设计者从C体系之外的语言获得启发：将变量名放在签名，类型说明放在后 面。这样更接近于自然语言，例如：

x: int

p: pointer to int

a: array[3] of int

b: slice of int

在此基础上，Go的设计者用*、[]等符号替换掉上面的冒号和部分关键字使得声明变得短小，也就形成了Go的声明语法：

var x int

var p *int

var a [3]int

var b []int

我们只需从左向右的顺序阅读代码，即可清晰的理解声明的含义，而不需要像C声明语法那样左右符号都要兼顾，螺旋理解。这里面的*、[n]和[]的含义如下：

****some_type*：读作 pointer to some_type

*[n]**some_type*： 读作 array[n] of some_type

*[]**some_type*： 读作 slice of some_type

下面我们通过Go与C的对比来进一步理解Go的声明语法。

**简单变量声明**

*C * *Golang*

int x; <–> var x int //x has the type int

float x; <–> var x float64 //x has the type float64

char c; <–> var c byte //x has the type byte

**指针变量声明**

*C Golang*

int *x; <–> var x *int //x is a pointer to int

int **p; <–> var p **int //p is a pointer to pointer to int

**数组/切片变量声明**

*C Golang*

int a[5]; <--> var a [5]int //a is an array[5] of int

int a[5][3]; <--> var a [5][3]int //a is an array[5] of array[3] of int

var s []int //s is a slice of int(C语言中无slice类型)

**函数类型变量声明**

*C Golang*

int (*x)(int, int) 类似于 var x func(int, int) int // x has the type "func(int, int) int"


Go中函数为first-class类型，其类型的变量等同于C中的函数指针。

**复合声明****(复杂声明)**

*C Golang*

int *x[5]; <--> var x [5]*int //x is an array[5] of pointer to int

int (*x[5])(int, int) 类似于 var x [5]func(int, int) int // x is an array[5] of "func(int, int) int"

var f func(func(int,int) int, int) func(int, int) int //f has the type "func(func(int,int) int, int) func(int, int) int"，这是一个函数类型变量，这个函数类型接收三个参数(其中一个参数是func(int, int)函数类型)，并返回另外一个函数类型(func(int, int) int)。

void (*signal (int signo, void (*Afunc) (int))) 类似于 var signal func(signo int, Afunc func(int))

有了上面的例子,signal就无需再作解释了，Go的声明语法可以让我们可以很容易的理解复杂的变量声明。但从可读性角度来看较长的声明依旧不利于代码理解。因此我们还是应该通过type定义一些新类型的方式尽量缩短变量声明的长度，例如：

type Handler func(int)

type SignalHandler func(signo int, handler Handler)

var signal SignalHandler

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论