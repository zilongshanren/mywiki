---
tags: [硬件可靠性, 电压, 超频, 电迁移, mttf]
date: 2026-04-19
sources: 1
---

# 电迁移与电压退化：静态超频为何比动态 Boost 更危险

CPU 老化（degradation）不是一夜之间发生的黑白切换，而是一场由**电流密度、温度、时间**共同决定的连续进程。把这件事量化的经典模型是 **Black's Equation**：

```
MTTF ∝ 1 / ( Jⁿ · exp(−Ea / kT) )
```

平均故障前时间与电流密度的 n 次方成反比、与温度按 Arrhenius 指数衰减。电迁移（electromigration）的物理本质是金属互连里电子流把原子一点点挤走，在 [[memory-hierarchy|越现代、越密集的工艺]]上这件事越严重——TSMC N7 一类小节点本就把风险指针往右拨，此时如果再把电压/温度抬上去，**MTTF 的下降是超线性的**。

## 静态超频 vs 动态 Boost 的关键差异

现代 Ryzen 的 PBO 和 Intel Turbo Boost 本质上是**同时调频调压**：负载轻时单核拉到 1.45 V 都没事，因为只要多核负载一进来，电压自己就能掉到 1.10 V 甚至更低；温度一高，频率和电压都会往回缩。这让「最坏情况下的电流密度 × 时间」始终维持在较低的积分值。

而**静态超频工具（例如 CTR）**给出的 profile 就是一条固定曲线：`(freq, voltage)` 一旦设定，多核负载一起来也不会降——1.35 V 在 AVX Light 测试下也许能稳定，一旦跑 Prime95 small-FFT 或 LinpackXtreme 这类 AVX Heavy 工作负载，晶体管上承担的电流密度与热应力会瞬间飙升，而 profile 并不能自降。于是静态 OC 在「重度 AVX + 高核数 + 良好散热掩盖了温控问题」的组合里，反而成了**对 MTTF 最不友好的压力模式**。

## 「一年 1.55 V 才掉 100 MHz」——不是这样的

CTR 作者曾辩称「运行 1.55 V 跑一年最多掉 100 MHz」，社区主流意见并不认同。关键反驳有几点：

- **退化不是线性累积**：黑方程里 J 的指数 n 通常是 1–2，电流密度抬高 30% 就能把 MTTF 砍一半甚至更多。
- **单次高压暴露就可能造成不可逆损伤**：实测在 4650G 上被 CTR 瞬间推到 1.55 V（Renoir VID 表上限）之后，同电压下不再能跑原先稳定的 4.3 GHz——这是**单次会话造成的永久退化**。
- **TSMC N7 的 daily safe 电压**在 OC 社区里的共识是 1.35 V（激进 LLC）或 1.41–1.42 V（loyal/Auto LLC），1.55 V 已经完全越过安全区。

## 软件层的安全责任

一个面向非专业用户的「一键超频」工具，如果 **自动挡会越过它手册里自己定义的安全电压**，这就不只是性能问题，而是**危及用户资产**。CTR 这件事的核心争议不在它能不能榨出性能，而在它的 auto-tune 会静默把电压推到 VID 表上限（即 Renoir 的 1.55 V），而手册写明的安全上限是 1.35–1.42 V。对「一键」承诺来说，这种不一致比任何性能 benchmark 都重要。

## 对比参照：Intel 13/14 代退化事件

[[intel-13th-14th-gen-clock-degradation|Intel 13/14 代事件]] 是这件事的放大镜：主板厂默认 BIOS 配 500 A 电流限、253 W TDP 的芯片在近乎无限 boost 电压下长期跑，最终造成时钟树物理退化、shader 解压失败。那是**整个生态的静态 OC 默认化**（主板把 unbounded turbo 当默认），比一个第三方软件造成的个例影响大几个量级，但物理机理同源——电压 × 时间 × 温度在小节点上是不饶人的。

## 相关

- [[mttf-reliability]]
- [[intel-13th-14th-gen-clock-degradation]]
- [[dennard-scaling]]
- [[cpu-performance-formula]]

## Sources

- [[sources/chipsandcheese-ctr-safety-revisited]]
