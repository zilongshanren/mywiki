---
title: Go语言项目的安全评估技术
url: https://tonybai.com/2019/11/08/security-assessment-techniques-for-go-projects/
published: '2019-11-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言项目的安全评估技术

在今年夏天我们对[Kubernetes的评估](https://github.com/trailofbits/audit-kubernetes)成功之后，我们收到了大量[Go项目](https://tonybai.com/tag/go)的安全评估需求。为此，我们将在其他编译语言中使用过的安全评估技术和策略调整适配到多个Go项目中。

我们从了解语言的设计开始，识别出开发人员可能无法完全理解语言语义特性的地方。多数这些被误解的语义来自我们向客户报告的调查结果以及对语言本身的独立研究。尽管不是详尽无遗，但其中一些问题领域包括作用域、协程、错误处理和依赖管理。值得注意的是，其中许多与运行时没有直接关系。默认情况下，Go运行时本身的设计是安全的，避免了很多类似C语言的漏洞。

对根本原因有了更好地理解后，我们搜索了现有的能帮助我们快速有效检测客户端代码库的工具。结果我们找到一些静态和动态开源工具，其中包括了一些与Go无关的工具。为了配合这些工具使用，我们还确定了几种有助于检测的编译器配置。

## 一. 静态分析

由于Go是一种编译型语言，因此编译器在生成二进制可执行文件之前就检测并杜绝了许多潜在的错误模式。虽然对于新的Go开发人员来说，这些编译器的输出[比较烦](https://tip.golang.org/doc/faq#unused_variables_and_imports)，但是这些警告对于防止意外行为以及保持代码的清洁和可读性非常重要。

静态分析趋向于捕获很多未包括在编译器错误和警告中的悬而未决的问题。在Go语言生态系统中，有[许多不同的工具](https://github.com/mre/awesome-static-analysis#go)，例如[go-vet](https://tip.golang.org/cmd/vet/)、[staticcheck](https://github.com/dominikh/go-tools)和[analysis包](https://godoc.org/golang.org/x/tools/go/analysis)中的工具。这些工具通常会识别出诸如变量遮蔽、不安全的指针使用以及未使用的函数返回值之类的问题。调查这些工具显示警告的项目区域通常会发现可被利用(进行安全攻击)的功能特性。

这些工具绝不是完美的。例如，go-vet可能会错过非常常见的问题，例如下面例子中这种。

```
package main
import "fmt"
func A() (bool, error) { return false, fmt.Errorf("I get overridden!") }
func B() (bool, error) { return true, nil }
func main() {
aSuccess, err := A()
bSuccess, err := B()
if err != nil {
fmt.Println(err)
}
fmt.Println(aSuccess, ":", bSuccess)
}
```


这个例子未使用A函数的err返回值，并在表达式左侧为bSuccess赋值期间立即重新对err做了赋值。编译器针对这种情况不会提供警告，而go-vet也不会检测到该问题；[errcheck](https://github.com/kisielk/errcheck)也不会。实际上，能成功识别这种情况的工具是前面提到的staticcheck和[ineffassign](https://github.com/gordonklaus/ineffassign)，它们将A的错误返回值标识为未使用或无效。

示例程序的输出以及errcheck，go-vet，staticcheck和ineffassign的检查结果如下：

```
$ go run .
false : true
$ errcheck .
$ go vet .
$ staticcheck .
main.go:5:50: error strings should not be capitalized (ST1005)
main.go:5:50: error strings should not end with punctuation or a newline (ST1005)
main.go:10:12: this value of err is never used (SA4006)
$ ineffassign .
main.go:10:12: ineffectual assignment to err
```


当您深入研究此示例时，您可能会想知道为什么编译器没有针对此问题发出警告。当程序中有未使用的变量时，Go编译器将出错，但此示例成功通过编译。这是由“短变量声明”的语义引起的。下面是短变量声明的语法规范：

```
ShortVarDecl = IdentifierList ":=" ExpressionList .
```


根据规范，短变量声明具有重新声明变量的特殊功能，只要：

- 重新声明在多变量短声明中。
- 重新声明的变量在同一代码块或函数的参数列表中声明较早。
- 重新声明的变量与先前的声明具有相同的类型。
- 声明中至少有一个非空白变量(“_”)是新变量。

所有这些约束在上一个示例中均得到满足，从而防止了编译器针对此问题产生编译错误。

许多工具都具有类似这样的极端情况，即它们在识别相关问题或识别问题但以不同的方式描述时均未成功。使问题复杂化的是，这些工具通常需要先构建Go源代码，然后才能执行分析。如果分析人员无法轻松构建代码库或其依赖项，这将使第三方安全评估变得复杂。

尽管存在这些困难，但只要付出一点点努力，这些工具就可以很好地提示我们在项目中从何处查找问题。我们建议至少使用[gosec](https://github.com/securego/gosec)、[go-vet](https://tip.golang.org/cmd/vet/)和[staticcheck](https://staticcheck.io/)。对大多数代码库而言，这些工具具有良好的文档和人机工效。他们还提供了针对常见问题的多种检查（例如ineffassign或errcheck）。但是，要对特定类型的问题进行更深入的分析，可能必须使用更具体的分析器，直接针对[SSA](https://godoc.org/golang.org/x/tools/go/ssa)开发定制的工具或使用[semmle](https://semmle.com/)。

## 二. 动态分析

一旦执行了静态分析并检查了结果，动态分析技术通常是获得更深层结果的下一步。由于Go的内存安全性，动态分析通常发现的问题是导致硬崩溃(hard crash)或程序状态无效的问题。Go社区已经建立了各种工具和方法来帮助识别Go生态系统中这些类型的问题。此外，可以改造现有的与语言无关的工具以满足Go动态分析的需求，我们将在下面展示。

### 1. 模糊测试

Go语言领域中最著名的动态测试工具可能是[Dimitry Vyukov](https://github.com/dvyukov/)的[go-fuzz](https://github.com/dvyukov/go-fuzz)了。该工具使您可以快速有效地实施模糊测试，并且它已经有了不错的[战利品](https://github.com/dvyukov/go-fuzz#trophies)。更高级的用户在猎错过程中可能还会发现[分布式的模糊测试](https://github.com/dvyukov/go-fuzz#random-notes)和[libFuzzer的支持](https://github.com/dvyukov/go-fuzz#libfuzzer-support)非常有用。

Google还发布了一个更原生的模糊器(fuzzer)，它拥有一个与上面的[go-fuzz](https://tonybai.com/2015/12/08/go-fuzz-intro/)相似的名字：[gofuzz](https://github.com/google/gofuzz)。它通过初始化具有随机值的结构来帮助用户。与Dimitry的go-fuzz不同，Google的gofuzz不会生成夹具(harness)或协助提供存储崩溃时的输出信息、模糊输入或任何其他类型的信息。尽管这对于测试某些目标可能是不利的，但它使轻量级且可扩展的框架成为可能。

为了简洁起见，我们请您参考各自自述文件中这两个工具的示例。

### 2. 属性测试(property test)

译注：属性测试指编写对你的代码来说为真的逻辑语句（即“属性”），然后使用自动化工具来生成测试输入（一般来说，是指某种特定类型的随机生成输入数据），并观察程序接受该输入时属性是否保持不变。如果某个输入违反了某一条属性，则证明用户程序存在错误 – 摘自网络。


与传统的模糊测试方法不同，Go的testing包（通常用于单元测试和集成测试）为Go函数的“黑盒测试” 提供了[testing/quick子包](https://golang.org/pkg/testing/quick/)。换句话说，它提供了属性测试的基本原语。给定一个函数和生成器，该包可用于构建夹具，以测试在给定输入生成器范围的情况下潜在的属性违规。以下示例是直接摘自官方文档。

```
func TestOddMultipleOfThree(t *testing.T) {
f := func(x int) bool {
y := OddMultipleOfThree(x)
return y%2 == 1 && y%3 == 0
}
if err := quick.Check(f, nil); err != nil {
t.Error(err)
}
}
```


上面示例正在测试OddMultipleOfThree函数，其返回值应始终为3的奇数倍。如果不是，则f函数将返回false并将违反该属性。这是由quick.Check功能检测到的。

虽然此包提供的功能对于属性测试的简单应用是可以接受的，但重要的属性通常不能很好地适合这种基本界面。为了解决这些缺点，诞生了[leanovate/gopter框架](https://github.com/leanovate/gopter)。Gopter为常见的Go类型提供了各种各样的生成器，并且支持您创建与Gopter兼容的[自定义生成器](https://godoc.org/github.com/leanovate/gopter#Gen)。通过[gopter/commands子包](https://godoc.org/github.com/leanovate/gopter/commands)还支持状态测试，这对于测试跨操作序列的属性是否有用很有有帮助。除此之外，当违反属性时，Gopter会缩小生成的输入。请参阅下面的输出中输入收缩的属性测试的简要示例。

Compute结构的测试夹具：

```
package main_test
import (
"github.com/leanovate/gopter"
"github.com/leanovate/gopter/gen"
"github.com/leanovate/gopter/prop"
"math"
"testing"
)
type Compute struct {
A uint32
B uint32
}
func (c *Compute) CoerceInt () { c.A = c.A % 10; c.B = c.B % 10; }
func (c Compute) Add () uint32 { return c.A + c.B }
func (c Compute) Subtract () uint32 { return c.A - c.B }
func (c Compute) Divide () uint32 { return c.A / c.B }
func (c Compute) Multiply () uint32 { return c.A * c.B }
func TestCompute(t *testing.T) {
parameters := gopter.DefaultTestParameters()
parameters.Rng.Seed(1234) // Just for this example to generate reproducible results
properties := gopter.NewProperties(parameters)
properties.Property("Add should never fail.", prop.ForAll(
func(a uint32, b uint32) bool {
inpCompute := Compute{A: a, B: b}
inpCompute.CoerceInt()
inpCompute.Add()
return true
},
gen.UInt32Range(0, math.MaxUint32),
gen.UInt32Range(0, math.MaxUint32),
))
properties.Property("Subtract should never fail.", prop.ForAll(
func(a uint32, b uint32) bool {
inpCompute := Compute{A: a, B: b}
inpCompute.CoerceInt()
inpCompute.Subtract()
return true
},
gen.UInt32Range(0, math.MaxUint32),
gen.UInt32Range(0, math.MaxUint32),
))
properties.Property("Multiply should never fail.", prop.ForAll(
func(a uint32, b uint32) bool {
inpCompute := Compute{A: a, B: b}
inpCompute.CoerceInt()
inpCompute.Multiply()
return true
},
gen.UInt32Range(0, math.MaxUint32),
gen.UInt32Range(0, math.MaxUint32),
))
properties.Property("Divide should never fail.", prop.ForAll(
func(a uint32, b uint32) bool {
inpCompute := Compute{A: a, B: b}
inpCompute.CoerceInt()
inpCompute.Divide()
return true
},
gen.UInt32Range(0, math.MaxUint32),
gen.UInt32Range(0, math.MaxUint32),
))
properties.TestingRun(t)
}
```


执行测试夹具并观察属性测试的输出（除法失败）：

```
user@host:~/Desktop/gopter_math$ go test
+ Add should never fail.: OK, passed 100 tests.
Elapsed time: 253.291µs
+ Subtract should never fail.: OK, passed 100 tests.
Elapsed time: 203.55µs
+ Multiply should never fail.: OK, passed 100 tests.
Elapsed time: 203.464µs
! Divide should never fail.: Error on property evaluation after 1 passed
tests: Check paniced: runtime error: integer divide by zero
goroutine 5 [running]:
runtime/debug.Stack(0x5583a0, 0xc0000ccd80, 0xc00009d580)
/usr/lib/go-1.12/src/runtime/debug/stack.go:24 +0x9d
github.com/leanovate/gopter/prop.checkConditionFunc.func2.1(0xc00009d9c0)
/home/user/go/src/github.com/leanovate/gopter/prop/check_condition_func.g
o:43 +0xeb
panic(0x554480, 0x6aa440)
/usr/lib/go-1.12/src/runtime/panic.go:522 +0x1b5
_/home/user/Desktop/gopter_math_test.Compute.Divide(...)
/home/user/Desktop/gopter_math/main_test.go:18
_/home/user/Desktop/gopter_math_test.TestCompute.func4(0x0, 0x0)
/home/user/Desktop/gopter_math/main_test.go:63 +0x3d
# snip for brevity;
ARG_0: 0
ARG_0_ORIGINAL (1 shrinks): 117380812
ARG_1: 0
ARG_1_ORIGINAL (1 shrinks): 3287875120
Elapsed time: 183.113µs
--- FAIL: TestCompute (0.00s)
properties.go:57: failed with initial seed: 1568637945819043624
FAIL
exit status 1
FAIL _/home/user/Desktop/gopter_math 0.004s
```


### 3. 故障注入

在攻击Go系统时，故障注入令人惊讶地有效。我们使用此方法发现的最常见错误包括对error类型的处理。因为error在Go中只是一种类型，所以当它返回时，它不会像panic语句那样自行改变程序的执行流程。我们通过强制生成来自最低级别(内核)的错误来识别此类错误。由于Go会生成静态二进制文件，因此必须在不使用LD_PRELOAD的情况下注入故障。我们的工具之一[KRF](https://github.com/trailofbits/krf)使我们能够做到这一点。

在我们最近的Kubernetes代码库评估中，我们使用KRF找到了一个vendored依赖深处的[问题](https://github.com/kubernetes/kubernetes/issues/81135)，只需通过随机为进程和其子进程发起的read和write系统调用制造故障。该技术对通常与底层系统交互的Kubelet十分有效。该错误是在ionice命令出现错误时触发的，未向STDOUT输出信息并向STDERR发送错误。记录错误后，将继续执行而不是将STDERR的错误返回给调用方。这导致STDOUT后续被索引，从而导致索引超出范围导致运行时panic。

下面是导致kubelet panic的调用栈信息：

```
E0320 19:31:54.493854 6450 fs.go:591] Failed to read from stdout for cmd [ionice -c3 nice -n 19 du -s /var/lib/docker/overlay2/bbfc9596c0b12fb31c70db5ffdb78f47af303247bea7b93eee2cbf9062e307d8/diff] - read |0: bad file descriptor
panic: runtime error: index out of range
goroutine 289 [running]:
k8s.io/kubernetes/vendor/github.com/google/cadvisor/fs.GetDirDiskUsage(0xc001192c60, 0x5e, 0x1bf08eb000, 0x1, 0x0, 0xc0011a7188)
/workspace/anago-v1.13.4-beta.0.55+c27b913fddd1a6/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/github.com/google/cadvisor/fs/fs.go:600 +0xa86
k8s.io/kubernetes/vendor/github.com/google/cadvisor/fs.(*RealFsInfo).GetDirDiskUsage(0xc000bdbb60, 0xc001192c60, 0x5e, 0x1bf08eb000, 0x0, 0x0, 0x0)
/workspace/anago-v1.13.4-beta.0.55+c27b913fddd1a6/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/github.com/google/cadvisor/fs/fs.go:565 +0x89
k8s.io/kubernetes/vendor/github.com/google/cadvisor/container/common.(*realFsHandler).update(0xc000ee7560, 0x0, 0x0)
/workspace/anago-v1.13.4-beta.0.55+c27b913fddd1a6/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/github.com/google/cadvisor/container/common/fsHandler.go:82 +0x36a
k8s.io/kubernetes/vendor/github.com/google/cadvisor/container/common.(*realFsHandler).trackUsage(0xc000ee7560)
/workspace/anago-v1.13.4-beta.0.55+c27b913fddd1a6/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/github.com/google/cadvisor/container/common/fsHandler.go:120 +0x13b
created by
k8s.io/kubernetes/vendor/github.com/google/cadvisor/container/common.(*realFsHandler).Start
/workspace/anago-v1.13.4-beta.0.55+c27b913fddd1a6/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/vendor/github.com/google/cadvisor/container/common/fsHandler.go:142 +0x3f
```


下面例子：记录了STDERR日志但未将error返回调用方。

```
stdoutb, souterr := ioutil.ReadAll(stdoutp)
if souterr != nil {
klog.Errorf("Failed to read from stdout for cmd %v - %v", cmd.Args, souterr)
}
```


当stdout为空，也尝试使用索引，这是运行时出现panic的原因：

```
usageInKb, err := strconv.ParseUint(strings.Fields(stdout)[0], 10, 64)
```


更完整的包含重现上述问题的步骤，可参见我们的[Kubernetes最终报告](https://github.com/kubernetes/community/blob/master/wg-security-audit/findings/Kubernetes%20Final%20Report.pdf)附录G（第109页），那里详细介绍了针对Kubelet使用KRF的方法。

Go的编译器还允许将测量工具包含在二进制文件中，从而可以在运行时检测race状况，这对于将潜在的race识别为攻击者非常有用，但也可以用来识别对defer、panic和recover的不正确处理。我们构建了[Trailofbits/on-edge](https://github.com/trailofbits/on-edge)来做到这一点：识别函数入口点和函数panic点之间的全局状态变化，并通过Go race检测器”泄露”此信息。有关OnEdge的更多详细信息，请参见我们以前的博客文章[“在Go中选择正确panic的方式”](https://blog.trailofbits.com/2019/06/26/panicking-the-right-way-in-go/)。

实践中，我们建议使用：

- dvyukov/go-fuzz为组件解析输入建立夹具
- google/gofuzz用于测试结构验证
- leanovate/gopter用于增强现有的单元和集成测试以及测试规范的正确性
- Trailofbits/krf和Trailofbits/on-edge用于测试错误处理。

除KRF外，所有这些工具在实践中都需要付出一些努力。

## 三. 利用编译器的优势

Go编译器具有许多内置功能和指令(directive)，可帮助我们查找错误。这些功能隐藏在各种开关中中，并且需要一些配置才能达到我们的目的。

### 1. 颠覆类型系统

有时在尝试测试系统功能时，导出函数不是我们要测试的。要获得对所需的函数的测试访问权，可能需要重命名许多函数，以便可以将其导出，这可能会很麻烦。要解决此问题，可以使用编译器的[build指令(directive)](https://tip.golang.org/cmd/compile/#hdr-Compiler_Directives)进行名称链接(name linking)以及导出系统的访问控制。作为此功能的示例，下面的程序（从[Stack Overflow答案](https://stackoverflow.com/a/32135975)中提取）访问未导出的reflect.typelinks函数，并随后迭代类型链接表以识别已编译程序中存在的类型。

下面是使用linkname build directive的Stack Overflow答案的通用版本:

```
package main
import (
"fmt"
"reflect"
"unsafe"
)
func Typelinks() (sections []unsafe.Pointer, offset [][]int32) {
return typelinks()
}
//go:linkname typelinks reflect.typelinks
func typelinks() (sections []unsafe.Pointer, offset [][]int32)
func Add(p unsafe.Pointer, x uintptr, whySafe string) unsafe.Pointer {
return add(p, x, whySafe)
}
//go:linkname add reflect.add
func add(p unsafe.Pointer, x uintptr, whySafe string) unsafe.Pointer
func main() {
sections, offsets := Typelinks()
for i, base := range sections {
for _, offset := range offsets[i] {
typeAddr := Add(base, uintptr(offset), "")
typ := reflect.TypeOf(*(*interface{})(unsafe.Pointer(&typeAddr)))
fmt.Println(typ)
}
}
}
```


下面是typelinks表的输出：

```
$ go run main.go
**reflect.rtype
**runtime._defer
**runtime._type
**runtime.funcval
**runtime.g
**runtime.hchan
**runtime.heapArena
**runtime.itab
**runtime.mcache
**runtime.moduledata
**runtime.mspan
**runtime.notInHeap
**runtime.p
**runtime.special
**runtime.sudog
**runtime.treapNode
**sync.entry
**sync.poolChainElt
**syscall.Dirent
**uint8
```


如果需要在运行时进行更精细的控制（即，不仅仅是linkname指令），则可以编写Go的[中间汇编码](https://golang.org/doc/asm#introduction)，并在编译过程中包括它。尽管在某些地方它可能不完整且有些过时，但是[teh-cmc/go-internals](https://golang.org/doc/asm#introduction)提供了有关Go如何组装函数的很好的介绍。

### 2. 编译器生成的覆盖图

为了帮助进行测试，Go编译器可以[执行预处理](https://blog.golang.org/cover)以生成coverage信息。这旨在标识单元测试和集成测试的测试覆盖范围信息，但是我们也可以使用它来标识由模糊测试和属性测试生成的测试覆盖范围。Filippo Valsorda在[博客文章](https://blog.cloudflare.com/go-coverage-with-external-tests/)中提供了一个简单的示例。

### 3. 类型宽度安全

Go支持根据目标平台自动确定整数和浮点数的大小。但是，它也允许使用固定宽度的定义，例如int32和int64。当混合使用自动宽度和固定宽度大小时，对于跨多个目标平台的行为，可能会出现错误的假设。

针对目标的32位和64位平台构建进行测试将有助于识别特定于平台的问题。这些问题通常在执行验证、解码或类型转换的时候发现，原因在于对源和目标类型属性做出了不正确的假设。在Kubernetes安全评估中就有一些这样的示例，特别是[TOB-K8S-015：使用strconv.Atoi并将结果向下转换时的溢出](https://github.com/kubernetes/kubernetes/issues/81121)（Kubernetes最终报告中的第42页），下面是这个示例。

```
// updatePodContainers updates PodSpec.Containers.Ports with passed parameters.
func updatePodPorts(params map[string]string, podSpec *v1.PodSpec) (err error) {
port := -1
hostPort := -1
if len(params["port"]) > 0 {
port, err = strconv.Atoi(params["port"]) // <-- this should parse port as strconv.ParseUint(params["port"], 10, 16)
if err != nil {
return err
}
}
// (...)
// Don't include the port if it was not specified.
if len(params["port"]) > 0 {
podSpec.Containers[0].Ports = []v1.ContainerPort{
{
ContainerPort: int32(port), // <-- this should later just be uint16(port)
},
}
```


错误的类型宽度假设导致的溢出：

```
root@k8s-1:/home/vagrant# kubectl expose deployment nginx-deployment --port 4294967377 --target-port 4294967376
E0402 09:25:31.888983 3625 intstr.go:61] value: 4294967376 overflows int32
goroutine 1 [running]:
runtime/debug.Stack(0xc000e54eb8, 0xc4f1e9b8, 0xa3ce32e2a3d43b34)
/usr/local/go/src/runtime/debug/stack.go:24 +0xa7
k8s.io/kubernetes/vendor/k8s.io/apimachinery/pkg/util/intstr.FromInt(0x100000050, 0xa, 0x100000050, 0x0, 0x0)
...
service/nginx-deployment exposed
```


实际上，很少需要颠覆类型系统。最需要的测试目标已经是导出了的，可以通过import获得。我们建议仅在需要助手和测试类似的未导出函数时才使用此功能。至于测试类型宽度安全性，我们建议您尽可能对所有目标进行编译，即使没有直接支持也是如此，因为不同目标上的问题可能更明显。最后，我们建议至少生成包含单元测试和集成测试的项目的覆盖率报告。它有助于确定未经直接测试的区域，这些区域可以优先进行审查。

## 四. 有关依赖的说明

在诸如JavaScript和Rust的语言中，依赖项管理器内置了对依赖项审核的支持-扫描项目依赖项以查找已知存在漏洞的版本。在Go中，不存在这样的工具，至少没有处于公开可用且非实验状态的。

这种缺乏可能是由于存在多种不同的依赖关系管理方法：[go-mod](https://blog.golang.org/using-go-modules)，[go-get](https://golang.org/cmd/go/#hdr-Legacy_GOPATH_go_get)，[vendored](https://golang.org/cmd/go/#hdr-Vendor_Directories)等。这些不同的方法使用根本不同的实现方案，导致无法直接识别依赖关系及其版本。此外，在某些情况下，开发人员通常会随后修改其vendor的依赖的源代码。

在Go的开发过程中，依赖管理问题的解决已经取得了进展，大多数开发人员都在朝使用go mod的方向发展。这样就可以通过项目中的go.mod跟踪和依赖项并进行版本控制，从而为以后的依赖项扫描工作打开了大门。我们可以在[OWASP DependencyCheck工具](https://github.com/jeremylong/DependencyCheck)中看到此类工作的示例，该工具是具有实验性质的go mod插件。

## 五. 结论

最终，Go生态系统中有许多可以使用的工具。尽管大多数情况是完全不同的，但是各种静态分析工具可帮助识别给定项目中的“悬而未决的问题”。当寻求更深层次的关注时，可以使用模糊测试，属性测试和故障注入工具。编译器配置随后增强了动态技术，使构建测试夹具和评估其有效性变得更加容易。

本文翻译自[“Security assessment techniques for Go projects”](https://blog.trailofbits.com/2019/11/07/attacking-go-vr-ttps/)。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

发现您的文章出现在别的网站，作者也没著名是您。就当提个醒吧。

网址如下，文章就是当前这篇。

http://itindex.net/detail/60137-go-%E8%AF%AD%E8%A8%80-%E9%A1%B9%E7%9B%AE

感谢提醒。