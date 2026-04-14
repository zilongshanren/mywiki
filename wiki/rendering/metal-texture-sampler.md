---
tags: [渲染, metal, 纹理, 采样器, msl, mipmap]
date: 2026-04-14
sources: 1
---

# Metal 的纹理与采样器（MTLTexture / MTLSamplerState / constexpr sampler）

[[warren-moore|Warren Moore]] 的 *Textures and Samplers in Metal* 把 Metal 纹理流水线的所有关键对象——**`MTLTextureDescriptor` / `MTLTexture` / `MTLSamplerDescriptor` / `MTLSamplerState`**，以及 MSL 里**两种声明 sampler 的方式**——用一个"给卡通奶牛 Spot 贴图"的例子全部串起来。这一页把其中容易忘的几点按对象分层记录。

## MTLTextureDescriptor：描述、而不是像素

Metal 把「纹理的元信息」和「纹理的内容」分开两步：第一步填一个 `MTLTextureDescriptor`（pixel format + 宽高 + 是否带 mipmap），第二步 `[device newTextureWithDescriptor:]` 拿到一个满足 `MTLTexture` 协议的对象。内容可以后续用 `replaceRegion:mipmapLevel:withBytes:bytesPerRow:` 写进去。一旦创建，**descriptor 里描述的部分（维度、pixel format）就不可变**，但像素数据随时可以更新。

常用的便捷工厂是：

```objc
[MTLTextureDescriptor texture2DDescriptorWithPixelFormat:MTLPixelFormatRGBA8Unorm
                                                   width:w height:h mipmapped:YES];
```

传 `mipmapped:YES` 让 Metal 自动为你算出 `floor(log₂(max(w, h))) + 1` 层的 mipmap 槽位——你仍要自己产生每层的数据，或者交给 Blit encoder 的 `generateMipmapsForTexture:` 做硬件下采样。Warren 在文里提了公式但样例没有实际开 mipmap。

## 坐标系陷阱：Metal 左上原点 vs OpenGL 左下原点

Metal 的纹理像素坐标原点在**左上角**（和 UIKit / Core Graphics 一致），OpenGL 默认是**左下角**。这意味着从 `UIImage` 拿到的 CGImage 位图可以直接交给 Metal，但如果你的模型 UV 是在 Blender / OpenGL 管线里做的，贴上去会**上下翻转**。文章给出的修法是加载阶段做一次翻转：把 Core Graphics context 先 `translate(0, h)` 再 `scale(1, -1)`，再把 `CGImage` 绘进去——相当于沿 y 轴反转。也可以在 shader 里做 `uv.y = 1 - uv.y`，或者在磁盘上就把图翻好，三选一。

## Pixel coord vs normalized coord

Metal 允许用 **normalized 坐标**（0-1 独立于尺寸）或 **pixel 坐标**（0 到 width/height）采样。normalized 是默认、也是推荐——它让 shader 与具体尺寸解耦，便于换贴图。pixel 坐标偶尔用于 blit-style 的 postprocess kernel。

评论区里 Jan 补了一个细节：`coord::pixel` 模式下坐标范围是 `(0, 0)` 到 `(width, height)`（开区间上界），而不是 `(width-1, height-1)`。原点落在**左上角像素**的左上角，不是像素中心。

## MTLSamplerState：把 filter / wrap / coord 打包

采样的具体行为由 **sampler** 决定，它独立于纹理存在。一个 sampler 封装三类状态：

- **Filter mode**：`nearest` 或 `linear`（Metal 叫 `MTLSamplerMinMagFilter*`），用于放大/缩小时的插值。见 [[sampler-filter-wrap-modes|Filter / Wrap 模式]] 的更通用讨论。
- **Address mode**：`clamp_to_edge` / `clamp_to_zero` / `repeat` / `mirrored_repeat`——决定 UV 超出 `[0,1]` 时的行为。Metal 独有的 `clamp_to_zero` 在越界时返回黑色（或透明），OpenGL 里没有对应项。
- **Coordinate space**：normalized 或 pixel。

在 host 侧填 `MTLSamplerDescriptor` 的一个麻烦是**所有参数都要独立设**——min 和 mag filter、s 和 t address mode 都是两个独立字段，无法一行搞定。

## constexpr sampler：在 shader 里声明的免分配版本

MSL 提供了**在 shader 源码里声明 sampler** 的语法糖，避免跑一次 `newSamplerStateWithDescriptor:`。关键字是 `constexpr`（C++11 新特性）——表示 sampler 对象在**编译期**构造，一个 shader 函数里所有调用共享同一份：

```metal
constexpr sampler s(coord::normalized, address::repeat, filter::linear);
```

- 参数可以任意顺序（sampler 构造器是 variadic template）。
- 每个枚举值必须带作用域前缀（`filter::linear` 而不是 `linear`）——这是 C++11 strongly-typed enum 的要求。
- `filter` 同时设置 min 和 mag；想分开用 `min_filter::...` 和 `mag_filter::...`。

constexpr sampler 适合"这个 shader 就是用这一套采样规则"的场景——filter 和 wrap 是静态选定的。如果要**运行时切换**（同一个 shader 对不同材质用不同 sampler），就得走 host 侧的 `MTLSamplerState` 加 `[[sampler(n)]]` 绑定。

## 绑定模型：texture 和 sampler 走独立的 argument table

纹理和采样器在 shader 侧分开绑定：

```objc
[encoder setFragmentTexture:texture atIndex:0];
[encoder setFragmentSamplerState:sampler atIndex:0];
```

shader 侧用 `[[texture(0)]]` 和 `[[sampler(0)]]` 分别引用——它们虽然索引都是 0，但位于不同的 argument table 槽位。采样一次：

```metal
float4 color = tex.sample(s, vert.uv);
```

## 一个易错的 texture 使用点：iOS 9 之后的 `usage` flag

评论区里 David Hoerl 指出：iOS 9 引入了 `MTLTextureDescriptor.usage`（默认 `MTLTextureUsageShaderRead`），如果你想让纹理被 compute kernel 写入，必须显式置 `MTLTextureUsageShaderRead | MTLTextureUsageShaderWrite`——老文章的样例里没有这一行，跑在新 SDK 上就会失败。这是 API 演进带来的隐性 breaking change 的典型例子。

## 相关

- [[metal-api-overview]]
- [[metal-shading-language-basics]]
- [[sampler-filter-wrap-modes]] —— 通用的 filter / wrap 讲解
- [[mipmap-moire-scanline]] —— mipmap 的动机与常见失真
- [[warren-moore]]

## Sources

- [[sources/metalbyexample-textures-and-samplers]]
