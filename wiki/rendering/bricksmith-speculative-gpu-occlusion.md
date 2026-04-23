---
tags: [渲染, 剔除, occlusion, bricksmith, vertex-bound, gpu-driven, transform-feedback, 反面案例]
date: 2026-04-19
sources: 1
---

# BrickSmith 推演的 GPU 遮挡剔除：为什么"可行但不可部署"

[[ben-supnik|Supnik]] 2013-08 *Theoretical Engineering: Occlusion Culling for BrickSmith* 做了一次公开的推演——在 LDraw 这种**顶点 bound 而非 fill-rate bound** 的罕见场景下，一套完整的 GPU-side 实例级遮挡剔除**长什么样**，以及**为什么最后决定不发车**。时间点上这篇比 [[gpu-based-occlusion-culling|Kostas Anagnostou 2017 那一条系列]]早四年，用的是 geometry shader + transform feedback 而非 compute + stream compaction，可看作早期 DX11-class GPU culling 的思路映照。

## 问题形状：少见的纯顶点瓶颈

BrickSmith 已经用 attribute-divisor instancing 把大模型推到 GPU，bricks 在 VBO 里、shader 简单、viewport 有时很小——125M 顶点塞过 GPU 时**瓶颈纯粹是顶点吞吐**，不是 fill、不是 CPU。多数 3D 系统的架构预设不会让这种情况出现，所以 Supnik 开头就强调："当你的 GPU 不在被上一帧像素拖慢时，哪怕 GPU 命令涉及很少顶点，也能很快完成"——这是后文算法能跑快的前提。

## 推演出的 pipeline

1. **每个部件预切两套几何**：
   - **crude occluders**：非透明、足够大的三角形 / 四边形，不含线；目标是"少顶点换快速 fill"，比如 2×4 积木就是外面 5 个顶面与侧面。
   - **the rest**：内腔、studs、tubes、边缘细节、线画。
2. **每块 brick 归一化到单位立方体**——实例数据里携带包含缩放的 4×3 变换，这样光靠 instance 数据就能推出 bounds。
3. **Off-screen RT + 直读 depth**：为最终 blit 回屏幕做准备，先把 depth 单独握在手上。
4. **正常跑现有引擎**：traverse 数据模型，生成 opaque instance list（半透明扔到 holding bay），这一步 CPU 已足够快。
5. **只画 crude occluders**：实例列表 × 占空间小的几何，early-Z 能起作用，做一张基础 depth。
6. **depth pyramid via ping-pong**：不断 render-to-texture 用 "**farthest**" 策略降采样——一个低分 texel 是它覆盖的 4 个高分 texel 里**最远**的深度，保守判是否可见。
7. **GPU cull via geometry shader**：每个 instance 走一个"vertex"进 GS——因为 instance 数据在 BrickSmith 是 4×3 仿射 + 两组 RGBA（共 20 float / 5 attrib），GS 算它的屏幕 AABB、对应 mip 层 fetch depth、bounds.minZ > pyramid.maxZ ⇒ 完全被挡 ⇒ 丢弃，否则输出 1 顶点。
8. **transform feedback 回收**：GS 输出进 transform feedback，后续用 `glDrawTransformFeedbackStreamInstanced` 让 GPU **自己知道有多少幸存 instance 要画**，CPU 不参与。
9. **画 the rest**：用压缩后的 instance list 再发起一次 draw——被遮的 brick 几乎 97% 顶点都省掉了。

## 为什么不发车

Supnik 诚实地列出**四条 show-stopper**，每条都值得单独记住：

1. **内容管线代价**：整个 LDraw part library 得手工 / 半自动地拆分成 crude occluder + rest，且结果**无法回灌**进 LDraw 格式——工作量比整次 renderer 重写还大，而 BrickSmith 是爱好项目。
2. **硬件基线太激进**：instanced transform feedback 是 OpenGL 4.2 feature，要求 DX11-class GPU。2013 年 Apple 甚至还没交付 OpenGL 4.0，上这套等于砍掉 Lion / Mountain Lion。
3. **per-brick VBO 代价**：为了让每个 brick 拿到自己的"幸存 instance 数"，可能需要每个 brick 一条 transform feedback VBO，draw 数翻倍；或者走 multi-draw-indirect / compute / atomic 写一张总 buffer，后两条 2013 年的 GL 生态尚不稳定。
4. **最后一根稻草是工程尺度**：BrickSmith 是业余项目；这套 pipeline 实现量比之前重写整条 renderer 还多，没人有预算。

文末他用 Daniel Rákos 的文章补了个 **edit**：如果用**异步 query 回读 feedback 顶点数**，可以把 instance 源头保留成一个大 VBO，省去 per-brick VBO；**但** Rákos 方案意味着 CPU-GPU 同步点。BrickSmith 的未同步版本本来能让帧迟到也不卡主线程，一旦引入回读就破坏了这个性质。

## 结论与更宽的意义

Supnik 的落地判决是**"直接在远视角上用更粗糙的 LOD 模型，回家开心"**——但他把推演写下来的理由是：一旦把完整算法搬到纸上，**可行性四个 failure mode 非常具体**，以后别人再问"要不要上遮挡剔除"时，可以直接把这四条对上清单。

这套推演在 wiki 的坐标：

- 跟 [[gpu-based-occlusion-culling|Anagnostou 2017 那一条]] 对照——后者用 compute + prefix scan + `DrawIndexedInstancedIndirect` 解决了 Supnik 当年**四条里的第三条**（per-brick VBO），剩下三条仍然受内容管线与项目形态决定。
- 它也反向印证了 [[occlusion-culling]] 里"**硬件 OQ 粒度与延迟都不对**"的论断——BrickSmith 选 OQ 同样不可行，才会被迫推演这套 HZB + GS + TFB 的早期 GPU culling。
- 把本案例记到顶点 bound 这个**非典型瓶颈**类别下：[[bottleneck-analysis]] 里的标准行"降低分辨率 FPS 几乎不变 ⇒ CPU 或 Geometry"对应的就是 BrickSmith 这种形状。

## 相关

- [[occlusion-culling]] —— 剔除方案全景
- [[gpu-based-occlusion-culling]] —— 2017 compute shader + stream compaction 落地版
- [[hierarchical-z-buffer]]
- [[gpgpu-transform-feedback-ios]] —— 用 transform feedback 做非渲染计算的同宗思路
- [[bricksmith-instancing-pipeline]] —— BrickSmith 本身的 instancing pipeline，本文 pipeline 的前提
- [[bottleneck-analysis]]
- [[xplane-instancing-2011-numbers]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-bricksmith-speculative-occlusion]]
