---
tags: [source, rendering, unreal, ssr, 后处理, temporal-antialiasing, tonemapping]
date: 2026-04-14
sources: 1
---

# How Unreal Renders a Frame part 3（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] *How Unreal Renders a Frame* 系列收官篇，覆盖 UE4.17 默认管线的后半段：image-space lighting、大气、透明物、后处理链。

## 摘要

**屏幕空间反射** 用 Hi-Z 做加速（按 surface roughness 选 mip，粗糙表面取粗 mip），每帧 jitter ray start + TAA 提质，采样**上一帧**的 scene color——所以反射里能看到体积雾、透明物、粒子。`ReflectionEnvironment` compute pass 把 SSR 和 2 颗 **reflection probe**（游戏启动时烘焙，只捕静态几何）的 mipmapped cubemap 合成回主 RT。之后是 Bruneton 风格的大气散射（precomputed transmittance / irradiance / inscattering）和指数雾 + light shaft——light shaft mask 先 quarter-res 生成，走 TAA 再 blur。**透明物**（玻璃雕像）使用 translucency lighting volume + atmosphere LUT + baked lightmap + reflection probe 采光；**粒子**写单独 full-res RT。**折射**的做法是：支持折射的透明物 + 粒子**重绘一次**写 distortion vector buffer，`DistortionApply` 读主 RT + distortion 产出折射纹理，最后按 stencil 合成回主 RT。后处理链：**TAA**（分 stencil / 非 stencil 两 pass，前者 dynamic blend factor、后者固定 0.25 防粒子 ghost）→ motion blur（先 velocity dilate）→ **auto-exposure**（compute shader 算亮度直方图，轻松跳极端 bin 求更稳均值）→ **bloom**（Gaussian down + up combine）→ `PostProcessCombineLUTs` 生成 32³ RGB10A2 colour-grading LUT → `Tonemapper` 合并 bloom、应用曝光、过 LUT 输出。

## 关键要点

- SSR 用 Hi-Z mip 选择加速 raymarch，按 roughness 选 mip。
- SSR 采色使用**上一帧** scene color —— 所以能看到雾、透明物反射。
- Reflection probe 只烘焙**静态**几何。
- 折射需要把透明物 / 粒子**重绘一次**写 distortion vector。
- TAA 双 pass：非 stencil 动态 blend / stencil 固定 0.25 blend 防粒子 ghost。
- Auto-exposure 用 compute 算 histogram，跳极暗极亮 bin 获得稳定均值。
- Tonemapper 同时 apply bloom、exposure、colour grading LUT。

## 链接到的概念

- [[unreal-frame-breakdown]]
- [[temporal-antialiasing]]
- [[color-lut]]
- [[bloom-threshold-blur-composite]]
- [[hierarchical-z-buffer]]
- [[volumetric-fog-froxels]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2017/10/25/how-unreal-renders-a-frame-part-3/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2017-10-25_how-unreal-renders-a-frame-part-3.md`
