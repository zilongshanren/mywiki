---
title: 给expvarmon插上数据持久化的“翅膀”
url: https://tonybai.com/2021/04/14/expvarmon-save-and-convert-to-xlsx/
published: '2021-04-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 给expvarmon插上数据持久化的“翅膀”

![](../../assets/a8953dd6313cb33e.png)


[本文永久链接](https://tonybai.com/2021/04/14/expvarmon-save-and-convert-to-xlsx) – https://tonybai.com/2021/04/14/expvarmon-save-and-convert-to-xlsx

### 1. expvar包与expvarmon

Go在标准库中为暴露Go应用内部指标数据提供了标准的对外接口，这就是[expvar包](https://tip.golang.org/pkg/expvar/)。expvar包通过init函数将内置的expvarHandler(一个标准http HandlerFunc)注册到http包ListenAndServe创建的默认Server上。

```
// $GOROOT/src/expvar/expvar.go
func init() {
http.HandleFunc("/debug/vars", expvarHandler)
Publish("cmdline", Func(cmdline))
Publish("memstats", Func(memstats))
}
```


这样如果一个Go应用要想利用expvar默认暴露的内部指标数据，仅需做到两点：

- 以副作用方式导入expvar包

```
import _ "expvar"
```


- 启动默认HTTP Server

```
http.ListenAndServe("localhost:8080", nil)
```


我们来建立的使用expvar包暴露指标的最简单的例子：

```
// expvar_demo1.go
package main
import (
_ "expvar"
"net/http"
)
func main() {
http.ListenAndServe(":8080", nil)
}
```


这样expvar包的expvarHandler会自动响应到localhost:8080/debug/vars上的http请求：

```
$go build expvar_demo1.go
$./expvar_demo1 -w=1 -r=2
$curl localhost:8080/debug/vars
{
"cmdline": ["./expvar_demo1","-w=1","-r=2"],
"memstats": {"Alloc":227088,"TotalAlloc":227088,"Sys":71650320,"Lookups":0,"Mallocs":730,"Frees":13,"HeapAlloc":227088,"HeapSys":66715648,"HeapIdle":65937408,"HeapInuse":778240,"HeapReleased":65937408,"HeapObjects":717,"StackInuse":393216,"StackSys":393216,"MSpanInuse":37536,"MSpanSys":49152,"MCacheInuse":9600,"MCacheSys":16384,"BuckHashSys":3769,"GCSys":3783272,"OtherSys":688879,"NextGC":4473924,"LastGC":0,"PauseTotalNs":0,"PauseNs":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"PauseEnd":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"NumGC":0,"NumForcedGC":0,"GCCPUFraction":0,"EnableGC":true,"DebugGC":false,"BySize":[{"Size":0,"Mallocs":0,"Frees":0},{"Size":8,"Mallocs":14,"Frees":0},{"Size":16,"Mallocs":297,"Frees":0},{"Size":24,"Mallocs":32,"Frees":0},{"Size":32,"Mallocs":20,"Frees":0},{"Size":48,"Mallocs":105,"Frees":0},{"Size":64,"Mallocs":31,"Frees":0},{"Size":80,"Mallocs":9,"Frees":0},{"Size":96,"Mallocs":13,"Frees":0},{"Size":112,"Mallocs":2,"Frees":0},{"Size":128,"Mallocs":7,"Frees":0},{"Size":144,"Mallocs":3,"Frees":0},{"Size":160,"Mallocs":16,"Frees":0},{"Size":176,"Mallocs":5,"Frees":0},{"Size":192,"Mallocs":0,"Frees":0},{"Size":208,"Mallocs":33,"Frees":0},{"Size":224,"Mallocs":3,"Frees":0},{"Size":240,"Mallocs":0,"Frees":0},{"Size":256,"Mallocs":10,"Frees":0},{"Size":288,"Mallocs":8,"Frees":0},{"Size":320,"Mallocs":2,"Frees":0},{"Size":352,"Mallocs":10,"Frees":0},{"Size":384,"Mallocs":24,"Frees":0},{"Size":416,"Mallocs":7,"Frees":0},{"Size":448,"Mallocs":0,"Frees":0},{"Size":480,"Mallocs":1,"Frees":0},{"Size":512,"Mallocs":0,"Frees":0},{"Size":576,"Mallocs":3,"Frees":0},{"Size":640,"Mallocs":3,"Frees":0},{"Size":704,"Mallocs":5,"Frees":0},{"Size":768,"Mallocs":0,"Frees":0},{"Size":896,"Mallocs":7,"Frees":0},{"Size":1024,"Mallocs":7,"Frees":0},{"Size":1152,"Mallocs":10,"Frees":0},{"Size":1280,"Mallocs":4,"Frees":0},{"Size":1408,"Mallocs":1,"Frees":0},{"Size":1536,"Mallocs":0,"Frees":0},{"Size":1792,"Mallocs":5,"Frees":0},{"Size":2048,"Mallocs":1,"Frees":0},{"Size":2304,"Mallocs":2,"Frees":0},{"Size":2688,"Mallocs":2,"Frees":0},{"Size":3072,"Mallocs":0,"Frees":0},{"Size":3200,"Mallocs":0,"Frees":0},{"Size":3456,"Mallocs":0,"Frees":0},{"Size":4096,"Mallocs":4,"Frees":0},{"Size":4864,"Mallocs":0,"Frees":0},{"Size":5376,"Mallocs":1,"Frees":0},{"Size":6144,"Mallocs":1,"Frees":0},{"Size":6528,"Mallocs":0,"Frees":0},{"Size":6784,"Mallocs":0,"Frees":0},{"Size":6912,"Mallocs":0,"Frees":0},{"Size":8192,"Mallocs":1,"Frees":0},{"Size":9472,"Mallocs":0,"Frees":0},{"Size":9728,"Mallocs":0,"Frees":0},{"Size":10240,"Mallocs":8,"Frees":0},{"Size":10880,"Mallocs":0,"Frees":0},{"Size":12288,"Mallocs":0,"Frees":0},{"Size":13568,"Mallocs":0,"Frees":0},{"Size":14336,"Mallocs":0,"Frees":0},{"Size":16384,"Mallocs":0,"Frees":0},{"Size":18432,"Mallocs":0,"Frees":0}]}
}
```


如果我们不使用http.ListenAndServe建立的默认Server呢？expvar包也提供了相应的方法帮助你在自定义http server以及自定义请求路径上使用expvarHandler，我们看看下面示例：

```
// expvar_demo2.go
package main
import (
"expvar"
"net/http"
)
func main() {
mux := http.NewServeMux()
mux.Handle("/mydebug/myvars", expvar.Handler())
var server = &http.Server{
Addr: "localhost:8081",
Handler: mux,
}
server.ListenAndServe()
}
```


在这个示例中，我们利用http.ServeMux建立了expvarHandler响应的自定义路径(/mydebug/myvars)，并自定义了一个http.Server，这样当expvar_demo2运行起来后，我们就可以在localhost:8081/mydebug/myvars上获取该应用暴露的指标数据了。

通过expvar_demo1的输出结果，我们看到expvar默认将命令行字段和[runtime包的MemStats结构](https://tip.golang.org/pkg/runtime/#MemStats)暴露给外部。我们也可以自定义要暴露到外部的数据，expvar包提供了常用指标类型的便捷接口以帮助我们更容易的自定义要暴露到外部的数据，看下面示例：

```
// expvar_demo3.go
package main
import (
"expvar"
_ "expvar"
"net/http"
)
var (
total *expvar.Int
)
func init() {
total = expvar.NewInt("TotalRequest")
}
func main() {
http.Handle("/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
total.Add(1)
w.Write([]byte("hello, go\n"))
}))
http.ListenAndServe(":8080", nil)
}
```


在这个示例中，我们自定义了一个公开指标TotalRequest，用于描述该Server总共处理了多少个请求。我们用*expvar.Int作为TotalRequest的类型，expvar.Int类型提供了并发安全的Add方法，利用该方法我们可以对指标做运算。运行上面示例后，我们就可以获取TotalRequest这个指标了：

```
$curl localhost:8080/debug/vars
{
"TotalRequest": 2,
... ..
}
```


expvar包提供了对外的数据接口，但观测方式却是你决定的。图形化的观测方式是对人类友好的，一位名为[divan](https://github.com/divan)的gopher开发了[expvarmon](https://github.com/divan/expvarmon)工具，该工具可以在命令行终端以图形化的方式实时展示特定的指标数据的变化，我们可以执行如下命令实时查看应用指标变化；

```
$expvarmon -ports="http://localhost:8080/debug/vars" -i 1s
```


命令执行的效果如下：

![](../../assets/452c07d8dbd3cd2c.png)


如果不指定指标，那么expvarmon默认展示上述图中的memstats的几个指标！

expvarmon支持实时获取数据并展示数据的实时变动趋势。但有些时候，我们不仅要看实时趋势，可能还需要将数据存储起来便于事后分析。但expvarmon不支持将数据序列化到磁盘并做历史数据查看和分析。笔者曾提过[issue](https://github.com/divan/expvarmon/issues/37)，但作者似乎认为这个项目完成度已经很高了，该项目到2019年后就没有更新了。因此自然也没人理我的issue。我也只能自己动手丰衣足食了。

### 2. expvarmon的大致原理

要想基于expvarmon二次开发出支持数据持久化的版本，我们首先需要大致弄清楚expvarmon的工作原理，这里我将其工作原理大致总结为下面这幅示意图：

![](../../assets/6515f2cd99acc888.png)


- expvarmon执行时的两个命令行标志参数很重要：-ports和-vars。前者决定了expvarmon启动多少个Service(每个Service一个goroutine承载)：

```
// https://github.com/divan/expvarmon/blob/master/main.go
for _, port := range ports {
service := NewService(port, vars)
data.Services = append(data.Services, service)
}
```


后者用于指定expvarmon要实时显示的数据项：

```
// https://github.com/divan/expvarmon/blob/master/service.go
// NewService returns new Service object.
func NewService(url url.URL, vars []VarName) *Service {
values := make(map[VarName]*Stack)
for _, name := range vars { //根据vars建立存储对应var数据的Stack
values[VarName(name)] = NewStack()
}
... ...
}
```


- expvar定时采集各个目标app的指标数据

```
// https://github.com/divan/expvarmon/blob/master/service.go
func main() {
... ...
UpdateAll(ui, data)
for {
select {
case <-tick.C:
UpdateAll(ui, data)
case e := <-termui.PollEvents():
if e.Type == termui.KeyboardEvent && e.ID == "q" {
return
}
if e.Type == termui.ResizeEvent {
ui.Update(*data)
}
}
}
}
// UpdateAll collects data from expvars and refreshes UI.
func UpdateAll(ui UI, data *UIData) {
var wg sync.WaitGroup
for _, service := range data.Services {
wg.Add(1)
go service.Update(&wg) // 每个服务单独获取对应port的数据
}
wg.Wait()
data.LastTimestamp = time.Now()
ui.Update(*data) // 更新并刷新命令行终端ui
}
```


### 3. 持久化到csv文件中

大致了解expvarmon的运作原理后，我们就来设计和实现将expvarmon启动后针对每个port得到的指标数据存储到磁盘文件中留待后续分析之用，这里选择持久化到csv文件中，csv文件不仅便于直接打开并肉眼查看，也便于后续转换为其他文件格式，比如：Microsoft的excel文件。

下面是对expvarmon的设计与实现改动点：

- 增加-w命令行标志参数(布尔型)，如果为true，则持久化获取到的指标数据

```
// https://github.com/bigwhite/expvarmon/blob/master/main.go
var (
... ...
serialize = flag.Bool("w", false, "Serialize the data into a disk file")
)
```


- 在Service结构中增加持久化数据所需字段

```
// https://github.com/bigwhite/expvarmon/blob/master/service.go
// Service represents constantly updating info about single service.
type Service struct {
... ...
vars []VarName
// for serializing the data
// controlled by cmd option: serialize
f *os.File
w *csv.Writer // csv writer
}
```


vars用于存储该Service对应的指标名；f为文件名；w是创建的csv.Writer结构。

- 在创建Service的时候，根据-w的值来决定是否创建持久化文件：

```
// https://github.com/bigwhite/expvarmon/blob/master/service.go
func NewService(url url.URL, vars []VarName) *Service {
... ...
if *serialize {
f, err := os.Create(s.Name + ".csv")
if err != nil {
panic(err)
}
s.f = f
s.w = csv.NewWriter(f)
// write first record: category line
record := []string{"time"}
for _, v := range vars {
record = append(record, string(v))
}
s.w.Write(record)
s.w.Flush()
}
... ...
}
```


我们看到：当-w为true时，NewService创建了持久化文件，并用Service的Name+.csv后缀为其命名。文件创建成功后，我们将写入第一行csv数据，这一行数据为数据类别，就像下面这样：

```
// 10.10.195.133:8080.csv
time,mem:memstats.Alloc,mem:memstats.Sys,mem:memstats.HeapAlloc,mem:memstats.HeapInuse,duration:memstats.PauseNs,duration:memstats.PauseTotalNs
```


除了第一列为时间(time)外，其余列都是以指标名命名的，如：mem:memstats.Alloc。

- 我们在Service的Update方法中定时写入指标数据

```
// https://github.com/bigwhite/expvarmon/blob/master/service.go
// Update updates Service info from Expvar variable.
func (s *Service) Update(wg *sync.WaitGroup) {
... ...
if *serialize {
// serialize the values to csv
tm := time.Now().Format("2006-01-02 15:04:05")
values := []string{tm}
for _, name := range s.vars {
values = append(values, s.Value(name))
}
s.w.Write(values)
s.w.Flush()
}
}
```


- 增加Service的Close方法以优雅关闭csv文件

和原expvarmon不同的是，我们二次开发的expvarmon在-w为true时会为每个Service创建一个磁盘文件，这样我们就需要记着在适当的时候优雅的关闭这些csv格式的磁盘文件。

```
// https://github.com/bigwhite/expvarmon/blob/master/service.go
// Close does some cleanup before service exit
func (s *Service) Close() {
if *serialize {
if s.f != nil {
s.f.Close()
}
}
}
```


我们在程序退出前通过defer来调用Service的关闭方法：

```
// https://github.com/bigwhite/expvarmon/blob/master/main.go
func main() {
... ...
// Init UIData
data := NewUIData(vars)
for _, port := range ports {
service := NewService(port, vars)
data.Services = append(data.Services, service)
}
defer func() {
// close service before program exit
for _, service := range data.Services {
service.Close()
}
}()
... ...
}
```


按照上述这几点改造后，我们再执行如下命令：

```
$expvarmon -ports="http://10.10.195.133:8080/debug/vars" -i 1s -w=true
```


我们将得到10.10.195.133:8080.csv文件(如果-ports由多个值组成，那么将生成多个.csv文件)，内容如下：

```
$cat 10.10.195.133:8080.csv
time,mem:memstats.Alloc,mem:memstats.Sys,mem:memstats.HeapAlloc,mem:memstats.HeapInuse,duration:memstats.PauseNs,duration:memstats.PauseTotalNs
2021-04-09 16:55:58,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:55:59,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:00,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:01,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:02,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:03,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:04,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:05,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:06,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:07,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:08,16MB,88MB,16MB,25MB,159µs,1m50s
2021-04-09 16:56:09,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:10,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:11,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:12,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:13,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:14,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:15,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:16,15MB,88MB,15MB,25MB,159µs,1m50s
2021-04-09 16:56:17,15MB,88MB,15MB,25MB,159µs,1m50s
... ...
```


### 4. 将csv数据转换为excel图表

csv存储了各个应用暴露给外部的分时指标数据，但要对这些数据进行分析，我们需要将csv中的数据以可视化的形式展示出来，而excel图表是一个不错的选择。

为此，我建立了一个[csv2xls](https://github.com/bigwhite/csv2xls)的工具项目，专门用来将expvarmon生成的csv文件转换为excel图表。

csv2xls的用法如下：

```
$./csv2xls -h
Usage of ./csv2xls:
-col int
the column which we draw a chart based on, default: 1 (range 0~max-1) (default 1)
-i string
the name of csv file
-o string
the name of xls file
Examples:
./csv2xls -i xxx.csv
./csv2xls -i xxx.csv -o yyy.xlsx
```


csv2xls将csv文件中的数据读取并存储在xls中，并支持基于其中某列数据生成对应的折线图。以上面的10.10.195.133:8080.csv为例，我们通过命令：csv2xls -i 10.10.195.133:8080.csv即可生成如下excel图表文件：

![](https://tonybai.com/wp-content/uploads/BlogImages/expvarmon-save-and-convert-to-xlsx-4.png)


csv2xls使用p著名的excelize(go语言execl操作库)](github.com/360EntSecGroup-Skylar/excelize)生成excel文件。


### 5. 小结

至此，我们给expvarmon插上数据持久化的“翅膀”的目的算是初步达到了。但是由于app指标数据千变万化，expvarmon使用的[byten包](https://tonybai.com/github.com/pyk/byten)又给解析指标数据单位带来了一些复杂性，因此csv2xls还不完善，后续还有很大的改进的空间。

- 支持公开指标持久化的expvarmon的代码在
[这里](https://github.com/bigwhite/expvarmon)(https://github.com/bigwhite/expvarmon)。 - csv2xls的代码在
[这里](https://github.com/bigwhite/csv2xls)(https://github.com/bigwhite/csv2xls)。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论