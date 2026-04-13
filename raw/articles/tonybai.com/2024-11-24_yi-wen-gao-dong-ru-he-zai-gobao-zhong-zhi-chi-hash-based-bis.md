---
title: 一文搞懂如何在Go包中支持Hash-Based Bisect调试
url: https://tonybai.com/2024/11/24/how-to-support-hash-based-bisect-in-go-package/
published: '2024-11-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一文搞懂如何在Go包中支持Hash-Based Bisect调试

![](../../assets/3fc5850b83f7548c.png)


[本文永久链接](https://tonybai.com/2024/11/24/how-to-support-hash-based-bisect-in-go-package) – https://tonybai.com/2024/mm/dd/how-to-support-hash-based-bisect-in-go-package

bisect是一个英文动词，意为“二分”或“分成两部分”。在数学和计算机科学中，通常指将一个区间或一个集合分成两个相等的部分。

对于程序员来说，最熟悉的bisect应用莫过于下面两个：

- 算法中的二分查找(binary search)

二分查找是一个经典且高效的查找算法，任何一本介绍数据结构或计算机算法的书都会包含对二分查找的系统说明。所谓二分查找就是通过不断将搜索区间一分为二来找到目标值。一些排序算法也应用了bisect的思想，比如快速排序(QuickSort)等。

- git bisect

git bisect是一个非常实用的Git命令，它通过二分查找的方式有效缩小可能导致错误的提交范围，帮助开发人员快速定位引入错误的提交。其工作原理是反复从版本控制系统中检出不同的提交并运行测试，将结果标记为“good”或“bad”。这个过程持续进行，直到找到引入bug的具体提交(bad commit)：

![](../../assets/fd0a5957c74bdb1d.png)


git bisect特别适用于当你怀疑某个bug是由于代码库历史中的特定更改引起时，这种情况在日常开发中非常常见。

然而，并非所有的bug都能通过git bisect查找出来。尤其在编译器、运行时库以及大型复杂项目中，问题往往潜藏在难以排查的调用栈、数据流或代码路径中。在这些情况下，git bisect这种传统的工具可能会显得力不从心。

注：如果你还不熟悉git bisect的使用方法，可以参考本文后面附录中的入门示例。


在今年7月份，Go团队前技术主管Russ Cox在他的博客上发表了一篇题为“[Hash-Based Bisect Debugging in Compilers and Runtimes](https://research.swtch.com/bisect)”的文章，介绍了Go编译器和运行时团队内部使用的高级调试技术——Hash-Based Bisect。这一技术为我们提供了一种全新的问题定位方式。

在这篇文章中，我将带领大家深入了解Hash-Based Bisect这一高级调试技术，探索如何让我们自己的Go包支持这一调试技术，以及如何在日常开发中帮助我们快速定位一些难以排查的潜在问题。

## 1. Hash-Based Bisect是什么

前面提到过，git bisect常用于代码提交历史的回归问题排查。然而，当问题不是由提交历史引发，而是涉及程序行为的动态变化时，git bisect便显得无能为力。例如：

- 某些代码路径或优化规则在特定运行时触发错误。
- 测试程序在调用栈中的某些路径上表现异常。
- 多线程或并行执行中，因运行时调度导致的问题。

Hash-Based Bisect正是为了解决这些问题而设计的。它突破了静态版本的局限，将调试范围扩展到了动态行为层面。

那么Hash-Based Bisect究竟是什么技术呢？它是一种基于哈希值和二分搜索的调试技术，旨在快速定位复杂程序中导致问题的最小变化点集合。通过为代码中的变化点（如函数、行号或调用栈）生成唯一的哈希值，该技术将程序行为映射到这些标识符上。接着，通过逐步启用或禁用特定变化点，结合测试程序的运行结果，递归缩小问题范围，最终定位问题根源(某几行代码甚至是某一行代码)：

![](../../assets/212758e98c9b283c.png)


与git bisect专注于找到引入错误的提交不同，**基于散列的bisect不会去遍历版本历史，而是直接对代码的结构和执行流进行操作**，其调试的结果也不会与特定提交相关，而是与代码与特定执行路径或功能的交互相关，即**精确定位特定的代码行，函数调用，甚至是触发失败的调用堆栈**。

下面我们再来仔细说明一下该技术的工作原理。

## 2. Hash-Based Bisect的工作原理

Hash-Based Bisect的核心在于利用哈希值为程序的变化点（如函数、代码行、调用栈等）分配唯一标识，并通过二分搜索算法，逐步缩小问题范围。它通过动态启用或禁用这些变化点，结合测试结果判断问题是否被触发，从而定位导致问题的最小变化集。

这个方法有两个关键要素：

- 变化点的唯一标识

在Russ Cox的文章中，他提及了一些传统的二分方法，比如List-Based Bisect-Reduce、Counter-Based Bisect-Reduce等，但这些方法存在编号顺序不稳定、多变化点调试困难、扩展性有限以及不适合并发或动态场景等问题。

而通过哈希函数生成变化点的标识，确保无论代码执行顺序、环境或并发情况如何，变化点的标识始终唯一且稳定的。同时输入更为简洁，通过简短的哈希模式（如001+110），避免长列表或复杂编号，并且可适配多种问题类型（优化规则、运行时行为、动态调用栈等）。

- 二分搜索

利用二分搜索算法在运行时动态启用和禁用变化点，高效缩小问题范围，减少需要手动排查的复杂度。

下面我们再通过Hash-Based Bisect的典型工作流程来进一步理解它的原理。

首先是**定义变化点**。

将程序中可能导致问题的变化点抽象出来，比如：

- 函数（函数名、文件路径）
- 代码行（文件路径和行号）
- 调用栈（运行时捕获）

接下来，**生成变化点的唯一哈希值**。

以Go当前的[hash-based bisect工具](https://github.com/golang/tools/tree/master/cmd/bisect)以及支持该工具调试的Go包为例，对于每个变化点，Go包需要通过bisect.Hash方法生成哈希值，用于唯一标识。例如：

```
id := bisect.Hash("foo.go", 10) // 生成foo.go文件第10行的唯一标识。
```


第三步，**利用二分搜索进行自动的递归测试**。具体来说，就是通过二分搜索逐步启用或禁用变化点：

- 启用一个变化点集合，运行测试程序，观察是否触发问题。
- 根据测试结果缩小范围，继续递归，直到找到最小变化点集合。

最后，**报告变化点**，即最终输出导致问题的最小变化集，帮助开发者快速定位问题。

Russ Cox文章中给了一个“某个函数的编译优化规则导致测试失败”的例子，例子中包含一组数学函数：

```
add, cos, div, exp, mod, mul, sin, sqr, sub, tan
```


要针对这个问题场景使用hash-based bisect进行调试，第一步就是要**定义函数变化点**，并为每个变化点生成唯一哈希值标识：

```
add: 00110010
cos: 00010000
sin: 11000111
...
```


然后启用二分搜索，利用Hash-Based Bisect工具依次禁用某些函数的优化，逐步缩小范围。例如：

```
第一步：禁用add, cos, div, exp, mod，测试通过。
第二步：禁用mul, sin, sqr, sub, tan，测试失败。
第三步：进一步细分，最终定位sin为导致问题的函数。开发者只需检查该函数的优化规则即可解决问题。
```


原文章中，Russ Cox利用函数变化点哈希值的位后缀构建了一颗二叉树(如下图)，并利用后缀模式的不同进行问题定位：

![](../../assets/198933c7d28a09fa.png)



了解了大致的工作原理后，我们再来看看Hash-Based Bisect在Go项目中的使用现状。

## 3. Hash-Based Bisect在Go项目中的使用现状

目前Hash-Based Bisect已经成为Go项目编译器和运行时的重要调试工具之一，其工具链(golang.org/x/tools/cmd/bisect)和库(golang.org/x/tools/internal/bisect)提供了强大的功能支持，帮助Go团队在编译器开发、运行时库升级和语言特性修改等场景下快速定位问题。

Go实现的hash-based bisect调试技术包含两部分：

bisect命令行工具可用于驱动测试运行（如go test）并自动化调试过程，支持灵活的模式定义（如-godebug、-compile选项），结合用户输入定位问题点。

- golang.org/x/tools/internal/bisect包

该包为库和工具开发者提供一个接口，轻松实现与bisect工具的集成。并且提供了哈希生成、启用判断和变化点报告等功能，适配复杂调试需求。

上述工具目前在Go编译器的SSA（静态单赋值）后端开发、Go运行时库升级（比如[Go 1.23的Timer Stop/Reset的新实现](https://github.com/golang/go/issues/37196)）以及语言特性的修改（比如[loopvar语义变更](https://tonybai.com/2023/08/20/some-changes-in-go-1-21)）等方面都有重要的应用，大大提高了Go团队在定位复杂问题时的调试效率。

以上工具和包在Go项目中已经演化多年，颇为成熟。[Russ Cox已经发起提案#67140](https://github.com/golang/go/issues/67140)，旨在将golang.org/x/tools/internal/bisect包发布为标准库debug/bisect包，这样编译器、运行时、标准库甚至标准库之外的包都可以基于它提供的功能实现与bisect工具的兼容，并利用bisect工具实现基于变更点hash值的高级调试。

讲到这里，屏幕前的你是否已经感到“迫不及待”了呢？这样优秀的工具！我们现在能否使用它？是否可以将其应用于我们自己的Go包的调试过程中呢？接下来，我就来用一个示例演示一下如何让我们自己的包支持Go bisect工具，以帮助我们提升调试效率。

## 4. 让你的库支持Hash-Based Bisect调试

要利用bisect调试技术，我们首先要解决的是bisect包位于internal中的问题，好在Russ Cox在实现bisect包时考虑了这个问题，bisect包没有任何外部依赖，连Go标准库都不依赖，这样避免了后续变为debug/bisect后导致标准库循环依赖的问题。现在，我们可以将它直接copy出来，放到我们自己的工程中使用。

下面是我准备的示例的目录结构：

```
$tree -F hash-based-bisect/bisect-demo
hash-based-bisect/bisect-demo
├── bisect/
│ └── bisect.go
├── foo/
│ ├── foo.go
│ └── foo_test.go
└── go.mod
```


其中bisect目录下的bisect.go来自github.com/golang/tools/blob/master/internal/bisect/bisect.go，foo包是我们这次要调试的目标包，我们先来看看foo.go的代码：

```
// bisect-demo/foo/foo.go
package foo
import (
"bisect-demo/bisect"
"flag"
)
var (
bisectFlag = flag.String("bisect", "", "bisect pattern")
matcher *bisect.Matcher
)
// Features represents different features that might cause issues
const (
FeatureRangeIteration = "range-iteration" // Using range vs classic for loop
FeatureConcurrentLogic = "concurrent-logic" // Adding concurrent modifications
)
func Init() {
flag.Parse()
if *bisectFlag != "" {
matcher, _ = bisect.New(*bisectFlag)
}
}
func ProcessItems(items []int) []int {
result := make([]int, 0, len(items))
// First potential problematic change: different iteration approach
id1 := bisect.Hash(FeatureRangeIteration)
if matcher == nil || matcher.ShouldEnable(id1) {
if matcher != nil && matcher.ShouldReport(id1) {
println(bisect.Marker(id1), "enabled feature:", FeatureRangeIteration)
}
// Potentially problematic implementation using range
for i := range items {
result = append(result, items[i]*2)
}
} else {
// Correct implementation using value iteration
for _, v := range items {
result = append(result, v*2)
}
}
// Second potential problematic change: concurrent modifications
id2 := bisect.Hash(FeatureConcurrentLogic)
if matcher == nil || matcher.ShouldEnable(id2) {
if matcher != nil && matcher.ShouldReport(id2) {
println(bisect.Marker(id2), "enabled feature:", FeatureConcurrentLogic)
}
// Potentially problematic implementation with concurrency
for i := 0; i < len(result); i++ {
go func(idx int) {
result[idx] += 1 // Race condition
}(i)
}
}
return result
}
```


大家可以结合前面提及的Hash-Based Bisect的典型工作流程来理解上面的代码。

首先，我们模拟可能导致问题的两个功能特性并定义了变化点，变化点由特性标识符的hash值标识，这里我们定义的特性标识符为：

```
const (
// 使用有意义的特性名称作为 hash 的输入
FeatureRangeIteration = "range-iteration" // 使用 range vs 经典 for 循环
FeatureConcurrentLogic = "concurrent-logic" // 添加并发修改逻辑
)
```


接下来，对于每个可能有问题的变化点，都遵循相同的模式：

```
// 1. 计算特性的唯一Hash值
id1 := bisect.Hash(FeatureRangeIteration)
// 2. 检查是否应该启用该特性
if matcher == nil || matcher.ShouldEnable(id1) {
// 3. 如果需要,报告该特性被启用
if matcher != nil && matcher.ShouldReport(id1) {
println(bisect.Marker(id1), "enabled feature:", FeatureRangeIteration)
}
// 4. 执行可能有问题的实现
for i := range items {
result = append(result, items[i]*2)
}
} else {
// 5. 执行正确的实现
for _, v := range items {
result = append(result, v*2)
}
}
```


这里对matcher == nil的检查算是一个小优化：当不在bisect调试模式时，matcher为nil。此时我们直接启用所有特性，不需要计算hash和调用其他方法。

代码中的ShouldEnable()决定是否启用该特性的代码，ShouldReport() 决定是否需要报告该特性被启用。这两个可能返回不同的值，尤其是在bisect搜索最小失败集合时。

Marker()用于生成标准格式的匹配标记，这些标记会被bisect工具用来识别和追踪启用了哪些特性，标记会在最终输出中被移除，只显示实际的描述文本。

这里还有一个接收bisect pattern的设置，我们是通过命令行参数来接收bisect每次传给foo包的Pattern的，这里我们在Init函数，而不是init函数中调用Parse，是因为如果在init函数中调用Parse，会干扰go test测试框架，导致出现类似“flag provided but not defined: -test.paniconexit0”的测试执行错误。

下面是foo_test.go的代码：

```
// bisect-demo/foo/foo_test.go
package foo
import (
"flag"
"testing"
"time"
)
func TestMain(m *testing.M) {
flag.Parse()
Init()
m.Run()
}
func TestProcessItems(t *testing.T) {
input := []int{1, 2, 3, 4, 5}
result := ProcessItems(input)
// Wait for all goroutines to complete
time.Sleep(1000 * time.Millisecond)
// Verify results
if len(result) != len(input) {
t.Fatalf("got len=%d, want len=%d", len(result), len(input))
}
// Check if results are correct
for i, v := range input {
expected := v * 2
if result[i] != expected {
t.Errorf("result[%d] = %d, want %d", i, result[i], expected)
}
}
}
```


显然为了foo包能成功获取命令行参数，我们重写了TestMain，在其中调用了foo.Init函数。

接下来，我们就来执行一下bisect工具，对foo包进行一下调试，你可以通过go install golang.org/x/tools/cmd/bisect@latest安装bisect。此外下面bisect命令行中的PATTERN是一个“占位符”，bisect命令会识别该“占位符”，并将其替换为相应的字符串，这个在bisect的执行过程中你也会看到：

```
// 在hash-based-bisect/bisect-demo/foo目录下执行
$bisect -v go test -v -args -bisect=PATTERN
bisect: checking target with all changes disabled
bisect: run: go test -v -args -bisect=n... ok (0 matches)
bisect: matches:
bisect: run: go test -v -args -bisect=n... ok (0 matches)
bisect: matches:
bisect: checking target with all changes enabled
bisect: run: go test -v -args -bisect=y... FAIL (2 matches)
bisect: matches:
[bisect-match 0xcf0b8943315a7804] enabled feature: range-iteration
[bisect-match 0x4d642a7960e4693f] enabled feature: concurrent-logic
bisect: run: go test -v -args -bisect=y... FAIL (2 matches)
bisect: matches:
[bisect-match 0xcf0b8943315a7804] enabled feature: range-iteration
[bisect-match 0x4d642a7960e4693f] enabled feature: concurrent-logic
bisect: target succeeds with no changes, fails with all changes
bisect: searching for minimal set of enabled changes causing failure
bisect: run: go test -v -args -bisect=+0... ok (1 matches)
bisect: matches:
[bisect-match 0xcf0b8943315a7804] enabled feature: range-iteration
bisect: run: go test -v -args -bisect=+0... ok (1 matches)
bisect: matches:
[bisect-match 0xcf0b8943315a7804] enabled feature: range-iteration
bisect: run: go test -v -args -bisect=+1... FAIL (1 matches)
bisect: matches:
[bisect-match 0x4d642a7960e4693f] enabled feature: concurrent-logic
bisect: run: go test -v -args -bisect=+1... FAIL (1 matches)
bisect: matches:
[bisect-match 0x4d642a7960e4693f] enabled feature: concurrent-logic
bisect: confirming failing change set
bisect: run: go test -v -args -bisect=v+x3f... FAIL (1 matches)
bisect: matches:
[bisect-match 0x4d642a7960e4693f] enabled feature: concurrent-logic
bisect: run: go test -v -args -bisect=v+x3f... FAIL (1 matches)
bisect: matches:
[bisect-match 0x4d642a7960e4693f] enabled feature: concurrent-logic
bisect: FOUND failing change set
--- change set #1 (enabling changes causes failure)
enabled feature: concurrent-logic
---
bisect: checking for more failures
bisect: run: go test -v -args -bisect=-x3f... ok (1 matches)
bisect: matches:
[bisect-match 0xcf0b8943315a7804] enabled feature: range-iteration
bisect: run: go test -v -args -bisect=-x3f... ok (1 matches)
bisect: matches:
[bisect-match 0xcf0b8943315a7804] enabled feature: range-iteration
bisect: target succeeds with all remaining changes enabled
```


简单解读一下这个bisect调试过程的输出。

bisect执行分为几个阶段：

- 初始检查阶段

首先用-bisect=n禁用所有变更进行测试 → 测试通过（ok）

然后用-bisect=y启用所有变更进行测试 → 测试失败（FAIL）

这表明程序在没有任何变更时是正常的，但启用所有变更后会失败。

启用所有变更时观察到两个特性：

```
[bisect-match 0xcf0b8943315a7804] enabled feature: range-iteration
[bisect-match 0x4d642a7960e4693f] enabled feature: concurrent-logic
```


- 二分查找阶段

测试+0（启用第一个变更：range-iteration）→ 测试通过（ok）

测试+1（启用第二个变更：concurrent-logic）→ 测试失败（FAIL）

这个过程帮助定位到具体是哪个变更导致了失败。

- 确认阶段

使用v+x3f 模式再次确认 → 测试失败（FAIL）

明确找到了导致失败的变更集合：

```
--- change set #1 (enabling changes causes failure)
enabled feature: concurrent-logic
---
```


- 最终验证

使用-x3f 模式（禁用确认的问题变更）进行测试 → 测试通过（ok）

确认启用其他所有变更（除了concurrent-logic）时程序都能正常运行。

从中得出调试结论：bisect工具成功定位到**问题出在concurrent-logic特性**上，range-iteration特性是安全的，不会导致测试失败。问题明确是在并发逻辑中的“故意”逻辑导致的，这符合我们的代码实现中的预期问题（在 concurrent-logic 特性中，我们确实故意修改了数据）。

## 5. 小结

在本文中，我们深入探讨了Hash-Based Bisect这一先进的调试技术，特别是在Go语言项目中的应用。Hash-Based Bisect通过为代码的变化点生成唯一的哈希值，结合二分搜索算法，帮助开发者快速定位复杂程序中的问题，超越传统的git bisect方法。我们还详细介绍了其工作原理、在Go项目中的现状，以及如何将这一技术集成到自己的Go库中，以提升调试效率。也许这里的示例也许并不恰当，但已经达成了我向你展示如何使用bisect工具和bisect包的目的。

尽管Hash-Based Bisect在定位复杂问题上表现出色，但感觉其当前设计仍存在一些不足，这些不足可能会影响开发者的使用体验，尤其是在将其集成到Go包或项目时，这个不足主要体现在对代码的侵入性上。为了支持Hash-Based Bisect，Go包需要显式实现与bisect工具交互的协议，包括支持从命令行或环境变量接收bisect传入的模式(pattern)；需要在代码中创建bisect.Matcher对象，并调用ShouldEnable和ShouldReport接口来管理变化点；代码中必须为潜在变化点显式生成唯一的哈希值，并根据需要启用或禁用。

这种显式集成导致代码逻辑被调试相关代码“污染”，增加了代码复杂度和维护成本。对于一些简单的库或项目，开发者可能不愿为调试需求增加这种负担。

在\$GOROOT/src/cmd/compile/internal/base中，编译器相关代码就将bisect封装到了一个HashDebug结构中，一定程度上减少了代码的侵入深度以及手动集成的工作量。

此外，golang.org/x/tools/internal/bisect包尚未正式变为debug/bisect，后续其API是否会发生变化，尚不得而知，本文中的示例代码不保证在后续的Go版本调整后依然能够正确运行。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/hash-based-bisect)下载。

## 6. 参考资料

[Hash-Based Bisect Debugging in Compilers and Runtimes](https://research.swtch.com/bisect)– https://research.swtch.com/bisect[proposal: debug/bisect: publish x/tools/internal/bisect](https://github.com/golang/go/issues/67140)– https://github.com/golang/go/issues/67140[golang.org/x/tools/internal/bisect package](https://pkg.go.dev/golang.org/x/tools/internal/bisect)– https://pkg.go.dev/golang.org/x/tools/internal/bisect[Hacker News- Hash-based bisect debugging in compilers and runtimes](https://news.ycombinator.com/item?id=40995982)– https://news.ycombinator.com/item?id=40995982

## 7. 附录：git bisect使用示例

假设你有一个Go语言项目，并且发现最近的某次提交引入了一个问题（例如，某个测试用例失败了）。你希望使用git bisect找到引入该问题的具体提交。

你的项目目录设计如下：

```
my-go-project/
├── main.go
└── main_test.go
```


我们来建立这个示例项目：

```
// 在hash-based-bisect/git-bisect下面执行
$mkdir my-go-project
$cd my-go-project
$git init
```


创建main.go：

```
// main.go
package main
func main() {
println("Hello, world!")
}
func Add(a, b int) int {
return a + b
}
```


提交变更：

```
$git add main.go
git commit -m "Initial commit with Add function"
[master (root-commit) 16f8736] Initial commit with Add function
1 file changed, 9 insertions(+)
create mode 100644 main.go
```


创建main_test.go：

```
// main_test.go
package main
import "testing"
func TestAdd(t *testing.T) {
if Add(2, 3) != 5 {
t.Error("Expected 5, got something else")
}
}
```


提交变更：

```
$git add main_test.go
git commit -m "Add test for Add function"
[master b7b3c44] Add test for Add function
1 file changed, 9 insertions(+)
create mode 100644 main_test.go
```


故意引入一个bug并提交变更：

```
$sed -i 's/return a + b/return a - b/' main.go
$git commit -am "Introduce a bug in Add function"
[master 977e647] Introduce a bug in Add function
1 file changed, 1 insertion(+), 1 deletion(-)
```


添加一些其他提交（无关的变更）：

```
$echo "// Just a comment" >> main.go
$git commit -am "Add a comment"
[master 25f88b0] Add a comment
1 file changed, 2 insertions(+)
```


这里列出上面所有commit的list，便于后续对照：

```
$git log --oneline
25f88b0 (HEAD -> master) Add a comment
977e647 Introduce a bug in Add function
b7b3c44 Add test for Add function
16f8736 Initial commit with Add function
```


接下来，我们就可以演示git bisect了，先来演示一下手工bisect。

启动git bisect模式：

```
$git bisect start
```


标记当前最新提交为bad：

```
$git bisect bad
```


标记首次提交为good：

```
$git bisect good 16f8736
Bisecting: 0 revisions left to test after this (roughly 1 step)
[977e647e7461c4c03ee25e53728dd743af925f17] Introduce a bug in Add function
```


我们看到git bisect自动切换到一个中间的提交，我们需要验证这次中间提交是否能通过测试：

```
$go test
--- FAIL: TestAdd (0.00s)
main_test.go:7: Expected 5, got something else
FAIL
exit status 1
FAIL github.com/bigwhite/experiments/hash-based-bisect/git-bisect/my-go-project 0.006s
```


测试失败，我们将该提交标记为bad：

```
$git bisect bad
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[b7b3c444f0fd55086e6ce36fb543a136a1611b61] Add test for Add function
```


git bisect又切换到了另外一个中间提交，我们用go test验证是否能通过：

```
$go test
PASS
ok github.com/bigwhite/experiments/hash-based-bisect/git-bisect/my-go-project 0.005s
```


测试通过，我们将这个中间提交标记为good：

```
$git bisect good
977e647e7461c4c03ee25e53728dd743af925f17 is the first bad commit
commit 977e647e7461c4c03ee25e53728dd743af925f17
Author: Tony Bai <bigwhite.cn@aliyun.com>
Date: Fri Nov 24 13:27:08 2024 +0800
Introduce a bug in Add function
:100644 100644 e357c05d933724eb8b7c1aafee34b8f95913355e e65baa0414a2a1f983379c23ac549b7d8b056db3 M main.go
```


我们看到：git bisect找到了一个bad commit，并显示“977e647e7461c4c03ee25e53728dd743af925f17 is the first bad commit”。

结束git bisect模式：

```
$git bisect reset
```


上面的过程可以使用git bisect run进行自动化，而无需中间手动多次的执行go test和标记，下面是一个等价的git bisect过程：

```
$git bisect start
$git bisect bad
$git bisect good 16f8736
Bisecting: 0 revisions left to test after this (roughly 1 step)
[977e647e7461c4c03ee25e53728dd743af925f17] Introduce a bug in Add function
$git bisect run go test
running go test
--- FAIL: TestAdd (0.00s)
main_test.go:7: Expected 5, got something else
FAIL
exit status 1
FAIL github.com/bigwhite/experiments/hash-based-bisect/git-bisect/my-go-project 0.006s
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[b7b3c444f0fd55086e6ce36fb543a136a1611b61] Add test for Add function
running go test
PASS
ok github.com/bigwhite/experiments/hash-based-bisect/git-bisect/my-go-project 0.006s
977e647e7461c4c03ee25e53728dd743af925f17 is the first bad commit
commit 977e647e7461c4c03ee25e53728dd743af925f17
Author: Tony Bai <bigwhite.cn@aliyun.com>
Date: Fri Nov 24 13:27:08 2024 +0800
Introduce a bug in Add function
:100644 100644 e357c05d933724eb8b7c1aafee34b8f95913355e e65baa0414a2a1f983379c23ac549b7d8b056db3 M main.go
bisect run success
$git bisect reset
Previous HEAD position was b7b3c44 Add test for Add function
Switched to branch 'master'
```


我们看到通过git bisect run可以更快速地定位问题，而无需中间的手工操作，这是我们日常开发中主要使用的bisect手段！

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