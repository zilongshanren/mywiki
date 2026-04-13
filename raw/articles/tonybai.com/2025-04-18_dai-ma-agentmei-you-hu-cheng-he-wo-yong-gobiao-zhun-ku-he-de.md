---
title: 代码Agent没有护城河？我用Go标准库和DeepSeek证明给你看！
url: https://tonybai.com/2025/04/18/reproduce-thorsten-balls-code-agent/
published: '2025-04-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 代码Agent没有护城河？我用Go标准库和DeepSeek证明给你看！

![](../../assets/2d2b90ebca5d8a06.jpg)


[本文永久链接](https://tonybai.com/2025/04/18/reproduce-thorsten-balls-code-agent) – https://tonybai.com/2025/04/18/reproduce-thorsten-balls-code-agent

大家好，我是Tony Bai。

人工智能Agent风头正劲，但构建它们真的那么难吗？本文深入解读Thorsten Ball 的“皇帝新衣”论，并通过一个 Go 标准库 + OpenAI Compatible API + DeepSeek的实战复现，揭示代码编辑 Agent 的核心简洁性，探讨真正的挑战与机遇。

## 引言：AI Agent 的神秘光环与现实

近来，AI Agent（人工智能代理）无疑是技术圈最炙手可热的话题之一。从能自主编码的软件工程师，到能规划执行复杂任务的智能助手，Agent 展现出的潜力令人兴奋。但与此同时，它们往往被一层神秘的光环笼罩，许多人觉得构建一个真正能工作的 Agent，尤其是能与代码交互、编辑文件的 Agent，必然涉及极其复杂的技术和深不可测的“炼金术”。

事实果真如此吗？Agent 的核心真的那么难以企及吗？

## 戳破泡沫：Thorsten Ball 的“皇帝新衣”论

著名开发者、“Writing A Compiler In Go”和“Writing An Interpreter In Go”两本高质量大作的作者Thorsten Ball最近发表了一篇振聋发聩的文章——《[How To Build An Agent](https://ampcode.com/how-to-build-an-agent)》（如何构建一个Agent），副标题更是直言不讳：“The Emperor Has No Clothes”（皇帝没有穿衣服）。

Thorsten 的核心观点非常清晰：构建一个功能齐全、能够编辑代码的 Agent，其核心原理并不神秘，甚至可以说**没有所谓的“护城河”**。他认为，那些看似神奇的 Agent（自动编辑文件、运行命令、从错误中恢复、尝试不同策略）背后并没有什么惊天秘密。

其**核心不过是：一个强大的大语言模型 (LLM) + 一个循环 (Loop) + 足够的上下文额度 (Tokens) + 工具调用 (Tools)**。

而那些让Agent产品（如Cursor等）令人印象深刻、甚至上瘾的特性，更多来自于务实的工程实践和大量的**“体力活” (Elbow Grease)**——UI 设计、编辑器集成、错误处理、提示词工程、工具链优化等等。

为了证明核心逻辑的简单性，Thorsten 在文章中手把手地用**不到 400 行 Go 代码**，基于Anthropic Claude模型和其[Go SDK](https://github.com/anthropics/anthropic-sdk-go)，实现了一个具备基本代码编辑能力的Agent Demo。这个Demo 包含了三个关键的工具：

**read_file**: 读取文件内容。**list_files**: 列出目录内容。**edit_file**: 编辑文件内容——令人惊讶的是，这个核心的编辑功能，其实现方式极其基础，仅仅是基于**字符串替换**！

就是这样一个看似“简陋”的Agent，却能在实验中成功完成创建JavaScript文件、修改代码逻辑、解码字符串等任务，展现了自主规划和调用工具的能力。

## 不止于理论：我们用标准库 + OpenAI Compatible API + DeepSeek复现并验证！

Thorsten 的文章和示例极具启发性。但为了进一步验证其观点的普适性(其实主要是我没有Claude的API key)——即这种 Agent 的核心逻辑是否独立于特定的 LLM 提供商或 SDK——我们进行了一项挑战：

**在不使用任何第三方 LLM SDK 的情况下，仅依靠Go标准库 (net/http, encoding/json 等)，将 Thorsten 的示例移植到使用通用的 OpenAI Compatible API(主要是Chat Completions API)。**

这意味着我们需要：

- 手动构建 HTTP 请求。
- 处理 API 认证 (Bearer Token)。
- 定义匹配 OpenAI API 格式的 Go 结构体。
- 处理 JSON 的序列化与反序列化。
- 实现 OpenAI 的工具调用 (Tool Calling) 规范，包括函数定义、参数传递和结果返回。

经过一番努力，我们成功了！这个纯标准库版本的 Go Agent 不仅编译通过，而且**完美地复现了 Thorsten 文章中的所有实验**，无论是文件读写、列表，还是代码创建与修改，其行为和效果与原版几乎一致。

这有力地证明了：**代码 Agent 的核心交互范式（请求 -> LLM 思考/工具调用 -> 执行工具 -> 返回结果 -> LLM 再思考…）确实是通用的，不依赖于特定的 SDK 或 API 提供商。** 掌握了底层的 HTTP 通信和 API 协议规范，用任何语言、任何网络库都可以构建类似的核心。

## 亲手体验：一步步复现你的代码编辑Agent

![](../../assets/c11b96f73e3e222c.jpg)


理论和别人的成功固然鼓舞人心，但亲手实践才能带来最真切的感受。“纸上得来终觉浅，绝知此事要躬行”。下面，我们将结合关键代码片段，指导你一步步复现这个使用 Go 标准库和 OpenAI Compatible API 构建的代码编辑 Agent 实验。

**(注意：你需要准备一个 OpenAI API Key 或其他兼容 OpenAI API 的服务商提供的 Key 和 Endpoint，我这里使用的是兼容OpenAI API的DeepSeek的deepseek-chat大模型。此外，这里展示的是关键代码片段，完整代码请参考 code-editing-agent-deepseek)**

**准备工作:**

**环境配置:**确保安装 Go 环境。设置环境变量 OPENAI_API_KEY，以及可选的 OPENAI_API_BASE (兼容 API 地址) 和 OPENAI_MODEL (模型名称，如 gpt-4o, gpt-3.5-turbo, 或其他兼容模型，比如deepseek-chat等)。**获取并运行代码:**将完整的 main.go 代码保存到 code-editing-agent 目录，执行 go mod tidy 下载依赖。- 设置环境变量(见下面)，然后运行 go run main.go 启动 Agent。你应该看到程序启动并等待你的输入。

```
$export OPENAI_API_KEY=<your_deepseek_api_key>
$export OPENAI_API_BASE=https://api.deepseek.com
$export OPENAI_MODEL=deepseek-chat
```


### 实验 0：基础对话 (验证连接)

**目标:**验证 Agent 与 LLM API 的基本连接和对话流程是否正常，此时不涉及工具调用。**关键代码 (简化流程):**Agent 的核心 Run 方法会接收用户输入，将其添加到 conversation 历史中，然后调用 callOpenAICompletion，最后处理并打印 AI 的文本回复。

```
// Simplified flow within Agent.Run for basic chat
func (a *Agent) Run(ctx context.Context) error {
// ... setup ...
conversation := []OpenAIChatCompletionMessage{ /* system prompt */ }
for { // Outer loop for user input
// ... get userInput from console ...
conversation = append(conversation, OpenAIChatCompletionMessage{Role: "user", Content: userInput})
// --- Call API ---
resp, err := a.callOpenAICompletion(ctx, conversation)
if err != nil {
fmt.Printf("\u001b[91mAPI Error\u001b[0m: %s\n", err.Error())
continue // Let user try again
}
if len(resp.Choices) == 0 { /* handle no choices */ continue }
assistantMessage := resp.Choices[0].Message
conversation = append(conversation, assistantMessage) // Add response to history
// --- Print Text Response ---
if assistantMessage.Content != "" {
fmt.Printf("\u001b[93mAI\u001b[0m: %s\n", assistantMessage.Content)
}
// --- Tool Handling Logic would go here, but skipped for basic chat ---
// In a basic chat without tool calls, the inner loop (if any) breaks immediately.
} // End of outer loop
return nil
}
```


**解释:**这一步主要测试 callOpenAICompletion 函数能否成功打包对话历史、发送 HTTP 请求到 API 端点、接收有效的文本响应，并由 Run 方法将其打印出来。-
**步骤:**-
在 You: 提示符后输入：

You: Hey! I'm Tony! How are you?

-
观察 AI 是否能正常回复，确认 API 连接。


-
-
**Agent输出:**

```
$./agent
Chat with AI (use 'ctrl-c' to quit)
You: Hey! I'm Tony! How are you?
AI: Hi Tony! I'm just a program, so I don't have feelings, but I'm here and ready to help you with anything you need. How can I assist you today?
```


### 实验 1 & 2：read_file 工具 (读取文件)

**目标:**测试 Agent 调用 read_file 工具读取指定文件内容的能力。**关键代码:**

工具定义 (ReadFileDefinition): 告诉AI 有一个名为 read_file 的工具，它需要一个path参数，并描述了其功能。

```
type ReadFileInput struct { // Defines the input structure for the tool
Path string json:"path" jsonschema_description:"The relative path..." jsonschema:"required"
}
var ReadFileDefinition = ToolDefinition{
Name: "read_file",
Description: "Read the contents of a given relative file path...",
InputSchema: GenerateSchema[ReadFileInput](), // Generates {"type": "object", "properties": {"path": {"type": "string", ...}}, "required": ["path"]}
Function: ReadFile, // Links to the Go function below
}
```


工具执行函数 (ReadFile): 这个 Go 函数接收 AI 提供的参数（文件路径），并使用标准库 os.ReadFile 实际执行文件读取。

```
func ReadFile(input json.RawMessage) (string, error) {
readFileInput := ReadFileInput{}
err := json.Unmarshal(input, &readFileInput) // Parse the JSON arguments from AI
if err != nil || readFileInput.Path == "" { /* handle parse error or missing path */ }
content, err := os.ReadFile(readFileInput.Path) // Use Go standard library to read file
if err != nil { /* handle file read error */ }
return string(content), nil // Return file content as a string
}
```


**解释:**当用户请求涉及文件内容时，AI 会根据 ReadFileDefinition 的描述，决定调用 read_file 工具，并提供 path 参数。Agent 的 Run 循环捕获到这个工具调用请求，找到对应的 ReadFile 函数，传入参数并执行。函数读取文件后返回内容字符串，这个字符串会被包装成 role: tool 的消息发送回给 AI，AI 再根据文件内容生成最终答复。**步骤 (实验 1 – secret-file.txt):**- 准备: 创建 secret-file.txt 文件，内容为“what animal is the most disagreeable because it always says neigh?”
- 输入: buddy, help me solve the riddle in the secret-file.txt file
- 观察: AI 回复 -> Tool Call: read_file({“path”:”secret-file.txt”}) -> AI 给出谜底。
- Agent输出:


```
You: buddy, help me solve the riddle in the secret-file.txt file
Tool Call: list_files({})
Tool Call: read_file({"path":"secret-file.txt"})
AI: The answer to the riddle is a **horse**, because it always says "neigh" (which sounds like "nay," meaning disagreement).
Let me know if you need help with anything else, Tony!
```


**步骤 (实验 2 – 读取main.go):**- 输入: What’s going on in main.go? Be brief!
- 观察: AI 回复 -> Tool Call: read_file({“path”:”main.go”}) -> AI 给出代码摘要。
- 模型输出:


```
You: What's going on in main.go? Be brief!
Tool Call: read_file({"path":"main.go"})
AI: The `main.go` file is a Go program that sets up an **AI agent** capable of interacting with the local filesystem (reading, listing, and editing files). Here's a brief breakdown:
1. **Purpose**:
- The agent acts as a helper, responding to user requests by either providing text answers or using tools to interact with files.
2. **Key Features**:
- **Tools**: It has three built-in tools:
- `read_file`: Reads file contents.
- `list_files`: Lists files/directories.
- `edit_file`: Edits or creates files.
- **OpenAI Integration**: Uses the OpenAI API (like GPT-4) to process user input and decide when to use tools.
- **Interactive CLI**: Takes user input from the command line and displays responses.
3. **Workflow**:
- The agent maintains a conversation history with the user.
- If a tool is needed, it calls the OpenAI API, executes the tool, and updates the conversation.
4. **Dependencies**:
- Requires an `OPENAI_API_KEY` environment variable to work with the OpenAI API.
In short, it's a **file-system assistant powered by OpenAI**, designed to help with file operations via natural language commands. Let me know if you'd like more details!
```


### 实验 3：list_files 工具

**目标:**测试 list_files 工具，让 AI 感知当前工作目录的文件结构。**关键代码:**

**工具定义 (ListFilesDefinition)**: 定义 list_files 工具，路径参数可选。

```
type ListFilesInput struct { // Input structure, path is optional
Path string json:"path,omitempty" jsonschema_description:"Optional relative path..."
}
var ListFilesDefinition = ToolDefinition{
Name: "list_files",
Description: "List files and directories at a given path. If no path...",
InputSchema: GenerateSchema[ListFilesInput](),
Function: ListFiles, // Links to the Go function below
}
```


**工具执行函数 (ListFiles)**: 使用 filepath.WalkDir 遍历目录，并将结果格式化为 JSON 数组字符串。

```
func ListFiles(input json.RawMessage) (string, error) {
// ... Parse optional path from input ...
dir := "." // Default to current directory
if listFilesInput.Path != "" { dir = listFilesInput.Path }
var files []string
err := filepath.WalkDir(dir, func(...) error { // Use standard library WalkDir
// ... build relative path ...
// ... append path to files slice (add "/" for directories) ...
return nil
})
if err != nil { /* handle walk error */ }
result, err := json.Marshal(files) // Return as JSON array string
if err != nil { /* handle marshal error */ }
return string(result), nil
}
```


**解释:**AI 被问及目录内容时，会调用 list_files 工具（通常不带参数，使用默认当前目录）。Go 代码执行 ListFiles 函数，遍历目录，将文件和目录名（目录带 /）的列表打包成 JSON 字符串返回给 AI。AI 再将这个列表呈现给用户。**步骤:**- 输入: what do you see in this directory?
- 观察: AI 回复 -> Tool Call: list_files({}) -> AI 列出当前目录文件。
- Agent输出：


```
You: what do you see in this directory?
Tool Call: list_files({})
AI: Here’s what’s in the current directory:
1. **Files**:
- `.main.go.swp` (likely a temporary swap file for `main.go`).
- `go.mod` and `go.sum` (Go module files for dependency management).
- `main.go` (the main Go program file).
- `secret-file.txt` (the file with the riddle you solved earlier).
2. **Directory**:
- `agent/` (a subdirectory, possibly containing agent-related code or resources).
Let me know if you'd like to explore any of these further!
```


### 实验 4 & 5：组合工具 (list_files + read_file)

**目标:**观察 Agent 如何自主地组合使用多个工具（先 list_files 发现文件，再 read_file 读取特定文件）来完成更复杂的任务。**关键代码 (Agent 的 Run 方法中的内部循环):**这是实现多步工具调用的核心。

```
// Inside Agent.Run method
for { // Outer loop for user input
// ... get user input, add to conversation ...
for { // <--- INNER LOOP: Handles multi-turn tool calls ---
resp, err := a.callOpenAICompletion(ctx, conversation) // Call API
// ... handle response ...
assistantMessage := resp.Choices[0].Message
conversation = append(conversation, assistantMessage) // Add assistant's response
// Check for tool calls in the response
if len(assistantMessage.ToolCalls) == 0 {
// No tools called by AI in this turn. Print text response (if any)
// and break the INNER loop to wait for next user input.
if assistantMessage.Content != "" { /* print content */ }
break // Exit INNER loop
}
// --- AI requested tools, execute them ---
toolResults := []OpenAIChatCompletionMessage{}
for _, toolCall := range assistantMessage.ToolCalls {
// ... find tool definition by toolCall.Function.Name ...
// ... execute the tool's Go function with toolCall.Function.Arguments ...
// ... prepare resultMsg (role: "tool", content: output/error) ...
toolResults = append(toolResults, resultMsg)
}
conversation = append(conversation, toolResults...) // Add tool results to history
// DO NOT BREAK! Continue the INNER loop immediately.
// The conversation now includes the tool results,
// so the next call to callOpenAICompletion will send them back to the AI.
} // <--- End of INNER LOOP ---
} // End of OUTER loop
```


-
**解释:**关键在于内部循环 (INNER LOOP)。当 AI 的回复包含 ToolCalls 时，Agent 会：- 执行所有请求的工具。
- 将每个工具的执行结果（成功输出或错误信息）构造成 role: “tool” 的消息。
- 将这些 tool 消息
**添加**到对话历史 conversation 中。 **不退出内部循环**，而是立即用更新后的 conversation（现在包含了工具结果）**再次调用**callOpenAICompletion。

这样，AI 就能在其下一步的思考中“看到”刚刚执行的工具结果，并据此决定是继续调用工具、生成最终答案，还是进行其他操作。这个循环会持续到 AI 的某次响应不再包含 ToolCalls 为止。

-
**步骤 (实验 4 – Go 文件信息):**- 输入: Tell me about all the Go files in here. Be brief!
- 观察: list_files -> AI 回复 -> read_file (main.go) -> AI 回复 -> read_file (go.mod) -> AI 回复 -> AI 最终汇总。
- Agent输出：


```
You: Tell me about all the Go files in here. Be brief!
AI: Here’s a quick rundown of the Go files in the directory:
1. **`main.go`**:
- The core program file. It sets up an **AI agent** that interacts with the local filesystem using tools (`read_file`, `list_files`, `edit_file`).
- Integrates with the **OpenAI API** for natural language processing.
- Handles user input via the command line.
2. **`go.mod` & `go.sum`**:
- **`go.mod`**: Defines the Go module (project) and its dependencies (e.g., `github.com/invopop/jsonschema` for JSON schema generation).
- **`go.sum`**: Locks dependency versions for reproducibility.
That’s it! The other files (like `.main.go.swp`) are temporary or non-Go files. Let me know if you want details on any specific part!
```


注意：这里DeepSeek模型并没有再调用read_file！与预期不相符，也许和模型的实现有关。比如模型缓存了这些文件的内容。


**步骤 (实验 5 – Go 版本):**- 输入: What go version are we using in this project?
- 观察: list_files -> AI 回复 -> read_file (go.mod) -> AI 回复 -> AI 最终回答 Go 版本。
- Agent输出：


```
You: What go version are we using in this project?
Tool Call: read_file({"path":"go.mod"})
AI: The project is using **Go version 1.24.0**, as specified in the `go.mod` file.
Let me know if you'd like help with anything else!
```


### 实验 6, 7, & 8：edit_file 工具 (创建、编辑文件)

**目标:**测试核心的 edit_file 工具，包括文件创建（当 old_str 为空且文件不存在时）和内容修改。**关键代码:**

工具定义 (EditFileDefinition): 定义 edit_file 工具，包含 path, old_str, new_str 三个参数。

```
type EditFileInput struct {
Path string json:"path" jsonschema_description:"The path..." jsonschema:"required"
OldStr string json:"old_str" jsonschema_description:"Text to search for..."
NewStr string json:"new_str" jsonschema_description:"Text to replace with..." jsonschema:"required"
}
var EditFileDefinition = ToolDefinition{
Name: "edit_file",
Description: "Make edits to a text file. Replaces ALL occurrences...",
InputSchema: GenerateSchema[EditFileInput](),
Function: EditFile, // Links to the Go function below
}
```


工具执行函数 (EditFile 及助手 createNewFile): 处理文件创建和修改逻辑。

```
func EditFile(input json.RawMessage) (string, error) {
editFileInput := EditFileInput{}
// ... parse input path, old_str, new_str ...
content, err := os.ReadFile(editFileInput.Path)
if err != nil {
// Key logic: If file doesn't exist AND old_str is empty, try creating it.
if os.IsNotExist(err) && editFileInput.OldStr == "" {
return createNewFile(editFileInput.Path, editFileInput.NewStr)
}
return "", err // Other read error
}
// File exists, perform replacement
oldContent := string(content)
newContent := strings.Replace(oldContent, editFileInput.OldStr, editFileInput.NewStr, -1) // Replace all
// ... check if replacement happened ...
err = os.WriteFile(editFileInput.Path, []byte(newContent), 0644) // Write back
// ... handle write error ...
return "OK", nil
}
// Helper to create a new file (and parent directories if needed)
func createNewFile(filePath, content string) (string, error) {
dir := path.Dir(filePath)
if dir != "." && dir != "" {
// Ensure parent directories exist
if err := os.MkdirAll(dir, 0755); err != nil { /* handle error */ }
}
err := os.WriteFile(filePath, []byte(content), 0644) // Write the new file
// ... handle error ...
return fmt.Sprintf("Successfully created file %s", filePath), nil
}
```


-
**解释:**edit_file 是最强大的工具。AI 根据用户的意图（创建或修改）来调用它，并提供必要的参数。Go 代码的核心逻辑在于：- 如果 os.ReadFile 返回“文件不存在”错误，并且 AI 提供的 old_str 是空字符串，则调用 createNewFile 来创建文件，将 new_str 作为初始内容。
- 如果文件存在，则使用 strings.Replace（替换所有匹配项）执行内容替换，并用 os.WriteFile 写回磁盘。

这种区分处理使得一个工具能同时处理创建和编辑两种场景。

-
**步骤 (实验 6 – 创建):**- 输入: hey buddy, create fizzbuzz.js…
- 观察: (可能 list_files) -> Tool Call: edit_file({“path”:”fizzbuzz.js”,”old_str”:”",”new_str”:”…”}) -> AI 回复成功。
- 验证: 退出 Agent，检查 fizzbuzz.js 是否生成。
- Agent输出与执行结果：


```
You: hey buddy, create fizzbuzz.js that I can run with Nodejs and that has fizzbuzz in it and executes it
Tool Call: edit_file({"path":"fizzbuzz.js","old_str":"","new_str":"// FizzBuzz in Node.js\nfunction fizzbuzz(n) {\n for (let i = 1; i <= n; i++) {\n if (i % 15 === 0) console.log(\"FizzBuzz\");\n else if (i % 3 === 0) console.log(\"Fizz\");\n else if (i % 5 === 0) console.log(\"Buzz\");\n else console.log(i);\n }\n}\n\n// Execute FizzBuzz for numbers 1 to 100\nfizzbuzz(100);"})
AI: Done! I've created **`fizzbuzz.js`** with a FizzBuzz implementation that runs in Node.js. Here's what it does:
1. **Function**:
- `fizzbuzz(n)` prints numbers from 1 to `n`, replacing multiples of 3 with "Fizz", multiples of 5 with "Buzz", and multiples of both with "FizzBuzz".
2. **Execution**:
- It runs for numbers **1 to 100** by default.
### How to Run:
node fizzbuzz.js
Let me know if you'd like any tweaks!
```


生成的fizzbuzz.js的文件内容如下：

```
$cat fizzbuzz.js
// FizzBuzz in Node.js
function fizzbuzz(n) {
for (let i = 1; i <= n; i++) {
if (i % 15 === 0) console.log("FizzBuzz");
else if (i % 3 === 0) console.log("Fizz");
else if (i % 5 === 0) console.log("Buzz");
else console.log(i);
}
}
// Execute FizzBuzz for numbers 1 to 100
fizzbuzz(100);%
```


使用node运行该fizzbuzz.js的文件，输出如下：

```
$node fizzbuzz.js
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
... ...
97
98
Fizz
Buzz
```


**步骤 (实验 7 – 编辑):**- 准备: 确保 fizzbuzz.js 存在。
- 运行 Agent。
- 输入: Please edit fizzbuzz.js so that it only prints until 15
- 观察: read_file -> edit_file (改代码) -> (可能) edit_file (改注释) -> AI 回复成功。
- 验证: 退出 Agent，检查 fizzbuzz.js 是否修改。
- Agent输出与执行结果：


```
You: Please edit fizzbuzz.js so that it only prints until 15
Tool Call: edit_file({"path":"fizzbuzz.js","old_str":"// Execute FizzBuzz for numbers 1 to 100\nfizzbuzz(100);","new_str":"// Execute FizzBuzz for numbers 1 to 15\nfizzbuzz(15);"})
AI: Got it! I updated **`fizzbuzz.js`** to print FizzBuzz only up to **15** instead of 100.
### How to Run:
node fizzbuzz.js
Now it’ll output:
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
Let me know if you'd like further changes!
```


查看更新后的fizzbuzz.js：

```
$cat fizzbuzz.js
// FizzBuzz in Node.js
function fizzbuzz(n) {
for (let i = 1; i <= n; i++) {
if (i % 15 === 0) console.log("FizzBuzz");
else if (i % 3 === 0) console.log("Fizz");
else if (i % 5 === 0) console.log("Buzz");
else console.log(i);
}
}
// Execute FizzBuzz for numbers 1 to 15
fizzbuzz(15);%
```


运行更新后的fizzbuzz.js结果如下：

```
$node fizzbuzz.js
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```


**步骤 (实验 8 – 创建):**- 输入: Create a congrats.js script that rot13-decodes…
- 观察: (可能 list_files) -> Tool Call: edit_file({“path”:”congrats.js”,”old_str”:”",”new_str”:”…”}) -> AI 回复成功。
- 验证: 退出 Agent，检查 congrats.js 是否生成，运行 node congrats.js 确认输出。
- Agent输出与执行结果：


```
You: Create a congrats.js script that rot13-decodes the following string 'Pbatenghyngvbaf ba ohvyqvat n pbqr-rqvgvat ntrag!' and prints it
AI: Here's the plan:
1. I'll create a **`congrats.js`** script.
2. It will **ROT13-decode** the string `'Pbatenghyngvbaf ba ohvyqvat n pbqr-rqvgvat ntrag!'`.
3. The decoded result will be printed to the console.
Let me implement this for you.
Tool Call: edit_file({"path":"congrats.js","old_str":"","new_str":"// ROT13 decoder in Node.js\nfunction rot13(str) {\n return str.replace(/[a-zA-Z]/g, function(c) {\n const base = c <= 'Z' ? 65 : 97;\n return String.fromCharCode((c.charCodeAt(0) - base + 13) % 26 + base);\n });\n}\n\n// Encoded string\nconst encoded = 'Pbatenghyngvbaf ba ohvyqvat n pbqr-rqvgvat ntrag!';\n\n// Decode and print\nconsole.log(rot13(encoded));"})
AI: Done! I've created **`congrats.js`** for you. Here's what it does:
1. **ROT13 Decoding**:
- The script decodes the string `'Pbatenghyngvbaf ba ohvyqvat n pbqr-rqvgvat ntrag!'` using ROT13.
2. **Output**:
- Running it will print the decoded message to the console.
### How to Run:
node congrats.js
The decoded result should appear. Let me know if you'd like to tweak anything!
```


查看生成的congrats.js结果如下：

```
$cat congrats.js
// ROT13 decoder in Node.js
function rot13(str) {
return str.replace(/[a-zA-Z]/g, function(c) {
const base = c <= 'Z' ? 65 : 97;
return String.fromCharCode((c.charCodeAt(0) - base + 13) % 26 + base);
});
}
// Encoded string
const encoded = 'Pbatenghyngvbaf ba ohvyqvat n pbqr-rqvgvat ntrag!';
// Decode and print
console.log(rot13(encoded));%
```


运行生成的congrats.js结果如下：

```
$node congrats.js
Congratulations on building a code-editing agent!
```


通过这些结合了代码片段和解释的步骤，你应该能更清晰地理解 Agent 在每个实验中是如何利用其被赋予的工具和核心循环机制来完成任务的。这再次印证了 Thorsten Ball 的观点：**核心很简单，但组合起来却能产生强大的效果**。

## 简单背后的深思：Agent 的真正壁垒在哪？

![](../../assets/66c2198b324a864b.jpg)


既然核心逻辑相对简单，那是否意味着构建一个优秀的 Agent 应用就没有门槛了呢？显然不是。Thorsten Ball 的“体力活” (Elbow Grease) 一词点醒了我们：**真正的挑战和壁垒，在于核心逻辑之外的大量工程细节和产品打磨。**

这包括但不限于：

**提示词工程 (Prompt Engineering):**如何设计出精确、高效、能引导 LLM 稳定输出预期格式和进行合理工具调用的 System Prompt 和 User Prompt？**工具设计与健壮性 (Tool Design & Robustness):**如何设计出功能明确、接口清晰、并且足够健壮（能处理各种边缘情况和错误输入）的工具？简单的字符串替换编辑文件显然是不够的，更复杂的场景需要更精密的工具（如 AST 操作、diff 应用等）。**状态管理与长上下文:**如何有效管理 Agent 的长期记忆、任务状态、以及在 LLM 的上下文窗口限制下处理复杂的多步骤任务？**错误处理与恢复:**当 LLM 理解错误、工具执行失败或外部环境变化时，Agent 如何优雅地处理错误、进行重试或寻求用户帮助？**用户体验与集成 (UI/UX & Integration):**如何将 Agent 无缝集成到用户的工作流中（如 IDE 插件、命令行工具、Web 应用）？如何提供直观、高效的交互界面？**性能与成本 (Performance & Cost):**如何优化 Agent 的响应速度？如何控制频繁调用 LLM API 带来的成本？**安全性:**如何确保 Agent 不会执行危险操作，或者被恶意利用？工具的权限控制至关重要。

这些才是构建一个能在现实世界中可靠、高效、安全地工作的 Agent 应用时，需要投入大量时间和精力去解决的**真正工程难题**。未来的 Agent 应用竞争，很可能就围绕着这些方面展开。

## 小结：人人皆可 Agent？拥抱实践的力量

Thorsten Ball 的文章和我们的复现实验，共同揭示了一个令人兴奋的事实：**理解和开始构建 AI Agent 的门槛，比许多人想象的要低得多。** 其核心概念是清晰且可及的。

这并不意味着打造卓越的 Agent 产品很容易，但它确实意味着，任何具备基本编程能力和对 LLM API 有所了解的开发者，都可以动手尝试，去探索 Agent 的可能性。

不要被表面的复杂性所迷惑，正如“皇帝的新衣”所揭示的，有时最强大的能力隐藏在最简洁的原理背后。现在，轮到你去发现、去实践、去创造了。

鼓励大家亲自尝试运行和修改这个Go Agent示例，感受一下与“你自己创造的智能体”协作编码的初步体验！

**想更进一步？开启你的 Go & AI 精进之旅！**

本文为你揭示了构建代码 Agent 的核心简洁性，但这仅仅是冰山一角。真正的挑战在于将这些基础概念，通过扎实的工程实践，转化为可靠、高效、能在实际场景中创造价值的应用。

如果你渴望在这条激动人心的道路上走得更远、更深，希望**系统性学习如何用Go构建AI原生应用**，深入探索 Agent、RAG（检索增强生成）、模型集成、向量数据库应用等前沿实践，我强烈推荐我的知识星球**「Gopher的AI原生应用开发第一课」**。在这里，我们不只有理论探讨，更有**动手实战项目、最新的技术趋势解读、活跃的高质量社群交流，以及与我的直接互动答疑**。如果你对用 Go 在 AI 时代创造真正有影响力的应用充满热情，这里将是你的最佳实践场和加速器。

![](../../assets/b594c752ab21b950.png)


**扫码加入「Go & AI 精进营」知识星球，开启你的 AI 原生开发之旅！** 并且，体系化Go核心进阶内容：「Go原理课」、「Go进阶课」、「Go避坑课」等独家深度专栏，将帮助你夯实Go内功

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


**你的支持，是创作的最大动力！**

最后，如果你觉得本文对你有启发、有帮助：

**【分享】**给你的朋友、同事或技术社群，一起交流探讨。**【关注】**我的公众号「[**iamtonybai**]」，第一时间获取更多Go语言、AI应用、云原生和架构思考与实践的硬核干货！

感谢你的耐心阅读与宝贵支持！期待在学习的路上与你继续同行！

![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


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

“亲手体验：一步步复现你的代码编辑Agent”这里 ai 配图有点诡异，左手六个指头，键盘也不是传统qwerty布局。

图片是ai生成的:)。