---
title: API设计的“Go境界”：Go团队设计MCP SDK过程中的取舍与思考
url: https://tonybai.com/2025/05/23/go-api-design-mcp-sdk/
published: '2025-05-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# API设计的“Go境界”：Go团队设计MCP SDK过程中的取舍与思考

![](../../assets/289c035610bcdc59.png)


[本文永久链接](https://tonybai.com/2025/05/23/go-api-design-mcp-sdk) – https://tonybai.com/2025/05/23/go-api-design-mcp-sdk

大家好，我是 Tony Bai。

作为开发者，我们每天都在与 API 打交道——调用它们，设计它们，有时也会为糟糕的 API 设计而头痛不已。一个优秀的 API，如同一位技艺精湛的向导，能清晰、高效地引领我们通往复杂功能的彼岸；而一个蹩脚的 API，则可能像一座布满陷阱的迷宫，让我们步履维艰。

那么，在 Go 语言的世界里，一个“好”的 API 应该是什么样子的？它应该如何体现 Go 语言简洁、高效、并发安全的哲学？它又如何在满足功能需求的同时，保持对开发者的友好和对未来的兼容？

最近，Go 官方团队为 Model Context Protocol (MCP) 发起了一项 Go SDK 的设计讨论，并公开了其详细的设计草案以及一个初期的原型代码实现。这份设计稿与代码，在我看来，不仅仅是对 MCP 协议的 Go 语言实现规划，更是一份**Go 官方团队关于 API 设计思考与实践的“公开课”**。它向我们生动地展示了，在打造一个既强大又符合 Go 惯例 (Idiomatic Go) 的 SDK 时，需要在哪些维度进行权衡取舍，以及如何将 Go 的设计哲学融入到每一个细节之中。

今天，就让我们一同走进这份设计稿和它的原型代码，探寻 Go 团队在 API 设计中所追求的“Go 境界”。

## API 设计的“初心”：Go 团队为 MCP SDK 设定的目标

在深入细节之前，我们先来看看 Go 团队为这个官方 MCP SDK 设定了哪些核心目标 (Requirements)。这些目标，本身就是设计任何高质量 Go SDK 的重要准则：

**完整性 (Complete):**能够实现 MCP 规范中的所有特性，并严格遵循其语义。这是 SDK 作为协议实现的基本要求。**符合 Go 惯例 (Idiomatic):**这是“Go 境界”的核心。SDK 应最大限度地利用 Go 语言自身的特性和标准库的设计风格，并重复 Go 生态中相似领域（如 net/http, grpc-go）已形成的习惯用法。**健壮性 (Robust):**SDK 自身必须是经过良好测试、稳定可靠的，并且要能让使用者轻松地对他们基于 SDK 构建的应用进行测试。**面向未来 (Future-proof):**设计必须考虑到 MCP 规范未来可能的演进，尽可能地避免因规范变更而导致 SDK API 发生不兼容的破坏性改动。**可扩展性 (Extensible) 与最小化 (Minimal):**为了最好地服务于前述四个目标，SDK 的核心 API 应保持最小化、正交化。同时，它必须允许用户通过简单、清晰的方式（如接口、中间件、钩子等）进行扩展，以满足特定需求。

这些目标清晰地勾勒出了 Go 团队对一个“好”的 Go SDK 的期望：它不仅要功能完备，更要“写起来像 Go，用起来像 Go”，并且能经受住时间的考验。

## 庖丁解牛：MCP Go SDK 设计中的“Go 味”与权衡

设定了清晰的 API 设计目标后，Go 团队便开始将这些原则付诸实践，着手设计 MCP Go SDK 的具体结构与接口。细细品读这份设计稿和其原型代码，我们能从多个关键的决策中，清晰地品味出浓浓的“Go 味”，并深刻体会到他们在功能完备性、语言惯例、当前易用性与未来演进性之间所做的精妙权衡。

### 包布局

在 SDK 的整体结构上，Go 团队针对包的布局做出了一个显著的选择，这直接体现了他们对 Go 生态习惯的深刻理解和对开发者体验的优先考量。不同于其他语言的 MCP SDK 可能会将客户端、服务端、传输层等功能细致地拆分到各自独立的包中，Go 团队提议将 SDK 的核心用户接口**集中在单个 mcp 包内**。

这种做法与 Go 标准库中的 net/http、net/rpc 以及社区广泛采纳的 google.golang.org/grpc 等核心包的组织方式保持了高度一致。对于 Go 开发者而言，这意味着更低的认知门槛——当他们需要使用 MCP 功能时，几乎所有的核心 API 都能在同一个 mcp 包下找到，**这极大地提升了 API 的发现性**。同时，集中的包结构也更利于生成聚合的包文档，并在 IDE 中提供更流畅的代码提示与导航体验。

更深一层的考量，则是为了 SDK 的**长期稳定性和面向未来的适应性**。如果将功能过度拆分到多个细粒度的包中，未来 MCP 规范的任何微小调整，都可能引发连锁的包结构变动或复杂的跨包依赖问题。而单一核心包的设计，则能更好地吸收这些变化，减少对用户代码的冲击。当然，像 JSON Schema 这种与 MCP 核心逻辑不直接相关、但又可能被 SDK 用户需要的辅助功能，则被合理地规划到了独立的子包（如 jsonschema/）中，做到了关注点分离。虽然这种策略可能会让一些追求极致“模块化”的开发者觉得核心包略显“庞大”，但 Go 团队在此显然是权衡了用户发现性、文档清晰度以及长期演进的稳定性，将它们放在了更高的优先级。

### JSON-RPC 与传输层抽象 (Transports)

MCP 协议的核心在于通过 JSON-RPC 在客户端和服务端之间交换消息，而其底层可以有多种传输方式，如 stdio、可流式 HTTP、SSE 等。如何为这些形态各异的传输方式设计一个统一且灵活的抽象层，是对 SDK 设计者的一大考验。Go 团队在这里再次展现了其对接口设计艺术的娴熟运用。

在 transport.go 中，他们定义了一个非常底层的 Transport 接口：

```
// A Transport is used to create a bidirectional connection between MCP client
// and server.
type Transport interface {
Connect(ctx context.Context) (Stream, error)
}
```


其核心职责仅在于通过 Connect 方法建立一个逻辑连接，并返回一个 Stream 接口实例。这个 Stream 接口则更为基础，借鉴了 golang.org/x/tools/internal/jsonrpc2_v2 的设计：

```
// A Stream is a bidirectional jsonrpc2 Stream.
type Stream interface {
jsonrpc2.Reader
jsonrpc2.Writer
io.Closer
}
```


它组合了读、写和关闭能力。这种设计充满了“Go 味”：**接口被设计得小巧而精炼**，只暴露了最根本的抽象，完美体现了 Go “定义小接口，实现大价值”的理念。

具体来看，Stream 接口因为内嵌了 io.Closer，使其自然地遵循了标准库的惯例，这使得它可以无缝集成到 Go 的资源管理模式中。更重要的是，Connect 方法的签名严格遵循了 (ctx context.Context, …params) (…results, error) 的形式。context.Context 作为第一个参数，用于优雅地处理操作的超时和取消；而 error 作为最后一个返回值，则用于明确、一致地传递错误信息。这些都是 Go I/O 和网络编程中雷打不动的**标准模式**。这种底层接口的简洁性不仅巧妙地隐藏了内部 JSON-RPC 实现的复杂细节（如 mcp/internal/jsonrpc2_v2 的使用），也为用户实现自定义的传输方式（如设计稿中提到的 InMemoryTransport 或 LoggingTransport）提供了极大的便利。

例如，NewCommandTransport 用于创建通过子进程 stdio 通信的客户端传输：

```
// NewCommandTransport returns a [CommandTransport] that runs the given command
// and communicates with it over stdin/stdout.
func NewCommandTransport(cmd *exec.Cmd) *CommandTransport { /* ... */ }
```


得到的CommandTransport的Connect 方法会启动命令并连接到其 stdin/stdout。这种清晰的职责划分和对 Go 标准模式的遵循，使得整个传输层易于理解和扩展。

### 客户端与服务端 API (Clients & Servers)

在客户端和服务端核心对象的 API 设计上，Go 团队同样融入了对 Go 并发模型的深刻理解。设计稿清晰地区分了 Client/Server 实例与 ClientSession/ServerSession 的概念，这在 client.go 和 server.go 中得到了体现。一个 Client 或 Server 实例可以处理多个并发的连接，即对应多个会话。这与我们熟悉的标准库 http.Client 可以发起多个 HTTP 请求，而 http.Server 可以同时为多个客户端提供服务的模式如出一辙。

```
// In client.go
type Client struct {
// ...
mu sync.Mutex
sessions []*ClientSession
// ...
}
func NewClient(name, version string, opts *ClientOptions) *Client { /* ... */ }
func (c *Client) Connect(ctx context.Context, t Transport) (*ClientSession, error) { /* ... */ }
// In server.go
type Server struct {
// ...
mu sync.Mutex
sessions []*ServerSession
// ...
}
func NewServer(name, version string, opts *ServerOptions) *Server { /* ... */ }
func (s *Server) Connect(ctx context.Context, t Transport) (*ServerSession, error) { /* ... */ }
```


这种 N:1（多个会话对应一个 Client/Server 实例）的设计，天然地利用并体现了 Go 语言强大的并发处理能力，通过 sync.Mutex 保护共享状态。考虑到 Client 和 Server 本身都是有状态的（例如，Client 可以动态添加或移除其追踪的根资源，Server 则可以动态添加或移除其提供的工具），当这些核心实例的状态发生变化时，设计确保了所有与其连接的对等方（即各个会话）都会收到相应的通知，从而维持了状态的一致性。

在配置方式上，Go 团队为 Client 和 Server 的创建选择了使用独立的 ClientOptions 和 ServerOptions **结构体**，如：

```
// In client.go
type ClientOptions struct {
CreateMessageHandler func(context.Context, *ClientSession, *CreateMessageParams) (*CreateMessageResult, error)
ToolListChangedHandler func(context.Context, *ClientSession, *ToolListChangedParams)
// ... other handlers
}
// In server.go
type ServerOptions struct {
Instructions string
InitializedHandler func(context.Context, *ServerSession, *InitializedParams)
// ... other handlers and fields like PageSize, LoggerName, LogInterval
}
```


而不是像社区中某些库（包括设计稿中对比的 mcp-go）那样采用可变参数选项 (variadic options) 的模式。他们认为，对于配置项较多或逻辑较复杂的情况，显式的结构体选项在可读性上更胜一筹，也使得包的公开文档更容易组织和理解。这是一个在 API 的简洁性（可变参数有时更短）与明确性和长期可维护性之间做出的典型且值得借鉴的权衡。

### Protocol Types 与 JSON Schema

MCP 协议的消息体是基于 JSON Schema 定义的。Go SDK 需要将这些 schema 映射为 Go 的结构体。设计稿中提到协议类型是从 MCP 规范的 JSON schema 生成的，并且在 mcp 包内，除非 API 用户需要，否则这些类型是未导出的。

以 content.go 中的 Content 类型为例：

```
// Content is the wire format for content.
// It represents the protocol types TextContent, ImageContent, AudioContent
// and EmbeddedResource.
type Content struct {
Type string json:"type"
Text string json:"text,omitempty"
MIMEType string json:"mimeType,omitempty"
Data []byte json:"data,omitempty"
Resource *ResourceContents json:"resource,omitempty"
Annotations *Annotations json:"annotations,omitempty"
}
func (c *Content) UnmarshalJSON(data []byte) error {
// ... custom unmarshaling logic to validate Type field ...
}
func NewTextContent(text string) *Content {
return &Content{Type: "text", Text: text}
}
// ... other constructors like NewImageContent, NewAudioContent ...
```


这里有几个值得注意的“Go 味”设计：

* **清晰的结构体定义：** 直接映射 JSON 结构，使用 json struct tag 控制序列化行为。

* **构造函数：** 提供 NewXXXContent 这样的辅助函数来创建特定类型的 Content 实例，确保 Type 字段被正确设置，提升了易用性和安全性。

* **自定义 JSON 处理：** Content 类型实现了 UnmarshalJSON 方法，用于在反序列化时对 Type 字段进行校验，确保其为协议定义的合法类型。对于 ResourceContents，它甚至实现了 MarshalJSON 来处理 Blob 字段 nil 与空切片的细微差别（为了兼容 Go 1.24 之前的 omitzero 行为）。这种在必要时介入编解码过程以保证数据正确性的做法，是 Go 类型系统能力的体现。

* **json.RawMessage 的使用：** 设计稿提到，对于用户提供的数据，SDK 会使用 json.RawMessage，这样可以将Marshal/Unmarshal的责任委托给客户端或服务器的业务逻辑。这是一种延迟解析的策略，可以提高性能，也增加了灵活性。

此外，jsonschema/ 子包提供了完整的 JSON Schema 实现，包括从 Go 类型推断 Schema (infer.go) 和校验 (validate.go)。jsonschema/generate.go (在构建时忽略) 则展示了如何从远程的 MCP JSON Schema URL 生成 protocol.go 中的 Go 类型定义，这体现了代码生成的工程实践。

### RPC 方法签名

对于 MCP 规范中定义的具体 RPC 方法，Go 团队在 SDK 中的签名设计上，将一致性和对向后兼容的执着追求体现得淋漓尽致。所有这些方法都严格遵循 func (s *SessionType) MethodName(ctx context.Context, params *XXXParams) (*XXXResult, error) 的模式。例如，在 client.go 中：

```
// ListPrompts lists prompts that are currently available on the server.
func (c *ClientSession) ListPrompts(ctx context.Context, params *ListPromptsParams) (*ListPromptsResult, error) {
return standardCall[ListPromptsResult](ctx, c.conn, methodListPrompts, params)
}
```


这里，context.Context 作为第一个参数，error 作为最后一个返回值，而参数 (*ListPromptsParams) 和结果 (*ListPromptsResult) 均使用指针类型——这些都是 Go API 设计的“黄金法则”，确保了接口风格的统一和与 Go 生态的无缝对接。

唯一的例外是 ClientSession.CallTool 方法：

```
// CallTool calls the tool with the given name and arguments.
// Pass a [CallToolOptions] to provide additional request fields.
func (c *ClientSession) CallTool(ctx context.Context, name string, args map[string]any, opts *CallToolOptions) (*CallToolResult, error) { /* ... */ }
```


为了提升用户直接调用工具时的便捷性，它接受工具的名称字符串和 map[string]any{} 类型的具体参数，以及一个可选的 *CallToolOptions，而不是要求用户预先封装一个 CallToolParams 结构体。这是一种在严格遵循模式与提升特定场景易用性之间做出的实用性调整。

设计稿中一个特别值得称道的细节，是对**向后兼容性的深思熟虑**。团队明确指出：“我们认为，任何需要调用者传递新参数的规范更改都是不向后兼容的。因此，对于当前非必需的任何 XXXParams 参数，始终可以传递 nil。”这意味着，即使未来 MCP 规范为某个方法增加了新的可选参数（这些参数会被加入到对应的 XXXParams 结构体中），现有的、传递 nil 作为参数的调用代码也无需修改，依然能够正常工作。这种对 API 演进的未雨绸缪，充分体现了 Go 团队对兼容性承诺的高度重视和丰富经验。至于为何不直接暴露完整的 JSON-RPC 请求对象，团队的考量是尽可能隐藏与业务逻辑无关的底层协议细节（如请求 ID），方法名由 Go 方法本身即可隐含，无需在参数中冗余体现，保持了 API 的纯粹性。

### 错误处理 (Errors) 与取消 (Cancellation)

在错误处理和操作取消这两个关键机制上，SDK 的设计力求透明化，并与 Go 语言的核心理念保持高度一致。除了工具处理程序自身的业务逻辑错误外，所有协议级别的错误都会被透明地处理为标准的 Go error 类型。例如，服务器端特性处理程序中发生的错误，会作为错误从 ClientSession 的相应调用中传播出来，反之亦然，使得错误处理路径清晰统一。

为了帮助上层代码更精确地理解错误的具体性质，设计稿提到协议层面的错误会包装一个 JSONRPCError 类型（其定义在 protocol.go 中自动生成），该类型能够暴露底层的 JSON-RPC 错误码，便于进行针对性的处理。

```
// (Generated in protocol.go, but conceptually similar to design doc)
type JSONRPCError struct {
Code int64 json:"code"
Message string json:"message"
Data json.RawMessage json:"data,omitempty"
}
```


而对于操作的取消，则完全依赖并无缝集成了 Go 标准的 context.Context 机制。在 transport.go 的 call 函数中，可以看到这样的逻辑：

```
// ... (inside call function)
case ctx.Err() != nil:
// Notify the peer of cancellation.
err := conn.Notify(xcontext.Detach(ctx), "notifications/cancelled", &CancelledParams{
Reason: ctx.Err().Error(),
RequestID: call.ID().Raw(),
})
return errors.Join(ctx.Err(), err)
// ...
```


当客户端代码取消一个传递给 SDK 方法的 context 时，SDK 会负责向服务器发送一个 “notifications/cancelled” 通知，同时客户端的该方法调用会立即返回 ctx.Err()。相应地，服务器端在处理该请求时，其持有的 context 会被取消，从而可以进行适当的清理或中止操作。这种设计让熟悉 Go 并发编程的开发者在处理取消逻辑时倍感亲切和自然，无需学习新的机制。

### 可扩展性：中间件模式的青睐

为了满足用户对 SDK 功能进行定制和扩展的需求，同时保持核心 API 的简洁性，Go 团队在可扩展性机制的设计上也体现了其偏好。在服务端（server.go）和客户端（client.go），都提供了 AddMiddleware 方法：

```
// In shared.go (conceptual definition)
type MethodHandler[S ClientSession | ServerSession] func(
ctx context.Context, _ *S, method string, params any) (result any, err error)
type Middleware[S ClientSession | ServerSession] func(MethodHandler[S]) MethodHandler[S]
// In server.go
func (s *Server) AddMiddleware(middleware ...Middleware[ServerSession]) { /* ... */ }
// In client.go
func (c *Client) AddMiddleware(middleware ...Middleware[ClientSession]) { /* ... */ }
```


这些方法允许用户注册一个或多个遵循特定签名的 Middleware 函数。这些函数本质上构成了 MCP 协议级别的中间件 (middleware) 链，它们会在服务器/客户端收到请求、请求被解析之后，但在进入正常的业务处理逻辑之前依次执行（从右到左应用，即第一个中间件最先执行）。mcp_test.go 中的 traceCalls 就是一个很好的示例，它展示了如何用中间件来记录请求和响应。

这种设计与 Go Web 开发（如 net/http 的 HandlerFunc 链）以及许多其他 Go 生态库中广泛采用的中间件模式一脉相承。它提供了一种强大且灵活的方式来注入横切关注点，如日志记录、认证、请求修改等。相比之下，社区的 mcp-go 实现（如设计稿中提到的）定义了多达 24 个具体的 Server Hooks，每个 Hook 对应一个特定的事件点。Go 团队的选择显然更倾向于通过一种更为通用和模式化的方式来满足扩展需求，从而避免了在核心 Server/Session 类型上暴露过多的、细粒度的钩子方法，保持了其接口的最小化和正交性。而对于像 HTTP 级别的身份验证这类与 MCP 协议本身不直接相关的横切关注点，设计稿则推荐使用标准的 HTTP 中间件模式来处理，进一步体现了关注点分离和利用现有生态成熟方案的设计思想。

通过对这些设计细节的“庖丁解牛”，我们不难发现，Go 团队在打造这个 MCP SDK 的过程中，无时无刻不在思考如何将 Go 语言的设计哲学、惯用模式以及对工程实践的深刻理解融入其中，力求在满足协议规范的完整性的同时，为 Go 开发者提供一个简洁、健壮、易用且面向未来的编程接口。

## API 设计的“Go 境界”：我们能学到什么？

Go 团队对 MCP SDK 的设计过程，如同一面镜子，映照出 API 设计的诸多考量和 Go 语言的独特气质。从中，我们可以提炼出一些宝贵的启示：

**“Go 味”始于目标：**完整性、符合惯例、健壮性、面向未来、可扩展与最小化——这些目标共同构成了设计优秀 Go API 的基石。**标准库是最好的老师：**学习并模仿 net/http, io, context 等核心库的设计模式和 API 风格，是通往“Idiomatic Go”的捷径。**接口的力量：**用小而美的接口来抽象行为、解耦组件，是 Go 设计哲学的精髓。**context 与 error 的“一等公民”地位：**在任何涉及 I/O、并发或可能失败的操作中，将它们融入 API 设计是标准做法。**向后兼容性是生命线：**API 一旦发布，就需要慎重对待变更。在设计之初就考虑未来的演进，预留扩展点，比事后打补丁要优雅得多。**权衡的艺术：**API 设计充满了权衡——简洁性与表达力、灵活性与易用性、当前需求与未来可能……没有绝对的“正确”，只有在特定上下文下的“更优”。Go 团队在包布局、配置方式等方面的选择，都体现了这种权衡。

## 小结

API 设计没有银弹，更像是一门手艺，需要在不断的实践、反思和学习中精进。Go 团队为 MCP SDK 所做的这些思考和设计决策，为我们提供了一个宝贵的学习范例，展示了如何在 Go 的世界里，打造出既满足复杂需求，又不失简洁与优雅的 API。

这种对“Go 境界”的追求——即代码不仅能工作，而且写得像 Go、用得像 Go，感觉像 Go——正是 Go 语言强大生命力和独特魅力的源泉。

希望这篇文章能为你未来的 API 设计带来一些启发。也欢迎你在评论区分享你对 API 设计的理解，或者你认为一个“好的 Go API”应该具备哪些特质。

参考资料地址：https://github.com/orgs/modelcontextprotocol/discussions/364

**精进有道，更上层楼：解锁 Go API 设计的“Go 境界”**

对今天的 Go API 设计案例意犹未尽？想系统学习，将 Go 官方的设计智慧融入你的每一个接口吗？

我在**最新上架的Go语言进阶课**中，特设 **“API 设计：构建用户喜爱、健壮可靠的公共接口”** 一讲。它将为你深入剖析 Go API设计的五大核心要素，并结合更多实战案例，助你**从“会用 Go”迈向“精通 Go”**。

**扫描下方二维码，立即开启你的进阶之旅！**

![](../../assets/ab2d7a5176ba4b48.png)


**深入探讨，加入我们！**

当然，学习的路上不孤单。关于 Go API 设计、SDK 构建、以及 MCP 协议本身等更前沿、更深入的话题，我的知识星球 **“Go & AI 精进营”** 依然是大家交流、碰撞思想的绝佳平台。

欢迎扫描下方二维码加入星球，与我和其他 Gopher 一起，在实践中成长，在讨论中精进！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论