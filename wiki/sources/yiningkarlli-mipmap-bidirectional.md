---
tags: [source, 渲染, 路径追踪, mipmap, ray-differentials, bidirectional, takua]
date: 2026-04-19
sources: 1
---

# Mipmapping with Bidirectional Techniques（Yining Karl Li / Code & Visuals）

[[yining-karl-li]] 2018 年 10 月在个人 hobby renderer **Takua Renderer** 上为实现 tiled/mipmapped 纹理缓存而写的长文——专门讨论「双向路径追踪下 mip level 到底怎么选」这个业内半开放的问题，并介绍他最后落地的 camera-based 方案。

## 摘要

文章先回顾 mipmap 的必要性和光栅化里用屏幕空间导数选 LOD 的做法，然后把重点落到路径追踪：[[ray-differentials]]（Igehy 1999）为相机 ray 提供了屏幕空间导数的代用品，是当今 PBRT / Mitsuba / Arnold / RenderMan / Hyperion / Manuka 都在用的核心机制。关键难题是**双向路径追踪（BDPT / photon mapping / VCM）**：光路径的最后一条 ray 才碰相机，在 path 完整构造前根本没有「屏幕空间 footprint」可供定义 ray differential；绝大多数生产渲染器对光路径干脆不算，退回 level 0 点采样，纹理缓存瞬间失效。Weta Manuka 的 **shade-before-hit** 架构天然回避这个问题（path sampling 时已经没有 texture lookup）；Yining 不愿改 Takua 的架构，设计出只依赖「世界空间到相机距离」的 camera-based mip level selection——BDPT 的 tile 访问率从 27.3% 降到 14.1%，接近 unidir 水准。

## 关键要点

- **Igehy 1999 ray differentials** 是相机 ray 的标准方案：每条 ray 携带「相对屏幕像素」的方向偏导，在命中点求切平面交，反解 `dudx/dvdx/dudy/dvdy`。Takua 实现里把 differential surface 和 screen space differential 都延迟到 texture lookup 时才算（而非每次 intersection），并在一次 shader invocation 内缓存。
- **二级 ray 的启发式百花齐放**：Igehy 只严格处理镜面/折射；glossy/diffuse 必须用 ad-hoc 展宽。SPI Arnold 跟踪累计粗糙度一到阈值直接跳最高 MIP（配 OSL 上的 dual arithmetic 自动微分，Kulla et al. 2018）；RenderMan 只用两个 float（origin width + unit spread）表示 ray differential（Christensen et al. 2018）；[[hyperion-renderer]] 用类似的简化；Weta Manuka 用 unified roughness / mean cosine 估计（Fascione et al. 2018）。Matt Pharr PBRTv3 实验分支里「diffuse 用 hemisphere 1/25、glossy 用 1/100」就够用。
- **Path differentials**（Suykens & Willems 2001）理论通用但复杂度路径长度平方增长，没人用。**Covariance tracing**（Belcour et al. 2013 / 2017）线性复杂度、可从光源端出发算 filter footprint，是最有希望的未来方向。
- **BDPT 的结构性难题**：ray differential 定义要求「相对屏幕像素」，而光路径在完整构造前不知道会连到哪个像素。更糟的是，光路径的 footprint 宽度不能随便扩宽，因为它随时可能连向相机。Belcour et al. 2017 证明两端 texture filtering 一致性对 BDPT unbiasedness 很关键。
- **Shade-before-hit（Manuka）的启示**：启动时把几何细分成 micropolygon grid，跑 pattern generation，BSDF 参数烘进顶点——path sampling 时不再有 texture lookup，BDPT mip level 问题自然消失。代价：启动时间长、camera 前放大透镜场景会失效。
- **Takua 的 camera-based 方案**：启动时求相机所有像素里「最窄」的 ray differential；每次命中用这条最窄 differential 构造一条从 camera origin 到命中点的「假 ray」求 dudx/dvdy。所有 path（包括光路径）mip level 仅由空间位置决定，BDPT 两端天然一致。
- **实测**（forest 场景，1920×1080、16 spp，745k tiles）：

  | 方案 | unidir | bdpt |
  |---|---|---|
  | 无 mipmap | 42.18% | 42.32% |
  | Ray-based 启发式 | 13.84% | 27.30% |
  | **Camera-based (Takua)** | 14.05% | **14.07%** |

- Takua 只做 point sampling、不做 bilinear filtering，靠 path tracer 自带 supersampling 兜底抗锯齿——[[ptex-gpu-streaming]] 等生产场景的独立结论一致（Moonray 的 Lee et al. 2017 也是）。
- **已知失效**：相机前放大透镜，与 shade-before-hit 的失效场景同源。Yining 设想的补救是开头用传统 ray differential 对镜面物体做一轮 mip level 缓存，渲染时对最近 N 个缓存比对修正——但尚未实现。
- 作者明确表态，长远看 covariance tracing 是更 principled 的方向，特别是 glinty microfacet 等对 filtering 敏感的场景。

## 链接到的概念

- [[ray-differentials]]
- [[mipmap-generation-sampling]]
- [[hyperion-renderer]]
- [[wavefront-path-tracing]]
- [[ptex-gpu-streaming]]
- [[yining-karl-li]]

## 原文

- 链接：<https://blog.yiningkarlli.com/2018/10/bidirectional-mipmap.html>
- 本地：`raw/articles/blog.yiningkarlli.com/2018-10-25_mipmapping-with-bidirectional-techniques.md`
