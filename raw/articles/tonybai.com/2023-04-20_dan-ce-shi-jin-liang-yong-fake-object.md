---
title: 单测时尽量用fake object
url: https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators/
published: '2023-04-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 单测时尽量用fake object

[本文永久链接](https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators) – https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators

![](../../assets/17de71f316084c28.png)


## 1. 单元测试的难点：外部协作者(external collaborators)的存在

单元测试是软件开发的一个重要部分，它有助于在开发周期的早期发现错误，帮助开发人员增加对生产代码正常工作的信心，同时也有助于改善代码设计。**Go语言从诞生那天起就内置Testing框架(以及测试覆盖率计算工具)**，基于该框架，Gopher们可以非常方便地为自己设计实现的package编写测试代码。

注：

[《Go语言精进之路》vol2]中的第40条到第44条有关于Go包内、包外测试区别、测试代码组织、表驱动测试、管理外部测试数据等内容的系统地讲解，感兴趣的童鞋可以读读。

不过即便如此，在实际开发工作中，大家发现单元测试的覆盖率依旧很低，究其原因，排除那些对测试代码不作要求的组织，剩下的无非就是代码设计不佳，使得代码不易测；或是代码有外部协作者（比如数据库、redis、其他服务等）。代码不易测可以通过重构来改善，但如果代码有外部协作者，我们该如何对代码进行测试呢，这也是**各种编程语言实施单元测试的一大共同难点**。

为此，[《xUnit Test Patterns : Refactoring Test Code》](https://book.douban.com/subject/1859393/)一书中提供了**Test Double(测试替身)**的概念专为解决此难题。那么什么是Test Double呢？我们接下来就来简单介绍一下Test Double的概念以及常见的种类。

## 2. 什么是Test Double？

测试替身是在测试阶段用来替代被测系统依赖的真实组件的对象或程序(如下图)，以方便测试，这些真实组件或程序即是外部协作者(external collaborators)。这些外部协作者在测试环境下通常很难获取或与之交互。测试替身可以使开发人员或QA专业人员专注于新的代码而不是代码与环境集成。

![](../../assets/35c2e6f7fe678c3c.png)


测试替身是通用术语，指的是不同类型的替换对象或程序。目前[xUnit Patterns](http://xunitpatterns.com/Test%20Double%20Patterns.html)至少定义了五种类型的Test Doubles：

- Test stubs
- Mock objects
- Test spies
- Fake objects
- Dummy objects

这其中最为常用的是Fake objects、stub和mock objects。下面逐一说说这三种test double：

### 2.1 fake object

fake object最容易理解，它是被测系统SUT(System Under Test)依赖的外部协作者的“替身”，和真实的外部协作者相比，fake object外部行为表现与真实组件几乎是一致的，但更简单也更易于使用，实现更轻量，仅用于满足测试需求即可。

fake object也是Go testing中最为常用的一类fake object。以Go的标准库为例，我们在src/database/sql下面就看到了Go标准库为进行sql包测试而实现的一个database driver：

```
// $GOROOT/src/database/fakedb_test.go
var fdriver driver.Driver = &fakeDriver{}
func init() {
Register("test", fdriver)
}
```


我们知道一个真实的sql数据库的代码量可是数以百万计的，这里不可能实现一个生产级的真实SQL数据库，从fakedb_test.go源文件的注释我们也可以看到，这个fakeDriver仅仅是用于testing，它是一个实现了driver.Driver接口的、支持少数几个DDL(create)、DML(insert)和DQL(selet)的toy版的纯内存数据库：

```
// fakeDriver is a fake database that implements Go's driver.Driver
// interface, just for testing.
//
// It speaks a query language that's semantically similar to but
// syntactically different and simpler than SQL. The syntax is as
// follows:
//
// WIPE
// CREATE|<tablename>|<col>=<type>,<col>=<type>,...
// where types are: "string", [u]int{8,16,32,64}, "bool"
// INSERT|<tablename>|col=val,col2=val2,col3=?
// SELECT|<tablename>|projectcol1,projectcol2|filtercol=?,filtercol2=?
// SELECT|<tablename>|projectcol1,projectcol2|filtercol=?param1,filtercol2=?param2
```


与此类似的，Go标准库中还有net/dnsclient_unix_test.go中的fakeDNSServer等。此外，Go标准库中一些以mock做前缀命名的变量、类型等其实质上是fake object。

我们再来看第二种test double: stub。

### 2.2 stub

stub显然也是一个在测试阶段专用的、用来替代真实外部协作者与SUT进行交互的对象。与fake object稍有不同的是，stub是一个内置了预期值/响应值且可以在多个测试间复用的替身object。

stub可以理解为一种fake object的特例。

注：fakeDriver在sql_test.go中的不同测试场景中时而是fake object，时而是stub(见sql_test.go中的newTestDBConnector函数)。


Go标准库中的net/http/httptest就是一个提供创建stub的典型的测试辅助包，十分适合对http.Handler进行测试，这样我们无需真正启动一个http server。下面就是基于httptest的一个测试例子：

```
// 被测对象 client.go
package main
import (
"bytes"
"net/http"
)
// Function that uses the client to make a request and parse the response
func GetResponse(client *http.Client, url string) (string, error) {
req, err := http.NewRequest("GET", url, nil)
if err != nil {
return "", err
}
resp, err := client.Do(req)
if err != nil {
return "", err
}
defer resp.Body.Close()
buf := new(bytes.Buffer)
_, err = buf.ReadFrom(resp.Body)
if err != nil {
return "", err
}
return buf.String(), nil
}
// 测试代码 client_test.go
package main
import (
"net/http"
"net/http/httptest"
"testing"
)
func TestClient(t *testing.T) {
// Create a new test server with a handler that returns a specific response
server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
w.WriteHeader(http.StatusOK)
w.Write([]byte(`{"message": "Hello, world!"}`))
}))
defer server.Close()
// Create a new client that uses the test server
client := server.Client()
// Call the function that uses the client
message, err := GetResponse(client, server.URL)
// Check that the response is correct
expected := `{"message": "Hello, world!"}`
if message != expected {
t.Errorf("Expected response %q, but got %q", expected, message)
}
// Check that no errors were returned
if err != nil {
t.Errorf("Unexpected error: %v", err)
}
}
```


在这个例子中，我们要测试一个名为GetResponse的函数，该函数通过client向url发送Get请求，并将收到的响应内容读取出来并返回。为了测试这个函数，我们需要“建立”一个与GetResponse进行协作的外部http server，这里我们使用的就是httptest包。我们通过httptest.NewServer建立这个server，该server预置了一个返回特定响应的HTTP handler。我们通过该server得到client和对应的url参数后，将其传给被测目标GetResponse，并将其返回的结果与预期作比较来完成这个测试。注意，我们在测试结束后使用defer server.Close()来关闭测试服务器，以确保该服务器不会在测试结束后继续运行。

httptest还常用来做http.Handler的测试，比如下面这个例子：

```
// handler.go
package main
import (
"bytes"
"io"
"net/http"
)
func AddHelloPrefix(w http.ResponseWriter, r *http.Request) {
b, err := io.ReadAll(r.Body)
if err != nil {
w.WriteHeader(http.StatusBadRequest)
return
}
w.Write(bytes.Join([][]byte{[]byte("hello, "), b}, nil))
w.WriteHeader(http.StatusOK)
}
// handler_test.go
package main
import (
"net/http"
"net/http/httptest"
"strings"
"testing"
)
func TestHandler(t *testing.T) {
r := strings.NewReader("world!")
req, err := http.NewRequest("GET", "/test", r)
if err != nil {
t.Fatal(err)
}
rr := httptest.NewRecorder()
handler := http.HandlerFunc(AddHelloPrefix)
handler.ServeHTTP(rr, req)
if status := rr.Code; status != http.StatusOK {
t.Errorf("handler returned wrong status code: got %v want %v",
status, http.StatusOK)
}
expected := "hello, world!"
if rr.Body.String() != expected {
t.Errorf("handler returned unexpected body: got %v want %v",
rr.Body.String(), expected)
}
}
```


在这个例子中，我们创建一个新的http.Request对象，用于向/test路径发出GET请求。然后我们创建一个新的httptest.ResponseRecorder对象来捕获服务器的响应。 我们定义一个简单的HTTP Handler(被测函数): AddHelloPrefix，该Handler会在请求的内容之前加上”hello, “并返回200 OK状态代码作为响应体。之后，我们在handler上调用ServeHTTP方法，传入httptest.ResponseRecorder和http.Request对象，这会将请求“发送”到处理程序并捕获响应。最后，我们使用标准的Go测试包来检查响应是否具有预期的状态码和正文。

在这个例子中，我们利用net/http/httptest创建了一个测试服务器“替身”，并向其“发送”间接预置信息的请求以测试Go中的HTTP handler。这个过程中其实并没有任何网络通信，也没有http协议打包和解包的过程，我们也不关心http通信，那是Go net/http包的事情，我们只care我们的Handler是否能按逻辑运行。

fake object与stub的优缺点基本一样。多数情况下，**大家也无需将这二者划分的很清晰**。

### 2.3 mock object

和fake/stub一样，mock object也是一个测试替身。通过上面的例子我们看到fake建立困难(比如创建一个近2千行代码的fakeDriver)，但使用简单。而mock object则是一种建立简单，使用简单程度因被测目标与外部协作者交互复杂程度而异的test double，我们看一下下面这个例子：

```
// db.go 被测目标
package main
// Define the `Database` interface
type Database interface {
Save(data string) error
Get(id int) (string, error)
}
// Example functions that use the `Database` interface
func saveData(db Database, data string) error {
return db.Save(data)
}
func getData(db Database, id int) (string, error) {
return db.Get(id)
}
// 测试代码
package main
import (
"testing"
"github.com/stretchr/testify/assert"
"github.com/stretchr/testify/mock"
)
// Define a mock struct that implements the `Database` interface
type MockDatabase struct {
mock.Mock
}
func (m *MockDatabase) Save(data string) error {
args := m.Called(data)
return args.Error(0)
}
func (m *MockDatabase) Get(id int) (string, error) {
args := m.Called(id)
return args.String(0), args.Error(1)
}
func TestSaveData(t *testing.T) {
// Create a new mock database
db := new(MockDatabase)
// Expect the `Save` method to be called with "test data"
db.On("Save", "test data").Return(nil)
// Call the code that uses the database
err := saveData(db, "test data")
// Assert that the `Save` method was called with the correct argument
db.AssertCalled(t, "Save", "test data")
// Assert that no errors were returned
assert.NoError(t, err)
}
func TestGetData(t *testing.T) {
// Create a new mock database
db := new(MockDatabase)
// Expect the `Get` method to be called with ID 123 and return "test data"
db.On("Get", 123).Return("test data", nil)
// Call the code that uses the database
data, err := getData(db, 123)
// Assert that the `Get` method was called with the correct argument
db.AssertCalled(t, "Get", 123)
// Assert that the correct data was returned
assert.Equal(t, "test data", data)
// Assert that no errors were returned
assert.NoError(t, err)
}
```


在这个例子中，被测目标是两个接受Database接口类型参数的函数：saveData和getData。显然在单元测试阶段，我们不能真正为这两个函数传入真实的Database实例去测试。

这里，我们没有使用fake object，而是定义了一个mock object：MockDatabase，该类型实现了Database接口。然后我们定义了两个测试函数，TestSaveData和TestGetData，它们分别使用MockDatabase实例来测试saveData和getData函数。

在每个测试函数中，我们对MockDatabase实例进行设置，包括期待特定参数的方法调用，然后调用使用该数据库的代码(即被测目标函数saveData和getData)。然后我们使用github.com/stretchr/testify中的assert包，对代码的预期行为进行断言。

注：除了上述测试中使用的AssertCalled方法外，MockDatabase结构还提供了其他方法来断言方法被调用的次数、方法被调用的顺序等。请查看github.com/stretchr/testify/mock包的文档，了解更多信息。


## 3. Test Double有多种，选哪个呢？

从mock object的例子来看，测试代码的核心就是mock object的构建与mock object的方法的参数和返回结果的设置，相较于fake object的简单直接，mock object在使用上较为难于理解。而且对Go语言来说，mock object要与接口类型联合使用，如果被测目标的参数是非接口类型，mock object便“无从下嘴”了。此外，mock object使用难易程度与被测目标与外部协作者的交互复杂度相关。像上面这个例子，建立mock object就比较简单。但对于一些复杂的函数，当存在多个外部协作者且与每个协作者都有多次交互的情况下，建立和设置mock object就将变得困难并更加难于理解。

mock object仅是满足了被测目标对依赖的外部协作者的调用需求，比如设置不同参数传入下的不同返回值，但mock object并未真实处理被测目标传入的参数，这会降低测试的可信度以及开发人员对代码正确性的信心。

此外，如果被测函数的输入输出未发生变化，但内部逻辑发生了变化，比如调用的外部协作者的方法参数、调用次数等，使用mock object的测试代码也需要一并更新维护。

而通过上面的fakeDriver、fakeDNSSever以及httptest应用的例子，我们看到：作为test double，fake object/stub有如下优点：

- 我们与fake object的交互方式与与真实外部协作者交互的方式相同，这让其显得更简单，更容易使用，也降低了测试的复杂性；
- fake objet的行为更像真正的协作者，可以给开发人员更多的信心；
- 当真实协作者更新时，我们不需要更新使用fake object时设置的expection和结果验证条件，因此，使用fake object时，重构代码往往比使用其他test double更容易。

不过fake object也有自己的不足之处，比如：

- fake object的创建和维护可能很费时，就像上面的fakeDriver，源码有近2k行；
- fake object可能无法提供与真实组件相同的功能覆盖水平，这与fake object的提供方式有关。
- fake object的实现需要维护，每当真正的协作者更新时，都必须更新fake object。

综上，测试的主要意义是保证SUT代码的正确性，让开发人员对自己编写的代码更有信心，从这个角度来看，我们**在单测时应首选为外部协作者提供fake object以满足测试需要**。

### 4. fake object的实现和获取方法

随着技术的进步，fake object的实现和获取日益容易。

我们可以借助类似ChatGPT/copilot的工具快速构建出一个fake object，即便是几百行代码的fake object的实现也很容易。

如果要更高的可信度和更高的功能覆盖水平，我们还可以借助docker来构建“真实版/无阉割版”的fake object。

借助github上开源的[testcontainers-go](https://golang.testcontainers.org/)可以更为简便的构建出一个fake object，并且testcontainer提供了常见的外部协作者的封装实现，比如：MySQL、Redis、Postgres等。

以测试redis client为例，我们使用testcontainer建立如下测试代码：

```
// redis_test.go
package main
import (
"context"
"fmt"
"testing"
"github.com/go-redis/redis/v8"
"github.com/testcontainers/testcontainers-go"
"github.com/testcontainers/testcontainers-go/wait"
)
func TestRedisClient(t *testing.T) {
// Create a Redis container with a random port and wait for it to start
req := testcontainers.ContainerRequest{
Image: "redis:latest",
ExposedPorts: []string{"6379/tcp"},
WaitingFor: wait.ForLog("Ready to accept connections"),
}
ctx := context.Background()
redisC, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
ContainerRequest: req,
Started: true,
})
if err != nil {
t.Fatalf("Failed to start Redis container: %v", err)
}
defer redisC.Terminate(ctx)
// Get the Redis container's host and port
redisHost, err := redisC.Host(ctx)
if err != nil {
t.Fatalf("Failed to get Redis container's host: %v", err)
}
redisPort, err := redisC.MappedPort(ctx, "6379/tcp")
if err != nil {
t.Fatalf("Failed to get Redis container's port: %v", err)
}
// Create a Redis client and perform some operations
client := redis.NewClient(&redis.Options{
Addr: fmt.Sprintf("%s:%s", redisHost, redisPort.Port()),
})
defer client.Close()
err = client.Set(ctx, "key", "value", 0).Err()
if err != nil {
t.Fatalf("Failed to set key: %v", err)
}
val, err := client.Get(ctx, "key").Result()
if err != nil {
t.Fatalf("Failed to get key: %v", err)
}
if val != "value" {
t.Errorf("Expected value %q, but got %q", "value", val)
}
}
```


运行该测试将看到类似如下结果：

```
$go test
2023/04/15 16:18:20 github.com/testcontainers/testcontainers-go - Connected to docker:
Server Version: 20.10.8
API Version: 1.41
Operating System: Ubuntu 20.04.3 LTS
Total Memory: 10632 MB
2023/04/15 16:18:21 Failed to get image auth for docker.io. Setting empty credentials for the image: docker.io/testcontainers/ryuk:0.3.4. Error is:credentials not found in native keychain
2023/04/15 16:19:06 Starting container id: 0d8341b2270e image: docker.io/testcontainers/ryuk:0.3.4
2023/04/15 16:19:10 Waiting for container id 0d8341b2270e image: docker.io/testcontainers/ryuk:0.3.4
2023/04/15 16:19:10 Container is ready id: 0d8341b2270e image: docker.io/testcontainers/ryuk:0.3.4
2023/04/15 16:19:28 Starting container id: 999cf02b5a82 image: redis:latest
2023/04/15 16:19:30 Waiting for container id 999cf02b5a82 image: redis:latest
2023/04/15 16:19:30 Container is ready id: 999cf02b5a82 image: redis:latest
PASS
ok demo 73.262s
```


我们看到建立这种真实版的“fake object”的一大不足就是依赖网络下载container image且耗时过长，在单元测试阶段使用还是要谨慎一些。testcontainer更多也会被用在集成测试或冒烟测试上。

一些开源项目，比如etcd，也提供了[用于测试的自身简化版的实现(embed)](https://github.com/etcd-io/etcd/blob/main/tests/integration/embed)。这一点也值得我们效仿，在团队内部每个服务的开发者如果都能提供一个服务的简化版实现，那么对于该服务调用者来说，它的单测就会变得十分容易。

## 5. 参考资料

- 《xUnit Test Patterns : Refactoring Test Code》- https://book.douban.com/subject/1859393/
- Test Double Patterns – http://xunitpatterns.com/Test%20Double%20Patterns.html
- The Unit in Unit Testing – https://www.infoq.com/articles/unit-testing-approach/
- Test Doubles — Fakes, Mocks and Stubs – https://blog.pragmatists.com/test-doubles-fakes-mocks-and-stubs-1a7491dfa3da

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

No related posts.

## 评论