---
title: gRPC服务的响应设计
url: https://tonybai.com/2021/09/26/the-design-of-the-response-for-grpc-server/
published: '2021-09-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# gRPC服务的响应设计

![](../../assets/a52c547aee4e89bc.png)


[本文永久链接](https://tonybai.com/2021/09/26/the-design-of-the-response-for-grpc-server) – https://tonybai.com/2021/09/26/the-design-of-the-response-for-grpc-server

### 1. 服务端响应的现状

做后端服务的开发人员对错误处理总是很敏感的，因此在做服务的响应(response/reply)设计时总是会很慎重。

如果后端服务选择的是HTTP API(rest api)，比如json over http，API响应(Response）中大多会包含如下信息：

```
{
"code": 0,
"msg": "ok",
"payload" : {
... ...
}
}
```


在这个http api的响应设计中，前两个状态标识这个请求的响应状态。这个状态由一个状态代码(code)与状态信息(msg)组成。状态信息是对状态代码所对应错误原因的详细诠释。只有当状态为正常时(code = 0)，后面的payload才具有意义。payload显然是在响应中意图传给客户端的业务信息。

这样的服务响应设计是目前比较常用且成熟的方案，理解起来也十分容易。

好，现在我们看看另外一大类服务：采用RPC方式提供的服务。我们还是以使用最为广泛的gRPC为例。在gRPC中，一个service的定义如下(我们借用一下grpc-go提供的[helloworld示例](https://github.com/grpc/grpc-go/tree/master/examples/helloworld))：

```
// https://github.com/grpc/grpc-go/blob/master/examples/helloworld/helloworld/helloworld.proto
package helloworld;
// The greeting service definition.
service Greeter {
// Sends a greeting
rpc SayHello (HelloRequest) returns (HelloReply) {}
}
// The request message containing the user's name.
message HelloRequest {
string name = 1;
}
// The response message containing the greetings
message HelloReply {
string message = 1;
}
```


grpc对于每个rpc方法(比如SayHello)都有约束，只能有一个输入参数和一个返回值。这个.proto定义通过protoc生成的go代码变成了这样：

```
// https://github.com/grpc/grpc-go/blob/master/examples/helloworld/helloworld/helloworld_grpc.pb.go
type GreeterServer interface {
// Sends a greeting
SayHello(context.Context, *HelloRequest) (*HelloReply, error)
... ...
}
```


我们看到对于SayHello RPC方法，protoc生成的go代码中，SayHello方法的返回值列表中多了一个Gopher们熟悉的error返回值。对于已经习惯了HTTP API那套响应设计的gopher来说，现在问题来了! http api响应中表示响应状态的code与msg究竟是定义在HelloReply这个业务响应数据中，还是通过error来返回的呢？这个grpc官方文档似乎也没有明确说明（如果各位看官找到位置，可以告诉我哦）。

### 2. gRPC服务端响应设计思路

我们先不急着下结论！我们继续借用helloworld这个示例程序来测试一下当error返回值不为nil时客户端的反应！先改一下[greeter_server](https://github.com/grpc/grpc-go/blob/master/examples/helloworld/greeter_server/main.go)的代码：

```
// SayHello implements helloworld.GreeterServer
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
log.Printf("Received: %v", in.GetName())
return &pb.HelloReply{Message: "Hello " + in.GetName()}, errors.New("test grpc error")
}
```


在上面代码中，我们故意构造一个错误并返回给调用该方法的客户端。我们来运行一下这个服务并启动[greeter_client](https://github.com/grpc/grpc-go/tree/master/examples/helloworld/greeter_client)来访问该服务，在客户端侧，我们得到的结果如下：

```
2021/09/20 17:04:35 could not greet: rpc error: code = Unknown desc = test grpc error
```


从客户端的输出结果中，我们看到了我们自定义的错误的内容(test grpc error)。但我们还发现错误输出的内容中还有一个”code = Unknown”的输出，这个code是从何而来呢？似乎grpc期待的error形式是包含code与desc的形式。

这时候就不得不查看一下[gprc-go(v1.40.0)的参考文档](https://pkg.go.dev/google.golang.org/grpc#section-readme)了！在grpc-go的文档中我们发现几个被DEPRECATED的与Error有关的函数：

![](../../assets/98b29f0c6d0ecc34.png)


在这几个作废的函数的文档中都提到了用status包的同名函数替代。那么这个status包又是何方神圣？我们翻看grpc-go的源码，终于找到了status包，在包说明的第一句中我们就找到了答案：

```
Package status implements errors returned by gRPC.
```


原来status包实现了上面grpc客户端所期望的error类型。那么这个类型是什么样的呢？我们逐步跟踪代码：

在grpc-go/status包中我们看到如下代码：

```
type Status = status.Status
// New returns a Status representing c and msg.
func New(c codes.Code, msg string) *Status {
return status.New(c, msg)
}
```


status包使用了internal/status包中的Status，我们再来看internal/status包中Status结构的定义：

```
// internal/status
type Status struct {
s *spb.Status
}
// New returns a Status representing c and msg.
func New(c codes.Code, msg string) *Status {
return &Status{s: &spb.Status{Code: int32(c), Message: msg}}
}
```


internal/status包的Status结构体组合了一个*spb.Status类型(google.golang.org/genproto/googleapis/rpc/status包中的类型)的字段，继续追踪spb.Status:

```
// https://pkg.go.dev/google.golang.org/genproto/googleapis/rpc/status
type Status struct {
// The status code, which should be an enum value of [google.rpc.Code][google.rpc.Code].
Code int32 `protobuf:"varint,1,opt,name=code,proto3" json:"code,omitempty"`
// A developer-facing error message, which should be in English. Any
// user-facing error message should be localized and sent in the
// [google.rpc.Status.details][google.rpc.Status.details] field, or localized by the client.
Message string `protobuf:"bytes,2,opt,name=message,proto3" json:"message,omitempty"`
// A list of messages that carry the error details. There is a common set of
// message types for APIs to use.
Details []*anypb.Any `protobuf:"bytes,3,rep,name=details,proto3" json:"details,omitempty"`
// contains filtered or unexported fields
}
```


我们看到最后的这个Status结构包含了Code与Message。这样一来，grpc的设计意图就很明显了，它期望开发者在error这个返回值中包含rpc方法的响应状态，而自定义的响应结构体只需包含业务所需要的数据即可。我们用一幅示意图来横向建立一下http api与rpc响应的映射关系：

![](../../assets/2406fa2d97bd27fe.png)


有了这幅图，再面对如何设计grpc方法响应这个问题时，我们就胸有成竹了！

grpc-go在[codes包](https://pkg.go.dev/google.golang.org/grpc@v1.40.0/codes#Code)中定义了grpc规范要求的10余种错误码：

```
const (
// OK is returned on success.
OK Code = 0
// Canceled indicates the operation was canceled (typically by the caller).
//
// The gRPC framework will generate this error code when cancellation
// is requested.
Canceled Code = 1
// Unknown error. An example of where this error may be returned is
// if a Status value received from another address space belongs to
// an error-space that is not known in this address space. Also
// errors raised by APIs that do not return enough error information
// may be converted to this error.
//
// The gRPC framework will generate this error code in the above two
// mentioned cases.
Unknown Code = 2
// InvalidArgument indicates client specified an invalid argument.
// Note that this differs from FailedPrecondition. It indicates arguments
// that are problematic regardless of the state of the system
// (e.g., a malformed file name).
//
// This error code will not be generated by the gRPC framework.
InvalidArgument Code = 3
... ...
// Unauthenticated indicates the request does not have valid
// authentication credentials for the operation.
//
// The gRPC framework will generate this error code when the
// authentication metadata is invalid or a Credentials callback fails,
// but also expect authentication middleware to generate it.
Unauthenticated Code = 16
```


在这些标准错误码之外，我们还可以扩展定义自己的错误码与错误描述。

### 3. 服务端如何构造error与客户端如何解析error

前面提到，gRPC服务端采用rpc方法的最后一个返回值error来承载应答状态。google.golang.org/grpc/status包为构建客户端可解析的error提供了一些方便的函数，我们看下面示例（基于上面helloworld的[greeter_server](https://github.com/grpc/grpc-go/blob/master/examples/helloworld/greeter_server/main.go)改造）：

```
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
log.Printf("Received: %v", in.GetName())
return nil, status.Errorf(codes.InvalidArgument, "you have a wrong name: %s", in.GetName())
}
```


status包提供了一个类似于fmt.Errorf的函数，我们可以很方便的构造一个带有code与msg的error实例并返回给客户端。

而客户端同样可以通过status包提供的函数将error中携带的信息解析出来，我们看下面代码：

```
ctx, _ := context.WithTimeout(context.Background(), time.Second)
r, err := c.SayHello(ctx, &pb.HelloRequest{Name: "tony")})
if err != nil {
errStatus := status.Convert(err)
log.Printf("SayHello return error: code: %d, msg: %s\n", errStatus.Code(), errStatus.Message())
}
log.Printf("Greeting: %s", r.GetMessage())
```


我们看到：通过status.Convert函数可以很简答地将rpc方法返回的不为nil的error中携带的信息提取出来。

### 4. 空应答

gRPC的proto文件规范要求每个rpc方法的定义中都必须包含一个返回值，返回值不能为空，比如上面helloworld项目的.proto文件中的SayHello方法：

```
rpc SayHello (HelloRequest) returns (HelloReply) {}
```


如果去掉HelloReply这个返回值，那么protoc在生成代码时会报错！

但是有些方法本身不需要返回业务数据，那么我们就需要为其定义一个空应答消息，比如：

```
message Empty {
}
```


考虑到每个项目在遇到空应答时都要重复造上面Empty message定义的轮子，grpc官方提供了一个可被复用的空message：

```
// https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/empty.proto
// A generic empty message that you can re-use to avoid defining duplicated
// empty messages in your APIs. A typical example is to use it as the request
// or the response type of an API method. For instance:
//
// service Foo {
// rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
// }
//
// The JSON representation for `Empty` is empty JSON object `{}`.
message Empty {}
```


我们只需在.proto文件中导入该empty.proto并使用Empty即可，比如下面代码：

```
// xxx.proto
syntax = "proto3";
import "google/protobuf/empty.proto";
service MyService {
rpc MyRPCMethod(...) returns (google.protobuf.Empty);
}
```


当然google.protobuf.Empty不仅仅适用于空响应，也适合空请求，这个就留给大家可自行完成吧。

### 5. 小结

本文我们讲述了gRPC服务端响应设计的相关内容，最主要想说的是直接使用gRPC生成的rpc方面的error返回值来表示rpc调用的响应状态，不要再在自定义的Message结构中重复放入code与msg字段来表示响应状态了。

btw，做API的错误设计，[google的这份API设计方面的参考资料](https://cloud.google.com/apis/design/errors)是十分好的。有时间一定要好好读读哦。

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