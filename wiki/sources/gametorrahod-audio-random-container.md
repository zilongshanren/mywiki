---
tags: [source, unity, 音频, audio]
date: 2026-04-19
sources: 1
---

# AudioResource, AudioClip, AudioRandomContainer Interactions（Sirawat Pitaksarit / Game Torrahod）

[[sirawat-pitaksarit]] 2025 年 10 月，为自研音频插件做 Unity 6 新 API 评估——`AudioResource`（`AudioClip` 和 `AudioRandomContainer` 的共同基类）和 `AudioRandomContainer`（ARC）。结论：功能诱人但**不适合全家桶式迁移**，作者决定继续 `PlayOneShot` 路线。

## 摘要

先回顾 `AudioClip` 的内存 / 生命期细节：**Preload Audio Data** 勾上 → 场景 load 时占内存，未勾 → 首播加载；Streaming 类型不可 Preload，且每个并发播放独立占 ~124 KB；Decompress-on-Load / Compressed-in-Memory 的多并发共享数据。`UnloadAudioData()` 手动卸载（会强停 running one-shot），`Resources.UnloadUnusedAssets()` 跟引用图——Hierarchy 有任何 GameObject 引用就不卸载。

`AudioSource.PlayOneShot` 的参数是 `AudioClip` 而不是 `AudioResource`——ARC 不能 one-shot（ARC 可能无限循环，语义无法定义）。叠播的 one-shot 在 Profiler 里表现为新增 "Audio Voices"（受 `Max Real Voices` 剔除），不增加 "Total Audio Sources"。在播期间改 source 的 Volume/Pitch/MixerGroup 会**实时影响所有并发 one-shot 实例**。

ARC 的底层：Profiler 露馅是 **`AudioPlayable Group`**——ARC 走 Audio Playable Graph 不走传统 AudioSource。过渡瞬间有短暂 Audio Voices +1（约 1 ms 重叠），即便 ARC UI 声明"不允许 overlap"也是如此。`.Play()` 在 ARC 上语义和 `AudioClip` 反着来：Trigger=Manual 下 `.Play()` 是"trigger"，连续调等价于 overlay（类似 PlayOneShot），Pause/Unpause 一口气管理；Trigger=Automatic 下回到 abort+restart。

作者不迁的理由：(a) 他自己 2022-2024 年写过类似插件，Audio Playable Graph 在生产用途被 FMOD 底层报错淹没 + WebGL 彻底 broken，最后降级成 PlayOneShot wrapper；(b) `AudioRandomContainer` **类是 `internal`**——没法公开访问 `AudioContainerElement` 数组，要对 ARC 内的 `AudioClip` 做 `UnloadAudioData` 就得外部另存引用；没有批量"把同名 clip 自动打包"的编辑器工具。

## 关键要点

- Preload + 手动 unload 是重要 SFX（如 level-up 音效）的最佳实践——首播不丢帧，完后释放内存。
- Streaming 每并发独立 124 KB，多并发别用 Streaming。
- ARC 不能 `PlayOneShot`（参数类型强制）——想要"叠播"只能 Trigger=Manual + `.Play()`。
- ARC 走 Audio Playable Graph，过渡瞬间有 short voice overlap，bloat "Audio Voices" 注意接近 `Max Real Voices` 上限。
- `AudioRandomContainer` `internal` → 不能通过脚本访问内部 `AudioClip` → 大规模生产不好管内存。
- `.Play()` 在 ARC(Manual) 上是 trigger 语义，连续调 = overlay；在 AudioClip / ARC(Automatic) 上是 abort+restart。

## 链接到的概念

- [[unity-audio-random-container]]
- [[resource-system-design]]
- [[unity-complexity-patterns]]

## 原文

- 链接：https://gametorrahod.com/audio-random-container/
- 本地：`raw/articles/gametorrahod.com/2025-10-09_audioresource-audioclip-audiorandomcontainer-interactions.md`
