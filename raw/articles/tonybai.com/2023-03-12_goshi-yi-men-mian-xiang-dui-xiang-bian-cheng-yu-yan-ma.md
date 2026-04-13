---
title: Go是一门面向对象编程语言吗
url: https://tonybai.com/2023/03/12/is-go-object-oriented/
published: '2023-03-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go是一门面向对象编程语言吗

![](../../assets/11099a70cefc93d9.png)


[本文永久链接](https://tonybai.com/2023/03/12/is-go-object-oriented) – https://tonybai.com/2023/03/12/is-go-object-oriented

[Go语言已经开源13年了](https://tonybai.com/2022/11/11/go-opensource-13-years/)，在近期[TIOBE](https://www.tiobe.com/tiobe-index/)发布的2023年3月份的编程语言排行榜中，Go再次冲入前十，相较于Go在[2022年底的排名](https://tonybai.com/2022/12/29/the-2022-review-of-go-programming-language)提升了2个位次：

![](../../assets/bf460b062ebe3820.png)


[《Go语言第一课》专栏](http://gk.link/a/10AVZ)中关于Go在这两年开始飞起的“预言”也正在逐步成为现实^_^，大家学习Go的热情也在快速提升， [《Go语言第一课》专栏](http://gk.link/a/10AVZ)的学习的人数年后也快速增加，快突破2w了。

很多专栏的订阅者都是第一次接触Go，他们中的很多是来自像Java, Ruby这样的OO(面向对象)语言阵营的，他们学习Go之后的第一个问题便是：**Go是一门OO语言吗**？在这篇博文中，我们就来探讨一下。

## 一. 溯源

在公认的Go语言“圣经”[《Go程序设计语言》](http://www.gopl.io)一书中，有这样一幅Go语言与其主要的先祖编程语言的亲缘关系图：

![](../../assets/f5ca4154a869772e.png)


从图中我们可以清晰看到Go语言的“继承脉络”：

- 从
[C语言](https://tonybai.com/tag/c)那里借鉴了表达式语法、控制语句、基本数据类型、值参数传递、指针等； - 从
[Oberon-2语言](https://cseweb.ucsd.edu/~wgg/CSE131B/oberon2.htm)那里借鉴了package、包导入和声明的语法，而Object Oberon提供了方法声明的语法。 - 从
[Alef语言](http://doc.cat-v.org/plan_9/2nd_edition/papers/alef/ref)以及[Newsqueak语言](https://newspeaklanguage.org)中借鉴了基于[CSP](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2008-09/tony-hoare/csp.html)的并发语法。

我们看到，从Go先祖溯源的情况来看，Go并没有从纯面向对象语言比如Simula、[SmallTalk](http://en.wikipedia.org/wiki/Smalltalk)等那里取经。

Go诞生于2007年，开源于2009年，那正是面向对象语言和OO范式大行其道的时期。不过Go设计者们觉得经典OO的继承体系对程序设计与扩展似乎并无太多好处，还带来了较多的限制，因此在正式版本中并没有支持经典意义上的OO语法，即基于类和对象实现的封装、继承和多态这三大OO主流特性。

但这是否说明Go不是一门OO语言呢？也不是！ 带有面向对象机制的[Object Oberon](http://www.projectoberon.net/)也是Go的先祖语言之一，虽然Object Oberon的OO语法又与我们今天常见的语法有较大差异。

就此问题，我还特意咨询了[ChatGPT](https://chat.openai.com/chat)^_^，得到的答复如下：

![](../../assets/6e10a622e556fb4a.png)


ChatGPT认为：Go支持面向对象，提供了对面向对象范式基本概念的支持，但支持的手段却并不是类与对象。

那么针对这个问题Go官方是否有回应呢？有的，我们来看一下。

## 二. 官方声音

```
Is Go an object-oriented language?
Yes and no. Although Go has types and methods and allows an object-oriented style of programming, there is no type hierarchy. The concept of “interface” in Go provides a different approach that we believe is easy to use and in some ways more general. There are also ways to embed types in other types to provide something analogous—but not identical—to subclassing. Moreover, methods in Go are more general than in C++ or Java: they can be defined for any sort of data, even built-in types such as plain, “unboxed” integers. They are not restricted to structs (classes).
Also, the lack of a type hierarchy makes “objects” in Go feel much more lightweight than in languages such as C++ or Java.
```


粗略翻译过来就是：

```
Go是一种面向对象的语言吗？
是，也不是。虽然Go有类型和方法，并且允许面向对象的编程风格，但却没有类型层次。Go中的“接口”概念提供了一种不同的OO实现方案，我们认为这种方案更易于使用，而且在某些方面更加通用。还有一些可以将类型嵌入到其他类型中以提供类似子类但又不等同于子类的机制。此外，Go中的方法比C++或Java中的方法更通用：Go可以为任何数据类型定义方法，甚至是内置类型，如普通的、“未装箱的”整数。Go的方法并不局限于结构体（类）。
此外，由于去掉了类型层次，Go中的“对象”比C++或Java等语言更轻巧。
```


“是，也不是”！我们看到Go官方给出了一个“对两方都无害”的中庸的回答。那么Go社区是怎么认为的呢？我们来看看Go社区的一些典型代表的观点。

## 三. 社区声音

[Jaana Dogan](https://rakyll.org/)和[Steve Francia](https://spf13.com/)都是前Go核心团队成员，他们在加入Go团队之前对“Go是否是OO语言”这一问题也都有自己的观点论述。

Jaana Dogan在[《The Go type system for newcomers》](https://rakyll.org/typesystem/)一文中给出的观点是：**Go is considered as an object-oriented language even though it lacks type hierarchy**，即“Go被认为是一种面向对象的语言，即使它缺少类型层次结构”。

而更早一些的是Steve Francia在2014年发表的文章[《Is Go an Object Oriented language?》](https://spf13.com/p/is-go-an-object-oriented-language/)中的结论观点：**Go，没有对象或继承的面向对象编程**，也可称为“无对象”的OO编程模型。

两者表达的遣词不同，但含义却异曲同工，即**Go支持面向对象编程，但却不是通过提供经典的类、对象以及类型层次来实现的**。

那么Go究竟是以何种方式实现对OOP的支持的呢？我们继续看！

## 四. Go的“无对象”OO编程

经典OO的三大特性是封装、继承与多态，这里我们看看Go中是如何对应的。

### 1. 封装

封装就是把数据以及操作数据的方法“打包”到一个抽象数据类型中，这个类型封装隐藏了实现的细节，所有数据仅能通过导出的方法来访问和操作。 这个抽象数据类型的实例被称为**对象**。经典OO语言，如Java、C++等都是通过类(class)来表达封装的概念，通过类的实例来映射对象的。熟悉Java的童鞋一定记得[《Java编程思想》](https://book.douban.com/subject/2130190/)一书的第二章的标题：“一切都是对象”。在Java中所有属性、方法都定义在一个个的class中。

Go语言没有class，那么封装的概念又是如何体现的呢？来自OO语言的初学者进入Go世界后，都喜欢“对号入座”，即Go中什么语法元素与class最接近！于是他们找到了struct类型。

Go中的struct类型中提供了对真实世界聚合抽象的能力，struct的定义中可以包含一组字段(field)，如果从OO角度来看，你也可以将这些字段视为属性，同时，我们也可以为struct类型定义方法(method)，下面例子中我们定义了一个名为Point的struct类型，它拥有一个导出方法Length：

```
type Point struct {
x, y float64
}
func (p Point) Length() float64 {
return math.Sqrt(p.x * p.x + p.y * p.y)
}
```


我们看到，从语法形式上来看，与经典OO声明类的方法不同，Go方法声明并不需要放在声明struct类型的大括号中。Length方法与Point类型建立联系的纽带是一个被称为**receiver参数**的语法元素。

那么，struct是否就是对应经典OO中的类呢? 是，也不是！从数据聚合抽象来看，似乎是这样, struct类型可以拥有多个异构类型的、代表不同抽象能力的字段(比如整数类型int可以用来抽象一个真实世界物体的长度，string类型字段可以用来抽象真实世界物体的名字等)。

但从拥有方法的角度，不仅是struct类型，**Go中除了内置类型的所有其他具名类型都可以拥有自己的方法**，哪怕是一个底层类型为int的新类型MyInt：

```
type MyInt int
func(a MyInt)Add(b int) MyInt {
return a + MyInt(b)
}
```


### 2. 继承

就像前面说的，Go设计者在Go诞生伊始就重新评估了对经典OO的语法概念的支持，最终放弃了对诸如类、对象以及类继承层次体系的支持。也就是说：**在Go中体现封装概念的类型之间都是“路人”，没有亲爹和儿子的关系的“牵绊”**。

谈到OO中的继承，大家更多想到的是子类继承了父类的属性与方法实现。Go虽然没有像Java extends关键字那样的显式继承语法，但Go也另辟蹊径地对“继承”提供了支持。这种支持方式就是类型嵌入(type embedding)，看一个例子：

```
type P struct {
A int
b string
}
func (P) M1() {
}
func (P) M2() {
}
type Q struct {
c [5]int
D float64
}
func (Q) M3() {
}
func (Q) M4() {
}
type T struct {
P
Q
E int
}
func main() {
var t T
t.M1()
t.M2()
t.M3()
t.M4()
println(t.A, t.D, t.E)
}
```


我们看到类型T通过嵌入P、Q两个类型，“继承”了P、Q的导出方法(M1~M4)和导出字段(A、D)。

关于类型嵌入的具体语法说明，大家可以温习一下

[《十分钟入门Go语言》]或[《Go语言第一课》专栏]。

不过实际Go中的这种“继承”机制并非经典OO中的继承，其外围类型(T)与嵌入的类型(P、Q)之间没有任何“亲缘”关系。P、Q的导出字段和导出方法只是被提升为T的字段和方法罢了，**其本质是一种组合**，是组合中的代理（delegate）模式的一种实现。T只是一个代理（delegate），对外它提供了它可以代理的所有方法，如例子中的M1~M4方法。当外界发起对T的M1方法的调用后，T将该调用委派给它内部的P实例来实际执行M1方法。

以经典OO理论话术去理解就是**T与P、Q的关系不是is-a，而是has-a的关系**。

### 3. 多态

经典OO中的多态是尤指**运行时多态**，指的是调用方法时，会根据调用方法的实际对象的类型来调用不同类型的方法实现。

下面是一个C++中典型多态的例子：

```
#include <iostream>
class P {
public:
virtual void M() = 0;
};
class C1: public P {
public:
void M();
};
void C1::M() {
std::cout << "c1.M()\n";
}
class C2: public P {
public:
void M();
};
void C2::M() {
std::cout << "c2.M()\n";
}
int main() {
C1 c1;
C2 c2;
P *p = &c1;
p->M(); // c1.M()
p = &c2;
p->M(); // c2.M()
}
```


这段代码比较清晰，一个父类P和两个子类C1和C2。父类P有一个虚拟成员函数M，两个子类C1和C2分别重写了M成员函数。在main中，我们声明父类P的指针，然后将C1和C2的对象实例分别赋值给p并调用M成员函数，从结果来看，在运行时p实际调用的函数会根据其指向的对象实例的实际类型而分别调用C1和C2的M。

显然，经典OO的多态实现依托的是类型的层次关系。那么对应没有了类型层次体系的Go来说，它又是如何实现多态的呢？**Go使用接口来解锁多态**！

和经典OO语言相比，Go更强调行为聚合与一致性，而非数据。因此Go提供了对类似duck typing的支持，即基于行为集合的类型适配，但相较于ruby等动态语言，Go的静态类型机制还可以保证应用duck typing时的类型安全。

Go的接口类型本质就是一组方法集合(行为集合)，一个类型如果实现了某个接口类型中的所有方法，那么就可以作为动态类型赋值给接口类型。通过该接口类型变量的调用某一方法，实际调用的就是其动态类型的方法实现。看下面例子：

```
type MyInterface interface {
M1()
M2()
M3()
}
type P struct {
}
func (P) M1() {}
func (P) M2() {}
func (P) M3() {}
type Q int
func (Q) M1() {}
func (Q) M2() {}
func (Q) M3() {}
func main() {
var p P
var q Q
var i MyInterface = p
i.M1() // P.M1
i.M2() // P.M2
i.M3() // P.M3
i = q
i.M1() // Q.M1
i.M2() // Q.M2
i.M3() // Q.M3
}
```


Go这种无需类型继承层次体系、低耦合方式的多态实现，是不是用起来更轻量、更容易些呢！

## 五. Gopher的“OO思维”

到这里，来自经典OO语言阵营的小伙伴们是不是已经找到了当初在入门Go语言时“感觉到别扭”的原因了呢！这种“别扭”就在于**Go对于OO支持的方式与经典OO语言的差别**：秉持着经典OO思维的小伙伴一上来就要建立的继承层次体系，但Go没有，也不需要。

要转变为正宗的Gopher的OO思维其实也不难，那就是“**prefer接口，prefer组合，将习惯了的is-a思维改为has-a思维**”。

## 六. 小结

是时候给出一些结论性的观点了：

- Go支持OO，只是用的不是经典OO的语法和带层次的类型体系；
- Go支持OO，只是用起来需要换种思维；
- 在Go中玩转OO的思维方式是：“优先接口、优先组合”。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论