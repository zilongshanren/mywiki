---
tags: [source, chipsandcheese, cpu, isa, arm, x86, risc-cisc]
date: 2026-04-19
sources: 1
---

# ARM or x86? ISA Doesn't Matter（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 7 月发表于 [[chips-and-cheese]] 的立论文章，汇总 Jim Keller 访谈原话、Blem et al. 2013 HPCA、Hirki et al. 2016 USENIX、Oboril et al. 2015 DATE 等研究，加上 Chips and Cheese 自家对 Zen 2 的实测数据，正面反驳"ARM/x86 ISA 差异决定性能或能效"的流行观点。核心论点写进了本 wiki 的 [[isa-implementation-not-architecture]]。

## 摘要

作者分三层推进。首先援引 Keller 对 Anandtech 的访谈：限制现代 CPU 性能的是**可预测性**（分支与数据局部性），不是 ISA；RISC/CISC 老划分已因 x86 microcode ROM 缩到找不到而失效。第二层引研究：Blem et al. 跨平台比较发现 ARM 与 x86 性能差来自 ISA 无关的微架构取舍；Atom（x86 in-order）能在低功耗场景胜过 A9 印证 ISA 不绑功耗。第三层是 Chips and Cheese 自产证据：Zen 2 关掉 op cache 走解码器，核功耗仅 +4–10%、package 仅 +0.5–6%，部分场景反因前端喂不饱功耗还跌；Hirki/Oboril 对 Haswell/IvyBridge 独立得出解码器 3–10% 量级小头。ARM 阵营自己的选择也证实此点——A77/A78/X1/X2、Exynos M5 纷纷引入 op cache 省解码能耗，ThunderX3 的最大单项提升就是"降低 micro-op 扩展"，A64FX 多条 ARM 指令解码为多微操作，SVE FADDA 甚至拆到 63 条。最后作者承认两个真实例外：ISA 扩展（AVX/NEON/AES-NI）与生态软件优化——这是实测 Zen 2 视频转码领先 Ampere Altra 一个数量级的主因。

## 关键要点

- Keller：限制性能的是分支与数据局部性，不是 ISA
- Blem et al. HPCA'13：性能/能耗差距来自 ISA 无关微架构
- 关闭 Zen 2 op cache 核功耗 +4–10%、package +0.5–6% → 解码功耗是小头
- ARM 也靠 op cache 省解码：A77/A78/X1/X2、Samsung M5
- ThunderX3 over ThunderX2：6% 性能提升里最大单项是减少 micro-op 扩展
- A64FX 指令表显示 ARM 也有多微操作指令，SVE FADDA 解码为 63 µops
- ARM 不是纯 load-store：LDADD 解码为 4 µops
- 真实 ISA 差异：SIMD/加密扩展、生态软件优化（libx265 aarch64 起步晚）

## 链接到的概念

- [[isa-implementation-not-architecture]]
- [[op-cache-decoded-uop-cache]]
- [[zen2-microarchitecture]]
- [[neoverse-n1-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/arm-or-x86-isa-doesnt-matter
- 本地：`raw/articles/chipsandcheese.com/2021-07-13_arm-or-x86-isa-doesnt-matter.md`
