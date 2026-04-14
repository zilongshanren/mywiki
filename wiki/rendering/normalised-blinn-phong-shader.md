---
tags: [渲染, pbr, blinn-phong, 能量守恒, 教学, toksvig-aa]
date: 2026-04-14
sources: 1
---

# 归一化 Blinn-Phong 教学 Shader

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年给美术同事写的一个 FX Composer 工程：把**归一化 Blinn-Phong**做成"组件可切换"的单 shader，逐项演示"从旧式 Blinn-Phong 走向 [[physically-based-shading|PBR]]"时每一项到底改变了什么。它不是生产可用代码，而是一个可以让非图形程序员**肉眼对比每个开关**的教具。

## 为什么要归一化 Blinn-Phong

传统 Blinn-Phong 的 specular 项是 $(N\cdot H)^n$，没有归一化常数——提高 $n$（更光滑）只让高光变尖、峰值不变。这违反能量守恒的直觉：**同样一份入射能量**，粗糙表面把它铺在宽光斑上，光滑表面把它聚成一个尖点，所以尖点峰值必须更亮。归一化常数（通常取 $(n+2)/8$）恰好补这个——它让 specular lobe 的半球积分近似恒定：

$$f_r^{spec}(l, v) = \frac{n+2}{8\pi}\,(N \cdot H)^n\,F(L\cdot H)\,(N \cdot L)$$

视觉后果是高光越尖越亮，也必然要求渲染管线进入 **HDR**——峰值会越过 1.0，必须交给 tonemapper 处理。Anagnostou 在 shader 里放了一个 Reinhard 开关来示意。

## 归一化和"关掉 specular"的张力

艺术家从旧管线带来的肌肉记忆是"specular mask = 纯黑通道，直接把高光关掉"。归一化项让这件事变得微妙：$(n+2)/8$ 在 $n=0$ 时的下限是 0.25——即使 spec power 归零也永远有一点环境镜面响应。物理上这是对的（现实里没有完全无高光的表面），但美术需要一把斧头。

Anagnostou 给的折中：**保留归一化、用 `gloss == 0` 做 mask**——gloss 贴图里画黑的地方完全不做 specular。另一种在 deferred 渲染里更难实现的方案是专门的 specular color map，用纯黑 spec color 关掉；deferred 下为它塞通道代价高，多数引擎不走这条路。

评论区里还纠正了一个 2013 年仍在流传的误解：Fresnel **不会**破坏能量守恒——现实材料本来就有 Fresnel。Anagnostou 文中说 Fresnel 是"为好看而接受的违反"，评论者 Naty Hoffman 式指出 Fresnel 是镜面反射能量的重新分布，总入射能量由 $F_0$（非金属 ≈0.04，金属 ≈albedo）决定，不是被放大。

## Gloss → spec power 的映射与线性化

多数管线用一张 gloss map 驱动 per-texel 的 specular power。从 $[0,1]$ 映射到可用的 $n$ 有两种：

- **线性**：$n = g \cdot scale$（分辨率均匀）
- **指数**：$n = 2^{g \cdot scale}$ 或 $n = g^p \cdot scale$（小 gloss 值分辨率更高，光滑面差异集中在最后一档）

指数映射通常更好——绝大多数材料是"粗糙"的，把分辨率给到光滑末端才有意义。

**更隐蔽的一个点**：gloss 贴图是美术在 Photoshop 里绘制的，和 albedo 一样是 sRGB 空间的 8-bit 图。如果不做 $\gamma$ 解码就喂进指数映射，gloss 的感知曲线会被 $\gamma \approx 2.2$ 二次放大——美术滑一下 gloss，高光会"爆炸式"变尖。Anagnostou 演示了 `LineariseGlossiness` 开关：线性化之后高光随 gloss 增长更平滑、更可控。这是[[color-space|线性空间渲染]]的一个容易被忽视的角落——颜色贴图都知道要线性化，单通道数据贴图（gloss、roughness、metallic mask）也一样要考虑。

## 金属 vs 非金属的 Fresnel 上色

文章展示了 Fresnel 如何兼职编码材质类别：

- **非金属**：单色低强度 $F_0 \approx 0.04$；diffuse 提供颜色
- **金属**：有色高强度 $F_0 \approx$ albedo；diffuse 为零，颜色完全来自 Fresnel + IBL

直接关掉 diffuse + 给个金色 Fresnel 之后，若没有 [[environment-probe-placement|环境光源]] 金属会看起来死气沉沉。加上预过滤的 cubemap（glossier → 更高 mip 级），金属才真的"活过来"。这是 PBR 直接推动 IBL 普及的一个具体例子——旧 Blinn-Phong 里金属一般靠夸张 ambient 硬撑，新管线必须加 cubemap。

## NdotL 对 specular 也生效

有个细节容易漏：$(N\cdot L)$ 不是 diffuse 专属——它属于 lighting 方程（入射能量的余弦项），应该乘在 diffuse **和** specular 上。文章对比了两种情况：不乘 NdotL 时，法线贴图正反面都能吃到高光，背光面会闪一些虚假的高光"鳞片"；乘上之后背面像素清零，符合物理。

## Toksvig specular 抗锯齿

远处表面的 mipmapped normal map 会因为 filter 而丢掉高频细节——平均后的法线向量长度 $< 1$，"粗糙度"在数据里其实已经增加，但 shader 看到的 $n$ 没变，结果是**远距离高光过尖**、相机动的时候高光在像素之间沸腾。

Toksvig 方案从 mip-averaged normal 的长度推算子像素粗糙度：

$$L = |\bar{n}|, \quad n_{eff} = \frac{L \cdot n}{L + n (1 - L)}$$

$L$ 越短 → 子像素越粗糙 → $n_{eff}$ 越低 → 高光自动变钝。这是最便宜的 specular AA 解，不需要任何额外 pass，纯解析式，也不改 mipmap 生成管线。Anagnostou 的演示里相机移动时的高光沸腾肉眼可见改善，静态截图的差别就小得多。

## 在这个 wiki 里的位置

这篇文章是美术/程序员对 PBR 过渡期的一个完整教学包——它不是[[microfacet-brdf|微表面 BRDF]] 的正式推导，更像是"用一个能切换开关的 Blinn-Phong 让 PBR 各个组件显形"。目标读者恰恰是那些"仍然想要 specular mask"的老派美术，文章的口吻里也能看到 Anagnostou 自己的无奈："如果美术威胁要辞职除非给 spec mask⋯⋯"。从架构观点看，这个 shader 位于 PBR 的"前菜"——[[journey-sand-specular|Journey 的风格化 sand specular]] 是反向案例（非 PBR、不归一化、多路 spec 相 max），它们一起说明 PBR 的选择从来都是艺术权衡而非强制义务。

## 相关

- [[microfacet-brdf]] — Blinn-Phong NDF 的现代继承者
- [[physically-based-shading]] — 文章要传达的最终目标
- [[color-space]] — 为什么 gloss 贴图也要线性化
- [[kostas-anagnostou]]
- [[journey-sand-specular]] — 反向案例：多路 non-PBR specular 叠加
- [[fragment-shader]]

## Sources

- [[sources/interplay-normalised-blinn-phong]]
