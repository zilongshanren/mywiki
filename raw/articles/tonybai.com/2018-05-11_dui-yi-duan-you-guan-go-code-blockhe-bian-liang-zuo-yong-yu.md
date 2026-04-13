---
title: 对一段有关Go Code Block和变量作用域的代码的简要分析
url: https://tonybai.com/2018/05/11/the-analysis-of-a-go-code-snippet-about-code-blocks-and-scope/
published: '2018-05-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 对一段有关Go Code Block和变量作用域的代码的简要分析

近期，[Go](https://tonybai.com/tag/go) team的[David CrawShaw](https://github.com/crawshaw)在[twitter](https://twitter.com/davidcrawshaw)上贴出了一段代码，如下：

```
func main() {
if a := 1; false {
} else if b := 2; false {
} else if c := 3; false {
} else {
println(a, b, c)
}
}
```


David CrawShaw想表达的意图是gopher们很少在”else if”后面的simple statement中使用[“短变量声明”](https://golang.org/ref/spec#Short_variable_declarations)形式，而这段代码是个例外。我们看到b、c两个变量都是在else if 的simple statement中使用短变量声明形式定义的。

我个人看到这段代码后，第一反应是：这段代码能编译运行吗？else语句中的“println(a, b, c)”是否会被compiler报出：undefined b, c的错误呢？不知道是否有其他的gopher们与我有同样的反应:)。无论怎样，既然有了疑问，我们就应该把它分析清楚。

## 一. Go代码块和作用域简介

根据[Go语言的规范](https://golang.org/ref/spec#Blocks)，我们知道Go的标识符作用域是基于[代码块（code block）](https://golang.org/ref/spec#Blocks)的。代码块就是包裹在一对大括号内部的声明和语句，并且是**可嵌套的**。我们在代码中直观可见的显式的(explicit)code block有很多，比如：函数的函数体、for循环的循环体等：

```
func Foo() {
// here：显式的(explict block)代码块，包裹在函数的函数体内
... ...
for {
// here: 显式的(explict block)代码块，包裹在for循环体内
// 该代码块就嵌套在函数体这个代码块的内部
... ...
}
}
```


但除了显式explict的code block，Go语言中还有几种隐式的(implicit)代码块，它们都是什么呢？这里摘录下go spec原文（不翻译了）：

```
1. The universe block encompasses all Go source text.
2. Each package has a package block containing all Go source text for that package.
3. Each file has a file block containing all Go source text in that file.
4. Each "if", "for", and "switch" statement is considered to be in its own implicit block.
5. Each clause in a "switch" or "select" statement acts as an implicit block.
```


我们看到if语句会引入一个隐式的code block，这为我们后续的分析奠定了基础。

## 二. if语句的code block

那么if语句的code block详细情况如何呢？我们分门别类地简单看看：

### 1. if _ 型

我们使用最多的if语句类型就是**单if型**，即:

```
if simplestmt; expression {
... ...
}
```


在这种类型的if语句中，有两个code block：一个隐式的code block和一个显式的code block。我们把上面的形式代码做一个等价变化，并加上code block起始和结束点的标注，结果如下：

```
{ // implicit block begin
simplestmt
if expression { // explicit block begin
... ...
} // explicit block end
} // implicit block end
```


我们看到if后面的”大括号对”引入的explict code block嵌套在if simplestmt所在的implicit code block内部，这也是为何simplestmt中用短声明形式定义的变量在explict block中可以使用的原因：

```
func main() {
if a := 1; true {
fmt.Println(a) // output: 1
}
}
```


### 2. if _ else _ 型

我们再来看看**if _ else _ 型**：

```
if simplestmt; expression {
... ...
} else {
... ...
}
```


分析逻辑同上，我们将上面的伪代码做一个等价变换，并作出code block起始结束点标注：

```
{ // implicit block begin
simplestmt
if expression { // explicit block1 begin
... ...
} else { // explicit block1 end, explicit block2 start
... ...
} //explicit block2 end
} // implicit block end
```


我们看到**if _ else _ 型** 有三个code block，除了单if型的两个block外，还由else引入一个explict code block（即上面代码中的explict block2）。

### 3. if _ else if _ else _ 型

最后我们来看看最为复杂的**if _ else if _ else _ 型**：

```
if simplestmt1; expression1 {
... ...
} else if simplestmt2; expression2 {
... ...
} else {
... ...
}
```


我们依旧将上面的伪代码做一个等价变换，并作出code block起始结束点标注，结果如下：

```
{ // implicit block1 begin
simplestmt1
if expression { // explicit block1 begin
... ...
} else { // explicit block1 end, explicit block2 start
{ // implicit block2 begin
simplestmt2
if expression2 { // explicit block3 start
} else { // explicit block3 end, explicit block4 start
} // explicit block4 end
} // implicit block2 end
} //explicit block2 end
} // implicit block1 end
```


我们看到在该类型下，我们一共识别出两个implict block和四个explict block。

## 三. 对David CrawShaw贴出的那段代码的分析

有了第二节的基础，再来看David CrawShaw的这段代码：

```
func main() {
if a := 1; false {
} else if b := 2; false {
} else if c := 3; false {
} else {
println(a, b, c)
}
}
```


依照我们的思路，我们可以对这段代码做一个等价变化：

```
func main() {
{
a := 1
if false {
} else {
{
b := 2
if false {
} else {
{
c := 3
if false {
} else {
println(a, b, c)
}
}
}
}
}
}
}
```


展开后的语句就很是一目了然了，不用说什么大家也会很清楚了。最重要的一点是原来代码中最后的那个else实际上是与最内层的else if配对的，而不是与最开始的if配对的，因此println(a, b, c)的时候，a, b, c三个变量都是已经声明定义了的(在外层的code block中)。

对于此类涉及code block或变量作用域的问题，还可以通过go vet -shadow工具来辨别，或通过go run执行后的出错信息来辨别，这里就不详细说明了。

## 四. 参考资料

[51短信平台](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论