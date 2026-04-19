---
tags: [渲染, unity, 后处理, glitch, vfx, 屏幕效果]
date: 2026-04-14
sources: 1
---

# Glitch 后处理（Glitch Image Effect）

"故障"视觉是把一张完好的 framebuffer **按照某种结构化噪声打碎**——水平撕裂、波浪抖动、颜色通道错位——冒充一台正在坏掉的显示器或一段松了的 VHS 磁带。[[harry-alisavakis|Harry Alisavakis]] 在 *My take on shaders* 第九篇里提出了他自己的 glitch 后处理的"三件套"组合：**两套 [[random-stripes-mask-shader|随机条纹 mask]] + [[uv-displacement-image-effect|波浪 UV 位移]] + [[chromatic-aberration-post|色差]]**。三者叠在一次 pass 里，最后挂一个**单一标量控制器**，让外部脚本用一个从 0 到 1 平滑变化的值推动整段 glitch 从"静"到"最失真"。

## 三层叠加的动机

Glitch 看起来复杂，是因为它是三类**互相独立的失真**同时发生的结果。拆开来看每一类都很朴素，真正贴合"坏掉的显示器"的是三者一起出现：

1. **水平撕裂**（stripes displacement）——一些横向行向左跳、另一些向右跳，模拟信号在行扫描时错位。用两张随机条纹 mask 做开关：`right` mask 标记哪些行向右偏移、`left` mask 标记哪些行向左偏移。两组 fill 参数允许上下撕裂强度不同。
2. **波浪扭曲**（wavy displacement）——整帧沿 Y 轴被 `sin(uv.y * freq)` 调制的横向正弦波拉扯，像热浪或松掉的磁带。Alisavakis 用一张 `lerp(red, green, (sin(uv.y*f)+1)/2)` 的 R/G 双通道遮罩同时承载「向上偏」和「向下偏」两个方向，然后 `R*up - G*down` 把它变成一个连续的位移向量。
3. **[[chromatic-aberration-post|色差]]**——最后对每个像素按 R / G / B 通道各采一次不同偏移，让颜色错开几个像素的宽度。这是所有 glitch 视觉里几乎必备的"签名味道"，因为真实的 RGB LCD panel 一旦信号丢失就会露出亚像素结构。

三者的顺序很关键：**条纹位移和波浪位移先把 UV 算好，再交给色差三次采样**。如果倒过来做（先色差再位移）就会得到糊成一团的结果——条纹位移必须在采样 framebuffer 之前完成。

## 单旋钮控制器：分阶段解锁

朴素地让美术调 9 个 uniform 会很累，也没法让 glitch 平滑地从无到强。Alisavakis 的办法是引入一个标量 `_GlitchEffect`，让脚本从 C# 每帧喂一个 `[0, N]` 的值，shader 内部**按 `frac(_GlitchEffect)` 对不同阈值分档**解锁失真种类：

```hlsl
if (frac(_GlitchEffect) < 0.8) {
    rightStripesFill = lerp(0, _RightStripesFill, frac(_GlitchEffect) * 2);
    leftStripesFill  = lerp(0, _LeftStripesFill,  frac(_GlitchEffect) * 2);
}
if (frac(_GlitchEffect) < 0.5) {
    chromAberrAmount = lerp(0, _ChromAberrAmount, frac(_GlitchEffect) * 2);
}
if (frac(_GlitchEffect) < 0.33) {
    displAmount = lerp(0, _DisplacementAmount, frac(_GlitchEffect) * 3);
}
```

- `frac(x)` 把无界的驱动值拉回 `[0, 1]` 的小周期，可以通过递增 `_GlitchEffect` 在一段连续时间内重放同一组随机模式。
- 三个分段阈值 **0.33 / 0.5 / 0.8** 是作者拍脑袋试出来的——数值本身无意义，工程意义是：越"便宜"的失真（条纹）越容易被触发，越"显眼"的失真（整帧位移）只有在最高强度才出现；递进感与"信号越坏，症状越多"的直觉一致。
- 每段内部还做一次 `lerp(0, target, frac*系数)`——让这档内部也能平滑放大，不是一个硬开关。

配合脚本每秒把 `_GlitchEffect` 从 0 线性推到 5，就得到"时而正常、时而失真、时而狂乱"的节奏化 glitch；或者喂一个柏林噪声，得到随机的气泡式故障。把复杂效果压缩到一维驱动是 [[shaping-functions|shaping function]] 思想在动画层面的一次具体应用。

## 为什么要三个 pass 合并

同一帧里跑三次全屏 pass 也能达到同样的视觉，但 Alisavakis 把它们塞进**一个 fragment shader**——对 framebuffer 只读一次（实际上读三次，因为色差），不走多次 blit。代价是代码长、uniform 多；收益是**移动 GPU 友好**，而且三个效果之间的中间量（如位移后的 UV）可以共享。这也呼应了 [[unity-postprocessing-adventures|Unity 后处理调优]] 里反复强调的原则：能并入同一个 fragment 的 full-screen pass，不要拆成多个 blit。

## 相关

- [[random-stripes-mask-shader]] —— 水平撕裂的底层积木
- [[uv-displacement-image-effect]] —— 波浪位移的通用形态
- [[chromatic-aberration-post]] —— 第三层失真，数字派色差
- [[image-effect-mask-blend]]
- [[unity-image-effect-basics]]
- [[crt-shader-effects]] —— 另一类"故障 CRT" 着色器
- [[shaping-functions]] —— 用单标量驱动多段行为
- [[shader-color-interpolation]]
- [[harry-alisavakis]]
- [[volume-mask-layers]] —— Snapshot 2 glitch effect 可按 layer 限制作用范围

## Sources

- [[sources/halisavakis-glitch-image-effect]]
- [[sources/danielilett-snapshot2-glitch]] —— 同类 glitch 效果的三段独立子效果产品化版本（offset texture / slice band / block artifact）
