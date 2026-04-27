---
tags: [rendering, path-tracing, camera-model, measurement-equation]
date: 2026-04-27
sources: 1
---

# 主光线 PDF 的消去（Primary Ray PDF Cancellation）

路径追踪实现中，从相机出发的主光线（primary ray）采样有一个非平凡的概率密度函数（PDF），但几乎所有教程和代码都不显式使用它。这并非疏忽，而是主光线 PDF 与相机重要性函数（importance function / We）以及测量方程中的几何项精确对消的结果。

## 主光线 PDF 的形式

设虚拟像素平面距相机距离 `d = res_h / tan(fov_y)`（使每像素面积为 1），则从相机采样主光线方向的立体角 PDF 为：

```
pdf_w = (res_h / tan(fov_y))² × 1/cos³θ
```

其中 θ 是主光线与相机朝向的夹角。

## 测量方程与 We

像素亮度实际上是一个双重积分（测量方程）：

```
I = ∫∫ We(p0→p1) × L(p1→p0) × G(p0↔p1) dA(p0) dA(p1)
```

`We` 是相机重要性函数，编码了相机对不同方向光线的"敏感度"。若令：

```
We = res_h² / (tan²(fov_y) × area_aperture × cos⁴θ)
```

则 Monte Carlo 估计后，所有包含主光线 PDF 和 G 项的因子恰好约分，估计值直接等于辐亮度 L。

## Vignetting 与景深

- **Vignetting（暗角）**：cos⁴θ 因子是真实相机的物理效应，可通过修改 We 使其反比于 cos⁴θ 来消除
- **景深（DOF）**：光圈面积越大，We 越小，保持总通量守恒，与现实相机缩短曝光时间的效果等价

## 为什么理解这个重要

对于单向路径追踪，推导结果为"吞掉"主光线 PDF，直接存入 L。但对于**光线追踪（light tracing）**——从光源出发，不经过相机主光线——必须显式代入 We 进行正确的 Monte Carlo 估计，否则图像亮度和视角响应均错误。

## Sources

- [[sources/graphics-guy-primary-ray-pdf]]
