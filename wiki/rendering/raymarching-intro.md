---
tags: [渲染, shader, raymarching, sdf, 3d]
date: 2026-04-14
sources: 1
---

# Sphere-assisted Raymarching 入门

**Raymarching** 是 shader 艺术家最爱的 raycasting 算法之一：它不依赖三角形管线，纯靠一个「返回到最近表面距离」的函数就能在 fragment shader 里渲染任意 3D 几何。相比解析 raycast（只对能写出闭式交点的形状有效）、相比 voxel 遍历（精度受限于网格），raymarching 的门槛低、表达能力强，而且能**顺手产出 soft shadows、glow、AO** 这类额外效果。[[xor-shader-artist|Xor]] 的这篇 mini 教程把核心思想浓缩在一页代码里：基于 **SDF（Signed Distance Field）** 的 **sphere tracing**。

## SDF：形状 = 一个距离函数

原点的单位球写成 SDF 就一行：

```glsl
float sphere_distance(vec3 p) {
    return length(p) - 1.0;
}
```

语义很直接——`length(p) == 4.0` 说明采样点离表面还有 3，`length(p) == 0.5` 说明已经在球内 0.5 深度处。**负值代表内部**，是「signed」的来历。两个球的并集写成 `min(d1, d2)`——谁更近就听谁的。同样一套思路 Inigo Quilez 推广出了[一整个基元库](https://iquilezles.org/articles/distfunctions/)。2D 场景下的 SDF 见 [[sdf-2d-primitives]]。

SDF 的优雅之处：**形状的布尔运算退化成了函数组合**。并 = `min`、交 = `max`、差 = `max(a, -b)`、偏移 = `d - r`、反相 = `-d`。没有网格 stitching，没有自交检测。

## Sphere tracing：为什么「沿距离前进」是安全的

核心观察：SDF 在点 `p` 的值 `d` 告诉你——以 `p` 为圆心、`d` 为半径的球内保证没有表面。所以**从 `p` 向任意方向最多可以安全前进 `d`**，不会穿过任何东西。

这就给出了 Xor 的 8 行 raymarcher：

```glsl
vec4 raymarch(vec3 pos, vec3 dir) {
    float d = 0.0;
    for (int i = 0; i < 100; i++) {
        float step_dist = distance_field(pos + dir * d);
        d += step_dist;
        if (step_dist < EPS || d > MAX) break;
    }
    return vec4(pos + dir * d, d);
}
```

每次步进**严格等于**当前 SDF 值——永远不过头。`EPS` 提前终止：到表面足够近就算命中。`MAX` 防止打空时死循环（射线根本打不到任何东西）。名字里的「sphere」来自「每步走一个安全球」——这和 [[volumetric-raymarching-intro|固定步长的朴素 raymarching]] 形成对比，后者不管远近都走 `0.01`，浪费极其严重。

## 为什么这么流行

- **廉价出效果**：一次 raymarch 顺便得到 surface point、depth、法线（用 SDF 的中心差分 gradient 得到）。这些都是[[sdf-ray-marched-shadows|软阴影]]、glow、AO 的直接输入。
- **函数即场景**：整个场景在 shader 代码里——无需传顶点缓冲、无需索引。非常适合 Shadertoy 单文件 demo。
- **和分辨率解耦**：SDF 是解析函数，放大不会出锯齿；远距离的质量只受迭代次数和浮点精度限制。
- **组合性**：并、交、差、平滑并（`smin`）、无限复制（`length(mod(p, 8.0) - 4.0) - 0.5`）全是函数组合。

## 射线方向：从 pixel 到 ray

raymarcher 需要每像素一条射线。最小版本就是「把屏幕当一个 pinhole [[pinhole-camera|针孔]]」：

```glsl
vec3 dir = normalize(vec3(pixel.xy - 0.5 * resolution.xy, resolution.y));
```

`pixel.xy - 0.5*res.xy` 把原点挪到屏幕中心；`resolution.y` 作为 z 分量定义了**焦距**（越大 FOV 越窄）。得到的方向可以再乘一个 view matrix（见 [[3d-rotation-math]]）做摄像机旋转。

## 常见套路清单

Xor 在文末列了几个「学会 raymarching 之后马上会用到的」技巧：

- **反相**：`radius - length(p)`，空间内部变空洞。
- **差集**：`max(a, -b)` 在形状 A 上挖掉 B。
- **无限复制**：`p = mod(p, period) - period/2`，一行代码铺满整个空间。一个球变成无限多个。
- **平滑并**：用 `smin(a, b, k)`（多项式或指数版本）代替 `min`，两个球融成 metaball。

这些都在 SDF 层面完成，raymarcher 本身不需要改。这就是为什么一套 shader 能渲染极其复杂的场景——复杂性在**函数组合**里，不在循环结构里。

## 和 2D、体积 raymarching 的关系

Raymarching 的 API 对 2D、3D、体积三种情形几乎是同一套——换的只是 `scene()` 函数的返回值和后处理：

- **2D SDF**：向量换成 `vec2`，循环结构不变。常见用途是 2D SDF 软阴影（见 [[sdf-ray-marched-shadows]]）或字体渲染。
- **3D 表面 raymarching**（本页主题）：命中 `d < EPS` 即停，用 SDF gradient 取法线做 shading。
- **[[volumetric-raymarching-intro|体积 raymarching]]**：不停循环，**沿途对密度做积分**（吸收/散射），直到射线走出体积或累计不透明度饱和。适合雾、云、plasma ball。

三者共享同一套「步长 = 安全距离」的核心——raymarching 的真正精妙在于**安全步长的定义**，具体做什么取决于每次迭代的 payload。

## 相关

- [[sdf-2d-primitives]] —— 2D SDF 基元与变换
- [[sdf-ray-marched-shadows]] —— 把 raymarching 用在阴影计算
- [[volumetric-raymarching-intro]] —— 体积渲染的 raymarching 变体
- [[jump-flooding-algorithm]] —— 另一条生成距离场的路线
- [[fragment-shader]]
- [[pinhole-camera]]
- [[3d-rotation-math]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-raymarching]]
