---
tags: [渲染, shader, sdf, 阴影, raymarching, 2d]
date: 2026-04-14
sources: 1
---

# 基于 SDF 的 Ray-marched 2D 软阴影

传统 [[shadow-mapping-basics|shadow mapping]] 依赖深度贴图 + 空间比较——这对 3D 栅格化管线天然适配，但在 **2D SDF 场景**里既没有 shadow map 的概念，也没有「从光源做一次 pass」的廉价方式。取而代之的常见做法是：**让每个像素自己从光源方向 raymarch**，而 SDF 提供了让这件事足够便宜的基础。这条路线得到的软阴影有一个很漂亮的副作用：**不需要滤波**——柔边是从距离场的几何结构里自动涌现出来的。

## 硬阴影：SDF raymarch 的基本结构

先从硬阴影开始。对每个待渲染像素 `p`，从它出发向光源 `L` 发射一条射线：

```hlsl
float2 dir = normalize(L - p);
float lightDist = length(L - p);
float t = 0;
for (int i = 0; i < SAMPLES; ++i) {
    float d = scene(p + dir * t);
    if (d <= 0) return 0;          // 击中遮挡 → 阴影
    if (t > lightDist) return 1;   // 越过光源 → 亮
    t += d;                        // 安全地前进
}
return 0;
```

三个关键点：

1. **`t += d`**：永远不能步长大于当前点到场景的最近距离，否则可能直接迈过一个小物体进入它后面的空白区——这是所有 [sphere tracing](https://en.wikipedia.org/wiki/Sphere_tracing) 方法的共同前提。和 3D raymarching 完全相同，只是降维到 2D。
2. **抽样数固定**：`#define SAMPLES 32` 这种写法方便编译器 unroll，也能让最坏开销可预测。教程用 32，实际工程里应结合射线长度做动态估计。
3. **两种退出情况**：命中 → 返回 0，达到光源 → 返回 1，耗尽样本 → 当作命中返回 0（安全兜底，视觉上几乎看不出）。

## 从硬阴影到软阴影：一行改动

Ronja 给的软阴影技巧（广为流传的 [Inigo Quilez soft shadow trick](https://iquilezles.org/articles/rmshadows/) 的 2D 版）非常精妙——只需要把 `return 1` 换成「沿途所见的最小 scene 距离」：

```hlsl
float shadow = 9999;
for (int i = 0; i < SAMPLES; ++i) {
    float d = scene(p + dir * t);
    if (d <= 0) return 0;
    if (t > lightDist) return saturate(shadow);
    shadow = min(shadow, d);
    t += d;
}
```

几何直觉：一条射线即使没击中遮挡，也可能**贴着物体边缘掠过**。贴得越近，阴影应当越暗。于是取整条射线上「最靠近场景的那一瞬间」作为阴影量——这恰恰是一个单次 raymarch 就能顺手算出的副产品，几乎没有额外成本。

## 三处微调让它真的好看

教程里按顺序演示了三次微调，每次都是一个 "aha" 时刻：

### 1. 硬度参数（hardness）

`shadow = min(shadow, hardness * d)` 把软边的宽度缩窄 `hardness` 倍。`hardness = 20` 意味着只有 `d < 0.05` 的像素才被认为「贴着遮挡」——既让软阴影更有张力，也减少「齿状 artefact」。这种 artefact 出现的原因是：当光源本身距离场景很近时，`d` 在光源位置仍然很小，算法误以为是遮挡在逼近。hardness 可以在 hack 掉问题的同时交给美术一个可调参数。

### 2. 除以 `t`（随距离软化）

`shadow = min(shadow, hardness * d / t)`——这行是整个效果的核心。不除 `t`：整条阴影的软度均匀。除 `t`：

- **射线起点附近**：`t ≈ 0`，`d / t` 很大 → `min` 不起作用 → 阴影在遮挡旁边**紧凑锐利**。
- **射线末端**：`t` 很大 → 同样的 `d` 被除下去 → 阴影随距离**越来越软**。

这恰好对应现实里**遮挡对光的角膜覆盖率**——遮挡越远（相对于像素和光源的连线）覆盖的光锥立体角越小，阴影越浅。用单变量 `d / t` 捕捉到了「Penumbra 随距离加宽」这件真实现象。必须从 `t = 0.0001` 起步——除 0 是永远的坑。

### 3. 最小步长（`max(sceneDist, 0.02)`）

如果光源恰好在一块几何体上方，`scene(lightPos)` 本身很小，raymarch 在末端会卡在微小步长里空转，用完 `SAMPLES` 仍然没到光源 → 返回 0 → 光源附近出现「虚假阴影圈」。**下限步长** `max(d, 0.02)` 让迭代保证前进，换取一点点潜在漏检，视觉上完全值得。

## 多光源：线性叠加

在这个全屏 fragment shader 的实现里多光源的做法最简单：对每盏灯独立 raymarch 一次，得到的 shadow mask 和光颜色相乘，然后把所有光源**相加**。

```hlsl
float3 col = geometry + s1 * col1 + s2 * col2;
```

每盏灯的 raymarching 成本是独立的 32 次 scene 采样——如果 scene 函数本身昂贵，每多一盏灯就线性加一份开销。这是一种典型的「为了简洁接受 O(lights) 成本」的权衡，适合灯数 <= 5 的 2D 游戏演出，不适合放一屏二十盏灯。

## 和 3D raymarching 的关系

这个算法几乎可以**原样升维到 3D SDF 场景**——把 `float2` 改成 `float3`，把 `scene` 换成 3D SDF，整套 raymarching 框架不变。iq 的经典 Shadertoy demo 里 3D 软阴影用的就是完全相同的 `min(shadow, k * d / t)` 一行。SDF 阴影因此是少数**同一份代码能从 2D 演示直接延伸到 3D 应用**的渲染技术之一。

## 和基于 SDF 纹理的阴影不同

要区分两条路线：

- **本页讲的**：场景由解析 SDF 函数定义（直接在 shader 里 hardcode 形状）。优点是精度任意、raymarch 一步到位；缺点是动态场景要把所有形状编进 shader 或走 uniform 数组。
- **纹理化 SDF**：先把场景烘到一张距离场纹理（例如用 [[jump-flooding-algorithm|JFA]] 从 alpha 贴图生成），然后 shader 采样纹理做同样的 raymarch。更灵活、支持动态内容，但有纹理分辨率和构造成本。

两条路线的 raymarching 数学完全一样，换掉的只是 `scene(p)` 的实现。

## 相关

- [[sdf-2d-primitives]] —— 提供 `scene(p)` 需要的 SDF 基元
- [[shadow-mapping-basics]] —— 3D 场景里的主流阴影算法
- [[jump-flooding-algorithm]] —— 从 alpha 贴图在 GPU 上构造距离场
- [[fragment-shader]]
- [[sampling-theorem-sinc]]
- [[volumetric-raymarching-intro]] —— raymarching 的入门与体积渲染动机

## Sources

- [[sources/ronja-2d-sdf-shadows]]
