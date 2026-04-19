---
tags: [source, rendering, shader, unity, polar-coordinates]
date: 2026-04-19
sources: 1
---

# Texture Effects with Polar Coordinates（Steven Sell / Vertex Fragment）

[[steven-sell]] 2024 年 2 月在 Vertex Fragment 发的 ramble，讲他在 *Beyond the Storm* 里复刻《荒野之息》脚下水圈时走过的弯路，以及为什么最终解法是极坐标。

## 摘要

作者一开始想靠 SDF 环形 + `sin` 波纹把水圈做出来，得到的效果"不难看但不对"：fade 是均匀的、始终是一个完整环、无法像 BotW 那样随机碎裂。卡了几次之后他想起了 **极坐标**。核心把戏是把 UV 从笛卡尔换到 `(r, θ)`，用 `.yx` 采样一张 tileable 噪声得到一张"从中心扩散的 swirl 噪声"；对 `polar.y`（角度）加时间得到旋转，对 `polar.x`（半径）减时间得到向外扩散。再用原来的 SDF 环做 mask，两者相乘，最后用 `saturate((final - fade01) * strength)` 做 time-based dissolve，环就会在扩散过程中"崩碎"，恰好命中 BotW 的视觉语言。水圈本身很小、截图不好看，作者顺带把这套 polar + noise + SDF 的玩法扩展到了 ShaderToy 风格的演示效果上。

## 关键要点

- **UV → polar**：`length(uv-origin)` 当 r、`atan2(dy, dx)` 当 θ；θ 范围 `[-π, π]`，可按需映射到 `[0, 1]`。作者曾把 `(r, θ)` 和 `(θ, r)` 搞反，得到"好看的错误"——强调约定只要一致就行。
- **为什么极坐标适合"从中心向外"**：在极坐标采样的噪声随 `polar.x`（半径）线性偏移等价于径向流动；θ = 0 处有 discontinuity，旋转 + tileable 能把缝遮住。
- **SDF ring × polar noise**：环形 mask 把连续噪声切成圈，乘法得到"噪声填充的扩散圈"。
- **Time-based dissolve**：`final - fade01` 让最亮的峰值最后消失，避免均匀衰减带来的"心电图感"。
- 极坐标另一用途：把 raymarch 云渲到极坐标参数化的 offscreen texture 再贴到半球 mesh。

## 链接到的概念

- [[polar-coordinate-texture-effects]]
- [[sdf-2d-primitives]]
- [[classic-shader-noise]]
- [[coordinate-spaces]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/polar-coordinates/
- 本地：`raw/articles/vertexfragment.com/2024-02-28_texture-effects-with-polar-coordinates.md`
