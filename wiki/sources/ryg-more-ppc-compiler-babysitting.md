---
tags: [source, ppc, xbox360, 编译器, 流水线]
date: 2026-04-14
sources: 1
---

# More PPC compiler babysitting（Fabian Giesen）

[[fabian-giesen|ryg]] 2010 年 11 月的一篇短文，记录了在 Xbox 360 / PS3 世代 in-order PowerPC 核上做 `int → float` 转换必然撞上 Load-Hit-Store 停顿，以及三家主流 PPC 编译器**全部**没有做「批量 store 再批量 load」这个显然的重排优化，所以要通过 `volatile S64` / `__fcfid` intrinsic 来手工诱导。

## 摘要

PPC 整数寄存器和浮点寄存器之间不能直接互传，`int → float` 必须走 `extsw → std → lfd → fcfid → frsp` 五步，其中 `std → lfd` 是 LHS 停顿的教科书样本——几十个 cycle 的 bubble。对四个独立的转换，编译器理论上应该把四次 store 全部做完、再做四次 load，这样只吃一次 LHS（其他落在同一 cache line 上的 load 可以 forward）。gcc / Microsoft / SN 三家 PPC 编译器实测都没做这件事，老老实实生成了四连串 LHS。workaround 是把临时变量类型换成 `volatile S64`（或者显式用 `__fcfid` intrinsic），让编译器把 store 和类型转换拆开，从而允许 store 提前。代价微小，收益巨大——在 SWF 解码器里四减一是几个百分点的加载速度提升。

## 关键要点

- in-order PPC 上 `int → float` 每次都 LHS；VMX 通路同样也是「跨 domain 必走内存」。
- 完全 SIMD 化是 clean 的解但不适用所有代码，尤其是分支密集的位流解析（`cr6` 对 `vcmp` 变体慢）。
- `volatile S64` + inline `fast_itof` 这样一行 workaround 就能把 4× LHS 降到 1×。
- 这是经典的「编译器盲区」例子：显然的优化机会，三家编译器全部错过。
- 实测是 RAD 当时的 SWF 矢量解码器性能调优，.SWF 的文件格式不能动，只能从代码侧抠。

## 链接到的概念

- [[ppc-int-float-lhs]]
- [[fabian-giesen]]
- [[latency-vs-throughput]]
- [[memory-hierarchy]]
- [[calling-conventions-x86]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/11/06/more-ppc-compiler-babysitting/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-11-06_more-ppc-compiler-babysitting.md`
