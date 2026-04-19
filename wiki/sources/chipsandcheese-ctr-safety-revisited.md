---
tags: [source, chipsandcheese, 超频, 硬件可靠性, ryzen]
date: 2026-04-19
sources: 1
---

# CTR Safety, Revisited（Chips and Cheese）

[[chips-and-cheese]] 2021 年 2 月对 Clock Tuner for Ryzen (CTR) 安全问题的追踪报道。前一篇初评引爆社区争议后，编辑部做了第二轮测试，并引用 Black's Equation、AMD 官方声明、以及 Buildzoid/keeph8n/Brutus 等超频圈专家意见，形成一份更偏物理机理的复盘。本 wiki 聚焦其**电压退化与静态超频 vs 动态 Boost 的物理差异**部分，作为产品评测的争吵细节并不入库。

## 摘要

文章先指出 CTR 2.0 的 built-in 稳定性测试只支持 AVX Light 一档且无法切换到 AVX Heavy，因此在高核数 + 良好散热的配置下容易给出「看似稳定」的 profile；一旦跑 Prime95 small-FFT、LinpackXtreme、现代视频编码这类 AVX Heavy 负载，`1.25 V` 下可稳的 profile 换成 `1.35 V` 都未必挡得住。随后用 Black's Equation 拆解电迁移的物理模型，说明**静态超频** 设死的 `(freq, voltage)` 曲线和 PBO **动态 Boost** 会随温度/负载自降电压这件事有本质差别——前者在重负载下暴露给晶体管的电流密度与温度积分要大得多。作者驳斥了 CTR 作者「1.55 V 跑一年才掉 100 MHz」的辩解，实测证据是一颗 4650G 在被 CTR 一次推到 1.55 V 后，同电压下不再能稳 4.3 GHz。AMD 官方也给出声明：「唯一绝对安全的电压就是出厂电压」，并对 PBO 之外的第三方超频工具不做背书。

## 关键要点

- **Black's Equation**：MTTF 与电流密度 Jⁿ 成反比、与温度按 Arrhenius 指数衰减；小节点（TSMC N7）把起点推向更危险区。
- **静态 OC 最坏情况** 被工具本身的 AVX Light 测试掩盖——这是 CTR 问题的根因。
- **动态 Boost** 在多核负载下自降电压，所以 Ryzen 怠速看到 1.45 V 不是退化风险；静态 profile 在同样负载下不会降。
- **一次高压暴露可造成不可逆退化**：4650G 被推到 Renoir VID 表上限 1.55 V 后同电压无法维持原有稳定频率。
- **AMD 官方立场**：PBO 之外（甚至包含 PBO）的任何非出厂电压都不在保修范围；唯一「绝对安全」的是 stock 电压。

## 链接到的概念

- [[electromigration-voltage-degradation]]
- [[mttf-reliability]]
- [[intel-13th-14th-gen-clock-degradation]]

## 原文

- 链接：https://chipsandcheese.com/p/ctr-safety-revisited
- 本地：`raw/articles/chipsandcheese.com/2021-02-15_ctr-safety-revisited.md`
