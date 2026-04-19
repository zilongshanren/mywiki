---
tags: [渲染, shader, sdf, 距离场, 2d]
date: 2026-04-14
sources: 1
---

# 2D SDF 基元与空间变换

**Signed Distance Field (SDF)** 把一个形状表示成一个函数 `d(p)`：传入空间点 `p`，返回它到最近表面的**有符号**距离——外部为正，表面为 0，内部为负。相比多边形网格，SDF 可以被光滑地合并、求差、求偏移，允许廉价 raymarching，也支持低分辨率纹理 + 高质量采样（text rendering 的经典技巧）。本页整理 Ronja 教程里覆盖的 2D SDF 基础：圆和矩形的 SDF、translate/rotate/scale 空间变换，以及两种常见的可视化手法。它是后续 [[sdf-ray-marched-shadows|SDF 软阴影]] 和 SDF 布尔运算的地基。

## 圆与矩形：最小可用的 SDF 集

**圆**是最平凡的例子——`length(p) - radius`，几何上就是「到原点的欧氏距离再减半径」。radius 越大等值面 `d=0` 越远，内部区域获得负值。

**矩形**复杂一点。直觉上可以写成 `max(|x|-hx, |y|-hy)`——这给出正确的外部距离的单轴度量，但在四个角外会低估距离，且在整个矩形内部都等于 `max(...)`。Ronja 给的「正确版」是：

```hlsl
float2 e = abs(p) - halfSize;
float outside = length(max(e, 0));   // 外部：欧氏距离
float inside  = min(max(e.x, e.y), 0); // 内部：负的最大投影
return outside + inside;
```

- **外部**：把每个分量拉到非负（`max(e, 0)`）后取长度——这是到最近角或最近边的欧氏距离。
- **内部**：`max(e.x, e.y)` 在内部是负数（两个分量都 ≤ 0），代表到最近一条边的「垂直距离的负值」。
- 外部项内部为 0，内部项外部为 0，两者相加既覆盖外部的欧氏距离，又覆盖内部的带符号距离，这是一种**分段合成、利用 min/max 自动屏蔽**的典型 shader 写法。

真正的 2D SDF 基元清单（[Inigo Quilez 有完整列表](https://iquilezles.org/articles/distfunctions2d/)）远不止这两个——椭圆、胶囊、扇形、星形都有解析解。圆和矩形只是让人能动起来的最小集合。

## 空间变换：动形状不如动坐标

移动一个形状最直接的方式是在形状的函数里加平移参数。但 Ronja 用了一个更干净的抽象：**把变换写成作用在采样点上的函数**。

```hlsl
float2 translate(float2 p, float2 offset) { return p - offset; }
float2 rotate   (float2 p, float rot)     { ... 反向旋转 p ... }
float2 scale    (float2 p, float s)       { return p / s; }
```

注意它们都是**逆变换**——要把形状向右移，就把采样点向左移；要把形状顺时针转，就把采样点逆时针转；要把形状放大 2 倍，就把采样点除以 2。这对应一个更一般的原理：**若希望在 "从 A 看到 B" 的视角下操作一个原本定义在 A 里的对象，只需把坐标系从 B 拉回 A**。这个模式在计算机图形里反复出现——纹理矩阵、相机矩阵、阴影矩阵全都是「逆变换施加在被采样点上」。

变换之间的顺序很重要：**先 translate 后 rotate** 让形状绕自身中心转；**先 rotate 后 translate** 让形状绕世界原点公转。和 [[mvp-transform|MVP 矩阵]] 里的 model matrix 一样，顺序决定了语义。

## 缩放会破坏 SDF 性质

有一个微妙的坑：把坐标除以 `s` 确实让形状看起来大了 `s` 倍，但是**返回的距离也被同样放大了 `s` 倍**。SDF 的定义是「返回真实的到表面距离」，被放大后 raymarching 会错误地迈出太大的步子，导致穿透。修复很简单——**在返回距离时再乘回 `s`**：

```hlsl
return rectangle(p / s, size) * s;
```

这个问题也解释了为什么 SDF 里**非均匀缩放**（x、y 不同比例）难以在保持距离正确的前提下实现：不同方向的 Lipschitz 常数不同，要求返回一个保守下界才能不破坏 raymarching。实践里常见的妥协是返回 `min(sx, sy) * ...`——最小比例意味着最保守的步长。

## 可视化：两种显示 SDF 的方式

把一张 SDF 直接喂 `fixed4(d, d, d, 1)` 只能看到灰度梯度，不能直接当形状。教程给了两种更有用的做法：

### 硬边 + 抗锯齿（text rendering 派系）

用 `fwidth(d)` 估计每像素下 `d` 的变化量——这就是「当前像素对应到屏幕上一个像素宽度的 SDF 变化」。然后：

```hlsl
float w = fwidth(d) * 0.5;
float alpha = smoothstep(w, -w, d);
```

在 `d == 0` 附近做一次宽度 = 1 个屏幕像素的 smoothstep——形状的边就有了天然抗锯齿。这就是 [TextMesh Pro / MSDF 字体渲染](https://github.com/Chlumsky/msdfgen) 的核心：低分辨率贴图（64×64 就够）加上这个 shader 就能清晰地渲染到任何字号。因为**距离场是连续的**，即使贴图被上采样成 1024×1024 也不会出马赛克。

### 等值线（height lines）

另一种用法是把 SDF 当作「地形高度」可视化：

```hlsl
float lineDist = abs(frac(d / spacing + 0.5) - 0.5) * spacing;
float line = smoothstep(thickness - w, thickness + w, lineDist);
```

- `frac(d / spacing + 0.5) - 0.5` 把 `d` 按 `spacing` 周期折叠到 `[-0.5, 0.5]`——每个 `spacing` 间隔处都有一条 0 穿越。
- `abs` 让折线上下对称，`* spacing` 恢复到和 `d` 相同的量纲（这样 `fwidth(d)` 估计的抗锯齿宽度仍然适用）。
- 第二个 `smoothstep(...)` 用 `thickness` 做厚度、用 `w` 做 AA，得到一条厚度固定、带抗锯齿的环线。

把主线、次线（`spacing / sublineCount`）、内外部不同颜色全叠起来就是一张漂亮的「地形图式」SDF 可视化——也是调试 SDF 非常有用的工具。

## 相关

- [[jump-flooding-algorithm]] —— 另一条路：从 alpha 贴图里在 GPU 上构造距离场
- [[sdf-ray-marched-shadows]] —— 用 SDF 在 2D 做 raymarch 软阴影
- [[planar-mapping]] —— 世界坐标喂 SDF 函数的常规做法
- [[fragment-shader]]
- [[sampling-theorem-sinc]]
- [[poisson-disk-sampling]]
- [[analytical-antialiasing]] —— 用 SDF 做完美的「一像素宽」边缘反走样
- [[sdf-operations-shader]] —— SDF 的布尔并差交、smooth min、空间镜像 / 平铺 / 扭曲 modification 清单

## Sources

- [[sources/ronja-2d-sdf-basics]]
