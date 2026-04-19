---
tags: [unity, 音频, audio, 游戏开发]
date: 2026-04-19
sources: 1
---

# Unity 6 AudioResource / AudioRandomContainer

Unity 6 引入 **`AudioResource`** 作为 `AudioClip` 和 `AudioRandomContainer`（ARC）的共同基类，把"播放器接受的 audio 资源"抽象了一层。ARC 本身是一个可以包装多个 `AudioClip` 并指定播放策略（shuffle / sequential / 间隔 / 循环）的资产。Sirawat Pitaksarit 在做 SFX 播放插件时对这套 API 做了一轮系统踩点，结论谨慎：特性丰富但**不适合"全家桶"式地替换项目里所有 `AudioClip`**。

## AudioClip 的内存与生命期回顾

- **Preload Audio Data** 勾上 + 场景引用 → 启动/加载场景时就占内存；未勾 → 首次播放时加载。Streaming 类型不可 Preload。
- `AudioClip.UnloadAudioData()` 手动卸载，正在 `PlayOneShot` 的实例会被强制停止。
- `Resources.UnloadUnusedAssets()` 按引用图扫描——Hierarchy 里有任何 GameObject 引用这个 clip 都不会被卸载，即便没在播放。
- Streaming 每个并发播放独立占 ~124 KB；同一 Decompress-on-Load / Compressed-in-Memory clip 的多个并发播放共享数据。

**Preload + 手动 unload 是重要 SFX（如升级音效）的最佳实践**——首播不能丢帧，玩完后手动卸降内存压力。

## `AudioSource.PlayOneShot` 的边界

- 参数类型是 **`AudioClip` 不是 `AudioResource`**——ARC 不能 PlayOneShot（因为 ARC 可能无限循环，one-shot 语义无从定义）。
- 叠播的 PlayOneShot 在 Profiler 里表现为新增"Audio Voices"，不增加"Total Audio Sources"——voices 会被 `Max Real Voices`（Project Settings）剔除。
- 在 voice 正在播时修改 `AudioSource` 的 Volume / Pitch / AudioMixerGroup，**所有 one-shot 实例实时生效**——可以把一组 SFX 整体挪到 mixer 的另一分支。

## ARC 的黑盒实现

Profiler 暴露了 ARC 的底层：**`AudioPlayable Group`**——ARC 走的是 Audio Playable Graph，不是传统 AudioSource。一旦某 source 播过 ARC，它会持有这个 playable group 即便换了 `AudioResource`，group 会跟着搬到 mixer tree 的新位置。Profiler 里 ARC 产生的 channel **name 是空的**，对着 frame 检视时还会因暂停编辑器跳帧（因为 Profiler pause editor），需要手动回退一帧。

过渡瞬间 Audio Voices 会短暂 +1（两个 clip 重叠 ≈ 1 ms），和 ARC 设置里"不允许 overlap"的 UI 承诺相矛盾——底层实现没法完全做到瞬态切换。

## `.Play()` 在 ARC 上的语义反转

- 资源是 `AudioClip`：重复 `Play()` 会 **abort + restart** 当前播放。
- 资源是 ARC + Trigger=Manual：`Play()` 是一次**"trigger"**——连续调 4 次等价于 overlay 4 份——类似 PlayOneShot 的语义。Pause/Unpause 可以一口气管理所有叠播实例。
- 资源是 ARC + Trigger=Automatic：回到"restart"语义。

这种"同一个 API 在两种资源下行为完全不同"是容易踩的陷阱。

## 为什么作者不迁到 ARC

Sirawat 花 1-2 年写过一个基于 Audio Playable Graph 的 SFX 插件（One Shot Framework），和 ARC 思路高度重合——结果在生产用途中被 FMOD 底层报错淹没、WebGL 构建完全 broken（Unity 文档对此只字未提），最后把插件降级成纯 `PlayOneShot` wrapper。ARC 在运行时同样走 playable graph，他对这条路重新信任不起来。

更硬的障碍是 **`AudioRandomContainer` 类是 `internal`**：

- 无法反射之外的方式访问 `AudioContainerElement` 数组——内部存的不是 `AudioClip` 而是"带 per-clip volume / enabled"的 wrapper struct。
- 想对 ARC 播放列表里的所有 `AudioClip` 做 `UnloadAudioData()` 需要外部另存一份引用；300+ SFX 各带 2-3 变体时这个负担很大。
- 编辑器里只能手建 ARC 资产，没有"把一堆同名 clip 自动打包"的工具。

作者的决定：**继续自研 `AudioClip` wrapper**（类似 ARC 但走 `PlayOneShot`），不 base 在 `AudioResource` 上——等 Unity 把 ARC 公开、提供脚本化创建和内部 clip 访问，再考虑迁移。

## 相关

- [[ecs]]
- [[unity-complexity-patterns]]
- [[resource-system-design]]
- [[sirawat-pitaksarit]]

## Sources

- [[sources/gametorrahod-audio-random-container]]
