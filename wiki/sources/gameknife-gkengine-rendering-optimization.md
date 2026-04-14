---
tags: [source, 渲染, 性能优化, gkengine]
date: 2026-04-14
sources: 1
---

# gkENGINE 渲染优化（gameknife, 2013-06）

[[people/gameknife|gameknife]] 发表于 2013 年 6 月的一篇实战优化总结。作者把 [[gkengine|gkEngine]] DEMO 的开场镜头从 GTX 560 上 **104 FPS 拉到 241 FPS（240 % 提升）**，并在博客中完整复盘了三轮优化的思路与权衡。文章同时记录了作者对 Intel GPA 老版本（4.3）的偏爱、对 PIX 与 PerfHUD 稳定性的不满，以及 gkEngine 即将开源至 CodePlex 的时点。

## 摘要

文章围绕"Intel GPA 测出的瓶颈 → 针对性砍像素计算"这条主线展开。初测的瓶颈集中在 SSAO、shadow mask、postprocess、以及场景无水面却仍在生成的 reflect map——全部是 pixel-bound 任务。第一轮作者引入 [[dynamic-resolution-scaling|变分辨率渲染]]：SSAO 和 shadow mask 走半分辨率，postprocess 合理安排 RT 顺序减少 stretch，最后把 backbuffer 之外的所有 RT 统一按 0.75 缩放，把像素计算量砍到接近一半。shadow mask 半分辨率引入的白边通过"右下偏移取 min"修掉。第二轮补锐化与地形 shader 的精修：地形因为内部用 `frac` 生成 texcoord 只能关 mipmap，改用深度手动计算 mip level，并把 `tex2Dlod` 换成 `tex2Dgrad` 绕开一条隐藏的双采样展开，地形 block 的采样次数从 26 次降到 9 次；高光贴图被合并进 diffuse 的 alpha 通道。第三轮作者抽象出 `IBasePipe` 策略模式，引入可切换的 [[deferred-rendering|Deferred Shading]] 管线与原本的 Deferred Lighting 并存，实验 Crytek GDC 2013 提出的 Hybrid Deferred Shading——deferred shading 让 DP 减半、G-Buffer 带宽压力涨 50 %，净收益 5 %，但材质一致性要求更高，最终 gkEngine 仍默认走 deferred lighting。

## 关键要点

- **先剖析后优化**：Intel GPA 4.3 把 GPU 时间精确分配到每个 pass，瓶颈先于修改出现。作者强调自己偏好 GPA 旧版本而非新版，也不太信任 PIX/PerfHUD 的稳定性。
- **0.75× 渲染尺寸 + 锐化 pass** 是最"终极"的单点优化。shader `color = lerp(blur, curr, k); // k > 1` 做 unsharp mask，补偿缩放引入的"压缩感"。
- **半分辨率 shadow mask 的白边 workaround**：着色阶段对右下方像素多采一次阴影值，两者 min。副作用是可能在无阴影处出现轻微黑边，但黑边比白边更不显眼。
- **`tex2Dlod` 陷阱**：DX9 世代下 `tex2Dlod` 在 GPA 中会显示两次采样指令，比 `tex2Dgrad` 更贵。手动用像素线性深度算 mip，再走 `tex2Dgrad` 送入 ddx/ddy，地形采样次数砍半。
- **地形高光合进 diffuse.alpha**：多采一张 spec 贴图不值，单色 spec 合并到 diffuse alpha 直接砍一次 tex sample。
- **IBasePipe 策略模式**：把 `shadowmapgen / zpass / ssao / shadowmask / deferred lighting / general pass / postprocess` 每一阶段抽象为 pipe 接口，允许 deferred lighting 和 deferred shading 在运行时切换。为日后的 Hybrid Deferred Shading 做铺垫。
- **Deferred Shading 实测**：DP 减半，但 G-Buffer 从 `DEPTH(R32F) + NORMAL+GLOSS(RGBA8)` 扩到多出 `ALBEDO+SPEC(RGBA8)` 的 MRT，带宽涨 50 %，净性能提升仅 5 %，材质属性统一难度上升——作者选择默认保留 deferred lighting。
- **最终战绩**：1280×720、35.9 万三角面、362 drawcall、特效全开、0.75 渲染尺寸。GTX 560 @ 241 FPS / 4.14 ms；GT 650M @ 140 FPS；Intel HD 3000 @ 30 FPS。

## 链接到的概念

- [[dynamic-resolution-scaling]]
- [[bottleneck-analysis]]
- [[deferred-rendering]]
- [[sampler-filter-wrap-modes]]
- [[gkengine]]
- [[people/gameknife]]

## 原文

- 链接：<http://gameknife.github.io/tech/2013/06/11/gkengine-opt/>
- 本地：`raw/articles/gameknife.github.io/2013-06-11_gkenginexuan-ran-you-hua.md`
