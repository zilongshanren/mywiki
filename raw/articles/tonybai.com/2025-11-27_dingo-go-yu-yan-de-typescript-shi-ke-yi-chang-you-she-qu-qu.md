---
title: dingo：Go 语言的 “TypeScript”时刻？—— 一场由社区驱动的语言演进实验
url: https://tonybai.com/2025/11/27/dingo-go-typescript-moment/
published: '2025-11-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# dingo：Go 语言的 “TypeScript”时刻？—— 一场由社区驱动的语言演进实验

![](../../assets/72b83f180a8c765a.png)


[本文永久链接](https://tonybai.com/2025/11/27/dingo-go-typescript-moment) – https://tonybai.com/2025/11/27/dingo-go-typescript-moment

大家好，我是Tony Bai。

Go 语言自诞生以来，以其极简主义哲学（Simplicity）赢得了全球开发者的青睐。然而，这种极简也伴随着长期的痛点：

- 满屏的 if err != nil。
- 缺失的
[和类型（Sum Types/Enums）](https://tonybai.com/2025/10/30/type-theory-intro-for-gopher)，导致状态表达含糊。 - nil 指针带来的运行时 panic 风险。
- 泛型虽已到来，但函数式编程体验（如 map/filter）依然匮乏。

在每年的 Go User Survey 中，这些问题总是名列前茅。

Gopher们渴望“越狱”，但Go 核心团队对此保持审慎，这不仅是为了保持语言的纯粹，也是为了向后兼容。

一个名为[dingo](https://github.com/MadAppGang/dingo) 的开源项目的出现，试图打破这一僵局。它自称是 **“逃逸的 Go”（Go that escaped）**。就像 TypeScript 之于 JavaScript，dingo 试图在不改变 Go 运行时、不引入额外依赖的前提下，通过编译时转译，为 Gopher 们提供**现代化的语法糖**和类型安全。

在本文中，我们就来深入剖析 dingo 的核心机制与创新语法，看看它是如何在保持 Go 零运行时开销的同时，实现那些 Gopher 们梦寐以求的现代语言特性的。

![](../../assets/5b15b2fa46955458.png)


## dingo 是什么？

简单来说，dingo 是一门**元语言（Meta-language）**。它拥有类似 Rust 或 TypeScript 的现代语法，但最终会被编译成**纯粹的、符合惯例的 Go 代码**。

其核心价值主张包括：

**零运行时开销**：编译产物就是标准的 Go 代码，性能与原生 Go 完全一致。**向后兼容**：可以直接引入现有的 Go 包，生成的代码也可以被其他 Go 项目引用。**类型安全增强**：引入 Option 和 Result 类型，语法层面消灭空指针异常。**人体工程学升级**：通过?操作符和模式匹配(Pattern matching)，大幅减少样板代码。

注：为什么叫 dingo（澳洲野犬）？dingo项目的README 中有一个有趣的隐喻：Go 的吉祥物 Gopher（地鼠）是规矩的、被管理的；而 dingo（澳洲野犬）曾是家犬，后来逃入荒野，恢复了野性。dingo 语言依然保留了 Go 的基因，但它拒绝被传统的规则束缚——它代表了

未经许可的自由。

## 核心特性与代码对比

dingo 并非为了标新立异，而是为了解决实际问题。以下是它如何通过转译解决 Go 的四大痛点：

### 错误传播：告别 if err != nil

Go 的错误处理不仅啰嗦，而且容易打断阅读逻辑。dingo 引入了类似 Rust 的 ? 操作符。

**dingo 写法：**

```
// 看起来像 Rust，实际上是 Go 的超集
func processOrder(orderID: string) -> Result<Order, Error> {
let order = fetchOrder(orderID)? // 如果出错，直接返回 Err
let validated = validateOrder(order)? // 自动解包 Ok 的值
let payment = processPayment(validated)?
return Ok(payment)
}
```


**转译后的 Go 代码（自动生成）：**

```
func processOrder(orderID string) (Order, error) {
order, err := fetchOrder(orderID)
if err != nil {
return Order{}, err
}
validated, err := validateOrder(order)
if err != nil {
return Order{}, err
}
// ...以此类推
}
```


我们从上面示例代码的字面上就能看到收益：样板代码减少约 67%，业务逻辑一目了然。

### Sum类型与模式匹配

这是 Go 社区呼声最高的功能之一（[Proposal #19412](在本文中，我们就来深入剖析 Dingo 的核心机制与创新语法，看看它如何在保持 Go 零运行时开销的同时，实现那些 Gopher 们梦寐以求的现代语言特性。)）。dingo 通过 enum 和 match 完美实现了这一点。

**dingo 写法：**

```
enum Shape {
Circle { radius: float64 },
Rectangle { width: float64, height: float64 },
Point,
}
func area(s: Shape) -> float64 {
match s {
Circle(r) => 3.14 * r * r,
Rectangle(w, h) => w * h,
Point => 0.0
}
}
```


dingo 将 enum 转译为 Go 的 struct + tag（标签联合体），并生成辅助方法（如 IsCircle(), NewCircle()）。match 语句在编译时会进行**穷尽性检查**（Exhaustiveness Checking），如果你漏掉了一种情况，编译就会报错。

### 3. 空值安全

受 Swift 和 Kotlin 启发，dingo 引入了安全导航(Safe navigation)操作符 ?. 和空值合并操作符 ??。

**dingo 写法：**

```
// 还在写嵌套的 nil 检查吗？
let city = user?.address?.city?.name ?? "Unknown"
```


**转译后的 Go 代码：**

这会被展开为一系列的 if 检查或立即执行函数表达式，确保不会发生 panic。

### 4. 函数式编程工具

**dingo 写法：**

```
let numbers = []int{1, 2, 3, 4, 5}
let doubled = numbers.filter(|x| x % 2 == 0).map(|x| x * 2)
```


支持 TypeScript 风格的箭头函数 (=>) 或 Rust 风格的管道符 (||)。

## 技术架构与实现原理

dingo 的实现非常务实，它没有重写整个 Go 编译器，而是采用了**两阶段转译架构**：

![](../../assets/d6e5eae98f7e4277.png)


### 编译器架构

**Stage 1: 预处理器 (Preprocessor)**- 处理 dingo 特有的语法糖（如 ? 操作符、enum 定义、类型注解 : Type）。
- 使用基于正则和文本的转换，将 dingo 代码转换为“合法的”但包含特殊标记的 Go 代码。

**Stage 2: AST 转换 (Plugin System)**- 利用 Go 原生的 go/parser 解析代码。
- 通过插件系统（Plugins）对 AST（抽象语法树）进行语义层面的转换。例如，将 Result
展开为具体的 struct 定义。

**Code Generation**: 最后使用 go/printer 输出格式化好的 Go 代码。

### IDE 支持的秘密武器：Source Maps

许多转译语言失败的原因是调试体验差——报错指向生成的代码，而不是源码。

dingo 实现了**精确的 Source Maps (v1 格式)**。

- 它建立 .dingo 文件和生成 .go 文件之间的双向映射。
**LSP 集成**：dingo 开发了一个 LSP 代理（Proxy），它包装了官方的 gopls。当你请求“跳转定义”时，代理拦截请求，利用 Source Map 将位置从 dingo 坐标转换到 Go 坐标，发送给 gopls，拿到结果后再转换回来。这样，你在 VS Code 中写 dingo，享受的是 Go 级别的智能提示和重构能力。

### 混合包管理策略

dingo 采用了一种聪明的混合策略来解决生态兼容性：

**应用开发**：保留 .dingo 文件，忽略生成的 .go 文件。开发体验类似 TypeScript。**库开发**：在发布时，将 .dingo 转译为 .go 并提交到版本控制系统。**意义**：任何纯 Go 项目都可以 go get 一个用 dingo 写的库，而不需要安装 dingo。这是生态融合的关键。

## 哲学与争议：为什么这很重要？

dingo 的 项目说明文档中提出了一个深刻的观点：**“自私地使用 dingo，顺便推动 Go 的演进。”**

TypeScript 最初并非为了改变 JavaScript 标准，而是为了让开发者在大项目中活下来。但随着 TS 的普及（Async/Await, Optional Chaining），这些特性最终被吸纳进 ECMAScript 标准。

dingo的对 Go 核心团队的参考价值，和TS类似。

Go 核心团队在引入新特性时非常依赖“证据”而非“理论”。 Proposal #19412 尚未被accept，是因为缺乏 Go 语境下的具体实现范例。但 dingo 如果能拥有 5 万开发者，它就提供了一份**实证数据**：

- “使用了 ? 操作符的项目，代码量减少了 X%。”
- “和类型在 Go 的 runtime 上运行良好，并没有导致性能下降。”

因此，**dingo 不是 Go 的竞争者，它是 Go 未来的沙盒。**

## 上手指南与现状

目前，截至本文编写时， dingo 还处于 ** v0.3.0-alpha** 阶段，主要核心特性（Sum类型、模式匹配、错误传播、LSP 支持）完成度还不高，仅适合向往拥有Rust、TypeScript等表达力更强的语法的Gopher尝鲜体验之用。

### 快速安装

```
# 克隆仓库并构建编译器
git clone https://github.com/MadAppGang/dingo.git 或 git clone --depth=1 git@github.com:MadAppGang/dingo.git
cd dingo && go build -o dingo ./cmd/dingo
# 将 dingo 加入环境变量 (可选)
export PATH=$PATH:$(pwd)
```


验证安装结果：

```
# dingo version
```


![](../../assets/871b25282df74c46.png)


### Hello World

```
# 编写 hello.dingo
package main
func main() {
let msg = "Hello from dingo"
println(msg)
}
# 编译并运行（dingo 会自动调用 Go 编译器）
dingo run hello.dingo
```


![](../../assets/a702b4ca2d74f16b.png)


运行过程中，dingo会生成转义后的hello.go代码：

```
package main
func main() {
msg := "Hello from dingo"
println(msg)
}
```


大家通过转义后的代码，也可以看到它的转换过程和原理。

## 小结

dingo 是一个大胆的实验。它证明了我们可以在不分叉 Go 语言、不分裂生态系统的前提下，拥有现代化的语言特性。

不过，目前**dingo的完成度还非常低**，很多项目自带的example都build/run failed，这也是本篇文章可以运行的示例较少的原因:(。根据作者的Roadmap，目前很多新增的语法特性还处于未完成阶段。

但对于 Gopher 来说，如果你厌倦了 if err != nil，将来一旦完成度上来的dingo 很值得一试。即使你坚持使用纯 Go，dingo 的存在也是一件好事——它是一只被放入沙丁鱼群的鲶鱼，或许能激活 Go 语言演进的一池春水。

**正如dingo项目宣言所说：这是你的语言，你的规则。无需委员会批准。**

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


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

很有趣的方向，用 rust 的语法去约束 go，比如 tinygo 在嵌入式方向的探索，dingo 看起来更有希望反向影响 go 语言本身。

嗯嗯，社区打个样，让go团队“抄作业”^_^。