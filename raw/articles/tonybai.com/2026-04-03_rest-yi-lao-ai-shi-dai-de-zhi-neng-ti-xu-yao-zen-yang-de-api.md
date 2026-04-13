---
title: REST 已老，AI 时代的智能体需要怎样的 API？
url: https://tonybai.com/2026/04/03/agentic-api-in-action/
published: '2026-04-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# REST 已老，AI 时代的智能体需要怎样的 API？

![](../../assets/a7fd4f60763582f8.png)


[本文永久链接](https://tonybai.com/2026/04/03/agentic-api-in-action) – https://tonybai.com/2026/04/03/agentic-api-in-action

大家好，我是Tony Bai。

在过去的十几年里，如果你问任何一位后端工程师：“我们应该如何设计 API？”得到的答案几乎是统一的：**RESTful**。

我们将世界抽象为一个个“资源（Resources）”，用名词来命名 URI（比如 /users, /orders），用 HTTP 动词（GET, POST, PUT, DELETE）来表达对这些资源的操作。这套基于 CRUD（创建、读取、更新、删除）的法则，优雅地统治了移动互联网和微服务时代。

然而，时代变了。

当我们步入 AI 时代，尤其是当各种大语言模型（LLM）驱动的**智能体（AI Agent）**开始接管我们的软件系统时，一个尖锐的矛盾浮出水面：**这群“硅基同事”在面对我们精心设计的 REST API 时，表现得像个无所适从的笨蛋。**

今天，作为本专栏的开篇，我想和你探讨一个极其现实的工程问题：**为什么在 AI 时代，统治后端十年的 REST 架构正在失效？我们又该如何为 AI 智能体设计下一代接口——Agentic API？**

![](../../assets/4b42c4fbe335e1ec.png)


## AI 智能体的“认知障碍”：REST API 的三大罪状

为了理解 REST 的局限性，我们不妨先来做个角色互换。

假设你现在不是一个人类工程师，而是一个被赋予了任务的 AI Agent。你的主人对你说：“帮我把昨天那个发错的订单取消掉，并给客户退款。”

作为 Agent，你拥有一个极其强大的大脑（比如 GPT-5.x 或 DeepSeek-V3.x），并且你被授权访问公司内部的订单系统 API。你兴冲冲地查看了该系统的 Swagger 文档，看到了以下几个端点：

- GET /orders/{id} (获取订单)
- PUT /orders/{id} (更新订单)
- DELETE /orders/{id} (删除订单)
- POST /refunds (创建退款)

这时候，你的“认知障碍”出现了。

### 罪状一：意图的丢失

你要“取消订单”，但在 REST 的世界里，并没有一个叫“取消”的操作。

你应该调用 DELETE /orders/{id} 吗？如果你真的这么做了，你可能就把这条订单的物理记录从数据库里抹掉了，这在真实的电商系统中是灾难性的（通常我们需要软删除或者状态流转）。

还是说，你应该调用 PUT /orders/{id}，并在 JSON Payload 里传一个 {“status”: “CANCELLED”}？这听起来合理一些，但如果你传的是 {“status”: “DELETED”} 呢？API 会报错吗？

**REST API 强迫调用者去猜测后端的业务逻辑映射。** 对于人类开发者，我们可以通过阅读厚厚的 API 接入文档，或者直接去问写这个接口的同事来澄清。但对于 AI Agent，它只能基于常识去“猜”。当 AI 开始猜你的系统设计时，就是灾难的开始。

### 罪状二：原子性与编排的噩梦

更糟糕的是，主人的任务是“取消订单并退款”。

在 REST 架构下，订单资源（/orders）和退款资源（/refunds）通常是分离的。AI Agent 必须自己完成以下编排：

- 调用 PUT /orders/{id} 将状态改为 CANCELLED。
- 解析步骤 1 的响应，确认成功。
- 调用 POST /refunds，并小心翼翼地把订单的金额、支付流水号等信息拼装到 Payload 中。

如果步骤 1 成功了，但步骤 2 因为网络超时失败了怎么办？AI Agent 需要具备复杂的错误恢复机制和分布式事务处理能力（比如发起撤销操作）。我们把极其复杂的系统状态一致性问题，推给了客户端（AI）。

### 罪状三：权限的过度宽泛

为了让 AI 能够完成上述操作，你需要给它分配什么样的权限？

在传统的 OAuth 2.0 体系中，你可能不得不给它 order:write 和 refund:write 权限。这意味着，这个 AI Agent 不仅能取消订单，它还能修改订单金额，甚至能随意发起退款！

**REST API 以“资源”为粒度划分权限，这对于非确定性的 AI 来说，权限敞口太大了。** 我们真正想给 AI 的权限是“仅限取消特定状态的订单”，但这在传统的 REST 模型中极难优雅地表达。

## 破局之道：从“面向资源”到“面向任务”

面对上述痛点，业界最近非常流行一种解决方案：**让 AI 使用工具（Tool Calling / Function Calling）。**

比如 Anthropic 推出的 MCP（Model Context Protocol）协议，它的核心思想是：在 AI 和系统之间架设一个中间件（MCP Server），将系统的能力包装成一个个具体的 Tool（工具）暴露给 AI。

这确实缓解了部分问题，AI 可以直接调用名为 cancel_order_and_refund 的工具了。**但请注意，这治标不治本。**

这相当于我们在后端依然写着糟糕的、极难编排的 REST API，然后派人写了一堆中间层胶水代码（Glue Code）来适配 AI。随着系统变得复杂，维护这些“胶水工具”的成本将呈指数级上升，状态同步和权限控制的难题依然存在。

**我们真正需要的，是一场后端架构范式的革命：从源头上设计对 AI 友好的 API。**

这就是本微专栏要向你隆重介绍的 **Agentic API** 理念。

Agentic API 的核心思想是：**放弃将世界强行扭曲为“资源（名词）”，回归人类和 AI 最自然的交流方式——“任务与意图（动词）”。**

我们来看一个对比。

**传统 REST API 的思维模式：**

“这里有一个 Order 资源。你可以对它执行 POST, GET, PUT, DELETE。”


**Agentic API 的思维模式：**

“这里有一个业务系统。你可以执行 CANCEL（取消订单）, REFUND（发起退款）, NOTIFY（发送通知）等明确的任务。”


我们用一张简单的时序图来对比一下这两种模式下，AI Agent 完成“取消并退款”任务的复杂度差异：

![](../../assets/95a8dd0253189ba0.png)


在 Agentic API 模式下：

- 意图极其明确：API 端点本身就是一个清晰的动词（或动词组合），AI 不需要猜测 PUT 到底意味着什么。
- 后端掌控状态：复杂的编排逻辑（改状态、调退款接口、处理分布式事务）被收敛到了后端。后端永远是状态的最终防线。
- 权限精准控制：我们可以给 AI 颁发一个名为 action:cancel_and_refund 的细粒度 Token，即使 AI 产生幻觉想去改订单金额，也会被 API 网关直接拦截。

## 实战演练：用 Go 构建你的第一个 Agentic API

光说不练假把式。接下来，我们将用 Go 语言，从零开始将一个传统的 REST 接口改造为 Agentic API。

假设我们正在开发一个博客系统，我们需要一个接口让 AI 帮我们**“总结一篇文章的核心观点”**。

### 项目目录准备

请确保你已安装 Go 1.21 或以上版本。我们将使用标准库 net/http 来保持代码最简。

创建一个新目录并初始化模块：

```
mkdir agentic-api-demo
cd agentic-api-demo
go mod init agentic-demo
touch main.go
```


### 传统的 RESTful 实现 (反模式)

在传统的 CRUD 思维下，很多开发者可能会这么设计：

让客户端发送一个 POST /documents/{id}/summary 请求，或者使用一个万能的 PATCH /documents/{id}，带上一个 action=summarize 的字段。

这虽然能工作，但语义不够清晰，扩展性极差（如果明天需要翻译、提取关键字呢？）。

### Agentic API 的实现思路

在 Agentic API 的设计中，我们提倡使用**明确的动词驱动路由**。针对这种数据处理类的任务，我们可以定义一个 COMPUTE 或 ANALYZE 大类。

让我们在 main.go 中写下这段优雅的代码：

```
// ch01/agentic-api-demo/main.go
package main
import (
"encoding/json"
"fmt"
"log"
"net/http"
"strings"
)
// AgenticRequest 代表了 AI 智能体发来的标准任务请求
type AgenticRequest struct {
// 明确的意图动作
Action string json:"action"
// 动作的目标上下文 (例如文档ID)
ContextID string json:"context_id"
// 动作需要的特定参数
Parameters map[string]interface{} json:"parameters,omitempty"
}
// AgenticResponse 代表了返回给 AI 的标准结构化响应
type AgenticResponse struct {
Status string json:"status" // SUCCESS, FAILED, REQUIRE_CONFIRM
Result interface{} json:"result,omitempty"
Message string json:"message,omitempty"
}
func main() {
// 定义一个面向动作的路由前缀
http.HandleFunc("/api/v1/actions", actionHandler)
fmt.Println("Agentic API Server started on :8080")
log.Fatal(http.ListenAndServe(":8080", nil))
}
// actionHandler 充当了“任务调度中心”
func actionHandler(w http.ResponseWriter, r *http.Request) {
if r.Method != http.MethodPost {
http.Error(w, "Only POST is allowed for actions", http.StatusMethodNotAllowed)
return
}
var req AgenticRequest
if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
sendResponse(w, http.StatusBadRequest, "FAILED", nil, "Invalid JSON payload")
return
}
// 核心：基于 Action (动词) 进行路由分发，而不是基于资源名词
switch strings.ToUpper(req.Action) {
case "SUMMARIZE":
handleSummarize(w, req)
case "TRANSLATE":
// handleTranslate(w, req)
sendResponse(w, http.StatusNotImplemented, "FAILED", nil, "Action TRANSLATE not implemented yet")
default:
sendResponse(w, http.StatusBadRequest, "FAILED", nil, fmt.Sprintf("Unknown action: %s", req.Action))
}
}
// handleSummarize 处理具体的总结任务
func handleSummarize(w http.ResponseWriter, req AgenticRequest) {
docID := req.ContextID
if docID == "" {
sendResponse(w, http.StatusBadRequest, "FAILED", nil, "context_id (Document ID) is required")
return
}
// 解析可选参数 (Agentic API 应该允许 AI 传入控制参数)
maxLength := 100 // 默认值
if ml, ok := req.Parameters["max_length"].(float64); ok {
maxLength = int(ml)
}
// 模拟从数据库获取文档并进行总结的复杂逻辑
log.Printf("Executing SUMMARIZE for doc: %s, max length: %d\n", docID, maxLength)
// 模拟生成的摘要
mockSummary := fmt.Sprintf("这是关于文档 %s 的核心总结，长度被限制在 %d 字以内：Agentic API 是未来的趋势。", docID, maxLength)
// 返回标准化响应
sendResponse(w, http.StatusOK, "SUCCESS", mockSummary, "Document summarized successfully")
}
// 统一的响应封装助手
func sendResponse(w http.ResponseWriter, statusCode int, status string, result interface{}, message string) {
w.Header().Set("Content-Type", "application/json")
w.WriteHeader(statusCode)
resp := AgenticResponse{
Status: status,
Result: result,
Message: message,
}
json.NewEncoder(w).Encode(resp)
}
```


### 运行与验证

在终端运行该代码：

```
go run main.go
```


现在，假设你是一个 AI Agent，你决定执行“总结文章”的任务，你可以构造如下清晰的 Payload 发送给后端：

```
curl -X POST http://localhost:8080/api/v1/actions \
-H "Content-Type: application/json" \
-d '{
"action": "SUMMARIZE",
"context_id": "doc_9527",
"parameters": {
"max_length": 50
}
}'
```


你会得到一个标准化的、极易解析的响应：

```
{
"status": "SUCCESS",
"result": "这是关于文档 doc_9527 的核心总结，长度被限制在 50 字以内：Agentic API 是未来的趋势。",
"message": "Document summarized successfully"
}
```


**看出区别了吗？**

我们建立了一个统一的 /actions 门户。AI 只需要指明它**想做什么（Action: SUMMARIZE）**，针对**什么目标（ContextID: doc_9527）**，以及**有何要求（Parameters）**。

后端完全掌控了路由分发、参数校验和复杂的业务实现。如果你明天需要增加一个“翻译”功能，对于 AI 来说，只是换了一个动词（TRANSLATE），它的交互模式（Schema）**没有任何改变**。这种一致性极大地降低了 AI 的试错成本和代码生成复杂度。

## 专栏剧透：我们将如何系统性地驯服 AI 智能体？

刚才的实战只是开胃菜。要让你的整个微服务集群、成百上千个接口都变成“Agent-Ready（AI 就绪）”，我们需要一套完整的架构方法论。

这就引出了我们这个《[Agentic API 实战：为 AI 智能体设计下一代接口](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4455138001052172294#wechat_redirect)》微专栏，以及后续的安排。

在接下来的 5 讲中，我将摒弃那些空洞的 AI 概念，从一名后端架构师的视角出发，带你一步步把这套理念落地为真实的生产级能力。所有核心模式都会配备详实的 Go 语言可运行代码。

以下是我们接下来的“作战路线图”：

**第 02 讲 | 重新定义动作：掌握 ACTION 接口分类法**

我们会深入探讨 Agentic API 的“六大核心动词”（获取、计算、交易、集成、编排、通知）。你会学到如何彻底抛弃 CRUD 思维，用 AI 最容易理解的意图来重塑你的路由设计。**第 03 讲 | 语义可发现性：让 AI 自己“读懂”你的系统能力**

当你有 100 个接口时，把文档全部喂给 AI 是愚蠢且昂贵的。我们将用 Go 实现一个动态的 DISCOVER 端点，让 AI 能够像人类查字典一样，按需、动态地探索你系统的能力边界和前置条件。**第 04 讲 | OpenAPI 进化：用 Agentic 扩展赋能机器阅读**

我们不需要推翻现有的基础设施。这一讲，我将教你如何利用 OpenAPI (Swagger) 的 x- 自定义扩展机制，把“不可逆风险”、“副作用”等业务约束“藏”进标准文档里，让死文档变成 AI 的“行动护栏”。**第 05 讲 | 复杂任务编排：链式调用 (Chaining) 与测试模式 (Dry Run)**

这是保证 AI 绝对安全的核心！当 AI 需要连续调用三个接口完成扣款时，如何在网络抖动中保全业务状态？我们将设计基于后端的链式调用，并引入价值连城的“Dry Run（安全演习）”模式，把 AI 犯错的成本降到最低。**第 06 讲 | 演进与落地：如何将现有系统平滑升级为 Agentic API？**

现实是骨感的，你的公司里堆满了 5 年前写的陈旧 REST 接口。大结局中，我将演示一种优雅的“代理与适配器（Proxy & Adapter）”架构，教你在不修改任何一行老代码的前提下，为遗留系统穿上“AI 外骨骼”。

这是一次从思维方式到工程实现的全面升级。如果你准备好了迎接 AI 带来的自动化红利，并且希望成为团队里那个“最懂如何让机器调接口”的架构师，那么，请扫描下方二维码，紧跟我的步伐。

![](../../assets/4b42c4fbe335e1ec.png)


## 本讲小结

今天，我们站在了一个新时代的起点。

**认知翻新：**传统的 RESTful API 围绕着“静态资源（名词）”展开，要求调用方（无论人还是机器）了解系统的内在状态流转。这在 AI 时代变成了沉重的认知负担，导致意图丢失、编排复杂、权限泛滥。**范式转移：**Agentic API 提倡转向“任务驱动（动词）”。API 端点应该直接表达操作意图（如 SUMMARIZE, CANCEL_ORDER），由后端收敛复杂的业务编排和状态管理。**实战起航：**我们用 Go 构建了一个极简的动作分发网关，展示了如何用统一的结构（Action, Context, Parameters）来响应 AI 智能体的请求。

这仅仅是冰山一角。在接下来的专栏中，我们将深入探讨 Agentic API 的骨架：**六大核心 ACTION 分类法**。我们将学习如何让 AI 自动“发现”你的系统能力，如何通过扩展 OpenAPI 规范生成完美的智能体说明书，以及如何设计让 AI 执行复杂连锁任务的“沙盒测试模式”。

世界正在不可逆转地走向自动化，懂 AI 调用的 API 架构师，将成为下个十年最稀缺的资源。我们下一讲见！

本讲涉及的示例代码和脚本可以在[这里](https://github.com/bigwhite/publication/tree/master/micro-column/agentic-api-in-action/ch01)下载。

## 思考题

在你的日常开发中，有没有遇到过一个传统的 REST API（比如一个修改用户状态的 PUT 接口），它的内部逻辑其实非常复杂（包含了发邮件、写审计日志、调起其他微服务等操作）？

如果让你用 Agentic API 的思维（动词驱动）重新设计这个接口的访问方式，你会怎么命名这个 Action？它的 Payload 结构会是什么样的？

欢迎在评论区留下你的思考和设计，我会和你一起讨论。

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


**原「Gopher部落」已重装升级为「Go & AI 精进营」知识星球，快来加入星球，开启你的技术跃迁之旅吧！**

我们致力于打造一个高品质的 **Go 语言深度学习** 与 **AI 应用探索** 平台。在这里，你将获得：

**体系化 Go 核心进阶内容:**深入「Go原理课」、「Go进阶课」、「Go避坑课」等独家深度专栏，夯实你的 Go 内功。**前沿 Go+AI 实战赋能:**紧跟时代步伐，学习「Go+AI应用实战」、「Agent开发实战课」、「Agentic软件工程课」、「Claude Code开发工作流实战课」、「OpenClaw实战分享」等，掌握 AI 时代新技能。**星主 Tony Bai 亲自答疑:**遇到难题？星主第一时间为你深度解析，扫清学习障碍。**高活跃 Gopher 交流圈:**与众多优秀 Gopher 分享心得、讨论技术，碰撞思想火花。**独家资源与内容首发:**技术文章、课程更新、精选资源，第一时间触达。

衷心希望「Go & AI 精进营」能成为你学习、进步、交流的港湾。让我们在此相聚，享受技术精进的快乐！欢迎你的加入！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论