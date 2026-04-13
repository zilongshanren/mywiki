---
title: 通过实例理解Go逃逸分析
url: https://tonybai.com/2021/05/24/understand-go-escape-analysis-by-example/
published: '2021-05-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Go逃逸分析

![](../../assets/c08a99a7b3f9e718.png)


[本文永久链接](https://tonybai.com/2021/05/24/understand-go-escape-analysis-by-example) – https://tonybai.com/2021/05/24/understand-go-escape-analysis-by-example

翻看了一下自己的[Go文章归档](https://tonybai.com/tag/go)，发现自己从未专门写过有关Go逃逸分析（escape analysis）的文章。关于Go变量的逃逸分析，大多数Gopher其实并不用关心，甚至可以无视。但是如果你将Go应用于性能敏感的领域，要完全压榨出Go应用的性能，那么理解Go逃逸分析就大有裨益了。在本文，我们就一起来理解一下Go的逃逸分析。

### 1. 逃逸分析（escape analysis）要解决的问题

[C/C++语言出身的程序员](https://tonybai.com/tag/c)对堆内存（heap）和栈内存（stack）都有着“泾渭分明”的理解。在操作系统演化出现进程虚拟内存地址（virtual memory address）的概念后，如下图所示，应用程序的虚拟内存地址空间就被划分为堆内存区（如图中的heap）和栈内存区（如图中的stack）：

![](../../assets/b63ad489fc6049d8.jpg)



在x86平台linux操作系统下，如上图，一般将栈内存区放在高地址，栈向下延伸；而堆内存去放在低地址，堆向上延伸，这样做的好处就是便于堆和栈可动态共享那段内存区域。

这是否意味着所有分配在堆内存区域的内存对象地址一定比分配在栈内存区域的内存对象地址要小呢？在C/C++中是这样的，但是在Go语言中，这是不一定的，因为

[go堆内存所使用的内存页(page)与goroutine的栈所使用的内存页是交织在一起的]。

无论是栈内存还是堆内存，对于应用而言都是合法可用的内存地址空间。之所以将其区分开，是因为应用程序的内存分配和管理的需要。

栈内存上的对象的存储空间是自动分配和销毁的，无需开发人员或编程语言运行时过多参与，比如下面的这段C代码（用C代码更能体现栈内存与堆内存的差别）：

```
// github.com/bigwhite/experiments/blob/master/go-escape-analysis/c/cstack.c
#include <stdio.h>
void bar() {
int e = 31;
int f = 32;
printf("e = %d\n", e);
printf("f = %d\n", f);
}
void foo() {
int c = 21;
int d = 22;
printf("c = %d\n", c);
printf("d = %d\n", d);
}
int main() {
int a = 11;
int b = 12;
printf("a = %d\n", a);
printf("b = %d\n", b);
foo();
bar();
}
```


上面这段c程序算上main函数共有三个函数，每个函数中都有两个整型变量，C编译器自动为这些变量在栈内存上分配空间，我们无需考虑它什么时候被创建以及何时被销毁，我们只需在特定的作用域（其所在函数内部）使用它即可，而无需担心其内存地址不合法，因此这些被分配在栈内存上的变量也被称为“自动变量”。但是如果将其地址返回到函数的外部，那么函数外部的代码通过解引用而访问这些变量时便会出错，如下面示例：

```
// github.com/bigwhite/experiments/blob/master/go-escape-analysis/c/cstack_coredump.c
#include <stdio.h>
int *foo() {
int c = 11;
return &c;
}
int main() {
int *p = foo();
printf("the return value of foo = %d\n", *p);
}
```


如代码所示，在上面这个例子中，我们将foo函数内的自动变量c的地址通过函数返回值返回给foo函数的调用者（main）了，这样当我们在main函数中引用该地址输出该变量值的时候，我们就会收到异常，比如在ubuntu上运行上述程序，我们会得到如下结果（在macos上运行，gcc会给出相同的警告，但程序运行不会dump core）：

```
# gcc cstack_dumpcore.c
cstack_dumpcore.c: In function ‘foo’:
cstack_dumpcore.c:5:12: warning: function returns address of local variable [-Wreturn-local-addr]
return &c;
^~
# ./a.out
Segmentation fault (core dumped)
```


这样一来我们就需要一种内存对象，可以在全局（跨函数间）合法使用，这就是堆内存对象。但是和位于栈上的内存对象由程序自行创建销毁不同，堆内存对象需要通过专用API手工分配和释放，在C中对应的分配和释放方法就是malloc和free：

```
// github.com/bigwhite/experiments/blob/master/go-escape-analysis/c/cheap.c
#include <stdio.h>
#include <stdlib.h>
int *foo() {
int *c = malloc(sizeof(int));
*c = 12;
return c;
}
int main() {
int *p = foo();
printf("the return value of foo = %d\n", *p);
free(p);
}
```


在这个示例中我们使用malloc在foo函数中分配了一个堆内存对象，并将该对象返回给main函数，main函数使用完该对象后调用了free函数手工释放了该堆内存块。

显然和自动变量相比，堆内存对象的生命周期管理将会给开发人员带来很大的心智负担。为了降低这方面的心智负担，带有GC（垃圾回收）的编程语言出现了，比如Java、Go等。这些带有GC的编程语言会对位于堆上的对象进行自动管理。当某个对象不可达时（即没有其对象引用它时），它将会被回收并被重用。

但GC的出现虽然降低了开发人员在内存管理方面的心智负担，但GC不是免费的，它给程序带来的性能损耗是不可忽视的，尤其是当堆内存上有大量待扫描的堆内存对象时，将会给GC带来过大的压力，从而使得GC占用更多本应用于处理业务逻辑的计算和存储资源。于是人们开始想方法尽量减少在堆上的内存分配，可以在栈上分配的变量尽量留在栈上。

**逃逸分析（escape analysis）就是在程序编译阶段根据程序代码中的数据流，对代码中哪些变量需要在栈上分配，哪些变量需要在堆上分配进行静态分析的方法**。一个理想的逃逸分析算法自然是能将那些人们认为需要分配在栈上的变量尽可能保留在栈上，尽可能少的“逃逸”到堆上的算法。但这太过理想，各种语言都有自己的特殊情况，各种语言的逃逸算法的精确度实际都会受到这方面的影响。

### 2. Go语言的逃逸分析

[Go从诞生那天](https://www.imooc.com/read/87/article/2320)起，逃逸分析就始终伴随其左右。正如上面说到的逃逸分析的目标，Go编译器使用逃逸分析来决定哪些变量应该在goroutine的栈上分配，哪些变量应该在堆上分配。

截至目前，Go一共有两个版本的**逃逸分析实现**，分水岭在[Go 1.13版本](https://mp.weixin.qq.com/s/Txqvanb17LYQYgohNiUHig)。Go 1.13版本之前是Go逃逸分析的第一版实现，位于Go源码的src/cmd/compile/internal/gc/esc.go中（以go 1.12.7版本为例），代码规模2400多行；Go 1.13版本中加入了由[Matthew Dempsky](https://github.com/mdempsky)重写的[第二版逃逸分析](https://github.com/golang/go/issues/23109)，并默认开启，可以通过-gcflags=”-m -newescape=false”恢复到使用第一版逃逸分析。之所以重写，主要是考虑第一版代码的可读性和可维护性问题，新版代码主要位于Go项目源码的src/cmd/compile/internal/gc/escape.go中，它将逃逸分析代码从上一版的2400多行缩减为1600多行，并作了更为完整文档和注释。但注意的是**新版代码在算法精确性上并没有质的变化**。

但即便如此，经过了这么多年的“修修补补”，Dmitry Vyukov 2015年提出的那些[“Go Escape Analysis Flaws”](https://docs.google.com/document/d/1CxgUBPlx9iJzkz9JWkb6tIpTe5q32QDmz8l0BouG0Cw/preview#)多数已经fix了。Go项目中内置了对逃逸分析的详尽的测试代码（位于Go项目下的test/escape*.go文件中）。

在新版逃逸分析实现的注释中（$GOROOT/src/cmd/compile/internal/gc/escape.go），我们可以大致了解逃逸分析的实现原理。注释中的原理说明中提到了算法基于的两个不变性：

- 指向栈对象的指针不能存储在堆中（pointers to stack objects cannot be stored in the heap）；
- 指向栈对象的指针不能超过该栈对象的存活期（即指针不能在栈对象被销毁后依旧存活）（pointers to a stack object cannot outlive that object）。

源码注释中也给出Go逃逸分析的大致原理和过程。Go逃逸分析的输入是Go编译器解析了Go源文件后所获得的整个程序的抽象语法树（Abstract syntax tree，AST）：

源码解析后得到的代码AST的Node切片为xtop：

```
// $GOROOT/src/cmd/compile/internal/gc/go.go
var xtop []*Node
```


在Main函数中，xtop被传入逃逸分析的入口函数escapes：

```
// $GOROOT/src/cmd/compile/internal/gc/main.go
// Main parses flags and Go source files specified in the command-line
// arguments, type-checks the parsed Go package, compiles functions to machine
// code, and finally writes the compiled package definition to disk.
func Main(archInit func(*Arch)) {
... ...
// Phase 6: Escape analysis.
// Required for moving heap allocations onto stack,
// which in turn is required by the closure implementation,
// which stores the addresses of stack variables into the closure.
// If the closure does not escape, it needs to be on the stack
// or else the stack copier will not update it.
// Large values are also moved off stack in escape analysis;
// because large values may contain pointers, it must happen early.
timings.Start("fe", "escapes")
escapes(xtop)
... ...
}
```


下面是escapes函数的实现：

```
// $GOROOT/src/cmd/compile/internal/gc/esc.go
func escapes(all []*Node) {
visitBottomUp(all, escapeFuncs)
}
// $GOROOT/src/cmd/compile/internal/gc/scc.go
// 强连接node - 一个数据结构
func visitBottomUp(list []*Node, analyze func(list []*Node, recursive bool)) {
var v bottomUpVisitor
v.analyze = analyze
v.nodeID = make(map[*Node]uint32)
for _, n := range list {
if n.Op == ODCLFUNC && !n.Func.IsHiddenClosure() {
v.visit(n)
}
}
}
// $GOROOT/src/cmd/compile/internal/gc/escape.go
// escapeFuncs performs escape analysis on a minimal batch of
// functions.
func escapeFuncs(fns []*Node, recursive bool) {
for _, fn := range fns {
if fn.Op != ODCLFUNC {
Fatalf("unexpected node: %v", fn)
}
}
var e Escape
e.heapLoc.escapes = true
// Construct data-flow graph from syntax trees.
for _, fn := range fns {
e.initFunc(fn)
}
for _, fn := range fns {
e.walkFunc(fn)
}
e.curfn = nil
e.walkAll()
e.finish(fns)
}
```


根据注释，escapes的大致原理是(直译)：

- 首先，构建一个有向加权图，其中顶点(称为”location”，由gc.EscLocation表示)代表由语句和表达式分配的变量，而边(gc.EscEdge)代表变量之间的赋值(权重代表寻址/取地址次数)。
- 接下来，遍历(visitBottomUp)该有向加权图，在图中寻找可能违反上述两个不变量条件的赋值路径。 违反上述不变量的赋值路径。如果一个变量v的地址是储存在堆或其他可能会超过它的存活期的地方，那么v就会被标记为需要在堆上分配。
- 为了支持函数间的分析，算法还记录了从每个函数的参数到堆的数据流以及到其结果的数据流。算法将这些信息称为“参数标签(parameter tag)”。这些标签信息在静态调用时使用，以改善对函数参数的逃逸分析。

当然即便看到这，你可能依旧一头雾水，没关系，这里不是讲解逃逸分析原理，如果想了解原理，那就请认真阅读那2400多行代码。

注：有一点需要明确，那就是静态逃逸分析也无法确定的对象会被放置在堆上，后续精确的GC会处理这些对象，这样最大程度保证了代码的安全性。


### 3. Go逃逸分析的示例

Go工具链提供了查看逃逸分析过程的方法，我们可以通过在-gcflags中使用-m来让Go编译器输出逃逸分析的过程，下面是一些典型的示例。

#### 1) 简单原生类型变量的逃逸分析

我们来看一个原生整型变量的逃逸分析过程，下面是示例的代码：

```
// github.com/bigwhite/experiments/blob/master/go-escape-analysis/go/int.go
1 package main
2
3 import "testing"
4
5 func foo() {
6 a := 11
7 p := new(int)
8 *p = 12
9 println("addr of a is", &a)
10 println("addr that p point to is", p)
11 }
12
13 func bar() (*int, *int) {
14 m := 21
15 n := 22
16 println("addr of m is", &m)
17 println("addr of n is", &n)
18 return &m, &n
19 }
20
21 func main() {
22 println(int(testing.AllocsPerRun(1, foo)))
23 println(int(testing.AllocsPerRun(1, func() {
24 bar()
25 })))
26 }
```


我们通过-gcflags “-m -l”来执行逃逸分析，之所以传入-l是为了关闭inline，屏蔽掉inline对这个过程以及最终代码生成的影响：

```
// go 1.16版本 on MacOS
$go build -gcflags "-m -l" int.go
# command-line-arguments
./int.go:7:10: new(int) does not escape
./int.go:14:2: moved to heap: m
./int.go:15:2: moved to heap: n
./int.go:23:38: func literal does not escape
```


逃逸分析的结果与我们手工分析的一致：函数bar中的m、n逃逸到heap(对应上面输出的有moved to heap: xx字样的行)，这两个变量将在heap上被分配存储空间。而函数foo中的a以及指针p指向的内存块都在栈上分配（即便我们是调用的new创建的int对象，Go中new出来的对象可不一定分配在堆上，逃逸分析的输出日志中还专门提及new(int)没有逃逸）。我们执行一下该示例（执行时同样传入-l关闭inline）：

```
$go run -gcflags "-l" int.go
addr of a is 0xc000074860
addr that p point to is 0xc000074868
addr of a is 0xc000074860
addr that p point to is 0xc000074868
0
addr of m is 0xc0000160e0
addr of n is 0xc0000160e8
addr of m is 0xc0000160f0
addr of n is 0xc0000160f8
2
```


首先，我们看到未逃逸的a和p指向的内存块的地址区域在0xc000074860~0xc000074868；而逃逸的m和n被分配到了堆内存空间，从输出的结果来看在0xc0000160e0~0xc0000160e8。我们可以明显看到这是两块不同的内存地址空间；另外通过testing包的AllocsPerRun的输出，我们同样印证了函数bar中执行了两次堆内存分配动作。

我们再来看看这个代码对应的汇编代码：

```
$go tool compile -S int.go |grep new
0x002c 00044 (int.go:14) CALL runtime.newobject(SB)
0x004d 00077 (int.go:15) CALL runtime.newobject(SB)
rel 45+4 t=8 runtime.newobject+0
rel 78+4 t=8 runtime.newobject+0
```


我们看到在对应源码的14和15行，汇编调用了runtime.newobject在堆上执行了内存分配动作，这恰是逃逸的m和n声明的位置。从下面newobject代码的实现我们也能看到，它实际上在gc管理的内存上执行了malloc动作：

```
// $GOROOT/src/runtime/malloc.go
// implementation of new builtin
// compiler (both frontend and SSA backend) knows the signature
// of this function
func newobject(typ *_type) unsafe.Pointer {
return mallocgc(typ.size, typ, true)
}
```


#### 2) 切片变量自身和切片元素的逃逸分析

了解过[切片实现原理](https://www.imooc.com/read/87/article/2383)的gopher都知道，切片变量实质上是一个三元组：

```
//$GOROOT/src/runtime/slice.go
type slice struct {
array unsafe.Pointer
len int
cap int
}
```


其中这个三元组的第一个字段array指向的是切片底层真正存储元素的指针。这样当为一个切片变量分配内存时，便既要考虑切片本身(即上面的slice结构体)在哪里分配，也要考虑切片元素的存储在哪里分配。我们看下面示例：

```
// github.com/bigwhite/experiments/blob/master/go-escape-analysis/go/slice.go
1 package main
2
3 import (
4 "reflect"
5 "unsafe"
6 )
7
8 func noEscapeSliceWithDataInHeap() {
9 var sl []int
10 println("addr of local(noescape, data in heap) slice = ", &sl)
11 printSliceHeader(&sl)
12 sl = append(sl, 1)
13 println("append 1")
14 printSliceHeader(&sl)
15 println("append 2")
16 sl = append(sl, 2)
17 printSliceHeader(&sl)
18 println("append 3")
19 sl = append(sl, 3)
20 printSliceHeader(&sl)
21 println("append 4")
22 sl = append(sl, 4)
23 printSliceHeader(&sl)
24 }
25
26 func noEscapeSliceWithDataInStack() {
27 var sl = make([]int, 0,
```

28 println("addr of local(noescape, data in stack) slice = ", &sl)
29 printSliceHeader(&sl)
30 sl = append(sl, 1)
31 println("append 1")
32 printSliceHeader(&sl)
33 sl = append(sl, 2)
34 println("append 2")
35 printSliceHeader(&sl)
36 }
37
38 func escapeSlice() *[]int {
39 var sl = make([]int, 0,

40 println("addr of local(escape) slice = ", &sl)
41 printSliceHeader(&sl)
42 sl = append(sl, 1)
43 println("append 1")
44 printSliceHeader(&sl)
45 sl = append(sl, 2)
46 println("append 2")
47 printSliceHeader(&sl)
48 return &sl
49 }
50
51 func printSliceHeader(p *[]int) {
52 ph := (*reflect.SliceHeader)(unsafe.Pointer(p))
53 println("slice data =", unsafe.Pointer(ph.Data))
54 }
55
56 func main() {
57 noEscapeSliceWithDataInHeap()
58 noEscapeSliceWithDataInStack()
59 escapeSlice()
60 }


对上述示例运行逃逸分析：

```
$go build -gcflags "-m -l" slice.go
# command-line-arguments
./slice.go:51:23: p does not escape
./slice.go:27:15: make([]int, 0,
```

does not escape
./slice.go:39:6: moved to heap: sl
./slice.go:39:15: make([]int, 0,

escapes to heap


我们从输出的信息中看到：

- 位于39行的escapeSlice函数中的sl逃逸到堆上了；
- 位于39行的escapeSlice函数中的切片sl的元素也逃逸到堆上了；
- 位于27行的切片sl的元素没有逃逸。

由于很难看到三个函数中各个切片的元素是否逃逸，我们通过运行该示例来看一下：

```
$go run -gcflags " -l" slice.go
addr of local(noescape, data in heap) slice = 0xc00006af48
slice data = 0x0
append 1
slice data = 0xc0000160c0
append 2
slice data = 0xc0000160d0
append 3
slice data = 0xc0000140c0
append 4
slice data = 0xc0000140c0
addr of local(noescape, data in stack) slice = 0xc00006af48
slice data = 0xc00006af08
append 1
slice data = 0xc00006af08
append 2
slice data = 0xc00006af08
addr of local(escape) slice = 0xc00000c030
slice data = 0xc00001a100
append 1
slice data = 0xc00001a100
append 2
slice data = 0xc00001a100
```


注：我们利用reflect包的SliceHeader输出切片三元组中的代表底层数组地址的字段，这里是slice data。


我们看到：

- 第一个函数noEscapeWithDataInHeap声明了一个空slice，并在后面使用append向切片附加元素。从输出结果来看，slice自身是分配在栈上的，但是运行时在动态扩展切片时，选择了将其元素存储在heap上；
- 第二个函数noEscapeWithDataInStack直接初始化了一个包含8个元素存储空间的切片，切片自身没有逃逸，并且在附加(append)的元素个数小于等于8个的时候，元素直接使用了为其分配的栈空间；但如果附加的元素超过8个，那么运行时会在堆上分配一个更大的空间并将原栈上的8个元素复制过去，后续该切片的元素就都存储在了堆上。这也是
[为什么强烈建议在创建 slice 时带上预估的cap参数的原因](https://www.imooc.com/read/87/article/2383)，不仅减少了堆内存的频繁分配，在切片变量未逃逸的情况下，在cap容量之下，所有元素都分配在栈上，这将提升运行性能。 - 第三个函数escapeSlice则是切片变量自身以及其元素的存储都在堆上。

#### 3) fmt.Printf系列函数让变量逃逸到堆(heap)上了？

很多人在go项目的issue中反馈fmt.Printf系列函数让变量逃逸到堆上了，情况真的是这样么？我们通过下面示例来看一下：

```
// github.com/bigwhite/experiments/blob/master/go-escape-analysis/go/printf1.go
1 package main
2
3 import "fmt"
4
5 func foo() {
6 var a int = 66666666
7 var b int = 77
8 fmt.Printf("a = %d\n", a)
9 println("addr of a in foo =", &a)
10 println("addr of b in foo =", &b)
11 }
12
13 func main() {
14 foo()
15 }
```


注：println和print两个预定义函数并没有像fmt.Printf系列函数的“副作用”，不会影响变量的逃逸性。所以这里使用println来输出变量的实际分配内存地址。


对上面的代码运行逃逸分析：

```
$go build -gcflags "-m -l" printf1.go
# command-line-arguments
./printf1.go:8:12: ... argument does not escape
./printf1.go:8:13: a escapes to heap
```


我们看到逃逸分析输出第8行的变量“a escapes to heap”，不过这个“逃逸”有些奇怪，因为按照之前的经验，如果某个变量真实逃逸了，那么逃逸分析会在其声明的那行输出：“moved to heap: xx”字样。而上面这个输出既不是在变量声明的那一行，也没有输出“moved to heap: a”字样，变量a真的逃逸了么？我们运行一下上面示例，看看变量a的地址究竟是在堆上还是栈上：

```
$go run -gcflags "-l" printf1.go
a = 66666666
addr of a in foo = 0xc000092f50
addr of b in foo = 0xc000092f48
```


我们看到变量a的地址与未逃逸的变量b的地址都在同一个栈空间，变量a并未逃逸！如果你反编译为汇编，你肯定也看不到runtime.newobject的调用。

那么“./printf1.go:8:13: a escapes to heap”这句的含义究竟是什么呢？显然逃逸分析在这一行是对进入fmt.Printf的数据流的分析，我们修改一下go标准库源码，然后[build -a重新编译一下printf1.go](https://www.imooc.com/read/87/article/2387)，看看在fmt.Printf内部变量的分布情况：

```
// $GOROOT/src/fmt/print.go
func Printf(format string, a ...interface{}) (n int, err error) {
// 添加下面四行代码
for i := 0; i < len(a); i++ {
println(a[i])
println(&a[i])
}
return Fprintf(os.Stdout, format, a...)
}
```


重新编译printf1.go并运行编译后的可执行文件(为了避免)：

```
$go build -a -gcflags "-l" printf1.go
$./printf1
(0x10af200,0xc0000160c8)
0xc00006cf58
a = 66666666
addr of a in foo = 0xc00006cf50
addr of b in foo = 0xc00006cf48
```


我们看到fmt.Printf的实参a在传入后被装箱到一个interface{}类型的形参变量中，而这个形参变量自身则是被分配在栈上的（0xc00006cf58），而通过println输出的该interface{}类型形参变量的类型部分和值部分分别指向0x10af200和0xc0000160c8。显然值部分是在堆内存上分配的。那么“./printf1.go:8:13: a escapes to heap”是否指的是装箱后的值部分在堆上分配呢？这里也不确定。

我们再来看一个例子来对比一下：

```
// github.com/bigwhite/experiments/blob/master/go-escape-analysis/go/printf2.go
1 package main
2
3 import "fmt"
4
5 func foo() {
6 var a int = 66666666
7 var b int = 77
8 fmt.Printf("addr of a in bar = %p\n", &a)
9 println("addr of a in bar =", &a)
10 println("addr of b in bar =", &b)
11 }
12
13 func main() {
14 foo()
15 }
```


在printf2.go这个例子中，与printf1.go不同的是我们在foo函数中使用fmt.Printf输出的是变量a的地址：&a。我们运行一下新版逃逸分析：

```
// go 1.16
$go build -gcflags "-m -l" printf2.go
# command-line-arguments
./printf2.go:6:6: moved to heap: a
./printf2.go:8:12: ... argument does not escape
```


我们看到位于第6行声明的变量a居然真的逃逸到了堆上。我们运行一下printf2.go：

```
$go build -a -gcflags "-l" printf2.go
$./printf2
(0x10ab4a0,0xc0000160c8)
0xc00006cf58
addr of a in bar = 0xc0000160c8
addr of a in bar = 0xc0000160c8
addr of b in bar = 0xc00006cf48
```


我们看到变量a的地址果然与位于栈上的变量b相差很大，应该就是在堆上，那么这样看那些在go项目中提issue的gopher所言不虚。变量a的地址以实参的形式传入fmt.Printf后被装箱到一个interface{}形参变量中，而从结果来看，fmt.Printf真的要求装箱的形参变量的值部分要在堆上分配，但根据逃逸分析不变性，堆上的对象不能存储一个栈上的地址，而这次存储的是a的地址，于是将a判定为逃逸，于是a自身也就被分配到了堆上(0xc0000160c8)。

我们用go 1.12.7运行一下老版的逃逸分析：

```
// go 1.12.7
$go build -gcflags "-m -l" printf2.go
# command-line-arguments
./printf2.go:8:40: &a escapes to heap
./printf2.go:8:40: &a escapes to heap
./printf2.go:6:6: moved to heap: a
./printf2.go:8:12: foo ... argument does not escape
./printf2.go:9:32: foo &a does not escape
./printf2.go:10:32: foo &b does not escape
```


老版的逃逸分析给出了更详细的输出，比如：“&a escapes to heap”，其所指想必就是&a被装箱到堆内存上；而println输出&a则无需&a被装箱。但此后对变量a的最终判定为逃逸。

Go核心团队成员

[Keith Randall]对逃逸分析输出的日志给过一个[解释]，大致意思是：当逃逸分析输出“b escapes to heap”时，意思是指存储在b中的值逃逸到堆上了(当b为指针变量时才有意义），即任何被b引用的对象必须分配在堆上，而b自身则不需要；如果b自身也逃逸到堆上，那么逃逸分析会输出“&b escapes to heap”。

这个问题目前已经没有fix，其核心问题在[8618这个issue](https://github.com/golang/go/issues/8618)中。

### 5. 手动强制避免逃逸

对于printf2.go中的例子，我们确定一定以及肯定：a不需要逃逸。但若使用fmt.Printf，我们无法阻拦a的逃逸。那是否有一种方法可以干扰逃逸分析，使逃逸分析认为需要在堆上分配的内存对象而我们确定认为不需要逃逸的对象避免逃逸呢？在Go运行时代码中，我们发现了一个函数：

```
// $GOROOT/src/runtime/stubs.go
func noescape(p unsafe.Pointer) unsafe.Pointer {
x := uintptr(p)
return unsafe.Pointer(x ^ 0) // 任何数值与0的异或都是原数
}
```


并且在Go标准库和运行时实现中，该函数得到大量使用。该函数的实现逻辑使得我们传入的指针值与其返回的指针值是一样的。该函数只是通过uintptr做了一次转换，而这次转换将指针转换成了数值，这“切断”了逃逸分析的数据流跟踪，导致传入的指针避免逃逸。

我们看一下下面例子：

```
// github.com/bigwhite/experiments/blob/master/go-escape-analysis/go/printf3.go
package main
import (
"fmt"
"unsafe"
)
func noescape(p unsafe.Pointer) unsafe.Pointer {
x := uintptr(p)
return unsafe.Pointer(x ^ 0)
}
func foo() {
var a int = 66666666
var b int = 77
fmt.Printf("addr of a in bar = %p\n", (*int)(noescape(unsafe.Pointer(&a))))
println("addr of a in bar =", &a)
println("addr of b in bar =", &b)
}
func main() {
foo()
}
```


对该代码实施统一分析：

```
$go build -gcflags "-m -l" printf3.go
# command-line-arguments
./printf3.go:8:15: p does not escape
./printf3.go:16:12: ... argument does not escape
```


我们看到a这次没有逃逸。运行一下编译后的可执行文件：

```
$./printf3
(0x10ab4c0,0xc00009af50)
0xc00009af58
addr of a in bar = 0xc00009af50
addr of a in bar = 0xc00009af50
addr of b in bar = 0xc00009af48
```


我们看到a没有像printf2.go那样被放在堆上，这次和b一样都是在栈上分配的。并且在fmt.Printf执行的过程中a的栈地址始终是有效的。

曾有一篇[通过逃逸分析优化性能的论文](http://www.wingtecher.com/themes/WingTecherResearch/assets/papers/ICSE20.pdf)《Escape from Escape Analysis of Golang》使用的就是上述noescape函数的思路，有兴趣的童鞋可以自行下载阅读。

### 6. 小结

通过这篇文章，我们了解到了逃逸分析要解决的问题、Go逃逸分析的现状与简单原理、一些Go逃逸分析的实例以及对逃逸分析输出日志的说明。最后，我们给出一个强制避开逃逸分析的方案，但要谨慎使用。

日常go开发过程，绝大多数情况无需考虑逃逸分析，除非性能敏感的领域。在这些领域，对系统执行热点路径做一次逃逸分析以及相应的优化，可能回带来程序性能的一定提升。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/blob/master/go-escape-analysis)下载：https://github.com/bigwhite/experiments/blob/master/go-escape-analysis

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

感谢。关于怎么区别哪些地址是stack or heap，好像没有提及

文中提到：“go堆内存所使用的内存页(page)与goroutine的栈所使用的内存页是交织在一起的https://github.com/golang/go/issues/30554#issuecomment-469141498” — go中仅通过一个地址值很难区分究竟是在堆上还是栈上。

大佬在前文中有一段通过C语言证明栈空间不可被访问那里是否有错误呢？我通过同样的方式使用gcc进行编译，然后通过ida静态分析查看了一下汇编代码，发现，并不是因为栈不可被访问，而是因为编译器认为这是一个非法访问，而将返回值 mov rax, 0,使系统产生一个短错误。然后我使用 gdb 去动态调试了程序，并将 mov rax, 0 更改为 mov rax, $var_c_ptr,最后的结果是栈空间的数据在函数结束后是可以被再次访问的，然后我咨询了AI,AI给我的回答为除非操作系统强制介入，将物理页释放，否则存储在栈上的内容依然是可访问的，只是不可见。