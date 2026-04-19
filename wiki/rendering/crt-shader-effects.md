---
tags: [shader, shadergraph, 后处理, 复古, vfx, 渲染]
date: 2026-04-14
sources: 1
---

# 复古 CRT Shader 的拆解

**CRT（阴极射线管）**显示器有一组很容易识别的"味道"：球形外凸的几何、可见的水平扫描线、红绿蓝子像素排列形成的彩色条纹、不时闪烁的噪声和滚动静电干扰。Cyan 为 Harry Alisavakis 的 `#TechnicallyAChallenge` "Retro" 主题做了一个 URP Shader Graph 版本，拆解之后正好是一份"如何把一种真实物理现象拆解为 5 个可叠加的 shader trick"的范本。

## 整体脚手架

作为全屏效果，它先通过 [[blit-render-feature|Blit Render Feature]] 插进 Forward Renderer，pass event 设为 *Before Rendering Post Processing*，pass index 设 0。Shader 是一张 **Unlit Graph**，包含一个 `_MainTex` property 拿到相机颜色。所有 5 个效果都挂在这张图的不同分支上，并用 Shader Graph 的 **Keyword** 节点做开关——配合 `shader_feature` 定义，未使用的变体会在构建时被剥离以减小包体（代价是运行时 `EnableKeyword` 切换时如果该变体没被构建，会显示为洋红色）。

## 效果 1：CRT 弯曲

最标志性的特征是屏幕向外球面凸起。`Spherize` 节点恰好做这件事：把 UV 按球面重新映射，中心设为 `(0.5, 0.5)`。它的输出**替代**所有下游节点的 UV 输入——包括 `Sample Texture 2D`。

球面弯曲后屏幕四角会溢出纹理边界，需要盖上黑边。手法是用 `Rounded Rectangle` 节点生成一个圆角矩形蒙版，再和 `Sample Texture 2D` 的结果相乘——矩形外面蒙版值为 0，乘完就变黑。

## 效果 2：扫描线

扫描线是"每隔若干像素一条暗线"的周期图案。算法就是一段最小的程序化图形合成：取 warped UV 的 **Y 分量**（可选乘以屏幕高度让线数随分辨率自适应），乘以 `Scanline Height` 控制线密度，再 `Fraction` 拿到 `[0, 1)` 的周期。`Fraction` 的三角波形状不好看，用 `Subtract 0.5 → Absolute` 把它翻折成对称的 V 形（中间暗、两端亮），然后 `Saturate` 钳位、和主颜色相乘。这是**先凑周期再塑形**的典型节点拼法。

## 效果 3：RGB 条纹（荧光粉 / 子像素）

真实 CRT 的一个像素由红绿蓝三条平行荧光粉条组成。复刻这个结构的套路是用 `Modulo` 节点代替 `Fraction`——Modulo 给 3 时输出 `[0, 3)` 的周期而不是 `[0, 1)`——再用三个 `Step` 节点切出 `(0, 1)`、`(1, 2)`、`(2, 3)` 三段，分别塞进 `Vector3` 的 R/G/B 通道。最终得到一张"每像素只点亮一个通道"的条纹图，和主颜色相乘即可。

但这样相乘后整体变暗，因为大部分像素只激活 1/3 的能量——Cyan 的补救是先把主颜色 `Add` 一个 `Image Brightness`，提到相乘前，把损失补回去。分辨率参数应该是 3 的倍数（例如 384 = 128 × 3），否则条纹周期和像素格对不上会出现 moiré。

## 效果 4：水平抖动 / 静电

CRT 的水平同步偶尔会抖一下，复刻方法是用 `Simple Noise` 节点生成 1D 噪声（输入只用 UV 的 Y 分量加 Time），把噪声 `-0.5` 中心化然后乘以一个小系数（0.1 级别）和 `Distortion Strength`——直接偏移采样 UV 的 X 分量。如果不乘小系数，一个 `[0, 1]` 的噪声会把采样坐标偏移半个屏幕宽度。

纯静电的部分用 `Random Range` 节点按 `warped UV + Time` 每帧随机采样，乘一个 `Static Strength` 系数**加**到采样结果上（不是相乘——相乘会把黑色部分也压暗，加法才是真正的叠加高光噪点）。避免 `Random` 在某些 Time 值上产生规则条纹的技巧是先对 Time 做一次 `Fraction`，防止浮点精度退化。

## 效果 5：滚动水平条

最后一种视觉元素是"从上到下反复扫过的一条亮带"，让画面像老磁带一样偶尔抖动。做法是：取 warped UV 的 Y 分量乘 1.5、加 Time、再 `Fraction` 得到 0-1 的滚动梯度，然后经过 `Power 5` 把曲线变得陡峭——大部分区域接近 0，只有顶端一小段接近 1，这样才像一条"带"而不是渐变。

这条滚动带做两件事：第一，乘以前面的 distortion 噪声再加到 X 偏移上，让带子经过的区域抖得更厉害；第二，把带子亮度作为 HSV 的 **Value**，用 `Colorspace Conversion (HSV → RGB)` 上色——Hue 接前面的 `Simple Noise` 输出、Saturation 固定 0.8——于是带子呈现"青绿色偏移的 glitch 色调"而不是纯白。

## 为什么这个 breakdown 有指导意义

它把一种真实光学现象拆成 5 个**相互正交**的小 trick，每一个都是"用 Fraction/Modulo 造周期 + 用 Step/Abs/Power 塑形 + 乘加回最终颜色"的套路，彼此可以独立 toggle。这种模块化是 Shader Graph 作品常见的结构——也是为什么 Cyan 在多处使用 `Keyword` 节点：每个效果独立开关，调试时能把贡献拆开看。同时它暴露了 Shader Graph 的一个代价：每加一个 keyword 变体数翻倍，build 时间和 Shader Variant Collection 会膨胀，而使用不同变体的材质也**无法被 SRP Batcher 合批**。

## 相关

- [[blit-render-feature]]
- [[urp-volume-post-processing]] —— CRT 效果常叠加 Volume 里的 Vignette / Film Grain / Chromatic Aberration
- [[uv-manipulation-nodes]]
- [[shaping-functions]]
- [[harry-alisavakis]] —— 挑战赛主办
- [[cyanilux]]
- [[chromatic-aberration-post]] —— 独立通道 UV 偏移，Teleglitch / Deadlight 的故障艺术后处理
- [[sources/alanzucconi-flixel-retro-crt]] —— Alan Zucconi 2012 年的 Flixel/AS3 版本，CPU `BitmapData.copyChannel` + 矩阵微缩放在 Flash 时代实现的 RGB 通道错位
- [[color-quantization-retro]] —— NES/SNES/GB 色阶量化与像素化下采样
- [[sources/danielilett-retro-godot-crt-mesh]] —— Daniel Ilett *Retro Shaders Pro for Godot* CRT Mesh 版，把同款 CRT/VHS 滤镜贴到普通网格做游戏内 CCTV 屏
- [[sources/danielilett-retro-godot-crt-post-process]] —— 全屏版 CRT + VHS，独有 *Scale In Screen Space / Reference Resolution* 做跨分辨率视觉一致性，*Tracking Color Damage* 走 YIQ 色空间建模 NTSC 磁带色损
- [[sources/danielilett-retro-urp-crt-mesh]] —— URP 版 CRT Mesh，和 Godot 版近似；Tracking Texture 用 x-by-1 的 RG 双通道编码 UV 偏移 + 扫描线概率
- [[sources/danielilett-retro-urp-crt-post-process]] —— URP 全屏版独有 *Interlaced Rendering*（每帧只渲半数行，真实 CRT 交错扫描）、*Custom RGB Sliders*（整数滑块直控 R/G/B 每通道级数）、*Render Pass Event*（插在 URP 内置 post 之前或之后）、以及 Custom Luminance / RGB / RGB+Intensity 三种 ramp 采样模式

## Sources

- [[sources/cyan-retro-crt-shader]]
- [[sources/alanzucconi-flixel-retro-crt]]
- [[sources/danielilett-retro-urp-crt-mesh]]
- [[sources/danielilett-retro-urp-crt-post-process]]
