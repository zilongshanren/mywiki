---
title: 上手MCP官方Go SDK：一份面向实战的入门指南
url: https://tonybai.com/2025/07/10/mcp-official-go-sdk/
published: '2025-07-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 上手MCP官方Go SDK：一份面向实战的入门指南

![](../../assets/9400dd6572b47b30.png)


[本文永久链接](https://tonybai.com/2025/07/10/mcp-official-go-sdk) – https://tonybai.com/2025/07/10/mcp-official-go-sdk

大家好，我是Tony Bai。

随着大型语言模型（LLM）的能力边界不断扩展，“function calling”或“tool use”已成为释放其潜力的关键。MCP（Model Context Protocol）正是为此而生，它定义了一套标准的、与模型无关的通信规范，使得任何应用都能以“工具”的形式被 LLM 调用。

长期以来，mcp官方都没有发布go-sdk，Go社区也一直在使用像[mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)这样的流行的第三方库。直到[Google Go团队安排专人协助mcp组织进行了Go SDK的设计](https://tonybai.com/2025/05/23/go-api-design-mcp-sdk)。

7月初，该Go SDK正式以modelcontextprotocol/go-sdk仓库的形式对外开源发布，这是Go 语言在这一浪潮中的一个里程碑事件。它的意义远超一个普通的库：

**标准化与权威性**：作为官方 SDK，它为 Go 开发者提供了与 MCP 规范紧密同步的、最权威的实现。这意味着更少的兼容性问题和更可靠的长期维护。**Go 语言哲学**：该 SDK 的设计充满了 Go 的味道——简洁、高效、强类型和高并发。它鼓励开发者编写惯用的 Go 代码，而不是将其他语言的范式生搬硬套过来。**生态系统的基石**：官方 SDK 的出现，将极大地促进 Go AI 生态的繁荣。开发者可以基于这个稳定的基石，构建出更复杂、更健壮的上层应用、框架和平台。

简而言之，它不仅仅是一个工具，更是 Go 语言与 AI 模型世界之间的一座标准化桥梁。

## MCP 服务架构：多种通信模式

MCP 协议设计了灵活的通信方式，以适应不同的部署场景。官方 Go SDK 对此提供了出色的支持。主要包括以下几种类型：

-
**标准输入/输出 (Stdio)**：这是最简单的模式，客户端通过启动一个子进程（MCP Server），并通过其 stdin 和 stdout 进行 JSON-RPC 通信。这种模式非常适合本地工具、CLI 插件或 Sidecar 模型的场景。我们将使用此模式构建**基础工具服务**和**文件系统服务**。 -
**HTTP 流式传输 (Streamable HTTP)**：这是 MCP 规范中最新、最推荐的 HTTP 模式。它通过一系列的 GET 和 POST 请求实现了一个可恢复的、无状态的会话管理机制，非常适合构建可扩展、高可用的网络服务。我们将使用此模式构建**多路复用 HTTP 服务**。 -
**服务器发送事件 (SSE)**：这是早期 MCP 规范中的一种 HTTP 模式，在社区版 SDK 中较为常见。官方 SDK 也提供了 SSEHandler 以支持这种模式，但新的 StreamableHTTPHandler 功能更强大，是未来的方向。

## 核心概念速览

尽管我们在此不深入探讨其完整的设计文档，但理解以下几个核心概念对于后续的实践至关重要：

**Server**：代表一个 MCP 服务实例。它本身是无状态的，是工具（Tools）、提示（Prompts）和资源（Resources）等能力的集合。**Client**：代表一个 MCP 客户端。**Session**：无论是 ServerSession 还是 ClientSession，它都代表一个已经建立的、具体的、有状态的连接。所有的交互都通过会话（Session）进行。**Transport**：负责建立底层通信的抽象层。它定义了客户端和服务器如何交换 JSON-RPC 消息。

Server 定义了“能做什么”，而 Session 则是“正在与谁通信”的实例。这种解耦设计为构建灵活、可扩展的服务提供了基础。

## 实战：构建三种典型的 MCP 服务

现在，让我们动手构建几个实用的 MCP 服务，来体验官方 SDK 的强大功能。

### 场景一：基础工具服务 (Greeter)

这是最经典的“Hello, World”场景，通过 stdio 运行，用于展示如何定义一个简单的工具。

**完整代码：greeter/main.go**

```
// mcp-go-sdk/greeter/main.go
package main
import (
"context"
"fmt"
"log"
"github.com/modelcontextprotocol/go-sdk/mcp"
)
// HiParams 定义了工具的输入参数，强类型保证
type HiParams struct {
Name string json:"name"
}
// SayHi 是工具的具体实现
func SayHi(ctx context.Context, _ *mcp.ServerSession, params *mcp.CallToolParamsFor[HiParams]) (*mcp.CallToolResultFor[any], error) {
resultText := fmt.Sprintf("Hi %s, welcome to the Go MCP world!", params.Arguments.Name)
return &mcp.CallToolResultFor[any]{
Content: []mcp.Content{
&mcp.TextContent{Text: resultText},
},
}, nil
}
func main() {
// 1. 创建 Server 实例
server := mcp.NewServer("greeter-server", "1.0.0", nil)
// 2. 添加工具
// NewServerTool 利用泛型和反射自动生成输入 schema
server.AddTools(
mcp.NewServerTool("greet", "Say hi to someone", SayHi),
)
// 3. 通过 StdioTransport 运行服务，它会监听标准输入/输出
log.Println("Greeter server running over stdio...")
if err := server.Run(context.Background(), mcp.NewStdioTransport()); err != nil {
log.Fatalf("Server run failed: %v", err)
}
}
```


在不依赖任何特殊客户端的情况下，我们可以通过管道向这个基于 stdio 的服务发送一系列原生的 JSON-RPC 消息，来模拟完整的客户端握手和工具调用流程。

**步骤一：运行服务并发送请求序列**

打开你的终端，执行以下命令。这行命令会使用 printf 来确保每个 JSON 对象都以换行符分隔，模拟一个完整的会话流程：

1. 发送 initialize 请求，启动会话。

2. 发送 initialized 通知，确认会话建立。

3. 发送 tools/call 请求，调用 greet 工具。

在greeter目录下执行下面命令：

```
printf '%s\n' \
'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"test-cli","version":"0.1"},"protocolVersion":"2025-03-26"}}' \
'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
'{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"greet","arguments":{"name":"Go MCP Enthusiast"}}}' \
| go run main.go
```


**预期输出：**

服务会处理这三个消息，并对两个有 ID 的请求（initialize 和 tools/call）作出响应。你将看到两个 JSON-RPC 响应对象被打印到标准输出（顺序可能会因并发处理而不同，但内容是固定的）：

```
2025/07/08 17:05:46 Greeter server running over stdio...
{"jsonrpc":"2.0","id":1,"result":{"capabilities":{"completions":{},"logging":{},"prompts":{"listChanged":true},"resources":{"listChanged":true},"tools":{"listChanged":true}},"protocolVersion":"2025-03-26","serverInfo":{"name":"greeter-server","version":"1.0.0"}}}
{"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"Hi Go MCP Enthusiast, welcome to the Go MCP world!"}]}}
```


看到这两个响应，证明我们的 Greeter 服务已经成功地完成了握手并正确响应了工具调用。

### 场景二：文件系统服务 (File System Server)

这个场景也通过 stdio 运行，展示了如何通过 Resource 机制，安全地向 LLM 暴露本地文件系统的读写能力。

```
// fileserver/main.go
package main
import (
"context"
"fmt"
"log"
"os"
"path/filepath"
"github.com/modelcontextprotocol/go-sdk/mcp"
)
func main() {
server := mcp.NewServer("filesystem-server", "1.0.0", nil)
pwd, err := os.Getwd()
if err != nil {
log.Fatalf("Failed to get current directory: %v", err)
}
log.Printf("File server serving from directory: %s", pwd)
// 使用我们自己实现的 File Handler
handler := createFileHandler(pwd)
// 添加一个虚构的资源，用于列出目录内容
server.AddResources(&mcp.ServerResource{
Resource: &mcp.Resource{
URI: "mcp://fs/list",
Name: "list_files",
Description: "List all non-directory files in the current directory.",
},
Handler: listDirectoryHandler(pwd),
})
// 添加一个资源模板，用于读取指定的文件
server.AddResourceTemplates(&mcp.ServerResourceTemplate{
ResourceTemplate: &mcp.ResourceTemplate{
Name: "read_file",
URITemplate: "file:///{+filename}",
Description: "Read a specific file from the directory. 'filename' is the relative path to the file.",
},
Handler: handler,
})
log.Println("File system server running over stdio...")
if err := server.Run(context.Background(), mcp.NewStdioTransport()); err != nil {
log.Fatalf("Server run failed: %v", err)
}
}
// createFileHandler 是一个简化的、用于演示的 ResourceHandler 工厂函数。
func createFileHandler(baseDir string) mcp.ResourceHandler {
return func(ctx context.Context, ss *mcp.ServerSession, params *mcp.ReadResourceParams) (*mcp.ReadResourceResult, error) {
// 注意：在生产环境中，这里必须调用 ss.ListRoots() 来获取客户端授权的
// 根目录，并进行严格的安全检查。
// 为了让这个入门示例能用简单的管道命令验证，我们暂时省略了这个双向调用。
requestedPath := filepath.Join(baseDir, filepath.FromSlash(params.URI[len("file:///"):]))
data, err := os.ReadFile(requestedPath)
if err != nil {
if os.IsNotExist(err) {
return nil, mcp.ResourceNotFoundError(params.URI)
}
return nil, fmt.Errorf("failed to read file: %w", err)
}
return &mcp.ReadResourceResult{
Contents: []*mcp.ResourceContents{
{URI: params.URI, MIMEType: "text/plain", Text: string(data)},
},
}, nil
}
}
// listDirectoryHandler 是一个自定义的 ResourceHandler，用于实现列出目录的功能
func listDirectoryHandler(dir string) mcp.ResourceHandler {
return func(ctx context.Context, ss *mcp.ServerSession, params *mcp.ReadResourceParams) (*mcp.ReadResourceResult, error) {
// 同样，为简化本地验证，暂时省略对 ss.ListRoots() 的调用。
entries, err := os.ReadDir(dir)
if err != nil {
return nil, fmt.Errorf("failed to read directory: %w", err)
}
var fileList string
for _, e := range entries {
if !e.IsDir() {
fileList += e.Name() + "\n"
}
}
if fileList == "" {
fileList = "(The directory is empty or contains no files)"
}
return &mcp.ReadResourceResult{
Contents: []*mcp.ResourceContents{
{URI: params.URI, MIMEType: "text/plain", Text: fileList},
},
}, nil
}
}
```


文件服务同样需要完整的握手流程。我们将用与上面类似的方式来验证其功能。

**步骤一：准备测试文件**

首先，在你的项目根目录下创建一个简单的文本文件。

```
echo "Hello from the File System MCP Server!" > my-test-file.txt
```


**步骤二：验证“列出文件”功能**

我们发送包含 initialize、initialized 和 resources/read 的请求序列。

在fileserver下执行下面命令：

```
printf '%s\n' \
'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"test-cli","version":"0.1"},"protocolVersion":"2025-03-26"}}' \
'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
'{"jsonrpc":"2.0","id":2,"method":"resources/read","params":{"uri":"mcp://fs/list"}}' \
| go run main.go
```


**预期输出：**

你将看到 initialize 的响应，以及 resources/read 的响应，后者包含了目录文件列表。

```
2025/07/08 18:13:47 File system server running over stdio...
{"jsonrpc":"2.0","id":1,"result":{"capabilities":{"completions":{},"logging":{},"prompts":{"listChanged":true},"resources":{"listChanged":true},"tools":{"listChanged":true}},"protocolVersion":"2025-03-26","serverInfo":{"name":"filesystem-server","version":"1.0.0"}}}
{"jsonrpc":"2.0","id":2,"result":{"contents":[{"uri":"mcp://fs/list","mimeType":"text/plain","text":"go.mod\ngo.sum\nmain.go\nmy-test-file.txt\n"}]}}
```


**步骤三：验证“读取文件”功能**

现在，我们发送请求序列来读取 my-test-file.txt 的内容。

```
printf '%s\n' \
'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"test-cli","version":"0.1"},"protocolVersion":"2025-03-26"}}' \
'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
'{"jsonrpc":"2.0","id":3,"method":"resources/read","params":{"uri":"file:///my-test-file.txt"}}' \
| go run main.go
```


**预期输出：**

除了 initialize 的响应外，你将看到包含文件内容的 resources/read 响应。

```
2025/07/08 18:15:12 File server serving from directory: /Users/tonybai/go/src/github.com/bigwhite/experiments/mcp-go-sdk/fileserver
2025/07/08 18:15:12 File system server running over stdio...
{"jsonrpc":"2.0","id":1,"result":{"capabilities":{"completions":{},"logging":{},"prompts":{"listChanged":true},"resources":{"listChanged":true},"tools":{"listChanged":true}},"protocolVersion":"2025-03-26","serverInfo":{"name":"filesystem-server","version":"1.0.0"}}}
{"jsonrpc":"2.0","id":3,"result":{"contents":[{"uri":"file:///my-test-file.txt","mimeType":"text/plain","text":"Hello from the File System MCP Server\n"}]}}
```


**步骤四：清理**

测试完成后，可以删除测试文件。

```
rm my-test-file.txt
```


### 场景三：多路复用 HTTP 服务 (Multi-Service HTTP Server)

这个场景展示了如何使用 StreamableHTTPHandler 在单个 HTTP 端点上提供多个不同的 MCP 服务。

**完整代码：httpserver/main.go**

```
package main
import (
"context"
"fmt"
"log"
"net/http"
"github.com/modelcontextprotocol/go-sdk/mcp"
)
// HiParams 和 SayHi 函数与场景一相同
type HiParams struct{ Name string json:"name" }
func SayHi(ctx context.Context, _ *mcp.ServerSession, params *mcp.CallToolParamsFor[HiParams]) (*mcp.CallToolResultFor[any], error) {
resultText := fmt.Sprintf("Hi %s, this response is from the HTTP server!", params.Arguments.Name)
return &mcp.CallToolResultFor[any]{
Content: []mcp.Content{&mcp.TextContent{Text: resultText}},
}, nil
}
// AddParams 和 Add 工具的实现
type AddParams struct{ A, B int }
func Add(_ context.Context, _ *mcp.ServerSession, params *mcp.CallToolParamsFor[AddParams]) (*mcp.CallToolResultFor[any], error) {
result := params.Arguments.A + params.Arguments.B
return &mcp.CallToolResultFor[any]{
Content: []mcp.Content{&mcp.TextContent{Text: fmt.Sprintf("The sum is: %d", result)}},
}, nil
}
func main() {
// 1. 创建 Greeter 服务实例
greeterServer := mcp.NewServer("greeter-service", "1.0", nil)
greeterServer.AddTools(mcp.NewServerTool("greet", "Say hi", SayHi))
// 2. 创建 Math 服务实例
mathServer := mcp.NewServer("math-service", "1.0", nil)
mathServer.AddTools(mcp.NewServerTool("add", "Add two integers", Add))
// 3. 创建 StreamableHTTPHandler
handler := mcp.NewStreamableHTTPHandler(func(request *http.Request) *mcp.Server {
log.Printf("Routing request for URL: %s\n", request.URL.Path)
switch request.URL.Path {
case "/greeter":
return greeterServer
case "/math":
return mathServer
default:
return nil // 返回 nil 将导致 404 Not Found
}
}, nil)
// 4. 启动标准的 Go HTTP 服务器
addr := ":8080"
log.Printf("Multi-service MCP server listening at http://localhost%s\n", addr)
if err := http.ListenAndServe(addr, handler); err != nil {
log.Fatalf("HTTP server failed: %v", err)
}
}
```


与基于 stdio 的简单服务不同，验证 Streamable HTTP 服务使用 curl 等工具会非常繁琐。这是因为 MCP 是一个有状态的协议，要求客户端在发送工具调用之前，必须先完成一个包含 initialize 请求和 initialized 通知的多步“握手”流程来建立会话。

一个简单的 curl 命令无法管理这种有状态的交互。因此，最理想的验证方式是使用一个真正的 MCP 客户端。我们将在下一节构建这样一个客户端——agent，然后用集成了大模型的它来统一验证我们创建的所有三个服务，包括这个 HTTP 服务。

## 集成大模型：让 Go Agent 直接成为 MCP 客户端

在前面的章节中，我们成功构建了三种不同类型的 MCP 服务。现在，是时候将它们与 AI 大模型（以 DeepSeek 为例）集成，构建一个能够调度这些mcp server工具的智能 Agent 了。

一个常见的思路可能是创建一个通用的命令行工具（CLI）来调用这些服务，然后让我们的 Go Agent 程序去执行这个 CLI。然而，既然我们的 Agent 本身就是用 Go 编写的，一个更优雅、更高效、更符合 Go 语言习惯的方式是：**让 Agent 程序直接导入 modelcontextprotocol/go-sdk，将自己作为原生的 MCP 客户端来与服务通信。**

这种方法避免了不必要的进程开销和数据序列化，使得整个系统更加内聚和高性能。接下来，我们将编写这样一个 Go Agent。

### Part 1: 编写 Go Agent 程序

这个程序将承担所有角色：它既是与 DeepSeek 模型对话的主循环，也是调用我们 MCP 服务的客户端。

**准备工作**：

- 安装 OpenAI Go SDK：go get github.com/openai/openai-go
- 获取 DeepSeek API Key，并设置为环境变量：export DEEPSEEK_API_KEY=”your-api-key”

**完整代码：agent/main.go**

```
// agent/main.go
package main
import (
"context"
"encoding/json"
"fmt"
"log"
"os"
"os/exec"
"strings"
"github.com/modelcontextprotocol/go-sdk/mcp"
"github.com/openai/openai-go"
"github.com/openai/openai-go/option"
)
// serverConfig 结构体用于管理不同 MCP 服务的连接信息
type serverConfig struct {
ServerCmd string // 用于 stdio 服务
HTTPAddr string // 用于 http 服务
}
// toolRegistry 映射对 LLM 友好的工具别名到其服务配置
var toolRegistry = map[string]serverConfig{
"greet": {ServerCmd: "go run ../greeter/main.go"},
"add": {HTTPAddr: "http://localhost:8080/math"},
"list_files": {ServerCmd: "go run ../fileserver/main.go"},
"read_file": {ServerCmd: "go run ../fileserver/main.go"},
}
// invokeMCPTool 是 Agent 的核心函数，负责直接与 MCP 服务通信
func invokeMCPTool(toolAlias string, arguments map[string]interface{}) (string, error) {
config, ok := toolRegistry[toolAlias]
if !ok {
return "", fmt.Errorf("unknown tool alias: %s", toolAlias)
}
// 1. 将 LLM 友好的别名和参数，转换为真正的 MCP 请求
mcpToolName := toolAlias
mcpArguments := arguments
if toolAlias == "list_files" {
mcpToolName = "resources/read"
mcpArguments = map[string]interface{}{"uri": "mcp://fs/list"}
} else if toolAlias == "read_file" {
mcpToolName = "resources/read"
if filename, ok := arguments["filename"].(string); ok {
mcpArguments = map[string]interface{}{"uri": "file:///" + filename}
} else {
return "", fmt.Errorf("tool 'read_file' requires a 'filename' argument")
}
}
// 2. 创建 MCP 客户端实例
client := mcp.NewClient("go-agent", "1.0", nil)
// 3. 根据配置选择并创建 Transport
var transport mcp.Transport
if config.ServerCmd != "" {
cmdParts := strings.Fields(config.ServerCmd)
transport = mcp.NewCommandTransport(exec.Command(cmdParts[0], cmdParts[1:]...))
} else {
transport = mcp.NewStreamableClientTransport(config.HTTPAddr, nil)
}
// 4. 授权客户端访问本地文件系统（仅对文件服务调用有效）
client.AddRoots(&mcp.Root{URI: "file://./"})
// 5. 连接到服务器，建立会话
ctx := context.Background()
session, err := client.Connect(ctx, transport)
if err != nil {
return "", fmt.Errorf("failed to connect to MCP server for tool %s: %w", toolAlias, err)
}
defer session.Close() // 每次调用都是一个独立的会话，确保关闭
// 6. 执行调用并处理结果
var resultText string
if mcpToolName == "resources/read" {
res, err := session.ReadResource(ctx, &mcp.ReadResourceParams{
URI: mcpArguments["uri"].(string),
})
if err != nil {
return "", fmt.Errorf("ReadResource failed: %w", err)
}
var sb strings.Builder
for _, c := range res.Contents {
sb.WriteString(c.Text)
}
resultText = sb.String()
} else {
res, err := session.CallTool(ctx, &mcp.CallToolParams{
Name: mcpToolName,
Arguments: mcpArguments,
})
if err != nil {
return "", fmt.Errorf("CallTool failed: %w", err)
}
if res.IsError {
return "", fmt.Errorf("tool execution failed: %s", res.Content[0].(*mcp.TextContent).Text)
}
resultText = res.Content[0].(*mcp.TextContent).Text
}
return resultText, nil
}
func main() {
apiKey := os.Getenv("DEEPSEEK_API_KEY")
if apiKey == "" {
log.Fatal("DEEPSEEK_API_KEY environment variable not set.")
}
client := openai.NewClient(
option.WithAPIKey(apiKey),
option.WithBaseURL("https://api.deepseek.com/v1"),
)
// 为所有工具使用合法的名称，特别是为 resources/read 创建别名
tools := []openai.ChatCompletionToolParam{
{
Function: openai.FunctionDefinitionParam{
Name: "greet",
Description: openai.String("Say hi to someone."),
Parameters: openai.FunctionParameters{
"type": "object", "properties": map[string]interface{}{"name": map[string]string{"type": "string", "description": "Name of the person to greet"}}, "required": []string{"name"},
},
},
},
{
Function: openai.FunctionDefinitionParam{
Name: "add",
Description: openai.String("Add two integers."),
Parameters: openai.FunctionParameters{
"type": "object", "properties": map[string]interface{}{"A": map[string]string{"type": "integer"}, "B": map[string]string{"type": "integer"}}, "required": []string{"A", "B"},
},
},
},
{
Function: openai.FunctionDefinitionParam{
Name: "list_files",
Description: openai.String("List all non-directory files in the current project directory."),
Parameters: openai.FunctionParameters{"type": "object", "properties": map[string]interface{}{}},
},
},
{
Function: openai.FunctionDefinitionParam{
Name: "read_file",
Description: openai.String("Read the content of a specific file."),
Parameters: openai.FunctionParameters{
"type": "object", "properties": map[string]interface{}{"filename": map[string]string{"type": "string", "description": "The name of the file to read."}}, "required": []string{"filename"},
},
},
},
}
messages := []openai.ChatCompletionMessageParamUnion{
openai.SystemMessage("You are a helpful assistant with access to local tools. You must call tools by using the tool_calls response format. Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."),
openai.UserMessage("Hi, can you greet my friend Alex, add 5 and 7, and then list the files in my project?"),
}
ctx := context.Background()
for i := 0; i < 5; i++ {
log.Println("--- Sending request to DeepSeek ---")
resp, err := client.Chat.Completions.New(ctx, openai.ChatCompletionNewParams{Model: "deepseek-chat", Messages: messages, Tools: tools})
if err != nil {
log.Fatalf("ChatCompletion error: %v\n", err)
}
if len(resp.Choices) == 0 {
log.Fatal("No choices returned from API")
}
msg := resp.Choices[0].Message
messages = append(messages, msg.ToParam())
if msg.ToolCalls != nil {
for _, toolCall := range msg.ToolCalls {
functionName := toolCall.Function.Name
var arguments map[string]interface{}
if err := json.Unmarshal([]byte(toolCall.Function.Arguments), &arguments); err != nil {
log.Fatalf("Failed to unmarshal function arguments: %v", err)
}
log.Printf("--- LLM wants to call tool: %s with args: %v ---\n", functionName, arguments)
// 直接调用我们的 Go 函数，该函数内建了 MCP 客户端逻辑
toolResult, err := invokeMCPTool(functionName, arguments)
if err != nil {
log.Printf("Tool call failed: %v\n", err)
toolResult = fmt.Sprintf("Error executing tool: %v", err)
}
log.Printf("--- Tool result: ---\n%s\n---------------------\n", toolResult)
messages = append(messages, openai.ToolMessage(toolResult, toolCall.ID))
}
continue
}
log.Println("--- Final response from LLM ---")
log.Println(msg.Content)
return
}
log.Println("Reached max conversation turns.")
}
```


注：上述代码使用了OpenAI的function calling api，不过即便不用function calling api，通过prompt依然可以实现mcp server接口的调用(需要自行解析response)，大家可以自行实现一下。


### Part 2: 集成验证

现在，我们的 agent 程序已经是一个功能齐全的、内建了 MCP 客户端的智能体。让我们来验证它的工作流程。

-
**启动 httpserver**：

agent 会通过 HTTP 调用 math 服务，所以我们必须先在后台运行它。`go run ./httpserver/main.go & HTTP_PID=$!`

-
**创建测试文件**：

为文件服务准备一个可供读取的文件。`echo "This file will be read by our Go AI Agent." > agent-test.txt`

-
**运行 agent 程序**：

确保你的 DEEPSEEK_API_KEY 已经设置。`go run ./agent/main.go`


**预期的输出流程**:

你的终端将清晰地展示 AI Agent 的思考和行动链。它直接在内部与各个 MCP 服务进行高效的 Go-to-Go通信。

```
$DEEPSEEK_API_KEY=<your_deepseek_api_key> go run main.go
2025/07/08 19:17:42 --- Sending request to DeepSeek ---
2025/07/08 19:17:53 --- LLM wants to call tool: greet with args: map[name:Alex] ---
2025/07/08 19:17:53 --- Tool result: ---
Hi Alex, welcome to the Go MCP world!
---------------------
2025/07/08 19:17:53 --- LLM wants to call tool: add with args: map[A:5 B:7] ---
2025/07/08 19:17:53 --- Tool result: ---
The sum is: 12
---------------------
2025/07/08 19:17:53 --- LLM wants to call tool: list_files with args: map[] ---
2025/07/08 19:17:53 --- Tool result: ---
go.mod
go.sum
main.go
---------------------
2025/07/08 19:17:53 --- Sending request to DeepSeek ---
2025/07/08 19:18:07 --- Final response from LLM ---
2025/07/08 19:18:07 Here's what you asked for:
1. **Greeting for Alex**: Hi Alex, welcome to the Go MCP world!
2. **Addition of 5 and 7**: The sum is 12.
3. **Files in your project**:
- go.mod
- go.sum
- main.go
Let me know if you'd like to do anything else!
```


最后，做一下清理工作：

```
kill $HTTP_PID
rm agent-test.txt
```


## 小结

通过本次从零到一的实践，我们不仅学习了如何使用 modelcontextprotocol/go-sdk 构建支持不同通信协议的 MCP 服务，更重要的是，我们探索并实现了将 Go Agent 程序**直接作为原生 MCP 客户端**的实践。

这种直接通过库调用的内聚架构，相比于通过外部 CLI 工具进行解耦的方式，充分发挥了 Go 语言的优势：

**高性能**：避免了不必要的进程创建和数据序列化开销，使得工具调用和响应链条更短、更高效。**强类型与健壮性**：整个调用链路都在 Go 的类型系统内完成，错误处理清晰，代码更易于维护和调试。**简洁的工程实现**：它展示了一种更加优雅和符合 Go 语言习惯的工程模式，让 AI Agent 的构建过程如同编写任何一个普通的 Go 应用一样自然。

modelcontextprotocol/go-sdk 不仅仅是一个协议的实现，它更像一个宣言：Go 语言凭借其出色的并发模型、强大的类型系统和简洁的工程哲学，完全有能力成为构建下一代高性能、高可靠性 AI Agent 和工具化应用的首选后端语言。

虽然官方 SDK 仍在快速迭代中，但其展现出的潜力和清晰的设计哲学已经足够令人振奋。我们鼓励所有对 Go 和 AI 结合感兴趣的开发者，立即上手体验。这个 SDK 无疑将成为连接你的 Go 程序与广阔智能模型世界之间最坚固、最标准的桥梁。

本文涉及源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/mcp-go-sdk)下载。

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论