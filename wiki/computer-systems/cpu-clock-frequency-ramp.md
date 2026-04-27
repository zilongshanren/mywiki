---
tags: [cpu, power-management, clock-speed, boost, performance]
date: 2026-04-27
sources: 1
---

# CPU 时钟频率爬升行为

现代 CPU 不会常驻最高频率运行——为节省功耗和散热，它们会在空闲时降频，并在检测到负载后爬升回高频。从空闲到最高 boost 频率所需的时间直接影响系统的响应性，尤其对短任务（如单帧渲染、输入响应）至关重要。

## 爬升速度的决定因素

时钟爬升速度主要受限于两点：

1. **电源递送电路的斜率（Slew Rate）**：提高频率需先提高电压，电压调节器（VRM）需要时间完成充放电，这是最根本的物理约束
2. **功耗管理策略**：操作系统或 CPU 自身决定何时请求更高的 P-state

Intel 在 Skylake（2015）引入了 **Speed Shift**，将 P-state 控制权从操作系统转移给 CPU 硬件本身，使 Core i5-6600K 能在 5.62 ms 内达到最大 boost。Haswell/Sandy Bridge 时代需要 60-80 ms。

## 各架构实测对比

| 架构 | 平台 | 典型最大 Boost 时间 |
|------|------|-------------------|
| Intel Skylake（i5-6600K） | 桌面 | ~5.6 ms |
| AMD Zen 3 Cezanne | 移动 | ~2 ms（到 3.7 GHz） |
| AMD Zen 2 Renoir | 移动 | ~9 ms |
| AMD Zen 2 Matisse | 桌面 | ~17 ms |
| Intel Goldmont Plus | 低功耗 | ~47 ms |
| Intel Kaby Lake（i7-7700K OEM） | 桌面 | ~62 ms（可能受主板限制） |
| Intel Sandy Bridge Xeon HEDT | 工作站 | ~500 ms |
| Qualcomm Snapdragon 670 A75 | 移动 | 极快（几毫秒） |
| Zhaoxin LuJiaZui | 桌面 | 介于 Skylake 与 Goldmont 之间 |

## 关键观察

**电压是瓶颈**：AMD Piledriver（FX-8350）在 Windows 电源计划设置最低 CPU 状态为 100% 时（保持高电压待机），可以在不到 0.2 ms 内从 1.41 GHz 飞升至 4.1 GHz，证明大部分延迟来自等待电压建立。

**移动比桌面更快爬升**：受热功耗限制，移动 CPU 通常在响应速度上做了更多优化；Renoir（移动 Zen 2）比 Matisse（桌面 Zen 2）快约 2 倍。

**HEDT 有意降速**：Intel 历代 HEDT（Sandy Bridge-E、Haswell-E）爬升时间在数百毫秒级别，推测是有意为之，以避免短任务也消耗大量功耗。

## 测量方法

通过测量固定数量的串行整数加法（每时钟周期恰好完成一次）来推算时钟频率，用 RDTSC（x86）或 CNTVCT_EL0（ARM）代替 gettimeofday 以获得亚毫秒精度。

## 相关

- [[power-wall]]
- [[dennard-scaling]]
- [[intel-hybrid-alder-lake]]
- [[gracemont-microarchitecture]]
- [[via-x86-isaiah-lujiazui]]

## Sources

- [[sources/chipsandcheese-cpu-clock-ramp]]
