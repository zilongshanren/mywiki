---
tags: [ppc, powerpc, lhs, 流水线, xbox360]
date: 2026-04-14
sources: 1
---

# PowerPC 整浮点转换与 Load-Hit-Store 停顿

Xbox 360、PlayStation 3 世代的乱序能力极弱的 in-order PowerPC 核心上，**整型寄存器和浮点寄存器之间不能直接互传数据**——必须走内存。一次普通的 `int → float` 转换展开后是：

1. `extsw`：把 32 位整数符号扩展到 64 位
2. `std`：把 64 位值写进栈上临时地址
3. `lfd`：把同一个地址加载到浮点寄存器
4. `fcfid`：把 64 位整数转成 double
5. `frsp`：再舍入回 single

第 2 步和第 3 步构成了**Load-Hit-Store（LHS）** 停顿的教科书样本：同一个地址刚被 store、立刻被 load，处理器必须等 store buffer 排干后才能服务这条 load。在 Xenon / CELL PPU 这类 in-order 核上，这一下就是几十个 cycle 的 bubble。[[fabian-giesen|ryg]] 把这条坑称为主机程序员的「上古恐惧」。

## 为什么编译器帮不上忙

按理说：四个独立的 int→float 转换应该能把四个 store 做完再做四个 load，这样只有第一个 load 撞上 LHS，后三个已经 retire 完毕。ryg 实测 gcc、Microsoft、SN 三家 PPC 编译器**全部没有做这个重排**——`int a; int b; int c; int d; some_function(a*scale, b*scale, ...)` 编出来是四连串 LHS，每一个都要单独等 store buffer 排干。

## 诱导编译器「分离 store 与 load」

ryg 找到的 workaround 思路是：把 `S32` 换成一个 `volatile S64` 临时量（或 `__fcfid` intrinsic），让编译器把 store 和 int→float 转换拆成两段，从而允许它把四个 store 全部提前。这样四次 LHS 降到一次（因为四个临时都落在同一条 cache line 上）。不同编译器的具体 spelling 不一样，但一个 `typedef volatile S64` + 内联 `fast_itof` 的组合可以照顾到三家。

```
typedef volatile S64 S32itof;  // compiler A
static inline F32 fast_itof(S32itof x) {
  return (F32)__fcfid(x);       // others
}
```

## 还能更干净吗

另一条路是彻底走 VMX（AltiVec）向量单元：有 `vcfsx` 这类直接的 int→float 指令，不走内存。问题是 VMX 自身的通路也**不能直接和整数 / 浮点单元互通**——进 VMX 还是得走内存，于是你只能整段 SIMD 化。对分支密集、`cr6` 对 `vcmp` 变体又慢的代码（比如 ryg 当时在做的 SWF 位流解码器），这不划算；减四倍 LHS 的单行 workaround 是性价比更高的选择。

## 和其他话题的连线

- **为什么这种坑会存在**：in-order PPC 对 store-to-load forwarding 的实现极其弱，反映出 [[latency-vs-throughput]] 里微架构选择的权衡。
- **同一原理的续集**：SPU / VMX 之间「要对话必须走 DMA / 内存」和这里的跨单元传递属于同一个设计哲学——寄存器 domain 之间物理隔离。
- **编译器盲区**：和 [[compiler-interference-analysis-bug]] 一样，这是一个编译器本该做但没做的「显然优化」，你只能用类型把真相塞进去。

## 相关

- [[fabian-giesen]]
- [[latency-vs-throughput]]
- [[memory-hierarchy]]
- [[sse-tricks]]
- [[calling-conventions-x86]]
- [[register-spilling-avoidance]]

## Sources

- [[sources/ryg-more-ppc-compiler-babysitting]]
