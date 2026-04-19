---
tags: [godot, shader, hologram, glitch, fresnel, stylized]
date: 2026-04-19
sources: 4
---

# Godot 全息着色器效果套件

Daniel Ilett 的 *Hologram Shaders* Godot 版以"同一套 PBR + glitch + fresnel 框架，再叠加一项主视觉模式"的方式组织四种材质变体——**Dot Matrix**（屏幕空间点阵）、**Glitch**（纯抖动）、**Gradient**（上下双色渐变）、**Grid**（世界空间网格线）。从工程角度看，它是把"全息风格"拆成几个正交特性的教科书例子：基础光照与形变（顶点）解耦，屏幕空间装饰、世界空间装饰、颜色映射装饰互不干扰，各自作为可选模块接入。

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

## 设计观察

把四个变体对齐看，Ilett 的设计选择有两点值得提：第一，所有"装饰层"都被设计成与几何形变解耦——glitch 发生在顶点阶段，dot/grid 发生在像素阶段，fresnel 发生在几何着色末端，任意组合不会冲突；第二，关键参数都做了"可调概率 + 可调强度 + 可调相位"三件套（Sensitivity / Strength / Time Offset），这是把随机美术特效产品化时绕不开的模式——美术要的不是"抖"，而是"可控地抖"。

## 相关

- [[godot-visual-shaders]] —— Godot 端 shader 开发基础
- [[fresnel-edge-highlight]]
- [[depth-intersection-subgraph]]
- [[dither-alpha-clipping]]
- [[glitch-image-effect]] —— 屏幕空间 glitch 后处理的对照

## Sources

- [[sources/danielilett-hologram-godot-dot-matrix]]
- [[sources/danielilett-hologram-godot-glitch]]
- [[sources/danielilett-hologram-godot-gradient]]
- [[sources/danielilett-hologram-godot-grid]]
