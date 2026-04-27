---
tags: [字体渲染, sdf, distance-field, 工具链, bitsquid]
date: 2026-04-19
sources: 1
---

# SDF 字体图集渲染（Valve / AngelCode 风格）

2007 年 Valve（Chris Green）在 SIGGRAPH 上提出了"Alpha-Tested Magnification for Vector Textures and Special Effects"——把字形烘成**distance field 贴图**，然后在 shader 里用一个 alpha test（或带抗锯齿的 smoothstep）决定像素是否在字内。优点是：**一张小贴图就能以任意大小清晰绘字**，比 bitmap font 上采样质量好得多，比 Bézier 直接光栅（比如 [[slug-gpu-glyph-rendering|Slug]]）简单得多。

[[niklas-frykholm|Niklas Frykholm]] 2010 年这篇是把 Valve 的思路装在一个生产流水线里：他没找到好工具，就自己写了一个 C# 工具，把 **AngelCode BMFont** 生成的位图字体转成 SDF 图集。

## BMFont + SDF 的管线

[AngelCode BMFont](http://www.angelcode.com/products/bmfont/) 是 Windows 上轻量的 bitmap font 工具，导出 `.fnt`（字形位置 / 大小 / kerning）+ `.tga`（atlas 图）。Bitsquid 的管线是：

1. 在 BMFont 里以**目标尺寸的 8 倍**生成位图 + atlas——比如最终要 32 px 字体，就先烘 256 px 的；
2. 字形周围**预留 `8 × spread` 像素的 padding**，否则相邻字形的 distance field 会互相污染；
3. 跑 Frykholm 的工具：读大图，按指定 scale factor 缩小，同时用**数像素**的方式估算每个像素到轮廓的距离，输出新 `.tga` + 新 `.fnt`，所有度量都映射到缩小后的坐标；
4. `spread` 参数决定 distance field 在轮廓**外侧**延伸多少像素才被 clamp 到 0——需要做 glow 之类效果时这段延伸是必需的。

**为什么要从大 8 倍的位图算距离**：distance 是靠数像素估的，source 越大，估计越准、粒度越细。不从 vector 直接算是工具简单的代价。

## 为什么有 `spread` 一说

runtime shader 通常以 "threshold = 0.5" 判定像素在不在字内，小于 0.5 视为字外；spread 决定了"**小于 0.5 到多远才归零**"——这段线性区间既是抗锯齿的过渡带，也是可以**二次利用成外发光 / 外描边**的区域（取一个更高的 threshold 就画出 outer glow）。

## TrueType hinting 的损失

评论里作者自己指出一个坑：**这条管线丢 TrueType hinting**——因为 hinting 是字号敏感的，缩放之后原本 hinting 对齐的笔画会被破坏。所以：

- 小号字用位图实际尺寸直接渲（有 hinting，笔画干净）；
- 需要"任意缩放"再用 SDF 版本——接受一点细节丢失，换缩放下的高质量。

## 中文字体的现实

另一个评论者抛出了生产环境里的难题：**整套 Unicode 中文字形 × 大号尺寸 = 贴图爆炸**。他们当时用 2 张 1024×32 纹理覆盖全字集，做 HUD 还能扛；再加几个大尺寸就撑不住。Frykholm 的回答是"**要维持最低分辨率**——如果笔画本身已经糊成一团，SDF 无法还原"。复杂中文字形若用太小的 source 烘，笔画间 distance field 已经互相消化，运行时怎么放大都回不来。后续业界的补丁办法（本文没谈）一般是 **multi-channel SDF（MSDF）**、或者**只为需要的字型 runtime 生成 SDF**。

## Valve / AngelCode 路线的历史位置

| 路线 | 特征 | 代价 |
|------|------|------|
| Bitmap font | 像素完美，带 hinting | 只在烘焙尺寸附近清晰 |
| 单通道 SDF（本篇） | 一张小图覆盖各种尺寸 | 尖角会变圆，丢 hinting |
| Multi-channel SDF | 多通道保尖角 | 烘焙工具更复杂 |
| GPU 直接光栅 Bézier（[[slug-gpu-glyph-rendering|Slug]]） | 任意变换 pixel-perfect | 实现复杂，历史上有专利 |

Bitsquid 这篇开源工具在后续很长一段时间里是小引擎 / 独立游戏做字体的默认起点。

## Sources

- [[sources/bitsquid-distance-field-angelcode-fonts]]
- [[sources/c0de517e-sdf-antialiasing]] —— Pesce 2012：4-tap marching squares 凸多边形面积 = SDF coverage 精确算法
