---
title: 聊聊Go与依赖注入
url: https://tonybai.com/2023/09/28/dependency-injection-with-go/
published: '2023-09-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 聊聊Go与依赖注入

![](../../assets/3347291eb5b83bcd.png)


[本文永久链接](https://tonybai.com/2023/09/28/dependency-injection-with-go) – https://tonybai.com/2023/09/28/dependency-injection-with-go

如果你读过[Robert C. Martin](http://cleancoder.com/)的[《敏捷软件开发：原则、模式与实践》](https://book.douban.com/subject/1140457/)(书的封皮见下图)，那么你一定知道经典的[SOLID设计原则](http://cleancoder.com/files/solid.md)中的“D”：依赖倒置原则（Dependency Inversion Principle, DIP）。

![](../../assets/560ce825781ec984.jpg)


依赖倒置原则是面向对象设计中的基本原则之一，它阐述了高层模块和低层模块的依赖关系应该倒置(如下图)，也就是:

- 高层模块不应该依赖低层模块，二者都应该依赖其抽象
- 抽象不应该依赖细节，细节应该依赖抽象

![](../../assets/fa78b9252028ef4b.png)


依赖倒置原则实际上就是对控制反转(Inversion of Control，IoC)这一概念的阐述，而[依赖注入(Dependency Injection)](http://en.wikipedia.org/wiki/Dependency_injection)是实现控制反转的一种机制。所以可以说，依赖倒置原则是设计级的指导思想，它提出了正确的依赖关系；而依赖注入是实现级的具体设计模式，它将组件的依赖关系控制权移到了外部，实现了组件之间的解耦，是对依赖倒置原则的一种实现手段。

依赖注入可以帮助你开发出松耦合的代码，**松耦合使代码更易于维护**。

在[《Go语言包设计指南》](https://tonybai.com/2023/06/18/go-package-design-guide)一文中，我们提到过：在Go中，耦合发生在包这一层次。而在Go代码层面最低的耦合是**接口耦合**。在Go中，接口的实现是隐式的，即a包实现b包中定义的接口时是不需要显式导入b包的，我们可以在c包中完成对a包与b包的组装，这样c包依赖a包和b包，但a包与b包之间没有任何耦合。那么负责组装a包与b包的c包能否在代码层面消除掉对a和b的依赖呢？这个就很难了。不过我们可以使用**依赖注入**技术来消除在代码层面手动基于依赖进行初始化或创建时的复杂性，在中大型的程序中，依赖注入的优点更能得到体现。

在这篇文章中，我们就来聊聊Go中依赖注入可以解决的问题，并初步认识一下两个在Go社区认可度较高的Go依赖注入框架。

## 1. 手动注入

我们先建立一个符合DIP原则的例子，其依赖关系如下图：

![](../../assets/fac7dd52c41bca76.png)


这里有三个“模块”，从高到低分别为Service、BussinessLogic和DatabaseAccess。Service是一个接口，其实现ServiceImpl依赖BussinessLogic接口。Business是BussinessLogic的实现，它还依赖DatabaseAccess接口。Database则是DatabaseAccess接口的实现。

围绕这一示例，我们分别用手动组装和依赖注入框架演示一下如何实现注入，先来看一下手动组装与注入。

下面是示例的项目结构布局：

```
./manual
└── demo/
├── Makefile
├── business/
│ └── business.go
├── database/
│ └── database.go
├── go.mod
├── main.go
└── service/
└── service.go
```


manual/demo目录下的service、business和database包下面包含了导出的接口与其具体实现的定义。这里将这些包的代码列出来，这些代码在后续应用依赖注入工具的示例中也是保持不变的：

```
// dependency-injection-examples/manual/demo/service/service.go
package service
import "demo/business"
// Service interface
type Service interface {
HandleRequest() string
}
// ServiceImpl struct
type ServiceImpl struct {
logic business.BusinessLogic
}
// Constructor
func NewService(logic business.BusinessLogic) *ServiceImpl {
return &ServiceImpl{logic: logic}
}
// Implement HandleRequest()
func (s ServiceImpl) HandleRequest() string {
return "Handled request: " + s.logic.ProcessData()
}
// dependency-injection-examples/manual/demo/business/business.go
package business
import (
"demo/database"
)
// BusinessLogic interface
type BusinessLogic interface {
ProcessData() string
}
// Business struct
type Business struct {
db database.DatabaseAccess
}
// Constructor
func NewBusiness(db database.DatabaseAccess) *Business {
return &Business{db: db}
}
// Implement ProcessData()
func (b Business) ProcessData() string {
return "Business logic processed " + b.db.GetData()
}
// dependency-injection-examples/manual/demo/database/database.go
package database
// DatabaseAccess interface
type DatabaseAccess interface {
GetData() string
}
// Database struct
type Database struct{}
func NewDatabase() *Database {
return &Database{}
}
// Implement GetData()
func (db Database) GetData() string {
return "Data from database"
}
```


service.Service是直面client的接口。于是在main函数中，我们实例化一个Service的实现并传给Client，后者调用Service的HandleRequest方法触发全流程。service.NewService的调用依赖一个实现了business.BusinessLogic接口的实例，我们在调用NewService之前还需要调用business.NewBusiness创建一个实现了business.BusinessLogic接口的实例；business.NewBusiness的调用依赖一个实现了database.DatabaseAccess接口的实例，我们在调用NewBusiness之前需要调用database.NewDatabase创建一个实现了database.DatabaseAccess接口的实例。

这就是手工组装的现实：**我们要记住“模块”间的依赖关系，并手动创建对应实例以满足这种依赖**。下面是main函数的代码：

```
// dependency-injection-examples/manual/demo/main.go
package main
import (
"demo/business"
"demo/database"
"demo/service"
"fmt"
)
// Client struct
type Client struct {
service service.Service
}
// Constructor
func NewClient(service service.Service) *Client {
return &Client{service: service}
}
// Call service
func (c Client) MakeRequest() string {
return "Client request: " + c.service.HandleRequest()
}
func main() {
// make dependency injection manually
db := database.NewDatabase()
busi := business.NewBusiness(db)
svc := service.NewService(busi)
client := NewClient(svc)
fmt.Println(client.MakeRequest())
}
```


编译运行上述示例的结果如下：

```
$cd dependency-injection-examples/manual/demo
$make
$./demo
Client request: Handled request: Business logic processed Data from database
```


这种为了满足依赖而进行的手工实例创建的行为，在一些小型或演示型程序中还可以自诩为straightforward，但在拥有上百个包的大型程序中，这种为了组装而进行的创建行为就会因多点发生、依赖众多而显现出“复杂性”和难于维护。为了保持代码的松耦合还要降低组装创建行为的复杂度，依赖注入工具被引入，并且**往往代码库越庞大，引入DI的好处就越发明显**。松耦合带来的好处并不总是立竿见影，但随着时间的推移，随着代码库复杂性的增加，这些好处就会变得显而易见。

注：大家不要进入这样的误区：“采用依赖注入工具的代码就一定是符合DIP原则的松耦合的代码”。至少在Go中，不符合DIP原则的代码(比如没有建立接口抽象)也可以使用依赖注入工具来进行依赖的创建和模块间的组装。


Go社区（尤其是一些大厂）提供了一些Go依赖注入工具，比如：[Google wire](https://github.com/google/wire)、[uber Fx](https://github.com/uber-go/fx)、[facebook inject](https://github.com/facebookarchive/inject)等。这些工具大致可分为两类，一类是**利用代码生成技术的编译期依赖注入**，另一类则是**利用反射技术的运行时依赖注入**。

下面我们分别以编译器依赖注入的Google wire和运行时依赖注入的uber fx为例来看看如何通过依赖注入工具来完成依赖模块的组装(assembly)。

注：facebook的inject已经public archived；google wire目前的开发也不是很active，wire团队给出的理由是要保持wire足够简单并认为从v0.3.0开始，wire已经是功能特性完备的了，目前不接受新feature，仅接受bug报告和修复的补丁pr。只有uber的fx还处于非常积极的开发状态，uber宣称fx是经过uber生产验证的：uber几乎所有的Go服务都是建立在Fx基础之上的。


## 2. google/wire：编译期的依赖注入

[wire](https://go.dev/blog/wire)是由[Google Go Cloud开发包团队](https://gocloud.dev/)于2018年下旬开源的Go编译期依赖注入工具，与uber fx、facebook的inject等使用反射在运行时注入不同的是，wire灵感来自Java的[Dagger 2](https://google.github.io/dagger/)，使用的是代码生成技术，而不是反射或服务定位器(service locator)技术。

相较于运行时依赖注入，编译期间注入的最大好处就是**生成的依赖注入和组装的代码是对你可见的**，没有任何背后的“魔法”。这便于在编译期捕捉到注入过程的错误，也便于代码的调试。

此外，wire团队认为编译期注入可以避免依赖膨胀。Wire生成的代码只会导入所需的依赖项，因此，你的二进制文件不会有未使用的导入。运行时依赖项注入在运行时之前无法识别未使用的依赖项。

下面我们就用wire注入来改造一下上面的示例。

注：安装wire命令为go install github.com/google/wire/cmd/wire@latest 。


相对于manual那个示例，我们在main包下面增加一个新文件wire.go：

```
// dependency-injection-examples/wire/demo/wire.go
//go:build wireinject
// +build wireinject
package main
// wire.go
import (
"demo/business"
"demo/database"
"demo/service"
"github.com/google/wire"
)
func InitializeService() service.Service {
wire.Build(service.NewService,
wire.Bind(new(service.Service), new(*service.ServiceImpl)),
business.NewBusiness,
wire.Bind(new(business.BusinessLogic), new(*business.Business)),
database.NewDatabase,
wire.Bind(new(database.DatabaseAccess), new(*database.Database)),
)
return nil
}
```


我们看到wire.go中提供了一个InitializeService函数，用于为main函数中的Client实例提供一个service.Service接口的具体实现。但是在这个函数中我们并没有像manual中那样手工调用NewService等来创建实例，我们仅仅是将各个“模块”Service、BussinessLogic以及DatabaseAccess的实例的创建函数传给了wire.Build函数。另外我们看到wire.go这个源文件使用了build tag，这个文件仅仅是用于代码生成，并不会参与到最终的代码编译过程中，这也是InitializeService函数的返回值随意设置为nil的原因，这个nil在代码生成过程中会被忽略并替换掉。

注：为什么要使用wire.Bind？我们示例中的各个模块的NewXXX函数接受的参数都为接口类型，返回的都是具体的类型实例，这符合Go的惯例。但如果不使用wire.Bind，wire将无法知道NewXXX依赖的接口类型参数该如何创建！通过wire.Bind告诉wire某个接口类型参数，比如service.Service，可由创建如*service.ServiceImpl的类型替代。关于

[Binding Interfaces的具体介绍]，可以参考wire官方文档。

接下来，我们就可以通过wire命令生成代码，完成注入过程：

```
$cd dependency-injection-examples/wire/demo
$wire
wire: demo: wrote /Users/tonybai/Go/src/github.com/bigwhite/experiments/dependency-injection-examples/wire/demo/wire_gen.go
```


wire工具基于wire.go生成了wire_gen.go文件，在该示例中，wire_gen.go的内容如下：

```
// Code generated by Wire. DO NOT EDIT.
//go:generate go run github.com/google/wire/cmd/wire
//go:build !wireinject
// +build !wireinject
package main
import (
"demo/business"
"demo/database"
"demo/service"
)
// Injectors from wire.go:
func InitializeService() service.Service {
databaseDatabase := database.NewDatabase()
businessBusiness := business.NewBusiness(databaseDatabase)
serviceImpl := service.NewService(businessBusiness)
return serviceImpl
}
```


看一下wire生成的代码，和我们在manual中手动组装的代码基本是一样的。基于这份代码，我们调整一下main函数，主要是去掉手动组装的过程，改为直接调用InitializeService：

```
// dependency-injection-examples/wire/demo/main.go
func main() {
// make dependency injection by code generated by wire
svc := InitializeService()
client := NewClient(svc)
fmt.Println(client.MakeRequest())
}
```


运行一下wire注入这个demo，其结果与manual demo是一致的：

```
$cd dependency-injection-examples/wire/demo
$make
$./demo
Client request: Handled request: Business logic processed Data from database
```


关于wire，这里仅是作了“浅尝辄止”的介绍。要想深入了解wire的功能特性，可以阅读[Wire tutorial](https://github.com/google/wire/blob/main/_tutorial/README.md)和[Wire User Guide](https://github.com/google/wire/blob/main/docs/guide.md)。

接下来，我们再来看看如何使用uber/fx来实现依赖注入。

## 3. uber/fx：运行时的依赖注入

如果我没记错的话，uber应该是先开源的[dig](https://github.com/uber-go/dig)，再有的[fx](https://github.com/uber-go/fx)。dig是基于反射的依赖注入工具包，而fx则是由dig支撑的依赖注入框架。对应普通Go开发者而言，直接使用fx就对了。

下面是使用fx实现上面示例依赖注入的代码，我们只需要改造一下main.go：

```
// dependency-injection-examples/fx/demo/main.go
func main() {
app := fx.New(
fx.Provide(
fx.Annotate(
service.NewService,
fx.As(new(service.Service)),
),
),
fx.Provide(
fx.Annotate(
business.NewBusiness,
fx.As(new(business.BusinessLogic)),
),
),
fx.Provide(
fx.Annotate(
database.NewDatabase,
fx.As(new(database.DatabaseAccess)),
),
),
fx.Invoke(func(svc service.Service) {
client := NewClient(svc)
fmt.Println(client.MakeRequest())
}),
fx.NopLogger, // no fx log output
)
app.Run()
}
```


我们在main函数中，使用fx.Provide注册了所有依赖类型的实例的构造方法(NewXXX)，然后将我们要执行的代码放入一个匿名函数，并传给fx.Invoke。当我们运行程序时，fx会在内存中构建对象调用依赖图，并使用Provide中注册的类型实例的构造方法构造实例，完成依赖注入和代码组装，然后运行传给Invoke的函数。

在向fx.Provide传递NewXXX时，我们使用了fx.Annotate，其目的与在wire示例中使用wire.Bind一样，即将一个类型实例转换为接口类型，以满足参数为接口类型的NewXXX的依赖所需。关于[fx.Annotate的详细说明](https://uber-go.github.io/fx/annotate.html#annotating-a-function)，可参考fx的官方文档。

上述使用fx示例还有两处要提及一下，一个是使用fx.NopLogger关闭fx框架自身的日志输出；另外一个则是上述示例run起来后并不会自动退出，只有当按下ctrl+c后，程序才会因收到系统退出信号而退出！

对比fx和wire，你可能也发现了这样一点：fx将很多工作放到了“背后隐蔽处”，如果你不了解fx框架的运行机理，你很难使用好fx框架；而wire生成的代码就是编译到程序中的代码，没有额外的“魔法”。

当然fx不仅提供了Provide、Annotate、Invoke，其他一些功能特性大家可以自行到[官方文档](https://uber-go.github.io/fx/intro.html)阅读并理解使用。

## 4. 小结

依赖注入常用来解决软件模块之间高度耦合的问题。传统的程序设计中，一个模块直接new或者静态调用另一个模块，这使得模块之间产生了强耦合。依赖注入将模块创建和注入的控制权移交给外部，由外部动态地将某个实现类实例注入到需要它的模块中。这样实现了模块之间的松耦合。

如果你来自Java等面向对象编程语言的群体，你对依赖注入肯定不陌生。

但是在Go社区，我觉得**依赖注入并非惯用法**。Go社区很多人崇尚“You often don’t need frameworks in Go”这样的信条。但凡引入一个框架，都会带来学习和理解上的额外负担，Go依赖注入框架亦是如此。

究竟是否使用依赖注入，完全取决于你在开发过程中的权衡和取舍。

如果你决定使用依赖注入，wire和fx都是你可选择的框架。就目前情况来看，fx是目前开发最active、历经生产考验最多的Go依赖注入框架，不过要想用好fx，必须深入理解fx的运行机制和底层原理，这又会带来一定的学习负担。

本文涉及的Go源码，可以在[这里](https://github.com/bigwhite/experiments/tree/master/dependency-injection-examples)下载。

## 5. 参考资料

[《Dependency Injection：Principles, Practices, and Patterns》](https://book.douban.com/subject/30932387/)– https://book.douban.com/subject/30932387/[Compile-time Dependency Injection With Go Cloud’s Wire](https://go.dev/blog/wire)– https://go.dev/blog/wire[Wire tutorial](https://github.com/google/wire/blob/main/_tutorial/README.md)– https://github.com/google/wire/blob/main/_tutorial/README.md[Wire User Guide](https://github.com/google/wire/blob/main/docs/guide.md)– https://github.com/google/wire/blob/main/docs/guide.md[Inversion of Control Containers and the Dependency Injection pattern](https://martinfowler.com/articles/injection.html)– https://martinfowler.com/articles/injection.html

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

老师您好 我这边开源了一个 可以快速进行自动化依赖注入的工具 是基于wire的实现

但是通过规范的注解命令工具 提供自动化的 Wire 声明维护

这个工具还包含很多其他不同的插件以提供强大的生态化功能，如 AOP代理，API路由映射，ORM生成等等

希望老师能够过目 如果对此项目认可 也可以协助宣传

https://github.com/go-zing/gozz

手动点赞！