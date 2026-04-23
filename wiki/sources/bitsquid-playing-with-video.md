---
tags: [source, bitsquid, video, licensing]
date: 2026-04-19
sources: 1
---

# Playing (with) Video — bitsquid: development blog

[[niklas-frykholm|Niklas Frykholm]] 2012 年 5 月的文章，把"给引擎加个视频播放"这个看似简单的任务拆解为**编解码器选型 + 专利授权 + 跨平台适配**三重问题。

## 摘要

视频播放的难点 90% 不在技术。任何商用 codec 都缠在数千项专利里——MPEG LA 的 H.264 patent pool 就有 1700 项专利，97 页清单。Bitsquid 把候选方案缩到五条：完全不做视频（全部走 in-game 渲染）、买 Bink（每平台每游戏 8500 USD）、用平台原生 API（Windows Media Foundation / QuickTime 等）、授权 H.264、选 VP8/WebM。Niklas 逐条列出风险与成本后选了 VP8——用 libvpx 做跨平台默认解码，容器用极简的 IVF 流，音轨走 Vorbis 接自家 3D 声音系统。担心 VP8 专利风险的客户可以退回 Bink 或 H.264。文章同时澄清一个基本概念：视频文件由**视频数据 + 音频数据 + 容器格式**三部分构成，扩展名只表示容器。

## 关键要点

- 视频播放的技术是小问题，专利才是大问题——H.264 patent pool 有 1700 项专利。
- 扩展名只代表容器，不代表 codec——`.mp4` 里也可能装 Theora。
- 平台原生 API 的最大好处是硬件解码器（尤其手机上的 H.264 硬解）。
- Bink 是事实标准，但定价对中小项目不划算。
- VP8/WebM 是 Bitsquid 选择的默认——最"free"给长期最大灵活性。
- 通用引擎不能替客户决定 cutscene 哲学；引擎只需提供一个能用的默认。

## 链接到的概念

- [[video-codec-licensing-tradeoffs]]
- [[middleware-vs-open-source]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/05/playing-with-video.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-05-20_playing-with-video.md`
