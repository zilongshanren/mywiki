---
tags: [渲染, 相机, 光学, 景深]
date: 2026-04-14
sources: 1
---

# 薄透镜模型（Thin Lens）

[[pinhole-camera|针孔相机]] 是理想几何模型，但无法表达真实相机的**景深、光圈、焦段**。薄透镜模型补上这些自由度——它是物理渲染和电影级摄影机虚拟化的基础。

## 从针孔到透镜

针孔只捕获通过一个点的光——效率低、无景深控制。薄透镜让**一个面**的入射光全部会聚到一个像点：

```
1/s_o + 1/s_i = 1/f
```

（thin lens equation，`s_o` 物距，`s_i` 像距，`f` 焦距）

## 核心参数

### 焦距 f

- 无限远的平行光会聚到焦点，焦距就是焦点到透镜的距离。
- **改变焦距需要移动成像面**才能保持对焦——导致 FoV 变化（focus breathing 现象的来源）。
- Prime lens = 固定焦距，zoom lens = 多个镜片组滑动。

### 光圈 Aperture 和 f-number

```
N = f / D     （f-number）
```

其中 `D` 是入瞳直径。f/2 意味着入瞳 = 焦距 / 2。

- 直径翻倍 → 面积 ×4 → 进光量 ×4
- 所以常见 f-stop 是 √2 ≈ 1.4 的倍数：f/1.4 → f/2 → f/2.8 → f/4...，每一档进光量减半
- **f-number 控制两件事**：进光量（曝光）和**景深**

### 景深（Depth of Field）

**景深 = 画面中「可接受锐利」的距离范围**。

- 对焦点的光会聚到一点，偏离对焦点的光会聚不到一点，在 sensor 上画出一个圆——**circle of confusion**
- 当 circle of confusion 小于一个像素时，人眼看不出模糊——这个范围就是景深
- **光圈越大 / 焦距越长 → 景深越浅**（circle of confusion 增长越快）

这是电影摄影最重要的艺术参数。游戏引擎的后处理 DoF 本质是在虚拟薄透镜模型下用 circle of confusion 大小模糊屏幕空间。

### Bokeh

散焦光斑的形状 = **光圈开口的形状**。多叶片光圈 → 多边形 bokeh，圆形光圈 → 圆形 bokeh。电影里故意选定光圈叶片数是美学决策。

## 像差：理想与现实的鸿沟

薄透镜假设用了 **paraxial approximation**（近轴近似），但真实球面透镜会引入误差。五大单色像差：

1. **Spherical aberration** — 边缘光线和近轴光线焦点不同
2. **Coma** — 斜入射点成彗尾状
3. **Astigmatism** — 切向/径向焦距不同
4. **Field curvature** — 焦面是曲面不是平面
5. **Distortion** — 桶形/枕形畸变

多色光还有 **chromatic aberration**（色散），因为折射率随波长变化——这是彩虹的同一个物理机制。

**解决方法**：非球面透镜、多组透镜组合、achromatic doublet。高端电影镜头内部是十几片镜片精心搭配的优化问题。

## 在图形管线里

- **游戏实时管线**：通常用 [[pinhole-camera|针孔模型]]，DoF 是后处理近似。
- **离线 / 光线追踪**：在相机发射光线时直接在光圈上采样，天然得到物理正确的景深、bokeh、cos⁴ 暗角。
- **电影 VFX**：经常模拟真实镜头的像差、色散、lens flare——为了和实拍镜头**匹配**。

## 关键教训

> 针孔模型给你透视，薄透镜模型给你**艺术控制**。景深不是 bug，是讲故事的工具。

## 相关

- [[pinhole-camera]] — 退化情形
- [[mvp-transform]] — 投影矩阵的几何基础
- [[rendering-pipeline]]
- [[bartosz-ciechanowski]]

## Sources

- [[sources/ciechanow-cameras-and-lenses]]
