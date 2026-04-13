---
title: 深入GOCACHEPROG：Go构建缓存的自定义扩展
url: https://tonybai.com/2025/03/04/deep-dive-into-gocacheprog-custom-extensions-for-go-build-cache/
published: '2025-03-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 深入GOCACHEPROG：Go构建缓存的自定义扩展

![](../../assets/772f92f090d09e66.png)


[本文永久链接](https://tonybai.com/2025/03/04/deep-dive-into-gocacheprog-custom-extensions-for-go-build-cache) – https://tonybai.com/2025/03/04/deep-dive-into-gocacheprog-custom-extensions-for-go-build-cache

## 1. 背景

众所周知，Go build cache是在[Go 1.10版本](https://tonybai.com/2018/02/17/some-changes-in-go-1-10)加入到Go工具链中的，缓存的主要目标是避免重复编译相同的代码，从而加快构建速度。

默认情况下，Go构建缓存位于用户主目录下的一个特定目录中，例如，Linux上通常是\$HOME/.cache/go-build，Windows上是%LocalAppData%\go-build）。Mac上则是\$HOME/Library/Caches/go-build。当然，Go开发者也可以通过GOCACHE环境变量自定义缓存位置。构建缓存的目录布局结构如下：

![](../../assets/cb319ab2f6eb226f.png)


除了Go build/install命令外，go test命令也会利用构建缓存(包括[fuzzing test](https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18))。除了编译测试代码本身，go test还会缓存测试结果：如果测试代码和依赖项没有变化，并且之前的测试通过，go test会报告(cached)，表示测试结果来自缓存，而无需重新运行测试。如果测试代码或依赖项发生变化，或者之前的测试失败，go test会重新编译和运行测试。

我们看到在GOCACHE目录下还有两个文件，一个是trim.txt，另外一个是testexpire.txt。trim.txt用于对Go构建缓存进行修剪(trim)(\$GOROOT/src/cmd/go/internal/cache/cache.go)，删除不太可能被重复使用的旧缓存条目，避免因过时的缓存占用过多资源，以保持缓存的高效性和有效性，trim.txt中保存了上次进行修剪的时间。testexpire.txt则是用于go clean清理测试缓存(\$GOROOT/src/cmd/go/internal/clean/clean.go)。

默认的Go构建缓存机制取得了不错的构建和测试加速效果，可以满足了大多数需求。不过，也有一些接纳Go的开发者以及公司希望Go构建缓存支持自定义扩展。前Go核心成员、tailscale联创之一的Brad Fitzpatrick在2023年就提出了[Go构建缓存自定义扩展的提案](https://github.com/golang/go/issues/59719)。

在提案中，Bradfitz认为Go内置的构建缓存机制仅支持基于本地文件系统的缓存。在一些持续集成 (CI) 环境中，通常的做法是在每次运行时解和压缩\$GOCACHE目录，这种方法效率低下，甚至可能比CI操作本身还要慢（例如，GitHub Actions 中的缓存）。提案希望Go能够支持更灵活地自定义构建缓存机制，例如：

- 直接利用GitHub的原生缓存系统（而不是低效的 tar/untar）。
- 在公司内部的可信同事之间实现P2P缓存共享协议。

这些扩展的高级功能不太可能直接添加到Go工具本身中，因此Bradfitz希望Go命令可以支持指定一个特定的程序来扩展和管理缓存，这个特定的程序将作为Go命令启动的一个子进程的形式运行，go命令将内部的缓存接口转换为与子进程的通信协议，通过stdin/stdout与其通信。这样该特定的子程序就可以实现任意的缓存机制和策略了。Go与特定程序(比如my-cache-prog)的关系见下面示意图：

![](../../assets/cb61a0fdb064f25d.png)


Bradfitz也对比了使用FUSE（用户空间文件系统）的方案（比如使用juicefs将基于S3的共享文件系统挂载到每个开发人员以及ci节点上，但Bradfitz认为FUSE文件系统在linux之外的平台上不稳定，在很多CI环境下无法工作。因此，一个Go原生支持的用户自定义构建缓存机制是非常有必要的，可以解决Go内置缓存的局限性，特别是在CI环境和团队协作场景中。它通过提供一个外部程序接口来实现灵活性，避免了直接修改Go命令本身。

在《[Go 1.24中值得关注的几个变化](https://tonybai.com/2025/02/16/some-changes-in-go-1-24/)》以及《[Go 1.24新特性前瞻：工具链和标准库](https://tonybai.com/2024/12/17/go-1-24-foresight-part2/)》我们也提及了Go 1.24新增的实验特性：**通过GOCACHEPROG实现Go构建缓存(go build cache)的自定义扩展**。并提到了Bradfitz给出的GOCACHEPROG的参考实现[go-tool-cache](https://github.com/bradfitz/go-tool-cache)。不过Go 1.24正式版发布后，我使用Go 1.24.0验证了一下go-tool-cache，发现go-tool-cache似乎已经**无法与Go 1.24.0正常协作了**：

```
$go version
go version go1.24.0 linux/amd64
$GOCACHEPROG="./go-cacher --verbose --cache-dir /tmp/go-cache" go install fmt
2025/03/03 17:00:30 put(action b8310cbc256f74a5f615df68a3a97753d42e1665adc309e78f20fc13259dec98, obj , 902 bytes): failed to write file to disk with right size: disk=1275; wanted=902
2025/03/03 17:00:30 put(action bc54b2b00ab97b34ef769b66fbe4afd5998f46f843cf2beddcd41974a2564bb1, obj , 1650 bytes): failed to write file to disk with right size: disk=116838; wanted=1650
2025/03/03 17:00:30 put(action 9c4f13b659995a6010f99d4427a18cf2e77919d251ef15e0f751bfdc2dff1806, obj , 1473 bytes): failed to write file to disk with right size: disk=273; wanted=1473
2025/03/03 17:00:30 put(action 6600d21f6b5d283315d789f13e681eed1c51d3ddde835b0f14817ecd144a667e, obj , 566 bytes): failed to write file to disk with right size: disk=565; wanted=566
/root/.bin/go1.24.0/src/internal/runtime/maps/runtime_swiss.go:11:2: package internal/asan is not in std (/root/.bin/go1.24.0/src/internal/asan)
/root/.bin/go1.24.0/src/internal/runtime/maps/group.go:10:2: package internal/runtime/sys is not in std (/root/.bin/go1.24.0/src/internal/runtime/sys)
/root/.bin/go1.24.0/src/fmt/print.go:8:2: package internal/fmtsort is not in std (/root/.bin/go1.24.0/src/internal/fmtsort)
/root/.bin/go1.24.0/src/sync/hashtriemap.go:10:2: package internal/sync is not in std (/root/.bin/go1.24.0/src/internal/sync)
```


修正这个问题还是新实现一个GOCACHEPROG的扩展程序呢？我们选择后者，这样可以让我们更好地从头理解GOCACHEPROG。在这篇文章中，我们会从理解GOCACHEPROG protocol开始，逐步深入到实现自定义缓存管理的具体步骤，包括代码示例。后续基于这个基础，大家可以自己动手，实现满足你的个人/组织需求的Go构建缓存的管理程序。

我们首先来看看Go命令与GOCACHEPROG扩展程序间的协议，这是实现自定义缓存扩展程序的核心。

## 2. 协议

在[cmd/go/internal/cacheprog包的文档](https://pkg.go.dev/cmd/go/internal/cacheprog)中，有关于Go命令与GOCACHEPROG扩展程序间的协议的详细说明。下面基于该文档，我们对这个协议做一些说明，并作为后续实现的参考。

前面说过，GOCACHEPROG是Go 1.24引入的新实验特性(很大可能在Go 1.25版本转正)，允许使用外部程序实现Go构建缓存。其间的通信协议基于JSON消息通过stdin/stdout进行交换。Go命令将GOCACHEPROG指定的程序(以下称为my-cache-prog)以child process的形式启动，之后my-cache-prog与go命令之间的通信过程大致如下：

- 初始化: my-cache-prog启动后立即发送一个包含自身支持命令的Response消息(也称为init response，对应的ID=0)给Go命令。
- 请求-响应模型: Go命令收到init response后，根据其支持的命令，发送Request，缓存程序my-cache-prog收到请求后进行处理，并回复Response

目前协议支持的命令类型包括如下三种：

- put: 将对象存储到缓存中。
- get: 从缓存中检索对象。
- close: 请求缓存程序优雅退出。

显然，通过KnownCommands机制，Go命令可以支持未来协议的扩展。

文档中还给出了协议请求响应模型中Request和Response的定义，这个我们在Go命令的实现中也能找到：

```
// $GOROOT/src/cmd/go/internal/cacheprog/cacheprog.go
// Cmd is a command that can be issued to a child process.
//
// If the interface needs to grow, the go command can add new commands or new
// versioned commands like "get2" in the future. The initial [Response] from
// the child process indicates which commands it supports.
type Cmd string
const (
// CmdPut tells the cache program to store an object in the cache.
//
// [Request.ActionID] is the cache key of this object. The cache should
// store [Request.OutputID] and [Request.Body] under this key for a
// later "get" request. It must also store the Body in a file in the local
// file system and return the path to that file in [Response.DiskPath],
// which must exist at least until a "close" request.
CmdPut = Cmd("put")
// CmdGet tells the cache program to retrieve an object from the cache.
//
// [Request.ActionID] specifies the key of the object to get. If the
// cache does not contain this object, it should set [Response.Miss] to
// true. Otherwise, it should populate the fields of [Response],
// including setting [Response.OutputID] to the OutputID of the original
// "put" request and [Response.DiskPath] to the path of a local file
// containing the Body of the original "put" request. That file must
// continue to exist at least until a "close" request.
CmdGet = Cmd("get")
// CmdClose requests that the cache program exit gracefully.
//
// The cache program should reply to this request and then exit
// (thus closing its stdout).
CmdClose = Cmd("close")
)
// Request is the JSON-encoded message that's sent from the go command to
// the GOCACHEPROG child process over stdin. Each JSON object is on its own
// line. A ProgRequest of Type "put" with BodySize > 0 will be followed by a
// line containing a base64-encoded JSON string literal of the body.
type Request struct {
// ID is a unique number per process across all requests.
// It must be echoed in the Response from the child.
ID int64
// Command is the type of request.
// The go command will only send commands that were declared
// as supported by the child.
Command Cmd
// ActionID is the cache key for "put" and "get" requests.
ActionID []byte `json:",omitempty"` // or nil if not used
// OutputID is stored with the body for "put" requests.
//
// Prior to Go 1.24, when GOCACHEPROG was still an experiment, this was
// accidentally named ObjectID. It was renamed to OutputID in Go 1.24.
OutputID []byte `json:",omitempty"` // or nil if not used
// Body is the body for "put" requests. It's sent after the JSON object
// as a base64-encoded JSON string when BodySize is non-zero.
// It's sent as a separate JSON value instead of being a struct field
// send in this JSON object so large values can be streamed in both directions.
// The base64 string body of a Request will always be written
// immediately after the JSON object and a newline.
Body io.Reader `json:"-"`
// BodySize is the number of bytes of Body. If zero, the body isn't written.
BodySize int64 `json:",omitempty"`
// ObjectID is the accidental spelling of OutputID that was used prior to Go
// 1.24.
//
// Deprecated: use OutputID. This field is only populated temporarily for
// backwards compatibility with Go 1.23 and earlier when
// GOEXPERIMENT=gocacheprog is set. It will be removed in Go 1.25.
ObjectID []byte `json:",omitempty"`
}
// Response is the JSON response from the child process to the go command.
//
// With the exception of the first protocol message that the child writes to its
// stdout with ID==0 and KnownCommands populated, these are only sent in
// response to a Request from the go command.
//
// Responses can be sent in any order. The ID must match the request they're
// replying to.
type Response struct {
ID int64 // that corresponds to Request; they can be answered out of order
Err string `json:",omitempty"` // if non-empty, the error
// KnownCommands is included in the first message that cache helper program
// writes to stdout on startup (with ID==0). It includes the
// Request.Command types that are supported by the program.
//
// This lets the go command extend the protocol gracefully over time (adding
// "get2", etc), or fail gracefully when needed. It also lets the go command
// verify the program wants to be a cache helper.
KnownCommands []Cmd `json:",omitempty"`
// For "get" requests.
Miss bool `json:",omitempty"` // cache miss
OutputID []byte `json:",omitempty"` // the ObjectID stored with the body
Size int64 `json:",omitempty"` // body size in bytes
Time *time.Time `json:",omitempty"` // when the object was put in the cache (optional; used for cache expiration)
// For "get" and "put" requests.
// DiskPath is the absolute path on disk of the body corresponding to a
// "get" (on cache hit) or "put" request's ActionID.
DiskPath string `json:",omitempty"`
}
```


Request是由Go命令发送的请求，它包含的几个字段的含义如下：

- ID: 每个进程中所有请求的唯一编号
- Command: 请求类型(put/get/close)
- ActionID: 缓存键
- OutputID: 存储在缓存中的对象ID，实际也是Body数据的Sha256的值。
- Body: “put”请求的主体数据，”get”和”close”请求没有Body。
- BodySize: Body的字节数

Response则是由缓存程序回复给Go命令的结构，它的定义中的几个字段的含义如下：

- ID: 对应请求的ID
- Err: 错误信息(如有)
- KnownCommands: 支持的命令列表(用于初始Response)
- Miss: 缓存未命中标志
- OutputID: 存储在缓存中的对象ID
- Size: 主体大小(字节)
- Time: 对象放入缓存的时间
- DiskPath: 对应缓存项在磁盘上的绝对路径

这里要注意几点：

- 除了init Response，其他Response可以乱序返回，Go命令会通过Response中的ID来匹配对应的Request。
- 不论缓存数据存储在哪里，最终提供给Go命令的都应该在本地文件系统中，并通过Response中的DiskPath来指示该数据对应的绝对路径。

为了能更好地理解这个协议的交互，我这里画了一幅Go命令与my-cache-prog之间的交互示意图：

![](../../assets/f9d3255289d59df2.png)


到这里，还有一个地方尚未清楚，那就是put请求与put/get请求之间以及put请求内部body的编码格式并未说清楚。在文档中，这部分也不是那么清晰，但这却决定了后续实现的正确性。为了给后面的实现做好铺垫，我们可以通过查看Go命令的对put请求的编码实现来确认这部分内容。在

```
// $GOROOT/src/cmd/go/internal/cache/prog.go
func (c *ProgCache) writeToChild(req *cacheprog.Request, resc chan<- *cacheprog.Response) (err error) {
c.mu.Lock()
if c.inFlight == nil {
return errCacheprogClosed
}
c.nextID++
req.ID = c.nextID
c.inFlight[req.ID] = resc
c.mu.Unlock()
defer func() {
if err != nil {
c.mu.Lock()
if c.inFlight != nil {
delete(c.inFlight, req.ID)
}
c.mu.Unlock()
}
}()
c.writeMu.Lock()
defer c.writeMu.Unlock()
if err := c.jenc.Encode(req); err != nil {
return err
}
if err := c.bw.WriteByte('\n'); err != nil {
return err
}
if req.Body != nil && req.BodySize > 0 {
if err := c.bw.WriteByte('"'); err != nil {
return err
}
e := base64.NewEncoder(base64.StdEncoding, c.bw)
wrote, err := io.Copy(e, req.Body)
if err != nil {
return err
}
if err := e.Close(); err != nil {
return nil
}
if wrote != req.BodySize {
return fmt.Errorf("short write writing body to GOCACHEPROG for action %x, output %x: wrote %v; expected %v",
req.ActionID, req.OutputID, wrote, req.BodySize)
}
if _, err := c.bw.WriteString("\"\n"); err != nil {
return err
}
}
if err := c.bw.Flush(); err != nil {
return err
}
return nil
}
```


通过上述代码，我们可以总结出下面put请求的编码格式：

![](../../assets/606f555e4a751518.png)


解释一下这张图。

- 顶部(蓝色区域): JSON编码的请求元数据

包含ID、ActionID、OutputID和BodySize等字段。这部分使用标准JSON格式。

- 中间(黄色条): 换行符分隔符(‘\n’)

JSON元数据后的第一个换行符。

- 中部(绿色区域): Base64编码的请求体(可选)

这部分以双引号(“)开始，紧接着是Base64编码的二进制数据，最后以双引号(“)结束。

- 底部(黄色条): 最终换行符(‘\n’)

整个请求的结束标记。

总的来说，Go命令的put请求使用了JSON+Base64的组合编码方式：请求的元数据以JSON格式编码，请求体以Base64编码(base64编码前后各有一个双引号)，它们之间用换行符分隔，整个请求最后以换行符结束。这种格式便于解析，同时也能处理二进制数据。

注意：根据json.Encoder.Encode的文档，编码后的json文本也会跟着一个换行符(newline)。


不过代码中还有一点非常值得注意，那就是**Put请求的BodySize的值为base64编码之前的Body长度**！这一点如果不看源码，很容易使用BodySize去读取Body体的内容，从而导致解码出错！

好了，详细了解了上述协议后，我们就来尝试实现一个my-cache-prog程序。程序开源到[github.com/bigwhite/go-cache-prog项目](https://github.com/bigwhite/go-cache-prog)中了，大家可以结合项目代码来继续阅读下面的内容。

## 3. 实现

### 3.1 整体设计

go-cache-prog的实现采用了模块化设计，将不同的功能划分到独立的包中，以提高代码的可维护性和可扩展性。整体结构如下：

```
go-cache-prog/
├── cmd/
│ └── go-cache-prog/
│ └── main.go (可执行程序入口)
├── protocol/
│ └── protocol.go (请求/响应定义和解析)
├── storage/
│ ├── storage.go (存储后端接口)
│ └── filesystem/
│ └── filesystem.go (基于本地文件系统的存储实现)
└── cache/
└── cache.go (内存缓存逻辑)
```


- cmd/go-cache-prog/main.go: 这是可执行程序的入口点。

它负责解析命令行参数、设置日志输出、确定缓存目录、初始化存储和缓存、发送初始能力响应、启动请求处理循环。

```
// cmd/go-cache-prog/main.go (部分)
func main() {
// ... (参数解析、日志设置、缓存目录确定) ...
store, err := filesystem.NewFileSystemStorage(cacheDir, verbose)
if err != nil {
log.Fatalf("Failed to initialize filesystem storage: %v", err)
}
cacheInstance := cache.NewCache(store)
// ... (发送初始响应) ...
requestHandler := protocol.NewRequestHandler(reader, os.Stdout, cacheInstance, verbose)
if err := requestHandler.HandleRequests(); err != nil {
log.Fatalf("Error handling requests: %v", err)
}
}
```


- protocol: 此包处理与go命令的通信协议，定义请求/响应结构，处理请求。

```
// protocol/protocol.go (部分)
type RequestHandler struct {
reader *bufio.Reader
writer io.Writer
cache *cache.Cache
verbose bool
gets int //statistics
getMiss int
}
func (rh *RequestHandler) HandleRequests() error {
for {
req, err := rh.readRequest()
// ... (错误处理、请求处理) ...
}
}
```


- storage: 此包定义了存储后端的抽象接口。

```
// storage/storage.go
type Storage interface {
Put(actionID, outputID []byte, data []byte, size int64) (string, error)
Get(actionID []byte) (outputID []byte, size int64, modTime time.Time, diskPath string, found bool, err error)
// ... (可选方法) ...
}
```


- storage/filesystem: 此包提供了storage.Storage接口的一个具体实现，使用本地文件系统。

```
// storage/filesystem/filesystem.go (部分)
type FileSystemStorage struct {
baseDir string
verbose bool
}
func NewFileSystemStorage(baseDir string, verbose bool) (*FileSystemStorage, error) {
// ... (创建目录) ...
}
```


- cache: 此包实现了内存缓存层, 位于存储接口之上。

```
// cache/cache.go (部分)
type Cache struct {
entries map[string]CacheEntry
mu sync.RWMutex
store storage.Storage
}
func NewCache(store storage.Storage) *Cache {
// ... (初始化 map) ...
}
```


### 3.2 协议解析

protocol包负责处理go-cache-prog与go命令之间的基于JSON的通信协议。

- 请求 (Request):

```
// protocol/protocol.go
type Request struct {
ID int64
Command Cmd
ActionID []byte `json:",omitempty"`
OutputID []byte `json:",omitempty"`
Body io.Reader `json:"-"`
BodySize int64 `json:",omitempty"`
ObjectID []byte `json:",omitempty"` // Deprecated
}
```


- 响应 (Response):

```
// protocol/protocol.go
type Response struct {
ID int64 `json:",omitempty"`
Err string `json:",omitempty"`
KnownCommands []Cmd `json:",omitempty"`
Miss bool `json:",omitempty"`
OutputID []byte `json:",omitempty"`
Size int64 `json:",omitempty"`
Time *time.Time `json:",omitempty"`
DiskPath string `json:",omitempty"`
}
```


RequestHandler的readRequest方法负责读取和解析请求：

```
// protocol/protocol.go (部分)
func (rh *RequestHandler) readRequest() (*Request, error) {
line, err := rh.reader.ReadBytes('\n')
if err != nil {
return nil, err
}
// ... (处理空行) ...
var req Request
if err := json.Unmarshal(line, &req); err != nil {
// 检查base64
if len(line) >= 2 && line[0] == '"' && line[len(line)-1] == '"'{
// ...
}
return nil, fmt.Errorf("failed to unmarshal request: %w", err)
}
return &req, nil
}
```


对于put请求, 如果BodySize大于0, 需要读取并解码Base64数据：

```
// protocol/protocol.go (部分)
func (rh *RequestHandler) handlePut(req *Request) {
var bodyData []byte
if req.BodySize > 0 {
bodyLine, err := rh.reader.ReadBytes('\n')
// ... (跳过空行)...
bodyLine, err = rh.reader.ReadBytes('\n')
// ... (错误处理) ...
bodyLine = bytes.TrimSpace(bodyLine)
if len(bodyLine) < 2 || bodyLine[0] != '"' || bodyLine[len(bodyLine)-1] != '"' {
// ... (格式错误) ...
}
base64Body := bodyLine[1 : len(bodyLine)-1]
bodyData, err = base64.StdEncoding.DecodeString(string(base64Body))
// ... (解码错误、大小不匹配处理) ...
}
// ... (调用 cache.Put) ...
}
```


### 3.3 缓存管理

cache包实现了内存缓存层，减少对底层存储的访问。

- CacheEntry结构体:

```
// cache/cache.go
type CacheEntry struct {
OutputID []byte
Size int64
Time time.Time
DiskPath string
}
```


- Cache结构体和NewCache:

```
// cache/cache.go
type Cache struct {
entries map[string]CacheEntry
mu sync.RWMutex
store storage.Storage
}
func NewCache(store storage.Storage) *Cache {
return &Cache{
entries: make(map[string]CacheEntry),
store: store,
}
}
```


- Put方法:

```
// cache/cache.go
func (c *Cache) Put(actionID, outputID []byte, data []byte, size int64) (string, error) {
diskPath, err := c.store.Put(actionID, outputID, data, size)
if err != nil {
return "", err
}
entry := CacheEntry{ /* ... */ }
actionIDHex := fmt.Sprintf("%x", actionID)
c.mu.Lock()
c.entries[actionIDHex] = entry
c.mu.Unlock()
return diskPath, nil
}
```


- Get方法:

```
// cache/cache.go
func (c *Cache) Get(actionID []byte) (*CacheEntry, bool, error) {
actionIDHex := fmt.Sprintf("%x", actionID)
c.mu.RLock()
entry, exists := c.entries[actionIDHex]
c.mu.RUnlock()
if exists {
return &entry, true, nil // 优先从内存缓存读取
}
// ... (从存储中读取, 并更新内存缓存) ...
}
```


### 3.4 抽象存储接口与本地文件系统实现

storage.Storage接口定义了存储后端的抽象，目的是为了支持更多的实现扩展，比如支持在S3上存储等。

```
// storage/storage.go
type Storage interface {
Put(actionID, outputID []byte, data []byte, size int64) (string, error)
Get(actionID []byte) (outputID []byte, size int64, modTime time.Time, diskPath string, found bool, err error)
}
```


storage/filesystem包提供了一种基于本地文件系统的实现。

- FileSystemStorage和NewFileSystemStorage:

```
// storage/filesystem/filesystem.go
type FileSystemStorage struct {
baseDir string
verbose bool
}
func NewFileSystemStorage(baseDir string, verbose bool) (*FileSystemStorage, error) {
if err := os.MkdirAll(baseDir, 0755); err != nil {
return nil, err
}
return &FileSystemStorage{baseDir: baseDir, verbose: verbose}, nil
}
```


- Put方法:

```
// storage/filesystem/filesystem.go
func (fss *FileSystemStorage) Put(actionID, outputID []byte, data []byte, size int64) (string, error) {
actionIDHex := fmt.Sprintf("%x", actionID)
//outputIDHex := fmt.Sprintf("%x", outputID) //Might not need
actionFile := filepath.Join(fss.baseDir, fmt.Sprintf("a-%s", actionIDHex))
diskPath := filepath.Join(fss.baseDir, fmt.Sprintf("o-%s", actionIDHex))
absPath, _ := filepath.Abs(diskPath)
// Write metadata
now := time.Now()
ie, err := json.Marshal(indexEntry{
Version: 1,
OutputID: outputID,
Size: size,
Time: &now,
})
// ... (错误处理, 写入元数据文件) ...
if size > 0{
// 写入数据文件
if err := os.WriteFile(diskPath, data, 0644); err != nil {
return "", fmt.Errorf("failed to write cache file: %w", err)
}
} else {
//创建空文件
zf, err := os.OpenFile(diskPath, os.O_CREATE|os.O_RDWR, 0644)
if err != nil {
return "", fmt.Errorf("failed to create empty file: %w", err)
}
zf.Close()
}
return absPath, nil
}
```


- Get方法:

```
// storage/filesystem/filesystem.go
func (fss *FileSystemStorage) Get(actionID []byte) (outputID []byte, size int64, modTime time.Time, diskPath string, found bool, err error) {
actionIDHex := fmt.Sprintf("%x", actionID)
actionFile := filepath.Join(fss.baseDir, fmt.Sprintf("a-%s", actionIDHex))
// Read metadata
af, err := os.ReadFile(actionFile)
// ... (文件不存在处理) ...
var ie indexEntry
if err := json.Unmarshal(af, &ie); err != nil {
return nil, 0, time.Time{}, "", false, fmt.Errorf("failed to unmarshal index entry: %w", err)
}
objectFile := filepath.Join(fss.baseDir, fmt.Sprintf("o-%s", actionIDHex))
info, err := os.Stat(objectFile)
// ... (对象文件不存在、或其他错误处理) ...
diskPath, _ = filepath.Abs(objectFile)
return ie.OutputID, info.Size(), info.ModTime(), diskPath, true, nil
}
```


storage/filesystem使用了两种类型的文件来分别存储缓存数据和元数据：

- a-{actionID} (Action File): 元数据文件

这个文件存储了关于缓存条目的元数据，使用JSON格式。actionID是缓存键的十六进制表示。

- o-{actionID} (Object File): 对象文件。

这个文件存储了实际的缓存数据（即Request.Body的内容）。actionID 与对应的元数据文件中的actionID 相同。

对于一些Put请求(with BodySize=0)的，同样会创建元数据文件和对象文件，只是对象文件的size为0。

这么设计便于快速查找：在执行Get操作时，go-cache-prog首先读取a-{actionID}文件。这个文件很小，因为它只包含元数据。通过读取这个文件，go-cache-prog可以快速确定：缓存条目是否存在（如果 a-{actionID} 文件不存在，则肯定不存在）。 如果存在，可以获取到OutputID、数据大小（Size）和最后修改时间（Time），并放入内存缓存中，而无需读取可能很大的o-{actionID}文件，便可以知道对象文件（o-{actionID}）是否存在。

## 4. 验证

下载go-cache-prog源码并编译：

```
$git clone https://github.com/bigwhite/go-cache-prog.git
$make
```


注意：go-cache-prog需要与Go 1.24及以上版本配合使用。


接下来，我们将fmt包首次编译安装到go-cache-prog的默认缓存目录下(~/.gocacheprog)：

```
$GOCACHEPROG="./go-cache-prog --verbose" go install fmt
2025/03/04 10:47:59 Using cache directory: /Users/tonybai/.gocacheprog
2025/03/04 10:47:59 Received request: ID=1, Command=get, ActionID=90c776cb58a3c3a99b5622344df5bc959fd2b90f299b40ae21ec6ccf16c77a23, OutputID=, BodySize=0
2025/03/04 10:47:59 Received request: ID=2, Command=put, ActionID=90c776cb58a3c3a99b5622344df5bc959fd2b90f299b40ae21ec6ccf16c77a23, OutputID=4e67091862cdc5ff3d44d51adaf9f5a3f5e993dcbc0b6aad884d00d929f3f4d3, BodySize=3037
2025/03/04 10:47:59 Put request: ID=2, Actual BodyLen=4055
2025/03/04 10:47:59 Received request: ID=3, Command=get, ActionID=b2d3027bda366ae198f991d65f62b5be25aa7fe41092bb81218ba24363923b69, OutputID=, BodySize=0
2025/03/04 10:47:59 Received request: ID=4, Command=get, ActionID=c48dafcc394ccfed5c334ef2e21ba8b5bd09a883956f17601cf8a3123f8afd2b, OutputID=, BodySize=0
2025/03/04 10:47:59 Received request: ID=5, Command=get, ActionID=b16400d94b83897b0e7a54ee4223208ff85b4926808bcae66e488d2dbab85054, OutputID=, BodySize=0
2025/03/04 10:47:59 Received request: ID=6, Command=get, ActionID=789f5b8e5b2390e56d26ac916b6f082bfb3e807ee34302f8aa0310e6e225ac77, OutputID=, BodySize=0
... ...
2025/03/04 10:48:03 Received request: ID=321, Command=close, ActionID=, OutputID=, BodySize=0
2025/03/04 10:48:03 Gets: 107, GetMiss: 107
```


由于初始情况下，默认缓存目录下(~/.gocacheprog)没有构建缓存的文件，因此上面的所有get都miss了，go命令会发送put请求，go-cache-prog会构建初始cache。在默认缓存目录下(~/.gocacheprog)下，我们可以看到类似这样的文件列表：

```
$ls ~/.gocacheprog
a-01fae6e8773991089b07eef70a209ee3e99e229231b4956689d7c914a84c70de
a-030b82281d0fae81d44e96b140c276fa232abe46ae92b7fe1d4b7213bc58eef1
a-046d1381c7f1061967c50c5ba2a112486374c6682e80b154f26f17302eb623a4
... ...
o-fc0a0cf26b5a438834ee47a7166286bfb4266c93b667a66e5630502db7651507
o-fc5364bf6b2b714e6a90e8b57652827666b93366f0e322875eefd21b4cc58b3f
o-fde27b35692f9efeae945f00ab029fe156cbfa961bf6149ab9767e1efd057545
o-ff141dd2b1c95d4cba6c3cda5792d8863e428824565ecb5765018710199a2f69
```


接下来，我们再次执行同样的命令，看看cache是否起到了作用：

```
$GOCACHEPROG="./go-cache-prog --verbose" go install fmt
2025/03/04 10:50:14 Using cache directory: /Users/tonybai/.gocacheprog
2025/03/04 10:50:14 Received request: ID=1, Command=get, ActionID=90c776cb58a3c3a99b5622344df5bc959fd2b90f299b40ae21ec6ccf16c77a23, OutputID=, BodySize=0
2025/03/04 10:50:14 Received request: ID=2, Command=get, ActionID=c48dafcc394ccfed5c334ef2e21ba8b5bd09a883956f17601cf8a3123f8afd2b, OutputID=, BodySize=0
2025/03/04 10:50:14 Received request: ID=3, Command=get, ActionID=b16400d94b83897b0e7a54ee4223208ff85b4926808bcae66e488d2dbab85054, OutputID=, BodySize=0
2025/03/04 10:50:14 Received request: ID=4, Command=get, ActionID=789f5b8e5b2390e56d26ac916b6f082bfb3e807ee34302f8aa0310e6e225ac77, OutputID=, BodySize=0
2025/03/04 10:50:14 Received request: ID=5, Command=get, ActionID=c6e6427a15f95d70621df48cc68ab039075d66c1087427eb9a04bcf729c5b491, OutputID=, BodySize=0
... ...
2025/03/04 10:50:14 Received request: ID=161, Command=close, ActionID=, OutputID=, BodySize=0
2025/03/04 10:50:14 Gets: 160, GetMiss: 0
```


我们看到所有的Get请求都命中了缓存(GetMiss: 0)，此次执行也肉眼可见的快！

我们再来用一个可执行程序验证一下利用build cache的构建。在go-cache-prog项目下有一个examples/helloworld示例，在该目录下执行make，我们就能看到构建的输出：

```
$cd examples/helloworld
$make
GOCACHEPROG="../../go-cache-prog --verbose" go build
2025/03/04 10:54:35 Using cache directory: /Users/tonybai/.gocacheprog
2025/03/04 10:54:35 Received request: ID=1, Command=get, ActionID=7c1950a92d55fae91254e8923f7ea4cdfd2ce34953bcf2348ba851be3e2402a1, OutputID=, BodySize=0
2025/03/04 10:54:35 Received request: ID=2, Command=put, ActionID=7c1950a92d55fae91254e8923f7ea4cdfd2ce34953bcf2348ba851be3e2402a1, OutputID=43b1c1a308784cd610fda967d781d3c5ccfd4950263df98d18a2ddb2dd218f5a, BodySize=251
2025/03/04 10:54:35 Put request: ID=2, Actual BodyLen=339
2025/03/04 10:54:35 Received request: ID=3, Command=get, ActionID=90c776cb58a3c3a99b5622344df5bc959fd2b90f299b40ae21ec6ccf16c77a23, OutputID=, BodySize=0
... ...
2025/03/04 10:54:35 Received request: ID=165, Command=close, ActionID=, OutputID=, BodySize=0
2025/03/04 10:54:35 Gets: 163, GetMiss: 1
```


我们看到绝大部分都是命中缓存的。

执行构建出的helloworld，程序也会正常输出内容：

```
$./helloworld
hello, world!
```


## 5. 小结

本文深入探讨了Go 1.24引入的GOCACHEPROG这一实验性特性，它为Go构建缓存带来了前所未有的灵活性。通过允许开发者使用自定义程序来管理构建缓存，GOCACHEPROG解决了Go内置缓存机制在特定场景下的局限性，特别是CI环境和团队协作中的痛点。

文中，我们基于对协议的理解，逐步构建了一个名为[go-cache-prog](https://github.com/bigwhite/go-cache-prog)的自定义缓存程序。go-cache-prog采用了模块化设计，将协议解析、缓存管理和存储抽象分离到不同的包中，提高了代码的可维护性和可扩展性。

最后，我们通过实际的编译和安装示例，验证了go-cache-prog的功能，展示了它如何与Go命令协同工作，实现自定义的构建缓存管理。

go-cache-prog项目提供了一个坚实的基础，开发者可以在此基础上进行扩展，实现更高级的功能，例如：

- 不同的存储后端：实现storage.Storage接口，支持将缓存数据存储到云存储（如 AWS S3、Google Cloud Storage）、分布式缓存（如 Redis、Memcached）或其他存储系统中。
- 缓存失效策略：实现更复杂的缓存失效策略，例如基于 LRU（最近最少使用）或 TTL（生存时间）的过期机制。
- 分布式缓存：构建一个分布式的缓存系统，支持在多个开发机器或 CI 节点之间共享构建缓存。
- 监控和统计：添加监控和统计功能，跟踪缓存命中率、缓存大小、性能指标等。

此外，目前的go-cache-prog是顺序处理go命令的请求的，大家也可以自行将其改造为并发处理请求，不过务必注意并发处理的同步。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格6$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论