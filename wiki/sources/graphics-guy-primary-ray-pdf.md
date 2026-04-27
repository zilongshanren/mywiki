---
tags: [source, rendering, path-tracing, camera-model, measurement-equation]
date: 2026-04-27
sources: 1
---

# The Missing Primary Ray PDF in Path Tracing（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2016 年 2 月的文章，解释了为什么路径追踪实现中不需要显式处理主光线（primary ray）的 PDF，其背后是相机重要性函数与测量方程中各项的完美对消。

## 摘要

路径追踪新手常有疑问：从相机发出的主光线采样有一个非平凡的 PDF（与 `cos^3(θ)` 相关），为何实现中从未见到它被使用？文章从测量方程出发，推导出像素亮度实际上是一个包含相机重要性函数 `We` 的双重积分。主光线 PDF 恰好与 `We` 中的 cos 项以及面积-立体角转换项完全对消，使得 Monte Carlo 估计的结果直接等于辐亮度 `L`。文章还解释了 Vignetting 效应（cos⁴θ 暗角）的成因，以及在景深（DOF）渲染中光圈大小如何通过重要性函数隐式归一化。理解此推导对于正确实现光线追踪（light tracing）至关重要——光线追踪从光源出发，无法发射主光线，必须显式处理测量方程。

## 关键要点

- 主光线 PDF（solid angle）= `(res_h/tan(fov_y))² × 1/cos³θ`
- 相机重要性函数 `We = res_h²/(tan²(fov_y) × area_aperture × cos⁴θ)`
- 两者与 G 项（`cosθ/r²`）相乘后恰好约分，Monte Carlo 估计值 = L（辐亮度）
- Vignetting 是 cos⁴θ 的直觉解释：可通过修改 `We` 使其与 `cos⁴θ` 成反比来消除
- 景深时光圈面积越大，We 越小，保持总通量不变
- 光线追踪（light tracing）必须显式代入 `We`，因为它从光源出发，不经过相机主光线

## 链接到的概念

- [[rendering/path-tracing-basics]]
- [[rendering/monte-carlo-integration]]
- [[rendering/physical-camera-model]]
- [[rendering/pinhole-camera]]
- [[rendering/thin-lens-model]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/the_missing_primary_ray_pdf_in_path_tracing/
- 本地：`raw/articles/agraphicsguynotes.com/2016-02-04_the-missing-primary-ray-pdf-in-path-tracing.md`
