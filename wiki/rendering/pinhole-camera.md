---
tags: [渲染, 相机, 光学]
date: 2026-04-14
sources: 1
---

# 针孔相机模型（Pinhole Camera）

**针孔模型**是计算机图形学中虚拟相机的数学本体——所有的 [[mvp-transform|view/projection 矩阵]] 背后站着的就是它。理解它的局限性也就理解了为什么物理正确的渲染器需要 [[thin-lens-model|薄透镜模型]]。

## 为什么需要针孔

把一个光探测器（sensor）放在场景里会拍出一片糊——场景中每个点都能把光射到 sensor 的每个像素上。**限制每个像素能「看到」哪些方向**是成像的前提。

最简单的做法：把 sensor 放进一个小盒子，盒子上开一个小孔。每个像素现在只能通过那个孔看到场景的一小部分——图像形成。

## 三个基本性质

### 1. 图像倒置

光线穿过针孔后交叉，上下左右翻转——真实相机的 sensor 读到的就是倒像，显示前做 180° 旋转。

### 2. Field of View 由「针孔到 sensor 距离」决定

```
FoV = 2 · atan(sensor_size / (2 × distance))
```

- 距离大 → FoV 小（长焦效果）
- 距离小 → FoV 大（广角效果）

这就是 [[mvp-transform|投影矩阵]] 里 `fovY` 参数的物理意义。

### 3. Cosine-Fourth-Power 自然暗角

画面四角比中心暗，按 **cos⁴(α)** 比例，α 是像素到光轴的角度。原因是四重叠加：
- 两个 cosine 来自像素到针孔距离变大（inverse-square law）
- 一个 cosine 来自针孔从斜角看去变成椭圆（面积减小）
- 一个 cosine 来自 sensor 表面相对倾斜（Lambert cosine）

这就是 **natural vignetting**——物理相机和虚拟相机都绕不开。

## 局限性：为什么现代渲染要进一步

针孔是数学理想，实际有两个致命问题：

1. **效率极低**：场景里每个点向全半球发光，但针孔只截获极小一部分，几乎全部光能被浪费。
2. **无法控制景深**：针孔越小图像越锐利，但艺术上需要有选择地让某些东西模糊（bokeh、对焦）——针孔给不了这种控制。

这两个问题的答案都是同一个——用透镜替换针孔。参见 [[thin-lens-model]]。

## 在图形管线里

标准 [[mvp-transform|MVP 变换]] 下的虚拟相机本质上是针孔：

- 所有光线无限锐利（没有景深）
- 图像无暗角（工程上不模拟 cos⁴）
- 无限光能效率（不用考虑 f-number）

**光线追踪 / 物理渲染** 把这些假设还回去——从针孔变成薄透镜可以得到真实景深，从 Lambert 小块变成面光源可以得到软阴影。

## 相关

- [[mvp-transform]] — 虚拟相机的代数形式
- [[coordinate-spaces]]
- [[thin-lens-model]] — 进一步物理建模
- [[rasterization]]
- [[bartosz-ciechanowski]]
- [[emilio-lopez-ros]] — 曾在 Thailand 寺庙里遇见一个真实的 camera obscura

## Sources

- [[sources/ciechanow-cameras-and-lenses]]
