---
tags: [rendering, shader-art, design, composition, color]
date: 2026-04-19
sources: 1
---

# Shader 艺术的五项设计考量

Xor 在 Mini: Design Choices 里汇总了他做 shader art 的**审美自查清单**——不是规则，是每次出片前过一遍、以防漏掉关键点的提纲。和 [[creative-coding-process]]、[[programmer-art-vis-dev]] 互补：前两者讲流程，这页讲「出片时要看的维度」。

## 1. 构图（Composition）

最重要。考虑**焦点位置**和**平衡感**：

- **居中 + 对称** 适合复杂图形、快动画、简单背景。
- **刻意失衡** 能产生张力，但要清楚地「故意」——否则只是不协调。
- **Rule of Thirds** 更适合有机、流动的场景。
- 每次都问：看的人眼睛第一眼落在哪儿？负空间和被裁掉的部分是否都是有意的？

## 2. 光照（Lighting）

- 用 **直方图** 看明度分布（GIMP 能直接看）。多数作品希望覆盖整个 0→255 范围以拿到最饱满的对比。
- 需要变暗变亮就动 [[gamma-correction-srgb|gamma]]：平方更暗更深，开方更亮更柔。
- 高光场景上 [[local-tonemapping|tonemapping]] 防过曝。

## 3. 颜色（Colors）

- **饱和度**、**色温**、**色相**、**调色板**四个维度都要想。
- Xor 本人偏鲜艳，但灰度 + [[chromatic-aberration-post|chromatic aberration]] 做工业感同样有效。
- 调色板用 RGB 三通道不同相位的 cos 生成（iq 的经典套路）：

```glsl
vec3 rainbow = 0.5 + 0.5 * cos(hue + vec3(0.0, 2.0, 4.0));
```

- **色彩渐变叠加**（screen blend 红蓝斜向渐变、或深度方向的雾）能瞬间给作品加上「大尺度性格」。

## 4. 纹理（Textures）

大脑爱 fractal——**多尺度细节**让图在一眼和凑近看都耐看。手段：[[turbulence-domain-warping]]、[[fractal-texturing]]、[[classic-shader-noise|fractal noise]]。出片前把画面缩放到远近两档都看看。

## 5. 动作（Motion）

最主观但最常被滥用。Xor 的建议：

- **默认慢一点**。做得太快会暴露周期性，让人一眼看出「这是算的」。
- 背景慢、抽象可以快、glitch/strobe 可以极快。
- **多时间尺度叠加**：颜色缓慢漂移、形状快速变化，产生层次感。
- 测试法：同一作品分别播 1.5× 和 0.5×，挑喜欢的那档。

## 和其它 Xor 页的关系

- [[programmer-art-vis-dev]]：面向游戏里视觉传达的姐妹篇。
- [[creative-coding-process]]：做一个 shader 作品的时间轴流程。
- 本页是**成品前的五维自查**；那两页是**过程方法论**。

## Sources

- [[sources/xor-mini-design-choices]]
