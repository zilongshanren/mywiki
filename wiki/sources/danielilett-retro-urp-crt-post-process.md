---
tags: [source, unity, urp, shader, crt, vhs, post-process]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro for URP - CRT (Post Process)（Daniel Ilett）

[[daniel-ilett]] 为 URP 版 *Retro Shaders Pro* 撰写的 **CRT Post Process** 参数手册——全屏版 CRT/VHS 滤镜，把游戏画面从现代高清面板重写成经典 CRT 显示 + 磁带做旧。

## 摘要

相比 [[sources/danielilett-retro-urp-crt-mesh|URP 版 CRT Mesh]] 或 [[sources/danielilett-retro-godot-crt-post-process|Godot 版 Post Process]]，URP Post Process 版多出几项**全屏专属**的技术参数。**Basic Settings** 段：*Show In Scene View*、*Enabled*、*Render Pass Event*（选择在 URP 内置 post-processing pipeline（Bloom 等）之前还是之后运行，决定 CRT 覆盖的是原始渲染还是经过 tonemap/bloom 的结果）。**Resolution & Fidelity** 段：*Pixel Size*、*Scale In Screen Space* + *Reference Resolution (Vertical)*（设计时的垂直参考分辨率，让像素/RGB/扫描线在不同屏幕上视觉密度一致）、*Force Point Filtering*、以及 **Interlaced Rendering**——交错渲染模式，每帧只渲染一半行，下一帧补上另一半行，模拟 CRT 的 interlace scan。Barrel / RGB Subpixels / Scanlines / VHS Artifacts 段与 Mesh 版一致；VHS 段多一个 *Use VHS Tracking* 总开关。**Color Adjustments** 段多出 **Custom RGB Sliders** 模式——用整数滑块直接指定每通道可取值数（Red Levels / Green Levels / Blue Levels），配合 *Use Dithering* 在色阶间做 dither 混色。Color Ramp 预设覆盖 16 台复古主机；此外还暴露 **Custom Luminance / Custom RGB / Custom RGB+Intensity** 三种自定义 ramp 采样模式：Luminance 用图像亮度沿 x 轴采、RGB 各通道独立沿 x 轴采、RGB+Intensity 在 RGB 基础上用亮度采 alpha 通道作为最终 RGB 的乘子。

## 关键要点

- *Render Pass Event* 让开发者选择 CRT 插在 URP 内置 post pipeline 之前还是之后——前者干净信号、后者已带 Bloom 等效果
- *Interlaced Rendering* 真正模拟 CRT 的交错扫描：每帧只渲一半行，是 Mesh 版和 Godot 版都没有的全屏专属
- *Custom RGB Sliders* 模式用整数滑块直接控每通道级数（Red/Green/Blue Levels）——相比必须外挂 ramp texture 的 Mesh 版，更方便快速调色
- 三种 Custom Ramp 采样模式（Luminance / RGB / RGB+Intensity）是**色阶重映射**的正交矩阵：用亮度还是通道查找、要不要再乘亮度
- *Scale In Screen Space* + *Reference Resolution* 是全屏 post-process 必须解决的跨分辨率视觉一致性问题——Mesh 版无此烦恼

## 链接到的概念

- [[crt-shader-effects]]
- [[color-quantization-retro]]
- [[chromatic-aberration-post]]
- [[urp-volume-post-processing]]
- [[blit-render-feature]]

## 原文

- 链接：https://danielilett.com/retro-shaders-pro/crt-post-process/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-urp-crt-post-process.md`
