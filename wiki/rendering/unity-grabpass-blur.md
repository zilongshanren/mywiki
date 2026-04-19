---
tags: [unity, shader, 后处理, blur, 透明物体]
date: 2026-04-14
sources: 2
---

# Unity GrabPass + 可分高斯模糊

Unity 的 `GrabPass` 是一个"把当前帧 backbuffer 里这个物体背后的像素抓成一张纹理"的内置机制，常用来实现**折射、毛玻璃、热浪、雾气窗户**等**需要读取背景**的透明物体 shader。Linden Reid 的 *Foggy Window Shader* 用它加一个可分离 Gaussian blur 做出"雾化窗户"效果。

## GrabPass 的机制

在 SubShader 块里声明：

```
Tags { "Queue" = "Transparent" }
GrabPass { "_BGTex" }
```

Unity 会在绘制该物体之前，**把已经绘制到 backbuffer 的所有东西拷贝到名为 `_BGTex` 的纹理**，然后把这张纹理作为 `sampler2D` 传给后续 pass 使用。代价是一次全屏拷贝，所以 GrabPass 物体越多越慢——这是它在现代 URP/HDRP 里被 `CopyColor` + `_CameraOpaqueTexture` 取代的根本原因。

读取时需要正确的屏幕空间 UV：Unity 提供 `ComputeGrabScreenPos(clipPos)` 把 clip-space 位置转成 GrabPass 的采样坐标（处理了 Y 翻转和 perspective divide）。

## 可分离高斯模糊的代价

标准 2D Gaussian kernel 是 `O(n²)`，但因为高斯核可分离，可以拆成**先横向一维卷积，再纵向一维卷积**，降到 `O(2n)`。这是现代 blur 的默认做法，Ronja 等其他 Unity 教程作者也都这么教。

**正确做法**是两 pass：

1. 横向 blur → 写入中间 RT
2. 以中间 RT 为输入做纵向 blur → 写入最终结果

Reid 的教程承认自己用了"懒汉实现"——在**同一 pass** 里对原图分别做横向和纵向 blur，然后相加。这保持了单 pass 的简单性，代价是：

1. 没有真正卷积两次，模糊质量低；
2. 两个单向结果相加导致亮度翻倍，必须靠乘 tint 色拉回来。

这是新手教程里常见的折衷：为了把教程焦点留给**交互驱动的 blur 强度变化**，把 blur 本身做"够用就行"。

## 与相关技术的对比

- **URP/HDRP 的 `_CameraOpaqueTexture`**：内置的全屏 opaque 纹理拷贝，功能等价于 GrabPass 但生命周期由 SRP 显式管理。
- **[[laplacian-pyramid|高斯金字塔]]** / Mip chain：需要多尺度模糊时更经济的做法，但 foggy window 这种"单一强度"场景用不上。
- **[[image-resampling-filters|Kawase blur]]**：大 kernel 的更快近似，代价是质量略差。
- **[[depth-aware-upsampling|bilateral blur]]**：想让模糊不跨越深度/法线边界时用。

## 相关

- [[fragment-shader]]
- [[alpha-blending]]
- [[image-resampling-filters]]
- [[laplacian-pyramid]]
- [[texture-encoded-state]] —— 同一篇教程的第二部分：用纹理编码 mouse + 时间驱动 blur 强度
- [[linden-reid]]
- [[harry-alisavakis]] —— *My take on shaders* 第五篇用 GrabPass 把任何 image effect 移植成「物体绑定式后处理」
- [[uv-displacement-image-effect]] —— 把同样的 displacement 套到 GrabPass 纹理上即得折射 / 玻璃 / 热浪
- [[refractive-glass-shader]] —— URP 下折射通过 `_CameraOpaqueTexture` 读取背景，Shader Toolbox 额外提供 `_CameraTransparentTexture` 让透明物体之间也能互相折射
- [[iridescent-bubble-shader]] —— 同一套 camera texture 机制，叠 Fresnel + color ramp 做彩虹肥皂泡

## Sources

- [[sources/lindenreid-foggy-window-shader]]
- [[sources/halisavakis-image-effects-grabpass]]
