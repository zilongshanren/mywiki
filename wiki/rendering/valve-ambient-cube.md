---
tags: [渲染, 环境光, 光照, 球谐]
date: 2026-04-14
sources: 1
---

# Valve Ambient Cube（六面常数环境光）

**Valve Ambient Cube** 是 Valve 为 Half-Life 2 的 Source 引擎开发的一种**紧凑环境光表示**，用**六个颜色常数**（世界空间 +X/-X/+Y/-Y/+Z/-Z 六个方向的平均环境辐亮度）代替更昂贵的 [[spherical-harmonics|球谐系数]]，在动画物体上做 per-vertex 或 per-pixel 的漫反射环境光评估。2006 年 Valve 在 SIGGRAPH 的《Shading in Valve's Source Engine》课程里公开了这个 trick，之后被大量 2000s–2010s 的 AAA 引擎复用。

## 求值公式

给定世界空间法线 `n`：

```
n² = n * n                // 分别对 +/- 通道算
L_pos = cubePos.x·n²_x + cubePos.y·n²_y + cubePos.z·n²_z
L_neg = cubeNeg.x·n²_x + cubeNeg.y·n²_y + cubeNeg.z·n²_z   // n 为负分量时
ambient = L_pos + L_neg
```

也就是把法线分成 `saturate(n)` 与 `saturate(-n)` 两份，分别和**正向三色**与**反向三色**做内积。六个 `cubePos/cubeNeg` 常数就是「六个方向的代表性环境色」。在 HLSL/shader 汇编里几乎只是 6 条 mad 指令——远比最低阶 SH（9 系数，3 通道共 27 个浮点）便宜。

## 为什么只存六个

从信号处理角度，这等价于把环境光投影到**六个轴向余弦平方**基——一个非正交但覆盖球面的简单基。精度逊于 SH，但：

- 存储从 SH 的 9 路下降到 6 路
- shader 求值便宜一个数量级（无矩阵乘、无点积展开）
- 艺术家可以**手调**六个常数做 dramatic lighting，而 SH 的系数几乎无法凭直觉编辑

代价是**丢失方向的高频细节**——Ambient Cube 本质是一个「平滑到只剩六个方向」的球形探针，做不了像低阶 SH 那样的镜面暗示。

## 谁在用

- **Half-Life 2 / Source 引擎**（2004）——动画角色在静态 Lightmap 世界中的环境光
- **Castlevania: Lords of Shadow 2**（2014）——[[sources/elopezr-clos2-rendering|MercurySteam Mercury 引擎]] 对动画几何的环境光就是 Ambient Cube，配合 DX9 shader 汇编里一段非常典型的 `sqPosNormal * PreCalcAOColors` 结构被 Emilio López Ros 逐字解出来。静态几何走传统 lightmap，动画几何走 Ambient Cube（或者叫「light probe」的实际实现）
- 许多 2005–2012 年使用自研引擎的 PS3/Xbox 360 游戏——对着色器预算极其敏感，Ambient Cube 常被当作 [[spherical-harmonics|SH]] 的「穷人替代方案」

## 和球谐的关系

低阶球谐（L2，9 系数）是方向光的**正交**投影，数学更优雅；Ambient Cube 是**非正交**投影到 6 个轴向基，牺牲精度换指令数和存储。两者的哲学差别很像 [[needlets]] 和 SH 的差别——**紧支撑 + 局部可控**胜过全球正交的简洁。

现代引擎（UE4/5、Unity HDRP）更倾向于直接用 L1/L2 SH，或者更精细的 [[environment-probe-placement|环境探针]] + spherical Gaussians / radiance volumes。Ambient Cube 今天主要作为一个**shader 汇编模式**被识别——当你在某个 G-Buffer pass 的伪代码里看到六次 mad 对称地乘 n² 时，它多半就是 Valve Cube。

## 相关

- [[spherical-harmonics]]
- [[environment-probe-placement]]
- [[deferred-rendering]]
- [[sources/elopezr-clos2-rendering]]

## Sources

- [[sources/elopezr-clos2-rendering]]
