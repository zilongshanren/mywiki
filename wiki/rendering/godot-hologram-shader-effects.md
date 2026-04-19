---
tags: [godot, unity, urp, hdrp, shader, hologram, glitch, fresnel, scanline, noise, dynamic-resolution, stylized]
date: 2026-04-19
sources: 9
---

# Godot 全息着色器效果套件

Daniel Ilett 的 *Hologram Shaders* Godot 版以"同一套 PBR + glitch + fresnel 框架，再叠加一项主视觉模式"的方式组织七种材质变体——**Dot Matrix**（屏幕空间点阵）、**Glitch**（纯抖动）、**Gradient**（上下双色渐变）、**Grid**（世界空间网格线）、**Noise**（胶片颗粒）、**Scanline**（扫描线 alpha）、**Uber**（三合一 + unscaled time）。从工程角度看，它是把"全息风格"拆成几个正交特性的教科书例子：基础光照与形变（顶点）解耦，屏幕空间装饰、世界空间装饰、颜色映射装饰互不干扰，各自作为可选模块接入。同一套产品还有 Unity URP/HDRP 移植（*Hologram Shaders Pro*），参数对齐但额外暴露 PBR 的 *Metallic / Smoothness / AO* 与 **Dynamic Resolution** 补偿项。

## 共享底座

四个变体都共用同一段"骨架"：

- **Basic PBR**——*Output Mode* 决定着色结果写入 Albedo、Emission 或两者（全息体的亮度几乎完全来自 Emission）；*Base Color / Base Texture* 乘合，*Normal Texture / Normal Strength* 调整法线，*Alpha Clip Threshold* 做硬裁切（见 [[dither-alpha-clipping]]）。
- **Vertex Glitches**——基于每顶点随机数与 *Glitch Sensitivity* 阈值比较，被选中的顶点沿法线方向外推 *Glitch Strength* 距离，*Glitch Normal Multiplier* 允许把 glitch 限制在某个平面（如 `(1,0,1)` 只在 XZ）。*Glitch Time Offset* 使同一份材质的两个实例之间产生相位差，避免视觉上同步闪烁。
- **Segment Glitches**——沿 Y 轴扫描一条世界空间高度 *Slice Width* 的水平切片，把切片内顶点沿 *Slice Direction* 平移一小段时间（*Slice Duration*），*Slice Speed* 控制扫描速度，*Slice Jitter* 加入小幅抖动使切片本身看起来不稳定。是"电视信号错位"与"故障全息投影"的经典表现手法。
- **Fresnel**——*Fresnel Power* 控制边缘宽度（值越大 rim 越细），*Fresnel Color* 独立于 Base Color；*Use Scene Intersections* 读深度缓冲，在几乎接触不透明物体时叠加 *Intersection Power* 控制的细边缘辉光，这是[[fresnel-edge-highlight|菲涅尔边缘强化]]的标准产品化形态，也与 [[depth-intersection-subgraph|深度相交子图]] 思路一致。

## 四种主视觉

- **Dot Matrix**——在屏幕空间把覆盖区域切成 *Dot Size* 像素的方块，方块之间留 *Dot Space* 空隙；*Rotation Radians* 旋转整套栅格。整体风格接近老式 LED 矩阵显示。
- **Glitch**——不附加主视觉，主体就是 Vertex + Segment 两类 glitch 的叠加，适合需要"纯故障感"但不想要任何几何装饰的场景。
- **Gradient**——沿 *Gradient Space*（Object / World / Screen）之一的 Y 轴，把表面在 *Gradient MinMax Y* 两个阈值之间做双色线性插值（*Base Color* 到 *Base Color 2*）。Fresnel 也有第二颜色 *Fresnel Color 2*。Gradient 变体另有 **Use Unscaled Time** 开关——因为 Godot/Unity 没有向 shader 内置 unscaled time，必须从脚本推送，这样当 `Time.timeScale` 改变时全息依然按真实节奏闪烁。
- **Grid**——在世界空间沿三轴生成规则网格线，*Grid Axis Strength* 单独开关每条轴，*Grid Density* 控制疏密、*Line Thickness* 控制线宽、*Line Falloff* 控制边缘过渡软硬；可选围绕 *Rotation Axis* 旋转、沿 *Grid Velocity* 滚动。典型"科幻网格投影"。
- **Noise**——叠加时变随机噪声模拟胶片颗粒；*Noise Speed / Scale / Strength / Color* 四参数组，形成通用的"时间 × 空间 × 强度 × 色彩"噪声接口，直接作用在 Emission 上。
- **Scanline**——用一张扫描线贴图**调制 alpha**（非叠色），*Scanline Mode* 可切屏幕空间（黏屏，像电视扫描线）或世界空间（黏物体，像真·全息投影）。*Scanline MinMax Alpha* 把贴图 0/1 映射到可调 alpha 区间，本质是"贴图当 1D LUT"的用法。
- **Uber**——把 Scanline + 两类 Glitch + Noise 合并进同一份 shader，每个子系统独立布尔开关；作者保留独立 shader 作为"单功能便宜版"，是典型的 [[shader-combination-strategies|uber vs variant]] 取舍。另外引入 *Use Unscaled Time*，由脚本推送 unscaled time uniform，保证 `Time.timeScale=0` 时 UI 全息仍动。

## 设计观察

把四个变体对齐看，Ilett 的设计选择有两点值得提：第一，所有"装饰层"都被设计成与几何形变解耦——glitch 发生在顶点阶段，dot/grid 发生在像素阶段，fresnel 发生在几何着色末端，任意组合不会冲突；第二，关键参数都做了"可调概率 + 可调强度 + 可调相位"三件套（Sensitivity / Strength / Time Offset），这是把随机美术特效产品化时绕不开的模式——美术要的不是"抖"，而是"可控地抖"。

第三点可补充：从 Godot 版到 Unity URP/HDRP *Pro* 版的移植中，Ilett 遇到一个平台相关的坑——**动态分辨率（FSR/DLSS）下屏幕空间 UV 的语义漂移**。Unity 启用动态分辨率时，shader 内部有时拿到的是升采样前分辨率而非呈现分辨率，导致 Dot Matrix 的点阵大小在不同帧率下波动。Pro 版暴露 *Upscaling Amount* 作为旁路补偿——这是任何依赖屏幕空间 UV 的材质或后处理在 [[dynamic-resolution-scaling|动态分辨率缩放]] 下都要面对的通用问题。

## 相关

- [[godot-visual-shaders]] —— Godot 端 shader 开发基础
- [[fresnel-edge-highlight]]
- [[depth-intersection-subgraph]]
- [[dither-alpha-clipping]]
- [[glitch-image-effect]] —— 屏幕空间 glitch 后处理的对照
- [[shader-combination-strategies]] —— Uber shader vs 多变体编译的取舍
- [[classic-shader-noise]] —— Noise 子模块的通用接口模式
- [[crt-shader-effects]] —— Scanline 与屏幕空间扫描线的对照
- [[dynamic-resolution-scaling]] —— Pro 版的 Upscaling Amount 补偿原因

## Sources

- [[sources/danielilett-hologram-godot-dot-matrix]]
- [[sources/danielilett-hologram-godot-glitch]]
- [[sources/danielilett-hologram-godot-gradient]]
- [[sources/danielilett-hologram-godot-grid]]
- [[sources/danielilett-hologram-godot-noise]]
- [[sources/danielilett-hologram-godot-scanline]]
- [[sources/danielilett-hologram-godot-uber]]
- [[sources/danielilett-hologram-pro-basic]]
- [[sources/danielilett-hologram-pro-dot-matrix-glitch]]
- [[sources/danielilett-hologram-pro-dot-matrix]]
- [[sources/danielilett-hologram-pro-glitch]]
- [[sources/danielilett-hologram-pro-gradient]]
- [[sources/danielilett-hologram-pro-grid]]
- [[sources/danielilett-hologram-pro-grid-glitch]]
- [[sources/danielilett-hologram-pro-noise]]
- [[sources/danielilett-hologram-pro-scanline]]
- [[sources/danielilett-hologram-pro-uber]]
