---
tags: [shader-graph, rendering-architecture, gbuffer, deferred-rendering]
date: 2026-04-19
sources: 1
---

# Shader Graph Contract

Shader graph 不是一种随便的「可视化编程」UI，而是一种**契约**——它规定了艺术家能改到哪一层、哪些东西必须按引擎预设的格式写出。理解这份契约，才能理解为什么 Unity/Unreal 的 Lit master node 无法支持自定义 toon lighting、为什么 Substrate 要发明 slab + tree flattening 这套工程。[[apoorva-joshi]] 的 *The Shader Graph Contract* 是这一主题的入门范本。

## Sink 节点决定契约

shader graph 是 DAG，source 节点（normal/position/UV）自动出现，**sink / master 节点**决定输出形式：

| sink 类型 | 艺术家能写什么 | 能做什么 | 代价 |
|---|---|---|---|
| **Unlit** | color 一路到屏幕 | 完全自由 toon / stylized | 放弃延迟、PBR、IBL |
| **Lit** | metallic / smoothness / emission → GBuffer | PBR，兼容 deferred、visibility buffer | 不能改 lighting loop |
| **Layered mixed**（Substrate/MaterialX） | 多层 BSDF 组合 | 接近离线渲染表达力 | 需要 slab + flattening 等工程 |

关键洞察：**艺术家能编程的是「在 GBuffer 写入之前」那部分**。Lit master node 接受的是一组预定义 surface 描述，shader graph 负责把 UV 采样、纹理混合、noise 组合等步骤填进去；最终 GBuffer 写入与 deferred lighting 对艺术家是黑盒，这正是引擎能跨平台 scale、能优化 VGPR、能上 Visibility Buffer 的保证。

## Substrate 的工程：slab + tree flattening

MaterialX 允许任意层叠：`mix(layer(bsdf_0, bsdf_1), bsdf_2, 0.5)` 是一棵树，deferred lighting 要还原这棵树就得把**整棵 BSDF 树编码到 GBuffer**——带宽、存储都爆炸。

Unreal **Substrate** 的解法：

1. **Slab**——预定义的 BSDF 组合块（diffuse + specular + fuzz + subsurface，顺序固定）；艺术家只能选 slab、不能重排 slab 内层；
2. **Tree flattening**——GBuffer laydown 阶段遍历 BSDF 树，算好每层的 coverage 与 transmittance，把树**压平成扁平的 slab 参数**写进 GBuffer；
3. **延迟阶段不再见树**——只是按预设 slab 结构计算光照。

结果：艺术家获得层叠自由度，引擎保住延迟渲染的批处理效率。这是 shader graph contract 的**最强变体**。

## 设计 shader graph 时的建议

- **先定契约、再定节点库**——上来就扩展节点而没想好输出契约，最后很难删；
- **让 forward / deferred / visibility buffer 路径都成立**——有些节点在 forward 可用、deferred 下因为 derivative 不可用；
- **显式拒绝「无 contract 的全自由」**——把 Unlit 作为唯一完全自由的 sink，其它 sink 都强绑定特定 lighting 模型；
- **用户教育**——多数艺术家直觉上想「一个 graph 搞定 toon + PBR」，但这是 contract 冲突。

## 相关

- [[deferred-rendering]]
- [[visibility-buffer]]
- [[shader-graph-custom-function-hlsl]]
- [[physically-based-shading]]

## Sources

- [[sources/apoorvaj-shader-graph-contract]]
