---
tags: [渲染, shader, blur, post-processing, 优化, gamemaker]
date: 2026-04-19
sources: 1
---

# 利用双线性插值降采样数的 Blur 优化

"模糊越大越贵" 并不是必然的——前提是你把 GPU 的 **texture interpolation**（硬件双线性）当成免费算力来用。[[xor-shader-artist|Xor]] 在 Blur Philosophy 第二篇里把这条优化讲得很具体：**在两个 texel 之间采样一次**，就等价于加权平均这两个 texel；把它推广到 2D，一次 `texture2D` 就能覆盖 4 个相邻 texel 的加权和。这是所有高质量、可分离、硬件可用的 blur shader 背后共同的省采样原理，和 [[separable-gaussian-blur]] 的空间分离正交——两个机制叠起来，一个 17-tap 2D Gaussian 可以从 289 次采样降到 18 次甚至更少。

## 在 texel 中间采样：一次采样覆盖 4 个 texel

把采样点从 texel 中心（整数坐标）移到两个 texel 交界（0.5 偏移），硬件双线性插值会把两个 texel 按距离做线性混合。把这套思路向 2D 扩展，采样 `uv + (±0.5, ±0.5) * texelSize` 这 4 个点，每一点实际是 4 个相邻 texel 的均值；四个采样合起来覆盖一个 3×3 的邻域，而中心 texel 在四个采样里都出现，外边中点 texel 出现两次，角 texel 各一次——自然形成一个 **4:2:1 权重**，和离散 Gaussian 的形状已经很接近。

Xor 给的 GLSL 片段：

```glsl
vec4 tex_sum = vec4(0);
const vec2 off = vec2(-0.5, 0.5);
tex_sum += 0.25 * texture(tex, uv + off.xx * texel);
tex_sum += 0.25 * texture(tex, uv + off.yx * texel);
tex_sum += 0.25 * texture(tex, uv + off.xy * texel);
tex_sum += 0.25 * texture(tex, uv + off.yy * texel);
```

4 次采样覆盖 9 个 texel，**免费拿到一个近似 Gaussian**——比显式写 9-tap box blur 快一倍多；如果需要每样本等权，把 ±0.5 换成 `±sqrt(0.5) ≈ ±0.707` 即可。

## 前提：纹理插值必须打开

GameMaker 里对应 `gpu_set_texfilter(true)`；OpenGL 是 `GL_LINEAR` min/mag filter；点采样（`GL_NEAREST`）下这个优化失效，采样点会 snap 到最近 texel，等于没做插值平均。移动端和 Switch 尤其怕 texture fetch 多，这个优化值几倍帧率。

## 和可分离 Gaussian 结合：Linear Sampling Trick

可分离 Gaussian 把 N² 采样降到 2N，再叠上双线性采样，每 pass 的 N 次采样可以**两两合并**成 `ceil(N/2)` 次，公式是 `w_ab = w_a + w_b`，`offset_ab = (a*w_a + b*w_b) / w_ab`——把相邻两个 texel 的权重和当成一次采样的权重，采样位置按权重加权居中。这样一个 17-tap 1D Gaussian pass 只要 9 次采样；两 pass 共 18 次。典型的 bloom/DOF/SSR 里看到的"`linearSampling`"或"`Rastergrid blur`"都是这招。

## 多 pass 指数扩展半径

即便每 pass 只覆盖 3×3，重复跑 N 次（**ping-pong**，见 [[ping-pong-surfaces]]）后有效半径按 N 倍扩展。Xor 暗示的更激进做法是在 [[mipmap-generation-sampling|mipmap]] 上做 blur——每下一级分辨率减半，半径自动翻倍，是 Dual-Kawase 的基础。这和"简单暴力扩大 kernel"相比，计算量增长由 `O(r)` 降到 `O(log r)`，是大半径模糊的唯一可行路径。

## 权衡

这条优化本质是用**硬件插值误差**换采样数量。对 HDR bloom、glow、depth blur 这类最终要经过色调映射的效果，插值误差完全被后处理吃掉；但如果你在做**精确的卷积**（比如需要可重复验证的后处理单元测试、或者 bilateral filter 里要同时读 color 和 depth），插值会把邻域混进来，这时必须退回到点采样 + 显式平均。

## 相关

- [[separable-gaussian-blur]] —— 可分离性把 N² 降到 2N，本页再叠一层硬件插值
- [[mipmap-generation-sampling]] —— 下采样金字塔是大半径的"免费"半径扩展
- [[ping-pong-surfaces]] —— 多 pass 叠加扩展有效半径
- [[bloom-threshold-blur-composite]] —— bloom 是这套优化的典型应用
- [[sampler-filter-wrap-modes]] —— 打开 linear filter 是前提
- [[image-convolution-kernel]]

## Sources

- [[sources/xor-mini-blur-philosophy-2]]
