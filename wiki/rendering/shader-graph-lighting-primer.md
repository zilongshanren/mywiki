---
tags: [shader, shadergraph, 光照, pbr, unity, 教学]
date: 2026-04-14
sources: 1
---

# Shader Graph Lit 输出栈速览

[[daniel-ilett|Daniel Ilett]] 在 2024 年 **Unity Shader Graph Basics Part 6** 里做了件很实用的事：把 URP Lit Shader Graph 的 **完整输出栈**从头到尾逐项讲了一遍。这页不是要重复 [[physically-based-shading|PBR]] 的理论——理论另有[[normalised-blinn-phong-shader|归一化 Blinn-Phong]]和[[microfacet-brdf|微表面 BRDF]]——而是把 Shader Graph 这个**黑盒**的每个 output 槽位对应的物理意义、工作流选择、贴图转换踩坑集中在一张图上说清楚。

## 为什么 Lit 输出栈这么长

Unlit 图基本上只输出 `Base Color + Alpha`；Lit 图一下子多出来 `Normal / Metallic (or Specular) / Smoothness / Emission / Ambient Occlusion`，因为 Unity 的 Lit shader 用 **Physically Based Rendering**：你告诉 Unity **物体的物理属性**（albedo、粗糙度、金属性、法线变形、被遮蔽程度），Unity **自己决定** diffuse 和 specular 的贡献量，shader 作者根本不接触光照公式。这是 [[diffuse-lighting-lambertian|手写 Lambert]] 或者 Surface Shader 自定义 Lighting 函数的对立面。

## 按槽位拆解

- **Base Color**：albedo，和 Unlit 一致。Ilett 把它和 **Displacement 高度图**配合：用一个 `Parallax Mapping` 节点吃高度图生成偏移 UV，把这组 UV 作为 `Sample Texture 2D` 的 UV 输入——不真的改 geometry，而是通过 UV 位移把高频细节"假装"凸出。这套技巧在 brick 贴图上肉眼可辨，在 grass 贴图上几乎看不出来。
- **Normal**：法线贴图。和 displacement 不同——**它不假装像素从表面移开，只改像素法线的朝向**。采样法线纹理时必须把 `Sample Texture 2D` 的 **Type** 改成 **Normal**，因为 Unity 对普通纹理和法线纹理的解码方式不同（切线空间解压缩 + 可能的 DXT5nm 重构）。要和 parallax UV 一起用——法线和 albedo 都走位移后的 UV，否则表面细节会解耦。见 [[tangent-space-normal-mapping]]。
- **Metallic / Specular**：图有两种 **Workflow**（在 Graph Settings 里切换）。Metallic 工作流用一个 [0, 1] 的 slider 说"这是金属还是不是"；Specular 工作流直接暴露高光颜色。两者都能表达 PBR 的同一套物理，选择是主观的——Ilett 推荐 Metallic 因为它参数更少。
- **Smoothness**：踩坑重灾区。[ambientCG](https://ambientcg.com/) 之类的库给的是 **Roughness** 贴图（黑 = 光滑、白 = 粗糙），Unity Shader Graph 要的是 **Smoothness**（反过来）。Ilett 的修法是采样后取 Red 通道（灰度图哪个通道都一样），过一个 `One Minus` 节点把值取反，再喂给 Smoothness 输出。**贴图语义翻转**是"懂一点 PBR 的新手第一坑"。
- **Emission**：发光颜色，不受场景光衰减。要做发光**必须**把 Color 属性的 Mode 设成 **HDR**，才能给出超过 1.0 的颜色分量，并且要在场景里有 **Bloom 后处理**（URP Default 工程自带 Volume Profile；否则要自己 `GameObject → Volume → Global Volume`，加 Override → Post-processing → Bloom，设 Intensity = 1）。"HDR 颜色 + Bloom"是 Unity 里所有"发光"的公式，不管是[[bloom-threshold-blur-composite|bloom 后处理]]、Hologram shader 还是 Terastallize 效果都是同一套。
- **Ambient Occlusion**：描述表面被遮蔽的程度，0 = 完全遮蔽、1 = 完全可见。和 [[diffuse-lighting-lambertian|Lambert diffuse]] 不同——它**不是**光照计算的输入，而是一个**乘在环境光上的调制因子**，用来把真实感加强：深沟缝里接不到环境光，应该暗下去。对 [[painted-foliage-bent-planes|草 / 布料 / 复杂表面]]特别有用。

## 为什么这页单独开，而不是塞进 diffuse-lighting-lambertian

因为关注点完全不同：[[diffuse-lighting-lambertian]] 讲的是"光照方程本身是什么"，面向写自定义 Lighting 函数的人；这页讲的是"把 PBR 当黑盒用时，每个输入槽位的**贴图准备**和**语义陷阱**是什么"，面向用 Shader Graph 的 TA。前者关心 `L·N`，后者关心"为什么我下载的 roughness 贴图接错了槽位"。

## 相关

- [[daniel-ilett]]
- [[physically-based-shading]] — 这页讲的是它在 Shader Graph 里的接线
- [[diffuse-lighting-lambertian]] — 手写光照的对立面
- [[tangent-space-normal-mapping]] — Normal 槽位的底层
- [[bloom-threshold-blur-composite]] — Emission 生效的必要条件
- [[scene-color-depth-nodes]]
- [[shaderlab-hlsl-basics]]

## Sources

- [[sources/danielilett-shader-graph-lighting-basics]]
