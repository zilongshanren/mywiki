---
title: Go 1.18之后的语法新特性Quiz，你能做对几个？
url: https://tonybai.com/2024/08/27/a-new-syntax-quiz-after-go-1-18/
published: '2024-08-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.18之后的语法新特性Quiz，你能做对几个？

![](../../assets/1851502749fd9459.png)


[本文永久链接](https://tonybai.com/2024/08/27/a-new-syntax-quiz-after-go-1-18) – https://tonybai.com/2024/08/27/a-new-syntax-quiz-after-go-1-18

自[Go 1.18版本](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)以来，Go语言引入了许多令人兴奋，但也可能令你感觉难以理解的语法新特性。这些特性大大增强了语言的表达能力，但也增加了学习曲线。今天，我们通过几个小Quiz来测试你对这些新特性的理解。准备好挑战自己了吗？答案在文章末尾公布，但请先尝试独立思考每个问题！

注：为了保证答案一致，这里的答案输出都是基于刚发布没多久的

[Go 1.23.0版本]。

## Quiz 1: 泛型与类型集合（[Go 1.18](https://mp.weixin.qq.com/s/4wYrwBwnuylSvTaxBMXUgg)）

```
import (
"fmt"
"golang.org/x/exp/constraints"
)
type Scalar interface {
constraints.Integer | constraints.Float | ~string
}
func Plus[T Scalar](a, b T) T {
return a + b
}
type MyString string
func main() {
fmt.Println(Plus(1, 2))
fmt.Println(Plus(1.5, 2.7))
fmt.Println(Plus("Hello, ", "World"))
fmt.Println(Plus(MyString("Go "), MyString("1.18+")))
}
```


问题：上述代码会输出什么？

- A) 编译错误，MyString类型不满足Scalar接口
- B) 3

4.2

Hello, World

Go 1.18+ - C) 3

4.2

Hello, World

编译错误，MyString类型不能进行加法操作 - D) 编译错误，不能对不同类型（如int和float64）使用同一个Plus函数

## Quiz 2: 修正后的循环变量语义（[Go 1.22](https://mp.weixin.qq.com/s/KUiTxRBQcywcyHsHmOFvEQ)）

```
func main() {
s := []string{"a", "b", "c"}
funcs := make([]func(), len(s))
for i, v := range s {
funcs[i] = func() {
fmt.Printf("%d: %s\n", i, v)
}
}
for _, f := range funcs {
f()
}
}
```


问题：在Go 1.22中，这段代码最可能的输出是什么？

- A) 0: c

1: c

2: c - B) 0: a

1: b

2: c - C) 输出不确定，可能是A或B中的任何一种
- D) 编译错误，因为在闭包中使用循环变量

## Quiz 3: range over int（[Go 1.22](https://mp.weixin.qq.com/s/KUiTxRBQcywcyHsHmOFvEQ)）

```
func generateSequence(n int) []int {
seq := make([]int, n)
for i := range n {
seq[i] = (i * i) % 10
}
return seq
}
func main() {
fmt.Println(generateSequence(7))
}
```


问题：这段代码会输出什么？

- A) [0 1 4 9 16 25 36]
- B) [0 1 4 9 6 5 6]
- C) [0 1 2 3 4 5 6]
- D) 编译错误，不能对int类型使用range

## Quiz 4: range-over-func（[Go 1.23](https://mp.weixin.qq.com/s/GvPDgWP6BjxllLPNnSNS3A)）

```
import (
"iter"
"fmt"
)
func fibonacci() iter.Seq[int] {
a, b := 0, 1
return func(yield func(int) bool) {
for {
if !yield(a) {
return
}
a, b = b, a+b
}
}
}
func main() {
count := 0
for v := range fibonacci() {
if count == 7 {
break
}
fmt.Printf("%d ", v)
count++
}
}
```


问题：假设启用了相关实验特性，这段代码会输出什么？

A) 0 1 1 2 3 5 8

B) 0 1 2 3 4 5 6

C) 1 1 2 3 5 8 13

D) 编译错误，iter.Seq不是一个合法的迭代器

## Quiz 5: 带类型参数的别名（试验特性，[Go 1.23](https://mp.weixin.qq.com/s/GvPDgWP6BjxllLPNnSNS3A)）

注：下面示例使用GOEXPERIMENT=aliastypeparams go run 运行


```
package main
import "fmt"
type Pair[T, U any] = struct {
First T
Second U
}
func MakePair[T, U any](first T, second U) Pair[T, U] {
return Pair[T, U]{First: first, Second: second}
}
func SwapPair[T, U any](p Pair[T, U]) Pair[U, T] {
return Pair[U, T]{First: p.Second, Second: p.First}
}
func main() {
intStringPair := MakePair(42, "Answer")
swappedPair := SwapPair(intStringPair)
fmt.Printf("Swapped Int-String Pair: %+v\n", swappedPair)
}
```


问题：假设启用了相关实验特性，这段代码的结果是什么？

A) Swapped Int-String Pair: {First:Answer Second:42}

B) Swapped Int-String Pair: {First:42 Second:Answer}

C) 运行时错误，类型推导失败

D) 编译错误，不支持带类型参数的别名

这些Quiz涵盖了Go 1.18以来的一些重要新特性，包括泛型、修正的循环变量语义、range over int、[range-over-func](https://tonybai.com/2024/06/24/range-over-func-and-package-iter-in-go-1-23/)以及类型参数别名。如果你能正确回答大部分问题，那么恭喜你，你对Go的新特性已经有很好的理解了！

注：关注公众号iamtonybai，回复“go1.23quiz”，即可获得这五道题目的正确答案。


[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论