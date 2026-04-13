---
title: 《图解 C# 教程 第5版》与性能优化
url: http://frankorz.com/2020/01/31/illustrated-csharp-and-performance/
author: 文章作者 猫冬
published: '2020-01-31'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

这本书仍然是入门 C# 最好的一本书。

这本书新版出来的时候我十分关注，于是英子姐送了一本给我，本文也是答应英子姐所写的一篇文章。她一开始还问我“你现在还需要看这本入门书吗？”，我认为是的。工作了遇到了不少问题，大都跟自己基础不牢有关系。

这本书以图形为载体，生动地介绍了 C# 语言本身。其中图形对我们了解 C# 语法在内存中的本质十分有帮助，异步、异常等章节中的处理流程图也很清晰明了，这也是我看重的一点。

本文会从本书出发，简单讲讲代码优化的一些点。

## 在内存中的形态

为什么要了解 C# 在内存中的形态呢？

书中第四章介绍内存区域的栈中，有一句话说的很好：

作为程序员，你不需要显式地对它做任何事情。但了解栈的基本功能可以更好地了解程序在运行时在做什么，并能更好地了解 C# 文档和著作。


游戏开发中，除了业务逻辑，我们还会更关注游戏的性能本身。我们需要保证游戏能流畅运行在大部分机型上，保证每一帧能流畅地播放，例如 CPU 需要处理渲染代码、物理模拟、动画回调等等，其中我们的代码也有可能引起性能问题。我们需要更了解执行代码的代价，例如：

- 这些代码产生了多少 GC
- GC 只会产生一次还是每帧都会产生
- 在极端情况下代码的性能如何
- 是否使用了正确的数据结构
- Unity API 或者一些库 API 的背后到底做了什么
- …

这本书相对上一版多了 .Net Core, C# 7.0 语法的讲解，对于我而言，重温的是第 4、7、11、13、15、17、19 和 27 章节，这些内容是我工作中经常要接触、着手优化的地方。书中对于异步编程也介绍地很好，但对于我来说，反射、异步编程、新增语法等到以后有需要再看也不迟。

脚本的性能优化，无非是用更合适的代码去实现需求，不必要的内存都给我吐出来！（注：作者在生活中并没有这么吝啬）

下面会列举一些代码写法的性能对比。

## 结构和类

这其实也是用栈还是用堆的考量。

### 垃圾回收

Unity 用的是 mono 虚拟机，其堆的内存是通过垃圾回收算法 Boehm GC 来管理的，其不分代（Non-generational）和非压缩式（Non-compacting）的特性，导致了我们平常要注意避免加载过多的小内存，从而内存碎片化（Memory fragmentation）。

**分代**：大块内存、小内存、超小内存分在不同内存区域来进行管理。此外还有长久内存，当有一个内存很久没动的时候会移到长久内存区域中，从而省出内存给更频繁分配的内存。**压缩式**：当有内存被回收的时候，压缩内存会把下图空的地方重新排布。

![compacting.png](../../assets/a19636d6c854654a.png)

**内存碎片化**：内存过多小内存，导致大内存不能有效地被使用。

![memory fragmentation](../../assets/05351accb80f3f38.png)


具体可以参考 Unity 文档 [Understanding the managed heap](https://docs.unity3d.com/Manual/BestPracticeUnderstandingPerformanceInUnity4-1.html)

同时也推荐高川老师的演讲：[浅谈 Unity 内存管理](https://www.bilibili.com/video/av79798486/)，和我看视频时的笔记：[笔记](https://www.notion.so/Unity-f79bb1d4ccfc483fbd8f8eb859ae55fe)。

### 用结构还是类

这里推一篇微软官方文档：[Choosing Between Class and Struct](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/choosing-between-class-and-struct)

引用类型被分配在堆上并被垃圾回收算法管理，值类型则分配在栈上，栈会按需 [unwind](http://en.wikipedia.org/wiki/Call_stack#Unwinding) 来释放他们。因此，值类型的释放比引用类型的释放开销要小。

书中 11.9 小节还提到：

对结构进行分配的开销比创建类实例小，所以使用结构代替类有时可以提高性能，但要注意装箱和拆箱的高昂代价。


**值类型数组**的分配和释放比**引用类型数组**的分配和释放开销也更小。

除了最基本的修改值类型和引用类型的区别外，要注意的是传递参数或者返回返回值的时候，值类型都会隐性地被创建，这可能也会产生没想到的内存开销。

从 .Net 内存分配成本的角度来说，类的对象储存的内存首先需要分配 4 个字节作为**对象头字节**（object header word），跟着再分配 4 个字节作为**方法表指针**（method table pointer），这些字段是服务于 JIT 和 CIL 的，是隐藏的分配成本。

保留在堆中所需的内存还会根据操作系统位数来决定：

- 32 位系统中，堆上的对象会对齐到最近 4 字节的倍数，因此如果一个对象只有一个 byte 成员，也需要对齐占 4 个字节，因此这个对象总共占堆上 12 个字节。
- 64 位系统中，堆上的对象会对齐到最近 8 字节的倍数，方法表指针和对象头字节也会分别占 8 字节的内存。

（注：平常开发我们不需要这么抠门，上面只是一个小知识点。）

大多时候我们都会用类型来实现设计模式、框架的设计，那什么时候使用结构体呢？我们可以遵循微软爸爸的建议：

- 逻辑上表示单个值
- 大小小于 16 个字节
- 不会改变值
- 不需要经常装箱拆箱

对于一些特定的场景下，我们也可以享受值类型数组在内存中线性排布的福利，例如内存连续、SIMD 等。Unity 的 DOTS 技术栈就是一个很好的例子。

推荐阅读：

[在C#中使用Struct代替Class](https://zhuanlan.zhihu.com/p/100162855)- 作者用 DOTS（结构体、Job System、Burst）实现 A 星寻路实现性能飞跃：y2b 搜 “Pathfinding in Unity DOTS!”

## 装箱

第 17 章介绍了转换，其中提到了装箱拆箱。那么装箱的代价有多大呢？我们可以做个测试：

1 | public const int Iterations = 100_000; |

![profiler](../../assets/c0f78291419c7580.png)


查看 Profiler 可以看到，调用十次 TestA 产生了 26.7MB GC，用了 267.22 毫秒；调用十次 TestB 只产生了 3.8MB GC，用了 20.92 毫秒。因此大量的装箱拆箱会导致不必要的性能消耗，而有些消耗则是完全可以避免的。

我的 Rider 插件 [Heap Allocations Viewer](https://plugins.jetbrains.com/plugin/9223-heap-allocations-viewer) 也会提示我 TestA 中存在装箱的情况。

![rider-boxing-plugin](../../assets/3051b3bb09924f31.png)


## 最后

写到这里，发现还很多东西没讲完就已经这么多篇幅了…

大家对于平常代码的不同写法也可以测试下性能，例如：

- foreach 和 for
- 装箱和拆箱
- 一维数组、多维数组（矩形数组）和交错数组（Jagged Arrays）
- 这里还是强调下尽量使用一维数组，实在需要用多维数组的话，可以改用交错数组

- 通过 for 循环复制数组和 Array.CopyTo 方法
- 字符串拼接，string 和 Stringbuilder
- 反射和 DynamicMethod
- …

上面装箱的截图中的测试项目我也上传了 Github：[Latias94/UnityCsharpPerformanceTest](https://github.com/Latias94/UnityCsharpPerformanceTest)，不用 Unity 的同学也可以参考下实际的测试代码：[UnityCsharpPerformanceTest/Assets/Scripts](https://github.com/Latias94/UnityCsharpPerformanceTest/tree/master/Assets/Scripts)，自己写个命令行项目来跑下对比。

当然我们开发中还是要以需求的变化为主，不能过早优化从而破坏代码的扩展性。