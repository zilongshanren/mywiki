---
title: Go 考古：错误处理的“语法糖”之战与最终的“投降”
url: https://tonybai.com/2025/10/28/go-archaeology-error-handling/
published: '2025-10-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 考古：错误处理的“语法糖”之战与最终的“投降”

![](../../assets/41005a0e29dddfdc.png)


[本文永久链接](https://tonybai.com/2025/10/28/go-archaeology-error-handling) – https://tonybai.com/2025/10/28/go-archaeology-error-handling

大家好，我是Tony Bai。

if err != nil，这可能是 Go 语言中最具辨识度，也最富争议性的代码片段。它如同一块磐石，奠定了 Go 错误处理哲学的基石，但也因其“繁琐”而常年位居 Go 开发者年度调查“最不满意特性”榜首。

许多新入门的 Gopher 可能会感到困惑：Go 团队为何如此“固执”，十余年来始终拒绝为这个明显的痛点，提供一个类似 try-catch 或 Rust ? 运算符的“语法糖”？

事实上，这并非因为 Go 团队的傲慢或忽视。Go 的设计，是在一场关于“异常 (Exceptions) vs. 返回码 (Status Returns)”的世纪之辩的硝烟中诞生的。而 Go 语言的历史，就是一部试图为“返回码”的繁琐寻找“语法糖”，却屡战屡败，并最终选择坚守初心的历史。

本文，就让我们扮演一次“Go 考古学家”，深入挖掘历史的尘埃，回顾这场旷日持久的“语法糖之战”，并揭示 Go 团队为何在 2025 年，最终[选择向“现状投降”](https://tonybai.com/2025/06/04/error-syntax/)。

![](../../assets/ce05c9c7438fe698.png)


## 历史的十字路口 —— 返回码的“五宗罪”与异常的“原罪”

要理解 Go 的选择，我们必须回到 Go 诞生之前，重温那场关于错误处理的根本性辩论。一篇由 Ned Batchelder 在 2003 年撰写的经典文章《[Exceptions vs. status returns](https://nedbatchelder.com/text/exceptions-vs-status.html)》，完美地总结了这场辩论。

### 返回码的“五宗罪”

文章雄辩地论证了 C++ 风格的返回码（Go 中 error 的前身）存在种种弊端。

#### 罪状一：代码混淆

返回码最大的问题，就是它用大量的错误检查代码，污染了正常的业务逻辑。

**C++ (返回码风格)**：

`cpp`


STATUS st = DoThing1(a);

if (st != S_OK) return st;

st = DoThing2(b);

if (st != S_OK) return st;**C++ (异常风格)**：

`cpp`


DoThing1(a);

DoThing2(b);

异常机制通过“隐式”地向上传播错误，让“快乐路径”的代码保持了极度的纯粹和整洁。

#### 罪状二：侵占宝贵的返回通道

返回码模式“霸占”了函数的返回值通道，使得函数无法自然地返回其计算结果。这常常导致各种奇怪的约定，如“失败时返回 NULL”或“失败时返回 -1”，增加了认知负担。

#### 罪状三：贫乏的错误信息

一个整数返回码，只能告诉你“出错了”，却无法告诉你**为什么出错、在哪里出错**。虽然可以通过其他全局变量（如 errno）来传递额外信息，但这既笨拙又不安全。

#### 罪状四：无法在构造函数等隐式代码中使用

在 C++ 中，构造函数和析构函数没有返回值，因此无法使用返回码模式。

#### 罪状五：容易被忽略（过失犯罪）

当开发者忘记检查一个返回码时，错误就会被**无声地忽略**，程序会带着错误的状态继续运行，最终在未来的某个时刻，以一种极其诡异的方式崩溃，让调试成为噩梦。

### 异常的“原罪”

与此同时，异常机制也并非银弹。文章也引用了Joel Spolsky 等人对异常机制提出的批评，同样振聋发聩：

#### 原罪一：隐形的 goto

异常，本质上是一种“超级 goto”。它在你代码的任何地方，都可能引入一个**不可见的、非线性的控制流跳转**。

“看着一段代码，你根本无法知道它会从哪里、以何种方式突然跳出去。” —— Joel Spolsky


这种不确定性，极大地增加了代码推理的难度。为了编写出真正健壮的异常处理代码，你必须像一个偏执狂一样，思考每一次函数调用背后，所有可能抛出的异常，以及它们对当前函数状态的影响。

#### 原罪二：过多的出口

每一个可能抛出异常的函数调用，都为你的函数增加了一个**隐式的“出口”**。这使得资源管理（如文件句柄、网络连接、锁）变得极其复杂。虽然 defer / finally / RAII 等机制可以缓解这个问题，但它无法消除其固有的复杂性。

## Go 的“初始选择” —— 带着镣铐的舞蹈

Go 的设计者们，正是在这场辩论的硝烟中，做出了他们的“初始”决策。他们深刻地洞察到：由返回码带来的**“显式的代码复杂性”**，其代价是**明确的、局部的、可控的**；而由异常带来的**“隐式的认知复杂性”**，其代价是**模糊的、全局的、难以推理的**。

在“代码的整洁度”和“控制流的明确性”之间，Go **毫不犹豫地选择了后者**。

同时，Go 语言通过一系列天才般的设计，精准地“反驳”了返回码的“五宗罪”：

**多返回值**：解决了“侵占返回通道”的问题，让错误和结果可以并行传输。

```
value, err := DoSomething()
if err != nil {
// handle error
}
// use value
```


这个看似简单的语言特性，却是一次天才般的设计。它让错误和结果可以**并行传输**，互不干扰，完美地保留了函数返回值的表达能力。

**error 接口**：解决了“信息贫乏”的问题，让错误可以携带任意丰富的上下文。

Go 将错误定义为一个**接口 error**，而不仅仅是一个整数。

```
type error interface {
Error() string
}
```


这意味着，任何实现了 Error() 方法的类型，都可以是一个错误。这赋予了 Go 错误**无限的表达能力**。我们可以创建自定义的错误类型，携带丰富的上下文信息，如堆栈跟踪、请求 ID、文件名等等。

**工厂模式 (New…)**：通过移除构造函数，解决了“适用性受限”的问题。

Go **从语言层面移除了构造函数和析构函数**，代之以普通的工厂函数 (New…)。这种设计，不仅简化了语言，也使得错误处理可以在对象的创建过程中，以一种自然、统一的方式进行。

**静态分析工具 (go vet)**：通过工具链，解决了“易被忽略”的问题。

Go 社区通过强大的**静态分析工具**（如 go vet 和 staticcheck）来对抗这种“过失犯罪”。这些工具能自动检测出被忽略的 error 返回值，并在 CI/CD 流程中强制开发者修正它们。

只剩下最后一项“原罪”——**代码混淆**——被 Go “坦然地接受”了。if err != nil，就是 Go 为了换取控制流的绝对清晰性，而选择戴上的“镣铐”。

## 奠基 —— “错误即是值”

这副“镣铐”虽然沉重，但 Go 的设计者们认为，开发者不应只是被动地忍受它。Rob Pike 2015 年的著名博文《[Errors are values](https://go.dev/blog/errors-are-values)》，正是这份“戴着镣铐跳舞”的宣言。

文章的核心观点是：既然错误是值，那么我们就可以像对待任何其他值一样，对它们进行**编程**。

### 考古发现一：bufio.Scanner 的优雅

Pike 举了 bufio.Scanner 的例子。它的 Scan() 方法并不返回 error，而是返回一个 bool。所有的错误都被内部“暂存”起来，直到整个迭代结束后，才通过一个单独的 Err() 方法一次性检查。

```
scanner := bufio.NewScanner(input)
for scanner.Scan() {
token := scanner.Text()
// ... process token
}
if err := scanner.Err(); err != nil {
// process the error
}
```


这种将“迭代逻辑”与“错误处理”分离的设计，极大地提升了代码的清晰度。

### 考古发现二：errWriter 的封装

Pike 还分享了他为日本 Gopher @jxck_ 现场编写的一个 errWriter 结构体，用以解决重复的 Write 调用和错误检查：

```
type errWriter struct {
w io.Writer
err error
}
func (ew *errWriter) write(buf []byte) {
if ew.err != nil {
return // 一旦出错，后续操作都变成 no-op
}
_, ew.err = ew.w.Write(buf)
}
// 使用方式
ew := &errWriter{w: fd}
ew.write(p0[a:b])
ew.write(p1[c:d])
// ...
if ew.err != nil {
return ew.err
}
```


这篇文章为 Go 的错误处理定下了基调——**不要总想着向语言索要语法糖，而要学会利用语言现有的能力，通过编程模式来优雅地处理错误。**

## 旷日持久的“语法糖之战”

尽管“错误即是值”的哲学深入人心，但“样板代码”的抱怨声从未停止。Go 团队也并非铁板一块，他们曾多次发起“冲锋”，试图卸下这副“镣铐”。

[Go 2 的 check/handle (2018)](https://go.googlesource.com/proposal/+/master/design/go2draft-error-handling.md)：一个功能全面但被认为**过于复杂**的方案，最终被放弃。

`go`


// check/handle 版本的 printSum

func printSum(a, b string) error {

handle err { return err } // 定义当前函数的错误处理器

x := check strconv.Atoi(a) // 如果 Atoi 返回错误，check 会将错误传递给 handle

y := check strconv.Atoi(b)

fmt.Println("result:", x + y)

return nil

}[臭名昭著的 try 提案 (2019)](https://go.googlesource.com/proposal/+/master/design/32437-try-builtin.md)：一个极其简化的方案，但因其**隐藏了 return**，被社区猛烈抨击为“隐形 goto”，最终也被放弃。

`go`


// try 版本的 printSum

func printSum(a, b string) error {

x := try(strconv.Atoi(a)) // 如果 Atoi 返回错误，try 会立即从 printSum 返回该错误

y := try(strconv.Atoi(b))

fmt.Println("result:", x + y)

return nil

}[最后的“诺曼底登陆” —— Ian Taylor 的 ? 尝试 (2024)](https://go.dev/issue/71203)：借鉴了 Rust 的成功经验，但依然未能获得社区的广泛共识。

`go`


// ? 版本的 printSum

func printSum(a, b string) error {

x := strconv.Atoi(a) ?

y := strconv.Atoi(b) ?

fmt.Println("result:", x + y)

return nil

}

## 宣布“停战” —— 2025 年的最终决定

在经历了三次大规模的“战争”，以及社区提交的数百个形形色色的提案之后，Go 团队终于在 2025 年，通过一篇[官方博文](https://go.dev/blog/error-syntax)，为这场旷日持久的“语法糖之战”画上了一个句号。

文章的结论，可以概括为一句无奈但充满智慧的“投降”：


在可预见的未来，Go 团队将停止为错误处理寻求任何语法上的语言变更。

其背后的原因，是 Go 团队在多年探索后得出的深刻反思：

**没有共识**：没有任何一个提案，能够获得社区压倒性的支持。强行推行任何一个，都只会制造新的分裂。**现状“足够好”**：Go 现有的错误处理方式，虽然繁繁，但**行之有效**。随着开发者对“错误即是值”的哲学理解加深，以及 errors.Is/As、cmp.Or 等库函数的增强，这种繁琐在很多时候是可以被接受或通过编程模式缓解的。**显式的好处**：if err != nil 的显式性，在代码阅读和调试时（例如，设置断点、打印日志）具有不可替代的好处。**成本巨大**：任何语言的语法变更，其带来的生态系统（工具、文档、教程、现有代码）的迁移成本都是巨大的。在没有明确、压倒性收益的情况下，这种成本难以被证明是合理的。

## 小结

Go 的“考古”之旅，让我们看到了一部关于工程权衡的生动历史。Go 语言之所以成为今天的 Go，不仅仅在于它**拥有**什么，更在于它在经历了反复的、痛苦的斗争后，**选择放弃**了什么。

这场围绕错误处理的“语法糖之战”，最终没有赢家。但 Go 社区，以及 Go 语言本身，却通过这场战争，更加深刻地理解并巩固了其设计的核心——**清晰性与简单性，有时比一时的便利更重要。** if err != nil 的样板代码，或许就是我们为这份哲学所付出的、值得付出的代价。

## 参考资料

- https://go.dev/blog/error-handling-and-go
- https://go.dev/blog/errors-are-values
- https://go.dev/blog/error-syntax
- https://nedbatchelder.com/text/exceptions-vs-status.html

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


**想系统学习Go，构建扎实的知识体系？**

我的新书《[Go语言第一课](https://book.douban.com/subject/37499496/)》是你的首选。源自2.4万人好评的极客时间专栏，内容全面升级，同步至Go 1.24。首发期有专属五折优惠，不到40元即可入手，扫码即可拥有这本300页的Go语言入门宝典，即刻开启你的Go语言高效学习之旅！

![](../../assets/d3fd3ab3e1fd7a7e.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论