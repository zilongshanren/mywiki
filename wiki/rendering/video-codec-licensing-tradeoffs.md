---
tags: [视频, 编解码器, 专利, 授权, 引擎设计, bitsquid]
date: 2026-04-19
sources: 1
---

# 视频编解码：技术之外的授权博弈

[[niklas-frykholm|Niklas Frykholm]] 在 2012 年写 Bitsquid 的视频播放选型时，开门见山地点明：真正难的不是对接一个 `play_video()` 函数，而是**专利沼泽**——上千项涉及视频解压的专利，随便踩中一项就可能被诉。"mutually assured destruction through lawyers" 是他对现状的讽刺。

## 三层结构的澄清

一个常被误解的基本概念：一个视频文件由三部分组成：

- **视频数据**（H.264 / DivX / Theora / VP8 …）
- **音频数据**（MP3 / AAC / Vorbis …）
- **容器格式**（AVI / MKV / MP4 / OGG …）

容器只是把音视频打包在一起并附加索引、多音轨、字幕等元信息。扩展名 `.mp4` 只告诉你容器是 MP4，**并不等同于里面的 codec 是什么**——这也是播放器常常"能打开但播不出"的根因。

## 五条路线的对比

Niklas 用同一把尺子（技术风险 / 授权风险 / 成本）评估候选：

1. **Just say no**——全部 cutscene 用 in-game 渲染。优点列得很明白（可复用资源、按用户设置渲染分辨率、可动态换装）；但 Bitsquid 是**通用引擎**，不能替客户做这个决定。
2. **Bink**（RAD）——业界事实标准，已用于 5800+ 款游戏。硬伤是定价：每平台每游戏 8500 USD，四平台就是 34000 USD，只为了一段 30 秒的片头——很多中小项目不划算。
3. **平台原生**（Windows Media Foundation / QuickTime / …）——免费且可能走硬件解码器（尤其手机 H.264 有硬解），但每新增一个平台就多一份后端工作，codec 支持差异、play-to-texture / 声音定位等能力不统一。
4. **H.264**——商业 codec 的画质王者，但 MPEG LA patent pool 里**1700 项专利**，97 页列表；而且不仅解码器要 license，**分发 H.264 内容本身也要 license**（>12 分钟按 0.02 USD/份计费）。即便买了 pool 的 license，也不排除被 pool 外的专利起诉。
5. **VP8 / WebM**（Google）——Google 宣称其专利免费使用，提供 BSD 许可的 libvpx。但 MPEG LA 放话过"我们认为它侵犯若干专利但不公开是哪些"，属于悬而未决的风险。画质略逊 H.264。

## Bitsquid 的决策

Bitsquid 选了 VP8：以 libvpx 作跨平台默认解码器，容器走极简的 IVF 流（不做 Matroska），音轨用 Vorbis 走自己的 3D 声音系统（这样能享受 positioning / reverb）。对低端设备可补以平台原生库吃硬解。

对于愿意付钱、视频需求重的客户，仍然建议接 Bink；担心 VP8 潜在专利风险的客户——"听你自己律师的"。

## 核心观察

三点 Niklas 给出的工程结论：

- **通用引擎不能替客户做 cutscene 哲学选择**——即使"in-game 渲染永远更好"在技术上成立。
- **license 的坏处不只是钱**，还有"哪种用法算 encoder / 哪种算 content"的模糊判定——游戏只播固定 cutscene 通常按 content 算。
- **没人能保护你不被起诉**。Google 不能、MPEG LA 不能、Bink 也不能。"风险"本身才是被买卖的东西。

## 相关

- [[niklas-frykholm]]
- [[volumetric-video-playback]] — 另一种视频形态的播放问题
- [[hdr-video-edr-metal]]
- [[middleware-vs-open-source]] — 同一类"买还是做"的取舍思路

## Sources

- [[sources/bitsquid-playing-with-video]]
- [[sources/chipsandcheese-4k-codecs]]
