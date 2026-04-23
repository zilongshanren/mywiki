---
tags: [渲染, shader, GLSL, 导数, mipmap]
date: 2026-04-19
sources: 1
---

# texture2DGradARB 与不连续 UV 的 LOD

[[ben-supnik|Supnik]] 描述了一个在 X-Plane 中反复碰到的 shader artifact：当 UV 坐标被 `fract()` 或 swizzle 处理成**不连续**时，硬件自动选择的 mip LOD 会在不连续缝隙处掉到最低级，产生一条**低分辨率伪影带**。

## 硬件如何推导 LOD

大多数 GPU 用 **2×2 像素 quad 的交叉差分**计算 `dFdx` / `dFdy`：把同一个 shader 同时跑在 4 个相邻像素上，取值相减。采样器在 texture fetch 时对传入的 UV 做同样的差分，**差分越大 → 屏幕单位下每像素覆盖越多纹理像素 → 选更低分辨率的 mip**。

这就是为什么你写任意复杂的 UV 表达式，mip 选择都「自动能工作」——硬件对整个表达式做差分。

这也是为什么 shader bug 经常表现为 **2×2 的块状 artifact**：一个 quad 内部各 lane 间的差分出了问题。

## 不连续的代价

考虑最简单的 wrap 纹理：

```glsl
vec2 uv_swizzled = fract(uv);
vec4 rgba = texture2D(my_tex, uv_swizzled);
```

绝大多数像素差分很小，mip 选得对。但在 `fract` 的跳跃点（UV 从 0.999... 到 0.000...），**同一个 quad 内的差分突然变成约 1.0**——硬件认为「这一像素覆盖了整个纹理」，直接采最低 mip。那一条像素带因此看起来糊掉。

## 解法：手喂正确的导数

`GL_ARB_shader_texture_lod` 提供 `texture2DGradARB`，允许**把采样坐标与用于 LOD 的导数解耦**：

```glsl
vec2 uv_swizzled = fract(uv);
vec4 rgba = texture2DGradARB(my_tex, uv_swizzled, dFdx(uv), dFdy(uv));
```

采样用「跳跃后」的 UV，但 LOD 用「原始连续」UV 的导数。两家厂商（NVIDIA / ATI）在不连续 UV 上的行为不同但都会出 artifact，显式导数能同时摆平两家。

这和硬件 antialiasing 里 [[fwidth-derivative-antialiasing]] 用导数做像素宽度估算是同一族技巧：**把你对坐标变化率的领域知识显式提供给硬件**，而不是让它从一个你知道是坏的表达式里猜。

## 一个重要的限制

spec 指出：mipmap / 各向异性 texture fetch 的隐式导数**在 non-uniform control flow 里未定义**，在 vertex shader 里也未定义。Supnik 说他怀疑自己遇到的很多 shader artifact 就来自**同一 quad 内 branch 走向不一致**——这些像素跑的根本不是同一组指令，差分就没意义了。对这种情况，解决办法同样是：别让硬件隐式差分，自己用 `texture2DGradARB` 显式传。

## 相关

- [[fwidth-derivative-antialiasing]] — 用 fwidth 估算像素覆盖做抗锯齿
- [[uv-precision-derivative-loss]] — 另一种导数失效：UV 精度不够
- [[ben-supnik]]

## Sources

- [[sources/supnik-change-uv-map-on-fly]]
