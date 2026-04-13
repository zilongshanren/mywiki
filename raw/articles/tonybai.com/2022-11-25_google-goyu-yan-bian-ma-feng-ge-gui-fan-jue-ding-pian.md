---
title: Google Go语言编码风格规范：决定篇
url: https://tonybai.com/google-go-style/google-go-style-decisions/
published: '2022-11-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Google Go语言编码风格规范：决定篇

![](../../assets/9e6134bbc036be7b.png)


[本文永久链接](https://tonybai.com/google-go-style/google-go-style-decisions) – https://tonybai.com/google-go-style/google-go-style-decisions

本页面是2022年11月中旬Google发布的[Go语言编码风格规范](https://google.github.io/styleguide/go/index)系列文档的[决定篇](https://google.github.io/styleguide/go/decisions)的中译版。

注意：这是介绍[Google Go编码风格的系列文档](https://tonybai.com/google-go-style)的一部分。本文档是规范性的，但不具备权威性。本篇级别要低于[指南篇](https://tonybai.com/google-go-style/google-go-style-guide)，更多信息请参见[概述篇](https://tonybai.com/google-go-style)。

## 关于

本文档包含了Go编码风格的决定，旨在整合统一Go可读性导师给出的建议，并提供标准的指导、解释和例子。

本文档并不是完全版，而是会随着时间的推移而增加内容。如果[核心风格指南](https://tonybai.com/google-go-style-guide)与这里给出的建议相矛盾，则以风格指南为准，本文档也应进行相应更新。

请参阅[“概述篇”](https://tonybai.com/google-go-style)中的全套Go编码风格文档。

以下部分已从本风格决定篇中移至[指南篇](https://tonybai.com/google-go-style/google-go-style-guide)了：

- 驼峰命名
- 格式化
- 行长

## 命名

关于命名的总体指导，见[核心风格指南](https://tonybai.com/google-go-style/google-go-style-guide)中的命名部分。以下各节将对命名进行细分场景的进一步的说明。

### 下划线

Go语言中的名称一般不应包含下划线，不过这一原则有三个例外：

- 仅由生成的代码导入的包名可以包含下划线。关于如何选择由多个单词组成的包名的更多细节，请参阅下面
**包名**一节。 - 在*_test.go文件中的Test、Benchmark和Example函数名称可以包含下划线。
- 与操作系统或cgo互操作的低级库可以重复使用标识符，就像在
[syscall](https://pkg.go.dev/syscall#pkg-constants)中那样。但这在大多数代码库中是非常罕见的。

### 包名

Go包的名称应该是短小的，并且只包含小写字母。由多个单词组成的包名的各个单词之间应该没有间断。例如，我们使用[tabwriter](https://pkg.go.dev/text/tabwriter)作为包名，而不是tabWriter，TabWriter或者tab_writer。

避免选择那些可能被常用的局部变量名称[遮蔽](https://google.github.io/styleguide/go/best-practices#shadowing)的包名。例如，usercount是一个比count更好的包名，因为count是一个常用的变量名。

Go包的名字不应该有下划线。如果您需要导入一个名称中含有下划线的包（通常来自自动生成的代码或第三方代码），必须**在导入时将其重命名为适合在Go代码中使用的名称**。

这方面的一个例外是，仅由生成的代码导入的包名可以包含下划线，具体的例子包括：

- 在外部测试包的包名中使用_test后缀，例如集成测试。
- 在
[包级的文档示例](https://go.dev/blog/examples)中使用_test后缀。

避免使用诸如util、utility、common、helper等信息量不足的包名。更多信息参见所谓的[“实用程序包”](https://google.github.io/styleguide/go/best-practices#util-packages)。

当一个导入的包被重命名时（例如：import foopb “path/to/foo_go_proto”），该包的本地名称必须符合上述规则，因为本地名称决定了包中的符号在文件中的引用方式。如果一个包在多个文件中被导入时都做了重命名，特别是在相同或邻近的包中，为了保持一致性，应尽可能使用相同的本地名称。

也请参见：[关于包名的Go博文](https://go.dev/blog/package-names)。

### Receiver命名

[Receiver](https://golang.org/ref/spec#Method_declarations)变量的名称必须满足下面要求：

- 短（通常为一或两个字母的长度）。
- 类型本身的缩略语。
- 统一应用于该类型的每一个Receiver。

![](../../assets/09167313fc18b60f.png)


| 长名字 | 更好的名字 |
|---|---|
`func (tray Tray)` |
`func (t Tray)` |
`func (info *ResearchInfo)` |
`func (ri *ResearchInfo)` |
`func (this *ReportWriter)` |
`func (w *ReportWriter)` |
`func (self *Scanner)` |
`func (s *Scanner)` |

### 常量命名

常量名称必须像Go中的其他名称一样使用驼峰命名法(MixedCaps)(导出的常量以大写字母开始，而未导出的常量以小写字母开始)。即便这与其他语言中的惯例有悖。常量名称不应该是其值的衍生物，而应该解释其值所表示的内容：

```
// Good:
const MaxPacketSize = 512 // 译注：不应命名为FiveHundredTwelve
const (
ExecuteBit = 1 << iota
WriteBit
ReadBit
)
```


不要使用非驼峰命名的常量名称或带有K前缀的常量：

```
// Bad:
const MAX_PACKET_SIZE = 512
const kMaxBufferSize = 1024
const KMaxUsersPergroup = 500
```


根据常量的作用来命名常量，而不是根据它们的值。如果一个常量除了它的值之外没有作用，那么就没有必要把它定义为一个常量。

```
// Bad:
const Twelve = 12
const (
UserNameColumn = "username"
GroupColumn = "group"
)
```


### 首字母缩略词(Initialisms)

名称中的单词如果是首字母缩略词或缩略语（例如，URL和NATO）应该使用相同的大小写命名。URL应该使用URL或url（如urlPony，或URLPony），而不是Url。这也适用于ID，当它是“标识符”的缩写时使用appID而不是appId。

- 在有多个首字母缩略词的名字中（例如XMLAPI，它包含XML和API两个首字母缩略词），每个首字母缩略词中的字母都应该具有一致的大小写，但名字中的多个首字母缩略词不需要有相同的大小写。
- 在包含小写字母的首字母缩略词名称中（例如DDoS、iOS、gRPC），首字母应该保持其在缩略词中原有的样子，除非你需要为了导出该名称而改变第一个字母。在这些情况下，整个首字母缩略词中的字母应该采用相同的大小写（例如，ddos, IOS, GRPC）。

![](../../assets/a9896530124b6ab6.png)


| 首字母缩略词 | 作用域 | 正确的 | 不正确的 |
|---|---|---|---|
| XML API | 导出的 | `XMLAPI` |
`XmlApi` , `XMLApi` , `XmlAPI` , `XMLapi` |
| XML API | 非导出的 | `xmlAPI` |
`xmlapi` , `xmlApi` |
| iOS | 导出的 | `IOS` |
`Ios` , `IoS` |
| iOS | 非导出的 | `iOS` |
`ios` |
| gRPC | 导出的 | `GRPC` |
`Grpc` |
| gRPC | 非导出的 | `gRPC` |
`grpc` |
| DDoS | 导出的 | `DDoS` |
`DDOS` , `Ddos` |
| DDoS | 非导出的 | `ddos` |
`dDoS` , `dDOS` |

### Getter命名

函数和方法名称不应该使用Get或get前缀，除非底层概念使用“get”一词（例如HTTP GET）。我们倾向于直接用那个要Get的事物名词进行命名，例如使用Counts而不是GetCounts。

如果函数涉及到执行复杂的计算或执行远程调用，可以使用不同的词，如Compute或Fetch来代替Get，以使读者清楚地知道函数调用可能需要时间，并可能阻塞或失败。

### 变量命名

一般的经验法则是，名字的长度应该与它使用的范围大小成正比，与它在该范围内使用的次数成反比。一个在文件范围内创建的变量，其名称可能需要由多个单词组成，而一个在单个内部代码块范围内的变量可能只需要用一个单词命名，甚至只有一两个字符，以保持代码的清晰和避免无关的信息。

这里有一个粗略的基线。这些数字准则并不是严格的规则。根据上下文、[清晰度](https://google.github.io/styleguide/go/guide#clarity)和[简明度](https://google.github.io/styleguide/go/guide#concision)来应用判断：

- 小范围是指执行一个或两个小操作的范围，例如1-7行。
- 中等范围是指几个小的或一个大的操作，例如8-15行。
- 大范围是指一个或几个大的操作，例如15-25行。
- 一个非常大的范围是任何跨越一页以上的范围（比如，超过25行）。

一个在小范围内可能非常清楚的名字（例如，c代表一个计数器）在大范围内可能是不足以胜任的，需要在代码中进一步澄清以提醒读者其目。当一个范围内有许多变量，或者有表示类似的值或概念的变量时，我们可能需要比范围建议的更长的变量名。

概念的特殊性也可以帮助保持变量名称的简明性。例如，假设只有一个单一的数据库在使用，那么像db这样的短小的变量名称，通常可能是为非常小的范围保留的，即使范围非常大，也可能保持完全清晰。在这种情况下，根据作用域的大小，以database命名可以接受的，但并不是必须的，因为db是一个非常常见的词的简称，几乎没有其他的解释。

局部变量的名称应该反映它所包含的内容以及它在当前上下文环境中的使用方式，而不是数值的来源。例如，通常情况下，最好的局部变量名称与结构体字段或protocol buffer的字段名称不一样。

一般来说：

- 像count或options这样的单个单词名称是一个好的起点。
- 可以添加额外的词来区分类似的名字，例如userCount和projectCount。
- 不要为了节省几次打字而简单地删除字母。例如，Sandbox比Sbx更受欢迎，特别是对于导出的名字。
- 在大多数变量名称中省略
[类型和类似类型](https://google.github.io/styleguide/go/decisions#repetitive-with-type)的词。- 对于一个数字来说，userCount是一个比numUsers或usersInt更好的名字。
- 对于一个切片来说，users是一个比userSlice更好的名字。
- 如果一个值在范围内有两个版本，那么名字中包含一个类似类型的修饰词是可以接受的，例如，你可能将命令行输入的内容存储在ageString中，并使用age作为解析后的值。

- 省略那些从
[周围上下文](https://google.github.io/styleguide/go/decisions#repetitive-in-context)中可以清楚看出的词。例如，在一个UserCount方法的实现中，一个叫做userCount的局部变量可能是多余的；count、users、甚至c都具备一样的可读性。

#### 单字母变量名

单字母变量名可以是一个有用的工具，可以最大限度地减少[重复](https://google.github.io/styleguide/go/decisions#repetition)，但这类变量名也可能使代码出现不必要地不透明。把它们的使用限制在其全词含义很明显的情况下，而且如果用全词来代替单字母变量，就会出现重复的情况。

一般来说：

- 对于一个方法接收器变量，最好使用一个或两个字母的名字。
- 对常见的类型使用熟悉的变量名通常是有帮助的。
- r代表io.Reader或*http.Request
- w代表io.Writer或http.ResponseWriter。

- 单字母标识符作为整数循环变量是可以接受的，特别是对于索引（如i）和坐标（如x和y）。
- 当范围很小时，缩写可以成为可接受的循环标识符，例如，for _, n := range nodes { … }。

### 重复

Go源代码应该避免不必要的重复。这方面的一个常见来源是重复的名称，它往往包括不必要的单词或重复其上下文或类型。如果相同或类似的代码段在很近的地方多次出现，代码本身也会出现不必要的重复。

重复性命名有多种形式，包括：

#### 包 vs. 导出符号的名称

当命名导出的符号时，包的名称在你的包外总是可见的，所以这两者之间的冗余信息应该减少或消除。如果一个包只导出了一个类型，并且是以包本身的名字命名的，如果需要一个构造函数，那么构造函数的规范名称就是New。

例子：

![](../../assets/31e68480b073afe6.png)


| 重复的名字 | 更好的名字 |
|---|---|
`widget.NewWidget` |
`widget.New` |
`widget.NewWidgetWithName` |
`widget.NewWithName` |
`db.LoadFromDatabase` |
`db.Load` |
`goatteleportutil.CountGoatsTeleported` |
`gtutil.CountGoatsTeleported` 或 `goatteleport.Count` |
`myteampb.MyTeamMethodRequest` |
`mtpb.MyTeamMethodRequest` 或 `myteampb.MethodRequest` |

#### 变量名称 vs. 类型

编译器总是知道变量的类型，而且在大多数情况下，读者也可以通过变量的使用方式清楚地知道它是什么类型。只有当一个变量的值在同一范围内出现两次时，才有必要澄清它的类型。

![](../../assets/6e2ae75dbe07f4fe.png)


| 重复的名字 | 更好的名字 |
|---|---|
`var numUsers int` |
`var users int` |
`var nameString string` |
`var name string` |
`var primaryProject *Project` |
`var primary *Project` |

如果该值以多种形式出现，可以用一个额外的词来澄清，如raw和parsed，或者用底层表示法：

```
// Good:
limitStr := r.FormValue("limit")
limit, err := strconv.Atoi(limitStr)
```


```
// Good:
limitRaw := r.FormValue("limit")
limit, err := strconv.Atoi(limitRaw)
```


#### 外部上下文 vs. 本地名称

包含周围上下文信息的名字往往不仅没有带来好处，还会产生额外的噪音。包名、方法名、类型名、函数名、导入路径、甚至文件名都可以提供自动限定其中所有名称的上下文信息。

```
// Bad:
// In package "ads/targeting/revenue/reporting"
type AdsTargetingRevenueReport struct{}
func (p *Project) ProjectName() string
```


```
// Good:
// In package "ads/targeting/revenue/reporting"
type Report struct{}
func (p *Project) Name() string
```


```
// Bad:
// In package "sqldb"
type DBConnection struct{}
```


```
// Good:
// In package "sqldb"
type Connection struct{}
```


```
// Bad:
// In package "ads/targeting"
func Process(in *pb.FooProto) *Report {
adsTargetingID := in.GetAdsTargetingID()
}
```


```
// Good:
// In package "ads/targeting"
func Process(in *pb.FooProto) *Report {
id := in.GetAdsTargetingID()
}
```


重复一般应在符号使用者的上下文中进行评估，而不是孤立地进行评估。例如，下面的代码有很多名字，在某些情况下可能是好的，但在上下文中是多余的。

```
// Bad:
func (db *DB) UserCount() (userCount int, err error) {
var userCountInt64 int64
if dbLoadError := db.LoadFromDatabase("count(distinct users)", &userCountInt64); dbLoadError != nil {
return 0, fmt.Errorf("failed to load user count: %s", dbLoadError)
}
userCount = int(userCountInt64)
return userCount, nil
}
```


相反，那些上下文或用法中明确的名称信息往往可以被省略：

```
// Good:
func (db *DB) UserCount() (int, error) {
var count int64
if err := db.Load("count(distinct users)", &count); err != nil {
return 0, fmt.Errorf("failed to load user count: %s", err)
}
return int(count), nil
}
```


## 注释

对注释的惯例（包括注释的内容、使用的风格、如何提供可运行的例子等）进行说明是为了更好地提升阅读公共API文档的体验。更多信息请参见[Effective Go](http://golang.org/doc/effective_go.html#commentary)。

**最佳实践**：在开发和代码审查过程中使用[文档预览](https://google.github.io/styleguide/go/best-practices#documentation-preview)，看看文档和可运行的例子是否有用，是否按照你期望的方式呈现。

**提示**：Godoc很少使用特殊格式；列表和代码片段通常应该缩进以避免换行。除缩进外，一般应避免使用其他修饰方法。

### 注释行的长度

确保注释即使在狭窄的屏幕上也能从源码中读到。

当一个注释变得太长时，建议将它拆成多个单行注释。在可能的情况下，争取使注释在80列宽的终端上也能很好阅读，但这并不是一个硬性规定；Go中的注释没有固定的行长限制。例如，标准库经常选择根据标点符号来中断注释，这有时会使个别行更接近60-70个字符。

有很多现有的代码中，注释的长度超过了80个字符。本指南不应作为修改这些代码的理由，作为可读性审查的一部分（见[一致性](https://google.github.io/styleguide/go/guide#consistency)），尽管我们鼓励团队适时地更新注释以遵循本指南并作为其他重构的一部分。本指南的主要目标是确保所有Go可读性导师在提出建议时都能做出相同的建议。

关于注释的更多内容，请参见[The Go Blog关于文档的这篇文章](https://blog.golang.org/godoc-documenting-go-code)。

```
# Good:
// This is a comment paragraph.
// The length of individual lines doesn't matter in Godoc;
// but the choice of wrapping makes it easy to read on narrow screens.
//
// Don't worry too much about the long URL:
// https://supercalifragilisticexpialidocious.example.com:8080/Animalia/Chordata/Mammalia/Rodentia/Geomyoidea/Geomyidae/
//
// Similarly, if you have other information that is made awkward
// by too many line breaks, use your judgment and include a long line
// if it helps rather than hinders.
```


避免在小屏幕上重复折行的注释，这是一种糟糕的读者体验：

```
# Bad:
// This is a comment paragraph. The length of individual lines doesn't matter in
Godoc;
// but the choice of wrapping causes jagged lines on narrow screens or in
Critique,
// which can be annoying, especially when in a comment block that will wrap
repeatedly.
//
// Don't worry too much about the long URL:
// https://supercalifragilisticexpialidocious.example.com:8080/Animalia/Chordata/Mammalia/Rodentia/Geomyoidea/Geomyidae/
```


### 文档注释

所有顶层导出的名字都必须有文档注释，具有不明显的行为或意义的未导出的类型或函数声明也应该如此。这些注释应该是以被描述对象的名称开始的[完整句子](https://google.github.io/styleguide/go/decisions#comment-sentences)。冠词（”a”、”an”、”the”）可以放在名字前面，使其读起来更自然。

```
// Good:
// A Request represents a request to run a command.
type Request struct { ...
// Encode writes the JSON encoding of req to w.
func Encode(w io.Writer, req *Request) { ...
```


文档注释出现在[Godoc](https://pkg.go.dev/)中，并被IDE显示出来，因此应该为使用该包的任何人编写文档注释。

文档注释适用于以下符号，如果它出现在一个结构体中，则适用于该组字段。

```
// Good:
// Options configure the group management service.
type Options struct {
// General setup:
Name string
Group *FooGroup
// Dependencies:
DB *sql.DB
// Customization:
LargeGroupThreshold int // optional; default: 10
MinimumMembers int // optional; default: 2
}
```


**最佳实践**：如果你有针对未导出代码的文档注释，请遵循与导出代码相同的习惯（即以未导出的名称开始注释）。这使得以后导出时很容易，只需在注释和代码中用新导出的名字替换未导出的名字即可。

### 注释句子

作为完整的句子的注释应该像标准英语句子一样首词头字母大写并使用标点符号。(作为一个例外，在一个句子的开头使用非头母大写的标识符是可以的。这种情况可能最好只在段落的开头进行）。

作为句子片段的注释对标点符号和大写字母没有这样的要求。

文档注释应该始终是完整的句子，因此应该始终首词头字母大写和使用标点。简单的行末注释（特别是对结构体字段）可以是简单的短语，并假定字段名是短语的主语。

```
// Good:
// A Server handles serving quotes from the collected works of Shakespeare.
type Server struct {
// BaseDir points to the base directory under which Shakespeare's works are stored.
//
// The directory structure is expected to be the following:
// {BaseDir}/manifest.json
// {BaseDir}/{name}/{name}-part{number}.txt
BaseDir string
WelcomeMessage string // displayed when user logs in
ProtocolVersion string // checked against incoming requests
PageLength int // lines per page when printing (optional; default: 20)
}
```


### 例子

软件包应该清楚地记录它们的预期用途。尽量提供一个[可运行的例子](http://blog.golang.org/examples)；例子将在Godoc中显示出来。可运行的例子属于测试文件，而不属于用于生产环境的源文件。请看这个例子（[Godoc](https://pkg.go.dev/time#example-Duration), [source](https://cs.opensource.google/go/go/+/HEAD:src/time/example_test.go)）。

如果无法提供一个可运行的例子，也可以在代码注释中提供例子代码。与其他代码和命令行片段的注释一样，它应该遵循标准的格式化惯例。

### 具名返回值参数

在命名函数参数时，要考虑函数签名在Godoc中的呈现方式。函数本身的名称和返回值参数的类型通常足够清楚。

```
// Good:
func (n *Node) Parent1() *Node
func (n *Node) Parent2() (*Node, error)
```


如果一个函数返回两个或更多相同类型的参数，为返回值参数添加名称可能会很有用：

```
// Good:
func (n *Node) Children() (left, right *Node, err error)
```


如果调用者必须对特定的返回值参数采取行动，对它们的命名可以帮助提示行动是什么。

```
// Good:
// WithTimeout returns a context that will be canceled no later than d duration
// from now.
//
// The caller must arrange for the returned cancel function to be called when
// the context is no longer needed to prevent a resource leak.
func WithTimeout(parent Context, d time.Duration) (ctx Context, cancel func())
```


在上面的代码中，“取消”是一个调用者必须采取的特殊行动。然而，如果把结果参数单独写成（Context, func()），就会不清楚“取消函数”是什么意思。

当名称产生[不必要的重复](https://google.github.io/styleguide/go/decisions#repetitive-with-type)时，不要使用命名的返回值参数。

```
// Bad:
func (n *Node) Parent1() (node *Node)
func (n *Node) Parent2() (node *Node, err error)
```


不要为了避免在函数中声明一个变量而给返回值参数命名，这种做法收获的仅仅是很小的实现简洁性，但却会导致不必要的API冗长。

只有在小型函数中才可以[接受 裸返回(naked return)](https://go.dev/tour/basics/7)。一旦是一个中等规模的函数，就要显式地带着返回值一起返回。同样地，不要因为可以使用裸返回就给返回值参数命名。

[清晰性](https://google.github.io/styleguide/go/guide#clarity)总是比在你的函数中节省几行字更重要。

如果一个返回值参数的值必须在deferred闭包中改变，命名它则总是可以接受的。

```
提示：在函数签名中，类型往往比名称更清晰。GoTip #38：作为具名类型的函数 说明了这一点。
在上面的WithTimeout中，真正的代码在返回值参数列表中使用了CancelFunc而不是func()，这样做(译注：使用表意的类型)可以省下来很多编写文档的工作。
```


### 包注释

包的注释必须紧挨着package子句出现，在注释和包名之间没有空行。例如。

```
// Good:
// Package math provides basic constants and mathematical functions.
//
// This package does not guarantee bit-identical results across architectures.
package math
```


每个包必须有一个包的注释。如果一个包是由多个文件组成的，则其中一个文件应该有一个包注释。

main包的注释有一个稍微不同的形式，BUILD文件中go_binary规则的名称代替了包名。

```
// Good:
// The seed_generator command is a utility that generates a Finch seed file
// from a set of JSON study configs.
package main
```


只要二进制文件的名称与BUILD文件中写的一模一样，其他样式的注释也可以。当二进制名称是第一个词时，需要将其大写，即使它与命令行调用的拼写不严格一致。

```
// Good:
// Binary seed_generator ...
// Command seed_generator ...
// Program seed_generator ...
// The seed_generator command ...
// The seed_generator program ...
// Seed_generator ...
```


提示：

- 命令行调用和API使用的例子可以成为有用的文档。考虑Godoc的格式，请缩进包含代码的注释行。
- 如果没有明显的主文件，或者包的注释特别长，把文档注释单独放在一个名为doc.go的文件中，只写上注释和包声明句也是可以接受的。
- 可以用多行注释来代替多个单行注释。这有利于在源文件中对部分内容的复制和粘贴操作，比如二进制文件的命令行说明或模板示例。

```
// Good:
/*
The seed_generator command is a utility that generates a Finch seed file
from a set of JSON study configs.
seed_generator *.json | base64 > finch-seed.base64
*/
package template
```


- 为维护者准备的、适用于整个文件的注释，通常放在import声明语句的后面。这些注释不在Godoc中显示，不受上述包注释规则的约束。

## 导入

### 重命名导入包

import只应该在为避免与其他import的名称冲突时才进行重命名(一个推论是，[好的包名](https://google.github.io/styleguide/go/decisions#package-names)不应该需要重命名)。在名字冲突的情况下，最好对本地的或项目特定的包进行重命名。包的本地名称（别名）必须遵循[包命名的指导](https://google.github.io/styleguide/go/decisions#package-names)，包括禁止使用下划线和大写字母。

生成的protobuf协议包必须被重新命名，以去除其名称中的下划线，其别名必须有一个pb后缀。更多信息请参见[proto和stub的最佳实践](https://google.github.io/styleguide/go/best-practices#import-protos)。

```
// Good:
import (
fspb "path/to/package/foo_service_go_proto"
)
```


如果导入的软件包名称没有任何有用的标识信息（例如，package v1），应该将其重新命名为包括之前路径成分的名字。重命名必须与其他导入相同软件包的本地文件一致，包括版本号。

注意：最好是重命名包以符合[好的包名称](https://google.github.io/styleguide/go/decisions#package-names)，但这对于在vendor目录中的软件包往往是不可行的。

```
// Good:
import (
core "github.com/kubernetes/api/core/v1"
meta "github.com/kubernetes/apimachinery/pkg/apis/meta/v1beta1"
)
```


如果您需要导入一个包，其名称与你想使用的常见局部变量名称相冲突（例如 url, ssh），并且你希望重命名该包，首选的方法是使用pkg后缀（例如urlpkg）。注意，一个本地变量可以遮蔽一个包；但只有当这样的变量在同一范围内时，且该包仍然需要被使用时，这种重命名才是必要的。

### 分组导入

包应分为两组导入：

- 标准库包
- 其他包（项目和vendor包）

```
// Good:
package main
import (
"fmt"
"hash/adler32"
"os"
"github.com/dsnet/compress/flate"
"golang.org/x/text/encoding"
"google.golang.org/protobuf/proto"
foopb "myproj/foo/proto/proto"
_ "myproj/rpc/protocols/dial"
_ "myproj/security/auth/authhooks"
)
```


将项目包分成多个组是可以接受的，例如，如果你想为重命名的、只为副作用效果而导入的，或其他特殊的包单独设一个组。

```
// Good:
package main
import (
"fmt"
"hash/adler32"
"os"
"github.com/dsnet/compress/flate"
"golang.org/x/text/encoding"
"google.golang.org/protobuf/proto"
foopb "myproj/foo/proto/proto"
_ "myproj/rpc/protocols/dial"
_ "myproj/security/auth/authhooks"
)
```


注意: [goimports](https://google.github.io/styleguide/go/golang.org/x/tools/cmd/goimports)工具不支持维护在标准库和Google导入包之间强制分出的可选组。额外的导入子组需要作者和审核者的关注，以保证其符合要求。

同是AppEngine应用程序的Google程序应该有一个单独的AppEngine导入组。

Gofmt负责按导入路径对每个组进行排序。然而，它并不会自动将导入的内容分成组。goimports工具结合了Gofmt的功能和导入管理，根据上面的决定将导入包分离成组。让goimports全权负责管理包导入是ok的，但当一个文件被修改时，其导入列表必须保持内部一致。

### 空导入(import _)

只为其副作用而导入的包（使用 import _ “package” 语法）只能在main包中，或在需要它们的测试中导入。

这种包的一些例子包括：

[time/tzdataa](https://pkg.go.dev/time/tzdata)- 图像处理代码中的
[image/jpeg](https://pkg.go.dev/image/jpeg)

避免在library包中进行空导入，即使library间接依赖于它们。将副作用导入限制在main包中有助于控制依赖关系，并使编写依赖不同导入的测试成为可能，而不会产生冲突或浪费构建成本。

以下是这个规则的唯一例外：

**提示**：如果你在生产中创建了一个间接依赖副作用导入的library包，请写明预期的用法。

### import dot(import .)

“import .”形式是一种语言特性，它允许将从另一个包中导出的标识符带到当前的包中，而无需在使用它们时使用包限定符。更多信息请参见[语言规范](https://go.dev/ref/spec#Import_declarations)。

不要在谷歌代码库中使用这个功能特性；它使人们更难分辨功能的来源。

```
// Bad:
package foo_test
import (
"bar/testutil" // also imports "foo"
. "foo"
)
var myThing = Bar() // Bar defined in package foo; no qualification needed.
```


```
// Good:
package foo_test
import (
"bar/testutil" // also imports "foo"
"foo"
)
var myThing = foo.Bar()
```


## 错误

### 返回错误

使用error来表示一个函数可能失败。按照惯例，error应作为最后一个返回值参数。

```
// Good:
func Good() error { /* ... */ }
```


返回一个nil错误是提示成功操作的惯用方法，否则就代表失败。如果一个函数返回一个错误，调用者必须将所有非错误类型的返回值视为未指定的，除非有明确的文档说明。通常情况下，这些非错误类型的返回值是它们的零值，但这不能被假定。

```
// Good:
func GoodLookup() (*Result, error) {
// ...
if err != nil {
return nil, err
}
return res, nil
}
```


返回错误的导出函数应该使用error类型来返回它们。而使用具体的错误类型容易受到微妙的错误影响：一个具体的nil指针可以被包装成一个接口，从而成为一个非nil值（见[Go FAQ中关于这个主题的条目](https://golang.org/doc/faq#nil_error)）。

```
// Bad:
func Bad() *os.PathError { /*...*/ }
```


提示：一个接受context.Context参数的函数通常应该返回一个错误，以便调用者可以确定在函数运行时是否取消了context。

### 错误字符串

错误字符串不应大写（除非是以导出名称、专有名词或首字母缩略词开始），也不应以标点符号结束。这是因为错误字符串在打印给用户之前，通常出现在其他环境中。

```
// Bad:
err := fmt.Errorf("Something bad happened.")
```


```
// Good:
err := fmt.Errorf("something bad happened")
```


另一方面，完整显示的消息（日志、测试失败、API响应或其他用户界面）的风格视情况而定，但通常应该以大写开头。

```
// Good:
log.Infof("Operation aborted: %v", err)
log.Errorf("Operation aborted: %v", err)
t.Errorf("Op(%q) failed unexpectedly; err=%v", args, err)
```


### 错误处理

在代码中遇到错误时应该慎重选择如何处理它。通常情况下，使用“_”空变量来丢弃错误是不合适的。如果一个函数返回一个错误，请做以下其中一个：

- 立即处理并解决该错误。
- 将错误返回给调用者。
- 在特殊情况下，调用log.Fatal或（如果绝对必要）panic。

注意：log.Fatalf不是标准库中的日志。参见[#logging]。

在极少数情况下，忽略或丢弃一个错误是合适的（例如对(*bytes.Buffer).Write的调用被记录为永不失败），附带的注释应该解释为什么这是安全的。

```
// Good:
var b *bytes.Buffer
n, _ := b.Write(p) // never returns a non-nil error
```


关于错误处理的更多讨论和例子，请参见[《Effective Go》](http://golang.org/doc/effective_go.html#errors)和[最佳实践](https://google.github.io/styleguide/go/best-practices.html#error-handling)。

### 带内(in-band)错误

在C语言和类似语言中，函数通常会返回-1、null或空字符串等值，以示错误或丢失结果。这就是所谓的带内错误处理。

译注：所谓带内(in-band)是指将错误值与普通返回值混在一起。


```
// Bad:
// Lookup returns the value for key or -1 if there is no mapping for key.
func Lookup(key string) int
```


未能检查带内错误值会导致错误，并可能将错误归于出错的函数。

```
// Bad:
// The following line returns an error that Parse failed for the input value,
// whereas the failure was that there is no mapping for missingKey.
return Parse(Lookup(missingKey))
```


Go对多返回值的支持为此提供了一个更好的解决方案（见[Effective Go中关于多个返回值的部分](http://golang.org/doc/effective_go.html#multiple-returns)）。与其要求客户检查带内的错误值，一个函数应该返回一个额外的值来表明它的其他返回值是否有效。这个返回值可以是一个错误或在不需要解释时是一个布尔值，并且应该是最终的返回值。

```
// Good:
// Lookup returns the value for key or ok=false if there is no mapping for key.
func Lookup(key string) (value string, ok bool)
```


这个API可以防止调用者错误地将代码写成Parse(Lookup(key))，因为Lookup(key)有两个返回值，所以会导致编译错误。

以这种方式返回错误，可以鼓励更强大和明确的错误处理。

```
// Good:
value, ok := Lookup(key)
if !ok {
return fmt.Errorf("no value for %q", key)
}
return Parse(value)
```


一些标准库函数，如包strings中的函数，返回带内错误值。这大大简化了字符串处理代码，但代价是要求程序员更加勤奋。一般来说，Google代码库中的Go代码应该为错误返回额外的值。

### 缩进错误流程

在继续进行你的代码的其余部分之前，先处理错误。这可以提高代码的可读性，使读者能够迅速找到正常的路径。这个逻辑同样适用于任何测试一个条件是否为终止条件的代码块（例如，return、panic、log.Fatal）。

如果终止条件没有得到满足，后续运行的代码应该出现在if块之后，而不应该放入缩进的else子句中。

```
// Good:
if err != nil {
// error handling
return // or continue, etc.
}
// normal code
```


```
// Bad:
if err != nil {
// error handling
} else {
// normal code that looks abnormal due to indentation
}
```


提示：如果你在多行代码中使用了一个变量，通常不值得使用if-with-initializer风格。在这种情况下，通常最好将声明移出，使用标准的if语句。

```
// Good:
x, err := f()
if err != nil {
// error handling
return
}
// lots of code that uses x
// across multiple lines
// Bad:
if x, err := f(); err != nil {
// error handling
return
} else {
// lots of code that uses x
// across multiple lines
}
```


详情见Go技巧1：Line of Sight和[TotT：通过减少嵌套降低代码的复杂性](https://testing.googleblog.com/2017/06/code-health-reduce-nesting-reduce.html)。

## 语言

### 字面值格式

Go有一个非常强大的[复合字面值语法](https://go.dev/ref/spec#Composite_literals)，可以用一个表达式来表达深度嵌套的复杂值。在可能的情况下，应该使用这种字面值语法，而不是逐个字段地赋值。一般来说，gofmt对字面值的格式化是非常好的，但是还有一些额外的规则来保持这些字面值的可读性和可维护性。

#### 字段名

结构体字面值通常应该为当前包之外定义的类型指定字段名。

- 包括来自其他软件包的类型的字段名

```
// Good:
good := otherpkg.Type{A: 42}
```


结构体中字段的位置和字段的完整集合（当字段名被省略时，这两者都是有必要搞清楚的）通常不被认为是结构体的公共API的一部分；需要指定字段名以避免不必要的耦合。

```
// Bad:
// https://pkg.go.dev/encoding/csv#Reader
r := csv.Reader{',', '#', 4, false, false, false, false}
```


在小型、简单的结构体中可以省略字段名，这些结构体的组成和顺序都是稳定的，都有对应的文档记录。

```
// Good:
okay := image.Point{42, 54}
also := image.Point{X: 42, Y: 54}
```


- 对于包的本地类型，字段名可选

```
// Good:
okay := Type{42}
also := internalType{4, 2}
```


如果要使代码更清晰，还是应该使用字段名，而且这样做是非常普遍的。例如，一个有大量字段的结构体几乎都应该用字段名来初始化。

```
// Good:
okay := StructWithLotsOfFields{
field1: 1,
field2: "two",
field3: 3.14,
field4: true,
}
```


#### 匹配括号

一对大括号的最后一半应该总是应该出现在缩进量与开头的大括号相同的一行中。单行字面值也必须有这个属性。当字面值跨越多行时，保持这一属性可以使字面值的大括号匹配与函数和if语句等常见Go语法结构的大括号匹配相同。

这方面最常见的错误是在多行结构体字面值中把收尾括号和值放在同一行。在这种情况下，该行应以逗号结束，收尾括号应出现在下一行。

```
// Good:
good := []*Type{{Key: "value"}}
```


```
// Good:
good := []*Type{
{Key: "multi"},
{Key: "line"},
}
```


```
// Bad:
bad := []*Type{
{Key: "multi"},
{Key: "line"}}
```


```
// Bad:
bad := []*Type{
{
Key: "value"},
}
```


#### 拥抱式大括号

只有在以下两种情况下，才允许在切片和数组字面值的大括号之间丢弃空格（又称 “拥抱”）。

[缩进匹配](https://google.github.io/styleguide/go/decisions#literal-matching-braces)- 内部值也是字面值或proto构建器（即不是变量或其他表达式）。

```
// Good:
good := []*Type{
{ // Not cuddled
Field: "value",
},
{
Field: "value",
},
}
```


```
// Good:
good := []*Type{{ // Cuddled correctly
Field: "value",
}, {
Field: "value",
}}
```


```
// Good:
good := []*Type{
first, // Can't be cuddled
{Field: "second"},
}
```


```
// Good:
okay := []*pb.Type{pb.Type_builder{
Field: "first", // Proto Builders may be cuddled to save vertical space
}.Build(), pb.Type_builder{
Field: "second",
}.Build()}
```


```
// Bad:
bad := []*Type{
first,
{
Field: "second",
}}
```


#### 重复的类型名

重复的类型名可以从切片和map字面值中省略。这有助于减少混乱。明确的使用重复类型名的一个合理场合是当处理一个在你的项目中不常见的复杂类型时，当重复的类型名在相隔很远的行上时，可以提醒读者的上下文。

```
// Good:
good := []*Type{
{A: 42},
{A: 43},
}
```


```
// Bad:
repetitive := []*Type{
&Type{A: 42},
&Type{A: 43},
}
```


```
// Good:
good := map[Type1]*Type2{
{A: 1}: {B: 2},
{A: 3}: {B: 4},
}
```


```
// Bad:
repetitive := map[Type1]*Type2{
Type1{A: 1}: &Type2{B: 2},
Type1{A: 3}: &Type2{B: 4},
}
```


提示：如果你想删除结构体字面值中重复的类型名称，你可以运行gofmt -s。

#### 零值字段

当清晰度不会因此而降低时，零值字段可以从结构体字面值中省略。

设计良好的API经常采用零值结构来提高可读性。例如，从下面的结构体中省略三个零值字段，可以使人们将注意力集中到正在赋值的option字段上。

```
// Bad:
import (
"github.com/golang/leveldb"
"github.com/golang/leveldb/db"
)
ldb := leveldb.Open("/my/table", &db.Options{
BlockSize: 1<<16,
ErrorIfDBExists: true,
// These fields all have their zero values.
BlockRestartInterval: 0,
Comparer: nil,
Compression: nil,
FileSystem: nil,
FilterPolicy: nil,
MaxOpenFiles: 0,
WriteBufferSize: 0,
VerifyChecksums: false,
})
```


```
// Good:
import (
"github.com/golang/leveldb"
"github.com/golang/leveldb/db"
)
ldb := leveldb.Open("/my/table", &db.Options{
BlockSize: 1<<16,
ErrorIfDBExists: true,
})
```


表驱动测试中的结构体经常受益于[显式的字段名](https://google.github.io/styleguide/go/decisions#literal-field-names)，特别是当测试结构体十分重要的时候。这允许作者在有关字段与测试用例无关时完全省略零值字段。例如，成功的测试用例应该省略任何与错误相关或失败相关的字段。在零值对于理解测试用例是必要的情况下，如测试零或零输入，应指定字段名。

**简明**

```
tests := []struct {
input string
wantPieces []string
wantErr error
}{
{
input: "1.2.3.4",
wantPieces: []string{"1", "2", "3", "4"},
},
{
input: "hostname",
wantErr: ErrBadHostname,
},
}
```


**显式**

```
tests := []struct {
input string
wantIPv4 bool
wantIPv6 bool
wantErr bool
}{
{
input: "1.2.3.4",
wantIPv4: true,
wantIPv6: false,
},
{
input: "1:2::3:4",
wantIPv4: false,
wantIPv6: true,
},
{
input: "hostname",
wantIPv4: false,
wantIPv6: false,
wantErr: true,
},
}
```


### 空切片

在大多数情况下，nil和空切片之间没有功能上的区别。像len和cap这样的内置函数在nil切片上的表现与预期一致。

```
// Good:
import "fmt"
var s []int // nil
fmt.Println(s) // []
fmt.Println(len(s)) // 0
fmt.Println(cap(s)) // 0
for range s {...} // no-op
s = append(s, 42)
fmt.Println(s) // [42]
```


如果你声明一个空切片作为局部变量（特别是如果它可以成为返回值的来源），最好选择nil初始化以减少调用者的bug风险。

```
// Good:
var t []string
```


```
// Bad:
t := []string{}
```


不要创建强迫其客户区分nil和空切片的API：

```
// Good:
// Ping pings its targets.
// Returns hosts that successfully responded.
func Ping(hosts []string) ([]string, error) { ... }
```


```
// Bad:
// Ping pings its targets and returns a list of hosts
// that successfully responded. Can be empty if the input was empty.
// nil signifies that a system error occurred.
func Ping(hosts []string) []string { ... }
```


在设计接口时，要避免区分nil切片和非nil的零长度切片，因为这可能导致微妙的编程错误。这通常需要我们使用len来检查是否为空，而不是与nil比较来实现。

这个实现接受nil和零长度的切片作为”空”：

```
// Good:
// describeInts describes s with the given prefix, unless s is empty.
func describeInts(prefix string, s []int) {
if len(s) == 0 {
return
}
fmt.Println(prefix, s)
}
```


而不是依靠区别nil和零长度的切片来作为API的一部分：

```
// Bad:
func maybeInts() []int { /* ... */ }
// describeInts describes s with the given prefix; pass nil to skip completely.
func describeInts(prefix string, s []int) {
// The behavior of this function unintentionally changes depending on what
// maybeInts() returns in 'empty' cases (nil or []int{}).
if s == nil {
return
}
fmt.Println(prefix, s)
}
describeInts("Here are some ints:", maybeInts())
```


进一步讨论见[带内错误](https://google.github.io/styleguide/go/decisions#in-band-errors)。

### 缩进的混乱

避免引入断行，如果它将使其余的行与缩进的代码块对齐。如果这是不可避免的，请留出一个空格，将代码块中的代码与被包裹的行分开。

```
// Bad:
if longCondition1 && longCondition2 &&
// Conditions 3 and 4 have the same indentation as the code within the if.
longCondition3 && longCondition4 {
log.Info("all conditions met")
}
```


具体准则和例子见以下章节：

### 函数格式化

函数或方法声明的签名应该保持在一行，以避免缩进的混乱。

函数参数列表可能成为Go源文件中最长的几行。然而，它们在缩进的变化之前，因此很难以一种不使后续行看起来像函数体的一部分的混乱方式来断行。

```
// Bad:
func (r *SomeType) SomeLongFunctionName(foo1, foo2, foo3 string,
foo4, foo5, foo6 int) {
foo7 := bar(foo1)
// ...
}
```


参见[最佳实践](https://google.github.io/styleguide/go/best-practices#funcargs)，了解一些缩短函数调用的选项，否则这些函数会有很多参数。

```
// Good:
good := foo.Call(long, CallOptions{
Names: list,
Of: of,
The: parameters,
Func: all,
Args: on,
Now: separate,
Visible: lines,
})
```


```
// Bad:
bad := foo.Call(
long,
list,
of,
parameters,
all,
on,
separate,
lines,
)
```


通过析出局部变量，通常可以缩短行数。

```
// Good:
local := helper(some, parameters, here)
good := foo.Call(list, of, parameters, local)
```


同样地，函数和方法的调用也不应该仅仅根据行的长度来区分。

```
// Good:
good := foo.Call(long, list, of, parameters, all, on, one, line)
```


```
// Bad:
bad := foo.Call(long, list, of, parameters,
with, arbitrary, line, breaks)
```


不要给特定的函数参数添加注释。相反，使用选项结构或在函数文档中添加更多细节。

```
// Good:
good := server.New(ctx, server.Options{Port: 42})
```


```
// Bad:
bad := server.New(
ctx,
42, // Port
)
```


如果调用函数时的语句长得让人不舒服，请考虑重构。

```
// Good:
// Sometimes variadic arguments can be factored out
replacements := []string{
"from", "to", // related values can be formatted adjacent to one another
"source", "dest",
"original", "new",
}
// Use the replacement struct as inputs to NewReplacer.
replacer := strings.NewReplacer(replacements...)
```


如果不能改变API，或者本地不常调用（无论调用是否太长），如果有助于理解调用，添加换行符总是允许的。

```
// Good:
canvas.RenderCube(cube,
x0, y0, z0,
x0, y0, z1,
x0, y1, z0,
x0, y1, z1,
x1, y0, z0,
x1, y0, z1,
x1, y1, z0,
x1, y1, z1,
)
```


请注意，上述例子中的行没有在特定的列边界处被换行，而是根据坐标三要素进行分组。

在函数中的长字符串字数不应该因为行长的原因而被打断。对于包含此类字符串的函数，可以在字符串格式之后添加一个换行符，参数可以在下一行或后续行提供。关于断行的位置，最好是根据输入的语义分组来决定，而不是单纯地根据行的长度。

```
// Good:
log.Warningf("Database key (%q, %d, %q) incompatible in transaction started by (%q, %d, %q)",
currentCustomer, currentOffset, currentKey,
txCustomer, txOffset, txKey)
```


```
// Bad:
log.Warningf("Database key (%q, %d, %q) incompatible in"+
" transaction started by (%q, %d, %q)",
currentCustomer, currentOffset, currentKey, txCustomer,
txOffset, txKey)
```


### 条件与循环

一个if语句不应断行；多行if子句会导致缩进混乱。

```
// Bad:
// The second if statement is aligned with the code within the if block, causing
// indentation confusion.
if db.CurrentStatusIs(db.InTransaction) &&
db.ValuesEqual(db.TransactionKey(), row.Key()) {
return db.Errorf(db.TransactionError, "query failed: row (%v): key does not match transaction key", row)
}
```


如果不需要短路行为，可以直接提取布尔操作数：

```
// Good:
inTransaction := db.CurrentStatusIs(db.InTransaction)
keysMatch := db.ValuesEqual(db.TransactionKey(), row.Key())
if inTransaction && keysMatch {
return db.Error(db.TransactionError, "query failed: row (%v): key does not match transaction key", row)
}
```


也可能有其他的局部变量可以被提取出来，特别是如果条件已经是重复的。

```
// Good:
uid := user.GetUniqueUserID()
if db.UserIsAdmin(uid) || db.UserHasPermission(uid, perms.ViewServerConfig) || db.UserHasPermission(uid, perms.CreateGroup) {
// ...
}
```


```
// Bad:
if db.UserIsAdmin(user.GetUniqueUserID()) || db.UserHasPermission(user.GetUniqueUserID(), perms.ViewServerConfig) || db.UserHasPermission(user.GetUniqueUserID(), perms.CreateGroup) {
// ...
}
```


包含闭包或多行结构体字面值的if语句应确保大括号的匹配，以避免缩进的混乱。

```
// Good:
if err := db.RunInTransaction(func(tx *db.TX) error {
return tx.Execute(userUpdate, x, y, z)
}); err != nil {
return fmt.Errorf("user update failed: %s", err)
}
```


```
// Good:
if _, err := client.Update(ctx, &upb.UserUpdateRequest{
ID: userID,
User: user,
}); err != nil {
return fmt.Errorf("user update failed: %s", err)
}
```


同样地，不要试图在for语句中人为的插入换行。如果没有优雅的方法来重构它，你总是可以让这一行简单地变长。

```
// Good:
for i, max := 0, collection.Size(); i < max && !collection.HasPendingWriters(); i++ {
// ...
}
```


不过，往往是有方法的：

```
// Good:
for i, max := 0, collection.Size(); i < max; i++ {
if collection.HasPendingWriters() {
break
}
// ...
}
```


switch和case语句也应该保持在一行：

```
// Good:
switch good := db.TransactionStatus(); good {
case db.TransactionStarting, db.TransactionActive, db.TransactionWaiting:
// ...
case db.TransactionCommitted, db.NoTransaction:
// ...
default:
// ...
}
```


```
// Bad:
switch bad := db.TransactionStatus(); bad {
case db.TransactionStarting,
db.TransactionActive,
db.TransactionWaiting:
// ...
case db.TransactionCommitted,
db.NoTransaction:
// ...
default:
// ...
}
```


如果行过长，请缩进所有case，并用空行隔开，以避免缩进的混乱。

```
// Good:
switch db.TransactionStatus() {
case
db.TransactionStarting,
db.TransactionActive,
db.TransactionWaiting,
db.TransactionCommitted:
// ...
case db.NoTransaction:
// ...
default:
// ...
}
```


在将变量与常数进行比较的条件语句中，将变量值放在判等运算符的左侧：

```
// Good:
if result == "foo" {
// ...
}
```


而不是采用常量在先（”[尤达式条件语句](https://en.wikipedia.org/wiki/Yoda_conditions)“）。

```
// Bad:
if "foo" == result {
// ...
}
```


### 拷贝

为了避免意外的别名和类似的错误，在从其他包中复制结构体时要小心。例如，同步对象（如sync.Mutex）不能被复制。

bytes.Buffer类型包含一个[]byte切片，作为对小字符串的优化，该切片可以引用一个小的字节数组。如果你拷贝一个Buffer，拷贝中的切片可能会建立原始数组的别名，导致后续的方法调用产生意外的结果。

一般来说，如果一个T类型的值的方法与指针类型*T有关，就不要复制它。

```
// Bad:
b1 := bytes.Buffer{}
b2 := b1
```


调用一个值类型接收器的方法可以隐藏复制。当你编写API时，如果你的结构体包含不应该被复制的字段，你一般应该使用指针类型和返回指针类型。

下面这些是可以接受的。

```
// Good:
type Record struct {
buf bytes.Buffer
// other fields omitted
}
func New() *Record {...}
func (r *Record) Process(...) {...}
func Consumer(r *Record) {...}
```


但是如下这些通常是错误的：

```
// Bad:
type Record struct {
buf bytes.Buffer
// other fields omitted
}
func (r Record) Process(...) {...} // Makes a copy of r.buf
func Consumer(r Record) {...} // Makes a copy of r.buf
```


本指南也适用于复制sync.Mutex。

### 不要panic

不要在正常的错误处理中使用panic。相反，使用错误和多个返回值。参见[Effective Go中关于错误的部分](http://go.dev/doc/effective_go.html#errors)。

在main包和初始化代码中，考虑用log.Exit来处理应该终止程序的错误（例如，无效的配置），因为在许多这种情况下，堆栈跟踪不会帮助到读者。**请注意：log.Exit调用os.Exit，任何defer函数都不会被运行**。

对于表明”不可能”的条件的错误，即应该总是在代码审查和/或测试期间捕获的错误，一个函数可以合理地返回一个错误或调用log.Fatal。

注意：log.Fatalf不是标准库中的日志。参见[#logging]。

### Must函数

在失败时停止程序的辅助函数遵循命名惯例MustXYZ（或mustXYZ）。一般来说，它们应该只在程序启动初期被调用，而不是在像用户输入这样的事情上被调用，因为在这种情况下，正常的Go错误处理是首选。

这经常出现在专门在包初始化时调用的初始化包级变量的函数中（如template.Must和regexp.MustCompile）。

```
// Good:
func MustParse(version string) *Version {
v, err := Parse(version)
if err != nil {
log.Fatalf("MustParse(%q) = _, %v", version, err)
}
return v
}
// Package level "constant". If we wanted to use `Parse`, we would have had to
// set the value in `init`.
var DefaultVersion = MustParse("1.2.3")
```


注意：log.Fatalf不是标准库中的日志。参见[#logging]。

同样的约定可以用在只停止当前测试的测试helper函数中（使用t.Fatal）。这样的helper函数在创建测试值时往往很方便，例如在表驱动测试的结构体字段中，因为返回错误的函数不能直接赋值给结构体字段。

```
// Good:
func mustMarshalAny(t *testing.T, m proto.Message) *anypb.Any {
t.Helper()
any, err := anypb.New(m)
if err != nil {
t.Fatalf("MustMarshalAny(t, m) = %v; want %v", err, nil)
}
return any
}
func TestCreateObject(t *testing.T) {
tests := []struct{
desc string
data *anypb.Any
}{
{
desc: "my test case",
// Creating values directly within table driven test cases.
data: mustMarshalAny(t, mypb.Object{}),
},
// ...
}
// ...
}
```


在这两种情况下，这种模式的价值在于helper函数可以在”值”的上下文中被调用。这些helper函数不应该在难以确保错误被捕获的地方或在应该[检查错误](https://google.github.io/styleguide/go/decisions#handle-errors)的上下文中被调用（例如，在许多请求处理程序中）。对于常量输入，这让测试可以轻松确保Must参数是格式良好的，而对于非常量输入，它允许测试验证[错误可以被正确处理或传播](https://google.github.io/styleguide/go/best-practices#error-handling)。

在测试中使用Must函数时，它们通常应该被标记为[测试助手](https://google.github.io/styleguide/go/decisions#mark-test-helpers)，并在出错时调用t.Fatal（如果要了解更多，可参见测试助手中的[错误处理](https://google.github.io/styleguide/go/best-practices#test-helper-error-handling)）。

当[常规错误处理](https://google.github.io/styleguide/go/best-practices#error-handling)可行时（包括一些重构），Must函数就不应该被使用。

```
// Bad:
func Version(o *servicepb.Object) (*version.Version, error) {
// Return error instead of using Must functions.
v := version.MustParse(o.GetVersionString())
return dealiasVersion(v)
}
```


### goroutine的生命周期

当你创建新的goroutines时，要明确它们何时或是否会退出。

goroutine可能因阻塞在channel的发送或接收操作上而导致泄漏。垃圾收集器不会终止一个goroutine，即使阻塞它的channel已经是不可到达的了。

即使goroutine没有泄漏，当它们不再被需要时，让它们继续存活也会导致其他微妙的、难以诊断的问题。在一个已经关闭的channel上执行发送操作会导致panic。

```
// Bad:
ch := make(chan int)
ch <- 42
close(ch)
ch <- 13 // panic
```


在“不需要结果之后”修改仍在使用的输入，会导致数据竞争。让goroutine存活任意长的时间会导致不可预知的内存使用。

编写并发代码时应该明确goroutine的生命周期。通常情况下，这意味着将同步相关的代码限制在一个函数的范围内，并将逻辑分解到[同步函数](https://google.github.io/styleguide/go/decisions#synchronous-functions)中。如果并发性仍然不明显，那么记录下goroutine退出的时间和原因是很重要的。

遵循围绕Context使用的最佳实践的代码通常有助于明确这一点。传统上，它是用context.Context来管理的。

```
// Good:
func (w *Worker) Run(ctx context.Context) error {
// ...
for item := range w.q {
// process returns at latest when the context is cancelled.
go process(ctx, item)
}
// ...
}
```


以上还有其他变种，使用原始信号channel，如chan struct{}、同步变量、条件变量等。重要的是，goroutine的结束对后续维护者来说是显而易见的。

相比之下，下面的代码对其生成的goroutine的结束时间很不在意：

```
// Bad:
func (w *Worker) Run() {
// ...
for item := range w.q {
// process returns when it finishes, if ever, possibly not cleanly
// handling a state transition or termination of the Go program itself.
go process(item)
}
// ...
}
```


这段代码可能看起来很正常，但有几个潜在的问题：

- 这段代码在生产中可能有未定义的行为，程序可能不会干净地终止，即使操作系统释放了资源。
- 由于代码的生命周期不确定，该代码很难进行有意义的测试。
- 该代码可能会像上面描述的那样泄漏资源。

也请参见：

[不要在不知道如何停止的情况下启动一个goroutine](https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop)- 反思经典的并发模式：
[幻灯片](https://drive.google.com/file/d/1nPdvhB0PutEJzdCq5ms6UI58dp50fcAN/view)，[视频](https://www.youtube.com/watch?v=5zXAHh5tJqQ) [Go程序何时结束](https://changelog.com/gotime/165)

### 接口

Go接口类型定义一般放在使用接口类型值的包中(如下面示例中的consumer包)，而不是实现接口类型的包中。实现包应该返回具体的（通常是指针或结构体）类型。这样一来，新的方法可以被添加到实现中，而不需要大量的重构。参见[GoTip #49: 接受接口，返回具体类型](https://google.github.io/styleguide/go/index.html#gotip)以了解更多细节。

不要从消费接口的API中导出接口的[测试替身](https://abseil.io/resources/swe-book/html/ch13.html#techniques_for_using_test_doubles)实现。相反，设计API，使其可以使用真正实现的公共API进行测试。请参阅[GoTip #42: 授权测试存根](https://google.github.io/styleguide/go/index.html#gotip)以了解更多细节。即使使用真实实现不可行，也没有必要引入一个完全覆盖真实类型中所有方法的接口；消费者可以创建一个只包含它所需要的方法的接口，正如[GoTip #78: 最小可行接口](https://google.github.io/styleguide/go/index.html#gotip)中所展示的。

要测试使用Stubby RPC客户端的包，请使用真实的客户端连接。如果在测试中不能运行真正的服务器，Google的内部做法是使用内部的rpctest包（即将推出！）获得一个真正的客户端连接到本地[测试替身]。

在使用之前不要定义接口（见[TotT: Code Health: Eliminate YAGNI Smells](https://testing.googleblog.com/2017/08/code-health-eliminate-yagni-smells.html) ）。如果没有一个真实的使用例子，就很难看出一个接口是否有必要，更不用说它应该包含哪些方法。

如果包的用户不需要为它们传递不同类型的参数，就不要使用接口类型的参数。

不要导出包用户不需要的接口。

TODO: 写一份关于接口的更深入的文档，并在此链接。

```
// Good:
package consumer // consumer.go
type Thinger interface { Thing() bool }
func Foo(t Thinger) string { ... }
```


```
// Good:
package consumer // consumer_test.go
type fakeThinger struct{ ... }
func (t fakeThinger) Thing() bool { ... }
...
if Foo(fakeThinger{...}) == "x" { ... }
```


```
// Bad:
package producer
type Thinger interface { Thing() bool }
type defaultThinger struct{ ... }
func (t defaultThinger) Thing() bool { ... }
func NewThinger() Thinger { return defaultThinger{ ... } }
```


```
// Good:
package producer
type Thinger struct{ ... }
func (t Thinger) Thing() bool { ... }
func NewThinger() Thinger { return Thinger{ ... } }
```


### 泛型

在满足你的业务需求时，泛型（正式名称是[“类型参数”](https://go.dev/design/43651-type-parameters)是允许被使用的。在许多应用中，使用现有的语言特性（切片、map、接口等）的传统方法也能很好地工作，并且不会增加复杂性，所以要警惕过早地使用泛型。见关于[最小机制](https://google.github.io/styleguide/go/guide#least-mechanism)的讨论。

当引入一个使用泛型的导出API时，要确保它有适当的文档。强烈建议包括可运行的[例子](https://google.github.io/styleguide/go/decisions#examples)。

不要因为你正在实现一个不关心其成员元素类型的算法或数据结构，就使用泛型。如果在实践中只有一种类型被实例化，那就从让你的代码从让这种类型可以工作开始，而完全不需要使用泛型。与删除那些被认为是不必要的抽象相比，以后再添加多态性将更为直接。

不要使用泛型来发明领域特定语言（DSL）。特别是，不要引入可能给读者带来巨大负担的错误处理框架。相反，应该选择既定的[错误处理实践](https://google.github.io/styleguide/go/decisions#errors)。对于测试，要特别警惕引入[断言库](https://google.github.io/styleguide/go/decisions#assert)或框架，因为它们会导致不太有用的[测试失败](https://google.github.io/styleguide/go/decisions#useful-test-failures)。

一般来说：

[写代码，不要设计类型](https://www.youtube.com/watch?v=Pa_e9EeCdy8&t=1250s)。来自Robert Griesemer和Ian Lance Taylor的GopherCon演讲。- 如果你有几个类型共享一个有用的统一接口，可以考虑使用该接口对解决方案进行建模。可能不需要泛型。
- 否则，与其依赖任何类型和过度的类型转换，不如考虑泛型。

也请参见。

### 传值

不要仅仅为了节省几个字节而把指针作为函数参数传递。如果一个函数自始至终只是以*x的形式对它的参数x进行了读操作，那么这个参数就不应该被设计成一个指针。常见的例子包括传递一个字符串的指针（*string）或一个接口值的指针（*io.Reader）。在这两种情况下，值本身是一个固定的大小，可以直接传递。

译注：string类型是一个二元组，接口类型也是一个二元组，它们都是固定大小的。


这个建议并不适用于大型结构体，甚至是可能增大的小型结构体。特别是，protocol buffer消息一般应通过指针而不是值来处理。指针类型满足proto.Message接口（由proto.Marshal、protocmp.Transform等接受），而protocol buffer消息可能相当大，并且经常随着时间的推移而变大。

### Receiver类型

一个[方法接收器(Receiver)](https://go.dev/ref/spec#Method_declarations)可以作为一个值或者一个指针来传递，就像它是一个普通的函数参数一样。选择哪种方式应该基于该方法应该是哪一个（几个）[方法集合](https://golang.org/ref/spec#Method_sets)的一部分。

**正确性胜过速度或简单性**。有些情况下，你必须使用一个指针值。在其他情况下，如果你对代码的发展没有很好的认识，可以为大的类型选择指针，或者作为对未来的保护，而对[简单的普通数据](https://en.wikipedia.org/wiki/Passive_data_structure)使用值类型。

下面的列表进一步详细说明了每种情况：

- 如果接收器是一个切片，并且该方法没有做reslice操作或重新分配切片，则使用一个值而不是一个指针。

```
// Good:
type Buffer []byte
func (b Buffer) Len() int { return len(b) }
```


- 如果方法需要修改receiver参数，那么receiver必须用指针类型

```
// Good:
type Counter int
func (c *Counter) Inc() { *c++ }
// See https://pkg.go.dev/container/heap.
type Queue []Item
func (q *Queue) Push(x Item) { *q = append([]Item{x}, *q...) }
```


- 如果receiver是一个包含不能安全复制的字段的结构体，请使用一个指针类型receiver。常见的例子是sync.Mutex和其他同步类型。

```
// Good:
type Counter struct {
mu sync.Mutex
total int
}
func (c *Counter) Inc() {
c.mu.Lock()
defer c.mu.Unlock()
c.total++
}
```


提示：检查该类型的Godoc，了解它是否可以安全地复制。

-
如果receiver是一个”大”结构体或数组，指针类型接收器可能更有效率。传递一个结构体相当于把它的所有字段或元素作为参数传递给方法。如果这看起来太大，无法通过数值传递，那么指针是一个不错的选择。

-
对于将调用或与其他修改receiver的函数并发运行的方法，如果这些修改不应该对你的方法可见，则使用一个值；否则使用一个指针。

-
如果receiver是一个结构体或数组，其任何元素都是指向可能被修改的东西的指针，那么最好使用指针类型接收器，以使读者清楚地了解可修改的意图。


```
// Good:
type Counter struct {
m *Metric
}
func (c *Counter) Inc() {
c.m.Add(1)
}
```


- 如果接收器是一个Go内置的类型，如整数或字符串，不需要被修改，则使用一个值类型。

```
// Good:
type User string
func (u User) String() { return string(u) }
```


- 如果接收器是一个map、函数或channel，使用一个值而不是一个指针。

```
// Good:
// See https://pkg.go.dev/net/http#Header.
type Header map[string][]string
func (h Header) Add(key, value string) { /* omitted */ }
```


- 如果接收器是一个”小”数组或结构体，并且元素是没有可变字段和指针的值类型，值类型接收器通常是正确的选择。

```
// Good:
// See https://pkg.go.dev/time#Time.
type Time struct { /* omitted */ }
func (t Time) Add(d Duration) Time { /* omitted */ }
```


- 如果不确定，那就使用指针类型receiver

作为一般的指导原则，最好使一个类型的方法要么所有都是指针方法，要么所有都是值方法。

注意：关于向函数传递值或指针是否会影响性能，有很多错误的信息。编译器可以选择向堆栈中的值传递指针以及复制堆栈中的值，但在大多数情况下，这些考虑的优先级不应该超过代码的可读性和正确性。当性能确实重要时，在决定一种方法优于另一种方法之前，用一个实际的基准测试对两种方法进行分析是很重要的。

### switch和break

不要在switch子句的末尾使用没有目标标签的break语句，它们是多余的。与C和Java不同，Go中的switch子句会自动跳出，我们需要显式使用fallthrough语句来实现C风格的行为。如果你想澄清一个空case子句的目的，请使用注释而不是break。

```
// Good:
switch x {
case "A", "B":
buf.WriteString(x)
case "C":
// handled outside of the switch statement
default:
return fmt.Errorf("unknown value: %q", x)
}
```


```
// Bad:
switch x {
case "A", "B":
buf.WriteString(x)
break // this break is redundant
case "C":
break // this break is redundant
default:
return fmt.Errorf("unknown value: %q", x)
}
```


注意：如果switch子句位于for循环中，在switch中使用break并不能退出外围的for循环。

```
for {
switch x {
case "A":
break // exits the switch, not the loop
}
}
```


为了跳出外围的循环，请在for语句上使用一个标签。

```
loop:
for {
switch x {
case "A":
break loop // exits the loop
}
}
```


### 同步函数

同步函数直接返回其结果，并在返回前完成所有回调或channel操作。比起异步函数，我们更喜欢同步函数。

同步函数在调用中保持goroutines的本地化。这有助于推断它们的生命周期，并避免泄漏和数据竞争。同步函数也更容易测试，因为调用者可以传递一个输入并检查输出，而不需要轮询或使用同步原语。

如果有必要，调用者可以通过在一个单独的goroutine中调用该函数来增加并发性。然而，在调用者一方删除不必要的并发是相当困难的（有时是不可能的）。

### 类型别名

使用类型定义：type T1 T2 来定义一个新的类型。使用[类型别名](http://go.dev/ref/spec#Type_declarations)：type T1 = T2 来引用一个现有的类型，而不用定义一个新的类型。类型别名是罕见的；它们的主要用途是帮助软件包迁移到新的源代码位置。在不需要时不要使用类型别名。

### 使用%q

Go的格式函数（fmt.Printf等）有一个%q的动词，可以打印双引号内的字符串。

```
// Good:
fmt.Printf("value %q looks like English text", someText)
```


尽量使用%q，而不是使用%s来手动操作：

```
// Bad:
fmt.Printf("value \"%s\" looks like English text", someText)
// Avoid manually wrapping strings with single-quotes too:
fmt.Printf("value '%s' looks like English text", someText)
```


当输入值可能为空或包含控制字符时，建议在面向人类的输出中使用%q。很难注意到一个空字符串，但%q输出的”"会很明显地表现出来。

### 使用any

Go 1.18引入了一个any类型作为interface{}的别名。因为它是一个别名，所以any在很多情况下等同于interface{}，而在其他情况下，它可以通过显式转换轻松地进行互换。倾向于在新代码中使用any。

## 常用库

### Flags

Google代码库中的Go程序使用标准库flag包的内部变体。它有一个和标准库flag包相似的接口，但与谷歌内部系统有更为良好的互操作性。Go二进制文件中的标志名称应该倾向于使用下划线来分隔单词，不过保存标志值的变量应该遵循标准的Go名称风格（驼峰命名）。具体来说，标志名应该使用蛇形命名，而变量名应该是驼峰命名的对应名称。

```
// Good:
var (
pollInterval = flag.Duration("poll_interval", time.Minute, "Interval to use for polling.")
)
```


```
// Bad:
var (
poll_interval = flag.Int("pollIntervalSeconds", 60, "Interval to use for polling in seconds.")
)
```


flag必须只在main包或等价包中定义。

通用包应该使用Go的API来配置，而不是通过命令行接口来配置；不要在导入一个库时附带导出新的标志的副作用。也就是说，最好是使用明确的函数参数或结构体字段赋值，或者在最严格的审查下，不那么频繁地导出全局变量。在极其罕见的情况下，如果有必要打破这一规则，标志的名称必须明确指出它所配置的包。

如果你的标志是全局变量，请将它们放在自己的var组中，遵循导入部分。

围绕创建带有子命令的复杂CLI的最佳实践，还有一些讨论。

也请参见：

- [Tip of the Week #45: Avoid Flags, Especially in Library Code][totw-45]
[Go Tip #10: Configuration Structs and Flags](https://google.github.io/styleguide/go/index.html#gotip)[Go Tip #80: Dependency Injection Principles](https://google.github.io/styleguide/go/index.html#gotip)

### 日志包

Google代码库中的Go程序使用了标准库日志包的一个变种。它有一个类似的但更强大的接口，并能与谷歌内部系统很好地互操作。这个库的开源版本是作为软件包[glog](https://pkg.go.dev/github.com/golang/glog)提供的，开源的Google项目可以使用它，但本指南自始至终将其称为log。

注意：对于异常的程序退出，这个库使用log.Fatal来终止，并有堆栈跟踪，使用log.Exit来停止，没有堆栈跟踪。没有像标准库中的log.Panic函数。

提示：log.Info(v)等同于log.Infof(“%v”, v)，对于其他日志级别也是如此。当你没有格式化工作时，更倾向于非格式化版本。

另请参见：

- 关于
[记录错误](https://google.github.io/styleguide/go/best-practices#error-logging)和[自定义verbosily级别](https://google.github.io/styleguide/go/best-practices#vlog)的最佳实践 - 何时以及如何使用日志包来
[停止程序](https://google.github.io/styleguide/go/best-practices#checks-and-panics)

### Contexts

context.Context类型的值携带安全凭证、跟踪信息、截止日期和取消信号，跨越API和进程边界。与C++和Java在Google代码库中使用线程本地存储不同，Go程序在整个函数调用链中明确地传递上下文，从传入的RPC和HTTP请求到传出的请求。

当被传递到一个函数或方法时，context.Context总是作为第一个参数。

```
func F(ctx context.Context /* other arguments */) {}
```


例外情况是：

- 在HTTP处理程序中，其上下文来自req.Context()。
- 在流式RPC方法中，上下文来自于流。

使用gRPC流的代码从生成的服务器类型中的Context()方法访问上下文，该类型实现了grpc.ServerStream。参见[gRPC生成的代码文档](https://grpc.io/docs/languages/go/generated-code/)。

- 在入口函数中（此类函数的例子见下文），使用context.background()。
- 在二进制目标中：main
- 在通用代码和库中：init
- 在测试中：TestXXX, BenchmarkXXX, FuzzXXX


```
注意：在调用链中间的代码需要使用context.background()来创建自己的基础上下文，这非常罕见。总是优先从你的调用者那里获取一个上下文，除非它是错误的上下文。
你可能会遇到一些服务器库（Stubby、gRPC或Google的Go服务器框架中的HTTP的实现），它们为每个请求构建一个新的上下文对象。这些上下文被立即填充了来自传入请求的信息，因此当传递给请求处理程序时，上下文的附加值已经从客户端调用者那里通过网络边界传播给了它。此外，这些上下文的生命期与请求的生命期是一致的：当请求完成时，上下文就被取消了。
除非你正在实现一个服务器框架，否则你不应该在库代码中用context.Background()创建上下文。相反，如果有一个现有的上下文可用的话，最好使用下面提到的context detachment。如果你认为你确实需要入口函数之外的context.Background()，请在承诺实现之前使用Google Go风格邮件列表讨论。
```


在函数中context.Context优先的惯例也适用于测试helper。

```
// Good:
func readTestFile(ctx context.Context, t *testing.T, path string) string {}
```


不要给结构体类型添加上下文成员。相反，在需要传递上下文的类型上的每个方法中添加一个上下文参数。唯一的例外是那些签名必须与标准库或谷歌控制之外的第三方库中的接口匹配的方法。这种情况非常罕见，应该在实施和可读性审查之前使用Google Go风格邮件列表讨论。

谷歌代码库中必须催生后台操作的代码，这些后台操作可以在父级上下文被取消后运行，可以使用内部包进行分离。请关注[问题#40221](https://github.com/golang/go/issues/40221)，了解关于开源替代方案的讨论。

由于上下文是不可改变的，因此可以将同一个上下文传递给共享相同的deadline、取消信号、凭证、父级跟踪等的多个调用。

也请参见：

#### 自定义上下文

不要创建自定义的上下文类型，也不要在函数签名中使用上下文以外的接口。这条规则没有例外。

想象一下，如果每个团队都有一个自定义的上下文。每个从包P到包Q的函数调用都必须确定如何将PContext转换为QContext，对于所有的包P和Q对来说都是不切实际的，而且容易出错，这使得增加上下文参数的自动化重构几乎不可能。

如果你有应用数据需要传递，请把它放在一个参数中，放在接收器中，放在globals中，或者放在Context值中，如果它真的属于那里。创建自己的Context类型是不可接受的，因为它破坏了Go团队使Go程序在生产中正常工作的能力。

### crypto/rand

不要使用软件包math/rand来生成key，即使是丢弃的key。如果不加种子，生成器是完全可预测的。用time.Nanoseconds()做种子，就只有几个比特的熵了。相反，如果你需要文本，打印成十六进制或base64，请使用crypto/rand的Reader。

```
// Good:
import (
"crypto/rand"
// "encoding/base64"
// "encoding/hex"
"fmt"
// ...
)
func Key() string {
buf := make([]byte, 16)
if _, err := rand.Read(buf); err != nil {
log.Fatalf("Out of randomness, should never happen: %v", err)
}
return fmt.Sprintf("%x", buf)
// or hex.EncodeToString(buf)
// or base64.StdEncoding.EncodeToString(buf)
}
```


注意：log.Fatalf不是标准库中的日志。参见[#logging]。

## 有用的测试失败

不需要阅读测试的源代码就可以诊断出测试的失败。测试失败时应该有有用的信息详细说明。

- 是什么导致了失败
- 哪些输入导致了错误
- 实际结果
- 预期结果是什么

以下是实现这一目标的具体约定。

### 断言库

不要创建 “断言库 “作为测试的辅助工具。

断言库是试图在测试中结合验证和生产失败信息的库（尽管同样的陷阱也可以适用于其他测试助手）。关于测试助手和断言库之间的区别的更多信息，请参见[最佳实践](https://google.github.io/styleguide/go/best-practices#test-functions)。

```
// Bad:
var obj BlogPost
assert.IsNotNil(t, "obj", obj)
assert.StringEq(t, "obj.Type", obj.Type, "blogPost")
assert.IntEq(t, "obj.Comments", obj.Comments, 2)
assert.StringNotEq(t, "obj.Body", obj.Body, "")
```


断言库往往要么提前停止测试（如果断言调用t.Fatalf或panic），要么省略关于测试正确的相关信息。

```
// Bad:
package assert
func IsNotNil(t *testing.T, name string, val interface{}) {
if val == nil {
t.Fatalf("data %s = nil, want not nil", name)
}
}
func StringEq(t *testing.T, name, got, want string) {
if got != want {
t.Fatalf("data %s = %q, want %q", name, got, want)
}
}
```


复杂的断言函数通常不提供[有用的失败信息](https://google.github.io/styleguide/go/decisions#useful-test-failures)和存在于测试函数中的上下文。太多的断言函数和库会导致开发人员的经验碎片化：我应该使用哪个断言库，它应该发出什么风格的输出格式，等等。碎片化产生了不必要的混乱，特别是对于库的维护者和大规模修改的作者，他们负责修复潜在的下游故障。与其创建一个特定领域的测试语言，不如使用Go本身。

断言库通常会把比较和相等性检查的因素排除在外。尽量使用标准库，如[cmp](https://pkg.go.dev/github.com/google/go-cmp/cmp)和fmt来代替。

```
// Good:
var got BlogPost
want := BlogPost{
Comments: 2,
Body: "Hello, world!",
}
if !cmp.Equal(got, want) {
t.Errorf("blog post = %v, want = %v", got, want)
}
```


对于更多特定领域的比较帮助器，倾向于返回一个值或一个可以在测试的失败消息中使用的错误，而不是传递*testing.T并调用其错误报告方法。

```
// Good:
func postLength(p BlogPost) int { return len(p.Body) }
func TestBlogPost_VeritableRant(t *testing.T) {
post := BlogPost{Body: "I am Gunnery Sergeant Hartman, your senior drill instructor."}
if got, want := postLength(post), 60; got != want {
t.Errorf("length of post = %v, want %v", got, want)
}
}
```


最佳实践：如果postLength是非琐碎的，那么直接测试它是有意义的，独立于任何使用它的测试。

另见：

### 识别函数

在大多数测试中，失败信息应该包括失败的函数名称，即使它从测试函数的名称中看起来很明显。具体来说，你的失败信息应该是“YourFunc(%v) = %v, want %v”，而不是仅仅“got %v, want %v”。

### 识别输入

在大多数测试中，如果函数输入很短，失败信息应该包括函数输入。如果输入的相关属性不明显（例如，因为输入很大或不透明），你应该在测试用例的名称中加入被测试内容的描述，并将该描述作为错误信息的一部分打印出来。

### got在want之前

测试输出应该包括函数返回的实际值，然后再打印预期的值。打印测试输出的标准格式是“YourFunc(%v) = %v, want %v”。在你写”actual”和”expected”的地方，最好分别使用”got “和”want”。

对于差异来说，方向性不那么明显，因此，重要的是包括一个键来帮助解释失败。参见[打印差异的章节](https://google.github.io/styleguide/go/decisions#print-diffs)。无论你在故障信息中使用哪种差异顺序，你都应该明确指出它是故障信息的一部分，因为现有的代码在顺序上是不一致的。

### 结构体整体比较

如果你的函数返回一个结构体（或任何有多个字段的数据类型，如切片、数组和map），避免编写测试代码，对结构体进行手工编码的逐字段比较。相反，构建你期望你的函数返回的数据，并直接使用[深度比较法](https://google.github.io/styleguide/go/decisions#types-of-equality)进行比较。

注意：如果您的数据包含不相关的字段，从而掩盖了测试的意图，那么这一点就不适用了。

如果你的结构体需要进行近似（或同等种类的语义）的相等性比较，或者它包含不能进行相等性比较的字段（例如，如果其中一个字段是io.Reader），用[cmpopts](https://pkg.go.dev/github.com/google/go-cmp/cmp/cmpopts)选项（如cmpopts.IgnoreInterfaces）调整[cmp.Diff](https://pkg.go.dev/github.com/google/go-cmp/cmp/cmp#Diff)或cmp.Equal比较可能满足你的需要（示例）。

如果你的函数返回多个返回值，你不需要在比较之前将这些返回值包裹在一个结构中。只需单独比较返回值并打印它们：

```
// Good:
val, multi, tail, err := strconv.UnquoteChar(`\"Fran & Freddie's Diner\"`, '"')
if err != nil {
t.Fatalf(...)
}
if val != `"` {
t.Errorf(...)
}
if multi {
t.Errorf(...)
}
if tail != `Fran & Freddie's Diner"` {
t.Errorf(...)
}
```


### 比较稳定的结果

避免比较可能依赖于你不拥有的包的输出稳定性的结果。相反，测试应该在语义相关的信息上进行比较，这些信息是稳定的，可以抵抗依赖关系的变化。对于返回格式化字符串或序列化字节的功能，一般来说，假设输出是稳定的并不安全。

例如，json.Marshal可以改变（而且在过去已经改变过）它所产生的特定字节。如果json包改变了它序列化字节的方式，在JSON字符串上执行字符串相等的测试可能会失败。相反，一个更健壮的测试将解析JSON字符串的内容，并确保它在语义上等同于一些预期的数据结构。

### 持续进行

测试应该尽可能地持续下去，即使在失败之后，以便在一次测试运行中打印出所有失败的检查。这样一来，正在修复失败测试的开发者就不必在修复每个错误后重新运行测试来发现下一个错误。

更倾向于调用t.Error而不是t.Fatal来报告一个不匹配。当比较一个函数输出的几个不同属性时，对每一个比较都使用t.Error。

调用t.Fatal主要用于报告一个意外的错误情况，当后续的比较失败不会有什么意义时。

对于表驱动的测试，考虑使用子测试(subtests)，使用t.Fatal而不是t.Error和continue。参见[GoTip #25: Subtests: 让你的测试更精简](https://google.github.io/styleguide/go/index.html#gotip)。

最佳实践：关于什么时候应该使用t.Fatal的更多讨论，见[最佳实践](https://google.github.io/styleguide/go/best-practices#t-fatal)。

### 相等性比较和差异

“==”操作符使用[语言定义的比较法](http://go.dev/ref/spec#Comparison_operators)来评估相等性。标量值（数字、布尔运算等）根据其值进行比较，但只有一些结构和接口可以用这种方式进行比较。指针的比较是基于它们是否指向同一个变量，而不是基于它们所指向的值是否相等。

[cmp包](https://pkg.go.dev/github.com/google/go-cmp/cmp)可以比较不适合由==处理的更复杂的数据结构，例如切片。使用cmp.Equal来进行相等性比较，使用cmp.Diff来获得对象之间可供人类阅读的差异。

```
// Good:
want := &Doc{
Type: "blogPost",
Comments: 2,
Body: "This is the post body.",
Authors: []string{"isaac", "albert", "emmy"},
}
if !cmp.Equal(got, want) {
t.Errorf("AddPost() = %+v, want %+v", got, want)
}
```


虽然cmp包不是Go标准库的一部分，但它是由Go团队维护的，随着时间的推移应该会产生稳定的相等性结果。它是用户可配置的，应该可以满足大多数的比较需求。

现有的代码可能会使用以下较早的库，并且可以继续使用它们以保持一致性。

[pretty](https://pkg.go.dev/github.com/kylelemons/godebug/pretty)产生美观的差异报告。然而，它非常谨慎地认为具有相同视觉表现的值是相等的。特别是，pretty不捕捉nil切片和空切片之间的差异，对具有相同字段的不同接口实现不敏感，并且可以使用嵌套map作为与结构值比较的基础。在产生差异之前，它还会将整个值序列化为一个字符串，因此对于比较大的值来说不是一个好的选择。默认情况下，它比较的是未导出的字段，这使得它对你的依赖关系中实现细节的变化很敏感。出于这个原因，在protobuf信息上使用pretty是不合适的。

在新的代码中更倾向于使用cmp，值得考虑更新旧的代码，以便在实际情况下使用cmp。

旧的代码可能使用标准库reflect.DeepEqual函数来比较复杂的结构。reflect.DeepEqual不应该被用来检查相等性，因为它对未导出的字段和其他实现细节的变化很敏感。使用reflect.DeepEqual的代码应该更新为上述库中的一个。

注意：cmp包是为测试而设计的，而不是为生产使用。因此，当它怀疑一个比较被错误地执行时，它可能会panic，以向用户提供关于如何改进测试以减少脆性的指导。鉴于cmp具有报panic的倾向，它不适合在生产中使用的代码，因为虚假的panic可能是致命的。

### 详细程度

传统的失败信息是“YourFunc(%v) = %v, want %v”，适用于大多数Go测试。然而，有些情况下可能需要更多或更少的细节：

- 进行复杂交互的测试也应该描述交互。例如，如果同一个YourFunc被调用了好几次，要确定哪个调用没有通过测试。如果知道系统的任何额外状态是很重要的，那么在失败输出中包括这些（或者至少在日志中）。
- 如果数据是一个复杂的结构，有大量的模板，在消息中只描述重要的部分是可以接受的，但不要过分地掩盖数据。
- 设置失败不需要同样水平的细节。如果一个测试助手填充了一个Spanner表，但Spanner是关闭的，你可能不需要包括你要存储在数据库中的测试输入。t.Fatalf(“Setup: Failed to set up test database: %s”, err)通常足以帮助解决这个问题。

提示：在开发过程中触发你的失败模式。审查失败信息是什么样子的，维护者是否能有效地处理失败。

有一些技术可以清晰地再现测试输入和输出。

- 当打印字符串数据时，%q通常是有用的，可以强调该值的重要性，并更容易发现坏值。
- 当打印（小）结构时，%+v可能比%v更有用。
- 当验证较大的数值失败时，打印一个差异可以使人们更容易理解失败的原因。

### 打印差异

如果你的函数返回大量的输出，那么当你的测试失败时，阅读失败信息的人很难发现其中的差异。与其同时打印返回值和想要的值，不如做一个差异。

要计算这些值的差异，首选cmp.Diff，特别是对于新的测试和新的代码，但也可以使用其他工具。关于每个函数的优势和劣势的指导，请看类型的相等性。

你可以使用diff包来比较多行字符串或字符串的列表。你可以把它作为其他类型的差异的构建模块。

在你的失败信息中添加一些文字，解释差异的方向。

- 当你使用cmp、pretty和diff包时，类似diff(-want +got)的东西很好（如果你向函数传递(want, got)），因为你添加到格式字符串中的-和+将与实际出现在diff行开头的-和+相匹配。如果你把(got, want)传给你的函数，正确的键将是(-got +want)。
- messagediff包使用不同的输出格式，所以当你使用它时，消息diff（want -> got）是合适的（如果你向函数传递（want，got）），因为箭头的方向将与”修改”行中的箭头方向一致。

diff将跨越多行，所以你应该在打印diff之前打印一个新行。

### 测试错误语义

当一个单元测试执行字符串比较或使用cmp包来检查针对特定输入返回的特定类型的错误时，你可能会发现，如果这些错误信息中的任何一个在未来被重新措辞，你的测试将是脆弱的。因为这有可能把你的单元测试变成一个变化检测器（[见TotT: Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html) ），所以不要使用字符串比较来检查你的函数返回什么类型的错误。然而，允许使用字符串比较来检查来自被测包的错误信息是否满足某些属性，例如，它是否包括参数名称。

Go中的错误值通常有一个用于人眼的部分和一个用于语义控制流的部分。测试应该设法只测试可以可靠地观察到的语义信息，而不是显示用于人类调试的信息，因为这通常会在未来发生变化。关于构建具有语义的错误的指导，请参见[有关错误的最佳实践](https://google.github.io/styleguide/go/best-practices#error-handling)。如果来自于你控制之外的依赖关系的错误的语义信息不充分，请考虑向所有者提交一个错误，以帮助改进API，而不是依靠解析错误信息。

在单元测试中，通常只关心一个错误是否发生。如果是这样，那么在你预期发生错误时，只测试错误是否为非零就足够了。如果你想测试错误在语义上是否与其他错误匹配，那么可以考虑使用cmp与[cmpopts.EquateErrors](https://pkg.go.dev/github.com/google/go-cmp/cmp/cmpopts#EquateErrors)。

注意：如果一个测试使用了cmpopts.EquateErrors，但是它所有的wantErr值都是nil或者cmpopts.AnyError，那么使用cmp是不必要的机制。简化代码，使want字段成为一个bool。然后，你可以使用一个简单的比较法，即!=。

```
// Good:
gotErr := f(test.input) != nil
if gotErr != test.wantErr {
t.Errorf("f(%q) returned err = %v, want error presence = %v", test.input, gotErr, test.wantErr)
}
```


## 测试的结构组织

### 子测试(subtests)

标准Go测试库提供了[定义子测试的功能](https://pkg.go.dev/testing#hdr-Subtests_and_Sub_benchmarks)。这使得设置和清理、控制并行性和测试过滤变得灵活。子测试可能很有用（特别是对于表驱动的测试），但不是必须使用它们。请参阅[Go博客中关于子测试的文章](https://blog.golang.org/subtests)。

子测试不应该依赖其他case的执行来获得成功或初始状态，因为子测试应该能够通过使用go test -run标志或使用Bazel测试过滤表达式来单独运行。

#### 子测试命名

命名你的子测试，使其在测试输出中可读，并在命令行中对测试过滤的用户有用。当你使用t.Run来创建一个子测试时，第一个参数被用作测试的描述性名称。为了确保测试结果对阅读日志的人来说是可读的，选择在转义后仍然有用和可读的子测试名称。把子测试名称想得更像一个函数标识符，而不是一个散文描述。test runner用下划线代替空格，并转义非打印字符。如果你的测试数据受益于较长的描述，可以考虑将描述放在一个单独的字段中（也许可以用t.Log打印，或者与失败信息一起打印）。

子测试可以使用Go test runner或Bazel测试过滤器的标志单独运行，所以选择描述性的名字，同时也要容易输入。

警告：斜杠”/”在子测试名称中是特别不友好的，因为它们对测试过滤器有特殊意义。

```
# Bad:
# Assuming TestTime and t.Run("America/New_York", ...)
bazel test :mytest --test_filter="Time/New_York" # Runs nothing!
bazel test :mytest --test_filter="Time//New_York" # Correct, but awkward.
```


为了识别函数的输入，把函数名包括在测试的失败信息中，在那里它们不会被test runner转义。

```
// Good:
func TestTranslate(t *testing.T) {
data := []struct {
name, desc, srcLang, dstLang, srcText, wantDstText string
}{
{
name: "hu=en_bug-1234",
desc: "regression test following bug 1234. contact: cleese",
srcLang: "hu",
srcText: "cigarettát és egy öngyújtót kérek",
dstLang: "en",
wantDstText: "cigarettes and a lighter please",
}, // ...
}
for _, d := range data {
t.Run(d.name, func(t *testing.T) {
got := Translate(d.srcLang, d.dstLang, d.srcText)
if got != d.wantDstText {
t.Errorf("%s\nTranslate(%q, %q, %q) = %q, want %q",
d.desc, d.srcLang, d.dstLang, d.srcText, got, d.wantDstText)
}
})
}
}
```


下面是一些要避免的例子：

```
// Bad:
// Too wordy.
t.Run("check that there is no mention of scratched records or hovercrafts", ...)
// Slashes cause problems on the command line.
t.Run("AM/PM confusion", ...)
```


### 表驱动的测试

当许多不同的测试用例可以使用类似的测试逻辑进行测试时，使用表驱动的测试。

- 当测试一个函数的实际输出是否等于预期输出。例如，fmt.Sprintf的许多测试或下面的最小片段。
- 当测试一个函数的输出是否总是符合同一组不变量时。例如，net.Dial的测试。

下面是一个表格驱动的测试的最小结构，从标准库strings包中复制出来的。如果需要，你可以使用不同的名字，把测试切片移到测试函数中，或者添加额外的设施，如子测试或设置和清理函数。始终牢记[有用的测试失败](https://google.github.io/styleguide/go/decisions#useful-test-failures)：

```
// Good:
var compareTests = []struct {
a, b string
i int
}{
{"", "", 0},
{"a", "", 1},
{"", "a", -1},
{"abc", "abc", 0},
{"ab", "abc", -1},
{"abc", "ab", 1},
{"x", "ab", 1},
{"ab", "x", -1},
{"x", "a", 1},
{"b", "x", -1},
// test runtime·memeq's chunked implementation
{"abcdefgh", "abcdefgh", 0},
{"abcdefghi", "abcdefghi", 0},
{"abcdefghi", "abcdefghj", -1},
}
func TestCompare(t *testing.T) {
for _, tt := range compareTests {
cmp := Compare(tt.a, tt.b)
if cmp != tt.i {
t.Errorf(`Compare(%q, %q) = %v`, tt.a, tt.b, cmp)
}
}
}
```


注意：上面这个例子中的失败信息满足了识别函数和识别输入的要求。没有必要再[用数字来识别行](https://google.github.io/styleguide/go/decisions#table-tests-identifying-the-row)。

当一些测试用例需要使用与其他测试用例不同的逻辑进行检查时，编写多个测试函数是比较合适的，正如[GoTip #50: Disjoint Table Tests](https://google.github.io/styleguide/go/index.html#gotip)中解释的那样。当一个表中的每个条目都有自己不同的条件逻辑来检查其输入的每个输出时，你的测试代码的逻辑会变得难以理解。如果测试用例有不同的逻辑，但有相同的设置，在一个单一的测试函数中使用子测试序列可能是更有意义的。

你可以将表驱动的测试与多个测试函数结合起来。例如，当测试一个函数的输出与预期的输出完全一致，并且函数对无效的输入返回一个非nil的错误时，那么编写两个单独的表驱动的测试函数是最好的方法：一个用于正常的非错误输出，一个用于错误输出。

#### 数据驱动的测试用例

表测试行有时会变得很复杂，行的值决定了测试用例内的条件行为。测试用例之间的重复所带来的额外清晰度对可读性是必要的。

```
// Good:
type decodeCase struct {
name string
input string
output string
err error
}
func TestDecode(t *testing.T) {
// setupCodex is slow as it creates a real Codex for the test.
codex := setupCodex(t)
var tests []decodeCase // rows omitted for brevity
for _, test := range tests {
t.Run(test.name, func(t *testing.T) {
output, err := Decode(test.input, codex)
if got, want := output, test.output; got != want {
t.Errorf("Decode(%q) = %v, want %v", test.input, got, want)
}
if got, want := err, test.err; !cmp.Equal(got, want) {
t.Errorf("Decode(%q) err %q, want %q", test.input, got, want)
}
})
}
}
func TestDecodeWithFake(t *testing.T) {
// A fakeCodex is a fast approximation of a real Codex.
codex := newFakeCodex()
var tests []decodeCase // rows omitted for brevity
for _, test := range tests {
t.Run(test.name, func(t *testing.T) {
output, err := Decode(test.input, codex)
if got, want := output, test.output; got != want {
t.Errorf("Decode(%q) = %v, want %v", test.input, got, want)
}
if got, want := err, test.err; !cmp.Equal(got, want) {
t.Errorf("Decode(%q) err %q, want %q", test.input, got, want)
}
})
}
}
```


在下面的反例中，注意在case设置中很难区分每个测试case使用哪种类型的Codex。(突出显示的部分违反了[TotT的建议：数据驱动的陷阱](https://testing.googleblog.com/2008/09/tott-data-driven-traps.html)！) .)

```
// Bad:
type decodeCase struct {
name string
input string
codex testCodex
output string
err error
}
type testCodex int
const (
fake testCodex = iota
prod
)
func TestDecode(t *testing.T) {
var tests []decodeCase // rows omitted for brevity
for _, test := tests {
t.Run(test.name, func(t *testing.T) {
var codex Codex
switch test.codex {
case fake:
codex = newFakeCodex()
case prod:
codex = setupCodex(t)
default:
t.Fatalf("unknown codex type: %v", codex)
}
output, err := Decode(test.input, codex)
if got, want := output, test.output; got != want {
t.Errorf("Decode(%q) = %q, want %q", test.input, got, want)
}
if got, want := err, test.err; !cmp.Equal(got, want) {
t.Errorf("Decode(%q) err %q, want %q", test.input, got, want)
}
})
}
}
```


#### 识别行

不要用测试表中的测试索引来代替命名你的测试或打印输入。没有人愿意去看你的测试表，为了弄清楚哪个测试用例失败而去数条目。

```
// Bad:
tests := []struct {
input, want string
}{
{"hello", "HELLO"},
{"wORld", "WORLD"},
}
for i, d := range tests {
if strings.ToUpper(d.input) != d.want {
t.Errorf("failed on case #%d", i)
}
}
```


在你的测试结构中添加测试描述，并将其与失败信息一起打印。当使用子测试时，你的子测试名称应能有效识别行。

重要的是：即使t.Run限定了输出和执行的范围，你也必须始终识别输入。表的测试行名称必须遵循子测试的命名指导。

### 测试助手

一个测试助手(test helper)是一个执行设置或清理任务的函数。所有发生在测试助手中的故障都被认为是环境的故障（而不是被测代码的故障）–例如，当一个测试数据库不能被启动，因为在这台机器上没有更多的空闲端口。

如果你传递一个*testing.T，调用t.Helper，将测试助手中的失败归因于调用该助手的那一行。如果有的话，这个参数应该在上下文参数之后，在任何其他参数之前。

```
// Good:
func TestSomeFunction(t *testing.T) {
golden := readFile(t, "testdata/golden-result.txt")
// ... tests against golden ...
}
// readFile returns the contents of a data file.
// It must only be called from the same goroutine as started the test.
func readFile(t *testing.T, filename string) string {
t.Helper()
contents, err := runfiles.ReadFile(filename)
if err != nil {
t.Fatal(err)
}
return string(contents)
}
```


当这种模式掩盖了测试失败和导致失败的条件之间的联系时，请不要使用这种模式。特别是，关于断言库的指导仍然适用，t.Helper不应该被用来实现这种库。

提示：更多关于测试助手和断言助手的区别，请参见[最佳实践](https://google.github.io/styleguide/go/best-practices#test-functions)。

虽然上面提到的是*testing.T，但很多建议对基准和模糊测试助手来说是一样的。

### 测试包

#### 同一包内的测试

测试可以定义在与被测试代码相同的包中。

要在同一个包中编写测试：

- 将测试放在foo_test.go文件中
- 在测试文件中使用包foo
- 不要明确地导入要测试的包

```
# Good:
go_library(
name = "foo",
srcs = ["foo.go"],
deps = [
...
],
)
go_test(
name = "foo_test",
size = "small",
srcs = ["foo_test.go"],
library = ":foo",
deps = [
...
],
)
```


同一包中的测试可以访问包中未导出的标识符。这可以实现更好的测试覆盖率和更简洁的测试。请注意，在测试中声明的任何例子都不会有用户在其代码中需要的包名。

#### 不同软件包中的测试

将测试定义在与被测代码相同的包中并不总是合适的，甚至不可能。在这种情况下，使用带有 _test 后缀的包名。这是包名的”无下划线”规则的一个例外。比如说：

- 如果一个集成测试没有一个明显它归属的库：

```
// Good:
package gmailintegration_test
import "testing"
```


- 如果在同一软件包中定义测试会导致循环依赖性

```
// Good:
package fireworks_test
import (
"fireworks"
"fireworkstestutil" // fireworkstestutil also imports fireworks
)
```


### 使用testing包

Go标准库提供了testing包。这是谷歌代码库中唯一允许用于Go代码的测试框架。特别是，断言库和第三方测试框架是不允许的。

testing包为编写好的测试提供了一个最小但完整的功能集：

- 顶层测试
- 性能基准测试
[可运行的例子](https://blog.golang.org/examples)- 子测试
- logging
- 失败和致命的失败

这些都是为了与核心语言功能协同工作，如复合字面值和if-with-initializer语法，使测试作者能够编写[清晰、可读、可维护的测试]。

## 非决定性

风格指南不可能列举出所有事项的正面规定，也不可能列举出所有它不提供意见的事项。也就是说，这里有几件可读性社区以前争论过但没有达成共识的事情。

- 局部变量的零值初始化。var i int和i := 0是等价的。请参见
[初始化的最佳实践](https://google.github.io/styleguide/go/best-practices#vardeclinitialization)。 - 空复合字面值 vs new 或make。&File{}和new(File)是等同的。map[string]bool{}和make(map[string]bool)也是如此。请参见
[复合类型声明的最佳实践](https://google.github.io/styleguide/go/best-practices#vardeclcomposite)。 - 在cmp.Diff调用中，got, want的参数排序。要有本地一致性，并在你的失败信息中
[包含一个示例说明](https://google.github.io/styleguide/go/decisions#print-diffs)。 - errors.New vs fmt.Errorf针对非格式化字符串。errors.New(“foo”) 和 fmt.Errorf(“foo”) 可以互换使用。

如果有特殊情况再次出现，可读性导师可能会做一个可选的注释，但一般来说，作者可以自由选择他们在特定情况下喜欢的风格。

当然，如果风格指南中没有涉及的东西确实需要更多的讨论，欢迎作者提出–在具体的审查中，或者在内部留言板上。

## 评论