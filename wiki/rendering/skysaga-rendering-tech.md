---
tags: [渲染, 引擎, deferred, voxel, skysaga, pipeline, pbr, weather, color-grading]
date: 2026-04-14
sources: 1
---

# SkySaga 的 Meandros 引擎渲染管线

*SkySaga: Infinite Isles* 是 Radiant Worlds 2015 年的一款 voxel 沙盒，使用自研引擎 **Meandros**。[[kostas-anagnostou|Kostas Anagnostou]] 那篇 2015 年的博客是一份罕见的**整套管线总览**——大多数 interplayoflight 的文章都是单点深挖，这一篇把 token command 系统、deferred + PBR、voxel-specific ambient occlusion、G-Buffer modification 天气系统、volumetric fog、3D LUT color grading 全部串起来讲了一遍。对了解 2015 前后中型工作室自研引擎是什么样子，这是个样本。

## Token + Pipeline Stage：命令流式架构

Meandros 不是"每个可渲染物体一个 virtual draw 函数"的 C++ 架构。它的核心是一个 **token submission / processing 系统**——每个可渲染实体生成一串紧凑的 token，每个 token 是一条最小操作：设一条 D3D 状态、绑一张纹理、切一个 pixel shader、发一个 drawcall 等等。token 流收集在 buffer 里，渲染时按顺序 sort + 去除冗余 state setting + 提交到 D3D API。

这种设计的优点是**缓存友好**——token 是 POD 小结构，连续排布，依赖数据局部可达。它也和渲染架构解耦：同一个 token + stage 体系既可以驱动 forward 也可以驱动 deferred，SkySaga 只是把它配成了 deferred。更上层的**Pipeline Stage**（shadow pass、lighting pass、post-processing pass 等）把 token 流分组、前一 stage 的输出可以作为后一 stage 的输入，让整个帧结构显式化——现代引擎里类似的东西是 [[render-graph|render graph]]，概念上同源。

## Deferred + PBR + Albedo-Metalness-Glossiness

为什么 deferred？两个硬约束：**大量动态光源**（一个昼夜循环 + 多种 biome + 大量点光）和**巨大的几何量**（voxel 世界，forward 的"几何 pass 乘以光源数"会炸）。选了 deferred shading 就接受 G-Buffer 带宽代价。

G-Buffer 有 4 张 RT，channel 被挤得很紧：

- **RT0**：Normal XYZ + Geometric Normal XY（view space，法线压到两张用 octahedral 或类似编码的可能很大）
- **RT1**：Depth（3 channel 编码）+ Ambient Occlusion（剩下 1 channel）
- **RT2**：Compressed Albedo XY + Emissive + Lit Alpha Flag
- **RT3**：Metalness + Midscale AO + Glossiness + 余量

Albedo 用 [jcgt.org](http://jcgt.org/published/0001/01/02/) 的压缩方法塞进 2 channel，换出一个 channel 给 **Lit Alpha Flag**——标记一个像素是不是来自光照透明层（后述）。Depth 编到 3 个 channel 是为了同样的理由：腾出一个 channel 给 AO。这种"把 channel 榨到底"的状态在 4-RT 限制下很常见。

材质模型是 **Albedo-Metalness-Glossiness**——metal 的 albedo 当 specular color 用，非金属 $F_0$ 固定 0.04。BRDF 从 Blinn-Phong → normalized Blinn-Phong → 最后 **GGX**，因为美术偏好 GGX 的软衰减高光边。HDR 管线全程 64-bit（G-Buffer 除外——它必须 8-bit 才能塞进带宽预算）。

## 两尺度 AO：per-corner 烘焙 + voxel 光传播

SkySaga 的 AO 有两层：

1. **Small-scale AO**：voxel corner / edge 交接处的小暗角，烘焙到一张纹理，由 lighting pass 直接采样。
2. **Midscale AO**：CPU 侧建一个 **voxel occupancy 3D array**，用**若干步光传播**算每个 voxel 能收到多少环境光。洞穴、门道里光会衰减得快，开放空间衰减慢。这一步同时做两件事——给 lighting pass 提供一个 GI-like 近似的 occlusion 项，以及给**其它系统当 enclosure mask**：雪 / 雾 / decal 不飘进洞穴，因为这些效果都用 midscale AO 作为衰减权重。对动态物体不能烘到顶点上，所以 shader 用物体世界位置采一次 midscale AO 填 constant 下传。

这是一个典型的**"用 voxel 数据结构的副产品做额外信号通道"**——voxel 游戏天然知道空间占用，一次光传播同时服务于 GI、AO、weather mask 三个子系统。非 voxel 引擎要做同样的事成本高得多。

## Six-axis Ambient：Valve 的老招数

[Valve 在 Half-Life 2 / Source 引擎](http://www.valvesoftware.com/publications/2006/SIGGRAPH06_Course_ShadingInValvesSourceEngine.pdf) 里用过的 six-axis ambient 在这里被重新捡起：沿 ±x/±y/±z 方向分别存 6 个环境光颜色，shader 里根据表面法线做 6 个方向的加权和。结果是**即使在阴影里，法线贴图也能产生色彩变化**，不是死平的暗色块。biome 间的氛围切换只需要换这 6 个颜色——甜点足够、比完整 [[spherical-harmonics|球谐]] 便宜得多、美术控制直观。

## G-Buffer Modification Pass：天气与装饰

这是 Meandros 最有趣的架构决策之一。SkySaga 需要**动态天气**——雪积累、泥水、装饰 decal——而这些效果的难点不是 rendering 本身，是"**哪些像素应该受影响**"。不能给 emissive 表面加雪、不能把金属 albedo 变暗（它同时是 spec color，变暗会让金属整个变色而不是只变湿）、洞穴内部不应积雪等等。

Meandros 的办法：在 lighting 之前先 **copy G-Buffer**，然后用一个 2D 屏幕空间 pass 做 **conditional blend**——根据 copy 版本的原始属性决定新值。能被改的字段几乎全部（normal、albedo、glossiness、metalness），**除了 AO**（因为 AO 是空间数据，屏幕空间改它没意义）。每种效果的 blending 规则独立：雪看法线朝上、湿只改 glossiness 和轻微 albedo darken 但不动 metal 的 albedo、decal 是直接正常 alpha blend。**用 midscale AO 做 indoor mask**让这些效果在门口自然淡出。

同一套 pipeline 既做全局天气又做局部 decal——没有单独的 decal 渲染路径，decal 是"局部有界的 G-Buffer modification pass"。这和近年 Remedy / DICE 在 Control / Frostbite 里演示的 "decal as G-Buffer edit" 思路同源，只是早了几年。

## Shadows：双层 shadow map for clouds

directional light 用标准 4-cascade shadow map + PCF。特殊处理在于 **SkySaga 有云投影**——云在 biome 里覆盖率不低，如果用纯 solid shadow map，世界会被压成漆黑。解法：shadow map **拆成两个 16-bit channel**，一层存 solid geometry 深度、一层存 translucent（云）深度。lighting pass 分别做两次深度比较，产生"solid shadowed"和"translucent shadowed"两个结果，translucent 阴影的强度由云的 alpha 决定。

代价是 per-channel 16-bit 的深度精度让 shadow acne 更严重——用 **Normal Offset Mapping** 补偿（沿法线偏移 sample 点避免自阴影）。可选有**彩色阴影 RT**——写 RGB 深度到另一张 RT，支持彩色玻璃、有色云影、彩色 volumetric light shaft。

## Transparency：一层进 G-Buffer

deferred 渲染下的透明一直是老问题：G-Buffer 里没有 per-pixel 透明层，lighting pass 只看到 solid 材质，透明物体只能走 forward 重新计算光照——和 solid 不一致。Meandros 的折中是**第一层透明当 solid 处理**：最靠近相机的那层透明材质直接写进 G-Buffer 对应像素位置，打上 **Lit Alpha Flag** 让后续 lighting pass 知道这是透明层，用和 solid 一样的光照路径打光。后面的透明层（多层 OIT 效果）才走 forward + directional only + ambient，承受轻微的一致性损失。这让海面、水、瀑布这类"单层透明 + 需要完整 light 计算"的场景质量接近 solid。

## Volumetric Fog 的两个 tricks

**Shadowed volumetric fog** 用 Toth et al 方法——沿视线 raymarch 采样 shadow map 产出从太阳光穿过大气的 god ray。

问题是 biome 差异巨大：室外日光 + 雾太密会让远处糊、太稀又看不到 light shaft。解法是**全局低密度 + 局部动态拉高**——CPU 侧的 enclosure detection 本来就存在（voxel 游戏嘛，玩家知道自己是不是在洞里），当玩家"进室内"时让局部 fog 密度 ramp up，出门时 ramp down。室内天然昏暗 + 高密度 fog + 太阳穿门缝的 god ray，视觉上 "indoor dusty mood" 直接出来。

**点光"假散射"**——volumetric raymarching 只考虑 directional light，但把 **light buffer 模糊后叠加到 fog** 上，产生点光照亮周围雾的效果。模糊前还把主 RT 的亮点（灯笼、火把等 emissive 中心）阈值化加进去，让灯具自身的光晕更明显。

## Color Grading 走 3D LUT 而不是 tonemap 公式

tonemap 试过 Reinhard、Filmic——艺术家需要**更直接的风格化 knob**，公式参数太抽象。最终选了 [[color-lut|3D LUT color grading]]：HDR 图 tone-scale 到 [0,1] → 在 HDR 游戏截图上贴一张 identity LUT 纹理 → 艺术家在 Photoshop 调到想要的风格 → 从截图抽出被调过的 LUT → 运行时把它变成 3D texture 用原像素颜色当 texcoord 采样。

per-biome 可切 LUT 让雪原偏冷 + 沙漠偏暖 + 日落偏金全部靠一张表实现。这是当时的"甜点解"：灵活性近于后处理 node graph，成本只有一次 3D texture lookup。

## 性能 / LOD / 规模化

voxel 游戏有它自己的扩展困难。Meandros 的解法组合：

- **Shader + geometry LOD**：同一材质多个 variant、距离越远 shader 越简单
- **Tree billboard**：远处的树换成 billboard 而不是 3D mesh
- **Voxel chunk LOD**：远处的 voxel 用更大 voxel size
- **Greedy meshing** ([[greedy-voxel-meshing]])：把相邻同材质面合并成大 quad，vertex buffer 大幅压缩
- **Chunk-based occlusion**：[tomcc 的方案](https://tomcc.github.io/2014/08/31/visibility-1.html)——利用 chunk 边界和可见性传播在 chunk level 剔除
- **后处理降级**：低端机 volumetric fog 退化成 distance fog（没有 god ray 但不掉帧）

## 回到 2015 年

这篇文章的意义与其说是"谁发明了什么"，不如说是**一份 2015 年中型工作室自研引擎的内部切片**——token command stream、deferred + PBR、voxel-specific 的 AO / weather / enclosure 数据流、3D LUT grading，全部都是那个时代的甜点解。几年后 render graph、compute-driven rendering、GI 的 Lumen/VXGI 等会把这些决策重写一遍。但 **token stream 这种架构直到今天仍然是 render graph 的思想底座**（GPU Pro / GDC 里类似体系反复出现），G-Buffer modification for decal / weather 的思想也在 Control、GT7 等大型项目里延续。

## 相关

- [[deferred-rendering]] — 为什么 voxel 沙盒选了 deferred
- [[physically-based-shading]] — Albedo-Metalness-Glossiness 的参数化
- [[microfacet-brdf]] — GGX NDF 的选型
- [[voxel-ambient-occlusion]] — voxel 世界的 AO 专属技巧
- [[greedy-voxel-meshing]] — 减少 vertex buffer 的合并算法
- [[volumetric-fog-froxels]] — 更现代的 fog 算法对照
- [[color-lut]] — 3D LUT color grading 的详细做法
- [[spherical-harmonics]] — six-axis ambient 的更高精度亲戚
- [[screenspace-reflections]] — local SSR + fall-back cubemap 的通用模式
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-skysaga-rendering]]
