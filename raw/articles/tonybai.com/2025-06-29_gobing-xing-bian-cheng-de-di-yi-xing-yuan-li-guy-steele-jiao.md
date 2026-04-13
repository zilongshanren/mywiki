---
title: Go并行编程的“第一性原理”：Guy Steele 教你如何“不去想”并行
url: https://tonybai.com/2025/06/29/thinking-parallel-programming/
published: '2025-06-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go并行编程的“第一性原理”：Guy Steele 教你如何“不去想”并行

![](../../assets/2b7d67e01e63197e.png)


[本文永久链接](https://tonybai.com/2025/06/29/thinking-parallel-programming) – https://tonybai.com/2025/06/29/thinking-parallel-programming

大家好，我是Tony Bai。

在多核处理器已成为标配的今天，并行编程能力几乎是每一位后端工程师的必备技能。Go 语言凭借其简洁的 Goroutine 和 Channel 设计，极大地降低了并发编程的门槛，让我们能相对轻松地驾驭并发。但是，写出“能跑”的并发代码，和写出“优雅、高效、可维护”的并行程序之间，往往还隔着一层思维模式的窗户纸。

今天，我想和大家分享一位计算机科学巨匠——Guy L. Steele Jr.——关于并行编程的深刻洞见。在深入探讨之前，有必要简单介绍一下这位大神：他是 Scheme 语言的共同创造者，Common Lisp 标准的核心定义者，Java 语言设计的关键人物，也是 Sun/Oracle 专门为并行计算设计的 Fortress 语言的领导者。他的见解，源于横跨数十年、从学术到工业的深厚语言设计实践。

他早在多年前（其经典 PPT《How to Think about Parallel Programming—Not!》可以追溯到 2009 年甚至更早）就提出了一些颠覆传统认知，但至今依然闪耀着智慧光芒的核心思想。这些思想，对于我们 Gopher 来说，不啻为并行编程的“第一性原理”，能帮助我们从根本上理解如何更好地设计并行系统。

Steele 的核心论点是什么？一言以蔽之：

“编写并行应用程序的最佳方式，就是不必去考虑并行本身。”


这听起来是不是有点反直觉？别急，让我们慢慢拆解 Steele 的智慧。

## 并行编程的“敌人”：根深蒂固的“累加器思维”

Steele 犀利地指出，我们过去几十年在顺序编程中养成的许多习惯，正在成为并行编程的障碍。其中，**“累加器 (Accumulators)”模式首当其冲被他判为“BAD”**。

什么是累加器模式？简单来说，就是通过一个共享状态（累加器），不断迭代地用新数据去更新这个状态。一个最经典的例子就是顺序求和：

```
// 典型的顺序累加求和
func sumSequential(nums []int) int64 {
var total int64 = 0 // 我就是那个“累加器” total
for _, n := range nums {
total += int64(n) // 不断更新自己
}
return total
}
```


这段代码再熟悉不过了，对吧？但在 Steele 看来，这种写法是并行编程的“噩梦”。为什么？

**强烈的顺序依赖：**每一步的 total 都依赖于上一步的结果。这种串行依赖使得直接将其并行化变得异常困难。如果多个 Goroutine 同时去更新 total，就需要引入锁或其他同步机制，不仅增加了复杂性，还可能因为锁竞争而严重影响性能，甚至违背了并行的初衷。**鼓励可变状态与副作用：**累加器本身就是一个可变状态，操作带有副作用。这在并行环境下是诸多问题的根源。

Steele 甚至略带调侃地说：DO 循环太上世纪五十年代了！… 当你写下 SUM = 0 并开始累加时，你就已经把自己“坑”了。

那么，我们应该如何摆脱这种“累加器思维”的桎梏呢？

## Steele的药方：拥抱“分治”与“结合性”

Steele 提倡的核心思想是 **“分治 (Divide-and-Conquer)”** 和利用操作的 **“代数性质 (Algebraic Properties)”**，尤其是 **“结合性 (Associativity)”**。

-
**分治 (Divide-and-Conquer)：**将大问题分解成若干个独立的、可以并行处理的子问题。每个子问题独立求解后，再将结果合并。这天然地契合了并行的思想。 -
**结合性 (Associativity)：**如果一个操作 ⊕ 满足结合律，即 (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)，那么在合并子问题的结果时，合并的顺序就不重要了。这给予了并行执行极大的“自由度”。例如，加法 + 和乘法 * 都满足结合律。

让我们用 Go 来实践一下这种思想，改造上面的求和函数。

**Go 实践 1：基于 Goroutine 和 Channel 的分块并行求和**

我们可以将数组切分成若干块 (chunk)，每个 Goroutine 负责计算一块的和，最后将各块的结果汇总。

```
import (
"runtime"
"sync"
)
func sumParallelChunks(nums []int, numChunks int) int64 {
if len(nums) == 0 { return 0 }
if numChunks <= 0 { numChunks = runtime.NumCPU() } // 默认使用CPU核心数作为块数
if len(nums) < numChunks { numChunks = len(nums) }
results := make(chan int64, numChunks)
chunkSize := (len(nums) + numChunks - 1) / numChunks
for i := 0; i < numChunks; i++ {
start := i * chunkSize
end := (i + 1) * chunkSize
if end > len(nums) { end = len(nums) }
// 每个goroutine处理一个独立的块
go func(chunk []int) {
var localSum int64 = 0
for _, n := range chunk { // 块内部仍然是顺序累加，但这是局部行为
localSum += int64(n)
}
results <- localSum // 将局部结果发送到channel
}(nums[start:end])
}
var total int64 = 0
for i := 0; i < numChunks; i++ {
total += <-results // 合并结果，加法是结合的！顺序不重要
}
return total
}
```


**Go 实践 2：递归分治的并行求和 (更纯粹地体现分治)**

对于分治思想，递归往往是更自然的表达：

```
// 辅助函数，保持接口一致性
func sumRecursiveParallelEntry(nums []int) int64 {
// 设定一个阈值，小于此阈值则顺序计算，避免过多goroutine开销
const threshold = 1024
return sumRecursiveParallel(nums, threshold)
}
func sumRecursiveParallel(nums []int, threshold int) int64 {
if len(nums) == 0 { return 0 }
if len(nums) < threshold {
return sumSequential(nums) // 小任务直接顺序计算
}
mid := len(nums) / 2
var sumLeft int64
var wg sync.WaitGroup
wg.Add(1) // 我们需要等待左半部分的计算结果
go func() {
defer wg.Done()
sumLeft = sumRecursiveParallel(nums[:mid], threshold)
}()
// 右半部分可以在当前goroutine计算，也可以再开一个goroutine
sumRight := sumRecursiveParallel(nums[mid:], threshold)
wg.Wait() // 等待左半部分完成
return sumLeft + sumRight // 合并，加法是结合的
}
```


## 基准测试：并行真的更快吗？

理论归理论，实践是检验真理的唯一标准。我们为上述三个求和函数编写了基准测试，在一个典型的多核开发机上运行（例如，4 核 8 线程的 CPU）。我们使用一个包含 1000 万个整数的切片作为输入。

```
// benchmark_test.go
package main
import (
"math/rand"
"runtime"
"testing"
"time"
)
var testNums []int
func init() {
rand.Seed(time.Now().UnixNano())
testNums = make([]int, 10000000) // 10 million numbers
for i := range testNums {
testNums[i] = rand.Intn(1000)
}
}
func BenchmarkSumSequential(b *testing.B) {
for i := 0; i < b.N; i++ {
sumSequential(testNums)
}
}
func BenchmarkSumParallelChunks(b *testing.B) {
numChunks := runtime.NumCPU()
b.ResetTimer()
for i := 0; i < b.N; i++ {
sumParallelChunks(testNums, numChunks)
}
}
func BenchmarkSumRecursiveParallel(b *testing.B) {
for i := 0; i < b.N; i++ {
sumRecursiveParallelEntry(testNums)
}
}
```


**典型的基准测试结果可能如下 (具体数字会因机器而异)：**

```
$go test -bench .
goos: darwin
goarch: amd64
pkg: demo
cpu: Intel(R) Core(TM) i5-8257U CPU @ 1.40GHz
BenchmarkSumSequential-8 429 2784507 ns/op
BenchmarkSumParallelChunks-8 520 1985197 ns/op
BenchmarkSumRecursiveParallel-8 265 4420254 ns/op
PASS
ok demo 4.612s
```


从结果可以看出：

- sumSequential 作为基线，但顺序版本的速度并非最慢。
- sumParallelChunks 显著快于顺序版本，它充分利用了多核 CPU 的优势，并在这个特定场景下可能因为更直接的控制和较少的递归开销而略胜一筹，但这取决于具体实现和输入规模。而sumRecursiveParallel虽是并行，但却因为较多的goroutine调度(数量大于机器核数)与递归的开销拖慢了执行的速度。

## 分治与性能：并非总是“更快”的银弹

看到上面的基准测试，你曾经认为的“分治 + 并行”总是能带来性能提升的结论是不成立的。**然而，这里需要强调：分治策略本身是为了“能够”并行化，而不是保证在所有情况下都比聪明的顺序算法更快。**

这是因为并行化是有成本的：

**任务分解与合并开销：**将问题分解、分发给 Goroutine、以及最后合并结果都需要时间。**Goroutine 创建与调度开销：**虽然 Go 的 Goroutine 很轻量，但创建和调度百万个 Goroutine 仍然有不可忽视的开销。这就是为什么在 sumRecursiveParallel 中我们设置了一个 threshold，当问题规模小于阈值时，退化为顺序执行。**通信开销：**Channel 通信比直接的函数调用要慢。**同步开销：**如果子问题间不是完全独立，或者合并过程复杂，可能需要额外的同步（如 sync.WaitGroup 或互斥锁），这也会引入开销。

**因此，“分治”的性能优势通常在以下情况才能显现：**

**问题规模足够大：**大到足以摊平并行化的固定开销。**子问题真正独立：**减少或避免同步需求。**合并操作高效：**合并步骤不能成为新的瓶颈。**有足够的并行资源：**即拥有足够的多核 CPU 来同时执行子任务。

如果问题规模很小，或者并行化引入的开销大于节省的时间，那么精心优化的顺序算法可能反而更快。Steele 的核心观点在于，**采用分治和关注独立性的设计，使得你的程序具备了“可并行化”的潜力，当资源允许且问题规模合适时，就能获得加速。更重要的是，这种设计往往更清晰、更易于推理和维护。**

## “独立性”是核心，而非“并行”本身

Steele 强调：“问题的核心并非并行本身，而是独立性。”

如果我们能够将问题分解成独立的部分，并且定义出具有良好代数性质（如结合性）的合并操作，那么并行化就成了一件相对自然和简单的事情。语言和运行时可以更好地帮助我们调度这些独立的任务。

这里，你可能会觉得 Steele 的思想与另一位 Go 圈尽人皆知的思想领袖 Rob Pike 的名言“Concurrency is not Parallelism”有异曲同工之妙。确实如此！

他们都在强调开发者应将关注点从底层执行细节提升到更高层次的程序结构设计上。一个结构良好的程序，自然就具备了高效执行的潜力。

**Pike 说：**不要去想“并行”(Parallelism)。去想“并发”(Concurrency)——如何把你的程序组织成一组可独立执行、通过通信来协作的组件（Goroutines）。**Steele 说：**不要去想“并行”(Parallelism)。去想“独立性”(Independence)——如何把你的问题分解成独立的子问题，并找到一个满足结合律的合并操作。

他们的思想完美互补：

**Pike 的思想为我们提供了构建程序的“骨架”**：我们使用 goroutine 和 channel 来搭建并发结构。**Steele 的思想则为我们填充了“血肉”**：我们确保每个 goroutine 的工作是真正**独立的**，并且我们用来合并结果的操作是**结合性的**。

例如，我们的并行求和示例，正是用 Goroutine（Pike 的工具）来执行独立的求和任务（Steele 的独立性原则），然后用 + 这个结合性操作来合并结果。一个优秀的 Gopher，脑中应该同时有这两个声音在对话。

## Gopher 的思维重塑：从“怎么做”到“是什么”

Steele 的思想，鼓励我们从更本质的层面思考问题：

**关注“是什么 (What)”而非“怎么做 (How)”：**就像数学家写 Σxᵢ 一样，先声明意图（求和），而不是一开始就陷入具体的循环和累加步骤。Fortran 90 的 SUM(X) 就是这种思想的体现。**寻找结合性的合并操作：**对于一个问题，思考能否将其分解，并找到一个满足结合律的合并方法。这往往需要对问题域有更深的理解。Steele 在 PPT 中展示了如何通过定义 WordState 及其结合性的 ⊕ 操作来并行化“字符串分词”问题，非常精彩。**拥抱不可变性与纯函数：**尽可能使子问题的处理函数是纯函数（无副作用，相同输入总有相同输出），这能极大地简化并行程序的推理。**可复现性至关重要：**Steele 强调，为了调试，可复现性极其重要，甚至值得牺牲一些性能。具有结合性的操作通常更容易保证结果的可复现性（即使并行执行顺序不同，最终结果也应一致）。

## 小结：让并行“自然发生”——Go 做到了吗？

Guy L. Steele Jr. 的思想提醒我们，真正的并行编程高手，不是那些能玩转各种复杂锁和同步原语的“技巧大师”，而是那些能洞察问题本质，将其分解为独立单元，并用优雅的代数方式重新组合的人。他的理想是让并行性像内存管理（垃圾回收）一样，成为语言和运行时为我们处理好的事情，让开发者可以更专注于业务逻辑本身。

**那么，Go 语言在“让并行自然发生”这条路上走了多远呢？**

-
**显著进步：**相比于 C/C++/Java 等需要手动管理线程、锁、条件变量的语言，Go 通过 go 关键字启动 Goroutine，并通过 Channel 进行通信和同步，极大地简化了并发编程的门槛和心智负担。可以说，Go 让“思考独立性”和“实现基本并发”变得前所未有地容易。 -
**尚未完全“自动化”：**尽管如此，Go 的并行还远未达到像垃圾回收那样“开发者无感知”的程度。开发者仍然需要：**主动设计并行策略：**如何分解问题（如分块、递归分治），如何选择合适的并发原语（Channel, WaitGroup, Mutex）。**管理并发单元：**决定启动多少 Goroutine，如何处理它们的生命周期和错误。**关注数据竞争：**虽然 Channel 有助于避免数据竞争，但如果共享了内存且没有正确同步，数据竞争依然是 Gopher 需要面对的问题（Go 的 race detector 是一个好帮手）。**理解并选择合并策略：**如何设计具有良好代数性质的合并操作，这仍依赖于开发者的洞察力。

-
**与其他语言的比较：****Erlang/Elixir (Actor Model)：**在进程隔离和消息传递方面与 Go 的 CSP 有相似的哲学，也致力于简化并发。它们在容错和分布式方面有独特优势。**函数式语言 (Haskell, Clojure)：**它们强调的不可变性和纯函数天然适合并行化，并提供了一些高级的并行集合与抽象。**Rust：**通过其所有权系统和 Send/Sync trait，在编译期提供了强大的内存安全和线程安全保证。其 async/await 提供了另一种并发模型。Rust 在追求极致性能和安全性的同时，其并发的学习曲线也相对陡峭。


**Go 的优势在于其务实的平衡：** 它提供了足够简单且强大的并发原语，使得开发者能够以较低的成本实现高效的并发和并行，尤其适合构建网络服务和分布式系统。它鼓励开发者思考任务的独立性，但将“如何并行”的许多细节交由开发者根据具体场景来设计。

最终，要达到 Steele 的理想境界——让并行编程像呼吸一样自然，还需要语言、运行时甚至硬件层面的持续进化。但 Go 毫无疑问地在这个方向上迈出了坚实而重要的一大步，它为我们 Gopher 提供了一套强大的工具，去实践“不去想并行（细节），而去思考独立性与组合”的编程智慧。

你对 Guy Steele 的这些观点有什么看法？在你的 Go 并行编程实践中，是否也曾遇到过“累加器思维”带来的困扰，或者通过“分治”获得了更好的解决方案？欢迎在评论区分享你的经验和思考！

参考资料地址 – https://www.infoq.com/presentations/Thinking-Parallel-Programming/

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/ab2d7a5176ba4b48.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论