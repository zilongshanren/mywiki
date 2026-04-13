---
title: 写Go代码时遇到的那些问题[第3期]
url: https://tonybai.com/2018/04/06/the-problems-i-encountered-when-writing-go-code-issue-3rd/
published: '2018-04-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 写Go代码时遇到的那些问题[第3期]

我有一个习惯，那就是随时记录下编程过程中遇到的问题（包括问题现场、问题起因以及对问题的分析），并喜欢阶段性的对一段时间内的**编码过程的得与失**进行回顾和总结。内容可以包括：对编程语法的新认知、遇坑填坑的经历、一些让自己豁然开朗的小tip/小实践等。记录和总结的多了，感觉有价值的，就成文发在博客上的；一些小的点，或是还没有想清楚的事情，或思路没法结构化统一的，就放在资料库里备用。“写Go代码时遇到的那些问题”这个系列也是基于这个思路做的。

在这一篇中，我把“所遇到的问题”划分为三类：语言类、库与工具类、实践类，这样应该更便于大家分类阅读和理解。另外借这篇文章，我们先来看一下[Go语言](https://tonybai.com/tag/golang)当前的State，资料来自于twitter、[reddit](https://www.reddit.com/r/golang)、[golang-dev forum](https://groups.google.com/forum/#!forum/golang-dev)、github上[golang项目](https://github.com/golang)的issue/cl以及各种gophercon的talk资料。

## 零. Go语言当前状态

### 1. vgo

[Go 1.10](http://tonybai.com/2018/02/17/some-changes-in-go-1-10/)在中国农历春节期间正式发布。随后Go team进入了Go 1.11的[开发周期](https://github.com/golang/go/wiki/Go-Release-Cycle)。

在2017年的[Go语言用户调查报告](https://blog.golang.org/survey2017-results)结果中，缺少良好的[包管理工具](https://tonybai.com/2017/06/08/first-glimpse-of-dep/)以及Generics依然是Gopher面临的最为棘手的挑战和难题的Top2，Go team也终于开始认真对待这两个问题了，尤其是包依赖管理的问题。在今年2月末，[Russ Cox](https://swtch.com/~rsc/)在自己的博客上连续发表了[七篇博文](https://research.swtch.com/vgo)，详细阐述了[vgo](https://github.com/golang/vgo) – 带版本感知和支持的Go命令行工具的设计思路和实现方案，并在3月末正式提交了”[versioned-go proposal](https://github.com/golang/proposal/blob/master/design/24301-versioned-go.md)“。

目前相对成熟的包管理方案是:

```
"语义化版本"
+manifest文件(手工维护的依赖约束描述文件)
+lock文件(工具自动生成的传递依赖描述文件)
+版本选择引擎工具（比如dep中的gps - Go Packaging Solver）
```


与之相比，vgo既有继承，更有创新。继承的是对[语义化版本](http://semver.org/lang/zh-CN/)的支持，创新的则是[semantic import versioning](https://research.swtch.com/vgo-import)、[最小版本选择minimal version selection](https://research.swtch.com/vgo-mvs)等新机制，不变的则是对[Go1语法](https://golang.org/doc/go1compat)的兼容。按照Russ Cox的计划，Go 1.11很可能会提供一个试验性的vgo实现（当然vgo所呈现的形式估计是merge到go tools中），让广大gopher试用和反馈，然后会像[vendor机制](http://tonybai.com/2015/07/31/understand-go15-vendor/)那样，在后续Go版本中逐渐成为默认选项。

### 2. wasm porting

知名开源项目[gopherjs](https://github.com/gopherjs/gopherjs)的作者[Richard Musiol](https://github.com/neelance)上个月提交了一个proposal: [WebAssembly architecture for Go](https://docs.google.com/document/d/131vjr4DH6JFnb-blm_uRdaC0_Nv3OUwjEY5qVCxCup4/preview#heading=h.mjo1bish3xni)，主旨在于让Gopher也可以用Go编写前端代码，让Go编写的代码可以在浏览器中运行。当然这并不是真的让Go能像js那样直接运行于浏览器或nodejs上，而是将Go编译为[WebAssembly，wasm](http://webassembly.org/)中间字节码，再在浏览器或nodejs初始化的运行环境中运行。这里根据自己的理解粗略画了一幅二进制机器码的go app与中间码的wasm的运行层次对比图，希望对大家有用：

![img{512x368}](../../assets/b57361533647d704.png)


wasm porting已经完成了[第一次commit](https://go-review.googlesource.com/c/go/+/102835) ，很大可能会随着go1.11一并发布第一个版本。

### 3. 非协作式的goroutine抢占式调度

当前[goroutine](http://tonybai.com/2017/06/23/an-intro-about-goroutine-scheduler/)的[“抢占式”调度](http://tonybai.com/2017/11/23/the-simple-analysis-of-goroutine-schedule-examples/)依靠的是compiler在函数中自动插入的“cooperative preemption point”来实现的，但这种方式在使用过程中依然有各种各样的问题，比如：检查点的性能损耗、诡异的全面延迟问题以及调试上的困难。近期负责go runtime gc设计与实现的[Austin Clements](https://github.com/aclements)提出了一个proposal：[non-cooperative goroutine preemption](https://github.com/golang/go/issues/24543) ，该proposal将去除cooperative preemption point，而改为利用构建和记录每条指令的stack和register map的方式实现goroutine的抢占， 该proposal预计将在go 1.12中实现。

### 4. Go的历史与未来

在[GopherConRu 2018大会](https://www.gophercon-russia.ru/en)上，来自Go team的核心成员Brad Fitzpatrick做了[“Go的历史与未来”](https://github.com/GopherConRu/talks/blob/master/2018/Go%20-%20looking%20back%20and%20looking%20forward%20-%20Brad%20Fitzpatrick.pdf)的主题演讲 ，Bradfitz“爆料”了关于Go2的几个可能，考虑到Bradfitz在Go team中的位置，这些可能性还是具有很大可信度的：

```
1). 绝不像Perl6和Python3那样分裂社区
2). Go1的包可以import Go2的package
3). Go2很可能加入Generics，Ian Lance Taylor应该在主导该Proposal
4). Go2在error handling方面会有改进，但不会是try--catch那种形式
5). 相比于Go1，Go2仅会在1-3个方面做出重大变化
6). Go2可能会有一个新的标准库，并且该标准库会比现有的标准库更小，很多功能放到标准库外面
7). 但Go2会在标准库外面给出最流行、推荐的、可能认证的常用包列表，这些在标准库外面的包可以持续更新，而不像那些在标准库中的包，只能半年更新一次。
```


## 一. 语言篇

### 1. len(channel)的使用

len是Go语言的一个[built-in函数](https://golang.org/ref/spec#Length_and_capacity)，它支持接受array、slice、map、string、channel类型的参数，并返回对应类型的”长度” – 一个整型值：

```
len(s)
如果s是string，len(s)返回字符串中的字节个数
如何s是[n]T, *[n]T的数组类型，len(s)返回数组的长度n
如果s是[]T的Slice类型，len(s)返回slice的当前长度
如果s是map[K]T的map类型，len(s)返回map中的已定义的key的个数
如果s是chan T类型，那么len(s)返回当前在buffered channel中排队（尚未读取）的元素个数
```


不过我们在代码经常见到的是len函数针对数组、slice、string类型的调用，而len与channel的联合使用却很少。那是不是说len(channel)就不可用了呢？我们先来看看len(channel)的语义。

- 当channel为unbuffered channel时，len(channel)总是返回0；
- 当channel为buffered channel时，len(channel)返回当前channel中尚未被读取的元素个数。

这样一来，所谓len(channel)中的[channel](https://tonybai.com/2014/09/29/a-channel-compendium-for-golang/)就是针对buffered channel。len(channel)从语义上来说一般会被用来做“判满”、”判有”和”判空”逻辑：

```
// 判空
if len(channel) == 0 {
// 这时：channel 空了 ?
}
// 判有
if len(channel) > 0 {
// 这时：channel 有数据了 ?
}
// 判满
if len(channel) == cap(channel) {
// 这时: channel 满了 ?
}
```


大家看到了，我在上面代码中注释：“空了”、“有数据了”和“满了”的后面打上了问号！channel多用于多个goroutine间的通讯，一旦多个goroutine共同读写channel，len(channel)就会在多个goroutine间形成”竞态条件”，单存的依靠len(channel)来判断队列状态，不能保证在后续真正读写channel的时候channel状态是不变的。以判空为例：

![img{512x368}](../../assets/5b745f45fb24b897.png)


从上图可以看到，当goroutine1使用len(channel)判空后，便尝试从channel中读取数据。但在真正从Channel读数据前，另外一个goroutine2已经将数据读了出去，goroutine1后面的**读取将阻塞在channel上**，导致后面逻辑的失效。因此，**为了不阻塞在channel上**，常见的方法是将“判空与读取”放在一起做、将”判满与写入”一起做，通过select实现操作的“事务性”：

```
//writing-go-code-issues/3rd-issue/channel_len.go/channel_len.go.go
func readFromChan(ch <-chan int) (int, bool) {
select {
case i := <-ch:
return i, true
default:
return 0, false // channel is empty
}
}
func writeToChan(ch chan<- int, i int) bool {
select {
case ch <- i:
return true
default:
return false // channel is full
}
}
```


我们看到由于用到了Select-default的trick，当channel空的时候，readFromChan不会阻塞；当channel满的时候，writeToChan也不会阻塞。这种方法也许适合大多数的场合，但是这种方法有一个“问题”，那就是“改变了channel的状态”：读出了一个元素或写入了一个元素。有些时候，我们不想这么做，我们想在不改变channel状态下单纯地侦测channel状态！很遗憾，目前没有哪种方法可以适用于所有场合。但是在特定的场景下，我们可以用len(channel)实现。比如下面这个场景：

![img{512x368}](../../assets/7ee8405ffe2e3f26.png)


这是一个“多producer + 1 consumer”的场景。controller是一个总控协程，初始情况下，它来判断channel中是否有消息。如果有消息，它本身不消费“消息”，而是创建一个consumer来消费消息，直到consumer因某种情况退出，控制权再回到controller，controller不会立即创建new consumer，而是等待channel下一次有消息时才创建。在这样一个场景中，我们就可以使用len(channel)来判断是否有消息。

### 2. 时间的格式化输出

时间的格式化输出是日常编程中经常遇到的“题目”。以前使用[C语言编程](https://tonybai.com/tag/c)时，用的是strftime。我们来回忆一下c的代码：

```
// writing-go-code-issues/3rd-issue/time-format/strftime_in_c.c
#include <stdio.h>
#include <time.h>
int main() {
time_t now = time(NULL);
struct tm *localTm;
localTm = localtime(&now);
char strTime[100];
strftime(strTime, sizeof(strTime), "%Y-%m-%d %H:%M:%S", localTm);
printf("%s\n", strTime);
return 0;
}
```


这段c代码输出结果是：

```
2018-04-04 16:07:00
```


我们看到strftime采用“字符化”的占位符(诸如：%Y、%m等)“拼”出时间的目标输出格式布局（如：”%Y-%m-%d %H:%M:%S”），这种方式不仅在C中采用，很多其他主流编程语言也采用了该方案，比如:shell、[python](https://tonybai.com/tag/python)、[ruby](https://tonybai.com/tag/ruby)、[java](https://tonybai.com/tag/java)等，这似乎已经成为了各种编程语言在时间格式化输出的标准。这些占位符对应的字符（比如Y、M、H）是对应英文单词的头母，因此相对来说较为容易记忆。

但是如果你在Go中使用strftime的这套“标准”，看到输出结果的那一刻，你肯定要“骂娘”！

```
// writing-go-code-issues/3rd-issue/time-format/timeformat_in_c_way.go
package main
import (
"fmt"
"time"
)
func main() {
fmt.Println(time.Now().Format("%Y-%m-%d %H:%M:%S"))
}
```


上述go代码输出结果如下：

```
%Y-%m-%d %H:%M:%S
```


Go居然将“时间格式占位符字符串”原封不动的输出了!

这是因为Go另辟了蹊径，采用了不同于strftime的时间格式化输出的方案。Go的设计者主要出于这样的考虑：虽然strftime的单个占位符使用了对应单词的首字母的形式，但是但真正写起代码来，不打开strftime函数的manual或查看[网页版的strftime助记符说明](http://strftime.org/)，很难真的拼出一个复杂的时间格式。并且对于一个”%Y-%m-%d %H:%M:%S”的格式串，不对照文档，很难在大脑中准确给出格式化后的时间结果，比如%Y和%y有何不同、%M和%m又有何差别呢？

Go语言采用了更为直观的“参考时间(reference time)”替代strftime的各种标准占位符，使用“参考时间”构造出来的“时间格式串”与最终输出串是“一模一样”的，这就省去了程序员再次在大脑中对格式串进行解析的过程：

```
格式串："2006年01月02日 15时04分05秒"
=>
输出结果：2018年04月04日 18时13分08秒
```


标准的参考时间如下：

```
2006-01-02 15:04:05 PM -07:00 Jan Mon MST
```


这个绝对时间本身并没有什么实际意义，仅是出于“好记”的考虑，我们将这个参考时间换为另外一种时间输出格式：

```
01/02 03:04:05PM '06 -0700
```


我们看出Go设计者的“用心良苦”，这个时间其实恰好是**将助记符从小到大排序(从01到07)的结果**，可以理解为：01对应的是%M, 02对应的是%d等等。下面这幅图形象地展示了“参考时间”、“格式串”与最终格式化的输出结果之间的关系：

![img{512x368}](../../assets/3c5cd812bb9c7b06.png)


就我个人使用go的经历来看，我在做时间格式化输出时，尤其是构建略微复杂的时间格式输出时，也还是要go doc time包或打开time包的web手册的。从社区的反馈来看，很多Gopher也都有类似经历，尤其是那些已经用惯了strftime格式的gopher。甚至有人专门做了[“Fucking Go Date Format”](http://fuckinggodateformat.com/)页面，来帮助自动将strftime使用的格式转换为go time的格式。

下面这幅cheatsheet也能提供一些帮助(由writing-go-code-issues/3rd-issue/time-format/timeformat_cheatsheet.go输出生成)：

![img{512x368}](../../assets/158766a7c9fcd080.png)


## 二. 库与工具篇

### 1. golang.org/x/text/encoding/unicode遇坑一则

在[gocmpp](https://github.com/bigwhite/gocmpp)这个项目中，我用到了unicode[字符集转换](https://tonybai.com/2007/11/03/also-talk-about-char-encoding/)：将utf8转换为ucs2(utf16)、ucs2转换为utf8、utf8转为GB18030等。这些转换功能，我是借助golang.org/x/text这个项目下的encoding/unicode和transform实现的。x/text是golang官方维护的text处理的工具包，其中包含了对unicode字符集的相关操作。

要实现一个utf8到ucs2(utf16)的字符集转换，只需像如下这样实现即可（这也是我的最初实现）：

```
func Utf8ToUcs2(in string) (string, error) {
if !utf8.ValidString(in) {
return "", ErrInvalidUtf8Rune
}
r := bytes.NewReader([]byte(in))
//UTF-16 bigendian, no-bom
t := transform.NewReader(r, unicode.All[1].NewEncoder())
out, err := ioutil.ReadAll(t)
if err != nil {
return "", err
}
return string(out), nil
}
```


这里要注意是unicode.All这个切片保存着UTF-16的所有格式：

```
var All = []encoding.Encoding{
UTF16(BigEndian, UseBOM),
UTF16(BigEndian, IgnoreBOM),
UTF16(LittleEndian, IgnoreBOM),
}
```


这里我最初我用的是All[1]，即UTF16(BigEndian, IgnoreBOM)，一切都是正常的。

但就在年前，我将text项目更新到最新版本，然后发现单元测试无法通过：

```
--- FAIL: TestUtf8ToUcs2 (0.00s)
utils_test.go:58: The first char is fe, not equal to expected 6c
FAIL
FAIL github.com/bigwhite/gocmpp/utils 0.008s
```


经查找发现：text项目的golang.org/x/text/encoding/unicode包做了不兼容的修改，上面那个unicode.All切片变成了下面这个样子：

```
// All lists a configuration for each IANA-defined UTF-16 variant.
var All = []encoding.Encoding{
UTF8,
UTF16(BigEndian, UseBOM),
UTF16(BigEndian, IgnoreBOM),
UTF16(LittleEndian, IgnoreBOM),
}
```


All切片在最前面插入了一个UTF8元素，这样导致我的代码中原本使用的 UTF16(BigEndian, IgnoreBOM)变成了UTF16(BigEndian, UseBOM)，test不过也就情有可原了。

如何改呢？这回儿我直接使用UTF16(BigEndian, IgnoreBOM)，而不再使用All切片了：

```
func Utf8ToUcs2(in string) (string, error) {
if !utf8.ValidString(in) {
return "", ErrInvalidUtf8Rune
}
r := bytes.NewReader([]byte(in))
//UTF-16 bigendian, no-bom
t := transform.NewReader(r,
unicode.UTF16(unicode.BigEndian, unicode.IgnoreBOM).NewEncoder())
out, err := ioutil.ReadAll(t)
if err != nil {
return "", err
}
return string(out), nil
}
```


这样即便All切片再有什么变动，我的代码也不会受到什么影响了。

### 2. logrus的非结构化日志定制输出

在该系列的[第一篇文章](http://tonybai.com/2018/01/13/the-problems-i-encountered-when-writing-go-code-issue-1st/)中，我提到过使用[logrus](https://github.com/sirupsen/logrus)+[lumberjack](https://github.com/natefinch/lumberjack)来实现支持rotate的logging。

默认情况下日志的输出格式是这样的（writing-go-code-issues/3rd-issue/logrus/logrus2lumberjack_default.go）：

```
time="2018-04-05T06:08:53+08:00" level=info msg="logrus log to lumberjack in normal text formatter"
```


这样相对结构化的日志比较适合后续的集中日志分析。但是日志携带的“元信息(time、level、msg)”过多，并不是所有场合都倾向于这种日志，于是我们期望以普通的非结构化的日志输出，我们定制formatter：

```
// writing-go-code-issues/3rd-issue/logrus/logrus2lumberjack.go
func main() {
customFormatter := &logrus.TextFormatter{
FullTimestamp: true,
TimestampFormat: "2006-01-02 15:04:05",
}
logger := logrus.New()
logger.Formatter = customFormatter
rotateLogger := &lumberjack.Logger{
Filename: "./foo.log",
}
logger.Out = rotateLogger
logger.Info("logrus log to lumberjack in normal text formatter")
}
```


我们使用textformatter，并定制了时间戳的格式，输出结果如下：

```
time="2018-04-05 06:22:57" level=info msg="logrus log to lumberjack in normal text formatter"
```


日志仍然不是我们想要的那种。但同样的customFormatter如果输出到terminal，结果却是我们想要的：

```
//writing-go-code-issues/3rd-issue/logrus/logrus2tty.go
INFO[2018-04-05 06:26:16] logrus log to tty in normal text formatter
```


到底如何设置TextFormatter的属性才能让我们输出到lumberjack中的日志格式是我们想要的这种呢？无奈下只能挖logrus的源码了，我们找到了这段代码：

```
//github.com/sirupsen/logrus/text_formatter.go
// Format renders a single log entry
func (f *TextFormatter) Format(entry *Entry) ([]byte, error) {
... ...
isColored := (f.ForceColors || f.isTerminal) && !f.DisableColors
timestampFormat := f.TimestampFormat
if timestampFormat == "" {
timestampFormat = defaultTimestampFormat
}
if isColored {
f.printColored(b, entry, keys, timestampFormat)
} else {
if !f.DisableTimestamp {
f.appendKeyValue(b, "time", entry.Time.Format(timestampFormat))
}
f.appendKeyValue(b, "level", entry.Level.String())
if entry.Message != "" {
f.appendKeyValue(b, "msg", entry.Message)
}
for _, key := range keys {
f.appendKeyValue(b, key, entry.Data[key])
}
}
b.WriteByte('\n')
return b.Bytes(), nil
}
```


我们看到如果isColored为false，输出的就是带有time, msg, level的结构化日志；只有isColored为true才能输出我们想要的普通日志。isColored的值与三个属性有关：ForceColors 、isTerminal和DisableColors。我们按照让isColored为true的条件组合重新设置一下这三个属性，因为输出到file，因此isTerminal自动为false。

```
//writing-go-code-issues/3rd-issue/logrus/logrus2lumberjack_normal.go
func main() {
// isColored := (f.ForceColors || f.isTerminal) && !f.DisableColors
customFormatter := &logrus.TextFormatter{
FullTimestamp: true,
TimestampFormat: "2006-01-02 15:04:05",
ForceColors: true,
}
logger := logrus.New()
logger.Formatter = customFormatter
rotateLogger := &lumberjack.Logger{
Filename: "./foo.log",
}
logger.Out = rotateLogger
logger.Info("logrus log to lumberjack in normal text formatter")
}
```


我们设置ForceColors为true后，在foo.log中得到了我们期望的输出结果：

```
INFO[2018-04-05 06:33:22] logrus log to lumberjack in normal text formatter
```


## 三. 实践篇

### 1. 说说网络数据读取timeout的处理 – 以SetReadDeadline为例

Go天生适合于[网络编程](https://tonybai.com/2015/11/17/tcp-programming-in-golang/)，但网络编程的复杂性也是有目共睹的、要写出稳定、高效的网络端程序，需要的考虑的因素有很多。比如其中之一的：从socket读取数据超时的问题。

Go语言标准网络库并没有实现epoll实现的那样的**“idle timeout”**，而是提供了Deadline机制，我们用一副图来对比一下两个机制的不同：

![img{512x368}](../../assets/8c2d6a7d75932884.png)


看上图a)和b)展示了”idle timeout”机制，所谓idle timeout就是指这个timeout是真正在没有data ready的情况的timeout（如图中a)，如果有数据ready可读(如图中b)，那么timeout机制暂停，直到数据读完后，再次进入数据等待的时候，idle timeout再次启动。

而deadline(以read deadline为例)机制，则是无论是否有数据ready以及数据读取活动，都会在到达时间（deadline）后的再次read时返回timeout error，并且后续的所有network read operation也都会返回timeout（如图中d），除非重新调用SetReadDeadline(time.Time{})取消Deadline或在再次读取动作前重新重新设定deadline实现**续时**的目的。Go网络编程一般是“阻塞模型”，那为什么还要有SetReadDeadline呢，这是因为有时候，我们要给调用者“感知”其他“异常情况”的机会，比如是否收到了main goroutine发送过来的**退出通知信息**。

Deadline机制在使用起来很容易出错，这里列举两个曾经遇到的出错状况：

a) 以为SetReadDeadline后，后续每次Read都可能实现idle timeout

![img{512x368}](../../assets/30411d0ba6204ad2.png)


在上图中，我们看到这个流程是读取一个完整业务包的过程，业务包的读取使用了三次Read调用，但是只在第一次Read前调用了SetReadDeadline。这种使用方式仅仅在Read A时实现了足额的“idle timeout”，且仅当A数据始终未ready时会timeout；一旦A数据ready并已经被Read，当Read B和Read C时，如果还期望足额的“idle timeout”那就误解了SetReadDeadline的真正含义了。因此要想在每次Read时都实现“足额的idle timeout”，需要在每次Read前都重新设定deadline。

b) 一个完整“业务包”分多次读取的异常情况的处理

![img{512x368}](../../assets/51a4508e864f1290.png)


在这幅图中，每个Read前都重新设定了deadline，那么这样就一定ok了么？对于在一个过程中读取一个“完整业务包”的业务逻辑来说，我们还要考虑对每次读取异常情况的处理，尤其是timeout发生。在该例子中，有三个Read位置需要考虑异常处理。

如果Read A始终没有读到数据，deadline到期，返回timeout，这里是最容易处理的，因为此时前一个完整数据包已经被读完，新的完整数据包还没有到来，外层控制逻辑收到timeout后，重启再次启动该读流程即可。

如果Read B或Read C处没有读到数据，deadline到期，这时异常处理就棘手一些，因为一个完整数据包的部分数据（A）已经从流中被读出，剩余的数据并不是一个完整的业务数据包，不能简单地再在外层控制逻辑中重新启动该过程。我们要么在Read B或Read C处尝试多次重读，直到将完整数据包读取完整后返回；要么认为在B或C处出现timeout是不合理的，返回区别于A处的错误码给外层控制逻辑，让外层逻辑决定是否是连接存在异常。

注：本文所涉及的示例代码，请到[这里](https://github.com/bigwhite/experiments/tree/master/writing-go-code-issues/3rd-issue)下载。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

好文，赞一个。

图挂了吗？

发完评论图就出来了。。

站点在国外，国内访问可能稍微慢了一些:)。

您好，我是开发者头条的运营。您的《写 Go 代码时遇到的那些问题（第 3 期）》已被我们平台用户推荐到首页。感谢您的辛苦创作，为了让更多读者认识您，我们邀请您来开发者头条分享。与创作不同，您仅需复制粘贴文章链接即可完成分享。您可以在各大应用市场搜索 “开发者头条” 找到我们的应用，欢迎了解。期待您的分享。