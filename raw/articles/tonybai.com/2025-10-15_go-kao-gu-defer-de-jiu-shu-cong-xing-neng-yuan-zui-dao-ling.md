---
title: Go 考古：defer 的“救赎”——从性能“原罪”到零成本的“开放编码”
url: https://tonybai.com/2025/10/15/go-archaeology-defer/
published: '2025-10-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 考古：defer 的“救赎”——从性能“原罪”到零成本的“开放编码”

![](../../assets/bb483651a6b20d8f.png)


[本文永久链接](https://tonybai.com/2025/10/15/go-archaeology-defer) – https://tonybai.com/2025/10/15/go-archaeology-defer

大家好，我是Tony Bai。

在 Go 语言的所有关键字中，defer 无疑是最具特色和争议的之一。它以一种近乎“魔法”的方式，保证了资源清理逻辑的执行，极大地提升了代码的可读性和健壮性。f, _ := os.Open(“…”); defer f.Close() 这一行代码，几乎是所有 Gopher 的**肌肉记忆**。

然而，在这份优雅的背后，曾几何时，defer 却背负着“性能杀手”的恶名。在 Go 的历史长河中，无数资深开发者，包括标准库的维护者们，都曾被迫在代码的可维护性与极致性能之间做出痛苦的抉择，含泪删掉 defer 语句，换上丑陋但高效的手动 if err != nil 清理逻辑。

![](../../assets/d6c5477628afbbec.png)


你是否好奇：

- defer 的早期实现究竟“慢”在哪里？为什么一个简单的函数调用会被放大数十倍的开销？
- 从 Go 1.13 到
[Go 1.14](https://tonybai.com/2020/03/08/some-changes-in-go-1-14)，Go 团队究竟施展了怎样的“魔法”，让 defer 的性能提升了超过 10 倍，几乎达到了与直接调用函数相媲美的程度？ - 为了实现这场“性能革命”，defer 在编译器和运行时层面，经历了怎样一场从“堆分配”到“栈上开放编码(open-coded defer)”的“心脏手术”？

今天，就让我们再一次化身“Go 语言考古学家”，在Go issues以及Go团队那些著名的演讲资料中挖掘，并结合 Go 官方的设计文档，深入 defer 性能演进的“地心”，去完整地再现这场波澜壮阔的“救赎之路”。

![](../../assets/e7aa987414f58103.png)


## “事后”的智慧：Defer 的设计哲学与独特性

在我们深入 defer 性能的“地心”之前，让我们先花点时间，站在一个更高的维度，欣赏一下 defer 这个语言构造本身的设计之美。defer机制 并非 Go 语言的首创，许多语言都有类似的机制来保证资源的确定性释放，但Go中defer 机制的实现方式却独树一帜，充满了 Go 语言独有的哲学。

### 保证“清理”的殊途同归

下面是几种主流语言的资源管理范式，这让我们能更清晰地看清 defer 的坐标：

**C++ 的 RAII (Resource Acquisition Is Initialization):**

这是一种极其强大和高效的范式。资源（如文件句柄、锁）的生命周期与一个栈上对象的生命周期绑定。当对象离开作用域时，其**析构函数 (destructor)** 会被**编译器**自动调用，从而释放资源。RAII 的优点是**静态可知、零运行时开销**。但它强依赖于 C++ 的析构函数和对象生命周期管理，对于一门拥有垃圾回收（GC）的语言来说，这种模式难以复制。

**Java/Python 的 try-finally:**

这是另一种常见的保证机制。finally 块中的代码，无论 try 块是正常结束还是抛出异常，都保证会被执行。try-finally 同样是**静态可知**的，编译器能明确地知道在每个代码块退出时需要执行什么。

这两种机制的共同点是：它们都是**块级 (block-level)** 的，并且清理逻辑的位置往往与资源获取的位置**相距甚远**。

### Defer 的三大独特优势

相比之下，Go 的 defer 提供了三种独特的优势，使其在代码的可读性和灵活性上脱颖而出：

**就近原则，极致清晰 (Clarity):**

这是 defer 最为人称道的优点。清理逻辑（defer f.Close()）可以紧跟在资源获取逻辑（os.Open(…)）之后。这种“开闭成对”的书写方式，极大地降低了程序员的心智负担，你再也不用在函数末尾的 finally 块和函数开头的资源申请之间来回跳转，从而有效避免了忘记释放资源的低级错误。

**函数级作用域，保证完整性 (Robustness):**

defer 的执行时机与函数（而非代码块）的退出绑定。这意味着，无论函数有多少个 return 语句，无论它们分布在多么复杂的 if-else 分支中，所有已注册的 defer 调用都保证会在函数返回前被执行。这对于重构和维护极其友好——你可以随意增删 return 路径，而无需担心破坏资源清理的逻辑。更重要的是，在 panic 发生时，defer 依然会被执行，这为构建健壮的、能从异常中恢复的常驻服务提供了坚实的基础。

**动态与条件执行，极致灵活 (Flexibility):**

这是 defer 与 RAII 和 try-finally 最本质的区别。defer 是一个**完全动态的语句**，它可以出现在 if 分支、甚至 for 循环中。

```
if useFile {
f, err := os.Open("...")
// ...
defer f.Close() // 只在文件被打开时，才注册清理逻辑
}
```


这种**条件式清理**的能力，是其他静态机制难以优雅表达的。

### “动态”的双刃剑

然而，defer 的**动态性**也是一把双刃剑。

正是因为它可以在循环中被调用，defer 在理论上可以被执行任意多次。编译器无法在编译期静态地知道一个函数到底会注册多少个 defer 调用。

**这种不确定性，迫使 Go 的早期设计者必须借助运行时的帮助**，通过一个动态的链表来管理 defer 调用栈。这就引出了我们即将要深入探讨的核心问题——为了这份极致的灵活性和清晰性，defer 在诞生之初，付出了怎样的**性能代价**？而 Go 团队又是如何通过一场载入史册的编译器革命，几乎将其“抹平”的？

现在，让我们带上“考古工具”，正式开始我们的性能探源之旅。

## “原罪”：Go 1.13 之前的 defer 为何如此之慢？

在GopherCon 2020上，Google工程师Dan Scales为大家进行了一次经常的[有关defer性能提升的演讲](https://www.youtube.com/watch?v=DHVeUsrKcbM)，在此次演讲中，他先为大家展示了一张令人震惊的性能对比图，也揭示了一个残酷的事实：在 Go 1.12 及更早的版本中，一次 defer 调用的开销高达 **44 纳秒**，而一次普通的函数调用仅需 **1.7 纳秒**，相差超过 **25 倍**！

这巨大的开销从何而来？答案隐藏在早期的实现机制中：**一切 defer 都需要运行时（runtime）的深度参与，并且都涉及堆分配（heap allocation）。**

让我们通过 Go 团队的内部视角，来还原一下当时 defer 的工作流程：

**创建 _defer 记录：**每当你的代码执行一个 defer 语句时，编译器会生成代码，在**堆上**分配一个 _defer 结构体。这个结构体就像一张“任务卡”，记录了要调用的函数指针、所有参数的拷贝，以及一个指向下一个 _defer 记录的指针。

![](../../assets/6bd17b0341c1d839.png)


**deferproc 运行时调用：**创建好“任务卡”后，程序会调用运行时的 runtime.deferproc 函数。这个函数负责将这张新的“任务卡”挂载到当前 goroutine 的一个**链表**上。这个链表，我们称之为“defer 链”。

![](../../assets/52b1f693f39f5427.png)


**deferreturn 运行时调用：**当函数准备退出时（无论是正常 return 还是 panic），编译器会插入一个对 runtime.deferreturn 的调用。这个函数会像“工头”一样，从 defer 链的**尾部**开始（后进先出 LIFO），依次取出“任务卡”，并执行其中记录的函数调用。

看到了吗？每一次 defer，都至少包含：

- 一次
**堆内存分配**（创建 _defer 记录）。 - 两次到
**运行时的函数调用**(deferproc 和 deferreturn)。

堆分配本身就是昂贵的操作，因为它需要加锁并与垃圾回收器（GC）打交道。而频繁地在用户代码和 runtime 之间切换，也带来了额外的开销。正是这“三座大山”，让 defer 在高性能场景下变得不堪重负。

[Go 1.13 迈出了优化的第一步](https://github.com/golang/go/issues/6980)：对于**不在循环中**的 defer，编译器尝试将 _defer 记录分配在**栈上**。这避免了堆分配和 GC 的压力，使得 defer 的开销从 44ns 降低到了 32ns。这是一个显著的进步，但离“零成本”的目标还相去甚甚远。defer 依然需要与 runtime 交互，依然需要构建那个链表。

## “革命”：Go 1.14 的 Open-Coded Defer

Go 1.14 带来的，不是改良，而是一场彻底的**革命**。Dan Scales 和他的同事们提出并实现了一个全新的机制，名为 “[开放编码的 defer (Open-Coded Defer)](https://go.googlesource.com/proposal/+/master/design/34481-opencoded-defers.md)”。

![](../../assets/f3bf72f4057ec8a2.png)


其核心思想是：**对于那些简单的、非循环内的 defer，我们能不能彻底摆脱 runtime，让编译器直接在函数内生成所有清理逻辑？**

答案是肯定的。这场“革命”分为两大战役：

### 战役一：在函数退出点直接生成代码

编译器不再生成对 deferproc 的调用。取而代之的是：

**栈上“专属”空间：**在函数的栈帧（stack frame）中，为每个 defer 调用的函数指针和参数预留“专属”的存储位置。**位掩码（Bitmask）：**同样在栈上，引入一个 _deferBits 字节。它的每一个 bit 位对应一个 defer 语句。当一个 defer 被执行时，不再是创建 _defer 记录，而是简单地将 _deferBits 中对应的 bit 位置为 1。这是一个极快、极轻量的操作。

当函数准备退出时，编译器也不再调用 deferreturn。它会在**每一个** return 语句前，插入一段“开放编码”的清理逻辑。这段逻辑就像一个智能的“清理机器人”，它会**逆序**检查 _deferBits 的每一位。如果 bit 位为 1，就从栈上的“专属空间”中取出函数指针和参数，直接发起调用：

![](../../assets/b0c4ea5dee08105c.png)


看到了吗？在正常执行路径下，整个过程**没有任何堆分配，没有任何 runtime 调用**！defer 的成本，被降低到了几次内存写入（保存参数和设置 bit 位）和几次 if 判断。这使得其开销从 Go 1.13 的 32ns 骤降到了惊人的 **3ns**，与直接调用函数（1.7ns）的开销几乎在同一个数量级！

### 战役二：与 panic 流程的“深度整合”

你可能会问：既然没有 _defer 链表了，当 panic 发生时，runtime 怎么知道要执行哪些 defer 呢？

这正是 Open-Coded Defer 设计中最精妙、也最复杂的部分。Go 团队通过一种名为 funcdata 的机制，在编译后的二进制文件中，为每个使用了 Open-Coded Defer 的函数，都附上了一份“藏宝图”。

![](https://tonybai.com/wp-content/uploads/2025/go-archaeology-defer-7.png)


这份“藏宝图”告诉 runtime：

- 这个函数使用了开放编码。
- _deferBits 存储在栈帧的哪个偏移量上。
- 每个 defer 调用的函数指针和参数，分别存储在栈帧的哪些偏移量上。

当 panic 发生时，runtime 的 gopanic 函数会扫描 goroutine 的栈。当它发现一个带有 Open-Coded Defer 的栈帧时，它就会：

- 读取这份“藏宝图” (funcdata)。
- 根据“藏宝图”的指引，在栈帧中找到 _deferBits。
- 根据 _deferBits 的值，再从栈帧中找到并执行所有已激活的 defer 调用。

这个设计，巧妙地将 defer 的信息编码在了栈帧和二进制文件中，使得 panic 流程依然能够正确地、逆序地执行所有 defer，同时保证了正常执行路径的极致性能。

下面是Dan Scales给出的一个defer性能对比结果：

![](../../assets/07be8c9842928b1f.png)


我们看到：采用Open-coded defer进行优化后，defer的开销非常接近与普通的函数调用了(1.x倍)。

## 小结：“救赎”的完成与新的约定

defer 的性能“救赎之路”，从 Go 1.12 的 44ns，到 Go 1.13 的 32ns（栈分配 _defer 记录），再到 Go 1.14 的 3ns（Open-Coded Defer），其演进历程波澜壮阔，是 Go 团队追求极致性能与工程实用性的最佳例证。

下面是汇总后的各个Go版本的defer实现机制与开销数据：

![](../../assets/07c3cf3d109b7033.png)


这场“革命”之后，Dan Scales 在演讲的最后发出了强有力的呼吁，这也应该成为我们所有 Gopher 的新共识：

“

defers should now be used whenever it makes sense to make code clearer and more maintainable. defer should definitely not be avoided for performance reasons.”

（现在，只要能让代码更清晰、更易于维护，就应该使用 defer。绝对不应该再因为性能原因而避免使用 defer。）

defer 的“原罪”已被救赎。从现在开始，请放心地使用它，去编写更优雅、更健壮的 Go 代码吧。

## 参考资料

- Proposal: Low-cost defers through inline code, and extra funcdata to manage the panic case – https://go.googlesource.com/proposal/+/master/design/34481-opencoded-defers.md
- GopherCon 2020: Implementing Faster Defers by Dan Scales – https://www.youtube.com/watch?v=DHVeUsrKcbM
- cmd/compile: allocate some defers in stack frames – https://github.com/golang/go/issues/6980

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


**想系统学习Go，构建扎实的知识体系？**

我的新书《[Go语言第一课](https://book.douban.com/subject/37499496/)》是你的首选。源自2.4万人好评的极客时间专栏，内容全面升级，同步至Go 1.24。首发期有专属五折优惠，不到40元即可入手，扫码即可拥有这本300页的Go语言入门宝典，即刻开启你的Go语言高效学习之旅！

![](../../assets/d3fd3ab3e1fd7a7e.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论