---
title: Go 1.24新特性前瞻：工具链和标准库
url: https://tonybai.com/2024/12/17/go-1-24-foresight-part2/
published: '2024-12-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.24新特性前瞻：工具链和标准库

![](../../assets/24d3f4fcd7572701.png)


[本文永久链接](https://tonybai.com/2024/12/17/go-1-24-foresight-part2) – https://tonybai.com/2024/12/17/go-1-24-foresight-part2

在[上一篇文章](https://tonybai.com/2024/12/16/go-1-24-foresight-part1/)中，我们介绍了即将于2025年2月发布的Go 1.24版本在语法、编译器和运行时方面的主要变化。本文将继续承接上文，重点介绍Go 1.24在工具链和标准库方面的重要更新，供大家参考。

## 1. 工具链

我们日常编写Go项目代码时常常会依赖一些使用Go编写的工具，比如golang.org/x/tools/cmd/stringer或github.com/kyleconroy/sqlc。我们希望所有项目合作者都使用相同版本的工具，以避免在不同时间、不同环境中的输出不同的结果。因此，Go社区希望通过go.mod将工具的版本以及依赖管理起来。

在Go 1.24版本之前，Go Wiki推荐tools.go的一种来自社区的最佳实践，阐述这种实践的最好的一个示例来自Go modules by example中的一个文档：”[Tools as dependencies](https://github.com/go-modules-by-example/index/blob/master/010_tools/README.md)“，其大致思路是将项目依赖的Go工具以“项目依赖”的方式存放到tools.go文件(放到go module根目录下)中，以golang.org/x/tools/cmd/stringer为例，tools.go的内容大致如下：

```
//go:build tools
package tools
import (
_ "golang.org/x/tools/cmd/stringer"
)
```


然后在同一目录下安装stringer或直接go run：

```
$go install golang.org/x/tools/cmd/stringer
```


在安装stringer时，go.mod会记录下对stringer的依赖以及对应的版本，后续go.mod提交到项目repo中，所有项目成员就都可以使用相同版本的Stringer了。

tools.go实践虽然能解决问题，但这种方式还是存在一些不便：

- 配置繁琐：需要手动创建 tools.go 文件，并添加特定的
[构建标签](https://tonybai.com/2024/11/21/go-source-file-selection-details-when-building-package)来排除它； - 使用不便：运行工具时可能需要额外的脚本或配置(每次手敲go run golang.org/x/tools/cmd/stringer的确有些不便)。

Go开发者期望**工具依赖**也能够无缝地与其他项目依赖(包依赖)统一管理，并纳入go.mod的版本控制体系。

为此，该提案设计并实现了下面几点以满足开发者的上述述求：

- go.mod引入tool directive，用于显式声明项目所需的工具。
- tool directive与其他依赖项统一纳入go.mod文件，方便管理和版本控制。
- 扩展go install和go get命令，支持安装、更新和卸载工具。

我们来看一个示例，首先我们初始化一个module：

```
$ gotip mod init demo
go: creating new go.mod: module demo
$ cat go.mod
module demo
go 1.24
```


编辑go.mod，加入下面内容：

```
$ cat go.mod
module demo
go 1.24
tool golang.org/x/tools/cmd/stringer
```


安装tool前需要go get它的依赖，否则go install会报错：

```
$gotip install tool
no required module provides package golang.org/x/tools/cmd/stringer; to add it:
go get golang.org/x/tools/cmd/stringer
$gotip get golang.org/x/tools/cmd/stringer
go: downloading golang.org/x/tools v0.28.0
go: downloading golang.org/x/sync v0.10.0
go: downloading golang.org/x/mod v0.22.0
go: added golang.org/x/mod v0.22.0
go: added golang.org/x/sync v0.10.0
go: added golang.org/x/tools v0.28.0
$ cat go.mod
module demo
go 1.24
tool golang.org/x/tools/cmd/stringer
require (
golang.org/x/mod v0.22.0 // indirect
golang.org/x/sync v0.10.0 // indirect
golang.org/x/tools v0.28.0 // indirect
)
```


我们看到：go.mod中require了stringer的依赖。

接下来，我们便可以用go install安装stringer了：

```
$ ls -l `which stringer` // old版本的stringer
-rwxr-xr-x 1 root root 6500561 1月 23 2024 /root/go/bin/stringer
$ gotip install tool
$ ls -l `which stringer`
-rwxr-xr-x 1 root root 7303970 12月 9 21:41 /root/go/bin/stringer
```


后续要更新stringer版本，可以直接使用go get -u：

```
$gotip get -u golang.org/x/tools/cmd/stringer
```


此外，除了手工编辑go.mod，添加依赖的tool外，我们也可以直接使用go get -tool像go.mod中添加依赖的tool，它们在效果上是等价的：

```
// 重置go.mod到最初状态
# cat go.mod
module demo
go 1.24
// 执行go get -tool
$gotip get -tool golang.org/x/tools/cmd/stringer
go: added golang.org/x/mod v0.22.0
go: added golang.org/x/sync v0.10.0
go: added golang.org/x/tools v0.28.0
$ cat go.mod
module demo
go 1.24
tool golang.org/x/tools/cmd/stringer
require (
golang.org/x/mod v0.22.0 // indirect
golang.org/x/sync v0.10.0 // indirect
golang.org/x/tools v0.28.0 // indirect
)
```


使用stringer时也无需手工敲入那么长的命令(go run golang.org/x/tools/cmd/stringer)，只需使用gotip tool stringer即可：

```
$ gotip tool stringer
Usage of stringer:
stringer [flags] -type T [directory]
stringer [flags] -type T files... # Must be a single package
For more information, see:
https://pkg.go.dev/golang.org/x/tools/cmd/stringer
Flags:
-linecomment
use line comment text as printed text when present
-output string
output file name; default srcdir/<type>_string.go
-tags string
comma-separated list of build tags to apply
-trimprefix prefix
trim the prefix from the generated constant names
-type string
comma-separated list of type names; must be set
```


go tool stringer就相当于go run golang.org/x/tools/cmd/stringer@v0.28.0了(注：v0.28.0是当前golang.org/x/tools的版本)。

tool directive和go工具链做了很好的融合，除了上面的命令外，还支持：

- go build tool构建module依赖的tool，并将构建出可执行文件放在当前目录下；
- go build -o bin/ tool将构建module依赖的tool，并将构建出可执行文件放在项目自己的bin目录下。

到这里，屏幕前的你可能会问一个问题：如果本地多个项目依赖同一个工具的不同版本，比如golangci-lint的v1.62.2和v1.62.0时，那么两个项目安装的golangci-lint是否会相互覆盖和影响呢？我们来验证一下，下面建立两个项目：tool-directive1和tool-directive2。

```
.
├── tool-directive1/
│ ├── go.mod
│ └── go.sum
└── tool-directive2/
├── go.mod
└── go.sum
```


我们先在tool-directive1下面执行下面命令添加对golangci-lint的依赖：

```
$gotip get -tool github.com/golangci/golangci-lint/cmd/golangci-lint
go: downloading github.com/golangci/golangci-lint v1.62.2
go: downloading github.com/gofrs/flock v0.12.1
go: downloading github.com/fatih/color v1.18.0
... ...
```


然后在同一个目录下，使用gotip tool golangci-lint执行该工具，查看其版本：

```
$ gotip tool golangci-lint --version
golangci-lint has version v1.62.2 built with devel go1.24-c8fb6ae6 Sun Dec 8 15:34:47 2024 +0000 from (unknown, modified: ?, mod sum: "h1:b8K5K9PN+rZN1+mKLtsZHz2XXS9aYKzQ9i25x3Qnxxw=") on (unknown)
```


我们看到tool-directive1依赖了v1.62.2版本的golangci-lint。不过你在执行上述命令时可能会注意到，这个命令的执行非常耗时，可能需要10~20s才能出结果。如果你再执行一次，它就可以瞬间输出结果，为什么会这样的？稍后我们给出答案。

现在我们切换到tool-directive2目录下，执行下面命令添加对golangci-lint v1.62.0版本的依赖：

```
$gotip get -tool github.com/golangci/golangci-lint/cmd/golangci-lint@v1.62.0
```


然后在同一个目录下，使用gotip tool golangci-lint执行该工具，查看其版本：

```
$gotip tool golangci-lint --version
golangci-lint has version v1.62.0 built with devel go1.24-c8fb6ae6 Sun Dec 8 15:34:47 2024 +0000 from (unknown, modified: ?, mod sum: "h1:/G0g+bi1BhmGJqLdNQkKBWjcim8HjOPc4tsKuHDOhcI=") on (unknown)
```


我们看到tool-directive2下得到的是v1.62.0版本的golangci-lint。并且我们会遇到同样的现象：第一次执行很慢，第二次执行就会瞬间出结果。

再回到tool-directive1下，看看它依赖的golangci-lint是否被覆盖了：

```
$gotip tool golangci-lint --version
golangci-lint has version v1.62.2 built with devel go1.24-c8fb6ae6 Sun Dec 8 15:34:47 2024 +0000 from (unknown, modified: ?, mod sum: "h1:b8K5K9PN+rZN1+mKLtsZHz2XXS9aYKzQ9i25x3Qnxxw=") on (unknown)
```


我们发现：两个项目下依赖的版本各自独立，并不会相互覆盖。

这其中的缘由又是什么呢？为什么使用go tool golangci-lint第一次执行会慢，而后续的执行就会飞快呢？下面的issue将回答这个问题。

Go 1.24 之前，cmd/go仅缓存编译后的包文件（build actions），而不缓存链接后的二进制文件（link actions）。不缓存二进制文件很大原因在于二进制文件比单个包对象文件大得多，并且它们不像包文件那样被经常重用。

不过上述1.1中，让go支持对依赖工具的管理以及让go tool支持自定义工具执行的issue让这个issue最终被纳入Go 1.24。该issue实现后，go run以及像上面那种go tool golangci-lint(本质上也是go run github.com/golangci/golangci-lint/cmd/golangci-lint@vx.y.z)的编译链接的结果会被缓存到go build cache中。这也是上面不同项目依赖同一工具不同版本时不会相互覆盖以及首次使用go tool执行依赖工具较慢的原因，第一次go tool执行会执行编译链接过程，之后的运行就会从缓存中直接找到缓存的文件并执行了。

由于这个issue会显著增大go build cache的磁盘空间占用，该issue也规定了，在[缓存执行定期清理](https://github.com/golang/go/issues/68872)的时候，**可执行文件缓存会优先于包缓存被优先清理掉**。

在Go 1.18及之后的版本中，cmd/go工具链在构建二进制文件时会嵌入依赖版本信息和VCS（版本控制系统）信息，这使得开发者可以更容易地追踪二进制文件的来源。然而，当使用go build命令构建主模块时，主模块的版本信息并不会被记录，而是显示为(devel)，这导致开发者需要使用外部构建脚本或-ldflags来手动设置版本信息。相比之下，go install命令会正确记录主模块的版本信息。

该issue就旨在让go build命令也能像go install一样，自动嵌入主模块的版本信息，从而避免开发者依赖外部构建脚本。

落地后，Go 1.24的go build命令会在编译后的二进制文件中包含版本信息。如果本地VCS（版本控制系统）标签可用，主模块的版本将从该标签中设置。如果没有本地VCS标签可用，则会生成一个伪版本（pseudo-version），通常包含时间戳和提交哈希。 此外，为了避免与已发布的版本混淆，go build还会在伪版本中添加一些特殊的标识符，例如devel，以表明这是一个本地构建的版本。如果有未提交的VCS更改，则会附加一个+dirty后缀。

使用-buildvcs=false标志可以省略二进制文件中的版本控制信息。

下面对比一下Go 1.24版本之前与Go 1.24版本在go build时生成的版本信息的差异：

以Go 1.23为例，其构建和安装的stringer的版本信息如下：

```
$go version -m `which stringer`
/root/go/bin/stringer: go1.23.0
... ...
```


而使用go1.24的build构建的stringer的版本信息如下：

```
$go version -m tool-directive1/bin/stringer
tool-directive1/bin/stringer: devel go1.24-c8fb6ae6 Sun Dec 8 15:34:47 2024 +0000
... ...
```


估计Go社区很少有人用过GOCACHEPROG，即便在Go 1.21版本之后，它是以实验特性的形式提供的，通过GOEXPERIMENT=cacheprog启用。这个特性是由Go语言元老[Brad Fitzpatrick](https://github.com/bradfitz)提出的，其主issue编号是[59719](https://github.com/golang/go/issues/59719)。

我们知道：Go语言的cmd/go工具已经具备了强大的缓存支持，但其缓存机制仅限于基于文件系统的缓存。这种缓存方式在某些场景下效率不高，尤其是在CI（持续集成）环境中，用户通常需要将GOCACHE目录打包和解压缩，这往往比CI操作本身还要慢。此外，用户可能希望利用位于网络上的共享缓存(比如S3)或公司内部的P2P缓存协议来提高缓存效率，但这些功能并不适合直接集成到cmd/go工具中。

为了解决上述问题，Brad Fitzpatrick提出了一个新的环境变量GOCACHEPROG，类似于现有的GOCACHE变量。通过设置GOCACHEPROG，用户可以指定一个外部程序，该程序将作为子进程运行，并通过标准输入/输出来与cmd/go工具进行通信。cmd/go工具将通过这个接口**与外部缓存程序交互**，外部程序可以根据需要实现任意的缓存机制和策略。

为此，Bradfitz在issue 59719中给出了交互的协议设计。cmd/go工具与外部缓存程序之间的通信基于JSON格式的消息。消息分为请求（ProgRequest）和响应（ProgResponse）。请求包括命令类型、操作ID（ActionID）、对象ID（ObjectID）等。响应则包括缓存命中与否、对象的磁盘路径等信息。

其中请求的命令类型有如下几种：

- get：从缓存中获取对象。
- put：将对象存入缓存。
- close：关闭缓存连接。

对于put请求，cmd/go工具会将对象的二进制数据通过base64编码后发送给外部程序。对于get请求，外部程序返回对象的磁盘路径。

在\$GOROOT/src/cmd/go/internal/cache/prog.go文件中可以看到具体协议相关的结构。

Bradfitz还给出了一个[外部cache的样例程序go-tool-cache](https://github.com/bradfitz/go-tool-cache)，还有开发者fork了该样例程序，将它改造为[以S3为后端cache的外部缓存程序](https://github.com/or-shachar/go-tool-cache/)。感兴趣的童鞋，可以按照这些样例程序的说明试验一下外部缓存功能。

在Go语言中，go get命令用于从远程代码仓库获取依赖包。通常，这些依赖包的导入路径是通过HTTP请求获取的，服务器会返回一个包含元标签（meta tag）的HTML页面，指示如何获取该包的源代码。然而，对于需要身份验证的私有仓库，go get无法直接工作，因为go get使用的是net/http.DefaultClient，它不知道如何处理需要身份验证的URL。具体来说，当go get尝试获取一个私有仓库的URL时，由于没有提供身份验证信息，服务器会返回401或403错误，导致go get无法继续执行。这个问题在企业环境中尤为常见，因为许多公司使用私有代码托管服务，而这些服务通常需要身份验证。

issue 26232为上述情况提供了一种方案，让go get能够支持需要身份验证的私有仓库，使得用户可以通过go get命令获取私有仓库中的代码：

```
$go get git.mycompany.com/private-repo
```


即使https://git.mycompany.com/private-repo需要身份验证，go get也能够正常工作。

方案采用了一种类似于Git凭证助手的机制，并通过新增的Go环境变量GOAUTH来指定一个或多个认证命令。go get在执行时会调用这些命令，获取身份验证信息，并在后续的HTTP请求中使用这些信息。

GOAUTH环境变量可以包含一个或多个认证命令，每个命令由空格分隔的参数列表组成，命令之间用分号分隔。go get会在每次需要进行HTTP请求时，首先检查缓存中的认证信息，如果没有匹配的认证信息，则会调用GOAUTH命令来获取新的认证信息。

通过go help goauth可以查看GOAUTH的详细用法，在Go 1.24中它支持如下认证命令：

- off：禁用GOAUTH功能
- netrc：从NETRC或用户主目录中的.netrc文件中获取访问凭证，这也是
**GOAUTH的默认值**。 - git dir：在指定目录dir中运行git credential fill并使用其凭证。go命令将运行git credential approve/reject来更新凭证助手的缓存。
- command：执行给定的命令（以空格分隔的参数列表），并将提供的头信息附加到 HTTPS 请求中。该命令必须按照以下格式生成输出：

```
Response = { CredentialSet } .
CredentialSet = URLLine { URLLine } BlankLine { HeaderLine } BlankLine .
URLLine = /* URL that starts with "https://" */ '\n' .
HeaderLine = /* HTTP Request header */ '\n' .
BlankLine = '\n' .
```


Go 1.24版本之前，Go已经支持了go test -json命令，旨在为测试过程提供结构化的JSON输出，便于工具解析和处理测试结果。然而，当测试或导入的包在构建过程中失败时，构建错误信息会与测试的JSON输出交织在一起，导致工具难以准确地将构建错误与受影响的测试包关联起来。这增加了工具处理go test -json输出的复杂性。

为了解决这个问题，issue 62067提出了为go build命令(包括go install)添加-json标志的建议，以便生成与go test -json兼容的结构化JSON输出。go test -json也得到了优化，现在在test时出现构建错误时，go test -json也会以json格式输出构建错误信息，与test结果的json内容可以很好的融合在一起。当然，你也可以通过GODEBUG=gotestjsonbuildtext=1继续让go test -json输出文本格式的构建错误信息，以保持与Go 1.24之前的情况一致。

## 2. 标准库

Go标准库向来是添加新特性的大户，不过鉴于变化太多，下面我们仅列举一些主要的变化点。

关于这个变化点，我在《[JSON包新提案：用“omitzero”解决编码中的空值困局](https://tonybai.com/2024/09/12/solve-the-empty-value-dilemma-in-json-encoding-with-omitzero/)》一文中有详细说明，请移步阅读，这里不赘述了。

### 2.2 [新增weak包和weak指针](https://github.com/golang/go/issues/67552)

weak包和weak指针是Go团队在设计和实现unique包时的“副产物”，Go团队认为weak指针可以给大家带来更灵活的内存管理机制，于是将其从internal中提到标准库中。我之前的《[Go weak包前瞻：弱指针为内存管理带来新选择](https://tonybai.com/2024/09/23/go-weak-package-preview/)》一文对weak包有详细说明，请移步阅读。

### 2.3 crypto: FIPS 140-3认证

在Go 1.24开发周期中，Go密码学小组与Russ Cox根据开发者日益增多的密码学合规性(满足FIPS 140)的需求反馈，决定对Go的加密库进行改造，以符合申请进行FIPS 140标准认证的要求。有关这个认证的issue和改动点(cl)都很多，大家可以阅读我的《[走向合规：Go加密库对FIPS 140的支持](https://tonybai.com/2024/11/16/go-crypto-and-fips-140/)》一文了解详情。

### 2.4 crypto：增加hkdf、pbkdf2、sha3等密码学包

读过我的《[Go开发者的密码学导航：crypto库使用指南](https://tonybai.com/2024/10/19/go-crypto-package-design-deep-dive)》一文的读者都知道：Go密码学团队维护的密码学包分布在Go标准库crypto目录和golang.org/x/crypto下面。Go密码学小组负责人[Roland Shoemaker认为当前这种”分割”的状态会带来一些问题](https://github.com/golang/go/issues/65269)：

- 用户困惑：用户经常对为什么某些加密库在x/crypto模块中，而另一些在标准库中感到困惑。这种困惑可能导致用户不愿意依赖x/crypto模块中的代码，因为他们误以为x/crypto中的代码是“实验性”的，质量或API稳定性不如标准库。
- 复杂的安全补丁流程：标准库依赖于x/crypto模块中的多个包（目前有7个），这些包需要被vendored。这种依赖关系增加了安全补丁的复杂性，因为需要一个特殊的第三方流程来处理这些包的补丁，而不是像标准库或x/crypto模块那样直接处理。
- 开发周期不一致：理论上，x/crypto模块是一个可以快速开发新加密算法或协议的地方，因为这些算法或协议的规范可能还在变化中。然而，实际上，x/crypto模块并没有被这样使用。如果开始这样做，反而会强化用户对x/crypto模块的误解。
- 特定包的快速开发需求：例如x/crypto/ssh包最近经历了非常快速的开发，许多用户希望立即使用新引入的功能和修复。如果将这个包移入标准库，可能会因为标准库的发布周期较慢而产生摩擦。

为此Shoemaker提议了一个将x/crypto下的包到标准库crypto目录下的方案，以简化Go语言加密库的管理和维护，提高用户对这些库的信任和使用率，方案的大致思路和步骤如下：

- 将x/crypto模块中的大部分包直接迁移到标准库的crypto/目录下，迁移过程应在单个标准库发布周期内完成，尽量接近发布周期的末尾，以避免需要同步两个版本的包。
- 迁移后，冻结x/crypto模块和标准库中的对应包，直到标准库重新开放，只接受标准库版本的更改。
- 使用构建标签（build tags）来区分迁移前后的版本，允许用户在不更新到最新Go版本的情况下继续使用x/crypto模块。
- 在迁移后的两个主要版本中（例如，假设在Go 1.24中完成迁移，则在Go 1.26中），移除旧的构建标签实现，只保留转发到标准库版本的包装器。
- 一些包由于其更新周期与标准库不一致，或者已经冻结/弃用，将不会迁移到标准库中。例如，x/crypto/x509roots包需要根据任意时间表进行更新，因此应移至独立的模块golang.org/x/x509roots。
- 一些已经弃用或冻结的包（如twofish、cast5、tea等）将保留在x/crypto模块中，并在v1版本中标记为冻结。
- x/crypto/ssh包由于其快速的开发周期，可能会在迁移时带来一些麻烦。虽然可以考虑将其推迟迁移，但最终仍建议将其移入标准库。

基于上述方案，Go 1.24版本中，Go密码学团队完成了hkdf、pbkdf2、sha3和mlkem等包的迁移。当然这次迁移与[Go密码学包要进行FIPS 140-3认证](https://github.com/golang/go/issues/69536)也有着直接的联系。

这里面值得一提的是mklem包，它实现了[NIST FIPS 203](https://doi.org/10.6028/NIST.FIPS.203)中指定的抗量子密钥封装方法ML-KEM（以前称为Kyber），也是Go密码学包中第一个[后量子密码学](https://en.wikipedia.org/wiki/Post-quantum_cryptography)包。

目录遍历漏洞（Directory Traversal Vulnerabilities）和符号链接遍历漏洞（Symlink Traversal Vulnerabilities）是常见的安全漏洞。攻击者通过提供相对路径（如”../../../etc/passwd”）或创建符号链接，诱使程序访问其本不应访问的文件，从而导致安全问题。例如，[CVE-2024-3400 ](https://nvd.nist.gov/vuln/detail/CVE-2024-3400)是一个最近的真实案例，展示了目录遍历漏洞如何导致远程代码执行。

在Go中，虽然可以通过 filepath.IsLocal等函数来验证文件名，但防御符号链接遍历攻击较为困难。现有的os.Open和os.Create等函数在处理不受信任的文件名时，容易受到这些攻击的影响。

为了解决这些问题，issue 67002提出了在os包中添加几个新的函数和方法，以安全地打开文件并防止目录遍历和符号链接遍历攻击。

最初该提案提出新增一些安全访问文件系统的API函数，在讨论过程中，Russ Cox 提出了一个更为简洁的方案，避免了引入大量新的 API，而是通过引入一个新的类型 Dir 来表示受限的文件系统根目录。这个方案最终奠定了该提案的最终实现。

最终Go在os包中引入了一个新的Root类型，并基于该类型提供了在特定目录内执行文件系统操作的能力。os.OpenRoot函数打开一个目录并返回一个os.Root。os.Root上的方法仅限于在该目录内操作，并且不允许路径引用目录外的位置，包括跟随符号链接指向目录外的路径。下面是一些Root类型的常用方法：

- os.Root.Open 打开一个文件以供读取。
- os.Root.Create 创建一个文件。
- os.Root.OpenFile 是通用的打开调用。
- os.Root.Mkdir 创建一个目录。

下面我们用一个示例对比一下通过os.Root进行的文件系统操作与传统文件系统操作的差异：

```
// go1.24-foresight/stdlib/osroot/main.go
package main
import (
"fmt"
"os"
)
func main() {
// 使用 os.Root 访问相对路径
root, err := os.OpenRoot(".") // 打开当前目录作为根目录
if err != nil {
fmt.Println("Error opening root:", err)
return
}
defer root.Close()
// 尝试访问相对路径 "../passwd"
file, err := root.Open("../passwd")
if err != nil {
fmt.Println("Error opening file with os.Root:", err)
} else {
fmt.Println("Successfully opened file with os.Root")
file.Close()
}
// 传统的 os.OpenFile 方式
// 尝试访问相对路径 "../passwd"
file2, err := os.OpenFile("../passwd", os.O_RDONLY, 0644)
if err != nil {
fmt.Println("Error opening file with os.OpenFile:", err)
} else {
fmt.Println("Successfully opened file with os.OpenFile")
file2.Close()
}
}
```


运行上述代码，我们得到：

```
$gotip run main.go
Error opening file with os.Root: openat ../passwd: path escapes from parent
Successfully opened file with os.OpenFile
```


我们看到：当代码通过os.Root返回的目录来尝试访问相对路径”../passwd”时，由于os.Root限制了操作仅限于根目录内，因此会返回错误。

从安全角度来看，Go 1.24之后，建议搭建多多使用这种安全操作文件系统的方式，如果你的文件操作都局限在一个目录下。

Go 1.24版本之前，Go提供了runtime.SetFinalizer函数用于对象的终结处理。然而，SetFinalizer的使用存在许多问题和限制，Michael Knyszek总结了下面几点：

- 必须引用分配的第一个字：SetFinalizer必须引用分配的第一个字，这要求程序员了解什么是“分配”，而这一概念在语言中通常不暴露。
- 每个对象只能有一个终结器：不能为同一个对象设置多个终结器。
- 引用循环问题：如果对象参与了引用循环，且该对象有终结器，那么该对象将不会被释放，终结器也不会运行。
- GC周期问题：有终结器的对象至少需要两个GC周期才能被释放。

后面两个问题主要源于SetFinalizer允许对象复活（object resurrection），这使得对象的清理变得复杂且不可靠。

为了解决上述问题，，Michael Knyszek提出了一个新的API runtime.AddCleanup，并建议正式弃用runtime.SetFinalizer。AddCleanup的设计目标是解决SetFinalizer的诸多问题，特别是避免对象复活，从而允许对象的及时清理，并支持对象的循环清理。

AddCleanup函数的原型如下：

```
func AddCleanup[T, S any](ptr *T, cleanup func(S), arg S) Cleanup
```


AddCleanup函数将一个清理函数附加到ptr。当ptr不再可达时，运行时会在一个单独的goroutine中调用 cleanup(arg)。

AddCleanup的一个典型的用法如下：

```
f, _ := Open(...)
runtime.AddCleanup(f, func(fd uintptr) { syscall.Close(fd) }, f.Fd())
```


通常，ptr是一个包装底层资源的对象（例如上面典型用法中的那个包装操作系统文件描述符的File对象），arg是底层资源（例如操作系统文件描述符），而清理函数释放底层资源（例如，通过调用close系统调用）。

AddCleanup对ptr的约束很少，支持为同一个指针附加多个清理函数。不过，如果ptr可以从cleanup或arg中可达，ptr将永远不会被回收，清理函数也永远不会运行。作为一种简单的保护措施，如果arg等于ptr，AddCleanup会引发panic。清理函数的运行顺序没有指定。特别是，如果几个对象相互指向并且同时变得不可达，它们的清理函数都可以运行，并且可以以任何顺序运行。即使对象形成一个循环也是如此。

cleanup(arg)调用并不总是保证运行，特别是它不保证在程序退出之前能运行。

清理函数可能在对象变得不可达时立即运行。为了正确使用清理函数，程序必须确保对象在清理函数安全运行之前保持可达。存储在全局变量中的对象，或者可以通过从全局变量跟踪指针找到的对象，是可达的。函数参数或方法接收者可能在函数最后一次提到它的地方变得不可达。为了确保清理函数不会过早调用，我们可以将对象传递给KeepAlive函数，以保证对象在保持可达的最后一个点之后依然可达。

到这里，也许一些读者想到了RAII(Resource Acquisition Is Initialization），RAII的核心思想是将资源的获取和释放与对象的生命周期绑定在一起，从而确保资源在对象不再使用时能够被正确释放。似乎AddCleanup可以用于实现Go版本的RAII，下面是一个示例：

```
// go1.24-foresight/stdlib/addcleanup/main.go
package main
import (
"fmt"
"os"
"runtime"
"syscall"
"time"
)
type FileResource struct {
file *os.File
}
func NewFileResource(filename string) (*FileResource, error) {
file, err := os.Open(filename)
if err != nil {
return nil, err
}
// 使用 AddCleanup 注册清理函数
fd := file.Fd()
runtime.AddCleanup(file, func(fd uintptr) {
fmt.Println("Closing file descriptor:", fd)
syscall.Close(int(fd))
}, fd)
return &FileResource{file: file}, nil
}
func main() {
fileResource, err := NewFileResource("example.txt")
if err != nil {
fmt.Println("Error opening file:", err)
return
}
// 模拟使用 fileResource
_ = fileResource
fmt.Println("File opened successfully")
// 当 fileResource 不再被引用时，AddCleanup 会自动关闭文件
fileResource = nil
runtime.GC() // 强制触发 GC，以便清理 fileResource
time.Sleep(time.Second * 5)
}
```


运行上述代码得到如下结果：

```
$gotip run main.go
File opened successfully
Closing file descriptor: 3
```


的确，在Go中，runtime.AddCleanup可以用来模拟RAII机制，但与传统的RAII有一些不同，在Go中，资源获取通常是通过显式的函数调用来完成的，例如打开文件等，而不是像C++那样在构造函数中隐式完成。并且，资源的释放由Go GC回收对象时触发。如果要实现C++那样的RAII，需要我们自行做一些封装。

在Go语言中，基准测试（benchmarking）是通过testing.B类型的b.N来实现的。b.N表示基准测试需要执行的迭代次数。然而，这种设计存在一些问题：

- 容易忘记使用b.N：在某些情况下，开发者可能会忘记使用b.N，导致基准测试无法正确执行。
- 误用b.N：开发者可能会错误地将b.N用于其他目的，例如调整算法输入的大小，而不是作为迭代次数。
- 复杂的计时器管理：基准测试框架无法知道b.N循环何时开始，因此如果基准测试有复杂的设置（setup），开发者需要手动调用ResetTimer来重置计时器，这提高了开发人员使用benchmark函数的门槛，还非常容易出错。

为了解决上述问题，Austin Clements提议在testing.B中添加一个新的方法Loop，并鼓励开发者使用Loop而不是b.N：

```
func (b *B) Loop() bool
func Benchmark(b *testing.B) {
...(setup)
for b.Loop() {
// … benchmark body …
}
...(cleanup)
}
```


显然新Loop方法以及基于新Loopfang方法的“新Benchmark”函数有如下优点：

- 避免误用b.N：Loop方法明确地用于基准测试的迭代，开发者无法将其用于其他目的。
- 自动计时器管理：基准测试框架可以仅记录发生在基准测试操作期间(即for循环内部)的时间和其他指标，因此开发者不再需要手动调用ResetTimer或担心setup的复杂性了。
- 减少重复设置：Loop方法可以在内部处理迭代启动（ramp-up），这意味着基准测试之前的setup只会执行一次，而不是在每次启动步骤中重复执行。这对于具有复杂设置的基准测试来说，可以节省大量时间。
- 防止编译器优化：对go编译器来说，Loop方法本身就是一个的明显信号，可阻止某些优化（如内联），以确保基准测试结果的有效性。
- 支持更丰富的统计分析：将来，Loop方法可以收集值分布而不是仅仅平均值，从而提供更深入的基准测试结果分析。

这里也**强烈建议大家在Go 1.24及以后版本中，使用基于B.Loop的新基准测试函数**。

在Go语言中，测试并发代码一直是一个具有挑战性的任务。传统的测试方法通常依赖于真实的系统时钟和同步机制，这会导致测试变得缓慢且容易出现不确定性（即“flaky”测试）。例如，测试一个带有超时机制的并发缓存时，测试代码可能需要等待几秒钟来验证缓存条目是否在预期时间内过期。这种等待不仅增加了测试的执行时间，还可能导致测试在某些情况下失败，尤其是在CI系统负载较高或执行环境不稳定的情况下。

为了解决这些问题，Go社区提出了一个[新的testing/synctest包](https://github.com/golang/go/issues/67434)，旨在简化并发代码的测试。该包的核心思想是通过使用虚拟时钟和goroutine组(也称为气泡(bubble)来控制并发代码的执行，从而使测试既快速又可靠。下面是synctest包的API：

```
func Run(f func()) {
synctest.Run(f)
}
func Wait() {
synctest.Wait()
}
```


我们看到synctest包对外仅暴露两个公开函数。

Run函数在一个新的goroutine中执行f函数，并创建一个独立的goroutine组（气泡），确保所有相关的goroutine都在虚拟时钟的控制下执行。气泡内的goroutine不能与气泡外的goroutine直接交互，否则会引发panic。如果所有goroutine都被阻塞且没有定时器被调度，Run会引发panic。Run 会在气泡中的所有goroutine退出后返回。

Wait函数调用后将阻塞，直到当前气泡中的所有其他goroutine都处于持久阻塞状态。该函数用于确保在虚拟时间推进后，所有相关的goroutine都已经完成其工作。即确保在测试继续之前所有后台goroutine都已空闲或退出。如果从非气泡的goroutine调用Wait，或者同一气泡中的两个goroutine同时调用Wait，会引发panic。阻塞在系统调用或外部事件（如网络操作）的goroutine不是持久阻塞的，Wait不会等待这些goroutine。

这里再明确一下上面API说明中提到的各种概念：

- goroutine组（气泡）

Run函数创建的goroutine及其间接启动的所有goroutine形成一个独立的“气泡”。气泡内的goroutine使用虚拟时钟，并且气泡内的所有操作（如通道、定时器等）都与该气泡关联。气泡内的goroutine不能与气泡外的goroutine直接交互。

- 虚拟时钟

虚拟时钟的初始时间为2000-01-01 00:00:00 UTC。每个气泡有一个虚拟时钟，它只有在所有goroutine都处于阻塞状态时才会推进。这意味着测试代码可以精确控制时间的流逝，而不会受到真实系统时钟的限制。

- 持久阻塞

一个goroutine如果只能被气泡内的另一个goroutine解除阻塞，则称其为持久阻塞。以下操作会使goroutine持久阻塞：

```
- 在气泡内向通道发送或接收数据
- 在select语句中，每个case都是气泡内的通道
- sync.Cond.Wait
- time.Sleep
```


下面是一个使用testing/synctest进行测试的简单示例，我们有一个Cache结构：

```
// go1.24-foresight/stdlib/synctest/cache.go
package main
import (
"sync"
"time"
)
// Cache 是一个泛型并发缓存，支持任意类型的键和值。
type Cache[K comparable, V any] struct {
mu sync.Mutex
items map[K]cacheItem[V]
expiry time.Duration
creator func(K) V
}
// cacheItem 是缓存中的单个条目，包含值和过期时间。
type cacheItem[V any] struct {
value V
expiresAt time.Time
}
// NewCache 创建一个新的缓存，带有指定的过期时间和创建新条目的函数。
func NewCache[K comparable, V any](expiry time.Duration, f func(K) V) *Cache[K, V] {
return &Cache[K, V]{
items: make(map[K]cacheItem[V]),
expiry: expiry,
creator: f,
}
}
// Get 返回缓存中指定键的值，如果键不存在或已过期，则创建新条目。
func (c *Cache[K, V]) Get(key K) V {
c.mu.Lock()
defer c.mu.Unlock()
// 检查缓存中是否存在该键
item, exists := c.items[key]
// 如果键存在且未过期，返回缓存的值
if exists && time.Now().Before(item.expiresAt) {
return item.value
}
// 如果键不存在或已过期，创建新条目
value := c.creator(key)
c.items[key] = cacheItem[V]{
value: value,
expiresAt: time.Now().Add(c.expiry),
}
return value
}
```


上述代码实现了一个简单的并发缓存，支持泛型键和值，并且具有过期机制。通过使用sync.Mutex来保护对缓存条目的并发访问，确保了线程安全。Get方法在键不存在或已过期时，会调用creator函数创建新条目，并更新缓存。

下面是对上面Cache结构进行并发测试的代码：

```
// go1.24-foresight/stdlib/synctest/cache_test.go
package main
import (
"testing"
"testing/synctest"
"time"
)
func TestCacheEntryExpires(t *testing.T) {
synctest.Run(func() {
count := 0
c := NewCache(2*time.Second, func(key string) int {
count++
return count
})
// Get an entry from the cache.
if got, want := c.Get("k"), 1; got != want {
t.Errorf("c.Get(k) = %v, want %v", got, want)
}
// Verify that we get the same entry when accessing it before the expiry.
time.Sleep(1 * time.Second)
synctest.Wait()
if got, want := c.Get("k"), 1; got != want {
t.Errorf("c.Get(k) = %v, want %v", got, want)
}
// Wait for the entry to expire and verify that we now get a new one.
time.Sleep(3 * time.Second)
synctest.Wait()
if got, want := c.Get("k"), 2; got != want {
t.Errorf("c.Get(k) = %v, want %v", got, want)
}
})
}
```


通过使用synctest.Run和synctest.Wait，上述测试代码能够在虚拟时钟的控制下**验证Cache的过期机制**。synctest.Run创建了一个独立的goroutine组，确保所有相关的goroutine都在虚拟时钟的控制下执行。synctest.Wait确保在虚拟时间推进后，所有相关的goroutine都已经完成其工作。

使用gotip执行该测试：

```
$GOEXPERIMENT=synctest gotip test -v
=== RUN TestCacheEntryExpires
--- PASS: TestCacheEntryExpires (0.00s)
PASS
ok demo 0.002s
```


我们可以瞬间得到结果，而**无需等待代码中的Sleep秒数**。

### 2.9 其他一些变化

slog包添加包级变量slog.DiscardHandler （类型为slog.Handler ），它将丢弃所有日志输出。

下面是五个返回迭代器的新增函数，以strings包为例：

```
- func Lines(s string) iter.Seq[string]
返回一个迭代器，遍历字符串s中以换行符结尾的行。
- func SplitSeq(s, sep string) iter.Seq[string]
返回一个迭代器，遍历s中由sep分隔的所有子字符串。
- func SplitAfterSeq(s, sep string) iter.Seq[string]
返回一个迭代器，遍历s中在每个sep实例之后分割的子字符串。
- func FieldsSeq(s string) iter.Seq[string]
返回一个迭代器，遍历s中由空白字符（由unicode.IsSpace定义）分隔的子字符串。
- func FieldsFuncSeq(s string, f func(rune) bool) iter.Seq[string]
返回一个迭代器，遍历s中由满足f(c)的Unicode码点分隔的子字符串。
```


和weak包一样，HashTrieMap同样是实现unique包的副产品，但它的性能很好，在很多情况下都要比sync.Map快很多。于是Michael Knyszek使用HashTrieMap替换了sync.Map的底层实现。

当然，如果你不满意HashTrieMap的表现，你也可以使用GOEXPERIMENT=nosynchashtriemap恢复到sync.Map之前的实现。

在Go语言的net/http包中，HTTP/2的支持默认是通过TLS加密的连接来实现的，通常称为”h2″。然而，HTTP/2也可以在不加密的TCP连接上运行，这种模式被称为”h2c”（HTTP/2 Clear Text）。尽管golang.org/x/net/http2/h2c包提供了对h2c的支持，但这种支持并不直接集成到net/http包中，导致用户在使用h2c时需要进行复杂的配置和处理。因此，社区提出了将h2c支持直接集成到net/http包中的issue，以简化用户的使用体验。

直接集成h2c支持后，将使得Go语言的HTTP/2功能更加完整，用户可以更方便地在未加密的连接上使用HTTP/2。

## 3. 其它

Go语言在WebAssembly（Wasm）的支持方面已经有了一定的进展，特别是在[Go 1.21版本](https://tonybai.com/2023/08/20/some-changes-in-go-1-21/)引入了[go:wasmimport指示符](https://github.com/golang/go/issues/59149)，使得[Go代码可以调用Wasm宿主定义的函数](https://go.dev/blog/wasi)。然而，目前仍然无法从Wasm宿主调用Go代码。这对于一些需要扩展功能的应用来说是一个限制，例如Envoy、Istio、VS Code等应用，它们允许通过调用Wasm编译的代码来扩展功能。但Go目前无法支持这些应用，因为Go编译的Wasm模块中唯一导出的函数是_start，对应于main包中的main函数。

但Go社区对导出Go函数为wasm有着迫切的需求，同时，导出函数到Wasm宿主也是实现GOOS=wasip2的必要条件([wasip2是WASI规范的预览2版本](https://github.com/WebAssembly/WASI/blob/main/preview2/README.md))。

于是issue 65199给出了导出Go函数到Wasm的落地方案。该issue提议在库模式下(即导出的Go函数供其他基于wasm运行时库开发的应用使用)，重用-buildmode构建标志值c-shared，用于wasip1。它现在向编译器发出信号，要求用_initialize函数替换_start函数，该函数执行运行时和包的初始化：

```
$gotip help buildmode
... ...
-buildmode=c-shared
Build the listed main package, plus all packages it imports,
into a C shared library. The only callable symbols will
be those functions exported using a cgo //export comment.
On wasip1, this mode builds it to a WASI reactor/library,
of which the callable symbols are those functions exported
using a //go:wasmexport directive. Requires exactly one
main package to be listed.
... ...
```


新增一个编译器指示符go:wasmexport，用于向编译器发出信号，表明某个函数应该使用Wasm导出（Wasm export），在生成的Wasm二进制文件中导出。该指示符只能在GOOS=wasip1时使用，否则会导致编译失败。

```
//go:wasmexport name
```


其中name是导出函数的名称，该参数是必需的。**该指示符只能用于函数，不能用于方法**。

该issue由Johan Brandhorst提出，但最终是由CherryMui给出了最终实现，并且CherryMui还给出了一个[应用go:wasmexport的example](https://go.googlesource.com/scratch/+/refs/heads/master/cherry/wasmtest/)，这个example演示了go:wasmexport在库模式下的应用方法。例子代码较多，这里我做了一个裁剪，下面是裁剪后的代码和使用方法，大家可以参考一下。

示例的结构如下：

```
$tree -F ./wasmtest
./wasmtest
├── Makefile
├── go.mod
├── go.sum
├── testprog/
│ └── x.go
└── w.go
```


其中testprog/x.go中导出了一个Add函数：

```
// go1.24-foresight/wasmtest/testprog/x.go
package main
func init() {
println("init function called")
}
//go:wasmexport Add
func Add(a, b int64) int64 {
return a+b
}
func main() {
println("hello")
}
```


我们将x.go编译为x.wasm文件：

```
$GOARCH=wasm GOOS=wasip1 gotip build -buildmode=c-shared -o x.wasm ./testprog
```


然后在w.go中使用x.wasm中的Add函数：

```
// go1.24-foresight/wasmtest/w.go
package main
import (
"context"
"fmt"
"os"
"github.com/tetratelabs/wazero"
"github.com/tetratelabs/wazero/api"
"github.com/tetratelabs/wazero/imports/wasi_snapshot_preview1"
)
func main() {
ctx := context.Background()
r := wazero.NewRuntime(ctx)
defer r.Close(ctx)
buf, err := os.ReadFile(os.Args[1])
if err != nil {
panic(err)
}
config := wazero.NewModuleConfig().
WithStdout(os.Stdout).WithStderr(os.Stderr).
WithStartFunctions() // don't call _start
wasi_snapshot_preview1.MustInstantiate(ctx, r)
m, err := r.InstantiateWithConfig(ctx, buf, config)
if err != nil {
panic(err)
}
// get export functions from the module
F := func(a int64, b int64) int64 {
exp := m.ExportedFunction("Add")
r, err := exp.Call(ctx, api.EncodeI64(a), api.EncodeI64(b))
if err != nil {
panic(err)
}
rr := int64(r[0])
fmt.Printf("host: Add %d + %d = %d\n", a,b,rr)
return rr
}
// Library mode.
entry := m.ExportedFunction("_initialize")
fmt.Println("Library mode: initialize")
_, err = entry.Call(ctx)
if err != nil {
panic(err)
}
fmt.Println("\nLibrary mode: call export functions")
println(F(5,6))
}
```


运行上述w.go，我们将得到以下预期结果：

```
$gotip run w.go ./x.wasm
Library mode: initialize
init function called
Library mode: call export functions
host: Add 5 + 6 = 11
11
```


### 3.2 移植(porting)

- Linux：要求内核版本不低于3.2。
- macOS：Go 1.24是支持macOS 11 Big Sur的最后一个版本。
- Windows：提升对Nano Server和内置服务帐户的支持，并修复域环境中的性能问题。
- 支持的Unicode版本升级到15.1.0。

## 4. 小结

本文详细介绍了即将发布的Go 1.24版本在工具链和标准库方面的重要新特性。这些新特性不仅简化了工具的使用，提升了开发体验，还增强了标准库的功能和安全性，特别是在加密、并发测试等方面。通过这些改进，Go语言将继续朝着更高效、更安全、更易用的方向发展。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.24-foresight)下载。

## 5. 参考资料

[Go 1.24 milestone](https://github.com/golang/go/milestone/322)– https://github.com/golang/go/milestone/322[Go 1.24 Release Notes Draft](https://tip.golang.org/doc/go1.24)– https://tip.golang.org/doc/go1.24[Go Release Dashboard](https://dev.golang.org/release)– https://dev.golang.org/release[Go spec tip](https://tip.golang.org/ref/spec)– https://tip.golang.org/ref/spec

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