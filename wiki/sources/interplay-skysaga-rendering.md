---
tags: [source, rendering, deferred, voxel, engine, skysaga, pipeline]
date: 2026-04-14
sources: 1
---

# The Rendering Technology of SkySaga: Infinite Isles（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2015 年 4 月发表的一篇 engine tech 总述：Radiant Worlds 的 voxel 沙盒 *SkySaga: Infinite Isles* 使用的自研引擎 **Meandros** 的完整渲染管线——从 token-based command system 到 deferred + PBR 到天气系统的 G-Buffer 修改 pass。这是 interplayoflight 博客里罕见的**整套引擎级别总览**，比其他几篇技术深挖的单点博客密度高得多。

## 摘要

Meandros 的核心是一个 **token submission / processing 系统**：每个可渲染实体生成一串紧凑 token（设状态、绑 texture、切 shader、发 drawcall），token 流被收集在若干 buffer 里，在提交到 D3D API 之前按顺序 sort 和去冗余 state。token 是 cache-friendly 的小数据结构、能 local 访问依赖数据。token 流归属到 **Pipeline Stages**（shadow、lighting、post processing 等），stage 可以串联、前者输出喂后者输入。基于这个 token + stage 体系之上是 **deferred shading** 管线——g-prepass 填一个 **4-RT G-Buffer**（normal/geometric normal/view-space depth + AO / 压缩 albedo + emissive + lit-alpha flag / metalness + midscale AO + glossiness），因为 voxel 世界几何量大 + 动态光源多所以选 deferred 而不是 forward。**BRDF 从 Blinn-Phong → normalized Blinn-Phong → GGX** 演进，走 Albedo-Metalness-Glossiness 参数化、metals 的 albedo 直接当 spec color、非金属 $F_0$ 固定 0.04。HDR 管线全程 64-bit 除 G-Buffer 外。一个太阳 / 月亮主光（cascaded shadow map × 4 + PCF）+ 少量投影点光；云影用两通道 shadow map 分开 solid / translucent 深度，自阴影变差靠 normal offset mapping 补。Ambient 用 Valve 的 six-axis ambient，另外把 voxel occupancy 烘成 3D array 做**光传播**得到 midscale AO——既用于间接光近似又用于"封闭空间 mask"（雪、雾不往洞里飘）。环境反射用一张动态 pre-blurred cubemap。**透明处理**：一层 transparency 存进 G-Buffer 和 solid 一起打光，多层走另一个 deferred 透明 RT。天气系统用一个 **G-Buffer modification pass** 在屏幕空间写雪 / 湿 / 脏 / decal——对 G-Buffer 拷贝 + 条件混合覆盖 normal/albedo/glossiness，用 midscale AO 做 indoor mask。后处理：local SSR（fade to global cubemap）、shadowed volumetric fog（太阳光 shaft 的 Toth et al 方法，indoor 时临时提升 fog 密度做 local light shaft）、Morgan et al 式 DoF、Reinhard/Filmic tonemap 最后换成 **3D LUT color grading**（艺术家 Photoshop 手动微调 LUT，per-biome 可切）。LOD 层面做 shader/geometry LOD + tree billboard + voxel chunk LOD，voxel mesh 用 **greedy meshing** 压、可见性走 Mikola Lysenko 风格的 **chunk occlusion**。

## 关键要点

- **Token + Pipeline Stage 架构**：Meandros 不是一张张 C++ virtual 结构，而是一个 byte stream 的命令记录器——每个 token 紧凑、cache 友好、local 访问数据。stage 之间 output→input 链接让引擎结构显式化，不依赖全局状态。
- **G-Buffer 为天气系统而设计**：把 metalness / AO / albedo / normal / glossiness 都以可独立修改的方式打包到 G-Buffer。天气 / decal pass **复制 G-Buffer 后 alpha blend 回去**——避免污染不该受影响的区域（不给 emissive 面加雪、不让 metal 变湿等），每个属性的 blending 规则独立可调。
- **Ambient occlusion 的两个尺度**：per-voxel 小尺度 AO（corner / intersection 的烘焙暗）+ per-voxel midscale AO（3D occupancy array 上的光传播）。后者兼做"封闭空间 mask"，让雪 / 雾不飘进洞穴、让 decal 在门口自然淡出。这是一种**把几何数据结构当额外信号通道**的做法，voxel 世界的特殊优势。
- **Six-axis ambient** 来自 Valve 的 Half-Life 2 管线——沿 ±x/±y/±z 存六个 ambient color，法线贴图在 shadow 里也能产生变化。biome 间切换只需要换 6 个颜色。
- **Lit transparency**：SkySaga 要大量水 / 瀑布 / 河流，forward-lit 透明在 deferred 引擎里难做。Meandros 把**最靠近相机的一层透明**当作 solid 放进 G-Buffer 和 solid 一起打光，后面的透明层只吃 directional + 环境。
- **Volumetric fog 的 indoor hack**：默认 fog 密度保持低、只在"CPU 确定玩家身处封闭空间"时**临时拉高 fog 密度**——靠 Toth et al 式 shadowed volumetric fog 产生光 shaft。这利用了 voxel 游戏的 enclosure detection 已经存在的事实。
- **Volumetric fog + 点光"假散射"**：volumetric raymarching 只考虑太阳光，但把 light buffer **模糊后叠加到 fog** 产生廉价的点光散射效果。阈值化主 RT 额外补强光源核心亮度。
- **3D LUT color grading** 而不是 Reinhard / Filmic：艺术家要一把 per-biome 可调的风格化工具，程序化 tonemap 的 knob 太抽象。LUT 做法是"截图 → Photoshop 调色 → 提取 identity cube → 采样"。per-biome 切 LUT 让雪原偏冷 / 沙漠偏暖全靠这一张表。
- **Voxel optimization**：greedy meshing 压 vertex buffer、chunk-based occlusion 剔掉不可见大块——这些是 Minecraft-like 引擎的标配技术，Anagnostou 链到 Mikola Lysenko 和 tomcc 的参考实现。
- **Clouds cast translucent shadow**：shadow map 拆 R/G 两通道存两层 16-bit 深度（solid + translucent），避免整个世界被云影压成漆黑；有可选彩色阴影通道支持有色玻璃 / 彩云。

## 链接到的概念

- [[skysaga-rendering-tech]]
- [[deferred-rendering]]
- [[voxel-ambient-occlusion]]
- [[greedy-voxel-meshing]]
- [[volumetric-fog-froxels]]
- [[color-lut]]
- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2015/04/08/the-rendering-technology-of-skysaga-infinite-isles/
- 本地：`raw/articles/interplayoflight.wordpress.com/2015-04-08_the-rendering-technology-of-skysaga-infinite-isles.md`
