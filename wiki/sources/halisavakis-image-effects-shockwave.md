---
tags: [source, 渲染, unity, shader, 后处理, 冲击波, vfx]
date: 2026-04-14
sources: 1
---

# My take on shaders: Shockwave effect (Harry Alisavakis)

[[harry-alisavakis]] *My take on shaders* 系列第七篇（2017-06-21），把前几篇的 [[custom-mask-shaders|圆环 mask]] 与 [[uv-displacement-image-effect|UV 位移]] 拼到一起，做出经典的 2D 冲击波命中反馈效果。

## 摘要

Alisavakis 自嘲这篇是「拿前两支 shader 凑合出一篇文章」，实际上确实——shader 主体就是 ring mask 的复制粘贴，再多加最后两行：把 mask 灰度乘上 `_DisplacementAmount` 当 UV 偏移，重新采样 framebuffer。圆环外侧 mask 为 0 不动；圆环中心带 mask 最大、被最大幅度位移；中间过渡。视觉上就是一圈窄环把屏幕扭一下，配合脚本驱动 `_Radius` 从 `-0.2f` 单调线性插值到 `2f`，圆环从「不可见」扩散到「冲出屏幕」，整套动画就完成了。配套的 C# 脚本演示了几个工程细节：用 `StopAllCoroutines()` 防连续点击叠加；从 `Input.mousePosition` 除以 `Screen.width/Height` 得到归一化 UV 坐标传给 shader 的 `_CenterX/_CenterY`；起止半径都故意取屏幕外的值让动画自动「淡入淡出」。文末作者强调：这个效果单看很弱，配合屏幕震动 / 色差 / 闪白才有命中力度。

## 关键要点

- shockwave shader = ring mask shader + 最后两行 UV 位移；物理上是「圆环 mask 驱动的径向 UV 扰动」。
- 用 `(mask, mask)` 的非径向位移就能在视觉上骗过眼睛——环形 mask 的几何对称性让结果看起来像在向外推。
- 触发脚本的工程细节：`StopAllCoroutines()`、起止半径取屏外值、center 用 `[0,1]` 屏幕 UV 而不是像素。
- 演示了 shader 模块化的思路：把每一层（mask 形状 / 位移规则 / 触发逻辑）解耦，之后能独立替换、派生出大量变体。
- 单层效果不够「爽」，需要和 [[chromatic-aberration-post|色差]]、屏幕震动、闪白等堆叠才能形成强力反馈。

## 链接到的概念

- [[shockwave-effect]]
- [[custom-mask-shaders]]
- [[uv-displacement-image-effect]]
- [[image-effect-mask-blend]]
- [[unity-image-effect-basics]]
- [[chromatic-aberration-post]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-shockwave-effect/>
- 本地：`raw/articles/halisavakis.com/2017-06-21_my-take-on-shaders-shockwave-effect.md`
