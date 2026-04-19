---
tags: [shader, shadergraph, hlsl, unity, custom-function, 光照]
date: 2026-04-19
sources: 1
---

# Shader Graph Custom Function 与 HLSL 桥梁

Shader Graph 是个节点图，覆盖不了所有 shader 场景——最典型的两个盲区是 **访问 URP/HDRP 的内部 API**（光照、阴影、camera data）和 **运行时循环**。[[daniel-ilett|Daniel Ilett]] 的 Shader Graph Basics Part 10 围绕 URP 的 **Additional Lights** 把这两个问题都讲完了：怎么写一个 `.hlsl` 文件、怎么通过 `Custom Function` 节点把它挂进图里、以及为什么 "把循环塞进 HLSL" 比 "把 HLSL 拆成多个节点展开" 快得多。

## `.hlsl` 文件的函数约定

Custom Function 节点可以选 "String" 模式（直接内嵌一小段代码）或 "File" 模式（指向一个 `.hlsl` 文件）。后者是正经做法。文件结构是普通的 HLSL header + `#ifndef` 头卫，函数要遵循两个硬规则：

- **函数名后缀 `_float` 或 `_half`**：对应 Shader Graph 节点层的单/半精度选项。绝大多数场合两个都写，函数体一样，节省后期被用户踩坑。
- **返回 `void`，所有输入输出在参数表里，输出标 `out`**：这和 HLSL 其它编程习惯不太一样，但是 Shader Graph 的 Custom Function 节点要求——它用这个约定解析输入输出的形状。

```hlsl
#ifndef CUSTOM_LIGHTING_INCLUDED
#define CUSTOM_LIGHTING_INCLUDED
void MainLight_float(float3 WorldPos,
                     out float3 Direction, out float3 Color, out float Attenuation) {
#ifdef SHADERGRAPH_PREVIEW
    Direction = normalize(float3(1, 1, 0));
    Color = 1;  Attenuation = 1;
#else
    Light mainLight = GetMainLight();
    Direction   = mainLight.direction;
    Color       = mainLight.color;
    Attenuation = mainLight.distanceAttenuation;
#endif
}
#endif
```

`SHADERGRAPH_PREVIEW` 宏是关键——Shader Graph 编辑器里的预览图里并没有真实光源，调 `GetMainLight()` 会拿到垃圾数据，所以要 `#ifdef` 分叉，编辑器走假数据、运行时走真 API。这条 guard 是所有涉及 URP/HDRP 内建 API 的 Custom Function 的必备样板。

## 节点侧的接线

Custom Function 节点的 inspector 里手动列出 inputs / outputs 和类型——参数名**必须**和 HLSL 里一致，类型用 `Vector3 / Float / Vector2` 等 Shader Graph 的名字（不是 HLSL 的 `float3`）。一个坑：Shader Graph 没有 `int` 类型，HLSL 侧的 `int` 参数在节点侧用 `Float` 声明即可，Unity 会隐式转换。

## URP 光照 API 入口

把 Custom Function 节点当作"把 URP 的 HLSL 函数拉回 Shader Graph"的端口：

- `GetMainLight()` → 主方向光，返回 `Light` 结构，包含 `direction / color / distanceAttenuation`。
- `GetAdditionalLight(int id, float3 worldPos)` → 第 `id` 盏附加光（point / spot / 额外 directional），`distanceAttenuation` 对 point 光包含基于距离的衰减，对方向光为 1。
- `GetAdditionalLightsCount()` → 当前帧这个物体接收的附加光数量。

这些函数都在 `Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl` 里；Shader Graph 已经通过模板自动 include 了这个文件，所以 Custom Function 里不用额外 `#include`。这个路径还有它的价值——读这个目录下的源码几乎是了解 URP 实际光照计算的唯一途径。

## Shader Graph 最大的短板：**没有循环**

写"处理所有附加光"最自然的写法是 `for(int i = 0; i < lightCount; ++i)`。Shader Graph 做不到——它是**静态图**，每个节点都是编译期确定的。Ilett 给了两种妥协：

1. **展开成固定数量的节点**：假设最多 4 盏附加光，把 `AdditionalLight_float` 调用 4 次，4 个 `LightID = 0..3` 写死在图上。即便场景只有 1 盏附加光，剩下 3 次调用也会执行——返回 `color = 0` 但仍消耗算力。而且固定为 4 就封顶了，超过就被截断。
2. **把循环塞进 HLSL**：写一个 `AllAdditionalLights_float` 函数，入参是 `(worldPos, worldNormal, thresholds)`，出参是 `LightColor`，HLSL 体内自己 `for` 循环 `GetAdditionalLightsCount()` 次，累加所有光的贡献。节点侧只放一个 Custom Function 节点，图一下子干净了、性能也只为实际存在的光付费。

第二条路其实是在说：**"Shader Graph 的 Custom Function 越用越接近写普通 HLSL shader"**。Ilett 的结论是坦诚的——如果你在做复杂 shader，纯图限制大，学一点 HLSL 总是值得的。

## 和 [[shader-graph-lighting-primer|Lit 图的黑盒]] 对比

Lit Shader Graph 完全封装了光照——你给 Unity albedo/metallic/smoothness，Unity 自己跑完 PBR。Custom Function + Unlit Graph 则是反过来："我全部自己算，Unity 只负责绘制像素"。这是做 [[cel-shading-pipeline|NPR cel shading]]、rim light、toon water 这类需要精确控制光照公式的效果的唯一路径（在 Shader Graph 里）。代价是你自己要写 HLSL，而且图里会多出十几个节点做 `dot` / `smoothstep` / `saturate` 这些 HLSL 里一行就够的操作——又一次印证"超过某个复杂度阈值直接写 HLSL 更好"。

## 相关
- [[daniel-ilett]]
- [[shader-graph-lighting-primer]] — Lit 图的黑盒对立面
- [[cel-shading-pipeline]] — 自定义光照的代表性用例
- [[shaderlab-hlsl-basics]]
- [[diffuse-lighting-lambertian]]
- [[scriptable-render-pipeline]]
- [[gpu-instanced-grass-urp]] — Custom Function 接入 `StructuredBuffer` 做 GPU instancing 的代表性用例

## Sources

- [[sources/danielilett-shader-graph-custom-functions]]
