---
tags: [渲染, 工具链, D3D11, 模型加载]
date: 2026-04-14
sources: 1
---

# SharpDX + Assimp 模型加载管线

**SharpDX** 是 C# 对 Direct3D 的一层轻封装，可以把它看作 XNA Game Studio 的精神继承者——提供同量级的抽象（`Device` / `DeviceContext` / `Buffer` / `ShaderResourceView` / `InputLayout`），但跟到 D3D11 并覆盖现代特性。[[kostas-anagnostou|Kostas Anagnostou]] 2013 年从 XNA 迁过来时指出：**SharpDX 刚好介于「完整 D3D11 C++ 引擎」和「shader IDE」之间**——程序员仍然要走 D3D11 的资源创建与 pipeline 配置流程，所以是个很好的学习工具，但又不至于像裸写 D3D11 那样被十几种 `DescriptorHeap` / `RasterizerState` / `SamplerState` 拖死。

相比 XNA，它的**主要短板是没有 content pipeline**——没有 `.xnb` 烘焙步骤，也不预置模型 / 贴图 / 音频加载器。

## 用 Assimp 补齐 content pipeline

**Assimp**（Open Asset Import Library）是 C++ 写的开源库，声称支持「几乎所有」常见 3D 模型格式（OBJ、3DS、FBX 部分支持、Collada、PLY……）。它把各种格式读进来后统一成一棵**节点树**：每个节点有 transform、子节点，以及若干 mesh 引用；每个 mesh 带顶点 / 索引 / 法线 / UV / 材质索引。

.NET 侧有若干 Assimp wrapper。Anagnostou 用的是 `assimp-net`，通过 **P/Invoke** 把 C++ dll 暴露给 C#：

```
raw C++ Assimp dll  ←P/Invoke←  assimp-net C# wrapper  →  SharpDX ModelMesh
```

## 转换层：Assimp 树 → SharpDX 资源

`assimp-net` 暴露的 model 不能直接送去渲染——需要一层**适配器**把它转成 SharpDX 的 `Buffer` + `InputLayout`。Anagnostou 的做法是最小化：

```
Model { List<ModelMesh> }
ModelMesh {
    VertexBuffer (位置 + 法线 + UV)
    IndexBuffer
    InputLayout  (vertex declaration)
    ShaderResourceView  (单张漫反射贴图)
}
```

这个结构足以加载并渲染 Sponza 3DS 文件（带贴图）以及 Stanford Dragon OBJ——后者是同时期 FX Composer 加载失败的那个模型，见 [[shader-prototyping-tools]]。材质系统只取了 diffuse；Assimp 暴露了更完整的材质定义（normal、specular、混合参数、shader 关键字），但 Anagnostou 没进一步实现。

## 格式覆盖与 FBX 坑

Assimp 不原生支持 FBX（当年的状况；后来有所改善）——AAA 常用的主力格式反而是最难的那个。当年的变通是先在 Autodesk FBX Converter 里转成 OBJ / Collada 再喂进去。

## 这条路线的演化后续

- **SharpDX Toolkit**（后来）直接把 Assimp 集成进去，`Content.Load<Model>(filename)` 一行加载。Anagnostou 本人之后就切过去了。
- **SharpDX 核心库本身**从 2015 年起也逐步停止维护，被 **Veldrid** / **Silk.NET** 等后续者接棒——但中间几年的 C# + D3D 原型体验主要靠它支撑。
- Assimp 本身继续活跃，至今仍是**跨引擎模型加载**的事实标准。

## 相关

- [[shader-prototyping-tools]]
- [[compact-vertex-format]]

## Sources

- [[sources/interplay-sharpdx-model-loading]]
