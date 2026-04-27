---
tags: [source, chipsandcheese, cpu, amd, zen5, clock-for-clock, ipc, benchmark, branch-prediction]
date: 2026-04-27
sources: 1
---

# Zen 5 Variants and More, Clock for Clock（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 8 月的文章，将多款 CPU（从 Athlon II X4 651 到 Zen 5）强制锁定在 3 GHz 进行横向对比，消除频率差异后评估纯 IPC 与架构效率，并用 libx264、7-Zip 两个工作负载加深分析分支预测和前端/后端停顿的影响。

## 摘要

本文是一项刻意"无实际意义但很有趣"的对比实验。降频至 3 GHz 可将 DRAM 延迟的周期代价减半，从而降低内存延迟对乱序执行效率的干扰，让架构本身的特性更清晰地浮现。核心结论：桌面版 Zen 5 在 libx264（AVX-512 重度）领先移动版 Zen 5 约 20%，但 7-Zip（延迟敏感）中移动版因更高 LPDDR5 延迟而明显落后。文章还系统比较了各代分支预测精度（MPKI）：7-Zip 分支密集，即使 Zen 5 达到 96% 准确率仍有 8.9 MPKI，限制了大乱序窗口的有效利用。最终结论是：CPU 性能的本质瓶颈始终是"可预测性"——分支/指令可预测性和数据局部性，这一点跨十年未变。

## 关键要点

- 3 GHz 统一时钟下：desktop Zen 5 > Zen 4 VCache ≈ Zen 4 vanilla > mobile Zen 5（libx264）；7-Zip 中 mobile Zen 5 因 LPDDR5 延迟而明显落后
- Zen 5 移动版的 IPC（instructions per cycle）与 Zen 4 桌面版接近，说明架构改进补偿了移动平台的内存劣势
- Intel Redwood Cove（Meteor Lake P-Core）在 7-Zip 中与 Zen 5c 接近；Crestmont E-Core 连 Zen 2 / Skylake 都够不到
- 分支预测准确率：内核编译 > libx264 > 7-Zip；7-Zip 中 Zen 5 约 96% 准确率、8.9 MPKI，Zen 4 约 9.3 MPKI
- 7-Zip 全程适配微操作缓存，但 taken branch 频繁导致 fetch 组槽位浪费，前端仍成瓶颈
- 内核编译：极度前端受限；L1i 溢出是主要原因，Apple/Qualcomm 用 192 KB L1i 应对，Zen 5 的 32 KB 仍嫌不足

## 链接到的概念

- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/redwood-cove-microarchitecture]]
- [[computer-systems/crestmont-microarchitecture]]
- [[people/chester-lam]]

## 原文

- 链接：https://chipsandcheese.com/p/zen-5-variants-and-more-clock-for-clock
- 本地：`raw/articles/chipsandcheese.com/2024-08-20_zen-5-variants-and-more-clock-for-clock.md`
