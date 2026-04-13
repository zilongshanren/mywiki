---
title: Go开发命令行程序指南
url: https://tonybai.com/2023/03/25/the-guide-of-developing-cli-program-in-go/
published: '2023-03-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go开发命令行程序指南

![](../../assets/0ea44e873a233f24.png)


注：上面篇首配图的底图由百度

[文心一格]生成。

[本文永久链接](https://tonybai.com/2023/03/25/the-guide-of-developing-cli-program-in-go) – https://tonybai.com/2023/03/25/the-guide-of-developing-cli-program-in-go

近期在Twitter上看到一个名为[“Command Line Interface Guidelines”的站点](https://clig.dev/)，这个站点汇聚了帮助大家编写出更好命令行程序的哲学与指南。这份指南[基于传统的Unix编程原则](https://book.douban.com/subject/1467587/)，又结合现代的情况进行了“与时俱进”的更新。之前我还真未就如何编写命令行交互程序做系统的梳理，在这篇文章中，我们就来结合[clig这份指南](https://clig.dev/)，(可能不会全面覆盖)整理出一份使用Go语言编写CLI程序的指南，供大家参考。

## 一. 命令行程序简介

命令行接口（Command Line Interface, 简称CLI）程序是一种允许用户使用文本命令和参数与计算机系统互动的软件。开发人员编写CLI程序通常用在自动化脚本、数据处理、系统管理和其他需要低级控制和灵活性的任务上。**命令行程序也是Linux/Unix管理员以及后端开发人员的最爱**。

[2022年Q2 Go官方用户调查结果](https://go.dev/blog/survey2022-q2-results)显示(如下图)：在使用Go开发的程序类别上，CLI类程序排行第二，得票率60%。

![](../../assets/6a538ed02e84c179.png)


之所以这样，得益于Go语言为CLI开发提供的诸多便利，比如：

- Go语法简单而富有表现力；
- Go拥有一个强大的标准库，并内置的并发支持；
- Go拥有几乎最好的跨平台兼容性和快速的编译速度；
- Go还有一个丰富的第三方软件包和工具的生态系统。

这些都让开发者使用Go创建强大和用户友好的CLI程序变得容易。

容易归容易，但要用Go编写出优秀的CLI程序，我们还需要遵循一些原则，获得一些关于Go CLI程序开发的最佳实践和惯例。这些原则和惯例涉及交互界面设计、错误处理、文档、测试和发布等主题。此外，借助于一些流行的Go CLI程序开发库和框架，比如：[cobra](https://github.com/spf13/cobra)、[Kingpin](https://github.com/alecthomas/kingpin)和[Goreleaser](https://github.com/goreleaser/goreleaser)等，我们可以又好又快地完成CLI程序的开发。在本文结束时，你将学会如何创建一个易于使用、可靠和可维护的Go CLI程序，你还将获得一些关于CLI开发的最佳实践和惯例的见解。

## 二. 建立Go开发环境

如果你读过

[《十分钟入门Go语言》]或订阅学习过我的极客时间[《Go语言第一课》专栏]，你大可忽略这一节的内容。

在我们开始编写Go CLI程序之前，我们需要确保我们的系统中已经安装和配置了必要的Go工具和依赖。在本节中，我们将向你展示如何安装Go和设置你的工作空间，如何[使用go mod进行依赖管理](https://tonybai.com/2022/03/12/dependency-hell-in-go/)，以及如何使用go build和go install来编译和安装你的程序。

### 1. 安装Go

要在你的系统上安装Go，你可以遵循你所用操作系统的官方安装说明。你也可以使用软件包管理器，如[homebrew](https://brew.sh)（用于macOS）、chocolatey（用于Windows）或snap/apt（用于Linux）来更容易地安装Go。

一旦你安装了Go，你可以通过在终端运行以下命令来验证它是否可以正常工作。

```
$go version
```


如果安装成功，go version这个命令应该会打印出你所安装的Go的版本。比如说：

```
go version go1.20 darwin/amd64
```


### 2. 设置你的工作区(workspace)

Go以前有一个惯例，即在工作区目录中(\$GOPATH)组织你的代码和依赖关系。默认工作空间目录位于$HOME/go，但你可以通过设置GOPATH环境变量来改变它的路径。工作区目录包含三个子目录：src、pkg和bin。src目录包含了你的源代码文件和目录。pkg目录包含被你的代码导入的已编译好的包。bin目录包含由你的代码生成的可执行二进制文件。

[Go 1.11引入Go module](https://tonybai.com/2018/11/19/some-changes-in-go-1-11)后，这种在\$GOPATH下组织代码和寻找依赖关系的要求被彻底取消。在这篇文章中，我依旧按照我的习惯在$HOME/go/src下放置我的代码示例。

为了给我们的CLI程序创建一个新的项目目录，我们可以在终端运行以下命令：

```
$mkdir -p $HOME/go/src/github.com/your-username/your-li-program
$cd $HOME/go/src/github.com/your-username/your-cli-program
```


注意，我们的项目目录名使用的是github的URL格式。这在Go项目中是一种常见的做法，因为它使得使用go get导入和管理依赖关系更加容易。go module成为构建标准后，这种对项目目录名的要求已经取消，但很多Gopher依旧保留了这种作法。

### 3. 使用go mod进行依赖管理

1.11版本后Go推荐开发者使用module来管理包的依赖关系。一个module是共享一个共同版本号和导入路径前缀的相关包的集合。一个module是由一个叫做go.mod的文件定义的，它指定了模块的名称、版本和依赖关系。

为了给我们的CLI程序创建一个新的module，我们可以在我们的项目目录下运行以下命令。

```
$go mod init github.com/your-username/your-cli-program
```


这将创建一个名为go.mod的文件，内容如下。

```
module github.com/your-username/your-cli-program
go 1.20
```


第一行指定了我们的module名称，这与我们的项目目录名称相匹配。第二行指定了构建我们的module所需的Go的最低版本。

为了给我们的模块添加依赖项，我们可以使用go get命令，加上我们想使用的软件包的导入路径和可选的版本标签。例如，如果我们想使用[cobra](https://github.com/spf13/cobra)作为我们的CLI框架，我们可以运行如下命令：

```
$go get github.com/spf13/cobra@v1.3.0
```


go get将从github下载cobra，并在我们的go.mod文件中把它作为一个依赖项添加进去。它还将创建或更新一个名为go.sum的文件，记录所有下载的module的校验和，以供后续验证使用。

我们还可以使用其他命令，如go list、go mod tidy、go mod graph等，以更方便地检查和管理我们的依赖关系。

### 4. 使用go build和go install来编译和安装你的程序

Go有两个命令允许你编译和安装你的程序：go build和go install。这两个命令都以一个或多个包名或导入路径作为参数，并从中产生可执行的二进制文件。

它们之间的主要区别在于它们将生成的二进制文件存储在哪里。

- go build将它们存储在当前工作目录中。
- go install将它们存储在\$GOPATH/bin或\$GOBIN（如果设置了）。

例如，如果我们想把CLI程序的main包（应该位于github.com/your-username/your-cli-program/cmd/your-cli-program）编译成一个可执行的二进制文件，称为your-cli-program，我们可以运行下面命令：

```
$go build github.com/your-username/your-cli-program/cmd/your-cli-program
```


或

```
$go install github.com/your-username/your-cli-program/cmd/your-cli-program@latest
```


## 三. 设计用户接口(interface)

要编写出一个好的CLI程序，最重要的环节之一是** 设计一个用户友好的接口**。好的命令行用户接口应该是

**一致的、直观的和富有表现力的**。在本节中，我将说明如何为命令行程序命名和选择命令结构(command structure)，如何使用标志(flag)、参数(argument)、子命令(subcommand)和选项(option)作为输入参数，如何使用cobra或Kingpin等来解析和验证用户输入，以及如何遵循POSIX惯例和GNU扩展的CLI语法。

### 1. 命令行程序命名和命令结构选择

你的CLI程序的名字应该是** 简短、易记、描述性的和易输入的**。它应该避免与目标平台中现有的命令或关键字发生冲突。例如，如果你正在编写一个在不同格式之间转换图像的程序，你可以把它命名为imgconv、imago、picto等，但不能叫image、convert或format。

你的CLI程序的命令结构应该反映你想提供给用户的主要功能特性。你可以选择使用下面命令结构模式中的一种：

- 一个带有多个标志(flag)和参数(argument)的单一命令（例如：curl、tar、grep等)
- 带有多个子命令(subcommand)的单一命令（例如：git、docker、kubectl等)
- 具有共同前缀的多个命令（例如：aws s3、gcloud compute、az vm等)

命令结构模式的选择取决于你的程序的复杂性和使用范围，一般来说：

- 如果你的程序只有一个主要功能或操作模式(operation mode)，你可以使用带有多个标志和参数的单一命令。
- 如果你的程序有多个相关但又不同的功能或操作模式，你可以使用一个带有多个子命令的单一命令。
- 如果你的程序有多个不相关或独立的功能或操作模式，你可以使用具有共同前缀的多个命令。

例如，如果你正在编写一个对文件进行各种操作的程序（如复制、移动、删除），你可以任选下面命令结构模式中的一种：

- 带有多个标志和参数的单一命令（例如，fileop -c src dst -m src dst -d src)
- 带有多个子命令的单个命令（例如，fileop copy src dst, fileop move src dst, fileop delete src)

### 2. 使用标志、参数、子命令和选项

**标志(flag)**是以一个或多个(通常是2个)中划线（-）开头的输入参数，它可以修改CLI程序的行为或输出。例如：

```
$curl -s -o output.txt https://example.com
```


在这个例子中：

- “-s”是一个让curl沉默的标志，即不输出执行日志到控制台；
- “-o”是另一个标志，用于指定输出文件的名称
- “output.txt”则是一个参数，是为“-o”标志提供的值。

**参数(argument)**是不以中划线（-）开头的输入参数，为你的CLI程序提供额外的信息或数据。例如：

```
$tar xvf archive.tar.gz
```


我们看在这个例子中：

- x是一个指定提取模式的参数
- v是一个参数，指定的是输出内容的详细(verbose)程度
- f是另一个参数，用于指定采用的是文件模式，即将压缩结果输出到一个文件或从一个压缩文件读取数据
- archive.tar.gz是一个参数，提供文件名。

**子命令(subcommand)**是输入参数，作为主命令下的辅助命令。它们通常有自己的一组标志和参数。比如下面例子：

```
$git commit -m "Initial commit"
```


我们看在这个例子中：

- git是主命令(primary command)
- commit是一个子命令，用于从staged的修改中创建一个新的提交(commit)
- “-m”是commit子命令的一个标志，用于指定提交信息
- “Initial commit”是commit子命令的一个参数，为”-m”标志提供值。

**选项(option)**是输入参数，它可以使用等号（=）将标志和参数合并为一个参数。例如:

```
$docker run --name=my-container ubuntu:latest
```


我们看在这个例子中“–name=my-container”是一个选项，它将容器的名称设为my-container。该选项前面的部分“–name”是一个标志，后面的部分“my-container”是参数。

### 3. 使用cobra包等来解析和验证用户输入的信息

如果手工来解析和验证用户输入的信息，既繁琐又容易出错。幸运的是，有许多库和框架可以帮助你在Go中解析和验证用户输入。其中最流行的是[cobra](https://github.com/spf13/cobra)。

cobra是一个Go包，它提供了简单的接口来创建强大的CLI程序。它支持子命令、标志、参数、选项、环境变量和配置文件。它还能很好地与其他库集成，比如：[viper](https://tonybai.com/2022/09/20/use-viper-to-do-merge-of-yml-configuration-files/)（用于配置管理）、[pflag](https://github.com/spf13/pflag)（用于POSIX/GNU风格的标志）和[Docopt](https://github.com/docopt/docopt.go)（用于生成文档）。

另一个不那么流行但却提供了一种声明式的方法来创建优雅的CLI程序的包是[Kingpin](https://github.com/alecthomas/kingpin)，它支持标志、参数、选项、环境变量和配置文件。它还具有自动帮助生成、命令完成、错误处理和类型转换等功能。

cobra和Kingpin在其官方网站上都有大量的文档和例子，你可以根据你的偏好和需要选择任选其一。

### 4. 遵循POSIX惯例和GNU扩展的CLI语法

[POSIX（Portable Operating System Interface）](http://get.posixcertified.ieee.org)是一套标准，定义了软件应该如何与操作系统进行交互。其中一个标准定义了CLI程序的语法和语义。GNU（GNU’s Not Unix）是一个旨在创建一个与UNIX兼容的自由软件操作系统的项目。GNU下的一个子项目是[GNU Coreutils](https://www.gnu.org/software/coreutils/)，它提供了许多常见的CLI程序，如ls、cp、mv等。

POSIX和GNU都为CLI语法建立了一些约定和扩展，许多CLI程序都采用了这些约定与扩展。下面列举了这些约定和扩展中的一些主要内容：

- 单字母标志(single-letter flag)以一个中划线（-）开始，可以组合在一起（例如：-a -b -c 或 -abc )
- 长标志(long flag)以两个中划线（–）开头，但不能组合在一起（例如：–all、–backup、–color )
- 选项使用等号(=)来分隔标志名和参数值(例如：–name=my-container )
- 参数跟在标志或选项之后，没有任何分隔符（例如：curl -o output.txt https://example.com ）。
- 子命令跟在主命令之后，没有任何分隔符（例如：git commit -m “Initial commit” )
- 一个双中划线（–）表示标志或选项的结束和参数的开始（例如：rm — -f 表示要删除“-f”这个文件，由于双破折线的存在，这里的“-f”不再是标志)

遵循这些约定和扩展可以使你的CLI程序更加一致、直观，并与其他CLI程序兼容。然而，它们并不是强制性的，如果你有充分的理由，你也大可不必完全遵守它们。例如，一些CLI程序使用斜线（/）而不是中划线（-）表示标志（例如， robocopy /S /E src dst ）。

## 四. 处理错误和信号

编写好的CLI程序的一个重要环节就是** 优雅地处理错误和信号**。

错误是指你的程序由于某些内部或外部因素而无法执行其预定功能的情况。信号是由操作系统或其他进程向你的程序发送的事件，以通知它一些变化或请求。在这一节中，我将说明一下如何使用log、fmt和errors包进行日志输出和错误处理，如何使用os.Exit和defer语句进行优雅的终止，如何使用os.Signal和context包进行中断和取消操作，以及如何遵循CLI程序的退出状态代码惯例。

### 1. 使用log、fmt和errors包进行日志记录和错误处理

Go标准库中有三个包log、fmt和errors可以帮助你进行日志和错误处理。log包提供了一个简单的接口，可以将格式化的信息写到标准输出或文件中。fmt包则提供了各种格式化字符串和值的函数。errors包提供了创建和操作错误值的函数。

要使用log包，你需要在你的代码中导入它：

```
import "log"
```


然后你可以使用log.Println、log.Printf、log.Fatal和log.Fatalf等函数来输出不同严重程度的信息。比如说：

```
log.Println("Starting the program...") // 打印带有时间戳的消息
log.Printf("Processing file %s...\n", filename) // 打印一个带时间戳的格式化信息
log.Fatal("Cannot open file: ", err) // 打印一个带有时间戳的错误信息并退出程序
log.Fatalf("Invalid input: %v\n", input) // 打印一个带时间戳的格式化错误信息，并退出程序。
```


为了使用fmt包，你需要先在你的代码中导入它：

```
import "fmt"
```


然后你可以使用fmt.Println、fmt.Printf、fmt.Sprintln、fmt.Sprintf等函数以各种方式格式化字符串和值。比如说：

```
fmt.Println("Hello world!") // 打印一条信息，后面加一个换行符
fmt.Printf("The answer is %d\n", 42) // 打印一条格式化的信息，后面是换行。
s := fmt.Sprintln("Hello world!") // 返回一个带有信息和换行符的字符串。
t := fmt.Sprintf("The answer is %d\n", 42) // 返回一个带有格式化信息和换行的字符串。
```


要使用错误包，你同样需要在你的代码中导入它：

```
import "errors"
```


然后你可以使用 errors.New、errors.Unwrap、errors.Is等函数来创建和操作错误值。比如说：

```
err := errors.New("Something went wrong") // 创建一个带有信息的错误值
cause := errors.Unwrap(err) // 返回错误值的基本原因（如果没有则为nil）。
match := errors.Is(err, io.EOF) // 如果一个错误值与另一个错误值匹配，则返回真（否则返回假）。
```


### 2. 使用os.Exit和defer语句实现CLI程序的优雅终止

Go有两个功能可以帮助你优雅地终止CLI程序：os.Exit和defer。os.Exit函数立即退出程序，并给出退出状态代码。defer语句则会在当前函数退出前执行一个函数调用，它常用来执行清理收尾动作，如关闭文件或释放资源。

要使用os.Exit函数，你需要在你的代码中导入os包：

```
import "os"
```


然后你可以使用os.Exit函数，它的整数参数代表退出状态代码。比如说

```
os.Exit(0) // 以成功的代码退出程序
os.Exit(1) // 以失败代码退出程序
```


要使用defer语句，你需要把它写在你想后续执行的函数调用之前。比如说

```
file, err := os.Open(filename) // 打开一个文件供读取。
if err != nil {
log.Fatal(err) // 发生错误时退出程序
}
defer file.Close() // 在函数结束时关闭文件。
// 对文件做一些处理...
```


### 3. 使用os.signal和context包来实现中断和取消操作

Go有两个包可以帮助你实现中断和取消长期运行的或阻塞的操作，它们是os.signal和context包。os.signal提供了一种从操作系统或其他进程接收信号的方法。context包提供了一种跨越API边界传递取消信号和deadline的方法。

要使用os.signal，你需要先在你的代码中导入它。

```
import (
"os"
"os/signal"
)
```


然后你可以使用signal.Notify函数针对感兴趣的信号(如下面的os.Interrupt信号)注册一个接收channel(sig)。比如说：

```
sig := make(chan os.Signal, 1) // 创建一个带缓冲的信号channel。
signal.Notify(sig, os.Interrupt) // 注册sig以接收中断信号（例如Ctrl-C）。
// 做一些事情...
select {
case <-sig: // 等待来自sig channel的信号
fmt.Println("被用户中断了")
os.Exit(1) // 以失败代码退出程序。
default: //如果没有收到信号就执行
fmt.Println("成功完成")
os.Exit(0) // 以成功代码退出程序。
}
```


要使用上下文包，你需要在你的代码中导入它：

```
import "context"
```


然后你可以使用它的函数，如context.Background、context.WithCancel、context.WithTimeout等来创建和管理Context。Context是一个携带取消信号和deadline的对象，可以跨越API边界。比如说：

```
ctx := context.Background() // 创建一个空的背景上下文（从不取消）。
ctx, cancel := context.WithCancel(ctx) // 创建一个新的上下文，可以通过调用cancel函数来取消。
defer cancel() // 在函数结束前执行ctx的取消动作
// 将ctx传递给一些接受它作为参数的函数......
select {
case <-ctx.Done(): // 等待来自ctx的取消信号
fmt.Println("Canceled by parent")
return ctx.Err() // 从ctx返回一个错误值
default: // 如果没有收到取消信号就执行
fmt.Println("成功完成")
return nil // 不返回错误值
}
```


### 4. CLI程序的退出状态代码惯例

退出状态代码是一个整数，表示CLI程序是否成功执行完成。CLI程序通过调用os.Exit或从main返回的方式返回退出状态值。其他CLI程序或脚本可以可以检查这些退出状态码，并根据状态码值的不同执行不同的处理操作。

业界有一些关于退出状态代码的约定和扩展，这些约定被许多CLI程序广泛采用。其中一些主要的约定和扩展如下：。

- 退出状态代码为0表示程序执行成功（例如：os.Exit(0) )
- 非零的退出状态代码表示失败（例如：os.Exit(1) ）。
- 不同的非零退出状态代码可能表示不同的失败类型或原因（例如：os.Exit(2)表示使用错误，os.Exit(3)表示权限错误等等）。
- 大于125的退出状态代码可能表示被外部信号终止（例如，os.Exit(130)为被信号中断）。

遵循这些约定和扩展可以使你的CLI程序表现的更加一致、可靠并与其他CLI程序兼容。然而，它们不是强制性的，你可以使用任何对你的程序有意义的退出状态代码。例如，一些CLI程序使用高于200的退出状态代码来表示自定义或特定应用的错误（例如，os.Exit(255)表示未知错误）。

## 五. 编写文档

编写优秀CLI程序的另一个重要环节是编写清晰简洁的文档，解释你的程序做什么以及如何使用它。文档可以采取各种形式，如README文件、usage信息、help flag等。在本节中，我们将告诉你如何为你的程序写一个README文件，如何为你的程序写一个有用的usage和help flag等。

### 1. 为你的CLI程序写一个清晰简洁的README文件

README文件是一个文本文件，它提供了关于你的程序的基本信息，如它的名称、描述、用法、安装、依赖性、许可证和联系细节等。它通常是用户或开发者在源代码库或软件包管理器上首次使用你的程序时会看到的内容。

如果你要为Go CLI程序编写一个优秀的README文件，你应该遵循一些最佳实践，比如：

- 使用一个描述性的、醒目的标题，反映你的程序的目的和功能。
- 提供一个简短的介绍，解释你的程序是做什么的，为什么它是有用的或独特的。
- 包括一个usage部分，说明如何用不同的标志、参数、子命令和选项来调用你的程序。你可以使用代码块或屏幕截图来说明这些例子。
- 包括一个安装(install)部分，解释如何在不同的平台上下载和安装你的程序。你可以使用go install、go get、
[goreleaser](https://github.com/goreleaser/goreleaser)或其他工具来简化这一过程。 - 指定你的程序的发行许可，并提供一个许可全文的链接。你可以使用
[SPDX标识符](https://spdx.dev/)来表示许可证类型。 - 为想要报告问题、请求新功能、贡献代码或提问的用户或开发者提供联系信息。你可以使用github issue、pr、discussion、电子邮件或其他渠道来达到这个目的。

以下是一个Go CLI程序的README文件的示例供参考：

![](../../assets/953929d5578df2bb.png)


### 2. 为你的CLI程序编写有用的usage和help标志

usage信息是一段简短的文字，总结了如何使用你的程序及其可用的标志、参数、子命令和选项。它通常在你的程序在没有参数或输入无效的情况下运行时显示。

help标志是一个特殊的标志（通常是-h或–help），它可以触发显示使用信息和一些关于你的程序的额外信息。

为了给你的Go CLI程序写有用的usage信息和help标志，你应该遵循一些准则，比如说：

- 使用一致而简洁的语法来描述标志、参数、子命令和选项。你可以用方括号“[ ]”表示可选元素，使用角括号“< >”表示必需元素，使用省略号“…”表示重复元素，使用管道“|”表示备选，使用中划线“-”表示标志(flag)，使用等号“=”表示标志的值等等。
- 对标志、参数、子命令和选项应使用描述性的名称，以反映其含义和功能。避免使用单字母名称，除非它们非常常见或非常直观（如-v按惯例表示verbose模式）。
- 为每个标志、参数、子命令和选项提供简短而清晰的描述，解释它们的作用以及它们如何影响你的程序的行为。你可以用圆括号“（ ）”来表达额外的细节或例子。
- 使用标题或缩进将相关的标志、参数、子命令和选项组合在一起。你也可以用空行或水平线（—）来分隔usage的不同部分。
- 在每组中按名称的字母顺序排列标志。在每组中按重要性或逻辑顺序排列参数。在每组中按使用频率排列子命令。

git的usage就是一个很好的例子：

```
$git
usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
[--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
[-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
[--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
<command> [<args>]
```


结合上面的准则，大家可以细心体会一下。

## 六. 测试和发布你的CLI程序

编写优秀CLI程序的最后一个环节是测试和发布你的程序。测试确保你的程序可以按预期工作，并符合质量标准。发布可以使你的程序可供用户使用和访问。

在本节中，我将说明如何使用testing、testify/assert、mock包对你的代码进行单元测试，如何使用go test、coverage、benchmark工具来运行测试和测量程序性能以及如何使用goreleaser包来构建跨平台的二进制文件。

### 1. 使用testing、testify的assert及mock包对你的代码进行单元测试

单元测试是一种验证单个代码单元（如函数、方法或类型）的正确性和功能的技术。单元测试可以帮助你尽早发现错误，提高代码质量和可维护性，并促进重构和调试。

要为你的Go CLI程序编写单元测试，你应该遵循一些最佳实践：

- 使用内置的测试包来创建测试函数，以Test开头，后面是被测试的函数或方法的名称。例如：func TestSum(t *testing.T) { … }；
- 使用*testing.T类型的t参数，使用t.Error、t.Errorf、t.Fatal或t.Fatalf这样的方法报告测试失败。你也可以使用t.Log、t.Logf、t.Skip或t.Skipf这样的方法来提供额外的信息或有条件地跳过测试。
- 使用
[Go子测试(sub test)](https://tonybai.com/2023/03/15/an-intro-of-go-subtest)，通过t.Run方法将相关的测试分组。例如：

```
func TestSum(t *testing.T) {
t.Run("positive numbers", func(t *testing.T) {
// test sum with positive numbers
})
t.Run("negative numbers", func(t *testing.T) {
// test sum with negative numbers
})
}
```


- 使用表格驱动(table-driven)的测试来运行多个测试用例，比如下面的例子：

```
func TestSum(t *testing.T) {
tests := []struct{
name string
a int
b int
want int
}{
{"positive numbers", 1, 2, 3},
{"negative numbers", -1, -2, -3},
{"zero", 0, 0 ,0},
}
for _, tt := range tests {
t.Run(tt.name, func(t *testing.T) {
got := Sum(tt.a , tt.b)
if got != tt.want {
t.Errorf("Sum(%d , %d) = %d; want %d", tt.a , tt.b , got , tt.want)
}
})
}
}
```


- 使用外部包，如testify/assert或mock来简化你的断言或对外部的依赖性。比如说：

```
import (
"github.com/stretchr/testify/assert"
"github.com/stretchr/testify/mock"
)
type Calculator interface {
Sum(a int , b int) int
}
type MockCalculator struct {
mock.Mock
}
func (m *MockCalculator) Sum(a int , b int) int {
args := m.Called(a , b)
return args.Int(0)
}
```


### 2. 使用Go的测试、覆盖率、性能基准工具来运行测试和测量性能

Go提供了一套工具来运行测试和测量你的代码的性能。你可以使用这些工具来确保你的代码按预期工作，检测错误或bug，并优化你的代码以提高速度和效率。

要使用go test、coverage、benchmark工具来运行测试和测量你的Go CLI程序的性能，你应该遵循一些步骤，比如说。

- 将以_test.go结尾的测试文件写在与被测试代码相同的包中。例如：sum_test.go用于测试sum.go。
- 使用go测试命令来运行一个包中的所有测试或某个特定的测试文件。你也可以使用一些标志，如-v，用于显示verbose的输出，-run用于按名字过滤测试用例，-cover用于显示代码覆盖率，等等。例如：go test -v -cover ./…
- 使用go工具cover命令来生成代码覆盖率的HTML报告，并高亮显示代码行。你也可以使用-func这样的标志来显示函数的代码覆盖率，用-html还可以在浏览器中打开覆盖率结果报告等等。例如：go tool cover -html=coverage.out
- 编写性能基准函数，以Benchmark开头，后面是被测试的函数或方法的名称。使用类型为*testing.B的参数b来控制迭代次数，并使用b.N、b.ReportAllocs等方法控制报告结果的输出。比如说

```
func BenchmarkSum(b *testing.B) {
for i := 0; i < b.N; i++ {
Sum(1 , 2)
}
}
```


-
使用go test -bench命令来运行一个包中的所有性能基准测试或某个特定的基准文件。你也可以使用-benchmem这样的标志来显示内存分配的统计数据，-cpuprofile或-memprofile来生成CPU或内存profile文件等等。例如：go test -bench . -benchmem ./…

-
使用pprof或benchstat等工具来分析和比较CPU或内存profile文件或基准测试结果。比如说。


```
# Generate CPU profile
go test -cpuprofile cpu.out ./...
# Analyze CPU profile using pprof
go tool pprof cpu.out
# Generate two sets of benchmark results
go test -bench . ./... > old.txt
go test -bench . ./... > new.txt
# Compare benchmark results using benchstat
benchstat old.txt new.txt
```


### 3. 使用goreleaser包构建跨平台的二进制文件

构建跨平台二进制文件意味着将你的代码编译成可执行文件，可以在不同的操作系统和架构上运行，如Windows、Linux、Mac OS、ARM等。这可以帮助你向更多的人分发你的程序，使用户更容易安装和运行你的程序而不需要任何依赖或配置。

为了给你的Go CLI程序建立跨平台的二进制文件，你可以使用外部软件包，比如goreleaser等 ，它们可以自动完成程序的构建、打包和发布过程。下面是使用goreleaser包构建程序的一些步骤。

- 使用go get或go install命令安装goreleaser。例如： go install github.com/goreleaser/goreleaser@latest
- 创建一个配置文件（通常是.goreleaser.yml），指定如何构建和打包你的程序。你可以定制各种选项，如二进制名称、版本、主文件、输出格式、目标平台、压缩、校验和、签名等。例如。

```
# .goreleaser.yml
project_name: mycli
builds:
- main: ./cmd/mycli/main.go
binary: mycli
goos:
- windows
- darwin
- linux
goarch:
- amd64
- arm64
archives:
- format: zip
name_template: "{{ .ProjectName }}_{{ .Version }}_{{ .Os }}_{{ .Arch }}"
files:
- LICENSE.txt
- README.md
checksum:
name_template: "{{ .ProjectName }}_checksums.txt"
algorithm: sha256
```


运行goreleaser命令，根据配置文件构建和打包你的程序。你也可以使用-snapshot用于测试，-release-notes用于从提交信息中生成发布说明，-rm-dist用于删除之前的构建，等等。例如：goreleaser –snapshot –rm-dist。

检查输出文件夹（通常是dist）中生成的二进制文件和其他文件。你也可以使用goreleaser的发布功能将它们上传到源代码库或软件包管理器中。

## 七. clig.dev指南要点

通过上述的系统说明，你现在应该可以设计并使用Go实现出一个CLI程序了。不过本文并非覆盖了clig.dev指南的所有要点，因此，在结束本文之前，我们再来回顾一下clig.dev指南中的要点，大家再体会一下。

前面说过，clig.dev上的cli指南是一个开源指南，可以帮助你写出更好的命令行程序，它采用了传统的UNIX原则，并针对现代的情况进行了更新。

遵循cli准则的一些好处是：

- 你可以创建易于使用、理解和记忆的CLI程序。
- 你可以设计出能与其他程序进行很好配合的CLI程序，并遵循共同的惯例。
- 你可以避免让用户和开发者感到沮丧的常见陷阱和错误。
- 你可以从其他CLI设计者和用户的经验和智慧中学习。

下面是该指南的一些要点：

- 理念

这一部分解释了好的CLI设计背后的核心原则，如人本设计、可组合性、可发现性、对话性等。例如，以人为本的设计意味着CLI程序对人类来说应该易于使用和理解，而不仅仅是机器。可组合性意味着CLI程序应该通过遵循共同的惯例和标准与其他程序很好地协作。

- 参数和标志

这一部分讲述了如何在你的CLI程序中使用位置参数(positional arguments )和标志。它还解释了如何处理默认值、必传参数、布尔标志、多值等。例如，你应该对命令的主要对象或动作使用位置参数，对修改或可选参数使用标志。你还应该使用长短两种形式的标志（如-v或-verbose），并遵循常见的命名模式（如–help或–version）。

- 配置

这部分介绍了如何使用配置文件和环境变量来为你的CLI程序存储持久的设置。它还解释了如何处理配置选项的优先级、验证、文档等。例如，你应该使用配置文件来处理用户很少改变的设置，或者是针对某个项目或环境的设置。对于特定于环境或会话的设置（如凭证或路径），你也应该使用环境变量。

- 输出

这部分介绍了如何格式化和展示你的CLI程序的输出。它还解释了如何处理输出verbose级别、进度指示器、颜色、表格等。例如，你应该使用标准输出（stdout）进行正常的输出，这样输出的信息可以通过管道输送到其他程序或文件。你还应该使用标准错误（stderr）来处理不属于正常输出流的错误或警告。

- 错误

这部分介绍了如何在你的CLI程序中优雅地处理错误。它还解释了如何使用退出状态码、错误信息、堆栈跟踪等。例如，你应该使用表明错误类型的退出代码（如0代表成功，1代表一般错误）。你还应该使用简洁明了的错误信息，解释出错的原因以及如何解决。

- 子命令

这部分介绍了当CLI程序有多种操作或操作模式时，如何在CLI程序中使用子命令。它还解释了如何分层构建子命令，组织帮助文本，以及处理常见的子命令（如help或version）。例如，当你的程序有不同的功能，需要不同的参数或标志时（如git clone或git commit），你应该使用子命令。你还应该提供一个默认的子命令，或者在没有给出子命令时提供一个可用的子命令列表。

业界有许多精心设计的CLI工具的例子，它们都遵循cli准则，大家可以通过使用来深刻体会一下这些准则。下面是一些这样的CLI工具的例子：

-
httpie：一个命令行HTTP客户端，具有直观的UI，支持JSON，语法高亮，类似wget的下载，插件等功能。例如，Httpie使用清晰简洁的语法进行HTTP请求，支持多种输出格式和颜色，优雅地处理错误并提供有用的文档。

-
git：一个分布式的版本控制系统，让你管理你的源代码并与其他开发者合作。例如，Git使用子命令进行不同的操作（如git clone或git commit），遵循通用的标志（如-v或-verbose），提供有用的反馈和建议（如git status或git help），并支持配置文件和环境变量。

-
npm：一个JavaScript的包管理器，让你为你的项目安装和管理依赖性。例如，NPM使用一个简单的命令结构（npm

[args]），提供一个简洁的初始帮助信息，有更详细的选项（npm help npm），支持标签完成和合理的默认值，并允许你通过配置文件（.npmrc）自定义设置。

## 八. 小结

在这篇文章中，我们系统说明了如何编写出遵循命令行接口指南的Go CLI程序。

你学习了如何设置Go环境、设计命令行接口、处理错误和信号、编写文档、使用各种工具和软件包测试和发布程序。你还看到了一些代码和配置文件的例子。通过遵循这些准则和最佳实践，你可以创建一个用户友好、健壮和可靠的CLI程序。

最后我们回顾了clig.dev的指南要点，希望你能更深刻理解这些要点的含义。

我希望你喜欢这篇文章并认为它很有用。如果你有任何问题或反馈，请随时联系我。编码愉快！

注：本文系与New Bing Chat联合完成，旨在验证如何基于AIGC能力构思和编写长篇文章。文章内容的正确性经过笔者全面审校，可放心阅读。


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

感谢分享，非常的详尽实用。

将命令行工具的设计、编码、测试、发布等各个阶段的注意点都说的清清楚楚。

感谢分析，之前一直用flag包，阅读以后才知道有更好的工具、办法、模式来编写CLI。

通常, 不复杂的cli应用使用标准库的flag包就足够了，还可以少引入一些外部依赖module。