---
title: 告别智能体孤岛：谷歌A2A协议能否成为企业AI协作的通用语？
url: https://tonybai.com/2025/04/14/what-is-a2a-protocol/
published: '2025-04-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 告别智能体孤岛：谷歌A2A协议能否成为企业AI协作的通用语？

[本文永久链接](https://tonybai.com/2025/04/14/what-is-a2a-protocol) – https://tonybai.com/2025/04/14/what-is-a2a-protocol

随着人工智能（AI）的飞速发展，AI 智能体（Agent）正成为企业自动化、提升生产力的关键力量。从处理日常重复任务到辅助复杂决策，智能体的应用场景日益广泛。然而，一个严峻的挑战随之而来：**不同框架、不同厂商构建的智能体往往如同信息孤岛，难以有效协作**，这极大地限制了它们在复杂企业环境中的潜力释放。

为了打破这一僵局，谷歌近日联合 Atlassian、Salesforce、SAP、LangChain、Cohere 等超过 50 家技术合作伙伴和领先服务提供商，共同**发布并推动一个全新的开放协议—— Agent2Agent(A2A)**。该协议旨在为不同生态系统中的AI智能体提供一种标准的通信语言，使其能够安全地发现彼此、交换信息、协调行动，最终实现跨平台、跨应用的无缝协作。

![](../../assets/7a29391b2a8675e5.png)


在这篇文章中，我们就来结合示例快速了解一下A2A协议的设计哲学、核心机制、交互流程与对象模型，以及它与[MCP(model context protocol)](https://modelcontextprotocol.io/introduction)的区别。这可能是你看过的关于Agent互操作协议最清晰的解读之一。

## 1. A2A协议的设计哲学与核心机制

企业环境中，单一智能体往往难以应对复杂的端到端流程。例如，一个完整的客户服务请求可能需要客服智能体、订单系统智能体、物流跟踪智能体协同工作。A2A协议的诞生，正是为了满足这种日益增长的跨系统、跨智能体协作需求。

**A2A的核心目标是促进智能体之间的互操作性（Interoperability）**，即使这些智能体基于不同的技术栈构建、不共享内部状态或工具集。谷歌及其合作伙伴在设计A2A时，明确了五大关键原则，这些原则深刻影响了协议的形态：

**拥抱智能体能力 (Embrace agentic capabilities)**

协议并非将智能体降级为简单的 API 或工具，而是承认并支持它们以更自然、有时甚至是非结构化的方式进行交互和协作。

**基于现有标准 (Build on existing standards)**

为了降低采用门槛和集成复杂度，A2A 建立在开发者熟悉的 **HTTP/1.1 或 HTTP/2 之上，采用 JSON-RPC 2.0 作为请求/响应格式，并利用服务器发送事件 (Server-Sent Events, SSE) 实现流式通信**。这使得 A2A 更易融入现有的企业 IT 架构。

**默认安全 (Secure by default)**

安全是企业级应用的基础。A2A 在设计上与 **OpenAPI 的认证规范保持一致**，支持如 OAuth2、API Key、JWT 等多种认证方案。关键在于，认证凭证通过标准的 HTTP Header（如 Authorization）传递，而非包含在 A2A 的 JSON 载荷中，确保协议本身与具体认证机制解耦，并强制要求服务器对每个请求进行验证。

**支持长时与异步任务 (Support for long-running tasks)**

许多智能体任务并非瞬时完成，可能涉及复杂计算、外部调用甚至人工介入（Human-in-the-loop）。A2A 通过**任务状态管理、流式更新 (SSE) 和可选的推送通知 (Push Notifications)** 机制，原生支持这类耗时较长的异步交互场景。

**模态无关 (Modality agnostic)**

智能体的交互远不止文本。A2A 的 Part 数据结构设计使其能够承载**文本 (TextPart)、文件 (FilePart，支持内联 Base64 或 URI 引用，可用于图像、文档等) 和结构化数据 (DataPart，用于表单、JSON 对象等)**。这为未来支持音频流、视频流等多模态交互奠定了基础。

## 2. A2A 的核心交互流程与对象模型

A2A 定义了一个清晰的客户端-服务器交互模型。一个“客户端”智能体（发起请求方）与一个“远程”智能体（A2A 服务器，处理请求方）通过一系列标准化的步骤进行通信：

![](../../assets/d72e174f6f5d01f1.png)


Agent交互的第一步是发现。

### 2.1 **发现 (Discovery)**

客户端首先需要找到并了解远程智能体的能力。这通过获取远程智能体的**Agent Card**实现。Agent Card是一个JSON 文件，通常发布在服务器的熟知路径下，推荐路径为：

```
https://base url/.well-known/agent.json
```


Agent Card中包含了智能体的**名称、描述、服务 URL、版本、提供商信息、支持的核心能力 (capabilities 如 streaming, pushNotifications)、认证要求 (authentication)、默认输入/输出模式 (defaultInputModes/defaultOutputModes) 以及最重要的——它所具备的技能列表 (skills)**。每个技能 (AgentSkill) 有 ID、名称、描述、标签、示例等，帮助客户端判断该智能体是否适合处理特定任务。

下面是A2A协议文档中Agent Card的一个示例，我们来看一下：

```
//agent card
{
"name": "Google Maps Agent",
"description": "Plan routes, remember places, and generate directions",
"url": "https://maps-agent.google.com",
"provider": {
"organization": "Google",
"url": "https://google.com"
},
"version": "1.0.0",
"authentication": {
"schemes": "OAuth2"
},
"defaultInputModes": ["text/plain"],
"defaultOutputModes": ["text/plain", "application/html"],
"capabilities": {
"streaming": true,
"pushNotifications": false
},
"skills": [
{
"id": "route-planner",
"name": "Route planning",
"description": "Helps plan routing between two locations",
"tags": ["maps", "routing", "navigation"],
"examples": [
"plan my route from Sunnyvale to Mountain View",
"what's the commute time from Sunnyvale to San Francisco at 9AM",
"create turn by turn directions from Sunnyvale to Mountain View"
],
// can return a video of the route
"outputModes": ["application/html", "video/mp4"]
},
{
"id": "custom-map",
"name": "My Map",
"description": "Manage a custom map with your own saved places",
"tags": ["custom-map", "saved-places"],
"examples": [
"show me my favorite restaurants on the map",
"create a visual of all places I've visited in the past year"
],
"outputModes": ["application/html"]
}
]
}
```


这个JSON对象是一个典型的Agent Card实例，它为”Google Maps Agent”提供了一份详细的说明书，旨在让其他客户端（可能是用户界面、应用程序或其他AI智能体）了解如何发现、连接和使用它。下面我们逐一解析其关键字段：

-
**基本信息 (Identification & Discovery):**- “name”: “Google Maps Agent”: 这是该智能体的
**人类可读名称**，简洁明了地标识了它的身份。 - “description”: “Plan routes, remember places, and generate directions”: 提供了更详细的
**功能概述**，帮助客户端快速理解该智能体的核心用途。 - “url”: “https://maps-agent.google.com”: 这是至关重要的
**基础服务端点 URL**。客户端将向这个 URL（或其下的特定路径，如 /a2a，具体取决于实现）发送 A2A 协议的 JSON-RPC 请求。 - “provider”: { “organization”: “Google”, “url”: “https://google.com” }: 指明了
**服务提供商**是 Google，增加了来源的可信度，并提供了组织信息。 - “version”: “1.0.0″: 表明了当前 Agent Card 所描述的智能体实现的
**版本号**，有助于客户端进行版本兼容性管理。

- “name”: “Google Maps Agent”: 这是该智能体的
-
**连接与交互要求 (Connection & Interaction Requirements):**- “authentication”: { “schemes”: “OAuth2″ }: 这个字段明确了与该智能体交互所需的
**认证机制**。客户端在发送请求时，需要通过标准的 HTTP Authorization 头携带有效的 OAuth2 令牌。这是实现安全通信的关键。 - “defaultInputModes”: ["text/plain"]: 定义了该智能体
**默认接受的输入内容类型**。除非特定技能另有说明，否则它主要期望接收纯文本输入。 - “defaultOutputModes”: ["text/plain", "application/html"]: 定义了该智能体
**默认能够生成的输出内容类型**。它可以返回纯文本或 HTML 格式的响应。

- “authentication”: { “schemes”: “OAuth2″ }: 这个字段明确了与该智能体交互所需的
-
**核心协议能力 (Core Protocol Capabilities):**- “capabilities”: { “streaming”: true, “pushNotifications”: false }: 这个对象说明了该智能体支持的 A2A 协议
**高级特性**。- “streaming”: true: 表示该智能体
**支持流式响应**。客户端可以使用 tasks/sendSubscribe 方法发起请求，并通过 SSE 实时接收任务状态和结果更新。 - “pushNotifications”: false: 表示该智能体
**不支持推送通知**。即使客户端配置了 webhook，该智能体也不会在连接断开后主动推送更新。

- “streaming”: true: 表示该智能体

- “capabilities”: { “streaming”: true, “pushNotifications”: false }: 这个对象说明了该智能体支持的 A2A 协议
-
**具体技能清单 (Skills List):**- “skills”: [...]: 这是 Agent Card 的核心部分，详细列出了该智能体
**具体能执行的任务类型（技能）**。客户端可以根据这个列表来判断该智能体是否具备完成特定用户请求的能力。 **技能 1: Route Planning (route-planner)**- “id”: 技能的唯一标识符。
- “name”: 技能的人类可读名称。
- “description”: 详细描述该技能的作用。
- “tags”: [...]: 相关的标签，便于分类和搜索。
- “examples”: [...]:
**非常重要**，提供了具体的**用户请求示例**。这极大地帮助了客户端（尤其是其他 AI 智能体）理解如何有效地触发和使用这项技能。 - “outputModes”: ["application/html", "video/mp4"]:
**覆盖了默认输出模式**。这个技能特别指出，除了默认的文本和 HTML，它还能生成 video/mp4 格式的输出（例如，路线演示视频）。这展示了 A2A 协议的灵活性，允许不同技能具有不同的输出能力。

**技能 2: Custom Map (custom-map)**- 同样包含 id, name, description, tags, examples。
- “outputModes”: ["application/html"]: 这个技能的输出模式仅限于 HTML，它也
**覆盖了默认设置**，但没有像 route-planner 那样增加额外的视频格式。


- “skills”: [...]: 这是 Agent Card 的核心部分，详细列出了该智能体

我们看到：客户端（无论是人类开发者阅读，还是另一个程序解析）可以通过这份”名片”，准确地了解如何与”Google Maps Agent”进行有效且安全的交互，选择合适的技能来满足用户需求，并预期可能收到的响应格式。这正是A2A协议实现智能体互操作性的基石。

### 2.2 **任务启动与管理 (Task Initiation & Management)**

一旦Agent相互发现后，后续所有交互都围绕**Task**对象展开。Task是A2A中的核心工作单元，代表一个需要完成的目标，拥有唯一的id和可选的 sessionId (用于关联同一会话中的多个任务)。

客户端通过向服务器的 A2A 端点发送 **JSON-RPC 请求**来启动或继续一个任务。主要方法包括：

- tasks/send: 用于发送初始请求或在多轮对话中发送后续用户输入。服务器处理后同步返回最终的 Task 状态及结果 (Artifacts)。适用于短时任务或客户端选择轮询获取更新的场景。
- tasks/get: 用于查询指定 id 的任务状态和已生成的 Artifacts，可选择性地获取最近的 N 条消息历史 (historyLength)。
- tasks/cancel: 请求取消一个正在进行的任务。
- tasks/sendSubscribe: 同样用于发送消息，但服务器会通过
**SSE 连接**持续推送任务进展。适用于长时任务，客户端可以实时接收更新。这是一种**流工作模式**。

Task 对象包含当前状态 (status)，该状态会经历一个生命周期：submitted -> working -> (可能进入 input-required) -> completed / failed / canceled。

下面是一个发送task和接收task response的示例。我们先看请求，具体字段的含义在示例的注释中，后续就不赘述了。

```
//Request
{
"jsonrpc": "2.0", // 1. 标准 JSON-RPC 版本声明
"id": 1, // 2. 客户端生成的请求 ID，用于匹配响应
"method":"tasks/send", // 3. 调用的 A2A 方法：发送消息以启动或继续任务
"params": { // 4. 方法参数
"id": "de38c76d-d54c-436c-8b9f-4c2703648d64", // 5. 任务 ID (由客户端生成)
"message": { // 6. 要发送的消息内容
"role":"user", // 7. 消息发送者角色：用户 (由客户端代理)
"parts": [{ // 8. 消息内容部分
"type":"text", // 9. 内容类型：纯文本
"text": "tell me a joke" // 10. 具体的文本内容
}]
},
"metadata": {} // 11. 可选的元数据，这里为空
}
}
```


这个请求是客户端在启动一个新任务（ID: de38c…），并通过 tasks/send 方法发送了一个包含文本 “tell me a joke” 的用户消息。

下面是该请求对应的响应体的内容：

```
//Response
{
"jsonrpc": "2.0", // 1. 标准 JSON-RPC 版本声明
"id": 1, // 2. 响应的 ID，与请求的 ID 匹配
"result": { // 3. 请求成功，包含结果数据
"id": "de38c76d-d54c-436c-8b9f-4c2703648d64", // 4. 任务 ID，与请求中的一致
"sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4", // 5. 会话 ID (由服务器生成)
"status": { // 6. 任务的当前状态
"state": "completed" // 7. 任务状态：已完成
},
"artifacts": [{ // 8. 任务生成的制品 (结果)
"name":"joke", // 9. 制品名称
"parts": [{ // 10. 制品内容部分
"type":"text", // 11. 内容类型：纯文本
"text":"Why did the chicken cross the road? To get to the other side!" // 12. 具体的笑话文本
}]
}],
"metadata": {} // 13. 可选的元数据，这里为空
}
}
```


这个响应表明服务器成功接收并处理了 ID 为 de38c… 的任务请求。任务已经完成 (completed)，服务器为此任务分配了一个会话 ID (c295ea…)，并将结果（笑话文本）封装在一个名为 “joke” 的 Artifact 中返回给了客户端。

上面这个简单的示例清晰地展示了A2A协议中最基础的一种交互模式。

通过task可以承载Message和Artifact，而Message和Artifact各自又可以分为多个Part，它们的对象关系图如下：

![](../../assets/e0490317a7f2a1ae.png)


Task 是状态和流程的容器。 Message 是 Task 请求过程中的通信载体。 Artifact 是 Task 产生的结果载体。 Part 是构成 Message 和 Artifact 内容的基本单元。

下面我们就来看看Message和Artifact这两种对象。

### 2.3 **通信载体：消息与部件 (Communication: Message & Part)**

Message(消息)包含任何非人工制品的内容。这可以包括智能体的想法、用户上下文、指令、错误、状态或元数据等。 客户端和服务器之间的交流通过**Message**对象进行。Message 标识了发送方 (role: “user” 或 “agent”)，并包含一个或多个**Part** 对象。

Part 是实际内容的载体，可以是：

- TextPart: 包含 text 字段。
- FilePart: 包含 file 对象，该对象内含 mimeType、name，以及 bytes (Base64 编码内容) 或 uri (文件链接)。
- DataPart: 包含 data 字段，承载任意 JSON 结构，常用于表单提交或结构化数据交换。

在上面发送task的示例中我们已经看到了Message的一个示例(下面再摘录一下其中内容，这是一个TextPart)：

```
"message": { // 6. 要发送的消息内容
"role":"user", // 7. 消息发送者角色：用户 (由客户端代理)
"parts": [{ // 8. 消息内容部分
"type":"text", // 9. 内容类型：纯文本
"text": "tell me a joke" // 10. 具体的文本内容
}]
},
```


我们再来看看Artifact。

### 2.4 **结果交付：制品 (Result Delivery: Artifact)**

当智能体完成任务或产生阶段性结果时，它会生成**Artifact** 对象。Artifact代表任务的最终或中间输出。

一个 Artifact 可以有名称 (name)、描述 (description)，并像 Message 一样包含一个或多个Part。例如，一个生成报告的任务可能产生一个包含 TextPart (报告文本) 和 FilePart (PDF 文件) 的 Artifact。

在上面示例的应答中，我们已经见识过Aritfact了：

```
"artifacts": [{ // 8. 任务生成的制品 (结果)
"name":"joke", // 9. 制品名称
"parts": [{ // 10. 制品内容部分
"type":"text", // 11. 内容类型：纯文本
"text":"Why did the chicken cross the road? To get to the other side!"
}
}],
```


此外，在流式传输中，Artifact 可以通过 TaskArtifactUpdateEvent 分块 (append: true) 发送，并用 lastChunk: true 标记结束。

### 2.5 **异步与实时更新：流式传输与推送通知**

A2A支持通过SSE实现的流式传输。 当使用 tasks/sendSubscribe 时，服务器通过 SSE 连接发送事件流。主要事件类型包括：

- TaskStatusUpdateEvent: 通知任务状态 (status) 的变化，包含状态码、可选的消息 (message) 和时间戳 (timestamp)。final: true 标记任务终结。
- TaskArtifactUpdateEvent: 流式传输 Artifact 的内容。

下面是一个流式传输的示例(主要是通过TaskArtifactUpdateEvent传输Artifact的内容)：

```
//Request
{
"method":"tasks/sendSubscribe",
"params": {
"id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
"sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
"message": {
"role":"user",
"parts": [{
"type":"text",
"text": "write a long paper describing the attached pictures"
},{
"type":"file",
"file": {
"mimeType": "image/png",
"data":"<base64-encoded-content>"
}
}]
},
"metadata": {}
}
}
//Response
data: {
"jsonrpc": "2.0",
"id": 1,
"result": {
"id": 1,
"status": {
"state": "working",
"timestamp":"2025-04-02T16:59:25.331844"
},
"final": false
}
}
data: {
"jsonrpc": "2.0",
"id": 1,
"result": {
"id": 1,
"artifact": [
"parts": [
{"type":"text", "text": "<section 1...>"}
],
"index": 0,
"append": false,
"lastChunk": false
]
}
}
data: {
"jsonrpc": "2.0",
"id": 1,
"result": {
"id": 1,
"artifact": [
"parts": [
{"type":"text", "text": "<section 2...>"}
],
"index": 0,
"append": true,
"lastChunk": false
]
}
}
data: {
"jsonrpc": "2.0",
"id": 1,
"result": {
"id": 1,
"artifact": [
"parts": [
{"type":"text", "text": "<section 3...>"}
],
"index": 0,
"append": true,
"lastChunk": true
]
}
}
data: {
"jsonrpc": "2.0",
"id": 1,
"result": {
"id": 1,
"status": {
"state": "completed",
"timestamp":"2025-04-02T16:59:35.331844"
},
"final": true
}
}
```


A2A还支持**推送通知 (Push Notifications)**，允许服务器在客户端断开连接后，仍能将任务状态更新发送到客户端预先配置的 webhook URL。客户端通过 tasks/pushNotification/set 提供 webhook URL 和可选的认证信息。服务器通过 tasks/pushNotification/get 查询配置。这对于需要人工介入或极长时间运行的任务至关重要。

最后再看看多轮交互。

### 2.6 **多轮交互 (Multi-turn Conversations)**

当任务状态变为 input-required 时，服务器发送的 TaskStatus 对象中的 message 会指示需要用户提供什么信息（可能是文本提示，也可能是包含 DataPart 的表单结构）。客户端获取用户输入后，再次调用 tasks/send (携带相同的 id 和 sessionId)，将用户响应作为新的 Message 发送给服务器，任务得以继续。

下面是协议规范中一个多轮交互的示例：

```
//Request - seq 1
{
"jsonrpc": "2.0",
"id": 1,
"method":"tasks/send",
"params": {
"id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
"message": {
"role":"user",
"parts": [{
"type":"text",
"text": "request a new phone for me"
}]
},
"metadata": {}
}
}
//Response - seq 2
{
"jsonrpc": "2.0",
"id": 1,
"result": {
"id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
"sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
"status": {
"state": "input-required",
"message": {
"parts": [{
"type":"text",
"text":"Select a phone type (iPhone/Android)"
}]
}
},
"metadata": {}
}
}
//Request - seq 3
{
"jsonrpc": "2.0",
"id": 2,
"method":"tasks/send",
"params": {
"id": "de38c76d-d54c-436c-8b9f-4c2703648d64",
"sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
"message": {
"role":"user",
"parts": [{
"type":"text",
"text": "Android"
}]
},
"metadata": {}
}
}
//Response - seq 4
{
"jsonrpc": "2.0",
"id": 2,
"result": {
"id": 1,
"sessionId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
"status": {
"state": "completed"
},
"artifacts": [{
"name": "order-confirmation",
"parts": [{
"type":"text",
"text":"I have ordered a new Android device for you. Your request number is R12443"
}],
"metadata": {}
}],
"metadata": {}
}
}
```


## 3. A2A与MCP：协同而非竞争，共筑智能体生态

在讨论智能体互操作性时，另一个常被提及的协议是 Anthropic 推出的 **Model Context Protocol (MCP)**。理解 A2A 与 MCP 的区别与联系，对于把握当前智能体生态的发展方向至关重要。谷歌在发布 A2A 时也明确指出，两者是互补而非竞争关系。正如下图所示：

![](../../assets/5a3334775c1de853.png)



上图形象地揭示了两者核心关注点的不同：

-
**A2A (Agent2Agent): 聚焦于智能体之间的通信与协作****核心目标:**A2A 的设计初衷是为了解决**不同 AI 智能体之间如何进行有效交互**的问题。它定义了一套标准的协议，使得由不同供应商、使用不同框架构建的、甚至内部逻辑互不透明（Opaque）的智能体，能够相互发现、理解对方的能力（通过 Agent Card）、协商交互方式（如数据格式、模态），并协同完成更复杂的任务。**交互模式:**是**Agent <-> Agent**。它关心的是智能体 A 如何将一个任务或子任务委托给智能体 B，如何传递必要的上下文，如何管理任务状态，以及如何接收来自智能体 B 的结果或需要进一步输入的请求。**应用场景:**主要用于构建**多智能体系统 (Multi-Agent Systems)**，实现跨系统、跨应用的企业级工作流自动化，需要多个具有不同专长的智能体协同工作的场景。

-
**MCP (Model Context Protocol): 聚焦于智能体与工具/API 的通信****核心目标:**MCP 主要关注的是**单个 AI 智能体如何更有效地理解和使用外部工具或 API**。它提供了一种标准化的方式来描述工具的功能、参数、以及如何将相关上下文信息传递给模型，从而提高模型调用工具的准确性和可靠性。**交互模式:**本质上是**Agent <-> API/Tool**。它关心的是智能体如何理解一个外部函数（如天气查询 API、数据库查询工具）并准确地调用它，以及如何处理返回结果。**应用场景:**主要用于增强**单个智能体的能力**，让它能够像人类使用软件一样，通过调用各种工具来完成自身无法独立完成的任务，例如联网搜索、代码执行、访问专有数据等。


综上，A2A和MCP是妥妥的**互补关系**：**A2A**致力于解决**“智能体们如何互相交谈与合作”** 的问题。而**MCP**则致力于解决**“一个智能体如何更好地使用它的工具箱”**的问题。

在一个复杂的系统中，两者可以很好地协同工作：一个主智能体可以使用 **MCP** 来理解和调用其内部集成的各种工具（如数据库查询、日历管理 API）；当需要与其他独立的、专门化的智能体（如财务审批智能体、报告生成智能体）协作时，它可以通过 **A2A** 协议与这些外部智能体进行通信和任务协调。 因此，将 A2A 和 MCP 视为智能体生态建设中不同层面的解决方案更为准确。A2A 构建了智能体之间的“社交网络”，而 MCP 则增强了每个智能体个体的“动手能力”。两者共同推动着更强大、更灵活、更具适应性的 AI 智能体系统的发展。

## 4. 小结

Agent2Agent (A2A) 协议是谷歌及其庞大生态伙伴网络为解决 AI 智能体互操作性难题而迈出的关键一步。通过提供一个基于开放标准、注重安全和灵活性的通信框架，A2A有望成为连接不同智能体、打通企业复杂流程的桥梁，从而真正释放 AI 在自动化和生产力提升方面的潜力。

虽然 A2A 目前仍处于草案阶段，但其清晰的设计理念、强大的合作伙伴支持以及开放的社区模式，都预示着其广阔的应用前景。谷歌计划在今年晚些时候推出生产就绪版本，并持续根据社区反馈进行迭代优化，未来可能涵盖更复杂的动态能力协商、任务内UX调整等高级特性。

A2A 的旅程才刚刚开始。它的最终成功将取决于业界的广泛采纳和开发者社区的积极贡献。我们期待 A2A 能够引领 AI 智能体进入一个更加协同、高效、互联互通的新时代。

对 A2A 感兴趣的开发者可以通过以下途径深入了解和参与：

**官方文档:**[A2A 官方文档网站](https://google.github.io/A2A/#/documentation)提供概览和深入主题。**协议规范:**[JSON 协议规范](https://github.com/google/A2A/tree/main/specification)定义了所有数据结构和方法。**代码示例:**官方 GitHub 仓库 ([google/A2A](https://github.com/google/A2A)) 提供了 Python 和 JavaScript 的[客户端/服务器实现](https://github.com/google/A2A/tree/main/samples)，以及与 CrewAI、LangGraph、Genkit 等框架集成的[智能体示例](https://github.com/google/A2A/tree/main/samples)。**社区参与:**通过[GitHub Discussions](https://github.com/google/A2A/discussions)交流，通过[GitHub Issues](https://github.com/google/A2A/issues)提交反馈，或使用[谷歌表单](https://docs.google.com/forms/d/e/1FAIpQLScS23OMSKnVFmYeqS2dP7dxY3eTyT7lmtGLUa8OJZfP4RTijQ/viewform)提供私密反馈。

你对 A2A 协议的前景怎么看？它能真正解决 Agent 协作的难题吗？欢迎在评论区留下你的看法！

关注我，获取更多 Go、AI 与云原生前沿解读。

**原「Gopher部落」已重装升级为「Go & AI 精进营」知识星球，快来加入星球，开启你的技术跃迁之旅吧！**

我们致力于打造一个高品质的 **Go 语言深度学习** 与 **AI 应用探索** 平台。在这里，你将获得：

**体系化 Go 核心进阶内容:**深入「Go原理课」、「Go进阶课」、「Go避坑课」等独家深度专栏，夯实你的 Go 内功。**前沿 Go+AI 实战赋能:**紧跟时代步伐，学习「Go+AI应用实战」、「Agent开发实战课」，掌握 AI 时代新技能。**星主 Tony Bai 亲自答疑:**遇到难题？星主第一时间为你深度解析，扫清学习障碍。**高活跃 Gopher 交流圈:**与众多优秀 Gopher 分享心得、讨论技术，碰撞思想火花。**独家资源与内容首发:**技术文章、课程更新、精选资源，第一时间触达。

衷心希望「Go & AI 精进营」能成为你学习、进步、交流的港湾。让我们在此相聚，享受技术精进的快乐！欢迎你的加入！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


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