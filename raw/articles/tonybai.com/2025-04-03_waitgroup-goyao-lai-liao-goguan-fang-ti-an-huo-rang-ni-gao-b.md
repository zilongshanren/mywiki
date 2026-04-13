---
title: WaitGroup.Go要来了？Go官方提案或让你告别Add和Done样板代码
url: https://tonybai.com/2025/04/03/waitgroup-go-proposal/
published: '2025-04-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# WaitGroup.Go要来了？Go官方提案或让你告别Add和Done样板代码

![](../../assets/e038b91986babf93.jpeg)


[本文永久链接](https://tonybai.com/2025/04/03/waitgroup-go-proposal) – https://tonybai.com/2025/04/03/waitgroup-go-proposal

[sync.WaitGroup](https://pkg.go.dev/sync#WaitGroup)是Go语言中处理[并发任务同步](https://tonybai.com/2015/06/23/concurrency-and-parallelism)最常用的原语之一。然而，其经典的Add(1)、go func() { defer wg.Done() … }()、Wait()模式虽然强大，却也因其固定写法和潜在的陷阱（如忘记Done或将Add误置于goroutine内部）而让开发者时常感到繁琐，对新手尤其不友好。近日，一项旨在简化这一模式的提案[#63796](https://github.com/golang/go/issues/63796)在Go社区引发了广泛关注，并已被标记为** Likely Accept**，预示着sync.WaitGroup可能很快将迎来一个实用的新方法：Go。这也意味着Go开发者可以告别Add、defer Done的样板代码，并避免它们的“陷阱”可能导致的难以捕捉的代码错误。在这篇文章中，我就来简单介绍一下WaitGroup.Go这个提案。

## 1. 现有模式的痛点与WaitGroup.Go的提出

当前使用WaitGroup的标准模式通常如下所示：

```
package main
import (
"fmt"
"sync"
"time"
)
func work(id int) {
fmt.Printf("Worker %d starting\n", id)
time.Sleep(time.Second)
fmt.Printf("Worker %d done\n", id)
}
func main() {
var wg sync.WaitGroup
for i := 1; i <= 5; i++ {
// 注意：在 Go 1.22 之前，需要 i := i 来避免闭包捕获问题
// i := i
wg.Add(1) // 必须在启动 goroutine 前调用 Add
go func(id int) {
defer wg.Done() // 必须在 goroutine 退出前调用 Done
work(id)
}(i)
}
wg.Wait() // 等待所有 goroutine 完成
fmt.Println("All workers done")
}
```


这种样板使用模式存在几个容器出错的关键点：

**wg.Add(1) 的位置:**必须在启动goroutine之前调用。如果将其放在goroutine内部，可能会导致Wait在Add执行前就返回，引发panic或竞态条件。这是最常见的错误之一。**defer wg.Done():**必须确保在goroutine逻辑结束时调用Done，否则Wait将永久阻塞。defer是推荐做法，但也可能被遗漏。**闭包变量捕获 (Go < 1.22):**在[Go 1.22](https://tonybai.com/2024/02/18/some-changes-in-go-1-22)之前的版本中，循环变量直接在goroutine的闭包中使用会导致所有goroutine共享同一个变量值，需要i := i 这样的技巧来创建副本。

为了解决这些问题，提案[#63796](https://github.com/golang/go/issues/63796) 建议为sync.WaitGroup添加一个Go方法：

```
// Go calls f on a new goroutine and adds that task to the WaitGroup.
// When f returns, the task is removed from the WaitGroup.
// ... (其他文档细节省略)
func (wg *WaitGroup) Go(f func()) {
wg.Add(1)
go func() {
defer wg.Done()
f()
}()
}
```


这个方法简洁地封装了Add(1)、启动goroutine和defer Done()的逻辑。使用Go方法后，之前的例子可以大幅简化为下面代码：

```
package main
import (
"fmt"
"sync"
"time"
)
func work(id int) {
fmt.Printf("Worker %d starting\n", id)
time.Sleep(time.Second)
fmt.Printf("Worker %d done\n", id)
}
func main() {
var wg sync.WaitGroup // 假设WaitGroup已包含Go方法
for i := 1; i <= 5; i++ {
// Go 1.22+版本无需i := i
wg.Go(func() {
work(i)
})
}
wg.Wait()
fmt.Println("All workers done")
}
```


我们可以看到，代码不仅行数减少，而且显著降低了出错的可能性，尤其是避免了Add位置错误这一高频陷阱。

## 2. 时机成熟：为何现在是引入WaitGroup.Go的好时机？

该提案并非首次提出（相关讨论可追溯至[#18022](https://github.com/golang/go/issues/18022)和[#39863](https://github.com/golang/go/issues/39863)），但之前的提案因各种原因未能被接受。此次能够获得”Likely Accept”的状态，可能主要得益于以下几个因素：

- Go 1.22循环变量语义变化

Go 1.22正式“修正”了for循环的变量语义，使得每次迭代都会创建新的循环变量实例。这极大地降低了在wg.Go的闭包函数中直接使用循环变量的风险，使得func()形式的API更加安全和自然。正如dsnet在评论中指出的，虽然闭包仍可能引入其他变量修改的风险，但相比wg.Add位置错误，这种风险出现的频率要低得多。

- 社区实践的验证

许多流行的第三方库（如tailscale.com/syncs和sourcegraph/conc）以及golang.org/x/sync/errgroup都已经实现了类似的Go方法，证明了其在实际开发中的价值和受欢迎程度。这为标准库采纳该模式提供了有力佐证。

- 错误预防的迫切性

尽管社区曾讨论过通过vet工具检查wg.Add误用（[#18022](https://github.com/golang/go/issues/18022)），但此前相关检查迟迟未能落地（直到最近才由adonovan等人推动并合并了相关分析器）。直接在API层面提供更安全的替代方案，被认为是更有效的解决途径。GitHub代码搜索也显示，虽然正确用法占绝大多数，但错误用法（go之后才Add）数量仍然不可忽视（上千例）。

## 3. 社区讨论焦点

在提案的讨论过程中，社区成员也提出了一些值得思考的问题，这里也找出一些典型的问题供大家玩味：

**是否需要新类型？**

有人建议创建一个新的类型（如sync.Tasks），以避免WaitGroup同时存在Add/Done和Go两种模式可能带来的混淆。但主流观点认为，将Go方法添加到现有WaitGroup可以方便现有代码的**原地升级**（gopls甚至已为此添加了自动化重构支持），并且混合使用的风险较低（错误使用Done会快速panic，多余的Add也会导致Wait阻塞，易于发现）。

**与errgroup的关系**

[errgroup.Group也有Go方法](https://pkg.go.dev/golang.org/x/sync/errgroup#Group.Go)，但它还处理了错误传播和context取消。WaitGroup.Go则更纯粹地关注任务同步，两者定位不同，可以共存。将errgroup引入标准库是另一个独立的提案（[#57534](https://github.com/golang/go/issues/57534)）。

**方法命名**

曾有提议使用Start或Run，但Go这个命名与errgroup中的Go保持一致，且能清晰表达“启动新goroutine”的含义，最终获得了更多支持。

**文档重塑**

Go当前的技术负责人aclements建议将WaitGroup的文档从“计数器”视角转向“任务集合”视角，并将Go作为首选方法进行介绍。对此adonovan提醒WaitGroup本质仍是计数信号量，文档更新需谨慎平衡。

## 4. 小结

sync.WaitGroup.Go提案的”Likely Accept”状态对于Go开发者来说是一个积极的信号。这个看似简单的补充，有望显著提升Go并发编程的体验，减少Add和Done的样板代码，规避常见错误。它体现了Go团队在保持核心库简洁性的同时，也愿意吸收社区成熟实践、优化开发者体验的务实态度。我们期待在未来的Go版本中看到这一实用特性的正式发布，届时，编写健壮、简洁的并发代码将变得更加容易。

## 5. 参考资料

[proposal: sync: add WaitGroup.Go](https://github.com/golang/go/issues/63796)– https://github.com/golang/go/issues/63796[errgroup doc](https://pkg.go.dev/golang.org/x/sync/errgroup)– https://pkg.go.dev/golang.org/x/sync/errgroup

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Gopher的AI原生应用开发第一课”、“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格6$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

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

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

所以没来之前我还是用着舒服的conc