---
title: 手把手带你玩转GOEXPERIMENT=jsonv2：Go下一代JSON库初探
url: https://tonybai.com/2025/05/15/go-json-v2/
published: '2025-05-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 手把手带你玩转GOEXPERIMENT=jsonv2：Go下一代JSON库初探

![](../../assets/fb083c29b2259fb5.png)


[本文永久链接](https://tonybai.com/2025/05/15/go-json-v2) – https://tonybai.com/2025/05/15/go-json-v2

大家好，我是Tony Bai。

Go 语言标准库中的 encoding/json 包，无疑是我们日常开发中使用频率最高的包之一。它为 Go 社区服务了十多年，几乎无处不在。但与此同时，它也因一些历史遗留的 API 缺陷、行为不一致以及在某些场景下的性能瓶颈而受到过不少讨论和批评。社区中甚至涌现出像Sonic、go-json、easyjson 等一系列高性能的第三方 JSON 库作为替代。

令人兴奋的是，Go 官方团队终于开始着手对 encoding/json 进行一次意义深远的升级——这就是 **encoding/json/v2** 的由来。虽然json/v2 尚未正式发布，但其核心代码已经合并到 Go 的开发分支，并可以通过一个实验性特性标志 **GOEXPERIMENT=jsonv2** 来提前体验！

今天，我就来手把手带大家玩转这个实验性特性，通过官方提供的 gotip 工具，亲自动手体验一下 Go 下一代 JSON 库到底带来了哪些令人期待的改进，特别是在行为正确性和性能方面。

## 背景回顾：为何需要 json/v2？—— encoding/json (v1) 的“四宗罪”

在深入实践之前，我们有必要回顾一下 encoding/json (v1) 长期以来积累的一些核心痛点。这些痛点也是催生 json/v2 的根本原因。Go 官方的 json/v2 提案（详见 GitHub Issue #71497）将这些缺陷归纳为四大类：

**行为缺陷**

**大小写不敏感的字段名匹配：**v1 在反序列化时，JSON 对象中的字段名与 Go 结构体字段的 JSON Tag 或字段名进行匹配时，采用的是大小写不敏感的策略。这虽然在某些情况下提供了便利，但并不符合 JSON 规范的最新趋势（RFC 8259 强调对象名是大小写敏感的），也可能导致非预期的匹配。**重复键处理不明确：**当输入的 JSON 对象包含重复的键名时，v1 的行为是不确定的（通常是后者覆盖前者），并且不会报错。这违反了 RFC 8259 中关于名称唯一性的建议，可能导致数据丢失或解析混乱。**无效 UTF-8 的静默替换：**v1 在遇到无效的 UTF-8 字节序列时，会将其静默地替换为 Unicode 替换字符 (U+FFFD)，而不是报错。v2 则默认要求严格的 UTF-8。**反序列化 null 到非空 Go 值的行为不一致：**v1 在此场景下行为不统一，有时清零有时保留原值。v2 则统一为清零。**合并 (Merge) 语义不一致：**v1 在反序列化到已有的非零 Go 值时，其合并行为在不同类型（如 struct 字段 vs map 值）之间存在差异。v2 对合并语义进行了重新设计。

**功能缺失**

**缺乏灵活的时间格式化支持：**v1 强制要求时间字符串符合 RFC 3339 格式，无法方便地处理其他常见的时间格式。**对 omitempty 的定义局限：**v1 的 omitempty 基于 Go 类型的零值判断，对于某些场景（如希望指针为 nil 时才省略，而不是其指向的值为空时省略）不够灵活。v2 重新定义了 omitempty 并引入了 omitzero。注：[v1版本也已经加入对omitzero支持的补丁](https://tonybai.com/2024/09/12/solve-the-empty-value-dilemma-in-json-encoding-with-omitzero/)。**处理未知字段不便：**v1 默认会丢弃 JSON 对象中未在 Go 结构体中定义的字段，缺乏一种内建的、优雅的方式来捕获这些未知字段。**nil Slice/Map 的序列化行为：**v1 将 nil slice 和 nil map 序列化为 JSON null，而许多用户期望它们被序列化为空数组 [] 和空对象 {}。

**API 缺陷**

**缺乏对 io.Reader 和 io.Writer 的一流支持：**v1 的核心 API Marshal 和 Unmarshal 主要操作 []byte，与 Go 广泛使用的 io.Reader/Writer 接口范式不够协调，导致需要额外的缓冲或转换。**Decoder.DisallowUnknownFields 和 Decoder.UseNumber 等配置方式不够灵活：**这些配置是解码器级别的，难以针对特定类型或字段进行细粒度控制。

**性能限制**

**反射开销：**v1 严重依赖反射，尤其是在处理大型、复杂的 JSON 对象或高频次的序列化/反序列化操作时，性能可能成为瓶颈。**内存分配：**在某些情况下，v1 的内存分配策略可能不是最优的，导致不必要的内存分配和 GC 压力。

正是为了系统性地解决这些问题，并提供一个更正确、更灵活、更高性能的 JSON 处理方案，json/v2 应运而生。

## 准备工作：安装并使用 gotip

要体验 Go 开发分支中的特性，我们需要使用 gotip 这个官方工具。gotip 可以下载并运行 Go 最新的（可能是未发布的）源代码版本。

**安装 gotip:**

```
$go install golang.org/dl/gotip@latest
```


**下载最新的 Go tip 版本:**

```
$gotip download
```


这个命令会使用你当前安装的 Go 版本来编译 Go 的 tip 版本。这个过程可能需要几分钟，因为它需要从源码构建整个 Go 工具链。耐心等待完成。

完成后，你就可以使用 gotip run、gotip build、gotip test 等命令来运行使用 Go tip 版本的代码了，就像使用普通的 go 命令一样。

注：更多关于安装gotip版本的内容，可以参考我之前写的《

[Gotip安装：基于Go镜像代码仓库]》。

## 开启 json/v2 实验特性

要启用 json/v2，我们需要在执行 gotip 命令时设置一个环境变量[GOEXPERIMENT](https://tonybai.com/2024/10/11/go-evolution-dual-insurance-goexperiment-godebug)：

```
$GOEXPERIMENT=jsonv2 gotip <command>
```


设置后，当你在示例代码中导入 “encoding/json/v2″ 包时，Go编译器就会选择使用v2版本的json包对源码进行编译。

## 实战演练：json/v2 带来了哪些显著变化？

让我们通过几个具体的例子来感受一下 json/v2 的不同之处。

注：本文使用的Go版本为go 1.24.1以及gotip(go1.25-devel_c0eb7ab3)。


### 行为正确性：重复键报错与大小写敏感

encoding/json (v1) 在处理 JSON 对象中重复的键名时，行为是不确定的（通常是后者覆盖前者）并且不会报错。同时，它在匹配 JSON 字段名和 Go 结构体字段时采用大小写不敏感的策略。这些都可能与最新的 JSON 规范或开发者的直观预期有所出入。让我们看看 json/v2 在这方面的表现。

```
// jsondemo1.go
package main
import (
"encoding/json"
"fmt"
)
type TargetRepeat struct {
Message string `json:"message"`
}
func main() {
fmt.Println("--- Testing Duplicate Keys ---")
inputJSONRepeat := `{"message": "hello 1", "message": "hello 2"}` // 重复键 "message"
var outRepeat TargetRepeat
errRepeat := json.Unmarshal([]byte(inputJSONRepeat), &outRepeat)
if errRepeat != nil {
fmt.Println("Unmarshal with duplicate keys error (expected for v2):", errRepeat)
} else {
fmt.Printf("Unmarshal with duplicate keys output (v1 behavior): %+v\n", outRepeat)
}
fmt.Println("\n--- Testing Case Sensitivity ---")
type TargetCase struct {
MyValue string `json:"myValue"` // Tag is camelCase
}
inputJSONCase := `{"myvalue": "hello case"}` // JSON key is lowercase
var outCase TargetCase
errCase := json.Unmarshal([]byte(inputJSONCase), &outCase)
if errCase != nil {
fmt.Println("Unmarshal with case mismatch error (expected for v2 default):", errCase)
} else {
fmt.Printf("Unmarshal with case mismatch output (v1 behavior or v2 with nocase): %+v\n", outCase)
if outCase.MyValue == "" {
fmt.Println("Note: myValue field was not populated due to case mismatch in v2 (default).")
}
}
}
```


注：当使用gotip运行上述示例代码前，我们需要将导入的encoding/json换为encoding/json/v2，后续示例都是如此，我就不再在每个示例末尾重复说明了。


接下来，我们分别用v1版本和v2版本json包进行编译、运行与对比：

```
$go run jsondemo1.go
--- Testing Duplicate Keys ---
Unmarshal with duplicate keys output (v1 behavior): {Message:hello 2}
--- Testing Case Sensitivity ---
Unmarshal with case mismatch output (v1 behavior or v2 with nocase): {MyValue:hello case}
```


V1不会因重复键而报错，且默认大小写不敏感匹配。

使用gotip运行：

```
$GOEXPERIMENT=jsonv2 gotip run jsondemo.go
--- Testing Duplicate Keys ---
Unmarshal with duplicate keys error (expected for v2): jsontext: duplicate object member name "message"
--- Testing Case Sensitivity ---
Unmarshal with case mismatch output (v1 behavior or v2 with nocase): {MyValue:}
Note: myValue field was not populated due to case mismatch in v2 (default).
```


我们看到：对于重复键，v2 会明确报错。对于大小写敏感性，v2 默认进行精确匹配，因此 myvalue 无法匹配到 myValue 标签的字段（除非使用nocase标签选项或全局配置）。

### 灵活的时间(Time)与时长(Duration)处理

encoding/json (v1) 对 time.Time 的解析强制要求 RFC 3339 格式，对 time.Duration 则序列化为纳秒整数，这在与其他系统交互或追求可读性时常常带来不便。json/v2 通过引入 format 标签选项，极大地增强了对这两种类型的格式化和解析能力。

我们先看v1版本json包对时间和时长的处理：

```
// jsondemo2-v1.go
package main
import (
"encoding/json"
"fmt"
"time"
)
type EventData struct {
EventName string `json:"event_name"`
Timestamp time.Time `json:"timestamp,format:'2006-01-02'"` // v2: 自定义日期格式
PreciseTime time.Time `json:"precise_time,format:RFC3339Nano"` // v2: RFC3339 Nano 格式
Duration time.Duration `json:"duration"` // v2 默认输出 "1h2m3s" 格式
Timeout time.Duration `json:"timeout,format:sec"` // v2: 以秒为单位的数字
OldDuration time.Duration `json:"old_duration,format:nano"` // v2: 兼容v1的纳秒数字
}
func main() {
fmt.Println("--- Testing Time and Duration Marshaling (v2) ---")
event := EventData{
EventName: "System Update",
Timestamp: time.Date(2025, 5, 6, 10, 30, 0, 0, time.UTC),
PreciseTime: time.Now(),
Duration: time.Hour*2 + time.Minute*15,
Timeout: time.Second * 90,
OldDuration: time.Millisecond * 500,
}
jsonData, err := json.MarshalIndent(event, "", " ")
if err != nil {
fmt.Println("Marshal error:", err)
return
}
fmt.Println(string(jsonData))
fmt.Println("\n--- Testing Time Unmarshaling (v2) ---")
inputTimeJSON := `{"event_name":"Test Event", "timestamp":"2024-12-25", "precise_time":"2024-12-25T08:30:05.123456789Z", "duration":"30m", "timeout":120, "old_duration": 700000000}`
var decodedEvent EventData
err = json.Unmarshal([]byte(inputTimeJSON), &decodedEvent)
if err != nil {
fmt.Println("Unmarshal error:", err)
} else {
fmt.Printf("Unmarshaled Event (v2 expected): %+v\n", decodedEvent)
}
}
```


使用Go 1.24.1运行上述代码，得到的结果如下：

```
$go run jsondemo2-v1.go
--- Testing Time and Duration Marshaling (v2) ---
{
"event_name": "System Update",
"timestamp": "2025-05-06T10:30:00Z",
"precise_time": "2025-05-14T04:36:26.428316395Z",
"duration": 8100000000000,
"timeout": 90000000000,
"old_duration": 500000000
}
--- Testing Time Unmarshaling (v2) ---
Unmarshal error: parsing time "2024-12-25" as "2006-01-02T15:04:05Z07:00": cannot parse "" as "T"
```


再来看看v2版的情况，注意v2版在json API上有不同：

```
// jsondemo2-v2.go
package main
import (
"encoding/json/v2"
"encoding/json/jsontext"
"fmt"
"time"
)
type EventData struct {
EventName string `json:"event_name"`
Timestamp time.Time `json:"timestamp,format:'2006-01-02'"` // v2: 自定义日期格式
PreciseTime time.Time `json:"precise_time,format:RFC3339Nano"` // v2: RFC3339 Nano 格式
Duration time.Duration `json:"duration"` // v2 默认输出 "1h2m3s" 格式
Timeout time.Duration `json:"timeout,format:sec"` // v2: 以秒为单位的数字
OldDuration time.Duration `json:"old_duration,format:nano"` // v2: 兼容v1的纳秒数字
}
func main() {
fmt.Println("--- Testing Time and Duration Marshaling (v2) ---")
event := EventData{
EventName: "System Update",
Timestamp: time.Date(2025, 5, 6, 10, 30, 0, 0, time.UTC),
PreciseTime: time.Now(),
Duration: time.Hour*2 + time.Minute*15,
Timeout: time.Second * 90,
OldDuration: time.Millisecond * 500,
}
jsonData, err := json.Marshal(event, json.Deterministic(true))
//jsonData, err := json.MarshalIndent(event, "", " ")
if err != nil {
fmt.Println("Marshal error:", err)
return
}
fmt.Println("Marshaled JSON (v2 expected):\n", string(jsonData))
(*jsontext.Value)(&jsonData).Indent() // indent for readability
fmt.Println(string(jsonData))
fmt.Println("\n--- Testing Time Unmarshaling (v2) ---")
inputTimeJSON := `{"event_name":"Test Event", "timestamp":"2024-12-25", "precise_time":"2024-12-25T08:30:05.123456789Z", "duration":"30m", "timeout":120, "old_duration": 700000000}`
var decodedEvent EventData
err = json.Unmarshal([]byte(inputTimeJSON), &decodedEvent)
if err != nil {
fmt.Println("Unmarshal error:", err)
} else {
fmt.Printf("Unmarshaled Event (v2 expected): %+v\n", decodedEvent)
}
}
```


运行v2版的结果如下：

```
$GOEXPERIMENT=jsonv2 gotip run jsondemo2-v2.go
--- Testing Time and Duration Marshaling (v2) ---
Marshaled JSON (v2 expected):
{"event_name":"System Update","timestamp":"2025-05-06","precise_time":"2025-05-14T04:43:16.476817544Z","duration":"2h15m0s","timeout":90,"old_duration":500000000}
{
"event_name": "System Update",
"timestamp": "2025-05-06",
"precise_time": "2025-05-14T04:43:16.476817544Z",
"duration": "2h15m0s",
"timeout": 90,
"old_duration": 500000000
}
--- Testing Time Unmarshaling (v2) ---
Unmarshaled Event (v2 expected): {EventName:Test Event Timestamp:2024-12-25 00:00:00 +0000 UTC PreciseTime:2024-12-25 08:30:05.123456789 +0000 UTC Duration:30m0s Timeout:2m0s OldDuration:700ms}
```


对比上面的运行结果，我们看到：

-
V1版本(普通 go run):** format标签无效，Timestamp 因非 RFC3339格式(“2006-01-02T15:04:05Z07:00″) 而解析失败；Duration 和 Timeout 会序列化/反序列化为纳秒数字。

-
**V2版本(GOEXPERIMENT=jsonv2 gotip run):**format 标签在 time.Time 和 time.Duration 上都生效了，提供了极大的灵活性。Duration 默认的字符串表示也更易读。

### omitempty 行为调整与 omitzero 引入

omitempty 标签在 v1 和 v2 中的行为定义有所不同。v1 主要基于 Go 类型的零值判断，而 v2 则更侧重于字段编码后的 JSON 值是否为空（如 null, “”, {}, []）。为了更好地处理 Go 零值的省略，v2 引入（并已向后移植到 v1.24+）了 omitzero 标签。

我们先看v1版本中omitempty和omitzero的语义：

```
// jsondemo3-v1.go
package main
import (
"encoding/json"
"fmt"
)
type Config struct {
Enabled bool `json:"enabled,omitempty"` // v1: false 时省略; v2: false 不编码为JSON空则不省略
Count int `json:"count,omitempty"` // v1: 0 时省略; v2: 0 不编码为JSON空则不省略
Name string `json:"name,omitempty"` // v1 & v2: "" 时省略
Description *string `json:"description,omitempty"` // v1 & v2: nil 时省略
IsSet bool `json:"is_set,omitzero"` // v1(1.24+)/v2: false 时省略
Port int `json:"port,omitzero"` // v1(1.24+)/v2: 0 时省略
APIKey *string `json:"api_key,omitzero"` // v1(1.24+)/v2: nil 时省略
}
func main() {
fmt.Println("--- Testing omitempty/omitzero ---")
emptyConf := Config{} // All zero values
descValue := ""
emptyConfWithEmptyStringPtr := Config{Description: &descValue, APIKey: &descValue}
jsonDataV1, _ := json.MarshalIndent(emptyConf, "", " ")
fmt.Println("V1 (go run) - Empty Config:\n", string(jsonDataV1))
jsonDataV1Ptr, _ := json.MarshalIndent(emptyConfWithEmptyStringPtr, "", " ")
fmt.Println("V1 (go run) - Empty Config with Empty String Ptr:\n", string(jsonDataV1Ptr))
}
```


上面代码在Go 1.24.1下运行输出如下：

```
$go run jsondemo3-v1.go
--- Testing omitempty/omitzero ---
V1 (go run) - Empty Config:
{}
V1 (go run) - Empty Config with Empty String Ptr:
{
"description": "",
"api_key": ""
}
```


接下来，我们再看看v2版本的代码和输出结果：

```
// jsondemo3-v2.go
package main
import (
"encoding/json/jsontext"
"encoding/json/v2"
"fmt"
)
type Config struct {
Enabled bool `json:"enabled,omitempty"` // v1: false 时省略; v2: false 不编码为JSON空则不省略
Count int `json:"count,omitempty"` // v1: 0 时省略; v2: 0 不编码为JSON空则不省略
Name string `json:"name,omitempty"` // v1 & v2: "" 时省略
Description *string `json:"description,omitempty"` // v1 & v2: nil 时省略
IsSet bool `json:"is_set,omitzero"` // v1(1.24+)/v2: false 时省略
Port int `json:"port,omitzero"` // v1(1.24+)/v2: 0 时省略
APIKey *string `json:"api_key,omitzero"` // v1(1.24+)/v2: nil 时省略
}
func main() {
fmt.Println("--- Testing omitempty/omitzero ---")
emptyConf := Config{} // All zero values
descValue := ""
emptyConfWithEmptyStringPtr := Config{Description: &descValue, APIKey: &descValue}
jsonDataV2, _ := json.Marshal(emptyConf)
(*jsontext.Value)(&jsonDataV2).Indent() // indent for readability
fmt.Println("V2 (go run) - Empty Config:\n", string(jsonDataV2))
jsonDataV2Ptr, _ := json.Marshal(emptyConfWithEmptyStringPtr)
(*jsontext.Value)(&jsonDataV2Ptr).Indent() // indent for readability
fmt.Println("V2 (go run) - Empty Config with Empty String Ptr:\n", string(jsonDataV2Ptr))
}
```


在gotip下上述代码输出如下：

```
$GOEXPERIMENT=jsonv2 gotip run jsondemo3-v2.go
--- Testing omitempty/omitzero ---
V2 (go run) - Empty Config:
{
"enabled": false,
"count": 0
}
V2 (go run) - Empty Config with Empty String Ptr:
{
"enabled": false,
"count": 0,
"api_key": ""
}
```


对比一下输出，可以看到：

**V1:**Enabled:false 和 Count:0 会被 omitempty 省略。Description为nil时也会被 omitempty 省略。**V2:**omitempty 的行为与 v1 不同。对于 Enabled:false 和 Count:0，omitempty 不会省略它们。而 omitzero 则会按 Go 的零值规则省略 IsSet:false, Port:0。*Description是 “” (JSON空字符串)，所以也会被 omitempty 省略。但api_key因非空，不会被omitzero省略。

我们看到改进后的V2版本使得开发者能更精确地控制字段的省略条件。

### Nil Slice/Map 的默认序列化行为

v1 版本将 nil 的 slice 和 map 序列化为 JSON null。而 json/v2 为了更符合多数场景的预期，默认将它们序列化为空数组 [] 和空对象 {}，同时也提供了 format:emitnull 标签选项以兼容旧行为或特定需求。

我们先来看看v1版本的序列化行为：

```
// jsondemo4-v1.go
package main
import (
"encoding/json"
"fmt"
)
type Data struct {
Tags []string `json:"tags"` // nil slice
Attrs map[string]string `json:"attrs"` // nil map
MaybeTags []string `json:"maybe_tags,format:emitnull"` // v2: 强制为 null
MaybeAttrs map[string]string `json:"maybe_attrs,format:emitnull"` // v2: 强制为 null
}
func main() {
fmt.Println("--- Testing Nil Slice/Map Serialization ---")
d := Data{} // Tags 和 Attrs 都是 nil
jsonData, _ := json.MarshalIndent(d, "", " ")
fmt.Println("Serialized Output (run with go and gotip to compare):\n", string(jsonData))
}
```


运行v1版的结果如下：

```
--- Testing Nil Slice/Map Serialization ---
Serialized Output (run with go and gotip to compare):
{
"tags": null,
"attrs": null,
"maybe_tags": null,
"maybe_attrs": null
}
```


再来看看v2版的示例：

```
package main
import (
"encoding/json/jsontext"
"encoding/json/v2"
"fmt"
)
type Data struct {
Tags []string `json:"tags"` // nil slice
Attrs map[string]string `json:"attrs"` // nil map
MaybeTags []string `json:"maybe_tags,format:emitnull"` // v2: 强制为 null
MaybeAttrs map[string]string `json:"maybe_attrs,format:emitnull"` // v2: 强制为 null
}
func main() {
fmt.Println("--- Testing Nil Slice/Map Serialization ---")
d := Data{} // Tags 和 Attrs 都是 nil
jsonData, _ := json.Marshal(d, json.Deterministic(true))
(*jsontext.Value)(&jsonData).Indent() // indent for readability
fmt.Println("Serialized Output (run with go and gotip to compare):\n", string(jsonData))
}
```


v2版的运行结果如下：

```
$GOEXPERIMENT=jsonv2 gotip run jsondemo4-v2.go
--- Testing Nil Slice/Map Serialization ---
Serialized Output (run with go and gotip to compare):
{
"tags": [],
"attrs": {},
"maybe_tags": null,
"maybe_attrs": null
}
```


通过对比，我们看到V2版本的改进：** 默认将 nil slice/map 序列化为 [] 和 {}，这通常更符合前端或其他语言消费者的预期。同时提供 format:emitnull 兼容旧行为或特定需求。

### 强大的新 Struct Tag Options: inline 和 unknown

json/v2 引入了多个强大的新标签选项，极大地增强了对结构体序列化和反序列化行为的控制能力。我们来看两个例子：inline 和 unknown。

**inline选项**

inline这个选项允许我们将一个内嵌（或普通）结构体字段的 JSON 表示“提升”到其父结构体中，而不是作为一个嵌套对象。

```
// jsondemo5-inline-v1.go
package main
import (
"encoding/json"
"fmt"
)
type Address struct {
Street string `json:"street"`
City string `json:"city"`
}
type Person struct {
Name string `json:"name"`
Address Address `json:"address,inline"` // v2 支持
}
func main() {
fmt.Println("--- Testing 'inline' Tag ---")
p := Person{
Name: "Tony Bai",
Address: Address{Street: "123 Go Ave", City: "Gopher City"},
}
jsonData, _ := json.MarshalIndent(p, "", " ")
fmt.Println("Serialized Person (v2 expected with inline):\n", string(jsonData))
}
```


用Go 1.24.1运行上面示例，输出如下：

```
$go run jsondemo5-inline-v1.go
--- Testing 'inline' Tag ---
Serialized Person (v2 expected with inline):
{
"name": "Tony Bai",
"address": {
"street": "123 Go Ave",
"city": "Gopher City"
}
}
```


再来看一下v2版的示例代码：

```
// jsondemo5-inline-v2.go
package main
import (
"encoding/json/jsontext"
"encoding/json/v2"
"fmt"
)
type Address struct {
Street string `json:"street"`
City string `json:"city"`
}
type Person struct {
Name string `json:"name"`
Address Address `json:",inline"` // v2 支持
}
func main() {
fmt.Println("--- Testing 'inline' Tag ---")
p := Person{
Name: "Tony Bai",
Address: Address{Street: "123 Go Ave", City: "Gopher City"},
}
jsonData, _ := json.Marshal(p, json.Deterministic(true))
(*jsontext.Value)(&jsonData).Indent() // indent for readability
fmt.Println("Serialized Person (v2 expected with inline):\n", string(jsonData))
}
```


使用gotip运行该示例：

```
$GOEXPERIMENT=jsonv2 gotip run jsondemo5-inline-v2.go
--- Testing 'inline' Tag ---
Serialized Person (v2 expected with inline):
{
"name": "Tony Bai",
"street": "123 Go Ave",
"city": "Gopher City"
}
```


对比两个输出结果，我们可以看到：v2版本通过inline标签将Address字段提升到了上一个父层次了，其字段直接作为父层次的字段，而不是作为一个单独的json object。

**unknown选项**

unknown这个选项允许我们将 JSON 对象中未在 Go 结构体中明确定义的字段捕获到一个指定的 map 或 jsontext.Value 类型的字段中，而不是像 v1 那样默认丢弃它们。

老规矩，我们还是先来看v1版本的行为：

```
// jsondemo5-unknown-v1.go
package main
import (
"encoding/json"
"fmt"
)
type Item struct {
ID string `json:"id"`
KnownData string `json:"known_data"`
UnknownFields map[string]json.RawMessage `json:",unknown"` // v2 支持
}
func main() {
fmt.Println("--- Testing 'unknown' Tag ---")
inputJSON := `{"id":"item1","known_data":"some data","new_field":"value for new field","another_unknown":123, "obj_field":{"nested":true}}`
var item Item
err := json.Unmarshal([]byte(inputJSON), &item)
if err != nil {
fmt.Println("Unmarshal error:", err)
return
}
fmt.Printf("Unmarshaled Item: %+v\n", item)
if item.UnknownFields != nil {
fmt.Println("Captured Unknown Fields:")
for k, v := range item.UnknownFields {
fmt.Printf(" %s: %s\n", k, string(v))
}
}
}
```


运行该示例：

```
$go run jsondemo5-unknown-v1.go
--- Testing 'unknown' Tag ---
Unmarshaled Item: {ID:item1 KnownData:some data UnknownFields:map[]}
```


我们看到V1默认会丢弃 new_field, another_unknown, obj_field。

再来看一下v2版本的示例代码：

```
// jsondemo5-unknown-v2.go
package main
import (
"encoding/json/jsontext"
"encoding/json/v2"
"fmt"
)
type Item struct {
ID string `json:"id"`
KnownData string `json:"known_data"`
UnknownFields map[string]jsontext.Value `json:",unknown"`
}
func main() {
fmt.Println("--- Testing 'unknown' Tag ---")
inputJSON := `{"id":"item1","known_data":"some data","new_field":"value for new field","another_unknown":123, "obj_field":{"nested":true}}`
var item Item
err := json.Unmarshal([]byte(inputJSON), &item)
if err != nil {
fmt.Println("Unmarshal error:", err)
return
}
fmt.Printf("Unmarshaled Item: %+v\n", item)
if item.UnknownFields != nil {
fmt.Println("Captured Unknown Fields:")
for k, v := range item.UnknownFields {
fmt.Printf(" %s: %s\n", k, string(v))
}
}
}
```


使用gotip运行上述代码：

```
$GOEXPERIMENT=jsonv2 gotip run jsondemo5-unknown-v2.go
--- Testing 'unknown' Tag ---
Unmarshaled Item: {ID:item1 KnownData:some data UnknownFields:map[another_unknown:123 new_field:"value for new field" obj_field:{"nested":true}]}
Captured Unknown Fields:
another_unknown: 123
obj_field: {"nested":true}
new_field: "value for new field"
```


我们很直观的看到了V2版本的改进：** unknown 标签使得捕获和处理动态或未预期的 JSON 字段成为可能**。

### 性能提升验证

json/v2 的一个重要目标是提升性能，尤其是在处理大型 JSON 对象时。这主要得益于其全新设计的、基于状态机的、更少依赖反射的解析器。

我们可以创建一个简单的基准测试文件 jsondemo_test.go 来验证这一点：

```
// benchmark/jsondemo_test.go
package main
import (
"encoding/json"
//"encoding/json/v2" // 使用gotip运行测试时使用这个v2包
"os"
"testing"
)
// 假设 swagger.json 文件已下载到当前目录，且内容为一个大型 JSON 对象
const swaggerFile = "swagger.json"
func BenchmarkUnmarshalSwagger(b *testing.B) {
data, err := os.ReadFile(swaggerFile)
if err != nil {
b.Fatalf("Failed to read %s: %v", swaggerFile, err)
}
b.ResetTimer() // 重置计时器，忽略文件读取时间
for i := 0; i < b.N; i++ {
var out interface{} // 使用 interface{} 简化，实际场景应为具体类型
err := json.Unmarshal(data, &out)
if err != nil {
b.Fatalf("Unmarshal failed: %v", err)
}
}
}
```


请确保你有一个名为 swagger.json 的较大 JSON 文件在同目录下，这里我们从 Kubernetes 仓库下载一个 OpenAPI 规范文件，大约3.6MB。

运行基准测试：

- V1 (普通 go test):

```
$ go test -bench . -benchmem
goos: linux
goarch: amd64
pkg: demo
cpu: Intel(R) Xeon(R) CPU E5-2695 v2 @ 2.40GHz
BenchmarkUnmarshalSwagger-2 15 69301910 ns/op 11902650 B/op 190568 allocs/op
PASS
ok demo 1.128s
```


- V2 (GOEXPERIMENT=jsonv2 gotip test):

```
$GOEXPERIMENT=jsonv2 gotip test -bench . -benchmem
goos: linux
goarch: amd64
pkg: demo
cpu: Intel(R) Xeon(R) CPU E5-2695 v2 @ 2.40GHz
BenchmarkUnmarshalSwagger-2 31 36510027 ns/op 11143039 B/op 163934 allocs/op
PASS
ok demo 2.112s
```


通过结果对比，我们看到：在处理类似 Kubernetes OpenAPI 规范这样的大型 JSON文件 时，json/v2 的反序列化性能相较于 v1 能有显著提升（例如，从 60多ms 级别降低到 30多ms 级别），同时内存分配次数也可能有所减少。这对于需要频繁处理大型 JSON 负载的应用（如 API 网关、配置中心、监控数据处理等）来说，无疑是一个重大利好。

当然，这里仅仅是针对一个场景做的benchmark。不过，从官方的数据来看，多数场景，jsonv2的性能都有大幅提升。

## 总结与展望

通过今天的动手实践，我们可以清晰地看到，实验性的 json/v2在**行为正确性、功能丰富性、API 易用性和性能**方面都带来了令人鼓舞的改进，旨在系统性地解决 encoding/json (v1) 长期以来存在的诸多痛点。

从更严格的 JSON 规范遵循（如重复键报错、大小写敏感），到更灵活的特性支持（如自定义时间格式、omitzero、inline、unknown 字段），再到底层解析性能的显著提升，json/v2 无疑承载了 Go 社区对于下一代标准库 JSON 包的厚望。

目前，json/v2 仍然处于 Go 开发分支的**实验阶段**，并计划在Go 1.25版本中以实验特性落地，由 GOEXPERIMENT=jsonv2 环境变量控制，**不建议在生产环境中使用**。但通过 gotip，我们可以提前一窥其风采，参与社区讨论，并为未来可能的正式发布做好准备。

**你对 encoding/json 存在哪些痛点？你对 json/v2 的这些改进有什么看法或期待？欢迎在评论区分享你的想法！** 如果你也想亲自动手试试，别忘了点个【赞】和【在看】，并把这篇文章分享给更多 Gopher！

本文中涉及到的源码可以在下载：https://github.com/bigwhite/experiments/tree/master/jsonv2 。

**想更系统地理解 Go 底层机制，写出更高性能、更地道的 Go 代码？**

今天我们深入探讨了 Go 标准库encoding/json的演进。如果你对 Go 语言的内部实现、性能优化、工程实践以及如何写出更符合 Go 设计哲学的代码感兴趣，希望：

**超越基础，系统性地提升你的 Go 语言技能水平；****深入理解 Go 的设计哲学、并发模型、以及在真实大型项目中的应用与避坑经验；****掌握更多 Go 语言的进阶技巧，解决复杂工程问题，在实践中写出更健壮、更优雅、更高性能的代码；**

那么，我诚挚地邀请你关注我在**极客时间开设的专栏——《Go语言进阶课》**。这门课程专为希望从“会用”Go 进阶到“精通”Go 的开发者设计，内容覆盖了 Go 语言的**语法强化、设计先行与工程实践**三大领域，包含大量实战案例、底层原理剖析和一线经验总结，旨在助你打通 Go 语言学习的“奇经八脉”，真正实现技术能力的跃迁。

![](../../assets/ab2d7a5176ba4b48.png)


希望它能成为你 Go 语言精进道路上的得力伙伴！

商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论