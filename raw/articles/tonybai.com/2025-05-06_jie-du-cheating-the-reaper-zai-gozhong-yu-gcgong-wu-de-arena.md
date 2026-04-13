---
title: 解读“Cheating the Reaper”：在Go中与GC共舞的Arena黑科技
url: https://tonybai.com/2025/05/06/cheating-the-reaper-in-go/
published: '2025-05-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 解读“Cheating the Reaper”：在Go中与GC共舞的Arena黑科技

![](../../assets/49aacb702ed02dd5.jpg)


[本文永久链接](https://tonybai.com/2025/05/06/cheating-the-reaper-in-go) – https://tonybai.com/2025/05/06/cheating-the-reaper-in-go

大家好，我是Tony Bai。

Go语言以其强大的垃圾回收 (GC) 机制解放了我们这些 Gopher 的心智，让我们能更专注于业务逻辑而非繁琐的内存管理。但你有没有想过，在 Go 这个看似由 GC “统治”的世界里，是否也能体验一把“手动管理”内存带来的极致性能？甚至，能否与 GC “斗智斗勇”，让它为我们所用？

**事实上，Go 官方也曾进行过类似的探索。** 他们尝试在标准库中加入一个arena包，提供一种基于区域 (Region-based) 的内存管理机制。测试表明，这种方式确实能在特定场景下通过**更早的内存复用**和**减少 GC 压力**带来显著的性能提升。然而，这个官方的 Arena 提案最终**被无限期搁置了**。原因在于，Arena 这种手动内存管理机制与 Go 语言现有的大部分特性和标准库**组合得很差 (compose poorly)**。

官方的尝试尚且受阻，那么个人开发者在 Go 中玩转手动内存管理又会面临怎样的挑战呢？最近，一篇名为 **“Cheating the Reaper in Go”** (在 Go 中欺骗死神/收割者) 的文章在技术圈引起了不小的关注。作者 mcyoung 以其深厚的底层功底，展示了如何利用unsafe包和对 Go GC 内部运作机制的深刻理解，构建了一个**非官方的、实验性的**高性能内存分配器——Arena。

这篇文章的精彩之处不仅在于其最终实现的性能提升，更在于它**揭示了在 Go 中进行底层内存操作的可能性、挑战以及作者与 GC “共舞”的巧妙思路**。**需要强调的是，本文的目的并非提供一个生产可用的 Arena 实现（官方尚且搁置，其难度可见一斑），而是希望通过解读作者这次与 GC “斗智斗勇”的“黑科技”，和大家一起更深入地理解 Go 的底层运作机制。**

## 为何还要探索 Arena？理解其性能诱惑

即使官方受阻，理解 Arena 的理念依然有价值。它针对的是 Go 自动内存管理在某些场景下的潜在瓶颈：

**高频、小对象的分配与释放：**频繁触碰 GC 可能带来开销。**需要统一生命周期管理的内存：**一次性处理比零散回收更高效。

Arena 通过**批量申请、内部快速分配、集中释放**（在 Go 中通常是让 Arena 不可达由 GC 回收）的策略，试图在这些场景下取得更好的性能。

## 核心挑战：Go 指针的“特殊身份”与 GC 的“规则”

作者很快指出了在 Go 中实现 Arena 的核心障碍：**Go 的指针不是普通的数据**。GC 需要通过**指针位图 (Pointer Bits)** 来识别内存中的指针，进行可达性分析。而自定义分配的原始内存块缺乏这些信息。

作者提供了一个类型安全的泛型函数New[T]来在 Arena 上分配对象：

```
type Allocator interface {
Alloc(size, align uintptr) unsafe.Pointer
}
// New allocates a fresh zero value of type T on the given allocator, and
// returns a pointer to it.
func New[T any](a Allocator) *T {
var t T
p := a.Alloc(unsafe.Sizeof(t), unsafe.Alignof(t))
return (*T)(p)
}
```


但问题来了，如果我们这样使用：

```
p := New[*int](myAlloc) // myAlloc是一个实现了Allocator接口的arena实现
*p = new(int)
runtime.GC()
**p = 42 // Use after free! 可能崩溃!
```


因为 Arena 分配的内存对 GC 不透明，GC 看不到里面存储的指向new(int)的指针。当runtime.GC()执行时，它认为new(int)分配的对象已经没有引用了，就会将其回收。后续访问**p就会导致 Use After Free。

## “欺骗”GC 的第一步：让 Arena 整体存活

面对这个难题，作者的思路是：**让 GC 知道 Arena 的存在，并间接保护其内部分配的对象**。关键在于确保：**只要 Arena 中有任何一个对象存活，整个 Arena 及其所有分配的内存块（Chunks）都保持存活。**

这至关重要，通过强制标记整个 arena，arena 中存储的任何指向其自身的指针将自动保持活动状态，而无需 GC 知道如何扫描它们。所以，虽然这样做后， *New[*int](a) = new(int) 仍然会导致释放后重用，但 *New[*int](a) = New[int](a) 不会！即arena上分配的指针仅指向arena上的内存块。 这个小小的改进并不能保证 arena 本身的安全，但只要进入 arena 的指针完全来自 arena 本身，那么拥有内部 arena 的数据结构就可以完全安全。

**1. 基本 Arena 结构与快速分配**

首先，定义 Arena 结构，包含指向下一个可用位置的指针next和剩余空间left。其核心分配逻辑 (Alloc) 主要是简单的指针碰撞：

```
package arena
import "unsafe"
type Arena struct {
next unsafe.Pointer // 指向当前 chunk 中下一个可分配位置
left uintptr // 当前 chunk 剩余可用字节数
cap uintptr // 当前 chunk 的总容量 (用于下次扩容参考)
// chunks 字段稍后添加
}
const (
maxAlign uintptr = 8 // 假设 64 位系统最大对齐为 8
minWords uintptr = 8 // 最小分配块大小 (以字为单位)
)
func (a *Arena) Alloc(size, align uintptr) unsafe.Pointer {
// 1. 对齐 size 到 maxAlign (简化处理)
mask := maxAlign - 1
size = (size + mask) &^ mask
words := size / maxAlign
// 2. 检查当前 chunk 空间是否足够
if a.left < words {
// 空间不足，分配新 chunk
a.newChunk(words) // 假设 newChunk 会更新 a.next, a.left, a.cap
}
// 3. 在当前 chunk 中分配 (指针碰撞)
p := a.next
// (优化后的代码，去掉了检查 one-past-the-end)
a.next = unsafe.Add(a.next, size)
a.left -= words
return p
}
```


**2. 持有所有 Chunks**

为了防止 GC 回收 Arena 已经分配但next指针不再指向的旧 Chunks，需要在 Arena 中明确持有它们的引用：

```
type Arena struct {
next unsafe.Pointer
left, cap uintptr
chunks []unsafe.Pointer // 新增：存储所有分配的 chunk 指针
}
// 在 Alloc 函数的 newChunk 调用之后，需要将新 chunk 的指针追加到 a.chunks
// 例如，在 newChunk 函数内部实现: a.chunks = append(a.chunks, newChunkPtr)
```


原文测试表明，这个append操作的成本是摊销的，对整体性能影响不大，结果基本与没有chunks字段时持平。

**3. 关键技巧：Back Pointer**

是时候保证整个arena安全了！这是“欺骗”GC 的核心。通过reflect.StructOf动态创建包含unsafe.Pointer字段的 Chunk 类型，并在该字段写入指向 Arena 自身的指针：

```
import (
"math/bits"
"reflect"
"unsafe"
)
// allocChunk 创建新的内存块并设置 Back Pointer
func (a *Arena) allocChunk(words uintptr) unsafe.Pointer {
// 使用 reflect.StructOf 创建动态类型 struct { Data [N]uintptr; BackPtr unsafe.Pointer }
chunkType := reflect.StructOf([]reflect.StructField{
{
Name: "Data", // 用于分配
Type: reflect.ArrayOf(int(words), reflect.TypeFor[uintptr]()),
},
{
Name: "BackPtr", // 用于存储 Arena 指针
Type: reflect.TypeFor[unsafe.Pointer](), // !! 必须是指针类型，让 GC 扫描 !!
},
})
// 分配这个动态结构体
chunkPtr := reflect.New(chunkType).UnsafePointer()
// 将 Arena 自身指针写入 BackPtr 字段 (位于末尾)
backPtrOffset := words * maxAlign // Data 部分的大小
backPtrAddr := unsafe.Add(chunkPtr, backPtrOffset)
*(**Arena)(backPtrAddr) = a // 写入 Arena 指针
// 返回 Data 部分的起始地址，用于后续分配
return chunkPtr
}
// newChunk 在 Alloc 中被调用，用于更新 Arena 状态
func (a *Arena) newChunk(requestWords uintptr) {
newCapWords := max(minWords, a.cap*2, nextPow2(requestWords)) // 计算容量
a.cap = newCapWords
chunkPtr := a.allocChunk(newCapWords) // 创建新 chunk 并写入 BackPtr
a.next = chunkPtr // 更新 next 指向新 chunk 的 Data 部分
a.left = newCapWords // 更新剩余容量
// 将新 chunk (整个 struct 的指针) 加入列表
a.chunks = append(a.chunks, chunkPtr)
}
// (nextPow2 和 max 函数省略)
```


通过这个 Back Pointer，任何指向 Arena 分配内存的外部指针，最终都能通过 GC 的扫描链条将 Arena 对象本身标记为存活，进而保活所有 Chunks。这样，Arena 内部的指针（指向 Arena 分配的其他对象）也就安全了！原文的基准测试显示，引入 Back Pointer 的reflect.StructOf相比直接make([]uintptr)对性能有轻微但可察觉的影响。

## 性能再“压榨”：消除冗余的 Write Barrier

分析汇编发现，Alloc函数中更新a.next(如果类型是unsafe.Pointer) 会触发 **Write Barrier**。这是 GC 用来追踪指针变化的机制，但在 Back Pointer 保证了 Arena 整体存活的前提下，这里的 Write Barrier 是冗余的。

作者的解决方案是将next改为uintptr：

```
type Arena struct {
next uintptr // <--- 改为 uintptr
left uintptr
cap uintptr
chunks []unsafe.Pointer
}
func (a *Arena) Alloc(size, align uintptr) unsafe.Pointer {
// ... (对齐和检查 a.left < words 逻辑不变) ...
if a.left < words {
a.newChunk(words) // newChunk 内部会设置 a.next (uintptr)
}
p := a.next // p 是 uintptr
a.next += size // uintptr 直接做加法，无 Write Barrier
a.left -= words
return unsafe.Pointer(p) // 返回时转换为 unsafe.Pointer
}
// newChunk 内部设置 a.next 时也应存为 uintptr
func (a *Arena) newChunk(requestWords uintptr) {
// ... (allocChunk 不变) ...
chunkPtr := a.allocChunk(newCapWords)
a.next = uintptr(chunkPtr) // <--- 存为 uintptr
// ... (其他不变) ...
}
```


这个优化效果如何？原文作者在一个 GC 压力较大的场景下（通过一个 goroutine 不断调用runtime.GC()模拟）进行了测试，结果表明，**对于小对象的分配，消除 Write Barrier 带来了大约 20% 的性能提升**。这证明了在高频分配场景下，即使是 Write Barrier 这样看似微小的开销也可能累积成显著的性能瓶颈。

## 更进一步的可能：Arena 复用与sync.Pool

文章还提到了一种潜在的优化方向：**Arena 的复用**。当一个 Arena 完成其生命周期后（例如，一次请求处理完毕），其占用的内存理论上可以被“重置”并重新利用，而不是完全交给 GC 回收。

作者建议，可以将不再使用的 Arena 对象放入sync.Pool中。下次需要 Arena 时，可以从 Pool 中获取一个已经分配过内存块的 Arena 对象，只需重置其next和left指针即可开始新的分配。这样做的好处是：

**避免了重复向 GC 申请大块内存**。- 可能
**节省了重复清零内存**的开销（如果 Pool 返回的 Arena 内存恰好未被 GC 清理）。

这需要更复杂的 Arena 管理逻辑（如 Reset 方法），但对于需要大量、频繁创建和销毁 Arena 的场景，可能带来进一步的性能提升。

## unsafe：通往极致性能的“危险边缘”

贯穿整个 Arena 实现的核心是unsafe包。作者坦诚地承认，这种实现方式严重依赖 Go 的内部实现细节和unsafe提供的“后门”。

这再次呼应了 Go 官方搁置 Arena 的原因——它与语言的安全性和现有机制的兼容性存在天然的矛盾。使用unsafe意味着：

- 放弃了类型和内存安全保障。
- 代码变得脆弱，可能因 Go 版本升级而失效（尽管作者基于
[Hyrum 定律](https://tonybai.com/2025/04/26/13-laws-of-software-engineering)认为风险相对可控）。 - 可读性和可维护性显著降低。

## 小结

“Cheating the Reaper in Go” 为我们呈现了一场精彩的、与 Go GC “共舞”的“黑客艺术”。通过对 GC 原理的深刻洞察和对unsafe包的大胆运用，作者展示了在 Go 中实现高性能自定义内存分配的可能性，虽然作者的实验性实现是一个toy级别的。

然而，正如 Go 官方的 Arena 实验所揭示的，将这种形式的手动内存管理完美融入 Go 语言生态，面临着巨大的挑战和成本。因此，我们应将这篇文章更多地视为一次理解 Go 底层运作机制的“思想实验”和“案例学习”，而非直接照搬用于生产环境的蓝图。

对于绝大多数 Go 应用，内建的内存分配器和 GC 依然是最佳选择。但通过这次“与死神共舞”的探索之旅，我们无疑对 Go 的底层世界有了更深的敬畏和认知。

**你如何看待在 Go 中使用unsafe进行这类底层优化？官方 Arena 实验的受阻说明了什么？欢迎在评论区分享你的思考！** 如果你对 Go 的底层机制和性能优化同样充满好奇，别忘了点个【赞】和【在看】！

原文链接：https://mcyoung.xyz/2025/04/21/go-arenas

商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论