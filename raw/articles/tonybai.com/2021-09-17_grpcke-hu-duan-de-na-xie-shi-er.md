---
title: gRPC客户端的那些事儿
url: https://tonybai.com/2021/09/17/those-things-about-grpc-client/
published: '2021-09-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# gRPC客户端的那些事儿

![](../../assets/f990d9f2222039fb.png)


[本文永久链接](https://tonybai.com/2021/09/17/those-things-about-grpc-client) – https://tonybai.com/2021/09/17/those-things-about-grpc-client

在云原生与微服务主导架构模式的时代，内部服务间交互所采用的通信协议选型无非就是两类：HTTP API(RESTful API)和RPC。在如今的硬件配置与网络条件下，现代RPC实现的性能一般都是好于HTTP API的。我们以json over http与[gRPC](https://grpc.io)(insecure)作比较，分别使用[ghz](https://github.com/bojand/ghz)和[hey](https://github.com/rakyll/hey)压测gRPC和json over http的实现，gRPC的性能（Requests/sec: 59924.34）要比http api性能(Requests/sec: 49969.9234)高出20%。实测gPRC使用的protobuf的编解码性能更是最快的json编解码的2-3倍，是Go标准库json包编解码性能的10倍以上(具体数据见本文附录)。

对于性能敏感并且内部通信协议较少变动的系统来说，内部服务使用RPC可能是多数人的选择。而gRPC虽然不是性能最好的RPC实现，但作为有谷歌大厂背书且是[CNCF唯一的RPC项目](https://www.cncf.io/projects/)，gRPC自然得到了开发人员最广泛的关注与使用。

本文也来说说gRPC，不过我们更多关注一下gRPC的客户端，我们来看看使用gRPC客户端时都会考虑的那些事情（本文所有代码基于gRPC v1.40.0版本，[Go 1.17版本](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg))。

### 1. 默认的gRPC的客户端

gRPC支持四种通信模式，它们是（以下四张图截自[《gRPC: Up and Running》](https://book.douban.com/subject/34796013/)一书）：

- 简单RPC(Simple RPC)：最简单的，也是最常用的gRPC通信模式，简单来说就是
**一请求一应答**

![](../../assets/3685aab78368a31f.png)


- 服务端流RPC(Server-streaming RPC)：
**一请求，多应答**

![](../../assets/2b1ea6e830a40a5c.png)


- 客户端流RPC(Client-streaming RPC)：
**多请求，一应答**

![](../../assets/abcfc9c7edaafed9.png)


- 双向流RPC(Bidirectional-Streaming RPC)：
**多请求，多应答**

![](../../assets/86fbce279820bef8.png)


我们以最常用的Simple RPC(也称Unary RPC)为例来看一下如何实现一个gRPC版的helloworld。

我们无需自己从头来编写helloworld.proto并生成相应的gRPC代码，[gRPC官方提供了一个helloworld的例子](https://github.com/grpc/grpc-go/tree/master/examples/helloworld)，我们仅需对其略微改造一下即可。

helloworld例子的IDL文件helloworld.proto如下：

```
// https://github.com/grpc/grpc-go/tree/master/examples/helloworld/helloworld/helloworld.proto
syntax = "proto3";
option go_package = "google.golang.org/grpc/examples/helloworld/helloworld";
option java_multiple_files = true;
option java_package = "io.grpc.examples.helloworld";
option java_outer_classname = "HelloWorldProto";
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


对.proto文件的规范讲解大家可以参考[grpc官方文档](https://grpc.io/docs/what-is-grpc/core-concepts/)，这里不赘述。显然上面这个IDL是极致简单的。这里定义了一个service：Greeter，它仅包含一个方法SayHello，并且这个方法的参数与返回值都是一个仅包含一个string字段的结构体。

我们无需手工执行protoc命令来基于该.proto文件生成对应的Greeter service的实现以及HelloRequest、HelloReply的protobuf编解码实现，因为gRPC在example下已经放置了生成后的Go源文件，我们直接引用即可。这里要注意，最新的[grpc-go项目仓库](https://github.com/grpc/grpc-go)采用了多module的管理模式，examples作为一个独立的go module而存在，因此我们需要将其单独作为一个module导入到其使用者的项目中。以gRPC客户端greeter_client为例，它的go.mod要这样来写：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo1/greeter_client/go.mod
module github.com/bigwhite/grpc-client/demo1
go 1.17
require (
google.golang.org/grpc v1.40.0
google.golang.org/grpc/examples v1.40.0
)
require (
github.com/golang/protobuf v1.4.3 // indirect
golang.org/x/net v0.0.0-20201021035429-f5854403a974 // indirect
golang.org/x/sys v0.0.0-20200930185726-fdedc70b468f // indirect
golang.org/x/text v0.3.3 // indirect
google.golang.org/genproto v0.0.0-20200806141610-86f49bd18e98 // indirect
google.golang.org/protobuf v1.25.0 // indirect
)
replace google.golang.org/grpc v1.40.0 => /Users/tonybai/Go/src/github.com/grpc/grpc-go
replace google.golang.org/grpc/examples v1.40.0 => /Users/tonybai/Go/src/github.com/grpc/grpc-go/examples
```


注：grpc-go项目的标签(tag)似乎打的有问题，由于没有打grpc/examples/v1.40.0标签，go命令在grpc-go的v1.40.0标签中找不到examples，因此上面的go.mod中使用了一个replace trick(example module的v1.40.0版本是假的哦)，将examples module指向本地的代码。


gRPC通信的两端我们也稍作改造。原greeter_client仅发送一个请求便退出，这里我们将其改为每隔2s发送请求（便于后续观察），如下面代码所示：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo1/greeter_client/main.go
... ...
func main() {
// Set up a connection to the server.
ctx, cf1 := context.WithTimeout(context.Background(), time.Second*3)
defer cf1()
conn, err := grpc.DialContext(ctx, address, grpc.WithInsecure(), grpc.WithBlock())
if err != nil {
log.Fatalf("did not connect: %v", err)
}
defer conn.Close()
c := pb.NewGreeterClient(conn)
// Contact the server and print out its response.
name := defaultName
if len(os.Args) > 1 {
name = os.Args[1]
}
for i := 0; ; i++ {
ctx, _ := context.WithTimeout(context.Background(), time.Second)
r, err := c.SayHello(ctx, &pb.HelloRequest{Name: fmt.Sprintf("%s-%d", name, i+1)})
if err != nil {
log.Fatalf("could not greet: %v", err)
}
log.Printf("Greeting: %s", r.GetMessage())
time.Sleep(2 * time.Second)
}
}
```


greeter_server加了一个命令行选项-port并支持[gRPC server的优雅退出](https://www.imooc.com/read/87/article/2473)：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo1/greeter_server/main.go
... ...
var port int
func init() {
flag.IntVar(&port, "port", 50051, "listen port")
}
func main() {
flag.Parse()
lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", port))
if err != nil {
log.Fatalf("failed to listen: %v", err)
}
s := grpc.NewServer()
pb.RegisterGreeterServer(s, &server{})
go func() {
if err := s.Serve(lis); err != nil {
log.Fatalf("failed to serve: %v", err)
}
}()
var c = make(chan os.Signal)
signal.Notify(c, os.Interrupt, os.Kill)
<-c
s.Stop()
fmt.Println("exit")
}
```


搞定go.mod以及对client和server进行改造ok后，我们就可以来构建和运行greeter_client和greeter_server了：

```
编译和启动server：
$cd grpc-client/demo1/greeter_server
$make
$./demo1-server -port 50051
2021/09/11 12:10:33 Received: world-1
2021/09/11 12:10:35 Received: world-2
2021/09/11 12:10:37 Received: world-3
... ...
编译和启动client：
$cd grpc-client/demo1/greeter_client
$make
$./demo1-client
2021/09/11 12:10:33 Greeting: Hello world-1
2021/09/11 12:10:35 Greeting: Hello world-2
2021/09/11 12:10:37 Greeting: Hello world-3
... ...
```


我们看到：greeter_client和greeter_server启动后可以正常的通信！我们重点看一下greeter_client。

greeter_client在Dial服务端时传给DialContext的target参数是一个静态的服务地址：

```
const (
address = "localhost:50051"
)
```


这个形式的target经过google.golang.org/grpc/internal/grpcutil.ParseTarget的解析后返回一个值为nil的resolver.Target。于是gRPC采用默认的scheme：”passthrough”(github.com/grpc/grpc-go/resolver/resolver.go)，默认的”passthrough” scheme下，gRPC将使用内置的passthrough resolver(google.golang.org/grpc/internal/resolver/passthrough)。默认的这个passthrough resolver是如何设置要连接的service地址的呢？下面是passthrough resolver的代码摘录：

```
// github.com/grpc/grpc-go/internal/resolver/passthrough/passthrough.go
func (r *passthroughResolver) start() {
r.cc.UpdateState(resolver.State{Addresses: []resolver.Address{{Addr: r.target.Endpoint}}})
}
```


我们看到它将target.Endpoint，即localhost:50051直接传给了ClientConnection(上面代码的r.cc)，后者将向这个地址建立tcp连接。这正应了该resolver的名字：**passthrough**。

上面greeter_client连接的仅仅是service的一个实例(instance)，如果我们同时启动了该service的三个实例，比如使用[goreman](https://github.com/mattn/goreman)通过加载脚本文件来启动多个service实例：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo1/greeter_server/Procfile
# Use goreman to run `go get github.com/mattn/goreman`
demo1-server1: ./demo1-server -port 50051
demo1-server2: ./demo1-server -port 50052
demo1-server3: ./demo1-server -port 50053
同时启动多实例：
$goreman start
15:22:12 demo1-server3 | Starting demo1-server3 on port 5200
15:22:12 demo1-server2 | Starting demo1-server2 on port 5100
15:22:12 demo1-server1 | Starting demo1-server1 on port 5000
```


那么我们应该如何告诉greeter_client去连接这三个实例呢？是否可以将address改为下面这样就可以了呢：

```
const (
address = "localhost:50051,localhost:50052,localhost:50053"
defaultName = "world"
)
```


我们来改改试试，修改后重新编译greeter_client，启动greeter_client，我们看到下面结果：

```
$./demo1-client
2021/09/11 15:26:32 did not connect: context deadline exceeded
```


greeter_client连接server超时！也就是说像上面这样简单的传入多个实例的地址是不行的！那问题来了！我们该怎么让greeter_client去连接一个service的多个实例呢？我们继续向下看。

### 2. 连接一个Service的多个实例(instance)

grpc.Dial/grpc.DialContext的参数target可不仅仅是service实例的服务地址这么简单，**它的实参(argument)形式决定了gRPC client将采用哪一个resolver来确定service实例的地址集合**。

下面我们以一个返回service实例地址静态集合(即service的实例数量固定且服务地址固定)的StaticResolver为例，来看如何让gRPC client连接一个Service的多个实例。

#### 1) StaticResolver

我们首先来设计一下传给grpc.DialContext的target形式。[关于gRPC naming resolution，gRPC有专门文档说明](https://github.com/grpc/grpc/blob/master/doc/naming.md)。在这里，我们也创建一个新的scheme：static，多个service instance的服务地址通过逗号分隔的字符串传入，如下面代码：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo2/greeter_client/main.go
const (
address = "static:///localhost:50051,localhost:50052,localhost:50053"
)
```


当address被作为target的实参传入grpc.DialContext后，它会被grpcutil.ParseTarget解析为一个resolver.Target结构体，该结构体包含三个字段：

```
// github.com/grpc/grpc-go/resolver/resolver.go
type Target struct {
Scheme string
Authority string
Endpoint string
}
```


其中Scheme为”static”，Authority为空，Endpoint为”localhost:50051,localhost:50052,localhost:50053″。

接下来，gRPC会根据Target.Scheme的值到resolver包中的builder map中查找是否有对应的Resolver Builder实例。到目前为止gRPC内置的的resolver Builder都无法匹配该Scheme值。是时候自定义一个StaticResolver的Builder了！

grpc的resolve包定义了一个Builder实例需要实现的接口：

```
// github.com/grpc/grpc-go/resolver/resolver.go
// Builder creates a resolver that will be used to watch name resolution updates.
type Builder interface {
// Build creates a new resolver for the given target.
//
// gRPC dial calls Build synchronously, and fails if the returned error is
// not nil.
Build(target Target, cc ClientConn, opts BuildOptions) (Resolver, error)
// Scheme returns the scheme supported by this resolver.
// Scheme is defined at https://github.com/grpc/grpc/blob/master/doc/naming.md.
Scheme() string
}
```


Scheme方法返回这个Builder对应的scheme，而Build方法则是真正用于构建Resolver实例的方法，我们来看一下StaticBuilder的实现：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo2/greeter_client/builder.go
func init() {
resolver.Register(&StaticBuilder{}) //在init函数中将StaticBuilder实例注册到resolver包的Resolver map中
}
type StaticBuilder struct{}
func (sb *StaticBuilder) Build(target resolver.Target, cc resolver.ClientConn,
opts resolver.BuildOptions) (resolver.Resolver, error) {
// 解析target.Endpoint (例如：localhost:50051,localhost:50052,localhost:50053)
endpoints := strings.Split(target.Endpoint, ",")
r := &StaticResolver{
endpoints: endpoints,
cc: cc,
}
r.ResolveNow(resolver.ResolveNowOptions{})
return r, nil
}
func (sb *StaticBuilder) Scheme() string {
return "static" // 返回StaticBuilder对应的scheme字符串
}
```


在这个StaticBuilder实现中，init函数在包初始化是就将一个StaticBuilder实例注册到resolver包的Resolver map中。这样gRPC在Dial时就能通过target中的scheme找到该builder。Build方法是StaticBuilder的关键，在这个方法中，它首先解析传入的target.Endpoint，得到三个service instance的服务地址并存到新创建的StaticResolver实例中，并调用StaticResolver实例的ResolveNow方法确定即将连接的service instance集合。

和Builder一样，grpc的resolver包也定义了每个resolver需要实现的Resolver接口：

```
// github.com/grpc/grpc-go/resolver/resolver.go
// Resolver watches for the updates on the specified target.
// Updates include address updates and service config updates.
type Resolver interface {
// ResolveNow will be called by gRPC to try to resolve the target name
// again. It's just a hint, resolver can ignore this if it's not necessary.
//
// It could be called multiple times concurrently.
ResolveNow(ResolveNowOptions)
// Close closes the resolver.
Close()
}
```


从这个接口注释我们也能看出，Resolver的实现负责监视(watch)服务测的地址与配置变化，并将变化更新给grpc的ClientConn。我们来看看我们的StaticResolver的实现：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo2/greeter_client/resolver.go
type StaticResolver struct {
endpoints []string
cc resolver.ClientConn
sync.Mutex
}
func (r *StaticResolver) ResolveNow(opts resolver.ResolveNowOptions) {
r.Lock()
r.doResolve()
r.Unlock()
}
func (r *StaticResolver) Close() {
}
func (r *StaticResolver) doResolve() {
var addrs []resolver.Address
for i, addr := range r.endpoints {
addrs = append(addrs, resolver.Address{
Addr: addr,
ServerName: fmt.Sprintf("instance-%d", i+1),
})
}
newState := resolver.State{
Addresses: addrs,
}
r.cc.UpdateState(newState)
}
```


注：resolver.Resolver接口的注释要求ResolveNow方法是要支持并发安全的，所以这里我们通过sync.Mutex来实现同步。


由于服务侧的服务地址数量与信息都是不变的，因此这里并没有watch和update的过程，而只是在实现了ResolveNow(并在Builder中的Build方法中调用），在ResolveNow中将service instance的地址集合更新给ClientConnection(r.cc)。

接下来我们来编译与运行一下demo2的client与server：

```
$cd grpc-client/demo2/greeter_server
$make
$goreman start
22:58:21 demo2-server1 | Starting demo2-server1 on port 5000
22:58:21 demo2-server2 | Starting demo2-server2 on port 5100
22:58:21 demo2-server3 | Starting demo2-server3 on port 5200
$cd grpc-client/demo2/greeter_client
$make
$./demo2-client
```


执行一段时间后，你会在server端的日志中发现一个问题，如下日志所示：

```
22:57:16 demo2-server1 | 2021/09/11 22:57:16 Received: world-1
22:57:18 demo2-server1 | 2021/09/11 22:57:18 Received: world-2
22:57:20 demo2-server1 | 2021/09/11 22:57:20 Received: world-3
22:57:22 demo2-server1 | 2021/09/11 22:57:22 Received: world-4
22:57:24 demo2-server1 | 2021/09/11 22:57:24 Received: world-5
22:57:26 demo2-server1 | 2021/09/11 22:57:26 Received: world-6
22:57:28 demo2-server1 | 2021/09/11 22:57:28 Received: world-7
22:57:30 demo2-server1 | 2021/09/11 22:57:30 Received: world-8
22:57:32 demo2-server1 | 2021/09/11 22:57:32 Received: world-9
```


我们的Service instance集合中明明有三个地址，为何只有server1收到了rpc请求，其他两个server都处于空闲状态呢？这是客户端的负载均衡策略在作祟！默认情况下，grpc会为客户端选择内置的“pick_first”负载均衡策略，即在service instance集合中选择第一个intance进行请求。在这个例子中，在pick_first策略的作用下，grpc总是会选择demo2-server1发起rpc请求。

如果要将请求发到各个server上，我们可以将负载均衡策略改为另外一个内置的策略：round_robin，就像下面代码这样：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo2/greeter_client/main.go
conn, err := grpc.DialContext(ctx, address, grpc.WithInsecure(), grpc.WithBlock(), grpc.WithBalancerName("round_robin"))
```


重新编译运行greeter_client后，在server测我们就可以看到rpc请求被轮询地发到了每个server instance上了。

#### 2) Resolver原理

我们再来用一幅图来梳理一下Builder以及Resolver的工作原理：

![](../../assets/5299ea18b7fca114.png)


图中的SchemeResolver泛指实现了某一特定scheme的resolver。如图所示，service instance集合resolve过程的步骤大致如下：

-
- SchemeBuilder将自身实例注册到resolver包的map中；

-
- grpc.Dial/DialContext时使用特定形式的target参数

-
- 对target解析后，根据target.Scheme到resolver包的map中查找Scheme对应的Buider；

-
- 调用Buider的Build方法

-
- Build方法构建出SchemeResolver实例；

-
- 后续由SchemeResolver实例监视service instance变更状态并在有变更的时候更新ClientConnection。


#### 3) NacosResolver

在生产环境中，考虑到服务的高可用、可伸缩等，我们很少使用固定地址、固定数量的服务实例集合，更多是通过服务注册和发现机制自动实现服务实例集合的更新。这里我们再来实现一个基于[nacos](https://nacos.io/zh-cn/)的NacosResolver，实现服务实例变更时grpc Client的自动调整(注：nacos的本地单节点安装方案见文本附录)，让示例具实战意义^_^。

由于有了上面关于Resolver原理的描述，这里简化了一些描述。

首先和StaticResolver一样，我们也来设计一下target的形式。nacos有namespace, group的概念，因此我们将target设计为如下形式：

```
nacos://[authority]/host:port/namespace/group/serviceName
```


具体到我们的greeter_client中，其address为：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo3/greeter_client/main.go
const (
address = "nacos:///localhost:8848/public/group-a/demo3-service" //no authority
)
```


接下来我们来看NacosBuilder：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo3/greeter_client/builder.go
func (nb *NacosBuilder) Build(target resolver.Target,
cc resolver.ClientConn,
opts resolver.BuildOptions) (resolver.Resolver, error) {
// use info in target to access naming service
// parse the target.endpoint
// target.Endpoint - localhost:8848/public/DEFAULT_GROUP/serviceName, the addr of naming service :nacos endpoint
sl := strings.Split(target.Endpoint, "/")
nacosAddr := sl[0]
namespace := sl[1]
group := sl[2]
serviceName := sl[3]
sl1 := strings.Split(nacosAddr, ":")
host := sl1[0]
port := sl1[1]
namingClient, err := initNamingClient(host, port, namespace, group)
if err != nil {
return nil, err
}
r := &NacosResolver{
namingClient: namingClient,
cc: cc,
namespace: namespace,
group: group,
serviceName: serviceName,
}
// initialize the cc's states
r.ResolveNow(resolver.ResolveNowOptions{})
// subscribe and watch
r.watch()
return r, nil
}
func (nb *NacosBuilder) Scheme() string {
return "nacos"
}
```


NacosBuilder的Build方法流程也StaticBuilder并无二致，首先我们也是解析传入的target的Endpoint，即”localhost:8848/public/group-a/demo3-service”，并将解析后的各段信息存入新创建的NacosResolver实例中备用。NacosResolver还需要一个信息，那就是与nacos的连接，这里用initNamingClient创建一个nacos client端实例(调用[nacos提供的go sdk](https://github.com/nacos-group/nacos-sdk-go))。

接下来我们调用NacosResolver的ResolveNow获取一次nacos上demo3-service的服务实例列表并初始化ClientConn，最后我们调用NacosResolver的watch方法来订阅并监视demo3-service的实例变化。下面是NacosResolver的部分实现：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo3/greeter_client/resolver.go
func (r *NacosResolver) doResolve(opts resolver.ResolveNowOptions) {
instances, err := r.namingClient.SelectAllInstances(vo.SelectAllInstancesParam{
ServiceName: r.serviceName,
GroupName: r.group,
})
if err != nil {
fmt.Println(err)
return
}
if len(instances) == 0 {
fmt.Printf("service %s has zero instance\n", r.serviceName)
return
}
// update cc.States
var addrs []resolver.Address
for i, inst := range instances {
if (!inst.Enable) || (inst.Weight == 0) {
continue
}
addrs = append(addrs, resolver.Address{
Addr: fmt.Sprintf("%s:%d", inst.Ip, inst.Port),
ServerName: fmt.Sprintf("instance-%d", i+1),
})
}
if len(addrs) == 0 {
fmt.Printf("service %s has zero valid instance\n", r.serviceName)
}
newState := resolver.State{
Addresses: addrs,
}
r.Lock()
r.cc.UpdateState(newState)
r.Unlock()
}
func (r *NacosResolver) ResolveNow(opts resolver.ResolveNowOptions) {
r.doResolve(opts)
}
func (r *NacosResolver) Close() {
r.namingClient.Unsubscribe(&vo.SubscribeParam{
ServiceName: r.serviceName,
GroupName: r.group,
})
}
func (r *NacosResolver) watch() {
r.namingClient.Subscribe(&vo.SubscribeParam{
ServiceName: r.serviceName,
GroupName: r.group,
SubscribeCallback: func(services []model.SubscribeService, err error) {
fmt.Printf("subcallback: %#v\n", services)
r.doResolve(resolver.ResolveNowOptions{})
},
})
}
```


这里的一个重要实现是ResolveNow和watch都调用的doResolve方法，该方法通过nacos-go sdk中的SelectAllInstances获取demo-service3的所有实例，并将得到的enabled(=true)和权重(weight)不为0的合法实例集合更新给ClientConn(r.cc.UpdateState)。

在NacosResolver的watch方法中，我们通过nacos-go sdk中的Subscribe方法订阅demo3-service并提供了一个回调函数。这样每当demo3-service的实例发生变化时，该回调会被调用。在该回调中我们可以基于传回的最新的service实例集合（services []model.SubscribeService）来更新ClientConn，但在这里我们复用了doResolve方法，即又去nacos获取一次demo-service3的实例。

编译运行demo3下greeter_server：

```
$cd grpc-client/demo3/greeter_server
$make
$goreman start
06:06:02 demo3-server3 | Starting demo3-server3 on port 5200
06:06:02 demo3-server1 | Starting demo3-server1 on port 5000
06:06:02 demo3-server2 | Starting demo3-server2 on port 5100
06:06:02 demo3-server3 | 2021-09-12T06:06:02.913+0800 INFO nacos_client/nacos_client.go:87 logDir:</tmp/nacos/log/50053> cacheDir:</tmp/nacos/cache/50053>
06:06:02 demo3-server2 | 2021-09-12T06:06:02.913+0800 INFO nacos_client/nacos_client.go:87 logDir:</tmp/nacos/log/50052> cacheDir:</tmp/nacos/cache/50052>
06:06:02 demo3-server1 | 2021-09-12T06:06:02.913+0800 INFO nacos_client/nacos_client.go:87 logDir:</tmp/nacos/log/50051> cacheDir:</tmp/nacos/cache/50051>
```


运行greeter_server后，我们在nacos dashboard上会看到demo-service3的所有实例信息：

![](../../assets/0eb78cb0bed70423.png)


![](../../assets/8575501e722314b4.png)


编译运行demo3下greeter_client：

```
$cd grpc-client/demo3/greeter_client
$make
$./demo3-client
2021-09-12T06:08:25.551+0800 INFO nacos_client/nacos_client.go:87 logDir:</Users/tonybai/go/src/github.com/bigwhite/experiments/grpc-client/demo3/greeter_client/log> cacheDir:</Users/tonybai/go/src/github.com/bigwhite/experiments/grpc-client/demo3/greeter_client/cache>
2021/09/12 06:08:25 Greeting: Hello world-1
2021/09/12 06:08:27 Greeting: Hello world-2
2021/09/12 06:08:29 Greeting: Hello world-3
2021/09/12 06:08:31 Greeting: Hello world-4
2021/09/12 06:08:33 Greeting: Hello world-5
2021/09/12 06:08:35 Greeting: Hello world-6
... ...
```


由于采用了round robin负载策略，greeter_server侧每个server(权重都为1)都会平等的收到rpc请求：

```
06:06:36 demo3-server1 | 2021/09/12 06:06:36 Received: world-1
06:06:38 demo3-server3 | 2021/09/12 06:06:38 Received: world-2
06:06:40 demo3-server2 | 2021/09/12 06:06:40 Received: world-3
06:06:42 demo3-server1 | 2021/09/12 06:06:42 Received: world-4
06:06:44 demo3-server3 | 2021/09/12 06:06:44 Received: world-5
06:06:46 demo3-server2 | 2021/09/12 06:06:46 Received: world-6
... ...
```


这时我们可以通过nacos dashboard调整demo3-service的实例权重或下线某个实例，比如下线service instance-2(端口50052)，之后我们会看到greeter_client回调函数执行，之后greeter_server侧将只有实例1和实例3收到rpc请求。重新上线service instance-2后，一切会恢复正常。

### 3. 自定义客户端balancer

现实中服务端的实例所部署的主机(虚拟机/容器)算力可能不同，如果所有实例都使用相同权重1，那么肯定是不科学且存在算力浪费。但grpc-go内置的balancer实现有限，不能满足我们需求，我们就需要自定义一个可以满足我们需求的balancer了。

这里我们以自定义一个Weighted Round Robin(wrr) Balancer为例，看看自定义balancer的步骤（我们参考grpc-go中内置[round_robin的实现](https://github.com/grpc/grpc-go/tree/master/balancer/roundrobin)）。

和resolver包相似，balancer也是通过一个Builder(创建模式)来实例化的，并且balancer的Balancer接口与resolver.Balancer差不多：

```
// github.com/grpc/grpc-go/balancer/balancer.go
// Builder creates a balancer.
type Builder interface {
// Build creates a new balancer with the ClientConn.
Build(cc ClientConn, opts BuildOptions) Balancer
// Name returns the name of balancers built by this builder.
// It will be used to pick balancers (for example in service config).
Name() string
}
```


通过Builder.Build方法我们构建一个Balancer接口的实现，Balancer接口定义如下：

```
// github.com/grpc/grpc-go/balancer/balancer.go
type Balancer interface {
// UpdateClientConnState is called by gRPC when the state of the ClientConn
// changes. If the error returned is ErrBadResolverState, the ClientConn
// will begin calling ResolveNow on the active name resolver with
// exponential backoff until a subsequent call to UpdateClientConnState
// returns a nil error. Any other errors are currently ignored.
UpdateClientConnState(ClientConnState) error
// ResolverError is called by gRPC when the name resolver reports an error.
ResolverError(error)
// UpdateSubConnState is called by gRPC when the state of a SubConn
// changes.
UpdateSubConnState(SubConn, SubConnState)
// Close closes the balancer. The balancer is not required to call
// ClientConn.RemoveSubConn for its existing SubConns.
Close()
}
```


可以看到，Balancer要比Resolver要复杂很多。gRPC的核心开发者们也看到了这一点，于是他们提供了一个可简化自定义Balancer创建的包：google.golang.org/grpc/balancer/base。gRPC内置的round_robin Balancer也是基于base包实现的。

base包提供了NewBalancerBuilder可以快速返回一个balancer.Builder的实现：

```
// github.com/grpc/grpc-go/balancer/base/base.go
// NewBalancerBuilder returns a base balancer builder configured by the provided config.
func NewBalancerBuilder(name string, pb PickerBuilder, config Config) balancer.Builder {
return &baseBuilder{
name: name,
pickerBuilder: pb,
config: config,
}
}
```


我们看到，这个函数接收一个参数：pb，它的类型是PikcerBuilder，这个接口类型则比较简单：

```
// github.com/grpc/grpc-go/balancer/base/base.go
// PickerBuilder creates balancer.Picker.
type PickerBuilder interface {
// Build returns a picker that will be used by gRPC to pick a SubConn.
Build(info PickerBuildInfo) balancer.Picker
}
```


我们仅需要提供一个PickerBuilder的实现以及一个balancer.Picker的实现即可，而Picker则是仅有一个方法的接口类型：

```
// github.com/grpc/grpc-go/balancer/balancer.go
type Picker interface {
Pick(info PickInfo) (PickResult, error)
}
```


嵌套的有些多，我们用下面这幅图来直观看一下balancer的创建和使用流程：

![](../../assets/3c7aa622c2741849.png)


再简述一下大致流程：

- 首先要注册一个名为”my_weighted_round_robin”的balancer Builder:wrrBuilder，该Builder由base包的NewBalancerBuilder构建；
- base包的NewBalancerBuilder函数需要传入一个PickerBuilder实现，于是我们需要自定义一个返回Picker接口实现的PickerBuilder。
- grpc.Dial调用时传入一个WithBalancerName(“my_weighted_round_robin”)，grpc通过balancer Name从已注册的balancer builder中选出我们实现的wrrBuilder，并调用wrrBuilder创建Picker：wrrPicker。
- 在grpc实施rpc调用SayHello时，wrrPicker的Pick方法会被调用，选出一个Connection，并在该connection上发送rpc请求。

由于用到的权重值，我们的resolver实现需要做一些变动，主要是在doResolve方法时将service instance的权重(weight)通过Attribute设置到ClientConnection中：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo4/greeter_client/resolver.go
func (r *NacosResolver) doResolve(opts resolver.ResolveNowOptions) {
instances, err := r.namingClient.SelectAllInstances(vo.SelectAllInstancesParam{
ServiceName: r.serviceName,
GroupName: r.group,
})
if err != nil {
fmt.Println(err)
return
}
if len(instances) == 0 {
fmt.Printf("service %s has zero instance\n", r.serviceName)
return
}
// update cc.States
var addrs []resolver.Address
for i, inst := range instances {
if (!inst.Enable) || (inst.Weight == 0) {
continue
}
addr := resolver.Address{
Addr: fmt.Sprintf("%s:%d", inst.Ip, inst.Port),
ServerName: fmt.Sprintf("instance-%d", i+1),
}
addr.Attributes = addr.Attributes.WithValues("weight", int(inst.Weight)) //考虑权重并纳入cc的状态中
addrs = append(addrs, addr)
}
if len(addrs) == 0 {
fmt.Printf("service %s has zero valid instance\n", r.serviceName)
}
newState := resolver.State{
Addresses: addrs,
}
r.Lock()
r.cc.UpdateState(newState)
r.Unlock()
}
```


接下来我们重点看看greeter_client中wrrPickerBuilder与wrrPicker的实现：

```
// https://github.com/bigwhite/experiments/tree/master/grpc-client/demo4/greeter_client/balancer.go
type wrrPickerBuilder struct{}
func (*wrrPickerBuilder) Build(info base.PickerBuildInfo) balancer.Picker {
if len(info.ReadySCs) == 0 {
return base.NewErrPicker(balancer.ErrNoSubConnAvailable)
}
var scs []balancer.SubConn
// 提取已经就绪的connection的权重信息，作为Picker实例的输入
for subConn, addr := range info.ReadySCs {
weight := addr.Address.Attributes.Value("weight").(int)
if weight <= 0 {
weight = 1
}
for i := 0; i < weight; i++ {
scs = append(scs, subConn)
}
}
return &wrrPicker{
subConns: scs,
// Start at a random index, as the same RR balancer rebuilds a new
// picker when SubConn states change, and we don't want to apply excess
// load to the first server in the list.
next: rand.Intn(len(scs)),
}
}
type wrrPicker struct {
// subConns is the snapshot of the roundrobin balancer when this picker was
// created. The slice is immutable. Each Get() will do a round robin
// selection from it and return the selected SubConn.
subConns []balancer.SubConn
mu sync.Mutex
next int
}
// 选出一个Connection
func (p *wrrPicker) Pick(info balancer.PickInfo) (balancer.PickResult, error) {
p.mu.Lock()
sc := p.subConns[p.next]
p.next = (p.next + 1) % len(p.subConns)
p.mu.Unlock()
return balancer.PickResult{SubConn: sc}, nil
}
```


这是一个简单的Weighted Round Robin实现，加权算法十分简单，如果一个conn的权重为n，那么就在加权结果集中加入n个conn，这样在后续Pick时不需要考虑加权的问题，只需向普通Round Robin那样逐个Pick出来即可。

运行demo4 greeter_server后，我们在nacos将instance-1的权重改为5，我们后续就会看到如下输出：

```
$goreman start
09:20:18 demo4-server3 | Starting demo4-server3 on port 5200
09:20:18 demo4-server2 | Starting demo4-server2 on port 5100
09:20:18 demo4-server1 | Starting demo4-server1 on port 5000
09:20:18 demo4-server2 | 2021-09-12T09:20:18.633+0800 INFO nacos_client/nacos_client.go:87 logDir:</tmp/nacos/log/50052> cacheDir:</tmp/nacos/cache/50052>
09:20:18 demo4-server1 | 2021-09-12T09:20:18.633+0800 INFO nacos_client/nacos_client.go:87 logDir:</tmp/nacos/log/50051> cacheDir:</tmp/nacos/cache/50051>
09:20:18 demo4-server3 | 2021-09-12T09:20:18.633+0800 INFO nacos_client/nacos_client.go:87 logDir:</tmp/nacos/log/50053> cacheDir:</tmp/nacos/cache/50053>
09:20:23 demo4-server2 | 2021/09/12 09:20:23 Received: world-1
09:20:25 demo4-server3 | 2021/09/12 09:20:25 Received: world-2
09:20:27 demo4-server1 | 2021/09/12 09:20:27 Received: world-3
09:20:29 demo4-server2 | 2021/09/12 09:20:29 Received: world-4
09:20:31 demo4-server3 | 2021/09/12 09:20:31 Received: world-5
09:20:33 demo4-server1 | 2021/09/12 09:20:33 Received: world-6
09:20:35 demo4-server2 | 2021/09/12 09:20:35 Received: world-7
09:20:37 demo4-server3 | 2021/09/12 09:20:37 Received: world-8
09:20:39 demo4-server1 | 2021/09/12 09:20:39 Received: world-9
09:20:41 demo4-server2 | 2021/09/12 09:20:41 Received: world-10
09:20:43 demo4-server1 | 2021/09/12 09:20:43 Received: world-11
09:20:45 demo4-server2 | 2021/09/12 09:20:45 Received: world-12
09:20:47 demo4-server3 | 2021/09/12 09:20:47 Received: world-13
//这里将权重改为5后
09:20:49 demo4-server1 | 2021/09/12 09:20:49 Received: world-14
09:20:51 demo4-server1 | 2021/09/12 09:20:51 Received: world-15
09:20:53 demo4-server1 | 2021/09/12 09:20:53 Received: world-16
09:20:55 demo4-server1 | 2021/09/12 09:20:55 Received: world-17
09:20:57 demo4-server1 | 2021/09/12 09:20:57 Received: world-18
09:20:59 demo4-server2 | 2021/09/12 09:20:59 Received: world-19
09:21:01 demo4-server3 | 2021/09/12 09:21:01 Received: world-20
09:21:03 demo4-server1 | 2021/09/12 09:21:03 Received: world-21
```


注意：每次nacos的service instance发生变化后，balancer都会重新build一个新Picker实例，后续会使用新Picker实例在其Connection集合中Pick出一个conn。

### 4. 小结

在本文中我们了解了gRPC的四种通信模式。我们重点关注了在最常用的simple RPC(unary RPC)模式下gRPC Client侧需要考虑的事情，包括：

- 如何实现一个helloworld的一对一的通信
- 如何实现一个自定义的Resolver以实现一个client到一个静态服务实例集合的通信
- 如何实现一个自定义的Resolver以实现一个client到一个动态服务实例集合的通信
- 如何自定义客户端Balancer

本文代码仅做示例使用，并未考虑太多异常处理。

本文涉及的所有代码可以从[这里下载](https://github.com/bigwhite/experiments/tree/master/grpc-client)：https://github.com/bigwhite/experiments/tree/master/grpc-client

### 5. 参考资料

- gRPC Name Resolution – https://github.com/grpc/grpc/blob/master/doc/naming.md
- Load Balancing in gRPC – https://github.com/grpc/grpc/blob/master/doc/load-balancing.md
- 基于 gRPC的服务发现与负载均衡（基础篇）- https://pandaychen.github.io/2019/07/11/GRPC-SERVICE-DISCOVERY/
- 比较 gRPC服务和HTTP API – https://docs.microsoft.com/zh-cn/aspnet/core/grpc/comparison

### 6. 附录

#### 1) json vs. protobuf编解码性能基准测试结果

测试源码位于[这里](https://github.com/bigwhite/experiments/tree/master/grpc-client/grpc-vs-httpjson/codec)：https://github.com/bigwhite/experiments/tree/master/grpc-client/grpc-vs-httpjson/codec

我们使用了Go标准库json编解码、字节开源的[sonic json编解码包](https://github.com/bytedance/sonic)以及[minio](https://tonybai.com/2020/03/16/build-high-performance-object-storage-with-minio-part1-prototype/)开源的[simdjson-go](https://github.com/minio/simdjson-go)高性能json解析库与protobuf作对比的结果如下：

```
$go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/codec
cpu: Intel(R) Core(TM) i5-8257U CPU @ 1.40GHz
BenchmarkSimdJsonUnmarshal-8 43304 28177 ns/op 113209 B/op 19 allocs/op
BenchmarkJsonUnmarshal-8 153214 7187 ns/op 1024 B/op 6 allocs/op
BenchmarkJsonMarshal-8 601590 2057 ns/op 2688 B/op 2 allocs/op
BenchmarkSonicJsonUnmarshal-8 1394211 861.1 ns/op 2342 B/op 2 allocs/op
BenchmarkSonicJsonMarshal-8 1592898 765.2 ns/op 2239 B/op 4 allocs/op
BenchmarkProtobufUnmarshal-8 3823441 317.0 ns/op 1208 B/op 3 allocs/op
BenchmarkProtobufMarshal-8 4461583 274.8 ns/op 1152 B/op 1 allocs/op
PASS
ok github.com/bigwhite/codec 10.901s
```


benchmark测试结果印证了protobuf的编解码性能要远高于json编解码。但是在benchmark结果中，一个结果让我很意外，那就是号称高性能的simdjson-go的数据难看到离谱。谁知道为什么吗？simd指令没生效？字节开源的sonic的确性能很好，与pb也就2-3倍的差距，没有数量级的差距。

#### 2) gRPC(insecure) vs. json over http

测试源码位于[这里](https://github.com/bigwhite/experiments/tree/master/grpc-client/grpc-vs-httpjson/protocol)：https://github.com/bigwhite/experiments/tree/master/grpc-client/grpc-vs-httpjson/protocol

使用ghz对gRPC实现的server进行压测结果如下：

```
$ghz --insecure -n 100000 -c 500 --proto publish.proto --call proto.PublishService.Publish -D data.json localhost:10000
Summary:
Count: 100000
Total: 1.67 s
Slowest: 48.49 ms
Fastest: 0.13 ms
Average: 6.34 ms
Requests/sec: 59924.34
Response time histogram:
0.133 [1] |
4.968 [40143] |∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
9.803 [47335] |∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
14.639 [11306] |∎∎∎∎∎∎∎∎∎∎
19.474 [510] |
24.309 [84] |
29.144 [89] |
33.980 [29] |
38.815 [3] |
43.650 [8] |
48.485 [492] |
Latency distribution:
10 % in 3.07 ms
25 % in 4.12 ms
50 % in 5.49 ms
75 % in 7.94 ms
90 % in 10.24 ms
95 % in 11.28 ms
99 % in 15.52 ms
Status code distribution:
[OK] 100000 responses
```


使用hey对使用[fasthttp](https://tonybai.com/2021/04/25/server-side-performance-nethttp-vs-fasthttp)与sonic实现的http server进行压测结果如下：

```
$hey -n 100000 -c 500 -m POST -D ./data.json http://127.0.0.1:10001/
Summary:
Total: 2.0012 secs
Slowest: 0.1028 secs
Fastest: 0.0001 secs
Average: 0.0038 secs
Requests/sec: 49969.9234
Response time histogram:
0.000 [1] |
0.010 [96287] |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
0.021 [2639] |■
0.031 [261] |
0.041 [136] |
0.051 [146] |
0.062 [128] |
0.072 [43] |
0.082 [24] |
0.093 [10] |
0.103 [4] |
Latency distribution:
10% in 0.0013 secs
25% in 0.0020 secs
50% in 0.0031 secs
75% in 0.0040 secs
90% in 0.0062 secs
95% in 0.0089 secs
99% in 0.0179 secs
Details (average, fastest, slowest):
DNS+dialup: 0.0000 secs, 0.0001 secs, 0.1028 secs
DNS-lookup: 0.0000 secs, 0.0000 secs, 0.0000 secs
req write: 0.0000 secs, 0.0000 secs, 0.0202 secs
resp wait: 0.0031 secs, 0.0000 secs, 0.0972 secs
resp read: 0.0005 secs, 0.0000 secs, 0.0575 secs
Status code distribution:
[200] 99679 responses
```


我们看到：gRPC的性能（Requests/sec: 59924.34）要比http api性能(Requests/sec: 49969.9234)高出20%。

#### 3) nacos docker安装

单机容器版nacos安装步骤如下：

```
$git clone https://github.com/nacos-group/nacos-docker.git
$cd nacos-docker
$docker-compose -f example/standalone-derby.yaml up
```


nacos相关容器启动成功后，可以打开浏览器访问http://localhost:8848/nacos，打开nacos仪表盘登录页面，输入nacos/nacos即可进入nacos web操作界面。

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