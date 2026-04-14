---
tags: [shader, 数学, 向量, 入门]
date: 2026-04-14
sources: 1
---

# 向量点乘（Dot Product）

**点乘**是 shader 里最高频、也最被低估的一个函数。它接受两个向量、吐出一个标量，本质是**把两个向量在同一方向上的"重合量"**一次算出来。一旦把它从"线性代数运算"的面具下解放出来，就会发现它其实是一把瑞士军刀——**颜色、距离、角度、光照、条纹**都能被它打包处理。

## 代数定义 vs 几何定义

代数上，`dot(a,b) = a.x*b.x + a.y*b.y + ...`——分量对乘求和。几何上，`dot(a,b) = |a| * |b| * cos(theta)`，其中 θ 是两向量夹角。shader 内部其实是走代数路线的，但几何解释对写代码更有用：

- 两向量**同向**时 cos=1，点乘 = 长度乘积；
- **垂直**时 cos=0，点乘 = 0；
- **反向**时 cos=-1。

如果两个向量都归一化了，点乘就是**纯角度信号**，落在 `[-1, 1]`——这就是 [[diffuse-lighting-lambertian|Lambert 漫反射]]的核心：`max(0, dot(N, L))` 直接给出"这块表面有多面向光源"。

## 用途 1：条纹图案

要在一个物体上做 x 方向的条纹：`mod(floor(position.x), 2.0)`。要沿**任意方向**的斜条纹？把 `position.x` 换成 `dot(position, direction)` 就行——点乘把位置向量投影到给定方向上，得到"在这个方向上走了多远"。而且 `direction` 的长度就是条纹频率：长度越大，条纹越密。这个技巧可以无痛推广到 3D 的**平面切片**。

## 用途 2：距离平方与衰减

物理光源的强度按**距离平方的倒数**衰减。朴素写法是 `1.0 / pow(length(d), 2.0)`，但 `length` 里藏着一个 `sqrt`，再 `pow` 平方又把它解开——完全是浪费。直接 `1.0 / dot(d, d)` 就好：`dot(d,d) = d.x² + d.y² + d.z²` 就是 Pythagoras 定理下的距离平方，不用开方也不用 `pow`。这也是 [[shader-code-golfing|code golf]] 里最经典的一条替换式。

## 用途 3：Lambert 光照

Lambert 漫反射的数学就是 `max(0, dot(N, L))`：表面法线 `N`、归一化光源方向 `L`，两者点乘即光照强度。负值意味着法线背光，截断到零即可。这是几乎所有[[rendering-pipeline|实时光照]]模型的地基——详见 [[diffuse-lighting-lambertian]]。

## 为什么值得反复重读

Xor 的话：点乘是进入**矩阵、旋转、投影**之前的最后一道入门门槛。矩阵乘法本质就是一堆点乘堆出来的，理解了点乘之后再看[[mvp-transform|MVP 变换]]就顺多了。

## 相关

- [[shader-vector-math-primer]]
- [[diffuse-lighting-lambertian]]
- [[mvp-transform]]
- [[shader-code-golfing]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-dot-product]]
