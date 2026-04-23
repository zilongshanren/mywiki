---
tags: [source, 渲染, 延迟渲染, 光照, light-prepass, msaa]
date: 2026-04-19
sources: 1
---

# Mythbusting: deferred rendering（Angelo Pesce / C0DE517E 2011-01-22）

[[angelo-pesce]] 2011 年初写的六条「延迟渲染常见误解」——在 deferred shading 已经成为 AAA 默认管线、light-prepass 与 tiled 正在铺开的时点，把业内流传的六种断言拆开讨论。这篇是 Pesce 博客的代表作之一，对理解这代渲染工程师如何**拒绝把技术选择神圣化**非常有用。

## 摘要

**六条神话 + Pesce 回答：**

**#1 延迟是不是好？** 是，且应该一直「想着 deferred」——但**要记住 deferred 不是某一项具体技术**，它是「**把计算拆到不同 pass、不同 space**」这个**通用手法**的一个实例。separable blur、screen-space shadow、光照到 UV 空间（surface caching）都是同一思路的其他应用。**与其抄标准 deferred，不如自己定义**：你的 lights 怎么来？有没有 shadow？是否需要 transparency？把 deferred 和 forward 当同一谱系的两端来混搭。

**#2 deferred 是处理大量灯的唯一方法？** 不是。**light-indexed deferred**（把灯索引写进像素再在 material shader 里循环）、forward 多 pass additive、forward 按对象分配灯 + cap 数量——都是可选工具。2011 年「纯 deferred」已经不值得再做；几乎所有 deferred 工程本身也带着一个 forward multipass（至少用来处理 alpha），**不对单灯物体走 forward 就是浪费**（Halo Reach 是公开案例）。

**#3 deferred 能替代 lightmap？** 不能。**deferred 只擅长无阴影 point light**——要么你接受 phong-shiny 3ds Max 4 DOS 风格的画面，要么让美术堆灯加 cookie 假装 GI，回到 90 年代。Lightmap 是**precomputation = 拿空间换性能**的一个实例，对静态场景 / 静态部分**永远有意义**。实时 GI（Geomerics 等）属于另一条赛道。

**#4 deferred shading 比 deferred lighting（light prepass）慢？** 不一定。memory 差距没那么大：**DS 典型 6 张 32-bit RT vs LPP 5 张**（不是 4 vs 1）；更多 memory 不等于更多带宽——两者写 attribute 的 pass 都基本 overdraw-free（front-to-back + z-prepass + [[tiled-light-prepass|tiled variant]]）。真正的瓶颈在 **lighting pass** 的 overdraw——DS 在 texture stage、LPP 在 blend stage 各有 bottleneck。而且**很多 deferred 引擎根本不是 bandwidth-bound**，是 ALU bound 或 vertex bound（LPP 要两次几何 pass）。评论区的一位读者反驳：LPP 只需「lighting buffer + final/normal 共享 + depth」，即 3（或 4）张；Pesce 回应 8-bit 光照 buffer 不够精度，至少要 16-bit 或 diffuse+specular 两张，带宽计算仍然接近。

**#5 LPP 能表达比 DS 更丰富的 material？** 基本不能。LPP 在 material pass 拿到的已是「固定 Phong 模型的结果」——二次几何 pass 的可操作空间微乎其微，而且 **specular 在 LPP 里有根本缺陷**（specular contribution 被线性相加、多数实现只支持单色高光）。两者都**解耦光和材质解得太晚**——都在 BRDF 内部解。**light-indexed 解得最早**（灯 attribute 层）；有没有中间点（比如存 radiance 而非 irradiance，SH 编码）是有趣的开放问题。Crytek 在 CryEngine 2/3 用相关思路做了 anisotropic materials。

**#6 LPP 对 MSAA 更友好？** 算是。不写 per-sample attribute 的话两种方案都需要 bilateral / inferred-lighting 式的 discontinuity 过滤才能配 MSAA——「很多人干脆不做 MSAA，改用 MLAA 等 post filter」。**DX10.1 后**可以 per-sample shade at discontinuities；此时 LPP **在边上 shading 的存储代价显著低**——LPP 的 lighting 结果只有一张 buffer（可与 final buffer 共享 memory），per-sample 保存 = final buffer 的体积；DS 要 per-sample 保存 4 张 G-Buffer，基本疯狂。一个常见 hack 是对 G-Buffer 做 manual resolve（albedo 做平均、normals 取 nearest-depth sample），勉强可用但不对。

**补充 tips**（update 段）：**deferred 的 decal 便宜**（光照已在表面上算好，decal 只需修改 normal 再 reuse lighting）；**小三角形 quad 浪费在 DS 里相对 LPP 较轻**（DS 只有一次 GBuffer pass，LPP 的两次几何 pass 都吃 quad overhead）。评论区读者补充：**clustered lighting 对 forward 与 deferred 通用**，只是 view-space bucketing 的 CPU 成本要小心。

## 关键要点

- **deferred 是一个通用 pattern（拆 pass、换 space）的实例**——不要把它神圣化。
- **2011 年「纯 deferred」已过时**——应至少混 forward multipass 处理 alpha 和单灯物体。
- **LPP 不一定比 DS 快**——memory 差距 6 vs 5 张而非 1 vs 4，瓶颈取决于平台（PS3 blend / 360 texture）。
- **LPP 的 specular 有根本缺陷**——多光源线性叠加 specular 是物理错的，多数实现还仅支持单色。
- **light-indexed 是「解耦得最早」的路线**——在灯 attribute 层而非 BRDF 层做 indirection。
- **per-sample MSAA 在 LPP 上可行、在 DS 上疯狂**——因为 LPP 的 intermediate buffer 体积小。
- **deferred 对 decal 与 small-tri quad 浪费各有好处**——少见讨论的工程细节。
- 如果 deferred 要有一个更准确的名字，应该叫 **image-space shading**——把 surface caching / megatexture + UV-space shading 都纳入同一谱系。
- 底层认知：**precomputation（lightmap） = 空间换性能**的 pattern，**deferred = 空间换灵活性**的 pattern，**它们不互斥也不可替代**。

## 链接到的概念

- [[angelo-pesce]]
- [[deferred-rendering-mythbusting]]
- [[deferred-rendering]]
- [[light-prepass-pipeline]]
- [[tiled-light-prepass]]
- [[aa-techniques-survey-2011]]
- [[msaa-ssaa]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/01/mythbuster-deferred-rendering.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-01-22_mythbusting-deferred-rendering.md`
