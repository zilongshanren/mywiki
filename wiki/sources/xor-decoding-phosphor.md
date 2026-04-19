---
tags: [source, 渲染, shader, raymarching, 创意编程]
date: 2026-04-19
sources: 1
---

# Decoding: Phosphor（Xor）

[[xor-shader-artist|Xor]] 2025 年 7 月的技术拆解，把自己的 258 字符 tweet shader 「Phosphor」一行一行解释清楚——它塞进了 raymarch 循环、glow 衰减、3D 场景旋转、相机位移、湍流、3D 圆环粒子分布。

## 摘要

Phosphor 的完整代码是一个 for 循环，用 [[tweet-shader-280-char|tweet shader]] 的所有常用 idiom：`INIT; COND; LAST` 三段全被塞满。核心是 80 步的 raymarch：每一步取 ray direction 上的采样点 `p = z * normalize(FC.rgb*2 - r.xyy)`（标准相机射线的压缩形式），计算"twisting 旋转轴 `a`" 并对 `p` 应用一个硬编码 270° 角度的简化 3D 旋转公式 `a = a*dot(a,p) - cross(a,p)`（等价于完整的 `mix(a*dot(p,a), p, -cos(t)) + sin(t)*cross(p,a)` 在 $t = 270°$ 时的特例）。接着 [[turbulence-domain-warping|湍流 domain warp]] `a += sin(a*d+t).yzx/d`（`d` 从 1 到 9 迭代）为采样点注入流体扰动。距离估计是 `0.05*|length(p)-3| + 0.04*|a.y|`——空心球 SDF 加一个扰动平面。颜色按步长距离做相位偏移 `cos(d/.1 + vec4(0,2,4,0))+1` 并除以距离作光衰减、乘 `z` 使近处淡出。最后 `tanh(o/1e4)` tonemap。Phosphor 2 和 Nucleus 是同架构的变种。

## 关键要点

- **3D rotation 压缩**：硬编码特定角度让 `cos/sin/mix` 全消失，只剩 `a*dot(a,p) - cross(a,p)`。
- **多任务 for 循环**：`INIT` 初始化三变量、`LAST` 做颜色累积、循环体做 raymarch——三段全用尽。
- **湍流 domain warp** 9 个 octave 嵌套，`a += sin(a*d+t).yzx/d`。
- **空心球 + 平面距离场**：`|length(p)-r|` 让 ray 能穿过壳做 volumetric 效果，再加平面项做复合形状。
- **距离估计有意缩小**（0.05 / 0.04 因子）——扰动过大会让朴素 sphere tracing overshoot，需要保守步长。

## 链接到的概念

- [[tweet-shader-280-char]]
- [[density-field-volumetric]]
- [[turbulence-domain-warping]]
- [[hyperbolic-tangent-shader]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/decoding-phosphor
- 本地：`raw/articles/mini.gmshaders.com/2025-07-26_decoding-phosphor.md`
