---
tags: [渲染, 光照, 延迟渲染, 分块]
date: 2026-04-14
sources: 1
---

# Tiled Light Prepass

**Crystal Dynamics Foundation 引擎（Rise of the Tomb Raider）使用的一种非主流光照方案**。它与主流的 [[deferred-rendering|deferred rendering]] 刚好相反：deferred 的思路是「把材质属性全部写进 G-Buffer，再统一做光照」；light prepass 则是**先把光照全部算好写成几张光照图，再重新提交几何、把材质属性取出来与光照相乘**。

## 为什么叫 prepass

Light prepass 只需要最小集合的几何信息来做光照——典型的只需要 **法线、粗糙度、金属度位**。为此需要一个非常瘦的「Normals Pass」：写入深度和 RGBA16_SNORM 的世界空间法线（alpha 通道塞 glossiness，符号位做 metallic 标记）。注意这个 pass 不同于标准 deferred 的 fat G-Buffer——缺少 albedo、AO、emissive、微遮蔽等。

之后光照计算在屏幕空间进行，并输出到**三张 RGBA16F**：

- diffuse 光照
- specular 光照
- ambient 光照

所有阴影已经在这一步应用完毕。

## 第二次提交几何

然后——这是 light prepass 区别于 deferred 的关键——**所有不透明几何体第二次被提交进管线**，每个物体在自己的像素着色器里采样这三张光照图、采样自己的 albedo/AO/emissive 等纹理，直接得到最终颜色。

相比 deferred，这个方案：

- **省带宽**：不用把所有材质属性写进 fat G-Buffer 再读出来；只有必需的光照输入进出显存
- **费绘图调用**：几何被提交两次，draw call 和顶点负载都翻倍
- **材质灵活**：每个物体可以有自己独特的 BRDF 组合，不被 G-Buffer 的固定布局绑死

## Tiled 的那部分

Light prepass 本身只解决材质/光照的分离。要进一步处理**大量光源**，Foundation 把屏幕切成 **16×16 的 tile**，在每一 tile 内预先计算覆盖它的光源列表，光照 pass 只遍历 tile 内的光源——和 [[deferred-rendering|tiled deferred]] 的 light culling 是同一种优化。透明物体光照也直接复用这套 tile 分类数据。

## 与主流方案的对比

| | Forward | Tiled Deferred | Tiled Light Prepass |
|---|---|---|---|
| G-Buffer | 无 | fat | thin（仅法线+粗糙度） |
| 几何提交次数 | 1 | 1 | 2 |
| 带宽压力 | 中 | 高 | 中 |
| 材质灵活性 | 高 | 低 | 高 |
| draw call | N | N | 2N |

Light prepass 是早年 PS3/Xbox 360 带宽紧张时代的产物（Crysis 2、Uncharted 走的都是这条路），后来随着显存带宽提升、deferred 成为主流而渐渐少见。Foundation 在 2015 年还在坚持这条路，是相对罕见的工程选择。

## 相关

- [[deferred-rendering]]
- [[rendering-pipeline]]
- [[fragment-shader]]
- [[early-z-late-z]]
- [[tiled-light-culling]] —— 和本页讲的管线结构不是同一件事：light culling 指 tile 级 per-light 剔除机制，和 deferred / forward+ / light prepass 的管线形态正交
- [[instant-radiosity-vpl]] —— light prepass 擅长消费大量 VPL 的经典示例
- [[deferred-alpha-lighting]] —— 在 Hieroglyph light prepass 上验证的 UV unwrap lightmap 方案

## Sources
- [[sources/elopezr-rotr-rendering]]
- 相关：[[light-prepass-pipeline]] — Engel 原始 light pre-pass，Ni No Kuni 2 里的实例
