---
tags: [渲染, 颜色, dither, 后处理, shader]
date: 2026-04-14
sources: 1
---

# 色带（Color Banding）与 shader 去色带

**色带**（color banding，又称 **posterization**）是指本应连续的色彩渐变在显示上被切成一圈圈清晰的同色阶梯。它的根源只有一个：**量化**——当编码位深（8-bit / 6-bit）不足以覆盖人眼在该亮度段的分辨率时，两个相邻 code point 之间的差异就跨过了「刚可察觉差异」（JND）的门槛，视觉上立刻变成台阶。深色大面积渐变（夜景、暗角、fog falloff、blur 背板、软半径 vignette）是重灾区——[[frost-kiwi|Frost]] 在文章开头那个半圆径向渐变只有 `vec3(0.15)` 到 `vec3(0.2)` 的跨度，却在 8-bit 面板上直接摆出一打台阶。

## 一行 GLSL 去色带：Interleaved Gradient Noise

Frost 文章的核心产出是 Jorge Jimenez 在 *Call of Duty: Advanced Warfare* 里使用的 **Interleaved Gradient Noise**——一种介于「有序 dither」和「伪随机 dither」之间的噪声，可以用一行 GLSL 写完：

```glsl
float gradientNoise(in vec2 uv) {
    return fract(52.9829189 * fract(dot(uv, vec2(0.06711056, 0.00583715))));
}
```

直接把它以 **一个 8-bit 量化步**（`1.0/255.0`）的幅度叠加到渐变上，并减去半步 `0.5/255.0` 以保持平均亮度：

```glsl
bgcolor += (1.0 / 255.0) * gradientNoise(gl_FragCoord.xy) - (0.5 / 255.0);
```

整个处理在 **fragment shader 里一次写完**、不需要额外贴图 tap、不需要任何 buffer。噪声的量级恰好只填满量化台阶之间的空隙，所以肉眼几乎看不出噪点，却能把所有台阶完全打散。相对于真正的 **error diffusion**（Floyd-Steinberg 等）——这些算法是顺序依赖的，没法在 GPU 上并行做；以及 **有序 Bayer dither**（见 [[dither-alpha-clipping]]）——固定图案在静态画面下非常容易被人眼察觉——interleaved gradient noise 是实时渲染里最划算的方案。

## 不要 double dither：6-bit 面板的诅咒

一个容易忽略的坑：很多笔记本（甚至工作站级别的 HP Zbook Fury）用的其实是 **6-bit 面板 + FRC**（frame rate control）在时间域上 dither 伪装成 8-bit 输出。shader 侧的去色带 dither **和面板自带的时间 dither 打架**——两种周期性噪声在色阶边界处形成干涉条纹（moiré / sawtooth）。把 shader 的 dither 幅度改成 6-bit（`1.0/63.0`）反而更糟，因为双倍的噪声幅度反过来被面板 FRC 放大成明显的斜纹。结论：**6-bit 面板就认倒霉**，不要为它调参数。

## 业界都怎么干

Frost 在文章后半部分横向对比了一圈「大厂做法」：

- **Valve**（*The Lab*, Alex Vlachos GDC 2015）——Portal 2 360 时代的 7 条汇编指令 RGB dither，三个通道用不同质数 `(103, 71, 97)` 去相关，再用 `g_flTime` 让 pattern 每帧抖动。
- **Alien: Isolation**（Creative Assembly）——同一个引擎里三条路：暴力糊 film grain（作者本人不喜欢，太吵）；开启 *Deep Color* 10-bit 输出（要求关掉 AA，因为它的 AA shader 会把信号砸回 8-bit，前功尽弃）；或什么都不做留色带。
- **ReShade Deband.fx**（haasn / JPulowski）——后处理钩子，先用 **Weber ratio** + 标准差检测平坦区域，只在检测到的带内 pixel 上应用 ordered dither，不影响已经高频的内容。
- **After Effects Gradient Ramp 的 Ramp Scatter**——文档里说它「只对检测到的色带做 dither」，但性能非常糟糕（4K 单帧 0.25s），疑似某种迭代算法。
- **KDE Plasma（KWin）Blur**——**Dual Kawase blur** 本身就会产生容易出带的软渐变，官方实现直接在 blur 之后叠一层噪声；这和 **Microsoft Windows 11 Acrylic** 的 blur + noise 组合是一样的思路。

## 16-bit 测试图

作为附录，Frost 做了一张 16-bit PNG 测试图：整张图是 0-256 之间的灰度渐变，每 4 个像素换一次值。在 8-bit 屏上应该看到 **3 条带**，10-bit 上 **9 条**，12-bit 上 **33 条**——而且两端带是中间带的一半宽度（因为渐变端点恰好落在整数 code point 上）。这是一套零设备成本的面板位深自检法，直接用手机相机翻拍屏幕就能读。

> 同一台屏在 Firefox 和 Edge 下条带的位置会偏——因为 Edge 的颜色管理把 sRGB 当成 γ=2.2 纯幂函数解码，而真正的 sRGB 曲线是分段的，两者在暗部会差一个 code point 量级。

## 和 wiki 其他条目的关系

- 和 [[dither-alpha-clipping]]：都用 dither，但目标相反——alpha clipping 是把连续 alpha 量化成二值 `discard`，去色带是把量化阶梯恢复为连续感知。
- 和 [[retro-rendering-techniques]]：复古渲染是**刻意**保留色带（甚至主动量化到 5-bit）制造怀旧感，去色带是**消除**色带。
- 和 [[color-space]] / [[display-edid-colorspace]]：EDID 告诉你面板位深声明是多少，但 FRC 6-bit 面板会对你撒谎；sRGB 分段曲线比 γ=2.2 更贴暗部，因此同一色带在正确和错误的 TRC 下位置会偏移。

## Sources

- [[sources/frost-kiwi-color-banding]]
