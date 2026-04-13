---
title: 使用section.key的形式读取ini配置项
url: https://tonybai.com/2021/07/10/read-ini-config-item-by-passing-section-key/
published: '2021-07-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用section.key的形式读取ini配置项

![](../../assets/a953f1019be5c462.png)


[本文永久链接](https://tonybai.com/2021/07/10/read-ini-config-item-by-passing-section-key) – https://tonybai.com/2021/07/10/read-ini-config-item-by-passing-section-key

配置文件读取是很多Go项目必备的功能，这方面社区提供的方案也相对成熟稳定。但之前写这部分代码时除了使用了针对不同配置文件格式（比如：ini、toml等）的驱动包之外，很少直接使用第三方包对读取出的配置项的值进行管理。于是我们就面对这样一个问题：其他包如果要使用这些被读取出的配置项的值该如何做呢？我们以读取ini格式承载的配置文件为例，来简单说说。

### 1. 全局变量法

这是最粗糙的方法，但却是最易理解的方法。我们建立一个config包，在main函数中读取配置文件并将读取到的配置项信息存放在config包的一个导出的全局变量中，这样其他包要想获取配置文件中配置项的信息，直接通过该全局变量读取即可。下面的demo1就是一个使用全局变量组织读取出的配置项信息的示例项目，其代码结构如下：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo1
demo1
├── conf
│ └── demo.ini
├── go.mod
├── go.sum
├── main.go
└── pkg
├── config
│ └── config.go
└── pkg1
└── pkg1.go
```


demo1中的conf/demo.ini中存储了下面这些配置项信息：

```
$cat demo.ini
[server]
id = 100001
port = 23333
tls_port = 83333
[log]
level = 0; info:0, warn: 1, error: 2, dpanic:3, panic:4, fatal: 5, debug: -1
compress = true ; indicate whether the rotated log files should be compressed using gzip (default true)
path = "./log/demo.log" ; if it is empty, we use default logger(to stderr)
max_age = 3 ; the maximum number of days to retain old log files based on the timestamp encoded in their filename
maxbackups = 7 ; the maximum number of old log files to retain (default 7)
maxsize = 100 ; the maximum size in megabytes of the log file before it gets rotated (default 100)
[debug]
profile_on = true ;add profile web server for app to enable pprof through web
profile_port = 8091 ; profile web port
```


我们通过config包读取该配置文件（基于github.com/go-ini/ini包实现ini配置文件读取）：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo1/pkg/config/config.go
package config
import (
ini "github.com/go-ini/ini"
)
type Server struct {
Id string `ini:""`
Port int `ini:"port"`
TlsPort int `ini:"tls_port"`
}
type Log struct {
Compress bool `ini:"compress"`
LogPath string `ini:"path"`
MaxAge int `ini:"max_age"`
MaxBackups int `ini:"maxbackups"`
MaxSize int `ini:"maxsize"`
}
type Debug struct {
ProfileOn bool `ini:"profile_on"`
ProfilePort string `ini:"profile_port"`
}
type IniConfig struct {
Server `ini:"server"`
Log `ini:"log"`
Debug `ini:"debug"`
}
var Config = &IniConfig{}
func InitFromFile(path string) error {
cfg, err := ini.Load(path)
if err != nil {
return err
}
return cfg.MapTo(Config)
}
```


这是一种典型的Go通过struct field tag与ini配置文件中section和key绑定读取的示例，我们在main包中调用InitFromFile读取ini配置文件：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo1/main.go
package main
import (
"github.com/bigwhite/readini/pkg/config"
"github.com/bigwhite/readini/pkg/pkg1"
)
func main() {
err := config.InitFromFile("conf/demo.ini")
if err != nil {
panic(err)
}
pkg1.Foo()
}
```


读取后的配置项信息存储在config.Config这个全局变量中。在其他包中（比如pkg/pkg1/pkg1.go），我们可直接访问该全局变量获取配置项信息：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo1/pkg/pkg1/pkg1.go
package pkg1
import (
"fmt"
"github.com/bigwhite/readini/pkg/config"
)
func Foo() {
fmt.Printf("%#v\n", config.Config)
}
```


这种方式很简单、直观也易于理解，但以全局变量形式将配置项信息暴露给其他包，从代码设计层面，这总是会予人口实的。那么我们是否可以只暴露包函数，而不暴露具体实现呢？

### 2. 通过section.key形式读取配置项

由于是采用的tag与结构体字段的绑定方法，实际配置项名字与绑定的字段名字可能是不一致的，比如下面代码段中的结构体字段TlsPort与其tag tls_port：

```
type Server struct {
Id string `ini:"id"`
Port int `ini:"port"`
TlsPort int `ini:"tls_port"`
}
```


这样使用config包的用户在要获取配置项值时就必须了解绑定的结构体字段的名字。如果我们不暴露这些绑定结构体的实现细节的话，config包的用户所掌握的信息仅仅就是配置文件(比如：demo.ini)本身了。

于是一个很自然的想法就会萌发出来！我们是否可以通过section.key的形式得到对应配置项的值，比如以下面配置项为例：

```
[server]
id = 100001
port = 23333
tls_port = 83333
```


我们需要通过server.id来获得id这个配置项的值，类似的其他配置项的获取方式是传入server.port、server.tls_port等。这样我们的config包仅需保留类似一个接收xx.yy.zz为参数的GetSectionKey函数即可，就像下面这样：

```
id, ok := config.GetSectionKey("server.id")
```


接下来，我们就沿着这个思路在demo1的基础上重构为新方案demo2。下面是修改后的demo2的config包代码：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo2/pkg/config/config.go
package config
import (
"reflect"
"strings"
ini "github.com/go-ini/ini"
)
type server struct {
Id string `ini:"id"`
Port int `ini:"port"`
TlsPort int `ini:"tls_port"`
}
type log struct {
Compress bool `ini:"compress"`
LogPath string `ini:"path"`
MaxAge int `ini:"max_age"`
MaxBackups int `ini:"maxbackups"`
MaxSize int `ini:"maxsize"`
}
type debug struct {
ProfileOn bool `ini:"profile_on"`
ProfilePort string `ini:"profile_port"`
}
type iniConfig struct {
Server server `ini:"server"`
Log log `ini:"log"`
Dbg debug `ini:"debug"`
}
var thisConfig = iniConfig{}
func InitFromFile(path string) error {
cfg, err := ini.Load(path)
if err != nil {
return err
}
return cfg.MapTo(&thisConfig)
}
func GetSectionKey(name string) (interface{}, bool) {
keys := strings.Split(name, ".")
lastKey := keys[len(keys)-1]
v := reflect.ValueOf(thisConfig)
t := reflect.TypeOf(thisConfig)
found := false
for _, key := range keys {
cnt := v.NumField()
for i := 0; i < cnt; i++ {
field := t.Field(i)
if field.Tag.Get("ini") == key {
t = field.Type
v = v.Field(i)
if key == lastKey {
found = true
}
break
}
}
}
if found {
return v.Interface(), true
}
return nil, false
}
```


我们将原先暴露出去的全局变量改为了包内变量(thisConfig)，几个绑定的结构体类型也都改为非导出的了。我们提供了一个对外的函数：GetSectionKey，这样通过该函数，我们就可以使用section.key的形式获取到对应配置项的值了。在GetSectionKey函数的实现中，我们使用了反射来获取结构体定义中各个字段的tag来和传入的section.key的各个部分做比对，一旦匹配，便将对应的值传出来。如果没有匹配到，则返回false，这里GetSectionKey的返回值列表设计也使用了经典的“comma, ok”模式。

这样，我们在pkg1包中便可以这样来获取对应的配置项的值了：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo2/pkg/pkg1/pkg1.go
package pkg1
import (
"fmt"
"github.com/bigwhite/readini/pkg/config"
)
func Foo() {
id, ok := config.GetSectionKey("server.id")
fmt.Printf("id = [%v], ok = [%t]\n", id, ok)
tlsPort, ok := config.GetSectionKey("server.tls_port")
fmt.Printf("tls_port = [%v], ok = [%t]\n", tlsPort, ok)
logPath, ok := config.GetSectionKey("log.path")
fmt.Printf("path = [%v], ok = [%t]\n", logPath, ok)
logPath1, ok := config.GetSectionKey("log.path1")
fmt.Printf("path1 = [%v], ok = [%t]\n", logPath1, ok)
}
```


运行demo2，我们将看到如下结果：

```
$go run main.go
id = [100001], ok = [true]
tls_port = [83333], ok = [true]
path = [./log/demo.log], ok = [true]
path1 = [<nil>], ok = [false]
```


现在还有一个问题，那就是config包暴露的函数GetSectionKey的第一个返回值类型为interface{}，这样我们得到配置项的值后还得根据其类型通过类型断言方式进行转型，体验略差，我们可以在config包中提供常见类型的“语法糖”函数，比如下面这些：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo2/pkg/config/config.go
func GetInt(name string) (int, bool) {
i, ok := GetSectionKey(name)
if !ok {
return 0, false
}
if v, ok := i.(int); ok {
return v, true
}
// maybe it is a digital string
s, ok := i.(string)
if !ok {
return 0, false
}
n, err := strconv.Atoi(s)
if err != nil {
return 0, false
}
return n, true
}
func GetString(name string) (string, bool) {
i, ok := GetSectionKey(name)
if !ok {
return "", false
}
s, ok := i.(string)
if !ok {
return "", false
}
return s, true
}
func GetBool(name string) (bool, bool) {
i, ok := GetSectionKey(name)
if !ok {
return false, false
}
b, ok := i.(bool)
if !ok {
return false, false
}
return b, true
}
```


这样我们在pkg1包中就可以直接使用这些语法糖函数获取对应类型的配置项值了：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo2/pkg/pkg1/pkg1.go
b, ok := config.GetBool("debug.profile_on")
fmt.Printf("profile_on = [%t], ok = [%t]\n", b, ok)
```


### 3. 优化

配置读取一般都是在系统初始化阶段，对其性能要求不高。后续系统运行过程中，也会偶有获取配置项的业务逻辑。一旦在关键路径上有获取配置项值的逻辑，上面的方案便值得商榷，因为每次通过GetSectionKey获取一个配置项的值都要通过[反射](https://mp.weixin.qq.com/s/KgUZGVF08yEO2oARryOLcg)进行一番操作，性能肯定不佳。

那么如何优化呢？我们可以通过为每个key建立索引来进行。我们在config包中创建一个除初始化时只读的map变量：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo3/pkg/config/config.go
var index = make(map[string]interface{}, 100)
```


在config包的InitFromFile中我们将配置项以section.key为key的形式索引到该index变量中：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo3/pkg/config/config.go
func InitFromFile(path string) error {
cfg, err := ini.Load(path)
if err != nil {
return err
}
err = cfg.MapTo(&thisConfig)
if err != nil {
return err
}
createIndex()
return nil
}
```


createIndex的实现如下：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo3/pkg/config/config.go
func createIndex() {
v := reflect.ValueOf(thisConfig)
t := reflect.TypeOf(thisConfig)
cnt := v.NumField()
for i := 0; i < cnt; i++ {
fieldVal := v.Field(i)
if fieldVal.Kind() != reflect.Struct {
continue
}
// it is a struct kind field, go on to get tag
fieldStructTyp := t.Field(i)
tag := fieldStructTyp.Tag.Get("ini")
if tag == "" {
continue // no ini tag, ignore it
}
// append Field Recursively
appendField(tag, fieldVal)
}
}
func appendField(parentTag string, v reflect.Value) {
cnt := v.NumField()
for i := 0; i < cnt; i++ {
fieldVal := v.Field(i)
fieldTyp := v.Type()
fieldStructTyp := fieldTyp.Field(i)
tag := fieldStructTyp.Tag.Get("ini")
if tag == "" {
continue
}
if fieldVal.Kind() != reflect.Struct {
// leaf field, add to map
index[parentTag+"."+tag] = fieldVal.Interface()
} else {
// recursive call appendField
appendField(parentTag+"."+tag, fieldVal)
}
}
}
```


这样我们的GetSectionKey就会变得异常简单：

```
func GetSectionKey(name string) (interface{}, bool) {
v, ok := index[name]
return v, ok
}
```


我们看到：每次调用config.GetSectionKey将变成一次map的查询操作，这性能那是相当的高:)。

### 4. 第三方方案

其实前面那些仅仅是一个配置项读取思路的演进过程，你完全无需自行实现，因为我们有实现的更好的第三方包可以直接使用，比如[viper](https://github.com/spf13/viper)。我们用viper来替换demo3中的config包，代码见demo4：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo4/main.go
package main
import (
"github.com/bigwhite/readini/pkg/pkg1"
"github.com/spf13/viper"
)
func main() {
viper.SetConfigName("demo")
viper.SetConfigType("ini")
viper.AddConfigPath("./conf")
err := viper.ReadInConfig()
if err != nil {
panic(err)
}
pkg1.Foo()
}
```


我们在main函数中利用viper的API读取demo.ini中的配置。然后在pkg1.Foo函数中向下面这样获取配置项的值即可：

```
// github.com/bigwhite/experiments/tree/master/read-ini/demo4/pkg/pkg1/pkg1.go
package pkg1
import (
"fmt"
"github.com/spf13/viper"
)
func Foo() {
id := viper.GetString("server.id")
fmt.Printf("id = [%s]\n", id)
tlsPort := viper.GetInt("server.tls_port")
fmt.Printf("tls_port = [%d]\n", tlsPort)
logPath := viper.GetString("log.path")
fmt.Printf("path = [%s]\n", logPath)
if viper.IsSet("log.path1") {
logPath1 := viper.GetString("log.path1")
fmt.Printf("path1 = [%s]\n", logPath1)
} else {
fmt.Printf("log.path1 is not found\n")
}
}
```


上面的实现基本等价于我们在demo3中所作的一切，viper没有使用“comma, ok”模式，我们需要自己调用viper.IsSet来判断是否有某个配置项，而不是通过像GetString这样的函数返回的空字符串来判断。

使用viper后，我们甚至无需创建与配置文件中配置项对应的结构体类型了。viper是一个强大的Go配置操作框架，它能实现的不仅限于上面这些，它还支持写配置文件、监视配置文件变化并热加载、支持多种配置文件类型(JSON, TOML, YAML, HCL, ini等)、支持从环境变量和命令行参数读取配置，并且命令行参数、环境变量、配置文件等究竟以哪个配置为准，viper是按一定优先级次序的，从高到低分别为：

- 明确调用Set
- flag
- env
- config
- key/value store
- default

有如此完善的配置操作第三方库，我们完全无需手动撸自己的实现了。

### 5. 小结

除了在本文中提供的使用包级API获取配置项值的方法外，我们还可以将读取出的配置项集合放入应用上下文，以参数的形式“传递”到应用的各个角落，但笔者更喜欢向viper这种通过公共函数获取配置项的方法。本文阐述的就是这种思路的演化过程，并给出一个“玩票”的实现（未经系统测试），以帮助大家了解其中原理，但不要将其用到你的项目中哦。

本文涉及的源码请到[这里下载](https://github.com/bigwhite/experiments/tree/master/read-ini)：https://github.com/bigwhite/experiments/tree/master/read-ini。

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