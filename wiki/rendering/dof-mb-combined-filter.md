---
tags: [渲染, 后处理, 景深, 运动模糊, 可分离卷积]
date: 2026-04-27
sources: 1
---

# DOF 与运动模糊联合后处理滤波器

景深（Depth of Field, DOF）与运动模糊（Motion Blur, MB）在后处理管线中通常分开实现，但两者在数学本质上是**同一积分的不同维度采样**：DOF 是相机胶片平面上的空间积分，MB 是时间轴上的积分。这一对称性暗示可以用单一的椭圆滤波基（basis）统一处理两者。

[[angelo-pesce]] 在 2012 年独立推导了这个联合方案，与 Crytek 在 SIGGRAPH 2011 公开的思路相似但实现路径不同。

## 联合核心思想

将 DOF 的圆形采样核和 MB 的线性方向结合：以运动方向向量为第一轴，以 DOF 量为半径的垂直方向为第二轴，构成一个**2×2 旋转基矩阵**，所有样本在这个椭圆核上采集。当 MB=0 时椭圆退化为圆（纯 DOF），当 DOF=0 时退化为线段（纯 MB）。

```hlsl
float2 MB_axis  = (currentViewPos - previousViewPos) * MB_MULTIPLIER;
float  DOF_amt  = ComputeDOFAmount(depth);
float  DOF_MB_ratio = DOF_amt / (length(MB_axis) + EPS);
float2 DOF_axis = MB_axis.yx * float2(1,-1) * DOF_MB_ratio;
// 组合成椭圆的两个对角轴
float4 basis = DOF_axis.xyxy + MB_axis.xyxy * float4(1,1,-1,-1);
```

当 MB 向量过短无法构成有效基时，插值回纯圆形 DOF 核。

## Gather-as-Scatter 权重

普通 gather（以当前像素的核大小采集周围样本）在大脱焦区域向焦内区域扩散时会失败——焦内像素的核很小，根本不会去采集周围大半径的散射贡献。

更物理正确的策略是 **gather-as-scatter**：判断候选样本点的散射核半径是否能"覆盖"当前距离，再决定是否贡献：

```hlsl
half weight = saturate(maxLengthAtSample - currentLength) * kernelWeight[i];
```

这等效于问"该样本的散射会到达我这里吗"，而非"我需要从那里采集吗"。

## 可分离滤波

Crytek 方案使用圆形多采样（N 个 tap）。Pesce 改用**可分离两 pass**，沿两条斜对角轴各做一次 1D blur。代价：纯 MB 场景下两轴方向相同，通过使两轴分别偏转 ±MB 方向避免退化，以略微不同的过滤覆盖提升有效采样密度。

## 预 pass：散射半径扩散

在正式 blur 之前，需要一个轻量的 gathering-as-scattering 预 pass：以较小的固定半径搜索周围，把能影响当前像素的最大散射半径写入辅助 buffer。类似 Percentage Closer Soft Shadows（PCSS）的思路：先算"最大遮蔽半径"，再用它驱动实际 blur。这样正式 pass 就能以可分离方式处理而不遗漏大半径散射。

## 与其他 DoF 方案的关系

| 方案 | 核形状 | 实现方式 | 参考 |
|---|---|---|---|
| Crytek SIGGRAPH 2011 | 圆形→椭圆 | 圆形 N tap | 与 Pesce 方案思路相同 |
| Pesce 2012 | 圆形→椭圆 | 可分离两对角 1D pass | 本页 |
| [[circular-separable-dof\|Garcia/Frostbite]] | 圆盘（复数核） | 可分离复数卷积 | FIFA 17 等 |
| [[scatter-bokeh-dof]] | 任意形状（精灵散射） | GPU 粒子 scatter | Witcher 2 路线 |

## 相关

- [[circular-separable-dof]]
- [[gather-bokeh-dof]]
- [[scatter-bokeh-dof]]
- [[variable-size-gather-dof]]
- [[motion-vectors]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-current-gen-dof-mb]]
