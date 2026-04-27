---
tags: [cpu, loongson, china, domestic-chip, microarchitecture, history, clock-speed]
date: 2026-04-27
sources: 1
---

# 龙芯历代架构轨迹

龙芯是中国最具代表性的国产通用 CPU 研发项目，由中国科学院计算技术研究所（ICT）孵化，后由龙芯中科技术有限公司产品化。通过逐代比较，可以清晰看到其长期存在的结构性短板：每周期性能（IPC）尚可，时钟频率长期落后，制造工艺与软件生态受制于外部因素。

## 历代核心数据

| 代际 | 核心 | 工艺 | 主频 | 同期对手主频 | 核心数 |
|------|------|------|------|-------------|--------|
| Godson-2（2003） | GS264，4-wide OoO | SMIC 180 nm | 434 MHz | AMD K8 2.2 GHz | 1 |
| Godson-2E（2006） | GS464，9 级流水 | ST 90 nm | 1 GHz | Intel Core 2 2.4 GHz | 1 |
| Godson-3（2008） | 4× GS464 | ST 65 nm | 1 GHz | Intel Nehalem 2.93 GHz | 4 |
| Godson-3B1500（2013） | 8× GS464GV | ST 32/28 nm | 1.5 GHz | Intel Haswell 3.5 GHz | 8 |
| GS464E（~2015） | 增强 OoO | 国产 40 nm | ~1 GHz | Intel Broadwell 3.5 GHz | 4 |
| LA464（3A5000，2021） | 全新微架构 | SMIC 12 nm | 2.5 GHz | AMD Zen 3 5 GHz | 4 |
| LA664（3A6000，2023） | IPC 大幅提升 | SMIC 12 nm | ~2.5 GHz | AMD Zen 4 5.7 GHz | 4 |

## 系统性问题分析

### 时钟频率瓶颈

龙芯历代频率提升远慢于 Intel/AMD。Godson-2E 在 90 nm 达到 1 GHz，之后十年几乎停滞。到 2024 年，LA664 在 SMIC 12 nm 上仅跑到约 2.5 GHz，而 AMD Zen 4 在 TSMC 5 nm 上可达 5.7 GHz。

问题根源有二：其一，每代架构升级时往往兼顾了 IPC 而忽视了关键路径优化（如 GS464E 时期）；其二，工艺节点质量受限——SMIC 12 nm 与 TSMC N7 有明显差距，而龙芯无法使用更先进节点。

### 制造工艺依赖

AMD 用 TSMC 5 nm（Zen 4），Intel 自建 Intel 18A 同时使用 TSMC N3。即便如此两者仍无法在工艺上领先龙芯太多——龙芯的真正劣势是无法选择最优工艺，而必须使用国内可用的节点（目前以 SMIC 12 nm 为上限）。全球化分工让各国专注特定领域；龙芯必须"全栈国产"，势必分散资源。

### 核心数落后

2024 年，龙芯 3A6000 仍是四核，而 AMD Ryzen 7700X（$300）已是八核，7950X 提供 16 核。现代应用日趋多线程化，核心数量差距对实际性能影响远超 IPC 差距。

扩展核心数还需要灵活的片间互联。龙芯早年使用 HyperTransport（2010 年前的技术）实现多核簇互联，但导致 NUMA 拓扑，而 AMD/Intel 已能在单 die 上集成 16 核 UMA 配置。

### 软件生态

龙芯存在两套不兼容的 Linux 发行版，应用层面缺乏优化。以 LBrowser v3（Chromium 衍生）跑 Speedometer 3.0 为例，得分约为 AMD 3950X 的 1/4.8——差距远超硬件 IPC 比值（LA664 与 Zen 2 的 IPC 差约 40%），额外的软件未优化损失才是主因。x86 二进制翻译进一步损耗本就不宽裕的性能余量。

## 龙芯的比较优势

龙芯并非一无是处。在相同频率下，历代 IPC 均属合理水平：Godson-2 与同期 K8 单周期性能差距不大；LA664 的 IPC 接近 Zen 2 的水平。龙芯工程师显然对微架构技术有足够的掌握，从未沦落为"买图纸"层面的团队。

其低功耗特性（Godson-2 仅 2-3 W）也有市场价值——嵌入式与工控市场对绝对性能要求较低，对功耗和供应链安全更敏感。

## 前景

频率问题与核心数问题的解法高度依赖工艺节点突破。在此之前，龙芯在通用计算市场（桌面、服务器）与 AMD/Intel 的差距难以缩小。参见 [[loongson-3a5000-microarchitecture]] 了解最新架构细节。

## Sources

- [[sources/chipsandcheese-loongson-vs-west]]
