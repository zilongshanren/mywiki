---
tags: [渲染, 反走样, sdf, shader]
date: 2026-04-14
sources: 1
---

# 解析抗锯齿（Analytical Anti-Aliasing, AAA）

**解析抗锯齿**把 [[aliasing|走样]] 问题反过来做：不是先光栅化再想办法补救，而是**因为我们已经知道形状的数学定义**，直接在片元着色器里按距离「淡出边缘恰好一个像素」。结果是形状边缘本身就自带完美的低通滤波——没有历史帧、没有多重采样 buffer、没有屏幕后处理、没有硬件依赖。前提是你得有目标形状的 [[sdf-2d-primitives|signed distance field]]。

Frost（[[frost-kiwi]]）在他的长文 _AAA - Analytical Anti-Aliasing_ 中把这个技术完整地展开了一遍，把它和 [[msaa-ssaa|SSAA/MSAA]]、[[temporal-antialiasing|TAA]]、FXAA 并列比较，并分享了几处他多年实现下来「从来没在别处读到过」的坑。

## 为什么「解析」

在图形学术语里，**analytical** 指的是一类效果：**事先知道被渲染对象的数学形状**，并**逐像素针对这个形状的方程式**做计算。它不是一个具体算法，而是一类思路。几个知名例子：

- **The Last of Us** 系列用若干拉长球体／胶囊拼成主角的形状，阴影和模糊反射都对胶囊的解析方程逐像素求值（Michał Iwanicki，Siggraph 2013）。这就是 Unreal 今天的 **capsule shadows**。
- **Inigo Quilez** 在 Shadertoy 上的 analytical ambient occlusion：地面对悬浮球的解析方程直接算出遮挡贡献，无噪声、不闪烁。
- **SDF 字体**（MSDF / TextMesh Pro）把字形编码成距离场贴图，逐像素对距离场做阈值 + 淡出——字号无限缩放都不出马赛克。

这些共同的底色是：**不依赖屏幕空间采样密度**，而是直接对形状的数学描述求解。AAA 只是把这个思路用在最基础的「反走样」这一件事上。

## 核心公式

给定一个带方向的距离 `dist`（到形状边缘，外部为正），以及像素的真实屏幕宽度 `pixelSize`，两行就够：

```glsl
float dist = length(uv);               // 圆的 SDF
float alpha = (1.0 - dist) / pixelSize; // 线性淡出一个像素
```

`alpha` 自然被 blending 单元截断到 `[0, 1]`，因此不需要 `clamp`。**不要用 `smoothstep`**——Frost 的一句暴论：`smoothstep` 做的是 Hermite 插值，但我们是在一个像素宽度内做过渡，这里根本没有任何曲线可言，只是在浪费几个 cycle 做 `t*t*(3-2t)`。在这里简单的线性插值在视觉上与 `smoothstep` 几乎不可区分，且更便宜。

## 像素尺寸怎么来

核心难点是「怎么知道一个像素在当前坐标系下有多大」。有三种做法：

1. **屏幕空间导数**：`fwidth(dist)` 或 `length(vec2(dFdx(dist), dFdy(dist)))`。需要 `GL_OES_standard_derivatives` 或 WebGL 2。自动尊重任意变换包括 3D 透视。**这是最通用的方式**，也是 Ronja 和 Freya Holmér 的 Shapes 插件使用的路线。
2. **`fwidth` 的快／慢之争**：`fwidth(x) = |dFdx(x)| + |dFdy(x)|` 是 `length` 的 L1 近似，比 `sqrt` 便宜，但对对角方向会**过估**——导致小圆在 45° 方向被「压扁」成菱形。Freya Holmér 的 Shapes 把这一模式命名为 **Fast Local AA**，并标注了这个已知偏差。选哪一个取决于你在意准确性还是性能。
3. **外部传入**：2D 场景下你显然**知道**画布分辨率和 quad 大小。把像素尺寸**每个 object 计算一次**当 uniform 传进来，避免 per-pixel 的 `length()`/`fwidth()`。没有扩展、没有 WebGL 2、连最古老的 GPU 都能跑，效果与 `dFdx + dFdy + length` 路线完全一致。这是 Frost 在文章里分享的「反直觉的干净做法」，也是他在文章里用的最终实现。

## 踩坑清单

- **quad 不能恰好等于形状大小**。如果在一个 1 单位的 quad 内画一个 1 单位的圆，边缘正好卡在 quad 边界上——光栅化会在某些屏幕分辨率下把最外一圈像素吃掉。必须**把 quad 扩大一个像素**，然后在 shader 里把 SDF 相应回收，才能让淡出过渡有「呼吸空间」。这点 AAA 与 MSAA + Alpha-to-Coverage 路径都需要。
- **Alpha-to-Coverage**：同一套 shader 如果想在 3D 场景里写深度并与前后物体正确混合，可以切到 `GL_SAMPLE_ALPHA_TO_COVERAGE` 路径——shader 代码**一行都不用改**，但必须依赖硬件 MSAA，带回了所有 MSAA 的烦恼（移动端强制 4x、iOS 2x 变伪 2x 等）。
- **透视** 会让「每像素计算一次 `length()`」反而比「per-object 计算」更划算，因为 per-object 路径要补上 perspective-correct 插值的复杂度。

## 和其他 AA 的比较

| 方法 | 源头 | 主要代价 |
|---|---|---|
| [[msaa-ssaa|SSAA]] | 渲染到更高分辨率再缩小 | VRAM × N、shader × N |
| [[msaa-ssaa|MSAA]] | 每像素多个 coverage 采样 | 硬件依赖、实现相关 artifacts |
| FXAA / SMAA | 后处理基于亮度边缘检测 | 亚像素丢失、糊、需要 post-process 链 |
| [[temporal-antialiasing|TAA]] | 多帧 jitter + reproject 累积 | ghosting、blurring、历史管理地狱 |
| **AAA** | 逐像素对已知 SDF 求值 + 淡出 1px | 只适用于「已知形状」——传统光栅化下无从下手 |

AAA 的局限非常明确：**它不解决通用场景的反走样**。它不能处理纹理内部高频、延迟渲染的屏幕空间走样、或没有 SDF 描述的几何边缘。它的价值是在**可以用 SDF 描述的形状**（2D UI、字体、程序化形状、基于距离场的 2D/3D primitive）上给出一个在工程上近乎完美的解：零额外 buffer、零帧间依赖、零硬件依赖、结果不随屏幕分辨率抖动。

## 相关

- [[aliasing]]
- [[msaa-ssaa]]
- [[temporal-antialiasing]]
- [[sdf-2d-primitives]]
- [[sdf-ray-marched-shadows]]
- [[fragment-shader]]
- [[frost-kiwi]]

## Sources

- [[sources/frost-kiwi-analytical-anti-aliasing]]
