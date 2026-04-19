---
tags: [渲染, 颜色, gamma, srgb, shader]
date: 2026-04-19
sources: 1
---

# Shader 里的 Gamma 校正与 sRGB 编解码

Xor 的 *Gamma* 教程用一页把 shader 人员需要掌握的 gamma 常识压缩完毕：**图像存储是 sRGB，光照计算必须在 linear**。这不是性能问题也不是艺术问题——是**数学正确性**问题。把 sRGB 像素值相加混合，等同于在非线性曲线上做加法，结果是中间色的错误变暗和色相偏移。

## 为什么要 gamma

CRT 年代的物理偶然：阴极射线管的输入电压到输出亮度之间是 γ≈2.2 的幂函数关系。工程师发现这个非线性**恰好和人眼感知对齐**——人眼对暗部敏感、亮部不敏感，用 γ=2.2 编码等于在暗部分配更多 code points。sRGB 格式保留了这个特性：8-bit PNG 里的 128 不是「一半亮度」，而是「一半感知亮度」，实际光强只有约 0.22。

相机传感器采集的是线性光子数，但**存储前要 encode 成 sRGB**——否则深色区域色带严重。读出来做任何数学运算之前必须 **decode 回 linear**，否则你在和一堆扭曲过的值做加减。

## 最小实现（γ=2.2 近似）

```glsl
#define GAMMA 2.2
vec3 gamma_decode(vec3 srgb) { return pow(srgb, vec3(GAMMA)); }
vec3 gamma_encode(vec3 lrgb) { return pow(lrgb, vec3(1.0 / GAMMA)); }
```

两点光源相加的对比：sRGB 直接相加会让重叠区域「过曝成脏橙色」；decode → 相加 → encode 得到干净的叠加，边界平滑、颜色准确。所有 [[alpha-blending]]、[[separable-gaussian-blur|blur]]、[[bloom-threshold-blur-composite|bloom]]、相加型 [[bartwronski-future-of-ssr|光照叠加]] 都必须在 linear 域做——iq 的 gamma 文章有专门演示错误 blur 的后果。

## 精确 sRGB 公式

γ=2.2 只是近似，sRGB 标准实际是分段的：**暗部用线性 slope、亮部用 γ=2.4 偏移幂**，接缝在 `0.0031308` / `0.04045`：

```glsl
vec3 SRGB_decode(vec3 srgb) {
    return mix(
        srgb / 12.92,
        pow((srgb + 0.055) / 1.055, vec3(2.4)),
        step(0.04045, srgb));
}
vec3 SRGB_encode(vec3 lrgb) {
    return mix(
        12.92 * lrgb,
        1.055 * pow(lrgb, vec3(1.0 / 2.4)) - 0.055,
        step(0.0031308, lrgb));
}
```

差异主要在深色与上中段可感知——professional color pipeline 应该用精确版；日常 game shader 用 γ=2.2 够好。

## shader 视角的最佳实践

- **纹理采样要标对 flag**：UI / albedo 贴图标 sRGB，GPU 自动 decode；法线、roughness、AO、mask 纹理必须是 linear 原始值，绝不能经过 sRGB decode。
- **render target 选 linear**：G-Buffer 全用线性格式（RGBA16F 或带硬件 sRGB 的 write flag），avoid 人工 encode/decode 穿插。
- **tonemap 后才 encode**：HDR linear → tonemap → sRGB encode → 提交 swap chain。现代 API（Vulkan / D3D12）把 encode 内建到 swap chain 格式里，shader 写线性值就行。
- **blur / bloom / 加法运算必须 linear**。否则会有 iq 那张「在 sRGB 里 blur 红绿条纹，中间出现暗带」的经典错图。

## 和 [[color-space]] 的区别

[[color-space]] 讲的是**一个完整色彩空间的三要素**：TRC + primaries + white point。这里只关心其中 TRC 那一部分——sRGB 的 gamma 曲线如何在 shader 里编解码。primaries 和白点变换属于 HDR、宽色域和 [[oklab-color-space|感知均匀空间]] 的话题。

## 相关
- [[color-space]]
- [[alpha-blending]]
- [[oklab-color-space]]
- [[separable-gaussian-blur]]
- [[bloom-threshold-blur-composite]]
- [[deferred-rendering]]
- [[display-edid-colorspace]]
- [[shader-instruction-cost]]
- [[xor-shader-artist]]
- [[srgb-premultiplied-alpha-compression]] —— 预乘与块压缩必须发生在 linear 域，sRGB encode 是最后一步

## Sources

- [[sources/xor-mini-gamma]]
