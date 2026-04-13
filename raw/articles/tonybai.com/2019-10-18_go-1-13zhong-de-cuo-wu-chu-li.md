---
title: Go 1.13中的错误处理
url: https://tonybai.com/2019/10/18/errors-handling-in-go-1-13/
published: '2019-10-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.13中的错误处理

## 介绍

在过去的[十年](https://tonybai.com/2017/10/24/go-evolution-for-ten-years-an-interview-by-osc/)中， Go的[errors are values](https://blog.golang.org/errors-are-values)的理念在[编码实践](https://tonybai.com/2017/04/20/go-coding-in-go-way/)中运行得也很良好。尽管标准库对[错误处理](https://tonybai.com/2015/10/30/error-handling-in-go/)的的支持很少（只有errors.New和fmt.Errorf函数可以用来构造仅包含字符串消息的错误），但是内置的error接口使Go程序员可以添加所需的任何信息。它所需要的只是一个实现Error方法的类型：

```
type QueryError struct {
Query string
Err error
}
func (e *QueryError) Error() string { return e.Query + ": " + e.Err.Error() }
```


像这样的错误类型无处不在，它们存储的信息变化很大，从时间戳到文件名再到服务器地址。通常，该信息包括另一个较低级别的错误以提供其他上下文信息。

在Go代码中，使用一个包含了另一个错误的错误类型的模式十分普遍，以至于经过[广泛讨论](https://golang.org/issue/29934)后，[Go 1.13](https://tip.golang.org/doc/go1.13)为其添加了明确的支持。这篇文章描述了标准库提供的支持：errors包中的三个新功能，以及fmt.Errorf中添加的新格式化动词。

在详细描述这些变化之前，让我们先回顾一下在Go语言的早期版本中如何检查和构造错误。

## Go 1.13版本之前的错误处理

### 检查错误

错误是值(errors are values)。程序通过几种方式基于这些值来做出决策。最常见的是通过与nil的比较来确定操作是否失败。

```
if err != nil {
// 出错了!
}
```


有时我们将错误与**已知的前哨值(sentinel value)**进行比较来查看是否发生了特定错误。比如：

```
var ErrNotFound = errors.New("not found")
if err == ErrNotFound {
// something wasn't found
}
```


错误值可以是满足语言定义的error 接口的任何类型。程序可以使用类型断言(type assertion)或类型开关(type switch)来判断错误值是否可被视为特定的错误类型。

```
type NotFoundError struct {
Name string
}
func (e *NotFoundError) Error() string { return e.Name + ": not found" }
if e, ok := err.(*NotFoundError); ok {
// e.Name wasn't found
}
```


### 添加信息

函数通常在将错误向上传递给调用堆栈时添加额外错误信息，例如对错误发生时所发生情况的简短描述。一种简单的方法是构造一个新错误，并在其中包括上一个错误：

```
if err != nil {
return fmt.Errorf("decompress %v: %v", name, err)
}
```


使用fmt.Errorf创建的新错误将丢弃原始错误中的所有内容（文本除外）。就像我们在前面所看到的QueryError那样，有时我们可能想要定义一个包含基础错误的新错误类型，并将其保存下来以供代码检查。我们再次来看一下QueryError：

```
type QueryError struct {
Query string
Err error
}
```


程序可以查看一个*QueryError值的内部以根据潜在的错误进行决策。有时您会看到称为“展开”错误的信息。

```
if e, ok := err.(*QueryError); ok && e.Err == ErrPermission {
// query failed because of a permission problem
}
```


标准库中的os.PathError类型就是另外一个在错误中包含另一个错误的示例。

## Go 1.13版本的错误处理

### Unwrap方法

Go 1.13在errors和fmt标准库包中引入了新功能以简化处理包含其他错误的错误。其中最重要的不是改变，而是一个约定：包含另一个错误的错误可以实现Unwrap方法来返回所包含的底层错误。**如果e1.Unwrap()返回了e2，那么我们说e1包装了e2，您可以Unwrap e1来得到e2**。

遵循此约定，我们可以为上面的QueryError类型提供一个Unwrap方法来返回其包含的错误：

```
func (e *QueryError) Unwrap() error { return e.Err }
```


Unwrap错误的结果本身(底层错误)可能也具有Unwrap方法。我们将这种通过重复unwrap而得到的错误序列为错误链。

### 使用Is和As检查错误

Go 1.13的errors包中包括了两个用于检查错误的新函数：Is和As。

errors.Is函数将错误与值进行比较。

```
// Similar to:
// if err == ErrNotFound { … }
if errors.Is(err, ErrNotFound) {
// something wasn't found
}
```


As函数用于测试错误是否为特定类型。

```
// Similar to:
// if e, ok := err.(*QueryError); ok { … }
var e *QueryError
if errors.As(err, &e) {
// err is a *QueryError, and e is set to the error's value
}
```


在最简单的情况下，errors.Is函数的行为类似于上面对哨兵错误(sentinel error))的比较，而errors.As函数的行为类似于类型断言(type assertion)。但是，在处理包装错误(包含其他错误的错误）时，这些函数会考虑错误链中的所有错误。让我们再次看一下通过展开QueryError以检查潜在错误：

```
if e, ok := err.(*QueryError); ok && e.Err == ErrPermission {
// query failed because of a permission problem
}
```


使用errors.Is函数，我们可以这样写：

```
if errors.Is(err, ErrPermission) {
// err, or some error that it wraps, is a permission problem
}
```


errors包还包括一个新Unwrap函数，该函数返回调用错误Unwrap方法的结果，或者当错误没有Unwrap方法时返回nil。通常我们最好使用errors.Is或errors.As，因为这些函数将在单个调用中检查整个错误链。

### 用%w包装错误

如前面所述，我们通常使用fmt.Errorf函数向错误添加其他信息。

```
if err != nil {
return fmt.Errorf("decompress %v: %v", name, err)
}
```


在Go 1.13中，fmt.Errorf函数支持新的%w动词。当存在该动词时，所返回的错误fmt.Errorf将具有Unwrap方法，该方法返回参数%w对应的错误。%w对应的参数必须是错误(类型)。在所有其他方面，%w与%v等同。

```
if err != nil {
// Return an error which unwraps to err.
return fmt.Errorf("decompress %v: %w", name, err)
}
```


使用%w创建的包装错误可用于errors.Is和errors.As：

```
err := fmt.Errorf("access denied: %w”, ErrPermission)
...
if errors.Is(err, ErrPermission) ...
```


### 是否包装

在使用fmt.Errorf或通过实现自定义类型将其他上下文添加到错误时，您需要确定新错误是否应该包装原始错误。这个问题没有统一答案。它取决于创建新错误的上下文。包装错误将会被公开给调用者。如果要避免暴露实现细节，那么请不要包装错误。

举一个例子，假设一个Parse函数从io.Reader读取复杂的数据结构。如果发生错误，我们希望报告发生错误的行号和列号。如果从io.Reader读取时发生错误，我们将包装该错误以供检查底层问题。由于调用者为函数提供了io.Reader，因此有理由公开它产生的错误。

相反，一个对数据库进行多次调用的函数可能不应该将其中调用之一的结果解开的错误返回。如果该函数使用的数据库是实现细节，那么暴露这些错误就是对抽象的违反。例如，如果你的程序包pkg中的函数LookupUser使用了Go的database/sql程序包，则可能会遇到sql.ErrNoRows错误。如果使用fmt.Errorf(“accessing DB: %v”, err)来返回该错误，则调用者无法检视到内部的sql.ErrNoRows。但是，如果函数使用fmt.Errorf(“accessing DB: %w”, err)返回错误，则调用者可以编写下面代码：

```
err := pkg.LookupUser(...)
if errors.Is(err, sql.ErrNoRows) …
```


此时，如果您不希望对客户端源码产生影响，该函数也必须始终返回sql.ErrNoRows，即使您切换到其他数据库程序包。换句话说，**包装错误会使该错误成为您API的一部分。如果您不想将来将错误作为API的一部分来支持，则不应包装该错误。**

重要的是要记住，无论是否包装错误，错误文本都将相同。那些试图理解错误的人将得到相同的信息，无论采用哪种方式; 是否要包装错误的选择是关于是否要给程序提供更多信息，以便他们可以做出更明智的决策，还是保留该信息以保留抽象层。

### 使用Is和As方法自定义错误测试

errors.Is函数检查错误链中的每个错误是否与目标值匹配。默认情况下，如果两者相等，则错误与目标匹配。另外，链中的错误可能会通过实现Is方法来声明它与目标匹配。

例如，下面的错误类型定义是受[Upspin error包](https://commandcenter.blogspot.com/2017/12/error-handling-in-upspin.html)的启发，它将错误与模板进行了比较，并且仅考虑模板中非零的字段：

```
type Error struct {
Path string
User string
}
func (e *Error) Is(target error) bool {
t, ok := target.(*Error)
if !ok {
return false
}
return (e.Path == t.Path || t.Path == "") &&
(e.User == t.User || t.User == "")
}
if errors.Is(err, &Error{User: "someuser"}) {
// err's User field is "someuser".
}
```


同样，errors.As函数将使用链中某个错误的As方法，如果该错误实现了As方法。

### 错误和包API

返回错误的程序包（大多数都会返回错误）应描述程序员可能依赖的那些错误的属性。一个经过精心设计的程序包也将避免返回带有不应依赖的属性的错误。

最简单的规约是用于说明操作成功或失败的属性，分别返回nil或non-nil错误值。在许多情况下，不需要进一步的信息了。

如果我们希望函数返回可识别的错误条件，例如“item not found”，则可能会返回包装哨兵的错误。

```
var ErrNotFound = errors.New("not found")
// FetchItem returns the named item.
//
// If no item with the name exists, FetchItem returns an error
// wrapping ErrNotFound.
func FetchItem(name string) (*Item, error) {
if itemNotFound(name) {
return nil, fmt.Errorf("%q: %w", name, ErrNotFound)
}
// ...
}
```


还有其他现有的提供错误的模式，可以由调用方进行语义检查，例如直接返回哨兵值，特定类型或可以使用谓词函数检查的值。

在所有情况下，都应注意不要向用户公开内部细节。正如我们在上面的“是否要包装”中提到的那样，当您从另一个包中返回错误时，应该将错误转换为不暴露基本错误的形式，除非您愿意将来再返回该特定错误。

```
f, err := os.Open(filename)
if err != nil {
// The *os.PathError returned by os.Open is an internal detail.
// To avoid exposing it to the caller, repackage it as a new
// error with the same text. We use the %v formatting verb, since
// %w would permit the caller to unwrap the original *os.PathError.
return fmt.Errorf("%v", err)
}
```


如果将函数定义为返回包装某些标记或类型的错误，请不要直接返回基础错误。

```
var ErrPermission = errors.New("permission denied")
// DoSomething returns an error wrapping ErrPermission if the user
// does not have permission to do something.
func DoSomething() {
if !userHasPermission() {
// If we return ErrPermission directly, callers might come
// to depend on the exact error value, writing code like this:
//
// if err := pkg.DoSomething(); err == pkg.ErrPermission { … }
//
// This will cause problems if we want to add additional
// context to the error in the future. To avoid this, we
// return an error wrapping the sentinel so that users must
// always unwrap it:
//
// if err := pkg.DoSomething(); errors.Is(err, pkg.ErrPermission) { ... }
return fmt.Errorf("%w", ErrPermission)
}
// ...
}
```


## 结论

尽管我们讨论的更改仅包含三个函数和一个格式化动词(%w)，但我们希望它们能大幅改善Go程序中错误处理的方式。我们希望通过包装来提供其他上下文的方式得到Gopher们地普遍使用，从而帮助程序做出更好的决策，并帮助程序员更快地发现错误。

正如Russ Cox在[GopherCon 2019主题演讲](https://blog.golang.org/experiment)中所说的那样，在Go2的道路上，我们进行了实验，简化和发布。现在，我们已经发布了这些更改，我们期待接下来的实验。

本文翻译自Go官方博客：[《Working with Errors in Go 1.13》](https://blog.golang.org/go1.13-errors)

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

一个函数的返回值是’结构体指针+error’，如果函数的实现者要求调用方在调用该函数后需要同时对这两个返回值做非nil判断（即使error为nil，结构体指针也同样有可能为nil），请问您怎么看待这样的设计？

如果把标准库当作教科书，那以我这点浅薄的修为，还没有在这本教科书中找到这样的先例，那据您所知是否有这样的先例？

我觉得严谨的设计者不会要求去判断返回的结构体指针是否为nil的。只需判断返回的error是否为nil。一旦error为nil，则暗示返回的结构体指针是有效的。反之，一旦err != nil，则说明返回的结构体指针是无效的，不应该使用。其实类似的例子很多，比如函数返回(int, err)，当err !=nil时，我们也不应该去使用返回的int，这时的int处于无效状态。因此你说的问题的关键其实是api设计者的问题，他不应该要求对两个返回值都进行非nil判断。

个人没觉得彻底消除了之前的if err != nil{}的代码，只是给错误加了点分组和具体类型值判断，并没有根治多多错误处理的代码的冗余风格！！！这是很失败的设计！还是一样的！根本没改变，不看好go2,看好try….catch….这种。。。本人愚钝，对于go的设计，我想我考虑用装饰器去掉这种无聊的设计！几乎我写100行go代码中，错误处理占领了我40行+的代码，go都出来10年了，还是谷歌出品，如今却说热不热，说不热有点热的程度，却是值得go设计者深思！现在我的首选语言不会是go,只要不是特别要求性能，我都不会采用他，他对我来说是一门糟糕的语言！我更加喜欢python!虽然我只学习了go 3个月，但是就我目前对go库的了解，go需要彻底重写！go库写的很一般，有些api命名不搭调！例子我就不举了！我几乎遍历了一次go的所有库和浏览了一遍go的源码，源码写的很一般！很c范！如果可以选择，我不会成为go的提倡者！go结构体确实是明晰，但是却搭配如此不明晰的错误处理，他使的我的代码逻辑充斥着各种错误处理！这不是我想要的！

1.13中只是解决了 Error value（及error链中值）判断的问题。整体的Error handling框架并未有改进。之前关于error handling的机制在加入go 1.13之前被社区否了。估计还要重新设计和讨论。

一个小细节，补充一下，就是官方关于errors.Unwrap的注释是Unwrap returns nil if the Unwrap method returns []error. 即返回nil还有一种情况是Unwrap返回值是[]error的时候，比如fmt.Errorf语句中有多个%w时，Unwrap对该语句的返回值作用后也是返回nil

Unwrap method returns []error ，这个是Go 1.20才增加的吧。