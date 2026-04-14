---
tags: [渲染, shader, 纹理, uv, gamemaker, atlas]
date: 2026-04-14
sources: 1
---

# 纹理图集下的 UV 归一化与多纹理采样

GameMaker、Unity sprite atlas、Unreal virtual textures ——几乎所有现代 2D/混合引擎都会把多个小 sprite 打包到一张大**纹理页（texture atlas）**里，用来减少 draw call 和提升带宽利用率。这种打包对上层几乎透明：你画一个 sprite 时，引擎会自动把它的 UV 转换到 atlas 上对应的那一小块矩形里。可一旦你要写 shader 在 UV 上做非平凡操作（翻转、波浪扭曲、normal map 叠加、两张贴图混合），atlas 就会以两种方式露出它原本的抽象泄漏：**UV 范围不再是 0–1**，且**两张贴图通常在 atlas 里位置不同**。[[xor-shader-artist|Xor]] 在这篇教程里给出了一个简洁的解法。

## 纹理页的抽象泄漏

一张默认 atlas（GM 里通常是 2048×2048 的 2 次幂纹理页）里塞了椅子、NPC、HUD 图标等一堆 sprite。每个 sprite 在 atlas 上有一个 `[u0, v0, u1, v1]` 的矩形范围——椅子可能占 `[0.4, 0.2, 0.7, 0.6]` 这一小块。

直接在 shader 里用 `v_vTexcoord` 会遇到三类问题：

1. **UV 不是 0–1**：想做个「整个 sprite 的上半部分特效更强」的渐变？分子不再是 `v_vTexcoord.y`——你得先知道 sprite 在 atlas 里的 `v0`、`v1`。
2. **wrap 模式废了**：`fract(uv * 5.0)` 这样的周期重复会跨出 sprite 的矩形边界，采到邻居的像素。GM 在 sprite 边缘加了一圈复制像素防止滤波串色，但这防不了 shader 主动乱走。
3. **多张贴图位置不同**：想把一张 diffuse 和一张 normal 叠在一起？两者在 atlas 上位置不一样，同一个 UV 对 A 是 diffuse 中心，对 B 可能是别的 sprite 边缘。

GM 提供了「Separate Texture Page」把某个 sprite 单独放一页（强制 power-of-2、加 padding），但这会增加 texture page switch（影响 batching）并打乱尺寸。更好的做法是**在 shader 里把 UV 归一化**。

## 归一化：两个一行函数

通过 uniform 把 sprite 的 atlas 矩形传进来（`sprite_get_uvs` 拿到 `[x, y, x+w, y+h]`，减一下得到 `vec4(x, y, w, h)`）：

```glsl
uniform vec4 sprite_uvs;   // [u0, v0, du, dv]

vec2 texcoord_normalize(vec2 coord, vec4 uvs) {
    return (coord - uvs.xy) / uvs.zw;   // 从 atlas UV 到 [0, 1]
}

vec2 texcoord_unnormalize(vec2 coord, vec4 uvs) {
    return coord * uvs.zw + uvs.xy;     // 回到 atlas UV
}
```

这一对互逆函数建立了 **sprite-local UV ↔ atlas UV** 的双向映射。本质上就是一次仿射变换（平移 + 缩放），参数由 CPU 传入。所有需要「0–1」语义的 shader 逻辑——翻转、旋转、波浪、[[uv-displacement-image-effect|displacement]]、[[texture-dissolve|dissolve]]——都在 sprite-local 空间里做，最后 `unnormalize` 回去再采样。

例如把 sprite 翻转：

```glsl
vec2 local = texcoord_normalize(v_vTexcoord, sprite_uvs);
vec2 flipped = 1.0 - local;
vec2 atlas_uv = texcoord_unnormalize(flipped, sprite_uvs);
vec4 col = texture2D(gm_BaseTexture, atlas_uv);
```

关键一步是**最后的 `unnormalize`**——`texture2D` 必须用 atlas UV，因为 `gm_BaseTexture` 本身就是整张 atlas。

## 跨 sprite 映射：一次归一化 + 一次反归一化

现在考虑更有意思的情形：diffuse 和 AO / normal map 是两个独立 sprite，但都在同一张 atlas 上（这对 batching 很重要）。**采样点在 diffuse 的 `v_vTexcoord`**，我们想同时拿到两张的对应纹素。

一个优雅的观察：**把 diffuse 的 atlas UV 归一化到 [0,1]，就等于得到了「sprite 内部的相对位置」**——这个相对位置对 AO 贴图同样有意义（假设两者物理对齐）。所以只要**用 AO 贴图的矩形把 local UV 反归一化**：

```glsl
vec2 local = texcoord_normalize(v_vTexcoord, diffuse_uvs);
vec2 ao_uv = texcoord_unnormalize(local, ao_uvs);
vec4 diffuse = texture2D(gm_BaseTexture, v_vTexcoord);
vec4 ao = texture2D(gm_BaseTexture, ao_uv);
```

两张贴图都在同一个 `gm_BaseTexture`（同一张 atlas）上，就能通过一次 sampler 完成——这对 normal mapping、splat map、mask blending 等都是基础套路。

## 为什么 ShaderToy 移植经常卡在这里

[[shadertoy-basics|ShaderToy]] 上的 shader 默认假设每个 sampler 是完整一张独立的贴图，UV 铺满 0–1。当你把它移植到 GM 这种 atlas 引擎里，原 shader 的 `texture2D(iChannel0, uv)` 直接失效——`uv` 在 atlas 里会落到别的 sprite。两种解法：

- **强制 separate page**（GM 的「Separate Texture Page」选项）让这张 sprite 独占一页，恢复 0–1 UV。简单但牺牲 batching。
- **用上面的 normalize/unnormalize 套路**显式转换。保持 batching，shader 里多一次仿射运算。

Xor 的下一篇教程（[[shadertoy-basics]]）直接明说：ShaderToy 移植的前提就是「每张贴图单独 page」——否则就得回到本页讲的手工归一化。

## 和其它 UV 技巧的关系

- [[texel-pixel-conversion]] —— 用 `1.0 / textureSize` 把 UV 和像素网格对齐，是更底层的单位换算。
- [[uv-manipulation-nodes]] —— Unity Shader Graph 里的 UV 操作节点，本质上都是仿射 + 非线性组合。
- [[planar-mapping]] —— 从世界坐标构造 UV 的另一条路，主要用于 terrain 和 [[triplanar-mapping|triplanar]]。
- [[sampler-filter-wrap-modes]] —— wrap 模式在 atlas 里失效的原因。

## 相关

- [[texel-pixel-conversion]]
- [[shadertoy-basics]]
- [[uv-manipulation-nodes]]
- [[uv-displacement-image-effect]]
- [[planar-mapping]]
- [[sampler-filter-wrap-modes]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-two-textures]]
