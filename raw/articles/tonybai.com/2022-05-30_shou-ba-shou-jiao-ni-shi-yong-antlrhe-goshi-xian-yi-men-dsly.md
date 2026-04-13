---
title: 手把手教你使用ANTLR和Go实现一门DSL语言（第五部分）：错误处理
url: https://tonybai.com/2022/05/30/an-example-of-implement-dsl-using-antlr-and-go-part5/
published: '2022-05-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 手把手教你使用ANTLR和Go实现一门DSL语言（第五部分）：错误处理

![](https://tonybai.com/wp-content/uploads/an-example-of-implement-dsl-using-antlr-and-go-part5-1.png)


[本文永久链接](https://tonybai.com/2022/05/30/an-example-of-implement-dsl-using-antlr-and-go-part5) – https://tonybai.com/2022/05/30/an-example-of-implement-dsl-using-antlr-and-go-part5

无论是端应用还是云应用，要上生产环境，有一件事必须要做好，那就是**错误处理**。在本系列前面的文章中，我们[设计了文法与语法](https://tonybai.com/2022/05/24/an-example-of-implement-dsl-using-antlr-and-go-part1)、[建立并验证了语义模型](https://tonybai.com/2022/05/27/an-example-of-implement-dsl-using-antlr-and-go-part3)，但我们没有特别关注错误处理。在这一篇中，我们就来补上这个环节。

DSL设计与实现过程有以下几个主要环节，在不同环节，我们关注的错误处理的主要对象是不同的。如下图所示：

![](../../assets/7dc23e022c984533.png)


在**文法设计与验证环节**，我们更多关注文法设计的正确性。错误的文法会导致解析法示例时失败，但这个环节是在生产Parser代码之前，我们更多是通过ANTLR提供的调试工具对文法的正确性进行调试，无需自己写代码做错误处理。

在**语法解析与建立语法树环节**，由于文法问题已经解决，生成的Parser可以解析正确的语法示例了。此时，错误处理主要聚焦在如何处理语法错误上面。

而在**组装语义模型并语义模型执行环节**，我们关注的则是用于组装语义模型的元素值的合理性。以windowsRange为例，在语义模型中，它有两个元素low和max，代表的windowsRange为[low, max]。但如果你的源码中low的值大于了max的值，从语法的角度是合法的，是可以通过语法解析的。但在语义层面，这就是不合理的。在组装语义模型与执行环节，我们需要将这类问题找出来，报告错误并进行处理。

在本文中我们将对后面两个环节的错误处理的思路与方法做简要说明。

### 一. 语法解析的错误处理

语法解析这个环节就好比静态语言的编译或动态语言的解析，如果发现语法错误，则提供源码中语法错误的位置和相关辅助信息。ANTLR的Go runtime中提供了ErrorListener接口以及一个DefaultErrorListener的空实现：

```
// github.com/antlr/antlr4/runtime/Go/antlr/error_listener.go
type ErrorListener interface {
SyntaxError(recognizer Recognizer, offendingSymbol interface{}, line, column int, msg string, e RecognitionException)
ReportAmbiguity(recognizer Parser, dfa *DFA, startIndex, stopIndex int, exact bool, ambigAlts *BitSet, configs ATNConfigSet)
ReportAttemptingFullContext(recognizer Parser, dfa *DFA, startIndex, stopIndex int, conflictingAlts *BitSet, configs ATNConfigSet)
ReportContextSensitivity(recognizer Parser, dfa *DFA, startIndex, stopIndex, prediction int, configs ATNConfigSet)
}
```


ErrorListener这个接口中的SyntaxError方法正是我们在这个环节需要的，它可以帮助我们捕捉到语法示例解析时的语法错误。

Parser内置了ErrorListener的实现，比如antlr.ConsoleErrorListener。但这个Listener在源码示例的解析过程中啥也不会输出，毫无存在感，我们需要自定义一个可以提示错误语法信息的ErrorListener实现。

下面是我参考《ANTLR4权威指南》中的Java例子实现的一个Go版本的VerboseErrorListener：

```
// tdat/error_listener.go
type VerboseErrorListener struct {
*antlr.DefaultErrorListener
hasError bool
}
func NewVerboseErrorListener() *VerboseErrorListener {
return new(VerboseErrorListener)
}
func (d *VerboseErrorListener) HasError() bool {
return d.hasError
}
func (d *VerboseErrorListener) SyntaxError(recognizer antlr.Recognizer, offendingSymbol interface{}, line, column int, msg string, e antlr.RecognitionException) {
p := recognizer.(antlr.Parser)
stack := p.GetRuleInvocationStack(p.GetParserRuleContext())
fmt.Printf("rule stack: %v ", stack[0])
fmt.Printf("line %d: %d at %v : %s\n", line, column, offendingSymbol, msg)
d.hasError = true
}
```


Parser在解析源码过程中，在发现语法错误时会回调VerboseErrorListener的SyntaxError方法，SyntaxError传入的各个参数中包含语法错误的详细信息，我们只需向上面这样将这些信息按一定格式组装起来输出即可。

另外这里给VerboseErrorListener增加了一个hasError布尔字段，用于标识源文件解析过程中是否出现了语法错误，程序可以根据这个错误标识选择后续的执行路径。

下面是main函数中VerboseErrorListener的用法：

```
func main() {
... ...
lexer := parser.NewTdatLexer(input)
stream := antlr.NewCommonTokenStream(lexer, 0)
p := parser.NewTdatParser(stream)
el := NewVerboseErrorListener()
p.RemoveErrorListeners()
p.AddErrorListener(el)
tree := p.Prog()
if el.HasError() {
return
}
... ...
}
```


从上面代码可以看到，我们在创建TdatParser实例后面，在解析源码(p.Prog())之前，需要先将其默认内置的ErrorListener删除掉，然后加入我们自己的VerboseErrorListener实例。之后main函数根据VerboseErrorListener是否包含监听到语法错误的状态决定是否继续向下执行，如果发现有语法错误，则终止程序运行。

我们添加一个带有语法错误的语法示例sample5-invalid.t：

```
// tdat/samples/sample5-invalid.t
r0006: Aach { |1,3| ($speed < 50e) and (($temperature + 1) < 4) or ((roundDown($salinity) <= 600.0) or (roundUp($ph) > 8.0)) } => ();
```


让tdat程序解析一下sample5-invalid.t，我们得到下面结果：

```
$./tdat samples/sample5-invalid.t
input file: samples/sample5-invalid.t
rule: enumerableFunc line 2: 7 at [@2,8:11='Aach',<29>,2:7] : mismatched input 'Aach' expecting {'Each', 'None', 'Any'}
rule: conditionExpr line 2: 32 at [@13,33:33='e',<29>,2:32] : extraneous input 'e' expecting ')'
```


我们看到，程序输出了语法问题的详细信息，并停止了继续执行。

### 二. 语义模型组装与执行环节的错误处理

和语法解析时相对形式固定的错误处理不同，语义层面的错误形式更加多种多样，分布的位置也比较光，每个解析规则(parse rule)处都可能存在语义问题，就像前面提到的windowsRange的low > high的问题。再比如在传入的数据中找不到result中指明的字段等。

无论是组装语义模型，还是语义模型的执行，都是树的遍历，遍历函数存在递归，且层次可能很深，这样传统的error作为返回值不太适合。最好的方式是结合panic+recover的方式，当某个环节的语义出现问题时，直接panic，然后在上层通过recover捕捉panic，再以error方式将panic携带的error信息返回。我们就以windowRange的语义问题作为一个例子来看看语义模型组装和执行过程中如何处理错误。

首先，我们改造一下ReversePolishExprListener的ExitWindowsWithLowAndHighIndex方法，当解析后发现low > high时，抛出panic：

```
// tdat/reverse_polish_expr_listener.go
func (l *ReversePolishExprListener) ExitWindowsWithLowAndHighIndex(c *parser.WindowsWithLowAndHighIndexContext) {
s := c.GetText()
s = s[1 : len(s)-1] // remove two '|'
t := strings.Split(s, ",")
if t[0] == "" {
l.low = 1
} else {
l.low, _ = strconv.Atoi(t[0])
}
if t[1] == "" {
l.high = windowsRangeMax
} else {
l.high, _ = strconv.Atoi(t[1])
}
if l.high < l.low {
panic(fmt.Sprintf("windowsRange: low(%d) > high(%d)", l.low, l.high))
}
}
```


为了不在main中直接捕获panic，我们将原先的遍历tree的语句：

```
antlr.ParseTreeWalkerDefault.Walk(l, tree)
```


挪到一个新函数extractReversePolishExpr中，我们在extractReversePolishExpr中捕获panic，并以普通error的形式将错误返回给main函数：

```
// tdat/main.go
func extractReversePolishExpr(listener antlr.ParseTreeListener, t antlr.Tree) (err error) {
defer func() {
if x := recover(); x != nil {
err = fmt.Errorf("semantic tree assembly error: %v", x)
}
}()
antlr.ParseTreeWalkerDefault.Walk(listener, t)
return nil
}
```


在main函数中，我们像下面这样使用extractReversePolishExpr：

```
// tdat/main.go
func main() {
... ...
l := NewReversePolishExprListener()
err = extractReversePolishExpr(l, tree)
if err != nil {
fmt.Printf("%s\n", err)
return
}
... ...
}
```


当extractReversePolishExpr返回错误时，意味着提取逆波兰式的过程出现了问题，我们将终止程序运行。

接下来我们就构造一个语义错误的例子samples/sample6-windowrange-invalid.t来看看上述程序捕捉语义错误的过程：

```
// samples/sample6-windowrange-invalid.t
r0006: Each { |3,1| ($speed < 50) and (($temperature + 1) < 4) or ((roundDown($salinity) <= 600.0) or (roundUp($ph) > 8.0)) } => ();
```


运行一下我们的新程序：

```
$./tdat samples/sample6-windowrange-invalid.t
input file: samples/sample6-windowrange-invalid.t
semantic tree assembly error: windowsRange: low(3) > high(1)
```


我们看到：程序成功捕捉到了预期的语义错误。

在后续的语义模型执行过程中，semantic包的Evaluate函数也使用了defer + recover捕捉了可能在表达式树求值过程中可能出现的panic，并通过error形式返回给其调用者。甚至在组装过程中没有被捕捉到的语义问题，一旦引发语义执行错误，同样也会被捕捉到。

由于原理相同，针对语义模型执行过程的错误处理，这里就不赘述了。

### 三. 小结

在本篇文章中，我们补充了设计与实现DSL过程中错误处理，针对语法解析和语义模型组装与执行两个环节给出相应的错误处理方案。

在《领域特定语言》一书中，Martin Fowler写道：“解析和生成输出是编写编译器中容易的部分，真正的难点在于给出更好的错误信息”。错误处理在基于DSL的处理引擎中占有十分重要的地位，良好的错误处理设计对后续引擎的问题诊断、演进与维护大有裨益。

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