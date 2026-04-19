---
tags: [人物, 作者, playcanvas, react, 3d]
date: 2026-04-19
sources: 1
---

# Mark Lundin

**Mark Lundin** 是 PlayCanvas 团队成员，主导了 [[playcanvas-react-declarative|@playcanvas/react]] 的设计与开源发布——一个把 PlayCanvas ECS 模型包装成 JSX 的**声明式 3D 绑定库**。在 2025 年 1 月的公告里他把 PlayCanvas React 定位为对 React 开发者的邀请：把 React 声明式的状态/组件/reconcile 心智直接套到 3D 场景。

## 主要贡献

- 设计并开源 `@playcanvas/react`（MIT 协议），对标 Three.js 生态里的 React Three Fiber。
- 采取"薄包装"策略：不重写 ECS，直接映射 JSX 节点到 PlayCanvas 的 Entity + Component；引擎升级几乎对 React 层透明。
- 推动 PlayCanvas 的**多入口生态**：Editor（可视化）、Engine（命令式）、React（声明式）三条并行路径共享同一内核。

## 相关

- [[playcanvas-react-declarative]]
- [[ecs]]
- [[will-eastcott]]

## Sources

- [[sources/playcanvas-react-declarative-3d]]
