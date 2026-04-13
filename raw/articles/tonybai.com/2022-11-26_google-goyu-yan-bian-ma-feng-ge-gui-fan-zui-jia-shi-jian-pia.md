---
title: Google Go语言编码风格规范：最佳实践篇
url: https://tonybai.com/google-go-style/google-go-style-best-practices/
published: '2022-11-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Google Go语言编码风格规范：最佳实践篇

![](../../assets/9e6134bbc036be7b.png)


[本文永久链接](https://tonybai.com/google-go-style/google-go-style-best-practices) – https://tonybai.com/google-go-style/google-go-style-best-practices

本页面是2022年11月中旬Google发布的[Go语言编码风格规范](https://google.github.io/styleguide/go/index)系列文档的[最佳指南篇](https://google.github.io/styleguide/go/best-practices)的中译版。

注意：这是介绍[Google Go编码风格的系列文档](https://tonybai.com/google-go-style)的一部分。本文档既不是规范性的，也不是权威性的。本文档是[指南篇](https://tonybai.com/google-go-style/google-go-style-guide)的辅助文档，更多信息请参见[概述篇](https://tonybai.com/google-go-style)。

## 关于

本文档将对如何最好地应用Go风格指南给出指导建议。这些指导建议旨在解决经常出现的常见问题情况，但不一定适用于所有情况。在可能的情况下，我们讨论了多种替代方法，以及决定何时和何时不应用这些方法的考虑因素。

更多内容，请参阅本系列文档的[概述篇](https://tonybai.com/google-go-style)。

## 命名

### 函数和方法名

#### 避免重复

当选择一个函数或方法的名字时，需要考虑该名字将被使用的上下文环境。请考虑以下建议，以避免在调用时出现过多的[重复](https://google.github.io/styleguide/go/decisions#repetition)：

-
以下内容一般可以从函数和方法的名字中省略。

- 输入和输出的类型（当不存在冲突的时候）
- 方法的接收器的类型
- 输入或输出是否是一个指针

-
对于函数，

[不要重复包的名称](https://google.github.io/styleguide/go/decisions#repetitive-with-package)。

```
// Bad:
package yamlconfig
func ParseYAMLConfig(input string) (*Config, error)
```


```
// Good:
package yamlconfig
func Parse(input string) (*Config, error)
```


- 对于方法，不要重复方法接收器的名称。

```
// Bad:
func (c *Config) WriteConfigTo(w io.Writer) (int64, error)
```


```
// Good:
func (c *Config) WriteTo(w io.Writer) (int64, error)
```


- 不要重复作为参数传递的变量的名称。

```
// Bad:
func OverrideFirstWithSecond(dest, source *Config) error
```


```
// Good:
func Override(dest, source *Config) error
```


- 不要重复返回值的名称和类型。

```
// Bad:
func TransformYAMLToJSON(input *Config) *jsonconfig.Config
```


```
// Good:
func Transform(input *Config) *jsonconfig.Config
```


当有必要区分相似名称的函数时，名字中可以包含额外的信息：

```
// Good:
func (c *Config) WriteTextTo(w io.Writer) (int64, error)
func (c *Config) WriteBinaryTo(w io.Writer) (int64, error)
```


#### 命名惯例

在为函数和方法选择名称时，还有一些常见的惯例。

- 返回某事物的函数通常被赋予类似名词的名字。

```
// Good:
func (c *Config) JobName(key string) (value string, ok bool)
```


这方面的一个推论是，函数和方法名称应该避免使用Get前缀。

```
// Bad:
func (c *Config) GetJobName(key string) (value string, ok bool)
```


- 做某事的函数被赋予类似动词的名称。

```
// Good:
func (c *Config) WriteDetail(w io.Writer) (int64, error)
```


- 只因所涉及的类型而不同的相同的函数在名称的末尾包括类型的名称。

```
// Good:
func ParseInt(input string) (int, error)
func ParseInt64(input string) (int64, error)
func AppendInt(buf []byte, value int) []byte
func AppendInt64(buf []byte, value int64) []byte
```


如果有一个明确的 “主要 “版本，该版本的名称中可以省略类型。

```
// Good:
func (c *Config) Marshal() ([]byte, error)
func (c *Config) MarshalText() (string, error)
```


### 测试替身包和类型

在命名提供测试助手，特别是[测试替身](https://en.wikipedia.org/wiki/Test_double)的包和类型时，有几条条款可以运用。测试替身可以是一个stub、fake、mock或spy。

这些例子大多使用stub这种测试替身。如果你的代码使用fake的或其他类型的测试替身，请相应地更新你的名字。

假设你有一个重点突出的包，提供类似这样的生产代码：

```
package creditcard
import (
"errors"
"path/to/money"
)
// ErrDeclined indicates that the issuer declines the charge.
var ErrDeclined = errors.New("creditcard: declined")
// Card contains information about a credit card, such as its issuer,
// expiration, and limit.
type Card struct {
// omitted
}
// Service allows you to perform operations with credit cards against external
// payment processor vendors like charge, authorize, reimburse, and subscribe.
type Service struct {
// omitted
}
func (s *Service) Charge(c *Card, amount money.Money) error { /* omitted */ }
```


#### 创建测试助手包

假设你想创建一个包，其中包含另一个包的测试替身。在这个例子中，我们将使用package creditcard（来自上面）。

一种方法是在生产包的基础上引入一个新的Go包进行测试。一个安全的选择是在原始包的名字后面加上test这个词（”creditcard “+”test”）。

```
// Good:
package creditcardtest
```


除非另有明确说明，以下各节中的所有例子都是在creditcardtest包中。

#### 简单情况

你想为Service添加一组测试替身。因为Card是一个有效的哑数据类型，类似于Protocol Buffer消息，它在测试中不需要特殊处理，所以不需要测试替身。如果你预计只对一种类型（如Service）使用测试替身，你可以采取一种简洁的方法来命名替身。

```
// Good:
import (
"path/to/creditcard"
"path/to/money"
)
// Stub stubs creditcard.Service and provides no behavior of its own.
type Stub struct{}
func (Stub) Charge(*creditcard.Card, money.Money) error { return nil }
```


严格来说，这比像StubService或非常差的StubCreditCardService这样的名字要好，因为基础包的名字和它的领域类型使得creditcardtest.Stub是什么变得显而易见。

最后，如果该包是用Bazel构建的，确保该包的新go_library规则被标记为testonly。

```
# Good:
go_library(
name = "creditcardtest",
srcs = ["creditcardtest.go"],
deps = [
":creditcard",
":money",
],
testonly = True,
)
```


上述方法是符合惯例的，很容易被其他工程师所理解。

请参阅：

- [Go tips#42：为测试编写stub](https://google.github.io/styleguide/go/index.html#gotip)

#### 多种测试替身行为

当一种stub不够用时（例如，你还需要一种总是失败的stub），我们建议根据它们模拟的行为来命名stub。这里我们将Stub重命名为AlwaysCharges，并引入一个新的stub，称为AlwaysDeclines。

```
// Good:
// AlwaysCharges stubs creditcard.Service and simulates success.
type AlwaysCharges struct{}
func (AlwaysCharges) Charge(*creditcard.Card, money.Money) error { return nil }
// AlwaysDeclines stubs creditcard.Service and simulates declined charges.
type AlwaysDeclines struct{}
func (AlwaysDeclines) Charge(*creditcard.Card, money.Money) error {
return creditcard.ErrDeclined
}
```


#### 针对多个类型的多个测试替身

但是现在，假设包creditcard包含多种值得创建测试替身的类型，正如下面看到的Service和StoredValue。

```
package creditcard
type Service struct {
// omitted
}
type Card struct {
// omitted
}
// StoredValue manages customer credit balances. This applies when returned
// merchandise is credited to a customer's local account instead of processed
// by the credit issuer. For this reason, it is implemented as a separate
// service.
type StoredValue struct {
// omitted
}
func (s *StoredValue) Credit(c *Card, amount money.Money) error { /* omitted */ }
```


在这种情况下，我们应该使用更明确的测试替身命名。

```
// Good:
type StubService struct{}
func (StubService) Charge(*creditcard.Card, money.Money) error { return nil }
type StubStoredValue struct{}
func (StubStoredValue) Credit(*creditcard.Card, money.Money) error { return nil }
```


#### 测试中的局部变量

当你的测试中的变量引用测试替身时，要根据上下文选择一个能最清楚地区分替身和其他生产类型的名称。考虑一下你要测试的一些生产代码。

```
package payment
import (
"path/to/creditcard"
"path/to/money"
)
type CreditCard interface {
Charge(*creditcard.Card, money.Money) error
}
type Processor struct {
CC CreditCard
}
var ErrBadInstrument = errors.New("payment: instrument is invalid or expired")
func (p *Processor) Process(c *creditcard.Card, amount money.Money) error {
if c.Expired() {
return ErrBadInstrument
}
return p.CC.Charge(c, amount)
}
```


在测试中，一个被称为CreditCard的”spy”的测试替身与生产类型并列，所以给这个名字加上前缀可以提高清晰度。

```
// Good:
package payment
import "path/to/creditcardtest"
func TestProcessor(t *testing.T) {
var spyCC creditcardtest.Spy
proc := &Processor{CC: spyCC}
// declarations omitted: card and amount
if err := proc.Process(card, amount); err != nil {
t.Errorf("proc.Process(card, amount) = %v, want %v", got, want)
}
charges := []creditcardtest.Charge{
{Card: card, Amount: amount},
}
if got, want := spyCC.Charges, charges; !cmp.Equal(got, want) {
t.Errorf("spyCC.Charges = %v, want %v", got, want)
}
}
```


这比没有前缀的名称更清楚。

```
// Bad:
package payment
import "path/to/creditcardtest"
func TestProcessor(t *testing.T) {
var cc creditcardtest.Spy
proc := &Processor{CC: cc}
// declarations omitted: card and amount
if err := proc.Process(card, amount); err != nil {
t.Errorf("proc.Process(card, amount) = %v, want %v", got, want)
}
charges := []creditcardtest.Charge{
{Card: card, Amount: amount},
}
if got, want := cc.Charges, charges; !cmp.Equal(got, want) {
t.Errorf("cc.Charges = %v, want %v", got, want)
}
}
```


### 遮蔽(shadowing)

注意：本解释使用了两个非正式的术语，重踏(stomping)和遮蔽。它们并不是Go语言规范中的正式概念。

像许多编程语言一样，Go有可变的变量：向一个变量赋值会改变其值。

```
// Good:
func abs(i int) int {
if i < 0 {
i *= -1
}
return i
}
```


当使用带有:=操作符的短变量声明时，在某些情况下不会创建一个新的变量。我们可以把这称为**重踏**。当不再需要原来的值时，这样做是可以的。

```
// Good:
// innerHandler is a helper for some request handler, which itself issues
// requests to other backends.
func (s *Server) innerHandler(ctx context.Context, req *pb.MyRequest) *pb.MyResponse {
// Unconditionally cap the deadline for this part of request handling.
ctx, cancel := context.WithTimeout(ctx, 3*time.Second)
defer cancel()
ctxlog.Info("Capped deadline in inner request")
// Code here no longer has access to the original context.
// This is good style if when first writing this, you anticipate
// that even as the code grows, no operation legitimately should
// use the (possibly unbounded) original context that the caller provided.
// ...
}
```


不过要小心在新的作用域中使用短的变量声明：这将引入一个新的变量。我们可以把这称为**对原始变量的遮蔽**。代码块结束后，代码中的变量将指向原来的变量。下面是一个有条件地缩短deadline的错误尝试。

```
// Bad:
func (s *Server) innerHandler(ctx context.Context, req *pb.MyRequest) *pb.MyResponse {
// Attempt to conditionally cap the deadline.
if *shortenDeadlines {
ctx, cancel := context.WithTimeout(ctx, 3*time.Second)
defer cancel()
ctxlog.Info(ctx, "Capped deadline in inner request")
}
// BUG: "ctx" here again means the context that the caller provided.
// The above buggy code compiled because both ctx and cancel
// were used inside the if statement.
// ...
}
```


一个正确版本的代码可能是这样的：

```
// Good:
func (s *Server) innerHandler(ctx context.Context, req *pb.MyRequest) *pb.MyResponse {
if *shortenDeadlines {
var cancel func()
// Note the use of simple assignment, = and not :=.
ctx, cancel = context.WithTimeout(ctx, 3*time.Second)
defer cancel()
ctxlog.Info(ctx, "Capped deadline in inner request")
}
// ...
}
```


在我们称之为**重踏**的情况下，因为没有新的变量，所以被分配的类型必须与原始变量的类型相匹配。而遮蔽则是引入一个全新的实体，所以它可以有不同的类型。有意的遮蔽可以是一种有用的做法，但如果从提高代码清晰度角度考虑，你总是可以使用一个新的名字。

除了非常小的范围之外，使用与标准包同名的变量并不是一个好主意，因为这使得该包的函数和值无法被访问。反过来说，在为你的包挑选名字时，要避免使用那些可能需要重命名导入包的名字，或者在客户端造成对其他好的变量名字的遮蔽。

```
// Bad:
func LongFunction() {
url := "https://example.com/"
// Oops, now we can't use net/url in code below.
}
```


### Util包

Go包在包声明中指定了一个名称，与导入路径分开。包的名称比路径更重要，因为它的可读性。

Go包的名字应该[与包所提供的内容相关](https://google.github.io/styleguide/go/decisions#package-names)。仅仅将一个包命名为util、helper、common或类似的名字通常是一个糟糕的选择（不过可以作为名字的一部分）。没有信息的名字会使代码更难阅读，而且如果使用的范围太广，很可能会造成不必要的[导入冲突](https://google.github.io/styleguide/go/decisions#import-renaming)。

相反，要考虑到调用时会是什么样子。

```
// Good:
db := spannertest.NewDatabaseFromFile(...)
_, err := f.Seek(0, io.SeekStart)
b := elliptic.Marshal(curve, x, y)
```


即使不知道导入列表（cloud.google.com/go/spanner/spannertest、io和crypto/elliptic），你也能大致知道这些包的作用。如果没那么关注命名，这些名字可能是：

```
// Bad:
db := test.NewDatabaseFromFile(...)
_, err := f.Seek(0, common.SeekStart)
b := helper.Marshal(curve, x, y)
```


## 包大小

如果你在问自己，你的Go包应该有多大，是把相关的类型放在同一个包里，还是把它们分成不同的包，那么[关于包名的Go博文](https://go.dev/blog/package-names)就是一个好的开始。尽管帖子的标题是这样的，但它并不只是关于命名的。它包含一些有用的提示，并引用了一些有用的文章和讲座。

下面是一些其他的考量和说明。

用户在一个页面中看到包的godoc，由包提供的类型导出的任何方法都按其类型分组。Godoc还将构造函数与它们返回的类型一起分组。如果客户端代码有可能需要两个不同类型的值来相互作用，那么把它们放在同一个包里可能会给用户带来方便。

包内的代码可以访问包内未导出的标识符。如果你有几个相关的类型，它们的实现是紧密耦合的，把它们放在同一个包里可以让你实现这种耦合，而不用用这些细节污染公共API。

综上所述，把你的整个项目放在一个包里，很可能会使这个包变得太大。当一个东西在概念上是不同的，将它自己放入一个单独的小包中可以使它更容易使用。客户端知道的包的短名称与导出的类型名称一起工作，构成一个有意义的标识符：例如bytes.Buffer，ring.New。[这篇博文](https://go.dev/blog/package-names)中有更多的例子。

在文件大小方面，Go表现得很灵活，因为维护者可以将包内的代码从一个文件移到另一个文件，而不影响调用者。但作为一般准则：通常情况下，一个文件有几千行，或者有许多小文件，都不是一个好主意。Go没有像其他一些语言那样的“一个类型，一个文件”的惯例。作为一个经验法则，文件应该足够内聚，以便维护者可以知道哪个文件包含了什么东西，而且文件应该足够小，以便一旦有了它，就很容易找到。标准库经常将大型包分割成几个源文件，将相关的代码按文件分组。[包byte](https://go.dev/src/bytes/)的源文件就是一个很好的例子。具有较长包文档的包可以选择一个名为doc.go的专门文件来放置[包文档](https://google.github.io/styleguide/go/decisions#package-comments)，该文件中仅有包的文档和包的声明，而没有其他内容，但这并不是必须的。

在Google代码库和使用Bazel的项目中，Go代码的目录布局与开源Go项目不同：你可以在一个目录中拥有多个go_library目标。如果你期望在未来将你的项目开源，那么给每个包提供自己的目录是一个很好的理由。

另见：

- 测试替身包

## 导入

### Protos和Stub

由于其跨语言的特性，Proto库导入的处理方式与标准Go导入不同。重命名proto导入的惯例是基于生成包的规则。

- pb后缀一般用于go_proto_library规则。
- 后缀grpc一般用于go_grpc_library规则。

一般来说，会使用一个或两个字母的短前缀。

```
// Good:
import (
fspb "path/to/package/foo_service_go_proto"
fsgrpc "path/to/package/foo_service_go_grpc"
)
```


如果一个包只使用一个proto，或者该包与该proto紧密相连，那么前缀可以省略。

```
import (
pb "path/to/package/foo_service_go_proto"
grpc "path/to/package/foo_service_go_grpc"
)
```


如果proto中的符号是通用的，或者不是很好的自描述，或者用首字母缩写来缩短包的名称是不明确的，那么一个简短的词就可以作为前缀。

```
// Good:
import (
mapspb "path/to/package/maps_go_proto"
)
```


在这种情况下，如果有关的代码没有明确与maps相关，那么mapspb.Address可能比mpb.Address更清晰。

### 导入顺序

包导入通常分为以下两个（或更多）块，按顺序是。

- 标准库导入（例如，”fmt”）。
- 普通项目导入（例如，”/path/to/somelib”）。
- (可选）Protobuf导入（例如，fpb “path/to/foo_go_proto”）。
- (可选) 副作用导入（例如，_ “path/to/package”）。

如果一个文件没有上述可选的导入类别，相关的导入就会被包含在项目导入组中。

任何清晰易懂的导入分组一般都是可以的。例如，一个团队可以选择将gRPC导入与protobuf导入分开分组。

```
注意: 对于只维护两个强制组的代码 (一个用于标准库， 一个用于所有其他导入的组)， goimports工具产生的输出与这个指南一致。
然而， goimports并不了解强制性组以外的组； 可选的组很容易被这个工具所忽略。当使用可选的组别时，代码作者和审查人都需要注意，以确保组别的一致性。
两种方法都可以，但不要让import部分处于不一致的、部分分组的状态。
```


## 错误处理

在Go中，[错误是值](https://go.dev/blog/errors-are-values)；它们由代码产生，也由代码消费。错误可以：

- 转化为诊断信息，显示给人类
- 由维护者使用
- 由终端用户解释

错误信息也显示在各种不同的表面上，包括日志信息、错误转储和渲染的UI。

处理（产生或消耗）错误的代码应该小心翼翼。忽略或盲目地传播错误的返回值可能是很诱人的。然而，我们总是应该考虑的是，函数调用栈中的当前函数是否是最适合处理该错误的那一个。这是一个很大的话题，很难给出明确的建议。使用你的判断，但要记住以下的考量。

虽然忽略一个错误通常是不合适的，但一个合理的例外是当编排相关操作时，通常只有第一个错误是有用的。包errgroup为一组操作提供了一个方便的抽象，这些操作都可以作为一个组失败或被取消。

另见：

[Effective Go中关于error的部分](https://go.dev/doc/effective_go#errors)[Go博客关于错误的文章](https://go.dev/blog/go1.13-errors)[package errors](https://pkg.go.dev/errors)[upspin.io/errors](https://commandcenter.blogspot.com/2017/12/error-handling-in-upspin.html)包[GoTip #89: 何时使用规范的状态代码作为错误代码](https://google.github.io/styleguide/go/index.html#gotip)[GoTip #48：哨兵错误值](https://google.github.io/styleguide/go/index.html#gotip)[GoTip #13: 设计用于检查的错误](https://google.github.io/styleguide/go/index.html#gotip)

### 错误结构

如果调用者需要查询错误（例如，区分不同的错误条件），那么给出错误值结构，这样就可以通过编程完成查询，而不是让调用者进行字符串匹配。这个建议适用于生产代码，也适用于关心不同错误条件的测试代码。

最简单的结构化的错误是无参数的全局值。

```
type Animal string
var (
// ErrDuplicate occurs if this animal has already been seen.
ErrDuplicate = errors.New("duplicate")
// ErrMarsupial occurs because we're allergic to marsupials outside Australia.
// Sorry.
ErrMarsupial = errors.New("marsupials are not supported")
)
func pet(animal Animal) error {
switch {
case seen[animal]:
return ErrDuplicate
case marsupial(animal):
return ErrMarsupial
}
seen[animal] = true
// ...
return nil
}
```


调用者可以简单地将函数返回的错误值与已知的错误值之一进行比较。

```
// Good:
func handlePet(...) {
switch err := process(an); err {
case ErrDuplicate:
return fmt.Errorf("feed %q: %v", an, err)
case ErrMarsupial:
// Try to recover with a friend instead.
alternate = an.BackupAnimal()
return handlePet(..., alternate, ...)
}
}
```


上面使用了哨兵值，错误必须等于（在==的意义上）预期值。这在许多情况下是完全足够的。如果process函数返回包装后的错误值（在下面讨论），你可以使用errors.Is。

```
// Good:
func handlePet(...) {
switch err := process(an); {
case errors.Is(err, ErrDuplicate):
return fmt.Errorf("feed %q: %v", an, err)
case errors.Is(err, ErrMarsupial):
// ...
}
}
```


不要试图根据字符串的形式来区分错误。(参见[Go Tip #13：为检查而设计错误](https://google.github.io/styleguide/go/index.html#gotip)）。

```
// Bad:
func handlePet(...) {
err := process(an)
if regexp.MatchString(`duplicate`, err.Error()) {...}
if regexp.MatchString(`marsupial`, err.Error()) {...}
}
```


如果在错误中存在调用者需要的额外信息，最好是以结构化方式呈现。例如，os.PathError类型将失败操作的路径名放在调用者可以轻松访问的结构体字段中。

其他的错误结构可以酌情使用，例如一个包含错误代码和细节字符串的项目结构体。[status包](https://pkg.go.dev/google.golang.org/grpc/status)是一种常见的封装方式；如果你选择这种方式（你没有义务这样做），请使用[codes](https://pkg.go.dev/google.golang.org/grpc/codes)。参见[Go Tip #89。何时使用规范的状态代码作为错误](https://google.github.io/styleguide/go/index.html#gotip)，以了解使用状态代码是否是正确的选择。

### 给错误添加信息

任何返回错误的函数都应该努力使错误值变得有用。通常情况下，该函数处于一个调用链的中间，并且只是在传播它所调用的其他函数的错误（甚至可能来自另一个包）。这里有机会用额外的信息来注解错误，但程序员应该确保错误中有足够的信息，而不添加重复的或不相关的细节。如果你不确定，可以尝试在开发过程中触发错误条件：这是一个很好的方法来评估错误的观察者（无论是人类还是代码）最终会得到什么。

符合惯例的良好的文档是有帮助的。例如，标准包os宣传其错误包含路径信息，当它可用时。这是一种有用的风格，因为得到错误的调用者不需要用他们已经提供了失败的函数的信息来注释它。

```
// Good:
if err := os.Open("settings.txt"); err != nil {
return err
}
// Output:
//
// open settings.txt: no such file or directory
```


如果对错误的含义有什么有趣的说法，当然可以加入。只要考虑调用链的哪一层最适合理解这个含义。

```
// Good:
if err := os.Open("settings.txt"); err != nil {
// We convey the significance of this error to us. Note that the current
// function might perform more than one file operation that can fail, so
// these annotations can also serve to disambiguate to the caller what went
// wrong.
return fmt.Errorf("launch codes unavailable: %v", err)
}
// Output:
//
// launch codes unavailable: open settings.txt: no such file or directory
```


与这里的冗余信息形成鲜明对比:

```
// Bad:
if err := os.Open("settings.txt"); err != nil {
return fmt.Errorf("could not open settings.txt: %w", err)
}
// Output:
//
// could not open settings.txt: open settings.txt: no such file or directory
```


当向一个传播的错误添加信息时，你可以包装该错误或提出一个新的错误。用fmt.Errorf中的%w动词包装错误，允许调用者访问原始错误中的数据。这在某些时候是非常有用的，但在其他情况下，这些细节对调用者来说是误导或不感兴趣的。更多信息请参见[关于错误包装的博文](https://blog.golang.org/go1.13-errors)。包装错误也会以一种不明显的方式扩展你的包的API界面，如果你改变了你的包的实现细节，这可能会导致破坏。

最好避免使用%w，除非你也记录（并有测试来验证）你所暴露的底层错误。如果你不希望你的调用者调用 errors.Unwrap, errors.Is 等等，就不要使用%w。

同样的概念适用于像*status.Status这样的[结构化错误](https://google.github.io/styleguide/go/best-practices#error-structure)（见codes）。例如，如果你的服务器向后端发送不合法的请求，并收到一个InvalidArgument错误码，这个错误码不应该被传播到客户端，假设客户端没有做错。相反，向客户端返回一个内部的规范的code。

然而，注解错误有助于自动日志系统保留错误的状态有效载荷。例如，在一个内部函数中注释错误是合适的。

```
// Good:
func (s *Server) internalFunction(ctx context.Context) error {
// ...
if err != nil {
return fmt.Errorf("couldn't find remote file: %w", err)
}
}
```


直接位于系统边界的代码（通常是RPC、IPC、存储和类似的）应该使用规范的错误空间报告错误。这里的代码有责任处理特定领域的错误，并以规范的方式表示它们。比如说。

```
// Bad:
func (*FortuneTeller) SuggestFortune(context.Context, *pb.SuggestionRequest) (*pb.SuggestionResponse, error) {
// ...
if err != nil {
return nil, fmt.Errorf("couldn't find remote file: %w", err)
}
}
```


```
// Good:
import (
"google.golang.org/grpc/codes"
"google.golang.org/grpc/status"
)
func (*FortuneTeller) SuggestFortune(context.Context, *pb.SuggestionRequest) (*pb.SuggestionResponse, error) {
// ...
if err != nil {
// Or use fmt.Errorf with the %w verb if deliberately wrapping an
// error which the caller is meant to unwrap.
return nil, status.Errorf(codes.Internal, "couldn't find fortune database", status.ErrInternal)
}
}
```


### 在错误中放置%w

倾向于将%w放在错误字符串的末尾。

错误可以用%w动词来包装，或者把它们放在一个实现了Unwrap() error的结构化错误中（例如：fs.PathError）。

被包装的错误形成错误链：每一层新的包装都会在错误链的前面增加一个新的条目。错误链可以用Unwrap() error进行遍历。比如说。

```
err1 := fmt.Errorf("err1")
err2 := fmt.Errorf("err2: %w", err1)
err3 := fmt.Errorf("err3: %w", err2)
```


这就形成了一个错误链的形式。

```
flowchart LR
err3 == err3 wraps err2 ==> err2;
err2 == err2 wraps err1 ==> err1;
```


无论%w动词放在哪里，返回的错误总是代表错误链的前面，而%w是下一个子节点。类似地，Unwrap() error 总是从最新的错误到最旧的错误来遍历错误链。

然而，%w动词的位置会影响错误链是从最新到最旧，从最旧到最新，还是两者都不影响。

```
// Good:
err1 := fmt.Errorf("err1")
err2 := fmt.Errorf("err2: %w", err1)
err3 := fmt.Errorf("err3: %w", err2)
fmt.Println(err3) // err3: err2: err1
// err3 is a newest-to-oldest error chain, that prints newest-to-oldest.
```


```
// Bad:
err1 := fmt.Errorf("err1")
err2 := fmt.Errorf("%w: err2", err1)
err3 := fmt.Errorf("%w: err3", err2)
fmt.Println(err3) // err1: err2: err3
// err3 is a newest-to-oldest error chain, that prints oldest-to-newest.
```


```
// Bad:
err1 := fmt.Errorf("err1")
err2 := fmt.Errorf("err2-1 %w err2-2", err1)
err3 := fmt.Errorf("err3-1 %w err3-2", err2)
fmt.Println(err3) // err3-1 err2-1 err1 err2-2 err3-2
// err3 is a newest-to-oldest error chain, that neither prints newest-to-oldest
// nor oldest-to-newest.
```


因此，为了使错误文本反映错误链结构，最好将%w动词放在最后，形式为[...]：%w。

### 日志中输出错误

函数有时需要告诉外部系统一个错误，而不是把它传播给其调用者。在这里，日志是一个明显的选择；但要注意记录错误的内容和方式。

- 就像好的测试失败信息一样，日志信息应该清楚地表达出错的原因，并通过包括相关信息来帮助维护者诊断问题。
- 避免重复。如果你返回一个错误，通常最好不要自己记录，而是让调用者处理。调用者可以选择记录错误，也可以用
[rate.Sometimes](https://pkg.go.dev/golang.org/x/time/rate#Sometimes)限制记录的速度。其他选择包括尝试恢复，甚至停止程序。在任何情况下，让调用者控制有助于避免记录“垃圾”日志。

然而，这种方法的缺点是，任何日志都是用调用者的行号记录的。

- 对
[PII](https://en.wikipedia.org/wiki/Personal_data)要小心。许多日志输出地并不是敏感的终端用户信息的合适目的地。 -
尽量少使用log.Error。ERROR级别的日志会导致刷新，并且比较低的日志级别更昂贵。这可能会对你的代码产生严重的性能影响。当决定错误和警告级别时，考虑最佳实践，即错误级别的信息应该是可操作的，而不是比警告”更严重”。

-
在谷歌内部，我们有监控系统，可以设置更有效的警报，而不是写到日志文件，希望有人注意到它。这与标准库包

[expvar](https://pkg.go.dev/expvar)类似，但不完全相同。

#### 自定义日志级别

使用冗长的日志（log.V）对你有利。冗长的日志对于开发和追踪是很有用的。建立一个围绕着log级别的约定是有帮助的。比如说。

- 在V(1)写少量的额外信息
- 在V(2)中追踪更多信息
- 在V(3)中输出大量的内部状态

为了最大限度地减少冗长日志的成本，你应该确保即使在log.V关闭的情况下也不要意外地调用昂贵的函数。log.V提供了两个API。更方便的那个带有这种意外开销的风险。当有疑问时，请使用稍显冗长的风格。

```
// Good:
for _, sql := range queries {
log.V(1).Infof("Handling %v", sql)
if log.V(2) {
log.Infof("Handling %v", sql.Explain())
}
sql.Run(...)
}
```


```
// Bad:
// sql.Explain called even when this log is not printed.
log.V(2).Infof("Handling %v", sql.Explain())
```


### 程序初始化

程序初始化错误（如错误的标志和配置）应该向上传播到main，main应该调用log.Exit，并解释如何修复错误。在这些情况下，一般不应使用log.Fatal，因为指向检查的堆栈跟踪不可能像人为生成的、可操作的消息那样有用。

### 程序检查和panic

正如在[反对panic的决定](https://google.github.io/styleguide/go/decisions#dont-panic)中所说，标准错误处理应该围绕错误返回值进行结构化。库应该倾向于向调用者返回错误，而不是中止程序，特别是对于暂时错误。

偶尔有必要对一个不变量进行一致性检查，如果违反了这个不变量，就终止程序。一般来说，只有当不变量检查失败意味着内部状态已经无法恢复时，才会这样做。在谷歌代码库中，最可靠的方法是调用log.Fatal。在这些情况下使用panic是不可靠的，因为defer函数有可能会出现死锁或进一步破坏内部或外部状态。

同样地，要抵制恢复panic以避免崩溃的诱惑，因为这样做可能会导致传播损坏的状态。你离panic越远，你对程序的状态就越不了解，它可能持有锁或其他资源。然后，程序可以发展出其他意想不到的故障模式，使问题更加难以诊断。与其试图在代码中处理意外的panic，不如使用监控工具来浮现出意外的故障，并以高优先级修复相关的错误。

注意：标准的net/http服务器违反了这个建议，从请求处理程序中恢复panic。有经验的Go工程师们的共识是，这是一个历史性的错误。如果你对其他语言的应用服务器的日志进行取样，通常会发现有大量的堆栈轨迹没有被处理。在你的服务器中避免这种陷阱。

### 何时用panic

标准库对API的误用会报panic。例如，在许多情况下，如果一个值的访问方式表明它被误解了，reflect就会报panic。这类似于对核心语言错误的panic，如访问一个超出边界的切片元素。代码审查和测试应该发现这样的错误，这些错误预计不会出现在生产代码中。这些panic作为不依赖库的不变性检查，因为标准库不能访问谷歌代码库使用的[分级日志包](https://google.github.io/styleguide/go/decisions#logging)。

另一种情况是，虽然不常见，但panics可以作为一个包的内部实现细节，在调用链中始终有一个匹配的recover。解析器和类似的深度嵌套、紧密耦合的内部函数组可以从这种设计中受益，若使用管道错误返回会增加复杂性而且没有价值。这种设计的关键属性是，这些panic永远不允许跨越包的边界，不构成包的API的一部分。这通常是通过一个顶层的deferred recover来实现的，它将传播的panic转化为公共API表面的返回错误。

当编译器无法识别不可到达的代码时，例如使用像log.Fatal这样不会返回的函数时，也会使用Panic。

```
// Good:
func answer(i int) string {
switch i {
case 42:
return "yup"
case 54:
return "base 13, huh"
default:
log.Fatalf("Sorry, %d is not the answer.", i)
panic("unreachable")
}
}
```


[在命令行标志被解析之前，不要调用日志函数](https://pkg.go.dev/github.com/golang/glog#pkg-overview)。如果你必须在init func中退出程序，可以用panic来代替日志调用。

## 文档

### 惯例

这一部分是对[决定文档](https://tonybai.com/google-go-style/google-go-style-decisions)的注释部分的补充。

以熟悉的风格记录的Go代码比那些错误记录或根本没有记录的代码更容易阅读，更不容易被误用。可运行的例子显示在Godoc和代码搜索中，这是解释如何使用你的代码的绝佳方式。

#### 参数和配置

不是每个参数都必须在文档中列举出来。这适用于

- 函数和方法参数
- 结构体字段
- 选项(option)的API

将易出错或不明显的字段和参数记录下来，说说它们为什么有趣。

在下面的片段中，突出显示的注释对读者来说没有增加什么有用的信息。

```
// Bad:
// Sprintf formats according to a format specifier and returns the resulting
// string.
//
// format is the format, and data is the interpolation data.
func Sprintf(format string, data ...interface{}) string
```


然而，这个片段展示了一个与之前类似的代码场景，其中的注释反而说明了一些非显而易见或对读者有实质性帮助的东西。

```
// Good:
// Sprintf formats according to a format specifier and returns the resulting
// string.
//
// The provided data is used to interpolate the format string. If the data does
// not match the expected format verbs or the amount of data does not satisfy
// the format specification, the function will inline warnings about formatting
// errors into the output string as described by the Format errors section
// above.
func Sprintf(format string, data ...interface{}) string
```


在选择文档的内容和深度时，要考虑到你可能的受众。维护者、新加入团队的人、外部用户，甚至是六个月后的你，可能会感激这些与你第一次来写文档时的想法略有不同的信息。

也请参见：

– [GoTip #41: 识别函数调用参数](https://google.github.io/styleguide/go/index.html#gotip)

– [GoTip #51: 配置的模式](https://google.github.io/styleguide/go/index.html#gotip)

#### Context

这意味着一个上下文参数的取消操作会中断提供给它的函数。如果该函数可以返回一个错误，惯例上是ctx.Err()。

这个事实不需要重述。

```
// Bad:
// Run executes the worker's run loop.
//
// The method will process work until the context is cancelled and accordingly
// returns an error.
func (Worker) Run(ctx context.Context) error
```


因为这句话是隐含的，所以下面的说法更好。

```
// Good:
// Run executes the worker's run loop.
func (Worker) Run(ctx context.Context) error
```


如果上下文行为是不同的或不明显的，应该明确地记录下来。

- 如果函数在取消上下文时返回ctx.Err()以外的错误。

```
// Good:
// Run executes the worker's run loop.
//
// If the context is cancelled, Run returns a nil error.
func (Worker) Run(ctx context.Context) error
```


- 如果该函数有其他机制，可能会中断它或影响寿命。

```
// Good:
// Run executes the worker's run loop.
//
// Run processes work until the context is cancelled or Stop is called.
// Context cancellation is handled asynchronously internally: run may return
// before all work has stopped. The Stop method is synchronous and waits
// until all operations from the run loop finish. Use Stop for graceful
// shutdown.
func (Worker) Run(ctx context.Context) error
func (Worker) Stop()
```


- 如果该函数对上下文的寿命、脉络或附加值有特殊期望。

```
// Good:
// NewReceiver starts receiving messages sent to the specified queue.
// The context should not have a deadline.
func NewReceiver(ctx context.Context) *Receiver
// Principal returns a human-readable name of the party who made the call.
// The context must have a value attached to it from security.NewContext.
func Principal(ctx context.Context) (name string, ok bool)
```


警告：避免设计对调用者提出这种要求（比如上下文没有截止日期）的API。以上只是一个例子，说明在无法避免的情况下该如何记录，而不是对该模式的认可。

#### 并发

Go用户认为概念上的只读操作对于并发使用是安全的，不需要额外的同步。

在这个Godoc中，关于并发性的额外说明可以安全地删除。

```
// Len returns the number of bytes of the unread portion of the buffer;
// b.Len() == len(b.Bytes()).
//
// It is safe to be called concurrently by multiple goroutines.
func (*Buffer) Len() int
```


然而，修改操作并不被认为对并发使用是安全的，需要用户考虑同步化。

同样地，这里可以安全地删除关于并发的额外注释。

```
// Grow grows the buffer's capacity.
//
// It is not safe to be called concurrently by multiple goroutines.
func (*Buffer) Grow(n int)
```


强烈鼓励在以下情况下提供文档：

- 目前还不清楚该操作是只读的还是包含修改的。

```
// Good:
package lrucache
// Lookup returns the data associated with the key from the cache.
//
// This operation is not safe for concurrent use.
func (*Cache) Lookup(key string) (data []byte, ok bool)
```


为什么？在查找key的时候，缓存命中会在内部改变一个LRU缓存。这一点是如何实现的，对所有读者来说可能并不明显。

- 同步是由API提供的

```
// Good:
package fortune_go_proto
// NewFortuneTellerClient returns an *rpc.Client for the FortuneTeller service.
// It is safe for simultaneous use by multiple goroutines.
func NewFortuneTellerClient(cc *rpc.ClientConn) *FortuneTellerClient
```


为什么？Stubby提供了同步特性。

注意：如果API是一个类型，并且API完整地提供了同步性，惯例上只有类型定义记录了语义。

- 该API消费用户实现的接口类型，并且该接口的消费者有特殊的并发性要求。

```
// Good:
package health
// A Watcher reports the health of some entity (usually a backen service).
//
// Watcher methods are safe for simultaneous use by multiple goroutines.
type Watcher interface {
// Watch sends true on the passed-in channel when the Watcher's
// status has changed.
Watch(changed chan<- bool) (unwatch func())
// Health returns nil if the entity being watched is healthy, or a
// non-nil error explaining why the entity is not healthy.
Health() error
}
```


为什么？一个API是否能被多个goroutines安全使用是其契约的一部分。

#### 清理

记录API的任何明确的清理要求。否则，调用者不会正确使用API，会导致资源泄漏和其他可能的错误。

调出由调用者决定的清理工作。

```
// Good:
// NewTicker returns a new Ticker containing a channel that will send the
// current time on the channel after each tick.
//
// Call Stop to release the Ticker's associated resources when done.
func NewTicker(d Duration) *Ticker
func (*Ticker) Stop()
```


如果有可能不清楚如何清理资源，请解释如何清理。

```
// Good:
// Get issues a GET to the specified URL.
//
// When err is nil, resp always contains a non-nil resp.Body.
// Caller should close resp.Body when done reading from it.
//
// resp, err := http.Get("http://example.com/")
// if err != nil {
// // handle error
// }
// defer resp.Body.Close()
// body, err := io.ReadAll(resp.Body)
func (c *Client) Get(url string) (resp *Response, err error)
```


### 预览

Go的特点是有一个文档服务器。建议在代码审查前和审查过程中都要预览你的代码产生的文档。这有助于验证godoc的格式是否会正确呈现。

### Godoc格式化

Godoc提供了一些特定的语法来格式化文档。

- 段落之间需要有一个空行。

```
// Good:
// LoadConfig reads a configuration out of the named file.
//
// See some/shortlink for config file format details.
```


- 测试文件可以包含
[可运行的例子](https://google.github.io/styleguide/go/decisions#examples)，这些例子会出现在godoc中相应的文档后面。

```
// Good:
func ExampleConfig_WriteTo() {
cfg := &Config{
Name: "example",
}
if err := cfg.WriteTo(os.Stdout); err != nil {
log.Exitf("Failed to write config: %s", err)
}
// Output:
// {
// "name": "example"
// }
}
```


- 缩进行加上两个空格，就可以将它们逐字排开。

```
// Good:
// Update runs the function in an atomic transaction.
//
// This is typically used with an anonymous TransactionFunc:
//
// if err := db.Update(func(state *State) { state.Foo = bar }); err != nil {
// //...
// }
```


然而，请注意，把代码放在可运行的例子中，而不是把它放在注释中，往往会更合适。

这种逐字格式化可以用于非godoc原生的格式化，如列表和表格。

```
// Good:
// LoadConfig reads a configuration out of the named file.
//
// LoadConfig treats the following keys in special ways:
// "import" will make this configuration inherit from the named file.
// "env" if present will be populated with the system environment.
```


- 一行以大写字母开始，除括号和逗号外不含标点符号，后面是另一个段落，这样的行将被格式化为标题。

```
// Good:
// The following line is formatted as a heading.
//
// Using headings
//
// Headings come with autogenerated anchor tags for easy linking.
```


### 信号增强

有时，一行代码看起来很普通很常见，但实际上不是。这方面最好的例子之一是err == nil检查（因为err != nil更常见）。下面的两个条件检查很难区分。

```
// Good:
if err := doSomething(); err != nil {
// ...
}
```


```
// Bad:
if err := doSomething(); err == nil {
// ...
}
```


你可以通过添加注释来“增强信号”：

```
// Good:
if err := doSomething(); err == nil { // if NO error
// ...
}
```


该只是提示请注意条件的不同。

## 变量声明

### 初始化

为了保持一致性，在用非零值初始化一个新的变量时，首选:=而不是var。

```
// Good:
i := 42
```


```
// Bad:
var i = 42
```


### 非指针零值

下面的声明使用了[零值](https://golang.org/ref/spec#The_zero_value)：

```
// Good:
var (
coords Point
magic [4]byte
primes []int
)
```


当你想表达一个空值，准备以后使用时，你应该使用零值来声明。使用显式初始化的复合字面值可能会很笨重。

```
// Bad:
var (
coords = Point{X: 0, Y: 0}
magic = [4]byte{0, 0, 0, 0}
primes = []int(nil)
)
```


零值声明的一个常见应用是当使用一个变量作为反序列化的输出时：

```
// Good:
var coords Point
if err := json.Unmarshal(data, &coords); err != nil {
```


如果你需要一个锁或其他[不能复制](https://google.github.io/styleguide/go/decisions#copying)的结构体字段时，你可以把它变成一个值类类型，以利用零值初始化的优势。这确实意味着，现在必须通过指针而不是值来传递包含的类型。该类型的方法必须采取指针类型接收器。

```
// Good:
type Counter struct {
// This field does not have to be "*sync.Mutex". However,
// users must now pass *Counter objects between themselves, not Counter.
mu sync.Mutex
data map[string]int64
}
// Note this must be a pointer receiver to prevent copying.
func (c *Counter) IncrementBy(name string, n int64)
```


对复合类型（如结构体和数组）的局部变量使用值类型是可以接受的，即使它们包含这种不可复制的字段。然而，如果复合类型是由函数返回的，或者如果对它的所有访问最终都需要取一个地址，那么最好一开始就把变量声明为指针类型。同样地，protobufs也应该被声明为指针类型。

```
// Good:
func NewCounter(name string) *Counter {
c := new(Counter) // "&Counter{}" is also fine.
registerCounter(name, c)
return c
}
var myMsg = new(pb.Bar) // or "&pb.Bar{}".
```


这是因为*pb.Something实现了proto.Message，而pb.Something没有：

```
// Bad:
func NewCounter(name string) *Counter {
var c Counter
registerCounter(name, &c)
return &c
}
var myMsg = pb.Bar{}
```


重要：map类型在修改之前必须被显式初始化。但是针对零值map变量进行读操作是可以的。

对于map和slice类型，如果代码对性能特别敏感，并且你事先知道尺寸，请看[尺寸提示部分](https://google.github.io/styleguide/go/best-practices#vardeclsize)。

### 复合字面值

下面是一些复合字面值的声明：

```
// Good:
var (
coords = Point{X: x, Y: y}
magic = [4]byte{'I', 'W', 'A', 'D'}
primes = []int{2, 3, 5, 7, 11}
captains = map[string]string{"Kirk": "James Tiberius", "Picard": "Jean-Luc"}
)
```


当你知道初始元素或成员时，你应该使用复合字面值来声明一个值。

相反，与零值初始化相比，使用复合字面值来声明空值或无成员的值在视觉上会有太多噪声。

当你需要一个指向零值的指针时，你有两个选择：空复合字面值和new。两者都很好，但是new关键字可以提醒读者，如果需要一个非零值，复合字面值就不能用。

```
// Good:
var (
buf = new(bytes.Buffer) // non-empty Buffers are initialized with constructors.
msg = new(pb.Message) // non-empty proto messages are initialized with builders or by setting fields one by one.
)
```


### 尺寸提示

以下是利用尺寸提示的声明，以便预先分配容量。

```
// Good:
var (
// Preferred buffer size for target filesystem: st_blksize.
buf = make([]byte, 131072)
// Typically process up to 8-10 elements per run (16 is a safe assumption).
q = make([]Node, 0, 16)
// Each shard processes shardSize (typically 32000+) elements.
seen = make(map[string]bool, shardSize)
)
```


尺寸提示和预分配是重要的步骤，当与代码及其集成的经验分析相结合时，可以创建对性能敏感和资源高效的代码。

大多数代码不需要大小提示或预分配，可以允许运行时根据需要自动扩展切片或map。当最终大小已知时，预分配是可以接受的（例如，在map和切片之间转换时），但这不是可读性的要求，而且在小规模情况下可能不值得这样做。

警告：预先分配比你需要的更多的内存会浪费内存，甚至损害性能。如有疑问，请参阅[GoTip #3: Benchmarking Go Code](https://google.github.io/styleguide/go/index.html#gotip)，默认[零值初始化](https://google.github.io/styleguide/go/best-practices#vardeclzero)或[复合字面值](https://google.github.io/styleguide/go/best-practices#vardeclcomposite)声明。

### channel方向

尽可能指明[channel方向](https://go.dev/ref/spec#Channel_types)。

```
// Good:
// sum computes the sum of all of the values. It reads from the channel until
// the channel is closed.
func sum(values <-chan int) int {
// ...
}
```


这可以防止在没有规范的情况下可能出现的随意编程错误。

```
// Bad:
func sum(values chan int) (out int) {
for v := range values {
out += v
}
// values must already be closed for this code to be reachable, which means
// a second close triggers a panic.
close(values)
}
```


当方向被指定时，编译器会捕捉到像这样的简单错误。它还有助于向类型传达一种所有权的措施。

也请看Bryan Mills的演讲 “重新思考经典的并发模式”：[幻灯片](https://drive.google.com/file/d/1nPdvhB0PutEJzdCq5ms6UI58dp50fcAN/view?usp=sharing)和[视频](https://www.youtube.com/watch?v=5zXAHh5tJqQ)。

## 函数参数列表

不要让一个函数的签名变得太长。当一个函数中的参数越多，单个参数的作用就越不明确，同一类型的相邻参数就越容易混淆。有大量参数的函数不容易被记住，在调用的时候也更难读懂。

在设计API时，可以考虑将一个签名越来越复杂的高可配函数分割成几个更简单的函数。如果有必要，这些函数可以共享一个（未导出的）实现。

当一个函数需要许多输入时，可以考虑为一些参数引入一个[功能选项结构](https://google.github.io/styleguide/go/best-practices#option-structure)，或者采用更高级的[variadic选项技术](https://google.github.io/styleguide/go/best-practices#variadic-options)。选择哪种策略的主要考虑因素应该是函数调用在所有预期的使用情况下看起来如何。

下面的建议主要适用于导出的API，它的标准比未导出的API要高。这些技术对于你的用例可能是不必要的。使用你的判断，并平衡清晰性和最小机制的原则。

也请参见：[Go技巧#24：使用特定案例的结构](https://google.github.io/styleguide/go/index.html#gotip)

### 功能选项结构

功能选项结构是一种结构体类型，它汇集了一个函数或方法的部分或全部参数，然后作为最后一个参数传递给该函数或方法。(只有在导出的函数中使用该结构时，才应该导出该结构)。

使用选项结构有很多好处：

- 结构体字面值包括每个参数的字段和值，这使得它们可以自我记录，并且更难被交换。
- 不相关的或”默认”的字段可以被省略。
- 调用者可以共享选项结构，并编写帮助程序对其进行操作。
- 与函数参数相比，结构体提供了更清晰的每个字段的文档。
- 选项结构可以随着时间的推移而增长，而不会影响到存量的函数调用。

下面是一个可以改进的函数的例子。

```
// Bad:
func EnableReplication(ctx context.Context, config *replicator.Config, primaryRegions, readonlyRegions []string, replicateExisting, overwritePolicies bool, replicationInterval time.Duration, copyWorkers int, healthWatcher health.Watcher) {
// ...
}
```


上面的函数可以用一个选项结构重写如下：

```
// Good:
type ReplicationOptions struct {
Config *replicator.Config
PrimaryRegions []string
ReadonlyRegions []string
ReplicateExisting bool
OverwritePolicies bool
ReplicationInterval time.Duration
CopyWorkers int
HealthWatcher health.Watcher
}
func EnableReplication(ctx context.Context, opts ReplicationOptions) {
// ...
}
```


然后，该函数可以在不同的包中被调用：

```
// Good:
func foo(ctx context.Context) {
// Complex call:
storage.EnableReplication(ctx, storage.ReplicationOptions{
Config: config,
PrimaryRegions: []string{"us-east1", "us-central2", "us-west3"},
ReadonlyRegions: []string{"us-east5", "us-central6"},
OverwritePolicies: true,
ReplicationInterval: 1 * time.Hour,
CopyWorkers: 100,
HealthWatcher: watcher,
})
// Simple call:
storage.EnableReplication(ctx, storage.ReplicationOptions{
Config: config,
PrimaryRegions: []string{"us-east1", "us-central2", "us-west3"},
})
}
```


注意：[选项结构中从不包含上下文](https://google.github.io/styleguide/go/decisions#contexts)。

当以下一些情况适用时，这个选项通常是首选。

- 所有调用者都需要指定一个或多个选项。
- 大量的调用者需要提供许多选项。
- 用户将调用的多个函数之间共享这些选项。

### 不定长选项

使用不定长选项，可以创建导出的函数，其返回的闭包可以传递给函数的不定长选项参数。该函数将选项的值作为其参数（如果有的话），而返回的闭包接受一个可变的引用（通常是一个指向结构体类型的指针），该引用将根据输入进行更新。

使用不定长选项可以提供很多好处：

- 当不需要配置时，在调用函数时选项将不占用空间
- 选项仍然是值，所以调用者可以共享它们，编写帮助程序，并积累它们。
- 选项可以接受多个参数（例如 cartesian.Translate(dx, dy int) TransformOption）。
- 选项函数可以返回一个命名的类型，以便在godoc中把选项组合起来。
- 包可以允许（或阻止）第三方包，定义（或不定义）他们自己的选项。

注意：使用不定长选项需要大量的额外代码（见下面的例子），所以只有在优势大于开销的情况下才可以使用。

下面是一个可以改进的函数的例子：

```
// Bad:
func EnableReplication(ctx context.Context, config *placer.Config, primaryCells, readonlyCells []string, replicateExisting, overwritePolicies bool, replicationInterval time.Duration, copyWorkers int, healthWatcher health.Watcher) {
...
}
```


上面的例子可以用不定长选项改写如下：

```
// Good:
type replicationOptions struct {
readonlyCells []string
replicateExisting bool
overwritePolicies bool
replicationInterval time.Duration
copyWorkers int
healthWatcher health.Watcher
}
// A ReplicationOption configures EnableReplication.
type ReplicationOption func(*replicationOptions)
// ReadonlyCells adds additional cells that should additionally
// contain read-only replicas of the data.
//
// Passing this option multiple times will add additional
// read-only cells.
//
// Default: none
func ReadonlyCells(cells ...string) ReplicationOption {
return func(opts *replicationOptions) {
opts.readonlyCells = append(opts.readonlyCells, cells...)
}
}
// ReplicateExisting controls whether files that already exist in the
// primary cells will be replicated. Otherwise, only newly-added
// files will be candidates for replication.
//
// Passing this option again will overwrite earlier values.
//
// Default: false
func ReplicateExisting(enabled bool) ReplicationOption {
return func(opts *replicationOptions) {
opts.replicateExisting = enabled
}
}
// ... other options ...
// DefaultReplicationOptions control the default values before
// applying options passed to EnableReplication.
var DefaultReplicationOptions = []ReplicationOption{
OverwritePolicies(true),
ReplicationInterval(12 * time.Hour),
CopyWorkers(10),
}
func EnableReplication(ctx context.Context, config *placer.Config, primaryCells []string, opts ...ReplicationOption) {
var options replicationOptions
for _, opt := range DefaultReplicationOptions {
opt(&options)
}
for _, opt := range opts {
opt(&options)
}
}
```


函数可以在不同的包中调用：

```
// Good:
func foo(ctx context.Context) {
// Complex call:
storage.EnableReplication(ctx, config, []string{"po", "is", "ea"},
storage.ReadonlyCells("ix", "gg"),
storage.OverwritePolicies(true),
storage.ReplicationInterval(1*time.Hour),
storage.CopyWorkers(100),
storage.HealthWatcher(watcher),
)
// Simple call:
storage.EnableReplication(ctx, config, []string{"po", "is", "ea"})
}
```


当以下许多情况适用时，最好选择不定长选项：

- 大多数调用者不需要指定任何选项。
- 大多数选项不经常使用。
- 有大量的选项。
- 选项需要参数。
- 选项可能会失败或被错误地设置（在这种情况下，选项函数会返回一个error）。
- 选项需要大量的文档，在一个结构中很难容纳。
- 用户或其他软件包可以提供自定义选项。

这种风格的选项应该接受参数，而不是用存在来表示它们的价值；后者会使参数的动态组成变得更加困难。例如，二进制设置应该接受一个布尔值（例如，rpc.FailFast(enable bool)比rpc.EnableFailFast()更合适。） 枚举的选项应该接受一个枚举的常量（例如，log.Format(log.Capacitor)比log.CapacitorFormat()更合适）。另一种方法使那些必须以编程方式选择传递哪些选项的用户更加困难；这种用户被迫改变参数的实际组成，而不是简单地改变选项的参数。不要假设所有的用户都会静态地知道全部的选项。

一般来说，选项应该被按顺序处理。如果有冲突或者一个非累积的选项被多次传递，以最后一个参数为准。

在这种模式下，选项函数的参数通常是非导出的，以限制选项只在包本身内定义。这是一个很好的默认值，尽管有时允许其他包定义选项也是合适的。

参见Rob Pike的[原始博文](http://commandcenter.blogspot.com/2014/01/self-referential-functions-and-design.html)和[Dave Cheney的演讲](https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis)，以更深入地了解这些选项的使用方法。

## 复杂的命令行交互界面

有些程序希望为用户提供丰富的命令行交互界面，包括子命令。例如，kubectl create、kubectl run以及其他许多子命令都是由程序kubectl提供的。至少有以下常用的库可以实现这一点。

如果你没有偏好或者其他考虑因素相同，推荐使用子命令，因为它最简单，而且容易正确使用。然而，如果你需要它无法提供的不同功能，请挑选其他候选之一。

-
- 命令行标志惯例：getopt
- 在谷歌代码库之外很常见。
- 许多额外的功能。
- usage中的陷阱（见下文）。

-
- 命令行标志约定：Go
- 简单且易于正确使用。
- 如果你不需要额外的功能，推荐使用。


警告：cobra命令函数应该使用cmd.Context()来获取上下文，而不是用context.Background()创建自己的根上下文。使用subcommands包的代码已经将正确的上下文作为一个函数参数来接收。

你不需要把每个子命令放在一个单独的包中，而且通常也没有必要这样做。应用与任何Go代码库相同的关于包边界的考虑。如果你的代码既可以作为库也可以作为二进制文件使用，通常将CLI代码和库分开是有益的，使CLI只是诸多客户端中的一个。(这不是专门针对有子命令的CLI的，但在此提及，因为它是一个常见的地方。）

## 测试

### 把测试留给Test函数

Go区分了”测试助手程序”和”断言助手程序”：

-
测试助手是负责设置或清理任务的函数。所有发生在测试助手中的故障都被认为是环境的故障（而不是被测代码的故障）–例如，当测试数据库无法启动时，因为这台机器上已经没有空闲的端口了。对于这样的函数，调用t.Helper通常是合适的，可以将其

[标记为测试助手](https://google.github.io/styleguide/go/decisions#mark-test-helpers)。更多细节见[测试助手的错误处理](https://google.github.io/styleguide/go/best-practices#test-helper-error-handling)。 -
断言助手是检查系统正确性的函数，如果没有达到预期，则测试失败。

[使用断言助手在Go中并不是一种惯例](https://google.github.io/styleguide/go/decisions#assert)。

测试的目的是报告被测代码的通过/失败情况。测试失败的理想场所是在Test函数自身中，因为这可以确保[失败信息](https://google.github.io/styleguide/go/decisions#useful-test-failures)和测试逻辑是清晰的。

随着你的测试代码的增长，可能有必要将一些功能分解为独立的功能。标准的软件工程考虑仍然适用，因为测试代码仍然是代码。如果功能不与测试框架交互，那么所有的常规规则都适用。然而，当普通代码与框架交互时，必须注意避免常见的陷阱，这些陷阱会导致信息量不足的失败信息和不可维护的测试。

如果许多独立的测试用例需要相同的验证逻辑，请以下列方式之一安排测试，而不是使用断言助手或复杂的验证函数。

- 在Test函数中内联逻辑（包括验证和失败），即使它是重复的。这在简单的情况下效果最好。
- 如果输入是类似的，考虑将它们统一到一个
[表驱动的测试](https://google.github.io/styleguide/go/decisions#table-driven-tests)中，同时在循环中保持逻辑的内联。这有助于避免重复，同时在测试中保持验证和失败。 - 如果有多个调用者需要相同的验证功能，但表格测试不适合（通常是因为输入不够简单或验证需要作为操作序列的一部分），安排验证函数，使其返回一个值（通常是一个error），而不是采取testing.T参数并使用它来使测试失败。在测试中使用逻辑来决定是否失败，并提供有用的测试失败。你也可以创建测试助手，以抽出常见的模板设置代码。

在最后一点中概述的设计保持正交性。例如，package cmp的设计不是为了使测试失败，而是为了比较（和差异）值。因此，它不需要知道进行比较的上下文，因为调用者可以提供这个。如果你的普通测试代码为你的数据类型提供了一个cmp.Transformer，这通常可以是最简单的设计。对于其他验证，可以考虑返回一个错误值。

```
// Good:
// polygonCmp returns a cmp.Option that equates s2 geometry objects up to
// some small floating-point error.
func polygonCmp() cmp.Option {
return cmp.Options{
cmp.Transformer("polygon", func(p *s2.Polygon) []*s2.Loop { return p.Loops() }),
cmp.Transformer("loop", func(l *s2.Loop) []s2.Point { return l.Vertices() }),
cmpopts.EquateApprox(0.00000001, 0),
cmpopts.EquateEmpty(),
}
}
func TestFenceposts(t *testing.T) {
// This is a test for a fictional function, Fenceposts, which draws a fence
// around some Place object. The details are not important, except that
// the result is some object that has s2 geometry (github.com/golang/geo/s2)
got := Fencepost(tomsDiner, 1*meter)
if diff := cmp.Diff(want, got, polygonCmp()); diff != "" {
t.Errorf("Fencepost(tomsDiner, 1m) returned unexpected diff (-want+got):\n%v", diff)
}
}
func FuzzFencepost(f *testing.F) {
// Fuzz test (https://go.dev/doc/fuzz) for the same.
f.Add(tomsDiner, 1*meter)
f.Add(school, 3*meter)
f.Fuzz(func(t *testing.T, geo Place, padding Length) {
got := Fencepost(geo, padding)
// Simple reference implementation: not used in prod, but easy to
// reasonable and therefore useful to check against in random tests.
reference := slowFencepost(geo, padding)
// In the fuzz test, inputs and outputs can be large so don't
// bother with printing a diff. cmp.Equal is enough.
if !cmp.Equal(got, reference, polygonCmp()) {
t.Errorf("Fencepost returned wrong placement")
}
})
}
```


polygonCmp函数对它的调用方式是不可知的；它不接受具体的输入类型，也不规定在两个对象不匹配的情况下该做什么。因此，更多的调用者可以使用它。

注意：在测试助手和普通库代码之间有一个类比。除非在极少数情况下，库中的代码通常不应该报panic；从测试中调用的代码不应该停止测试，除非继续下去没有意义。

### 设计可扩展的验证APIs

风格指南中关于测试的大部分建议都是关于测试你自己的代码。本节是关于如何为其他人提供设施来测试他们编写的代码，以确保它符合你的库的要求。

#### 验收测试

这种测试被称为[验收测试](https://en.wikipedia.org/wiki/Acceptance_testing)。这种测试的前提是，使用测试的人不知道测试中的每一个细节；他们只是把输入交给测试设施来完成工作。这可以被认为是一种[控制倒置](https://en.wikipedia.org/wiki/Inversion_of_control)的形式。

在一个典型的Go测试中，test函数控制着程序流程，没有断言和test函数指导鼓励你保持这种方式。本节解释了如何以符合Go风格的方式来编写对这些测试的支持。

在深入探讨如何做之前，请考虑下面摘录自io/fs中的一个例子。

```
type FS interface {
Open(name string) (File, error)
}
```


虽然已存在许多fs.FS的实现，但Go开发者可能会期望自己编写一个。为了帮助验证用户的fs.FS实现是否正确，testing/fstest中提供了一个名为fstest.TestFS的通用库。这个API将实现作为一个黑箱来处理，以确保它维护io/fs契约的最基本部分。

#### 编写验收测试

现在我们知道了什么是验收测试，以及为什么要使用验收测试，让我们来探讨为包chess建立验收测试，这是一个用来模拟国际象棋游戏的包。国际象棋的用户应该实现chess.Player接口。这些实现是我们要验证的主要内容。我们的验收测试关注的是棋手的实现是否合法走出棋子，而不是这些棋子是否聪明。

- 为验证行为创建一个新的包，通常在包名后面加上test一词来
[命名](https://google.github.io/styleguide/go/best-practices#naming-doubles-helper-package)（例如，chesstest）。 - 创建执行验证的函数，接受被测试的实现作为参数并对其进行练习。

```
// ExercisePlayer tests a Player implementation in a single turn on a board.
// The board itself is spot checked for sensibility and correctness.
//
// It returns a nil error if the player makes a correct move in the context
// of the provided board. Otherwise ExercisePlayer returns one of this
// package's errors to indicate how and why the player failed the
// validation.
func ExercisePlayer(b *chess.Board, p chess.Player) error
```


测试应该注意哪些不变式被破坏，以及如何破坏。你的设计可以在两种失败报告的规则中选择。

- 快速失败：一旦实现违反了一个不变式，就返回一个错误。

这是最简单的方法，如果预计验收测试会快速执行，那么它的效果很好。简单的[错误哨兵](https://google.github.io/styleguide/go/index.html#gotip)和[自定义类型](https://google.github.io/styleguide/go/index.html#gotip)可以很容易地用在这里，这反倒使测试验收测试变得容易。

```
for color, army := range b.Armies {
// The king should never leave the board, because the game ends at
// checkmate.
if army.King == nil {
return &MissingPieceError{Color: color, Piece: chess.King}
}
}
```


- 汇总所有的失败：收集所有的失败，并全部报告。

这种方法感觉上类似于[“继续进行下去”的规则](https://google.github.io/styleguide/go/decisions#keep-going)，如果验收测试预计执行缓慢，这种方法可能更可取。

你如何聚集失败，应该由你是否想让用户或你自己有能力询问单个失败（例如，测试你的验收测试）来决定。下面演示了使用一个自定义的错误类型来聚合错误。

```
var badMoves []error
move := p.Move()
if putsOwnKingIntoCheck(b, move) {
badMoves = append(badMoves, PutsSelfIntoCheckError{Move: move})
}
if len(badMoves) > 0 {
return SimulationError{BadMoves: badMoves}
}
return nil
```


验收测试应该遵守[“继续进行下去”](https://google.github.io/styleguide/go/decisions#keep-going)的规则，不调用t.Fatal，除非测试检测到被测试的系统中的不变量被损坏。

例如，t.Fatal应该保留给特殊情况，如[设置失败](https://google.github.io/styleguide/go/best-practices#test-helper-error-handling)：

```
func ExerciseGame(t *testing.T, cfg *Config, p chess.Player) error {
t.Helper()
if cfg.Simulation == Modem {
conn, err := modempool.Allocate()
if err != nil {
t.Fatalf("no modem for the opponent could be provisioned: %v", err)
}
t.Cleanup(func() { modempool.Return(conn) })
}
// Run acceptance test (a whole game).
}
```


这种技术可以帮助你创建简明、规范的验证。但不要试图用它来绕过断言的规则。

最终产品应该以类似这样的形式提供给终端用户。

```
// Good:
package deepblue_test
import (
"chesstest"
"deepblue"
)
func TestAcceptance(t *testing.T) {
player := deepblue.New()
err := chesstest.ExerciseGame(t, chesstest.SimpleGame, player)
if err != nil {
t.Errorf("deepblue player failed acceptance test: %v", err)
}
}
```


### 使用真实的传输

当测试组件集成时，特别是HTTP或RPC被用作组件之间的底层传输时，最好使用真正的底层传输来连接到后端的测试版本。

例如，假设你要测试的代码（有时被称为 “被测系统 “或SUT）与实现[长期运行操作的API](https://pkg.go.dev/google.golang.org/genproto/googleapis/longrunning)的后端交互。为了测试你的SUT，使用一个真正的[OperationsClient](https://pkg.go.dev/google.golang.org/genproto/googleapis/longrunning#OperationsClient)，它连接到[OperationsServer](https://pkg.go.dev/google.golang.org/genproto/googleapis/longrunning#OperationsServer)的测试替身（例如，一个mock、stub或fake）。

由于正确模仿客户端行为的复杂性，我们建议不要手工实现客户端。通过使用生产客户端和测试专用服务器，你可以确保你的测试尽可能多地使用真实代码。

提示：在可能的情况下，使用由被测服务的作者提供的测试库。

### t.Error vs. t.Fatal

正如[决定篇](https://tonybai.com/google-go-style/google-go-style-decisions)中所讨论的，测试一般不应该在第一次遇到问题时就中止。

然而，有些情况需要测试不要继续进行。当某些测试设置失败时，调用t.Fatal是合适的，特别是在测试设置助手中，没有它你就不能运行测试的其余部分。在表驱动的测试中，t.Fatal适合于在测试循环之前设置整个测试功能的失败。影响测试表中单个条目的故障，使该条目无法继续进行，应按以下方式报告。

- 如果你没有使用t.Run子测试，使用t.Error，后面跟一个continue语句，继续执行下一个表项。
- 如果你使用了子测试（并且你在调用t.Run的过程中），使用t.Fatal，结束当前的子测试并允许你的测试用例进入下一个子测试。

警告：调用t.Fatal和类似函数并不总是安全的。更多的细节[在这里](https://google.github.io/styleguide/go/best-practices#t-fatal-goroutine)。

### 测试助手中的错误处理

注意：本节讨论的是Go使用的测试助手：执行测试设置和清理的函数，而不是普通的断言设施。更多讨论见[测试函数部分](https://google.github.io/styleguide/go/best-practices#test-functions)。

由测试助手执行的操作有时会失败。例如，创建一个带有文件的目录涉及到I/O，这可能会失败。当测试助手失败时，它们的失败往往意味着测试不能继续，因为一个设置前提条件失败了。当这种情况发生时，最好在帮助器中调用一个Fatal函数。

```
// Good:
func mustAddGameAssets(t *testing.T, dir string) {
t.Helper()
if err := os.WriteFile(path.Join(dir, "pak0.pak"), pak0, 0644); err != nil {
t.Fatalf("Setup failed: could not write pak0 asset: %v", err)
}
if err := os.WriteFile(path.Join(dir, "pak1.pak"), pak1, 0644); err != nil {
t.Fatalf("Setup failed: could not write pak1 asset: %v", err)
}
}
```


这就使调用方比帮助器返回错误给测试本身更干净：

```
// Bad:
func addGameAssets(t *testing.T, dir string) error {
t.Helper()
if err := os.WriteFile(path.Join(d, "pak0.pak"), pak0, 0644); err != nil {
return err
}
if err := os.WriteFile(path.Join(d, "pak1.pak"), pak1, 0644); err != nil {
return err
}
return nil
}
```


警告：调用t.Fatal和类似函数并不总是安全的。更多的细节[在这里](https://google.github.io/styleguide/go/best-practices#t-fatal-goroutine)。

失败信息应该包括对所发生的事情的描述。这一点很重要，因为你可能会向许多用户提供测试用的API，特别是随着帮助器中产生错误的步骤的增加。当测试失败时，用户应该知道在哪里，以及为什么。

提示：Go 1.14引入了一个t.Cleanup函数，可以用来注册清理函数，在你的测试完成后运行。该函数也适用于测试帮助器。请参阅[GoTip #4: 清理你的测试以获得简化测试助手](https://google.github.io/styleguide/go/index.html#gotip)的指导。

下面是一个名为paint_test.go的虚构文件中的片段，演示了(*testing.T).Helper如何影响Go测试中的失败报告。

```
package paint_test
import (
"fmt"
"testing"
)
func paint(color string) error {
return fmt.Errorf("no %q paint today", color)
}
func badSetup(t *testing.T) {
// This should call t.Helper, but doesn't.
if err := paint("taupe"); err != nil {
t.Fatalf("could not paint the house under test: %v", err) // line 15
}
}
func mustGoodSetup(t *testing.T) {
t.Helper()
if err := paint("lilac"); err != nil {
t.Fatalf("could not paint the house under test: %v", err)
}
}
func TestBad(t *testing.T) {
badSetup(t)
// ...
}
func TestGood(t *testing.T) {
mustGoodSetup(t) // line 32
// ...
}
```


下面是上面示例的运行输出结果，请注意高亮部分以及它们的内容差别：

```
=== RUN TestBad
paint_test.go:15: could not paint the house under test: no "taupe" paint today
--- FAIL: TestBad (0.00s)
=== RUN TestGood
paint_test.go:32: could not paint the house under test: no "lilac" paint today
--- FAIL: TestGood (0.00s)
FAIL
```


paint_test.go:15的错误是指在badSetup中失败的setup函数的那一行。

```
t.Fatalf("could not paint the house under test: %v", err)
```


而paint_test.go:32指的是TestGood中失败的测试行。

```
goodSetup(t)
```


正确地使用(*testing.T).Helper可以将失败的位置归结得更好：

- 助手函数扩展
- 帮助器函数调用其他帮助器
- 测试函数中的帮助器使用量增加

提示：如果一个帮助器调用 (*testing.T).Error 或 (*testing.T).Fatal，在格式字符串中提供一些上下文，以帮助确定什么地方出错以及为什么。

提示：如果一个帮助器没有做任何事情会导致测试失败，它就不需要调用t.Helper。通过从函数参数列表中删除t来简化其签名。

### 不要从独立的goroutine中调用t.Fatal

正如包testing中所记载的，从任何goroutine中调用t.FailNow、t.Fatal等都是不正确的，除了运行Test函数（或子测试）的goroutine。如果你的测试启动了新的goroutine，它们一定不能从这些goroutine内部调用这些函数。

测试助手通常不会从新的goroutine发出失败信号，因此他们使用t.Fatal是完全正确的。如果有疑问，可以调用t.Error并返回。

```
// Good:
func TestRevEngine(t *testing.T) {
engine, err := Start()
if err != nil {
t.Fatalf("Engine failed to start: %v", err)
}
num := 11
var wg sync.WaitGroup
wg.Add(num)
for i := 0; i < num; i++ {
go func() {
defer wg.Done()
if err := engine.Vroom(); err != nil {
// This cannot be t.Fatalf.
t.Errorf("No vroom left on engine: %v", err)
return
}
if rpm := engine.Tachometer(); rpm > 1e6 {
t.Errorf("Inconceivable engine rate: %d", rpm)
}
}()
}
wg.Wait()
if seen := engine.NumVrooms(); seen != num {
t.Errorf("engine.NumVrooms() = %d, want %d", seen, num)
}
}
```


在测试或子测试中添加t.Parallel并不意味着调用t.Fatal就不安全。

当所有对testing包API的调用都在测试函数中时，通常很容易发现不正确的用法，因为go关键字是显而易见的。传递testing.T参数会使跟踪这种用法更加困难。通常情况下，传递这些参数的原因是为了引入一个测试助手，而这些测试助手不应该依赖于被测系统。因此，如果一个测试助手注册了一个致命的测试失败，它可以而且应该从测试的goroutine中这样做。

### 使用结构体字面值的字段标签

在表格驱动的测试中，最好为每个测试用例指定key。当测试用例覆盖了大量的垂直空间（例如，超过20-30行），当有相同类型的相邻字段时，以及当你希望省略具有零值的字段时，这是有帮助的。比如说。

```
// Good:
tests := []struct {
foo *pb.Foo
bar *pb.Bar
want string
}{
{
foo: pb.Foo_builder{
Name: "foo",
// ...
}.Build(),
bar: pb.Bar_builder{
Name: "bar",
// ...
}.Build(),
want: "result",
},
}
```


### 保持setup代码在特定的测试范围内

在可能的情况下，资源和依赖关系的设置应该尽可能地与具体的测试案例紧密联系。例如，给定一个设置函数。

```
// mustLoadDataSet loads a data set for the tests.
//
// This example is very simple and easy to read. Often realistic setup is more
// complex, error-prone, and potentially slow.
func mustLoadDataset(t *testing.T) []byte {
t.Helper()
data, err := os.ReadFile("path/to/your/project/testdata/dataset")
if err != nil {
t.Fatalf("could not load dataset: %v", err)
}
return data
}
```


在需要它的测试函数中明确调用mustLoadDataset：

```
// Good:
func TestParseData(t *testing.T) {
data := mustLoadDataset(t)
parsed, err := ParseData(data)
if err != nil {
t.Fatalf("unexpected error parsing data: %v", err)
}
want := &DataTable{ /* ... */ }
if got := parsed; !cmp.Equal(got, want) {
t.Errorf("ParseData(data) = %v, want %v", got, want)
}
}
func TestListContents(t *testing.T) {
data := mustLoadDataset(t)
contents, err := ListContents(data)
if err != nil {
t.Fatalf("unexpected error listing contents: %v", err)
}
want := []string{ /* ... */ }
if got := contents; !cmp.Equal(got, want) {
t.Errorf("ListContents(data) = %v, want %v", got, want)
}
}
func TestRegression682831(t *testing.T) {
if got, want := guessOS("zpc79.example.com"), "grhat"; got != want {
t.Errorf(`guessOS("zpc79.example.com") = %q, want %q`, got, want)
}
}
```


测试函数TestRegression682831没有使用数据集，因此没有调用慢且容易失败的mustLoadDataset：

```
// Bad:
var dataset []byte
func TestParseData(t *testing.T) {
// As documented above without calling mustLoadDataset directly.
}
func TestListContents(t *testing.T) {
// As documented above without calling mustLoadDataset directly.
}
func TestRegression682831(t *testing.T) {
if got, want := guessOS("zpc79.example.com"), "grhat"; got != want {
t.Errorf(`guessOS("zpc79.example.com") = %q, want %q`, got, want)
}
}
func init() {
dataset = mustLoadDataset()
}
```


用户可能希望在与其他函数隔离的情况下运行一个函数，不应受到这些因素的惩罚：

```
# No reason for this to perform the expensive initialization.
$ go test -run TestRegression682831
```


### 何时使用自定义TestMain入口

如果软件包中的所有测试都需要共同的setup，并且setup需要teardown，你可以使用一个[自定义的testmain入口](https://go.dev/pkg/testing/#hdr-Main)。如果测试用例需要的资源的设置特别昂贵，而且成本应该被摊销，就会发生这种情况。通常情况下，你在这一点上已经从测试套件中提取了任何无关的测试。它通常只用于[功能测试](https://en.wikipedia.org/wiki/Functional_testing)。

使用一个自定义的TestMain不应该是你的第一选择，因为正确使用它应该有一定的谨慎。首先考虑在[摊销普通测试设置部分](https://google.github.io/styleguide/go/best-practices#t-setup-amortization)的解决方案或普通测试助手是否足以满足你的需求。

```
// Good:
var db *sql.DB
func TestInsert(t *testing.T) { /* omitted */ }
func TestSelect(t *testing.T) { /* omitted */ }
func TestUpdate(t *testing.T) { /* omitted */ }
func TestDelete(t *testing.T) { /* omitted */ }
// runMain sets up the test dependencies and eventually executes the tests.
// It is defined as a separate function to enable the setup stages to clearly
// defer their teardown steps.
func runMain(ctx context.Context, m *testing.M) (code int, err error) {
ctx, cancel := context.WithCancel(ctx)
defer cancel()
d, err := setupDatabase(ctx)
if err != nil {
return 0, err
}
defer d.Close() // Expressly clean up database.
db = d // db is defined as a package-level variable.
// m.Run() executes the regular, user-defined test functions.
// Any defer statements that have been made will be run after m.Run()
// completes.
return m.Run(), nil
}
func TestMain(m *testing.M) {
code, err := runMain(context.Background(), m)
if err != nil {
// Failure messages should be written to STDERR, which log.Fatal uses.
log.Fatal(err)
}
// NOTE: defer statements do not run past here due to os.Exit
// terminating the process.
os.Exit(code)
}
```


理想情况下，一个测试用例在自身的调用和其他测试用例之间是隔离的。

至少要确保单个测试用例重置他们所修改的任何全局状态，如果他们已经这样做了（例如，如果测试是与外部数据库一起工作）。

### 摊销共同测试设置

如果共同setup有以下情况，使用sync.Once可能是合适的，尽管不是必须的：

- 它很昂贵。
- 它只适用于某些测试。
- 它不需要teardown。

```
// Good:
var dataset struct {
once sync.Once
data []byte
err error
}
func mustLoadDataset(t *testing.T) []byte {
t.Helper()
dataset.once.Do(func() {
data, err := os.ReadFile("path/to/your/project/testdata/dataset")
// dataset is defined as a package-level variable.
dataset.data = data
dataset.err = err
})
if err := dataset.err; err != nil {
t.Fatalf("could not load dataset: %v", err)
}
return dataset.data
}
```


当mustLoadDataset被用于多个测试函数时，其成本被摊销。

```
// Good:
func TestParseData(t *testing.T) {
data := mustLoadDataset(t)
// As documented above.
}
func TestListContents(t *testing.T) {
data := mustLoadDataset(t)
// As documented above.
}
func TestRegression682831(t *testing.T) {
if got, want := guessOS("zpc79.example.com"), "grhat"; got != want {
t.Errorf(`guessOS("zpc79.example.com") = %q, want %q`, got, want)
}
}
```


共同的teardown之所以棘手，是因为没有统一的地方来注册清理例程。如果setup函数（在这种情况下是loadDataset）依赖于一个上下文，sync.Once可能会有问题。这是因为对setup函数的两次竞争调用中的第二次需要等待第一次调用完成后再返回。这段等待时间可能与上下文的取消操作有竞争。

## 字符串连接

Go支持很多种字符串连接的方法，比如：

- “+” 操作符
- fmt.Sprintf
- strings.Builder
- text/template
- safehtml/template

虽然没有一个放之四海而皆准的选择规则，但以下指导意见概述了每种方法在什么情况下是首选。

### 简单情况下首选”+”操作符

当连接几个字符串时，更倾向于使用”+”。这种方法在语法上是最简单的，不需要导入。

```
// Good:
key := "projectid: " + p
```


### 在需要格式化的情况下，选择fmt.Sprintf

当建立一个带有格式化的复杂字符串时，更倾向于使用fmt.Sprintf。使用许多”+”运算符可能会掩盖最终的结果。

```
// Good:
str := fmt.Sprintf("%s [%s:%d]-> %s", src, qos, mtu, dst)
```


```
// Bad:
bad := src.String() + " [" + qos.String() + ":" + strconv.Itoa(mtu) + "]-> " + dst.String()
```


最佳实践：当字符串构建操作的输出是io.Writer时，不要为了发送到Writer而用fmt.Sprintf构建一个临时字符串，相反，使用fmt.Fprintf来直接向Writer发送。

当格式化更加复杂时，请酌情选择text/template或safehtml/template。

### 倾向于使用strings.Builder基于零散字符串构建字符串

尽量使用strings.Builder基于零散字符串构建字符串。strings.Builder需要摊销的线性时间，而”+”和fmt.Sprintf在连续调用以形成一个较大的字符串时需要二次方时间。

```
// Good:
b := new(strings.Builder)
for i, d := range digitsOfPi {
fmt.Fprintf(b, "the %d digit of pi is: %d\n", i, d)
}
str := b.String()
```


注意：关于更多的讨论，请参阅[GoTip #29: 高效地构建字符串](https://google.github.io/styleguide/go/index.html#gotip)。

### 常量字符串

尽量用“构建多行常量字符串。

```
// Good:
usage := `Usage:
custom_tool [args]`
```


```
// Bad:
usage := "" +
"Usage:\n" +
"\n" +
"custom_tool [args]"
```


## 评论