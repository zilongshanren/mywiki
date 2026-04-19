---
tags: [source, shader, 复古, ps1, n64, vhs, crt, urp, unity, 作者自述]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro — A Technical Breakdown（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2026 年 1 月写的 *Retro Shaders Pro* **devlog / 作者自述**——和之前的参数手册系列（[[sources/danielilett-retro-urp-retro-lit]] 等）不同，这篇讲**每个 feature 在 shader 里是怎么实现的、为什么这样设计、踩过哪些坑**。长达数千字，是目前 wiki 里关于 PSX/N64 风格 shader 最详细的实现揭秘。

## 摘要

作者把 asset 的**核心约束**定在"URP only"——之前做 *Snapshot Shaders Pro* 跨管线支持让他对 multi-pipeline 产生了 PTSD。Retro Shaders Pro 的两大支柱：*Retro Lit* 核心 object shader 和 *CRT post process*。文章分两段：**PSX 技术特征**（vertex snap / affine texture / 色深 / 光照 / cubemap / dither / terrain / skybox / decal / outline）和 **CRT post 效果**（降分辨率 / interlaced scan / subpixel + scanline 纹理 / VHS tracking / 复古色板 filter）。最后一段谈 Unity Asset Store 发布踩坑——命名权冲突（PSX 被认为可能侵权）、差评渠道问题。技术揭秘里的新信息：

## 关键要点

### PSX 技术特征的 shader 实现

- **Vertex snap**：`round(pos * snapsPerMeter) / snapsPerMeter`，空间可选 view/world/object；default view space。
- **Affine texture warping**（PS1 不做透视校正 UV 插值）：HLSL 有 `noperspective` 关键字跳过插值前的 `/w`——但 Ilett 用的是手动实现（undo perspective in fragment），因为要让 affine ↔ perspective 平滑可调。
- **分辨率上限**：用 `SAMPLE_TEXTURE2D_LOD` 强制采到指定 mip level——log2(原尺寸) - log2(上限) = LOD 偏移。讽刺点：为模拟"低 VRAM"反而多占 33% 的 mip chain 内存。
- **N64 3-point bilinear**：单独的滤波模式，接三个 texel 混而非四个；v1.5 合并进 Retro Lit 的参数。
- **色深限制 + 动态 offset**：`floor(col * depth + offset) / depth`，offset 默认 0.5 补偿量化导致的整体变暗。
- **Flat shading 晚到**：最初没做，itch.io 用户提 request 后加了 toggle。
- **Texel-aligned lighting**：基于 `ddx/ddy` 把 pixel 位置"吸附"到 texel 中心再算光照——思路来自 Unity 社区的 GreatestBear 帖子，Ilett 特意标注来源（因为 asset pack 圈存在不署名复制问题）。
- **Dither 双模式**：texel-space（贴 texture）或 screen-space（贴屏幕 chunky pixel）。screen mode 需要读 CRT post 的 pixel 大小——用 global shader variable 传递，作者承认"有点偷懒"。
- **Terrain 专版妥协**：舍弃 affine warping（terrain 已自动细分三角形缓解）；resolution cap 和 texel lit 固定用第一张 splat 的 texel size；interpolator 用到 13/15 个（shader model 3.5 上限）。
- **Skybox 合并**：原本分 cubemap 和程序云两个 shader，v1.5 合一；cubemap / gradient / procedural clouds 三种组合。
- **Inverted hull outline**：`_OutlineSize` 沿法线外推，叠一层 vertex snap 让描边也抖动；作者说这更像 PS2 而非 PS1 风。

### CRT post 的实现

- **降分辨率 → 升采样**：用 point 或 bilinear 滤波。
- **Interlaced scan**：保留上一帧 buffer，每帧只渲染奇数或偶数扫描行。
- **Subpixel + scanline 纹理**：用户提供两张纹理，shader 按"一个 chunky pixel = N × M 个 screen pixel"分割 RGB 子像素 + 扫描线间隙；与 URP Bloom 叠能做到亮处 RGB 混合模糊。
- **CRT Mesh shader**：把同样的效果暴露成普通 unlit shader，可用在场景里的电视屏幕物体上。
- **VHS tracking**：屏幕坐标 hash 出伪随机，做条带扭曲 + 色偏 + fuzz；参数暴露但作者承认精度取决于 VCR 型号，没完全重现。
- **复古色板 filter**：14 种近似调色板（Game Boy / GBA / NES / SNES / MSX2 / ZX Spectrum / Sega Master / Genesis / Game Gear 等 + 灰度），NES 只做 27 色近似（真实 PPU 是 54 基色 + 3 个 emphasis bit = 448），SNES 只做 15-bit 调色板不做"同屏 256 色"约束（实时选色算法代价不划算）。讽刺点：**作者漏掉了 PS1 本身**——和 SNES 一样是 15-bit 色板。

### 发布踩坑

- 原名 *PSX Shaders Pro* 被 Asset Store 拒（PSX 可能侵权），被迫改名 Retro Shaders Pro——但 itch.io 版 URL 仍保留旧名，且 Asset Store 上有大量 late-comer 包直接叫 PSX 不做 trademark 检查。作者情绪外溢但承认改名反而让 asset 扩展到 N64/VHS 成为可能。
- 差评机制：Asset Store 不通知作者收到 review，bug 常通过差评先被发现。作者建议用户用邮件走 support，而非靠差评发泄。

### 其他

- **自定义 editor GUI**：Unity editor scripting 可做参数条件隐藏、自动修复按钮、deprecated shader 升级 button——v1.5 把 Retro Lit/Vertex Lit/Unlit 合一后，editor 提供 one-click 转换。

## 链接到的概念

- [[retro-rendering-techniques]]
- [[crt-shader-effects]]
- [[dither-alpha-clipping]]
- [[color-quantization-retro]]
- [[procedural-retro-skybox]]
- [[noperspective-affine-texture]]
- [[cel-shader-outline]]

## 原文

- 链接：<https://danielilett.com/2026-01-27-article-retro-1-5-1-update/>
- 本地：`raw/articles/danielilett.com/2026-01-27_retro-shaders-pro-a-technical-breakdown.md`
