---
tags: [source, 渲染, temporal, ssao, 环境光遮蔽]
date: 2026-04-14
sources: 1
---

# Temporal supersampling pt. 2 – SSAO demonstration（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 4 月的博文，是 [[sources/bartwronski-temporal-supersampling|temporal supersampling 基础篇]]的续集——他为 Digital Dragons 2014 准备 slides 时终于抽时间补做了 **_Assassin's Creed 4: Black Flag_ 上 temporal SSAO 的前后对比截图和视频**，并解释为什么这个改动「几乎零成本」却效果惊人。

## 摘要

AC4 的基础 SSAO 用的是 McGuire 的 **Scalable Ambient Obscurance**（[1]），在主机上全分辨率 + 两次 bilateral blur 只花 ~1.6 ms，最大 1.5 m 半径。Wronski 把[[temporal-supersampling|temporal supersampling]]挂到 AO 计算上——**3 套屏幕空间采样图案按帧轮换**（每个屏幕像素位置的图案也是 unique 的，所以每 3 帧才回到同一状态），把前一帧的 AO 缓冲按[[motion-vectors|motion vectors]]重投影、做深度 rejection / acceptance、以 0.9 历史权重指数衰减累加。**静态画面下等效把 AO 样本数乘以 3**——这不稀奇。真正惊人的是**运动画面**：相机一动，每个像素从不同历史像素拉回样本，**等效样本数可以到几百倍**，SSAO 的 undersampling、flickering、桌角脏 pattern 全部消失。

在算法选择上他解释了几处细节。**为什么在 AO pass 而不是 blur 后做 temporal？**——因为 blur 已经把样本的信息低通掉了、细节丢了，在 blur 前做时域累积才是真的增加样本数，细节保留得更好。**为什么用深度 rejection 而不是 color clamping？**——Scalable AO 把 16-bit 深度压到 2 个 8-bit 通道塞进 AO 纹理里（原本是为了加速 bilateral blur 时只做单 sample tap），这意味着**fetch AO 的同时就拿到了深度**，depth rejection 是零成本附赠的。motion vectors 和 temporal AO 表都是 8-bit，cache 友好，整体没有看到额外开销。depth rejection 的一个已知缺陷是 occluder 消失时信息会"拖影"（occluded 像素没办法知道 occluder 没了），但他和测试人员都没看到这个 artifact——AC4 的 SSAO 本身就调得很 subtle，好的技术美术功不可没。

和前人工作的区别也说得很清楚。DICE 的 _Battlefield 3_ 和 Epic 的 _Gears of War_ 都做过类似的 temporal SSAO，但**动机不同**：他们是为了**平滑 flickering**（尤其 HBAO 半分辨率版），只对"不稳定"的像素做时域混合。Wronski 的思路是把 SSAO 当成 TAA 的分支问题——**目的就是多样本**，所以 rejection 启发式相反：**尽可能多地保留历史**，除非深度变了。

## 关键要点

- **temporal SSAO = 3 采样图案轮换 + 深度 rejection + 0.9 历史权重累积**。
- **动机和其他实现不同**：不是为了降低噪声，是为了真正的多样本超采样。因此 rejection 启发式相反——"尽量多保留历史"。
- **零成本附赠**：Scalable AO 已经把 depth 压到 AO 纹理，rejection 用的 depth 和 color 同一次 fetch 拿到。
- **blur 前做 temporal**：信息还没被低通，细节保留更好。
- **motion 下比 static 下提升更大**：每个像素从不同历史像素拉样本，等效样本数成百倍上升。
- **SSR / GI / AA 等 stochastic 采样效果**全部适用这个思路——Wronski 结尾挑衅："你还没给它们加 temporal 的理由是什么？"
- **落地速度**：AC4 temporal SSAO 是和 PS4 分辨率提升 + TAA 同一个 title update 发的，Wronski 把 motion vectors 挂过去、调一下参数就上线了，当时连完整 before/after 都没时间做。

## 链接到的概念

- [[temporal-supersampling]]
- [[hbao-interleaved-sampling]]
- [[motion-vectors]]
- [[depth-aware-upsampling]]
- [[temporal-antialiasing]]
- [[taa-history-rectification]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/04/27/temporal-supersampling-pt-2-ssao-demonstration/
- 本地：`raw/articles/bartwronski.com/2014-04-27_temporal-supersampling-pt-2-ssao-demonstration.md`
