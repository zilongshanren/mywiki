---
tags: [shader, godot, visualshader, shadergraph, 节点编辑器, 渲染]
date: 2026-04-14
sources: 1
---

# Godot VisualShader 与 Unity Shader Graph 的差异

[[daniel-ilett|Daniel Ilett]] 常年写 [[shaderlab-hlsl-basics|Unity shader]]，2024 年第一次尝试 Godot 4.2.1 的 **VisualShader**，把 Dissolve / Hologram / Hull Outline 三个他在 Unity 里做过的效果原样迁移了一遍。这次迁移的价值不在于三个效果本身（它们都属于入门级模板），而在于把两个可视化 shader 编辑器的**设计哲学差异**放在了显微镜下。

## 表面上的相似，内里的差距

从远处看，Godot VisualShader 和 [[shader-prototyping-tools|Unity Shader Graph]] 长得很像：节点拖线、Inspector 里暴露参数、节点库里找 Multiply / Step / Noise。但一旦动手，差距就露出来了：

- **没有"世界空间位置"节点**。Unity 里一个 `Position (World)` 就是三秒钟的事；Godot 里你得自己切到 **Vertex 阶段**、用 `Vertex` × `Model` 矩阵（`TransformVectorMult`）算出世界位置，再通过自定义 `Varying` 声明一个 `Vector3 WorldPos`，在 `VaryingSetter` 里写入，回 Fragment 阶段用 `VaryingGetter` 读出来。本质上 Godot 把"手写代码 shader 里你本来就要在 vertex shader 里做的事"一一暴露到了图上，没有替美术/程序员做抽象。
- **Multiply 要分七种**。Godot 对类型安全更严格：Float × Float、Vec × Vec、Matrix × Vec、Matrix × Matrix 都是不同节点（`TransformOp` / `TransformVectorMult` 等），搜索 "Multiply" 会弹出七个同名节点。Shader Graph 用一个 `Multiply` 节点靠类型推断自动匹配。
- **没有内建噪声节点**，但有远比 Unity 强的**自定义节点机制**。Unity 只能写 `Custom Function` 节点从文件注入 HLSL 片段；Godot 提供 `VisualShaderNodeCustom` 脚本类（配 `@tool` 属性），可以覆写 `_get_code()`（在节点插入处注入代码）、`_get_func_code()`（在 shader stage 开头注入）、`_get_global_code()`（在文件顶部注入 helper 函数和全局变量）。最后这一个特别关键——Unity Shader Graph 要做全局 helper 需要 include 文件 hack，Godot 直接内建。

文章里把官方 docs 的 Perlin Noise 3D 自定义节点拿来用——而且这个实现是**三维 Perlin**，Unity 内建的 [[classic-shader-noise|噪声节点]]只有 2D。

## 参数声明位置：图里还是图外

还有一个习惯差异：Unity Shader Graph 把 **Blackboard** 放在侧边栏，参数（Properties）是独立于图的。Godot 里参数节点（`ColorParameter` / `FloatParameter` / `Texture2DParameter`）直接放在图**中间**，参数名是节点上的文本框，默认值是一个 checkbox。这让图更自包含（每个参数看得到用在哪），但也让图更杂乱——没有"参数总览"这个视图。

## 三个案例映射出的具体摩擦

三个 shader 暴露的摩擦点可以列成一张表：

- **Dissolve**：需要世界空间 y 坐标 → 被迫用 Varying 机制；需要 3D 噪声 → 用自定义节点；Godot 缺 `Remap` 节点 → 用两个 `Multiply` + 一个 `Subtract` 手工展开；从 Vector3 拿 Y 分量走 `VectorDecompose` 而不是节点右侧的"展开箭头"（后者在当时版本有 bug）。
- **Hologram**：核心技术是 `Texture2D` × scroll 时间 UV；需要的 `Fresnel` 节点 Godot 有现成的，`Time` 节点也有，反而比 Dissolve 简单。
- **Hull Outline**：[[cel-shader-outline|反向外推轮廓]]在 Godot 里的实现几乎一模一样——`Normal × OutlineSize + Vertex → Vertex` 输出。唯一的细节是 Material 上要挂两份材质：第一份是 `StandardMaterial`（Godot 的等价 Lit），通过 **Next Pass** 槽位挂第二份 `ShaderMaterial` 跑 outline，并在 Mode / Cull 下拉里把 Cull 设为 `Front`。这比 Unity 多 pass 里写 Pass 块要直观，至少在多 pass 组合的 UI 上 Godot 反而更友好。

## HDR Emission 与 Glow

Godot 里要看到发光边缘（Dissolve 的发光边、Hologram 的 Fresnel），必须在 **Camera 的 Environment** 里开 Glow 选项；颜色参数的 RGB 值要超过 1（通过 Color Picker 的 RAW 标签可以解锁 >1 的滑条）。Unity 等价是 Bloom 后处理 + HDR Color Mode——两者的哲学一致，只是位置不同：Godot 把它挂在 Environment 上，Unity 挂在 Volume 上。

## 教学/工具链视角

把这次迁移当作两款工具的横评，**Godot 更接近"可视化的代码 shader"——你在图里的每一步几乎都能一一对应到一行 GLSL**；Unity Shader Graph 更接近"生成式编辑器"——它替你藏掉很多样板代码但也让你无法轻易 escape hatch。哪种更好取决于目标：工程化地积累 node 库时 Godot 的全局代码注入是巨大优势；快速原型时 Unity 的少量高级节点更省事。

## 相关

- [[daniel-ilett]]
- [[shader-prototyping-tools]]
- [[classic-shader-noise]] — Unity 内建噪声只 2D，Godot 自定义节点可以补 3D Perlin
- [[cel-shader-outline]] — 反向外推 hull outline 在 Godot 的 Next Pass + Cull Front 等价实现
- [[fragment-shader]]
- [[shaderlab-hlsl-basics]]

## Sources

- [[sources/danielilett-godot-visual-shaders]]
