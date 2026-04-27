---
tags: [渲染, UI, IMGUI, 抗锯齿, alpha混合, 多边形]
date: 2026-04-27
sources: 1
---

# IMGUI 边缘羽化（Edge Feathering）

**边缘羽化（edge feathering）** 是一种在即时模式 GUI（IMGUI）渲染中实现**无 MSAA 平滑边缘**的轻量技巧，最早见于 Mikko Mononen 的 Recast 演示实现，后由 Rory Driscoll 整理发布。

## 原理

多边形边界处的锯齿来自光栅化对覆盖率的粗粒度采样。羽化技巧的思路是在顶点级别**模拟覆盖率的连续过渡**：

1. 取多边形的每条边，向外挤出一圈额外顶点。
2. 这圈顶点颜色与原多边形相同，但 **alpha 值强制置零**。
3. 渲染时，原多边形内部 alpha = 1，外侧羽化带的 alpha 从 1 线性插值到 0。
4. 配合普通 alpha blending，渲染结果在边缘处自然过渡，视觉上消除锯齿。

挤出宽度通常取 **1 像素**即可。更宽的羽化带会使边界看起来模糊而非锐利。

## 优缺点

**优点**：
- 纯 CPU 端几何生成，GPU 侧只是普通 alpha blending，无 MSAA 也无后处理
- 实现极简，适合工具 UI、调试 overlay、编辑器 IMGUI

**缺点**：
- 顶点数翻倍（每条边额外一圈顶点）
- 对非凸多边形需要额外处理法线方向，挤出方向可能出错
- 动态字体等曲线形状需要精细拆三角，否则羽化带可能穿插

## 与其他抗锯齿方法的对比

| 方法 | 原理 | 代价 |
|---|---|---|
| MSAA | 多采样点 | GPU 内存 × N |
| 后处理 AA（FXAA 等） | 图像空间模糊 | 一个全屏 pass |
| [[analytical-antialiasing]] | 解析覆盖率积分 | 着色器开销 |
| **边缘羽化** | 顶点 alpha 渐变 | 顶点数增加 |

对于 IMGUI 这类以凸多边形为主的场景，羽化是性价比最高的方案。

## 相关

- [[alpha-blending]] — 羽化依赖 alpha 混合管线
- [[analytical-antialiasing]] — 解析 AA 的通用框架
- [[fwidth-derivative-antialiasing]] — 着色器级别的 AA 替代思路

## Sources

- [[sources/rory-ui-antialiasing]]
