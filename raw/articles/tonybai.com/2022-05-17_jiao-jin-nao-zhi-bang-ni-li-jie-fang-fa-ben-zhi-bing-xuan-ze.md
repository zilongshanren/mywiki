---
title: 绞尽脑汁，帮你理解方法本质并选择正确的receiver类型
url: https://tonybai.com/2022/05/17/understand-the-nature-of-go-method-and-how-to-choose-the-correct-receiver-type/
published: '2022-05-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 绞尽脑汁，帮你理解方法本质并选择正确的receiver类型

![](../../assets/4326fa5523386089.png)


[本文永久链接](https://tonybai.com/2022/05/17/understand-the-nature-of-go-method-and-how-to-choose-the-correct-receiver-type) – https://tonybai.com/2022/05/17/understand-the-nature-of-go-method-and-how-to-choose-the-correct-receiver-type

Go语言虽然不支持经典的面向对象语法元素，比如：类、对象、继承等，但Go语言也有方法（method）。和函数相比，Go语言中的方法在声明形式上仅仅多了一个参数，Go称之为**receiver参数**，而receiver参数正是方法与类型之间的纽带。

那么Go语言的方法究竟是什么？它与函数究竟是什么关系？我们又该如何选择receiver参数的类型呢? 是选择值类型还是指针类型？

本文将通过[《Go语言精进之路：从新手到高手的编程思想、方法与技巧》](https://item.jd.com/13694000.html)这本书的内容来帮助大家深入理解Go方法的本质，并给出receiver参数类型选择的原则，让大家不再困惑。

![img{512x368}](../../assets/547482cabd3c0134.png)


### 1.什么是Go语言的方法(method)

Go方法的一般声明形式如下：

```
func (receiver T/*T) MethodName(参数列表) (返回值列表) {
// 方法体
}
```


上面方法声明中的T称为receiver的基类型。通过receiver，上述方法被绑定到类型T上。换句话说：上述方法是类型T的一个方法，我们可以通过类型T或*T的实例调用该方法，如下面伪代码：

```
var t T
t.MethodName(参数列表)
var pt *T = &t
pt.MethodName(参数列表)
```


Go方法具有如下特点：

1）方法名的首字母是否大写决定了该方法是否是导出方法；

2）方法定义要与类型定义放在同一个包内。由此我们可以推出：不能为原生类型（如int、float64、map等）添加方法，只能为自定义类型定义方法（示例代码如下）。

```
// 错误的做法
func (i int) String() string { // 编译器错误：cannot define new methods on non-local type int
return fmt.Sprintf("%d", i)
}
// 正确的做法
type MyInt int
func (i MyInt) String() string {
return fmt.Sprintf("%d", int(i))
}
```


同理，可以推出：不能横跨Go包为其他包内的自定义类型定义方法。

3）每个方法只能有一个receiver参数，不支持多receiver参数列表或变长receiver参数。一个方法只能绑定一个基类型，Go语言不支持同时绑定多个类型的方法。

4）receiver参数的基类型本身不能是指针类型或接口类型，下面的示例展示了这点：

```
type MyInt *int
func (r MyInt) String() string { // 编译器错误：invalid receiver type MyInt (MyInt is a pointer type)
return fmt.Sprintf("%d", *(*int)(r))
}
type MyReader io.Reader
func (r MyReader) Read(p []byte) (int, error) { // 编译器错误：invalid receiver type MyReader (MyReader is an interface type)
return r.Read(p)
}
```


和其他主流编程语言相比，Go语言从函数到方法仅仅多出了一个receiver，这大大降低了Gopher们学习方法的门槛。但即便如此，Gopher们在把握方法本质以及如何选择receiver的类型时仍存在困惑，本节我就针对这些困惑做重点的说明。

### 2. 方法的本质

前面提到过：Go语言没有类，方法与类型通过receiver联系在一起，我们可以为任何非内置原生类型定义方法，比如下面的类型T：

```
type T struct {
a int
}
func (t T) Get() int {
return t.a
}
func (t *T) Set(a int) int {
t.a = a
return t.a
}
```


C++的对象在调用方法时，编译器会自动传入指向对象自身的this指针作为方法的第一个参数。而对于Go来说，receiver其实也是同样道理，我们将receiver作为第一个参数传入方法的参数列表，上面示例中的类型T的方法就可以等价转换为下面的普通函数：

```
func Get(t T) int {
return t.a
}
func Set(t *T, a int) int {
t.a = a
return t.a
}
```


这种转换后的函数就是**方法的原型**。只不过在Go语言中，这种等价转换是由Go编译器在编译和生成代码时自动完成的。Go语言规范中提供了一个新概念，可以让我们更充分地理解上面的等价转换。

Go方法的一般使用方式如下：

```
var t T
t.Get()
t.Set(1)
```


我们可以将上面方法调用用下面的方式做等价替换：

```
var t T
T.Get(t)
(*T).Set(&t, 1)
```


这种直接以类型名T调用方法的表达方式被称为**方法表达式(Method Expression)**。类型T只能调用T的方法集合（Method Set）中的方法；同理*T只能调用*T的方法集合中的方法（关于方法集合，我们会在下一节中做详细讲解）。我们看到：方法表达式有些类似于C++中的类的静态方法，静态方法在使用时以该C++类的某个对象实例作为第一个参数。而Go语言的方法表达式（Method Expression）在使用时，同样以receiver参数所代表的实例作为第一个参数。

这种通过方法表达式对方法进行调用的方式与我们之前所做的方法到函数的等价转换如出一辙。这就是Go方法的本质：**一个以方法所绑定类型实例为第一个参数的普通函数**。

方法表达式体现了Go方法的本质：其自身的类型就是一个普通函数。我们甚至可以将其作为右值赋值给一个函数类型的变量：

```
var t T
f1 := (*T).Set // f1的类型，也是T类型Set方法的原型：func (t *T, int)int
f2 := T.Get // f2的类型，也是T类型Get方法的原型：func(t T)int
f1(&t, 3)
fmt.Println(f2(t))
```


### 3. 正确选择receiver参数类型

有了上面对Go方法本质的分析，我们再来理解receiver并在定义方法时选择正确的receiver类型就简单多了。我们再来看一下方法和函数的“等价变换公式”：

```
func (t T) M1() <=> M1(t T)
func (t *T) M2() <=> M2(t *T)
```


我们看到：M1方法的receiver参数类型为T，而M2方法的receiver参数类型为*T。

1）当receiver参数的类型为T时，即选择值类型的receiver

我们选择以T作为receiver参数类型时，T的M1方法等价为M1(t T)。我们知道Go函数的参数采用的是值拷贝传递，也就是说M1函数体中的t是T类型实例的一个副本，这样M1函数的实现中无论对参数t做任何修改都只会影响副本，而不会影响到原T类型实例。

2）当receiver参数的类型为*T时，即选择指针类型的receiver

我们选择以*T作为receiver参数类型时，T的M2方法等价为M2(t *T)。我们传递给M2函数的t是T类型实例的地址，这样M2函数体中对参数t做的任何修改都会反映到原T类型实例。

我们以下面的例子演示一下选择不同的receiver类型对原类型实例的影响：

```
// chapter4/sources/method_nature_1.go
type T struct {
a int
}
func (t T) M1() {
t.a = 10
}
func (t *T) M2() {
t.a = 11
}
func main() {
var t T // t.a = 0
println(t.a)
t.M1()
println(t.a)
t.M2()
println(t.a)
}
```


运行该程序：

```
$ go run method_nature_1.go
0
0
11
```


在该示例中，M1和M2方法体内都对字段a做了修改，但M1（采用值类型receiver）修改的只是实例的副本，对原实例并没有影响，因此M1调用后，输出t.a的值仍为0；而M2（采用指针类型receiver）修改的是实例本身，因此M2调用后，t.a的值变为了11。

很多Go初学者还有这样的疑惑：是不是T类型实例只能调用receiver为T类型的方法，不能调用receiver为*T类型的方法呢？答案是否定的。无论是T类型实例，还是*T类型实例，都既可以调用receiver为T类型的方法，也可以调用receiver为*T类型的方法。下面例子证明了这一点：

```
// chapter4/sources/method_nature_2.go
package main
type T struct {
a int
}
func (t T) M1() {
}
func (t *T) M2() {
t.a = 11
}
func main() {
var t T
t.M1() // ok
t.M2() // <=> (&t).M2()
var pt = &T{}
pt.M1() // <=> (*pt).M1()
pt.M2() // ok
}
```


通过例子我们看到T类型实例t调用receiver类型为*T的M2方法是没问题的，同样*T类型实例pt调用receiver类型为T的M1方法也是可以的。实际上这都是Go语法糖，Go编译器在编译和生成代码时为我们自动做了转换。

到这里，我们可以得出receiver类型选用的初步结论：

- 如果要对类型实例进行修改，那么为receiver选择*T类型；
- 如果没有对类型实例修改的需求，那么为receiver选择T类型或*T类型均可；但考虑到Go方法调用时，receiver是以值拷贝的形式传入方法中的。如果类型size较大，以值形式传入会导致较大损耗，这时选择*T作为receiver类型会更好些。

对于receiver的类型的选择其实还有一个重要因素，那就是类型是否要实现某个interface，我们继续往下看。

Go语言的一个创新就是自定义类型与接口之间的实现关系是松耦合的：如果某个自定义类型T的方法集合是某个interface类型的方法集合的超集，那么就说类型T实现了该接口，并且类型T的变量可以被赋值给该接口类型的变量了，即我们说的方法集合决定接口实现。

**方法集合（Method Set）**是Go语言中一个重要的概念，在为接口类型变量赋值、使用结构体嵌入/接口嵌入、类型别名（type alias）和方法表达式（method expression）等时都会用到方法集合，它像“胶水”一样将自定义类型与接口隐式地粘结在一起。

要判断一个自定义类型是否实现了某接口类型，我们首先要识别出自定义类型的方法集合以及接口类型的方法集合。但有些时候它们并非那么明显，尤其是当存在结构体嵌入、接口嵌入和类型别名时。

这里我们实现了一个工具函数可以方便输出一个自定义类型或接口类型的方法集合。

```
// chapter4/sources/method_set_utils.go
func DumpMethodSet(i interface{}) {
v := reflect.TypeOf(i)
elemTyp := v.Elem()
n := elemTyp.NumMethod()
if n == 0 {
fmt.Printf("%s's method set is empty!\n", elemTyp)
return
}
fmt.Printf("%s's method set:\n", elemTyp)
for j := 0; j < n; j++ {
fmt.Println("-", elemTyp.Method(j).Name)
}
fmt.Printf("\n")
}
```


接下来，我们就用该工具函数输出一下本节开头那个示例中的接口类型和自定义类型的方法集合：

```
// chapter4/sources/method_set_2.go
type Interface interface {
M1()
M2()
}
type T struct{}
func (t T) M1() {}
func (t *T) M2() {}
func main() {
var t T
var pt *T
DumpMethodSet(&t)
DumpMethodSet(&pt)
DumpMethodSet((*Interface)(nil))
}
```


运行上述代码：

```
$ go run method_set_2.go method_set_utils.go
main.T's method set:
- M1
*main.T's method set:
- M1
- M2
main.Interface's method set:
- M1
- M2
```


在上述输出结果中，T、*T和Interface各自的方法集合一目了然。我们看到T类型的方法集合中只包含M1，无法成为Interface类型的方法集合的超集，因此这就是开篇例子中编译器认为变量t不能赋值给Interface类型变量的原因。在输出的结果中，我们还看到*T类型的方法集合为[M1, M2]。*T类型没有直接实现M1，但M1仍出现在*T类型的方法集合中了。这符合Go语言规范中的说法：对于非接口类型的自定义类型T，其方法集合为所有receiver为T类型的方法组成；而类型*T的方法集合则包含所有receiver为T和*T类型的方法。也正因为如此，pt才能成功赋值给Interface类型变量。

到这里，我们完全明确了为receiver选择类型时需要考虑的第三点因素：**是否支持将T类型实例赋值给某个接口类型变量。如果需要支持，我们就要实现receiver为T类型的接口类型方法集合中的所有方法**。

### 4. 小结

本文详细介绍了Go语言方法的定义与使用注意实现，并通过实例告诉大家Go方法的本质以及receiver参数的类型选择的三点原则，牢记这三点原则，方法的receiver就再也不会困扰到你了。如果您想要了解更多有关Go语言编程方面的精华内容，推荐您详细阅读我的新作[《Go语言精进之路：从新手到高手的编程思想、方法与技巧》](https://item.jd.com/13694000.html)。

本文涉及的源码可以在[这里](https://github.com/bigwhite/GoProgrammingFromBeginnerToMaster)下载 – https://github.com/bigwhite/GoProgrammingFromBeginnerToMaster。

![](../../assets/686fc4f9a8565f62.jpeg)


Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论