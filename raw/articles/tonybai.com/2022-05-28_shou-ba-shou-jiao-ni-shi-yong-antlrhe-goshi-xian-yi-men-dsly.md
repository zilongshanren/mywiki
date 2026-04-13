---
title: 手把手教你使用ANTLR和Go实现一门DSL语言（第四部分）：组装语义模型并测试DSL
url: https://tonybai.com/2022/05/28/an-example-of-implement-dsl-using-antlr-and-go-part4/
published: '2022-05-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 手把手教你使用ANTLR和Go实现一门DSL语言（第四部分）：组装语义模型并测试DSL

![](../../assets/dcf34f2d49196832.png)


[本文永久链接](https://tonybai.com/2022/05/28/an-example-of-implement-dsl-using-antlr-and-go-part4) – https://tonybai.com/2022/05/28/an-example-of-implement-dsl-using-antlr-and-go-part4

在[上一篇文章](https://tonybai.com/2022/05/27/an-example-of-implement-dsl-using-antlr-and-go-part3)中，我们为DSL建立了完整的语义模型，我们距离DSL的语法示例真正run起来还差最后一步，那就是基于语法树提取信息(逆波兰式)、组装语义模型，在加载语义模型并实例化各个规则处理器(processor)后，我们就可以处理数据了！下面是我们部署在海洋浮标上的指标采集程序的全景图：

![](../../assets/88638c95b6207008.png)


在这一篇中，我们就来按照上图，通过语法树提取逆波兰式并组装语义模型，让我们的语法示例能真正按预期run起来！

### 一. 从语法树提取逆波兰式并组装语义模型

通过上面语义模型的讲解，我们知道了语法树与语义模型之间的联系包括逆波兰式、windowsRange、result和enumableFunc。其主要联系是那个逆波兰式，而像windowsRange、result和enumableFunc这些信息都相对容易提取。

![](../../assets/19ac5199d9124248.png)


接下来，我们先来看看如何从DSL的语法树构提取到逆波兰式，完成逆波兰式的提取，我们的语义模型组装工作就算完成大半了。好，下面我们就将目光聚焦在DSL语法树上。

为了聚焦原理的讲解，我们在本篇**仅实现支持语法示例文件中包含单rule的语法树的逆波兰式等信息的提取**。而语法示例文件中有多个rule的情况就当做思考题留给大家了。

在[本系列第二部分验证文法](https://tonybai.com/2022/05/25/an-example-of-implement-dsl-using-antlr-and-go-part2)中，我们知道了ANTLR Listener对DSL语法树的遍历默认都是前序遍历。在这样的遍历过程中，我们要提取variable、literal、一元操作符以及二元操作符，并将它们的运算次序以逆波兰式的形式组织起来。我们采用的提取转换算法如下：

- 我们借由两个Stack来完成此次转换，s1用于存储已有序的逆波兰式；s2是一个临时栈，用于临时存放一元和二元操作符；
- 我们在所有节点的ExitXXX回调中执行提取操作；
- 当节点为variable或literal时，直接将节点text转换为对应的类型值(比如int、float64或string)后，打包为Value，压入s1栈；
- 当节点为一元操作符节点时，计算节点深度(level)，与其代表的一个semantic.UnaryOperator一同压入s2栈；
- 当节点为二元操作符节点时，包括arithmeticOp、comparisionOp以及logicalOp，则用当前节点的深度(level)与s2栈顶元素进行比较，如果比s2栈顶内的节点的深度(level)小，就将s2栈顶的节点弹出，并压入s1栈；循环此步骤，直到s2栈空或当前节点深度大于s2栈顶元素深度，则将该节点打包为semantic.BinaryOperator并压入s2栈；
- 在顶层conditionExpr节点(parent node为ruleLine)的exit回调中，将s2栈中元素全部弹出并依次压入s1栈；此时s1栈中从栈底到栈顶就是一个逆波兰式。

下面是具体的代码实现，我们建立一个ReversePolishExprListener结构用于从语法树中提取用于构建语义模型的信息：

```
// tdat/reverse_polish_expr_listener.go
type ReversePolishExprListener struct {
*parser.BaseTdatListener
ruleID string
// for constructing Reverse Polish expression
//
// infixExpr:($speed<5)and($temperature<2)or(roundDown($sanility)<600) =>
//
// reversePolishExpr:
// $speed,5,<,$temperature,2,<,and,$sanility,roundDown,600,<,or
//
reversePolishExpr []semantic.Value
s1 semantic.Stack[*Item] // temp stack for constructing reversePolishExpr, for final result
s2 semantic.Stack[*Item] // temp stack for constructing reversePolishExpr, for operator temporarily
// for windowsRange
low int
high int
// for enumerableFunc
ef string
// for result
result []string
}
```


对于variable、literal都是直接压到s1栈中，对于一元操作符，直接压入s2栈中；对于二元操作符，我们以比较操作符(comparisonOp)为例，看看其处理逻辑：

```
func (l *ReversePolishExprListener) ExitComparisonOp(c *parser.ComparisonOpContext) {
l.handleBinOperator(c.BaseParserRuleContext)
}
func (l *ReversePolishExprListener) handleBinOperator(c *antlr.BaseParserRuleContext) {
v := c.GetText()
lvl := getLevel(c)
for {
lastOp := l.s2.Top()
if lastOp == nil {
l.s2.Push(&Item{
level: lvl,
val: &semantic.BinaryOperator{
Val: v,
},
})
return
}
if lvl > lastOp.level {
l.s2.Push(&Item{
level: lvl,
val: &semantic.BinaryOperator{
Val: v,
},
})
return
}
l.s1.Push(l.s2.Pop())
}
}
```


算术操作符、逻辑操作符等二元操作符都像比较操作符一样，直接调用handleBinOperator。handleBinOperator的逻辑就像我们前面描述的算法步骤那样，先比较s2栈顶的节点的level，如果该节点的深度比s2栈顶内的节点的深度(level)小，就将s2栈顶的节点弹出，并压入s1栈；循环此步骤，直到s2栈空或当前节点深度大于s2栈顶节点深度，则将该节点打包为semantic.BinaryOperator并压入s2栈。

我们在最顶层的conditionExpr中基于s1栈得到我们期望的逆波兰表达式：

```
func (l *ReversePolishExprListener) ExitConditionExpr(c *parser.ConditionExprContext) {
// get the rule index of parent context
if i, ok := c.GetParent().(antlr.RuleContext); ok {
if i.GetRuleIndex() != parser.TdatParserRULE_ruleLine {
// 非最顶层的conditionExpr节点
return
}
}
// pop all left in the stack
for l.s2.Len() != 0 {
l.s1.Push(l.s2.Pop())
}
// fill in the reversePolishExpr
var vs []semantic.Value
for l.s1.Len() != 0 {
vs = append(vs, l.s1.Pop().val)
}
for i := len(vs) - 1; i >= 0; i-- {
l.reversePolishExpr = append(l.reversePolishExpr, vs[i])
}
}
```


其他诸如result、windowsRange等构建语义模型所需的信息的提取比较简单，大家可以直接参考ReversePolishExprListener相应的方法的源码。

### 二. 实例化Processor并运行语法示例

是时候将这门语言的前端(语法树)和后端(语义模型)串起来了！为此，我们定义了一个类型Processor用于组装前端与后端：

```
type Processor struct {
name string // for ruleid
model *semantic.Model
}
```


同时每个Processor实例对应一个语法rule，如果有多个rule，可以实例化不同的Processor，之后我们就可以使用Processor实例的Exec方法来处理数据了：

```
func (p *Processor) Exec(in []map[string]interface{}) (map[string]interface{}, error) {
return p.model.Exec(in)
}
```


我们看一下main函数：

```
// tdat/main.go
func main() {
println("input file:", os.Args[1])
input, err := antlr.NewFileStream(os.Args[1])
if err != nil {
panic(err)
}
lexer := parser.NewTdatLexer(input)
stream := antlr.NewCommonTokenStream(lexer, 0)
p := parser.NewTdatParser(stream)
tree := p.Prog()
l := NewReversePolishExprListener()
antlr.ParseTreeWalkerDefault.Walk(l, tree)
processor := &Processor{
name: l.ruleID,
model: semantic.NewModel(l.reversePolishExpr, semantic.NewWindowsRange(l.low, l.high), l.ef, l.result),
}
// r0006: Each { |1,3| ($speed < 50) and (($temperature + 1) < 4) or ((roundDown($salinity) <= 600.0) or (roundUp($ph) > 8.0)) } => ();
in := []map[string]interface{}{
{
"speed": 30,
"temperature": 6,
"salinity": 500.0,
"ph": 7.0,
},
{
"speed": 31,
"temperature": 7,
"salinity": 501.0,
"ph": 7.1,
},
{
"speed": 30,
"temperature": 6,
"salinity": 498.0,
"ph": 6.9,
},
}
out, err := processor.Exec(in)
if err != nil {
panic(err)
}
fmt.Printf("%v\n", out)
}
```


main函数的步骤大致是：构建语法树(p.Prog)，提取语义模型所需信息(ParseTreeWalkerDefault.Walk)，然后实例化Processor，连接前后端，最后通过processor.Exec处理输入数据in。

接下来，我们定义samples/sample4.t作为语法示例来测试main：

```
// samples/sample4.t
r0006: Each { |1,3| ($speed < 50) and (($temperature + 1) < 4) or ((roundDown($salinity) <= 600.0) or (roundUp($ph) > 8.0)) } => ();
```


构建并执行main：

```
$make
$./tdat samples/sample4.t
map[ph:7 salinity:500 speed:30 temperature:6]
```


我们看到，程序输出了我们期望的结果！

### 三. 小结

到这里，我们为《后天》里的气象学家构建的DSL语言以及其处理引擎的核心都已经介绍完了。上述代码**目前仅能处理一个源文件中仅有一个rule**。将处理引擎扩展为可以支持在一个源文件中放置多个rule的任务就留给大家作为“作业”了^_^。

经过这个系列四篇文章后，相信你已经基本了解了基于ANTLR和Go设计和实现一门DSL语言的方法。现在你可以为你的领域设计你自用或团队自用的DSL了，欢迎大家在文章后面留言交流，我们一起提升设计和实现DSL的水平。

本文中涉及的代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/antlr/tdat)下载 – https://github.com/bigwhite/experiments/tree/master/antlr/tdat 。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论