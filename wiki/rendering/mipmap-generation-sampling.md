---
tags: [渲染, 纹理, mipmap, lod, 过滤, 抗锯齿]
date: 2026-04-14
sources: 1
---

# Mipmap 生成与采样

**Mipmap** 是一组预生成的、按 2× 递减分辨率的纹理金字塔：512×512 的 LOD 0、256×256 的 LOD 1、128×128 的 LOD 2……一路缩到 1×1。这一整叠加起来多出 1/3 的存储，但换来两件事——**远处或缩小的纹理采样看起来不再闪烁**，以及**带宽更友好**（GPU 采样金字塔高层时局部性更好）。[[xor-shader-artist|Xor]] 在 GM Shaders 的 mipmap 短文里不仅讲了怎么开，还展示了如何用 mipmap 的 **bias 参数**把它挪用成一个接近免费的模糊/景深原语。

## 为什么需要 mipmap

没有 mipmap 时，一个远距离的 3D 物体或极度缩小的 sprite 会让每个屏幕像素对应多个 texel——GPU 只能从原图里抓一个点，剩下的直接丢弃。结果就是经典的 **[[mipmap-moire-scanline|moiré 条纹]]** 和闪烁：采样的高频成分在子像素层面做相干叠加，肉眼看见的是游动的干涉纹路。这是一种标准的 aliasing，只是发生在纹理坐标的频域里。

Mipmap 的做法是**预先把高频滤掉**：LOD 1 是 LOD 0 四个 texel 的平均，高频已经被提前合成掉；当采样点的屏幕密度变稀时，GPU 选用更高的 LOD，等价于在原纹理上做一个已经 box-filter 过的平均。这是一个**离线完成的空间降采样**，不需要在 shader 里花功夫。

## GPU 如何选 LOD：屏幕导数

GPU 在后台给每个片元算纹理坐标的屏幕空间导数 `dFdx(uv)` 和 `dFdy(uv)`，乘以纹理分辨率就得到**一个像素内覆盖了多少个 texel**。取两个导数长度的最大值 `md`，LOD = `log2(md)`（写成平方版本就是 `log2(md²) * 0.5`）：

```glsl
vec2 dx = dFdx(v_vTexcoord) * tex_res;
vec2 dy = dFdy(v_vTexcoord) * tex_res;
float md = max(dot(dx,dx), dot(dy,dy));
float lod = log2(md) * 0.5;
```

这就是**等向（isotropic）过滤**的内部机制。结果通常是一个浮点 LOD，例如 0.5 表示在 LOD 0 和 LOD 1 之间各取一半做 trilinear 混合。**各向异性过滤**（[[sampler-filter-wrap-modes|anisotropic]]）则允许 x/y 方向独立采样多层，代价是更多 VRAM 和更复杂的采样流水线，但能保住斜视角下的清晰度。三档最常用的是 `tf_point`、`tf_linear`、`tf_anisotropic`，默认建议 linear。

**陷阱**：因为导数是按 **2×2 pixel quad** 计算的，任何 `uv = fract(uv)` 这种不连续操作都会让 quad 内部两边的 UV 跳变，进而让 GPU 误以为「这里纹理巨大」，瞬间降到最粗的 LOD——视觉上就是 UV tile 缝隙处出现一圈糊带。解决办法是**优先 `gpu_set_texrepeat(true)` 或等价的 wrap mode**，让硬件负责 wrap 而不是自己在 shader 里 fract。

## Bias：把 mipmap 当廉价模糊

`texture2D(sampler, uv, bias)` 的第三个参数会**加到系统算出的 LOD 上**。正 bias 强制采样更粗的 LOD，视觉效果接近一次 box blur；这让你能在**零额外采样成本**下拿到「半分辨率看这张图」「每像素 4 texel 的糊」的效果。常见创意用法：

- **伪景深**：按片元到焦点的距离做 bias 插值，远离焦点的像素自然糊掉；[Shadertoy 上有现成 demo](https://www.shadertoy.com/view/ws3cDj) 在单 pass 里模拟 DOF。
- **软阴影 / 光晕**：把辉光贴图用一个大 bias 采样一次，就是廉价 glow。
- **和真正的 blur 组合**：先用 mipmap bias 拿到预模糊，再叠一层小半径 [[separable-gaussian-blur]]，花极少预算做出大半径效果——[Dual-Kawase](https://github.com/XorDev/Dual-Kawase/wiki) 就是这一哲学的工业化延伸。

`texture2DLod(sampler, uv, lod)` 可以**绕过系统导数**直接指定 LOD，代价是得自己算 `lod` 并接管 wrap/filter 行为（GameMaker 的 GLSL 1.00 不支持这个函数，但可以用 bias 等价替代）。

## 代价与限制

- **存储代价**：等向过滤多 33% VRAM，各向异性多 4 倍。对全尺寸纹理库而言绝不是小数。
- **尺寸要求**：严格的 POT（2 的幂次方）方块纹理最友好；非方形或非 POT 会被自动 padding。对 sprite 尤其要留边，避免模糊时采到邻居的透明区域变脏。
- **surface / render texture 常不支持 mipmap**：GameMaker、以及许多自渲染管线的临时 surface 没有 mipmap 级别，这也是「用 mipmap 做 bloom」在 GM 里至今做不到的原因。现代引擎通常靠 `glGenerateMipmap` 或 `vkCmdBlitImage` 手动生成。
- **不连续 UV 会破坏 LOD 选择**：fract、floor 或任何基于条件分支的 UV 技巧都可能在 mipmap 环境里产生接缝，Ben Golus 的 [Distinctive Derivative Differences](https://bgolus.medium.com/distinctive-derivative-differences-cce38d36797b) 是这类陷阱最全面的参考。

## 相关

- [[mipmap-moire-scanline]] —— 故意不用 mipmap 以换取一种视觉风格
- [[aliasing]]
- [[sampler-filter-wrap-modes]]
- [[image-resampling-filters]]
- [[separable-gaussian-blur]] —— mipmap 的 bias 技巧是对它的廉价替代
- [[bloom-threshold-blur-composite]]
- [[laplacian-pyramid]] —— 金字塔思想的一般化
- [[dynamic-resolution-scaling]]
- [[scatter-bokeh-dof]]
- [[texel-pixel-conversion]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-mipmaps]]
