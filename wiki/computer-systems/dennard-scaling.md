---
tags: [计算机体系结构, 历史]
date: 2026-04-05
sources: 1
---

# Dennard Scaling（及其崩塌）

**晶体管越小越省电**——这个规律从 1970s 延续到 ~2004 年，然后**崩塌**了。

## 原理

Robert Dennard (1974)：晶体管尺寸缩小 k 倍时，电压也能缩小 k 倍，于是**单位面积功耗保持不变**——可以把更多更快的晶体管塞进同一芯片。

这是 CPU 频率从 1 MHz 爬到 3+ GHz 的物理原因。

## 崩塌（~2004）

**漏电流（leakage current）** 随晶体管尺寸缩小**相对变大**，静态功耗最终吞噬了电压缩放的收益。

## 后果：[[power-wall|功耗墙]]

频率在 **3-5 GHz 停滞**至今。单核速度不再自然提升，必须：

- **多核**：横向扩展。Amdahl 定律的战场变得重要。
- **SIMD**：向量化。
- **专用加速器**：GPU、TPU、DSP。
- **能效优先**：Apple M1 等。

## 历史意义

**Dennard Scaling 的终结**是软件工程范式转变的物理根源：
- 2004 前：免费午餐——等下一代 CPU 就好。
- 2004 后：必须**主动重写程序**才能利用新硬件。

Unity DOTS 的存在正是对此的回应。

## 相关

- [[power-wall]]
- [[amdahls-law]]
- [[cpu-performance-formula]]
- [[aos-vs-soa]]

## Sources

- [[sources/caqa-day02]]
