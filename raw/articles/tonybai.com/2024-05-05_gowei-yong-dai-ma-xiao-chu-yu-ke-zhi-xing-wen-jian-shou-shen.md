---
title: Go未用代码消除与可执行文件瘦身
url: https://tonybai.com/2024/05/05/dead-code-elimination-and-executable-file-slimming-in-go/
published: '2024-05-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go未用代码消除与可执行文件瘦身

![](../../assets/06c69ad0f553b98a.png)


[本文永久链接](https://tonybai.com/2024/05/05/dead-code-elimination-and-executable-file-slimming-in-go) – https://tonybai.com/2024/05/05/dead-code-elimination-and-executable-file-slimming-in-go

在日常编写Go代码时，我们会编写很多包，也会在编写的包中引入了各种依赖包。在大型Go工程中，这些直接依赖和间接依赖的包数目可能会有几十个甚至上百个。依赖包有大有小，但通常我们不会使用到依赖包中的所有导出函数或类型方法。

这时Go初学者就会有一个疑问：这些直接依赖包和间接依赖包中的所有代码是否会进入到最终的可执行文件中呢？即便我们只是使用了某个依赖包中的一个导出函数。

这里先给出结论：不会！在这篇文章中，我们就来探索一下这个话题，了解一下其背后的支撑机制以及对Go可执行文件Size的影响。

## 1. 实验：哪些函数进入到最终的可执行文件中了？

我们先来做个实验，验证一下究竟哪些函数进入到最终的可执行文件中了！我们建立demo1，其目录结构和部分代码如下：

```
// dead-code-elimination/demo1
$tree -F .
.
├── go.mod
├── main.go
└── pkga/
└── pkga.go
// main.go
package main
import (
"fmt"
"demo/pkga"
)
func main() {
result := pkga.Foo()
fmt.Println(result)
}
// pkga/pkga.go
package pkga
import (
"fmt"
)
func Foo() string {
return "Hello from Foo!"
}
func Bar() {
fmt.Println("This is Bar.")
}
```


这个示例十分简单！main函数中调用了pkga包的导出函数Foo，而pkga包中除了Foo函数，还有Bar函数(但并没有被任何其他函数调用)。现在我们来编译一下这个module，然后查看一下编译出的可执行文件中都包含pkga包的哪些函数！(本文实验中使用的[Go为1.22.0版本](https://tonybai.com/2024/02/18/some-changes-in-go-1-22/))

```
$go build
$go tool nm demo|grep demo
```


在输出的可执行文件中，居然没有查到关于pkga的任何符号信息，这可能是Go的优化在“作祟”。我们关闭掉Go编译器的优化后，再来试试：

```
$go build -gcflags '-l -N'
$go tool nm demo|grep demo
108ca80 T demo/pkga.Foo
```


关掉[内联优化](https://tonybai.com/2022/10/17/understand-go-inlining-optimisations-by-example)后，我们看到pkga.Foo出现在最终的可执行文件demo中，但并未被调用的Bar函数并没有进入可执行文件demo中。

我们再来看一下有间接依赖的例子：

```
// dead-code-elimination/demo2
$tree .
.
├── go.mod
├── main.go
├── pkga
│ └── pkga.go
└── pkgb
└── pkgb.go
// pkga/pkga.go
package pkga
import (
"demo/pkgb"
"fmt"
)
func Foo() string {
pkgb.Zoo()
return "Hello from Foo!"
}
func Bar() {
fmt.Println("This is Bar.")
}
```


在这个示例中，我们在pkga.Foo函数中又调用了一个新包pkgb的Zoo函数，我们来编译一下该新示例并查看一下哪些函数进入到最终的可执行文件中：

```
$go build -gcflags='-l -N'
$go tool nm demo|grep demo
1093b40 T demo/pkga.Foo
1093aa0 T demo/pkgb.Zoo
```


我们看到：只有程序执行路径上能够触达（被调用）的函数才会进入到最终的可执行文件中！

在复杂的示例中，我们也可以通过带有-ldflags=’-dumpdep’的go build命令来查看这种调用依赖关系(这里以demo2为例)：

```
$go build -ldflags='-dumpdep' -gcflags='-l -N' > deps.txt 2>&1
$grep demo deps.txt
# demo
main.main -> demo/pkga.Foo
demo/pkga.Foo -> demo/pkgb.Zoo
demo/pkga.Foo -> go:string."Hello from Foo!"
demo/pkgb.Zoo -> math/rand.Int31n
demo/pkgb.Zoo -> demo/pkgb..stmp_0
demo/pkgb..stmp_0 -> go:string."Zoo in pkgb"
```


到这里，我们知道了Go通过某种机制保证了只有真正使用到的代码才会最终进入到可执行文件中，即便某些代码（比如pkga.Bar）和那些被真正使用的代码（比如pkga.Foo）在同一个包内。这同时保证了最终可执行文件大小在可控范围内。

接下来，我们就来看看Go的这种机制。

## 2. 未用代码消除(dead code elimination)

我们先来复习一下go build的构建过程，以下是 go build 命令的步骤概述：

-
读取go.mod和go.sum：如果当前目录包含go.mod文件，go build会读取该文件以确定项目的依赖项。它还会根据go.sum文件中的校验和验证依赖项的完整性。

-
计算包依赖图：go build 分析正在构建的包及其依赖项中的导入语句，以构建依赖图。该图表示包之间的关系，使编译器能够确定包的构建顺序。

-
决定要构建的包：基于构建缓存和依赖图，go build 确定需要构建的包。它检查构建缓存，以查看已编译的包是否是最新的。如果自上次构建以来某个包或其依赖项发生了更改，go build将重新构建这些包。

-
调用编译器（go tool compile）：对于每个需要构建的包，go build调用Go编译器（go tool compile）。编译器将Go源代码转换为特定目标平台的机器码，并生成目标文件（.o 文件）。

-
调用链接器（go tool link）：在编译所有必要的包之后，go build 调用 Go 链接器（go tool link）。链接器将编译器生成的目标文件合并为可执行二进制文件或包归档文件。它解析包之间的符号和引用，执行必要的重定位，并生成最终的输出。


上述的整个构建过程可以由下图表示：

![](../../assets/0989394b8e815f81.png)


在构建过程中，go build 命令还执行各种优化，例如未用代码消除和内联，以提高生成二进制文件的性能和降低二进制文件的大小。其中的未用代码消除就是保证Go生成的二进制文件大小可控的重要机制。

未用检测算法的实现位于$GOROOT/src/cmd/link/internal/ld/deadcode.go文件中。该算法通过图遍历的方式进行，具体过程如下：

- 从系统的入口点开始，标记所有可通过重定位到达的符号。重定位是两个符号之间的依赖关系。
- 通过遍历重定位关系，算法标记所有可以从入口点访问到的符号。例如，在主函数main.main中调用了pkga.Foo函数，那么main.main会有对这个函数的重定位信息。
- 标记完成后，算法会将所有未被标记的符号标记为不可达的未用。这些未被标记的符号表示不会被入口点或其他可达符号访问到的代码。

不过，这里有一个特殊的语法元素要注意，那就是带有方法的类型。类型的方法是否进入到最终的可执行文件中，需要考虑不同情况。在deadcode.go，用于标记可达符号的函数实现将可达类型的方法的调用方式分为三种：

- 直接调用
- 通过可到达的接口类型调用
- 通过反射调用：reflect.Value.Method（或 MethodByName）或 reflect.Type.Method（或 MethodByName）

第一种情况，可以直接将调用的方法被标记为可到达。第二种情况通过将所有可到达的接口类型分解为方法签名来处理。遇到的每个方法都与接口方法签名进行比较，如果匹配，则将其标记为可到达。这种方法非常保守，但简单且正确。

第三种情况通过寻找编译器标记为REFLECTMETHOD的函数来处理。函数F上的REFLECTMETHOD意味着F使用反射进行方法查找，但编译器无法在静态分析阶段确定方法名。因此所有调用reflect.Value.Method 或reflect.Type.Method的函数都是REFLECTMETHOD。调用reflect.Value.MethodByName或reflect.Type.MethodByName且参数为非常量的函数也是REFLECTMETHOD。如果我们找到了REFLECTMETHOD，就会放弃静态分析，并将所有可到达类型的导出方法标记为可达。

下面是一个来自参考资料中的示例：

```
// dead-code-elimination/demo3/main.go
type X struct{}
type Y struct{}
func (*X) One() { fmt.Println("hello 1") }
func (*X) Two() { fmt.Println("hello 2") }
func (*X) Three() { fmt.Println("hello 3") }
func (*Y) Four() { fmt.Println("hello 4") }
func (*Y) Five() { fmt.Println("hello 5") }
func main() {
var name string
fmt.Scanf("%s", &name)
reflect.ValueOf(&X{}).MethodByName(name).Call(nil)
var y Y
y.Five()
}
```


在这个示例中，类型*X有三个方法，类型*Y有两个方法，在main函数中，我们通过反射调用X实例的方法，通过Y实例直接调用Y的方法，我们看看最终X和Y都有哪些方法进入到最后的可执行文件中了：

```
$go build -gcflags='-l -N'
$go tool nm ./demo|grep main
11d59c0 D go:main.inittasks
10d4500 T main.(*X).One
10d4640 T main.(*X).Three
10d45a0 T main.(*X).Two
10d46e0 T main.(*Y).Five
10d4780 T main.main
... ...
```


我们看到通过直接调用的可达类型Y只有代码中直接调用的方法Five进入到最终可执行文件中，而通过反射调用的X的所有方法都可以在最终可执行文件找到！这与前面提到的第三种情况一致。

## 3. 小结

本文介绍了Go语言中的未用代码消除和可执行文件瘦身机制。通过实验验证，只有在程序执行路径上被调用的函数才会进入最终的可执行文件，未被调用的函数会被消除。

本文解释了Go编译过程，包括包依赖图计算、编译和链接等步骤，并指出未用代码消除是其中的重要优化策略。具体的未用代码消除算法是通过图遍历实现的，标记可达的符号并将未被标记的符号视为未用。文章还提到了对类型方法的处理方式。

通过这种未用代码消除机制，Go语言能够控制最终可执行文件的大小，实现可执行文件瘦身。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/dead-code-elimination)下载。

## 4. 参考资料

[Getting the most out of Dead Code elimination](https://golab.io/talks/getting-the-most-out-of-dead-code-elimination)– https://golab.io/talks/getting-the-most-out-of-dead-code-elimination[all: binaries too big and growing](https://github.com/golang/go/issues/6853)– https://github.com/golang/go/issues/6853[aarzilli/whydeadcode](https://github.com/aarzilli/whydeadcode)– https://github.com/aarzilli/whydeadcode

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论