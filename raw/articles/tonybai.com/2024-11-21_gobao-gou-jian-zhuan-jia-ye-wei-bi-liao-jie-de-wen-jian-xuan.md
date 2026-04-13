---
title: Go包构建：专家也未必了解的文件选择细节
url: https://tonybai.com/2024/11/21/go-source-file-selection-details-when-building-package/
published: '2024-11-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go包构建：专家也未必了解的文件选择细节

![](../../assets/8ca4f5b06cfebd4f.png)


[本文永久链接](https://tonybai.com/2024/11/21/go-source-file-selection-details-when-building-package) – https://tonybai.com/2024/11/21/go-source-file-selection-details-when-building-package

在Go语言开发中，[包（package）是代码组织的基本单位](https://tonybai.com/2023/06/18/go-package-design-guide/)，也是基本的构建单元。Go编译器会将每个包构建成一个目标文件(.a)，然后通过链接器将这些目标文件链接在一起，形成最终的可执行程序。

尽管Go包的构建过程看似简单，但实际上蕴含着许多值得深入了解的细节。例如，当我们执行go build命令时，Go编译器是如何选择需要编译的源文件的？你可能会回答：“不就是通过文件名中的ARCH和OS标识以及构建约束（build constraints）来选择的吗？” 虽然你的答案并没有错，但如果我进一步提出以下问题，你是否还能给出确切的答案呢？

假设一个Go源文件使用了如下的构建约束：

```
//go:build unix
package foo
// ... ...
```


在执行GOOS=android go build时，这个文件是否会被编译？如果执行的是GOOS=aix go build呢？而“unix”究竟包含了哪些操作系统？

再进一步，当一个源文件的文件名中包含ARCH和操作系统标识，并且文件内容中也使用了构建约束时，Go编译器会如何处理这些信息的优先级？

即使是经验丰富的Go专家，对于上述在包构建过程中涉及的文件选择细节，可能也只能给出模糊的答案。

在实际开发中，我们常常需要针对不同操作系统和架构编写特定的代码，这意味着灵活性与复杂性并存。Go的构建约束和文件名约定虽然为我们提供了灵活性，但也带来了额外的复杂性。理解这些规则不仅有助于优化构建过程，还能有效避免潜在的错误和不必要的麻烦。

在这篇文章中，我将与大家探讨**Go包构建过程中源文件选择的细节**，包括文件名中ARCH和os标识约定和构建约束的作用，以及二者的优先级处理问题。希望通过这些内容，帮助开发者更好地掌握Go语言的构建机制，从而提高开发效率。

为了更好地说明Go包构建时的文件选择逻辑，我们先从Go包构建的一些“表象”说起。

注：在本文中，我们将使用

[Go 1.17]引入的新版build constraints写法：//go:build ，之前的// +build aix darwin dragonfly freebsd js,wasm …写法已经不再被推荐使用。如果你想对旧版build constraints写法有一个全面了解以便与新写法对比，推荐阅读我的[《Go语言精进之路：从新手到高手的编程思想、方法和技巧》第2册]。

## 1. 表象

在Go工程中，通常一个目录对应一个Go包，每个Go包下可以存在多个以.go为后缀的Go源文件，这些源文件只能具有唯一的包名（测试源文件除外），以标准库fmt包为例，它的目录下的源文件列表如下(以[Go 1.23.0](https://tonybai.com/2024/08/19/some-changes-in-go-1-23/)源码为例)：

```
$ls $GOROOT/src/fmt
doc.go export_test.go print.go stringer_example_test.go
errors.go fmt_test.go scan.go stringer_test.go
errors_test.go format.go scan_test.go
example_test.go gostringer_example_test.go state_test.go
```


在这些文件中，哪些最终进入到了fmt包的目标文件(fmt.a)中呢？**贴心的Go工具链**为我们提供了查看方法：

```
$go list -f '{{.GoFiles}}' fmt
[doc.go errors.go format.go print.go scan.go]
```


对于独立于目标ARCH和OS的fmt包来说，其Go源文件的选择似乎要简单一些。我们看到，除了包测试文件(xxx_test.go)，其他文件都被编译到了最终的fmt包中。

我们再来看一个与目标ARCH和OS相关性较高的net包。除去子目录，这个包目录下的Go源文件数量大约有220多个，但在**macOS/amd64**下通过go list查看最终进入net包目标文件的文件，大约只有几十个：

```
$go list -f '{{.GoFiles}}' net
[addrselect.go cgo_darwin.go cgo_unix.go cgo_unix_syscall.go conf.go dial.go dnsclient.go dnsclient_unix.go dnsconfig.go dnsconfig_unix.go error_posix.go error_unix.go fd_posix.go fd_unix.go file.go file_unix.go hook.go hook_unix.go hosts.go interface.go interface_bsd.go interface_darwin.go ip.go iprawsock.go iprawsock_posix.go ipsock.go ipsock_posix.go lookup.go lookup_unix.go mac.go mptcpsock_stub.go net.go netcgo_off.go netgo_off.go nss.go parse.go pipe.go port.go port_unix.go rawconn.go rlimit_unix.go sendfile_unix_alt.go sock_bsd.go sock_posix.go sockaddr_posix.go sockopt_bsd.go sockopt_posix.go sockoptip_bsdvar.go sockoptip_posix.go splice_stub.go sys_cloexec.go tcpsock.go tcpsock_posix.go tcpsock_unix.go tcpsockopt_darwin.go tcpsockopt_posix.go udpsock.go udpsock_posix.go unixsock.go unixsock_posix.go unixsock_readmsg_cloexec.go writev_unix.go]
```


接下来，我们跳出Go标准库，来看一个自定义的示例：

```
$tree -F buildconstraints/demo1
buildconstraints/demo1
├── foo/
│ ├── f1_android.go
│ ├── f2_linux.go
│ └── f3_darwin.go
└── go.mod
// buildconstraints/demo1/foo/f1_android.go
//go:build linux
package foo
func F1() {
}
// buildconstraints/demo1/foo/f2_linux.go
//go:build android
package foo
func F2() {
}
// buildconstraints/demo1/foo/f3_darwin.go
//go:build android
package foo
func F3() {
}
```


在GOOS=android下构建buildconstraints/demo1/foo这个包，哪些文件会被选出来呢，看下面输出结果：

```
$GOOS=android go list -f '{{.GoFiles}}' github.com/bigwhite/demo1/foo
[f1_android.go f2_linux.go]
```


如果说前两个示例还好理解，那这第三个示例很可能会让很多开发者觉得有些“发蒙”。 别急，上面三个示例都是表象，接下来，我们就来仔细探索一下Go构建时的文件选择机制。

## 2. 文件选择机制

Go包构建时选择源文件的机制还是蛮繁琐的，我们需要从源码入手梳理出其主要逻辑，在Go 1.23版本中，Go包构建过程源文件选择逻辑的代码位于\$GOROOT/src/go/build/build.go中，这个源文件有2k多行，不过不用担心，我这里会替你把主要调用逻辑梳理为下图：

![](../../assets/e2bf9aa6eb5fa18f.png)


函数Import调用Default.Import去获取包的详细信息，信息用build.Package结构表示：

```
// $GOROOT/src/go/build/build.go
// A Package describes the Go package found in a directory.
type Package struct {
Dir string // directory containing package sources
Name string // package name
ImportComment string // path in import comment on package statement
Doc string // documentation synopsis
ImportPath string // import path of package ("" if unknown)
Root string // root of Go tree where this package lives
SrcRoot string // package source root directory ("" if unknown)
PkgRoot string // package install root directory ("" if unknown)
PkgTargetRoot string // architecture dependent install root directory ("" if unknown)
BinDir string // command install directory ("" if unknown)
Goroot bool // package found in Go root
PkgObj string // installed .a file
AllTags []string // tags that can influence file selection in this directory
ConflictDir string // this directory shadows Dir in $GOPATH
BinaryOnly bool // cannot be rebuilt from source (has //go:binary-only-package comment)
// Source files
GoFiles []string // .go source files (excluding CgoFiles, TestGoFiles, XTestGoFiles)
... ...
```


其中的GoFiles就是参与Go包编译的源文件列表。

Default是默认的上下文信息，包括构建所需的默认goenv中几个环境变量，比如GOARCH、GOOS等的值：

```
// Default is the default Context for builds.
// It uses the GOARCH, GOOS, GOROOT, and GOPATH environment variables
// if set, or else the compiled code's GOARCH, GOOS, and GOROOT.
var Default Context = defaultContext()
```


Context的Import方法代码行数很多，对于要了解文件选择细节的我们来说，其中最重要的调用是Context的matchFile方法。

matchFile正是那个**用于确定某个Go源文件是否应该被选入最终包文件中的方法**。它内部的逻辑可以分为两个主要步骤。

第一步是**调用Context的goodOSArchFile方法对Go源文件的名字进行判定**，goodOSArchFile方法的判定也有两个子步骤：

- 判断名字中的OS和ARCH是否在Go支持的OS和ARCH列表中

当前Go支持的OS和ARCH在syslist.go文件中有定义：

```
// $GOROOT/src/go/build/syslist.go
// knownArch is the list of past, present, and future known GOARCH values.
// Do not remove from this list, as it is used for filename matching.
var knownArch = map[string]bool{
"386": true,
"amd64": true,
"amd64p32": true,
"arm": true,
"armbe": true,
"arm64": true,
"arm64be": true,
"loong64": true,
"mips": true,
"mipsle": true,
"mips64": true,
"mips64le": true,
"mips64p32": true,
"mips64p32le": true,
"ppc": true,
"ppc64": true,
"ppc64le": true,
"riscv": true,
"riscv64": true,
"s390": true,
"s390x": true,
"sparc": true,
"sparc64": true,
"wasm": true,
}
// knownOS is the list of past, present, and future known GOOS values.
// Do not remove from this list, as it is used for filename matching.
// If you add an entry to this list, look at unixOS, below.
var knownOS = map[string]bool{
"aix": true,
"android": true,
"darwin": true,
"dragonfly": true,
"freebsd": true,
"hurd": true,
"illumos": true,
"ios": true,
"js": true,
"linux": true,
"nacl": true,
"netbsd": true,
"openbsd": true,
"plan9": true,
"solaris": true,
"wasip1": true,
"windows": true,
"zos": true,
}
```


我们也可以通过下面命令查看：

```
$go tool dist list
aix/ppc64
android/386
android/amd64
android/arm
android/arm64
darwin/amd64
darwin/arm64
dragonfly/amd64
freebsd/386
freebsd/amd64
freebsd/arm
freebsd/arm64
freebsd/riscv64
illumos/amd64
ios/amd64
ios/arm64
js/wasm
linux/386
linux/amd64
linux/arm
linux/arm64
linux/loong64
linux/mips
linux/mips64
linux/mips64le
linux/mipsle
linux/ppc64
linux/ppc64le
linux/riscv64
linux/s390x
netbsd/386
netbsd/amd64
netbsd/arm
netbsd/arm64
openbsd/386
openbsd/amd64
openbsd/arm
openbsd/arm64
openbsd/ppc64
openbsd/riscv64
plan9/386
plan9/amd64
plan9/arm
solaris/amd64
wasip1/wasm
windows/386
windows/amd64
windows/arm
windows/arm64
```


注：像sock_bsd.go、sock_posix.go这样的Go源文件，虽然它们的文件名中包含posix、bsd等字样，但这些文件实际上只是普通的Go源文件。其文件名本身并不会影响Go包在构建时选择文件的结果。


- 调用matchTag来判定该Go源文件名字中的OS和ARCH是否与当前上下文信息中的OS和ARCH匹配

Go支持的源文件名组成格式如下：

```
// name_$(GOOS).*
// name_$(GOARCH).*
// name_$(GOOS)_$(GOARCH).*
// name_$(GOOS)_test.*
// name_$(GOARCH)_test.*
// name_$(GOOS)_$(GOARCH)_test.*
```


不过这里有三个例外，即：

如果上下文中的GOOS=android，那么文件名字中OS值为linux的Go源文件也算是匹配的；

如果上下文中的GOOS=illumos，那么文件名字中OS值为solaris的Go源文件也算是匹配的；

如果上下文中的GOOS=ios，那么文件名字中OS值为darwin的Go源文件也算是匹配的。

还有一个特殊处理，那就是当文件名字中OS值为unix时，该源文件可以匹配以下上下文中GOOS的值：

```
// $GOROOT/src/go/build/syslist.go
// unixOS is the set of GOOS values matched by the "unix" build tag.
// This is not used for filename matching.
// This list also appears in cmd/dist/build.go and
// cmd/go/internal/imports/build.go.
var unixOS = map[string]bool{
"aix": true,
"android": true,
"darwin": true,
"dragonfly": true,
"freebsd": true,
"hurd": true,
"illumos": true,
"ios": true,
"linux": true,
"netbsd": true,
"openbsd": true,
"solaris": true,
}
```


这里面列出os都是所谓的“类Unix”操作系统。

如果goodOSArchFile方法返回文件名匹配成功，那么**第二步就是调用Context的shouldBuild方法对Go源文件中的build constraints进行判定**，这个判定过程也是调用matchTag完成的，因此规则与上面对matchTag的说明一致。如果判定match成功，那么该源文件将会被Go编译器编译到最终的Go包目标文件中去。

下面我们结合文章第一节“表象”中的那个自定义示例来判定一下为何最终会输出那个结果。

## 3. 示例分析

在buildconstraints/demo1/foo包目录中，一共有三个Go源文件：

```
$tree -F foo
foo
├── f1_android.go
├── f2_linux.go
└── f3_darwin.go
```


注意：当前我的系统为**darwin/amd64**，但我们使用了GOOS=android的环境变量。我们顺着上一节梳理出来的文件选择判定的主逻辑，对着三个文件逐一过一遍。

- f1_android.go

首先用goodOSArchFile判定文件名是否匹配。当GOOS=android时，文件名中的os为android，文件名匹配成功，

然后用shouldBuild判定文件中的build constraints是否匹配。该文件的约束为linux，在上面matchTag的三个例外规则里提到过，当GOOS=android时，如果build constraints是linux，是可以匹配的。

因此，f1_android.go将出现在最终编译文件列表中。

- f2_linux.go

首先用goodOSArchFile判定文件名是否匹配。当GOOS=android时，文件名中的os为linux，linux显然在go支持的os列表中，并且根据matchTag的例外规则，当GOOS=android时，文件名中的os为linux时是可以匹配的。

然后用shouldBuild判定文件中的build constraints是否匹配。该文件的约束为android，与GOOS相同，可以匹配。

因此，f2_linux.go将出现在最终编译文件列表中。

- f3_darwin.go

首先用goodOSArchFile判定文件名是否匹配。当GOOS=android时，文件名中的os为darwin，虽然darwin在go支持的os列表中，但darwin与GOOS=android并不匹配，因此在goodOSArchFile这步中，f3_darwin.go就被“淘汰”掉了！即便f3_darwin.go中的build constraints为android。

因此，f3_darwin.go不会出现在最终编译文件列表中。

如果再增加一个源文件f4_unix.go，其内容为：

```
//go:build android
func F4() {
}
```


这个f4_unix.go是否会出现在最终的包编译文件列表中呢？这个作为思考题留给大家了，也欢迎你在评论区留言，说说你的思考结果。

## 4. 小结

在Go语言的开发过程中，包的构建是核心环节之一，而源文件的选择则是构建过程中一个复杂且关键的细节。本文深入探讨了Go编译器在执行go build命令时，如何根据文件名中的架构（ARCH）和操作系统（OS）标识，以及构建约束（build constraints），来选择需要编译的源文件。

通过具体示例，本文展示了不同文件名和构建约束如何影响最终的编译结果，并揭示了Go编译器处理这些信息的优先级。理解这些内部机制不仅能帮助开发者优化构建过程，还能有效避免潜在的错误。希望本文的分析能够给大家带去帮助。

注：限于篇幅，本文仅针对包编译文件选择最复杂的部分进行的探索，而像ReleaseTags(比如: go1.21等)、cgo、_test.go后缀等比较明显的约束并未涉及，同时对于新版build constraints的运算符组合也未提及，感兴趣的童鞋可以参考

[go build constraints]官方文档查阅。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/buildconstraints)下载。

## 5. 参考资料

[Go build constraints](https://pkg.go.dev/cmd/go#hdr-Build_constraints)– https://pkg.go.dev/cmd/go#hdr-Build_constraints[proposal: cmd/go: allow && and || operators and parentheses in build tags](https://github.com/golang/go/issues/25348)– https://github.com/golang/go/issues/25348[Bug-resistant build constraints — Draft Design](https://go.googlesource.com/proposal/+/master/design/draft-gobuild.md)– https://go.googlesource.com/proposal/+/master/design/draft-gobuild.md[cmd/go: continue conversion to bug-resistant //go:build constraints](https://github.com/golang/go/issues/41184)– https://github.com/golang/go/issues/41184[Go 1.17 release notes](https://go.dev/doc/go1.17)– https://go.dev/doc/go1.17[cmd/go: provide build tags for architecture environment variables](https://github.com/golang/go/issues/45454)– https://github.com/golang/go/issues/45454

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