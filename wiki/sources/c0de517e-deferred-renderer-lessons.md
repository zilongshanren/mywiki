---
tags: [source, rendering, deferred-rendering, engine, performance]
date: 2026-04-27
sources: 1
---

# What I've Learned from Shipping a Deferred Lighting Renderer（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2011 年 9 月的短文，以 bullet 清单列出实际把一个 deferred lighting renderer 发货后总结的工程经验。

## 摘要

文章以极其精练的形式（约 20 条要点）给出了 deferred lighting 渲染器在生产中的实战教训，覆盖 CPU 瓶颈、缓存 miss、并行渲染、批处理策略、几何管线、遮挡剔除、平台差异等维度。核心结论：**平均每个 mesh 要渲染三次（含阴影），很容易就变成 CPU 瓶颈而非 GPU 瓶颈**；GPU 侧的优化重点则是 tiled lighting 取代 stencil volume。

## 关键要点

- CPU bound 是 deferred 场景的常见瓶颈：三遍 mesh（depth/GBuffer/shadow）叠加 cache miss 效应极为致命
- 避免对 drawable 集合做多次迭代；用固定长度 sort-key（bit-packed draw call descriptor）是作者认可的最佳方案
- 并行 command buffer 生成很重要，若未双缓冲则延迟帧内没有足够任务喂饱多核
- 软件遮挡剔除实现不难且收益显著
- Megatexture（clipmap）在 deferred 里有额外优势：大幅减少 material shader 变体，减少静态 decal 数量
- Tiled lighting 优于 stencil volume，尤其当 lighting stage 需要多 shader 变体时（主机的 1-bit hi-stencil 不够用）
- 只有点光、聚光、平行光是不够的，需要 ambient 体积光补充
- Edge-filtering AA 极快，且不仅限于最终 framebuffer
- PS3 的 early-z 行为是个麻烦，PC DX9 调试工具匮乏

## 链接到的概念

- [[deferred-rendering]]
- [[deferred-rendering-mythbusting]]
- [[tiled-light-prepass]]
- [[batching]]
- [[culling]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/09/what-ive-learned-from-shipping-deferred.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-09-08_what-i-ve-learned-from-shipping-a-deferred-lighting-renderer.md`
