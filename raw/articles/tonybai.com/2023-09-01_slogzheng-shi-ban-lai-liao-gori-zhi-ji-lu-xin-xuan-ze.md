---
title: slog正式版来了：Go日志记录新选择！
url: https://tonybai.com/2023/09/01/slog-a-new-choice-for-logging-in-go/
published: '2023-09-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# slog正式版来了：Go日志记录新选择！

![](../../assets/ef932960fb0124d2.png)


[本文永久链接](https://tonybai.com/2023/09/01/slog-a-new-choice-for-logging-in-go) – https://tonybai.com/2023/09/01/slog-a-new-choice-for-logging-in-go

在大约一年前，我就写下了《[slog：Go官方版结构化日志包](https://tonybai.com/2022/10/30/first-exploration-of-slog)》一文，文中介绍了Go团队正在设计并计划在下一个Go版本中落地的Go官方结构化日志包：[slog](https://pkg.go.dev/log/slog)。但slog并未如预期在[Go 1.20版本](https://tonybai.com/2023/02/08/some-changes-in-go-1-20/)中落地，而是在golang.org/x/exp/slog下面给出了slog的初始实现供社区体验。

时光飞逝，slog在golang.org/x/exp/slog下经历了1年多时间的改善和演进，终于在最近发布的[Go 1.21版本](https://tonybai.com/2023/08/20/some-changes-in-go-1-21/)中以log/slog的包导入路径正式加入Go标准库。

正式版的slog在结构上并未作较大变化，依旧是分为前端和后端，因此讲exp/slog时的那幅图依然适用：

![](../../assets/975b7b5df18e7ab0.png)


不过，正式版的slog与当初那篇文章中的exp/slog在一些类型与API上已有不同。在这篇文章中，我就来简要说明一下。我这里讲述的思路大致是将《[slog：Go官方版结构化日志包](https://tonybai.com/2022/10/30/first-exploration-of-slog)》一文中的例子用log/slog改造一遍，这个过程可以让我们看到正式版log/slog与exp/slog的差异。

## 1. slog快速入门

### 1.1 slog的”hello, world”

如果仅是想以最快速的方式开始使用slog，那么下面可以算是slog的”hello, world”版本：

```
//slog-examples-go121/demo0/main.go
package main
import (
"log/slog"
)
func main() {
slog.Info("my first slog msg", "greeting", "hello, slog")
}
```


运行这段程序，会得到下面输出：

```
$go run main.go
2023/08/29 05:01:36 INFO my first slog msg greeting="hello, slog"
```


### 1.2 TextHandler和JSONHandler

默认情况下，slog输出的格式仅是普通text格式，而并非JSON格式，也不是以key=value形式呈现的文本。

slog提供了以JSON格式输出的JSONHandler和以key=value形式呈现的文本形式的TextHandler。不过要使用这两种Handler进行日志输出，我们需要显式创建它们：

```
//slog-examples-go121/demo1/main.go
h := slog.NewTextHandler(os.Stderr, nil)
l := slog.New(h)
l.Info("greeting", "name", "tony")
l.Error("oops", "err", net.ErrClosed, "status", 500)
h1 := slog.NewJSONHandler(os.Stderr, nil)
l1 := slog.New(h1)
l1.Info("greeting", "name", "tony")
l1.Error("oops", "err", net.ErrClosed, "status", 500)
```


注：相对于exp/slog，正式版的log/slog的NewTextHandler和NewJSONHandler增加了一个新的opts *HandlerOptions参数。


上述代码分别创建了一个使用TextHandler的slog.Logger实例以及一个使用JSONHandler的slog.Logger实例，执行这段代码后将输出如下日志：

```
$go run main.go
time=2023-08-29T05:34:27.370+08:00 level=INFO msg=greeting name=tony
time=2023-08-29T05:34:27.370+08:00 level=ERROR msg=oops err="use of closed network connection" status=500
{"time":"2023-08-29T05:34:27.370306+08:00","level":"INFO","msg":"greeting","name":"tony"}
{"time":"2023-08-29T05:34:27.370315+08:00","level":"ERROR","msg":"oops","err":"use of closed network connection","status":500}
```


如果觉得每次还得使用l或l1来调用Info、Error等输出日志的函数不便利，可以将l或l1设置为Default Logger，这样无论在任何包内都可以直接通过slog包级函数，如Info、Error等直接输出日志：

```
//slog-examples-go121/demo1/main.go
time=2023-08-29T05:40:08.503+08:00 level=INFO msg="textHandler after setDefault" name=tony age=30
{"time":"2023-08-29T05:40:08.503672+08:00","level":"INFO","msg":"jsonHandler after setDefault","name":"tony","age":30}
```


注：相对于exp/slog，正式版的log/slog提供了带有Context的Info、Error日志输出函数：DebugContext、InfoContext、ErrorContext等。


### 1.3 HandlerOption

通过在创建Handler时传入自定义的HandlerOption，我们可以设置Logger的日志级别和是否输出Source，比如下面示例：

```
//slog-examples-go121/demo2/main.go
opts := slog.HandlerOptions{
AddSource: true,
Level: slog.LevelError,
}
slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stderr, &opts)))
slog.Info("open file for reading", "name", "foo.txt", "path", "/home/tonybai/demo/foo.txt")
slog.Error("open file error", "err", os.ErrNotExist, "status", 2)
```


上述代码通过HandlerOption设置了Handler仅输出Error级别日志，并在输出的日志中带上Source信息，运行这段程序，会得到下面输出：

```
$go run main.go
{"time":"2023-08-29T05:18:18.068213+08:00","level":"ERROR","source":{"function":"main.main","file":"/Users/tonybai/Go/src/github.com/bigwhite/experiments/slog-examples-go121/demo2/main.go","line":17},"msg":"open file error","err":"file does not exist","status":2}
```


我们看到通过Info函数输出的日志并没有被仅处理Error级别的Handler输出到console上。另外在输出的日志中，我们看到了source这个key，以及它的值，即输出日志的那行代码在源代码文件中位置。

### 1.4 属性字段

我们日常输出的日志都有一些共同的字段，比如上面的level、time，这些字段被称为属性。slog支持带有属性(attribute)的日志输出，slog内置了若干属性，如下面代码所示：

```
// log/slog/handler.go
// Keys for "built-in" attributes.
const (
// TimeKey is the key used by the built-in handlers for the time
// when the log method is called. The associated Value is a [time.Time].
TimeKey = "time"
// LevelKey is the key used by the built-in handlers for the level
// of the log call. The associated value is a [Level].
LevelKey = "level"
// MessageKey is the key used by the built-in handlers for the
// message of the log call. The associated value is a string.
MessageKey = "msg"
// SourceKey is the key used by the built-in handlers for the source file
// and line of the log call. The associated value is a string.
SourceKey = "source"
)
```


当然slog也支持自定义属性：

```
//slog-examples-go121/demo2/main.go
l := slog.Default().With("attr1", "attr1_value", "attr2", "attr2_value")
l.Error("connect server error", "err", net.ErrClosed, "status", 500)
l.Error("close conn error", "err", net.ErrClosed, "status", 501)
```


在上面的代码中，我们定义了两个属性：attr1和attr2，以及它们的值，这样当我们用带有这两个属性的Logger输出日志时，每行日志都会包含这两个属性：

```
{"time":"2023-08-29T05:28:39.322014+08:00","level":"ERROR","source":{"function":"main.main","file":"/Users/tonybai/Go/src/github.com/bigwhite/experiments/slog-examples-go121/demo2/main.go","line":23},"msg":"connect server error","attr1":"attr1_value","attr2":"attr2_value","err":"use of closed network connection","status":500}
{"time":"2023-08-29T05:28:39.322028+08:00","level":"ERROR","source":{"function":"main.main","file":"/Users/tonybai/Go/src/github.com/bigwhite/experiments/slog-examples-go121/demo2/main.go","line":24},"msg":"close conn error","attr1":"attr1_value","attr2":"attr2_value","err":"use of closed network connection","status":501}
```


当然你也可以通过slog.LogAttrs做“一次性”的属性输出：

```
//slog-examples-go121/demo2/main.go
l.LogAttrs(context.Background(), slog.LevelError, "log with attribute once", slog.String("attr3", "attr3_value"))
l.Error("reconnect error", "err", net.ErrClosed, "status", 502)
```


这两行输出如下日志：

```
{"time":"2023-08-29T05:32:00.419772+08:00","level":"ERROR","source":{"function":"main.main","file":"/Users/tonybai/Go/src/github.com/bigwhite/experiments/slog-examples-go121/demo2/main.go","line":26},"msg":"log with attribute once","attr1":"attr1_value","attr2":"attr2_value","attr3":"attr3_value"}
{"time":"2023-08-29T05:32:00.419778+08:00","level":"ERROR","source":{"function":"main.main","file":"/Users/tonybai/Go/src/github.com/bigwhite/experiments/slog-examples-go121/demo2/main.go","line":27},"msg":"reconnect error","attr1":"attr1_value","attr2":"attr2_value","err":"use of closed network connection","status":502}
```


我们看到通过LogAttrs输出的attr3属性仅出现一次。

注：相对于exp/slog，正式版的log/slog提供的LogAttrs方法多了一个context.Context参数。


### 1.5 Group形式的日志输出

slog支持group形式的日志输出，这点保持了与exp/slog的一致。下面是一个输出group log的例子：

```
//slog-examples-go121/demo2/main.go
gl := l.WithGroup("response")
gl.Error("http post response", "code", 403, "status", "server not response", "server", "10.10.121.88")
```


我们先创建一个名为“response”的group logger，然后调用Error输出日志。Error会将所有attribute之外的字段放入response这个group中呈现，我们看一下运行结果：

```
{"time":"2023-08-29T12:54:07.623002+08:00","level":"ERROR","source":{"function":"main.main","file":"/Users/tonybai/Go/src/github.com/bigwhite/experiments/slog-examples-go121/demo2/main.go","line":30},"msg":"http post response","attr1":"attr1_value","attr2":"attr2_value","response":{"code":403,"status":"server not response","server":"10.10.121.88"}}
```


## 2. 动态调整日志级别

exp/slog使用slog.AtomicLevel实现Logger级别的动态调整。在正式版slog中，我们则使用slog.LevelVar来实现Logger日志级别的动态调整，使用方法差不多，看下面这个例子：

```
// slog-examples-go121-demo3/main.go
func main() {
var lvl slog.LevelVar
lvl.Set(slog.LevelDebug)
opts := slog.HandlerOptions{
Level: &lvl,
}
slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stderr, &opts)))
slog.Info("before resetting log level:")
slog.Info("greeting", "name", "tony")
slog.Error("oops", "err", net.ErrClosed, "status", 500)
slog.LogAttrs(context.Background(), slog.LevelError, "oops",
slog.Int("status", 500), slog.Any("err", net.ErrClosed))
slog.Info("after resetting log level to error level:")
lvl.Set(slog.LevelError)
slog.Info("greeting", "name", "tony")
slog.Error("oops", "err", net.ErrClosed, "status", 500)
slog.LogAttrs(context.Background(), slog.LevelError, "oops",
slog.Int("status", 500), slog.Any("err", net.ErrClosed))
}
```


结合LevelVar和HandlerOption，我们实现了Logger日志级别的动态调整，这里是由LevelDebug调整为LevelError。上面示例的输出结果如下：

```
{"time":"2023-08-29T06:15:26.103022+08:00","level":"INFO","msg":"before resetting log level:"}
{"time":"2023-08-29T06:15:26.103197+08:00","level":"INFO","msg":"greeting","name":"tony"}
{"time":"2023-08-29T06:15:26.103203+08:00","level":"ERROR","msg":"oops","err":"use of closed network connection","status":500}
{"time":"2023-08-29T06:15:26.103222+08:00","level":"ERROR","msg":"oops","status":500,"err":"use of closed network connection"}
{"time":"2023-08-29T06:15:26.103226+08:00","level":"INFO","msg":"after resetting log level to error level:"}
{"time":"2023-08-29T06:15:26.103232+08:00","level":"ERROR","msg":"oops","err":"use of closed network connection","status":500}
{"time":"2023-08-29T06:15:26.103236+08:00","level":"ERROR","msg":"oops","status":500,"err":"use of closed network connection"}
```


我们看到，动态调整到LevelError后，Info函数打印的日志将不再输出到console了。

## 3. 自定义后端Handler

在《[slog：Go官方版结构化日志包](https://tonybai.com/2022/10/30/first-exploration-of-slog)》一文中，我们就举例说明了如何自定义一个后端Handler，正式版slog在自定义Handler这方面变化不大，都是通过实现slog.Handler接口的方式达成的。大家可自行查看slog-examples-go121/demo4中的代码，这里就不赘述了。

此外，log/slog的作者Jonathan Amsterdam还提供了一篇[“slog自定义handler指南”](https://github.com/golang/example/blob/master/slog-handler-guide/guide.md)供大家参考。

## 4. 验证handler

Go 1.21正式版提供了一个testing/slogtest包可以用来辅助测试自定义后端Handler，我们就以slog-examples-go121/demo4中自定义的ChanHandler为例，用slogtest包对其进行一下测试：

```
// slog-examples-go121/demo4/handler_test.go
func TestChanHandlerParsing(t *testing.T) {
var ch = make(chan []byte, 100)
h := NewChanHandler(ch)
results := func() []map[string]any {
var ms []map[string]any
ticker := time.NewTicker(time.Second)
loop:
for {
select {
case line := <-ch:
if len(line) == 0 {
break
}
var m map[string]any
if err := json.Unmarshal(line, &m); err != nil {
t.Fatal(err)
}
ms = append(ms, m)
case <-ticker.C:
break loop
}
}
return ms
}
err := slogtest.TestHandler(h, results)
if err != nil {
log.Fatal(err)
}
}
```


slogtest仅提供一个导出函数TestHandler，它会自动基于你提供的Handler创建Logger并向Logger写入一些日志，然后通过传入的results函数对写入的日志进行格式验证，主要是json反序列化，如果成功，会记录在map[string]any类型的切片中。最后TestHandler会比对写入日志条数与反序列化成功的条数，如果一致，说明测试ok，反之则测试失败。

注：基于这个TestHandler，还真测试出原ChanHandler的一个问题，已经fix。


## 5. 性能tips

按官方benchmark结果，log/slog的性能要高于Go社区常用的结构化日志包，比如[zap](https://tonybai.com/2021/07/14/uber-zap-advanced-usage)等。

即便如此，log在go应用中带来的延迟依旧不可忽视。slog的[proposal design](https://go.googlesource.com/proposal/+/master/design/56345-structured-logging.md)中给出了一些关于性能的考量和tip，大家可以在日后使用slog时借鉴：

- 使用Logger.With避免重复格式化公共属性字段，这使得处理程序可以缓存格式化结果。
- 将昂贵的计算推迟到日志输出时再进行，例如传递指针而不是格式化后的字符串。这可以避免在禁用的日志行上进行不必要的工作。
- 对于昂贵的值，可以实现LogValuer接口，这样在输出时可以进行lazy加载计算。

```
// log/slog/value.go
// A LogValuer is any Go value that can convert itself into a Value for logging.
//
// This mechanism may be used to defer expensive operations until they are
// needed, or to expand a single value into a sequence of components.
type LogValuer interface {
LogValue() Value
}
```


最后，内置的Handler已经处理了原子写入的加锁。自定义Handler应该实现自己的加锁。

## 6. 小结

总体来说，slog正式版与之前实现相比，接口变化不大，功能也基本保持不变，但代码质量、性能、文档等有较大改进，符合预期。

slog填补了Go标准库在结构化日志支持上的短板，提供了简洁、易用、易扩展的API。相信随着slog的推广，可以逐步统一Go社区中的日志实践，也让更多人受益。

个人建议：新项目如果没有使用第三方日志包，可以直接采用slog，无需再考虑zap、zerolog等第三方选择。对于没有升级到Go 1.21版本的新项目，也可以使用exp/slog，目前exp/slog也已经与log/slog保持了同步。

本文涉及的示例代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/slog-examples-go121)下载。

## 7. 参考资料

- Proposal: Structured Logging – https://go.googlesource.com/proposal/+/master/design/56345-structured-logging.md
- slog包手册 – https://pkg.go.dev/log/slog
- Structured Logging with slog – https://go.dev/blog/slog
- A Guide to Writing slog Handlers – https://github.com/golang/example/blob/master/slog-handler-guide/README.md

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论