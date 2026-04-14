---
tags: [渲染, 体素, 环境光遮蔽, 烘焙]
date: 2026-04-14
sources: 1
---

# 体素环境光遮蔽（Voxel Ambient Occlusion）

在一个**每个 voxel 都是单位方块**的世界里，环境光遮蔽不需要 SSAO 那种屏幕空间估算——它可以在 [[greedy-voxel-meshing|meshing]] 时**精确、便宜地预计算**，然后作为顶点属性烘进 mesh。这是 Minecraft 风格渲染里最著名的「既对又快」trick。

## 每顶点四级 AO

关键观察：一个面顶点的 AO 值**只依赖于该顶点共享的三个相邻 voxel**——两个侧面方向的邻居和一个对角邻居。结果有四个离散等级（0~3）：

```
if (side0 && side1) return 0;           // 两侧都实，最暗
return 3 - side0 - side1 - corner;      // 否则按数量递减
```

这四个等级再经一条曲线（比如 `[0.75, 0.825, 0.9, 1.0]`）映射成线性亮度系数，在片段着色器里直接乘到 albedo 上。

## 双线性插值的坑

把 4 个顶点的 AO 塞进 `vec4` 再让 GPU 按 triangle 做重心插值，会在「梯形 AO 分布」上产生明显的**视觉接缝**——一条三角形对角线会从原本连续的 AO 中暴露出来。

解决办法：**把四个顶点的 AO 值同时广播给每个顶点**，在片段着色器里根据该像素的 $u/v$（面内坐标）做**双线性插值**。这样整个 quad 上的 AO 是连续的，也能正确处理长条 quad 的情况。

## 为什么这个 trick 这么便宜

- **只查 3 个邻居**：每个顶点一次——每个面 4 个顶点 × 3 邻居 = 12 次 voxel 查询；比 SSAO 少三四个数量级。
- **和 meshing 同一遍做**：已经在扫邻居算遮蔽了，顺便算 AO 几乎零开销。
- **可以烘进顶点**：四个值 × 每值 2 bit = 8 bit，塞进 [[compact-vertex-format|紧凑顶点格式]] 的零头里。
- **无 runtime 成本**：shader 只做一次 bilinear insert + 乘法，没有 ray cast、没有 screen-space 扫窗口。

## 和其它 AO 的对比

- **SSAO / HBAO**：能处理任意几何但有噪声、依赖屏幕空间——在体素世界是杀鸡用牛刀。
- **voxel ray trace AO**：能拿更远距离的遮挡但贵得多；在 Minecraft shader mod 里作为画质选项出现。
- **这一套 mesh 时烘出来的 AO**：只考虑紧邻 1 个 voxel，不能处理远距离遮挡——但足以让角落和凹面「看起来对」，且完全免费。

## 相关

- [[greedy-voxel-meshing]] — AO 的产生时机
- [[compact-vertex-format]] — AO 值的存储位置
- [[hbao-interleaved-sampling]] — 通用几何上的 AO 方案，对比之下体素的奢侈

## Sources

- [[sources/slater-exile-voxel-rendering]]
