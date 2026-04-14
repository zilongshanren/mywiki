---
tags: [渲染, decal, 法线贴图, 材质过渡, fallout, cryengine]
date: 2026-04-14
sources: 1
---

# 法线 Decal 掩盖硬边过渡（Normal Decal Edge Blending）

**Fallout 3 的石头**从远处看崩坏感非常强——像是一块高多边形的碎石；但近看线框会发现石头本体的几何其实**非常低多边形**。那种「carved」感并不是来自几何，而是来自一层**环绕在石头轮廓上的额外 decal 几何**，上面贴着 diffuse 和 normal map，专门用来**遮住低多边形石头与另一层纹理之间的生硬过渡**。

## 要解决的问题

一块石头的主体用一张光滑 stone 纹理贴出来，而它破碎的边缘需要一张不同的 broken-edge 纹理。直接在低多边形上做纹理混合会遇到两个问题：

1. **硬过渡**——UV 边界附近两种纹理会出现肉眼可见的拼接缝
2. **边缘轮廓是几何的轮廓**——低多边形石头的外轮廓就是几个直线段，任你怎么混纹理都改不了那条生硬的外沿

解决办法是在**几何边缘再套一层薄 decal 片**：一个多边形壳环绕着石头的碎边，贴着一张带 alpha 的 normal-mapped 破损纹理。这层 decal 既在颜色上做了渐变（alpha），又在法线上加了起伏（normal map），从而**两层纹理之间有了一个带光照反应的缓冲带**。

## CryEngine 的同款技术

评论区里 *wichenroder* 贴出了 [CryEngine 的官方文档](http://docs.cryengine.com/display/SDKDOC2/Using+Decals+for+Destroyed+Structures)，讲的是几乎一样的做法：在被破坏建筑的边缘摆 normal-mapped decal 来隐藏 mesh 被切开的硬边。Simon 后来在 Crytek 遇到一位前 Bethesda 员工，这位员工证实了 Fallout 3 **确实**用同样的思路——**不是** [[physically-based-shading|parallax mapping]]，而是**真正的额外 geometry**，只是这层 geometry 薄到从线框里几乎看不见。

Simon 用 **Intel GPA** 关闭 Alpha1/AlphaTest 后，破边上的 decal 片显形了——这不是最终的证据，但佐证了「有额外几何存在」。后续一位读者用 NifSkope 直接打开游戏的 `.nif` 模型，清楚地看到 decal 网格是一层略大于实体边缘的薄壳。

## LOD 策略

最漂亮的 trick 是**「LOD 就是把 decal 删掉」**：近距离 decal 带来的轮廓和法线细节值回票价；远距离玩家看不清边缘细节，把这些 decal 片从 LOD 里整张删掉，既节省 draw call 又免去 alpha test 的带宽开销。这是一个典型的「**人眼察觉不到的地方就是 LOD 的第一刀**」案例。

## 作为一个通用原则

这个技巧本质是**把局部的高频细节从几何层搬到一个独立的薄几何层**，然后让这个薄层带着 alpha / normal map 做无缝过渡。它与以下技巧同属一家：

- [[normal-map-blending]] — 在同一 surface 上做法线叠加
- **Relief / parallax mapping** — 在 pixel shader 里伪造凹凸
- [[deferred-grass-shader]] — 把草的 billboard 当作独立几何层

相比 parallax mapping，decal 法的好处是**从任意角度看都是真实几何**，不会在边缘暴露 heightmap 的视差极限。

## 正交细节：法线贴图的 alpha 通道

Simon 顺便发现 Fallout 3 把 specular map 存在 normal map 的 **alpha 通道**里：normal 用 RGB 的三个通道（切线空间 xyz），alpha 存 specular 强度。读者补充说 Bethesda 在 Oblivion / Fallout 3 里这样做是为了**省空间**——带 alpha 的 DXT5 比无 alpha 的 DXT1 大一倍，但把 specular 塞进 alpha 等于用一张 DXT5 替代两张贴图。Skyrim Special Edition / Fallout 4 基本放弃了这种打包，因为 PBR 工作流对 specular 的数据要求变得不同。

还有一个更激进的变种：只在 R、G 两通道存 xy，Z 在 shader 里用 $z = \sqrt{1-x^2-y^2}$ 重建，把 B 通道留给 specular。Fallout 3 没有这么做，可能是为了省掉 pixel shader 里的那一次 sqrt。

## 相关

- [[normal-map-blending]]
- [[painted-foliage-bent-planes]]
- [[fizzle-lod-fading]] — LOD 切换的典型视觉技巧

## Sources

- [[sources/simonschreibt-fallout3-edges]]
