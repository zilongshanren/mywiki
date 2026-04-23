---
tags: [渲染, 路径追踪, GPU, 实时渲染, 引擎]
date: 2026-04-19
sources: 1
---

# Brigade 引擎（实时路径追踪）

Brigade 是 [[jacco-bikker|Jacco Bikker]] 主导的实时[[path-tracing-basics|路径追踪]]引擎线，2010 年首次以**游戏场景下带动态全局光照**的形式在 YouTube 亮相。后来发展为 Brigade 2、Brigade 3，被 OTOY 收入商业化管线；学术线延续成 [[lighthouse-2-optix|Lighthouse 2]]。

## 2010 年的原型

[[sam-lapere|Sam Lapere]] 2010-04 的博客记录了一则决定性的演示视频：

- **硬件**：Core i7（四核）+ GTX 260，CPU/GPU 混合架构
- **性能**：~40 Mrays/s，每帧 8 spp
- **场景**：一个动态浮动物体 + 反射环/立方体/柱体产生焦散、运动模糊
- **后处理小技巧**：对最近 4 帧做样本平均（只在相机静止时有效），相当于把有效采样数翻到 32 spp，噪声按 1/√N 下降

Lapere 读到 reddit 上的数学解释后补了一段：由于路径追踪无偏，噪声方差随样本数呈 1/N（std 按 1/√N）下降，多帧累积在静止相机下合法，本质就是拉长了积分时间。

## 为什么是分水岭

2010 之前那些打着"游戏实时光线追踪"旗号的演示——Quake 3/4/Wars raytraced、Intel Larrabee Quake Wars、Outbound、NVIDIA Bugatti、Let there be light——都只做 **Whitted 光线追踪**：只有直接光 + 完美反射 / 折射，**光照平淡**，质量上反而比光栅化的 SSAO / SSGI / baked GI / Crytek LPV 要差。Brigade 直接跳到**路径追踪**，把软阴影、多次反弹间接光、焦散、景深、运动模糊全部"自动化"——这是它跟同期那些 tech demo 的本质差别。

它同时揭示了后来十多年实时路径追踪的核心工程命题：**采样数 × 时间积分 × 降噪**。Brigade 用帧间平均凑 spp，日后 NVIDIA 的 RTX 用 temporal accumulation + ReSTIR + [[path-tracing-monte-carlo|Monte Carlo]] 降噪网络，思路一脉相承。

## 相关

- [[jacco-bikker]]
- [[lighthouse-2-optix]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[gpu-unbiased-path-tracing]]
- [[sam-lapere]]

## Sources

- [[sources/raytracey-bikker-pathtracing-demo]]
