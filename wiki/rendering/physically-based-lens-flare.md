---
tags: [渲染, 后处理, lens-flare, 相机, 光学, fourier, 物理模拟]
date: 2026-04-19
sources: 1
---

# 物理基础 Lens Flare

大多数游戏的 lens flare 是**美术摆的 sprite 链**：沿太阳到画面中心连线等间距放几个七彩光晕，简单能骗眼睛但经不起镜头运动。Stingray 的 Jp 在 2017 年基于 Hullin 等人 2011 的 *Physically-Based Real-Time Lens Flare Rendering* 论文做了一版真·物理 lens flare——**把一整套镜头组（lens interface）里的光线全部追一遍**，记录它在每两片镜片之间的内反射如何形成 "ghost"，最后在 sensor 上用 compute + 几何 shader 把每个 ghost 画出来。

## Ghost 的组合爆炸

一个 "ghost" 就是一次 **双次反射路径**：光线在某两片镜面之间 bounce 两次（两次反射方向相反，每次都从 air → glass 或 glass → air 界面反射回来），最终穿过后续镜片落到 sensor。Nikon 28–75mm 镜头有 27 个光学面，两两组合 ghosts 数 = `C(27, 2) = 352`。每个 ghost 都要被独立追踪 + 绘制。

## 追踪管线

1. **解析 lens prescription**：镜头专利给出每面的曲率半径、厚度、折射率、光阑（aperture）位置。实际工程里最烦的就是这一步——老镜头（如俄制 MIR-1）的描述甚至不完整。
2. **初始化 tessellated patch**：在相机光入口处划一张规则网格，每个顶点出一条光线朝向太阳方向。
3. **追踪 + 记录**：compute shader 按镜头面串行追踪。**关键技巧**是光线 miss 某一面时**不立即终止**，只要它能沿有意义路径继续走就保留；每条光线追踪最大 "相对距离"，shader 最后用它判断光线是否已经离开合法镜头口径。miss 整个球面（面的有效半径之外）才 break。这是为了保留 patch 的几何连续性，让后续插值不撕裂。
4. **每个光束的能量守恒**：光线不是独立的粒子，是一束 "bundle"，bundle 的面积变化 = 能量密度变化。论文原用 geometry shader transform feedback 查四个邻接 quad；Jp 改用 compute + UAV，粗略用"相邻顶点求平均"估算每个 bundle 的 base / height。这里是计算热点，Jp 坦言需要优化。

## Ghost 的 pixel shader

追踪完得到一张扭曲的四边形 patch。pixel shader 用一串 **discard** 链清理：

```hlsl
// 1) 丢弃离开镜头系统的 ray
if (max_relative_distance >= 1.0) discard;
// 2) 丢弃进入时不在 sun disk 范围内的
float lens_distance = length(entry_coordinates.xy);
float sun_disk = smoothstep(0, 1, 1 - saturate((lens_distance - 1.0 + fade)/fade));
if (sun_disk == 0) discard;
// 3) 丢弃被 aperture 挡住的
if (aperture_sample == 0) discard;
// 4) 用 bundle 面积比做 radiance 归一
float intensity = (original_area/(new_area + eps)) * energy
                  * sun_disk * aperture_sample;
float3 color = intensity * reflectance.xyz * TempToColor(sun_temperature);
```

`reflectance` 是 ghost 对应两次反射的 **anti-reflection coating** 计算结果——coating 按设计波长 λ 和两侧介质 IOR `n0, n2` 生成理想 `n1 = sqrt(n0*n2)`、`d = λ/(4*n1)` 的 quarter-wavelength 层，AR coating 越厚 ghost 越亮。Jp 把 coating 厚度做成可调 knob，滑动它可以从"高端镜头"到"廉价镜头"平滑过渡。

## Aperture：SDF 程序化

光圈形状用 signed distance field 程序化生成（受 Padraic Hennessy 的 *placeholderart* 博客启发）：

- `n` 条线段围成的凸多边形 SDF（Inigo Quilez 式的一套 primitive）
- 用 `abs(distance) < threshold` 在 aperture 边缘加一层模拟衍射的薄光
- SDF 再叠一个周期性 `sin` 偏移 → 曲面叶片（多叶片光圈的弧形刀片）

## Starburst：Fourier 衍射

太阳高亮时肉眼看到的"星芒"是 **小孔单缝衍射**——物理上是光的波动性结果。论文用 **Fraunhofer 近似** 把 aperture 形状变换到 Fourier 域：

1. 用 Intel Joseph S. 的 compute butterfly FFT 把 aperture 图案变到频域，取 power spectrum。
2. 频谱本身和波长相关——**scale 采样坐标**就等于换波长。对可见光分段，每个波长拿一个不同缩放的频谱样本。
3. 所有波长加起来 = 白光 starburst。
4. 额外做一步 spiral 模式 + 小旋转的滤波，消掉残余径向 ring 纹。

这是**把物理现象映射到信号处理工具**的漂亮案例——衍射是卷积，卷积在 Fourier 域是乘法，波长切换是坐标缩放，全部闭式。

## 代价与优化空间

Nikon 28–75mm 在当代 GPU 上跑 **12 ms**（3 ms ray march 352×32×32 + 9 ms 光栅 352 patches），大部分时间花在 ghost 的过度 overshading 上——sun disk 越大每个 patch 光栅越满。Jp 提出但没落地的优化是 **Compute + DrawIndirect 粗筛**：先跑一个低分辨率 pass 估每个 ghost 的贡献，intensity 低于阈值直接不画。这和 GPU culling、compaction 是同一套工具。

## 评价

Jp 自己说这东西 **"现役游戏大概不值得"**——预可视化 / 过场镜头用得起，实时单相机 12 ms 太吓人。但它展示了一种彻底不同的 lens flare 哲学：不是"加两个七彩 sprite"，而是"把相机光学系统作为 physically-correct 的一阶 primitive 建模"，顺便暴露了一批工程心得（bundle 面积、SDF aperture、AR coating、Fourier starburst）可以零成本借用到其他效果里。

源码开放在 [greje656/PhysicallyBasedLensFlare](https://github.com/greje656/PhysicallyBasedLensFlare)。注意论文本身有专利。

## 相关

- [[thin-lens-model]] — 薄透镜近似 vs 全 lens interface 追踪
- [[physical-camera-model]] — Stingray 这一系列的后续工作
- [[scatter-bokeh-dof]] — 同样从光圈形状出发的另一个物理现象（bokeh）
- [[chromatic-aberration-post]] — 色散的另一个"便宜货"路线
- [[sdf-2d-primitives]] — aperture SDF 用的是这套工具
- [[bloom-threshold-blur-composite]] — lens flare 常与 bloom 在同一 post-effect 链
- [[niklas-frykholm]]

## Sources
- [[sources/bitsquid-physically-based-lens-flare]]
(already links to [[sources/bitsquid-physically-based-lens-flare]] — no patch needed)
