---
title: 从DevOps到日常脚本：聊聊Go语言的多面性
url: https://tonybai.com/2024/10/08/go-languages-versatility-from-devops-to-daily-scripts/
published: '2024-10-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 从DevOps到日常脚本：聊聊Go语言的多面性

![](../../assets/d1b84f7c29f3400d.png)


[本文永久链接](https://tonybai.com/2024/10/08/go-languages-versatility-from-devops-to-daily-scripts) – https://tonybai.com/2024/10/08/go-languages-versatility-from-devops-to-daily-scripts

2024年初，TIOBE编程语言排行榜上，[Go再次进入了前十，并在之后又成功冲高至第七名](https://mp.weixin.qq.com/s?__biz=MzIyNzM0MDk0Mg==&mid=2247497403&idx=1&sn=03bc972e38163e1539da765249d46586&chksm=e860115adf17984cfe47f9680d8c0fb6370987ad45415ff2d38233d05fe6b315210ce6ada385#rd)。

Go语言的排名上升，至少在[Reddit Go论坛](https://www.reddit.com/r/golang/)上帖子数量和在线人数上得到了体现，尽管目前与[Rust](https://tonybai.com/tag/rust)热度仍有差距，但可见Go的关注度在提升：

![](../../assets/daf81d249f58e1ba.png)



随着Go语言人气的上升，论坛中的问题也变得愈发多样化。许多Gopher常常问及[为何Go是DevOps语言](https://www.reddit.com/r/golang/comments/1fqwbv0/why_is_golang_the_language_of_devops/)和[Go适合用作脚本语言吗](https://www.reddit.com/r/golang/comments/1ftpk2m/do_you_use_go_for_scripts/)等问题，这些都反映了Go语言的多面性。

从最初的系统编程语言，到如今在DevOps领域的广泛应用，再到一些场合被探索用作脚本语言，Go展现出了令人惊叹的灵活性和适应性。在本篇文章中，我们将聚焦于Go语言在DevOps领域的应用以及它作为脚本替代语言的潜力，聊聊其强大多面性如何满足这些特定场景的需求。

## 1. Go在DevOps中的优势

随着DevOps的发展，[平台工程(Platform Engineering)](https://en.wikipedia.org/wiki/Platform_engineering)这一新兴概念逐渐兴起。在自动化任务、微服务部署和系统管理中，编程语言的作用变得愈发重要。Go语言凭借其高性能、并发处理能力以及能够编译成单一二进制文件的特点，越来越受到DevOps领域开发人员的青睐，成为开发DevOps工具链的重要组成部分。

首先，Go的跨平台编译能力使得DevOps团队可以在一个平台上编译，然后在多个不同的操作系统和架构上运行，结合**编译出的单一可执行文件**的能力，大大简化了部署流程，这也是很多Go开发者认为Go适合DevOps的第一优势：

```
$GOOS=linux GOARCH=amd64 go build -o myapp-linux-amd64 main.go
$GOOS=linux GOARCH=arm64 go build -o myapp-linux-arm64 main.go
$GOOS=darwin GOARCH=amd64 go build -o myapp-darwin-amd64 main.go
$GOOS=windows GOARCH=amd64 go build -o myapp-windows-amd64.exe main.go
```


其次，Go的标准库仿佛“瑞士军刀”，开箱即用，**为DevOps场景提供了所需的丰富的网络、加密和系统操作功能库**，大幅降低对外部的依赖，即便不使用第三方包生态系统，也可以满足大部分的DevOps功能需求。

此外，Go的goroutines和channels为处理高并发任务提供了极大便利，这在DevOps中也尤为重要。例如，以下代码展示了如何使用goroutines并发检查多个服务的健康状态：

```
func checkServices(services []string) {
var wg sync.WaitGroup
for _, service := range services {
wg.Add(1)
go func(s string) {
defer wg.Done()
if err := checkHealth(s); err != nil {
log.Printf("Service %s is unhealthy: %v", s, err)
} else {
log.Printf("Service %s is healthy", s)
}
}(service)
}
wg.Wait()
}
```


并且，许多知名的DevOps基础设施、中间件和工具都是用Go编写的，如Docker、Kubernetes、Prometheus等，集成起来非常丝滑。这些工具的成功进一步证明了Go在DevOps领域的适用性。

## 2. Go作为脚本语言的潜力

在传统的DevOps任务中，Python和Shell脚本长期以来都是主力军，它们(尤其是Python)以其简洁的语法和丰富的生态系统赢得了DevOps社区的广泛青睐。然而，传统主力Python和Shell脚本虽然灵活易用，但在处理大规模数据或需要高性能的场景时往往力不从心。此外，它们的动态类型系统可能导致运行时错误，增加了调试难度。

随着Go的普及，它的“超高性价比”逐渐被开发运维人员所接受：**既有着接近于脚本语言的较低的学习曲线与较高的生产力(也得益于Go超快的编译速度)，又有着静态语言的高性能，还有单一文件在部署方面的便利性**。

下面是一个简单的文件处理脚本，用于向大家展示Go的简单易学：

```
package main
import (
"bufio"
"fmt"
"os"
"strings"
)
func main() {
file, err := os.Open("input.txt")
if err != nil {
fmt.Println("Error opening file:", err)
return
}
defer file.Close()
scanner := bufio.NewScanner(file)
for scanner.Scan() {
line := scanner.Text()
if strings.Contains(line, "ERROR") {
fmt.Println(line)
}
}
}
```


这个示例虽然要比同等功能的Python或shell代码行数要多，但由于Go的简单和直观，多数人都很容易看懂这段代码。

此外，Go的静态强类型系统可以在编译时捕获更多错误，避免在运行时的调试，提高了脚本在运行时的可靠性。

开发运维人员眼中的脚本语言，如Shell脚本和Python脚本，通常是直接基于源代码进行解释和运行的。实际上，Go语言同样可以实现这一点，而其关键工具就是go run命令。这个命令允许开发者快速执行Go代码，从而使Go源码看起来更像是“脚本”，下面我们就来看看go run。

## 3. go run：桥接编译型语言与脚本语言的利器

我们知道go run命令实际上是编译和运行的组合，它**首先编译源代码，然后立即执行生成的二进制文件**。这个过程对用户来说是透明的，使得Go程序可以像脚本一样方便地运行。这一命令也大大简化了Go程序的开发流程，使Go更接近传统的脚本语言工作流。可以说，通过go run，Go语言向脚本语言的使用体验更靠近了一步。

此外，go run与go build在编译阶段的行为并不完全相同：

-
go run在运行结束后，不保留编译后的二进制文件；而go build生成可执行文件并保留。

-
go run编译时

**默认不包含调试信息，以减少构建时间**；而go build则保留完整的调试信息。 -
go run可以使用-exec标志指定运行环境，比如：


```
$go run -exec="ls" main.go
/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build1742641170/b001/exe/main
```


我们看到，如果设置了-exec标志，那么go run -exec=”prog” main.go args编译后的命令执行就变为了”prog a.out args”。go run还支持跨平台模拟执行，当GOOS或GOARCH与系统默认值不同时，如果在\$PATH路径下存在名为”go_\$GOOS_\$GOARCH_exec”的程序，那么go run就会执行：

```
$go_$GOOS_$GOARCH_exec a.out args
比如：go_js_wasm_exec a.out args
```


-
go run通常用于运行main包，在go module开启的情况下，go run使用的是main module的上下文。go build可以编译多个包，对于非main包时只检查构建而不生成输出

-
go run还支持运行一个指定版本号的包


当指定了版本后缀（如@v1.0.0或@latest）时，go run会进入module-aware mode（模块感知模式），并忽略当前目录或上级目录中的go.mod文件。这意味着，即使你当前的项目中存在依赖管理文件go.mod，go run也不会影响或修改当前项目的依赖关系，下面这个示例展示了这一点：

```
$go run golang.org/x/example/hello@latest
go: downloading golang.org/x/example v0.0.0-20240925201653-1a5e218e5455
go: downloading golang.org/x/example/hello v0.0.0-20240925201653-1a5e218e5455
Hello, world!
```


这个功能特别适合在不影响主模块依赖的情况下，临时运行某个工具或程序。例如，如果你只是想测试某个工具的特定版本，或者快速运行一个远程程序包，而不希望它干扰你正在开发的项目中的依赖项，这种方式就很实用。

不过有一点要注意的是：go run的退出状态并不等于编译后二进制文件的退出状态，看下面这个示例：

```
// main.go成功退出
$go run main.go
Hello from myapp!
$echo $?
0
// main.go中调用os.Exit(2)退出
$go run main.go
Hello from myapp!
exit status 2
$echo $?
1
```


go run使用退出状态1来表示其运行程序的异常退出状态，但这个值和真实的exit的状态值不相等。

到这里我们看到，go run xxx.go可以像bash xxx.sh或python xxx.py那样，以“解释”方式运行一个Go源码文件。这使得Go语言在某种程度上具备了脚本语言的特性。然而，在脚本语言中，例如Bash或Python等，用户可以通过将源码文件设置为可执行，并在文件的首行添加适当的解释器指令，从而直接运行脚本，而无需显式调用解释器。这种灵活性使得脚本的执行变得更加简便。那么Go是否也可以做到这一点呢？我们继续往下看。

## 4. Go脚本化的实现方式

下面是通过一些技巧或第三方工具实现Go脚本化的方法。对于喜欢使用脚本的人来说，最熟悉的莫过于shebang（即解释器指令）。在许多脚本语言中，通过在文件的第一行添加指定的解释器路径，可以直接运行脚本，而无需显式调用解释器。例如，在Bash或Python脚本中，通常会看到这样的行：

```
#!/usr/bin/env python3
```


那么Go语言支持shebang吗? 是否可以实现实现类似的效果呢？我们下面来看看。

### 4.1 使用“shebang(#!)”运行Go脚本

很遗憾，Go不能直接支持shebang，我们看一下这个示例main.go：

```
#!/usr/bin/env go run
package main
import (
"fmt"
"os"
)
func main() {
s := "world"
if len(os.Args) > 1 {
s = os.Args[1]
}
fmt.Printf("Hello, %v!\n", s)
}
```


这一示例的第一行就是一个shebang解释器指令，我们chmod u+x main.go，然后执行该Go“脚本”：

```
$./main.go
main.go:1:1: illegal character U+0023 '#'
```


这个执行过程中，Shell可以正常识别shebang，然后调用go run去运行main.go，问题就在于go编译器视shebang这一行为非法语法！

常规的shebang写法行不通，我们就使用一些trick，下面是改进后的示例：

```
//usr/bin/env go run $0 $@; exit
package main
import (
"fmt"
"os"
)
func main() {
s := "world"
if len(os.Args) > 1 {
s = os.Args[1]
}
fmt.Printf("Hello, %v!\n", s)
}
```


这段代码则可以chmod +x 后直接运行：

```
$./main.go
Hello, world!
$./main.go gopher
Hello, gopher!
```


这是因为它巧妙地结合了shell脚本和Go代码的特性。我们来看一下第一行：

```
//usr/bin/env go run $0 $@; exit
```


这一行看起来像是Go的注释，但实际上是一个shell命令。当文件被执行时，shell会解释这一行，/usr/bin/env用于寻找go命令的路径，go run \$0 \$@ 告诉go命令运行当前脚本文件(\$0)以及所有传递给脚本的参数(\$@)，当go run编译这个脚本时，又会将第一行当做注释行而忽略，这就是关键所在。最后的exit确保shell在Go程序执行完毕后退出。如果没有exit，shell会执行后续Go代码，那显然会导致报错！

除了上述trick外，我们还可以将Go源码文件注册为可执行格式(仅在linux上进行了测试)，下面就是具体操作步骤。

### 4.2 在Linux系统中注册Go为可执行格式

就像在Windows上双击某个文件后，系统打开特定程序处理对应的文件一样，我们也可以将Go源文件(xxx.go)注册为可执行格式，并指定用于处理该文件的程序。实现这一功能，我们需要借助binfmt_misc。binfmt_misc是Linux内核的一个功能，允许用户注册新的可执行文件格式。这使得Linux系统能够识别并执行不同类型的可执行文件，比如脚本、二进制文件等。

我们用下面命令将Go源文件注册到binfmt_misc中：

```
echo ':golang:E::go::/usr/local/bin/gorun:OC' | sudo tee /proc/sys/fs/binfmt_misc/register
```


简单解释一下上述命令：

- :golang:：这是注册的格式的名称，可以自定义。
- E::：表示执行文件的魔数（magic number），在这里为空，表示任何文件类型。
- go::：指定用于执行的解释器，这里是go命令。
- /usr/local/bin/gorun：指定用于执行的程序路径，这里是一个自定义的gorun脚本
- :OC：表示这个格式是可执行的（O）并且支持在运行时创建（C）。

当你执行一个Go源文件时，Linux内核会检查文件的类型。如果文件的格式与注册的格式匹配，内核会调用指定的解释器（在这个例子中是gorun）来执行该文件。

gorun脚本是我们自己编写的，源码如下：

```
#!/bin/bash
# 检查是否提供了源文件
if [ -z "$1" ]; then
echo "用法: gorun <go源文件> [参数...]"
exit 1
fi
# 检查文件是否存在
if [ ! -f "$1" ]; then
echo "错误: 文件 $1 不存在"
exit 1
fi
# 将第一个参数作为源文件，剩余的参数作为执行参数
GO_FILE="$1"
shift # 移除第一个参数，剩余的参数将会被传递
# 使用go run命令执行Go源文件，传递其余参数
go run "$GO_FILE" "$@"
```


将gorun脚本放置带/usr/local/bin下，并chmod +x使其具有可执行权限。

接下来，我们就可以直接执行不带有”shebang”的正常go源码了：

```
// main.go
package main
import (
"fmt"
"os"
)
func main() {
s := "world"
if len(os.Args) > 1 {
s = os.Args[1]
}
fmt.Printf("Hello, %v!\n", s)
}
```


直接执行上述源文件：

```
$ ./main.go
Hello, world!
$ ./main.go gopher
Hello, gopher!
```


### 4.3 第三方工具支持

Go社区也有一些将支持将Go源文件视为脚本的解释器工具，比如：[traefik/yaegi](https://github.com/traefik/yaegi)等。

```
$go install github.com/traefik/yaegi/cmd/yaegi@latest
go: downloading github.com/traefik/yaegi v0.16.1
$yaegi main.go
Hello, main.go!
```


yaegi还可以像python那样，提供Read-Eval-Print-Loop功能，我们可以与yaegi配合进行交互式“Go脚本”编码：

```
$ yaegi
> 1+2
: 3
> import "fmt"
: 0xc0003900d0
> fmt.Println("hello, golang")
hello, golang
: 14
>
```


类似的提供REPL功能的第三方Go解释器还包括：[cosmos72/gomacro](https://github.com/cosmos72/gomacro)、[x-motemen/gore](https://github.com/x-motemen/gore)等，这里就不深入介绍了，感兴趣的童鞋可以自行研究。

## 5. 小结

在本文中，我们探讨了Go语言在DevOps和日常脚本编写中的多面性。首先，Go语言因其高性能、并发处理能力及跨平台编译特性，成为DevOps领域的重要工具，助力于自动化任务和微服务部署。其次，随着Go语言的普及，其作为脚本语言的潜力逐渐被开发运维人员认识，Go展现出了优于传统脚本语言的高效性和可靠性。

我们还介绍了Go脚本的实现方式，包括使用go run命令，它使得Go程序的执行更像传统脚本语言，同时也探讨了一些技巧和工具，帮助开发者将Go源码文件作为可执行脚本直接运行。通过这些探索，我们可以看到Go语言在现代开发中的灵活应用及其日益增长的吸引力。

随着AI能力的飞速发展，使用Go编写一个日常脚本就是分分钟的事情，但Go的特性让这样的脚本具备了传统脚本语言所不具备的并发性、可靠性和性能优势。我们有理由相信，Go在DevOps和脚本编程领域的应用将会越来越广泛，为开发者带来更多的可能性和便利。

## 6. 参考资料

[Using Go as a scripting language in Linux](https://blog.cloudflare.com/using-go-as-a-scripting-language-in-linux/)– https://blog.cloudflare.com/using-go-as-a-scripting-language-in-linux/[Go as a Scripting Language](https://www.infoq.com/news/2020/04/go-scripting-language/)– https://www.infoq.com/news/2020/04/go-scripting-language/[Go compared to Python for small scale system administration scripts and tools](https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SysadminGoVsPython)– https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SysadminGoVsPython

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

大开眼界，原来 go 脚本也能写 shebang！