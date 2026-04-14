---
tags: [source, 渲染, unity, shader, mask, 随机, 噪声]
date: 2026-04-14
sources: 1
---

# My take on shaders: Random stripes mask (Harry Alisavakis)

[[harry-alisavakis]] *My take on shaders* 系列 2017-08-26 的一篇，Alisavakis 从 Book of Shaders 得到灵感，把一维伪随机 hash 搬进 Unity fragment shader，做出一张能驱动下游效果的随机条纹 mask。

## 摘要

shader 极小：定义 `random(float2) = frac(sin(dot(x, k12)) * big)` 的一维 hash，然后 `floor(i.uv.y * _Frequency)` 把屏幕切成等高条带并给每条一个整数 ID，`step(_Fill, random(ID))` 把这些条带随机置 0 或 1，最后 `1 - step(...)` 反一下得到白条黑底的 mask。两个参数 `_Frequency`（条带数量）和 `_Fill`（阈值，越大白条越少）就是全部可调项。Alisavakis 自己承认这支 shader 自身没什么看头——"填屏幕黑白条"——它的全部价值在于为后续 [[glitch-image-effect|glitch effect]]、CRT 模拟、行级 UV 扰动等提供一个**逐行的二值噪声源**。文末明确说"this will be a good entry point to other cool effects using randomness and a bit of math"，是一个承上启下的小积木文。

## 关键要点

- `frac(sin(dot(x, float2(12.9898, 78.233))) * 43758.5453)` 是 shader 里事实标准的一维伪随机 hash（源自 Book of Shaders Chapter 10）。
- `floor(uv.y * freq)` 把连续坐标量化成条带 ID，让同一条内所有像素拿到同一个 hash 结果 —— "条带内相关、条带间独立"的结构正是这种 mask 想要的。
- `step(_Fill, r)` 是二值化；`1 - step(...)` 只是语义反转，让美术以"白条比例 = 1 - _Fill"的方式设置。
- 单看这张 mask 无用，它是**下游乘子**：glitch 的横向位移开关、CRT scanline、行级 color noise 的权重。
- `sin` 精度坑在移动 GPU 上要换 integer hash（[[pcg3d-hash]]）才稳。
- 灵感显式来自 thebookofshaders.com——Alisavakis 诚实标注"If you're really interested in figuring it out, you can check the explanation given here"。

## 链接到的概念

- [[random-stripes-mask-shader]]
- [[glitch-image-effect]]
- [[shader-color-interpolation]]
- [[pcg3d-hash]]
- [[shaping-functions]]
- [[unity-image-effect-basics]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-random-stripes-mask/>
- 本地：`raw/articles/halisavakis.com/2017-08-26_my-take-on-shaders-random-stripes-mask.md`
