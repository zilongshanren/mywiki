---
title: Unity DOTS 走马观花
url: http://frankorz.com/2019/05/07/simple-talk-unity-dots/
author: 文章作者 猫冬
published: '2019-05-07'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

![The Big Picture](../../assets/cf972cd7eb352a87.png)


简单介绍 Data-Oriented Technology Stack (DOTS, 数据导向型技术栈) ，其包含了 C# Job System、the Entity Component System (ECS) 和 Burst。

# 特点

DOTS 要实现的特点有：

- **性能的准确性。**我们希望的效果是：如果循环因为某些原因无法向量化，它应该会出现编译器错误，而不是使代码运行速度慢 8 倍，并得到正确结果，完全不报错。
**跨平台架构特性**。我们编写的输入代码无论是面向 iOS 系统还是 Xbox，都应该是相同的。- 我们应该
**有不错的迭代循环**。在修改代码时，可以轻松查看为所有架构生成的机器代码。机器代码“查看器”应该很好地说明或解释所有机器指令的行为。 **安全性**。大多数游戏开发者不把安全性放在很高的优先级，但我们认为，解决 Unity 出现内存损坏问题是关键特性之一。在运行代码时应该有一个特别模式，如果读取或写入到内存界限外或取消引用 Null 时，它能够提供我们明确的错误信息。

其中向量化指的是 Vectorization。

向量化的相关介绍：

[https://stackoverflow.com/questions/1422149/what-is-vectorization](https://stackoverflow.com/questions/1422149/what-is-vectorization)[https://www.wikiwand.com/en/Array_programming](https://www.wikiwand.com/en/Array_programming)

# Burst

Unity 构建了名为 Burst 的代码生成器和编译器。

当使用 C# 时，我们对整个流程有完整的控制，包括从源代码编译到机器代码生成，如果有我们不想要的部分，我们会找到并修复它。我们会逐渐把 C++ 语言的性能敏感代码移植为 HPC# （高性能 C#，下文会提到）代码，这样会更容易得到想要的性能，更难出现 Bug，更容易进行处理。

![](../../assets/e64c2d276db0b145.png)


如果 Asset Store 资源插件的开发者在资源中使用 HPC# 代码，资源插件在运行时代码会运行得更快。除此之外，高级用户也会通过使用 HPC# 编写出自定义高性能代码而受益。

Burst 对于 HPC# 更详细的支持可以在下面找到：

## 深入栈

向量化（Vectorization）无法进行的常见情况是，编译器无法确保二个指针不指向相同的内存，即混淆情况（Alias）。Alias 的问题在 Unity GDC 中也有一个演讲提到过：[Unity at GDC - C# to Machine Code](https://www.youtube.com/watch?v=NF6kcNS6U80)。

[Collections 类](https://docs.unity3d.com/Packages/com.unity.collections@0.0/manual/index.html)就是为了解决这个问题而诞生的，里面包含 NativeList

两个 NativeArray 之间从不会发生混淆这种情况，这也是为什么我们将会经常使用这些数据结构。我们可以在 Burst 中运用这个知识，使它不会由于害怕两个数组指针指向相同内存而放弃优化。

Unity 还编写了 [Unity.Mathemetics](https://github.com/Unity-Technologies/Unity.Mathematics) 数学库，提供了很多像 Shader 代码的数据结构。Burst 也能和这数学库很好的工作，未来 Burst 将能够为 `math.sin()`

等计算作出牺牲精度的优化。

对于 Burst 而言，`math.sin()`

不仅是要编译的 C# 方法，Burst 还能理解出 `sin()`

的三角函数属性，同时知道 x 值较小时会出现 `sin(x)`

等于 x 的情况，并了解它能替换为泰勒级数展开，以便牺牲特定精度。

**跨平台和架构的浮点准确性是 Burst 未来的目标。**

# 传统模式的问题

传统模式指的是什么呢？

- 跟 MonoBehaviours 打交道
- 数据和其处理过程耦合在一起
- 高度依赖引用类型

![](../../assets/6200be86d4cf8fc7.png)


## 问题一：数据分布在内存的各个角落

![](../../assets/e1c1febc70a3adad.jpg)


离散的数据导致搜索效率十分低下，还有 Cache Miss 的问题，这个问题可以参考下面的链接：

## 问题二：很多不必要的数据也被提供了

![](../../assets/e150d61c9e10ad7b.png)


例如当我们要调用 Transform 时，可能实际上我们只需要 position 和 rotation 两个属性来移动 gameObject，但是其他不需要的数据也被提供给了 gameObject。

## 问题三：低效的单线程数据处理

传统模式只使用单线程来按顺序一个一个地处理数据和操作，这样十分低效。

# 高性能 C＃（HPC#）

当我们使用 C# 语言时，仍然无法控制数据在内存中如何进行分布，但这是我们提升性能的关键点。

除此之外，标准库面向的是“堆上的对象”和“具有其它对象指针引用的对象”。

也就是意味着，当处理性能敏感代码时，我们可以放弃使用大部分标准库，例如：Linq、StringFormatter、List、Dictionary。禁止内存分配，即不使用类，只使用结构、映射、垃圾回收器和虚拟调用，并添加可使用的部分新容器，例如：NativeArray 和其他集合类型。

我们可以在越界访问时得到错误和错误信息，以及使用 C++ 代码时的调试器支持和编译速度。我们通常把该子集称为高性能 C# 或 HPC#。

它可以被总结为：

- 大部分的原始类型（float、int、uint、short、bool…），enums，structs 和其他类型的指针
- 集合：用
`NavtiveArray<T>`

代替`T[]`

- 所有的控制流语句（除了 try、finally、foreach、using）
- 对
`throw new XXXException(...)`

给予基础支持

# Job System

Job System 是针对上述传统模式问题的一种解决方式。例如下图可以把发射子弹看成一个 Job，从而用多线程来并行地处理发射操作。

![](../../assets/ace2744d573e82a7.jpg)


目前主流的 CPU 有 4-6 个物理核心，8-12 个逻辑核心，多线程处理将能够更好地发挥 CPU 的性能。

传统的多线程问题也有很多：

- 线程安全的代码十分难写
- 竞态条件，也就是计算结果依赖于两个或更多进程被调度的顺序
- 低效的上下文切换，切换线程的时候十分耗时

而 Job System 就是专注解决上面问题的一个方案，这样我们就能享受着多线程的好处来开发游戏。当然了，我们也要写出正确的 ECS 代码，熟悉新的开发模式。

## 解决的多线程问题

**C++ 和 C# 都无法为开发者编写线程安全代码提供太多帮助。**即使在今天，拥有多个核心游戏消费级硬件发展至今已经过去了十年，但依旧很难有效处理使用多个核心的程序。

数据冲突，不确定性和死锁是使多线程代码难以编写的挑战。Unity 想要的特性是“确保代码调用的函数和所有内容不会在全局状态下读取或写入”。Unity 希望应该让编译器抛出错误来提醒，而不是属于“程序员应遵守的准则”，Burst 则会提供编译器错误。

Unity 鼓励 Unity 用户编写 “Jobified” 代码：将「所有需要发生的数据转换」划分为 Job。

Job 会明确指定使用的只读缓冲区和读写缓冲区，尝试访问其它数据会得到编译器错误。Job 调度程序会确保在 Job 运行时，任何程序都不会写入只读缓冲区。Unity 也会确保在 Job 运行时，任何程序都不会读取读写缓冲区。

如果调度的 Job 违反了这些规则，我们会得到运行时错误（通常这种错误会在竞态条件出现时得到）。错误信息会说明，你正在尝试调度的 Job 想要读取缓冲区 A，但你之前已经调度了会写入缓冲区 A 的 Job ，所以如果想要执行该操作，需要把之前的 Job 指定为依赖。

# Entity Component System

Unity 一直以组件的概念为中心，例如：我们可以添加 Rigidbody 组件到游戏对象上，使对象能够向下掉落。我们也可以添加 Light 组件到游戏对象上，使它可以发射光线。我们添加 AudioEmitter 组件，可以使游戏对象发出声音。

我们实现组件系统的方法并没有很好地演变。过去我们**使用面向对象的思维编写组件系统**，导致组件和游戏对象都是“大量使用 C++ 代码”的对象，创建或销毁它们需要使用互斥锁修改“id 到对象指针”的全局列表。

通过使用面向数据的思维方式，我们可以更好地处理这种情况。我们可以保留用户眼中的优良特性，即**只需添加组件就可以实现功能，而同时通过新组件系统取得出色的性能和并行效果。**

这个全新的组件系统就是实体组件系统 ECS。简单来说，如今我们对游戏对象进行的操作可用于处理新系统的实体，组件仍称作组件。那么区别是什么？区别在于数据布局。

## ECS 数据布局

ECS 使用的数据布局会把这些情况看作一种非常常见的模式，并**优化内存布局**，使类似操作更加快捷。

### 组件（Component）

首先要明确的是这里的“组件”与上文提到的 Rigidbody “组件”是不一样的概念。ECS 中的组件只会存单纯的数据，不参与任何逻辑运算，逻辑运算会交由系统（System）来处理。

### 原型（Archetype）

**ECS 会在内存中对带有相同组件（Component）集的所有实体（Entity）进行组合**。ECS 把这类组件集称为原型（Archetype）。

下图的原型就是由 Position 组件、Velocity 组件、Rigidbody 组件和 Renderer 组件组成的。

如果一个实体只有三个组件（不同于前面提到的原型），那么那三个组件就组成了一个新的原型。

下面的图来自 Unite LA 的一次演讲的讲义， 很遗憾那次演讲没有录制下来。讲义可以在[这里](https://docs.google.com/presentation/d/1vxE61D_N79cvgUI3eIocF2n4rn04wjgRRq00ugyoB1M/edit?usp=sharing)找到。

![](../../assets/7560ca48bbf9472d.png)


ECS 以 16k 大小的块（Chunk）来分配内存，每个块仅包含单个原型中所有**实体**的**组件**数据。

一个[帖子](https://forum.unity.com/threads/memory-layout-for-ecs-components.590731/)中有人提供了更加形象的内存布局图，例如上半部分的原型由 Position 组件和 Rock 组件组成，其中整个原型占了一个块（Chunk），两个组件的数据分别存在两个数组中，里面还带着组件数据对应的实体的信息。

![](../../assets/43d881f0dc5cd564.jpg)


每个原型都有一个 Chunks 块列表，用来保存原型的实体。我们会循环所有块，并在每个块中，对紧凑的内存进行线性循环处理，以读取或写入组件数据。该线性循环会对每个实体运行相同的代码，同时为 Burst 创造向量化（Vectorization，可以参考 [StackOverflow 的问题](https://stackoverflow.com/questions/1422149/what-is-vectorization)）处理的机会。

每个块会被安排好内存中的位置，以便于快速从内存得到想要的数据，详情可以参考下面的文章。

### 实体（Entity）

实体是什么？实体只是一个 32 位的整数 key （和一些额外的数据例如 index 和 version 实体版本，不过在这里不重要），所以除了实体的组件数据外，不必为实体保存或分配太多内存。实体可以实现游戏对象的所有功能，甚至更多功能，因为实体非常轻量。

实体的性能消耗很低，所以我们可以把实体用在不适合游戏对象的情况，例如：为粒子系统内的每个单独粒子使用一个实体。

实体本身不是对象，也不是一个容器，它的作用是把其组件的数据关联到一起。

![](../../assets/85403e3d8729ca0c.png)


### 系统（System）

![](../../assets/35744984cf4d6d2c.png)


我们不必使用用户的 Update 方法搜索组件，然后在运行时对每个实例进行操作，使用 ECS 时我们只需静态地声明：我想对同时附带 Velocity 组件和 Rigidbody 组件的所有实体进行操作。为了找到所有实体，我们只需找到所有符合**特定“组件搜索查询”的原型**即可，而这个过程就是由系统（System）来完成的。

很多情况下，这个过程会分成多个 Job ，使处理 ECS 组件的代码达到几乎 100% 的核心利用率。ECS 会完成所有工作，我们只需要提供对每个实体运行的代码即可。我们也可以手动处理块迭代过程（[IJobChunk](https://github.com/Unity-Technologies/EntityComponentSystemSamples/blob/master/Samples/Assets/HelloECS/HelloCube_03_IJobChunk/README.md)）。

当我们从实体添加或移除组件时，ECS 会切换原型。我们会把它从当前块移动到新原型的块，然后交换之前块的最后实体来“填补空缺”。

在 ECS 中，我们还要静态声明要对组件数据进行什么处理，是 ReadOnly 只读还是 ReadWrite 读写（Job System 一小节提到过的两种缓冲区）。通过确定仅对 Position 组件进行读取，ECS 可以更高效地调度 Job ，其它需要读取 Position 组件的 Job 不必进行等待。

大体上，实体提供纯粹的数据给系统，系统根据自己所需要的组件来获得相应的满足条件的实体，最后系统再通过多线程来基于 Job System 来处理数据。

![](../../assets/a80c759baf8d4bce.jpg)


这种数据布局也解决了 Unity 长期以来的困扰，即：加载时间和序列化的性能。现在从大型场景加载或流式处理 ECS 数据的时间，不会比从硬盘加载和使用原始字节多多少。

## 优点

总的来说，ECS 有以下好处：

- 为性能而生
- 更容易写出高度优化和可重用的代码
- 更能充分利用硬件的性能
- 原型的数据被紧密地排列在内存中
- 享受 Burst 编译器带来的魔法

## 缺点

对 ECS 的常见观点是：ECS 需要编写很多代码。因此，实现想要的功能需要处理很多样板代码。现在针对移除多数样板代码需求的大量改进即将推出，这些改进会使开发者更简单地表达自己的目的。

Unity 暂时没有实现太多这类改进，因为 Unity 现在正专注于处理基础性能。

太多样板代码对 ECS 游戏代码没有好处，我们不能让编写 ECS 代码比编写 MonoBehaviour 更麻烦。


——Unity

而为网页游戏而生的基于 ECS 的 Project Tiny 已经实现了部分改进，例如：基于 lambda 函数的迭代 API。

# 最后

由于自己空闲时间不多，只能囫囵吞枣地拼凑出这样一篇笔记。上面大部分文字都是来自 Unity 的博文介绍，自己加了其他的内容帮助理解。本文从内存布局介绍了 ECS 的概念，也介绍了 Job System 和 Burst。我相信走过一遍文章之后，能清楚 Unity 对数据驱动的未来开发趋势的布局，也能更加容易从 [Unity ECS Sample](https://github.com/Unity-Technologies/EntityComponentSystemSamples) 中理解如何实践 ECS。

# 参考

[Unity DOD (ECS) 基础概念与资料汇总](https://indienova.com/indie-game-development/unity-dod-all-in-one/)- 这篇文章总结得很好，但很多视频链接都错了，我提供给了一个改好的版本：
[DOD 相关文章](https://www.notion.so/frankorz/DOTS-3562fce36b2a44909e5910609ddfd6a7)

- 这篇文章总结得很好，但很多视频链接都错了，我提供给了一个改好的版本：
[Unity ECS 编程官方文档选译–Getting Started](https://zhuanlan.zhihu.com/p/36649462)[面向数据技术栈 DOTS 之 ECS 实体组件系统](https://mp.weixin.qq.com/s/GsrX6o-sHLrqVgffp1svqg)[On DOTS: Entity Component System - Unity Blog](https://blogs.unity3d.com/2019/03/08/on-dots-entity-component-system/)[On DOTS: C++ & C# - Unity Blog](https://blogs.unity3d.com/2019/02/26/on-dots-c-c/)[ECS Deep Dive](https://rams3s.github.io/blog/2019-01-09-ecs-deep-dive/)[UniteLA 2018 - ECS deep dive](https://docs.google.com/presentation/d/1vxE61D_N79cvgUI3eIocF2n4rn04wjgRRq00ugyoB1M/edit?usp=sharing)[Intro To The Entity Component System And C# Job System](https://www.youtube.com/playlist?list=PLX2vGYjWbI0S4yHZwjDI1boIrYStpBCdN)- 视频中代码部分已经过时，建议参考
[Unity ECS Sample](https://github.com/Unity-Technologies/EntityComponentSystemSamples)官方 Demo 来学习 ECS

- 视频中代码部分已经过时，建议参考