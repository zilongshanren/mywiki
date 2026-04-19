---
tags: [source, playcanvas, 开源, editor, 前端, 工具链]
date: 2026-04-19
sources: 1
---

# PlayCanvas Editor Frontend is now Open Source（Bamrah / PlayCanvas Blog）

Kris Bamrah 2025-07-30 发布于 blog.playcanvas.com 的公告：PlayCanvas Editor 的**前端部分**从商业闭源改为开源，补齐了 "Engine 开源 / Editor 闭源" 这个老结构的最后一块。

## 摘要

PlayCanvas Engine 多年来一直是 MIT 开源，但 Editor Frontend（Web 端的可视化编辑界面）此前是闭源的——这导致社区只能通过公开 API 观察编辑器行为，没法修 bug / 加定制。2025-07-30 起 Editor Frontend 以开源协议放到 `github.com/playcanvas/editor`，基于的开源组件栈也同步公开：Observer（数据层）、PCUI（UI 组件库）、PCUI-Graph（图形编辑控件）、Editor API。这让社区可以：fork 出定制版 Editor 接到官方后端做专有工作流；直接提 PR 修 bug 和加功能；在本地起调试环境看 Editor 真实行为。为降低贡献门槛，Editor 代码做了：结构重组、TypeScript 类型收紧、本地调试流程简化、新加一套测试套件防回归。

## 关键要点

- **开源的是 frontend**：后端仍是官方托管，fork 出来的 Editor 连接官方后端。
- **组件栈**：Observer / PCUI / PCUI-Graph / Editor API 同步开源或早已开源。
- **贡献体验优化**：重组 + 类型 + 调试 + 测试四件套，降低"从 0 到第一个 PR"的门槛。
- **生态意义**：和 [[supersplat-publish-platform|SuperSplat Viewer 开源]] 以及后续的 VSCode Extension 开源串成一条线——PlayCanvas 把全链路都开放。
- **定制化**：允许专有工作流搭在官方后端之上，这对 OEM、行业化 3D 工具的团队有吸引力。

## 链接到的概念

- [[supersplat-publish-platform]]
- [[playcanvas-webgpu-editor]]
- [[playcanvas-engine-2-breaking-changes]]

## 原文

- 链接：<https://blog.playcanvas.com/playcanvas-editor-frontend-is-now-open-source>
- 本地：`raw/articles/blog.playcanvas.com/2025-07-30_playcanvas-editor-frontend-is-now-open-source-playcanvas-blo.md`
