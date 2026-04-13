---
title: 理解Golang语句中的求值顺序
url: https://tonybai.com/2015/08/27/understanding-go-statements-evaluating-order/
published: '2015-08-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 理解Golang语句中的求值顺序

[Golang](http://tonybai.com/tag/go)在变量声明、初始化以及赋值语句上照比C语言有了许多改进：

**a) 支持在同一行声明多个变量**

var a, b, c int

**b) 支持在同一行初始化多个变量（不同类型也可以）**

var a, b, c = 5, "hello", 3.45

a, b, c := 5, "hello", 3.45 (short variable declaration)

**c) 支持在同一行对多个变量进行赋值（在声明后且不同类型也可以）**

a, b, c = 5, "hello", 3.45

这种语法糖我们是笑纳的，毕竟人生苦短，少写一行是一行啊^_^。

但这种语法糖却给我们带来了一些令人困惑的问题！比如下面这个就是Rob Pike在一个talk中slide(Go Course Day2)中的一个问题：

n0, n1 = n0 + n1, n0

or：

n0, n1 = op(n0,n1), n0

n0, n1的值在上述语句执行完毕后到底为多少呢？

显然这个问题涉及到Go语言的语句求值顺序(evaluation order)。求值序在任何一门编程语言中都是比较难缠的，很多情形下，语言规范给出的答案都是“undefined（未定义）” or "not specified" or “依赖实现”，尤其是对于哪些模棱两可的写法，就如Rob Pike给出的那个问题。

我们要想搞清楚Go中的求值顺序，我们需要求助于Go language specification，Go spec与Go发行版一起发布，你可以启动一个godoc web server(godoc -http=:6060，然后访问localhost:6060/ref/spec)查看go language specification。Go language specification专门有一个小节/ref/spec#Order_of_evaluation对求值顺序做了说明。

在Go specs中，有这样三点陈述：

1、变量声明(variable declaration)中的初始化表达式(initialization expressions)的求值顺序(evaluation order)由初始化依赖(initialization dependencies)决定；但对于初始化表达式内部的操作数的求值需要按照2中的顺序：从左到右；

2、在非变量初始化语句中，对表达式、赋值语句或返回语句中的操作数进行求值时，操作数中包含的函数(function)调用、方法(method)调用和通信操作(主要针对channel)将按语法从左到右的顺序求值。

3、赋值语句求值分为两个阶段，第一阶段是等号左边的index expressions、pointer indirections和等号右边的表达式中的操作数的求值顺序按照2中从左到右的顺序；第二阶段按从左到右的顺序对变量赋值。

下面我们就分别理解一下这三点。

**一、变量声明中初始化表达式的求值顺序**

带初始化表达式的变量声明的形式如下：

var a, b, c = expr1, expr2, expr3 //包级别或函数/方法内部

or

a, b, c := expr1, expr2, expr3 //仅函数/方法内部

根据lang specs说明，求值顺序是由初始化依赖（initialization dependencies）规则决定的。那初始化依赖规则是什么呢？在Golang specs中也有专门章节说明：ref/spec#Package_initialization。

初始化依赖规则总结一下，大致有如下几条：

1、包中，包级别变量的初始化顺序按照声明先后的顺序，但如果某个变量(比如a)的初始化表达式中依赖其他变量(比如b)，那么变量a的初始化顺序在变量b后面。

2、对于未初始化的，且不含有对应初始化表达式或其初始化表达式不依赖任何未初始化变量的变量，我们称之为"ready for initialization"变量。初始化就是按照声明顺序重复执行对下一个变量的初始化过程，直到没有"ready for initialization"变量为止。

3、如果初始化过程完毕后依然有变量处于未初始化状态，那程序有语法错误。

4、多个处于不同文件中的变量的声明顺序依赖编译器处理文件的顺序，先处理的文件中的变量的声明顺序先于后处理的文件中的所有变量。

5、依赖分析以包为单位执行，只有位于同一个包中的被依赖的变量、函数、方法才会被考虑。

规则是抽象难懂的，例子更直观易理解，我们看一个golang spec中的例子，并使用上述规则进行分析。实验环境：[go 1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/), amd64,Darwin Kernel Version 13.1.0。

//golang-statements-evaluating-order/example1.go

package main

import "fmt"

var (

a = c + b

b = f()

c = f()

d = 3

)

func f() int {

d++

return d

}

func main() {

fmt.Println(a, b, c, d)

}

我们来分析一下程序执行后的a, b, c, d四个变量的结果值，不过不同的初始化顺序会导致结果值不同，因此分析四个变量的初始化顺序是至关重要的。

变量a, b, c, d的初始化过程如下：

1、根据规则，初始化按照变量声明先后顺序进行，因此先来分析变量a，a初始化表达式依赖b 和c；因此变量a的初始化次序排在b、c的后面；

2、按照a的初始化右值表达式，c、b在右值表达式中的出现顺序是c先于b；

3、c是否是一个ready for initialization变量呢？我们看到c依赖f这个函数，而f这个函数则依赖变量d的初始化，因此d排在c之前；

4、我们来看变量d，"d = 3"，d未初始化且不含有初始化表达式，因此d是一个ready for initialization变量，我们可以从d开始初始化了。至此四个变量的初始化顺序排定 d -> c -> b -> a；(这块儿与spec中分析有差异，但从运行结果来看，应该是这个顺序;关于这个spec的issue参见[#12369](https://github.com/golang/go/issues/12369))

5、d初始化为3，此时已初始化变量集合[d=3]；

6、接着初始化c：c = f()，因此c = 4（此时d=4），此时已初始化变量集合[c=4,d=4]；

7、接下来轮到b：b = f()，因此b = 5 （此时d = 5)，此时已初始化变量集合[b=5,c=4,d=5]；

8、最后初始化a： a = c + b，在已初始化变量集合中我们可以找到b和c，因此a= 9，这样四个变量到此均已初始化；

9、经过分析：程序执行的结果应该是9，5，4，5。

我们来执行一下这个程序，验证一下我们的分析结果是否正确：

$go run example1.go

9 5 4 5

我们再来看一个例子，也是golang specs中的例子，我们稍作改造，并把它设定为example2：

//golang-statements-evaluating-order/example2.go

package main

import "fmt"

**var a, b, c = f() + v(), g(), sqr(u()) + v()**

func f() int {

fmt.Println("calling f")

return c

}

func g() int {

fmt.Println("calling g")

return a

}

func sqr(x int) int {

fmt.Println("calling sqr")

return x * x

}

func v() int {

fmt.Println("calling v")

return 1

}

func u() int {

fmt.Println("calling u")

return 2

}

func main() {

fmt.Println(a, b, c)

}

同样根据变量初始化依赖规则对这个例子进行分析：

1、按照变量声明顺序，先初始化a：a= f() + v()，f()依赖变量c；v不依赖任何变量，因此变量c的初始化顺序应该在a变量前：c -> a。

2、分析c：c = sqr(u()) + v()；u、sqr、v三个函数不依赖任何变量，因此c处于ready for initialization，于是对c进行初始化，函数执行顺序(从左到右)为：u() -> sqr() -> v(); 此时已初始化变量集合：[c = 5]；

3、回到a：a = f() + v()，c初始化后，a也处理ready for initialization，于是对a初始化，函数执行顺序为：f() -> v()，此时已初始化变量集合：[c=5, a= 6]；

4、按照变量声明次序，接下来轮到变量b：b= g()，而g()依赖a，a已经初始化完毕了，因此b也是ready for initialization，于是对b初始化，函数执行次序为：g()，至此已初始化变量集合：[c=5, a=6, b=6]。

5、经过分析：程序执行的结果应该是6，6，5。

我们来执行一下这个程序，验证一下我们的分析结果是否正确：

$go run example2.go

calling u

calling sqr

calling v

calling f

calling v

calling g

6 6 5

**二、非变量初始化语句中的求值顺序**

前面提到过：在非变量初始化语句中，对表达式、赋值语句或返回语句中的操作数进行求值时，操作数中包含的函数(function)调用、方法(method)调用和通信操作(主要针对channel)将按语法**从左到右的顺序求值**。

我们同样来看一个例子：example3.go。

//golang-statements-evaluating-order/example3.go

package main

import "fmt"

func f() int {

fmt.Println("calling f")

return 1

}

func g(a, b, c int) int {

fmt.Println("calling g")

return 2

}

func h() int {

fmt.Println("calling h")

return 3

}

func i() int {

fmt.Println("calling i")

return 1

}

func j() int {

fmt.Println("calling j")

return 1

}

func k() bool {

fmt.Println("calling k")

return true

}

func main() {

var y = []int{11, 12, 13}

var x = []int{21, 22, 23}

var c chan int = make(chan int)

go func() {

c <- 1

}()

**y[f()], _ = g(h(), i()+x[j()], <-c), k()**

fmt.Println(y)

}

y[f()], _ = g(h(), i()+x[j()], <-c), k() 这行语句是赋值语句，但赋值语句的操作数中包含函数调用、channel操作，按照规则，这些函数调用、channel操作按从左到右顺序估值。

1、按照从左到右顺序，第一个是y[f()]中的f()；

2、接下来是g()，g()的参数列表依然是一个赋值操作，因此其涉及到的函数调用顺序为h()， i()，j()，<-c，因此实际上的顺序为h() –> i()–> j() –> c操作 -> g()；

3、最后是k(),因此完整的调用顺序是：f()-> h() –> i()–> j() –> c操作 -> g() –> k()。

实际运行情况如下：

$go run example3.go

calling f

calling h

calling i

calling j

calling g

calling k

[11 2 13]

三、赋值语句的求值顺序

我们再回到前面Rob Pike那个问题：

n0, n1 = n0 + n1, n0

or：

n0, n1 = op(n0, n1), n0

这是一个赋值语句，根据规则3，我们对等号两端的表达式的操作数采用从左到右的求值顺序。

我们假定初值：

n0, n1 = 1, 2

1、第一阶段：等号两端表达式求值，上述问题中，只有右端有n0+n1和n0两个表达式，但表达式的操作数(n0，n1)都是初始化过后的了，因此直接将值带入，得到求值结果。求值后，语句可以看成：n0, n1 = 3, 1；

2、第二阶段：赋值。n0 =3， n1 = 1

//golang-statements-evaluating-order/example4.go

package main

import "fmt"

func example1() {

n0, n1 := 1, 2

n0, n1 = n0+n1, n0

fmt.Println(n0, n1)

}

func op(a, b int) int {

return a + b

}

func example2() {

n0, n1 := 1, 2

n0, n1 = op(n0, n1), n0

fmt.Println(n0, n1)

}

func main() {

example1()

example2()

}

$go run example4.go

3 1

3 1

**四、小结**

虽说理解了规则，但实际工作中我们还是尽量不要写出像：**"var a, b, c = f() + v(), g(), sqr(u()) + v()"**这样复杂、难以让人理解的语句。必要的话，拆分成多行就好了，还可以增加些代码量（如果你的公司是以代码量为评价绩效指标之一的），得饶人处且饶人啊，烧脑的语句还是尽量避免为好。

以上实验代码在[这里](https://github.com/bigwhite/experiments/tree/master/golang-statements-evaluating-order)可以下载到。

**五、参考资料**

[The Go Programming Language Specification](https://golang.org/ref/spec) (Version of August 5, 2015)

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

[b=4,c=5,d=5] 与 结果应该是9，5，4，5 不是矛盾吗

你说的没错，似乎golang doc中的初始化顺序也有误，应该是d -> c -> b->a，这样才能与运行结果一致。post已经修改：b，c应该按照表达式从左到右的顺序初始化，应该是c 先于b。