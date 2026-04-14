---
tags: [渲染, mipmap, 纹理过滤, moire, 风格化, 屏幕]
date: 2026-04-14
sources: 1
---

# 以 mipmap 采样伪造 CRT 扫描线

《Deus Ex: Human Revolution》的总部里挂着许多电子公告牌，走近时屏幕会浮现出一层**会随距离变化**的扫描线和颜色裂变，像《黑客帝国》或《午夜凶铃》里主角被「拉进」显示器前那一瞬间的故障感。[[simon-trumpler|Simon Trümpler]] 在这篇短文里讨论了这种效果的成因：它看起来像精心设计的 post-process，但很可能**只是一张没有 mipmap（或 lod-bias 为负）的高对比度纹理，在相机接近时触发的 moiré 图案**。

底层原理是**纹理像素网格和屏幕像素网格之间的采样频率冲突**。显示器本身是一张规则的像素阵列；一张以黑白横条构成的「扫描线」纹理也是一个规则阵列。当这两个规则阵列以非整数倍率叠加（以及非轴对齐地旋转）时，采样结果会产生低频干涉纹——也就是 moiré。正常的游戏开发会开 [[mipmap-filtering|mipmap]] 加上三线性或各向异性过滤，把远处纹理自动 LoD 降级掉高频内容，避免 moiré。但 Deus Ex 在这些屏幕资产上**反其道而行**：要么不生成 mipmap、要么用 negative lod bias 强行采样高分辨率 level，让 moiré 故意出现——从而把「近处看屏幕会崩纹」变成一种视觉语言。

几个值得单独记下来的点：

- **同款现象在摄影和电视上很常见**：穿格子西装的嘉宾一上电视就会闪出彩色干涉纹，这是相机传感器的 Bayer 阵列和织物图案之间的 moiré，机制与此一致。
- **不仅有明度干涉，还有色彩**。由于屏幕 RGB subpixel 有固定的水平偏移，高对比的规则纹理可以让相邻像素的 R、G、B 通道以**不同相位**采样到黑或白，观感上就是「莫名其妙出现了洋红和绿色条」——Deus Ex 的屏幕近看时确实会伴随 RGB 裂变。
- **评论里另一个 TF2 的趣闻**：Team Fortress 2 里玩家会故意利用 mipmap 机制做「近看远看两张图」的喷漆——比如远处是一盘三明治、走近后触发最高 mip level 切换成一盘空盘子加一行字「How could this happen?」。这是对 mipmap 的**同一套机制的创意反用**：远 mip 和近 mip 藏着完全不同的内容。
- **Scanline 也可以用 UV scale 动态做**：评论里一位开发者提到他的做法是**按相机距离调整 scanline 纹理的 UV scale**，让扫描线的视觉密度随着接近而加密，从而以更可控的方式模拟同样的视觉。

这是一条有趣的设计法则：**aliasing 通常是我们要消除的瑕疵，但选择性地保留它能免费得到某种材质感**。CRT shader 里大量用到 mipmap-bias 作为调味料；老游戏里 pixel art 强行开 bilinear 的「糊感」也是同一类——我们今天一眼能辨的「复古风」里很大一部分是**过去硬件缺陷的审美化**。它跟 [[crt-shader-effects]] 一脉相承，但实现得更懒更便宜：不需要 post，不需要额外 pass，只要在纹理导入器里把 *Generate Mipmaps* 取消勾选。

## 相关

- [[crt-shader-effects]] —— 更完整的 CRT 视觉模拟
- [[mipmap-filtering]]
- [[aliasing]] —— moiré 是频域层面的 aliasing
- [[chromatic-aberration-post]]

## Sources

- [[sources/simonschreibt-deus-ex-scanlines]]
