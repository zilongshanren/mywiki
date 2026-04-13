---
title: Service Weaver：以单体形式编码，以微服务形式部署
url: https://tonybai.com/2023/10/09/service-weaver-coding-in-monolithic-deploy-in-microservices/
published: '2023-10-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Service Weaver：以单体形式编码，以微服务形式部署

![](../../assets/ded4242129066c5d.png)


[本文永久链接](https://tonybai.com/2023/10/09/service-weaver-coding-in-monolithic-deploy-in-microservices) – https://tonybai.com/2023/10/09/service-weaver-coding-in-monolithic-deploy-in-microservices

分布式应用的主流架构模式演化为**微服务架构**已经有些年头了。微服务、DevOps、持续交付和容器技术(k8s)是构成[最初云原生概念](https://tanzu.vmware.com/de/cloud-native)的核心要素。它们相生相拌，共同演进，并推动了云计算**全面进入云原生时代**。

云原生应用普遍采用微服务架构，遗留的单体应用程序会逐步演进并拆分为多个微服务，新应用则会直接采用微服务架构进行设计与实现。微服务的好处是显而易见的：

- 每个微服务都编译为一个二进制文件并独立部署和扩展，可以提高资源利用率；
- 一个微服务的崩溃不会影响到其他微服务，限制了错误的传播半径，从而提高了容错能力；
- 改善了抽象的边界。微服务需要清晰明确的API，降低了代码纠缠不清的可能性；
- 灵活部署，不同微服务的二进制文件可以以不同频率发布，从而实现更敏捷的代码升级。
- … …

不过做过微服务的朋友都知道，微服务架构带来的不仅仅是好处，还有很多挑战：

- 单体应用内的模块间可通过内存直接交互，而在微服务架构的应用中，多个微服务需要进行跨进程跨机器的通信，对数据的序列化和反序列化操作必不可少，其开销很难避免，对应用性能是有较大损耗的；
[研究表明，三分之二的故障是由于不同版本的微服务之间的交互引发的](https://scholar.google.com/scholar?cluster=4116586908204898847)，这会损害应用的正确性；- 每个微服务开发人员都有自己的发布和管理计划，而无法像单体应用那样使用单个二进制文件来统一构建、测试和部署，这给微服务开发管理带来了很高的复杂性；
- API管理变得复杂。一旦某个微服务发布了，它的API很难在不影响其他使用该API的服务的情况下进行变更，新老API同时存在是常态；
- 减慢了应用程序开发的速度。在进行会影响多个微服务的更改时，开发人员无法原子地实现和部署这些更改。他们必须仔细计划如何根据自己的发布时间表在n个微服务中引入变更；

… …

由此可见，微服务并非“银弹”，[人们在消除微服务的缺点方面做了很多工作](https://tonybai.com/2021/11/26/build-all-in-one-runtime-environment-with-docker-compose)，不可谓不努力，但收效甚微，甚至出现了[回归monolith(大单体)的现象](https://thenewstack.io/return-of-the-monolith-amazon-dumps-microservices-for-video-monitoring/)。

今年年初Google发布了一个在这方面的探索成果：[Service Weaver](https://serviceweaver.dev/blog/quick_intro.html)。Service Weaver不仅仅是一个分布式应用的开发框架，更是一个旨在减少或消除微服务弊端的探索实验的结论。

Service Weaver到底有何与众不同？它的核心抽象是什么？它的最大优点又是什么呢？在这一篇文章中，我就和大家一起来学习和了解一下Service Weaver这个开发框架。

## 1. Service Weaver简介

Service Weaver是Google开源的一个编程框架(programming framework) ，用于编写、部署和管理用Go开发的分布式应用程序。

注：随着Service Weaver的演进，后续可能会有其他语言的版本。


使用Service Weaver，你可以像编写在本地机器上运行的传统单进程Go可执行文件一样编写应用程序。然后，将其部署到云中，该框架会将其分解为一组微服务，并将其与云提供商(主要是k8s)集成（如监控、跟踪、日志等）。简单来说，就是**“以单体形式编码，以微服务形式部署”**。

开篇提过，Google开源的Service Weaver本就是为解决微服务架构在实践中出现的诸多问题而提出的创新思路与实验，为此它提出并实现了三个**核心原则**：

- 在构建阶段，开发人员只需编写模块化的单体程序；
- 在首次部署和运行阶段，Service Weaver会将逻辑组件分配给物理进程，可以是本地的一个进程，也可以是多个进程，当然最主流的还是分配给运行在公有云提供商k8s的不同pod；
- 以原子方式升级变更应用，彻底杜绝应用的不同版本间的交互。

这么说依然很抽象，闻名不如见面，接下来我们就用一些例子来看一下Service Weaver是如何践行这三个原则的。

我们先来看看用Service Weaver开发的“Hello, World”程序长什么样子。

## 2. Hello, World

安装Service Weaver很简单，只需执行下面命令：

```
$go install github.com/ServiceWeaver/weaver/cmd/weaver@latest
$weaver
USAGE
weaver generate // weaver code generator
weaver version // show weaver version
weaver single <command> ... // for single process deployments
weaver multi <command> ... // for multiprocess deployments
weaver ssh <command> ... // for multimachine deployments
weaver gke <command> ... // for GKE deployments
weaver gke-local <command> ... // for simulated GKE deployments
weaver kube <command> ... // for vanilla Kubernetes deployments
DESCRIPTION
Use the "weaver" command to deploy and manage Weaver applications.
The "weaver generate", "weaver version", "weaver single", "weaver multi", and
"weaver ssh" subcommands are baked in, but all other subcommands of the form
"weaver <deployer>" dispatch to a binary called "weaver-<deployer>".
"weaver gke status", for example, dispatches to "weaver-gke status".
```


注：Weaver要求

[Go版本高于1.21]。另外在MacOS上安装使用时，官方文档提到要开启export CGO_ENABLED=1; export CC=gcc; 不过CGO_ENABLED=1通常是默认的。另外我使用CC=clang也可以正常安装和使用weaver。

安装完Weaver后，我们就来看一个基于Weaver的Hello, World示例，了解一下基于Weaver框架开发的应用的基本结构。

我们创建一个hello目录，然后在hello下面使用go mod init hello来初始化一个go module。这个例子非常简单，hello目录下只有一个main.go：

```
// serviceweaver-examples/hello/main.go
package main
import (
"context"
"fmt"
"log"
"github.com/ServiceWeaver/weaver"
)
func main() {
if err := weaver.Run(context.Background(), serve); err != nil {
log.Fatal(err)
}
}
// app is the main component of the application. weaver.Run creates
// it and passes it to serve.
type app struct {
weaver.Implements[weaver.Main]
}
// serve is called by weaver.Run and contains the body of the application.
func serve(context.Context, *app) error {
fmt.Println("Hello, World")
return nil
}
```


我们看到：示例导入了weaver包，然后在main函数中调用weaver.Run函数。Run函数的原型如下：

```
// github.com/ServiceWeaver/weaver/weaver.go
func Run[T any, P PointerToMain[T]](ctx context.Context, app func(context.Context, *T) error) error
```


weaver充分利用了[Go 1.18引入的泛型](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)，Run就是一个泛型函数，它的第二个参数为app，这是一个函数类型的参数。顾名思义，app这个函数封装了整个应用的主运行逻辑。在hello这个示例中，我们为Run的第二个参数传入的是serve。而serve的逻辑非常简单，就是输出“Hello, World”，然后就返回nil了，返回nil表示正常退出。weaver.Run会处理应用的生命周期，比如[优雅关闭](https://tonybai.com/2014/10/09/gracefully-shutdown-app-running-in-docker)等，serve函数就只需要关心业务逻辑即可，通过这种方式，通用的服务框架代码和业务代码便分离开来，降低了耦合，提高可维护性。

到这里，很多读者可能注意到了：由于示例过于简单，serve函数并没有使用传入的第二个参数(类型为*app)，但在用Weaver开发的实用程序中，Run的第二个参数是整个应用的核心，并且app这个类型恰好就是weaver.Run泛型函数中T的类型实参(type argument)。

Run函数的注释中明确说明：T类型(app)必须是一个struct类型且包含一个weaver.Implements[weaver.Main]的嵌入字段，在该示例中app类型的定义恰是如此：

```
// serviceweaver-examples/hello/main.go
type app struct {
weaver.Implements[weaver.Main]
}
```


说到这里，就不得不提到**Service Weaver的核心抽象：组件(component)**了！基于Service Weaver框架开发的应用是**由一个组件的集合**。实际上，Weaver中的组件就是一个普通Go接口的实现，编写代码时，组件间的交互也是通过接口的方法调用完成的。

那么，上面示例中的组件在哪里呢？上面的示例仅包含一个Weaver应用必须的组件：main组件。app类型就理解为一个main组件，它通过嵌入weaver.Implements[weaver.Main]这个类型实现了weaver.Main接口：

```
// Main is the interface implemented by an application's main component.
type Main interface{}
```


对于Weaver应用而言，main组件是不可获取的，如果注释掉app结构体类型中weaver.Implements[weaver.Main]这一行，那么无论执行weaver generate命令还是go run命令，你得到的都会是错误：

```
$weaver generate .
-: # hello
./main.go:12:22: *app does not satisfy "github.com/ServiceWeaver/weaver".PointerToMain[app] (missing method implements)
/Users/tonybai/Test/Go/service-weaver/hello/main.go:12:12: *app does not satisfy "github.com/ServiceWeaver/weaver".PointerToMain[app] (missing method implements)
$go run .
# hello
./weaver_gen.go:34:40: cannot use (*app)(nil) (value of type *app) as "github.com/ServiceWeaver/weaver".InstanceOf["github.com/ServiceWeaver/weaver".Main] value in variable declaration: *app does not implement "github.com/ServiceWeaver/weaver".InstanceOf["github.com/ServiceWeaver/weaver".Main] (missing method implements)
./weaver_gen.go:37:25: cannot use (*app)(nil) (value of type *app) as "github.com/ServiceWeaver/weaver".Unrouted value in variable declaration: *app does not implement "github.com/ServiceWeaver/weaver".Unrouted (missing method routedBy)
./main.go:12:22: *app does not satisfy "github.com/ServiceWeaver/weaver".PointerToMain[app] (missing method implements)
```


好了，大致了解Weaver应用的结构后，我们来运行一下这个示例：

```
$go mod tidy
go: finding module for package github.com/ServiceWeaver/weaver
go: found github.com/ServiceWeaver/weaver in github.com/ServiceWeaver/weaver v0.21.2
go: downloading modernc.org/ccgo/v3 v3.16.13
go: downloading modernc.org/cc/v3 v3.40.0
go: downloading lukechampine.com/uint128 v1.2.0
go: downloading modernc.org/token v1.0.1
$weaver generate .
$go run .
╭───────────────────────────────────────────────────╮
│ app : hello │
│ deployment : ca0fcdf2-d9bc-456b-a668-159688e3cca5 │
╰───────────────────────────────────────────────────╯
Hello, World
```


我们看到，在go run执行之前，我们通过weaver generate命令生成一些代码，这些生成的代码放在了weaver_gen.go中，有100多行，是weaver应用运行所必须的stub代码。

hello, world虽然简单易懂，但对Weaver的核心抽象：逻辑组件(component)的体现并不明显，我们再来看一个复杂一些的例子。

## 3. 一个http服务器例子

我们来实现一个http服务器的例子，下面是这个例子的组件逻辑拓扑结构：

![](../../assets/2e6d622e1233ee62.png)


从图中可以看到，这个实例程序一共有三个weaver component：main组件(listener)、reverser组件(用于将输入的字符串反转)和converter组件（用于将输入的字符串变成大写字符串）。

reverser组件和converter组件都比较简单，每个组件对应的接口仅有一个方法，它们的代码如下：

```
// serviceweaver-examples/httpserver/reverser.go
package main
import (
"context"
"github.com/ServiceWeaver/weaver"
)
// Reverser component.
type Reverser interface {
Reverse(context.Context, string) (string, error)
}
// Implementation of the Reverser component.
type reverser struct {
weaver.Implements[Reverser]
}
func (r *reverser) Reverse(_ context.Context, s string) (string, error) {
runes := []rune(s)
n := len(runes)
for i := 0; i < n/2; i++ {
runes[i], runes[n-i-1] = runes[n-i-1], runes[i]
}
return string(runes), nil
}
// serviceweaver-examples/httpserver/converter.go
package main
import (
"context"
"strings"
"github.com/ServiceWeaver/weaver"
)
// Converter component.
type Converter interface {
ToUpper(context.Context, string) (string, error)
}
// Implementation of the Converter component.
type converter struct {
weaver.Implements[Converter]
}
func (r *converter) ToUpper(_ context.Context, s string) (string, error) {
return strings.ToUpper(s), nil
}
```


接下来，我们实现这个示例的实现weaver.Main接口的app类型：

```
// serviceweaver-examples/httpserver/main.go
type app struct {
weaver.Implements[weaver.Main]
reverser weaver.Ref[Reverser]
converter weaver.Ref[Converter]
lis weaver.Listener
}
```


这里app结构体类型通过weaver.Ref嵌入了实现了另外两个组件接口的组件实例，Ref函数的定义如下：

```
// Ref[T] is a field that can be placed inside a component implementation
// struct. T must be a component type. Service Weaver will automatically
// fill such a field with a handle to the corresponding component.
type Ref[T any] struct {
value T
}
// Get returns a handle to the component of type T.
func (r Ref[T]) Get() T { return r.value }
```


此外，通过泛型类型Ref的Get方法，可以获得对相应组件的访问权。

app结构体类型中还包含了一个weaver.Listener类型的实例，Listener理论上并非组件，而是Weaver框架提供了网络服务端口监听的实现，可以放置在任何提供网络服务的组件实现内部，比如本示例的app这个main组件。app将reverser、converter和listener聚合在一起，为后续的serve函数实现提供支持。

接下来，我们看看serve函数的实现：

```
// serviceweaver-examples/httpserver/main.go
func serve(ctx context.Context, app *app) error {
// The lis listener will listen on a random port chosen by the operating
// system. This behavior can be changed in the config file.
fmt.Printf("http listener available on %v\n", app.lis)
// Serve the /reverse endpoint.
http.HandleFunc("/reverse", func(w http.ResponseWriter, r *http.Request) {
name := r.URL.Query().Get("name")
if name == "" {
name = "World"
}
reversed, err := app.reverser.Get().Reverse(ctx, name)
if err != nil {
http.Error(w, err.Error(), http.StatusInternalServerError)
return
}
fmt.Fprintf(w, "after reversing, name is %s\n", reversed)
})
// Serve the /convert endpoint.
http.HandleFunc("/convert", func(w http.ResponseWriter, r *http.Request) {
name := r.URL.Query().Get("name")
if name == "" {
name = "World"
}
converted, err := app.converter.Get().ToUpper(ctx, name)
if err != nil {
http.Error(w, err.Error(), http.StatusInternalServerError)
return
}
fmt.Fprintf(w, "after converting, name is %s\n", converted)
})
return http.Serve(app.lis, nil)
}
```


我们看到serve函数定义了两个端点/reverse和/convert的Handler函数，并通过http.Serve启动了一个http服务器，http服务器返回，应用退出，否则http服务将一直运行。

我们来运行一下这个程序：

```
$cd serviceweaver-examples/httpserver
$go mod tidy
$weaver generate .
$go run .
╭───────────────────────────────────────────────────╮
│ app : httpserver │
│ deployment : 55827837-896f-4060-88c2-f1f1d953d142 │
╰───────────────────────────────────────────────────╯
http listener available on [::]:59493
```


我们看到，示例中的httpserver启动后在59493这个端口监听客户端的连接，我们用curl工具来测试一下：

```
$curl "http://localhost:59493/convert?name=abcdefg"
after converting, name is ABCDEFG
$curl "http://localhost:59493/reverse?name=abcdefg"
after reversing, name is gfedcba
```


我们看到，无论是reverser组件还是converter组件工作都正常。

由于我们没有指定端口，59493是一个随机端口。如果要指定监听的地址和端口，我们可以借助weaver提供的toml格式的配置文件来实现：

```
// weaver.toml
[single]
listeners.lis = {address = "localhost:8080"}
```


基于weaver.toml配置文件启动httpserver的命令如下：

```
$SERVICEWEAVER_CONFIG=weaver.toml go run .
╭───────────────────────────────────────────────────╮
│ app : httpserver │
│ deployment : ee49694c-4935-4f44-96f3-cc7d1d0167ae │
╰───────────────────────────────────────────────────╯
http listener available on 127.0.0.1:8080
```


在这种模式下启动的httpserver，所有组件都会在一个单一的进程中，组件间的通信通过方法调用进行。这种单体程序在单个进程中部署运行的方式称为**single process部署模式**，十分适合开发者对程序的开发与调试。weaver为这种方式提供了专门的子命令single，我们可以通过single命令在单进程启动httpserver，不过我们要修改一下weaver.toml：

```
// weaver.toml
[single]
listeners.lis = {address = "localhost:8080"}
[serviceweaver]
binary = "./httpserver"
```


无论是single子命令，还是后面即将讲到的multi，都是基于一个可执行文件进行的，因此我们要将httpserver这个示例编译为一个可执行文件”httpserver”，我已经将编译命令放入Makefile，大家输入make命令执行即可。

有了可执行的二进制文件httpserver后，我们就可以使用single子命令启动单进程版的httpserver了：

```
$weaver single deploy weaver.toml
╭───────────────────────────────────────────────────╮
│ app : httpserver │
│ deployment : ad7c0341-d5d2-4182-8944-306d7682e708 │
╰───────────────────────────────────────────────────╯
http listener available on 127.0.0.1:8080
```


在开篇讲Service Weaver的三个核心原则时提到，基于Weaver的应用既可以跑在一个进程中，也可以部署在多个进程，以及云提供商的k8s环境中，下面我们就来看看weaver应用的部署，先来将单进程部署模式改为本地多进程部署模式。

## 4. 部署

基于Weaver应用的部署方式与编码完全解耦，我们无需修改源码便可以实现多进程部署。唯一要做的就是改改weaver.toml，新增多进程部署模式下应用的监听地址信息：

```
// weaver.toml
[single]
listeners.lis = {address = "localhost:8080"}
[serviceweaver]
binary = "./httpserver"
[multi]
listeners.lis = {address = "localhost:8080"} // 新增
```


接下来使用下面命令，我们就可以将httpserver以多进程的形式启动起来：

```
$weaver multi deploy weaver.toml
╭───────────────────────────────────────────────────╮
│ app : httpserver │
│ deployment : bd689290-4929-47f1-a0f0-774d5e1a9307 │
╰───────────────────────────────────────────────────╯
S1003 18:51:02.042859 stdout ac04576d │ http listener available on 127.0.0.1:8080
S1003 18:51:02.043210 stdout c03c4eed │ http listener available on 127.0.0.1:8080
```


weaver multi子命令提供了查看httpserver多进程启动后状态的方法：

```
$weaver multi status
╭──────────────────────────────────────────────────────────╮
│ DEPLOYMENTS │
├────────────┬──────────────────────────────────────┬──────┤
│ APP │ DEPLOYMENT │ AGE │
├────────────┼──────────────────────────────────────┼──────┤
│ httpserver │ bd689290-4929-47f1-a0f0-774d5e1a9307 │ 1m3s │
╰────────────┴──────────────────────────────────────┴──────╯
╭───────────────────────────────────────────────────────────────╮
│ COMPONENTS │
├────────────┬────────────┬──────────────────────┬──────────────┤
│ APP │ DEPLOYMENT │ COMPONENT │ REPLICA PIDS │
├────────────┼────────────┼──────────────────────┼──────────────┤
│ httpserver │ bd689290 │ weaver.Main │ 30194, 30195 │
│ httpserver │ bd689290 │ httpserver.Converter │ 30198, 30199 │
│ httpserver │ bd689290 │ httpserver.Reverser │ 30196, 30197 │
╰────────────┴────────────┴──────────────────────┴──────────────╯
╭─────────────────────────────────────────────────────╮
│ LISTENERS │
├────────────┬────────────┬──────────┬────────────────┤
│ APP │ DEPLOYMENT │ LISTENER │ ADDRESS │
├────────────┼────────────┼──────────┼────────────────┤
│ httpserver │ bd689290 │ lis │ 127.0.0.1:8080 │
╰────────────┴────────────┴──────────┴────────────────╯
```


在status输出的信息中，我们能看到deployment(部署)信息、组件(components)信息以及listener信息。从组件信息来看，weaver multi子命令将每个component放入了一个单独进程，包括main component，并且每个component的副本数(replica)为2，即一共启动了6个进程。从下面ps命令的输出结果也能印证这点：

```
$ps -ef|grep httpserver
501 30194 30193 0 6:51下午 ttys006 0:00.05 /Users/tonybai/test/go/service-weaver/httpserver/httpserver
501 30195 30193 0 6:51下午 ttys006 0:00.05 /Users/tonybai/test/go/service-weaver/httpserver/httpserver
501 30196 30193 0 6:51下午 ttys006 0:00.07 /Users/tonybai/test/go/service-weaver/httpserver/httpserver
501 30197 30193 0 6:51下午 ttys006 0:00.04 /Users/tonybai/test/go/service-weaver/httpserver/httpserver
501 30198 30193 0 6:51下午 ttys006 0:00.05 /Users/tonybai/test/go/service-weaver/httpserver/httpserver
501 30199 30193 0 6:51下午 ttys006 0:00.04 /Users/tonybai/test/go/service-weaver/httpserver/httpserver
```


在multi process这种模式下，应用的各个组件由于不在同一进程内，它们之间的通信由基于方法调用改为了基于RPC调用的方式。

weaver multi还提供了以web形式查看应用运行状态的命令：dashboard

```
$weaver multi dashboard
Dashboard available at: http://127.0.0.1:62183
```


weaver multi dashboard命令会自动打开浏览器并展示httpserver的各种运行信息和状态信息：

![](../../assets/dbfb42b72f038bee.png)


点击页面上的Deployment超链接，我们将进入到下面的页面中：

![](../../assets/9dcec6007bb2af72.png)


除此之外，页面最下方还有一个展示组件拓扑以及组件间traffic的图：

![](../../assets/f1694af64e9a10d7.png)


通过上图我们知道，reverse端点和convert端点分别接到过2次和1次请求。

注：web状态页面上的traces由于没有开启trace，会暂无数据。


和weaver multi一样，weaver ssh可以实现多机器部署，weaver kube实现基于k8s的部署，weaver gke实现在Google Kubernetes Engine上的部署，这里的multi、ssh、kube等都可以称为**deployer**。single、multi、ssh是weaver内置支持的，而其他weaver

注：由于手里没有现成的kubernetes环境，weaver kube命令无法展示了。


到这里，我们已经践行了Service Weaver的两大核心原则：开发阶段以单体程序形式编码开发，以及运行时通过不同deployer(multi、ssh、k8s等)来实现部署环境与代码的解耦。到这里，你是否体会到了本文题目“以单体形式编码，以微服务形式部署”的深意了呢！

下面我们再来看看Weaver核心原则的第3条：原子升级。

## 5. 升级

对于使用go run或weaver multi deployment部署的应用程序来说，避免升级过程中的跨版本通信是轻而易举的事，因为每个部署都是独立运行的。

我本地没有Kubernetes环境，也没有GKE的账号，那么如何验证weaver的原子升级过程呢？好在weaver提供了gke-local，即在本地建立一个模拟gke环境，我们可以使用这种方式来看看通过weaver如何实现app的原子升级。

首先我们要执行下面命令单独安装weaver-gke-local：

```
$go install github.com/ServiceWeaver/weaver-gke/cmd/weaver-gke-local@latest
```


在我的机器和网络环境下，这个安装过程略显“漫长”，因为要拉取很多依赖的go module，还包括像k8s、k8s client这样的go module。

安装好weaver-gke-local后，我们基于httpserver建立一个新module：httpserver-upgrade。然后修改其weaver.toml，增加gke和rollout相关配置：

```
// serviceweaver-examples/httpserver-upgrade/weaver.toml
[single]
listeners.lis = {address = "localhost:8080"}
[serviceweaver]
binary = "./httpserver"
rollout = "5m" # Perform five minutes slow rollout.
[multi]
listeners.lis = {address = "localhost:8080"}
[gke]
regions = ["us-west1"]
listeners.lis = {public_hostname = "hello.com"}
```


然后，为了区分不同版本，我在main.go中为各个端点的处理handler加上了一些带有版本信息的日志，并重新执行make构建新的可执行文件。

下面我们就在gke-local环境下首次部署httpserver：

```
$weaver gke-local deploy weaver.toml
Deploying the application... Done
Version "b343b4de-bb84-4bd7-8bc0-09eb0054b07d" of app "httpserver" started successfully.
Note that stopping this binary will not affect the app in any way.
Tailing the logs...
S1004 06:33:14.621470 stdout ea68b26c │ http v1 listener available on http://localhost:8000
S1004 06:33:14.627226 stdout be97798d │ http v1 listener available on http://localhost:8000
```


我们可以ctrl+c结束weaver gke-local deploy这个命令的执行，但一旦部署成功，即便这个命令退出，已经部署的程序依然会运行。

```
^CTo continue watching the logs, run the following command:
weaver gke-local logs --follow 'version == "b343b4de"'
```


并且按照上述提示，我们可以继续执行下面命令来tail整个应用的输出日志：

```
$weaver gke-local logs --follow 'version == "b343b4de"'
S1004 06:33:14.621470 stdout ea68b26c │ http v1 listener available on http://localhost:8000
S1004 06:33:14.627226 stdout be97798d │ http v1 listener available on http://localhost:8000
```


和multi子命令在本地多进程部署一样，在gke-local下部署后，我们也可以使用status查看应用部署信息和状态：

```
$weaver gke-local status
╭────────────────────────────────────────────────────────────────────╮
│ Deployments │
├────────────┬──────────────────────────────────────┬───────┬────────┤
│ APP │ DEPLOYMENT │ AGE │ STATUS │
├────────────┼──────────────────────────────────────┼───────┼────────┤
│ httpserver │ b343b4de-bb84-4bd7-8bc0-09eb0054b07d │ 4m55s │ ACTIVE │
╰────────────┴──────────────────────────────────────┴───────┴────────╯
╭─────────────────────────────────────────────────────────────────────╮
│ COMPONENTS │
├────────────┬────────────┬──────────┬──────────────────────┬─────────┤
│ APP │ DEPLOYMENT │ LOCATION │ COMPONENT │ HEALTHY │
├────────────┼────────────┼──────────┼──────────────────────┼─────────┤
│ httpserver │ b343b4de │ us-west1 │ weaver.Main │ 2/2 │
│ httpserver │ b343b4de │ us-west1 │ httpserver.Converter │ 2/2 │
│ httpserver │ b343b4de │ us-west1 │ httpserver.Reverser │ 2/2 │
╰────────────┴────────────┴──────────┴──────────────────────┴─────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ TRAFFIC │
├───────────┬────────────┬────────────┬────────────┬──────────┬────────────┬──────────────────┤
│ HOST │ VISIBILITY │ APP │ DEPLOYMENT │ LOCATION │ ADDRESS │ TRAFFIC FRACTION │
├───────────┼────────────┼────────────┼────────────┼──────────┼────────────┼──────────────────┤
│ hello.com │ public │ httpserver │ b343b4de │ us-west1 │ [::]:62559 │ 0.5 │
│ hello.com │ public │ httpserver │ b343b4de │ us-west1 │ [::]:62564 │ 0.5 │
╰───────────┴────────────┴────────────┴────────────┴──────────┴────────────┴──────────────────╯
╭────────────────────────────╮
│ ROLLOUT OF httpserver │
├─────────────────┬──────────┤
│ │ us-west1 │
├─────────────────┼──────────┤
│ TIME │ b343b4de │
│ Oct 3 22:37:59 │ 1.00 │
╰─────────────────┴──────────╯
```


我们看到整个应用被模拟部署到us-west1 region，每个组件有两个副本，用ps命令查看，我们也能看到6个进程：

```
$ps -ef|grep httpserver
501 38480 35224 0 6:33上午 ttys006 0:00.13 /Users/tonybai/test/go/service-weaver/httpserver-upgrade/httpserver
501 38481 35224 0 6:33上午 ttys006 0:00.11 /Users/tonybai/test/go/service-weaver/httpserver-upgrade/httpserver
501 38482 35224 0 6:33上午 ttys006 0:00.10 /Users/tonybai/test/go/service-weaver/httpserver-upgrade/httpserver
501 38483 35224 0 6:33上午 ttys006 0:00.10 /Users/tonybai/test/go/service-weaver/httpserver-upgrade/httpserver
501 38484 35224 0 6:33上午 ttys006 0:00.10 /Users/tonybai/test/go/service-weaver/httpserver-upgrade/httpserver
501 38485 35224 0 6:33上午 ttys006 0:00.10 /Users/tonybai/test/go/service-weaver/httpserver-upgrade/httpserver
```


现在我们可以使用curl命令来验证一下应用的可用性：

```
$curl --header 'Host: hello.com' "http://localhost:8000/reverse?name=abcdefg"
after reversing-v1, name is gfedcba
$curl --header 'Host: hello.com' "http://localhost:8000/reverse?name=abcdefg"
after reversing-v1, name is gfedcba
$curl --header 'Host: hello.com' "http://localhost:8000/reverse?name=abcdefg"
after reversing-v1, name is gfedcba
$curl --header 'Host: hello.com' "http://localhost:8000/convert?name=abcdefg"
after converting-v1, name is ABCDEFG
$curl --header 'Host: hello.com' "http://localhost:8000/convert?name=abcdefg"
after converting-v1, name is ABCDEFG
```


可以看到，app工作正常！

此外，我们还可以通过dashboard可以以图形化的方式观测app状态(weaver gke-local dashboard)，在后续升级过程中，通过dashboard可以清楚地看到整个升级过程：

![](../../assets/05876084a289cd3a.png)


注：gke-local会在本地建立一个模拟load balancer，并将发到hello.com主机的请求按Traffic Fraction分发给不同副本。


接下来，我们就来开发httpserver的v2版本，将main.go中的version改为v2，然后重新编译httpserver，执行下面命令部署新版httpserver：

```
$weaver gke-local deploy weaver.toml
Deploying the application... Done
Version "2ee38e73-323f-4b42-b115-ee5bc40a8c09" of app "httpserver" started successfully.
Note that stopping this binary will not affect the app in any way.
Tailing the logs...
S1004 06:50:12.575585 stdout 702058ba │ http v2 listener available on http://localhost:8000
S1004 06:50:12.586352 stdout ef3d7c3f │ http v2 listener available on http://localhost:8000
^CTo continue watching the logs, run the following command:
weaver gke-local logs --follow 'version == "2ee38e73"'
```


由于我们配置的rollout为5分钟，所以新版httpserver替换掉旧版httpserver的过程会持续5分钟。而这个过程中load balancer针对新旧两个版本的Traffic Fraction也会动态调整：旧版本会逐渐降低，新版本会逐渐升高：

![](../../assets/5b067a05ca409b4f.png)


![](../../assets/59f06f898ae3abf8.png)


![](../../assets/91e7bd76defa2e79.png)


这时向app发送的请求，既可能由v1版本处理，也可能由v2版本处理：

```
$curl --header 'Host: hello.com' "http://localhost:8000/convert?name=abcdefg"
after converting-v1, name is ABCDEFG
$curl --header 'Host: hello.com' "http://localhost:8000/reverse?name=abcdefg"
after reversing-v1, name is gfedcba
$curl --header 'Host: hello.com' "http://localhost:8000/convert?name=abcdefg"
after converting-v1, name is ABCDEFG
$curl --header 'Host: hello.com' "http://localhost:8000/reverse?name=abcdefg"
after reversing-v2, name is gfedcba
```


最后新版app将全面接手对请求的处理：

![](../../assets/da5ff4849135659d.png)


之后，旧版的app将被delete掉：

![](../../assets/dbfbea3dd15c1d19.png)


这样新版app的升级部署(rollout)就结束了！rollout后，所有请求将被v2版本处理，应答中将带有v2字样。

在新版本升级的过程中，你如果使用ps查看httpserver进程数量，你会发现数量多出一倍，那是因为整个rollout过程采用的是[蓝绿部署](https://en.wikipedia.org/wiki/Blue%E2%80%93green_deployment)方式，即完全部署一套新app，然后通过调整load balancer的分发比例，让新版app逐渐承担全部流量，而在这个过程中，不会存在新老版本组件交互的情况出现。下图展示了这一过程：

![](../../assets/8a2a3e77c8e31076.png)


注：如果要杀掉app，可以用weaver gke-local kill httpserver命令。


## 6. 小结

Service Weaver是一个优秀的框架，可以帮助开发人员以单体形式快速构建、以微服务形式快速部署分布式应用，其三个核心原则的创新思路值得我们学习借鉴。

但Service Weaver也不是万能的，Service Weaver主要针对在线的分布式服务系统，即需要在用户请求到达时处理它们的系统，例如网络应用程序或API Server正是此类分布式服务系统。基于Weaver开发这类系统，应用可以轻松获取网络Listener并建立HTTP 服务器，应用可以支持原子升级，且应用组件的副本数量可以根据请求压力的大小自动扩缩(本文并未演示这个特性)。

不过要注意的是：Service Weaver仅仅开源了几个月，其API尚未Stable，本文中的示例基于v0.21.2版本实现，也许在未来的某个时间点，这些示例可能会因API的变化而无法Run起来, status命令和dashboard命令所展现给用户的样式也会发生变化。另外学习weaver本身也是有学习成本的，weaver自身的代码由于采用了泛型和[反射](https://tonybai.com/2023/06/04/reflection-programming-guide-in-go/)，读起来也是很晦涩。

综上，Service Weaver所践行的理念的优秀的，但考虑其成熟度以及Go社区崇尚的“The Best Go framework is no framework”的信条，选择引入Service Weaver框架之前务必要仔细斟酌。

本文涉及的Go源码，可以在[这里](https://github.com/bigwhite/experiments/tree/master/serviceweaver-examples)下载。

## 7. 参考资料

[A Quick Introduction to Service Weaver](https://serviceweaver.dev/blog/quick_intro.html)– https://serviceweaver.dev/blog/quick_intro.html[Towards Modern Development of Cloud Applications](https://serviceweaver.dev/assets/docs/hotos23_vision_paper.pdf)– https://serviceweaver.dev/assets/docs/hotos23_vision_paper.pdf[Service Weaver FAQ](https://serviceweaver.dev/docs.html#faq)– https://serviceweaver.dev/docs.html#faq

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

微博(暂不可用)：https://weibo.com/bigwhite20xx

微博2：https://weibo.com/u/6484441286

博客：tonybai.com

github: https://github.com/bigwhite

Gopher Daily归档 – https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论