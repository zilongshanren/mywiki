---
tags: [game-engines, playcanvas, react, 声明式, jsx, ecs]
date: 2026-04-19
sources: 1
---

# PlayCanvas React：把 3D 场景声明式化

2025 年 1 月，[[mark-lundin|Mark Lundin]] 宣布开源 `@playcanvas/react`——一个 PlayCanvas API 之上的**声明式 React 绑定**。用 JSX 描述场景树，而不是写命令式的 `entity.addComponent('render', { type: 'box' })`。对比 Three.js 生态里的 React Three Fiber，PlayCanvas React 的定位是同一种解法、不同的底座。

## 声明式 vs 命令式：3D 场景的范式借用

React 当年对前端 UI 的革命核心在"声明式"：开发者只写"应该是什么"，React 运行时负责"diff → reconcile → patch"。这种心智模型天然适合**有层级结构、有状态、随 props 变化而更新**的系统——而 3D 场景图恰恰满足这三条：Entity 有父子层级、Transform/Visibility/Material 是状态、帧之间随游戏逻辑变化而更新。于是把 React 套到 3D 不需要发明新抽象，只需要把 JSX 节点映射成 Entity + Component：

```jsx
<Entity name='camera' position={[4, 3, 4]}>
  <Camera clearColor='#111111' fov={28} />
</Entity>

<Entity position={[0, 0.5, 0]}>
  <Render type='box' material={material} />
  <Script script={Spinner} speed={10}/>
</Entity>
```

`<Entity>` 对应 PlayCanvas 的 Entity，`<Camera>` / `<Render>` / `<Script>` 对应 [[ecs|Component]]。React 的 `useMaterial` hook 用来声明材质。这种写法的好处不是"代码更短"——同样的场景命令式也就多几行——而是**改动时的局部性**：props 变了 React 自动 reconcile 到对应组件，不用开发者记得去 `entity.findComponent('render').material = newMaterial`。

## 薄包装策略

Lundin 在文章里反复强调 PlayCanvas React 是"thin wrapper"——引擎层完全不动，所有原生 Component（rigid body、collision、physics、audio、gaussian splat）都直接可用。这个选择有两个战略含义：

- **引擎升级免疫**：PlayCanvas Engine 每个 minor 版升级，React 层几乎无需修改；维护成本比"重写一套并行 API"低得多。
- **语义零损失**：不是"React 能做的 3D 功能子集"，而是"任何 Engine 能做的事 React 也能做"。这避免了很多生态包装层常见的"80% 满足，20% 得绕开"困境。

## Editor / Engine / React：三条并行路径

PlayCanvas 现在有三种写 3D 内容的入口：

1. **Editor**（浏览器可视化编辑）——面向美术/设计师，负责资产管理、场景布局、快速迭代。
2. **Engine**（命令式 JavaScript API）——面向引擎开发者，直接和底层打交道。
3. **React**（声明式 JSX）——面向 React 生态里的应用开发者，把 3D 嵌进更大的 React app。

这三条路径**互为替代而非覆盖**：Snap Inc 的 Snap AI（文本生 3D 资产）选了 React 路径，因为整个应用本来就是 React 写的，3D 场景只是其中一个路由；一个传统游戏团队可能继续走 Editor 路径；一个做 WebGL 库的开发者会留在 Engine 层。

## 和 React Three Fiber 的对比

相似点都是"React + 3D = JSX 驱动声明式场景图"；区别在底座：R3F 绑的是 Three.js，PlayCanvas React 绑的是 PlayCanvas。对选型者来说值得看的维度：

- **引擎定位**：Three.js 是渲染库；PlayCanvas 是完整引擎（含 ECS、物理、音频、[[supersplat-pwa|3DGS]] 集成、[[playcanvas-webgpu-editor|WebGPU 支持]]、Editor）。
- **打包体积 vs 功能密度**：Three.js 更轻但要自己攒生态；PlayCanvas React 自带的 battery 多一点。
- **3DGS 一等公民**：PlayCanvas 对 gaussian splat 是引擎级内建，R3F 需要第三方库。

## 启示

声明式 3D 不是"更好的写法"，而是**对已经在用 React 构建产品的团队而言更低摩擦的接入方式**。引擎生态的长期趋势是**多种入口、共享内核**——Editor、命令式 API、声明式绑定、未来可能还有 low-code 工具——全部指向同一个 Engine 核心。PlayCanvas React 是这个趋势的一个具体实例。

## 相关

- [[ecs]]
- [[playcanvas-webgpu-editor]]
- [[gaussian-splatting-web]]
- [[mark-lundin]]
- [[will-eastcott]]
- [[reactive-ui-rust]]
- [[component-entity-data-binding]]
- [[playcanvas-esm-scripts]] —— 同期（2025-06）推出的 Editor 路径现代化：`.mjs` + class 继承 `Script` + `@attribute` 的属性声明；和 React 包装构成 PlayCanvas 的多入口矩阵（Editor / Engine / React）

## Sources

- [[sources/playcanvas-react-declarative-3d]]
