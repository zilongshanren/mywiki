---
tags: [source, 渲染, D3D11, 工具链, 模型加载]
date: 2026-04-14
sources: 1
---

# SharpDX and 3D Model Loading（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 3 月的实战笔记，记录把 XNA 原型迁移到 **SharpDX** 并用 **Assimp** 补齐模型加载能力的过程。

## 摘要

Anagnostou 长期用 XNA 做 D3D9 图形 demo，但 XNA 停更后必须寻找替代。他选了 **SharpDX**，一个跟随到 D3D11 的 C# 对 D3D 的轻封装；评价其「恰好把 D3D11 复杂度藏得刚好够用」——仍需走资源创建、pipeline 配置的流程，所以对学 D3D11 也有帮助，但不至于像裸 D3D11 C++ 项目那样被大量模板代码淹没。同类的 **SlimDX** 他认为不够活跃。SharpDX 唯一的大问题是**没有内容管线**——必须自己解决模型 / 贴图加载。他找到了 **Assimp**（C++ 开源库，覆盖大量 3D 模型格式）并用 `assimp-net`（通过 P/Invoke 调 Assimp dll）把它接进 C#。然后写了一个最小适配层：把 Assimp 的节点树 → `Model` / `ModelMesh`，每个 mesh 持有 SharpDX 的 vertex / index buffer、input layout 和单张漫反射 ShaderResourceView。Assimp 的材质系统更丰富，他没继续挖。结果：**成功加载 Sponza 3DS（带贴图）以及之前在 FX Composer 里加载失败的 Stanford Dragon OBJ**。提到 Assimp 当时不支持 FBX，需要 Autodesk FBX Converter 先转格式。评论区里 SharpDX 维护者出现：建议关注后续 SharpDX Toolkit 内建的 live shader 重编译以及通过 Build Action 自动编译 fx / font 的能力；**SharpDX Toolkit 后来内建 Assimp 支持**（`Content.Load<Model>(filename)`），Anagnostou 之后切换过去了。文章末尾链接了他的示例项目 zip 供读者复用。

## 关键要点

- XNA 停更 → SharpDX 作为 C# + D3D11 替代
- SharpDX 学习曲线介于「shader IDE」和「裸 D3D11 C++」之间
- 缺失内容管线 → Assimp + assimp-net 补足
- 自建最小适配器：Assimp 节点树 → `Model { ModelMesh }` → SharpDX buffer / input layout / SRV
- 验证案例：Sponza 3DS、Stanford Dragon OBJ（后者是 FX Composer 里无法加载的「反面教材」）
- FBX 当时 Assimp 不支持，要外部转换
- 后续 SharpDX Toolkit 内建 Assimp 支持，文中样例代码已不再维护

## 链接到的概念

- [[sharpdx-assimp-pipeline]]
- [[shader-prototyping-tools]]
- [[compact-vertex-format]]
- [[kostas-anagnostou]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2013/03/03/sharpdx-and-3d-model-loading/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-03-03_sharpdx-and-3d-model-loading.md`
