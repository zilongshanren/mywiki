---
title: Go 1.24中值得关注的几个变化
url: https://tonybai.com/2025/02/16/some-changes-in-go-1-24/
published: '2025-02-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.24中值得关注的几个变化

![](../../assets/359110df7b29049a.png)


[本文永久链接](https://tonybai.com/2025/02/16/some-changes-in-go-1-24) – https://tonybai.com/2025/02/16/some-changes-in-go-1-24

北京时间2025年2月12日，恰逢中国传统元宵佳节，远在美国的[Go团队正式发布了Go 1.24](https://go.dev/blog/go1.24)的第一个版本[Go 1.24.0](https://go.dev/dl/go1.24.0.src.tar.gz)。这也是[Go团队在更换Tech Leader为Austin Clements](https://tonybai.com/2024/10/10/pass-torch-to-go-new-leadership-team/)后发布的首个大版本。

按照惯例，每次Go大版本发布时，我都会撰写一篇“Go 1.x中值得关注的几个变化”的文章。自2014年的[Go 1.4版本](https://tonybai.com/2014/11/04/some-changes-in-go-1-4)起，这一系列文章已经持续了11年。

不过，随着从[Go 1.17版本](https://tonybai.com/2021/08/17/some-changes-in-go-1-17)开始引入的“[Go 1.x新特性前瞻](https://tonybai.com/2021/08/18/go-language-specs-changes-in-go-1-17)”系列以及针对特定技术特性的专题文章，“Go 1.x中值得关注的几个变化”系列文章的形式也在不断演变。原先的“Go 1.x中值得关注的几个变化”可以理解为被目前的“Go 1.x新特性前瞻” + “特定技术特性文章” + “Go 1.x中值得关注的几个变化”所替代。

不过，随着从[Go 1.17版本](https://tonybai.com/2021/08/17/some-changes-in-go-1-17)开始引入的“[Go 1.x新特性前瞻](https://tonybai.com/2021/08/18/go-language-specs-changes-in-go-1-17)”系列以及针对特定技术特性的专题文章，“Go 1.x中值得关注的几个变化”系列的形式也在不断演变。原先的“Go 1.x中值得关注的几个变化”已逐渐被目前的“Go 1.x新特性前瞻” + “特定技术特性文章” + “Go 1.x中值得关注的几个变化(新版)”所替代。希望各位读者能够理解这种变化，“Go 1.x中值得关注的几个变化”系列依然会延续，但文章中将不再进行细致的分析，因为这些内容已经在之前的前瞻和专题文章中讨论过了。

好了，言归正传，我们来说说Go 1.24！

## 1. 语言变化

正如Go一贯所做的，新版Go 1.24.0继续遵循[Go1的兼容性规范](https://go.dev/doc/go1compat)。使用Go 1.24.0，你可以顺利编译和运行你用[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)编写的代码。相信许多Gopher正是因为这一点而喜欢上Go，就像下面这位Gopher在Go 1.24发布后所表现出的惊喜一样：

![](../../assets/f7f10cf97ad83f11.png)


不过，正如Go一贯所做的那样，在语法特性方面，Go显得十分“吝啬”。在[Go 1.18大方地引入了泛型](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)之后，Go团队又恢复了这种“吝啬”的风格。在[Go 1.24的发布说明](https://go.dev/doc/go1.24)中，那短短的一行字充分展现了这一特点：

![](../../assets/4bb39510149908f6.png)


我们看到，Go 1.24仅仅是将[Go 1.23版本](https://tonybai.com/2024/08/19/some-changes-in-go-1-23)中的实验特性“带有类型参数的类型别名”转正了，成为了默认特性。当然你仍然可以GOEXPERIMENT=noaliastypeparams显式关闭它。关于这个特性的具体内容，我们多次说过了，大家可以到《[Go 1.24新特性前瞻：语法、编译器与运行时](https://tonybai.com/2024/12/16/go-1-24-foresight-part1/)》温习一下它的具体内容。

不过这种“吝啬”也是很多Gopher所期望的，当年Go语言之父Rob Pike在[“Simplicity is Complicated”演讲](https://go.dev/talks/2015/simplicity-is-complicated.slide#9)中提到的如下权威观点，影响了诸多Gopher，当然也包括我：

![](../../assets/5835bf9f57726e3c.png)


因此，在正在如火如荼的“[spec: reduce error handling boilerplate using ?](https://github.com/golang/go/discussions/71460)”的讨论中，就[当前的情况来看，我也倾向于保持现状](https://tonybai.com/2025/02/08/personal-idea-about-using-question-mark-operator-in-go-error-handling-new-proposal/)。

## 2. 编译器与运行时

在2024年中旬，Fasthttp的作者、VictoriaMetrics的联合创始人Aliaksandr Valialkin曾因[Go加入自定义函数迭代的特性](https://tonybai.com/2024/06/24/range-over-func-and-package-iter-in-go-1-23/)而发文抱怨“[Go正在朝着错误的方向演进](https://itnext.io/go-evolves-in-the-wrong-direction-7dfda8a1a620)”。不过他也提到，如果Go团队专注于提升Go的性能，而不是在与社区争论一些“华而不实”的语法糖，可能会赢得更多开发者的青睐：

![](../../assets/e2300d9d65841f6b.png)


尽管Go 1.24尚未[添加对SIMD的官方支持](https://github.com/golang/go/issues/67520)，但引入的优化显然不会让Aliaksandr Valialkin失望。首当其冲的就是对map底层实现的优化——[使用更为高效的Swiss Table](https://github.com/golang/go/issues/54766)。关于Swiss Table及Go 1.24重写map的思路，可以参考我的《[Go map使用Swiss Table重新实现，性能最高提升近50%](https://tonybai.com/2024/11/14/go-map-use-swiss-table/)》一文。根据文中的实测结果，新版基于Swiss Table的map在多数测试项中表现出显著的性能提升，有些甚至接近50%！

当然，基于Swiss Table的map实现仍在不断完善，其实现者Michael Pratt将持续进行打磨和优化：

![](../../assets/dc5274196a4ee5d2.png)


参与Go Swiss Table重写方案讨论，并提供参考实现之一的CockroachDB CTO Peter Mattis，也在X.com上分享了[新map设计和实现的诞生过程与优势](https://x.com/petermattis/status/1889080982273163466)，大家可以阅读以加深理解。

此外，Go 1.24还优化了runtime内部的锁实现，新实现在高竞争情况下取得了显著的可扩展性提升，而不是像Go 1.24之前的实现那样随线程数增加而急剧下降。基准测试表明，在GOMAXPROCS=20时，性能提升达3倍。

更多编译器和运行时的变化，可以参考《[Go 1.24新特性前瞻：语法、编译器与运行时](https://tonybai.com/2024/12/16/go-1-24-foresight-part1/)》。

Go 1.24版本在编译器和运行时方面的优化投入和勇于改变，正是Go社区所期望的。相信后续版本在这方面的持续投入不会让Aliaksandr Valialkin失望。

## 3. 工具链

Go团队在Go工具链上的投入和结果一直被Go社区认可和赞扬！《[Go 1.24新特性前瞻：工具链和标准库](https://tonybai.com/2024/12/17/go-1-24-foresight-part2/)》一文中有对Go 1.24工具链变化的详细介绍，但在这里我还是要再次提及其中的三个变化。

### go.mod增加tool指示符，支持对tool的依赖管理

借用《[Go工具链版本已不由你定：go和toolchain指令详解](https://tonybai.com/2025/01/14/understand-go-and-toolchain-in-go-dot-mod/)》中的那幅图：

![](../../assets/a7fb043897583670.png)


Go的目标显然是要实现对Go应用所依赖“全要素”进行版本管理”，涵盖Go版本、工具链版本、第三方包版本以及依赖工具版本的管理。而Go 1.24在go.mod中增加tool指示符就是要实现对依赖工具的版本进行管理。增加tool指示符后，你可以像管理第三方包版本那样，使用go get -tool对依赖的tool的版本进行管理，go install tool对tool进行安装，并支持一个tool同时存在多个版本在本地，这是由于通过go.mod管理的依赖的tool会被像module那样缓存在本地构建缓存中(go build cache)。

btw，再说说go 1.24对toolchain依赖管理和选择的改善。即便看了《[Go工具链版本已不由你定：go和toolchain指令详解](https://tonybai.com/2025/01/14/understand-go-and-toolchain-in-go-dot-mod/)》一文，很多Gopher还是可能因为gotoolchain决策的复杂性和参与要素的众多而感到困惑，Go 1.24增加了GODEBUG=toolchaintrace=1可以输出做出决策的过程日志，告诉你Go为何会选择某个特定的toolchain版本。

### go vet的增强

在Go 1.24中，go vet的功能有了较大变化，新增或增强了如下一些分析器(analyzer)：

- 新增测试分析器

可以检测test、fuzz test、基准测试和example test中的常见错误，避免因命名、签名错误或引用不存在的标识符而导致测试无法运行。

- printf分析器增强

新增对fmt.Printf(s)的检查，如果这类调用中格式字符串并非常量且没有传入其他参数，则提醒用户使用fmt.Print。

- buildtag分析器增强

新增对无效Go主版本构建约束的检测，避免错误引用次版本号。例如，如果你使用//go:build go1.23.1，该分析器会提醒你应该使用//go:build go1.23。

- copylock分析器增强

增强对经典三段式for循环中包含sync.Locker的变量复制的不安全操作的诊断，防止锁的复制带来的潜在问题。这也是Go 1.23修正loopvar语义后避免Go用户误用的一个防卫手段。

### 新增GOCACHEPROG

另一个大家可能忽视的值得关注的改变是新增了GOCACHEPROG环境变量。

Go语言的cmd/go工具已经具备了强大的缓存支持，但其缓存机制仅限于基于文件系统的缓存。这种缓存方式在某些场景下效率不高，尤其是在CI（持续集成）环境中，用户通常需要将GOCACHE目录打包和解压缩，这往往比CI操作本身还要慢。此外，用户可能希望利用位于网络上的共享缓存(比如S3)或公司内部的P2P缓存协议来提高缓存效率，但这些功能并不适合直接集成到cmd/go工具中。

为了解决上述问题，Brad Fitzpatrick提出了一个新的环境变量GOCACHEPROG，类似于现有的GOCACHE变量。通过设置GOCACHEPROG，用户可以指定一个外部程序，该程序将作为子进程运行，并通过标准输入/输出来与cmd/go工具进行通信。cmd/go工具将通过这个接口**与外部缓存程序交互**，外部程序可以根据需要实现任意的缓存机制和策略。其大致结构如下：

![](../../assets/c5194cb58ee10415.png)


显然一旦可以在云上存储build cache，也能缓解一下Go用户抱怨本地缓存过大的问题。当然从实际情况来看(我的本地环境)，go build cache还不是最大的：

```
$go env|grep CACHE
GOCACHE='/Users/tonybai/Library/Caches/go-build'
GOCACHEPROG=''
GOMODCACHE='/Users/tonybai/Go/pkg/mod'
$cd /Users/tonybai/Library/Caches/go-build
$du -sh
155M .
$cd /Users/tonybai/Go/pkg/mod
$du -sh
7.0G
```


我们看到在我本地的环境中，go build cache和go module cache的size相比，简直是不值得一提，所以说如果后续**要有个GOMODCACHEPROG就更好了**，我也十分希望能将go module cache搬移到云端（比如S3）中，甚至可以让组织内的Gopher共享这些go module cache（当然要区分不同arch和os）。

更多关于工具链的变化，可以参考《[Go 1.24新特性前瞻：工具链和标准库](https://tonybai.com/2024/12/17/go-1-24-foresight-part2/)》。

## 4. 标准库

Go标准库向来是变化的大户，这里我显然不会列出所有变化，甚至一些值得关注的变化，比如：[json包增加对omitzero选项的支持](https://tonybai.com/2024/09/12/solve-the-empty-value-dilemma-in-json-encoding-with-omitzero)、[新增weak包和weak指针](https://tonybai.com/2024/09/23/go-weak-package-preview)等，也都在新特性前瞻或技术专题性文章中有过详细说明。

这里要说的是[Go对fips 140-3合规性的支持](https://tonybai.com/2024/11/16/go-crypto-and-fips-140/)，因为这个最终版本与当初新特性前瞻时有所变化。

基于[最新的Go fips 140-3文档](https://go.dev/doc/security/fips140)，我们可以得到关于fips 140-3使用方法的说明，这里简要梳理如下：

- Go 1.24及更高版本开始，Go二进制文件可以原生运行在FIPS 140-3合规模式下，不必依赖注入boringssl等第三方C++包。
- Go新增了的一个特殊的Go加密模块 (Go Cryptographic Module)，其下有一组新增的标准库包（位于crypto/internal/fips140/…下），实现了 FIPS 140-3批准的算法。这个cryptographic module的版本当前为v1.0.0，目前正在接受CMVP认证实验室的测试。

Go引入了GOFIPS140环境变量，用于go build、go install和go test命令，以选择要链接到可执行程序中的Go加密模块版本。该环境变量有三类可选值：

- off (默认): 使用标准库中的crypto/internal/fips140/…包。
- latest: 类似off，但默认启用FIPS 140-3模式。
- v1.0.0: 使用Go加密模块 v1.0.0 版本（在Go 1.24中首次发布，并在2025年初冻结），默认启用FIPS 140-3模式。

在运行时，可以通过GODEBUG=fips140=xxx来控制上述编译到Go中的Go cryptographic module是否运行在FIPS 140-3模式下，默认是off。

当使用GODEBUG=fips140=on时，Go运行时将会启用Go cryptographic module的FIPS 140-3模式。启用后，Go加密模块会执行以下操作：

- 完整性自检: 在init阶段，会验证模块对象文件的校验和，确保代码未被篡改。
- 已知答案自检: 根据FIPS 140-3指南，在init阶段或首次使用时，对算法进行已知答案测试。
- 密钥一致性测试: 对生成的密钥进行配对一致性测试 (这可能导致某些密钥类型生成速度减慢，特别是临时密钥)。
- crypto/rand.Reader改进: 使用NIST SP 800-90A DRBG，并从平台CSPRNG获取随机字节混合到输出中。
- crypto/tls限制: 仅协商符合NIST SP 800-52r2 的协议版本、密码套件、签名算法和密钥交换机制。
- crypto/rsa.SignPSS限制: 使用PSSSaltLengthAuto时，盐的长度会被限制为哈希的长度。

当使用GODEBUG=fips140=only时，不符合FIPS140-3的加密算法会返回错误或者panic。但是此模式仅为尽力而为，不保证符合所有的FIPS 140-3要求。

不过大家要知道的是：在Go 1.24版本中，GODEBUG=fips140=on和only在OpenBSD、Wasm、AIX和32位Windows平台上暂不受支持。

另外要想要检测FIPS 140-3模式是否已经激活，可以调用crypto/fips140.Enabled函数。

之前，一些场合用户使用BoringCrypto模块来实现某些FIPS 140-3算法的机制仍然可用，但**已不被官方支持**，并计划在未来版本中移除。另外要知道Go+BoringCrypto与原生FIPS 140-3模式并不兼容。这也是[Microsoft Go依旧宣称将保留自己维护的符合fips140-3的Go版本的原因](https://devblogs.microsoft.com/go/go-1-24-fips-update)。

## 5. 其他

最后重点说说WebAssembly port。

Go从Go 1.11版本开始通过js/wasm增加了对编译到Wasm的支持。Go 1.21版本又增加了对WASI的支持(GOOS=wasip1)，Go 1.24版本中，Go对Wasm的支持又有了新的特性。在Go 1.24发布没多久，Cherry Mui便在官博发表了名为“[Extensible Wasm Applications with Go](https://go.dev/blog/wasmexport)”的介绍Go 1.24中WebAssembly新特性的文章，文章介绍了Go 1.24对Wasm的支持程度以及一些限制。这里也参考了这篇文章，简单梳理一下Cherry给出的内容要点。

Go 1.24引入了新的编译器指示符go:wasmexport，允许将Go函数导出，以便从Wasm模块外部（通常是从运行Wasm运行时的主机应用程序）调用。该指示符指示编译器将带注释的函数作为Wasm导出提供，在生成的Wasm二进制文件中可用，比如：

```
//go:wasmexport add
func add(a, b int32) int32 { return a + b }
```


这样，Wasm模块将具有一个名为add的导出函数，可以从主机调用。

这是如何实现的呢？Cherry告诉我们这是通过构建一种名为WASI Reactor的Wasm模块来实现的。WASI Reactor是一种持续运行的WebAssembly模块，可以多次调用以响应事件或请求。与在主函数完成后终止的“命令”模块不同，reactor实例在初始化后保持活动状态，其导出保持可访问状态。

在Go 1.24中，要构建一个WASI reactor需要使用下面命令：

```
$GOOS=wasip1 GOARCH=wasm go build -buildmode=c-shared -o reactor.wasm
```


该构建命令指示链接器不生成_start函数（wasm命令模块的入口点），而是生成_initialize函数（执行运行时和包初始化）以及任何导出的函数及其依赖项。_initialize函数必须在任何其他导出函数之前调用。而main函数不会自动调用。

go:wasmexport指示符和reactor构建模式允许通过调用基于Go的Wasm代码来扩展应用程序。这对于采用Wasm作为具有明确定义接口的**插件或扩展机制**的应用程序特别有价值。**通过导出Go函数，应用程序可以利用Go Wasm模块提供功能，而无需重新编译整个应用程序**。此外，构建为reactor可确保可以多次调用导出的函数而无需重新初始化，使其适用于长时间运行的应用程序或服务。

次卧，Go 1.24还放宽了对可用于go:wasmimport函数的输入和结果参数类型的限制。例如，可以传递bool、string、指向int32的指针或指向嵌入structs.HostLayout并包含受支持字段类型的结构体的指针，这使得Go Wasm应用程序可以用更自然的方式编写，并消除了不必要的类型转换。

不过，go:wasmexport当前也有局限性，首先，Wasm 是单线程架构，没有并行性。go:wasmexport标识的函数可以生成新的goroutine。但是，如果函数创建了后台goroutine，则当go:wasmexport指示的函数返回时，它将不会继续执行，直到回调到基于Go的Wasm模块。

另外，尽管Go 1.24中放宽了一些类型限制，但对于可与go:wasmimport和go:wasmexport函数一起使用的类型仍然存在限制。比如由于客户端的64位体系结构和主机的32位体系结构之间的不匹配，我们无法传递内存中的指针。例如，go:wasmimport指示的函数不能采用指向包含指针类型字段的结构体的指针。

但不可否认的是go:wasmexport的支持，让Go更稳固了自己成为主流wasm开发语言之一的位置，虽然还有各种不足。近期Docker之父的初创公司Dagger就发博客宣称使用了[Go+WebAssembly重写了其Dagger Cloud的前端](https://dagger.io/blog/replaced-react-with-go)！

## 6. 小结

Go 1.24的发布，标志着Go语言在保持其核心理念——简洁与兼容性的同时，进入了一个新的发展阶段。这个版本没有在语法上大刀阔斧，而是将重心放在了底层性能优化、工具链完善和新兴技术布局上，展现出Go团队务实且具有前瞻性的发展策略。同时，Go 1.24也可以看成是一个承上启下的版本。它既巩固了Go语言在性能和工具链方面的优势，又为未来的发展方向做出了积极的布局。Go语言正以稳健的步伐，朝着更高效、更安全、更具适应性的方向迈进。我们可以期待，在未来的版本中，Go将继续在云原生计算、WebAssembly、AI应用等领域发挥更大的作用，为开发者带来更多的惊喜。

借此文章插播一条国内Go社区的news!

近期GoCN社区发文“[Farewell Go，Hello AI：是时候说再见了](https://mp.weixin.qq.com/s/9VtjDwbxu1BxLTbgHVQeXA)”和所有国内Go开发人员分享了“GoCN社区将正式转型升级为ThinkInAI社区”，全面拥抱AI的决定！这也意味国内最大Go技术社区的退出，最大Go技术大会GopherChina的正式落幕！除了AI是热门赛道这一原因之外，文章也给出了Go技术分享遇到瓶颈的说法：

![](../../assets/5af46e082310d23c.png)


不过就像文中所说的“这是任何技术发展到成熟阶段的必然现象”，在评论中一些Gopher也提到：**一个技术不再被更多讨论是成熟的标志**。

这其实与我在《[2024年Go语言盘点：排名历史新高，团队新老传承](https://tonybai.com/2025/01/06/the-2024-review-of-go-programming-language/)》一文中表达的Go演进趋势不谋而合！Go真的进入了成熟期了!

GoCn不在了，但go在国内的传播和使用依然会继续。请继续关注诸如[Gopher Daily](https://gopherdaily.tonybai.com)、我的公众号以及国内其他诸如像[鸟窝老师的blog](https://colobu.com)以及公众号，了解Go的最新动态以及技术理解。

最后感谢AstaXie(谢孟军)对国内Go社区发展所做出的卓越贡献，我也因有幸多次参与GopherChina以及会上分享而感到无比自豪。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

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

No related posts.

## 评论