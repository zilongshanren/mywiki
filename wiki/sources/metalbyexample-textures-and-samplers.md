---
tags: [source, 渲染, metal, 纹理, 采样器, 教程]
date: 2026-04-14
sources: 1
---

# Textures and Samplers in Metal（Warren Moore）

[[warren-moore|Warren Moore]] 2014 年 9 月的 *Metal by Example* 系列教程，继续在 Part 3 的茶壶工程之上教"怎么给 3D 模型贴图"——以卡通奶牛 Spot 为例展示 `MTLTexture`、`MTLSamplerState`、以及 MSL 里 `constexpr sampler` 的用法。

## 摘要

文章先花一节讲**texture mapping 的基本概念**——把 3D mesh"展平"成 2D 图的 UV 映射，以及 Metal 左上原点 vs OpenGL 左下原点的坐标系差异（UIKit 和 Core Graphics 都是左上原点，所以从 `UIImage` 来的贴图不需要翻转，但从 Blender / OpenGL 管线导出的 UV 会上下颠倒）。然后细聊 **filtering**（nearest / linear）和 **mipmap**——提到 mipmap 层数公式 `floor(log₂(max(w,h))) + 1`，但样例本身没开 mipmap。**Addressing mode** 一节展示 Metal 独有的 `clamp_to_zero`（越界返回黑色）与常见的 `clamp_to_edge` / `repeat` / `mirrored_repeat`。创建纹理的流程是 `MTLTextureDescriptor` + `newTextureWithDescriptor:` + `replaceRegion:...withBytes:`——内容和描述分开两步。加载 `UIImage` 走的是 Core Graphics bitmap context，context 用 `translate + scale(1, -1)` 做垂直翻转以匹配 Metal 坐标系。Sampler 可以在 **shader 里**用 `constexpr sampler s(coord::normalized, address::repeat, filter::linear)` 声明（C++11 的 strongly-typed enum 和 variadic template 特性），也可以在 **host 侧**用 `MTLSamplerDescriptor` + `newSamplerStateWithDescriptor:` 构造。两种 sampler 通过 `[[sampler(n)]]` 和 `[[texture(n)]]` 分别绑定到 shader argument table 上。评论区值得一读：iOS 9 引入的 `textureDescriptor.usage` 默认值为 `ShaderRead`，让老代码的 compute kernel 写操作集体失败；pixel 坐标范围是 `(0, 0)` 到 `(width, height)`（而非 `width-1`）；David Gavilan 提醒 `MTKTextureLoader` 出现后更简单。

## 关键要点

- **Metal 纹理坐标左上原点**——与 UIKit 一致，但与 OpenGL 的 `(0,0)` 左下相反，从 OpenGL 管线迁移的资产需要 vertical flip。
- **Texture 创建两步走**：descriptor（immutable 的维度 / format）+ content（可更新）。mipmap 层数可以自动算，但层级数据需要自己产生或交给 blit encoder。
- **constexpr sampler 的价值**：在 shader 里声明，编译期构造，整个函数共享一份；代价是参数必须静态——运行时切换只能走 host 侧 `MTLSamplerState` + `setFragmentSamplerState:atIndex:`。
- **MSL sampler 语法的 C++11 味道**：variadic template 构造器 + strongly-typed enum 让 `filter::linear` 的作用域前缀强制化。
- **Texture 和 sampler 走独立 argument table**：`[[texture(0)]]` 与 `[[sampler(0)]]` 的 `0` 是不同槽位。
- **Interleaved vertex buffer 的选择**：评论区里 Apple 工程师的立场是"interleaved 是更好的默认"——原因是 cache coherency，从同一个 buffer 相邻位置连续读多个 attribute 比跨 buffer 跳读友好得多。

## 链接到的概念

- [[metal-texture-sampler]]
- [[metal-api-overview]]
- [[metal-shading-language-basics]]
- [[sampler-filter-wrap-modes]]
- [[mipmap-moire-scanline]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/textures-and-samplers/
- 本地：`raw/articles/metalbyexample.com/2014-09-29_textures-and-samplers-in-metal.md`
