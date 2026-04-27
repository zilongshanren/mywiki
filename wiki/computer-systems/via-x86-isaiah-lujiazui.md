---
tags: [cpu, 微架构, x86, via, zhaoxin, isaiah, lujiazui, low-power]
date: 2026-04-19
sources: 2
---

# VIA 与兆芯（Zhaoxin）的 x86 血脉：Isaiah 与 Lujiazui

x86 生态里除了 Intel 与 AMD 还有第三方：VIA。VIA 同时收购了 Cyrix（从 National Semiconductor）与 Centaur（从 IDT），最后保留 Centaur 的 Samuel 核心一路演化成 C3/C7。2008 年 VIA 用 Isaiah 核心全面替代 Samuel 家族，把目标放在低功耗市场。Isaiah 延伸出与上海市政府合资的兆芯（Zhaoxin），后者以 Zhangjiang（换了中国国密 SM3/SM4 的 Isaiah II 小改）→ Wudaokou（IPC +25%）→ Lujiazui（HLMC 28nm 改 TSMC 16nm，时钟 + 50%）三代逐步演进。

## Isaiah：名为「低功耗」，实则重装

George Cozma 拆开 2008 年发布的 VIA Nano（Isaiah）后给出的判断是：**放错了赛道**。对比指标触目惊心——

- **前端**：3-wide 解码（低功耗 x86 里直到 2016 年 Goldmont 才追上），4096 项 4-way BTB（Intel 要等到 2011 年 Sandy Bridge 才铺同规模），tournament 式方向预测器（3 条 BHT + 1 条 meta），模式识别能力压过同代 Core 2。代价是每三周期才能吞一条 taken 分支，靠尺寸换精度。
- **后端**：65 项 ROB（Bobcat 晚 3 年才做到 56），46+48 独立整数/FP 寄存器文件，Media A/B 两条 128-bit SIMD 管道与 Core 2 看齐，FP add **2 cycle** 延迟（至今无人能复制）。L1D 64 KB 16-way、2 cycle 延迟——同代普遍 3 cycle。
- **结果**：Nano 发热跟同代 Core 2 Duo 差不多，能维持咖啡微温；低功耗定位名不副实，又跑不赢 Core 2。Isaiah 的 Media 单元疑似为视频解码而设，但硬件解码器很快普及，优势消失。

Isaiah 说明一件事：[[branch-predictor-design|分支预测]]做太精、L1D 做太低延迟，功耗必然超支——AMD 此后数代都在缩减前端气泡而非扩大预测表。

## Lujiazui：反向工程——把 Isaiah 砍窄

兆芯的 Lujiazui 呈现与 Isaiah 相反的权衡：

- **解码收窄到 2-wide**、rename/retire 也随之 2-wide。ROB 缩回 48 项，且退回 P6 式 ROB+RRF（ROB 槽与寄存器文件合一），整数与 256-bit AVX 共用同一份寄存器。
- **缓存层次重排**：L1 从 64 KB 砍到 32 KB，4 核共享 4 MB L2（类似 Zen 1/2 APU 的 LLC 布局），内存控制器上 die 取代 FSB。
- **分支预测**：加了 16 项 L0 BTB 做零气泡 taken 分支（类似 Zen 2），但主 BTB 仍是 4096 项 + 2 气泡惩罚，方向预测器几乎没升级。L1 return stack 仅 2 项、L2 return stack 13–16 周期延迟——深嵌套调用堪比 Haswell 栈溢出。
- **AVX 聋哑**：256-bit AVX 拆成两条 128-bit 微操作消耗双 ROB 槽，且有额外延迟惩罚——不像 Piledriver/Zen 1 的拆分是平价的。加上 ROB 小，256-bit AVX 场景 reordering 容量腰斩。AVX2 的 FMA 直接 fault；官方说不支持 AVX2，但 256-bit 整数加法意外能跑。
- **不做 memory dependence prediction**：load 不能越过地址未知的 store，这是 Core 2（2006）首发的老功能。

Lujiazui 的目的很明确：**为了塞 8 核**，牺牲单核宽度换面积和功耗（类似 ARM A72 → A73 的缩窄策略）。25% 十年 IPC 涨幅追不上 Intel 或 AMD；时钟 50% 涨幅靠工艺。总结：**Nano 是伪装成低功耗核的大核，Lujiazui 是伪装成大核的低功耗核**——比较对象应该是 Jaguar 或 Goldmont，不是 Zen 2。

## 参见
- [[branch-predictor-design]]
- [[isa-implementation-not-architecture]]
- [[zen2-microarchitecture]]
- [[neoverse-n1-microarchitecture]]
- [[op-cache-decoded-uop-cache]]
- [[x86-simd-integer-multiplies]]
- [[golden-cove-microarchitecture]] — 同期 Intel 大核的另一极：把结构堆到极限
- [[gracemont-microarchitecture]] — 现代 Atom 走向：宽乱序 + 共享 L2

## Sources
- [[sources/chipsandcheese-via-isaiah]]
- [[sources/chipsandcheese-zhaoxin-lujiazui]]
- [[sources/chipsandcheese-zhaoxin-part3]]
- [[sources/chipsandcheese-via-centaur-cns]]
