---
title: Go 1.16新功能特性不完全前瞻
url: https://tonybai.com/2020/12/12/a-forward-look-to-new-feature-of-go-1-16/
published: '2020-12-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.16新功能特性不完全前瞻

2020年最后一个购物狂欢，[双十二购物节“Gopher部落”知识星球推出双十二优惠！](http://image.tonybai.com/img/202011/gopher-tribe-2020-12-12.png)本年度最低折扣仅限今天一天。笔者建立“Gopher部落”旨在建立一个高质量的Go语言技术精品社区，持续不断的高质量技术资料分享，让加入的星友每天都有新收获！欢迎大家加入！

![](../../assets/0d50872309039abd.png)


Go 1.16将于2021年2月发布。目前已经进入freeze状态，即不再接受新feature，仅fix bug、编写文档和接受安全更新等。

![img{512x368}](../../assets/8870b3ced9193626.png)


目前Go 1.16的[发布说明](https://tip.golang.org/doc/go1.16)尚处于早期草稿阶段，但Go团队成员正在致力于编写发布说明。Go 1.16的完全特性列表说明还得等真正发布前才能得到。如今要了解Go 1.16功能特性都有哪些变化，只能结合现有的release note以及从[Go 1.16里程碑](https://github.com/golang/go/issues?q=is%3Aissue+milestone%3AGo1.16+is%3Aclosed)中的issue列表中挖掘。

下面就“挖掘”到的Go 1.16重要功能特性变化做简要的且不完全的前瞻。

### 1. 支持Apple Silicon M1芯片

Apple Silicon M1芯片Macbook的发布让Go团队紧急为Go 1.16增加对M1的支持。如果要跨平台编译，只需设定GOOS=darwin, GOARCH=arm64即可构建出可以在搭载M1芯片的Macbook上运行的Go应用。

同时Go 1.16还增加了对ios/amd64的支持，主要是为了支持在amd64架构上的MacOS上运行ios模拟器。

### 2. RISC-V架构支持cgo和-buildmode=pie

RISC-V架构很可能是未来5-10年挑战ARM的最主要架构，Go语言持续加大对RISC-V架构的支持，在Go 1.16中对linux/riscv64又增加了cgo支持以及-buildmode=pie。不过目前对risc-v仍仅限于linux os。

### 3. 有关go module的变化

- module-aware模式成为默认状态。如要回到gopath mode，将GO111MODULE设置为auto；
- go build和go test不会修改go.mod和go.sum文件。能修改这两个文件的命令只有go get和go mod tidy；
- go get之前的构建和安装go包的行为模式将被废弃。go get将专注于分析依赖，并获取go包/module，更新go.mod/go.sum；
- go install将恢复自己构建和安装包的“角色”（在go module加入后，go install日益受到冷落，这次翻身了)；
[go.mod将支持retract指示符](https://github.com/golang/go/issues/24031)，包或module作者可以利用该指示符在自己module的go.mod中标记某些版本撤回(因不安全、不兼容或损坏等原因)，不建议使用。- go.mod中的exclude指示符语义变更：Go 1.16中将忽略exclude指示的module/包依赖；而之前的版本go工具链仅仅是跳过exclude指示的版本，而使用该依赖包/module的下一个版本。
- -i build flag废弃；
- go get的-insecure命令行标志选项作废，可以用GOINSECURE环境变量指示go get是否通过不安全的http去获取包；

### 4. 支持在Go二进制文件中嵌入静态文件(文本、图片等)

Go 1.16新增**go:embed**指示符和embed标准库包，二者一起用于支持在在Go二进制文件中嵌入静态文件。下面是一个在Go应用中嵌入文本文件用于http应答内容的小例子：

```
// hello.txt
hello, go 1.16
// main.go
package main
import (
_ "embed"
"net/http"
)
//go:embed hello.txt
var s string
func main() {
http.Handle("/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
w.Write([]byte(s))
}))
http.ListenAndServe(":8080", nil)
}
```


上述源码中的**go:embed**指示符的含义是：将hello.txt内容存储在字符串变量s中。我们构建该源码，并验证一下s中存储的是否是hello.txt中的数据：

```
$ go build -o demo main.go
$ mv hello.txt hello.txt.bak // 将hello.txt改名，我们看看数据是否真的已经嵌入到二进制文件demo中了
$ ./demo
$curl localhost:8080
hello, go 1.16
```


### 5.GODEBUG环境变量支持跟踪

当GODEBUG环境变量包含inittrace=1时，Go运行时将会报告各个源代码文件中的init函数的执行时间和内存开辟消耗情况。比如对于上面的程序demo，我们按如下命令执行：

```
# GODEBUG=inittrace=1 ./demo
init internal/bytealg @0.014 ms, 0 ms clock, 0 bytes, 0 allocs
init runtime @0.033 ms, 0.015 ms clock, 0 bytes, 0 allocs
init errors @0.24 ms, 0.003 ms clock, 0 bytes, 0 allocs
init sync @0.47 ms, 0.001 ms clock, 16 bytes, 1 allocs
init io @0.66 ms, 0 ms clock, 144 bytes, 9 allocs
init internal/oserror @0.85 ms, 0 ms clock, 80 bytes, 5 allocs
init syscall @1.0 ms, 0.006 ms clock, 624 bytes, 2 allocs
init time @1.2 ms, 0.013 ms clock, 384 bytes, 8 allocs
init path @1.4 ms, 0.003 ms clock, 16 bytes, 1 allocs
init io/fs @1.6 ms, 0 ms clock, 16 bytes, 1 allocs
init context @2.3 ms, 0.002 ms clock, 128 bytes, 4 allocs
init math @2.5 ms, 0 ms clock, 0 bytes, 0 allocs
init strconv @2.7 ms, 0 ms clock, 32 bytes, 2 allocs
init unicode @2.9 ms, 0.065 ms clock, 23736 bytes, 26 allocs
init bytes @3.2 ms, 0 ms clock, 48 bytes, 3 allocs
init crypto @3.3 ms, 0.001 ms clock, 160 bytes, 1 allocs
init reflect @3.5 ms, 0.002 ms clock, 0 bytes, 0 allocs
init encoding/binary @3.7 ms, 0 ms clock, 16 bytes, 1 allocs
init crypto/cipher @3.8 ms, 0 ms clock, 16 bytes, 1 allocs
init crypto/aes @4.0 ms, 0.003 ms clock, 16 bytes, 1 allocs
init internal/poll @4.1 ms, 0 ms clock, 64 bytes, 4 allocs
init os @4.2 ms, 0.029 ms clock, 544 bytes, 13 allocs
init fmt @4.4 ms, 0.003 ms clock, 32 bytes, 2 allocs
init math/rand @4.5 ms, 0.023 ms clock, 5440 bytes, 3 allocs
init math/big @4.7 ms, 0.002 ms clock, 32 bytes, 2 allocs
init crypto/sha512 @4.8 ms, 0.004 ms clock, 0 bytes, 0 allocs
init encoding/asn1 @5.0 ms, 0.004 ms clock, 224 bytes, 7 allocs
init vendor/golang.org/x/crypto/cryptobyte @5.1 ms, 0 ms clock, 48 bytes, 2 allocs
init crypto/ecdsa @5.3 ms, 0 ms clock, 48 bytes, 3 allocs
init bufio @5.4 ms, 0.003 ms clock, 176 bytes, 11 allocs
init crypto/rand @5.6 ms, 0.001 ms clock, 120 bytes, 4 allocs
init crypto/rsa @5.7 ms, 0.007 ms clock, 648 bytes, 18 allocs
init crypto/sha1 @5.8 ms, 0 ms clock, 0 bytes, 0 allocs
init crypto/sha256 @5.9 ms, 0 ms clock, 0 bytes, 0 allocs
init encoding/base64 @5.9 ms, 0.006 ms clock, 1408 bytes, 4 allocs
init crypto/md5 @6.0 ms, 0 ms clock, 0 bytes, 0 allocs
init encoding/hex @6.1 ms, 0 ms clock, 16 bytes, 1 allocs
init crypto/x509/pkix @6.1 ms, 0.001 ms clock, 624 bytes, 2 allocs
init path/filepath @6.2 ms, 0 ms clock, 16 bytes, 1 allocs
init vendor/golang.org/x/net/dns/dnsmessage @6.3 ms, 0.009 ms clock, 1616 bytes, 27 allocs
init net @6.3 ms, 0.029 ms clock, 2840 bytes, 74 allocs
init crypto/dsa @6.5 ms, 0 ms clock, 16 bytes, 1 allocs
init crypto/x509 @6.5 ms, 0.016 ms clock, 4768 bytes, 15 allocs
init io/ioutil @6.7 ms, 0.002 ms clock, 16 bytes, 1 allocs
init vendor/golang.org/x/sys/cpu @6.7 ms, 0.009 ms clock, 1280 bytes, 1 allocs
init vendor/golang.org/x/crypto/chacha20poly1305 @6.8 ms, 0 ms clock, 16 bytes, 1 allocs
init vendor/golang.org/x/crypto/curve25519 @6.9 ms, 0 ms clock, 0 bytes, 0 allocs
init crypto/tls @7.0 ms, 0.007 ms clock, 1600 bytes, 11 allocs
init log @7.0 ms, 0 ms clock, 80 bytes, 1 allocs
init mime @7.1 ms, 0.008 ms clock, 1232 bytes, 4 allocs
init mime/multipart @7.2 ms, 0.001 ms clock, 192 bytes, 4 allocs
init compress/flate @7.3 ms, 0.012 ms clock, 4240 bytes, 7 allocs
init hash/crc32 @7.4 ms, 0.014 ms clock, 1024 bytes, 1 allocs
init compress/gzip @7.5 ms, 0 ms clock, 32 bytes, 2 allocs
init vendor/golang.org/x/text/transform @7.5 ms, 0 ms clock, 80 bytes, 5 allocs
init vendor/golang.org/x/text/unicode/bidi @7.6 ms, 0.005 ms clock, 272 bytes, 2 allocs
init vendor/golang.org/x/text/secure/bidirule @7.7 ms, 0.008 ms clock, 16 bytes, 1 allocs
init vendor/golang.org/x/text/unicode/norm @7.8 ms, 0.002 ms clock, 0 bytes, 0 allocs
init vendor/golang.org/x/net/idna @7.8 ms, 0 ms clock, 0 bytes, 0 allocs
init vendor/golang.org/x/net/http/httpguts @7.9 ms, 0.002 ms clock, 848 bytes, 3 allocs
init vendor/golang.org/x/net/http2/hpack @7.9 ms, 0.063 ms clock, 22440 bytes, 32 allocs
init net/http/internal @8.1 ms, 0.005 ms clock, 1808 bytes, 3 allocs
init vendor/golang.org/x/net/http/httpproxy @8.2 ms, 0 ms clock, 336 bytes, 2 allocs
init net/http @8.3 ms, 0.026 ms clock, 10280 bytes, 113 allocs
```


我们看到各个依赖包中的init函数执行的消耗情况都被输出了出来，根据这些信息，我们可以很容易判断出init函数中可能存在的性能问题或瓶颈。

### 6. 链接器进一步优化

既[Go 1.15](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)实现了go linker的第一阶段优化后，Go 1.16中继续实施了对linker的第二阶段优化。优化后的链接器要平均比Go 1.15的快20%-25%，消耗的内存却减少5%-15%。

### 7. struct field的tag中的多个key可以合并写

如果某个结构体支持多种编码格式的序列化和反序列化，比如：json、bson、xml，那么之前版本需要按如下书写该结构体的字段tag，冗长且重复：

```
type MyStruct struct {
Field1 string `json:"field_1,omitempty" bson:"field_1,omitempty" xml:"field_1,omitempty" form:"field_1,omitempty" other:"value"`
}
```


[Go 1.16支持将多个key进行合并](https://github.com/golang/go/issues/40281)，上面的tag可以写成如下形式：

```
type MyStruct struct {
Field1 string `json bson xml form:"field_1,omitempty" other:"value"`
}
```


### 8. 其他改变

- 新增runtime/metrics包，以替代runtime.ReadMemStats和debug.ReadGCStats输出runtime的各种度量数据，这个包更通用稳定，性能也更好；
- 新增io/fs包，用于提供只读的操作os的文件树的高级接口；
- 对Unicode标准的支持从12.0.0升级为13.0.0。

### 附录：安装go tip版本的两种方式

#### 1) 从源码安装

```
$git clone https//github.com/golang/go.git
$cd go/src
$./all.bash
```


#### 2) 使用gotip工具安装

```
$go get golang.org/dl/gotip
$gotip download
```


我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

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

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论