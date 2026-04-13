---
title: 一个有关Golang变量作用域的坑
url: https://tonybai.com/2015/01/13/a-hole-about-variable-scope-in-golang/
published: '2015-01-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一个有关Golang变量作用域的坑

临近下班前编写和调试一段[Golang](http://tonybai.com/tag/golang)代码，但运行结果始终与期望不符，怪异的很，下班前依旧无果。代码Demo如下：

//testpointer.go

package main

import (

"fmt"

)

var p *int

func foo() (*int, error) {

var i int = 5

return &i, nil

}

func bar() {

//use p

fmt.Println(*p)

}

func main() {

p, err := foo()

if err != nil {

fmt.Println(err)

return

}

bar()

fmt.Println(*p)

}

这段代码原意是定义一个包内全局变量p，用foo()的返回值对p进行初始化，在bar中使用p。预期结果：bar()和main()中均输出5。但编译执行后的结果却是：

$go run testpointer.go

panic: runtime error: invalid memory address or nil pointer dereference

[signal 0xb code=0x1 addr=0x0 pc=0x20d1]

goroutine 1 [running]:

main.bar()

/Users/tony/Test/Go/testpointer.go:17 +0xd1

main.main()

/Users/tony/Test/Go/testpointer.go:26 +0x11c

goroutine 2 [runnable]:

runtime.forcegchelper()

/usr/local/go/src/runtime/proc.go:90

runtime.goexit()

/usr/local/go/src/runtime/asm_amd64.s:2232 +0×1

goroutine 3 [runnable]:

runtime.bgsweep()

/usr/local/go/src/runtime/mgc0.go:82

runtime.goexit()

/usr/local/go/src/runtime/asm_amd64.s:2232 +0×1

goroutine 4 [runnable]:

runtime.runfinq()

/usr/local/go/src/runtime/malloc.go:712

runtime.goexit()

/usr/local/go/src/runtime/asm_amd64.s:2232 +0×1

exit status 2

晚饭后，继续调试这段代码。怎么还crash了！代码看似半点问题都没有，难道是Go编译器的问题，我用的可是最新的[1.4](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)，切换回1.3.3，问题依旧啊。看来还是代码的问题，但问题在哪里呢？加上些打印语句再看看：

func bar() {

//use p

fmt.Printf("%p, %T\n", p, p) //output: 0x14dc80, 0×0, *int

fmt.Println(*p) //Crash!!!

}

func main() {

fmt.Printf("%p, %T\n", p, p) //output: 0x14dc80, 0×0, *int

p, err := foo()

if err != nil {

fmt.Println(err)

return

}

fmt.Printf("%p, %T\n", p, p) //output: 0x2081c6020, 0x20818a258, *int

bar()

fmt.Println(*p)

}

通过打印输出，发现从foo函数中返回的p(0x2081c6020)与全局变量的p(0x14dc80)居然不是一个地址，也就是说不是一个变量。而且 从bar()中的调试输出来看，全局变量p在foo函数返回时并未被赋值为foo中变量i的地址，而依然是一个nil值，从而导致程序Crash。

好了，废话不说了，该是揭晓真相的时候了。问题就在于":="。在main这个作用域中，我们使用了

p, err := foo()

最初的理解是golang会定义新变量err，p为初始定义的那个全局变量。但实际情况是，对于使用:=定义的变量，如果新变量p与那个同名已定义变量 (这里就是那个全局变量p)不在一个作用域中时，那么golang会新定义这个变量p，遮盖住全局变量p，这就是导致这个问题的真凶。

我们将main函数改为：

func main() {

var err error

p, err = foo()

if err != nil {

fmt.Println(err)

return

}

bar()

}

则执行结果就完全符合预期了。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

这个是很容易错

foo 中的i不是局部变量？这样传地址出来没问题吗？

这里是go语言啊，不是c语言，呵呵。

Go 语言就可以返回局部变量的地址了么？根据是什么？

go的语法规定啊。go语言是支持垃圾回收的语言，gc根据上下文分配局部变量的地址，如果变量地址被返回，那gc就在heap上分配这个变量，而不是传统意义的stack上。实际上go变量也许都是在heap上分配的。

啊，谢谢回复。这个我已经在邮件列表里问过了，原来出处在 FAQ。确实不能再以 C 的思维来考虑新语言。

谢谢解释。第一反应也以为是stack被销毁造成的。

哈哈，我的第一反应是golang的gc不会出这么低级的bug把，还好确实不是gc的问题。

我也在这上犯过几次错，吃一堑长一智，不会再犯了。~~~

文章不错,评论的也不错

func foo() (*int, error) { var i int = 5 return &i, nil}中的i是栈中的局部变量，函数执行完变量就出栈了，返回这个地址难度不是问题的真凶

我也遇到了同样的问题，搞到晚上11点多才找到问题的症结，早看到博主的文章就好了。

只有自己趟过一遍印象才更为深刻^_^

被坑的都来一下

这个确实容易疏忽啊

被坑+1

+1

本质是对:=没理解造成的。 := 左边是新创建一个 变量

坑了几次 才明白。。。从python转过来的很容易犯这错。。。

学习了。不过现在 Goland IDE 中会很轻易识别出

嗯，Go的相关tool能力日益增强！好事！

在函数中， := 简洁赋值语句在明确类型的地方，可以用于替代 var 定义！

上面这句话是对:=操作符的中文翻译。我觉得说的已经很清楚了，main中的p，就明显是个局部变量，bar中的p明显是全局变量，他们的地址肯定是不一样的，大多数语言里面也都是这样的。