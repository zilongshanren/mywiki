---
title: 为什么这个T类型实例无法调用*T类型的方法
url: https://tonybai.com/2022/02/27/go-addressable/
published: '2022-02-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为什么这个T类型实例无法调用*T类型的方法

![](../../assets/fb4fc11c35377ed4.png)


[本文永久链接](https://tonybai.com/2022/02/27/go-addressable) – https://tonybai.com/2022/02/27/go-addressable

近期在[“Go语言第一课”专栏](http://gk.link/a/10AVZ)后台看到一位学员的一则留言，如下图：

![](../../assets/34246e5cddcb82d0.png)


由于有课程上下文，所以我这里将问题的上下文重新描述一下。

在[专栏](http://gk.link/a/10AVZ)的第25讲，我们学习了Go语言提供的一个“语法糖”，比如下面这个例子：

```
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
var t1 T
t1.M1()
t1.M2()
var t2 = &T{}
t2.M1()
t2.M2()
}
```


Go语言的类型有方法集合(method set)的概念，以上面例子来说，类型T的方法集合为{M1}，而类型*T的方法集合为{M1, M2}。不过方法集合仅用于判断某类型是否实现某接口类型。当我们通过类型实例来调用方法时，Go会提供“语法糖”。上面这个例子先声明了类型T的变量t1，我们看到它不仅可以调用其方法集合中receiver参数类型为T的方法M1，它还可以直接调用不属于其方法集合的、receiver参数类型为*T的方法M2。T类型的实例t1之所以可以调用receiver参数类型为*T的方法M2都是Go编译器在背后自动进行转换的结果，即t1.M2()这种用法是Go提供的“语法糖”：Go判断t1的类型为T，与方法M2的receiver参数类型*T不一致后，会自动将t1.M2()转换为(&t1).M2()。

同理，类型为*T的实例t2，它不仅可以调用receiver参数类型为*T的方法M2，还可以调用receiver参数类型为T的方法M1，这同样是因为Go编译器在背后做了转换：Go判断t2的类型为*T，与方法M1的receiver参数类型T不一致后，会自动将t2.M1()转换为(*t2).M1()。

好了，问题来了！我们参考本文开头处那位学员的留言给出另外一个例子：

```
func main() {
T{}.M2() // 编译器错误：cannot call pointer method M2 on T
(&T{}).M1() // OK
(&T{}).M2() // OK
}
```


在这个例子中，我们通过T{}对T进行实例化后并调用receiver参数类型为*T的M2方法，但编译器报了错误：**cannot call pointer method M2 on T**。

前后两个例子，同样是基于T类型实例，一个可以使用“语法糖”调用M2方法，一个则不行。why？

其实答案就在于：上面的“语法糖”使用有一个前提，那就是T类型的实例需要是**可被取地址的**，即Go语言规范中的**addressable**。

什么是**addressable**呢？[Go语言规范](https://go.dev/ref/spec#Address_operators)中的原话是这样的：

“For an operand x of type T, the address operation &x generates a pointer of type *T to x. The operand must be addressable, that is, either a variable, pointer indirection, or slice indexing operation; or a field selector of an addressable struct operand; or an array indexing operation of an addressable array. As an exception to the addressability requirement, x may also be a (possibly parenthesized) composite literal. ”


翻译过来，大致是说：下面情况中的&x操作后面的操作数x是可被取地址的：

- 一个变量。比如：&x
- 指针解引用(pointer indirection)。比如：&*x
- 切片下标操作。比如：&sl[2]
- 可被取地址的结构体(struct)的字段。比如：&Person.Name
- 可被取地址的数组的下标操作。比如：&arr[1]
- 如果T是一个复合类型，那么&T{}是一个例外，是合法的。

不过，Go语言规范中并没有明确说明哪些情况的操作数或值是不可被取地址的。Go 101作者老貘在其[“非官方Go FAQ”](https://gfw.go101.org/article/unofficial-faq.html#unaddressable-values)中，对不可被取地址的情况做了梳理，这里我们也借鉴一下：

- 字符串中的字节元素

```
s := "hello"
println(&s[1]) // invalid operation: cannot take address of s[1] (value of type byte)
```


- map键值对中的值元素

```
m := make(map[string]int)
m["hello"] = 5
println(&m["hello"]) // invalid operation: cannot take address of m["hello"] (map index expression of type int)
for k, v := range m {
println(&k) // ok, 键元素是可以取地址的
_ = v
}
```


- 接口值的动态值（类型断言的结果）

```
var a int = 5
var i interface{} = a
println(&(i.(int))) // invalid operation: cannot take address of i.(int) (comma, ok expression of type int)
```


- 常量（包括具名常量和字面量）

```
const s = "hello" // 具名常量
println(&s) // invalid operation: cannot take address of s (untyped string constant "hello")
println(&("golang")) // invalid operation: cannot take address of "golang" (untyped string constant)
```


- 包级函数

```
func Foo() {}
func foo() {}
func main() {
f := func() {}
println(&f) //ok, 局部匿名函数可取地址
println(&Foo) // invalid operation: cannot take address of Foo (value of type func())
println(&foo) // invalid operation: cannot take address of foo (value of type func())
}
```


- 方法（用做函数值）

```
type T struct {
a int
}
func (T) M1() {}
func main() {
var t T
println(&(t.M1)) // invalid operation: cannot take address of t.M1 (value of type func())
println(&(T.M1)) // invalid operation: cannot take address of T.M1 (value of type func(T))
}
```


- 中间结果值
- 函数调用
- 显式值转换
- channel接收操作
- 子字符串操作
- 子切片操作
- 加减乘除法操作


```
// 函数调用
func add(a, b int) int {
return a + b
}
println(&(add(5, 6))) // invalid operation: cannot take address of add(5, 6) (value of type int)
// 显示值转换
var b byte = 12
println(&int(b)) // invalid operation: cannot take address of int(b) (value of type int)
// channel接收操作
var c = make(chan int)
println(&(<-c)) // invalid operation: cannot take address of <-c (comma, ok expression of type int)
// 子字符串操作
var s = "hello"
println(&(s[1:3])) // invalid operation: cannot take address of s[1:3] (value of type string)
// 子切片操作
var sl = []int{1, 2, 3, 4, 5}
println(&(sl[1:3])) // invalid operation: cannot take address of sl[1:3] (value of type []int)
// 加减乘除操作
var a, b int = 10, 20
println(&(a + b)) // invalid operation: cannot take address of a + b (value of type int)
println(&(a - b)) // invalid operation: cannot take address of a - b (value of type int)
println(&(a * b)) // invalid operation: cannot take address of a * b (value of type int)
println(&(a / b)) // invalid operation: cannot take address of a / b (value of type int)
```


最后貘兄在非官方Go FAQ中也提到了&T{}是一个例外(貘兄认为是一个语法糖，&T{}被编译器替换为tmp := T{}; (&tmp))，但不代表T{}是可被取地址的。事实告诉我们：**T{}不可被取地址**。这也是文章开头处那个留言中问题的答案。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

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