---
tags: [渲染, 辐射度量, 物理渲染, 路径追踪, 数学]
date: 2026-04-19
sources: 1
---

# 以积分视角理解辐射度量（Radiometry）

[[christoph-peters|Christoph Peters]] 的「Radiometry, part 1: I got it backwards」提出了一种和主流教科书相反的讲法：**不从 radiant energy 起步、不用 differential 记号**，而是**从 radiance 起步、用积分向其它量推导**。这对写路径追踪器的人特别友好——path tracer 本来就在算各种积分，用积分定义的量可以直接对号入座。

## 传统讲法的困惑

PBRT 等教材的讲法：从 radiant energy $Q$（焦耳）开始，定义 flux $\Phi = \mathrm{d}Q/\mathrm{d}t$，然后 irradiance $E = \mathrm{d}\Phi/\mathrm{d}A$，再 radiance $L = \mathrm{d}^2\Phi / (\mathrm{d}A\,\mathrm{d}\omega\cos\theta)$。问题是 $\mathrm{d}\Phi / \mathrm{d}A$ 不是高中学的那种导数——$\Phi$ 不是 $A$ 的可微函数，它依赖**一整片区域的选择**。这个记号传达了直觉但不严谨。

## Peters 的积分式重构

### 第一公民：Radiance $L(x, t, \omega)$，单位 $\mathrm{W}/(\mathrm{m}^2\,\mathrm{sr})$

**定义**：想象一个无透镜、零曝光时间、零像素面积的理想相机。它在点 $x$、时刻 $t$、朝向 $\omega$ 读到的值就是 radiance。直觉上**就是相机像素数值**的物理对应（linear、无 DoF、无 motion blur）。

关键性质：**真空中 radiance 沿射线守恒**：$L(x, t, \omega) = L(x + s\omega, t, \omega)$——这正是 ray tracing 作为渲染手段的物理依据。

### 所有其它量都是对 radiance 做积分

- **Irradiance**：$E(x, t, n) := \int_{\mathbb{S}^2} L(x, t, \omega)\,|n \cdot \omega|\,\mathrm{d}\omega$——「一个朝向 $n$ 的 Lambert 表面能收到多少光」。
- **Radiant flux**：$\Phi_A(t) := \int_A E(x, t, n(x))\,\mathrm{d}x$——「整个表面 $A$ 收到多少光」，光源标定常用。
- **Radiant energy**：$Q_A(t_0, t_1) := \int_{t_0}^{t_1} \Phi_A(t)\,\mathrm{d}t$——「某时段内总能量」，连接到 SI 的焦耳。
- **Radiant intensity**：$I_A(t, \omega) := \int_A L(x, t, \omega)\,|n(x) \cdot \omega|\,\mathrm{d}x$——沿一个方向的总辐射（IES profile 就是 luminous intensity 的空间化查找表）。

## 常见渲染错误的诊断

Peters 指出写 path tracer 的两大偏差来源：

1. **Monte Carlo / 重要性采样错了**——收敛慢或收敛到错误值。
2. **根本没在算正确的积分**——radiometric quantity 搞错了。

比如 area light 的强度如果用 irradiance 定义，缩放 light 面积时总能量会变。用 flux（瓦）定义就和现实生活里「选灯泡看 lm」对齐，光源大小不改能量。

「要不要乘 cos」、「要不要除 $4\pi$ 或 $r^2$」这类问题，只要**把每一个量写成积分**、看清楚积分域是什么、$\cos$ 是怎么进去的，就能自动给出答案。

## 对渲染器的启示

- **写 path tracer 时只用 radiance 就能自洽**：射线只需要携带 $L$，无需概念上在 flux、irradiance 之间来回。
- **和 [[spectral-rendering|spectral rendering]] 的衔接**：所有 radiometric 量都有 spectral 版本（对波长再加一维 CDF），Peters 的 Part 2 会在此基础上引入 [[photometry-luminance|photometric 量]] 和光谱化。
- **cosine law 不是魔法**：$|n \cdot \omega|$ 在 irradiance 定义里就是几何原因（beam cross-section / lit area），不是「为了模拟 Lambert 反射」而事后加的。

## 相关

- [[christoph-peters]]
- [[spectral-rendering]]
- [[photometry-luminance]]
- [[path-tracing-basics]]
- [[microfacet-brdf]]

## Sources

- [[sources/peters-radiometry-1-backwards]]
