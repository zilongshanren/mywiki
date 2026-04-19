---
tags: [visualization, fluid-dynamics, debug]
date: 2026-04-19
sources: 1
---

# 流体流场可视化

研究流体时最大的工程障碍不是方程而是**看不见**——空气与水都透明，压力场与速度场都是抽象数值。[[bartosz-ciechanowski]] 在 [[airfoil-lift-physics|Airfoil]] 一文中系统展示了三种互补的可视化方案，它们几乎就是物理仿真、CFD、流体渲染、shader debug 的通用工具包。

## Eulerian 箭头场

在空间中均匀撒下观察点，每个点标注该时刻的瞬时速度向量（方向 + 长度）。优点：覆盖整片区域、同步呈现全场结构；缺点：粒子本身不动，很难建立「这一口气从哪来」的直觉。适合看稳态流场、涡结构的瞬时形态。

## Lagrangian 粒子 marker

撒入大量轻质粒子，让它们随流场运动。粒子足够小、足够轻，能近似认为随流体元共动。优点：直观呈现**轨迹**，加上拖尾 ghost trail 可以看到「这股气来自哪」；缺点：粒子会聚集（涡核）或发散（源），某些区域得重新补粒子；算法上需要每步一个积分步（Euler / RK4）。

在 shader 里，这就是各种 flow-map 纹理采样、VFX 粒子系统的底子；在 [[bluk-2d-fog-sprite-shader]] 这类 2D 雾效果里，开发者往往只是用静态 flow 纹理驱动随机分布的粒子，本质是同一个 Lagrangian 思想的廉价版本。

## 标量色图

把每个点的**某个标量**（通常是速率 |v|，有时是压强、涡量、温度）映射为色带。优点：能看清梯度、锋面、分离线；缺点：丢掉方向信息。常和箭头场叠加使用：色图给「多快」，箭头给「往哪」。

## 为什么要三种一起用

- 箭头负责**空间全景**（哪里快哪里慢）；
- marker 负责**时间轨迹**（空气往哪走）；
- 色图负责**标量梯度**（在哪里发生骤变）。

Ciechanowski 的交互 demo 通常默认三个同时开。这种「三表示同构」思路在渲染领域也有强共鸣——颜色通道、深度、motion vector 常常要并排查看才能 debug TAA 鬼影或 volumetric fog 漏光。

## 与渲染/shader 领域的连接

- **[[motion-vectors]]**——屏幕空间的 Eulerian 速度场，就是箭头场的 per-pixel 化；
- **[[volumetric-fog-froxels]]**——用 Lagrangian 方式在 froxel 内追踪散射体；
- **[[turbulence-domain-warping]]**——把 Lagrangian 扰动写进 shader 查表；
- flow-map 纹理（水流、岩浆）——对 marker 思路的烘焙版本。

## Sources

- [[sources/ciechanow-airfoil]]
