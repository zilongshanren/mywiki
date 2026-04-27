---
tags: [cpu, 微架构, renamer, move-elimination, 前端]
date: 2026-04-19
sources: 3
---

# Move Elimination 与 Zeroing Idiom

现代乱序核的 **renamer** 不再只是把架构寄存器映射成物理寄存器，它还能识别出几类"空操作"直接在 rename 阶段消掉，省下 ALU 口与调度器槽位。两个代表招数：**Move Elimination**（消 MOV）与 **Zeroing Idiom Elimination**（消自清零）。

## Move Elimination

`MOV reg1, reg2` 不必真的让 ALU 复制一份值——renamer 可以把两个架构寄存器指向同一个物理寄存器即可。Intel Ivy Bridge 首次引入，Sunny Cove 推广到可消掉连环 MOV（只受 rename 宽度限制）。影响不仅是省 ALU 口：被消的 MOV **不占调度器槽位、不占 ROB 发射周期、延迟为零**。

各家水平：

- [[golden-cove-microarchitecture|Golden Cove]] / Sunny Cove：连环都能消
- Zen 3 / Zen 2：与 Golden Cove 对等
- [[gracemont-microarchitecture|Gracemont]]：接近 Zen 2 水平，比同期 Atom 前辈跃升
- [[tremont-microarchitecture|Tremont]]：独立 MOV 可消，依赖链 MOV 偶尔成功但机制不靠谱
- Skylake / Haswell：只消部分场景

编译器（GCC/Clang/MSVC）会自觉生成易消的 MOV，Haswell 的 PMU 显示多数 MOV 实际被消掉——说明这是**编译器侧默契 + renamer 侧硬件约定**共同演化的结果。

## Zeroing Idiom Elimination

`XOR reg, reg` 或 `SUB reg, reg` 结果必为零，renamer 可以识别这类"自消"模式，直接分配一个零常量物理寄存器，免去依赖前值的真实计算。

- Golden Cove：**所有** zeroing idiom（包括 `MOV reg, 0`）都能识别并消掉，完全不占 ALU 口
- Zen 3：XOR/SUB 两类可消；`MOV reg, 0` 仍走 ALU（受 4 ALU 限）
- Gracemont：识别为独立但**仍占 ALU 口**（吞吐被 4/cycle 限制）
- Tremont：`xor r,r` 认得独立，但不消除

## 为什么算 renamer 的活

这两类消除都发生在 **rename/allocate 阶段**，不需要等操作数就绪。"rename 是前端到后端的桥"——在这里消掉的 uop 根本不进后端，既省后端资源（调度器、执行口、寄存器写回），也省误预测时的清理工作。这是"花前端的逻辑换后端资源"的典型手段，和 [[op-cache-decoded-uop-cache|op cache]] 的"花 cache 换解码功耗"一样，是现代核的必修课。

## 参见

- [[golden-cove-microarchitecture]]
- [[gracemont-microarchitecture]]
- [[tremont-microarchitecture]]
- [[zen2-microarchitecture]]
- [[cpu-scheduler-design]]
- [[op-cache-decoded-uop-cache]]

## Sources

- [[sources/chipsandcheese-golden-cove]]
- [[sources/chipsandcheese-gracemont]]
- [[sources/chipsandcheese-tremont]]
- [[sources/chipsandcheese-sunny-cove-intel-lost-gen]]
- [[sources/chipsandcheese-graviton3-first-impressions]]
