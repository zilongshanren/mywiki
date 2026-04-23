---
tags: [source, raytracey, 路径追踪, Brigade, 实时渲染]
date: 2026-04-19
sources: 1
---

# Real-time pathtracing demo shows future of game graphics（Sam Lapere, 2010-04-15）

[[sam-lapere|Sam Lapere]] 2010-04-15 的博客——把 [[jacco-bikker|Jacco Bikker]] 早期 [[brigade-engine|Brigade]] 原型的 YouTube 演示定性为"**游戏语境下第一个不丢人的实时路径追踪**"。

## 摘要

开头先挨个点名此前的所有"实时光追 for games"演示——Quake 3/4/Wars raytraced、Outbound、*Let there be light*、Intel Larrabee 版 Quake Wars、NVIDIA Bugatti——一句话结论：**都是 Whitted ray tracing，没有动态全局光照，画面比光栅化的 SSAO/SSGI/baked GI/Crytek LPV 还要平。**

随后切到 Bikker 的新视频：Core i7 + GTX260 混合架构，~40 Mrays/s，8 spp，带反射/焦散/运动模糊的动态场景。Lapere 盛赞"path tracing 的美妙之处在于软阴影、反射、折射、间接光全部自动化"，并在 UPDATE 部分补上一条 reddit 用户的数学解释：因为无偏路径追踪噪声方差随 1/N 下降，通过**4 帧样本平均**（相机静止时）把有效 spp 拉到 32，以工程技巧换质量。UPDATE 2 提到 Bikker 又放出新视频——**旋转光源 + 实时路径追踪 GI，14–18 fps**。

Lapere 判断这种慢节奏游戏（Myst / Outbound 风格）对低帧率和噪声最宽容，是实时路径追踪最早的落地场景。

## 关键要点

- 2010-04 Brigade 原型性能：i7 + GTX260，~40 Mrays/s，8 spp
- 与同期 Whitted demo 的本质差：**动态 GI**，软阴影 + 间接光 + 焦散 + 景深 + 运动模糊"免费"
- 帧间平均（temporal accumulation）拉有效 spp——与日后 RTX 的 TAA-style denoise 思路一脉相承
- 旋转光源版 GI demo 达到 **14–18 fps**，打消了"全动态 GI 不可能实时"的疑虑
- Lapere 对 GPU 十年加速的预测：**100–200×**，比读者评论里的 10× 激进得多（事实上 2010→2020 的 Turing RT Core + DLSS 组合大致验证了这个激进预测）

## 链接到的概念

- [[brigade-engine]]
- [[jacco-bikker]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[gpu-unbiased-path-tracing]]
- [[sam-lapere]]

## 原文

- 链接：http://raytracey.blogspot.com/2010/04/real-time-pathtracing-demo-shows-future.html
- 本地：`raw/articles/raytracey.blogspot.com/2010-04-15_real-time-pathtracing-demo-shows-future-of-game-graphics.md`
