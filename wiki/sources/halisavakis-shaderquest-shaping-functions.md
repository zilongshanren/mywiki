---
tags: [source, rendering, shader, tutorial]
date: 2026-04-14
sources: 1
---

# ShaderQuest Part 6: Shaping functions（Harry Alisavakis / Technically Art）

[[harry-alisavakis]] 于 2021 年 9 月发表的 ShaderQuest 系列第六篇，面向着色器初学者讲解**塑形函数（shaping functions）**——把标量输入映射为输出的基础数学原语。

## 摘要

这篇教程把着色器中最常用的几种塑形函数逐一讲清：**step** 做硬阈值，**smoothstep** 做三次多项式平滑过渡（退化情形等价于 step）；**lerp/mix** 做线性插值，**inverse lerp** 做反向插值并把任意区间重映射到 `[0, 1]`；**sin/cos** 提供周期信号，用于呼吸、水波、闪烁等动画；**frac/fract** 返回小数部分，得到锯齿波，并可通过 `abs(frac(x) - 0.5) * 2.0` 转成三角波；此外还有 **min/max/floor/ceil** 等基础函数。作者强调这些函数既能单独用 UV 喂入做静态渐变，也能加上引擎提供的时间变量（Shadertoy 的 `iTime`，Unity 的 `_Time`）立刻做出动画效果。每个函数都配有 Shadertoy 交互示例和 Unity Shader Graph 节点截图。

## 关键要点

- smoothstep 的缓动公式是 `t*t*(3.0 - 2.0*t)`，在端点处导数为零，比 step 更适合抗走样
- lerp 的线性插值公式：`(1 - t) * a + t * b`
- Unity HLSL 没有内置 inverse lerp，需要手写 `(x - a) / (b - a)`
- sin/cos 的输入是弧度，习惯上乘以 π 或 τ 使频率可预测
- sin/cos 返回 `[-1, 1]`，通常要重映射到 `[0, 1]`
- frac 能把任意数值周期性折叠到 `[0, 1)`，既可用于平铺也可用于调试
- 时间变量是着色器动画的关键：把 `time` 加进任何函数的输入就能让静态效果动起来
- 作者推荐参考 [Book of Shaders](https://thebookofshaders.com) 的交互式编辑器

## 链接到的概念

- [[shaping-functions]]
- [[fragment-shader]]
- [[aliasing]]

## 原文

- 链接：<https://halisavakis.com/shaderquest-part-6-shaping-functions/>
- 本地：`raw/articles/halisavakis.com/2021-09-12_shaderquest-part-6-shaping-functions.md`
