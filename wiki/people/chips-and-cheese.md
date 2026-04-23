---
tags: [人物, 作者, collective]
date: 2026-04-19
sources: 5
---

# Chips and Cheese（集体作者）

Chips and Cheese 是一个聚焦于 CPU/GPU 微架构实测分析的独立技术博客，Substack 发表。核心作者包括 [[chester-lam]]（主笔，贡献大量缓存/内存/互连延迟带宽测试）、George Cozma、Clam 等，以 Nemes 的 Vulkan 微基准套件、自研 pointer chasing 测试为主要工具。风格偏实测数据，几乎每篇都带厂商 performance counter 解读。

## 常见研究题材

- CPU 核心微架构深挖（Zen 5、Lion Cove、Cortex X925、Bulldozer）
- 缓存/内存子系统时延带宽曲线
- 互连、chipset、PCIe 延迟
- GPU 架构分析（Blackwell、RDNA3.5、Arc）
- 原子操作、cache coherence 边角用例

## 相关
- [[chester-lam]]
- [[gb10-memory-subsystem]]
- [[gb10-gpu-blackwell-igpu]]
- [[chipset-pcie-latency]]
- [[split-lock-x86]]
- [[llm-generated-c-compiler-perf]]
- [[blueswordm]]
- [[jpeg-codec-pipeline]]
- [[cpu-gpu-platform-security-features]]
- [[electromigration-voltage-degradation]]
- [[george-cozma]]
- [[jeremy-tingle]]
- [[apex-chipsandcheese]]
- [[rdna1-overclocking-navi10]]
- [[ampere-warp-stall-utilization]]
- [[samsung-8n-vs-tsmc-n7]]
- [[gpu-driver-support-lifecycle]]
- [[core-to-core-latency-lock-test]]
- [[op-cache-decoded-uop-cache]]
- [[isa-implementation-not-architecture]]
- [[dispatch-stall-breakdown]]
- [[neoverse-n1-microarchitecture]]

## Sources
- [[sources/chipsandcheese-gb10-cpu-memory]]
- [[sources/chipsandcheese-gb10-gpu]]
- [[sources/chipsandcheese-chipset-microbench]]
- [[sources/chipsandcheese-ccc-april-fools]]
- [[sources/chipsandcheese-split-locks]]
- [[sources/chipsandcheese-nvidia-mcm-gpu]]
- [[sources/chipsandcheese-jpeg-image-compression-overview]]
- [[sources/chipsandcheese-security-overview]]
- [[sources/chipsandcheese-ctr-safety-revisited]]
- [[sources/chipsandcheese-zen2-op-cache-performance]]
- [[sources/chipsandcheese-isa-doesnt-matter]]
- [[sources/chipsandcheese-zen3-bottlenecks]]
- [[sources/chipsandcheese-neoverse-n1-vs-zen2]]
- [[sources/chipsandcheese-gigabyte-zen4-leak]]
