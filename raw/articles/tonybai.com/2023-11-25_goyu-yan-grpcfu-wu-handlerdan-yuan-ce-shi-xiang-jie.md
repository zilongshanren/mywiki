---
title: Go语言gRPC服务Handler单元测试详解
url: https://tonybai.com/2023/11/25/grpc-handler-unit-testing-in-go/
published: '2023-11-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言gRPC服务Handler单元测试详解

![](../../assets/9ff1c2b266335829.png)


[本文永久链接](https://tonybai.com/2023/11/25/grpc-handler-unit-testing-in-go) – https://tonybai.com/2023/11/25/grpc-handler-unit-testing-in-go

在云原生时代和微服务架构背景下，HTTP和RPC协议成为服务间通信和与客户端交互的两种主要方式。对于Go语言而言，标准库提供了net/http/httptest包，为开发人员提供了便捷的方式来构建服务端HTTP Handler单元测试的测试脚手架代码，而无需真正建立HTTP服务器，让开发人员可以聚焦于对Handler业务逻辑的测试。比如下面这个示例：

```
// grpc-test-examples/httptest/http_handler_test.go
func myHandler(w http.ResponseWriter, r *http.Request) {
// 设置响应头
w.Header().Set("Content-Type", "text/plain")
// 根据请求方法进行不同的处理
switch r.Method {
case http.MethodGet:
// 处理GET请求
fmt.Fprint(w, "Hello, World!")
... ...
}
}
func TestMyHandler(t *testing.T) {
// 创建一个ResponseRecorder来记录Handler的响应
rr := httptest.NewRecorder()
// 创建一个模拟的HTTP请求，可以指定请求的方法、路径、正文等
req, err := http.NewRequest("GET", "/path", nil)
if err != nil {
t.Fatal(err)
}
// 调用被测试的Handler函数，传入ResponseRecorder和Request对象
// 这里假设被测试的Handler函数为myHandler
myHandler(rr, req)
// 检查响应状态码和内容
if rr.Code != http.StatusOK {
t.Errorf("Expected status 200; got %d", rr.Code)
}
expected := "Hello, World!"
if rr.Body.String() != expected {
t.Errorf("Expected body to be %q; got %q", expected, rr.Body.String())
}
}
```


注：对http client端的单元测试，也可以

[利用httptest的NewServer来构建一个fake的http server]。

然而，对于使用主流的[gRPC等RPC协议的服务端Handler](https://tonybai.com/2021/09/26/the-design-of-the-response-for-grpc-server)来说，是否存在类似httptest的测试脚手架生成工具包呢？对gRPC的服务端Handler有哪些单元测试的方法呢？在这篇文章中，我们就一起来探究一下。

## 1. 建立被测的gRPC服务端Handler

我们首先来建立一个涵盖多种gRPC通信模式的服务端Handler集合。

gRPC支持四种通信模式，它们分别为：

- 简单RPC(Simple RPC，也称为Unary RPC)

这是最简单的，也是最常用的gRPC通信模式，简单来说就是**一请求一应答**。

- 服务端流RPC(Server-streaming RPC)

客户端发来一个请求，服务端通过流返回多个应答。

- 客户端流RPC(Client-streaming RPC)

客户端通过流发来多个请求，服务端以一个应答回复。

- 双向流RPC(Bidirectional-Streaming RPC)

客户端通过流发起多个请求，服务端也通过流对应返回多个应答。

注：关于gRPC四种通信方式的详情，可以参考我之前写的《

[gRPC客户端的那些事儿]》一文。

我们这个SUT(被测目标)是包含以上四种通信模式的gRPC服务，它的[Protocol Buffers](https://protobuf.dev/)文件如下：

```
// grpc-test-examples/grpctest/IDL/proto/mygrpc.proto
syntax = "proto3";
package mygrpc;
service MyService {
// Unary RPC
rpc UnaryRPC(RequestMessage) returns (ResponseMessage) {}
// Server-Streaming RPC
rpc ServerStreamingRPC(RequestMessage) returns (stream ResponseMessage) {}
// Client-Streaming RPC
rpc ClientStreamingRPC(stream RequestMessage) returns (ResponseMessage) {}
// Bidirectional-Streaming RPC
rpc BidirectionalStreamingRPC(stream RequestMessage) returns (stream ResponseMessage) {}
}
message RequestMessage {
string message = 1;
}
message ResponseMessage {
string message = 1;
}
```


通过protoc，我们可基于上述proto文件生成MyService桩(Stub)代码，生成的代码放在了mygrpc目录下面：

```
// grpc-test-examples/grpctest/Makefile
all: gen
gen:
protoc -I ./IDL/proto mygrpc.proto --gofast_out=plugins=grpc:./mygrpc
```


注：你的环境下需要安装

[protoc]和[protoc-gen-go]才能正确执行上面生成命令，具体的安装方法可参考[protoc安装文档]。注：除了使用经典的

[protoc]基于proto文件生成Go源码外，也可以基于Go开发的[buf cli]进行代码生成和API管理。buf cLi是现代、快速、高效的Protobuf API管理的终极工具，为基于Protobuf的开发和维护提供了全面的解决方案。等有机会的时候，我在以后的文章中详细说说buf。

有了生成的桩代码后，我们便可以建立一个gRPC服务器：

```
// grpc-test-examples/grpctest/main.go
package main
import (
pb "demo/mygrpc"
"log"
"net"
"google.golang.org/grpc"
)
func main() {
// 创建 gRPC 服务器
lis, err := net.Listen("tcp", ":50051")
if err != nil {
log.Fatalf("failed to listen: %v", err)
}
s := grpc.NewServer()
// 注册 MyService 服务
pb.RegisterMyServiceServer(s, &server{})
// 启动 gRPC 服务器
log.Println("Starting gRPC server...")
if err := s.Serve(lis); err != nil {
log.Fatalf("failed to serve: %v", err)
}
}
```


我们看到：在main函数中，我们创建了一个TCP监听器，并使用grpc.NewServer()创建了一个gRPC服务器。然后，我们通过调用pb.RegisterMyServiceServer()将server类型的实例注册到gRPC服务器上，以处理来自客户端的请求。最后，我们启动gRPC服务器并监听指定的端口。

上面代码中注册到服务器中的server类型就是实现了MyService服务接口的具体类型，它实现了MyService定义的所有方法：

```
// grpc-test-examples/grpctest/server.go
package main
import (
"context"
"fmt"
"strconv"
pb "demo/mygrpc"
)
type server struct{}
func (s *server) UnaryRPC(ctx context.Context, req *pb.RequestMessage) (*pb.ResponseMessage, error) {
message := "Unary RPC received: " + req.Message
fmt.Println(message)
return &pb.ResponseMessage{
Message: "Unary RPC response",
}, nil
}
func (s *server) ServerStreamingRPC(req *pb.RequestMessage, stream pb.MyService_ServerStreamingRPCServer) error {
message := "Server Streaming RPC received: " + req.Message
fmt.Println(message)
for i := 0; i < 5; i++ {
response := &pb.ResponseMessage{
Message: "Server Streaming RPC response " + strconv.Itoa(i+1),
}
if err := stream.Send(response); err != nil {
return err
}
}
return nil
}
func (s *server) ClientStreamingRPC(stream pb.MyService_ClientStreamingRPCServer) error {
var messages []string
for {
req, err := stream.Recv()
if err != nil {
return err
}
messages = append(messages, req.Message)
if req.Message == "end" {
break
}
}
message := "Client Streaming RPC received: " + fmt.Sprintf("%v", messages)
fmt.Println(message)
return stream.SendAndClose(&pb.ResponseMessage{
Message: "Client Streaming RPC response",
})
}
func (s *server) BidirectionalStreamingRPC(stream pb.MyService_BidirectionalStreamingRPCServer) error {
for {
req, err := stream.Recv()
if err != nil {
return err
}
message := "Bidirectional Streaming RPC received: " + req.Message
fmt.Println(message)
response := &pb.ResponseMessage{
Message: "Bidirectional Streaming RPC response",
}
if err := stream.Send(response); err != nil {
return err
}
}
}
```


在上面代码中，我们创建了一个server结构体类型，并实现了MyService的所有RPC方法。每个方法都接收相应的请求消息，并返回对应的响应消息。我们的目标仅是演示如何对上述gRPC Handler进行单元测试，所以这里的实现逻辑非常简单。

接下来，我们就来逐一对这些gRPC的Handler方法进行单测，我们先从简单的UnaryRPC方法开始。

## 2. Unary RPC Handler的单元测试

Unary RPC是最简单，也是最容易理解的RPC通信模式，即客户端与服务端采用一请求一应答的模式。server类型的UnaryRPC Handler方法的原型如下：

```
// grpc-test-examples/grpctest/server.go
func (s *server) UnaryRPC(ctx context.Context, req *pb.RequestMessage) (*pb.ResponseMessage, error)
```


就像文章开头做的那个httpserver的handler单测一样，我们肯定不想真实启动一个gRPC server，也不想测试gRPC服务器本身。我们只想测试服务端handler方法的逻辑是否正确。

观察一下这个方法原型，我们发现它仅依赖两个消息结构：RequestMessage和ResponseMessage，这两个消息结构是上面基于proto文件自动生成的，这样我们就可以不借助任何工具包实现对UnaryRPC handler方法的单测，也无需启动真实的gRPC Server：

```
// grpc-test-examples/grpctest/server_test.go
type server struct{}
func TestServerUnaryRPC(t *testing.T) {
s := &server{}
req := &pb.RequestMessage{
Message: "Test message",
}
resp, err := s.UnaryRPC(context.Background(), req)
if err != nil {
t.Fatalf("UnaryRPC failed: %v", err)
}
expectedResp := &pb.ResponseMessage{
Message: "Unary RPC response",
}
if resp.Message != expectedResp.Message {
t.Errorf("Unexpected response. Got: %s, Want: %s", resp.Message, expectedResp.Message)
}
}
```


将其改造为[基于subtest](https://tonybai.com/2023/03/15/an-intro-of-go-subtest/)和表驱动的测试也非常easy：

```
// grpc-test-examples/grpctest/server_test.go
func TestServerUnaryRPCs(t *testing.T) {
tests := []struct {
name string
requestMessage *pb.RequestMessage
expectedResp *pb.ResponseMessage
}{
{
name: "Test Case 1",
requestMessage: &pb.RequestMessage{
Message: "Test message",
},
expectedResp: &pb.ResponseMessage{
Message: "Unary RPC response",
},
},
// Add more test cases as needed
}
s := &server{}
for _, tt := range tests {
t.Run(tt.name, func(t *testing.T) {
resp, err := s.UnaryRPC(context.Background(), tt.requestMessage)
if err != nil {
t.Fatalf("UnaryRPC failed: %v", err)
}
if resp.Message != tt.expectedResp.Message {
t.Errorf("Unexpected response. Got: %s, Want: %s", resp.Message, tt.expectedResp.Message)
}
})
}
}
```


如果gRPC handler测试都像UnaryRPC这样简单那就好了，但实际上…，好吧，我们继续向下看就好了。

## 3. 针对Streaming通信模式的单元测试

### 3.1 ServerStreamingRPC的测试

前面说过，gRPC支持三种Streaming通信模式：Server-Streaming RPC、Client-Streaming RPC和Bidirectional-Streaming RPC。

我们先来看看Server-Streaming RPC的方法原型：

```
// grpc-test-examples/grpctest/server.go
func (s *server) ServerStreamingRPC(req *pb.RequestMessage, stream pb.MyService_ServerStreamingRPCServer) error
```


我们看到除了RequestMessag外，该方法还依赖一个MyService_ServerStreamingRPCServer的类型，这个类型是一个接口类型：

```
// grpc-test-examples/mygrpc/mygrpc.pb.go
type MyService_ServerStreamingRPCServer interface {
Send(*ResponseMessage) error
grpc.ServerStream
}
```


到这里，你脑子中可能已经冒出了一个想法：[使用fake object来对ServerStreamingRPC进行单测](https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators/)，这的确是一个可行的方法，我们下面就基于这个思路实现一下。

注：关于基于fake object进行单测的内容，大家可以看看我以前写的一篇文章《[]单测时尽量用fake object(https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators)》。


### 3.2 基于fake object的测试

我们首先创建一个实现MyService_ServerStreamingRPCServer的fake object用以代替真实运行RPC服务器时由服务器传入的stream object：

```
// grpc-test-examples/grpctest/server_with_fakeobject_test.go
import (
"testing"
pb "demo/mygrpc"
"google.golang.org/grpc"
)
type fakeServerStreamingRPCStream struct {
grpc.ServerStream
responses []*pb.ResponseMessage
}
func (m *fakeServerStreamingRPCStream) Send(resp *pb.ResponseMessage) error {
m.responses = append(m.responses, resp)
return nil
}
```


我们看到fakeServerStreamingRPCStream的Send方法只是将收到的ResponseMessage追加到且内部的ResponseMessage切片中。

接下来我们为ServerStreamingRPC编写测试用例：

```
// grpc-test-examples/grpctest/server_with_fakeobject_test.go
func TestServerServerStreamingRPC(t *testing.T) {
s := &server{}
req := &pb.RequestMessage{
Message: "Test message",
}
stream := &fakeServerStreamingRPCStream{}
err := s.ServerStreamingRPC(req, stream)
if err != nil {
t.Fatalf("ServerStreamingRPC failed: %v", err)
}
expectedResponses := []string{
"Server Streaming RPC response 1",
"Server Streaming RPC response 2",
"Server Streaming RPC response 3",
"Server Streaming RPC response 4",
"Server Streaming RPC response 5",
}
if len(stream.responses) != len(expectedResponses) {
t.Errorf("Unexpected number of responses. Got: %d, Want: %d", len(stream.responses), len(expectedResponses))
}
for i, resp := range stream.responses {
if resp.Message != expectedResponses[i] {
t.Errorf("Unexpected response at index %d. Got: %s, Want: %s", i, resp.Message, expectedResponses[i])
}
}
}
```


在这个测试中，ServerStreamingRPC接收一个请求(req)，并通过fake stream object的Send方法返回了5个response，通过与预期的response对比，即可做出测试是否通过的断言。

到这里，我们看到：fake object完全满足对gRPC Server Handler进行测试的要求。不过我们需要针对不同的Handler建立不同的fake object类型，和文初基于httptest创建的测试用例相比，用例间欠缺了一些一致性。

那grpc-go是否提供了类似httptest的工具来帮助我们更一致的实现grpc server handler的测试用例呢？我们继续往下看。

### 3.3 利用grpc-go提供的测试工具包

grpc-go项目在test下提供了bufconn包，可以帮助我们像httptest那样建立用于测试的“虚拟gRPC服务器”，下面是基于bufconn包建立gRPC测试用服务器的代码：

```
// grpc-test-examples/grpctest/server_with_buffconn_test.go
package main
import (
"context"
"log"
"net"
"testing"
pb "demo/mygrpc"
"google.golang.org/grpc"
"google.golang.org/grpc/test/bufconn"
)
func newGRPCServer(t *testing.T) (pb.MyServiceClient, func()) {
// 创建 bufconn.Listener 作为服务器的监听器
listener := bufconn.Listen(1024 * 1024)
// 创建 gRPC 服务器
srv := grpc.NewServer()
// 注册服务处理程序
pb.RegisterMyServiceServer(srv, &server{})
// 在监听器上启动服务器
go func() {
if err := srv.Serve(listener); err != nil {
t.Fatalf("Server failed to start: %v", err)
}
}()
// 创建 bufconn.Dialer 作为客户端连接
dialer := func(context.Context, string) (net.Conn, error) {
return listener.Dial()
}
// 使用 DialContext 和 bufconn.Dialer 创建客户端连接
conn, err := grpc.DialContext(context.Background(), "bufnet", grpc.WithContextDialer(dialer), grpc.WithInsecure())
if err != nil {
t.Fatalf("Failed to dial server: %v", err)
}
// 创建客户端实例
client := pb.NewMyServiceClient(conn)
return client, func() {
err := listener.Close()
if err != nil {
log.Printf("error closing listener: %v", err)
}
srv.Stop()
}
}
```


newGRPCServer是一个用于在测试中创建gRPC服务器和客户端的辅助函数，它使用bufconn.Listen创建一个bufconn.Listener作为服务器的监听器。bufconn包提供了一种在内存中模拟网络连接的方法。然后，它使用grpc.NewServer()创建了一个新的gRPC服务器实例，并使用pb.RegisterMyServiceServer将待测的服务实例(这里是server类型实例)注册到gRPC服务器中。接下来，它创建了与该服务器建连的gRPC客户端，由于该客户端要与bufconn.Listener建连，这里用了一个dialer函数，该函数将通过调用listener.Dial()来建立与服务器的连接。之后基于该连接，我们创建了MyServiceClient的客户端实例，并返回，供测试用例使用。

基于newGPRCServer这种方式，我们改造一下UnaryRPC的测试用例：

```
// grpc-test-examples/grpctest/server_with_buffconn_test.go
func TestServerUnaryRPCWithBufConn(t *testing.T) {
client, shutdown := newGRPCServer(t)
defer shutdown()
tests := []struct {
name string
requestMessage *pb.RequestMessage
expectedResp *pb.ResponseMessage
}{
{
name: "Test Case 1",
requestMessage: &pb.RequestMessage{
Message: "Test message",
},
expectedResp: &pb.ResponseMessage{
Message: "Unary RPC response",
},
},
// Add more test cases as needed
}
for _, tt := range tests {
t.Run(tt.name, func(t *testing.T) {
resp, err := client.UnaryRPC(context.Background(), tt.requestMessage)
if err != nil {
t.Fatalf("UnaryRPC failed: %v", err)
}
if resp.Message != tt.expectedResp.Message {
t.Errorf("Unexpected response. Got: %s, Want: %s", resp.Message, tt.expectedResp.Message)
}
})
}
}
```


我们看到，相对于前面的TestServerUnaryRPCs，两者复杂度在一个层次。如果结合下面的ServerStreamRPC的测试用例，你就能看出这种方式在测试用例一致性方面的优势了：

```
// grpc-test-examples/grpctest/server_with_buffconn_test.go
func TestServerServerStreamingRPCWithBufConn(t *testing.T) {
client, shutdown := newGRPCServer(t)
defer shutdown()
req := &pb.RequestMessage{
Message: "Test message",
}
stream, err := client.ServerStreamingRPC(context.Background(), req)
if err != nil {
t.Fatalf("ServerStreamingRPC failed: %v", err)
}
expectedResponses := []string{
"Server Streaming RPC response 1",
"Server Streaming RPC response 2",
"Server Streaming RPC response 3",
"Server Streaming RPC response 4",
"Server Streaming RPC response 5",
}
gotResponses := []string{}
for {
resp, err := stream.Recv()
if err != nil {
break
}
gotResponses = append(gotResponses, resp.Message)
}
if len(gotResponses) != len(expectedResponses) {
t.Errorf("Unexpected number of responses. Got: %d, Want: %d", len(gotResponses), len(expectedResponses))
}
for i, resp := range gotResponses {
if resp != expectedResponses[i] {
t.Errorf("Unexpected response at index %d. Got: %s, Want: %s", i, resp, expectedResponses[i])
}
}
}
```


我们再也无需为每个Server Handler建立各自的fake object了！

由此看到：grpc-go的test/bufconn就是类似httptest的那个grpc server handler的测试脚手架搭建工具。

### 3.4 其他Streaming模式的Handler测试

有了bufconn这一利器，其他Streaming模式的Handler测试实现逻辑就大同小异了。本文示例中的ClientStreamingRPC和BidirectionalStreamingRPC两个Handler的测试用例就作为作业，交给各位读者去完成吧！

## 4. 小结

在本文中，我们详细探讨了如何对gRPC服务端Handler进行单元测试，我们的目标是找到像net/http/httptest包那样的，可以为gRPC服务端handler测试提供脚手架代码帮助的测试方法。

我们按照gRPC的四种通信方式，由简到难的逐一探讨各种Handler的单测方法。UnaryRPC handler测试最为简单，毫无技巧的普通测试逻辑便能应付。

但一旦涉及streaming通信方式的测试，我们就需要借助类似fake object的单测技术了。但fake object也有不足，那就是需要为每个RPC handler建立单独的fake object，费时费力还缺少一致性！

好在，grpc-go项目为我们提供了test/bufconn包，该包可以像net/http/httptest包那样帮助我们快速建立可复用的测试脚手架代码，这样我们便可以为所有服务端RPC Handler建立一致、稳定的单元测试用例了！

当然，服务端RPC Handler的单测方法可能不止文中提及这些，各位读者如果有更好的方法和实践，欢迎在评论区留言！

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/grpc-test-examples)下载。

## 5. 参考资料

[Testing gRPC methods](https://medium.com/@johnsiilver/testing-grpc-methods-6a8edad4159d)– https://medium.com/@johnsiilver/testing-grpc-methods-6a8edad4159d[《gRPC Up and Running》](https://book.douban.com/subject/34796013/)– https://book.douban.com/subject/34796013/[Mocking the Universe: Two Techniques for Testing gRPC with Mocks](https://rotational.io/blog/mocking-the-universe/)– https://rotational.io/blog/mocking-the-universe/

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