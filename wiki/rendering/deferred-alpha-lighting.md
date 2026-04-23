---
tags: [渲染, 延迟渲染, 透明, 光照, alpha混合]
date: 2026-04-14
sources: 1
---

# 延迟渲染里给透明物体打光的四条路

[[deferred-rendering|deferred shading]] 的长板是大量光源下的摊销效率，短板是**透明物体的处理**：G-Buffer 每个屏幕像素只能存一份材质属性，而半透明天然需要把多层重叠的颜色/材质全部保留到最后 blend。一旦你决定让场景里的玻璃、水面、气泡真正被几十个动态光源照亮，就必须在标准 deferred 的外面另想办法。[[kostas-anagnostou|Kostas Anagnostou]] 在 Hieroglyph light prepass 上做了一轮梳理，整理出四个互相独立的路子。

## 1. Deep G-Buffer / Per-Pixel Linked List

最朴素的想法：**把 G-Buffer 深化**，为可能的 alpha 叠加层数预留额外层。Humus 的 deep G-buffer 就是这种；DX11 之后的版本通常用 **per-pixel linked list** 把可变数量的 alpha fragment 挂在每像素上，最后一次遍历做 back-to-front 的 blend。功能最强，精度最好，缺点同样明显：显存吃得很凶，硬编死的层数永远不够用，而 linked list 本身需要 atomic 和 UAV 支持，在早期硬件上不现实。

## 2. Stencil 多 Pass

John Chapman 的方案：**对每个透明物体都跑一遍完整的 deferred 流程**——写 G-Buffer、在 stencil buffer 中标记受影响像素、用 stencil 当 mask 累加光照、最后把结果 blend 回主帧缓冲。正确，但成本是 O(#透明物 × #灯)——每多一个物体就要多一整套 light accumulation pass，在灯数多或透明物多的场景下会很快炸开。

## 3. 屏幕门 / Dithered / Stochastic Transparency

把问题**绕开**：不真的做 alpha blending，而是用**屏幕门**（stippled alpha）让透明物假装不透明地进入 G-Buffer——用点阵图案让底层像素从透明物的「孔洞」里透过来。Inferred Rendering 就是这条路；进一步的 **Stochastic Transparency** 用随机化的子像素点阵，噪声换精度。适用于真实硬件资源吃紧的场景，代价是视觉上明显的 dither 噪声。[[dither-alpha-clipping|dither-alpha-clipping]] 里讨论过它和 LOD fade 的关系。

## 4. UV 展开渲染到纹理（Creative Assembly, Develop 2012）

Creative Assembly 在 Develop 2012 提出的方案，也是 Kostas 这篇文章亲自实现的那条：

1. **把所有透明物体 UV 展开到一张共享纹理**里——前提是它们的 UV 不能重叠或镜像。
2. 在这张纹理的每个 texel 写入对应表面点的**世界空间（或 view 空间）坐标**，相当于一张「不在屏幕上的 G-Buffer」。
3. **把这张纹理交给 light prepass / 光照 pass**，让光照遍历场景所有灯，对 texel 里存的位置做光照计算，写出一张 **alpha object lightmap**。
4. 最后用 **forward rendering** 正常渲染透明物，shader 采样这张 lightmap 作为其已经被场景灯照过的漫反射输入。

核心 insight 是把光照目标从「屏幕像素」改成「物体表面」——一旦位置信息不再绑定 screen-space，就不受 alpha blending 的 depth 排序约束，也就不受 G-Buffer 层数约束。代价：

- **镜面反射不便宜**——只存位置就只能做 diffuse；要加 specular 得再加一张法线纹理，内存翻倍。
- **纹理容量是硬上限**——能塞多少个 alpha 物体取决于 UV 打包效率，大型场景里透明物太多就塞不下。
- **光照 pass 要改**——标准 tile/cluster light culling 假设输入是 screen-space 像素坐标，UV 展开的 lightmap 需要用世界位置重新做 light-volume 相交和剔除。

这套方案视觉上和「真正的 per-object forward lighting」效果一致，但省掉了在每帧对每个物体做一遍 light culling 的 CPU 开销——灯光遍历可以和场景其它 deferred 灯光一并处理。

## 相关
- [[deferred-rendering]]
- [[alpha-blending]] — 透明物的排序/混合数学
- [[tiled-light-prepass]] — 本文原型所用的引擎
- [[dither-alpha-clipping]] — 屏幕门类方案的近亲
- [[kostas-anagnostou]]
- [[hybrid-hair-rendering]] —— 另一种 deferred + alpha 的 hack：头发按「实心 + 边缘」两段分别走 deferred / forward
- [[xplane-deferred-pipeline-hacks]] —— X-Plane 10.10 的 alpha-in-deferred 选择：G-Buffer 内按 src-alpha 加权平均全部通道（除 eye-space Z），albedo/emissive 层间必须 sRGB blend

## Sources

- [[sources/interplay-lighting-alpha-deferred]]
