---
title: Go 1.26 发布在即，为何 json/v2 依然“难产”？七大技术路障全解析
url: https://tonybai.com/2026/02/11/go-1-26-json-v2-delay-7-technical-roadblocks/
published: '2026-02-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.26 发布在即，为何 json/v2 依然“难产”？七大技术路障全解析

![](../../assets/6d664bc10bc44fd3.png)


[本文永久链接](https://tonybai.com/2026/02/11/go-1-26-json-v2-delay-7-technical-roadblocks) – https://tonybai.com/2026/02/11/go-1-26-json-v2-delay-7-technical-roadblocks

大家好，我是Tony Bai。

Go 1.26 预计将于本月（2026 年 2 月）正式发布。然而，在即将到来的 release notes 的欢呼声中，有一个备受瞩目的名字依然带着“实验性”的标签躲在 GOEXPERIMENT 背后——那就是 **encoding/json/v2**。

作为 Go 生态中最核心的基础设施之一，JSON 库的每一次呼吸都牵动着数百万开发者的神经。从 v1 到 v2，不仅仅是性能的提升，更是一场关于**API 设计哲学、向后兼容性与极致性能**的艰难博弈。

很多人以为 v2 的延迟是因为“官方动作慢”或“设计理念之争”。但当我们深入 [json/v2 工作组的看板](https://github.com/orgs/golang/projects/50)，剥开表层的讨论，会发现横亘在稳定版之前的，是**七个具体而微、却又关乎全局的技术“钉子”**。这些问题并非宏大的路线图分歧，而是关乎浮点数精度、错误处理语义、API 封装性等实打实的工程细节。

![](../../assets/d8f214af00cf899a.png)


本文将基于最新的 GitHub Issues 讨论（截至 2026 年 2 月），带你通过显微镜审视这七大阻塞问题，一窥 Go 标准库演进背后的严谨与妥协。

![](../../assets/eea4f3d68dbb3fdb.png)


## 七大阻塞问题（Blockers）一览

![](../../assets/342cf7eadfc5074b.png)


## 深度解析：魔鬼藏在细节中

![](../../assets/8bbab60abf732f74.png)


### 1. API 设计的“丑陋妥协”：jsontext.Internal (#73435)

在当前的 encoding/json/jsontext 包中，竟然存在一个导出的 Internal 类型。这在 Go 标准库的审美中，简直是“房间里的大象”。

jsontext 是 v2 引入的底层包，专注于 JSON 的语法解析（Tokenizing），而上层的 json 包负责语义绑定（Binding）。为了让上层包能够访问底层的缓冲区或状态机，当前的实现不得不导出一个 Internal 符号。

这违背了 Go 标准库的黄金法则之一：**公共 API 必须是为用户设计的，而不是为实现者自己设计的。**

Joe Tsai (dsnet) 提出了一种解决方案：将 jsontext 的核心逻辑移入 encoding/json/internal/jsontext，然后通过类型别名（Type Alias）在公共包中暴露 API。然而，这带来了一个新的难题：godoc 对类型别名的支持并不友好，生成的文档可能会让用户感到困惑，因为方法都挂载在内部类型上。

这个问题已经上升为工具链生态问题。如果这个问题不解决，v2 发布后将面临两个风险：要么用户依赖了这个“临时” API 导致未来无法修改，要么标准库留下了一个永久的“伤疤”。

### 2. 致命的递归：当 Unmarshaler 遇到指针 (#75361)

这是一个真实且诡异的 Bug。一位开发者在迁移旧代码时发现，以下模式在 v1 中正常工作，但在开启 GOEXPERIMENT=jsonv2 后会导致栈溢出（Stack Overflow）：

```
type MyType string
// 自定义 Unmarshal 方法
func (m *MyType) UnmarshalJSON(b []byte) error {
// 试图通过定义一个新类型来“剥离”当前类型的方法，以回退到默认行为
type MyTypeNoMethods *MyType
var derived MyTypeNoMethods = MyTypeNoMethods(m)
// v2 在这里会错误地再次识别出 derived 拥有 UnmarshalJSON 方法
// 从而导致无限递归调用自己
return json.Unmarshal(b, derived)
}
```


在 v1 中，开发者习惯通过类型转换来“剥离”自定义方法。但在 v2 中，为了修复 v1 中某些指针方法无法被调用的 Bug（如 #22967），引入了更激进的**方法集查找逻辑**。

v2 的逻辑是：只要这个值的地址（Addressable）能找到 UnmarshalJSON 方法，就调用它。在上面的例子中，derived 虽然是新类型，但它底层的指针指向的还是 *MyType，v2 过于“聪明”地认为应该调用 (*MyType).UnmarshalJSON，结果造成了死循环。

这是一个典型的“修复了一个 Bug，却引入了另一个 Bug”的案例。Go 团队目前倾向于**保留 v2 的正确逻辑**（即更一致的方法调用），但也必须为这种遗留代码提供一种**检测机制**。目前的计划是引入运行时检测或 go vet 检查，明确告知用户：请使用 type MyTypeNoMethods MyType（非指针别名）来剥离方法，而不是使用指针别名。

### 3. 浮点数的“薛定谔精度”：float32 (#76430)

下面是展示该问题的一段示例代码：

```
var f float32 = 3.1415927 // math.Pi 的 float32 近似值
json.Marshal(f)
```


输出应该是 3.1415927（保持 float32 精度），还是 3.1415927410125732（提升到 float64 精度以确保无损）？

Go v1 的 json 包为了兼容性，倾向于将所有浮点数视为 float64 处理。这导致 float32 在序列化时经常会出现“精度噪音”——那些用户并不想要的、只有在 float64 精度下才有意义的尾数。

然而，v2 的 jsontext 包默认使用 64 位精度。这导致了 json.Marshal（上层）和 jsontext.Encoder（底层）在行为上的不一致。

- 用户期望：float32 就该像 float32，短小精悍。
- 技术现实：JSON 标准（RFC 8259）并没有区分浮点精度。
- 性能视角：处理 32 位浮点数理论上更快，但需要专门的算法路径。

Go 团队正在考虑引入 Float32 构造器和访问器到 jsontext 包中，并修改底层的 AppendFloat 逻辑，以支持显式的 32 位浮点数格式化。这不仅是为了“好看”，更是为了**数值正确性**——避免“双重舍入”（Double Rounding）带来的微小误差。

### 4. 选项系统的“任督二脉”：透传难题 (#76440)

你调用 json.Marshal(v, json.WithIndent(” “)) 很爽，但如果你想控制底层的 jsontext 行为（比如“允许非法 UTF-8”或“允许重复键名”），你发现：**顶层函数把路堵死了**。目前的 MarshalEncode 只接受 json.Option，不接受 jsontext.Option。

v2 将 json（语义层）和 jsontext（语法层）拆分是架构的一大进步。但这也带来了**配置穿透**的问题。

如果为了保持 API 纯洁，强迫用户必须先创建一个 jsontext.Encoder 并在那里配置选项，再传给 json.MarshalEncode，那么 99% 的简单用例都会变得无比繁琐。

Go团队给出的提案是打破层级隔离，允许 json.Marshal 等顶层函数直接接受 jsontext.Option。这是一个实用主义战胜洁癖的胜利。

### 5. 功能做减法：unknown 标签的存废 (#77271)

v2 曾引入了一个 unknown 结构体标签，用于指示某个字段专门用来捕获所有未知的 JSON 字段。同时，还有一个 DiscardUnknownMembers 选项用于丢弃未知字段。

dsnet（Joe Tsai）发起提案，建议删除两个功能。理由如下：

- 功能重叠：v2 已经引入了 inline 标签，它与 unknown 的行为非常相似，仅仅是语义上的微小差别（是否包含“已知”字段）。这种微小的差别会让用户感到困惑。
- API 极简主义：如果用户真的需要处理未知字段，可以通过自定义 Unmarshaler 来实现，或者利用 inline 标签配合后期处理。
- 向后兼容的智慧：添加功能永远比删除功能容易。现在删除，未来如果真有需求还可以加回来；但如果现在保留，未来想删就难了。

### 6. 控制流的缺失：SkipFunc (#74324)

json.SkipFunc 是 v2 引入的一个 Sentinel Error，用于告诉编码器“跳过当前字段/值”。目前它只能在 MarshalToFunc（用户自定义函数）中使用。但如果我在类型的方法 MarshalJSONTo 中想跳过自己怎么办？目前是不支持的。

这是一个典型的**“二等公民”问题**。用户自定义的函数拥有比类型方法更高的权限。这导致在迁移旧代码时，如果要实现“条件性跳过”，必须写出非常丑陋的 hack 代码（比如定义一个空结构体来占位）。

允许 MarshalJSONTo 返回 SkipFunc 看似简单，但它要求调用者必须处理这个错误。这意味着**不能直接调用 v.MarshalJSONTo**，而必须通过 json.Marshal 来调用，否则你会收到一个未处理的错误。这需要文档和工具链的配合。

### 7. 文档真空：新接口的最佳实践 (#76712)

v2 引入了 MarshalerTo 和 UnmarshalerFrom 两个高性能接口，它们直接操作 jsontext.Encoder/Decoder，避免了内存分配。但是，**到底该什么时候用它们？**

目前缺乏明确的文档指导。如果用户在任何时候都直接调用 v.MarshalJSONTo(enc)，可能会绕过 json.Marshal 中处理的许多全局选项（如大小写敏感、省略零值等）。

Go 团队计划在文档中明确：**这属于“高级 API”，普通用户应始终使用 json.Marshal，除非你在编写极其底层的库。**

## 路线图：我们何时能用上“真v2”？

根据[最新的工作组纪要](https://github.com/golang/go/issues/76406)和 Issue 状态，我们可以画出一条清晰的时间线：

- 当前 (Go 1.26, 2026.02)：GOEXPERIMENT=jsonv2 继续存在。v2 代码库已进入主仓库，但 API 仍未冻结。此时适合库作者进行集成测试，但不建议在生产环境核心业务中大规模铺开。
- 决战期 (2026 H1)：必须彻底解决上述 7 个 Blocker。特别是 API 签名相关的修改（如 float32 支持和 SkipFunc），一旦定型就是 10 年承诺。
- 目标 (Go 1.27, 2026.08)：如果一切顺利，我们有望在今年 8 月发布的 Go 1.27 中，看到移除实验标签、正式可用的 encoding/json/v2。这意味着 Go 语言将迎来其历史上最大规模的标准库升级之一。

## 小结：给 Gopher 的建议

- 别急着重构：现有的 encoding/json (v1) 依然稳健。除非你有极端的性能需求（v2 性能提升显著）或需要 v2 独有的某些特性，否则请按兵不动。
- 关注 jsontext：即使不用 v2 的序列化，新独立的 jsontext 包也是一个处理 JSON Token 流的神器，非常适合写高性能的底层解析工具。它的 API 设计比 v1 的 Scanner 更加现代化和高效。
- 参与反馈：现在是影响 Go 未来 10 年 JSON 处理方式的最后窗口期。如果你对上述 Issue 有独到见解，去 GitHub 上发声吧！

Go 团队的“慢”，是对生态的“敬”。这七个拦路虎，每一个都是为了让未来的十年里，我们能写出更少 Bug、更快速度的 Go 代码。好事多磨，让我们静候佳音。

## 参考资料

- json/v2 工作组的看板 – https://github.com/orgs/golang/projects/50
- encoding/json/v2: working group meeting minutes – https://github.com/golang/go/issues/76406

**你更在意什么？**

Go 团队为了 API 的洁癖和严谨，宁愿让 json/v2 多飞一会儿。在你的开发实践中，你更倾向于“尽快用上新特性”，还是“哪怕慢一点也要保证接口设计的绝对完美”？你对 float32 的精度噪音有切肤之痛吗？

欢迎在评论区分享你的看法，我们一起坐等 Go 1.26 官宣！

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


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


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论