---
title: 手把手教你使用ANTLR和Go实现一门DSL语言（第一部分）：设计DSL语法与文法
url: https://tonybai.com/2022/05/24/an-example-of-implement-dsl-using-antlr-and-go-part1/
published: '2022-05-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 手把手教你使用ANTLR和Go实现一门DSL语言（第一部分）：设计DSL语法与文法

![](../../assets/86eb903ba8acaf4f.png)


[本文永久链接](https://tonybai.com/2022/05/24/an-example-of-implement-dsl-using-antlr-and-go-part1) – https://tonybai.com/2022/05/24/an-example-of-implement-dsl-using-antlr-and-go-part1

在[《使用ANTLR和Go实现DSL入门》](https://tonybai.com/2022/05/10/introduction-of-implement-dsl-using-antlr-and-go)一文中，我们了解了DSL与通用编程语言(GPL)的差异、DSL解析器生成工具选择以及ANTLR文法的简要书写规则，并和大家一起完成了一个CSV解析器的例子。看完上述文章后，你是不是有了**打造属于自己的DSL的冲动**了呢！

那么究竟该如何设计和实现一门自己的DSL呢？在这个系列文章中，我将“手把手”地和大家一起看看设计和实现一门DSL(这里主要指**外部DSL**)的全流程。

结合Martin Fowler在[《领域特定语言》](https://book.douban.com/subject/21964984/)一书中的建议，我将设计与实现一门外部DSL的过程分为如下几个步骤：

![](../../assets/731ea47afe67ca5b.png)



本文是系列文章的第一篇，在这一篇中，我将先来说说前三个步骤，即为某一特定领域设计一门DSL的语法(syntax)、并编写可以解析该DSL的ANTLR文法(grammar)，生成该DSL语法的解析器并验证ANTLR文法的正确性。

到这里有朋友可能会问：“一会儿文法，一会儿又语法，它们到底有啥区别？”，别急！在设计这门DSL语法之前，我先来和大家一起简单理解一下文法与语法的区别。

### 一. 文法(grammar)和语法(syntax)

![](../../assets/4dcc334a446c191c.png)



如上图所示，**语法是面向使用该编程语言的应用开发者的**，就像Go语法面向的是Gopher；而**文法则是面向这门编程语言的编译器或解释器(Interpreter)的核心开发者的**。

我们**通常用自然语言描述编程语言的语法**，这样的文档一般被称为该**编程语言的语言规范(language specification)**，比如用于描述Go语法的[Go语言规范](https://go.dev/ref/spec)。

但自然语言通常是不精确的，有时带有歧义。为了给出更为精确的语法描述，编程语言规范通常也会有采用某种形式语言(比如：EBNF)表示的关于这门语言语法所对应的文法，比如在Go语言规范中，我们就能看到用EBNF所描述的文法：

```
SourceFile = PackageClause ";" { ImportDecl ";" } { TopLevelDecl ";" } .
PackageClause = "package" PackageName .
PackageName = identifier .
ImportDecl = "import" ( ImportSpec | "(" { ImportSpec ";" } ")" ) .
ImportSpec = [ "." | PackageName ] ImportPath .
ImportPath = string_lit .
... ...
```


通常应用开发人员是不会关心这些夹带在语言规范文档中的文法描述的，只有当规范中的说明有歧义时，开发人员才会根据文法中的产生式规则去推导语法的合规形式的，当然了这一推导过程是比较“痛苦”的。

到这里，结合我们在[《使用ANTLR和Go实现DSL入门》](https://tonybai.com/2022/05/10/introduction-of-implement-dsl-using-antlr-and-go)一文中的说明，我们进一步明确了**文法就是一组规则**，这组规则告诉我们如何将文本流转换为语法树。如果转换失败，说明文本流中存在不符合编程语言语法的地方。

此外，**用于描述一门编程语言语法的文法可以不止一种**，每种形式语言工具都有自己的表示形式，比如针对Go语言语法，我们可以使用EBNF给出形式化的文法，也可以使用ANTLR专用的形式化文法。

到这里，你对文法与语法的概念是不是更深刻一些了呢！不过这时可能会有朋友站出来提问：**设计一门编程语言或DSL，是先设计语法还是先设计文法呢**？

在语言设计伊始，**语法和文法设计的边界其实并非那么清晰**。讨论语法是为了确定文法做准备，而一旦确定了一版文法，语法的使用形式又被进一步精确了。**在编程语言/DSL设计过程中，语法与文法是交替螺旋上升的**。简单的DSL语言，可能一轮迭代就完成了全部设计。复杂的通用编程语言可能要反复针对语法讨论多次，确定下来后，才会编写出新一版本的文法，依次反复迭代。

不过**通常来说我们会先确定一版语言的语法**，写出一些采用此版语言语法的样例源文件，供后续文法以及生成的解析器(Parser)验证使用。回顾Go语言的历史，我们会发现Go语言创世团队当初也是这么做的。Robert Griesemer、Rob Pike和Ken Thompson这三位大佬在Google总部的一间会议室里首先进行了一场有关Go具体设计的会议。会后的第二天，Robert Griesemer发出了一封题为“prog lang discussion”的电邮，这封电邮便成为了这门新语言的第一版设计稿，三位大佬在这门语言的一些**基础语法特性与形式**上达成了初步一致：

```
Date: Sun, 23 Sep 2007 23:33:41 -0700
From: "Robert Griesemer" <gri@google.com>
To: "Rob 'Commander' Pike" <r@google.com>, ken@google.com
Subject: prog lang discussion
...
*** General:
Starting point: C, fix some obvious flaws, remove crud, add a few missing features
- no includes, instead: import
- no macros (do we need something instead?)
- ideally only one file instead of a .h and .c file, module interface
should be extracted automatically
- statements: like in C, though should fix 'switch' statement
- expressions: like in C, though with caveats (do we need ',' expressions?)
- essentially strongly typed, but probably w/ support for runtime types
- want arrays with bounds checking on always (except perhaps in 'unsafe mode'-see section on GC)
- mechanism to hook up GC (I think that most code can live w/ GC, but for a true systems
programming language there should be mode w/ full control over memory allocation)
- support for interfaces (differentiate between concrete, or implementation types, and abstract,
or interface types)
- support for nested and anonymous functions/closures (don't pay if not used)
- a simple compiler should be able to generate decent code
- the various language mechanisms should result in predictable code
...
```


基于这版设计，2008年初，Unix之父Ken Thompson实现了第一版Go编译器(文法相关)，用于验证之前的语法设计。

好了，在理解了文法与语法的区别后，接下来，我们就来为某一特定领域创建一门DSL语言，我们先来介绍一下这门DSL的背景与语法设计。

注：以上提到的对文法与语法的理解仅限于计算机编程语言领域，并不一定适合自然语言领域(自然语言领域也有文法与语法的概念)。


### 二. 为《后天》中的气象学家设计一门DSL

![](../../assets/244937f294433c0b.jpeg)


注：下面只是一个虚构的领域例子，大家无需在其合理性、可行性、科学性与严谨性上产生质疑:)。


如果你看过灾难片专业户罗兰·艾默里奇指导的美国灾难题材电影[《后天》](https://movie.douban.com/subject/1308779/)，你肯定会对电影里发生的威胁人类文明的灾难情节记忆犹新。不过《后天》里的情节其实离我们并不“遥远”，尤其是进入二十一世纪以来，极端异常天气在全球各个地区屡屡发生：两极高温冰川消融、北美陆地飓风以及我国2021年华北地区的极端降水等等。各国的气象学家、地球物理科学家们都在努力破解这些极端天气背后的原因，并预测全球气候的走势。他们在全球设置了诸多气象数据的采集装置，就像《后天》中部署在大西洋上的浮标那样，7×24小时地监视着“地球的生命体征”。

![](../../assets/02aaedb28adc1fdf.jpeg)


像浮标这样的采集装置内置采集程序，按照设定的规则定期向中心上报数据或发送异常事件信息。不过浮标一般都是无人值守的，一旦投放，便很难维护。一旦要进行程序升级，比如更新采集数据与上报事件的规则，就比较麻烦了。

如果我们为像浮标这样的采集装置设计一门DSL，让这些装置内置某种DSL引擎，这样变更采集和报警规则只需给装置远程传送一个极小数据量的规则文件即可完成升级，采集装置将按照新规则上报数据和事件。

好了，领域背景介绍完了，下面我们就来为气象学家们分忧，帮助他们设计一门DSL语言，用于“指挥”像浮标这样的数据收集装置按照气象学家们设定的规则上报数据与事件。

### 三. DSL语言的语法样例

我们先来构思一下这门DSL的语法。什么样的DSL是好DSL？没有固定的评价标准。

- 自然语言 vs. 编程语言

有人说DSL是给领域专家用的，应该更贴近自然语言一些，但实际情况是DSL更多还是开发人员/测试人员去写，或有开发经验的领域专家使用。所以在[《领域特定语言》](https://martinfowler.com/books/dsl.html)一书的第二章末尾，Martin Fowler给出关于DSL的特别警示：**不要试图让DSL读起来像自然语言。牢记，DSL是一种程序设计语言**。

![](../../assets/afb1e8412aa503e1.png)


使用DSL更像是在编程，而不是写小说。同自然语言相比，像DSL这样的程序设计语言的目标是**简洁、清晰与精确**。

- 一门大的DSL vs. 多门小的DSL

DSL正如其名，是领域相关的。绝大多数DSL都是非常简单、非常小的“编程语言”，比如一个算术表达式求值语言，再比如DSL一书中格兰特小姐的控制器状态机等。

但DSL始终存在演化成庞然大物-一门图灵完备的通用编程语言的风险，这个是要极力避免的。那么怎么识别这种风险呢？Martin Fowler告诉我们：**如果一个系统整体都是用一门DSL实现的，那么这门DSL就成为了事实上的通用编程语言了**。更佳的作法是**切分领域，为不同领域构建不同的DSL，而不要构建一门DSL用于所有领域**。

好了，到这里我们先了解一下虚构例子的领域需求，我们需要为这样的一个无人值守的海洋浮标设备设计一门DSL，DSL可用于描述采集设备数据采集与上报的规则。

科学家们对设备的采集能力描述如下：

- 可通过传感器周期性(默认间隔一分钟)获取所在坐标位置的大气温度、水温、水流速、盐度、….等物理指标；
- 可对传感器实时获取到的各种物理指标信息进行一元运算(向下取整、向上取整、绝对值)、算术运算(加减乘除取模)、关系运算(大于、小于…)、逻辑运算(与、或) ，构造混合这些运算的条件，当条件为真时，上报指定的物理指标信息；
- 可结合采集设备缓存的历史时刻数据(缓存能力有限，最大300分钟，即300条数据)进行综合条件判定，这里将其定义为
**窗口计算**，判定策略包括：都不满足、全部满足和至少一项满足。

面对这样的需求，我们怎么定义DSL的语法呢？外部DSL的语法设计往往会受到设计者对以往的编程语言的使用经验的影响。很多开发人员都会从自己熟悉的编程语言的语法中“借鉴”一些语法元素来构成自己的DSL。下面是我设计的一组语法样例：

```
r0001: Each { || $speed > 30 } => ("speed", "temperature", "salinity");
r0002: None { |,30| $temperature > 5 } => ("speed", "temperature", "salinity");
r0003: None { |3,| $temperature > 10 } => ("speed", "temperature", "salinity");
r0004: Any { |11,30| ($speed < 5) and ($temperature < 2) and (roundUp($salinity) < 600) } => ("speed", "temperature", "salinity");
r0005: Each { |,| (($speed < 5) and (($temperature + 1) < 10)) or ((roundDown($speed) <= 10) and (roundUp($salinity) >= 500))} => ();
```


到这里，一些童鞋会惊讶到DSL的简单，没错！就像前面所说的，**DSL就应该简单、清晰和表意精确**。

下面我来对上面的语法样例做个简单说明：

- 一条规则占用一行，以ruleID开头，以分号结尾；
- ruleID与rule body之间通过冒号分隔；
- rule body借鉴了Ruby语言中的迭代器语法：

```
#!/usr/bin/ruby
a = [1,2,3,4,5]
b = Array.new
b = a.collect{ |x| x <= 4 }
puts b
输出：
true
true
true
true
false
```


在上面ruby的这种迭代器语法中，collect迭代器会将迭代数组a中每个元素，并针对每个元素进行x <= 4的求值，求值结果存储在b中对应的元素位置上。我借鉴了这种形式的语法，形成支持窗口计算和表达式求值的语法。以下面语法为例：

```
r0001: Each { |1,5| $speed > 30 } => ("speed", "temperature", "salinity");
```


这个规则的含义是：当窗口数据，从第1项到第5项数据中的speed指标都大于30时，输出并上报当前最新的speed、temperature和salinity指标数据。

Each是对窗口满足策略的判定，Each表示窗口数据中每一项都符合后面的条件表达式；其他两个判定词是None和Any，None表示窗口数据中没有一项满足后面的条件表达式；Any表示窗口数据中有一项满足后面的条件表达式即可。

Each后面的大括号中放置了窗口范围以及条件表达式。

两个竖线表示要参与求值的窗口数据，窗口表示的标准形式为|low, high|，low和high是下标值(下标从1开始)，表示的窗口范围为：[low, high]。当省略low时，比如：|, high|表示的窗口范围为|1, high|；当low与high相同时，比如：|n, n|表示只有下标为n这一个元素参与后续求值；当省略high时，比如：|low, |表示窗口范围为|low, max|，其中max为默认设置的窗口的大小；当low与high都省略，但保留逗号时，比如：|,|，表示窗口中所有数据；当low与high都省略，逗号也省略时，比如：||，则表示|1,1|，即窗口中最新的那条数据。这种设计也部分借鉴了Go的切片下标的语法。

窗口后面条件表达式的求值结果要么为true，要么为false。其支持的运算符可以参考r0005规则。物理指标用**$+指标名字**表示，比如$speed。

当整个规则求值结果为真时，输出窗口中最新数据的speed、temperature和salinity这三个指标。如果最后输出指标的元组为空，则代表输出所有指标。

好了，大致确定了DSL语法后，我们就来根据语法样例编写对应ANTLR文法。

### 四. 为DSL编写ANTLR文法

在之前的文章中，我们也提到过，ANTLR文法规则存储在以.g4为后缀的文件中，文件名要与文件内的grammar关键字后面的名字保持一致，比如我们的文件名为Tdat.g4，那么该文件中grammar后面也必须是Tdat：

```
// the grammar for tdat RuleEngine
grammar Tdat;
```


注意：如果生成的解析器的目标语言为Go，那么ANTLR文法文件名必须要大写，否则生成的一些重要的结构无法被导出。


每个ANTLR文法文件都需要一个起始语法解析规则(parser rule)，在Tdat.g4中，我们的起始规则为prog：

```
// the first parser rule, also the first rule of RuleEngine grammar
// prog is a sequence of rule lines.
prog
: ruleLine+
;
```


正如prog规则的注释那样，一个采集装置的完整规则文件是由一组(至少包含一条)规则行（ruleLine)组成。而每个ruleLine的组成模式也非常固定：

```
ruleLine
: ruleID ':' enumerableFunc '{' windowsRange conditionExpr '}' '=>' result ';'
;
```


大家可以对照着前面语法样例来理解ruleLine这个规则。接下来我们自顶向下(从左向右)的将各个组成部分的规则逐一定义就好了。先来看ruleID这个最简单的规则：

- ruleID就是以字母开头，由数字与数字组成的文本：

```
ruleID
: ID
;
// the first char of ID must be a letter
ID
: ID_LETTER (ID_LETTER | DIGIT)*
;
fragment
ID_LETTER
: 'a'..'z'|'A'..'Z'|'_' // [a-zA-Z_]
;
fragment
DIGIT
: [0-9] // match single digit
;
```


像ID这样的词法规则，大家其实无需自己去从头编写，[《ANTLR 4权威指南》](https://book.douban.com/subject/27082372/)或[antlr/grammar-v4](https://github.com/antlr/grammars-v4)中有大量样例可供参考。

- enumerableFunc就是窗口判定策略，这里直接将Each、None和Any定为语言的关键字了：

```
enumerableFunc
: 'Each'
| 'None'
| 'Any'
;
```


- windowsRange是窗口规则，它有两个候选产生式：

```
windowsRange
: '|' INT? '|' #WindowsWithSingleOrZeroIndex
| '|' INT? ',' INT? '|' #WindowsWithLowAndHighIndex
;
```


为了便于后续解析，这里用#为每个产生式起了一个名字，这样后续ANTLR在基于Tdat.g4生成Parser代码时，就会单独针对每个名字生成一对EnterXXX和ExitXXX(以listener模式下为例)，便于我们解析。当然这里你还可以拆分的更细碎一些以进一步减少在处理Parser规则时自己写代码做判断的工作量。

- conditionExpr是这里最复杂的parser规则，它的求值结果永远是true或false，因此我将其产生式规则定义如下：

```
conditionExpr
: conditionExpr logicalOp conditionExpr
| '(' conditionExpr ')'
| primaryExpr comparisonOp primaryExpr
;
```


我们看到：conditionExpr规则有三个候选产生式，它可以是带括号的自身，支持自身通过逻辑操作符(and和or)的运算，也可以是经由比较操作符计算(比如>、<等)的普通表达式(primaryExpr)。

而普通表达式(primaryExpr)同样可以是带括号的自身，可以是经由算术运算符(比如：加减乘除等)计算的普通表达式，可以是单一的指标(METRIC)，可以是经由一元内置函数(比如：roundUp、abs等)计算的普通表达式，当然也可以仅仅是一个字面值(literal)。literal字面值支持整型、浮点(非科学记数法表示形式)和字符串(双引号括起的文本)：

```
primaryExpr
: '(' primaryExpr ')' #BracketExprInPrimaryExpr
| primaryExpr arithmeticOp primaryExpr #ArithmeticExprInPrimaryExpr
| METRIC #MetricInPrimaryExpr
| builtin '(' primaryExpr ')' #BuildinExprInPrimaryExpr
| literal #RightLiteralInPrimaryExpr
;
arithmeticOp
: '+'
| '-'
| '*'
| '/'
| '%'
;
builtin
: 'roundUp'
| 'roundDown'
| 'abs'
;
logicalOp
: 'or'
| 'and'
;
comparisonOp
: '<'
| '>'
| '<='
| '>='
| '=='
| '!='
;
METRIC
: '$' ID // match $speed
;
INT
: DIGIT+
;
FLOAT
: DIGIT+ '.' DIGIT* // match 1. 39. 3.14159 etc...
| '.' DIGIT+ // match .1 .14159
;
STRING
: '"' (ESC|.)*? '"'
;
```


- result规则定义了声明输出指标的形式，它是一个小括号表示的元组，指标间用逗号分隔，如果元组为空，则表示输出所有指标。

```
result
: '(' STRING (',' STRING)* ')' # ResultWithElements
| '(' ')' # ResultWithoutElements
;
```


好了，到这里针对这门DSL的ANTLR文法也编写完了。

### 五. 小结

在这一篇中，我们了解了开发一门DSL的基本流程，我们以一门为气象科学家打造的DSL为示例，和大家一起为该DSL设计了语法样例，并用ANTLR4的文法规则定义了这门DSL。

那么这个文法是否能被ANTLR正确解析并生成目标代码？通过这个文法能否正确识别出前面我们给出的语法样例呢？在下一篇“文法验证”中我将给大家揭晓答案。

本文中涉及的代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/antlr/tdat)下载 – https://github.com/bigwhite/experiments/tree/master/antlr/tdat 。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


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