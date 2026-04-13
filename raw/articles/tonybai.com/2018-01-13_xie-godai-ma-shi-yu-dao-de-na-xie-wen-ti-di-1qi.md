---
title: 写Go代码时遇到的那些问题[第1期]
url: https://tonybai.com/2018/01/13/the-problems-i-encountered-when-writing-go-code-issue-1st/
published: '2018-01-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 写Go代码时遇到的那些问题[第1期]

程序员步入“大龄”，写代码的节奏也会受到影响。以前是长时间持续地写，现在写代码的节奏变成了“波浪形”：即写一段时间，歇一段时间。当然这里的“歇”并不是真的歇，而是做其他事情了，比如：回顾、整理与总结。

平时写[Go](http://tonybai.com/tag/go)代码，时不时就遇到一些问题，或是写出一些让自己还算满意的代码，这里全部列为“问题”行列。这些“问题”(以及其解决方法)往往比较“小”、比较“碎片”，不适合以自己“擅长”的“长篇”风格写出来分享，也不知道以什么样的“题目”去分享更好，但这样的“问题”在日常又总是会遇到。考量来考量去，赶脚还是用一系列的文章去分享比较合适，即每隔一段时间，积累了一些问题后，就写一篇文章分享一下。

这是第一篇，后续不确定时间地(注意：这不是weekly的哦)发布新篇，直到没啥可写了或不写[Go代码](https://golang.org/)了^0^。

## 一、Go包管理

首当其冲的是[Go包管理](http://tonybai.com/2017/06/08/first-glimpse-of-dep/)。

### 1. vendor的“传染性”带来的问题

Go从[1.5版本](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)开始引入[vendor机制](http://tonybai.com/2015/07/31/understand-go15-vendor/)以辅助Go的包管理。随着[vendor](http://tonybai.com/2015/07/31/understand-go15-vendor/)机制的应用日益广泛，我们会发现：有些时候你要是不用vendor（在不借助第三方包管理工具的前提下），很多编译问题是解决不了的，或者说**vendor机制有一定的传染性**。比如下面这个例子：

![img{512x368}](../../assets/235fb16d09841905.png)


如上图所示：app_c包直接调用lib_a包中函数，并使用了lib_b包(v0.2版本)中的类型，lib_a包vendor了lib_b包(v0.1版本)。在这样的情况下，当我们编译app_c包时，是否会出现什么问题呢？我们一起来看一下这个例子：

```
在$GOPATH/src路径下面我们查看当前示例的目录结构：
$tree
├── app_c
├── c.go
├── lib_a
├── a.go
└── vendor
└── lib_b
└── b.go
├── lib_b
├── b.go
```


各个源文件的示例代码如下：

```
//lib_a/a.go
package lib_a
import "lib_b"
func Foo(b lib_b.B) {
b.Do()
}
//lib_a/vendor/lib_b/b.go
package lib_b
import "fmt"
type B struct {
}
func (*B) Do() {
fmt.Println("lib_b version:v0.1")
}
// lib_b/b.go
package lib_b
import "fmt"
type B struct {
}
func (*B) Do() {
fmt.Println("lib_b version:v0.2")
}
// app_c/c.go
package app_c
import (
"lib_a"
"lib_b"
)
func main() {
var b lib_b.B
lib_a.Foo(b)
}
```


进入app_c目录，执行编译命令：

```
$go build c.go
# command-line-arguments
./c.go:10:11: cannot use b (type "lib_b".B) as type "lib_a/vendor/lib_b".B in argument to lib_a.Foo
```


我们看到go compiler认为：**app_c包main函数中定义的变量b的类型(lib_b.B)与lib_a.Foo的参数b的类型(lib_a/vendor/lib_b.B)是不同的类型，不能相互赋值**。

### 2. 通过手工vendor解决上述问题

这个例子非常有代表性，那么怎么解决这个问题呢？**我们需要在app_c中也使用vendor机制**，即将app_c所需的lib_a和lib_b都vendor到app_c中。

```
按照上述思路解决后的示例的目录结构：
$tree
├── app_c
├── c.go
└── vendor
├── lib_a
│ └── a.go
└── lib_b
└── b.go
├── lib_a
├── a.go
└── vendor
└── lib_b
└── b.go
├── lib_b
├── b.go
```


不过要注意的是：app_c/vendor下面的库中的vendor目录要被删除掉的，我们只保留顶层vendor。现在我们再来编译c.go就可以顺利编译通过了。

### 3. 使用dep

对于demo或规模不大、依赖不多的小项目，手工进行vendor还是蛮有效的。一个可行的手工vendor步骤：

- 在项目顶层创建vendor；
- 通过go list -json ./…查看项目依赖 “deps”;
- 逐一下载各个依赖，并确定要使用的版本(tag or branch)，将特定版本cp到顶层的vendor目录下，至少要做到vendor所有直接依赖包；
- 可以在顶层vendor下创建dependencies.list文件，手工记录vendor的依赖包列表以及版本信息。

但是对于稍大一点的项目，手工vendor就会费时费力，有时仅能顾及到“直接依赖包”的vendor，“数不清”的间接依赖/传递依赖会让你头疼不已。这个时候我们会想到使用第三方的包管理工具。在现在这个时间点，如果你再和我提[godep](http://tonybai.com/2014/10/30/a-hole-of-godep/)、[glide](https://github.com/Masterminds/glide)等，那你就out了，[dep](https://github.com/golang/dep)是首选。

在[《初窥dep》](http://tonybai.com/2017/06/08/first-glimpse-of-dep/)一文中，我们对当时的dep进行了较为详细的工作机制分析，如今dep已经演化到0.3.2版本了，并且commandline交互接口已经稳定了。dep init默认采用network mode，即到各个依赖包的upstream上查找版本信息并下载；dep init也支持-gopath模式，即在本地$GOPATH下获取依赖包的元信息并分析。

不过，对于在国内的gopher，dep init的过程依然是一道很难逾越的“坎”。问题多出在：第三方包特别喜欢依赖的golang.org/x下的那些包，常见的包有：net、text、crypto等。golang.org/x/{package_name}仅仅是[canonical import path](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)，真正的代码存储在go.googlesource.com上，而在国内get这些包，我们会得到如下错误：

```
$go get -u golang.org/x/net
package golang.org/x/net: unrecognized import path "golang.org/x/net" (https fetch: Get https://golang.org/x/net?go-get=1: dial tcp 216.239.37.1:443: i/o timeout)
```


这将导致dep init命令长期阻塞，给国内gopher带来极为糟糕的体验。更为糟糕的是，即便是采用了一些fan qiang方式，有些时候go.googlesource.com依旧无法连接。因此，我一般的作法是在国外的主机上进行dep init，然后将vendor checkin到代码仓库中。这样其他人在得到你的代码后，也不需dep ensure(也要下载依赖包)即可实现reproducable build。

有些朋友可能会将从github.com/golang上下载的net包来代替golang.org/x/net，并使用dep init -v -gopath=true的模式。但这种替换会被dep分析出来，因为dep会尝试去读取代码库的元信息，结果依然会是失败。

## 二. 非容器化应用的本地日志管理

在[微服务](http://tonybai.com/2018/01/03/an-intro-of-microservices-governance-by-istio/)、容器化大行其道的今天，单个应用的日志处理变得简单化了，应用只需要将要输出的信息输出到stdout、stderr上即可。[logging基础设施](http://tonybai.com/2017/03/03/implement-kubernetes-cluster-level-logging-with-fluentd-and-elasticsearch-stack/)会收集容器日志，并做后续归档、分析、过滤、查找、展示等处理。但是在非容器环境、在没有统一的logging基础设施的前提下，日志的管理就又交还给应用自身了。浅显的日志管理至少要包含日志的rotate(轮转)、压缩归档以及历史归档文件的处理吧。这里我们就来探讨一下这个问题的几种解决方法。

### 1. 托管给logrotate

在主流的Linux发行版上都有一个[logrotate](https://github.com/logrotate/logrotate)工具程序，应用程序可以借助该工具对应用输出的日志进行rotate、压缩、归档和删除历史归档日志，这样可大幅简化应用的日志输出逻辑，应用仅需要将日志输出到一个具名文件中即可，其余都交给logrotate处理。

我们建立一个输出log的demo app:

```
//testlogrotate.go
package main
import (
"log"
"os"
"time"
)
func main() {
file, err := os.OpenFile("./app.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
if err != nil {
log.Fatalln("Failed to open log file:", err)
}
defer file.Close()
logger := log.New(file,
"APP_LOG_PREFIX: ",
log.Ldate|log.Ltime|log.Lshortfile)
for {
logger.Println("test log")
time.Sleep(time.Second * 1)
}
}
```


该程序每隔1s向app.log文件写入一行日志。

```
# tail -f app.log
APP_LOG_PREFIX: 2018/01/12 19:14:43 testlogrotate.go:22: test log
APP_LOG_PREFIX: 2018/01/12 19:14:44 testlogrotate.go:22: test log
APP_LOG_PREFIX: 2018/01/12 19:14:45 testlogrotate.go:22: test log
APP_LOG_PREFIX: 2018/01/12 19:14:46 testlogrotate.go:22: test log
APP_LOG_PREFIX: 2018/01/12 19:14:47 testlogrotate.go:22: test log
... ..
```


接下来，我们就要用logrotate对该app.log文件进行定期的rotate、压缩归档以及历史归档清理了，我们需要为app.log定制一个配置。logrotate读取配置的目录是/etc/logrotate.d，我们在/etc/logrotate.d下面建立applog文件(当然你也可以在任意其他目录下建立配置文件，不过其他目录下的配置文件无法被logrotate的cron任务感知到，不过这样的配置文件可以手工与logrotate程序结合使用)，文件内容如下：

```
# cat /etc/logrotate.d/applog
/data/tonybai/test/go/app.log {
rotate 7
daily
size=10M
compress
dateext
missingok
copytruncate
}
```


这个配置的大致含义是：

* 每天rotate一次

* 日志保留7天(rotate=7, daily rotate)

* 归档日志采用压缩形式

* 归档日志带有时间戳

* 当当前日志size > 10M时，会进行一次rotate

* 最重要的是copytruncate这个配置，这个配置的含义是将app.log当前日志copy到一个归档文件后，对app.log进行truncate操作，这样app.log的open file fd并不改变，不会影响到原app继续写日志。当然这个copy的过程中可能会有少量日志lost。

如果你觉得logrotate在时间粒度和精确度上依旧无法满足你的要求，你可以结合crontab自己定时执行logrotate(crontab -e编辑crontab的配置)：

```
# logrotate -f /etc/logrotate.d/applog
```


下面是rotate时，tail -f中看到的情况：

```
APP_LOG_PREFIX: 2018/01/12 20:25:59 testlogrotate.go:21: test log
APP_LOG_PREFIX: 2018/01/12 20:26:00 testlogrotate.go:21: test log
tail: app.log: file truncated
APP_LOG_PREFIX: 2018/01/12 20:26:01 testlogrotate.go:21: test log
APP_LOG_PREFIX: 2018/01/12 20:26:02 testlogrotate.go:21: test log
APP_LOG_PREFIX: 2018/01/12 20:26:03 testlogrotate.go:21: test log
```


可以看到tail可以检测到file truncate事件。

### 2. 使用自带rotate功能log包

在go技术栈中[众多的logging包](https://github.com/avelino/awesome-go#logging)中，[logrus](https://github.com/sirupsen/logrus)是使用较为广泛的一个包，支持与std库 log API兼容的结构化日志、支持logging level设置、支持安全地并发写日志以及hook等。但logrus自身并不具备auto rotate功能，需要结合其他工具才能实现。这里用[nate finch](https://npf.io/)的[lumberjack](https://github.com/natefinch/lumberjack)，我们来看一个简单的例子：

```
// testlogrusAndlumberjack.go
package main
import (
"time"
"github.com/natefinch/lumberjack"
log "github.com/sirupsen/logrus"
)
func main() {
logger := log.New()
logger.SetLevel(log.DebugLevel)
logger.Formatter = &log.JSONFormatter{}
logger.Out = &lumberjack.Logger{
Filename: "./app.log",
MaxSize: 1, // megabytes
MaxBackups: 3,
MaxAge: 1, //days
Compress: true, // disabled by default
LocalTime: true,
}
for {
logger.Debug("this is an app log")
time.Sleep(2 * time.Millisecond)
}
}
```


从代码里，我们看到：通过设置logger.Out为一个lumberjack.Logger的实例，将真正的Write交给了lumberjack.Logger，而后者实现了log的rotate功能，与logrotate的配置有些类似，这里也包括日志最大size设定、保留几个归档日志、是否压缩、最多保留几天的日志。不过当前lumberjack实现的rotate判断条件仅有一个：MaxSize，而没有定时rotate的功能。

我们执行一下该程序，等待一会，并停止程序。可以看到目录下的日志文件发生了变化：

```
$ls -lh
-rw-r--r-- 1 tony staff 3.7K Jan 12 21:03 app-2018-01-12T21-03-42.844.log.gz
-rw-r--r-- 1 tony staff 3.7K Jan 12 21:04 app-2018-01-12T21-04-15.017.log.gz
-rw-r--r-- 1 tony staff 457K Jan 12 21:04 app.log
```


lumberjack每发现app.log大于MaxSize就会rotate一次，这里已经有了两个归档压缩文件，并被lumberjack赋予了时间戳和序号，便于检索和查看。

### 3. 关于对日志level的支持以及loglevel的热更新

对日志level的支持是logging包选项的一个重要参考要素。logrus支持设置六个log level：

```
PanicLevel
FatalLevel
ErrorLevel
WarnLevel
InfoLevel
DebugLevel
```


并且对不同的leve的日志，logrus支持设定hook分别处理，比如：放到不同的日志文件中。通过logrus.Logger.SetLevel方法可以运行时更新logger实例的loglevel，这个特性可以让我们在生产环境上通过临时打开debuglevel日志对程序进行更细致的观察，以定位问题，快速定位bug，非常实用。

结合[系统Signal](http://tonybai.com/2012/09/21/signal-handling-in-go/)机制，我们可以通过USR1和USR2两个signal来运行时调整程序的日志级别，我们来看一个示例：

![img{512x368}](../../assets/6c755037a0be9c38.png)


从上面图片可以看到，日志级别从高到低分别为：Panic, Fatal, Error, Warn，Info和Debug。如果要调高log level，我们向程序发送USR1来调高日志级别，相反，发送USR2来调低日志级别：

我们在testlogrusAndlumberjack.go上面做些修改：增加对signal: USR1和USR2的监听处理，同时循环打印各种级别日志，以后续验证日志级别的动态调整：

```
// testloglevelupdate.go
import (
log "github.com/sirupsen/logrus"
... ...
)
func main() {
logger := log.New()
logger.SetLevel(log.DebugLevel)
logger.Formatter = &log.JSONFormatter{}
logger.Out = &lumberjack.Logger{
Filename: "./app.log",
MaxSize: 1, // megabytes
MaxBackups: 3,
MaxAge: 1, //days
Compress: true, // disabled by default
LocalTime: true,
}
c := make(chan os.Signal, 1)
signal.Notify(c, syscall.SIGUSR1, syscall.SIGUSR2)
go watchAndUpdateLoglevel(c, logger)
for {
logger.Debug("it is debug level log")
logger.Info("it is info level log")
logger.Warn("it is warning level log")
logger.Error("it is warning level log")
time.Sleep(5 * time.Second)
}
}
```


watchAndUpdateLoglevel函数用于监听程序收到的系统信号，并根据信号类型调整日志级别：

```
// testloglevelupdate.go
func watchAndUpdateLoglevel(c chan os.Signal, logger *log.Logger) {
for {
select {
case sig := <-c:
if sig == syscall.SIGUSR1 {
level := logger.Level
if level == log.PanicLevel {
fmt.Println("Raise log level: It has been already the most top log level: panic level")
} else {
logger.SetLevel(level - 1)
fmt.Println("Raise log level: the current level is", logger.Level)
}
} else if sig == syscall.SIGUSR2 {
level := logger.Level
if level == log.DebugLevel {
fmt.Println("Reduce log level: It has been already the lowest log level: debug level")
} else {
logger.SetLevel(level + 1)
fmt.Println("Reduce log level: the current level is", logger.Level)
}
} else {
fmt.Println("receive unknown signal:", sig)
}
}
}
}
```


运行该程序后，你可以通过如下命令向程序发送信号：

```
$ kill -s USR1|USR2 程序的进程号
```


通过日志的输出，可以判断出日志级别调整是否生效，这里就不细说了。

不过这里还要提一点的是logrus目前对于输出的日志中双引号内的一些字符（比如双引号自身）会做转义处理，即在前面加上“反斜杠”，比如：

```
{"level":"debug","msg":"receive a msg: {\"id\":\"000002\",\"ip\":\"201.108.111.117\"}","time":"2018-01-11T20:42:31+08:00"}
```


这个问题让日志可读性大幅下降，但这个问题似乎尚处于无解状态

## 三. json marshal json string时的转义问题

之前写过这样一个function，用于统一marshal内部组件通信的应答消息：

```
func marshalResponse(code int, msg string, result interface{}) (string, error) {
m := map[string]interface{}{
"code": 0,
"msg": "ok",
"result": result,
}
b, err := json.Marshal(&m)
if err != nil {
return "", err
}
return string(b), nil
}
```


不过当result类型为json string时，这个函数的输出带有转义反斜线：

```
//testmarshaljsonstring.go
... ...
func main() {
s, err := marshalResponse(0, "ok", `{"name": "tony", "city": "shenyang"}`)
if err != nil {
fmt.Println("marshal response error:", err)
return
}
fmt.Println(s)
}
```


运行这个程序输出：

```
{"code":0,"msg":"ok","result":"{\"name\": \"tony\", \"city\": \"shenyang\"}"}
```


怎么解决掉这个问题呢？json提供了一种RawMessage类型，本质上就是[]byte，我们将json string转换成RawMessage后再传给json.Marshal就可以解决掉这个问题了：

```
//testmarshaljsonstring.go
func marshalResponse1(code int, msg string, result interface{}) (string, error) {
s, ok := result.(string)
var m = map[string]interface{}{
"code": 0,
"msg": "ok",
}
if ok {
rawData := json.RawMessage(s)
m["result"] = rawData
} else {
m["result"] = result
}
b, err := json.Marshal(&m)
if err != nil {
return "", err
}
return string(b), nil
}
func main() {
s, err = marshalResponse1(0, "ok", `{"name": "tony", "city": "shenyang"}`)
if err != nil {
fmt.Println("marshal response1 error:", err)
return
}
fmt.Println(s)
}
```


再运行这个程序的输出结果就变成了我们想要的结果了：

```
{"code":0,"msg":"ok","result":{"name":"tony","city":"shenyang"}}
```


## 四. 如何在main包之外使用flag.Parse后的命令行flag变量

我们在使用Go开发交互界面不是很复杂的command-line应用时，一般都会使用std中的flag包进行命令行flag解析，并在main包中校验和使用flag.Parse后的flag变量。常见的套路是这样的：

```
//testflag1.go
package main
import (
"flag"
"fmt"
)
var (
endpoints string
user string
password string
)
func init() {
flag.StringVar(&endpoints, "endpoints", "127.0.0.1:2379", "comma-separated list of etcdv3 endpoints")
flag.StringVar(&user, "user", "", "etcdv3 client user")
flag.StringVar(&password, "password", "", "etcdv3 client password")
}
func usage() {
fmt.Println("flagdemo-app is a daemon application which provides xxx service.\n")
fmt.Println("Usage of flagdemo-app:\n")
fmt.Println("\t flagdemo-app [options]\n")
fmt.Println("The options are:\n")
flag.PrintDefaults()
}
func main() {
flag.Usage = usage
flag.Parse()
// ... ...
// 这里我们可以使用endpoints、user、password等flag变量了
}
```


在这样的一个套路中，我们可以在main包中直接使用flag.Parse后的flag变量了。但有些时候，我们需要在main包之外使用这些flag vars(比如这里的：endpoints、user、password)，怎么做呢，有几种方法，我们逐一来看看。

### 1. 全局变量法

我想大部分gopher第一个想法就是使用全局变量，即建立一个config包，包中定义全局变量，并在main中将这些全局变量绑定到flag的Parse中：

```
$tree globalvars
globalvars
├── config
│ └── config.go
├── etcd
│ └── etcd.go
└── main.go
// flag-demo/globalvars/config/config.go
package config
var (
Endpoints string
User string
Password string
)
// flag-demo/globalvars/etcd/etcd.go
package etcd
import (
"fmt"
"../config"
)
func EtcdProxy() {
fmt.Println(config.Endpoints, config.User, config.Password)
//... ....
}
// flag-demo/globalvars/main.go
package main
import (
"flag"
"fmt"
"time"
"./config"
"./etcd"
)
func init() {
flag.StringVar(&config.Endpoints, "endpoints", "127.0.0.1:2379", "comma-separated list of etcdv3 endpoints")
flag.StringVar(&config.User, "user", "", "etcdv3 client user")
flag.StringVar(&config.Password, "password", "", "etcdv3 client password")
}
.... ...
func main() {
flag.Usage = usage
flag.Parse()
go etcd.EtcdProxy()
time.Sleep(5 * time.Second)
}
```


可以看到，我们在绑定cmdline flag时使用的是config包中定义的全局变量。并且在另外一个etcd包中，使用了这些变量。

我们运行这个程序：

```
./main -endpoints 192.168.10.69:2379,10.10.12.36:2378 -user tonybai -password xyz123
192.168.10.69:2379,10.10.12.36:2378 tonybai xyz123
```


不过这种方法要**注意这些全局变量值在Go包初始化过程的顺序**，比如：如果在etcd包的init函数中使用这些全局变量，那么你得到的各个变量值将为空值，因为etcd包的init函数在main.init和main.main之前执行，这个时候绑定和Parse都还未执行。

### 2. 传参法

第二种比较直接的想法就是将Parse后的flag变量以参数的形式、以某种init的方式传给其他要使用这些变量的包。

```
$tree parampass
parampass
├── etcd
│ └── etcd.go
└── main.go
// flag-demo/parampass/etcd/etcd.go
package etcd
... ...
func EtcdProxy(endpoints, user, password string) {
fmt.Println(endpoints, user, password)
}
// flag-demo/parampass/main.go
package main
import (
"flag"
"fmt"
"time"
"./etcd"
)
var (
endpoints string
user string
password string
)
func init() {
flag.StringVar(&endpoints, "endpoints", "127.0.0.1:2379", "comma-separated list of etcdv3 endpoints")
flag.StringVar(&user, "user", "", "etcdv3 client user")
flag.StringVar(&password, "password", "", "etcdv3 client password")
}
... ...
func main() {
flag.Usage = usage
flag.Parse()
go etcd.EtcdProxy(endpoints, user, password)
time.Sleep(5 * time.Second)
}
```


这种方法非常直观，这里就不解释了。但注意：一旦使用这种方式，一定需要在main包与另外的包之间建立某种依赖关系，至少main包会import那些使用flag变量的包。

### 3. 配置中心法

全局变量法直观，而且一定程度上解除了其他包与main包的耦合。但是有一个问题，那就是一旦flag变量发生增减，config包就得相应添加或删除变量定义。是否有一种方案可以在flag变量发生变化时，config包不受影响呢？我们可以用配置中心法。所谓的配置中心法，就是实现一个与flag变量类型和值无关的通过配置存储结构，我们在main包中向该结构注入parse后的flag变量，在其他需要flag变量的包中，我们使用该结构得到flag变量的值。

```
$tree configcenter
configcenter
├── config
│ └── config.go
└── main.go
//flag-demo/configcenter/config/config.go
package config
import (
"log"
"sync"
)
var (
m map[string]interface{}
mu sync.RWMutex
)
func init() {
m = make(map[string]interface{}, 10)
}
func SetString(k, v string) {
mu.Lock()
m[k] = v
mu.Unlock()
}
func SetInt(k string, i int) {
mu.Lock()
m[k] = i
mu.Unlock()
}
func GetString(key string) string {
mu.RLock()
defer mu.RUnlock()
v, ok := m[key]
if !ok {
return ""
}
return v.(string)
}
func GetInt(key string) int {
mu.RLock()
defer mu.RUnlock()
v, ok := m[key]
if !ok {
return 0
}
return v.(int)
}
func Dump() {
log.Println(m)
}
// flag-demo/configcenter/main.go
package main
import (
"flag"
"fmt"
"time"
"./config"
)
var (
endpoints string
user string
password string
)
func init() {
flag.StringVar(&endpoints, "endpoints", "127.0.0.1:2379", "comma-separated list of etcdv3 endpoints")
flag.StringVar(&user, "user", "", "etcdv3 client user")
flag.StringVar(&password, "password", "", "etcdv3 client password")
}
... ...
func main() {
flag.Usage = usage
flag.Parse()
// inject flag vars to config center
config.SetString("endpoints", endpoints)
config.SetString("user", user)
config.SetString("password", password)
time.Sleep(5 * time.Second)
}
```


我们在main中使用config的SetString将flag vars注入配置中心。之后，我们在其他包中就可以使用：GetString、GetInt获取这些变量值了，这里就不举例了。

### 4、“黑魔法”: flag.Lookup

flag包中提供了一种类似上述的”配置中心”的机制，但这种机制不需要我们显示注入“flag vars”了，我们只需按照flag提供的方法在其他package中读取对应flag变量的值即可。

```
$tree flaglookup
flaglookup
├── etcd
│ └── etcd.go
└── main.go
// flag-demo/flaglookup/main.go
package main
import (
"flag"
"fmt"
"time"
"./etcd"
)
var (
endpoints string
user string
password string
)
func init() {
flag.StringVar(&endpoints, "endpoints", "127.0.0.1:2379", "comma-separated list of etcdv3 endpoints")
flag.StringVar(&user, "user", "", "etcdv3 client user")
flag.StringVar(&password, "password", "", "etcdv3 client password")
}
......
func main() {
flag.Usage = usage
flag.Parse()
go etcd.EtcdProxy()
time.Sleep(5 * time.Second)
}
// flag-demo/flaglookup/etcd/etcd.go
package etcd
import (
"flag"
"fmt"
)
func EtcdProxy() {
endpoints := flag.Lookup("endpoints").Value.(flag.Getter).Get().(string)
user := flag.Lookup("user").Value.(flag.Getter).Get().(string)
password := flag.Lookup("password").Value.(flag.Getter).Get().(string)
fmt.Println(endpoints, user, password)
}
```


运行该程序：

```
$go run main.go -endpoints 192.168.10.69:2379,10.10.12.36:2378 -user tonybai -password xyz123
192.168.10.69:2379,10.10.12.36:2378 tonybai xyz123
```


输出与我们的预期是一致的。

### 5、对比

我们用一幅图来对上述几种方法进行对比：

![img{512x368}](../../assets/7a6cae039dfd9572.png)


很显然，经过简单包装后，“黑魔法”flaglookup应该是比较优异的方案。main包、other packages只需import flag即可。

注意：**在main包中定义exported的全局flag变量并被其他package import的方法是错误的，很容易造成import cycle问题。并且任何其他package import main包都是不合理的**。

## 五. 小结

以上是这段时间遇到的、收集的一些Go问题以及solution。注意：**这些solution不一定是最优方案哦！如果您有更好方案，欢迎批评指正和互动交流**。

本文章中涉及到的所有源码和配置文件在[这里](https://github.com/bigwhite/experiments/tree/master/writing-go-code-issues/1st-issue)可以下载到。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

因为lumberjack不支持按时间滚动特意搞了个 io.WriteCloser https://github.com/fpay/rollout

“对于输出的日志中双引号内的一些字符（比如双引号自身）会做转义处理” 这个是json格式限制的。我现在的方案是尽量记录结构化的日志，后面入到ES之类的分析工具里比较容易处理。

感谢分享！已推荐到《开发者头条》：https://toutiao.io/posts/8d50gz 欢迎点赞支持！

欢迎订阅《go》https://toutiao.io/subjects/18464