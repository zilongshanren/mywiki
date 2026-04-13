---
title: Go 解析器的“隐秘角落”：encoding/json 的安全陷阱与 JSONv2 的救赎
url: https://tonybai.com/2025/06/22/unexpected-security-footguns-in-go-parsers/
published: '2025-06-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 解析器的“隐秘角落”：encoding/json 的安全陷阱与 JSONv2 的救赎

![](../../assets/3e84e719c7b8c6b5.png)


[本文永久链接](https://tonybai.com/2025/06/22/unexpected-security-footguns-in-go-parsers) – https://tonybai.com/2025/06/22/unexpected-security-footguns-in-go-parsers

大家好，我是Tony Bai。

在 Go 语言中，标准库的 encoding/json 包无疑是我们日常打交道最多的伙伴之一。它简洁易用，性能尚可，支撑了无数 Go 应用的数据交换需求。然而，正如俗话所说，“最熟悉的地方可能藏着最深的坑”，最近拜读了知名安全公司 Trail of Bits 的一篇深度剖析文章——**“Unexpected security footguns in Go’s parsers”**（Go 解析器中意想不到的安全“绊脚石”）——让我对这个朝夕相处的伙伴有了全新的、甚至可以说是“惊出一身冷汗”的认识。

这篇文章系统性地揭示了 Go 标准库中的 JSON、XML（以及流行的第三方 YAML）解析器在处理**非受信数据**时，存在一些设计上或默认行为上的“特性”，这些“特性”在特定场景下很容易被攻击者利用，演变成严重的安全漏洞。文中提到的真实案例，如 Hashicorp Vault 的认证绕过 (CVE-2020-16250)，更是触目惊心。

今天，我们就结合 Trail of Bits 的这篇“檄文”，深入挖掘一下 Go 解析器（特别是我们最常用的 encoding/json）的那些“隐秘角落”，看看它们是如何成为安全陷阱的，并展望一下被寄予厚望的 JSONv2 将如何带来“救赎”。

## Go 解析器的“温柔一刀”：那些被忽视的默认行为

Trail of Bits 的文章通过三个核心的攻击场景，向我们展示了 Go 解析器的一些“意外行为”是如何被利用的。让我们聚焦于与 encoding/json (v1 版本，即我们目前广泛使用的版本) 相关的几个关键点：

### 场景一：非预期的序列化/反序列化

你以为你很好地控制了哪些数据该公开，哪些该保密？但encoding/json 的一些默认行为可能会让你大吃一惊。

- 无标签字段的“默认暴露”

Go 结构体中，如果一个字段没有 json 标签，encoding/json 在反序列化时会尝试使用该字段的**导出名**（首字母大写）作为 JSON 键进行匹配（大小写不敏感）。这可能导致开发者预期之外的数据被修改。

```
// https://go.dev/play/p/soIQPrr0GiI
package main
import (
"encoding/json"
"fmt"
)
type UserNoTag struct {
Username string // 没有 json 标签，但字段名是 Username
IsAdmin bool // 同样没有标签
}
func main() {
jsonData := {"Username": "attacker", "IsAdmin": true}
var u UserNoTag
err := json.Unmarshal([]byte(jsonData), &u)
if err != nil {
fmt.Println("Error:", err)
return
}
// 预期：可能希望 IsAdmin 不被外部设置
// 结果：u.IsAdmin 会被设置为 true
fmt.Printf("User: %+v\n", u) // Output: User: {Username:attacker IsAdmin:true}
}
```


在这个例子中，即使 IsAdmin 字段没有 json 标签，攻击者仍然可以通过提供名为 “IsAdmin” (或 “isAdmin”, “isadmin” 等) 的 JSON 键来设置其值。如果 IsAdmin 是一个敏感字段，这就构成了一个潜在的安全风险。Trail of Bits 指出，一个分心或经验不足的开发者可能就此引入漏洞。

- 误用 json:”-,omitempty”

json:”-” 标签的正确含义是“在序列化和反序列化时完全忽略此字段”。但如果错误地与 omitempty 组合成 json:”-,omitempty”，Go 解析器会将其解释为：此字段在 JSON 中的名称是 “-” (一个短横线字符串)，并且当其为空值时在序列化时省略。这意味着，它**不再被忽略**，而是可以通过名为 “-” 的 JSON 键来操作。看下面示例：

```
// https://go.dev/play/p/hmADZWNxk2Y
package main
import (
"encoding/json"
"fmt"
)
type UserMisuseDash struct {
Username string json:"username"
IsAdmin bool json:"-,omitempty" // 错误用法！
}
func main() {
// 攻击者尝试通过名为 "-" 的键设置 IsAdmin
jsonData := {"username": "guest", "-": true}
var u UserMisuseDash
err := json.Unmarshal([]byte(jsonData), &u)
if err != nil {
fmt.Println("Error:", err)
return
}
// 结果：u.IsAdmin 被成功设置为 true!
fmt.Printf("User: %+v\n", u) // Output: User: {Username:guest IsAdmin:true}
}
```


Trail of Bits 发现 Flipt 和 Langchaingo 等项目中都曾出现过这种误用，导致敏感字段可被外部控制。正确的忽略方式应该是 json:”-”。

- 误用 json:”omitempty” 作为字段名

这是一个更直接的错误：开发者本意是想为字段添加 omitempty 选项，却错误地将其写成了 JSON 键名。

```
// https://go.dev/play/p/FpH2Ff0pXZ6
package main
import (
"encoding/json"
"fmt"
)
type UserMisuseOmitempty struct {
Username string json:"username"
Role string json:"omitempty" // 错误！Role 字段在 JSON 中的名字变成了 "omitempty"
}
func main() {
jsonData := {"username": "user1", "omitempty": "admin"}
var u UserMisuseOmitempty
err := json.Unmarshal([]byte(jsonData), &u)
if err != nil {
fmt.Println("Error:", err)
return
}
// 结果：u.Role 被设置为 "admin"
fmt.Printf("User: %+v\n", u) // Output: User: {Username:user1 Role:admin}
}
```


Trail of Bits 在 GitHub 上搜索发现了多个知名项目（如 Gitea, Kustomize, Btcd, Evcc）中存在将字段 JSON 名错误设置为 omitempty 的情况。正确的做法应该是 json:”fieldName,omitempty” 或者如果想用默认字段名则是 json:”,omitempty”。

### 场景二：解析器差异性攻击

当同一个 JSON 数据被多个行为不一致的解析器处理时，攻击者可以利用这些差异性来绕过安全控制。

- 重复字段：Go 的 encoding/json 默认取最后一个同名键的值

```
// https://go.dev/play/p/uw0ElbJYrp9
package main
import (
"encoding/json"
"fmt"
)
type ActionRequest struct {
Action string json:"action"
}
func main() {
jsonData := {"action": "readData", "action": "deleteData"}
var req ActionRequest
err := json.Unmarshal([]byte(jsonData), &req)
if err != nil {
fmt.Println("Error:", err)
return
}
// Go 会取最后一个 "action" 的值
fmt.Printf("Request: %+v\n", req) // Output: Request: {Action:deleteData}
}
```


如果一个权限校验服务（可能用其他语言实现，或用了取第一个值的 Go JSON 库如 jsonparser）看到的是 “readData” 并放行，而实际执行业务逻辑的 Go 服务看到的是 “deleteData”，就可能导致权限绕过。

- 大小写不敏感的键名匹配：这是 encoding/json (v1) 一个广受诟病的特性

```
// https://go.dev/play/p/qaQlNq4bumo
package main
import (
"encoding/json"
"fmt"
)
type Config struct {
IsEnabled bool json:"isEnabled"
}
func main() {
jsonData := {"isenabled": true} // JSON 中键名是全小写
var cfg Config
err := json.Unmarshal([]byte(jsonData), &cfg)
if err != nil {
fmt.Println("Error:", err)
return
}
// 即使大小写不匹配，v1 版本的 encoding/json 也会成功赋值
fmt.Printf("Config: %+v\n", cfg) // Output: Config: {IsEnabled:true}
// 更危险的场景，结合重复键
jsonDataAttack := {"isEnabled": false, "isenabled": true}
var cfgAttack Config
json.Unmarshal([]byte(jsonDataAttack), &cfgAttack)
// 结果可能是 true，取决于最后一个匹配上的键 (isenabled)
fmt.Printf("Attack Config: %+v\n", cfgAttack) // Output: Attack Config: {IsEnabled:true}
}
```


Trail of Bits 强调这是 Go JSON 解析器最关键的缺陷之一，因为它与几乎所有其他主流语言的 JSON 解析器行为都不同（它们通常是严格大小写敏感的）。攻击者可以轻易构造 payload，如 {“action”: “UserAction”, “aCtIoN”: “AdminAction”}，利用这种差异性绕过权限检查。

### 场景三：数据格式混淆攻击

当一个解析器被错误地用来解析另一种格式的数据，或者其对输入数据的校验不够严格时，都可能为攻击者打开方便之门。

- 未知键 (Unknown keys) 的潜在风险

encoding/json (v1) 默认会**静默地忽略**输入 JSON 中，Go 目标结构体未定义的字段。虽然在简单场景下这只是数据被丢弃，但如果应用在后续流程中使用了更通用的方式（如 map[string]interface{}）来处理或透传原始 JSON 数据，这些被“忽略”的未知键就可能“复活”并造成危害。

```
// https://go.dev/play/p/85voViHyEEK
package main
import (
"encoding/json"
"fmt"
)
// 目标是解析成这个结构体，它没有 IsAdmin 字段
type UserProfile struct {
Username string json:"username"
Email string json:"email"
}
func processUserData(jsonData []byte) {
// 步骤 1: 尝试按预期结构体解析
var profile UserProfile
if err := json.Unmarshal(jsonData, &profile); err != nil {
fmt.Println("Error unmarshaling to UserProfile:", err)
// return
}
fmt.Printf("Parsed UserProfile: %+v\n", profile)
// 步骤 2: 假设后续流程或为了更灵活处理，
// 使用 map[string]interface{} 再次解析或直接用它承接原始数据
var rawData map[string]interface{}
if err := json.Unmarshal(jsonData, &rawData); err != nil {
fmt.Println("Error unmarshaling to map:", err)
return
}
fmt.Printf("Raw data map: %+v\n", rawData)
// 潜在风险点：如果后续逻辑不加区分地使用了 rawData 中的所有键值对
// 例如，直接将 rawData 用于更新数据库记录或传递给下游服务
if isAdmin, ok := rawData["isAdmin"].(bool); ok && isAdmin {
fmt.Println("!!! VULNERABILITY RISK: 'isAdmin' flag found in raw data and is true !!!")
// 这里可能就根据这个 isAdmin 执行了非预期的权限提升操作
}
}
func main() {
// 攻击者在 JSON 中加入了一个 UserProfile 结构体中不存在的 "isAdmin" 字段
maliciousJSON := {"username": "hacker", "email": "hacker@example.com", "isAdmin": true, "notes": "ignored by struct"}
fmt.Println("--- Processing Malicious Order (with unknown 'isAdmin' key) ---")
processUserData([]byte(maliciousJSON))
}
```


在这个例子中，json.Unmarshal 到 UserProfile 结构体时，isAdmin 和 notes 字段会被忽略。但是，当同一个 maliciousJSON 被解析到 map[string]interface{} 时，**所有键（包括 isAdmin 和 notes）都会被完整地保留下来**。如果后续的业务逻辑（比如权限判断、数据存储、传递给模板引擎或下游 API）不加小心地依赖了这个 rawData map，就可能错误地使用了攻击者注入的、未在预期结构体中定义的 isAdmin: true，从而导致权限提升或其他安全问题。这本质上是一种参数污染。

- 头部/尾部垃圾数据 (Leading/Trailing garbage data)

encoding/json (v1) 对输入数据的“纯净度”要求并非总是那么严格。json.Unmarshal通常期望输入是一个单一、完整的 JSON 值。如果JSON值后面跟着非空白的垃圾数据，它通常会报错。但是，如 Trail of Bits 指出的，json.Decoder 在处理流式数据时，如果使用其 Decode() 方法，它可能在成功解析流中的第一个有效 JSON 对象后，并不会因为流中后续存在“垃圾数据”而立即报错，而是成功返回。只有当尝试读取下一个 Token (例如调用 decoder.Token()) 并且该 Token 不是预期的 io.EOF 时，错误才会被显现。 下面Go 示例演示了 json.Decoder 对尾部垃圾数据的潜在容忍可能导致的问题：

```
// https://go.dev/play/p/bPTXaPHm6jD
package main
import (
"bytes"
"encoding/json"
"fmt"
"io"
)
type SimpleMessage struct {
Content string json:"content"
}
func main() {
fmt.Println("--- Testing Trailing Garbage Data with json.Decoder ---")
// 一个有效的 JSON 对象，后面跟着 "恶意payload"
jsonDataWithTrailing := {"content":"legit data"} malicious_payload_here
reader := bytes.NewReader([]byte(jsonDataWithTrailing))
decoder := json.NewDecoder(reader)
var msg SimpleMessage
// Decoder.Decode() 会尝试解码流中的下一个 JSON 值
err := decoder.Decode(&msg)
if err != nil {
// 如果 JSON 本身格式错误，这里会报错
fmt.Println("Initial Decode Error:", err)
} else {
// 第一个 JSON 对象被成功解码
fmt.Printf("Successfully Decoded Message: %+v\n", msg)
}
// 关键：检查 Decode 之后流中是否还有剩余数据
// Trail of Bits 指出这是 encoding/json 的一个开放 issue (golang/go#13407)，
// 即 Decoder.Decode 后面跟非空白字符不报错。
// 通常需要额外调用 decoder.Token() 并检查是否为 io.EOF 来确保流已耗尽。
var buf [1]byte
n, errPeek := reader.Read(buf[:]) // 尝试读取 Decode 之后的数据
if n > 0 {
fmt.Printf("!!! VULNERABILITY RISK: Trailing garbage data found after valid JSON: '%s'\n", string(buf[:n]))
// 在某些场景下，如果应用只调用 Decode() 一次且不检查流的末尾，
// 攻击者可能通过附加数据来尝试进行其他类型的攻击。
} else if errPeek == io.EOF {
fmt.Println("Stream fully consumed as expected.")
} else if errPeek != nil {
fmt.Println("Error peeking after decode:", errPeek)
} else {
fmt.Println("No trailing data or EOF not reached clearly.")
}
// 更规范的检查方式是使用 decoder.More() 或尝试再解码一个Token
fmt.Println("\n--- Proper check for trailing data ---")
reader2 := bytes.NewReader([]byte(jsonDataWithTrailing))
decoder2 := json.NewDecoder(reader2)
var msg2 SimpleMessage
decoder2.Decode(&msg2) // 解码第一个
// 尝试解码下一个token，期望是EOF
tok, errTok := decoder2.Token()
if errTok == io.EOF {
fmt.Println("Proper check: Stream fully consumed (EOF).")
} else if errTok != nil {
fmt.Printf("Proper check: Error after expected JSON object: %v (Token: %v)\n", errTok, tok)
} else if tok != nil {
fmt.Printf("!!! VULNERABILITY RISK (Proper check): Unexpected token after first JSON object: %v\n", tok)
}
}
```


如果应用逻辑仅仅依赖 decoder.Decode() 的单次成功返回，而没有后续检查（如确保流已到达 io.EOF），攻击者就可能在有效的 JSON 数据之后附加恶意数据。这些数据可能被后续的、未预期的处理流程读取，或者在某些HTTP请求劫持、请求伪造场景中被利用。Trail of Bits 指出这是一个已知的、但因兼容性等原因未计划修复的 issue (golang/go#13407)。

- XML 解析器的极端容忍度 (与 JSON 混淆)

虽然不是直接的 encoding/json 问题，但 Trail of Bits 强调了当数据格式处理发生混淆时（例如，用 XML 解析器去解析一个实际是 JSON 的响应），Go XML 解析器的宽松性可能导致严重问题。这提醒我们在处理任何外部输入时，都必须严格校验 Content-Type 并使用对应的正确解析器。

## JSONv2 的曙光：更安全的默认与更强的控制

面对 encoding/json (v1) 的这些“隐秘角落”，Go 社区和核心团队并没有坐视不理。Trail of Bits 的文章也将最终的希望寄托在了将以实验性特性 GOEXPERIMENT=jsonv2 存在于 Go 1.25的encoding/json/v2了。

根据官方提案 (GitHub Issue #71497) ，json/v2 在安全性方面将带来诸多关键改进，很多都直接针对上述的“痛点”：

**默认禁止重复名称：**v2 在遇到 JSON 对象中存在重复名称时，会**直接报错**，而不是像 v1 那样默默接受最后一个。**默认大小写敏感匹配：**v2 的字段匹配将采用**精确的、大小写敏感**的方式。虽然也提供了 MatchCaseInsensitiveNames 选项和 nocase 标签来兼容特定场景，但“默认安全”的原则得到了贯彻。**更强的未知键控制：**v2 提供了 RejectUnknownMembers 选项（虽然非默认启用，但行为等同于 v1 的 DisallowUnknownFields），并引入了 unknown 标签，允许开发者将未知字段捕获到指定的 map 或 jsontext.Value 类型的字段中，而不是简单忽略。**UnmarshalRead 校验 EOF：**v2 的 UnmarshalRead 函数（用于处理 io.Reader）会校验整个输入流直到 EOF，从而有效阻止尾部垃圾数据的问题。**更严格的 UTF-8 处理：**v2 默认要求严格的 UTF-8 编码，对无效 UTF-8 会报错。

这些改进，特别是**默认行为的调整**，将极大地提升 Go 应用在处理不可信 JSON 数据时的安全性，从源头上减少了许多潜在的漏洞。

## 给 Go 开发者的关键启示

在 JSONv2 真正成为主流之前，我们能做些什么来保护我们的 Go 应用呢？Trail of Bits 给出了一些宝贵的建议，结合 JSONv2 的趋势，我们可以总结为：

**默认启用严格解析：**- 对于 encoding/json (v1)，尽可能使用 Decoder.DisallowUnknownFields() 来禁止未知字段。
- 警惕并正确使用 json:”-” 来忽略字段，避免误用 json:”-,omitempty” 或 json:”omitempty” 作为字段名。

**保持服务边界的解析一致性：**当数据流经多个服务时（尤其是异构系统），确保所有环节对数据的解析行为（如重复键处理、大小写敏感性）是一致的。如果无法保证，需要在边界处增加额外的校验层。**警惕数据格式混淆：**严格校验输入数据的 Content-Type，确保使用正确的解析器处理对应的数据格式。**关注 JSONv2 的进展：**积极了解 JSONv2 的设计和特性，为未来可能的迁移做好准备，并理解其带来的安全增益。**利用静态分析工具：**Trail of Bits 提供了一些 Semgrep 规则来帮助检测代码库中常见的 JSON 解析误用模式。将静态分析集成到 CI/CD 流程中。**编写明确的测试用例：**针对反序列化逻辑，编写包含各种边界情况（如重复键、不同大小写的键、未知键、垃圾数据）的测试用例，确保解析行为符合预期。

## 小结

Trail of Bits 的这篇文章为我们所有 Go 开发者敲响了警钟：即使是像 encoding/json 这样基础、常用的标准库，也可能因为一些不符合直觉的默认行为或被忽视的配置，而成为安全攻击的突破口。

理解这些“隐秘角落”，认识到“便利”与“安全”之间的权衡，并积极拥抱像 JSONv2 这样的改进，是我们构建更健壮、更安全的 Go 应用的必经之路。在日常开发中，对任何外部输入都保持一份警惕，审慎处理数据的解析与校验，应成为我们每个人的习惯。

**你是否在项目中遇到过类似 Go 解析器的“坑”？你对 JSONv2 有哪些期待？欢迎在评论区分享你的经验和看法！** 如果觉得本文对你有所启发，也请不吝点个【赞】和【在看】，让更多 Gopher 关注 Go 的解析器安全！

资料地址：https://blog.trailofbits.com/2025/06/17/unexpected-security-footguns-in-gos-parsers/

**你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？**

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