---
title: go protobuf v1败给了gogo protobuf，那v2呢？
url: https://tonybai.com/2020/04/24/gogoprotobuf-vs-goprotobuf-v1-and-v2/
published: '2020-04-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# go protobuf v1败给了gogo protobuf，那v2呢？

近期的一个项目有对结构化数据进行序列化和反序列化的需求，该项目具有**performance critical**属性，因此我们在选择序列化库包时是要考虑包的性能的。

[github](https://tonybai.com/2020/04/07/illustrated-tale-of-git-internal-key-concepts/)上有一个有关Go序列化方法性能比较的repo：[go_serialization_benchmarks](https://github.com/alecthomas/go_serialization_benchmarks)，这个repo横向比较了数十种数据序列化方法的正确性、性能、内存分配等，并给出了一个结论：推荐** gogo protobuf**。对于这样一个粗选的结果，我们是直接笑纳的^_^。接下来就是进一步对gogo protobuf做进一步探究。

![img{512x368}](../../assets/983ba7640f108a35.png)


## 一. go protobuf v1 vs. gogo protobuf

[gogo protobuf](https://github.com/gogo/protobuf)是既[go protobuf官方api](https://github.com/golang/protobuf)之外的另一个go protobuf的api实现，它兼容[go官方protobuf api](https://github.com/golang/protobuf)(更准确的说是[v1版本](https://github.com/golang/protobuf))。gogo protobuf提供了三种代码生成方式：protoc-gen-gogofast、protoc-gen-gogofaster和protoc-gen-gogoslick。究竟选择哪一个呢？这里我也写了一些benchmark来比较，并顺便将官方go protobuf api也一并加入比较了。

我们首先安装一下gogo protobuf实现的protoc的三个插件，用于生成proto文件对应的Go包源码文件：

```
go get github.com/gogo/protobuf/protoc-gen-gofast
go get github.com/gogo/protobuf/protoc-gen-gogofaster
go get github.com/gogo/protobuf/protoc-gen-gogoslick
```


安装后，我们在**$GOPATH/bin**下将看到这三个文件(protoc-gen-go是go protobuf官方实现的代码生成插件)：

```
$ls -l $GOPATH/bin|grep proto
-rwxr-xr-x 1 tonybai staff 6252344 4 24 14:43 protoc-gen-go*
-rwxr-xr-x 1 tonybai staff 9371384 2 28 09:35 protoc-gen-gofast*
-rwxr-xr-x 1 tonybai staff 9376152 2 28 09:40 protoc-gen-gogofaster*
-rwxr-xr-x 1 tonybai staff 9380728 2 28 09:40 protoc-gen-gogoslick*
```


为了对采用不同插件生成的数据序列化和反序列化方法进行性能基准测试，我们建立了下面repo。在repo中，每一种方法生成的代码放入独立的[module](https://tonybai.com/2019/12/21/go-modules-minimal-version-selection/)中：

```
$tree -L 2 -F
.
├── IDL/
│ └── submit.proto
├── Makefile
├── gogoprotobuf-fast/
│ ├── go.mod
│ ├── go.sum
│ ├── submit/
│ └── submit_test.go
├── gogoprotobuf-faster/
│ ├── go.mod
│ ├── go.sum
│ ├── submit/
│ └── submit_test.go
├── gogoprotobuf-slick/
│ ├── go.mod
│ ├── go.sum
│ ├── submit/
│ └── submit_test.go
└── goprotobuf/
├── go.mod
├── go.sum
├── submit/
└── submit_test.go
```


我们的proto文件如下:

```
$cat IDL/submit.proto
syntax = "proto3";
option go_package = ".;submit";
package submit;
message request {
int64 recvtime = 1;
string uniqueid = 2;
string token = 3;
string phone = 4;
string content = 5;
string sign = 6;
string type = 7;
string extend = 8;
string version = 9;
}
```


我们还建立了Makefile，用于简化操作：

```
$cat Makefile
gen-protobuf: gen-goprotobuf gen-gogoprotobuf-fast gen-gogoprotobuf-faster gen-gogoprotobuf-slick
gen-goprotobuf:
protoc -I ./IDL submit.proto --go_out=./goprotobuf/submit
gen-gogoprotobuf-fast:
protoc -I ./IDL submit.proto --gofast_out=./gogoprotobuf-fast/submit
gen-gogoprotobuf-faster:
protoc -I ./IDL submit.proto --gogofaster_out=./gogoprotobuf-faster/submit
gen-gogoprotobuf-slick:
protoc -I ./IDL submit.proto --gogoslick_out=./gogoprotobuf-slick/submit
benchmark: goprotobuf-bench gogoprotobuf-fast-bench gogoprotobuf-faster-bench gogoprotobuf-slick-bench
goprotobuf-bench:
cd goprotobuf && go test -bench .
gogoprotobuf-fast-bench:
cd gogoprotobuf-fast && go test -bench .
gogoprotobuf-faster-bench:
cd gogoprotobuf-faster && go test -bench .
gogoprotobuf-slick-bench:
cd gogoprotobuf-slick && go test -bench .
```


针对每一种方法，我们建立一个benchmark test。benchmark test代码都是一样的，我们以**gogoprotobuf-fast**为例：

```
// submit_test.go
package protobufbench
import (
"fmt"
"os"
"testing"
"github.com/bigwhite/protobufbench_gogoprotofast/submit"
"github.com/gogo/protobuf/proto"
)
var request = submit.Request{
Recvtime: 170123456,
Uniqueid: "a1b2c3d4e5f6g7h8i9",
Token: "xxxx-1111-yyyy-2222-zzzz-3333",
Phone: "13900010002",
Content: "Customizing the fields of the messages to be the fields that you actually want to use removes the need to copy between the structs you use and structs you use to serialize. gogoprotobuf also offers more serialization formats and generation of tests and even more methods.",
Sign: "tonybaiXZYDFDS",
Type: "submit",
Extend: "",
Version: "v1.0.0",
}
var requestToUnMarshal []byte
func init() {
var err error
requestToUnMarshal, err = proto.Marshal(&request)
if err != nil {
fmt.Printf("marshal err:%s\n", err)
os.Exit(1)
}
}
func BenchmarkMarshal(b *testing.B) {
b.ReportAllocs()
for i := 0; i < b.N; i++ {
_, _ = proto.Marshal(&request)
}
}
func BenchmarkUnmarshal(b *testing.B) {
b.ReportAllocs()
var request submit.Request
for i := 0; i < b.N; i++ {
_ = proto.Unmarshal(requestToUnMarshal, &request)
}
}
func BenchmarkMarshalInParalell(b *testing.B) {
b.ReportAllocs()
b.RunParallel(func(pb *testing.PB) {
for pb.Next() {
_, _ = proto.Marshal(&request)
}
})
}
func BenchmarkUnmarshalParalell(b *testing.B) {
b.ReportAllocs()
var request submit.Request
b.RunParallel(func(pb *testing.PB) {
for pb.Next() {
_ = proto.Unmarshal(requestToUnMarshal, &request)
}
})
}
```


我们看到，对每种方法生成的代码，我们都会进行顺序和并行的marshal和unmarshal基准测试。

我们首先分别使用不同方式生成对应的go代码：

```
$make gen-protobuf
protoc -I ./IDL submit.proto --go_out=./goprotobuf/submit
protoc -I ./IDL submit.proto --gofast_out=./gogoprotobuf-fast/submit
protoc -I ./IDL submit.proto --gogofaster_out=./gogoprotobuf-faster/submit
protoc -I ./IDL submit.proto --gogoslick_out=./gogoprotobuf-slick/submit
```


然后运行基准测试(使用macos上的[go 1.14](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/))：

```
$make benchmark
cd goprotobuf && go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/protobufbench_goproto
BenchmarkMarshal-8 2437068 483 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshal-8 2262229 529 ns/op 400 B/op 7 allocs/op
BenchmarkMarshalInParalell-8 7592120 162 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshalParalell-8 5306744 225 ns/op 400 B/op 7 allocs/op
PASS
ok github.com/bigwhite/protobufbench_goproto 6.239s
cd gogoprotobuf-fast && go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/protobufbench_gogoprotofast
BenchmarkMarshal-8 7186828 164 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshal-8 4706794 251 ns/op 400 B/op 7 allocs/op
BenchmarkMarshalInParalell-8 15107896 83.0 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshalParalell-8 6258507 179 ns/op 400 B/op 7 allocs/op
PASS
ok github.com/bigwhite/protobufbench_gogoprotofast 5.449s
cd gogoprotobuf-faster && go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/protobufbench_gogoprotofaster
BenchmarkMarshal-8 7036842 166 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshal-8 4666698 256 ns/op 400 B/op 7 allocs/op
BenchmarkMarshalInParalell-8 15444961 83.2 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshalParalell-8 6936337 202 ns/op 400 B/op 7 allocs/op
PASS
ok github.com/bigwhite/protobufbench_gogoprotofaster 5.750s
cd gogoprotobuf-slick && go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/protobufbench_gogoprotoslick
BenchmarkMarshal-8 6529311 176 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshal-8 4737463 252 ns/op 400 B/op 7 allocs/op
BenchmarkMarshalInParalell-8 15700746 81.8 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshalParalell-8 6528390 202 ns/op 400 B/op 7 allocs/op
PASS
ok github.com/bigwhite/protobufbench_gogoprotoslick 5.668s
```


在我的macpro(4核8线程)上，我们看到两点结论：

-
官方go protobuf实现生成的代码性能的确弱于gogo protobuf生成的代码，在顺序测试中，差距还较大；

-
针对我预置的proto文件中数据格式，gogo protobuf的三种生成方法产生的代码的性能差异并不大，选择protoc-gen-gofast生成的代码在性能上即可满足。


## 二. go protobuf v2

今年三月份初，[Go官方发布了protobuf的新API版本](https://blog.golang.org/protobuf-apiv2)，这个版本与[原go protobuf](https://github.com/golang/protobuf)并不兼容。新版API旨在使protobuf的类型系统与go类型系统充分融合，提供反射功能和自定义消息实现。那么该版本生成的序列/反序列化代码在性能上有提升吗？我们将其加入我们的benchmark。

我们先下载go protobuf v2的代码生成插件(注意：由于go protobuf v1和go protobuf v2的插件名称相同，需要先备份好原先已经安装的**protoc-gen-go**)：

```
$ go get google.golang.org/protobuf/cmd/protoc-gen-go
go: found google.golang.org/protobuf/cmd/protoc-gen-go in google.golang.org/protobuf v1.21.0
```


然后将新安装的插件名称改为**protoc-gen-gov2**，这样**$GOPATH/bin**下的插件文件列表如下：

```
$ls -l $GOPATH/bin/|grep proto
-rwxr-xr-x 1 tonybai staff 6252344 4 24 14:43 protoc-gen-go*
-rwxr-xr-x 1 tonybai staff 9371384 2 28 09:35 protoc-gen-gofast*
-rwxr-xr-x 1 tonybai staff 9376152 2 28 09:40 protoc-gen-gogofaster*
-rwxr-xr-x 1 tonybai staff 9380728 2 28 09:40 protoc-gen-gogoslick*
-rwxr-xr-x 1 tonybai staff 8716064 4 24 14:56 protoc-gen-gov2*
```


在Makefile中增加针对go protobuf v2的代码生成和Benchmark target：

```
gen-goprotobufv2:
protoc -I ./IDL submit.proto --gov2_out=./goprotobufv2/submit
goprotobufv2-bench:
cd goprotobufv2 && go test -bench .
```


由于go protobuf v2与v1版本不兼容，因此也无法与gogo protobuf兼容，我们需要修改一下go protobuf v2对应的submit_test.go，将导入的**“github.com/gogo/protobuf/proto”**包换为**“google.golang.org/protobuf/proto”**。

重新生成代码：

```
$make gen-protobuf
protoc -I ./IDL submit.proto --go_out=./goprotobuf/submit
protoc -I ./IDL submit.proto --gov2_out=./goprotobufv2/submit
protoc -I ./IDL submit.proto --gofast_out=./gogoprotobuf-fast/submit
protoc -I ./IDL submit.proto --gogofaster_out=./gogoprotobuf-faster/submit
protoc -I ./IDL submit.proto --gogoslick_out=./gogoprotobuf-slick/submit
```


运行benchmark:

```
$make benchmark
cd goprotobuf && go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/protobufbench_goproto
BenchmarkMarshal-8 2420620 485 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshal-8 2186240 538 ns/op 400 B/op 7 allocs/op
BenchmarkMarshalInParalell-8 7334412 162 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshalParalell-8 4537429 222 ns/op 400 B/op 7 allocs/op
PASS
ok github.com/bigwhite/protobufbench_goproto 6.052s
cd goprotobufv2 && go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/protobufbench_goprotov2
BenchmarkMarshal-8 2404473 506 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshal-8 1901947 626 ns/op 400 B/op 7 allocs/op
BenchmarkMarshalInParalell-8 6629139 171 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshalParalell-8 panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x11d4956]
goroutine 196 [running]:
google.golang.org/protobuf/internal/impl.(*messageState).protoUnwrap(0xc00007e210, 0xc000010360, 0xc00008ce01)
/Users/tonybai/Go/pkg/mod/google.golang.org/protobuf@v1.21.0/internal/impl/message_reflect_gen.go:27 +0x26
google.golang.org/protobuf/internal/impl.(*messageState).Interface(0xc00007e210, 0xc00007e210, 0xc00012c000)
/Users/tonybai/Go/pkg/mod/google.golang.org/protobuf@v1.21.0/internal/impl/message_reflect_gen.go:24 +0x2b
google.golang.org/protobuf/proto.UnmarshalOptions.unmarshal(0x0, 0x12acc00, 0xc000010360, 0xc00012c000, 0x177, 0x177, 0x12b23e0, 0xc00007e210, 0xc000200001, 0x0, ...)
/Users/tonybai/Go/pkg/mod/google.golang.org/protobuf@v1.21.0/proto/decode.go:71 +0x2c5
google.golang.org/protobuf/proto.Unmarshal(0xc00012c000, 0x177, 0x177, 0x12ac180, 0xc00007e210, 0x0, 0x0)
/Users/tonybai/Go/pkg/mod/google.golang.org/protobuf@v1.21.0/proto/decode.go:48 +0x89
github.com/bigwhite/protobufbench_goprotov2.BenchmarkUnmarshalParalell.func1(0xc0004a8000)
/Users/tonybai/test/go/protobuf/goprotobufv2/submit_test.go:65 +0x6a
testing.(*B).RunParallel.func1(0xc0000161b0, 0xc0000161a8, 0xc0000161a0, 0xc00010c700, 0xc00004a000)
/Users/tonybai/.bin/go1.14/src/testing/benchmark.go:763 +0x99
created by testing.(*B).RunParallel
/Users/tonybai/.bin/go1.14/src/testing/benchmark.go:756 +0x192
exit status 2
FAIL github.com/bigwhite/protobufbench_goprotov2 4.878s
make: *** [goprotobufv2-bench] Error 1
```


我们看到go protobuf v2并未完成所有benchmark test，在运行并行unmarshal测试中panic了。目前[go protobuf v2官方并未在github开通issue](https://github.com/protocolbuffers/protobuf-go)，因此尚不知道哪里去提issue。于是回到test代码，再仔细看一下submit_test.go中 BenchmarkUnmarshalParalell的代码：

```
func BenchmarkUnmarshalParalell(b *testing.B) {
b.ReportAllocs()
var request submit.Request
b.RunParallel(func(pb *testing.PB) {
for pb.Next() {
_ = proto.Unmarshal(requestToUnMarshal, &request)
}
})
}
```


这里存在一个“问题”，那就是多goroutine会共享一个request。但在其他几个测试中同样的代码并未引发panic。我修改一下代码，将其放入for循环中：

```
func BenchmarkUnmarshalParalell(b *testing.B) {
b.ReportAllocs()
b.RunParallel(func(pb *testing.PB) {
for pb.Next() {
var request submit.Request
_ = proto.Unmarshal(requestToUnMarshal, &request)
}
})
}
```


再运行go protobuf v2的benchmark：

```
$go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/protobufbench_goprotov2
BenchmarkMarshal-8 2348630 509 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshal-8 1913904 627 ns/op 400 B/op 7 allocs/op
BenchmarkMarshalInParalell-8 7133936 175 ns/op 384 B/op 1 allocs/op
BenchmarkUnmarshalParalell-8 4841752 232 ns/op 576 B/op 8 allocs/op
PASS
ok github.com/bigwhite/protobufbench_goprotov2 6.355s
```


看来的确是这个问题。

从Benchmark结果来看，即便是与go protobuf v1相比，go protobuf v2生成的代码性能也要逊色一些，更不要说与gogo protobuf相比了。

## 三. 小结

从性能角度考虑，如果要使用go protobuf api，首选gogo protobuf。

如果从功能角度考虑，显然go protobuf v2在成熟稳定了以后，会成为Go语言功能上最为强大的protobuf API。

本文涉及源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/protobuf)下载。

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

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

为什么gogoprotobuf-fast更快呢