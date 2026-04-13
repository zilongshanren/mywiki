---
title: 通过实例理解Go静态单赋值（SSA）
url: https://tonybai.com/2022/10/21/understand-go-ssa-by-example/
published: '2022-10-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Go静态单赋值（SSA）

![](../../assets/d617f14d5b237915.png)


[本文永久链接](https://tonybai.com/2022/10/21/understand-go-ssa-by-example) – https://tonybai.com/2022/10/21/understand-go-ssa-by-example

在上一篇文章[《通过实例理解Go内联优化》](https://tonybai.com/2022/10/17/understand-go-inlining-optimisations-by-example)中，我们探讨了Go编译器在编译中端进行的内联优化。内联优化基于IR中间表示进行，不过Go编译过程不止有一种IR表示，这点和[龙书《编译原理(第二版)》](https://book.douban.com/subject/3296317/)的在第六章“中间代码生成”一开始处的讲解是一致的，即在将给定源语言的一个程序翻译成特定的目标机器代码的过程中，一个编译器可能构造出一系列中间表示(IR)，如下图：

![](../../assets/043e20b2b9fb0bca.png)


高层中间表示更接近于源语言，而低层的中间表示则更接近于目标机器。在Go编译过程中，如果说内联优化使用的IR是高层中间表示，那么低层中间表示非支持静态单赋值(SSA)的中间代码形式莫属。

在这一篇中，我们将沿着Go编译器的后端优化之路继续走下去，我们来认识一下**静态单赋值(SSA)**。

### 1. 静态单赋值(SSA)的历史

静态单赋值(Static Single Assignment，SSA)，也有称为Single Static Assignment的，是一种**中间代码的表示形式(IR)**，或者说是某种中间代码所具备的属性，它是由IBM的三位研究员：Barry K. Rosen、Mark N. Wegman和F. Kenneth Zadeck于1988年提出的。

具有SSA属性的IR都具有这样的特征：

- 每个变量在使用前都需要被定义
- 每个变量被精确地赋值一次(使得一个变量的值与它在程序中的位置无关)

下面是一个简单的例子(伪代码)：

```
y = 1
y = 2
x = y
```


转换为SSA形式为：

```
y1 = 1
y2 = 2
x1 = y2
```


我们看到由于SSA要求每个变量只能赋值一次，因此在转换为SSA后，变量y用y1和y2来表示，后面的序号越大，表明y的版本越新。从这一段三行的代码我们也可以看到，在SSA层面，y1 = 1这行代码就是一行死代码(dead code)，即对结果不会产生影响的代码，可以在中间代码优化时被移除掉。

1991年，同样来自IBM研究院的Ron Cytron和Jeanne Ferrante以及前面的三位研究员又一起给出了[构建SSA的快速算法](https://www.cs.utexas.edu/~pingali/CS380C/2010/papers/ssaCytron.pdf)，这进一步推动了SSA在编译器领域的快速应用。

SSA的提出以及后续的流行正是因为SSA形式中间代码具有很好的优化空间，基于SSA可以开启一些新的编译器优化算法或增强现有的优化算法，因此自SSA提出后，各种主流语言编译器后端均逐渐开始支持SSA，包括GCC、llvm、hotspot JVM、v8 js等。SSA也成为了一种IR表示的事实标准。

那么Go语言是何时开始与SSA结缘的呢？我们继续往下看。

### 2. Go与SSA

相对于GCC、LLVM，[Go编译器还相对年轻](https://tonybai.com/2021/11/11/go-opensource-12-years)，因此SSA加入Go的时间还不算太长。

Go SSA的工作始于[Go 1.5版本](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)实现自举之前，2015年2月初，负责编译器后端的Go团队核心成员的Keith Randall博士就在[golang-dev google group](https://groups.google.com/g/golang-dev)上提出要让Go支持SSA的工作计划：

```
“我想从目前基于语法树的IR转换到更现代的基于SSA的IR。有了SSA IR，我们可以实现很多在当前编译器中难以做到的优化” - Keith Randall
```


同期，Keith Randall博士还编写了[“New SSA Backend for the Go Compiler”](https://docs.google.com/document/d/1szwabPJJc4J-igUZU4ZKprOrNRNJug2JPD8OYi3i1K0/edit)文档，具体介绍了Go要支持SSA的理由以及分几步走的实现方案。

在为什么选择自己实现SSA IR，而不是转换为当时现成的诸如gcc, llvm等支持的IR形式并利用成熟后端进行中间代码优化这个问题上，Keith Randall博士给出了三点理由：

-
从Go编译速度考虑：Go团队和社区对编译速度有着格外的青睐，Randall的目标是设计一个线性时间的SSA算法，实现快速SSA优化，但gcc, llmv等IR显然没有在速度方面给予额外的考虑；

-
从功能完整性上考虑：Go运行时需要精确的栈帧地图(the map of stack frame)，用来支持GC和栈拷贝，这些在gcc, llvm中都不会提供；

- 从Go核心开发者的编译器使用体验方面考虑：如果使用llvm、gcc等ir，显然Go核心开发人员在编译go的时候还需要依赖llvm或gcc，这种额外的依赖对他们来说很难说是体验友好的。

2016年3月1日，在Go 1.7版本的master分支提交权限刚刚打开之后，Keith Randall就将支持ssa的dev.ssa分支合并到Go项目主线中了。

在[Go 1.7版本](https://tonybai.com/2016/06/21/some-changes-in-go-1-7)中，Go正式支持SSA，不过由于时间有限，Go 1.7 SSA仅支持针对amd64架构的优化。即便如此，Go支持SSA后，Keith Randall的benchmark显示性能提升12%，代码段缩小13%：

![](../../assets/575b846da66a8e05.png)



Go 1.7正式发布时，其发布文档称[Go程序的性能因对SSA的支持而提升5%-35%以上](https://go.dev/doc/go1.7)。由此看，Go SSA的实现达到了Keith Randall博士的预期目标，也为Go编译器后续的持续优化奠定了基础。

在2017年2月发布的[Go 1.8版本](https://tonybai.com/2017/02/03/some-changes-in-go-1-8/)中，Go SSA的支持范围扩展到其他所有Go支持的cpu架构，包括arm和arm64、mips和mips64、ppc64等。

了解了Go SSA的演进后，我们再来简单说说Go编译器中SSA的实现。

### 3. 转换为SSA

我们先来看看转换为SSA以及SSA优化在编译过程中所处的位置：

![](../../assets/db7b894ad3f033d5.png)



上图是keith博士在2017年gophercon大会上slide中的一幅图，这幅图中明确了生成SSA形式以及SSA优化所处的环节。不过较新的Go版本中，convert to SSA之前也有一种不同于最初的抽象语法树的ir(比如：Go 1.19)，SSA是由此种ir转换过来的。

从代码上来看，ir到SSA形式的转换发生在下面环节(Go 1.19版本代码，其他版本可能代码位置和内容均由不同)：

```
// $GOROOT/src/cmd/compile/internal/gc/main.go
func Main(archInit func(*ssagen.ArchInfo)) {
base.Timer.Start("fe", "init")
defer handlePanic()
archInit(&ssagen.Arch)
... ...
// Compile top level functions.
// Don't use range--walk can add functions to Target.Decls.
base.Timer.Start("be", "compilefuncs")
fcount := int64(0)
for i := 0; i < len(typecheck.Target.Decls); i++ {
if fn, ok := typecheck.Target.Decls[i].(*ir.Func); ok {
// Don't try compiling dead hidden closure.
if fn.IsDeadcodeClosure() {
continue
}
enqueueFunc(fn)
fcount++
}
}
base.Timer.AddEvent(fcount, "funcs")
compileFunctions()
... ...
}
```


在Main中，我们看到代码会将所有Target.Decls(函数)通过enqueueFunc入队列(compilequeue)，然后调用compileFunctions来实现各个函数从AST ir到SSA形式的转换，compileFunctions在compile.go中，其实现如下：

```
// $GOROOT/src/cmd/compile/internal/gc/compile.go
func compileFunctions() {
if len(compilequeue) == 0 {
return
}
... ...
// By default, we perform work right away on the current goroutine
// as the solo worker.
queue := func(work func(int)) {
work(0)
}
... ...
var compile func([]*ir.Func)
compile = func(fns []*ir.Func) {
wg.Add(len(fns))
for _, fn := range fns {
fn := fn
queue(func(worker int) {
ssagen.Compile(fn, worker)
compile(fn.Closures)
wg.Done()
})
}
}
types.CalcSizeDisabled = true // not safe to calculate sizes concurrently
base.Ctxt.InParallel = true
compile(compilequeue)
... ...
}
```


在compileFunctions中我们看到，编译器从compilequeue取出AST IR形式的函数，并调用ssagen.Compile将其编译为SSA形式。下面是ssagen.Compile的代码：

```
// $GOROOT/src/cmd/compile/internal/ssagen/pgen.go
// Compile builds an SSA backend function,
// uses it to generate a plist,
// and flushes that plist to machine code.
// worker indicates which of the backend workers is doing the processing.
func Compile(fn *ir.Func, worker int) {
f := buildssa(fn, worker)
// Note: check arg size to fix issue 25507.
if f.Frontend().(*ssafn).stksize >= maxStackSize || f.OwnAux.ArgWidth() >= maxStackSize {
largeStackFramesMu.Lock()
largeStackFrames = append(largeStackFrames, largeStack{locals: f.Frontend().(*ssafn).stksize, args: f.OwnAux.ArgWidth(), pos: fn.Pos()})
largeStackFramesMu.Unlock()
return
}
pp := objw.NewProgs(fn, worker)
defer pp.Free()
genssa(f, pp)
// Check frame size again.
// The check above included only the space needed for local variables.
// After genssa, the space needed includes local variables and the callee arg region.
// We must do this check prior to calling pp.Flush.
// If there are any oversized stack frames,
// the assembler may emit inscrutable complaints about invalid instructions.
if pp.Text.To.Offset >= maxStackSize {
largeStackFramesMu.Lock()
locals := f.Frontend().(*ssafn).stksize
largeStackFrames = append(largeStackFrames, largeStack{locals: locals, args: f.OwnAux.ArgWidth(), callee: pp.Text.To.Offset - locals, pos: fn.Pos()})
largeStackFramesMu.Unlock()
return
}
pp.Flush() // assemble, fill in boilerplate, etc.
// fieldtrack must be called after pp.Flush. See issue 20014.
fieldtrack(pp.Text.From.Sym, fn.FieldTrack)
}
```


这里贴出了Compile的完整实现，Compile函数中真正负责生成具有SSA属性的中间代码的是buildssa函数，看了一下buildssa函数有近300行代码，有点复杂，这里挑挑拣拣，把主要的调用摘录出来：

```
// $GOROOT/src/cmd/compile/internal/ssagen/ssa.go
// buildssa builds an SSA function for fn.
// worker indicates which of the backend workers is doing the processing.
func buildssa(fn *ir.Func, worker int) *ssa.Func {
name := ir.FuncName(fn)
... ...
// Convert the AST-based IR to the SSA-based IR
s.stmtList(fn.Enter)
s.zeroResults()
s.paramsToHeap()
s.stmtList(fn.Body)
// fallthrough to exit
if s.curBlock != nil {
s.pushLine(fn.Endlineno)
s.exit()
s.popLine()
}
... ...
// Main call to ssa package to compile function
ssa.Compile(s.f)
... ...
}
```


buildssa中的ssa.Compile咱们后续再看，那个涉及到SSA的多轮(pass)优化，我们看一下从基于AST形式的IR到基于SSA形式的IR的转换，无论是fn.Enter还是fn.Body，本质都是一组ir Node，stmtList将这些node逐个转换为SSA形式。Go提供了可视化的ssa dump工具，我们可以更直观的来看一下。

Go语言隶属于命令式编程语言(imperative programming language)，这类编程范式有三大典型控制结构：顺序结构、选择结构和循环结构，我们先来看看一个最简单的顺序结构是如何翻译为SSA的：

```
// github.com/bigwhite/experiments/tree/master/ssa-examples/sequential.go
package main
func sum(a, b, c int) int {
d := a + b
e := d + c
return e
}
func main() {
println(sum(1, 2, 3))
}
```


我们通过下面命令来生成函数sum的SSA转换过程：

```
$GOSSAFUNC=sum go build sequential.go
dumped SSA to ./ssa.html
$mv ssa.html ssa-sequential.html
$open ./ssa-sequential.html
```


上面的open命令会在本地打开浏览器并显示ssa-sequential.html页面：

![](../../assets/5bc7fe8f0fc8f152.png)


上图中，最左侧是源码（源码显示两次，感觉是bug），中间的是AST形式的IR，最右侧的框框中就是Go编译器生成的第一版SSA，为了更好说明，我们将其贴到下面来：

```
// github.com/bigwhite/experiments/tree/master/ssa-examples/ssa-sequential.html
b1:-
v1 (?) = InitMem <mem>
v2 (?) = SP <uintptr>
v3 (?) = SB <uintptr>
v4 (?) = LocalAddr <*int> {a} v2 v1
v5 (?) = LocalAddr <*int> {b} v2 v1
v6 (?) = LocalAddr <*int> {c} v2 v1
v7 (?) = LocalAddr <*int> {~r0} v2 v1
v8 (3) = Arg <int> {a} (a[int])
v9 (3) = Arg <int> {b} (b[int])
v10 (3) = Arg <int> {c} (c[int])
v11 (?) = Const64 <int> [0]
v12 (+4) = Add64 <int> v8 v9 (d[int])
v13 (+5) = Add64 <int> v12 v10 (e[int])
v14 (+6) = MakeResult <int,mem> v13 v1
Ret v14 (+6)
name a[int]: v8
name b[int]: v9
name c[int]: v10
name d[int]: v12
name e[int]: v13
```


从结构上来看，SSA分为两部分，一部分是由b1、Ret组成的blocks，另一部分则是命名变量与SSA value的对应关系。

在SSA中，一个block代表了一个函数控制流图(control flow graph)中的基本代码块(basic block)，从代码注释中可以看到SSA有四种block类型：Plain，If、Exit和Defer：

```
// $GOROOT/src/cmd/compile/internal/ssa/block.go
// BlockKind is the kind of SSA block.
//
// kind controls successors
// ------------------------------------------
// Exit [return mem] []
// Plain [] [next]
// If [boolean Value] [then, else]
// Defer [mem] [nopanic, panic] (control opcode should be OpStaticCall to runtime.deferproc)
type BlockKind int16
```


但实际的BlockKind已经与注释不一致了，opGen.go是一个自动生成的文件，其中的BlockKind类型的常量值有数十个，即便滤掉CPU架构相关的常量，剩下的还有8个(从BlockPlain到BlockFirst)：

```
// $GOROOT/src/cmd/compile/internal/ssa/opGen.go
const (
BlockInvalid BlockKind = iota
... ...
BlockPlain
BlockIf
BlockDefer
BlockRet
BlockRetJmp
BlockExit
BlockJumpTable
BlockFirst
)
```


上面的sum函数的SSA代码例子中，b1应该就是Plain类型的，Ret显然是BlockRet类型。

Plain类型的Block中是一组values，value是SSA的基本构成要素。根据SSA的定义，一个value只能被精确地定义一次，但是它可以被使用任意多次。如示例，一个value主要包括一个唯一的标识符，一个操作符，一个类型和一些参数，下面的Value类型的LongString和LongHTML方法返回的字符串更能说明Value的格式。尤其是LongHTML方法就是输出ssa html中内容的方法：

```
// $GOROOT/src/cmd/compile/internal/ssa/value.go
// long form print. v# = opcode <type> [aux] args [: reg] (names)
func (v *Value) LongString() string {
... ...
}
// $GOROOT/src/cmd/compile/internal/ssa/html.go
func (v *Value) LongHTML() string {
// TODO: Any intra-value formatting?
// I'm wary of adding too much visual noise,
// but a little bit might be valuable.
// We already have visual noise in the form of punctuation
// maybe we could replace some of that with formatting.
s := fmt.Sprintf("<span class=\"%s ssa-long-value\">", v.String())
linenumber := "<span class=\"no-line-number\">(?)</span>"
if v.Pos.IsKnown() {
linenumber = fmt.Sprintf("<span class=\"l%v line-number\">(%s)</span>", v.Pos.LineNumber(), v.Pos.LineNumberHTML())
}
s += fmt.Sprintf("%s %s = %s", v.HTML(), linenumber, v.Op.String())
s += " <" + html.EscapeString(v.Type.String()) + ">"
s += html.EscapeString(v.auxString())
for _, a := range v.Args {
s += fmt.Sprintf(" %s", a.HTML())
}
r := v.Block.Func.RegAlloc
if int(v.ID) < len(r) && r[v.ID] != nil {
s += " : " + html.EscapeString(r[v.ID].String())
}
var names []string
for name, values := range v.Block.Func.NamedValues {
for _, value := range values {
if value == v {
names = append(names, name.String())
break // drop duplicates.
}
}
}
if len(names) != 0 {
s += " (" + strings.Join(names, ", ") + ")"
}
s += "</span>"
return s
}
```


以例子中的v12这一个value为例：

```
v12 (+4) = Add64 <int> v8 v9 (d[int])
```


- v12是该value的唯一标识符，其中的12为ID，ID是从1开始的整数；
- (+4)是对应的源码的行号；
- Add64是操作符；
是value的类型(v.Type())； - v8, v9则是Add64操作符的参数；
- (d[int])是v12对应的LocalSlot，LocalSlot代表栈帧上的一个位置(location)，用来识别和存储输出参数、输出参数或其他变量node。

ssa dump输出的另一部分则是命名变量与SSA value的对应关系，其格式也是：name LocalSlot: value：

```
name a[int]: v8
name b[int]: v9
name c[int]: v10
name d[int]: v12
name e[int]: v13
```


输出上述第二部分的代码如下：

```
// $GOROOT/src/cmd/compile/internal/ssa/print.go
func (p stringFuncPrinter) named(n LocalSlot, vals []*Value) {
fmt.Fprintf(p.w, "name %s: %v\n", n, vals)
}
```


顺序结构的**代码执行流是从上到下的**，每个block后面**仅有一个后继block**，这样的SSA转换较为好理解。

下面我们再来看看一个选择控制结构 – if控制语句的ssa，下面是我们的示例Go源码：

```
// github.com/bigwhite/experiments/tree/master/ssa-examples/selection_if.go
package main
func foo(b bool) int {
if b {
return 2
}
return 3
}
func main() {
println(foo(true))
}
```


我们通过下面命令输出函数foo的SSA中间代码：

```
$GOSSAFUNC=foo go build selection_if.go
dumped SSA to ./ssa.html
$mv ssa.html ssa-selection-if.html
$open ./ssa-selection-if.html
```


open命令启动浏览器显示foo函数的SSA形式：

![](../../assets/52f92426f8686f28.png)


有了上面关Go SSA格式的基础，这段SSA代码分析起来就容易一些了。

这段SSA中有多个block，包括plain block、if block、ret block等。我们重点关注SSA对if语句的处理。

经典SSA转换理论中，SSA将if分支转换为带有Φ函数的SSA代码(如下图)：

![](../../assets/7391702c364dbcae.png)



Φ函数(希腊字母fài)是代码中的一个merge point，它可以将其前置的n个block的执行路径汇聚在一起。不过它仅用于代码分析使用，最终生成的代码中并不会有Φ函数的存在。关于在何处插入Φ函数等算法太理论了，这里就不展开了。

我们看看现实中go针对if语句的处理：

```
b1:
v1 (?) = InitMem <mem>
v2 (?) = SP <uintptr>
v3 (?) = SB <uintptr>
v4 (?) = LocalAddr <*bool> {b} v2 v1
v5 (?) = LocalAddr <*int> {~r0} v2 v1
v6 (3) = Arg <bool> {b} (b[bool])
v7 (?) = Const64 <int> [0]
v8 (?) = Const64 <int> [2]
v11 (?) = Const64 <int> [3]
If v6 → b3 b2 (4)
b2: ← b1
v13 (7) = Copy <mem> v1
v12 (7) = MakeResult <int,mem> v11 v13
Ret v12 (+7)
b3: ← b1
v10 (5) = Copy <mem> v1
v9 (5) = MakeResult <int,mem> v8 v10
Ret v9 (+5)
name b[bool]: v6
```


这里关键是if block，if判断v6即变量b的值，如果为true，代码执行就流向block b3，否则流向block b2。

下面的b2、b3 block也都包含了前置block的属性，以b2为例，对于来自b1 block的流，执行对应block的代码。基于switch的选择语句更为复杂，有兴趣的朋友可以自己看一下ssa-selection-switch.html。

我们最后看一下循环结构，下面是Go代码：

```
// github.com/bigwhite/experiments/tree/master/ssa-examples/for_loop.go
package main
func sumN(n int) int {
var r int
for i := 1; i <= n; i++ {
r = r + i
}
return r
}
func main() {
println(sumN(10))
}
```


其生成的SSA如下图：

![](../../assets/90d5dbcce0101edc.png)


我们看到循环结构的ssa block更多，流向更为复杂，如果将其转换为一张图的话，那就应该是这样的：

![](../../assets/608afd7cf9523d0b.png)


我们看到：无论是选择结构还是循环结构，SSA实质上构建了一个函数的控制流图(control flow graph)，图中每个节点就是一个block，函数的执行控制流在各个block间转移。而后续**基于SSA的优化就是基于block中value的仅赋值一次的特性以及block的控制流图进行的**。

接下来，我们简单看看目前Go基于SSA IR都做了哪些优化。

### 4. 基于SSA的多轮(pass)优化

buildssa函数中ssa.Compile调用执行了基于SSA IR的多轮(passes)优化：

```
// $GOROOT/src/cmd/compile/internal/ssa/compile.go
func Compile(f *Func) {
... ...
for _, p := range passes {
... ...
tStart := time.Now()
p.fn(f)
tEnd := time.Now()
... ...
}
}
```


我们看到，针对某个函数，Compile函数对其安装预置的passes进行多轮优化，都有哪些pass呢？我们来看看：

```
// $GOROOT/src/cmd/compile/internal/ssa/compile.go
// list of passes for the compiler
var passes = [...]pass{
{name: "number lines", fn-3693: numberLines, required: true},
{name: "early phielim", fn-3693: phielim},
{name: "early copyelim", fn-3693: copyelim},
{name: "early deadcode", fn-3693: deadcode}, // remove generated dead code to avoid doing pointless work during opt
{name: "short circuit", fn-3693: shortcircuit},
{name: "decompose user", fn-3693: decomposeUser, required: true},
{name: "pre-opt deadcode", fn-3693: deadcode},
... ...
{name: "regalloc", fn-3693: regalloc, required: true}, // allocate int & float registers + stack slots
{name: "loop rotate", fn-3693: loopRotate},
{name: "stackframe", fn-3693: stackframe, required: true},
{name: "trim", fn-3693: trim}, // remove empty blocks
}
```


粗略数了一下，这里约有50个pass(其中包含多轮的deadcode清理)，每个pass执行的代码都位于$GOROOT/src/cmd/compile/internal/ssa目录下，我们也可以通过dump出的html查看每一pass后得到的SSA结果，以ssa-sequential.html为例，其多轮优化的示意图如下：

![](../../assets/056b95872ef06d5f.png)


点击浏览器页面上的黑体字优化标题(比如：lowered deadcode for cse)，这一步产生的SSA代码都会显示出来，最后一个框框中是基于SSA生成目标架构的汇编代码。

每一个pass都有其独特性，比如cse，代表Common Subexpression Elimination(共同子表达式删除) ，下面是一个cse优化的例子：

```
y = x + 5
...
z = x + 5
```


cse优化后(前提中间过程中x值没变过)：

```
y = x + 5
...
z = y
```


在这个示例中，经过一轮cse，Go便可以节省下一次没必要的加法运算(z = x + 5)。别看一次加法运算不起眼，积累多了也是不小的性能提升，

如果你对某一pass的优化动作感兴趣，可以对照$GOROOT/src/cmd/compile/internal/ssa目录下的代码与浏览器中生成的SSA来对其进行深入研究。

### 5. 小结

编译器后端的逻辑总是很难理解的，本文对Go编译器与SSA的渊源、Go编译器中驱动SSA转换和优化的环节以及Go生成的SSA的形式与过程做了介绍，算是对SSA入了个门。但要想真正搞懂SSA转换以及基于SSA的优化步骤的细节，认真阅读SSA相关的paper和资料(见参考资料)以及相关code是不可或缺的。

本文涉及的代码在[这里](https://github.com/bigwhite/experiments/tree/master/ssa-examples)可以下载。

### 6. 参考资料

- 《编译原理(第二版)》- https://book.douban.com/subject/3296317/
- SSA: Static Single-Assignment Form – https://www.slideserve.com/heidi-farmer/ssa-static-single-assignment-form
- 《Static Single Assignment Book》 – https://pfalcon.github.io/ssabook/latest/book-full.pdf
- Static single-assignment form – https://en.wikipedia.org/wiki/Static_single_assignment_form
- GopherCon 2017: Keith Randall – Generating Better Machine Code with SSA – https://about.sourcegraph.com/blog/go/generating-better-machine-code-with-ssa
- Generating Better Machine Code with SSA(slide) – https://raw.githubusercontent.com/gophercon/2017-talks/master/KeithRandall-GeneratingBetterMachineCodeWithSSA/GeneratingBetterMachineCodeWithSSA.pdf
- New SSA Backend for the Go Compiler – https://docs.google.com/document/d/1szwabPJJc4J-igUZU4ZKprOrNRNJug2JPD8OYi3i1K0/edit

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论