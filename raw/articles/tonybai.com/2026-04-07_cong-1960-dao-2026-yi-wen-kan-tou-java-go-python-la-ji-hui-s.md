---
title: 从 1960 到 2026：一文看透 Java、Go、Python 垃圾回收器的原理与演进
url: https://tonybai.com/2026/04/07/garbage-collectors-deep-dive/
published: '2026-04-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 从 1960 到 2026：一文看透 Java、Go、Python 垃圾回收器的原理与演进

![](../../assets/0ff18ef053f5521c.png)


[本文永久链接](https://tonybai.com/2026/04/07/garbage-collectors-deep-dive) – https://tonybai.com/2026/04/07/garbage-collectors-deep-dive

大家好，我是Tony Bai。

为什么 Java 的 G1GC 需要设置停顿目标？Go 的混合写屏障是如何消除栈重扫的？Python 又是如何解决引用计数无法处理的循环引用？

垃圾回收（GC）不仅是语言运行时的核心，更是理解高性能系统绕不开的坎。

本文翻译自Shubham Raizada的文章《[Garbage Collection: From First Principles to Modern Collectors in Java, Go and Python](https://shbhmrzd.github.io/systems/garbage-collection/memory-management/2026/04/01/garbage-collectors-deep-dive.html)》。

此文通过对历史经典论文的溯源和对现代主流语言底层实现的拆解，构建了一套完整的 GC 知识体系。

文章涵盖了从基础的标记-清除、复制与整理算法，到复杂的三色标记抽象、写屏障机制以及有色指针技术。

无论你是想调优 JVM 性能，还是试图理解 Go 并发垃圾收集的吞吐成本，这篇文章都将为你提供从理论支撑到代码实现的全景视角。

![](../../assets/4b42c4fbe335e1ec.png)


以下是译文全文：

在过去的几年里，我的技术栈经历了从 Java 到 Go，再到 Rust，现在又回到了 Java 的过程。

在这些语言之间切换时，一直绕不开的一个话题就是垃圾回收（Garbage Collection, GC）。Java 和 Go 有 GC，而 Rust 没有。

在基准测试、延迟讨论以及“为什么这个服务变慢了”的对话中，GC 总会出现在某个角落。我经常听到关于 GC pauses（GC 停顿）、throughput overhead（吞吐量开销）和 write barriers（写屏障）的讨论，但我并不完全理解底层发生了什么。

在追溯起源时，我读到了 McCarthy 1960 年的论文，这篇论文因引入 Lisp 而闻名，但它也是首次描述 mark-and-sweep（标记-清除）的地方。

这又引导我阅读了 Wilson 1992 年的综述《Uniprocessor Garbage Collection Techniques》，该文将随后的所有发展组织成了一个清晰的分类学。

阅读这两篇文献让我更容易理解现代垃圾收集器，因为 G1GC、ZGC、Go 的并发收集器以及 CPython 的混合方案全都是这些论文所描述思想的变体。我还用 Go 编写了一个简单的玩具级 GC，以便亲自观察其机制。

以下是我在这一过程中的笔记。

## 起源论文

这篇论文因引入 Lisp 而闻名，但垃圾回收器几乎是作为实现细节被埋藏在其中的。McCarthy 需要一种方法来管理符号表达式的内存。Lisp 程序操作的是嵌套的列表（lists of lists of lists），这种递归结构使得要求程序员手动释放内存变得不切实际。因此，他描述了一种自动执行此操作的机制。

该机制分为两个阶段。首先，从程序正在活跃使用的 root（根）变量开始，遍历它们引用的每一个对象，将每个对象标记为 reachable（可达）。其次，扫描所有内存。任何未被标记的对象都是垃圾。将它们重新添加回 free list（空闲列表）。

这就是 mark-and-sweep（标记-清除）。它能自然地处理 cycles（循环引用，因为不可达的循环永远不会被标记），不需要逐个对象的簿记工作，并让程序员可以完全忽略内存管理。

其代价是程序在收集器运行时必须完全停止。每一次分配、每一次计算，所有一切都会冻结，直到标记和清除完成。对于 McCarthy 在 1960 年编写的程序来说，这完全是合理的。

随着程序规模变大并进入对延迟敏感的环境（如处理每秒数千次请求的 Web 服务器），stop-the-world（全线停顿）成了一个难以接受的权衡。现代 GC 研究产生的大部分成果都是为了回答一个问题：如何在不停止世界的情况下进行垃圾内存回收？

### Wilson (1992): [Uniprocessor Garbage Collection Techniques](https://dl.acm.org/doi/10.5555/645648.664824)

到 1992 年，三十年的 GC 研究已经产生了许多想法，但缺乏统一的词汇。Wilson 的综述论文将这一切组织了起来。它不是一种新算法，而是一个分类学，为散落在几十年论文中的思想赋予了名称和结构。

Wilson 正式确立了所有后续算法构建其上的三种经典算法。

第一种是 **mark-and-sweep**（标记-清除），即 McCarthy 的原始算法。从 roots 开始，遍历对象图，标记你能触达的所有内容，然后扫过堆并释放任何未标记的内容。它自然处理循环引用，实现简单。缺点是经过足够多的分配和回收循环后，堆会变得 fragmented（碎片化）。存活对象最终散落在各处，中间夹杂着细小的空闲间隙，分配器(allocator)必须更费力地寻找空间。

第二种是 **copying**（复制算法），有时被称为 semi-space（半空间）。其想法是将堆分成两个相等的部分。你在其中一半进行分配，当它填满时，将所有存活对象拷贝到另一半，然后将第一半完全丢弃。碎片消失了，因为存活对象在拷贝过程中被紧密排列在一起。分配速度很快，因为你只需移动一个 bump pointer（碰撞指针）。代价是有一半的内存始终处于空闲状态，等待成为下一次拷贝的目标。

第三种是 **reference counting**（引用计数）。每个对象都记录有多少个指针指向它。当创建一个新引用时，计数增加；当移除一个引用时，计数减少。当计数归零时，对象立即被释放。没有追踪过程，没有停顿，销毁是确定性的。问题在于 cycles（循环引用）。如果两个对象相互指向，即使程序中没有任何其他部分可以触达它们，它们的计数也至少为 1。仅靠引用计数，它们永远不会被释放。

除了这三种算法，Wilson 还探讨了现代垃圾回收器赖以生存的两个观察结果。

第一个是 **generational hypothesis**（分代假说）：大多数对象死得早。在实践中，程序分配的临时对象（中间值、请求作用域的缓冲区、循环变量）往往很快变成垃圾，而只有一小部分对象会贯穿整个程序生命周期。如果你频繁回收年轻对象，偶尔回收老对象，你就能将大部分工作集中在堆中主要是垃圾的部分，这比每次都扫描所有内容的代价要小得多。

第二个是 **tricolor marking**（三色标记），这是一种用于增量和并发收集的抽象。你不再简单地将对象标记为已访问或未访问，而是使用三种颜色：white（白色，尚未见到）、grey（灰色，已见到但子节点尚未扫描）和 black（黑色，已完全处理）。收集器一次处理一个灰色对象。结束时，白色对象即为垃圾。这种抽象使得收集器和应用程序可以同时运行，而不会破坏彼此对堆的视图。Go 的并发 mark-and-sweep 和 ZGC 的并发标记都是这一思想的直接后裔。

本文“现代 GC”部分中的所有内容都可以映射回 Wilson 的分类。工程实现已经变得更加复杂，但底层结构依然如故。

## 两种基本方法

几乎所有的垃圾回收器要么是 reference counting（引用计数），要么是 tracing（追踪），或者是两者的某种结合。Wilson 的论文围绕这一划分进行组织，三十年后依然成立。

### Reference Counting (引用计数)

每个对象维护一个指向它的引用计数。当引用创建时，计数增加。当引用移除时，计数减少。当计数归零时，对象立即被释放。

![](../../assets/0bd2892fefad31ad.png)


这是 CPython 所使用的其主要机制。它很简单，并能提供确定性的销毁。当指向文件句柄的最后一个引用消失时，**del** 运行，文件当场关闭，而不是在以后的某个 GC cycle中。

有两个问题使得引用计数无法独立胜任。

**Cycles (循环引用)。** 如果对象 A 指向对象 B，且对象 B 指向 A，那么即使程序中没有任何其他部分能触达它们，两者的计数也至少为 1。两者都不会被释放。

![](../../assets/f2af24470eff757d.png)


这并非理论上的边缘案例。循环引用在链表数据结构、父子关系、观察者模式和缓存中自然出现。稍后在介绍 CPython 的 GC 时，我将讨论 Python 如何处理这个问题。

**Per-mutation overhead (每次修改的开销)。** 每次指针赋值都需要更新引用计数。在多线程程序中，这些必须是 atomic（原子）操作，成本昂贵得多。每当你将对象传递给函数、返回它或将其赋值给字段时，你都要支付这种代价。

### Tracing (追踪式，即 Mark-and-Sweep)

追踪式收集器不跟踪单个引用，而是从一组已知的存活引用（称为 root set，根集合）开始，遍历整个对象图。它能触达的每个对象都被标记为存活。其他所有对象都被释放。

Root set 是起点，因此什么算作 root（根）至关重要。不同语言的答案是相同的：root 是 runtime（运行时）无需追踪就能找到的任何引用。这些指针锚定在程序当前的执行状态中，是在任何遍历开始之前你就知道是存活的东西。

在实践中，roots 分为以下几类。

每个活跃 stack frame（栈帧）中的 **local variables**（局部变量）和函数参数都是 roots。程序正在活跃地运行这些函数，因此它们引用的任何内容定义上都是在使用中的。

**Global and static variables**（全局变量和静态变量）是 roots，因为它们在程序的整个生命周期内都存在。

**CPU registers**（CPU 寄存器）是 roots。因为当 JIT 编译器优化一个热点方法时，它可能会将频繁访问的对象引用保留在 CPU 寄存器中，而不是写回栈。如果 GC 此时运行，寄存器保存着该对象的唯一存活引用。如果 GC 不扫描寄存器，它就会释放一个仍在使用中的对象。为了防止这种情况，运行时在代码中定义了 safe points（安全点），GC 只能在这些点发生，并且在这些点，它会快照寄存器状态以寻找持有的任何引用。

**Runtime（运行时）本身**也持有与用户代码无关的 roots。在 JVM 中，class loaders 是 roots：你加载的每个类都由其类加载器引用，只要类加载器存活，它加载的每个类（包括它们的静态字段）就保持存活。Interned strings（常量池字符串）是 roots，因为 String.intern() 将字符串存储在 JVM 维护的共享池中。JNI handles 是 roots，因为当原生 C 或 C++ 代码通过 Java Native Interface 持有 Java 对象的引用时，该引用存在于 Java 堆外的句柄表中，GC 必须扫描它。每个活跃线程都是一个 root，其整个调用栈帧都是 root set 的一部分。

Go 的运行时遵循同样的原则。每个 goroutine 都有自己的栈，必须扫描所有 goroutine 栈以寻找 roots。运行时还跟踪自己的内部数据结构，例如 finalizer 队列，作为 root set 的一部分。

![](../../assets/0ff0538a077ab5db.png)


核心见解是：roots 是由运行时在无需追踪的情况下就已经知道是存活的东西定义的。其他所有东西必须通过从 root 可达来证明自己的生存权。这就是为什么这个概念是与语言无关的。Java、Go 和 Python 之间的具体 roots 集合有所不同，但原则是一样的：从你知道是存活的地方开始，向外追踪，并回收其余部分。

循环引用被自然处理。如果 A 和 B 相互指向，但都无法从任何 root 到达，则标记阶段永远不会访问它们。它们保持未标记状态并被清除。

代价：朴素的 mark-and-sweep 必须在追踪堆时暂停整个程序。这种 stop-the-world（全线停顿）是早期垃圾回收器的核心问题，也是现代 GC 几十年来工程化改进的重点。

### 为什么大多数现代 GC 都是追踪式的

在具有高分配速率的服务器工作负载中，引用计数的逐次修改成本会积少成多。每次指针写入都会增减计数。在多线程程序中，这些更新必须是原子的，而原子操作很昂贵。在数十个线程中每秒进行数千次分配时，这种开销变得可衡量。此外，循环引用问题无论如何都需要一个补充的追踪步骤。而且追踪式收集器可以做成并发的，在应用程序运行的同时运行，只有简短的停顿。

Java 和 Go 使用追踪式收集器。Python 是一个显著的例外，它以引用计数为基础，并在此之上增加了一层用于追踪循环引用的检测器。

## 追踪式的变体

Wilson 的论文描述了实现追踪的四种方式，每种方式都有不同的权衡。

### Mark-Sweep (标记-清除)

最简单的追踪式收集器。分为两个阶段：

**Mark (标记)：**从 roots 开始，遍历对象图并在每个可达对象上设置标记位。**Sweep (清除)：**遍历整个堆。任何没有标记位的对象都是垃圾。释放它并将内存添加回空闲列表。

![](../../assets/986abc09a5268c9d.png)


Mark-sweep 的主要问题是 fragmentation（碎片化）。经过足够的回收周期后，堆看起来就像瑞士奶酪：存活对象散布其间，中间有很小的空闲间隙。你总共可能有 100MB 空闲内存，但没有一个连续的块大到足以满足一次新分配。分配器必须维护一个 free list 并搜索合适的空间，随着堆变得碎片化，这会变慢。

### Copying (Semi-Space，复制算法/半空间)

堆被分成两个相等的一半：from-space（源空间）和 to-space（目标空间）。分配发生在 from-space，使用简单的 bump pointer（碰撞指针）。当 from-space 填满时，收集器将所有存活对象拷贝到 to-space，更新所有指针，然后交换两者的角色。旧的 from-space 被完全丢弃。

![](../../assets/3721f07299e19fa7.png)


分配速度极快，因为它只是一个指针移动。Compaction（压缩）自然发生。代价是任何时候只有一半的堆可用。

### Mark-Compact (标记-整理)

标记阶段与 mark-sweep 相同，但收集器不是简单地释放未标记的对象，而是将所有存活对象滑动到堆的一端。这消除了碎片，且没有复制算法 50% 的内存开销。

![](../../assets/f14f69d066e5506d.png)


缺点是整理需要对堆进行多次扫描：一次标记，一次计算新地址，一次更新所有指针，一次移动对象。

### The Generational Hypothesis (分代假说)

Wilson 论文中最具影响力的观察之一是弱分代假说：大多数对象死得早。

在典型的 Web 服务器中，每个请求都会创建临时对象（解析器、中间字符串、响应构建器），它们只存活几毫秒。配置对象、连接池和缓存则贯穿整个应用程序生命周期。

分代收集器利用这一点，将堆划分为 generations（代）。新对象进入 young generation（年轻代）。如果它们在几次回收中幸存下来，就会被提升到 old generation（老年代）。年轻代回收频繁且速度快，因为那里的大多数对象已经死了。老年代回收较少发生。

![](../../assets/b27a9b1814da5651.png)


**Eden** 是所有新对象出生的地方。每一个 new Object() 都去这里。它很快就会填满，因为大多数程序分配速率很高。

**S0 和 S1** 是两个较小的 survivor spaces（幸存者空间）。当 Eden 填满并运行 minor GC（次要回收）时，收集器将 Eden 中的每个存活对象拷贝到其中一个空间（比如 S0）。下一次回收时，来自 Eden 和 S0 的幸存者被拷贝到 S1。再下一次，回到 S0。它们在每个周期轮换。这是年轻代中的复制算法：没有碎片，没有空闲列表，只有两半空间轮流充当目标。代价是你需要两个幸存者空间，但它们保持得很小，因为到回收运行时，Eden 中的大多数对象都已经死了。

**Promotion to old generation (提升到老年代)。** 在对象在 S0 和 S1 之间反弹足够多次之后（JVM 中的默认阈值是 15 次），收集器认定它已赢得了一席之地，并将其提升到老年代。老年代回收频率低得多，并且使用更重的算法（标记-整理而非复制），因为那里的对象庞大且长寿。

关键的实现挑战是跟踪从老对象到新对象的引用。如果一个老对象指向一个年轻对象，即使没有年轻代 root 指向它，该年轻对象也绝不能被回收。这通过 write barrier（写屏障）解决，即在每次指针写入时注入的一小段代码，用于在 remembered set（记录集）中记录跨代引用。

## 用 Go 构建一个玩具级 Mark-and-Sweep GC

我写了一个极简的 mark-and-sweep 收集器来使这些概念具体化。它大约有 70 行代码，演示了完整循环：分配对象、构建对象图、从 roots 标记以及清除不可达对象。

```
package main
import "fmt"
// Object 代表一个在堆上分配的对象。
type Object struct {
name string
marked bool
children []*Object
}
// VM 是一个带有垃圾回收器的微型虚拟机。
type VM struct {
heap []*Object
roots []*Object // 模拟栈变量和全局变量
}
// NewObject 在 VM 的堆上分配一个对象。
func (vm *VM) NewObject(name string) *Object {
obj := &Object{name: name}
vm.heap = append(vm.heap, obj)
return obj
}
// mark 从每个 root 开始遍历并标记所有可达对象。
func (vm *VM) mark() {
for _, root := range vm.roots {
vm.markObject(root)
}
}
func (vm *VM) markObject(obj *Object) {
if obj == nil || obj.marked {
return
}
obj.marked = true
for _, child := range obj.children {
vm.markObject(child)
}
}
// sweep 释放未标记的对象并重置幸存者的标记。
func (vm *VM) sweep() {
alive := []*Object{}
for _, obj := range vm.heap {
if obj.marked {
obj.marked = false // 为下一个 GC 周期重置
alive = append(alive, obj)
} else {
fmt.Printf(" collected: %s\n", obj.name)
}
}
vm.heap = alive
}
// GC 运行一次完整的 mark-and-sweep 回收。
func (vm *VM) GC() {
fmt.Printf("gc: heap has %d objects\n", len(vm.heap))
vm.mark()
vm.sweep()
fmt.Printf("gc: %d objects remain\n\n", len(vm.heap))
}
func main() {
vm := &VM{}
a := vm.NewObject("A")
b := vm.NewObject("B")
c := vm.NewObject("C")
_ = vm.NewObject("D") // 已分配但从未链接到任何东西
// 构建图: A -> B -> C
a.children = append(a.children, b)
b.children = append(b.children, c)
// 只有 A 是 root
vm.roots = append(vm.roots, a)
fmt.Println("=== GC #1: D is unreachable ===")
vm.GC()
// 创建循环: C -> A, 然后移除所有 roots
c.children = append(c.children, a)
vm.roots = nil
fmt.Println("=== GC #2: A->B->C->A cycle, no roots ===")
vm.GC()
}
```


运行结果：

```
=== GC #1: D is unreachable ===
gc: heap has 4 objects
collected: D
gc: 3 objects remain
=== GC #2: A->B->C->A cycle, no roots ===
gc: heap has 3 objects
collected: A
collected: B
collected: C
gc: 0 objects remain
```


第一次回收：A、B 和 C 通过 root A 可达。D 没有任何 root 路径，因此被回收。

第二次回收：A、B 和 C 形成了一个循环（A->B->C->A），但没有 roots。标记阶段从未访问过它们中的任何一个。所有三个都被清除了。这正是击败引用计数的场景。循环中的每个对象都有非零的引用计数，但没有一个能从 root 到达。

**追踪式 GC 不关心循环。它们只关心从 roots 开始的可达性。**

有一点需要注意：markObject 函数使用了递归，这在深层对象图上会耗尽栈空间。真实的垃圾回收器使用显式的 worklist（工作列表）而不是调用栈。

## 现代 GC 实现

上面的玩具收集器为了整个标记和清除过程停止了世界。现代 GC 已经进化到在应用程序持续运行的同时并发完成大部分工作。

### Go: 三色并发标记-清除 (Tri-Color Concurrent Mark-and-Sweep)

Go 的垃圾回收器是非分代的、非整理的且并发的。它不按年龄区分对象，也不在内存中移动对象。其重点是保持低停顿时间。

收集器使用三色抽象（tri-color abstraction）进行并发标记。每个对象处于三种状态之一：

![](../../assets/4fb292b6d736ace5.png)


**White (白色)**: 尚未访问。标记结束时仍为白色的任何东西都是垃圾。**Grey (灰色)**: 已访问，但其子节点尚未全部扫描。遍历的前沿（frontier）。**Black (黑色)**: 已访问，所有子节点已扫描。确定存活。

收集器开始时将所有对象设为白色，然后将 roots 设为灰色，并处理灰色对象直到不再剩余。所有仍为白色的内容都被清除。

![](../../assets/89c5b6bfae8dca90.png)


```
开始: 所有对象为白色，roots 为灰色
步骤 1: 选取一个灰色对象，扫描其子节点
- 将子节点标为灰色
- 将扫描过的对象标为黑色
步骤 2: 重复直到没有灰色对象剩余
步骤 3: 所有白色对象都是垃圾
示例:
Roots: [A]
开始: A(grey) --> B(white) --> D(white)
A(grey) --> C(white)
扫描 A: A(black) --> B(grey) --> D(white)
A(black) --> C(grey)
扫描 B: A(black) --> B(black) --> D(grey)
A(black) --> C(grey)
扫描 C: A(black) --> B(black) --> D(grey)
A(black) --> C(black)
扫描 D: A(black) --> B(black) --> D(black)
A(black) --> C(black)
结果: 任何剩余的白色对象都是垃圾并被释放
```


难点在于应用程序在收集器遍历时持续运行并修改指针。这造成了一个需要仔细处理的正确性问题。

收集器认为黑色对象已完成。一旦对象变黑，收集器就不会再扫描它。它的所有子节点都已被访问并设为灰色。但是，如果应用程序在收集器仍在运行时，将一个指向白色对象的指针写入黑色对象，收集器就有麻烦了。黑色对象已经处理完了。该白色对象也无法从任何灰色对象触达。当标记阶段结束并清除运行时，该白色对象将被释放，即便有一个存活的黑色对象指向它。

这被称为 **tricolor invariant**（三色不变性）：黑色对象绝不能直接指向白色对象。如果发生了这种情况，白色对象对收集器是不可见的，会被错误释放。write barrier（写屏障）的存在专门用于在并发标记期间应用程序修改对象图时维护这一不变性。

Go 通过 **hybrid write barrier**（混合写屏障，Go 1.8 引入）解决了这个问题。要理解它为什么有效，看看它结合的两种旧屏障会有所帮助。

**Dijkstra’s 插入屏障 (1978)**：每当一个指针被写入对象时，将新的被引用者设为灰色。如果一个黑色对象存储了对白色对象的引用，该白色对象会在收集器错过它之前变灰。这维护了三色不变性。

问题在于 goroutine 栈与堆对象不同。编译器在堆指针写入处注入写屏障，例如写入结构体字段或切片元素。栈写入是局部变量赋值，编译器对其分别处理。在每一个局部变量赋值上放屏障会使函数调用和基本操作变得极其昂贵，所以屏障不覆盖它们。这意味着在并发标记期间，goroutine 可以自由地将指向白色对象的指针写入局部变量，而没有屏障触发。收集器不知道发生了这事。

为了修复这一点，在并发标记结束时，Go 曾经必须停止世界并从头重新扫描每个 goroutine 的整个栈。重新扫描时发现的任何指向白色对象的指针都会变灰，防止它们被错误释放。此步骤的停顿时间随着 goroutine 数量和其栈大小而增加。拥有成千上万个 goroutine 的程序可能会看到数毫秒的 STW 停顿，仅仅是为了这次重新扫描。这是 Go 1.8 之前主要的 STW 停顿来源。

**Yuasa’s 删除屏障 (1990)** 采取相反的方法：每当一个指针即将被覆盖时，在旧引用消失前将其变灰。这确保了在标记开始时可达的任何东西直到结束都保持可达，即便应用程序在标记期间丢弃了它的引用。缺点是标记期间死亡的一些对象会存活到下一个周期（floating garbage，浮动垃圾），因为屏障保守地让它们活着。

**Go 的混合屏障**结合了两者。在堆写入时，它同时应用两种屏障：将旧引用变灰（Yuasa）并将新引用变灰（Dijkstra）。在栈写入时，不运行屏障，但栈上新分配的对象开始时就是黑色而不是白色。这种组合赋予了收集器足够强的不变性，使其在标记结束时永远不需要重新扫描栈。STW 停顿从几十毫秒降到了不到一毫秒。

```
// 混合屏障在堆指针写入时的逻辑:
// *slot = new_ptr
shade(*slot) // 将旧引用变灰 (Yuasa: 不要丢掉之前在那里的内容)
shade(new_ptr) // 将新引用变灰 (Dijkstra: 不要错过新到来的内容)
*slot = new_ptr
```


这就是并发垃圾回收的吞吐量成本：标记阶段的每一次堆指针写入都要运行此 shade 逻辑。单次操作开销虽小，但在高分配速率下会累积。权衡的结果是你获得了亚毫秒级的 STW 停顿，而不是几十毫秒。

Go 仅简短地停止世界以扫描 goroutine 栈并切换写屏障的开关。实际的标记和清除与应用程序并发进行。

**No compaction (无整理)。** Go 在分配后不移动对象。相反，Go 使用 tcmalloc 风格的分配器，将内存划分为 size classes（大小类），并从每个处理器的缓存（per-processor caches）中分配。对象被分组为固定的大小类（8 字节、16 字节、32 字节，最高达 32 KB）。分配时从空闲列表中选取合适大小的槽。这减少了碎片而无需移动对象，但并不能完全消除碎片。

**No generational collection (无分代收集)。** Go 团队的理由是，考虑到 Go 典型的带有 goroutine 和并发工作负载的分配模式，分代 GC 增加的复杂性（用于跟踪老到新指针的写屏障、提升逻辑、分代大小调优）带来的收益是不确定的。Go 通过使其并发标记器足够快来补偿，从而使额外的回收频率变得可以接受。

**关键里程碑：**

- Go 1.5 (2015)：引入并发 GC。在此之前，Go 使用全停顿收集器，停顿时间达 10-100ms 或更多。此版本使 Go 能够胜任延迟敏感型服务。
- Go 1.8 (2017)：混合写屏障。降低了在并发标记期间维护三色不变性的开销。
- Go 1.19 (2022)：GOMEMLIMIT。使 Go 程序能在容器环境的内存预算内工作。

**GOGC 调节旋钮。** Go 提供了一个主要的调优参数：GOGC。它控制在下一次 GC 触发之前堆可以增长多少。默认值是 100，意味着当堆自上次回收以来翻倍时触发 GC。

![](../../assets/25d8ca5906420d9f.png)


```
GOGC=100 (默认):
GC 后，存活堆 = 500MB
下次 GC 触发点: 500MB * (1 + 100/100) = 1000MB
GOGC=50 (更激进):
GC 后，存活堆 = 500MB
下次 GC 触发点: 500MB * (1 + 50/100) = 750MB
GOGC=200 (较保守):
GC 后，存活堆 = 500MB
下次 GC 触发点: 500MB * (1 + 200/100) = 1500MB
```


更低的 GOGC 意味着更频繁的回收（更低的内存占用，更高的 CPU 开销）。更高的 GOGC 意味着较少的回收（更高的内存占用，更低的 CPU 开销）。

Go 1.19 增加了 GOMEMLIMIT，这是一个软内存限制。在具有硬性内存预算的容器环境中，GOMEMLIMIT 告诉 GC pacer（步调算法）在内存使用接近限制时变得更加激进。

**亲自尝试：**

```
package main
import (
"fmt"
"runtime"
"time"
)
var longLived []*[1024 * 1024]byte
func main() {
fmt.Println("Go version:", runtime.Version())
for round := 0; round < 50; round++ {
// 短寿对象: 分配小对象，让它们死亡
for i := 0; i < 5000; i++ {
_ = make([]byte, 1024)
}
// 长寿对象: 每 10 轮保留一个
if round%10 == 0 {
arr := new([1024 * 1024]byte)
longLived = append(longLived, arr)
}
time.Sleep(50 * time.Millisecond)
}
var stats runtime.MemStats
runtime.ReadMemStats(&stats)
fmt.Printf("Total GC cycles: %d\n", stats.NumGC)
fmt.Printf("Total STW pause: %v\n", time.Duration(stats.PauseTotalNs))
fmt.Printf("Long-lived objects: %d\n", len(longLived))
}
```


运行并开启 GC 追踪：

```
GODEBUG=gctrace=1 go run gcdemo.go
```


观察输出内容：

```
gc 1 @0.011s 1%: 0.044+0.56+0.13 ms clock, 0.62+0.21/0.57/0+1.8 ms cpu, 3->4->0 MB, 4 MB goal, 0 MB stacks, 0 MB globals, 14 P
```


从左到右阅读：

- gc 1: GC 周期编号
- @0.011s: 自程序启动的时间
- 1%: 到目前为止 GC 消耗的 CPU 百分比
-
0.044+0.56+0.13 ms clock: GC 周期的三个阶段：STW 标记开始 (0.044ms) + 并发标记和扫描 (0.56ms) + STW 标记结束 (0.13ms)。STW 停顿是 clock 字段中的第一个和第三个数字。在此例中，应用程序被冻结的总墙钟时间是 0.044 + 0.13 = 0.174ms。中间的 0.56ms 是并发的：你的应用程序一直在运行。在 Go 中，STW 停顿通常在 1ms 以下，往往远低于 0.1ms。

-
0.62+0.21/0.57/0+1.8 ms cpu: CPU 时间细目。格式为：STW-开始 + 辅助/背景/空闲 + STW-结束。每个数字代表：

- 0.62ms — STW 标记开始时所有核心的 CPU 总时间。高于墙钟时间 (0.044ms)，因为 Go 会在多个核心上并行化初始栈扫描。
- 0.21ms — 应用程序 goroutine 执行 mutator assists（赋值器辅助）所花费的 CPU 时间。当某个 goroutine 分配速度超过 GC 处理速度时，它会被“征税”，必须在允许其分配之前自己做一些标记工作。
- 0.57ms — 专用背景 GC 工作 goroutine 执行并发标记所使用的 CPU 时间。
- 0 — 空闲 GC 工作者的 CPU 时间（仅在调度器没有其他任务运行时才领取 GC 任务的 goroutine）。此处为零意味着专用工作者处理了所有事情。
- 1.8ms — STW 标记结束时所有核心的 CPU 总时间。高于墙钟 (0.13ms)，因为多个核心并行工作以排空剩余任务并禁用写屏障。


![](../../assets/ab301a8163241aaa.png)


当多个核心并行工作时，CPU 时间可以超过墙钟时间。并发阶段的 CPU 时间可能少于墙钟时间，因为 GC 与你的应用程序共享核心。

- 3->4->0 MB: GC 开始时的堆大小、GC 触发点的堆大小、GC 完成后的存活堆大小
- 4 MB goal: 下次 GC 触发前的目标堆大小（基于 GOGC 和当前存活堆）
- 0 MB stacks: goroutine 栈使用的内存
- 0 MB globals: 标记期间扫描的全局变量使用的内存
- 14 P: 逻辑处理器数量 (GOMAXPROCS)

### Java: G1GC (Garbage First Collector)

G1GC 自 JDK 9 以来一直是 Java 的默认垃圾回收器。它是一个分代的、基于区域（region）的收集器。它进行追踪、标记和整理，但它是增量式进行的，而不是一次性完成。

**Region layout (区域布局)。** G1 将堆划分为大小相等的区域，通常每个区域为 1MB 到 32MB，取决于堆的大小。每个区域在任何时候扮演四种角色之一：Eden（伊甸园）、Survivor（幸存者）、Old（老年代）或 Humongous（巨型对象，用于超过半个区域大小的对象）。区域的角色可以在不同回收周期之间改变。

![](../../assets/a90139ee5ec0f58d.png)


**Young collection (次要 GC)。** Eden 区域填满。G1 停止世界，使用并行多线程标记器标记 Eden 和 Survivor 区域中的存活对象，将幸存者拷贝到新的 Survivor 区域或提升到 Old 区域，并完全丢弃旧的 Eden 区域。这是一个并行的 STW 停顿，但很短，因为年轻代区域较小且年轻对象大多已死。

**Mixed collection (混合回收)。** G1 周期性地运行并发标记周期，以找出哪些老年代区域包含的垃圾最多。然后运行混合回收：同时疏散（evacuating）年轻代区域和最具“盈利价值”的老年代区域。这就是“Garbage First”名称的由来。G1 总是优先选取垃圾密度最高的老年代区域，从而在单位停顿时间内实现最大的回收量。

**SATB (Snapshot-At-The-Beginning，起始快照)。** 在并发标记期间，应用程序持续运行并修改对象图。G1 使用 SATB 维护正确性。在标记开始时，G1 对哪些对象存活进行逻辑快照。该快照中存活的对象在此周期被视为存活，即使应用程序在标记期间丢弃了它们。写屏障将修改字段的旧值记录到 SATB 队列中。这种做法是保守的（一些垃圾会存活到下个周期），但是正确的。

```
并发标记正在运行。应用程序执行：
obj.field = null (原本指向 X)
没有 SATB: X 可能没有其他引用，未被标记，在使用中被释放。
有 SATB: 写屏障记录“此处曾有 X”，将 X 标为灰色。安全。
```


**Pause target (停顿目标)。** 你可以通过 -XX:MaxGCPauseMillis 配置 G1 的目标最大停顿时间。默认值是 200ms。G1 通过调整区域数量、回收集合大小和时机，尝试将停顿保持在目标范围内。它并不总是能成功，特别是在 Full GC 期间，但它是主要的调优旋钮。

**亲自尝试：**

```
import java.util.ArrayList;
import java.util.List;
public class GCDemo {
static List<byte[]> longLived = new ArrayList<>();
public static void main(String[] args) throws InterruptedException {
System.out.println("Starting GC demo...");
for (int round = 0; round < 50; round++) {
// 短寿对象：创建并立即丢弃
for (int i = 0; i < 1000; i++) {
byte[] tmp = new byte[10 * 1024]; // 每个 10KB
}
// 长寿对象：保留一些对象以构建老年代
if (round % 5 == 0) {
longLived.add(new byte[1024 * 1024]); // 1MB
}
Thread.sleep(50);
}
System.out.println("Done. Long-lived objects: " + longLived.size());
}
}
```


使用 G1GC 日志运行：

```
# 编译
javac GCDemo.java
# 使用 G1GC (Java 9+ 默认) 并开启 GC 日志
java -Xmx256m \
-XX:+UseG1GC \
"-Xlog:gc*:file=gc_g1.log:time,uptime,level,tags" \
GCDemo
# 或者，使用简洁的一行输出
java -Xmx256m -Xlog:gc GCDemo
```


观察日志：

```
[0.005s][info][gc] Using G1
[0.135s][info][gc] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 26M->3M(256M) 0.644ms
[0.812s][info][gc] GC(1) Pause Young (Normal) (G1 Evacuation Pause) 132M->7M(256M) 0.707ms
[1.710s][info][gc] GC(2) Pause Young (Normal) (G1 Evacuation Pause) 165M->13M(256M) 1.019ms
[2.528s][info][gc] GC(3) Pause Young (Normal) (G1 Evacuation Pause) 171M->19M(256M) 0.964ms
```


阅读日志：

- Using G1: 确认 G1GC 是活跃收集器
- Pause Young (Normal): 回收 Eden 和 Survivor 区域的次要 GC
- G1 Evacuation Pause: G1 正在将存活对象从回收区域拷贝（疏散）到新区域
- 26M->3M(256M) 0.644ms: 堆之前是 26MB，之后是 3MB，总堆容量 256MB，停顿耗时 0.644ms
- 在 2.5 秒的运行时中进行了四个 GC 周期，每个周期在 1.1ms 内完成。大多数分配的对象都是短寿的，并在年轻代被回收。

### Java: ZGC (Z Garbage Collector)

ZGC 自 Java 11 起可用，并在 Java 15 中达到生产就绪状态。扩展了分代收集的 Generational ZGC 在 Java 21 中引入。ZGC 的目标是无论堆大小如何（包括数百 GB 的堆），停顿时间均保持在亚毫秒级。

G1 在年轻代回收时停顿较短，但随着堆的增长，在并发标记设置和混合回收期间会有更长的停顿。ZGC 的方法不同：它几乎将所有工作（标记、重定位、引用处理）并发进行，将 STW 工作降至最低。

**Colored pointers (有色指针)。** ZGC 直接在指针位中编码 GC 元数据。在 64 位平台上，指针宽度为 64 位，但你实际上并不需要所有 64 位来寻址内存。2^42 就能给你 4TB 的可寻址空间，这超出了大多数应用程序的使用范围。这使得每个指针中留有超过 20 位空闲。ZGC 重新利用其中一些空闲位，直接在指针内部存储 GC 状态。

![](../../assets/ad1d250d8ebb1893.png)


每个元数据位都有特定用途：

-
**M0 和 M1 (标记位)：**用于跟踪对象是否已被标记为存活。ZGC 在每个 GC 周期中交替使用 M0 和 M1。在周期 1，收集器对每个可达对象设置 M0。在周期 2，它改用 M1。这样收集器就能区分“本周期标记”和“上个周期标记”，而无需在周期之间清除所有标记位。 -
**Remap (R，重映射)：**此位跟踪在对象重定位（relocated）后指针是否已更新。在并发重定位期间，ZGC 将对象移动到新地址，但并不立即更新堆中的每一个指针。相反，它保留旧指针，并使 remap 位处于未设置状态。当应用程序加载这些过时指针之一时，load barrier（读屏障/加载屏障）会注意到 remap 位未设置，并对其进行修正。 -
**Finalizable (F)：**表示该对象具有一个需要在释放前运行的 finalizer。

巧妙之处在于元数据随指针移动。GC 不需要一个单独的侧表来查找对象的 GC 状态。每个指针都已经携带了它。

**Load barriers (加载屏障)。** 每次应用程序从堆加载引用时，ZGC 都会插入一个加载屏障。屏障检查指针的颜色位，如果它们不处于预期状态，则采取行动。

以下是实际操作中的情况。假设收集器在并发重定位阶段将一个对象从地址 0×1000 移动到了 0×2000。应用程序仍然持有一个地址为 0×1000 且 remap 位未设置的指针。

```
应用程序代码:
Object x = obj.field;
实际执行的内容:
raw_ptr = load obj.field // raw_ptr = 0x1000, remap bit = 0
if (raw_ptr.color != expected) { // remap bit 为 0, expected 为 1 → 进入 slow path
new_addr = forwarding_table[0x1000] // 查找: 对象已移动到 0x2000
raw_ptr = set_address(raw_ptr, 0x2000)
raw_ptr = set_remap_bit(raw_ptr)
obj.field = raw_ptr // 就地修正指针，以便下次使用
}
x = raw_ptr // x 现在指向 0x2000
```


下次任何线程加载 obj.field 时，remap 位已经设置好了。屏障检查通过 fast path，没有额外工作。过时指针在第一次访问时被惰性修正。

这是关键机制。与其像 G1 在疏散期间那样让 GC 停止世界以一次性更新所有指向重定位对象的指针，ZGC 让应用程序在遇到指针时逐个修正。代价是每次指针加载都要支付屏障检查的开销，即便没有任何东西被重定位。在实践中，fast path（检查几位）执行代价足够小，与避免 STW 重定位停顿带来的收益相比，开销很小。

**Concurrent relocation (并发重定位)。** G1 停止世界以将存活对象从回收区域中疏散。ZGC 在应用程序运行的同时重定位对象。它能做到这一点是因为加载屏障处理了指针修正。在启动和结束每个阶段（标记开始、标记结束、重定位开始）时有简短的 STW 停顿，但这些通常远低于 1ms。拷贝对象和修正指针的实际工作是并发发生的。

**Generational ZGC (Java 21+)。** 最初的 ZGC 不按年龄划分堆。分代 ZGC 增加了年轻代和老年代，同时保留了亚毫秒级停顿的保证。它更频繁地回收年轻区域（垃圾最多的地方），较少回收老年代区域。加载屏障和有色指针机制被扩展以处理分代写屏障。

**何时使用 ZGC vs G1：**

![](../../assets/368f2e7dcd034fb5.png)


**亲自尝试：**

```
# 使用 ZGC 运行
java -Xmx256m \
-XX:+UseZGC \
"-Xlog:gc*:file=gc_zgc.log:time,uptime,level,tags" \
GCDemo
# 使用分代 ZGC (Java 21+)
java -Xmx256m \
-XX:+UseZGC -XX:+ZGenerational \
-Xlog:gc \
GCDemo
```


观察日志：

```
[0.318s] GC(0) Garbage Collection (Warmup) 28M(11%)->12M(5%)
[0.321s] GC(0) Pause Mark Start 0.023ms
[0.489s] GC(0) Concurrent Mark 168.123ms
[0.491s] GC(0) Pause Mark End 0.019ms
[0.492s] GC(0) Concurrent Select Relocation Set 1.234ms
[0.502s] GC(0) Concurrent Relocate 10.456ms
```


STW 停顿是标记为“Pause”的行。其他所有内容都是并发的。将此处的停顿持续时间与 G1 的输出进行对比。

### Python: 引用计数加循环 GC

CPython（Python 的参考实现）是“追踪式收集器占主导”模式的主要例外。它使用引用计数作为主要机制，并在之上增加了一层用于追踪循环引用的检测器。

**CPython 中的引用计数。**

每个 Python 对象都有一个 ob_refcnt 字段。Python 的 C API 在 Py_INCREF 时增加，在 Py_DECREF 时减少。当计数归零时，对象在 _Py_Dealloc 中被立即释放。这赋予了 Python 确定性的销毁：**del** 方法和上下文管理器的 **exit** 调用在最后一个引用掉落的那一刻发生。

```
import sys
x = []
print(sys.getrefcount(x)) # 2: 1个来自x，1个来自getrefcount参数本身的临时引用
y = x
print(sys.getrefcount(x)) # 3: 1个x, 1个y, 1个getrefcount参数
del y
print(sys.getrefcount(x)) # 2: 回到1个x, 1个getrefcount参数
```


**循环引用问题。** 仅靠引用计数无法回收循环垃圾。

```
import gc
# 创建循环引用
class Node:
def __init__(self, name):
self.name = name
self.ref = None
a = Node("A")
b = Node("B")
a.ref = b
b.ref = a # cycle: A -> B -> A
# a 和 b 的计数都 >= 1（由于相互引用）。
# 仅靠引用计数，两者都不会被释放。
del a
del b
# a 和 b 依然存活！Refcount: A 为 1 (来自 b.ref), B 为 1 (来自 a.ref)
# 显式触发循环检测器
collected = gc.collect()
print(f"Collected {collected} objects") # 收集了 4 个对象 (2个node + 2个dict)
```


引用计数处理了常见情况，但它无法收集循环引用。CPython 的答案是运行在引用计数系统之上的独立循环检测器。其实现在 Modules/gcmodule.c 中。

循环检测器是一个追踪式收集器，但它并不追踪整个堆。它仅跟踪能够参与循环引用的对象：如列表、字典、集合及用户自定义类实例等容器对象。字符串和整数无法持有对其他对象的引用，因此无需跟踪它们。

与 Java 的收集器一样，循环检测器使用分代方法。共有三代，编号为 0、1 和 2。思路与我们之前讨论的分代假说相同：大多数对象死得早，所以经常检查年轻对象，少打扰老对象。默认阈值硬编码在 CPython 的 [Modules/gcmodule.c](https://github.com/python/cpython/blob/v3.9.6/Modules/gcmodule.c#L137) 中：

```
struct gc_generation generations[NUM_GENERATIONS] = {
/* PyGC_Head, threshold, count */
{ {(uintptr_t)_GEN_HEAD(0), (uintptr_t)_GEN_HEAD(0)}, 700, 0},
{ {(uintptr_t)_GEN_HEAD(1), (uintptr_t)_GEN_HEAD(1)}, 10, 0},
{ {(uintptr_t)_GEN_HEAD(2), (uintptr_t)_GEN_HEAD(2)}, 10, 0},
};
```


你可以验证你的运行时实际使用的是什么：

```
python3 -c "import gc; print(gc.get_threshold())"
# (700, 10, 10)
```


请注意，某些框架和发行版会在启动时通过 gc.set_threshold() 覆盖这些默认值，因此你的环境可能显示不同的值。

第 0 代持有新分配的容器对象。当自上次回收以来的新分配数量超过阈值（默认 700）时，回收第 0 代。幸存的对象被提升到第 1 代。在第 0 代被回收 10 次后，第 1 代被回收一次。幸存者移至第 2 代。在第 1 代被回收 10 次后，第 2 代被回收一次。

效果是第 0 代大约每 700 次分配回收一次，第 1 代大约每 7,000 次，第 2 代大约每 70,000 次。进入第 2 代的长寿对象几乎永远不会被打扰。检测器将其大部分时间花在最年轻的对象上，这些对象最有可能最近变成了垃圾。

你可以看到这些计数：

```
import gc
# 当前各代阈值
print(gc.get_threshold()) # (700, 10, 10)
# 当前分配计数: (gen0分配, 自上次gen1回收以来的gen0回收数, 自上次gen2回收以来的gen1回收数)
print(gc.get_count()) # 例如 (342, 8, 2)
# 强制进行全量回收
gc.collect()
# 完全禁用循环检测器 (如果你确定代码中没有循环引用)
gc.disable()
```


当检测器在某一代码代上运行时，它需要找出哪些对象仅被循环引用保持存活。通过一个例子更容易理解算法。

假设检测器正在查看三个被跟踪的对象：X、Y 和 Z。X 指向 Y 和 Z。Y 指回 X。还有一个局部变量持有对 X 的引用。

![](../../assets/395dbc75b317a876.png)


步骤 1：拷贝引用计数。X=2, Y=1, Z=1。

步骤 2：减去内部引用。Y 指向 X，所以从 X 的副本中减 1 (X 从 2 变为 1)。X 指向 Y，所以从 Y 的副本中减 1 (Y 从 1 变为 0)。X 指向 Z，所以从 Z 的副本中减 1 (Z 从 1 变为 0)。

步骤 3：检查剩余部分。X 的调整后计数为 1。被跟踪集合之外的某些东西（局部变量）仍然指向它。X 存活。Y 和 Z 虽然调整后计数为 0，但它们可以从 X 到达，因此它们也幸存下来。

现在想象局部变量消失了。X 的引用计数掉到 1 (只有 Y 指向它)。运行相同算法：拷贝 X=1, Y=1, Z=1。减去内部引用：X 变为 0, Y 变为 0, Z 变为 0。每个调整后的计数都是零。被跟踪集合之外没有任何东西指向它们。它们仅因彼此而存在。三者都是垃圾。

这就是核心思想。算法寻找那些存在的唯一理由是同一集合中其他对象的目标。

有一个边缘案例困扰了多年：finalizers（终结器）。

终结器是运行时在对象被销毁前调用的方法，给予其清理外部资源（如文件句柄或网络连接）的机会。在 Python 中，这就是 **del** 方法。

假设 A 和 B 处于循环中，且两者都有 **del** 方法。检测器知道它们是垃圾，但要释放它们，它需要打破循环。问题是：哪个 **del** 先运行？如果你先运行 A 的终结器，而它尝试使用 B，但 B 已经正在被销毁，你就会崩溃。如果你先运行 B 的，而它使用 A，同样的问题。没有安全的顺序。

在 Python 3.4 之前，CPython 直接放弃处理这些对象。它将它们放入名为 gc.garbage 的列表中，且永远不释放它们。如果你的代码创建了带有 **del** 的循环引用，你就会有一个静默的内存泄漏。PEP 442 通过在打破任何引用之前调用终结器修复了这个问题。当 A 和 B 的 **del** 运行时，两者都保持完整。只有在所有终结器执行完毕后，检测器才会打破循环并释放对象。

关于 CPython 的内存模型还有一件事值得了解。每当 Python 执行类似 x = some_object 的操作时，它会增加 some_object 的引用计数（C 语言中的 Py_INCREF）。每当变量超出作用域时，它减少计数 (Py_DECREF)。在 C 中这些是普通的整数操作：refcount += 1, refcount -= 1。没有锁，没有原子指令。

在多线程程序中，这是一个问题。两个线程可能同时增加同一个对象的引用计数。如果没有同步，一个增加操作会丢失（经典的竞态条件），之后该对象可能会在有人仍在使用时被释放。

GIL (全局解释器锁) 防止了这种情况。一次只有一个线程执行 Python 字节码，因此两个线程永远不会同时修改同一个引用计数。GIL 免费使所有引用计数操作变得安全，而无需任何原子指令。

这也是移除 GIL 如此困难的原因。如果拿掉它，整个代码库中的每一个 Py_INCREF 和 Py_DECREF 都需要变成原子操作。原子操作比普通整数增量要昂贵得多。Python 3.13 开始附带实验性的 free-threaded 模式，它使用 biased reference counting（偏向引用计数）来降低这种成本：创建对象的线程可以对引用计数进行廉价的非原子更新，只有访问该对象的其他线程才支付原子操作的代价。

## 映射回 Wilson：全景图

每一种现代垃圾回收器都可以映射回 Wilson 在 1992 年描述的两个家族。它们之间的区别在于关于如何最小化停顿、处理并发以及高效管理内存的工程决策。

![](../../assets/b9c26289e89cbb30.png)


从这一对比中可以观察到几点：

**Wilson 的追踪式家族在服务器运行时占据主导地位。** 引用计数用于 Swift、Python 和 Rust 的 Arc，但对于具有高分配速率的托管运行时，追踪式收集器是标准做法。循环引用问题无论如何都需要补充追踪步骤，这增加了复杂性，且无法消除每次修改时的引用计数开销。

**分代收集除 Go 以外随处可见。** Java 重度利用了分代假说。Python 的循环检测器使用了三代。Go 最初选择不使用分代收集，因为跨代指针写屏障的开销对 Go 的典型工作负载来说不划算。这种情况可能正在改变：最近的 Go 版本中已经开发了实验性的分代支持。

**Compaction (整理) vs No compaction 是一个真正的设计分歧点。** Java 收集器进行整理，这允许 bump-pointer 分配（非常快）并消除碎片。Go 不整理，这意味着它永远不需要更新指向已移动对象的指针（更简单的写屏障，无需读屏障以保证正确性）。Go 通过大小类分配器（size-class allocator）来补偿。这是经典的 Wilson 权衡：拷贝和整理收集器以内存开销和指针更新成本换取分配速度和碎片消除。

**ZGC 的有色指针是 Wilson 指针标记 (pointer-tagging) 思想的现代实现。** Wilson 提到过在指针中使用位来存储 GC 元数据。ZGC 将此进一步发展，将标记状态、重映射状态和终结状态直接嵌入 64 位指针。在每次指针加载时检查这些位的加载屏障是 ZGC 为亚毫秒级停顿支付的代价。

**基本问题从未改变。** 从 roots 开始追踪，标记存活内容，回收其余部分。自 1960 年以来的所有发展都是对 McCarthy 原始洞察的工程改进。

## 参考资料

[McCarthy, J. (1960). Recursive functions of symbolic expressions and their computation by machine, Part I](https://dl.acm.org/doi/10.1145/367177.367199)[Wilson, P. R. (1992). Uniprocessor Garbage Collection Techniques. IWMM ‘92](https://www.cs.rice.edu/~javaplt/311/Readings/wilson92uniprocessor.pdf)[A Guide to the Go Garbage Collector](https://tip.golang.org/doc/gc-guide)[Getting to Go: The Journey of Go’s Garbage Collector](https://go.dev/blog/ismmkeynote)[Proposal: Eliminate STW stack re-scanning – Austin Clements (2016)](https://github.com/golang/proposal/blob/master/design/17503-eliminate-rescan.md)[Java Garbage Collection: The G1 Garbage Collector](https://www.oracle.com/technetwork/tutorials/tutorials-1876574.html)[ZGC: The Z Garbage Collector – JEP 333](https://openjdk.org/jeps/333)[Generational ZGC – JEP 439](https://openjdk.org/jeps/439)[PEP 442: Safe object finalization](https://peps.python.org/pep-0442/)

**你的“停顿”时刻**

GC 的艺术在于平衡。在你的开发生涯中，是否遇到过因为 GC 停顿导致的生产事故？你是倾向于 Go 的极致低延迟，还是 Java G1GC 的高吞吐？

欢迎在评论区分享你的调优经历或吐槽！

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


**原「Gopher部落」已重装升级为「Go & AI 精进营」知识星球，快来加入星球，开启你的技术跃迁之旅吧！**

我们致力于打造一个高品质的 **Go 语言深度学习** 与 **AI 应用探索** 平台。在这里，你将获得：

**体系化 Go 核心进阶内容:**深入「Go原理课」、「Go进阶课」、「Go避坑课」等独家深度专栏，夯实你的 Go 内功。**前沿 Go+AI 实战赋能:**紧跟时代步伐，学习「Go+AI应用实战」、「Agent开发实战课」、「Agentic软件工程课」、「Claude Code开发工作流实战课」、「OpenClaw实战分享」等，掌握 AI 时代新技能。**星主 Tony Bai 亲自答疑:**遇到难题？星主第一时间为你深度解析，扫清学习障碍。**高活跃 Gopher 交流圈:**与众多优秀 Gopher 分享心得、讨论技术，碰撞思想火花。**独家资源与内容首发:**技术文章、课程更新、精选资源，第一时间触达。

衷心希望「Go & AI 精进营」能成为你学习、进步、交流的港湾。让我们在此相聚，享受技术精进的快乐！欢迎你的加入！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论