---
title: Go modules：最小版本选择
url: https://tonybai.com/2019/12/21/go-modules-minimal-version-selection/
published: '2019-12-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go modules：最小版本选择

## 一. 介绍

每个[依赖管理解决方案](https://tonybai.com/2019/09/21/brief-history-of-go-package-management/)都必须解决选择依赖项版本的问题。[当前存在的许多版本](https://tonybai.com/2017/06/08/first-glimpse-of-dep/)选择算法都试图识别任何依赖项的“最新最大(latest greatest)”版本。如果您认为[语义版本控制(sematic versioning)](https://semver.org)将被正确应用并且这种社会契约得到遵守，那么这是有道理的。在这样的情况下，依赖项的“最新最大”版本应该是最稳定和安全的版本，并且应与较早版本具有向后兼容性。至少在相同的主版本(major verion)依赖树中是如此。

[Go](https://tonybai.com/tag/golang)决定采用其他方法，[Russ Cox](https://swtch.com/%7Ersc/)花费了大量时间和精力[撰写文章](https://research.swtch.com/vgo)和[演讲探讨](https://www.youtube.com/watch?v=F8nrpe0XWRg)Go团队的版本选择方法，即最小版本选择或MVS(Minimal Version Selection)。从本质上讲，Go团队相信MVS为Go程序实现痴线持久的和可重复的构建提供了最佳的方案。我建议大家阅读[这篇文章](https://research.swtch.com/vgo-principles)以了解Go团队为什么相信这一点。

在本文中，我将尽最大努力解释MVS语义，展示一个实际的Go语言示例，并实际使用MVS算法。

## 二. MVS语义

将Go的依赖项版本选择算法命名为“最小版本选择”是有点用词不当，但是一旦您了解了它的工作原理，您会发现这个名称真的很贴切。如我之前所述，许多选择算法会选择依赖项的“最新最大”版本。我喜欢将MVS视为选择“最新非最大(latest non-greatest)”版本的算法。并不是说MVS不能选择“最新最大”，而是只要项目中的任何依赖项都不需要“最新最大”，那么就不需要该版本。

为了更好地理解这一点，让我们创建一种情况，其中几个module（A，B和C）依赖于同一module（D），但是每个module都需要不同的版本。

![img{512x368}](../../assets/961bfeffda207163.png)


上图显示了module A，B和C如何分别独立地需要module D和各自需要D的不同版本。

如果我启动一个需要module A的项目，那么为了构建代码，我还需要module D。module D可能有很多版本可供选择。例如，假设module D代表sirupsen的logrus module。我可以要求Go向我提供module D所有已存在（打tag)的版本列表。

清单1：

```
$ go list -m -versions github.com/sirupsen/logrus
github.com/sirupsen/logrus v0.1.0 v0.1.1 v0.2.0
v0.3.0 v0.4.0 v0.4.1 v0.5.0 v0.5.1 v0.6.0 v0.6.1
v0.6.2 v0.6.3 v0.6.4 v0.6.5 v0.6.6 v0.7.0 v0.7.1
v0.7.2 v0.7.3 v0.8.0 v0.8.1 v0.8.2 v0.8.3 v0.8.4
v0.8.5 v0.8.6 v0.8.7 v0.9.0 v0.10.0 v0.11.0 v0.11.1
v0.11.2 v0.11.3 v0.11.4 v0.11.5 v1.0.0 v1.0.1 v1.0.3
v1.0.4 v1.0.5 v1.0.6 v1.1.0 v1.1.1 v1.2.0 v1.3.0
v1.4.0 v1.4.1 v1.4.2
```


清单2显示了module D存在的所有版本，我们看到其中显示的“最新最大”版本为1.4.2。

该项目应选择哪个版本的module D呢？确实有两种选择。首选是选择“最新的”版本（在主要版本为1的这一行中），即v1.4.2。第二个选择是选择module A所需的版本v1.0.6。

像[dep](https://tonybai.com/2017/06/08/first-glimpse-of-dep/)这样的依赖工具将选择v1.4.2版，并在语义版本化和遵守社会契约的前提下可以正常工作。但是，考虑到Russ Cox在[这里](https://research.swtch.com/vgo-principles)阐述的一些原因，Go会尊重module A的要求并选择版本1.0.6。在需要module的项目的所有依赖项的当前所需版本集合中，Go会选择“最小”版本。换句话说，现在只有module A需要module D，而module A已指定它要求的版本为v1.0.6，所需版本集合中只有v1.0.6，因此Go选择的module D的版本即是它。

如果我引入要求项目导入module B的新代码时会怎样？将module B导入项目后，Go会将项目的module D版本从v1.0.6升级到v1.2.0。Go再次在项目依赖项module A和B的当前所需版本集合(v1.0.6和v1.2.0)中选择了module D的“最小”版本。

如果我再次引入需要项目导入module C的新代码时会怎样？Go将从当前所需版本集合（v1.0.6，v1.2.0，v1.3.2）中选择最新版本（v1.3.2）。请注意，版本v1.3.2仍然是module D（v1.4.2）的“最小”版本，而不是“最新最大”版本。

最后，如果删除刚刚添加的依赖module C的代码会怎样？Go会将项目锁定到module D的版本v1.3.2上。降级到版本v1.2.0将是一个更大的更改，而Go知道版本v1.3.2可以正常并稳定运行，因此版本v1.3.2仍然是module D的“最新但非最大(latest non-greatest)“版本。另外，module文件(go.mod)仅维护快照，而不是日志。没有有关历史撤消或降级的信息。

这就是为什么我喜欢将MVS视为选择“最新非最大(latest non-greatest)”module 版本的算法的原因。希望您现在可以理解为什么Russ Cox在命名算法时选择名称“minimal”。

## 三. 示例项目

有了上述基础，我将用一个示例项目让你看到Go和MVS算法实际是如何工作的。在此项目中，module D将用[logrus module](https://tonybai.com/2018/01/13/the-problems-i-encountered-when-writing-go-code-issue-1st/)代表，而该项目将直接依赖于[rethinkdb-go](https://github.com/rethinkdb/rethinkdb-go)（moduleA）和[golib](https://github.com/Bhinneka/golib)（moduleB）module。rethinkdb-go和golib module直接依赖[logrus](https://github.com/sirupsen/logrus) module，并且每个module都需要一个不同的logrus版本，并且这些版本都不是logrus的“最新”版本。

![img{512x368}](../../assets/094212e968d430ae.png)


上图显示了三个module之间的独立关系。首先，我将创建项目，初始化module，然后加载[VS Code](https://tonybai.com/2016/12/23/write-go-code-in-vscode/)。

清单2：

```
$ cd $HOME
$ mkdir app
$ mkdir app/cmd
$ mkdir app/cmd/db
$ touch app/cmd/db/main.go
$ cd app
$ go mod init app
$ code .
```


清单2显示了所有要运行的命令。运行这些命令后，以下代码应出现在VS Code中。

![img{512x368}](../../assets/53ef6c80751bf568.png)


上图显示了项目结构和module文件应包含的内容。有了这个，现在该添加使用rethinkdb-go module的代码了。

清单3：

https://play.golang.org/p/bc5I0Afxhvc

```
01 package main
02
03 import (
04 "context"
05 "log"
06
07 db "gopkg.in/rethinkdb/rethinkdb-go.v5"
08 )
09
10 func main() {
11 c, err := db.NewCluster([]db.Host{{Name: "localhost", Port: 3000}}, nil)
12 if err != nil {
13 log.Fatalln(err)
14 }
15
16 if _, err = c.Query(context.Background(), db.Query{}); err != nil {
17 log.Fatalln(err)
18 }
19 }
```


清单3引入了rethinkdb-go module的major版本v5。添加并保存此代码后，Go会查找、下载和提取module，并更新go.mod和go.sum文件。

清单4：

```
01 module app
02
03 go 1.13
04
05 require gopkg.in/rethinkdb/rethinkdb-go.v5 v5.0.1
```


清单4显示了go.mod需要rethinkdb-go module作为直接依赖项，并选择了v5.0.1版本，该版本是该module的“最新最大版本”。

清单5：

```
...
github.com/sirupsen/logrus v1.0.6 h1:hcP1GmhGigz/O7h1WVUM5KklBp1JoNS9FggWKdj/j3s=
github.com/sirupsen/logrus v1.0.6/go.mod h1:pMByvHTf9Beacp5x1UXfOR9xyW/9antXMhjMPG0dEzc=
...
```


清单5显示了go.sum文件中引入logrus module v1.0.6版本的两行。在这一点上，您可以看到MVS算法已经选择了满足rethinkdb-go module指定要求所需的logrus module的“最小”版本。记住logrus module的“最新最大”版本是1.4.2。

注意：go.sum文件不应用于理解依赖关系。我在上面所做的版本确定的操作是错误的，稍后我将向您展示确定项目所使用的版本的正确方法。


![img{512x368}](../../assets/0b2919738910be0c.png)


上图显示了Go将使用哪个版本的logrus module来构建项目。

接下来，我将添加引入对golib module有依赖关系的代码。

清单6：

https://play.golang.org/p/h23opcp5qd0

```
01 package main
02
03 import (
04 "context"
05 "log"
06
07 "github.com/Bhinneka/golib"
08 db "gopkg.in/rethinkdb/rethinkdb-go.v5"
09 )
10
11 func main() {
12 c, err := db.NewCluster([]db.Host{{Name: "localhost", Port: 3000}}, nil)
13 if err != nil {
14 log.Fatalln(err)
15 }
16
17 if _, err = c.Query(context.Background(), db.Query{}); err != nil {
18 log.Fatalln(err)
19 }
20
21 golib.CreateDBConnection("")
22 }
```


清单6向该程序添加了07和21行行代码。Go查找、下载并解压缩golib module后，以下更改将显示在go.mod文件中。

清单7：

```
01 module app
02
03 go 1.13
04
05 require (
06 github.com/Bhinneka/golib v0.0.0-20191209103129-1dc569916cba
07 gopkg.in/rethinkdb/rethinkdb-go.v5 v5.0.1
08 )
```


清单7显示go.mod文件已被修改为包括golib module的“最新最大”版本依赖关系，该版本恰好没有语义版本标签。

清单8：

```
...
github.com/sirupsen/logrus v1.0.6 h1:hcP1GmhGigz/O7h1WVUM5KklBp1JoNS9FggWKdj/j3s=
github.com/sirupsen/logrus v1.0.6/go.mod h1:pMByvHTf9Beacp5x1UXfOR9xyW/9antXMhjMPG0dEzc=
github.com/sirupsen/logrus v1.2.0 h1:juTguoYk5qI21pwyTXY3B3Y5cOTH3ZUyZCg1v/mihuo=
github.com/sirupsen/logrus v1.2.0/go.mod h1:LxeOpSwHxABJmUn/MG1IvRgCAasNZTLOkJPxbbu5VWo=
...
```


清单8显示了go.sum文件中的四行，现在包括logrus module的v1.0.6和v1.2.0版本。查看go.sum文件中列出的两个版本会带来两个问题：

- 为什么在go.sum文件中列出了两个版本？
- Go执行构建时将使用哪个版本？

Go团队的Bryan Mills很好地回答了go.sum文件中列出两个版本的原因。

“go.sum文件仍包含旧版本（1.0.6），因为其传递依赖的要求可能会影响其他module的选定版本。我们真的只需要为go.mod文件提供校验和，因为go.mod中声明了这些传递要求的内容，但是由于go mod tidy不够精确，最终我们也保留了源代码的校验和。” golang.org/issue/33008


现在仍然存在在构建项目时将使用哪个版本的logrus module的问题。要正确确定将使用哪些module及其版本，请不要查看该go.sum文件，而应使用go list命令。

清单9：

```
$ go list -m all | grep logrus
github.com/sirupsen/logrus v1.2.0
```


清单9显示了在构建项目时将使用logrus module的v1.2.0版本。该-m标志指示go list列出module而不是package。

查看module图可以更深入地了解项目对logrus module的要求。

清单10：

```
$ go mod graph | grep logrus
github.com/sirupsen/logrus@v1.2.0 github.com/pmezard/go-difflib@v1.0.0
github.com/sirupsen/logrus@v1.2.0 github.com/stretchr/objx@v0.1.1
github.com/sirupsen/logrus@v1.2.0 github.com/stretchr/testify@v1.2.2
github.com/sirupsen/logrus@v1.2.0 golang.org/x/crypto@v0.0.0-20180904163835-0709b304e793
github.com/sirupsen/logrus@v1.2.0 golang.org/x/sys@v0.0.0-20180905080454-ebe1bf3edb33
gopkg.in/rethinkdb/rethinkdb-go.v5@v5.0.1 github.com/sirupsen/logrus@v1.0.6
github.com/sirupsen/logrus@v1.2.0 github.com/konsorten/go-windows-terminal-sequences@v1.0.1
github.com/sirupsen/logrus@v1.2.0 github.com/davecgh/go-spew@v1.1.1
github.com/Bhinneka/golib@v0.0.0-20191209103129-1dc569916cba github.com/sirupsen/logrus@v1.2.0
github.com/prometheus/common@v0.2.0 github.com/sirupsen/logrus@v1.2.0
```


清单10显示了logrus module在项目中的关系。我将直接提取显示对logrus的依赖要求的行。

清单11：

```
gopkg.in/rethinkdb/rethinkdb-go.v5@v5.0.1 github.com/sirupsen/logrus@v1.0.6
github.com/Bhinneka/golib@v0.0.0-20191209103129-1dc569916cba github.com/sirupsen/logrus@v1.2.0
github.com/prometheus/common@v0.2.0 github.com/sirupsen/logrus@v1.2.0
```


在清单11中，这些行显示三个module（rethinkdb-go，golib和common）都需要logrus module。由于有了go list命令，我知道所需的最低版本为v1.2.0。

![img{512x368}](../../assets/6bb7e01421bbcc67.png)


上图展示了Go现在将使用哪个版本的logrus module来构建项目中的代码。

## 四. Go Mod Tidy

在将代码提交/推回存储库之前，请运行go mod tidy以确保module文件是最新且准确的。您在本地构建，运行或测试的代码将随时影响Go对module文件中内容的更新。运行go mod tidy将确保项目具有所需内容的准确和完整的快照，这将帮助您团队中的其他人和您的CI/CD环境。

清单12：

```
$ go mod tidy
go: finding github.com/Bhinneka/golib latest
go: finding github.com/bitly/go-hostpool latest
go: finding github.com/bmizerany/assert latest
```


清单12显示了运行go mod tidy后的输出结果。您会在输出中看到两个新的依赖项。这将更改module文件。

清单13：

```
01 module app
02
03 go 1.13
04
05 require (
06 github.com/Bhinneka/golib v0.0.0-20191209103129-1dc569916cba
07 github.com/bitly/go-hostpool v0.0.0-20171023180738-a3a6125de932 // indirect
08 github.com/bmizerany/assert v0.0.0-20160611221934-b7ed37b82869 // indirect
09 gopkg.in/rethinkdb/rethinkdb-go.v5 v5.0.1
10 )
```


清单13显示了go-hostpool和assert module被列为构建项目所需的间接module。之所以在此处列出它们，是因为这些项目当前与module机制不兼容。换句话说，这些项目的任何tag版本或master中“最新的”版本都不存在go.mod文件。

为什么运行go mod tidy后包含了这些module？我可以使用go mod why命令找出答案。

清单14：

```
$ go mod why github.com/hailocab/go-hostpool
# github.com/hailocab/go-hostpool
app/cmd/db
gopkg.in/rethinkdb/rethinkdb-go.v5
github.com/hailocab/go-hostpool
------------------------------------------------
$ go mod why github.com/bmizerany/assert
# github.com/bmizerany/assert
app/cmd/db
gopkg.in/rethinkdb/rethinkdb-go.v5
github.com/hailocab/go-hostpool
github.com/hailocab/go-hostpool.test
github.com/bmizerany/assert
```


清单14显示了为什么项目间接需要这些module。rethinkdb-go module需要go-hostpool module，而go-hostpool module需要assert module。

## 五. 升级依赖关系

该项目具有三个依赖项，每个依赖项都需要logrus module，其中当前正在选择logrus module的v1.2.0版本。在项目生命周期的某个时刻，升级直接和间接依赖关系以确保项目所需的代码是最新的并且可以利用新功能、错误修复和升级安全补丁将变得很重要。要进行升级，Go提供了go get命令。

在运行go get升级项目的依赖项之前，需要考虑几个选项。

### 使用MVS仅升级必需的直接和间接依赖项

我建议从这种升级开始，直到您了解更多有关项目和module的信息。这是的最保守的形式go get。

清单15：

```
$ go get -t -d -v ./...
```


清单15显示了如何使用MVS算法对那些必需依赖项的升级。下面是命令中一些命令行选型的定义。

- -t flag：考虑构建测试所需的module。
- -d flag：下载每个module的源代码，但不要构建或安装它们。
- -v flag：提供详细输出。
- ./… ：在整个源代码树中执行这些操作，并且仅更新所需的依赖项。

对当前项目运行此命令不会导致任何更改，因为该项目已经是最新版本，并且具有构建和测试该项目所需的最低版本。那是因为我刚运行了go mod tidy，项目是新的。

### 使用最新最大版本仅升级必需的直接和间接依赖项

这种升级会将整个项目的依赖性从“最小”提高到“最新最大”。所需要做的只是将-u标志添加到命令行。

清单16：

```
$ go get -u -t -d -v ./...
go: finding golang.org/x/net latest
go: finding golang.org/x/sys latest
go: finding github.com/hailocab/go-hostpool latest
go: finding golang.org/x/crypto latest
go: finding github.com/google/jsonapi latest
go: finding gopkg.in/bsm/ratelimit.v1 latest
go: finding github.com/Bhinneka/golib latest
```


清单16显示了运行带有-u标志的go get命令的输出。此输出无法说明真实情况。如果我问go list命令现在使用哪个版本的logrus module来构建项目，会发生什么情况呢？

清单17：

```
$ go list -m all | grep logrus
github.com/sirupsen/logrus v1.4.2
```


清单17显示了如何选择“最新”的logrus。为了使这一选择更加明确，对go.mod文件进行了更改。

清单18：

```
01 module app
02
03 go 1.13
04
05 require (
06 github.com/Bhinneka/golib v0.0.0-20191209103129-1dc569916cba
07 github.com/bitly/go-hostpool v0.0.0-20171023180738-a3a6125de932 // indirect
08 github.com/bmizerany/assert v0.0.0-20160611221934-b7ed37b82869 // indirect
09 github.com/cenkalti/backoff v2.2.1+incompatible // indirect
10 github.com/golang/protobuf v1.3.2 // indirect
11 github.com/jinzhu/gorm v1.9.11 // indirect
12 github.com/konsorten/go-windows-terminal-sequences v1.0.2 // indirect
13 github.com/sirupsen/logrus v1.4.2 // indirect
14 golang.org/x/crypto v0.0.0-20191206172530-e9b2fee46413 // indirect
15 golang.org/x/net v0.0.0-20191209160850-c0dbc17a3553 // indirect
16 golang.org/x/sys v0.0.0-20191210023423-ac6580df4449 // indirect
17 gopkg.in/rethinkdb/rethinkdb-go.v5 v5.0.1
18 )
```


清单18在第13行显示版本v1.4.2现在是项目中logrus module的选定版本。构建项目时，Go会注意module文件中的这一行。即使删除了对logrus module的依赖关系更改的代码，该项目的v1.4.2版现在也已被锁定。请记住，降级将是一个更大的变化，而v1.4.2版将不受影响。

go.sum文件中可以看到哪些更改？

清单19：

```
github.com/sirupsen/logrus v1.0.6/go.mod h1:pMByvHTf9Beacp5x1UXfOR9xyW/9antXMhjMPG0dEzc=
github.com/sirupsen/logrus v1.2.0 h1:juTguoYk5qI21pwyTXY3B3Y5cOTH3ZUyZCg1v/mihuo=
github.com/sirupsen/logrus v1.2.0/go.mod h1:LxeOpSwHxABJmUn/MG1IvRgCAasNZTLOkJPxbbu5VWo=
github.com/sirupsen/logrus v1.4.2 h1:SPIRibHv4MatM3XXNO2BJeFLZwZ2LvZgfQ5+UNI2im4=
github.com/sirupsen/logrus v1.4.2/go.mod h1:tLMulIdttU9McNUspp0xgXVQah82FyeX6MwdIuYE2rE=
```


清单19显示了go.sum文件中表示logrus的所有三个版本。正如上面的Bryan所解释的，这是因为传递要求可能会影响其他module的选定版本。

![img{512x368}](../../assets/4942b68d7d6530fb.png)


上图展示了Go现在将使用哪个版本的logrus module来构建项目中的代码。

### 使用最新最大版本升级所有直接和间接依赖项

您可以将./…选项替换为all来升级所有直接和间接依赖项，包括构建项目时也并不需要的依赖项。

清单20：

```
$ go get -u -t -d -v all
go: downloading github.com/mattn/go-sqlite3 v1.11.0
go: extracting github.com/mattn/go-sqlite3 v1.11.0
go: finding github.com/bitly/go-hostpool latest
go: finding github.com/denisenkom/go-mssqldb latest
go: finding github.com/hailocab/go-hostpool latest
go: finding gopkg.in/bsm/ratelimit.v1 latest
go: finding github.com/google/jsonapi latest
go: finding golang.org/x/net latest
go: finding github.com/Bhinneka/golib latest
go: finding golang.org/x/crypto latest
go: finding gopkg.in/tomb.v1 latest
go: finding github.com/bmizerany/assert latest
go: finding github.com/erikstmartin/go-testdb latest
go: finding gopkg.in/check.v1 latest
go: finding golang.org/x/sys latest
go: finding github.com/golang-sql/civil latest
```


清单20显示了现在为该项目找到、下载和提取了多少个依赖项。

清单21：

```
Added to Module File
cloud.google.com/go v0.49.0 // indirect
github.com/denisenkom/go-mssqldb v0.0.0-20191128021309-1d7a30a10f73 // indirect
github.com/google/go-cmp v0.3.1 // indirect
github.com/jinzhu/now v1.1.1 // indirect
github.com/lib/pq v1.2.0 // indirect
github.com/mattn/go-sqlite3 v2.0.1+incompatible // indirect
github.com/onsi/ginkgo v1.10.3 // indirect
github.com/onsi/gomega v1.7.1 // indirect
github.com/stretchr/objx v0.2.0 // indirect
google.golang.org/appengine v1.6.5 // indirect
gopkg.in/check.v1 v1.0.0-20190902080502-41f04d3bba15 // indirect
gopkg.in/yaml.v2 v2.2.7 // indirect
Removed from Module File
github.com/golang/protobuf v1.3.2 // indirect
```


清单21显示了对该go.mod文件的更改。添加了更多module，并删除了一个module。

注意：如果你使用vendor，则go mod vendor命令将从vendor文件夹中剥离test文件。


通常，通过go get升级项目的依赖项时不要使用all或-u选项。坚持只升级需要的module，并使用MVS算法选择这些module及其版本。必要时手动更改为特定的module版本。手动更改可以通过手动编辑go.mod文件来完成，我将在以后的文章中向您展示。

## 五. 重置依赖关系

如果您在任何时候都不满意所选的module和版本，则你始终可以通过删除module文件并再次运行go mod tidy来重置选择。当项目还很年轻并且情况不稳定时，这更是一种选择。项目稳定并发布后，我会犹豫重新设置依赖关系。正如我上面提到的，随着时间的推移，可能会设置module版本，并且您需要长期持久且可重复的构建。

清单22：

```
$ rm go.*
$ go mod init <module name>
$ go mod tidy
```


清单22显示了允许MVS从头开始再次执行所有选择的命令。在撰写本文的整个过程中，我一直在进行此操作以重置项目并提供本文的代码清单。

## 六. 结论

在这篇文章中，我解释了MVS语义，并展示了Go和MVS算法实际应用的真实示例。我还展示了一些Go命令，这些命令可以在您遇到未知问题时为您提供信息。在为项目添加越来越多的依赖项时，可能会遇到一些极端情况。这是因为Go生态系统已有[10年的历史](https://tonybai.com/2019/11/09/go-opensource-10-years/)，所有现有项目都需要更多时间才能符合module要求。

在以后的文章中，我将讨论在同一项目中使用不同主要版本的依赖关系，以及如何手动检索和锁定依赖关系的特定版本。现在，我希望您对module和Go工具有更多的信任，并且对MVS如何随着时间的推移选择版本有了更清晰的了解。如果您遇到任何问题，可以在#module组的Gopher Slack上找到一群愿意提供帮助的人。

本文翻译自[《Modules Part 03: Minimal Version Selection》](https://www.ardanlabs.com/blog/2019/12/modules-03-minimal-version-selection.html)。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

翻译很准确到位，谢谢

又Get到不少知识点

感谢博主的翻译， 这里： 清单2显示了module D存在的所有版本，我们看到其中显示的“最新最大”版本为1.4.2。

好像应该是清单1，我看原作者这块似乎弄错了