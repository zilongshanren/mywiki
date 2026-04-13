---
title: Go开发者必读：JSON 的跨语言陷阱与 Go 防御指南
url: https://tonybai.com/2025/10/09/json-isnt-json/
published: '2025-10-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go开发者必读：JSON 的跨语言陷阱与 Go 防御指南

![](../../assets/913ead80d049708e.png)


[本文永久链接](https://tonybai.com/2025/10/09/json-isnt-json) – https://tonybai.com/2025/10/09/json-isnt-json

大家好，我是Tony Bai。

JSON (JavaScript Object Notation)，以其简洁、轻量、人类可读的特性，早已成为 Web API 和系统集成的“通用语”。它的承诺是：“一次编写，随处解析”。然而，这份看似美好的承诺背后，隐藏着一个被许多开发者忽略的残酷现实：**JSON 并不像其规范所暗示的那样通用。**

它的简约性，恰恰为其留下了太多“解释空间”。当 JavaScript 前端、Go 后端、Python 数据管道、以及 Java 企业服务开始以各自的方式“解释”同一个 JSON 时，一个现代版的“巴别塔”便悄然建起：**每个人都在说 JSON，但每个人表达的意思却可能不尽相同**。

这篇文章，是一份为 Go 开发者量身定制的“防御指南”，将为你全面揭示 JSON 在跨语言环境中最隐蔽、最危险的几大陷阱，并展示如何利用 Go 的特性（包括实验性的 [json/v2](https://tonybai.com/2025/05/15/go-json-v2)）来构建坚不可摧的防线。

![](../../assets/e7aa987414f58103.png)


## 陷阱一：数字精度 —— 无声的整数溢出

这是 JSON 跨语言中最常见、也最致命的陷阱。

**问题根源**：JavaScript 将所有数字都表示为 64 位浮点数，其能精确表示的最大安全整数是 Number.MAX_SAFE_INTEGER (2^53 – 1)。任何超过这个值的整数，都会在解析时**无声地丢失精度**。

```
{ "id": 9007199254740993 }
```


- 在
**JavaScript**中，JSON.parse 会得到 9007199254740992 (错误！)。 - 在
**Python**或**Java**中，则能正确解析。

Go 的 encoding/json (v1) 在处理数字时，若反序列化到 interface{}，会**默认将所有 JSON 数字解析为 float64**，从而掉入和 JavaScript 同样的精度陷阱。

-
**v1 陷阱**：`// demo1/main.go package main import ( "encoding/json" "fmt" ) func main() { jsonData := []byte({"id": 9007199254740993}) var data map[string]interface{} json.Unmarshal(jsonData, &data) // id 被解析为 float64，精度丢失！ fmt.Printf("v1 with interface{}: %.0f\n", data["id"]) // 输出: 9007199254740992 }`

-
**v2 行为**：[Go 1.25版本](https://tonybai.com/2025/08/15/some-changes-in-go-1-25)引入的实验性的 encoding/json/v2 在此行为上与 v1 保持一致，反序列化到 any 时同样默认使用 float64。

**Go 防御指南**：

**首选强类型结构体**：这是最根本的解决方案。始终使用带有明确整型（如 int64）的结构体来反序列化。

`go`


var typed struct { ID int64 json:"id" }

json.Unmarshal(jsonData, &typed)

fmt.Println(typed.ID) // 输出: 9007199254740993**拥抱“数字即字符串”**：对于所有需要跨语言传递的、可能会超过 2^53 – 1 的整数 ID（如数据库自增 ID），最佳实践是在 API 层面约定俗成地使用**字符串**类型。

## 陷阱二：浮点数运算 —— 0.1 + 0.2 ≠ 0.3

这个问题并非 JSON 独有，而是 IEEE 754 浮点数标准的“天性”。由于计算机使用二进制表示数字，像 0.1 这样的十进制小数无法被精确表示，只能存储一个近似值。当 JSON 依赖于各语言的默认数字实现时，这个问题在跨语言交互中就会被放大。

```
{ "price": 0.1 }
```


Go 的 encoding/json（包括 v1 和实验性的 v2）在反序列化 JSON 时，默认会将带小数点的数字解析为 float64 类型，这使得 Go 程序同样会遇到和 JavaScript 一样的精度问题：

```
// demo2/main.go
package main
import (
"encoding/json"
"fmt"
)
func main() {
// 包含浮点数的 JSON
jsonData := []byte({"price": 0.1})
// 定义一个结构体，使用 float64 来接收 price 字段
var product struct {
Price float64 json:"price"
}
// 反序列化
if err := json.Unmarshal(jsonData, &product); err != nil {
panic(err)
}
// 单独打印时，浮点数通常会以最短、最精确的十进制形式显示
fmt.Println("Parsed price:", product.Price)
// 当进行算术运算时，其底层的二进制不精确性就会暴露出来
result := product.Price + 0.2
fmt.Println("product.Price + 0.2 =", result)
// 为了对比，直接在 Go 中进行浮点数运算
fmt.Println("0.1 + 0.2 directly in Go =", float64(0.1)+float64(0.2))
}
```


**输出：**

```
Parsed price: 0.1
product.Price + 0.2 = 0.30000000000000004
0.1 + 0.2 directly in Go = 0.30000000000000004
```


这个例子清晰地表明，问题不在于 JSON 解析本身，而在于使用 float64 进行后续计算。对于金融、科学计算等要求精确的场景，这种微小的误差累积起来可能是致命的。

**Go 防御指南**：

**永远不要使用 float64 来处理货币或任何要求精确计算的场景。** 建议大家遵循以下模式：

**使用字符串传输**：在 JSON 中将金额表示为字符串（如 “19.99″），在 Go 中使用 github.com/shopspring/decimal 或 math/big.Rat 等高精度库进行处理。**使用整数单位**：将金额转换为最小单位的整数（如“分”）进行传输和计算，例如用 1999 代表 19.99 元。这是在工程实践中非常常见且高效的解决方案。

## 陷阱三：Unicode 规范化 —— 看似相同的“José”

Unicode 允许同一个字符（如 é）有多种字节表示方式（单一码点 vs. 组合形式）：

```
单一码点: U+00E9 (é)
组合形式: U+0065 U+0301 (e + ́)
```


显然，这两种编码形式的字节序列和长度都不同。但在视觉上的呈现却完全相同，都是é。不过，如果直接比较，会返回 false。JSON 规范对此未做规定。

**Go 防御指南**：

这并非 encoding/json 包的职责，但作为 Go 开发者必须了解。在进行任何需要比较、索引或持久化的字符串操作之前，**必须对 Unicode 字符串进行规范化**。Go 的 golang.org/x/text/unicode/norm 包为此提供了强大的工具：

```
// demo3/main.go
package main
import (
"fmt"
"golang.org/x/text/unicode/norm"
)
func main() {
name1 := "José"
name2 := "Jose\u0301"
fmt.Println(name1 == name2) // 输出: false
// 使用 NFC 形式进行规范化后再比较
fmt.Println(norm.NFC.String(name1) == norm.NFC.String(name2)) // 输出: true
}
```


## 陷阱四：对象键序 —— 加密签名的噩梦

JSON 规范明确指出：“对象是无序的键值对集合。” 然而，在 [HMAC 签名、内容哈希](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4082448928904577033#wechat_redirect)、缓存键生成等需要**字节级别稳定性**的场景中，我们又隐式地依赖于一个确定的序列化顺序。

对此，不同语言和库对此的处理方式大相径庭：

**JavaScript (ES2015+)**和**Python (3.7+)**：在现代版本中，它们都倾向于**保留对象键的插入顺序**。**Java**: 依赖于具体的 Map 实现，LinkedHashMap 保留顺序，而 HashMap 不保证。**Go (v1 & v2)**：行为最为独特和明确。**反序列化/迭代**：Go 的 map 迭代顺序是**故意随机化**的。**序列化 map**：encoding/json 在序列化 map 时，会**默认按字母顺序对键进行排序**。**序列化 struct**：会**遵循结构体中字段的定义顺序**。


这种不一致性，是导致加密操作在开发环境（例如，JS fetch）和生产环境（Go 后端）之间签名验证失败的常见元凶。

下面的例子模拟了一个场景：一个 JavaScript 前端和一个 Go 后端，对相同的业务数据生成 HMAC 签名。

```
// demo4/main.go
package main
import (
"crypto/hmac"
"crypto/sha256"
"encoding/hex"
"encoding/json"
"fmt"
)
func main() {
// --- 问题场景 ---
// 假设两个不同的系统需要对相同的业务数据进行签名。
// 系统 1: 一个 JavaScript 服务，它保留了对象属性的插入顺序。
// 注意键的顺序: "currency" 在前, "amount" 在后。
jsONString := {"currency":"USD","amount":100}
fmt.Printf("JSON from JS-like system: %s\n", jsONString)
// 系统 2: 一个 Go 服务，它序列化一个 map。
data := map[string]interface{}{
"currency": "USD",
"amount": 100,
}
// Go 的 json.Marshal 会对 map 的键按字母顺序排序。
// 因此 "amount" 会排在 "currency" 前面。
goJSONBytes, _ := json.Marshal(data)
goJSONString := string(goJSONBytes)
fmt.Printf("JSON from Go system (map): %s\n", goJSONString)
// --- 导致的后果: 加密签名失败 ---
secret := []byte("my-super-secret-key")
// 为 JS 风格的 JSON 字符串计算 HMAC
hmacJS := calculateHMAC(secret, []byte(jsONString))
fmt.Printf("HMAC for JS JSON: %s\n", hmacJS)
// 为 Go 生成的 JSON 字符串计算 HMAC
hmacGo := calculateHMAC(secret, goJSONBytes)
fmt.Printf("HMAC for Go JSON: %s\n", hmacGo)
// 比较两个签名
signaturesMatch := hmac.Equal([]byte(hmacJS), []byte(hmacGo))
fmt.Printf("\nDo the signatures match? %t\n", signaturesMatch)
if !signaturesMatch {
fmt.Println("Authentication Fails! The byte representations were different.")
}
}
// calculateHMAC 是一个辅助函数，用于计算并编码 HMAC 值
func calculateHMAC(secret, data []byte) string {
h := hmac.New(sha256.New, secret)
h.Write(data)
return hex.EncodeToString(h.Sum(nil))
}
```


运行这个示例，得到下面输出：

```
JSON from JS-like system: {"currency":"USD","amount":100}
JSON from Go system (map): {"amount":100,"currency":"USD"}
HMAC for JS JSON: 6e79a600ccff47618144c12713f24af06b3278eef5b895f61bb6c74fde2d861e
HMAC for Go JSON: fe2d3217a0ddcbe8a5879f42703124c31824b87747d017e61e3f7ce8a289e7f7
Do the signatures match? false
Authentication Fails! The byte representations were different.
```


这个例子清晰地表明，尽管两份 JSON 在语义上完全等价，但由于字节表示不同，最终导致了签名验证失败。

**Go 防御指南**：

对于任何需要字节级一致性的操作，**必须使用“规范化 JSON” (Canonical JSON)**。最简单的规范化方法，就是在序列化前，**始终对对象的键按字母顺序进行排序**。

幸运的是，Go 的 encoding/json 在处理 map 时**默认就在这样做**，这反而使 Go 在处理这类问题时，比其他语言更具天生的健 robustness。当你需要确保跨语言的签名一致性时，应确保所有其他语言的客户端在生成 JSON 签名负载时，也遵循相同的键排序规则。

## 陷阱五：空值的迷思 —— null vs. 零值 vs. 缺失

如何在 JSON 中表达“值的缺失”？这是一个比看起来要复杂得多的问题，因为不同语言对此有不同的理解。

**JavaScript**：拥有 null（显式为空）和 undefined（从未定义）两个概念。**Python**：用 None 表示，序列化为 null。**Go**：Go 的静态类型系统为我们提供了精确控制的能力，但同时也需要开发者理解其背后的模式和权衡。

**解码时的核心挑战:**

在解码（反序列化）时，我们常常需要处理三种不同的状态：

**提供了具体的值**（如 “description”: “A user”）**显式地提供了 null**（如 “description”: null）**完全没有提供该字段**（missing）

当使用 map[string]interface{} 时，你**无法区分**一个键在 JSON 中是被显式设置为 null，还是根本就不存在，因为这两种情况都会导致 map 中的值为 nil。

**Go 防御指南：分层解决方案**

### 第一层防御（95% 的场景）：用指针区分“零值”与“值的缺失”

在绝大多数 API 设计（尤其是 PATCH 请求）中，我们最关心的其实是区分**“用户想把字段更新为一个空值/零值”**（例如 “” 或 0）和**“用户根本不想碰这个字段”**。

对于这个核心需求，**指针字段是 Go 最地道、最简洁的解决方案**。

```
// demo5/main1.go
package main
import (
"encoding/json"
"fmt"
)
type UserUpdatePayload struct {
Nickname string json:"nickname"
Description *string json:"description" // 指针字段表示可选
}
func main() {
// 场景一：用户想将 description 更新为空字符串 ""
jsonWithValue := []byte({"nickname":"Gopher", "description":""})
var u1 UserUpdatePayload
json.Unmarshal(jsonWithValue, &u1)
fmt.Printf("Scenario 1 (Zero Value): Description is nil: %t, Value: '%s'\n", u1.Description == nil, *u1.Description)
// 场景二：用户未提供 description 字段 (无论是显式 null 还是 missing)
jsonWithoutValue := []byte({"nickname":"Gopher"}) // or {"description":null}
var u2 UserUpdatePayload
json.Unmarshal(jsonWithoutValue, &u2)
fmt.Printf("Scenario 2 (Absence): Description is nil: %t\n", u2.Description == nil)
}
```


**输出：**

```
Scenario 1 (Zero Value): Description is nil: false, Value: ''
Scenario 2 (Absence): Description is nil: true
```


这个例子清晰地表明，指针字段**完美地区分了“零值” (“”) 和“值的缺失” (nil)**。对于大多数业务场景，将显式的 null 和 missing 都视为“值的缺失”，是一种合理且有效的简化。

### 第二层防御（高级场景）：当必须区分 null 与 missing 时

然而，在某些严格的 API 或数据同步场景中，你可能**必须**区分“用户显式地将值设为 null”和“用户完全没有提及这个字段”。

对于这种高级需求，简单的结构体与指针已不足够。我们需要借助 json.RawMessage 来实现终极控制。

```
// demo5/main2.go
package main
import (
"encoding/json"
"fmt"
)
func main() {
// 场景一：description 显式为 null
jsonWithNull := []byte({"name":"Gopher", "description":null})
// 场景二：description 字段缺失
jsonMissing := []byte({"name":"Gopher"})
distinguish(jsonWithNull)
distinguish(jsonMissing)
}
func distinguish(jsonData []byte) {
// 步骤 1: 解码到一个 map[string]json.RawMessage
var raw map[string]json.RawMessage
if err := json.Unmarshal(jsonData, &raw); err != nil {
panic(err)
}
// 步骤 2: 检查 "description" 键是否存在
descData, ok := raw["description"]
if !ok {
fmt.Println("Result: 'description' key is MISSING.")
return
}
// 步骤 3: 如果键存在，检查其内容是否为 "null"
if string(descData) == "null" {
fmt.Println("Result: 'description' key is explicitly NULL.")
return
}
// 如果存在且不为 null，则可以进一步解码
var desc string
json.Unmarshal(descData, &desc)
fmt.Printf("Result: 'description' has value: %s\n", desc)
}
```


**输出：**

```
Result: 'description' key is explicitly NULL.
Result: 'description' key is MISSING.
```


这个模式虽然更复杂，但它提供了最精确的控制。它首先检查键是否存在于 map 中，如果存在，再检查其原始的 JSON 文本是否就是 null。

## 陷阱六：时间格式 —— 无尽的变体

JSON 规范没有原生的日期时间类型，这是一个“历史遗留问题”，导致了社区在实践中发展出多种多样的表示方式，成了一个“标准分裂”的重灾区。

一个典型的跨语言 API 可能会收到如下混合格式的 JSON：

```
{
"iso_string": "2023-01-15T10:30:00.000Z",
"unix_timestamp": 1673780200,
"unix_milliseconds": 1673780200000,
"date_only": "2023-01-15",
"custom_format": "15/01/2023 10:30:00"
}
```


不同语言的库对这些格式的默认解析行为千差万别，极易出错。例如，JavaScript 的 new Date() 构造函数在处理 Unix 时间戳时，期望的是毫秒而非秒，这常常导致微妙的 bug。

**Go 防御指南**：

Go 的 time.Time 类型及其与 encoding/json 的集成，为处理这种混乱提供了强大而灵活的工具。

-
**善用 time.Time 的默认行为**：Go 的 time.Time 类型在 json.Unmarshal 时，**默认就能正确解析符合 RFC 3339 标准（ISO 8601 的一个常见子集）的字符串**。这是最推荐、最无痛的方式。 -
**为非标准格式实现自定义 UnmarshalJSON**：对于 Unix 时间戳或其他自定义格式，我们可以通过为自定义类型实现 json.Unmarshaler 接口，来精确控制解析逻辑。

下面的例子展示了如何在一个结构体中，优雅地处理上述所有时间格式。

```
//demo6/main.go
package main
import (
"encoding/json"
"fmt"
"strconv"
"time"
)
// CustomTime 是一个自定义类型，用于处理非标准的 "DD/MM/YYYY HH:MM:SS" 格式
type CustomTime struct {
time.Time
}
// 为 CustomTime 实现 UnmarshalJSON 接口
func (ct *CustomTime) UnmarshalJSON(b []byte) error {
// 首先去除字符串的引号
s, err := strconv.Unquote(string(b))
if err != nil {
return err
}
// 定义我们期望的格式
const layout = "02/01/2006 15:04:05"
t, err := time.Parse(layout, s)
if err != nil {
return err
}
ct.Time = t
return nil
}
// UnixTime 是一个自定义类型，用于处理以秒为单位的 Unix 时间戳
type UnixTime struct {
time.Time
}
func (ut *UnixTime) UnmarshalJSON(b []byte) error {
// 将 JSON 数字转换为 int64
unixSec, err := strconv.ParseInt(string(b), 10, 64)
if err != nil {
return err
}
ut.Time = time.Unix(unixSec, 0)
return nil
}
// Event 结构体包含了所有不同格式的时间字段
type Event struct {
ISOString time.Time json:"iso_string" // 标准库直接支持
UnixTimestamp UnixTime json:"unix_timestamp" // 自定义类型处理
UnixMilliseconds int64 json:"unix_milliseconds" // 直接用 int64 接收
DateOnly string json:"date_only" // 简单情况用 string
CustomFormat CustomTime json:"custom_format" // 自定义类型处理
}
func main() {
jsonData := []byte({
"iso_string": "2023-01-15T10:30:00.000Z",
"unix_timestamp": 1673780200,
"unix_milliseconds": 1673780200000,
"date_only": "2023-01-15",
"custom_format": "15/01/2023 10:30:00"
})
var event Event
if err := json.Unmarshal(jsonData, &event); err != nil {
panic(err)
}
fmt.Printf("ISO String: %s\n", event.ISOString.UTC())
fmt.Printf("Unix Timestamp: %s\n", event.UnixTimestamp.UTC())
// 从毫秒时间戳创建 time.Time
msTime := time.UnixMilli(event.UnixMilliseconds)
fmt.Printf("Unix Milliseconds: %s\n", msTime.UTC())
fmt.Printf("Date Only: %s\n", event.DateOnly)
fmt.Printf("Custom Format: %s\n", event.CustomFormat.UTC()) // 假设 custom format 也是 UTC
}
```


**运行这个示例输出：**

```
ISO String: 2023-01-15 10:30:00 +0000 UTC
Unix Timestamp: 2023-01-15 10:56:40 +0000 UTC
Unix Milliseconds: 2023-01-15 10:56:40 +0000 UTC
Date Only: 2023-01-15
Custom Format: 2023-01-15 10:30:00 +0000 UTC
```


这个示例清晰地展示了 Go 在处理时间格式时的灵活性和健壮性。

## 陷阱七：错误处理 —— 宽容还是严格？

对于不规范的 JSON（如尾随逗号、重复的键），不同解析器的行为也大相径庭。

Go在jsonv1和jsonv2中对不规范json的错误处理略有差异，下面我们看一个示例在jsonv1和jsonv2下的不同表现。

```
// demo7/main.go
package main
import (
"encoding/json" // 在jsonv2时，改为"encoding/json/v2"
"fmt"
)
func main() {
var data map[string]int
// Duplicate keys - last value wins (no error)
err := json.Unmarshal([]byte({"a": 1, "a": 2}), &data)
if err != nil {
fmt.Println("Duplicate key error:", err)
} else {
fmt.Printf("Duplicate keys allowed, value: %d\n", data["a"]) // 2
}
// Trailing commas - error
err = json.Unmarshal([]byte({"a": 1,}), &data)
if err != nil {
fmt.Println("Trailing comma error:", err)
}
// Leading zeros - error
err = json.Unmarshal([]byte({"num": 007}), &data)
if err != nil {
fmt.Println("Leading zeros error:", err)
}
// Single quotes - error
err = json.Unmarshal([]byte({'a': 1}), &data)
if err != nil {
fmt.Println("Single quotes error:", err)
}
}
```


上述示例在json/v1下的运行结果：

```
Duplicate keys allowed, value: 2
Trailing comma error: invalid character '}' looking for beginning of object key string
Leading zeros error: invalid character '0' after object key:value pair
Single quotes error: invalid character '\'' looking for beginning of object key string
```


而在Go 1.25.0 GOEXPERIMENT=jsonv2下的运行结果如下：

```
Duplicate key error: jsontext: duplicate object member name "a"
Trailing comma error: jsontext: invalid character ',' at start of value after offset 7
Leading zeros error: jsontext: invalid character '0' after object value (expecting ',' or '}') after offset 9
Single quotes error: jsontext: invalid character '\'' at start of value after offset 1
```


**Go 防预指南：v1 的宽容与 v2 的严格**

**坚持最小公分母原则**。在生成 JSON 时，始终产出最严格、最符合 RFC 8259 规范的格式。Go 的 encoding/json (v1) 在这方面表现得相对严格，但在某些地方又过于“宽容”。实验性的 json/v2 则旨在提供更严格、更安全的默认行为。

让我们结合上面的例子输出，来具体对比 v1 和 v2 在处理不规范 JSON 时的行为差异：

**1. 重复的键 (Duplicate Keys)**

-
**v1 行为：“最后出现者获胜”**`Duplicate keys allowed, value: 2`

json/v1 默认

**允许**对象中出现重复的键，并且不会报错。最后一个出现的值会**无声地覆盖**前面的值。这是一种非常危险的行为，因为它可能导致难以追踪的数据丢失或状态不一致问题。 -
**v2 行为：显式错误**`Duplicate key error: jsontext: duplicate object member name "a"`

json/v2 默认会

**拒绝**带有重复键的 JSON，并返回一个清晰的错误。这是一个**重大的安全改进**，它将一个潜在的、静默的数据损坏风险，转变为一个在解析阶段就能被立即捕获的编译时错误，强制开发者修正不规范的数据源。

**2. 尾随逗号 (Trailing Commas)**

-
**v1 行为：语法错误**`Trailing comma error: invalid character '}' looking for beginning of object key string`

v1 正确地拒绝了尾随逗号，但其错误信息略显晦涩。它告诉你它在 } 字符处遇到了问题，因为它期望看到下一个键的开始，而不是直接暗示问题在于前一个多余的逗号。

-
**v2 行为：更精确的错误**`Trailing comma error: jsontext: invalid character ',' at start of value after offset 7`

v2 同样拒绝了尾随逗号，但它的错误信息

**更加精确**。它直接指出了问题字符是 ,，并给出了其在字节流中的确切偏移位置 (offset 7)，极大地提升了调试效率。

**3. 数字中的前导零 (Leading Zeros)**

-
**v1 行为：语法错误**`Leading zeros error: invalid character '0' after object key:value pair`

v1 拒绝了不符合 JSON 规范的八进制风格数字 007，但错误信息同样不够直观。

-
**v2 行为：更精确的错误**`Leading zeros error: jsontext: invalid character '0' after object value (expecting ',' or '}') after offset 9`

v2 的错误信息再次胜出，它明确指出了在数字值之后遇到的无效字符 0，并提示了此处期望的字符（, 或 }），让开发者能更快地定位问题。


**4. 使用单引号 (Single Quotes)**

**v1 & v2 行为对比**

`v1: Single quotes error: invalid character '\'' looking for beginning of object key string`


v2: Single quotes error: jsontext: invalid character '\'' at start of value after offset 1

两种版本都正确地拒绝了使用单引号的 JSON 字符串（规范要求必须使用双引号）。同样地，v2 提供了带有偏移位置的、更利于调试的错误信息。

对于 Go 开发者而言，这意味着 json/v2 不仅仅是一个性能上的升级，更是在**健壮性和开发者体验**上的一次意义深远的飞跃，这些改变使得 Go 在处理 JSON 时的默认行为更加安全。

## 小结

JSON 的优雅简洁是其最大的优点，但也是其最危险的弱点。当你的 Go 服务开始与一个由不同团队、不同语言、不同假设构建的复杂系统进行交互时，这种弱点就会被放大，演变成一系列难以追踪、足以毁掉整个周末的“灵异事件”：无声丢失精度的用户 ID、因键序不同而验证失败的 HMAC 签名、看似相同却无法匹配的 Unicode 用户名……

解决方案不是抛弃 JSON，而是放弃“它在任何地方都一样”的天真幻想。幸运的是，对于 Go 开发者而言，我们拥有一个强大的“军火库”来应对这场跨语言的“阵地战”。

这份“防御指南”的核心，可以浓缩为以下几条可立即执行的军规：

-
**首选强类型 struct**：这是你的第一道，也是最坚固的一道防线。它能从根本上解决数字精度丢失、null 与缺失的歧义等一系列问题。请将 map[string]interface{} 留给那些你必须处理未知结构的场景。 -
**ID 用字符串，金额用整数**：对于所有可能超过 JavaScript 安全整数范围的 ID，请在 API 层面约定俗成地使用**字符串**类型。对于所有货币和精确计算，请将其转换为最小单位的**整数**（如“分”）进行传输。 -
**规范化你的字符串，统一你的时间**：在处理任何来自外部的 Unicode 字符串之前，先用 golang.org/x/text/unicode/norm 将其“消毒”。在 API 契约中，强制规定所有时间都使用**ISO 8601 格式的 UTC 字符串**，并始终在你的 struct 中使用 time.Time。 -
**善用指针与标签**：在解码时，用**指针字段**来处理“值的缺失”。在编码时，精准地使用 omitempty/omitzero。 -
**拥抱 json/v2 的严格性**：实验性的 json/v2 并非简单的性能优化，它在安全性和正确性上迈出了重要一步。其默认**拒绝重复键**的行为，将一个潜在的数据损坏风险，提升为了一个可在开发阶段就立即捕获的错误。这是 Go 语言在 JSON 处理上走向成熟的重要标志。

请记住：在一个由不完美标准和人类（以及未来的 AI）编写的解析器组成的世界里，一点点怀疑精神，将大有裨益。**信任，但要验证**。

本文涉及到的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/json-isnt-json)下载。

## 参考资料

- json spec – https://www.json.org/json-en.html
- https://blog.dochia.dev/blog/json-isnt-json/

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


**想系统学习Go，构建扎实的知识体系？**

我的新书《[Go语言第一课](https://book.douban.com/subject/37499496/)》是你的首选。源自2.4万人好评的极客时间专栏，内容全面升级，同步至Go 1.24。首发期有专属五折优惠，不到40元即可入手，扫码即可拥有这本300页的Go语言入门宝典，即刻开启你的Go语言高效学习之旅！

![](../../assets/d3fd3ab3e1fd7a7e.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论