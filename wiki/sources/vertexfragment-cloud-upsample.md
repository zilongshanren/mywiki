---
tags: [source, rendering, volumetric-clouds, temporal-reprojection, unity, urp]
date: 2026-04-19
sources: 1
---

# Upsampling to Improve Volumetric Cloud Render Performance（Steven Sell / Vertex Fragment）

[[steven-sell]] 2024 年 3 月的 ramble，坦诚记录他误读了六年《Real-Time Volumetric Cloudscapes of Horizon Zero Dawn》里"每帧更新 1/16 像素"这句话，直到翻到 Schneider & Vos 论文才恍然大悟：那不是在 full-res 里跳过 15/16 像素，而是**渲染到 1/16 面积的 quarter buffer 再靠时间重投影补齐**。

## 摘要

作者第一次实现时照字面把 fragment shader 改成 `[branch]` 里每 16 个只做 1 个的形式，结果性能没有任何提升——因为 GPU 的 wave/wavefront 宽度是 16/32/64，哪怕只有一个 fragment 要执行，其余 lane 也在分支处陪跑直到 wave 退役。正解是把 raymarch 画到 quarter buffer（1/4 宽 × 1/4 高 = 1/16 像素），fragment 总量直接砍到 1/16，然后**每帧给 ray direction 的 UV 施加一个 jitter 偏移**，让 16 帧累积下来正好覆盖 4×4 block 中的 16 个位置。Upsample 是双缓冲：`FullPrev` 保留历史、`Quarter` 是本帧新渲的低分辨率；per-pixel 用一个 `JitterCorrection(uv)` 判定"这个 full-res 像素是不是本帧 jitter 选中的那个"，是则用 curr、否则用 prev。再叠一层 **convergence speed**（天顶快、地平线慢，或用 depth 权重），让近距离云优先收敛。作者最后感慨："原文根本没提 jitter"。

## 关键要点

- 误读陷阱：`if ((cx == fx) && (cy == fy))` 式的稀疏 execute 不省 wave 时间、不省带宽、还破坏 2×2 quad 调度。
- 需要 3 张 buffer：quarter raymarch 目标 + full-res double buffer（history）。
- Jitter 必须**除以 full-res** 而不是 quarter-res——几何上是 full-res 像素偏移，误用 quarter 会让连续帧跳 4 格。
- JitterCorrection：`floor(fmod(uv*fullRes, 4))` → 减 jitter → saturate 求和，返回 0/1 选择 curr 或 prev。
- 不要在本 pass 里 Clear back buffer——同一帧会被阴影图 / 反射探针等外部消费者读取，容易读到清空后的数据。

## 链接到的概念

- [[volumetric-cloud-quarter-res-upsample]]
- [[temporal-antialiasing]]
- [[temporal-supersampling]]
- [[depth-aware-upsampling]]
- [[volumetric-raymarching-intro]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/volumetric-cloud-upsampling/
- 本地：`raw/articles/vertexfragment.com/2024-03-20_upsampling-to-improve-volumetric-cloud-render-performance.md`
