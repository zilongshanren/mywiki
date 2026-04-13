---
title: Go类型系统：有何与众不同
url: https://tonybai.com/2022/12/18/go-type-system/
published: '2022-12-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go类型系统：有何与众不同

![](../../assets/adb423dd84293c41.png)


[本文永久链接](https://tonybai.com/2022/12/18/go-type-system) – https://tonybai.com/2022/12/18/go-type-system

Go是一门强类型的静态编程语言。使用Go编程，我们的每一行代码几乎都离不开**类型**。因此，深入学习Go，我们首先要对Go的类型系统(type system)有一个全面和深入的认知。Go类型系统可以给予我们一个全局整体的视角，以帮助我们更好地学习和理解Go语言中那些具体的与类型相关的内容。

### 一. 什么是类型系统

作为拥有一定Go编程经验的Gopher来说，大家对Go语言中的类型是有一定了解的，比如：Go内置了原生整型类型、浮点类型、复数类型、字符串类型、函数类型，提供了数组、切片、map、struct、channel等复合类型以及代表行为抽象的接口类型。通过Go提供的type关键字，我们还可以自定义类型等等。

那么大家是否想过这样的问题：**为什么会有类型？类型可以带来哪些好处呢**？回顾编程语言的发展史(见下图)，我们发现：**类型是高级语言有别于机器语言与低级语言的一种重要的抽象**。

![](../../assets/2d6abf80592e5632.png)


从机器的视角来看，无论什么类型数据都是0101的二进制数据，但程序员直接用机器语言编码难度非常大且效率极其低下；汇编语言将层次提升到了面向多字节数据的编码，汇编指令的操作数都是固定长度字节的，比如：movb操作的是一个字节，movl操作的是四个字节。汇编指令并不关心真实存储的是什么数据，只是在各个地址之间搬移特定长度的数据。显然汇编的抽象层次依旧不高，直接用汇编写程序依然有很大难度以及较为低效。

高级语言之所以高级，就是因为**它建立了类型这一重要抽象**，类型抽象为开发者屏蔽了机器层面数据的复杂表示。类型下面的复杂的字节和bit操作由高级语言的编译器和运行时协助完成，**开发人员只需面向类型进行编码即可**，也就是说**类型成为了开发者与编译器之间的“操作界面”**。

![](../../assets/fe6e901517b15a39.png)


面向类型编程，开发者就要了解类型的能力、其所代表的抽象的含义以及遵循类型的使用规则/约束。类型决定了你可以在该类型实例中存储的值的范围；类型决定了你可以对该类型进行的操作；类型决定了该类型的变量需要的存储空间；类型决定了与其他类型间建立连接的方法：组合、“继承”还是接口实现等。

那么类型的这些能力、规则与约束是谁赋予的呢？没错，正是**编程语言的类型系统**！

**类型系统是高级语言的核心，它存在于语言规范中，向开发者明确了类型的能力、使用规则与约束；它存在于编译器中，保证开发者对类型的正确合规使用；它也存在于语言运行时里，为类型提供如多态这样的动态能力**。

可以说，高级编程语言用类型系统赋能类型并管理类型。不过，不同语言的类型系统的设计与实现是有较大差别的，那么Go语言的类型系统又有哪些与众不同之处呢？我们接下来就来重点看看Go的类型系统。

### 二. Go的类型系统

下面我们从类型定义、类型推导、类型检查、类型连接等多个方面说明一下Go类型系统具备的能力与不足。

#### 1. 类型定义

大家知道Go支持几乎所有类型，下面是Go spec中的类型分类的列表截图：

![](../../assets/340c473342e615d6.png)


同时，Go还支持使用type关键字定义的自定义类型以及类型别名(type alias)：

```
type CustomType int // 底层类型为原生类型int的自定义类型CustomType
type S struct {
a int
b string
} // 基于struct的自定义类型S
type IntAlias = int // int的类型别名IntAlias
```


注：自定义类型与其底层类型(underlying type)是两个完全不同的类型，而类型别名并未引入新类型，与原类型等价。


不过有两种在其他语言中常见的类型，Go类型系统没有给予支持，一种是union联合类型，在这种类型中，其所有字段共享同一个内存空间：

```
// C代码
// 定义一个名为num的union类型
// 其三个成员m, ch, f共享同一个内存空间
// C编译器会以最大的字段的size为num类型变量分配内存空间
union num {
int m;
char ch;
double f;
};
union num a, b, c; // 声明三个union类型变量
```


另外一种是enum枚举类型，不过enum枚举类型可一定程度上用const(可选加iota)来模拟：

```
// C语法
enum Weekday {
SUNDAY,
MONDAY,
TUESDAY,
WEDNESDAY,
THURSDAY,
FRIDAY,
SATURDAY
};
// Go模拟实现Weekday
type Weekday int
const (
Sunday Weekday = iota
Monday
Tuesday
Wednesday
Thursday
Friday
Saturday
)
```


Go从[1.18版本](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)开始支持[泛型](https://tonybai.com/2022/03/25/intro-generics)，这让Go类型系统具备定义带有类型参数(type parameters)的类型以及函数的能力。

#### 2. 类型推导

Go类型系统支持自动类型推导能力，编译器可以推断出变量或函数的类型，而不需要我们明确指定：

```
var s = "hello" // s是string类型
a := 128 // a是int类型
f := 4.3567 // f是float64类型
```


除了支持普通类型推导，Go还支持泛型的自动类型实参推导，下面是一个来自go spec的例子：

```
func scale[Number ~int64|~float64|~complex128](v []Number, s Number) []Number
var vector []float64
scaledVector := scale(vector, 42)
```


例子中，通过scale调用时传入的实参类型，编译器可以自动推导出scale的类型参数Number的实参为float64。更多关于Go泛型的语法细节，可以参考[《Go语言第一课》](http://gk.link/a/10AVZ)专栏的**泛型篇**。

#### 3. 类型检查

Go是一门强类型静态编程语言，意味着每个变量在使用之前都必须声明其类型。有了类型后，我们就可以按照Go类型系统规定的针对这个类型有效操作对其进行操作。

Go编译器以及运行时会分别在编译期间和运行期间对变量类型作检查，目的是确保操作只用于正确的类型，并且类型系统的规则被程序所遵守，保证类型安全等。

Go是强类型语言，并且没有隐式类型转换，所有类型转换都要以明确意图的显式类型转换来实施，Go编译器会在编译期间对类型转换进行检查，只有底层类型兼容的两个类型才可以实施显式转型：

```
type T1 int
type T2 struct{}
var i int = 5
var t T1
var s T2
t = i // 错误，不是同一类型
t = T1(i) // ok，底层类型兼容
s = T2(t) // 错误，底层类型不兼容
```


除了编译期间的静态检查之外，Go类型系统还支持运行时动态类型检查，比如：检查传给接口变量的类型实例是否实现了该接口；在运行时对数组、切片类型的下标边界进行检查，确保下标不越界，保证内存安全等。

不过Go也提供了绕过类型系统检查的手段，比如unsafe.Pointer以及反射等。

#### 4. 类型连接

Go并非经典OO语言，它的类型虽然可以拥有自己的方法(method)，但Go却没有提供经典OO中的复杂的继承层次结构，没有父类，没有子类，更没有供类型初始化的构造函数。在Go的类型系统中，**类型之间建立连接的方式只有组合**，通过类型嵌入(type embedding)，我们可以实现各类组合，可以嵌入非接口类型，亦可以嵌入接口来定义新组合后的类型。

通过类型组合，我们可以将各种类型连接在一起，共同对外提供聚合后的行为，包括多态能力。Go中标准的多态能力由interface类型实现，方法在运行时被分派，这取决于传给接口类型变量的具体类型。比如下面例子中AnimalQuackInForest中的Quack会依据传入的具体类型实例而分派，先后分派给Duck.Quack、Dog.Quack和Bird.Quack：

```
type QuackableAnimal interface {
Quack()
}
type Duck struct{}
func (Duck) Quack() {
println("duck quack!")
}
type Dog struct{}
func (Dog) Quack() {
println("dog quack!")
}
type Bird struct{}
func (Bird) Quack() {
println("bird quack!")
}
func AnimalQuackInForest(a QuackableAnimal) {
a.Quack()
}
func main() {
animals := []QuackableAnimal{new(Duck), new(Dog), new(Bird)}
for _, animal := range animals {
AnimalQuackInForest(animal)
}
}
```


注：类型与接口之间的实现关系是隐式的，类型无需使用类implements关键字显式告知要实现的interface类型。


Go中的函数是一等公民，函数类型也可展现出一定的运行时多态能力，函数类型实例的最终执行结果取决于运行时传入的函数对象值。

### 三. 小结

Go提供了强大而又有趣的类型系统，不过Go没有提供enum、union类型，也不支持运算符重载(operator overloading)、函数重载、结构化错误处理以及可选/默认函数参数等。这与Go的设计者做出的保持Go简单的决策不无关系。同时类型系统在保证Go这门的语言的安全性方面也是功不可没。

如果你认真对待Go编程，你应该投入时间，了解它的类型系统和它的特殊性，这将是非常值得你花时间的。

### 四. 参考资料

- Type Systems in Software Explained With Examples – https://thevaluable.dev/type-system-software-explained-example/
- The Go type system for newcomers – https://rakyll.org/typesystem/
- Deep Dive Into the Go Type System – https://code.tutsplus.com/tutorials/deep-dive-into-the-go-type-system–cms-29065
- Understanding Golang Type System – https://thenewstack.io/understanding-golang-type-system/
- A Closer Look at Golang From an Architect’s Perspective – https://thenewstack.io/a-closer-look-at-golang-from-an-architects-perspective/
- https://go101.org/article/type-system-overview.html
- https://baziotis.cs.illinois.edu/compilers/the-weird-type-system-of-golang.html
- https://blog.ankuranand.com/2018/11/29/a-closer-look-at-go-golang-type-system/
- 《Type Systems for Programming Languages》 – https://ropas.snu.ac.kr/~kwang/520/pierce_book.pdf
- 《Programming with Types》 – https://book.douban.com/subject/35325133/
- Type Systems in Programming Languages – https://www.tektutorialshub.com/programming/type-systems-in-programming-languages/
- 《Category Theory for Programmers》 – https://book.douban.com/subject/30357114/
- Type system(维基百科) – https://en.wikipedia.org/wiki/Type_system
- 类型系统的比较 – https://en.wikipedia.org/wiki/Comparison_of_type_systems

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

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

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论