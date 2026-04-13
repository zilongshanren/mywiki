---
title: Go 标准库提供一个“Must” 函数？社区关于“断言式初始化”的思考
url: https://tonybai.com/2025/10/07/proposal-must-do/
published: '2025-10-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 标准库提供一个“Must” 函数？社区关于“断言式初始化”的思考

![](../../assets/c43991e9a0de9206.png)


[本文永久链接](https://tonybai.com/2025/10/07/proposal-must-do) – https://tonybai.com/2025/10/07/proposal-must-do

大家好，我是Tony Bai。

if err != nil 不仅是 Go 代码中最常见的片段，更是其[错误处理哲学](https://tonybai.com/2025/04/30/go-vs-zig-in-error-handling)的基石。它强制开发者在每一个可能出错的地方，都必须直面失败的可能性。然而，当一个错误在理论上可能发生，但在实践中（尤其是在处理静态、已知的常量时）又“不可能”发生时，这种严谨性是否就变成了一种冗余的样板代码？

这种在便利性与哲学纯粹性之间的张力并非新生事物。Go 标准库自身，就在特定场景下为我们提供了“捷径”。例如，text/template 包就提供了一个 Must 函数：

```
func Must(t *Template, err error) *Template
```


它接收一个 (*Template, error)，并在 error 不为 nil 时直接 panic。这正是为了简化那些基于静态字符串、本不应失败的模板解析过程。

这种“我断言此操作必不失败，否则就是程序级错误”的模式，可以被称为**“断言式初始化” (Assertive Initialization)**。

这一既有模式，正是最近一个被Go技术负责人Austin Clements纳入到Active阶段的提案（[#54297](https://github.com/golang/go/issues/54297)）的灵感来源。该提案由前Go团队成员 Brad Fitzpatrick 发起，其核心问题是：我们是否应该将这种模式从特定包的“特例”，提升为一个通用的、由标准库提供的泛型函数？

这个看似微小的提议，却在 Go 社区引发了一场关于便利性、最佳实践与语言哲学的深度辩论，在这篇文章中，我们就一起来看看这场辩论的过程，并看看是否能从中学习到一些值得借鉴的东西。

![](../../assets/f3973191ef9d6abe.png)


## 问题的缘起：那些“不可能失败”的失败

Brad Fitzpatrick 最初的痛点非常具体而普遍：在初始化一个 httputil.ReverseProxy 时，你需要一个 *url.URL。而创建一个 *url.URL 的标准方式是调用 url.Parse，这是一个会返回 error 的函数：

```
// 常见的初始化代码
var proxy *httputil.ReverseProxy
func init() {
targetURL, err := url.Parse("http://localhost:8080")
if err != nil {
panic(fmt.Sprintf("failed to parse URL: %v", err))
}
proxy = httputil.NewSingleHostReverseProxy(targetURL)
}
```


问题在于，url.Parse(“http://localhost:8080″) 这样一个使用**硬编码、静态已知**的字符串的调用，在实践中是**不可能失败**的。为了处理这个理论上存在、但现实中永不发生的 error，我们不得不编写 3-4 行错误处理的样板代码。

## 社区的“最佳实践”：Tailscale 的 must.Get

Brad Fitzpatrick 在提案中顺便分享了 他所在的创业公司Tailscale 内部广泛使用的一个 must 包的实现，其核心函数 Get 极其简洁：

```
package must
// Get 返回 v。如果 err 不为 nil，它会 panic。
func Get[T any](v T, err error) T {
if err != nil {
panic(err)
}
return v
}
```


有了这个函数，之前的初始化代码可以被简化为一行优雅的表达式：

```
var targetURL = must.Get(url.Parse("http://localhost:8080"))
```


这个小小的辅助函数，其核心价值并不仅仅是减少了代码行数。正如一位评论者所指出的：

“它更大的影响是，使得返回 error 的函数能够被用在表达式中。这常常能将一个冗长的 10-20 行过程，转换为一个 2-3 行的声明。”


## 争议与权衡：一个“潘多拉魔盒”？

尽管社区中许多开发者都分享了他们自己实现的、类似的 must 包，证明了其**广泛的现实需求**，但将其引入标准库的提议，依然引发了深刻的担忧。

### 担忧一：滥用的风险

Ian Lance Taylor 等核心团队成员表达了他们的顾虑：如果标准库提供了一个官方的 must包及相关函数，它是否会被新手或图方便的开发者**滥用作常规的错误处理机制**？

```
// 滥用的例子：在处理动态、不可信的用户输入时使用 must
func handleRequest(r *http.Request) {
// 错误的做法！这里的 err 应该被妥善处理，而不是直接 panic
body := must.Get(io.ReadAll(r.Body))
// ...
}
```


这种滥用，将与 Go 语言核心的错误处理哲学**背道而驰**，让本应健壮的程序变得脆弱不堪。这正是社区在讨论中反复强调的：must 模式的**合法使用场景非常狭窄**，它应该**仅限于**“断言式初始化”的范畴。

### 担忧二：Must 语义的模糊性

另一位开发者提出了一个更微妙的问题：Must 的语义并非总是 if err != nil { panic(err) }。在某些特定场景下，一个包可能需要一个特殊的 Must 函数，比如它会忽略 io.EOF 错误。

如果标准库提供了一个通用的 must，当某个包未来需要引入一个具有特殊行为的 Package.Must 时，就会造成用户的困惑和潜在的向后不兼容问题。

### “自行车棚效应”：它应该放在哪里？叫什么名字？

提案的讨论也充分展现了“自行车棚效应”：在一个简单的问题上，人们会花费大量时间进行辩论。

**应该叫什么？**must.Get, must.Do, must.Value, errors.Must？**应该放在哪里？**一个新的 must 包？还是现有的 errors 包？

其中一个颇具说服力的建议是：将其放入 errors 包，并命名为 errors.Must。这样既能体现其与 error 的相关性，又能利用现有包的“命名空间”，避免了为一个仅有 6 行代码的函数创建一个全新的包。不过关于究竟如何命名，目前尚未有定论！

## 小结：目前的共识与展望

经过激烈的讨论，Go 提案评审委员会似乎已经形成了一些初步的共识：

**最初的 url.MustParse 提案没有争议**，可以独立推进为url包单独添加一个MustParse的函数。- 社区普遍支持在标准库中增加一个**泛型的、带返回值的类似TailScale的must.Get的函数，因为它价值最高。
- 对于不返回值的 must.Do(error)，以及可变参数版本的 must，团队的热情不高，因为担心其被滥用。
- 可能会考虑在 testing.T 中增加一个 t.Must(error) 方法，它在出错时调用 t.Fatal，这在测试代码中非常有用。

54297 提案的最终命运尚未尘埃落定，但它已经成功地将一个长期存在于 Go 社区“灰色地带”的最佳实践，推向了聚光灯下。

这场辩论的核心，并非是否需要这个功能——无数的第三方 must 包已经证明了其价值。真正的核心在于：Go 语言作为一门以严谨和安全著称的语言，应如何以一种**官方的、有引导性的方式**来提供这种“便利”，同时又最大限度地**防止其被误用和滥用**。

无论最终结果如何，这场关于“断言式初始化”的思考，本身就是对 Go 语言设计哲学的一次深刻反思与精彩演绎。

资料链接：https://github.com/golang/go/issues/54297

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论