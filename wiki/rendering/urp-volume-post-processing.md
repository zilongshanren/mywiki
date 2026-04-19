---
tags: [unity, urp, 后处理, volume, 渲染]
date: 2026-04-14
sources: 2
---

# URP Volume 后处理系统（PPv3）

Unity 从 **Universal Render Pipeline**（URP，前身 LWRP）开始，抛弃了旧的 **Post Processing Stack V2**（PPv2，作为独立 Package Manager 包存在），改为集成式的 **Volume** 系统，社区也叫它 **PPv3**。Cyan 的 URP 后处理教程把这套系统的架构讲得很清楚：它不再是「附加在相机上的一条后处理链」，而是「基于体积的渲染参数插值器」。

## 基本架构

一个 Volume 组件挂在场景里的任意 GameObject 上，有两种形态：

- **Global**：始终作用于整个场景，是一个全局参数源。
- **Local**：必须附带一个 Collider（建议开 IsTrigger），只有当相机进入该 Collider 时才生效；配合 **Blend Distance** 可以让相机跨越边界时平滑过渡（例如进入水下瞬间渐变出浓雾与色调偏冷）。

多个 Volume 可以叠加。当它们重叠或嵌套时，**Priority**（数值越大越优先）决定谁覆盖谁，**Weight** 则决定该 Volume 中的效果以多大比例贡献进最终混合结果。每个 Volume 引用一个 **Profile** 资源，Profile 存放一组 effect override（Bloom、Chromatic Aberration、Depth of Field、Color Adjustments、Tonemapping、Vignette 等）。多个 Volume 可以共享同一个 Profile。每项参数都有默认值，默认被置灰；只有用户手动勾选左侧复选框、把该参数标记为 override，它才会参与混合。

## 从 PPv2 到 PPv3 的断层

如果从旧项目升级，PPv2 的 Post-Process Layer / Post-Process Volume 组件**无法自动迁移**到 PPv3，必须手工重建。在 URP v7.2–v7.4（随 Unity 2019.4 LTS）时代，URP Asset 上还有一个 "Feature Set" 选项，可以把后处理切回 PPv2；v8.0 之后这个选项被彻底移除，只剩 Volume 系统。想使用任何后处理效果，相机的 Inspector 上还必须把 **Post Processing** 开关打开。

## Volume Mask 与 Volume Trigger

相机的 **Environment** 区块有两个容易被忽略的设置：**Volume Mask** 指明哪些 Layer 上的 Volume 可以影响这台相机，便于做"编辑器预览相机不受游戏后处理影响"这类隔离；**Volume Trigger** 指定用哪个 Transform 的位置来做 Local Volume 碰撞判定，留空则用相机自身位置——但有时想让第三人称角色的后处理跟着角色而非相机移动，就需要把 Trigger 指向角色 Transform。

## 限制与缺失的效果

直到 Cyan 写这篇文章时（URP v8），**Ambient Occlusion** 还没进 URP Volume 系统；此外 PPv2 上的 **Motion Blur** 和 **Temporal Anti-aliasing** 在 URP 初期也不全支持。想要自定义后处理效果，当时 Volume 系统**完全不开放扩展点**——只能通过 [[blit-render-feature|自定义 Blit Render Feature]] 绕路实现（这条限制后来 Unity 2022 推出 Fullscreen Graph / Fullscreen Pass Renderer Feature 才缓解）。这是 URP 早期和 HDRP 在架构成熟度上的典型差异。

## 相关

- [[blit-render-feature]] —— 在 Volume 系统无法扩展时的补救方案
- [[crt-shader-effects]] —— 一个典型的通过 Blit feature 叠加 Volume 效果的案例
- [[scriptable-render-pipeline]]
- [[custom-srp]]
- [[chromatic-aberration-post]] —— URP 内建的色差 volume override 的底层实现
- [[godot-hologram-shader-effects]] —— Godot 端的 PBR + Volume 叠加 glitch/fresnel 的等价实现

## Sources

- [[sources/cyan-urp-post-processing]]
- [[sources/cyan-retro-crt-shader]]
- [[sources/danielilett-blur-shaders-pro-scripting]]
