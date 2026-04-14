---
tags: [渲染, unity, 后处理, displacement, uv, 屏幕效果]
date: 2026-04-14
sources: 2
---

# UV 位移后处理（UV Displacement Image Effect）

「位移」是把一张图按某个二维向量场重新采样的操作——对每个屏幕像素，先算出一个 `(dx, dy)` 偏移，再用 `tex2D(_MainTex, uv + offset)` 取颜色，结果就是原图被「揉」成了波纹、热浪、冲击波或者水面折射的样子。它是几乎所有「画面要扭曲」的视觉效果的统一抽象，从 2D 水波到玻璃折射、从冲击波到屏幕受击反馈，本质都是「在已有的 framebuffer 上做一次非均匀 UV 变形」。

## 最朴素的形式：用一张灰度图当位移场

Harry Alisavakis 在 *My take on shaders* 第五篇里给出最直接的实现——用一张灰度遮罩当位移强度的权重：

```hlsl
fixed4 displ      = tex2D(_DisplacementMask, i.uv);
float2 displ_uv   = i.uv + displ.xy * _DisplacementAmount;
return tex2D(_MainTex, displ_uv);
```

灰度遮罩里黑色（0）的区域不动，白色（1）的区域被偏移最多，灰色按比例。配上一张「中心白、边缘黑、带柔边」的圆形遮罩，再脚本驱动让这个圆从一个点开始往外扩散，就是一发**冲击波**——这个最小可用的工具链构成了无数游戏的命中反馈。这种实现的局限性和 [[image-effect-mask-blend]] 一样：遮罩的纵横比必须匹配屏幕，遮罩位置/大小不能在 shader 里直接调。

这套位移操作在 [[glitch-image-effect|glitch 后处理]] 里被复用了两次：一次用波浪位移（`sin(uv.y * freq)` 合成的 R/G 双通道 mask）做磁带式纵向抖动，一次用 [[random-stripes-mask-shader|随机条纹 mask]] 做逐行水平撕裂。两次都只改变计算 `displUV` 的那一行，最终采样路径完全一致——说明「UV 位移」是一套统一的抽象。

## 进阶：把贴图当作向量场，并随时间滚动

第六篇 *Waving Displacement* 把这个思路推到更接近「水面折射」的形态：位移向量不再来自单通道亮度，而是直接读纹理的 R/G 通道当作 `(dx, dy)` 的二维向量场，再用 `_Time.x` 让 UV 持续滚动制造动画：

```hlsl
float2 changingUV = i.uv + _Time.x * 2;
float2 displ      = tex2D(_DisplTex, changingUV).xy;
displ             = (displ * 2 - 1) * _DisplAmount;   // [0,1] → [-1,1]
return tex2D(_MainTex, i.uv + displ);
```

两个关键转换：

1. **R/G → 二维向量**。把贴图当作有符号的二维向量场，红通道控制 X，绿通道控制 Y。这是和经典 normal map 一样的 packing 思路——用纹理通道存方向信息。
2. **`[0, 1] → [-1, 1]`**。纹理像素天然是非负的，得用 `2x - 1` 把范围拉到正负，否则位移永远是单方向的偏置。
3. **`_Time.x` 滚动 UV**。Unity 内置的 `_Time = (t/20, t, 2t, 3t)` 让位移场本身在屏幕上漂移，构造出「液体在动」的错觉。每帧采样的不是同一片像素，所以即便贴图是静态的，输出也是动态的。

效果近似一个伪水面：原画被一团缓慢翻滚的波纹分量推来推去。Dan Moran（"Makin' Stuff Look Good In Unity"）的早期教程是这个 trick 的源头之一。

## 与其它扭曲技术的关系

- **[[unity-grabpass-blur|GrabPass]] + 位移**——把同样的 `i.uv + displ` 套在 GrabPass 抓到的背景纹理上，物体会变成一块「会扭曲背后画面」的玻璃或者火焰热浪。和后处理版本的差别仅在于纹理来源是物体后面的局部背景，而不是全屏 framebuffer。
- **法线贴图驱动的折射**——更物理地，把法线贴图的 xy 当折射方向，在 shader 里按斯涅尔定律计算出射 UV 偏移。Waving Displacement 是它的「美术友好」简化版本。
- **[[chromatic-aberration-post]]**——本质上也是 UV 位移，只是每个颜色通道用不同的偏移量。把通道偏移和位移合并就是「带色散的折射」。
- **[[texture-dissolve|溶解效果]]**——同一张噪声图既能驱动位移也能驱动 alpha clip，两者经常组合在一支 shader 里做「能量护盾被打破」的复合特效。

## 美术上的用途

UV 位移看上去不起眼，但几乎所有「画面要会动」的效果都能拆成一次位移加一次混合：水面 / 火焰扭曲 / 屏幕受击反馈 / 折射 / 冲击波 / 透视哈哈镜。它便宜（只多一次纹理采样）、表达力强、参数少（一张贴图 + 一个标量 amount + 可选的 mask），是 [[unity-image-effect-basics|image effect 骨架]] 之上最值得最早学会的工具之一。

## 相关

- [[unity-image-effect-basics]]
- [[image-effect-mask-blend]]
- [[unity-grabpass-blur]]
- [[chromatic-aberration-post]]
- [[texture-dissolve]]
- [[fragment-shader]]
- [[uv-manipulation-nodes]]
- [[harry-alisavakis]]
- [[shockwave-effect]] —— 圆环 mask × UV 位移的最经典组合
- [[custom-mask-shaders]] —— 提供 in-shader 圆环 mask 作为位移强度场

## Sources

- [[sources/halisavakis-image-effects-simple-displacement]]
- [[sources/halisavakis-image-effects-waving-displacement]]
