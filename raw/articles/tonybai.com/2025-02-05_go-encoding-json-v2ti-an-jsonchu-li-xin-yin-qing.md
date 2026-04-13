---
title: Go encoding/json/v2提案：JSON处理新引擎
url: https://tonybai.com/2025/02/05/go-encoding-json-v2-proposal-json-processing-new-engine/
published: '2025-02-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go encoding/json/v2提案：JSON处理新引擎

![](../../assets/b316b3a9c549fec5.jpeg)


[本文永久链接](https://tonybai.com/2025/02/05/go-encoding-json-v2-proposal-json-processing-new-engine) – https://tonybai.com/2025/02/05/go-encoding-json-v2-proposal-json-processing-new-engine

Go标准库中的encoding/json包，作为Go社区广泛使用的JSON处理工具，[至今已走过十余年](https://tonybai.com/2024/11/12/go-turns-15/)。凭借其将JSON数据与原生Go类型相互转换的能力、通过struct tag自定义字段表示的灵活性，以及Go类型自定义JSON格式的特性，赢得了Go开发者的青睐。

然而，随着时间的推移，encoding/json的局限性也逐渐显现。孤立地解决这些问题可能会导致非正交特性之间产生意外的交互。因此，Go团队在2023年下旬发起了[关于encoding/json/v2的讨论](https://github.com/golang/go/discussions/63397)，旨在全面审视现有encoding/json包，并提出一个面向未来十年的Go JSON处理方案，打造一个 **JSON处理新引擎**。

经过近一年多的讨论、设计调整以及参考实现的优化，Go团队于近期正式提出了[关于encoding/json/v2的提案issue](https://github.com/golang/go/issues/71497)。在该issue中，Go团队梳理并总结了讨论结果以及初始设计与后续调整之间的差异，以供Go社区进一步审阅与反馈。

为了让大家更好地了解该提案issue的核心内容，本文将对提案的背景、主要内容、相对于v1版本的主要改进，以及与v1版本的联系等进行全面介绍，希望通过这篇文章，大家能够及时了解到Go标准库json包的演进与变化。

## 1. 提案背景：现有encoding/json包的局限与改进的需求

在过去十年中，开发者在使用encoding/json的过程中，逐渐意识到了它在功能、API设计、性能和行为上存在的不足。这些问题可以归纳为以下几个方面，也正是encoding/json/v2提案希望解决的核心痛点：

### 1.1 功能缺失 (Missing functionality)

尽管encoding/json功能完善，但仍存在一些重要的功能缺失，社区也为此提出了诸多Feature Request，其中最突出的包括：

**time.Time的自定义格式化 (#21990)**: 缺乏灵活的方式来指定time.Time类型在JSON中的格式，例如自定义日期时间字符串格式。**Marshal时忽略特定Go值 (#11939, #22480, #50480, #29310, #52803, #45669)**: 现有的omitempty标签在某些场景下无法满足需求，开发者希望更精细地控制哪些Go值在Marshal时被忽略，例如忽略零值、空值或特定条件下的值。[Go 1.24版本](https://tonybai.com/2024/12/17/go-1-24-foresight-part2)增加了[omitzero tag](https://tonybai.com/2024/09/12/solve-the-empty-value-dilemma-in-json-encoding-with-omitzero)，将在一定层度缓解这个问题。**将nil切片和mapMarshal为空JSON数组和对象 (#37711, #27589)**: encoding/json默认将nil切片和mapMarshal为JSONnull，但在某些场景下，开发者更期望将其Marshal为空的JSON数组[]和对象{}。**无Go嵌入的Inline类型 (#6213)**: 希望能够更灵活地将Go类型内联到JSON对象中，而无需依赖Go的struct嵌入机制。

虽然这些功能缺失大部分可以通过向现有encoding/json包添加新功能来解决，但可能会导致API变得臃肿和复杂。

### 1.2 API 设计缺陷 (API deficiencies)

encoding/json的API设计存在一些尖锐或限制性的问题，影响了开发者的使用体验：

**难以正确地从io.Reader进行Unmarshal**: 常用的json.NewDecoder(r).Decode(v)方法并不能正确处理JSON payload末尾的垃圾数据 (#36225)，容易导致数据解析错误。**Marshal和Unmarshal函数无法使用Options**: 虽然Encoder和Decoder类型支持Options配置，但Marshal和Unmarshal函数却无法使用，同样，实现Marshaler和Unmarshaler接口的类型也无法利用Options，缺乏选项配置的传递机制(#41144)。**Compact, Indent, HTMLEscape函数输出目标受限**: 这些格式化函数只能将结果写入bytes.Buffer，而不是更灵活的[]byte或io.Writer，限制了函数的使用场景。

这些API缺陷可以通过向现有encoding/json包引入新的API来修复，但这可能会导致同一个任务在同一个包中存在多种不同的实现方式，增加学习成本和使用困惑。

### 1.3 性能限制 (Performance limitations)

encoding/json的性能表现一直备受关注，存在诸多限制性能提升的因素：

**MarshalJSON接口**: 强制实现者分配[]byte返回值，且encoding/json需要再次解析返回值以验证JSON的有效性并重新格式化，造成不必要的性能开销。**UnmarshalJSON接口**: 要求提供完整的JSON value，导致encoding/json需要预先完整解析JSON值以确定边界，之后UnmarshalJSON方法本身还需要再次解析，如果UnmarshalJSON递归调用Unmarshal，则会导致O(N²)的性能退化，例如Kubernetes kube-openapi项目在Unmarshalspec.Swagger时遇到的性能瓶颈 (kubernetes/kube-openapi#315)。**Encoder.WriteToken**: 缺乏流式Encoder API，虽然提案已被接受(#40127)，但尚未实现，且可能同样存在性能问题。**Decoder.Token**: Token类型是一个接口，可以容纳多种类型 (Delim, bool, float64, Number, string, nil)，当boxing数字或字符串到Token接口类型时，会频繁发生内存分配 (#40128)。**缺乏真正的流式处理**: 即使Encoder.Encode和Decoder.Decode方法操作io.Writer和io.Reader，它们仍然会将整个JSON value缓冲到内存中，需要二次扫描JSON，与流式处理的初衷背道而驰 (#33714, #7872, #11046)。

encoding/json应该默认以真正的流式方式操作io.Writer和io.Reader。缓冲整个JSON value违背了使用io.Reader和io.Writer的意义。希望避免在发生错误时输出JSON 的用例应该调用Marshal，并在错误为nil时才写入输出。不幸的是，encoding/json无法默认切换到流式处理，因为这将是一个破坏性的行为变更，暗示着需要一个v2版本的json包来实现这个目标。

### 1.4 行为缺陷 (Behavioral flaws)

encoding/json在行为上存在诸多缺陷，随着JSON规范的日益严格 (RFC 4627, RFC 7159, RFC 7493, RFC 8259)，这些缺陷显得愈发突出：

**JSON 语法处理不严谨**: encoding/json允许无效UTF-8字符，而最新的互联网标准 (RFC 8259) 要求使用有效的UTF-8编码。默认行为至少应符合RFC 8259，将无效UTF-8视为错误。**允许重复的对象成员名称**: RFC8259规定，重复的对象成员名称会导致未指定的行为。从安全角度考虑，默认行为应更严格，拒绝重复名称，正如 RFC 7493 所建议的那样。**Unmarshal时大小写不敏感**: Unmarshal时，JSON对象名称与Go struct字段名称使用大小写不敏感匹配 (#14750)，这既令人意外，也可能存在安全漏洞和性能瓶颈。**类型定义方法调用不一致**: 由于encoding/json及其对Go反射的使用，MarshalJSON和UnmarshalJSON方法在底层值不可寻址时无法调用 (#22967, #27722, #33993, #55890)。**Merge语义不一致**: Unmarshal到非空的Go值时，是否清除目标、重置并重用目标内存、或合并到目标的行为不一致 (#27172, #31924, #26946)。**Error 类型不一致**: encoding/json返回的Error类型不一致，难以可靠地检测Syntactic error, Semantic error, I/O error等不同类型的错误。

这些行为缺陷在不破坏向后兼容性的前提下难以修复。虽然可以添加选项来指定不同的行为，但这并非理想方案，因为期望的行为不应作为非默认选项存在。改变默认行为同样意味着需要一个v2版本的json包。

为了解决上述encoding/json包的种种问题，并为Go语言构建更强大、更现代化的JSON处理能力，Go团队正式提出了encoding/json/v2提案。正如**“JSON处理新引擎”**这个本文标题所寓意的，encoding/json/v2并非简单的修补和改进，而是一次对Go语言JSON处理的**彻底革新**。下面我们就来介绍一下这个新json引擎的主要功能和特点。

## 2. encoding/json/v2：Go JSON处理的新引擎

encoding/json/v2提案并非简单地对现有encoding/json进行升级，而是引入了两个全新的包：

- encoding/json/jsontext: 这是一个
**纯语法层面**的JSON处理包，专注于JSON语法的解析和生成，**不依赖Go反射**。它提供了对JSON令牌(Token)和原始值(Value)的操作，允许开发者在语法层面精细地控制JSON的编解码过程。 - encoding/json/v2: 这是一个
**语义层面**的JSON处理包，**基于jsontext包实现**，并**依赖Go反射**。它继承了encoding/json的核心功能，负责将Go值与JSON数据进行语义上的转换（Marshal 和 Unmarshal），并提供了更丰富的功能和更优的性能。

提案中还给出了两者的关系图，通过该图大家可以更直观地看出两个包之间的关系：

![](../../assets/bafb24c006e03ff4.png)


此外，提案还考虑了与现有encoding/json的兼容性，并提供了选项来实现互操作。encoding/json包本身也将被重构，**底层实现将基于encoding/json/v2来重新实现**。

下面是对jsontext包和json/v2包的核心API的介绍。

### 2.1 encoding/json/jsontext包的关键API

jsontext包提供了Encoder和Decoder类型，用于JSON的编码和解码，以及Token和Value类型来表示JSON的语法元素。

```
package jsontext // "encoding/json/jsontext"
type Encoder struct { /* no exported fields */ }
func NewEncoder(io.Writer, ...Options) *Encoder
func (*Encoder) WriteToken(Token) error
func (*Encoder) WriteValue(Value) error
type Decoder struct { /* no exported fields */ }
func NewDecoder(io.Reader, ...Options) *Decoder
func (*Decoder) PeekKind() Kind
func (*Decoder) ReadToken() (Token, error)
func (*Decoder) ReadValue() (Value, error)
func (*Decoder) SkipValue() error
type Kind byte // JSON 令牌类型
type Token struct { /* no exported fields */ } // JSON 令牌
type Value []byte // JSON 原始值
```


其中：

**Encoder和Decoder**: 提供流式的JSON编码和解码能力，操作io.Writer和io.Reader。**Token**: 表示JSON的基本语法单元，例如null, true, false, 字符串, 数字, 对象开始{, 对象结束}, 数组开始[, 数组结束]等。**Value**: 表示JSON的原始值，可以是完整的JSON对象或数组，类似于encoding/json中的RawMessage。**Kind**: 枚举类型，表示Token和Value的类型，例如’n'(null),’t'(true),’”‘(string),’{‘(object start) 等。

jsontext包还提供了格式化JSON的函数，例如AppendFormat, AppendQuote, AppendUnquote等，以及用于配置行为的Options类型。

### 2.2 encoding/json/v2包的关键API

encoding/json/v2包提供了Marshal, Unmarshal等核心函数，以及MarshalWrite, MarshalEncode, UnmarshalRead, UnmarshalDecode等变体，用于不同场景下的JSON编解码。

```
package json // "encoding/json/v2"
func Marshal(in any, opts ...Options) (out []byte, err error)
func MarshalWrite(out io.Writer, in any, opts ...Options) error
func MarshalEncode(out *jsontext.Encoder, in any, opts ...Options) error
func Unmarshal(in []byte, out any, opts ...Options) error
func UnmarshalRead(in io.Reader, out any, opts ...Options) error
func UnmarshalDecode(in *jsontext.Decoder, out any, opts ...Options) error
```


其中：

**Marshal和Unmarshal**: 核心的Marshal和Unmarshal函数，与encoding/json中的函数签名类似，但行为有所改进。**MarshalWrite, UnmarshalRead**: 直接操作io.Writer和io.Reader，避免中间[]byte的分配。**MarshalEncode, UnmarshalDecode**: 操作jsontext.Encoder和jsontext.Decoder，提供更底层的流式编解码能力。**Options**: 用于配置Marshal和Unmarshal的行为，例如大小写敏感性、omitempty语义、错误处理等。

encoding/json/v2包还引入了更丰富的**struct tag选项**，例如omitzero, omitempty, string, nocase, strictcase, inline,unknown,format等，提供更灵活的字段映射和格式化控制。

### 2.3 设计原则

下面是该proposal的一些设计原则梳理：

**分离语法与语义**: 明确区分JSON的语法处理(jsontext)和语义处理(json/v2)，使得开发者可以根据需求选择合适的API。**流式处理**: 提供流式的Encoder和Decoder，支持高效处理大规模JSON数据，避免一次性加载整个JSON文档到内存。**选项化配置**: 通过Options类型提供丰富的配置选项，允许开发者根据具体需求定制JSON编解码的行为，例如大小写敏感性、格式化风格、错误处理方式等。**改进错误处理**: 引入SyntacticError和SemanticError类型，提供更详细的错误信息，包括错误发生的位置 (JSON Pointer) 和具体的错误原因，方便问题定位和调试。**兼容性与迁移**: encoding/json/v2尽可能兼容现有的encoding/json的行为，并提供选项 (`DefaultOptionsV1`

) 来模拟v1的行为，方便用户平滑迁移。

接下来，我们再来看看json/v2相对于之前版本的提升与改进！

## 3. 相对于encoding/json的提升与改进

encoding/json/v2相对于现有的encoding/json包，在多个方面进行了显著的提升和改进：

### 3.1 性能提升

jsontext包采用更高效的语法解析算法，json/v2在语义处理方面也进行了优化，整体性能相比encoding/json有显著提升，尤其在反序列化和流式处理方面。Benchmark 测试显示，encoding/json/v2的反序列化速度比encoding/json快2.7x到10.2x：

以具体类型为例，下面是github.com/go-json-experiment/jsonbench给出的benchmark结果：

![](../../assets/dbec5140270292bf.png)


![](../../assets/f9ab28df241323e9.png)


### 3.2 更正的行为

encoding/json/v2修正了encoding/json中一些行为不一致性和历史遗留问题，例如：

**大小写敏感的字段匹配**: 默认采用严格的大小写敏感匹配，更符合JSON规范，并通过MatchCaseInsensitiveNames和nocasetag选项提供大小写不敏感匹配的灵活性。**重新定义omitempty语义**: omitempty基于JSON类型系统重新定义，更加清晰和一致，并通过OmitEmptyWithLegacyDefinition选项提供兼容v1 行为的选择。**nil切片和map的处理**: 默认将nil切片和mapMarshal为空JSON数组和对象，而非null，并通过FormatNilSliceAsNull和FormatNilMapAsNull选项提供Marshal为null的选择。**字节数组的表示**: 默认将[]\byteMarshal为Base64编码的JSON字符串，而非JSON数字数组，并通过FormatBytesWithLegacySemantics和format:arraytag 选项提供兼容v1行为的选择。**方法调用的可寻址性**: MarshalJSON方法无论Go值是否可寻址都可调用，更符合预期。**Map Key 的方法调用**: MarshalJSON和UnmarshalJSON方法可以用于 Map Key，提供更强大的自定义能力。**确定性输出**: 通过Deterministic选项，可以保证相同输入Marshal出相同的JSON字节序列。**最小化转义**: 默认使用最小化的JSON字符串转义，仅在必要时进行转义，例如只在HTML或JavaScript环境下才进行特殊字符的转义。**UTF-8 验证**: 默认严格验证UTF-8编码，拒绝包含无效UTF-8的JSON输入，并通过AllowInvalidUTF8选项允许处理无效UTF-8。**重复Key错误**: 默认拒绝JSON对象中存在重复的Key，更符合JSON 规范，并通过AllowDuplicateNames选项允许处理重复Key。**Null值的Unmarshal**: Unmarshal JSONnull时，始终一致地将Go值置零。**Unmarshal合并行为**: Unmarshal JSON对象时，默认合并到已有的Go值，而非完全替换，提供更灵活的更新语义。**time.Duration的表示**: 默认将time.DurationMarshal为JSON 字符串，而非纳秒数字，并通过FormatTimeWithLegacySemantics和format:nanotag选项提供兼容v1行为的选择。**运行时错误报告**: 对Go结构体类型中的结构性错误（例如错误的tag选项）进行运行时错误报告，提前发现问题。

### 3.3 更灵活的 API

jsontext包提供了更底层的API，允许开发者直接操作JSON token和原始值，实现更精细的JSON处理逻辑。json/v2提供了更多的选项和 struct tag 选项，支持更丰富的自定义需求。

### 3.4 更清晰的错误信息

SyntacticError和SemanticError类型提供了更详细的错误信息，包括错误位置 (JSON Pointer) 和错误原因，方便问题排查。

## 4. encoding/json与encoding/json/v2的联系

encoding/json/v2提案的一个重要目标是实现与现有encoding/json的平滑过渡。为此，提案采取了以下策略：

**encoding/json基于encoding/json/v2实现**: 未来的encoding/json包将完全基于encoding/json/v2包进行重构，这意味着encoding/json/v2将成为Go语言官方JSON处理的核心引擎。**DefaultOptionsV1选项**: encoding/json包将提供DefaultOptionsV1选项，该选项预设了一系列兼容v1行为的配置，使得encoding/json的默认行为尽可能与旧版本保持一致。**互操作选项**: encoding/json/v2和encoding/json都提供了大量的选项，允许开发者在v1和v2行为之间进行灵活切换，逐步迁移到v2的新特性。

## 5. 示例代码

以下示例展示了encoding/json/v2的基本用法(示例改自https://github.com/go-json-experiment/json/blob/master/example_test.go)：

```
package main
import (
"fmt"
"log"
"github.com/go-json-experiment/json"
"github.com/go-json-experiment/json/jsontext"
)
func main() {
var value struct {
// This field is explicitly ignored with the special "-" name.
Ignored any `json:"-"`
// No JSON name is not provided, so the Go field name is used.
GoName any
// A JSON name is provided without any special characters.
JSONName any `json:"jsonName"`
// No JSON name is not provided, so the Go field name is used.
Option any `json:",nocase"`
// An empty JSON name specified using an single-quoted string literal.
Empty any `json:"''"`
// A dash JSON name specified using an single-quoted string literal.
Dash any `json:"'-'"`
// A comma JSON name specified using an single-quoted string literal.
Comma any `json:"','"`
// JSON name with quotes specified using a single-quoted string literal.
Quote any `json:"'\"\\''"`
// An unexported field is always ignored.
unexported any
}
b, err := json.Marshal(value)
if err != nil {
log.Fatal(err)
}
(*jsontext.Value)(&b).Indent() // indent for readability
fmt.Println(string(b))
}
```


这段示例代码旨在演示github.com/go-json-experiment/json (即提案中encoding/json/v2的参考实现) 在处理Go结构体字段的json tag时，对于不同命名约定和特殊字符的处理方式。结构体value定义了多个字段，每个字段都使用了不同的json tag，用于演示不同的命名和选项，具体选项含义可以参考proposal中的说明。

```
(*jsontext.Value)(&b).Indent() // indent for readability
```


前面说过，jsontext是操作json语法的包，json缩进的工作就交给了该包的Value的Indent方法。在encoding/json中，我们通常直接用MarshalIndent来进行格式化json的工作。

运行上述示例将输出如下结果：

```
$go run main.go
{
"GoName": null,
"jsonName": null,
"Option": null,
"": null,
"-": null,
",": null,
"\"'": null
}
```


更多示例，可以参见 https://github.com/go-json-experiment/json/blob/master/example_test.go源文件。

## 6. 小结

encoding/json/v2提案代表了Go语言在JSON处理方面的一次重大升级。通过引入jsontext和json/v2两个包，并提供更强大的API、更丰富的选项和更优的性能，encoding/json/v2将为Go开发者带来更高效、更灵活、更可靠的JSON处理体验。同时，该提案也充分考虑了与现有encoding/json的兼容性，为用户平滑迁移提供了保障。encoding/json/v2的引入，无疑将进一步提升Go语言在Web开发、数据处理等领域的竞争力，为Go开发者构建下一代应用提供更强大的**JSON处理新引擎**。

## 7. 参考资料

[proposal: encoding/json/v2: new API for encoding/json](https://github.com/golang/go/issues/71497)– https://github.com/golang/go/issues/71497[discussions: encoding/json/v2](https://github.com/golang/go/discussions/63397)– https://github.com/golang/go/discussions/63397[GopherCon 2023: The Future of JSON in Go – Joe Tsai](https://www.youtube.com/watch?v=avilmOcHKHE)– https://www.youtube.com/watch?v=avilmOcHKHE[json/v2参考实现](https://github.com/go-json-experiment/json)– https://github.com/go-json-experiment/json[json/v2 benchmark](https://github.com/go-json-experiment/jsonbench)– https://github.com/go-json-experiment/jsonbench

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