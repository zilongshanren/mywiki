---
tags: [渲染, 延迟渲染, 光照, light-prepass, 工程判断]
date: 2026-04-19
sources: 1
---

# 延迟渲染的六条误解（Pesce 2011）

[[angelo-pesce]] 2011 年初在博客把「延迟渲染」这代技术的常见误解拆成六条。这篇的价值不在给定论，而在**给一套拒绝把技术神圣化的判断框架**：把 deferred 看作「**拆 pass、换 space**」这个通用手法的一个实例，而不是和 forward 对立的独立分类。以下六条误解 + Pesce 的修正。

## 神话 1：「deferred 就是 G-Buffer + 光照 pass」

**修正**：deferred 是**通用手法**。任何一次「把计算从 pass A 挪到 pass B、从 space X 挪到 space Y」都是 deferred 思想的实例：separable blur、screen-space shadow、UV-space surface caching（Abrash 早期提出）、甚至 [[virtual-texturing|megatexture]] 都能套进来。更准确的名字应该叫 **image-space shading**——和「future 的 UV-space shading」是一体两面。工程上要做的不是选 deferred 还是 forward，而是**针对自己的 lights / alpha / GI 需求定义一套混合管线**。

## 神话 2：「要处理大量灯必须 deferred」

**修正**：不必。可选工具至少还有：

- **Light-indexed deferred**：把灯的 index 写到像素上，由 material shader 自己循环读灯 attribute——解耦最早、材质最灵活。
- **Forward multipass additive**：每盏灯一次 draw，additive blend。老但仍有效。
- **Forward + per-object light assignment + cap**：对「物体相对光源小」的场景足够。
- **[[tiled-light-prepass|Tiled / clustered]]**：forward 与 deferred 均可享用的现代做法。

Pesce 的断言是：**2011 年再做「纯 deferred」已无意义**——几乎所有 deferred 工程都伴随 forward multipass（至少处理 alpha）。不对「仅被 1 盏灯影响」的物体走 forward 就是浪费；Halo Reach 公开过这一 hybrid 做法。

## 神话 3：「deferred 能替代 lightmap」

**修正**：不能。**deferred 只擅长无阴影 point light**——接受 3ds Max 4 DOS 风格的 phong-shiny 画面，或让美术堆灯加 cookie 假装 GI。Lightmap 的本质是**precomputation = 空间换性能**这一通用模式，对**场景中任何静态的部分**都永远有意义。烘焙慢是**工具链问题**（可以用 CUDA / 分布式加速），不是技术本身的问题。实时 GI（Geomerics 等）是**另一条独立赛道**，不是 deferred 的延伸。

## 神话 4：「deferred shading 比 light-prepass 慢（带宽）」

**修正**：不一定，分三层：

1. **Memory 差距没那么大**：典型 DS = 4 张 RGBA8 + depth + final = **6 张 32-bit**；典型 LPP = 1 张 RGBA8（normal + spec exp）+ depth + 1~2 张 lighting（8-bit 不够精度，多数用 16-bit 或两张 8-bit diffuse+specular）+ final = **约 5 张**。**6 vs 5，差距小**。
2. **更多 memory ≠ 更多带宽**：写 attribute 的 pass 两者都能做到 overdraw-free（front-to-back sort + z-prepass）。
3. **瓶颈在 lighting pass 的 overdraw**：
   - **DS**：bottleneck 在 texture stage（多张 G-Buffer 要采）。
   - **LPP**：bottleneck 在 blend stage（PS3 尤其痛）。
   - 出路是 **[[tiled-light-prepass|tiled variant]]**，让每个 tile 只遍历覆盖它的灯列表。

且**很多 deferred 引擎根本不是 bandwidth-bound**，是 ALU bound 或 vertex bound（LPP 需要两次几何 pass，二次 vertex transform 不可忽略）。

## 神话 5：「LPP 能表达比 DS 更丰富的 material」

**修正**：基本不能。LPP 的 material pass 拿到的已是「固定 Phong 模型的结果」——二次几何 pass 的发挥空间很小。更关键：**LPP 的 specular 有根本缺陷**——多光源 specular 被线性相加（物理错），且多数实现只支持单色 specular。

两种 deferred 都**解耦光与材质解得太晚**（都在 BRDF 内部解）。更极端的是 **light-indexed**：解耦发生在灯 attribute 层——材质完全自由。中间点是开放问题：能否存 **radiance** 而非 irradiance？SH 编码？CryEngine 2/3 用类似思路做了 anisotropic materials，方向上可行。

## 神话 6：「LPP 对 MSAA 更友好」

**修正**：**per-pixel shade**时两者都不行——都需要 bilateral 或 [[aa-techniques-survey-2011|inferred-lighting]] 式的 discontinuity filter，否则 G-Buffer 的不连续会 resolve 失败。**很多工程直接放弃 MSAA 改用 MLAA / FXAA 等 post filter**。

**per-sample shade at discontinuities**（DX10.1+）时 LPP 确实占优：

- **LPP**：lighting 结果只是一张 buffer，per-sample 版本体积 = final buffer 的大小，且可与 final buffer 共享 memory。
- **DS**：per-sample 保存 4 张 G-Buffer 基本疯狂。常见 hack 是对 G-Buffer 做 manual resolve（albedo 做平均、normals 取 nearest-depth sample）——不严谨但能用。

## 少被提及的两个 deferred 优势

- **Decal 便宜**：光照已在表面上算好，decal 只需要改写 normal 再复用 lighting，不用给 decal 重新跑一遍灯。同样便宜的还有 G-Buffer 里塞「1-pixel probe」给粒子 / 透明物 reuse 光照（Saints Row 3 用过）。
- **小三角 quad 浪费相对 LPP 轻**：DS 只有一次 GBuffer pass；LPP 两次几何 pass 都要吃 quad overhead。在 tessellation 时代尤其相关。

## 这篇的元启示

Pesce 的六条写法共享一个判断轴：**技术选择要回到「我的工程约束是什么」而非「业界现在做什么」**。

- deferred 不是一个**结构**——是一个**模式**。
- LPP / DS / light-indexed / forward+ / tiled 不是互斥分类——是**连续谱系**。
- 精度、带宽、ALU、vertex、overdraw、quad 浪费是**六个独立维度**，每个项目都要测自己的瓶颈。

这种「拒绝把技术神圣化」的态度在 [[angelo-pesce]] 的博客是一贯风格（cf. [[pitfalls-of-experience]]、[[experience-as-noise-filter]]）。

## 相关

- [[deferred-rendering]]
- [[light-prepass-pipeline]]
- [[tiled-light-prepass]]
- [[aa-techniques-survey-2011]]
- [[msaa-ssaa]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-mythbusting-deferred]]
- [[sources/c0de517e-deferred-renderer-lessons]]
