---
title: 探索Go gcflags的使用模式与完整参数选项列表
url: https://tonybai.com/2025/01/22/gcflags-options-list-and-usage/
published: '2025-01-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 探索Go gcflags的使用模式与完整参数选项列表

![](../../assets/d8a5404e4fc00baf.png)


[本文永久链接](https://tonybai.com/2025/01/22/gcflags-options-list-and-usage) – https://tonybai.com/2025/01/22/gcflags-options-list-and-usage

Go build是Go开发中不可或缺的构建工具，其中-gcflags参数为开发者提供了向编译器传递额外选项的能力。然而，关于-gcflags的完整参数选项和使用模式，官方文档多有局限，很多开发者对此了解不深。本文将系统性地解析-gcflags的完整参数来源以及其结合包模式（package pattern）的使用方法，供大家参考。

注：本文主要以-gcflags为例，其实go build的-ldflags参数与-gcflags在使用方法上如出一辙，唯一不同的是ldflags是将参数传递给go链接器。


gcflags是Go构建工具的一个标志，用于向Go编译器 (go tool compile) 传递额外的编译参数。通过它，开发者可以调整编译行为，例如禁用优化、生成调试信息或输出反汇编代码等。

Go build文档中关于-gcflags的说明很短小精悍：

```
$go help build
... ...
-gcflags '[pattern=]arg list'
arguments to pass on each go tool compile invocation.
-ldflags '[pattern=]arg list'
arguments to pass on each go tool link invocation.
... ...
The -asmflags, -gccgoflags, -gcflags, and -ldflags flags accept a space-separated list of arguments to pass to an underlying tool during the build. To embed spaces in an element in the list, surround it with either single or double quotes. The argument list may be preceded by a package pattern and an equal sign, which restricts the use of that argument list to the building of packages matching that pattern (see 'go help packages' for a description of package patterns). Without a pattern, the argument list applies only to the packages named on the command line. The flags may be repeated with different patterns in order to specify different arguments for different sets of packages. If a package matches patterns given in multiple flags, the latest match on the command line wins. For example, 'go build -gcflags=-S fmt' prints the disassembly only for package fmt, while 'go build -gcflags=all=-S fmt' prints the disassembly for fmt and all its dependencies.
... ...
```


多数Go初学者初次看到上述关于gcflags的说明，都无法知道到底有哪些arg可用以及究竟如何使用gcflags，而[Go cmd文档](https://pkg.go.dev/cmd/go)中关于gcflags的内容也仅限于上述这些。

我将大家遇到的主要问题总结为下面两条：

- gcflags的完整参数选项列表在哪里可以找到？
- gcflags的使用模式，尤其是其中的package pattern应该如何正确使用？

如果你能正确回答上述两个问题，那你就基本掌握了gcflags的使用，**大可不必继续往下看了**。

否则，我们就一起分别看一下这两个问题该如何解答。

在哪里能**查找到gcflags可用的全部参数选项呢**？go help build不行，[go command的web文档](https://pkg.go.dev/cmd/go)中没有！甚至[Go tool compile的web文档](https://pkg.go.dev/cmd/compile)中列举的gcflag的参数列表也是不全的(或者说是文档没有及时同步最新的参数列表变化)，也许我们应该提一个issue给Go团队^_^。

远在天边近在眼前！下面命令可以让-gcflag可用的参数选项完整列表尽收眼底：

```
$go tool compile -h
usage: compile [options] file.go...
-% debug non-static initializers
-+ compiling runtime
-B disable bounds checking
-C disable printing of columns in error messages
-D path
set relative path for local imports
-E debug symbol export
-I directory
add directory to import search path
-K debug missing line numbers
-L also show actual source file names in error messages for positions affected by //line directives
-N disable optimizations
-S print assembly listing
-V print version and exit
-W debug parse tree after type checking
-asan
build code compatible with C/C++ address sanitizer
-asmhdr file
write assembly header to file
... ...
```


同样，如果你要查看-ldflags的完整参数选项列表，你可以使用下面命令：

```
$go tool link -h
usage: link [options] main.o
-B note
add an ELF NT_GNU_BUILD_ID note when using ELF; use "gobuildid" to generate it from the Go build ID
-E entry
set entry symbol name
-H type
set header type
-I linker
use linker as ELF dynamic linker
-L directory
add specified directory to library path
-R quantum
set address rounding quantum (default -1)
-T int
set the start address of text symbols (default -1)
-V print version and exit
-X definition
add string value definition of the form importpath.name=value
-a no-op (deprecated)
-asan
enable ASan interface
... ...
```


到这里，我们得到了第一个问题的答案。

接下来，我们**再来看第二个问题**：-gcflags的使用模式。

根据go help build的输出，我们知道-gcflags的使用形式如下：

```
-gcflags '[pattern=]arg list'
```


其中：

- [pattern=]（可选）：包模式(package pattern)，用于作用范围控制，即限定参数仅应用于特定的包。如果省略此部分，则参数仅适用于命令行中指定的包。
- arg list：参数选项列表，多个参数以空格分隔。

对包模式有很好地理解并非是使用好gcflags的必要条件。但在一些复杂项目中，我们可能会通过包模式精确控制调试和优化，在这种情况下，对包模式有深入理解还是大有裨益的。

包模式是一种通过匹配规则指定目标包的方式，常见的包模式有几下几种：

- ./…：匹配当前目录及其所有子目录中的包。
- /DIR/…：匹配/DIR及其子目录中的包。
- cmd/…：匹配Go仓库中cmd目录下的所有命令包。
- github.com/user/repo/…：匹配该github仓库中的所有包。
- all：GOPATH模式下，匹配的是所有GOPATH路径中的包，Go module模式下，all匹配主模块及其所有依赖的包（包括测试依赖）。
- std：仅匹配标准库包。
- cmd：匹配Go仓库中的Go命令及其内部包(internal)。

基于上述关于gcflags使用形式以及包模式的说明，我们举几个示例来直观理解一下gcflags的用法：

- 对单个包设置参数

```
$go build -gcflags=-S fmt
```


上述命令中的参数-S仅作用于fmt包，显示其反汇编代码。

- 对特定模式(比如all/std等)的包设置参数

```
$go build -gcflags='all=-N -l'
```


在Go module模式下，参数-N和-l应用于当前主模块所有包及其依赖，禁用优化和内联。

- 对不同包模式设置不同参数

```
$go build -gcflags='fmt=-S' -gcflags='net/http=-N'
```


Go build命令行中可以**多次使用-gcflags**，上述命令中的第一个gcflags对fmt包启用反汇编输出(-S)。第二个gcflags对net/http包禁用优化(-N)。

- 模式的优先级

```
$go build -gcflags='all=-N' -gcflags='fmt=-S'
```


像上面命令中，两个gcflags都匹配了fmt包，或者说两个gcflags的作用范围都包含了fmt包，这种情况下哪些参数会对fmt包生效呢？Go规定：当一个包匹配多个模式时，以最后一个匹配的参数为准。在这个例子中，fmt包将只应用-S参数，而其他包应用-N参数。

到这里，我们完成了对两个关于gcflags问题的回答!

最后小结一下：

- gcflags(以及-ldflags)是Go构建工具中的重要选项，能极大提升调试和优化效率。
- gcflags的完整的参数选项需通过底层工具获取，即go tool compile -h和go tool link -h。
- 对包模式的灵活使用能够精确控制gcflags参数的作用范围，为复杂项目提供了更大的自由度。

通过本篇文章，希望你能掌握查看gcflags完整参数列表的方法以及gcflags的使用模式，并在构建和调试Go项目时能更加得心应手。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾

。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

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

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

感谢分享，有帮助！

开心:)