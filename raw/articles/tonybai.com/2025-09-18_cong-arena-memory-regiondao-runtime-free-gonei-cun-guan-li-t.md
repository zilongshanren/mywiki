---
title: 从arena、memory region到runtime.free：Go内存管理探索的务实转向
url: https://tonybai.com/2025/09/18/go-runtime-free-proposal/
published: '2025-09-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 从arena、memory region到runtime.free：Go内存管理探索的务实转向

![](../../assets/2a66a78efcbb2636.png)


[本文永久链接](https://tonybai.com/2025/09/18/go-runtime-free-proposal) – https://tonybai.com/2025/09/18/go-runtime-free-proposal

大家好，我是Tony Bai。

Go 的垃圾收集器（GC）是其简单性和并发安全性的基石，但也一直是性能优化的焦点。近年来，Go 核心团队为了进一步降低 GC 开销，进行了一系列前沿探索：从备受争议的[arena](https://github.com/golang/go/issues/51317) 实验，到更优雅但实现复杂的 [memory regions构想](https://github.com/golang/go/discussions/70257)，最终，焦点似乎汇聚在了一项更务实、更具潜力的提案上——runtime.free。这项编号为 [#74299](https://github.com/golang/go/issues/74299) 的实验性提案，正试图为 Go 的内存管理引入一个革命性的新维度：**允许编译器和部分标准库在特定安全场景下，绕过 GC，直接释放和重用内存**。其原型已在 strings.Builder 等场景中展现出高达 2 倍的性能提升。

本文将带着大家一起回顾 Go 内存管理的这段探索之旅，并初步剖析一下 runtime.free 提案的背景、核心机制及其对 Go 性能生态的深远影响。

![](../../assets/f3973191ef9d6abe.png)


## 背景：一场关于“手动”内存管理的漫长探索

Go 语言自诞生以来，其自动内存管理（GC）一直是核心特性之一。然而，对于性能极致敏感的场景——例如高吞吐量的网络服务——GC 的开销始终是开发者关注的焦点。为了赋予开发者更多控制力，Go 团队近年来开启了一系列关于“手动”或“半自动”内存管理的探索。

### 第一站：arena 实验——功能强大但难以融合

arena 实验（#51317）是第一次大胆的尝试。它引入了一个 arena.Arena 类型，允许开发者将一组生命周期相同的对象分配到一个独立的内存区域中，并在不再需要时**一次性、批量地释放整个区域**。

**优点**：arena 在特定场景下取得了显著的性能提升，因为它极大地减少了 GC 的扫描和回收工作。**问题**：arena 的 API**侵入性太强**。几乎所有需要利用 arena 的函数都必须额外接收一个 arena 参数，这会导致 API 的“病毒式”传播，并且与 Go 的隐式接口、逃逸分析等特性组合得非常糟糕。最终，由于其糟糕的“可组合性”，arena 提案被无限期搁置。

### 第二站：memory regions——更优雅的构想与巨大的挑战

吸取了 arena 的教训，Go 团队提出了一个更优雅、更符合 Go 哲学的构想：**内存区域（Memory Regions）**（#70257）。其核心思想是，通过一个 region.Do(func() { … }) 调用，将一个函数作用域内的所有内存分配**隐式地**绑定到一个临时的、与 goroutine 绑定的区域中。

**优点**：API 对用户透明，无需修改现有函数的签名。更重要的是，它是**内存安全**的——如果区域内的某个对象“逃逸”到了区域之外，运行时会自动将其“拯救”出来，交还给全局 GC 管理，避免了 arena 可能导致的 use-after-free 崩溃。**问题**：这个优雅设计的背后，是**极其复杂的实现**。它需要在开启区域的 goroutine 中启用一个特殊的、低开销的**写屏障（write barrier）**来动态追踪内存的逃逸。虽然理论上可行，但其实现复杂度和潜在的性能开销，使其成为一个长期且充满不确定性的研究课题。

### 最终的焦点：runtime.free——务实且精准的“外科手术”

在 arena 的侵入性和 memory regions 的复杂性之间，Go 团队似乎找到了一个更务实、更具工程可行性的平衡点——runtime.free 提案。

它不再追求一个“要么全有，要么全无”的全局解决方案，而是提出了一种**精准的、由编译器和运行时主导的“外科手术”**。其核心思想是：与其让开发者手动管理整个内存区域，不如让更了解代码细节的**编译器**和**底层标准库**，在绝对安全的前提下，对那些生命周期短暂的、已知的堆分配进行**点对点的、即时的释放和重用**。

这种方法解决了 arena 的可组合性问题（因为它是自动的或内部的），也绕开了 memory regions 的全局复杂性。它像一把锋利的手术刀，精确地切除了那些最明确、最高频的冗余内存分配，为解决 Go 性能优化中的“鸡与蛋”问题提供了全新的思路。

## runtime.free 的双重策略：编译器自动化与标准库手动优化

该提案并非要将 free 的能力直接暴露给普通开发者。相反，它采取了一种高度受控的、分两路进行的策略：

### 1. 编译器自动化 (runtime.freetracked)

这是该提案最激动人心的部分。编译器将获得自动插入内存跟踪和释放代码的能力。

-
**工作流程**：**识别**：当编译器遇到一个 make([]T, size)，它能证明这个 slice 的生命周期不会超过当前函数作用域，但因其大小未知（或超过 32 字节）而必须在堆上分配时，它会将这次分配标记为“可跟踪”。**跟踪**：编译器会生成 makeslicetracked64 来分配内存，并将一个“跟踪对象”记录在当前函数**栈上的一个特殊数组**freeablesArr 中。**释放**：编译器会自动插入一个 defer freeTracked(&freeables) 调用。当函数退出时，这个 defer 会被执行，通知运行时可以安全地回收 freeablesArr 中记录的所有堆对象。

-
**对开发者的影响**：这意味着，未来开发者编写的许多看似会产生堆分配的函数，将被编译器**自动重写**为不产生 GC 压力的版本，而开发者对此**完全无感**。

```
// 开发者编写的代码
func f1(size int) {
s := make([]int64, size) // 堆分配
// ... use s
}
// 编译器可能重写为（概念上）
func f1(size int) {
var freeablesArr [1]trackedObj
freeables := freeablesArr[:]
defer runtime.freeTracked(&freeables)
s := runtime.makeslicetracked64(..., &freeables) // 分配并跟踪
// ... use s
}
```


### 2. 标准库手动优化 (runtime.freesized)

对于一些底层、性能关键的标准库组件，它们内部的内存管理逻辑比编译器能静态证明的要复杂。对于这些场景，提案提供了一个受限的、手动的 runtime.freesized 接口。

-
**目标场景**：- strings.Builder / bytes.Buffer 的扩容：当内部 []byte 缓冲区需要扩容时，旧的、较小的缓冲区就可以被立即释放。
- map 的扩容：当 map 增长或分裂时，旧的 backing array 也可以被回收。
- slices.Collect：在构建最终 slice 过程中产生的中间 slice 也可以被释放。

-
**惊人的性能提升**：提案中的基准测试显示，通过在 strings.Builder 的扩容逻辑中手动调用 runtime.freesized，在有多次写入（即多次扩容）的场景下，其性能**提升了 45% 到 55%**，几乎是原来的两倍快！

![](../BlogImages/2025/go-runtime-free-proposal-2.png)


这证明，在正确的“热点”位置进行手动释放，可以带来巨大的性能收益。

## 性能影响与权衡

引入手动内存管理，必然会带来对正常分配路径的性能影响。提案对此进行了细致的评估：

**对正常分配路径的影响**：基准测试表明，即使开启了 runtimefree 实验，对于不涉及内存重用的普通分配路径，其性能影响在**-1.5% 到 +2.2%**之间，几何平均值几乎为零。这表明该功能在不使用时，几乎是“免费”的。**潜在的性能收益**：**减少 GC CPU 使用**：这是最直接的好处。**延长 GC 周期**：更少的垃圾意味着 GC 运行频率更低，从而减少写屏障（write barrier）开启的时间，提升应用代码的执行速度。**更优的缓存局部性**：被释放的内存可以立即被下一个分配重用，可能形成 LIFO（后进先出）式的内存访问模式，对 CPU 缓存极为友好。**减少 GC 停顿**：更少的 GC 工作意味着更少的 STW（Stop-The-World）时间和 GC 辅助（assist）开销。


## 小结：Go 内存管理的“第三条路”

runtime.free 提案并非要将 Go 变成 C++ 或 Rust，它无意将手动内存管理的复杂性抛给普通开发者。相反，它代表了 Go 在自动内存管理（GC）和静态内存管理（栈分配）之外，探索的**“第三条路”——由编译器和运行时主导的、高度受控的动态内存优化**。

这一探索是务实且极具潜力的：

**务实**：它从解决现实的性能瓶颈（如 strings.Builder）和优化僵局（逃逸分析）入手，目标明确。**安全**：通过将能力严格限制在编译器和少数底层标准库中，它最大限度地避免了困扰其他语言的手动内存管理错误。**潜力巨大**：一旦这个机制成熟，编译器可以将其应用到更多模式中（如循环内的 append），进一步减少 Go 程序的内存分配。

虽然这项工作仍处于实验阶段，但它清晰地指明了 Go 性能优化的下一个前沿方向。通过让编译器和运行时变得更加“智能”，在保证安全性的前提下，选择性地介入内存管理，Go 语言有望在保持其简洁易用性的同时，攀上新的性能高峰。

## 参考资料

- runtime, cmd/compile: add runtime.free, runtime.freetracked and GOEXPERIMENT=runtimefree – https://github.com/golang/go/issues/74299
- a safe free of memory proposal, runtime.FreeMemory() – https://groups.google.com/g/golang-nuts/c/cmpiArv10f4
- Directly freeing user memory to reduce GC work – https://go.googlesource.com/proposal/+/94843c2c941f64a86001e51ed775b918cc89b365/design/74299-runtime-free.md
- memory regions – https://github.com/golang/go/discussions/70257
- proposal: arena: new package providing memory arenas – https://github.com/golang/go/issues/51317

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论