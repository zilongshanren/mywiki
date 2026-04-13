---
title: 一文搞懂Go subtest
url: https://tonybai.com/2023/03/15/an-intro-of-go-subtest/
published: '2023-03-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一文搞懂Go subtest

![](../../assets/575f8251b424747c.png)


注：本篇首图片基于

[lexica AI]生成的图片二次加工而成。

[本文永久链接](https://tonybai.com/2023/03/15/an-intro-of-go-subtest) – https://tonybai.com/2023/03/15/an-intro-of-go-subtest

[单元测试(unit testing)](https://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)是软件开发中至关重要的一环，它存在的意义包括但不限于如下几个方面：

- 提高代码质量：单元测试可以确保代码的正确性、可靠性和稳定性，从而减少代码缺陷和bug。
- 减少回归测试成本：在修改代码时，单元测试可以快速检查是否影响了其他模块的功能，避免了整个系统的回归测试成本。
- 促进团队合作：单元测试可以帮助团队成员更好地理解和使用彼此编写的代码，提高代码的可读性和可维护性。
- 提高开发效率：单元测试可以自动化执行测试，减少手动测试的时间和工作量，从而提高开发效率。

Go语言设计者在Go设计伊始就决定语言特性与环境特性“两手都要抓，两手都要硬”，事实证明：** Go的成功正是因为其对工程软件项目整体环境的专注**。而Go内置轻量级测试框架这一点也正是Go重视环境特性的体现。并且，Go团队对这一内置测试框架的投入是持续的，不断有更便捷的、更灵活的新特性加入Go测试框架中，可以帮助Gopher更好地组织测试代码，更高效地执行测试等。

Go在[Go 1.7版本](https://tonybai.com/2016/06/21/some-changes-in-go-1-7)引入的subtest就是一个典型的代表，subtest的加入使得Gopher可以更灵活地应用内置go test框架。

在本文中，我将结合日常开发中了解到的关于subtest的认知、理解和使用的问题，和大家一起聊聊subtest。

## 一. Go单元测试回顾

在Go语言中，单元测试被视为**一等公民**，结合Go内置的轻量级测试框架，Go开发者可以很方便的编写单元测试用例。

Go的单元测试通常放在与被测试代码相同的包中，单元测试所在源文件以_test.go结尾，这个Go测试框架要求的。测试函数以Test为前缀，接受一个*testing.T类型的参数，并使用t.Error、t.Fail以及t.Fatal等方法来报告测试失败。使用go test命令即可运行所有的测试代码。如果测试通过，则输出一条消息表示测试成功；否则输出错误信息，指出哪些测试失败了。

注：Go还支持基准测试、example测试、

[模糊测试]等，以便进行性能测试和文档生成，但这些不是这篇文章所要关注的内容。

注：t.Error <=> t.Log+t.Fail

通常编写Go测试代码时，我们首先会考虑top-level test。

## 二. Go top-level test

上面提到的与被测源码在相同目录下的*_test.go中的以Test开头的函数就是Go top-level test。在*_test.go可以定义一个或多个以Test开头的函数用于测试被测源码中函数或方法。例如：

```
// https://github.com/bigwhite/experiments/blob/master/subtest/add_test.go
// 被测代码，仅是demo
func Add(a, b int) int {
return a + b
}
// 测试代码
func TestAdd(t *testing.T) {
got := Add(2, 3)
if got != 5 {
t.Errorf("Add(2, 3) got %d, want 5", got)
}
}
func TestAddZero(t *testing.T) {
got := Add(2, 0)
if got != 2 {
t.Errorf("Add(2, 0) got %d, want 2", got)
}
}
func TestAddOppositeNum(t *testing.T) {
got := Add(2, -2)
if got != 0 {
t.Errorf("Add(2, -2) got %d, want 0", got)
}
}
```


注：“got-want”是Go test中在Errorf中常用的命名惯例


top-level test的执行有如下特点：

- go test会将每个TestXxx放在
**单独的goroutine中执行，保持相互的隔离**； - 某个TestXxx用例未过，通过Errorf，甚至是Fatalf输出错误结果，都不会影响到其他TestXxx的执行；
- 某个TestXxx用例中的某个结果判断未过，如果通过Errorf输出错误结果，则该TestXxx会继续执行；
- 不过，如果TestXxx使用的是Fatal/Fatalf，这会导致该TestXxx的执行在调用Fatal/Fatalf的位置立即结束，TestXxx函数体内的后续测试代码将不会得到执行；
- 默认各个TestXxx按声明顺序逐一执行，即便它们是在各自的goroutine中执行的；
- 通过go test -shuffle=on可以让各个TestXxx按随机次序执行，这样可以检测出各个TestXxx之间是否存在执行顺序的依赖，我们要避免在测试代码中出现这种依赖；
- 通过“go test -run=正则式”的方式，可以选择执行某些TestXxx。
- 各个TestXxx函数可以调用t.Parallel方法(即testing.T.Parallel方法)来将TestXxx加入到可并行执行的用例集合中，注意：加入到并行执行集合后，这些TestXxx的执行顺序就不确定了。

结合属于Go最佳实践的表驱动(table-driven)测试(如下面代码TestAddWithTable所示)，我们可以无需写很多TestXxx，用下面的TestAddWithTable即可实现上面三个TestXxx的等价测试：

```
func TestAddWithTable(t *testing.T) {
cases := []struct {
name string
a int
b int
r int
}{
{"2+3", 2, 3, 5},
{"2+0", 2, 0, 2},
{"2+(-2)", 2, -2, 0},
//... ...
}
for _, caze := range cases {
got := Add(caze.a, caze.b)
if got != caze.r {
t.Errorf("%s got %d, want %d", caze.name, got, caze.r)
}
}
}
```


Go top-level test可以满足大多数Gopher的常规单测需求，表驱动的惯例理解起来也十分容易。

但基于top-level test+表驱动的测试在简化测试代码编写的同时，也会带来一些不足：

- 表内的cases顺序执行，无法shuffle;
- 表内所有cases在同一个goroutine中执行，隔离性差；
- 如果使用fatal/fatalf，那么一旦某个case失败，后面的测试表项(cases)将不能得到执行；
- 表内test case无法并行(parallel)执行；
- 测试用例的组织只能平铺，不够灵活，无法建立起层次。

为此[Go 1.7版本](https://tonybai.com/2016/06/21/some-changes-in-go-1-7)引入了subtest！

## 三. Subtest

Go语言的subtest是指将一个测试函数(TestXxx)分成多个小测试函数，每个小测试函数可以独立运行并报告测试结果的功能。这种测试方式可以更细粒度地控制测试用例，方便定位问题和调试。

下面是一个使用subtest改造TestAddWithTable的示例代码，展示如何使用Go语言编写subtest：

```
// https://github.com/bigwhite/experiments/blob/master/subtest/add_sub_test.go
func TestAddWithSubtest(t *testing.T) {
cases := []struct {
name string
a int
b int
r int
}{
{"2+3", 2, 3, 5},
{"2+0", 2, 0, 2},
{"2+(-2)", 2, -2, 0},
//... ...
}
for _, caze := range cases {
t.Run(caze.name, func(t *testing.T) {
t.Log("g:", curGoroutineID())
got := Add(caze.a, caze.b)
if got != caze.r {
t.Errorf("got %d, want %d", got, caze.r)
}
})
}
}
```


在上面的代码中，我们定义了一个名为TestAddWithSubtest的测试函数，并在其中使用t.Run()方法结合表测试方式来创建三个subtest，这样每个subtest都可以复用相同的错误处理逻辑，但通过测试用例参数的不同来体现差异。当然你若不使用表驱动测试，那么每个subtest也都可以有自己独立的错误处理逻辑！

执行上面TestAddWithSubtest这个测试用例（我们故意将Add函数的实现改成错误的），我们将看到下面结果：

```
$go test add_sub_test.go
--- FAIL: TestAddWithSubtest (0.00s)
--- FAIL: TestAddWithSubtest/2+3 (0.00s)
add_sub_test.go:54: got 6, want 5
--- FAIL: TestAddWithSubtest/2+0 (0.00s)
add_sub_test.go:54: got 3, want 2
--- FAIL: TestAddWithSubtest/2+(-2) (0.00s)
add_sub_test.go:54: got 1, want 0
```


我们看到：在错误信息输出中，每个失败case都是以“TestXxx/subtestName”标识，我们可以很容易地将其与相应的代码行对应起来。更深层的意义是subtest让整个测试组织形式有了“层次感”！通过-run标志位，我们便能够以这种“层次”选择要执行的某个top-level test的某个/某些Subtest：

```
$go test -v -run TestAddWithSubtest/-2 add_sub_test.go
=== RUN TestAddWithSubtest
=== RUN TestAddWithSubtest/2+(-2)
add_sub_test.go:51: g: 19
add_sub_test.go:54: got 1, want 0
--- FAIL: TestAddWithSubtest (0.00s)
--- FAIL: TestAddWithSubtest/2+(-2) (0.00s)
FAIL
FAIL command-line-arguments 0.006s
FAIL
```


我们来看看subtest有哪些特点(可以和前面的top-level test对比着看)：

- go subtest也会放在
**单独的goroutine中执行，保持相互的隔离**； - 某个Subtest用例未过，通过Errorf，甚至是Fatalf输出错误结果，都不会影响到同一TestXxx下的其他Subtest的执行；
- 某个Subtest中的某个结果判断未过，如果通过Errorf输出错误结果，则该Subtest会继续执行；
- 不过，如果subtest使用的是Fatal/Fatalf，这会导致该subtest的执行在调用Fatal/Fatalf的位置立即结束，subtest函数体内的后续测试代码将不会得到执行；
- 默认各个TestXxx下的subtest将按声明顺序逐一执行，即便它们是在各自的goroutine中执行的；
- 到目前为止，subtest
**不支持shuffle方式的随机序执行**； - 通过“go test -run=TestXxx/正则式[/...]”的方式，我们可以选择执行TestXxx下的某个或某些subtest；
- 各个subtest可以调用t.Parallel方法(即testing.T.Parallel方法)来将subtest加入到可并行执行的用例集合中，注意：加入到并行执行集合后，这些subTest的执行顺序就不确定了。

综上，subtest的优点可以总结为以下几点：

- 更细粒度的测试：通过将测试用例分成多个小测试函数，可以更容易地定位问题和调试。
- 可读性更好：subtest可以让测试代码更加清晰和易于理解。
- 更灵活的测试：subtest可以根据需要进行组合和排列，以满足不同的测试需求。
- 更有层次的组织测试代码：通过subtest可以设计出更有层次的测试代码组织形式，更方便地共享资源和在某一组织层次上设置setup与teardown，我的
[《Go语言精进之路》vol2](https://book.douban.com/subject/35720729/)的第41条“有层次地组织测试代码”对这方面内容有系统说明，大家可以参考。

## 四. Subtest vs. top-level test

top-level test自身其实也是一种subtest，只是在它的调度与执行是由Go测试框架掌控的的，对我们开发人员并不可见。

对于gopher而言：

- 简单的包的测试在top-level test中就可以满足，直接、直观、易懂。
- 对于稍大一些的工程中的复杂包来说，一旦涉及到测试代码组织的层次设计时，subtest的组织性、灵活性和可扩展性便可以更好地的帮助我们提高测试效率和减少测试时间。

注：本文少部分内容来自于

[ChatGPT]生成的答案。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/blob/master/subtest)下载。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论