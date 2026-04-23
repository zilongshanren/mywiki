---
tags: [cpu, 微架构, 前端, op-cache, uop-cache, 解码器]
date: 2026-04-19
sources: 3
---

# Op Cache（已解码微操作缓存）

Op cache 是一层位于传统 L1i + 解码器之后的 L0 指令缓存，直接存放解码后的微操作。命中时核前端无需重新取指与解码，可以更高带宽地灌入后端，同时让解码器整段时间空闲以省电。分支误预测恢复路径上若新目标在 op cache 中，还能省掉解码延迟，使误预测惩罚更短。

## 工业现状

AMD、Intel、ARM 的高性能核几乎都已采用 op cache：Intel 在 Sandy Bridge 上首次引入 DSB（称 Decoded Stream Buffer），Zen 1 起 AMD 跟进，ARM 在 Cortex-A77 加入 1.5k 条目的 op cache，A78/A710/X1/X2 延续，Samsung M5 也追加 op cache 主要理由同样是**省解码功耗**。[[zen2-microarchitecture|Zen 2]] 将容量从 Zen 1 的 2k 扩到 4k，Zen 3 保持 4k，足以覆盖多数实测 workload。

## 命中率的现实

厂商宣传往往引用"80–85% 命中率"这一数字，但 Chester Lam 在 3950X 上实测显示差异极大：CPU-Z / 3DPM v2.1 可超 90%（SMT 双线程共享同一 op cache 仍保得住），Cinebench 因代码体积更大降到 50–60%，编译 / Vray 这类后端受内存限制的负载既 L1i 命中率低、op cache 命中率也低——此类场景前端带宽本非瓶颈，更需要的是大 L1/L2/L3。

同一作者在 [[zen2-microarchitecture|Zen 2 vs Skylake]] 实测中还观察到一个反直觉结果：Skylake 的 1536 条目 op cache 在 CBR15 中命中率反超 Zen 2 的 4096 条目，说明**容量与命中率非单调关系**，替换策略与误预测路径污染同样关键。见 [[branch-predictor-design]]。

## 对性能与功耗的贡献

把 Zen 2 的 op cache 用未公开 MSR 位强制关闭后：

- Cinebench、3DPM v2.1 性能下降 >10%；即便解码器半数以上时间可空闲，关闭 op cache 后核功耗反升，因为前端喂得更饱、执行单元利用率更高。这反推出**解码器本身功耗很低**。
- Y-Cruncher op cache 命中率近 70%，但性能增益有限——核大量时间等数据，前端带宽非瓶颈。
- Vray、代码编译几乎感受不到差别，前端压根不紧。

作者进一步用 CPU-Z 单线程场景做解码器功耗隔离（>99% op cache 命中、分数几乎不变），估出解码器在核功耗里仅占 ~4%（约 0.24 W），对 package 功耗的影响 <1%。

## ARM 也付一样的税

曾有一种说法：x86 变长指令解码是 "decode tax"，ARM 定长指令因此更省电。[[isa-implementation-not-architecture|这种说法并不成立]]。ARM 高端核为省解码功耗主动引入 op cache，说明 ARM 解码同样昂贵；A64FX 手册显示不少 ARM 指令也被拆成多个微操作，极端案例 SVE FADDA 可解码成 63 个微操作。ARM 的 "RISC 优势" 在现代乱序核前已稀释殆尽。

## 参见

- [[zen2-microarchitecture]]
- [[branch-predictor-design]]
- [[isa-implementation-not-architecture]]
- [[dispatch-stall-breakdown]]

## Sources

- [[sources/chipsandcheese-zen2-op-cache-performance]]
- [[sources/chipsandcheese-isa-doesnt-matter]]
- [[sources/chipsandcheese-zen3-bottlenecks]]
