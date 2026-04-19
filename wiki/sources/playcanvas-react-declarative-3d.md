---
tags: [source, playcanvas, react, 声明式, 3d, ecs]
date: 2026-04-19
sources: 1
---

# Declarative 3D with React（Mark Lundin / PlayCanvas）

[[mark-lundin]] 在 2025 年 1 月发表的公告，宣布 PlayCanvas React（`@playcanvas/react`）开源发布——一个把 PlayCanvas 的实体-组件模型包成 JSX 的**声明式 3D** 绑定。

## 摘要

PlayCanvas React 是 PlayCanvas API 之上的**薄包装**：开发者不再用命令式的 `entity.addComponent('render', ...)` 去一步步搭场景，而是像写 HTML 一样用 `<Entity>` / `<Camera>` / `<Render>` / `<Script>` 这样的 JSX 组件声明整个场景树。引擎底层完全不变——物理、碰撞、音频、gaussian splat 这些 PlayCanvas 原生组件直接可用；React 负责的是**状态管理、组件复用、和生态集成**。作者把定位说得很清楚：相对于 Editor（浏览器内可视化编辑 + 资产管理）和 Engine（原生命令式 API），PlayCanvas React 是"第三条路"——面向那些已经站在 React 生态里、希望把 3D 内容直接嵌进更大 React 应用的开发者。文章展示了 Snap Inc 的 Snap AI 应用已在生产中使用 PlayCanvas React。该库以 MIT 协议开源。

## 关键要点

- **声明式 vs 命令式**：React 把 UI 的"描述 → diff → reconcile"范式套到 3D 场景，开发者只描述"应该是什么"而不关心"怎么改到那个样子"。
- **薄包装**策略的妙处：没有为 3D 重写 ECS，而是直接 mount 到 PlayCanvas 的 Entity-Component 模型，引擎升级后 React 层几乎无需改动。
- **生态对齐**：对一个已经用 React 构建产品的团队，这个选择意味着 state 管理、路由、devtool、SSR 都可以继承——这是对 Three.js + React Three Fiber 组合的直接对标。
- **定位分层**：Editor（可视化）、Engine（命令式）、React（声明式代码），三者并列，互为替代而非覆盖。
- 生产案例：Snap AI（文本生成 3D 资产）已落地。

## 链接到的概念

- [[playcanvas-react-declarative]]
- [[mark-lundin]]
- [[ecs]]

## 原文

- 链接：<https://blog.playcanvas.com/declarative-3d-with-playcanvas-react>
- 本地：`raw/articles/blog.playcanvas.com/2025-01-14_declarative-3d-with-react-playcanvas-blog.md`
