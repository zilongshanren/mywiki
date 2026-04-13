---
title: Go 1.18新特性前瞻：原生支持Fuzzing测试
url: https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18/
published: '2021-12-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.18新特性前瞻：原生支持Fuzzing测试

![](../../assets/7a1c94763f734735.png)


[本文永久链接](https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18) – https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18

今年6月初，Go官博发表了一篇名为[《Fuzzing is Beta Ready》](https://go.dev/blog/fuzz-beta)的文章，文中称[gotip版本](https://tip.golang.org)已经原生支持[Fuzzing](https://en.wikipedia.org/wiki/Fuzzing)并开始了公测。这意味着Fuzzing将以一等公民(first-class citizen)的身份正式加入到即将于2022年2月发布的[Go 1.18版本](https://mp.weixin.qq.com/s/_4p1wyo3eKEaCU_9GNdkLA)中：

![](../../assets/d17ee7d9990222ea.png)



有了对Fuzzing技术的原生支持后，我相信会有更多代码经过Fuzzing测试，未来不久Go社区的Go代码的安全水平将会得到整体提升。本文我们就来简单聊聊Fuzzing这个Go 1.18版本的新特性。

注意：在Go 1.18版本Beta版发布前要想体验Fuzzing特性，需要自行安装gotip版本，安装方法如下：

```
$go install golang.org/dl/gotip@latest // go 1.17版本及以后使用go install。go 1.16及之前的版本用go get
$gotip download
$gotip version // 验证安装是否ok
```


### 为什么Go要支持Fuzzing

无论是在过去的**单机时代**，还是在今天的云计算时代，亦或是已经出现苗头的人工智能时代，**安全**都是程序员在构建软件过程中必不可少且日益重要的考量因素。

同时，**安全**也是Go语言设计者们在语言设计伊始就为Go设定的一个重要目标。在语言层面，Go提供了很多“安全保障”特性，比如：

- 显式类型转换，不允许隐式转换；
- 针对数组、切片的下标越界访问的检查；
- 不安全代码隔离到unsafe包中，并提供安全使用unsafe包的几条rules；
- go module构建模式内置包hash校验，放置恶意包对程序的攻击；
- 雇佣安全专家，提供高质量且及时更新的crypto包，尽量防止使用第三方加解密包带来的不安全性；
- 支持纯静态编译，避免动态连接到恶意动态库；
- 原生提供方便测试的工具链，并支持测试覆盖率统计。
- … …

进入云原生时代后，Go语言成为了云原生基础设施与云原生服务的头部语言，由Go语言建造的基础设施、中间件以及应用服务支撑着这个世界的很多重要系统的运行，这些系统对安全性的要求不言而喻。尤其是在“输入”方面，这些系统都会被要求：无论用户使用什么本文数据、二进制数据，无论用户如何构造协议包、无论用户提供的文件包含何种内容，系统都应该是安全健壮的，不会因为用户的故意攻击而出现处理异常、被操控，甚至崩溃。

这就需要我们的系统面对任何输入的情况下都能正确处理，但传统的代码review、静态分析、人工测试和自动化的单元测试无法穷尽所有输入组合，尤其是难于模拟一些无效的、意料之外的、随机的、边缘的输入数据。

于是，[Go社区的一些安全方面的专家](https://github.com/dvyukov)就尝试将业界在解决这方面问题的优秀实践引入Go，[Fuzzing技术就是其中最重要的一个](https://tonybai.com/2015/12/08/go-fuzz-intro/)。

### 什么是Fuzzing？

说了这么半天，**啥是Fuzzing**？

Fuzzing，又叫fuzz testing，中文叫做模糊测试或随机测试。其本质上是一种自动化测试技术，更具体一点，它是一种基于随机输入的自动化测试技术，常被用于发现处理用户输入的代码中存在的bug和问题。

在具体实现上，Fuzzing不需要像单元测试那样使用预先定义好的数据集作为程序输入，而是会通过数据构造引擎自行构造或基于开发人员提供的初始数据构造一些随机数据，并作为输入提供给我们的程序，然后监测程序是否出现panic、断言失败、无限循环等。这些构造出来的随机数据被称为**语料(corpus)**。另外Fuzz testing不是一次性执行的测试，如果不限制执行次数和执行时间，Fuzz testing会一直执行下去，因此它也是一种持续测试的技术。

Fuzzing技术形态最初的出现可追溯到[以打孔卡承载的数据作为计算机输入的时代](http://secretsofconsulting.blogspot.com/2017/02/fuzz-testing-and-fuzz-history.html)。那个时候开发人员经常从废纸篓里随便拿出几张打孔卡输入到自己的程序中来验证程序是否可以正确处理这些“随机”的输入。但Fuzzing测试作为一门技术理论走进广大开发者视野是始于1988年的[Barton Miller](http://www.cs.wisc.edu/~bart/fuzz)教授的研究成果，

当时任教于威斯康星大学的Barton Miller教授在高级操作系统研究生班（CS736）上的一个秋季项目中运用了随机测试技术，他通过fuzzing对一个UNIX工具进行测试，为该工具自动生成随机输入和命令行参数。该项目旨在通过快速连续执行大量的随机输入来测试UNIX命令行程序的可靠性，直到它们崩溃。当时Miller团队能够使他们所测试的实用程序中的25%至33%崩溃。然后，他们对每个崩溃的程序进行调试，以确定原因，并对每个检测到的故障进行分类。1990年，Miller团队对外发表了这一成果。自那以后，Fuzzing技术便确定了自己独立的研究分支，并逐渐发展演化到今天。在过去的十多年中，Fuzzing测试的技术水平有了很大的提高，以[AFL(american fuzzy lop)](https://lcamtuf.coredump.cx/afl/)、[AFL++](https://github.com/AFLplusplus/AFLplusplus)、[libFuzzer](https://www.llvm.org/docs/LibFuzzer.html)、[go-fuzz](https://github.com/dvyukov/go-fuzz)、[syzkaller](https://github.com/google/syzkaller)等开源项目为代表的Fuzzing项目已经被各种编程语言的开发人员应用于实践，并且[取得了不错的“战绩”](https://github.com/dvyukov/go-fuzz#trophies)。

Fuzzing是对其他形式的测试、代码审查和静态分析的补充，它通过生成一个有趣的输入语料库，而这些输入几乎不可能用手去想去写出来，因此极易被传统类型的测试所遗漏。Fuzzing可以帮助开发人员发现难以发现的稳定性、逻辑性甚至是安全性方面的错误，特别是当被测系统变得更加复杂时。

更为关键的，也是Fuzzing技术能够流行开来的原因是构建一个Fuzzing测试足够简单。有了上述Fuzzing相关开源工具和开源库的支持，Fuzzing test不再是需要专业知识才能成功使用的技术，并且现代Fuzzing引擎可以更有策略的、更快的、更有效地找到有用的输入语料。

### Go对Fuzzing技术支持的简要回顾

说过将Fuzzing技术引入Go，我们不能不提到一个人，它就是[Go goroutine调度器](https://tonybai.com/2017/06/23/an-intro-about-goroutine-scheduler/)的作者、前Intel Black Belt级工程师，现Google工程师的[Dmitry Vyukov](https://github.com/dvyukov)，它也是Go语言首个fuzzing工具[go-fuzz](https://github.com/dvyukov/go-fuzz)的作者。

2015年的GopherCon大会上，Dmitry Vyukov在其名为“[Go Dynamic Tools]”的presentation中就介绍了[go-fuzz](https://github.com/dvyukov/go-fuzz/blob/master/slides/go-fuzz.slide)。我个人的[gocmpp项目](https://github.com/bigwhite/gocmpp)就是[使用go-fuzz搭建的Fuzz test](http://tonybai.com/2015/12/08/go-fuzz-intro/)。

之后，Dmitry Vyukov发现虽然通过第三方的fuzzing工具可以解决Go开发者关于Fuzzing的部分需求，但有很多功能特性是通过第三方工具无法实现的。2016年，Dmitry Vyukov在Go官方issue列表中创建[“cmd/compile: coverage instrumentation for fuzzing”](https://github.com/golang/go/issues/14565)的issue归纳说明了这些问题，也是从那时开始，Dmitry Vyukov极力推进Fuzzing进入Go原生工具链的。

2017年，Dmitry Vyukov首次提出希望[在Go工具链中原生支持Fuzzing的Proposal](https://docs.google.com/document/u/1/d/1zXR-TFL3BfnceEAWytV8bnzB2Tfp6EPFinWVJ5V4QC8/pub)，并给出了[为什么我们需要在Go工具链的支持下使Fuzzing成为Go开发的标准做法的原因](http://tiny.cc/why-go-fuzz)。

之后，Dmitry还开源了一个名为syzkaller的项目，该项目用Go语言实现了一个针对操作系统内核的Fuzzing引擎。

Dmitry虽然是goroutine调度器的开发者，也是Google员工，但他却不是Go语言团队的一员，也许正是因为这样，又或是Go核心团队对新特性保持的一贯的谨慎态度，该Dmitry的提议一直处理讨论与反馈的状态，直到2020年中旬，Go安全团队的[Katie Hockman](https://github.com/katiehockman)才正式发布了[在Go中原生支持Fuzzing的新提案](https://golang.org/s/draft-fuzzing-design)。

新提案与Dmitry的提案的目标是相同的，都是期望在Go工具链中加入对Fuzzing的原生支持。不同的是，新提案中的API稍微复杂一些，新提案允许以编程方式设置初始语料库的种子语料，并支持字节字符串以外的输入类型，包括原生的基本数据类型(整型、浮点、字符串等)、复合数据类型(数组、map、结构体等)以及实现了BinaryMarshaler/BinaryUnmarshaler或TextMarshaler/TextUnmarshaler接口的自定义类型。

不过Go fuzzing没有如预期加入到[Go 1.17版本](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg)中，再继续打磨了半年后，Go 1.18版本正式接受了原生支持Fuzzing这个特性，Fuzzing成为Go的“一等公民”。

### 如何使用成为Go“一等公民”的Fuzzing

作为普通Go开发人员，我们无需关心Fuzzing引擎是如何实现的，我们只需根据Go提供的Fuzzing API使用就好了。前面也提到过了，Fuzzing技术之所以可以流行到现在，更多也是因为其使用起来十分简单。

Go 1.18将fuzz testing纳入了go test工具链，与单元测试、[性能基准测试](https://www.imooc.com/read/87/article/2439)等一起成为了Go原生测试工具链中的重要成员。

go fuzzing test的测试用例与普通的测试用例(TestXxx)、性能基准测试(BenchmarkXxx)等一样放在xx_test.go中，只不过用例对应的函数名样式换为了FuzzXxx了。一个简单的Fuzzing test用例如下：

```
func FuzzXxx(f *testing.F) {
// 设置种子语料(可选)
// 执行Fuzzing
f.Fuzz(func(t *testing.T, b []byte) {
//... ...
})
}
```


我们通过go test -fuzz命令即可执行所有xx_test.go中以Fuzz为前缀的Fuzz testing用例。不过这里要注意的是go test -fuzz会先进行普通TestXxx的用例执行，之后才会执行FuzzXxx。

我们看到：每个FuzzXxx函数的参数列表是固定的，fuzzing在testing包中新增了一个F结构体类型，其与testing.T、testing.B是类似的，用于表示一次Fuzzing test的执行，结构体变量中存储了此次fuzzing test执行的上下文信息。

FuzzXxx函数的最主要只能就是调用testing.F的Fuzz方法对目标函数/方法执行测试。testing.F的Fuzz方法接受一个函数类型的参数，按照fuzzing提案的说明，该函数的第一个参数必须是*testing.T，后面可以是多个输入参数，且输入参数的类型不局限于传统的byte切片，还可以是上面提到过的原生的基本数据类型(整型、浮点、字符串等)、复合数据类型(数组、map、结构体等)以及实现了BinaryMarshaler/BinaryUnmarshaler或TextMarshaler/TextUnmarshaler接口的自定义类型。

Fuzz方法会根据目标所需的输入参数类型生成fuzzing后的数据，并将这些数据作为输入参数传给其参数代表的函数。

Go开发人员也可以通过testing.F的Add方法为fuzzing过程提供初始的种子语料(seed corpus)，后续fuzzing test会基于这些种子语料进行fuzzing，虽然这不是必须的，但提供与目标处理逻辑相关的种子语料，可能会加速被测目标中问题的暴露。

当然我们也可以不通过testing.F的Add方法来提供种子语料，go fuzzing还允许你通过文件的形式为每个FuzzXxx函数提供种子语料，以FuzzXxx为例，我们可以在testdata/fuzz/FuzzXxx目录下以文件的形式放置其初始语料，比如：

```
// testdata/fuzz/FuzzXxx/corpus1
go test fuzz v1
[]byte("ABC\xa8\x8c\xb3G\xfc")
```


在这个种子语料文件中，第一行go test fuzz v1是go fuzzing要求的文件头，用于标识这是一个种子语料文件，并且使用的编解码器的版本为v1。而下面的一行则是种子语料，其实这行就是一个go代码的片段，fuzzing工具会将其解码后直接作为输入赋值给被测目标。后续的fuzzing过程也是基于这个种子语料的。注意：种子语料可以有很多个，不同语料单独放置在一行中即可。目前，这个种子语料文件需要手工编辑，后续go团队可能会提供相关工具以方便对种子语料文件的编辑，尤其是针对一些二进制数据的种子语料。

下面我们用一个例子来看看如何使用go原生fuzzing。我这里还以我的gocmpp项目为例，对项目中的Submit消息的Unpack方法进行fuzz testing。

我们先来看不提供初始种子语料的情况。

#### 不提供初始种子语料

虽说FuzzXxx测试用例可以与普通用例TestXxx放在一个xxx_test.go文件中，但例子中为了着重强调我们是在写Fuzz testing用例，我们将FuzzXxxx函数放在submit_fuzz_test.go中，下面是不显式提供初始种子语料的FuzzSubmit：

```
// submit_fuzz_test.go
//go:build go1.18
// +build go1.18
package cmpp_test
import (
"testing"
cmpp "github.com/bigwhite/gocmpp"
)
func FuzzSubmit(f *testing.F) {
f.Fuzz(func(t *testing.T, data []byte) {
p := &cmpp.Cmpp2SubmitReqPkt{}
_ = p.Unpack(data)
})
}
```


我们看到，为了兼容go 1.18之前的版本，我们使用build指示符来告诉编译器这个文件只在go 1.18及后续版本才参与编译，这样go 1.17及之前的版本会ignore这个源文件。

使用下面命令我们来运行一下这个fuzz test：

```
$gotip test -v -fuzz .
=== RUN TestTypeString
--- PASS: TestTypeString (0.00s)
... ...
=== RUN TestCmppTerminateRspPktPack
--- PASS: TestCmppTerminateRspPktPack (0.00s)
=== RUN TestCmppTerminateRspUnpack
--- PASS: TestCmppTerminateRspUnpack (0.00s)
=== FUZZ FuzzSubmit
fuzz: elapsed: 0s, gathering baseline coverage: 0/38 completed
fuzz: elapsed: 0s, gathering baseline coverage: 38/38 completed, now fuzzing with 8 workers
fuzz: elapsed: 3s, execs: 403378 (134408/sec), new interesting: 0 (total: 38)
fuzz: elapsed: 6s, execs: 800451 (132348/sec), new interesting: 0 (total: 38)
fuzz: elapsed: 9s, execs: 1104435 (101366/sec), new interesting: 0 (total: 38)
fuzz: elapsed: 12s, execs: 1346809 (80789/sec), new interesting: 0 (total: 38)
fuzz: elapsed: 15s, execs: 1718297 (123747/sec), new interesting: 1 (total: 39)
^Cfuzz: elapsed: 16s, execs: 1771361 (92170/sec), new interesting: 1 (total: 39)
--- PASS: FuzzSubmit (15.59s)
PASS
ok github.com/bigwhite/gocmpp 15.607s
```


通过上面的执行我们得到几点信息；

-
gotip test -fuzz会先进行普通TestXxx的用例执行，之后才会执行FuzzXxx。

-
fuzz testing默认会一直执行下去，直到遇到crash。如果要限制fuzz testing的执行时间，可以使用-fuzztime，比如下面的命令允许fuzz testing只执行10s：


```
$gotip test -v -fuzztime 10s -fuzz .
```


- 覆盖率引导的fuzzing

我们看到：测试输出内容中包含“gathering baseline coverage字样”，这里要告诉大家的是，go fuzzing使用的是一种名为“覆盖率引导的fuzzing(coverage-guided fuzzing)”。我们知道Fuzzing测试使用的是随机生成的随机数据对被测目标进行测试，如果仅仅是用凭空随机的方式生成的输入很难有效找到边缘情况，当今大多数现代的fuzzing工具都是用了coverage-guided fuzzing的引擎来驱动测试，它可以确定新生成的语料是否能覆盖到新的代码路径。Dmitry在[“Fuzzing support for Go”](https://docs.google.com/document/u/1/d/1zXR-TFL3BfnceEAWytV8bnzB2Tfp6EPFinWVJ5V4QC8/pub)一文中曾经对coverage-guided fuzzing的引擎的工作逻辑做过如下描述：

```
从一些（可能是空的）输入的语料库开始
for {
从语料库中随机选择一个输入
对输入进行变异(mutate)
执行变异后的输入并收集代码覆盖率
如果该输入给出了新的覆盖率，则将其添加到语料库中
}
```


收集代码覆盖率数据和检测一个输入”给出新的覆盖率”并非易事，这也是为什么很多第三方fuzzing工具难于实现的原因，而加入到go原生工具链中，这些特性可借助Go编译器以及已有的设施来完成。

- 缓存新加入的语料

在上面go test -fuzz执行过程中，新生成的可以覆盖新代码路径的语料放置在哪里了呢？Go fuzzing会将其缓存在cache路径下，我在本机的gocache路径下发现如下与fuzz有关的内容：

```
//GOCACHE="/Users/tonybai/Library/Caches/go-build"
$ls /Users/tonybai/Library/Caches/go-build/fuzz/github.com/bigwhite/gocmpp/FuzzSubmit
01e40385855b3d317d42bf7ba4a9118702d867492fe2cd52bc84e554769480e5
06ba4bdb19de593e669c642987e270fe2488d4d58ecd712db136a3e011071253
086eabebec22d361087ce571571d86b1cbe1ad3e713f981473275f2c8fa64f09
... ...
```


go fuzzing会为每个FuzzXxx函数建立对应的语料缓存。目前fuzz cache的默认路径为$GOCACHE/fuzz/包路径/FuzzXxx，后续可能会提供环境变量或cmd option，以允许开发人员自定义fuzzing语料的缓存路径。

前面我们说过，fuzzing test默认会一直执行下去，如果不限制执行次数和执行时间，执行Fuzzing test的机器要有足够的存储才行。而要想清理过多的fuzz缓存，用gotip clean -cache是不行的，需要为clean加上-fuzzcache才可以清除fuzz的cache。

#### 使用Add方法提供种子语料

下面是通过testing.F的Add方法为fuzzing test提供种子语料的例子：

```
//go:build go1.18
// +build go1.18
package cmpp_test
import (
"testing"
cmpp "github.com/bigwhite/gocmpp"
)
func FuzzSubmit(f *testing.F) {
data := []byte{
0x00, 0x00, 0x00, 0xbd, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x74, 0x65, 0x73, 0x74, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x02, 0x31, 0x33, 0x35, 0x30, 0x30, 0x30, 0x30, 0x32, 0x36, 0x39, 0x36, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x39, 0x30, 0x30, 0x30, 0x30,
0x31, 0x30, 0x32, 0x31, 0x30, 0x00, 0x00, 0x00, 0x00, 0x31, 0x35, 0x31, 0x31, 0x30, 0x35, 0x31,
0x33, 0x31, 0x35, 0x35, 0x35, 0x31, 0x30, 0x31, 0x2b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x39, 0x30, 0x30, 0x30, 0x30,
0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x01, 0x31, 0x33, 0x35, 0x30, 0x30, 0x30, 0x30, 0x32, 0x36, 0x39, 0x36, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x6d, 0x4b, 0x8b, 0xd5, 0x00, 0x67, 0x00, 0x6f, 0x00,
0x63, 0x00, 0x6d, 0x00, 0x70, 0x00, 0x70, 0x00, 0x20, 0x00, 0x73, 0x00, 0x75, 0x00, 0x62, 0x00,
0x6d, 0x00, 0x69, 0x00, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
}
f.Add(data[8:])
f.Fuzz(func(t *testing.T, data []byte) {
p := &cmpp.Cmpp2SubmitReqPkt{}
_ = p.Unpack(data)
})
}
```


在上面代码中，我们使用了一个正确的cmpp2 submit消息包的数据作为种子语料，后续fuzzing会基于该语料做mutate，生成其他语料对Submit的Unpack方法进行测试。执行该fuzz test的输出与不设置种子语料的输出差别不大：

```
$gotip test -fuzz .
fuzz: elapsed: 0s, gathering baseline coverage: 0/1 completed
fuzz: elapsed: 0s, gathering baseline coverage: 1/1 completed, now fuzzing with 8 workers
fuzz: elapsed: 3s, execs: 395490 (131760/sec), new interesting: 20 (total: 20)
fuzz: elapsed: 6s, execs: 795164 (133251/sec), new interesting: 22 (total: 22)
fuzz: elapsed: 9s, execs: 1106761 (103875/sec), new interesting: 22 (total: 22)
^Cfuzz: elapsed: 11s, execs: 1281577 (92654/sec), new interesting: 22 (total: 22)
PASS
ok github.com/bigwhite/gocmpp 10.917s
```


#### 使用testdata/fuzz/FuzzXxx目录提供种子语料

除了通过Add方法添加种子语料外，我们还可以在项目的testdata/fuzz/FuzzXxx目录下为FuzzXxx用例提供种子语料：

```
$tree testdata
testdata
└── fuzz
└── FuzzSubmit
└── corpus1
$cat testdata/fuzz/FuzzSubmit/corpus1
go test fuzz v1
[]byte("ABC\xa8\x8c\xb3G\xfc")
```


我们把FuzzSubmit代码恢复为不带有Add的形式：

```
func FuzzSubmit(f *testing.F) {
f.Fuzz(func(t *testing.T, data []byte) {
p := &cmpp.Cmpp2SubmitReqPkt{}
_ = p.Unpack(data)
})
}
```


执行这一用例，输出入下结果：

```
$gotip test -fuzz .
fuzz: elapsed: 0s, gathering baseline coverage: 0/23 completed
fuzz: elapsed: 0s, gathering baseline coverage: 23/23 completed, now fuzzing with 8 workers
fuzz: elapsed: 3s, execs: 355689 (118485/sec), new interesting: 3 (total: 25)
fuzz: elapsed: 6s, execs: 623934 (89390/sec), new interesting: 5 (total: 27)
fuzz: elapsed: 9s, execs: 756400 (44154/sec), new interesting: 5 (total: 27)
^Cfuzz: elapsed: 10s, execs: 771910 (28387/sec), new interesting: 5 (total: 27)
PASS
ok github.com/bigwhite/gocmpp 9.564s
```


### 模拟crash

Fuzzing技术作为其他测试的一种补充，可以用于发现代码中潜在的不易被发现的问题，但这一过程有时候也是很漫长的。因此在这里我们模拟一个crash的产生来看看：当fuzzing test过程中发现代码bug时，fuzzing都做了那些事情。

我们在被测方法Unpack中故意放置了一个panic语句：

```
// submit.go
func (p *Cmpp2SubmitReqPkt) Unpack(data []byte) error {
... ...
panic("panic for fuzz demo")
... ...
}
```


这样，当fuzzing test执行到这里时Unpack方法就会panic，而fuzzing会生成crash报告并终止fuzz testing执行。

但要注意的是：go test -fuzz是先运行TestXxx，然后再运行FuzzXxx的，如果在TestXxx中发生了panic，那么go fuzzing是不会生成crash报告的。另外还有一点要格外注意：**go fuzzing将种子语料作为输入时出现的panic也是不会生成crash报告的**，因为，此时对数据的fuzzing还没有真正开始。因此，这里我们使用上面那个不带有种子语料的FuzzSubmit。

好了，我们执行一下fuzzing test：

```
$gotip test -fuzz .
fuzz: elapsed: 0s, gathering baseline coverage: 0/27 completed
fuzz: minimizing 148-byte crash file
fuzz: elapsed: 0s, gathering baseline coverage: 0/27 completed
--- FAIL: FuzzSubmit (0.03s)
--- FAIL: FuzzSubmit (0.00s)
testing.go:1319: panic: panic for fuzz demo
goroutine 49 [running]:
runtime/debug.Stack()
/Users/tonybai/sdk/gotip/src/runtime/debug/stack.go:24 +0x90
testing.tRunner.func1()
/Users/tonybai/sdk/gotip/src/testing/testing.go:1319 +0x1f2
panic({0x11ca860, 0x1241148})
/Users/tonybai/sdk/gotip/src/runtime/panic.go:838 +0x207
github.com/bigwhite/gocmpp.(*Cmpp2SubmitReqPkt).Unpack(0xc00025a5a0, {0xc000024400, 0x1, 0x80})
/Users/tonybai/Go/src/github.com/bigwhite/gocmpp/submit.go:262 +0x625
github.com/bigwhite/gocmpp_test.FuzzSubmit.func1(0x0?, {0xc000024400, 0x1, 0x80})
/Users/tonybai/Go/src/github.com/bigwhite/gocmpp/submit_fuzz_test.go:32 +0x45
reflect.Value.call({0x11ccf40?, 0x12111c8?, 0x13?}, {0x1200df5, 0x4}, {0xc000217080, 0x2, 0x2?})
/Users/tonybai/sdk/gotip/src/reflect/value.go:543 +0x814
reflect.Value.Call({0x11ccf40?, 0x12111c8?, 0x10f9980?}, {0xc000217080, 0x2, 0x2})
/Users/tonybai/sdk/gotip/src/reflect/value.go:339 +0xbf
testing.(*F).Fuzz.func1.1(0x0?)
/Users/tonybai/sdk/gotip/src/testing/fuzz.go:327 +0x20b
testing.tRunner(0xc000201860, 0xc0003a0900)
/Users/tonybai/sdk/gotip/src/testing/testing.go:1409 +0x102
created by testing.(*F).Fuzz.func1
/Users/tonybai/sdk/gotip/src/testing/fuzz.go:316 +0x5b8
Crash written to testdata/fuzz/FuzzSubmit/582528ddfad69eb57775199a43e0f9fd5c94bba343ce7bb6724d4ebafe311ed4
To re-run:
go test github.com/bigwhite/gocmpp -run=FuzzSubmit/582528ddfad69eb57775199a43e0f9fd5c94bba343ce7bb6724d4ebafe311ed4
FAIL
exit status 1
FAIL github.com/bigwhite/gocmpp 0.037s
```


我们看到go fuzzing在执行第一个测试时就发生了crash，fuzzing将crash输出了crash报告，并将引发这一crash的语料放入了testdata/fuzz/FuzzSubmit目录下：

```
$tree testdata
testdata
└── fuzz
└── FuzzSubmit
└── 582528ddfad69eb57775199a43e0f9fd5c94bba343ce7bb6724d4ebafe311ed4
```


查看一下引发crash的语料：

```
$cat testdata/fuzz/FuzzSubmit/582528ddfad69eb57775199a43e0f9fd5c94bba343ce7bb6724d4ebafe311ed4
go test fuzz v1
[]byte("0")
```


如果是真实的fuzz测试引发了crash，我们可以将该语料提取出来，建立针对它的TestXxx或为现有TestXxx添加一条测试数据来验证目标方法是否真实存在缺陷，如果的确存在缺陷，我们就需要修复它，并在修复后再次运行TestXxx，以保证我们的修复是有效的。

### 小结

在即将到来的Go 1.18中，Go fuzzing将正式成为Go的“一等公民”，Go将原生支持Fuzzing。不过Go fuzzing刚刚加入，可能还存在各种问题，根据以往经验，在2-3个版本后，go fuzzing必将成熟稳定起来，到那时，Gopher们就又拥有了一柄挖掘潜在bug和安全问题的利器了。

### 参考资料

[《Fuzzing in Go》](https://lwn.net/Articles/829242/)– https://lwn.net/Articles/829242/[《Fuzzing is Beta Ready》](https://go.dev/blog/fuzz-beta)– https://go.dev/blog/fuzz-beta[《Design Draft: First Class Fuzzing》](https://golang.org/s/draft-fuzzing-design)– https://golang.org/s/draft-fuzzing-design-
[issue: testing: add fuzz test support](https://github.com/golang/go/issues/44551)– https://github.com/golang/go/issues/44551 -
[Fuzz testing doc](https://pkg.go.dev/testing@master#hdr-Fuzzing)– https://pkg.go.dev/testing@master#hdr-Fuzzing - 《
[Go语言随机测试工具go-fuzz](http://tonybai.com/2015/12/08/go-fuzz-intro/)》 – http://tonybai.com/2015/12/08/go-fuzz-intro/ [维基百科Fuzzing](https://en.wikipedia.org/wiki/Fuzzing)– https://en.wikipedia.org/wiki/Fuzzing[Fuzzing introduction by OWASP](https://owasp.org/www-community/Fuzzing)– https://owasp.org/www-community/Fuzzing[Fuzzing support for Go](https://docs.google.com/document/u/1/d/1zXR-TFL3BfnceEAWytV8bnzB2Tfp6EPFinWVJ5V4QC8/pub)– https://docs.google.com/document/u/1/d/1zXR-TFL3BfnceEAWytV8bnzB2Tfp6EPFinWVJ5V4QC8/pub[Go播客：深入研究Fuzzing及Go官方Fuzzing提案](https://changelog.com/gotime/145)– https://changelog.com/gotime/145

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


微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论