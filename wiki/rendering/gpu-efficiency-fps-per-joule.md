---
tags: [gpu, 能效, power, 架构对比, turing, ampere, rdna1, rdna2, vega]
date: 2026-04-19
sources: 1
---

# GPU 能效：按 FPS/Joule 拆 Turing / Ampere / RDNA

Serebit 2021 年 9 月给出的横测基线用的是**每瓦帧数**（Frames per Watt，等价于 Frames per Joule, f/J）。数据来自 TechPowerUp 与 Tom's Hardware 两套公开 GPU 评测的几何平均——自家没有实测条件，就找两家大站拉齐做 sanity check。单项 SKU 会有差异，但用来看**架构层面的能效分布**已经够用。

## 四档分辨率画像

方法锁定 1080p / 1440p / 2160p 三档：

- **Vega 20（Radeon VII）**在所有分辨率都贴底——0.456 f/J @ 1080p；HBM2 带宽再多也救不回 14nm 年代设计的能耗。
- **Turing RTX** 基本聚在 0.61 f/J 附近（2080 Super 被推到 0.567，2070 疑似部分屏蔽）。GTX 1660 Ti 则因为多 shader、低频反而坐上 Turing 能效王座（0.701 f/J @ 1080p），这是"把硅片推回甜点"的典型案例。
- **RDNA1** 在 0.55–0.67 区间，5500 XT 是低位（小 die 没压住），5700 非 XT 靠低频坐稳 RDNA1 榜首。
- **Ampere** 是最复杂的样本——**GDDR6X 型号（3080/3080 Ti/3090）在 1080p 贴底**，因为 GDDR6X 本身就吃 60 W 级电，同时 shader 过剩 occupancy 拉不满；换成 GDDR6 的 3070/3060 Ti 直接飙到 0.738 f/J 榜首。
- **RDNA2** 最稳——最差的 6800 XT 仍接近 5700；6800 是综合头名（0.757 f/J @ 1080p），6600 XT 在 1080p 登顶（0.798 f/J）但 2160p 因 128-bit 总线 + 32 MB L3 不够用断崖式回落。

## 三条方法学教训

1. **分辨率对架构排序会重新洗牌**。GDDR6X Ampere 在 1080p 吃亏、4K 翻盘（shader 利用率终于接近 peak）；低位宽 + 小缓存的 6600 XT 与 1650 Super 在 4K 崩盘。**"每瓦帧数"这一个数字不存在——至少要分 1080p/1440p/2160p 三条**。
2. **显存才是显性能耗项**。GTX 1660 与 1660 Super 除了 VRAM 毫无区别（GDDR5 vs GDDR6），但仅换显存就把 f/J 从 0.63 推到 0.674——显存带宽瓶颈的隐形能耗税很重。GDDR6X 在 1080p 的损失更直白。
3. **"架构低效"要和"SKU 推到墙"分开看**。RX 5700 XT 与 RTX 2080 Super 都属于把 die 推到超出甜点的例子，把它们拿去代表架构能效不公允。

## 对 PC 架构讨论的意义

能效曲线不是「Nvidia > AMD」或反之的单句结论——[[samsung-8n-vs-tsmc-n7|Ampere 用三星 8N 还是 TSMC N7]] 决定了 20% 能效；**memory subsystem**（GDDR6/6X、[[mcm-gpu-design|L1.5 / Infinity Cache]]、带宽总线宽）吃掉另一大块；剩下才轮到 shader / RT / tensor 核的微架构效率。

Serebit 在结语里强调这只是"第 I 部分，只谈功率"。后续 Part II 讨论带宽维度的能效，同属 [[chips-and-cheese]] 对 GPU 架构"拆因子"的一贯风格。

## 参见

- [[samsung-8n-vs-tsmc-n7]]
- [[ampere-warp-stall-utilization]]
- [[rdna1-overclocking-navi10]]
- [[gpu-memory-hierarchy-latency]]
- [[electromigration-voltage-degradation]]

## Sources

- [[sources/chipsandcheese-video-card-efficiency-power]]
