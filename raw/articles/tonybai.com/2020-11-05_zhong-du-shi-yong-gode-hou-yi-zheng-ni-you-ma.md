---
title: 重度使用Go的“后遗症“，你有吗？
url: https://tonybai.com/2020/11/05/the-sequela-after-being-used-to-writting-code-in-go/
published: '2020-11-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 重度使用Go的“后遗症“，你有吗？

![img{512x368}](../../assets/3a7e8874f77ec9ca.png)


有一种未经证实的说法：**Go诞生于C++程序的漫长构建过程中**。如果C++编译很快，那么Robert Griesemer、Rob Pike和Ken Thompson这三位大佬也没有闲暇时间[一起喝着咖啡并决定是时候设计一门新语言](https://www.imooc.com/read/87/article/2320)了。的确，[Go语言诞生](https://www.imooc.com/read/87/article/2320)后，其简洁的语法、极速地构建、新颖的并发结构、体验优良的工具链以及完成度不低的标准库吸引了很多C/C++程序员转型成为Gopher并开始重度使用Go，比如鄙人^_^。如果能一直使用Go总也是不错的，但偶尔因项目需要可能还会写一些C/C++代码，这时候很多Gopher发现自己在长期重度使用Go之后出现了一些“后遗症”！这里我们就来细数一下都有哪些“后遗症”，各位Gopher小伙伴们也自我评估一下，这些“后遗症”是否也发生在你的身上^_^。

### 1. 声明变量时类型与变量名的顺序总写反

Go语言是C家族编程语言的一个分支，和C/C++一样，Go也是静态编译型语言，这就要求在使用任何变量之前需要先[声明这个变量](https://tip.golang.org/ref/spec#Variable_declarations)，无论使用常规声明方法还是[短声明形式](https://tip.golang.org/ref/spec#Short_variable_declarations)。

但Go采用的变量声明语法颇似Pascal：**变量名在前，变量类型在后**，这与C/C++恰好相反：

```
Go:
var a, b int
var p, q *int
vs.
C/C++：
int a, b;
int *p, *q;
```


这样，gopher在长期使用Go编写代码后，一旦回归写C/C++代码，遇到的第一个问题就是经常在声明的时候将变量名与类型写反^_^。还好C/C++编译器会发现并告知我们这个问题，并不会给程序带来实质性的伤害。

-
发病指数：3

-
危害指数：1


### 2. 经常在函数中使用“短声明”形式声明变量

短声明不是Go语言独创的语法。短声明的好处正如其名：短小，无需显式提供变量类型，编译器会根据赋值操作符后面的初始化表达式的结果自动为变量赋予适当类型。因此，它成为了Gopher们喜爱和重度使用的语法。但短声明在C/C++中却不是合法的语法元素：

```
int main() {
a := 5; // error: expected expression
printf("a = %d\n", a);
}
```


和上面的问题一样，C/C++编译器会发现并告知我们这个问题，并不会给程序带来实质性的伤害。

-
发病指数：2

-
危害指数：1


### 3. 总是忘记代码行结尾的分号

**Go的正式标准语法是带有分号的**，下面的代码片段才是编译器眼中认为正确的代码形式：

```
package main;
import "fmt";
import _ "database/sql";
type Foo struct {
Name string;
Age int;
};
func main() {
var a, b = 1, 2;
println(a, b);
if a == 1 { fmt.Println("a = 1"); }
}
```


但这种形式显然与我们日常**“惯用”的代码形式**有很大不同，我们日常编写Go代码时**极少手写分号**。Go设计者当初为了简化代码编写，提高代码可读性，选择了由编译器在词法分析阶段自动在适当位置插入分号的技术路线，并在Go语言规范中描述了分号的插入规则：

```
1. 在Go中，除去注释，如果一个代码行的最后一个token为下列情况时，则编译器会将一个分号自动插入在此字段后：
- 一个标识符；
- 一个整数、浮点数、实数虚部、rune(码点)或者字符串字面量；
- 关键字之一：break、continue、fallthrough和return；
- 自增运算符++、自减运算符--、右括号)、]或}。
2. 为支持在一个代码行中放置复杂语句，分号可能被插入在右小括号)或者右大括号}之前。
```


被Go编译器**惯坏了**的Gopher们一旦回到编写C/C++代码，遗忘代码行尾的分号的“后遗症”行为就见怪不怪了。

-
发病指数：5

-
危害指数：2


### 4. 遇到在其他头文件中定义的头母小写的函数时总以为不能直接使用

在Go中，头母大写的包级变量、常量、类型、函数、方法都是导出的，即对外部包可见。反之，头母小写的则为包私有的，仅在包内使用。一旦习惯了这样的规则，在切换到其他语言中，就会产生“心理后遗症”：遇到在其他头文件中定义的头母小写的函数时总以为不能直接使用。

-
发病指数：3

-
危害指数：2


### 5. 写条件分支语句、选择分支语句和循环语句时，总忘记给条件加上括号

同样是出于简化代码，增加可读性的考虑，Go设计者最初就取消掉了条件分支语句(if)、选择分支语句(switch)和循环语句(for)中条件表达式外围的小括号：

```
func f() int {
return 5
}
func main() {
a := 1
if a == 1 { // 无需小括号包裹条件表达式
fmt.Println(a)
}
switch b := f(); b { // 无需小括号包裹条件表达式
case 4:
fmt.Println("b = 4")
case 5:
fmt.Println("b = 5")
default:
fmt.Println("b = n/a")
}
for i := 1; i < 10; i++ { // 无需小括号包裹循环语句的循环表达式
a += i
}
fmt.Println(a)
}
```


这恰与C/C++“背道而驰”，于是我们经常看到在编写C/C++的gopher为大量的如下编译器错误而苦恼：

```
int main()
{
int a = 1;
if a == 1 { // error: expected '(' after 'if'
printf("a = 1\n");
}
int i = 0;
for i = 1; i < 10; i++ { // error: expected '(' after 'for'
a += i;
}
}
```


-
发病指数：4

-
危害指数：2


### 6. 总是忘记在switch case语句中添加break

C/C++的选择分支语句有一个陷阱，那就是case语句中如果没有显式加入break语句，那么代码将向下自动掉落执行。Go在最初设计时填了这个“坑”，重新规定了swtich case语义，默认不自动掉落(fallthrough)，除非开发者显式使用fallthrough关键字。

适应了Go的switch case语句的语义后，再回来写C/C++代码就会存在潜在的“风险”：

```
int main()
{
int a = 1;
switch(a) {
case 1:printf("a = 1\n");
case 2:printf("a = 2\n");
case 3:printf("a = 3\n");
default:printf("a = ?\n");
}
}
```


这段代码按go语义编写switch case，编译运行后得到的结果如下：

```
a = 1
a = 2
a = 3
a = ?
```


我们看到代码首先匹配到了 case1的情况，然后一路自动掉落到default case。这个“后遗症”存在很大危害，因为这样编写的代码在C/C++编译器眼中是完全合法的，但所代表的语义却完全不是开发人员想要的。这样的程序一旦流入到生产环境，其缺陷可能会引发生产故障。

-
发病指数：3

-
危害指数：4


对于这样的问题，一些C/C++ lint工具可以将其检测出来，因此建议写C/C++代码的Gopher在提交代码前使用lint工具对代码做一下检查。

### 参考资料

-
https://go101.org/article/line-break-rules.html

-
https://tip.golang.org/ref/spec#Semicolons

-
https://medium.com/golangspec/automatic-semicolon-insertion-in-go-1990338f2649


只有写书者，才能体会到写者的艰辛！[Go专栏：《改善Go语言编程质量的50个有效实践》](https://www.imooc.com/read/87)也是我努力了一年多才打磨雕琢出来的心血之作。自从上线后，收到大家的热烈关注和好评！现在恰逢双11慕课大促，欢迎有意愿在Go这条技术路线上进阶的朋友们订阅，在学习过程中欢迎随时反馈和交流！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中！欢迎小伙伴们学习支持！双十一慕课网优惠空前！别错过机会哦！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

补充一个 switch 的小坑， = =：

“`go

package main

import (

“fmt”

)

func main() {

i := 0

switch i {

case 0:

case 1:

fmt.Println(“fallthrough”)

}

}

“`

不是很懂你的意思^_^，我没看到代码中有啥坑啊。要不你再详细说说。

这不是写惯了Go，是写惯了其它语言

很少有程序员只会一门编程语言。况且很多资深go开发者都来自于c,c++。对于c、c++转化为go，再偶尔写c/c++代码时，多数会患上文中的“后遗症”:)