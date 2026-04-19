---
tags: [rendering, post-processing, ascii, stylized, atlas, retro]
date: 2026-04-19
sources: 1
---

# ASCII 终端后处理（Text Adventure Post-Process）

把屏幕当成字符终端：按固定大小把画面切成 cells，**每个 cell 用亮度索引一张字符图集**，查出最接近该亮度的字符贴回屏幕。最终图像看起来就像一块 ASCII 文字墙，亮的像素变成 `#`、`@` 之类笔画密集的字符，暗的像素变成 `.`、` `。Snapshot Shaders Pro 的 Text Adventure 效果是这一思路的产品化封装。

## 字符图集与亮度映射

核心数据结构是一张 **Character Atlas**：`(n·x, y)` 的纹理，里面横向排列 `n` 个字符，每个字符尺寸 `x × y`。字符**必须按亮度升序排列**——即 `index 0` 是最暗的（通常空格），`index n-1` 是最密的（`#` 或 `█`）——这样才能直接用 `int(lum * n)` 做索引。参数：

- `Character Size` —— cell 的屏幕像素大小（`x × y`）
- `Character Atlas` —— 上面那张图
- `Character Count` —— `n`（图集有多少字符）
- `Background Color` / `Character Color` —— 最终输出 `lerp(bg, fg, atlasSample)`，把单色字符染上用户指定的前景色 / 背景色

## Fragment shader 的两步 UV

```hlsl
// 1) 把屏幕切成 cell，找到当前像素所在 cell 的"代表亮度"
float2 cellIdx = floor(i.uv * _ScreenParams.xy / charSize);
float2 cellUV  = cellIdx * charSize / _ScreenParams.xy + 0.5 * charSize/_ScreenParams;
float  lum     = Luminance(tex2D(_MainTex, cellUV));

// 2) 按亮度选字符，在 cell 内采样该字符
int    charId = clamp((int)(lum * charCount), 0, charCount - 1);
float2 subUV  = frac(i.uv * _ScreenParams.xy / charSize);   // cell 内 0..1
float2 atlasUV = float2((charId + subUV.x) / charCount, subUV.y);
float4 ch     = tex2D(_CharAtlas, atlasUV);

return lerp(_Background, _Character, ch.r);
```

第一步把屏幕降到"cell 分辨率"采一次亮度、第二步在同一个 cell 内取字符图集的相应切片。分辨率牺牲全在第一步——cell 越大越 ASCII，cell 越小越接近原图。

## 亮度的选择与调色

`lum = dot(rgb, (0.299, 0.587, 0.114))` 是最常见的取法（Rec.601）；也可以用 luma 近似 `(0.3, 0.59, 0.11)`（见 [[color-quantization-retro|Game Boy 量化]]里同一个系数）。字符图集如果本身不是纯灰度，还需要 `Luminance(ch.rgb)` 再 lerp，避免字符颜色本身污染结果。

## 陷阱与变体

- **图集必须严格按亮度排**：排错了会出现"高亮处突然变空格"的跳变；这是出现视觉 bug 时第一排查点
- **Character Size 不整除屏幕**：cell 在边缘会被截断，观感是屏幕右/下有半格残影；Pro 版似乎不处理，自行调整分辨率是最简单的解
- **Point sampler 必须**：atlas 用 bilinear 会把字符边糊成渐变，ASCII 的硬边感全丢——和 [[color-quantization-retro|像素化下采样]]一样的 FilterMode.Point 约束
- **色彩版 vs 单色版**：Pro 版只有 fg/bg 单色；想做"每个字符保留原场景色"的变体，把 `_Character` 换成原像素色即可，一行改动

## 相关

- [[color-quantization-retro]] —— 同家族的"牺牲细节换风格"后处理，同样靠 atlas / 离散映射
- [[image-convolution-kernel]] —— ASCII 的 cell 平均其实是 box filter 的极端
- [[crt-shader-effects]] —— ASCII + CRT 扫描线的组合是"80 年代终端"视觉
- [[urp-volume-post-processing]]

## Sources

- [[sources/danielilett-snapshot-pro-text-adventure]]
