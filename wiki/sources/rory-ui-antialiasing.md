---
tags: [source, 渲染, IMGUI, 抗锯齿, UI, 多边形]
date: 2026-04-27
sources: 1
---

# UI Anti-Aliasing（Rory Driscoll / CodeItNow）

[[rory-driscoll]] 于 2012 年 1 月的博文，介绍一种为 IMGUI 渲染添加边缘抗锯齿的简单技巧，灵感来自 Mikko Mononen 在 Recast 中的实现。

## 摘要

技巧的核心是**多边形边缘羽化（edge feathering）**：在多边形每条边外侧挤出一圈额外顶点，这些顶点拥有与原顶点相同的颜色，但 alpha 设为零。在光栅化时，这条 alpha 从 1 到 0 的过渡带就实现了近似的子像素抗锯齿效果，而无需 MSAA 或任何后处理。Driscoll 发现只向外挤出 1 像素已经足够，效果在 800% 放大下仍然清晰可见。

## 关键要点

- 做法：在多边形边界外侧挤出一层顶点，alpha = 0
- 无需 MSAA 或后处理，顶点着色器即可完成
- 适合 IMGUI、2D 调试界面、工具 UI
- Mikko Mononen（Recast 作者）称之为"feathering"
- 挤出量 1px 实测已够用

## 链接到的概念

- [[imgui-edge-feathering]]
- [[alpha-blending]]
- [[analytical-antialiasing]]

## 原文

- 链接：https://www.rorydriscoll.com/2012/01/08/ui-anti-aliasing/
- 本地：`raw/articles/rorydriscoll.com/2012-01-08_ui-anti-aliasing.md`
